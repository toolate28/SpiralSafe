import json
from ops.integrations.benchmarks.grok_benchmark import benchmark, write_summary_with_questions, QUERIES, run_mock_grok


def test_benchmark_basic(tmp_path):
    data = benchmark(QUERIES, iterations=2, mock_dir=tmp_path)  # tmp_path has no mocks -> fallback
    assert data['summary']['total_runs'] == len(QUERIES) * 2
    assert data['summary']['avg_latency_ms'] is not None


def test_write_summary(tmp_path):
    out = tmp_path / 'summary.txt'
    data = {'runs': [], 'summary': {'total_runs': 0}}
    write_summary_with_questions(out, QUERIES, data)
    text = out.read_text(encoding='utf-8')
    # Should include the mock benchmark header
    assert '# MOCK BENCHMARK RESULTS' in text
    assert 'NOT real API call performance' in text
    # First line should include first query id
    assert f"[{QUERIES[0]['id']}]" in text
    # There should be a blank line separating queries from JSON
    assert '\n\n' in text
    # JSON should be valid and contain expected structure - find the JSON part after all headers
    lines = text.split('\n')
    json_start = None
    for i, line in enumerate(lines):
        if line.strip().startswith('{'):
            json_start = i
            break
    assert json_start is not None, "JSON object not found in output"
    parsed_json = json.loads('\n'.join(lines[json_start:]))
    assert 'runs' in parsed_json
    assert 'summary' in parsed_json
    assert parsed_json['summary']['total_runs'] == 0


def test_xml_parsing_success(tmp_path):
    """Test that valid XML mock files are parsed correctly."""
    mock_file = tmp_path / 'test_mock.xml'
    xml_content = """<?xml version="1.0"?>
<response>
    <result>
        <title>Test Title</title>
        <url>https://example.com</url>
        <snippet>Test snippet content</snippet>
    </result>
</response>"""
    mock_file.write_text(xml_content, encoding='utf-8')
    
    result = run_mock_grok("test query", mock_xml_path=mock_file)
    assert result['query'] == "test query"
    assert len(result['results']) == 1
    assert result['results'][0]['title'] == 'Test Title'
    assert result['results'][0]['url'] == 'https://example.com'
    assert result['results'][0]['snippet'] == 'Test snippet content'


def test_xml_parsing_malformed(tmp_path):
    """Test that malformed XML falls back to deterministic response."""
    mock_file = tmp_path / 'bad_mock.xml'
    mock_file.write_text("not valid xml <><>", encoding='utf-8')
    
    result = run_mock_grok("test query", mock_xml_path=mock_file)
    assert result['query'] == "test query"
    assert result['results'][0]['title'] == 'Fallback'


def test_xml_parsing_missing_results(tmp_path):
    """Test that XML without result elements falls back gracefully."""
    mock_file = tmp_path / 'empty_mock.xml'
    xml_content = """<?xml version="1.0"?>
<response>
    <no_results/>
</response>"""
    mock_file.write_text(xml_content, encoding='utf-8')
    
    result = run_mock_grok("test query", mock_xml_path=mock_file)
    assert result['query'] == "test query"
    assert result['results'][0]['title'] == 'Fallback'


def test_p95_calculation_edge_cases(tmp_path):
    """Test p95 calculation with various sample sizes."""
    # Single sample: should use max (fallback)
    data = benchmark(QUERIES[:1], iterations=1, mock_dir=tmp_path)
    assert data['summary']['p95_ms'] is not None
    
    # Two samples: should use quantiles
    data = benchmark(QUERIES[:1], iterations=2, mock_dir=tmp_path)
    assert data['summary']['p95_ms'] is not None
    
    # Many samples: should use quantiles
    data = benchmark(QUERIES, iterations=10, mock_dir=tmp_path)
    assert data['summary']['p95_ms'] is not None
    assert data['summary']['total_runs'] == len(QUERIES) * 10


def test_json_output_file(tmp_path):
    """Test that JSON output file is generated correctly."""
    data = benchmark(QUERIES, iterations=1, mock_dir=tmp_path)
    json_file = tmp_path / 'output.json'
    json_file.write_text(json.dumps(data, indent=2), encoding='utf-8')
    
    # Verify JSON is valid and contains expected keys
    loaded = json.loads(json_file.read_text(encoding='utf-8'))
    assert 'runs' in loaded
    assert 'summary' in loaded
    assert 'total_runs' in loaded['summary']
    assert 'avg_latency_ms' in loaded['summary']
    assert 'p50_ms' in loaded['summary']
    assert 'p95_ms' in loaded['summary']
