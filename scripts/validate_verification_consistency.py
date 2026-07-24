#!/usr/bin/env python3
"""validate_verification_consistency.py — the has_unverified_sources truthfulness gate.

Mechanizes a lesson from the 2026-07-24 Phase-B session: a determination cell can
claim its sources are content-verified (has_unverified_sources=0) while the cited
sources still sit at verification_status='UNVERIFIED-1' in evidence_sources — a
narrative/DB-state mismatch that no existing validator caught. (validate_evidence_state
only forces `pending` on UNVERIFIED-CLOSED/CLOSED-DELETED sole bases; it never
cross-checks the has_unverified_sources flag against the sources it names.)

Invariant (per schemas/evidence_state.py: "has_unverified_sources = Any UNVERIFIED-1
sources in basis"), for every `stated`/`provisional` cell:

  has_unverified_sources == 1  iff  any governing_ref has
      verification_status == 'UNVERIFIED-1'

Also flags governing_refs that do not resolve to an evidence_sources row (dangling).

Read-only. Exit 0 = consistent, 1 = violations. GUIDEBOOK_DB_PATH honored.
Standalone stdlib (no pydantic). Intended for scripts/preflight.sh and, once owner
approves, promotion into the audit.yml battery.
"""
import json
import os
import sqlite3
import sys

DB = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")


def _jlist(v):
    if not v:
        return []
    try:
        out = json.loads(v)
        return out if isinstance(out, list) else []
    except (ValueError, TypeError):
        return []


def _check(con) -> list:
    """Core invariant over an open connection. Returns list of violation strings."""
    c = con.cursor()
    status = {
        r[0]: r[1]
        for r in c.execute("SELECT ref_id, verification_status FROM evidence_sources")
    }
    rows = c.execute(
        "SELECT cell_id,item_code,population_code,state,governing_refs,"
        "has_unverified_sources FROM evidence_cell_state "
        "WHERE state IN ('stated','provisional')"
    ).fetchall()
    errors = []
    for cell_id, item, pop, state, gref, hus in rows:
        tag = f"cell {cell_id} ({item}×{pop}, {state})"
        refs = _jlist(gref)
        for r in [r for r in refs if r not in status]:
            errors.append(f"{tag}: governing_ref {r} not in evidence_sources (dangling)")
        actual_unverified = any(status.get(r) == "UNVERIFIED-1" for r in refs)
        flag = bool(hus)
        if actual_unverified and not flag:
            bad = [r for r in refs if status.get(r) == "UNVERIFIED-1"]
            errors.append(
                f"{tag}: has_unverified_sources=0 but cites UNVERIFIED-1 source(s) "
                f"{bad} — advance the source(s) or set the flag (Phase-B truthfulness)"
            )
        if flag and not actual_unverified:
            errors.append(
                f"{tag}: has_unverified_sources=1 but no governing_ref is UNVERIFIED-1 "
                f"— clear the flag (stale)"
            )
    return errors, len(rows)


def selftest() -> int:
    """Mutation harness (integrity-protocol_SKILL Mode 1 rule 3): prove the checker FIRES on
    tampered input, not merely that it passes on clean input."""
    con = sqlite3.connect(":memory:")
    con.executescript(
        "CREATE TABLE evidence_sources(ref_id TEXT, verification_status TEXT);"
        "CREATE TABLE evidence_cell_state(cell_id INT, item_code TEXT, population_code TEXT,"
        " state TEXT, governing_refs TEXT, has_unverified_sources INT);"
        "INSERT INTO evidence_sources VALUES('R1','VERIFIED'),('R2','UNVERIFIED-1');"
    )
    cases = [
        # (row, expect_violation, why)
        ((1, "A-01", "X", "provisional", '["R1"]', 0), False, "clean: verified ref, flag 0"),
        ((2, "A-02", "X", "provisional", '["R2"]', 0), True, "lies: cites UNVERIFIED-1 with flag 0"),
        ((3, "A-03", "X", "stated", '["R1"]', 1), True, "stale: flag 1 but no unverified ref"),
        ((4, "A-04", "X", "provisional", '["R2"]', 1), False, "honest: unverified ref, flag 1"),
        ((5, "A-05", "X", "provisional", '["R9"]', 0), True, "dangling: R9 not in sources"),
    ]
    ok = True
    for row, expect, why in cases:
        con.execute("DELETE FROM evidence_cell_state")
        con.execute("INSERT INTO evidence_cell_state VALUES(?,?,?,?,?,?)", row)
        errs, _ = _check(con)
        got = len(errs) > 0
        status = "OK" if got == expect else "**MISSED**"
        if got != expect:
            ok = False
        print(f"  [{status}] cell {row[0]}: {why} -> violation={got} (expected {expect})")
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    errors, n = _check(con)
    if errors:
        print(f"FAIL verification-consistency ({DB}):")
        for e in errors:
            print(f"  {e}")
        print(f"\nFAIL: {n} cells checked, {len(errors)} violations")
        return 1
    print(f"OK verification-consistency: {n} stated/provisional cells consistent ({DB})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
