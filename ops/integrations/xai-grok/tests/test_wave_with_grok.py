from pathlib import Path
from typing import List
import re

ROOT = Path(__file__).resolve().parents[2]
MOCK = ROOT / "mocks" / "grok_web_search_response.xml"


def compute_metrics(text: str) -> dict:
    # Simple proxies for curl & divergence (same style as CI coherence step)
    sentences = [s.strip() for s in re.split(r'[\.\n\?]+', text) if s.strip()]
    total = len(sentences)
    # repeated sentences = proxy for "curl"
    lower = [s.lower() for s in sentences]
    uniques = set(lower)
    curl = 0.0 if total == 0 else round(1.0 - (len(uniques) / total), 2)

    question_count = text.count('?')
    has_conclusion = bool(re.search(r'\b(therefore|thus|conclusions?|summary|in summary)\b', text, re.I))
    divergence = 0.2 if has_conclusion else min(0.3 + question_count * 0.05, 0.8)

    return {'curl': curl, 'divergence': round(divergence, 2), 'total_sentences': total}


def parse_snippets_from_grok(xml_path: Path, top_k: int = 2) -> List[str]:
    import xml.etree.ElementTree as ET
    tree = ET.parse(xml_path)
    root = tree.getroot()
    snippets = []
    for r in root.findall('.//result'):
        snippet = r.findtext('snippet') or ''
        relevance = float(r.findtext('relevance') or 0)
        snippets.append((relevance, snippet))
    snippets.sort(reverse=True)
    return [s for _, s in snippets[:top_k]]


def test_wave_metrics_improve_with_grok_evidence():
    baseline = (
        "How does wave.md measure divergence?\n"
        "What counts as curl?\n"
        "We are uncertain about whether the document resolves its questions.\n"
        "More questions remain."
    )

    base_metrics = compute_metrics(baseline)
    assert base_metrics['divergence'] >= 0.3

    snippets = parse_snippets_from_grok(MOCK, top_k=2)
    enriched = baseline + "\n\nReferences:\n" + "\n".join(snippets)

    enriched_metrics = compute_metrics(enriched)

    # divergence should decrease after adding evidence
    assert enriched_metrics['divergence'] <= base_metrics['divergence']
    # provide an actionable improvement threshold (non-arbitrary: 0.05 absolute)
    assert (base_metrics['divergence'] - enriched_metrics['divergence']) >= 0.05
    # curl should not increase significantly
    assert enriched_metrics['curl'] <= base_metrics['curl'] + 0.1
