# 🎓 Quantum-Minecraft Bridge Curriculum

**Teaching Quantum Computing Through Play**

---

## Overview

This curriculum teaches quantum computing concepts through Minecraft Redstone circuits, leveraging the **Isomorphism Principle** (discrete = continuous) to make cutting-edge physics accessible to students ages 8-18.

### Core Insight

> "A Minecraft Redstone XOR gate IS a quantum CNOT gate - not metaphorically, but topologically identical."

By building circuits in Minecraft, students learn quantum mechanics, boolean algebra, and category theory **while playing a game they love**.

---

## Curriculum Structure

### Age-Based Tracks

| Age Group | Track Name | Focus | Duration |
|-----------|------------|-------|----------|
| 8-10 | **Block Builders** | Logic gates, cause-effect | 4 weeks |
| 11-13 | **Circuit Designers** | Boolean algebra, truth tables | 6 weeks |
| 14-16 | **Quantum Explorers** | Quantum gates, isomorphisms | 8 weeks |
| 17-18 | **Theory Architects** | Category theory, proofs | 12 weeks |

### Learning Objectives (All Tracks)

By the end of this curriculum, students will:
1. ✅ Build functional logic gates in Minecraft
2. ✅ Understand boolean algebra and truth tables
3. ✅ Explain quantum computing basics
4. ✅ Recognize structural equivalences across substrates
5. ✅ Appreciate that games can be research tools

---

## Materials Required

### Software

- **Minecraft Java Edition** (version 1.20+)
  - Available: minecraft.net
  - Cost: ~$27 USD (one-time purchase)
  - Alternatives: Minecraft Education Edition (free for some schools)

- **Optional: Litematica Mod**
  - For loading pre-built schematics
  - Install via Fabric mod loader
  - Makes building faster and more accurate

- **Optional: Python + Jupyter**
  - For executing interactive proof notebook
  - Ages 14+ recommended

### Physical Materials

- **None required** - this is a fully digital curriculum
- Optional: Printouts of truth tables, circuit diagrams for reference

### Teacher Resources

- Access to this GitHub repository
- Minecraft world files (provided in `/museum/builds/`)
- Lesson plan PDFs (below)
- Assessment rubrics (below)

---

## Lesson Plans

### Track 1: Block Builders (Ages 8-10)

**Goal**: Build logic gates in Minecraft and understand input-output relationships

#### Lesson 1: Redstone Basics (1 hour)
- **Learning objective**: Students can place redstone dust and observe signal flow
- **Activity**: Build a simple on/off circuit with lever and lamp
- **Success criteria**: Lamp turns on when lever is pulled
- **Materials**: [Starter world file](/museum/builds/redstone-basics.world)
- **Assessment**: Observation checklist

#### Lesson 2: The NOT Gate (1 hour)
- **Learning objective**: Students understand signal inversion
- **Activity**: Build redstone torch circuit (lever ON → lamp OFF)
- **Success criteria**: Student explains "opposite" behavior
- **Materials**: NOT gate schematic
- **Assessment**: Verbal explanation

#### Lesson 3: The AND Gate (1 hour)
- **Learning objective**: Students build circuits requiring multiple inputs
- **Activity**: Two levers must both be ON to light lamp
- **Success criteria**: Truth table completion (drawing)
- **Materials**: AND gate schematic
- **Assessment**: Truth table worksheet

#### Lesson 4: The XOR Gate - Capstone (2 hours)
- **Learning objective**: Students build a complex gate from simple components
- **Activity**: Guided construction of XOR using NOT and AND
- **Success criteria**: Working XOR gate, tested on all inputs
- **Materials**: [XOR schematic](/museum/builds/xor-gate.litematic)
- **Assessment**: Functionality test + reflection (draw what you learned)

**Full track**: See [Block Builders Track PDF](./block-builders-track.pdf)

---

### Track 2: Circuit Designers (Ages 11-13)

**Goal**: Master boolean algebra and design custom circuits

