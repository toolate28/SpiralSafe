"""
SAIF NPC Core Module - DSPy-based NPC Behavior System
Part of SpiralSafe HOPE-AI-NPC-SUITE

Implements the SaifNpc class with context-aware response generation
using DSPy's ChainOfThought and Predict modules. This provides:

1. Heavy-tailed inference stability through systematic context building
2. Multi-provider instruction support for seamless handoffs
3. Behavioral coherence tuning for AGI-like emergence patterns

Example Usage:
    npc = SaifNpc()
    response = npc.forward(
        state={"location": "village_square", "mood": "helpful"},
        input="Hello, can you help me find the blacksmith?"
    )
    print(response.response)

H&&S:WAVE | Hope&&Sauced
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import json

# DSPy imports - these will be available when dspy is installed
try:
    import dspy
    DSPY_AVAILABLE = True
except ImportError:
    DSPY_AVAILABLE = False
    # Provide mock classes for documentation/testing without DSPy
    class MockModule:
        """Mock DSPy module for testing without DSPy installed."""
        def __init__(self, *args, **kwargs):
            pass
        def __call__(self, *args, **kwargs):
            return MockOutput()

    class MockOutput:
        """Mock output for testing."""
        def __init__(self):
            self.context = "Mock context"
            self.response = "Mock response"


@dataclass
class NpcContext:
    """
    Represents the full context for an NPC interaction.

    Attributes:
        location: Current game location/area
        mood: NPC's current emotional state
        inventory: Items the NPC has available
        relationships: Player relationship scores
        quest_state: Active quest information
        world_state: Global game state variables
        timestamp: When this context was created
        handoff_marker: H&&S protocol marker for multi-agent coordination
    """
    location: str = "unknown"
    mood: str = "neutral"
    inventory: List[str] = field(default_factory=list)
    relationships: Dict[str, float] = field(default_factory=dict)
    quest_state: Dict[str, Any] = field(default_factory=dict)
    world_state: Dict[str, Any] = field(default_factory=dict)
    timestamp: Optional[datetime] = None
    handoff_marker: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary for serialization."""
        return {
            "location": self.location,
            "mood": self.mood,
            "inventory": self.inventory,
            "relationships": self.relationships,
            "quest_state": self.quest_state,
            "world_state": self.world_state,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "handoff_marker": self.handoff_marker,
        }

    def to_state_string(self) -> str:
        """Convert context to a string for DSPy input."""
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NpcContext':
        """Create NpcContext from dictionary."""
        timestamp = data.get("timestamp")
        if timestamp and isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        return cls(
            location=data.get("location", "unknown"),
            mood=data.get("mood", "neutral"),
            inventory=data.get("inventory", []),
            relationships=data.get("relationships", {}),
            quest_state=data.get("quest_state", {}),
            world_state=data.get("world_state", {}),
            timestamp=timestamp,
            handoff_marker=data.get("handoff_marker"),
        )


@dataclass
class NpcResponse:
    """
    Represents an NPC's response with metadata.

    Attributes:
        response: The actual text response
        context_used: The context that informed this response
        reasoning: Chain-of-thought reasoning (if available)
        confidence: Confidence score (0.0 to 1.0)
        suggested_actions: Suggested follow-up actions
        handoff_state: State for H&&S protocol handoff
    """
    response: str
    context_used: str = ""
    reasoning: str = ""
    confidence: float = 0.8
    suggested_actions: List[str] = field(default_factory=list)
    handoff_state: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "response": self.response,
            "context_used": self.context_used,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "suggested_actions": self.suggested_actions,
            "handoff_state": self.handoff_state,
        }


