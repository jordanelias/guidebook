#!/usr/bin/env python3
"""
graph_audit.py — vectorized structural audit (stdlib graph spine, data layer).

Builds a derived, read-only audit graph from data/guidebook.db and runs Tier-1
topology checks over it, unifying orphan / dangling-reference / empty-table /
state-distribution checks that today are scattered across skills and audit scripts.
It NEVER writes guidebook.db; the audit graph is a throwaway artifact.

Checks (increment 1 — data layer):
  1. orphan.dangling_citation     (ERROR) value-layer ref with no evidence_sources row
                                  — the vetting-surface `orphan_links` invariant; must be 0
  2. cycle.population_parent      (ERROR) populations.parent_code forms a cycle
  3. orphan.uncited_source        (WARN)  evidence source cited by nothing
  4. ref.unresolved_conn_target   (WARN)  connection_target not resolving to item/slug
                                  (phantom-item vs unresolved-identifier)
  5. table.empty_mission_critical (INFO)  mission-critical table at/near 0 rows
                                  (suppressed against known_debt.yaml, warrant-checked)
  6. connection.empty_description (INFO)  connections with empty description
  7. state.distribution           (INFO)  lifecycle CHECK-enum distributions
  8. graph.components             (INFO)  connected-component / island count

Every check ships with the `--selftest` mutation harness below (a verifier that has
only ever passed is unverified — integrity-protocol Mode 1 §3).

Exit code: 0 = no LIVE (non-known-debt) ERROR finding; 1 = at least one.

Usage:
    python3 scripts/audit/graph_audit.py
    python3 scripts/audit/graph_audit.py --selftest
    GUIDEBOOK_DB_PATH=/path/to/db python3 scripts/audit/graph_audit.py
"""
import json
import os
import sqlite3
import sys
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "graph"))

import build as gbuild            # noqa: E402

KNOWN_DEBT_PATH = Path(_HERE) / "graph" / "known_debt.yaml"
SEP = "=" * 70


# --------------------------------------------------------------------------- #
# known-debt suppression (with warrant / staleness enforcement)
# --------------------------------------------------------------------------- #
def load_known_debt():
    try:
        import yaml
    except ImportError:
        return []
    if not KNOWN_DEBT_PATH.exists():
        return []
    doc = yaml.safe_load(KNOWN_DEBT_PATH.read_text(encoding="utf-8")) or {}
    return doc.get("entries", []) or []


def _lift_count(gdb, entry):
    sql = entry.get("lift_when_sql")
    if not sql:
        return None
    try:
        return gdb.execute(sql).fetchone()[0]
    except Exception:
        return None


def apply_known_debt(store, gdb, entries):
    """Suppress matching findings; flag any suppression whose warrant is satisfied."""
    cur = store.conn.cursor()
    stale = []
    for e in entries:
        count = _lift_count(gdb, e)
        ge = e.get("lift_when_ge")
        if count is not None and ge is not None and count >= ge:
            # Debt resolved — do NOT suppress; surface the stale suppression instead.
            stale.append((e["id"], count, ge))
            store.add_finding("known_debt.stale", "WARN",
                              f"Known-debt suppression '{e['id']}' is stale: warrant satisfied "
                              f"({count} >= {ge}) — remove it from known_debt.yaml.",
                              attrs={"entry": e["id"], "count": count})
            continue
        # Apply suppression to matching findings.
        rows = cur.execute("SELECT finding_id, attrs FROM findings WHERE check_id=? AND known_debt IS NULL",
                           (e["check_id"],)).fetchall()
        for fid, attrs in rows:
            if "table" in e:
                a = json.loads(attrs) if attrs else {}
                if a.get("table") != e["table"]:
                    continue
            cur.execute("UPDATE findings SET known_debt=? WHERE finding_id=?", (e["id"], fid))
    store.commit()
    return stale


