# Security & Commit Guidelines 🔒

Purpose: Keep secrets, personal files, and session artifacts out of the repository and public history.

Quick checklist before committing or creating a PR:

- [ ] Run `scripts/setup-precommit.ps1` to install local pre-commit checks.
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

- PRs must pass the `secret-scan` workflow (internal fail-closed scanner).
- Maintainers should review any exception in `.secrets.baseline` before merging.

Tools & setup:

- `scripts/scan-secrets.sh` for internal repository scanning logic.
- `secret-scan` GitHub workflow enforces fail-closed CI execution of the internal scanner.

Contact & escalation:

- If unsure, ping the security owner (see `SECURITY.md`) or open an issue tagged `security/secret-leak`.
