"""
ATOM Trail Streaming Module
Part of SpiralSafe Hardware Integration Suite

Provides async streaming interface to ATOM trail entries
for real-time visualization and monitoring.
"""

import asyncio
import json
import os
from pathlib import Path
from typing import AsyncIterator, Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass
import watchdog.observers
import watchdog.events


@dataclass
class ATOMEntry:
    """Represents a single ATOM trail entry"""
    timestamp: datetime
    entry_type: str
    message: str
    context: Dict[str, Any]
    raw_line: str

    @classmethod
    def from_line(cls, line: str) -> Optional['ATOMEntry']:
        """Parse an ATOM trail line into an ATOMEntry"""
        try:
            # ATOM format: [TIMESTAMP] TYPE: message | context
            line = line.strip()
            if not line or line.startswith('#'):
                return None

            # Extract timestamp
            if not line.startswith('['):
                return None
            timestamp_end = line.find(']')
            if timestamp_end == -1:
                return None

            timestamp_str = line[1:timestamp_end]
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

            # Extract type and message
            rest = line[timestamp_end + 1:].strip()
            if ':' not in rest:
                return None

            type_end = rest.find(':')
            entry_type = rest[:type_end].strip()
            message_part = rest[type_end + 1:].strip()

            # Extract context if present
            context = {}
            if '|' in message_part:
                message, context_str = message_part.split('|', 1)
                message = message.strip()
                try:
                    context = json.loads(context_str.strip())
                except json.JSONDecodeError:
                    context = {'raw': context_str.strip()}
            else:
                message = message_part

            return cls(
                timestamp=timestamp,
                entry_type=entry_type,
                message=message,
                context=context,
                raw_line=line
            )
        except Exception as e:
            # Silently skip malformed entries
            return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'type': self.entry_type,
            'message': self.message,
            'context': self.context
        }

    def get_color_code(self) -> str:
        """Get color code for visualization based on entry type"""
        color_map = {
            'CONFIG': '#0066FF',  # Hope Blue
            'STATUS': '#00FFAA',  # Success Green
            'NETWORK': '#FF6600', # Sauce Orange
            'ERROR': '#FF0066',   # Alert Red
            'WARNING': '#FFAA00', # Caution Yellow
            'INFO': '#FFFFFF',    # White
        }
        return color_map.get(self.entry_type, '#FFFFFF')


