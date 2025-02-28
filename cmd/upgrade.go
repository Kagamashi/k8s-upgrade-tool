package cmd

import (
	"fmt"
	"log"
	"aks-upgrade-cli/internal/azure"
	"aks-upgrade-cli/internal/kubernetes"

	"github.com/spf13/cobra"
)

// upgradeCmd represents the upgrade command
var upgradeCmd = &cobra.Command{
	Use:   "upgrade",
	Short: "Upgrade an AKS cluster",
	Long:  "This command upgrades an Azure Kubernetes Service (AKS) cluster to the latest stable Kubernetes version after performing necessary checks.",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Running pre-upgrade checks...")

		// Run pre-upgrade checks before proceeding
		if err := azure.CheckBreakingChanges(); err != nil {
			log.Fatalf("Upgrade blocked due to breaking changes: %v", err)
		}
		if err := kubernetes.CheckPDBs(); err != nil {
			log.Fatalf("Upgrade blocked due to PDB issues: %v", err)
		}
		if err := azure.CheckNetworkSettings(); err != nil {
			log.Fatalf("Upgrade blocked due to network configuration issues: %v", err)
		}
		if err := kubernetes.CheckToolCompatibility(); err != nil {
			log.Fatalf("Upgrade blocked due to incompatible tools: %v", err)
		}

		fmt.Println("Pre-checks passed. Proceeding with AKS upgrade...")
		// TODO: Implement actual AKS upgrade logic
	},
}

func init() {
	RootCmd.AddCommand(upgradeCmd)

	upgradeCmd.Flags().StringP("cluster", "c", "", "AKS cluster name (required)")
	upgradeCmd.Flags().StringP("resource-group", "g", "", "Azure resource group (required)")
	upgradeCmd.Flags().BoolP("auto-approve", "y", false, "Automatically approve the upgrade")

	_ = upgradeCmd.MarkFlagRequired("cluster")
	_ = upgradeCmd.MarkFlagRequired("resource-group")
}
