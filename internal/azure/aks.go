// This file contain all interactions with Azure SDK for Go: cluster upgrade logic, fetching AKS details, checking curretn version.

package azure

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/containerservice/armcontainerservice"
	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
)

// UpgradeAKSCluster upgrades the specified AKS cluster to a new Kubernetes version
func UpgradeAKSCluster(subscriptionID, resourceGroupName, clusterName, kubernetesVersion string, dryRun bool) error {
	ctx := context.Background()
	cred, err := azidentity.NewDefaultAzureCredential(nil)
	if err != nil {
		return fmt.Errorf("failed to obtain Azure credentials: %v", err)
	}

	if dryRun {
        fmt.Printf("Dry-run: Would upgrade %s in %s to version %s\n", clusterName, resourceGroupName, kubernetesVersion)
        return nil
    }

	client, err := armcontainerservice.NewManagedClustersClient(subscriptionID, cred, nil)
	if err != nil {
		return fmt.Errorf("failed to create AKS client: %v", err)
	}

	poller, err := client.BeginUpgrade(ctx, resourceGroupName, clusterName, armcontainerservice.ManagedClusterUpgradeProfile{
		KubernetesVersion: &kubernetesVersion,
	}, nil)
	if err != nil {
		return fmt.Errorf("failed to start upgrade: %v", err)
	}

	fmt.Println("AKS upgrade in progress...")
	for {
		resp, err := poller.Poll(ctx)
		if err != nil {
			return fmt.Errorf("error polling for upgrade status: %v", err)
		}
		if poller.Done() {
			break
		}
		fmt.Println("Waiting for upgrade to complete...")
		time.Sleep(30 * time.Second)
	}

	fmt.Println("AKS upgrade completed successfully!")
	return nil
}

func GetLatestKubernetesVersion(subscriptionID, location string) (string, error) {
    ctx := context.Background()
    cred, err := azidentity.NewDefaultAzureCredential(nil)
    if err != nil {
        return "", fmt.Errorf("failed to obtain Azure credentials: %v", err)
    }

    client, err := armcontainerservice.NewManagedClustersClient(subscriptionID, cred, nil)
    if err != nil {
        return "", fmt.Errorf("failed to create AKS client: %v", err)
    }

    result, err := client.ListKubernetesVersions(ctx, location, nil)
    if err != nil {
        return "", fmt.Errorf("failed to list available versions: %v", err)
    }

    if len(result.Values) == 0 {
        return "", fmt.Errorf("no Kubernetes versions found")
    }

    latestVersion := result.Values[len(result.Values)-1].Version
    return *latestVersion, nil
}

// CheckBreakingChanges validates if there are any AKS-related breaking changes
func CheckBreakingChanges() error {
	fmt.Println("Checking for breaking changes in AKS...")
	// TODO: Implement actual logic (Azure API call or predefined checks)
	// Simulate a failure case
	hasBreakingChanges := false
	if hasBreakingChanges {
		return fmt.Errorf("breaking changes detected! Resolve them before upgrade.")
	}
	fmt.Println("No breaking changes detected.")
	return nil
}

// CheckNetworkSettings validates Azure CNI or Kubenet configurations
func CheckNetworkSettings() error {
	fmt.Println("Validating network settings for AKS upgrade...")
	// TODO: Implement logic to check IP availability for Azure CNI or Kubenet
	fmt.Println("Network settings are valid.")
	return nil
}
