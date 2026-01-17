# Detect-Secrets Triage Log

**ATOM:** ATOM-DOC-20260107-005-security-triage-log

This file records why specific findings were allowlisted in `.secrets.baseline`.

Entries (2026-01-07):

- `.atom-trail/decisions/*` — Base64/Hex high-entropy strings were identified as decision artifacts and not developer secrets; allowlisted after review.
- `.atom-trail/sessions/*` and `.verification/*` — Session and verification artifacts contain digests and non-secret identifiers used for audit; allowlisted; `.verification/` files were untracked and added to `.gitignore`.
- `.github/SECRETS.md` — Documentation placeholders (templates and examples) are intentionally present; entries marked as `REDACTED` where necessary.
- `archive/releases/ops-1.0.1/RELEASE_MANIFEST.json` — Contains release artifact digests; verified as non-sensitive.

If a finding is later suspected to be an actual secret, remove the allowlist entry and follow rotation/remediation procedures in `docs/SECURITY_COMMIT_GUIDELINES.md`.
