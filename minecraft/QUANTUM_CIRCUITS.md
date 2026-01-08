# 🔮 SpiralCraft: Quantum Circuits & Computing

**Version**: 1.1.0-circuits
**Extension**: Quantum computing in Minecraft via redstone
**Purpose**: Build actual quantum algorithms in-game

---

## Quantum Circuit System

### Overview

SpiralCraft adds **quantum logic gates** as redstone components. Players can build actual quantum circuits that manipulate qubit superpositions, create entanglement, and run quantum algorithms—all visualized in Minecraft.

```
┌─────────────────────────────────────────────────────────┐
│              Quantum Circuit Building                    │
│                                                           │
│  Input Qubits  →  Gates  →  Measurements  →  Output     │
│                                                           │
│     |0⟩ + |1⟩  →   H    →      ■          →    Result   │
│                   CNOT        Measure                     │
└─────────────────────────────────────────────────────────┘
```

---

## Quantum Blocks

### 1. Qubit Block

**Appearance**: Glowing cyan/purple sphere with rotating particles

**States**:
- `|0⟩` - Ground state (cyan glow)
- `|1⟩` - Excited state (purple glow)
- `α|0⟩ + β|1⟩` - Superposition (both colors shimmering)

**Crafting**:
```
[Quantum Crystal] [Observer] [Quantum Crystal]
[Redstone]        [Diamond]  [Redstone]
[Quantum Crystal] [Observer] [Quantum Crystal]
```

**Properties**:
```java
public class QubitBlock {
  private Complex alpha;  // Amplitude of |0⟩
  private Complex beta;   // Amplitude of |1⟩
  private boolean measured;
  private List<QubitBlock> entangledWith;

  public QubitState getState() {
    if (measured) {
      return collapsed ? QubitState.ONE : QubitState.ZERO;
    }
    return QubitState.SUPERPOSITION;
  }

  public void applyGate(QuantumGate gate) {
    Matrix2x2 gateMatrix = gate.getMatrix();
    Complex[] stateVector = {alpha, beta};
    Complex[] newState = gateMatrix.multiply(stateVector);

    this.alpha = newState[0];
    this.beta = newState[1];

    // Sync with SpiralSafe API
    spiralSafeAPI.logQuantumOperation("gate_applied", gate.getName(), this.getCoherenceScore());
  }

  public boolean measure() {
    if (measured) return collapsed;

    // Collapse wavefunction
    double probZero = alpha.magnitudeSquared();
    this.collapsed = Math.random() > probZero;
    this.measured = true;

    // Collapse all entangled qubits
    for (QubitBlock entangled : entangledWith) {
      entangled.collapseFrom(this);
    }

    return collapsed;
  }
}
```

### 2. Quantum Gates (Redstone Components)

#### Hadamard Gate (H)

**Function**: Creates equal superposition
**Matrix**:
```
H = 1/√2 [ 1   1 ]
         [ 1  -1 ]
```

**Effect**: `|0⟩ → (|0⟩ + |1⟩)/√2`

**Crafting**:
```
[Redstone] [Quantum Crystal] [Redstone]
[Observer] [Diamond Block]   [Observer]
[Redstone] [Quantum Crystal] [Redstone]
```

**Visual**: Yellow cube with rotating "H" symbol

**Behavior**: When qubit passes through (via hopper or pipe), apply Hadamard transformation

#### CNOT Gate (Controlled-NOT)

**Function**: Entangles two qubits
**Matrix**:
```
CNOT = [ 1  0  0  0 ]
       [ 0  1  0  0 ]
       [ 0  0  0  1 ]
       [ 0  0  1  0 ]
```

**Effect**: Flips target if control is |1⟩

**Crafting**:
```
[Quantum Crystal] [Comparator] [Quantum Crystal]
[Redstone]        [Diamond]    [Redstone]
[Quantum Crystal] [Comparator] [Quantum Crystal]
```

**Visual**: Two-block structure with control (top) and target (bottom)

