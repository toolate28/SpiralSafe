#!/usr/bin/env bash
# Hook: Triggered when KENL knowledge relay occurs
set -euo pipefail

source "$(dirname "$0")/../lib/verification-gate.sh"

main() {
    local kenl_artifact="${1:-}"
    
    if [ -z "$kenl_artifact" ]; then
        echo "[HOOK] Error: No KENL artifact provided"
        exit 1
    fi
    
    echo "[HOOK] on-knowledge-relay: $kenl_artifact"
    
    # Record in ATOM trail (use absolute path)
    "$(dirname "$0")/../atom-track.sh" KENL "Knowledge relay: $kenl_artifact" "$kenl_artifact"
    
    # Verify knowledge → intention gate
    gate_knowledge_to_intention
    
    echo "[HOOK] Knowledge → Intention transition verified"
}

main "$@"
