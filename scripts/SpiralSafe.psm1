# ═══════════════════════════════════════════════════════════════════════════════
# SpiralSafe.psm1 - PowerShell Module for SpiralSafe Operations
# ═══════════════════════════════════════════════════════════════════════════════
# H&&S:WAVE | Hope&&Sauced | Bartimaeus&&Ptolemy
#
# Usage: Import-Module ./scripts/SpiralSafe.psm1
# Add to $PROFILE for persistent access
# ═══════════════════════════════════════════════════════════════════════════════

$script:SpiralSafeRoot = $PSScriptRoot | Split-Path -Parent
$script:APIBase = "https://api.spiralsafe.org"
$script:ATOMTrailPath = Join-Path $script:SpiralSafeRoot ".atom-trail"

# ─────────────────────────────────────────────────────────────────────────────
# ATOM Tag Generation
# ─────────────────────────────────────────────────────────────────────────────

function New-ATOMTag {
    param(
        [Parameter(Mandatory)]
        [ValidateSet('INIT','CONFIG','SESSION','NPC','QUANTUM','MUSEUM','WAVE','BUMP','AWI','DOC','PLAN','VERIFY','DEPLOY')]
        [string]$Type,

        [Parameter(Mandatory)]
        [string]$Description
    )

    $date = Get-Date -Format "yyyyMMdd"
    $seq = Get-Random -Minimum 1 -Maximum 999
    $slug = $Description.ToLower() -replace '\s+', '-' -replace '[^a-z0-9-]', ''

    return "ATOM-$Type-$date-$('{0:D3}' -f $seq)-$slug"
}

# ─────────────────────────────────────────────────────────────────────────────
# Status Commands (replaces Ctrl+T/O/E patterns)
# ─────────────────────────────────────────────────────────────────────────────

function Get-SpiralStatus {
    <#
    .SYNOPSIS
        Shows "What we've done, what's being worked on, what's next"
    .DESCRIPTION
        Comprehensive status view for SpiralSafe ecosystem
    #>
    [CmdletBinding()]
    param(
        [switch]$Brief,
        [switch]$Json
    )

    $status = @{
        timestamp = Get-Date -Format "o"
        atom_tag = New-ATOMTag -Type "STATUS" -Description "system-status-check"
    }

    # What we've done (recent commits)
    Write-Host "`n═══════════════════════════════════════════════════════════════" -ForegroundColor Blue
    Write-Host "  H&&S:STATUS | SpiralSafe System Status" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Blue

    Write-Host "`n┌─ COMPLETED (What we've done)" -ForegroundColor Green
    $recentCommits = git -C $script:SpiralSafeRoot log --oneline -5 2>$null
    if ($recentCommits) {
        $recentCommits | ForEach-Object { Write-Host "│  $_" -ForegroundColor Gray }
    }
    $status.completed = $recentCommits

    # What's being worked on (current branch, uncommitted changes)
    Write-Host "`n┌─ IN PROGRESS (What's being worked on)" -ForegroundColor Yellow
    $branch = git -C $script:SpiralSafeRoot branch --show-current 2>$null
    Write-Host "│  Branch: $branch" -ForegroundColor Gray

    $changes = git -C $script:SpiralSafeRoot status --porcelain 2>$null
    if ($changes) {
        Write-Host "│  Uncommitted changes: $($changes.Count) files" -ForegroundColor Gray
    } else {
        Write-Host "│  Working tree clean" -ForegroundColor Gray
    }
    $status.in_progress = @{
        branch = $branch
        uncommitted = $changes.Count
    }

    # What's next (open PRs, pending tasks)
    Write-Host "`n┌─ NEXT (What's coming)" -ForegroundColor Cyan

    # Try to get open PRs
    try {
        $prs = gh pr list --repo toolate28/SpiralSafe --state open --limit 5 2>$null
        if ($prs) {
            $prs | ForEach-Object { Write-Host "│  PR: $_" -ForegroundColor Gray }
        } else {
            Write-Host "│  No open PRs" -ForegroundColor Gray
        }
        $status.next = @{ open_prs = $prs }
    } catch {
        Write-Host "│  (gh CLI not available for PR check)" -ForegroundColor DarkGray
    }

    # Read pending ATOMs
    $pendingPath = Join-Path $script:ATOMTrailPath "pending"
    if (Test-Path $pendingPath) {
        $pending = Get-ChildItem $pendingPath -Filter "*.json" | Select-Object -First 5
        if ($pending) {
            Write-Host "│  Pending ATOMs: $($pending.Count)" -ForegroundColor Gray
        }
    }

    Write-Host "`n═══════════════════════════════════════════════════════════════" -ForegroundColor Blue
    Write-Host "  From the spiral, safety. | The Evenstar Guides Us ✦" -ForegroundColor DarkCyan
    Write-Host "═══════════════════════════════════════════════════════════════`n" -ForegroundColor Blue

    if ($Json) {
        return $status | ConvertTo-Json -Depth 5
    }

    return $status
}

