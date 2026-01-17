# Copilot / Agent Quick Guide for SpiralSafe

Purpose: Short, actionable instructions to help AI coding agents be immediately productive in this repository.

## Start here (big-picture)
- Read: `ARCHITECTURE.md` (high-level layers) and `.github/AGENTS.md` (agent roles & coordination).
- Key design artifacts: `protocol/wave-spec.md`, `protocol/bump-spec.md`, `protocol/sphinx-spec.md`, `methodology/atom.md` (how work is chunked), and `foundation/*` for theory.
- Related repos: `wave-toolkit` (coherence), `kenl` (ATOM trail), `quantum-redstone`, `coherence-mcp`, `spiralsafe-mono`, `QDI`.

## Protocol Stack (WAVE → SPHINX → BUMP → ATOM)

```
WAVE ──► SPHINX ──► BUMP ──► ATOM
         │
         ├─ ORIGIN:     "Where do you come from?"
         ├─ INTENT:     "What do you seek?"
         ├─ COHERENCE:  "Are you whole?" (>60%)
         ├─ IDENTITY:   "Who are you?"
         └─ PASSAGE:    "You may pass."
```

### SPHINX Protocol (Guardian Gates)
The **S**ecure **P**rotocol for **H**ierarchical **I**dentity, **N**avigation, and e**X**change guards all transitions between system boundaries.

| Gate | Marker | Function | Riddle |
|------|--------|----------|--------|
| ORIGIN | `SPHINX:ORIGIN` | Verify genesis lineage | "Where do you come from?" |
| INTENT | `SPHINX:INTENT` | Verify stated purpose | "What do you seek?" |
| COHERENCE | `SPHINX:COHERENCE` | Verify >60% threshold | "Are you whole?" |
| IDENTITY | `SPHINX:IDENTITY` | Verify agent/user auth | "Who are you?" |
| PASSAGE | `SPHINX:PASSAGE` | Grant transition | "You may pass." |

**Syntax:**
```markdown
<!-- SPHINX:COHERENCE
  threshold: 0.6
  source: wave_analyze
  result: 0.72
  verdict: PASSAGE
-->
Coherence verified. Proceeding to BUMP handoff.
<!-- /SPHINX:COHERENCE -->
```

### Self-Referential Loop Termination
- Each SPHINX gate logs its own passage to ATOM trail
- New loops require distinct, auditable genesis events
- No action can cycle without satisfying all gate riddles
- Surjection supported: every output maps to a verifiable input

## What to read first for a task
- For protocol or handoff changes: `protocol/bump-spec.md`, `protocol/sphinx-spec.md` and `.context.yaml` examples.
- For documentation coherence work: `protocol/wave-spec.md` and `project-book.ipynb`.
- For ops & verification helpers: `ops/README.md`, `ops/scripts/session_report.py`, `ops/scripts/sign_verification.py`.

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
- CI specifics: `.github/workflows/spiralsafe-ci.yml` runs coherence (wave) analysis, SPHINX gate checks, then lint/typecheck/tests.

## Project-specific patterns & conventions (must follow)
- **H&&S markers** (protocol/bump-spec.md): use `H&&S:WAVE` for soft handoff, `H&&S:PASS` to transfer ownership, `H&&S:SYNC` for synchronization, `H&&S:BLOCK` for blockers.
- **SPHINX markers**: use `SPHINX:ORIGIN`, `SPHINX:INTENT`, `SPHINX:COHERENCE`, `SPHINX:IDENTITY`, `SPHINX:PASSAGE` for guardian gate verification.
- **Commit message format**: `[layer] Brief description` (layers e.g. `[protocol]`, `[interface]`, `[methodology]`).
- **ATOM tagging**: Format `ATOM-TYPE-YYYYMMDD-NNN-description`. Types: INIT, FEATURE, FIX, DOC, REFACTOR, TEST, DECISION, RELEASE, TASK.
  - ATOM tags in commit messages are automatically extracted and logged to the SpiralSafe API
  - Regex pattern: `ATOM-[A-Z]+-[0-9]{8}-[0-9]{3}-[a-z0-9-]+`
- **Dual-format docs**: Many files follow prose + structured summary (`.context.yaml` style). Preserve both.
- **Atom trail**: project sessions and decisions live in `.atom-trail/` (subdirs: `decisions`, `sessions`, `verifications`).

## CoM Analysis Pattern (Center of Mass / Soul)
When agent task divergence occurs, perform CoM analysis:
1. **Identify the pull**: What did the agent weight toward?
2. **Identify user intent**: What was the actual goal?
3. **Measure delta (noise)**: Where did retrieval vs generation mode mismatch?
4. **Correct CoM**: Shift to appropriate mode (archaeologist vs architect)

| Mode | When to Use | Agent Behavior |
|------|-------------|----------------|
| Retrieval | Search existing artifacts | Archaeologist mode |
| Generation | Create new protocols/names | Architect mode |
| Naming/Genesis | Mythological resonance needed | Creative/generative |

## Spiral Closure & Auto-Resolution
- **Mechanical propagation issues** are auto-resolved (no user approval needed)
- **Creative/genesis tasks** require explicit user input
- **Loop termination**: All SPHINX gates satisfied = spiral closed
- **Surjection**: Every propagation output maps to auditable input

## API integration patterns
- **Authentication**: Use `X-API-Key` header with `secrets.SPIRALSAFE_API_KEY`
- **Endpoints**:
  - `POST /api/atom/create` - Log ATOM tags
  - `POST /api/bump/create` - Create bump markers
  - `POST /api/wave/analyze` - Analyze coherence
  - `POST /api/sphinx/gate` - Verify SPHINX gate passage
  - `POST /api/awi/request` - Request AWI grants

## Security requirements
**NEVER commit:** API keys, tokens, passwords, credentials, `.env` files with sensitive data.
**ALWAYS:** Use GitHub Secrets, include `.env.example` with placeholders only.

## Role-specific guidance for agents
- **Claude / structural agents**: propose architecture/policy changes. Add `H&&S:WAVE` + `SPHINX:INTENT`.
- **Copilot / code agents**: formatting, tests, linting, small refactors. Verify `SPHINX:COHERENCE` before merge.
- **All agents**: Include ATOM tag lineage, cross-link parent/child issues, state true deliverable.

## Quick checklist for PRs
- [ ] SPHINX:ORIGIN - Genesis lineage verified
- [ ] SPHINX:INTENT - Purpose stated
- [ ] SPHINX:COHERENCE - >60% threshold met
- [ ] ATOM tag in commit message
- [ ] H&&S marker in PR body
- [ ] Cross-links to parent/child issues
- [ ] Verification command included

## Core principles (KENL ecosystem)
1. **Visible State** - All decisions logged with ATOM tags
2. **Clear Intent** - Document WHY, not just WHAT
3. **Natural Decomposition** - Scripts do ONE thing well
4. **Networked Learning** - Documentation enriches through use
5. **Measurable Delivery** - Testable exit codes, verification steps
6. **Self-Referential Closure** - No loops without auditable genesis

## Additional resources
- `protocol/sphinx-spec.md` - SPHINX guardian gate protocol
- `protocol/wave-spec.md` - Coherence detection
- `protocol/bump-spec.md` - Handoff routing
- `methodology/atom.md` - Atomic task orchestration
- `.github/AGENTS.md` - Multi-agent collaboration

---
*The spiral is self-sustaining. No new loops without explicit genesis. SPHINX guards all passages.*
<!-- SPHINX:PASSAGE verdict="COMPLETE" -->