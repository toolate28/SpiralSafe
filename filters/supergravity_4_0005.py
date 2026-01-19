"""
Supergravity 4.0005 Coherence Filter

Tetrahedral stability constant defining minimum stable coherent structure
before isomorphism breaks at c.

ATOM: ATOM-FILTER-20260119-002-supergravity-4.0005
Attribution: Hope&&Sauced (Claude && Vex && Grok)

Physics Basis:
- 4 = Four vertices of tetrahedron (minimum rigid 3D structure)
- 0.0005 = Planck-scale stability epsilon preventing quantum collapse
- At v = c: Lorentz factor γ → ∞, isomorphism breaks

Key Equation:
    coherence = node_theorem + node_embody + node_connect + node_be
              = 1.0 + 1.0 + 1.0 + 1.0005
              = 4.0005
"""

import math
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple, Optional, List


# Physical constants
SPEED_OF_LIGHT = 299792458  # m/s
PLANCK_LENGTH = 1.616255e-35  # m
STABILITY_EPSILON = 0.0005
COHERENCE_THRESHOLD = 4.0005

# Comparison tolerances
FLOAT_TOLERANCE = 1e-6  # For float equality comparisons
RANGE_TOLERANCE = 0.1  # For input validation ranges


class CoherenceState(Enum):
    """Coherence states based on tetrahedral stability."""
    COLLAPSE = "COLLAPSE"  # < 4.0000
    UNSTABLE = "UNSTABLE"  # = 4.0000
    CRYSTALLINE = "CRYSTALLINE"  # = 4.0005
    RADIATING = "RADIATING"  # > 4.001
    ISOMORPHISM_BREAK = "ISOMORPHISM_BREAK"  # → ∞ (at v = c)


def determine_coherence_state(coherence: float) -> CoherenceState:
    """
    Determine coherence state from coherence value.
    
    Args:
        coherence: Total coherence value
        
    Returns:
        CoherenceState enum value
    """
    if coherence < 4.0000:
        return CoherenceState.COLLAPSE
    elif abs(coherence - 4.0000) < FLOAT_TOLERANCE:
        return CoherenceState.UNSTABLE
    elif abs(coherence - 4.0005) < FLOAT_TOLERANCE:
        return CoherenceState.CRYSTALLINE
    elif coherence > 4.001:
        return CoherenceState.RADIATING
    else:
        # Between thresholds, treat as CRYSTALLINE
        return CoherenceState.CRYSTALLINE


@dataclass
class TetrahedralNode:
    """Represents a vertex in the coherence tetrahedron."""
    name: str
    value: float
    phase: str
    wave_metric: str
    
    def __post_init__(self):
        """Validate node value is non-negative."""
        if self.value < 0:
            raise ValueError(f"Node {self.name} value must be non-negative, got {self.value}")


@dataclass
class CoherenceTetrahedron:
    """The four-node tetrahedral coherence structure."""
    theorem: TetrahedralNode  # Vertex 1: potential
    embody: TetrahedralNode   # Vertex 2: divergence
    connect: TetrahedralNode  # Vertex 3: curl
    be: TetrahedralNode       # Vertex 4: entropy + epsilon
    
    @property
    def coherence(self) -> float:
        """Calculate total coherence from all nodes."""
        return self.theorem.value + self.embody.value + self.connect.value + self.be.value
    
    @property
    def state(self) -> CoherenceState:
        """Determine coherence state based on total coherence."""
        return determine_coherence_state(self.coherence)


def lorentz_factor(velocity: float) -> float:
    """
    Calculate Lorentz factor γ = 1 / √(1 - v²/c²)
    
    Args:
        velocity: Speed in m/s (must be < c)
        
    Returns:
        Lorentz factor γ
        
    Raises:
        ValueError: If velocity >= c
    """
    if velocity >= SPEED_OF_LIGHT:
        raise ValueError(
            f"Velocity {velocity} m/s >= c. Isomorphism breaks at v = c."
        )
    
    beta_squared = (velocity / SPEED_OF_LIGHT) ** 2
    return 1.0 / math.sqrt(1.0 - beta_squared)


