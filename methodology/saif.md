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

*~ Hope&&Sauced*
