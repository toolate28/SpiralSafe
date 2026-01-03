# Archive Index

This directory contains documentation that is not directly referenced in the main README.md but may contain valuable historical context or working drafts.

## Structure

```
archive/
├── historical-docs/     # Completed work, historical context
├── working-drafts/      # Work in progress, pre-release content
└── ARCHIVE_INDEX.md     # This file
```

## Archiving Policy

Documents are archived when they:
1. Are not directly referenced in README.md
2. Contain outdated information or references to old filenames
3. Are superseded by newer, consolidated documentation
4. Serve as historical record but not active navigation

## Active Documents (in root)

Per README.md, these documents are actively maintained:
- `README.md` - Main entry point
- `THE_AINULINDALE_OF_HOPE_AND_SAUCE.md` - Creation story
- `SAFE_SPIRAL_MASTER_INDEX.md` - Complete navigation
- `KENL_ECOSYSTEM_TITLE_PAGE.md` - Title page
- `docs/reports/verification/SYSTEM_VERIFICATION_REPORT.md` - Production testing
- `PUBLICATION_MANIFEST_v1.0.md` - Complete catalog
- `docs/reports/analysis/PART_3_OBJECTIVE_ANALYSIS_SPIRAL.md` - Analysis

## Archived Documents

### Historical Documentation

| Document | Archived Date | Reason | Notes |
|----------|---------------|--------|-------|
| `00_SAFE_SPIRAL_MASTER_START_HERE.md` | 2026-01-02 | Superseded by README.md | Historical "start here" guide |
| `00_INVENTORY_AND_NAVIGATION_COMPLETE.md` | 2026-01-02 | Working draft | Pre-release navigation |
| `01_THE_BRIDGE.md` | 2026-01-02 | Historical context | Bridge document, valuable context |
| `02_SAFE_SPIRAL_CONSOLIDATED.md` | 2026-01-02 | Consolidated elsewhere | Merged into master docs |
| `KENL_ECOSYSTEM_MASTER_INDEX.md` | 2026-01-02 | Alternative index | Similar to SAFE_SPIRAL_MASTER_INDEX.md |
| `PART_3_OBJECTIVE_ANALYSIS.md` | 2026-01-02 | Has spiral-specific version | Use docs/reports/analysis/PART_3_OBJECTIVE_ANALYSIS_SPIRAL.md |
| `PACKAGE_INVENTORY_COMPLETE.md` | 2026-01-02 | Superseded by PUBLICATION_MANIFEST | Package inventory |
| `ACKNOWLEDGEMENTS.md` | 2026-01-02 | Can be integrated elsewhere | Credits and acknowledgements |

## Restoration

To restore an archived document:
```bash
# Move back to root
mv archive/historical-docs/FILENAME.md ./

# Update README.md if needed
# Add ATOM tag for the restoration decision
./scripts/atom-track.sh DOC "Restored FILENAME from archive" "FILENAME.md"
```

## ATOM Tracking

All archiving decisions are logged with ATOM tags:
- Type: `DOC` or `ARCHIVE`
- Decision files in: `.atom-trail/decisions/`

---

**ATOM:** ATOM-DOC-20260102-004-archive-index-creation
**Last Updated:** 2026-01-02
**Maintained by:** Repository maintainers
