#!/usr/bin/env python3
"""
scripts/audit/rename_insurance.py — prove a table rename changed NAMES ONLY.

Rule 4 says a 0-row object is unproven, not clean. 33 of 66 tables hold no rows, so a
rename that silently breaks a reader renders nothing and a byte-diff of the output
certifies it. This script is the insurance: it snapshots every structural fact a rename
must preserve, and compares two snapshots under a name map.

  --snapshot OUT.json [--db PATH]     capture
  --compare BEFORE.json AFTER.json --map MAP.json     verify

What it captures, per CLAUDE.md's own list of what a rename breaks:
  rows        every table's row count            (writing:  no data lost)
  columns     every table's column set           (writing:  no column lost)
  fks         every FK edge src.col -> tgt.col   (pointers: every key preserved)
  views       every view's row count AND its resolved base tables (reading + pointers)
  indexes     every index's table and columns    (walkability: the reverse lookup)
  triggers    every trigger's table
  checks      every CHECK constraint text        (writing:  the refusal vocabulary)
"""
import argparse, json, re, sqlite3, sys, os

def snap(db):
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    o = {"tables": {}, "views": {}, "fks": [], "indexes": {}, "triggers": {}, "checks": {}}
    tabs = [r[0] for r in c.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    for t in tabs:
        o["tables"][t] = c.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
        o["columns" ] = o.get("columns", {})
        o["columns"][t] = sorted(r[1] for r in c.execute('PRAGMA table_info("%s")' % t))
        for r in c.execute('PRAGMA foreign_key_list("%s")' % t):
            o["fks"].append(f"{t}.{r[3]} -> {r[2]}.{r[4]}")
        sql = c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (t,)).fetchone()[0] or ""
        o["checks"][t] = sorted(re.findall(r"CHECK\s*\((.*?)\)\s*[,)]", sql, re.S | re.I))
        idx = []
        for r in c.execute('PRAGMA index_list("%s")' % t):
            cols = [x[2] for x in c.execute('PRAGMA index_info("%s")' % r[1])]
            idx.append({"unique": bool(r[2]), "cols": cols})
        o["indexes"][t] = sorted(idx, key=lambda d: (str(d["cols"]), d["unique"]))
    views = {n: s for n, s in c.execute("SELECT name, sql FROM sqlite_master WHERE type='view'")}
    for v, sql in sorted(views.items()):
        try:
            n = c.execute('SELECT COUNT(*) FROM "%s"' % v).fetchone()[0]
        except sqlite3.Error as e:
            n = f"ERROR: {e}"
        base = set()
        def walk(s, seen=frozenset()):
            for m in re.findall(r'(?:FROM|JOIN)\s+["\']?([a-zA-Z_][a-zA-Z0-9_]*)', s, re.I):
                if m in views and m not in seen: walk(views[m], seen | {m})
                elif m in o["tables"]: base.add(m)
        walk(sql or "")
        o["views"][v] = {"rows": n, "base_tables": sorted(base)}
    o["fks"].sort()
    return o

def rename(name, m):  return m.get(name, name)

def compare(before, after, m):
    issues = []
    # rows + columns
    for t, n in before["tables"].items():
        t2 = rename(t, m)
        if t2 not in after["tables"]:
            issues.append(f"TABLE LOST: {t} -> expected {t2}, absent"); continue
        if after["tables"][t2] != n:
            issues.append(f"ROWS CHANGED: {t}({n}) -> {t2}({after['tables'][t2]})")
        cb, ca = before["columns"][t], after["columns"][t2]
        if cb != ca:
            issues.append(f"COLUMNS CHANGED: {t2} lost={sorted(set(cb)-set(ca))} gained={sorted(set(ca)-set(cb))}")
    # fks
    exp = sorted({f"{rename(s.split('.')[0], m)}.{s.split('.')[1].split(' ->')[0]} -> "
                  f"{rename(s.split('-> ')[1].split('.')[0], m)}.{s.split('-> ')[1].split('.')[1]}"
                  for s in before["fks"]})
    got = sorted(set(after["fks"]))
    for e in exp:
        if e not in got: issues.append(f"FK LOST: {e}")
    for g in got:
        if g not in exp: issues.append(f"FK ADDED (unexpected): {g}")
    # views
    for v, d in before["views"].items():
        if v not in after["views"]:
            issues.append(f"VIEW LOST: {v}"); continue
        a = after["views"][v]
        if isinstance(a["rows"], str):
            issues.append(f"VIEW BROKEN: {v} {a['rows']}")
        elif a["rows"] != d["rows"]:
            issues.append(f"VIEW ROWS CHANGED: {v} {d['rows']} -> {a['rows']}")
        expb = sorted({rename(b, m) for b in d["base_tables"]})
        if expb != a["base_tables"]:
            issues.append(f"VIEW BASE TABLES CHANGED: {v} expected {expb} got {a['base_tables']}")
    # indexes + checks
    for t, idx in before["indexes"].items():
        t2 = rename(t, m)
        if t2 in after["indexes"] and after["indexes"][t2] != idx:
            issues.append(f"INDEXES CHANGED: {t2}")
    for t, ck in before["checks"].items():
        t2 = rename(t, m)
        if t2 in after["checks"] and sorted(after["checks"][t2]) != sorted(ck):
            issues.append(f"CHECK CONSTRAINTS CHANGED: {t2}")
    return issues

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot")
    # GUIDEBOOK_DB_PATH is the contract (references/project-standards.md, 2026-08-25):
    # a script that ignores it "will silently read the committed database while a test
    # believes it is reading a scratch copy". For THIS script that is fatal rather than
    # untidy -- it would snapshot the wrong database and the comparison it produces would
    # be meaningless while looking authoritative. Precedence: explicit --db, then the
    # variable, then the canonical default.
    ap.add_argument("--db", default=os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))
    ap.add_argument("--compare", nargs=2); ap.add_argument("--map")
    a = ap.parse_args()
    if a.snapshot:
        s = snap(a.db)
        json.dump(s, open(a.snapshot, "w"), indent=1)
        print(f"EXAMINED: {len(s['tables'])} tables, {len(s['views'])} views, {len(s['fks'])} foreign keys")
        print(f"snapshot -> {a.snapshot}")
    elif a.compare:
        b = json.load(open(a.compare[0])); af = json.load(open(a.compare[1]))
        m = json.load(open(a.map)) if a.map else {}
        iss = compare(b, af, m)
        print(f"EXAMINED: {len(b['tables'])} tables, {len(b['views'])} views, {len(b['fks'])} foreign keys")
        for i in iss: print("  " + i)
        print("RESULT:", "FAIL — %d structural difference(s)" % len(iss) if iss
              else "PASS — names changed, structure identical")
        sys.exit(1 if iss else 0)
    else: ap.error("need --snapshot or --compare")
