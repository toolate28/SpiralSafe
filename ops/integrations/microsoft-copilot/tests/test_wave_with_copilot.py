"""
Tests for wave coherence analysis using Microsoft Copilot data.
Validates that adding evidence from Copilot improves wave metrics.
"""
import json
import re
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
MOCK_COPILOT = ROOT / "mocks" / "copilot_extension_response.json"


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
    has_conclusion = bool(re.search(r'\b(therefore|thus|conclusions?|summary|in summary|recommendation)\b', text, re.I))
    divergence = 0.2 if has_conclusion else min(0.3 + question_count * 0.05, 0.8)

    return {'curl': curl, 'divergence': round(divergence, 2), 'total_sentences': total}


def extract_copilot_insights(json_path: Path) -> List[str]:
    """Extract key insights from Copilot extension response."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    insights = []
    
    # Extract recommendations as insights
    recommendations = data['response']['analysis'].get('recommendations', [])
    for rec in recommendations:
        insights.append(f"Recommendation: {rec['suggestion']}")
    
    # Extract metrics summary
    metrics = data['response']['analysis']['metrics']
    insights.append(f"Coherence score: {metrics['coherence_score']}")
    
    return insights


def test_wave_metrics_improve_with_copilot_evidence():
    """
    Validate that adding Copilot-generated evidence reduces divergence.
    This mirrors the test pattern from xai-grok integration.
    """
    # Baseline: document with unresolved questions
    baseline = (
        "How should we structure the Azure OpenAI integration?\n"
        "What authentication method works best?\n"
        "We are uncertain about the optimal configuration.\n"
        "More questions need investigation."
    )
    
    base_metrics = compute_metrics(baseline)
    assert base_metrics['divergence'] >= 0.3, "Baseline should have high divergence"
    
    # Enrich with Copilot insights
    insights = extract_copilot_insights(MOCK_COPILOT)
    enriched = baseline + "\n\nAnalysis from Microsoft Copilot:\n" + "\n".join(insights)
    enriched += "\n\nIn summary, the analysis provides clear recommendations for improvement."
    
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


def test_copilot_mock_contains_wave_signature():
    """Verify Copilot response includes H&&S:WAVE handoff signature."""
    with open(MOCK_COPILOT, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    assert data['handoff']['protocol'] == 'H&&S:WAVE'
    assert data['response']['analysis']['wave_signature'] == 'H&&S:WAVE'


def test_metrics_bounds():
    """Validate that all metrics are within expected bounds."""
    with open(MOCK_COPILOT, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    metrics = data['response']['analysis']['metrics']
    
    for key in ['curl', 'divergence', 'potential', 'coherence_score']:
        assert 0.0 <= metrics[key] <= 1.0, f"{key} should be between 0 and 1"


def test_compute_metrics_edge_cases():
    """Test compute_metrics with edge cases."""
    # Empty text
    empty_metrics = compute_metrics("")
    assert empty_metrics['curl'] == 0.0
    assert empty_metrics['total_sentences'] == 0
    
    # Single sentence with conclusion
    single = "In summary, this is a conclusion."
    single_metrics = compute_metrics(single)
    assert single_metrics['divergence'] == 0.2
    
    # Repeated sentences (high curl)
    repeated = "Same text. Same text. Same text."
    repeated_metrics = compute_metrics(repeated)
    assert repeated_metrics['curl'] > 0.5
