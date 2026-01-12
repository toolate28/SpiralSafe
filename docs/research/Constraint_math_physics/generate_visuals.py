#!/usr/bin/env python3
"""
Generate visualizations for the Constraint Mathematics paper.
Uses the SpiralSafe visualization and image pipelines.

Usage:
    python generate_visuals.py --output ./figures
    python generate_visuals.py --all --format pdf
"""

import sys
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'media' / 'pipelines'))

try:
    from visualization_pipeline import BlochSphere, ConstraintManifold, IsomorphismDiagram
    HAS_VIZ_PIPELINE = True
except ImportError:
    HAS_VIZ_PIPELINE = False
    print("Note: visualization_pipeline not available, using fallback")


class ConstraintVisualization:
    """Generate constraint mathematics visualizations."""

    def __init__(self, output_dir: str = "./figures"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Color scheme
        self.colors = {
            'quantum': '#3498db',      # Blue
            'discrete': '#e74c3c',     # Red
            'constraint': '#9b59b6',   # Purple
            'emergence': '#2ecc71',    # Green
            'gold': '#f39c12',         # Gold
            'dark': '#2c3e50'          # Dark blue-gray
        }

        plt.rcParams['figure.facecolor'] = 'white'
        plt.rcParams['axes.facecolor'] = 'white'
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['mathtext.fontset'] = 'cm'

    def fig1_quantum_discrete_isomorphism(self, save: bool = True) -> plt.Figure:
        """Figure 1: The fundamental isomorphism Q2 <-> D15."""

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        # Left: Quantum space (Bloch sphere projection)
        ax1 = axes[0]
        theta = np.linspace(0, 2*np.pi, 100)
        ax1.plot(np.cos(theta), np.sin(theta), color=self.colors['quantum'], linewidth=2)
        ax1.fill(np.cos(theta), np.sin(theta), color=self.colors['quantum'], alpha=0.1)

        # Mark some states
        states = [(1, 0, r'$|0\rangle$'),
                  (-1, 0, r'$|1\rangle$'),
                  (0, 1, r'$|+\rangle$'),
                  (0, -1, r'$|-\rangle$')]
        for x, y, label in states:
            ax1.plot(x, y, 'o', color=self.colors['quantum'], markersize=10)
            ax1.annotate(label, (x, y), xytext=(10, 10), textcoords='offset points', fontsize=12)

        ax1.set_xlim(-1.5, 1.5)
        ax1.set_ylim(-1.5, 1.5)
        ax1.set_aspect('equal')
        ax1.set_title(r'$Q_2$: Quantum States', fontsize=14, fontweight='bold')
        ax1.annotate(r'$|\alpha|^2 + |\beta|^2 = 1$', (0, -1.3), ha='center', fontsize=12)
        ax1.axis('off')

        # Middle: The mapping
        ax2 = axes[1]
        ax2.axis('off')
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 10)

        # Draw arrow
        arrow = FancyArrowPatch((2, 5), (8, 5),
                                connectionstyle="arc3,rad=0",
                                arrowstyle='->,head_length=0.5,head_width=0.3',
                                color=self.colors['constraint'], linewidth=3)
        ax2.add_patch(arrow)

        ax2.text(5, 6.5, r'$\pi$', fontsize=20, ha='center', fontweight='bold',
                color=self.colors['constraint'])
        ax2.text(5, 3.5, 'Constraint-Preserving\nSurjection', fontsize=11, ha='center',
                style='italic')
        ax2.set_title('Isomorphism', fontsize=14, fontweight='bold')

        # Right: Discrete space
        ax3 = axes[2]
        # Draw the D15 constraint line
        m_vals = np.arange(0, 16)
        n_vals = 15 - m_vals

        ax3.plot(m_vals, n_vals, 'o-', color=self.colors['discrete'], linewidth=2, markersize=8)

        # Highlight some points
        highlights = [(0, 15), (7, 8), (15, 0)]
        for m, n in highlights:
            ax3.plot(m, n, 's', color=self.colors['gold'], markersize=15, zorder=5)
            ax3.annotate(f'({m},{n})', (m, n), xytext=(5, 5), textcoords='offset points', fontsize=10)

        ax3.set_xlabel(r'$\alpha$ (ALPHA)', fontsize=12)
        ax3.set_ylabel(r'$\omega$ (OMEGA)', fontsize=12)
        ax3.set_xlim(-1, 16)
        ax3.set_ylim(-1, 16)
        ax3.grid(True, alpha=0.3)
        ax3.set_title(r'$D_{15}$: Discrete States', fontsize=14, fontweight='bold')
        ax3.annotate(r'$\alpha + \omega = 15$', (7.5, -0.5), ha='center', fontsize=12)

        plt.tight_layout()

        if save:
            fig.savefig(self.output_dir / 'fig1_isomorphism.png', dpi=300, bbox_inches='tight')
            fig.savefig(self.output_dir / 'fig1_isomorphism.pdf', bbox_inches='tight')

        return fig

    def fig2_derivation_hierarchy(self, save: bool = True) -> plt.Figure:
        """Figure 2: The derivation hierarchy from self-consistency to physics."""

        fig, ax = plt.subplots(figsize=(12, 14))
        ax.axis('off')
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 14)

        # Levels
        levels = [
            (6, 13, 'SELF-CONSISTENCY', self.colors['constraint']),
            (6, 11.5, 'EXISTENCE', self.colors['gold']),
            (6, 10, 'EMERGENCE', self.colors['emergence']),
            (6, 8.5, 'SYMMETRY', self.colors['quantum']),
            (3, 7, 'Energy', '#95a5a6'),
            (5, 7, 'Momentum', '#95a5a6'),
            (7, 7, 'Ang. Mom.', '#95a5a6'),
            (9, 7, 'Charge', '#95a5a6'),
            (6, 5.5, 'GAUGE FIELDS', self.colors['discrete']),
            (3, 4, 'E&M', '#7f8c8d'),
            (6, 4, 'Weak', '#7f8c8d'),
            (9, 4, 'Strong', '#7f8c8d'),
            (3.5, 2.5, 'SPACETIME', self.colors['quantum']),
            (8.5, 2.5, 'GRAVITY', self.colors['discrete']),
            (6, 1, 'QUANTUM MECHANICS', self.colors['emergence']),
        ]

        # Draw boxes
        for x, y, text, color in levels:
            width = 2.5 if len(text) > 8 else 1.8
            height = 0.7
            box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                                boxstyle="round,pad=0.05,rounding_size=0.1",
                                facecolor=color, edgecolor='black', alpha=0.8,
                                linewidth=2)
            ax.add_patch(box)
            ax.text(x, y, text, ha='center', va='center', fontsize=9 if len(text) > 10 else 10,
                   fontweight='bold', color='white')

        # Draw arrows
        arrows = [
            ((6, 12.7), (6, 11.9)),      # Self-consistency -> Existence
            ((6, 11.2), (6, 10.4)),      # Existence -> Emergence
            ((6, 9.7), (6, 8.9)),        # Emergence -> Symmetry
            ((4, 8.2), (3, 7.4)),        # Symmetry -> Energy
            ((5, 8.2), (5, 7.4)),        # Symmetry -> Momentum
            ((7, 8.2), (7, 7.4)),        # Symmetry -> Ang Mom
            ((8, 8.2), (9, 7.4)),        # Symmetry -> Charge
            ((6, 6.7), (6, 5.9)),        # Conservation -> Gauge
            ((4.5, 5.2), (3, 4.4)),      # Gauge -> E&M
            ((6, 5.2), (6, 4.4)),        # Gauge -> Weak
            ((7.5, 5.2), (9, 4.4)),      # Gauge -> Strong
            ((4.5, 5.2), (3.5, 2.9)),    # Gauge -> Spacetime
            ((7.5, 5.2), (8.5, 2.9)),    # Gauge -> Gravity
            ((3.5, 2.2), (5, 1.4)),      # Spacetime -> QM
            ((8.5, 2.2), (7, 1.4)),      # Gravity -> QM
        ]

        for start, end in arrows:
            arrow = FancyArrowPatch(start, end,
                                   connectionstyle="arc3,rad=0",
                                   arrowstyle='->,head_length=0.2,head_width=0.15',
                                   color=self.colors['dark'], linewidth=1.5)
            ax.add_patch(arrow)

        ax.set_title('The Derivation Hierarchy\nFrom Self-Consistency to Physics',
                    fontsize=16, fontweight='bold', pad=20)

        if save:
            fig.savefig(self.output_dir / 'fig2_hierarchy.png', dpi=300, bbox_inches='tight')
            fig.savefig(self.output_dir / 'fig2_hierarchy.pdf', bbox_inches='tight')

        return fig

    def fig3_constraint_intersection(self, save: bool = True) -> plt.Figure:
        """Figure 3: Measurement as constraint intersection."""

        fig, ax = plt.subplots(figsize=(10, 8))

        # Draw overlapping circles
        circle1 = Circle((3.5, 5), 2.5, fill=True, facecolor=self.colors['quantum'],
                         alpha=0.3, edgecolor=self.colors['quantum'], linewidth=2)
        circle2 = Circle((6.5, 5), 2.5, fill=True, facecolor=self.colors['discrete'],
                         alpha=0.3, edgecolor=self.colors['discrete'], linewidth=2)

        ax.add_patch(circle1)
        ax.add_patch(circle2)

        # Highlight intersection
        theta = np.linspace(0, 2*np.pi, 100)
        ax.fill_between([4, 6], [3, 3], [7, 7], color=self.colors['emergence'], alpha=0.5)

        # Labels
        ax.text(2.5, 5, r'$Q$' + '\nNormalization\nConstraint', ha='center', va='center',
               fontsize=11, fontweight='bold')
        ax.text(7.5, 5, r'$M$' + '\nMeasurement\nConstraint', ha='center', va='center',
               fontsize=11, fontweight='bold')
        ax.text(5, 5, r'$Q \cap M$' + '\nCollapsed\nState', ha='center', va='center',
               fontsize=11, fontweight='bold', color=self.colors['dark'])

        ax.set_xlim(0, 10)
        ax.set_ylim(1, 9)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Measurement as Constraint Intersection\n(No "Collapse" - Just Intersection)',
                    fontsize=14, fontweight='bold')

        if save:
            fig.savefig(self.output_dir / 'fig3_measurement.png', dpi=300, bbox_inches='tight')
            fig.savefig(self.output_dir / 'fig3_measurement.pdf', bbox_inches='tight')

        return fig

    def fig4_self_reference(self, save: bool = True) -> plt.Figure:
        """Figure 4: The self-reference - existence as self-consistent constraint."""

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.axis('off')
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)

        # Draw ouroboros-like circle
        theta = np.linspace(0, 2*np.pi, 100)
        r = 1
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        # Gradient color along the circle
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        for i in range(len(segments)):
            color = plt.cm.viridis(i / len(segments))
            ax.plot([segments[i][0][0], segments[i][1][0]],
                   [segments[i][0][1], segments[i][1][1]],
                   color=color, linewidth=8)

        # Arrow showing self-reference
        ax.annotate('', xy=(0.1, 1.05), xytext=(-.1, 1.05),
                   arrowprops=dict(arrowstyle='->,head_length=0.3,head_width=0.2',
                                 color=self.colors['gold'], lw=3))

        # Central equation
        ax.text(0, 0, r'$\exists \equiv C(C)$', fontsize=24, ha='center', va='center',
               fontweight='bold', color=self.colors['dark'])
        ax.text(0, -0.3, 'Existence IS\nSelf-Referential Constraint',
               fontsize=12, ha='center', va='center', style='italic')

        # Outer labels
        labels = [
            (0, 1.3, 'Constraint'),
            (1.1, 0.5, 'requires'),
            (1.1, -0.5, 'structure'),
            (0, -1.3, 'Structure'),
            (-1.1, -0.5, 'is'),
            (-1.1, 0.5, 'constraint'),
        ]
        for x, y, text in labels:
            ax.text(x, y, text, fontsize=11, ha='center', va='center')

        ax.set_title('The Self-Reference Theorem\n(Theorem 6.3)', fontsize=16, fontweight='bold')

        if save:
            fig.savefig(self.output_dir / 'fig4_self_reference.png', dpi=300, bbox_inches='tight')
            fig.savefig(self.output_dir / 'fig4_self_reference.pdf', bbox_inches='tight')

        return fig

    def fig5_noether(self, save: bool = True) -> plt.Figure:
        """Figure 5: Symmetry -> Conservation (Noether)."""

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        symmetries = [
            ('Time Translation', 'Energy', 't -> t + dt', 'H = const'),
            ('Space Translation', 'Momentum', 'x -> x + dx', 'p = const'),
            ('Rotation', 'Angular Momentum', 'theta -> theta + d_theta', 'L = const'),
            ('U(1) Gauge', 'Electric Charge', 'psi -> e^{i*theta}*psi', 'Q = const'),
        ]

        colors = [self.colors['quantum'], self.colors['discrete'],
                 self.colors['emergence'], self.colors['gold']]

        for ax, (symm, conserved, transform, result), color in zip(axes.flat, symmetries, colors):
            ax.axis('off')
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)

            # Symmetry box
            box1 = FancyBboxPatch((0.5, 6), 4, 2.5,
                                 boxstyle="round,pad=0.1",
                                 facecolor=color, alpha=0.7,
                                 edgecolor='black', linewidth=2)
            ax.add_patch(box1)
            ax.text(2.5, 7.25, symm, ha='center', va='center',
                   fontsize=11, fontweight='bold', color='white')
            ax.text(2.5, 6.5, f'${transform}$', ha='center', va='center',
                   fontsize=10, color='white')

            # Arrow
            arrow = FancyArrowPatch((4.5, 5), (5.5, 5),
                                   arrowstyle='->,head_length=0.3,head_width=0.2',
                                   color='black', linewidth=2)
            ax.add_patch(arrow)
            ax.text(5, 5.5, 'Noether', ha='center', fontsize=9, style='italic')

            # Conservation box
            box2 = FancyBboxPatch((5.5, 3.5), 4, 2.5,
                                 boxstyle="round,pad=0.1",
                                 facecolor=self.colors['constraint'], alpha=0.7,
                                 edgecolor='black', linewidth=2)
            ax.add_patch(box2)
            ax.text(7.5, 4.75, conserved, ha='center', va='center',
                   fontsize=11, fontweight='bold', color='white')
            ax.text(7.5, 4, f'${result}$', ha='center', va='center',
                   fontsize=10, color='white')

        fig.suptitle('Symmetry -> Conservation Laws (Theorem 12.1)',
                    fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()

        if save:
            fig.savefig(self.output_dir / 'fig5_noether.png', dpi=300, bbox_inches='tight')
            fig.savefig(self.output_dir / 'fig5_noether.pdf', bbox_inches='tight')

        return fig

    def generate_all(self) -> None:
        """Generate all figures."""

        print("Generating Figure 1: Quantum-Discrete Isomorphism...")
        self.fig1_quantum_discrete_isomorphism()

        print("Generating Figure 2: Derivation Hierarchy...")
        self.fig2_derivation_hierarchy()

        print("Generating Figure 3: Measurement as Constraint Intersection...")
        self.fig3_constraint_intersection()

        print("Generating Figure 4: Self-Reference Theorem...")
        self.fig4_self_reference()

        print("Generating Figure 5: Noether/Conservation...")
        self.fig5_noether()

        print(f"\nAll figures saved to: {self.output_dir}")
        print("Formats: PNG (300 DPI) and PDF (vector)")


def main():
    parser = argparse.ArgumentParser(description='Generate Constraint Mathematics visualizations')
    parser.add_argument('--output', '-o', default='./figures', help='Output directory')
    parser.add_argument('--all', '-a', action='store_true', help='Generate all figures')
    parser.add_argument('--figure', '-f', type=int, help='Generate specific figure (1-5)')

    args = parser.parse_args()

    viz = ConstraintVisualization(args.output)

    if args.all or args.figure is None:
        viz.generate_all()
    elif args.figure:
        fig_methods = {
            1: viz.fig1_quantum_discrete_isomorphism,
            2: viz.fig2_derivation_hierarchy,
            3: viz.fig3_constraint_intersection,
            4: viz.fig4_self_reference,
            5: viz.fig5_noether,
        }
        if args.figure in fig_methods:
            fig_methods[args.figure]()
            print(f"Figure {args.figure} generated.")
        else:
            print(f"Invalid figure number. Choose 1-5.")


if __name__ == '__main__':
    main()
