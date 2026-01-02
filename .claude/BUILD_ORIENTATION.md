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
