# GitHub Copilot Custom Instructions for SpiralSafe

> **Note:** This is a supplementary detailed reference. For quick start guidance, see `../.github/copilot-instructions.md`.
> This file contains comprehensive code patterns, examples, and anti-patterns for working with the KENL ecosystem.

## Repository Context

This is the **SpiralSafe** repository - a knowledge management system implementing the KENL ecosystem frameworks:
- **ATOM** (Adaptive Transformation Operations Matrix) - Decision tracking
- **AWI** (Adaptive Workflow Intelligence) - Permission and workflow management
- **SAIF** (Structured, Actionable, Illustrated, Feedback) - Documentation standard
- **KENL** (Knowledge Exchange & Network Learning) - Knowledge relay system
- **Safe Spiral** - Organizational framework for collaborative intelligence

## Core Principles

When generating code or suggestions, always follow these principles:

### 1. Visible State
- All decisions must be logged with ATOM tags
- Use `scripts/atom-track.sh TYPE "description" [file]` for tracking
- State changes should be observable in git history
- Create decision files in `.atom-trail/decisions/`

### 2. Clear Intent
- Document WHY, not just WHAT
- Include ATOM tags in commits: `ATOM-TYPE-YYYYMMDD-NNN-description`
- Reference decision history in code comments
- Use explicit error messages with recovery steps

### 3. Natural Decomposition
- Scripts should do ONE thing well
- Fail fast with clear error messages
- Use graceful degradation (warn, don't fail when possible)
- Dependencies should be explicit and checkable

### 4. Networked Learning
- Documentation enriches through use
- Include examples in all scripts
- Reference related files and decisions
- Build on existing patterns

### 5. Measurable Delivery
- Scripts must have testable exit codes
- Include verification steps
- Log all actions to `.claude/logs/*.jsonl`
- Provide clear success/failure indicators

## Code Style Guidelines

### Shell Scripts
```bash
#!/usr/bin/env bash
set -euo pipefail  # Always use strict mode

# Function example
function_name() {
  local param="$1"
  
  # Validate inputs
  if [ -z "$param" ]; then
    echo "ERROR: parameter required" >&2
    return 1
  fi
  
  # Graceful checks
  if ! command -v sometool >/dev/null 2>&1; then
    echo "WARNING: sometool not available, skipping..." >&2
    return 0
  fi
  
  # Do work...
}
```

### PowerShell Scripts
```powershell
#Requires -Version 5.1
[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Use Write-Host for user output
# Use Write-Verbose for debug
# Use Write-Error for errors
```

### Markdown Documentation
- Use ATOM tags in headers: `## Feature Name (ATOM-DOC-YYYYMMDD-NNN)`
- Include "Tomorrow Test" - can someone use this tomorrow?
- Provide concrete examples
- Link to related documents
- Use visual ASCII diagrams where helpful

## Secrets Management

### NEVER commit:
- API keys, tokens, passwords
- `.env` files with sensitive data
- SSH keys or certificates
- Database connection strings with credentials
- Any `*secret*`, `*password*`, `*token*` named files

### ALWAYS use:
- GitHub Secrets for CI/CD
- `.env.example` files with placeholders
- `scripts/redact-log.sh` before sharing logs
- Environment variables for runtime secrets

### Secret Patterns to Detect:
```regex
(password|passwd|pwd|secret|token|api[_-]?key|private[_-]?key)[\s]*[=:]\s*['\"]?[\w\-]+['\"]?
```

## ATOM Tagging Convention

Format: `ATOM-TYPE-YYYYMMDD-NNN-description`

Types:
- **INIT** - Initial setup or bootstrap
- **FEATURE** - New functionality
- **FIX** - Bug fixes
- **DOC** - Documentation changes
- **REFACTOR** - Code improvements
- **TEST** - Test additions
- **DECISION** - Architectural decisions
- **RELEASE** - Version releases
- **TASK** - General tasks

Example: `ATOM-FEATURE-20260102-001-add-ci-workflow`

## Testing Requirements

All code must be:
1. **Shellcheck validated** (for bash scripts)
2. **Syntax checked** with `bash -n`
3. **Executable** with proper permissions
4. **Documented** with usage examples
5. **Idempotent** when possible (safe to run multiple times)

Use `scripts/test-scripts.sh` to validate all shell scripts.

## Workflow Integration

### Before committing:
```bash
# Validate scripts
./scripts/test-scripts.sh

# Create ATOM tag
./scripts/atom-track.sh FEATURE "Your change description" "path/to/file"

# Verify environment
./scripts/verify-environment.sh

# Update freshness (if old decisions changed)
./scripts/update-freshness.sh
```

### Commit message format:
```
ATOM-TYPE-YYYYMMDD-NNN: Brief description

Longer explanation if needed.

- Bullet points for specifics
- Reference related ATOM tags
- Note any breaking changes
```

## Common Patterns

### Script Header Template:
```bash
#!/usr/bin/env bash
# Purpose: One line description
# Usage: script-name.sh [OPTIONS] REQUIRED_ARG
# Example: script-name.sh --verbose input.txt
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
```

### Error Handling:
```bash
# Graceful degradation
if ! command -v optional_tool >/dev/null 2>&1; then
  echo "WARNING: optional_tool not found, skipping optional feature" >&2
fi

# Hard requirement
if ! command -v required_tool >/dev/null 2>&1; then
  echo "ERROR: required_tool not found. Install with: apt install required_tool" >&2
  exit 1
fi
```

### Logging Pattern:
```bash
log_action() {
  local action="$1"
  local details="$2"
  local timestamp
  timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  
  # Log to JSONL
  echo "{\"timestamp\":\"$timestamp\",\"action\":\"$action\",\"details\":\"$details\"}" >> .claude/logs/actions.jsonl
}
```

## MCP Server Configuration

This repository can integrate with Model Context Protocol servers:

### GitHub MCP Server
- Use for repository operations
- Query issues, PRs, workflows
- Access commit history

### File System MCP Server  
- Navigate repository structure
- Read/write files with ATOM tracking
- Search codebase

### Custom KENL MCP Server (future)
- Query ATOM trail
- Analyze decision patterns
- Generate framework documentation

## Anti-Patterns to Avoid

❌ **Don't:**
- Assume tools are installed (always check)
- Use `sudo` without explicit permission in bump.md
- Write to production paths without validation
- Commit without ATOM tags
- Create scripts without usage examples
- Use hard-coded paths (use relative or discovered paths)
- Mix concerns (one script = one responsibility)

✅ **Do:**
- Check dependencies gracefully
- Provide clear error messages
- Log all state changes
- Use ATOM tracking for decisions
- Include usage examples
- Make scripts idempotent
- Follow existing patterns

## Questions to Ask Before Generating Code

1. Does this follow the Five Core Principles?
2. Is the state change visible and logged?
3. Can this fail gracefully?
4. Is the intent clear from the code/comments?
5. Will this work "tomorrow" without context?
6. Is there an existing pattern to follow?
7. Does this need an ATOM decision tag?

## Resources

- `.claude/ORIENTATION.md` - Quick start guide
- `bump.md` - Current task specification
- `scripts/atom-track.sh` - Decision logging
- `SAFE_SPIRAL_MASTER_INDEX.md` - Framework overview
- `07_FAILURE_MODES_AND_RECOVERY.md` - Error handling patterns

---

**Remember:** Code is a conversation with future developers. Make it clear, make it safe, make it traceable.

*"Information enriches through relay"* - Safe Spiral Principle
