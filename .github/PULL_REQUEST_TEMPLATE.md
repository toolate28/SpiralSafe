<!--
SPIRALSAFE PR TEMPLATE
-------------------------------------------------------------------------
Before submitting, please review:
1. .github/copilot-instructions.md (Protocol & Agents)
2. GIT_INSIGHTS_ANALYSIS.md (Anti-patterns to avoid)
-->

## 📝 ATOM Identity
<!-- Format: ATOM-TYPE-YYYYMMDD-NNN-description -->
<!-- Types: INIT, FEATURE, FIX, DOC, REFACTOR, TEST, DECISION, RELEASE, TASK -->
**ATOM Tag:** `ATOM-TYPE-YYYYMMDD-NNN-desc`

## 🎯 Purpose & Context
<!-- Link to related Linear issue, GitHub issue, or parent ATOM tag -->
- **Why is this change necessary?**
- **What component/layer does it affect?** (Protocol, Interface, Methodology)

## 📡 Handoff & Synchronization (H&&S)
<!-- MANDATORY: Select at least one or describe rationale -->
- [ ] **H&&S:WAVE** (Project-wide coherence check or architecture change)
- [ ] **H&&S:PASS** (Ownership transfer)
- [ ] **H&&S:SYNC** (Synchronization/Docs update)
- [ ] **H&&S:BLOCK** (Identified blocker)
- [ ] **None** (Trivial fix/chore)

**Rationale for H&&S:**
<!-- If WAVE is selected, explain the architectural implication or semantic conflict resolution -->

## 🛠️ Changes
- [ ] Code Changes
- [ ] Documentation Updates (`.context.yaml` or dual-format docs)
- [ ] Infrastructure/CI

## 🛡️ Anti-Pattern Check (Critical)
<!-- Based on GIT_INSIGHTS_ANALYSIS.md -->
- [ ] **No "Initial plan" commits:** I have squashed or removed any Copilot planning stubs.
- [ ] **No Desktop Paths:** I have ensured no local paths (e.g., `C:\Users\...`) are hardcoded.
- [ ] **Conventional Commits:** My commit messages follow `feat(scope): desc` or `fix(scope): desc`.
- [ ] **Single Agent Focus:** If AI-generated, this was primarily driven by ONE agent (Claude for Arch, Copilot for Fixes).
- [ ] **Clean Branches:** I have deleted my old/stale experiment branches.

## ✅ Verification Checklist
<!-- Check relevant items. All CI checks must pass. -->
- [ ] I have run `npm run lint` and `npm run typecheck` locally.
- [ ] I have run `shellcheck` on modified `.sh` files.
- [ ] I have updated the Project Book / Docs if architecture changed.
- [ ] "Tomorrow Test": Can a new agent/dev understand this without extra context?

## 🔒 Security & Privacy
- [ ] No secrets, tokens, or keys added.
- [ ] No PII exposed.
- [ ] **MCP Bypass Check:** If adding MCP tools, I have verified auth handling.

---
*SpiralSafe — Seamless & Flawless Coherence*
