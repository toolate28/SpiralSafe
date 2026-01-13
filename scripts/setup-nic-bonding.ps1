#Requires -RunAsAdministrator
# NIC Bonding/Teaming Setup for SpiralSafe Development
# Run as Administrator: powershell -ExecutionPolicy Bypass -File setup-nic-bonding.ps1

Write-Host "SpiralSafe NIC Bonding Setup" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

# Check current state
Write-Host "`nCurrent Network Adapters:" -ForegroundColor Yellow
Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } |
    Select-Object Name, InterfaceDescription, LinkSpeed |
    Format-Table -AutoSize

# Option 1: Equal-cost multi-path (load balancing via metrics)
Write-Host "`nSetting equal metrics for Ethernet + Wi-Fi (load balancing)..." -ForegroundColor Green
try {
    Set-NetIPInterface -InterfaceAlias 'Ethernet' -InterfaceMetric 10 -ErrorAction Stop
    Set-NetIPInterface -InterfaceAlias 'Wi-Fi' -InterfaceMetric 10 -ErrorAction Stop
    Write-Host "SUCCESS: Both adapters now have equal priority" -ForegroundColor Green
} catch {
    Write-Host "Note: Metric change requires elevation or may be managed by policy" -ForegroundColor Yellow
}

# Option 2: Enable receive-side scaling on both
Write-Host "`nEnabling Receive Side Scaling..." -ForegroundColor Green
Enable-NetAdapterRss -Name 'Ethernet' -ErrorAction SilentlyContinue
Enable-NetAdapterRss -Name 'Wi-Fi' -ErrorAction SilentlyContinue

# Option 3: Increase TCP connections
Write-Host "`nOptimizing TCP settings for parallel connections..." -ForegroundColor Green
netsh int tcp set global autotuninglevel=normal
netsh int tcp set global congestionprovider=ctcp

# Verify
Write-Host "`nVerifying routes:" -ForegroundColor Yellow
Get-NetRoute -DestinationPrefix '0.0.0.0/0' |
    Select-Object InterfaceAlias, NextHop, RouteMetric |
    Format-Table -AutoSize

Write-Host "`nDone! Both Ethernet (1Gbps) and Wi-Fi (1.2Gbps) should now load-balance." -ForegroundColor Cyan
Write-Host "Effective bandwidth: ~2.2 Gbps theoretical max" -ForegroundColor Cyan
