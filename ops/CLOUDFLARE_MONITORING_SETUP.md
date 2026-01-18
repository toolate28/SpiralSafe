# 📊 Cloudflare Monitoring Setup Guide

**SpiralSafe Operations API**
**Target**: api.spiralsafe.org
**Worker**: spiralsafe-api

---

## Quick Start Checklist

- [ ] Enable Cloudflare Analytics
- [ ] Configure email notifications
- [ ] Set up real-time log tailing
- [ ] Create monitoring dashboard
- [ ] Configure external health checks
- [ ] Test alert triggers

---

## 1. Enable Analytics (Built-in)

### Access Analytics Dashboard

1. Log in to Cloudflare Dashboard
2. Navigate to **Workers & Pages**
3. Click **spiralsafe-api**
4. Click **Analytics** tab

### Available Metrics

**Request Metrics**:

- Total requests (24h, 7d, 30d views)
- Requests per second (real-time)
- Success rate percentage
- Error breakdown (4xx vs 5xx)

**Performance Metrics**:

- CPU time (avg, p50, p75, p99)
- Duration (avg, p50, p75, p99)
- Wall time vs CPU time

**Geographic Distribution**:

- Requests by country
- Requests by Cloudflare data center

### Export Analytics Data

```bash
# Via Cloudflare API
curl -X GET "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/workers/scripts/spiralsafe-api/metrics" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json"
```

---

## 2. Configure Email Notifications

### Step-by-Step Setup

1. **Navigate to Notifications**:
   - Cloudflare Dashboard → Notifications → Add

2. **Create Worker Error Rate Alert**:
   - **Event Type**: Workers
   - **Worker**: spiralsafe-api
   - **Metric**: Error Rate
   - **Threshold**: Greater than 5%
   - **Time Period**: 5 minutes
   - **Recipients**: ops@spiralsafe.org, toolate28@spiralsafe.org
   - **Delivery Method**: Email

3. **Create High Request Rate Alert** (DDoS Detection):
   - **Event Type**: Workers
   - **Worker**: spiralsafe-api
   - **Metric**: Requests per minute
   - **Threshold**: Greater than 1000
   - **Time Period**: 5 minutes
   - **Recipients**: ops@spiralsafe.org
   - **Delivery Method**: Email + SMS (if available)

4. **Create Performance Degradation Alert**:
   - **Event Type**: Workers
   - **Worker**: spiralsafe-api
   - **Metric**: CPU time (p99)
   - **Threshold**: Greater than 50ms
   - **Time Period**: 10 minutes
   - **Recipients**: dev@spiralsafe.org
   - **Delivery Method**: Email

5. **Create Downtime Alert**:
   - **Event Type**: Workers
   - **Worker**: spiralsafe-api
   - **Metric**: Invocations
   - **Threshold**: Equal to 0
   - **Time Period**: 5 minutes
   - **Recipients**: ops@spiralsafe.org, toolate28@spiralsafe.org
   - **Delivery Method**: Email + PagerDuty (if configured)

### Test Alerts

```bash
# Trigger error rate alert by sending invalid requests
for i in {1..20}; do
  curl -X POST https://api.spiralsafe.org/api/wave/analyze \
    -H "X-API-Key: invalid-key-trigger-alert" \
    -d '{"content":"test"}'
done

# Check if alert email received within 5 minutes
```

---

## 3. Real-Time Log Tailing

### Basic Tailing

```bash
# Monitor all requests in real-time
npx wrangler tail spiralsafe-api

# Output format:
# GET https://api.spiralsafe.org/api/health - Ok @ 1/7/2026, 5:30:00 PM
```

### Advanced Filtering

```bash
# Only show errors (4xx, 5xx)
npx wrangler tail spiralsafe-api --status error

# Filter by specific status code
npx wrangler tail spiralsafe-api --status-code 401

# Filter by IP address
npx wrangler tail spiralsafe-api --ip-address 203.0.113.45

# Filter by HTTP method
npx wrangler tail spiralsafe-api --method POST

# Filter by header (requires custom logging)
npx wrangler tail spiralsafe-api --header "X-API-Key"

# Sample only 10% of requests (high volume)
npx wrangler tail spiralsafe-api --sampling-rate 0.1
```

### Save Logs to File

