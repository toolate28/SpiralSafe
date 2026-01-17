# Sorting Hat Protocol Specification

**Quantum Archetypal Classification for Repos, Agents, Users, and Systems**

---

## Overview

The Sorting Hat is a deterministic classifier that maps targets to one of four archetypal "houses" using:

1. **Feature extraction** from target metadata
2. **Axis projection** to a 2D space
3. **Quantum encoding** via rotation angles
4. **Circuit execution** yielding house assignment

The design ensures auditability, reproducibility, and integration with downstream systems (Minecraft, ClaudeNPC, ATOM trail).

---

## Version

Current: **v0.2**

Location: `scripts/sorting_hat.py`

---

## Houses

Four houses corresponding to 2-bit measurement outcomes:

| Key     | Bits | Name          | Symbol | Archetype                           |
| ------- | ---- | ------------- | ------ | ----------------------------------- |
| rubin   | 00   | House Rubin   | 🔭     | Data-driven, observatory, rigorous  |
| shannon | 01   | House Shannon | 📡     | Structure, protocols, communication |
| noether | 10   | House Noether | 🔮     | Invariants, symmetry, deep theory   |
| firefly | 11   | House Firefly | 🌟     | Play, exploration, pedagogy         |

### House Strengths

**Rubin**: Infrastructure, verification, safety tooling, observability

**Shannon**: APIs, specs, codecs, glue code, interface agents

**Noether**: Architecture, libraries, constraint systems, mathematics

**Firefly**: Museum builds, stories, interactive agents, education

---

## Target Types

| Kind   | Description        | Feature Sources                     |
| ------ | ------------------ | ----------------------------------- |
| repo   | Git repository     | Commit history, structure, docs     |
| agent  | AI agent           | Behavior patterns, style, responses |
| user   | Human collaborator | Interaction history, preferences    |
| system | Local filesystem   | Directory structure, file types     |

---

## Feature Vector

Eight normalized features (0.0 to 1.0):

### Repo/System Features

| Feature               | Meaning                                        |
| --------------------- | ---------------------------------------------- |
| doc_code_coherence    | How well documentation matches code            |
| ci_health             | Reliability of CI, test coverage               |
| change_entropy        | Burstiness of changes                          |
| contributor_diversity | Number of contributors (low = high bus factor) |

### Agent/User Features

| Feature       | Meaning                                   |
| ------------- | ----------------------------------------- |
| risk_appetite | Willingness to explore, take bold actions |
| style_entropy | Stylistic variation in outputs            |
| latency       | Speed vs. deliberateness                  |
| coherence     | Internal consistency of outputs           |

---

## Axis Mapping

Features project to two compact axes:

### Rigor ↔ Play Axis

```python
rigor_play = (
    0.3 * doc_code_coherence +
    0.3 * ci_health +
    0.2 * latency +
    0.1 * coherence +
    0.1 * (1 - risk_appetite)
)
```

### Structure ↔ Chaos Axis

```python
structure_chaos = (
    0.3 * (1 - change_entropy) +
    0.3 * (1 - style_entropy) +
    0.2 * coherence +
    0.2 * (1 - contributor_diversity)
)
```

---

## Angle Encoding

Axes map to rotation angles:

```python
theta0 = pi * rigor_play      # Qubit 0 rotation
theta1 = pi * structure_chaos  # Qubit 1 rotation
```

---

## Circuit Structure

See `protocol/quantum-circuits-spec.md` for full QASm specification.

```qasm
RESET 0
RESET 1
RY 0 <theta0>
RY 1 <theta1>
CNOT 0 1
MEASURE 0
MEASURE 1
```

---

## Classification Logic

### Probability Distribution

The quantum state yields probabilities for each house:

```python
P(rubin)   = cos²(θ₀/2) × cos²(θ₁/2)  # 00
P(shannon) = cos²(θ₀/2) × sin²(θ₁/2)  # 01
P(noether) = sin²(θ₀/2) × sin²(θ₁/2)  # 10
P(firefly) = sin²(θ₀/2) × cos²(θ₁/2)  # 11
```

### Deterministic Assignment

The house with highest probability is assigned:

```python
house = max(probabilities, key=probabilities.get)
```

For simulation: use probability weights
For hardware: use actual measurement outcome

---

## Local Filesystem Heuristics

When `--path` is provided, real filesystem analysis:

| Signal          | Detection                      | Feature Impact         |
| --------------- | ------------------------------ | ---------------------- |
| README exists   | `README.md` or `README.rst`    | +doc_code_coherence    |
| Docs folder     | `docs/` or `doc/`              | +doc_code_coherence    |
| CI config       | `.github/` or `.gitlab-ci.yml` | +ci_health             |
| Tests exist     | `tests/` or `test/`            | +ci_health             |
| CONTRIBUTING.md | File exists                    | +contributor_diversity |

---

## Output Formats

### Terminal (Static)

```
╔════════════════════════════════════════════════════════════╗
║                     SORTING HAT RESULT                     ║
╠════════════════════════════════════════════════════════════╣
║ 🔭 House Rubin                                             ║
║   Data-driven, observatory, rigorous, measurement-heavy.   ║
╚════════════════════════════════════════════════════════════╝
```

### JSON (API Integration)

```json
{
  "version": "0.2.0",
  "target": {"kind": "repo", "name": "SpiralSafe"},
  "features": {...},
  "axes": {"rigor_play": 0.5, "structure_chaos": 0.3},
  "angles": {"theta0": 1.57, "theta1": 0.94},
  "house": {
    "key": "rubin",
    "id_bits": "00",
    "name": "House Rubin",
    "probabilities": {"rubin": 0.65, "shannon": 0.20, ...}
  }
}
```

---

## CLI Usage

```bash
# Classify a repository by name
python -m scripts.sorting_hat sort-house --kind repo --name SpiralSafe

# Classify local filesystem
python -m scripts.sorting_hat sort-house --kind system --path /path/to/project

# JSON output for API integration
python -m scripts.sorting_hat sort-house --kind agent --name claude-npc --json

# Static output (no animation)
python -m scripts.sorting_hat sort-house --kind user --name iamto --static
```

---

## Integration Points

### Minecraft Plugin

Parse QASm output, execute on Vera-Rubin circuit board, trigger house reveal.

### ClaudeNPC

Narrate house assignment with personality-appropriate flair.

### ATOM System

Log house assignments as coherence trail events.

### Wave Toolkit

Use house probabilities as coherence signals.

---

## Extensibility

### Custom Feature Extractors

```python
def my_extractor(target: str, kind: str) -> FeatureVector:
    # Custom logic
    return FeatureVector(...)

register_extractor("my_source", my_extractor)
```

### Custom Axis Mappings

```python
def my_axes(features: FeatureVector) -> CompactAxes:
    # Custom projection
    return CompactAxes(...)
```

---

## Verification

### Determinism Check

Same inputs must produce same outputs:

```bash
for i in {1..10}; do
  python -m scripts.sorting_hat sort-house --kind repo --name Test --json
done | uniq | wc -l
# Should output: 1
```

### Probability Normalization

All house probabilities must sum to 1.0.

---

## References

- Quantum Circuits Spec: `protocol/quantum-circuits-spec.md`
- Wave Protocol: `protocol/wave-spec.md`
- Implementation: `scripts/sorting_hat.py`

---

_~ Hope&&Sauced_

<!-- H&&S:WAVE -->

Sorting Hat protocol specification complete.
Compliant with SpiralSafe QASm v0.2.

<!-- /H&&S:WAVE -->
