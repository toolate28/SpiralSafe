#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                         SPIRAL VERIFIER                                      ║
║                                                                              ║
║        DSPy-Inspired Constraint Verification for SpiralSafe                  ║
║                                                                              ║
║                      SPIRAL Phase (70% Coherence)                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

This module implements the SpiralVerifier pattern for constraint-based validation
of outputs against SpiralSafe's architectural principles.

The SPIRAL phase unifies:
- Foundation constraints (isomorphism principle)
- Interface contracts (AWI, dual-format)
- Methodology patterns (ATOM, SAIF, Day Zero)
- Protocol compliance (Wave coherence, Bump handoffs)

Key components:
1. ConstraintChecker: RAG-style retrieval + verification
2. CoherenceAnalyzer: Wave protocol integration
3. EntropyMonitor: COPRO-style pre/post optimization tracking
4. TeleprompterBase: GEPA annealing pattern

Author: Hope&&Sauced
Date: 2026-01-17
Protocol: H&&S:WAVE
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable, Tuple
import json
import math
from datetime import datetime
import random
import re


# =============================================================================
# CONFIGURATION CONSTANTS
# =============================================================================

# Dual-format constraint: minimum words for prose content
DUAL_FORMAT_MIN_WORDS = 50

# Coherence calculation: multiplier for repetition ratio in curl computation
CURL_REPETITION_MULTIPLIER = 1.5


# =============================================================================
# CORE DATA STRUCTURES
# =============================================================================

@dataclass
class Constraint:
    """A verifiable constraint from the SpiralSafe architecture."""
    
    name: str
    description: str
    source: str  # e.g., "foundation/isomorphism-principle.md"
    check_fn: Optional[Callable[[Any], bool]] = None
    severity: str = "warning"  # "warning" | "error" | "critical"
    
    def verify(self, content: Any) -> bool:
        """Verify content against this constraint."""
        if self.check_fn:
            return self.check_fn(content)
        return True


@dataclass
class VerificationResult:
    """Result of constraint verification."""
    
    constraint_name: str
    passed: bool
    message: str
    severity: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CoherenceMetrics:
    """Wave protocol coherence metrics."""
    
    curl: float  # Circular reasoning indicator
    divergence: float  # Unresolved expansion indicator
    potential: float  # Development opportunity indicator
    coherence_score: float  # Overall coherence (0-1)
    regions: List[Dict[str, Any]] = field(default_factory=list)
    
    @property
    def is_coherent(self) -> bool:
        """Check if metrics meet SPIRAL 70% threshold."""
        return self.coherence_score >= 0.70


@dataclass
class EntropyComparison:
    """COPRO-style pre/post optimization comparison."""
    
    pre_entropy: float
    post_entropy: float
    differential: float
    within_threshold: bool
    
    @classmethod
    def compute(cls, pre_metrics: CoherenceMetrics, 
                post_metrics: CoherenceMetrics,
                threshold: float = 0.05) -> "EntropyComparison":
        """Compute entropy differential between pre and post states."""
        # Entropy approximation from coherence metrics
        pre_entropy = (pre_metrics.curl + abs(pre_metrics.divergence)) / 2
        post_entropy = (post_metrics.curl + abs(post_metrics.divergence)) / 2
        differential = abs(post_entropy - pre_entropy)
        
        return cls(
            pre_entropy=pre_entropy,
            post_entropy=post_entropy,
            differential=differential,
            within_threshold=differential < threshold
        )


# =============================================================================
# CONSTRAINT CHECKER (RAG-STYLE)
# =============================================================================

