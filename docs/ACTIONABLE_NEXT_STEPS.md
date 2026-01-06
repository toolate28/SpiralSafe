# Actionable Next Steps — Short-term

1. Add dependency manifests
   - Create `package.json` with `markdown-link-check` and `markdownlint-cli` pinned.
   - Create `requirements.txt` listing any Python packages used by `scripts/` (e.g., pyyaml, requests).

2. CI & Linting
   - Add PSScriptAnalyzer step in `.github/workflows/` to lint PowerShell scripts.
   - Ensure `markdown-and-linkcheck.yml` runs successfully and produces actionable reports. Pin Node version.

3. Consolidate script utilities
   - Move repeated helper functions into `scripts/lib/utils.ps1` and import from each script.

4. Notebook verification
   - Add a workflow to compute Merkle root of critical files and project-book.ipynb; record artifact.

5. Secret management
   - Add `REPO_PAT` only if bot account push behavior is required.

6. Documentation
   - Update `docs/WORKFLOWS_README.md` to include runbook for `apply=true` decisions and rollback instructions.

7. Merge plan
   - Merge infra changes (workflows, scripts) first in a small PR.
   - Run dry-run workflows for 48 hours and collect artifacts.
   - If stable, run `docs-reorg` in apply mode behind a review step.
