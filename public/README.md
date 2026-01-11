# SpiralSafe Public Site

## Deployment

### Cloudflare Pages (Recommended)

```bash
# From public directory
npx wrangler pages deploy . --project-name spiralsafe

# Or from root
npx wrangler pages deploy public --project-name spiralsafe
```

### GitHub Pages

1. Enable GitHub Pages in repository settings
2. Point to `public` folder on main branch
3. Site will be live at `https://toolate28.github.io/SpiralSafe`

### Vercel (Alternative)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from public directory
cd public
vercel --prod
```

## URL

**Production**: https://spiralsafe.org (custom domain)
**Cloudflare Pages**: https://spiralsafe.pages.dev
**GitHub Pages**: https://toolate28.github.io/SpiralSafe

## Update Deployment

```bash
# Pull latest changes
git pull origin main

# Redeploy
cd public
npx wrangler pages deploy . --project-name spiralsafe
```

## Status Check

Visit: https://spiralsafe.org
Expected: Beautiful landing page with H&&S:WAVE protocol information
