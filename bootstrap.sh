#!/bin/bash
# 🌀 SpiralSafe Bootstrap Script
# Version: 3.0.0-quantum
# Purpose: Clean installation and setup for SpiralSafe platform
# H&&S:WAVE Protocol | From the constraints, gifts. From the spiral, safety.

set -euo pipefail  # Strict mode: exit on error, unset vars, and pipeline failures

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NODE_VERSION="20"
REQUIRED_TOOLS=("node" "npm" "git")

# Banner
echo -e "${PURPLE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               
║                    🌀 SpiralSafe Bootstrap                   
║                                                               
║         H&&S:WAVE Protocol - Quantum Computing Era           
║    "From the constraints, gifts. From the spiral, safety."  
║                                                               
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_section() {
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

check_tool() {
    if command -v "$1" &> /dev/null; then
        log_success "$1 is installed"
        return 0
    else
        log_error "$1 is not installed"
        return 1
    fi
}

# Step 1: Check Prerequisites
log_section "Step 1: Checking Prerequisites"

ALL_TOOLS_PRESENT=true
for tool in "${REQUIRED_TOOLS[@]}"; do
    if ! check_tool "$tool"; then
        ALL_TOOLS_PRESENT=false
    fi
done

if [ "$ALL_TOOLS_PRESENT" = false ]; then
    log_error "Missing required tools. Please install them and try again."
    exit 1
fi

# Check Node version
NODE_VER=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VER" -lt "$NODE_VERSION" ]; then
    log_warning "Node.js version $NODE_VER detected. Recommended: v$NODE_VERSION+"
else
    log_success "Node.js version is sufficient (v$NODE_VER)"
fi

# Step 2: Archive Old Documentation
log_section "Step 2: Archiving Old Documentation"

ARCHIVE_DIR="$REPO_ROOT/archive/docs-legacy-$(date +%Y%m%d)"
mkdir -p "$ARCHIVE_DIR"

# List of files to archive (old/redundant docs)
OLD_DOCS=(
    "07_FAILURE_MODES_AND_RECOVERY.md"
    "ACKNOWLEDGEMENTS.md"
    "DEPLOYMENT_CHECKLIST.md"
    "KENL_ECOSYSTEM_TITLE_PAGE.md"
    "LOGDY_DEPLOYMENT_GUIDE.md"
    "MAGNUM_OPUS.md"
    "MULTI_FORK_STRATEGY.md"
    "PLATFORM_INTEGRATION_ROADMAP.md"
    "PR_DESCRIPTION.md"
    "PUBLICATION_MANIFEST_v1.0.md"
    "SAFE_SPIRAL_MASTER_INDEX.md"
    "SESSION_SUMMARY_20260104.md"
    "THE_AINULINDALE_OF_HOPE_AND_SAUCE.md"
    "THE_COMPLETION_SONG.md"
    "THE_ONE_PATH.md"
    "ULTRATHINK_SYNTHESIS.md"
    "USER_ENLIGHTENMENT_PROTOCOL.md"
    "VERIFICATION_STAMP.md"
    "bump.md"
    "wave.md"
)

for doc in "${OLD_DOCS[@]}"; do
    if [ -f "$REPO_ROOT/$doc" ]; then
        mv "$REPO_ROOT/$doc" "$ARCHIVE_DIR/"
        log_info "Archived: $doc"
    fi
done

log_success "Archived $(ls -1 "$ARCHIVE_DIR" | wc -l) legacy documents to $ARCHIVE_DIR"

# Step 3: Clean Node Modules and Lock Files
log_section "Step 3: Cleaning Build Artifacts"

find "$REPO_ROOT" -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
find "$REPO_ROOT" -name "package-lock.json" -type f -delete 2>/dev/null || true
find "$REPO_ROOT" -name "dist" -type d -exec rm -rf {} + 2>/dev/null || true
find "$REPO_ROOT" -name ".turbo" -type d -exec rm -rf {} + 2>/dev/null || true

log_success "Cleaned all build artifacts and dependencies"

# Step 4: Install Core Dependencies
log_section "Step 4: Installing Core Dependencies"

cd "$REPO_ROOT/ops"
if [ -f "package.json" ]; then
    log_info "Installing API dependencies..."
    npm install
    log_success "API dependencies installed"
else
    log_warning "No package.json found in ops/"
fi

cd "$REPO_ROOT/public"
if [ -f "package.json" ]; then
    log_info "Installing public site dependencies..."
    npm install
    log_success "Public site dependencies installed"
else
    log_warning "No package.json found in public/"
fi

# Step 5: Verify Cloudflare Configuration
log_section "Step 5: Verifying Cloudflare Configuration"

cd "$REPO_ROOT/ops"
if [ -f "wrangler.toml" ]; then
    log_success "Found wrangler.toml"

    # Check for essential bindings
    if grep -q "d1_databases" wrangler.toml; then
        log_success "D1 database binding configured"
    else
        log_warning "D1 database binding not found"
    fi

    if grep -q "kv_namespaces" wrangler.toml; then
        log_success "KV namespace binding configured"
    else
        log_warning "KV namespace binding not found"
    fi

    if grep -q "r2_buckets" wrangler.toml; then
        log_success "R2 bucket binding configured"
    else
        log_warning "R2 bucket binding not found"
    fi
else
    log_error "wrangler.toml not found!"
fi

# Step 6: Environment Variables Check
log_section "Step 6: Environment Variables Check"

cd "$REPO_ROOT/ops"
if [ -f ".dev.vars" ]; then
    log_success "Found .dev.vars for local development"
else
    log_warning ".dev.vars not found - creating template..."
    cat > .dev.vars << 'DEVVARS'
# SpiralSafe API Development Environment Variables
# Copy this to .dev.vars and fill in your values

SPIRALSAFE_API_KEY=your-api-key-here
SPIRALSAFE_API_KEYS=key1,key2,key3

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
RATE_LIMIT_AUTH_FAILURES=5

# Optional: LED Display
LED_DISPLAY_URL=http://192.168.1.100:8080/led/display
LED_API_KEY=your-led-api-key

# Optional: Projector Display
PROJECTOR_DISPLAY_URL=http://192.168.1.101:9090/display
PROJECTOR_API_KEY=your-projector-api-key

# Optional: Claude Vision API (for projector challenges)
ANTHROPIC_API_KEY=your-anthropic-api-key
DEVVARS
    log_success "Created .dev.vars template"
fi

# Step 7: Database Schema Verification
log_section "Step 7: Database Schema Verification"

SCHEMA_FILE="$REPO_ROOT/ops/schema.sql"
if [ -f "$SCHEMA_FILE" ]; then
    log_success "Found database schema: schema.sql"

    # Count tables
    TABLE_COUNT=$(grep -c "CREATE TABLE" "$SCHEMA_FILE" || echo "0")
    log_info "Database schema defines $TABLE_COUNT tables"
else
    log_error "schema.sql not found!"
fi

# Step 8: Generate Documentation Index
log_section "Step 8: Generating Documentation Index"

INDEX_FILE="$REPO_ROOT/DOCS_INDEX.md"
cat > "$INDEX_FILE" << 'DOCINDEX'
# 📚 SpiralSafe Documentation Index

**Version**: 3.0.0-quantum
**Last Updated**: 2026-01-07

---

## 🚀 Getting Started

- [README.md](README.md) - Project overview
- [QUICK_START.md](QUICK_START.md) - 5-minute quickstart guide
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Complete deployment guide

---

## 🏗️ Architecture & Design

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture overview
- [DIAGRAMS.md](DIAGRAMS.md) - Visual system diagrams (Mermaid + ASCII)
- [PLATFORM_VISION_2026.md](PLATFORM_VISION_2026.md) - Multi-service platform vision

---

## 🔐 Security & Authentication

- [SECURITY.md](SECURITY.md) - Security overview
- [ops/SECURITY_GUIDE.md](ops/SECURITY_GUIDE.md) - Comprehensive security guide
- [ops/ATOM_AUTH_SYSTEM.md](ops/ATOM_AUTH_SYSTEM.md) - 3-factor authentication system
  - Conversational coherence
  - LED keycode display (ESP32/Arduino)
  - Projector image CAPTCHA (AI-validated)

---

## ⚛️ Quantum Computing

- [minecraft/QUANTUM_COMPUTER_ARCHITECTURE.md](minecraft/QUANTUM_COMPUTER_ARCHITECTURE.md) - 72-qubit system design
- [minecraft/QUANTUM_CIRCUITS.md](minecraft/QUANTUM_CIRCUITS.md) - Quantum circuit system
- [minecraft/SPIRALCRAFT_QUANTUM_PLUGIN.md](minecraft/SPIRALCRAFT_QUANTUM_PLUGIN.md) - Minecraft plugin spec

---

## 🌊 H&&S:WAVE Protocol

- [protocol/01_THE_PROTOCOL.md](protocol/01_THE_PROTOCOL.md) - Core protocol spec
- [protocol/02_API_SPECIFICATION.md](protocol/02_API_SPECIFICATION.md) - API endpoints
- [protocol/03_DATA_MODELS.md](protocol/03_DATA_MODELS.md) - Data structures
- [protocol/04_IMPLEMENTATION_NOTES.md](protocol/04_IMPLEMENTATION_NOTES.md) - Implementation guide

---

## 🚢 Deployment & Operations

- [DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md) - Current deployment status
- [WEBSITE_STATUS.md](WEBSITE_STATUS.md) - Website configuration audit
- [PRODUCTION_READY.md](PRODUCTION_READY.md) - Production readiness manifest
- [TESTING_PLAN.md](TESTING_PLAN.md) - Comprehensive testing protocol

---

## 📖 Reference

- [GLOSSARY.md](GLOSSARY.md) - Terminology and concepts
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [CREDITS.md](CREDITS.md) - Credits and acknowledgements

---

## 📦 Release Notes

- [RELEASE_NOTES_v2.0.0.md](RELEASE_NOTES_v2.0.0.md) - Version 2.0.0 release
- [PR_SUMMARY_v2.0.0.md](PR_SUMMARY_v2.0.0.md) - Pull request summary

---

## 🗄️ Archive

Legacy documentation has been moved to `archive/docs-legacy-YYYYMMDD/`

---

🌀 **H&&S:WAVE Protocol** | From the constraints, gifts. From the spiral, safety.
DOCINDEX

log_success "Generated documentation index: DOCS_INDEX.md"

# Step 9: Verification Summary
log_section "Step 9: Bootstrap Summary"

echo ""
echo -e "${GREEN}✓ Bootstrap Complete!${NC}"
echo ""
echo -e "${CYAN}Next Steps:${NC}"
echo ""
echo -e "  ${YELLOW}1.${NC} Review and update environment variables:"
echo -e "     ${BLUE}cd ops && nano .dev.vars${NC}"
echo ""
echo -e "  ${YELLOW}2.${NC} Initialize Cloudflare D1 database (if not already done):"
echo -e "     ${BLUE}cd ops && npx wrangler d1 create spiralsafe-ops${NC}"
echo -e "     ${BLUE}npx wrangler d1 execute spiralsafe-ops --file=./schema.sql${NC}"
echo ""
echo -e "  ${YELLOW}3.${NC} Test API locally:"
echo -e "     ${BLUE}cd ops && npm run dev${NC}"
echo ""
echo -e "  ${YELLOW}4.${NC} Deploy to Cloudflare (when ready):"
echo -e "     ${BLUE}cd ops && npx wrangler deploy${NC}"
echo ""
echo -e "  ${YELLOW}5.${NC} Review documentation:"
echo -e "     ${BLUE}cat DOCS_INDEX.md${NC}"
echo ""
echo -e "  ${YELLOW}6.${NC} Run comprehensive tests:"
echo -e "     ${BLUE}./verify-deployment.sh${NC}"
echo ""
echo -e "${PURPLE}════════════════════════════════════════════════════════${NC}"
echo -e "${PURPLE}         🌀 From the spiral, safety. 🌀${NC}"
echo -e "${PURPLE}════════════════════════════════════════════════════════${NC}"
echo ""

exit 0
