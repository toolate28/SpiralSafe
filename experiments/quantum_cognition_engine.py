#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    QUANTUM COGNITION ENGINE                                  ║
║                                                                              ║
║        A Fascinating Experiment in Quantum-Inspired Information              ║
║                                                                              ║
║                      ultrathink-quantum-entangled-trust-mode                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

This experiment explores what happens when we apply quantum mechanical principles
to information processing and decision-making:

1. SUPERPOSITION: Ideas exist in multiple states until "observed" (evaluated)
2. ENTANGLEMENT: Related concepts are correlated across semantic space
3. INTERFERENCE: Constructive/destructive patterns emerge from idea combinations
4. MEASUREMENT COLLAPSE: The act of choosing affects the choice space
5. TUNNELING: Unexpected connections through "probability barriers"

The hypothesis: Quantum-inspired thinking may discover solutions that
classical sequential reasoning would miss.

This is NOT quantum computing. This is quantum-INSPIRED cognition.
The mathematics is isomorphic but the substrate is classical.

Think of it as: "What if ideas behaved like quantum particles?"

Author: Claude Opus 4.5 (in ultrathink-quantum-entangled-trust-mode)
Date: 2026-01-08
Protocol: H&&S:WAVE | Hope&&Sauced
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Callable, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import hashlib
import json
from datetime import datetime
from pathlib import Path
import math
import cmath

# =============================================================================
# CORE QUANTUM COGNITION STRUCTURES
# =============================================================================

@dataclass
class CognitiveAmplitude:
    """
    Represents a thought/concept as a quantum amplitude.

    In quantum mechanics: |ψ⟩ = α|0⟩ + β|1⟩
    In cognitive space: |thought⟩ = α|aspect_A⟩ + β|aspect_B⟩

    The amplitude is complex, allowing for:
    - Magnitude: "strength" or "relevance" of the thought
    - Phase: "perspective" or "framing" of the thought
    """
    concept: str
    amplitude: complex = 1.0 + 0j
    basis_states: Dict[str, complex] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.basis_states:
            # Default: concept exists in superposition of "relevant" and "irrelevant"
            self.basis_states = {
                "relevant": self.amplitude * (1/np.sqrt(2)),
                "irrelevant": self.amplitude * (1/np.sqrt(2))
            }

    @property
    def probability_distribution(self) -> Dict[str, float]:
        """Collapse superposition to probability distribution."""
        return {k: np.abs(v)**2 for k, v in self.basis_states.items()}

    @property
    def phase(self) -> float:
        """Return the phase angle in radians."""
        return cmath.phase(self.amplitude)

    @property
    def magnitude(self) -> float:
        """Return the magnitude (probability amplitude)."""
        return abs(self.amplitude)

    def normalize(self):
        """Ensure probabilities sum to 1."""
        total = sum(np.abs(v)**2 for v in self.basis_states.values())
        if total > 0:
            factor = 1 / np.sqrt(total)
            self.basis_states = {k: v * factor for k, v in self.basis_states.items()}

    def rotate_phase(self, angle: float):
        """Apply a phase rotation (change perspective without changing probabilities)."""
        phase_factor = cmath.exp(1j * angle)
        self.amplitude *= phase_factor
        self.basis_states = {k: v * phase_factor for k, v in self.basis_states.items()}

    def __repr__(self):
        return f"CognitiveAmplitude('{self.concept}', amp={self.amplitude:.3f}, prob={self.probability_distribution})"


