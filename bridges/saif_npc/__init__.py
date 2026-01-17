"""
SAIF NPC Module - DSPy-powered NPC AI Behaviors
Part of SpiralSafe HOPE-AI-NPC-SUITE

This module implements SAIF (Systematic Analysis and Issue Fixing)
methodology for tuning NPC AI behaviors using DSPy's optimization
framework. It provides:

- Context-aware NPC response generation
- MIPROv2 teleprompter for NPC trace bootstrapping
- BootstrapFinetune for context-aware responses
- Integration with bump-spec handoff protocol

H&&S:WAVE | Hope&&Sauced
"""

__version__ = '1.0.0'
__author__ = 'SpiralSafe Team'
__license__ = 'MIT'

from .saif_npc import SaifNpc, NpcContext, NpcResponse
from .teleprompter import NpcTeleprompter, MIPROv2NpcOptimizer
from .finetuner import BootstrapFinetuner, NpcTraceDataset

__all__ = [
    'SaifNpc',
    'NpcContext',
    'NpcResponse',
    'NpcTeleprompter',
    'MIPROv2NpcOptimizer',
    'BootstrapFinetuner',
    'NpcTraceDataset',
]
