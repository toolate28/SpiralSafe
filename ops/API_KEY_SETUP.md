# API Key Setup Guide

This guide explains how to generate and configure the API key for SpiralSafe Operations API.

## Overview

The SpiralSafe API protects all write endpoints (POST, PUT, DELETE) with API key authentication using the `X-API-Key` header. Read endpoints (GET) remain publicly accessible.

## Protected Endpoints

All endpoints with these HTTP methods require authentication:
- `POST /api/wave/analyze` - Coherence analysis
- `POST /api/bump/create` - Create routing markers
- `PUT /api/bump/resolve/{id}` - Resolve bumps
- `POST /api/awi/request` - Request AWI grants
- `POST /api/awi/verify` - Verify permissions
- `POST /api/atom/create` - Create task atoms
- `PUT /api/atom/status/{id}` - Update atom status
- `POST /api/context/store` - Store context units

## Setup Instructions

### 1. Generate a Strong API Key

**Recommended**: Use bash/openssl for maximum security (256-bit entropy):

```bash
# Generate a strong API key (64 hex characters = 256 bits of entropy)
openssl rand -hex 32
```

Alternatively, use PowerShell (190-bit entropy):

```powershell
# Navigate to ops directory
cd $env:USERPROFILE\repos\SpiralSafe\ops

# Generate a strong API key (64 random alphanumeric characters)
$apiKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | % {[char]$_})
Write-Host "Your API key: $apiKey"
```

**Important**: Store this key securely. You'll need it for the next step.

### 2. Store as Cloudflare Secret

Store the generated API key as a Cloudflare Worker secret:

```bash
# Navigate to ops directory
cd ops

# Set the secret (you'll be prompted to enter the key)
npx wrangler secret put SPIRALSAFE_API_KEY
```

When prompted, paste the API key generated in step 1.

### 3. Redeploy the Worker

After setting the secret, redeploy the worker:

```bash
npx wrangler deploy
```

For development environment:

```bash
npx wrangler deploy --env dev
```

## Usage

### Making Authenticated Requests

Include the API key in the `X-API-Key` header:

```bash
# Example: Create a bump marker
curl -X POST https://api.spiralsafe.org/api/bump/create \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -d '{
    "type": "WAVE",
    "from": "copilot",
    "to": "claude",
    "state": "pending",
    "context": {"pr": "#50"}
  }'
```

### Unauthorized Response

Requests without a valid API key will receive:

```json
{
  "error": "Unauthorized"
}
```

HTTP Status: `401 Unauthorized`

## Security Best Practices

1. **Never commit the API key** to version control
2. **Use environment-specific keys** - different keys for dev and production
3. **Rotate keys periodically** - update the secret and redeploy
4. **Limit key sharing** - only share with authorized systems/users
5. **Monitor usage** - check Cloudflare Worker analytics for unauthorized attempts

## Troubleshooting

### "Unauthorized" Error

- Verify the API key is set correctly: `npx wrangler secret list`
- Ensure the `X-API-Key` header is included in your request
- Check that the key matches exactly (no extra spaces or characters)

### Key Not Working After Update

- Redeploy the worker after updating secrets
- Allow a few seconds for propagation across Cloudflare's network

### Testing Authentication

Test with a GET request (no auth required):

```bash
curl https://api.spiralsafe.org/api/health
```

Then test with a POST request (auth required):

```bash
curl -X POST https://api.spiralsafe.org/api/wave/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -d '{"content": "test content"}'
```

## Custom Domain Configuration

If you want to remove the custom domain route and rely solely on workers.dev with Cloudflare Access:

1. Edit `wrangler.toml` and comment out the routes section:

```toml
# Production route
# routes = [
#   { pattern = "api.spiralsafe.org/*", zone_name = "spiralsafe.org" }
# ]
```

2. Redeploy:

```bash
npx wrangler deploy
```

3. Access the API via: `https://spiralsafe-api.ACCOUNT.workers.dev`

## References

- [Cloudflare Workers Secrets Documentation](https://developers.cloudflare.com/workers/configuration/secrets/)
- [Wrangler CLI Reference](https://developers.cloudflare.com/workers/wrangler/commands/)
- [SpiralSafe Protocol Documentation](../protocol/)