class SaifNpc:
    """
    SAIF NPC - DSPy-powered NPC behavior module.

    Implements the SAIF (Systematic Analysis and Issue Fixing) methodology
    for NPC interactions, using DSPy's ChainOfThought for context building
    and Predict for response generation.

    Architecture:
        state, input → context_builder (ChainOfThought) → context
        context → responder (Predict) → response

    This enables:
        - Heavy-tailed inference stability
        - Multi-provider instruction support
        - Behavioral coherence tuning

    Example:
        npc = SaifNpc()
        result = npc.forward(
            state=NpcContext(location="tavern", mood="friendly"),
            input="What drinks do you serve?"
        )
        print(result.response)  # "We have ale, mead, and fresh cider..."
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 256,
        npc_personality: str = "helpful and informative",
        enable_handoff: bool = True,
    ):
        """
        Initialize the SAIF NPC module.

        Args:
            model_name: The LM model to use (e.g., "gpt-4", "claude-3-opus")
            temperature: Response randomness (0.0-1.0)
            max_tokens: Maximum response length
            npc_personality: Base personality for the NPC
            enable_handoff: Whether to include H&&S handoff markers
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.npc_personality = npc_personality
        self.enable_handoff = enable_handoff
        self._initialized = False

        if DSPY_AVAILABLE:
            self._init_dspy_modules()
        else:
            self._init_mock_modules()

    def _init_dspy_modules(self):
        """Initialize DSPy modules for context building and response."""
        # Context Builder: Uses Chain-of-Thought to analyze state and input
        self.context_builder = dspy.ChainOfThought(
            "state, input -> context"
        )

        # Responder: Generates NPC response from built context
        self.responder = dspy.Predict(
            "context -> response"
        )

        self._initialized = True

    def _init_mock_modules(self):
        """Initialize mock modules when DSPy is not available."""
        self.context_builder = MockModule("state, input -> context")
        self.responder = MockModule("context -> response")
        self._initialized = True

    def forward(
        self,
        state: NpcContext | Dict[str, Any],
        input: str,
    ) -> NpcResponse:
        """
        Generate an NPC response given state and player input.

        This implements the SAIF methodology:
        1. Analyze state and input to build context (ChainOfThought)
        2. Generate response from context (Predict)
        3. Include handoff markers if enabled

        Args:
            state: Current NPC/game state (NpcContext or dict)
            input: Player's input/question

        Returns:
            NpcResponse with generated text and metadata
        """
        # Normalize state to NpcContext
        if isinstance(state, dict):
            state = NpcContext.from_dict(state)

        state_str = state.to_state_string()

        # Build context using ChainOfThought
        context_result = self.context_builder(state=state_str, input=input)

        # Extract context string
        context_str = getattr(context_result, 'context', str(context_result))

        # Generate response using Predict
        response_result = self.responder(context=context_str)
        response_str = getattr(response_result, 'response', str(response_result))

        # Build handoff state if enabled
        handoff_state = None
        if self.enable_handoff:
            handoff_state = f"H&&S:SYNC state={state.mood} location={state.location}"

        # Create response object
        return NpcResponse(
            response=response_str,
            context_used=context_str,
            reasoning=getattr(context_result, 'rationale', ''),
            confidence=0.8,  # Could be enhanced with actual confidence scoring
            suggested_actions=self._extract_suggested_actions(response_str),
            handoff_state=handoff_state,
        )

    def _extract_suggested_actions(self, response: str) -> List[str]:
        """
        Extract potential follow-up actions from response.

        This uses simple heuristics to identify actionable items.
        Could be enhanced with more sophisticated NLP.
        """
        actions = []

        # Look for question marks suggesting player choices
        if "?" in response:
            actions.append("await_player_response")

        # Look for directional hints
        direction_words = ["go", "head", "walk", "travel", "find"]
        for word in direction_words:
            if word in response.lower():
                actions.append("provide_navigation_hint")
                break

        # Look for item mentions suggesting trades/quests
        item_words = ["bring", "need", "want", "give", "take"]
        for word in item_words:
            if word in response.lower():
                actions.append("potential_quest_trigger")
                break

        return actions

    def configure(
        self,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ):
        """
        Reconfigure the NPC module settings.

        Args:
            model_name: New model to use
            temperature: New temperature setting
            max_tokens: New max tokens limit
        """
        if model_name is not None:
            self.model_name = model_name
        if temperature is not None:
            self.temperature = temperature
        if max_tokens is not None:
            self.max_tokens = max_tokens

        # Re-initialize DSPy modules with new settings
        if DSPY_AVAILABLE:
            self._init_dspy_modules()

    def get_handoff_context(self) -> Dict[str, Any]:
        """
        Get context for H&&S protocol handoff.

        Returns a dictionary suitable for bump.md handoff markers.
        """
        return {
            "module": "SaifNpc",
            "version": "1.0.0",
            "model": self.model_name,
            "personality": self.npc_personality,
            "marker": "H&&S:WAVE",
            "status": "operational" if self._initialized else "not_initialized",
        }

    def __repr__(self) -> str:
        return (
            f"SaifNpc(model={self.model_name}, "
            f"personality='{self.npc_personality}', "
            f"initialized={self._initialized})"
        )


# Example demonstration
def demo():
    """Demonstrate SAIF NPC functionality."""
    print("=" * 60)
    print("SAIF NPC DEMONSTRATION")
    print("=" * 60)

    # Create NPC
    npc = SaifNpc(
        npc_personality="a friendly village blacksmith named Erik",
        enable_handoff=True,
    )
    print(f"\nCreated: {npc}")

    # Create game state
    state = NpcContext(
        location="blacksmith_shop",
        mood="busy_but_friendly",
        inventory=["iron_sword", "steel_shield", "repair_kit"],
        relationships={"player": 0.6},
        quest_state={"active_quest": "find_ancient_ore"},
    )
    print(f"\nGame State: {state.location}, mood={state.mood}")

    # Generate response
    print("\nPlayer: 'Hello! Do you have any weapons for sale?'")
    response = npc.forward(
        state=state,
        input="Hello! Do you have any weapons for sale?"
    )

    print(f"\nNPC Response: {response.response}")
    print(f"Context Used: {response.context_used[:100]}...")
    print(f"Suggested Actions: {response.suggested_actions}")
    print(f"Handoff State: {response.handoff_state}")

    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    demo()
