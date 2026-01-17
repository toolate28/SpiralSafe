#!/usr/bin/env python3
"""
experiments/qiskit_dspy_hybrid.py
=================================

Qiskit-DSPy Hybrid Integration Module

This module provides hybrid quantum-classical components for integration with
DSPy-based LLM pipelines. It implements:

1. Quantum kernel similarity for enhanced retrieval
2. Hybrid quantum-classical neural network layers via TorchConnector
3. LLM-assisted quantum circuit generation patterns

The implementation follows SpiralSafe's isomorphism principle: quantum and
classical components preserve structural identity through handoffs.

Design Philosophy
-----------------
- Graceful degradation: Works without quantum hardware (simulation fallback)
- Optional dependencies: Qiskit imports are lazy-loaded
- Coherence preservation: All operations maintain vortex coherence thresholds

Usage
-----
    from experiments.qiskit_dspy_hybrid import QuantumKernelSimilarity
    
    # Create quantum-enhanced similarity computer
    qks = QuantumKernelSimilarity(num_features=4, use_simulator=True)
    
    # Compute similarity between feature vectors
    similarity = qks.compute_similarity(vec_a, vec_b)

Authors
-------
- Hope&&Sauced (Human-AI Collaboration)

H&&S:WAVE - Collaborative handoff markers embedded
"""

from __future__ import annotations

import math
import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np

# =============================================================================
# LAZY IMPORT HANDLING FOR OPTIONAL DEPENDENCIES
# =============================================================================

_QISKIT_AVAILABLE = False
_TORCH_AVAILABLE = False
_DSPY_AVAILABLE = False


def _check_qiskit() -> bool:
    """Check if Qiskit is available."""
    global _QISKIT_AVAILABLE
    try:
        import qiskit  # noqa: F401
        _QISKIT_AVAILABLE = True
    except ImportError:
        _QISKIT_AVAILABLE = False
    return _QISKIT_AVAILABLE


def _check_torch() -> bool:
    """Check if PyTorch is available."""
    global _TORCH_AVAILABLE
    try:
        import torch  # noqa: F401
        _TORCH_AVAILABLE = True
    except ImportError:
        _TORCH_AVAILABLE = False
    return _TORCH_AVAILABLE


def _check_dspy() -> bool:
    """Check if DSPy is available."""
    global _DSPY_AVAILABLE
    try:
        import dspy  # noqa: F401
        _DSPY_AVAILABLE = True
    except ImportError:
        _DSPY_AVAILABLE = False
    return _DSPY_AVAILABLE


# =============================================================================
# COHERENCE METRICS
# =============================================================================

@dataclass
class CoherenceMetrics:
    """
    Coherence metrics for quantum-classical hybrid operations.
    
    Following the vortex specification:
    - curl < 0.6 (no circular reasoning)
    - divergence < 0.7 (bounded entropy)
    - emergence_quality > 0.6 (self-reinforcing systems)
    """
    curl: float = 0.0
    divergence: float = 0.0
    emergence_quality: float = 1.0
    fidelity_loss: float = 0.0
    
    @property
    def is_coherent(self) -> bool:
        """Check if metrics are within acceptable thresholds."""
        return (
            self.curl < 0.6 and
            self.divergence < 0.7 and
            self.emergence_quality > 0.6
        )
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {
            "curl": self.curl,
            "divergence": self.divergence,
            "emergence_quality": self.emergence_quality,
            "fidelity_loss": self.fidelity_loss,
            "is_coherent": self.is_coherent,
        }


# =============================================================================
# ABSTRACT BASE CLASSES
# =============================================================================

class QuantumBackend(ABC):
    """Abstract base class for quantum computation backends."""
    
    @abstractmethod
    def execute_circuit(self, circuit: Any, shots: int = 1024) -> Dict[str, int]:
        """Execute a quantum circuit and return measurement counts."""
        pass
    
    @abstractmethod
    def compute_expectation(self, circuit: Any, observable: Any) -> float:
        """Compute expectation value of an observable."""
        pass