#### Lesson 1: Boolean Algebra Basics (1 hour)
- **Learning objective**: Students write boolean expressions
- **Activity**: Convert Redstone circuits to AND/OR/NOT notation
- **Success criteria**: Correctly writes XOR = (A ∧ ¬B) ∨ (¬A ∧ B)
- **Materials**: Boolean algebra reference sheet
- **Assessment**: Written worksheet

#### Lesson 2: Truth Tables (1 hour)
- **Learning objective**: Students can complete and verify truth tables
- **Activity**: Test XOR gate for all 4 input combinations, record results
- **Success criteria**: Correct truth table matches expectation
- **Materials**: Truth table template
- **Assessment**: Accuracy check

#### Lesson 3: Half-Adder Circuit (2 hours)
- **Learning objective**: Students combine gates to perform addition
- **Activity**: Build half-adder (sum and carry bits)
- **Success criteria**: Working adder, explains how it adds binary numbers
- **Materials**: Half-adder schematic
- **Assessment**: Demonstration + explanation

#### Lesson 4: Design Your Own Gate (2 hours)
- **Learning objective**: Students apply principles to create novel circuits
- **Activity**: Design circuit meeting specific truth table
- **Success criteria**: Circuit matches given specification
- **Materials**: Blank Minecraft world, specification sheet
- **Assessment**: Peer review + teacher verification

**Full track**: See [Circuit Designers Track PDF](./circuit-designers-track.pdf)

---

### Track 3: Quantum Explorers (Ages 14-16)

**Goal**: Understand quantum computing through Redstone equivalents

#### Lesson 1: Intro to Quantum Computing (1.5 hours)
- **Learning objective**: Students explain what qubits are
- **Activity**: Video + discussion + notation practice (|0⟩, |1⟩)
- **Success criteria**: Can describe superposition in own words
- **Materials**: Khan Academy quantum video, notation worksheet
- **Assessment**: Short quiz

#### Lesson 2: Quantum Gates (1.5 hours)
- **Learning objective**: Students recognize X, H, CNOT gates
- **Activity**: Match quantum gates to Redstone equivalents
- **Success criteria**: Correctly identifies XOR ≅ CNOT target bit
- **Materials**: Quantum gate reference poster
- **Assessment**: Matching worksheet

#### Lesson 3: Building CNOT in Minecraft (2 hours)
- **Learning objective**: Students build quantum-equivalent circuit
- **Activity**: Construct CNOT using Redstone XOR + identity
- **Success criteria**: Circuit matches quantum truth table
- **Materials**: CNOT schematic
- **Assessment**: Truth table comparison

#### Lesson 4: The Isomorphism Principle (2 hours)
- **Learning objective**: Students understand structural equivalence
- **Activity**: Compare Redstone and quantum circuits side-by-side
- **Success criteria**: Explains "same structure, different substrate"
- **Materials**: Side-by-side diagram, isomorphism explainer
- **Assessment**: Essay (2-3 paragraphs): "Why is Minecraft quantum computing?"

#### Lesson 5: Bell State Challenge (2 hours)
- **Learning objective**: Students implement entanglement equivalent
- **Activity**: Build probabilistic circuit creating correlated outputs
- **Success criteria**: 50% (0,0), 50% (1,1) distribution verified
- **Materials**: RNG circuit schematic
- **Assessment**: Statistical verification

**Full track**: See [Quantum Explorers Track PDF](./quantum-explorers-track.pdf)

---

### Track 4: Theory Architects (Ages 17-18)

**Goal**: Formal understanding of category theory and quantum foundations

#### Lesson 1-4: Category Theory Basics (8 hours)
- Categories, objects, morphisms, functors, natural transformations
- Work through [Isomorphism Formal Proof](/docs/research/ISOMORPHISM_FORMAL_PROOF.md)

#### Lesson 5-8: Quantum Mechanics Foundations (8 hours)
- Hilbert spaces, unitary operators, measurement
- Compare to boolean circuits formally

#### Lesson 9-12: Research Project (8 hours)
- Students pick open question from proof document
- Design experiment (computational or Minecraft-based)
- Present findings

