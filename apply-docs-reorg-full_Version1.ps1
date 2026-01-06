<#
apply-docs-reorg-full.ps1
Comprehensive, idempotent PowerShell script to:
 - consolidate root documentation into docs/ with categorized subfolders
 - preserve history using git mv
 - create pointer files at root for moved docs
 - merge ACKNOWLEDGEMENTS into CREDITS (docs/community/CREDITS.md)
 - add methodology docs: Day Zero, SAIF, ATOM
 - add ops artifacts: PR template, NEGATIVE_SPACE_ANALYSIS.md, SIGNOFF_CHECKLIST.md
 - inject small callouts into key docs (architecture, quick-start, troubleshooting)
 - optionally configure Git LFS for zip files
 - optionally update repo references from old filenames -> new paths
 - run markdown link-check (if npx present) and pre-commit (if present)
 - grouped commits per area for easy review
 - DryRun mode by default for safe preview

Usage:
  # preview (no filesystem or git changes)
  .\apply-docs-reorg-full.ps1 -DryRun

  # apply changes, auto-confirm replacements and enable Git LFS
  .\apply-docs-reorg-full.ps1 -AutoConfirm -UseLfs -UpdateRefs

Notes:
 - Run from repository root in PowerShell 7+.
 - Inspect DryRun output carefully before applying.
 - Script makes commits locally; push and create PR after verifying.
 - The script assumes git is on PATH.
#>

param(
  [switch]$DryRun = $true,
  [switch]$AutoConfirm,
  [switch]$UseLfs,
  [switch]$UpdateRefs,
  [switch]$CreateOpsFiles,
  [switch]$InjectCallouts,
  [switch]$RunLinkCheck
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Action {
  param($msg)
  if ($DryRun) { Write-Host "[DRY-RUN] $msg" -ForegroundColor Yellow } else { Write-Host $msg -ForegroundColor Cyan }
}

# Verify we are in a git repo
try {
  & git rev-parse --is-inside-work-tree 2>$null | Out-Null
} catch {
  throw "Not a git repository. cd to repo root and re-run the script."
}

$branch = (& git rev-parse --abbrev-ref HEAD).Trim()
Write-Host "On branch: $branch"

# Suggested branch
$expectedBranch = 'docs/cleanup/root-docs-consolidation'
  Write-Host "Warning: recommended branch is '$expectedBranch'. Current branch is '$branch'."
  if ($AutoConfirm) {
    Write-Action "No branch switch. Proceeding on $branch (AutoConfirm enabled)."
  } else {
    # Prompt for confirmation (fix: $ans was never set)
    $ans = Read-Host "Continue on current branch? [y/N]"
    if ($ans -notmatch '^[Yy]') { throw "Abort: switch to the recommended branch and re-run." }
  }

# Ensure target directories exist
$targetDirs = @(
  'docs/design','docs/guides','docs/roadmap','docs/community','docs/specs',
  'docs/appendix','docs/notes','docs/misc','docs/scripts','docs/methodology','docs/ops'
)
foreach ($d in $targetDirs) {
  if (-not (Test-Path $d)) {
    Write-Action "Create directory: $d"
    if (-not $DryRun) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
  }
}

# Mapping: source -> destination
$mappings = @{
  'ARCHITECTURE.md' = 'docs/design/ARCHITECTURE.md'
  'IMPLEMENTATION_COMPLETE.md' = 'docs/design/IMPLEMENTATION_COMPLETE.md'
  'SAFE_SPIRAL_MASTER_INDEX.md' = 'docs/design/SAFE_SPIRAL_MASTER_INDEX.md'
  'QUICK_START.md' = 'docs/guides/QUICK_START.md'
  'LOGDY_DEPLOYMENT_GUIDE.md' = 'docs/guides/LOGDY_DEPLOYMENT_GUIDE.md'
  'PLATFORM_INTEGRATION_ROADMAP.md' = 'docs/roadmap/PLATFORM_INTEGRATION_ROADMAP.md'
  'MULTI_FORK_STRATEGY.md' = 'docs/roadmap/MULTI_FORK_STRATEGY.md'
  'DOMAIN_PLAN.md' = 'docs/specs/DOMAIN_PLAN.md'
  'GLOSSARY.md' = 'docs/specs/GLOSSARY.md'
  'MAGNUM_OPUS.md' = 'docs/appendix/MAGNUM_OPUS.md'
  'THE_ONE_PATH.md' = 'docs/appendix/THE_ONE_PATH.md'
  'THE_COMPLETION_SONG.md' = 'docs/appendix/THE_COMPLETION_SONG.md'

  'THE_AINULINDALE_OF_HOPE_AND_SAUCE.md' = 'docs/appendix/THE_AINULINDALE_OF_HOPE_AND_SAUCE.md'
  '07_FAILURE_MODES_AND_RECOVERY.md' = 'docs/notes/07_FAILURE_MODES_AND_RECOVERY.md'
  'USER_ENLIGHTENMENT_PROTOCOL.md' = 'docs/notes/USER_ENLIGHTENMENT_PROTOCOL.md'
  'bump.md' = 'docs/misc/bump.md'
  'wave.md' = 'docs/misc/wave.md'
  'create_spiral_payload.sh' = 'docs/scripts/create_spiral_payload.sh'
  'project-book.ipynb' = 'docs/misc/project-book.ipynb'
}

function New-Pointer {
  param($rootName, $destPath)
  $ptr = @"
# $rootName


If automation, CI, or external references require the file at the original path, update references or ask for compatibility retention.
"@
  Write-Action "Write pointer file at root: $rootName -> $destPath"
  if (-not $DryRun) { Set-Content -LiteralPath $rootName -Value $ptr -Encoding UTF8 }
  if (-not $DryRun) { & git add -- $rootName }
}

function Safe-GitMove {
  param($src, $dest)
  if (-not (Test-Path $src)) {
    Write-Host "SKIP (not found): $src" -ForegroundColor DarkYellow
  }
  $destDir = Split-Path $dest -Parent
  if (-not (Test-Path $destDir)) { Write-Action "Create dest directory: $destDir"; if (-not $DryRun) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null } }
  return $true
}

