# 🚀 SpiralSafe Production Deployment Guide

**Target**: Get SpiralSafe running in production for ANYONE, ANYWHERE
**Time**: 15 minutes from zero to hero
**Skill Level**: Anyone with basic terminal knowledge

---

## 🎯 What You're Deploying

```
┌─────────────────────────────────────────────────────────┐
│                  SpiralSafe Ecosystem                    │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌──────▼───────┐  ┌────────▼────────┐
│  Public Site   │  │   Core API   │  │ Quantum Plugin  │
│spiralsafe.org  │  │  api.***.org │  │  SpiralCraft    │
└────────────────┘  └──────────────┘  └─────────────────┘
```

**What This Gives You**:
- ✅ Public landing page showcasing H&&S:WAVE protocol
- ✅ Production API with authentication & rate limiting
- ✅ Admin console with ATOM-AUTH login
- ✅ Quantum Minecraft plugin (optional)
- ✅ Full monitoring & alerting setup

---

## 📋 Prerequisites

### Required
- **Cloudflare Account** (free tier works!)
- **GitHub Account**
- **Terminal** (bash, zsh, PowerShell, whatever)
- **Node.js 18+** (for wrangler CLI)

### Optional
- **Minecraft Java Edition 1.20+** (for SpiralCraft plugin)
- **Custom Domain** (can use workers.dev subdomain for free)

---

## 🏁 Quick Start (15 Minutes)

### Step 1: Clone the Repository (2 min)

```bash
# Clone SpiralSafe
git clone https://github.com/spiralsafe/spiralsafe.git
cd spiralsafe

# Install dependencies
cd ops
npm install
```

### Step 2: Set Up Cloudflare (5 min)

```bash
# Login to Cloudflare
npx wrangler login

# Create D1 database
npx wrangler d1 create spiralsafe-ops

# Create KV namespace
npx wrangler kv:namespace create SPIRALSAFE_KV

# Create R2 bucket
npx wrangler r2 bucket create spiralsafe-contexts
```

**Copy the IDs from output and update `ops/wrangler.toml`**:
```toml
[[d1_databases]]
database_id = "YOUR_D1_ID_HERE"

[[kv_namespaces]]
id = "YOUR_KV_ID_HERE"

[[r2_buckets]]
bucket_name = "spiralsafe-contexts"
```

### Step 3: Initialize Database (2 min)

```bash
# Run database migrations
npx wrangler d1 execute spiralsafe-ops --file=schemas/init.sql
```

### Step 4: Set Secrets (3 min)

```bash
# Generate secure API key
API_KEY=$(openssl rand -hex 32)
echo "Your API Key: $API_KEY"
echo "SAVE THIS SOMEWHERE SAFE!"

# Set in Cloudflare
npx wrangler secret put SPIRALSAFE_API_KEY
# Paste the API key when prompted

# (Optional) Set custom rate limits
npx wrangler secret put RATE_LIMIT_REQUESTS
# Enter: 200  (or leave default 100)
```

### Step 5: Deploy to Production (3 min)

```bash
# Build the worker
npm run build

# Deploy to Cloudflare
npx wrangler deploy

# You'll get URLs like:
# https://spiralsafe-api.YOUR-SUBDOMAIN.workers.dev
# Custom domain: api.spiralsafe.org (if configured)
```

### Step 6: Test It! (< 1 min)

```bash
# Test health endpoint
curl https://YOUR-WORKER-URL.workers.dev/api/health

# Should return:
# {
#   "status": "healthy",
#   "checks": { "d1": true, "kv": true, "r2": true },
#   "version": "2.1.0-security"
# }

# Test authenticated endpoint
curl -X POST https://YOUR-WORKER-URL.workers.dev/api/wave/analyze \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content":"From the constraints, gifts. From the spiral, safety."}'

# Should return coherence analysis!
```

---

## 🌐 Deploy Public Website

### Using Cloudflare Pages (Recommended)

```bash
# From repository root
cd public

# Deploy to Cloudflare Pages
npx wrangler pages publish . --project-name=spiralsafe

# Your site is live at:
# https://spiralsafe.pages.dev
# Or custom domain: spiralsafe.org
```

### Using GitHub Pages

```bash
# Enable GitHub Pages in repository settings
# Point to /public folder on main branch

# Your site is live at:
# https://YOUR-USERNAME.github.io/spiralsafe
```

---

## 🔐 Deploy Admin Console (Optional but Recommended)

