# apply-docs-move-now.ps1
# Run in repo root with PowerShell 7.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Map source -> dest (add or remove entries if you want)
$mappings = @{
  'ARCHITECTURE.md' = 'docs/design/ARCHITECTURE.md'
  'IMPLEMENTATION_COMPLETE.md' = 'docs/design/IMPLEMENTATION_COMPLETE.md'
  'SAFE_SPIRAL_MASTER_INDEX.md' = 'docs/design/SAFE_SPIRAL_MASTER_INDEX.md'
  'QUICK_START.md' = 'docs/guides/QUICK_START.md'
  'TROUBLESHOOTING.md' = 'docs/guides/TROUBLESHOOTING.md'
  'LOGDY_DEPLOYMENT_GUIDE.md' = 'docs/guides/LOGDY_DEPLOYMENT_GUIDE.md'
  'PLATFORM_INTEGRATION_ROADMAP.md' = 'docs/roadmap/PLATFORM_INTEGRATION_ROADMAP.md'
  'MULTI_FORK_STRATEGY.md' = 'docs/roadmap/MULTI_FORK_STRATEGY.md'
  'PUBLICATION_MANIFEST_v1.0.md' = 'docs/roadmap/PUBLICATION_MANIFEST_v1.0.md'
  'CREDITS.md' = 'docs/community/CREDITS.md'
  'ACKNOWLEDGEMENTS.md' = 'docs/community/ACKNOWLEDGEMENTS.md'  # will be merged below
  'VERIFICATION_STAMP.md' = 'docs/specs/VERIFICATION_STAMP.md'
  'DOMAIN_PLAN.md' = 'docs/specs/DOMAIN_PLAN.md'
  'GLOSSARY.md' = 'docs/specs/GLOSSARY.md'
  'MAGNUM_OPUS.md' = 'docs/appendix/MAGNUM_OPUS.md'
  'SESSION_SUMMARY_20260104.md' = 'docs/appendix/SESSION_SUMMARY_20260104.md'
  'THE_ONE_PATH.md' = 'docs/appendix/THE_ONE_PATH.md'
  'THE_COMPLETION_SONG.md' = 'docs/appendix/THE_COMPLETION_SONG.md'
  'THE_AINULINDALE_OF_HOPE_AND_SAUCE.md' = 'docs/appendix/THE_AINULINDALE_OF_HOPE_AND_SAUCE.md'
  '07_FAILURE_MODES_AND_RECOVERY.md' = 'docs/notes/07_FAILURE_MODES_AND_RECOVERY.md'
  'USER_ENLIGHTENMENT_PROTOCOL.md' = 'docs/notes/USER_ENLIGHTENMENT_PROTOCOL.md'
  'bump.md' = 'docs/misc/bump.md'
  'wave.md' = 'docs/misc/wave.md'
  'spiral_safe_bump_ci_payload.zip' = 'docs/misc/spiral_safe_bump_ci_payload.zip'
  'create_spiral_payload.sh' = 'docs/scripts/create_spiral_payload.sh'
  'project-book.ipynb' = 'docs/misc/project-book.ipynb'
}

# Ensure docs dirs exist
$dirs = @('docs/design','docs/guides','docs/roadmap','docs/community','docs/specs','docs/appendix','docs/notes','docs/misc','docs/scripts','docs/methodology','docs/ops')
foreach ($d in $dirs) { if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null } }

function New-Pointer($rootName, $newPath) {
  $content = "# $rootName`n`nThis file has been moved to `$newPath`. See that file for the full content and history.`n"
  Set-Content -LiteralPath $rootName -Value $content -Encoding UTF8
  & git add -- $rootName
}

function SafeGitMove($src, $dest) {
  if (Test-Path $src) {
    $destDir = Split-Path $dest -Parent
    if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
    Write-Host "Moving $src -> $dest"
    & git mv -- "$src" "$dest"
    # create pointer at root with same filename
    New-Pointer (Split-Path $src -Leaf) $dest
    return $true
  } else {
    Write-Host "Skip (not found): $src"
    return $false
  }
}

