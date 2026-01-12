name: Pull request template
about: Use this template for PRs that add CI, bump templates, or agent-facing files
title: ''
labels: ''
assignees: ''

---

## Summary

Describe the change in 1-2 sentences.

## ATOM Tag

**ATOM:** `ATOM-TYPE-YYYYMMDD-NNN-description`

_(Generate with: `./scripts/atom-track.sh TYPE "description" "file"`)_

## Why

Why this change is needed and what it enables.

## What changed

- Files added
- Scripts
- CI workflows

## Verification / Testing

- [ ] `scripts/validate-bump.sh` passes locally (if bump.md changed)
- [ ] `scripts/validate-branch-name.sh` tested on example branches (if applicable)
- [ ] `bash scripts/verify-environment.sh` prints `ENV OK`
- [ ] `scripts/test-scripts.sh` passes (if scripts changed)
- [ ] All shell scripts pass shellcheck
- [ ] ATOM tag created and logged

## Claude Interaction

You can interact with Claude in this PR by:
- **@mentioning Claude** in comments for questions or reviews
- **Adding labels**: `claude:review`, `claude:help`, `claude:analyze`
- **Requesting reviews**: Claude will provide automated feedback
- **Ask questions**: Claude can explain code, suggest improvements, or identify issues

### Example commands:
- `@claude please review this PR for ATOM compliance`
- `@claude explain the changes in scripts/atom-track.sh`
- `@claude check for security issues`
- `@claude suggest improvements`

## Notes