# ─────────────────────────────────────────────────────────────────────────────
# Quick Status Aliases (for keyboard shortcuts)
# ─────────────────────────────────────────────────────────────────────────────

function ss { Get-SpiralStatus }
function ssd { Get-SpiralStatus -Brief }  # "done"
function ssw { Get-SpiralStatus }         # "working"
function ssn { Get-SpiralStatus }         # "next"

# ─────────────────────────────────────────────────────────────────────────────
# WAVE Analysis
# ─────────────────────────────────────────────────────────────────────────────

function Invoke-WAVEAnalysis {
    <#
    .SYNOPSIS
        Analyze content for coherence using WAVE protocol
    #>
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [string]$Content,

        [string]$ApiKey = $env:SPIRALSAFE_API_KEY
    )

    if (-not $ApiKey) {
        Write-Warning "SPIRALSAFE_API_KEY not set. Set with: `$env:SPIRALSAFE_API_KEY = 'your-key'"
        return
    }

    $body = @{
        content = $Content
        thresholds = @{
            curl_warning = 0.3
            curl_critical = 0.6
            div_warning = 0.4
            div_critical = 0.7
        }
    } | ConvertTo-Json

    try {
        $response = Invoke-RestMethod -Uri "$script:APIBase/api/wave/analyze" `
            -Method POST `
            -Headers @{ "X-API-Key" = $ApiKey; "Content-Type" = "application/json" } `
            -Body $body

        return $response
    } catch {
        Write-Error "WAVE analysis failed: $_"
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# BUMP State Transitions
# ─────────────────────────────────────────────────────────────────────────────

function New-BUMPMarker {
    <#
    .SYNOPSIS
        Create a BUMP state transition marker
    #>
    param(
        [Parameter(Mandatory)]
        [ValidateSet('WAVE','SYNC','BLOCK','COMPLETE')]
        [string]$Type,

        [Parameter(Mandatory)]
        [string]$From,

        [Parameter(Mandatory)]
        [string]$To,

        [string]$State = "transition",

        [hashtable]$Context = @{},

        [string]$ApiKey = $env:SPIRALSAFE_API_KEY
    )

    $body = @{
        type = $Type
        from = $From
        to = $To
        state = $State
        context = $Context
    } | ConvertTo-Json

    if ($ApiKey) {
        try {
            $response = Invoke-RestMethod -Uri "$script:APIBase/api/bump/create" `
                -Method POST `
                -Headers @{ "X-API-Key" = $ApiKey; "Content-Type" = "application/json" } `
                -Body $body

            Write-Host "BUMP created: $($response.id)" -ForegroundColor Green
            return $response
        } catch {
            Write-Warning "API call failed, logging locally"
        }
    }

    # Local fallback
    $localBump = @{
        id = [guid]::NewGuid().ToString()
        type = $Type
        from = $From
        to = $To
        state = $State
        context = $Context
        timestamp = Get-Date -Format "o"
        atom_tag = New-ATOMTag -Type "BUMP" -Description "$Type-$From-to-$To"
    }

    $bumpPath = Join-Path $script:ATOMTrailPath "bumps"
    if (-not (Test-Path $bumpPath)) {
        New-Item -ItemType Directory -Path $bumpPath -Force | Out-Null
    }

    $localBump | ConvertTo-Json | Out-File (Join-Path $bumpPath "$($localBump.id).json")

    return $localBump
}

