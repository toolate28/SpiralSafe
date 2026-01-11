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
