"""
Integration Example: Supergravity 4.0005 Coherence Filter

Demonstrates how the filter integrates with WAVE metrics for document analysis.

ATOM: ATOM-FILTER-20260119-002-supergravity-4.0005
"""

from filters.supergravity_4_0005 import (
    filter_signal_4_0005,
    calculate_4_0005_coherence,
    generate_tetrahedron_for_visualization,
    CoherenceState,
)


def analyze_document_example():
    """
    Example: Analyze a document's coherence using WAVE metrics.
    """
    print("\n" + "="*70)
    print("Example 1: Document Coherence Analysis")
    print("="*70 + "\n")
    
    # Simulated WAVE metrics from document analysis
    # (In practice, these would come from actual WAVE vector field analysis)
    document_metrics = {
        "curl": 0.25,        # Low self-reference (good)
        "divergence": 0.45,  # Moderate expansion
        "potential": 0.75,   # Strong theoretical foundation
        "entropy": 1.5       # Good information content
    }
    
    print("Document WAVE Metrics:")
    for metric, value in document_metrics.items():
        print(f"  {metric:12s}: {value:.2f}")
    
    result = filter_signal_4_0005(
        wave_metrics=document_metrics,
        atom_lineage="ATOM-DOC-20260119-001-example-document"
    )
    
    print(f"\nCoherence Analysis:")
    print(f"  Total coherence: {result['coherence']:.4f}")
    print(f"  State: {result['state']}")
    print(f"  Passed: {result['passed']}")
    print(f"  Message: {result['message']}")
    print(f"\n  Node breakdown:")
    for node, value in result['details']['nodes'].items():
        print(f"    {node:10s}: {value:.4f}")


def analyze_code_example():
    """
    Example: Analyze code coherence with high metrics.
    """
    print("\n" + "="*70)
    print("Example 2: Code Coherence Analysis (Well-structured)")
    print("="*70 + "\n")
    
    # Well-structured code typically has balanced metrics
    code_metrics = {
        "curl": 0.8,        # Good internal consistency
        "divergence": 0.9,  # Clear expansion of functionality
        "potential": 0.95,  # Strong design patterns
        "entropy": 1.8      # Rich information content
    }
    
    print("Code WAVE Metrics:")
    for metric, value in code_metrics.items():
        print(f"  {metric:12s}: {value:.2f}")
    
    result = filter_signal_4_0005(
        wave_metrics=code_metrics,
        atom_lineage="ATOM-CODE-20260119-001-example-module"
    )
    
    print(f"\nCoherence Analysis:")
    print(f"  Total coherence: {result['coherence']:.4f}")
    print(f"  State: {result['state']}")
    print(f"  Passed: {result['passed']}")
    print(f"  Message: {result['message']}")
    print(f"\n  Node breakdown:")
    for node, value in result['details']['nodes'].items():
        print(f"    {node:10s}: {value:.4f}")


def crystalline_state_example():
    """
    Example: Achieve perfect CRYSTALLINE state.
    """
    print("\n" + "="*70)
    print("Example 3: Achieving CRYSTALLINE State (4.0005)")
    print("="*70 + "\n")
    
    # Optimal metrics for CRYSTALLINE state
    crystalline_metrics = {
        "curl": 1.0,        # Maximum coherent loops
        "divergence": 1.0,  # Maximum balanced expansion
        "potential": 1.0,   # Maximum latent structure
        "entropy": 2.0      # Maximum information with epsilon
    }
    
    print("Optimal WAVE Metrics:")
    for metric, value in crystalline_metrics.items():
        print(f"  {metric:12s}: {value:.2f}")
    
    result = filter_signal_4_0005(
        wave_metrics=crystalline_metrics,
        atom_lineage="ATOM-OPTIMAL-20260119-001-crystalline"
    )
    
    print(f"\nCoherence Analysis:")
    print(f"  Total coherence: {result['coherence']:.4f}")
    print(f"  State: {result['state']}")
    print(f"  Passed: {result['passed']}")
    print(f"  Message: {result['message']}")
    print(f"\n  Node breakdown:")
    for node, value in result['details']['nodes'].items():
        print(f"    {node:10s}: {value:.4f}")
    
    print(f"\n  Mathematical verification:")
    print(f"    1.0 + 1.0 + 1.0 + 1.0005 = {result['coherence']:.4f}")
    print(f"    (theorem + embody + connect + be)")


