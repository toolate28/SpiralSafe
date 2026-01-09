#!/usr/bin/env python3
"""
Human co-sign for verification receipts.
Usage:
  ./ops/scripts/sign_verification.py ATOM-VERIFY-20260104-001-complete-system-audit --name "toolate28"

This computes SHA256 of the verification document (VERIFICATION_STAMP.md) and updates the corresponding verifications entry with the human signature hash and combined hash.
"""

import argparse, hashlib, json
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
ver_dir = repo_root / '.atom-trail' / 'verifications'
if not ver_dir.exists():
    raise SystemExit('No verifications directory found')

p = argparse.ArgumentParser()
p.add_argument('atom_tag')
p.add_argument('--name', required=True)
args = p.parse_args()

vfile = ver_dir / f"{args.atom_tag}.json"
if not vfile.exists():
    raise SystemExit(f'Verification file not found: {vfile}')

# Compute hash of verification document
vdoc = repo_root / 'VERIFICATION_STAMP.md'
if not vdoc.exists():
    raise SystemExit('VERIFICATION_STAMP.md not found')

vhash = hashlib.sha256(vdoc.read_bytes()).hexdigest()
# Human signature is hash of (vhash + name)
human_sig = hashlib.sha256((vhash + args.name).encode()).hexdigest()
combined = hashlib.sha256((vhash + human_sig).encode()).hexdigest()

data = json.loads(vfile.read_text(encoding='utf-8'))
data['human_signature_hash'] = human_sig
data['human_signed_by'] = args.name
data['combined_hash'] = combined
data['status'] = 'complete'

vfile.write_text(json.dumps(data, indent=2), encoding='utf-8')
print(f"Updated {vfile} with human signature: {human_sig}")

# Also update decision file if exists
decision = repo_root / '.atom-trail' / 'decisions' / f"{args.atom_tag}.json"
if decision.exists():
    d = json.loads(decision.read_text(encoding='utf-8'))
    d.setdefault('verification', {})
    d['verification']['human_signed'] = True
    d['verification']['human_signature_hash'] = human_sig
    d['verification']['combined_hash'] = combined
    decision.write_text(json.dumps(d, indent=2), encoding='utf-8')
    print(f"Updated decision file: {decision}")

print('Human co-sign complete.')
