# Security Incident: Secret Leak — Action Template

Use this template to open an internal incident issue (label: `security/secret-leak`) when a secret is discovered.

Title: [SECURITY] Secret exposure: Cloudflare API token found in docs/history (rotated)

Body:
```
Summary:
- Secret type: Cloudflare API token
- Location discovered: `LOGDY_DEPLOYMENT_GUIDE.md` (documentation) and recent commit history
- Date discovered: 2026-01-07
- Detected by: automated/manual review

Immediate actions taken:
- Documentation redacted and placeholder inserted
- Security note added to docs advising rotation and history cleanup
- Secret-scan workflows added/updated (`.github/workflows/secret-scan.yml`)
- Local secrets scan run: `scripts/scan-secrets.sh` (results attached)

Required remediation (owner action):
1. Revoke the exposed Cloudflare API token immediately and create a new token with least privileges (Zone:Edit, Tunnel:Edit only if required).
2. Inspect Cloudflare audit logs for any suspicious activity between exposure and revocation.
3. If secret was committed to git history, remove it using `git filter-repo` or BFG and coordinate the force-push with all maintainers.
4. Update repo and CI to use the new token via GitHub Secrets (Organization/Repository secrets) and verify deployments.
5. Add proof of rotation (screenshot or audit log snippet) to this issue and close once verified.

Reference docs:
- `docs/SECURITY_INCIDENTS.md`
- `docs/SECURITY_COMMIT_GUIDELINES.md`
- `docs/SECURITY.md`

ATOM tag suggestion: `ATOM-SECURITY-20260107-001-secret-leak`

Reported by: @toolate28 (or whoever performs the action)
```
