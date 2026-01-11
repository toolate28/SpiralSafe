Param(
    [string]$RepoRoot = (Split-Path -Parent $MyInvocation.MyCommand.Path),
    [string]$OutZip = $null
)

Set-StrictMode -Version Latest

if (-not (Test-Path $RepoRoot)) { Write-Error "RepoRoot not found: $RepoRoot"; exit 1 }

if (-not $OutZip) { $OutZip = Join-Path $RepoRoot 'docs\staging\wave_payload.zip' }

$items = @(
    'docs\LESSON_TEMPLATE.md',
    'docs\LESSONS.md',
    'docs\staging\lessons_summary.json',
    'docs\staging\lessons_summary.md',
    'docs\staging\WAVE_NEXT.md',
    '.github\workflows\collect-lessons.yml',
    'scripts\collect_lessons.ps1',
    'scripts\README.md'
)

$found = @()
foreach ($i in $items) {
    $p = Join-Path $RepoRoot $i
    if (Test-Path $p) { $found += $p }
}

if ($found.Count -eq 0) { Write-Error "No files found to package."; exit 1 }

if (Test-Path $OutZip) { Remove-Item $OutZip -Force }

Compress-Archive -Path $found -DestinationPath $OutZip -Force

Write-Host "Created wave payload: $OutZip (contains $($found.Count) item(s))"