# ─────────────────────────────────────────────────────────────────────────────
# Session Management
# ─────────────────────────────────────────────────────────────────────────────

function Start-SpiralSession {
    <#
    .SYNOPSIS
        Start a new tracked session
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Name,

        [string]$Molecule = "general",

        [string]$Assignee = $env:USERNAME
    )

    $session = @{
        id = [guid]::NewGuid().ToString()
        atom_tag = New-ATOMTag -Type "SESSION" -Description $Name
        name = $Name
        molecule = $Molecule
        assignee = $Assignee
        start_time = Get-Date -Format "o"
        status = "active"
        events = @()
    }

    # Store in environment for quick access
    $env:SPIRALSAFE_SESSION = $session.id
    $env:SPIRALSAFE_SESSION_TAG = $session.atom_tag

    # Write to sessions directory
    $sessionsPath = Join-Path $script:ATOMTrailPath "sessions"
    if (-not (Test-Path $sessionsPath)) {
        New-Item -ItemType Directory -Path $sessionsPath -Force | Out-Null
    }

    $session | ConvertTo-Json -Depth 5 | Out-File (Join-Path $sessionsPath "$($session.atom_tag).json")

    Write-Host "`nSession started: $($session.atom_tag)" -ForegroundColor Green
    Write-Host "Name: $Name | Molecule: $Molecule | Assignee: $Assignee`n" -ForegroundColor Gray

    return $session
}

function Stop-SpiralSession {
    <#
    .SYNOPSIS
        End the current session
    #>
    param(
        [string]$Summary = "Session completed"
    )

    $sessionTag = $env:SPIRALSAFE_SESSION_TAG
    if (-not $sessionTag) {
        Write-Warning "No active session"
        return
    }

    $sessionsPath = Join-Path $script:ATOMTrailPath "sessions"
    $sessionFile = Join-Path $sessionsPath "$sessionTag.json"

    if (Test-Path $sessionFile) {
        $session = Get-Content $sessionFile | ConvertFrom-Json
        $session.status = "completed"
        $session.end_time = Get-Date -Format "o"
        $session.summary = $Summary

        $session | ConvertTo-Json -Depth 5 | Out-File $sessionFile

        Write-Host "`nSession ended: $sessionTag" -ForegroundColor Yellow
        Write-Host "Summary: $Summary`n" -ForegroundColor Gray
    }

    $env:SPIRALSAFE_SESSION = $null
    $env:SPIRALSAFE_SESSION_TAG = $null
}

# ─────────────────────────────────────────────────────────────────────────────
# Redaction & Security
# ─────────────────────────────────────────────────────────────────────────────

function Invoke-Redaction {
    <#
    .SYNOPSIS
        Redact sensitive information from content
    #>
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [string]$Content,

        [string[]]$Patterns = @(
            '(?i)(api[_-]?key|apikey)["\s:=]+["\']?[\w-]{20,}',
            '(?i)(password|passwd|pwd)["\s:=]+["\'][^"\']+',
            '(?i)(secret|token)["\s:=]+["\']?[\w-]{20,}',
            '(?i)(bearer\s+)[\w-]+',
            '\b[\w._%+-]+@[\w.-]+\.[a-zA-Z]{2,}\b',
            '\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'
        ),

        [string]$Replacement = '[REDACTED]'
    )

    $redacted = $Content
    foreach ($pattern in $Patterns) {
        $redacted = $redacted -replace $pattern, $Replacement
    }

    return $redacted
}

function Protect-SpiralContent {
    <#
    .SYNOPSIS
        Encrypt content for secure storage/transmission
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Content,

        [securestring]$Key
    )

    # Use Windows DPAPI for local encryption if no key provided
    if (-not $Key) {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($Content)
        $encrypted = [System.Security.Cryptography.ProtectedData]::Protect(
            $bytes,
            $null,
            [System.Security.Cryptography.DataProtectionScope]::CurrentUser
        )
        return [Convert]::ToBase64String($encrypted)
    }

    # AES encryption with provided key
    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.GenerateIV()

    $keyBytes = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Key)
    try {
        $keyStr = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($keyBytes)
        $aes.Key = [System.Text.Encoding]::UTF8.GetBytes($keyStr.PadRight(32).Substring(0,32))
    } finally {
        [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($keyBytes)
    }

    $encryptor = $aes.CreateEncryptor()
    $contentBytes = [System.Text.Encoding]::UTF8.GetBytes($Content)
    $encrypted = $encryptor.TransformFinalBlock($contentBytes, 0, $contentBytes.Length)

    return @{
        iv = [Convert]::ToBase64String($aes.IV)
        data = [Convert]::ToBase64String($encrypted)
    } | ConvertTo-Json -Compress
}