class ConstraintChecker:
    """
    RAG-style constraint checker that retrieves relevant constraints
    and verifies outputs against them.
    
    Pattern: query -> retrieve constraints -> verify -> verified_output
    """
    
    def __init__(self, constraints: Optional[List[Constraint]] = None):
        self.constraints = constraints or self._load_default_constraints()
        self.verification_history: List[VerificationResult] = []
    
    def _load_default_constraints(self) -> List[Constraint]:
        """Load default SpiralSafe constraints."""
        return [
            Constraint(
                name="dual_format",
                description="Content should serve both humans and agents",
                source="protocol/wave-spec.md",
                check_fn=self._check_dual_format,
                severity="warning"
            ),
            Constraint(
                name="coherence_threshold",
                description="Coherence score must meet 70% threshold",
                source="methodology/spiral-phase.md",
                check_fn=self._check_coherence,
                severity="error"
            ),
            Constraint(
                name="structure_preservation",
                description="Topological structure must be preserved",
                source="foundation/isomorphism-principle.md",
                check_fn=self._check_structure,
                severity="critical"
            ),
            Constraint(
                name="handoff_markers",
                description="Proper H&&S bump markers for handoffs",
                source="protocol/bump-spec.md",
                check_fn=self._check_handoff_markers,
                severity="warning"
            ),
        ]
    
    def _check_dual_format(self, content: Any) -> bool:
        """Check if content has both prose and structure."""
        if isinstance(content, str):
            has_prose = len(content.split()) > DUAL_FORMAT_MIN_WORDS
            has_structure = any(marker in content for marker in 
                              ["```", "| ", "- ", "1. ", "#"])
            return has_prose and has_structure
        return True
    
    def _check_coherence(self, content: Any) -> bool:
        """Check coherence against threshold."""
        if isinstance(content, CoherenceMetrics):
            return content.is_coherent
        return True
    
    def _check_structure(self, content: Any) -> bool:
        """Check that structure is preserved (simplified check)."""
        if isinstance(content, str):
            # Check for balanced structure indicators
            open_count = content.count("{") + content.count("[") + content.count("(")
            close_count = content.count("}") + content.count("]") + content.count(")")
            return open_count == close_count
        return True
    
    def _check_handoff_markers(self, content: Any) -> bool:
        """Check for proper H&&S markers when handoffs are present."""
        if isinstance(content, str):
            has_handoff_context = any(word in content.lower() for word in 
                                     ["handoff", "review", "pass to"])
            if has_handoff_context:
                return "H&&S:" in content
            return True
        return True
    
    def retrieve_relevant(self, query: str) -> List[Constraint]:
        """Retrieve constraints relevant to the query."""
        # Simple keyword matching for constraint retrieval
        relevant = []
        query_lower = query.lower()
        
        for constraint in self.constraints:
            keywords = constraint.name.split("_") + constraint.description.lower().split()
            if any(kw in query_lower for kw in keywords):
                relevant.append(constraint)
        
        # If no specific match, return all constraints
        return relevant if relevant else self.constraints
    
    def verify(self, query: str, content: Any) -> List[VerificationResult]:
        """
        Verify content against constraints relevant to the query.
        
        Args:
            query: Description of what is being verified
            content: The content to verify
            
        Returns:
            List of verification results
        """
        constraints = self.retrieve_relevant(query)
        results = []
        
        for constraint in constraints:
            passed = constraint.verify(content)
            result = VerificationResult(
                constraint_name=constraint.name,
                passed=passed,
                message=f"{'Passed' if passed else 'Failed'}: {constraint.description}",
                severity=constraint.severity if not passed else "info",
                details={
                    "source": constraint.source,
                    "query": query
                }
            )
            results.append(result)
            self.verification_history.append(result)
        
        return results


# =============================================================================
# COHERENCE ANALYZER (WAVE PROTOCOL)
# =============================================================================

