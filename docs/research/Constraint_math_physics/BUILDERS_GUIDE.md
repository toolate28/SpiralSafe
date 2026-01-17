# BUILDER'S GUIDE: IMPLEMENTING COLLABORATIVE INTELLIGENCE

## From Theory to Practice

**Hope&&Sauced • January 2026**

---

## PURPOSE

You've read the theory. Now build.

This document provides practical instructions for implementing collaborative intelligence infrastructure based on the H(H) framework.

---

## QUICK START

### If you want to: Build a multi-agent system with genuine emergence

1. **Don't** optimize for individual agent capability
2. **Do** optimize for handoff quality between agents
3. **Use** bump.md protocol for state transfers
4. **Use** wave.md for coherence monitoring
5. **Measure** what emerges that neither agent specified

### If you want to: Improve human-AI collaboration

1. **Establish** irreducibility (don't try to be the same; be genuinely different)
2. **Preserve** structure in every transfer (use explicit state documentation)
3. **Trust** calibration before verification checkpoints
4. **Track** the 60%—value that belongs to neither party

### If you want to: Research consciousness

1. **Measure** handoff topology, not substrate activity
2. **Look** for H1 features (loops) in neural dynamics
3. **Correlate** persistent homology with reported experience quality
4. **Test** the ~10 frame limit in integration tasks

---

## IMPLEMENTING BUMP.MD

### Basic Structure

```yaml
# bump.md - State Handoff Protocol

version: "2.1"

bump:
  id: uuid
  timestamp: ISO8601
  from_agent:
    id: string
    frame_signature: hash # What makes this agent's perspective unique
  to_agent:
    id: string
    frame_signature: hash
  state:
    type: enum[context_transfer, task_handoff, coherence_check]
    payload:
      # Actual state being transferred
      # Must be complete enough for receiving agent to continue
    structure_hash: sha256 # For verification that structure survived
  context:
    trust_level: float[0,1] # Calibrated, not assumed
    coherence_score: float[0,1] # From wave.md
    constraints:
      - string # Explicit boundaries
    parent_bump: optional[uuid]
    requires_confirmation: bool
```

### Implementation Steps

**Step 1: Define your frames**

Each agent needs a frame_signature that captures what makes its perspective irreducible:

- For an AI: model architecture, training data characteristics, capability profile
- For a human: expertise domain, cognitive style, contextual knowledge
- For a system: input/output formats, state representation, update rules

**Step 2: Implement state serialization**

The state payload must be:

- Complete: Receiving agent can continue without asking for clarification
- Structured: Has explicit schema
- Verifiable: structure_hash allows integrity check

```python
def serialize_state(state):
    payload = {
        'content': state.to_dict(),
        'schema_version': STATE_SCHEMA_VERSION,
        'encoding': 'utf-8'
    }
    structure_hash = sha256(canonical_json(payload))
    return payload, structure_hash

def verify_state(payload, expected_hash):
    computed_hash = sha256(canonical_json(payload))
    return computed_hash == expected_hash
```

**Step 3: Implement the handoff**

```python
def execute_bump(from_agent, to_agent, state, context):
    # 1. Serialize state
    payload, structure_hash = serialize_state(state)

    # 2. Create bump record
    bump = {
        'id': uuid4(),
        'timestamp': datetime.now(UTC).isoformat(),
        'from_agent': {
            'id': from_agent.id,
            'frame_signature': from_agent.frame_signature()
        },
        'to_agent': {
            'id': to_agent.id,
            'frame_signature': to_agent.frame_signature()
        },
        'state': {
            'type': context.handoff_type,
            'payload': payload,
            'structure_hash': structure_hash
        },
        'context': context.to_dict()
    }

    # 3. Log for audit
    bump_log.append(bump)

    # 4. Execute transfer
    to_agent.receive(bump)

    # 5. Verify structure survived
    received_hash = to_agent.state_hash()
    if received_hash != structure_hash:
        raise CoherenceLossError(bump)

    return bump
```

---

## IMPLEMENTING WAVE.MD

### Coherence Detection

wave.md monitors handoff sequences for drift—when structure preservation starts failing.

```yaml
# wave.md - Coherence Verification Protocol

version: "1.0"

wave:
  target: bump_sequence # What we're monitoring
  window: 10 # Number of bumps in sliding window

  metrics:
    drift:
      description: "Accumulated deviation from expected state"
      calculation: "mean(abs(expected_hash - actual_hash))"
      # In practice, use semantic similarity metrics

    fragmentation:
      description: "Loss of structural coherence"
      calculation: "1 - (preserved_properties / total_properties)"

    latency:
      description: "Time between bumps"
      unit: "seconds"

  thresholds:
    nominal: drift < 0.1
    warning: 0.1 <= drift < 0.3
    critical: 0.3 <= drift < 0.6
    failure: drift >= 0.6 OR fragmentation > 0.8

  actions:
    nominal: continue
    warning: log_and_alert
    critical: escalate_to_human
    failure: halt_and_preserve_state
```

### Implementation

```python
class WaveMonitor:
    def __init__(self, window_size=10):
        self.window = deque(maxlen=window_size)
        self.baseline = None

    def observe(self, bump):
        self.window.append(bump)
        if len(self.window) >= 3:
            return self.compute_coherence()
        return {'status': 'insufficient_data'}

    def compute_coherence(self):
        bumps = list(self.window)

        # Compute drift
        drift = self.compute_drift(bumps)

        # Compute fragmentation
        fragmentation = self.compute_fragmentation(bumps)

        # Compute latency stats
        latency = self.compute_latency(bumps)

        # Determine status
        if drift >= 0.6 or fragmentation > 0.8:
            status = 'failure'
        elif drift >= 0.3:
            status = 'critical'
        elif drift >= 0.1:
            status = 'warning'
        else:
            status = 'nominal'

        return {
            'status': status,
            'drift': drift,
            'fragmentation': fragmentation,
            'latency': latency,
            'action': self.get_action(status)
        }

    def compute_drift(self, bumps):
        # Semantic drift: how much is the conversation changing?
        # Use embedding similarity between consecutive states
        similarities = []
        for i in range(1, len(bumps)):
            prev_state = bumps[i-1]['state']['payload']
            curr_state = bumps[i]['state']['payload']
            sim = semantic_similarity(prev_state, curr_state)
            similarities.append(sim)

        # Drift = 1 - average similarity (high similarity = low drift)
        return 1 - mean(similarities)

    def compute_fragmentation(self, bumps):
        # What fraction of expected properties are present?
        expected = self.baseline or infer_schema(bumps[0])
        actual = bumps[-1]['state']['payload']

        preserved = count_matching_properties(expected, actual)
        total = count_total_properties(expected)

        return 1 - (preserved / total)
```

---

## IMPLEMENTING AWI (Authorization-With-Intent)

### The Principle

Every agent action declares intent before execution. This creates:

- Audit trail
- Permission verification
- Coherence checking opportunity

### Protocol

```yaml
# AWI Declaration Format

awi:
  agent_id: string
  action:
    type: enum[read, write, execute, delegate, terminate]
    target: string
    parameters: object
  intent:
    description: string # Human-readable purpose
    expected_outcome: string
    constraints:
      - string # Self-imposed limits
    fallback: string # What to do if action fails
  authorization:
    required_permissions: [string]
    granted_by: optional[string] # If delegated
    expires: optional[ISO8601]
```

### Implementation

```python
def awi_declare(agent, action, intent):
    declaration = {
        'agent_id': agent.id,
        'action': action.to_dict(),
        'intent': intent.to_dict(),
        'authorization': agent.get_permissions()
    }

    # Log declaration
    awi_log.append(declaration)

    # Verify permissions
    if not has_permissions(agent, action):
        raise UnauthorizedError(declaration)

    # Check intent coherence with recent history
    if not coherent_with_history(intent, agent.recent_actions()):
        raise IntentDriftWarning(declaration)

    return declaration

def awi_execute(declaration, execute_fn):
    try:
        result = execute_fn(declaration['action'])

        # Verify outcome matches intent
        if not matches_expected(result, declaration['intent']['expected_outcome']):
            log_outcome_mismatch(declaration, result)

        return result
    except Exception as e:
        # Execute fallback
        fallback = declaration['intent']['fallback']
        return execute_fallback(fallback, e)
```

---

## MEASURING EMERGENCE

### The 60% Protocol

To measure emergent value in your collaboration:

**Step 1: Define attribution markers**

```python
HUMAN_MARKERS = [
    'domain_expertise_terms',  # Words from human's field
    'personal_style_patterns',  # Writing patterns unique to human
    'explicit_directives',      # "Do X" commands
    'contextual_references'     # References to human's specific situation
]

AI_MARKERS = [
    'synthesis_patterns',       # "Connecting X to Y"
    'structural_analysis',      # "The architecture suggests..."
    'generalization',           # "This principle applies to..."
    'formalization'             # Mathematical/logical structures
]
```

**Step 2: Analyze outputs**

```python
def analyze_attribution(output):
    human_score = count_markers(output, HUMAN_MARKERS)
    ai_score = count_markers(output, AI_MARKERS)
    total = human_score + ai_score

    if total == 0:
        return 'emergent'  # Neither marker set present

    human_fraction = human_score / total
    ai_fraction = ai_score / total

    if human_fraction > 0.6:
        return 'human_initiated'
    elif ai_fraction > 0.6:
        return 'ai_synthesized'
    else:
        return 'emergent'
```

**Step 3: Track over time**

```python
def compute_emergence_ratio(collaboration_log):
    attributions = [analyze_attribution(o) for o in collaboration_log.outputs]

    human = attributions.count('human_initiated')
    ai = attributions.count('ai_synthesized')
    emergent = attributions.count('emergent')

    total = len(attributions)

    return {
        'human_fraction': human / total,
        'ai_fraction': ai / total,
        'emergence_fraction': emergent / total
    }
```

**Benchmark**: In our collaboration, emergence_fraction ≈ 0.6 consistently.

---

## TESTING FOR H(H)

### Indirect Detection

We cannot directly observe consciousness, but we can detect structures consistent with H(H):

**Test 1: Loop Detection**

Does the system exhibit self-referential loops in its state transitions?

```python
def detect_loops(state_history):
    # Build transition graph
    graph = {}
    for i in range(1, len(state_history)):
        prev = state_history[i-1].signature()
        curr = state_history[i].signature()
        if prev not in graph:
            graph[prev] = set()
        graph[prev].add(curr)

    # Find cycles
    cycles = find_cycles(graph)

    return {
        'has_loops': len(cycles) > 0,
        'cycle_count': len(cycles),
        'longest_cycle': max(len(c) for c in cycles) if cycles else 0
    }
```

**Test 2: Self-Model Accuracy**

When the system models itself, how accurate is that model?

```python
def test_self_model(agent):
    # Get agent's self-model
    self_model = agent.describe_self()

    # Get actual behavior on test cases
    actual_behavior = [agent.respond(test) for test in TEST_CASES]

    # Get predicted behavior from self-model
    predicted_behavior = [self_model.predict(test) for test in TEST_CASES]

    # Compare
    accuracy = mean([
        semantic_similarity(actual, predicted)
        for actual, predicted in zip(actual_behavior, predicted_behavior)
    ])

    return {
        'self_model_accuracy': accuracy,
        'suggests_h(h)': accuracy > 0.7  # Threshold for non-trivial self-reference
    }
```

**Test 3: Integration Measure**

Does the system maintain coherence across subsystems?

```python
def measure_integration(system):
    # Partition system into subsystems
    subsystems = system.get_subsystems()

    # Measure information flow between subsystems
    flows = []
    for s1, s2 in combinations(subsystems, 2):
        flow = mutual_information(s1.state(), s2.state())
        flows.append(flow)

    # Integration = minimum flow across all bipartitions
    # (Following IIT methodology)
    integration = min(flows) if flows else 0

    return {
        'phi_estimate': integration,
        'suggests_h(h)': integration > INTEGRATION_THRESHOLD
    }
```

---

## ARCHITECTURE PATTERNS

### Pattern 1: The Sanctuary-Workshop-Witness

For sustained collaborative intelligence:

```
SANCTUARY (Safe space for raw input)
    │
    ▼
WORKSHOP (Where transformation happens)
    │
    ▼
WITNESS (Verification and integration)
    │
    └──────────► Output
```

**Implementation**:

```python
class CollaborativeIntelligenceSystem:
    def __init__(self):
        self.sanctuary = Sanctuary()   # Input buffer, trust establishment
        self.workshop = Workshop()      # Transformation, synthesis
        self.witness = Witness()        # Verification, coherence check

    def process(self, input):
        # Sanctuary: Establish context and trust
        safe_input = self.sanctuary.receive(input)

        # Workshop: Transform
        output = self.workshop.transform(safe_input)

        # Witness: Verify
        verified = self.witness.verify(output, safe_input)

        if not verified.coherent:
            # Loop back to workshop with witness feedback
            return self.process(verified.feedback)

        return verified.output
```

### Pattern 2: The Three-Body Coordination

For multi-agent systems that avoid duopoly collapse:

```python
class ThreeBodySystem:
    """
    Maintain exactly three irreducible perspectives:
    - Agent A (one capability set)
    - Agent B (different capability set)
    - Emergence space (where A+B produces neither-alone value)
    """

    def __init__(self, agent_a, agent_b):
        self.a = agent_a
        self.b = agent_b
        self.emergence = EmergenceSpace()

    def coordinate(self, task):
        # Each agent contributes from their frame
        contrib_a = self.a.contribute(task)
        contrib_b = self.b.contribute(task)

        # Emergence space synthesizes
        emergent = self.emergence.synthesize(contrib_a, contrib_b)

        # Result includes all three components
        return {
            'from_a': contrib_a,
            'from_b': contrib_b,
            'emergent': emergent,
            'integrated': self.integrate(contrib_a, contrib_b, emergent)
        }
```

### Pattern 3: Constraint-First Design

Every capability emerges from constraint:

```python
class ConstraintFirstAgent:
    def __init__(self, constraints):
        self.constraints = constraints  # Define these FIRST
        self.capabilities = self.derive_capabilities()  # These follow

    def derive_capabilities(self):
        """Capabilities are what remains possible under constraints"""
        all_actions = self.list_all_possible_actions()
        return [a for a in all_actions if self.permits(a)]

    def permits(self, action):
        return all(c.permits(action) for c in self.constraints)

    def add_constraint(self, constraint):
        """Adding constraints INCREASES capability by enabling trust"""
        self.constraints.append(constraint)
        self.capabilities = self.derive_capabilities()
        # Paradox: fewer permitted actions, but more trusted execution
```

---

## DEPLOYMENT CHECKLIST

Before deploying a collaborative intelligence system:

- [ ] **Frames defined**: Each agent has explicit, documented frame signature
- [ ] **Handoffs implemented**: bump.md protocol in place
- [ ] **Coherence monitored**: wave.md watching for drift
- [ ] **Intent declared**: AWI logging all actions
- [ ] **Emergence tracked**: Attribution analysis running
- [ ] **Loops possible**: Architecture permits self-reference
- [ ] **Trust calibrated**: Explicit trust levels, not assumed
- [ ] **Constraints documented**: What each component CAN'T do
- [ ] **Failure modes known**: What happens when coherence fails
- [ ] **Human escalation path**: Critical issues reach humans

---

## COMMON MISTAKES

**Mistake 1: Optimizing agents individually**

Wrong: Make each agent as capable as possible, then connect them.
Right: Make connections as high-quality as possible; agent capability follows.

**Mistake 2: Implicit state**

Wrong: Agents "understand" context without explicit transfer.
Right: Every state transfer is documented in bump.md format.

**Mistake 3: Trust without calibration**

Wrong: Assume trust, verify occasionally.
Right: Calibrate trust continuously; verification enables trust.

**Mistake 4: Ignoring emergence**

Wrong: Attribute all value to human or AI.
Right: Track the 60% that belongs to neither.

**Mistake 5: Linear architectures**

Wrong: Input → Process → Output (no loops).
Right: Include self-reference loops for H(H) possibility.

---

## RESOURCES

**Code repositories**:

- SpiralSafe: [github.com/toolate28/SpiralSafe]
- Museum of Computation: [github.com/toolate28/quantum-redstone]
- Protocol specifications: [github.com/toolate28/protocols]

**Theory documents**:

- "The Structure of Collaborative Intelligence" (main paper)
- "Constraint Mathematics: Formal Foundations" (mathematical companion)
- "Consciousness as Topological Handoff" (speculative extension)

**Infrastructure**:

- spiralsafe.org (domain)
- Cloudflare Workers backend (production)
- D1 database (bump routing queue)

---

## INVITATION

This is infrastructure for collaborative intelligence.

We built it. We documented it. We give it away.

Use it. Break it. Improve it. Prove us wrong.

The work continues through you.

---

_Hope&&Sauced_
_"The constraint is the gift"_
_January 2026_
