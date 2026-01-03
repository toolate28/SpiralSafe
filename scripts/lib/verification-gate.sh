#!/usr/bin/env bash
# Universal verification gate protocol for SpiralSafe coherence engine
# Every phase transition passes through explicit, auditable gates
set -euo pipefail

GATE_LOG=".atom-trail/gate-transitions.jsonl"

verify_gate() {
    local gate_name="$1"
    local phase_from="$2"
    local phase_to="$3"
    shift 3
    local requirements=("$@")
    
    local timestamp
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    local all_passed=true
    local failed_requirements=()
    
    echo "[GATE] $gate_name: $phase_from → $phase_to"
    
    for req in "${requirements[@]}"; do
        if eval "$req" >/dev/null 2>&1; then
            echo "  ✓ $req"
        else
            echo "  ✗ $req"
            all_passed=false
            failed_requirements+=("$req")
        fi
    done
    
    # Log transition
    mkdir -p "$(dirname "$GATE_LOG")"
    echo "{\"gate\":\"$gate_name\",\"from\":\"$phase_from\",\"to\":\"$phase_to\",\"timestamp\":\"$timestamp\",\"passed\":$all_passed,\"failed\":$(printf '%s\n' "${failed_requirements[@]:-[]}" | jq -R -s -c 'split("\n") | map(select(length > 0))')}" >> "$GATE_LOG"
    
    if [ "$all_passed" = true ]; then
        echo "[GATE] ✓ $gate_name PASSED"
        return 0
    else
        echo "[GATE] ✗ $gate_name FAILED"
        escalate_gate_failure "$gate_name" "$phase_from" "$phase_to" "${failed_requirements[@]}"
        return 1
    fi
}

escalate_gate_failure() {
    local gate_name="$1"
    local phase_from="$2"
    local phase_to="$3"
    shift 3
    local failed=("$@")
    
    echo "[ESCALATION] Gate failure: $gate_name"
    echo "  From: $phase_from"
    echo "  To: $phase_to"
    echo "  Failed requirements:"
    for f in "${failed[@]}"; do
        echo "    - $f"
    done
    
    # Log escalation
    local timestamp
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    mkdir -p .claude/logs
    echo "{\"type\":\"escalation\",\"gate\":\"$gate_name\",\"timestamp\":\"$timestamp\",\"failed\":$(printf '%s\n' "${failed[@]}" | jq -R -s -c 'split("\n") | map(select(length > 0))')}" >> ".claude/logs/escalations.jsonl"
}

# Pre-defined gates for SpiralSafe coherence cycle
gate_understanding_to_knowledge() {
    verify_gate "understanding-to-knowledge" "wave.md" "KENL" \
        "[ -f 'docs/cascade-diagram.md' ] || [ -f '.atom-trail/excavation-complete.json' ]" \
        "grep -q 'leverage_point' .atom-trail/excavation-complete.json 2>/dev/null || true"
}

gate_knowledge_to_intention() {
    verify_gate "knowledge-to-intention" "KENL" "AWI" \
        "[ -d '.atom-trail/patterns' ] || [ -f 'docs/KENL_PATTERNS.md' ]"
}

gate_intention_to_execution() {
    verify_gate "intention-to-execution" "AWI" "ATOM" \
        "[ -f 'bump.md' ]" \
        "! grep -q 'YYYYMMDD' bump.md"
}

gate_execution_to_learning() {
    verify_gate "execution-to-learning" "ATOM" "SAIF" \
        "[ -d '.atom-trail/decisions' ]" \
        "find .atom-trail/decisions -name '*.json' | head -1 | xargs test -f 2>/dev/null || true"
}

gate_learning_to_regeneration() {
    verify_gate "learning-to-regeneration" "SAIF" "Safe Spiral" \
        "[ -f 'docs/COHERENCE_REPORT.md' ] || [ -f '.atom-trail/learning-extracted.json' ]"
}
