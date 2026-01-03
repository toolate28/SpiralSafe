#!/usr/bin/env bash
# Freshness tracking and bedrock migration system
# Run periodically to update freshness levels and migrate stable decisions to bedrock
set -euo pipefail

DECISION_DIR=".atom-trail/decisions"
BEDROCK_DIR=".atom-trail/bedrock"
CURRENT_EPOCH=$(date +%s)

# Thresholds (in seconds)
AGING_THRESHOLD=$((30 * 24 * 3600))    # 30 days -> aging
SETTLED_THRESHOLD=$((90 * 24 * 3600))   # 90 days -> settled
BEDROCK_THRESHOLD=$((180 * 24 * 3600))  # 180 days -> bedrock eligible

mkdir -p "$BEDROCK_DIR"

echo "Updating freshness levels..."

# Process each decision file
for decision_file in "$DECISION_DIR"/*.json; do
  if [ ! -f "$decision_file" ]; then
    continue
  fi
  
  # Extract created_epoch using grep and sed (avoiding jq dependency)
  CREATED_EPOCH=$(grep -o '"created_epoch":[[:space:]]*[0-9]*' "$decision_file" | sed 's/[^0-9]*//g')
  
  if [ -z "$CREATED_EPOCH" ]; then
    echo "Warning: Could not parse created_epoch from $decision_file"
    continue
  fi
  
  AGE=$((CURRENT_EPOCH - CREATED_EPOCH))
  ATOM_TAG=$(basename "$decision_file" .json)
  
  # Determine freshness level
  if [ "$AGE" -ge "$BEDROCK_THRESHOLD" ]; then
    NEW_FRESHNESS="bedrock-eligible"
    BEDROCK_ELIGIBLE="true"
  elif [ "$AGE" -ge "$SETTLED_THRESHOLD" ]; then
    NEW_FRESHNESS="settled"
    BEDROCK_ELIGIBLE="false"
  elif [ "$AGE" -ge "$AGING_THRESHOLD" ]; then
    NEW_FRESHNESS="aging"
    BEDROCK_ELIGIBLE="false"
  else
    NEW_FRESHNESS="fresh"
    BEDROCK_ELIGIBLE="false"
  fi
  
  # Update the file - Note: Using sed for portability. If jq is available, it would be preferred:
  # jq ".freshness_level = \"$NEW_FRESHNESS\" | .bedrock_eligible = $BEDROCK_ELIGIBLE" "$decision_file" > "$decision_file.tmp" && mv "$decision_file.tmp" "$decision_file"
  sed -i "s/\"freshness_level\":[[:space:]]*\"[^\"]*\"/\"freshness_level\": \"$NEW_FRESHNESS\"/" "$decision_file"
  sed -i "s/\"bedrock_eligible\":[[:space:]]*[^,}]*/\"bedrock_eligible\": $BEDROCK_ELIGIBLE/" "$decision_file"
  
  echo "  $ATOM_TAG: $NEW_FRESHNESS (age: $((AGE / 86400)) days)"
  
  # Migrate to bedrock if eligible (requires verification)
  if [ "$BEDROCK_ELIGIBLE" = "true" ]; then
    # Require verification before bedrock migration
    VERIFIED=$(grep -o '"verified":[[:space:]]*true' "$decision_file" 2>/dev/null || echo "")
    if [ -z "$VERIFIED" ]; then
      echo "    ⚠ Bedrock-eligible but not verified: $ATOM_TAG"
      echo "    → Run: ./scripts/verify-decision.sh $ATOM_TAG"
      BEDROCK_ELIGIBLE="false"  # Don't migrate unverified decisions
    else
      if [ ! -f "$BEDROCK_DIR/$ATOM_TAG.json" ]; then
        cp "$decision_file" "$BEDROCK_DIR/"
        echo "    → Migrated to bedrock (verified)"
      fi
    fi
  fi
done

echo ""
echo "Freshness update complete"
echo "Fresh: $(find "$DECISION_DIR" -name "*.json" -exec grep -l '"freshness_level": "fresh"' {} \; 2>/dev/null | wc -l)"
echo "Aging: $(find "$DECISION_DIR" -name "*.json" -exec grep -l '"freshness_level": "aging"' {} \; 2>/dev/null | wc -l)"
echo "Settled: $(find "$DECISION_DIR" -name "*.json" -exec grep -l '"freshness_level": "settled"' {} \; 2>/dev/null | wc -l)"
echo "Bedrock-eligible: $(find "$DECISION_DIR" -name "*.json" -exec grep -l '"freshness_level": "bedrock-eligible"' {} \; 2>/dev/null | wc -l)"
echo "Bedrock: $(find "$BEDROCK_DIR" -name "*.json" 2>/dev/null | wc -l)"

exit 0
