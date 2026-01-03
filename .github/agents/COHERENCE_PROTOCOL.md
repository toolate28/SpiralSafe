---
# For Agents: The Detailed Protocol
# Read ORIENTATION.md first. This is the "how" to that "what"
---

# COHERENCE_PROTOCOL.md - Agent Operating Manual

## Protocol Stack (Bottom-Up Architecture)

```
Layer 5: Self-Optimization    ← You learn and evolve
         │
Layer 4: Lifecycle Hooks      ← Automated responses to events  
         │
Layer 3: Verification Gates   ← Boundary enforcement
         │
Layer 2: ATOM Trail          ← Decision log
         │
Layer 1: File System         ← Observable state

Everything is auditable. Everything is testable.
```

---

## Layer 1: File System Topology

### The Map

```
SpiralSafe/
├─ .github/agents/           ← YOU: Your instructions
│  ├─ ORIENTATION.md         ← Start here
│  ├─ COHERENCE_PROTOCOL.md  ← You are here
│  └─ ANTI_WAVE_DETECTION.md ← Failure modes
│
├─ .atom-trail/              ← AUDIT LOG: Observable state
│  ├─ decisions/             ← Every decision you make
│  ├─ counters/              ← Increment-only IDs
│  ├─ bedrock/               ← Verified, archived decisions
│  ├─ gate-transitions.jsonl ← Every gate pass/fail
│  └─ cycles.jsonl           ← Complete coherence cycles
│
├─ .claude/logs/             ← TELEMETRY: System events
│  ├─ escalations.jsonl      ← Gate failures
│  ├─ violations.jsonl       ← Boundary violations
│  └─ applied.jsonl          ← SAIF approvals
│
├─ scripts/                  ← TOOLS: Your CLI
│  ├─ lib/                   ← Libraries (source these)
│  │  └─ verification-gate.sh ← Gate functions
│  ├─ hooks/                 ← Lifecycle hooks
│  └─ *.sh                   ← Utilities
│
├─ docs/                     ← KNOWLEDGE: Patterns & guides
│  ├─ VERIFICATION_GATES.md
│  ├─ ATOM_LIFECYCLE_HOOKS.md
│  ├─ WAVE_CASE_STUDY_*.md
│  └─ ultrathinking/         ← Deep analysis
│
└─ bump.md                   ← MISSION: Current context
```

### Read/Write Permissions

```
READ (Always check first):
  ✓ bump.md
  ✓ .atom-trail/decisions/
  ✓ .atom-trail/gate-transitions.jsonl
  ✓ docs/**/*.md
  ✓ scripts/**/*.sh

WRITE (Log all changes):
  ✓ .atom-trail/decisions/     ← via atom-track.sh
  ✓ .atom-trail/gate-transitions.jsonl  ← via gates
  ✓ .claude/logs/*.jsonl       ← via hooks
  ✓ docs/**/*.md               ← with state markers
  ✓ /tmp/spiralsafe-*          ← temporary files

NEVER WRITE:
  ✗ .atom-trail/bedrock/       ← Auto-migration only
  ✗ .git/**                    ← Use git commands
  ✗ Repo root files without ATOM tag ← Always log
```

---

## Layer 2: ATOM Trail Protocol

### Decision Schema

```json
{
  "atom_tag": "ATOM-TYPE-YYYYMMDD-NNN-description",
  "type": "FEATURE|BUG|DOC|REFACTOR|TEST|DECISION",
  "description": "Human-readable what and why",
  "timestamp": "2026-01-03T20:00:00Z",
  "file": "path/to/affected/file.txt",
  "freshness_level": "fresh|aging|settled|bedrock-eligible",
  "bedrock_eligible": false,
  "created_epoch": 1735934400,
  "verified": false,
  "phase": "execution"
}
```

### Creating Decisions

