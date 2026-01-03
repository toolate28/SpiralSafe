<#
.SYNOPSIS
    KENL Ecosystem Bootstrap - One Command Setup
.DESCRIPTION
    Post-clone setup script that configures everything for immediate use.
    Run this once after cloning the repository.

    What it does:
    1. Verifies dependencies (git, bun, PowerShell)
    2. Installs PowerShell Command Center
    3. Sets up terminal profiles
    4. Configures Claude Code settings
    5. Initializes ATOM trail
    6. Opens workspace in VS Code

.PARAMETER SkipProfile
    Skip PowerShell profile installation
.PARAMETER SkipTerminalProfiles
    Skip terminal profile installation
.PARAMETER Quick
    Run in quick mode (skip optional steps)

.EXAMPLE
    .\Bootstrap.ps1
    Full installation with all features

.EXAMPLE
    .\Bootstrap.ps1 -Quick
    Quick setup, skip optional components

.NOTES
    Version: 1.0.0
    Author: KENL Team
    Safe: Backs up existing configs before modification
    Idempotent: Safe to run multiple times
#>

param(
    [switch]$SkipProfile,
    [switch]$SkipTerminalProfiles,
    [switch]$Quick
)

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

# ============================================
# VISUAL PANACHE - Color Output Helpers
# ============================================

function Write-Step {
    param($Message, $Step, $Total)
    Write-Host "`n[$Step/$Total] " -ForegroundColor DarkGray -NoNewline
    Write-Host $Message -ForegroundColor Cyan
}

function Write-Success {
    param($Message)
    Write-Host "  ✅ " -ForegroundColor Green -NoNewline
    Write-Host $Message -ForegroundColor White
}

function Write-Info {
    param($Message)
    Write-Host "  ℹ️  " -ForegroundColor Cyan -NoNewline
    Write-Host $Message -ForegroundColor Gray
}

function Write-Warning {
    param($Message)
    Write-Host "  ⚠️  " -ForegroundColor Yellow -NoNewline
    Write-Host $Message -ForegroundColor Yellow
}

function Write-Error {
    param($Message)
    Write-Host "  ❌ " -ForegroundColor Red -NoNewline
    Write-Host $Message -ForegroundColor Red
}

function Write-Banner {
    $banner = @"

╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   KENL ECOSYSTEM BOOTSTRAP                                ║
║   Post-Clone Setup & Configuration                        ║
║                                                           ║
║   Operational effectiveness • Flow • Execution panache    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

"@
    Write-Host $banner -ForegroundColor Magenta
}

function Write-Complete {
    $complete = @"

╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🎉 BOOTSTRAP COMPLETE                                   ║
║                                                           ║
║   Your KENL environment is ready for action!              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

"@
    Write-Host $complete -ForegroundColor Green
}

# ============================================
# DEPENDENCY VERIFICATION
# ============================================

function Test-Dependency {
    param(
        [string]$Command,
        [string]$Name,
        [string]$InstallHint
    )

    if (Get-Command $Command -ErrorAction SilentlyContinue) {
        Write-Success "$Name found"
        return $true
    } else {
        Write-Warning "$Name not found"
        if ($InstallHint) {
            Write-Info "Install hint: $InstallHint"
        }
        return $false
    }
}

# ============================================
# MAIN EXECUTION
# ============================================

Clear-Host
Write-Banner

Write-Host "Starting bootstrap at $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor DarkGray
Write-Host "Repository: $PSScriptRoot`n" -ForegroundColor DarkGray

$totalSteps = 8
$currentStep = 0

# ============================================
# STEP 1: Verify Dependencies
# ============================================

$currentStep++
Write-Step "Verifying System Dependencies" $currentStep $totalSteps

$gitOk = Test-Dependency "git" "Git" "winget install Git.Git"
$pwshOk = Test-Dependency "pwsh" "PowerShell 7+" "winget install Microsoft.PowerShell"
$bunOk = Test-Dependency "bun" "Bun Runtime" "https://bun.sh/"

if (-not $Quick) {
    $wranglerOk = Test-Dependency "wrangler" "Cloudflare Wrangler" "npm install -g wrangler"
    $codeOk = Test-Dependency "code" "VS Code" "winget install Microsoft.VisualStudioCode"
}

if (-not $gitOk -or -not $pwshOk) {
    Write-Error "Critical dependencies missing. Install Git and PowerShell 7+ first."
    exit 1
}