**Behavior**:
```java
public void applyCNOT(QubitBlock control, QubitBlock target) {
  // Create entanglement
  control.entangleWith(target);
  target.entangleWith(control);

  // Apply CNOT transformation
  Complex c0_t0 = control.alpha.multiply(target.alpha);
  Complex c0_t1 = control.alpha.multiply(target.beta);
  Complex c1_t0 = control.beta.multiply(target.beta);  // Flipped!
  Complex c1_t1 = control.beta.multiply(target.alpha); // Flipped!

  // Update amplitudes
  // (Complex 2-qubit state management)
}
```

#### Phase Gate (P)

**Function**: Adds relative phase
**Matrix**:
```
P(θ) = [ 1      0    ]
       [ 0   e^(iθ)  ]
```

**Effect**: `|1⟩ → e^(iθ)|1⟩`

**Crafting**:
```
[Glowstone] [Quantum Crystal] [Glowstone]
[Redstone]  [Ender Pearl]     [Redstone]
[Glowstone] [Quantum Crystal] [Glowstone]
```

**Visual**: Purple cube with rotating phase angle dial

**Behavior**: Right-click to adjust phase angle (0° to 360°)

#### Pauli Gates (X, Y, Z)

**X Gate (NOT)**:
```
X = [ 0  1 ]
    [ 1  0 ]
```
Effect: Bit flip (|0⟩ ↔ |1⟩)

**Y Gate**:
```
Y = [ 0  -i ]
    [ i   0 ]
```
Effect: Bit flip + phase flip

**Z Gate**:
```
Z = [ 1   0 ]
    [ 0  -1 ]
```
Effect: Phase flip (|1⟩ → -|1⟩)

### 3. Measurement Block

**Appearance**: Gold block with redstone comparator on top

**Function**: Collapses qubit superposition to |0⟩ or |1⟩

**Crafting**:
```
[Observer] [Redstone] [Observer]
[Gold]     [Diamond]  [Gold]
[Observer] [Redstone] [Observer]
```

**Behavior**:
```java
public class MeasurementBlock {
  public void measure(QubitBlock qubit) {
    boolean result = qubit.measure();

    // Output redstone signal based on result
    if (result) {
      // |1⟩ measured → Redstone ON (power 15)
      this.setPowered(true);
    } else {
      // |0⟩ measured → Redstone OFF (power 0)
      this.setPowered(false);
    }

    // Visual feedback
    spawnParticles(result ? ParticleEffect.PURPLE_FLAME : ParticleEffect.CYAN_SPARKLE);

    // Log to SpiralSafe
    spiralSafeAPI.logQuantumMeasurement(qubit.getId(), result, qubit.getCoherenceScore());
  }
}
```

### 4. Quantum Circuit Board

**Appearance**: Large flat block (like a crafting table) with grid overlay

**Function**: Visual circuit builder UI

**UI**:
```
┌────────────────────────────────────────┐
│   Quantum Circuit Designer             │
├────────────────────────────────────────┤
│                                         │
│  Qubit 1:  |0⟩ ─[H]─●─────[M] → ?     │
│                     │                   │
│  Qubit 2:  |0⟩ ────X─[H]─[M] → ?     │
│                                         │
│  [Run Circuit]  [Clear]  [Save]        │
│                                         │
│  Coherence: ████████░░ 83%             │
│  Entanglement: Yes (Q1 ↔ Q2)           │
└────────────────────────────────────────┘
```

**Behavior**: Right-click to open GUI, drag gates onto qubits, run circuit

---

## Quantum Algorithms

### 1. Bell State Creator

**Circuit**:
```
Q1: |0⟩ ─[H]─●─[M]
Q2: |0⟩ ─────X─[M]
```

**Effect**: Creates maximally entangled state (|00⟩ + |11⟩)/√2

**In-Game**:
```java
public void createBellState() {
  QubitBlock q1 = new QubitBlock(); // |0⟩
  QubitBlock q2 = new QubitBlock(); // |0⟩

  // Apply Hadamard to Q1
  q1.applyGate(QuantumGate.HADAMARD);

  // Apply CNOT (Q1 control, Q2 target)
  applyCNOT(q1, q2);

  // Now q1 and q2 are entangled!
  // Measuring q1 instantly determines q2's state
}
```

