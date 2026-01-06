# Repository Review — SpiralSafe

Generated: 2026-01-07 UTC

This document captures a focused, practical review of the SpiralSafe repository aimed at:
- surfacing load-bearing issues and hidden dependencies
- identifying patterns and anti-patterns
- providing an actionable, prioritized remediation plan

Scope
- All root-level documentation and scripts under repository root
- `scripts/`, `.github/`, `ops/`, `docs/`, `interface/`, and `meta/`

Summary Findings (high-level)
- The repository is documentation-rich and intentionally designed to surface issues.
- Safer-by-default behavior has been implemented in scripts and workflows (dry-run defaults), but a few spots needed tightening (explicit `-DryRun`, default switches).
- New CI workflows and verification tooling were added to help automation; ensure secrets and self-hosted runner steps are provisioned before enabling destructive modes.

Load-bearing issues (high priority)
1. apply-docs-reorg-full_Version1.ps1 — powerful, repo-restructuring script. Risk: if run with `-AutoConfirm` on the wrong branch it will rewrite and commit many docs. Mitigation: keep DryRun default, require explicit `-AutoConfirm` and prefer merging via PR only.
2. Lack of a centralized dependency manifest for tooling — various tools (node, python packages, powershell modules) are referenced but not consistently pinned. Add `package.json` (for node) and `requirements.txt` top-level where appropriate.
3. Workflows that run host-level simulations (`journey-sim.yml`) require a self-hosted runner. Risk if run accidentally on hosted runners; label and documentation added but ensure organization-level policy.

Patterns & Anti-patterns
- Pattern: Dual-format docs (prose + machine-readable summaries) — good for both readers and tools.
- Pattern: Dry-run-first automation — safe and reduces accidental mutation.
- Anti-pattern: Multiple similar scripts doing overlapping tasks (verify/hash/walk). Consolidate common utilities into `scripts/lib` to reduce duplication.
- Anti-pattern: Some large markdown files include embedded ASCII art and long banners which reduce machine readability in automated link-checks — preserve but consider separate `showcase/` or `assets/` folder.

Mass and Negative Space
- Mass: large code/docs blobs concentrated in root. Moving to `docs/` was planned by reorg script; follow PR workflow to relocate while preserving history.
- Negative space: missing tests and CI checks for scripts themselves (PSScriptAnalyzer for PowerShell, Python linting). Add linters as workflow steps.

Dependency and Integration Risks
- External services (Cloudflare, Docker, Twilio, Signal) referenced in docs; automation requiring their credentials must gate use and require repo secrets.
- `apply-docs-reorg` uses `git` — ensure workflows run in a checkout with persist-credentials and that `GITHUB_TOKEN` or `REPO_PAT` is available when pushing.
- Notebook verification (project-book.ipynb) references local ops scripts for Merkle/verification. The notebook should be runnable in a controlled CI environment; add a verification workflow or a Docker devcontainer for reproducibility.

Security & Secrets
- Do not commit secrets. Use `gh secret` to populate `REPO_PAT`, `CLOUDFLARE_API_TOKEN`, etc.
- Workflows: prefer `GITHUB_TOKEN` for in-repo operations; require `REPO_PAT` only when cross-repo or bot-account behavior is desired.

Operational Recommendations (prioritized)
1. Keep `apply-docs-reorg-full_Version1.ps1` dry-run default; add an explicit `--confirm` CLI flag (already implemented as `-AutoConfirm`). Add extra safety checks: verify branch equals expected branch unless `--force` provided.
2. Add PSScriptAnalyzer and markdownlint to CI for script and doc hygiene.
3. Add `requirements.txt` or `pyproject.toml` for Python tools used in `scripts/` and a `package.json` for node tools used by markdown linkcheck.
4. Consolidate utility functions used by scripts into `scripts/lib/` and reference them from other scripts.
5. Add a `devcontainer.json` describing a reproducible developer environment (Node, Python, pwsh) and a `Makefile` or top-level `scripts/bootstrap.ps1` (already added) to standardize setup.

Actionable short-term checklist
- [ ] Add `requirements.txt` if Python tools used (or point to existing). 
- [ ] Add `package.json` and lockfile to pin Node versions for markdown link-check.
- [ ] Add PSScriptAnalyzer check in a workflow.
- [ ] Add linting for shell scripts and Python (flake8/ruff).
- [ ] Run `scripts/hash_all.ps1` and `scripts/verify_claims.ps1` locally and upload artifacts to Actions (verify-and-hash workflow).

Interesting notes / observations
- `project-book.ipynb` contains a living verification section with Merkle root computation — formalize this in CI to capture the notebook's integrity after merges.
- The repo uses `H&&S:WAVE` signature conventions consistently — consider automation to check for missing signatures in new docs.

Appendix: key files referenced
- `apply-docs-reorg-full_Version1.ps1`
- `.github/workflows/*.yml` (newly added workflows: scripts-runner, docs-reorg, verify-and-hash, journey-sim, markdown-and-linkcheck)
- `scripts/bootstrap.ps1`, `scripts/hash_all.ps1`, `scripts/verify_claims.ps1`, `scripts/walk_journeys.ps1`
- `project-book.ipynb`

If you want, I will now: (pick one)
- expand this into an issue template and create high-priority Issues in the repo for the top 5 items (requires GH write access), or
- prepare a patch that adds `package.json`, `requirements.txt`, PSScriptAnalyzer workflow and devcontainer scaffolding for you to review before committing.
