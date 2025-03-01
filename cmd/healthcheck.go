package cmd

import (
	"fmt"
	"log"

	"aks-upgrade-cli/internal/kubernetes"
	"github.com/spf13/cobra"
)

// healthCheckCmd represents the healthcheck command
var healthCheckCmd = &cobra.Command{
	Use:   "healthcheck",
	Short: "Check the health of an AKS cluster",
	Long:  "This command checks the health of an AKS cluster by validating node and pod statuses.",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Checking cluster health...")

		// Verify node readiness
		if err := kubernetes.VerifyClusterHealth(); err != nil {
			log.Fatalf("Cluster health check failed: %v", err)
		}

		// Check for blocking PDBs
		if err := kubernetes.CheckPDBs(); err != nil {
			log.Fatalf("Pod Disruption Budget issue detected: %v", err)
		}

		// Validate compatibility of installed tools (KEDA, Kiali)
		if err := kubernetes.CheckToolCompatibility(); err != nil {
			log.Fatalf("Tool compatibility check failed: %v", err)
		}

		fmt.Println("Cluster health check completed successfully!")
	},
}

func init() {
	RootCmd.AddCommand(healthCheckCmd)

	healthCheckCmd.Flags().StringP("cluster", "c", "", "AKS cluster name (required)")
	healthCheckCmd.Flags().StringP("resource-group", "g", "", "Azure resource group (required)")

	_ = healthCheckCmd.MarkFlagRequired("cluster")
	_ = healthCheckCmd.MarkFlagRequired("resource-group")
}
