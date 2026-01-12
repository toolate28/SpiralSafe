# SpiralSafe Operations

> **The coherence engine made operational**

This directory contains the infrastructure layer that transforms SpiralSafe protocols into living systems. Where the root `/docs` directory defines *what* SpiralSafe is, `/ops` defines *how* it runs.

---

## Architecture

```
spiralsafe-ops/
├── api/                    # Cloudflare Worker API
│   └── spiralsafe-worker.ts    # Main coordination endpoint
├── schemas/               # Database definitions
│   └── d1-schema.sql          # D1 table structure
├── scripts/               # CLI tools
│   ├── spiralsafe             # Bash CLI (Unix/Mac)
│   └── SpiralSafe.psm1        # PowerShell module (Windows)
├── integrations/          # External service bridges
│   ├── README.md              # Integration overview
│   └── sentry.md              # Sentry ↔ SAIF bridge
├── .github/
│   └── workflows/
│       └── ci.yml             # CI/CD with coherence gates
├── wrangler.toml          # Cloudflare deployment config
├── package.json           # Node.js package definition
└── tsconfig.json          # TypeScript configuration
```

---

## Quick Start

### 1. Prerequisites

- Node.js 18+
- Cloudflare account with Workers, D1, KV, R2 enabled
- Wrangler CLI (`npm install -g wrangler`)
- ShellCheck (for script linting) - CI runs it automatically; install locally with your package manager (e.g., `apt install shellcheck` or `choco install shellcheck`)
- PowerShell 7+ (`pwsh`) and PSScriptAnalyzer for PowerShell linting (`Install-Module -Name PSScriptAnalyzer -Force -Scope CurrentUser`)

### 2. Initial Setup

```bash
# Clone and install
git clone https://github.com/toolate28/SpiralSafe.git
cd SpiralSafe/ops
npm install

# Authenticate with Cloudflare
wrangler login

# Create backend resources
npm run setup
# This creates: D1 database, KV namespace, R2 bucket

# Initialize database schema
npm run db:migrate
```

### 3. Deploy

```bash
# Deploy to production
npm run deploy

# Or deploy to dev environment
npm run deploy:dev
```

### 4. Configure Local CLI

**Bash (Unix/Mac):**
```bash
# Add to ~/.bashrc or ~/.zshrc
export SPIRALSAFE_API_BASE="https://api.spiralsafe.org"

# Make CLI executable and link
chmod +x ./scripts/spiralsafe
sudo ln -s $(pwd)/scripts/spiralsafe /usr/local/bin/spiralsafe
```

**PowerShell (Windows):**
```powershell
# Add to $PROFILE
$env:SPIRALSAFE_API_BASE = "https://api.spiralsafe.org"
Import-Module /path/to/spiralsafe-ops/scripts/SpiralSafe.psm1
```

### 5. Verify

```bash
spiralsafe status
```

Expected output:
```
SpiralSafe Operations Status
════════════════════════════════════════

  Local Configuration:
    API Base: https://api.spiralsafe.org
    AWI Grant: (none)

  API Status:
    Status: healthy
    D1: ✓
    KV: ✓
    R2: ✓
```

---

## CLI Reference

### Wave - Coherence Analysis

```bash
# Analyze a directory
spiralsafe wave analyze ./docs

# Analyze specific content
spiralsafe wave analyze --content "Text to analyze"

# Local mode (no API)
spiralsafe wave analyze ./docs --local

# View threshold configuration
spiralsafe wave thresholds
```

### Bump - Routing & Handoff

```bash
# Create handoff marker
spiralsafe bump WAVE --to copilot --state "PR ready"
spiralsafe bump PASS --to human --state "Review complete"
spiralsafe bump BLOCK --to oncall --state "Critical issue"

# List pending bumps
spiralsafe bump list

# Resolve a bump
spiralsafe bump resolve <bump-id>
```

### AWI - Permission Scaffolding

