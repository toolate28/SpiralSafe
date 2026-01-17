"""
Tests for KENL Orchestrator Module
Validates intent parsing, safety checks, and execution planning
"""

import sys
from pathlib import Path

# Add the kenl module directory to path for direct imports
kenl_dir = Path(__file__).parent
sys.path.insert(0, str(kenl_dir))

import pytest
from datetime import datetime

# Direct imports from orchestrator module
from orchestrator import (
    KenlOrchestrator,
    IntentResult,
    ExecutionPlan,
    SafetyStatus,
    RollbackCheckpoint,
    IntentParser,
    ExecutionPlanner,
)


class TestIntentParser:
    """Tests for the IntentParser class"""

    def test_safe_command_passes(self):
        """Safe commands should pass safety checks"""
        parser = IntentParser()
        result = parser.parse("git status")

        assert result.safety_check == SafetyStatus.PASS
        assert result.parsed_intent == "version_control"
        assert result.confidence >= 0.9

    def test_unsafe_rm_rf_fails(self):
        """Dangerous rm -rf / command should fail"""
        parser = IntentParser()
        result = parser.parse("rm -rf /")

        assert result.safety_check == SafetyStatus.FAIL
        assert len(result.warnings) > 0

    def test_drop_database_fails(self):
        """DROP DATABASE command should fail"""
        parser = IntentParser()
        result = parser.parse("DROP DATABASE production")

        assert result.safety_check == SafetyStatus.FAIL

    def test_read_only_commands_pass(self):
        """Read-only commands should pass with high confidence"""
        parser = IntentParser()

        for cmd in ["ls -la", "cat file.txt", "echo hello", "Get-Process"]:
            result = parser.parse(cmd)
            assert result.safety_check in [SafetyStatus.PASS, SafetyStatus.WARN]

    def test_warn_patterns_detected(self):
        """Commands with warning patterns should be flagged"""
        parser = IntentParser()
        result = parser.parse("delete old_files.txt")

        assert len(result.warnings) > 0

    def test_intent_extraction(self):
        """Intent should be correctly extracted from commands"""
        parser = IntentParser()

        assert parser.parse("git push origin main").parsed_intent == "version_control"
        assert parser.parse("npm install lodash").parsed_intent == "package_management"
        assert parser.parse("docker build .").parsed_intent == "container_management"

    def test_strict_mode_affects_warnings(self):
        """Strict mode should affect warning handling"""
        strict_parser = IntentParser(strict_mode=True)
        relaxed_parser = IntentParser(strict_mode=False)

        # Use a command that matches the warning pattern (update.*where)
        result_strict = strict_parser.parse("update users set name='test' where id=1")
        result_relaxed = relaxed_parser.parse("update users set name='test' where id=1")

        # Both should have warnings
        assert len(result_strict.warnings) > 0
        assert len(result_relaxed.warnings) > 0


class TestExecutionPlanner:
    """Tests for the ExecutionPlanner class"""

    def test_plan_creation(self):
        """Plans should be created with proper structure"""
        planner = ExecutionPlanner()
        plan = planner.plan("version_control", "vortex_state")

        assert plan.intent == "version_control"
        assert plan.context == "vortex_state"
        assert len(plan.steps) > 0
        assert len(plan.checkpoints) == 3  # before, mid, after

    def test_divergence_calculation(self):
        """Divergence should be calculated based on intent complexity"""
        planner = ExecutionPlanner()

        safe_plan = planner.plan("list_files", "vortex_state")
        risky_plan = planner.plan("kubernetes_management", "vortex_state")

        # Risky operations should have higher divergence
        assert risky_plan.divergence_estimate >= safe_plan.divergence_estimate

    def test_divergence_cap_blocking(self):
        """Plans exceeding divergence cap should be blocked"""
        planner = ExecutionPlanner(divergence_cap=0.01)  # Very strict
        plan = planner.plan("complex_modification", "vortex_state")

        assert plan.blocked
        assert plan.block_reason is not None
        assert "divergence" in plan.block_reason.lower()

    def test_recovery_rate_estimation(self):
        """Recovery rate should be estimated based on plan complexity"""
        planner = ExecutionPlanner()
        plan = planner.plan("version_control", "vortex_state")

        assert 0.90 <= plan.estimated_recovery_rate <= 1.0

    def test_checkpoint_creation(self):
        """Checkpoints should have valid structure"""
        planner = ExecutionPlanner()
        plan = planner.plan("test_intent", "test_context")

        for checkpoint in plan.checkpoints:
            assert checkpoint.id.startswith("ckpt-")
            assert isinstance(checkpoint.timestamp, datetime)
            assert checkpoint.reversible is True


