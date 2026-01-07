<#
Simulate walking pipelines/journeys across the repository in forward and backward directions.

Usage:
  .\walk_journeys.ps1           # dry-run summary
  .\walk_journeys.ps1 -Apply    # optional: perform a safe copy-to-temp and restore to simulate round-trip

This is a non-destructive simulation by default.
#>
param(
  [switch]$Apply
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Info($m) { Write-Host "[WALK] $m" -ForegroundColor Cyan }

Write-Info "Scanning canonical doc and script pipelines..."

$docs = Get-ChildItem -Path (Get-Location) -Recurse -Include *.md,*.ps1 -File | Where-Object { $_.FullName -notmatch '\.git\\' }
Write-Info "Found $($docs.Count) docs/scripts to simulate pipeline journeys. DryRun: $(-not $Apply)"

foreach ($f in $docs) {
  Write-Host "-> Inspect: $($f.FullName)"
}

if ($Apply) {
  $tmp = Join-Path $env:TEMP "spiralsafe-journey-$(Get-Date -Format o | ForEach-Object { $_ -replace '[:.]','-' })"
  New-Item -ItemType Directory -Path $tmp -Force | Out-Null
  Write-Info "Copying selected files to temp ($tmp) to simulate forward journey..."
  foreach ($f in $docs) { Copy-Item -Path $f.FullName -Destination $tmp -Force }
  Write-Info "Now simulating backward journey: restoring copies back to workspace (no overwrite)"
  foreach ($f in Get-ChildItem -Path $tmp -File) {
    $target = Join-Path (Get-Location) $f.Name
    if (-not (Test-Path $target)) { Copy-Item -Path $f.FullName -Destination $target }
  }
  Write-Info "Simulation complete. Temp files remain at $tmp (delete when satisfied)."
} else {
  Write-Info "Dry-run: no files copied. Rerun with -Apply to run safe simulation."
}
