# Negative-Space Analysis — SpiralSafe

Prepared: TODO — add date and owner

Purpose
- Identify unused, duplicated, or noisy areas in the repository (negative space).
- Provide short, actionable recommendations to improve discoverability, reduce cognitive load, and prepare the repo for ongoing operations.

Executive summary
- The repository root contains many large Markdown files. This creates noise and duplication of concepts (architecture, implementation notes, roadmaps, manifests).
- Consolidating long-form docs into docs/ reduces root clutter and improves discoverability.
- Some workflows and scripts may reference absolute paths in root — these must be checked and updated.
- There are many thematic documents that overlap (ARCHITECTURE.md, IMPLEMENTATION_COMPLETE.md, SAFE_SPIRAL_MASTER_INDEX.md). A dedupe/merge pass is recommended.

Findings
1. Root doc proliferation
   - Numerous large top-level markdown files make the repo entry point noisy and harder to scan.
   - Action: Consolidate into docs/ with categorized subfolders (done in this reorg).

2. Potential CI / workflow breakage
   - .github/workflows or other automation may reference moved files by path.
   - Action: Scan all workflow files and scripts for paths; update or maintain pointer files.

3. Duplicate or overlapping content
   - Architecture + implementation + master index likely contain overlapping sections.
   - Action: Run content-dedup pass and produce canonical sources (single source of truth per subject).

4. Orphaned scripts and env-config expectations
   - Bootstrap reported missing env-config, templates, frameworks directory entries.
   - Action: Identify owners or provide stubs or instructions for initializing missing pieces.

5. Binary assets
   - Binary/zip (spiral_safe_bump_ci_payload.zip) should be tracked with Git LFS or moved to release assets.
   - Action: Track with LFS or upload to GitHub Releases and reference from docs.

Prioritized recommendations (short-term)
- [P1] Run link-check across docs/ and update internal links (markdown-link-check).
- [P1] Scan .github/workflows and scripts for references to moved docs; update paths where necessary.
- [P2] Merge or canonicalize overlapping design docs: produce a single ARCHITECTURE + IMPLEMENTATION snapshot with clear ADR links.
- [P2] Add small README.md files in each docs/ subfolder explaining scope and owner.
- [P3] Move large binaries to LFS or Releases and document storage policy in docs/ops.

Operational artifacts to add (this PR or follow-up)
- docs/ops/SIGNOFF_CHECKLIST.md — pre-merge checklist (included in this PR)
- docs/DECISIONS.md — ADR starter for Day Zero decisions and architecture records
- docs/ops/OWNERS.md — list of maintainers for docs sections

Verification & metrics
- After merge run:
  - markdown-link-check "docs/**/*.md"
  - pre-commit run --all-files
  - GitHub Actions CI run on main and PRs
- Track regressions in repo entry noise (weekly review), and measure number of root-level markdown files (goal: < 8 root docs).

Owners
- Proposed owner: docs-maintainers@spiralsafe.local  (please replace with actual GitHub teams or handles)

Sign-off
- Prepared by: toolate28 (H&&S)
- Reviewed by: ____________________
- Date:
