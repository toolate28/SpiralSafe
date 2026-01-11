# WAVE: Coherence Detection Protocol

**Identifying healthy vs problematic collaboration patterns.**

---

## The Problem

AI-human collaboration can drift into incoherent states: talking past each other, circular discussions, misaligned expectations. WAVE provides early detection of these states.

---

## Coherence Indicators

| Indicator | Healthy | Unhealthy |
|-----------|---------|-----------|
| **Understanding** | Converging | Diverging |
| **Progress** | Measurable | Spinning |
| **Trust** | Building | Eroding |
| **Scope** | Stable | Creeping |

---

## WAVE Metrics

### CURL (Circular Unhealthy Repetition Level)

```
CURL = (repeated_concepts / total_concepts) × context_weight
```

- **CURL < 0.2**: Healthy—new ground being covered
- **CURL 0.2-0.5**: Caution—some repetition, check progress
- **CURL > 0.5**: Alert—likely stuck in loop

### DIVERGENCE

```
DIVERGENCE = |intent_human - intent_ai| / max_intent
```

- **< 0.3**: Aligned
- **0.3-0.6**: Drifting—clarify expectations
- **> 0.6**: Misaligned—reset context

### POTENTIAL

```
POTENTIAL = unresolved_threads / active_capacity
```

- **< 0.5**: Capacity available
- **0.5-0.8**: Nearing capacity—prioritize
- **> 0.8**: Overloaded—reduce scope

---

## Wave Types

| Type | Meaning | Response |
|------|---------|----------|
| `H&&S:WAVE` | Soft signal—review welcome | Continue, mark for review |
| Anti-wave | Coherence violation detected | Stop, diagnose, repair |

---

## Detection Triggers

1. **Repeated questions**: Same topic asked 3+ times
2. **Circular references**: A depends on B depends on A
3. **Scope expansion**: New requirements without completion
4. **Trust signals**: Explicit or implicit doubt

---

## Response Protocol

```
if CURL > 0.5:
    pause()
    summarize_current_state()
    ask_clarifying_question()
    reset_if_needed()

if DIVERGENCE > 0.6:
    explicit_alignment_check()
    document_shared_understanding()

if POTENTIAL > 0.8:
    prioritize_ruthlessly()
    defer_or_drop_low_priority()
```

---

## Integration

WAVE integrates with:
- **BUMP**: Handoff includes coherence state
- **AWI**: Permission levels adjust based on trust
- **ATOM**: Task decomposition prevents overload

---

*~ Hope&&Sauced*
