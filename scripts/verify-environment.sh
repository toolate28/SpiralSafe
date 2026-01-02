#!/usr/bin/env bash
set -euo pipefail

# Simple environment verification script used by build agents.
# Exits non-zero if a critical expectation is not met.

echo "Verifying environment..."

# Python
if command -v python3 >/dev/null 2>&1; then
  PYVER=$(python3 --version 2>&1 || true)
  echo "Python: $PYVER"
else
  echo "ERROR: python3 not found"
  exit 1
fi

# pytest
if python3 -c "import pytest" >/dev/null 2>&1; then
  echo "pytest: available"
else
  echo "WARNING: pytest not importable (may be missing). Try: pip install pytest"
fi

# node (optional)
if command -v node >/dev/null 2>&1; then
  NODEVER=$(node --version 2>&1 || true)
  echo "Node: $NODEVER"
else
  echo "Node: not present (OK if not required)"
fi

# .claude orientation presence
if [ -f .claude/ORIENTATION.md ]; then
  echo "ORIENTATION: OK"
else
  echo "WARNING: .claude/ORIENTATION.md not found; create one to reduce friction"
fi

# Verify logs dir writable
mkdir -p .claude/logs
if [ -w .claude/logs ]; then
  echo "logs: writable"
else
  echo "ERROR: .claude/logs not writable"
  exit 1
fi

echo "ENV OK"
exit 0
