#!/usr/bin/env bash
# Hook: Triggered when any verification gate fails
set -euo pipefail

main() {
    local gate_name="${1:-unknown}"
    local violation_details="${2:-}"
    
    echo "[HOOK] on-boundary-violated: $gate_name"
    
    # Log violation
    local timestamp
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    mkdir -p .claude/logs
    echo "{\"type\":\"boundary_violation\",\"gate\":\"$gate_name\",\"details\":\"$violation_details\",\"timestamp\":\"$timestamp\"}" >> .claude/logs/violations.jsonl
    
    # Create ATOM decision for violation
    ./scripts/atom-track.sh VIOLATION "Boundary violated: $gate_name" "none"
    
    echo "[HOOK] Violation logged and tracked"
}

main "$@"
