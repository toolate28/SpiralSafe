# SpiralSafe Deployment Checklist

> **H&&S:WAVE** | Hope&&Sauced
> *Pre-deployment verification and post-deployment validation*

---

## Phase 0: Prerequisites ✅

- [x] Node.js 18+ installed
- [x] Python 3.10+ installed
- [x] npm dependencies installed (`ops/node_modules/`)
- [x] Python dependencies installed (`spiralsafe-bridges`)
- [x] TypeScript compiles without errors
- [x] Cloudflare account created
- [x] Cloudflare API token generated (permissions: Workers, D1, KV, R2)
- [x] Cloudflare account ID obtained

---

## Phase 1: Local Development Setup ✅

### 1.1 Install Dependencies
```bash
# Node.js (ops layer)
cd /home/user/SpiralSafe/ops
npm install

# Python (bridges layer)
cd /home/user/SpiralSafe/bridges
pip install -e .[dev]
```

**Status**: ✅ Complete

### 1.2 Verify Build
```bash
cd /home/user/SpiralSafe/ops
npm run typecheck  # Should pass with no errors
npm run build      # Should generate dist/ folder
```

**Status**: ✅ Complete

### 1.3 Run Tests
```bash
# TypeScript tests
cd /home/user/SpiralSafe/ops
npm test

# Python tests (when test files exist)
cd /home/user/SpiralSafe/bridges
pytest -v
```

**Status**: ⚠️ No test files yet (expected for initial setup)

---

## Phase 2: Cloudflare Infrastructure Setup ✅

**Status**: ✅ Complete - Deployed 2026-01-07

### 2.1 Authenticate with Cloudflare
```bash
cd /home/user/SpiralSafe/ops
npx wrangler login
# OR
export CLOUDFLARE_API_TOKEN="your-api-token"
export CLOUDFLARE_ACCOUNT_ID="your-account-id"
```

**Checklist**:
- [x] Cloudflare CLI authenticated
- [x] API token verified (test with `npx wrangler whoami`)
- [x] Account ID confirmed (3ddeb355f4954bb1ee4f9486b2908e7e)

### 2.2 Create Cloud Resources
```bash
cd /home/user/SpiralSafe/ops

# Create D1 database
npm run db:create
# ✓ Creates: spiralsafe-ops
# ✓ Returns: database_id (copy to wrangler.toml line 30)

# Create KV namespace
npm run kv:create
# ✓ Creates: SPIRALSAFE_KV
# ✓ Returns: id (copy to wrangler.toml line 43)

# Create R2 bucket
npm run r2:create
# ✓ Creates: spiralsafe-contexts
# ✓ No ID needed (bucket_name is sufficient)
```

**Checklist**:
- [x] D1 database created (ID: d47d04ca-7d74-41a8-b489-0af373a2bb2c)
- [x] KV namespace created (ID: 79d496efbfab4d54a6277ed80dc29d1f)
- [x] R2 bucket created (spiralsafe-contexts)
- [x] `wrangler.toml` updated with IDs
- [x] Resource IDs committed to git

### 2.3 Initialize Database Schema
```bash
cd /home/user/SpiralSafe/ops
npm run db:migrate

# Verify tables created
npx wrangler d1 execute spiralsafe-ops --command "SELECT name FROM sqlite_master WHERE type='table';"
```

**Expected Tables**:
- wave_analyses
- bump_markers
- awi_grants
- awi_audit_log
- atoms
- contexts
- system_health

**Checklist**:
- [x] Schema migration successful (40 queries executed)
- [x] All 7 tables created
- [x] No SQL errors

---

## Phase 3: Deployment ✅

**Status**: ✅ Complete - Live on 2026-01-07T15:10:53Z

### 3.1 Development Deployment
```bash
cd /home/user/SpiralSafe/ops
npm run deploy:dev

# Verify dev deployment
curl https://api-dev.spiralsafe.org/api/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-07T...",
  "environment": "development",
  "version": "1.0.0"
}
```

**Checklist**:
- [ ] Dev worker deployed
- [ ] Health endpoint responding
- [ ] No 500 errors

