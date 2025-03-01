Implement the actual AKS upgrade logic using the Azure SDK for Go (github.com/Azure/azure-sdk-for-go).

Add logging support for tracking upgrade progress.

Allow running dry-run mode before applying upgrades.



cmd/ → Houses Cobra CLI commands.
internal/ → Core logic for AKS upgrades & health checks.
pkg/ → If you want reusable, public functions.
config/ → YAML config for storing defaults.
scripts/ → Optional helper Bash scripts.
tests/ → For unit and integration testing.
