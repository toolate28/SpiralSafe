# OpenAI GPT Integration

> **H&&S:WAVE** | Hope&&Sauced
> Commercial AI Integration for SpiralSafe

---

## Overview

This integration connects SpiralSafe with OpenAI's GPT ecosystem, enabling access to GPT-4, GPT-4o, and the Assistants API through unified H&&S:WAVE handoff protocols.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         OPENAI GPT INTEGRATION                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │ Chat Completions│  │   Assistants    │  │   Embeddings    │            │
│  │   (GPT-4/4o)    │  │   API + Tools   │  │  (text-embed)   │            │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘            │
│           │                    │                    │                      │
│           └────────────────────┼────────────────────┘                      │
│                                │                                           │
│                    ┌───────────┴───────────┐                              │
│                    │  SpiralSafe Adapter   │                              │
│                    │     (H&&S:WAVE)       │                              │
│                    └───────────────────────┘                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Features

| Feature | Status | Description |
|---------|--------|-------------|
| Chat Completions | ✓ Ready | GPT-4o and GPT-4-turbo via Chat API |
| Assistants API | ✓ Ready | Persistent assistants with tools |
| Function Calling | ✓ Ready | Structured tool use |
| Code Interpreter | ✓ Ready | Python execution in sandboxed env |
| Vision | ✓ Ready | Image analysis with GPT-4V |
| Embeddings | ✓ Ready | Semantic search and similarity |

---

## Configuration

```yaml
# ops/integrations/openai-config.yaml
provider: openai
model: gpt-4o
alternative_models:
  - gpt-4-turbo
  - gpt-4o-mini
  - gpt-3.5-turbo
features:
  function_calling: true
  code_interpreter: true
  vision: true
  streaming: true
handoff_protocol: H&&S:WAVE
compatibility:
  - tool_use_mapping
  - context_window_adaptation
  - rate_limit_awareness
api:
  base_url: "https://api.openai.com/v1"
  auth: "Bearer ${OPENAI_API_KEY}"
```

---

## API Response Format

OpenAI responses are normalized to SpiralSafe format:

```json
{
  "spiralsafe": {
    "version": "1.0",
    "provider": "openai-gpt",
    "response": {
      "id": "chatcmpl-abc123",
      "object": "chat.completion",
      "model": "gpt-4o-2024-08-06",
      "usage": {
        "prompt_tokens": 180,
        "completion_tokens": 225,
        "total_tokens": 405
      },
      "choices": [{
        "message": {
          "role": "assistant",
          "content": "Analysis complete with wave coherence metrics..."
        },
        "finish_reason": "stop"
      }]
    },
    "handoff": {
      "signature": "H&&S:WAVE",
      "from": "openai-gpt",
      "context_preserved": true
    }
  }
}
```

---

## Files

```
openai-gpt/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── mocks/
│   ├── chat_completion_response.json  # Mock Chat API response
│   └── function_call_response.json    # Mock function calling response
└── tests/
    ├── test_openai_parsing.py         # Parse and validate OpenAI responses
    └── test_wave_with_gpt.py          # Wave coherence with GPT data
```

---

## Running Tests

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -q
```

---

## Design Notes

1. **Commercial Grade**: OpenAI offers the widest ecosystem and best developer experience for production deployments.

2. **Deterministic Mocks**: Tests use predefined mock responses for CI/CD reliability - no live API calls during testing.

3. **H&&S:WAVE Protocol**: All handoffs include signature markers for multi-agent coordination.

4. **Rate Limiting**: Configuration supports rate limit awareness and automatic retries.

5. **Cost Optimization**: Support for model tiering (GPT-4o vs GPT-4o-mini) based on task complexity.

---

## Integration Examples

### Chat Completion

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a SpiralSafe wave analyst."},
        {"role": "user", "content": "Analyze the coherence of this document."}
    ]
)
```

### Function Calling for Wave Analysis

```python
tools = [{
    "type": "function",
    "function": {
        "name": "analyze_wave_coherence",
        "description": "Analyze document coherence using wave.md metrics",
        "parameters": {
            "type": "object",
            "properties": {
                "document": {"type": "string", "description": "Document text"},
                "threshold": {"type": "number", "description": "Coherence threshold"}
            },
            "required": ["document"]
        }
    }
}]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)
```

---

## Strengths & Considerations

### Strengths
- **Widest Ecosystem**: Best developer experience, most integrations
- **Consistent Updates**: Regular model improvements
- **Enterprise Support**: SOC 2 compliance, data privacy options

### Considerations
- **Closed Source**: No access to model weights
- **Vendor Lock-in**: API-dependent infrastructure
- **Cost**: Higher per-token costs than open-source alternatives

---

**H&&S:WAVE** | Hope&&Sauced
*Commercial AI Integration Through Protocol*
