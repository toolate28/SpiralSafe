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
