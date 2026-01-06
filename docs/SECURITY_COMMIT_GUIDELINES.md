# Security & Commit Guidelines 🔒

Purpose: Keep secrets, personal files, and session artifacts out of the repository and public history.

Quick checklist before committing or creating a PR:

- [ ] Run `scripts/setup-precommit.ps1` to install pre-commit hooks (`detect-secrets`, `gitleaks`, basic checks).
- [ ] Confirm `.secrets.baseline` is up to date and contains only reviewed exceptions.
- [ ] Verify `.gitignore` includes: `.env`, `.env.*`, `.verification/`, `.vscode/`, `.ipynb_checkpoints/`, keys (`*.key`, `*.pem`), and other local artifacts.
- [ ] Search for obvious tokens in your changes: `git grep -iE "(password|secret|api[_-]?key|token|AKIA)" -- "$(git diff --name-only)"`
- [ ] Do not add real credentials in docs—use placeholders such as `REDACTED` or `your_api_key_here`.

If you find a secret committed (accidentally):

1. Revoke the secret immediately (rotate token/password).
2. Remove it from history using `git filter-repo` or BFG and force push (coordinate with the team).
3. Open an incident note and record the rotation proof in the security audit log.

Ephemeral session artifacts:
- `.verification/` should be ignored and preserved as CI build artifacts when needed; do NOT commit session files.

CI & PR requirements:
- PRs must pass the `secret-scan` workflow (Gitleaks + detect-secrets).
- Maintainers should review any exception in `.secrets.baseline` before merging.

Tools & setup:
- `pre-commit` with `detect-secrets` and `gitleaks` pre-commit hooks (see `scripts/setup-precommit.ps1`).
- `gitleaks` GitHub Action (runs on PRs) and `detect-secrets` scan in CI.

Contact & escalation:
- If unsure, ping the security owner (see `SECURITY.md`) or open an issue tagged `security/secret-leak`.