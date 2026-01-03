#!/usr/bin/env bash
# Hook: Triggered when AWI intention is enforced
set -euo pipefail

source "$(dirname "$0")/../lib/verification-gate.sh"

main() {
    local intention_artifact="${1:-bump.md}"
    
    echo "[HOOK] on-intention-enforced: $intention_artifact"
    
    # Record in ATOM trail (use absolute path)
    "$(dirname "$0")/../atom-track.sh" INTENTION "Intention enforced: $intention_artifact" "$intention_artifact"
    
    # Verify intention → execution gate
    gate_intention_to_execution
    
    echo "[HOOK] Intention → Execution transition verified"
}

main "$@"
