---
status: draft
last_verified: 2026-01-12
atom_tags:
  - TODO: add ATOM tag after decision log
---

# ATOM-AUTH Minimal Contract

## Purpose
- Provide scoped, auditable authentication for tools, MCP servers, and automation.
- Ensure every sensitive action ties back to an ATOM decision and a verifiable token.

## Token Shape (proposed)
- Format: signed JWT or opaque token with server-side lookup.
- Claims: `sub`, `scopes` (e.g., `read:mcp`, `write:logs`, `publish:papers`), `iat`, `exp`, `atom_tag`, `client_id`.
- Transport: env vars or headers; never committed. Document required var names in `.env.example`.

## Issuance & Rotation
- Issuer signs tokens; rotation interval: short-lived (hours). Refresh requires ATOM log entry.
- Audit: every issuance writes to `.claude/logs/auth.jsonl` with `atom_tag` and scope set.

## Validation Hook (for scripts)
- Scripts should call a small validator before sensitive actions:
  - Check `ATOM_AUTH_TOKEN` present.
  - Verify signature (local key or verifier endpoint).
  - Enforce scope per action.
  - Emit MCP log entry if the action uses MCP servers.

## Failure Modes
- Missing/expired/invalid token → fail fast with guidance.
- Scope mismatch → refuse action; log attempt (no secrets).

## Integrations
- GitHub Actions: use repo/environment secrets; inject token per job; limit scope.
- IDE/browser/Minecraft bridges: read token from user-local secure store; never hardcode.
- MCP servers: require token for any networked call; log via `mcp-logger.sh`.

## Open Items
- Select signing mechanism (local key vs. provider KMS).
- Define scope registry and mapping to repo actions.
- Add automated tests in `scripts/test-integration.sh` once validator exists.
