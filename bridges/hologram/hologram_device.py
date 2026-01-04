"""
Hologram Device SDK
Interface for 3D Hologram Fan Projector (224 LED, 1250 RPM)

Provides async interface for rendering 3D visualizations,
ATOM trail displays, and token stream animations.
"""

import asyncio
import json
import struct
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import math


@dataclass
class HologramFrame:
    """Represents a single frame for hologram display"""
    width: int = 400
    height: int = 400
    pixels: List[List[Tuple[int, int, int]]] = None  # RGB values
    brightness: float = 1.0  # 0.0 to 1.0
    rotation_speed: int = 1250  # RPM

    def __post_init__(self):
        if self.pixels is None:
            # Initialize black frame
            self.pixels = [
                [(0, 0, 0) for _ in range(self.width)]
                for _ in range(self.height)
            ]

    def set_pixel(self, x: int, y: int, color: Tuple[int, int, int]):
        """Set a single pixel color"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = color

    def draw_text(self, text: str, x: int, y: int, color: Tuple[int, int, int], size: int = 16):
        """Draw text on frame (simplified - in production would use PIL)"""
        # Simplified text rendering - just mark the region
        for i, char in enumerate(text[:20]):  # Limit to 20 chars
            char_x = x + (i * size)
            if char_x < self.width:
                for dy in range(size):
                    if y + dy < self.height:
                        self.set_pixel(char_x, y + dy, color)

    def draw_circle(self, cx: int, cy: int, radius: int, color: Tuple[int, int, int]):
        """Draw a circle"""
        for angle in range(0, 360, 5):
            rad = math.radians(angle)
            x = int(cx + radius * math.cos(rad))
            y = int(cy + radius * math.sin(rad))
            self.set_pixel(x, y, color)

    def draw_spiral(self, cx: int, cy: int, turns: int, color: Tuple[int, int, int], thickness: int = 2):
        """Draw a spiral pattern (perfect for ATOM trail visualization)"""
        max_radius = min(cx, cy, self.width - cx, self.height - cy) - 10
        points = 360 * turns

        for i in range(points):
            angle = (i / points) * turns * 2 * math.pi
            radius = (i / points) * max_radius
            x = int(cx + radius * math.cos(angle))
            y = int(cy + radius * math.sin(angle))

            # Draw with thickness
            for dx in range(-thickness, thickness + 1):
                for dy in range(-thickness, thickness + 1):
                    self.set_pixel(x + dx, y + dy, color)

    def clear(self, color: Tuple[int, int, int] = (0, 0, 0)):
        """Clear frame to specified color"""
        self.pixels = [[color for _ in range(self.width)] for _ in range(self.height)]


class HologramDevice:
    """Interface to 3D Hologram Fan hardware"""

    def __init__(self, device_path: str = "/dev/hologram0", fps: int = 20):
        """
        Initialize hologram device

        Args:
            device_path: Path to hologram device (or 'virtual' for simulation)
            fps: Target frames per second (default: 20)
        """
        self.device_path = device_path
        self.fps = fps
        self.is_virtual = device_path == 'virtual' or device_path.startswith('virtual')
        self.connected = False
        self.current_mode = 'idle'

        # Color scheme (Hope && Sauce)
        self.COLOR_HOPE = (0, 102, 255)      # #0066FF
        self.COLOR_SAUCE = (255, 102, 0)     # #FF6600
        self.COLOR_SUCCESS = (0, 255, 170)   # #00FFAA
        self.COLOR_WARNING = (255, 170, 0)   # #FFAA00
        self.COLOR_ERROR = (255, 0, 102)     # #FF0066
        self.COLOR_WHITE = (255, 255, 255)

    async def connect(self):
        """Connect to hologram device"""
        if self.is_virtual:
            print(f"🌀 Connected to VIRTUAL hologram device")
            self.connected = True
            return

        try:
            # In production, would open serial/USB connection here
            # For now, simulate connection
            await asyncio.sleep(0.1)
            self.connected = True
            print(f"✨ Connected to hologram device: {self.device_path}")
        except Exception as e:
            print(f"❌ Failed to connect to hologram: {e}")
            raise

    async def disconnect(self):
        """Disconnect from hologram device"""
        self.connected = False
        print("👋 Disconnected from hologram device")

    async def display(self, frame: HologramFrame, duration: Optional[float] = None):
        """
        Display a frame on the hologram

        Args:
            frame: HologramFrame to display
            duration: Optional duration in seconds (None = single frame)
        """
        if not self.connected:
            raise RuntimeError("Hologram device not connected")

        if self.is_virtual:
            # Virtual display - just log it
            print(f"  🖼️  Displaying frame ({frame.width}x{frame.height}, {frame.brightness*100:.0f}% brightness)")
        else:
            # In production, would send frame data to device
            await asyncio.sleep(1 / self.fps)

        if duration:
            await asyncio.sleep(duration)

    async def display_text(self, text: str, color: Optional[Tuple[int, int, int]] = None, duration: float = 2.0):
        """Display text message on hologram"""
        if color is None:
            color = self.COLOR_HOPE

        frame = HologramFrame()
        frame.draw_text(text, 50, 200, color, size=20)
        await self.display(frame, duration=duration)

    async def display_atom_entry(self, entry: Any, duration: float = 1.5):
        """
        Display a single ATOM entry with appropriate visualization

        Args:
            entry: ATOMEntry object
            duration: How long to display (seconds)
        """
        frame = HologramFrame()

        # Get color based on entry type
        color_map = {
            'CONFIG': self.COLOR_HOPE,
            'STATUS': self.COLOR_SUCCESS,
            'NETWORK': self.COLOR_SAUCE,
            'ERROR': self.COLOR_ERROR,
            'WARNING': self.COLOR_WARNING,
        }
        color = color_map.get(entry.entry_type, self.COLOR_WHITE)

        # Draw entry type at top
        frame.draw_text(f"[{entry.entry_type}]", 100, 50, color, size=18)

        # Draw message in center
        frame.draw_text(entry.message[:30], 50, 200, color, size=14)

        # Draw timestamp at bottom
        timestamp_str = entry.timestamp.strftime("%H:%M:%S")
        frame.draw_text(timestamp_str, 150, 350, self.COLOR_WHITE, size=12)

        await self.display(frame, duration=duration)

    async def display_atom_spiral(self, entries: List[Any], duration: float = 5.0):
        """
        Display ATOM entries as a 3D spiral visualization

        Args:
            entries: List of ATOMEntry objects
            duration: Animation duration (seconds)
        """
        frame = HologramFrame()
        cx, cy = frame.width // 2, frame.height // 2

        # Draw base spiral
        frame.draw_spiral(cx, cy, turns=3, color=self.COLOR_HOPE, thickness=1)

        # Place entries along the spiral
        if entries:
            points = min(len(entries), 50)  # Limit to 50 most recent
            for i, entry in enumerate(entries[-points:]):
                angle = (i / points) * 3 * 2 * math.pi
                radius = (i / points) * (min(cx, cy) - 20)
                x = int(cx + radius * math.cos(angle))
                y = int(cy + radius * math.sin(angle))

                # Color based on entry type
                color = (0, 102, 255) if entry.entry_type == 'CONFIG' else \
                       (0, 255, 170) if entry.entry_type == 'STATUS' else \
                       (255, 102, 0) if entry.entry_type == 'NETWORK' else \
                       (255, 0, 102)  # ERROR

                # Draw node
                frame.draw_circle(x, y, radius=3, color=color)

        await self.display(frame, duration=duration)

    async def display_token_stream(self, tokens: List[str], delay: float = 0.1):
        """
        Display tokens streaming through LLM

        Args:
            tokens: List of token strings
            delay: Delay between tokens (seconds)
        """
        for i, token in enumerate(tokens):
            frame = HologramFrame()

            # Draw token stream title
            frame.draw_text("TOKEN STREAM", 100, 30, self.COLOR_SAUCE, size=16)

            # Draw current token (large)
            frame.draw_text(f"> {token}", 80, 200, self.COLOR_HOPE, size=24)

            # Draw previous tokens (fading)
            y_offset = 250
            for j in range(max(0, i - 3), i):
                if j < len(tokens):
                    frame.draw_text(tokens[j], 100, y_offset, self.COLOR_WHITE, size=12)
                    y_offset += 20

            # Draw progress bar
            progress = (i + 1) / len(tokens)
            bar_width = int(300 * progress)
            for x in range(50, 50 + bar_width):
                frame.set_pixel(x, 350, self.COLOR_SUCCESS)

            await self.display(frame, duration=delay)

    async def display_system_stats(self, gpu_usage: float, ram_usage: float, duration: float = 2.0):
        """
        Display system resource usage

        Args:
            gpu_usage: GPU usage percentage (0-100)
            ram_usage: RAM usage percentage (0-100)
            duration: Display duration
        """
        frame = HologramFrame()

        # Title
        frame.draw_text("SYSTEM STATS", 100, 50, self.COLOR_HOPE, size=18)

        # GPU bar
        frame.draw_text(f"GPU: {gpu_usage:.0f}%", 80, 150, self.COLOR_SAUCE, size=14)
        gpu_bar_width = int(200 * (gpu_usage / 100))
        for x in range(80, 80 + gpu_bar_width):
            for y in range(180, 195):
                frame.set_pixel(x, y, self.COLOR_SAUCE)

        # RAM bar
        frame.draw_text(f"RAM: {ram_usage:.0f}%", 80, 230, self.COLOR_SUCCESS, size=14)
        ram_bar_width = int(200 * (ram_usage / 100))
        for x in range(80, 80 + ram_bar_width):
            for y in range(260, 275):
                frame.set_pixel(x, y, self.COLOR_SUCCESS)

        await self.display(frame, duration=duration)

    async def animate_thinking(self, duration: float = 3.0):
        """Animate 'AI thinking' visualization"""
        frames = int(duration * self.fps)

        for i in range(frames):
            frame = HologramFrame()
            cx, cy = frame.width // 2, frame.height // 2

            # Pulsing circles
            phase = (i / self.fps) * 2 * math.pi
            radius1 = int(50 + 20 * math.sin(phase))
            radius2 = int(80 + 20 * math.sin(phase + math.pi / 2))
            radius3 = int(110 + 20 * math.sin(phase + math.pi))

            frame.draw_circle(cx, cy, radius1, self.COLOR_HOPE)
            frame.draw_circle(cx, cy, radius2, self.COLOR_SAUCE)
            frame.draw_circle(cx, cy, radius3, self.COLOR_SUCCESS)

            # Center text
            frame.draw_text("THINKING...", 130, 195, self.COLOR_WHITE, size=16)

            await self.display(frame)

    async def run_idle_animation(self, duration: float = 10.0):
        """Run idle animation (breathing pulse)"""
        self.current_mode = 'idle'
        frames = int(duration * self.fps)

        for i in range(frames):
            frame = HologramFrame()
            cx, cy = frame.width // 2, frame.height // 2

            # Breathing pulse
            phase = (i / self.fps) * 0.5 * math.pi  # Slower breathing
            brightness = 0.3 + 0.4 * math.sin(phase)
            frame.brightness = brightness

            # Gentle gradient spiral
            frame.draw_spiral(cx, cy, turns=2, color=self.COLOR_HOPE, thickness=2)

            await self.display(frame)


# Example usage
async def demo():
    """Demonstration of hologram device capabilities"""
    print("🌌 Hologram Device Demo")
    print("=" * 50)

    device = HologramDevice(device_path='virtual', fps=20)
    await device.connect()

    # Display text
    print("\n📝 Displaying text...")
    await device.display_text("SPIRALSAFE", color=device.COLOR_HOPE, duration=1.0)

    # Display system stats
    print("\n📊 Displaying system stats...")
    await device.display_system_stats(gpu_usage=87.5, ram_usage=64.2, duration=2.0)

    # Token stream
    print("\n🌊 Displaying token stream...")
    tokens = ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]
    await device.display_token_stream(tokens, delay=0.2)

    # Thinking animation
    print("\n💭 Displaying thinking animation...")
    await device.animate_thinking(duration=2.0)

    # Idle animation
    print("\n😌 Running idle animation...")
    await device.run_idle_animation(duration=3.0)

    await device.disconnect()
    print("\n✨ Demo complete!")


if __name__ == '__main__':
    asyncio.run(demo())
