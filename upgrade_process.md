

1. Get newest version:
az aks get-versions --location westeurope --output table

Breaking changes:
https://kubernetes.io/docs/reference/using-api/deprecation-guide/

https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions?tabs=azure-cli#aks-components-breaking-changes-by-version

Supported AKS versions:
https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions?tabs=azure-cli#aks-kubernetes-release-calendar

2. Upgrade Istio Operatorbefore AKS
thanks to that only one restart of all servcies is required

no need to check patch versions eg 1.20.1 as patches cannot contain breaking changes
https://istio.io/latest/docs/releases/supported-releases/#support-status-of-istio-releases

https://istio.io/latest/news/releases/1.20.x/announcing-1.20/upgrade-notes/


3. Check PodDisruptionBudget [PDB]
kubectl get pdb -A
k get pdb -A | awk 'NR==1 || $5 ~ /0/'

if there are any PDB with Allowed Disruptions = 0 it will block upgrade

4. Network
During AKS upgrade one additional node is created and one node is upgraded at the time

- Azure CNI: every node pool uses 1 IP from Subnet. 
For upgrade it needs 1 IP + reserving IPs of maximum pods that can be deployed on node
(maximum pods)

If surge is set to default = 1 node and maximum pods is 110 it would require 111 free IPs for upgrade


- Kubenet - only 1 free IP is needed.
Kubenet uses private network inside AKS.


5. Check tools compatibility.
Keda, Kiali etc..

---

# AKS UPGRADE

## Full with AZ-CLI
kind of automatic, easiest but low control over the process

Check current status of Pods
k get pods -A

az aks get-upgrades --resource-group <rg name> --name <aks name> --output table
OR
az aks get-upgrades -g <rg name> -n <aks name> -o table

Upgrade controlplane and nodepools
az aks upgrade -g <rg name> -n <aks name> -k <aks version> --verbose

Control progress during upgrade
watch -n 5 'k get nodes'
watch -n 5 'k get pods -A'

Check situation of pods after upgrade and compare it to situation before upgrade

Update Kubernetes version in terraform cluster

## Control Plane + new NodePool

upgrade control plane
az aks upgrade -g [rg_name] -n [aks] -k [version] --control-plane-only --verbose

create new nodepool
exactly same as existing one but with desired K8S version

drain and delete old nodepool
k drain --ignore-daemonsets <node name>

drain all nodes in a nodepool
for host in `kubectl get nodes | grep aks-test | awk '{print $1}'`; do kubectl drain $host; done


we can also use cordon but it would require us to wait long time for services to redeploy they deployments so they go to new node
k cordon <node name>
for host in `kubectl get nodes | grep aks-test | awk '{print $1}'`; do kubectl cordon $host; done


# Istio upgrade
istioctl version
istioctl ps

check if all containers are updated
istioctl ps | grep -v 1.18.2

version of istio can also be checked by describing istiod pod in istio-system and looking at image version

also check istio/proxy sidecar version in a pod that you know is using it

2. Pick Istio Operator yaml fwith desired version



3. restart all pods to get new version of istio-proxy containers
k get ns
k rollout restart deploy -n [ns]
k rollout restart sts -n [ns]


. Known issues.
If you notice any known issue, please add it here.

5.1. LRS disks cannot be attached to node.
By default on AKS there is default Storage Class creating LRS disks. We already changed it on most of AKSes to have default Storage Class with ZRS disks.

The issue occurs with LRS disks if nodepool is created without specyfing availability zone - meaning nodes can be created in all zones. When pods are restarted during AKS ugprade, they might be scheduled on nodes in different zone than before, LRS disk exists only in one zone, therefore if pod is scheduled on node in different zone than disk, disk cannot be attached. We should always try to force projects to use ZRS disk and prepare default Storage Class for that.

quick solution / workaround: restart pod again and have hope it will be scheduled on node in same zone as disk, or edit deployment/sts and nodeselector to enforce scheduling pod on node in given zone (there is a label on node containing info about zone). This is only workaround, if you do so, inform SM of that project to take this topic up with developers team
long term solution: prepare default Storage Class with ZRS disk and move disk from LRS to ZRS (Disk swap LRS to ZRS) - take snapshot of existing disk > create new ZRS disk from snapshot > replace PV/PVC on the cluster
5.2. Updating stuck in progress / Operation conflict.
AKS upgrade cannot be performed because there is other operation on AKS running, similar error appeared for 'az aks upgrade' command when cluster stuck in 'Updating' status. To fix this, list all the pods and check if there are some unexpected statuses like 'ContainerStatusUnknown', delete those pods (if this is PROD environment, think twice and check if replica set will redeploy those pods).