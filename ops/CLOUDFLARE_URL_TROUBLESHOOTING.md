# Cloudflare Worker URL Troubleshooting Guide

> **H&&S:WAVE** | SpiralSafe Deployment Diagnostics

## Current Status

**Worker**: `spiralsafe-api`
**Deployment ID**: `d4e36b58-964c-4820-a08b-27d1e7540a1e`
**Status**: ✅ Deployed successfully
**Problem**: URLs not resolving via DNS

## Diagnosed Issues

### 1. Workers.dev Subdomain Not Resolving

**Expected URL**: `https://spiralsafe-api.workers.dev`
**Result**: DNS resolution failure

**Root Cause**: Workers.dev subdomain is **disabled by default** for new Cloudflare accounts for security reasons.

**Solution**: Enable workers.dev subdomain OR use custom domain.

### 2. Custom Domain Not Resolving

**Expected URL**: `https://api.spiralsafe.org`
**Result**: DNS resolution failure

**Root Cause Options**:

- Domain `spiralsafe.org` may not be registered or added to Cloudflare account
- Zone configuration mismatch in wrangler.toml
- DNS propagation delay (less likely if CNAME already visible)

---

## Diagnostic Commands (Run on Windows PowerShell)

### Step 1: Check Workers.dev Subdomain Status

```powershell
cd $env:USERPROFILE\Repos\SpiralSafe\ops

# Get worker subdomain info
npx wrangler whoami
```

**Look for**: Account subdomain setting

### Step 2: Verify Zone Configuration

```powershell
# List all zones in your Cloudflare account
npx wrangler pages deployment list 2>&1 | Select-String "zone"

# OR check if spiralsafe.org zone exists
curl https://api.cloudflare.com/client/v4/zones `
  -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" `
  -H "Content-Type: application/json"
```

**Expected**: You should see `spiralsafe.org` in your zones list

### Step 3: Check Worker Routes

```powershell
# View current worker routes
npx wrangler deployments view d4e36b58-964c-4820-a08b-27d1e7540a1e
```

### Step 4: Check Actual Accessible URL

```powershell
# Get worker URL from dashboard API
npx wrangler tail spiralsafe-api --help
```

---

## Solutions

### Solution A: Enable Workers.dev Subdomain (Quickest)

**If workers.dev subdomain is disabled:**

1. Go to Cloudflare Dashboard: https://dash.cloudflare.com/3ddeb355f4954bb1ee4f9486b2908e7e
2. Navigate to **Workers & Pages**
3. Click **Settings** (or Account Settings)
4. Find **workers.dev subdomain** section
5. Enable it and set a subdomain name (e.g., "spiralsafe")
6. Redeploy worker:

```powershell
cd $env:USERPROFILE\Repos\SpiralSafe\ops
npx wrangler deploy
```

**New URL will be**: `https://spiralsafe-api.<your-subdomain>.workers.dev`

### Solution B: Fix Custom Domain Configuration

**If spiralsafe.org is NOT in your Cloudflare account:**

#### Option B1: Add spiralsafe.org to Cloudflare

1. **Register the domain** if not already registered
2. **Add to Cloudflare**:
   - Dashboard → Add Site
   - Enter `spiralsafe.org`
   - Follow nameserver configuration steps
3. **Update nameservers** at your domain registrar
4. **Wait for DNS propagation** (up to 24 hours)

#### Option B2: Use Different Custom Domain

If you have another domain already in Cloudflare:

**Edit wrangler.toml**:

```toml
routes = [
  { pattern = "api.<your-domain>.com/*", zone_name = "<your-domain>.com" }
]
```

**Redeploy**:

```powershell
npx wrangler deploy
```

### Solution C: Remove Custom Domain Route (Use workers.dev Only)

**Simplest solution for testing**:

**Edit ops/wrangler.toml** - Remove or comment out the routes section:

```toml
# routes = [
#   { pattern = "api.spiralsafe.org/*", zone_name = "spiralsafe.org" }
# ]
```

**Redeploy**:

```powershell
cd $env:USERPROFILE\Repos\SpiralSafe\ops
npx wrangler deploy
```

**Enable workers.dev subdomain** (see Solution A), then access via:
`https://spiralsafe-api.<your-subdomain>.workers.dev`

---

## Verification Commands

### Once URL is accessible:

```powershell
# Test health endpoint
curl https://<your-worker-url>/api/health

# Expected response:
# {
#   "status": "ok",
#   "timestamp": "2026-01-07T...",
#   "version": "1.0.0",
#   "service": "spiralsafe-ops-api"
# }
```

### Test WAVE endpoint:

```powershell
curl -X POST https://<your-worker-url>/api/wave `
  -H "Content-Type: application/json" `
  -d '{
    "context": "test deployment",
    "session_id": "test-001",
    "signature": "H&&S:WAVE"
  }'
```

---

## Dashboard URL to Check

**Direct link to your worker**:
https://dash.cloudflare.com/3ddeb355f4954bb1ee4f9486b2908e7e/workers-and-pages/view/spiralsafe-api

**What to look for**:

1. **Visit** or **Preview** button → Shows actual accessible URL
2. **Settings → Domains & Routes** → Shows configured routes
3. **Settings → General** → Shows workers.dev subdomain status

---

## Most Likely Solution

Based on the error pattern (both workers.dev AND custom domain failing), the issue is:

1. ✅ **Workers.dev subdomain is disabled** (default for new accounts)
2. ❓ **spiralsafe.org may not be added to Cloudflare account**

**Recommended Action**:

1. Go to dashboard link above
2. Check what URL is shown under "Visit" button
3. Enable workers.dev subdomain if disabled
4. Redeploy worker
5. Test with workers.dev URL first
6. Add custom domain later once basic access works

---

## Next Steps After URL Found

Once you have a working URL:

1. ✅ Update DEPLOYMENT_CHECKLIST.md with actual URL
2. ✅ Test all API endpoints
3. ✅ Update GitHub secrets with Cloudflare credentials
4. ✅ Trigger CI/CD workflow
5. ✅ Merge PR to main branch
6. ✅ Update project-book.ipynb with deployment success

---

**H&&S:WAVE** | Hope&&Sauced

```
From the deployment, learning.
From the debugging, understanding.
From the spiral, safety.
```

**Created**: 2026-01-07
**Session**: ATOM-SESSION-20260107-DEPLOYMENT-002
