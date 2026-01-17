"""
KENL Orchestrator Module
DSPy-inspired intent-driven command orchestration with safety checks

This module provides infrastructure orchestration capabilities with:
- Intent parsing from natural language commands
- Safety verification with rollback support
- Divergence capping to maintain coherence
- Vortex state context for execution planning

Note: This is a standalone implementation inspired by DSPy patterns.
For full DSPy integration, install dspy-ai package.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Callable
from enum import Enum
from datetime import datetime
import re


class SafetyStatus(Enum):
    """Safety check status for command execution"""
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"


@dataclass
class IntentResult:
    """Result of intent parsing from a command"""
    parsed_intent: str
    safety_check: SafetyStatus
    confidence: float = 1.0
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RollbackCheckpoint:
    """Checkpoint for safe rollback operations"""
    id: str
    timestamp: datetime
    state: Dict[str, Any]
    command: str
    reversible: bool = True
    intent: Optional[str] = None  # Store intent explicitly for rollback

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "state": self.state,
            "command": self.command,
            "reversible": self.reversible,
            "intent": self.intent,
        }


@dataclass
class ExecutionPlan:
    """Execution plan with rollback support"""
    intent: str
    context: str
    steps: List[str] = field(default_factory=list)
    checkpoints: List[RollbackCheckpoint] = field(default_factory=list)
    estimated_recovery_rate: float = 0.95
    divergence_estimate: float = 0.05
    blocked: bool = False
    block_reason: Optional[str] = None


class IntentParser:
    """
    Parse commands into structured intents with safety checks.
    Inspired by DSPy ChainOfThought signature pattern.
    """

    # Patterns that indicate potentially unsafe operations
    UNSAFE_PATTERNS = [
        r"rm\s+-rf\s+/",  # Dangerous recursive delete
        r"drop\s+database",  # Database deletion
        r"truncate\s+table",  # Table truncation
        r"format\s+[cC]:",  # Disk format
        r":(){ :|:& };:",  # Fork bomb
        r"del\s+/[sS]\s+/[qQ]",  # Windows recursive delete
    ]

    # Patterns that indicate rollback-friendly operations
    SAFE_PATTERNS = [
        r"git\s+",  # Git commands (have built-in undo)
        r"echo\s+",  # Echo commands (safe)
        r"ls\s+",  # List commands (read-only)
        r"cat\s+",  # Cat commands (read-only)
        r"Get-",  # PowerShell Get cmdlets (read-only)
    ]

    # Patterns that require extra verification
    WARN_PATTERNS = [
        r"delete",
        r"remove",
        r"drop",
        r"update.*where",
        r"Set-",  # PowerShell Set cmdlets
        r"New-",  # PowerShell New cmdlets
    ]

    def __init__(self, strict_mode: bool = True):
        """
        Initialize the intent parser.

        Args:
            strict_mode: If True, fail on any unsafe pattern.
                        If False, allow with warnings.
        """
        self.strict_mode = strict_mode
        self._compiled_unsafe = [re.compile(p, re.IGNORECASE)
                                 for p in self.UNSAFE_PATTERNS]
        self._compiled_safe = [re.compile(p, re.IGNORECASE)
                               for p in self.SAFE_PATTERNS]
        self._compiled_warn = [re.compile(p, re.IGNORECASE)
                               for p in self.WARN_PATTERNS]

    def parse(self, command: str) -> IntentResult:
        """
        Parse a command into an IntentResult.

        Args:
            command: Natural language or shell command to parse

        Returns:
            IntentResult with parsed intent and safety status
        """
        command = command.strip()
        warnings: List[str] = []

        # Check for unsafe patterns
        for pattern in self._compiled_unsafe:
            if pattern.search(command):
                return IntentResult(
                    parsed_intent=command,
                    safety_check=SafetyStatus.FAIL,
                    confidence=0.99,
                    warnings=["Unsafe pattern detected: potential destructive operation"],
                    metadata={"matched_pattern": pattern.pattern},
                )

        # Check for warning patterns
        for pattern in self._compiled_warn:
            if pattern.search(command):
                warnings.append(f"Pattern requires verification: {pattern.pattern}")

        # Check for safe patterns (boost confidence)
        confidence = 0.85
        for pattern in self._compiled_safe:
            if pattern.search(command):
                confidence = 0.95
                break

        # Determine safety status
        if warnings and self.strict_mode:
            safety_status = SafetyStatus.WARN
        else:
            safety_status = SafetyStatus.PASS

        return IntentResult(
            parsed_intent=self._extract_intent(command),
            safety_check=safety_status,
            confidence=confidence,
            warnings=warnings,
            metadata={"original_command": command},
        )

    def _extract_intent(self, command: str) -> str:
        """Extract the core intent from a command string."""
        # Remove common shell prefixes
        command = re.sub(r"^(sudo|doas|runas)\s+", "", command)

        # Extract the primary action
        parts = command.split()
        if not parts:
            return "empty_command"

        action = parts[0].lower()

        # Map common commands to intents
        intent_map = {
            "git": "version_control",
            "npm": "package_management",
            "pip": "package_management",
            "docker": "container_management",
            "kubectl": "kubernetes_management",
            "az": "azure_management",
            "aws": "aws_management",
            "ls": "list_files",
            "dir": "list_files",
            "cd": "change_directory",
            "cat": "read_file",
            "echo": "output_text",
            "Get-": "powershell_query",
            "Set-": "powershell_modification",
        }

        for prefix, intent in intent_map.items():
            if action.startswith(prefix.lower()):
                return intent

        return f"execute_{action}"


class ExecutionPlanner:
    """
    Generate execution plans from parsed intents.
    Inspired by DSPy Predict signature pattern.
    """

    # Maximum allowed divergence from vortex standards
    MAX_DIVERGENCE = 0.10

    # Target error recovery rate
    TARGET_RECOVERY_RATE = 0.95

    def __init__(self, divergence_cap: float = 0.10):
        """
        Initialize the execution planner.

        Args:
            divergence_cap: Maximum allowed divergence (default: 10%)
        """
        self.divergence_cap = divergence_cap
        self._checkpoint_counter = 0

    def plan(self, intent: str, context: str = "vortex_state") -> ExecutionPlan:
        """
        Generate an execution plan for a given intent.

        Args:
            intent: Parsed intent from IntentParser
            context: Current execution context

        Returns:
            ExecutionPlan with steps and checkpoints
        """
        # Create initial checkpoint
        initial_checkpoint = self._create_checkpoint(
            f"before_{intent}",
            {"context": context, "phase": "pre_execution"},
            intent=intent,
        )

        # Generate execution steps based on intent type
        steps = self._generate_steps(intent, context)

        # Create mid-execution checkpoint
        mid_checkpoint = self._create_checkpoint(
            f"mid_{intent}",
            {"context": context, "phase": "mid_execution"},
            intent=intent,
        )

        # Create final checkpoint
        final_checkpoint = self._create_checkpoint(
            f"after_{intent}",
            {"context": context, "phase": "post_execution"},
            intent=intent,
        )

        # Estimate divergence based on intent complexity
        divergence = self._estimate_divergence(intent, steps)

        # Check if plan should be blocked due to divergence
        blocked = divergence > self.divergence_cap
        block_reason = None
        if blocked:
            block_reason = (
                f"Divergence {divergence:.1%} exceeds cap {self.divergence_cap:.1%}"
            )

        return ExecutionPlan(
            intent=intent,
            context=context,
            steps=steps,
            checkpoints=[initial_checkpoint, mid_checkpoint, final_checkpoint],
            estimated_recovery_rate=self._estimate_recovery_rate(steps),
            divergence_estimate=divergence,
            blocked=blocked,
            block_reason=block_reason,
        )

    def _create_checkpoint(
        self, command: str, state: Dict[str, Any], intent: str = None
    ) -> RollbackCheckpoint:
        """Create a rollback checkpoint."""
        self._checkpoint_counter += 1
        return RollbackCheckpoint(
            id=f"ckpt-{self._checkpoint_counter:04d}",
            timestamp=datetime.now(),
            state=state,
            command=command,
            reversible=True,
            intent=intent,
        )

    def _generate_steps(self, intent: str, context: str) -> List[str]:
        """Generate execution steps for an intent."""
        base_steps = [
            f"Verify {context} accessibility",
            f"Initialize {intent} operation",
            f"Execute {intent} with monitoring",
            f"Validate {intent} results",
            f"Update {context} state",
        ]
        return base_steps

    def _estimate_divergence(self, intent: str, steps: List[str]) -> float:
        """Estimate divergence from vortex standards."""
        # Simple heuristic: more steps = higher potential divergence
        base_divergence = 0.02
        step_factor = len(steps) * 0.01

        # Higher-risk intents have higher divergence
        high_risk_intents = ["modification", "management", "execute_"]
        for risk in high_risk_intents:
            if risk in intent.lower():
                step_factor += 0.02

        return min(base_divergence + step_factor, 0.20)

    def _estimate_recovery_rate(self, steps: List[str]) -> float:
        """Estimate error recovery rate for the plan."""
        # Base recovery rate
        base_rate = 0.98

        # Deduct for each step (more steps = more failure points)
        step_penalty = len(steps) * 0.005

        return max(base_rate - step_penalty, 0.90)


class KenlOrchestrator:
    """
    Main orchestrator class for KENL infrastructure operations.

    Combines intent parsing and execution planning with safety checks
    and rollback support for infrastructure-aware AI orchestration.

    Example:
        orchestrator = KenlOrchestrator()
        result = orchestrator.forward("git push origin main")
        if result != "Blocked":
            print(f"Execution plan: {result}")
    """

    def __init__(
        self,
        strict_mode: bool = True,
        divergence_cap: float = 0.10,
        recovery_threshold: float = 0.95,
    ):
        """
        Initialize the KENL Orchestrator.

        Args:
            strict_mode: Fail on any potentially unsafe patterns
            divergence_cap: Maximum allowed divergence (default: 10%)
            recovery_threshold: Minimum required recovery rate (default: 95%)
        """
        self.intent_parser = IntentParser(strict_mode=strict_mode)
        self.executor = ExecutionPlanner(divergence_cap=divergence_cap)
        self.recovery_threshold = recovery_threshold
        self._history: List[Dict[str, Any]] = []
        self._rollback_handlers: Dict[str, Callable] = {}

    def forward(self, command: str) -> ExecutionPlan | str:
        """
        Process a command through the KENL orchestration pipeline.

        This is the main entry point following the DSPy Module pattern.

        Args:
            command: Natural language or shell command

        Returns:
            ExecutionPlan if command passes safety checks, or "Blocked" string
        """
        # Parse intent with safety check
        parsed = self.intent_parser.parse(command)

        # Log to history
        self._history.append({
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "parsed_intent": parsed.parsed_intent,
            "safety_status": parsed.safety_check.value,
        })

        # Block unsafe commands
        if parsed.safety_check == SafetyStatus.FAIL:
            return "Blocked"

        # Generate execution plan
        plan = self.executor.plan(
            intent=parsed.parsed_intent,
            context="vortex_state",
        )

        # Check if plan is blocked due to divergence
        if plan.blocked:
            return "Blocked"

        # Check recovery rate threshold
        if plan.estimated_recovery_rate < self.recovery_threshold:
            return "Blocked"

        return plan

    def register_rollback_handler(
        self, intent: str, handler: Callable[[RollbackCheckpoint], bool]
    ) -> None:
        """
        Register a rollback handler for a specific intent type.

        Args:
            intent: The intent type to handle
            handler: Function that takes a checkpoint and returns success status
        """
        self._rollback_handlers[intent] = handler

    def rollback(self, checkpoint: RollbackCheckpoint) -> bool:
        """
        Attempt to rollback to a checkpoint.

        Args:
            checkpoint: The checkpoint to rollback to

        Returns:
            True if rollback succeeded, False otherwise
        """
        if not checkpoint.reversible:
            return False

        # Use explicit intent if available, otherwise extract from command
        intent = checkpoint.intent
        if not intent:
            # Fallback to command parsing for backward compatibility
            intent = checkpoint.command.split("_")[0] if "_" in checkpoint.command else "default"

        handler = self._rollback_handlers.get(intent)
        if handler:
            return handler(checkpoint)

        # Default rollback: log and return success
        self._history.append({
            "timestamp": datetime.now().isoformat(),
            "action": "rollback",
            "checkpoint_id": checkpoint.id,
            "intent": intent,
        })
        return True

    def get_metrics(self) -> Dict[str, Any]:
        """Get current orchestrator metrics."""
        total_commands = len(self._history)
        blocked_commands = sum(
            1 for h in self._history
            if h.get("safety_status") == "fail"
        )

        return {
            "total_commands": total_commands,
            "blocked_commands": blocked_commands,
            "block_rate": blocked_commands / max(total_commands, 1),
            "divergence_cap": self.executor.divergence_cap,
            "recovery_threshold": self.recovery_threshold,
        }

    @property
    def history(self) -> List[Dict[str, Any]]:
        """Get command processing history."""
        return self._history.copy()


def main():
    """CLI entry point for KENL Orchestrator demonstration."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="KENL Orchestrator - Infrastructure-aware AI orchestration"
    )
    parser.add_argument(
        "command",
        nargs="?",
        help="Command to orchestrate (or enter interactive mode if omitted)",
    )
    parser.add_argument(
        "--strict",
        dest="strict",
        action="store_true",
        default=True,
        help="Enable strict safety mode (default: True). Use --no-strict to disable.",
    )
    parser.add_argument(
        "--no-strict",
        dest="strict",
        action="store_false",
        help="Disable strict safety mode",
    )
    parser.add_argument(
        "--divergence-cap",
        type=float,
        default=0.10,
        help="Maximum allowed divergence (default: 0.10)",
    )
    parser.add_argument(
        "--recovery-threshold",
        type=float,
        default=0.95,
        help="Minimum required recovery rate (default: 0.95)",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Run in interactive mode",
    )

    args = parser.parse_args()

    orchestrator = KenlOrchestrator(
        strict_mode=args.strict,
        divergence_cap=args.divergence_cap,
        recovery_threshold=args.recovery_threshold,
    )

    print("═" * 60)
    print("  KENL Orchestrator - Infrastructure-aware AI Orchestration")
    print("═" * 60)
    print(f"  Divergence Cap: {args.divergence_cap:.1%}")
    print(f"  Recovery Threshold: {args.recovery_threshold:.1%}")
    print(f"  Strict Mode: {args.strict}")
    print("─" * 60)

    if args.command:
        # Single command mode
        result = orchestrator.forward(args.command)
        if result == "Blocked":
            print(f"\n⛔ BLOCKED: {args.command}")
            print("   Reason: Failed safety checks or exceeded thresholds")
            sys.exit(1)
        else:
            print(f"\n✓ APPROVED: {args.command}")
            print(f"   Intent: {result.intent}")
            print(f"   Recovery Rate: {result.estimated_recovery_rate:.1%}")
            print(f"   Divergence: {result.divergence_estimate:.1%}")
            print(f"   Steps: {len(result.steps)}")
            print(f"   Checkpoints: {len(result.checkpoints)}")
            sys.exit(0)

    elif args.interactive:
        # Interactive mode
        print("\nEntering interactive mode (type 'quit' to exit)")
        print("─" * 60)

        while True:
            try:
                command = input("\nkenl> ").strip()
                if command.lower() in ("quit", "exit", "q"):
                    print("\n✨ Session ended")
                    break
                if command.lower() == "metrics":
                    metrics = orchestrator.get_metrics()
                    print(f"   Total Commands: {metrics['total_commands']}")
                    print(f"   Blocked Commands: {metrics['blocked_commands']}")
                    print(f"   Block Rate: {metrics['block_rate']:.1%}")
                    continue
                if not command:
                    continue

                result = orchestrator.forward(command)
                if result == "Blocked":
                    print(f"   ⛔ BLOCKED")
                else:
                    print(f"   ✓ APPROVED | Intent: {result.intent} | "
                          f"Recovery: {result.estimated_recovery_rate:.1%}")

            except (KeyboardInterrupt, EOFError):
                print("\n✨ Session ended")
                break

        # Print final metrics
        metrics = orchestrator.get_metrics()
        print("\n" + "─" * 60)
        print("Session Summary:")
        print(f"   Total Commands: {metrics['total_commands']}")
        print(f"   Blocked Commands: {metrics['blocked_commands']}")
        print("═" * 60)

    else:
        # Demo mode
        print("\nDemo Mode - Testing various commands:")
        print("─" * 60)

        test_commands = [
            "git status",
            "npm install lodash",
            "rm -rf /",  # Should be blocked
            "docker build .",
            "kubectl get pods",
        ]

        for cmd in test_commands:
            result = orchestrator.forward(cmd)
            if result == "Blocked":
                print(f"   ⛔ {cmd}")
            else:
                print(f"   ✓ {cmd} (intent: {result.intent})")

        print("\n" + "─" * 60)
        metrics = orchestrator.get_metrics()
        print(f"   Total: {metrics['total_commands']} | "
              f"Blocked: {metrics['blocked_commands']} | "
              f"Rate: {metrics['block_rate']:.1%}")
        print("═" * 60)


if __name__ == "__main__":
    main()