```bash
# Tail logs and save to file
npx wrangler tail spiralsafe-api >> logs/production-$(date +%Y%m%d).log

# With timestamps
npx wrangler tail spiralsafe-api | while read line; do
  echo "$(date -Iseconds) $line"
done >> logs/production-$(date +%Y%m%d).log
```

### Automated Log Collection Script

Create `ops/scripts/collect-logs.sh`:

```bash
#!/bin/bash

LOG_DIR="logs/production"
mkdir -p "$LOG_DIR"

FILENAME="$LOG_DIR/$(date +%Y%m%d-%H%M%S).log"

echo "Collecting logs to: $FILENAME"
echo "Press Ctrl+C to stop"

npx wrangler tail spiralsafe-api | while read line; do
  echo "$(date -Iseconds) $line" >> "$FILENAME"
done
```

Run in background:

```bash
nohup ./ops/scripts/collect-logs.sh &
```

---

## 4. Create Monitoring Dashboard

### Option A: Cloudflare Dashboard (Built-in)

**Access**: Cloudflare Dashboard → Workers & Pages → spiralsafe-api → Analytics

**Custom Time Ranges**:

- Last 24 hours
- Last 7 days
- Last 30 days
- Custom date range

**Export Options**:

- Download CSV
- API export (for external dashboards)

### Option B: Grafana Dashboard

**Prerequisites**:

- Grafana instance (self-hosted or Grafana Cloud)
- Cloudflare API token with Analytics read permissions

**Setup Steps**:

1. **Install Cloudflare Grafana Plugin**:

   ```bash
   grafana-cli plugins install cloudflare-app
   ```

2. **Configure Data Source**:
   - Grafana → Configuration → Data Sources → Add data source
   - Select "Cloudflare"
   - Enter API token
   - Select account

3. **Import Dashboard Template**:

   ```bash
   # Download SpiralSafe dashboard template
   curl -o grafana-dashboard.json https://gist.github.com/.../spiralsafe-dashboard.json

   # Import in Grafana
   # Grafana → Dashboards → Import → Upload JSON
   ```

4. **Dashboard Panels**:
   - Request rate (requests/sec)
   - Error rate (%)
   - P50/P75/P99 latency
   - Success vs Error status codes
   - Top 10 IPs by request count
   - Failed auth attempts timeline
   - Geographic distribution map
   - KV operations count

### Option C: Custom Analytics with Workers Analytics Engine

**Enable Analytics Engine**:

```toml
# ops/wrangler.toml
[analytics_engine_datasets]
binding = "ANALYTICS"
```

**Write Custom Events**:

```typescript
// In spiralsafe-worker.ts
env.ANALYTICS.writeDataPoint({
  blobs: [path, ip, userAgent],
  doubles: [responseTime, status],
  indexes: [timestamp],
});
```

**Query via GraphQL**:

```bash
curl -X POST https://api.cloudflare.com/client/v4/graphql \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -d '{
    "query": "query { viewer { accounts(filter: {accountTag: $accountId}) { analyticsEngineDatasets(filter: {name: $datasetName}) { ... } } } }"
  }'
```

---

## 5. External Health Check Monitoring

### UptimeRobot Setup (Free Tier)

1. **Sign up**: https://uptimerobot.com

2. **Add New Monitor**:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: SpiralSafe API Health
   - **URL**: https://api.spiralsafe.org/api/health
   - **Monitoring Interval**: 5 minutes (free tier)
   - **Monitor Timeout**: 30 seconds

3. **Set Alert Contacts**:
   - Email: ops@spiralsafe.org
   - SMS: +1-XXX-XXX-XXXX (optional)

4. **Configure Keyword Monitoring**:
   - **Keyword**: "healthy"
   - **Alert if keyword not found**: Yes

5. **Status Page** (optional):
   - Create public status page: status.spiralsafe.org
   - Show uptime percentage
   - Incident history

### Pingdom Setup (Paid)

**Advantages**: More frequent checks (1min), global locations, advanced alerting

1. **Add Check**:
   - **Check Type**: HTTP
   - **Name**: SpiralSafe API Health
   - **URL**: https://api.spiralsafe.org/api/health
   - **Check Interval**: 1 minute

2. **Advanced Settings**:
   - **Validation**:
     ```json
     "status": "healthy"
     ```
   - **Headers**:
     ```
     User-Agent: Pingdom-Health-Check
     ```

3. **Test from Multiple Locations**:
   - North America (Virginia)
   - Europe (London)
   - Asia (Tokyo)
   - Australia (Sydney)

