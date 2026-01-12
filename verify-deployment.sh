#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# SpiralSafe Deployment Verification Script
# ═══════════════════════════════════════════════════════════════
# Usage: ./verify-deployment.sh [api-key]
# Example: ./verify-deployment.sh your-api-key-here

set -euo pipefail  # Strict mode: exit on error, unset vars, and pipeline failures

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# API configuration
API_BASE="${API_BASE:-https://api.spiralsafe.org}"
PUBLIC_SITE="${PUBLIC_SITE:-https://spiralsafe.org}"
API_KEY="${1:-}"

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     SpiralSafe Deployment Verification                    ║"
echo "║     H&&S:WAVE Protocol - Production Readiness Check      ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Counters
PASSED=0
FAILED=0
WARNINGS=0

# ═══════════════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════════════

print_test() {
    echo -e "${BLUE}━━━ $1 ━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✅ PASS:${NC} $1"
    ((PASSED++))
}

print_failure() {
    echo -e "${RED}❌ FAIL:${NC} $1"
    ((FAILED++))
}

print_warning() {
    echo -e "${YELLOW}⚠️  WARN:${NC} $1"
    ((WARNINGS++))
}

print_info() {
    echo -e "${CYAN}ℹ️  INFO:${NC} $1"
}

# ═══════════════════════════════════════════════════════════════
# 1. Configuration Checks
# ═══════════════════════════════════════════════════════════════

print_test "Configuration Verification"

# Check wrangler.toml
if [ -f "ops/wrangler.toml" ]; then
    print_success "Found ops/wrangler.toml"

    # Check D1 binding
    if grep -q "database_id = \"d47d04ca-7d74-41a8-b489-0af373a2bb2c\"" ops/wrangler.toml; then
        print_success "D1 database binding configured"
    else
        print_failure "D1 database binding missing or incorrect"
    fi

    # Check KV binding
    if grep -q "id = \"79d496efbfab4d54a6277ed80dc29d1f\"" ops/wrangler.toml; then
        print_success "KV namespace binding configured"
    else
        print_failure "KV namespace binding missing or incorrect"
    fi

    # Check R2 binding
    if grep -q "bucket_name = \"spiralsafe-contexts\"" ops/wrangler.toml; then
        print_success "R2 bucket binding configured"
    else
        print_failure "R2 bucket binding missing or incorrect"
    fi
else
    print_failure "ops/wrangler.toml not found"
fi

# Check public site
if [ -f "public/index.html" ]; then
    FILE_SIZE=$(stat -f%z "public/index.html" 2>/dev/null || stat -c%s "public/index.html" 2>/dev/null)
    print_success "Found public/index.html (${FILE_SIZE} bytes)"

    # Check for key content
    if grep -q "SpiralSafe" public/index.html; then
        print_success "Public site contains SpiralSafe branding"
    else
        print_warning "Public site missing SpiralSafe branding"
    fi

    if grep -q "H&&S:WAVE" public/index.html; then
        print_success "Public site contains H&&S:WAVE protocol references"
    else
        print_warning "Public site missing H&&S:WAVE protocol info"
    fi
else
    print_failure "public/index.html not found"
fi

echo ""

# ═══════════════════════════════════════════════════════════════
# 2. API Endpoint Tests (if deployed)
# ═══════════════════════════════════════════════════════════════

print_test "API Endpoint Verification"

