# Answer: Which PR has the perf-takehome where they found the V=c paradox?

## Quick Answer

**PR #194**: `ATOM-FEATURE-20260122-002-quasicrystal-phason-scheduler`

**Link**: https://github.com/toolate28/SpiralSafe/pull/194

---

## The V=c Paradox: What It Is

The **V=c paradox** refers to a coherence boundary guard in the quasicrystal phason scheduler implementation. It's not a traditional physics paradox, but rather a **safeguard mechanism** that prevents "coherence collapse" in the optimization algorithm.

### Technical Details

**Location**: `experiments/quasicrystal_phason_scheduler.py`

**Default Limit**: 62 iterations (`DEFAULT_VC_GUARD_LIMIT = 62`)

**Guard Implementation** (lines 150-155):
```python
# v=c guard limit (can be overridden with vc_guard_override)
vc_limit = vc_guard_override if vc_guard_override is not None else DEFAULT_VC_GUARD_LIMIT

for it in range(iterations):
    if it > vc_limit:
        raise RuntimeError("v=c boundary guarded — coherence collapse prevented")
```

### What It Means

According to the SpiralSafe architecture:

1. **From `SUPERPOSITION_LOCK.md`** (line 61):
   - "Isomorphism breaks at v=c"
   
2. **From `docs/thread-crystallization/COMPLETE_THREAD.md`**:
   - "Isomorphism breaks at v=c, making this the coherence boundary"

The **v=c boundary** represents a topological limit where the isomorphism principle breaks down, analogous to how physics treats the speed of light (c) as an absolute boundary. At this boundary, the system's coherence guarantees can no longer be maintained.

---

## perf-takehome Integration

PR #194 includes a comprehensive integration proposal for `perf_takehome.py` (lines 405-447), proposing how to use quasicrystal scheduling for VLIW bundle packing optimization:

### Key Integration Points

1. **Coordinate-to-Priority Mapping**: Maps quasicrystal coordinates to operation scheduling priorities
2. **Bundle Packing Integration**: Uses quasicrystal-optimized coordinates to seed scheduling heuristics
3. **Benchmarking Comparison**: Expected 5-15% improvement in bundle utilization vs uniform random baseline
4. **Key Benefits**: Aperiodic exploration avoids local minima traps using golden ratio balance

### Example Integration Code (from PR)

```python
from quasicrystal_phason_scheduler import quasicrystal_schedule

def get_schedule_priority(ops):
    coord, density = quasicrystal_schedule(n_points=len(ops), iterations=62)
    # Map coordinate to priority using golden ratio projection
    priorities = [(coord[0] * PHI + coord[1]) for _ in range(len(ops))]
    return sorted(range(len(ops)), key=lambda i: priorities[i])
```

---

## PR #194 Summary

**Title**: ATOM-FEATURE-20260122-002-quasicrystal-phason-scheduler

**Status**: Merged on 2026-01-22

**Purpose**: Standalone quasicrystal scheduler with golden Penrose coordinates, phason flips, and VLIW bundle packing simulation. **Fixes the v=c guard by making iteration limit configurable.**

### What Changed

- `experiments/quasicrystal_phason_scheduler.py` — Pure first-principles implementation:
  - 5D→2D Penrose projection for aperiodic coordinates
  - Golden angle phason flips with Fibonacci-strided propagation
  - `VLIWBundle` class (12 ALU, 6 VALU, 2 LS slots)
  - **Configurable v=c guard via `vc_guard_override` parameter**
  - Benchmark comparison vs uniform random baseline
  - Integration proposal for perf_takehome.py (docstring)

- `experiments/test_quasicrystal_phason_scheduler.py` — 13 tests covering constants, projection, v=c guard, reproducibility, density comparison, VLIW packing

### The Original Problem

The original prompt in PR #194 mentioned that the code had a **hardcoded `if it > 62: raise RuntimeError`** that blocked any run exceeding 62 iterations. PR #194 fixed this by making the v=c guard configurable while still preserving the safety mechanism as a default.

### Key API

```python
# Default: 62 iterations (v=c guard)
coord, density = quasicrystal_schedule(n_points=32, seed=42)

# Override guard for longer runs
coord, density = quasicrystal_schedule(n_points=32, iterations=1000, vc_guard_override=1000)
```

---

## The Discovery Context

The original prompt from PR #194 referenced "the Anthropic take home test" and mentioned:

> "in order of priority, starting with the open PRs and the Anthropic take home test"

This suggests the v=c paradox was discovered during performance optimization work related to a take-home test assignment, where the 62-iteration limit became a practical constraint that needed to be understood and addressed.

---

## Related Files and References

- **Implementation**: `experiments/quasicrystal_phason_scheduler.py`
- **Tests**: `experiments/test_quasicrystal_phason_scheduler.py`
- **Theory**: `SUPERPOSITION_LOCK.md`
- **ATOM Tag**: `ATOM-FEATURE-20260122-002-quasicrystal-phason-scheduler`
- **Related PR**: #193 (quasicrystal optimization foundation)

---

## Key Takeaway

The **v=c paradox** is a coherence boundary safeguard at 62 iterations in the quasicrystal phason scheduler. **PR #194** is where this was documented, explained, and made configurable while maintaining the safety properties of the default guard. The integration with `perf_takehome.py` demonstrates how this theoretical boundary translates into practical performance optimization constraints.
