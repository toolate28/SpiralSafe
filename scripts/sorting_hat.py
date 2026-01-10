#!/usr/bin/env python3
"""
scripts/sorting_hat.py
======================

Sorting Hat: A deterministic, auditable classifier that maps targets
(repo/agent/user/system) -> one of four "houses" using a compact
feature-vector -> 2-axis mapping, emitting a canonical QASm-like circuit.

Design Goals
------------
- Small, deterministic, testable surface for quick iteration
- Clear separation: feature extraction | axis mapping | angles | classifier | output
- Easy to replace stubs with real extractors (git, wave-toolkit, SpiralSafe API)
- Emit human-friendly explanation + QASm circuit for downstream systems
  (Minecraft plugin, Vera-Rubin emulator, ClaudeNPC) to consume

Usage
-----
    python -m scripts.sorting_hat sort-house --kind repo --name SpiralSafe
    python -m scripts.sorting_hat sort-house --kind agent --name "claude-npc:museum-guide"
    python -m scripts.sorting_hat sort-house --kind user --name iamto
    python -m scripts.sorting_hat sort-house --kind system --path C:/Repos/wave-toolkit

Integration Points
------------------
- command_center.py: Wire as subcommand via `add_sort_house_subparser()`
- Minecraft plugin: Parse QASm output, execute on Vera-Rubin circuit board
- ClaudeNPC: Narrate house assignment with personality-appropriate flair
- ATOM system: Log house assignments as coherence trail events

Architecture
------------
    +-----------------+     +----------------+     +---------------+
    | Feature         | --> | Axis Mapping   | --> | Angle Encoder |
    | Extraction      |     | (2D compact)   |     | (theta0, th1) |
    +-----------------+     +----------------+     +---------------+
            |                                              |
            v                                              v
    +------------------+                          +-----------------+
    | Stubbed/Real     |                          | Classifier      |
    | Data Sources     |                          | (4 quadrants)   |
    +------------------+                          +-----------------+
                                                          |
                                                          v
                                                  +-----------------+
                                                  | House Output +  |
                                                  | QASm Circuit    |
                                                  +-----------------+

Authors
-------
- iamto (Human Lead)
- HOPE (Claude Opus 4.5, Anthropic)

H&&S:WAVE - Collaborative handoff markers embedded
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple


# =============================================================================
# SECTION 1: House Definitions
# =============================================================================
# Each house maps to a 2-bit measurement outcome (q0, q1) from the 2-qubit
# sorting circuit. Houses encode archetypal project/agent/user orientations.

@dataclass(frozen=True)
class House:
    """Immutable house definition with semantic metadata."""
    key: str           # Canonical identifier (lowercase)
    id_bits: str       # Binary outcome from quantum measurement (2 bits)
    name: str          # Display name
    symbol: str        # Unicode symbol for visual flair
    desc: str          # One-line description
    strengths: List[str]  # What this house excels at
    color: str         # Hex color for visualizations


HOUSES: Dict[str, House] = {
    "rubin": House(
        key="rubin",
        id_bits="00",
        name="House Rubin",
        symbol="🔭",
        desc="Data-driven, observatory, rigorous, measurement-heavy.",
        strengths=["infra", "verification", "safety tooling", "observability"],
        color="#1E3A5F"  # Deep observatory blue
    ),
    "shannon": House(
        key="shannon",
        id_bits="01",
        name="House Shannon",
        symbol="📡",
        desc="Structure, compression, clean communication, protocols.",
        strengths=["APIs", "specs", "codecs", "glue code", "interface agents"],
        color="#2D5A27"  # Information green
    ),
    "noether": House(
        key="noether",
        id_bits="10",
        name="House Noether",
        symbol="🔮",
        desc="Invariants, symmetry, deep theory, refactorers.",
        strengths=["architecture", "libraries", "constraint systems", "mathematics"],
        color="#4A1A6B"  # Theoretical purple
    ),
    "firefly": House(
        key="firefly",
        id_bits="11",
        name="House Firefly",
        symbol="🌟",
        desc="Play, exploration, pedagogy, creative UX.",
        strengths=["museum builds", "stories", "interactive agents", "education"],
        color="#FF6B35"  # Creative orange
    ),
}


# =============================================================================
# SECTION 2: Feature Extraction (Stubbed)
# =============================================================================
# Replace these stubs with real extractors. Each extractor returns normalized
# features in [0, 1]. The stub uses deterministic pseudo-hash for testability.

@dataclass
class FeatureVector:
    """Normalized feature vector with semantic labels."""
    # Repo-style signals
    doc_code_coherence: float   # 1.0 = docs match code perfectly
    ci_health: float            # 1.0 = reliable CI, all tests pass
    change_entropy: float       # 1.0 = bursty/churny changes
    contributor_diversity: float  # 1.0 = many contributors (low bus factor)

    # Agent/user style signals
    risk_appetite: float        # 1.0 = explores, takes bold actions
    style_entropy: float        # 1.0 = high stylistic variation
    latency: float              # 1.0 = slower, more deliberate
    coherence: float            # 1.0 = internally consistent outputs

    def to_dict(self) -> Dict[str, float]:
        return {
            "doc_code_coherence": self.doc_code_coherence,
            "ci_health": self.ci_health,
            "change_entropy": self.change_entropy,
            "contributor_diversity": self.contributor_diversity,
            "risk_appetite": self.risk_appetite,
            "style_entropy": self.style_entropy,
            "latency": self.latency,
            "coherence": self.coherence,
        }


def _deterministic_hash(s: str) -> int:
    """Stable hash for reproducible stub values across runs."""
    return sum(ord(c) * (i + 1) for i, c in enumerate(s)) % 1000


def analyze_local_feature_signals(path_str: str) -> Dict[str, float]:
    """
    Extract partial feature signals from a local filesystem path.
    Returns a dict of found features (0.0 to 1.0) to override defaults.
    """
    p = Path(path_str)
    if not p.exists():
        return {}

    signals = {}
    
    # Heuristics for repo/structure
    has_readme = (p / "README.md").exists() or (p / "README.rst").exists()
    has_docs = (p / "docs").exists() or (p / "doc").exists()
    has_tests = (p / "tests").exists() or (p / "test").exists()
    has_ci = (p / ".github").exists() or (p / ".gitlab-ci.yml").exists()
    has_contributing = (p / "CONTRIBUTING.md").exists()
    
    # doc_code_coherence: High if docs + readme exist
    if has_readme and has_docs:
        signals["doc_code_coherence"] = 0.9
    elif has_readme:
        signals["doc_code_coherence"] = 0.6
    else:
        signals["doc_code_coherence"] = 0.2

    # ci_health: High if CI config or tests exist
    if has_ci and has_tests:
        signals["ci_health"] = 0.95
    elif has_ci or has_tests:
        signals["ci_health"] = 0.7
    else:
        signals["ci_health"] = 0.3

    # contributor_diversity: Proxy via governance docs
    if has_contributing:
        signals["contributor_diversity"] = 0.8
    else:
        signals["contributor_diversity"] = 0.4
        
    return signals


def stub_features_for(kind: str, name: str) -> FeatureVector:
    """
    Deterministic stub returning normalized features from pseudo-hash.
    
    If 'name' is a valid local path and kind is 'repo'/'system', 
    it attempts to extract real signals from the filesystem.

    Parameters
    ----------
    kind : str
        Target type: 'repo', 'agent', 'user', or 'system'
    name : str
        Target identifier (name or path)

    Returns
    -------
    FeatureVector
        Normalized features in [0, 1]
    """
    h = _deterministic_hash(f"{kind}:{name}")

    def bucket(offset: int) -> float:
        """Map hash to normalized bucket value."""
        return ((h + offset * 37) % 100) / 99.0

    # Default values from hash
    vals = {
        "doc_code_coherence": bucket(0),
        "ci_health": bucket(1),
        "change_entropy": bucket(2),
        "contributor_diversity": bucket(3),
        "risk_appetite": bucket(4),
        "style_entropy": bucket(5),
        "latency": bucket(6),
        "coherence": bucket(7),
    }

    # Override with real signals if applicable
    if kind in ("repo", "system"):
        real_signals = analyze_local_feature_signals(name)
        vals.update(real_signals)

    return FeatureVector(
        doc_code_coherence=vals["doc_code_coherence"],
        ci_health=vals["ci_health"],
        change_entropy=vals["change_entropy"],
        contributor_diversity=vals["contributor_diversity"],
        risk_appetite=vals["risk_appetite"],
        style_entropy=vals["style_entropy"],
        latency=vals["latency"],
        coherence=vals["coherence"],
    )


# H&&S:WAVE - Future: Wire real extractors here
# ---------------------------------------------
# def git_features_for(repo_path: Path) -> FeatureVector:
#     """Extract features from git history using wave-toolkit."""
#     pass
#
# def api_features_for(endpoint: str) -> FeatureVector:
#     """Fetch features from SpiralSafe API."""
#     pass


# =============================================================================
# SECTION 3: Axis Mapping
# =============================================================================
# Compress the 8-dimensional feature vector into 2 interpretable axes.
# This is the core "projection" step that enables the quantum encoding.

@dataclass
class CompactAxes:
    """Two normalized axes for quantum encoding."""
    rigor_play: float       # 1.0 = pure rigor, 0.0 = pure play
    structure_chaos: float  # 1.0 = structured, 0.0 = chaotic

    def __repr__(self) -> str:
        return f"CompactAxes(rigor_play={self.rigor_play:.4f}, structure_chaos={self.structure_chaos:.4f})"


def features_to_axes(f: FeatureVector) -> CompactAxes:
    """
    Project feature vector onto two interpretable axes.

    Axis 1: Rigor <-> Play
        - Rigor signals: doc_code_coherence, ci_health, coherence
        - Play signals: risk_appetite, inverse style_entropy

    Axis 2: Structure <-> Chaos
        - Structure signals: contributor_diversity, inverse change_entropy
        - Chaos signals: style_entropy, inverse ci_health

    The weights are tunable. Current values emphasize clear house separation.

    Parameters
    ----------
    f : FeatureVector
        Normalized feature vector

    Returns
    -------
    CompactAxes
        Two normalized axes in [0, 1]
    """
    # Rigor component (high coherence, high CI, high doc quality)
    rigor_score = (f.doc_code_coherence + f.ci_health + f.coherence) / 3.0

    # Play component (risk-taking, creative variation)
    play_score = (f.risk_appetite + (1.0 - f.style_entropy)) / 2.0

    # Combined axis: 1.0 = pure rigor
    rigor_play = (rigor_score * 0.7) + (play_score * 0.3)

    # Structure component (diverse contributors, steady changes)
    structure_score = (f.contributor_diversity + (1.0 - f.change_entropy)) / 2.0

    # Chaos component (high style entropy, low CI)
    chaos_score = (f.style_entropy + (1.0 - f.ci_health)) / 2.0

    # Combined axis: 1.0 = structured
    structure_chaos = (structure_score * 0.6) + ((1.0 - chaos_score) * 0.4)

    # Clamp to valid range
    rigor_play = max(0.0, min(1.0, rigor_play))
    structure_chaos = max(0.0, min(1.0, structure_chaos))

    return CompactAxes(rigor_play, structure_chaos)


# =============================================================================
# SECTION 4: Angle Encoding (Quantum Preparation)
# =============================================================================
# Map compact axes to rotation angles for the parameterized quantum circuit.
# This is the "encoder" step that prepares qubit states.

@dataclass
class EncodedAngles:
    """Rotation angles for the 2-qubit sorting circuit."""
    theta0: float  # Rotation angle for qubit 0 (radians, 0..pi)
    theta1: float  # Rotation angle for qubit 1 (radians, 0..pi)

    def __repr__(self) -> str:
        return f"EncodedAngles(theta0={self.theta0:.6f}, theta1={self.theta1:.6f})"


def axes_to_angles(axes: CompactAxes) -> EncodedAngles:
    """
    Map normalized axes to rotation angles for RZ gates.

    Encoding: theta = pi * axis_value
    This maps [0, 1] -> [0, pi] radians for single-qubit RZ rotations.

    Parameters
    ----------
    axes : CompactAxes
        Normalized 2D axes

    Returns
    -------
    EncodedAngles
        Rotation angles in radians
    """
    theta0 = math.pi * axes.rigor_play
    theta1 = math.pi * axes.structure_chaos
    return EncodedAngles(theta0, theta1)


# =============================================================================
# SECTION 5: Classical Classifier (Reference Implementation)
# =============================================================================
# Deterministic mapping from angles to house. This mirrors the quantum
# measurement outcome under the simple threshold model.

def classify_from_angles(angles: EncodedAngles) -> str:
    """
    Classify angles into one of four houses.

    This is the classical reference implementation. The quantum version
    would measure the 2-qubit state after applying the sorting circuit,
    yielding probabilistic outcomes that match this deterministic rule
    when the input is well-separated.

    Classification Rule:
        - Threshold at pi/2 (midpoint of [0, pi])
        - bit0 = 1 if theta0 >= pi/2, else 0
        - bit1 = 1 if theta1 >= pi/2, else 0
        - House = lookup by (bit0, bit1)

    Parameters
    ----------
    angles : EncodedAngles
        Rotation angles from the encoder

    Returns
    -------
    str
        House key ('rubin', 'shannon', 'noether', 'firefly')
    """
    threshold = math.pi / 2.0

    bit0 = 1 if angles.theta0 >= threshold else 0
    bit1 = 1 if angles.theta1 >= threshold else 0

    outcome = (bit0, bit1)
    house_map = {
        (0, 0): "rubin",
        (0, 1): "shannon",
        (1, 0): "noether",
        (1, 1): "firefly",
    }

    return house_map[outcome]


# =============================================================================
# SECTION 6: QASm Circuit Emitter
# =============================================================================
# Generate canonical QASm-like circuit for downstream systems.
# Compliant with protocol/QUANTUM_CIRCUITS_SPEC.md

def qasm_for_sorting(angles: EncodedAngles) -> str:
    """
    Emit the canonical Sorting Hat quantum circuit in QASm format.

    This circuit can be executed by:
        - SpiralCraft Minecraft plugin (Vera-Rubin emulator)
        - Python quantum simulators
        - Real quantum hardware (with appropriate transpilation)

    Circuit Structure:
        1. RESET both qubits to |0>
        2. Apply Hadamard to create superposition
        3. Apply parameterized RZ rotations (the "encoding" step)
        4. Entangle with CNOT
        5. Measure both qubits

    Parameters
    ----------
    angles : EncodedAngles
        Rotation angles for the RZ gates

    Returns
    -------
    str
        Multi-line QASm-like circuit string
    """
    lines = [
        "# ============================================",
        "# Sorting Hat Circuit (SpiralSafe QASm v0.1)",
        "# ============================================",
        "# Compliant with: protocol/QUANTUM_CIRCUITS_SPEC.md",
        f"# Parameters: theta0={angles.theta0:.6f}, theta1={angles.theta1:.6f}",
        "#",
        "# Initialize register",
        "RESET 0",
        "RESET 1",
        "",
        "# Create superposition (uniform prior)",
        "H 0",
        "H 1",
        "",
        "# Apply parameterized rotations (encode features)",
        f"RZ 0 {angles.theta0:.6f}",
        f"RZ 1 {angles.theta1:.6f}",
        "",
        "# Entangle (correlate axes)",
        "CNOT 0 1",
        "",
        "# Collapse to house (measurement)",
        "MEASURE 0",
        "MEASURE 1",
        "# ============================================",
    ]
    return "\n".join(lines)


# =============================================================================
# SECTION 7: JSON Output for API/Integration
# =============================================================================
# Structured output format for SpiralSafe API and Minecraft plugin.

def result_to_json(
    kind: str,
    name: str,
    features: FeatureVector,
    axes: CompactAxes,
    angles: EncodedAngles,
    house: House,
) -> Dict:
    """
    Build structured JSON result for API responses and logging.

    Returns
    -------
    Dict
        Complete sorting result with all intermediate values
    """
    return {
        "version": "0.1.0",
        "target": {
            "kind": kind,
            "name": name,
        },
        "features": features.to_dict(),
        "axes": {
            "rigor_play": axes.rigor_play,
            "structure_chaos": axes.structure_chaos,
        },
        "angles": {
            "theta0": angles.theta0,
            "theta1": angles.theta1,
        },
        "house": {
            "key": house.key,
            "id_bits": house.id_bits,
            "name": house.name,
            "symbol": house.symbol,
            "desc": house.desc,
            "strengths": house.strengths,
            "color": house.color,
        },
    }


# =============================================================================
# SECTION 8: CLI Output Formatting (Dynamic Terminal)
# =============================================================================
# Dynamic, animated terminal output with colors and progressive reveal.

import time
import random

# ANSI color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # House colors
    RUBIN = "\033[38;2;30;58;95m"      # Deep blue
    SHANNON = "\033[38;2;45;90;39m"    # Green
    NOETHER = "\033[38;2;74;26;107m"   # Purple
    FIREFLY = "\033[38;2;255;107;53m"  # Orange

    # UI colors
    CYAN = "\033[36m"
    YELLOW = "\033[33m"
    GREEN = "\033[32m"
    MAGENTA = "\033[35m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"


HOUSE_COLORS = {
    "rubin": Colors.CYAN,
    "shannon": Colors.GREEN,
    "noether": Colors.MAGENTA,
    "firefly": Colors.YELLOW,
}


def _clear_line():
    """Clear the current line."""
    print("\r\033[K", end="", flush=True)


def _spinner(message: str, duration: float = 0.5, frames: str = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"):
    """Show animated spinner."""
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{Colors.CYAN}{frames[i % len(frames)]}{Colors.RESET} {message}", end="", flush=True)
        time.sleep(0.08)
        i += 1
    _clear_line()


def _typing(text: str, delay: float = 0.02):
    """Typing effect for text."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def _progress_bar(label: str, value: float, width: int = 30, color: str = Colors.CYAN):
    """Animated progress bar."""
    filled = int(value * width)
    for i in range(filled + 1):
        bar = "█" * i + "░" * (width - i)
        pct = (i / width) * 100
        print(f"\r  {Colors.DIM}{label:<20}{Colors.RESET} {color}[{bar}]{Colors.RESET} {pct:5.1f}%", end="", flush=True)
        time.sleep(0.015)
    print()


