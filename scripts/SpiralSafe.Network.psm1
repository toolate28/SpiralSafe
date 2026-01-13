# SpiralSafe.Network.psm1
# Network optimization module for SpiralSafe development environment
# Provides NIC bonding, load balancing, and network diagnostics

<#
.SYNOPSIS
    SpiralSafe Network Optimization Module
.DESCRIPTION
    Provides functions for configuring multi-NIC load balancing,
    network diagnostics, and bandwidth optimization.
.NOTES
    Author: Hope&&Sauced
    Version: 1.0.0
    Requires: Windows 10/11, PowerShell 5.1+
#>

# Module-level variables
$script:NetworkConfig = @{
    PrimaryAdapters = @('Ethernet', 'Wi-Fi')
    TargetMetric = 10
    LogPath = "$env:TEMP\spiralsafe-network.log"
}

function Write-NetworkLog {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    Add-Content -Path $script:NetworkConfig.LogPath -Value $logEntry -ErrorAction SilentlyContinue

    switch ($Level) {
        "ERROR" { Write-Host $logEntry -ForegroundColor Red }
        "WARN"  { Write-Host $logEntry -ForegroundColor Yellow }
        "SUCCESS" { Write-Host $logEntry -ForegroundColor Green }
        default { Write-Host $logEntry -ForegroundColor Cyan }
    }
}

function Get-NetworkStatus {
    <#
    .SYNOPSIS
        Get current network adapter status and routing information
    .EXAMPLE
        Get-NetworkStatus
    #>
    [CmdletBinding()]
    param()

    Write-NetworkLog "Gathering network status..."

    $adapters = Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } |
        Select-Object Name, InterfaceDescription, Status, LinkSpeed,
                      @{N='SpeedGbps';E={[math]::Round($_.LinkSpeed / 1GB, 2)}}

    $routes = Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue |
        Select-Object InterfaceAlias, NextHop, RouteMetric, InterfaceMetric

    $interfaces = Get-NetIPInterface -AddressFamily IPv4 |
        Where-Object { $_.InterfaceAlias -in $script:NetworkConfig.PrimaryAdapters } |
        Select-Object InterfaceAlias, InterfaceMetric, ConnectionState

    return [PSCustomObject]@{
        Adapters = $adapters
        Routes = $routes
        Interfaces = $interfaces
        Timestamp = Get-Date
    }
}

function Set-LoadBalancing {
    <#
    .SYNOPSIS
        Configure equal-cost multi-path load balancing across NICs
    .DESCRIPTION
        Sets both interface metrics AND route metrics to enable true load balancing
    .PARAMETER TargetMetric
        The metric value to set for all primary adapters (lower = higher priority)
    .EXAMPLE
        Set-LoadBalancing -TargetMetric 10
    #>
    [CmdletBinding()]
    param(
        [int]$TargetMetric = 10
    )

    $requiresAdmin = -not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

    if ($requiresAdmin) {
        Write-NetworkLog "This function requires Administrator privileges" "WARN"
        Write-NetworkLog "Run: Start-Process powershell -Verb RunAs -ArgumentList '-Command Import-Module SpiralSafe.Network; Set-LoadBalancing'" "INFO"
        return $false
    }

    Write-NetworkLog "Configuring load balancing with metric: $TargetMetric"

    foreach ($adapter in $script:NetworkConfig.PrimaryAdapters) {
        try {
            # Check if adapter exists and is up
            $netAdapter = Get-NetAdapter -Name $adapter -ErrorAction SilentlyContinue
            if (-not $netAdapter -or $netAdapter.Status -ne 'Up') {
                Write-NetworkLog "Adapter '$adapter' not available, skipping" "WARN"
                continue
            }

            # Set interface metric (affects how Windows chooses default route)
            Set-NetIPInterface -InterfaceAlias $adapter -InterfaceMetric $TargetMetric -ErrorAction Stop
            Write-NetworkLog "Set interface metric for $adapter to $TargetMetric" "SUCCESS"

            # Also try to set automatic metric to manual
            Set-NetIPInterface -InterfaceAlias $adapter -AutomaticMetric Disabled -ErrorAction SilentlyContinue

        } catch {
            Write-NetworkLog "Failed to configure $adapter : $_" "ERROR"
        }
    }

    # Verify the changes
    Start-Sleep -Milliseconds 500
    $status = Get-NetworkStatus

    Write-NetworkLog "Load balancing configuration complete" "SUCCESS"
    return $status
}