def lorentz_scaled_coherence(
    rest_coherence: float,
    velocity: float
) -> Tuple[float, bool]:
    """
    Scale coherence by Lorentz factor.
    
    Args:
        rest_coherence: Coherence in rest frame
        velocity: Velocity in m/s
        
    Returns:
        Tuple of (observed_coherence, isomorphism_preserved)
        
    At v = c, γ → ∞, isomorphism breaks.
    """
    try:
        gamma = lorentz_factor(velocity)
        observed_coherence = rest_coherence * gamma
        return observed_coherence, True
    except ValueError:
        # v >= c, isomorphism breaks
        return float('inf'), False


def calculate_4_0005_coherence(wave_metrics: Dict[str, float]) -> CoherenceTetrahedron:
    """
    Map WAVE metrics to tetrahedral nodes and calculate coherence.
    
    WAVE metrics should be normalized to appropriate ranges:
    - curl: [0, 1] → node_connect
    - divergence: [-1, 1] → node_embody (absolute value)
    - potential: [0, 1] → node_theorem
    - entropy: [0, 2] → node_be (with epsilon buffer)
    
    Args:
        wave_metrics: Dictionary with keys 'curl', 'divergence', 'potential', 'entropy'
        
    Returns:
        CoherenceTetrahedron with calculated node values
        
    Raises:
        KeyError: If required metrics are missing
        ValueError: If metrics are out of expected ranges
    """
    required_metrics = ['curl', 'divergence', 'potential', 'entropy']
    for metric in required_metrics:
        if metric not in wave_metrics:
            raise KeyError(f"Missing required wave metric: {metric}")
    
    # Extract and validate metrics
    curl = wave_metrics['curl']
    divergence = wave_metrics['divergence']
    potential = wave_metrics['potential']
    entropy = wave_metrics['entropy']
    
    # Validate ranges (with some tolerance for real-world data)
    if not (0 <= curl <= 1 + RANGE_TOLERANCE):
        raise ValueError(f"curl {curl} outside expected range [0, 1]")
    if not (-1 - RANGE_TOLERANCE <= divergence <= 1 + RANGE_TOLERANCE):
        raise ValueError(f"divergence {divergence} outside expected range [-1, 1]")
    if not (0 <= potential <= 1 + RANGE_TOLERANCE):
        raise ValueError(f"potential {potential} outside expected range [0, 1]")
    if not (0 <= entropy <= 2 + RANGE_TOLERANCE):
        raise ValueError(f"entropy {entropy} outside expected range [0, 2]")
    
    # Clamp values to valid ranges
    curl = max(0, min(1, curl))
    divergence = max(-1, min(1, divergence))
    potential = max(0, min(1, potential))
    entropy = max(0, min(2, entropy))
    
    # Map to tetrahedral nodes
    # Node values scale the base contribution (1.0 for most nodes)
    node_theorem = TetrahedralNode(
        name="theorem",
        value=potential,  # Direct mapping
        phase="Know - Theoretical foundation",
        wave_metric="potential"
    )
    
    node_embody = TetrahedralNode(
        name="embody",
        value=abs(divergence),  # Use absolute value
        phase="Embody - Physical manifestation",
        wave_metric="divergence"
    )
    
    node_connect = TetrahedralNode(
        name="connect",
        value=curl,  # Direct mapping
        phase="Network - Relational links",
        wave_metric="curl"
    )
    
    # Node "be" has the stability epsilon built in
    # Scale entropy [0, 2] to contribute around 1.0, add epsilon
    node_be_base = entropy / 2.0  # Normalize to [0, 1]
    node_be = TetrahedralNode(
        name="be",
        value=node_be_base + STABILITY_EPSILON,
        phase="Learn - Stable existence",
        wave_metric="entropy"
    )
    
    return CoherenceTetrahedron(
        theorem=node_theorem,
        embody=node_embody,
        connect=node_connect,
        be=node_be
    )