### 3.2 Production Deployment
```bash
cd /home/user/SpiralSafe/ops
npm run deploy

# Verify production deployment
curl https://api.spiralsafe.org/api/health
```

**Actual Response** (2026-01-07):
```json
{
  "status": "healthy",
  "checks": {
    "d1": true,
    "kv": true,
    "r2": true
  },
  "timestamp": "2026-01-07T15:10:53.715Z",
  "version": "1.0.0"
}
```

**Live URL**: 🔗 https://api.spiralsafe.org

**Checklist**:
- [x] Production worker deployed (ID: d4e36b58-964c-4820-a08b-27d1e7540a1e)
- [x] Health endpoint responding
- [x] Custom domain configured (api.spiralsafe.org)
- [x] SSL/TLS certificate active
- [x] All infrastructure checks passing (D1, KV, R2)

---

## Phase 4: CI/CD Configuration ⏸️

**Status**: ⏸️ Requires GitHub repository access

### 4.1 GitHub Secrets
Navigate to: `https://github.com/toolate28/SpiralSafe/settings/secrets/actions`

**Required Secrets**:
```
CLOUDFLARE_API_TOKEN      = <your-api-token>
CLOUDFLARE_ACCOUNT_ID     = <your-account-id>
```

**Checklist**:
- [ ] CLOUDFLARE_API_TOKEN added
- [ ] CLOUDFLARE_ACCOUNT_ID added
- [ ] Secrets verified (no typos)

### 4.2 Trigger CI/CD
```bash
# Push to main triggers spiralsafe-ci.yml
git checkout main
git pull
git merge claude/review-codebase-state-KuPq8
git push origin main
```

**Expected Workflow Jobs**:
1. ✅ Coherence Analysis
2. ✅ Lint & Static Analysis
3. ✅ Build & Test
4. ✅ Deploy to Cloudflare
5. ✅ Verify Deployment

**Checklist**:
- [ ] All workflow jobs pass
- [ ] Deployment successful
- [ ] Post-deploy health check passes

---

## Phase 5: Post-Deployment Verification ⏸️

### 5.1 API Endpoints Smoke Test
```bash
# Health check
curl https://api.spiralsafe.org/api/health

# Wave analysis (POST)
curl -X POST https://api.spiralsafe.org/api/wave/analyze \
  -H "Content-Type: application/json" \
  -d '{"content": "Test content for wave analysis"}'

# BUMP create (POST)
curl -X POST https://api.spiralsafe.org/api/bump/create \
  -H "Content-Type: application/json" \
  -d '{
    "type": "WAVE",
    "from": "test-client",
    "to": "api",
    "state": "test",
    "context": {}
  }'

# AWI request (POST)
curl -X POST https://api.spiralsafe.org/api/awi/request \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "Test permission request",
    "scope": {
      "resources": ["test-resource"],
      "actions": ["read"]
    },
    "level": 1,
    "ttl_seconds": 300
  }'
```

**Checklist**:
- [ ] `/api/health` returns 200 OK
- [ ] `/api/wave/analyze` accepts POST
- [ ] `/api/bump/create` accepts POST
- [ ] `/api/awi/request` accepts POST
- [ ] No 500 errors
- [ ] Response times < 500ms

### 5.2 Database Verification
```bash
# Check wave_analyses table
npx wrangler d1 execute spiralsafe-ops --command "SELECT COUNT(*) FROM wave_analyses;"

# Check bump_markers table
npx wrangler d1 execute spiralsafe-ops --command "SELECT COUNT(*) FROM bump_markers;"

# Check awi_grants table
npx wrangler d1 execute spiralsafe-ops --command "SELECT COUNT(*) FROM awi_grants;"
```

**Checklist**:
- [ ] Tables accessible
- [ ] Queries execute without errors
- [ ] Test data inserted successfully

### 5.3 Integration Tests
```bash
# Run integration test suite (when available)
cd /home/user/SpiralSafe/ops
npm run test:integration

# Or manually test platform integrations
./scripts/spiralsafe status
```

