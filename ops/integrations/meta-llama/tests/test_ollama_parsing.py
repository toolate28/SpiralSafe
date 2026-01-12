"""
Tests for parsing Ollama API responses.
Validates response structure and extracts key metrics.
"""
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional

ROOT = Path(__file__).resolve().parents[1]
MOCK_GENERATE = ROOT / "mocks" / "ollama_generate_response.json"
MOCK_CHAT = ROOT / "mocks" / "ollama_chat_response.json"


class OllamaGenerateResponse(BaseModel):
    model: str
    created_at: str
    response: str
    done: bool
    context: Optional[List[int]] = None
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None


class Message(BaseModel):
    role: str
    content: str


class OllamaChatResponse(BaseModel):
    model: str
    created_at: str
    message: Message
    done: bool
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None


def parse_ollama_generate_response(json_path: Path) -> OllamaGenerateResponse:
    """Parse Ollama generate API response from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return OllamaGenerateResponse(**data)


def parse_ollama_chat_response(json_path: Path) -> OllamaChatResponse:
    """Parse Ollama chat API response from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return OllamaChatResponse(**data)


def test_generate_mock_exists():
    """Verify generate mock file exists."""
    assert MOCK_GENERATE.exists(), f"Mock file not found: {MOCK_GENERATE}"


def test_chat_mock_exists():
    """Verify chat mock file exists."""
    assert MOCK_CHAT.exists(), f"Mock file not found: {MOCK_CHAT}"


def test_parse_ollama_generate_response():
    """Parse and validate Ollama generate response structure."""
    response = parse_ollama_generate_response(MOCK_GENERATE)
    
    # Validate basic structure
    assert response.model.startswith('llama')
    assert response.done is True
    assert len(response.response) > 0
    
    # Validate timing information
    assert response.total_duration is not None
    assert response.total_duration > 0
    assert response.eval_count is not None
    assert response.eval_count > 0


def test_parse_ollama_chat_response():
    """Parse and validate Ollama chat response structure."""
    response = parse_ollama_chat_response(MOCK_CHAT)
    
    # Validate basic structure
    assert response.model.startswith('llama')
    assert response.done is True
    
    # Validate message
    assert response.message.role == 'assistant'
    assert len(response.message.content) > 0
    
    # Validate timing information
    assert response.total_duration is not None


def test_generate_response_contains_wave_metrics():
    """Verify generate response mentions wave coherence metrics."""
    response = parse_ollama_generate_response(MOCK_GENERATE)
    content = response.response.lower()
    
    # Should mention coherence-related concepts
    assert 'divergence' in content
    assert 'curl' in content
    assert 'coherence' in content


def test_chat_response_contains_wave_signature():
    """Verify chat response includes H&&S:WAVE handoff signature."""
    response = parse_ollama_chat_response(MOCK_CHAT)
    content = response.message.content
    
    # Should include handoff signature
    assert 'H&&S:WAVE' in content


def test_performance_metrics_present():
    """Validate performance timing metrics are present."""
    generate = parse_ollama_generate_response(MOCK_GENERATE)
    chat = parse_ollama_chat_response(MOCK_CHAT)
    
    # Generate response should have detailed timing
    assert generate.prompt_eval_duration is not None
    assert generate.eval_duration is not None
    
    # Both should have total duration
    assert generate.total_duration > 0
    assert chat.total_duration > 0


def test_tokens_per_second_calculation():
    """Calculate tokens per second from response timing."""
    response = parse_ollama_generate_response(MOCK_GENERATE)
    
    if response.eval_count and response.eval_duration:
        # eval_duration is in nanoseconds
        tokens_per_second = response.eval_count / (response.eval_duration / 1e9)
        # Should be positive and reasonable
        assert tokens_per_second > 0
        assert tokens_per_second < 10000  # Sanity check upper bound
