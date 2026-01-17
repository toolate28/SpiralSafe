#!/usr/bin/env bash
set -euo pipefail

# Usage: scripts/validate-branch-name.sh <branch-name>
BRANCH="${1:-}"

if [ -z "$BRANCH" ]; then
  # try to detect
  if git rev-parse --abbrev-ref HEAD >/dev/null 2>&1; then
    BRANCH="$(git rev-parse --abbrev-ref HEAD)"
  fi
fi

if [ -z "$BRANCH" ]; then
  echo "ERROR: Branch name not provided and could not be detected."
  exit 1
fi

# Allowed patterns:
# - New canonical: {type}/ATOM-{TYPE}-YYYYMMDD-NNN-{slug}
# - Legacy agent branches: claude/* or copilot/*
RE='^(feat|fix|docs|chore|refactor|test|ci|perf|build|revert)\/ATOM-[A-Z]+-[0-9]{8}-[0-9]{3}-[a-z0-9-]+$'
if [[ "$BRANCH" =~ ^claude\/.* ]] || [[ "$BRANCH" =~ ^copilot\/.* ]]; then
  echo "OK: Legacy agent branch allowed (grandfathered): $BRANCH"
  exit 0
fi

if [[ "$BRANCH" =~ $RE ]]; then
  echo "OK: Branch name matches canonical format: $BRANCH"
  exit 0
fi

echo "ERROR: Invalid branch name: $BRANCH"
echo "Expected formats:"
echo " - claude/* or copilot/* (agent branches, grandfathered)"
echo " - {type}/ATOM-{TYPE}-YYYYMMDD-NNN-{slug}"
echo "   e.g. feat/ATOM-FEAT-20251116-010-live-dashboard"
exit 2