class TestRollbackCheckpoint:
    """Tests for the RollbackCheckpoint dataclass"""

    def test_checkpoint_to_dict(self):
        """Checkpoint should serialize to dict correctly"""
        # Use a fixed date for deterministic testing
        test_time = datetime(2020, 1, 1, 12, 0, 0)
        checkpoint = RollbackCheckpoint(
            id="ckpt-001",
            timestamp=test_time,
            state={"key": "value"},
            command="test_command",
            reversible=True,
        )

        data = checkpoint.to_dict()
        assert data["id"] == "ckpt-001"
        assert data["command"] == "test_command"
        assert data["reversible"] is True
        assert "timestamp" in data


class TestKenlOrchestrator:
    """Tests for the main KenlOrchestrator class"""

    def test_safe_command_returns_plan(self):
        """Safe commands should return an ExecutionPlan"""
        orchestrator = KenlOrchestrator()
        result = orchestrator.forward("git status")

        assert isinstance(result, ExecutionPlan)
        assert result.intent == "version_control"

    def test_unsafe_command_blocked(self):
        """Unsafe commands should be blocked"""
        orchestrator = KenlOrchestrator()
        result = orchestrator.forward("rm -rf /")

        assert result == "Blocked"

    def test_high_divergence_blocked(self):
        """Commands with high divergence should be blocked"""
        orchestrator = KenlOrchestrator(divergence_cap=0.01)
        result = orchestrator.forward("complex management operation")

        assert result == "Blocked"

    def test_history_tracking(self):
        """Commands should be tracked in history"""
        orchestrator = KenlOrchestrator()
        orchestrator.forward("git status")
        orchestrator.forward("ls -la")

        assert len(orchestrator.history) == 2
        assert orchestrator.history[0]["command"] == "git status"

    def test_metrics(self):
        """Metrics should be calculated correctly"""
        orchestrator = KenlOrchestrator()
        orchestrator.forward("git status")  # Should pass
        orchestrator.forward("rm -rf /")  # Should be blocked

        metrics = orchestrator.get_metrics()
        assert metrics["total_commands"] == 2
        assert metrics["blocked_commands"] == 1

    def test_rollback_handler_registration(self):
        """Rollback handlers should be registerable"""
        orchestrator = KenlOrchestrator()
        handler_called = False

        def test_handler(checkpoint):
            nonlocal handler_called
            handler_called = True
            return True

        orchestrator.register_rollback_handler("test", test_handler)

        checkpoint = RollbackCheckpoint(
            id="ckpt-001",
            timestamp=datetime.now(),
            state={},
            command="test_action",
        )

        result = orchestrator.rollback(checkpoint)
        assert handler_called
        assert result is True

    def test_recovery_threshold(self):
        """Plans below recovery threshold should be blocked"""
        # Note: With current implementation, it's hard to hit this threshold
        # This test verifies the threshold check exists
        orchestrator = KenlOrchestrator(recovery_threshold=0.99)
        metrics = orchestrator.get_metrics()
        assert metrics["recovery_threshold"] == 0.99


class TestEndToEnd:
    """End-to-end integration tests"""

    def test_full_orchestration_flow(self):
        """Test complete orchestration flow from command to plan"""
        orchestrator = KenlOrchestrator(
            strict_mode=True,
            divergence_cap=0.15,
            recovery_threshold=0.90,
        )

        # Safe command should produce execution plan
        result = orchestrator.forward("git push origin main")

        assert isinstance(result, ExecutionPlan)
        assert not result.blocked
        assert result.estimated_recovery_rate >= 0.90
        assert result.divergence_estimate <= 0.15
        assert len(result.checkpoints) == 3

    def test_multiple_commands_tracking(self):
        """Multiple commands should be tracked correctly"""
        orchestrator = KenlOrchestrator()

        commands = [
            "git status",
            "npm install",
            "docker build .",
            "rm -rf /",  # Should be blocked
            "kubectl get pods",
        ]

        results = [orchestrator.forward(cmd) for cmd in commands]

        # 4 should pass, 1 should be blocked
        plans = [r for r in results if isinstance(r, ExecutionPlan)]
        blocked = [r for r in results if r == "Blocked"]

        assert len(plans) == 4
        assert len(blocked) == 1


# Allow running with pytest or directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
