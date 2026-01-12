<#
.SYNOPSIS
    SpiralSafe Operations CLI
    Local command interface for the coherence engine

.DESCRIPTION
    PowerShell module providing CLI access to SpiralSafe protocols:
    - wave: Coherence analysis
    - bump: Routing and handoff
    - awi: Permission scaffolding  
    - atom: Task orchestration
    - saif: Issue investigation

.NOTES
    H&&S: Structure-preserving operations across substrates
#>

#Requires -Version 7.0

# ═══════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════

$script:SpiralSafeConfig = @{
    ApiBase = $env:SPIRALSAFE_API_BASE ?? 'https://api.spiralsafe.org'
    LocalMode = $false
    Verbose = $false
    DefaultThresholds = @{
        CurlWarning = 0.3
        CurlCritical = 0.6
        DivWarning = 0.4
        DivCritical = 0.7
    }
}

# ═══════════════════════════════════════════════════════════════
# Wave Commands - Coherence Analysis
# ═══════════════════════════════════════════════════════════════

function Invoke-SpiralWave {
    <#
    .SYNOPSIS
        Analyze content coherence using wave.md protocol
    
    .PARAMETER Path
        File or directory to analyze
    
    .PARAMETER Content
        Direct content string to analyze
    
    .PARAMETER Threshold
        Coherence threshold (default: 0.4)
    
    .PARAMETER Recurse
        Recursively analyze directories
    
    .EXAMPLE
        Invoke-SpiralWave -Path ./docs -Recurse
        
    .EXAMPLE
        Invoke-SpiralWave -Content "Some text to analyze"
    #>
    [CmdletBinding()]
    [Alias('wave', 'ss-wave')]
    param(
        [Parameter(Position=0, ParameterSetName='Path')]
        [string]$Path,
        
        [Parameter(ParameterSetName='Content')]
        [string]$Content,
        
        [Parameter()]
        [double]$Threshold = 0.4,
        
        [Parameter()]
        [switch]$Recurse,
        
        [Parameter()]
        [switch]$Local
    )
    
    $results = @()
    
    if ($Path) {
        $items = if ($Recurse) {
            Get-ChildItem -Path $Path -Recurse -File -Include '*.md','*.txt','*.yaml','*.yml'
        } else {
            Get-ChildItem -Path $Path -File -Include '*.md','*.txt','*.yaml','*.yml'
        }
        
        foreach ($item in $items) {
            $content = Get-Content -Path $item.FullName -Raw
            $analysis = if ($Local) {
                Invoke-LocalWaveAnalysis -Content $content
            } else {
                Invoke-ApiWaveAnalysis -Content $content
            }
            
            $results += [PSCustomObject]@{
                Path = $item.FullName
                Curl = $analysis.curl
                Divergence = $analysis.divergence
                Potential = $analysis.potential
                Coherent = $analysis.coherent
                Status = if ($analysis.coherent) { '✓' } else { '⚠' }
            }
        }
    }
    elseif ($Content) {
        $analysis = if ($Local) {
            Invoke-LocalWaveAnalysis -Content $Content
        } else {
            Invoke-ApiWaveAnalysis -Content $Content
        }
        
        $results += [PSCustomObject]@{
            Path = '<direct>'
            Curl = $analysis.curl
            Divergence = $analysis.divergence
            Potential = $analysis.potential
            Coherent = $analysis.coherent
            Status = if ($analysis.coherent) { '✓' } else { '⚠' }
        }
    }
    
    # Output formatted results
    $results | Format-Table -AutoSize
    
    # Summary
    $incoherent = $results | Where-Object { -not $_.Coherent }
    if ($incoherent) {
        Write-Host "`n⚠ $($incoherent.Count) file(s) below coherence threshold:" -ForegroundColor Yellow
        $incoherent | ForEach-Object {
            Write-Host "  - $($_.Path) (curl: $($_.Curl.ToString('F2')), div: $($_.Divergence.ToString('F2')))" -ForegroundColor Yellow
        }
    } else {
        Write-Host "`n✓ All files pass coherence checks" -ForegroundColor Green
    }
    
    return $results
}

