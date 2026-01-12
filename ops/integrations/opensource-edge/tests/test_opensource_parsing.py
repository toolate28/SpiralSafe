"""
Tests for parsing open source and edge model API responses.
Validates response structure for Qwen, Phi, and other OSS models.
"""
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Any

ROOT = Path(__file__).resolve().parents[1]
MOCK_QWEN = ROOT / "mocks" / "qwen_response.json"
MOCK_PHI = ROOT / "mocks" / "phi_mobile_response.json"


class SpiralSafeMetadata(BaseModel):
    provider: str
    runtime: str
    quantization: Optional[str] = None
    offline_capable: bool = True
    model_type: Optional[str] = None
    device_optimized: Optional[List[str]] = None
    memory_mb: Optional[int] = None


class OpenSourceResponse(BaseModel):
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
    spiralsafe_metadata: Optional[SpiralSafeMetadata] = None


def parse_opensource_response(json_path: Path) -> OpenSourceResponse:
    """Parse open source model response from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return OpenSourceResponse(**data)


def test_qwen_mock_exists():
    """Verify Qwen mock file exists."""
    assert MOCK_QWEN.exists(), f"Mock file not found: {MOCK_QWEN}"


def test_phi_mock_exists():
    """Verify Phi mobile mock file exists."""
    assert MOCK_PHI.exists(), f"Mock file not found: {MOCK_PHI}"


def test_parse_qwen_response():
    """Parse and validate Qwen response structure."""
    response = parse_opensource_response(MOCK_QWEN)
    
    # Validate basic structure
    assert response.model.startswith('qwen')
    assert response.done is True
    assert len(response.response) > 0
    
    # Validate timing information
    assert response.total_duration is not None
    assert response.total_duration > 0
    
    # Validate SpiralSafe metadata
    assert response.spiralsafe_metadata is not None
    assert response.spiralsafe_metadata.provider == 'opensource-edge'
    assert response.spiralsafe_metadata.runtime == 'ollama'


def test_parse_phi_mobile_response():
    """Parse and validate Phi mobile response structure."""
    response = parse_opensource_response(MOCK_PHI)
    
    # Validate basic structure
    assert response.model.startswith('phi')
    assert response.done is True
    assert len(response.response) > 0
    
    # Validate mobile-specific metadata
    assert response.spiralsafe_metadata is not None
    assert response.spiralsafe_metadata.model_type == 'mobile'
    assert response.spiralsafe_metadata.device_optimized is not None
    assert 'ios' in response.spiralsafe_metadata.device_optimized
    assert 'android' in response.spiralsafe_metadata.device_optimized


def test_qwen_response_contains_wave_metrics():
    """Verify Qwen response mentions wave coherence metrics."""
    response = parse_opensource_response(MOCK_QWEN)
    content = response.response.lower()
    
    # Should mention coherence-related concepts
    assert 'divergence' in content
    assert 'curl' in content
    assert 'coherence' in content


def test_phi_response_contains_wave_signature():
    """Verify Phi response includes H&&S:WAVE handoff signature."""
    response = parse_opensource_response(MOCK_PHI)
    content = response.response
    
    # Should include handoff signature
    assert 'H&&S:WAVE' in content


def test_offline_capable_flag():
    """Verify all open source models support offline mode."""
    qwen = parse_opensource_response(MOCK_QWEN)
    phi = parse_opensource_response(MOCK_PHI)
    
    assert qwen.spiralsafe_metadata.offline_capable is True
    assert phi.spiralsafe_metadata.offline_capable is True


def test_quantization_info_present():
    """Validate quantization information is present."""
    qwen = parse_opensource_response(MOCK_QWEN)
    phi = parse_opensource_response(MOCK_PHI)
    
    # Both should have quantization specified
    assert qwen.spiralsafe_metadata.quantization is not None
    assert phi.spiralsafe_metadata.quantization is not None
    
    # Should be valid quantization formats
    valid_quants = ['q4_0', 'q4_K_M', 'q5_K_M', 'q8_0']
    assert qwen.spiralsafe_metadata.quantization in valid_quants
    assert phi.spiralsafe_metadata.quantization in valid_quants


def test_mobile_memory_constraint():
    """Verify mobile model specifies memory requirement."""
    phi = parse_opensource_response(MOCK_PHI)
    
    assert phi.spiralsafe_metadata.memory_mb is not None
    # Mobile models should fit in reasonable memory
    assert phi.spiralsafe_metadata.memory_mb <= 8192


def test_performance_comparison():
    """Compare performance metrics between full and mobile models."""
    qwen = parse_opensource_response(MOCK_QWEN)
    phi = parse_opensource_response(MOCK_PHI)
    
    # Mobile model should be faster (lower total duration)
    assert phi.total_duration < qwen.total_duration
    
    # Mobile model should use fewer tokens
    assert phi.eval_count < qwen.eval_count
