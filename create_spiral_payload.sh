#!/usr/bin/env bash
# Create the payload files and produce spiral_safe_bump_ci_payload.zip
# Usage:
#   chmod +x create_spiral_payload.sh
#   ./create_spiral_payload.sh
# Output:
#   spiral_safe_bump_ci_payload.zip

set -euo pipefail

OUTZIP="spiral_safe_bump_ci_payload.zip"
ROOTDIR="spiral_payload_tmp"

rm -rf "$ROOTDIR" "$OUTZIP"
mkdir -p "$ROOTDIR"

# Helper to write a file with directories created
write_file() {
  local path="$ROOTDIR/$1"
  mkdir -p "$(dirname "$path")"
  cat > "$path"
  echo "Wrote $path"
}

echo "Creating payload files under $ROOTDIR..."

# .github/workflows/validate-bump.yml
write_file ".github/workflows/validate-bump.yml" <<'YAML'
name: Validate bump.md & Run Basic Checks
on:
  pull_request:
    paths:
      - 'bump.md'
      - '.claude/**'
      - 'scripts/**'
      - '.github/**'
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup bash
        run: sudo apt-get update && sudo apt-get install -y jq

      - name: Make scripts executable
        run: |
          chmod +x scripts/validate-bump.sh || true
          chmod +x scripts/validate-branch-name.sh || true
          chmod +x scripts/atom-tag.sh || true

      - name: Validate bump.md presence
        run: |
          if [ ! -f bump.md ]; then
            echo "bump.md not found at repo root" && exit 1
          fi

      - name: Validate bump.md fields
        run: scripts/validate-bump.sh

      - name: Validate branch name (PR head ref)
        env:
          PR_REF: ${{ github.head_ref }}
        run: |
          # pass branch name to validator
          scripts/validate-branch-name.sh "${PR_REF}"
YAML

# .github/workflows/validate-branch-name.yml
write_file ".github/workflows/validate-branch-name.yml" <<'YAML'
name: Validate branch name on PR
on:
  pull_request:
    types: [opened, synchronize, reopened]
jobs:
  branch-name-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Run branch name validation
        run: |
          chmod +x scripts/validate-branch-name.sh || true
          echo "Validating branch: ${{ github.head_ref }}"
          scripts/validate-branch-name.sh "${{ github.head_ref }}"
YAML

# scripts/validate-bump.sh
write_file "scripts/validate-bump.sh" <<'BASH'
#!/usr/bin/env bash
set -euo pipefail

BUMP_FILE="bump.md"
REQUIRED_SECTIONS=("CURRENT STATE" "MISSION" "PERMISSION RULES" "STEPS" "VERIFICATION" "SUCCESS CRITERIA" "LOGGING / AUDIT")

if [ ! -f "$BUMP_FILE" ]; then
  echo "ERROR: $BUMP_FILE not found."
  exit 1
fi

content="$(tr '[:upper:]' '[:lower:]' < "$BUMP_FILE")"

missing=()
for sec in "${REQUIRED_SECTIONS[@]}"; do
  lowsec="$(echo "$sec" | tr '[:upper:]' '[:lower:]')"
  if ! grep -qi "$lowsec" "$BUMP_FILE"; then
    missing+=("$sec")
  fi
done

