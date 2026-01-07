#!/usr/bin/env python3
"""Generate repo markers manifest (.verification/repo_markers.json)

Scans selected directories for files of interest and writes a manifest mapping a
marker id (hash) to file metadata. This allows "markers" to be planted without
editing source files directly.
"""
import hashlib
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / ".verification" / "repo_markers.json"
OUT.parent.mkdir(exist_ok=True, parents=True)

TARGET_DIRS = ["museum/builds", "museum/datapacks", "server-suite/python-scripts", "showcase"]

markers = {}
for d in TARGET_DIRS:
    base = ROOT / d
    if not base.exists():
        continue
    for p in base.rglob("*"):
        if p.is_file():
            rel = str(p.relative_to(ROOT))
            h = hashlib.sha1(rel.encode()).hexdigest()[:12]
            st = p.stat()
            markers[h] = {
                "path": rel,
                "size": st.st_size,
                "modified": datetime.utcfromtimestamp(st.st_mtime).isoformat() + "Z"
            }

OUT.write_text(json.dumps({"generated": datetime.utcnow().isoformat() + "Z", "markers": markers}, indent=2))
print(f"Wrote markers to {OUT}")
