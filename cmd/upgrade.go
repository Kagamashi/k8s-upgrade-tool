package cmd

import (
	"fmt"
	"github.com/spf13/cobra"
)

// upgradeCmd represents the upgrade command
var upgradeCmd = &cobra.Command{
	Use:   "upgrade",
	Short: "Upgrade an AKS cluster",
	Long:  "This command upgrades an Azure Kubernetes Service (AKS) cluster to the latest stable Kubernetes version.",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Starting AKS cluster upgrade...")
		// TODO: Implement the AKS upgrade logic
	},
}

func init() {
	RootCmd.AddCommand(upgradeCmd)

	// Example flags
	upgradeCmd.Flags().StringP("cluster", "c", "", "AKS cluster name (required)")
	upgradeCmd.Flags().StringP("resource-group", "g", "", "Azure resource group (required)")
	upgradeCmd.Flags().BoolP("auto-approve", "y", false, "Automatically approve the upgrade")

	_ = upgradeCmd.MarkFlagRequired("cluster")
	_ = upgradeCmd.MarkFlagRequired("resource-group")
}