# ============================================
# STEP 2: Initialize Repository Structure
# ============================================

$currentStep++
Write-Step "Initializing Repository Structure" $currentStep $totalSteps

$kenlRoot = $PSScriptRoot
Set-Location $kenlRoot

# Verify critical directories
$criticalDirs = @(
    "env-config",
    "frameworks",
    "templates",
    "SpiralSafe"
)

foreach ($dir in $criticalDirs) {
    if (Test-Path $dir) {
        Write-Success "Verified: $dir"
    } else {
        Write-Warning "Missing: $dir (expected in repository)"
    }
}

# ============================================
# STEP 3: Initialize ATOM Trail
# ============================================

$currentStep++
Write-Step "Initializing ATOM Trail" $currentStep $totalSteps

$atomTrailPath = Join-Path $kenlRoot ".." ".atom-trail"

if (-not (Test-Path $atomTrailPath)) {
    Write-Info "Creating ATOM trail file..."
    New-Item -Path $atomTrailPath -ItemType File -Force | Out-Null
    $timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"
    Add-Content -Path $atomTrailPath -Value "$timestamp | ATOM-INIT-$(Get-Date -Format 'yyyyMMdd')-001 | [System] | Local | KENL ecosystem initialized via Bootstrap.ps1"
    Write-Success "ATOM trail initialized"
} else {
    $entryCount = (Get-Content $atomTrailPath).Count
    Write-Success "ATOM trail exists ($entryCount entries)"
}

# ============================================
# STEP 4: Install PowerShell Command Center
# ============================================

$currentStep++
Write-Step "Installing PowerShell Command Center" $currentStep $totalSteps

if ($SkipProfile) {
    Write-Info "Skipped (--SkipProfile)"
} else {
    $installScript = Join-Path $kenlRoot "env-config\Install-CommandCenter.ps1"

    if (Test-Path $installScript) {
        try {
            Write-Info "Running Command Center installer..."
            & $installScript -Force *>&1 | Out-Null
            Write-Success "Command Center installed to PowerShell profile"
            Write-Info "Commands available: cc, ccref, ccoff, ccon"
        } catch {
            Write-Warning "Command Center installation had issues: $_"
        }
    } else {
        Write-Warning "Install-CommandCenter.ps1 not found"
    }
}

# ============================================
# STEP 5: Configure Terminal Profiles
# ============================================

$currentStep++
Write-Step "Configuring Terminal Profiles" $currentStep $totalSteps

if ($SkipTerminalProfiles) {
    Write-Info "Skipped (--SkipTerminalProfiles)"
} else {
    # Windows Terminal
    $wtProfileSource = Join-Path $kenlRoot "env-config\windows-terminal-profiles.json"
    $wtProfileDest = "$env:LOCALAPPDATA\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"

    if (Test-Path $wtProfileSource) {
        if (Test-Path $wtProfileDest) {
            $backup = "$wtProfileDest.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
            Copy-Item $wtProfileDest $backup -Force
            Write-Info "Windows Terminal profile backed up"
        }

        Write-Info "Windows Terminal profile available at: $wtProfileSource"
        Write-Info "Manual merge recommended (profiles vary by installation)"
        Write-Success "Reference profiles ready"
    } else {
        Write-Warning "Windows Terminal profile template not found"
    }

    # WaveTerm
    $waveProfileSource = Join-Path $kenlRoot "env-config\waveterm-profiles.json"
    if (Test-Path $waveProfileSource) {
        Write-Success "WaveTerm profiles available at: $waveProfileSource"
    }
}

# ============================================
# STEP 6: Configure Claude Code Settings
# ============================================

$currentStep++
Write-Step "Configuring Claude Code Settings" $currentStep $totalSteps

$claudeSettingsDir = Join-Path $kenlRoot ".claude"
$claudeSettingsFile = Join-Path $claudeSettingsDir "settings.local.json"

if (Test-Path $claudeSettingsFile) {
    Write-Success "Claude Code settings already configured"
    Write-Info "Location: $claudeSettingsFile"
} else {
    Write-Info "Claude Code settings will be created on first run"
}

# Check for skills
$skillsDir = Join-Path $claudeSettingsDir "skills"
if (Test-Path $skillsDir) {
    $skillCount = (Get-ChildItem $skillsDir -Directory).Count
    Write-Success "Claude Code skills found ($skillCount skills)"
} else {
    Write-Info "Skills directory will be created as needed"
}

