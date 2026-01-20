# GitHub Labels Reference

**ATOM:** ATOM-DOC-20260120-002-github-labels-documentation  
**Status:** Complete  
**Date:** 2026-01-20

---

## Overview

This document catalogs all GitHub labels used in the SpiralSafe repository. Labels are organized by category and integrated with the SYNAPSE framework and SPHINX data integrity testing.

## Setup

To initialize all required labels in your repository:

```bash
./scripts/setup-github-labels.sh
```

For a dry run (preview without changes):

```bash
./scripts/setup-github-labels.sh --dry-run
```

---

## Label Categories

### 1. Dependabot Labels

These labels are automatically applied by Dependabot to dependency update PRs (configured in `.github/dependabot.yml`):

| Label | Color | Description | Usage |
|-------|-------|-------------|-------|
| `dependencies` | ![#0366d6](https://via.placeholder.com/15/0366d6/000000?text=+) `#0366d6` | Dependency updates from Dependabot | All Dependabot PRs |
| `automated` | ![#1d76db](https://via.placeholder.com/15/1d76db/000000?text=+) `#1d76db` | Automated processes and workflows | Automated PRs and issues |
| `cascade-stage-1` | ![#7057ff](https://via.placeholder.com/15/7057ff/000000?text=+) `#7057ff` | Vortex Cascade Collapse Stage 1 | First stage of coherence cascade |
| `github-actions` | ![#000000](https://via.placeholder.com/15/000000/000000?text=+) `#000000` | GitHub Actions workflow updates | Action dependency updates |
| `ops` | ![#d4c5f9](https://via.placeholder.com/15/d4c5f9/000000?text=+) `#d4c5f9` | Operations and infrastructure | Ops workspace dependencies |
| `python` | ![#3572A5](https://via.placeholder.com/15/3572A5/000000?text=+) `#3572A5` | Python dependency updates | Python package updates |

**SPHINX Gate Check:** Before accepting a Dependabot PR, verify:
- `SPHINX:ORIGIN` - Dependency comes from trusted source
- `SPHINX:INTENT` - Update has clear security/feature benefit
- `SPHINX:COHERENCE` - No breaking changes to API contracts
- `SPHINX:IDENTITY` - Package signature and checksums verified
- `SPHINX:PASSAGE` - Tests pass and coherence maintained

### 2. Issue Template Labels

Applied automatically by issue templates (`.github/ISSUE_TEMPLATE/*.md`):

| Label | Color | Description | Template |
|-------|-------|-------------|----------|
| `bug` | ![#d73a4a](https://via.placeholder.com/15/d73a4a/000000?text=+) `#d73a4a` | Something isn't working | bug_report.md |
| `enhancement` | ![#a2eeef](https://via.placeholder.com/15/a2eeef/000000?text=+) `#a2eeef` | New feature or request | feature_request.md |
| `documentation` | ![#0075ca](https://via.placeholder.com/15/0075ca/000000?text=+) `#0075ca` | Improvements or additions to documentation | documentation.md |
| `task` | ![#fbca04](https://via.placeholder.com/15/fbca04/000000?text=+) `#fbca04` | Task or chore that needs to be done | task.md |
| `needs-atom-tag` | ![#ededed](https://via.placeholder.com/15/ededed/000000?text=+) `#ededed` | Requires ATOM tag assignment | All templates (auto-removed) |
| `atom-tagged` | ![#c2e0c6](https://via.placeholder.com/15/c2e0c6/000000?text=+) `#c2e0c6` | Has been assigned an ATOM tag | Added by auto-atom-tags.yml |

**ATOM Trail Integration:** Issues with these labels automatically receive ATOM tags via `.github/workflows/auto-atom-tags.yml`.

### 3. SYNAPSE Framework Labels

Used to categorize work related to the SYNAPSE visualization framework:

| Label | Color | Description | Use Case |
|-------|-------|-------------|----------|
| `synapse` | ![#9C27B0](https://via.placeholder.com/15/9C27B0/000000?text=+) `#9C27B0` | SYNAPSE visualization framework | SYNAPSE component work |
| `sphinx-gate` | ![#673AB7](https://via.placeholder.com/15/673AB7/000000?text=+) `#673AB7` | SPHINX protocol gate verification | Gate implementation/testing |
| `wave-protocol` | ![#3F51B5](https://via.placeholder.com/15/3F51B5/000000?text=+) `#3F51B5` | WAVE coherence protocol | Coherence analysis work |
| `bump-protocol` | ![#2196F3](https://via.placeholder.com/15/2196F3/000000?text=+) `#2196F3` | BUMP handoff protocol | Handoff marker work |
| `atom-protocol` | ![#00BCD4](https://via.placeholder.com/15/00BCD4/000000?text=+) `#00BCD4` | ATOM tagging protocol | ATOM implementation work |

**SYNAPSE Testing:** These labels help categorize issues for framework testing:
- Issues labeled `sphinx-gate` must pass all five SPHINX riddles
- Issues labeled `wave-protocol` must maintain >60% coherence threshold
- Issues labeled `bump-protocol` must use correct H&&S markers

### 4. Quality and Coherence Labels

Track code quality, testing, and security:

| Label | Color | Description | Usage |
|-------|-------|-------------|-------|
| `coherence` | ![#00E676](https://via.placeholder.com/15/00E676/000000?text=+) `#00E676` | Coherence metrics and quality | Coherence-related work |
| `testing` | ![#795548](https://via.placeholder.com/15/795548/000000?text=+) `#795548` | Testing and quality assurance | Test additions/fixes |
| `security` | ![#B71C1C](https://via.placeholder.com/15/B71C1C/000000?text=+) `#B71C1C` | Security vulnerabilities and fixes | Security issues |

**42.00055 Framework:** Issues labeled `coherence` are tracked for impact on the 42.00055% quality threshold.

### 5. Workflow State Labels

Track issue and PR progress:

| Label | Color | Description | State |
|-------|-------|-------------|-------|
| `in-progress` | ![#FFC107](https://via.placeholder.com/15/FFC107/000000?text=+) `#FFC107` | Work in progress | Active development |
| `review-needed` | ![#FF9800](https://via.placeholder.com/15/FF9800/000000?text=+) `#FF9800` | Needs review | Awaiting review |
| `blocked` | ![#E91E63](https://via.placeholder.com/15/E91E63/000000?text=+) `#E91E63` | Blocked by external dependency | Blocked state |

### 6. Agent Coordination Labels

Facilitate multi-agent collaboration (see `.github/AGENTS.md`):

| Label | Color | Description | Agent |
|-------|-------|-------------|-------|
| `claude:help` | ![#512DA8](https://via.placeholder.com/15/512DA8/000000?text=+) `#512DA8` | Claude AI assistance requested | Claude |
| `copilot:review` | ![#1976D2](https://via.placeholder.com/15/1976D2/000000?text=+) `#1976D2` | GitHub Copilot review requested | Copilot |

### 7. Hope&&Sauced (H&&S) Protocol Labels

Mark handoff and synchronization points:

| Label | Color | Description | H&&S Marker |
|-------|-------|-------------|-------------|
| `H&&S:WAVE` | ![#00ACC1](https://via.placeholder.com/15/00ACC1/000000?text=+) `#00ACC1` | Hope&&Sauced soft handoff | Soft handoff for review |
| `H&&S:PASS` | ![#00897B](https://via.placeholder.com/15/00897B/000000?text=+) `#00897B` | Hope&&Sauced ownership transfer | Ownership transfer |
| `H&&S:SYNC` | ![#0097A7](https://via.placeholder.com/15/0097A7/000000?text=+) `#0097A7` | Hope&&Sauced synchronization | Synchronization point |
| `H&&S:BLOCK` | ![#D32F2F](https://via.placeholder.com/15/D32F2F/000000?text=+) `#D32F2F` | Hope&&Sauced blocking issue | Blocking issue |

See `protocol/bump-spec.md` for detailed H&&S marker usage.

---

## SPHINX Data Integrity Testing

Labels are used in automated SPHINX gate verification:

### Test Matrix

| Label Combination | SPHINX Gates Tested | Expected Outcome |
|-------------------|---------------------|------------------|
| `dependencies` + `automated` | ORIGIN, IDENTITY | Verify Dependabot signature |
| `sphinx-gate` | ALL | Verify all five gates |
| `security` | INTENT, COHERENCE | Verify no vulnerabilities introduced |
| `H&&S:WAVE` | ORIGIN, INTENT, PASSAGE | Verify handoff protocol |

### Negative Space Testing

The setup script ensures **corpus-wide consistency** by:

1. **Exhaustive enumeration:** All labels defined in one place
2. **Automated verification:** Script can run in CI to detect drift
3. **Edge case coverage:** Special characters in H&&S labels (`:` delimiter)
4. **Color consistency:** Protocol labels use complementary colors

### Common Errors Prevented

The script prevents these common Dependabot configuration errors:

| Error | Prevention |
|-------|------------|
| Label name typos | Centralized definitions |
| Missing labels | Comprehensive list |
| Case sensitivity issues | Exact name matching |
| Color inconsistencies | Standardized color scheme |
| Description drift | Single source of truth |

---

## Usage Examples

### For Repository Maintainers

```bash
# Initial setup
./scripts/setup-github-labels.sh

# Verify all labels exist (dry-run mode)
./scripts/setup-github-labels.sh --dry-run

# Update label descriptions/colors
# (Edit script then re-run)
./scripts/setup-github-labels.sh
```

### For Dependabot PRs

When a Dependabot PR arrives:

1. Verify it has the correct labels (`dependencies`, ecosystem label)
2. Run SPHINX gate checks (manual or automated)
3. Check coherence impact with WAVE analysis
4. Merge if all gates pass

### For Issue Triage

```bash
# Add multiple labels
gh issue edit <number> --add-label "bug,needs-atom-tag"

# Check if ATOM tag was applied
gh issue view <number> --json labels
```

### For PR Reviews

Add coordination labels based on who should review:

```bash
# Request Claude review
gh pr edit <number> --add-label "claude:help"

# Request Copilot review
gh pr edit <number> --add-label "copilot:review"

# Mark as H&&S soft handoff
gh pr edit <number> --add-label "H&&S:WAVE"
```

---

## Maintenance

### Adding New Labels

1. Edit `scripts/setup-github-labels.sh`
2. Add new label to `LABELS` array
3. Document in this file
4. Run script to apply changes
5. Update `.github/dependabot.yml` if needed
6. Commit with ATOM tag

Example:

```bash
# In LABELS array:
"new-label|FF5722|Description of new label"
```

### Removing Labels

1. Remove from script
2. Remove from documentation
3. Remove from `.github/dependabot.yml` if present
4. Manually delete from GitHub (script won't delete)

### Bulk Label Operations

```bash
# List all labels
gh label list

# Delete a label (use with caution)
gh label delete "old-label"

# Clone labels to another repo
gh label clone source-repo/name target-repo/name
```

---

## Integration with CI/CD

### Automated Label Verification

The script can run in CI to ensure labels exist:

```yaml
# .github/workflows/verify-labels.yml
name: Verify Labels Exist
on:
  pull_request:
    paths:
      - '.github/dependabot.yml'
      - 'scripts/setup-github-labels.sh'

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Verify labels
        env:
          GH_TOKEN: ${{ github.token }}
        run: ./scripts/setup-github-labels.sh --dry-run
```

### SPHINX Gate Automation

Labels trigger SPHINX gate verification in PRs:

```yaml
# In PR workflow
- name: SPHINX Gate Check
  if: contains(github.event.pull_request.labels.*.name, 'sphinx-gate')
  run: ./ops/scripts/sphinx-verify.sh
```

---

## References

- **Protocol Specs:** `protocol/bump-spec.md`, `protocol/wave-spec.md`, `protocol/sphinx-spec.md`
- **Agent Coordination:** `.github/AGENTS.md`
- **Dependabot Config:** `.github/dependabot.yml`
- **Issue Templates:** `.github/ISSUE_TEMPLATE/`
- **SYNAPSE Docs:** `synapse/README.md`, `SYNAPSE_IMPLEMENTATION_SUMMARY.md`

---

## ATOM Trail

**Tags Generated:**
- `ATOM-TASK-20260120-001-setup-github-labels` (script creation)
- `ATOM-DOC-20260120-002-github-labels-documentation` (this document)

**H&&S Markers:**
- `H&&S:WAVE` — Documentation and script ready for review
- `H&&S:GH-COPILOT` — GitHub Copilot implementation signature

---

**SPHINX:PASSAGE** — Label system complete and documented. 🌀