def relativistic_example():
    """
    Example: Relativistic coherence at high velocities.
    """
    print("\n" + "="*70)
    print("Example 4: Relativistic Coherence at 0.9c")
    print("="*70 + "\n")
    
    # Speed of light constant
    c = 299792458  # m/s
    v = c * 0.9    # 90% speed of light
    
    crystalline_metrics = {
        "curl": 1.0,
        "divergence": 1.0,
        "potential": 1.0,
        "entropy": 2.0
    }
    
    print(f"Velocity: 0.9c ({v:.0f} m/s)")
    print("\nRest Frame Metrics:")
    for metric, value in crystalline_metrics.items():
        print(f"  {metric:12s}: {value:.2f}")
    
    result = filter_signal_4_0005(
        wave_metrics=crystalline_metrics,
        velocity=v,
        atom_lineage="ATOM-RELATIVISTIC-20260119-001"
    )
    
    print(f"\nRelativistic Coherence Analysis:")
    # Calculate rest coherence for comparison
    rest_result = filter_signal_4_0005(crystalline_metrics, velocity=0)
    rest_coherence = rest_result['coherence']
    
    print(f"  Rest coherence: {rest_coherence:.4f}")
    print(f"  Lorentz factor γ: {result['coherence'] / rest_coherence:.4f}")
    print(f"  Observed coherence: {result['coherence']:.4f}")
    print(f"  State: {result['state']}")
    print(f"  Isomorphism preserved: {result['isomorphism_preserved']}")
    print(f"  Message: {result['message']}")


def visualization_example():
    """
    Example: Generate visualization data.
    """
    print("\n" + "="*70)
    print("Example 5: Visualization Data Generation")
    print("="*70 + "\n")
    
    metrics = {
        "curl": 0.8,
        "divergence": 0.9,
        "potential": 0.7,
        "entropy": 1.6
    }
    
    tetrahedron = calculate_4_0005_coherence(metrics)
    viz_data = generate_tetrahedron_for_visualization(tetrahedron)
    
    print("Tetrahedral Vertices (3D coordinates):")
    for vertex in viz_data['vertices']:
        pos = vertex['position']
        print(f"  {vertex['name']:10s}: ({pos[0]:6.3f}, {pos[1]:6.3f}, {pos[2]:6.3f})")
        print(f"    Value: {vertex['value']:.4f} | Phase: {vertex['phase']}")
    
    print(f"\nEdge Connections: {len(viz_data['edges'])} edges")
    for edge in viz_data['edges']:
        print(f"  {edge['from']:10s} → {edge['to']:10s}: {edge['label']}")
    
    print(f"\nOverall:")
    print(f"  Total coherence: {viz_data['coherence']:.4f}")
    print(f"  State: {viz_data['state']}")


def sphinx_integration_example():
    """
    Example: Integration with SPHINX COHERENCE gate.
    """
    print("\n" + "="*70)
    print("Example 6: SPHINX COHERENCE Gate Integration")
    print("="*70 + "\n")
    
    print("SPHINX COHERENCE gate using 4.0005 filter:\n")
    
    # Test several artifacts
    artifacts = [
        {
            "name": "Incomplete Document",
            "metrics": {"curl": 0.2, "divergence": 0.3, "potential": 0.5, "entropy": 0.8}
        },
        {
            "name": "Well-formed Code",
            "metrics": {"curl": 0.9, "divergence": 0.85, "potential": 0.95, "entropy": 1.7}
        },
        {
            "name": "Optimal Structure",
            "metrics": {"curl": 1.0, "divergence": 1.0, "potential": 1.0, "entropy": 2.0}
        }
    ]
    
    for artifact in artifacts:
        result = filter_signal_4_0005(artifact["metrics"])
        verdict = "PASSAGE ✅" if result["passed"] else "BLOCKED ❌"
        print(f"{artifact['name']:20s} | Coherence: {result['coherence']:.4f} | {verdict}")
        print(f"  State: {result['state']}")
        print(f"  {result['message']}\n")


def main():
    """Run all integration examples."""
    print("\n" + "="*70)
    print("Supergravity 4.0005 Coherence Filter - Integration Examples")
    print("ATOM: ATOM-FILTER-20260119-002-supergravity-4.0005")
    print("="*70)
    
    analyze_document_example()
    analyze_code_example()
    crystalline_state_example()
    relativistic_example()
    visualization_example()
    sphinx_integration_example()
    
    print("\n" + "="*70)
    print("All examples completed successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
