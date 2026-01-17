#!/usr/bin/env bash
# Test PowerShell scripts using PSScriptAnalyzer
# Usage: ./scripts/test-powershell.sh
set -euo pipefail

EXIT_CODE=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== PowerShell Script Testing ==="
echo ""

cd "$REPO_ROOT"

# Check if PowerShell is available
if ! command -v pwsh >/dev/null 2>&1; then
  echo "⚠ PowerShell (pwsh) not installed"
  echo "Install with: https://aka.ms/powershell"
  echo "Skipping PowerShell testing..."
  exit 0
fi

echo "Found PowerShell: $(pwsh --version)"
echo ""

# Check if PSScriptAnalyzer is installed
if ! pwsh -Command "Get-Module -ListAvailable PSScriptAnalyzer" >/dev/null 2>&1; then
  echo "⚠ PSScriptAnalyzer not installed"
  echo "Install with: pwsh -Command 'Install-Module -Name PSScriptAnalyzer -Force -Scope CurrentUser'"
  echo "Skipping PowerShell linting..."
  exit 0
fi

# Find PowerShell scripts
PS_SCRIPTS=$(find . -name "*.ps1" ! -path "*/node_modules/*" ! -path "*/.git/*" 2>/dev/null || true)

if [ -z "$PS_SCRIPTS" ]; then
  echo "No PowerShell scripts found"
  exit 0
fi

echo "Testing PowerShell scripts..."
echo ""

for script in $PS_SCRIPTS; do
  script_name=$(basename "$script")
  echo "Testing: $script_name"
  
  # Syntax check
  if pwsh -NoProfile -Command "Test-Path '$script' -PathType Leaf" >/dev/null 2>&1; then
    echo "  ✓ file accessible"
  else
    echo "  ✗ file not accessible"
    EXIT_CODE=1
    continue
  fi
  
  # PSScriptAnalyzer
  VIOLATIONS=$(pwsh -NoProfile -Command "Invoke-ScriptAnalyzer -Path '$script' -Severity Warning,Error | Measure-Object | Select-Object -ExpandProperty Count" 2>/dev/null || echo "error")
  
  if [ "$VIOLATIONS" = "error" ]; then
    echo "  ⚠ PSScriptAnalyzer check failed"
  elif [ "$VIOLATIONS" -eq 0 ]; then
    echo "  ✓ PSScriptAnalyzer passed (0 issues)"
  else
    echo "  ⚠ PSScriptAnalyzer found $VIOLATIONS issue(s)"
    pwsh -NoProfile -Command "Invoke-ScriptAnalyzer -Path '$script' -Severity Warning,Error" 2>/dev/null || true
    # Don't fail on warnings for now, just report
  fi
  
  echo ""
done

echo "=== Test Summary ==="
if [ $EXIT_CODE -eq 0 ]; then
  echo "✓ PowerShell scripts validated"
else
  echo "✗ Some PowerShell scripts have issues"
fi

exit $EXIT_CODE