def _dramatic_reveal(house: House):
    """Dramatic house reveal animation."""
    color = HOUSE_COLORS.get(house.key, Colors.WHITE)

    # Suspense dots
    print(f"\n{Colors.DIM}  Analyzing quantum amplitudes", end="", flush=True)
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print(Colors.RESET)

    time.sleep(0.2)

    # The reveal
    print()
    print(f"  {Colors.BOLD}{color}╔══════════════════════════════════════════════════════════╗{Colors.RESET}")
    time.sleep(0.1)
    print(f"  {Colors.BOLD}{color}║{Colors.RESET}                                                          {Colors.BOLD}{color}║{Colors.RESET}")
    time.sleep(0.1)

    # House name with symbol - centered
    house_line = f"{house.symbol}  {house.name.upper()}  {house.symbol}"
    padding = (58 - len(house_line)) // 2
    print(f"  {Colors.BOLD}{color}║{' ' * padding}{house_line}{' ' * (58 - padding - len(house_line))}║{Colors.RESET}")
    time.sleep(0.1)

    print(f"  {Colors.BOLD}{color}║{Colors.RESET}                                                          {Colors.BOLD}{color}║{Colors.RESET}")
    time.sleep(0.1)
    print(f"  {Colors.BOLD}{color}╚══════════════════════════════════════════════════════════╝{Colors.RESET}")
    print()


