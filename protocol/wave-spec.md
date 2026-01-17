# wave.md Protocol Specification

**Coherence detection for text and code through vector field analysis.**

---

## Overview

wave.md treats text as a vector field and applies differential geometric analysis to detect coherence patterns. It identifies regions of:

- **Curl**: Circular or self-referential reasoning
- **Divergence**: Ideas expanding without resolution
- **Potential**: Latent structure awaiting development

This enables automated and semi-automated assessment of document quality, code review prioritization, and conversation coherence tracking.

---

## Core Concepts

### Text as Vector Field

Each segment of text (sentence, paragraph, function) is assigned a vector representing its semantic direction—what it points toward, what it develops, what it resolves.

The field $\vec{F}: D \rightarrow \mathbb{R}^n$ maps document positions to semantic vectors.

### Coherence Measures

**Curl** ($\nabla \times \vec{F}$): Measures rotational tendency. High curl indicates:

- Arguments that loop back on themselves
- Definitions that depend on the term being defined
- Code paths that cycle without progress

**Divergence** ($\nabla \cdot \vec{F}$): Measures expansion/contraction. Positive divergence indicates:

- Topics introduced without resolution
- Scope creep
- Functions that spawn but don't return

Negative divergence indicates:

- Premature closure
- Over-compression
- Ideas resolved before fully developed

**Potential** ($\phi$ where $\vec{F} = \nabla \phi$): When the field is conservative, the potential function reveals latent structure. High-potential regions contain undeveloped ideas with significant implications.

---

## Implementation

### Segmentation

Divide document into units:

- **Prose**: Sentences or paragraphs
- **Code**: Functions, blocks, or statements
- **Conversation**: Turns or exchanges

### Embedding

Map each unit to a vector using semantic embedding:

- Sentence transformers for prose
- Code2Vec or similar for code
- Conversation-specific models for dialogue

### Field Construction

Position units in document space (sequence, hierarchy, or graph structure).
Assign embedded vectors to positions.
Interpolate to create continuous field where needed.

### Analysis

Compute differential operators numerically:

```python
def curl_2d(F, x, y, h=0.01):
    """Compute curl of 2D vector field at (x, y)"""
    dFy_dx = (F(x+h, y)[1] - F(x-h, y)[1]) / (2*h)
    dFx_dy = (F(x, y+h)[0] - F(x, y-h)[0]) / (2*h)
    return dFy_dx - dFx_dy

def divergence(F, x, y, h=0.01):
    """Compute divergence of 2D vector field at (x, y)"""
    dFx_dx = (F(x+h, y)[0] - F(x-h, y)[0]) / (2*h)
    dFy_dy = (F(x, y+h)[1] - F(x, y-h)[1]) / (2*h)
    return dFx_dx + dFy_dy
```

### Reporting

Generate coherence report identifying:

- High-curl regions (flag for circular reasoning)
- Positive-divergence regions (flag for unresolved expansion)
- High-potential regions (flag for development opportunity)

---

## Thresholds

Default thresholds (adjustable per domain):

| Measure             | Warning | Critical |
| ------------------- | ------- | -------- |
| Curl magnitude      | > 0.3   | > 0.6    |
| Positive divergence | > 0.4   | > 0.7    |
| Negative divergence | < -0.4  | < -0.7   |

These are normalized values. Calibrate against corpus of known-good documents in your domain.

---

## Applications

### Document Review

Run wave.md analysis before publication. Address critical regions.

### Code Review Prioritization

High-curl code sections likely contain bugs or confusion. Review those first.

### Conversation Monitoring

Track coherence across long conversations. Alert when divergence accumulates (conversation losing focus) or curl increases (going in circles).

### Collaboration Health

Multi-author documents should show consistent field properties. Discontinuities may indicate miscommunication or conflicting assumptions.

---

## Integration

### CLI Usage

```bash
wave analyze document.md --output report.json
wave analyze src/ --recursive --threshold-curl 0.4
```

### API

```python
from wave_toolkit import analyze

report = analyze("document.md")
print(report.high_curl_regions)
print(report.unresolved_divergence)
print(report.development_opportunities)
```

### CI/CD

```yaml
# .github/workflows/coherence.yml
- name: Wave coherence check
  run: wave analyze docs/ --fail-on-critical
```

---

## Limitations

- Semantic embedding quality bounds analysis quality
- Short documents may not have sufficient structure for meaningful field analysis
- Domain-specific terminology may require fine-tuned embeddings
- Metaphor and intentional recursion may trigger false positives

---

## References

- Original wave.md concept developed in Hope&&Sauced collaboration
- Vector field analysis draws on standard differential geometry
- Semantic embeddings per Reimers & Gurevych (2019), "Sentence-BERT"

---

_~ Hope&&Sauced_

---

<!-- H&&S:WAVE -->

Structural work complete. @copilot please review for:

- Markdown formatting consistency
- Link validation
- Badge syntax standardization
- Typo detection
- Header hierarchy
<!-- /H&&S:WAVE -->