function Invoke-LocalWaveAnalysis {
    param([string]$Content)
    
    $paragraphs = $Content -split '\n\n+'
    
    # Simplified local coherence analysis
    $phrases = $paragraphs | ForEach-Object { 
        ($_ -split '[.!?]+' | Where-Object { $_.Trim().Length -gt 20 }).ToLower().Trim()
    }
    $uniquePhrases = $phrases | Select-Object -Unique
    $curl = if ($phrases.Count -gt 0) { 1 - ($uniquePhrases.Count / $phrases.Count) } else { 0 }
    
    $hasConclusion = $Content -match 'therefore|thus|in conclusion|finally|to summarize'
    $questionCount = ([regex]::Matches($Content, '\?')).Count
    $divergence = if ($hasConclusion) { 0.2 } else { [Math]::Min(0.3 + ($questionCount * 0.1), 0.8) }
    
    $potentialMarkers = ($paragraphs | Where-Object { $_ -match 'could|might|perhaps|possibly|future work|TODO|TBD' }).Count
    $potential = [Math]::Min($potentialMarkers * 0.15, 1.0)
    
    $t = $script:SpiralSafeConfig.DefaultThresholds
    
    return @{
        curl = $curl
        divergence = $divergence
        potential = $potential
        coherent = ($curl -lt $t.CurlCritical) -and ([Math]::Abs($divergence) -lt $t.DivCritical)
    }
}

function Invoke-ApiWaveAnalysis {
    param([string]$Content)
    
    $body = @{ content = $Content } | ConvertTo-Json
    $response = Invoke-RestMethod -Uri "$($script:SpiralSafeConfig.ApiBase)/api/wave/analyze" `
        -Method Post -Body $body -ContentType 'application/json'
    return $response
}

# ═══════════════════════════════════════════════════════════════
# Bump Commands - Routing and Handoff
# ═══════════════════════════════════════════════════════════════

function New-SpiralBump {
    <#
    .SYNOPSIS
        Create a bump marker for handoff routing
    
    .PARAMETER Type
        Bump type: WAVE, PASS, PING, SYNC, BLOCK
    
    .PARAMETER To
        Target agent for handoff
    
    .PARAMETER State
        Current state description
    
    .PARAMETER Context
        Additional context as hashtable
    
    .EXAMPLE
        New-SpiralBump -Type WAVE -To copilot -State "PR ready for review"
    #>
    [CmdletBinding()]
    [Alias('bump', 'ss-bump')]
    param(
        [Parameter(Mandatory, Position=0)]
        [ValidateSet('WAVE', 'PASS', 'PING', 'SYNC', 'BLOCK')]
        [string]$Type,
        
        [Parameter(Mandatory, Position=1)]
        [string]$To,
        
        [Parameter(Position=2)]
        [string]$State = 'pending',
        
        [Parameter()]
        [hashtable]$Context = @{},
        
        [Parameter()]
        [string]$From = 'cli'
    )
    
    $bump = @{
        type = $Type
        from = $From
        to = $To
        state = $State
        context = $Context
    }
    
    try {
        $body = $bump | ConvertTo-Json
        $response = Invoke-RestMethod -Uri "$($script:SpiralSafeConfig.ApiBase)/api/bump/create" `
            -Method Post -Body $body -ContentType 'application/json'
        
        Write-Host "✓ Bump created: $($response.id)" -ForegroundColor Green
        Write-Host "  H&&S:$Type → $To" -ForegroundColor Cyan
        Write-Host "  State: $State" -ForegroundColor Gray
        
        # Copy marker to clipboard
        $marker = "H&&S:$Type"
        Set-Clipboard -Value $marker
        Write-Host "`n  Marker copied to clipboard: $marker" -ForegroundColor DarkGray
        
        return $response
    }
    catch {
        Write-Host "✗ Failed to create bump: $_" -ForegroundColor Red
        
        # Return local marker anyway
        $marker = "H&&S:$Type"
        Set-Clipboard -Value $marker
        Write-Host "`n  Local marker copied to clipboard: $marker" -ForegroundColor DarkGray
        
        return @{ type = $Type; to = $To; state = $State; local = $true }
    }
}

