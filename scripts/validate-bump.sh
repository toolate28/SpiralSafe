#!/usr/bin/env bash
# Validate bump.md is properly filled (not template placeholders)
set -euo pipefail

BUMP_FILE="${1:-bump.md}"

if [ ! -f "$BUMP_FILE" ]; then
    echo "✗ bump.md not found"
    exit 1
fi

# Check required sections
REQUIRED_SECTIONS=("CURRENT STATE" "MISSION" "PERMISSION RULES" "STEPS" "VERIFICATION" "SUCCESS CRITERIA" "LOGGING / AUDIT")

missing=()
for sec in "${REQUIRED_SECTIONS[@]}"; do
  lowsec="$(echo "$sec" | tr '[:upper:]' '[:lower:]')"
  if ! grep -qi "$lowsec" "$BUMP_FILE"; then
    missing+=("$sec")
  fi
done

if [ ${#missing[@]} -ne 0 ]; then
  echo "✗ bump.md is missing required sections:"
  for m in "${missing[@]}"; do
    echo "    - $m"
  done
  echo "Please add them before merging."
  exit 2
fi

# Check for template placeholders
PLACEHOLDERS=(
    "YYYYMMDD"
    "<short:[^>]*>"
    "<architect name"
    "<owner/repo"
    "<branch name>"
    "<YYYY-MM-DD>"
    "<short summary"
    "<explicit question"
)

errors=()

for placeholder in "${PLACEHOLDERS[@]}"; do
    if grep -q "$placeholder" "$BUMP_FILE"; then
        errors+=("Contains unfilled placeholder: $placeholder")
    fi
done

if [ ${#errors[@]} -gt 0 ]; then
    echo "✗ bump.md contains template placeholders:"
    for err in "${errors[@]}"; do
        echo "    - $err"
    done
    echo ""
    echo "bump.md must be fully populated before execution."
    exit 1
fi

# Basic smoke check: make sure 'autoApprove' or 'AWI' text exists
if ! grep -qiE "auto-?approve|awi|permission rules" "$BUMP_FILE"; then
  echo "WARNING: bump.md does not appear to define permission/auto-approve rules (AWI)."
  # not fatal but advised
fi

echo "✓ bump.md is properly filled"
exit 0
