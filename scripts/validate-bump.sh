#!/usr/bin/env bash
set -euo pipefail

BUMP_FILE="bump.md"
REQUIRED_SECTIONS=("CURRENT STATE" "MISSION" "PERMISSION RULES" "STEPS" "VERIFICATION" "SUCCESS CRITERIA" "LOGGING / AUDIT")

if [ ! -f "$BUMP_FILE" ]; then
  echo "ERROR: $BUMP_FILE not found."
  exit 1
fi

# Read content for later checks (used in line 32)
_content_check="$(tr '[:upper:]' '[:lower:]' < "$BUMP_FILE")"

missing=()
for sec in "${REQUIRED_SECTIONS[@]}"; do
  lowsec="$(echo "$sec" | tr '[:upper:]' '[:lower:]')"
  if ! grep -qi "$lowsec" "$BUMP_FILE"; then
    missing+=("$sec")
  fi
done

if [ ${#missing[@]} -ne 0 ]; then
  echo "ERROR: bump.md is missing required sections:"
  for m in "${missing[@]}"; do
    echo " - $m"
  done
  echo "Please add them before merging."
  exit 2
fi

# Basic smoke check: make sure 'autoApprove' or 'AWI' text exists
if ! grep -qiE "auto-?approve|awi|permission rules" "$BUMP_FILE"; then
  echo "WARNING: bump.md does not appear to define permission/auto-approve rules (AWI)."
  # not fatal but advised
fi

echo "bump.md basic validation passed."
exit 0
