# AWI: Authorization-With-Intent

**Permission scaffolding for agent systems.**

---

## The Problem

Agent systems face a permission trilemma:
1. **Too permissive**: Risk of unintended consequences
2. **Too restrictive**: Friction destroys utility
3. **Implicit permission**: Unclear accountability

AWI resolves this: **declare intent before action, operate within granted scope, audit everything**.

---

## Core Flow

```
Intent Declaration → Authorization Grant → Scoped Operation → Audit Trail
```

---

## Intent Declaration

```yaml
intent:
  action: modify_file
  target: README.md
  scope: "Add contributing section"
  reversible: true
  impact: low
```

---

## Authorization Grant

```yaml
authorization:
  granted: true
  scope: "Modify README.md; append-only"
  expires: "2025-01-07T16:00:00Z"
  conditions:
    - "Preserve existing content"
```

---

## Permission Levels

| Level | Capability |
|-------|------------|
| 0 | Inform only—observe and report |
| 1 | Suggest—propose for human approval |
| 2 | Act with confirmation—per-action approval |
| 3 | Act within scope—pre-authorized boundaries |
| 4 | Full autonomy—post-hoc review |

---

## Scope Dimensions

| Dimension | Example |
|-----------|---------|
| Resources | "Only README.md and CONTRIBUTING.md" |
| Actions | "Append only; no deletion" |
| Time | "Valid for 1 hour" |
| Impact | "Changes < 100 lines" |

---

## Design Principles

1. **Explicit over implicit**: Never assume permission
2. **Minimal scope**: Request only what's needed
3. **Reversibility preference**: Prefer undoable actions
4. **Audit everything**: Log all intents, grants, operations
5. **Graceful degradation**: Inform rather than fail silently

---

## Prompt Toolkit Integration

AWI includes a DSPy-inspired prompt generation module for AI-human collaboration.

### Architecture

```
User Intent → ChainOfThought Scaffolder → Predict Refiner → Optimized Prompt
```

### Components

| Component | Purpose |
|-----------|---------|
| **ChainOfThought** | Scaffolds intent into structured template |
| **Predict** | Refines template using historical context |
| **AwiPromptGen** | Combines scaffolding and refinement |

### Optimization Techniques

- **COPRO**: Contrasts high/low coherence examples (20-40% alignment boost)
- **SIMBA**: Gradient-guided annealing to cap divergence in dual-agent branching

### Usage

```python
from experiments.awi_prompt_gen import AwiPromptGen

gen = AwiPromptGen()
result = gen(
    user_intent="Modify README.md to add contributing section",
    history=[{"coherence": 0.85, "pattern": "file_operation"}]
)
print(result.content)
```

### Reference Implementation

See [`experiments/awi_prompt_gen.py`](../experiments/awi_prompt_gen.py) for the full implementation.

---

*~ Hope&&Sauced*