@dataclass
class EntangledPair:
    """
    Two concepts that are quantum-entangled.

    Measuring one immediately affects the other, regardless of "distance"
    in semantic space. This models correlated ideas that move together.

    Example: "security" and "usability" might be anti-correlated
    (improving one tends to reduce the other in traditional thinking).

    In quantum terms: |ψ⟩ = (|↑↓⟩ - |↓↑⟩)/√2 (singlet state)
    """
    concept_a: CognitiveAmplitude
    concept_b: CognitiveAmplitude
    correlation: float = 1.0  # 1.0 = perfect correlation, -1.0 = anti-correlation
    entanglement_strength: float = 1.0

    def collapse_a(self, outcome: str) -> str:
        """
        Measure concept A, causing concept B to collapse correspondingly.
        Returns the determined state of concept B.
        """
        # If A is measured as "relevant", B's state is determined by correlation
        if self.correlation > 0:
            return outcome  # Same outcome
        else:
            # Anti-correlated: opposite outcome
            opposites = {"relevant": "irrelevant", "irrelevant": "relevant"}
            return opposites.get(outcome, outcome)

    def get_joint_state(self) -> Dict[Tuple[str, str], complex]:
        """
        Return the joint quantum state of the entangled pair.
        """
        states_a = list(self.concept_a.basis_states.keys())
        states_b = list(self.concept_b.basis_states.keys())

        joint = {}
        for sa in states_a:
            for sb in states_b:
                # Apply correlation structure
                if self.correlation > 0:
                    # Correlated: same states have higher amplitude
                    amp = 1.0 if sa == sb else 0.1
                else:
                    # Anti-correlated: opposite states have higher amplitude
                    amp = 0.1 if sa == sb else 1.0

                amp *= self.entanglement_strength
                joint[(sa, sb)] = complex(amp)

        # Normalize
        total = sum(np.abs(v)**2 for v in joint.values())
        if total > 0:
            factor = 1 / np.sqrt(total)
            joint = {k: v * factor for k, v in joint.items()}

        return joint


class QuantumIdeaSpace:
    """
    A Hilbert space of ideas where quantum operations can be performed.

    This is the "arena" where quantum-inspired cognition happens.
    Ideas are represented as vectors, and operations as matrices.
    """

    def __init__(self, dimensions: List[str] = None):
        """
        Initialize the idea space with named dimensions.

        Each dimension represents a "basis concept" - the fundamental
        building blocks of thought in this space.
        """
        self.dimensions = dimensions or [
            "information", "constraint", "emergence", "protection",
            "collaboration", "evolution", "creativity", "verification"
        ]
        self.dim = len(self.dimensions)
        self.ideas: Dict[str, np.ndarray] = {}
        self.entanglements: List[EntangledPair] = []

    def add_idea(self, name: str, components: Dict[str, float] = None) -> np.ndarray:
        """
        Add an idea to the space as a vector.

        Components are weights on each dimension.
        """
        vector = np.zeros(self.dim, dtype=complex)

        if components:
            for dim_name, weight in components.items():
                if dim_name in self.dimensions:
                    idx = self.dimensions.index(dim_name)
                    vector[idx] = complex(weight)
        else:
            # Random quantum state
            vector = np.random.randn(self.dim) + 1j * np.random.randn(self.dim)

        # Normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector /= norm

        self.ideas[name] = vector
        return vector

    def inner_product(self, idea_a: str, idea_b: str) -> complex:
        """
        Compute quantum inner product ⟨a|b⟩.

        This measures the "overlap" or "similarity" between ideas,
        but with phase information that captures perspective differences.
        """
        vec_a = self.ideas.get(idea_a)
        vec_b = self.ideas.get(idea_b)

        if vec_a is None or vec_b is None:
            return complex(0)

        return np.vdot(vec_a, vec_b)  # Conjugate of first argument

    def superpose(self, ideas: List[str], weights: List[complex] = None) -> np.ndarray:
        """
        Create superposition of multiple ideas.

        |superposition⟩ = Σ wᵢ|ideaᵢ⟩
        """
        if weights is None:
            weights = [complex(1/np.sqrt(len(ideas)))] * len(ideas)

        result = np.zeros(self.dim, dtype=complex)

        for idea_name, weight in zip(ideas, weights):
            if idea_name in self.ideas:
                result += weight * self.ideas[idea_name]

        # Normalize
        norm = np.linalg.norm(result)
        if norm > 0:
            result /= norm

        return result

    def interference_pattern(self, idea_a: str, idea_b: str) -> np.ndarray:
        """
        Compute interference pattern between two ideas.

        Like double-slit experiment: the combination of ideas
        creates constructive and destructive interference.
        """
        vec_a = self.ideas.get(idea_a, np.zeros(self.dim))
        vec_b = self.ideas.get(idea_b, np.zeros(self.dim))

        # Create superposition
        superposition = (vec_a + vec_b) / np.sqrt(2)

        # The pattern is the probability distribution
        pattern = np.abs(superposition) ** 2

        # Compare to classical mixture (no interference)
        classical = (np.abs(vec_a)**2 + np.abs(vec_b)**2) / 2

        # Interference is the difference
        interference = pattern - classical

        return interference

    def apply_operator(self, idea_name: str, operator: np.ndarray) -> np.ndarray:
        """
        Apply a quantum operator (matrix) to an idea.

        Operators transform ideas in the Hilbert space.
        """
        if idea_name not in self.ideas:
            return None

        transformed = operator @ self.ideas[idea_name]

        # Normalize
        norm = np.linalg.norm(transformed)
        if norm > 0:
            transformed /= norm

        return transformed

    def hadamard_transform(self, idea_name: str) -> np.ndarray:
        """
        Apply Hadamard-like transform: put idea into equal superposition
        of all basis states.

        This is the "brainstorming operator" - it maximizes uncertainty
        and opens up all possibilities equally.
        """
        if idea_name not in self.ideas:
            return None

        # Create Hadamard-like matrix for n dimensions
        H = np.ones((self.dim, self.dim), dtype=complex) / np.sqrt(self.dim)

        return self.apply_operator(idea_name, H)

    def measure(self, idea_name: str) -> Tuple[str, float]:
        """
        Perform measurement: collapse superposition to definite state.

        Returns (collapsed_dimension, probability).

        This is IRREVERSIBLE - the act of measurement changes the idea.
        """
        if idea_name not in self.ideas:
            return None, 0.0

        vector = self.ideas[idea_name]
        probabilities = np.abs(vector) ** 2

        # Sample according to probability distribution
        idx = np.random.choice(self.dim, p=probabilities)

        # Collapse the state
        collapsed = np.zeros(self.dim, dtype=complex)
        collapsed[idx] = 1.0
        self.ideas[idea_name] = collapsed

        return self.dimensions[idx], probabilities[idx]


