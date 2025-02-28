package cmd

import (
	"fmt"
	"github.com/spf13/cobra"
)

// healthCheckCmd represents the healthcheck command
var healthCheckCmd = &cobra.Command{
	Use:   "healthcheck",
	Short: "Check the health of an AKS cluster",
	Long:  "This command checks the health of an AKS cluster by validating node and pod statuses.",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Checking cluster health...")
		// TODO: Implement health check logic
	},
}

func init() {
	RootCmd.AddCommand(healthCheckCmd)

	healthCheckCmd.Flags().StringP("cluster", "c", "", "AKS cluster name (required)")
	healthCheckCmd.Flags().StringP("resource-group", "g", "", "Azure resource group (required)")

	_ = healthCheckCmd.MarkFlagRequired("cluster")
	_ = healthCheckCmd.MarkFlagRequired("resource-group")
}