function Get-SpiralBumps {
    <#
    .SYNOPSIS
        List pending bump markers
    #>
    [CmdletBinding()]
    [Alias('bumps', 'ss-bumps')]
    param(
        [Parameter()]
        [switch]$All
    )
    
    try {
        $response = Invoke-RestMethod -Uri "$($script:SpiralSafeConfig.ApiBase)/api/bump/pending"
        
        if ($response.Count -eq 0) {
            Write-Host "✓ No pending bumps" -ForegroundColor Green
            return @()
        }
        
        Write-Host "Pending Bumps:" -ForegroundColor Cyan
        $response | ForEach-Object {
            $age = [DateTime]::Now - [DateTime]::Parse($_.timestamp)
            Write-Host "  [$($_.type)] $($_.from_agent) → $($_.to_agent)" -ForegroundColor Yellow
            Write-Host "    State: $($_.state)" -ForegroundColor Gray
            Write-Host "    Age: $($age.ToString('hh\:mm\:ss'))" -ForegroundColor DarkGray
        }
        
        return $response
    }
    catch {
        Write-Host "✗ Failed to fetch bumps: $_" -ForegroundColor Red
        return @()
    }
}

function Resolve-SpiralBump {
    <#
    .SYNOPSIS
        Mark a bump as resolved
    #>
    [CmdletBinding()]
    [Alias('resolve-bump', 'ss-resolve')]
    param(
        [Parameter(Mandatory, Position=0)]
        [string]$Id
    )
    
    try {
        $response = Invoke-RestMethod -Uri "$($script:SpiralSafeConfig.ApiBase)/api/bump/resolve/$Id" `
            -Method Put
        
        Write-Host "✓ Bump resolved: $Id" -ForegroundColor Green
        return $response
    }
    catch {
        Write-Host "✗ Failed to resolve bump: $_" -ForegroundColor Red
    }
}

# ═══════════════════════════════════════════════════════════════
# AWI Commands - Permission Scaffolding
# ═══════════════════════════════════════════════════════════════

function Request-SpiralPermission {
    <#
    .SYNOPSIS
        Request AWI permission grant
    
    .PARAMETER Intent
        Clear statement of intent
    
    .PARAMETER Resources
        Resources to access
    
    .PARAMETER Actions
        Actions to perform
    
    .PARAMETER Level
        Permission level (0-4)
    
    .PARAMETER TTL
        Time-to-live in seconds
    
    .EXAMPLE
        Request-SpiralPermission -Intent "Deploy docs update" -Resources "docs/*" -Actions "modify" -Level 2
    #>
    [CmdletBinding()]
    [Alias('awi', 'ss-awi')]
    param(
        [Parameter(Mandatory, Position=0)]
        [string]$Intent,
        
        [Parameter(Mandatory)]
        [string[]]$Resources,
        
        [Parameter(Mandatory)]
        [string[]]$Actions,
        
        [Parameter()]
        [ValidateRange(0,4)]
        [int]$Level = 1,
        
        [Parameter()]
        [int]$TTL = 3600
    )
    
    $request = @{
        intent = $Intent
        scope = @{
            resources = $Resources
            actions = $Actions
        }
        level = $Level
        ttl_seconds = $TTL
    }
    
    try {
        $body = $request | ConvertTo-Json -Depth 3
        $response = Invoke-RestMethod -Uri "$($script:SpiralSafeConfig.ApiBase)/api/awi/request" `
            -Method Post -Body $body -ContentType 'application/json'
        
        Write-Host "✓ AWI Grant Created" -ForegroundColor Green
        Write-Host "  ID: $($response.id)" -ForegroundColor Cyan
        Write-Host "  Intent: $Intent" -ForegroundColor Gray
        Write-Host "  Level: $Level" -ForegroundColor Gray
        Write-Host "  Expires: $($response.expires_at)" -ForegroundColor DarkGray
        
        # Store grant ID in environment for subsequent operations
        $env:SPIRALSAFE_AWI_GRANT = $response.id
        
        return $response
    }
    catch {
        Write-Host "✗ Failed to create AWI grant: $_" -ForegroundColor Red
    }
}

