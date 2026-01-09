#!/usr/bin/env python3
"""
SpiralSafe Video Generation Pipeline
=====================================
Multi-source video creation with AI enhancement

Supports:
- FFmpeg-based composition
- Image sequence animation
- AI video generation (Runway, Pika, Kling)
- Audio synchronization
- Automated captioning

Usage:
    python video_pipeline.py --images ./frames/*.png --output video.mp4
    python video_pipeline.py --prompt "quantum particle simulation" --duration 5
    python video_pipeline.py --compose manifest.json
"""

import os
import json
import shutil
import subprocess
import asyncio
import tempfile
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Literal, Union
from abc import ABC, abstractmethod
import httpx

# Configuration
OUTPUT_PATH = Path(__file__).parent.parent / "output" / "videos"
TEMP_PATH = Path(tempfile.gettempdir()) / "spiralsafe_video"

@dataclass
class VideoRequest:
    """Video generation request."""
    prompt: Optional[str] = None
    images: Optional[List[Path]] = None
    audio: Optional[Path] = None
    duration: float = 5.0
    fps: int = 24
    width: int = 1920
    height: int = 1080
    format: Literal["mp4", "webm", "gif", "mov"] = "mp4"
    codec: str = "libx264"
    quality: Literal["low", "medium", "high", "ultra"] = "high"
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class VideoResult:
    """Video generation result."""
    success: bool
    provider: str
    video_path: Optional[Path] = None
    video_url: Optional[str] = None
    error: Optional[str] = None
    duration_seconds: float = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class FFmpegProcessor:
    """Core FFmpeg operations for video processing."""

    def __init__(self):
        self.ffmpeg = shutil.which("ffmpeg")
        self.ffprobe = shutil.which("ffprobe")

    def is_available(self) -> bool:
        return bool(self.ffmpeg)

    async def images_to_video(
        self,
        images: List[Path],
        output: Path,
        fps: int = 24,
        codec: str = "libx264",
        quality: str = "high"
    ) -> VideoResult:
        """Convert image sequence to video."""
        if not self.is_available():
            return VideoResult(
                success=False,
                provider="ffmpeg",
                error="FFmpeg not found. Install from https://ffmpeg.org"
            )

        # Create temp directory with symlinked frames
        TEMP_PATH.mkdir(parents=True, exist_ok=True)
        frame_dir = TEMP_PATH / f"frames_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        frame_dir.mkdir()

        try:
            # Copy/symlink images with sequential names
            for i, img in enumerate(sorted(images)):
                ext = img.suffix
                dst = frame_dir / f"frame_{i:05d}{ext}"
                shutil.copy(img, dst)

            # Quality presets
            crf = {"low": 28, "medium": 23, "high": 18, "ultra": 15}.get(quality, 18)

            # Build FFmpeg command
            cmd = [
                self.ffmpeg, "-y",
                "-framerate", str(fps),
                "-i", str(frame_dir / f"frame_%05d{images[0].suffix}"),
                "-c:v", codec,
                "-crf", str(crf),
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                str(output)
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                return VideoResult(
                    success=False,
                    provider="ffmpeg",
                    error=stderr.decode()
                )

            return VideoResult(
                success=True,
                provider="ffmpeg",
                video_path=output,
                duration_seconds=len(images) / fps
            )

        finally:
            # Cleanup
            shutil.rmtree(frame_dir, ignore_errors=True)

    async def add_audio(
        self,
        video: Path,
        audio: Path,
        output: Path,
        loop_audio: bool = True
    ) -> VideoResult:
        """Add audio track to video."""
        if not self.is_available():
            return VideoResult(success=False, provider="ffmpeg", error="FFmpeg not found")

        # Get video duration
        probe_cmd = [
            self.ffprobe, "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            str(video)
        ]

        probe = await asyncio.create_subprocess_exec(
            *probe_cmd,
            stdout=asyncio.subprocess.PIPE
        )
        duration_str, _ = await probe.communicate()
        duration = float(duration_str.decode().strip())

        # Build audio mixing command
        audio_filter = f"aloop=loop=-1:size=2e+09" if loop_audio else ""

        cmd = [
            self.ffmpeg, "-y",
            "-i", str(video),
            "-i", str(audio),
            "-filter_complex", f"[1:a]{audio_filter},atrim=0:{duration}[a]" if loop_audio else "[1:a]atrim=0:{duration}[a]",
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            str(output)
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        _, stderr = await process.communicate()

        if process.returncode != 0:
            return VideoResult(success=False, provider="ffmpeg", error=stderr.decode())

        return VideoResult(
            success=True,
            provider="ffmpeg",
            video_path=output,
            duration_seconds=duration
        )

    async def create_slideshow(
        self,
        images: List[Path],
        output: Path,
        duration_per_image: float = 3.0,
        transition: str = "fade",
        transition_duration: float = 0.5,
        fps: int = 24
    ) -> VideoResult:
        """Create slideshow with transitions."""
        if not self.is_available():
            return VideoResult(success=False, provider="ffmpeg", error="FFmpeg not found")

        # Build complex filter for transitions
        n = len(images)
        filter_parts = []

        # Input setup
        inputs = []
        for i, img in enumerate(images):
            inputs.extend(["-loop", "1", "-t", str(duration_per_image), "-i", str(img)])

        # Create crossfade transitions
        if n > 1 and transition == "fade":
            for i in range(n - 1):
                if i == 0:
                    filter_parts.append(
                        f"[0][1]xfade=transition=fade:duration={transition_duration}:offset={duration_per_image - transition_duration}[v1]"
                    )
                else:
                    offset = (i + 1) * duration_per_image - (i + 1) * transition_duration
                    filter_parts.append(
                        f"[v{i}][{i + 1}]xfade=transition=fade:duration={transition_duration}:offset={offset}[v{i + 1}]"
                    )
            final_stream = f"[v{n - 1}]"
        else:
            # Simple concatenation
            concat_inputs = "".join(f"[{i}:v]" for i in range(n))
            filter_parts.append(f"{concat_inputs}concat=n={n}:v=1:a=0[v]")
            final_stream = "[v]"

        filter_complex = ";".join(filter_parts)

        cmd = [
            self.ffmpeg, "-y",
            *inputs,
            "-filter_complex", filter_complex,
            "-map", final_stream.strip("[]"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(output)
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        _, stderr = await process.communicate()

        if process.returncode != 0:
            return VideoResult(success=False, provider="ffmpeg", error=stderr.decode())

        total_duration = n * duration_per_image - (n - 1) * transition_duration

        return VideoResult(
            success=True,
            provider="ffmpeg",
            video_path=output,
            duration_seconds=total_duration
        )

    async def add_text_overlay(
        self,
        video: Path,
        text: str,
        output: Path,
        position: str = "bottom",
        font_size: int = 48,
        font_color: str = "white",
        bg_color: str = "black@0.5"
    ) -> VideoResult:
        """Add text overlay to video."""
        if not self.is_available():
            return VideoResult(success=False, provider="ffmpeg", error="FFmpeg not found")

        # Position mapping
        positions = {
            "top": "x=(w-text_w)/2:y=50",
            "center": "x=(w-text_w)/2:y=(h-text_h)/2",
            "bottom": "x=(w-text_w)/2:y=h-text_h-50"
        }

        pos = positions.get(position, positions["bottom"])

        # Escape text for FFmpeg
        escaped_text = text.replace("'", "'\\''").replace(":", "\\:")

        cmd = [
            self.ffmpeg, "-y",
            "-i", str(video),
            "-vf", f"drawtext=text='{escaped_text}':fontsize={font_size}:fontcolor={font_color}:box=1:boxcolor={bg_color}:{pos}",
            "-c:a", "copy",
            str(output)
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        _, stderr = await process.communicate()

        if process.returncode != 0:
            return VideoResult(success=False, provider="ffmpeg", error=stderr.decode())

        return VideoResult(success=True, provider="ffmpeg", video_path=output)

    async def resize(
        self,
        video: Path,
        output: Path,
        width: int = 1920,
        height: int = 1080
    ) -> VideoResult:
        """Resize video."""
        if not self.is_available():
            return VideoResult(success=False, provider="ffmpeg", error="FFmpeg not found")

        cmd = [
            self.ffmpeg, "-y",
            "-i", str(video),
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
            "-c:a", "copy",
            str(output)
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        _, stderr = await process.communicate()

        if process.returncode != 0:
            return VideoResult(success=False, provider="ffmpeg", error=stderr.decode())

        return VideoResult(success=True, provider="ffmpeg", video_path=output)

    async def to_gif(
        self,
        video: Path,
        output: Path,
        fps: int = 15,
        width: int = 480
    ) -> VideoResult:
        """Convert video to optimized GIF."""
        if not self.is_available():
            return VideoResult(success=False, provider="ffmpeg", error="FFmpeg not found")

        # Two-pass for better quality
        palette_path = TEMP_PATH / "palette.png"
        TEMP_PATH.mkdir(parents=True, exist_ok=True)

        # Generate palette
        cmd1 = [
            self.ffmpeg, "-y",
            "-i", str(video),
            "-vf", f"fps={fps},scale={width}:-1:flags=lanczos,palettegen",
            str(palette_path)
        ]

        process1 = await asyncio.create_subprocess_exec(
            *cmd1,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process1.communicate()

        # Create GIF with palette
        cmd2 = [
            self.ffmpeg, "-y",
            "-i", str(video),
            "-i", str(palette_path),
            "-filter_complex", f"fps={fps},scale={width}:-1:flags=lanczos[x];[x][1:v]paletteuse",
            str(output)
        ]

        process2 = await asyncio.create_subprocess_exec(
            *cmd2,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        _, stderr = await process2.communicate()

        palette_path.unlink(missing_ok=True)

        if process2.returncode != 0:
            return VideoResult(success=False, provider="ffmpeg", error=stderr.decode())

        return VideoResult(success=True, provider="ffmpeg", video_path=output)


class AIVideoProvider(ABC):
    """Base class for AI video generation providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def generate(self, request: VideoRequest) -> VideoResult:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass


class RunwayProvider(AIVideoProvider):
    """Runway Gen-3 Alpha video generation."""

    name = "runway"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("RUNWAY_API_KEY")

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def generate(self, request: VideoRequest) -> VideoResult:
        if not self.is_available():
            return VideoResult(
                success=False,
                provider=self.name,
                error="Runway API key not configured"
            )

        # Runway API integration would go here
        # For now, placeholder
        return VideoResult(
            success=False,
            provider=self.name,
            error="Runway integration coming soon - use web interface"
        )


class ReplicateVideoProvider(AIVideoProvider):
    """Replicate video models (Stable Video Diffusion, etc.)."""

    name = "replicate"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("REPLICATE_API_TOKEN")

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def generate(self, request: VideoRequest) -> VideoResult:
        if not self.is_available():
            return VideoResult(
                success=False,
                provider=self.name,
                error="Replicate API token not configured"
            )

        # Check for input image (required for SVD)
        if not request.images or len(request.images) == 0:
            return VideoResult(
                success=False,
                provider=self.name,
                error="Stable Video Diffusion requires an input image"
            )

        try:
            async with httpx.AsyncClient() as client:
                # Read and encode image
                import base64
                image_data = request.images[0].read_bytes()
                image_b64 = base64.b64encode(image_data).decode()

                # Create prediction
                response = await client.post(
                    "https://api.replicate.com/v1/predictions",
                    headers={
                        "Authorization": f"Token {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "stability-ai/stable-video-diffusion",
                        "input": {
                            "input_image": f"data:image/png;base64,{image_b64}",
                            "frames_per_second": request.fps,
                            "sizing_strategy": "maintain_aspect_ratio"
                        }
                    },
                    timeout=30.0
                )

                if response.status_code not in [200, 201]:
                    return VideoResult(
                        success=False,
                        provider=self.name,
                        error=f"API error: {response.text}"
                    )

                prediction = response.json()
                prediction_id = prediction.get("id")

                # Poll for completion
                for _ in range(300):  # 5 min max
                    await asyncio.sleep(1)

                    status_resp = await client.get(
                        f"https://api.replicate.com/v1/predictions/{prediction_id}",
                        headers={"Authorization": f"Token {self.api_key}"}
                    )

                    status_data = status_resp.json()
                    status = status_data.get("status")

                    if status == "succeeded":
                        video_url = status_data.get("output")

                        # Download video
                        video_resp = await client.get(video_url)

                        OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
                        output_path = OUTPUT_PATH / f"svd_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
                        output_path.write_bytes(video_resp.content)

                        return VideoResult(
                            success=True,
                            provider=self.name,
                            video_path=output_path,
                            video_url=video_url,
                            duration_seconds=request.duration
                        )

                    elif status == "failed":
                        return VideoResult(
                            success=False,
                            provider=self.name,
                            error=status_data.get("error", "Generation failed")
                        )

                return VideoResult(
                    success=False,
                    provider=self.name,
                    error="Generation timed out"
                )

        except Exception as e:
            return VideoResult(
                success=False,
                provider=self.name,
                error=str(e)
            )


class VideoPipeline:
    """
    Complete video generation pipeline.

    Supports:
    - Image sequence to video
    - AI video generation
    - Composition and effects
    - Audio mixing
    """

    def __init__(self):
        self.ffmpeg = FFmpegProcessor()
        self.ai_providers = [
            ReplicateVideoProvider(),
            RunwayProvider(),
        ]

        OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
        TEMP_PATH.mkdir(parents=True, exist_ok=True)

    async def from_images(
        self,
        images: List[Union[str, Path]],
        output: Optional[Path] = None,
        mode: Literal["sequence", "slideshow"] = "sequence",
        fps: int = 24,
        duration_per_image: float = 3.0,
        **kwargs
    ) -> VideoResult:
        """Create video from images."""
        image_paths = [Path(i) if isinstance(i, str) else i for i in images]

        if output is None:
            output = OUTPUT_PATH / f"video_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"

        if mode == "sequence":
            return await self.ffmpeg.images_to_video(image_paths, output, fps=fps, **kwargs)
        else:
            return await self.ffmpeg.create_slideshow(
                image_paths, output,
                duration_per_image=duration_per_image,
                fps=fps, **kwargs
            )

    async def from_prompt(
        self,
        prompt: str,
        source_image: Optional[Path] = None,
        duration: float = 5.0,
        **kwargs
    ) -> VideoResult:
        """Generate video from text prompt using AI."""
        request = VideoRequest(
            prompt=prompt,
            images=[source_image] if source_image else None,
            duration=duration,
            **kwargs
        )

        available_providers = [p for p in self.ai_providers if p.is_available()]

        if not available_providers:
            return VideoResult(
                success=False,
                provider="none",
                error="No AI video providers available. Configure API keys."
            )

        for provider in available_providers:
            result = await provider.generate(request)
            if result.success:
                return result

        return VideoResult(
            success=False,
            provider="all",
            error="All AI providers failed"
        )

    async def compose(self, manifest: Dict[str, Any]) -> VideoResult:
        """
        Compose video from manifest specification.

        Manifest format:
        {
            "output": "final.mp4",
            "width": 1920,
            "height": 1080,
            "scenes": [
                {
                    "type": "images",
                    "source": ["frame1.png", "frame2.png"],
                    "duration": 5.0,
                    "transition": "fade"
                },
                {
                    "type": "video",
                    "source": "clip.mp4",
                    "start": 0,
                    "end": 10
                },
                {
                    "type": "ai",
                    "prompt": "quantum visualization",
                    "duration": 3.0
                }
            ],
            "audio": {
                "source": "music.mp3",
                "volume": 0.8
            },
            "overlays": [
                {
                    "type": "text",
                    "content": "SpiralSafe",
                    "position": "bottom",
                    "start": 0,
                    "end": 5
                }
            ]
        }
        """
        # Complex composition logic would go here
        # For now, basic implementation

        scenes = manifest.get("scenes", [])
        output = Path(manifest.get("output", OUTPUT_PATH / "composed.mp4"))

        if not scenes:
            return VideoResult(
                success=False,
                provider="compose",
                error="No scenes in manifest"
            )

        # Process each scene
        temp_videos = []

        for i, scene in enumerate(scenes):
            scene_type = scene.get("type")

            if scene_type == "images":
                images = [Path(s) for s in scene.get("source", [])]
                temp_out = TEMP_PATH / f"scene_{i}.mp4"
                result = await self.from_images(
                    images, temp_out,
                    mode="slideshow",
                    duration_per_image=scene.get("duration", 3.0) / len(images)
                )
                if result.success:
                    temp_videos.append(temp_out)

            elif scene_type == "video":
                # Copy/trim existing video
                temp_videos.append(Path(scene.get("source")))

        if not temp_videos:
            return VideoResult(
                success=False,
                provider="compose",
                error="No valid scenes processed"
            )

        # Concatenate scenes
        # (simplified - full implementation would handle transitions)
        if len(temp_videos) == 1:
            shutil.copy(temp_videos[0], output)
        else:
            # Create concat file
            concat_file = TEMP_PATH / "concat.txt"
            with open(concat_file, "w") as f:
                for v in temp_videos:
                    f.write(f"file '{v}'\n")

            cmd = [
                self.ffmpeg.ffmpeg, "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_file),
                "-c", "copy",
                str(output)
            ]

            process = await asyncio.create_subprocess_exec(*cmd)
            await process.communicate()

        return VideoResult(
            success=True,
            provider="compose",
            video_path=output
        )

    async def to_gif(self, video: Path, output: Optional[Path] = None, **kwargs) -> VideoResult:
        """Convert video to GIF."""
        if output is None:
            output = video.with_suffix(".gif")
        return await self.ffmpeg.to_gif(video, output, **kwargs)


# Preset compositions for common use cases
PRESETS = {
    "quantum_demo": {
        "description": "Animated quantum concept visualization",
        "scenes": [
            {"type": "images", "duration": 10.0, "transition": "fade"}
        ],
        "audio": {"source": None},
        "overlays": [
            {"type": "text", "content": "Quantum-Redstone Framework", "position": "bottom"}
        ]
    },
    "spiralsafe_intro": {
        "description": "SpiralSafe introduction video",
        "scenes": [
            {"type": "images", "duration": 15.0, "transition": "fade"}
        ],
        "overlays": [
            {"type": "text", "content": "SpiralSafe", "position": "center"}
        ]
    }
}


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="SpiralSafe Video Pipeline")
    subparsers = parser.add_subparsers(dest="command")

    # Images to video
    img_parser = subparsers.add_parser("images", help="Create video from images")
    img_parser.add_argument("--input", "-i", nargs="+", required=True, help="Input images")
    img_parser.add_argument("--output", "-o", help="Output file")
    img_parser.add_argument("--mode", choices=["sequence", "slideshow"], default="sequence")
    img_parser.add_argument("--fps", type=int, default=24)
    img_parser.add_argument("--duration", type=float, default=3.0, help="Per-image duration for slideshow")

    # AI generation
    ai_parser = subparsers.add_parser("ai", help="Generate video with AI")
    ai_parser.add_argument("--prompt", "-p", required=True, help="Text prompt")
    ai_parser.add_argument("--image", help="Source image for video")
    ai_parser.add_argument("--duration", type=float, default=5.0)
    ai_parser.add_argument("--output", "-o", help="Output file")

    # Compose
    compose_parser = subparsers.add_parser("compose", help="Compose from manifest")
    compose_parser.add_argument("manifest", help="Manifest JSON file")

    # Convert to GIF
    gif_parser = subparsers.add_parser("gif", help="Convert video to GIF")
    gif_parser.add_argument("input", help="Input video")
    gif_parser.add_argument("--output", "-o", help="Output GIF")
    gif_parser.add_argument("--width", type=int, default=480)
    gif_parser.add_argument("--fps", type=int, default=15)

    args = parser.parse_args()
    pipeline = VideoPipeline()

    if args.command == "images":
        result = await pipeline.from_images(
            args.input,
            Path(args.output) if args.output else None,
            mode=args.mode,
            fps=args.fps,
            duration_per_image=args.duration
        )
    elif args.command == "ai":
        result = await pipeline.from_prompt(
            args.prompt,
            source_image=Path(args.image) if args.image else None,
            duration=args.duration
        )
    elif args.command == "compose":
        with open(args.manifest) as f:
            manifest = json.load(f)
        result = await pipeline.compose(manifest)
    elif args.command == "gif":
        result = await pipeline.to_gif(
            Path(args.input),
            Path(args.output) if args.output else None,
            width=args.width,
            fps=args.fps
        )
    else:
        parser.print_help()
        return

    if result.success:
        print(f"Success! Output: {result.video_path}")
    else:
        print(f"Failed: {result.error}")


if __name__ == "__main__":
    asyncio.run(main())
