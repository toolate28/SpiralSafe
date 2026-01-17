# scripts — small helpers

This folder contains small, safe scripts used during documentation verification and lesson collection.

collect_lessons.ps1

- Scans `docs/LESSONS.md` and writes `docs/staging/lessons_summary.json` and `docs/staging/lessons_summary.md`.
- Usage:

```powershell
pwsh .\scripts\collect_lessons.ps1
```

Notes:

- The script performs simple markdown parsing — it looks for sections separated by `---` and keys like `- **Title:**` and `- **Date:**`.
- The staging output is intended for automatic workflows or human review before curating into `project-book.ipynb`.
