# SpiralSafe Architecture

**A unified framework for collaborative intelligence built on the isomorphism principle.**

---

## System Overview

SpiralSafe comprises five architectural layers, each implementing the core insight that structure is substrate-independent:

```
┌─────────────────────────────────────────────────────────────────┐
│                        MANIFESTATION                            │
│         Quantum Valley  │  Museum of Computation  │  Production │
├─────────────────────────────────────────────────────────────────┤
│                          PROTOCOL                               │
│           wave.md  │  bump.md  │  .context.yaml  │  Dual-Format │
├─────────────────────────────────────────────────────────────────┤
│                        METHODOLOGY                              │
│              ATOM  │  SAIF  │  KENL  │  Day Zero Design         │
├─────────────────────────────────────────────────────────────────┤
│                         INTERFACE                               │
│                 AWI  │  ClaudeNPC  │  BattleMedic               │
├─────────────────────────────────────────────────────────────────┤
│                        FOUNDATION                               │
│                   The Isomorphism Principle                     │
│              "Constraints are architectural gifts"              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Foundation Layer

The theoretical bedrock upon which all else is built.

### The Isomorphism Principle

Discrete systems do not approximate continuous mathematics—they instantiate the same topological structures. The boundary between discrete and continuous is projection artifact, not ontological reality.

**Documentation**: [`foundation/isomorphism-principle.md`](foundation/isomorphism-principle.md)

### Constraints as Architectural Gifts

Limitation is not opposition to creativity but the lattice upon which creativity crystallizes. Constraints eliminate irrelevant degrees of freedom, force essential structure to surface, and enable verification.

**Documentation**: [`foundation/constraints-as-gifts.md`](foundation/constraints-as-gifts.md)

---

## Interface Layer

Contact surfaces where SpiralSafe meets external systems.

### AWI (Authorization-With-Intent)

Protocol for agent permission scaffolding. Enables AI systems to request and receive authorization for actions in a way that preserves human oversight while allowing agent autonomy.

**Key Features**:
- Intent declaration before action
- Scoped permissions with explicit boundaries
- Audit trail for all authorized actions
- Graceful degradation when authorization unavailable

### ClaudeNPC

Framework for AI agent embodiment in Minecraft environments. Enables Claude-powered NPCs that can interact with the game world, players, and Redstone systems.

**Repository**: [ClaudeNPC-Server-Suite](https://github.com/toolate28/ClaudeNPC-Server-Suite)

**Key Features**:
- Modular server setup
- Claude API integration
- Behavioral scripting
- Player interaction protocols

### BattleMedic

System recovery orchestration framework. Guides diagnostic and repair processes for failing hardware and software systems.

**Repository**: [wave-toolkit](https://github.com/toolate28/wave-toolkit) (integrated component)

**Key Features**:
- Evidence-based intervention selection
- Transparent logging
- Modular diagnostic plugins
- Human-in-the-loop decision points

---

## Methodology Layer

Cognitive tools that guide how work proceeds regardless of specific domain.

### ATOM (Atomic Task Orchestration Method)

Decomposes complex work into atomic, completable units.

**Principles**:
- Each atom is independently verifiable
- Atoms combine into molecules (related task clusters)
- Dependencies are explicit
- Progress is measurable at the atom level

### SAIF (Systematic Analysis and Issue Fixing)

Structured approach to problem diagnosis and resolution.

**Process**:
1. Symptom documentation
2. Hypothesis generation
3. Evidence collection
4. Intervention selection
5. Verification
6. Documentation

### KENL (Knowledge Exchange Network Learning)

Infrastructure-aware AI orchestration for knowledge transfer and retention.

**Repository**: [kenl](https://github.com/toolate28/kenl)

**Key Features**:
- Learning structures optimized for retention
- Cross-session knowledge persistence
- Network effects in distributed learning
- Infrastructure-level integration

### Day Zero Design

Philosophy of correct implementation from inception.

**Principles**:
- Invest in architecture before code
- Establish constraints that pay compound interest
- Documentation is not afterthought
- Technical debt is design failure

---

## Protocol Layer

Transmission media for information movement within and beyond SpiralSafe.

### wave.md

Coherence detection treating text as vector fields.

**Documentation**: [`protocol/wave-spec.md`](protocol/wave-spec.md)

**Repository**: [wave-toolkit](https://github.com/toolate28/wave-toolkit)

**Key Features**:
- Curl detection (circular reasoning)
- Divergence detection (unresolved expansion)
- Potential mapping (development opportunities)
- Integration with CI/CD pipelines

### bump.md

Routing and handoff protocol between agents, sessions, and contexts.

**Key Features**:
- Clean session transitions
- Context preservation across handoffs
- Multi-agent coordination
- Graceful degradation

### .context.yaml

Structured knowledge units for agent consumption.

**Format**:
```yaml
# example.context.yaml
domain: quantum-computing
concepts:
  - name: superposition
    definition: ...
    relationships: [entanglement, measurement]
