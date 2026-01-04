#!/usr/bin/env python3
"""
Hologram Bridge - ATOM Trail to 3D Hologram Streamer
Part of SpiralSafe Hardware Integration Suite

Streams ATOM trail + AI inference to 3D hologram fan in real-time.
Provides visual feedback for system operations, AI thinking, and data flow.

Usage:
    python hologram-bridge.py [--device DEVICE] [--fps FPS] [--mode MODE]

Modes:
    - atom: Stream ATOM trail entries (default)
    - thinking: Show AI thinking animation
    - idle: Gentle breathing pulse
    - stats: System resource monitoring
"""

import asyncio
import argparse
import signal
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# Add bridges to path
sys.path.insert(0, str(Path(__file__).parent))

from atom.atom_trail import ATOMReader, ATOMEntry
from hologram.hologram_device import HologramDevice


class HologramBridge:
    """Main bridge coordinator for ATOM → Hologram streaming"""

    def __init__(self, device_path: str = 'virtual', fps: int = 20):
        self.device = HologramDevice(device_path=device_path, fps=fps)
        self.atom_reader = ATOMReader()
        self.running = False
        self.current_mode = 'atom'

    async def start(self):
        """Start the bridge"""
        print("🌀 Starting Hologram Bridge...")
        print(f"   Device: {self.device.device_path}")
        print(f"   FPS: {self.device.fps}")
        print("=" * 50)

        await self.device.connect()
        self.running = True

        # Show startup message
        await self.device.display_text("SPIRALSAFE", color=self.device.COLOR_HOPE, duration=1.5)
        await self.device.display_text("BRIDGE ACTIVE", color=self.device.COLOR_SUCCESS, duration=1.0)

        print("✨ Bridge active! Streaming ATOM trail...\n")

    async def stop(self):
        """Stop the bridge gracefully"""
        print("\n\n🛑 Stopping Hologram Bridge...")
        self.running = False

        await self.device.display_text("BRIDGE OFFLINE", color=self.device.COLOR_WARNING, duration=1.0)
        await self.device.disconnect()

        print("👋 Bridge stopped.")

    async def stream_atom_trail(self):
        """Stream ATOM trail entries to hologram"""
        entry_count = 0
        recent_entries = []

        try:
            async for entry in self.atom_reader.stream(follow=True):
                if not self.running:
                    break

                entry_count += 1
                recent_entries.append(entry)

                # Keep last 50 entries for spiral visualization
                if len(recent_entries) > 50:
                    recent_entries.pop(0)

                # Display current entry
                print(f"  [{entry.entry_type}] {entry.message}")
                await self.device.display_atom_entry(entry, duration=1.0)

                # Every 10 entries, show spiral visualization
                if entry_count % 10 == 0:
                    print(f"  📊 Displaying spiral view ({len(recent_entries)} entries)...")
                    await self.device.display_atom_spiral(recent_entries, duration=2.0)

        except asyncio.CancelledError:
            print("  Stream cancelled")
        except Exception as e:
            print(f"  ❌ Error streaming ATOM trail: {e}")

    async def run_thinking_mode(self, duration: Optional[float] = None):
        """Run continuous thinking animation"""
        print("💭 Running thinking animation mode...")

        elapsed = 0
        chunk_duration = 5.0

        while self.running and (duration is None or elapsed < duration):
            await self.device.animate_thinking(duration=chunk_duration)
            elapsed += chunk_duration

            if duration is not None:
                remaining = duration - elapsed
                print(f"  ⏱️  {remaining:.1f}s remaining...")

    async def run_idle_mode(self, duration: Optional[float] = None):
        """Run continuous idle animation"""
        print("😌 Running idle animation mode...")

        elapsed = 0
        chunk_duration = 10.0

        while self.running and (duration is None or elapsed < duration):
            await self.device.run_idle_animation(duration=chunk_duration)
            elapsed += chunk_duration

    async def run_stats_mode(self, duration: Optional[float] = None):
        """Display system stats continuously"""
        print("📊 Running system stats mode...")

        try:
            import psutil
            has_psutil = True
        except ImportError:
            print("  ⚠️  psutil not installed, using simulated stats")
            has_psutil = False

        elapsed = 0
        update_interval = 2.0

        while self.running and (duration is None or elapsed < duration):
            if has_psutil:
                # Real stats
                gpu_usage = 0  # Would need nvidia-smi or similar
                ram_usage = psutil.virtual_memory().percent
                cpu_usage = psutil.cpu_percent(interval=0.1)

                # Estimate GPU usage from CPU as fallback
                gpu_usage = min(cpu_usage * 1.2, 100)
            else:
                # Simulated stats
                import random
                gpu_usage = random.uniform(40, 90)
                ram_usage = random.uniform(50, 80)

            await self.device.display_system_stats(
                gpu_usage=gpu_usage,
                ram_usage=ram_usage,
                duration=update_interval
            )

            elapsed += update_interval
            print(f"  📈 GPU: {gpu_usage:.0f}% | RAM: {ram_usage:.0f}%")

    async def run(self, mode: str = 'atom', duration: Optional[float] = None):
        """
        Run the bridge in specified mode

        Args:
            mode: Operation mode (atom/thinking/idle/stats)
            duration: Optional duration (None = run forever)
        """
        await self.start()
        self.current_mode = mode

        try:
            if mode == 'atom':
                await self.stream_atom_trail()
            elif mode == 'thinking':
                await self.run_thinking_mode(duration=duration)
            elif mode == 'idle':
                await self.run_idle_mode(duration=duration)
            elif mode == 'stats':
                await self.run_stats_mode(duration=duration)
            else:
                print(f"❌ Unknown mode: {mode}")

        except KeyboardInterrupt:
            print("\n  🛑 Interrupted by user")
        finally:
            await self.stop()


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='SpiralSafe Hologram Bridge - Stream ATOM trail to 3D hologram',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Stream ATOM trail (default)
  python hologram-bridge.py

  # Use physical device
  python hologram-bridge.py --device /dev/hologram0

  # Show thinking animation for 30 seconds
  python hologram-bridge.py --mode thinking --duration 30

  # Display system stats
  python hologram-bridge.py --mode stats
        """
    )

    parser.add_argument(
        '--device',
        default='virtual',
        help='Hologram device path (default: virtual)'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=20,
        help='Target frames per second (default: 20)'
    )
    parser.add_argument(
        '--mode',
        choices=['atom', 'thinking', 'idle', 'stats'],
        default='atom',
        help='Operation mode (default: atom)'
    )
    parser.add_argument(
        '--duration',
        type=float,
        help='Run duration in seconds (default: run forever)'
    )

    args = parser.parse_args()

    # Create and run bridge
    bridge = HologramBridge(device_path=args.device, fps=args.fps)

    # Handle Ctrl+C gracefully
    loop = asyncio.get_event_loop()

    def signal_handler():
        print("\n🛑 Received interrupt signal...")
        bridge.running = False

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler)

    # Run bridge
    await bridge.run(mode=args.mode, duration=args.duration)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
