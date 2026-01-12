#!/usr/bin/env python3
"""
SpiralSafe Image Generation Pipeline
=====================================
Multi-provider image generation with automatic fallback

Supports:
- OpenAI DALL-E 3
- Replicate (Stable Diffusion, Flux)
- Local models (ComfyUI API)
- Cloudflare Workers AI

Usage:
    python image_pipeline.py --prompt "quantum constraint manifold visualization"
    python image_pipeline.py --template nmsi_diagram --params "alpha=0.5,omega=0.5"
"""

import os
import json
import base64
import hashlib
import argparse
import asyncio
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Literal
from abc import ABC, abstractmethod
import httpx

# Configuration
CONFIG_PATH = Path(__file__).parent.parent / "config" / "image_config.json"
OUTPUT_PATH = Path(__file__).parent.parent / "output" / "images"
TEMPLATES_PATH = Path(__file__).parent.parent / "templates" / "prompts"

@dataclass
class ImageRequest:
    """Standardized image generation request."""
    prompt: str
    negative_prompt: str = ""
    width: int = 1024
    height: int = 1024
    style: Literal["vivid", "natural", "artistic", "technical"] = "natural"
    format: Literal["png", "jpg", "webp"] = "png"
    seed: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ImageResult:
    """Result from image generation."""
    success: bool
    provider: str
    image_path: Optional[Path] = None
    image_url: Optional[str] = None
    image_data: Optional[bytes] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    generation_time_ms: float = 0


