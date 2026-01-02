# Secrets Management Guide

## Overview

This guide explains how to handle secrets, credentials, and sensitive data in the SpiralSafe repository following security best practices.

## The Golden Rule

**NEVER commit secrets to the repository.**

## What Counts as a Secret?

- API keys and tokens
- Passwords and passphrases
- Private keys and certificates
- Database connection strings with credentials
- OAuth client secrets
- Webhook secrets
- Service account credentials
- Encryption keys
- Session tokens
- Any data marked as confidential

## Detection Patterns

The repository automatically scans for these patterns:

```regex
# API Keys
(api[_-]?key|apikey)[\s]*[=:]\s*['\"]?[A-Za-z0-9_-]{20,}['\"]?

# AWS Keys
(aws[_-]?access[_-]?key[_-]?id|aws[_-]?secret[_-]?access[_-]?key)[\s]*[=:]
AKIA[0-9A-Z]{16}

# Generic Secrets
(secret|password|passwd|pwd|token)[\s]*[=:]\s*['\"]?[^\s'\",;]+['\"]?

# Private Keys
-----BEGIN[\s\w]*PRIVATE KEY-----

# GitHub Token
ghp_[A-Za-z0-9]{36}
ghs_[A-Za-z0-9]{36}

# Connection Strings
(mongodb|mysql|postgres|postgresql)://[^:]+:[^@]+@
```

## Safe Alternatives

### 1. Environment Variables

**For local development:**
```bash
# .env.example (commit this)
API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# .env (DO NOT commit - in .gitignore)
API_KEY=actual_secret_key_xyz123
DATABASE_URL=postgresql://realuser:realpass@prod.example.com:5432/proddb
```

**In code:**
```bash
# Shell script
API_KEY="${API_KEY:-}"
if [ -z "$API_KEY" ]; then
  echo "ERROR: API_KEY not set" >&2
  exit 1
fi
```

```powershell
# PowerShell
$ApiKey = $env:API_KEY
if (-not $ApiKey) {
    Write-Error "API_KEY not set"
    exit 1
}
```

### 2. GitHub Secrets

**For CI/CD workflows:**

1. Go to: Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add your secrets

**Usage in workflows:**
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          # Secrets available as environment variables
          ./deploy.sh
```

### 3. Configuration Files

**For structured configuration:**

```yaml
# config.example.yml (commit this)
api:
  endpoint: https://api.example.com
  key: ${API_KEY}  # Environment variable reference
  
database:
  host: ${DB_HOST}
  port: 5432
  name: ${DB_NAME}
  
features:
  debug_mode: false
  rate_limit: 100
```

Load with environment variable substitution:
```bash
envsubst < config.example.yml > config.yml
```

## Accidentally Committed a Secret?

### Immediate Actions:

1. **Revoke the secret immediately**
   - Rotate API keys
   - Change passwords
   - Regenerate tokens

2. **Remove from git history**
   ```bash
   # For recent commits (not pushed)
   git reset --soft HEAD~1
   git restore --staged <file>
   
   # For pushed commits - requires force push
   # Contact repository admin - this affects all contributors
   ```

3. **Use git-filter-repo or BFG Repo-Cleaner**
   ```bash
   # Install git-filter-repo
   pip install git-filter-repo
   
   # Remove file from entire history
   git filter-repo --path <file> --invert-paths
   
   # Force push (coordinate with team!)
   git push origin --force --all
   ```

4. **Notify security team**
   - Document what was exposed
   - How long it was exposed
   - Who had access
   - What has been done to remediate

### Prevention:

Add to `.gitignore`:
```
# Secrets and credentials
.env
.env.local
.env.*.local
*secret*
*credential*
*.key
*.pem
*.p12
*.pfx
config.yml
config.json
!config.example.*
```

## Log Redaction

Always redact logs before sharing:

```bash
# Use the redaction script
./scripts/redact-log.sh input.log > output.log

# Manual patterns to remove
sed -E 's/(password|api[_-]?key|token|secret)=\S+/\1=REDACTED/gi' input.log
```

## Testing with Secrets

### Local Testing
```bash
# Load from .env file
source .env
./run-tests.sh
```

### CI/CD Testing
```yaml
# Use test/mock credentials
env:
  API_KEY: "test_key_not_real"
  DATABASE_URL: "postgresql://testuser:testpass@localhost/testdb"
```

### Test Files
```bash
# tests/fixtures/test-config.yml
api:
  endpoint: https://api.test.example.com
  key: "test_key_12345"  # Clearly marked as test data
```

## Audit and Compliance

### Regular Scans

Run automated scans:
```bash
# Manual check
git grep -iE "(password|secret|api[_-]?key|token)[\s]*[=:]" | grep -v ".github/SECRETS.md"

# Check recent commits
git log -p -10 | grep -iE "(password|secret|api[_-]?key|token)[\s]*[=:]"
```

### Pre-commit Hooks

Install pre-commit hook:
```bash
# .git/hooks/pre-commit
#!/bin/bash
set -e

# Check for secrets
if git diff --cached | grep -iE "(password|secret|api[_-]?key|token)[\s]*[=:]"; then
  echo "ERROR: Potential secret detected!"
  echo "If this is not a secret, add '# nosecret' comment on the line"
  exit 1
fi
```

### Audit Log

Track secret usage:
```jsonl
{"timestamp":"2026-01-02T10:00:00Z","action":"secret_accessed","secret_name":"API_KEY","user":"deploy_bot","purpose":"production_deployment"}
{"timestamp":"2026-01-02T11:00:00Z","action":"secret_rotated","secret_name":"DATABASE_PASSWORD","user":"admin","reason":"scheduled_rotation"}
```

## Secret Rotation Schedule

| Secret Type | Rotation Frequency | Owner |
|-------------|-------------------|-------|
| API Keys | 90 days | DevOps team |
| Database passwords | 60 days | Database admin |
| Service account credentials | 30 days | Security team |
| Deployment tokens | 90 days | CI/CD admin |
| Webhook secrets | 180 days | Integration owner |

## GitHub Actions Specific

### Using Secrets in Workflows
```yaml
name: Deploy
on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # Environment protection rules
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Deploy with secrets
        env:
          # Never log these
          API_KEY: ${{ secrets.API_KEY }}
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        run: |
          # DO NOT echo secrets
          # DO NOT include in error messages
          ./deploy.sh
```

### Masking Secrets in Logs
```yaml
- name: Use secret safely
  run: |
    # This will be masked in logs
    echo "::add-mask::${{ secrets.API_KEY }}"
    
    # Now you can use it (still don't echo it directly)
    API_KEY="${{ secrets.API_KEY }}"
```

## Emergency Procedures

### If secrets are exposed in a public PR:

1. **Close PR immediately**
2. **Revoke all exposed secrets**
3. **Create incident report**
4. **Clean git history**
5. **Review access logs**
6. **Update security procedures**

### Contact Information

- Security issues: security@safespiral.org
- Repository admin: @toolate28
- Emergency: [Define emergency contact procedure]

## Resources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [git-filter-repo](https://github.com/newren/git-filter-repo)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)

---

**ATOM:** ATOM-DOC-20260102-003-secrets-management-guide
**Last Updated:** 2026-01-02
**Owner:** Security Team / @toolate28
