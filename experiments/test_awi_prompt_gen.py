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

import pytest

# Add experiments to path
sys.path.insert(0, str(Path(__file__).parent))

from awi_prompt_gen import (
    AwiPromptGen,
    Prediction,
    get_coherence_examples,
    COHERENCE_HIGH_THRESHOLD,
)


def test_scaffolder_refiner_integration():
    """Test that scaffolder and refiner work together correctly."""
    gen = AwiPromptGen()
    result = gen(
        user_intent="Modify README.md to add section",
        history=[{"coherence": 0.85, "pattern": "file_operation"}]
    )

    assert isinstance(result, Prediction), f"Expected Prediction, got {type(result)}"
    assert len(result.content) > 0, "Content should not be empty"
    assert result.reasoning is not None, "Reasoning should be present"
    assert len(result.metadata) > 0, "Metadata should not be empty"
    assert "AWI" in result.content or "intent" in result.content.lower(), \
        "Content should contain AWI-related text"


def test_metadata_propagation():
    """Test that metadata propagates correctly through pipeline."""
    gen = AwiPromptGen()
    result = gen(
        user_intent="Deploy API to production",
        history=[{"coherence": 0.9}]
    )

    assert "scaffolding" in result.metadata, "Missing 'scaffolding' in metadata"
    assert "refinement" in result.metadata, "Missing 'refinement' in metadata"
    assert result.metadata.get("pipeline") == "AwiPromptGen", \
        f"Expected pipeline='AwiPromptGen', got {result.metadata.get('pipeline')}"
    assert "permission_level" in result.metadata.get("scaffolding", {}), \
        "Missing permission_level in scaffolding metadata"


def test_empty_history():
    """Test handling of empty history."""
    gen = AwiPromptGen()

    # Test with None history
    result_none = gen(user_intent="Query database", history=None)
    assert isinstance(result_none, Prediction), "Should handle None history gracefully"
    assert len(result_none.content) > 0, "Content should not be empty with None history"

    # Test with empty list
    result_empty = gen(user_intent="Query database", history=[])
    assert isinstance(result_empty, Prediction), "Should handle empty list history gracefully"
    assert len(result_empty.content) > 0, "Content should not be empty with empty history"


def test_malformed_intents():
    """Test handling of malformed or edge-case intents."""
    gen = AwiPromptGen()

    # Test with empty string
    result_empty = gen(user_intent="", history=[])
    assert isinstance(result_empty, Prediction), "Should handle empty intent"

    # Test with whitespace only
    result_whitespace = gen(user_intent="   ", history=[])
    assert isinstance(result_whitespace, Prediction), "Should handle whitespace-only intent"

    # Test with very long intent
    long_intent = "A" * 1000
    result_long = gen(user_intent=long_intent, history=[])
    assert isinstance(result_long, Prediction), "Should handle long intents"
    assert len(result_long.content) > 0, "Content should not be empty for long intent"

    # Test with special characters
    result_special = gen(user_intent="Do <something> & 'other' \"things\"", history=[])
    assert isinstance(result_special, Prediction), "Should handle special characters in intent"


def test_yaml_injection_prevention():
    """Test that YAML injection is properly prevented."""
    gen = AwiPromptGen()

    # Test with YAML-breaking characters
    yaml_injection = 'test"\nmalicious: true\n  injected: "value'
    result = gen(user_intent=yaml_injection, history=[])
    
    assert '\\n' in result.content or '\n  injected' not in result.content, \
        "Newlines in intent should be escaped"
    
    # Test with quotes
    quote_test = 'Do "something" with \'quotes\''
    result_quotes = gen(user_intent=quote_test, history=[])
    assert isinstance(result_quotes, Prediction), \
        "Should handle quotes without breaking YAML structure"

    # Test with malicious pattern in history
    malicious_history = [
        {"coherence": 0.9, "pattern": "normal_pattern\ninjected: malicious"},
        "string\nwith\nnewlines"
    ]
    result_history = gen(user_intent="Normal intent", history=malicious_history)
    # The sanitization should replace newlines with spaces, preventing structure break
    # Check that the pattern line doesn't have a literal newline followed by "injected"
    assert isinstance(result_history, Prediction), "Should handle malicious history"
    assert "\ninjected:" not in result_history.content, \
        "Newlines in history patterns should be replaced with spaces"


def test_permission_level_inference():
    """Test that permission levels are correctly inferred."""
    gen = AwiPromptGen()

    # Query intent should get lower permission level
    query_result = gen(user_intent="Query the database for users", history=[])
    query_perm = query_result.metadata.get("scaffolding", {}).get("permission_level")

    # System action should get higher permission level
    system_result = gen(user_intent="Deploy to production", history=[])
    system_perm = system_result.metadata.get("scaffolding", {}).get("permission_level")

    assert isinstance(query_perm, int) and isinstance(system_perm, int), \
        f"Permission levels should be integers: query={query_perm}, system={system_perm}"
    assert 0 <= query_perm <= 4 and 0 <= system_perm <= 4, \
        f"Permission levels should be 0-4: query={query_perm}, system={system_perm}"


def test_coherence_examples():
    """Test coherence examples for COPRO optimization."""
    examples = get_coherence_examples()

    assert len(examples.get("positive", [])) > 0, "Should have positive coherence examples"
    assert len(examples.get("negative", [])) > 0, "Should have negative coherence examples"

    # Check positive examples have high coherence
    for ex in examples.get("positive", []):
        assert ex.coherence_score >= COHERENCE_HIGH_THRESHOLD, \
            f"Positive example should have high coherence: expected >= {COHERENCE_HIGH_THRESHOLD}, got {ex.coherence_score}"
        assert ex.is_positive is True, "Positive example should have is_positive=True"

    # Check negative examples have low coherence
    for ex in examples.get("negative", []):
        assert ex.coherence_score < COHERENCE_HIGH_THRESHOLD, \
            f"Negative example should have low coherence: expected < {COHERENCE_HIGH_THRESHOLD}, got {ex.coherence_score}"