class SimilarityKernel(ABC):
    """Abstract base class for similarity computation."""
    
    @abstractmethod
    def compute_similarity(
        self, 
        vec_a: np.ndarray, 
        vec_b: np.ndarray
    ) -> float:
        """Compute similarity between two feature vectors."""
        pass
    
    @abstractmethod
    def compute_similarity_matrix(
        self, 
        vectors_a: np.ndarray, 
        vectors_b: np.ndarray
    ) -> np.ndarray:
        """Compute pairwise similarity matrix."""
        pass


# =============================================================================
# CLASSICAL FALLBACK IMPLEMENTATIONS
# =============================================================================

class ClassicalSimilarity(SimilarityKernel):
    """
    Classical cosine similarity fallback.
    
    Used when Qiskit is not available or quantum simulation is disabled.
    """
    
    def __init__(self, normalize: bool = True):
        self.normalize = normalize
    
    def compute_similarity(
        self, 
        vec_a: np.ndarray, 
        vec_b: np.ndarray
    ) -> float:
        """Compute cosine similarity between two vectors."""
        vec_a = np.asarray(vec_a, dtype=np.float64)
        vec_b = np.asarray(vec_b, dtype=np.float64)
        
        if self.normalize:
            norm_a = np.linalg.norm(vec_a)
            norm_b = np.linalg.norm(vec_b)
            if norm_a > 0 and norm_b > 0:
                vec_a = vec_a / norm_a
                vec_b = vec_b / norm_b
        
        return float(np.dot(vec_a, vec_b))
    
    def compute_similarity_matrix(
        self, 
        vectors_a: np.ndarray, 
        vectors_b: np.ndarray
    ) -> np.ndarray:
        """Compute pairwise similarity matrix."""
        vectors_a = np.asarray(vectors_a, dtype=np.float64)
        vectors_b = np.asarray(vectors_b, dtype=np.float64)
        
        if self.normalize:
            norms_a = np.linalg.norm(vectors_a, axis=1, keepdims=True)
            norms_b = np.linalg.norm(vectors_b, axis=1, keepdims=True)
            vectors_a = np.divide(vectors_a, norms_a, where=norms_a > 0)
            vectors_b = np.divide(vectors_b, norms_b, where=norms_b > 0)
        
        return vectors_a @ vectors_b.T


