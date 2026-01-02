#!/usr/bin/env bash
# MCP Server Healthcheck
# Validates Docker, Node.js, environment variables, and MCP configuration
set -euo pipefail

EXIT_CODE=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║                MCP Server Healthcheck                      ║"
echo "║                  ◉──◉───◉───◉──◉                           ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check 1: Docker availability
echo -e "${BLUE}[1/7]${NC} Checking Docker availability..."
if command -v docker >/dev/null 2>&1; then
  if docker ps >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Docker is available and running"
  else
    echo -e "${RED}✗${NC} Docker is installed but not running"
    echo "  → Start Docker Desktop or run: sudo systemctl start docker"
    EXIT_CODE=1
  fi
else
  echo -e "${RED}✗${NC} Docker is not installed"
  echo "  → Install from: https://docs.docker.com/get-docker/"
  EXIT_CODE=1
fi
echo ""

# Check 2: GitHub MCP image pullability
echo -e "${BLUE}[2/7]${NC} Checking GitHub MCP Docker image..."
if command -v docker >/dev/null 2>&1 && docker ps >/dev/null 2>&1; then
  if docker pull mcp/github:latest >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} GitHub MCP image is pullable"
  else
    echo -e "${YELLOW}⚠${NC} Cannot pull mcp/github:latest"
    echo "  → Check Docker Hub status or network connectivity"
    echo "  → Try manually: docker pull mcp/github:latest"
    # Not fatal - image might already exist locally
  fi
else
  echo -e "${YELLOW}⚠${NC} Skipping image pull check (Docker not available)"
fi
echo ""

# Check 3: Node.js availability
echo -e "${BLUE}[3/7]${NC} Checking Node.js availability..."
if command -v node >/dev/null 2>&1; then
  NODE_VERSION=$(node --version)
  echo -e "${GREEN}✓${NC} Node.js is available: $NODE_VERSION"
  
  # Check if version is 18+ (recommended for MCP)
  NODE_MAJOR=$(echo "$NODE_VERSION" | cut -d'.' -f1 | sed 's/v//')
  if [ "$NODE_MAJOR" -ge 18 ]; then
    echo "  → Version is compatible with MCP"
  else
    echo -e "${YELLOW}⚠${NC} Node.js version is older than recommended (18+)"
    echo "  → Consider upgrading for best compatibility"
  fi
else
  echo -e "${RED}✗${NC} Node.js is not installed"
  echo "  → Install from: https://nodejs.org/"
  EXIT_CODE=1
fi
echo ""

# Check 4: npx availability
echo -e "${BLUE}[4/7]${NC} Checking npx availability..."
if command -v npx >/dev/null 2>&1; then
  NPX_VERSION=$(npx --version)
  echo -e "${GREEN}✓${NC} npx is available: $NPX_VERSION"
else
  echo -e "${RED}✗${NC} npx is not available"
  echo "  → Usually comes with Node.js - try reinstalling Node.js"
  EXIT_CODE=1
fi
echo ""