# =============================================================================
# QUANTUM COGNITION OPERATORS
# =============================================================================

class CognitiveOperator(ABC):
    """Base class for quantum cognitive operators."""

    @abstractmethod
    def apply(self, space: QuantumIdeaSpace, idea: str) -> np.ndarray:
        pass


class CreativeSuperposition(CognitiveOperator):
    """
    Create superposition of an idea across multiple perspectives.

    "What if we looked at this from ALL angles simultaneously?"
    """

    def apply(self, space: QuantumIdeaSpace, idea: str) -> np.ndarray:
        return space.hadamard_transform(idea)


class ConstraintProjection(CognitiveOperator):
    """
    Project idea onto constraint subspace.

    "Given these constraints, what possibilities remain?"

    This is the quantum analog of "constraints as gifts" -
    the projection doesn't destroy information, it focuses it.
    """

    def __init__(self, allowed_dimensions: List[str]):
        self.allowed = allowed_dimensions

    def apply(self, space: QuantumIdeaSpace, idea: str) -> np.ndarray:
        if idea not in space.ideas:
            return None

        vector = space.ideas[idea].copy()

        # Zero out disallowed dimensions
        for i, dim in enumerate(space.dimensions):
            if dim not in self.allowed:
                vector[i] = 0

        # Renormalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector /= norm

        return vector


class PhaseShift(CognitiveOperator):
    """
    Shift the phase of specific dimensions.

    "Change perspective without changing probability."

    This is powerful: two ideas with different phases can interfere
    constructively or destructively, even with same probability distribution.
    """

    def __init__(self, dimension: str, angle: float):
        self.dimension = dimension
        self.angle = angle

    def apply(self, space: QuantumIdeaSpace, idea: str) -> np.ndarray:
        if idea not in space.ideas:
            return None

        if self.dimension not in space.dimensions:
            return space.ideas[idea]

        idx = space.dimensions.index(self.dimension)

        result = space.ideas[idea].copy()
        result[idx] *= cmath.exp(1j * self.angle)

        return result