# ============================================
# STEP 7: Verify VS Code Workspace
# ============================================

$currentStep++
Write-Step "Verifying VS Code Workspace" $currentStep $totalSteps

$workspaceFile = Join-Path $kenlRoot "kenl-workspace.code-workspace"

if (Test-Path $workspaceFile) {
    Write-Success "Workspace file verified"
    Write-Info "Open with: code kenl-workspace.code-workspace"

    # Check if VS Code is available and offer to open
    if ((Get-Command code -ErrorAction SilentlyContinue) -and -not $Quick) {
        $open = Read-Host "`n  Open workspace in VS Code now? (y/N)"
        if ($open -eq 'y' -or $open -eq 'Y') {
            Write-Info "Opening VS Code..."
            & code $workspaceFile
            Write-Success "Workspace opened"
        }
    }
} else {
    Write-Warning "Workspace file not found"
}

# ============================================
# STEP 8: Create Quick Start Aliases
# ============================================

$currentStep++
Write-Step "Creating Quick Start Commands" $currentStep $totalSteps

# Create startup script references
$startupScripts = @{
    "Start-KenlEnvironment" = "env-config\Start-KenlEnvironment.ps1"
    "View-AtomTrail" = "View-AtomTrail.ps1"
    "Write-AtomTrail" = "Write-AtomTrail.ps1"
}

foreach ($scriptName in $startupScripts.Keys) {
    $scriptPath = Join-Path $kenlRoot $startupScripts[$scriptName]
    if (Test-Path $scriptPath) {
        Write-Success "$scriptName available"
    } else {
        Write-Warning "$scriptName not found at $scriptPath"
    }
}

Write-Info "Add to PATH or use full paths: .\env-config\Start-KenlEnvironment.ps1"

# ============================================
# COMPLETION SUMMARY
# ============================================

Write-Complete

Write-Host "[>] Quick Start Commands:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Start Environment:" -ForegroundColor White
Write-Host "    .\env-config\Start-KenlEnvironment.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "  View ATOM Trail:" -ForegroundColor White
Write-Host "    .\View-AtomTrail.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Open Workspace:" -ForegroundColor White
Write-Host "    code kenl-workspace.code-workspace" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Command Center (after profile reload):" -ForegroundColor White
Write-Host "    cc              # Show Command Center" -ForegroundColor Yellow
Write-Host "    ccref           # Refresh display" -ForegroundColor Yellow
Write-Host ""

Write-Host "[i] Documentation:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  README.md                       - Overview" -ForegroundColor Gray
Write-Host "  frameworks/SPIRALSAFE_FRAMEWORK.md    - Core philosophy" -ForegroundColor Gray
Write-Host "  frameworks/ULTRATHINK_PROTOCOL.md     - Strategic thinking" -ForegroundColor Gray
Write-Host "  PUBLICATION_MANIFEST_v1.0.md    - All major works" -ForegroundColor Gray
Write-Host ""

Write-Host "[+] Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  1. Restart PowerShell (to load Command Center)" -ForegroundColor White
Write-Host "  2. Run: .\env-config\Start-KenlEnvironment.ps1" -ForegroundColor White
Write-Host "  3. Open: code kenl-workspace.code-workspace" -ForegroundColor White
Write-Host ""

if (-not $Quick) {
    Write-Host "[*] Optional:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  - Review docs/reports/verification/SYSTEM_VERIFICATION_REPORT.md for deployment status" -ForegroundColor Gray
    Write-Host "  - Deploy SpiralSafe website: cd SpiralSafe && wrangler pages deploy ." -ForegroundColor Gray
    Write-Host "  - Explore ClaudeNPC: cd claudenpc-server-suite" -ForegroundColor Gray
    Write-Host ""
}

# Log to ATOM trail
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"
$dateStamp = Get-Date -Format "yyyyMMdd"
$atomEntry = "$timestamp | ATOM-CONFIG-$dateStamp-999 | [System] | Local | Bootstrap complete - environment ready for immediate use"
Add-Content -Path $atomTrailPath -Value $atomEntry -ErrorAction SilentlyContinue

$timeNow = Get-Date -Format "HH:mm:ss"
Write-Host "Bootstrap completed at $timeNow" -ForegroundColor DarkGray
Write-Host "ATOM trail updated`n" -ForegroundColor DarkGray
