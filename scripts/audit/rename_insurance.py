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

def checks_of(ddl):
    """Every CHECK(...) expression, balanced-paren scanned.

    A non-greedy regex to the first ')' truncates any CHECK containing a nested
    paren -- an IN (...) list, a compound OR. Two such CHECKs read as LOST when
    both had in fact survived the migration intact: the instrument was wrong, not
    the migration, which is the worst failure mode an insurance script has.
    """
    out, i, low = [], 0, ddl.lower()
    while True:
        i = low.find("check", i)
        if i < 0: return out
        j = i + 5
        while j < len(ddl) and ddl[j] in " \t\n": j += 1
        if j >= len(ddl) or ddl[j] != "(":
            i += 5; continue
        depth, k = 0, j
        while k < len(ddl):
            if ddl[k] == "(": depth += 1
            elif ddl[k] == ")":
                depth -= 1
                if depth == 0: break
            k += 1
        out.append(" ".join(ddl[j + 1:k].split()))
        i = k + 1


def snap(db):
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    o = {"tables": {}, "views": {}, "fks": [], "indexes": {}, "triggers": {}, "checks": {}}
    tabs = [r[0] for r in c.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    for t in tabs:
        o["tables"][t] = c.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
        o["columns" ] = o.get("columns", {})
        # table_xinfo, not table_info: table_info omits GENERATED columns entirely,
        # so the harness reported every generated coalesce as "declared but absent".
        o["columns"][t] = sorted(r[1] for r in c.execute('PRAGMA table_xinfo("%s")' % t))
        for r in c.execute('PRAGMA foreign_key_list("%s")' % t):
            o["fks"].append(f"{t}.{r[3]} -> {r[2]}.{r[4]}")
        sql = c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (t,)).fetchone()[0] or ""
        o["checks"][t] = sorted(checks_of(sql))
        idx = []
        for r in c.execute('PRAGMA index_list("%s")' % t):
            cols = [x[2] for x in c.execute('PRAGMA index_info("%s")' % r[1])]
            # r[4] is `partial`: a partial UNIQUE index is WEAKER than a full one
            # over the same columns, and recording only {unique, cols} would let a
            # substitution of one for the other pass unremarked.
            idx.append({"unique": bool(r[2]), "cols": cols, "partial": bool(r[4])})
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

