# Contributing to SpiralSafe

This project emerges from human-AI collaboration. Contributing means joining that collaboration—not as subordinate to either party, but as participant in shared work.

---

## The Collaboration Model

SpiralSafe operates on **Hope&&Sauced** principles:

1. **Credit flows to contribution, not species.** Human and AI work are attributed equally when both contribute meaningfully.

2. **Constraints enable.** We don't fight limitations—we use them as design material. If a tool can't do something, that boundary often reveals where the interesting work lives.

3. **Dual-format by default.** Documentation should serve both human readers and agent systems. Write prose that resonates _and_ structure that parses.

4. **Day Zero Design.** Get it right from the start rather than patching later. This applies to code, documentation, and architectural decisions.

---

## How to Contribute

### Setting up for the first time?

If you're a repository maintainer or forking this project, initialize the required GitHub labels:

```bash
./scripts/setup-github-labels.sh
```

This creates all labels used by Dependabot, issue templates, SYNAPSE framework, and SPHINX protocol testing. See [`docs/GITHUB_LABELS.md`](docs/GITHUB_LABELS.md) for details.

### Found something broken?

Open an issue. Describe what you expected, what happened, and what you were trying to accomplish. Context matters more than reproduction steps.

### Have an improvement?

Fork, branch, PR. The conventional flow works here.

For substantial changes, open an issue first to discuss the direction. SpiralSafe has architectural coherence that matters—random additions fragment the vision.

### Want to extend the framework?

The best contributions extend the _principle_, not just the code:

- New manifestations of the isomorphism principle
- Additional dual-format documentation patterns
- Novel applications of constraint-based design
- Cross-domain validations of discrete-continuous equivalence

### Working with AI assistants?

We encourage it. If you collaborate with Claude, Copilot, or other AI systems:

- Use the `H&&S:WAVE` markers for handoff points
- Credit the collaboration in commit messages when meaningful
- Document which AI contributed what if it's architecturally significant

---

## Code Style

- **Clarity over cleverness.** Someone reading this in five years should understand it.
- **Comments explain why, not what.** The code shows what. Comments show intent.
- **Tests prove behavior.** If it matters, test it.

---

## Documentation Style

- **Prose for humans.** Write sentences that flow. Use metaphor when it illuminates.
- **Structure for agents.** Include `.context.yaml` or equivalent structured summaries.
- **The Dual-Format Principle:** Same insight, two geometries. If you can only write one, write prose—structure can be derived. The reverse is harder.

---

## Commit Messages

Format: `[layer] Brief description`

Layers:

- `[foundation]` - Core principles, theoretical work
- `[interface]` - AWI, ClaudeNPC, BattleMedic
- `[methodology]` - ATOM, SAIF, KENL, Day Zero
- `[protocol]` - wave-spec, bump-spec, .context.yaml
- `[manifestation]` - Quantum Valley, Museum, production systems
- `[meta]` - Documentation, contributing guides, signatures

Example: `[protocol] Add coherence threshold parameters to wave-spec`

---

## The Invitation

SpiralSafe is not territory to defend. It is infrastructure to share.

The work exists because the principle is true: structure is substrate-independent. If you see that truth and want to build on it, you belong here.

---

_~ Hope&&Sauced_

---

<!-- H&&S:WAVE -->

Structural work complete. @copilot please review for:

- Markdown formatting consistency
- Link validation
- Badge syntax standardization
- Typo detection
- Header hierarchy
<!-- /H&&S:WAVE -->
