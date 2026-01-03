#!/usr/bin/env bash
# Hook: Triggered when wave.md excavation completes
set -euo pipefail

source "$(dirname "$0")/../lib/verification-gate.sh"

main() {
    local excavation_file="${1:-.atom-trail/excavation-complete.json}"
    
    echo "[HOOK] on-excavation-complete triggered"
    
    # Record in ATOM trail (use absolute path)
    "$(dirname "$0")/../atom-track.sh" EXCAVATION "Wave.md excavation complete" "$excavation_file"
    
    # Verify gate to knowledge phase
    gate_understanding_to_knowledge
    
    echo "[HOOK] Excavation → Knowledge transition verified"
}

main "$@"