**Quest**: "Quantum Entanglement 101"
- Build Bell state circuit
- Measure 100 times
- Verify correlation (should see 50% |00⟩, 50% |11⟩, never |01⟩ or |10⟩)
- Reward: Entanglement Master title + coherence boost

### 2. Quantum Teleportation

**Circuit**:
```
Q1 (Alice): |ψ⟩ ─[Bell]─[M]───────────────
Q2 (Shared):|0⟩ ─[Bell]─[M]─●───────────
Q3 (Bob):   |0⟩ ───────────X─[Z?]─[X?]─
```

**Effect**: Teleports quantum state from Q1 to Q3 using entanglement

**In-Game Implementation**:
```java
public void quantumTeleport(QubitBlock psi, Location bobLocation) {
  // 1. Create Bell pair between Alice and Bob
  QubitBlock alice = new QubitBlock();
  QubitBlock bob = new QubitBlock();
  createBellState(alice, bob);

  // 2. Alice entangles her qubit with the Bell pair
  applyCNOT(psi, alice);
  psi.applyGate(QuantumGate.HADAMARD);

  // 3. Alice measures both qubits
  boolean m1 = psi.measure();
  boolean m2 = alice.measure();

  // 4. Send classical bits to Bob (via BUMP marker!)
  BumpMarker teleportBump = spiralSafeAPI.createBump(
    "PASS",
    "alice_dimension",
    "bob_dimension",
    "quantum_teleport",
    new HashMap<>() {{
      put("m1", m1);
      put("m2", m2);
    }}
  );

  // 5. Bob applies corrections based on measurements
  if (m2) bob.applyGate(QuantumGate.PAULI_X);
  if (m1) bob.applyGate(QuantumGate.PAULI_Z);

  // Bob's qubit now has the original state!
  teleportQubitVisual(bob, bobLocation);
}
```

**Quest**: "Quantum Courier"
- Set up teleportation circuit across two BUMP portals
- Teleport 10 different quantum states successfully
- Reward: Portal Entangler (allows quantum teleportation of items)

### 3. Grover's Search

**Purpose**: Quantum database search (finds item in unsorted list in √N time)

**Circuit** (simplified 2-qubit):
```
Q1: |0⟩ ─[H]─[Oracle]─[Diffusion]─[M]
Q2: |0⟩ ─[H]─[Oracle]─[Diffusion]─[M]
```

**In-Game**:
```java
public int groverSearch(List<Item> database, Item target) {
  int n = (int) Math.ceil(Math.log(database.size()) / Math.log(2));
  QubitBlock[] qubits = new QubitBlock[n];

  // Initialize superposition
  for (QubitBlock q : qubits) {
    q.applyGate(QuantumGate.HADAMARD);
  }

  // Grover iterations (√N times)
  int iterations = (int) Math.sqrt(database.size());
  for (int i = 0; i < iterations; i++) {
    // Oracle: marks target item
    applyOracle(qubits, target);

    // Diffusion: amplifies marked amplitude
    applyDiffusion(qubits);
  }

  // Measure
  int index = measureQubits(qubits);
  return index;
}
```

