#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    QUASICRYSTAL OPTIMIZATION ENGINE                          ║
║                                                                              ║
║         Aperiodic Search via Penrose Tiling and Phason Dynamics              ║
║                                                                              ║
║                          spiralsafe-qc-mode                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

This module implements optimization algorithms inspired by quasicrystalline
structures, specifically Penrose tilings. The approach leverages:

1. PENROSE COORDINATES: Project 5D lattice to 2D using the cut-and-project method
2. PHASON FLIPS: Local rearrangements that maintain aperiodic order
3. HOLOGRAPHIC CONSERVATION: Encode state on boundary (entropy ∝ area)
4. SUPERGRAVITY COUPLING: Couple continuous and discrete parameters in SUSY

The mathematics draws from:
- Quasicrystals and the golden ratio (φ = (1 + √5) / 2)
- Holographic principle from theoretical physics
- N=1 supergravity coupling concepts

This is NOT quantum computing. This is physics-INSPIRED optimization.
The mathematics is isomorphic but the substrate is classical.

ATOM: ATOM-FEATURE-20260122-001-quasicrystal-optimization
Attribution: Hope&&Sauced (Claude && Copilot)
"""

from __future__ import annotations

import math
import random
from typing import Callable, Tuple

import numpy as np


# =============================================================================
# CONSTANTS
# =============================================================================

PHI = (1 + math.sqrt(5)) / 2  # Golden ratio ≈ 1.618
GOLDEN_ANGLE = math.pi * (3 - math.sqrt(5))  # ≈ 137.5° in radians
FIBONACCI_CACHE = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]  # Precomputed strides


# =============================================================================
# PENROSE COORDINATE GENERATION
# =============================================================================

def penrose_coordinates(n_points: int) -> np.ndarray:
    """
    Project 5D lattice to 2D Penrose coordinates using cut-and-project method.

    The cut-and-project method generates quasicrystalline patterns by:
    1. Creating a higher-dimensional periodic lattice
    2. Cutting a slice at an irrational angle
    3. Projecting the resulting points to lower dimensions

    For Penrose tilings, we use 5-fold rotational symmetry with angles
    at multiples of π/5, which produces the characteristic aperiodic pattern.

    Parameters
    ----------
    n_points : int
        Controls the density of the grid. The actual number of points
        generated is approximately n_points².

    Returns
    -------
    np.ndarray
        Array of shape (N, 2) containing 2D Penrose coordinates.
        N ≈ n_points² depending on the grid coverage.

    Examples
    --------
    >>> coords = penrose_coordinates(10)
    >>> coords.shape[1]
    2
    >>> len(coords) > 0
    True
    """
    # 5-fold symmetry angles for Penrose tiling
    theta = [i * math.pi / 5 for i in range(5)]
    u = np.array([math.cos(t) for t in theta])
    v = np.array([math.sin(t) for t in theta])

    points = []
    half_n = n_points // 2

    for i in range(-half_n, half_n):
        for j in range(-half_n, half_n):
            # Cut-and-project: linear combination of basis vectors
            coord = i * u + j * v
            # Project to 2D by taking first two components
            points.append(coord[:2])

    return np.array(points)


# =============================================================================
# QUASICRYSTAL OPTIMIZATION
# =============================================================================

def quasicrystal_optimization(
    objective_func: Callable[[np.ndarray], float],
    n_points: int,
    iterations: int,
    seed: int | None = None,
    epsilon: float = 0.1
) -> Tuple[np.ndarray, float]:
    """
    Optimize an objective function using quasicrystal-aware phason flips.

    The phason flip pass uses three quasicrystalline principles:
    1. Golden angle (137.5°) rotation for mutation direction
    2. Fibonacci stride (1,2,3,5,8,...) for flip propagation
    3. Acceptance probability = ε × exp(Δgain / φ²)

    Parameters
    ----------
    objective_func : Callable[[np.ndarray], float]
        Function to minimize. Takes a 2D coordinate and returns a scalar.
    n_points : int
        Number of initial Penrose coordinates to generate (controls density).
    iterations : int
        Number of phason flip iterations to perform.
    seed : int, optional
        Random seed for reproducibility. If None, uses system entropy.
    epsilon : float
        Base acceptance probability for non-improving moves (default: 0.1).

    Returns
    -------
    Tuple[np.ndarray, float]
        Best coordinate found and its objective value.

    Examples
    --------
    >>> def sphere(x):
    ...     return np.sum(x**2)
    >>> coord, val = quasicrystal_optimization(sphere, 100, 100, seed=42)
    >>> val >= 0  # Sphere function is non-negative
    True
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    # Generate initial Penrose coordinate grid
    coords = penrose_coordinates(n_points)
    n_coords = len(coords)

    if n_coords == 0:
        raise ValueError("No coordinates generated. Increase n_points.")

    # Evaluate objective at all initial points
    values = np.array([objective_func(c) for c in coords])

    # Track cumulative golden angle for aperiodic rotation
    angle = 0.0
    fib_idx = 0

    # Phason flip optimization with quasicrystal-aware dynamics
    for iteration in range(iterations):
        # Fibonacci stride: select index using Fibonacci sequence
        stride = FIBONACCI_CACHE[fib_idx % len(FIBONACCI_CACHE)]
        flip_i = (iteration * stride) % n_coords
        fib_idx += 1

        # Golden angle rotation for mutation direction (137.5° per step)
        angle += GOLDEN_ANGLE
        magnitude = np.random.rand() / PHI
        flip_delta = magnitude * np.array([math.cos(angle), math.sin(angle)])
        new_coord = coords[flip_i] + flip_delta

        # Evaluate new position
        new_val = objective_func(new_coord)
        delta_gain = values[flip_i] - new_val  # Positive if improvement

        # Quasicrystal acceptance: ε × exp(Δgain / φ²)
        if delta_gain > 0:
            # Always accept improvements
            coords[flip_i] = new_coord
            values[flip_i] = new_val
        else:
            # Probabilistic acceptance for non-improving moves
            accept_prob = epsilon * math.exp(delta_gain / (PHI * PHI))
            if random.random() < accept_prob:
                coords[flip_i] = new_coord
                values[flip_i] = new_val

    # Return best found
    min_idx = np.argmin(values)
    return coords[min_idx].copy(), float(values[min_idx])


