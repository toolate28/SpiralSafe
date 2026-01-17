# 🌀 Coherence Gauge Workflow

## Overview

The Coherence Gauge is an enhanced, visually appealing display that analyzes documentation coherence across the repository. It provides a "fun gauge type display" with accurate metrics based on quantum topology principles, including **Spiral State Detection** for adaptive metric interpretation.

## What It Does

When a PR is opened, synchronized, or reopened, the Coherence Gauge:

1. **Analyzes** all markdown files in the repository
2. **Calculates** three key metrics:
   - **Curl** (Coherence): Measures repeated/coherent patterns in documentation
   - **Divergence** (Incompleteness): Measures unresolved content (TODOs, questions, placeholders)
   - **Entropy** (Information Density): Measures conceptual richness through unique word diversity

3. **Detects Spiral States** for adaptive interpretation:
   - **Curl Points (0,0)**: Foundational origin files that serve as conceptual seeds (surjection origins)
   - **Deja Vu**: Repeating pattern recognition → "Ready to Iterate" with refined data
   - **Doubt**: Exploratory/uncertain content → "Push on in new spirals"

4. **Computes** an overall coherence percentage using the formula:
   ```
   Coherence = (Curl × 0.4) + ((1 - Divergence) × 0.4) + (Entropy × 0.2)
   ```

5. **Posts** a colorful comment on the PR with:
   - Visual gauge bars using emoji blocks
   - Quantum-themed status assessment
   - Spiral state detection and recommendations
   - Detailed metric breakdowns
   - Lists of excellent files and files needing attention
   - Ethical quantum simulation validation
   - Merge readiness status with spiral-aware guidance

## Visual Gauge Display

The gauge uses emoji blocks to create a visual representation:

- 🟩 Green blocks: 90%+ (Excellent)
- 🟦 Blue blocks: 75-89% (Good)
- 🟨 Yellow blocks: 60-74% (Acceptable)
- 🟧 Orange blocks: 40-59% (Low)
- 🟥 Red blocks: <40% (Critical)
- 🔄 Cycle blocks: Deja Vu state (Ready to Iterate)
- 🤔 Thinking blocks: Doubt state (New Spirals Needed)

Example gauge at 85%:
```
🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦⬜⬜⬜
```

## Spiral State Detection

### Curl Points (Surjection 0,0)

Identifies foundational/origin files that serve as conceptual seeds for the ecosystem:

