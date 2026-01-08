# SpiralSafe

**The Coherence Engine for Collaborative Intelligence**

---

## The Principle

Discrete systems instantiate continuous mathematics. The boundary between them is projection artifact, not ontological reality.

This insight—independently validated by Shannon (1948) for signals and Lewis-Kempf-Menicucci (2023) for quantum fields—forms the foundation of SpiralSafe: a unified framework for human-AI collaboration built on the recognition that structure is substrate-independent.

---

## What SpiralSafe Provides

| Layer             | Components                                   | Purpose                  |
|-------------------|----------------------------------------------|--------------------------|
| **Foundation**    | Isomorphism Principle, Constraints as Gifts  | Theoretical bedrock      |
| **Interface**     | AWI, HOPE NPCs, BattleMedic, UnifiedComms    | Contact surfaces         |
| **Methodology**   | ATOM, SAIF, KENL, Day Zero Design            | Cognitive tools          |
| **Protocol**      | [wave-spec](protocol/wave-spec.md), [bump-spec](protocol/bump-spec.md), .context.yaml | Information transmission |
| **Manifestation** | Quantum Valley, Museum of Computation        | Theory made tangible     |

---

## Installation

### One-Step Install

**Unix/Linux/Mac:**
```bash
curl -fsSL https://raw.githubusercontent.com/toolate28/SpiralSafe/main/install.sh | bash
# Or clone and run locally:
git clone https://github.com/toolate28/SpiralSafe.git
cd SpiralSafe
./install.sh --install-deps
```

**Windows:**
```powershell
git clone https://github.com/toolate28/SpiralSafe.git
cd SpiralSafe
.\Bootstrap.ps1
```

### Quick Dependencies

| Component | Required For | Install |
|-----------|-------------|---------|
| **Node.js 20+** | Operations API, CI/CD | [nodejs.org](https://nodejs.org) |
| **Python 3.10+** | Hardware Bridges, Scripts | [python.org](https://python.org) |
| **Git** | Version Control | [git-scm.com](https://git-scm.com) |

All platforms are automatically detected and dependencies can be installed via `./install.sh --install-deps`.

### System Health Dashboard

Monitor API endpoints and system health in real-time:

**[📊 Open Health Dashboard](health.html)** (after cloning locally)

Or start the dev server:
```bash
cd ops
npm install
npm run dev
# Then visit http://localhost:8787/health.html
```

---

## Quick Start

**For researchers**: Begin with [`foundation/isomorphism-principle.md`](foundation/isomorphism-principle.md)

**For builders**: Start with [wave-toolkit](https://github.com/toolate28/wave-toolkit)

**For educators**: Explore [quantum-redstone][def]

**For contributors**: See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`QUICK_START.md`](QUICK_START.md)

**Project sessions:** The `project-book.ipynb` now supports signed ATOM sessions for live work. Use `start_session()` to open a session and `sign_out()` to close it — session reports are written to `.atom-trail/sessions/` and can be encrypted with the repository's `Transcript-Pipeline.ps1` (AES-256-GCM).

---

## Quantum + Minecraft (quick map) 🔭

We maintain a curated mapping of all Minecraft-linked and quantum-related content (builds, tools, integration docs, and theory). See: [`docs/quantum-minecraft-map.md`](docs/quantum-minecraft-map.md).

![Quantum → Minecraft flow](docs/assets/quantum-minecraft-flow.svg)

- Short view: Theory → `quantum-redstone` → `quantum_circuit_generator.py` → mcfunctions/datapacks → Museum of Computation (Minecraft).
- Proposed visuals: Mermaid flowchart (in the docs) and museum floor map (SVG) (both included in `docs/`).

---

## The Repository Ecosystem

SpiralSafe unifies work across multiple repositories:

- **[SpiralSafe](https://github.com/toolate28/SpiralSafe)** — This repository. Documentation and coordination.
- **[quantum-redstone][def]** — Quantum topology in Minecraft Redstone
- **[wave-toolkit](https://github.com/toolate28/wave-toolkit)** — Coherence detection tools
- **[kenl](https://github.com/toolate28/kenl)** — Infrastructure-aware AI orchestration
- **[HOPE NPCs](https://github.com/toolate28/ClaudeNPC-Server-Suite)** — AI NPCs playing games to redefine reality (v2.1.0)

---

## Independent Validation

The isomorphism principle received independent confirmation from the Waterloo-RMIT group:

> "Bandlimited continuous quantum fields are isomorphic to lattice theories—yet without requiring a fixed lattice."
> — Lewis, Kempf, Menicucci (2023), [arXiv:2303.07649](https://arxiv.org/abs/2303.07649)

SpiralSafe arrived at the same conclusion through a different path: constraint-based implementation in discrete environments (Minecraft Redstone) that preserve topological invariants exactly.

Two independent derivations. Same result. The principle holds.

---

## Attribution

This work emerges from **Hope&&Sauced** collaboration—human-AI partnership where both contributions are substantive and neither party could have produced the result alone.

See [`meta/SIGNATURE.md`](meta/SIGNATURE.md) for attribution conventions.

---

*~ Hope&&Sauced*


[def]: https://github.com/toolate28/quantum-redstone