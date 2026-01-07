<#
Safe bootstrap helper for SpiralSafe.

Usage:
  # Preview (no installs)
  .\bootstrap.ps1

  # Run installs where possible (may require admin/interactive steps)
  .\bootstrap.ps1 -Apply

Notes:
 - This script is intentionally conservative and non-destructive.
 - It will print recommended commands and run only the ones flagged by -Apply.
#>
param(
  [switch]$Apply
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Info { param($m) Write-Host "[BOOT] $m" -ForegroundColor Cyan }

Write-Info "Bootstrap started (Apply=$Apply)"

# 1) Python deps (if requirements file exists)
$reqPaths = @('python-requirements.txt','ClaudeNPC-Server-Suite/python-requirements.txt') | ForEach-Object { Join-Path (Get-Location) $_ }
$found = $reqPaths | Where-Object { Test-Path $_ }
if ($found) {
  foreach ($f in $found) {
    Write-Info "Found requirements: $f"
    $cmd = "python -m pip install -r `"$f`""
    if ($Apply) {
      Write-Info "Installing Python requirements from $f..."
      & python -m pip install -r $f
    } else {
      Write-Host "DRY-RUN: $cmd"
    }
  }
} else { Write-Info "No python requirements file found in expected locations." }

# 2) Recommend tools (print instructions only)
Write-Info "Recommended tools: git, pwsh/powershell, cloudflared, docker (optional)."
if ($Apply) {
  Write-Info "Apply is set: this script will NOT auto-install platform packages. Please run platform installers as needed."
}

Write-Info "Bootstrap complete. Review output and run with -Apply to perform installs where safe."
