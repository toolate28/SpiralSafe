#!/usr/bin/env python3
"""
Unit tests for the Vortex Curl Vector Surjection Engine.

Tests the core functionality of the vortex system including:
- Fibonacci utilities
- VortexVector operations
- VortexSurjectionEngine metrics
- Surjection and collapse operations
"""

import sys
from pathlib import Path

# Add experiments to path
sys.path.insert(0, str(Path(__file__).parent))

from vortex_surjection import (
    fibonacci,
    fibonacci_weight,
    CollapsePoint,
    VortexVector,
    VortexType,
    VortexSurjectionEngine,
)


class VortexTestSuite:
    """Test suite for Vortex Curl Vector Surjection Engine."""

    def __init__(self):
        self.passed = 0
        self.failed = 0

    def test(self, name: str):
        """Decorator for test methods."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    print(f"\n🧪 Testing: {name}")
                    func(*args, **kwargs)
                    print(f"   ✅ PASS: {name}")
                    self.passed += 1
                except Exception as e:
                    print(f"   ❌ FAIL: {name}")
                    print(f"      Error: {e}")
                    self.failed += 1
            return wrapper
        return decorator

    def run_all(self):
        """Run all tests."""
        print("=" * 60)
        print("Vortex Curl Vector Surjection Engine - Test Suite")
        print("=" * 60)

        # Run each test manually
        tests = [
            ("Fibonacci number generation", self._test_fibonacci),
            ("Fibonacci weight normalization", self._test_fibonacci_weight),
            ("CollapsePoint creation", self._test_collapse_point),
            ("VortexVector creation", self._test_vortex_vector_creation),
            ("VortexVector self-maintaining", self._test_vortex_self_maintaining),
            ("VortexVector history accumulation", self._test_vortex_history_accumulation),
            ("VortexVector collapse", self._test_vortex_collapse),
            ("Engine creation", self._test_engine_creation),
            ("Engine add vortex", self._test_engine_add_vortex),
            ("Engine collapse proximity", self._test_engine_collapse_proximity),
            ("Engine emergence quality", self._test_engine_emergence_quality),
            ("Engine suggest action", self._test_engine_suggest_action),
            ("Engine iterate", self._test_engine_iterate),
            ("JSON serialization", self._test_json_serialization),
        ]

        for name, test_func in tests:
            try:
                print(f"\n🧪 Testing: {name}")
                test_func()
                print(f"   ✅ PASS: {name}")
                self.passed += 1
            except Exception as e:
                print(f"   ❌ FAIL: {name}")
                print(f"      Error: {e}")
                self.failed += 1

        print("\n" + "=" * 60)
        print(f"Test Results: {self.passed} passed, {self.failed} failed")
        print("=" * 60)

        return self.failed == 0

    def _test_fibonacci(self):
        """Test Fibonacci number generation."""
        # Known Fibonacci values
        assert fibonacci(0) == 0, "fibonacci(0) should be 0"
        assert fibonacci(1) == 1, "fibonacci(1) should be 1"
        assert fibonacci(2) == 1, "fibonacci(2) should be 1"
        assert fibonacci(5) == 5, "fibonacci(5) should be 5"
        assert fibonacci(8) == 21, "fibonacci(8) should be 21"
        assert fibonacci(13) == 233, "fibonacci(13) should be 233"

        print("      - Fibonacci sequence: OK")

    def _test_fibonacci_weight(self):
        """Test Fibonacci weight normalization."""
        # Test normalization
        weight_0 = fibonacci_weight(0)
        assert 0 <= weight_0 <= 1, "Weight should be normalized"

        weight_5 = fibonacci_weight(5)
        assert weight_5 > weight_0, "Higher index should have higher weight"

        weight_max = fibonacci_weight(20)
        assert weight_max == 1.0, "Max index should give weight 1.0"

        # Test bounding
        weight_bounded = fibonacci_weight(100, max_index=20)
        assert weight_bounded == 1.0, "Index should be bounded"

        print("      - Weight normalization: OK")

    def _test_collapse_point(self):
        """Test CollapsePoint creation and serialization."""
        cp = CollapsePoint(
            description="Test collapse",
            birthed_system="Test system",
            coherence=0.85,
        )

        assert cp.description == "Test collapse"
        assert cp.birthed_system == "Test system"
        assert cp.coherence == 0.85

        # Test serialization
        d = cp.to_dict()
        assert "description" in d
        assert "birthed_system" in d
        assert "coherence" in d
        assert "timestamp" in d

        print("      - CollapsePoint: OK")

    def _test_vortex_vector_creation(self):
        """Test VortexVector creation."""
        vortex = VortexVector(
            vector="Test vector",
            surjection_description="Test surjection",
            collapse_point=CollapsePoint(
                description="Test collapse",
                birthed_system="Test system",
            ),
            vortex_type=VortexType.QRC_HYBRID,
            fibonacci_weight=8,
            resonance_score=0.75,
        )

        assert vortex.vector == "Test vector"
        assert vortex.vortex_type == VortexType.QRC_HYBRID
        assert vortex.fibonacci_weight == 8
        assert vortex.resonance_score == 0.75

        print("      - VortexVector creation: OK")

    def _test_vortex_self_maintaining(self):
        """Test VortexVector self-maintaining property."""
        # Below threshold
        vortex_low = VortexVector(
            vector="Low resonance",
            surjection_description="Test",
            collapse_point=CollapsePoint("Test", "Test"),
            resonance_score=0.50,
        )
        assert not vortex_low.is_self_maintaining, "Should not be self-maintaining"

        # Above threshold
        vortex_high = VortexVector(
            vector="High resonance",
            surjection_description="Test",
            collapse_point=CollapsePoint("Test", "Test"),
            resonance_score=0.75,
        )
        assert vortex_high.is_self_maintaining, "Should be self-maintaining"

        # Exactly at threshold
        vortex_threshold = VortexVector(
            vector="Threshold",
            surjection_description="Test",
            collapse_point=CollapsePoint("Test", "Test"),
            resonance_score=0.60,
        )
        assert not vortex_threshold.is_self_maintaining, "Threshold should not be self-maintaining"

        print("      - Self-maintaining property: OK")

    def _test_vortex_history_accumulation(self):
        """Test VortexVector history accumulation."""
        vortex = VortexVector(
            vector="Test",
            surjection_description="Test",
            collapse_point=CollapsePoint("Test", "Test"),
        )

        assert len(vortex.history) == 0, "Should start empty"

        vortex.accumulate_history({"coherence": 0.8, "event": "test1"})
        assert len(vortex.history) == 1, "Should have 1 entry"

        vortex.accumulate_history({"coherence": 0.9, "event": "test2"})
        assert len(vortex.history) == 2, "Should have 2 entries"

        # Check structure
        entry = vortex.history[0]
        assert "state" in entry
        assert "timestamp" in entry
        assert "contribution" in entry

        print("      - History accumulation: OK")

    def _test_vortex_collapse(self):
        """Test VortexVector collapse operation."""
        vortex = VortexVector(
            vector="Test",
            surjection_description="Test",
            collapse_point=CollapsePoint("Test", "Test"),
        )

        # Add some history
        vortex.accumulate_history({"coherence": 0.8})
        vortex.accumulate_history({"coherence": 0.9})
        vortex.accumulate_history({"coherence": 0.7})

        # Collapse
        cp = vortex.collapse()

        assert cp.coherence > 0, "Collapse should update coherence"
        assert "history_length" in cp.metadata
        assert cp.metadata["history_length"] == 3

        print("      - Collapse operation: OK")

    def _test_engine_creation(self):
        """Test VortexSurjectionEngine creation."""
        engine = VortexSurjectionEngine("Test-VSE")

        assert engine.name == "Test-VSE"
        assert len(engine.vortexes) == 0
        assert engine.iteration == 0

        print("      - Engine creation: OK")

    def _test_engine_add_vortex(self):
        """Test adding vortexes to engine."""
        engine = VortexSurjectionEngine()

        # Add with custom key
        v1 = engine.create_qrc_hybrid_vortex(
            "Test QRC", "Collapse 1", "System 1"
        )
        key1 = engine.add_vortex(v1, "custom_key")
        assert key1 == "custom_key"
        assert "custom_key" in engine.vortexes

        # Add with auto key
        v2 = engine.create_qdi_prompt_vortex(
            "Test QDI", "Collapse 2", "System 2"
        )
        key2 = engine.add_vortex(v2)
        assert key2.startswith("vortex_")
        assert key2 in engine.vortexes

        print("      - Add vortex: OK")

    def _test_engine_collapse_proximity(self):
        """Test collapse proximity calculation."""
        engine = VortexSurjectionEngine()

        # Empty engine
        assert engine.collapse_proximity() == 0.0

        # Add vortexes with different weights and scores
        v1 = VortexVector(
            vector="V1",
            surjection_description="Test",
            collapse_point=CollapsePoint("Test", "Test"),
            fibonacci_weight=5,
            resonance_score=0.80,
        )
        v2 = VortexVector(
            vector="V2",
            surjection_description="Test",
            collapse_point=CollapsePoint("Test", "Test"),
            fibonacci_weight=8,
            resonance_score=0.90,
        )

        engine.add_vortex(v1, "v1")
        engine.add_vortex(v2, "v2")

        proximity = engine.collapse_proximity()
        # Weighted average: (0.80*5 + 0.90*8) / (5+8) = (4 + 7.2) / 13 ≈ 0.862
        assert 0.85 < proximity < 0.87, f"Proximity {proximity} out of expected range"

        print("      - Collapse proximity: OK")

    def _test_engine_emergence_quality(self):
        """Test emergence quality calculation."""
        engine = VortexSurjectionEngine()

        # Empty engine
        assert engine.emergence_quality() == 0.0

        # Add mixed vortexes
        v1 = VortexVector(
            vector="V1",
            surjection_description="Test",
            collapse_point=CollapsePoint("Test", "Test"),
            resonance_score=0.50,  # Below threshold
        )
        v2 = VortexVector(
            vector="V2",
            surjection_description="Test",
            collapse_point=CollapsePoint("Test", "Test"),
            resonance_score=0.80,  # Above threshold
        )
        v3 = VortexVector(
            vector="V3",
            surjection_description="Test",
            collapse_point=CollapsePoint("Test", "Test"),
            resonance_score=0.90,  # Above threshold
        )

        engine.add_vortex(v1, "v1")
        engine.add_vortex(v2, "v2")
        engine.add_vortex(v3, "v3")

        quality = engine.emergence_quality()
        # 2 out of 3 are self-maintaining
        assert quality == 2/3, f"Expected 2/3, got {quality}"

        print("      - Emergence quality: OK")

    def _test_engine_suggest_action(self):
        """Test action suggestion generation."""
        engine = VortexSurjectionEngine()

        # Empty engine
        suggestion = engine.suggest_action()
        assert "No active vortexes" in suggestion["suggestion"]

        # Add vortexes
        v1 = engine.create_qdi_prompt_vortex(
            "QDI Test", "Collapse QDI", "QDI System"
        )
        engine.add_vortex(v1, "qdi")

        suggestion = engine.suggest_action()
        assert "immediate_suggestion" in suggestion
        assert "strongest_resonance_vector" in suggestion
        assert "collapse_triggered" in suggestion

        print("      - Suggest action: OK")

    def _test_engine_iterate(self):
        """Test engine iteration."""
        engine = VortexSurjectionEngine()

        v1 = engine.create_qrc_hybrid_vortex(
            "QRC Test", "Collapse QRC", "QRC System"
        )
        v2 = engine.create_reservoir_audit_vortex(
            "Audit Test", "Collapse Audit", "Audit System"
        )

        engine.add_vortex(v1, "qrc")
        engine.add_vortex(v2, "audit")

        # Add some history
        engine.vortexes["qrc"].accumulate_history({"coherence": 0.8})
        engine.vortexes["audit"].accumulate_history({"coherence": 0.7})

        # Iterate
        result = engine.iterate()

        assert result["meta"]["iteration"] == 1
        assert "coherence_projection" in result["meta"]
        assert "emergent_quality" in result["meta"]
        assert "active_vortexes" in result
        assert len(result["active_vortexes"]) == 2

        print("      - Iteration: OK")

    def _test_json_serialization(self):
        """Test JSON export."""
        engine = VortexSurjectionEngine()

        v1 = engine.create_remix_vortex(
            "Remix Test",
            "Test surjection",
            "Test collapse",
            "Test system",
        )
        engine.add_vortex(v1, "remix")

        json_str = engine.to_json()

        assert "$schema" in json_str
        assert "vortex-curl-vector-surjection" in json_str
        assert "active_vortexes" in json_str

        # Should be valid JSON
        import json
        parsed = json.loads(json_str)
        assert "meta" in parsed
        assert "active_vortexes" in parsed

        print("      - JSON serialization: OK")


def main():
    """Run the test suite."""
    suite = VortexTestSuite()
    success = suite.run_all()

    if success:
        print("\n✨ ALL TESTS PASSED ✨\n")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED ❌\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