class ATOMReader:
    """Async reader for ATOM trail with real-time streaming support"""

    def __init__(self, trail_path: Optional[str] = None):
        """
        Initialize ATOM reader

        Args:
            trail_path: Path to ATOM trail file (default: ~/.kenl/.atom-trail)
        """
        if trail_path is None:
            trail_path = os.path.expanduser('~/.kenl/.atom-trail')

        self.trail_path = Path(trail_path)
        self._ensure_trail_exists()

    def _ensure_trail_exists(self):
        """Create ATOM trail file if it doesn't exist"""
        self.trail_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.trail_path.exists():
            self.trail_path.touch()

    async def read_all(self) -> list[ATOMEntry]:
        """Read all entries from ATOM trail"""
        entries = []
        try:
            with open(self.trail_path, 'r', encoding='utf-8') as f:
                for line in f:
                    entry = ATOMEntry.from_line(line)
                    if entry:
                        entries.append(entry)
        except FileNotFoundError:
            pass
        return entries

    async def stream(self, follow: bool = True) -> AsyncIterator[ATOMEntry]:
        """
        Stream ATOM entries in real-time

        Args:
            follow: If True, continues watching for new entries (tail -f behavior)
                   If False, reads existing entries and stops

        Yields:
            ATOMEntry objects as they're written to the trail
        """
        # First, read all existing entries
        entries = await self.read_all()
        for entry in entries:
            yield entry
            await asyncio.sleep(0)  # Yield control

        if not follow:
            return

        # Then watch for new entries
        class ATOMEventHandler(watchdog.events.FileSystemEventHandler):
            def __init__(self):
                self.queue = asyncio.Queue()

            def on_modified(self, event):
                if event.src_path == str(self.trail_path):
                    asyncio.create_task(self.queue.put('modified'))

        # Watch for file changes
        last_position = self.trail_path.stat().st_size if self.trail_path.exists() else 0

        while follow:
            try:
                current_size = self.trail_path.stat().st_size
                if current_size > last_position:
                    with open(self.trail_path, 'r', encoding='utf-8') as f:
                        f.seek(last_position)
                        for line in f:
                            entry = ATOMEntry.from_line(line)
                            if entry:
                                yield entry
                        last_position = f.tell()

                await asyncio.sleep(0.1)  # Poll every 100ms

            except FileNotFoundError:
                await asyncio.sleep(1)  # Wait for file to be created
            except Exception as e:
                print(f"Error streaming ATOM trail: {e}")
                await asyncio.sleep(1)

    async def query(self,
                   entry_type: Optional[str] = None,
                   since: Optional[datetime] = None,
                   until: Optional[datetime] = None,
                   limit: Optional[int] = None) -> list[ATOMEntry]:
        """
        Query ATOM trail with filters

        Args:
            entry_type: Filter by entry type (e.g., 'ERROR', 'CONFIG')
            since: Only entries after this timestamp
            until: Only entries before this timestamp
            limit: Maximum number of entries to return

        Returns:
            Filtered list of ATOMEntry objects
        """
        entries = await self.read_all()

        # Apply filters
        if entry_type:
            entries = [e for e in entries if e.entry_type == entry_type]

        if since:
            entries = [e for e in entries if e.timestamp >= since]

        if until:
            entries = [e for e in entries if e.timestamp <= until]

        # Apply limit
        if limit:
            entries = entries[-limit:]  # Get most recent N entries

        return entries


class ATOMWriter:
    """Write entries to ATOM trail"""

    def __init__(self, trail_path: Optional[str] = None):
        if trail_path is None:
            trail_path = os.path.expanduser('~/.kenl/.atom-trail')

        self.trail_path = Path(trail_path)
        self._ensure_trail_exists()

    def _ensure_trail_exists(self):
        """Create ATOM trail file if it doesn't exist"""
        self.trail_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.trail_path.exists():
            self.trail_path.touch()

    async def write(self,
                   entry_type: str,
                   message: str,
                   context: Optional[Dict[str, Any]] = None):
        """
        Write an entry to ATOM trail

        Args:
            entry_type: Type of entry (CONFIG, STATUS, ERROR, etc.)
            message: Human-readable message
            context: Optional context dictionary
        """
        timestamp = datetime.now().isoformat()

        # Format entry
        entry_line = f"[{timestamp}] {entry_type}: {message}"

        if context:
            context_json = json.dumps(context, separators=(',', ':'))
            entry_line += f" | {context_json}"

        entry_line += "\n"

        # Write to trail
        with open(self.trail_path, 'a', encoding='utf-8') as f:
            f.write(entry_line)


# Example usage and testing
async def demo():
    """Demonstration of ATOM trail streaming"""
    print("🌀 ATOM Trail Streaming Demo")
    print("=" * 50)

    # Create reader
    reader = ATOMReader()
    writer = ATOMWriter()

    # Write some test entries
    print("\n📝 Writing test entries...")
    await writer.write('CONFIG', 'System initialized', {'version': '1.0.0'})
    await writer.write('STATUS', 'All systems operational')
    await writer.write('NETWORK', 'Connected to hologram device', {'device': '/dev/hologram0'})

    # Query entries
    print("\n🔍 Querying ERROR entries...")
    errors = await reader.query(entry_type='ERROR', limit=10)
    print(f"Found {len(errors)} error entries")

    # Stream entries (first 5, then stop)
    print("\n📡 Streaming recent entries...")
    count = 0
    async for entry in reader.stream(follow=False):
        print(f"  [{entry.entry_type}] {entry.message}")
        count += 1
        if count >= 5:
            break

    print("\n✨ Demo complete!")


if __name__ == '__main__':
    asyncio.run(demo())
