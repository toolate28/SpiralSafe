"""
Tests for parsing OpenAI API responses.
Validates response structure and extracts key metrics.
"""
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Any

ROOT = Path(__file__).resolve().parents[1]
MOCK_CHAT = ROOT / "mocks" / "chat_completion_response.json"
MOCK_FUNCTION = ROOT / "mocks" / "function_call_response.json"


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class Message(BaseModel):
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[Any]] = None


class Choice(BaseModel):
    index: int
    message: Message
    logprobs: Optional[Any] = None
    finish_reason: str


class OpenAIChatResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
    system_fingerprint: Optional[str] = None


def parse_openai_chat_response(json_path: Path) -> OpenAIChatResponse:
    """Parse OpenAI Chat API response from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return OpenAIChatResponse(**data)


def test_chat_mock_exists():
    """Verify chat mock file exists."""
    assert MOCK_CHAT.exists(), f"Mock file not found: {MOCK_CHAT}"


def test_function_mock_exists():
    """Verify function call mock file exists."""
    assert MOCK_FUNCTION.exists(), f"Mock file not found: {MOCK_FUNCTION}"


def test_parse_openai_chat_response():
    """Parse and validate OpenAI Chat response structure."""
    response = parse_openai_chat_response(MOCK_CHAT)
    
    # Validate basic structure
    assert response.id.startswith('chatcmpl-')
    assert response.object == 'chat.completion'
    assert response.model.startswith('gpt-4')
    
    # Validate choices
    assert len(response.choices) >= 1
    assert response.choices[0].finish_reason == 'stop'
    assert response.choices[0].message.role == 'assistant'
    assert len(response.choices[0].message.content) > 0
    
    # Validate usage
    assert response.usage.total_tokens == response.usage.prompt_tokens + response.usage.completion_tokens
    assert response.usage.total_tokens > 0


def test_parse_function_call_response():
    """Parse and validate function call response structure."""
    response = parse_openai_chat_response(MOCK_FUNCTION)
    
    # Validate basic structure
    assert response.id.startswith('chatcmpl-')
    assert response.model.startswith('gpt-4')
    
    # Validate function call
    assert response.choices[0].finish_reason == 'tool_calls'
    assert response.choices[0].message.tool_calls is not None
    assert len(response.choices[0].message.tool_calls) >= 1
    
    # Validate tool call structure
    tool_call = response.choices[0].message.tool_calls[0]
    assert tool_call['type'] == 'function'
    assert tool_call['function']['name'] == 'analyze_wave_coherence'


def test_chat_response_contains_wave_metrics():
    """Verify chat response mentions wave coherence metrics."""
    response = parse_openai_chat_response(MOCK_CHAT)
    content = response.choices[0].message.content.lower()
    
    # Should mention coherence-related concepts
    assert 'divergence' in content
    assert 'curl' in content
    assert 'coherence' in content


def test_chat_response_contains_wave_signature():
    """Verify chat response includes H&&S:WAVE handoff signature."""
    response = parse_openai_chat_response(MOCK_CHAT)
    content = response.choices[0].message.content
    
    # Should include handoff signature
    assert 'H&&S:WAVE' in content


def test_function_call_arguments_valid_json():
    """Verify function call arguments are valid JSON."""
    response = parse_openai_chat_response(MOCK_FUNCTION)
    tool_call = response.choices[0].message.tool_calls[0]
    
    # Arguments should be parseable JSON
    args = json.loads(tool_call['function']['arguments'])
    
    # Should contain wave metrics
    assert 'metrics' in args
    assert 'curl' in args['metrics']
    assert 'divergence' in args['metrics']
    
    # Should contain handoff signature
    assert 'handoff' in args
    assert args['handoff']['signature'] == 'H&&S:WAVE'


def test_usage_metrics():
    """Validate usage metrics across both response types."""
    chat_response = parse_openai_chat_response(MOCK_CHAT)
    function_response = parse_openai_chat_response(MOCK_FUNCTION)
    
    for response in [chat_response, function_response]:
        assert response.usage.prompt_tokens > 0
        assert response.usage.completion_tokens > 0
        assert response.usage.total_tokens > 0
