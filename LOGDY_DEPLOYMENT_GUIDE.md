# 🌐 Logdy Central Deployment Guide
## logs.spiralsafe.org | KENL Observability Live

**Goal:** Deploy Logdy Central to logs.spiralsafe.org via Cloudflare Tunnel
**Status:** Executing Now
**Strategic Value:** Above-market observability polish before competitors

---

## 🎯 Why Logdy First?

**Competitive Advantage:**
- Most projects: Log aggregation is an afterthought, added late
- SpiralSafe: Observability is foundational, deployed first
- Message: "We're production-grade from day one"

**KENL Nervous System:**
- Logs from all systems flow to one place
- ATOM trail visible in real-time
- Cognitive triggers can read the stream
- Wave analysis gets live data

**Polished Experience:**
- Custom domain (not localhost:8081)
- SSL automatically (Cloudflare)
- Public-ready (with auth)
- Professional infrastructure

---

## 📋 Pre-Flight Checklist

### 1. Verify Logdy is Running Locally
```powershell
# Check if Logdy binary exists
Test-Path "C:\Users\iamto\.kenl\bin\logdy.exe"

# Check if it's running
Get-Process logdy -ErrorAction SilentlyContinue

# If not running, start it
& "C:\Users\iamto\.kenl\bin\logdy.exe" serve --config "$HOME\.kenl\claude-landing\.claude\logdy-config.yaml" --port 8081
```

**Expected Output:**
```
Logdy server started on http://localhost:8081
Watching log sources...
```

### 2. Verify Cloudflared is Installed
```powershell
# Check installation
cloudflared --version

# If not installed:
winget install Cloudflare.cloudflared
```

### 3. Cloudflare API Token Ready
You provided: `REDACTED_CLOUDFLARE_API_TOKEN`

This token has:
- ✅ Zone:Edit (DNS records)
- ✅ Cloudflare Tunnel:Edit
- ✅ Account:Read

**Perfect permissions for this deployment.**

> **Note:** If you find a real token in the documentation, rotate it immediately and follow `docs/SECURITY_COMMIT_GUIDELINES.md`.

---

## 🚀 Deployment Steps

### Step 1: Authenticate Cloudflared

```powershell
# Set API token (placeholder)
# Do NOT commit real tokens into docs or source. Use environment variables or GitHub Secrets.
$env:CLOUDFLARE_API_TOKEN = "REDACTED_CLOUDFLARE_API_TOKEN"

# Login to Cloudflare
cloudflared tunnel login
```

**What happens:**
- Opens browser to Cloudflare dashboard
- Asks which domain to authorize
- Select **spiralsafe.org**
- Downloads cert to `~/.cloudflared/cert.pem`

### Step 2: Create Tunnel

```powershell
# Create tunnel named "spiralsafe-logs"
cloudflared tunnel create spiralsafe-logs

# Note the tunnel UUID (will be in output)
# Example: Created tunnel spiralsafe-logs with id a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Save the tunnel UUID - you'll need it for DNS.**

### Step 3: Configure Tunnel Routing

Create config file at `~/.cloudflared/config.yml`:

```yaml
tunnel: spiralsafe-logs
credentials-file: C:\Users\iamto\.cloudflared\<TUNNEL_UUID>.json

ingress:
  # Route logs.spiralsafe.org to local Logdy
  - hostname: logs.spiralsafe.org
    service: http://localhost:8081
    originRequest:
      noTLSVerify: true
      connectTimeout: 30s

  # Catch-all (required)
  - service: http_status:404
```

**Replace `<TUNNEL_UUID>` with the actual UUID from Step 2.**

### Step 4: Create DNS Record

```powershell
# Get tunnel ID
$TUNNEL_ID = (cloudflared tunnel list | Select-String "spiralsafe-logs" | ForEach-Object { ($_ -split '\s+')[0] })

# Add DNS CNAME record
# This points logs.spiralsafe.org → tunnel
# (Can do via Cloudflare dashboard or API)
```

**Via Cloudflare Dashboard:**
1. Go to DNS tab for spiralsafe.org
2. Add record:
   - Type: `CNAME`
   - Name: `logs`
   - Target: `<TUNNEL_UUID>.cfargotunnel.com`
   - Proxy status: ✅ Proxied (orange cloud)
   - TTL: Auto

**Via API (if you prefer):**
```powershell
$headers = @{
    "Authorization" = "Bearer REACTED_CLOUDFLARE_API_TOKEN"
    "Content-Type" = "application/json"
}