**Quest**: "Quantum Archaeologist"
- Build Grover circuit
- Search for hidden treasure in 16-item chest array
- Prove it's faster than linear search
- Reward: Quantum Compass (finds nearest ore using Grover's algorithm)

### 4. Quantum Random Number Generator (QRNG)

**Circuit**:
```
Q1: |0⟩ ─[H]─[M] → Random bit
```

**In-Game**:
```java
public boolean quantumRandomBit() {
  QubitBlock q = new QubitBlock();
  q.applyGate(QuantumGate.HADAMARD);
  return q.measure(); // 50% |0⟩, 50% |1⟩ (truly random!)
}

public int quantumRandomInt(int bits) {
  int result = 0;
  for (int i = 0; i < bits; i++) {
    if (quantumRandomBit()) {
      result |= (1 << i);
    }
  }
  return result;
}
```

**Application**: Loot table RNG, world generation, quantum lottery

**Quest**: "Entropy Master"
- Generate 1000 quantum random numbers
- Verify statistical randomness (chi-squared test)
- Reward: Quantum Dice (unbreakable RNG tool)

---

## Quantum Visualizers

### 1. Bloch Sphere Projector

**Appearance**: Obsidian pedestal with rotating holographic sphere

**Function**: Displays qubit state on Bloch sphere

**Visual**:
```
       |0⟩ (North Pole)
         ↑
         |
    ←─────────→ X-axis
         |
         ↓
       |1⟩ (South Pole)
```

**Rendering**:
```java
public void renderBlochSphere(QubitBlock qubit) {
  // Calculate Bloch vector
  double theta = 2 * Math.acos(qubit.alpha.magnitude());
  double phi = qubit.beta.phase() - qubit.alpha.phase();

  // 3D coordinates
  double x = Math.sin(theta) * Math.cos(phi);
  double y = Math.sin(theta) * Math.sin(phi);
  double z = Math.cos(theta);

  // Spawn particle at location
  Location center = this.getLocation().add(0.5, 2, 0.5);
  Location point = center.add(x, z, y); // Y is up in Minecraft

  // Different colors for different states
  Particle particle = getParticleForState(qubit);
  point.getWorld().spawnParticle(particle, point, 5);

  // Spawn axis lines
  spawnAxisLines(center);
}
```

**Interaction**: Place qubit on pedestal, see its state visualized in 3D

### 2. Entanglement Web

**Appearance**: Particle beams connecting entangled qubits

**Visual Effect**:
```
Qubit A ◉━━━━━━━━━━◉ Qubit B
         ╲        ╱
          ╲      ╱
           ◉━━◉
          Qubit C
```

**Rendering**:
```java
public void renderEntanglementWeb() {
  List<QubitBlock> entangled = getEntangledQubits();

  for (int i = 0; i < entangled.size(); i++) {
    for (int j = i + 1; j < entangled.size(); j++) {
      QubitBlock q1 = entangled.get(i);
      QubitBlock q2 = entangled.get(j);

      // Draw particle beam between them
      drawParticleLine(
        q1.getLocation(),
        q2.getLocation(),
        Particle.END_ROD,
        getEntanglementStrength(q1, q2)
      );
    }
  }
}
```

**Effect**: Visual feedback showing which qubits are entangled

### 3. Quantum State Analyzer

**Appearance**: Diamond block with redstone dust patterns

**Function**: Displays detailed qubit statistics

**UI**:
```
┌────────────────────────────────────────┐
│   Quantum State Analyzer               │
├────────────────────────────────────────┤
│                                         │
│  Qubit ID: Q_abc123                    │
│                                         │
│  State Vector:                          │
│    α|0⟩: 0.707 + 0.000i                │
│    β|1⟩: 0.707 + 0.000i                │
│                                         │
│  Probabilities:                         │
│    P(|0⟩): ████████░░ 50.0%            │
│    P(|1⟩): ████████░░ 50.0%            │
│                                         │
│  Entanglement:                          │
│    Yes → [Q_def456, Q_ghi789]          │
│                                         │
│  Coherence: ████████░░ 87%             │
│  Phase: 0.000 rad (0°)                 │
│                                         │
│  [Measure] [Clone*] [Teleport]         │
│                                         │
│  *Cannot clone due to no-cloning       │
│   theorem! (Shows error message)       │
└────────────────────────────────────────┘
```

---

## Quantum Computing Lab

### Lab Structure

**Build Requirements**:
- 16x16 obsidian platform
- Beacon at center (provides "Quantum Stability" buff)
- 4 Quantum Circuit Boards at corners
- Bloch Sphere Projector at center
- Coherence Amplifier (diamond block + 4 quantum crystals)

**Lab Benefits**:
- +20% coherence in lab area
- Qubits maintain superposition longer
- Reduced measurement noise
- Access to advanced gates (Toffoli, Fredkin)

**Quest**: "Quantum Architect"
- Build a complete quantum lab
- Set up 8-qubit quantum computer
- Run Shor's algorithm (factor number 15 = 3 × 5)
- Reward: ARCHON authority + "Quantum Architect" title

---

## Advanced Features

### Quantum Error Correction

**Problem**: Coherence decays over time, introducing errors

**Solution**: 3-qubit bit flip code

**Circuit**:
```
Data:   |ψ⟩ ─●─●───────────[Error]─────────●─●─[M]
Ancilla1: |0⟩ ─X─┼───────────────────────────X─┼─[M]
Ancilla2: |0⟩ ───X───────────────────────────── X─[M]
```

**In-Game**:
```java
public QubitBlock errorCorrection(QubitBlock data) {
  // Encode: create 3-qubit state
  QubitBlock a1 = new QubitBlock();
  QubitBlock a2 = new QubitBlock();
  applyCNOT(data, a1);
  applyCNOT(data, a2);

  // Simulate error (coherence decay)
  if (Math.random() < 0.1) {
    data.applyGate(QuantumGate.PAULI_X); // Bit flip error
  }

  // Detect and correct
  applyCNOT(data, a1);
  applyCNOT(data, a2);
  boolean s1 = a1.measure();
  boolean s2 = a2.measure();

  // Syndrome indicates which qubit has error
  if (s1 && !s2) data.applyGate(QuantumGate.PAULI_X);
  else if (!s1 && s2) a1.applyGate(QuantumGate.PAULI_X);
  else if (s1 && s2) a2.applyGate(QuantumGate.PAULI_X);

  return data; // Corrected!
}
```

### Quantum Fourier Transform (QFT)

**Purpose**: Basis change for period finding (used in Shor's algorithm)

**Circuit** (3-qubit):
```
Q1: ─[H]─[P(π/2)]─[P(π/4)]─[SWAP]─
Q2: ─────●────────[H]──────[P(π/2)]─[SWAP]─
Q3: ──────────────●───────●─────────[H]────
```

**Application**: Phase estimation, Shor's factoring, quantum simulation

---

## SpiralSafe API Integration

### Log Quantum Operations

```java
public void logQuantumOperation(String operation, QubitBlock qubit) {
  spiralSafeAPI.post("/api/wave/analyze", new HashMap<>() {{
    put("content", operation + " on qubit " + qubit.getId());
    put("player", player.getUniqueId().toString());
    put("coherence", qubit.getCoherenceScore());
    put("curl", calculateCurl(qubit));
    put("divergence", calculateDivergence(qubit));
  }});
}
```

### Store Circuit Blueprints

```java
public void saveCircuit(QuantumCircuit circuit) {
  spiralSafeAPI.post("/api/context/store", new HashMap<>() {{
    put("domain", "quantum_circuits");
    put("content", new HashMap<>() {{
      put("name", circuit.getName());
      put("qubits", circuit.getQubitCount());
      put("gates", circuit.getGates().stream()
        .map(g -> g.toJSON())
        .collect(Collectors.toList()));
      put("coherence", circuit.getCoherence());
    }});
    put("signals", new HashMap<>() {{
      put("use_when", new String[]{"quantum_computing", "high_coherence"});
    }});
  }});
}
```

### Quantum Achievements

Track via ATOM system:

```java
public void unlockQuantumAchievement(String name) {
  spiralSafeAPI.post("/api/atom/create", new HashMap<>() {{
    put("name", name);
    put("molecule", "quantum_achievements");
    put("status", "complete");
    put("verification", new HashMap<>() {{
      put("player_uuid", player.getUniqueId().toString());
      put("timestamp", System.currentTimeMillis());
    }});
  }});
}
```

---

## Commands

```
/quantum create <qubit|gate|circuit>
  - Create quantum component

/quantum measure <qubit-id>
  - Force measurement of qubit

/quantum entangle <qubit1-id> <qubit2-id>
  - Manually entangle two qubits

/quantum circuit run <circuit-name>
  - Execute saved circuit

/quantum stats
  - View quantum statistics (measurements, coherence, etc.)

/quantum tutorial
  - Start interactive quantum computing tutorial
```

---

**H&&S:WAVE** | From qubits to quantum time. From superposition to spiral-play.

```
SpiralCraft Quantum Circuits: v1.1.0
Status: READY FOR PRODUCTION
Quantum Gates: 9 types
Algorithms: 4 implemented
Integration: Full SpiralSafe API
```

⚛️ **Quantum Computing**: Not just theory anymore—build it, see it, play it.