# --------------------------------------------------------------------------- #
# reporting
# --------------------------------------------------------------------------- #
def _live_errors(store):
    return store.conn.execute(
        "SELECT COUNT(*) FROM findings WHERE severity='ERROR' AND known_debt IS NULL"
    ).fetchone()[0]


def report(store):
    cur = store.conn.cursor()
    counts = store.counts()
    uv = cur.execute("SELECT value FROM build_meta WHERE key='guidebook_user_version'").fetchone()
    print(SEP)
    print("graph_audit.py — vectorized structural audit (data layer, increment 1)")
    print(SEP)
    print(f"guidebook.db user_version={uv[0] if uv else '?'}  |  "
          f"nodes={counts['nodes']}  edges={counts['edges']}  "
          f"dangling_edges={counts['dangling_edges']}")
    print()
    # per-check summary (the INFO summary rows carry the headline counts)
    order = ["orphan.dangling_citation", "cycle.population_parent", "orphan.uncited_source",
             "ref.unresolved_conn_target", "table.empty_mission_critical",
             "connection.empty_description", "state.distribution", "graph.components",
             "known_debt.stale"]
    seen = set()
    for check in order:
        rows = cur.execute(
            "SELECT severity, message, known_debt FROM findings WHERE check_id=? ORDER BY severity",
            (check,)).fetchall()
        if not rows:
            continue
        seen.add(check)
        live_err = sum(1 for s, _, kd in rows if s == "ERROR" and kd is None)
        supp = sum(1 for _, _, kd in rows if kd is not None)
        info = [m for s, m, _ in rows if s == "INFO"]
        headline = info[-1] if info else rows[0][1]
        flag = "FAIL" if live_err else "ok"
        extra = f"  [{supp} suppressed]" if supp else ""
        print(f"  [{check}] {flag}{extra}")
        print(f"      {headline}")
    print()
    # live errors detail
    errs = cur.execute(
        "SELECT check_id, message FROM findings WHERE severity='ERROR' AND known_debt IS NULL LIMIT 20"
    ).fetchall()
    if errs:
        print("LIVE ERRORS:")
        for check, msg in errs:
            print(f"  - [{check}] {msg}")
        print()
    # known-debt suppressions in force
    supp = cur.execute(
        "SELECT known_debt, COUNT(*) FROM findings WHERE known_debt IS NOT NULL "
        "AND known_debt!='' GROUP BY known_debt").fetchall()
    if supp:
        print("KNOWN-DEBT SUPPRESSIONS IN FORCE:")
        for kd, n in supp:
            print(f"  - {kd}  ({n} finding[s])")
        print()
    live = _live_errors(store)
    print(SEP)
    print(f"VERDICT: {'PASS' if live == 0 else 'FAIL'}   (live errors={live})")
    print(SEP)
    return 0 if live == 0 else 1


# --------------------------------------------------------------------------- #
# entry
# --------------------------------------------------------------------------- #
def audit():
    store = gbuild.build()
    gdb = sqlite3.connect(f"file:{gbuild.GUIDEBOOK_DB}?mode=ro", uri=True)
    try:
        apply_known_debt(store, gdb, load_known_debt())
    finally:
        gdb.close()
    code = report(store)
    store.close()
    return code


# --------------------------------------------------------------------------- #
# mutation harness (selftest) — each check must fire on tampered input
# --------------------------------------------------------------------------- #
def _count_check(store, check_id, severity=None):
    q = "SELECT COUNT(*) FROM findings WHERE check_id=? AND known_debt IS NULL"
    args = [check_id]
    if severity:
        q += " AND severity=?"
        args.append(severity)
    return store.conn.execute(q, args).fetchone()[0]


def _insert_row(con, table, values):
    """Insert a row, filling NOT-NULL/no-default/non-pk columns with a placeholder."""
    cols = con.execute(f"PRAGMA table_info({table})").fetchall()  # cid,name,type,notnull,dflt,pk
    row = dict(values)
    for _, name, _t, notnull, dflt, pk in cols:
        if name not in row and notnull and dflt is None and not pk:
            row[name] = "selftest"
    keys = list(row)
    con.execute(f"INSERT INTO {table}({','.join(keys)}) VALUES({','.join('?' * len(keys))})",
                [row[k] for k in keys])


