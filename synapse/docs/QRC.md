# Quantum Reservoir Computing in SYNAPSE

## Overview

SYNAPSE integrates Quantum Reservoir Computing (QRC) as a fundamental visualization layer, mapping QRC substrates to the Fibonacci scale hierarchy.

## QRC Fundamentals

### What is QRC?

Quantum Reservoir Computing leverages intrinsic quantum dynamics for temporal information processing:

```
Input → Quantum Reservoir → Measurement → Readout
         (Unitary Evolution)   (Collapse)   (Training)
```

Key advantages over classical reservoirs:
- **Exponential Hilbert space**: N qubits → 2^N dimensions
- **Quantum interference**: Complex feature maps
- **Entanglement**: Non-local correlations
- **Natural fading memory**: Via decoherence

### Mathematical Foundation

State evolution:
```
|ψ(t+1)⟩ = U(x(t)) |ψ(t)⟩
```

Where:
- `|ψ(t)⟩` is the quantum state
- `U(x(t))` is a unitary operator encoding input `x(t)`
- Measurement yields classical output for readout

## SYNAPSE Implementation

### 1. Substrate Types

```typescript
enum QRCSubstrate {
  SINGLE_QUBIT,      // fib:1  - Educational
  JC_PAIRS,          // fib:3  - Jaynes-Cummings
  OSCILLATOR_NETS,   // fib:5  - Parametric oscillators
  BOSE_HUBBARD,      // fib:8  - Optical lattices
  AQUILA_SCALE,      // fib:13 - Rydberg atoms (256+ qubits)
}
```

### 2. Quantum State Representation

```typescript
interface QuantumState {
  amplitudes: Array<[number, number]>;  // [real, imaginary]
  probabilities: number[];               // |amplitude|²
  coherence: number;                     // Fidelity metric
}
```

### 3. Reservoir Creation

```typescript
function createReservoirState(
  substrate: QRCSubstrate,
  nQubits: number,
  inputParams: number[],
  depth: number = 1
): ReservoirState
```

Circuit structure:
1. **Initial superposition**: Hadamard on all qubits
2. **Entanglement layers**: CNOT chains (depth × nQubits)
3. **Input encoding**: Rotation gates R_z(θ) with input params

### 4. Visualization Features

#### Phase Color Mapping
Complex amplitudes map to colors:
- **Phase** → Hue (0° = red, 120° = green, 240° = blue)
- **Magnitude** → Brightness

```glsl
vec3 complexToColor(vec2 amplitude) {
    float phase = atan(amplitude.y, amplitude.x);
    float magnitude = length(amplitude);
    float hue = (phase + PI) / (2.0 * PI);
    return hsv2rgb(vec3(hue, 0.8, magnitude));
}
```

#### Entanglement Patterns
Helical visualization connecting entangled qubits:
```glsl
vec3 entanglementPattern(vec3 pos, vec3 q1, vec3 q2, float time) {
    // Helical pattern along connection line
    // Color shifts with entanglement phase
}
```

#### Measurement Collapse
Wave-front animation showing collapse:
```typescript
useSuperposition({
  collapseAnimationDuration: 1000,  // ms
  decoherenceRate: 0.001
})
```

## Performance Metrics

### QRC-Specific Metrics

```typescript
interface QRCMetrics {
  fidelity: number;           // Coherence [0, 1]
  energy: number;             // Circuit depth (FLOPs proxy)
  collapseProximity: number;  // Distance to measurement
  snapInRate: number;         // Successful integrations
  entanglement: {
    entropy: number;          // Von Neumann entropy
    pairs: Array<[number, number]>;
    strength: number;
  };
}
```

### Target Values
- **Fidelity**: ≥ 0.95 (95% coherence)
- **Energy**: Minimize (circuit depth)
- **Snap-in Rate**: ≥ 0.85 (85% success)

## Integration Examples

### Example 1: Single Qubit Visualization

```typescript
import { createReservoirState, QRCSubstrate } from '@spiralsafe/synapse';

const reservoir = createReservoirState(
  QRCSubstrate.SINGLE_QUBIT,
  1,
  [Math.PI / 4],  // 45° rotation
  1
);

// Visualize on Bloch sphere
```

### Example 2: Aquila-Scale System

```typescript
const aquilaReservoir = createReservoirState(
  QRCSubstrate.AQUILA_SCALE,
  256,
  inputParams,
  3  // 3 entanglement layers
);

// Hexagonal lattice visualization
// Rydberg blockade radius shown
```

### Example 3: QRC-HR Hybrid

