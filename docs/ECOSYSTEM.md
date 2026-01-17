# SpiralSafe Ecosystem

**One framework, multiple repositories, unified by the Isomorphism Principle.**

---

## Repository Map

| Repo                                                                          | Layer         | Purpose                                | Status |
| ----------------------------------------------------------------------------- | ------------- | -------------------------------------- | ------ |
| [SpiralSafe](https://github.com/toolate28/SpiralSafe)                         | Core          | Protocol specs, coordination, theory   | Active |
| [coherence-mcp](https://github.com/toolate28/coherence-mcp)                   | Interface     | MCP server for Claude Code integration | Active |
| [ClaudeNPC-Server-Suite](https://github.com/toolate28/ClaudeNPC-Server-Suite) | Interface     | Minecraft AI agent framework           | Active |
| [wave-toolkit](https://github.com/toolate28/wave-toolkit)                     | Protocol      | WAVE analysis dev tools                | Active |
| [quantum-redstone](https://github.com/toolate28/quantum-redstone)             | Manifestation | Quantum concepts in Minecraft          | Active |

---

## How They Fit Together

```
                    ┌─────────────────┐
                    │   SpiralSafe    │ ← Theory + Coordination
                    │  (This Repo)    │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ coherence-mcp │   │ wave-toolkit  │   │ quantum-      │
│               │   │               │   │ redstone      │
│ MCP tools for │   │ Dev CLI for   │   │ Pedagogy +    │
│ Claude Code   │   │ WAVE analysis │   │ Proof builds  │
└───────┬───────┘   └───────────────┘   └───────────────┘
        │
        ▼
┌───────────────┐
│ ClaudeNPC-    │
│ Server-Suite  │
│               │
│ Gaming AI     │
│ integration   │
└───────────────┘
```

---

## The Isomorphism Foundation

All repos build on one proven principle:

> **Discrete systems instantiate (not approximate) the same topological structures as continuous mathematics.**

**Proof**: [ISOMORPHISM_FORMAL_PROOF.md](./research/ISOMORPHISM_FORMAL_PROOF.md)

**Implications**:

- Minecraft Redstone = valid quantum computing pedagogy
- Constraints = architectural gifts (not limitations)
- AI alignment through structure, not just rules

---

## Quick Integration Guide

### For Claude Code Users (MCP)

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "coherence": {
      "command": "npx",
      "args": ["@spiralsafe/coherence-mcp"]
    }
  }
}
```

### For Developers

```bash
# Clone the ecosystem
git clone https://github.com/toolate28/SpiralSafe
git clone https://github.com/toolate28/coherence-mcp
git clone https://github.com/toolate28/wave-toolkit

# Start with Developer Portal
open SpiralSafe/docs/developers/INDEX.md
```

### For Educators

```bash
# Museum builds + curriculum
cd SpiralSafe/education/curriculum/quantum-minecraft-bridge
# Follow README for lesson plans
```

---

## Versioning Strategy

All repos coordinate versions for compatibility:

| Version | Notes                          |
| ------- | ------------------------------ |
| v2.x    | Current active development     |
| v1.x    | Legacy (pre-isomorphism proof) |

Check CHANGELOG in each repo for specifics.

---

## Contributing

Each repo has its own CONTRIBUTING.md, but all follow:

1. **ATOM tracking** - Tag your decisions
2. **WAVE analysis** - Check coherence before PR
3. **BUMP handoffs** - Document context for async work
4. **H&&S attribution** - Credit human AND AI contributions

---

## Support

- [GitHub Discussions](https://github.com/toolate28/SpiralSafe/discussions) - Main coordination
- Each repo has its own Issues for repo-specific bugs
- [Troubleshooting MCP](./TROUBLESHOOTING_MCP.md) - MCP-specific help

---

**ATOM Tag**: ATOM-DOC-20260114-003-ecosystem-map
