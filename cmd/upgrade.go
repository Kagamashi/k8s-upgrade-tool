package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"aks-upgrade-cli/cmd"
	"aks-upgrade-cli/internal/azure"
	"github.com/spf13/cobra"
)

func main() {
	if err := cmd.Execute(); err != nil {
		log.Fatalf("Error: %v", err)
	}
}

// upgradeCmd represents the upgrade command
var upgradeCmd = &cobra.Command{
	Use:   "upgrade",
	Short: "Upgrade an AKS cluster",
	Long:  "This command upgrades an Azure Kubernetes Service (AKS) cluster to the specified Kubernetes version.",
	Run: func(cmd *cobra.Command, args []string) {
		subscriptionID, _ := cmd.Flags().GetString("subscription-id")
		resourceGroupName, _ := cmd.Flags().GetString("resource-group")
		clusterName, _ := cmd.Flags().GetString("cluster")
		kubernetesVersion, _ := cmd.Flags().GetString("version")

		if subscriptionID == "" || resourceGroupName == "" || clusterName == "" || kubernetesVersion == "" {
			log.Fatalf("Missing required flags: --subscription-id, --resource-group, --cluster, --version")
		}

		fmt.Println("Starting AKS cluster upgrade...")
		err := azure.UpgradeAKSCluster(subscriptionID, resourceGroupName, clusterName, kubernetesVersion)
		if err != nil {
			log.Fatalf("Failed to upgrade AKS cluster: %v", err)
		}

		fmt.Println("AKS cluster upgrade completed successfully!")
	},
}

func init() {
	cmd.RootCmd.AddCommand(upgradeCmd)

	upgradeCmd.Flags().String("subscription-id", "", "Azure Subscription ID (required)")
	upgradeCmd.Flags().String("resource-group", "", "Azure Resource Group (required)")
	upgradeCmd.Flags().String("cluster", "", "AKS Cluster Name (required)")
	upgradeCmd.Flags().String("version", "", "Kubernetes Version to upgrade to (required)")

	_ = upgradeCmd.MarkFlagRequired("subscription-id")
	_ = upgradeCmd.MarkFlagRequired("resource-group")
	_ = upgradeCmd.MarkFlagRequired("cluster")
	_ = upgradeCmd.MarkFlagRequired("version")
}
