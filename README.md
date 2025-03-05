# AKS and Istio Upgrade Process

This document explains how to upgrade an AKS cluster (control plane and node pools) alongside an Istio installation. It also shows how to automate large parts of that process with a custom Python-based `kubectl` plugin.

---

## Table of Contents

1. [Overview of the Upgrade Process](#overview-of-the-upgrade-process)  
2. [Prerequisites](#prerequisites)  
3. [Detailed Upgrade Steps](#detailed-upgrade-steps)  
   1. [Check Available Versions and Breaking Changes](#1-check-available-versions-and-breaking-changes)  
   2. [Upgrade Istio Operator Before AKS](#2-upgrade-istio-operator-before-aks)  
   3. [Ensure PodDisruptionBudgets Do Not Block the Upgrade](#3-ensure-poddisruptionbudgets-do-not-block-the-upgrade)  
   4. [Check Network Requirements](#4-check-network-requirements)  
   5. [Confirm Tool Compatibility (KEDA, Kiali, etc.)](#5-confirm-tool-compatibility-keda-kiali-etc)  
4. [Performing the AKS Upgrade](#performing-the-aks-upgrade)  
   1. [Full Upgrade with Azure CLI (Automatic Approach)](#1-full-upgrade-with-azure-cli-automatic-approach)  
   2. [Control Plane + New Node Pool (Granular Approach)](#2-control-plane--new-node-pool-granular-approach)  
5. [Upgrading Istio](#upgrading-istio)  
   1. [Check Current Istio Version](#1-check-current-istio-version)  
   2. [Apply New Istio Operator YAML](#2-apply-new-istio-operator-yaml)  
   3. [Restart Workloads to Update Istio Sidecars](#3-restart-workloads-to-update-istio-sidecars)  
6. [Known Issues](#known-issues)  
   1. [LRS vs. ZRS Disks](#1-lrs-vs-zrs-disks)  
   2. [Cluster Stuck in Updating State](#2-cluster-stuck-in-updating-state)  
7. [Using the Python-Based Plugin](#using-the-python-based-plugin)  
   1. [Installation](#1-installation)  
   2. [Commands Overview](#2-commands-overview)  
   3. [Usage Examples](#3-usage-examples)  
8. [References](#references)

---

## Overview of the Upgrade Process

1. **Check newest available Kubernetes versions** and any **breaking changes** in both Kubernetes and AKS.  
2. **Upgrade the Istio operator first**, so there is only one major service restart.  
3. **Verify PodDisruptionBudgets (PDBs)** are not set in a way that blocks the upgrade.  
4. **Confirm networking requirements** (especially with Azure CNI) to avoid IP exhaustion during node pool upgrades.  
5. **Check tool compatibility** (KEDA, Kiali, etc.) and ensure they are compatible with the target Kubernetes version.  
6. **Upgrade AKS** either:  
   - In one step via Azure CLI (less control, more automation).  
   - Or in a more controlled manner by upgrading the control plane first, creating a new node pool, draining and deleting the old node pool.  
7. **Upgrade Istio** (if not already covered):  
   - Patch or replace the Istio operator.  
   - Restart workloads to pick up the new sidecars.  
8. **Handle known issues**, like LRS disks failing to attach on different availability zones, or a cluster stuck in updating state.

---

## Prerequisites

- Azure CLI installed and authenticated (`az login`).  
- Kubernetes CLI (`kubectl`) and context set to the target AKS cluster.  
- `istioctl` installed if you manage Istio Operator.  
- Enough permissions to perform cluster upgrades, manipulate node pools, and change resources.

---

## Detailed Upgrade Steps

### 1. Check Available Versions and Breaking Changes

- **Check newest AKS/K8s versions**:  
    az aks get-versions --location westeurope --output table

- **Review potential breaking changes**:  
  - [Kubernetes Deprecation Guide](https://kubernetes.io/docs/reference/using-api/deprecation-policy/)  
  - [AKS Breaking Changes](https://docs.microsoft.com/azure/aks/upgrade-guide#breaking-changes)  
  - [AKS Supported Versions](https://docs.microsoft.com/azure/aks/supported-kubernetes-versions)

---

### 2. Upgrade Istio Operator Before AKS

- Ensures only one major restart of your services.  
- Check Istio’s supported releases and [upgrade notes](https://istio.io/latest/about/supported-releases/).

---

### 3. Ensure PodDisruptionBudgets Do Not Block the Upgrade

Check existing PDBs:

    kubectl get pdb -A

Or filter out ones with `Allowed Disruptions = 0`:

    kubectl get pdb -A | awk 'NR==1 || $5 ~ /0/'

Any PDB with `Allowed Disruptions = 0` might block upgrades. Consider temporarily adjusting or removing those PDBs.

---

### 4. Check Network Requirements

During an AKS upgrade, an additional node is temporarily created. Each new node requires:

- **Azure CNI**: One IP for the node, plus IPs for up to the maximum pods (defaults to 110).  
- **Kubenet**: Only one IP per node (the cluster uses internal IP addressing for pods).

If you use Azure CNI with the default `surge = 1` node, confirm you have enough free IPs in the subnet.

---

### 5. Confirm Tool Compatibility (KEDA, Kiali, etc.)

Make sure that external tools like KEDA, Kiali, or other controllers are compatible with the target Kubernetes version.

---

## Performing the AKS Upgrade

### 1. Full Upgrade with Azure CLI (Automatic Approach)

- **Check cluster status**:  
    kubectl get pods -A

- **Check available upgrades**:  
    az aks get-upgrades -g <resource-group> -n <aks-name> -o table

- **Upgrade control plane + node pools**:  
    az aks upgrade -g <resource-group> -n <aks-name> -k <target-version> --verbose

- **Monitor progress**:  
    watch -n 5 'kubectl get nodes'  
    watch -n 5 'kubectl get pods -A'

- **Post-upgrade checks**:  
  - Ensure pods match their previous state (same number of replicas, healthy, etc.).  
  - Update any IaC references (e.g., the Kubernetes version in Terraform).

---

### 2. Control Plane + New Node Pool (Granular Approach)

- **Upgrade control plane only**:  
    az aks upgrade -g <resource-group> -n <aks-name> -k <target-version> --control-plane-only --verbose

- **Create a new node pool** with the desired Kubernetes version.  
- **Drain and delete the old node pool**:  

    kubectl drain <node-name> --ignore-daemonsets

  Or, to drain every node in a node pool:
  
    for host in $(kubectl get nodes | grep <nodepool-label> | awk '{print $1}'); do
      kubectl drain $host --ignore-daemonsets
    done
  
  Once drained, you can safely delete the old node pool:
  
    az aks nodepool delete --resource-group <rg> --cluster-name <aks-name> --name <nodepool-name>

---

## Upgrading Istio

### 1. Check Current Istio Version

    istioctl version
    istioctl ps

Also check `istiod` pod images or the proxy sidecar images in your workloads.

---

### 2. Apply New Istio Operator YAML

    kubectl apply -f istio-operator.yaml  # containing the new version

---

### 3. Restart Workloads to Update Istio Sidecars

    # For each namespace with Istio sidecars:
    kubectl rollout restart deploy -n <namespace>
    kubectl rollout restart sts -n <namespace>

Confirm all pods are running the updated proxy version (e.g., `istio-proxy:1.20.0`).

---

## Known Issues

### 1. LRS vs. ZRS Disks

If a cluster uses **LRS** disks but the node pool is zonal (or spans multiple zones), a disk might fail to attach if the pod is scheduled in a different zone from the disk. The recommended solution is to use **ZRS** disks.

- **Workaround**: Manually reschedule the pod in the correct zone, or assign a node selector matching the disk’s zone.  
- **Permanent fix**: Create a default storage class with ZRS disks and migrate your volumes.

---

### 2. Cluster Stuck in Updating State

Sometimes an AKS upgrade is blocked if there is another conflicting operation. You might see errors like “Operation cannot be completed because cluster is updating.”

- Check for pods in unusual states (`ContainerStatusUnknown`, `Init:Error`, etc.) and remove them if needed.  
- Plan ahead for minimal disruptions to production pods.

---

## Using the Python-Based Plugin

### 1. Installation

1. Save the script as `kubectl-upgrade` (or another name prefixed with `kubectl-`).  
2. Make it executable:
    
        chmod +x kubectl-upgrade

3. Place it in your `PATH` (e.g., `/usr/local/bin/` or a similar directory).

---

### 2. Commands Overview

- **Check for the newest Kubernetes versions, Istio operator versions, and PodDisruptionBudgets**:
    
        kubectl upgrade check --location <azure-location>

- **Upgrade control plane and node pools to `<version>`**:
    
        kubectl upgrade aks-upgrade -g <resource-group> -n <aks-name> -k <version>
    
  Add `--control-plane-only` to upgrade only the control plane.

- **Check current Istio operator and sidecar versions**:
    
        kubectl upgrade istio-check

---

### 3. Usage Examples

    # 1. Perform pre-upgrade checks
    kubectl upgrade check --location westeurope

    # 2. Upgrade AKS cluster
    kubectl upgrade aks-upgrade -g MyResourceGroup -n MyAKSCluster -k 1.27.3

    # 3. Only upgrade control plane
    kubectl upgrade aks-upgrade -g MyResourceGroup -n MyAKSCluster -k 1.27.3 --control-plane-only

    # 4. Check Istio versions/operator
    kubectl upgrade istio-check

---

## References

- **Kubernetes**  
  - [Kubernetes Official Docs](https://kubernetes.io/docs/home/)  
  - [Kubectl Plugin Basics](https://kubernetes.io/docs/tasks/extend-kubectl/kubectl-plugins/)  
  - [Kubernetes Deprecation Guide](https://kubernetes.io/docs/reference/using-api/deprecation-policy/)  

- **AKS**  
  - [AKS Breaking Changes](https://docs.microsoft.com/azure/aks/upgrade-guide#breaking-changes)  
  - [AKS Supported Versions](https://docs.microsoft.com/azure/aks/supported-kubernetes-versions)  

- **Istio**  
  - [Istio Supported Releases](https://istio.io/latest/about/supported-releases/)  
  - [Istio Upgrade Notes](https://istio.io/latest/docs/setup/upgrade/)
