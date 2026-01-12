"""
Tests for wave coherence analysis using OpenAI GPT data.
Validates that adding evidence from GPT improves wave metrics.
"""
import json
import re
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
MOCK_CHAT = ROOT / "mocks" / "chat_completion_response.json"
MOCK_FUNCTION = ROOT / "mocks" / "function_call_response.json"


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


def extract_gpt_insights(json_path: Path) -> List[str]:
    """Extract key insights from GPT chat response."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    content = data['choices'][0]['message'].get('content', '')
    if not content:
        return []
    
    # Extract sentences that look like findings or recommendations
    insights = []
    sentences = [s.strip() for s in content.split('\n') if s.strip()]
    for sentence in sentences:
        if any(word in sentence.lower() for word in ['divergence', 'curl', 'coherence', 'recommend', 'observation']):
            insights.append(sentence)
    
    return insights[:5]  # Limit to top 5 insights


def extract_function_call_metrics(json_path: Path) -> dict:
    """Extract wave metrics from function call response."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tool_call = data['choices'][0]['message']['tool_calls'][0]
    args = json.loads(tool_call['function']['arguments'])
    
    return args.get('metrics', {})


def test_wave_metrics_improve_with_gpt_evidence():
    """
    Validate that adding GPT-generated evidence reduces divergence.
    This mirrors the test pattern from xai-grok integration.
    """
    # Baseline: document with unresolved questions
    baseline = (
        "How should we implement the OpenAI integration?\n"
        "What model should we use for production?\n"
        "We are uncertain about cost optimization.\n"
        "Rate limiting strategy needs investigation."
    )
    
    base_metrics = compute_metrics(baseline)
    assert base_metrics['divergence'] >= 0.3, "Baseline should have high divergence"
    
    # Enrich with GPT insights
    insights = extract_gpt_insights(MOCK_CHAT)
    enriched = baseline + "\n\nAnalysis from OpenAI GPT:\n" + "\n".join(insights)
    enriched += "\n\nIn summary, the recommendations provide clear guidance for implementation."
    
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


def test_function_call_contains_wave_metrics():
    """Verify function call response contains valid wave metrics."""
    metrics = extract_function_call_metrics(MOCK_FUNCTION)
    
    # All metrics should be present
    assert 'curl' in metrics
    assert 'divergence' in metrics
    assert 'coherence_score' in metrics
    
    # All metrics should be in valid range
    for key in ['curl', 'divergence', 'coherence_score']:
        assert 0.0 <= metrics[key] <= 1.0, f"{key} should be between 0 and 1"


def test_chat_response_includes_recommendations():
    """Verify chat response includes actionable recommendations."""
    with open(MOCK_CHAT, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    content = data['choices'][0]['message']['content']
    
    # Should mention recommendations
    assert 'recommendation' in content.lower() or 'recommend' in content.lower()


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


def test_handoff_signature_in_function_call():
    """Verify function call includes H&&S:WAVE handoff signature."""
    with open(MOCK_FUNCTION, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tool_call = data['choices'][0]['message']['tool_calls'][0]
    args = json.loads(tool_call['function']['arguments'])
    
    assert 'handoff' in args
    assert args['handoff']['signature'] == 'H&&S:WAVE'