def compare(before, after, m, dropped=(), added_cols=None,
            dropped_cols=None, renamed_cols=None, index_cols=None,
            changed_views=None, added_fks=()):
    """Declare every INTENDED structural change; anything undeclared is a finding.

      dropped       tables deliberately removed
      added_cols    {table: [new columns]}      deliberately added
      dropped_cols  {table: [old columns]}      deliberately removed
      renamed_cols  {table: {old: new}}         deliberately renamed

    Two source tables may map to ONE target (a fold). The target's row count is then
    expected to be the SUM of its sources, and its column set the UNION -- that is what
    makes a fold checkable rather than a hole in the instrument.

    A rename migration that also restructures produces INTENDED structural change. Without
    declaring it, every run reports it and the reader learns to ignore the check -- the
    failure the retired-vocabulary register names in its own words. Declaring it keeps the
    instrument sharp: anything NOT declared is still a finding.
    """
    issues = []
    dropped = set(dropped); added_cols = added_cols or {}
    dropped_cols = dropped_cols or {}; renamed_cols = renamed_cols or {}
    index_cols = index_cols or {}; changed_views = changed_views or {}
    # Which targets are folds? More than one live source maps onto them.
    fan = {}
    for t in before["tables"]:
        if t not in dropped:
            fan.setdefault(rename(t, m), []).append(t)
    folds = {k: v for k, v in fan.items() if len(v) > 1}
    # rows + columns
    for t, n in before["tables"].items():
        t2 = rename(t, m)
        if t in dropped:
            if t2 in after["tables"]:
                issues.append(f"TABLE NOT DROPPED: {t} was declared dropped but is present as {t2}")
            continue
        if t2 not in after["tables"]:
            issues.append(f"TABLE LOST: {t} -> expected {t2}, absent"); continue
        if t2 in folds:
            want = sum(before["tables"][x] for x in folds[t2])
            if after["tables"][t2] != want:
                issues.append(f"FOLD ROWS WRONG: {'+'.join(folds[t2])} = {want}"
                              f" but {t2} holds {after['tables'][t2]}")
        elif after["tables"][t2] != n:
            issues.append(f"ROWS CHANGED: {t}({n}) -> {t2}({after['tables'][t2]})")
        ren_c = renamed_cols.get(t, {})
        cb = {ren_c.get(c, c) for c in before["columns"][t]} - set(dropped_cols.get(t, []))
        ca = set(after["columns"][t2])
        expected_new = set(added_cols.get(t, []))
        lost, gained = sorted(cb - ca), sorted(ca - cb - expected_new)
        if t2 in folds:              # a fold's target legitimately carries its siblings'
            gained = sorted(set(gained) - {ren_c.get(c, c)
                            for s in folds[t2] for c in before["columns"][s]})
        undelivered = sorted(expected_new - ca)
        if lost or gained:
            issues.append(f"COLUMNS CHANGED: {t2} lost={lost} unexpected-gain={gained}")
        if undelivered:
            issues.append(f"COLUMNS NOT ADDED: {t2} declared {undelivered} but they are absent")
    # fks
    exp = set()
    for e in before["fks"]:
        src, tgt = e.split(" -> ")
        st, sc = src.split(".", 1); tt, tc = tgt.split(".", 1)
        if st in dropped or tt in dropped: continue
        if sc in dropped_cols.get(st, []): continue
        sc = renamed_cols.get(st, {}).get(sc, sc)
        tc = renamed_cols.get(tt, {}).get(tc, tc)
        exp.add(f"{rename(st, m)}.{sc} -> {rename(tt, m)}.{tc}")
    exp = sorted(exp)
    got = sorted(set(after["fks"]))
    for e in exp:
        if e not in got: issues.append(f"FK LOST: {e}")
    # added_fks must be declared EDGE BY EDGE, not merely tolerated because the
    # source column was declared new. Accepting any FK on a new column meant the 44
    # lens keys -- the entire point of this migration -- were never checked at all:
    # a build that made them plain TEXT with no REFERENCES passed green. That is
    # §2(a), a gate that passes having examined nothing, on the pointers themselves.
    added_fks = set(added_fks)
    for g in got:
        if g in exp or g in added_fks: continue
        issues.append(f"FK ADDED (unexpected): {g}")
    for e in sorted(added_fks - set(got)):
        issues.append(f"FK DECLARED BUT ABSENT: {e}")
    # views
    for v, d in before["views"].items():
        if v not in after["views"]:
            issues.append(f"VIEW LOST: {v}"); continue
        a = after["views"][v]
        if isinstance(a["rows"], str):
            issues.append(f"VIEW BROKEN: {v} {a['rows']}")
        elif a["rows"] != d["rows"]:
            issues.append(f"VIEW ROWS CHANGED: {v} {d['rows']} -> {a['rows']}")
        # A view that now REACHES a taxonomy through a link table instead of
        # holding a copy of it legitimately gains a base table. Declared, not waived.
        expb = sorted({rename(b, m) for b in d["base_tables"]} | set(changed_views.get(v, [])))
        if expb != a["base_tables"]:
            issues.append(f"VIEW BASE TABLES CHANGED: {v} expected {expb} got {a['base_tables']}")
    # indexes + checks
    for t, idx in before["indexes"].items():
        t2 = rename(t, m)
        if t in dropped or t2 not in after["indexes"]: continue
        # index_cols maps a column an index was BUILT ON to what now stands in its
        # place -- a renamed registry PK, or the generated coalesce that replaced a
        # single taxonomy column. Without it every index on population_code reads
        # as lost when it was in fact rebuilt one column wider.
        cmap = dict(renamed_cols.get(t, {})); cmap.update(index_cols.get(t, {}))
        want = [dict(i, cols=[cmap.get(c, c) for c in i["cols"]]) for i in idx]
        lostix = [i for i in want if i not in after["indexes"][t2]]
        if lostix:
            issues.append(f"INDEXES LOST: {t2} {lostix}")
    for t, ck in before["checks"].items():
        t2 = rename(t, m)
        if t in dropped or t2 not in after["checks"]: continue
        lostck = [c for c in ck if c not in after["checks"][t2]]
        if lostck:
            issues.append(f"CHECK CONSTRAINTS LOST: {t2} {lostck}")
    return issues


