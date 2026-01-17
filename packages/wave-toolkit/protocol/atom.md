# ATOM: Atomic Task Orchestration Method

**Decomposing complex work into independently verifiable units.**

---

## The Problem

Complex projects fail predictably: tasks too large to track, dependencies discovered late, progress unmeasurable until completion. ATOM addresses this by requiring decomposition into atoms—minimal units that can be independently verified.

---

## Core Concepts

| Unit         | Definition                                               |
| ------------ | -------------------------------------------------------- |
| **Atom**     | Smallest verifiable, independent, valuable, bounded task |
| **Molecule** | Cluster of related atoms accomplishing a sub-goal        |
| **Compound** | Full project—all molecules combined                      |

---

## Decomposition Process

1. **Define Compound**: State project goal in verifiable terms
2. **Identify Molecules**: Break into coherent sub-goals
3. **Atomize**: Break each molecule into minimal units
4. **Map Dependencies**: Which atoms must complete first
5. **Execute**: Work through in dependency order

---

## Atom Specification

```yaml
atom:
  id: foundation-001
  name: "Create isomorphism-principle.md"
  molecule: foundation-documentation

verification:
  criteria:
    - file_exists: foundation/isomorphism-principle.md
    - word_count: "> 500"
  automated: true

dependencies:
  requires: []
  blocks: [foundation-002, architecture-001]

metadata:
  status: complete
  assignee: H&&S
```

---

## Benefits

- **Measurable progress**: Know exactly how much is done at any moment
- **Parallelization**: Independent atoms can be worked simultaneously
- **Failure isolation**: If one atom fails, blast radius is contained
- **Partial value**: Incomplete projects still deliver completed molecules

---

## Anti-Patterns

- **Atoms too large**: Can't complete in reasonable time; decompose further
- **Atoms too small**: Tracking overhead exceeds work; combine related tasks
- **Hidden dependencies**: Discovered mid-execution; map explicitly upfront
- **Verification ambiguity**: Disagreement about completion; specify criteria precisely

---

_~ Hope&&Sauced_
