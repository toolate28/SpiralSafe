#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# SpiralSafe GitHub Labels Setup
# Creates all required labels for Dependabot, SYNAPSE, and SPHINX
# ═══════════════════════════════════════════════════════════════
#
# ATOM: ATOM-TASK-20260120-001-setup-github-labels
# H&&S: Autonomous maintenance lattice
#
# Usage:
#   ./scripts/setup-github-labels.sh [--dry-run]
#
# Prerequisites:
#   - GitHub CLI (gh) installed and authenticated
#   - Repository owner and name in environment or detected from git
#
# Label Categories:
#   1. Dependabot labels (dependencies, automated, cascade-stage-1, etc.)
#   2. Issue template labels (bug, enhancement, documentation, etc.)
#   3. Workflow labels (atom-tagged, etc.)
#   4. SYNAPSE framework labels (synapse, sphinx-gate, etc.)
#   5. Protocol labels (wave, bump, coherence, etc.)
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DRY_RUN=false
VERBOSE=false

# Parse arguments
for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --list-labels)
            # Output labels in machine-readable format (one per line, names only)
            cat << 'EOF' | sed 's/"\([^|]*\)|.*/\1/' | sort
"dependencies|0366d6|Dependency updates from Dependabot"
"automated|1d76db|Automated processes and workflows"
"cascade-stage-1|7057ff|Vortex Cascade Collapse Stage 1"
"github-actions|000000|GitHub Actions workflow updates"
"ops|d4c5f9|Operations and infrastructure"
"python|3572A5|Python dependency updates"
"bug|d73a4a|Something isn't working"
"enhancement|a2eeef|New feature or request"
"documentation|0075ca|Improvements or additions to documentation"
"task|fbca04|Task or chore that needs to be done"
"needs-atom-tag|ededed|Requires ATOM tag assignment"
"atom-tagged|c2e0c6|Has been assigned an ATOM tag"
"synapse|9C27B0|SYNAPSE visualization framework"
"sphinx-gate|673AB7|SPHINX protocol gate verification"
"wave-protocol|3F51B5|WAVE coherence protocol"
"bump-protocol|2196F3|BUMP handoff protocol"
"atom-protocol|00BCD4|ATOM tagging protocol"
"coherence|00E676|Coherence metrics and quality"
"testing|795548|Testing and quality assurance"
"security|B71C1C|Security vulnerabilities and fixes"
"in-progress|FFC107|Work in progress"
"review-needed|FF9800|Needs review"
"blocked|E91E63|Blocked by external dependency"
"claude:help|512DA8|Claude AI assistance requested"
"copilot:review|1976D2|GitHub Copilot review requested"
"H&&S:WAVE|00ACC1|Hope&&Sauced soft handoff"
"H&&S:PASS|00897B|Hope&&Sauced ownership transfer"
"H&&S:SYNC|0097A7|Hope&&Sauced synchronization"
"H&&S:BLOCK|D32F2F|Hope&&Sauced blocking issue"
EOF
            exit 0
            ;;
        --help|-h)
            echo "Usage: $0 [--dry-run] [--verbose] [--list-labels]"
            echo ""
            echo "Creates all required GitHub labels for SpiralSafe repository."
            echo ""
            echo "Options:"
            echo "  --dry-run      Show what would be created without making changes"
            echo "  --verbose      Show detailed output"
            echo "  --list-labels  Output label names only (machine-readable)"
            echo "  --help         Show this help message"
            exit 0
            ;;
    esac
done

# Check for gh CLI
if ! command -v gh &> /dev/null; then
    echo -e "${RED}ERROR: GitHub CLI (gh) is not installed.${NC}"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check authentication
if ! gh auth status &> /dev/null; then
    echo -e "${RED}ERROR: GitHub CLI is not authenticated.${NC}"
    echo "Run: gh auth login"
    exit 1
fi

# Get repository info
REPO_OWNER=$(gh repo view --json owner -q .owner.login 2>/dev/null || echo "")
REPO_NAME=$(gh repo view --json name -q .name 2>/dev/null || echo "")

if [ -z "$REPO_OWNER" ] || [ -z "$REPO_NAME" ]; then
    echo -e "${RED}ERROR: Could not determine repository information.${NC}"
    echo "Make sure you're in a git repository with a GitHub remote."
    exit 1