4. **Integrate with Slack**:
   - Pingdom → Integrations → Add Slack
   - Webhook URL: https://hooks.slack.com/services/YOUR/WEBHOOK
   - Channel: #spiralsafe-alerts

### Custom Health Check Script

For internal monitoring, create `ops/scripts/health-check.sh`:

```bash
#!/bin/bash

ENDPOINT="https://api.spiralsafe.org/api/health"
WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK"

# Make request
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$ENDPOINT")

if [ "$RESPONSE" -ne 200 ]; then
  # Send Slack alert
  curl -X POST "$WEBHOOK_URL" \
    -H 'Content-Type: application/json' \
    -d "{
      \"text\": \"🚨 SpiralSafe API Health Check Failed\",
      \"attachments\": [{
        \"color\": \"danger\",
        \"fields\": [
          {\"title\": \"Status Code\", \"value\": \"$RESPONSE\", \"short\": true},
          {\"title\": \"Endpoint\", \"value\": \"$ENDPOINT\", \"short\": false}
        ]
      }]
    }"

  echo "$(date -Iseconds) - Health check failed: HTTP $RESPONSE" >> logs/health-check.log
  exit 1
fi

echo "$(date -Iseconds) - Health check passed" >> logs/health-check.log
```

Run via cron (every 5 minutes):

```cron
*/5 * * * * /path/to/ops/scripts/health-check.sh
```

---

## 6. Test Alert Triggers

### Test Error Rate Alert

```bash
# Generate 100 failed auth requests within 2 minutes
for i in {1..100}; do
  curl -X POST https://api.spiralsafe.org/api/wave/analyze \
    -H "X-API-Key: intentionally-wrong-key" \
    -d '{"content":"test"}' &
done
wait

# Expected: Email alert within 5 minutes
```

### Test High Request Rate Alert

```bash
# Generate 2000 requests within 1 minute (if threshold is 1000/min)
for i in {1..2000}; do
  curl -s https://api.spiralsafe.org/api/health > /dev/null &
  if [ $((i % 100)) -eq 0 ]; then
    wait # Prevent overwhelming local system
  fi
done

# Expected: Email alert for potential DDoS
```

### Test Downtime Alert

**Simulate downtime** (NOT recommended for production):

```bash
# Disable worker temporarily
npx wrangler publish --name spiralsafe-api-down --route "api-down.spiralsafe.org/*"

# Wait 5 minutes
sleep 300

# Re-enable production worker
npx wrangler publish

# Expected: Downtime alert email
```

**Better alternative**: Use Cloudflare maintenance mode or preview environment

---

## 7. Integrate with Third-Party Services

### Datadog

**Setup**:

1. Install Datadog Cloudflare integration
2. Add API token to Datadog
3. Configure log forwarding (Logpush)

**Benefits**:

- Unified monitoring with other services
- Advanced log querying
- Anomaly detection
- Custom dashboards

### Sentry (Error Tracking)

**Add to worker**:

```typescript
// ops/api/spiralsafe-worker.ts
import * as Sentry from '@sentry/cloudflare';

Sentry.init({
  dsn: env.SENTRY_DSN,
  tracesSampleRate: 0.1,
});

// In catch blocks
catch (error) {
  Sentry.captureException(error);
  // ... existing error handling
}
```

**Configure**:

```bash
npx wrangler secret put SENTRY_DSN
# Enter: https://YOUR_KEY@o12345.ingest.sentry.io/67890
```

### PagerDuty (On-call Alerts)

**Integration Steps**:

1. PagerDuty → Services → Add Service
2. Integration Type: Cloudflare
3. Copy Integration Key
4. Cloudflare → Notifications → Add → PagerDuty
5. Paste Integration Key

**Escalation Policy**:

- Level 1 (5 min): On-call engineer (email + SMS)
- Level 2 (15 min): Team lead (phone call)
- Level 3 (30 min): VP Engineering (phone call)

---

## 8. Security Monitoring

### Monitor Failed Auth Attempts

Create `ops/scripts/security-check.sh`:

