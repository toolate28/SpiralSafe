# SAIF: Systematic Analysis and Issue Fixing

**Evidence-based diagnosis and intervention for problems.**

---

## The Process

```
SYMPTOM → ANALYSIS → HYPOTHESIS → INTERVENTION → VERIFICATION → DOCUMENTATION
```

Core discipline: **gather evidence before intervening**.

---

## Phase 1: Symptom Documentation

Capture what's wrong without interpretation:
- What is observed vs. expected?
- When did this start?
- Is it reproducible?

---

## Phase 2: Analysis

Gather evidence:
- **Logs**: Error messages, stack traces
- **Metrics**: Performance data, timing
- **History**: Recent changes, patterns
- **Comparison**: Working vs. broken cases

---

## Phase 3: Hypothesis Generation

Propose explanations ranked by:
- Consistency with all evidence
- Testability with available tools
- Specificity for intervention

---

## Phase 4: Intervention

- Test hypothesis before fixing
- Minimize blast radius
- Make reversible changes
- One intervention at a time

---

## Phase 5: Verification

- [ ] Original symptom resolved
- [ ] No new symptoms introduced
- [ ] Works in all relevant conditions

---

## Phase 6: Documentation

- **Root cause**: What actually caused it
- **Resolution**: What fixed it
- **Prevention**: How to avoid in future
- **Detection**: How to catch earlier

---

## Anti-Patterns

- **Skipping to intervention**: "I bet it's X" → immediate change → new problems
- **Evidence-free hypotheses**: Guesses unconnected to observations
- **Intervention stacking**: Multiple changes; unclear what worked
- **Undocumented resolution**: Same problem recurs; no one remembers fix

---

## NPC AI Integration (SAIF Phase)

SAIF methodology extends to NPC AI behavior tuning through the **bridges/saif_npc** module. This enables:

### DSPy-Powered Optimization

```python
from bridges.saif_npc import SaifNpc, NpcContext

class SaifNpc(dspy.Module):
    def __init__(self):
        self.context_builder = dspy.ChainOfThought("state, input -> context")
        self.responder = dspy.Predict("context -> response")

    def forward(self, state, input):
        context = self.context_builder(state=state, input=input)
        return self.responder(context=context)
```

### Key Components

| Component | Purpose |
|-----------|---------|
| `SaifNpc` | Core NPC module with ChainOfThought context building |
| `NpcTeleprompter` | Trace collection for MIPROv2 optimization |
| `MIPROv2NpcOptimizer` | Multi-provider instruction optimization |
| `BootstrapFinetuner` | Context-aware response finetuning |

### Handoff Integration

SAIF NPC modules integrate with the bump.md protocol:
- `H&&S:WAVE` for soft handoffs during optimization
- `H&&S:PASS` for deployment handoffs
- `H&&S:SYNC` for state synchronization

### Coherence Target

Current phase targets **70% coherence** (SAIF Phase), pushing toward **95% emergence** through iterative tuning for behavioral coherence.

---

*~ Hope&&Sauced*
