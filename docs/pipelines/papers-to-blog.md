---
status: draft
last_verified: 2026-01-12
atom_tags:
  - TODO: add ATOM tag after decision log
---

# Pipeline: Theoretical Papers → Blog

## Goal

- Publish blog-friendly adaptations of theoretical work on the site with ATOM lineage and state markers.

## Steps (proposed)

1. Source: select paper; ensure state markers are current.
2. Adapt: produce blog draft (summary, key insights, diagrams) while keeping references to the source ATOM tags.
3. Assets: place images/diagrams in `media/` with README (source, license, atom tag).
4. Log: ATOM (DOC/POST) and MCP log entry if tooling used (e.g., converters/renderers).
5. Deploy: integrate into site/blog pipeline (TBD); ensure preview and review steps.

## Implementation Hooks

- Script placeholder (TBD): `scripts/publish/papers-to-blog.sh` for packaging assets into the site’s expected structure.
- Works offline; no secrets needed unless deploying.

## Safety

- Keep state markers on blog content; include last_verified.
- Avoid embedding large binaries; link to optimized media.
- Validate links with `scripts/validate-links.sh` before publish.

## Open Items

- Exact blog generator/tooling path.
- Review/approval workflow before publishing.
