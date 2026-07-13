#!/usr/bin/env python3
"""
jurisdictional_divergence.py — surface value divergence across jurisdictions.

The vectorized-audit-tool's Tier-4 "value matrix", right-sized to the data that
actually exists. It reads the (item_code x jurisdiction -> value) matrix from
`jurisdictional_values` and surfaces, per item, where jurisdictions state
DIFFERENT numeric values for the same parameter. This automates
`references/item-jurisdiction-divergence-matrix.md` (hand-authored today) and is
NOT covered by the `v_divergence` view (which is determination-level over
`evidence_cell_state`, and currently empty).

Doctrine framing (read-only, flags-only — proposes nothing):
  - Cross-jurisdiction divergence is EXPECTED, not a defect: different jurisdictions
    legitimately adopt different code minima. The value is surfacing WHERE a
    best-practice determination is needed to adjudicate, and WHERE agreement across
    jurisdictions is being mistaken for evidence.
  - Cross-jurisdiction CONVERGENCE is flagged as "convergence-not-evidence"
    (tier-system.md §3): many jurisdictions agreeing on a value does not make it
    best practice — they may all copy one unevidenced ancestor.
  - WITHIN-jurisdiction divergence (two standards in the SAME jurisdiction giving
    different values for the same item+unit) is the stronger signal — closer to a
    genuine contradiction than legitimate cross-jurisdiction variation.

Only values sharing the SAME unit are ever compared (never 43 °C vs 900 mm).

Checks:
  1. within_jurisdiction_divergence   (WARN) same item+unit+jurisdiction, >1 value
  2. cross_jurisdiction_divergence    (INFO) same item+unit, values differ across jurisdictions
  3. convergence_not_evidence         (INFO) same item+unit, >=3 jurisdictions agree — not best practice
  4. unadjudicated_divergence         (WARN) a divergent item with no evidence_cell_state determination

This is a DESCRIPTIVE / surfacing tool: everything it finds is a CANDIDATE for
human adjudication (a within-jurisdiction divergence may be a genuine contradiction,
a standard superseded by a newer edition, or a legitimate scope distinction —
residential vs public), so it exits 0 and never hard-fails; it flags, it does not
rule. Ships its `--selftest` mutation harness.

Usage:
    python3 scripts/audit/jurisdictional_divergence.py
    python3 scripts/audit/jurisdictional_divergence.py --selftest
    GUIDEBOOK_DB_PATH=/path/to/db python3 scripts/audit/jurisdictional_divergence.py
"""
import os
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

DB_PATH = Path(os.environ.get(
    "GUIDEBOOK_DB_PATH",
    str(Path(__file__).resolve().parents[2] / "data" / "guidebook.db"),
))
SEP = "=" * 70
REL_TOL = 1e-9  # values within this relative tolerance are "equal"


def _rows(conn):
    return conn.execute(
        "SELECT item_code, jurisdiction, unit, value_numeric, is_code_minimum, "
        "       COALESCE(standard_name,'') AS standard_name, evidence_tier "
        "FROM jurisdictional_values "
        "WHERE value_numeric IS NOT NULL AND unit IS NOT NULL AND jurisdiction IS NOT NULL "
        "ORDER BY item_code, unit, jurisdiction"
    ).fetchall()


def _equalish(a, b):
    hi = max(abs(a), abs(b), 1e-12)
    return abs(a - b) / hi <= REL_TOL


def analyze(conn):
    """Return findings as a list of (check_id, severity, message). Pure over the DB."""
    rows = _rows(conn)
    # group by (item, unit)
    groups = defaultdict(list)
    for item, jur, unit, val, cm, std, tier in rows:
        groups[(item, unit)].append((jur, float(val), cm, std, tier))

    # items that have any best-practice determination (adjudicator present)
    adjudicated = {r[0] for r in conn.execute(
        "SELECT DISTINCT item_code FROM evidence_cell_state "
        "WHERE state IN ('stated','provisional')").fetchall()}

    findings = []
    for (item, unit), vals in sorted(groups.items()):
        by_jur = defaultdict(list)
        for jur, val, cm, std, tier in vals:
            by_jur[jur].append((val, std))
        distinct_vals = sorted({v for _, v, *_ in vals})

        # (1) within-jurisdiction divergence — the strongest signal
        for jur, jvals in sorted(by_jur.items()):
            uniq = sorted({v for v, _ in jvals})
            if len(uniq) > 1:
                detail = "; ".join(f"{v}{unit} ({s or '?'})" for v, s in sorted(jvals))
                findings.append((
                    "within_jurisdiction_divergence", "WARN",
                    f"{item} in {jur}: {len(uniq)} differing values for the same unit "
                    f"({unit}) — candidate contradiction; verify supersession vs scope: {detail}",
                ))

        if len(by_jur) < 2:
            continue  # single jurisdiction — nothing cross-jurisdiction to say

        # cross-jurisdiction: convergent or divergent?
        vmin, vmax = min(distinct_vals), max(distinct_vals)
        convergent = len(distinct_vals) == 1 or _equalish(vmin, vmax)
        if convergent:
            # (3) convergence-not-evidence (only meaningful with several jurisdictions)
            if len(by_jur) >= 3:
                findings.append((
                    "convergence_not_evidence", "INFO",
                    f"{item}: {len(by_jur)} jurisdictions converge on {vmin}{unit} — "
                    f"convergence is NOT best-practice evidence (tier-system §3).",
                ))
            continue

        # (2) cross-jurisdiction divergence
        spread = vmax - vmin
        rel = spread / vmax if vmax else 0.0
        extremes = []
        for jur, jvals in by_jur.items():
            for v, _ in jvals:
                if _equalish(v, vmin) or _equalish(v, vmax):
                    extremes.append(f"{jur}={v}{unit}")
        findings.append((
            "cross_jurisdiction_divergence", "INFO",
            f"{item}: values span {vmin}-{vmax}{unit} across {len(by_jur)} jurisdictions "
            f"(spread {spread:g}{unit}, {rel*100:.0f}%); {', '.join(sorted(set(extremes)))}.",
        ))
        # (4) divergence with no best-practice determination to adjudicate it
        if item not in adjudicated:
            findings.append((
                "unadjudicated_divergence", "WARN",
                f"{item}: jurisdictions diverge on {unit} but no evidence_cell_state "
                f"best-practice determination exists to adjudicate (judgment stage unbuilt).",
            ))
    return findings


