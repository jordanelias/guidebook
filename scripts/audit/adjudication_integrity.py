#!/usr/bin/env python3
"""
adjudication_integrity.py — audit the evidence-adjudication substrate.

Adds the one mechanical adjudication check that is specified-but-unbuilt — the
Stage-2.5 tier-derivation consistency sweep that schemas/tier_derivation.py's own
docstring names ("rows for which check_tier_consistency returns False ... are
exactly the Stage 2.5 tier-consistency sweep targets") but which nothing runs
across the whole corpus — and prints an honest readiness report for the
determination field.

It deliberately does NOT duplicate its siblings, which own the other
evidence-architecture §10 checks and remain authoritative:
  - matrix_consistency.py         §10.1  grain × scale directness matrix vs §3
  - validate_evidence_state.py    §10.4  per-cell state machine (governing_refs
                                  non-empty; code_floor_only / regulatory_stratum_only
                                  never `stated`; Tier-3-alone threshold)
  - register_integrity_check.py   §10.3  render invariants I1–I5

Check (the additive one):
  1. tier_derivation_consistency — every evidence_source's stored `tier` equals
     derive_tier(evidence_type, scope); an underivable (type, scope) pair is a
     violation too. This guards against hand-set tiers that break the ratified
     (type × scope) → tier ladder. Exit 1 on any violation.

Readiness (INFO — honest coverage, not a green light): the determination field is
largely unbuilt pre-C1 (evidence_cell_state is pilot-only; source_value_extractions
is empty), so value-level convergence and most per-cell invariants cannot yet bite.
This reports exactly what is and is not assessable today rather than implying full
coverage.

Read-only; flags-only. Ships its --selftest mutation harness.

Usage:
    python3 scripts/audit/adjudication_integrity.py
    python3 scripts/audit/adjudication_integrity.py --selftest
    GUIDEBOOK_DB_PATH=/path/to/db python3 scripts/audit/adjudication_integrity.py
"""
import os
import sqlite3
import sys
from pathlib import Path

REPO = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, str(REPO))

from schemas.tier_derivation import derive_tier, TierDerivationError  # noqa: E402

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", str(REPO / "data" / "guidebook.db")))
SEP = "=" * 70


def tier_violations(rows):
    """rows: iterable of (ref_id, evidence_type, scope, tier).
    Return [(ref_id, evidence_type, scope, stored_tier, reason), ...]. Pure/testable."""
    out = []
    for ref_id, et, scope, tier in rows:
        if tier is None or et is None:
            continue  # nothing to check (tier not yet assigned)
        try:
            derived = derive_tier(et, scope)
        except TierDerivationError as e:
            out.append((ref_id, et, scope, tier, f"underivable: {e}"))
            continue
        if derived != tier:
            out.append((ref_id, et, scope, tier,
                        f"stored tier {tier} != derived tier {derived}"))
    return out


def _col_exists(cur, table, col):
    return col in {r[1] for r in cur.execute(f"PRAGMA table_info({table})")}


def _readiness(cur):
    lines = []
    n_cells = cur.execute("SELECT COUNT(*) FROM evidence_cell_state").fetchone()[0]
    lines.append(f"evidence_cell_state: {n_cells} determination cell(s)")
    if n_cells:
        dist = {str(s): n for s, n in cur.execute(
            "SELECT state, COUNT(*) FROM evidence_cell_state GROUP BY state ORDER BY state")}
        lines.append(f"    state distribution: {dist}")
        if _col_exists(cur, "evidence_cell_state", "regulatory_stratum_only"):
            rso = cur.execute("SELECT COUNT(*) FROM evidence_cell_state "
                              "WHERE regulatory_stratum_only=1").fetchone()[0]
            cfo = cur.execute("SELECT COUNT(*) FROM evidence_cell_state "
                              "WHERE code_floor_only=1").fetchone()[0]
            lines.append(f"    excluded from best-practice: regulatory_stratum_only={rso}, "
                         f"code_floor_only={cfo}")
    sve = cur.execute("SELECT COUNT(*) FROM source_value_extractions").fetchone()[0]
    lines.append(f"source_value_extractions: {sve} row(s) — "
                 f"{'value-directness assessable' if sve else 'EMPTY: value-level convergence not yet assessable (pre-C1)'}")
    conv = {str(s): n for s, n in cur.execute(
        "SELECT status, COUNT(*) FROM convergence_assessment GROUP BY status ORDER BY status")}
    lines.append(f"convergence_assessment: {conv or '{}'}")
    return lines


def audit():
    if not DB_PATH.exists():
        print(f"ERROR: DB not found at {DB_PATH}", file=sys.stderr)
        return 1
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    cur = conn.cursor()
    print(SEP)
    print("adjudication_integrity.py — evidence-adjudication substrate")
    print(SEP)

    rows = cur.execute(
        "SELECT ref_id, evidence_type, scope, tier FROM evidence_sources ORDER BY ref_id"
    ).fetchall()
    viol = tier_violations(rows)
    checked = sum(1 for _, et, _, t in rows if et is not None and t is not None)
    if viol:
        print(f"[1] FAIL: {len(viol)} tier-derivation inconsistency(ies) of {checked} checked:")
        for ref_id, et, scope, tier, reason in viol[:20]:
            print(f"    {ref_id}: ({et}, {scope}) stored tier {tier} — {reason}")
        if len(viol) > 20:
            print(f"    ... ({len(viol) - 20} more)")
    else:
        print(f"[1] PASS: all {checked} evidence_sources are tier-consistent "
              f"(stored tier == derive_tier(evidence_type, scope)).")

    print("\n[readiness] determination-field coverage (honest; not a pass/fail):")
    for line in _readiness(cur):
        print(f"    {line}")
    print("\n[siblings] authoritative §10 enforcers (not re-run here):")
    print("    matrix_consistency.py (grain×scale matrix) · validate_evidence_state.py "
          "(per-cell state machine) · register_integrity_check.py (render I1–I5)")

    conn.close()
    print()
    print(SEP)
    print(f"VERDICT: {'PASS' if not viol else 'FAIL'}   (tier inconsistencies={len(viol)})")
    print(SEP)
    return 0 if not viol else 1


# --------------------------------------------------------------------------- #
# mutation harness
# --------------------------------------------------------------------------- #
def selftest():
    print(SEP)
    print("adjudication_integrity.py --selftest (mutation harness)")
    print(SEP)
    results = []

    # a consistent row is not flagged; an inconsistent tier IS; an underivable pair IS.
    good = ("REF-A", "clinical", "high_control", 1)          # derives to 1
    bad_tier = ("REF-B", "clinical", "high_control", 5)       # derives to 1, stored 5
    underivable = ("REF-C", "clinical", "intrinsic", 3)       # clinical has no 'intrinsic' scope
    v = tier_violations([good, bad_tier, underivable])
    flagged = {r[0] for r in v}
    results.append(("consistent row not flagged", "REF-A" not in flagged))
    results.append(("inconsistent stored tier flagged", "REF-B" in flagged))
    results.append(("underivable (type, scope) flagged", "REF-C" in flagged))
    results.append(("null tier / null type are skipped, not flagged",
                    tier_violations([("REF-D", "clinical", "high_control", None),
                                     ("REF-E", None, "intrinsic", 2)]) == []))

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