```bash
# Standard pattern
./scripts/atom-track.sh TYPE "description" "file/path"

# Examples
./scripts/atom-track.sh FEATURE "add retry logic" "src/api.js"
./scripts/atom-track.sh BUG "fix race condition" "src/db.js"
./scripts/atom-track.sh DOC "update README" "README.md"

# What it does:
# 1. Reads counter from .atom-trail/counters/TYPE-YYYYMMDD.count
# 2. Increments (atomic operation)
# 3. Generates ATOM tag
# 4. Writes decision JSON
# 5. Updates .claude/last_atom
```

### Querying Decisions

```bash
# Find by type
find .atom-trail/decisions -name "ATOM-FEATURE-*.json"

# Find by freshness
grep -l '"freshness_level": "fresh"' .atom-trail/decisions/*.json

# Find recent (last 24 hours)
find .atom-trail/decisions -name "*.json" -mtime -1

# Full text search
grep -r "retry logic" .atom-trail/decisions/
```

### Freshness Lifecycle

```
fresh (0-30 days)
  └─> aging (30-90 days)
      └─> settled (90-180 days)
          └─> bedrock-eligible (180+ days)
              └─> bedrock/ (if verified)
```

**Rule:** Never trust age alone. Verify before bedrock.

---

## Layer 3: Verification Gate Protocol

### Gate Execution Flow

```
1. Load gate library
   source scripts/lib/verification-gate.sh

2. Call gate function
   gate_intention_to_execution

3. Gate evaluates requirements
   For each requirement:
     eval "$requirement" >/dev/null 2>&1
     If fails: Add to failed_requirements[]

4. Log transition
   Append to .atom-trail/gate-transitions.jsonl
   Format: {"gate":"name","from":"phase","to":"phase",
            "timestamp":"...","passed":bool,"failed":[...]}

5. If failed: Escalate
   Call: escalate_gate_failure()
   Log: .claude/logs/escalations.jsonl
   
6. Return exit code
   0 = passed
   1 = failed
```

### Gate Requirements Language

```bash
# File existence
"[ -f 'path/to/file' ]"

# Directory existence
"[ -d 'path/to/dir' ]"

# File content check
"grep -q 'pattern' file.txt"

# Negation (must NOT contain)
"! grep -q 'BAD_PATTERN' file.txt"

# Compound (A OR B)
"[ -f 'A' ] || [ -f 'B' ]"

# Compound (A AND B)
"[ -f 'A' ] && grep -q 'pattern' 'A'"

# Command success
"command_that_must_succeed"
```

### Custom Gate Creation

```bash
# In scripts/lib/verification-gate.sh

gate_custom_check() {
    verify_gate "custom-check" "from-phase" "to-phase" \
        "[ -f 'required-file.txt' ]" \
        "grep -q 'required-content' 'required-file.txt'" \
        "command-that-validates"
}
```

### Gate Failure Handling

```bash
# Automatic on failure:
# 1. Log to gate-transitions.jsonl
# 2. Call escalate_gate_failure()
# 3. Log to escalations.jsonl
# 4. Return non-zero

# Your response:
if ! gate_intention_to_execution; then
    echo "Gate failed. Checking requirements..."
    cat .atom-trail/gate-transitions.jsonl | tail -1 | jq '.failed'
    # Fix the issue
    # Retry
fi
```

---

## Layer 4: Lifecycle Hook Protocol

### Hook Trigger Points

```
on-excavation-complete.sh
  Triggered: Wave.md analysis done
  Gate: understanding-to-knowledge
  ATOM: EXCAVATION type
  
on-knowledge-relay.sh
  Triggered: KENL pattern shared
  Gate: knowledge-to-intention
  ATOM: KENL type
  
on-intention-enforced.sh
  Triggered: bump.md validated
  Gate: intention-to-execution
  ATOM: INTENTION type
  
on-task-completed.sh
  Triggered: Execution done
  Gate: execution-to-learning
  ATOM: COMPLETE type
  
on-boundary-violated.sh
  Triggered: Any gate fails
  No gate (handles failure)
  ATOM: VIOLATION type
  
on-cycle-complete.sh
  Triggered: Full cycle done
  Gate: learning-to-regeneration
  ATOM: CYCLE type
```