fi

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     SpiralSafe GitHub Labels Setup                   ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Repository: ${GREEN}${REPO_OWNER}/${REPO_NAME}${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "Mode: ${YELLOW}DRY RUN${NC} (no changes will be made)"
fi
echo ""

# Label definitions
# Format: "name|color|description"
declare -a LABELS=(
    # Dependabot labels (from .github/dependabot.yml)
    "dependencies|0366d6|Dependency updates from Dependabot"
    "automated|1d76db|Automated processes and workflows"
    "cascade-stage-1|7057ff|Vortex Cascade Collapse Stage 1"
    "github-actions|000000|GitHub Actions workflow updates"
    "ops|d4c5f9|Operations and infrastructure"
    "python|3572A5|Python dependency updates"
    
    # Issue template labels
    "bug|d73a4a|Something isn't working"
    "enhancement|a2eeef|New feature or request"
    "documentation|0075ca|Improvements or additions to documentation"
    "task|fbca04|Task or chore that needs to be done"
    "needs-atom-tag|ededed|Requires ATOM tag assignment"
    "atom-tagged|c2e0c6|Has been assigned an ATOM tag"
    
    # SYNAPSE framework labels
    "synapse|9C27B0|SYNAPSE visualization framework"
    "sphinx-gate|673AB7|SPHINX protocol gate verification"
    "wave-protocol|3F51B5|WAVE coherence protocol"
    "bump-protocol|2196F3|BUMP handoff protocol"
    "atom-protocol|00BCD4|ATOM tagging protocol"
    
    # Quality and coherence labels
    "coherence|00E676|Coherence metrics and quality"
    "testing|795548|Testing and quality assurance"
    "security|B71C1C|Security vulnerabilities and fixes"
    
    # Workflow state labels
    "in-progress|FFC107|Work in progress"
    "review-needed|FF9800|Needs review"
    "blocked|E91E63|Blocked by external dependency"
    
    # Agent coordination labels
    "claude:help|512DA8|Claude AI assistance requested"
    "copilot:review|1976D2|GitHub Copilot review requested"
    
    # Special protocol labels
    "H&&S:WAVE|00ACC1|Hope&&Sauced soft handoff"
    "H&&S:PASS|00897B|Hope&&Sauced ownership transfer"
    "H&&S:SYNC|0097A7|Hope&&Sauced synchronization"
    "H&&S:BLOCK|D32F2F|Hope&&Sauced blocking issue"
)

# Statistics
CREATED=0
UPDATED=0
SKIPPED=0
FAILED=0

# Process all labels
echo -e "${BLUE}Processing labels...${NC}"
echo ""

# Fetch all existing labels once for efficiency (O(1) API call instead of O(n))
echo -e "${BLUE}Fetching existing labels...${NC}"
EXISTING_LABELS=$(gh label list --limit 1000 --json name --jq '.[].name' 2>/dev/null || echo "")

for label_def in "${LABELS[@]}"; do
    IFS='|' read -r name color description <<< "$label_def"
    
    if [ "$VERBOSE" = true ]; then
        echo -e "Processing: ${BLUE}${name}${NC}"
    fi
    
    # Check if label exists in our cached list
    if echo "$EXISTING_LABELS" | grep -q "^${name}$"; then
        # Label exists, update it
        if [ "$DRY_RUN" = true ]; then
            echo -e "  ${YELLOW}Would update:${NC} ${name}"
            ((SKIPPED++))
        else
            if gh label edit "$name" --color "$color" --description "$description" 2>/dev/null; then
                echo -e "  ${GREEN}✓ Updated:${NC} ${name}"
                ((UPDATED++))
            else
                echo -e "  ${RED}✗ Failed to update:${NC} ${name}"
                ((FAILED++))
            fi
        fi
    else
        # Label doesn't exist, create it
        if [ "$DRY_RUN" = true ]; then
            echo -e "  ${YELLOW}Would create:${NC} ${name}"
            ((SKIPPED++))
        else
            if gh label create "$name" --color "$color" --description "$description" 2>/dev/null; then
                echo -e "  ${GREEN}✓ Created:${NC} ${name}"
                ((CREATED++))
            else
                echo -e "  ${RED}✗ Failed to create:${NC} ${name}"
                ((FAILED++))
            fi
        fi
    fi
done

# Summary
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "Would create: ${YELLOW}${SKIPPED}${NC} labels"
else
    echo -e "Created:      ${GREEN}${CREATED}${NC}"
    echo -e "Updated:      ${GREEN}${UPDATED}${NC}"
    if [ "$FAILED" -gt 0 ]; then
        echo -e "Failed:       ${RED}${FAILED}${NC}"
    fi
fi
echo ""

# Exit with appropriate code
if [ "$FAILED" -gt 0 ]; then
    exit 1
else
    echo -e "${GREEN}✓ Label setup complete!${NC}"
    exit 0
fi
