#!/usr/bin/env python3
"""T-019 F8: what the lens routing changes on the live corpus, cell by cell (a comparison, not a gate).

Re-run from the repository root, with the base engine extracted beside it (no worktree):
    mkdir -p "$D/base" && git archive origin/task/t-018-link-table scripts/assess scripts/dbcore.py schemas | tar -x -C "$D/base"
    python3 -I scratchpad/session_2026-11-13-t019-lens-gather/compare_live.py "$D/base" . "$D"

For every ACTIVE parameter and each identity lens below it runs assess_cell.py from each engine tree on its own
scratch copy of the canonical database (--report-json per cell, the same session and stamp), then prints, per
cell: written or refused on each side, state, and every report key that differs (derivation_sha, row ids and the
link list are not compared; the renamed count keys are compared as in_lens). Nothing is typed: the parameters
come from base_parameters, the lenses are the argument below.
"""
import json
import os
import shutil
import sqlite3
import subprocess
import sys

BASE_TREE, HEAD_TREE, WORK = (os.path.abspath(a) for a in sys.argv[1:4])
LENSES = ("ALL", "BLIND", "MOB", "MS", "SCI", "DEAF")
SKIP = {"derivation_sha", "specification_id", "gap_register_id", "convergence_id", "links", "n_extractions",
        "n_extractions_in_lens", "n_extractions_outside_lens", "unkeyed_models", "source_records", "slug", "note"}
DB = os.path.join(HEAD_TREE, "data", "guidebook.db")
params = [r[0] for r in sqlite3.connect(f"file:{DB}?mode=ro", uri=True).execute(
    "SELECT parameter_id FROM base_parameters WHERE status='active' ORDER BY 1")]


def run(tree, copy, pid, ident):
    rj = os.path.join(WORK, f"cmp-{os.path.basename(tree)}-{pid}-{ident}.json")
    r = subprocess.run([sys.executable, os.path.join(tree, "scripts/assess/assess_cell.py"), "--db", copy,
                        "--emit-sql", os.path.join(WORK, "cmp.sql"), "--parameter-id", str(pid), "--slug",
                        "accessible-circulation-geometry", "--identity", ident, "--session",
                        "session_task-probe", "--stamp", "2026-01-01 00:00", "--report-json", rj],
                       capture_output=True, text=True)
    rep = json.load(open(rj))[0] if r.returncode == 0 and os.path.exists(rj) else None
    if os.path.exists(rj):
        os.remove(rj)
    return rep, (r.stdout + r.stderr).strip().splitlines()[:1]


copies = {}
for name, tree in (("base", BASE_TREE), ("head", HEAD_TREE)):
    copies[name] = os.path.join(WORK, f"cmp-{name}.db")
    shutil.copy(DB, copies[name])
written = refused = changed = 0
for pid in params:
    for ident in LENSES:
        b, bl = run(BASE_TREE, copies["base"], pid, ident)
        h, hl = run(HEAD_TREE, copies["head"], pid, ident)
        if b is None or h is None:
            print(f"param {pid} x {ident}: base {'written' if b else 'REFUSED'}, head "
                  f"{'written' if h else 'REFUSED'}" + (f"  [{hl[0][:90]}]" if not h and hl else ""))
            written += bool(h)
            refused += not h
            continue
        written += 1
        keys = sorted(k for k in set(b) & set(h) if k not in SKIP and b[k] != h[k])
        if keys:
            changed += 1
            print(f"param {pid} x {ident}: {b['state']} -> {h['state']}; changed: "
                  + ", ".join(f"{k} {json.dumps(b[k])[:40]} -> {json.dumps(h[k])[:40]}" for k in keys))
print(f"cells: {len(params) * len(LENSES)}; head writes {written}, refuses {refused}; "
      f"written cells whose report differs from the base: {changed}")
for c in copies.values():
    os.remove(c)