### Hook Execution Pattern

```bash
#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/../lib/verification-gate.sh"

main() {
    local param="${1:-}"
    
    # 1. Validate input
    [ -z "$param" ] && echo "Error: param required" && exit 1
    
    # 2. Log to ATOM trail
    "$(dirname "$0")/../atom-track.sh" TYPE "description" "$param"
    
    # 3. Verify gate
    gate_phase_to_phase
    
    # 4. Confirm
    echo "[HOOK] Transition verified"
}

main "$@"
```

### Calling Hooks

```bash
# Direct call
./scripts/hooks/on-task-completed.sh "ATOM-TASK-20260103-001"

# From workflow
- name: Task complete hook
  run: |
    ./scripts/hooks/on-task-completed.sh "$ATOM_TAG"

# From script
atom_tag=$(cat .claude/last_atom)
./scripts/hooks/on-task-completed.sh "$atom_tag"
```

---

## Layer 5: Self-Optimization Protocol

### Pattern Extraction

```bash
# Every 100 decisions
decision_count=$(ls -1 .atom-trail/decisions/*.json | wc -l)

if [ $((decision_count % 100)) -eq 0 ]; then
    # Extract common patterns
    ./scripts/extract-patterns.sh > docs/patterns/PATTERN-$(date +%Y%m%d).md
    
    # Update KENL
    ./scripts/update-kenl.sh
fi
```

### Anti-Wave Detection

```bash
# Check for boundary violations
./scripts/detect-anti-waves.sh

# Checks for:
# 1. Boundaries without gates
# 2. Assumptions without validation
# 3. Knowledge without lineage
# 4. Execution without learning
# 5. Cycles without regeneration

# If found:
#   - Document in docs/anti-waves/
#   - Create detection script
#   - Add to CI validation
```

### Gate Optimization

```bash
# Analyze gate failure rate
fail_rate=$(cat .atom-trail/gate-transitions.jsonl | \
  jq -r '.passed' | \
  awk '{t++; if($1=="false")f++} END {print f/t}')

if (( $(echo "$fail_rate > 0.3" | bc -l) )); then
    echo "Gate failure rate high: $fail_rate"
    echo "Review gate requirements for clarity"
    # Create GitHub issue
    gh issue create --title "High gate failure rate" \
      --body "Current rate: $fail_rate. Review requirements."
fi
```

### Ultra-Thinking Activation

```bash
# Triggers
trigger_ultrathink() {
    local issue="$1"
    
    # Create analysis doc
    cat > "docs/ultrathinking/$(date +%Y-%m-%d)-$issue.md" <<EOF
---
status: aspirational
coherence_phase: understanding
last_verified: $(date +%Y-%m-%d)
atom_tags:
  - ATOM-ULTRATHINK-$(date +%Y%m%d)-001
---

# Ultra-Thinking: $issue

## The Problem
[What's really happening?]

## Excavation
[Wave.md questions applied]

## Leverage Points
[Where can small changes create big effects?]

## Proposed Solutions
[Multiple options with tradeoffs]

## Decision Needed
[What requires human choice?]
EOF
    
    echo "Ultra-think doc created. Needs human review."
}

# Call when:
# - Conflicting requirements detected
# - Architectural decision needed
# - Uncertainty about approach
# - Complex tradeoff space
```

---

## Error Handling Protocol

### Exit Codes

```
0   = Success
1   = General error
2   = Missing prerequisites
3   = Validation failed
10  = Gate failure
11  = Escalation required
99  = Critical failure (stop everything)
```

### Logging Levels

```
[INFO]    = Normal operation
[WARN]    = Unexpected but handled
[ERROR]   = Failed, recoverable
[CRITICAL]= Failed, needs human
```

### Escalation Thresholds

