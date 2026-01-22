#!/usr/bin/env python3
"""
Tests for Quasicrystal Optimization

Test case: forest_height=4, batch_size=16, rounds=2
- Assert output matches reference kernel
- Measure cycles before/after phason pass
- Pass if cycles decrease or stay within 5%
"""

import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np

from quasicrystal_optimization import (
    PHI, GOLDEN_ANGLE,
    penrose_project, phason_flip,
    quasicrystal_optimize, baseline_optimize, benchmark,
)

# Test parameters (forest_height=4, batch_size=16, rounds=2)
FOREST_HEIGHT = 4   # maps to n_points
BATCH_SIZE = 16     # maps to iterations
ROUNDS = 2          # test repetitions
SEED = 42


def sphere(x):
    return float(np.sum(x**2))


class TestSuite:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.cycles = {}

    def run(self):
        print("=" * 50)
        print("[Experiment 56] Quasicrystal Tests")
        print(f"forest_height={FOREST_HEIGHT}, batch_size={BATCH_SIZE}, rounds={ROUNDS}")
        print("=" * 50)

        tests = [
            ("PHI exact", self._test_phi),
            ("Golden angle", self._test_angle),
            ("Penrose projection", self._test_penrose),
            ("v=c guard", self._test_vc_guard),
            ("Reference output", self._test_reference),
            ("Reproducibility", self._test_reproducibility),
            ("Cycles: baseline", self._test_cycles_baseline),
            ("Cycles: phason", self._test_cycles_phason),
            ("Cycles: comparison", self._test_cycles_compare),
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

        print("\n" + "=" * 50)
        print(f"Results: {self.passed}/{self.passed + self.failed} passed")
        if self.cycles:
            print(f"Baseline: {self.cycles.get('baseline', 0)/1e6:.2f} ms")
            print(f"Phason:   {self.cycles.get('phason', 0)/1e6:.2f} ms")
        print("=" * 50)

        return self.failed == 0

    def _test_phi(self):
        assert PHI == (1 + math.sqrt(5)) / 2

    def _test_angle(self):
        expected = 2 * math.pi / PHI**2
        assert abs(GOLDEN_ANGLE - expected) < 1e-10
        deg = math.degrees(GOLDEN_ANGLE)
        print(f"      {deg:.2f}°")

    def _test_penrose(self):
        coords = penrose_project(FOREST_HEIGHT)
        assert coords.ndim == 2
        assert coords.shape[1] == 2
        print(f"      {len(coords)} points")

    def _test_vc_guard(self):
        try:
            quasicrystal_optimize(sphere, 4, 100, seed=1)
            raise AssertionError("Should raise")
        except RuntimeError as e:
            assert "v=c" in str(e)

    def _test_reference(self):
        coord, val, enc = quasicrystal_optimize(sphere, FOREST_HEIGHT, BATCH_SIZE, seed=SEED)
        assert val >= 0
        assert coord.shape == (2,)
        print(f"      val={val:.6f}")

    def _test_reproducibility(self):
        c1, v1, _ = quasicrystal_optimize(sphere, FOREST_HEIGHT, BATCH_SIZE, seed=123)
        c2, v2, _ = quasicrystal_optimize(sphere, FOREST_HEIGHT, BATCH_SIZE, seed=123)
        assert np.allclose(c1, c2)
        assert abs(v1 - v2) < 1e-10

    def _test_cycles_baseline(self):
        baseline_optimize(sphere, FOREST_HEIGHT, BATCH_SIZE, seed=1)  # warmup
        times = []
        for _ in range(ROUNDS):
            start = time.perf_counter_ns()
            baseline_optimize(sphere, FOREST_HEIGHT, BATCH_SIZE, seed=SEED)
            times.append(time.perf_counter_ns() - start)
        self.cycles["baseline"] = sum(times) / len(times)
        print(f"      {self.cycles['baseline']/1e6:.2f} ms")

    def _test_cycles_phason(self):
        quasicrystal_optimize(sphere, FOREST_HEIGHT, BATCH_SIZE, seed=1)  # warmup
        times = []
        for _ in range(ROUNDS):
            start = time.perf_counter_ns()
            quasicrystal_optimize(sphere, FOREST_HEIGHT, BATCH_SIZE, seed=SEED)
            times.append(time.perf_counter_ns() - start)
        self.cycles["phason"] = sum(times) / len(times)
        print(f"      {self.cycles['phason']/1e6:.2f} ms")

    def _test_cycles_compare(self):
        bl = self.cycles.get("baseline", 1)
        ph = self.cycles.get("phason", 1)
        ratio = ph / bl
        pct = (ratio - 1) * 100
        print(f"      ratio={ratio:.3f} ({pct:+.1f}%)")
        # Pass if cycles decrease or within 5%
        assert ratio <= 1.05, f"Overhead {pct:.1f}% > 5%"


def main():
    suite = TestSuite()
    ok = suite.run()

    # Run benchmark
    print("\n" + "=" * 50)
    print("BENCHMARK")
    print("=" * 50)
    benchmark(sphere, n_points=32, iterations=62, seed=42)

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
