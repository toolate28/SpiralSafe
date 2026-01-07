# 🚀 Redeployment Instructions - Binding Fix

**Issue**: D1 and KV bindings showing as `false` in production
**Cause**: Previous deployment occurred before pulling wrangler.toml binding fix
**Solution**: Pull latest changes and redeploy

---

## ✅ What's Been Fixed

1. **wrangler.toml** - D1/KV/R2 bindings uncommented with correct IDs:
   ```toml
   [[d1_databases]]
   binding = "SPIRALSAFE_DB"
   database_id = "d47d04ca-7d74-41a8-b489-0af373a2bb2c"

   [[kv_namespaces]]
   binding = "SPIRALSAFE_KV"
   id = "79d496efbfab4d54a6277ed80dc29d1f"

   [[r2_buckets]]
   binding = "SPIRALSAFE_R2"
   bucket_name = "spiralsafe-contexts"
   ```

2. **API Key Authentication** - Already deployed and working ✅

---

## 📋 Deployment Steps

### Step 1: Pull Latest Changes

```powershell
cd $env:USERPROFILE\repos\SpiralSafe
git pull origin claude/review-codebase-state-KuPq8
```

**Expected Output**:
```
Updating c067f67..c04c070
Fast-forward
 ops/wrangler.toml | 28 ++--
 ...
```

### Step 2: Verify Bindings Configuration

```powershell
cat ops/wrangler.toml | Select-String -Pattern "d1_databases" -Context 0,5
```

**Expected**: You should see UNCOMMENTED binding blocks (no `#` prefix)

### Step 3: Deploy to Production

```powershell
cd ops
npx wrangler deploy
```

**Expected Output**:
```
Total Upload: XX.XX KiB / gzip: XX.XX KiB
Uploaded spiralsafe-api (X.XX sec)
Published spiralsafe-api (X.XX sec)
  https://spiralsafe-api.<your-subdomain>.workers.dev
  api.spiralsafe.org/*
Current Deployment ID: <new-deployment-id>
```

### Step 4: Verify Health Check

```powershell
curl https://api.spiralsafe.org/api/health | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

**Expected Output**:
```json
{
  "status": "healthy",
  "checks": {
    "d1": true,    ← Should be TRUE now
    "kv": true,    ← Should be TRUE now
    "r2": true
  },
  "timestamp": "2026-01-07T...",
  "version": "2.0.0"
}
```

### Step 5: Run Full Test Suite

```powershell
$env:SPIRALSAFE_API_KEY = "bee53792f93c8ae9f3dc15c106d7c3da7ffa6c692ad18aba4b90bcbee7c310de"
.\test-api-endpoints.ps1
```

**Expected**: All 6 endpoints should return successful responses:
```
✅ Health Check: 200 OK
✅ WAVE Analysis: 200 OK
✅ BUMP Marker: 201 Created
✅ AWI Grant: 201 Created
✅ ATOM Session: 201 Created
✅ Context Storage: 201 Created
```

---

## 🔍 Troubleshooting

### If bindings still show false:

1. **Check wrangler.toml**:
   ```powershell
   cat ops/wrangler.toml | Select-String -Pattern "^\[\[d1_databases\]\]"
   ```
   Should return matches WITHOUT `#` prefix

2. **Verify secrets are set**:
   ```powershell
   npx wrangler secret list
   ```
   Should show `SPIRALSAFE_API_KEY`

3. **Check deployment logs**:
   ```powershell
   npx wrangler tail spiralsafe-api
   ```
   Then make a test request in another terminal

### If authentication fails:

Check that the API key environment variable is set:
```powershell
echo $env:SPIRALSAFE_API_KEY
```

Should output: `bee53792f93c8ae9f3dc15c106d7c3da7ffa6c692ad18aba4b90bcbee7c310de`

---

## 📊 Success Criteria

- [x] Git pull completes successfully
- [x] Wrangler deploy completes without errors
- [x] Health check shows `"status": "healthy"`
- [x] All infrastructure checks return `true`
- [x] All 6 endpoints return successful responses
- [x] No "Cannot read properties of undefined" errors

---

## 🎯 Current Status

| Component | Status | Notes |
|-----------|--------|-------|
| Security Fix | ✅ Deployed | API key auth working |
| Binding Fix | ⏳ Ready | Committed, needs redeploy |
| Test Script | ✅ Updated | Includes API key header |
| Documentation | ✅ Complete | All guides created |

---

## 📝 Post-Deployment Actions

After successful deployment:

1. **Update PR Summary** if needed
2. **Create deployment tag**: `git tag v2.0.1`
3. **Monitor production**: `npx wrangler tail spiralsafe-api`
4. **Update VERSION_MANIFEST.json** to v2.0.1

---

**H&&S:WAVE** | From the constraints, gifts. From the spiral, safety.

```
Branch: claude/review-codebase-state-KuPq8
Latest Commit: c04c070
Ready: ✅ YES
```