### Step 1: Create Admin Tables

```bash
npx wrangler d1 execute spiralsafe-ops --file=schemas/admin-schema.sql
```

### Step 2: Generate JWT Secret

```bash
ADMIN_JWT_SECRET=$(openssl rand -hex 32)
npx wrangler secret put ADMIN_JWT_SECRET
# Paste the secret
```

### Step 3: Deploy Admin Worker

```bash
cd ops/admin
npm install
npm run build
npx wrangler deploy --config wrangler-admin.toml

# Your admin console is live at:
# https://console-YOUR-SUBDOMAIN.workers.dev
# Or custom domain: console.spiralsafe.org
```

### Step 4: Create Initial Admin User

```bash
curl -X POST https://YOUR-ADMIN-URL/admin/setup/init \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "your-email@domain.com",
    "password": "CHANGE-THIS-SECURE-PASSWORD"
  }'
```

### Step 5: Login with ATOM-AUTH!

Visit `https://YOUR-ADMIN-URL/admin/login.html` and experience conversational coherence authentication!

---

## 🎮 Deploy SpiralCraft Minecraft Plugin (Optional)

### For Server Admins

```bash
# Download latest release
wget https://github.com/spiralsafe/spiralcraft/releases/latest/download/SpiralCraft.jar

# Copy to your Minecraft server plugins folder
cp SpiralCraft.jar /path/to/your/minecraft/server/plugins/

# Configure API connection
cd /path/to/your/minecraft/server/plugins/SpiralCraft
cat > config.yml <<EOF
api:
  url: https://YOUR-WORKER-URL.workers.dev
  key: YOUR-API-KEY-HERE
EOF

# Restart server
# The plugin will automatically:
# - Create quantum blocks
# - Generate WAVE-based worlds
# - Set up BUMP portals
# - Initialize AWI permission system
```

### For Players

1. Install Litematica mod (client-side)
2. Join a SpiralCraft-enabled server
3. Start with `/quantum tutorial`
4. Begin your quantum journey!

---

## 🔧 Configuration

### Environment Variables

**Required**:
```bash
SPIRALSAFE_API_KEY          # Your main API key
CLOUDFLARE_ACCOUNT_ID       # From dashboard
```

**Optional** (with defaults):
```bash
RATE_LIMIT_REQUESTS=100     # Max requests per IP per window
RATE_LIMIT_WINDOW=60        # Time window in seconds
RATE_LIMIT_AUTH_FAILURES=5  # Max failed auth attempts

# Admin console (if deployed)
ADMIN_JWT_SECRET            # JWT signing secret
ADMIN_JWT_EXPIRATION=86400  # 24 hours
```

### Custom Domain Setup

1. **Add Domain to Cloudflare**:
   - Dashboard → Add Site → Enter domain
   - Update nameservers at registrar

2. **Add Workers Route**:
   - Dashboard → Workers & Pages → spiralsafe-api
   - Settings → Triggers → Add Route
   - Pattern: `api.yourdomain.com/*`
   - Zone: `yourdomain.com`

3. **Test**:
   ```bash
   curl https://api.yourdomain.com/api/health
   ```

---

## 📊 Monitoring Setup

### Enable Email Alerts (5 min)

1. Cloudflare Dashboard → Notifications → Add

2. **Create 3 Alerts**:
   - **Error Rate Alert**: > 5% for 5 minutes
   - **Downtime Alert**: 0 invocations for 5 minutes
   - **High Traffic Alert**: > 1000 req/min (potential DDoS)

3. **Add Recipients**: your-email@domain.com

### Set Up Health Monitoring (5 min)

**UptimeRobot** (free, recommended):
1. Sign up at https://uptimerobot.com
2. Add HTTP(s) monitor
3. URL: `https://api.yourdomain.com/api/health`
4. Keyword: `healthy`
5. Interval: 5 minutes
6. Alert email: your-email@domain.com

### View Logs in Real-Time

```bash
# Monitor all requests
npx wrangler tail spiralsafe-api

# Filter by status
npx wrangler tail spiralsafe-api --status error

# Filter by IP
npx wrangler tail spiralsafe-api --ip-address 203.0.113.45
```

---

## 🚨 Security Checklist

Before going public, verify:

