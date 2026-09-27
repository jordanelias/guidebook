#!/usr/bin/env python3
"""scripts/audit/provenance_artefact_audit.py — a candidate checked against the bytes
its search actually returned (RC1, DR-2026-09-26-recurring-defect-shapes-remediation.md
section 2). Two registrations, one script -- the precedent is `citation_mining_session`
and `citation_mining_backlog_t2`, one script under two check-registry entries.

  --mode surfaced      Every candidate carrying `surfaced_in`. Re-derives section 2.2(d)'s
                        refusal from bytes, via `retrieval_log.check_surfaced_in` -- the
                        SAME function `db.py`'s add-candidate/reattribute-candidate call at
                        write time (rule 5: one evaluation, not two that can drift apart).
                        FAILS any row the writer would refuse today: a row that reached the
                        DB without the writer (hand SQL inside a data migration), or a
                        payload changed or removed after the write. BLOCKING.

  --mode attribution    Every candidate WITHOUT `surfaced_in` whose search has at least one
                        linked payload (a `search_execution_artefacts` row for its exec_id).
                        FAILS when the candidate's single locator DOI occurs in none of
                        them. Reports two non-failing cases: UNLINKED (the search has no
                        linked payload) and NO-IDENTIFIER (the candidate has no DOI to
                        check). ADVISORY -- its history links are derived by the section
                        2.1 rule, which errs toward not linking, so anything it finds in
                        history is a finding for a batch, not a defect in the PR that lands
                        it.

EXAMINED is the mode's own subject count (CLAUDE.md 5(a)): a check that reports nothing
found without saying how much it looked at is indistinguishable from one that looked at
nothing. Both modes are non-vacuous once any candidate carries `surfaced_in` or belongs to
a search with linked artefacts; a fresh clone with neither is NOTHING-IN-SCOPE.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import dbcore                                                        # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research"))
import retrieval_log                                                 # noqa: E402

DB_PATH = dbcore.db_path()


def _connect():
    import sqlite3
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _mode_surfaced(conn) -> int:
    rows = conn.execute(
        "SELECT candidate_id, exec_id, locator, surfaced_in, surfaced_quote "
        "FROM search_candidates WHERE surfaced_in IS NOT NULL "
        "ORDER BY candidate_id").fetchall()
    print(f"EXAMINED: {len(rows)} candidate(s) carrying surfaced_in")
    if not rows:
        print("VERDICT: PASS — NOTHING-IN-SCOPE (no candidate carries surfaced_in yet).")
        return 0
    failures, routes = [], {}
    for r in rows:
        try:
            route = retrieval_log.check_surfaced_in(
                r["exec_id"], r["surfaced_in"], r["surfaced_quote"], r["locator"],
                conn=conn)
            routes[route] = routes.get(route, 0) + 1
        except ValueError as e:
            failures.append(f"candidate {r['candidate_id']}: {e}")
    if routes:
        print("Routes: " + ", ".join(f"{k}={v}" for k, v in sorted(routes.items())))
    if failures:
        print(f"FAIL: {len(failures)} candidate(s) fail re-derivation from bytes:")
        for f in failures:
            print(f"  {f}")
        return 1
    print(f"VERDICT: PASS — {len(rows)} candidate(s) re-derive from bytes.")
    return 0


def _mode_attribution(conn) -> int:
    rows = conn.execute(
        "SELECT candidate_id, exec_id, locator FROM search_candidates "
        "WHERE surfaced_in IS NULL AND exec_id IS NOT NULL "
        "ORDER BY candidate_id").fetchall()
    print(f"EXAMINED: {len(rows)} candidate(s) without surfaced_in")
    if not rows:
        print("VERDICT: PASS — NOTHING-IN-SCOPE (every candidate already carries surfaced_in, "
              "or none has an exec_id).")
        return 0
    failures, unlinked, no_identifier, matched = [], [], [], 0
    for r in rows:
        artefacts = [a for (a,) in conn.execute(
            "SELECT artefact FROM search_execution_artefacts WHERE exec_id=?",
            [r["exec_id"]]).fetchall()]
        if not artefacts:
            unlinked.append(r["candidate_id"])
            continue
        identifier = dbcore.single_doi_in(r["locator"])
        if not identifier:
            no_identifier.append(r["candidate_id"])
            continue
        needle = retrieval_log.normalise_quote(identifier)
        hit = False
        for artefact in artefacts:
            try:
                raw = retrieval_log.read_artefact_bytes(artefact)
            except ValueError:
                continue
            text, _enc = retrieval_log.decode_artefact(raw)
            if text is not None and needle in retrieval_log.normalise_quote(text):
                hit = True
                break
        if hit:
            matched += 1
        else:
            failures.append(
                f"candidate {r['candidate_id']}: DOI {identifier!r} occurs in none of "
                f"exec {r['exec_id']}'s {len(artefacts)} linked artefact(s).")
    print(f"Matched: {matched}, UNLINKED: {len(unlinked)}, NO-IDENTIFIER: {len(no_identifier)}")
    if unlinked:
        print(f"  UNLINKED (search has no linked payload): {unlinked}")
    if no_identifier:
        print(f"  NO-IDENTIFIER (candidate has no locator DOI): {no_identifier}")
    if failures:
        print(f"FAIL: {len(failures)} candidate(s) whose DOI occurs in none of their "
              f"search's linked payloads:")
        for f in failures:
            print(f"  {f}")
        return 1
    print(f"VERDICT: PASS — {matched} candidate(s) attributable, "
          f"{len(unlinked) + len(no_identifier)} reported without failing.")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", required=True, choices=["surfaced", "attribution"])
    args = p.parse_args()

    if not DB_PATH.exists():
        print(f"[ERROR] no database at {DB_PATH}.")
        print("EXAMINED: 0")
        return 2
    conn = _connect()
    try:
        if args.mode == "surfaced":
            return _mode_surfaced(conn)
        return _mode_attribution(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
