import xml.etree.ElementTree as ET
from pydantic import BaseModel, AnyUrl, Field
from typing import List
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MOCK = ROOT / "mocks" / "grok_web_search_response.xml"


class GrokResult(BaseModel):
    id: str
    title: str
    url: AnyUrl
    snippet: str
    timestamp: str
    relevance: float = Field(..., ge=0.0, le=1.0)


def parse_grok_web_search(xml_path: Path) -> List[GrokResult]:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    results = []
    for result in root.findall('.//result'):
        data = {
            'id': result.get('id') or result.findtext('id') or result.attrib.get('id'),
            'title': result.findtext('title') or '',
            'url': result.findtext('url') or '',
            'snippet': result.findtext('snippet') or '',
            'timestamp': result.findtext('timestamp') or '',
            'relevance': float(result.findtext('relevance') or 0.0),
        }
        results.append(GrokResult(**data))
    return results


def test_parse_grok_web_search_exists():
    assert MOCK.exists(), f"Mock file not found: {MOCK}"


def test_parse_grok_web_search_contents():
    results = parse_grok_web_search(MOCK)
    assert len(results) >= 1
    # Top result should have high relevance
    assert results[0].relevance >= 0.5
    assert results[0].title
    assert results[0].url.scheme in ('http', 'https')
