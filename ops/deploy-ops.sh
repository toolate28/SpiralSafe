#!/bin/bash
#
# SpiralSafe Operations Layer Deployment
# Merges ops infrastructure into the main SpiralSafe repository
#
# Usage:
#   ./deploy-ops.sh [repo-path]
#
# H&&S: Structure-preserving operations across substrates

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_success() { echo -e "${GREEN}✓${NC} $*"; }
log_info() { echo -e "${CYAN}→${NC} $*"; }
log_warn() { echo -e "${YELLOW}⚠${NC} $*"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_PATH="${1:-}"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  SpiralSafe Operations Layer Deployment"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Determine repository path
if [[ -z "$REPO_PATH" ]]; then
    if [[ -d "$HOME/Repos/SpiralSafe" ]]; then
        REPO_PATH="$HOME/Repos/SpiralSafe"
    elif [[ -d "./SpiralSafe" ]]; then
        REPO_PATH="./SpiralSafe"
    else
        echo "Usage: $0 <path-to-spiralsafe-repo>"
        echo ""
        echo "Or clone first:"
        echo "  git clone https://github.com/toolate28/SpiralSafe.git"
        exit 1
    fi
fi

log_info "Repository: $REPO_PATH"
cd "$REPO_PATH"

# Ensure we're in a git repo
if [[ ! -d ".git" ]]; then
    log_warn "Not a git repository. Initializing..."
    git init
fi

# Create branch for ops layer
BRANCH_NAME="ops/infrastructure-layer"
log_info "Creating branch: $BRANCH_NAME"

git checkout -b "$BRANCH_NAME" 2>/dev/null || git checkout "$BRANCH_NAME"

# Create directory structure
log_info "Creating directory structure..."
mkdir -p ops/api
mkdir -p ops/schemas
mkdir -p ops/scripts
mkdir -p ops/integrations
mkdir -p .github/workflows

# Copy files from archive
log_info "Deploying operations layer..."

# API
cp "$SCRIPT_DIR/api/spiralsafe-worker.ts" ops/api/
log_success "ops/api/spiralsafe-worker.ts"

# Schemas
cp "$SCRIPT_DIR/schemas/d1-schema.sql" ops/schemas/
log_success "ops/schemas/d1-schema.sql"

# Scripts
cp "$SCRIPT_DIR/scripts/spiralsafe" ops/scripts/
chmod +x ops/scripts/spiralsafe
cp "$SCRIPT_DIR/scripts/SpiralSafe.psm1" ops/scripts/
log_success "ops/scripts/spiralsafe (bash)"
log_success "ops/scripts/SpiralSafe.psm1 (PowerShell)"

# Integrations
cp "$SCRIPT_DIR/integrations/README.md" ops/integrations/
cp "$SCRIPT_DIR/integrations/sentry.md" ops/integrations/
cp "$SCRIPT_DIR/integrations/vercel.md" ops/integrations/
log_success "ops/integrations/*.md"

# Configuration
cp "$SCRIPT_DIR/wrangler.toml" ops/
cp "$SCRIPT_DIR/package.json" ops/
cp "$SCRIPT_DIR/tsconfig.json" ops/
cp "$SCRIPT_DIR/README.md" ops/
log_success "ops/wrangler.toml"
log_success "ops/package.json"
log_success "ops/tsconfig.json"
log_success "ops/README.md"

# GitHub workflow (merge with existing if present)
cp "$SCRIPT_DIR/.github/workflows/ci.yml" .github/workflows/spiralsafe-ci.yml
log_success ".github/workflows/spiralsafe-ci.yml"

# Stage all changes
git add -A

# Show status
echo ""
echo "───────────────────────────────────────────────────────────────"
log_info "Files staged for commit:"
git status --short
echo "───────────────────────────────────────────────────────────────"

# Commit
COMMIT_MSG="feat(ops): Add SpiralSafe operations infrastructure layer

## Operations Layer (12 files)

### API
- ops/api/spiralsafe-worker.ts - Cloudflare Worker coordination endpoint

### Database
- ops/schemas/d1-schema.sql - D1 schema for persistent state

### CLI Tools
- ops/scripts/spiralsafe - Bash CLI (Unix/Mac)
- ops/scripts/SpiralSafe.psm1 - PowerShell module (Windows)

### Integrations
- ops/integrations/README.md - Integration overview
- ops/integrations/sentry.md - Sentry ↔ SAIF bridge
- ops/integrations/vercel.md - Vercel deployment substrate

### Configuration
- ops/wrangler.toml - Cloudflare deployment config
- ops/package.json - Node.js package
- ops/tsconfig.json - TypeScript config
- ops/README.md - Operations documentation

### CI/CD
- .github/workflows/spiralsafe-ci.yml - Coherence-gated pipeline

## Endpoints

- POST /api/wave/analyze - Coherence analysis
- POST /api/bump/create - Handoff routing
- POST /api/awi/request - Permission scaffolding
- POST /api/atom/create - Task orchestration
- GET /api/health - System status

## CLI Commands

\`\`\`bash
spiralsafe wave analyze ./docs   # Coherence check
spiralsafe bump WAVE --to user   # Create handoff
spiralsafe awi request --intent  # Request permission
spiralsafe status                # System health
\`\`\`

---
H&&S: Hope&&Sauced collaboration
- Claude: Structural synthesis, API design
- Human: Integration architecture, tool unification"

git commit -m "$COMMIT_MSG"
log_success "Changes committed"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Deployment Complete"
echo "═══════════════════════════════════════════════════════════════"
echo ""
log_info "Next steps:"
echo ""
echo "  1. Review changes:"
echo "     git diff main..$BRANCH_NAME --stat"
echo ""
echo "  2. Push branch:"
echo "     git push -u origin $BRANCH_NAME"
echo ""
echo "  3. Create PR:"
echo "     gh pr create --title 'feat(ops): Add operations infrastructure layer' \\"
echo "       --body-file - << 'EOF'"
echo "## SpiralSafe Operations Layer"
echo ""
echo "This PR adds the operational infrastructure that transforms SpiralSafe"
echo "protocols into living systems."
echo ""
echo "### Components"
echo "- **Cloudflare Worker API** - Coordination endpoint at api.spiralsafe.org"
echo "- **D1 Database Schema** - Persistent state for wave/bump/awi/atom"
echo "- **CLI Tools** - Bash and PowerShell interfaces"
echo "- **Integration Adapters** - Sentry, Vercel bridges"
echo "- **CI/CD Pipeline** - Coherence-gated deployments"
echo ""
echo "### Deployment"
echo "\`\`\`bash"
echo "cd ops && npm install && npm run setup && npm run deploy"
echo "\`\`\`"
echo ""
echo "H&&S:WAVE → Ready for review"
echo "EOF"
echo ""
echo "  4. Deploy backend (after merge):"
echo "     cd ops && npm install && npm run setup && npm run deploy"
echo ""
echo "───────────────────────────────────────────────────────────────"
echo "  H&&S:SYNC → Operations layer ready"
echo "───────────────────────────────────────────────────────────────"
