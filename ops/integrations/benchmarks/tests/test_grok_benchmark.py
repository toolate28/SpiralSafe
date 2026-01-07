import json
from ops.integrations.benchmarks.grok_benchmark import benchmark, write_summary_with_questions, QUERIES


def test_benchmark_basic(tmp_path):
    data = benchmark(QUERIES, iterations=2, mock_dir=tmp_path)  # tmp_path has no mocks -> fallback
    assert data['summary']['total_runs'] == len(QUERIES) * 2
    assert data['summary']['avg_latency_ms'] is not None


def test_write_summary(tmp_path):
    out = tmp_path / 'summary.txt'
    data = {'runs': [], 'summary': {'total_runs': 0}}
    write_summary_with_questions(out, QUERIES, data)
    text = out.read_text(encoding='utf-8')
    # First line should include first query id
    assert f"[{QUERIES[0]['id']}]" in text
    # There should be a blank line separating queries from JSON
    assert '\n\n' in text
    # JSON should be valid
    assert json.loads(text.split('\n\n',1)[1])