```bash
#!/bin/bash

# Check for suspicious failed auth patterns
SUSPICIOUS_IPS=$(npx wrangler d1 execute spiralsafe-ops --command="
  SELECT
    json_extract(details, '$.ip') as ip,
    COUNT(*) as attempts
  FROM system_health
  WHERE status = 'auth_failure'
  AND timestamp > datetime('now', '-1 hour')
  GROUP BY ip
  HAVING attempts > 10
  ORDER BY attempts DESC
" --json)

if [ -n "$SUSPICIOUS_IPS" ]; then
  echo "⚠️  Suspicious IPs detected with >10 failed auth attempts in last hour:"
  echo "$SUSPICIOUS_IPS"

  # Send Slack alert
  curl -X POST "$SLACK_WEBHOOK_URL" \
    -H 'Content-Type: application/json' \
    -d "{
      \"text\": \"🔒 Security Alert: Brute Force Detected\",
      \"attachments\": [{
        \"color\": \"warning\",
        \"text\": \"Multiple IPs with >10 failed auth attempts in last hour\",
        \"fields\": [{\"title\": \"Details\", \"value\": \"$SUSPICIOUS_IPS\"}]
      }]
    }"
fi
```

Run hourly via cron:

```cron
0 * * * * /path/to/ops/scripts/security-check.sh
```

### Monitor Rate Limit Hits

```bash
# Query KV for rate limit keys
npx wrangler kv:key list --binding=SPIRALSAFE_KV --prefix="ratelimit:auth_failures"

# Check for IPs hitting auth failure rate limit frequently
```

---

## 9. Performance Monitoring

### Track P99 Latency

```bash
# View latency distribution in Cloudflare Analytics
# Dashboard → Workers → spiralsafe-api → Analytics → Duration

# Set up alert if p99 > 100ms (configured in step 2)
```

### CPU Time Analysis

```bash
# Identify slow endpoints
npx wrangler tail spiralsafe-api | grep "CPU time" | sort -t: -k2 -nr
```

### Database Query Performance

```bash
# Enable D1 query logging (when available)
npx wrangler d1 execute spiralsafe-ops --command="PRAGMA query_only = ON"

# Monitor slow queries in production logs
```

---

## 10. Cost Monitoring

### Track Worker Invocations

**Free Tier Limits**:

- 100,000 requests/day
- 10ms CPU time per request

**Paid Plan** ($5/month):

- 10 million requests/month included
- $0.50 per additional million

**Check Current Usage**:

```bash
curl -X GET "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/workers/scripts/spiralsafe-api/usage" \
  -H "Authorization: Bearer $CF_API_TOKEN"
```

### Monitor Storage Costs

**D1 Database**:

- Free: 5 GB storage, 5 million reads/day
- Paid: $0.50/GB/month, $0.001 per 1000 reads

**KV Namespace**:

- Free: 100,000 reads/day, 1000 writes/day
- Paid: $0.50 per million reads, $5 per million writes

**R2 Storage**:

- Free: 10 GB storage, 1 million Class A operations/month
- Paid: $0.015/GB/month

**Check Storage Usage**:

```bash
# D1
npx wrangler d1 info spiralsafe-ops

# KV
npx wrangler kv:namespace list

# R2
npx wrangler r2 bucket list
```

---

## Monitoring Dashboard URLs

**Cloudflare Analytics**:
`https://dash.cloudflare.com/<account_id>/workers/services/view/spiralsafe-api/production/analytics`

**Health Endpoint**:
`https://api.spiralsafe.org/api/health`

**Status Page** (if configured):
`https://status.spiralsafe.org`

---

## Troubleshooting

### No Metrics Showing in Dashboard

**Cause**: Worker not receiving traffic
**Solution**: Check routes in wrangler.toml, verify DNS

### Email Alerts Not Received

**Cause**: Notification settings incorrect
**Solution**: Verify email address in Cloudflare notifications, check spam folder

### Real-Time Logs Not Showing

**Cause**: Wrangler not authenticated
**Solution**: Run `npx wrangler login` and re-authenticate

### High CPU Time

**Cause**: Inefficient database queries or complex computations
**Solution**: Review query plans, add indexes, optimize algorithms

---

## Next Steps

- [ ] Set up weekly security review meetings
- [ ] Create runbook for common incidents
- [ ] Configure automated reporting (daily/weekly summaries)
- [ ] Set up synthetic monitoring for critical user flows
- [ ] Implement custom business metrics (WAVE coherence scores, etc.)

---

**H&&S:WAVE** | From the constraints, gifts. From the spiral, safety.

```
Monitoring Version: 2.1.0
Last Updated: 2026-01-07
Maintained by: SpiralSafe Operations Team
```

📊 **Observability Commitment**: Comprehensive monitoring ensures reliability and security.