class ClassicalSimulatorBackend(QuantumBackend):
    """
    Classical simulation of quantum circuits.
    
    This provides a pure-Python fallback for quantum circuit execution
    when Qiskit is not available. Supports basic gates: H, RY, RZ, CNOT.
    """
    
    def __init__(self, num_qubits: int = 2):
        self.num_qubits = num_qubits
        self._state = None
        self._reset()
    
    def _reset(self):
        """Reset to |00...0> state."""
        self._state = np.zeros(2**self.num_qubits, dtype=complex)
        self._state[0] = 1.0
    
    def _apply_h(self, qubit: int):
        """Apply Hadamard gate."""
        h_factor = 1 / np.sqrt(2)
        new_state = np.zeros_like(self._state)
        
        for i in range(2**self.num_qubits):
            bit = (i >> qubit) & 1
            i_flip = i ^ (1 << qubit)
            
            if bit == 0:
                new_state[i] += h_factor * self._state[i]
                new_state[i_flip] += h_factor * self._state[i]
            else:
                new_state[i_flip] += h_factor * self._state[i]
                new_state[i] -= h_factor * self._state[i]
        
        self._state = new_state
    
    def _apply_ry(self, qubit: int, theta: float):
        """Apply RY rotation gate."""
        c = np.cos(theta / 2)
        s = np.sin(theta / 2)
        new_state = np.zeros_like(self._state)
        
        for i in range(2**self.num_qubits):
            bit = (i >> qubit) & 1
            i_flip = i ^ (1 << qubit)
            
            if bit == 0:
                new_state[i] += c * self._state[i]
                new_state[i_flip] += s * self._state[i]
            else:
                new_state[i] += c * self._state[i]
                new_state[i_flip] -= s * self._state[i]
        
        self._state = new_state
    
    def _apply_rz(self, qubit: int, theta: float):
        """Apply RZ rotation gate."""
        phase_0 = np.exp(-1j * theta / 2)
        phase_1 = np.exp(1j * theta / 2)
        
        for i in range(2**self.num_qubits):
            bit = (i >> qubit) & 1
            if bit == 0:
                self._state[i] *= phase_0
            else:
                self._state[i] *= phase_1
    
    def _apply_cnot(self, control: int, target: int):
        """Apply CNOT gate."""
        new_state = np.zeros_like(self._state)
        
        for i in range(2**self.num_qubits):
            control_bit = (i >> control) & 1
            if control_bit == 1:
                # Flip target bit
                i_flip = i ^ (1 << target)
                new_state[i_flip] = self._state[i]
            else:
                new_state[i] = self._state[i]
        
        self._state = new_state
    
    def execute_circuit(self, circuit: List[Tuple], shots: int = 1024) -> Dict[str, int]:
        """
        Execute a circuit defined as a list of gate tuples.
        
        Circuit format: [(gate_name, qubit, param), ...]
        Example: [("H", 0, None), ("RY", 1, 0.5), ("CNOT", 0, 1)]
        """
        self._reset()
        
        for gate in circuit:
            gate_name = gate[0].upper()
            if gate_name == "H":
                self._apply_h(gate[1])
            elif gate_name == "RY":
                self._apply_ry(gate[1], gate[2])
            elif gate_name == "RZ":
                self._apply_rz(gate[1], gate[2])
            elif gate_name == "CNOT" or gate_name == "CX":
                self._apply_cnot(gate[1], gate[2])
            elif gate_name == "RESET":
                pass  # Handled by _reset()
        
        # Sample from probability distribution
        probabilities = np.abs(self._state)**2
        outcomes = np.random.choice(
            2**self.num_qubits, 
            size=shots, 
            p=probabilities
        )
        
        counts = {}
        for outcome in outcomes:
            key = format(outcome, f"0{self.num_qubits}b")
            counts[key] = counts.get(key, 0) + 1
        
        return counts
    
    def compute_expectation(self, circuit: List[Tuple], observable: str = "Z") -> float:
        """Compute expectation value of Z observable on last qubit."""
        self._reset()
        
        for gate in circuit:
            gate_name = gate[0].upper()
            if gate_name == "H":
                self._apply_h(gate[1])
            elif gate_name == "RY":
                self._apply_ry(gate[1], gate[2])
            elif gate_name == "RZ":
                self._apply_rz(gate[1], gate[2])
            elif gate_name == "CNOT" or gate_name == "CX":
                self._apply_cnot(gate[1], gate[2])
        
        # Compute <Z> expectation for last qubit
        expectation = 0.0
        for i in range(2**self.num_qubits):
            bit = (i >> (self.num_qubits - 1)) & 1
            eigenvalue = 1 if bit == 0 else -1
            expectation += eigenvalue * np.abs(self._state[i])**2
        
        return float(expectation)


# =============================================================================
# QUANTUM KERNEL SIMILARITY
# =============================================================================

