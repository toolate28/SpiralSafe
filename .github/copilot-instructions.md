# Copilot / Agent Quick Guide for SpiralSafe

Purpose: Short, actionable instructions to help AI coding agents be immediately productive in this repository.

## Start here (big-picture)
- Read: `ARCHITECTURE.md` (high-level layers) and `.github/AGENTS.md` (agent roles & coordination).
- Key design artifacts: `protocol/wave-spec.md`, `protocol/bump-spec.md`, `methodology/atom.md` (how work is chunked), and `foundation/*` for theory.
- Related repos: `wave-toolkit` (coherence), `kenl` (ATOM trail), `quantum-redstone`, `ClaudeNPC-Server-Suite`.

## What to read first for a task
- For protocol or handoff changes: `protocol/bump-spec.md` and `.context.yaml` examples.
- For documentation coherence work: `protocol/wave-spec.md` and `project-book.ipynb`.
- For ops & verification helpers: `ops/README.md`, `ops/scripts/session_report.py`, `ops/scripts/sign_verification.py`, `ops/scripts/Transcript-Pipeline.ps1`.

## Local dev & CI (how to run things)
- Node (repo uses Node 20 in CI). Common commands:
  - npm ci
  - npm run typecheck
  - npm run lint
  - npm test
  - npm run build
- Lint & static analysis:
  - Shell scripts: `shellcheck` (pre-commit and CI)
  - PowerShell: `PSScriptAnalyzer` (invoked in CI)
- CI specifics: `.github/workflows/spiralsafe-ci.yml` runs a document "coherence" (wave) analysis before lint/build, then runs lint, typecheck, tests, and Cloudflare deploys with AWI grants.

## Project-specific patterns & conventions (must follow)
- H&&S markers (protocol/bump-spec.md): use `H&&S:WAVE` for soft handoff (add to PR body for review), `H&&S:PASS` to transfer ownership, `H&&S:SYNC` for synchronization, `H&&S:BLOCK` for blocking issues. Examples: include `H&&S:WAVE` in PR body for architectural changes.
- Commit message format: `[layer] Brief description` (layers e.g. `[protocol]`, `[interface]`, `[methodology]`). See `CONTRIBUTING.md`.
- Dual-format docs: Many files follow a dual-format convention—prose + structured summary (`.context.yaml` style). Preserve both when adding or editing docs.
- Atom trail: project sessions and decisions live in `.atom-trail/` (subdirs: `decisions`, `sessions`, `verifications`). Use `ops/scripts/session_report.py` (`start` / `signout`) for session work, and `ops/scripts/sign_verification.py` to record human signatures.
- Verification & signing:
  - Start a session: `python ops/scripts/session_report.py start "desc"`
  - Sign out: `python ops/scripts/session_report.py signout <ATOM_TAG>`
  - Add verification: `python ops/scripts/sign_verification.py <VER_TAG> --name "your-name"`
  - Encryption helper: `ops/scripts/Transcript-Pipeline.ps1` (PowerShell, AES-256-GCM)
  - Verify signatures: documented as `ss-verify <path>` in docs (see `ops/DEPLOYMENT_ARCHITECTURE.md`).

## Integration points & external dependencies
- Cloudflare (wrangler) deploys in CI; AWI grant requests are created during deploy job (`SPIRALSAFE_API_BASE` used for API calls).
- Coherence analysis reports to the Wave API (`/api/wave/analyze`) during CI.
- `kenl` and other companion repos may provide local `~/.kenl/.atom-trail` artifacts used by scripts—be cautious when modifying atom-tracking code.

## Role-specific guidance for agents
- Claude / structural agents: propose architecture or policy changes (protocol, bump, wave). Add `H&&S:WAVE` and include rationale + specific file changes. For semantic conflicts, Claude's version is preferred as the architectural authority (see `.github/AGENTS.md`).
- Copilot / code agents: focus on formatting, tests, linting, small refactors, and PR polish. Prefer Copilot fixes for markdown, style, and CI-failing items.
- Always include exact file references and minimal, testable changes. For edits affecting `protocol/*` or `foundation/*`, open an issue first and include `H&&S:WAVE` in the PR body.

## Examples
- PR body minimal template (soft handoff):
  - Title: `feat(protocol): clarify bump state transitions`
  - Body: `H&&S:WAVE — clarify how H&&S:SYNC is created by CI bump API; see protocol/bump-spec.md`.
- Commit example: `[protocol] Add H&&S:SYNC creation script`.

## Quick checklist for PRs
- Add or update `.context.yaml` or structured summary for documentation changes.
- Run `npm ci && npm run typecheck && npm run lint && npm test` locally (or run the subset relevant to your changes).
- If you touch scripts, run ShellCheck / PSScriptAnalyzer locally to mirror CI.
- Add appropriate `H&&S` marker in PR body before requesting Copilot/Claude review.

## Where to ask for help
- Humans: file an issue and tag maintainers.
- Agents: follow `.github/AGENTS.md` coordination flow (`Claude -> H&&S:WAVE -> Copilot -> Human`).

---
If you'd like, I can open a PR to add this file (or expand any section with examples tailored to a specific subdirectory). Feedback? Any section you want shifted or expanded?