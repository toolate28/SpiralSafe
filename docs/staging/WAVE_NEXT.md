# Wave payload for next contributor

Purpose: produce a single, reviewable PR payload containing the documentation reorg, verification helpers, and lesson artifacts so the next contributor can open one consolidated PR.

Contents included in this wave:

- `docs/LESSON_TEMPLATE.md`
- `docs/LESSONS.md`
- `docs/staging/lessons_summary.*`
- `.github/workflows/collect-lessons.yml`
- `scripts/collect_lessons.ps1`
- `scripts/*verification*.ps1` (if present)

How to use:

1. Download and extract the payload (zip).
2. Create a new branch from `main` or your working branch.
3. Copy the files into the repository root (preserving paths) and commit.
4. Push the branch and open a single PR titled: "Docs: consolidate root docs + verification helpers (wave)".
5. Attach the `docs/staging/lessons_summary.md` to the PR or rely on the workflow which will generate it.

Notes:

- This wave is intentionally minimal and safe: scripts are dry-run friendly and `collect_lessons.ps1` only reads markdown and writes staging outputs.
- If you want the workflow to also run verification scripts before collection, update the workflow or run them locally and include generated artifacts in the payload.
