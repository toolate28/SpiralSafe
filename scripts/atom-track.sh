#!/usr/bin/env bash
# Enhanced ATOM tracking with counters and freshness
# Usage: scripts/atom-track.sh TYPE "description" [FILE_OR_ISSUE]
set -euo pipefail

TYPE="${1:-}"
DESC="${2:-}"
FILE_OR_ISSUE="${3:-}"

if [ -z "$TYPE" ] || [ -z "$DESC" ]; then
  echo "Usage: $0 TYPE \"description\" [FILE_OR_ISSUE]"
  echo "Examples:"
  echo "  $0 DECISION \"Added CI workflow\" .github/workflows/ci.yml"
  echo "  $0 DOC \"Updated README\" issue-#42"
  echo "  $0 FEATURE \"New feature\" #123"
  echo "  $0 FIX \"Bug fix\" GH-456"
  exit 1
fi

DATE="$(date +%Y%m%d)"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
PREFIX="ATOM-${TYPE}-${DATE}-"

# Pattern for detecting issue references
# Matches: issue-#123, #123, issue-123, GH-123
ISSUE_PATTERN="^(issue-#|#|issue-|GH-)[0-9]+$"

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

# Detect if third parameter is an issue reference or file path
ISSUE=""
FILE=""
if [ -n "$FILE_OR_ISSUE" ]; then
  if [[ "$FILE_OR_ISSUE" =~ $ISSUE_PATTERN ]]; then
    ISSUE="$FILE_OR_ISSUE"
  elif [ "$FILE_OR_ISSUE" != "none" ]; then
    FILE="$FILE_OR_ISSUE"
  fi
  # If FILE_OR_ISSUE is "none", both ISSUE and FILE remain empty
fi

# Common metadata for JSON output
CREATED_EPOCH="$(date +%s)"

# Create decision entry with freshness tracking
DECISION_FILE=".atom-trail/decisions/${ATOM_TAG}.json"
if [ -n "$ISSUE" ]; then
  # Issue reference format
  cat > "$DECISION_FILE" <<EOF
{
  "atom_tag": "${ATOM_TAG}",
  "type": "${TYPE}",
  "description": "${DESC}",
  "timestamp": "${TIMESTAMP}",
  "issue": "${ISSUE}",
  "freshness_level": "fresh",
  "bedrock_eligible": false,
  "created_epoch": ${CREATED_EPOCH}
}
EOF
  # Log to JSONL for easy parsing
  echo "{\"atom_tag\":\"${ATOM_TAG}\",\"type\":\"${TYPE}\",\"description\":\"${DESC}\",\"timestamp\":\"${TIMESTAMP}\",\"issue\":\"${ISSUE}\"}" >> .claude/logs/atom-trail.jsonl
else
  # File path or no reference format
  if [ -n "$FILE" ]; then
    # Has a file path
    cat > "$DECISION_FILE" <<EOF
{
  "atom_tag": "${ATOM_TAG}",
  "type": "${TYPE}",
  "description": "${DESC}",
  "timestamp": "${TIMESTAMP}",
  "file": "${FILE}",
  "freshness_level": "fresh",
  "bedrock_eligible": false,
  "created_epoch": ${CREATED_EPOCH}
}
EOF
    # Log to JSONL for easy parsing
    echo "{\"atom_tag\":\"${ATOM_TAG}\",\"type\":\"${TYPE}\",\"description\":\"${DESC}\",\"timestamp\":\"${TIMESTAMP}\",\"file\":\"${FILE}\"}" >> .claude/logs/atom-trail.jsonl
  else
    # No file or issue reference (omit the field entirely for cleaner JSON)
    cat > "$DECISION_FILE" <<EOF
{
  "atom_tag": "${ATOM_TAG}",
  "type": "${TYPE}",
  "description": "${DESC}",
  "timestamp": "${TIMESTAMP}",
  "freshness_level": "fresh",
  "bedrock_eligible": false,
  "created_epoch": ${CREATED_EPOCH}
}
EOF
    # Log to JSONL for easy parsing
    echo "{\"atom_tag\":\"${ATOM_TAG}\",\"type\":\"${TYPE}\",\"description\":\"${DESC}\",\"timestamp\":\"${TIMESTAMP}\"}" >> .claude/logs/atom-trail.jsonl
  fi
fi

echo "${ATOM_TAG}"
exit 0
