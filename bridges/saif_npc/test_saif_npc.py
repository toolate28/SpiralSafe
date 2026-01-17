"""
Tests for SAIF NPC Module
Part of SpiralSafe HOPE-AI-NPC-SUITE

H&&S:WAVE | Hope&&Sauced
"""

import pytest
import json
from datetime import datetime


class TestNpcContext:
    """Tests for NpcContext dataclass."""

    def test_default_initialization(self):
        """Test default NpcContext initialization."""
        from bridges.saif_npc.saif_npc import NpcContext

        ctx = NpcContext()
        assert ctx.location == "unknown"
        assert ctx.mood == "neutral"
        assert ctx.inventory == []
        assert ctx.relationships == {}
        assert ctx.timestamp is not None

    def test_custom_initialization(self):
        """Test NpcContext with custom values."""
        from bridges.saif_npc.saif_npc import NpcContext

        ctx = NpcContext(
            location="tavern",
            mood="friendly",
            inventory=["ale", "bread"],
            relationships={"player": 0.8},
        )
        assert ctx.location == "tavern"
        assert ctx.mood == "friendly"
        assert len(ctx.inventory) == 2
        assert ctx.relationships["player"] == 0.8

    def test_to_dict(self):
        """Test NpcContext serialization."""
        from bridges.saif_npc.saif_npc import NpcContext

        ctx = NpcContext(location="market", mood="busy")
        data = ctx.to_dict()
        assert data["location"] == "market"
        assert data["mood"] == "busy"
        assert "timestamp" in data

    def test_from_dict(self):
        """Test NpcContext deserialization."""
        from bridges.saif_npc.saif_npc import NpcContext

        data = {
            "location": "forest",
            "mood": "cautious",
            "inventory": ["sword"],
            "relationships": {},
            "quest_state": {},
            "world_state": {},
        }
        ctx = NpcContext.from_dict(data)
        assert ctx.location == "forest"
        assert ctx.mood == "cautious"
        assert ctx.inventory == ["sword"]

    def test_to_state_string(self):
        """Test NpcContext to JSON string conversion."""
        from bridges.saif_npc.saif_npc import NpcContext

        ctx = NpcContext(location="castle")
        state_str = ctx.to_state_string()
        parsed = json.loads(state_str)
        assert parsed["location"] == "castle"


class TestNpcResponse:
    """Tests for NpcResponse dataclass."""

    def test_basic_response(self):
        """Test basic NpcResponse creation."""
        from bridges.saif_npc.saif_npc import NpcResponse

        resp = NpcResponse(response="Hello, traveler!")
        assert resp.response == "Hello, traveler!"
        assert resp.confidence == 0.8

    def test_response_with_metadata(self):
        """Test NpcResponse with full metadata."""
        from bridges.saif_npc.saif_npc import NpcResponse

        resp = NpcResponse(
            response="Welcome!",
            context_used="friendly merchant context",
            reasoning="Player greeted politely",
            confidence=0.95,
            suggested_actions=["offer_trade"],
            handoff_state="H&&S:SYNC",
        )
        assert resp.confidence == 0.95
        assert "offer_trade" in resp.suggested_actions
        assert resp.handoff_state == "H&&S:SYNC"

    def test_to_dict(self):
        """Test NpcResponse serialization."""
        from bridges.saif_npc.saif_npc import NpcResponse

        resp = NpcResponse(response="Test", suggested_actions=["action1"])
        data = resp.to_dict()
        assert data["response"] == "Test"
        assert "action1" in data["suggested_actions"]


class TestSaifNpc:
    """Tests for SaifNpc class."""

    def test_initialization(self):
        """Test SaifNpc initialization."""
        from bridges.saif_npc.saif_npc import SaifNpc

        npc = SaifNpc()
        assert npc._initialized is True
        assert npc.enable_handoff is True

    def test_custom_personality(self):
        """Test SaifNpc with custom personality."""
        from bridges.saif_npc.saif_npc import SaifNpc

        npc = SaifNpc(npc_personality="grumpy blacksmith")
        assert npc.npc_personality == "grumpy blacksmith"

    def test_forward_with_dict_state(self):
        """Test forward pass with dict state."""
        from bridges.saif_npc.saif_npc import SaifNpc

        npc = SaifNpc()
        state = {"location": "village", "mood": "helpful"}
        result = npc.forward(state=state, input="Hello!")

        assert result is not None
        assert result.response is not None
        assert result.handoff_state is not None

    def test_forward_with_context_state(self):
        """Test forward pass with NpcContext state."""
        from bridges.saif_npc.saif_npc import SaifNpc, NpcContext

        npc = SaifNpc()
        state = NpcContext(location="tavern", mood="cheerful")
        result = npc.forward(state=state, input="What's on the menu?")

        assert result is not None
        assert "H&&S:SYNC" in result.handoff_state

    def test_get_handoff_context(self):
        """Test handoff context generation."""
        from bridges.saif_npc.saif_npc import SaifNpc

        npc = SaifNpc(npc_personality="test_personality")
        handoff = npc.get_handoff_context()

        assert handoff["module"] == "SaifNpc"
        assert handoff["marker"] == "H&&S:WAVE"
        assert handoff["personality"] == "test_personality"

    def test_configure(self):
        """Test NPC configuration."""
        from bridges.saif_npc.saif_npc import SaifNpc

        npc = SaifNpc(temperature=0.5)
        assert npc.temperature == 0.5

        npc.configure(temperature=0.8)
        assert npc.temperature == 0.8

    def test_extract_suggested_actions_question(self):
        """Test action extraction for questions."""
        from bridges.saif_npc.saif_npc import SaifNpc

        npc = SaifNpc()
        actions = npc._extract_suggested_actions("Would you like to buy something?")
        assert "await_player_response" in actions

    def test_extract_suggested_actions_navigation(self):
        """Test action extraction for navigation hints."""
        from bridges.saif_npc.saif_npc import SaifNpc

        npc = SaifNpc()
        actions = npc._extract_suggested_actions("Go to the market to find it.")
        assert "provide_navigation_hint" in actions

    def test_extract_suggested_actions_quest(self):
        """Test action extraction for quest triggers."""
        from bridges.saif_npc.saif_npc import SaifNpc

        npc = SaifNpc()
        actions = npc._extract_suggested_actions("I need you to bring me some herbs.")
        assert "potential_quest_trigger" in actions


