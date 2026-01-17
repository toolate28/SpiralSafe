# Meta LLaMA Integration

> **H&&S:WAVE** | Hope&&Sauced
> Open-Source AI Integration for SpiralSafe

---

## Overview

This integration connects SpiralSafe with Meta's LLaMA ecosystem, enabling fully open-source AI capabilities through Ollama, vLLM, and Hugging Face deployments with H&&S:WAVE handoff protocols.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       META LLAMA INTEGRATION                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │     Ollama      │  │      vLLM       │  │  Hugging Face   │            │
│  │ (Local Runtime) │  │(High-Perf Serve)│  │   (Hub/Cloud)   │            │
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

| Feature             | Status  | Description                              |
| ------------------- | ------- | ---------------------------------------- |
| Ollama Integration  | ✓ Ready | Local LLaMA inference via Ollama API     |
| vLLM Backend        | ✓ Ready | High-performance serving for production  |
| Hugging Face Hub    | ✓ Ready | Access to model weights and inference    |
| Fine-tuning Support | ✓ Ready | LoRA and full fine-tuning capabilities   |
| Quantization        | ✓ Ready | 4-bit, 8-bit quantization for efficiency |
| Local Deployment    | ✓ Ready | Run completely offline                   |

---

## Configuration

```yaml
# ops/integrations/meta-llama-config.yaml
provider: meta
models:
  - llama-3.1-70b
  - llama-3.1-8b
  - llama-3.2-3b
  - llama-3.2-1b
features:
  open_weights: true
  local_deployment: true
  fine_tuning: true
  quantization:
    - q4_0
    - q8_0
handoff_protocol: H&&S:WAVE
compatibility:
  - ollama_integration
  - vllm_backend
  - huggingface_hub
deployment:
  local:
    runtime: ollama
    gpu_required: optional
    api_endpoint: "http://localhost:11434"
  cloud:
    providers: [aws, gcp, azure, runpod]
```

---

## API Response Format

LLaMA responses via Ollama are normalized to SpiralSafe format:

```json
{
  "spiralsafe": {
    "version": "1.0",
    "provider": "meta-llama",
    "response": {
      "model": "llama3.1:8b",
      "created_at": "2026-01-12T08:00:00Z",
      "response": "Analysis complete with wave coherence metrics...",
      "done": true,
      "context": [1, 2, 3],
      "total_duration": 1250000000,
      "eval_count": 145,
      "eval_duration": 800000000
    },
    "handoff": {
      "signature": "H&&S:WAVE",
      "from": "meta-llama",
      "context_preserved": true
    }
  }
}
```

---

## Files

```
meta-llama/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── mocks/
│   ├── ollama_generate_response.json  # Mock Ollama generate response
│   └── ollama_chat_response.json      # Mock Ollama chat response
└── tests/
    ├── test_ollama_parsing.py         # Parse and validate Ollama responses
    └── test_wave_with_llama.py        # Wave coherence with LLaMA data
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

## Deployment Options

### 1. Ollama (Recommended for Development)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull model
ollama pull llama3.1:8b

# Start server (default port 11434)
ollama serve

# Test
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Analyze wave coherence metrics",
  "stream": false
}'
```

### 2. vLLM (Recommended for Production)

```bash
# Install vLLM
pip install vllm

# Start server
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --port 8000

# Test with OpenAI-compatible API
curl http://localhost:8000/v1/completions -d '{
  "model": "meta-llama/Llama-3.1-8B-Instruct",
  "prompt": "Analyze wave coherence metrics"
}'
```

### 3. Hugging Face Transformers

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_id = "meta-llama/Llama-3.1-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)
```

---

## Design Notes

1. **Fully Open Source**: LLaMA models can run entirely locally with no external dependencies.

2. **Deterministic Mocks**: Tests use predefined mock responses for CI/CD reliability.

3. **H&&S:WAVE Protocol**: All handoffs include signature markers for multi-agent coordination.

4. **Hardware Flexibility**: Supports CPU-only, GPU, and Apple Silicon deployments.

5. **Model Selection**: Choose model size based on hardware capabilities:
   - 1B/3B: Mobile devices, edge deployment
   - 8B: Consumer GPUs, laptops
   - 70B: Server-grade hardware, cloud

---

**H&&S:WAVE** | Hope&&Sauced
_Open-Source AI Integration Through Protocol_
