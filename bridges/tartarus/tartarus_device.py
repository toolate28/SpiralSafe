"""
Razer Tartarus Pro Device SDK
Interface for 32-key programmable macro pad with analog switches

Provides async interface for SpiralSafe command mapping,
RGB lighting control, and cognitive mode triggers.
"""

import asyncio
import json
from typing import Optional, Callable, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import time


class KeyState(Enum):
    """Key press states"""
    RELEASED = 0
    PRESSED = 1
    HELD = 2


@dataclass
class KeyEvent:
    """Represents a key event from Tartarus"""
    key_id: int  # 1-32
    state: KeyState
    timestamp: float
    pressure: float = 1.0  # 0.0 to 1.0 (analog pressure)
    metadata: Dict[str, Any] = None


class TartarusPro:
    """Interface to Razer Tartarus Pro hardware"""

    def __init__(self, device_path: str = 'virtual'):
        """
        Initialize Tartarus Pro interface

        Args:
            device_path: Path to device (or 'virtual' for simulation)
        """
        self.device_path = device_path
        self.is_virtual = device_path == 'virtual'
        self.connected = False

        # Key bindings
        self.key_handlers: Dict[int, Callable] = {}
        self.key_states: Dict[int, KeyState] = {i: KeyState.RELEASED for i in range(1, 33)}

        # RGB state (per-key colors)
        self.key_colors: Dict[int, Tuple[int, int, int]] = {
            i: (0, 102, 255) for i in range(1, 33)  # Default: Hope Blue
        }

        # Color scheme (Hope && Sauce)
        self.COLOR_HOPE = (0, 102, 255)      # #0066FF
        self.COLOR_SAUCE = (255, 102, 0)     # #FF6600
        self.COLOR_SUCCESS = (0, 255, 170)   # #00FFAA
        self.COLOR_WARNING = (255, 170, 0)   # #FFAA00
        self.COLOR_ERROR = (255, 0, 102)     # #FF0066
        self.COLOR_WHITE = (255, 255, 255)
        self.COLOR_OFF = (0, 0, 0)

        # Current mode state
        self.current_mode = 'idle'

    async def connect(self):
        """Connect to Tartarus device"""
        if self.is_virtual:
            print("🎮 Connected to VIRTUAL Tartarus Pro device")
            self.connected = True
            await self.set_all_keys(color=self.COLOR_HOPE, brightness=0.3)
            return

        try:
            # In production, would use OpenRazer or Razer Chroma SDK
            await asyncio.sleep(0.1)
            self.connected = True
            print(f"✨ Connected to Tartarus Pro: {self.device_path}")
            await self.set_all_keys(color=self.COLOR_HOPE, brightness=0.3)
        except Exception as e:
            print(f"❌ Failed to connect to Tartarus: {e}")
            raise

    async def disconnect(self):
        """Disconnect from device"""
        # Turn off all LEDs
        await self.set_all_keys(color=self.COLOR_OFF)
        self.connected = False
        print("👋 Disconnected from Tartarus Pro")

    def on_key(self, key_id: int):
        """
        Decorator to bind a handler to a key

        Usage:
            @tartarus.on_key(1)
            async def handle_key_1():
                print("Key 1 pressed!")
        """
        def decorator(func: Callable):
            self.key_handlers[key_id] = func
            return func
        return decorator

    def bind_key(self, key_id: int, handler: Callable):
        """Bind a handler function to a key"""
        self.key_handlers[key_id] = handler

    async def handle_key_event(self, event: KeyEvent):
        """Process a key event"""
        if event.key_id in self.key_handlers and event.state == KeyState.PRESSED:
            handler = self.key_handlers[event.key_id]

            # Flash the key
            await self.flash_key(event.key_id, color=self.COLOR_SUCCESS, duration=0.1)

            # Call handler
            if asyncio.iscoroutinefunction(handler):
                await handler()
            else:
                handler()

    async def set_key_color(self, key_id: int, color: Tuple[int, int, int], brightness: float = 1.0):
        """
        Set color of a specific key

        Args:
            key_id: Key number (1-32)
            color: RGB tuple (0-255, 0-255, 0-255)
            brightness: Brightness multiplier (0.0-1.0)
        """
        if not (1 <= key_id <= 32):
            raise ValueError(f"Invalid key_id: {key_id} (must be 1-32)")

        # Apply brightness
        adjusted_color = tuple(int(c * brightness) for c in color)
        self.key_colors[key_id] = adjusted_color

        if self.is_virtual:
            print(f"  💡 Key {key_id:02d} → RGB{adjusted_color}")
        else:
            # In production, would send to Razer Chroma SDK
            pass

    async def set_all_keys(self, color: Tuple[int, int, int], brightness: float = 1.0):
        """Set all keys to the same color"""
        for key_id in range(1, 33):
            await self.set_key_color(key_id, color, brightness)

    async def flash_key(self, key_id: int, color: Tuple[int, int, int], duration: float = 0.2):
        """Flash a key briefly"""
        original_color = self.key_colors[key_id]

        # Flash on
        await self.set_key_color(key_id, color, brightness=1.0)
        await asyncio.sleep(duration)

        # Restore original
        await self.set_key_color(key_id, original_color)

    async def pulse_key(self, key_id: int, color: Tuple[int, int, int], cycles: int = 3, speed: float = 0.5):
        """Pulse a key (breathing effect)"""
        import math

        for cycle in range(cycles):
            for step in range(20):
                brightness = 0.3 + 0.7 * (math.sin(step / 20 * 2 * math.pi) + 1) / 2
                await self.set_key_color(key_id, color, brightness=brightness)
                await asyncio.sleep(speed / 20)

    async def set_mode_lighting(self, mode: str):
        """
        Set lighting mode

        Modes:
            - idle: Gentle blue-orange gradient
            - ultrathink: Bright blue pulsing
            - atom_active: Green flashing on ATOM keys
            - error: Red glow
            - safety: Yellow warning
        """
        self.current_mode = mode

        if mode == 'idle':
            # Blue-orange gradient (Hope && Sauce)
            for key_id in range(1, 33):
                # Gradient from blue to orange
                ratio = (key_id - 1) / 31
                r = int(self.COLOR_HOPE[0] * (1 - ratio) + self.COLOR_SAUCE[0] * ratio)
                g = int(self.COLOR_HOPE[1] * (1 - ratio) + self.COLOR_SAUCE[1] * ratio)
                b = int(self.COLOR_HOPE[2] * (1 - ratio) + self.COLOR_SAUCE[2] * ratio)
                await self.set_key_color(key_id, (r, g, b), brightness=0.3)

        elif mode == 'ultrathink':
            # All keys bright blue
            await self.set_all_keys(self.COLOR_HOPE, brightness=1.0)

        elif mode == 'atom_active':
            # ATOM operation keys (1-5) green
            for key_id in range(1, 6):
                await self.set_key_color(key_id, self.COLOR_SUCCESS, brightness=0.8)

        elif mode == 'error':
            # All keys red
            await self.set_all_keys(self.COLOR_ERROR, brightness=0.7)

        elif mode == 'safety':
            # All keys yellow warning
            await self.set_all_keys(self.COLOR_WARNING, brightness=0.6)

        if self.is_virtual:
            print(f"  🎨 Lighting mode: {mode}")

    async def simulate_key_press(self, key_id: int):
        """Simulate a key press (for testing)"""
        event = KeyEvent(
            key_id=key_id,
            state=KeyState.PRESSED,
            timestamp=time.time(),
            pressure=1.0
        )
        await self.handle_key_event(event)


