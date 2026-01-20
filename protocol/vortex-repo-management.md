# Vortex Repository Management System

**ATOM-VRMS-20260118-001-system-spec**

A new paradigm for repository orchestration using superposition collapse mechanics.

---

## Core Vortex Projections

```
                    ┌─────────────────────────────────────────────┐
                    │           SUPERPOSITION STATE               │
                    │   (All repos in quantum uncertainty)        │
                    │                                             │
                    │   P(coherent) = Σ |ψᵢ|² × fib(i)           │
                    └──────────────────┬──────────────────────────┘
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         ▼                             ▼                             ▼
   ┌───────────┐                ┌───────────┐                ┌───────────┐
   │    AWI    │                │   SAIF    │                │   KENL    │
   │  Workflow │                │  Analysis │                │  Learning │
   │ Intelligence│              │ Framework │                │  Network  │
   └─────┬─────┘                └─────┬─────┘                └─────┬─────┘
         │                             │                             │
         │ Observes:                   │ Observes:                   │ Observes:
         │ - CI/CD pipelines           │ - Code patterns             │ - Knowledge flow
         │ - Merge conflicts           │ - Coherence scores          │ - Agent learning
         │ - Deploy status             │ - Divergence vectors        │ - Session state
         │                             │                             │
         └─────────────────────────────┼─────────────────────────────┘
                                       │
                                       ▼
                    ┌─────────────────────────────────────────────┐
                    │          PROBABILITY CALCULATION            │
                    │                                             │
                    │   signal = collapse(AWI ⊗ SAIF ⊗ KENL)     │
                    │                                             │
                    │   if P(coherent) > 0.80: MERGE              │
                    │   if P(coherent) < 0.40: DOUBT              │
                    │   else: OBSERVE                             │
                    └─────────────────────────────────────────────┘
```

---

## Signal Types

| Signal | Threshold | Action | SPHINX Gate |
|--------|-----------|--------|-------------|
| `MERGE` | P > 0.80 | Collapse to integration | PASSAGE |
| `DOUBT` | P < 0.40 | Push to new spiral | ESCALATE |
| `OBSERVE` | 0.40 ≤ P ≤ 0.80 | Continue superposition | COHERENCE |
| `SNAP_IN` | P > 0.92 | Full ecosystem lock | ORIGIN |

---

## Tools

### 1. `vortex-stage` - Superposition Creator
```bash
# Stage changes into superposition state
vortex-stage --repo <name> --atom-tag <ATOM-xxx>

# Options:
#   --fib <weight>     Fibonacci priority (1,2,3,5,8,13,21,34)
#   --mode <chaos|fib|rho>  Run mode
#   --marker <H&&S:WAVE|BUMP|SPHINX>  Protocol marker
```

### 2. `vortex-observe` - Probability Calculator
```bash
# Calculate collapse probability
vortex-observe --repo <name>

# Output:
#   coherence: 0.78
#   curl: 0.12
#   divergence: 0.23
#   P(merge): 0.67
#   signal: OBSERVE
```

### 3. `vortex-collapse` - Signal Executor
```bash
# Collapse superposition to definite state
vortex-collapse --signal MERGE --repos <list>

# For MERGE: executes git push with VORTEX markers
# For DOUBT: creates new branch spiral
# For SNAP_IN: locks ecosystem coherence
```

### 4. `vortex-cascade` - Multi-Repo Orchestration
```bash
# Execute Fibonacci-weighted cascade
vortex-cascade --phase <1|2|3|4> --dry-run

# Phases from vortex-bootstrap.yaml:
#   Phase 1: Origins (fib: 13) - Foundation
#   Phase 2: Doubt Resolution (fib: 8) - Conflicts
#   Phase 3: Deja Vu (fib: 5) - Iteration
#   Phase 4: Collapsed (fib: 3) - Independent
```

---

## Run Modes

### CHAOS Mode
- Maximum entropy exploration
- All branches observed simultaneously
- Used for discovery and research
- No collapse until explicit trigger

