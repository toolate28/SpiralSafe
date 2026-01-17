# Archive Index

This directory contains documentation that is not directly referenced in the main README.md but may contain valuable historical context or working drafts.

## Structure

```
archive/
├── historical-docs/     # Completed work, historical context, narrative documents
├── releases/            # Version-specific release documentation
│   ├── v2.0.0/         # Release 2.0.0 documents
│   └── ops-1.0.1/      # Operations tooling release 1.0.1
└── ARCHIVE_INDEX.md     # This file
```

## Archiving Policy

Documents are archived when they:

1. Are release-specific (not latest) - moved to `archive/releases/{version}/`
2. Are historical or narrative in nature - moved to `archive/historical-docs/`
3. Contain outdated information or references to old filenames
4. Are superseded by newer, consolidated documentation
5. Serve as historical record but not active navigation
6. Are not system-critical or actively maintained

**System-critical documents remain in root**: README, LICENSE, SECURITY, CONTRIBUTING, ARCHITECTURE, CODEOWNERS, configuration files

## Active Documents (in root)

System-critical and actively maintained documents:

- `README.md` - Main entry point
- `LICENSE` - Legal requirement
- `SECURITY.md` - Security policy
- `CONTRIBUTING.md` - Contributor guide
- `ARCHITECTURE.md` - System overview
- `QUICK_START.md` - Getting started guide
- `docs/guides/TROUBLESHOOTING.md` - Active support documentation (moved 2026-01-08)
- `ops/DEPLOYMENT_GUIDE.md` - Active deployment instructions (moved 2026-01-08)
- `ops/DEPLOYMENT_CHECKLIST.md` - Deployment verification (moved 2026-01-08)

## Archived Documents

### Recent Additions (2026-01-08)

**Mission Artifacts:**

- `mission-accomplished-v3.0.0.txt` - Complete v3.0.0 quantum implementation milestone (originally `B&&P`)

**One-time Scripts:**

- `apply-docs-reorg-full_Version1.ps1` - Completed documentation reorganization script

### Release v2.0.0 (2026-01-07)

Moved to `archive/releases/v2.0.0/`:

- `RELEASE_NOTES_v2.0.0.md` - Release notes for v2.0.0
- `PR_SUMMARY_v2.0.0.md` - Pull request summary
- `IMPLEMENTATION_COMPLETE.md` - Implementation completion status
- `PRODUCTION_READY.md` - Production readiness report
- `VERIFICATION_STAMP.md` - Verification stamp for v2.0.0
- `SESSION_SUMMARY_20260104.md` - Session summary from January 4, 2026

### Historical Documentation (2026-01-07)

Moved to `archive/historical-docs/`:

- `THE_AINULINDALE_OF_HOPE_AND_SAUCE.md` - Creation story/narrative
- `THE_COMPLETION_SONG.md` - Completion narrative
- `THE_ONE_PATH.md` - Philosophical narrative
- `MAGNUM_OPUS.md` - Major work description
- `ULTRATHINK_SYNTHESIS.md` - Synthesis document
- `USER_ENLIGHTENMENT_PROTOCOL.md` - User enlightenment guide
- `KENL_ECOSYSTEM_TITLE_PAGE.md` - Ecosystem title page
- `PLATFORM_VISION_2026.md` - 2026 platform vision
- `PLATFORM_INTEGRATION_ROADMAP.md` - Integration roadmap
- `MULTI_FORK_STRATEGY.md` - Multi-fork strategy document
- `DOMAIN_PLAN.md` - Domain planning document
- `SAFE_SPIRAL_MASTER_INDEX.md` - Master index (superseded)
- `PUBLICATION_MANIFEST_v1.0.md` - v1.0 publication manifest
- `CREDITS.md` - Project credits
- `PR_DESCRIPTION.md` - Working PR description artifact

### Earlier Archives

| Document                                  | Archived Date | Reason                             | Notes                                                         |
| ----------------------------------------- | ------------- | ---------------------------------- | ------------------------------------------------------------- |
| `00_SAFE_SPIRAL_MASTER_START_HERE.md`     | 2026-01-02    | Superseded by README.md            | Historical "start here" guide                                 |
| `00_INVENTORY_AND_NAVIGATION_COMPLETE.md` | 2026-01-02    | Working draft                      | Pre-release navigation                                        |
| `01_THE_BRIDGE.md`                        | 2026-01-02    | Historical context                 | Bridge document, valuable context                             |
| `02_SAFE_SPIRAL_CONSOLIDATED.md`          | 2026-01-02    | Consolidated elsewhere             | Merged into master docs                                       |
| `KENL_ECOSYSTEM_MASTER_INDEX.md`          | 2026-01-02    | Alternative index                  | Similar to SAFE_SPIRAL_MASTER_INDEX.md                        |
| `PART_3_OBJECTIVE_ANALYSIS.md`            | 2026-01-02    | Has spiral-specific version        | Use docs/reports/analysis/PART_3_OBJECTIVE_ANALYSIS_SPIRAL.md |
| `PACKAGE_INVENTORY_COMPLETE.md`           | 2026-01-02    | Superseded by PUBLICATION_MANIFEST | Package inventory                                             |
| `ACKNOWLEDGEMENTS.md`                     | 2026-01-02    | Can be integrated elsewhere        | Credits and acknowledgements                                  |

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