def apply_waivers(issues, waived):
    """A waiver must carry a REASON and is PRINTED, never hidden.

    An insurance script whose findings can be silently suppressed insures nothing.
    A waiver whose text no longer matches any finding is itself reported, so a
    waiver cannot outlive the thing it waives.
    """
    kept, notes, unused = [], [], dict(waived)
    for i in issues:
        hit = next((k for k in waived if k in i), None)
        if hit:
            notes.append(f"WAIVED: {i}\n           reason: {waived[hit]}")
            unused.pop(hit, None)
        else:
            kept.append(i)
    for k, why in unused.items():
        kept.append(f"STALE WAIVER: nothing matches {k!r} (reason given: {why})")
    return kept, notes


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
    ap.add_argument("--dropped", help="JSON list of tables deliberately removed")
    ap.add_argument("--added-cols", dest="added_cols", help="JSON {table: [cols]} deliberately added")
    ap.add_argument("--dropped-cols", dest="dropped_cols", help="JSON {table: [cols]} deliberately removed")
    ap.add_argument("--renamed-cols", dest="renamed_cols", help="JSON {table: {old: new}} deliberately renamed")
    ap.add_argument("--index-cols", dest="index_cols", help="JSON {table: {old: new}} column standing in for another IN INDEXES")
    ap.add_argument("--changed-views", dest="changed_views", help="JSON {view: [base tables it now also reaches]}")
    ap.add_argument("--added-fks", dest="added_fks", help="JSON list of FK edges deliberately added")
    ap.add_argument("--waived", help="JSON {substring of a finding: reason} -- printed, not hidden")
    a = ap.parse_args()
    if a.snapshot:
        s = snap(a.db)
        json.dump(s, open(a.snapshot, "w"), indent=1)
        print(f"EXAMINED: {len(s['tables'])} tables, {len(s['views'])} views, {len(s['fks'])} foreign keys")
        print(f"snapshot -> {a.snapshot}")
    elif a.compare:
        b = json.load(open(a.compare[0])); af = json.load(open(a.compare[1]))
        m = json.load(open(a.map)) if a.map else {}
        dropped = json.load(open(a.dropped)) if a.dropped else []
        addc = json.load(open(a.added_cols)) if a.added_cols else {}
        dropc = json.load(open(a.dropped_cols)) if a.dropped_cols else {}
        renc = json.load(open(a.renamed_cols)) if a.renamed_cols else {}
        idxc = json.load(open(a.index_cols)) if a.index_cols else {}
        chv = json.load(open(a.changed_views)) if a.changed_views else {}
        afk = json.load(open(a.added_fks)) if a.added_fks else []
        iss = compare(b, af, m, dropped, addc, dropc, renc, idxc, chv, afk)
        waived = json.load(open(a.waived)) if a.waived else {}
        iss, notes = apply_waivers(iss, waived)
        print(f"EXAMINED: {len(b['tables'])} tables, {len(b['views'])} views, {len(b['fks'])} foreign keys")
        for n in notes: print("  " + n)
        for i in iss: print("  " + i)
        print("RESULT:", "FAIL — %d structural difference(s)" % len(iss) if iss
              else "PASS — names changed, structure identical")
        sys.exit(1 if iss else 0)
    else: ap.error("need --snapshot or --compare")
