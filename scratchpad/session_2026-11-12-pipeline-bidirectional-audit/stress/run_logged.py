#!/usr/bin/env python3
"""Run ONE command against a SCRATCH database and log everything about it.

    python3 -I run_logged.py --db SCRATCH.db --log LOG.jsonl --tag SCENARIO [--note TEXT] -- CMD ARG...

Sets GUIDEBOOK_DB_PATH=SCRATCH.db for the child only (the harness resets env between shells, so this is
inline on every call, as CLAUDE.md §4 requires). Refuses the canonical database. Appends one JSON line:
tag, note, argv, cwd, rc, seconds, stdout, stderr (full, untruncated), per-table row counts before/after
and the tables that changed, and the sha256 of the canonical DB before/after (it must never move).
Prints the first 3000 characters of stdout/stderr plus rc and the changed-table summary, so the caller
reads the headline and the log holds the rest.
"""
import argparse, hashlib, json, os, sqlite3, subprocess, sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]  # the scripts live inside the checkout they test
CANON = REPO / "data/guidebook.db"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def counts(db):
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        out = {}
        for (t,) in con.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'"):
            out[t] = con.execute(f'select count(*) from "{t}"').fetchone()[0]
        return out
    finally:
        con.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--note", default="")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--cwd", default=str(REPO), help="run in this directory (e.g. a clone, for write-path replays that write into the tree)")
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
    db = Path(a.db).resolve()
    if db == CANON.resolve() or not db.exists():
        sys.exit(f"REFUSED: --db must be an existing scratch copy, not the canonical database ({db})")
    sha0 = sha(CANON)
    before = counts(db)
    env = dict(os.environ, GUIDEBOOK_DB_PATH=str(db))
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=a.cwd, env=env, capture_output=True, text=True, timeout=a.timeout)
        rc, so, se = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        rc, so, se = "TIMEOUT", (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or ""), "timeout"
    dt = round(time.time() - t0, 2)
    try:
        after = counts(db)
    except Exception as e:  # a command can leave the scratch DB unreadable; that is itself a behaviour
        after = {"__unreadable__": str(e)}
    changed = {t: [before.get(t), after.get(t)] for t in set(before) | set(after) if before.get(t) != after.get(t)}
    sha1 = sha(CANON)
    rec = dict(tag=a.tag, note=a.note, argv=cmd, cwd=a.cwd, db=str(db), rc=rc, seconds=dt,
               stdout=so, stderr=se, rows_before_after_changed=changed,
               canonical_sha256_before=sha0, canonical_sha256_after=sha1, canonical_moved=(sha0 != sha1),
               at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    with open(a.log, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"[{a.tag}] rc={rc} {dt}s changed={json.dumps(changed, ensure_ascii=False)}"
          f"{'  !!CANONICAL MOVED!!' if sha0 != sha1 else ''}")
    print("--- stdout (first 3000) ---\n" + (so or "")[:3000])
    if se:
        print("--- stderr (first 3000) ---\n" + se[:3000])


main()
