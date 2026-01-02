#!/usr/bin/env bash
set -euo pipefail

# Usage: scripts/atom-tag.sh TYPE "short description"
# Example: scripts/atom-tag.sh TASK "baseline tests passed"

TYPE="${1:-}"
DESC="${2:-}"

if [ -z "$TYPE" ] || [ -z "$DESC" ]; then
  echo "Usage: $0 TYPE \"short description\""
  exit 1
fi

DATE="$(date +%Y%m%d)"
PREFIX="ATOM-${TYPE}-${DATE}-"

# Find existing tags in git history or files that match today's prefix and extract highest sequence
# fallback to scanning repository files for occurrences
grep -RohE "ATOM-${TYPE}-${DATE}-[0-9]{3}" . || true
LAST_NUM=0
# try in git log
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  nums=$(git grep -hE "ATOM-${TYPE}-${DATE}-[0-9]{3}" || true | grep -oE "[0-9]{3}" || true)
  if [ -n "$nums" ]; then
    for n in $nums; do
      (( n10 = 10#$n ))
      if [ "$n10" -gt "$LAST_NUM" ]; then
        LAST_NUM="$n10"
      fi
    done
  fi
fi

NEXT_NUM=$(printf "%03d" $((LAST_NUM + 1)))
TAG="${PREFIX}${NEXT_NUM}"

# Make descriptive slug sanitized
SLUG=$(echo "$DESC" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-+|-+$//g' | cut -c1-60)

ATOM_TAG="${TAG}-${SLUG}"

# Optionally write to .claude/last_atom (create folder)
mkdir -p .claude
echo "${ATOM_TAG}" > .claude/last_atom
echo "${ATOM_TAG}"
# Caller may choose to commit / use this tag in a commit message
exit 0
