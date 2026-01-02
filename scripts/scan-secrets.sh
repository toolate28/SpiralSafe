#!/usr/bin/env bash
# Secrets scanner for the repository
# Scans for common secret patterns and potential leaks
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
EXIT_CODE=0

cd "$REPO_ROOT"

echo "=== Secrets Scanning ==="
echo ""

# Secret patterns to detect
declare -A PATTERNS=(
  ["API Keys"]='(api[_-]?key|apikey)[\s]*[=:]\s*['"'"'"]?[A-Za-z0-9_-]{20,}['"'"'"]?'
  ["AWS Keys"]='(AKIA[0-9A-Z]{16}|aws[_-]?secret[_-]?access[_-]?key)'
  ["Generic Secrets"]='(secret|password|passwd|pwd|token)[\s]*[=:]\s*['"'"'"]?[A-Za-z0-9_!@#$%^&*()-+=]{8,}['"'"'"]?'
  ["Private Keys"]='-----BEGIN[\s\w]*PRIVATE KEY-----'
  ["GitHub Tokens"]='(ghp|ghs|gho|ghu|github_pat)_[A-Za-z0-9]{36,}'
  ["Connection Strings"]='(mongodb|mysql|postgres|postgresql)://[^:]+:[^@]+@'
  ["JWT Tokens"]='eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*'
)

# Files and directories to exclude
EXCLUDE_PATTERNS=(
  ".git/"
  "node_modules/"
  ".github/SECRETS.md"
  ".github/copilot/instructions.md"
  "scripts/scan-secrets.sh"
  ".atom-trail/"
  "archive/"
)

# Build exclude arguments for grep
EXCLUDE_ARGS=""
for pattern in "${EXCLUDE_PATTERNS[@]}"; do
  EXCLUDE_ARGS="$EXCLUDE_ARGS --exclude-dir=$pattern"
done

echo "Scanning for potential secrets..."
echo ""

FOUND_ISSUES=0

for pattern_name in "${!PATTERNS[@]}"; do
  pattern="${PATTERNS[$pattern_name]}"
  
  echo "Checking for: $pattern_name"
  
  # Scan files
  if grep -rniE $EXCLUDE_ARGS "$pattern" . 2>/dev/null | grep -v "# nosecret" | grep -v "example" | grep -v "REDACTED" | grep -v "placeholder" | grep -v "your_.*_here" | grep -v "\${.*}"; then
    echo "  ⚠️  FOUND: Potential $pattern_name detected"
    FOUND_ISSUES=$((FOUND_ISSUES + 1))
    EXIT_CODE=1
  else
    echo "  ✓ No $pattern_name found"
  fi
  echo ""
done

# Check for .env files (should only have .env.example)
echo "Checking for .env files..."
if find . -type f -name ".env" ! -name ".env.example" ! -path "*/.git/*" 2>/dev/null | grep -q .; then
  echo "  ⚠️  FOUND: .env files detected (should be in .gitignore)"
  find . -type f -name ".env" ! -name ".env.example" ! -path "*/.git/*"
  FOUND_ISSUES=$((FOUND_ISSUES + 1))
  EXIT_CODE=1
else
  echo "  ✓ No .env files found (good)"
fi
echo ""

# Check git history for secrets (last 10 commits)
echo "Checking recent git history..."
if git log -p -10 --all 2>/dev/null | grep -iE "(password|secret|api[_-]?key|token)[\s]*[=:]" | grep -v "example" | grep -v "REDACTED" | grep -v ".github/SECRETS.md" | grep -v "placeholder" | head -5; then
  echo "  ⚠️  WARNING: Potential secrets found in recent commits"
  echo "  Review the matches above carefully"
  FOUND_ISSUES=$((FOUND_ISSUES + 1))
  EXIT_CODE=1
else
  echo "  ✓ No obvious secrets in recent history"
fi
echo ""

# Summary
echo "=== Scan Summary ==="
if [ $EXIT_CODE -eq 0 ]; then
  echo "✓ No secrets detected"
  echo ""
  echo "Note: This scanner checks common patterns but may have false negatives."
  echo "Always review code carefully before committing."
else
  echo "⚠️  $FOUND_ISSUES potential issue(s) found"
  echo ""
  echo "Actions to take:"
  echo "1. Review each finding carefully"
  echo "2. If it's a false positive, add '# nosecret' comment on the line"
  echo "3. If it's an example, ensure it's clearly marked (use 'example' or 'placeholder')"
  echo "4. If it's a real secret:"
  echo "   - DO NOT commit"
  echo "   - Move to environment variable"
  echo "   - Use .env file (in .gitignore)"
  echo "   - Or use GitHub Secrets for CI/CD"
  echo ""
  echo "See .github/SECRETS.md for more information"
fi

exit $EXIT_CODE