def format_result_dynamic(
    kind: str,
    name: str,
    features: FeatureVector,
    axes: CompactAxes,
    angles: EncodedAngles,
    house: House,
    animate: bool = True,
) -> None:
    """
    Dynamic animated terminal output.

    Includes spinners, progress bars, and dramatic reveal.
    Set animate=False for static output (e.g., piped to file).
    """
    color = HOUSE_COLORS.get(house.key, Colors.WHITE)

    if not animate:
        # Fall back to static output
        print(format_result_for_terminal(kind, name, features, axes, angles, house))
        return

    # Header
    print()
    print(f"  {Colors.BOLD}{Colors.WHITE}┌──────────────────────────────────────────────────────────┐{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.WHITE}│{Colors.RESET}  {Colors.CYAN}🎩 SORTING HAT{Colors.RESET}                                         {Colors.BOLD}{Colors.WHITE}│{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.WHITE}│{Colors.RESET}  {Colors.DIM}Quantum Archetypal Classifier v0.1{Colors.RESET}                    {Colors.BOLD}{Colors.WHITE}│{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.WHITE}└──────────────────────────────────────────────────────────┘{Colors.RESET}")
    print()

    # Target info
    _spinner("Loading target profile", 0.4)
    print(f"  {Colors.DIM}Target:{Colors.RESET} {Colors.BOLD}{kind}{Colors.RESET} → {Colors.CYAN}{name}{Colors.RESET}")
    print()

    # Feature extraction
    _spinner("Extracting feature vector", 0.5)
    print(f"  {Colors.DIM}Feature Vector (8 dimensions):{Colors.RESET}")

    for key, val in list(features.to_dict().items())[:4]:
        _progress_bar(key.replace("_", " "), val, 25, Colors.CYAN)
        time.sleep(0.05)

    print(f"  {Colors.DIM}  ... +4 more features{Colors.RESET}")
    print()

    # Axis projection
    _spinner("Projecting to 2D axes", 0.4)
    print(f"  {Colors.DIM}Compact Axes:{Colors.RESET}")
    _progress_bar("Rigor ↔ Play", axes.rigor_play, 30, Colors.YELLOW)
    _progress_bar("Structure ↔ Chaos", axes.structure_chaos, 30, Colors.MAGENTA)
    print()

    # Quantum encoding
    _spinner("Encoding rotation angles", 0.3)
    print(f"  {Colors.DIM}Quantum Parameters:{Colors.RESET}")
    print(f"    θ₀ = {Colors.CYAN}{angles.theta0:.6f}{Colors.RESET} rad")
    print(f"    θ₁ = {Colors.CYAN}{angles.theta1:.6f}{Colors.RESET} rad")
    print()

    # Circuit execution
    _spinner("Executing quantum circuit", 0.6)
    print(f"  {Colors.DIM}Circuit:{Colors.RESET} H⊗H → RZ(θ₀)⊗RZ(θ₁) → CNOT → MEASURE")
    print()

    # Measurement
    _spinner("Collapsing wavefunction", 0.4)
    print(f"  {Colors.DIM}Measurement outcome:{Colors.RESET} |{Colors.BOLD}{house.id_bits}{Colors.RESET}⟩")

    # Dramatic reveal
    _dramatic_reveal(house)

    # House details
    print(f"  {Colors.DIM}{house.desc}{Colors.RESET}")
    print()
    print(f"  {Colors.DIM}Strengths:{Colors.RESET}")
    for s in house.strengths:
        print(f"    {color}•{Colors.RESET} {s}")
    print()


