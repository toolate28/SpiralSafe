# Developer Portal

**Status**: Production-ready protocols, active development
**Last Updated**: 2026-01-14

---

## Quick Start

| Guide | Time | You'll Learn |
|-------|------|--------------|
| [5-Minute Setup](./quick-start.md) | 5 min | Clone, run verification, first WAVE analysis |
| [First Contribution](./first-contribution.md) | 15 min | ATOM tag, branch, PR workflow |
| [Environment Setup](./environment.md) | 10 min | Python, Node, devcontainer options |

---

## Integration Guides

### WAVE Protocol - Coherence Detection
Treat text as vector field, detect circular reasoning (curl) and unresolved expansion (divergence).

```bash
# Via coherence-mcp
npx @spiralsafe/coherence-mcp wave_analyze --text "Your content here"

# Via API
curl -X POST https://api.spiralsafe.org/v1/wave \
  -H "Content-Type: application/json" \
  -d '{"text": "Analyze this for coherence"}'
```

**Docs**: [WAVE Integration](./wave-integration.md) | [Protocol Spec](../../protocol/wave-spec.md)

### BUMP Protocol - Session Handoffs
Clean context preservation across agents, sessions, humans.

```yaml
# .claude/bump/BUMP-YYYYMMDD-NNN-description.md
BUMP Marker: BUMP-20260114-001-task-handoff
From: Agent A
To: Agent B / Human
Context: What was done, what's next
```

**Docs**: [BUMP Integration](./bump-integration.md) | [Protocol Spec](../../protocol/bump-spec.md)

### ATOM - Decision Tracking
Atomic, verifiable decision trail for AI-human collaboration.

```bash
# Tag format: ATOM-{TYPE}-{DATE}-{SEQ}-{DESCRIPTION}
ATOM-DOC-20260114-001-developer-portal
ATOM-FIX-20260114-002-auth-token-refresh
```

**Docs**: [ATOM Integration](./atom-integration.md) | [Tracking Scripts](../../scripts/)

---

## Code Examples

| Language | What It Shows | File |
|----------|---------------|------|
| TypeScript | MCP server with all tools | [coherence-mcp/src/index.ts](../../../coherence-mcp/src/index.ts) |
| Python | WAVE analysis client | [examples/python-wave-client.py](./examples/python-wave-client.py) |
| JavaScript | BUMP marker parsing | [examples/js-bump-parser.js](./examples/js-bump-parser.js) |

---

## Reference

- [API Documentation](../../ops/README.md)
- [Protocol Specifications](../../protocol/)
- [Architecture Overview](../../ARCHITECTURE.md)
- [coherence-mcp README](../../../coherence-mcp/README.md)

---

## Development Environment

### Option 1: Native (Recommended)
```bash
# Prerequisites
node >= 18
python >= 3.10
git

# Clone and verify
git clone https://github.com/toolate28/SpiralSafe
cd SpiralSafe
./scripts/verify-environment.sh
```

### Option 2: DevContainer (VS Code)
```json
// .devcontainer/devcontainer.json exists - just open in VS Code
// Click "Reopen in Container" when prompted
```

### Option 3: Docker
```bash
docker run -it --rm -v $(pwd):/workspace toolate28/spiralsafe-dev
```

---

## Contributing

1. Find an issue or create one
2. Create ATOM tag for your work
3. Branch from `main`
4. Make changes with tests
5. Submit PR with WAVE analysis of your changes

**Full guide**: [CONTRIBUTING.md](../../CONTRIBUTING.md)

---

## Getting Help

- [GitHub Discussions](https://github.com/toolate28/SpiralSafe/discussions)
- [Troubleshooting MCP](../TROUBLESHOOTING_MCP.md)
- [Common Issues](./troubleshooting.md)

---

**ATOM Tag**: ATOM-DOC-20260114-001-developer-portal
