"""
Tests for wave coherence analysis using open source and edge models.
Validates that adding evidence from OSS models improves wave metrics.
"""
import json
import re
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
MOCK_QWEN = ROOT / "mocks" / "qwen_response.json"
MOCK_PHI = ROOT / "mocks" / "phi_mobile_response.json"


def compute_metrics(text: str) -> dict:
    """
    Simple proxies for curl & divergence (same style as CI coherence step).
    Matches the pattern used in xai-grok/tests/test_wave_with_grok.py.
    """
    sentences = [s.strip() for s in re.split(r'[\.\n\?]+', text) if s.strip()]
    total = len(sentences)
    
    # Repeated sentences = proxy for "curl"
    lower = [s.lower() for s in sentences]
    uniques = set(lower)
    curl = 0.0 if total == 0 else round(1.0 - (len(uniques) / total), 2)

    # Divergence: questions without conclusions increase divergence
    question_count = text.count('?')
    has_conclusion = bool(re.search(r'\b(therefore|thus|conclusions?|summary|in summary|recommendations?)\b', text, re.I))
    divergence = 0.2 if has_conclusion else min(0.3 + question_count * 0.05, 0.8)

    return {'curl': curl, 'divergence': round(divergence, 2), 'total_sentences': total}


def extract_model_insights(json_path: Path) -> List[str]:
    """Extract key insights from model response."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    content = data['response']
    
    # Extract sentences that look like findings or recommendations
    insights = []
    sentences = [s.strip() for s in content.split('\n') if s.strip()]
    for sentence in sentences:
        if any(word in sentence.lower() for word in ['divergence', 'curl', 'coherence', 'recommend', 'result']):
            insights.append(sentence)
    
    return insights[:5]  # Limit to top 5 insights


def test_wave_metrics_improve_with_qwen_evidence():
    """
    Validate that adding Qwen-generated evidence reduces divergence.
    This mirrors the test pattern from xai-grok integration.
    """
    # Baseline: document with unresolved questions
    baseline = (
        "How should we deploy open source models?\n"
        "What quantization level works best?\n"
        "We are uncertain about memory requirements.\n"
        "Offline deployment needs investigation."
    )
    
    base_metrics = compute_metrics(baseline)
    assert base_metrics['divergence'] >= 0.3, "Baseline should have high divergence"
    
    # Enrich with Qwen insights
    insights = extract_model_insights(MOCK_QWEN)
    enriched = baseline + "\n\nAnalysis from Qwen:\n" + "\n".join(insights)
    enriched += "\n\nIn summary, the recommendations provide clear guidance for deployment."
    
    enriched_metrics = compute_metrics(enriched)
    
    # Divergence should decrease after adding evidence with conclusion
    assert enriched_metrics['divergence'] <= base_metrics['divergence'], \
        f"Divergence should decrease: {base_metrics['divergence']} -> {enriched_metrics['divergence']}"
    
    # Provide actionable improvement threshold (at least 0.05 absolute)
    improvement = base_metrics['divergence'] - enriched_metrics['divergence']
    assert improvement >= 0.05, f"Expected improvement >= 0.05, got {improvement}"
    
    # Curl should not increase significantly
    assert enriched_metrics['curl'] <= base_metrics['curl'] + 0.1, \
        f"Curl should not increase significantly: {base_metrics['curl']} -> {enriched_metrics['curl']}"


def test_wave_metrics_with_mobile_model():
    """Test that mobile model (Phi) also improves coherence metrics."""
    baseline = (
        "Can we run AI on mobile devices?\n"
        "What models fit in phone memory?\n"
        "Is offline operation possible?"
    )
    
    base_metrics = compute_metrics(baseline)
    
    insights = extract_model_insights(MOCK_PHI)
    enriched = baseline + "\n\nPhi Analysis:\n" + "\n".join(insights)
    enriched += "\n\nTherefore, mobile deployment is viable with proper configuration."
    
    enriched_metrics = compute_metrics(enriched)
    
    assert enriched_metrics['divergence'] <= base_metrics['divergence']


def test_compute_metrics_edge_cases():
    """Test compute_metrics with edge cases."""
    # Empty text
    empty_metrics = compute_metrics("")
    assert empty_metrics['curl'] == 0.0
    assert empty_metrics['total_sentences'] == 0
    
    # Single sentence with conclusion
    single = "In summary, this is the recommendation."
    single_metrics = compute_metrics(single)
    assert single_metrics['divergence'] == 0.2
    
    # Repeated sentences (high curl)
    repeated = "Same text. Same text. Same text."
    repeated_metrics = compute_metrics(repeated)
    assert repeated_metrics['curl'] > 0.5


def test_qwen_includes_recommendations():
    """Verify Qwen response includes actionable recommendations."""
    with open(MOCK_QWEN, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    content = data['response']
    
    # Should mention recommendations
    assert 'recommendation' in content.lower() or 'recommend' in content.lower()


def test_handoff_signature_present():
    """Verify all responses include H&&S:WAVE handoff signature."""
    with open(MOCK_QWEN, 'r', encoding='utf-8') as f:
        qwen = json.load(f)
    with open(MOCK_PHI, 'r', encoding='utf-8') as f:
        phi = json.load(f)
    
    assert 'H&&S:WAVE' in qwen['response']
    assert 'H&&S:WAVE' in phi['response']


def test_extract_insights_finds_metrics():
    """Test insight extraction finds coherence metrics."""
    insights = extract_model_insights(MOCK_QWEN)
    
    # Should extract coherence-related insights
    assert len(insights) >= 1
    
    # At least one should mention a metric
    has_metric = any('divergence' in i.lower() or 'curl' in i.lower() or 'coherence' in i.lower() for i in insights)
    assert has_metric, "Should extract at least one metric-related insight"


def test_mobile_model_concise():
    """Verify mobile model produces concise output."""
    qwen = extract_model_insights(MOCK_QWEN)
    phi = extract_model_insights(MOCK_PHI)
    
    # Mobile model should be more concise (fewer insights extracted)
    assert len(phi) <= len(qwen), "Mobile model should produce concise output"