# SpiralSafe Key Mapping Configuration
class SpiralSafeKeyMap:
    """Standard SpiralSafe key mapping for Tartarus Pro"""

    # Row 1: ATOM Operations
    ATOM_LOG = 1
    ATOM_VIEW = 2
    ATOM_SYNC = 3
    ATOM_QUERY = 4
    ATOM_CLEAR = 5

    # Row 2: AI Model Control
    MODEL_OPUS = 6
    MODEL_SONNET = 7
    MODEL_HAIKU = 8
    MODEL_LOCAL = 9
    MODEL_SWITCH = 10

    # Row 3: Cognitive Modes
    MODE_ULTRATHINK = 11
    MODE_NEGATIVE_SPACE = 12
    MODE_CREATIVE = 13
    MODE_SAFETY = 14

    # Row 4: System Commands
    CMD_DOCTOR = 15
    CMD_TASKS = 16
    CMD_CONFIG = 17
    CMD_DEBUG = 18
    CMD_COMPACT = 19

    # Row 5: Museum & Showcase
    MUSEUM = 20
    STORY = 21
    HOLOGRAM = 22
    SNAPSHOT = 23
    PUBLISH = 24

    # Row 6: Development Flow
    DEV_TEST = 25
    DEV_BUILD = 26
    DEV_COMMIT = 27
    DEV_PUSH = 28

    # Thumb Pad
    NAV_UP = 29
    NAV_LEFT = 30
    NAV_CENTER = 31
    NAV_RIGHT = 32

    @classmethod
    def get_key_name(cls, key_id: int) -> str:
        """Get human-readable name for key"""
        mapping = {
            1: "ATOM-LOG", 2: "ATOM-VIEW", 3: "ATOM-SYNC", 4: "ATOM-QUERY", 5: "CLEAR",
            6: "OPUS", 7: "SONNET", 8: "HAIKU", 9: "LOCAL-LLM", 10: "SWITCH",
            11: "ULTRATHINK", 12: "NEGATIVE-SPACE", 13: "CREATIVE", 14: "SAFETY",
            15: "/doctor", 16: "/tasks", 17: "/config", 18: "/debug", 19: "COMPACT",
            20: "MUSEUM", 21: "STORY", 22: "HOLOGRAM", 23: "SNAPSHOT", 24: "PUBLISH",
            25: "TEST", 26: "BUILD", 27: "COMMIT", 28: "PUSH",
            29: "↑", 30: "←", 31: "●", 32: "→"
        }
        return mapping.get(key_id, f"KEY-{key_id}")


