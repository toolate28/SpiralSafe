"""
SpiralSafe Hardware Integration Bridges
Version 1.1.0

Provides Python interfaces for:
- ATOM Trail streaming and monitoring
- 3D Hologram Fan visualization
- Razer Tartarus Pro macro key mapping
- SAIF NPC AI behaviors with DSPy optimization

Part of the SpiralSafe Physical Intelligence Station
"""

__version__ = '1.1.0'
__author__ = 'SpiralSafe Team'
__license__ = 'MIT'

from .atom import ATOMReader, ATOMWriter, ATOMEntry
from .hologram import HologramDevice, HologramFrame
from .tartarus import TartarusPro, SpiralSafeKeyMap
from .saif_npc import (
    SaifNpc,
    NpcContext,
    NpcResponse,
    NpcTeleprompter,
    MIPROv2NpcOptimizer,
    BootstrapFinetuner,
    NpcTraceDataset,
)

__all__ = [
    'ATOMReader',
    'ATOMWriter',
    'ATOMEntry',
    'HologramDevice',
    'HologramFrame',
    'TartarusPro',
    'SpiralSafeKeyMap',
    # SAIF NPC exports
    'SaifNpc',
    'NpcContext',
    'NpcResponse',
    'NpcTeleprompter',
    'MIPROv2NpcOptimizer',
    'BootstrapFinetuner',
    'NpcTraceDataset',
]