# Check 5: Environment variables
echo -e "${BLUE}[5/7]${NC} Checking environment variables..."
if [ -n "${GITHUB_PERSONAL_ACCESS_TOKEN:-}" ]; then
  # Mask token for security - use bash substring for portability
  TOKEN_LENGTH=${#GITHUB_PERSONAL_ACCESS_TOKEN}
  if [ "$TOKEN_LENGTH" -gt 8 ]; then
    MASKED_TOKEN="${GITHUB_PERSONAL_ACCESS_TOKEN:0:8}..."
  else
    MASKED_TOKEN="***"
  fi
  echo -e "${GREEN}✓${NC} GITHUB_PERSONAL_ACCESS_TOKEN is set: $MASKED_TOKEN"
  
  # Test token validity
  if command -v curl >/dev/null 2>&1; then
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
      -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" \
      https://api.github.com/user 2>&1 || echo "000")
    
    if [ "$RESPONSE" = "200" ]; then
      echo "  → Token is valid"
    elif [ "$RESPONSE" = "401" ]; then
      echo -e "${RED}✗${NC} Token is invalid or expired"
      echo "  → Regenerate at: https://github.com/settings/tokens"
      EXIT_CODE=1
    elif [ "$RESPONSE" = "000" ]; then
      echo -e "${YELLOW}⚠${NC} Cannot validate token (network issue)"
    else
      echo -e "${YELLOW}⚠${NC} Unexpected response code: $RESPONSE"
    fi
  fi
else
  echo -e "${RED}✗${NC} GITHUB_PERSONAL_ACCESS_TOKEN is not set"
  echo "  → Set with: export GITHUB_PERSONAL_ACCESS_TOKEN='ghp_your_token_here'"
  echo "  → Generate token at: https://github.com/settings/tokens"
  EXIT_CODE=1
fi
echo ""

# Check 6: MCP configuration file
echo -e "${BLUE}[6/7]${NC} Checking MCP configuration..."
MCP_CONFIG=".claude/mcp-servers.json"
if [ -f "$MCP_CONFIG" ]; then
  echo -e "${GREEN}✓${NC} MCP configuration file exists: $MCP_CONFIG"
  
  # Validate JSON syntax
  if command -v jq >/dev/null 2>&1; then
    if jq empty "$MCP_CONFIG" >/dev/null 2>&1; then
      echo "  → JSON syntax is valid"
      
      # Check for hardcoded secrets
      if grep -q "ghp_\|github_pat_" "$MCP_CONFIG" 2>/dev/null; then
        echo -e "${RED}✗${NC} WARNING: Hardcoded GitHub token found in config!"
        echo "  → Remove hardcoded tokens and use environment variables"
        EXIT_CODE=1
      fi
    else
      echo -e "${RED}✗${NC} JSON syntax is invalid"
      echo "  → Fix syntax errors in $MCP_CONFIG"
      EXIT_CODE=1
    fi
  else
    echo -e "${YELLOW}⚠${NC} Cannot validate JSON (jq not installed)"
    echo "  → Install jq to enable validation"
  fi
else
  echo -e "${YELLOW}⚠${NC} MCP configuration file not found: $MCP_CONFIG"
  echo "  → This is expected if MCP is not configured yet"
fi
echo ""

# Check 7: Test MCP server connectivity
echo -e "${BLUE}[7/7]${NC} Testing MCP server connectivity..."
if command -v docker >/dev/null 2>&1 && docker ps >/dev/null 2>&1 && [ -n "${GITHUB_PERSONAL_ACCESS_TOKEN:-}" ]; then
  echo "  Testing GitHub MCP server..."
  # Note: Skipping actual token test to avoid exposing credentials to potentially untrusted images
  # Users should verify manually: docker run --rm -i -e GITHUB_PERSONAL_ACCESS_TOKEN mcp/github
  if docker image inspect mcp/github:latest >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} GitHub MCP image is available locally"
  else
    echo -e "${YELLOW}⚠${NC} GitHub MCP image not found locally"
    echo "  → Pull manually: docker pull mcp/github:latest"
    echo "  → Test manually: docker run --rm -i -e GITHUB_PERSONAL_ACCESS_TOKEN mcp/github"
  fi
else
  echo -e "${YELLOW}⚠${NC} Skipping connectivity test (prerequisites not met)"
fi

if command -v npx >/dev/null 2>&1; then
  echo "  Testing Mermaid MCP server..."
  if timeout 10s npx -y @modelcontextprotocol/server-mermaid --version >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Mermaid MCP server is accessible"
  else
    echo -e "${YELLOW}⚠${NC} Mermaid MCP server test failed"
    echo "  → May be a network issue - check npm connectivity"
  fi
else
  echo -e "${YELLOW}⚠${NC} Skipping Mermaid test (npx not available)"
fi
echo ""

# Summary
echo "════════════════════════════════════════════════════════════"
if [ $EXIT_CODE -eq 0 ]; then
  echo -e "${GREEN}✓ All checks passed!${NC}"
  echo ""
  echo "MCP is ready to use. Start Claude Desktop and ask:"
  echo "  \"Can you list the recent issues in this repository?\""
else
  echo -e "${RED}✗ Some checks failed${NC}"
  echo ""
  echo "Fix the issues above and run this script again."
  echo "For detailed troubleshooting, see: docs/TROUBLESHOOTING_MCP.md"
fi
echo "════════════════════════════════════════════════════════════"

exit $EXIT_CODE