- [ ] API key is cryptographically random (32+ bytes)
- [ ] API key stored in Cloudflare secrets (NOT in code)
- [ ] Rate limiting enabled (default or custom)
- [ ] Email alerts configured
- [ ] Health monitoring active
- [ ] Admin password changed from default
- [ ] JWT secret is unique and secure
- [ ] All endpoints return expected responses
- [ ] CORS headers correctly configured
- [ ] No secrets in git history

---

## 🔄 Updating / Maintenance

### Deploy New Version

```bash
# Pull latest changes
git pull origin main

# Review changes
git log --oneline -5

# Rebuild
cd ops
npm run build

# Deploy
npx wrangler deploy

# Test
curl https://YOUR-URL/api/health
```

### Rotate API Key

```bash
# Generate new key
NEW_KEY=$(openssl rand -hex 32)

# Add to secondary keys (zero-downtime rotation)
npx wrangler secret put SPIRALSAFE_API_KEYS
# Enter: OLD_KEY,NEW_KEY

# Update your clients to use NEW_KEY over 7 days

# After all clients migrated, remove OLD_KEY
npx wrangler secret put SPIRALSAFE_API_KEYS
# Enter: NEW_KEY
```

### Backup Database

```bash
# Export D1 database
npx wrangler d1 export spiralsafe-ops --output=backup-$(date +%Y%m%d).sql

# Store backup safely (Git LFS, S3, etc.)
```

---

## 🌍 One-Click Install for Others

### GitHub Fork + Deploy Button

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloudflare

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          cd ops
          npm ci

      - name: Build worker
        run: |
          cd ops
          npm run build

      - name: Deploy to Cloudflare
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          workingDirectory: 'ops'
```

**For others to deploy**:
1. Fork repository
2. Add `CLOUDFLARE_API_TOKEN` to GitHub Secrets
3. Push to main → Auto-deploys! 🚀

### Replit One-Click (Alternative)

Create `.replit` file:

```toml
run = "cd ops && npm install && npm run build && npx wrangler deploy"

[env]
SPIRALSAFE_API_KEY = "will-be-set-by-user"
```

**Deploy URL**: `https://replit.com/@YOUR-USERNAME/spiralsafe`

Users click "Fork" → Set secrets → Run!

---

## 🎓 Tutorial Mode

### For First-Time Users

```bash
# Interactive setup wizard
npm run setup

# Guided prompts:
# 1. Cloudflare login
# 2. Create resources (D1, KV, R2)
# 3. Generate secrets
# 4. Deploy worker
# 5. Test endpoints
# 6. Setup monitoring

# Everything done automatically!
```

### Example Setup Script

```bash
#!/bin/bash
# setup.sh - One-click SpiralSafe deployment

set -e

echo "🌀 SpiralSafe Setup Wizard"
echo "=========================="
echo ""

# Check prerequisites
command -v node >/dev/null 2>&1 || { echo "❌ Node.js required but not installed. Visit https://nodejs.org"; exit 1; }
command -v npx >/dev/null 2>&1 || { echo "❌ npx required but not installed. Install Node.js"; exit 1; }

echo "✅ Prerequisites check passed"
echo ""

# Step 1: Cloudflare login
echo "Step 1/6: Cloudflare Login"
npx wrangler login

# Step 2: Create resources
echo "Step 2/6: Creating Cloudflare resources..."
D1_ID=$(npx wrangler d1 create spiralsafe-ops --json | jq -r '.database_id')
KV_ID=$(npx wrangler kv:namespace create SPIRALSAFE_KV --json | jq -r '.id')
npx wrangler r2 bucket create spiralsafe-contexts

# Step 3: Update config
echo "Step 3/6: Updating configuration..."
sed -i "s/database_id = \".*\"/database_id = \"$D1_ID\"/" ops/wrangler.toml
sed -i "s/id = \".*\"/id = \"$KV_ID\"/" ops/wrangler.toml

# Step 4: Generate & set secrets
echo "Step 4/6: Generating secrets..."
API_KEY=$(openssl rand -hex 32)
echo "$API_KEY" | npx wrangler secret put SPIRALSAFE_API_KEY

# Step 5: Deploy
echo "Step 5/6: Deploying to production..."
cd ops
npm install
npm run build
npx wrangler deploy
cd ..

# Step 6: Test
echo "Step 6/6: Testing deployment..."
WORKER_URL=$(npx wrangler deployments list --json | jq -r '.[0].url')
HEALTH=$(curl -s "$WORKER_URL/api/health" | jq -r '.status')

if [ "$HEALTH" = "healthy" ]; then
  echo ""
  echo "🎉 SUCCESS! SpiralSafe is live!"
  echo "================================"
  echo ""
  echo "📡 API URL: $WORKER_URL"
  echo "🔑 API Key: $API_KEY"
  echo ""
  echo "Next steps:"
  echo "1. Save your API key somewhere safe"
  echo "2. Test: curl $WORKER_URL/api/health"
  echo "3. Read docs: cat README.md"
  echo "4. Join community: https://discord.gg/spiralsafe"
  echo ""
  echo "H&&S:WAVE | From the constraints, gifts. From the spiral, safety."
else
  echo "❌ Health check failed. Check logs: npx wrangler tail spiralsafe-api"
  exit 1
fi
```

