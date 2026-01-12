---
status: draft
last_verified: 2026-01-12
atom_tags:
  - TODO: add ATOM tag after decision log
---

# Pipeline: Theoretical Papers → Discord (templates/methods)

## Goal
- Deliver sanitized, templated excerpts to Discord for collaboration without leaking sensitive data.

## Steps (proposed)
1) Source: `docs/theory/` (or specified path). Ensure state markers are present.
2) Transform: apply wave-toolkit template (TBD) to produce concise, transferrable methodology.
3) Redact: run `scripts/redact-log.sh` or similar filter for secrets and PII.
4) Log: create ATOM (DOC/SHARE) and append MCP log entry if any MCP tools used.
5) Publish: send via Discord webhook/bot using token from env (not committed).

## Implementation Stub
- Script: `scripts/publish/papers-to-discord.sh`
  - Checks required env: `DISCORD_WEBHOOK_URL` (or bot token) and `ATOM_AUTH_TOKEN` (if enforced).
  - Accepts: `--source <path>`, `--atom-tag <tag>`, optional `--dry-run`.
  - Logs: call `mcp_log tool=discord-publish status=success/fail` with redacted params.

## Safety
- Do not post full papers; post templates/abstracts only.
- Keep webhook URL in secrets; never in repo.
- Validate doc state markers before send.

## Open Items
- Finalize wave-toolkit transform step.
- Add automated test to confirm redaction and state markers prior to publish.