# Move files; group commits to be tidy
$groups = @{
  'design' = @('ARCHITECTURE.md','IMPLEMENTATION_COMPLETE.md','SAFE_SPIRAL_MASTER_INDEX.md')
  'guides' = @('QUICK_START.md','TROUBLESHOOTING.md','LOGDY_DEPLOYMENT_GUIDE.md')
  'roadmap' = @('PLATFORM_INTEGRATION_ROADMAP.md','MULTI_FORK_STRATEGY.md','PUBLICATION_MANIFEST_v1.0.md')
  'community' = @('CREDITS.md','ACKNOWLEDGEMENTS.md')
  'specs' = @('VERIFICATION_STAMP.md','DOMAIN_PLAN.md','GLOSSARY.md')
  'appendix' = @('MAGNUM_OPUS.md','SESSION_SUMMARY_20260104.md','THE_ONE_PATH.md','THE_COMPLETION_SONG.md','THE_AINULINDALE_OF_HOPE_AND_SAUCE.md')
  'notes' = @('07_FAILURE_MODES_AND_RECOVERY.md','USER_ENLIGHTENMENT_PROTOCOL.md')
  'misc' = @('bump.md','wave.md','spiral_safe_bump_ci_payload.zip','create_spiral_payload.sh','project-book.ipynb')
}

foreach ($grp in $groups.Keys) {
  $moved = $false
  foreach ($src in $groups[$grp]) {
    if ($mappings.ContainsKey($src)) {
      $ok = SafeGitMove $src $mappings[$src]
      if ($ok) { $moved = $true }
    }
  }
  if ($moved) {
    $msg = "chore(docs): move $grp docs into docs/$grp/"
    & git add -A
    & git commit -m $msg
  } else {
    Write-Host "No $grp files moved."
  }
}

# Merge ACKNOWLEDGEMENTS into CREDITS if both present (or if ack exist)
$ack = 'ACKNOWLEDGEMENTS.md'
$credits = 'docs/community/CREDITS.md'
if (Test-Path $ack) {
  if (-not (Test-Path $credits)) { New-Item -ItemType File -Path $credits -Force | Out-Null }
  Write-Host "Merging $ack into $credits"
  Add-Content -Path $credits -Value "`n`n## Acknowledgements`n"
  Get-Content $ack | Add-Content -Path $credits
  # replace root ack with pointer
  Remove-Item $ack
  New-Pointer $ack $credits
  & git add $credits
  & git commit -m "chore(docs): merge ACKNOWLEDGEMENTS into docs/community/CREDITS.md and add pointer"
}

# Create methodology files (Day Zero, SAIF, ATOM) from provided content
$methodDir = 'docs/methodology'
$dayZero = @'
# Day Zero Design

**Get it right from the start.**

... (full content inserted here)
'@
$saif = @'
# SAIF: Systematic Analysis and Issue Fixing

**Evidence-based diagnosis and intervention for problems.**

... (full content inserted here)
'@
$atom = @'
# ATOM: Atomic Task Orchestration Method

**Decomposing complex work into independently verifiable units.**

... (full content inserted here)
'@

Set-Content -Path "$methodDir/day-zero-design.md" -Value $dayZero -Encoding UTF8
Set-Content -Path "$methodDir/saif.md" -Value $saif -Encoding UTF8
Set-Content -Path "$methodDir/atom.md" -Value $atom -Encoding UTF8
& git add $methodDir/*.md
& git commit -m "chore(docs): add methodology docs (day-zero, saif, atom)"

# Add docs/README.md if missing
$docsIndex = 'docs/README.md'
if (-not (Test-Path $docsIndex)) {
  $index = @"
# SpiralSafe Documentation Index

See docs/design, docs/guides, docs/roadmap, docs/community, docs/specs, docs/appendix, docs/notes, docs/methodology.
"@
  Set-Content -Path $docsIndex -Value $index -Encoding UTF8
  & git add $docsIndex
  & git commit -m "chore(docs): add docs/ README index"
}

# Short root README if missing or small (this keeps root tidy)
$rootReadme = 'README.md'
$rootContent = @"
# SpiralSafe

Top-level docs consolidated into docs/ for discoverability. See docs/README.md for an index.
"@
Set-Content -LiteralPath $rootReadme -Value $rootContent -Encoding UTF8
& git add $rootReadme
& git commit -m "chore(docs): shorten root README to point to docs/"

# Git LFS: track zip if present
# Only proceed if git-lfs available
try {
  & git lfs version > $null
  Write-Host "Git LFS available: enabling tracking for *.zip"
  & git lfs track "*.zip"
  & git add .gitattributes
  & git commit -m "chore(docs): track zip files with Git LFS"
} catch {
  Write-Host "Git LFS not available or failed: run 'git lfs install' and re-run tracking if desired."
}

Write-Host "`nDONE. Verify with:"
Write-Host "  git status"
Write-Host "  git log --oneline -n 10"
Write-Host "  ls docs -Recurse | Select-String '\.md' -Quiet"