def format_result_for_terminal(
    kind: str,
    name: str,
    features: FeatureVector,
    axes: CompactAxes,
    angles: EncodedAngles,
    house: House,
) -> str:
    """
    Static format for non-TTY output (piping, files).

    Uses box-drawing characters for visual clarity.
    Optimized for L->R, T->B reading flow.
    """
    width = 60

    lines = [
        "",
        f"╔{'═' * width}╗",
        f"║{'SORTING HAT RESULT':^{width}}║",
        f"╠{'═' * width}╣",
        f"║ {house.symbol} {house.name:<{width - 5}} ║",
        f"║   {house.desc:<{width - 6}} ║",
        f"╠{'═' * width}╣",
        f"║ {'TARGET':<{width - 2}} ║",
        f"║   Kind: {kind:<{width - 11}} ║",
        f"║   Name: {name:<{width - 11}} ║",
        f"╠{'═' * width}╣",
        f"║ {'COMPACT AXES':<{width - 2}} ║",
        f"║   Rigor ↔ Play:      {axes.rigor_play:>6.4f}  [{'█' * int(axes.rigor_play * 20):<20}] ║",
        f"║   Structure ↔ Chaos: {axes.structure_chaos:>6.4f}  [{'█' * int(axes.structure_chaos * 20):<20}] ║",
        f"╠{'═' * width}╣",
        f"║ {'ENCODER ANGLES (radians)':<{width - 2}} ║",
        f"║   θ₀ (q0): {angles.theta0:>10.6f}  │  θ₁ (q1): {angles.theta1:>10.6f}{' ' * 13} ║",
        f"╠{'═' * width}╣",
        f"║ {'HOUSE STRENGTHS':<{width - 2}} ║",
    ]

    for strength in house.strengths:
        lines.append(f"║   • {strength:<{width - 7}} ║")

    lines.extend([
        f"╚{'═' * width}╝",
        "",
    ])

    return "\n".join(lines)


