#!/usr/bin/env bash
set -euo pipefail

# Simple redaction utility for logs.
# Usage: scripts/redact-log.sh input.jsonl output.jsonl

if [ $# -ne 2 ]; then
  echo "Usage: $0 input.jsonl output.jsonl"
  exit 1
fi

INPUT="$1"
OUTPUT="$2"

# Patterns to redact (case-insensitive)
RE_PATTERNS=('api_key' 'secret' 'password' 'authorization' 'token' 'access_key' 'private_key')

# Copy and redact lines
mkdir -p "$(dirname "$OUTPUT")"
while IFS= read -r line; do
  redacted="$line"
  for pat in "${RE_PATTERNS[@]}"; do
    redacted=$(echo "$redacted" | sed -E "s/(${pat}\":\")[^\"]+\"/\1<REDACTED>\"/Ig")
    redacted=$(echo "$redacted" | sed -E "s/(${pat}=)[^[:space:]]+/\1<REDACTED>/Ig")
  done
  echo "$redacted" >> "$OUTPUT"
done < "$INPUT"
exit 0
