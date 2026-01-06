<#
Generate two unique IDs (host and session) and produce signatures and a short verification report.

Usage:
  .\verify_claims.ps1            # dry-run (prints report)
  .\verify_claims.ps1 -Out report.md -Apply

Note: Signatures here are SHA256 digests of identifying fields and timestamps. For cryptographic, auditable signatures use GPG or a PKI.
#>
param(
  [string]$Out = 'verification_report.md',
  [switch]$Apply
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Sha256Hex($s) {
  $b = [System.Text.Encoding]::UTF8.GetBytes($s)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  $h = $sha.ComputeHash($b)
  return ($h | ForEach-Object { $_.ToString('x2') }) -join ''
}

Write-Host "Preparing verification data (Apply=$Apply)"

# Host identifier (if available)
try {
  $hostGuid = (Get-CimInstance -ClassName Win32_ComputerSystemProduct).UUID
} catch {
  $hostGuid = [guid]::NewGuid().ToString()
}

$user = $env:USERNAME
$timestamp = (Get-Date).ToUniversalTime().ToString('o')
$sessionId = [guid]::NewGuid().ToString()

$hostSig = Sha256Hex("$hostGuid|$user|$timestamp")
$sessionSig = Sha256Hex("$sessionId|$user|$timestamp")

$report = @()
$report += "# SpiralSafe Verification Report"
$report += ""
$report += "Generated: $timestamp (UTC)"
$report += ""
$report += "## Identifiers"
$report += "- Host ID: $hostGuid"
$report += "- Host Signature (SHA256): $hostSig"
$report += "- Session ID: $sessionId"
$report += "- Session Signature (SHA256): $sessionSig"
$report += "- User: $user"
$report += ""
$report += "## Notes"
$report += "- Signatures are SHA256 digests of id|user|timestamp. For higher-assurance signing, use GPG/OpenSSL with a private key."
$report += ""
$report += "## Sample verification" 
$report += "To verify a signature locally, recompute SHA256 on the same fields and compare." 

if ($Apply) {
  Set-Content -Path $Out -Value $report -Encoding UTF8
  Write-Host "Wrote verification report to $Out"
} else {
  Write-Host "DRY-RUN: Verification report preview:" -ForegroundColor Cyan
  $report | ForEach-Object { Write-Host $_ }
}
