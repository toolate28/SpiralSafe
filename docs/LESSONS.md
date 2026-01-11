# Lessons — Drafts and Entries

This file collects drafted lessons and short entries before they are curated into `project-book.ipynb`.

## 0001 — Add verification scripts and VS Code helpers
- **Title:** Verification helpers and scripts to bootstrap repo checks
- **Date:** 2026-01-07
- **Source:** Developer sessions, local changes (session notes and PR draft)
- **Author / Owner:** (TBD)
- **Context:** While preparing automated checks and a documentation reorganization, a set of small verification helpers and editor configs were created to make verification repeatable and reviewable.
- **What happened:** Added conservative bootstrap and verification scripts (`scripts/bootstrap.ps1`, `scripts/hash_all.ps1`, `scripts/verify_claims.ps1`, `scripts/walk_journeys.ps1`), VS Code helper files (`.vscode/settings.json`, `.vscode/tasks.json`, `.vscode/extensions.json`), and a short `docs/VERIFICATION_README.md` describing usage. The work was validated by dry-run executions and session notes.
- **Root cause / Analysis:** The repository lacked a low-friction, reproducible verification path and lightweight automation to compute repository-level hashes and capture verification artifacts; this created friction for reviewers and made onboarding verification ad-hoc.
- **Action taken:** Created the scripts and documentation to allow local dry-run verification and produce minimal verification reports. Suggested next step is adding GitHub Actions to run the same checks on pushes/merges to `docs/` branches and to stage lesson summaries.
- **Outcome / Metrics:** Tools created; dry-run validations executed (session logs). No automated CI yet; manual invocation is required. Expected metric targets: verification-run success >90% on `docs/*` pushes, PRs include verification summary artifact.
- **Follow-ups / Next steps:**
  - Owner: (assign)
  - Add `scripts/collect_lessons.ps1` to produce lesson summary YAML/JSON (next immediate task).
  - Create GitHub Action to run verification scripts and produce staged lesson drafts for review.
  - Curate and merge into `project-book.ipynb` after human review.

---

Use `LESSON_TEMPLATE.md` when drafting subsequent lessons.