class ImageProvider(ABC):
    """Abstract base class for image providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def generate(self, request: ImageRequest) -> ImageResult:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass


class OpenAIProvider(ImageProvider):
    """OpenAI DALL-E 3 provider."""

    name = "openai"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def generate(self, request: ImageRequest) -> ImageResult:
        start = datetime.now()

        if not self.is_available():
            return ImageResult(
                success=False,
                provider=self.name,
                error="OpenAI API key not configured"
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/images/generations",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "dall-e-3",
                        "prompt": request.prompt,
                        "n": 1,
                        "size": f"{request.width}x{request.height}",
                        "quality": "hd" if request.style == "technical" else "standard",
                        "style": "vivid" if request.style in ["vivid", "artistic"] else "natural",
                        "response_format": "b64_json"
                    },
                    timeout=120.0
                )

                if response.status_code != 200:
                    return ImageResult(
                        success=False,
                        provider=self.name,
                        error=f"API error: {response.status_code} - {response.text}"
                    )

                data = response.json()
                image_data = base64.b64decode(data["data"][0]["b64_json"])
                revised_prompt = data["data"][0].get("revised_prompt", request.prompt)

                elapsed = (datetime.now() - start).total_seconds() * 1000

                return ImageResult(
                    success=True,
                    provider=self.name,
                    image_data=image_data,
                    metadata={
                        "revised_prompt": revised_prompt,
                        "model": "dall-e-3"
                    },
                    generation_time_ms=elapsed
                )

        except Exception as e:
            return ImageResult(
                success=False,
                provider=self.name,
                error=str(e)
            )


class ReplicateProvider(ImageProvider):
    """Replicate provider for Stable Diffusion, Flux, etc."""

    name = "replicate"

    MODELS = {
        "sdxl": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        "flux-pro": "black-forest-labs/flux-pro",
        "flux-schnell": "black-forest-labs/flux-schnell",
        "flux-dev": "black-forest-labs/flux-dev",
    }

    def __init__(self, api_key: Optional[str] = None, model: str = "flux-schnell"):
        self.api_key = api_key or os.getenv("REPLICATE_API_TOKEN")
        self.model = self.MODELS.get(model, model)
        self.base_url = "https://api.replicate.com/v1"

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def generate(self, request: ImageRequest) -> ImageResult:
        start = datetime.now()

        if not self.is_available():
            return ImageResult(
                success=False,
                provider=self.name,
                error="Replicate API token not configured"
            )

        try:
            async with httpx.AsyncClient() as client:
                # Create prediction
                create_response = await client.post(
                    f"{self.base_url}/predictions",
                    headers={
                        "Authorization": f"Token {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "version": self.model.split(":")[-1] if ":" in self.model else None,
                        "model": self.model.split(":")[0] if ":" in self.model else self.model,
                        "input": {
                            "prompt": request.prompt,
                            "negative_prompt": request.negative_prompt,
                            "width": request.width,
                            "height": request.height,
                            "seed": request.seed,
                            "num_outputs": 1,
                            "output_format": request.format
                        }
                    },
                    timeout=30.0
                )

                if create_response.status_code not in [200, 201]:
                    return ImageResult(
                        success=False,
                        provider=self.name,
                        error=f"Create prediction failed: {create_response.text}"
                    )

                prediction = create_response.json()
                prediction_url = prediction.get("urls", {}).get("get", prediction.get("id"))

                # Poll for completion
                for _ in range(120):  # Max 2 minutes
                    await asyncio.sleep(1)

                    status_response = await client.get(
                        prediction_url if prediction_url.startswith("http") else f"{self.base_url}/predictions/{prediction_url}",
                        headers={"Authorization": f"Token {self.api_key}"}
                    )

                    status_data = status_response.json()
                    status = status_data.get("status")

                    if status == "succeeded":
                        output = status_data.get("output")
                        image_url = output[0] if isinstance(output, list) else output

                        # Download image
                        img_response = await client.get(image_url)
                        image_data = img_response.content

                        elapsed = (datetime.now() - start).total_seconds() * 1000

                        return ImageResult(
                            success=True,
                            provider=self.name,
                            image_url=image_url,
                            image_data=image_data,
                            metadata={"model": self.model},
                            generation_time_ms=elapsed
                        )

                    elif status == "failed":
                        return ImageResult(
                            success=False,
                            provider=self.name,
                            error=status_data.get("error", "Generation failed")
                        )

                return ImageResult(
                    success=False,
                    provider=self.name,
                    error="Generation timed out"
                )

        except Exception as e:
            return ImageResult(
                success=False,
                provider=self.name,
                error=str(e)
            )


class CloudflareAIProvider(ImageProvider):
    """Cloudflare Workers AI provider."""

    name = "cloudflare"

    def __init__(
        self,
        account_id: Optional[str] = None,
        api_token: Optional[str] = None,
        model: str = "@cf/stabilityai/stable-diffusion-xl-base-1.0"
    ):
        self.account_id = account_id or os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.api_token = api_token or os.getenv("CLOUDFLARE_API_TOKEN")
        self.model = model

    def is_available(self) -> bool:
        return bool(self.account_id and self.api_token)

    async def generate(self, request: ImageRequest) -> ImageResult:
        start = datetime.now()

        if not self.is_available():
            return ImageResult(
                success=False,
                provider=self.name,
                error="Cloudflare credentials not configured"
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model}",
                    headers={
                        "Authorization": f"Bearer {self.api_token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "prompt": request.prompt,
                        "negative_prompt": request.negative_prompt,
                        "width": min(request.width, 1024),
                        "height": min(request.height, 1024),
                    },
                    timeout=120.0
                )

                if response.status_code != 200:
                    return ImageResult(
                        success=False,
                        provider=self.name,
                        error=f"API error: {response.status_code}"
                    )

                image_data = response.content
                elapsed = (datetime.now() - start).total_seconds() * 1000

                return ImageResult(
                    success=True,
                    provider=self.name,
                    image_data=image_data,
                    metadata={"model": self.model},
                    generation_time_ms=elapsed
                )

        except Exception as e:
            return ImageResult(
                success=False,
                provider=self.name,
                error=str(e)
            )


class ComfyUIProvider(ImageProvider):
    """Local ComfyUI API provider."""

    name = "comfyui"

    def __init__(self, base_url: str = "http://127.0.0.1:8188"):
        self.base_url = base_url

    def is_available(self) -> bool:
        try:
            import httpx
            response = httpx.get(f"{self.base_url}/system_stats", timeout=2.0)
            return response.status_code == 200
        except:
            return False

    async def generate(self, request: ImageRequest) -> ImageResult:
        # ComfyUI workflow integration would go here
        # This is a placeholder for local generation
        return ImageResult(
            success=False,
            provider=self.name,
            error="ComfyUI integration not yet implemented - use workflow JSON"
        )


class ImagePipeline:
    """
    Multi-provider image generation pipeline with fallback.

    Usage:
        pipeline = ImagePipeline()
        result = await pipeline.generate("A quantum constraint manifold")
    """

    def __init__(self, providers: Optional[List[ImageProvider]] = None):
        self.providers = providers or [
            OpenAIProvider(),
            ReplicateProvider(),
            CloudflareAIProvider(),
            ComfyUIProvider(),
        ]

        # Filter to available providers
        self.available = [p for p in self.providers if p.is_available()]

        OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    def list_providers(self) -> Dict[str, bool]:
        """List all providers and their availability."""
        return {p.name: p.is_available() for p in self.providers}

    async def generate(
        self,
        prompt: str,
        fallback: bool = True,
        preferred_provider: Optional[str] = None,
        **kwargs
    ) -> ImageResult:
        """
        Generate an image with automatic provider fallback.

        Args:
            prompt: Text description of desired image
            fallback: If True, try next provider on failure
            preferred_provider: Name of provider to try first
            **kwargs: Additional ImageRequest parameters
        """
        request = ImageRequest(prompt=prompt, **kwargs)

        # Reorder providers if preferred specified
        providers = self.available.copy()
        if preferred_provider:
            providers = sorted(
                providers,
                key=lambda p: 0 if p.name == preferred_provider else 1
            )

        if not providers:
            return ImageResult(
                success=False,
                provider="none",
                error="No image providers available. Configure API keys."
            )

        errors = []
        for provider in providers:
            print(f"Trying {provider.name}...")
            result = await provider.generate(request)

            if result.success:
                # Save image
                if result.image_data:
                    filename = self._generate_filename(prompt, request.format)
                    filepath = OUTPUT_PATH / filename
                    filepath.write_bytes(result.image_data)
                    result.image_path = filepath
                    print(f"Saved: {filepath}")
                return result

            errors.append(f"{provider.name}: {result.error}")

            if not fallback:
                break

        return ImageResult(
            success=False,
            provider="all",
            error=f"All providers failed: {'; '.join(errors)}"
        )

    def _generate_filename(self, prompt: str, format: str) -> str:
        """Generate unique filename from prompt hash."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
        return f"img_{timestamp}_{prompt_hash}.{format}"

    async def generate_batch(
        self,
        prompts: List[str],
        concurrent: int = 3,
        **kwargs
    ) -> List[ImageResult]:
        """Generate multiple images concurrently."""
        semaphore = asyncio.Semaphore(concurrent)

        async def bounded_generate(prompt: str) -> ImageResult:
            async with semaphore:
                return await self.generate(prompt, **kwargs)

        tasks = [bounded_generate(p) for p in prompts]
        return await asyncio.gather(*tasks)