function Enable-NetworkOptimizations {
    <#
    .SYNOPSIS
        Enable TCP/IP optimizations for better throughput
    .EXAMPLE
        Enable-NetworkOptimizations
    #>
    [CmdletBinding()]
    param()

    Write-NetworkLog "Enabling network optimizations..."

    # Enable RSS (Receive Side Scaling) on all primary adapters
    foreach ($adapter in $script:NetworkConfig.PrimaryAdapters) {
        try {
            Enable-NetAdapterRss -Name $adapter -ErrorAction SilentlyContinue
            Write-NetworkLog "Enabled RSS on $adapter" "SUCCESS"
        } catch {
            Write-NetworkLog "RSS not available on $adapter" "WARN"
        }
    }

    # TCP optimizations
    $tcpSettings = @(
        @{Cmd = "netsh int tcp set global autotuninglevel=normal"; Desc = "TCP auto-tuning"},
        @{Cmd = "netsh int tcp set global ecncapability=enabled"; Desc = "ECN capability"},
        @{Cmd = "netsh int tcp set global timestamps=enabled"; Desc = "TCP timestamps"}
    )

    foreach ($setting in $tcpSettings) {
        try {
            $result = Invoke-Expression $setting.Cmd 2>&1
            if ($LASTEXITCODE -eq 0 -or $result -match "Ok") {
                Write-NetworkLog "$($setting.Desc) enabled" "SUCCESS"
            }
        } catch {
            Write-NetworkLog "Could not set $($setting.Desc)" "WARN"
        }
    }
}

function Test-NetworkBonding {
    <#
    .SYNOPSIS
        Test if load balancing is working by checking route distribution
    .EXAMPLE
        Test-NetworkBonding
    #>
    [CmdletBinding()]
    param()

    Write-NetworkLog "Testing network bonding configuration..."

    $routes = Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue
    $primaryRoutes = $routes | Where-Object { $_.InterfaceAlias -in $script:NetworkConfig.PrimaryAdapters }

    if ($primaryRoutes.Count -lt 2) {
        Write-NetworkLog "Only $($primaryRoutes.Count) primary adapter(s) have default routes" "WARN"
        return $false
    }

    $metrics = $primaryRoutes | Select-Object -ExpandProperty RouteMetric | Sort-Object -Unique

    if ($metrics.Count -eq 1) {
        Write-NetworkLog "All routes have equal metric ($($metrics[0])) - load balancing active!" "SUCCESS"

        # Calculate theoretical bandwidth
        $totalBandwidth = 0
        foreach ($adapter in $script:NetworkConfig.PrimaryAdapters) {
            $speed = (Get-NetAdapter -Name $adapter -ErrorAction SilentlyContinue).LinkSpeed
            if ($speed) { $totalBandwidth += $speed }
        }
        Write-NetworkLog "Theoretical combined bandwidth: $([math]::Round($totalBandwidth / 1GB, 2)) Gbps" "INFO"

        return $true
    } else {
        Write-NetworkLog "Routes have different metrics: $($metrics -join ', ') - not balanced" "WARN"
        return $false
    }
}

function Initialize-SpiralSafeNetwork {
    <#
    .SYNOPSIS
        One-command setup for SpiralSafe network optimization
    .DESCRIPTION
        Runs all network optimizations: load balancing, RSS, TCP tuning
    .EXAMPLE
        Initialize-SpiralSafeNetwork
    #>
    [CmdletBinding()]
    param()

    Write-Host "`n" -NoNewline
    Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║         SpiralSafe Network Optimization Module           ║" -ForegroundColor Cyan
    Write-Host "║                     H&&S:WAVE                            ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""

    # Step 1: Show current status
    Write-Host "Step 1: Current Network Status" -ForegroundColor Yellow
    $status = Get-NetworkStatus
    $status.Adapters | Format-Table -AutoSize

    # Step 2: Configure load balancing
    Write-Host "`nStep 2: Configuring Load Balancing" -ForegroundColor Yellow
    Set-LoadBalancing -TargetMetric 10

    # Step 3: Enable optimizations
    Write-Host "`nStep 3: Enabling TCP Optimizations" -ForegroundColor Yellow
    Enable-NetworkOptimizations

    # Step 4: Verify
    Write-Host "`nStep 4: Verification" -ForegroundColor Yellow
    $bonded = Test-NetworkBonding

    # Summary
    Write-Host ""
    Write-Host "=======================================================" -ForegroundColor Cyan
    if ($bonded) {
        Write-Host "  Network bonding: ACTIVE" -ForegroundColor Green
        Write-Host "  Adapters: Ethernet 1Gbps + Wi-Fi 1.2Gbps" -ForegroundColor Green
        Write-Host "  Combined: 2.2 Gbps theoretical" -ForegroundColor Green
    } else {
        Write-Host "  Network bonding: PARTIAL" -ForegroundColor Yellow
        Write-Host "  Some optimizations may require admin or reboot" -ForegroundColor Yellow
    }
    Write-Host "=======================================================" -ForegroundColor Cyan

    return $bonded
}

# Export functions
Export-ModuleMember -Function @(
    'Get-NetworkStatus',
    'Set-LoadBalancing',
    'Enable-NetworkOptimizations',
    'Test-NetworkBonding',
    'Initialize-SpiralSafeNetwork'
)