def audit():
    if not DB_PATH.exists():
        print(f"ERROR: DB not found at {DB_PATH}", file=sys.stderr)
        return 1
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        findings = analyze(conn)
    finally:
        conn.close()

    print(SEP)
    print("jurisdictional_divergence.py — value matrix over jurisdictional_values")
    print(SEP)
    order = ["within_jurisdiction_divergence", "cross_jurisdiction_divergence",
             "unadjudicated_divergence", "convergence_not_evidence"]
    by_check = defaultdict(list)
    for check, sev, msg in findings:
        by_check[check].append((sev, msg))
    for check in order:
        items = by_check.get(check, [])
        sev = "WARN" if check in ("within_jurisdiction_divergence", "unadjudicated_divergence") else "INFO"
        print(f"\n[{check}] {len(items)} ({sev})")
        for _, msg in items[:40]:
            print(f"    {msg}")
        if len(items) > 40:
            print(f"    ... ({len(items) - 40} more)")

    within = len(by_check.get("within_jurisdiction_divergence", []))
    cross = len(by_check.get("cross_jurisdiction_divergence", []))
    unadj = len(by_check.get("unadjudicated_divergence", []))
    print()
    print(SEP)
    print(f"SURFACED: {within} within-jurisdiction candidate contradiction(s), "
          f"{cross} cross-jurisdiction divergence(s), {unadj} unadjudicated "
          f"(all advisory — flags for human adjudication, not defects).")
    print(SEP)
    return 0  # descriptive tool: always exits 0; it flags, it does not rule


# --------------------------------------------------------------------------- #
# mutation harness
# --------------------------------------------------------------------------- #
def _mem_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("""CREATE TABLE jurisdictional_values (
        item_code TEXT, jurisdiction TEXT, unit TEXT, value_numeric REAL,
        is_code_minimum INTEGER, standard_name TEXT, evidence_tier INTEGER)""")
    conn.execute("CREATE TABLE evidence_cell_state (item_code TEXT, state TEXT)")
    return conn


def _ins(conn, item, jur, unit, val, std="S"):
    conn.execute("INSERT INTO jurisdictional_values(item_code,jurisdiction,unit,"
                 "value_numeric,is_code_minimum,standard_name,evidence_tier) "
                 "VALUES(?,?,?,?,1,?,6)", (item, jur, unit, val, std))


def selftest():
    print(SEP)
    print("jurisdictional_divergence.py --selftest (mutation harness)")
    print(SEP)
    results = []

    # cross-jurisdiction divergence is detected
    c = _mem_db()
    _ins(c, "X-01", "US", "mm", 10); _ins(c, "X-01", "UK", "mm", 20)
    ids = {f[0] for f in analyze(c)}
    results.append(("cross-jurisdiction divergence detected", "cross_jurisdiction_divergence" in ids))

    # convergence is NOT reported as divergence, and >=3 agree -> convergence-not-evidence
    c = _mem_db()
    for j in ("US", "UK", "DE"):
        _ins(c, "Y-01", j, "mm", 5)
    ids = {f[0] for f in analyze(c)}
    results.append(("convergent values are not flagged divergent",
                    "cross_jurisdiction_divergence" not in ids and "convergence_not_evidence" in ids))

    # unit mismatch is NEVER compared (no false divergence)
    c = _mem_db()
    _ins(c, "Z-01", "DE", "C", 43); _ins(c, "Z-01", "US", "mm", 900)
    ids = {f[0] for f in analyze(c)}
    results.append(("different units are never compared",
                    "cross_jurisdiction_divergence" not in ids and "within_jurisdiction_divergence" not in ids))

    # within-jurisdiction divergence (two standards, one jurisdiction) is detected
    c = _mem_db()
    _ins(c, "W-01", "US", "mm", 10, "StdA"); _ins(c, "W-01", "US", "mm", 15, "StdB")
    ids = {f[0] for f in analyze(c)}
    results.append(("within-jurisdiction divergence detected",
                    "within_jurisdiction_divergence" in ids))

    # unadjudicated flag lifts when a best-practice cell exists
    c = _mem_db()
    _ins(c, "V-01", "US", "mm", 10); _ins(c, "V-01", "UK", "mm", 20)
    c.execute("INSERT INTO evidence_cell_state VALUES('V-01','stated')")
    ids = {f[0] for f in analyze(c)}
    results.append(("adjudicated divergence is not flagged unadjudicated",
                    "cross_jurisdiction_divergence" in ids and "unadjudicated_divergence" not in ids))

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
