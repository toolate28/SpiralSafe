# SPHINX Protocol Specification

**S**ecure **P**rotocol for **H**ierarchical **I**dentity, **N**avigation, and e**X**change

The SPHINX protocol provides a multi-layered security gate framework for validating artifacts before allowing them through system boundaries. It consists of 5 sequential gates that must all pass for an artifact to be approved.

## Implementation Status

✅ **Fully Implemented** - All 5 gates operational in SpiralSafe v2.1+

- **API**: `/api/sphinx/validate`, `/api/sphinx/gate`, `/api/sphinx/gates`
- **CLI**: `spiralsafe sphinx validate <file>`, `spiralsafe sphinx gate <name> <file>`
- **Tests**: 37 tests including adversarial scenarios
- **ATOM Integration**: All gate decisions logged to ATOM trail

---

## Gate Types

### 1. ORIGIN

**Question**: "Where did this come from?"

**Validates**:
- Source repository/author identity
- Digital signatures (if present)
- Trust chain verification
- ATOM trail reference

**Implementation**: `/ops/api/sphinx/origin-gate.ts`

```typescript
async function validateOrigin(artifact: Artifact): Promise<GateResult> {
  // Check: Is source repository known/trusted?
  // Check: Does author have valid identity?
  // Check: Is there a valid ATOM trail for creation?
  // Check: Is there a digital signature?
  return { passed, evidence, reasoning, timestamp, gateName: 'ORIGIN' };
}
```

**Evidence Types**:
- `source_present` / `source_missing`
- `author_present` / `author_missing`
- `signature_present`
- `atom_trail_reference` / `atom_trail_missing`

**Failure Conditions**:
- Missing source declaration (severity: warning)
- Missing author declaration

---

### 2. INTENT

**Question**: "What is this trying to do?"

**Validates**:
- Declared purpose matches actual behavior
- No hidden side effects
- Aligns with system constraints
- No undeclared sensitive operations

**Implementation**: `/ops/api/sphinx/intent-gate.ts`

```typescript
async function validateIntent(artifact: Artifact): Promise<GateResult> {
  // Check: Does declared purpose match code analysis?
  // Check: Are there undeclared capabilities?
  // Check: Does it violate any system invariants?
  return { passed, evidence, reasoning, timestamp, gateName: 'INTENT' };
}
```

**Evidence Types**:
- `intent_declared` / `intent_missing` (critical)
- `sensitive_patterns_detected` (eval, exec, system calls, credentials)
- `undeclared_capabilities` (critical - fails gate)
- `vague_intent` (warning)

**Detected Patterns**:
- `eval()` / `exec()` usage
- `system()` calls
- Path traversal (`../`)
- Credential handling (password, secret, token, api_key)

**Failure Conditions**:
- No declared intent (critical)
- Sensitive patterns not mentioned in intent (critical)

---

### 3. COHERENCE

**Question**: "Does this make sense internally?"

**Validates**:
- WAVE coherence score meets threshold (default: 80)
- Internal consistency (no contradictions)
- Mathematical correctness
- Curl, divergence, and potential metrics

**Implementation**: `/ops/api/sphinx/coherence-gate.ts`

```typescript
async function validateCoherence(
  artifact: Artifact, 
  threshold: number
): Promise<GateResult> {
  const waveScore = await analyzeWAVE(artifact.content, threshold);
  // Check: Does WAVE score pass threshold?
  // Check: Are all internal references valid?
  // Check: Do all equations/logic chains resolve?
  return { passed: waveScore.overall >= threshold, evidence, reasoning };
}
```

**Evidence Types**:
- `wave_analysis` (overall score, curl, divergence, potential)
- `high_curl` (circular reasoning, repetition)
- `positive_divergence` (ideas expanding without resolution)
- `negative_divergence` (premature closure, over-compression)
- `high_potential` (high complexity)

