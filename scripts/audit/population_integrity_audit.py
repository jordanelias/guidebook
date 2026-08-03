#!/usr/bin/env python3
"""
Audit query for value-claim population integrity (migration 021 +
owner directive 2026-05-28: populations must be canonical disability codes).

Checks:
1. Every population_code in each junction (citation/probe/extraction) exists
   in the canonical populations table. FK enforces this at write time; this
   check is belt-and-braces in case FK enforcement was off during a bulk
   load (migrations may toggle PRAGMA foreign_keys per architecture
   <data_layer_pattern>).
2. Scalar<->junction CONSISTENCY: for each value-claim row with a non-null
   scalar population (reasoning_doc_citations.population,
   spec_value_probes.population) or population_code
   (source_value_extractions), the set of comma-split scalar codes must
   equal the set of junction population_codes. The scalar columns are
   deprecated transition aliases; this guards against silent drift between
   the authoritative junction and the denormalized scalar.
3. MIGRATION COMPLETENESS: no value-claim row has a non-null scalar
   population but an empty junction (would mean the backfill missed it).
4. SCALAR CANONICALITY: every comma-split code in a scalar population field
   is itself a canonical code (catches a bad scalar write that has no
   junction counterpart yet).
5. Distribution summary (informational): population usage across junctions.

Level 2 enforcement (audit, not hook). The population FK is already enforced
in CI via db_integrity's PRAGMA foreign_key_check; this script adds the
scalar-consistency and completeness checks that the FK cannot express.
Run before each session close; promotable to CI Level 4 if drift recurs.

DB path defaults to data/guidebook.db relative to repo root, overridable
via GUIDEBOOK_DB_PATH.
"""
import os
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DB = Path(os.environ.get("GUIDEBOOK_DB_PATH", str(REPO / "data" / "guidebook.db")))

# (junction table, parent table, parent PK col, scalar col on parent)
JUNCTIONS = [
    ("citation_population_links", "reasoning_doc_citations", "citation_id", "population"),
    ("probe_population_links", "spec_value_probes", "probe_id", "population"),
    ("extraction_population_links", "source_value_extractions", "extraction_id", "population_code"),
]


def _scalar_codes(value):
    """Comma-split a scalar population value into a set of trimmed codes."""
    if not value:
        return set()
    return {x.strip() for x in str(value).split(",") if x.strip()}


def audit():
    db = sqlite3.connect(str(DB))
    db.row_factory = sqlite3.Row
    issues = 0

    print("=" * 64)
    print("VALUE-CLAIM POPULATION INTEGRITY AUDIT (migration 021)")
    print("=" * 64)

    # Confirm tables exist
    have = {
        r["name"]
        for r in db.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    missing = [j[0] for j in JUNCTIONS if j[0] not in have]
    if missing:
        print(f"Junction tables missing: {missing}. Run migration 021 first.")
        return 1

    canon = {r["population_code"] for r in db.execute("SELECT population_code FROM populations")}
    print(f"\nCanonical population codes: {len(canon)}")

    # CHECK 1: junction codes canonical
    print("\n[CHECK 1] Junction population_code validity (FK belt-and-braces)")
    for jt, _, _, _ in JUNCTIONS:
        bad = [
            r["population_code"]
            for r in db.execute(f"SELECT DISTINCT population_code FROM {jt}")
            if r["population_code"] not in canon
        ]
        if bad:
            issues += len(bad)
            print(f"  ✗ {jt}: non-canonical codes {bad}")
        else:
            n = db.execute(f"SELECT COUNT(*) c FROM {jt}").fetchone()["c"]
            print(f"  ✓ {jt}: {n} rows, all codes canonical")

    # CHECK 2 + 3: scalar<->junction consistency and completeness
    print("\n[CHECK 2/3] Scalar<->junction consistency + migration completeness")
    for jt, parent, pk, scalar in JUNCTIONS:
        rows = db.execute(
            f"SELECT {pk} AS pid, {scalar} AS sc FROM {parent} WHERE {scalar} IS NOT NULL AND {scalar} != ''"
        ).fetchall()
        local_issue = 0
        for r in rows:
            scalar_set = _scalar_codes(r["sc"])
            junc_set = {
                x["population_code"]
                for x in db.execute(
                    f"SELECT population_code FROM {jt} WHERE {pk}=?", (r["pid"],)
                )
            }
            if not junc_set:
                issues += 1
                local_issue += 1
                print(f"  ✗ {parent}.{pk}={r['pid']}: scalar={scalar_set} but EMPTY junction (backfill missed)")
            elif scalar_set != junc_set:
                issues += 1
                local_issue += 1
                print(f"  ✗ {parent}.{pk}={r['pid']}: scalar={scalar_set} != junction={junc_set}")
        if not local_issue:
            print(f"  ✓ {parent}: {len(rows)} scalar-bearing rows, all consistent with junction")

    # CHECK 4: scalar canonicality
    print("\n[CHECK 4] Scalar population code canonicality")
    for jt, parent, pk, scalar in JUNCTIONS:
        bad_rows = []
        for r in db.execute(
            f"SELECT {pk} AS pid, {scalar} AS sc FROM {parent} WHERE {scalar} IS NOT NULL AND {scalar} != ''"
        ):
            bad = [code for code in _scalar_codes(r["sc"]) if code not in canon]
            if bad:
                bad_rows.append((r["pid"], bad))
        if bad_rows:
            issues += len(bad_rows)
            for pid, bad in bad_rows:
                print(f"  ✗ {parent}.{pk}={pid}: scalar has non-canonical {bad}")
        else:
            print(f"  ✓ {parent}: all scalar codes canonical")

    # CHECK 5: distribution summary (informational)
    print("\n[CHECK 5] Population usage across junctions (informational)")
    for jt, _, _, _ in JUNCTIONS:
        dist = db.execute(
            f"SELECT population_code, COUNT(*) c FROM {jt} GROUP BY population_code ORDER BY c DESC"
        ).fetchall()
        summary = ", ".join(f"{r['population_code']}:{r['c']}" for r in dist) or "(empty)"
        print(f"  {jt}: {summary}")

    print()
    print("=" * 64)
    print(f"ISSUES: {issues}")
    print("=" * 64)
    db.close()
    return 0 if issues == 0 else 1


if __name__ == "__main__":
    sys.exit(audit())