class TestNpcTrace:
    """Tests for NpcTrace dataclass."""

    def test_trace_creation(self):
        """Test NpcTrace creation."""
        from bridges.saif_npc.teleprompter import NpcTrace

        trace = NpcTrace(
            trace_id="test_001",
            state={"location": "village"},
            input="Hello",
            output="Greetings!",
        )
        assert trace.trace_id == "test_001"
        assert trace.score == 0.0
        assert trace.timestamp is not None

    def test_trace_serialization(self):
        """Test NpcTrace serialization."""
        from bridges.saif_npc.teleprompter import NpcTrace

        trace = NpcTrace(
            trace_id="test_002",
            state={"mood": "happy"},
            input="Hi",
            output="Hello!",
            score=0.85,
            provider="openai",
        )
        data = trace.to_dict()
        assert data["trace_id"] == "test_002"
        assert data["score"] == 0.85
        assert data["provider"] == "openai"

    def test_trace_from_dict(self):
        """Test NpcTrace deserialization."""
        from bridges.saif_npc.teleprompter import NpcTrace

        data = {
            "trace_id": "test_003",
            "state": {"location": "castle"},
            "input": "Test",
            "output": "Response",
            "context": "Built context",
            "score": 0.9,
            "provider": "anthropic",
        }
        trace = NpcTrace.from_dict(data)
        assert trace.trace_id == "test_003"
        assert trace.score == 0.9


class TestNpcTeleprompter:
    """Tests for NpcTeleprompter class."""

    def test_initialization(self):
        """Test teleprompter initialization."""
        from bridges.saif_npc.teleprompter import NpcTeleprompter

        tp = NpcTeleprompter()
        assert tp.max_traces == 1000
        assert tp.min_score_threshold == 0.7

    def test_add_trace(self):
        """Test adding traces."""
        from bridges.saif_npc.teleprompter import NpcTeleprompter

        tp = NpcTeleprompter()
        trace = tp.add_trace(
            trace_id="t1",
            state={"loc": "village"},
            input="Hello",
            output="Hi!",
            score=0.8,
        )
        assert len(tp.traces) == 1
        assert trace.trace_id == "t1"

    def test_get_high_quality_traces(self):
        """Test filtering high quality traces."""
        from bridges.saif_npc.teleprompter import NpcTeleprompter

        tp = NpcTeleprompter(min_score_threshold=0.7)
        tp.add_trace("t1", {}, "a", "b", score=0.5)  # Below threshold
        tp.add_trace("t2", {}, "c", "d", score=0.8)  # Above threshold
        tp.add_trace("t3", {}, "e", "f", score=0.9)  # Above threshold

        high_quality = tp.get_high_quality_traces()
        assert len(high_quality) == 2

    def test_get_traces_by_provider(self):
        """Test filtering traces by provider."""
        from bridges.saif_npc.teleprompter import NpcTeleprompter

        tp = NpcTeleprompter()
        tp.add_trace("t1", {}, "a", "b", provider="openai")
        tp.add_trace("t2", {}, "c", "d", provider="anthropic")
        tp.add_trace("t3", {}, "e", "f", provider="openai")

        openai_traces = tp.get_traces_by_provider("openai")
        assert len(openai_traces) == 2

    def test_calculate_provider_stats(self):
        """Test provider statistics calculation."""
        from bridges.saif_npc.teleprompter import NpcTeleprompter

        tp = NpcTeleprompter(providers=["openai", "anthropic"])
        tp.add_trace("t1", {}, "a", "b", score=0.8, provider="openai")
        tp.add_trace("t2", {}, "c", "d", score=0.9, provider="openai")

        stats = tp.calculate_provider_stats()
        assert stats["openai"]["count"] == 2
        assert abs(stats["openai"]["avg_score"] - 0.85) < 0.0001  # Float comparison
        assert stats["anthropic"]["count"] == 0


