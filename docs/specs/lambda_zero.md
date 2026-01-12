---
status: draft
last_verified: 2026-01-12
atom_tags:
  - TODO: add ATOM tag after decision log
---

# lambda_zero Protocol (skeleton)

## Purpose
- Define a minimal execution/coordination unit that emits ATOM decisions and MCP logs for every transition.
- Keep it provider-neutral and offline-friendly.

## State Model (proposed)
- Inputs: task descriptor (bump.md), optional patterns/knowledge refs, auth token.
- Outputs: artifacts, ATOM tag(s), MCP log entries, gate transition results.
- Phases: `prepare` → `execute` → `verify` → `publish`.

## Interfaces
- CLI entrypoint (TBD) should accept:
  - `--task-file` (bump.md or equivalent)
  - `--atom-tag` (required) or `--atom-type/desc` to mint via atom-track
  - `--mcp-log` flag to enforce logging
- Emits: JSON report to stdout + log append via `mcp-logger.sh` and ATOM trail.

## Hooks
- Before execution: run `gate_intention_to_execution`.
- After execution: run `gate_execution_to_learning` and ensure MCP log presence.
- Failure: log to `.claude/logs/antiwave.jsonl` with error and atom_tag.

## Open Items
- Concrete CLI location (scripts/lambda-zero.sh?)
- Minimal schema for outputs (artifact manifest, decision refs)
- Alignment with ATOM-AUTH (token required for networked operations)
