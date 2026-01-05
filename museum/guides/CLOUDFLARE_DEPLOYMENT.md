# SpiralSafe.org Cloudflare Deployment Guide

## Domain: spiralsafe.org

**Status:** DNS managed via Cloudflare
**Deployment Target:** Cloudflare Pages
**Repository:** https://github.com/toolate28/SpiralSafe

---

## Deployment Architecture

```
GitHub Repository (toolate28/SpiralSafe)
         │
         ▼
    Cloudflare Pages
    (auto-deploy on push)
         │
         ▼
    spiralsafe.org
    (Cloudflare DNS + CDN)
```

---

## Step 1: Cloudflare Pages Setup

### 1.1 Create Pages Project

```bash
# Using Wrangler CLI
npx wrangler pages project create spiralsafe \
  --production-branch=main \
  --build-command="echo 'Static site - no build needed'" \
  --build-output-directory="."
```

**Or via Cloudflare Dashboard:**
1. Go to Pages → Create a project
2. Connect GitHub account
3. Select repository: `toolate28/SpiralSafe`
4. Configure build settings:
   - **Framework preset:** None
   - **Build command:** (leave empty for static site)
   - **Build output directory:** `/`
   - **Root directory:** `/` or `/website` if website files are in a subdirectory

### 1.2 Environment Variables (Optional)

If the site needs any environment variables:
```bash
npx wrangler pages secret put ATOM_API_KEY
# Enter value when prompted
```

---

## Step 2: DNS Configuration

### 2.1 Add DNS Records

In Cloudflare DNS dashboard for `spiralsafe.org`:

| Type | Name | Target | Proxy | TTL |
|------|------|--------|-------|-----|
| CNAME | @ | spiralsafe.pages.dev | ✅ Proxied | Auto |
| CNAME | www | spiralsafe.pages.dev | ✅ Proxied | Auto |

**Or via Wrangler:**
```bash
# Add apex domain
npx wrangler pages domain add spiralsafe.org

# Add www subdomain
npx wrangler pages domain add www.spiralsafe.org
```

### 2.2 Verify DNS Propagation

```bash
# Check DNS resolution
dig spiralsafe.org
dig www.spiralsafe.org

# Or use online tool
curl https://dns.google/resolve?name=spiralsafe.org&type=A
```

---

## Step 3: SSL/TLS Configuration

### 3.1 Enable Universal SSL

Cloudflare should automatically provision SSL certificates. Verify:
1. Go to SSL/TLS tab in Cloudflare dashboard
2. Ensure **Full (strict)** mode is enabled
3. Verify certificate status: ✅ Active

### 3.2 Force HTTPS

Create Page Rule for HTTP → HTTPS redirect:
```
If URL matches: http://*spiralsafe.org/*
Then: Always Use HTTPS
```

**Or via API:**
```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/pagerules" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  --data '{
    "targets": [{"target": "url", "constraint": {"operator": "matches", "value": "http://*spiralsafe.org/*"}}],
    "actions": [{"id": "always_use_https"}],
    "priority": 1,
    "status": "active"
  }'
```

---

## Step 4: Performance Optimization

### 4.1 Enable Rocket Loader

```
Speed → Optimization → Rocket Loader: ON
```

### 4.2 Enable Auto Minify

```
Speed → Optimization → Auto Minify:
  - ✅ JavaScript
  - ✅ CSS
  - ✅ HTML
```

### 4.3 Enable Brotli Compression

```
Speed → Optimization → Brotli: ON
```

---

## Step 5: Security Hardening

### 5.1 Enable Security Headers

Create Worker or use Transform Rules:

```javascript
// _headers file in repository
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  X-XSS-Protection: 1; mode=block
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';
```

### 5.2 Enable DDoS Protection

Cloudflare automatically provides DDoS protection. For enhanced protection:
```
Security → DDoS → Sensitivity: High
```

---

## Step 6: Analytics & Monitoring

### 6.1 Enable Web Analytics

```
Analytics → Web Analytics → Enable
```

Adds privacy-friendly analytics without cookies.

### 6.2 Set Up Notifications

```
Notifications → Add:
  - SSL certificate expiration
  - DDoS attack detected
  - Pages deployment failures
```

---

## Step 7: Automated Deployment

### 7.1 GitHub Actions Integration

Already configured in `.github/workflows/` - every push to `main` triggers Pages deployment automatically.

### 7.2 Preview Deployments

Pull requests automatically get preview URLs:
```
https://{branch}.spiralsafe.pages.dev
```

---

## Verification Checklist

- [ ] DNS resolves: `spiralsafe.org` → Cloudflare Pages
- [ ] www redirect works: `www.spiralsafe.org` → `spiralsafe.org`
- [ ] HTTPS enabled (no certificate warnings)
- [ ] HTTP → HTTPS redirect active
- [ ] Security headers present (check with securityheaders.com)
- [ ] Brotli compression active (check Network tab)
- [ ] Web Analytics tracking pageviews
- [ ] GitHub auto-deployment working
- [ ] Lighthouse score > 90

---

## Deployment Commands (Quick Reference)

```bash
# Deploy manually (if not using GitHub integration)
npx wrangler pages deploy . --project-name=spiralsafe

# List deployments
npx wrangler pages deployments list --project-name=spiralsafe

# Roll back to previous deployment
npx wrangler pages deployment rollback --project-name=spiralsafe

# View logs
npx wrangler pages functions logs --project-name=spiralsafe

# Check DNS status
npx wrangler pages domain list --project-name=spiralsafe
```

---

## Custom Domain Configuration (spiralsafe.org)

If domain isn't already in Cloudflare:

1. **Transfer nameservers** to Cloudflare:
   - At your registrar (e.g., Namecheap, GoDaddy)
   - Replace existing nameservers with:
     - `amber.ns.cloudflare.com`
     - `ben.ns.cloudflare.com`
   - (Actual nameservers shown in Cloudflare dashboard)

2. **Wait for DNS propagation** (2-48 hours)

3. **Verify** via Cloudflare dashboard (will show "Active")

---

## ATOM Trail Integration

Log deployment events to ATOM trail:

```bash
# On successful deployment
echo "$(date -Iseconds) | ATOM-DEPLOY-$(date +%Y%m%d)-001 | [Cloudflare Pages] | Remote | SpiralSafe.org deployed successfully" >> .atom-trail/deployments.txt
```

---

## Support & Resources

- **Cloudflare Pages Docs:** https://developers.cloudflare.com/pages
- **Wrangler CLI Docs:** https://developers.cloudflare.com/workers/wrangler
- **DNS Propagation Checker:** https://dnschecker.org
- **SSL Checker:** https://www.ssllabs.com/ssltest

---

**Deployment Status:** 🟢 Ready to deploy
**ATOM:** ATOM-DOC-20260104-003-cloudflare-deployment-guide
