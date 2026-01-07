<#
Compute SHA256 hashes for files in the repo and write to hashes.sha256.

Usage:
  .\hash_all.ps1            # dry-run, prints count
  .\hash_all.ps1 -Out hashes.sha256 -Apply
#>
param(
  [string]$Out = 'hashes.sha256',
  [switch]$Apply
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Hash-File($path) {
  $sha = [System.Security.Cryptography.SHA256]::Create()
  $fs = [System.IO.File]::OpenRead($path)
  try { $hash = $sha.ComputeHash($fs) } finally { $fs.Close() }
  return ($hash | ForEach-Object { $_.ToString('x2') }) -join ''
}

$root = Get-Location
$files = Get-ChildItem -Path $root -Recurse -File -Exclude '.git','node_modules','target','*.pyc','*.pkl' | Where-Object { $_.FullName -notmatch '\.git\\' }
Write-Host "Found $($files.Count) files to hash. DryRun: $(-not $Apply)"

$lines = @()
foreach ($f in $files) {
  try {
    $h = Hash-File $f.FullName
    $rel = $f.FullName.Substring($root.Path.Length).TrimStart('\\','/')
    $lines += "$h  $rel"
  } catch {
    Write-Warning "Skipping $($f.FullName): $_"
  }
}

if ($Apply) {
  Set-Content -Path $Out -Value $lines -Encoding UTF8
  Write-Host "Wrote $($lines.Count) hashes to $Out"
} else {
  Write-Host "DRY-RUN: Would write $($lines.Count) lines to $Out"
}
