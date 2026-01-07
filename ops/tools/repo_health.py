#!/usr/bin/env python3
"""Repo health scanner

Runs a set of quick diagnostics and writes a JSON report to .verification/

Checks performed:
- Run pytest (if present)
- Markdown link status (HTTP HEAD with timeout)
- Orphan detection by filename reference (git grep)
- Datapack sanity (pack.mcmeta present, mcfunction presence)
- Collect file metadata for selected paths

Usage: python ops/tools/repo_health.py --output .verification/repo_health-YYYYMMDD-HHMMSS.json
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import shutil

try:
    import requests
except Exception:
    requests = None

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / ".verification"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MARKED_EXTS = [".schem", ".nbt", ".json", ".mcfunction", ".schematic", ".md"]


def run_cmd(cmd, cwd=ROOT, timeout=30):
    try:
        p = subprocess.run(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout, universal_newlines=True)
        return p.returncode, p.stdout
    except subprocess.TimeoutExpired:
        return 2, "Timed out"


def run_pytest():
    rc, out = run_cmd("python -m pytest -q", timeout=300)
    return {"rc": rc, "output": out}


def check_markdown_links(max_check=200, timeout=5):
    files = list(ROOT.rglob("*.md"))
    urls = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore")
        for token in text.split():
            if token.startswith("http://") or token.startswith("https://"):
                urls.append((str(f.relative_to(ROOT)), token.strip("\),.\n\r'\"")))
    # dedupe
    urls = list(dict.fromkeys(urls))
    report = []
    if requests is None:
        return {"skipped": True, "reason": "requests not installed", "checked": 0}
    for i, (src, url) in enumerate(urls):
        if i >= max_check:
            break
        try:
            r = requests.head(url, allow_redirects=True, timeout=timeout)
            status = r.status_code
        except Exception as e:
            status = str(e)
        report.append({"source": src, "url": url, "status": status})
    return {"skipped": False, "checked": len(report), "results": report}


def find_orphans():
    # Find files with target extensions and check if their basename appears in the repo
    orphans = []
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in MARKED_EXTS:
            name = p.name
            rc, out = run_cmd(f"git grep -n \"{name}\" || true")
            if rc != 0 and not out.strip():
                orphans.append(str(p.relative_to(ROOT)))
    return orphans


def check_datapacks():
    results = []
    dp_root = ROOT / "museum" / "datapacks"
    if not dp_root.exists():
        return {"exists": False, "detail": "no datpacks folder"}
    for dp in dp_root.iterdir():
        pack = dp / "pack.mcmeta"
        funcs = list((dp / "data").rglob("*.mcfunction")) if (dp / "data").exists() else []
        results.append({"datapack": str(dp.relative_to(ROOT)), "pack_mcmeta_present": pack.exists(), "functions_count": len(funcs)})
    return {"exists": True, "datapacks": results}


def collect_file_metadata(paths):
    meta = []
    for p in paths:
        pp = ROOT / p
        if not pp.exists():
            meta.append({"path": p, "exists": False})
            continue
        st = pp.stat()
        meta.append({"path": p, "exists": True, "size": st.st_size, "modified": st.st_mtime})
    return meta


def run_all(output_path):
    report = {"timestamp": datetime.utcnow().isoformat() + "Z", "results": {}}
    print("Running pytest...")
    report["results"]["pytest"] = run_pytest()

    print("Checking markdown links (HTTP HEAD)...")
    report["results"]["md_links"] = check_markdown_links()

    print("Detecting orphan files...")
    report["results"]["orphans"] = find_orphans()

    print("Checking datapacks...")
    report["results"]["datapacks"] = check_datapacks()

    print("Collecting metadata for core files...")
    core_files = ["museum/builds/logic-gates.json", "museum/builds/binary-counter.json", "server-suite/python-scripts/quantum_circuit_generator.py", "README.md"]
    report["results"]["core_files"] = collect_file_metadata(core_files)

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(report, indent=2))
    print(f"Report written: {out_file}")
    # Exit with non-zero if any critical failures found
    rc = 0
    if report["results"]["pytest"]["rc"] != 0:
        rc = 2
    if report["results"]["md_links"].get("skipped") is True:
        print("Note: Markdown link checks skipped (requests not installed)")
    return rc


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUT_DIR / f"repo_health-{int(time.time())}.json"))
    args = parser.parse_args()
    rc = run_all(args.output)
    sys.exit(rc)
