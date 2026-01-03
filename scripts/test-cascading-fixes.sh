#!/usr/bin/env bash
# Test suite for cascading issues fixes
# ATOM: ATOM-TEST-20260103-001-cascading-fixes

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/utf8-safe.sh"
source "${SCRIPT_DIR}/lib/plugin-init.sh"
source "${SCRIPT_DIR}/lib/safe-exec.sh"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

TESTS_PASSED=0
TESTS_FAILED=0

test_result() {
    local exit_code=$1
    local message="$2"
    if [ "$exit_code" -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $message"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗${NC} $message"
        ((TESTS_FAILED++))
    fi
}

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        Cascading Issues Fixes - Test Suite                ║"
echo "║                  ◉──◉───◉───◉──◉                           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Test 1: UTF-8 Safe String Operations
echo -e "${YELLOW}[Test Suite 1]${NC} UTF-8 Safe String Operations"
echo "─────────────────────────────────────────────────────────────"

# Test 1.1: CJK character length
echo -n "Test 1.1: CJK character length... "
result=$(utf8_length "你好世界")
if [ "$result" = "4" ]; then
    test_result 0 "CJK length calculation (expected 4, got $result)"
else
    test_result 1 "CJK length calculation (expected 4, got $result)"
fi

# Test 1.2: ASCII length
echo -n "Test 1.2: ASCII length... "
result=$(utf8_length "Hello")
if [ "$result" = "5" ]; then
    test_result 0 "ASCII length calculation (expected 5, got $result)"
else
    test_result 1 "ASCII length calculation (expected 5, got $result)"
fi

# Test 1.3: Mixed content length
echo -n "Test 1.3: Mixed content length... "
result=$(utf8_length "Hello世界")
if [ "$result" = "7" ]; then
    test_result 0 "Mixed content length (expected 7, got $result)"
else
    test_result 1 "Mixed content length (expected 7, got $result)"
fi

# Test 1.4: UTF-8 validation (valid)
echo -n "Test 1.4: Valid UTF-8 validation... "
if utf8_validate "Hello 世界 🌍"; then
    test_result 0 "Valid UTF-8 string accepted"
else
    test_result 1 "Valid UTF-8 string accepted"
fi

# Test 1.5: Substring extraction
echo -n "Test 1.5: UTF-8 substring extraction... "
result=$(utf8_substring "你好世界" 2 2)
if [ "$result" = "好世" ]; then
    test_result 0 "Substring extraction (expected '好世', got '$result')"
else
    test_result 1 "Substring extraction (expected '好世', got '$result')"
fi

echo ""

# Test 2: Plugin Initialization Ordering
echo -e "${YELLOW}[Test Suite 2]${NC} Plugin Initialization Ordering"
echo "─────────────────────────────────────────────────────────────"

# Define mock initialization functions
init_environment() { echo "  Initializing environment..."; return 0; }
init_lsp_server() { echo "  Initializing LSP server..."; return 0; }
init_mcp_server() { echo "  Initializing MCP server..."; return 0; }
init_workspace() { echo "  Initializing workspace..."; return 0; }

# Test 2.1: Proper initialization order
echo -n "Test 2.1: Plugins initialize in correct order... "
if plugin_init_all >/dev/null 2>&1; then
    test_result 0 "All plugins initialized in dependency order"
else
    test_result 1 "All plugins initialized in dependency order"
fi

# Test 2.2: Prevent re-initialization
echo -n "Test 2.2: Prevent duplicate initialization... "
if plugin_init "environment" "init_environment" 2>&1 | grep -q "already initialized"; then
    test_result 0 "Duplicate initialization prevented"
else
    test_result 1 "Duplicate initialization prevented"
fi

# Test 2.3: Dependency validation (reset state first)
echo -n "Test 2.3: Dependency validation enforced... "
# Run in fresh bash process to completely isolate state  
TEMP_SCRIPT="/tmp/test-plugin-$$.sh"
cat > "$TEMP_SCRIPT" << 'EOF'
source "$1/lib/plugin-init.sh"
init_mcp_server() { return 0; }
plugin_init "mcp_server" "init_mcp_server" 2>&1
EOF
# Capture output to file to avoid pipefail issues
bash "$TEMP_SCRIPT" "${SCRIPT_DIR}" > /tmp/test-output-$$.txt 2>&1
# Check for specific error message pattern indicating dependency enforcement
if grep -q "\[ERROR\].*requires.*to be initialized first" /tmp/test-output-$$.txt; then
    # Expected to fail with dependency error
    test_result 0 "Dependency validation enforced"
else
    # Should not succeed without dependencies
    test_result 1 "Dependency validation enforced"
fi
rm -f "$TEMP_SCRIPT" /tmp/test-output-$$.txt

echo ""

# Test 3: Permission Execution-Layer Validation
echo -e "${YELLOW}[Test Suite 3]${NC} Permission Execution-Layer Validation"
echo "─────────────────────────────────────────────────────────────"

# Test 3.1: Block dangerous rm -rf / command
echo -n "Test 3.1: Block 'rm -rf /' command... "
if safe_exec "rm -rf /" >/dev/null 2>&1; then
    test_result 1 "Dangerous rm command blocked"
else
    test_result 0 "Dangerous rm command blocked"
fi

# Test 3.2: Block fork bomb
echo -n "Test 3.2: Block fork bomb pattern... "
if safe_exec ":(){ :|:& };:" >/dev/null 2>&1; then
    test_result 1 "Fork bomb pattern blocked"
else
    test_result 0 "Fork bomb pattern blocked"
fi

# Test 3.3: Allow safe commands
echo -n "Test 3.3: Allow safe echo command... "
if safe_exec "echo 'test'" >/dev/null 2>&1; then
    test_result 0 "Safe command executed"
else
    test_result 1 "Safe command executed"
fi

# Test 3.4: Path validation for destructive operations
echo -n "Test 3.4: Path validation for destructive ops... "
mkdir -p /tmp/test-safe-exec-$$
if safe_exec "rm -rf /tmp/test-safe-exec-$$" >/dev/null 2>&1; then
    test_result 0 "Safe path allowed for destructive operation"
else
    test_result 1 "Safe path allowed for destructive operation"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo -e "Test Results: ${GREEN}${TESTS_PASSED} passed${NC}, ${RED}${TESTS_FAILED} failed${NC}"
echo "═══════════════════════════════════════════════════════════"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed.${NC}"
    exit 1
fi
