#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    QUANTUM RESERVOIR COMPUTING MODULE                        ║
║                                                                              ║
║        Qiskit-DSPy Hybrid for Nonlinear Temporal Processing                  ║
║                                                                              ║
║                          H&&S:WAVE | Hope&&Sauced                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

This module implements Quantum Reservoir Computing (QRC) using:
- Qiskit for quantum circuit simulation
- DSPy integration patterns for readout optimization

QRC leverages quantum dynamics for temporal information processing:
1. Input encoding via parameterized rotations
2. Reservoir dynamics via entanglement layers
3. Readout via measurement and classical post-processing

Fibonacci-weighted scaling:
- fib:1 (single qubit) → fib:3 (JC pairs) → fib:5 (oscillator nets)
- fib:8 (lattices) → fib:13 (Aquila-scale)

ATOM: ATOM-CODE-20260117-001-qrc-reservoir
Date: 2026-01-17
Protocol: H&&S:WAVE | Hope&&Sauced

Usage:
    python qrc_reservoir.py              # Run demo
    python -m pytest qrc_reservoir.py    # Run tests (if pytest available)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# =============================================================================
# CORE QRC IMPLEMENTATION (Pure Python - No External Dependencies)
# =============================================================================


@dataclass
class QuantumState:
    """
    Represents a quantum state as a dictionary of basis states to amplitudes.

    For n qubits, there are 2^n basis states (e.g., '00', '01', '10', '11' for 2 qubits).
    Amplitudes are complex numbers where |amplitude|^2 gives probability.
    """

    amplitudes: Dict[str, complex] = field(default_factory=dict)
    n_qubits: int = 2

    def __post_init__(self):
        if not self.amplitudes:
            # Initialize to |00...0⟩ state
            ground_state = "0" * self.n_qubits
            self.amplitudes = {ground_state: complex(1.0, 0.0)}

    @property
    def probabilities(self) -> Dict[str, float]:
        """Convert amplitudes to measurement probabilities."""
        return {k: abs(v) ** 2 for k, v in self.amplitudes.items()}

    def normalize(self) -> None:
        """Ensure amplitudes are normalized (probabilities sum to 1)."""
        total = sum(abs(a) ** 2 for a in self.amplitudes.values())
        if total > 0:
            factor = 1.0 / math.sqrt(total)
            self.amplitudes = {k: v * factor for k, v in self.amplitudes.items()}

    def measure(self, shots: int = 1024) -> Dict[str, int]:
        """
        Simulate measurement of the quantum state.

        Returns counts for each basis state based on probability distribution.
        Uses deterministic allocation proportional to probabilities.
        """
        probs = self.probabilities
        counts: Dict[str, int] = {}

        # Deterministic allocation for reproducibility
        remaining = shots
        for state, prob in sorted(probs.items()):
            if remaining <= 0:
                break
            count = int(round(prob * shots))
            if count > remaining:
                count = remaining
            if count > 0:
                counts[state] = count
                remaining -= count

        # Handle any rounding remainder
        if remaining > 0:
            if counts:
                max_state = max(counts, key=lambda x: probs.get(x, 0))
                counts[max_state] += remaining
            else:
                # Allocate all remaining shots to the state with highest probability
                max_state = max(probs.items(), key=lambda x: x[1])[0]
                counts[max_state] = remaining

        return counts


def apply_hadamard(state: QuantumState, qubit: int) -> QuantumState:
    """
    Apply Hadamard gate to specified qubit.

    H|0⟩ = (|0⟩ + |1⟩)/√2
    H|1⟩ = (|0⟩ - |1⟩)/√2
    """
    new_amplitudes: Dict[str, complex] = {}
    sqrt2_inv = 1.0 / math.sqrt(2)

    for basis, amp in state.amplitudes.items():
        # Get the bit value at the qubit position
        bit = basis[qubit]

        # Create new basis states with flipped bit
        basis_list = list(basis)
        basis_0 = "".join(basis_list[:qubit] + ["0"] + basis_list[qubit + 1 :])
        basis_1 = "".join(basis_list[:qubit] + ["1"] + basis_list[qubit + 1 :])

        if bit == "0":
            # H|0⟩ = (|0⟩ + |1⟩)/√2
            new_amplitudes[basis_0] = new_amplitudes.get(basis_0, 0) + amp * sqrt2_inv
            new_amplitudes[basis_1] = new_amplitudes.get(basis_1, 0) + amp * sqrt2_inv
        else:
            # H|1⟩ = (|0⟩ - |1⟩)/√2
            new_amplitudes[basis_0] = new_amplitudes.get(basis_0, 0) + amp * sqrt2_inv
            new_amplitudes[basis_1] = new_amplitudes.get(basis_1, 0) - amp * sqrt2_inv

    result = QuantumState(amplitudes=new_amplitudes, n_qubits=state.n_qubits)
    result.normalize()
    return result