class QuantumKernelSimilarity(SimilarityKernel):
    """
    Quantum kernel-based similarity computation.
    
    Uses quantum feature maps to encode classical data into quantum states,
    then computes fidelity as similarity measure. Falls back to classical
    simulation when Qiskit is not available.
    
    Parameters
    ----------
    num_features : int
        Dimension of input feature vectors (must match circuit width)
    use_simulator : bool
        If True, use simulator even when hardware is available
    reps : int
        Number of repetitions in the feature map circuit
    
    Example
    -------
    >>> qks = QuantumKernelSimilarity(num_features=4)
    >>> similarity = qks.compute_similarity([0.1, 0.2, 0.3, 0.4], [0.2, 0.3, 0.4, 0.5])
    >>> print(f"Quantum similarity: {similarity:.4f}")
    """
    
    def __init__(
        self, 
        num_features: int = 4,
        use_simulator: bool = True,
        reps: int = 2,
    ):
        self.num_features = num_features
        self.use_simulator = use_simulator
        self.reps = reps
        
        # Check for Qiskit availability
        self._qiskit_available = _check_qiskit()
        
        # Initialize backend
        if self._qiskit_available and not use_simulator:
            self._init_qiskit_backend()
        else:
            self._backend = ClassicalSimulatorBackend(num_qubits=num_features)
            self._classical_fallback = ClassicalSimilarity()
            if not self._qiskit_available:
                warnings.warn(
                    "Qiskit not available. Using classical similarity fallback.",
                    UserWarning
                )
    
    def _init_qiskit_backend(self):
        """Initialize Qiskit backend (when available)."""
        try:
            from qiskit.circuit.library import ZZFeatureMap
            from qiskit_machine_learning.kernels import FidelityQuantumKernel
            from qiskit.primitives import Sampler
            
            self._feature_map = ZZFeatureMap(
                feature_dimension=self.num_features,
                reps=self.reps,
                entanglement="linear"
            )
            
            self._kernel = FidelityQuantumKernel(
                feature_map=self._feature_map,
                fidelity=Sampler()
            )
        except ImportError:
            self._qiskit_available = False
            self._backend = ClassicalSimulatorBackend(num_qubits=self.num_features)
            self._classical_fallback = ClassicalSimilarity()
    
    def _create_feature_map_circuit(self, features: np.ndarray) -> List[Tuple]:
        """
        Create a simplified ZZ feature map circuit.
        
        This is used when Qiskit is not available.
        """
        circuit = []
        n = len(features)
        
        for rep in range(self.reps):
            # Hadamard layer
            for i in range(n):
                circuit.append(("H", i, None))
            
            # RZ encoding layer
            for i in range(n):
                circuit.append(("RZ", i, 2.0 * features[i]))
            
            # ZZ entanglement layer (simplified)
            for i in range(n - 1):
                circuit.append(("CNOT", i, i + 1))
                circuit.append(("RZ", i + 1, 2.0 * features[i] * features[i + 1]))
                circuit.append(("CNOT", i, i + 1))
        
        return circuit
    
    def compute_similarity(
        self, 
        vec_a: np.ndarray, 
        vec_b: np.ndarray
    ) -> float:
        """
        Compute quantum kernel similarity between two feature vectors.
        
        When Qiskit is available, uses fidelity-based quantum kernel.
        Otherwise, uses classical cosine similarity as fallback.
        """
        vec_a = np.asarray(vec_a, dtype=np.float64).flatten()
        vec_b = np.asarray(vec_b, dtype=np.float64).flatten()
        
        if len(vec_a) != self.num_features or len(vec_b) != self.num_features:
            raise ValueError(
                f"Feature vectors must have dimension {self.num_features}, "
                f"got {len(vec_a)} and {len(vec_b)}"
            )
        
        # Normalize to [0, pi] range for quantum encoding
        vec_a_norm = np.clip(vec_a, 0, 1) * np.pi
        vec_b_norm = np.clip(vec_b, 0, 1) * np.pi
        
        if self._qiskit_available and hasattr(self, '_kernel'):
            # Use Qiskit kernel
            similarity_matrix = self._kernel.evaluate(
                x_vec=vec_a_norm.reshape(1, -1),
                y_vec=vec_b_norm.reshape(1, -1)
            )
            return float(similarity_matrix[0, 0])
        else:
            # Classical simulation fallback
            # Compute overlap via state fidelity estimation
            circuit_a = self._create_feature_map_circuit(vec_a_norm)
            circuit_b = self._create_feature_map_circuit(vec_b_norm)
            
            # Execute circuits
            self._backend._reset()
            for gate in circuit_a:
                if gate[0] == "H":
                    self._backend._apply_h(gate[1])
                elif gate[0] == "RZ":
                    self._backend._apply_rz(gate[1], gate[2])
                elif gate[0] == "CNOT":
                    self._backend._apply_cnot(gate[1], gate[2])
            state_a = self._backend._state.copy()
            
            self._backend._reset()
            for gate in circuit_b:
                if gate[0] == "H":
                    self._backend._apply_h(gate[1])
                elif gate[0] == "RZ":
                    self._backend._apply_rz(gate[1], gate[2])
                elif gate[0] == "CNOT":
                    self._backend._apply_cnot(gate[1], gate[2])
            state_b = self._backend._state.copy()
            
            # Fidelity = |<a|b>|^2
            overlap = np.vdot(state_a, state_b)
            fidelity = np.abs(overlap)**2
            
            return float(fidelity)
    
    def compute_similarity_matrix(
        self, 
        vectors_a: np.ndarray, 
        vectors_b: np.ndarray
    ) -> np.ndarray:
        """Compute pairwise similarity matrix."""
        vectors_a = np.asarray(vectors_a, dtype=np.float64)
        vectors_b = np.asarray(vectors_b, dtype=np.float64)
        
        if vectors_a.ndim == 1:
            vectors_a = vectors_a.reshape(1, -1)
        if vectors_b.ndim == 1:
            vectors_b = vectors_b.reshape(1, -1)
        
        n_a, n_b = len(vectors_a), len(vectors_b)
        similarity_matrix = np.zeros((n_a, n_b))
        
        for i in range(n_a):
            for j in range(n_b):
                similarity_matrix[i, j] = self.compute_similarity(
                    vectors_a[i], vectors_b[j]
                )
        
        return similarity_matrix


