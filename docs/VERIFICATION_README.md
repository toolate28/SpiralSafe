# Verification & Setup Helpers

This folder contains helper scripts to bootstrap local environments, compute repository hashes, and generate a small verification report.

Files added:

- `scripts/bootstrap.ps1` — conservative bootstrap helper (dry-run by default).
- `scripts/hash_all.ps1` — compute SHA256 for files and optionally write `hashes.sha256`.
- `scripts/verify_claims.ps1` — generate host and session IDs and SHA256-based signatures; writes `verification_report.md` when run with `-Apply`.
- `scripts/walk_journeys.ps1` — simulate forward/backward walks of doc/script pipelines (dry-run by default).

Usage examples (PowerShell / Windows):

```powershell
# Preview bootstrap
.\scripts\bootstrap.ps1

# Run bootstrap (careful, installs are conservative)
.\scripts\bootstrap.ps1 -Apply

# Compute hashes (dry-run)
.\scripts\hash_all.ps1

# Compute hashes and write output
.\scripts\hash_all.ps1 -Out hashes.sha256 -Apply

# Generate verification report (dry-run)
.\scripts\verify_claims.ps1

# Write verification report
.\scripts\verify_claims.ps1 -Out verification_report.md -Apply

# Simulate journey walk (dry-run)
.\scripts\walk_journeys.ps1

# Simulate real walk (copies to temp)
.\scripts\walk_journeys.ps1 -Apply
```

Notes:
- All scripts default to DryRun mode; use `-Apply` to perform actions that modify files.
- The built-in signatures are SHA256 digests for convenience and are not a substitute for PKI/GPG signing.