class CoherenceAnalyzer:
    """
    Analyzer for Wave protocol coherence metrics.
    
    Computes curl, divergence, and potential from text content.
    """
    
    def __init__(self, thresholds: Optional[Dict[str, float]] = None):
        self.thresholds = thresholds or {
            "curl_warning": 0.3,
            "curl_critical": 0.6,
            "divergence_warning": 0.4,
            "divergence_critical": 0.7,
        }
    
    def analyze(self, content: str) -> CoherenceMetrics:
        """
        Analyze content for coherence metrics.
        
        Args:
            content: Text content to analyze
            
        Returns:
            CoherenceMetrics with curl, divergence, potential scores
        """
        paragraphs = content.split("\n\n")
        
        curl = self._compute_curl(paragraphs)
        divergence = self._compute_divergence(paragraphs)
        potential = self._compute_potential(paragraphs)
        
        # Coherence is inverse of problematic indicators
        coherence_score = 1.0 - (curl + abs(divergence)) / 2
        coherence_score = max(0.0, min(1.0, coherence_score))
        
        regions = self._identify_regions(content, curl, divergence)
        
        return CoherenceMetrics(
            curl=curl,
            divergence=divergence,
            potential=potential,
            coherence_score=coherence_score,
            regions=regions
        )
    
    def _compute_curl(self, paragraphs: List[str]) -> float:
        """Detect circular/repetitive patterns."""
        if not paragraphs:
            return 0.0
        
        # Extract significant phrases
        phrases = []
        for p in paragraphs:
            sentences = re.split(r'[.!?]+', p.lower())
            phrases.extend([s.strip() for s in sentences if len(s.strip()) > 20])
        
        if not phrases:
            return 0.0
        
        unique = set(phrases)
        repetition_ratio = 1 - (len(unique) / len(phrases))
        
        return min(repetition_ratio * CURL_REPETITION_MULTIPLIER, 1.0)
    
    def _compute_divergence(self, paragraphs: List[str]) -> float:
        """
        Detect divergence (expansion/compression) in content.
        
        Per Wave protocol spec:
        - Positive divergence: unresolved expansion, scope creep
        - Negative divergence: premature closure, over-compression
        """
        text = " ".join(paragraphs)
        word_count = len(text.split())
        
        # Check for concluding markers
        conclusion_markers = [
            "therefore", "thus", "in conclusion", "finally",
            "to summarize", "in summary", "consequently"
        ]
        has_conclusion = any(marker in text.lower() for marker in conclusion_markers)
        
        # Check for premature closure indicators (negative divergence)
        premature_closure_markers = [
            "obviously", "clearly", "simply put", "needless to say",
            "as everyone knows", "it goes without saying"
        ]
        has_premature_closure = any(marker in text.lower() for marker in premature_closure_markers)
        
        # Count open questions/topics (positive divergence indicators)
        question_count = text.count("?")
        todo_count = len(re.findall(r'\bTODO\b|\bTBD\b|\bFIXME\b', text, re.IGNORECASE))
        
        # Calculate positive divergence (unresolved expansion)
        positive_indicators = (question_count * 0.05) + (todo_count * 0.1)
        if not has_conclusion:
            positive_indicators += 0.2
        
        # Calculate negative divergence (premature closure, over-compression)
        negative_indicators = 0.0
        if has_premature_closure:
            negative_indicators += 0.3
        # Short content with conclusions may indicate over-compression
        if has_conclusion and word_count < 100:
            negative_indicators += 0.2
        # High conclusion-to-content ratio suggests over-compression
        conclusion_count = sum(1 for m in conclusion_markers if m in text.lower())
        if conclusion_count > 1 and word_count < 200:
            negative_indicators += 0.2
        
        # Net divergence: positive - negative (can be negative)
        divergence = positive_indicators - negative_indicators
        
        # Clamp to [-1.0, 1.0] range
        return max(-1.0, min(divergence, 1.0))
    
    def _compute_potential(self, paragraphs: List[str]) -> float:
        """Detect development opportunities."""
        text = " ".join(paragraphs)
        
        potential_markers = [
            "could", "might", "perhaps", "possibly",
            "future work", "next steps", "potential"
        ]
        
        count = sum(1 for marker in potential_markers if marker in text.lower())
        return min(count * 0.15, 1.0)
    
    def _identify_regions(self, content: str, curl: float, 
                         divergence: float) -> List[Dict[str, Any]]:
        """Identify problematic regions in content."""
        regions = []
        
        if curl > self.thresholds["curl_warning"]:
            regions.append({
                "type": "high_curl",
                "severity": "critical" if curl > self.thresholds["curl_critical"] else "warning",
                "description": "Circular or repetitive patterns detected"
            })
        
        if divergence > self.thresholds["divergence_warning"]:
            regions.append({
                "type": "positive_divergence",
                "severity": "critical" if divergence > self.thresholds["divergence_critical"] else "warning",
                "description": "Unresolved expansion detected"
            })
        
        return regions


# =============================================================================
# TELEPROMPTER BASE (GEPA PATTERN)
# =============================================================================

class TeleprompterBase(ABC):
    """
    Base class for teleprompter optimization patterns.
    
    Implements GEPA (Gradient-free Evolutionary Prompt Annealing) pattern.
    """
    
    def __init__(self, target_coherence: float = 0.70):
        self.target_coherence = target_coherence
        self.optimization_history: List[Dict[str, Any]] = []
    
    @abstractmethod
    def mutate(self, prompt: str) -> str:
        """Mutate a prompt for exploration."""
        pass
    
    @abstractmethod
    def evaluate(self, prompt: str, traces: List[Dict]) -> float:
        """Evaluate prompt fitness against traces."""
        pass
    
    def anneal(self, initial_prompt: str, traces: List[Dict],
               iterations: int = 10, temperature: float = 1.0,
               cooling_rate: float = 0.9) -> Tuple[str, float]:
        """
        Anneal prompt toward optimal configuration.
        
        Args:
            initial_prompt: Starting prompt
            traces: Execution traces for evaluation
            iterations: Number of annealing iterations
            temperature: Initial temperature
            cooling_rate: Temperature decay rate
            
        Returns:
            Tuple of (optimized_prompt, final_score)
        """
        current_prompt = initial_prompt
        current_score = self.evaluate(current_prompt, traces)
        best_prompt = current_prompt
        best_score = current_score
        
        for i in range(iterations):
            # Generate candidate via mutation
            candidate = self.mutate(current_prompt)
            candidate_score = self.evaluate(candidate, traces)
            
            # Acceptance criteria (simulated annealing)
            delta = candidate_score - current_score
            if delta > 0 or random.random() < math.exp(delta / temperature):
                current_prompt = candidate
                current_score = candidate_score
                
                if current_score > best_score:
                    best_prompt = current_prompt
                    best_score = current_score
            
            # Cool down
            temperature *= cooling_rate
            
            # Record history
            self.optimization_history.append({
                "iteration": i,
                "temperature": temperature,
                "current_score": current_score,
                "best_score": best_score
            })
            
            # Early termination if target reached
            if best_score >= self.target_coherence:
                break
        
        return best_prompt, best_score