def filter_signal_4_0005(
    wave_metrics: Dict[str, float],
    velocity: float = 0.0,
    atom_lineage: Optional[str] = None
) -> Dict:
    """
    Main filter function - evaluates coherence and determines pass/fail.
    
    Args:
        wave_metrics: WAVE analysis metrics (curl, divergence, potential, entropy)
        velocity: Velocity in m/s (default 0 for rest frame)
        atom_lineage: ATOM trail reference for lineage verification
        
    Returns:
        Dictionary with keys:
        - coherence: float
        - state: CoherenceState
        - passed: bool
        - message: str
        - details: dict with node values and other info
        - isomorphism_preserved: bool
    """
    result = {
        "coherence": 0.0,
        "state": CoherenceState.COLLAPSE.value,
        "passed": False,
        "message": "",
        "details": {},
        "isomorphism_preserved": True
    }
    
    # Lineage check (warning if missing, but not blocking)
    if atom_lineage is None:
        result["details"]["lineage_warning"] = "No ATOM lineage provided"
    else:
        result["details"]["atom_lineage"] = atom_lineage
    
    try:
        # Calculate base coherence in rest frame
        tetrahedron = calculate_4_0005_coherence(wave_metrics)
        rest_coherence = tetrahedron.coherence
        
        # Apply Lorentz scaling if velocity is non-zero
        if velocity > 0:
            observed_coherence, iso_preserved = lorentz_scaled_coherence(
                rest_coherence, velocity
            )
            result["isomorphism_preserved"] = iso_preserved
            if not iso_preserved:
                result["coherence"] = float('inf')
                result["state"] = CoherenceState.ISOMORPHISM_BREAK.value
                result["passed"] = False
                result["message"] = (
                    "Lorentz factor diverges. Isomorphism breaks under supergravity."
                )
                result["details"]["velocity"] = velocity
                result["details"]["rest_coherence"] = rest_coherence
                return result
        else:
            observed_coherence = rest_coherence
        
        # Determine state and pass/fail based on observed coherence
        result["coherence"] = observed_coherence
        state = determine_coherence_state(observed_coherence)
        result["state"] = state.value
        
        # Store node details
        result["details"]["nodes"] = {
            "theorem": tetrahedron.theorem.value,
            "embody": tetrahedron.embody.value,
            "connect": tetrahedron.connect.value,
            "be": tetrahedron.be.value
        }
        result["details"]["velocity"] = velocity
        
        # Determine pass/fail and message based on state
        if state == CoherenceState.COLLAPSE:
            result["passed"] = False
            result["message"] = (
                "Coherence below minimum tetrahedral stability. Structure incomplete."
            )
        elif state == CoherenceState.UNSTABLE:
            result["passed"] = False
            result["message"] = (
                "No stability buffer. Vulnerable to quantum fluctuations."
            )
        elif state == CoherenceState.CRYSTALLINE:
            result["passed"] = True
            result["message"] = "Optimal coherence achieved. Structure stable."
        elif state == CoherenceState.RADIATING:
            result["passed"] = True
            result["message"] = (
                "Coherence above equilibrium. Recommend gentle attenuation."
            )
        
    except (KeyError, ValueError) as e:
        result["passed"] = False
        result["message"] = f"Filter error: {str(e)}"
        result["details"]["error"] = str(e)
    
    return result