def apply_rz(state: QuantumState, qubit: int, angle: float) -> QuantumState:
    """
    Apply RZ (rotation around Z-axis) gate to specified qubit.

    RZ(θ)|0⟩ = e^(-iθ/2)|0⟩
    RZ(θ)|1⟩ = e^(iθ/2)|1⟩
    """
    new_amplitudes: Dict[str, complex] = {}

    phase_0 = complex(math.cos(-angle / 2), math.sin(-angle / 2))
    phase_1 = complex(math.cos(angle / 2), math.sin(angle / 2))

    for basis, amp in state.amplitudes.items():
        bit = basis[qubit]
        if bit == "0":
            new_amplitudes[basis] = amp * phase_0
        else:
            new_amplitudes[basis] = amp * phase_1

    return QuantumState(amplitudes=new_amplitudes, n_qubits=state.n_qubits)


def apply_cnot(state: QuantumState, control: int, target: int) -> QuantumState:
    """
    Apply CNOT (controlled-NOT) gate.

    Flips target qubit if control qubit is |1⟩.
    """
    new_amplitudes: Dict[str, complex] = {}

    for basis, amp in state.amplitudes.items():
        control_bit = basis[control]
        if control_bit == "1":
            # Flip the target bit
            basis_list = list(basis)
            basis_list[target] = "1" if basis_list[target] == "0" else "0"
            new_basis = "".join(basis_list)
            new_amplitudes[new_basis] = amp
        else:
            new_amplitudes[basis] = amp

    return QuantumState(amplitudes=new_amplitudes, n_qubits=state.n_qubits)


# =============================================================================
# QRC MODULE (Pure Python Implementation)
# =============================================================================


class QRCModule:
    """
    Quantum Reservoir Computing module.

    Implements a quantum reservoir using:
    - Hadamard gates for superposition
    - CNOT gates for entanglement (reservoir dynamics)
    - RZ gates for input encoding

    This is a pure Python implementation for environments without Qiskit.
    The structure is designed to be compatible with Qiskit integration.
    """

    def __init__(self, n_qubits: int = 2, depth: int = 1):
        """
        Initialize QRC reservoir.

        Args:
            n_qubits: Number of qubits in the reservoir
            depth: Number of entanglement layers
        """
        self.n_qubits = n_qubits
        self.depth = depth
        self._circuit_depth: Optional[int] = None

    def forward(self, input_params: List[float], shots: int = 1024) -> Dict[str, int]:
        """
        Process input through the quantum reservoir.

        Args:
            input_params: List of floats to encode as rotation angles
            shots: Number of measurement shots

        Returns:
            Dictionary of measurement outcomes {bitstring: count}
        """
        # Initialize quantum state
        state = QuantumState(n_qubits=self.n_qubits)

        # Apply Hadamard to all qubits (superposition)
        for i in range(self.n_qubits):
            state = apply_hadamard(state, i)

        # Apply entanglement layers (reservoir dynamics)
        for _ in range(self.depth):
            for i in range(self.n_qubits - 1):
                state = apply_cnot(state, i, i + 1)

        # Encode input as RZ rotations
        for i, param in enumerate(input_params):
            if i < self.n_qubits:
                state = apply_rz(state, i, param)

        # Measure
        return state.measure(shots=shots)

    @property
    def circuit_depth(self) -> int:
        """
        Estimate circuit depth.

        Depth = Hadamard layer (1) + CNOT layers (depth * (n-1)) + RZ layer (1)
        """
        if self._circuit_depth is None:
            self._circuit_depth = 1 + self.depth * (self.n_qubits - 1) + 1
        return self._circuit_depth

    def get_state_vector(self, input_params: List[float]) -> Dict[str, complex]:
        """
        Get the full state vector (for analysis, not measurement).

        Returns amplitudes for each basis state.
        """
        state = QuantumState(n_qubits=self.n_qubits)

        for i in range(self.n_qubits):
            state = apply_hadamard(state, i)

        for _ in range(self.depth):
            for i in range(self.n_qubits - 1):
                state = apply_cnot(state, i, i + 1)

        for i, param in enumerate(input_params):
            if i < self.n_qubits:
                state = apply_rz(state, i, param)

        return state.amplitudes