**Full track**: See [Theory Architects Track PDF](./theory-architects-track.pdf)

---

## Assessment Rubrics

### Rubric 1: Circuit Functionality (All Tracks)

| Criteria | Emerging (1) | Developing (2) | Proficient (3) | Advanced (4) |
|----------|--------------|----------------|----------------|--------------|
| **Correctness** | Circuit doesn't work | Works for some inputs | Works for all inputs | Works + optimized |
| **Understanding** | Can't explain | Partial explanation | Full explanation | Teaches others |
| **Documentation** | No truth table | Incomplete table | Complete table | Table + analysis |

### Rubric 2: Conceptual Understanding (Tracks 2-4)

| Criteria | Emerging (1) | Developing (2) | Proficient (3) | Advanced (4) |
|----------|--------------|----------------|----------------|--------------|
| **Boolean Logic** | Struggles with AND/OR | Uses gates correctly | Writes expressions | Proves equivalences |
| **Abstraction** | Sees only blocks | Recognizes patterns | Explains structure | Generalizes |
| **Connections** | Isolated knowledge | Links some concepts | Integrates well | Creates new insights |

### Rubric 3: Research Skills (Track 4)

| Criteria | Emerging (1) | Developing (2) | Proficient (3) | Advanced (4) |
|----------|--------------|----------------|----------------|--------------|
| **Question Formulation** | Vague | Specific | Testable | Novel |
| **Methodology** | Unclear method | Standard approach | Rigorous protocol | Innovative |
| **Analysis** | Observation only | Basic analysis | Statistical rigor | Theoretical depth |
| **Communication** | Hard to follow | Clear | Compelling | Publication-ready |

---

## Classroom Management

### Time Management

**Block schedule** (90-minute classes):
- 10 min: Review previous lesson
- 20 min: New concept introduction
- 50 min: Hands-on building in Minecraft
- 10 min: Share + reflect

**Traditional schedule** (45-minute classes):
- Split activities across multiple days
- Homework: Complete truth tables, watch videos

### Differentiation

**For students who struggle**:
- Pre-built templates they can modify
- Pair programming (work with partner)
- Visual guides with every step shown

**For advanced students**:
- Open-ended challenges (design your own)
- Research extension projects
- Help teach struggling students (solidifies understanding)

### Behavior Management