class GEPATeleprompter(TeleprompterBase):
    """
    GEPA implementation for SpiralSafe prompt optimization.
    
    Anneals on Jupyter traces and CI/CD execution logs.
    """
    
    def __init__(self, target_coherence: float = 0.70):
        super().__init__(target_coherence)
        self.analyzer = CoherenceAnalyzer()
    
    def mutate(self, prompt: str) -> str:
        """Mutate prompt by adjusting structure and constraints."""
        mutations = [
            self._add_constraint_reminder,
            self._simplify_structure,
            self._add_verification_step,
            self._reorder_sections
        ]
        
        mutation = random.choice(mutations)
        return mutation(prompt)
    
    def _add_constraint_reminder(self, prompt: str) -> str:
        """Add constraint verification reminder."""
        reminder = "\n\nRemember to verify constraints before finalizing."
        return prompt + reminder if reminder not in prompt else prompt
    
    def _simplify_structure(self, prompt: str) -> str:
        """Simplify complex nested structures."""
        # Remove excessive bullet nesting
        return re.sub(r'(\s{4,})-', '  -', prompt)
    
    def _add_verification_step(self, prompt: str) -> str:
        """Add explicit verification step."""
        if "verify" not in prompt.lower():
            return prompt + "\n\nStep: Verify output against SpiralSafe constraints."
        return prompt
    
    def _reorder_sections(self, prompt: str) -> str:
        """Reorder sections for better flow."""
        # Simple reordering: move questions to end
        lines = prompt.split("\n")
        questions = [l for l in lines if "?" in l]
        non_questions = [l for l in lines if "?" not in l]
        return "\n".join(non_questions + questions)
    
    def evaluate(self, prompt: str, traces: List[Dict]) -> float:
        """Evaluate prompt fitness based on trace coherence."""
        if not traces:
            return self.analyzer.analyze(prompt).coherence_score
        
        scores = []
        for trace in traces:
            if "output" in trace:
                metrics = self.analyzer.analyze(str(trace["output"]))
                scores.append(metrics.coherence_score)
        
        return sum(scores) / len(scores) if scores else 0.5


# =============================================================================
# SPIRAL VERIFIER MODULE (DSPy-STYLE)
# =============================================================================

