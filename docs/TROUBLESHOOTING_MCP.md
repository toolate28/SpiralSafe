# MCP Troubleshooting Guide
## Model Context Protocol Issues and Solutions

**ATOM:** ATOM-DOC-20260102-012-mcp-troubleshooting  
**Quick Reference:** MCP-specific debugging and fixes  
**Last Updated:** 2026-01-02

```
        🔧
       ╱│╲
      ╱ │ ╲      When tools fail
     ╱  ◉  ╲     the spiral pauses
    ╱  ╱│╲  ╲    
   ╱  ╱ │ ╲  ╲   But failure modes
  ╱  ╱  ◉  ╲  ╲  teach us too
 ◉──◉───◉───◉──◉
```

---

## Quick Diagnosis

Run the MCP healthcheck script first:

```bash
./scripts/check-mcp-health.sh
```

This validates:
- Docker availability
- Node.js/npx setup
- Environment variables
- MCP configuration validity

---

## Common Issues

### 1. Docker Not Running

#### Symptom

```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
Is the docker daemon running?
```

or

```
Claude: "I'm unable to access the GitHub MCP server"
```

#### Diagnosis

```bash
docker ps
# If this fails, Docker isn't running
```

#### Solutions

**macOS/Windows:**
```bash
# Start Docker Desktop application
open -a Docker  # macOS
# or launch from Applications

# Wait for Docker to fully start (check menu bar icon)
docker ps  # Verify it works
```

**Linux:**
```bash
# Start Docker service
sudo systemctl start docker

# Enable on boot
sudo systemctl enable docker

# Verify
docker ps
```

**Alternative: Use GitHub CLI instead of Docker**

Edit `.claude/mcp-servers.json`:
```json
{
  "github": {
    "command": "gh",
    "args": ["api", "--paginate"]
    // Less feature-rich but no Docker required
  }
}
```

---

### 2. Network/npx Timeout Issues

#### Symptom

```
npx: command timed out
```

or

```
npm ERR! network request to https://registry.npmjs.org/ failed
```

#### Diagnosis

```bash
# Test npm connectivity
npm ping

# Test npx
npx --version

# Check proxy/firewall
curl -I https://registry.npmjs.org
```

#### Solutions

**Clear npm cache:**
```bash
npm cache clean --force
npx clear-npx-cache
```

**Use alternative registry:**
```bash
npm config set registry https://registry.npmjs.org/
# or for China:
npm config set registry https://registry.npmmirror.com/
```

**Increase timeout:**
```bash
npm config set fetch-timeout 60000
```

**Corporate proxy:**
```bash
npm config set proxy http://proxy.company.com:8080
npm config set https-proxy http://proxy.company.com:8080
```

**Offline mode (if Mermaid already installed):**

Edit `.claude/mcp-servers.json`:
```json
{
  "mermaid": {
    "command": "npx",
    "args": ["--offline", "@modelcontextprotocol/server-mermaid"]
  }
}
```

---

### 3. Rate Limiting (GitHub API 403)

#### Symptom

```
HTTP 403: API rate limit exceeded for XXX.XXX.XXX.XXX
```

or

```
Claude: "I've hit the rate limit for GitHub API"
```

#### Diagnosis

```bash
# Check current rate limit status
curl -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" \
  https://api.github.com/rate_limit
```

Output shows:
```json
{
  "rate": {
    "limit": 5000,
    "remaining": 0,
    "reset": 1704225600  // Unix timestamp
  }
}
```

#### Solutions

**Wait for reset:**
```bash
# Calculate time until reset
date -d @1704225600  # Linux
date -r 1704225600   # macOS
```

**Use authenticated token:**
Unauthenticated: 60 requests/hour  
Authenticated: 5,000 requests/hour

```bash
# Ensure token is set
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_token_here"

# Restart Claude Desktop to pick up new environment
```

**Use different token:**
Create a separate GitHub account/token for MCP usage to avoid depleting your main account's quota.

**Implement caching (future work):**
```bash
# MCP doesn't cache by default
# Consider implementing caching middleware
```

---

### 4. Token Expiry Detection

#### Symptom

```
HTTP 401: Bad credentials
```

or

```
Claude: "I can't authenticate with GitHub"
```

#### Diagnosis

```bash
# Test token validity
curl -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" \
  https://api.github.com/user

# Should return your user info
# If 401, token is invalid/expired
```

