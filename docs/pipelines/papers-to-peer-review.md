---
status: draft
last_verified: 2026-01-12
atom_tags:
  - TODO: add ATOM tag after decision log
---

# Pipeline: Theoretical Papers → Peer-Review Sites

## Goal
- Package and submit unique work to peer-review venues with traceable provenance.

## Steps (proposed)
1) Source: canonical paper in `docs/theory/` with state markers.
2) Package: generate PDF and metadata (authors, abstract, keywords, ATOM tags, last_verified).
3) Provenance bundle: include ATOM trail refs and hash manifest of submitted files.
4) Log: ATOM (DOC/PUBLISH) and MCP log entry summarizing venue, version, hash.
5) Submit: manual or automated upload; store submission receipt in `archive/artifacts/` with state marker.

## Implementation Hooks
- Script placeholder (TBD): `scripts/publish/papers-to-peer-review.sh` for packaging and manifest creation (not submission credentials).
- Env vars for credentials go in `.env.example` placeholders; never committed.

## Safety
- Redact any secrets prior to packaging.
- Verify state markers and last_verified date before submission.
- Keep submission receipts under version control if allowed (or hashed reference).

## Open Items
- Target venue list and required metadata formats.
- Hashing/manifest format (e.g., SHA256 manifest file).
