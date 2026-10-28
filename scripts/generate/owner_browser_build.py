#!/usr/bin/env python3
"""
scripts/generate/owner_browser_build.py -- build the owner's browser page.

WHAT THIS IS. One HTML file that opens the guidebook database inside the viewer (sql.js, WebAssembly), so the
owner can read every table, follow every pointer and see what is waiting on them, from a phone. The request and
the owner's answer on the code it adds: references/project-standards.md, "Owner statement 2026-10-28".

WHAT IT INJECTS. The page derives tables, columns, keys, pointers and views from the embedded database. It cannot
derive four things, each read from its single home: the stage of a table (governance/stage-map.yaml), the
vocabularies and CHECK shapes (dbcore.check_values / check_expression), the determinations a source holds up
(dbcore.determinations_resting_on), and the glossary and queue (governance/owner-browser.yaml).

THE OUTPUT IS NEVER COMMITTED. --out inside the repository is refused: a rendered page is not a pipeline object
(workplan T-5, the report's K-13) and the repository's scratchpad/ is committed by rule 6. Publish the file as a
private Artifact. The output is a pure function of the database, the commit and the two YAML files.

USAGE
  python3 scripts/generate/owner_browser_build.py --out /tmp/owner-browser/index.html [--db PATH] [--wasm PATH]
  --db defaults to GUIDEBOOK_DB_PATH, else the canonical file (opened read-only). --wasm skips the download.
Exit codes: 0 ok; 2 refused or misconfigured.
"""
import argparse
import base64
import hashlib
import json
import os
import subprocess
import sys
import urllib.request

import yaml

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "scripts"))
import dbcore  # noqa: E402

SQLJS_URL = "https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.3/"
SQLJS_WASM_SHA256 = "d7e61b828523001f26ce0b3f88dabcf6c12e5e6edf80eb4f08b26ac7b946ff88"
MAX_BYTES = 16 * 1024 * 1024  # the Artifact page limit


def load(name):
    with open(os.path.join(REPO, "governance", name), encoding="utf-8") as f:
        return yaml.safe_load(f)


def meta(conn, db_file):
    stages, owner = load("stage-map.yaml"), load("owner-browser.yaml")
    tables = [t for (t,) in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY 1")]
    vocab, shape = {}, {}
    for t in tables:
        for c in dbcore.columns(conn, t):
            if (v := dbcore.check_values(conn, t, c)):
                vocab.setdefault(t, {})[c] = sorted(v)
            elif (e := dbcore.check_expression(conn, t, c)):
                shape.setdefault(t, {})[c] = e
    refs = [r for (r,) in conn.execute("SELECT ref_id FROM evidence_sources ORDER BY 1")]
    holds = {r: d for r in refs if (d := dbcore.determinations_resting_on(conn, r))}
    for what, bad in (("table with no gloss", set(tables) - set(owner["glossary"])),
                      ("gloss with no table", set(owner["glossary"]) - set(tables)),
                      ("table with no stage", set(tables) - set(stages["tables"]))):
        for t in sorted(bad):
            print(f"owner_browser_build: {what}: {t}", file=sys.stderr)
    order = [s["id"] if isinstance(s, dict) else s for s in load("pipeline-contract.yaml")["stages"]]
    commit = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    with open(db_file, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    return {
        "stamp": {"sha256": sha, "user_version": conn.execute("PRAGMA user_version").fetchone()[0], "commit": commit or "unknown"},
        "stage_order": order + ["infrastructure"], "stage": stages["tables"],
        "stage_judged": {"by": stages["judged_by"], "on": stages["judged_on"]},
        "vocab": vocab, "shape": shape, "holds": holds,
        "glossary": owner["glossary"], "words": owner["words"], "decisions": owner["decisions"], "queue": owner["queue"],
        "gloss_status": {k: owner[k] for k in ("drafted_by", "drafted_on", "ratified_by", "ratified_on")},
    }


def wasm_bytes(path):
    if path:
        with open(path, "rb") as f:
            b = f.read()
    else:
        b = urllib.request.urlopen(SQLJS_URL + "sql-wasm.wasm", timeout=60).read()
    if hashlib.sha256(b).hexdigest() != SQLJS_WASM_SHA256:
        sys.exit("owner_browser_build: sql-wasm.wasm does not match the pinned sha256")
    return b


def main():
    ap = argparse.ArgumentParser(description="Build the owner's browser page (never into the repository).")
    ap.add_argument("--out", required=True)
    ap.add_argument("--db")
    ap.add_argument("--wasm")
    a = ap.parse_args()
    out = os.path.realpath(a.out)
    if out == REPO or out.startswith(REPO + os.sep):
        print(f"owner_browser_build: refusing to write inside the repository ({out}); a rendered page is not committed.", file=sys.stderr)
        return 2
    db_file = str(a.db or dbcore.db_path())
    with open(db_file, "rb") as f:
        db_b64 = base64.b64encode(f.read()).decode()
    with open(os.path.join(REPO, "scripts", "generate", "owner_browser.html"), encoding="utf-8") as f:
        html = f.read()
    with dbcore.connect(readonly=True, path=db_file) as conn:
        m = json.dumps(meta(conn, db_file), separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    for token, value in (("__SQLJS_JS__", SQLJS_URL + "sql-wasm.js"), ("__META__", m),
                         ("__WASM_B64__", base64.b64encode(wasm_bytes(a.wasm)).decode()), ("__DB_B64__", db_b64)):
        html = html.replace(token, value, 1)
    if len(html.encode()) > MAX_BYTES:
        print("owner_browser_build: the page exceeds the 16 MB Artifact limit.", file=sys.stderr)
        return 2
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"owner_browser_build: wrote {out} ({len(html.encode())} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