```bash
# Request permission
spiralsafe awi request \
  --intent "Deploy documentation update" \
  --resources "docs/*" \
  --actions "modify,create" \
  --level 2 \
  --ttl 3600

# Verify an action against current grant
spiralsafe awi verify --action "modify:README.md"

# View audit trail
spiralsafe awi audit <grant-id>
```

### Session Reports

Run and export session reports from the command line (creates `.atom-trail/sessions/*.json` and optional encrypted bundle):

```bash
# Start a session
python ops/scripts/session_report.py start "verification-session"

# Close session and generate report (encrypts if Transcript-Pipeline is available)
python ops/scripts/session_report.py signout ATOM-SESSION-20260107-001-verification-session
```

### Status

```bash
# Full system status
spiralsafe status
```

---

## API Endpoints

Base URL: `https://api.spiralsafe.org`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | System health check |
| `/api/wave/analyze` | POST | Coherence analysis |
| `/api/wave/thresholds` | GET | Threshold configuration |
| `/api/bump/create` | POST | Create handoff marker |
| `/api/bump/pending` | GET | List unresolved bumps |
| `/api/bump/resolve/:id` | PUT | Resolve a bump |
| `/api/awi/request` | POST | Request permission grant |
| `/api/awi/verify` | POST | Verify action permission |
| `/api/awi/audit/:id` | GET | Permission audit trail |
| `/api/atom/create` | POST | Create task unit |
| `/api/atom/status/:id` | PUT | Update task status |
| `/api/atom/ready` | GET | Get executable atoms |
| `/api/context/store` | POST | Store knowledge unit |
| `/api/context/query` | GET | Query contexts |

---

## Integration Points

### GitHub Actions

The CI workflow (`.github/workflows/ci.yml`) implements:

1. **Coherence Gate**: Wave analysis on PRs
2. **AWI Logging**: Permission audit for deployments
3. **Bump Markers**: Automated handoff tracking
4. **SAIF Triggers**: Investigation on failures

### Sentry

See `integrations/sentry.md` for:

- Webhook configuration
- Error → SAIF mapping
- Seer → hypothesis bridging
- Alert → bump routing

### Vercel

Deployment hooks create:

- AWI grants for deploy actions
- SYNC bumps for state propagation
- Wave checks on build artifacts

---

## Development

### Local Development

```bash
# Start local worker
npm run dev

# Local API is available at http://localhost:8787
```

### Database Migrations

```bash
# Apply schema to dev
npm run db:migrate:dev

# Apply to production
npm run db:migrate
```

### Testing

```bash
# Run tests
npm test

# Watch mode
npm run test:watch
```

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SPIRALSAFE_API_BASE` | No | `https://api.spiralsafe.org` | API endpoint |
| `SPIRALSAFE_AWI_GRANT` | No | - | Current permission grant ID |
| `SPIRALSAFE_LOCAL` | No | `false` | Use local analysis mode |

### Cloudflare Secrets

Set via `wrangler secret put <NAME>`:

| Secret | Description |
|--------|-------------|
| `SENTRY_DSN` | Sentry error tracking |
| `WEBHOOK_SECRET` | Webhook signature verification |

---

## Troubleshooting

### API Unreachable

```bash
# Check if using correct endpoint
echo $SPIRALSAFE_API_BASE

# Test directly
curl https://api.spiralsafe.org/api/health
```

### Coherence Check Failures

```bash
# Run with verbose output
spiralsafe wave analyze ./docs --verbose

# Check specific thresholds
spiralsafe wave thresholds
```

### AWI Permission Denied

```bash
# Check current grant
echo $SPIRALSAFE_AWI_GRANT

# Request new grant with appropriate level
spiralsafe awi request --intent "..." --level 3
```

---

## Contributing

1. Fork the repository
2. Create feature branch
3. Ensure `spiralsafe wave analyze .` passes
4. Create PR with `H&&S:WAVE` marker

---

*H&&S: Coherence engine infrastructure*
