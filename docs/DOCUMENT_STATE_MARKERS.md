---
status: active
coherence_phase: intention
last_verified: 2026-01-03
verification_method: manual
atom_tags:
  - ATOM-COHERENCE-20260103-001-unified-deployment
intent: "Document the document state markers system for SpiralSafe coherence"
---

# Document State Markers

## Overview

Document state markers are YAML frontmatter blocks that provide metadata about the lifecycle, coherence phase, and verification status of every documentation artifact in SpiralSafe. They make it possible to distinguish active documentation from aspirational, historical, or archived content.

## Problem Solved

**Anti-Wave Pattern**: Documentation Archaeology

- Without state markers, users can't tell if a document is current guidance or historical record
- Aspirational designs look identical to production reality
- Stale documentation creates confusion and wasted effort

**Solution**: Every document carries explicit state metadata

## Required Fields

All markdown documents must include:

### status

**Values**: `active | aspirational | historical | archived`

- **active**: Current, authoritative documentation
- **aspirational**: Planned/proposed features not yet implemented
- **historical**: Past designs/decisions kept for reference
- **archived**: Deprecated, moved to archive directory

### coherence_phase

**Values**: `understanding | knowledge | intention | execution | learning`

Indicates which phase of the coherence cycle this document supports:

- **understanding**: wave.md excavation, problem analysis
- **knowledge**: KENL patterns, knowledge relay
- **intention**: AWI rules, bump.md templates
- **execution**: ATOM implementation guides
- **learning**: SAIF reports, retrospectives

### last_verified

**Format**: `YYYY-MM-DD`

Date when the document was last verified as accurate.

### atom_tags

**Format**: Array of ATOM tags

Links document to specific ATOM decisions:

```yaml
atom_tags:
  - ATOM-DOC-20260103-001-document-created
  - ATOM-UPDATE-20260104-002-content-refreshed
```

## Optional Fields

### last_verified_by

ATOM tag or identifier of who/what verified the document.

### verification_method

**Values**: `automated | manual | survey`

How the document was verified.

### intent

One-sentence explanation of why this document exists.

### dependencies

Documents this one references or is referenced by:

```yaml
dependencies:
  - document: VERIFICATION_GATES.md
    relationship: implements
  - document: ATOM_LIFECYCLE_HOOKS.md
    relationship: informs
```

**Relationship types**: `informs | implements | validates | supersedes`

### verification_checklist

Optional checklist for document verification:

```yaml
verification_checklist:
  - all_examples_tested: pending
  - links_valid: pending
  - screenshots_current: pending
```

## Example

```yaml
---
status: active
coherence_phase: execution
last_verified: 2026-01-03
last_verified_by: ATOM-COHERENCE-20260103-001
verification_method: manual
atom_tags:
  - ATOM-DOC-20260103-001-verification-gates

intent: "Document the verification gate protocol for SpiralSafe coherence"

dependencies:
  - document: ATOM_LIFECYCLE_HOOKS.md
    relationship: informs

verification_checklist:
  - all_code_examples_tested: complete
  - usage_patterns_documented: complete
---
# Document Title

Content begins here...
```

## Validation

Use the validation script to check all documents:

```bash
./scripts/validate-document-state.sh
```

This script:

- Finds all markdown files (excluding node_modules, archive)
- Checks for YAML frontmatter
- Validates required fields are present
- Verifies status is a valid value
- Reports missing or invalid markers

## Template

Use the template for new documents:

```bash
cp docs/templates/DOCUMENT_STATE_MARKER.md docs/NEW_DOCUMENT.md
# Edit NEW_DOCUMENT.md and fill in all fields
```

## CI Integration

The `coherence-gates.yml` workflow automatically validates document state markers on every push/PR:

```yaml
- name: Validate document state markers
  run: |
    chmod +x scripts/validate-document-state.sh
    ./scripts/validate-document-state.sh
```

## Migration Guide

To add state markers to existing documents:

1. Add YAML frontmatter at the top of the file
2. Set `status` based on current usage
3. Identify appropriate `coherence_phase`
4. Set `last_verified` to today's date
5. Link relevant `atom_tags`
6. Run validation: `./scripts/validate-document-state.sh`

## Best Practices

1. **Always add markers**: New documents must include state markers
2. **Update last_verified**: Refresh when content changes significantly
3. **Track dependencies**: Link related documents
4. **Use aspirational status**: Clearly mark future plans
5. **Archive old docs**: Move deprecated docs to archive/ with archived status
6. **Verify regularly**: Run validation script periodically

## Anti-Patterns to Avoid

❌ **Don't**: Leave documents without state markers  
✅ **Do**: Add markers to every markdown file

❌ **Don't**: Set everything to "active"  
✅ **Do**: Use appropriate status for each document's reality

❌ **Don't**: Let last_verified date get stale  
✅ **Do**: Update when reviewing or modifying content

❌ **Don't**: Ignore validation failures  
✅ **Do**: Fix marker issues immediately

## Relationship to ATOM Trail

Document state markers complement the ATOM trail by:

- Linking documentation to decisions via atom_tags
- Tracking when documentation was verified
- Showing which coherence phase each document serves
- Making documentation lifecycle explicit and auditable