# Example usage
async def demo():
    """Demonstration of Tartarus Pro capabilities"""
    print("🎮 Tartarus Pro Demo")
    print("=" * 50)

    tartarus = TartarusPro(device_path='virtual')
    await tartarus.connect()

    # Set up some key bindings
    @tartarus.on_key(SpiralSafeKeyMap.ATOM_LOG)
    async def handle_atom_log():
        print("  📝 ATOM-LOG triggered!")
        await tartarus.flash_key(1, tartarus.COLOR_SUCCESS, duration=0.2)

    @tartarus.on_key(SpiralSafeKeyMap.MODE_ULTRATHINK)
    async def handle_ultrathink():
        print("  🧠 ULTRATHINK mode activated!")
        await tartarus.set_mode_lighting('ultrathink')

    # Test key presses
    print("\n🔘 Simulating key presses...")
    await tartarus.simulate_key_press(SpiralSafeKeyMap.ATOM_LOG)
    await asyncio.sleep(0.5)

    await tartarus.simulate_key_press(SpiralSafeKeyMap.MODE_ULTRATHINK)
    await asyncio.sleep(0.5)

    # Test lighting modes
    print("\n💡 Testing lighting modes...")
    modes = ['idle', 'ultrathink', 'atom_active', 'error', 'safety']
    for mode in modes:
        print(f"  Setting mode: {mode}")
        await tartarus.set_mode_lighting(mode)
        await asyncio.sleep(0.5)

    # Pulse effect
    print("\n✨ Testing pulse effect...")
    await tartarus.pulse_key(11, tartarus.COLOR_HOPE, cycles=2)

    await tartarus.disconnect()
    print("\n✨ Demo complete!")


if __name__ == '__main__':
    asyncio.run(demo())
