# SKILLS: read-first list

Agents MUST read these in order before making modifications.

1. templates/ORIENTATION-TEMPLATE.md (if present)
2. bump.md (authoritative mission file)
3. behavior-library-handbook.md
4. scripts/verify-environment.sh (how environment is validated)
5. scripts/atom-tag.sh (how to generate ATOM tags)
6. scripts/redact-log.sh (how to sanitize logs)

If any skill is missing, log the read attempt to `.claude/logs/access.jsonl` and stop.
