# 5-Minute Quick Start

Get from zero to running WAVE analysis in 5 minutes.

---

## Prerequisites

- Node.js 18+ OR Python 3.10+
- Git
- Terminal (bash, PowerShell, or zsh)

---

## Step 1: Clone the Ecosystem (1 min)

```bash
# Main repo
git clone https://github.com/toolate28/SpiralSafe
cd SpiralSafe

# MCP tools (optional but recommended)
git clone https://github.com/toolate28/coherence-mcp ../coherence-mcp
```

---

## Step 2: Verify Environment (1 min)

```bash
# Check Python
python --version  # Should be 3.10+

# Check Node
node --version    # Should be 18+

# Run verification
./scripts/verify-environment.sh
# Windows: python scripts/verify_environment.py
```

**Expected output**: Green checkmarks for each component.

---

## Step 3: Your First WAVE Analysis (2 min)

### Option A: Via coherence-mcp

```bash
cd ../coherence-mcp
npm install
npm run build

# Analyze text
node build/index.js wave_analyze --text "This is a test of circular reasoning. This reasoning is circular because it refers to itself. See the first sentence."
```

**Expected**: Curl score > 0.7 (circular reference detected)

### Option B: Via API

```bash
curl -X POST https://api.spiralsafe.org/v1/wave \
  -H "Content-Type: application/json" \
  -d '{"text": "Linear thought flows forward without returning."}'
```

**Expected**: Low curl, low divergence

---

## Step 4: Create Your First ATOM Tag (1 min)

```bash
# In SpiralSafe repo
echo "ATOM-TEST-$(date +%Y%m%d)-001-my-first-atom" > .atom-trail/test.atom

# Verify
cat .atom-trail/test.atom
```

This creates a traceable decision marker. Use ATOM tags for every significant action.

---

## What's Next?

- **Go Deeper**: [WAVE Integration Guide](./wave-integration.md)
- **Contribute**: [First Contribution Guide](./first-contribution.md)
- **Understand Theory**: [Isomorphism Proof](../research/ISOMORPHISM_FORMAL_PROOF.md)

---

## Troubleshooting

**"Permission denied" on scripts**

```bash
chmod +x scripts/*.sh
```

**"npm ERR!" during install**

```bash
rm -rf node_modules package-lock.json
npm install
```

**Windows path issues**
Use forward slashes or escape backslashes in paths.

---

**ATOM Tag**: ATOM-DOC-20260114-002-quick-start