def format_features_table(features: FeatureVector) -> str:
    """Format feature vector as readable table."""
    lines = [
        "┌────────────────────────┬─────────┬──────────────────────┐",
        "│ Feature                │  Value  │ Bar                  │",
        "├────────────────────────┼─────────┼──────────────────────┤",
    ]

    for key, val in features.to_dict().items():
        bar = "█" * int(val * 18)
        lines.append(f"│ {key:<22} │ {val:>6.4f} │ {bar:<20} │")

    lines.append("└────────────────────────┴─────────┴──────────────────────┘")
    return "\n".join(lines)


# =============================================================================
# SECTION 9: CLI Handler
# =============================================================================

def cmd_sort_house(args: argparse.Namespace) -> int:
    """
    CLI handler for the sort-house subcommand.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments with 'kind', 'name', 'path', 'json', 'static' flags

    Returns
    -------
    int
        Exit code (0 = success, non-zero = error)
    """
    # Determine target name
    target_name = args.name or args.path
    if not target_name:
        print("ERROR: Please provide --name or --path for the target.", file=sys.stderr)
        return 2

    # Step 1: Extract features (stubbed for now)
    features = stub_features_for(args.kind, target_name)

    # Step 2: Map to compact axes
    axes = features_to_axes(features)

    # Step 3: Encode as rotation angles
    angles = axes_to_angles(axes)

    # Step 4: Classify
    house_key = classify_from_angles(angles)
    house = HOUSES[house_key]

    # Step 5: Output
    if hasattr(args, 'json') and args.json:
        # JSON mode for API integration
        result = result_to_json(args.kind, target_name, features, axes, angles, house)
        print(json.dumps(result, indent=2))
    elif hasattr(args, 'static') and args.static:
        # Static mode (no animation)
        print(format_result_for_terminal(args.kind, target_name, features, axes, angles, house))
        print("\nFEATURE VECTOR:")
        print(format_features_table(features))
        print("\nQASM CIRCUIT:")
        print(qasm_for_sorting(angles))
    else:
        # Dynamic animated output (default)
        import sys as _sys
        animate = _sys.stdout.isatty()  # Only animate if terminal
        format_result_dynamic(args.kind, target_name, features, axes, angles, house, animate=animate)
        if not animate:
            print("\nQASM CIRCUIT:")
            print(qasm_for_sorting(angles))

    return 0