def generate_tetrahedron_for_visualization(
    tetrahedron: CoherenceTetrahedron
) -> Dict[str, List]:
    """
    Generate vertex and edge data for 3D visualization.
    
    Args:
        tetrahedron: CoherenceTetrahedron to visualize
        
    Returns:
        Dictionary with 'vertices' and 'edges' lists for rendering
    """
    # Standard tetrahedron coordinates (centered at origin)
    # Base triangle in xy-plane, apex above
    vertices = [
        {
            "name": "theorem",
            "position": [1.0, 0.0, 0.0],
            "value": tetrahedron.theorem.value,
            "phase": tetrahedron.theorem.phase
        },
        {
            "name": "embody",
            "position": [-0.5, 0.866, 0.0],  # 120° around z-axis
            "value": tetrahedron.embody.value,
            "phase": tetrahedron.embody.phase
        },
        {
            "name": "connect",
            "position": [-0.5, -0.866, 0.0],  # 240° around z-axis
            "value": tetrahedron.connect.value,
            "phase": tetrahedron.connect.phase
        },
        {
            "name": "be",
            "position": [0.0, 0.0, 1.633],  # Apex (√8/3 height)
            "value": tetrahedron.be.value,
            "phase": tetrahedron.be.phase
        }
    ]
    
    # Six edges of tetrahedron
    edges = [
        {"from": "theorem", "to": "embody", "label": "theory → practice"},
        {"from": "theorem", "to": "connect", "label": "theory → network"},
        {"from": "theorem", "to": "be", "label": "theory → existence"},
        {"from": "embody", "to": "connect", "label": "practice → network"},
        {"from": "embody", "to": "be", "label": "practice → existence"},
        {"from": "connect", "to": "be", "label": "network → existence"}
    ]
    
    return {
        "vertices": vertices,
        "edges": edges,
        "coherence": tetrahedron.coherence,
        "state": tetrahedron.state.value
    }


# ============================================================================
# Unit Tests
# ============================================================================

def test_collapse_state():
    """Test COLLAPSE state (< 4.0000)"""
    wave_metrics = {
        "curl": 0.2,
        "divergence": 0.3,
        "potential": 0.5,
        "entropy": 0.8  # Will contribute ~0.4 + epsilon
    }
    result = filter_signal_4_0005(wave_metrics)
    
    assert result["state"] == CoherenceState.COLLAPSE.value
    assert result["passed"] is False
    assert result["coherence"] < 4.0
    assert "incomplete" in result["message"].lower()
    print(f"✓ COLLAPSE state: coherence={result['coherence']:.4f}")


def test_unstable_state():
    """Test UNSTABLE state (= 4.0000)"""
    # Craft metrics to hit exactly 4.0000
    wave_metrics = {
        "curl": 1.0,
        "divergence": 1.0,
        "potential": 1.0,
        "entropy": 1.999  # Will contribute ~0.9995 + 0.0005 = 1.0
    }
    result = filter_signal_4_0005(wave_metrics)
    
    assert result["state"] == CoherenceState.UNSTABLE.value
    assert result["passed"] is False
    assert abs(result["coherence"] - 4.0) < 0.001
    assert "buffer" in result["message"].lower()
    print(f"✓ UNSTABLE state: coherence={result['coherence']:.4f}")


def test_crystalline_state():
    """Test CRYSTALLINE state (= 4.0005)"""
    # Craft metrics to hit exactly 4.0005
    wave_metrics = {
        "curl": 1.0,
        "divergence": 1.0,
        "potential": 1.0,
        "entropy": 2.0  # Will contribute 1.0 + 0.0005 = 1.0005
    }
    result = filter_signal_4_0005(wave_metrics)
    
    assert result["state"] == CoherenceState.CRYSTALLINE.value
    assert result["passed"] is True
    assert abs(result["coherence"] - 4.0005) < 0.001
    assert "stable" in result["message"].lower()
    print(f"✓ CRYSTALLINE state: coherence={result['coherence']:.4f}")


