# Collect lessons from `docs/LESSONS.md` and write JSON + Markdown summaries
#
# Usage:
#   pwsh .\scripts\collect_lessons.ps1
#
# Outputs:
#   docs/staging/lessons_summary.json
#   docs/staging/lessons_summary.md

Param(
    [string]$RepoRoot = (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
)

Set-StrictMode -Version Latest

$lessonsFile = Join-Path $RepoRoot 'docs\LESSONS.md'
$stagingDir = Join-Path $RepoRoot 'docs\staging'
New-Item -ItemType Directory -Path $stagingDir -Force | Out-Null

if (-not (Test-Path $lessonsFile)) {
    Write-Error "LESSONS.md not found at $lessonsFile"
    exit 1
}

$content = Get-Content $lessonsFile -Raw -ErrorAction Stop

# Split on lines that contain only three dashes (---)
$blocks = $content -split "(?m)^\s*---\s*$"

$entries = @()
foreach ($b in $blocks) {
    # Find required fields using simple markdown key lines
    if ($b -match "- \*\*Title:\*\*\s*(.+)") { $title = $Matches[1].Trim() } else { continue }
    if ($b -match "- \*\*Date:\*\*\s*(.+)") { $date = $Matches[1].Trim() } else { $date = '' }
    if ($b -match "- \*\*Source:\*\*\s*(.+)") { $source = $Matches[1].Trim() } else { $source = '' }
    if ($b -match "- \*\*Author / Owner:\*\*\s*(.+)") { $owner = $Matches[1].Trim() } else { $owner = '' }

    $excerpt = ($b -replace '\r?\n', ' ') -replace '\s{2,}', ' '
    if ($excerpt.Length -gt 240) { $excerpt = $excerpt.Substring(0,240) + '...' }

    $entries += [pscustomobject]@{
        title = $title
        date = $date
        source = $source
        owner = $owner
        excerpt = $excerpt
    }
}

$outJson = Join-Path $stagingDir 'lessons_summary.json'
$entries | ConvertTo-Json -Depth 5 | Out-File $outJson -Encoding UTF8

$outMd = Join-Path $stagingDir 'lessons_summary.md'
$mdBuilder = New-Object System.Text.StringBuilder
foreach ($e in $entries) {
    [void]$mdBuilder.AppendLine("### $($e.title)")
    [void]$mdBuilder.AppendLine('')
    [void]$mdBuilder.AppendLine("*Date:* $($e.date)")
    [void]$mdBuilder.AppendLine("*Source:* $($e.source)")
    if ($e.owner) { [void]$mdBuilder.AppendLine("*Owner:* $($e.owner)") }
    [void]$mdBuilder.AppendLine('')
    [void]$mdBuilder.AppendLine($e.excerpt)
    [void]$mdBuilder.AppendLine('')
}

[System.IO.File]::WriteAllText($outMd, $mdBuilder.ToString(), [System.Text.Encoding]::UTF8)

Write-Host "Wrote $($entries.Count) lesson(s) to:`n  $outJson`n  $outMd"
