---
status: active
coherence_phase: intention
last_verified: 2026-01-03
verification_method: manual
atom_tags:
  - ATOM-COHERENCE-20260103-001-unified-deployment
intent: "Document the verification gate protocol for SpiralSafe coherence"
---

# Verification Gates Protocol

## Overview

Verification gates are explicit, auditable checkpoints at every phase transition in the SpiralSafe coherence cycle. They ensure that:

1. Preconditions are met before proceeding
2. Transitions are observable and logged
3. Failures trigger escalation
4. Coherence is measurable

## The Coherence Cycle

```
Understanding (wave.md)
    │ [Gate: understanding-to-knowledge]
    ▼
Knowledge (KENL)
    │ [Gate: knowledge-to-intention]
    ▼
Intention (AWI)
    │ [Gate: intention-to-execution]
    ▼
Execution (ATOM)
    │ [Gate: execution-to-learning]
    ▼
Learning (SAIF)
    │ [Gate: learning-to-regeneration]
    ▼
Regeneration → [loops back]
```

## Gate Functions

### gate_understanding_to_knowledge
Verifies transition from wave.md excavation to KENL knowledge patterns.

**Requirements:**
- Excavation complete file exists or cascade diagram exists
- Leverage points identified in excavation

### gate_knowledge_to_intention
Verifies transition from KENL patterns to AWI intention.

**Requirements:**
- Pattern directory exists or KENL patterns document exists

### gate_intention_to_execution
Verifies transition from AWI to ATOM execution.

**Requirements:**
- bump.md file exists
- No template placeholders remain in bump.md

### gate_execution_to_learning
Verifies transition from ATOM execution to SAIF learning.

**Requirements:**
- ATOM decisions directory exists
- At least one decision file exists

### gate_learning_to_regeneration
Verifies transition from SAIF learning back to regeneration.

**Requirements:**
- Coherence report exists or learning extraction file exists

## Usage

```bash
# Source the verification gate library
source scripts/lib/verification-gate.sh

# Use pre-defined gates
gate_understanding_to_knowledge
gate_intention_to_execution

# Or create custom gates
verify_gate "custom-gate" "phase-a" "phase-b" \
    "[ -f 'required-file.txt' ]" \
    "command-that-must-succeed"
```

## Gate Logging

All gate transitions are logged to `.atom-trail/gate-transitions.jsonl`:

```json
{
  "gate": "intention-to-execution",
  "from": "AWI",
  "to": "ATOM",
  "timestamp": "2026-01-03T12:00:00Z",
  "passed": true,
  "failed": []
}
```

## Escalation

Failed gates trigger escalation via `scripts/hooks/on-boundary-violated.sh`:
- Logged to `.claude/logs/escalations.jsonl`
- ATOM decision created for violation
- Optionally triggers notifications

## Integration with ATOM Trail

Gate transitions are automatically logged to the ATOM trail, creating a complete audit log of all coherence transitions. This enables:

- **Observability**: See exactly where the system is in the coherence cycle
- **Debugging**: Identify where transitions fail
- **Metrics**: Measure coherence health over time
- **Compliance**: Provide audit trail for all phase transitions

## Best Practices

1. **Always use gates**: Never bypass verification gates
2. **Handle failures**: Address gate failures immediately
3. **Monitor trends**: Track gate pass/fail rates over time
4. **Add custom gates**: Create domain-specific gates as needed
5. **Document requirements**: Clearly specify what each gate checks
