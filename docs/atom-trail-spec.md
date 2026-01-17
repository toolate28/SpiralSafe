---
title: ATOM Trail Spec (stub)
status: draft
---

# ATOM Trail Specification (stub)

This file is a placeholder for the ATOM trail format specification. It was created to satisfy an internal link from `bridges/README.md`.

TODO: Replace this stub with the full ATOM format spec. Suggested contents:

- entry timestamp format (ISO 8601)
- entry type (INFO|ERROR|STATUS|CONFIG)
- message field
- optional JSON context field
- example lines and parsing guidance

Example entry (single-line ATOM):

```
[2026-01-05T08:00:00Z] ERROR: Connection failed | {"host": "device0", "attempt": 3}
```

For now this file is intentionally minimal. Please expand into a full spec as needed.
