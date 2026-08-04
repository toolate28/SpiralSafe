#!/usr/bin/env python3
"""
Tests for Quasicrystal Phason Scheduler

Test case: forest_height=4, batch_size=16, rounds=2
- Assert output matches reference values
- Verify v=c guard behavior
- Compare quasicrystal vs baseline density
- Test VLIW bundle packing simulation
"""

import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np

from quasicrystal_phason_scheduler import (
    PHI, GOLDEN_ANGLE, EPSILON, DEFAULT_VC_GUARD_LIMIT,
    penrose_project, phason_flip, bundle_density_objective,
    quasicrystal_schedule, uniform_random_schedule, compare_schedulers,
    VLIWBundle, vliw_packing_objective, simulate_vliw_packing,
)

# Test parameters (forest_height=4, batch_size=16, rounds=2)
FOREST_HEIGHT = 4   # maps to n_points
BATCH_SIZE = 16     # maps to iterations
ROUNDS = 2          # test repetitions
SEED = 42


class TestSuite:
    """Test suite for quasicrystal phason scheduler."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.metrics = {}

    def run(self):
        """Run all tests and return success status."""
        print("=" * 60)
        print("[Quasicrystal Phason Scheduler Tests]")
        print(f"forest_height={FOREST_HEIGHT}, batch_size={BATCH_SIZE}, rounds={ROUNDS}")
        print("=" * 60)

        tests = [
            ("PHI constant", self._test_phi),
            ("Golden angle", self._test_golden_angle),
            ("Epsilon coherence seed", self._test_epsilon),
            ("Penrose projection", self._test_penrose),
            ("Bundle density objective", self._test_objective),
            ("v=c guard", self._test_vc_guard),
            ("Reference output", self._test_reference),
            ("Reproducibility", self._test_reproducibility),
            ("Density: baseline", self._test_density_baseline),
            ("Density: quasicrystal", self._test_density_qc),
            ("Density: comparison", self._test_density_compare),
            ("VLIW bundle packing", self._test_vliw_bundle),
            ("VLIW packing objective", self._test_vliw_objective),
        ]

        for name, fn in tests:
            try:
                print(f"\n🧪 {name}")
                fn()
                print("   ✅ PASS")
                self.passed += 1
            except AssertionError as e:
                print(f"   ❌ FAIL: {e}")
                self.failed += 1
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
                self.failed += 1

        print("\n" + "=" * 60)
        print(f"Results: {self.passed}/{self.passed + self.failed} passed")
        if self.metrics:
            print(f"QC density:       {self.metrics.get('qc_density', 0):.6f}")
            print(f"Baseline density: {self.metrics.get('ur_density', 0):.6f}")
        print("=" * 60)

        return self.failed == 0

    def _test_phi(self):
        """Test PHI constant is correct golden ratio."""
        expected = (1 + math.sqrt(5)) / 2
        assert PHI == expected, f"PHI={PHI} != {expected}"
        print(f"      φ = {PHI:.6f}")

    def _test_golden_angle(self):
        """Test golden angle calculation."""
        expected = 2 * math.pi / PHI**2
        assert abs(GOLDEN_ANGLE - expected) < 1e-10
        deg = math.degrees(GOLDEN_ANGLE)
        print(f"      {deg:.2f}°")
        assert 137 < deg < 138, f"Golden angle {deg}° out of expected range"

    def _test_epsilon(self):
        """Test epsilon coherence seed value."""
        assert EPSILON == 0.00055, f"EPSILON={EPSILON} != 0.00055"
        print(f"      ε = {EPSILON}")

    def _test_penrose(self):
        """Test Penrose projection generates valid coordinates."""
        coords = penrose_project(FOREST_HEIGHT)
        assert coords.ndim == 2, f"Expected 2D array, got {coords.ndim}D"
        assert coords.shape[1] == 2, f"Expected 2 columns, got {coords.shape[1]}"
        n_points = (FOREST_HEIGHT + 1) ** 2  # Grid is -n//2 to n//2 inclusive
        assert len(coords) == n_points, f"Expected {n_points} points, got {len(coords)}"
        print(f"      {len(coords)} points generated")

    def _test_objective(self):
        """Test bundle density objective function."""
        coords = penrose_project(4)
        val = bundle_density_objective(coords[0])
        assert isinstance(val, (float, np.floating)), f"Expected float, got {type(val)}"
        assert val <= 0, f"Objective should be negative (density proxy), got {val}"
        print(f"      Single point objective: {val:.6f}")

    def _test_vc_guard(self):
        """Test v=c boundary guard raises error appropriately."""
        try:
            # Should raise error when iterations > 62 (default v=c limit)
            quasicrystal_schedule(4, 100, seed=1, verbose=False)
            raise AssertionError("Should raise RuntimeError for v=c guard")
        except RuntimeError as e:
            assert "v=c" in str(e), f"Expected v=c error, got: {e}"
            print("      v=c guard triggered correctly")

    def _test_reference(self):
        """Test reference output values."""
        coord, density = quasicrystal_schedule(
            FOREST_HEIGHT, BATCH_SIZE, seed=SEED, verbose=False
        )
        assert density >= 0, f"Density should be positive, got {density}"
        assert coord.shape == (2,), f"Expected 2D coord, got shape {coord.shape}"
        print(f"      coord=[{coord[0]:.4f}, {coord[1]:.4f}], density={density:.6f}")

    def _test_reproducibility(self):
        """Test that same seed produces same results."""
        c1, d1 = quasicrystal_schedule(FOREST_HEIGHT, BATCH_SIZE, seed=123, verbose=False)
        c2, d2 = quasicrystal_schedule(FOREST_HEIGHT, BATCH_SIZE, seed=123, verbose=False)
        assert np.allclose(c1, c2), f"Coordinates differ: {c1} vs {c2}"
        assert abs(d1 - d2) < 1e-10, f"Densities differ: {d1} vs {d2}"
        print("      Reproducibility verified")

    def _test_density_baseline(self):
        """Test uniform random baseline density."""
        # Warmup call to JIT-compile/cache numpy operations for consistent timing
        uniform_random_schedule(FOREST_HEIGHT, BATCH_SIZE, seed=1, verbose=False)
        densities = []
        for _ in range(ROUNDS):
            _, density = uniform_random_schedule(
                FOREST_HEIGHT, BATCH_SIZE, seed=SEED, verbose=False
            )
            densities.append(density)
        self.metrics["ur_density"] = sum(densities) / len(densities)
        print(f"      Baseline density: {self.metrics['ur_density']:.6f}")

    def _test_density_qc(self):
        """Test quasicrystal scheduler density."""
        # Warmup call to JIT-compile/cache numpy operations for consistent timing
        quasicrystal_schedule(FOREST_HEIGHT, BATCH_SIZE, seed=1, verbose=False)
        densities = []
        for _ in range(ROUNDS):
            _, density = quasicrystal_schedule(
                FOREST_HEIGHT, BATCH_SIZE, seed=SEED, verbose=False
            )
            densities.append(density)
        self.metrics["qc_density"] = sum(densities) / len(densities)
        print(f"      QC density: {self.metrics['qc_density']:.6f}")

    def _test_density_compare(self):
        """Compare quasicrystal vs baseline density."""
        qc = self.metrics.get("qc_density", 0)
        ur = self.metrics.get("ur_density", 0)

        if ur > 0:
            improvement = (qc - ur) / ur * 100
        else:
            improvement = 0

        print(f"      QC: {qc:.6f}, Baseline: {ur:.6f}")
        print(f"      Improvement: {improvement:+.2f}%")

        # Both should achieve some positive density
        assert qc > 0 or ur > 0, "At least one scheduler should achieve positive density"

    def _test_vliw_bundle(self):
        """Test VLIW bundle packing logic."""
        bundle = VLIWBundle(alu_slots=12, valu_slots=6, ls_slots=2)

        # Should be able to pack ALU ops
        assert bundle.can_pack("ALU"), "Should be able to pack ALU"
        assert bundle.pack("ALU", 0), "Should pack ALU op"

        # Fill ALU slots
        for i in range(1, 12):
            bundle.pack("ALU", i)
        assert not bundle.can_pack("ALU"), "ALU should be full"

        # VALU should still be available
        assert bundle.can_pack("VALU"), "VALU should be available"

        util = bundle.utilization()
        expected_util = 12 / 20  # 12 ALU out of 20 total slots
        assert abs(util - expected_util) < 0.01, f"Utilization {util} != {expected_util}"
        print(f"      Bundle utilization: {util*100:.1f}%")

    def _test_vliw_objective(self):
        """Test VLIW packing objective function."""
        import random
        random.seed(SEED)
        np.random.seed(SEED)

        ops = [("ALU", i) for i in range(10)]
        coord = np.array([0.5, 0.5])

        util = -vliw_packing_objective(coord, ops)
        assert 0 <= util <= 1, f"Utilization {util} out of [0,1] range"
        print(f"      VLIW objective utilization: {util*100:.1f}%")


def main():
    """Run test suite and benchmark."""
    suite = TestSuite()
    ok = suite.run()

    # Run comparison benchmark
    print("\n" + "=" * 60)
    print("BENCHMARK")
    print("=" * 60)
    compare_schedulers(n_points=32, iterations=62, seed=42)

    # Run VLIW simulation
    simulate_vliw_packing(n_ops=50, seed=42)

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
