#!/usr/bin/env bash
# Hook: Triggered when a complete coherence cycle finishes
set -euo pipefail

source "$(dirname "$0")/../lib/verification-gate.sh"

main() {
    local cycle_id="${1:-$(date +%Y%m%d-%H%M%S)}"
    
    echo "[HOOK] on-cycle-complete: $cycle_id"
    
    # Verify learning → regeneration gate
    gate_learning_to_regeneration
    
    # Record cycle completion
    local timestamp
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    mkdir -p .atom-trail
    echo "{\"type\":\"cycle_complete\",\"cycle_id\":\"$cycle_id\",\"timestamp\":\"$timestamp\"}" >> .atom-trail/cycles.jsonl
    
    # Create ATOM decision for cycle completion (use absolute path)
    "$(dirname "$0")/../atom-track.sh" CYCLE "Coherence cycle complete: $cycle_id" ".atom-trail/cycles.jsonl"
    
    echo "[HOOK] Learning → Regeneration transition verified"
    echo "[HOOK] Cycle $cycle_id complete and logged"
}

main "$@"