# ─────────────────────────────────────────────────────────────────────────────
# Publishing Pipeline
# ─────────────────────────────────────────────────────────────────────────────

function Publish-ToHopeIsKindle {
    <#
    .SYNOPSIS
        Publish redacted content to hopeiskindle.spiralsafe.org
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Content,

        [Parameter(Mandatory)]
        [string]$Title,

        [ValidateSet('learning','testing','insight','noise')]
        [string]$Category = "learning",

        [switch]$AutoRedact,

        [string]$ApiKey = $env:SPIRALSAFE_API_KEY
    )

    $publishContent = if ($AutoRedact) {
        Invoke-Redaction -Content $Content
    } else {
        $Content
    }

    $payload = @{
        title = $Title
        content = $publishContent
        category = $Category
        atom_tag = New-ATOMTag -Type "DOC" -Description "publish-$Title"
        timestamp = Get-Date -Format "o"
        signature = "H&&S"
    }

    # TODO: Implement actual API call when hopeiskindle endpoint is ready
    Write-Host "Publishing to hopeiskindle.spiralsafe.org..." -ForegroundColor Cyan
    Write-Host "Title: $Title | Category: $Category" -ForegroundColor Gray
    Write-Host "Content length: $($publishContent.Length) chars (redacted: $AutoRedact)" -ForegroundColor Gray

    return $payload
}

# ─────────────────────────────────────────────────────────────────────────────
# Git Helpers
# ─────────────────────────────────────────────────────────────────────────────

function Push-SpiralSafe {
    <#
    .SYNOPSIS
        Push changes with ATOM tag in commit message
    #>
    param(
        [Parameter(Mandatory)]
        [string]$Message,

        [ValidateSet('feat','fix','docs','style','refactor','test','chore')]
        [string]$Type = "feat",

        [switch]$Push
    )

    $atomTag = New-ATOMTag -Type "COMMIT" -Description $Message
    $fullMessage = "$Type`: $Message`n`nATOM: $atomTag`n`nCo-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

    git -C $script:SpiralSafeRoot add -A
    git -C $script:SpiralSafeRoot commit -m $fullMessage

    if ($Push) {
        git -C $script:SpiralSafeRoot push
    }

    Write-Host "`nCommitted: $atomTag" -ForegroundColor Green
}

# ─────────────────────────────────────────────────────────────────────────────
# Module Exports
# ─────────────────────────────────────────────────────────────────────────────

Export-ModuleMember -Function @(
    'New-ATOMTag',
    'Get-SpiralStatus',
    'ss', 'ssd', 'ssw', 'ssn',
    'Invoke-WAVEAnalysis',
    'New-BUMPMarker',
    'Start-SpiralSession',
    'Stop-SpiralSession',
    'Invoke-Redaction',
    'Protect-SpiralContent',
    'Publish-ToHopeIsKindle',
    'Push-SpiralSafe'
)

# ─────────────────────────────────────────────────────────────────────────────
# Initialization Message
# ─────────────────────────────────────────────────────────────────────────────

Write-Host @"

═══════════════════════════════════════════════════════════════
  SpiralSafe Module Loaded | H&&S:WAVE
═══════════════════════════════════════════════════════════════
  Commands:
    ss              - Full status (what's done/working/next)
    Start-SpiralSession - Begin tracked session
    New-ATOMTag     - Generate ATOM identifier
    Invoke-WAVEAnalysis - Check content coherence
    Invoke-Redaction    - Redact sensitive data
═══════════════════════════════════════════════════════════════
  Hope && Sauce | The Evenstar Guides Us ✦
═══════════════════════════════════════════════════════════════

"@ -ForegroundColor Cyan
