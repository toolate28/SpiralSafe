<#
Produce a small audit of session/sign-in events, and write `docs/staging/session_audit.json` and markdown summary.

This script does not access remote services; it collects locally available session files in `.verification/` and any `session-*.json` files.
Run locally with: `pwsh .\scripts\audit_sessions.ps1`
#>

Set-StrictMode -Version Latest

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$verDir = Join-Path $repoRoot '.verification'
New-Item -Path (Join-Path $repoRoot 'docs\staging') -ItemType Directory -Force | Out-Null

$sessions = @()
if (Test-Path $verDir) {
    Get-ChildItem -Path $verDir -Filter 'session-*.json' -File -ErrorAction SilentlyContinue | ForEach-Object {
        try {
            $obj = Get-Content $_.FullName -Raw | ConvertFrom-Json -ErrorAction Stop
            $obj.__file = $_.Name
            $sessions += $obj
        } catch {
            $sessions += @{ file = $_.Name; error = $_ }
        }
    }
}

# Also look for any .verification session files in repo root
Get-ChildItem -Path $repoRoot -Filter 'session-*.json' -File -ErrorAction SilentlyContinue | ForEach-Object {
    try { $obj = Get-Content $_.FullName -Raw | ConvertFrom-Json -ErrorAction Stop; $obj.__file = $_.Name; $sessions += $obj } catch { $sessions += @{ file = $_.Name; error = $_ } }
}

$outJson = Join-Path $repoRoot 'docs\staging\session_audit.json'
$sessions | ConvertTo-Json -Depth 6 | Out-File $outJson -Encoding UTF8

$outMd = Join-Path $repoRoot 'docs\staging\session_audit.md'
$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('# Session Audit')
[void]$sb.AppendLine("Generated: $(Get-Date -Format o)")
[void]$sb.AppendLine('')
foreach ($s in $sessions) {
    if ($s.__file) { [void]$sb.AppendLine("## $($s.__file)") }
    if ($s.user) { [void]$sb.AppendLine("*User:* $($s.user)") }
    if ($s.started) { [void]$sb.AppendLine("*Started:* $($s.started)") }
    if ($s.ended) { [void]$sb.AppendLine("*Ended:* $($s.ended)") }
    if ($s.actions) { [void]$sb.AppendLine("*Actions:* $($s.actions.Count)") }
    [void]$sb.AppendLine('')
}

[System.IO.File]::WriteAllText($outMd, $sb.ToString(), [System.Text.Encoding]::UTF8)
Write-Host "Wrote session audit: $outJson and $outMd"