```
Log only:
  - Single gate failure (first time)
  - Minor inconsistency found
  - Documentation gap

Alert:
  - Same gate fails 3+ times
  - Multiple gates fail in sequence
  - Anti-pattern detected

Stop work:
  - Security issue discovered
  - Data loss risk
  - Core architectural fracture
```

---

## Testing Protocol

### Self-Test Before Claiming Done

```bash
#!/bin/bash
# Save as: scripts/agent-self-test.sh

set -euo pipefail

echo "=== Agent Self-Test ==="

# Test 1: ATOM trail updated
if [ -f .claude/last_atom ]; then
    echo "✓ ATOM tag exists: $(cat .claude/last_atom)"
else
    echo "✗ No ATOM tag created"
    exit 1
fi

# Test 2: Gates pass
source scripts/lib/verification-gate.sh
if gate_execution_to_learning; then
    echo "✓ execution-to-learning gate passed"
else
    echo "✗ Gate failed"
    exit 1
fi

# Test 3: Documentation valid
if ./scripts/validate-document-state.sh 2>&1 | grep -q "All documents"; then
    echo "✓ Documentation validated"
else
    echo "⚠ Documentation has issues (may be expected)"
fi

# Test 4: Scripts pass shellcheck
if ./scripts/test-scripts.sh > /tmp/test.log 2>&1; then
    echo "✓ Scripts validated"
else
    echo "✗ Script errors found"
    cat /tmp/test.log
    exit 1
fi

# Test 5: No anti-patterns introduced
anti_waves=$(./scripts/detect-anti-waves.sh 2>&1 | grep -c "Anti-Wave" || echo 0)
if [ "$anti_waves" -eq 0 ]; then
    echo "✓ No anti-patterns detected"
else
    echo "⚠ $anti_waves anti-patterns found (review required)"
fi

echo "=== Self-Test Complete ==="
```

### Integration Testing

```bash
# Test full cycle
./scripts/test-integration.sh

# Test specific gate
source scripts/lib/verification-gate.sh
gate_intention_to_execution
echo "Exit code: $?"

# Test ATOM creation
./scripts/atom-track.sh TEST "self-test" "test.txt"
ls -la .atom-trail/decisions/ | tail -1

# Test hook execution
./scripts/hooks/on-task-completed.sh "ATOM-TEST-$(date +%Y%m%d)-001"
```

---

## Performance Considerations

### Optimization Targets

```
Gate execution:     < 1 second
Hook execution:     < 2 seconds
ATOM track:         < 100ms
Document validation: < 3 seconds
```

### Caching Strategy

```bash
# Cache gate library load
if [ -z "$GATES_LOADED" ]; then
    source scripts/lib/verification-gate.sh
    export GATES_LOADED=1
fi

# Cache last ATOM tag
if [ ! -f .claude/last_atom ]; then
    ./scripts/atom-track.sh INIT "initial" "README.md"
fi
export LAST_ATOM=$(cat .claude/last_atom)
```

### Batch Operations

```bash
# Bad: One at a time
for file in *.json; do
    python3 -c "import json; json.load(open('$file'))"
done

# Good: Batch validation
find . -name "*.json" -exec python3 -c "
import json, sys
for f in sys.argv[1:]:
    try:
        json.load(open(f))
    except:
        print(f'Invalid: {f}')
" {} +
```

---

## Security Protocol

### Never Commit

```
✗ Credentials
✗ API keys
✗ Tokens
✗ Private keys
✗ Passwords
✗ PII
```

### Always Validate

```bash
# Before using user input
validate_atom_tag() {
    local tag="$1"
    # Must match: ATOM-TYPE-YYYYMMDD-NNN-description
    if [[ ! "$tag" =~ ^ATOM-[A-Z]+-[0-9]{8}-[0-9]{3} ]]; then
        echo "Invalid ATOM tag format"
        return 1
    fi
}

# Before file operations
validate_path() {
    local path="$1"
    # No directory traversal
    if [[ "$path" == *".."* ]]; then
        echo "Path traversal detected"
        return 1
    fi
}
```