function Test-SpiralPermission {
    <#
    .SYNOPSIS
        Verify an AWI grant allows an action
    #>
    [CmdletBinding()]
    [Alias('test-awi', 'ss-test-awi')]
    param(
        [Parameter(Position=0)]
        [string]$GrantId = $env:SPIRALSAFE_AWI_GRANT,
        
        [Parameter(Mandatory, Position=1)]
        [string]$Action
    )
    
    if (-not $GrantId) {
        Write-Host "✗ No grant ID provided or stored in environment" -ForegroundColor Red
        return $false
    }
    
    try {
        $body = @{ grant_id = $GrantId; action = $Action } | ConvertTo-Json
        $response = Invoke-RestMethod -Uri "$($script:SpiralSafeConfig.ApiBase)/api/awi/verify" `
            -Method Post -Body $body -ContentType 'application/json'
        
        if ($response.valid) {
            Write-Host "✓ Action permitted: $Action" -ForegroundColor Green
        } else {
            Write-Host "✗ Action denied: $Action" -ForegroundColor Red
        }
        
        return $response.valid
    }
    catch {
        Write-Host "✗ Failed to verify permission: $_" -ForegroundColor Red
        return $false
    }
}

# ═══════════════════════════════════════════════════════════════
# ATOM Commands - Task Orchestration
# ═══════════════════════════════════════════════════════════════

function New-SpiralAtom {
    <#
    .SYNOPSIS
        Create a new atomic task unit
    
    .EXAMPLE
        New-SpiralAtom -Name "Write README" -Molecule "docs" -Compound "spiralsafe" -Criteria @{has_quickstart=$true}
    #>
    [CmdletBinding()]
    [Alias('atom', 'ss-atom')]
    param(
        [Parameter(Mandatory, Position=0)]
        [string]$Name,
        
        [Parameter(Mandatory)]
        [string]$Molecule,
        
        [Parameter(Mandatory)]
        [string]$Compound,
        
        [Parameter()]
        [hashtable]$Criteria = @{},
        
        [Parameter()]
        [string[]]$Requires = @(),
        
        [Parameter()]
        [string]$Assignee = 'unassigned'
    )
    
    $atom = @{
        name = $Name
        molecule = $Molecule
        compound = $Compound
        verification = @{
            criteria = $Criteria
            automated = $Criteria.Count -gt 0
        }
        dependencies = @{
            requires = $Requires
            blocks = @()
        }
        assignee = $Assignee
    }
    
    try {
        $body = $atom | ConvertTo-Json -Depth 4
        $response = Invoke-RestMethod -Uri "$($script:SpiralSafeConfig.ApiBase)/api/atom/create" `
            -Method Post -Body $body -ContentType 'application/json'
        
        Write-Host "✓ Atom created: $($response.id)" -ForegroundColor Green
        Write-Host "  $Compound / $Molecule / $Name" -ForegroundColor Cyan
        
        return $response
    }
    catch {
        Write-Host "✗ Failed to create atom: $_" -ForegroundColor Red
    }
}