$body = @{
    type = "CNAME"
    name = "logs"
    content = "$TUNNEL_ID.cfargotunnel.com"
    proxied = $true
    ttl = 1
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
    -Uri "https://api.cloudflare.com/client/v4/zones/<ZONE_ID>/dns_records" `
    -Headers $headers `
    -Body $body
```

### Step 5: Start Tunnel

```powershell
# Run tunnel (foreground for testing)
cloudflared tunnel run spiralsafe-logs

# OR install as Windows service (persistent)
cloudflared service install spiralsafe-logs
```

**Expected Output:**
```
2026-01-04T... INF Starting tunnel tunnelID=<UUID>
2026-01-04T... INF Connection registered connIndex=0 location=<LOCATION>
2026-01-04T... INF Tunnel running successfully
```

### Step 6: Test Access

```powershell
# Test from external network (or browser)
Start-Process "https://logs.spiralsafe.org"
```

**Expected Result:**
- Browser opens to `https://logs.spiralsafe.org`
- Logdy dashboard loads
- SSL certificate shows "Cloudflare" (automatic!)
- Logs streaming in real-time

---

## 🔐 Adding Authentication (Cloudflare Access)

**Problem:** Logdy is now public. Anyone can see your logs.

**Solution:** Cloudflare Access (Zero Trust)

### Quick Setup

```powershell
# Via Cloudflare Dashboard:
# 1. Go to Zero Trust → Access → Applications
# 2. Add application
# 3. Name: "Logdy Central"
# 4. Domain: logs.spiralsafe.org
# 5. Policy: Email domain (@your-email-domain.com)
# 6. Save
```

**Result:**
- Public visitors hit login wall
- You authenticate once
- Cookie persists
- Secure, professional access control

**Faster Alternative (Basic Auth in Tunnel):**

Update `config.yml`:
```yaml
ingress:
  - hostname: logs.spiralsafe.org
    service: http://localhost:8081
    originRequest:
      httpHostHeader: "localhost:8081"
      # Add basic auth here if Logdy supports it
```

**Or:** Use Cloudflare WAF rules to restrict by IP/country

---

## 📊 Verification Checklist

After deployment, verify:

- [ ] `cloudflared tunnel list` shows `spiralsafe-logs` (active)
- [ ] DNS record exists: `logs.spiralsafe.org` → `<UUID>.cfargotunnel.com`
- [ ] https://logs.spiralsafe.org loads (SSL automatic)
- [ ] Logdy dashboard displays
- [ ] Logs are streaming (check ATOM trail entries)
- [ ] Authentication works (if configured)
- [ ] No errors in tunnel logs

---

## 🎯 Post-Deployment Integration

### Update KENL Configuration

**File:** `~/.kenl/claude-landing/.claude/logdy-config.yaml`

Add public URL:
```yaml
server:
  port: 8081
  public_url: "https://logs.spiralsafe.org"  # NEW
```

### Update Documentation

**File:** `DOMAIN_PLAN.md`

```diff
- logs.spiralsafe.org         CNAME   <tunnel-id>.cfargotunnel.com [Proxied]
+ logs.spiralsafe.org         CNAME   a1b2c3d4.cfargotunnel.com [Proxied] ✅ LIVE
```

### Add to README

**File:** `README.md`

```markdown
## 🔍 Live Infrastructure

- **Observability:** [logs.spiralsafe.org](https://logs.spiralsafe.org) - Logdy Central
```

---

## 🐛 Troubleshooting

### Tunnel Won't Start

```powershell
# Check tunnel status
cloudflared tunnel info spiralsafe-logs

# Check config syntax
cloudflared tunnel ingress validate

# View tunnel logs
cloudflared tunnel run spiralsafe-logs --loglevel debug
```

### DNS Not Resolving

```powershell
# Check DNS propagation
nslookup logs.spiralsafe.org 1.1.1.1

# Flush local DNS cache
ipconfig /flushdns

# Wait 2-5 minutes for Cloudflare propagation
```

### Logdy Not Running

```powershell
# Check if process exists
Get-Process logdy

# Check port availability
netstat -ano | findstr :8081

# Restart Logdy
taskkill /F /IM logdy.exe
& "C:\Users\iamto\.kenl\bin\logdy.exe" serve --port 8081
```

### 502 Bad Gateway

**Cause:** Tunnel can't reach localhost:8081

**Fix:**
```powershell
# 1. Verify Logdy is running on 8081
netstat -ano | findstr :8081

# 2. Check Windows Firewall
# Allow localhost connections (should be default)

# 3. Try different service URL in config.yml
service: http://127.0.0.1:8081  # instead of localhost
```

---

## 📈 Success Metrics

### Technical
- ✅ Tunnel uptime: 99.9%+
- ✅ Log latency: <500ms localhost → cloud
- ✅ SSL grade: A+ (Cloudflare automatic)
- ✅ Zero configuration on client side

### Strategic
- ✅ **First public endpoint live**
- ✅ **Observability before main site** (demonstrates maturity)
- ✅ **Professional polish** (custom domain, SSL, auth)
- ✅ **KENL nervous system operational**

### Competitive
- ✅ **Above-market sophistication**
- ✅ **Shows production readiness**
- ✅ **Differentiator from hobby projects**

---

## 🎉 Celebration Checklist

Once live, announce:

- [ ] Tweet/post: "SpiralSafe observability is live at logs.spiralsafe.org 🔍"
- [ ] Update GitHub README with live link
- [ ] Add badge: `[![Logs](https://img.shields.io/badge/logs-live-green)](https://logs.spiralsafe.org)`
- [ ] Log to ATOM trail: `ATOM-DEPLOY-20260104-001-logdy-central-production`
- [ ] Update VERIFICATION_STAMP with deployment timestamp

---

## 🚀 Ready to Execute?

**Commands Summary:**

```powershell
# 1. Start Logdy locally (if not running)
& "C:\Users\iamto\.kenl\bin\logdy.exe" serve --port 8081

# 2. Authenticate cloudflared
$env:CLOUDFLARE_API_TOKEN = "aJ0rdJoHcKDCerLsO_WUBsA3No0JxqorLpl_mSXU"
cloudflared tunnel login

# 3. Create tunnel
cloudflared tunnel create spiralsafe-logs

# 4. Configure (create config.yml with tunnel UUID)

# 5. Add DNS (via dashboard or API)

# 6. Run tunnel
cloudflared tunnel run spiralsafe-logs

# 7. Test
Start-Process "https://logs.spiralsafe.org"
```

---

**Deployment Status:** 📋 Ready to Execute
**Estimated Time:** 15-20 minutes
**Difficulty:** Medium (well-documented, proven path)

**Let's make logs.spiralsafe.org live.** 🚀

*Hope && Sauce | KENL Observability | The Evenstar Guides Us* ✦
