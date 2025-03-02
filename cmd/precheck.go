package cmd

import (
	"fmt"
	"aks-upgrade-cli/internal/azure"
	"aks-upgrade-cli/internal/kubernetes"

	"github.com/spf13/cobra"
)

// preCheckCmd represents the pre-upgrade checks
var preCheckCmd = &cobra.Command{
	Use:   "precheck",
	Short: "Perform pre-upgrade checks before upgrading AKS",
	Long:  "This command validates breaking changes, PDB issues, network configurations, and tool compatibility before AKS upgrade.",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Starting pre-upgrade checks...")

		// 1. Check for breaking changes
		if err := azure.CheckBreakingChanges(); err != nil {
			log.Fatalf("Upgrade blocked due to breaking changes: %v", err)
		}		

		// 2. Validate PodDisruptionBudgets
		if err := kubernetes.CheckPDBs(); err != nil {
			log.Fatalf("PodDisruptionBudget check failed: %v", err)
		}

		// 3. Validate network configurations
		if err := azure.CheckNetworkSettings(); err != nil {
			log.Fatalf("Network validation failed: %v", err)
		}

		// 4. Validate tool compatibility
		if err := kubernetes.CheckToolCompatibility(); err != nil {
			log.Fatalf("Tool compatibility check failed: %v", err)
		}

		fmt.Println("Pre-upgrade checks completed successfully!")
	},
}

func init() {
	RootCmd.AddCommand(preCheckCmd)

	preCheckCmd.Flags().StringP("cluster", "c", "", "AKS cluster name (required)")
	preCheckCmd.Flags().StringP("resource-group", "g", "", "Azure resource group (required)")

	_ = preCheckCmd.MarkFlagRequired("cluster")
	_ = preCheckCmd.MarkFlagRequired("resource-group")
}