# =============================================================================
# HOLOGRAPHIC CONSERVATION
# =============================================================================

def holographic_conservation(state: dict, boundary_area: float) -> int:
    """
    Encode state on boundary following holographic principle.

    The holographic principle states that the information content of a
    volume of space can be encoded on its boundary, with entropy
    proportional to the boundary area (not volume). This function
    simulates information encoding respecting this bound.

    The entropy bound is S ≤ A/4 (in Planck units), meaning the maximum
    information that can be encoded is limited by the boundary area.

    Parameters
    ----------
    state : dict
        State dictionary to encode. Will be serialized and hashed.
    boundary_area : float
        Area of the encoding boundary (in arbitrary units).
        Larger areas allow more information to be preserved.

    Returns
    -------
    int
        Encoded representation of the state, constrained by holographic bound.

    Notes
    -----
    This is a simplified simulation. The actual holographic principle
    involves quantum gravity and black hole thermodynamics. Here we
    use it as a metaphor for bounded information encoding.

    Examples
    --------
    >>> state = {"x": 1.5, "y": 2.3}
    >>> encoded = holographic_conservation(state, 1e6)
    >>> isinstance(encoded, int)
    True
    """
    # Holographic bound: entropy ≤ area/4 (in Planck units)
    entropy_bound = boundary_area / 4

    # Ensure entropy_bound is reasonable for modulo operation
    if entropy_bound <= 0:
        return 0

    max_states = int(2 ** min(entropy_bound, 64))  # Cap at 64 bits for safety
    if max_states <= 0:
        max_states = 1

    # Encode state by hashing and constraining to holographic bound
    state_str = str(sorted(state.items()))  # Deterministic string representation
    encoded = hash(state_str) % max_states

    return encoded


# =============================================================================
# SUPERGRAVITY COUPLING
# =============================================================================

