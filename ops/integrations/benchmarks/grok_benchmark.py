"""
Improved grok benchmark harness for xAI/Grok.
- Adds CLI (iterations, output dir)
- Writes a human-readable summary file that begins with the questions (one blank line), then a JSON payload
- Handles missing mocks gracefully
- Emits p50/p95 latencies
"""
import argparse
import json
import statistics
import time
from pathlib import Path
from typing import List, Dict, Any

QUERIES = [
    {"id": "q1", "query": "What is wave.md divergence and how to reduce it?"},
    {"id": "q2", "query": "How to measure curl in documents?"},
    {"id": "q3", "query": "Provide a short summary of coherence gates"},
]


def run_mock_grok(query: str, mock_xml_path: Path = None) -> Dict[str, Any]:
    """Deterministic mock that reads a predefined XML and returns a single top result.
    If the mock XML is missing, return a minimal fallback response.
    """
    if mock_xml_path and mock_xml_path.exists():
        import xml.etree.ElementTree as ET
        try:
            tree = ET.parse(str(mock_xml_path))
            root = tree.getroot()
            top = root.findall('.//result')[0]
            return {
                'query': query,
                'time_ms': 5,
                'results': [
                    {'title': top.findtext('title'), 'url': top.findtext('url'), 'snippet': top.findtext('snippet')}
                ]
            }
        except Exception:
            # fall through to fallback
            pass

    # Fallback deterministic response
    return {'query': query, 'time_ms': 1, 'results': [{'title': 'Fallback', 'url': '', 'snippet': ''}]}


def benchmark(queries: List[Dict[str, str]], iterations: int = 1, mock_dir: Path = None) -> Dict[str, Any]:
    runs = []
    for i in range(iterations):
        for q in queries:
            start = time.perf_counter()
            r = run_mock_grok(q['query'], mock_xml_path=(mock_dir / 'grok_web_search_response.xml') if mock_dir else None)
            dur = (time.perf_counter() - start) * 1000.0
            runs.append({'query_id': q['id'], 'query': q['query'], 'latency_ms': dur, 'hit': len(r.get('results', [])) > 0})

    latencies = [r['latency_ms'] for r in runs]
    summary = {
        'total_runs': len(runs),
        'avg_latency_ms': statistics.mean(latencies) if latencies else None,
        'p50_ms': statistics.median(latencies) if latencies else None,
        'p95_ms': statistics.quantiles(latencies, n=100)[94] if len(latencies) >= 2 else (max(latencies) if latencies else None),
    }

    return {'runs': runs, 'summary': summary}


def write_summary_with_questions(dest: Path, queries: List[Dict[str, str]], data: Dict[str, Any]) -> None:
    # Human-friendly prefix: list the questions, then one blank line, then JSON
    lines = []
    for q in queries:
        lines.append(f"- [{q['id']}] {q['query']}")
    lines.append('')
    lines.append(json.dumps(data, indent=2))
    dest.write_text('\n'.join(lines), encoding='utf-8')


def parse_args():
    p = argparse.ArgumentParser(description='Grok benchmark harness')
    p.add_argument('--iterations', '-n', type=int, default=1, help='Number of iterations per query')
    p.add_argument('--outdir', '-o', type=str, default=None, help='Directory to write output summary (if omitted, writes to ops/integrations/results)')
    p.add_argument('--mock-dir', type=str, default=None, help='Directory containing mock XML responses')
    return p.parse_args()


def find_repo_root(start: Path) -> Path:
    """
    Attempt to locate the repository root by walking up from ``start`` until a
    directory containing a ``.git`` marker is found. If no such directory is
    found, fall back to the directory containing ``start``.
    """
    for path in [start] + list(start.parents):
        if (path / '.git').is_dir():
            return path
    return start.parent


def main():
    args = parse_args()
    script_path = Path(__file__).resolve()
    repo_root = find_repo_root(script_path)
    outdir = Path(args.outdir) if args.outdir else (repo_root / 'ops' / 'integrations' / 'results')
    outdir.mkdir(parents=True, exist_ok=True)
    mock_dir = Path(args.mock_dir) if args.mock_dir else (repo_root / 'ops' / 'ops' / 'integrations' / 'xai-grok' / 'mocks')

    data = benchmark(QUERIES, iterations=args.iterations, mock_dir=mock_dir)

    summary_path = outdir / 'grok-benchmark-summary.txt'
    write_summary_with_questions(summary_path, QUERIES, data)
    # Also write machine-readable JSON
    (outdir / 'grok-benchmark-summary.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
    print('Wrote:', summary_path)


if __name__ == '__main__':
    main()
