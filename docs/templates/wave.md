# wave.md: Cascading Issues Analysis Protocol

## Primary Excavation Layer
*These questions force relationship-thinking, not isolated symptom-documentation*

### Load-Bearing Structural Questions

For each issue in the dataset, excavate along these vectors:

- **Architectural Violation**: What foundational assumption about the system is this issue exposing or breaking? What was assumed to be stable that has fractured?

- **Secondary Constraint Generation**: Where does this issue create or amplify constraints in adjacent systems? How does it propagate beyond its surface location?

- **Necessary Conditions Inversion**: What would need to be true—in system design, in user mental models, in infrastructure assumptions—for this to *not* be a problem? This reveals the architectural gift hidden in the constraint.

### Cascading Consequence Mapping

Map the relationships between issues as architectural cascades:

- **Root Cause Clustering**: Which issues share a common root cause even though their symptoms appear unrelated? What structure are they all complaining about?

- **Cascade Resolution Pathways**: If we addressed issue X, which other issues would cascade-resolve naturally? Which would become more acute? Where are the leverage points?

- **Failure Mode Sequences**: What must break first for this chain to collapse? What's the sequence of dependencies that creates the current state?

## Pattern Recognition Layer
*These probe for emergent structural insights*

### Domain Bridging Questions

Look across functional boundaries for systems-level patterns:

- **Cross-Domain Presence**: Does this pattern appear across different systems—UX blocking, integration failures, performance cascades, conceptual misalignments? What does it look like in each domain?

- **Problem Class Classification**: Is this fundamentally architectural, operational, or epistemic? (A knowledge gap, a design boundary, or an execution constraint?)

- **Symptom vs. Structure**: Where is the system treating symptoms instead of addressing the load-bearing structure creating them?

### Leverage Point Analysis

Identify where small structural shifts create disproportionate improvements:

- **Structural Multipliers**: If we could fix one underlying structure, how many surface issues would resolve as a natural consequence?

- **Trade-Off Archaeology**: What trade-offs is the current system making—consciously or unconsciously? Where are constraints being imposed that could be reframed as architectural gifts?

- **Constraint as Enabler**: Where do boundaries actually *enable* rather than restrict? What becomes possible precisely because of these limits?

## Synthesis Layer
*These make the analysis itself load-bearing*

### Collective Intelligence Questions

Move from individual issues to systemic understanding:

- **Holistic Visibility**: What pattern is visible to the system as a whole that no single issue reveals? What emerges only when we map the entire structure?

- **Stakeholder Divergence**: How would different perspectives—maintainers, users, integrators, architects—see the same issue differently? Where are legitimate disagreements structural?

- **Emergent Solutions**: What solutions naturally emerge when we understand the cascading structure rather than fight individual symptoms one by one?

### Synthesis Output

The analysis generates not just fixes but architectural clarity:

- **Structural Diagnosis**: Here's the load-bearing structure. Here's where it's been fractured and why those fractures are cascading.

- **Leverage Interventions**: Here are the highest-leverage places to intervene. Address these and watch the system stabilize naturally.

- **Regenerative Design**: Here's how to rebuild so constraints become architectural gifts. Here's the design that absorbs future stress without fragmentation.

## Implementation Guidance

### For GitHub Query Construction

When harvesting issues, request enough metadata to map relationships:

- **Component/Domain**: What system does this touch?
- **Impact Signature**: Does it block other systems? Create cascades?
- **Temporal Dimension**: Is this chronic or acute?
- **Stakeholder Impact**: Who does this constrain most immediately?

### For Analysis Execution

Process the data with these movement patterns:

1. **Horizontal Mapping**: Identify all issues across domains. What's the full landscape?

2. **Vertical Excavation**: For each cluster, dig into root structures. What would need to be true for this not to happen?

3. **Cascade Tracing**: Follow the secondary consequences. Where does fixing one thing create leverage for others?

4. **Synthesis**: Step back. What's the single structural insight that makes sense of this entire landscape?

## Output Frame

The analysis delivers:

- **Structural Map**: Here's how the system is organized and where the fractures are occurring
- **Cascade Diagram**: Here's how issues propagate and reinforce each other
- **Leverage Points**: Here's where small interventions create systemic shifts
- **Regenerative Design**: Here's the architecture that prevents these cascades from forming again

---

*This protocol treats each issue as archaeological evidence of deeper structural arrangement. The goal is not to collect problems but to excavate the load-bearing structures that, once understood, allow solutions to emerge naturally.*
