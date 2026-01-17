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
