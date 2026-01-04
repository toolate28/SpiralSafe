# SpiralSafe Domain Architecture Plan
## spiralsafe.org Subdomain Strategy

```
spiralsafe.org (apex)
├── www.spiralsafe.org          → Main website (SpiralSafe framework)
├── logs.spiralsafe.org         → Logdy Central dashboard
├── moc.spiralsafe.org          → Museum of Computation (Minecraft exhibits)
├── docs.spiralsafe.org         → Documentation hub
├── api.spiralsafe.org          → API endpoints (future)
└── cdn.spiralsafe.org          → Static assets (future)
```

---

## Deployment Plan

### 1. Main Site (spiralsafe.org + www)
- **Source:** SpiralSafe GitHub repo
- **Platform:** Cloudflare Pages
- **Content:** Framework documentation, philosophy, downloads
- **Status:** Ready to deploy

### 2. Logdy Central (logs.spiralsafe.org)
- **Source:** Logdy instance with KENL config
- **Platform:** Cloudflare Tunnel → localhost:8081
- **Content:** Real-time log aggregation dashboard
- **Auth:** Basic auth (username/password)
- **Status:** Needs tunnel setup

### 3. Museum of Computation (moc.spiralsafe.org)
- **Source:** Museum builds from `/museum` directory
- **Platform:** Cloudflare Pages (static site)
- **Content:** Interactive Minecraft exhibit catalog, download links
- **Features:** 3D previews (via three.js), schematic downloads
- **Status:** Needs static site generation

### 4. Documentation Hub (docs.spiralsafe.org)
- **Source:** All markdown docs compiled
- **Platform:** Cloudflare Pages (Docusaurus or similar)
- **Content:** API docs, guides, tutorials
- **Status:** Future enhancement

---

## DNS Configuration (Cloudflare)

```dns
# A/AAAA records (via Cloudflare Pages)
spiralsafe.org              CNAME   spiralsafe.pages.dev        [Proxied]
www.spiralsafe.org          CNAME   spiralsafe.pages.dev        [Proxied]
moc.spiralsafe.org          CNAME   moc-spiralsafe.pages.dev    [Proxied]

# Tunnel for Logdy (localhost:8081)
logs.spiralsafe.org         CNAME   <tunnel-id>.cfargotunnel.com [Proxied]
```

---

## Execution Steps

### Phase 1: Cloudflare Tunnel for Logdy
```bash
# Install cloudflared
winget install Cloudflare.cloudflared

# Login and create tunnel
cloudflared tunnel login
cloudflared tunnel create spiralsafe-logs

# Configure tunnel
# File: ~/.cloudflared/config.yml
```

### Phase 2: Deploy Main Site
```bash
cd ~/repos/SpiralSafe
npx wrangler pages deploy . --project-name=spiralsafe
npx wrangler pages domain add spiralsafe.org
npx wrangler pages domain add www.spiralsafe.org
```

### Phase 3: Deploy Museum of Computation
```bash
# Create static site from museum builds
cd ~/repos/SpiralSafe/museum
# Generate index.html with exhibit catalog
npx wrangler pages deploy builds --project-name=moc-spiralsafe
npx wrangler pages domain add moc.spiralsafe.org
```

---

## Implementation (Immediate)

**Now executing...**