```typescript
const { state: hrState } = useHindmarshRose({
  params: { I: 3.0 }
});

const qrcState = createReservoirState(
  QRCSubstrate.OSCILLATOR_NETS,
  5,
  [hrState.x, hrState.y, hrState.z],
  2
);

// Quantum reservoir modulated by neural state
// HR coherence affects QRC fidelity
```

## Substrate Details

### 1. Single Qubit (fib:1)
- **Visualization**: Bloch sphere
- **Use case**: Educational, concept demonstration
- **Advantages**: Simple, fast simulation

### 2. JC Pairs (fib:3)
- **Visualization**: Coupled oscillators
- **Use case**: Time-series processing
- **Advantages**: Tunable coupling, natural ML basis

### 3. Oscillator Networks (fib:5)
- **Visualization**: Dense neuron network
- **Use case**: High-dimensional feature maps
- **Advantages**: Infinite-dimensional Hilbert space, up to 81 effective neurons from 2 oscillators

### 4. Bose-Hubbard (fib:8)
- **Visualization**: Optical lattice
- **Use case**: Clean physics testbed
- **Advantages**: Optimal in ergodic regime, no disorder needed

### 5. Aquila Scale (fib:13)
- **Visualization**: Hexagonal Rydberg array
- **Use case**: Large-scale QRC
- **Advantages**: 256+ qubits, gradient-free training, native graph structure

## Shader Reference

### Quantum Interference
```glsl
float quantumInterference(vec3 pos, vec2 amp1, vec2 amp2, float time) {
    float phase1 = atan(amp1.y, amp1.x);
    float phase2 = atan(amp2.y, amp2.x);
    float deltaPhase = phase2 - phase1;
    
    float mag1 = length(amp1);
    float mag2 = length(amp2);
    
    // Interference term
    return mag1*mag1 + mag2*mag2 + 2.0*mag1*mag2*cos(k*length(pos) + deltaPhase - time);
}
```

### Decoherence Animation
```glsl
float decoherence(float initialCoherence, float time, float rate) {
    return initialCoherence * exp(-rate * time);
}
```

### Substrate Rendering
```glsl
vec3 substrateVisualization(vec3 pos, int substrate, float time) {
    // substrate: 0=qubit, 1=jc, 2=oscillator, 3=bose_hubbard, 4=aquila
    // Returns color based on substrate geometry
}
```

## Research Applications

### 1. Pattern Recognition
QRC naturally separates patterns in high-dimensional space:
- Input encoding via rotation gates
- Reservoir dynamics create rich feature space
- Linear readout for classification

### 2. Time-Series Prediction
Fading memory via decoherence enables temporal processing:
- Recent inputs have stronger influence
- Past inputs gradually fade
- Natural forgetting mechanism

### 3. Hybrid Classical-Quantum
SYNAPSE supports hybrid workflows:
- Classical preprocessing
- QRC feature extraction
- Classical readout training
- Real-time visualization of all layers

## SpiralSafe Alignment

### Isomorphism Principle
QRC demonstrates substrate independence:
```
Oscillators ≅ Spins ≅ Atoms ≅ Photons
```
The reservoir computation is preserved; only the physical implementation changes.

### Constraints as Gifts
- **Limited qubits** → Forces efficient encoding
- **Decoherence** → Natural fading memory (feature, not bug)
- **Measurement** → Definite outcomes for readout
- **Unitarity** → Information preservation

### WAVE Integration
QRC coherence maps to WAVE metrics:
- **Curl**: Cyclic dynamics in reservoir
- **Potential**: Unused computational capacity
- **Dispersion**: Decoherence spreading

## References

1. Fujii & Nakajima (2017). "Harnessing Disordered-Ensemble Quantum Dynamics for Machine Learning." *Physical Review Applied*.

2. Mujal et al. (2021). "Opportunities in Quantum Reservoir Computing." *Advanced Quantum Technologies*.

3. Bravo et al. (2022). "Quantum Reservoir Computing Using Arrays of Rydberg Atoms." *PRX Quantum*.

4. Nature (2023). "Quantum reservoir computing with a single nonlinear oscillator."

## API Quick Reference

```typescript
// Create reservoir
const reservoir = createReservoirState(substrate, nQubits, inputs, depth);

// Measure
const result = measureReservoir(reservoir, shots);

// Calculate metrics
const metrics = calculateQRCMetrics(reservoir);

// Evolve with decoherence
const evolved = evolveReservoir(reservoir, dt, decoherenceRate);

// Hooks
const { state, history } = useHindmarshRose();
const { coherence } = useCoherence();
const { currentScale } = useFibonacciScale();
const { observe, isCollapsing } = useSuperposition();
```

---

**ATOM:** ATOM-DOC-20260119-002-qrc-synapse-integration

From quantum substrates, emergent patterns arise. 🔬🌀