# =============================================================================
# SECTION 10: CLI Parser
# =============================================================================

def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="python -m scripts.sorting_hat",
        description=(
            "Sorting Hat: Classify repos, agents, users, and systems into "
            "one of four houses (Rubin, Shannon, Noether, Firefly) based on "
            "their feature profiles. Emits both human-readable results and "
            "canonical QASm circuits for downstream integration."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m scripts.sorting_hat sort-house --kind repo --name SpiralSafe
  python -m scripts.sorting_hat sort-house --kind agent --name claude-npc:museum-guide
  python -m scripts.sorting_hat sort-house --kind user --name iamto --json

Houses:
  rubin    (00)  Data-driven, observatory, rigorous
  shannon  (01)  Structure, compression, protocols
  noether  (10)  Invariants, symmetry, deep theory
  firefly  (11)  Play, exploration, pedagogy

For more information: protocol/SORTING_HAT_SPEC.md
        """,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # sort-house subcommand
    p_sort = subparsers.add_parser(
        "sort-house",
        help="Sort a target into one of four houses.",
        description="Classify a target and emit house assignment with QASm circuit.",
    )
    p_sort.add_argument(
        "--kind",
        choices=["repo", "agent", "user", "system"],
        required=True,
        help="Target type to classify.",
    )
    p_sort.add_argument(
        "--name",
        help="Name identifier (e.g., 'SpiralSafe', 'claude-npc:museum-guide').",
    )
    p_sort.add_argument(
        "--path",
        help="Filesystem path for repo/system targets (alternative to --name).",
    )
    p_sort.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON for API integration.",
    )
    p_sort.add_argument(
        "--static",
        action="store_true",
        help="Disable animations (static output).",
    )
    p_sort.set_defaults(func=cmd_sort_house)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    func = getattr(args, "func", None)
    if func is None:
        parser.print_help(sys.stderr)
        return 1

    return func(args)


# =============================================================================
# SECTION 11: Integration Helpers
# =============================================================================
# Functions for wiring into command_center.py

def add_sort_house_subparser(subparsers) -> None:
    """
    Add sort-house subcommand to an existing argparse subparsers object.

    Usage in command_center.py:
        from scripts.sorting_hat import add_sort_house_subparser
        add_sort_house_subparser(subparsers)
    """
    p = subparsers.add_parser(
        "sort-house",
        help="Sort a target into one of four houses (Rubin, Shannon, Noether, Firefly).",
    )
    p.add_argument("--kind", choices=["repo", "agent", "user", "system"], required=True)
    p.add_argument("--name", help="Name identifier for the target.")
    p.add_argument("--path", help="Filesystem path (alternative to --name).")
    p.add_argument("--json", action="store_true", help="Output as JSON.")
    p.set_defaults(func=cmd_sort_house)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    raise SystemExit(main())