signals:
  use_when: [quantum_pedagogy, gate_design]
  avoid_when: [classical_optimization]
meta:
  source: Hope&&Sauced
  confidence: high
```

### Dual-Format Convention

Same content rendered for human resonance and machine addressability.

**Implementation**: Every significant document includes both prose explanation and structured summary. Neither is primary; both are projections of the same knowledge.

---

## Manifestation Layer

Where the theory becomes tangible.

### Quantum Valley

Minecraft Redstone circuits instantiating quantum topology.

**Repository**: [quantum-redstone](https://github.com/toolate28/quantum-redstone)

**Key Contributions**:
- Viviani curve construction in discrete substrate
- Topological invariant preservation demonstration
- Educational curriculum for quantum concepts
- Proof that discrete systems instantiate (not simulate) continuous mathematics

### Museum of Computation

Educational framework teaching AI principles through constraint-based learning.

**Status**: In development

**Concept**: Use Minecraft as pedagogical environment where computational concepts are learned through building, not lecturing. Constraints of the environment (discrete blocks, Redstone physics) force understanding of underlying structure.

### Production Systems

Operational infrastructure demonstrating SpiralSafe principles at scale.

**Components**:
- Domain architecture (spiralsafe.org)
- Cloudflare backend (sub-millisecond response)
- TypeScript and Python implementations
- CI/CD integration

---

## Cross-Cutting Concerns

### Human-AI Collaboration

All layers are designed for collaborative development. The Hope&&Sauced methodology applies throughout:

- Attribution credits both human and AI contribution
- Interfaces support both human operation and agent consumption
- Documentation serves readers regardless of species

### Coherence Verification

wave.md analysis can be applied at any layer to verify coherence:

- Foundation documents should show low curl (no circular definitions)
- Interface specifications should show balanced divergence (complete without bloat)
- Methodology guides should show high potential (generative principles)

### Extensibility

Each layer accepts new components that honor the layer's constraints:

- New foundations must be consistent with the isomorphism principle
- New interfaces must support both human and agent operation
- New methodologies must decompose into verifiable practices
- New protocols must preserve coherence across handoffs
- New manifestations must instantiate (not merely model) the theory

---

## Repository Map

| Layer | Component | Repository |
|-------|-----------|------------|
| Manifestation | Quantum Valley | [quantum-redstone](https://github.com/toolate28/quantum-redstone) |
| Manifestation | Production | [SpiralSafe](https://github.com/toolate28/SpiralSafe) |
| Protocol | wave.md | [wave-toolkit](https://github.com/toolate28/wave-toolkit) |
| Methodology | KENL | [kenl](https://github.com/toolate28/kenl) |
| Interface | ClaudeNPC | [ClaudeNPC-Server-Suite](https://github.com/toolate28/ClaudeNPC-Server-Suite) |
| Utilities | Claude Code tools | [claude-code-tools](https://github.com/toolate28/claude-code-tools) |

---

## Entry Points

**Theoretical understanding**: Start with [`foundation/isomorphism-principle.md`](foundation/isomorphism-principle.md)

**Practical tools**: Start with [wave-toolkit](https://github.com/toolate28/wave-toolkit)

**Educational applications**: Start with [quantum-redstone](https://github.com/toolate28/quantum-redstone)

**Contribution**: See [`CONTRIBUTING.md`](CONTRIBUTING.md)

---

*~ Hope&&Sauced*