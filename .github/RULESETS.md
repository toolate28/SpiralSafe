# GitHub Repository Rulesets Configuration Guide
# 
# This file documents the recommended custom rulesets for the SpiralSafe repository.
# These rulesets enforce the Five Core Principles and ensure code quality.
#
# To apply these rulesets:
# 1. Go to: Settings → Rules → Rulesets
# 2. Click "New ruleset" → "New branch ruleset"
# 3. Configure each ruleset as documented below

## Ruleset 1: Main Branch Protection (Production)
# 
# Name: Main Branch Protection
# Enforcement: Active
# Target branches: main
# 
### Rules:
# - Restrict deletions: YES
# - Require linear history: YES
# - Require signed commits: RECOMMENDED
# - Require a pull request before merging: YES
#   - Required approvals: 1
#   - Dismiss stale reviews: YES
#   - Require review from Code Owners: YES
#   - Require approval of most recent push: YES
# - Require status checks to pass: YES
#   - Status checks required:
#     * CI - Code Quality and Tests / lint-and-test
#     * Validate bump.md & Run Basic Checks / validate (if applicable)
#   - Require branches to be up to date: YES
# - Block force pushes: YES
# - Require conversation resolution: YES
#
### Additional rules:
# - Require ATOM tag in PR title or commits
# - No direct pushes (PRs only)
# - Automatic deletion of head branches after merge

---

## Ruleset 2: Develop Branch Protection (Integration)
#
# Name: Develop Branch Protection  
# Enforcement: Active
# Target branches: develop
#
### Rules:
# - Restrict deletions: YES
# - Require a pull request before merging: YES
#   - Required approvals: 1
#   - Dismiss stale reviews: NO (allow faster iteration)
# - Require status checks to pass: YES
#   - Status checks required:
#     * CI - Code Quality and Tests / lint-and-test
# - Block force pushes: YES
#
### Additional rules:
# - Allow merge commits and squash merges
# - Require ATOM tags in commits

---

## Ruleset 3: Feature Branch Standards
#
# Name: Feature Branch Standards
# Enforcement: Evaluate (warnings only)
# Target branches: feature/*, feat/*, fix/*, docs/*, refactor/*, copilot/*
#
### Rules:
# - Require status checks to pass: YES (but allow bypass)
#   - Status checks required:
#     * CI - Code Quality and Tests / lint-and-test
# - Require conversation resolution: RECOMMENDED
#
### Additional rules:
# - Branch name must match pattern: (feature|feat|fix|docs|refactor|test|chore)/[a-z0-9-]+
# - Stale branches (30 days inactive) get flagged for cleanup

---

## Ruleset 4: Agent/Copilot Branch Protection
#
# Name: Agent Branch Protection
# Enforcement: Active
# Target branches: copilot/*, agent/*, claude/*
#
### Rules:
# - Require status checks to pass: YES
#   - Status checks required:
#     * CI - Code Quality and Tests / lint-and-test
#     * Claude PR Assistant / claude-interaction
# - Require ATOM tracking: YES
# - All changes must log to .claude/logs/
#
### Additional rules:
# - Auto-label with 'automated'
# - Require explicit approval for:
#   * Production file changes
#   * Secret additions
#   * Workflow modifications

---

## Ruleset 5: Documentation Protection
#
# Name: Documentation Standards
# Enforcement: Evaluate
# Target branches: ALL
# File patterns: **.md, docs/**
#
### Rules:
# - Require markdown linting to pass
# - Require ATOM tags in significant documentation
# - No broken links (if checker available)
#
### Additional rules:
# - Documentation changes should reference related code changes
# - Include examples for new features

---

## Ruleset 6: Secrets and Security
#
# Name: Security Enforcement
# Enforcement: Active
# Target branches: ALL
#
### Rules:
# - Block commits containing:
#   * API keys (pattern: ['\"]?[A-Za-z0-9_-]{32,}['\"]?)
#   * AWS keys (pattern: AKIA[0-9A-Z]{16})
#   * Private keys (pattern: -----BEGIN.*PRIVATE KEY-----)
#   * Passwords (pattern: password[\s]*[=:])
# - Require secret scanning to pass
# - No .env files (only .env.example)
#
### Additional rules:
# - All logs must be redacted with scripts/redact-log.sh
# - Sensitive data in code requires explicit approval

---

## Ruleset 7: Script and Code Quality
#
# Name: Script Quality Standards
# Enforcement: Active  
# Target branches: ALL
# File patterns: scripts/**.sh, **.ps1
#
### Rules:
# - Require shellcheck to pass (for .sh files)
# - Require PSScriptAnalyzer to pass (for .ps1 files)
# - All scripts must be executable (755 permissions)
# - Scripts must include:
#   * Shebang line
#   * Usage documentation
#   * Error handling (set -euo pipefail for bash)
#
### Additional rules:
# - Test coverage required for new scripts
# - Graceful degradation preferred over hard failures

---

## Ruleset 8: ATOM Compliance
#
# Name: ATOM Tracking Requirements
# Enforcement: Active
# Target branches: ALL (except personal forks)
#
### Rules:
# - All PRs must include ATOM tag
# - Format: ATOM-TYPE-YYYYMMDD-NNN-description
# - Decision files must be created for:
#   * Architecture changes
#   * New features
#   * Breaking changes
#   * Security fixes
#
### Additional rules:
# - ATOM counter must increment
# - Decision file must exist in .atom-trail/decisions/
# - Cross-reference related ATOM tags

---

## Implementation Priority

1. **Immediate** (Security & Main Branch):
   - Ruleset 6: Secrets and Security
   - Ruleset 1: Main Branch Protection

2. **High Priority** (Code Quality):
   - Ruleset 7: Script Quality
   - Ruleset 8: ATOM Compliance

3. **Medium Priority** (Process):
   - Ruleset 2: Develop Branch
   - Ruleset 4: Agent Branch Protection

4. **Nice to Have** (Standards):
   - Ruleset 3: Feature Branch Standards
   - Ruleset 5: Documentation Standards

---

## Bypass Permissions

Allow bypass for:
- Repository administrators (emergency fixes only)
- Dependabot (automated dependency updates)

Require justification and audit log for all bypasses.

---

## Monitoring and Audit

Create monthly reports on:
- Ruleset violations
- Bypass usage
- ATOM tag compliance
- Security scan results

Store reports in: `.github/compliance-reports/YYYY-MM.md`

---

## Notes

- Rulesets are cumulative - a branch can match multiple rulesets
- More specific rulesets take precedence
- Use "Evaluate" mode first to test new rules
- Adjust based on team feedback and workflow reality

---

**ATOM:** ATOM-DOC-20260102-002-custom-rulesets-configuration
**Last Updated:** 2026-01-02
**Owner:** @toolate28