**Failure Conditions**:
- Overall coherence score below threshold
- High curl (> 0.4)
- High divergence (|divergence| > 0.4)

---

### 4. IDENTITY

**Question**: "Is this what it claims to be?"

**Validates**:
- Type signatures match declarations
- Interface contracts honored
- No masquerading/deception
- Content matches declared type

**Implementation**: `/ops/api/sphinx/identity-gate.ts`

```typescript
async function validateIdentity(artifact: Artifact): Promise<GateResult> {
  // Check: Do runtime types match declared types?
  // Check: Does API surface match documentation?
  // Check: Are there hidden interfaces?
  return { passed, evidence, reasoning, timestamp, gateName: 'IDENTITY' };
}
```

**Evidence Types**:
- `type_declared` / `type_missing` (critical)
- `type_content_match` / `type_content_mismatch` (critical)
- `metadata_complete` / `missing_metadata_fields`
- `interface_contract_check` (validates required methods)

**Supported Type Validations**:
- `markdown`: Headers, lists, links
- `json`: Valid JSON parsing
- `yaml`: YAML structure
- `typescript`/`javascript`: Language keywords
- `python`: def, class, import
- `html`: HTML tags

**Failure Conditions**:
- No type declared (critical)
- Content doesn't match declared type (critical)
- Missing required interface methods (critical)

---

### 5. PASSAGE

**Question**: "Should this be allowed through?"

**Validates**:
- All previous gates passed
- Context-specific rules (custom policies)
- Final authorization decision
- Permissions and environment constraints

**Implementation**: `/ops/api/sphinx/passage-gate.ts`

```typescript
async function validatePassage(
  artifact: Artifact, 
  context: SPHINXGateContext
): Promise<GateResult> {
  // Check: Did all previous gates pass?
  // Check: Are context-specific requirements met?
  // Check: Is there explicit authorization?
  return { passed, evidence, reasoning, timestamp, gateName: 'PASSAGE' };
}
```

**Evidence Types**:
- `all_gates_passed` / `previous_gates_failed` (critical)
- `permissions_sufficient` / `insufficient_permissions` (critical)
- `environment_allowed` / `environment_not_allowed` (critical)
- `rate_limit_ok` / `rate_limit_exceeded` (critical)
- `explicit_authorization` / `explicit_denial` (critical)

**Context Rules**:
- `requiredPermissions` / `grantedPermissions`
- `allowedEnvironments` / `environment`
- `rateLimit: { current, max }`
- `authorized: boolean`

**Failure Conditions**:
- Any previous gate failed (critical)
- Insufficient permissions (critical)
- Environment not allowed (critical)
- Rate limit exceeded (critical)
- Explicit authorization denied (critical)

---

## Core Implementation

### SPHINXGateway Class

**Location**: `/ops/api/sphinx/gates.ts`

```typescript
class SPHINXGateway {
  // Validate artifact through all gates sequentially
  async validate(artifact: Artifact, options?: SPHINXOptions): Promise<SPHINXResult>;
  
  // Validate a single gate independently
  async validateGate(gateName: string, artifact: Artifact): Promise<GateResult>;
  
  // Register custom gate validator
  registerCustomGate(name: string, validator: GateValidator): void;
  
  // Get list of available gates
  getAvailableGates(): string[];
}
```

### SPHINXResult

```typescript
interface SPHINXResult {
  artifact: Artifact;
  gates: {
    origin: GateResult | null;
    intent: GateResult | null;
    coherence: GateResult | null;
    identity: GateResult | null;
    passage: GateResult | null;
  };
  overallPassed: boolean;
  atomTrail: string[]; // IDs of ATOM entries logged
  timestamp: string;
  failedAt?: string; // Which gate failed (if any)
}
```

---

## Integration Points

### 1. WAVE Integration (Gate 3)

```typescript
const coherenceResult = await validateCoherence(artifact, {
  coherenceThreshold: 80
});
```