class TestNpcTraceDataset:
    """Tests for NpcTraceDataset class."""

    def test_initialization(self):
        """Test dataset initialization."""
        from bridges.saif_npc.finetuner import NpcTraceDataset

        dataset = NpcTraceDataset()
        assert len(dataset) == 0

    def test_add_example(self):
        """Test adding examples."""
        from bridges.saif_npc.finetuner import NpcTraceDataset

        dataset = NpcTraceDataset()
        example = dataset.add(
            state={"location": "shop"},
            input="What do you sell?",
            expected_output="Various goods!",
        )
        assert len(dataset) == 1
        assert example.input == "What do you sell?"

    def test_iteration(self):
        """Test dataset iteration."""
        from bridges.saif_npc.finetuner import NpcTraceDataset

        dataset = NpcTraceDataset()
        dataset.add({}, "in1", "out1")
        dataset.add({}, "in2", "out2")

        inputs = [e.input for e in dataset]
        assert "in1" in inputs
        assert "in2" in inputs

    def test_batching(self):
        """Test batch iteration."""
        from bridges.saif_npc.finetuner import NpcTraceDataset

        dataset = NpcTraceDataset()
        for i in range(5):
            dataset.add({}, f"in{i}", f"out{i}")

        batches = list(dataset.batches(batch_size=2))
        assert len(batches) == 3  # 2 + 2 + 1

    def test_filter_by_weight(self):
        """Test filtering by weight."""
        from bridges.saif_npc.finetuner import NpcTraceDataset

        dataset = NpcTraceDataset()
        dataset.add({}, "a", "b", weight=0.3)
        dataset.add({}, "c", "d", weight=0.8)
        dataset.add({}, "e", "f", weight=0.9)

        filtered = dataset.filter_by_weight(min_weight=0.5)
        assert len(filtered) == 2

    def test_filter_by_source(self):
        """Test filtering by source."""
        from bridges.saif_npc.finetuner import NpcTraceDataset

        dataset = NpcTraceDataset()
        dataset.add({}, "a", "b", source="manual")
        dataset.add({}, "c", "d", source="trace")
        dataset.add({}, "e", "f", source="manual")

        manual = dataset.filter_by_source("manual")
        assert len(manual) == 2


class TestBootstrapFinetuner:
    """Tests for BootstrapFinetuner class."""

    def test_initialization(self):
        """Test finetuner initialization."""
        from bridges.saif_npc.finetuner import BootstrapFinetuner, NpcTraceDataset

        dataset = NpcTraceDataset()
        finetuner = BootstrapFinetuner(dataset)
        assert finetuner.target_model == "claude-3-opus"
        assert finetuner.max_rounds == 5

    def test_default_metric(self):
        """Test default evaluation metric."""
        from bridges.saif_npc.finetuner import BootstrapFinetuner, NpcTraceDataset

        dataset = NpcTraceDataset()
        finetuner = BootstrapFinetuner(dataset)

        # Create mock example and prediction
        class MockExample:
            response = "Hello world"

        class MockPrediction:
            response = "Hello world"

        score = finetuner._default_metric(MockExample(), MockPrediction())
        assert score > 0  # Should have some overlap

    def test_generate_handoff_state(self):
        """Test handoff state generation."""
        from bridges.saif_npc.finetuner import BootstrapFinetuner, NpcTraceDataset

        dataset = NpcTraceDataset()
        dataset.add({}, "a", "b")
        finetuner = BootstrapFinetuner(dataset, target_model="test-model")

        handoff = finetuner.generate_handoff_state()
        assert "H&&S:PASS" in handoff
        assert "test-model" in handoff


# Integration test
class TestIntegration:
    """Integration tests for SAIF NPC workflow."""

    def test_full_workflow(self):
        """Test complete NPC workflow."""
        from bridges.saif_npc.saif_npc import SaifNpc, NpcContext
        from bridges.saif_npc.teleprompter import NpcTeleprompter
        from bridges.saif_npc.finetuner import BootstrapFinetuner, NpcTraceDataset

        # Create NPC
        npc = SaifNpc(npc_personality="helpful merchant")

        # Generate response
        state = NpcContext(location="shop", mood="friendly")
        response = npc.forward(state=state, input="What do you have?")
        assert response is not None

        # Create teleprompter and add trace
        tp = NpcTeleprompter()
        tp.add_trace(
            trace_id="int_test_001",
            state=state.to_dict(),
            input="What do you have?",
            output=response.response,
            score=0.8,
        )
        assert len(tp.traces) == 1

        # Create dataset from traces
        dataset = NpcTraceDataset()
        for trace in tp.traces:
            dataset.add_from_trace(trace.to_dict())
        assert len(dataset) == 1

        # Create finetuner
        finetuner = BootstrapFinetuner(dataset)
        handoff = finetuner.generate_handoff_state()
        assert "H&&S:PASS" in handoff


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
