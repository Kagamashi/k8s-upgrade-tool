# AKS Upgrade CLI

## Overview
The **AKS Upgrade CLI** is a command-line tool designed to automate the process of upgrading Azure Kubernetes Service (AKS) clusters. It includes pre-upgrade validation, cluster health checks, and post-upgrade verification to ensure a smooth upgrade process.

## Features
- **Pre-Upgrade Checks (`precheck`)**: Identifies potential upgrade blockers.
- **Cluster Health Check (`healthcheck`)**: Ensures AKS is in a good state before and after the upgrade.
- **AKS Upgrade Execution (`upgrade`)**: Performs the Kubernetes version upgrade on an AKS cluster.
- **Dry-Run Mode**: Simulates an upgrade without making changes.

## Prerequisites
- **Azure CLI installed** (`az` command available)
- **kubectl installed**
- **Authenticated with Azure (`az login`)**

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/aks-upgrade-cli.git
   cd aks-upgrade-cli
   ```
2. Build the CLI tool:
   ```sh
   go build -o aks-upgrade-cli
   ```
3. Run the tool:
   ```sh
   ./aks-upgrade-cli --help
   ```

## Usage

### 1. Run Pre-Upgrade Checks
Before upgrading, check for potential issues:
```sh
./aks-upgrade-cli precheck --cluster <CLUSTER_NAME> --resource-group <RESOURCE_GROUP>
```

### 2. Check AKS Cluster Health
Verify the health of the cluster before upgrading:
```sh
./aks-upgrade-cli healthcheck --cluster <CLUSTER_NAME> --resource-group <RESOURCE_GROUP>
```

### 3. Perform the Upgrade
Upgrade the AKS cluster to a specific Kubernetes version:
```sh
./aks-upgrade-cli upgrade --subscription-id <SUBSCRIPTION_ID> \
                          --resource-group <RESOURCE_GROUP> \
                          --cluster <CLUSTER_NAME> \
                          --version <K8S_VERSION>
```
Example:
```sh
./aks-upgrade-cli upgrade --subscription-id 12345-abcde-67890 \
                          --resource-group my-rg \
                          --cluster my-cluster \
                          --version 1.26.6
```

### 4. Perform a Dry Run
If you want to simulate the upgrade without applying changes:
```sh
./aks-upgrade-cli upgrade --subscription-id <SUBSCRIPTION_ID> \
                          --resource-group <RESOURCE_GROUP> \
                          --cluster <CLUSTER_NAME> \
                          --version <K8S_VERSION> \
                          --dry-run
```

## Notes
- Ensure that **Istio Operator** is upgraded before AKS to minimize service restarts.
- **Pod Disruption Budgets (PDBs) with `Allowed Disruptions = 0`** will block the upgrade. Developers must correct or remove these configurations.
- The upgrade process adds an extra node (surge) temporarily.
- Check **tool compatibility** for KEDA, Kiali, or any other deployed services before proceeding.

## Troubleshooting
If any command fails, check:
- `kubectl get nodes` to ensure nodes are in a **Ready** state.
- `kubectl get pods -A` to verify all workloads are running correctly.
- Logs using:
  ```sh
  ./aks-upgrade-cli upgrade --log-level debug
  ```

## Future Improvements
- Automate Istio upgrades before AKS upgrades.
- Auto-detect the latest stable Kubernetes version.
- Implement retry logic for transient failures.
- Improve structured logging and monitoring integrations.

## Contributors
- Your Name <your.email@example.com>
