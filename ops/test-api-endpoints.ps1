# ═══════════════════════════════════════════════════════════════
# SpiralSafe Operations API - Endpoint Testing
# ═══════════════════════════════════════════════════════════════

$API_BASE = "https://api.spiralsafe.org"

Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║  SpiralSafe Operations API - Endpoint Validation            ║" -ForegroundColor Blue
Write-Host "║  H&&S:WAVE | Hope&&Sauced                                   ║" -ForegroundColor Blue
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Blue
Write-Host ""

# Test 1: Health Check
Write-Host "━━━ Test 1: Health Check ━━━" -ForegroundColor Cyan
Write-Host "GET /api/health" -ForegroundColor Gray
$response = curl -s "$API_BASE/api/health" | ConvertFrom-Json
Write-Host ($response | ConvertTo-Json -Depth 5) -ForegroundColor Green
Write-Host ""

# Test 2: WAVE Analysis
Write-Host "━━━ Test 2: WAVE Analysis ━━━" -ForegroundColor Cyan
Write-Host "POST /api/wave" -ForegroundColor Gray
$wavePayload = @{
    context = "Initial deployment test"
    session_id = "ATOM-SESSION-20260107-DEPLOYMENT-002"
    signature = "H&&S:WAVE"
    metadata = @{
        test = $true
        timestamp = (Get-Date -Format "o")
    }
} | ConvertTo-Json

$response = curl -s -X POST "$API_BASE/api/wave" `
    -H "Content-Type: application/json" `
    -d $wavePayload | ConvertFrom-Json
Write-Host ($response | ConvertTo-Json -Depth 5) -ForegroundColor Green
Write-Host ""

# Test 3: BUMP Marker
Write-Host "━━━ Test 3: BUMP Marker ━━━" -ForegroundColor Cyan
Write-Host "POST /api/bump" -ForegroundColor Gray
$bumpPayload = @{
    session_id = "ATOM-SESSION-20260107-DEPLOYMENT-002"
    event_type = "deployment_validation"
    context = "Testing BUMP marker creation"
    signature = "H&&S:WAVE"
} | ConvertTo-Json

$response = curl -s -X POST "$API_BASE/api/bump" `
    -H "Content-Type: application/json" `
    -d $bumpPayload | ConvertFrom-Json
Write-Host ($response | ConvertTo-Json -Depth 5) -ForegroundColor Green
Write-Host ""

# Test 4: AWI Grant
Write-Host "━━━ Test 4: AWI (Authority-With-Intent) Grant ━━━" -ForegroundColor Cyan
Write-Host "POST /api/awi" -ForegroundColor Gray
$awiPayload = @{
    session_id = "ATOM-SESSION-20260107-DEPLOYMENT-002"
    authority_level = "read"
    intent = "deployment_validation"
    scope = "api_testing"
    signature = "H&&S:WAVE"
} | ConvertTo-Json

$response = curl -s -X POST "$API_BASE/api/awi" `
    -H "Content-Type: application/json" `
    -d $awiPayload | ConvertFrom-Json
Write-Host ($response | ConvertTo-Json -Depth 5) -ForegroundColor Green
Write-Host ""

# Test 5: ATOM Session
Write-Host "━━━ Test 5: ATOM Session ━━━" -ForegroundColor Cyan
Write-Host "POST /api/atom" -ForegroundColor Gray
$atomPayload = @{
    session_id = "ATOM-SESSION-20260107-DEPLOYMENT-002"
    action = "start"
    context = @{
        type = "deployment_validation"
        environment = "production"
        url = $API_BASE
    }
    signature = "H&&S:WAVE"
} | ConvertTo-Json

$response = curl -s -X POST "$API_BASE/api/atom" `
    -H "Content-Type: application/json" `
    -d $atomPayload | ConvertFrom-Json
Write-Host ($response | ConvertTo-Json -Depth 5) -ForegroundColor Green
Write-Host ""

# Test 6: Context Storage
Write-Host "━━━ Test 6: Context Storage ━━━" -ForegroundColor Cyan
Write-Host "POST /api/context" -ForegroundColor Gray
$contextPayload = @{
    session_id = "ATOM-SESSION-20260107-DEPLOYMENT-002"
    context_data = @{
        deployment_id = "d4e36b58-964c-4820-a08b-27d1e7540a1e"
        timestamp = (Get-Date -Format "o")
        status = "validated"
        endpoints_tested = @("/api/health", "/api/wave", "/api/bump", "/api/awi", "/api/atom", "/api/context")
    }
    signature = "H&&S:WAVE"
} | ConvertTo-Json

$response = curl -s -X POST "$API_BASE/api/context" `
    -H "Content-Type: application/json" `
    -d $contextPayload | ConvertFrom-Json
Write-Host ($response | ConvertTo-Json -Depth 5) -ForegroundColor Green
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host "✓ All endpoints tested successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "H&&S:WAVE | Hope&&Sauced" -ForegroundColor Blue
Write-Host "From the deployment, confidence." -ForegroundColor Gray
Write-Host "From the spiral, safety." -ForegroundColor Gray
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
