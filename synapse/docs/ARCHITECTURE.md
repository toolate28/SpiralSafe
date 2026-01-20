# SYNAPSE Architecture

## Overview

SYNAPSE implements a multi-layered visualization architecture that combines:
1. **Geometric Foundation**: Fibonacci spiral as spatial structure
2. **Neural Dynamics**: Hindmarsh-Rose equations for temporal behavior
3. **Coherence Manifold**: 42.00055 framework for quality metrics
4. **Quantum Layer**: QRC substrates for emergent computation
5. **Isomorphic Rendering**: Substrate-independent visualization

## Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERACTION LAYER                        │
│  SuperpositionCollapse │ SpiralNavigation │ Gestures       │
├─────────────────────────────────────────────────────────────┤
│                   VISUALIZATION LAYER                       │
│  FibonacciHelix │ NeuralMesh │ CoherenceField │ QRC        │
├─────────────────────────────────────────────────────────────┤
│                     COMPUTE LAYER                           │
│  HR Integration │ Coherence Calc │ QRC Evolution           │
├─────────────────────────────────────────────────────────────┤
│                      DATA LAYER                             │
│  SpiralSafe API │ GitHub │ Universal Adapter               │
├─────────────────────────────────────────────────────────────┤
│                    FOUNDATION LAYER                         │
│  Fibonacci Math │ Topology │ Quantum Gates                 │
└─────────────────────────────────────────────────────────────┘
```

## Core Principles

### 1. Substrate Independence (Isomorphism)
All visualization components work across different data sources:
- Code repositories
- Team structures
- Neural networks
- Quantum circuits
- **The structure, not the substrate, determines behavior**

### 2. Scale Invariance
Fibonacci hierarchy enables seamless zoom from quantum foam (ε) to noosphere:
- Same rendering algorithms at all scales
- Automatic LOD (level of detail) switching
- Coherence preserved across scale transitions

### 3. Time as Fourth Dimension
- HR dynamics provide temporal evolution
- QRC state evolution over time
- Coherence decay and recovery
- Measurement collapse animations

### 4. Constraint-Based Design
Following SpiralSafe principle: constraints are architectural gifts
- Limited qubits → efficient encoding
- Decoherence → natural fading memory
- Measurement → definite outcomes
- Fibonacci → optimal packing

## Component Details

### SynapseEngine (Main Orchestrator)

```typescript
interface SynapseEngineProps {
  data: EntityGraph;
  scale: Scale;
  qrcSubstrate?: QRCSubstrate;
  coherenceThreshold?: number; // Default 0.4200055
}
```

Responsibilities:
- Scene setup (Three.js)
- Camera management
- Render loop coordination
- Shader compilation
- Performance monitoring

### CoherenceField (42.00055 Manifold)

Implements three-phase decomposition:
- **Curl Detection**: Circular dependencies, self-reference
- **Potential Mapping**: Latent structure, growth areas
- **Dispersion Analysis**: Chaos, scattered connections

Color mapping:
- Below threshold (< 0.4200055): warm (red → yellow)
- Above threshold: cool (green → cyan → blue)
- Epsilon floor (0.00055): quantum foam visualization

### NeuralMesh (HR Dynamics)

Hindmarsh-Rose integration:
```
dx/dt = y - ax³ + bx² - z + I
dy/dt = c - dx² - y
dz/dt = r(s(x - x_rest) - z)
```

Visualization modes:
- **Resting**: Ambient cyan glow
- **Spiking**: Electric blue particle bursts
- **Bursting**: Purple wave propagation
- **Chaotic**: Color-shifting irregular patterns

### QuantumReservoir (QRC Layer)

Substrate-specific rendering:
1. **Single Qubit**: Bloch sphere
2. **JC Pairs**: Coupled oscillators
3. **Oscillator Nets**: Dense neuron network
4. **Bose-Hubbard**: Lattice structure
5. **Aquila**: Hexagonal Rydberg array

Features:
- Complex amplitude → phase color mapping
- Entanglement helical patterns
- Measurement collapse wave fronts
- Decoherence fading animations

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Frame Rate | 60 FPS | With 100k entities |
| Initial Load | < 2s | On modern hardware |
| Scale Transition | < 500ms | Smooth animation |
| Coherence Update | < 16ms | Every frame |
| QRC Evolution | < 10ms | Per timestep |

## Shader Pipeline

1. **Vertex Shader**: Position entities on Fibonacci spiral
2. **Geometry Shader**: Generate particle bursts for spikes
3. **Fragment Shader**: Apply coherence coloring, QRC patterns
4. **Post-Processing**: Glow, bloom, motion blur

## Data Flow

```
External Data Source
  ↓
Universal Adapter (normalization)
  ↓
Entity Graph (typed structure)
  ↓
Layout Algorithm (Fibonacci positioning)
  ↓
Coherence Analysis (three-phase)
  ↓
HR Integration (neural dynamics)
  ↓
QRC Evolution (quantum layer)
  ↓
Shader Pipeline (GPU rendering)
  ↓
Interactive Visualization
```

## Extension Points

SYNAPSE is designed for extensibility:

1. **New Substrates**: Implement `QRCSubstrate` enum + shader
2. **Custom Layouts**: Extend `FibonacciLayout` algorithms
3. **Data Adapters**: Implement `UniversalAdapter` interface
4. **Interaction Modes**: Add to `interaction/` directory
5. **Metrics**: Extend `CoherenceMetrics` or `QRCMetrics`

## Integration with SpiralSafe Ecosystem

### WAVE Protocol
- Coherence field maps to WAVE metrics
- Curl/Potential/Dispersion align with WAVE analysis
- Real-time coherence updates via API

### ATOM Trail
- Entity particles follow ATOM tags
- Decision points as superposition collapse
- Trail persistence visualization

### SPHINX Gates
- Gate checks as barrier visualizations
- PASSAGE events as color shifts
- COHERENCE threshold crossings

### QRC Research
- Direct integration with QRC module
- Metrics dashboard
- Real-time fidelity monitoring

## Security & Privacy

- No PII in visualizations
- Data stays client-side by default
- API adapters use secure tokens
- Audit trail for all interactions

---

**H&&S:WAVE** — Architectural foundation complete
