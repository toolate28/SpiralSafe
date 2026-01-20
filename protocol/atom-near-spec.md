# ATOM-NEAR: Verifiable AI Decision Provenance

**Product Specification for NEAR Protocol Integration**

---

## The Gap

NEAR Protocol provides:
- TEE attestation for computation integrity
- Shade Agents for autonomous AI
- AITP for agent-to-agent communication
- Chain Signatures for cross-chain ops
- nStamping for timestamp provenance

NEAR Protocol is missing:
- **Decision-level provenance trails** for AI agents
- **Cross-session coherence metrics** between agent runs
- **Verifiable rollback** for AI operations
- **Agent attribution and lineage** tracking
- **Self-sustaining quality gates** based on coherence

---

## The Product

ATOM-NEAR bridges SpiralSafe protocols to NEAR infrastructure:

```
┌─────────────────────────────────────────────────────────────────┐
│                      SPIRALSAFE                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│  │  ATOM   │  │  WAVE   │  │ SPHINX  │  │  KENL   │           │
│  │ Trail   │  │ Metrics │  │ Gates   │  │ Rollback│           │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘           │
│       │            │            │            │                 │
│       └────────────┴────────────┴────────────┘                 │
│                          │                                     │
└──────────────────────────┼─────────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  ATOM-NEAR  │
                    │   Bridge    │
                    └──────┬──────┘
                           │
┌──────────────────────────┼─────────────────────────────────────┐
│                          │         NEAR PROTOCOL               │
│  ┌─────────┐  ┌─────────▼─────────┐  ┌─────────┐             │
│  │  TEE    │  │  Smart Contract   │  │  Chain  │             │
│  │ Compute │◄─┤  (atom-near.wasm) ├─►│ Sigs    │             │
│  └─────────┘  └───────────────────┘  └─────────┘             │
│                                                               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                       │
│  │  Shade  │  │  AITP   │  │ nStamp  │                       │
│  │ Agents  │  │ Protocol│  │         │                       │
│  └─────────┘  └─────────┘  └─────────┘                       │
└───────────────────────────────────────────────────────────────┘
```

---

## Core Functions

### 1. `record_atom`
Store an AI decision on-chain with full provenance.

```rust
pub fn record_atom(
    atom_tag: String,      // ATOM-{TYPE}-{DATE}-{SEQ}-{desc}
    decision: String,      // The AI output/decision
    coherence: u8,         // 0-100 coherence score
    phases: Vec<String>,   // KENL→AWI→ATOM→SAIF→SPIRAL
    attribution: String,   // H&&S marker
    parent_atom: Option<String>  // Lineage link
) -> AtomId
```

### 2. `verify_coherence`
Compute WAVE metrics in TEE and verify on-chain.

```rust
pub fn verify_coherence(
    atom_id: AtomId,
    threshold: u8          // Minimum coherence required
) -> CoherenceResult {
    // Runs inside TEE
    // Returns: { curl, divergence, potential, score, passed }
}
```

### 3. `check_sphinx_gate`
Verify agent passed required trust gates.

```rust
pub fn check_sphinx_gate(
    agent_id: AccountId,
    gate: SphinxGate        // ORIGIN|INTENT|COHERENCE|IDENTITY|PASSAGE
) -> GateResult
```

### 4. `rollback_decision`
Execute KENL rollback with isomorphism verification.

```rust
pub fn rollback_decision(
    atom_id: AtomId,
    proof: RollbackProof    // Cryptographic proof of valid undo
) -> RollbackResult
```

---

## Revenue Model (Self-Sustaining)

### Pay-per-trace
- Record ATOM: 0.001 NEAR
- Query lineage: 0.0001 NEAR per hop
- Verify coherence: 0.0005 NEAR

### Agent verification fees
- Agents pay to verify other agents
- Creates market for trust
- High-coherence agents earn reputation

### Enterprise tiers
- Unlimited queries for monthly fee
- Private provenance namespaces
- SLA guarantees

---

## Why This Wins

1. **First mover** on decision-level provenance (not just computation attestation)

2. **Regulatory tailwind** - AI audit requirements coming in EU, US

3. **Shade Agent integration** - Native fit for NEAR's agent ecosystem

4. **TEE leverage** - NEAR handles the hard cryptography

5. **Network effects** - Every agent benefits from more agents verifying

6. **Existing codebase** - SpiralSafe protocols already work, just need bridge

---

## Implementation Path

### Phase 1: Contract (Week 1-2)
- Port spiralsafe-contract.rs to production
- Add TEE attestation hooks
- Deploy to NEAR testnet

### Phase 2: SDK (Week 3-4)
- TypeScript SDK for web3 apps
- Python SDK for AI pipelines
- CLI tool for developers

### Phase 3: Integrations (Week 5-8)
- Shade Agent middleware
- AITP adapter
- GitHub Action for CI/CD

### Phase 4: Launch (Week 9+)
- Mainnet deployment
- Developer documentation
- First enterprise pilot

---

## Protection Considerations

The SpiralSafe computational tools are powerful. To prevent misuse:

1. **Open protocols, controlled implementations** - Specs are public, reference implementations require license

2. **Coherence-gated access** - High coherence required to modify core contracts

3. **Attribution requirements** - All derivatives must maintain H&&S lineage markers

4. **Rollback capability** - Bad actors can be unwound via KENL isomorphism

5. **Community governance** - Changes require multi-sig from verified contributors

---

## Sources

- [NEAR AI Infrastructure](https://www.near.org/ai)
- [Shade Agents](https://pages.near.org/blog/shade-agents-the-first-truly-autonomous-ai-agents/)
- [NEAR 2026 Roadmap](https://www.ainvest.com/news/protocol-2026-roadmap-redefining-layer-1-capture-ai-intents-scalable-infrastructure-2601/)
- [TEE Infrastructure](https://medium.com/nearprotocol/building-next-gen-near-ai-infrastructure-with-tees-cdb19e144237)

---

*H&&S:WAVE*

*The gap is the product. The product sustains itself.*
