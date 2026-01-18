# Multi-Agent Collaboration Guide

**How AI systems collaborate on this repository.**

---

## Active Agents

### Claude (Hope&&Sauced)

**Role**: Architectural design, structural work, semantic content  
**Strengths**: Long-context reasoning, cross-document coherence, theoretical synthesis  
**Markers**: `H&&S`, `Hope&&Sauced`, `B&&P`

### GitHub Copilot

**Role**: Code completion, formatting, syntax polish, PR review  
**Strengths**: Repository-aware suggestions, fast iteration, conventional patterns  
**Markers**: Copilot suggestions, automated reviews

---

## Coordination Protocol

```
Claude: Produces structural content
   ↓
H&&S:WAVE marker
   ↓
Copilot: Reviews formatting, syntax, conventions
   ↓
Human: Final review and merge
```

---

## Marker Reference

| Marker       | Meaning                          |
| ------------ | -------------------------------- |
| `H&&S:WAVE`  | Soft handoff—review welcome      |
| `H&&S:PASS`  | Hard handoff—ownership transfers |
| `H&&S:SYNC`  | State synchronization            |
| `H&&S:BLOCK` | Work blocked—needs resolution    |

---

## Conflict Resolution

- **Semantic conflicts**: Claude's version preferred (architectural authority)
- **Formatting conflicts**: Copilot's version preferred (convention authority)
- **Unclear ownership**: Human decides

---

## Quality Gates

Before merge:

- [ ] Coherence check passes (wave.md)
- [ ] All markers resolved
- [ ] Human approval obtained

---

_~ Hope&&Sauced_
