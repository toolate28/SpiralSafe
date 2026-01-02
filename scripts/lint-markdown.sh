#!/usr/bin/env bash
# Markdown linting using markdownlint-cli if available
set -euo pipefail

EXIT_CODE=0

echo "=== Markdown Linting ==="
echo ""

# Check if markdownlint is available
if ! command -v markdownlint >/dev/null 2>&1; then
  echo "⚠ markdownlint-cli not installed"
  echo "Install with: npm install -g markdownlint-cli"
  echo "Skipping markdown linting..."
  exit 0
fi

# Create a basic config
cat > .markdownlint.json <<'EOF'
{
  "default": true,
  "MD013": false,
  "MD033": false,
  "MD041": false,
  "MD034": false
}
EOF

echo "Linting markdown files..."

# Find and lint markdown files
if ! markdownlint ./*.md 2>&1; then
  echo "✗ Some markdown files have issues"
  EXIT_CODE=1
else
  echo "✓ All markdown files passed linting"
fi

exit $EXIT_CODE
