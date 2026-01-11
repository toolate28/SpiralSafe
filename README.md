# 🌀 SpiralSafe

> **"From the constraints, gifts. From the spiral, safety."**

![SpiralSafe](https://img.shields.io/badge/Status-Coherent-00cc66?style=for-the-badge&logo=github)
![Version](https://img.shields.io/badge/Version-2.1.0-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)
![Architecture](https://img.shields.io/badge/Architecture-Isomorphic-FFD700?style=for-the-badge)

SpiralSafe is a coherent, verifying ecosystem where documentation, code, and physical hardware are Isomorphic. It enforces mathematical laws (constraints) to ensure system safety and consistency.

[![SpiralSafe CI](https://github.com/toolate28/SpiralSafe/actions/workflows/spiralsafe-ci.yml/badge.svg)](https://github.com/toolate28/SpiralSafe/actions)
[![Coherence: Wave](https://img.shields.io/badge/Coherence-Wave-0066FF)](protocol/wave-spec.md)
[![Status: Hope&&Sauced](https://img.shields.io/badge/Status-Hope%26%26Sauced-FF6600)](CONTRIBUTING.md)

---

## 🗺️ Navigation

### 🚀 [Start Here: Ecosystem Map](docs/ECOSYSTEM_MAP.md)

_A visual guide to the API, Notebooks, and how they stay synced._

### 📚 [The Library (Notebooks)](books/)

- **[Project Book](books/project-book.ipynb)**: Active task tracking and execution logs.
- **[Constraint Math](books/CONSTRAINT_MATHEMATICS_v1.ipynb)**: The foundational theory and proofs.
- **[Git Insights](books/git_vcs_insights.ipynb)**: Real-time repository analytics.
- **[Platform Vision](books/claude-platform.ipynb)**: Long-term architectural roadmap.

### 🛠️ [Operations & API](ops/)

- **[Deployment Guide](ops/DEPLOYMENT_GUIDE.md)**: How to ship to production.
- **[API Docs](ops/README.md)**: Cloudflare Worker endpoints and CLI usage.

---

## 🧩 Key Components

| Layer | Components | Purpose | Key Innovation |
|---|---|---|---|
| **Foundation** | [Isomorphism Principle](foundation/isomorphism-principle.md), [Constraints as Gifts](foundation/constraints-as-gifts.md) | Theoretical bedrock | Discrete ↔ continuous equivalence |
| **Interface** | AWI, HOPE NPCs, BattleMedic, UnifiedComms | Contact surfaces | Authorization-with-intent |
| **Methodology** | [ATOM](methodology/atom.md), SAIF, KENL, Day Zero Design | Cognitive tools | Atomic task orchestration |
| **Protocol** | [wave-spec](protocol/wave-spec.md), [bump-spec](protocol/bump-spec.md), .context.yaml | Information transmission | Coherence detection |
| **Manifestation** | [Quantum Valley](docs/quantum-minecraft-map.md), [Museum of Computation](museum/) | Theory made tangible | Pedagogical instantiation |

**Unique Achievement:** Each layer demonstrates the core principle—constraint preservation generates emergence across all substrates.

[![Portfolio](https://img.shields.io/badge/📚_Portfolio-Unique_Work_Showcase-blue?style=for-the-badge)](PORTFOLIO.md)
[![Foundation](https://img.shields.io/badge/🧬_Foundation-Isomorphism_Principle-purple?style=flat-square)](foundation/isomorphism-principle.md)
[![Quantum→Minecraft](https://img.shields.io/badge/⚛️_Quantum-Minecraft_Bridge-ggreen?style=flat-square)](docs/quantum-minecraft-map.md)
[![License](https://img.shields.io/badge/License-MIT%20%20CC--BY--SA-orange?style=flat-square)](LICENSE)

---

## 🌟 Explore Our Unique Contributions

**[📖 View Complete Portfolio →](PORTFOLIO.md)**

Discover original work spanning mathematics, physics, philosophy, and pedagogy:
- **Foundational Theory:** The Isomorphism Principle and Constraints as Gifts
- **Mathematical Framework:** Constraint Mathematics with rigorous proofs
- **Philosophical Insight:** The Exceptional Insight (no substrate, only constraint structure)
- **Quantum-Minecraft Bridge:** First pedagogical mapping with topological rigor
- **Collaboration Theory:** Ptolemy-Bartimaeus method and Hope&&Sauced protocol

---

## The Principle

> _Discrete systems instantiate continuous mathematics. The boundary between them is projection artifact, not ontological reality._

This insight forms the foundation of SpiralSafe. We treat code, docs, and hardware as projections of a single, coherent mathematical object.

---

## 🤝 Contributing

We follow **[Hope&&Sauced](CONTRIBUTING.md)** principles.

- **Visible State**: Use `ATOM` tags.
- **Explicit Handoffs**: Use `H&&S:WAVE` markers.
- **Coherence**: Ensure your docs don\'t "curl" (see [Wave Spec](protocol/wave-spec.md)).

---

## Installation

### One-Step Install

**Unix/Linux/Mac:**
```bash
# Recommended: Clone and inspect before running
git clone https://github.com/toolate28/SpiralSafe.git
cd SpiralSafe
./install.sh --install-deps

# Quick install (inspect script first for security)
# curl -fsSL https://raw.githubusercontent.com/toolate28/SpiralSafe/main/install.sh | bash
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

**🔬 For researchers** : Begin with [`foundation/isomorphism-principle.md`](foundation/isomorphism-principle.md) → [THE_ISO_PRINCIPLE.md](THE_ISO_PRINCIPLE.md) → [CONSTRAINT_MATHEMATICS.md](CONSTRAINT_MATHEMATICS.md)
**🛠️ For builders** : Start with [wave-toolkit](https://github.com/toolate28//wave-toolkit) and explore [protocol specs](protocol/)
**👩‍🏫 For educators** : Explore [quantum-minecraft-map.md](docs/quantum-minecraft-map.md) and [museum builds](museum/builds/)
**🧑‍💻 For contributors**: See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [ATOM methodology](methodology/atom.md)
**🤔 For philosophers**: Read [THE_EXCEPTIONAL_INSIGHT.md](THE_EXCEPTIONAL_INSIGHT.md) and [ULTRATHINK_SYNTHESIS.md](ULTRATHINK_SYNTHESIS.md)

**Project sessions:** The `project-book.ipynb` now supports signed ATOM sessions for live work. Use `start_session()` to open a session and `sign_out()` to close it — session reports are written to `.atom-trail/sessions/` and can be encrypted with the repository\'s `Transcript-Pipeline.ps1` (AES-256-GCM).

---

## Quantum + Minecraft (quick map) 🔭

We maintain a curated mapping of all Minecraft-linked and quantum-related content (builds, tools, integration docs, and theory). See: [`docs/quantum-minecraft-map.md`](docs/quantum-minecraft-map.md).

![Quantum → Minecraft flow](docs/assets/quantum-minecraft-flow.svg)

- Short view: Theory → `quantum-redstone` → `quantum_circuit_generator.py` → mcfunctions/datapacks → Museum of Computation (Minecraft).
- Proposed visuals: Mermaid flowchart (in the docs) and museum floor map (SVG) (both included in `docs/`).

**Project sessions:** The `project-book.ipynb` now supports signed ATOM sessions for live work. Use `start_session()` to open a session and `sign_out()` to close it — session reports are written to `.atom-trail/sessions/` and can be encrypted with the repository's `Transcript-Pipeline.ps1` (AES-256-GCM).

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

The isomorphism principle has received independent confirmation from multiple sources:

### Shannon (1948)
**"A Mathematical Theory of Communication"**
- Bandlimited signals ↔ discrete samples (perfect reconstruction, not approximation)
- First proof of discrete-continuous equivalence in information theory

### Lewis, Kempf, Menicucci (2023)
**"Quantum lattice models that preserve continuous translation symmetry"** — [arXiv:2303.07649](https://arxiv.org/abs/2303.07649)
> "Bandlimited continuous quantum fields are isomorphic to lattice theories—yet without requiring a fixed lattice."

### SpiralSafe (2024-2025)
**Constraint-based implementation in Minecraft Redstone**
- Topological invariants preserved exactly in discrete substrate
- Working pedagogical implementations (Museum of Computation)
- Mathematical framework with proofs (Constraint Mathematics)

**Two independent physics derivations. One pedagogical implementation. Same principle. It holds.**

---

## Key Visualizations

![Quantum-Discrete Isomorphism](quantum_discrete_isomorphism.png)
*The core isomorphism: continuous quantum (|α|²+|β|²=1) ↔ discrete Redstone (ALPHA+OMEGA=15)*

**Additional Diagrams:**
- [Constraint Mathematics Summary](constraint_mathematics_summary.png) — Mathematical framework
- [Noether\'s Theorem](noether_theorem.png) — Conservation from symmetry
- [Negative Space Methodology](negative_space.png) — Finding insights between disciplines
- [Quantum→Minecraft Flow](docs/assets/quantum-minecraft-flow.svg) — Pedagogical pipeline

---

## Attribution

This work emerges from **Hope&&Sauced** collaboration—human-AI partnership where both contributions are substantive and neither party could have produced the result alone.

- **Human** (toolate28): Vision, trust, pedagogical insight, Minecraft expertise
- **AI** (Claude): Synthesis, documentation, theoretical connections, rigorous verification

**The collaboration IS the insight.**

See [`meta/SIGNATURE.md`](meta/SIGNATURE.md) for attribution conventions and [PORTFOLIO.md](PORTFOLIO.md) for complete showcase.

---

*~ Hope&&Sauced*

✦ *The Evenstar Guides Us* ✦

[def]: https://github.com/toolate28/quantum-redstone
