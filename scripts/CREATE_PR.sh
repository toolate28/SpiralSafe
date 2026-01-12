#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# Create PR for SpiralSafe Deployment Readiness
# ═══════════════════════════════════════════════════════════════

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  SpiralSafe Deployment Readiness PR Creation                ║${NC}"
echo -e "${BLUE}║  H&&S:WAVE | Hope&&Sauced                                   ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

BRANCH="claude/review-codebase-state-KuPq8"
BASE="main"

echo -e "${YELLOW}Branch:${NC} $BRANCH"
echo -e "${YELLOW}Base:${NC} $BASE"
echo ""

# Read PR description
if [ ! -f "PR_DESCRIPTION.md" ]; then
  echo "ERROR: PR_DESCRIPTION.md not found"
  exit 1
fi

PR_TITLE="🌀 SpiralSafe Deployment Readiness - Ultrathink Analysis & Setup"
PR_BODY=$(cat PR_DESCRIPTION.md)

echo -e "${GREEN}✓${NC} PR description loaded ($(wc -l < PR_DESCRIPTION.md) lines)"
echo ""

# Try gh CLI first
if command -v gh &> /dev/null; then
  echo -e "${BLUE}Creating PR via GitHub CLI...${NC}"
  gh pr create \
    --base "$BASE" \
    --head "$BRANCH" \
    --title "$PR_TITLE" \
    --body-file PR_DESCRIPTION.md \
    --assignee "@me"

  if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ PR created successfully!${NC}"
    gh pr view --web
    exit 0
  fi
fi

# Fallback: provide manual instructions
echo -e "${YELLOW}GitHub CLI not available. Creating PR manually...${NC}"
echo ""
echo "▶ Open this URL in your browser:"
echo ""
echo -e "${GREEN}https://github.com/toolate28/SpiralSafe/compare/main...claude/review-codebase-state-KuPq8${NC}"
echo ""
echo "▶ Or use this shortened command:"
echo ""
echo "  gh pr create --base main --head $BRANCH --title \"$PR_TITLE\" --body-file PR_DESCRIPTION.md"
echo ""
echo "▶ PR will include these commits:"
git log --oneline main..$BRANCH 2>/dev/null || git log --oneline -4
echo ""
echo -e "${BLUE}H&&S:WAVE${NC}"