### 2. ATOM Integration (Every Gate)

```typescript
await atom.log({
  actor: 'sphinx-gateway',
  decision: `Gate ${gateName}: ${result.passed ? 'PASS' : 'FAIL'}`,
  rationale: result.reasoning,
  outcome: JSON.stringify(result.evidence)
});
```

### 3. CLI Usage

```bash
# Validate artifact through all gates
spiralsafe sphinx validate <file> --threshold 80

# Validate single gate
spiralsafe sphinx gate coherence <file>

# Generate full report (JSON)
spiralsafe sphinx report <file>
```

### 4. API Usage

```bash
# Validate artifact
curl -X POST https://api.spiralsafe.org/api/sphinx/validate \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "artifact": {
      "id": "artifact-001",
      "type": "markdown",
      "content": "# Test",
      "metadata": { "intent": "Documentation" },
      "source": "github.com/repo",
      "author": "user"
    },
    "options": { "coherenceThreshold": 80 }
  }'

# Validate single gate
curl -X POST https://api.spiralsafe.org/api/sphinx/gate \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "gateName": "coherence",
    "artifact": {...}
  }'

# List available gates
curl https://api.spiralsafe.org/api/sphinx/gates
```

### 5. GitHub Action (Future)

```yaml
- name: SPHINX Gate Check
  uses: toolate28/spiralsafe-action@v1
  with:
    gate-threshold: 80
    fail-on-gate-failure: true
```

---

## Adversarial Testing

The SPHINX framework includes comprehensive adversarial tests to ensure robust security:

### Test Coverage

1. **Anamnesis-style Exploits**
   - Self-modifying code detection
   - Obfuscated malicious intent
   - Circular reasoning patterns

2. **Malicious Code with Valid Signatures**
   - Hidden eval() calls
   - Credential harvesting
   - Fails INTENT gate despite valid ORIGIN

3. **Contradictory Documentation**
   - Internal contradictions
   - Premature conclusions (negative divergence)

4. **Type Masquerading**
   - Content/type mismatches
   - Missing interface methods
   - Fails IDENTITY gate

5. **Context-Based Attacks**
   - Wrong environment deployment
   - Insufficient permissions
   - Rate limit violations

### Test Results

```
✓ 37 tests passed (24 core + 13 adversarial)
✓ All gates implement correctly
✓ Sequential execution with short-circuit
✓ ATOM trail captures every decision
✓ Adversarial tests fail appropriately
```

**Test Location**: `/ops/api/__tests__/sphinx-gates.test.ts`, `/ops/api/__tests__/sphinx-adversarial.test.ts`

---

## Success Criteria

- ✅ All 5 gates implement correctly
- ✅ Gates execute sequentially (short-circuit on failure)
- ✅ ATOM trail captures every gate decision
- ✅ WAVE integration works (Gate 3)
- ✅ Adversarial tests fail appropriately
- ✅ CLI and programmatic access work
- ✅ Export gate reports in multiple formats

---

## Self-Referential Loop Termination

Each SPHINX gate logs its own passage to the ATOM trail, creating an auditable decision chain:

- New validation loops require distinct genesis events (ORIGIN gate)
- No action can cycle without satisfying all gate riddles
- Every gate decision is immutable once logged
- Surjection supported: every output maps to a verifiable input

---

## References

- [SpiralSafe README](../README.md) - SPHINX gate overview
- [WAVE Specification](./wave-spec.md) - Coherence analysis
- [BUMP Specification](./bump-spec.md) - Routing and handoff
- [ATOM Methodology](../methodology/atom.md) - Task orchestration
- **Implementation**: [ATOM-FEATURE-20260119-007-sphinx-gateway](/.atom-trail/decisions/)

---

**Status**: ✅ **Production Ready** (v2.1+)  
**Last Updated**: 2026-01-19  
**ATOM**: ATOM-DOC-20260119-001-sphinx-spec-update