**Minecraft-specific challenges**:
- Students may wander off-task (building houses instead of circuits)
- Griefing (destroying others' work)

**Solutions**:
- Adventure mode (can't break blocks except in designated areas)
- Individual worlds (each student has own space)
- Clear success criteria (must demonstrate working circuit to teacher)

---

## Sample Lesson Plan (Detailed)

### Lesson: Building the XOR Gate (Ages 10-12)

**Duration**: 90 minutes
**Prerequisites**: Students have built NOT and AND gates
**Materials**: Minecraft worlds, XOR schematic printout, truth table worksheet

#### Timeline

**Minutes 0-10: Hook + Review**
1. Show magic trick: "I have a lamp that does something strange..."
2. Demonstrate XOR behavior (ON when inputs differ)
3. "Can you figure out the rule?"
4. Quick review: "Who remembers what NOT does? What about AND?"

**Minutes 10-30: Direct Instruction**
5. Reveal: "This is called XOR - exclusive OR"
6. Draw truth table on board together
7. Show schematic: "We'll build this using NOT and AND gates you already know"
8. Walk through logic: (A AND NOT B) OR (NOT A AND B)

**Minutes 30-70: Hands-On Building**
9. Students load schematic in Minecraft (or build from diagram)
10. Circulate: Check on progress, answer questions, troubleshoot
11. Common issues:
    - Redstone torch placement (must be on block side)
    - Dust not connecting (need to be adjacent)
    - Power levels dropping (repeaters if needed)

**Minutes 70-85: Testing + Verification**
12. Students test all 4 input combinations
13. Record results on truth table worksheet
14. Compare to expected truth table
15. Troubleshoot any mismatches

**Minutes 85-90: Reflection + Preview**
16. "What was hardest part? What clicked for you?"
17. "Next week: We'll see how this exact circuit is used in quantum computers"
18. Exit ticket: "Draw XOR symbol and write what it does"

#### Differentiation

**Advanced**: "Can you build XOR using only NAND gates?" (It's possible!)
**Struggling**: Provide partially completed circuit, students finish last step
**Absent**: Video walkthrough available for asynchronous completion

---

## Extension Activities

### For Students Who Finish Early

1. **Build a full adder** (combines two half-adders)
2. **Optimize circuit** (fewer blocks, faster signal)
3. **Design challenge**: Build circuit for given truth table
4. **Teach mode**: Help classmate who's stuck

### Cross-Curricular Connections

**Math**: Binary numbers, modular arithmetic, boolean algebra
**Physics**: Electricity, signal propagation, quantum mechanics
**History**: Claude Shannon, Alan Turing, quantum computing pioneers
**Art**: Circuit aesthetics, redstone as sculpture
**English**: Technical writing (document your circuit design)

---

## Teacher FAQ

### Q: I don't know quantum mechanics. Can I still teach this?

**A**: Yes! The curriculum is designed so you stay one lesson ahead of students. Use the formal proof document and notebook for your own learning. By Track 4, you might learn alongside students (which models growth mindset beautifully).

### Q: Do students need prior Minecraft experience?

**A**: Helpful but not required. Reserve first 1-2 weeks for Minecraft basics if needed. Most students pick it up quickly.

### Q: What if students grief/break things?

**A**: Use Adventure mode or Litematica schematics (students can reload broken circuits instantly). Emphasize that circuits are like code - we can always rebuild.

### Q: How do I grade creative work fairly?

**A**: Use rubrics (above) focusing on understanding rather than aesthetics. A messy but functional circuit scores higher than a pretty broken one.

### Q: What about students without Minecraft at home?

**A**: Coordinate lab time, lend school devices, or use free Minetest alternative. Some students may only build during class time (fine if you extend timeline).

### Q: Is this aligned to standards?

**A**: Yes! Covers:
- **NGSS**: Engineering design, computational thinking
- **Common Core Math**: Logic, patterns, functions
- **CSTA CS**: Algorithms, abstraction, troubleshooting

---

## Success Stories

(To be added as teachers implement curriculum)

**Share yours!** Open a GitHub discussion or email results to [contact info]

---

## Additional Resources

### For Teachers

- [SpiralSafe Documentation](/docs/)
- [Minecraft Education Edition Resources](https://education.minecraft.net)
- [Quantum Computing Basics (Khan Academy)](https://www.khanacademy.org/computing/computer-science/cryptography/comp-number-theory/v/intro-to-quantum-computing)
- Category Theory for Programmers (Bartosz Milewski)

### For Students

- [Interactive Proof Notebook](/books/isomorphism-proof-interactive.ipynb)
- [Redstone Handbook](https://minecraft.fandom.com/wiki/Redstone_Handbook)
- [Qiskit Textbook](https://qiskit.org/textbook/)

### For Parents

- "Is my child really learning quantum physics in Minecraft?" (Yes! Here's how...)
- Safety tips for Minecraft multiplayer
- How to support STEM learning at home

---

## License

This curriculum is open-source under MIT license. Use freely, adapt for your classroom, share improvements back to the community.

**Attribution**: Please credit SpiralSafe project and link back to repo.

---

## Contact

**Questions?** Open a GitHub issue or discussion
**Collaborations?** Email [to be added] or submit PR
**Share successes**: We'd love to hear how it went!

---

**H&&S:WAVE**
**ATOM-EDU-20260113-001-quantum-minecraft-curriculum**
**Created by**: toolate28 (human) + Claude (AI, Anthropic)
**Session**: claude/identify-implementation-gaps-kbs0S
**Date**: 2026-01-13

*From the constraints, gifts. From the spiral, safety. From the sauce, hope.* 🌀

**Teaching the future through play.** 🎓⚛️🎮