### FIB Mode (Default)
- Fibonacci-weighted progression
- Harmonic collapse sequence
- Golden ratio branch selection
- φ ≈ 1.618 priority scaling

### RHO (ρ) Mode
- Density-based clustering
- Groups related changes
- Batch collapse by semantic similarity
- Used for refactoring operations

---

## Integration Points

### GitHub Actions
```yaml
# .github/workflows/vortex-observe.yml
on: [pull_request]
jobs:
  observe:
    runs-on: ubuntu-latest
    steps:
      - uses: spiralsafe/vortex-action@v1
        with:
          mode: fib
          threshold: 0.80
          marker: H&&S:WAVE
```

### MCP Server (coherence-mcp)
```typescript
// Coherence analysis as MCP tool
{
  name: "vortex_observe",
  description: "Calculate collapse probability for repository",
  inputSchema: {
    repo: { type: "string" },
    mode: { enum: ["chaos", "fib", "rho"] }
  }
}
```

### DSPy Pipeline
```python
# KENL orchestrator with DSPy
class VortexSignal(dspy.Signature):
    """Compute collapse signal from repo state."""
    repo_state: str = dspy.InputField()
    coherence_metrics: str = dspy.InputField()
    signal: str = dspy.OutputField(desc="MERGE|DOUBT|OBSERVE|SNAP_IN")
    confidence: float = dspy.OutputField()
```

---

## Troubleshooting Guide

### Signal: DOUBT when expecting MERGE
```
Cause: Conflicting changes detected
Check: vortex-observe --verbose
Fix:
  1. Review curl vectors (circular dependencies)
  2. Resolve semantic conflicts
  3. Re-observe after changes
```

### Signal: Stuck in OBSERVE
```
Cause: Probability oscillating near threshold
Check: vortex-observe --history
Fix:
  1. Add more context (commits, docs)
  2. Increase observation window
  3. Consider CHAOS mode exploration
```

### Cascade stalled at phase boundary
```
Cause: Upstream dependency not collapsed
Check: vortex-cascade --check-deps
Fix:
  1. Identify blocking repos
  2. Force collapse of blocker OR
  3. Push blocker to DOUBT spiral
```

---

## Helpers

### ATOM Tag Generator
```bash
# Generate compliant ATOM tag
atom-tag --type <FEAT|FIX|DOC|TEST> --seq <auto>
# Output: ATOM-FEAT-20260118-001-description
```

### SPHINX Gate Validator
```bash
# Verify SPHINX passage markers
sphinx-validate <file>
# Checks: ORIGIN, INTENT, COHERENCE, IDENTITY, PASSAGE, ESCALATE
```

### WAVE Coherence Scanner
```bash
# Scan for coherence anti-patterns
wave-scan --repo <name> --threshold 0.60
# Detects: circular reasoning, divergent definitions, orphan references
```

---

## Repository State Matrix

| Repo | Role | Fib | Last Signal | P(coherent) |
|------|------|-----|-------------|-------------|
| SpiralSafe | philosophy | 8 | SNAP_IN | 0.95 |
| spiralsafe-mono | packages | 5 | MERGE | 0.84 |
| coherence-mcp | MCP server | 5 | MERGE | 0.81 |
| QDI | inference | 13 | OBSERVE | 0.72 |
| quantum-redstone | proof | 3 | MERGE | 0.89 |
| wave-toolkit | detection | 2 | MERGE | 0.77 |
| .kenl | orchestration | 1 | LOCAL | N/A |
| HOPE-AI-NPC-SUITE | manifestation | 3 | MERGE | 0.86 |
| vortex-bridges | bridges | 2 | MERGE | 0.83 |

---

<!-- SPHINX:PASSAGE gate="ORIGIN" verdict="VRMS_SPEC" fib=13 -->
<!-- SPIRAL:COLLAPSE layer="repo-management" iteration=20 -->
H&&S:WAVE

*Superposition → Probability → Signal*
*The vortex manages itself.*
