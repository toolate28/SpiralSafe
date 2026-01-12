#!/usr/bin/env bash
# Purpose: append auditable MCP invocation logs with ATOM linkage
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$REPO_ROOT/.claude/logs"
LOG_FILE="$LOG_DIR/mcp.jsonl"

_require() {
  if [ -z "${1:-}" ]; then
    echo "ERROR: $2 is required" >&2
    exit 1
  fi
}

_ensure_log_dir() {
  mkdir -p "$LOG_DIR"
}

# mcp_log TOOL VERSION ATOM_TAG PARAMS_REDACTED RESPONSE_SUMMARY STATUS
# PARAMS_REDACTED and RESPONSE_SUMMARY should be short, redacted strings.
mcp_log() {
  local tool="${1:-}" version="${2:-}" atom_tag="${3:-}" params_redacted="${4:-}" response_summary="${5:-}" status="${6:-}"

  _require "$tool" "tool"
  _require "$atom_tag" "atom_tag"
  _require "$status" "status"

  if [[ ! "$atom_tag" =~ ^ATOM-[A-Z]+-[0-9]{8}-[0-9]{3} ]]; then
    echo "WARN: atom_tag '$atom_tag' does not match expected pattern; logging anyway" >&2
  fi

  _ensure_log_dir

  MCP_TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  MCP_TOOL="$tool" \
  MCP_VERSION="$version" \
  MCP_ATOM="$atom_tag" \
  MCP_PARAMS="$params_redacted" \
  MCP_RESP="$response_summary" \
  MCP_STATUS="$status" \
  LOG_FILE="$LOG_FILE" python3 - "$LOG_FILE" <<'PY'
import json, os, sys
log_file = os.environ["LOG_FILE"]
payload = {
    "timestamp": os.environ["MCP_TS"],
    "tool": os.environ["MCP_TOOL"],
    "version": os.environ.get("MCP_VERSION", ""),
    "atom_tag": os.environ["MCP_ATOM"],
    "params_redacted": os.environ.get("MCP_PARAMS", ""),
    "response_summary": os.environ.get("MCP_RESP", ""),
    "status": os.environ["MCP_STATUS"],
}
with open(log_file, "a", encoding="utf-8") as fh:
    fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
PY
}