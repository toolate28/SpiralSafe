"""
SpiralSafe Hardware Integration Bridges
Version 1.0.0

Provides Python interfaces for:
- ATOM Trail streaming and monitoring
- 3D Hologram Fan visualization
- Razer Tartarus Pro macro key mapping

Part of the SpiralSafe Physical Intelligence Station
"""

__version__ = '1.0.0'
__author__ = 'SpiralSafe Team'
__license__ = 'MIT'

from .atom import ATOMReader, ATOMWriter, ATOMEntry
from .hologram import HologramDevice, HologramFrame
from .tartarus import TartarusPro, SpiralSafeKeyMap

__all__ = [
    'ATOMReader',
    'ATOMWriter',
    'ATOMEntry',
    'HologramDevice',
    'HologramFrame',
    'TartarusPro',
    'SpiralSafeKeyMap',
]
