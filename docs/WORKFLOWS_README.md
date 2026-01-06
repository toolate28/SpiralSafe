# Workflows & Automation

This document explains the repository workflows added to automate safe, dry-run-first operations for the SpiralSafe repo.

Workflows added:

- `.github/workflows/scripts-runner.yml` — Run local helper scripts (dry-run by default). Manual dispatch input `apply` toggles `-Apply` for scripts.
- `.github/workflows/docs-reorg.yml` — Run the `apply-docs-reorg-full_Version1.ps1` script. Dry-run by default; when `apply=true` the workflow commits, pushes to the target branch, and opens a PR. Uses `GITHUB_TOKEN` to create the PR.
- `.github/workflows/verify-and-hash.yml` — Scheduled daily and manual dispatch. Runs `verify_claims.ps1` and `hash_all.ps1`. Uploads artifacts.
- `.github/workflows/journey-sim.yml` — Designed to run on a self-hosted runner; simulates forward/backward pipeline walks. `apply=true` triggers safe copy/restore simulation and requires a self-hosted runner.

Security & required secrets
- `GITHUB_TOKEN` — automatically provided to workflows; sufficient for commit/push/PR within the same repository. No action needed.
- If you want workflows to push as a different bot account or access other repos, provide a Personal Access Token with `repo` and `workflow` scopes as a repo secret (e.g. `REPO_PAT`).
- External services (optional): `CLOUDFLARE_API_TOKEN`, `DOCKERHUB_TOKEN`, etc. Add as repo secrets if you intend to enable automated deploy steps.

Safety defaults
- Every workflow defaults to dry-run behaviour. `apply` must be explicitly passed as workflow input or via a manual run to enable write operations.
- `journey-sim.yml` is intended for self-hosted runners to avoid exposing host-level operations on GitHub-hosted runners.

How to run

From GitHub Actions UI: open the repository > Actions > pick the workflow > Run workflow. Set input `apply` to `true` only when you intend to write changes.

From CLI (using `gh`):

```bash
# Example: run verify-and-hash manually (dry-run)
gh workflow run verify-and-hash.yml

# Example: run docs reorg in dry-run
gh workflow run docs-reorg.yml

# Example: run with apply=true
gh workflow run docs-reorg.yml -f apply=true -f target_branch=docs/cleanup/root-docs-consolidation
```

Self-hosted runner notes
- To run `journey-sim.yml` with `apply=true`, register a self-hosted runner on a machine you control and give it the `self-hosted, Windows` labels. The workflow will then be able to perform copy/restore simulation on that host.

Next steps you can provide me to further automate

- Add `REPO_PAT` to repo secrets if you want PRs opened under a different bot account.
- Provide Cloudflare / registry tokens as repo secrets if you want the workflows to perform deployments.
- Confirm whether `docs-reorg.yml` should create the PR automatically on `apply=true` (currently does).
