import hashlib, uuid, json, datetime, os
from pathlib import Path

session = {
    'session_id': str(uuid.uuid4()),
    'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
    'agent': 'GitHub Copilot',
    'note': 'Signed session: added infra files and verification helpers'
}

payload = session['session_id'] + '|' + session['timestamp'] + '|' + os.path.basename(os.getcwd())
session['signature'] = hashlib.sha256(payload.encode('utf-8')).hexdigest()

out_dir = Path('.verification')
out_dir.mkdir(exist_ok=True)
out_file = out_dir / f"session-{session['session_id']}.json"
with out_file.open('w', encoding='utf-8') as f:
    json.dump(session, f, indent=2)

print(out_file)
print(json.dumps(session))