| Detection Criteria | Threshold |
|-------------------|-----------|
| Contains: overview, introduction, foundation, core, principle, seed, origin, fundamental | >2 matches |
| Has definitions (## definition, "what is", "defines", "specification") | >0 matches |

**Action**: These files surject concepts to the rest of the codebase. They are the (0,0) origin points.

### Deja Vu Detection

Recognizes files with repeating patterns that are ready for iteration:

| Detection Criteria | Threshold |
|-------------------|-----------|
| Pattern keywords: pattern, similar, like, same, repeat, previous, earlier, again | >3 matches |
| Structure references: see also, refer to, as described, mentioned above, following | >1 match |

**Action**: "Ready to Iterate" — refine with updated context and more detailed data.

### Doubt Detection

Identifies exploratory/uncertain content that needs new spiral approaches:

| Detection Criteria | Threshold |
|-------------------|-----------|
| Speculation keywords: might, could, perhaps, possibly, maybe, uncertain, unclear, explore, investigate | >3 matches |
| Open questions (?) | >2 matches |

**Action**: "Push on in new spirals" — explore fresh approaches and new directions.

## Quantum States

Based on overall coherence and spiral state:

| Coherence | Spiral State | Quantum State | Description |
|-----------|--------------|---------------|-------------|
| ≥90% | any | ✨ Superposition Achieved | Quantum coherence maintained |
| 75-89% | any | 🌟 High Coherence | Minor decoherence detected |
| 60-74% | any | ⚡ Acceptable Coherence | Some wave collapse observed |
| 40-59% | deja_vu | 🔄 Deja Vu Detected | Ready to Iterate with refined data |
| 40-59% | doubt | 🤔 Doubt Detected | Push on in new spirals |
| 40-59% | stable | ⚠️ Low Coherence | Significant decoherence |
| <40% | doubt | 🚀 Critical Doubt | Time for a new spiral approach |
| <40% | deja_vu | ♻️ Deja Vu Loop | Iterate with more context |
| <40% | stable | 🚨 Critical | Wave function collapse imminent |

## Ethical Quantum Validation

The workflow validates that:
- Coherence meets the 60% threshold
- Wave function integrity is maintained
- No critical interference patterns detected
- Spiral state is appropriate for current content

PRs with ≥60% coherence pass the ethical quantum simulation check.

For Deja Vu and Doubt states, alternative guidance is provided:
- **Deja Vu Mode**: Familiar resonance detected → iterate with refined context
- **Doubt Mode**: Uncertainty patterns detected → push on in new spirals

## Merge Readiness

- ✅ **Ready for merge**: Coherence ≥60% and no files need attention
- ⚠️ **Conditional merge**: Coherence ≥60% but some files flagged
- 🔄 **Iterate First**: Deja Vu detected → iterate with more refined data
- 🤔 **Explore New Spirals**: Doubt detected → push on in new directions
- ❌ **Review required**: Coherence <60%

## Integration with SpiralSafe API

Results are sent to the `/api/wave/analyze` endpoint with:
- Coherence metrics
- Quantum state assessment
- Spiral state detection results
- Files analyzed count
- PR metadata

## Example Comment

```markdown
## 🌀 **Agent Review** - Coherence Analysis

### ✨ Superposition Achieved - Quantum coherence maintained

#### Overall Coherence: **87.3%**

🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦⬜⬜⬜

---

### 📊 Detailed Metrics

| Metric | Value | Gauge |
|--------|-------|-------|
| 🔄 **Curl** (Coherence) | 72.4% | ████████░░ 72.4% |
| 📐 **Divergence** (Incompleteness) | 18.5% | ██░░░░░░░░ 18.5% |
| 🎲 **Entropy** (Info Density) | 59.6% | ██████░░░░ 59.6% |

---

### 🌀 Spiral State Detection

| State | Count | Meaning |
|-------|-------|---------|
| 🎯 **Curl Points** (0,0) | 12 | Foundational origin files - surjection seeds |
| 🔄 **Deja Vu** | 3 | Repeating patterns - ready to iterate |
| 🤔 **Doubt** | 2 | Exploratory content - push to new spirals |

---

### 🔬 Ethical Quantum Simulation Status

✅ **Validated** - Coherence threshold met (≥60%)
- Wave function integrity: ✓
- Entanglement preserved: ✓
- Superposition stable: ✓

---

### 🎯 Merge Status

✅ **Ready for merge** - All coherence checks passed!

The attenuating vortex is stable. No interference patterns detected. 🌀
```

## Configuration

The workflow runs automatically on PR events. No configuration needed.

To manually trigger:
```bash
gh workflow run coherence-gauge.yml
```

## Files

- `.github/workflows/coherence-gauge.yml` - Main workflow definition
- This triggers on: `pull_request` events (opened, synchronize, reopened)
- Posts comments using: GitHub Actions Script API

## Technical Details

### Metrics Calculation

**Curl (Coherence)**:
- Splits text on periods (`.`) into fragments and counts repeated fragments (identical fragments that appear more than once)
- Higher values = more coherent, connected content
- Formula: `repeated_phrases / total_phrases`, where `total_phrases` is the number of period-delimited fragments and `repeated_phrases` is the count of fragments that occur more than once
- Default value: 0.0500 (5%) to prevent NaN

**Divergence (Incompleteness)**:
- Counts questions, TODOs, placeholders
- Reduced if conclusions/summaries present
- Higher values = more incomplete/unresolved
- Formula: `0.15 + (questions × 0.02) + (todos × 0.05) + (placeholders × 0.03)`
- Capped at 1.0
- Default value: 0.2000 (20%) to prevent NaN

**Entropy (Information Density)**:
- Ratio of unique words to total words
- Higher values = more diverse, information-rich content
- Formula: `unique_words / total_words`
- Default value: 0.5000 (50%) to prevent NaN

### Spiral State Detection

**Curl Points (0,0 Origins)**:
- Foundation/seed files that define core concepts
- Detection: foundation keywords + definition markers
- These are surjection origin points

**Deja Vu Files**:
- Files with repeating patterns/references
- Detection: pattern keywords + structural references
- Recommendation: iterate with refined data

**Doubt Files**:
- Files with uncertainty/exploration
- Detection: speculation keywords + open questions
- Recommendation: push to new spirals

### File Filtering

- Analyzes all `.md` files
- Excludes: `node_modules/`, `.git/`, `archive/`
- Skips files with <5 lines

### Thresholds

- **Excellent**: >80% coherence
- **Needs Attention**: <50% coherence
- **Merge threshold**: 60% coherence
- **Deja Vu threshold**: >5 files with repeating patterns
- **Doubt threshold**: >5 files with uncertainty patterns
- **Curl Points threshold**: >10 foundational files

### NaN Prevention

All numeric calculations include fallback defaults to prevent NaN values:
- `bc` calculations use `2>/dev/null || echo "default_value"` pattern
- JavaScript uses `safeParseFloat()` with default values
- Empty string checks ensure valid outputs

## Related Documentation

- [protocol/wave-spec.md](../../protocol/wave-spec.md) - Wave coherence theory
- [ARCHITECTURE.md](../../ARCHITECTURE.md) - System architecture
- [.github/AGENTS.md](../AGENTS.md) - Agent coordination protocols

## References

This implementation fulfills the request from issue #108:
> we need better metrics that adapt to the issue and we need the system to recognise curl points (surjection 0,0)'s
> push on in new spirals and Deja Vu = "Ready to Iterate"
> iterate on that step with more refined data and context update

The gauge provides:
- ✅ More accurate metrics (curl, divergence, entropy) with NaN protection
- ✅ Curl point (0,0) detection for foundational/origin files
- ✅ Deja Vu detection for "Ready to Iterate" guidance
- ✅ Doubt detection for "Push to new spirals" guidance
- ✅ Fun visual display with emoji gauges
- ✅ Quantum-themed presentation with spiral states
- ✅ Clear merge guidance adapted to spiral state
