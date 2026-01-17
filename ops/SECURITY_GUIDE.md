# 🔐 SpiralSafe API Security Guide

**Version**: 2.1.0
**Last Updated**: 2026-01-07

---

## Table of Contents

1. [Security Features](#security-features)
2. [Rate Limiting](#rate-limiting)
3. [API Key Management](#api-key-management)
4. [Request Logging & Auditing](#request-logging--auditing)
5. [Cloudflare Monitoring Setup](#cloudflare-monitoring-setup)
6. [API Key Rotation](#api-key-rotation)
7. [Security Best Practices](#security-best-practices)

---

## Security Features

SpiralSafe API implements multiple layers of security:

### ✅ Implemented (v2.1.0)

1. **API Key Authentication** - Header-based authentication for all write operations
2. **Rate Limiting** - KV-based request throttling to prevent abuse
3. **Request Logging** - Comprehensive audit trail of all requests
4. **Multiple API Keys** - Support for service-specific keys
5. **Auth Failure Tracking** - Stricter limits on failed authentication attempts
6. **IP-Based Blocking** - Temporary blocks for suspicious activity

### 🚧 Planned (v2.2.0)

1. **JWT Authentication** - Token-based auth for user sessions
2. **OAuth2 Integration** - Third-party authentication
3. **mTLS Support** - Mutual TLS for enterprise clients
4. **WAF Rules** - Custom Web Application Firewall rules

---

## Rate Limiting

### Configuration

Rate limits are configured via Cloudflare secrets (environment variables):

| Variable                   | Default | Description                         |
| -------------------------- | ------- | ----------------------------------- |
| `RATE_LIMIT_REQUESTS`      | 100     | Max requests per IP per window      |
| `RATE_LIMIT_WINDOW`        | 60      | Time window in seconds              |
| `RATE_LIMIT_AUTH_FAILURES` | 5       | Max auth failures per IP per window |

### Setting Rate Limits

```bash
# Set general rate limit to 200 requests per minute
npx wrangler secret put RATE_LIMIT_REQUESTS
# Enter: 200

# Set window to 60 seconds
npx wrangler secret put RATE_LIMIT_WINDOW
# Enter: 60

# Set auth failure limit to 3 attempts per minute
npx wrangler secret put RATE_LIMIT_AUTH_FAILURES
# Enter: 3
```

### Rate Limit Headers

Every response includes rate limit information:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1704732120
```

### Rate Limit Response

When limit exceeded (HTTP 429):

```json
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded. Try again in 42 seconds.",
  "limit": 100,
  "window": 60,
  "resetAt": 1704732120
}
```

### Auth Failure Rate Limiting

Failed authentication attempts have stricter limits:

```json
{
  "error": "Too Many Failed Authentication Attempts",
  "message": "Temporary block due to too many failed attempts. Try again in 58 seconds.",
  "resetAt": 1704732120
}
```

**Purpose**: Prevents brute-force attacks on API keys.

---

## API Key Management

### Primary API Key

Set via Cloudflare secret:

```bash
npx wrangler secret put SPIRALSAFE_API_KEY
# Enter your 64-character hex key
```

**Example Key Format** (use your actual key):

```
your-64-character-hex-api-key-here
```

> **Security Note**: Never commit actual API keys to the repository. Store them securely in Cloudflare Secrets or environment variables.

### Multiple API Keys

For service-specific or environment-specific keys:

```bash
npx wrangler secret put SPIRALSAFE_API_KEYS
# Enter comma-separated keys:
# key1,key2,key3
```

**Example Use Cases**:

```bash
# Development, Staging, Production keys
SPIRALSAFE_API_KEYS=dev_abc123...,staging_def456...,prod_ghi789...

# Service-specific keys
SPIRALSAFE_API_KEYS=helpdesk_key,billing_key,analytics_key
```

### Generating Secure Keys

```bash
# Linux/macOS
openssl rand -hex 32

# PowerShell
-join ((1..32) | ForEach-Object { '{0:x2}' -f (Get-Random -Maximum 256) })

# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

**Key Requirements**:

- Minimum 32 characters (64 hex characters recommended)
- Cryptographically random
- Unique per environment/service
- Never committed to git
- Rotated every 90 days

### Using API Keys

Include in request header:

```bash
curl -X POST https://api.spiralsafe.org/api/wave/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '{"content": "..."}'
```

---

## Request Logging & Auditing

### Log Storage

All requests are logged to two locations:

1. **KV Store** - Last 30 days (automatic expiration)
   - Key format: `log:{timestamp}:{uuid}`
   - TTL: 2,592,000 seconds (30 days)

2. **D1 Database** - Failed auth attempts (permanent)
   - Table: `system_health`
   - Includes: IP, path, user agent, timestamp

### Log Entry Structure

```json
{
  "timestamp": "2026-01-07T17:30:00.000Z",
  "ip": "203.0.113.45",
  "method": "POST",
  "path": "/api/wave/analyze",
  "authenticated": true,
  "status": 200,
  "error": null,
  "userAgent": "curl/7.68.0",
  "country": "US"
}
```

### Querying Logs

#### Via Wrangler CLI

```bash
# List recent KV log keys
npx wrangler kv:key list --binding=SPIRALSAFE_KV --prefix="log:"

# Get specific log entry
npx wrangler kv:key get --binding=SPIRALSAFE_KV "log:1704732000000:abc-123"
```

#### Via D1 Database

```bash
# Query failed auth attempts from last 24 hours
npx wrangler d1 execute spiralsafe-ops --command="
  SELECT * FROM system_health
  WHERE status = 'auth_failure'
  AND timestamp > datetime('now', '-24 hours')
  ORDER BY timestamp DESC
"

# Count failed attempts by IP
npx wrangler d1 execute spiralsafe-ops --command="
  SELECT json_extract(details, '$.ip') as ip, COUNT(*) as attempts
  FROM system_health
  WHERE status = 'auth_failure'
  GROUP BY ip
  ORDER BY attempts DESC
"
```

### Log Analysis Scripts

Create `ops/scripts/analyze-logs.sh`:

```bash
#!/bin/bash

echo "=== Failed Authentication Attempts (Last 24h) ==="
npx wrangler d1 execute spiralsafe-ops --command="
  SELECT
    timestamp,
    json_extract(details, '$.ip') as ip,
    json_extract(details, '$.path') as path,
    json_extract(details, '$.userAgent') as user_agent
  FROM system_health
  WHERE status = 'auth_failure'
  AND timestamp > datetime('now', '-24 hours')
  ORDER BY timestamp DESC
  LIMIT 50
"

echo ""
echo "=== Top Attacking IPs ==="
npx wrangler d1 execute spiralsafe-ops --command="
  SELECT
    json_extract(details, '$.ip') as ip,
    json_extract(details, '$.country') as country,
    COUNT(*) as attempts
  FROM system_health
  WHERE status = 'auth_failure'
  GROUP BY ip
  ORDER BY attempts DESC
  LIMIT 20
"
```

---

## Cloudflare Monitoring Setup

### 1. Analytics Dashboard

**Access**: Cloudflare Dashboard → Workers & Pages → spiralsafe-api → Analytics

**Metrics Available**:

- Requests per second
- Success rate (2xx/3xx responses)
- Error rate (4xx/5xx responses)
- CPU time
- Duration (p50, p75, p99)
- Invocations by country

### 2. Real-Time Logs (Tail Workers)

```bash
# Monitor production logs in real-time
npx wrangler tail spiralsafe-api

# Filter for errors only
npx wrangler tail spiralsafe-api --status error

# Filter by IP
npx wrangler tail spiralsafe-api --ip-address 203.0.113.45

# Filter by method
npx wrangler tail spiralsafe-api --method POST
```

### 3. Logpush (Enterprise Feature)

For high-volume logging to external services:

**Cloudflare Dashboard → Analytics → Logs → Add Logpush job**

Destinations:

- AWS S3
- Google Cloud Storage
- Azure Blob Storage
- Datadog
- Splunk
- Sumo Logic

### 4. Email Alerts

Set up email notifications for critical events:

**Cloudflare Dashboard → Notifications → Add**

**Recommended Alerts**:

| Event               | Threshold  | Action                    |
| ------------------- | ---------- | ------------------------- |
| Error Rate          | > 5%       | Email immediately         |
| Request Rate        | > 1000/min | Email (potential DDoS)    |
| CPU Time            | > 30ms p99 | Email (performance issue) |
| Workers Invocations | 0 for 5min | Email (downtime)          |

**Email Template**:

```
To: ops@spiralsafe.org
Subject: [SpiralSafe] Alert: {event_type}
Body: Worker spiralsafe-api has triggered an alert:
      Event: {event_type}
      Threshold: {threshold}
      Current Value: {current_value}
      Time: {timestamp}
```

### 5. Health Check Monitoring

Use external monitoring service (UptimeRobot, Pingdom, etc.):

**Endpoint**: `https://api.spiralsafe.org/api/health`
**Method**: GET
**Expected Response**: 200 OK
**Check Interval**: 60 seconds

**Response Validation**:

```json
{
  "status": "healthy",
  "checks": {
    "d1": true,
    "kv": true,
    "r2": true
  }
}
```

**Alert Conditions**:

- Status code != 200
- `status` field != "healthy"
- Any `checks` field == false
- Response time > 2000ms
- 3 consecutive failures

### 6. Grafana Dashboard (Advanced)

**Setup**:

1. Deploy Grafana Worker or self-hosted instance
2. Connect to Cloudflare Analytics API
3. Import SpiralSafe dashboard template

**Panels**:

- Request rate timeline
- Error rate percentage
- P50/P75/P99 latency
- Top 10 IPs by request count
- Failed auth attempts timeline
- Geographic request distribution
- Cache hit rate (KV)

---

## API Key Rotation

### Rotation Schedule

| Key Type    | Rotation Frequency | Method               |
| ----------- | ------------------ | -------------------- |
| Production  | Every 90 days      | Overlapping rotation |
| Staging     | Every 180 days     | Direct replacement   |
| Development | Annually           | Direct replacement   |
| Emergency   | Immediately        | Revoke + new key     |

### Overlapping Rotation Process

**Purpose**: Zero-downtime key rotation

**Steps**:

1. **Generate New Key**:

   ```bash
   NEW_KEY=$(openssl rand -hex 32)
   echo "New key: $NEW_KEY"
   ```

2. **Add to Secondary Keys** (both keys now valid):

   ```bash
   npx wrangler secret put SPIRALSAFE_API_KEYS
   # Enter: old_key,new_key
   ```

3. **Update Clients** (over 7-day period):
   - Update internal services to use `$NEW_KEY`
   - Update documentation
   - Notify external API consumers

4. **Remove Old Key** (after all clients migrated):

   ```bash
   npx wrangler secret put SPIRALSAFE_API_KEYS
   # Enter: new_key
   ```

5. **Document Rotation**:
   ```bash
   echo "$(date '+%Y-%m-%d') - Rotated API key from OLD_KEY to NEW_KEY" >> ops/KEY_ROTATION_LOG.md
   ```

### Emergency Rotation (Compromised Key)

**Immediate Actions**:

1. **Revoke Compromised Key**:

   ```bash
   # Remove from all key lists
   npx wrangler secret put SPIRALSAFE_API_KEY
   # Enter new key immediately

   npx wrangler secret put SPIRALSAFE_API_KEYS
   # Enter only non-compromised keys
   ```

2. **Audit Recent Activity**:

   ```bash
   npx wrangler d1 execute spiralsafe-ops --command="
     SELECT * FROM system_health
     WHERE timestamp > datetime('now', '-7 days')
     ORDER BY timestamp DESC
   "
   ```

3. **Review Logs for Suspicious Activity**:

   ```bash
   # Check for unusual IPs, countries, or request patterns
   npx wrangler kv:key list --binding=SPIRALSAFE_KV --prefix="log:"
   ```

4. **Notify Stakeholders**:
   - Internal team via Slack/email
   - Affected customers if data breach suspected
   - Security team for incident report

5. **Post-Incident**:
   - Document timeline in `ops/SECURITY_INCIDENTS.md`
   - Update rotation schedule (more frequent)
   - Review access controls

### Automated Rotation (Advanced)

Create `ops/scripts/rotate-api-key.sh`:

```bash
#!/bin/bash

# Generate new key
NEW_KEY=$(openssl rand -hex 32)

# Get current secondary keys
CURRENT_KEYS=$(npx wrangler secret get SPIRALSAFE_API_KEYS 2>/dev/null || echo "")

# Add new key to secondary keys
if [ -z "$CURRENT_KEYS" ]; then
  UPDATED_KEYS="$NEW_KEY"
else
  UPDATED_KEYS="$CURRENT_KEYS,$NEW_KEY"
fi

# Update secrets
echo "$UPDATED_KEYS" | npx wrangler secret put SPIRALSAFE_API_KEYS

# Log rotation
echo "$(date '+%Y-%m-%d %H:%M:%S') - Added new key: $NEW_KEY" >> ops/KEY_ROTATION_LOG.md

# Output for manual client updates
echo "New API key generated: $NEW_KEY"
echo "Update clients within 7 days"
echo "Remove old keys from SPIRALSAFE_API_KEYS after migration"
```

### Key Rotation Checklist

- [ ] Generate cryptographically secure new key
- [ ] Add new key to `SPIRALSAFE_API_KEYS` (overlapping)
- [ ] Update internal services
- [ ] Update documentation
- [ ] Notify external API consumers
- [ ] Monitor logs for migration progress
- [ ] Remove old key after 100% migration
- [ ] Update `KEY_ROTATION_LOG.md`
- [ ] Test all endpoints with new key
- [ ] Archive old key securely (for incident investigation)

---

## Security Best Practices

### 1. Principle of Least Privilege

- Create service-specific API keys
- Limit key access to required endpoints only
- Use separate keys for dev/staging/prod

### 2. Key Storage

**✅ DO**:

- Store in password manager (1Password, LastPass)
- Use environment variables
- Encrypt at rest
- Use Cloudflare secrets for production

**❌ DON'T**:

- Commit to git
- Store in plaintext files
- Share via email/chat
- Reuse across environments

### 3. Network Security

- Enable Cloudflare WAF rules
- Configure IP allowlists for admin endpoints
- Use Cloudflare Access for internal tools
- Enable DDoS protection

### 4. Monitoring & Alerting

- Set up real-time log monitoring
- Configure email alerts for anomalies
- Review audit logs weekly
- Track failed auth attempts

### 5. Incident Response

- Maintain `SECURITY_INCIDENTS.md` log
- Have key rotation playbook ready
- Document escalation procedures
- Conduct quarterly security reviews

### 6. Compliance

- GDPR: Log retention (30 days KV, configurable D1)
- SOC 2: Audit trail for all write operations
- PCI DSS: Rate limiting, encryption in transit
- HIPAA: Request logging, access controls

---

## Security Contacts

**Security Issues**: security@spiralsafe.org
**API Support**: api@spiralsafe.org
**Emergency Hotline**: +1-XXX-XXX-XXXX (24/7)

**Bug Bounty Program**: Coming soon (v2.2.0)

---

## Appendix: Environment Variables

| Variable                   | Required | Default | Description                     |
| -------------------------- | -------- | ------- | ------------------------------- |
| `SPIRALSAFE_API_KEY`       | ✅ Yes   | -       | Primary API key                 |
| `SPIRALSAFE_API_KEYS`      | ❌ No    | -       | Comma-separated additional keys |
| `RATE_LIMIT_REQUESTS`      | ❌ No    | 100     | Max requests per window         |
| `RATE_LIMIT_WINDOW`        | ❌ No    | 60      | Window duration (seconds)       |
| `RATE_LIMIT_AUTH_FAILURES` | ❌ No    | 5       | Max auth failures per window    |
| `CLOUDFLARE_ACCOUNT_ID`    | ✅ Yes   | -       | Cloudflare account ID           |
| `CLOUDFLARE_API_TOKEN`     | ✅ Yes   | -       | Wrangler deployment token       |

---

**H&&S:WAVE** | From the constraints, gifts. From the spiral, safety.

```
Version: 2.1.0-security
Status: SECURITY ENHANCED
Last Updated: 2026-01-07
Next Key Rotation: 2026-04-07
```

🔐 **Security Commitment**: We take security seriously. Report vulnerabilities responsibly.
