"""
Tests for wave coherence analysis using Meta LLaMA data.
Validates that adding evidence from LLaMA improves wave metrics.
"""
import json
import re
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
MOCK_GENERATE = ROOT / "mocks" / "ollama_generate_response.json"
MOCK_CHAT = ROOT / "mocks" / "ollama_chat_response.json"


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
    has_conclusion = bool(re.search(r'\b(therefore|thus|conclusions?|summary|in summary|recommendation|in conclusion)\b', text, re.I))
    divergence = 0.2 if has_conclusion else min(0.3 + question_count * 0.05, 0.8)

    return {'curl': curl, 'divergence': round(divergence, 2), 'total_sentences': total}


def extract_llama_insights(json_path: Path, is_chat: bool = False) -> List[str]:
    """Extract key insights from LLaMA response."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if is_chat:
        content = data['message']['content']
    else:
        content = data['response']
    
    # Extract sentences that look like findings or recommendations
    insights = []
    sentences = [s.strip() for s in content.split('\n') if s.strip()]
    for sentence in sentences:
        if any(word in sentence.lower() for word in ['divergence', 'curl', 'coherence', 'recommend', 'finding']):
            insights.append(sentence)
    
    return insights[:5]  # Limit to top 5 insights


def test_wave_metrics_improve_with_llama_evidence():
    """
    Validate that adding LLaMA-generated evidence reduces divergence.
    This mirrors the test pattern from xai-grok integration.
    """
    # Baseline: document with unresolved questions
    baseline = (
        "How should we deploy the LLaMA model locally?\n"
        "What quantization settings work best?\n"
        "We are uncertain about memory requirements.\n"
        "More performance testing is needed."
    )
    
    base_metrics = compute_metrics(baseline)
    assert base_metrics['divergence'] >= 0.3, "Baseline should have high divergence"
    
    # Enrich with LLaMA insights
    insights = extract_llama_insights(MOCK_GENERATE)
    enriched = baseline + "\n\nAnalysis from Meta LLaMA:\n" + "\n".join(insights)
    enriched += "\n\nIn conclusion, the analysis provides actionable guidance for deployment."
    
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


def test_chat_response_improves_coherence():
    """Test that chat response also improves coherence metrics."""
    baseline = (
        "What are the key metrics for documentation quality?\n"
        "How do we measure completeness?\n"
        "Are there any gaps in our coverage?"
    )
    
    base_metrics = compute_metrics(baseline)
    
    insights = extract_llama_insights(MOCK_CHAT, is_chat=True)
    enriched = baseline + "\n\nLLaMA Chat Response:\n" + "\n".join(insights)
    enriched += "\n\nTherefore, we have clear metrics and improvement paths."
    
    enriched_metrics = compute_metrics(enriched)
    
    assert enriched_metrics['divergence'] <= base_metrics['divergence']


def test_compute_metrics_edge_cases():
    """Test compute_metrics with edge cases."""
    # Empty text
    empty_metrics = compute_metrics("")
    assert empty_metrics['curl'] == 0.0
    assert empty_metrics['total_sentences'] == 0
    
    # Single sentence with conclusion
    single = "In conclusion, this is the summary."
    single_metrics = compute_metrics(single)
    assert single_metrics['divergence'] == 0.2
    
    # Repeated sentences (high curl)
    repeated = "Same text. Same text. Same text."
    repeated_metrics = compute_metrics(repeated)
    assert repeated_metrics['curl'] > 0.5


def test_extract_insights_from_generate():
    """Test insight extraction from generate response."""
    insights = extract_llama_insights(MOCK_GENERATE)
    
    # Should extract coherence-related insights
    assert len(insights) >= 1
    
    # At least one should mention a metric
    has_metric = any('divergence' in i.lower() or 'curl' in i.lower() or 'coherence' in i.lower() for i in insights)
    assert has_metric, "Should extract at least one metric-related insight"


def test_extract_insights_from_chat():
    """Test insight extraction from chat response."""
    insights = extract_llama_insights(MOCK_CHAT, is_chat=True)
    
    # Should extract coherence-related insights
    assert len(insights) >= 1
