#!/usr/bin/env bash
# Hook: Triggered when ATOM task completes
set -euo pipefail

source "$(dirname "$0")/../lib/verification-gate.sh"

main() {
    local atom_tag="${1:-}"
    
    if [ -z "$atom_tag" ]; then
        echo "[HOOK] Error: No ATOM tag provided"
        exit 1
    fi
    
    echo "[HOOK] on-task-completed: $atom_tag"
    
    # Verify execution → learning gate
    gate_execution_to_learning
    
    # Extract learning
    echo "[HOOK] Task $atom_tag complete, learning extraction triggered"
}

main "$@"