function Set-SpiralAtomStatus {
    <#
    .SYNOPSIS
        Update atom status
    #>
    [CmdletBinding()]
    [Alias('atom-status', 'ss-atom-status')]
    param(
        [Parameter(Mandatory, Position=0)]
        [string]$Id,
        
        [Parameter(Mandatory, Position=1)]
        [ValidateSet('pending', 'in_progress', 'blocked', 'complete', 'verified')]
        [string]$Status
    )
    
    try {
        $body = @{ status = $Status } | ConvertTo-Json
        $response = Invoke-RestMethod -Uri "$($script:SpiralSafeConfig.ApiBase)/api/atom/status/$Id" `
            -Method Put -Body $body -ContentType 'application/json'
        
        $icon = switch ($Status) {
            'pending' { '○' }
            'in_progress' { '◐' }
            'blocked' { '✗' }
            'complete' { '●' }
            'verified' { '✓' }
        }
        
        Write-Host "$icon Atom $Id → $Status" -ForegroundColor Cyan
        return $response
    }
    catch {
        Write-Host "✗ Failed to update atom: $_" -ForegroundColor Red
    }
}

# ═══════════════════════════════════════════════════════════════
# SAIF Commands - Issue Investigation
# ═══════════════════════════════════════════════════════════════

function Start-SpiralInvestigation {
    <#
    .SYNOPSIS
        Begin a SAIF investigation
    
    .DESCRIPTION
        Initializes a systematic analysis following the SAIF protocol:
        Symptom → Analysis → Hypothesis → Intervention → Verification → Documentation
    
    .EXAMPLE
        Start-SpiralInvestigation -Title "Deploy failure" -Symptoms "Worker timeout", "KV write error"
    #>
    [CmdletBinding()]
    [Alias('saif', 'ss-saif')]
    param(
        [Parameter(Mandatory, Position=0)]
        [string]$Title,
        
        [Parameter(Mandatory)]
        [string[]]$Symptoms
    )
    
    $investigation = @{
        title = $Title
        phase = 'symptom'
        symptoms = $Symptoms
    }
    
    Write-Host "`n═══════════════════════════════════════════════════════════════" -ForegroundColor DarkCyan
    Write-Host "  SAIF Investigation: $Title" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor DarkCyan
    Write-Host "`n  Phase 1: SYMPTOM DOCUMENTATION" -ForegroundColor Yellow
    Write-Host "  Recorded symptoms:" -ForegroundColor Gray
    $Symptoms | ForEach-Object { Write-Host "    • $_" -ForegroundColor White }
    Write-Host "`n  Next: Proceed to analysis phase with Invoke-SpiralAnalysis" -ForegroundColor DarkGray
    
    # Store in session for pipeline
    $script:CurrentInvestigation = $investigation
    
    return $investigation
}

# ═══════════════════════════════════════════════════════════════
# Health & Status
# ═══════════════════════════════════════════════════════════════

function Get-SpiralStatus {
    <#
    .SYNOPSIS
        Check SpiralSafe API health and local configuration
    #>
    [CmdletBinding()]
    [Alias('ss-status')]
    param()
    
    Write-Host "`nSpiralSafe Operations Status" -ForegroundColor Cyan
    Write-Host "════════════════════════════════════════" -ForegroundColor DarkCyan
    
    # Local config
    Write-Host "`n  Local Configuration:" -ForegroundColor Yellow
    Write-Host "    API Base: $($script:SpiralSafeConfig.ApiBase)" -ForegroundColor Gray
    Write-Host "    AWI Grant: $(if ($env:SPIRALSAFE_AWI_GRANT) { $env:SPIRALSAFE_AWI_GRANT } else { '(none)' })" -ForegroundColor Gray
    
    # API health
    Write-Host "`n  API Status:" -ForegroundColor Yellow
    try {
        $health = Invoke-RestMethod -Uri "$($script:SpiralSafeConfig.ApiBase)/api/health" -TimeoutSec 5
        Write-Host "    Status: $($health.status)" -ForegroundColor $(if ($health.status -eq 'healthy') { 'Green' } else { 'Yellow' })
        Write-Host "    D1: $(if ($health.checks.d1) { '✓' } else { '✗' })" -ForegroundColor $(if ($health.checks.d1) { 'Green' } else { 'Red' })
        Write-Host "    KV: $(if ($health.checks.kv) { '✓' } else { '✗' })" -ForegroundColor $(if ($health.checks.kv) { 'Green' } else { 'Red' })
        Write-Host "    R2: $(if ($health.checks.r2) { '✓' } else { '✗' })" -ForegroundColor $(if ($health.checks.r2) { 'Green' } else { 'Red' })
    }
    catch {
        Write-Host "    Status: UNREACHABLE" -ForegroundColor Red
        Write-Host "    (Using local mode)" -ForegroundColor DarkGray
    }
    
    Write-Host ""
}

# ═══════════════════════════════════════════════════════════════
# Module Export
# ═══════════════════════════════════════════════════════════════

Export-ModuleMember -Function @(
    'Invoke-SpiralWave',
    'New-SpiralBump',
    'Get-SpiralBumps',
    'Resolve-SpiralBump',
    'Request-SpiralPermission',
    'Test-SpiralPermission',
    'New-SpiralAtom',
    'Set-SpiralAtomStatus',
    'Start-SpiralInvestigation',
    'Get-SpiralStatus'
) -Alias @(
    'wave', 'ss-wave',
    'bump', 'ss-bump',
    'bumps', 'ss-bumps',
    'resolve-bump', 'ss-resolve',
    'awi', 'ss-awi',
    'test-awi', 'ss-test-awi',
    'atom', 'ss-atom',
    'atom-status', 'ss-atom-status',
    'saif', 'ss-saif',
    'ss-status'
)
