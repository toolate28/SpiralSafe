#!/usr/bin/env python3
"""
SpiralSafe Scientific Visualization Pipeline
=============================================
Generate mathematical and scientific visualizations

Supports:
- Bloch sphere / quantum state visualization
- Constraint manifolds (NMSI, quantum-redstone)
- Phase diagrams
- Network/graph visualizations
- Animated evolutions
- Manim integration

Dependencies:
    pip install matplotlib numpy scipy plotly manim
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass
import json

OUTPUT_PATH = Path(__file__).parent.parent / "output" / "visualizations"
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


# =============================================================================
# QUANTUM STATE VISUALIZATIONS
# =============================================================================

class BlochSphere:
    """
    Bloch sphere visualization for single-qubit states.

    The Bloch sphere represents:
    |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩

    Where:
    - θ ∈ [0, π] is the polar angle
    - φ ∈ [0, 2π) is the azimuthal angle
    """

    def __init__(self, figsize: Tuple[int, int] = (10, 10)):
        self.fig = plt.figure(figsize=figsize)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self._draw_sphere()
        self._draw_axes()

    def _draw_sphere(self, alpha: float = 0.1):
        """Draw transparent sphere."""
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))

        self.ax.plot_surface(x, y, z, alpha=alpha, color='cyan', edgecolor='none')

    def _draw_axes(self):
        """Draw X, Y, Z axes with labels."""
        # Axis lines
        self.ax.plot([-1.3, 1.3], [0, 0], [0, 0], 'k-', alpha=0.3, linewidth=1)
        self.ax.plot([0, 0], [-1.3, 1.3], [0, 0], 'k-', alpha=0.3, linewidth=1)
        self.ax.plot([0, 0], [0, 0], [-1.3, 1.3], 'k-', alpha=0.3, linewidth=1)

        # Labels
        self.ax.text(1.4, 0, 0, r'$|+\rangle$', fontsize=12)
        self.ax.text(-1.4, 0, 0, r'$|-\rangle$', fontsize=12)
        self.ax.text(0, 1.4, 0, r'$|+i\rangle$', fontsize=12)
        self.ax.text(0, -1.4, 0, r'$|-i\rangle$', fontsize=12)
        self.ax.text(0, 0, 1.4, r'$|0\rangle$', fontsize=14, fontweight='bold')
        self.ax.text(0, 0, -1.4, r'$|1\rangle$', fontsize=14, fontweight='bold')

    def add_state(
        self,
        theta: float,
        phi: float,
        color: str = 'red',
        label: Optional[str] = None
    ):
        """
        Add a state vector to the Bloch sphere.

        Args:
            theta: Polar angle [0, π]
            phi: Azimuthal angle [0, 2π)
            color: Vector color
            label: Optional label
        """
        # Convert to Cartesian
        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)

        # Draw vector from origin
        self.ax.quiver(0, 0, 0, x, y, z, color=color, arrow_length_ratio=0.1, linewidth=2)

        # Draw point
        self.ax.scatter([x], [y], [z], color=color, s=50, zorder=10)

        if label:
            self.ax.text(x * 1.1, y * 1.1, z * 1.1, label, fontsize=10)

    def add_state_from_amplitudes(
        self,
        alpha: complex,
        beta: complex,
        **kwargs
    ):
        """
        Add state from amplitude coefficients.

        |ψ⟩ = α|0⟩ + β|1⟩
        """
        # Normalize
        norm = np.sqrt(np.abs(alpha)**2 + np.abs(beta)**2)
        alpha, beta = alpha / norm, beta / norm

        # Convert to angles
        theta = 2 * np.arccos(np.abs(alpha))
        phi = np.angle(beta) - np.angle(alpha)

        self.add_state(theta, phi, **kwargs)

    def add_trajectory(
        self,
        thetas: np.ndarray,
        phis: np.ndarray,
        color: str = 'blue',
        alpha: float = 0.7
    ):
        """Add a trajectory on the sphere."""
        x = np.sin(thetas) * np.cos(phis)
        y = np.sin(thetas) * np.sin(phis)
        z = np.cos(thetas)

        self.ax.plot(x, y, z, color=color, alpha=alpha, linewidth=2)

    def add_great_circle(
        self,
        normal: Tuple[float, float, float] = (1, 0, 0),
        color: str = 'gray',
        alpha: float = 0.3
    ):
        """Add a great circle to the sphere."""
        # Generate circle perpendicular to normal
        t = np.linspace(0, 2 * np.pi, 100)

        # Create rotation to align z-axis with normal
        nx, ny, nz = normal
        n = np.sqrt(nx**2 + ny**2 + nz**2)
        nx, ny, nz = nx/n, ny/n, nz/n

        # Simple case for axis-aligned normals
        if abs(nz) > 0.99:
            x, y, z = np.cos(t), np.sin(t), np.zeros_like(t)
        elif abs(nx) > 0.99:
            x, y, z = np.zeros_like(t), np.cos(t), np.sin(t)
        elif abs(ny) > 0.99:
            x, y, z = np.cos(t), np.zeros_like(t), np.sin(t)
        else:
            # General case - use Rodrigues rotation
            x, y, z = np.cos(t), np.sin(t), np.zeros_like(t)

        self.ax.plot(x, y, z, color=color, alpha=alpha, linestyle='--')

    def save(self, filename: str = "bloch_sphere.png", dpi: int = 150):
        """Save figure."""
        self.ax.set_xlim([-1.5, 1.5])
        self.ax.set_ylim([-1.5, 1.5])
        self.ax.set_zlim([-1.5, 1.5])
        self.ax.set_box_aspect([1, 1, 1])
        self.ax.axis('off')

        path = OUTPUT_PATH / filename
        self.fig.savefig(path, dpi=dpi, bbox_inches='tight', transparent=True)
        plt.close(self.fig)
        return path


# =============================================================================
# CONSTRAINT MANIFOLD VISUALIZATIONS
# =============================================================================

class ConstraintManifold:
    """
    Visualize constraint manifolds like:
    - |α|² + |β|² = 1 (quantum normalization)
    - ALPHA + OMEGA = 15 (quantum-redstone)
    - cos²(φ) + sin²(φ) = 1 (fundamental identity)
    """

    @staticmethod
    def normalization_surface(
        output: str = "normalization_manifold.html",
        constraint_value: float = 1.0
    ) -> Path:
        """
        Visualize the constraint surface |α|² + |β|² = C

        This is the fundamental NMSI constraint that underlies
        quantum mechanics and emerges from informational dynamics.
        """
        # Create mesh for constraint surface
        theta = np.linspace(0, 2 * np.pi, 100)
        r = np.sqrt(constraint_value)

        x = r * np.cos(theta)
        y = r * np.sin(theta)

        fig = go.Figure()

        # The constraint circle
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            name=f'|α|² + |β|² = {constraint_value}',
            line=dict(color='blue', width=3)
        ))

        # Sample states on the constraint
        for i, t in enumerate(np.linspace(0, 2*np.pi, 8, endpoint=False)):
            px, py = r * np.cos(t), r * np.sin(t)
            fig.add_trace(go.Scatter(
                x=[0, px], y=[0, py],
                mode='lines+markers',
                name=f'|ψ_{i}⟩',
                line=dict(width=1, dash='dot'),
                marker=dict(size=[0, 8])
            ))

        fig.update_layout(
            title=dict(
                text='Quantum Normalization Constraint Manifold<br><sup>|α|² + |β|² = 1 — The Mathematical DNA</sup>',
                x=0.5
            ),
            xaxis_title='|α|²',
            yaxis_title='|β|²',
            showlegend=True,
            width=800,
            height=800
        )

        fig.update_xaxes(scaleanchor="y", scaleratio=1)

        path = OUTPUT_PATH / output
        fig.write_html(path)
        return path

    @staticmethod
    def alpha_omega_constraint(
        output: str = "alpha_omega_constraint.html",
        max_value: int = 15
    ) -> Path:
        """
        Visualize ALPHA + OMEGA = 15 constraint from quantum-redstone.

        This is the discrete analog of quantum normalization.
        """
        fig = go.Figure()

        # Valid states on constraint
        alphas = list(range(max_value + 1))
        omegas = [max_value - a for a in alphas]

        fig.add_trace(go.Scatter(
            x=alphas, y=omegas,
            mode='lines+markers',
            name=f'ALPHA + OMEGA = {max_value}',
            line=dict(color='red', width=3),
            marker=dict(size=10)
        ))

        # Highlight key states
        special_states = [
            (0, max_value, '|0⟩ analog'),
            (max_value, 0, '|1⟩ analog'),
            (max_value // 2, max_value - max_value // 2, '|+⟩ analog'),
        ]

        for alpha, omega, label in special_states:
            fig.add_annotation(
                x=alpha, y=omega,
                text=label,
                showarrow=True,
                arrowhead=2,
                ax=30, ay=-30
            )

        # Show invalid region
        fig.add_shape(
            type="rect",
            x0=0, y0=0, x1=max_value, y1=max_value,
            fillcolor="lightgray",
            opacity=0.3,
            layer="below",
            line_width=0,
        )

        fig.update_layout(
            title=dict(
                text=f'Quantum-Redstone Constraint Manifold<br><sup>ALPHA + OMEGA = {max_value} — Discrete Unitarity</sup>',
                x=0.5
            ),
            xaxis_title='ALPHA (signal level)',
            yaxis_title='OMEGA (complement)',
            showlegend=True,
            width=800,
            height=800
        )

        fig.update_xaxes(range=[-1, max_value + 1], scaleanchor="y", scaleratio=1)
        fig.update_yaxes(range=[-1, max_value + 1])

        path = OUTPUT_PATH / output
        fig.write_html(path)
        return path

    @staticmethod
    def cos_sin_identity_3d(output: str = "cos_sin_identity.html") -> Path:
        """
        Visualize cos²(φ) + sin²(φ) = 1 as a 3D surface.

        This is the "mathematical DNA" that both NMSI and
        quantum-redstone are built upon.
        """
        phi = np.linspace(0, 2 * np.pi, 100)
        cos2 = np.cos(phi) ** 2
        sin2 = np.sin(phi) ** 2

        fig = go.Figure()

        # 3D parametric curve
        fig.add_trace(go.Scatter3d(
            x=phi,
            y=cos2,
            z=sin2,
            mode='lines',
            name='Trajectory',
            line=dict(color='purple', width=5)
        ))

        # Project onto xy plane
        fig.add_trace(go.Scatter3d(
            x=phi,
            y=cos2,
            z=np.zeros_like(phi),
            mode='lines',
            name='cos²(φ)',
            line=dict(color='blue', width=2, dash='dash')
        ))

        # Project onto xz plane
        fig.add_trace(go.Scatter3d(
            x=phi,
            y=np.zeros_like(phi),
            z=sin2,
            mode='lines',
            name='sin²(φ)',
            line=dict(color='red', width=2, dash='dash')
        ))

        # Constraint plane cos² + sin² = 1
        xx = np.linspace(0, 2 * np.pi, 20)
        yy = np.linspace(0, 1, 20)
        X, Y = np.meshgrid(xx, yy)
        Z = 1 - Y  # cos² + sin² = 1 → sin² = 1 - cos²

        fig.add_trace(go.Surface(
            x=X, y=Y, z=Z,
            opacity=0.3,
            colorscale='Viridis',
            showscale=False,
            name='Constraint plane'
        ))

        fig.update_layout(
            title=dict(
                text='The Fundamental Identity: cos²(φ) + sin²(φ) = 1<br><sup>Mathematical Foundation of NMSI and Quantum-Redstone</sup>',
                x=0.5
            ),
            scene=dict(
                xaxis_title='Phase φ',
                yaxis_title='cos²(φ)',
                zaxis_title='sin²(φ)',
            ),
            width=900,
            height=700
        )

        path = OUTPUT_PATH / output
        fig.write_html(path)
        return path


# =============================================================================
# PHASE EVOLUTION VISUALIZATIONS
# =============================================================================

class PhaseEvolution:
    """Visualize phase evolution and probability dynamics."""

    @staticmethod
    def probability_oscillation(
        output: str = "probability_oscillation.html",
        periods: float = 2.0
    ) -> Path:
        """
        Show probability oscillation P₀(φ) = cos²(φ), P₁(φ) = sin²(φ)
        """
        phi = np.linspace(0, periods * 2 * np.pi, 500)
        p0 = np.cos(phi) ** 2
        p1 = np.sin(phi) ** 2

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=phi, y=p0,
            mode='lines',
            name='P(|0⟩) = cos²(φ)',
            line=dict(color='blue', width=2)
        ))

        fig.add_trace(go.Scatter(
            x=phi, y=p1,
            mode='lines',
            name='P(|1⟩) = sin²(φ)',
            line=dict(color='red', width=2)
        ))

        # Sum = 1
        fig.add_trace(go.Scatter(
            x=phi, y=p0 + p1,
            mode='lines',
            name='P(|0⟩) + P(|1⟩) = 1',
            line=dict(color='green', width=2, dash='dash')
        ))

        # Mark special points
        special_phi = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
        for p in special_phi:
            fig.add_vline(x=p, line_dash="dot", line_color="gray", opacity=0.5)

        fig.update_layout(
            title='Probability Oscillation Under Phase Evolution',
            xaxis_title='Phase φ',
            yaxis_title='Probability',
            yaxis_range=[0, 1.1],
            width=900,
            height=500
        )

        path = OUTPUT_PATH / output
        fig.write_html(path)
        return path

    @staticmethod
    def discrete_phase_evolution(
        output: str = "discrete_phase_evolution.html",
        max_level: int = 15,
        steps: int = 16
    ) -> Path:
        """
        Discrete phase evolution for quantum-redstone.
        Shows how ALPHA and OMEGA evolve while maintaining ALPHA + OMEGA = 15.
        """
        fig = go.Figure()

        # Continuous evolution mapped to discrete
        phases = np.linspace(0, 2 * np.pi, steps)

        # Map cos²/sin² to discrete levels
        alphas = np.round(np.cos(phases) ** 2 * max_level).astype(int)
        omegas = max_level - alphas

        fig.add_trace(go.Scatter(
            x=list(range(steps)),
            y=alphas,
            mode='lines+markers',
            name='ALPHA',
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        ))

        fig.add_trace(go.Scatter(
            x=list(range(steps)),
            y=omegas,
            mode='lines+markers',
            name='OMEGA',
            line=dict(color='red', width=2),
            marker=dict(size=8)
        ))

        fig.add_trace(go.Scatter(
            x=list(range(steps)),
            y=[max_level] * steps,
            mode='lines',
            name=f'ALPHA + OMEGA = {max_level}',
            line=dict(color='green', width=2, dash='dash')
        ))

        fig.update_layout(
            title=f'Discrete Phase Evolution (max={max_level})<br><sup>Conservation: ALPHA + OMEGA = {max_level}</sup>',
            xaxis_title='Evolution Step',
            yaxis_title='Signal Level',
            yaxis_range=[0, max_level + 1],
            width=900,
            height=500
        )

        path = OUTPUT_PATH / output
        fig.write_html(path)
        return path


# =============================================================================
# INFORMATION FIELD VISUALIZATIONS
# =============================================================================

class InformationField:
    """Visualize information-theoretic concepts from NMSI."""

    @staticmethod
    def informational_density_field(
        output: str = "info_density_field.html",
        resolution: int = 50
    ) -> Path:
        """
        Visualize an informational density field.
        In NMSI, physical phenomena emerge from modulation of information density.
        """
        x = np.linspace(-5, 5, resolution)
        y = np.linspace(-5, 5, resolution)
        X, Y = np.meshgrid(x, y)

        # Simulated informational density with oscillatory pattern
        # (Represents the Riemann Oscillatory Network concept)
        R = np.sqrt(X**2 + Y**2)
        density = np.exp(-R/3) * np.cos(R * 2) ** 2 + 0.1

        fig = go.Figure(data=go.Heatmap(
            x=x, y=y, z=density,
            colorscale='Viridis',
            colorbar=dict(title='ρ_info')
        ))

        fig.update_layout(
            title='Informational Density Field<br><sup>NMSI: Physical phenomena emerge from information modulation</sup>',
            xaxis_title='x',
            yaxis_title='y',
            width=700,
            height=700
        )

        fig.update_xaxes(scaleanchor="y", scaleratio=1)

        path = OUTPUT_PATH / output
        fig.write_html(path)
        return path

    @staticmethod
    def riemann_oscillatory_network(
        output: str = "riemann_network.html",
        n_nodes: int = 100
    ) -> Path:
        """
        Visualize a simplified Riemann Oscillatory Network.

        In NMSI, N ≈ 10¹² nodes correspond to non-trivial zeros
        of the Riemann zeta function.
        """
        # Generate positions (simplified - real positions would use zeta zeros)
        np.random.seed(42)
        angles = np.linspace(0, 2 * np.pi, n_nodes, endpoint=False)
        radii = 1 + 0.3 * np.sin(5 * angles) + 0.1 * np.random.randn(n_nodes)

        x = radii * np.cos(angles)
        y = radii * np.sin(angles)

        # Generate edges (nearest neighbors)
        edges_x = []
        edges_y = []
        for i in range(n_nodes):
            j = (i + 1) % n_nodes
            edges_x.extend([x[i], x[j], None])
            edges_y.extend([y[i], y[j], None])

        fig = go.Figure()

        # Edges
        fig.add_trace(go.Scatter(
            x=edges_x, y=edges_y,
            mode='lines',
            line=dict(color='lightblue', width=0.5),
            hoverinfo='none'
        ))

        # Nodes
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='markers',
            marker=dict(
                size=8,
                color=angles,
                colorscale='Rainbow',
                showscale=True,
                colorbar=dict(title='Phase')
            ),
            hovertemplate='Node %{pointNumber}<br>x: %{x:.3f}<br>y: %{y:.3f}'
        ))

        fig.update_layout(
            title=f'Riemann Oscillatory Network ({n_nodes} nodes)<br><sup>NMSI: Computational substrate underlying observable physics</sup>',
            showlegend=False,
            width=700,
            height=700
        )

        fig.update_xaxes(scaleanchor="y", scaleratio=1, visible=False)
        fig.update_yaxes(visible=False)

        path = OUTPUT_PATH / output
        fig.write_html(path)
        return path


# =============================================================================
# ISOMORPHISM DIAGRAM
# =============================================================================

class IsomorphismDiagram:
    """Visualize the isomorphism between NMSI and Quantum-Redstone."""

    @staticmethod
    def nmsi_qr_mapping(output: str = "nmsi_qr_isomorphism.html") -> Path:
        """
        Create a visual mapping between NMSI and Quantum-Redstone concepts.
        """
        fig = go.Figure()

        # NMSI side (left)
        nmsi_concepts = [
            ('|α|² + |β|² = 1', 4),
            ('Informational Lagrangian', 3),
            ('Infobit', 2),
            ('Maxwell Emergence', 1),
            ('Topological Protection', 0),
        ]

        # Quantum-Redstone side (right)
        qr_concepts = [
            ('ALPHA + OMEGA = 15', 4),
            ('Two-Rail Encoding', 3),
            ('Redstone Signal', 2),
            ('Gate Operations Emerge', 1),
            ('Constraint Preservation', 0),
        ]

        # Draw boxes and labels
        for (nmsi_text, y), (qr_text, _) in zip(nmsi_concepts, qr_concepts):
            # NMSI box
            fig.add_shape(
                type="rect",
                x0=0, y0=y-0.3, x1=2.5, y1=y+0.3,
                fillcolor="lightblue",
                line=dict(color="blue")
            )
            fig.add_annotation(
                x=1.25, y=y,
                text=nmsi_text,
                showarrow=False,
                font=dict(size=11)
            )

            # QR box
            fig.add_shape(
                type="rect",
                x0=5.5, y0=y-0.3, x1=8, y1=y+0.3,
                fillcolor="lightcoral",
                line=dict(color="red")
            )
            fig.add_annotation(
                x=6.75, y=y,
                text=qr_text,
                showarrow=False,
                font=dict(size=11)
            )

            # Arrow connecting them
            fig.add_annotation(
                x=5.5, y=y,
                ax=2.5, ay=y,
                xref="x", yref="y",
                axref="x", ayref="y",
                showarrow=True,
                arrowhead=2,
                arrowsize=1.5,
                arrowwidth=2,
                arrowcolor="purple"
            )

        # Title labels
        fig.add_annotation(x=1.25, y=5, text="<b>NMSI</b><br>(Lazarev)", showarrow=False, font=dict(size=14))
        fig.add_annotation(x=6.75, y=5, text="<b>Quantum-Redstone</b><br>(Hope&&Sauce)", showarrow=False, font=dict(size=14))

        # Central isomorphism label
        fig.add_annotation(x=4, y=5.5, text="<b>ISOMORPHISM</b>", showarrow=False, font=dict(size=16, color="purple"))

        fig.update_layout(
            title='NMSI ↔ Quantum-Redstone Isomorphism<br><sup>Independent discovery of constraint-based physics emergence</sup>',
            xaxis=dict(visible=False, range=[-0.5, 8.5]),
            yaxis=dict(visible=False, range=[-1, 6]),
            width=900,
            height=600,
            showlegend=False
        )

        path = OUTPUT_PATH / output
        fig.write_html(path)
        return path


# =============================================================================
# MAIN GENERATION FUNCTIONS
# =============================================================================

def generate_all_visualizations():
    """Generate complete visualization suite."""
    outputs = []

    print("Generating visualizations...")

    # Bloch sphere
    print("  - Bloch sphere...")
    bloch = BlochSphere()
    bloch.add_state(0, 0, color='blue', label='|0⟩')
    bloch.add_state(np.pi, 0, color='red', label='|1⟩')
    bloch.add_state(np.pi/2, 0, color='green', label='|+⟩')
    bloch.add_state(np.pi/2, np.pi/2, color='purple', label='|+i⟩')
    outputs.append(bloch.save("bloch_sphere.png"))

    # Constraint manifolds
    print("  - Constraint manifolds...")
    outputs.append(ConstraintManifold.normalization_surface())
    outputs.append(ConstraintManifold.alpha_omega_constraint())
    outputs.append(ConstraintManifold.cos_sin_identity_3d())

    # Phase evolution
    print("  - Phase evolution...")
    outputs.append(PhaseEvolution.probability_oscillation())
    outputs.append(PhaseEvolution.discrete_phase_evolution())

    # Information fields
    print("  - Information fields...")
    outputs.append(InformationField.informational_density_field())
    outputs.append(InformationField.riemann_oscillatory_network())

    # Isomorphism diagram
    print("  - Isomorphism diagram...")
    outputs.append(IsomorphismDiagram.nmsi_qr_mapping())

    print(f"\nGenerated {len(outputs)} visualizations in {OUTPUT_PATH}")
    return outputs


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SpiralSafe Scientific Visualization Pipeline")
    parser.add_argument("--all", action="store_true", help="Generate all visualizations")
    parser.add_argument("--bloch", action="store_true", help="Generate Bloch sphere")
    parser.add_argument("--constraints", action="store_true", help="Generate constraint manifolds")
    parser.add_argument("--phase", action="store_true", help="Generate phase evolution")
    parser.add_argument("--info", action="store_true", help="Generate information field visualizations")
    parser.add_argument("--isomorphism", action="store_true", help="Generate NMSI/QR isomorphism diagram")

    args = parser.parse_args()

    if args.all or not any([args.bloch, args.constraints, args.phase, args.info, args.isomorphism]):
        generate_all_visualizations()
    else:
        if args.bloch:
            bloch = BlochSphere()
            bloch.add_state(np.pi/4, np.pi/4, color='purple')
            bloch.save()
        if args.constraints:
            ConstraintManifold.normalization_surface()
            ConstraintManifold.alpha_omega_constraint()
            ConstraintManifold.cos_sin_identity_3d()
        if args.phase:
            PhaseEvolution.probability_oscillation()
            PhaseEvolution.discrete_phase_evolution()
        if args.info:
            InformationField.informational_density_field()
            InformationField.riemann_oscillatory_network()
        if args.isomorphism:
            IsomorphismDiagram.nmsi_qr_mapping()
