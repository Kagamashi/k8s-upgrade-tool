#!/usr/bin/env python3

import argparse
import subprocess
import sys

def run_command(cmd):
    """Helper to run shell commands and capture output."""
    try:
        print(f"Running command: {cmd}")
        completed = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return completed.stdout.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{cmd}': {e.stderr.decode('utf-8')}")
        sys.exit(e.returncode)

def check_k8s_versions(location):
    """Check newest available AKS versions."""
    print("\nChecking newest AKS versions...")
    cmd = f"az aks get-versions --location {location} --output table"
    output = run_command(cmd)
    print(output)

def check_istio():
    """Check current Istio operator and sidecar versions."""
    print("\nChecking Istio operator version...")
    run_command("istioctl version")
    print("\nChecking active Istio sidecars...")
    run_command("istioctl ps")

def check_pdb():
    """Check for PodDisruptionBudget constraints."""
    print("\nChecking PodDisruptionBudgets with Allowed Disruptions = 0...")
    pdb_list = run_command("kubectl get pdb -A | awk 'NR==1 || $5 ~ /0/'")
    print(pdb_list)

def upgrade_aks(resource_group, aks_name, new_version, control_plane_only=False):
    """Perform AKS upgrade."""
    print("\nStarting AKS upgrade...")
    cmd = f"az aks upgrade -g {resource_group} -n {aks_name} -k {new_version} --verbose"
    if control_plane_only:
        cmd += " --control-plane-only"
    run_command(cmd)

def main():
    parser = argparse.ArgumentParser(
        description="kubectl plugin for automating AKS & Istio upgrades"
    )
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Example command: check pre-upgrade conditions
    check_parser = subparsers.add_parser("check", help="Check conditions before upgrade")
    check_parser.add_argument("--location", default="westeurope", help="Azure region")

    # Example command: upgrade AKS
    aks_upgrade_parser = subparsers.add_parser("aks-upgrade", help="Upgrade AKS cluster")
    aks_upgrade_parser.add_argument("-g", "--resource-group", required=True, help="Resource group name")
    aks_upgrade_parser.add_argument("-n", "--aks-name", required=True, help="AKS cluster name")
    aks_upgrade_parser.add_argument("-k", "--k8s-version", required=True, help="Desired Kubernetes version")
    aks_upgrade_parser.add_argument("--control-plane-only", action="store_true", help="Upgrade control plane only")

    # Example command: check Istio
    istio_parser = subparsers.add_parser("istio-check", help="Check Istio versions/operator")
    # You could also add an istio-upgrade subcommand

    args = parser.parse_args()

    if args.command == "check":
        # Perform all checks
        check_k8s_versions(args.location)
        check_istio()
        check_pdb()
        # You can add more checks for IP capacity, etc.
    elif args.command == "aks-upgrade":
        # Perform the upgrade
        upgrade_aks(args.resource_group, args.aks_name, args.k8s_version, control_plane_only=args.control_plane_only)
    elif args.command == "istio-check":
        check_istio()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