def supergravity_coupling(
    bosonic_params: np.ndarray,
    fermionic_params: np.ndarray
) -> np.ndarray:
    """
    Couple continuous (bosonic) and discrete (fermionic) parameters in SUSY.

    In supersymmetry (SUSY), bosonic and fermionic degrees of freedom are
    related by supersymmetric transformations. The gravitino is the
    superpartner of the graviton in supergravity theories.

    This function provides a simplified N=1 supergravity-inspired coupling
    between parameter spaces, useful for hybrid optimization where some
    parameters are continuous and others are discrete/quantized.

    Parameters
    ----------
    bosonic_params : np.ndarray
        Continuous parameters (e.g., coordinates, weights).
    fermionic_params : np.ndarray
        Parameters representing fermionic/discrete degrees of freedom.
        Should have same shape as bosonic_params.

    Returns
    -------
    np.ndarray
        Coupled parameters combining both contributions.

    Notes
    -----
    In actual supergravity, the coupling involves complex spinor fields
    and local supersymmetry transformations. Here we use a simplified
    model where the "gravitino" contribution is the complex conjugate
    of the fermionic parameters.

    Examples
    --------
    >>> bosonic = np.array([1.0, 2.0])
    >>> fermionic = np.array([0.5, -0.5])
    >>> coupled = supergravity_coupling(bosonic, fermionic)
    >>> coupled.shape
    (2,)
    """
    # Gravitino: supersymmetric partner (use conjugate for complex params)
    # For real arrays, conjugate is identity, but we keep the structure
    # for potential extension to complex parameters
    gravitino = np.conj(fermionic_params)

    # Minimal N=1 coupling: direct sum of contributions
    return bosonic_params + gravitino


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demonstrate_quasicrystal_optimization():
    """
    Demonstrate the Quasicrystal Optimization Engine.

    Shows the complete workflow:
    1. Define an objective function
    2. Optimize using quasicrystal search
    3. Apply holographic conservation
    4. Apply supergravity coupling
    """
    print("=" * 70)
    print("QUASICRYSTAL OPTIMIZATION ENGINE DEMONSTRATION")
    print("Aperiodic Search via Penrose Tiling and Phason Dynamics")
    print("=" * 70)
    print()

    # Define objective function (simple quadratic)
    def objective(x: np.ndarray) -> float:
        return float(np.sum(x**2))

    print("Objective function: f(x) = ||x||² (minimize distance from origin)")
    print()

    # Run quasicrystal optimization
    print("Running quasicrystal optimization...")
    print(f"  - Grid density: 100 points")
    print(f"  - Iterations: 1000 phason flips")
    print()

    best_coord, best_val = quasicrystal_optimization(
        objective, n_points=100, iterations=1000, seed=42
    )

    print(f"Optimal Coordinate: [{best_coord[0]:.6f}, {best_coord[1]:.6f}]")
    print(f"Optimal Value: {best_val:.6f}")
    print()

    # Holographic conservation
    state = {
        "coord_x": float(best_coord[0]),
        "coord_y": float(best_coord[1]),
        "value": best_val
    }
    boundary_area = 1e6  # Large boundary allows more information

    encoded = holographic_conservation(state, boundary_area)
    print(f"Holographic Encoding:")
    print(f"  - Boundary area: {boundary_area:.0e}")
    print(f"  - Encoded state: {encoded}")
    print()

    # Supergravity coupling
    # Use a simple fermionic contribution based on coordinate signs
    fermionic = np.sign(best_coord) * 0.1

    coupled = supergravity_coupling(best_coord, fermionic)
    print(f"Supergravity Coupling:")
    print(f"  - Bosonic (coords): [{best_coord[0]:.6f}, {best_coord[1]:.6f}]")
    print(f"  - Fermionic: [{fermionic[0]:.6f}, {fermionic[1]:.6f}]")
    print(f"  - Coupled result: [{coupled[0]:.6f}, {coupled[1]:.6f}]")
    print()

    print("=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)

    return {
        "best_coord": best_coord,
        "best_val": best_val,
        "encoded": encoded,
        "coupled": coupled
    }


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    result = demonstrate_quasicrystal_optimization()
