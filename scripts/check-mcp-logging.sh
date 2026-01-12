#!/usr/bin/env bash
# Validate MCP log formatting (optional pass-through if absent)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_FILE="$REPO_ROOT/.claude/logs/mcp.jsonl"

if [ ! -f "$LOG_FILE" ]; then
  echo "INFO: no MCP log file present; skipping validation"
  exit 0
fi

python3 - "$LOG_FILE" <<'PY'
import json, sys
log_file = sys.argv[1]
required = {"timestamp", "tool", "atom_tag", "status"}
with open(log_file, "r", encoding="utf-8") as fh:
    for idx, line in enumerate(fh, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception as exc:  # pylint: disable=broad-except
            raise SystemExit(f"Invalid JSON at line {idx}: {exc}")
        missing = required - obj.keys()
        if missing:
            raise SystemExit(f"Missing fields {missing} at line {idx}")
print("OK: MCP log format valid")
PY

exit 0