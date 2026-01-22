#!/usr/bin/env python3
"""
Unit tests for the Quasicrystal Optimization Engine.

Tests the core functionality including:
- Penrose coordinate generation
- Quasicrystal optimization algorithm
- Holographic conservation
- Supergravity coupling
"""

import sys
from pathlib import Path

# Add experiments to path
sys.path.insert(0, str(Path(__file__).parent))

import numpy as np

from quasicrystal_optimization import (
    PHI,
    penrose_coordinates,
    quasicrystal_optimization,
    holographic_conservation,
    supergravity_coupling,
)


class QuasicrystalTestSuite:
    """Test suite for Quasicrystal Optimization Engine."""

    def __init__(self):
        self.passed = 0
        self.failed = 0

    def run_all(self):
        """Run all tests."""
        print("=" * 60)
        print("Quasicrystal Optimization Engine - Test Suite")
        print("=" * 60)

        tests = [
            ("Golden ratio constant", self._test_golden_ratio),
            ("Penrose coordinate generation", self._test_penrose_coordinates),
            ("Penrose coordinate shape", self._test_penrose_shape),
            ("Quasicrystal optimization basic", self._test_optimization_basic),
            ("Quasicrystal optimization reproducibility", self._test_optimization_seed),
            ("Quasicrystal optimization improves", self._test_optimization_improves),
            ("Holographic conservation basic", self._test_holographic_basic),
            ("Holographic conservation deterministic", self._test_holographic_deterministic),
            ("Holographic conservation boundary", self._test_holographic_boundary),
            ("Supergravity coupling basic", self._test_supergravity_basic),
            ("Supergravity coupling shape", self._test_supergravity_shape),
            ("Supergravity coupling real arrays", self._test_supergravity_real),
            ("End-to-end integration", self._test_integration),
        ]

        for name, test_func in tests:
            try:
                print(f"\n🧪 Testing: {name}")
                test_func()
                print(f"   ✅ PASS: {name}")
                self.passed += 1
            except AssertionError as e:
                print(f"   ❌ FAIL: {name}")
                print(f"      AssertionError: {e}")
                self.failed += 1
            except Exception as e:
                print(f"   ❌ FAIL: {name}")
                print(f"      Error: {type(e).__name__}: {e}")
                self.failed += 1

        print("\n" + "=" * 60)
        print(f"Test Results: {self.passed} passed, {self.failed} failed")
        print("=" * 60)

        return self.failed == 0

    def _test_golden_ratio(self):
        """Test golden ratio constant."""
        expected = (1 + 5**0.5) / 2
        assert abs(PHI - expected) < 1e-10, f"PHI should be {expected}, got {PHI}"
        assert PHI > 1.6 and PHI < 1.7, "PHI should be approximately 1.618"
        print("      - Golden ratio: OK")

    def _test_penrose_coordinates(self):
        """Test Penrose coordinate generation."""
        coords = penrose_coordinates(5)
        assert isinstance(coords, np.ndarray), "Should return numpy array"
        assert len(coords) > 0, "Should generate some coordinates"
        print(f"      - Generated {len(coords)} coordinates")

    def _test_penrose_shape(self):
        """Test Penrose coordinate shape."""
        coords = penrose_coordinates(10)
        assert coords.ndim == 2, "Should be 2D array"
        assert coords.shape[1] == 2, "Should have 2 columns (x, y)"
        print(f"      - Shape: {coords.shape}")

    def _test_optimization_basic(self):
        """Test basic optimization functionality."""
        def sphere(x):
            return np.sum(x**2)

        coord, val = quasicrystal_optimization(sphere, 50, 100, seed=42)

        assert isinstance(coord, np.ndarray), "Coordinate should be array"
        assert len(coord) == 2, "Coordinate should be 2D"
        assert isinstance(val, float), "Value should be float"
        assert val >= 0, "Sphere function is non-negative"
        print(f"      - Found: coord={coord}, val={val:.6f}")

    def _test_optimization_seed(self):
        """Test optimization reproducibility with seed."""
        def sphere(x):
            return np.sum(x**2)

        coord1, val1 = quasicrystal_optimization(sphere, 50, 100, seed=123)
        coord2, val2 = quasicrystal_optimization(sphere, 50, 100, seed=123)

        assert np.allclose(coord1, coord2), "Same seed should give same result"
        assert abs(val1 - val2) < 1e-10, "Values should match with same seed"
        print("      - Reproducibility: OK")

    def _test_optimization_improves(self):
        """Test that optimization improves the objective."""
        def sphere(x):
            return np.sum(x**2)

        # Get initial grid values
        coords = penrose_coordinates(50)
        initial_values = [sphere(c) for c in coords]
        initial_min = min(initial_values)

        # Run optimization
        _, optimized_val = quasicrystal_optimization(sphere, 50, 500, seed=42)

        # Optimized should be at least as good as initial minimum
        assert optimized_val <= initial_min + 0.1, \
            f"Optimization should improve: {optimized_val} vs {initial_min}"
        print(f"      - Initial min: {initial_min:.6f}, Optimized: {optimized_val:.6f}")

    def _test_holographic_basic(self):
        """Test basic holographic conservation."""
        state = {"x": 1.0, "y": 2.0}
        encoded = holographic_conservation(state, 1e6)

        assert isinstance(encoded, int), "Should return integer"
        assert encoded >= 0, "Encoded value should be non-negative"
        print(f"      - Encoded: {encoded}")

    def _test_holographic_deterministic(self):
        """Test holographic conservation is deterministic."""
        state = {"a": 1.5, "b": 2.5, "c": 3.5}

        enc1 = holographic_conservation(state, 1000)
        enc2 = holographic_conservation(state, 1000)

        assert enc1 == enc2, "Same state should give same encoding"
        print("      - Deterministic: OK")

    def _test_holographic_boundary(self):
        """Test holographic conservation with different boundaries."""
        state = {"value": 42}

        enc_small = holographic_conservation(state, 10)
        enc_large = holographic_conservation(state, 1e10)

        # Both should be valid integers
        assert isinstance(enc_small, int)
        assert isinstance(enc_large, int)

        # With zero boundary, should return 0
        enc_zero = holographic_conservation(state, 0)
        assert enc_zero == 0, "Zero boundary should give 0"
        print("      - Boundary handling: OK")

    def _test_supergravity_basic(self):
        """Test basic supergravity coupling."""
        bosonic = np.array([1.0, 2.0, 3.0])
        fermionic = np.array([0.1, 0.2, 0.3])

        coupled = supergravity_coupling(bosonic, fermionic)

        assert isinstance(coupled, np.ndarray), "Should return array"
        expected = bosonic + fermionic
        assert np.allclose(coupled, expected), "Should be sum for real arrays"
        print(f"      - Coupled: {coupled}")

    def _test_supergravity_shape(self):
        """Test supergravity coupling preserves shape."""
        bosonic = np.array([[1, 2], [3, 4]])
        fermionic = np.array([[0.1, 0.2], [0.3, 0.4]])

        coupled = supergravity_coupling(bosonic, fermionic)

        assert coupled.shape == bosonic.shape, "Shape should be preserved"
        print(f"      - Shape preserved: {coupled.shape}")

    def _test_supergravity_real(self):
        """Test supergravity coupling with real arrays (conjugate is identity)."""
        bosonic = np.array([1.0, -2.0])
        fermionic = np.array([-0.5, 0.5])

        coupled = supergravity_coupling(bosonic, fermionic)

        # For real arrays, conjugate is identity
        expected = np.array([0.5, -1.5])
        assert np.allclose(coupled, expected), f"Expected {expected}, got {coupled}"
        print("      - Real array coupling: OK")

    def _test_integration(self):
        """Test end-to-end integration."""
        # 1. Optimize
        def rosenbrock_2d(x):
            """Rosenbrock function in 2D."""
            return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

        coord, val = quasicrystal_optimization(rosenbrock_2d, 100, 500, seed=42)

        # 2. Holographic encode
        state = {"coord": coord.tolist(), "val": val}
        encoded = holographic_conservation(state, 1e8)

        # 3. Supergravity couple
        fermionic = np.sin(coord)  # Non-trivial fermionic contribution
        coupled = supergravity_coupling(coord, fermionic)

        # All should complete without error
        assert coord.shape == (2,)
        assert isinstance(val, float)
        assert isinstance(encoded, int)
        assert coupled.shape == (2,)
        print(f"      - Integration complete: val={val:.6f}")


def main():
    """Run the test suite."""
    suite = QuasicrystalTestSuite()
    success = suite.run_all()

    if success:
        print("\n✨ ALL TESTS PASSED ✨\n")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED ❌\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
