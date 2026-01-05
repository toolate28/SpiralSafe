#!/usr/bin/env python3
"""
Integration Test Suite for SpiralSafe Hardware Bridges
Tests all modules end-to-end with virtual devices
"""

import asyncio
import sys
import tempfile
from pathlib import Path

# Add bridges to path
sys.path.insert(0, str(Path(__file__).parent))

from atom import ATOMReader, ATOMWriter, ATOMEntry
from hologram import HologramDevice, HologramFrame
from tartarus import TartarusPro, SpiralSafeKeyMap


class IntegrationTestSuite:
    """Comprehensive integration tests for all bridges"""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.temp_dir = tempfile.mkdtemp()

    def test(self, name: str):
        """Decorator for test methods"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                try:
                    print(f"\n🧪 Testing: {name}")
                    await func(*args, **kwargs)
                    print(f"   ✅ PASS: {name}")
                    self.passed += 1
                except Exception as e:
                    print(f"   ❌ FAIL: {name}")
                    print(f"      Error: {e}")
                    self.failed += 1
            return wrapper
        return decorator

    async def run_all(self):
        """Run all integration tests"""
        print("=" * 60)
        print("SpiralSafe Hardware Bridges - Integration Test Suite")
        print("=" * 60)

        await self.test_atom_trail_write_read()
        await self.test_atom_trail_query()
        await self.test_hologram_basic()
        await self.test_hologram_visualizations()
        await self.test_tartarus_basic()
        await self.test_tartarus_key_binding()
        await self.test_end_to_end_flow()

        print("\n" + "=" * 60)
        print(f"Test Results: {self.passed} passed, {self.failed} failed")
        print("=" * 60)

        return self.failed == 0

    async def test_atom_trail_write_read(self):
        """Test ATOM trail writing and reading"""
        trail_path = Path(self.temp_dir) / "test_trail.atom"

        # Write entries
        writer = ATOMWriter(str(trail_path))
        await writer.write('CONFIG', 'Test initialization', {'test': True})
        await writer.write('STATUS', 'Test status update')
        await writer.write('ERROR', 'Test error message')

        # Read entries
        reader = ATOMReader(str(trail_path))
        entries = await reader.read_all()

        assert len(entries) == 3, f"Expected 3 entries, got {len(entries)}"
        assert entries[0].entry_type == 'CONFIG', "First entry should be CONFIG"
        assert entries[0].context.get('test') == True, "Context not preserved"
        assert entries[1].entry_type == 'STATUS', "Second entry should be STATUS"
        assert entries[2].entry_type == 'ERROR', "Third entry should be ERROR"

        print(f"      - Written and read {len(entries)} entries")
        print(f"      - Context preservation verified")

    async def test_atom_trail_query(self):
        """Test ATOM trail querying"""
        trail_path = Path(self.temp_dir) / "test_trail2.atom"

        writer = ATOMWriter(str(trail_path))
        await writer.write('CONFIG', 'Config entry 1')
        await writer.write('ERROR', 'Error entry 1')
        await writer.write('CONFIG', 'Config entry 2')
        await writer.write('STATUS', 'Status entry 1')

        reader = ATOMReader(str(trail_path))

        # Query by type
        errors = await reader.query(entry_type='ERROR')
        assert len(errors) == 1, f"Expected 1 error, got {len(errors)}"

        configs = await reader.query(entry_type='CONFIG')
        assert len(configs) == 2, f"Expected 2 configs, got {len(configs)}"

        # Query with limit
        limited = await reader.query(limit=2)
        assert len(limited) == 2, f"Expected 2 entries, got {len(limited)}"

        print(f"      - Type filtering: OK")
        print(f"      - Limit filtering: OK")

    async def test_hologram_basic(self):
        """Test hologram basic operations"""
        device = HologramDevice(device_path='virtual', fps=20)
        await device.connect()

        assert device.connected, "Device should be connected"
        assert device.is_virtual, "Should be virtual device"

        # Test text display
        await device.display_text("TEST", color=device.COLOR_HOPE, duration=0.1)

        # Test frame creation
        frame = HologramFrame()
        assert frame.width == 400, "Frame width should be 400"
        assert frame.height == 400, "Frame height should be 400"

        await device.disconnect()
        assert not device.connected, "Device should be disconnected"

        print(f"      - Device connection: OK")
        print(f"      - Text display: OK")
        print(f"      - Frame creation: OK")

    async def test_hologram_visualizations(self):
        """Test hologram visualization modes"""
        device = HologramDevice(device_path='virtual', fps=20)
        await device.connect()

        # Test system stats
        await device.display_system_stats(gpu_usage=75.0, ram_usage=50.0, duration=0.1)

        # Test token stream
        tokens = ["Test", "token", "stream"]
        await device.display_token_stream(tokens, delay=0.01)

        # Test thinking animation
        await device.animate_thinking(duration=0.1)

        # Test idle animation
        await device.run_idle_animation(duration=0.1)

        await device.disconnect()

        print(f"      - System stats display: OK")
        print(f"      - Token stream: OK")
        print(f"      - Animations: OK")

    async def test_tartarus_basic(self):
        """Test Tartarus basic operations"""
        device = TartarusPro(device_path='virtual')
        await device.connect()

        assert device.connected, "Device should be connected"
        assert device.is_virtual, "Should be virtual device"

        # Test key color setting
        await device.set_key_color(1, device.COLOR_HOPE, brightness=1.0)
        assert device.key_colors[1] == device.COLOR_HOPE, "Key color not set"

        # Test all keys
        await device.set_all_keys(device.COLOR_SAUCE, brightness=0.5)

        # Test flash
        await device.flash_key(11, device.COLOR_SUCCESS, duration=0.01)

        await device.disconnect()
        assert not device.connected, "Device should be disconnected"

        print(f"      - Device connection: OK")
        print(f"      - Key color control: OK")
        print(f"      - Lighting effects: OK")

    async def test_tartarus_key_binding(self):
        """Test Tartarus key binding system"""
        device = TartarusPro(device_path='virtual')
        await device.connect()

        # Test decorator binding
        called = False

        @device.on_key(SpiralSafeKeyMap.ATOM_LOG)
        async def test_handler():
            nonlocal called
            called = True

        # Simulate key press
        await device.simulate_key_press(SpiralSafeKeyMap.ATOM_LOG)

        assert called, "Key handler should have been called"

        # Test manual binding
        called2 = False

        async def test_handler2():
            nonlocal called2
            called2 = True

        device.bind_key(SpiralSafeKeyMap.MODE_ULTRATHINK, test_handler2)
        await device.simulate_key_press(SpiralSafeKeyMap.MODE_ULTRATHINK)

        assert called2, "Manual bound handler should have been called"

        await device.disconnect()

        print(f"      - Decorator binding: OK")
        print(f"      - Manual binding: OK")
        print(f"      - Key event handling: OK")

    async def test_end_to_end_flow(self):
        """Test complete end-to-end workflow"""
        trail_path = Path(self.temp_dir) / "e2e_trail.atom"

        # Setup all devices
        atom_writer = ATOMWriter(str(trail_path))
        atom_reader = ATOMReader(str(trail_path))
        hologram = HologramDevice(device_path='virtual', fps=20)
        tartarus = TartarusPro(device_path='virtual')

        await hologram.connect()
        await tartarus.connect()

        # Simulate workflow: key press -> ATOM log -> hologram display

        # 1. Simulate ATOM-LOG key press
        log_pressed = False

        @tartarus.on_key(SpiralSafeKeyMap.ATOM_LOG)
        async def handle_atom_log():
            nonlocal log_pressed
            log_pressed = True
            # Write ATOM entry
            await atom_writer.write('STATUS', 'ATOM-LOG key pressed', {'source': 'tartarus'})
            # Flash key
            await tartarus.flash_key(SpiralSafeKeyMap.ATOM_LOG, tartarus.COLOR_SUCCESS, duration=0.01)

        await tartarus.simulate_key_press(SpiralSafeKeyMap.ATOM_LOG)
        assert log_pressed, "Key should have been pressed"

        # 2. Read the entry
        entries = await atom_reader.read_all()
        assert len(entries) == 1, "Should have 1 entry"
        entry = entries[0]

        # 3. Display on hologram
        await hologram.display_atom_entry(entry, duration=0.1)

        # 4. Set lighting mode
        await tartarus.set_mode_lighting('atom_active')

        await hologram.disconnect()
        await tartarus.disconnect()

        print(f"      - Key press simulation: OK")
        print(f"      - ATOM logging: OK")
        print(f"      - Hologram visualization: OK")
        print(f"      - Multi-device coordination: OK")


async def main():
    """Run the test suite"""
    suite = IntegrationTestSuite()
    success = await suite.run_all()

    if success:
        print("\n✨ ALL TESTS PASSED - 0% IMPLEMENTATION GAP ✨\n")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED - GAPS DETECTED ❌\n")
        return 1


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