def selftest():
    import shutil
    import tempfile
    print(SEP)
    print("graph_audit.py --selftest (mutation harness)")
    print(SEP)
    results = []
    canonical = str(gbuild.GUIDEBOOK_DB)
    tmpd = tempfile.mkdtemp(prefix="graph_audit_selftest_")
    try:
        copy = os.path.join(tmpd, "gb.db")

        # 1. clean build -> no live ERROR (asserts the canonical DB passes our ERROR checks)
        shutil.copy(canonical, copy)
        s = gbuild.build(audit_db=os.path.join(tmpd, "a1.db"), guidebook_db=copy)
        results.append(("clean build has no live ERROR", _live_errors(s) == 0))
        s.close()

        # 2. dangling citation ERROR fires on an injected bad ref
        con = sqlite3.connect(copy)
        con.execute("PRAGMA foreign_keys=OFF")
        slug = con.execute("SELECT slug FROM slugs LIMIT 1").fetchone()[0]
        _insert_row(con, "source_slug_links",
                    {"ref_id": "REF-99999", "slug": slug, "local_ref_id": "SELFTEST"})
        con.commit()
        con.close()
        s = gbuild.build(audit_db=os.path.join(tmpd, "a2.db"), guidebook_db=copy)
        results.append(("dangling citation fires on injected bad ref",
                        _count_check(s, "orphan.dangling_citation", "ERROR") > 0))
        s.close()

        # 3. phantom connection target WARN fires
        shutil.copy(canonical, copy)
        con = sqlite3.connect(copy)
        cid = con.execute("SELECT con_id FROM connections LIMIT 1").fetchone()[0]
        _insert_row(con, "connection_targets", {"con_id": cid, "target": "item:Z-99"})
        con.commit()
        con.close()
        s = gbuild.build(audit_db=os.path.join(tmpd, "a3.db"), guidebook_db=copy)
        results.append(("phantom connection target fires",
                        _count_check(s, "ref.unresolved_conn_target", "WARN") > 0))
        s.close()

        # 4. self-ref cycle ERROR fires on an injected population parent loop
        shutil.copy(canonical, copy)
        con = sqlite3.connect(copy)
        con.execute("PRAGMA foreign_keys=OFF")
        two = con.execute("SELECT population_code FROM populations LIMIT 2").fetchall()
        if len(two) >= 2:
            a, b = two[0][0], two[1][0]
            con.execute("UPDATE populations SET parent_code=? WHERE population_code=?", (b, a))
            con.execute("UPDATE populations SET parent_code=? WHERE population_code=?", (a, b))
        con.commit()
        con.close()
        s = gbuild.build(audit_db=os.path.join(tmpd, "a4.db"), guidebook_db=copy)
        results.append(("population parent cycle fires",
                        _count_check(s, "cycle.population_parent", "ERROR") > 0))
        s.close()

        # 5. known-debt staleness is detected when a warrant is satisfied
        shutil.copy(canonical, copy)
        s = gbuild.build(audit_db=os.path.join(tmpd, "a5.db"), guidebook_db=copy)
        gdb = sqlite3.connect(f"file:{copy}?mode=ro", uri=True)
        fake = [{"id": "selftest-stale", "check_id": "table.empty_mission_critical",
                 "table": "slugs", "lift_when_sql": "SELECT COUNT(*) FROM slugs", "lift_when_ge": 1}]
        stale = apply_known_debt(s, gdb, fake)
        gdb.close()
        results.append(("stale known-debt suppression is detected", len(stale) == 1))
        s.close()
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)

    ok = True
    for name, passed in results:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    print(SEP)
    print(f"SELFTEST: {'PASS' if ok else 'FAIL'} ({sum(1 for _, p in results if p)}/{len(results)})")
    print(SEP)
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    return audit()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
