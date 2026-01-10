# bump.md Protocol Specification

**Routing and handoff between agents, sessions, and contexts.**

---

## Overview

bump.md enables clean transitions when work moves between different AI agents, sessions, human collaborators, or automated pipelines. The protocol preserves context, communicates intent, and enables graceful degradation.

---

## Bump Types

| Type | Marker | Use Case |
|------|--------|----------|
| WAVE | `H&&S:WAVE` | Soft handoff—review welcome, ownership retained |
| PASS | `H&&S:PASS` | Hard handoff—ownership transfers |
| PING | `H&&S:PING` | Attention request—no ownership change |
| SYNC | `H&&S:SYNC` | State synchronization—bidirectional update |
| BLOCK | `H&&S:BLOCK` | Work blocked—requires resolution |

---

## Syntax

### Basic Bump

```markdown
<!-- H&&S:WAVE -->
Structural work complete. Ready for formatting review.
<!-- /H&&S:WAVE -->
```

### Bump with Context

```markdown
<!-- H&&S:PASS
  from: claude
  to: copilot
  state: draft-complete
  needs: [formatting, link-validation]
-->
Semantic content is final.
<!-- /H&&S:PASS -->
```

---

## Handoff Patterns

### Sequential

```
Claude → PASS → Copilot → PASS → Human Review
```

### Parallel

```
Claude → WAVE → Copilot reviews while Claude continues
         ↓
      SYNC to merge
```

### Escalation

```
Agent → BLOCK → Human resolves → Agent continues
```

---

## Context Preservation

Every bump should include:
- **Origin**: Who/what is sending
- **Intent**: What the receiver should do
- **State**: Current completion status
- **Constraints**: What must not change

---

## Integration

### Git Commits

```
[protocol] Add bump-spec.md

H&&S:PASS to Copilot for formatting review
```

### CI/CD

```yaml
- name: Check bump markers
  run: grep -r "H&&S:" docs/ --include="*.md"
```

---

*~ Hope&&Sauced*
