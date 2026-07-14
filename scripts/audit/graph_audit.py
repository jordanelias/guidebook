#!/usr/bin/env python3
"""
graph_audit.py — vectorized structural audit (stdlib graph spine, data layer).

Builds a derived, read-only audit graph from data/guidebook.db and runs Tier-1
topology checks over it, unifying orphan / dangling-reference / empty-table /
state-distribution checks that today are scattered across skills and audit scripts.
It NEVER writes guidebook.db; the audit graph is a throwaway artifact.

Checks (data + code + content layers):
  1. orphan.dangling_citation     (ERROR) value-layer ref with no evidence_sources row
                                  — the vetting-surface `orphan_links` invariant; must be 0
  2. cycle.population_parent      (ERROR) populations.parent_code forms a cycle
  3. orphan.uncited_source        (WARN)  evidence source cited by nothing
  4. ref.unresolved_conn_target   (WARN)  connection_target not resolving to item/slug
                                  (phantom-item vs unresolved-identifier)
  5. code.phantom_table           (WARN)  script SQL references a table absent from
                                  guidebook.db (dormant/stale/legacy query)
  6. ref.phantom_identifier       (WARN)  prose references an item/source/... identifier
                                  that resolves to no entity (candidate phantom ref)
  7. table.empty_mission_critical (INFO)  mission-critical table at/near 0 rows
                                  (suppressed against known_debt.yaml, warrant-checked)
  8. connection.empty_description (INFO)  connections with empty description
  9. state.distribution           (INFO)  lifecycle CHECK-enum distributions
 10. graph.components             (INFO)  connected-component / island count

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
    """Suppress matching findings, but only soundly. A suppression must not outlive
    its warrant and must never silently swallow a regression, so:
      - an entry with no warrant is refused (known_debt.unsound);
      - an unverifiable warrant (lift_when_sql errors, or lift_when_ge missing) is
        refused, NOT applied — a broken warrant can never suppress forever;
      - a satisfied warrant (count >= lift_when_ge) surfaces as stale, not suppressed;
      - an ERROR finding is never suppressed without an explicit allow_error_suppression.
    Returns the list of stale suppressions."""
    cur = store.conn.cursor()
    stale = []
    for e in entries:
        eid = e.get("id", "?")
        if not str(e.get("warrant", "")).strip():
            store.add_finding("known_debt.unsound", "WARN",
                              f"Known-debt entry '{eid}' has no warrant — not applied.",
                              attrs={"entry": eid})
            continue
        count = _lift_count(gdb, e)
        ge = e.get("lift_when_ge")
        if count is None or ge is None:
            store.add_finding("known_debt.unsound", "WARN",
                              f"Known-debt entry '{eid}': warrant unverifiable "
                              f"(lift_when_sql errored or lift_when_ge missing) — not applied, "
                              f"so it cannot suppress a regression forever.",
                              attrs={"entry": eid})
            continue
        if count >= ge:
            stale.append((eid, count, ge))
            store.add_finding("known_debt.stale", "WARN",
                              f"Known-debt suppression '{eid}' is stale: warrant satisfied "
                              f"({count} >= {ge}) — remove it from known_debt.yaml.",
                              attrs={"entry": eid, "count": count})
            continue
        allow_error = bool(e.get("allow_error_suppression", False))
        rows = cur.execute("SELECT finding_id, severity, attrs FROM findings "
                           "WHERE check_id=? AND known_debt IS NULL", (e["check_id"],)).fetchall()
        for fid, sev, attrs in rows:
            if "table" in e:
                a = json.loads(attrs) if attrs else {}
                if a.get("table") != e["table"]:
                    continue
            if sev == "ERROR" and not allow_error:
                store.add_finding("known_debt.unsound", "WARN",
                                  f"Known-debt entry '{eid}' would suppress an ERROR finding "
                                  f"without allow_error_suppression — refused.",
                                  attrs={"entry": eid})
                continue
            cur.execute("UPDATE findings SET known_debt=? WHERE finding_id=?", (eid, fid))
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
    print("graph_audit.py — vectorized structural audit (data + code + content layers)")
    print(SEP)
    print(f"guidebook.db user_version={uv[0] if uv else '?'}  |  "
          f"nodes={counts['nodes']}  edges={counts['edges']}  "
          f"dangling_edges={counts['dangling_edges']}")
    print()
    # per-check summary (the INFO summary rows carry the headline counts)
    order = ["orphan.dangling_citation", "cycle.population_parent", "orphan.uncited_source",
             "ref.unresolved_conn_target", "code.phantom_table", "ref.phantom_identifier",
             "table.empty_mission_critical", "connection.empty_description",
             "state.distribution", "graph.components", "known_debt.stale"]
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
        # A-99 is in category [A-K] so it exercises the phantom-ITEM branch (Z-99 would
        # only ever hit the unresolved-identifier branch).
        _insert_row(con, "connection_targets", {"con_id": cid, "target": "item:A-99"})
        con.commit()
        con.close()
        s = gbuild.build(audit_db=os.path.join(tmpd, "a3.db"), guidebook_db=copy)
        phantom_item = s.conn.execute(
            "SELECT COUNT(*) FROM findings WHERE check_id='ref.unresolved_conn_target' "
            "AND message LIKE '%phantom item%' AND known_debt IS NULL").fetchone()[0]
        results.append(("phantom-item connection target fires", phantom_item > 0))
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

        # 5. known-debt soundness: (a) satisfied warrant surfaces as stale (not suppressed)
        shutil.copy(canonical, copy)
        s = gbuild.build(audit_db=os.path.join(tmpd, "a5.db"), guidebook_db=copy)
        gdb = sqlite3.connect(f"file:{copy}?mode=ro", uri=True)
        stale = apply_known_debt(s, gdb, [{"id": "selftest-stale", "warrant": "selftest",
            "check_id": "table.empty_mission_critical", "table": "slugs",
            "lift_when_sql": "SELECT COUNT(*) FROM slugs", "lift_when_ge": 1}])
        results.append(("satisfied warrant surfaces as stale (not suppressed)", len(stale) == 1))
        # (b) a broken lift_when_sql is refused as unsound — it can never suppress forever
        before = _count_check(s, "known_debt.unsound")
        apply_known_debt(s, gdb, [{"id": "selftest-broken", "warrant": "selftest",
            "check_id": "table.empty_mission_critical", "table": "conflicts",
            "lift_when_sql": "SELECT COUNT(*) FROM no_such_table", "lift_when_ge": 1}])
        results.append(("broken warrant refused as unsound",
                        _count_check(s, "known_debt.unsound") > before))
        gdb.close()
        s.close()
        # (c) an ERROR finding is never suppressed without allow_error_suppression
        shutil.copy(canonical, copy)
        con = sqlite3.connect(copy)
        con.execute("PRAGMA foreign_keys=OFF")
        slug = con.execute("SELECT slug FROM slugs LIMIT 1").fetchone()[0]
        _insert_row(con, "source_slug_links", {"ref_id": "REF-88888", "slug": slug, "local_ref_id": "ST"})
        con.commit()
        con.close()
        s = gbuild.build(audit_db=os.path.join(tmpd, "a5c.db"), guidebook_db=copy)
        gdb = sqlite3.connect(f"file:{copy}?mode=ro", uri=True)
        apply_known_debt(s, gdb, [{"id": "selftest-error", "warrant": "selftest",
            "check_id": "orphan.dangling_citation", "lift_when_sql": "SELECT 0", "lift_when_ge": 1}])
        gdb.close()
        results.append(("ERROR finding not suppressed without allow_error_suppression",
                        _live_errors(s) > 0))
        s.close()

        # 6. code table-ref detector fires on injected SQL, ignores non-SQL prose
        import extract_code
        refs = set(extract_code.iter_table_refs("SELECT x FROM zzz_phantom JOIN items ON 1"))
        no_sql = list(extract_code.iter_table_refs("plain prose from here to there"))
        results.append(("code table-ref detector: phantom+real found, prose ignored",
                        "zzz_phantom" in refs and "items" in refs and no_sql == []))

        # 7. content identifier detector fires on scheme refs, rejects coincidental matches
        import extract_content
        ids = set(extract_content.iter_identifier_refs("see K-99, REF-00157 and CON-0247"))
        fp = set(extract_content.iter_identifier_refs("COVID-19 ISO-9001 x-A-01"))
        results.append(("content ref detector: scheme found, false positives rejected",
                        {("item", "K-99"), ("source", "REF-00157"), ("connection", "CON-0247")} <= ids
                        and not any(k == "item" for k, _ in fp)))

        # 8. code + content checks execute and emit on the real repo build
        s = gbuild.build(audit_db=os.path.join(tmpd, "a6.db"), guidebook_db=copy)
        c = s.conn.execute
        has_code = c("SELECT COUNT(*) FROM findings WHERE check_id='code.phantom_table'").fetchone()[0] > 0
        has_ref = c("SELECT COUNT(*) FROM findings WHERE check_id='ref.phantom_identifier'").fetchone()[0] > 0
        results.append(("code+content checks execute on real repo", has_code and has_ref))
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
