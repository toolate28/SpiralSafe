# ═══════════════════════════════════════════════════════════════════════════════
# Install-SpiralSafeProfile.ps1 - Add SpiralSafe to PowerShell Profile
# ═══════════════════════════════════════════════════════════════════════════════
# H&&S:WAVE | Run this script to integrate SpiralSafe into your shell
# ═══════════════════════════════════════════════════════════════════════════════

param(
    [switch]$Force,
    [switch]$WhatIf
)

$ErrorActionPreference = 'Stop'
$SpiralSafeRoot = $PSScriptRoot | Split-Path -Parent
$ModulePath = Join-Path $SpiralSafeRoot "scripts\SpiralSafe.psm1"

# Profile integration block
$ProfileBlock = @"

# ═══════════════════════════════════════════════════════════════════════════════
# SpiralSafe Integration - H&&S:WAVE
# ═══════════════════════════════════════════════════════════════════════════════
`$env:SPIRALSAFE_ROOT = "$SpiralSafeRoot"
`$env:SPIRALSAFE_API = "https://api.spiralsafe.org"

if (Test-Path "$ModulePath") {
    Import-Module "$ModulePath" -Force -DisableNameChecking

    # Aliases
    Set-Alias -Name ss -Value Get-SpiralStatus -Scope Global
    Set-Alias -Name atom -Value New-ATOMTag -Scope Global
    Set-Alias -Name wave -Value Invoke-WAVEAnalysis -Scope Global
    Set-Alias -Name bump -Value New-BUMPMarker -Scope Global

    # Tab completion for ATOM types
    Register-ArgumentCompleter -CommandName New-ATOMTag -ParameterName Type -ScriptBlock {
        param(`$commandName, `$parameterName, `$wordToComplete, `$commandAst, `$fakeBoundParameter)
        @('INIT','CONFIG','SESSION','NPC','QUANTUM','MUSEUM','WAVE','BUMP','AWI','DOC','PLAN','VERIFY','DEPLOY') |
            Where-Object { `$_ -like "`$wordToComplete*" } |
            ForEach-Object { [System.Management.Automation.CompletionResult]::new(`$_, `$_, 'ParameterValue', `$_) }
    }

    # Prompt enhancement (optional - uncomment to enable)
    # function global:prompt {
    #     `$session = `$env:SPIRALSAFE_SESSION
    #     `$branch = git branch --show-current 2>`$null
    #     "[SS:`$session] `$PWD`n`$branch> "
    # }
}
# ═══════════════════════════════════════════════════════════════════════════════
"@

# Check if profile exists
if (-not (Test-Path $PROFILE)) {
    if ($WhatIf) {
        Write-Host "[WhatIf] Would create profile at: $PROFILE" -ForegroundColor Yellow
    } else {
        New-Item -Path $PROFILE -ItemType File -Force | Out-Null
        Write-Host "Created profile at: $PROFILE" -ForegroundColor Green
    }
}

# Check if already integrated
$CurrentProfile = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue
if ($CurrentProfile -match 'SpiralSafe Integration') {
    if ($Force) {
        Write-Host "Removing existing SpiralSafe integration..." -ForegroundColor Yellow
        $CurrentProfile = $CurrentProfile -replace '(?s)# ═+\r?\n# SpiralSafe Integration.*?# ═+\r?\n', ''
        if ($WhatIf) {
            Write-Host "[WhatIf] Would remove existing integration" -ForegroundColor Yellow
        } else {
            Set-Content -Path $PROFILE -Value $CurrentProfile.Trim()
        }
    } else {
        Write-Host "SpiralSafe already integrated. Use -Force to reinstall." -ForegroundColor Cyan
        return
    }
}

# Add to profile
if ($WhatIf) {
    Write-Host "[WhatIf] Would add SpiralSafe integration to profile" -ForegroundColor Yellow
    Write-Host $ProfileBlock -ForegroundColor Gray
} else {
    Add-Content -Path $PROFILE -Value $ProfileBlock
    Write-Host @"

SpiralSafe integrated into PowerShell profile.

Available commands:
  ss        - Get-SpiralStatus (what's done/doing/next)
  atom      - New-ATOMTag (generate ATOM identifiers)
  wave      - Invoke-WAVEAnalysis (coherence check)
  bump      - New-BUMPMarker (state transitions)

Reload profile with:
  . `$PROFILE

"@ -ForegroundColor Green
}

# ATOM tag for this installation
$atomTag = "ATOM-CONFIG-$(Get-Date -Format 'yyyyMMdd')-001-profile-integration"
Write-Host "Installation tagged: $atomTag" -ForegroundColor Cyan
