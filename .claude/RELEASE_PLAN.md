# SpiralSafe Release Plan

## Condense, Clarify, Solidify | 2026-01-10

---

## Overview

Three packages to release:

1. **quantum-redstone** - Quantum computing in Minecraft
2. **ClaudeNPC-Server-Suite** (rebranded as **HOPE NPCs**) - Multi-AI gaming framework
3. **wave-toolkit** - Barebones AI-User collaborative tools

---

## 1. quantum-redstone

### Purpose

Demonstrate the Iso Principle through playable quantum circuits in Minecraft Redstone.

### Core Content

- `QUANTUM_CIRCUITS.md` - Gates, algorithms, visuals
- `QUANTUM_COMPUTER_ARCHITECTURE.md` - Full architecture
- `SPIRALCRAFT_QUANTUM_PLUGIN.md` - Plugin implementation
- Java plugin source (if available)

### Key Claims

- |α|² + |β|² = 1 maps to ALPHA + OMEGA = 15
- 9 quantum gates implemented
- 4 algorithms: Bell state, Teleportation, Grover, QRNG
- SpiralSafe API integration

### NEW: F_p² Validation

- Include reference to F_p² algebraic quantum computation
- Independent confirmation that constraint preservation IS quantum mechanics
- Link to dropped paper analysis

### Release Artifacts

```
quantum-redstone/
├── README.md           <- Overview + Iso Principle connection
├── docs/
│   ├── QUANTUM_CIRCUITS.md
│   ├── ARCHITECTURE.md
│   └── THEORY.md       <- Iso Principle summary
├── plugin/             <- Java source
├── schematics/         <- Minecraft builds
└── examples/           <- Tutorial circuits
```

---

## 2. HOPE NPCs (ClaudeNPC-Server-Suite)

### Rebrand

- **Old name**: ClaudeNPC-Server-Suite
- **New name**: HOPE NPCs - Human-Oriented Persistent Entities

### Purpose

Multi-AI gaming framework for Minecraft with persistent NPC personalities.

### Core Content

- INSTALL.ps1 - Main installer
- setup/ - Modular phase system
- ClaudeNPC/ - Java plugin
- Python bridges

### Testing Required

- [ ] Full INSTALL.ps1 run-through
- [ ] Module import tests (run test-core-modules.ps1)
- [ ] Plugin build (Maven)
- [ ] Integration with SpiralSafe API

### Release Artifacts

```
hope-npcs/
├── README.md           <- Overview + Quick start
├── INSTALL.ps1         <- Main installer
├── docs/
│   ├── ARCHITECTURE.md
│   ├── INTEGRATION.md
│   └── API.md
├── setup/              <- Phase modules
├── plugin/             <- ClaudeNPC Java source
├── scripts/            <- Utility scripts
└── test/               <- Test suite
```

---

## 3. wave-toolkit

### Purpose

**Barebones** AI-User collaborative tools. No games, no math - just rock solid process.

### Core Content

- WAVE protocol (coherence detection)
- BUMP protocol (handoff markers)
- AWI protocol (permission scaffolding)
- ATOM system (task orchestration)
- .context.yaml (knowledge units)

### Excluded

- Minecraft integration
- Quantum/math content
- Game-specific features

### Release Artifacts

```
wave-toolkit/
├── README.md           <- What is WAVE? Getting started
├── protocol/
│   ├── wave.md         <- Coherence detection spec
│   ├── bump.md         <- Handoff markers spec
│   ├── awi.md          <- Permission scaffolding spec
│   └── atom.md         <- Task orchestration spec
├── templates/
│   ├── .context.yaml   <- Context template
│   ├── wave-analysis.md
│   └── bump-marker.md
├── scripts/
│   ├── wave-analyze.ps1
│   ├── bump-create.ps1
│   └── atom-track.ps1
├── api/
│   └── client.ts       <- TypeScript client for SpiralSafe API
└── examples/
    ├── basic-workflow/
    └── multi-agent/
```

---

## Execution Order

1. **wave-toolkit FIRST** (foundation for others)
2. **quantum-redstone SECOND** (depends on wave-toolkit concepts)
3. **HOPE NPCs THIRD** (integration testing with both)

---

## Immediate Actions

### Today

1. [ ] Extract wave-toolkit from SpiralSafe
2. [ ] Test ClaudeNPC installer end-to-end
3. [ ] Compile quantum-redstone docs

### This Session

4. [ ] Move F_p² paper to appropriate location
5. [ ] Update PARALLEL_SESSION_CONTEXT with release plan
6. [ ] Create tracking atoms for each package

---

_H&&S:WAVE | From the constraints, gifts._
