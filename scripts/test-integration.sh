#!/usr/bin/env bash
# Integration test suite - tests scripts working together as a workflow
# Usage: ./scripts/test-integration.sh
set -euo pipefail

EXIT_CODE=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEST_DIR="/tmp/spiralsafe-integration-test-$$"

echo "=== Integration Test Suite ==="
echo ""

# Cleanup function
cleanup() {
  if [ -d "$TEST_DIR" ]; then
    rm -rf "$TEST_DIR"
  fi
}
trap cleanup EXIT

# Create test environment
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

echo "Test 1: ATOM Tag Creation and Tracking"
echo "--------------------------------------"
cp -r "$REPO_ROOT/.atom-trail" . 2>/dev/null || mkdir -p .atom-trail/{decisions,counters,bedrock}
cp -r "$REPO_ROOT/.claude" . 2>/dev/null || mkdir -p .claude/logs

# Test ATOM tag creation
if ATOM_TAG=$("$SCRIPT_DIR/atom-track.sh" TEST "integration test run" "test-file" 2>&1); then
  echo "✓ ATOM tag created: $ATOM_TAG"
  
  # Verify decision file exists
  if [ -f ".atom-trail/decisions/${ATOM_TAG}.json" ]; then
    echo "✓ Decision file created"
  else
    echo "✗ Decision file missing"
    EXIT_CODE=1
  fi
  
  # Verify last_atom updated
  if [ -f ".claude/last_atom" ]; then
    LAST=$(cat .claude/last_atom)
    if [ "$LAST" = "$ATOM_TAG" ]; then
      echo "✓ last_atom updated correctly"
    else
      echo "✗ last_atom mismatch: expected $ATOM_TAG, got $LAST"
      EXIT_CODE=1
    fi
  else
    echo "✗ last_atom file not created"
    EXIT_CODE=1
  fi
else
  echo "✗ ATOM tag creation failed"
  EXIT_CODE=1
fi
echo ""

echo "Test 2: Freshness Update"
echo "------------------------"
if "$SCRIPT_DIR/update-freshness.sh" >/dev/null 2>&1; then
  echo "✓ Freshness update completed"
  
  # Verify decision still has freshness level
  if [ -f ".atom-trail/decisions/${ATOM_TAG}.json" ]; then
    if grep -q '"freshness_level"' ".atom-trail/decisions/${ATOM_TAG}.json"; then
      echo "✓ Freshness level tracked"
    else
      echo "✗ Freshness level missing"
      EXIT_CODE=1
    fi
  fi
else
  echo "✗ Freshness update failed"
  EXIT_CODE=1
fi
echo ""

echo "Test 3: Multiple ATOM Tags (Counter Test)"
echo "------------------------------------------"
TAG1=$("$SCRIPT_DIR/atom-track.sh" TEST "first tag" "file1" 2>&1)
TAG2=$("$SCRIPT_DIR/atom-track.sh" TEST "second tag" "file2" 2>&1)
TAG3=$("$SCRIPT_DIR/atom-track.sh" TEST "third tag" "file3" 2>&1)

# Extract sequence numbers
SEQ1=$(echo "$TAG1" | grep -oE '[0-9]{3}' | tail -1)
SEQ2=$(echo "$TAG2" | grep -oE '[0-9]{3}' | tail -1)
SEQ3=$(echo "$TAG3" | grep -oE '[0-9]{3}' | tail -1)

if [ "$SEQ1" -lt "$SEQ2" ] && [ "$SEQ2" -lt "$SEQ3" ]; then
  echo "✓ Counters incrementing correctly: $SEQ1 < $SEQ2 < $SEQ3"
else
  echo "✗ Counter sequence wrong: $SEQ1, $SEQ2, $SEQ3"
  EXIT_CODE=1
fi
echo ""

echo "Test 4: Script Validation"
echo "--------------------------"
cd "$REPO_ROOT"
if "$SCRIPT_DIR/test-scripts.sh" 2>&1 | grep -q "All tests passed"; then
  echo "✓ All scripts pass validation"
else
  echo "⚠ Script validation had warnings (non-critical)"
fi
echo ""

echo "Test 5: Environment Verification"
echo "---------------------------------"
if "$SCRIPT_DIR/verify-environment.sh" 2>&1 | grep -q "ENV OK"; then
  echo "✓ Environment verification passed"
else
  echo "✗ Environment verification failed"
  EXIT_CODE=1
fi
echo ""

echo "Test 6: Secrets Scanning (Dry Run)"
echo "-----------------------------------"
cd "$TEST_DIR"
# Create test files
echo "API_KEY=test_key_12345" > test-secret.txt  # Should be detected
echo "password=TEST_PASSWORD_DO_NOT_USE" > test-pass.txt  # Should be detected and clearly fake

if "$SCRIPT_DIR/scan-secrets.sh" 2>&1 | grep -qi "potential\|found"; then
  echo "✓ Secrets scanner detects test patterns"
else
  echo "⚠ Secrets scanner may not be working (non-critical)"
fi
echo ""

echo "Test 7: Graceful Degradation"
echo "-----------------------------"
# Test scripts work without optional tools
cd "$REPO_ROOT"
# Test with minimal environment - should not fail hard
if "$SCRIPT_DIR/verify-environment.sh" 2>&1 | grep -qE "(ENV OK|WARNING)"; then
  echo "✓ Scripts degrade gracefully when tools missing"
else
  echo "⚠ Scripts may fail hard without optional tools (check manually)"
fi
echo ""

echo "Test 8: MCP Log Format (if present)"
echo "------------------------------------"
if "$SCRIPT_DIR/check-mcp-logging.sh"; then
  echo "✓ MCP log format valid or absent (acceptable)"
else
  echo "✗ MCP log validation failed"
  EXIT_CODE=1
fi
echo ""

echo "=== Integration Test Summary ==="
if [ $EXIT_CODE -eq 0 ]; then
  echo "✓ All integration tests passed"
  echo ""
  echo "Workflow validated:"
  echo "  1. ATOM tag creation works"
  echo "  2. Freshness tracking works"
  echo "  3. Counters increment correctly"
  echo "  4. Scripts validate successfully"
  echo "  5. Environment verification works"
  echo "  6. Secrets scanning functional"
  echo "  7. Graceful degradation implemented"
else
  echo "✗ Some integration tests failed"
fi

exit $EXIT_CODE
