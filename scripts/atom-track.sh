#!/usr/bin/env bash
# Enhanced ATOM tracking with counters and freshness
# Usage: scripts/atom-track.sh TYPE "description" [FILE]
set -euo pipefail

TYPE="${1:-}"
DESC="${2:-}"
FILE="${3:-}"

if [ -z "$TYPE" ] || [ -z "$DESC" ]; then
  echo "Usage: $0 TYPE \"description\" [FILE]"
  echo "Example: $0 DECISION \"Added CI workflow\" .github/workflows/ci.yml"
  exit 1
fi

DATE="$(date +%Y%m%d)"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
PREFIX="ATOM-${TYPE}-${DATE}-"

# Create directories if they don't exist
mkdir -p .atom-trail/decisions
mkdir -p .atom-trail/counters
mkdir -p .claude/logs

# Get current counter for this type and date
COUNTER_FILE=".atom-trail/counters/${TYPE}-${DATE}.count"
if [ -f "$COUNTER_FILE" ]; then
  CURRENT_COUNT=$(cat "$COUNTER_FILE")
else
  CURRENT_COUNT=0
fi

# Increment counter
NEXT_COUNT=$((CURRENT_COUNT + 1))
echo "$NEXT_COUNT" > "$COUNTER_FILE"

# Format sequence number
SEQ=$(printf "%03d" "$NEXT_COUNT")
TAG="${PREFIX}${SEQ}"

# Create descriptive slug
SLUG=$(echo "$DESC" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-+|-+$//g' | cut -c1-60)
ATOM_TAG="${TAG}-${SLUG}"

# Store in last_atom for quick reference
echo "${ATOM_TAG}" > .claude/last_atom

# Create decision entry with freshness tracking
DECISION_FILE=".atom-trail/decisions/${ATOM_TAG}.json"
cat > "$DECISION_FILE" <<EOF
{
  "atom_tag": "${ATOM_TAG}",
  "type": "${TYPE}",
  "description": "${DESC}",
  "timestamp": "${TIMESTAMP}",
  "file": "${FILE:-none}",
  "freshness_level": "fresh",
  "bedrock_eligible": false,
  "created_epoch": $(date +%s)
}
EOF

# Log to JSONL for easy parsing
echo "{\"atom_tag\":\"${ATOM_TAG}\",\"type\":\"${TYPE}\",\"description\":\"${DESC}\",\"timestamp\":\"${TIMESTAMP}\",\"file\":\"${FILE:-none}\"}" >> .claude/logs/atom-trail.jsonl

echo "${ATOM_TAG}"
exit 0
