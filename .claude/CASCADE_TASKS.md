# Cascade Tasks for Parallel Workers

## Leading Tasker: Claude Opus (Primary Session)

## Generated: 2026-01-10T09:45:00Z

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           PARALLEL WORK ORCHESTRATION                         ║
║                                                                                ║
║  Primary Session: Leading Tasker (finishes LAST, signs off session)          ║
║  Parallel Workers: Pick up cascade tasks based on availability                ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Cascade Structure

```
PRIMARY SESSION (Orchestrator)
     │
     ├──→ CASCADE A: Documentation (20 min)
     │         └── Worker can claim
     │
     ├──→ CASCADE B: Testing (30 min)
     │         └── Worker can claim
     │
     ├──→ CASCADE C: Packaging (15 min)
     │         └── Worker can claim
     │
     └──→ FINAL: Session Sign-off (5 min)
               └── Primary ONLY
```

---

## CASCADE A: Documentation Consolidation

**Time estimate:** 20 minutes
**Dependencies:** None
**Claimable by:** Any parallel worker

### Tasks

1. [ ] Review all `.md` files in SpiralSafe/foundation/
2. [ ] Cross-reference THE_ISO_PRINCIPLE.md with FP2_ALGEBRAIC_QUANTUM.md
3. [ ] Create summary document: `ISO_FP2_SYNTHESIS.md`
4. [ ] Update README.md with F_p² reference

### Completion BUMP

```json
{
  "type": "PASS",
  "from": "worker-a",
  "to": "primary",
  "task": "cascade-a-docs",
  "status": "complete",
  "artifacts": ["ISO_FP2_SYNTHESIS.md"]
}
```

---

## CASCADE B: ClaudeNPC Testing

**Time estimate:** 30 minutes
**Dependencies:** None
**Claimable by:** Any parallel worker

### Tasks

1. [ ] Navigate to ClaudeNPC-Server-Suite/
2. [ ] Run: `.\test-core-modules.ps1`
3. [ ] Run: `.\test-syntax.ps1`
4. [ ] Document any failures
5. [ ] Check INSTALL.ps1 for broken paths

### Completion BUMP

```json
{
  "type": "PASS",
  "from": "worker-b",
  "to": "primary",
  "task": "cascade-b-testing",
  "status": "complete",
  "test_results": { "passed": 0, "failed": 0 }
}
```

---

## CASCADE C: wave-toolkit Extraction

**Time estimate:** 15 minutes
**Dependencies:** None
**Claimable by:** Any parallel worker

### Tasks

1. [ ] Create directory: SpiralSafe/packages/wave-toolkit/
2. [ ] Copy protocol docs (wave, bump, awi, atom specs)
3. [ ] Copy template files (.context.yaml, etc.)
4. [ ] Create minimal README.md
5. [ ] Verify no game/math content included

### Completion BUMP

```json
{
  "type": "PASS",
  "from": "worker-c",
  "to": "primary",
  "task": "cascade-c-packaging",
  "status": "complete",
  "package_path": "packages/wave-toolkit/"
}
```

---

## Timing Schedule

| Time | Primary Session           | Parallel Workers        |
| ---- | ------------------------- | ----------------------- |
| T+0  | Create cascade tasks      | Read CASCADE_TASKS.md   |
| T+5  | Begin orchestration       | Claim cascade A/B/C     |
| T+15 | Monitor progress          | Work on claimed tasks   |
| T+25 | Review completed cascades | Submit completion BUMPs |
| T+35 | Integrate all work        | Await sign-off          |
| T+40 | Session sign-off          | Session complete        |

---

## Re-Task Points

If a worker finishes early, check these for additional work:

1. **Stale branch cleanup** - List and delete merged branches
2. **Security PRs** - Review #72, #73 for merge readiness
3. **API endpoint fix** - Debug /api/atom/ready 500 error
4. **Git identity normalization** - Configure toolate28 consistently

---

## Claiming Protocol

To claim a cascade:

1. Read this file
2. Check if cascade is unclaimed
3. Create file: `.claude/CLAIM_{CASCADE_LETTER}.md` with your worker ID
4. Begin work
5. On completion, post BUMP and delete claim file

---

## Primary Session Responsibilities

1. Monitor all cascades
2. Resolve conflicts
3. Integrate completed work
4. Update main tracking
5. **FINAL: Sign off via claude_local.ipynb**

---

_H&&S:WAVE | The primary session finishes last._
