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

<<<<<<< HEAD
- PRs must pass the `secret-scan` workflow (Gitleaks + detect-secrets). The Gitleaks job is scheduled daily and uploads a report artifact for audits; maintainers should block merges on critical findings.
=======
- PRs must pass the `secret-scan` workflow (Gitleaks + detect-secrets).
>>>>>>> main
- Maintainers should review any exception in `.secrets.baseline` before merging.

Tools & setup:

- `pre-commit` with `detect-secrets` and `gitleaks` pre-commit hooks (see `scripts/setup-precommit.ps1`).
- `gitleaks` GitHub Action (runs on PRs) and `detect-secrets` scan in CI.

Contact & escalation:

- If unsure, ping the security owner (see `SECURITY.md`) or open an issue tagged `security/secret-leak`.
<<<<<<< HEAD

---

## Iteration log

- **2026-01-07 (Iteration 1):** Added `.secrets.baseline`, initial triage, and untracked `.verification/` artifacts. See `docs/SECURITY_TRIAGE.md` for detailed rationale.
- **2026-01-07 (Iteration 2):** Documentation hygiene pass — redacted hardcoded tokens (Cloudflare), standardized GitHub token placeholders to `your_github_pat_here`, and replaced example tokens in scripts and docs to reduce false positives.
- **Next (Iteration 3):** Enforce CI gating for secret scans and add scheduled Gitleaks retention/alerting; prepare PR updates to require maintainers to review any `.secrets.baseline` changes.
=======
>>>>>>> main
