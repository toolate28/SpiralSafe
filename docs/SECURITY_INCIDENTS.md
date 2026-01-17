# Security Incidents Log

This document records security incidents, exposures, and remediation steps. Maintain a short timeline and actions taken; link to relevant ATOM tags and issues.

## INCIDENT: Exposed Cloudflare API token in `LOGDY_DEPLOYMENT_GUIDE.md`

- **Date discovered:** 2026-01-07
- **Detected by:** Manual review during audit
- **Severity:** Medium (token found in documentation; token may have limited scopes)

### Actions taken immediately

1. Removed/redacted token from documentation and replaced with placeholder: `your_cloudflare_api_token_here`. (commit)
2. Added **Security note** to `LOGDY_DEPLOYMENT_GUIDE.md` advising to rotate/revoke and remove token from history if found.
3. Added/updated secret-scan workflows (`.github/workflows/secret-scan.yml`) to run `gitleaks` and `detect-secrets` on PRs and pushes to `main`.
4. Added an entry to the security incidents log (this file).
5. Recommended immediate rotation/revocation of the impacted Cloudflare token (owner action required). See _Remediation Steps_ below.

### Remediation Steps (recommended)

- Revoke the exposed API token in Cloudflare and create a new token with the minimum required scopes.
- Inspect Cloudflare audit logs for unauthorized activity between the time the token was exposed and now.
- Rotate any secrets that may have been derived from or used with the token (CI secrets, deployment pipelines).
- **History note:** The scan detected examples of the token in recent commits (now redacted). If secrets appear in the git history, remove them using `git filter-repo` or BFG and coordinate a force-push with all maintainers; see `docs/SECURITY_COMMIT_GUIDELINES.md` for steps.
- Run `./scripts/scan-secrets.sh` across the repo and fix any findings.
- Create an ATOM security tag and open an internal `security/secret-leak` issue documenting rotation proof.

### Follow-up tasks

- [ ] Verify no other tokens exist in repo or recent commits
- [ ] Validate secret-scan workflow triggers on PRs and blocks merges when secrets are detected
- [ ] Add `CLOUDFLARE_API_TOKEN` to the org/team secrets and update deployment docs to reference secrets instead of inline tokens

---
