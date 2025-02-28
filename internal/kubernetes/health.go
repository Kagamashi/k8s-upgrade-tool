package kubernetes

import (
	"fmt"
	"os/exec"
	"strings"
)

// CheckPDBs ensures no blocking PodDisruptionBudgets exist
func CheckPDBs() error {
	fmt.Println("Checking PodDisruptionBudgets (PDB)...")

	cmd := exec.Command("kubectl", "get", "pdb", "-A")
	output, err := cmd.Output()
	if err != nil {
		return fmt.Errorf("failed to fetch PDBs: %v", err)
	}

	lines := strings.Split(string(output), "\n")
	for _, line := range lines {
		if strings.Contains(line, " 0 ") {
			return fmt.Errorf("blocking PDB found! Inform SM or developers.")
		}
	}

	fmt.Println("No blocking PDBs found.")
	return nil
}

// CheckToolCompatibility checks for compatibility of tools like KEDA and Kiali
func CheckToolCompatibility() error {
	fmt.Println("Checking compatibility of installed tools (KEDA, Kiali)...")

	cmd := exec.Command("kubectl", "get", "pods", "-A", "|", "grep", "'keda\\|kiali'")
	output, err := cmd.Output()
	if err != nil {
		return fmt.Errorf("failed to check installed tools: %v", err)
	}

	if len(output) > 0 {
		fmt.Println("Found tools that may require updates:", string(output))
	}

	fmt.Println("Tool compatibility check completed.")
	return nil
}
