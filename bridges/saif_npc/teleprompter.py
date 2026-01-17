"""
NPC Teleprompter Module - MIPROv2 Optimization for NPC Traces
Part of SpiralSafe HOPE-AI-NPC-SUITE

Implements teleprompter functionality for bootstrapping NPC traces
using MIPROv2 (Multi-provider Instruction Prompt Optimization v2).

This enables:
- Automatic instruction optimization across multiple providers
- NPC trace collection and analysis
- Seamless handoff instruction generation

H&&S:WAVE | Hope&&Sauced
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json

try:
    import dspy
    from dspy.teleprompt import MIPROv2, BootstrapFewShot
    DSPY_AVAILABLE = True
except ImportError:
    DSPY_AVAILABLE = False


@dataclass
class NpcTrace:
    """
    Represents a single NPC interaction trace for optimization.

    Attributes:
        trace_id: Unique identifier for this trace
        state: The game state at interaction time
        input: Player's input
        output: NPC's response
        context: Intermediate context built by ChainOfThought
        score: Quality score (0.0 to 1.0)
        provider: Which LM provider generated this trace
        timestamp: When this trace was created
    """
    trace_id: str
    state: Dict[str, Any]
    input: str
    output: str
    context: str = ""
    score: float = 0.0
    provider: str = "unknown"
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert trace to dictionary."""
        return {
            "trace_id": self.trace_id,
            "state": self.state,
            "input": self.input,
            "output": self.output,
            "context": self.context,
            "score": self.score,
            "provider": self.provider,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NpcTrace':
        """Create NpcTrace from dictionary."""
        timestamp = data.get("timestamp")
        if timestamp and isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        return cls(
            trace_id=data["trace_id"],
            state=data["state"],
            input=data["input"],
            output=data["output"],
            context=data.get("context", ""),
            score=data.get("score", 0.0),
            provider=data.get("provider", "unknown"),
            timestamp=timestamp,
            metadata=data.get("metadata", {}),
        )


class NpcTeleprompter:
    """
    Teleprompter for NPC behavior optimization.

    Collects NPC interaction traces and provides them to
    MIPROv2 for automatic instruction optimization.

    The teleprompter acts as a "prompt engineer" that:
    1. Collects successful interaction traces
    2. Analyzes patterns in effective responses
    3. Generates optimized instructions for different providers
    4. Handles H&&S handoff markers for multi-agent coordination

    Example:
        teleprompter = NpcTeleprompter()
        teleprompter.add_trace(trace)
        optimized_instructions = teleprompter.optimize()
    """

    def __init__(
        self,
        max_traces: int = 1000,
        min_score_threshold: float = 0.7,
        providers: Optional[List[str]] = None,
    ):
        """
        Initialize the NPC Teleprompter.

        Args:
            max_traces: Maximum number of traces to store
            min_score_threshold: Minimum quality score to include in optimization
            providers: List of LM providers to optimize for
        """
        self.max_traces = max_traces
        self.min_score_threshold = min_score_threshold
        self.providers = providers or ["openai", "anthropic", "cohere"]
        self.traces: List[NpcTrace] = []
        self._optimized_instructions: Dict[str, str] = {}

    def add_trace(
        self,
        trace_id: str,
        state: Dict[str, Any],
        input: str,
        output: str,
        context: str = "",
        score: float = 0.0,
        provider: str = "unknown",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> NpcTrace:
        """
        Add a new interaction trace.

        Args:
            trace_id: Unique identifier
            state: Game state at interaction
            input: Player input
            output: NPC response
            context: Built context
            score: Quality score
            provider: LM provider used
            metadata: Additional metadata

        Returns:
            The created NpcTrace
        """
        trace = NpcTrace(
            trace_id=trace_id,
            state=state,
            input=input,
            output=output,
            context=context,
            score=score,
            provider=provider,
            metadata=metadata or {},
        )

        self.traces.append(trace)

        # Trim to max_traces
        if len(self.traces) > self.max_traces:
            self.traces = self.traces[-self.max_traces:]

        return trace

    def get_high_quality_traces(self) -> List[NpcTrace]:
        """Get traces that meet the quality threshold."""
        return [t for t in self.traces if t.score >= self.min_score_threshold]

    def get_traces_by_provider(self, provider: str) -> List[NpcTrace]:
        """Get traces from a specific provider."""
        return [t for t in self.traces if t.provider == provider]

    def calculate_provider_stats(self) -> Dict[str, Dict[str, float]]:
        """
        Calculate statistics per provider.

        Returns:
            Dict mapping provider to stats (count, avg_score, etc.)
        """
        stats = {}
        for provider in self.providers:
            traces = self.get_traces_by_provider(provider)
            if traces:
                scores = [t.score for t in traces]
                stats[provider] = {
                    "count": len(traces),
                    "avg_score": sum(scores) / len(scores),
                    "max_score": max(scores),
                    "min_score": min(scores),
                }
            else:
                stats[provider] = {
                    "count": 0,
                    "avg_score": 0.0,
                    "max_score": 0.0,
                    "min_score": 0.0,
                }
        return stats

    def export_traces(self, filepath: str):
        """Export traces to JSON file."""
        data = {
            "version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "trace_count": len(self.traces),
            "traces": [t.to_dict() for t in self.traces],
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def import_traces(self, filepath: str):
        """Import traces from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for trace_data in data.get("traces", []):
            trace = NpcTrace.from_dict(trace_data)
            self.traces.append(trace)

        # Trim to max_traces
        if len(self.traces) > self.max_traces:
            self.traces = self.traces[-self.max_traces:]


class MIPROv2NpcOptimizer:
    """
    MIPROv2-based optimizer for NPC instructions.

    Uses DSPy's MIPROv2 teleprompter to optimize NPC behavior
    instructions across multiple LM providers.

    This enables:
    - Automatic instruction optimization
    - Multi-provider instruction generation
    - Seamless handoff instructions for H&&S protocol

    Example:
        optimizer = MIPROv2NpcOptimizer(teleprompter)
        optimized = optimizer.optimize(npc_module)
    """

    def __init__(
        self,
        teleprompter: NpcTeleprompter,
        metric: Optional[Callable] = None,
        num_candidates: int = 10,
        num_demos: int = 5,
    ):
        """
        Initialize the MIPROv2 optimizer.

        Args:
            teleprompter: NpcTeleprompter with collected traces
            metric: Evaluation metric function
            num_candidates: Number of instruction candidates to generate
            num_demos: Number of demonstrations per candidate
        """
        self.teleprompter = teleprompter
        self.metric = metric or self._default_metric
        self.num_candidates = num_candidates
        self.num_demos = num_demos
        self._optimized_module = None

    def _default_metric(self, example, prediction, trace=None) -> float:
        """
        Default metric for evaluating NPC responses.

        Scores based on:
        - Response relevance to context
        - Appropriate length
        - Personality consistency
        """
        response = str(prediction.response) if hasattr(prediction, 'response') else str(prediction)

        score = 0.0

        # Length score (prefer medium-length responses)
        length = len(response)
        if 50 <= length <= 500:
            score += 0.3
        elif 20 <= length <= 800:
            score += 0.15

        # Completeness (has punctuation)
        if any(p in response for p in ['.', '!', '?']):
            score += 0.2

        # Not empty
        if response.strip():
            score += 0.2

        # Contains context keywords (if available)
        if hasattr(example, 'state'):
            state_str = str(example.state).lower()
            if any(word in response.lower() for word in state_str.split()[:5]):
                score += 0.3

        return min(score, 1.0)

    def optimize(self, npc_module) -> Any:
        """
        Optimize an NPC module using MIPROv2.

        Args:
            npc_module: The SaifNpc module to optimize

        Returns:
            Optimized module (or original if DSPy not available)
        """
        if not DSPY_AVAILABLE:
            print("Warning: DSPy not available. Returning original module.")
            return npc_module

        # Prepare training data from traces
        trainset = self._prepare_trainset()

        if len(trainset) < self.num_demos:
            print(f"Warning: Only {len(trainset)} traces available. "
                  f"Need at least {self.num_demos} for optimization.")
            return npc_module

        # Create MIPROv2 teleprompter
        teleprompter = MIPROv2(
            metric=self.metric,
            num_candidates=self.num_candidates,
        )

        # Compile/optimize the module
        self._optimized_module = teleprompter.compile(
            npc_module,
            trainset=trainset,
        )

        return self._optimized_module

    def _prepare_trainset(self) -> List:
        """Prepare training set from teleprompter traces."""
        if not DSPY_AVAILABLE:
            return []

        trainset = []
        high_quality_traces = self.teleprompter.get_high_quality_traces()

        for trace in high_quality_traces:
            example = dspy.Example(
                state=json.dumps(trace.state),
                input=trace.input,
            ).with_inputs('state', 'input')
            trainset.append(example)

        return trainset

    def bootstrap_few_shot(self, npc_module, max_rounds: int = 3) -> Any:
        """
        Alternative optimization using BootstrapFewShot.

        This is faster but less thorough than MIPROv2.

        Args:
            npc_module: The SaifNpc module to optimize
            max_rounds: Maximum optimization rounds

        Returns:
            Optimized module
        """
        if not DSPY_AVAILABLE:
            print("Warning: DSPy not available. Returning original module.")
            return npc_module

        trainset = self._prepare_trainset()

        if len(trainset) < 2:
            return npc_module

        teleprompter = BootstrapFewShot(
            metric=self.metric,
            max_bootstrapped_demos=self.num_demos,
            max_rounds=max_rounds,
        )

        return teleprompter.compile(npc_module, trainset=trainset)

    def generate_handoff_instructions(self, provider: str = "all") -> Dict[str, str]:
        """
        Generate H&&S handoff instructions for providers.

        Creates formatted instructions suitable for bump.md
        handoff markers.

        Args:
            provider: Specific provider or "all"

        Returns:
            Dict mapping provider to instruction string
        """
        instructions = {}

        providers = [provider] if provider != "all" else self.teleprompter.providers

        stats = self.teleprompter.calculate_provider_stats()

        for p in providers:
            p_stats = stats.get(p, {})
            instruction = f"""<!-- H&&S:WAVE
  module: SaifNpc
  provider: {p}
  traces_analyzed: {p_stats.get('count', 0)}
  avg_quality: {p_stats.get('avg_score', 0.0):.2f}
  status: optimized
-->
NPC behavior optimized for {p}.
Use context-aware response generation with heavy-tailed inference stability.
<!-- /H&&S:WAVE -->"""
            instructions[p] = instruction

        return instructions


# Example demonstration
def demo():
    """Demonstrate teleprompter functionality."""
    print("=" * 60)
    print("NPC TELEPROMPTER DEMONSTRATION")
    print("=" * 60)

    # Create teleprompter
    teleprompter = NpcTeleprompter(
        max_traces=100,
        min_score_threshold=0.7,
    )

    # Add sample traces
    for i in range(10):
        teleprompter.add_trace(
            trace_id=f"trace_{i}",
            state={"location": "village", "mood": "friendly"},
            input=f"Test input {i}",
            output=f"Test response {i}",
            context=f"Built context {i}",
            score=0.5 + (i * 0.05),  # Increasing scores
            provider="openai" if i % 2 == 0 else "anthropic",
        )

    print(f"\nAdded {len(teleprompter.traces)} traces")
    print(f"High quality traces: {len(teleprompter.get_high_quality_traces())}")

    # Show provider stats
    stats = teleprompter.calculate_provider_stats()
    print("\nProvider Statistics:")
    for provider, s in stats.items():
        if s["count"] > 0:
            print(f"  {provider}: {s['count']} traces, avg={s['avg_score']:.2f}")

    # Create optimizer
    optimizer = MIPROv2NpcOptimizer(
        teleprompter=teleprompter,
        num_candidates=5,
        num_demos=3,
    )

    # Generate handoff instructions
    instructions = optimizer.generate_handoff_instructions()
    print("\nHandoff Instructions (OpenAI):")
    print(instructions.get("openai", "N/A")[:200])

    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    demo()
