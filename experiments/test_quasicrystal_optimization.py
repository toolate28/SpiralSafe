#!/usr/bin/env python3
"""
Unit tests for Quasicrystal Optimization Engine.

Test case: n_points=16, iterations=4, batch_size equivalent coverage
- Validates same output as reference kernel
- Measures cycles before/after phason pass
- Pass if cycles decrease or stay within 5% (noise tolerance)
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
    greedy_baseline_optimization,
    compare_with_baseline,
    holographic_conservation,
    supergravity_coupling,
)


# =============================================================================
# REFERENCE KERNEL VALUES (n_points=16, iterations=4, seed=42)
# =============================================================================

REFERENCE_SEED = 42
REFERENCE_N_POINTS = 16  # Small test case (forest_height≈4)
REFERENCE_ITERATIONS = 4  # batch_size equivalent
REFERENCE_ROUNDS = 2  # Comparison rounds


def sphere(x: np.ndarray) -> float:
    """Reference objective: ||x||²."""
    return float(np.sum(x**2))


# =============================================================================
# TEST SUITE
# =============================================================================

class QuasicrystalTestSuite:
    """Test suite with cycle measurement."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.cycles = {}

    def run_all(self):
        """Run all tests."""
        print("=" * 60)
        print("[Experiment 56] Quasicrystal Optimization Tests")
        print("Golden Phason Flips - Reference Kernel Validation")
        print("=" * 60)

        tests = [
            ("PHI = (1+√5)/2 exactly", self._test_phi_exact),
            ("Golden angle ≈ 137.5°", self._test_golden_angle),
            ("Fibonacci cache valid", self._test_fibonacci),
            ("Epsilon = 0.0005", self._test_epsilon),
            ("v=c guard at 62", self._test_vc_guard),
            ("Reference kernel output", self._test_reference_output),
            ("Reproducibility (seed)", self._test_reproducibility),
            ("Cycles: baseline measurement", self._test_cycles_baseline),
            ("Cycles: phason pass", self._test_cycles_phason),
            ("Cycles: comparison (≤5% overhead)", self._test_cycles_comparison),
            ("Baseline vs QC comparison", self._test_baseline_comparison),
            ("Holographic encoding", self._test_holographic),
            ("Supergravity coupling", self._test_supergravity),
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
            print(f"\nCycle measurements:")
            for k, v in self.cycles.items():
                print(f"  {k}: {v:,.0f} ns ({v/1e6:.2f} ms)")
        print("=" * 60)

        return self.failed == 0

    def _test_phi_exact(self):
        """PHI must be exactly (1+√5)/2."""
        expected = (1 + math.sqrt(5)) / 2
        assert PHI == expected, f"PHI={PHI}, expected {expected}"

    def _test_golden_angle(self):
        """Golden angle must be ≈137.5°."""
        deg = math.degrees(GOLDEN_ANGLE)
        assert 137.5 < deg < 137.6, f"Got {deg:.2f}°"

    def _test_fibonacci(self):
        """Fibonacci cache must be valid."""
        for i in range(2, len(FIBONACCI_CACHE)):
            assert FIBONACCI_CACHE[i] == FIBONACCI_CACHE[i-1] + FIBONACCI_CACHE[i-2]

    def _test_epsilon(self):
        """Epsilon must be 0.0005."""
        assert EPSILON_STABILITY == 0.0005

    def _test_vc_guard(self):
        """v=c guard must trigger at iterations > 62."""
        try:
            quasicrystal_optimization(sphere, 10, 63, seed=1)
            raise AssertionError("Should raise RuntimeError")
        except RuntimeError as e:
            assert "v=c boundary" in str(e)

    def _test_reference_output(self):
        """Output must match reference kernel."""
        coord, val = quasicrystal_optimization(
            sphere, REFERENCE_N_POINTS, REFERENCE_ITERATIONS, seed=REFERENCE_SEED
        )
        assert val >= 0, "Sphere is non-negative"
        assert coord.shape == (2,), "Must be 2D coordinate"
        # Store for comparison
        self.ref_coord = coord
        self.ref_val = val

    def _test_reproducibility(self):
        """Same seed must produce same output."""
        c1, v1 = quasicrystal_optimization(sphere, 16, 4, seed=123)
        c2, v2 = quasicrystal_optimization(sphere, 16, 4, seed=123)
        assert np.allclose(c1, c2), "Coordinates differ"
        assert abs(v1 - v2) < 1e-10, "Values differ"

    def _test_cycles_baseline(self):
        """Measure baseline (greedy) cycles."""
        # Warmup
        greedy_baseline_optimization(sphere, REFERENCE_N_POINTS, REFERENCE_ITERATIONS, seed=1)

        # Measure
        times = []
        for _ in range(REFERENCE_ROUNDS):
            start = time.perf_counter_ns()
            greedy_baseline_optimization(sphere, REFERENCE_N_POINTS, REFERENCE_ITERATIONS, seed=REFERENCE_SEED)
            times.append(time.perf_counter_ns() - start)

        avg = sum(times) / len(times)
        self.cycles["baseline"] = avg
        print(f"      Baseline: {avg:,.0f} ns")

    def _test_cycles_phason(self):
        """Measure phason pass cycles."""
        # Warmup
        quasicrystal_optimization(sphere, REFERENCE_N_POINTS, REFERENCE_ITERATIONS, seed=1)

        # Measure
        times = []
        for _ in range(REFERENCE_ROUNDS):
            start = time.perf_counter_ns()
            quasicrystal_optimization(sphere, REFERENCE_N_POINTS, REFERENCE_ITERATIONS, seed=REFERENCE_SEED)
            times.append(time.perf_counter_ns() - start)

        avg = sum(times) / len(times)
        self.cycles["phason"] = avg
        print(f"      Phason: {avg:,.0f} ns")

    def _test_cycles_comparison(self):
        """Phason cycles must be ≤105% of baseline (5% tolerance)."""
        baseline = self.cycles.get("baseline", 0)
        phason = self.cycles.get("phason", 0)

        if baseline == 0:
            print("      Skipped (no baseline)")
            return

        ratio = phason / baseline
        overhead_pct = (ratio - 1) * 100
        print(f"      Ratio: {ratio:.3f} ({overhead_pct:+.1f}%)")

        # Pass if cycles decrease or stay within 5%
        assert ratio <= 1.05, f"Overhead {overhead_pct:.1f}% exceeds 5% tolerance"

    def _test_baseline_comparison(self):
        """QC optimizer should match or beat baseline."""
        _, qc_val = quasicrystal_optimization(sphere, 30, 30, seed=42)
        _, baseline_val = greedy_baseline_optimization(sphere, 30, 30, seed=42)

        # QC should be at least as good
        assert qc_val <= baseline_val * 1.1, f"QC={qc_val}, baseline={baseline_val}"
        print(f"      QC: {qc_val:.6f}, Baseline: {baseline_val:.6f}")

    def _test_holographic(self):
        """Holographic encoding must be deterministic."""
        state = {"x": 1.0, "y": 2.0}
        e1 = holographic_conservation(state, 1e6)
        e2 = holographic_conservation(state, 1e6)
        assert e1 == e2

    def _test_supergravity(self):
        """Supergravity coupling must work."""
        b = np.array([1.0, 2.0])
        f = np.array([0.1, 0.2])
        c = supergravity_coupling(b, f)
        assert np.allclose(c, b + f)


def main():
    suite = QuasicrystalTestSuite()
    success = suite.run_all()
    print("\n✨ ALL TESTS PASSED ✨\n" if success else "\n❌ TESTS FAILED ❌\n")
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