# =============================================================================
# QISKIT INTEGRATION (Optional - when Qiskit is available)
# =============================================================================


def create_qiskit_reservoir(n_qubits: int, depth: int = 1):
    """
    Create a QRC reservoir circuit using Qiskit.

    This function is optional and only works when Qiskit is installed.

    Args:
        n_qubits: Number of qubits
        depth: Number of entanglement layers

    Returns:
        Qiskit QuantumCircuit or None if Qiskit not available
    """
    try:
        from qiskit import QuantumCircuit

        qc = QuantumCircuit(n_qubits, n_qubits)

        # Superposition layer
        qc.h(range(n_qubits))

        # Entanglement layers
        for _ in range(depth):
            for i in range(n_qubits - 1):
                qc.cx(i, i + 1)

        return qc
    except ImportError:
        return None


def run_qiskit_reservoir(
    input_params: List[float], n_qubits: int = 2, depth: int = 1, shots: int = 1024
) -> Optional[Dict[str, int]]:
    """
    Run QRC using Qiskit backend (if available).

    Args:
        input_params: Input parameters to encode
        n_qubits: Number of qubits
        depth: Entanglement depth
        shots: Measurement shots

    Returns:
        Measurement counts or None if Qiskit not available
    """
    try:
        from qiskit import QuantumCircuit
        from qiskit.transpiler import transpile
        from qiskit_aer import AerSimulator

        # Create base circuit
        qc = QuantumCircuit(n_qubits, n_qubits)
        qc.h(range(n_qubits))

        for _ in range(depth):
            for i in range(n_qubits - 1):
                qc.cx(i, i + 1)

        # Encode input
        for i, param in enumerate(input_params):
            if i < n_qubits:
                qc.rz(param, i)

        # Measure
        qc.measure(range(n_qubits), range(n_qubits))

        # Transpile and run
        sim = AerSimulator()
        optimized = transpile(qc, optimization_level=3)
        job = sim.run(optimized, shots=shots)
        result = job.result()

        return dict(result.get_counts())
    except ImportError:
        return None


# =============================================================================
# DEMO AND TESTING
# =============================================================================


def demonstrate_qrc():
    """Demonstrate QRC functionality."""
    print("=" * 70)
    print("QUANTUM RESERVOIR COMPUTING DEMONSTRATION")
    print("Pure Python Implementation")
    print("=" * 70)
    print()

    # Create 2-qubit reservoir
    qrc = QRCModule(n_qubits=2, depth=1)

    print(f"Reservoir Configuration:")
    print(f"  - Qubits: {qrc.n_qubits}")
    print(f"  - Depth: {qrc.depth}")
    print(f"  - Circuit depth: {qrc.circuit_depth}")
    print()

    # Test with different inputs
    test_inputs = [
        ([0.0, 0.0], "Zero rotations"),
        ([math.pi / 2, 0.0], "π/2 on qubit 0"),
        ([0.0, math.pi / 2], "π/2 on qubit 1"),
        ([math.pi / 2, math.pi / 2], "π/2 on both qubits"),
        ([math.pi, math.pi], "π on both qubits"),
    ]

    print("Reservoir Outputs:")
    print("-" * 50)

    for params, description in test_inputs:
        result = qrc.forward(params)
        print(f"\n{description}: {params}")
        print(f"  Counts: {result}")

        # Verify normalization
        total = sum(result.values())
        print(f"  Total shots: {total}")

    # Show state vector for analysis
    print("\n" + "=" * 70)
    print("STATE VECTOR ANALYSIS")
    print("=" * 70)

    params = [math.pi / 4, math.pi / 3]
    state = qrc.get_state_vector(params)
    print(f"\nInput: {params}")
    print("Amplitudes:")
    for basis, amp in sorted(state.items()):
        prob = abs(amp) ** 2
        print(f"  |{basis}⟩: {amp:.4f} (prob: {prob:.4f})")

    # Check if Qiskit is available
    print("\n" + "=" * 70)
    print("QISKIT INTEGRATION CHECK")
    print("=" * 70)

    qiskit_result = run_qiskit_reservoir([0.5, 0.5])
    if qiskit_result is not None:
        print("\nQiskit is available!")
        print(f"Qiskit result: {qiskit_result}")
    else:
        print("\nQiskit not installed. Using pure Python implementation.")
        print("To enable Qiskit: pip install qiskit qiskit-aer")

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


