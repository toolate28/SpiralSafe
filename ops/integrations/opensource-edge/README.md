# Open Source & Edge AI Integration

> **H&&S:WAVE** | Hope&&Sauced
> Cutting-Edge Open Source Models for Mobile and Edge Deployment

---

## Overview

This integration connects SpiralSafe with open-source AI models optimized for edge deployment, including Ollama-hosted models, Qwen, and mobile-optimized architectures through H&&S:WAVE handoff protocols.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OPEN SOURCE & EDGE INTEGRATION                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │     Ollama      │  │   Qwen Series   │  │  Mobile Models  │            │
│  │ (Local Runtime) │  │ (Alibaba Cloud) │  │  (Phi, Gemma)   │            │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘            │
│           │                    │                    │                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │   Mistral       │  │   DeepSeek      │  │   Yi Series     │            │
│  │   (EU-hosted)   │  │    (Code+)      │  │  (Multilingual) │            │
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

## Supported Models

### Tier 1: Production Ready

| Model       | Parameters | Use Case      | Platform     |
| ----------- | ---------- | ------------- | ------------ |
| Qwen2.5     | 0.5B-72B   | General, Code | Ollama, vLLM |
| Mistral     | 7B-22B     | EU-compliant  | Ollama, API  |
| DeepSeek-V3 | 37B-671B   | Code, Math    | Ollama, API  |
| Gemma 2     | 2B-27B     | Mobile, Edge  | Ollama, MLX  |
| Phi-3/4     | 3.8B-14B   | Phone, Edge   | Ollama, ONNX |

### Tier 2: Cutting Edge

| Model         | Parameters | Specialty      | Notes             |
| ------------- | ---------- | -------------- | ----------------- |
| Yi-Lightning  | 6B-34B     | Multilingual   | Chinese + English |
| Command R+    | 35B-104B   | RAG, Search    | Cohere-backed     |
| Mixtral-8x22B | 141B       | MoE Efficiency | 8 experts         |
| SmolLM2       | 135M-1.7B  | Ultra-light    | Phone-first       |

---

## Features

| Feature           | Status  | Description                         |
| ----------------- | ------- | ----------------------------------- |
| Ollama Runtime    | ✓ Ready | Local model serving via unified API |
| Qwen Integration  | ✓ Ready | Alibaba's leading OSS model         |
| Mobile Deployment | ✓ Ready | iOS/Android via ONNX/MLX            |
| Quantization      | ✓ Ready | 4-bit, 8-bit for efficiency         |
| Offline Mode      | ✓ Ready | No internet required                |
| Multi-model       | ✓ Ready | Run multiple models simultaneously  |

---

## Configuration

```yaml
# ops/integrations/opensource-edge-config.yaml
provider: opensource-edge
runtimes:
  ollama:
    endpoint: "http://localhost:11434"
    default_model: "qwen2.5:7b"
  vllm:
    endpoint: "http://localhost:8000"
    default_model: "Qwen/Qwen2.5-7B-Instruct"
  mlx:
    enabled: true
    platform: macos
models:
  - name: qwen2.5:7b
    use_cases: [general, code, analysis]
    quantization: q4_K_M
  - name: phi3:mini
    use_cases: [mobile, edge, quick]
    quantization: q4_0
  - name: mistral:7b
    use_cases: [eu_compliance, general]
    quantization: q5_K_M
  - name: deepseek-coder-v2:16b
    use_cases: [code, debugging]
    quantization: q4_K_M
features:
  offline_mode: true
  multi_model: true
  hot_swap: true
handoff_protocol: H&&S:WAVE
compatibility:
  - ollama_api
  - openai_compatible
  - mlx_backend
  - onnx_runtime
```

---

## API Response Format

Open source models normalize to SpiralSafe format:

```json
{
  "spiralsafe": {
    "version": "1.0",
    "provider": "opensource-edge",
    "runtime": "ollama",
    "response": {
      "model": "qwen2.5:7b",
      "created_at": "2026-01-12T08:45:00Z",
      "response": "Wave coherence analysis complete...",
      "done": true,
      "context": [1, 2, 3],
      "total_duration": 980000000,
      "eval_count": 156
    },
    "handoff": {
      "signature": "H&&S:WAVE",
      "from": "opensource-edge",
      "context_preserved": true,
      "offline_capable": true
    }
  }
}
```

---

## Files

```
opensource-edge/
├── README.md                            # This file
├── requirements.txt                     # Python dependencies
├── mocks/
│   ├── qwen_response.json              # Mock Qwen model response
│   └── phi_mobile_response.json        # Mock Phi mobile response
└── tests/
    ├── test_opensource_parsing.py      # Parse and validate responses
    └── test_wave_with_edge.py          # Wave coherence with edge models
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

## Deployment Scenarios

### 1. Desktop/Server (Ollama)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull qwen2.5:7b
ollama pull phi3:mini

# Start with multiple models
OLLAMA_MODELS_LIMIT=3 ollama serve
```

### 2. Mobile (iOS/Android)

```python
# Using ONNX Runtime for mobile
import onnxruntime as ort

# Load quantized model
session = ort.InferenceSession("phi3-mini-q4.onnx")

# Run inference
outputs = session.run(None, {"input_ids": tokens})
```

### 3. Apple Silicon (MLX)

```python
# Using MLX for M1/M2/M3
from mlx_lm import load, generate

model, tokenizer = load("mlx-community/Qwen2.5-7B-Instruct-4bit")
response = generate(model, tokenizer, prompt, max_tokens=500)
```

---

## Model Selection Guide

### By Hardware

| Device         | RAM     | Recommended Models          |
| -------------- | ------- | --------------------------- |
| iPhone/Android | 4-6GB   | Phi-3-mini, SmolLM2         |
| MacBook M1/M2  | 8-16GB  | Qwen2.5:7b, Mistral:7b      |
| Desktop GPU    | 16-24GB | Qwen2.5:14b, DeepSeek-coder |
| Server         | 48GB+   | Qwen2.5:72b, Mixtral-8x22B  |

### By Use Case

| Task           | Best Models                |
| -------------- | -------------------------- |
| Wave Analysis  | Qwen2.5, Mistral           |
| Code Review    | DeepSeek-coder, Qwen-coder |
| Documentation  | Phi-3, Gemma-2             |
| Quick Response | SmolLM2, Phi-mini          |

---

## Design Notes

1. **Fully Offline**: All models can run without internet connectivity after download.

2. **Deterministic Mocks**: Tests use predefined mock responses for CI/CD reliability.

3. **H&&S:WAVE Protocol**: All handoffs include signature markers for multi-agent coordination.

4. **Model Agnostic**: Same adapter works across all supported models.

5. **Edge First**: Optimized for resource-constrained environments.

---

## Cutting-Edge Updates (2026)

Recent models to watch:

- **Qwen2.5**: State-of-the-art at every size tier
- **DeepSeek-V3**: Best open-source reasoning
- **Phi-4**: Microsoft's latest small model
- **Mistral Large 2**: EU-hosted, 123B
- **SmolLM2**: Hugging Face's ultra-efficient series

---

**H&&S:WAVE** | Hope&&Sauced
_Open Source AI Integration Through Protocol_
