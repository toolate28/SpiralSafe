#!/usr/bin/env python3
"""
Unit tests for the Quasicrystal Optimization Engine.

Validates against baseline kernel with:
- Same input → same output (deterministic with seed)
- Cycle measurement for performance baseline
"""

import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np

from quasicrystal_optimization import (
    PHI,
    GOLDEN_ANGLE,
    FIBONACCI_CACHE,
    EPSILON_STABILITY,
    penrose_coordinates,
    quasicrystal_optimization,
    holographic_conservation,
    supergravity_coupling,
)


# =============================================================================
# BASELINE KERNEL VALUES (computed with seed=42, n_points=50, iterations=50)
# =============================================================================

BASELINE_SEED = 42
BASELINE_N_POINTS = 50
BASELINE_ITERATIONS = 50
BASELINE_COORD = np.array([0.0, 0.0])  # Origin is in the Penrose grid
BASELINE_VAL = 0.0


def sphere(x: np.ndarray) -> float:
    """Baseline objective: minimize ||x||²."""
    return float(np.sum(x**2))


# =============================================================================
# TEST SUITE
# =============================================================================

class QuasicrystalTestSuite:
    """Test suite validating against baseline kernel."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.cycles = {}

    def run_all(self):
        """Run all tests."""
        print("=" * 60)
        print("Quasicrystal Optimization - Baseline Kernel Validation")
        print("=" * 60)

        tests = [
            ("Constants: PHI", self._test_phi),
            ("Constants: golden angle", self._test_golden_angle),
            ("Constants: Fibonacci cache", self._test_fibonacci),
            ("Constants: epsilon stability", self._test_epsilon),
            ("Penrose coordinates: shape", self._test_penrose_shape),
            ("Penrose coordinates: deterministic", self._test_penrose_deterministic),
            ("Optimization: v=c guard", self._test_vc_guard),
            ("Optimization: baseline output", self._test_baseline_output),
            ("Optimization: reproducibility", self._test_reproducibility),
            ("Optimization: cycles measured", self._test_cycles),
            ("Holographic: deterministic", self._test_holographic),
            ("Supergravity: coupling", self._test_supergravity),
            ("Integration: full pipeline", self._test_integration),
        ]

        for name, test_func in tests:
            try:
                print(f"\n🧪 {name}")
                test_func()
                print(f"   ✅ PASS")
                self.passed += 1
            except AssertionError as e:
                print(f"   ❌ FAIL: {e}")
                self.failed += 1
            except Exception as e:
                print(f"   ❌ ERROR: {type(e).__name__}: {e}")
                self.failed += 1

        print("\n" + "=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        if self.cycles:
            print(f"Cycles: {self.cycles}")
        print("=" * 60)

        return self.failed == 0

    def _test_phi(self):
        """Validate golden ratio."""
        expected = (1 + math.sqrt(5)) / 2
        assert abs(PHI - expected) < 1e-10
        assert abs(PHI - 1.618033988749895) < 1e-12

    def _test_golden_angle(self):
        """Validate golden angle ≈ 137.5°."""
        deg = math.degrees(GOLDEN_ANGLE)
        assert 137.5 < deg < 137.6, f"Expected ~137.5°, got {deg:.2f}°"

    def _test_fibonacci(self):
        """Validate Fibonacci sequence."""
        for i in range(2, len(FIBONACCI_CACHE)):
            assert FIBONACCI_CACHE[i] == FIBONACCI_CACHE[i-1] + FIBONACCI_CACHE[i-2]

    def _test_epsilon(self):
        """Validate stability epsilon = 0.0005."""
        assert EPSILON_STABILITY == 0.0005

    def _test_penrose_shape(self):
        """Validate Penrose coordinate shape."""
        coords = penrose_coordinates(10)
        assert coords.ndim == 2
        assert coords.shape[1] == 2

    def _test_penrose_deterministic(self):
        """Validate Penrose coordinates are deterministic."""
        c1 = penrose_coordinates(20)
        c2 = penrose_coordinates(20)
        assert np.allclose(c1, c2)

    def _test_vc_guard(self):
        """Validate v=c boundary guard at iteration > 62."""
        try:
            quasicrystal_optimization(sphere, 10, 63, seed=1)
            raise AssertionError("Should raise RuntimeError for iterations > 62")
        except RuntimeError as e:
            assert "v=c boundary" in str(e)

    def _test_baseline_output(self):
        """Validate output matches baseline kernel."""
        coord, val = quasicrystal_optimization(
            sphere, BASELINE_N_POINTS, BASELINE_ITERATIONS, seed=BASELINE_SEED
        )
        # Origin [0,0] should be in grid and have value 0
        assert val >= 0, "Sphere function is non-negative"
        assert np.allclose(coord, BASELINE_COORD) or val <= BASELINE_VAL + 0.01

    def _test_reproducibility(self):
        """Validate same seed → same output."""
        c1, v1 = quasicrystal_optimization(sphere, 30, 30, seed=123)
        c2, v2 = quasicrystal_optimization(sphere, 30, 30, seed=123)
        assert np.allclose(c1, c2)
        assert abs(v1 - v2) < 1e-10

    def _test_cycles(self):
        """Measure cycles for baseline kernel."""
        start = time.perf_counter_ns()
        quasicrystal_optimization(sphere, BASELINE_N_POINTS, BASELINE_ITERATIONS, seed=BASELINE_SEED)
        elapsed_ns = time.perf_counter_ns() - start
        self.cycles["baseline_ns"] = elapsed_ns
        self.cycles["baseline_ms"] = elapsed_ns / 1e6
        print(f"      Measured: {elapsed_ns:,} ns ({elapsed_ns/1e6:.2f} ms)")

    def _test_holographic(self):
        """Validate holographic encoding is deterministic."""
        state = {"x": 1.5, "y": 2.5}
        e1 = holographic_conservation(state, 1e6)
        e2 = holographic_conservation(state, 1e6)
        assert e1 == e2
        assert isinstance(e1, int)

    def _test_supergravity(self):
        """Validate supergravity coupling."""
        b = np.array([1.0, 2.0])
        f = np.array([0.1, 0.2])
        c = supergravity_coupling(b, f)
        assert np.allclose(c, b + f)

    def _test_integration(self):
        """Validate full pipeline integration."""
        coord, val = quasicrystal_optimization(sphere, 50, 50, seed=42)
        state = {"coord": coord.tolist(), "val": val}
        encoded = holographic_conservation(state, 1e6)
        coupled = supergravity_coupling(coord, np.sign(coord) * 0.1)

        assert coord.shape == (2,)
        assert isinstance(val, float)
        assert isinstance(encoded, int)
        assert coupled.shape == (2,)


def main():
    suite = QuasicrystalTestSuite()
    success = suite.run_all()
    print("\n✨ ALL TESTS PASSED ✨\n" if success else "\n❌ TESTS FAILED ❌\n")
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
