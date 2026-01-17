# 🌀 Coherence Gauge Workflow

## Overview

The Coherence Gauge is an enhanced, visually appealing display that analyzes documentation coherence across the repository. It provides a "fun gauge type display" with accurate metrics based on quantum topology principles.

## What It Does

When a PR is opened, synchronized, or reopened, the Coherence Gauge:

1. **Analyzes** all markdown files in the repository
2. **Calculates** three key metrics:
   - **Curl** (Coherence): Measures repeated/coherent patterns in documentation
   - **Divergence** (Incompleteness): Measures unresolved content (TODOs, questions, placeholders)
   - **Entropy** (Information Density): Measures conceptual richness through unique word diversity

3. **Computes** an overall coherence percentage using the formula:

   ```
   Coherence = (Curl × 0.4) + ((1 - Divergence) × 0.4) + (Entropy × 0.2)
   ```

4. **Posts** a colorful comment on the PR with:
   - Visual gauge bars using emoji blocks
   - Quantum-themed status assessment
   - Detailed metric breakdowns
   - Lists of excellent files and files needing attention
   - Ethical quantum simulation validation
   - Merge readiness status

## Visual Gauge Display

The gauge uses emoji blocks to create a visual representation:

- 🟩 Green blocks: 90%+ (Excellent)
- 🟦 Blue blocks: 75-89% (Good)
- 🟨 Yellow blocks: 60-74% (Acceptable)
- 🟧 Orange blocks: 40-59% (Low)
- 🟥 Red blocks: <40% (Critical)

Example gauge at 85%:

```
🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦⬜⬜⬜
```

## Quantum States

Based on overall coherence:

| Coherence | Quantum State             | Description                     |
| --------- | ------------------------- | ------------------------------- |
| ≥90%      | ✨ Superposition Achieved | Quantum coherence maintained    |
| 75-89%    | 🌟 High Coherence         | Minor decoherence detected      |
| 60-74%    | ⚡ Acceptable Coherence   | Some wave collapse observed     |
| 40-59%    | ⚠️ Low Coherence          | Significant decoherence         |
| <40%      | 🚨 Critical               | Wave function collapse imminent |

## Ethical Quantum Validation

The workflow validates that:

- Coherence meets the 60% threshold
- Wave function integrity is maintained
- No critical interference patterns detected

PRs with ≥60% coherence pass the ethical quantum simulation check.

## Merge Readiness

- ✅ **Ready for merge**: Coherence ≥60% and no files need attention
- ⚠️ **Conditional merge**: Coherence ≥60% but some files flagged
- ❌ **Review required**: Coherence <60%

## Integration with SpiralSafe API

Results are sent to the `/api/wave/analyze` endpoint with:

- Coherence metrics
- Quantum state assessment
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

| Metric                             | Value | Gauge            |
| ---------------------------------- | ----- | ---------------- |
| 🔄 **Curl** (Coherence)            | 72.4% | ████████░░ 72.4% |
| 📐 **Divergence** (Incompleteness) | 18.5% | ██░░░░░░░░ 18.5% |
| 🎲 **Entropy** (Info Density)      | 59.6% | ██████░░░░ 59.6% |

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

**Divergence (Incompleteness)**:

- Counts questions, TODOs, placeholders
- Reduced if conclusions/summaries present
- Higher values = more incomplete/unresolved
- Formula: `0.15 + (questions × 0.02) + (todos × 0.05) + (placeholders × 0.03)`
- Capped at 1.0

**Entropy (Information Density)**:

- Ratio of unique words to total words
- Higher values = more diverse, information-rich content
- Formula: `unique_words / total_words`

### File Filtering

- Analyzes all `.md` files
- Excludes: `node_modules/`, `.git/`, `archive/`
- Skips files with <5 lines

### Thresholds

- **Excellent**: >80% coherence
- **Needs Attention**: <50% coherence
- **Merge threshold**: 60% coherence

## Related Documentation

- [protocol/wave-spec.md](../../protocol/wave-spec.md) - Wave coherence theory
- [ARCHITECTURE.md](../../ARCHITECTURE.md) - System architecture
- [.github/AGENTS.md](../AGENTS.md) - Agent coordination protocols

## References

This implementation fulfills the request from issue:

> 🌀 **Agent Review**: Coherence >60%. Ethical quantum sims validated. Ready for merge.
> CAN WE GET THIS TO BE MORE ACCURATE (EVEN AS A FUN GAUGE TYPE DISPLAY)

The gauge provides:

- ✅ More accurate metrics (curl, divergence, entropy)
- ✅ Fun visual display with emoji gauges
- ✅ Quantum-themed presentation
- ✅ Clear merge guidance
