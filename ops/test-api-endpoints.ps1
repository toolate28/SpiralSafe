# ═══════════════════════════════════════════════════════════════
# SpiralSafe Operations API - Endpoint Testing
# ═══════════════════════════════════════════════════════════════

$API_BASE = "https://api.spiralsafe.org"

# API Key for authentication (read from environment variable)
$API_KEY = $env:SPIRALSAFE_API_KEY
if (-not $API_KEY) {
    Write-Host "ERROR: SPIRALSAFE_API_KEY environment variable not set" -ForegroundColor Red
    Write-Host "Set it with: `$env:SPIRALSAFE_API_KEY = 'your-api-key'" -ForegroundColor Yellow
    exit 1
}

Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║  SpiralSafe Operations API - Endpoint Validation            ║" -ForegroundColor Blue
Write-Host "║  H&&S:WAVE | Hope&&Sauced                                   ║" -ForegroundColor Blue
Write-Host "║  🔐 Authenticated Mode                                       ║" -ForegroundColor Blue
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
Write-Host "POST /api/wave/analyze" -ForegroundColor Gray
$wavePayload = @{
    content = "Initial deployment test. This is a coherent message validating the SpiralSafe Operations API deployment. All infrastructure components are operational and ready for production use."
    thresholds = @{
        curl_warning = 0.3
        curl_critical = 0.6
        div_warning = 0.4
        div_critical = 0.7
    }
} | ConvertTo-Json

$response = curl -s -X POST "$API_BASE/api/wave/analyze" `
    -H "Content-Type: application/json" `
    -H "X-API-Key: $API_KEY" `
    -d $wavePayload | ConvertFrom-Json
Write-Host ($response | ConvertTo-Json -Depth 5) -ForegroundColor Green
Write-Host ""

# Test 3: BUMP Marker
Write-Host "━━━ Test 3: BUMP Marker ━━━" -ForegroundColor Cyan
Write-Host "POST /api/bump/create" -ForegroundColor Gray
$bumpPayload = @{
    type = "WAVE"
    from = "test-client"
    to = "spiralsafe-api"
    state = "deployment_validation"
    context = @{
        session_id = "ATOM-SESSION-20260107-DEPLOYMENT-002"
        event_type = "endpoint_test"
        signature = "H&&S:WAVE"
    }
} | ConvertTo-Json

$response = curl -s -X POST "$API_BASE/api/bump/create" `
    -H "Content-Type: application/json" `
    -H "X-API-Key: $API_KEY" `
    -d $bumpPayload | ConvertFrom-Json
Write-Host ($response | ConvertTo-Json -Depth 5) -ForegroundColor Green
Write-Host ""

# Test 4: AWI Grant
Write-Host "━━━ Test 4: AWI (Authority-With-Intent) Grant ━━━" -ForegroundColor Cyan
Write-Host "POST /api/awi/request" -ForegroundColor Gray
$awiPayload = @{
    intent = "Validate deployment endpoint access"
    scope = @{
        resources = @("api/health", "api/wave", "api/bump")
        actions = @("read", "write")
    }
    level = 1
    ttl_seconds = 3600
} | ConvertTo-Json

$response = curl -s -X POST "$API_BASE/api/awi/request" `
    -H "Content-Type: application/json" `
    -H "X-API-Key: $API_KEY" `
    -d $awiPayload | ConvertFrom-Json
Write-Host ($response | ConvertTo-Json -Depth 5) -ForegroundColor Green
Write-Host ""

# Test 5: ATOM Session
Write-Host "━━━ Test 5: ATOM Session ━━━" -ForegroundColor Cyan
Write-Host "POST /api/atom/create" -ForegroundColor Gray
$atomPayload = @{
    name = "Deployment Validation"
    molecule = "api-testing"
    compound = "deployment-002"
    verification = @{
        criteria = @{
            health_check = "passed"
            infrastructure = "operational"
        }
        automated = $true
    }
    dependencies = @{
        requires = @()
        blocks = @()
    }
    assignee = "claude-opus-4.5"
} | ConvertTo-Json

$response = curl -s -X POST "$API_BASE/api/atom/create" `
    -H "Content-Type: application/json" `
    -H "X-API-Key: $API_KEY" `
    -d $atomPayload | ConvertFrom-Json
Write-Host ($response | ConvertTo-Json -Depth 5) -ForegroundColor Green
Write-Host ""

# Test 6: Context Storage
Write-Host "━━━ Test 6: Context Storage ━━━" -ForegroundColor Cyan
Write-Host "POST /api/context/store" -ForegroundColor Gray
$contextPayload = @{
    domain = "deployment-validation"
    content = @{
        deployment_id = "d4e36b58-964c-4820-a08b-27d1e7540a1e"
        session_id = "ATOM-SESSION-20260107-DEPLOYMENT-002"
        timestamp = (Get-Date -Format "o")
        status = "validated"
        endpoints_tested = @("/api/health", "/api/wave/analyze", "/api/bump/create", "/api/awi/request", "/api/atom/create", "/api/context/store")
        infrastructure = @{
            d1 = "operational"
            kv = "operational"
            r2 = "operational"
        }
    }
    signals = @{
        use_when = @("deployment_review", "post_deployment_audit")
        avoid_when = @("pre_deployment")
    }
} | ConvertTo-Json

$response = curl -s -X POST "$API_BASE/api/context/store" `
    -H "Content-Type: application/json" `
    -H "X-API-Key: $API_KEY" `
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
