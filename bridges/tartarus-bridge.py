#!/usr/bin/env python3
"""
Tartarus Bridge - SpiralSafe Command Mapper for Razer Tartarus Pro
Part of SpiralSafe Hardware Integration Suite

Maps SpiralSafe commands to 32 programmable macro keys with RGB feedback.
Provides instant access to ATOM operations, AI models, cognitive modes,
and development workflows.

Usage:
    python tartarus-bridge.py [--device DEVICE] [--profile PROFILE]

Profiles:
    - spiralsafe: Full SpiralSafe key mapping (default)
    - dev: Development-focused shortcuts
    - minimal: Essential commands only
"""

import asyncio
import argparse
import signal
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Add bridges to path
sys.path.insert(0, str(Path(__file__).parent))

from tartarus.tartarus_device import TartarusPro, SpiralSafeKeyMap
from atom.atom_trail import ATOMWriter


class TartarusBridge:
    """Main bridge coordinator for Tartarus → SpiralSafe commands"""

    def __init__(self, device_path: str = 'virtual', profile: str = 'spiralsafe'):
        self.device = TartarusPro(device_path=device_path)
        self.atom_writer = ATOMWriter()
        self.profile = profile
        self.running = False
        self.ultrathink_mode = False

    async def start(self):
        """Start the bridge"""
        print("🎮 Starting Tartarus Bridge...")
        print(f"   Device: {self.device.device_path}")
        print(f"   Profile: {self.profile}")
        print("=" * 50)

        await self.device.connect()
        self.running = True

        # Load key bindings
        await self.load_profile(self.profile)

        # Set idle lighting
        await self.device.set_mode_lighting('idle')

        print("✨ Bridge active! Keys ready.\n")
        self.print_key_map()

    async def stop(self):
        """Stop the bridge gracefully"""
        print("\n\n🛑 Stopping Tartarus Bridge...")
        self.running = False

        await self.device.set_mode_lighting('error')
        await asyncio.sleep(0.5)
        await self.device.disconnect()

        print("👋 Bridge stopped.")

    def print_key_map(self):
        """Print current key mapping"""
        print("\n📋 Active Key Map:")
        print("-" * 50)
        print("Row 1 (ATOM):      [1]LOG [2]VIEW [3]SYNC [4]QUERY [5]CLEAR")
        print("Row 2 (AI):        [6]OPUS [7]SONNET [8]HAIKU [9]LOCAL [10]SWITCH")
        print("Row 3 (Cognitive): [11]ULTRATHINK [12]NEG-SPACE [13]CREATIVE [14]SAFETY")
        print("Row 4 (System):    [15]/doctor [16]/tasks [17]/config [18]/debug [19]COMPACT")
        print("Row 5 (Museum):    [20]MUSEUM [21]STORY [22]HOLOGRAM [23]SNAPSHOT [24]PUBLISH")
        print("Row 6 (Dev):       [25]TEST [26]BUILD [27]COMMIT [28]PUSH")
        print("Thumb Pad:         [29]↑ [30]← [31]● [32]→")
        print("-" * 50)

    async def load_profile(self, profile: str):
        """Load key binding profile"""

        if profile == 'spiralsafe':
            await self.load_spiralsafe_profile()
        elif profile == 'dev':
            await self.load_dev_profile()
        elif profile == 'minimal':
            await self.load_minimal_profile()
        else:
            print(f"⚠️  Unknown profile: {profile}, using spiralsafe")
            await self.load_spiralsafe_profile()

    async def load_spiralsafe_profile(self):
        """Load full SpiralSafe key mapping"""

        # Row 1: ATOM Operations
        @self.device.on_key(SpiralSafeKeyMap.ATOM_LOG)
        async def atom_log():
            print("📝 ATOM-LOG: Writing entry...")
            await self.atom_writer.write(
                'STATUS',
                'Manual ATOM entry via Tartarus',
                {'source': 'tartarus-bridge', 'key': 1}
            )
            await self.device.flash_key(1, self.device.COLOR_SUCCESS)
            print("   ✅ Entry written!")

        @self.device.on_key(SpiralSafeKeyMap.ATOM_VIEW)
        async def atom_view():
            print("👁️  ATOM-VIEW: Displaying recent entries...")
            # In production, would trigger hologram display
            await self.device.flash_key(2, self.device.COLOR_SUCCESS)

        @self.device.on_key(SpiralSafeKeyMap.ATOM_SYNC)
        async def atom_sync():
            print("🔄 ATOM-SYNC: Synchronizing trail...")
            await self.atom_writer.write('CONFIG', 'ATOM sync triggered')
            await self.device.flash_key(3, self.device.COLOR_SUCCESS)

        @self.device.on_key(SpiralSafeKeyMap.ATOM_QUERY)
        async def atom_query():
            print("🔍 ATOM-QUERY: Querying trail...")
            await self.device.flash_key(4, self.device.COLOR_SUCCESS)

        @self.device.on_key(SpiralSafeKeyMap.ATOM_CLEAR)
        async def atom_clear():
            print("🗑️  ATOM-CLEAR: Clearing display...")
            await self.device.flash_key(5, self.device.COLOR_WARNING)

        # Row 2: AI Model Control
        @self.device.on_key(SpiralSafeKeyMap.MODEL_OPUS)
        async def model_opus():
            print("🧠 MODEL: Switching to Opus...")
            await self.atom_writer.write('CONFIG', 'AI model switched to Opus')
            await self.device.flash_key(6, self.device.COLOR_SAUCE)

        @self.device.on_key(SpiralSafeKeyMap.MODEL_SONNET)
        async def model_sonnet():
            print("🎵 MODEL: Switching to Sonnet...")
            await self.atom_writer.write('CONFIG', 'AI model switched to Sonnet')
            await self.device.flash_key(7, self.device.COLOR_SAUCE)

        @self.device.on_key(SpiralSafeKeyMap.MODEL_HAIKU)
        async def model_haiku():
            print("🌸 MODEL: Switching to Haiku...")
            await self.atom_writer.write('CONFIG', 'AI model switched to Haiku')
            await self.device.flash_key(8, self.device.COLOR_SAUCE)

        # Row 3: Cognitive Modes
        @self.device.on_key(SpiralSafeKeyMap.MODE_ULTRATHINK)
        async def toggle_ultrathink():
            self.ultrathink_mode = not self.ultrathink_mode
            status = "ENABLED" if self.ultrathink_mode else "DISABLED"
            print(f"🧠 ULTRATHINK: {status}")

            await self.atom_writer.write(
                'CONFIG',
                f'Ultrathink mode {status}',
                {'mode': 'ultrathink', 'active': self.ultrathink_mode}
            )

            if self.ultrathink_mode:
                await self.device.set_mode_lighting('ultrathink')
            else:
                await self.device.set_mode_lighting('idle')

        @self.device.on_key(SpiralSafeKeyMap.MODE_NEGATIVE_SPACE)
        async def negative_space():
            print("🌌 NEGATIVE-SPACE: Analyzing gaps...")
            await self.atom_writer.write('STATUS', 'Negative space analysis initiated')
            await self.device.pulse_key(12, self.device.COLOR_HOPE, cycles=2)

        @self.device.on_key(SpiralSafeKeyMap.MODE_CREATIVE)
        async def creative_mode():
            print("🎨 CREATIVE: Entering creative mode...")
            await self.atom_writer.write('CONFIG', 'Creative mode activated')
            await self.device.flash_key(13, self.device.COLOR_SUCCESS)

        @self.device.on_key(SpiralSafeKeyMap.MODE_SAFETY)
        async def safety_mode():
            print("🛡️  SAFETY: Safety checkpoint...")
            await self.atom_writer.write('WARNING', 'Safety checkpoint triggered')
            await self.device.set_mode_lighting('safety')
            await asyncio.sleep(1)
            await self.device.set_mode_lighting('idle')

        # Row 4: System Commands
        @self.device.on_key(SpiralSafeKeyMap.CMD_DOCTOR)
        async def cmd_doctor():
            print("🏥 COMMAND: /doctor")
            await self.device.flash_key(15, self.device.COLOR_SUCCESS)

        @self.device.on_key(SpiralSafeKeyMap.CMD_TASKS)
        async def cmd_tasks():
            print("📋 COMMAND: /tasks")
            await self.device.flash_key(16, self.device.COLOR_SUCCESS)

        # Row 5: Museum & Showcase
        @self.device.on_key(SpiralSafeKeyMap.MUSEUM)
        async def museum():
            print("🏛️  MUSEUM: Opening Museum of Computation...")
            await self.atom_writer.write('STATUS', 'Museum accessed')
            await self.device.pulse_key(20, self.device.COLOR_SAUCE, cycles=2)

        @self.device.on_key(SpiralSafeKeyMap.HOLOGRAM)
        async def hologram():
            print("🌀 HOLOGRAM: Triggering hologram display...")
            await self.atom_writer.write('NETWORK', 'Hologram display activated')
            await self.device.flash_key(22, self.device.COLOR_HOPE)

        # Row 6: Development Flow
        @self.device.on_key(SpiralSafeKeyMap.DEV_TEST)
        async def dev_test():
            print("🧪 DEV: Running tests...")
            await self.atom_writer.write('STATUS', 'Test suite initiated')
            await self.device.pulse_key(25, self.device.COLOR_SUCCESS, cycles=1)

        @self.device.on_key(SpiralSafeKeyMap.DEV_BUILD)
        async def dev_build():
            print("🔨 DEV: Building project...")
            await self.atom_writer.write('STATUS', 'Build process started')
            await self.device.pulse_key(26, self.device.COLOR_SAUCE, cycles=1)

        @self.device.on_key(SpiralSafeKeyMap.DEV_COMMIT)
        async def dev_commit():
            print("💾 DEV: Committing changes...")
            await self.atom_writer.write('STATUS', 'Git commit triggered')
            await self.device.flash_key(27, self.device.COLOR_SUCCESS)

        @self.device.on_key(SpiralSafeKeyMap.DEV_PUSH)
        async def dev_push():
            print("🚀 DEV: Pushing to remote...")
            await self.atom_writer.write('NETWORK', 'Git push initiated')
            await self.device.flash_key(28, self.device.COLOR_SAUCE)

        print("✅ Loaded: SpiralSafe Profile (32 keys)")

    async def load_dev_profile(self):
        """Load development-focused profile"""
        # Simplified dev profile
        print("✅ Loaded: Dev Profile (development shortcuts)")

    async def load_minimal_profile(self):
        """Load minimal essential commands"""
        print("✅ Loaded: Minimal Profile (essential commands)")

    async def run_event_loop(self):
        """Run the main event loop (keyboard simulation for demo)"""
        print("\n⌨️  Listening for key events...")
        print("   (In production, this would receive events from Razer SDK)")
        print("   Press Ctrl+C to stop")

        try:
            while self.running:
                # In production, would receive real key events from hardware
                # For demo, we just keep running
                await asyncio.sleep(0.1)

        except KeyboardInterrupt:
            print("\n  🛑 Interrupted by user")

    async def run(self):
        """Run the bridge"""
        await self.start()

        try:
            await self.run_event_loop()
        except KeyboardInterrupt:
            print("\n  🛑 Interrupted by user")
        finally:
            await self.stop()


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='SpiralSafe Tartarus Bridge - Map commands to macro keys',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start with default SpiralSafe profile
  python tartarus-bridge.py

  # Use physical device
  python tartarus-bridge.py --device /dev/tartarus0

  # Load development profile
  python tartarus-bridge.py --profile dev
        """
    )

    parser.add_argument(
        '--device',
        default='virtual',
        help='Tartarus device path (default: virtual)'
    )
    parser.add_argument(
        '--profile',
        choices=['spiralsafe', 'dev', 'minimal'],
        default='spiralsafe',
        help='Key binding profile (default: spiralsafe)'
    )

    args = parser.parse_args()

    # Create and run bridge
    bridge = TartarusBridge(device_path=args.device, profile=args.profile)

    # Run bridge
    await bridge.run()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