class SpiralVerifier:
    """
    Main SpiralVerifier module implementing DSPy-style verification.
    
    Pattern: query -> retrieve constraints -> verify -> verified_output
    
    Achieves SPIRAL phase 70% coherence target through:
    - Constraint retrieval and verification
    - Wave protocol coherence analysis
    - COPRO entropy comparison
    - GEPA prompt optimization
    """
    
    def __init__(self, target_coherence: float = 0.70,
                 entropy_threshold: float = 0.05):
        self.constraint_checker = ConstraintChecker()
        self.coherence_analyzer = CoherenceAnalyzer()
        self.teleprompter = GEPATeleprompter(target_coherence)
        self.target_coherence = target_coherence
        self.entropy_threshold = entropy_threshold
    
    def forward(self, query: str, content: Optional[str] = None) -> Dict[str, Any]:
        """
        Forward pass: verify query/content against SpiralSafe constraints.
        
        Args:
            query: The verification query or content description
            content: Optional content to verify (uses query if not provided)
            
        Returns:
            Verified output with coherence metrics and constraint results
        """
        content = content or query
        
        # Analyze coherence
        metrics = self.coherence_analyzer.analyze(content)
        
        # Verify constraints
        verification_results = self.constraint_checker.verify(query, content)
        verification_results.append(
            VerificationResult(
                constraint_name="coherence_metrics",
                passed=metrics.is_coherent,
                message=f"Coherence: {metrics.coherence_score:.2%}",
                severity="error" if not metrics.is_coherent else "info",
                details={"metrics": {
                    "curl": metrics.curl,
                    "divergence": metrics.divergence,
                    "potential": metrics.potential,
                    "coherence_score": metrics.coherence_score
                }}
            )
        )
        
        # Compile results
        all_passed = all(r.passed for r in verification_results)
        critical_failures = [r for r in verification_results 
                           if not r.passed and r.severity == "critical"]
        
        return {
            "verified": all_passed,
            "coherence_score": metrics.coherence_score,
            "meets_threshold": metrics.is_coherent,
            "results": [
                {
                    "constraint": r.constraint_name,
                    "passed": r.passed,
                    "message": r.message,
                    "severity": r.severity
                }
                for r in verification_results
            ],
            "critical_failures": len(critical_failures),
            "timestamp": datetime.now().isoformat()
        }
    
    def optimize(self, query: str, traces: Optional[List[Dict]] = None,
                 iterations: int = 10) -> Dict[str, Any]:
        """
        Optimize query/prompt using GEPA teleprompter.
        
        Args:
            query: Initial query or prompt
            traces: Execution traces for optimization
            iterations: Number of optimization iterations
            
        Returns:
            Optimization results with improved prompt
        """
        traces = traces or []
        
        # Pre-optimization metrics
        pre_metrics = self.coherence_analyzer.analyze(query)
        
        # Run GEPA annealing
        optimized, final_score = self.teleprompter.anneal(
            query, traces, iterations=iterations
        )
        
        # Post-optimization metrics
        post_metrics = self.coherence_analyzer.analyze(optimized)
        
        # COPRO comparison
        entropy_comparison = EntropyComparison.compute(
            pre_metrics, post_metrics, self.entropy_threshold
        )
        
        return {
            "original_query": query,
            "optimized_query": optimized,
            "pre_coherence": pre_metrics.coherence_score,
            "post_coherence": post_metrics.coherence_score,
            "improvement": post_metrics.coherence_score - pre_metrics.coherence_score,
            "entropy_comparison": {
                "pre_entropy": entropy_comparison.pre_entropy,
                "post_entropy": entropy_comparison.post_entropy,
                "differential": entropy_comparison.differential,
                "within_threshold": entropy_comparison.within_threshold
            },
            "optimization_history": self.teleprompter.optimization_history
        }


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Command-line interface for SpiralVerifier."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="SPIRAL Phase Constraint Verifier"
    )
    parser.add_argument(
        "content",
        nargs="?",
        help="Content to verify (reads from stdin if not provided)"
    )
    parser.add_argument(
        "--target-coherence",
        type=float,
        default=0.70,
        help="Target coherence threshold (default: 0.70)"
    )
    parser.add_argument(
        "--entropy-threshold",
        type=float,
        default=0.05,
        help="Maximum entropy differential (default: 0.05)"
    )
    parser.add_argument(
        "--optimize",
        action="store_true",
        help="Run GEPA optimization"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=10,
        help="Optimization iterations (default: 10)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    args = parser.parse_args()
    
    # Get content
    if args.content:
        content = args.content
    else:
        import sys
        content = sys.stdin.read()
    
    # Initialize verifier
    verifier = SpiralVerifier(
        target_coherence=args.target_coherence,
        entropy_threshold=args.entropy_threshold
    )
    
    # Run verification
    if args.optimize:
        result = verifier.optimize(content, iterations=args.iterations)
    else:
        result = verifier.forward("Verify content", content)
    
    # Output results
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("=" * 60)
        print("SPIRAL VERIFIER RESULTS")
        print("=" * 60)
        
        if args.optimize:
            print(f"Pre-coherence:  {result['pre_coherence']:.2%}")
            print(f"Post-coherence: {result['post_coherence']:.2%}")
            print(f"Improvement:    {result['improvement']:+.2%}")
            print(f"Entropy diff:   {result['entropy_comparison']['differential']:.4f}")
            print(f"Within threshold: {result['entropy_comparison']['within_threshold']}")
        else:
            print(f"Verified: {result['verified']}")
            print(f"Coherence: {result['coherence_score']:.2%}")
            print(f"Meets threshold: {result['meets_threshold']}")
            print()
            for r in result['results']:
                status = "✓" if r['passed'] else "✗"
                print(f"  {status} {r['constraint']}: {r['message']}")


if __name__ == "__main__":
    main()
