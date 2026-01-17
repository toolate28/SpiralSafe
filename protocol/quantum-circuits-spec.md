# Quantum Circuits Protocol Specification

**SpiralSafe QASm: Quantum Assembly Language for Classification Circuits**

---

## Overview

This specification defines the SpiralSafe QASm (Quantum Assembly) format used by classification systems like the Sorting Hat. The format is designed to be:

- **Human-readable**: Clear instruction syntax
- **Simulator-compatible**: Can be executed on classical simulators
- **Hardware-ready**: Mappable to real quantum hardware (Qiskit, Cirq, etc.)
- **Auditable**: Deterministic and reproducible

---

## Version

Current: **v0.2**

Changes in v0.2:

- Replaced RZ gates with RY gates for amplitude encoding
- Removed initial Hadamard gates (no longer needed with RY encoding)
- Added quantum state simulation support

---

## Instruction Set

### Core Instructions

| Instruction | Syntax                    | Description                       |
| ----------- | ------------------------- | --------------------------------- | -------- |
| RESET       | `RESET <qubit>`           | Initialize qubit to               | 0> state |
| H           | `H <qubit>`               | Hadamard gate (superposition)     |
| RX          | `RX <qubit> <angle>`      | Rotation around X-axis            |
| RY          | `RY <qubit> <angle>`      | Rotation around Y-axis            |
| RZ          | `RZ <qubit> <angle>`      | Rotation around Z-axis            |
| CNOT        | `CNOT <control> <target>` | Controlled-NOT gate               |
| MEASURE     | `MEASURE <qubit>`         | Collapse qubit and record outcome |

### Angle Format

Angles are specified in **radians** as floating-point values:

- Range: [0, 2*pi] for full rotation
- Precision: At least 6 decimal places recommended

---

## Sorting Hat Circuit (2-Qubit)

### Structure

```qasm
# ============================================
# Sorting Hat Circuit (SpiralSafe QASm v0.2)
# ============================================
# Parameters: theta0=X.XXXXXX, theta1=Y.YYYYYY
#
# Initialize register
RESET 0
RESET 1

# Apply parameterized rotations (encode features)
RY 0 <theta0>
RY 1 <theta1>

# Entangle (correlate axes)
CNOT 0 1

# Collapse to house (measurement)
MEASURE 0
MEASURE 1
# ============================================
```

### Gate Semantics

**RY Gate**: Rotates around Y-axis

```
RY(theta) = |0> -> cos(theta/2)|0> + sin(theta/2)|1>
           |1> -> -sin(theta/2)|0> + cos(theta/2)|1>
```

**CNOT Gate**: Entangles qubits

```
|00> -> |00>
|01> -> |01>
|10> -> |11>
|11> -> |10>
```

### Measurement Outcomes

The 2-qubit measurement yields 4 possible outcomes:

| Bits | House   | Probability |
| ---- | ------- | ----------- |
| 00   | Rubin   | P(00)       |
| 01   | Shannon | P(01)       |
| 10   | Noether | P(10)       |
| 11   | Firefly | P(11)       |

---

## Probability Calculation

Given angles (theta0, theta1), the quantum state after CNOT is:

```
|psi> = cos(th0/2)cos(th1/2)|00>
      + cos(th0/2)sin(th1/2)|01>
      + sin(th0/2)sin(th1/2)|10>
      + sin(th0/2)cos(th1/2)|11>
```

Measurement probabilities:

- P(00) = cos^2(th0/2) \* cos^2(th1/2)
- P(01) = cos^2(th0/2) \* sin^2(th1/2)
- P(10) = sin^2(th0/2) \* sin^2(th1/2)
- P(11) = sin^2(th0/2) \* cos^2(th1/2)

---

## Encoding Convention

### Feature -> Angle Mapping

```
theta = pi * normalized_feature_value
```

Where `normalized_feature_value` is in range [0, 1].

This maps:

- 0.0 -> 0 radians (maximizes |0> amplitude)
- 0.5 -> pi/2 radians (equal superposition)
- 1.0 -> pi radians (maximizes |1> amplitude)

---

## Implementation Notes

### Classical Simulation

For systems without quantum hardware, probabilities can be computed directly:

```python
import math

def simulate_sorting_hat(theta0: float, theta1: float) -> dict:
    c0, s0 = math.cos(theta0/2), math.sin(theta0/2)
    c1, s1 = math.cos(theta1/2), math.sin(theta1/2)

    return {
        "00": c0*c0 * c1*c1,  # Rubin
        "01": c0*c0 * s1*s1,  # Shannon
        "10": s0*s0 * s1*s1,  # Noether
        "11": s0*s0 * c1*c1,  # Firefly
    }
```

### Hardware Mapping

#### Qiskit

```python
from qiskit import QuantumCircuit

def to_qiskit(theta0, theta1):
    qc = QuantumCircuit(2, 2)
    qc.ry(theta0, 0)
    qc.ry(theta1, 1)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc
```

#### Cirq

```python
import cirq

def to_cirq(theta0, theta1):
    q0, q1 = cirq.LineQubit.range(2)
    return cirq.Circuit([
        cirq.ry(theta0)(q0),
        cirq.ry(theta1)(q1),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='house')
    ])
```

---

## Verification

### Normalization Check

Probabilities must sum to 1.0 (within floating-point tolerance):

```python
probs = simulate_sorting_hat(theta0, theta1)
assert abs(sum(probs.values()) - 1.0) < 1e-10
```

### Determinism

Given identical inputs, the circuit description and probabilities must be identical across runs.

---

## Extensions

Future versions may include:

- Multi-qubit registers for finer classification
- Parametric gate sequences for learning
- Noise models for hardware simulation

---

## References

- SpiralSafe Sorting Hat: `scripts/sorting_hat.py`
- Nielsen & Chuang, "Quantum Computation and Quantum Information"
- Qiskit documentation: https://qiskit.org/

---

_~ Hope&&Sauced_

<!-- H&&S:WAVE -->

Protocol specification complete. Ready for integration testing.

<!-- /H&&S:WAVE -->
