package cmd

import (
	"fmt"
	"github.com/spf13/cobra"
)

// RootCmd represents the base command when called without any subcommands
var RootCmd = &cobra.Command{
	Use:   "aks-upgrade-cli",
	Short: "A CLI tool for automating AKS cluster upgrades",
	Long:  "This CLI tool automates Azure Kubernetes Service (AKS) cluster upgrades with check-gates and health checks.",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Welcome to AKS Upgrade CLI! Use --help for available commands.")
	},
}

func Execute() error {
	return RootCmd.Execute()
}
