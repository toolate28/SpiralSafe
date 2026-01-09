#!/usr/bin/env python3
"""
Session report helper for SpiralSafe
Usage:
  ./session_report.py start "description"
  ./session_report.py signout ATOM-SESSION-20260107-001-description

Creates session JSON files under .atom-trail/sessions and signs out by generating a report and calling Transcript-Pipeline.ps1 to encrypt it.
"""

import argparse
import json
import hashlib
import time
import uuid
import getpass
import socket
import subprocess
from pathlib import Path
from datetime import datetime

repo_root = Path(__file__).resolve().parents[2]
sessions_dir = repo_root / '.atom-trail' / 'sessions'
sessions_dir.mkdir(parents=True, exist_ok=True)

def _next_seq_for_date(date_str: str) -> int:
    files = list(sessions_dir.glob(f'ATOM-SESSION-{date_str}-*.json'))
    return len(files) + 1


def start_session(description: str = 'session') -> dict:
    now = datetime.utcnow()
    date_str = now.strftime('%Y%m%d')
    seq = _next_seq_for_date(date_str)
    tag = f'ATOM-SESSION-{date_str}-{seq:03d}-{description}'
    start_epoch = int(time.time())
    nonce = uuid.uuid4().hex
    session_hash = hashlib.sha256((tag + str(start_epoch) + nonce).encode()).hexdigest()

    session = {
        'atom_tag': tag,
        'type': 'session',
        'description': description,
        'start_epoch': start_epoch,
        'start_iso': now.isoformat() + 'Z',
        'created_by': getpass.getuser(),
        'host': socket.gethostname(),
        'nonce': nonce,
        'session_hash': session_hash,
        'signed': True
    }

    path = sessions_dir / f"{tag}.json"
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(session, fh, indent=2)

    print(f"Session started: {tag}")
    print(f"Hash: {session_hash}")
    return session


def sign_out(tag: str) -> dict:
    path = sessions_dir / f"{tag}.json"
    if not path.exists():
        raise FileNotFoundError(f'Session file not found: {path}')

    with open(path, 'r', encoding='utf-8') as fh:
        session = json.load(fh)

    end_epoch = int(time.time())
    session['end_epoch'] = end_epoch
    session['end_iso'] = datetime.utcfromtimestamp(end_epoch).isoformat() + 'Z'

    decisions_dir = repo_root / '.atom-trail' / 'decisions'
    session_decisions = []
    if decisions_dir.exists():
        for f in decisions_dir.glob('*.json'):
            try:
                d = json.loads(f.read_text(encoding='utf-8'))
                created = d.get('created_epoch') or d.get('created') or d.get('timestamp')
                if created and isinstance(created, int) and session['start_epoch'] <= created <= end_epoch:
                    session_decisions.append({'file': str(f.name), 'id': d.get('atom_tag') or d.get('id')})
            except Exception:
                continue

    report = {
        'session': session,
        'decisions': session_decisions,
        'generated_at': int(time.time())
    }

    report_path = sessions_dir / f"{tag}-report.json"
    with open(report_path, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=2)

    print(f"Session report written: {report_path}")

    # Try encryption via Transcript-Pipeline.ps1
    script = repo_root / 'ops' / 'scripts' / 'Transcript-Pipeline.ps1'
    if script.exists():
        cmd = [
            'pwsh',
            '-NoProfile',
            '-File',
            str(script),
            '-Action',
            'Encrypt',
            '-InputPath',
            str(report_path),
        ]
        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
            )
            print('Encryption command executed (check transcript.encrypted.json near the report output)')
        except subprocess.CalledProcessError as e:
            print('Encryption command failed with non-zero exit status.')
            print('  Command:', e.cmd)
            print('  Return code:', e.returncode)
            if e.stdout:
                print('  Stdout:', e.stdout.strip())
            if e.stderr:
                print('  Stderr:', e.stderr.strip())
        except OSError as e:
            print('Failed to execute encryption command:', e)
            print('  Command:', cmd)
    else:
        print('Transcript-Pipeline.ps1 not found; encrypted output not generated')

    # Save updated session
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(session, fh, indent=2)

    return report


def main():
    p = argparse.ArgumentParser(description='Session report helper')
    sub = p.add_subparsers(dest='cmd')

    s_start = sub.add_parser('start')
    s_start.add_argument('description', nargs='?', default='session')

    s_sign = sub.add_parser('signout')
    s_sign.add_argument('tag', help='ATOM session tag to close')

    args = p.parse_args()
    if args.cmd == 'start':
        start_session(args.description)
    elif args.cmd == 'signout':
        sign_out(args.tag)
    else:
        p.print_help()

if __name__ == '__main__':
    main()
