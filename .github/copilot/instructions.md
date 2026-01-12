## SpiralSafe Copilot Playbook (keep it short, specific, actionable)

**Mission context**
- Repo hosts the Coherence Engine for Safe Spiral: verification gates, ATOM decision trail, and documentation state markers. Start from [README.md](README.md) for narrative, [QUICK_START.md](QUICK_START.md) for commands, [archive/ARCHIVE_INDEX.md](archive/ARCHIVE_INDEX.md) for archived docs, and [docs/VERIFICATION_GATES.md](docs/VERIFICATION_GATES.md) for gate semantics.

**Non‑negotiables**
- Never write without an ATOM: generate with `./scripts/atom-track.sh TYPE "desc" "path"` (writes to .atom-trail/decisions and .claude/last_atom). Commit/PR titles must include the ATOM tag (format `ATOM-TYPE-YYYYMMDD-NNN-description`).
- Verification gates guard every phase. Source [scripts/lib/verification-gate.sh](scripts/lib/verification-gate.sh) and run `gate_intention_to_execution` before work; run `gate_execution_to_learning` before calling work “done”. Failed gates must be fixed, not bypassed.
- Docs need state markers (YAML frontmatter with status/last_verified/atom_tags). Archive docs keep their ATOM lineage; if you move or edit items under [archive/](archive), log the decision and update the archive index.
- Respect boundaries: append-only logs in [.atom-trail/](.atom-trail) and [.claude/logs/](.claude/logs); never touch .atom-trail/bedrock or delete logs.
- Media discipline: store binaries in [media/](media) (or subfolders) with a README describing source, license, and the ATOM that added it. Never embed large binaries in docs; link to media assets instead. Prefer SVG/PNG optimized; run `scripts/media-optimize.sh` when present.

**Layout that matters**
- [scripts/](scripts): utilities, gates library, hooks; follow `set -euo pipefail` and single-responsibility style. PowerShell scripts expect strict error preferences.
- [docs/](docs): coherence/verification references; check [docs/DOCUMENT_STATE_MARKERS.md](docs/DOCUMENT_STATE_MARKERS.md) when editing docs.
- [bump.md](bump.md): current mission context; gates fail if placeholders remain.
- [archive/](archive): historical material; keep ATOM tags when touching it.
- [.github/workflows/](.github/workflows): CI expects shellcheck/PSScriptAnalyzer, doc state validation, ATOM in titles. If adding workflows, keep jobs reusable, name gates clearly, and reuse the decision/secret scanning steps.

**Happy-path workflow**
- Before coding: `source scripts/lib/verification-gate.sh && gate_intention_to_execution` (ensures bump.md and context are complete).
- While coding: mirror existing script patterns, validate inputs, and log decisions with ATOM tags as you make them.
- Finish line: `./scripts/test-scripts.sh` (bash), `./scripts/scan-secrets.sh`, `./scripts/validate-document-state.sh`, plus any targeted checks (e.g., `./scripts/test-integration.sh` when gates/hooks change).
- Commit: `ATOM-...: summary` using the latest tag in `.claude/last_atom`; reference impacted files and decisions inside the body.
- Docs/media pipeline: add/update content with state markers, run `./scripts/validate-document-state.sh`, optimize assets, and if archiving, update [archive/ARCHIVE_INDEX.md](archive/ARCHIVE_INDEX.md) with reason/ATOM/date.
- Extensibility: new gates go in [scripts/lib/verification-gate.sh](scripts/lib/verification-gate.sh) with tests in `scripts/test-integration.sh`; new hooks live in [scripts/hooks/](scripts/hooks) and should log gate transitions. Add CI coverage in [.github/workflows](.github/workflows) when introducing new gate types.

**Implementation patterns**
- Bash: strict mode, guard optional deps with warnings, hard-fail required deps. Use repo-relative paths via `SCRIPT_DIR` pattern. Keep commands observable (echo progress, structured errors).
- PowerShell: `#Requires -Version 5.1`, `$ErrorActionPreference = "Stop"`, prefer `Write-Verbose`/`Write-Error`.
- Logging: append JSONL to .claude/logs/* and .atom-trail/gate-transitions.jsonl; never rewrite.
- Docs: always include frontmatter; prefer linking to assets in media rather than embedding. When adding patterns or case studies, cite ATOM tags and related gates.

**Safety & security**
- Run `./scripts/scan-secrets.sh` before PRs; no `.env` or secrets in git. CI expects shellcheck/PSScriptAnalyzer compliance for scripts and ATOM presence in commits/PR titles (see [ .github/RULESETS.md](.github/RULESETS.md)).
- If adding integrations (MCP servers, external APIs), document required env vars in `.env.example`, add secret names to [.github/SECRETS.md](.github/SECRETS.md), and gate usage with dependency checks.

**When in doubt**
- Check the gate output and the latest decision files in [.atom-trail/decisions](.atom-trail/decisions).
- Prefer updating existing patterns over inventing new ones; if you must diverge, create a DOC/DECISION ATOM and cite the rationale in-code and in docs.