if [ ${#missing[@]} -ne 0 ]; then
  echo "ERROR: bump.md is missing required sections:"
  for m in "${missing[@]}"; do
    echo " - $m"
  done
  echo "Please add them before merging."
  exit 2
fi

# Basic smoke check: make sure 'autoApprove' or 'AWI' text exists
if ! grep -qiE "auto-?approve|awi|permission rules" "$BUMP_FILE"; then
  echo "WARNING: bump.md does not appear to define permission/auto-approve rules (AWI)."
  # not fatal but advised
fi

echo "bump.md basic validation passed."
exit 0
BASH

# scripts/validate-branch-name.sh
write_file "scripts/validate-branch-name.sh" <<'BASH'
#!/usr/bin/env bash
set -euo pipefail

# Usage: scripts/validate-branch-name.sh <branch-name>
BRANCH="${1:-}"

if [ -z "$BRANCH" ]; then
  # try to detect
  if git rev-parse --abbrev-ref HEAD >/dev/null 2>&1; then
    BRANCH="$(git rev-parse --abbrev-ref HEAD)"
  fi
fi

if [ -z "$BRANCH" ]; then
  echo "ERROR: Branch name not provided and could not be detected."
  exit 1
fi

# Allowed patterns:
# - New canonical: {type}/ATOM-{TYPE}-YYYYMMDD-NNN-{slug}
# - Legacy agent branches: claude/* or copilot/*
RE='^(feat|fix|docs|chore|refactor|test|ci|perf|build|revert)\/ATOM-[A-Z]+-[0-9]{8}-[0-9]{3}-[a-z0-9-]+$'
if [[ "$BRANCH" =~ ^claude\/.* ]] || [[ "$BRANCH" =~ ^copilot\/.* ]]; then
  echo "OK: Legacy agent branch allowed (grandfathered): $BRANCH"
  exit 0
fi

if [[ "$BRANCH" =~ $RE ]]; then
  echo "OK: Branch name matches canonical format: $BRANCH"
  exit 0
fi

echo "ERROR: Invalid branch name: $BRANCH"
echo "Expected formats:"
echo " - claude/* or copilot/* (agent branches, grandfathered)"
echo " - {type}/ATOM-{TYPE}-YYYYMMDD-NNN-{slug}"
echo "   e.g. feat/ATOM-FEAT-20251116-010-live-dashboard"
exit 2
BASH

# scripts/atom-tag.sh
write_file "scripts/atom-tag.sh" <<'BASH'
#!/usr/bin/env bash
set -euo pipefail

# Usage: scripts/atom-tag.sh TYPE "short description"
# Example: scripts/atom-tag.sh TASK "baseline tests passed"

TYPE="${1:-}"
DESC="${2:-}"

if [ -z "$TYPE" ] || [ -z "$DESC" ]; then
  echo "Usage: $0 TYPE \"short description\""
  exit 1
fi

DATE="$(date +%Y%m%d)"
PREFIX="ATOM-${TYPE}-${DATE}-"

# Find existing tags in git history or files that match today's prefix and extract highest sequence
# fallback to scanning repository files for occurrences
grep -RohE "ATOM-${TYPE}-${DATE}-[0-9]{3}" . || true
LAST_NUM=0
# try in git log
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  nums=$(git grep -hE "ATOM-${TYPE}-${DATE}-[0-9]{3}" || true | grep -oE "[0-9]{3}" || true)
  if [ -n "$nums" ]; then
    for n in $nums; do
      (( n10 = 10#$n ))
      if [ "$n10" -gt "$LAST_NUM" ]; then
        LAST_NUM="$n10"
      fi
    done
  fi
fi

NEXT_NUM=$(printf "%03d" $((LAST_NUM + 1)))
TAG="${PREFIX}${NEXT_NUM}"

# Make descriptive slug sanitized
SLUG=$(echo "$DESC" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-+|-+$//g' | cut -c1-60)

ATOM_TAG="${TAG}-${SLUG}"

# Optionally write to .claude/last_atom (create folder)
mkdir -p .claude
echo "${ATOM_TAG}" > .claude/last_atom
echo "${ATOM_TAG}"
# Caller may choose to commit / use this tag in a commit message
exit 0
BASH

# scripts/verify-environment.sh
write_file "scripts/verify-environment.sh" <<'BASH'
#!/usr/bin/env bash
set -euo pipefail

# Simple environment verification script used by build agents.
# Exits non-zero if a critical expectation is not met.

echo "Verifying environment..."

# Python
if command -v python3 >/dev/null 2>&1; then
  PYVER=$(python3 --version 2>&1 || true)
  echo "Python: $PYVER"
else
  echo "ERROR: python3 not found"
  exit 1
fi

# pytest
if python3 -c "import pytest" >/dev/null 2>&1; then
  echo "pytest: available"
else
  echo "WARNING: pytest not importable (may be missing). Try: pip install pytest"
fi

# node (optional)
if command -v node >/dev/null 2>&1; then
  NODEVER=$(node --version 2>&1 || true)
  echo "Node: $NODEVER"
else
  echo "Node: not present (OK if not required)"
fi

# .claude orientation presence
if [ -f .claude/ORIENTATION.md ]; then
  echo "ORIENTATION: OK"
else
  echo "WARNING: .claude/ORIENTATION.md not found; create one to reduce friction"
fi

# Verify logs dir writable
mkdir -p .claude/logs
if [ -w .claude/logs ]; then
  echo "logs: writable"
else
  echo "ERROR: .claude/logs not writable"
  exit 1
fi

echo "ENV OK"
exit 0
BASH

# scripts/redact-log.sh
write_file "scripts/redact-log.sh" <<'BASH'
#!/usr/bin/env bash
set -euo pipefail

# Simple redaction utility for logs.
# Usage: scripts/redact-log.sh input.jsonl output.jsonl

if [ $# -ne 2 ]; then
  echo "Usage: $0 input.jsonl output.jsonl"
  exit 1
fi

INPUT="$1"
OUTPUT="$2"

# Patterns to redact (case-insensitive)
RE_PATTERNS=('api_key' 'secret' 'password' 'authorization' 'token' 'access_key' 'private_key')

# Copy and redact lines
mkdir -p "$(dirname "$OUTPUT")"
while IFS= read -r line; do
  redacted="$line"
  for pat in "${RE_PATTERNS[@]}"; do
    redacted=$(echo "$redacted" | sed -E "s/(${pat}\":\")[^\"]+\"/\1<REDACTED>\"/Ig")
    redacted=$(echo "$redacted" | sed -E "s/(${pat}=)[^[:space:]]+/\1<REDACTED>/Ig")
  done
  echo "$redacted" >> "$OUTPUT"
done < "$INPUT"
exit 0
BASH

# .github/ISSUE_TEMPLATE/bug_report.md
write_file ".github/ISSUE_TEMPLATE/bug_report.md" <<'MD'
---
name: Bug report
about: Report a problem, include reproduction steps and ATOM tags if available
title: ''
labels: bug
assignees: ''
---

**Summary**
A clear and concise description of the bug.

**Steps to reproduce**
1.
2.
3.

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment**
- Repository:
- Branch:
- ATOM tag (if any):

**Logs / outputs**
Paste relevant log snippets or link to `.claude/logs/*`. Redact secrets.

**Additional context**
Add any other context about the problem here.
MD

# .github/ISSUE_TEMPLATE/feature_request.md
write_file ".github/ISSUE_TEMPLATE/feature_request.md" <<'MD'
---
name: Feature request
about: Suggest an improvement or new capability; the request should include an ATOM-style intent if possible
title: ''
labels: enhancement
assignees: ''
---

**Summary**
Short description of the desired feature.

**Motivation**
Why is this feature useful?

**Implementation ideas**
High-level notes on how this could be implemented (optional).

**Acceptance criteria**
- [ ] Small, testable goals for completion
- [ ] Verification commands/examples

**ATOM / Intent**
If you have an ATOM tag or intended intent line, include here:
`ATOM-<TYPE>-<YYYYMMDD>-NNN: <short intent>`
MD

# .github/PULL_REQUEST_TEMPLATE/pull_request.md
write_file ".github/PULL_REQUEST_TEMPLATE/pull_request.md" <<'MD'
---
name: Pull request template
about: Use this template for PRs that add CI, bump templates, or agent-facing files
title: ''
labels: ''
assignees: ''

---

## Summary

Describe the change in 1-2 sentences.

## Why

Why this change is needed and what it enables.

## What changed

- Files added
- Scripts
- CI workflows

## Verification / Testing

- [ ] `scripts/validate-bump.sh` passes locally
- [ ] `scripts/validate-branch-name.sh` tested on example branches
- [ ] `bash scripts/verify-environment.sh` prints `ENV OK`

## Notes

- Sensitive logs must be redacted before sharing
- Any change that allows production writes must be reviewed by a human
MD

# CODEOWNERS
write_file "CODEOWNERS" <<'TXT'
# CODEOWNERS — change to your team or individuals
# Lines are matched from top to bottom, later entries take precedence.
# Use GitHub handles or teams.

# Core documentation and bump files
/docs/ @toolate28
bump.md @toolate28

# Scripts and CI
/scripts/ @toolate28
.github/workflows/ @toolate28

# CLAUDE context files
.claude/ @toolate28

# Fallback
* @toolate28
TXT

# .gitignore
write_file ".gitignore" <<'TXT'
# Environment and local files
/.claude/settings.local.json
/.claude/state.json
/.claude/logs/
/.vscode/
/node_modules/
/dist/
/__pycache__/
*.pyc
.env
.env.local
.idea/
.DS_Store
TXT

# .gitattributes
write_file ".gitattributes" <<'TXT'
# Ensure consistent handling for bump.md and markdown
bump.md text=auto eol=lf
*.md text=auto eol=lf
*.sh text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
TXT

# .pre-commit-config.yaml
write_file ".pre-commit-config.yaml" <<'YAML'
repos:
  - repo: local
    hooks:
      - id: validate-bump
        name: Validate bump.md when modified
        entry: scripts/validate-bump.sh
        language: system
        files: ^bump\.md$
      - id: shellcheck
        name: Shellcheck scripts
        entry: shellcheck
        language: system
        files: ^scripts/.*\.sh$
        always_run: false
YAML

# bump.md
write_file "bump.md" <<'MD'
# BUMP: Authoritative Build Instructions (Template)
# Fill this file completely before a build/agent instance runs. One mission per bump.md.

ATOM: ATOM-TASK-YYYYMMDD-001
Title: <short: e.g. "Run unit tests and create baseline checkpoint">
Author: <architect name or id>
Date: <YYYY-MM-DD>

--- CURRENT STATE
- repo: <owner/repo or local path>
- branch: <branch name>
- last_verified: <YYYY-MM-DDThh:mm:ssZ>
- summary: <short summary of current validated state>

--- UNKNOWNs
- <explicit question the agent must NOT assume>
- e.g. "Is SendGrid test API key present?" "Are production secrets accessible?"

--- MISSION (one sentence)
Run the verified steps to validate environment and perform the mission. Keep changes minimal, idempotent and logged.

--- SYSTEM ENVIRONMENT (verification commands)
# The agent MUST run these before any modification. Each command must return expected value.
- Verify python: `python --version`  -> expected startswith "Python 3.11"
- Verify pytest: `python -m pytest --version` -> expected presence of pytest
- Verify node: `node --version` -> (if needed)
- Verify devcontainer hooks: `test -f .claude/ORIENTATION.md && echo "ORIENTATION OK"`

--- PERMISSION RULES (AWI)
# Auto-approve patterns (allowed without interactive permission)
autoApprove:
  enabled: true
  patterns:
    - "python -m pytest*"
    - "pytest*"
    - "npm test"
    - "npm run lint"
    - "bash scripts/verify-environment.sh"
# Explicit denies (must be proposed & approved)
deny:
  - "Write(./production/**)"
  - "Write(./secrets/**)"
  - "curl http://*"
# For other actions that change files, agent must:
# 1. Log proposed change to .claude/logs/proposed.jsonl
# 2. Wait for SAIF approval (human or pre-authorized verifier)

--- STEPS (ordered, idempotent)
1. `bash scripts/verify-environment.sh`  # exit non-zero -> abort
2. Create session checkpoint: `scripts/atom-tag.sh "TASK" "pre-tests checkpoint"` -> store tag
3. Run tests: `python -m pytest tests/ -q`  # allowed by autoApprove
4. If tests PASS:
     - Commit checkpoint: `git commit -m "ATOM: <tag> - baseline tests passed"`
     - Write SAIF applied flag: append JSON to `.claude/logs/applied.jsonl`
     - Update Current State below with timestamp and ATOM tag
5. If tests FAIL:
     - Write `.claude/logs/proposed.jsonl` entry with error output and suggested fix
     - Stop and append Work Session to this bump.md

--- VERIFICATION / TOMORROW'S TEST
# Explicit command + exact expected output (used to claim success)
- Command: `python -m pytest tests/ -q`
- Expected: exit code 0 and output containing `passed` (e.g. "3 passed")
- Environment check: `bash scripts/verify-environment.sh` must print `ENV OK`

--- LOGGING / AUDIT
# Agent must write these entries (JSONL)
access_log: `.claude/logs/access.jsonl`
proposed: `.claude/logs/proposed.jsonl`
applied: `.claude/logs/applied.jsonl`
# Redaction policy: remove any line matching `API_KEY|SECRET|PASSWORD` before writing to shared logs.

--- SUCCESS CRITERIA
- Tests pass (see Verification)
- SAIF applied entry appended
- Checkpoint commit created with ATOM tag and pushed (if push permitted)
- bump.md `Last Run Summary` updated with ATOM and brief 1-line result

--- ON FAILURE
- Append Work Session to bump.md with:
  - timestamp
  - attempted commands
  - exact outputs
  - proposed remediation (short)
- Do not attempt further changes beyond remediation proposal.

--- NEXT (architect instructions)
- If success: schedule the next bump (lint, doc check)
- If fail: architect to review proposed remediation and update bump.md

--- LAST RUN SUMMARY
- run_by: <agent id>
- started_at:
- finished_at:
- result: <success|failed|partial>
- atom_tag:
- logs: `.claude/logs/applied.jsonl` (line with atom_tag)

--- CONTACT / REVIEW
- Notify: `#channel-or-issue-template` (optional)
- Human reviewer: <name_or_handle>

# Author notes:
# - Keep missions narrow and unit-testable.
# - Use skills and templates in `.claude/skills/` (agent "read-first" requirement).
# - Architect must include exact expected outputs; avoid fuzzy success conditions.
MD

# .claude/ORIENTATION.md
write_file ".claude/ORIENTATION.md" <<'MD'
# ORIENTATION

Project: KENL / Safe Spiral — Agent/Build Orientation

Purpose:
Provide the single-page view of what this repository is, its constraints, and how an automated build agent should behave.

Quick checks:
- Run: `bash scripts/verify-environment.sh` → expect `ENV OK`
- Read: `.claude/CONTEXT.md` before starting any mission
- Skills: `.claude/skills/README.md`

Constraints:
- No writes to production directories unless bump.md explicitly allows
- All proposed source changes must be recorded in `.claude/logs/proposed.jsonl` and include ATOM tags

Verification:
- `scripts/verify-environment.sh`
- `scripts/validate-bump.sh`

Contact:
- Architect: @toolate28 (CODEOWNERS)
MD

# .claude/CONTEXT.md
write_file ".claude/CONTEXT.md" <<'MD'
# CONTEXT

**Last updated:** YYYY-MM-DDThh:mm:ssZ
**Active branch:** feature/architect/bump-and-ci
**Active mission:** Create bump.md + CI validation scaffolding
**Blockers:** None

Recent decisions:
- AWI autoApprove list includes pytest and verify-environment for early iterations
- Redaction policy: redact API_KEY, SECRET, PASSWORD tokens in logs

Next actions:
1. Validate bump.md locally with scripts/validate-bump.sh
2. Run verify-environment.sh
3. Build instance should run bump.md mission (tests)
MD

# .claude/skills/README.md
write_file ".claude/skills/README.md" <<'MD'
# SKILLS: read-first list

Agents MUST read these in order before making modifications.

1. templates/ORIENTATION-TEMPLATE.md (if present)
2. bump.md (authoritative mission file)
3. behavior-library-handbook.md
4. scripts/verify-environment.sh (how environment is validated)
5. scripts/atom-tag.sh (how to generate ATOM tags)
6. scripts/redact-log.sh (how to sanitize logs)

If any skill is missing, log the read attempt to `.claude/logs/access.jsonl` and stop.
MD

# .claude/BUILD_ORIENTATION.md
write_file ".claude/BUILD_ORIENTATION.md" <<'MD'
# Build Orientation for Claude (build agent)

Purpose: Guidance for an automated Claude instance performing build missions from bump.md.

Steps:
1. Load `.claude/ORIENTATION.md` and `.claude/CONTEXT.md`
2. Read `.claude/skills/README.md` and each listed SKILL.md
3. Validate bump.md using `scripts/validate-bump.sh`
4. Run environment verification `bash scripts/verify-environment.sh`
5. Create ATOM tag: `scripts/atom-tag.sh TASK "build-start"`
6. Execute permitted steps in bump.md (respect AWI autoApprove)
7. Log all actions to `.claude/logs/*.jsonl` and redact using `scripts/redact-log.sh` before shared publishing
8. On success/failure update bump.md Last Run Summary and write SAIF flag

Safety:
- Do not write to production paths unless explicitly allowed in bump.md
- If uncertain, propose change and append to `.claude/logs/proposed.jsonl`

Contact: Architect (human) must review any proposed write to source files.
MD

echo "All files created. Creating zip archive $OUTZIP ..."
cd "$ROOTDIR"
zip -r "../$OUTZIP" .
cd ..
echo "Zip archive created: $OUTZIP"
echo "Payload ready. Remove $ROOTDIR when done: rm -rf $ROOTDIR"