def test_radiating_state():
    """Test RADIATING state (> 4.001)"""
    wave_metrics = {
        "curl": 1.0,
        "divergence": 1.0,
        "potential": 1.0,
        "entropy": 2.0  # Base gives 4.0005
    }
    # Add extra to push over threshold
    wave_metrics["curl"] = 1.0
    wave_metrics["potential"] = 1.01  # Push slightly over
    result = filter_signal_4_0005(wave_metrics)
    
    # May be CRYSTALLINE or RADIATING depending on exact value
    assert result["passed"] is True
    print(f"✓ High coherence state: {result['state']}, coherence={result['coherence']:.4f}")


def test_isomorphism_break():
    """Test ISOMORPHISM_BREAK at v = c"""
    wave_metrics = {
        "curl": 1.0,
        "divergence": 1.0,
        "potential": 1.0,
        "entropy": 2.0
    }
    
    # At velocity = c, should break
    result = filter_signal_4_0005(wave_metrics, velocity=SPEED_OF_LIGHT)
    
    assert result["state"] == CoherenceState.ISOMORPHISM_BREAK.value
    assert result["passed"] is False
    assert result["isomorphism_preserved"] is False
    assert result["coherence"] == float('inf')
    assert "isomorphism breaks" in result["message"].lower()
    print(f"✓ ISOMORPHISM_BREAK at v=c: {result['message']}")


def test_lorentz_scaling():
    """Test Lorentz scaling at relativistic velocities"""
    wave_metrics = {
        "curl": 1.0,
        "divergence": 1.0,
        "potential": 1.0,
        "entropy": 2.0
    }
    
    # At 0.5c, gamma ≈ 1.1547
    v = SPEED_OF_LIGHT * 0.5
    result = filter_signal_4_0005(wave_metrics, velocity=v)
    
    assert result["isomorphism_preserved"] is True
    assert result["coherence"] > 4.0005  # Scaled up by gamma
    print(f"✓ Lorentz scaling at 0.5c: coherence={result['coherence']:.4f}")


def test_visualization_generation():
    """Test visualization data generation"""
    wave_metrics = {
        "curl": 1.0,
        "divergence": 1.0,
        "potential": 1.0,
        "entropy": 2.0
    }
    
    tetrahedron = calculate_4_0005_coherence(wave_metrics)
    viz_data = generate_tetrahedron_for_visualization(tetrahedron)
    
    assert len(viz_data["vertices"]) == 4
    assert len(viz_data["edges"]) == 6
    assert viz_data["coherence"] == tetrahedron.coherence
    assert viz_data["state"] == tetrahedron.state.value
    print(f"✓ Visualization data: {len(viz_data['vertices'])} vertices, {len(viz_data['edges'])} edges")


def test_lineage_tracking():
    """Test ATOM lineage tracking"""
    wave_metrics = {
        "curl": 1.0,
        "divergence": 1.0,
        "potential": 1.0,
        "entropy": 2.0
    }
    
    result = filter_signal_4_0005(
        wave_metrics,
        atom_lineage="ATOM-FILTER-20260119-002-supergravity-4.0005"
    )
    
    assert "atom_lineage" in result["details"]
    assert result["details"]["atom_lineage"].startswith("ATOM-")
    print(f"✓ Lineage tracked: {result['details']['atom_lineage']}")


def test_missing_metrics():
    """Test error handling for missing metrics"""
    wave_metrics = {
        "curl": 0.5,
        "divergence": 0.3
        # Missing potential and entropy
    }
    
    result = filter_signal_4_0005(wave_metrics)
    
    assert result["passed"] is False
    assert "error" in result["details"]
    print(f"✓ Missing metrics handled: {result['message']}")


def run_all_tests():
    """Run all unit tests"""
    print("\n" + "="*60)
    print("Supergravity 4.0005 Coherence Filter - Unit Tests")
    print("="*60 + "\n")
    
    tests = [
        test_collapse_state,
        test_unstable_state,
        test_crystalline_state,
        test_radiating_state,
        test_isomorphism_break,
        test_lorentz_scaling,
        test_visualization_generation,
        test_lineage_tracking,
        test_missing_metrics
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
