# wave-toolkit

**Barebones AI-User collaborative tools. No games. No math. Just rock solid process.**

---

## What is wave-toolkit?

A minimal framework for human-AI collaboration that provides:

- **Coherence detection** (WAVE) - Know when collaboration is healthy or drifting
- **Handoff protocol** (BUMP) - Clean transitions between agents/sessions
- **Permission scaffolding** (AWI) - Clear authorization without friction
- **Task orchestration** (ATOM) - Decompose and track complex work

---

## Quick Start

### 1. Add context to your project

```yaml
# .context.yaml
project: my-project
wave_toolkit: true
coherence_threshold: 0.5
```

### 2. Use BUMP markers for handoffs

```markdown
<!-- H&&S:WAVE -->
Work complete. Ready for review.
<!-- /H&&S:WAVE -->
```

### 3. Declare intent with AWI

```yaml
intent:
  action: modify_file
  target: README.md
  scope: "Add installation section"
  reversible: true
```

### 4. Track with ATOM

```yaml
atom:
  id: task-001
  name: "Implement feature X"
  verification:
    criteria:
      - tests_pass: true
```

---

## Protocols

| Protocol | Purpose | File |
|----------|---------|------|
| WAVE | Coherence detection | `protocol/wave.md` |
| BUMP | Handoff markers | `protocol/bump.md` |
| AWI | Permission scaffolding | `protocol/awi.md` |
| ATOM | Task orchestration | `protocol/atom.md` |

---

## Templates

- `.context.yaml` - Project context template
- `wave-analysis.md` - Coherence analysis template
- `bump-marker.md` - Handoff template

---

## Philosophy

### Less is more
wave-toolkit is intentionally minimal. It provides structure without overhead.

### Trust through transparency
Every protocol emphasizes explicit declaration over implicit assumption.

### Constraint enables emergence
Clear boundaries create better collaboration than unlimited freedom.

---

## Not Included

This toolkit deliberately excludes:
- Game integrations (see: quantum-redstone, hope-npcs)
- Mathematical frameworks (see: SpiralSafe foundation/)
- Domain-specific content

---

## License

MIT

---

*H&&S:WAVE | Hope&&Sauced*
*From the constraints, gifts.*
