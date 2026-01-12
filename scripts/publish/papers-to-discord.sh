#!/usr/bin/env bash
# Stub: prepare and (optionally) send templated papers to Discord
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

source "$REPO_ROOT/scripts/lib/mcp-logger.sh"

usage() {
  cat <<'EOF'
Usage: papers-to-discord.sh --source <path> --atom-tag <ATOM-...> [--dry-run]

Environment:
  DISCORD_WEBHOOK_URL   Required for real sends (omit in dry-run)
  ATOM_AUTH_TOKEN       Optional auth if enforced upstream

Behavior:
  - Validates inputs only; sending is TODO.
  - Logs intent via mcp_log to .claude/logs/mcp.jsonl
EOF
}

SOURCE=""
ATOM_TAG=""
DRY_RUN=0

while [ $# -gt 0 ]; do
  case "$1" in
    --source)
      SOURCE="${2:-}"
      shift 2
      ;;
    --atom-tag)
      ATOM_TAG="${2:-}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift 1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

[ -n "$SOURCE" ] || { echo "--source is required" >&2; usage; exit 1; }
[ -n "$ATOM_TAG" ] || { echo "--atom-tag is required" >&2; usage; exit 1; }

if [ ! -e "$SOURCE" ]; then
  echo "ERROR: source path not found: $SOURCE" >&2
  exit 1
fi

if [ "$DRY_RUN" -eq 0 ] && [ -z "${DISCORD_WEBHOOK_URL:-}" ]; then
  echo "ERROR: DISCORD_WEBHOOK_URL required for send; use --dry-run to skip" >&2
  exit 1
fi

STATUS="dry-run"
if [ "$DRY_RUN" -eq 0 ]; then
  STATUS="pending-send"
fi

mcp_log "papers-to-discord" "v0" "$ATOM_TAG" "source=$SOURCE" "status=$STATUS" "$STATUS"

echo "Stub complete: $STATUS (no send implemented). Logged to .claude/logs/mcp.jsonl"
exit 0