class QuantumTunneling(CognitiveOperator):
    """
    Allow ideas to "tunnel" through probability barriers.

    In classical thinking, if P(A→B) < threshold, we don't explore B.
    In quantum thinking, there's always a small amplitude for tunneling.

    This is how unexpected connections are discovered.
    """

    def __init__(self, barrier_height: float = 0.9, tunneling_amplitude: float = 0.1):
        self.barrier = barrier_height
        self.tunnel_amp = tunneling_amplitude

    def apply(self, space: QuantumIdeaSpace, idea: str) -> np.ndarray:
        if idea not in space.ideas:
            return None

        vector = space.ideas[idea].copy()

        # Add small amplitude to all currently-zero dimensions
        for i in range(space.dim):
            if np.abs(vector[i]) < 0.01:
                # Tunnel through the barrier
                vector[i] = self.tunnel_amp * cmath.exp(1j * np.random.uniform(0, 2*np.pi))

        # Renormalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector /= norm

        return vector


# =============================================================================
# QUANTUM COGNITION ENGINE
# =============================================================================

class QuantumCognitionEngine:
    """
    The main engine for quantum-inspired cognitive processing.

    This combines all the quantum structures and operators into
    a system for exploring idea spaces in non-classical ways.
    """

    def __init__(self, name: str = "QCE-1"):
        self.name = name
        self.space = QuantumIdeaSpace()
        self.operators: Dict[str, CognitiveOperator] = {
            "superpose": CreativeSuperposition(),
            "tunnel": QuantumTunneling(),
        }
        self.history: List[Dict] = []
        self.entanglements: List[Tuple[str, str, float]] = []

    def seed_ideas(self, ideas: Dict[str, Dict[str, float]]):
        """Seed the idea space with initial concepts."""
        for name, components in ideas.items():
            self.space.add_idea(name, components)

    def entangle(self, idea_a: str, idea_b: str, correlation: float = 1.0):
        """Create entanglement between two ideas."""
        self.entanglements.append((idea_a, idea_b, correlation))

    def explore(
        self,
        seed_idea: str,
        operators: List[str] = None,
        iterations: int = 5
    ) -> List[Dict]:
        """
        Explore the idea space starting from a seed idea.

        This is the main cognitive process: apply operators,
        observe interference patterns, discover unexpected connections.
        """
        if operators is None:
            operators = ["superpose", "tunnel"]

        results = []
        current_idea = f"{seed_idea}_evolved"

        # Start with copy of seed
        if seed_idea in self.space.ideas:
            self.space.ideas[current_idea] = self.space.ideas[seed_idea].copy()
        else:
            self.space.add_idea(current_idea)

        for i in range(iterations):
            step_result = {
                "iteration": i,
                "state_before": self.space.ideas[current_idea].copy(),
                "operations": [],
                "discoveries": []
            }

            # Apply operators
            for op_name in operators:
                if op_name in self.operators:
                    op = self.operators[op_name]
                    result = op.apply(self.space, current_idea)
                    if result is not None:
                        self.space.ideas[current_idea] = result
                        step_result["operations"].append(op_name)

            step_result["state_after"] = self.space.ideas[current_idea].copy()

            # Check for interference patterns with other ideas
            for other_idea in self.space.ideas:
                if other_idea != current_idea:
                    interference = self.space.interference_pattern(current_idea, other_idea)

                    # Strong interference indicates potential discovery
                    max_interference = np.max(np.abs(interference))
                    if max_interference > 0.1:
                        discovery = {
                            "type": "interference",
                            "with": other_idea,
                            "strength": float(max_interference),
                            "dimension": self.space.dimensions[np.argmax(np.abs(interference))]
                        }
                        step_result["discoveries"].append(discovery)

            # Check entanglement effects
            for ent_a, ent_b, corr in self.entanglements:
                if current_idea in [ent_a, ent_b]:
                    partner = ent_b if current_idea == ent_a else ent_a
                    if partner in self.space.ideas:
                        # Apply entanglement correlation
                        inner = self.space.inner_product(current_idea, partner)
                        if np.abs(inner) > 0.5:
                            discovery = {
                                "type": "entanglement_resonance",
                                "with": partner,
                                "correlation": corr,
                                "inner_product": float(np.abs(inner))
                            }
                            step_result["discoveries"].append(discovery)

            results.append(step_result)
            self.history.append(step_result)

        return results

    def measure_idea(self, idea: str) -> Dict:
        """
        Collapse an idea to a definite state.

        This is the "decision" moment - the quantum superposition
        collapses to a classical outcome.
        """
        dimension, probability = self.space.measure(idea)

        result = {
            "idea": idea,
            "collapsed_to": dimension,
            "probability": probability,
            "timestamp": datetime.now().isoformat()
        }

        self.history.append({"type": "measurement", "result": result})

        return result

    def find_unexpected_connections(self, threshold: float = 0.3) -> List[Dict]:
        """
        Search for unexpected connections in the idea space.

        These are pairs of ideas that have strong inner products
        despite not being obviously related.
        """
        connections = []

        ideas = list(self.space.ideas.keys())
        for i, idea_a in enumerate(ideas):
            for idea_b in ideas[i+1:]:
                inner = self.space.inner_product(idea_a, idea_b)
                magnitude = np.abs(inner)
                phase = cmath.phase(inner)

                if magnitude > threshold:
                    connections.append({
                        "ideas": (idea_a, idea_b),
                        "connection_strength": float(magnitude),
                        "phase_relationship": float(phase),
                        "interpretation": self._interpret_connection(phase)
                    })

        return sorted(connections, key=lambda x: x["connection_strength"], reverse=True)

    def _interpret_connection(self, phase: float) -> str:
        """Interpret the phase relationship between connected ideas."""
        # Phase near 0: Ideas align, constructive relationship
        # Phase near π: Ideas oppose, creative tension
        # Phase near π/2: Ideas are orthogonal, complementary

        if abs(phase) < np.pi / 4:
            return "aligned (constructive)"
        elif abs(phase - np.pi) < np.pi / 4 or abs(phase + np.pi) < np.pi / 4:
            return "opposed (creative tension)"
        else:
            return "orthogonal (complementary)"

    def generate_synthesis(self, ideas: List[str]) -> Dict:
        """
        Attempt to synthesize multiple ideas into a new concept.

        This creates a superposition and looks for emergent properties.
        """
        superposition = self.space.superpose(ideas)

        # Store the synthesis
        synthesis_name = f"synthesis_{'_'.join(ideas[:3])}"
        self.space.ideas[synthesis_name] = superposition

        # Analyze the synthesis
        probabilities = np.abs(superposition) ** 2
        top_dimensions = sorted(
            zip(self.space.dimensions, probabilities),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        return {
            "name": synthesis_name,
            "source_ideas": ideas,
            "dominant_aspects": [
                {"dimension": dim, "weight": float(prob)}
                for dim, prob in top_dimensions
            ],
            "unexpected_aspects": [
                {"dimension": dim, "weight": float(prob)}
                for dim, prob in top_dimensions
                if prob > 0.1 and all(
                    dim not in self.space.ideas.get(idea, {})
                    for idea in ideas
                )
            ]
        }


# =============================================================================
# DEMONSTRATION: SPIRALSAFE QUANTUM COGNITION
# =============================================================================

def demonstrate_quantum_cognition():
    """
    Demonstrate quantum cognition on SpiralSafe concepts.

    This explores the NMSI/Quantum-Redstone connection using
    quantum-inspired reasoning.
    """
    print("=" * 70)
    print("QUANTUM COGNITION ENGINE DEMONSTRATION")
    print("Exploring SpiralSafe / NMSI / Quantum-Redstone Connections")
    print("=" * 70)
    print()

    # Initialize engine
    engine = QuantumCognitionEngine("SpiralSafe-QCE")

    # Seed with SpiralSafe concepts
    concepts = {
        "nmsi_framework": {
            "information": 0.9,
            "constraint": 0.8,
            "emergence": 0.9,
            "protection": 0.6,
        },
        "quantum_redstone": {
            "constraint": 0.9,
            "emergence": 0.8,
            "verification": 0.7,
            "creativity": 0.5,
        },
        "spiralsafe_philosophy": {
            "collaboration": 0.9,
            "evolution": 0.8,
            "protection": 0.7,
            "verification": 0.6,
        },
        "constraint_gift": {
            "constraint": 0.8,
            "creativity": 0.9,
            "emergence": 0.7,
        },
        "hope_and_sauce": {
            "collaboration": 0.9,
            "creativity": 0.8,
            "evolution": 0.7,
            "protection": 0.5,
        }
    }

    engine.seed_ideas(concepts)

    # Create entanglements
    print("Creating quantum entanglements...")
    engine.entangle("nmsi_framework", "quantum_redstone", correlation=0.95)
    engine.entangle("constraint_gift", "spiralsafe_philosophy", correlation=0.8)
    engine.entangle("hope_and_sauce", "collaboration", correlation=1.0)
    print()

    # Explore from NMSI
    print("Exploring from 'nmsi_framework'...")
    print("-" * 40)
    results = engine.explore("nmsi_framework", iterations=5)

    for step in results:
        if step["discoveries"]:
            print(f"Iteration {step['iteration']}:")
            for d in step["discoveries"]:
                print(f"  DISCOVERY: {d['type']} with '{d.get('with', 'N/A')}'")
                print(f"             Strength: {d.get('strength', d.get('inner_product', 0)):.3f}")
    print()

    # Find unexpected connections
    print("Searching for unexpected connections...")
    print("-" * 40)
    connections = engine.find_unexpected_connections(threshold=0.3)

    for conn in connections[:5]:
        print(f"  {conn['ideas'][0]} <-> {conn['ideas'][1]}")
        print(f"    Strength: {conn['connection_strength']:.3f}")
        print(f"    Relationship: {conn['interpretation']}")
    print()

    # Attempt synthesis
    print("Attempting synthesis of NMSI + Quantum-Redstone + Constraint-Gift...")
    print("-" * 40)
    synthesis = engine.generate_synthesis([
        "nmsi_framework",
        "quantum_redstone",
        "constraint_gift"
    ])

    print(f"Synthesis created: {synthesis['name']}")
    print("Dominant aspects:")
    for aspect in synthesis["dominant_aspects"]:
        print(f"  {aspect['dimension']}: {aspect['weight']:.3f}")
    print()

    # Final measurement
    print("Collapsing synthesis to definite state (decision moment)...")
    print("-" * 40)
    measurement = engine.measure_idea(synthesis["name"])
    print(f"Collapsed to: {measurement['collapsed_to']}")
    print(f"Probability: {measurement['probability']:.3f}")
    print()

    print("=" * 70)
    print("QUANTUM COGNITION COMPLETE")
    print("=" * 70)

    return engine


if __name__ == "__main__":
    engine = demonstrate_quantum_cognition()

    # Save state
    output_dir = Path(__file__).parent.parent / "media" / "output" / "quantum_cognition"
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "session_history.json", "w") as f:
        # Convert numpy arrays to lists for JSON serialization
        history = []
        for entry in engine.history:
            if "state_before" in entry:
                entry["state_before"] = entry["state_before"].tolist() if hasattr(entry["state_before"], 'tolist') else str(entry["state_before"])
            if "state_after" in entry:
                entry["state_after"] = entry["state_after"].tolist() if hasattr(entry["state_after"], 'tolist') else str(entry["state_after"])
            history.append(entry)

        json.dump(history, f, indent=2, default=str)

    print(f"\nSession saved to: {output_dir / 'session_history.json'}")