# Test if API is reachable
if command -v curl &> /dev/null; then
    # Health check
    print_info "Testing: GET ${API_BASE}/api/health"
    HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "${API_BASE}/api/health" 2>&1 || echo "FAILED")
    HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -n1)
    HEALTH_BODY=$(echo "$HEALTH_RESPONSE" | sed '$d')

    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "503" ]; then
        print_success "Health endpoint responded (HTTP $HTTP_CODE)"

        # Check response content
        if echo "$HEALTH_BODY" | grep -q "status"; then
            print_success "Health response contains status field"

            # Parse status
            if echo "$HEALTH_BODY" | grep -q "\"status\":\"healthy\""; then
                print_success "API status: HEALTHY"
            elif echo "$HEALTH_BODY" | grep -q "\"status\":\"degraded\""; then
                print_warning "API status: DEGRADED (some bindings may not be working)"
            fi

            # Check bindings
            if echo "$HEALTH_BODY" | grep -q "\"d1\":true"; then
                print_success "D1 database binding: WORKING"
            else
                print_warning "D1 database binding: NOT WORKING"
            fi

            if echo "$HEALTH_BODY" | grep -q "\"kv\":true"; then
                print_success "KV namespace binding: WORKING"
            else
                print_warning "KV namespace binding: NOT WORKING"
            fi

            if echo "$HEALTH_BODY" | grep -q "\"r2\":true"; then
                print_success "R2 bucket binding: WORKING"
            else
                print_warning "R2 bucket binding: NOT WORKING"
            fi
        fi
    elif [ "$HTTP_CODE" = "FAILED" ] || [ -z "$HTTP_CODE" ]; then
        print_warning "API not reachable at ${API_BASE} (not deployed yet or network issue)"
        print_info "This is OK if you haven't deployed yet. Run: cd ops && npx wrangler deploy"
    else
        print_failure "Health endpoint returned HTTP $HTTP_CODE"
    fi

    # Test authentication (if API key provided)
    if [ -n "$API_KEY" ]; then
        echo ""
        print_info "Testing authentication with provided API key..."

        # Test unauthenticated request (should fail)
        print_info "Testing: POST /api/wave/analyze (no auth)"
        UNAUTH_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${API_BASE}/api/wave/analyze" \
            -H "Content-Type: application/json" \
            -d '{"content":"test"}' 2>&1 || echo "FAILED")
        UNAUTH_CODE=$(echo "$UNAUTH_RESPONSE" | tail -n1)

        if [ "$UNAUTH_CODE" = "401" ]; then
            print_success "Unauthenticated request correctly rejected (HTTP 401)"
        else
            print_warning "Unauthenticated request got HTTP $UNAUTH_CODE (expected 401)"
        fi

        # Test authenticated request
        print_info "Testing: POST /api/wave/analyze (with auth)"
        AUTH_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${API_BASE}/api/wave/analyze" \
            -H "Content-Type: application/json" \
            -H "X-API-Key: $API_KEY" \
            -d '{"content":"From the constraints, gifts."}' 2>&1 || echo "FAILED")
        AUTH_CODE=$(echo "$AUTH_RESPONSE" | tail -n1)

        if [ "$AUTH_CODE" = "200" ]; then
            print_success "Authenticated request accepted (HTTP 200)"
        elif [ "$AUTH_CODE" = "403" ]; then
            print_failure "Authenticated request rejected (HTTP 403) - API key may be incorrect"
        else
            print_warning "Authenticated request got HTTP $AUTH_CODE"
        fi
    else
        print_info "No API key provided - skipping authentication tests"
        print_info "Run with API key: ./verify-deployment.sh YOUR_API_KEY"
    fi
else
    print_warning "curl not found - skipping API tests"
fi

echo ""

# ═══════════════════════════════════════════════════════════════
# 3. Public Site Tests (if deployed)
# ═══════════════════════════════════════════════════════════════

print_test "Public Site Verification"

if command -v curl &> /dev/null; then
    print_info "Testing: GET ${PUBLIC_SITE}"
    SITE_RESPONSE=$(curl -s -w "\n%{http_code}" "${PUBLIC_SITE}" 2>&1 || echo "FAILED")
    SITE_CODE=$(echo "$SITE_RESPONSE" | tail -n1)
    SITE_BODY=$(echo "$SITE_RESPONSE" | sed '$d')

    if [ "$SITE_CODE" = "200" ]; then
        print_success "Public site is live (HTTP 200)"

        # Check content
        if echo "$SITE_BODY" | grep -q "SpiralSafe"; then
            print_success "Site contains SpiralSafe branding"
        fi

        if echo "$SITE_BODY" | grep -q "H&&S:WAVE"; then
            print_success "Site contains H&&S:WAVE protocol info"
        fi

        if echo "$SITE_BODY" | grep -q "Quantum"; then
            print_success "Site contains quantum computing references"
        fi
    elif [ "$SITE_CODE" = "FAILED" ] || [ -z "$SITE_CODE" ]; then
        print_warning "Public site not reachable at ${PUBLIC_SITE} (not deployed yet)"
        print_info "Deploy with: cd public && npx wrangler pages deploy . --project-name spiralsafe"
    else
        print_failure "Public site returned HTTP $SITE_CODE"
    fi