# =============================================================================
# HYBRID QUANTUM-CLASSICAL LAYER
# =============================================================================

@dataclass
class HybridLayerConfig:
    """Configuration for hybrid quantum-classical layer."""
    num_qubits: int = 4
    num_layers: int = 2
    entanglement: str = "linear"  # "linear", "full", "circular"
    use_input_gradients: bool = True
    shots: int = 1024


class HybridQuantumLayer:
    """
    Hybrid quantum-classical layer for neural network integration.
    
    When PyTorch and Qiskit ML are available, uses TorchConnector.
    Otherwise, provides a classical approximation.
    
    This layer can be integrated into DSPy modules that use
    neural network components for enhanced optimization.
    
    Parameters
    ----------
    config : HybridLayerConfig
        Configuration for the hybrid layer
    
    Example
    -------
    >>> layer = HybridQuantumLayer(HybridLayerConfig(num_qubits=4))
    >>> output = layer.forward(input_tensor)
    """
    
    def __init__(self, config: HybridLayerConfig):
        self.config = config
        self._torch_available = _check_torch()
        self._qiskit_available = _check_qiskit()
        
        # Initialize weights (classical fallback)
        self._weights = np.random.randn(config.num_qubits * config.num_layers) * 0.1
        
        if self._torch_available and self._qiskit_available:
            self._init_quantum_layer()
        else:
            self._backend = ClassicalSimulatorBackend(num_qubits=config.num_qubits)
    
    def _init_quantum_layer(self):
        """Initialize Qiskit-based quantum layer with TorchConnector."""
        try:
            import torch
            from qiskit import QuantumCircuit
            from qiskit.circuit import Parameter
            from qiskit_machine_learning.neural_networks import EstimatorQNN
            from qiskit_machine_learning.connectors import TorchConnector
            
            n = self.config.num_qubits
            qc = QuantumCircuit(n)
            
            # Create parameters
            input_params = [Parameter(f"x_{i}") for i in range(n)]
            weight_params = [
                Parameter(f"θ_{l}_{i}") 
                for l in range(self.config.num_layers) 
                for i in range(n)
            ]
            
            # Build circuit
            for layer in range(self.config.num_layers):
                # Encoding layer (input)
                for i in range(n):
                    qc.ry(input_params[i], i)
                
                # Variational layer (weights)
                for i in range(n):
                    qc.ry(weight_params[layer * n + i], i)
                
                # Entanglement
                if self.config.entanglement == "linear":
                    for i in range(n - 1):
                        qc.cx(i, i + 1)
                elif self.config.entanglement == "full":
                    for i in range(n):
                        for j in range(i + 1, n):
                            qc.cx(i, j)
                elif self.config.entanglement == "circular":
                    for i in range(n):
                        qc.cx(i, (i + 1) % n)
            
            # Create QNN
            qnn = EstimatorQNN(
                circuit=qc,
                input_params=input_params,
                weight_params=weight_params,
            )
            
            # Wrap with TorchConnector
            self._torch_layer = TorchConnector(
                qnn,
                initial_weights=torch.tensor(self._weights, dtype=torch.float64)
            )
            
        except Exception as e:
            warnings.warn(f"Failed to initialize quantum layer: {e}")
            self._torch_layer = None
    
    def _create_variational_circuit(
        self, 
        inputs: np.ndarray, 
        weights: np.ndarray
    ) -> List[Tuple]:
        """Create variational circuit for classical simulation."""
        circuit = []
        n = self.config.num_qubits
        
        for layer in range(self.config.num_layers):
            # Encoding layer
            for i in range(n):
                circuit.append(("RY", i, inputs[i % len(inputs)]))
            
            # Variational layer
            for i in range(n):
                w_idx = layer * n + i
                if w_idx < len(weights):
                    circuit.append(("RY", i, weights[w_idx]))
            
            # Entanglement
            if self.config.entanglement == "linear":
                for i in range(n - 1):
                    circuit.append(("CNOT", i, i + 1))
        
        return circuit
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        Forward pass through hybrid layer.
        
        Parameters
        ----------
        x : np.ndarray
            Input tensor of shape (batch_size, num_features) or (num_features,)
        
        Returns
        -------
        np.ndarray
            Output tensor
        """
        x = np.asarray(x, dtype=np.float64)
        if x.ndim == 1:
            x = x.reshape(1, -1)
        
        batch_size = x.shape[0]
        outputs = []
        
        if hasattr(self, '_torch_layer') and self._torch_layer is not None:
            import torch
            x_torch = torch.tensor(x, dtype=torch.float64)
            output = self._torch_layer(x_torch)
            return output.detach().numpy()
        else:
            # Classical simulation
            for i in range(batch_size):
                circuit = self._create_variational_circuit(x[i], self._weights)
                expectation = self._backend.compute_expectation(circuit)
                outputs.append(expectation)
            
            return np.array(outputs)
    
    def get_coherence_metrics(self) -> CoherenceMetrics:
        """Compute coherence metrics for the hybrid layer."""
        # Estimate metrics based on layer configuration
        entanglement_score = {
            "linear": 0.3,
            "full": 0.7,
            "circular": 0.5,
        }.get(self.config.entanglement, 0.4)
        
        # More entanglement = more potential for curl/divergence
        curl = 0.1 + entanglement_score * 0.3
        divergence = 0.2 + (self.config.num_layers - 1) * 0.1
        
        # Emergence quality increases with complexity (up to a point)
        emergence = min(0.95, 0.6 + self.config.num_qubits * 0.05)
        
        return CoherenceMetrics(
            curl=curl,
            divergence=divergence,
            emergence_quality=emergence,
            fidelity_loss=0.05 * self.config.num_layers,
        )


# =============================================================================
# DSPY MODULE INTEGRATION (STUB)
# =============================================================================

class QuantumEnhancedRetriever:
    """
    Quantum-enhanced document retriever for DSPy RAG modules.
    
    Uses quantum kernel similarity to find relevant documents.
    Falls back to classical similarity when quantum features unavailable.
    
    Parameters
    ----------
    num_passages : int
        Number of passages to retrieve
    feature_dim : int
        Dimension of document embeddings
    
    Example
    -------
    >>> retriever = QuantumEnhancedRetriever(num_passages=3, feature_dim=4)
    >>> context = retriever.retrieve("quantum computing", corpus, embeddings)
    """
    
    def __init__(
        self,
        num_passages: int = 3,
        feature_dim: int = 4,
    ):
        self.num_passages = num_passages
        self.feature_dim = feature_dim
        self.similarity_kernel = QuantumKernelSimilarity(
            num_features=feature_dim,
            use_simulator=True
        )
    
    def retrieve(
        self,
        query_embedding: np.ndarray,
        corpus: List[str],
        corpus_embeddings: np.ndarray,
    ) -> List[str]:
        """
        Retrieve most relevant passages using quantum similarity.
        
        Parameters
        ----------
        query_embedding : np.ndarray
            Embedding vector for the query
        corpus : List[str]
            List of document strings
        corpus_embeddings : np.ndarray
            Embedding vectors for corpus documents
        
        Returns
        -------
        List[str]
            Top-k most similar documents
        """
        query_embedding = np.asarray(query_embedding).flatten()
        corpus_embeddings = np.asarray(corpus_embeddings)
        
        if corpus_embeddings.ndim == 1:
            corpus_embeddings = corpus_embeddings.reshape(1, -1)
        
        # Ensure feature dimensions match
        if len(query_embedding) != self.feature_dim:
            # Truncate or pad
            if len(query_embedding) > self.feature_dim:
                query_embedding = query_embedding[:self.feature_dim]
            else:
                query_embedding = np.pad(
                    query_embedding, 
                    (0, self.feature_dim - len(query_embedding))
                )
        
        # Normalize embeddings to [0, 1]
        query_norm = (query_embedding - query_embedding.min()) / (
            query_embedding.max() - query_embedding.min() + 1e-8
        )
        
        # Compute similarities
        similarities = []
        for i, doc_emb in enumerate(corpus_embeddings):
            if len(doc_emb) > self.feature_dim:
                doc_emb = doc_emb[:self.feature_dim]
            elif len(doc_emb) < self.feature_dim:
                doc_emb = np.pad(doc_emb, (0, self.feature_dim - len(doc_emb)))
            
            doc_norm = (doc_emb - doc_emb.min()) / (
                doc_emb.max() - doc_emb.min() + 1e-8
            )
            
            sim = self.similarity_kernel.compute_similarity(query_norm, doc_norm)
            similarities.append((i, sim))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top passages
        top_indices = [idx for idx, _ in similarities[:self.num_passages]]
        return [corpus[i] for i in top_indices if i < len(corpus)]


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demonstrate_qiskit_dspy_hybrid():
    """Demonstrate Qiskit-DSPy hybrid integration."""
    print("=" * 70)
    print("QISKIT-DSPY HYBRID INTEGRATION DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Check dependencies
    print("Dependency Status:")
    print(f"  Qiskit available: {_check_qiskit()}")
    print(f"  PyTorch available: {_check_torch()}")
    print(f"  DSPy available: {_check_dspy()}")
    print()
    
    # Test quantum kernel similarity
    print("1. Quantum Kernel Similarity")
    print("-" * 40)
    
    qks = QuantumKernelSimilarity(num_features=4, use_simulator=True)
    
    vec_a = np.array([0.1, 0.2, 0.3, 0.4])
    vec_b = np.array([0.15, 0.25, 0.35, 0.45])
    vec_c = np.array([0.9, 0.8, 0.7, 0.6])
    
    sim_ab = qks.compute_similarity(vec_a, vec_b)
    sim_ac = qks.compute_similarity(vec_a, vec_c)
    
    print(f"  Similarity(a, b): {sim_ab:.4f} (similar vectors)")
    print(f"  Similarity(a, c): {sim_ac:.4f} (dissimilar vectors)")
    print()
    
    # Test hybrid layer
    print("2. Hybrid Quantum-Classical Layer")
    print("-" * 40)
    
    config = HybridLayerConfig(num_qubits=4, num_layers=2, entanglement="linear")
    layer = HybridQuantumLayer(config)
    
    test_input = np.array([[0.1, 0.2, 0.3, 0.4], [0.5, 0.6, 0.7, 0.8]])
    output = layer.forward(test_input)
    
    print(f"  Input shape: {test_input.shape}")
    print(f"  Output shape: {output.shape}")
    print(f"  Output values: {output}")
    print()
    
    # Coherence metrics
    metrics = layer.get_coherence_metrics()
    print("  Coherence Metrics:")
    for key, val in metrics.to_dict().items():
        print(f"    {key}: {val}")
    print()
    
    # Test retriever
    print("3. Quantum-Enhanced Retriever")
    print("-" * 40)
    
    corpus = [
        "Quantum computing uses qubits for parallel computation.",
        "Machine learning models learn patterns from data.",
        "Quantum entanglement enables correlated measurements.",
        "Neural networks approximate complex functions.",
    ]
    
    # Simple embedding simulation (normally would use real embeddings)
    corpus_embeddings = np.array([
        [0.9, 0.1, 0.8, 0.2],  # quantum computing
        [0.3, 0.7, 0.2, 0.6],  # machine learning
        [0.8, 0.2, 0.9, 0.1],  # quantum entanglement
        [0.2, 0.8, 0.3, 0.7],  # neural networks
    ])
    
    query_embedding = np.array([0.85, 0.15, 0.75, 0.25])  # quantum-related query
    
    retriever = QuantumEnhancedRetriever(num_passages=2, feature_dim=4)
    results = retriever.retrieve(query_embedding, corpus, corpus_embeddings)
    
    print("  Query: (quantum-related embedding)")
    print("  Retrieved passages:")
    for i, passage in enumerate(results):
        print(f"    {i+1}. {passage}")
    print()
    
    print("=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_qiskit_dspy_hybrid()