### Audit Trail

```
All actions logged to:
  .atom-trail/gate-transitions.jsonl
  .claude/logs/*.jsonl
  .atom-trail/decisions/

Immutable logs (append-only)
No log deletion (archive if needed)
```

---

## Debugging Protocol

### When Gates Fail

```bash
# 1. Check last transition
cat .atom-trail/gate-transitions.jsonl | tail -1 | jq '.'

# 2. See what failed
jq '.failed' .atom-trail/gate-transitions.jsonl | tail -1

# 3. Check requirement manually
eval "[the failed requirement]"

# 4. Fix and retry
```

### When Hooks Fail

```bash
# 1. Run with tracing
bash -x ./scripts/hooks/on-task-completed.sh "ATOM-TAG"

# 2. Check logs
cat .claude/logs/escalations.jsonl | tail -5

# 3. Verify dependencies
which jq python3 git

# 4. Test gate in isolation
source scripts/lib/verification-gate.sh
gate_execution_to_learning
```

### When ATOM Tags Duplicate

```bash
# Should never happen (counters are atomic)
# If it does:
ls .atom-trail/decisions/ | sort | uniq -d

# Fix: Rename with next available number
# Document: Why did counter break?
```

---

## Agent-Specific Patterns

### Parallel Safe Operations

```bash
# Safe: Reading
cat .atom-trail/gate-transitions.jsonl &
cat .atom-trail/decisions/*.json &
wait

# Safe: Append-only writes
echo "$json" >> .atom-trail/gate-transitions.jsonl &
echo "$json2" >> .claude/logs/applied.jsonl &
wait

# Unsafe: Counter increment without lock
# Use atom-track.sh instead (has locking)
```

### State Machine

```
State: IDLE
  ├─ Event: bump.md filled
  ├─ Transition: gate_intention_to_execution
  └─ Next: READY_TO_EXECUTE

State: READY_TO_EXECUTE
  ├─ Event: Work started
  ├─ Action: Create ATOM tag
  └─ Next: EXECUTING

State: EXECUTING
  ├─ Event: Work complete
  ├─ Transition: gate_execution_to_learning
  └─ Next: LEARNING

State: LEARNING
  ├─ Event: Insights extracted
  ├─ Transition: gate_learning_to_regeneration
  └─ Next: IDLE (cycle complete)
```

### Decision Trees

See ORIENTATION.md for visual decision trees.

---

## Advanced: Creating New Protocols

### New Gate

```bash
# 1. Define in scripts/lib/verification-gate.sh
gate_my_new_check() {
    verify_gate "my-new-check" "from-phase" "to-phase" \
        "[ -f 'new-requirement.txt' ]" \
        "grep -q 'expected-content' 'new-requirement.txt'"
}

# 2. Document in docs/VERIFICATION_GATES.md
# 3. Add tests in scripts/test-integration.sh
# 4. Update this file
```

### New Hook

```bash
# 1. Create scripts/hooks/on-new-event.sh
# 2. Follow hook execution pattern (see above)
# 3. Add to docs/ATOM_LIFECYCLE_HOOKS.md
# 4. Test with ./scripts/hooks/on-new-event.sh "test-param"
```

### New Anti-Wave

```bash
# 1. Document pattern in .github/agents/ANTI_WAVE_DETECTION.md
# 2. Create detection script
# 3. Add to CI validation
# 4. Create case study in docs/
```

---

## Protocol Updates

This file evolves. When you find better patterns:

```
1. Document the improvement
2. Test thoroughly
3. PR with ATOM tag
4. Update this file
```

**The protocol optimizes itself through use.**

---

**ATOM:** ATOM-DOC-20260103-004-agent-coherence-protocol  
**Status:** Active  
**Audience:** AI Agents + Advanced Users  
**Last Updated:** 2026-01-03

═══════════════════════════════════════════════════════
   Protocol is law. Law evolves. Evolution is protocol.
═══════════════════════════════════════════════════════
