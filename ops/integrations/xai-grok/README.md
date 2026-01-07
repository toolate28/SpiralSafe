xAI/Grok integration tests and mocks

This folder contains deterministic mocks and tests used to validate Grok-style tool calls and H&&S:WAVE effects.

Files:
- mocks/grok_web_search_response.xml - XML function-call style web_search mock
- mocks/grok_function_call_envelope.xml - function call envelope mock
- tests/test_grok_xml_parsing.py - parses mocks, asserts schema
- tests/test_wave_with_grok.py - simple wave.md proxy test that verifies divergence improves when evidence is added
- requirements.txt - Python deps for running tests locally

Run locally:

python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
pytest -q

Design notes:
- Tests are deliberately deterministic and offline to be CI-friendly.
- We use pydantic to demonstrate structured parsing of tool outputs.
- The wave test uses the same simple heuristics as CI coherence checks (curl and divergence proxies) so we can measure material improvements.