else
    print_warning "curl not found - skipping site tests"
fi

echo ""

# ═══════════════════════════════════════════════════════════════
# 4. Documentation Check
# ═══════════════════════════════════════════════════════════════

print_test "Documentation Completeness"

DOCS=(
    "DEPLOYMENT_GUIDE.md:Deployment guide"
    "PRODUCTION_READY.md:Production readiness manifest"
    "ops/SECURITY_GUIDE.md:Security documentation"
    "ops/ADMIN_SYSTEM_ARCHITECTURE.md:Admin console architecture"
    "ops/ATOM_AUTH_SYSTEM.md:ATOM-AUTH design"
    "minecraft/SPIRALCRAFT_QUANTUM_PLUGIN.md:SpiralCraft plugin spec"
    "minecraft/QUANTUM_CIRCUITS.md:Quantum circuits guide"
    "minecraft/QUANTUM_COMPUTER_ARCHITECTURE.md:Quantum computer design"
)

for doc in "${DOCS[@]}"; do
    IFS=':' read -r file desc <<< "$doc"
    if [ -f "$file" ]; then
        print_success "Found $desc ($file)"
    else
        print_warning "Missing $desc ($file)"
    fi
done

echo ""

# ═══════════════════════════════════════════════════════════════
# 5. Git Status
# ═══════════════════════════════════════════════════════════════

print_test "Git Repository Status"

if command -v git &> /dev/null; then
    CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
    print_info "Current branch: $CURRENT_BRANCH"

    if [ "$CURRENT_BRANCH" = "main" ]; then
        print_success "On main branch (production ready)"
    else
        print_info "On branch: $CURRENT_BRANCH"
    fi

    # Check for uncommitted changes
    if git diff --quiet 2>/dev/null && git diff --cached --quiet 2>/dev/null; then
        print_success "No uncommitted changes"
    else
        print_warning "Uncommitted changes detected"
    fi

    # Show latest commit
    LATEST_COMMIT=$(git log -1 --oneline 2>/dev/null || echo "unknown")
    print_info "Latest commit: $LATEST_COMMIT"
else
    print_warning "git not found - skipping repository checks"
fi

echo ""

# ═══════════════════════════════════════════════════════════════
# 6. Summary
# ═══════════════════════════════════════════════════════════════

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                  VERIFICATION SUMMARY                      ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

echo -e "${GREEN}✅ Passed:   $PASSED${NC}"
echo -e "${RED}❌ Failed:   $FAILED${NC}"
echo -e "${YELLOW}⚠️  Warnings: $WARNINGS${NC}"
echo ""

# Overall status
if [ $FAILED -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║  🎉 ALL CHECKS PASSED - READY FOR PRODUCTION! 🎉    ║${NC}"
        echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
        EXIT_CODE=0
    else
        echo -e "${YELLOW}╔═══════════════════════════════════════════════════════╗${NC}"
        echo -e "${YELLOW}║  ⚠️  MOSTLY READY - REVIEW WARNINGS ABOVE           ║${NC}"
        echo -e "${YELLOW}╚═══════════════════════════════════════════════════════╝${NC}"
        EXIT_CODE=0
    fi
else
    echo -e "${RED}╔═══════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ❌ FAILED CHECKS - REVIEW ERRORS ABOVE              ║${NC}"
    echo -e "${RED}╚═══════════════════════════════════════════════════════╝${NC}"
    EXIT_CODE=1
fi

echo ""
echo -e "${CYAN}Next Steps:${NC}"
if [ $FAILED -gt 0 ]; then
    echo "1. Fix the failed checks above"
    echo "2. Re-run this script to verify"
fi
if [ $WARNINGS -gt 0 ] && [ $FAILED -eq 0 ]; then
    echo "1. Review warnings (they may be expected if not deployed yet)"
    echo "2. Deploy: cd ops && npx wrangler deploy"
    echo "3. Deploy site: cd public && npx wrangler pages deploy ."
fi
if [ $FAILED -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "1. Everything looks good!"
    echo "2. If not deployed: cd ops && npx wrangler deploy"
    echo "3. Merge to main: git checkout main && git merge $CURRENT_BRANCH"
fi

echo ""
echo -e "${PURPLE}H&&S:WAVE | From verification to deployment. From the spiral, production.${NC}"
echo ""

exit $EXIT_CODE
