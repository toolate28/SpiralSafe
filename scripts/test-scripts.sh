#!/usr/bin/env bash
# Test runner for all shell scripts
# Uses shellcheck for linting and basic execution tests
set -euo pipefail

EXIT_CODE=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== Shell Script Testing ==="
echo ""

# Function to test a script
test_script() {
  local script="$1"
  local script_name
  script_name=$(basename "$script")
  
  echo "Testing: $script_name"
  
  # Shellcheck if available (ignore info-level, only warn on warning+)
  if command -v shellcheck >/dev/null 2>&1; then
    if shellcheck -x --severity=warning "$script" 2>&1; then
      echo "  ✓ shellcheck passed"
    else
      echo "  ✗ shellcheck failed"
      EXIT_CODE=1
    fi
  else
    echo "  ⚠ shellcheck not available (install recommended)"
  fi
  
  # Syntax check
  if bash -n "$script" 2>&1; then
    echo "  ✓ syntax check passed"
  else
    echo "  ✗ syntax check failed"
    EXIT_CODE=1
  fi
  
  echo ""
}

# Test all shell scripts
cd "$REPO_ROOT"

echo "Finding shell scripts..."
SCRIPTS=$(find scripts -type f -name "*.sh" 2>/dev/null || true)

if [ -z "$SCRIPTS" ]; then
  echo "No shell scripts found"
  exit 0
fi

for script in $SCRIPTS; do
  test_script "$script"
done

# Test create_spiral_payload.sh if it exists
if [ -f "create_spiral_payload.sh" ]; then
  test_script "create_spiral_payload.sh"
fi

echo "=== Test Summary ==="
if [ $EXIT_CODE -eq 0 ]; then
  echo "✓ All tests passed"
else
  echo "✗ Some tests failed"
fi

exit $EXIT_CODE
