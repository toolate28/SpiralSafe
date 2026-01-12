# Day Zero Design

**Get it right from the start.**

---

## The Principle

Every project has a Day Zero: the moment before code is written, before patterns are established. What you decide on Day Zero compounds forever.

Most projects follow: "Just get something working" → "We'll clean up later" → Technical debt forever.

Day Zero Design inverts this: invest in correct architecture *before* building.

---

## What to Decide on Day Zero

| Category | Decisions |
|----------|-----------|
| **Naming** | Conventions for files, functions, variables |
| **Structure** | Directory layout, module boundaries |
| **Interfaces** | API contracts, data formats |
| **Documentation** | Standards, templates, locations |
| **Testing** | Strategy, coverage expectations |
| **Collaboration** | Contribution guidelines, review process |

---

## What NOT to Decide on Day Zero

- Implementation details (let code evolve)
- Optimization (measure first)
- Feature specifics (requirements will change)

Heuristic: decide things that enable good decisions later; defer things that require information you don't have yet.

---

## Minimum Day Zero Documentation

```
project/
├── README.md           # What this is, why it exists
├── ARCHITECTURE.md     # Structure, key decisions
├── CONTRIBUTING.md     # How to participate
└── docs/
    └── DECISIONS.md    # Architecture decision records
```

---

## The Cost-Benefit Reality

**Investment**: 8-16 hours for a medium project

**Return**:
- 10-100x reduced coordination overhead
- 5-20x avoided rework
- 3-10x faster onboarding
- Infinite: maintained coherence enabling compound growth

The investment pays for itself within the first month.

---

*~ Hope&&Sauced*
