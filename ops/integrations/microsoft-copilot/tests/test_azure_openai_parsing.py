"""
Tests for parsing Azure OpenAI API responses.
Validates response structure and extracts key metrics.
"""
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional

ROOT = Path(__file__).resolve().parents[1]
MOCK_AZURE = ROOT / "mocks" / "azure_openai_response.json"
MOCK_COPILOT = ROOT / "mocks" / "copilot_extension_response.json"


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class Message(BaseModel):
    role: str
    content: str


class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: str


class AzureOpenAIResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
    system_fingerprint: Optional[str] = None


class WaveMetrics(BaseModel):
    curl: float = Field(..., ge=0.0, le=1.0)
    divergence: float = Field(..., ge=0.0, le=1.0)
    potential: float = Field(..., ge=0.0, le=1.0)
    coherence_score: float = Field(..., ge=0.0, le=1.0)


class Recommendation(BaseModel):
    type: str
    location: str
    suggestion: str


class Analysis(BaseModel):
    document: str
    metrics: WaveMetrics
    recommendations: List[Recommendation]
    wave_signature: str


class CopilotExtensionResponse(BaseModel):
    extension: str
    skill: str
    version: str


def parse_azure_openai_response(json_path: Path) -> AzureOpenAIResponse:
    """Parse Azure OpenAI API response from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return AzureOpenAIResponse(**data)


def parse_copilot_extension_response(json_path: Path) -> dict:
    """Parse Copilot extension response from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def test_azure_mock_exists():
    """Verify mock file exists."""
    assert MOCK_AZURE.exists(), f"Mock file not found: {MOCK_AZURE}"


def test_copilot_mock_exists():
    """Verify Copilot extension mock file exists."""
    assert MOCK_COPILOT.exists(), f"Mock file not found: {MOCK_COPILOT}"


def test_parse_azure_openai_response():
    """Parse and validate Azure OpenAI response structure."""
    response = parse_azure_openai_response(MOCK_AZURE)
    
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


def test_parse_copilot_extension_response():
    """Parse and validate Copilot extension response structure."""
    data = parse_copilot_extension_response(MOCK_COPILOT)
    
    # Validate extension metadata
    assert data['extension'] == 'spiralsafe'
    assert data['skill'] == 'wave_analysis'
    
    # Validate analysis metrics
    metrics = data['response']['analysis']['metrics']
    assert 0 <= metrics['curl'] <= 1.0
    assert 0 <= metrics['divergence'] <= 1.0
    assert 0 <= metrics['coherence_score'] <= 1.0
    
    # Validate H&&S:WAVE signature
    assert data['response']['analysis']['wave_signature'] == 'H&&S:WAVE'
    assert data['handoff']['protocol'] == 'H&&S:WAVE'


def test_extract_wave_metrics_from_content():
    """Extract wave metrics from Azure OpenAI response content."""
    response = parse_azure_openai_response(MOCK_AZURE)
    content = response.choices[0].message.content
    
    # Should mention divergence and curl metrics
    assert 'divergence' in content.lower()
    assert 'curl' in content.lower()
    assert 'coherence' in content.lower()


def test_recommendations_structure():
    """Validate recommendations in Copilot extension response."""
    data = parse_copilot_extension_response(MOCK_COPILOT)
    recommendations = data['response']['analysis']['recommendations']
    
    assert len(recommendations) >= 1
    for rec in recommendations:
        assert 'type' in rec
        assert 'location' in rec
        assert 'suggestion' in rec
