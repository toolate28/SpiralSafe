# Surjection Integration Points

**ATOM-DOC-20260117-013-surjection-points**

Curated list of GitHub repositories providing tooling for self-sustaining monitoring, security, MLOps, inference, testing, and attribution systems.

---

## Security & Red Team

### 1. miracle078/application-security-engineering
- **Purpose**: SAST/DAST automation, security header checks, AWS Security Hub integration
- **Surjection Point**: `SPHINX:COHERENCE` ← security scan results feed coherence scoring
- **Integration**: Run `security-scanner-tool.py` in CI, pipe findings to WAVE analysis
- **URL**: https://github.com/miracle078/application-security-engineering

### 2. qianl15/code_puppy
- **Purpose**: Security auditor agent with risk-based remediation
- **Surjection Point**: `SPHINX:IDENTITY` ← agent authentication and role verification
- **Integration**: SecurityAuditorAgent verifies agent actions before BUMP handoff
- **URL**: https://github.com/qianl15/code_puppy

### 3. SWORDOps/SWORDSwarm
- **Purpose**: Compliance frameworks (HIPAA, ISO27001, OWASP), security tool orchestration
- **Surjection Point**: `SPHINX:INTENT` ← legal basis verification for security actions
- **Integration**: Compliance check gates before production deployments
- **URL**: https://github.com/SWORDOps/SWORDSwarm

### 4. GaryOcean428/monkey-coder
- **Purpose**: Security specialist agent for vuln assessment, secure coding, architecture review
- **Surjection Point**: `WAVE` ← architecture coherence analysis
- **Integration**: Security code review as SPHINX gate prerequisite
- **URL**: https://github.com/GaryOcean428/monkey-coder

### 5. bivex/NubemGenesisMCP
- **Purpose**: 60+ security domains, incident response, DevSecOps integration
- **Surjection Point**: Full protocol stack (WAVE→SPHINX→BUMP→ATOM)
- **Integration**: Comprehensive security persona for multi-agent collaboration
- **URL**: https://github.com/bivex/NubemGenesisMCP

### 6. kaydenraquel-crypto/Nova-Forge
- **Purpose**: Intelligent vulnerability scanner with remediation roadmaps
- **Surjection Point**: `ATOM` ← provenance trail for vulnerability lifecycle
- **Integration**: Executive summary generation for human escalation (SPHINX:ESCALATE)
- **URL**: https://github.com/kaydenraquel-crypto/Nova-Forge

---

## MLOps & Inference

### 7. cbwinslow/template2 (CrewAI Dev Team)
- **Purpose**: Multi-agent development crew (code review, architecture, security, DevOps)
- **Surjection Point**: `BUMP` ← agent handoff coordination
- **Integration**: Drop-in replacement for SpiralSafe agent coordination
- **URL**: https://github.com/cbwinslow/template2

### 8. liangdabiao/autogen-financial-analysis
- **Purpose**: Enterprise agents for risk analysis, quantitative modeling
- **Surjection Point**: `QRC-Oracle-Seed` ← coherence metrics for model validation
- **Integration**: Risk thresholds feed SPHINX:COHERENCE gate (>92% fidelity)
- **URL**: https://github.com/liangdabiao/autogen-financial-analysis

---

## Provenance & Attribution

### 9. GriffinCanCode/LangViz
- **Purpose**: Data provenance and lineage tracking with checksums
- **Surjection Point**: `ATOM` trail ← immutable transformation records
- **Integration**: Provenance model directly maps to ATOM tagging schema
- **URL**: https://github.com/GriffinCanCode/LangViz

### 10. rexdivakar/HippocampAI
- **Purpose**: Memory provenance with citation extraction and lineage chains
- **Surjection Point**: `SPHINX:ORIGIN` ← citation verification for genesis claims
- **Integration**: ProvenanceChain model for cross-session agent memory
- **URL**: https://github.com/rexdivakar/HippocampAI

### 11. Zweiblum66/vpams
- **Purpose**: Blockchain provenance with events, verification, licensing
- **Surjection Point**: `ATOM` ← immutable event chain with signatures
- **Integration**: ProvenanceEvent model for audit-grade trail logging
- **URL**: https://github.com/Zweiblum66/vpams

### 12. dreamsoft-pro/RAE-agentic-memory
- **Purpose**: Context provenance for AI decisions, confidence scoring
- **Surjection Point**: `SPHINX:COHERENCE` ← context quality metrics
- **Integration**: DecisionRecord model for human-in-loop approval tracking
- **URL**: https://github.com/dreamsoft-pro/RAE-agentic-memory

### 13. chrishayuk/chuk-tool-processor
- **Purpose**: Provenance guard for tool output attribution
- **Surjection Point**: `SPHINX:IDENTITY` ← reference validation before reuse
- **Integration**: ProvenanceGuard enforces attribution requirements
- **URL**: https://github.com/chrishayuk/chuk-tool-processor

### 14. MatLab-Research/OntExtract
- **Purpose**: Agent provenance with tool attribution (NLTK, spaCy, transformers)
- **Surjection Point**: `ATOM` ← software agent lineage tracking
- **Integration**: ProvAgent model for multi-tool orchestration audit
- **URL**: https://github.com/MatLab-Research/OntExtract

---

## Testing & Specification

### 15. aRustyDev/specs
- **Purpose**: Enterprise spec templates (security, SLA, compliance)
- **Surjection Point**: `SPHINX:INTENT` ← requirement verification
- **Integration**: Security requirements template for SPHINX gate definitions
- **URL**: https://github.com/aRustyDev/specs

### 16. 6ogo/Tech-Skills
- **Purpose**: Role matcher with automation types and skill matrices
- **Surjection Point**: `AGENTS.md` ← capability-based agent assignment
- **Integration**: Skill model for N-agent scaling (future scalability)
- **URL**: https://github.com/6ogo/Tech-Skills

---

## Priority Integration Order

1. **Immediate** (closes existing gaps):
   - `chuk-tool-processor` → ProvenanceGuard for ATOM trail integrity
   - `RAE-agentic-memory` → DecisionRecord for SPHINX:ESCALATE human approval
   - `Nova-Forge` → Remediation roadmaps for security coherence

2. **Near-term** (scalability):
   - `template2/CrewAI` → Multi-agent coordination pattern
   - `6ogo/Tech-Skills` → Capability matrix for N-agent scaling

3. **Strategic** (ecosystem completeness):
   - `vpams` → Blockchain-grade provenance (optional, high-trust scenarios)
   - `HippocampAI` → Cross-session memory persistence spiral

---

<!-- SPHINX:PASSAGE verdict="SURJECTION_MAPPED" epoch=1 iteration=19 -->