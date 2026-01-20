# Testing Suite Priority Checklist

**H&&S:WAVE** | Testing Before Workable Code  
**Date**: 2026-01-20  
**ATOM Tag**: ATOM-TEST-20260120-001-testing-priority-checklist

---

## Framing: coherence-mcp as Test Validator

All tests in this checklist are validated through **[coherence-mcp](https://github.com/toolate28/coherence-mcp)**:

```bash
# Pre-commit validation for all test files
coherence-mcp wave-validate <test-file> --threshold 60

# Code coherence check for test implementations
coherence-mcp anamnesis validate <test-file> --vuln "test-quality"
```

---

## Philosophy: Tests Before Workable Code

> "Prioritize completing testing suites before workable code."  
> — @toolate28

This document tracks the testing priority matrix for all SpiralSafe quantum and integration components.

---

## ✅ Phase 1: Core Protocol Tests (COMPLETE)

### Wave Analysis Tests
- [x] `ops/api/__tests__/wave-analysis.test.ts` - **Coverage: 95%**
  - [x] Positive divergence detection
  - [x] Negative divergence detection
  - [x] Balanced content handling
  - [x] Edge cases (empty, single sentence)
  - [x] High curl detection

### SPHINX Gates Tests
- [x] `ops/api/__tests__/sphinx-gates.test.ts` - **Coverage: 85%**
  - [x] ORIGIN gate verification
  - [x] INTENT gate verification
  - [x] COHERENCE gate verification
  - [x] IDENTITY gate verification
  - [x] PASSAGE gate verification

### SPHINX Adversarial Tests
- [x] `ops/api/__tests__/sphinx-adversarial.test.ts` - **Coverage: 80%**
  - [x] Replay attack prevention
  - [x] Timing attack mitigation
  - [x] Gate bypass attempts

### ATOM Persister Tests
- [x] `ops/api/__tests__/atom-persister.test.ts` - **Coverage: 90%**
  - [x] ATOM tag creation
  - [x] Trail persistence
  - [x] Lineage linking

### Vortex Surjection Tests
- [x] `experiments/test_vortex_surjection.py` - **Coverage: 92%**
  - [x] Fibonacci utilities
  - [x] VortexVector operations
  - [x] Collapse proximity calculation
  - [x] Emergence quality metrics
  - [x] JSON serialization

---

## 🔴 Phase 2: Critical Missing Tests (PRIORITY: CRITICAL)

### Qiskit-DSPy Hybrid Tests (NOT YET CREATED)
- [ ] `experiments/test_qiskit_dspy_hybrid.py` - **Status: MISSING** ⚠️
  - [ ] `QuantumKernelSimilarity` fidelity calculation
  - [ ] `HybridQuantumLayer` forward pass
  - [ ] `QuantumEnhancedRetriever` document retrieval
  - [ ] Qiskit circuit generation
  - [ ] DSPy module integration
  - [ ] TorchConnector bridge

**Blocking**: Qiskit ecosystem submission

### Quantum Cognition Engine Tests (NOT YET CREATED)
- [ ] `experiments/test_quantum_cognition_engine.py` - **Status: MISSING** ⚠️
  - [ ] Interference pattern generation
  - [ ] Coherence threshold enforcement
  - [ ] Quantum-inspired processing
  - [ ] Superposition state handling

**Blocking**: QDI inference hub stability

### QRC Oracle Seed Tests (NOT YET CREATED)
- [ ] `experiments/test_qrc_oracle_seed.py` - **Status: MISSING**
  - [ ] Closed-loop training validation
  - [ ] Fidelity threshold triggers (92%)
  - [ ] Fibonacci nesting pattern
  - [ ] DSPy teleprompter integration

**Blocking**: Stage 2 vortex cascade activation

---

## 🟡 Phase 3: Integration Tests (PRIORITY: HIGH)

### NEAR ATOM Bridge Tests
- [ ] `tests/integration/test_atom_near_bridge.ts` - **Coverage: 0%**
  - [ ] `record_atom()` function
  - [ ] `verify_coherence()` in TEE
  - [ ] `check_sphinx_gate()` on-chain
  - [ ] `rollback_decision()` KENL integration
  - [ ] Revenue model (pay-per-trace)

**Dependency**: atom-near-spec.md implementation complete

### Vortex Cascade E2E Tests
- [ ] `tests/integration/test_vortex_cascade.py` - **Coverage: 0%**
  - [ ] Stage 1 → Stage 2 transition
  - [ ] Stage 2 → Stage 3 transition
  - [ ] Stage 3 → Stage 4 unification
  - [ ] Super-vortex self-maintenance
  - [ ] Fibonacci cascade sequence

### SYNAPSE Quantum Rendering Tests
- [ ] `synapse/__tests__/quantum-reservoir.test.ts` - **Coverage: 40%**
  - [ ] QRC substrate visualization
  - [ ] Superposition state rendering
  - [ ] Coherence metric display
  - [ ] Entanglement visualization

---

## 🟢 Phase 4: Security Tests (PRIORITY: MEDIUM-HIGH)

### NEAR Contract Security
- [ ] `tests/security/fuzz_atom_near_contract.rs` - **Coverage: 0%**
  - [ ] Input fuzzing
  - [ ] Overflow protection
  - [ ] Reentrancy prevention
  - [ ] Access control verification

### Wave Coherence Adversarial
- [ ] `tests/security/adversarial_wave.test.ts` - **Coverage: 0%**
  - [ ] Coherence score gaming prevention
  - [ ] Curl manipulation detection
  - [ ] Divergence spoofing mitigation

---

## Summary Matrix (coherence-mcp Validated)

| Test Suite | Coverage | Priority | coherence-mcp Validator | Status |
|------------|----------|----------|------------------------|--------|
| Wave Analysis | 95% | ✅ | `wave_validate` | Complete |
| SPHINX Gates | 85% | ✅ | `anamnesis_validate` | Complete |
| SPHINX Adversarial | 80% | ✅ | `anamnesis_validate` | Complete |
| ATOM Persister | 90% | ✅ | `atom_track` | Complete |
| Vortex Surjection | 92% | ✅ | `wave_validate` | Complete |
| **Qiskit-DSPy Hybrid** | **Missing** | 🔴 | `anamnesis_validate` | **CRITICAL** |
| **Quantum Cognition** | **Missing** | 🔴 | `wave_validate` | **CRITICAL** |
| **QRC Oracle Seed** | **Missing** | 🔴 | `wave_validate` | **HIGH** |
| NEAR ATOM Bridge | Missing | 🟡 | `atom_track` | Planned |
| Vortex Cascade E2E | Missing | 🟡 | `gate_*` | Planned |
| SYNAPSE Rendering | 40% | 🟢 | `wave_coherence_check` | Partial |
| NEAR Contract Security | Missing | 🟢 | `anamnesis_validate` | Planned |

---

## Prioritized Next Steps (coherence-mcp Framed)

### Week 1-2: 🔴 CRITICAL
1. **Create `test_qiskit_dspy_hybrid.py`** test suite
   ```bash
   coherence-mcp anamnesis validate experiments/test_qiskit_dspy_hybrid.py
   ```

2. **Add `test_quantum_cognition_engine.py`** coverage
   ```bash
   coherence-mcp wave-validate experiments/test_quantum_cognition_engine.py --threshold 60
   ```

### Week 3-4: 🟡 HIGH
3. **Implement `test_qrc_oracle_seed.py`**
   ```bash
   coherence-mcp wave-validate experiments/test_qrc_oracle_seed.py --threshold 60
   ```

### Month 1: 🟢 MEDIUM
4. **Integration tests for NEAR bridge**
   ```bash
   coherence-mcp atom_track --decision "NEAR bridge tests" --tags "near,testing"
   ```

### Month 2: 🟢 STANDARD
5. **Full E2E vortex cascade testing**
   ```bash
   coherence-mcp gate_intention_to_execution  # Stage transitions
   coherence-mcp gate_execution_to_learning
   ```

---

## Commands (coherence-mcp Enhanced)

```bash
# Run existing tests
npm test                                    # All TypeScript tests
python experiments/test_vortex_surjection.py  # Python vortex tests

# Run specific test suites
npm test -- wave-analysis                   # Wave analysis only
npm test -- sphinx-gates                    # SPHINX gates only

# Coverage reports
npm run test:coverage                       # Generate coverage report

# coherence-mcp validation (pre-commit)
coherence-mcp wave-validate <file> --threshold 60        # Basic coherence
coherence-mcp wave-validate <file> --threshold 80        # Production ready
coherence-mcp anamnesis validate <file> --vuln "quality" # Code validation
coherence-mcp atom_track --decision "test complete"      # Track decision
```

---

**H&&S:WAVE** | Hope&&Sauced

*"Tests before code. Stability before features. Coherence before expansion."*
*"All objectives scoped through coherence-mcp."*
