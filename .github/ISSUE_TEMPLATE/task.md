---
name: Task / Chore
about: General task, maintenance, or refactoring work
title: "[TASK] "
labels: task, needs-atom-tag
assignees: ""
---

## ATOM Tag

**ATOM:** `ATOM-TASK-[DATE]-[NUM]-[description]`

_Create with:_

```bash
./scripts/atom-track.sh TASK "Task description" "issue-#N"
```

---

## Summary

Brief description of the task or maintenance work.

## Task Type

- [ ] Refactoring (improve code without changing behavior)
- [ ] Maintenance (updates, cleanup, deprecation)
- [ ] Dependency update
- [ ] Configuration change
- [ ] CI/CD improvement
- [ ] Tooling setup
- [ ] Other: [describe]

## Current State

**What exists now?**

Describe the current state of what needs work.

## Desired End State

**What should exist after this task?**

Describe the target state clearly.

## Steps / Subtasks

Break down the work into actionable steps:

- [ ] Step 1: [specific action]
- [ ] Step 2: [specific action]
- [ ] Step 3: [specific action]

## Affected Components

**What will this task touch?**

- Files: `path/to/file1`, `path/to/file2`
- Scripts: `scripts/script-name.sh`
- Workflows: `.github/workflows/workflow.yml`
- Dependencies: [list any package updates]

## Risk Assessment

**What could go wrong?**

- [ ] Low risk - Isolated change
- [ ] Medium risk - Affects multiple components
- [ ] High risk - Critical path or production impact

**Mitigation:**

- Backup/rollback plan: [describe]
- Testing approach: [describe]

## Dependencies

**What needs to happen first?**

- Depends on: Issue #XXX
- Blocks: Issue #YYY
- Related ATOM: `ATOM-XXX-YYYYMMDD-NNN`

## Testing / Verification

**How to verify this task is complete:**

```bash
# Verification commands
./scripts/test-scripts.sh
./scripts/verify-environment.sh
```

**Acceptance criteria:**

- [ ] All tests pass
- [ ] No regressions introduced
- [ ] Documentation updated
- [ ] ATOM tag logged

## Rollback Plan

**If this breaks, how to undo:**

```bash
# Rollback steps
git revert <commit>
# or specific undo steps
```

## Timeline

- **Estimated effort:** [hours/days]
- **Target completion:** [date]
- **Priority:** [Low/Medium/High/Urgent]

## Related Items

- Issue: #XXX
- PR: #YYY
- ATOM: `ATOM-XXX-YYYYMMDD-NNN`

---

## Checklist

- [ ] Task is clearly defined
- [ ] Steps are actionable
- [ ] Verification method specified
- [ ] Risks identified and mitigated
- [ ] Dependencies noted
