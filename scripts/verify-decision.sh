#!/usr/bin/env bash
# Verify ATOM decision for bedrock eligibility
# Ensures decisions are validated before becoming bedrock
set -euo pipefail

ATOM_TAG="${1:-}"

if [ -z "$ATOM_TAG" ]; then
    echo "Usage: $0 <ATOM-TAG>"
    echo "Example: $0 ATOM-INIT-20260102-001-repository-setup-with-ci-and-atom-tracking"
    exit 1
fi

DECISION_DIR=".atom-trail/decisions"
DECISION_FILE="$DECISION_DIR/$ATOM_TAG.json"

if [ ! -f "$DECISION_FILE" ]; then
    echo "✗ Decision file not found: $DECISION_FILE"
    exit 1
fi

echo "Verifying decision: $ATOM_TAG"
echo ""

# Check if already verified
if grep -q '"verified":[[:space:]]*true' "$DECISION_FILE"; then
    echo "✓ Decision already verified"
    exit 0
fi

# Perform verification checks
echo "Verification checks:"
echo "  1. Decision file exists: ✓"

# Check if decision has required fields
REQUIRED_FIELDS=("atom_tag" "type" "description" "timestamp" "freshness_level")
ALL_FIELDS_PRESENT=true

for field in "${REQUIRED_FIELDS[@]}"; do
    if grep -q "\"$field\":" "$DECISION_FILE"; then
        echo "  2. Has $field: ✓"
    else
        echo "  2. Has $field: ✗"
        ALL_FIELDS_PRESENT=false
    fi
done

if [ "$ALL_FIELDS_PRESENT" = false ]; then
    echo ""
    echo "✗ Decision missing required fields"
    exit 1
fi

# Check if decision is old enough (at least 30 days for bedrock consideration)
CREATED_EPOCH=$(grep -o '"created_epoch":[[:space:]]*[0-9]*' "$DECISION_FILE" | sed 's/[^0-9]*//g')
CURRENT_EPOCH=$(date +%s)
AGE=$((CURRENT_EPOCH - CREATED_EPOCH))
AGE_DAYS=$((AGE / 86400))

echo "  3. Decision age: $AGE_DAYS days"

if [ "$AGE_DAYS" -ge 30 ]; then
    echo "     ✓ Old enough for verification (>= 30 days)"
else
    echo "     ⚠ Too recent for bedrock (< 30 days)"
fi

# Mark as verified
echo ""
echo "Marking decision as verified..."

# Add verified field to JSON
CURRENT_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)
if command -v jq >/dev/null 2>&1; then
    # Use jq if available
    jq '. + {verified: true, verified_at: "'"$CURRENT_TIME"'", verified_by: "manual"}' "$DECISION_FILE" > "$DECISION_FILE.tmp"
else
    # Fallback to sed (portable, no in-place -i)
    sed 's/}$/,"verified":true,"verified_at":"'"$CURRENT_TIME"'","verified_by":"manual"}/' "$DECISION_FILE" > "$DECISION_FILE.tmp"
fi
mv "$DECISION_FILE.tmp" "$DECISION_FILE"

echo "✓ Decision verified successfully"
echo ""
echo "Decision can now be migrated to bedrock when it reaches bedrock age threshold."
exit 0