# Template system for common visualizations
TEMPLATES = {
    "nmsi_constraint": """
Scientific visualization of quantum constraint manifold.
Mathematical surface where |alpha|^2 + |beta|^2 = 1.
Elegant topology with smooth gradients from blue to purple.
Abstract, clean, technical illustration style.
White background, high contrast, publication quality.
""",

    "quantum_redstone": """
Minecraft-style isometric view of redstone quantum circuit.
Two parallel rails representing ALPHA and OMEGA signals.
Constraint ALPHA + OMEGA = 15 visualized as balanced flow.
Warm redstone glow, blocky aesthetic, technical diagram overlay.
""",

    "spiral_pattern": """
Golden spiral pattern emerging from central point.
Represents recursive self-improvement and learning.
Fibonacci sequence visible in structure.
Gradient from warm gold to cool teal.
Abstract, minimalist, logo-worthy composition.
""",

    "hope_sauce": """
Abstract representation of human-AI collaboration.
Two intertwined light streams - one organic, one digital.
Emergence of new pattern from their intersection.
Warm hopeful colors with technological accents.
""",

    "bloch_sphere": """
3D Bloch sphere quantum state representation.
Transparent sphere with visible internal axes.
Single qubit state vector from origin to surface.
Clean mathematical visualization, dark background.
Subtle grid lines, glowing state indicator.
""",

    "information_substrate": """
Abstract visualization of information as fundamental reality.
Grid of luminous points forming wave-like patterns.
Particles emerging from informational field.
Deep space aesthetic with quantum foam texture.
Scientific visualization, publication quality.
"""
}


def get_template(name: str, **params) -> str:
    """Get and optionally customize a prompt template."""
    template = TEMPLATES.get(name)
    if not template:
        raise ValueError(f"Unknown template: {name}. Available: {list(TEMPLATES.keys())}")

    # Simple parameter substitution
    for key, value in params.items():
        template = template.replace(f"{{{key}}}", str(value))

    return template.strip()


async def main():
    parser = argparse.ArgumentParser(description="SpiralSafe Image Generation Pipeline")
    parser.add_argument("--prompt", "-p", type=str, help="Text prompt for image generation")
    parser.add_argument("--template", "-t", type=str, help="Use named template")
    parser.add_argument("--params", type=str, help="Template parameters (key=value,key=value)")
    parser.add_argument("--provider", type=str, help="Preferred provider")
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--style", type=str, default="natural",
                       choices=["vivid", "natural", "artistic", "technical"])
    parser.add_argument("--list-providers", action="store_true", help="List available providers")
    parser.add_argument("--list-templates", action="store_true", help="List available templates")

    args = parser.parse_args()

    pipeline = ImagePipeline()

    if args.list_providers:
        print("\nImage Providers:")
        for name, available in pipeline.list_providers().items():
            status = "available" if available else "not configured"
            print(f"  {name}: {status}")
        return

    if args.list_templates:
        print("\nPrompt Templates:")
        for name in TEMPLATES.keys():
            print(f"  {name}")
        return

    # Determine prompt
    if args.template:
        params = {}
        if args.params:
            for pair in args.params.split(","):
                key, value = pair.split("=")
                params[key.strip()] = value.strip()
        prompt = get_template(args.template, **params)
    elif args.prompt:
        prompt = args.prompt
    else:
        print("Error: Provide --prompt or --template")
        return

    print(f"\nGenerating image...")
    print(f"Prompt: {prompt[:100]}...")

    result = await pipeline.generate(
        prompt=prompt,
        preferred_provider=args.provider,
        width=args.width,
        height=args.height,
        style=args.style
    )

    if result.success:
        print(f"\nSuccess!")
        print(f"  Provider: {result.provider}")
        print(f"  Path: {result.image_path}")
        print(f"  Time: {result.generation_time_ms:.0f}ms")
    else:
        print(f"\nFailed: {result.error}")


if __name__ == "__main__":
    asyncio.run(main())