def run_tests():
    """Run basic tests for QRC implementation."""
    print("Running QRC Tests...")
    print("-" * 40)

    tests_passed = 0
    tests_failed = 0

    # Test 1: Basic initialization
    try:
        qrc = QRCModule(n_qubits=2)
        assert qrc.n_qubits == 2
        assert qrc.depth == 1
        tests_passed += 1
        print("✓ Test 1: Initialization")
    except AssertionError as e:
        tests_failed += 1
        print(f"✗ Test 1: Initialization - {e}")

    # Test 2: Forward pass produces valid output
    try:
        qrc = QRCModule(n_qubits=2)
        result = qrc.forward([0.5, 0.5])
        assert isinstance(result, dict)
        assert sum(result.values()) == 1024
        tests_passed += 1
        print("✓ Test 2: Forward pass")
    except AssertionError as e:
        tests_failed += 1
        print(f"✗ Test 2: Forward pass - {e}")

    # Test 3: Normalization
    try:
        state = QuantumState(n_qubits=2)
        state.amplitudes = {"00": 3.0, "11": 4.0}  # 3-4-5 triangle
        state.normalize()
        total_prob = sum(abs(a) ** 2 for a in state.amplitudes.values())
        assert abs(total_prob - 1.0) < 1e-10
        tests_passed += 1
        print("✓ Test 3: Normalization")
    except AssertionError as e:
        tests_failed += 1
        print(f"✗ Test 3: Normalization - {e}")

    # Test 4: Hadamard gate
    try:
        state = QuantumState(n_qubits=1)
        state = apply_hadamard(state, 0)
        probs = state.probabilities
        assert abs(probs.get("0", 0) - 0.5) < 0.01
        assert abs(probs.get("1", 0) - 0.5) < 0.01
        tests_passed += 1
        print("✓ Test 4: Hadamard gate")
    except AssertionError as e:
        tests_failed += 1
        print(f"✗ Test 4: Hadamard gate - {e}")

    # Test 5: CNOT gate
    try:
        # |10⟩ should become |11⟩
        state = QuantumState(n_qubits=2)
        state.amplitudes = {"10": 1.0}
        state = apply_cnot(state, 0, 1)
        assert "11" in state.amplitudes
        assert abs(state.amplitudes["11"]) > 0.99
        tests_passed += 1
        print("✓ Test 5: CNOT gate")
    except AssertionError as e:
        tests_failed += 1
        print(f"✗ Test 5: CNOT gate - {e}")

    # Test 6: Different qubit counts
    try:
        for n in [1, 2, 3, 4]:
            qrc = QRCModule(n_qubits=n)
            result = qrc.forward([0.1] * n)
            assert len(result) > 0
        tests_passed += 1
        print("✓ Test 6: Different qubit counts")
    except AssertionError as e:
        tests_failed += 1
        print(f"✗ Test 6: Different qubit counts - {e}")

    # Test 7: Circuit depth calculation
    try:
        qrc = QRCModule(n_qubits=3, depth=2)
        assert qrc.circuit_depth > 0
        tests_passed += 1
        print("✓ Test 7: Circuit depth")
    except AssertionError as e:
        tests_failed += 1
        print(f"✗ Test 7: Circuit depth - {e}")

    print("-" * 40)
    print(f"Tests: {tests_passed} passed, {tests_failed} failed")

    return tests_failed == 0


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        success = run_tests()
        sys.exit(0 if success else 1)
    else:
        demonstrate_qrc()