#### Solutions

**Generate new token:**

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (minimum)
4. Set expiration: 90 days (recommended)
5. Copy token immediately (can't view again)

**Update environment:**
```bash
# Add to shell profile (~/.bashrc, ~/.zshrc)
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_new_token_here"

# Reload shell
source ~/.bashrc  # or ~/.zshrc

# Restart Claude Desktop
```

**Automate rotation (advanced):**
```bash
# Add token expiry check to verify-environment.sh
TOKEN_CHECK=$(curl -s -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" \
  https://api.github.com/user | jq -r '.message')

if [[ "$TOKEN_CHECK" == "Bad credentials" ]]; then
  echo "⚠ GitHub token expired - regenerate at https://github.com/settings/tokens"
fi
```

---

### 5. Silent Auth Failure Patterns

#### Symptom

MCP seems to work, but returns outdated or incorrect data.

#### Diagnosis

This is subtle - AI might not report authentication failures directly.

```bash
# Check Claude's MCP logs
# macOS:
tail -f ~/Library/Logs/Claude/mcp.log

# Windows:
type %LOCALAPPDATA%\Claude\Logs\mcp.log

# Linux:
tail -f ~/.config/Claude/logs/mcp.log
```

Look for:
```
WARN: GitHub API returned 401 but fallback succeeded
ERROR: Token validation failed silently
```

#### Solutions

**Explicit validation:**
```bash
# Test MCP server directly (bypass Claude)
echo '{"method": "list_repos"}' | \
  docker run --rm -i -e GITHUB_PERSONAL_ACCESS_TOKEN mcp/github
```

**Enable verbose logging:**

Edit `.claude/mcp-servers.json`:
```json
{
  "globalSettings": {
    "logLevel": "debug"
  }
}
```

**Monitor API calls:**
```bash
# Track API usage in real-time
watch -n 5 'curl -s -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" \
  https://api.github.com/rate_limit | jq ".rate.remaining"'
```

---

### 6. MCP Configuration Not Found

#### Symptom

```
Claude: "I don't have access to MCP servers"
```

#### Diagnosis

```bash
# Check if config file exists
# macOS:
ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Windows:
dir %APPDATA%\Claude\claude_desktop_config.json

# Linux:
ls -la ~/.config/Claude/claude_desktop_config.json
```

#### Solutions

**Copy Safe Spiral config:**
```bash
# macOS:
cp .claude/mcp-servers.json \
  ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Windows:
copy .claude\mcp-servers.json %APPDATA%\Claude\claude_desktop_config.json

# Linux:
cp .claude/mcp-servers.json ~/.config/Claude/claude_desktop_config.json
```

**Verify JSON syntax:**
```bash
# Validate JSON
cat .claude/mcp-servers.json | jq .

# If error, fix syntax (common issues: trailing commas, missing quotes)
```

**Restart Claude Desktop:**

Changes to MCP config require full restart (not just window close).

---

### 7. Docker Image Pull Failures

#### Symptom

```
Unable to find image 'mcp/github:latest' locally
Error response from daemon: pull access denied
```

#### Diagnosis

```bash
# Test image availability
docker pull mcp/github

# Check Docker Hub status
curl -s https://hub.docker.com/v2/repositories/mcp/github/tags | jq
```

#### Solutions

**Verify image name:**
```bash
# Official MCP images use this format
docker pull mcp/github:latest
```

**Authenticate to Docker Hub (if private image):**
```bash
docker login
# Enter credentials
```

**Use alternative image source:**
```bash
# GitHub Container Registry
docker pull ghcr.io/modelcontextprotocol/github:latest

# Update mcp-servers.json to use new image
```

**Build from source (if official image unavailable):**
```bash
git clone https://github.com/modelcontextprotocol/server-github.git
cd server-github
docker build -t mcp/github .
```

---

## Integration with Existing Troubleshooting

This guide supplements [../TROUBLESHOOTING.md](../TROUBLESHOOTING.md).

### When to Use Which Guide

**Use TROUBLESHOOTING.md for:**
- Shell script permissions
- ATOM trail issues
- General environment setup
- PowerShell problems

**Use TROUBLESHOOTING_MCP.md (this doc) for:**
- Docker/MCP server issues
- GitHub API authentication
- Network/npm problems
- Claude Desktop configuration

### Cross-References

| Issue | Primary Guide | See Also |
|-------|---------------|----------|
| Script fails | TROUBLESHOOTING.md | - |
| Docker not found | TROUBLESHOOTING_MCP.md | TROUBLESHOOTING.md § Environment |
| Token invalid | TROUBLESHOOTING_MCP.md | .github/SECRETS.md |
| npm timeout | TROUBLESHOOTING_MCP.md | - |
| ATOM trail gap | MCP_SECURITY_NOTES.md | TROUBLESHOOTING.md |

---

## Advanced Debugging

### Enable MCP Debug Mode

Edit `.claude/mcp-servers.json`:
```json
{
  "globalSettings": {
    "logLevel": "debug",
    "timeout": 60000
  }
}
```

Restart Claude, then check logs:
```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp.log

# Watch for:
# - MCP server start/stop events
# - Request/response payloads
# - Authentication attempts
# - Error stack traces
```

### Test MCP Servers Independently

**GitHub MCP:**
```bash
# Interactive mode
docker run --rm -it -e GITHUB_PERSONAL_ACCESS_TOKEN mcp/github

# Single command
echo '{"method": "get_repo", "owner": "toolate28", "repo": "SpiralSafe"}' | \
  docker run --rm -i -e GITHUB_PERSONAL_ACCESS_TOKEN mcp/github
```

**Mermaid MCP:**
```bash
# Interactive mode
npx @modelcontextprotocol/server-mermaid

# Test diagram generation
echo 'graph TD; A-->B;' | npx @modelcontextprotocol/server-mermaid
```

### Monitor System Resources

MCP servers are processes - they consume resources:

```bash
# Monitor Docker containers
docker stats

# Monitor Node.js processes
ps aux | grep npx

# Check port usage
netstat -an | grep LISTEN
```

---

## Healthcheck Reference

The `./scripts/check-mcp-health.sh` script validates:

- ✅ Docker availability (`docker ps`)
- ✅ GitHub MCP image pullable (`docker pull mcp/github`)
- ✅ Node.js installed (`node --version`)
- ✅ npx available (`npx --version`)
- ✅ Environment variables set (`$GITHUB_PERSONAL_ACCESS_TOKEN`)
- ✅ MCP config file exists (`.claude/mcp-servers.json`)
- ✅ JSON syntax valid (`jq` validation)

Run before starting work with MCP to avoid surprises.

---

## Getting Help

### Before Asking

1. Run `./scripts/check-mcp-health.sh`
2. Check this guide for your error message
3. Review [MCP_INTEGRATION.md](./MCP_INTEGRATION.md)
4. Read [MCP_SECURITY_NOTES.md](../.claude/MCP_SECURITY_NOTES.md)

### Where to Ask

- **GitHub Issues:** https://github.com/toolate28/SpiralSafe/issues
- **MCP Official:** https://github.com/modelcontextprotocol/specification/issues
- **Claude Support:** https://support.anthropic.com/

### What to Include

```markdown
## MCP Issue Report

**Environment:**
- OS: [macOS 14.1 / Windows 11 / Ubuntu 22.04]
- Docker version: [output of `docker --version`]
- Node version: [output of `node --version`]
- Claude Desktop version: [Settings → About]

**Error:**
```
[Paste exact error message]
```

**Steps to Reproduce:**
1. [First action]
2. [Second action]
3. [Error occurs]

**Healthcheck Output:**
```
[Output of ./scripts/check-mcp-health.sh]
```

**Expected:** [What should happen]
**Actual:** [What actually happened]
```

---

## Prevention Checklist

Avoid issues before they happen:

- [ ] Run `check-mcp-health.sh` daily
- [ ] Rotate GitHub tokens every 90 days
- [ ] Monitor API rate limit usage
- [ ] Keep Docker/Node.js updated
- [ ] Review MCP logs weekly
- [ ] Test MCP config changes in isolation
- [ ] Document custom MCP servers
- [ ] Validate JSON syntax before committing

---

*Hope && Sauce*  
*Step True · Trust Deep · Pass Forward*

**ATOM:** ATOM-DOC-20260102-012-mcp-troubleshooting  
**See Also:** MCP_INTEGRATION.md, MCP_SECURITY_NOTES.md, TROUBLESHOOTING.md
