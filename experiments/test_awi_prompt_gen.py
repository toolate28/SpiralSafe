#!/usr/bin/env python3
"""
Unit Tests for AWI Prompt Generation Module

Tests the AwiPromptGen module including:
- Integration between scaffolder and refiner
- Metadata propagation
- Edge cases (empty history, malformed intents)

ATOM-TEST-20260117-001-awi-prompt-gen-tests
"""

import sys
from pathlib import Path

# Add experiments to path
sys.path.insert(0, str(Path(__file__).parent))

from awi_prompt_gen import (
    AwiPromptGen,
    Prediction,
    get_coherence_examples,
    COHERENCE_HIGH_THRESHOLD,
)


class TestAwiPromptGen:
    """Test suite for AwiPromptGen module."""

    def __init__(self):
        self.passed = 0
        self.failed = 0

    def test(self, name: str, condition: bool, error_msg: str = ""):
        """Simple test assertion."""
        if condition:
            print(f"  ✅ PASS: {name}")
            self.passed += 1
        else:
            print(f"  ❌ FAIL: {name}")
            if error_msg:
                print(f"     Error: {error_msg}")
            self.failed += 1

    def run_all(self):
        """Run all tests."""
        print("=" * 60)
        print("AWI Prompt Generation Module - Unit Tests")
        print("=" * 60)

        self.test_scaffolder_refiner_integration()
        self.test_metadata_propagation()
        self.test_empty_history()
        self.test_malformed_intents()
        self.test_yaml_injection_prevention()
        self.test_permission_level_inference()
        self.test_coherence_examples()

        print("\n" + "=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        print("=" * 60)

        return self.failed == 0

    def test_scaffolder_refiner_integration(self):
        """Test that scaffolder and refiner work together correctly."""
        print("\n🧪 Testing: Scaffolder-Refiner Integration")

        gen = AwiPromptGen()
        result = gen(
            user_intent="Modify README.md to add section",
            history=[{"coherence": 0.85, "pattern": "file_operation"}]
        )

        self.test(
            "Result is Prediction",
            isinstance(result, Prediction),
            f"Expected Prediction, got {type(result)}"
        )
        self.test(
            "Result has content",
            len(result.content) > 0,
            "Content should not be empty"
        )
        self.test(
            "Result has reasoning",
            result.reasoning is not None,
            "Reasoning should be present"
        )
        self.test(
            "Result has metadata",
            len(result.metadata) > 0,
            "Metadata should not be empty"
        )
        self.test(
            "Content contains AWI markers",
            "AWI" in result.content or "intent" in result.content.lower(),
            "Content should contain AWI-related text"
        )

    def test_metadata_propagation(self):
        """Test that metadata propagates correctly through pipeline."""
        print("\n🧪 Testing: Metadata Propagation")

        gen = AwiPromptGen()
        result = gen(
            user_intent="Deploy API to production",
            history=[{"coherence": 0.9}]
        )

        self.test(
            "Metadata has scaffolding key",
            "scaffolding" in result.metadata,
            "Missing 'scaffolding' in metadata"
        )
        self.test(
            "Metadata has refinement key",
            "refinement" in result.metadata,
            "Missing 'refinement' in metadata"
        )
        self.test(
            "Metadata has pipeline key",
            result.metadata.get("pipeline") == "AwiPromptGen",
            f"Expected pipeline='AwiPromptGen', got {result.metadata.get('pipeline')}"
        )
        self.test(
            "Scaffolding has permission_level",
            "permission_level" in result.metadata.get("scaffolding", {}),
            "Missing permission_level in scaffolding metadata"
        )

    def test_empty_history(self):
        """Test handling of empty history."""
        print("\n🧪 Testing: Empty History Handling")

        gen = AwiPromptGen()

        # Test with None history
        result_none = gen(user_intent="Query database", history=None)
        self.test(
            "Handles None history",
            isinstance(result_none, Prediction) and len(result_none.content) > 0,
            "Should handle None history gracefully"
        )

        # Test with empty list
        result_empty = gen(user_intent="Query database", history=[])
        self.test(
            "Handles empty list history",
            isinstance(result_empty, Prediction) and len(result_empty.content) > 0,
            "Should handle empty list history gracefully"
        )

    def test_malformed_intents(self):
        """Test handling of malformed or edge-case intents."""
        print("\n🧪 Testing: Malformed Intent Handling")

        gen = AwiPromptGen()

        # Test with empty string
        result_empty = gen(user_intent="", history=[])
        self.test(
            "Handles empty intent",
            isinstance(result_empty, Prediction),
            "Should handle empty intent"
        )

        # Test with whitespace only
        result_whitespace = gen(user_intent="   ", history=[])
        self.test(
            "Handles whitespace intent",
            isinstance(result_whitespace, Prediction),
            "Should handle whitespace-only intent"
        )

        # Test with very long intent
        long_intent = "A" * 1000
        result_long = gen(user_intent=long_intent, history=[])
        self.test(
            "Handles very long intent",
            isinstance(result_long, Prediction) and len(result_long.content) > 0,
            "Should handle long intents"
        )

        # Test with special characters
        result_special = gen(user_intent="Do <something> & 'other' \"things\"", history=[])
        self.test(
            "Handles special characters",
            isinstance(result_special, Prediction),
            "Should handle special characters in intent"
        )

    def test_yaml_injection_prevention(self):
        """Test that YAML injection is properly prevented."""
        print("\n🧪 Testing: YAML Injection Prevention")

        gen = AwiPromptGen()

        # Test with YAML-breaking characters
        yaml_injection = 'test"\nmalicious: true\n  injected: "value'
        result = gen(user_intent=yaml_injection, history=[])
        
        self.test(
            "YAML injection characters are escaped",
            '\\n' in result.content or '\n  injected' not in result.content,
            "Newlines in intent should be escaped"
        )
        
        # Test with quotes
        quote_test = 'Do "something" with \'quotes\''
        result_quotes = gen(user_intent=quote_test, history=[])
        self.test(
            "Quotes are properly escaped",
            isinstance(result_quotes, Prediction),
            "Should handle quotes without breaking YAML structure"
        )

        # Test with malicious pattern in history
        malicious_history = [
            {"coherence": 0.9, "pattern": "normal_pattern\ninjected: malicious"},
            "string\nwith\nnewlines"
        ]
        result_history = gen(user_intent="Normal intent", history=malicious_history)
        # The sanitization should replace newlines with spaces, preventing structure break
        # Check that the pattern line doesn't have a literal newline followed by "injected"
        self.test(
            "Malicious history patterns are sanitized",
            isinstance(result_history, Prediction) and "\ninjected:" not in result_history.content,
            "Newlines in history patterns should be replaced with spaces"
        )

    def test_permission_level_inference(self):
        """Test that permission levels are correctly inferred."""
        print("\n🧪 Testing: Permission Level Inference")

        gen = AwiPromptGen()

        # Query intent should get lower permission level
        query_result = gen(user_intent="Query the database for users", history=[])
        query_perm = query_result.metadata.get("scaffolding", {}).get("permission_level")

        # System action should get higher permission level
        system_result = gen(user_intent="Deploy to production", history=[])
        system_perm = system_result.metadata.get("scaffolding", {}).get("permission_level")

        self.test(
            "Permission levels are integers",
            isinstance(query_perm, int) and isinstance(system_perm, int),
            f"Permission levels should be integers: query={query_perm}, system={system_perm}"
        )
        self.test(
            "Permission levels in valid range",
            0 <= query_perm <= 4 and 0 <= system_perm <= 4,
            f"Permission levels should be 0-4: query={query_perm}, system={system_perm}"
        )

    def test_coherence_examples(self):
        """Test coherence examples for COPRO optimization."""
        print("\n🧪 Testing: Coherence Examples")

        examples = get_coherence_examples()

        self.test(
            "Has positive examples",
            len(examples.get("positive", [])) > 0,
            "Should have positive coherence examples"
        )
        self.test(
            "Has negative examples",
            len(examples.get("negative", [])) > 0,
            "Should have negative coherence examples"
        )

        # Check positive examples have high coherence
        for ex in examples.get("positive", []):
            self.test(
                f"Positive example has high coherence ({ex.coherence_score})",
                ex.coherence_score >= COHERENCE_HIGH_THRESHOLD,
                f"Expected >= {COHERENCE_HIGH_THRESHOLD}, got {ex.coherence_score}"
            )
            self.test(
                "Positive example is_positive=True",
                ex.is_positive is True,
                "Positive example should have is_positive=True"
            )

        # Check negative examples have low coherence
        for ex in examples.get("negative", []):
            self.test(
                f"Negative example has low coherence ({ex.coherence_score})",
                ex.coherence_score < COHERENCE_HIGH_THRESHOLD,
                f"Expected < {COHERENCE_HIGH_THRESHOLD}, got {ex.coherence_score}"
            )


def main():
    """Run tests."""
    suite = TestAwiPromptGen()
    success = suite.run_all()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
