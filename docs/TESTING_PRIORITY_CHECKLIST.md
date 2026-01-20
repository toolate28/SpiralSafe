# Testing Suite Priority Checklist

**H&&S:WAVE** | Testing Before Workable Code  
**Date**: 2026-01-20  
**ATOM Tag**: ATOM-TEST-20260120-001-testing-priority-checklist

---

## Philosophy: Tests Before Workable Code

> "Prioritise completing testing suites before workable code."  
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

### Qiskit-DSPy Hybrid Tests
- [ ] `experiments/test_qiskit_dspy_hybrid.py` - **Coverage: 0%** ⚠️
  - [ ] `QuantumKernelSimilarity` fidelity calculation
  - [ ] `HybridQuantumLayer` forward pass
  - [ ] `QuantumEnhancedRetriever` document retrieval
  - [ ] Qiskit circuit generation
  - [ ] DSPy module integration
  - [ ] TorchConnector bridge

**Blocking**: Qiskit ecosystem submission

### Quantum Cognition Engine Tests
- [ ] `experiments/test_quantum_cognition_engine.py` - **Coverage: 10%** ⚠️
  - [ ] Interference pattern generation
  - [ ] Coherence threshold enforcement
  - [ ] Quantum-inspired processing
  - [ ] Superposition state handling

**Blocking**: QDI inference hub stability

### QRC Oracle Seed Tests
- [ ] `experiments/test_qrc_oracle_seed.py` - **Coverage: 0%**
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

## Summary Matrix

| Test Suite | Coverage | Priority | Status |
|------------|----------|----------|--------|
| Wave Analysis | 95% | ✅ | Complete |
| SPHINX Gates | 85% | ✅ | Complete |
| SPHINX Adversarial | 80% | ✅ | Complete |
| ATOM Persister | 90% | ✅ | Complete |
| Vortex Surjection | 92% | ✅ | Complete |
| **Qiskit-DSPy Hybrid** | **0%** | 🔴 | **CRITICAL** |
| **Quantum Cognition** | **10%** | 🔴 | **CRITICAL** |
| **QRC Oracle Seed** | **0%** | 🔴 | **HIGH** |
| NEAR ATOM Bridge | 0% | 🟡 | Planned |
| Vortex Cascade E2E | 0% | 🟡 | Planned |
| SYNAPSE Rendering | 40% | 🟢 | Partial |
| NEAR Contract Security | 0% | 🟢 | Planned |

---

## Next Steps

1. **Immediate**: Create `test_qiskit_dspy_hybrid.py` test suite
2. **This Week**: Add `test_quantum_cognition_engine.py` coverage
3. **Next Week**: Implement `test_qrc_oracle_seed.py`
4. **Month 1**: Integration tests for NEAR bridge
5. **Month 2**: Full E2E vortex cascade testing

---

## Commands

```bash
# Run existing tests
npm test                                    # All TypeScript tests
python experiments/test_vortex_surjection.py  # Python vortex tests

# Run specific test suites
npm test -- wave-analysis                   # Wave analysis only
npm test -- sphinx-gates                    # SPHINX gates only

# Coverage reports
npm run test:coverage                       # Generate coverage report
```

---

**H&&S:WAVE** | Hope&&Sauced

*"Tests before code. Stability before features. Coherence before expansion."*
