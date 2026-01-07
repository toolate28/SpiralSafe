"""
Lightweight benchmark harness for xAI/Grok vs other adapters.
Produces JSON summary with latency, hit_rate, coherence_delta placeholders.
This is a skeleton intended to be run manually or via scheduled CI.
"""
import json
from pathlib import Path
import time

QUERIES = [
    {"id": "q1", "query": "What is wave.md divergence and how to reduce it?"},
    {"id": "q2", "query": "How to measure curl in documents?"},
    {"id": "q3", "query": "Provide a short summary of coherence gates"},
]

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def run_mock_grok(query: str):
    # Deterministic mock: returns the static mock snippets
    from pathlib import Path
    xml = Path(__file__).resolve().parents[1] / "xai-grok" / "mocks" / "grok_web_search_response.xml"
    import xml.etree.ElementTree as ET
    tree = ET.parse(xml)
    root = tree.getroot()
    top = root.findall('.//result')[0]
    return {
        'query': query,
        'time_ms': 5,
        'results': [
            { 'title': top.findtext('title'), 'url': top.findtext('url'), 'snippet': top.findtext('snippet') }
        ]
    }


def benchmark():
    out = {'runs': [], 'summary': {}}
    for q in QUERIES:
        start = time.time()
        r = run_mock_grok(q['query'])
        dur = (time.time() - start) * 1000.0
        out['runs'].append({
            'query_id': q['id'],
            'query': q['query'],
            'latency_ms': dur,
            'hit': len(r['results']) > 0,
        })
    out['summary']['total_runs'] = len(out['runs'])
    out['summary']['avg_latency_ms'] = sum(r['latency_ms'] for r in out['runs']) / len(out['runs'])

    dest = RESULTS_DIR / f"grok-benchmark-summary.json"
    dest.write_text(json.dumps(out, indent=2))
    print("Wrote:", dest)


if __name__ == '__main__':
    benchmark()