$groups = @{
  'design' = @('ARCHITECTURE.md','IMPLEMENTATION_COMPLETE.md','SAFE_SPIRAL_MASTER_INDEX.md')
  'guides' = @('QUICK_START.md','TROUBLESHOOTING.md','LOGDY_DEPLOYMENT_GUIDE.md')
  'roadmap' = @('PLATFORM_INTEGRATION_ROADMAP.md','MULTI_FORK_STRATEGY.md','PUBLICATION_MANIFEST_v1.0.md')
  'community' = @('CREDITS.md')
  'specs' = @('VERIFICATION_STAMP.md','DOMAIN_PLAN.md','GLOSSARY.md')
  'appendix' = @('MAGNUM_OPUS.md','SESSION_SUMMARY_20260104.md','THE_ONE_PATH.md','THE_COMPLETION_SONG.md','THE_AINULINDALE_OF_HOPE_AND_SAUCE.md')
  'notes' = @('07_FAILURE_MODES_AND_RECOVERY.md','USER_ENLIGHTENMENT_PROTOCOL.md')
  'misc' = @('bump.md','wave.md','spiral_safe_bump_ci_payload.zip','create_spiral_payload.sh','project-book.ipynb')
}

# Apply moves, grouped commits
foreach ($grp in $groups.Keys) {
  $moved = $false
  foreach ($src in $groups[$grp]) {
    if ($mappings.ContainsKey($src)) {
      $ok = Safe-GitMove $src $mappings[$src]
      if ($ok) { $moved = $true }
    }
  }
  if ($moved) {
    $msg = "chore(docs): move $grp docs into docs/$grp/"
    Write-Action "Commit: $msg"
    if (-not $DryRun) { & git add -A ; & git commit -m $msg }
  } else {
    Write-Host "No files moved for group: $grp" -ForegroundColor DarkGray
  }
}

# Merge ACKNOWLEDGEMENTS.md into docs/community/CREDITS.md if present
$ack = 'ACKNOWLEDGEMENTS.md'
$credits = 'docs/community/CREDITS.md'
if (Test-Path $ack) {
  if (-not (Test-Path $credits)) {
    Write-Action "Create $credits"
    if (-not $DryRun) { New-Item -ItemType File -Path $credits -Force | Out-Null }
  }
  Write-Action "Merge $ack into $credits under 'Acknowledgements'"
  if (-not $DryRun) {
    Add-Content -Path $credits -Value "`n`n## Acknowledgements`n"
    Get-Content -Path $ack | Add-Content -Path $credits
    # replace root ack with pointer
    Remove-Item $ack
    New-Pointer -rootName $ack -destPath $credits
    & git add $credits
    & git commit -m "chore(docs): merge ACKNOWLEDGEMENTS into docs/community/CREDITS.md and add pointer"
  }
}

# Write methodology files (full content)
$methodDir = 'docs/methodology'
if (-not (Test-Path $methodDir)) { if (-not $DryRun) { New-Item -ItemType Directory -Path $methodDir -Force | Out-Null } }


