---
status: active
coherence_phase: execution
last_verified: 2026-01-03
verification_method: manual
atom_tags:
  - ATOM-COHERENCE-20260103-001-unified-deployment
intent: "Document the ATOM lifecycle hooks system for SpiralSafe coherence"
---

# ATOM Lifecycle Hooks

## Overview

ATOM lifecycle hooks are event-driven scripts that execute automatically at key transitions in the SpiralSafe coherence cycle. They enforce coherence boundaries, log transitions, and trigger verification gates.

## Available Hooks

### on-excavation-complete.sh

**Trigger**: When wave.md excavation completes  
**Purpose**: Transition from Understanding to Knowledge phase  
**Actions**:

- Records excavation completion in ATOM trail
- Verifies understanding-to-knowledge gate
- Logs transition

**Usage**:

```bash
./scripts/hooks/on-excavation-complete.sh [excavation-file]
```

### on-knowledge-relay.sh

**Trigger**: When KENL knowledge is relayed/enriched  
**Purpose**: Transition from Knowledge to Intention phase  
**Actions**:

- Records knowledge relay in ATOM trail
- Verifies knowledge-to-intention gate
- Logs transition

**Usage**:

```bash
./scripts/hooks/on-knowledge-relay.sh <kenl-artifact>
```

### on-intention-enforced.sh

**Trigger**: When AWI intention is enforced (bump.md filled)  
**Purpose**: Transition from Intention to Execution phase  
**Actions**:

- Records intention enforcement in ATOM trail
- Verifies intention-to-execution gate
- Validates bump.md is properly filled

**Usage**:

```bash
./scripts/hooks/on-intention-enforced.sh [intention-artifact]
```

### on-task-completed.sh

**Trigger**: When ATOM task execution completes  
**Purpose**: Transition from Execution to Learning phase  
**Actions**:

- Verifies execution-to-learning gate
- Triggers learning extraction
- Logs completion

**Usage**:

```bash
./scripts/hooks/on-task-completed.sh <atom-tag>
```

### on-cycle-complete.sh

**Trigger**: When complete coherence cycle finishes  
**Purpose**: Transition from Learning to Regeneration phase  
**Actions**:

- Verifies learning-to-regeneration gate
- Records cycle completion
- Creates cycle ATOM decision
- Logs to cycles.jsonl

**Usage**:

```bash
./scripts/hooks/on-cycle-complete.sh [cycle-id]
```

### on-boundary-violated.sh

**Trigger**: When any verification gate fails  
**Purpose**: Handle boundary violations  
**Actions**:

- Logs violation to violations.jsonl
- Creates ATOM decision for violation
- Triggers escalation (optional)

**Usage**:

```bash
./scripts/hooks/on-boundary-violated.sh <gate-name> [violation-details]
```

## Hook Architecture

### Event Flow

```
Event Occurs
    ↓
Hook Triggered
    ↓
ATOM Trail Updated
    ↓
Verification Gate Checked
    ↓
[Pass] → Log Success → Continue
    ↓
[Fail] → Escalate → on-boundary-violated.sh
```

### Integration Points

Hooks integrate with:

- **Verification Gates**: Enforce coherence boundaries
- **ATOM Trail**: Record all transitions
- **Logging System**: Create audit trails
- **CI/CD**: Automated coherence validation

## Creating Custom Hooks

To create a new hook:

1. Create script in `scripts/hooks/`
2. Follow naming convention: `on-<event-name>.sh`
3. Source verification-gate.sh if using gates
4. Record events in ATOM trail
5. Make executable: `chmod +x scripts/hooks/on-<event-name>.sh`

**Template**:

```bash
#!/usr/bin/env bash
# Hook: Triggered when <event occurs>
set -euo pipefail

source "$(dirname "$0")/../lib/verification-gate.sh"

main() {
    local param="${1:-}"

    echo "[HOOK] on-<event-name> triggered"

    # Record in ATOM trail
    ./scripts/atom-track.sh TYPE "Description" "$param"

    # Verify gate (if applicable)
    gate_<phase>_to_<phase>

    echo "[HOOK] Transition verified"
}

main "$@"
```

## Best Practices

1. **Always use hooks**: Don't bypass lifecycle events
2. **Keep hooks focused**: One responsibility per hook
3. **Log everything**: Record all state transitions
4. **Handle errors**: Gracefully handle hook failures
5. **Test hooks**: Verify hooks work before deployment
6. **Document triggers**: Clearly specify when each hook runs

## Debugging Hooks

To debug hook execution:

```bash
# Enable bash tracing
bash -x scripts/hooks/on-<hook-name>.sh <args>

# Check hook logs
cat .claude/logs/*.jsonl
cat .atom-trail/gate-transitions.jsonl

# Verify ATOM trail
ls -la .atom-trail/decisions/
```

## Hook Logs

Hooks create logs in:

- `.atom-trail/gate-transitions.jsonl` - Gate transitions
- `.atom-trail/decisions/` - ATOM decisions
- `.claude/logs/violations.jsonl` - Boundary violations
- `.claude/logs/escalations.jsonl` - Gate failures
- `.atom-trail/cycles.jsonl` - Cycle completions
