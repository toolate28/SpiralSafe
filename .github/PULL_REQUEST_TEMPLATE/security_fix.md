### Summary
- Redacted example secrets and replaced realistic examples with placeholders in `.github/SECRETS.md`
- Added a security note to `LOGDY_DEPLOYMENT_GUIDE.md` advising rotation and history cleanup if secrets are found
- Added incident log `docs/SECURITY_INCIDENTS.md` and an action template `docs/SECURITY_INCIDENT_ACTIONS.md`
- Updated `.github/workflows/secret-scan.yml` to run `detect-secrets`, `gitleaks`, and the repo `scripts/scan-secrets.sh`
- Clarified placeholder/test comments in `scripts/test-integration.sh` and example placeholders in `ops/schemas/PLATFORM_MATRIX.md` and `docs/TROUBLESHOOTING_MCP.md`

### Verification
- Ran `./scripts/scan-secrets.sh` to verify no remaining obvious secrets in working tree (only finding: previous commit history contained an example token; see notes).
- Please **rotate** any exposed/affected tokens (Cloudflare) immediately and document rotation in the issue created for the incident.

### Follow-ups
- Remove the token from git history if it existed in any pushed commits: use `git filter-repo` or BFG and coordinate a force-push with maintainers
- Create an ATOM security tag: `ATOM-SECURITY-20260107-001-secret-leak`
- Open issue `security/secret-leak` with details (use `docs/SECURITY_INCIDENT_ACTIONS.md` template)

**Labels:** security, chore, infra
