# .context.yaml Specification

**Structured knowledge units for agent consumption.**

---

## Overview

`.context.yaml` files provide machine-readable knowledge that agents can query and reason about. They complement prose documentation by offering the same insights in addressable, composable form.

---

## Schema

```yaml
meta:
  domain: string           # Knowledge domain
  source: string           # Attribution
  version: string          # Semantic version
  confidence: high|medium|low|experimental

concepts:
  - name: string
    definition: string
    relationships:
      - type: is_a|part_of|enables|requires|contrasts
        target: string
    examples: []
    counterexamples: []

signals:
  use_when: []             # Conditions favoring this knowledge
  avoid_when: []           # Conditions where this doesn't apply

invariants: []             # Conditions that must always hold
```

---

## Example

```yaml
# isomorphism-principle.context.yaml
meta:
  domain: foundations
  source: Hope&&Sauced
  version: 1.0.0
  confidence: high

concepts:
  - name: isomorphism-principle
    definition: >
      Discrete systems instantiate the same topological structures
      as continuous mathematics. The boundary is projection artifact.
    relationships:
      - type: enables
        target: discrete-continuous-equivalence
      - type: contrasts
        target: approximation-model
    examples:
      - "Shannon sampling theorem"
      - "Lewis-Kempf-Menicucci lattice QFT"
      - "Redstone topology preservation"

signals:
  use_when:
    - designing_discrete_implementations
    - teaching_continuous_mathematics
  avoid_when:
    - continuous_structure_genuinely_required

invariants:
  - "Topological invariants preserved across substrate"
```

---

## Usage

```python
from spiralsafe import context

ctx = context.load("isomorphism-principle.context.yaml")
if ctx.should_use(current_conditions):
    apply_knowledge(ctx)
```

---

*~ Hope&&Sauced*
