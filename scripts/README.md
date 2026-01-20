# scripts — small helpers

This folder contains small, safe scripts used during documentation verification, lesson collection, and repository setup.

## Repository Setup

### setup-github-labels.sh

Creates all required GitHub labels for Dependabot, issue templates, SYNAPSE framework, and SPHINX protocol testing.

**Usage:**

```bash
./scripts/setup-github-labels.sh [--dry-run] [--verbose]
```

**Options:**
- `--dry-run` - Show what would be created without making changes
- `--verbose` - Show detailed output for each label
- `--help` - Display help message

**Prerequisites:**
- GitHub CLI (`gh`) installed and authenticated
- Repository owner/admin permissions

**Example:**

```bash
# Preview changes
./scripts/setup-github-labels.sh --dry-run

# Apply changes
./scripts/setup-github-labels.sh
```

See [`docs/GITHUB_LABELS.md`](../docs/GITHUB_LABELS.md) for comprehensive documentation.

## Documentation Tools

### collect_lessons.ps1

- Scans `docs/LESSONS.md` and writes `docs/staging/lessons_summary.json` and `docs/staging/lessons_summary.md`.
- Usage:

```powershell
pwsh .\scripts\collect_lessons.ps1
```

Notes:

- The script performs simple markdown parsing — it looks for sections separated by `---` and keys like `- **Title:**` and `- **Date:**`.
- The staging output is intended for automatic workflows or human review before curating into `project-book.ipynb`.