Make it executable:
```bash
chmod +x setup.sh
./setup.sh
```

---

## 📦 Distribution

### GitHub Releases

```bash
# Tag release
git tag -a v2.1.0 -m "Security enhancements + Quantum playground"
git push origin v2.1.0

# Build release artifacts
cd ops && npm run build && cd ..
cd minecraft && mvn package && cd ..

# Create release on GitHub with:
# - spiralsafe-worker-v2.1.0.js
# - SpiralCraft-v1.1.0.jar
# - setup.sh
# - DEPLOYMENT_GUIDE.md
```

### Docker Image (Optional)

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY ops/ ./ops/
COPY public/ ./public/

RUN cd ops && npm ci && npm run build

CMD ["npx", "wrangler", "dev", "--remote"]
```

```bash
docker build -t spiralsafe:latest .
docker run -p 8787:8787 spiralsafe:latest
```

---

## 🌟 Success Metrics

After deployment, you should see:

### Health Dashboard
```
✅ API Status: Healthy
✅ D1 Database: Connected
✅ KV Store: Connected
✅ R2 Storage: Connected
⚡ Avg Response Time: ~118ms
🔒 Auth: Enabled (API key + rate limiting)
📊 Uptime: 100%
```

### Test All Endpoints
```bash
# Run comprehensive test suite
cd ops
./test-api-endpoints.sh

# Expected output:
# ✅ Health Check: 200 OK
# ✅ WAVE Analysis: 200 OK (authenticated)
# ✅ BUMP Marker: 201 Created (authenticated)
# ✅ AWI Grant: 201 Created (authenticated)
# ✅ ATOM Session: 201 Created (authenticated)
# ✅ Context Storage: 201 Created (authenticated)
# ✅ Rate Limiting: 429 after 101 requests
# ✅ Auth Failure Limiting: 429 after 6 failures
```

---

## 🆘 Troubleshooting

### "Cannot read properties of undefined (reading 'prepare')"
**Cause**: D1 binding not configured
**Fix**: Check `wrangler.toml` has correct `database_id`

### "Invalid API key"
**Cause**: Secret not set or wrong key used
**Fix**: `npx wrangler secret put SPIRALSAFE_API_KEY`

### "Rate limit exceeded"
**Cause**: Too many requests from same IP
**Fix**: Wait 60 seconds or adjust rate limits

### "Workers.dev subdomain disabled"
**Cause**: Cloudflare free tier limit
**Fix**: Use custom domain or upgrade plan

### "Build failed"
**Cause**: Dependencies not installed
**Fix**: `cd ops && npm install`

---

## 📚 Resources

- **Documentation**: `/docs` folder
- **API Reference**: `https://api.spiralsafe.org/docs`
- **Discord**: `https://discord.gg/spiralsafe`
- **GitHub Issues**: `https://github.com/spiralsafe/spiralsafe/issues`
- **YouTube Tutorials**: `https://youtube.com/@spiralsafe`

---

## 🎉 You're Live!

Congratulations! You've deployed:
- ✅ Production API with security
- ✅ Public landing page
- ✅ Admin console (optional)
- ✅ Quantum Minecraft plugin (optional)
- ✅ Monitoring & alerts

**Next Steps**:
1. Share your deployment with the world!
2. Join the SpiralSafe community
3. Build something amazing with H&&S:WAVE
4. Contribute back to the project

**Remember**:
> From the constraints, gifts.
> From the spiral, safety.
> From the sauce, hope.

---

**H&&S:WAVE Protocol** | Deployed by the people, for the people, anywhere, anytime.

```
Deployment Version: 2.1.0-security
Status: PRODUCTION READY
Deployment Time: ~15 minutes
Skill Level: Anyone
Global Reach: EVERYWHERE
```

🚀 **Let's spiral together.**