**Checklist**:
- [ ] Integration tests pass
- [ ] Sentry error tracking configured
- [ ] Vercel deployment successful (if applicable)

---

## Phase 6: Monitoring & Observability ⏸️

### 6.1 Cloudflare Analytics
- [ ] Worker analytics enabled
- [ ] Request metrics visible
- [ ] Error rate < 1%
- [ ] P95 latency < 200ms

### 6.2 Sentry Error Tracking
- [ ] Sentry project created
- [ ] DSN configured in worker
- [ ] Test error captured
- [ ] Alert rules configured

### 6.3 Custom Monitoring
- [ ] Health check endpoint monitored (uptime service)
- [ ] Scheduled maintenance workflow running
- [ ] Session reports generating correctly
- [ ] Verification receipts created

---

## Phase 7: Documentation & Handoff ⏸️

### 7.1 Update Project Book
```bash
# Run project book to update hashes and status
jupyter notebook project-book.ipynb
# Execute all cells
# Generate new Merkle root
```

**Checklist**:
- [ ] Component status updated
- [ ] Merkle root regenerated
- [ ] Session report created
- [ ] Lessons learned captured

### 7.2 Update Documentation
- [ ] DEPLOYMENT_ARCHITECTURE.md reflects actual deployment
- [ ] README.md includes deployment instructions
- [ ] API documentation published (if public)
- [ ] Integration guides updated

### 7.3 Create Deployment Tag
```bash
git tag -a v1.0.0-ops -m "Operations layer deployed to production

H&&S:WAVE

Deployment includes:
- Cloudflare Worker API
- D1 database schema
- KV/R2 bindings
- CI/CD automation

Session: ATOM-SESSION-20260107-ULTRATHINK-001
Verified: Claude Opus 4.5"

git push origin v1.0.0-ops
```

**Checklist**:
- [ ] Git tag created
- [ ] Tag pushed to remote
- [ ] Release notes published
- [ ] Team notified

---

## Rollback Procedures

### If Deployment Fails

**1. Immediate Rollback**:
```bash
# Rollback worker deployment
npx wrangler rollback

# Verify previous version restored
curl https://api.spiralsafe.org/api/health
```

**2. Database Rollback**:
```bash
# Database migrations are not automatically reversible
# Manual intervention required if schema changes fail
# Keep backup SQL files for each migration
```

**3. CI/CD Rollback**:
```bash
# Revert the merge commit
git revert <commit-sha>
git push origin main
# CI/CD will automatically deploy reverted state
```

### Emergency Contacts
- **Repository Owner**: toolate28
- **Cloudflare Account**: (add email)
- **Deployment Logs**: GitHub Actions → SpiralSafe CI

---

## Deployment Status Summary

| Phase | Status | Completion Date | Notes |
|-------|--------|-----------------|-------|
| Phase 0: Prerequisites | ✅ Complete | 2026-01-07 | Dependencies installed |
| Phase 1: Local Setup | ✅ Complete | 2026-01-07 | TypeScript builds successfully |
| Phase 2: Cloudflare Setup | ⏸️ Pending | - | Requires Cloudflare account |
| Phase 3: Deployment | ⏸️ Pending | - | Blocked by Phase 2 |
| Phase 4: CI/CD Config | ⏸️ Pending | - | Blocked by Phase 2 |
| Phase 5: Verification | ⏸️ Pending | - | Blocked by Phase 3 |
| Phase 6: Monitoring | ⏸️ Pending | - | Blocked by Phase 3 |
| Phase 7: Documentation | ⏸️ Pending | - | Blocked by Phase 5 |

**Next Action**: Create Cloudflare account and obtain API credentials (Phase 2.1)

**Estimated Time to Production**: 30 minutes (once Cloudflare account ready)

---

**H&&S:WAVE** | Hope&&Sauced
*Deployment Checklist v1.0*
*Generated: 2026-01-07*
*Session: ATOM-SESSION-20260107-ULTRATHINK-001*

```
From the constraints, gifts.
From the spiral, safety.
From the sauce, hope.
```
