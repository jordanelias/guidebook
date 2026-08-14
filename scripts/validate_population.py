#!/usr/bin/env python3
"""
scripts/validate_population.py — Validate population codes against the live taxonomy.

WHAT THIS WAS, AND WHY IT WAS REPLACED (2026-08-05)
---------------------------------------------------
This is a `blocking` check in governance/check-registry.yaml. Run before this
rewrite, it printed:

    No files with population codes found to validate.

and exited 0. It had never validated a single file, for two independent reasons,
either of which alone was fatal:

1. **Its subject did not exist.** It scanned `references/bpc/**/*.md` for a
   `population:` key in YAML front matter. *No BPC file has YAML front matter* —
   0 of 102 — so the extractor returned empty for every file and the scan fell
   through to the zero-subject branch. Population lives in `bpc_metadata`, in the
   file body, and in a dozen DB columns; it has never lived in front matter.
2. **Its rules were the superseded taxonomy.** DR-2026-07-23 (ADOPTED, DG-NON)
   retired the whole parent/slash code scheme and replaced it with a flat 23-code
   set. This script still enforced the old model: a `SUBCODE_PARENTS` map of
   `MOB/UPL`, `NEU/PCS`, `OFS/POTS` and friends — codes that no longer exist; a
   `SUPPLEMENTARY_CODES` set containing `EXH` (retired to `TALL`) while treating
   `LPA`/`BAR` as supplementary-only when both are now first-class populations;
   and an explicit rule that "IntD is not a standalone population code — proxy
   through DEM + NDV", which sub-decision 4 of that DR specifically overturned.
   Had the extractor ever found a file, the check would have rejected valid codes
   and accepted retired ones.

**A check that examines zero subjects now FAILS.** That is the general lesson,
and it is why the vacuity guard below is not optional politeness: a gate that
passes by having nothing in scope is indistinguishable, in CI, from a gate that
passed on the merits, and it is worse than no gate because it reads as assurance.

WHAT IT CHECKS NOW
------------------
P1  schemas/enums.py `PopulationCode` and the `populations` table agree, in both
    directions. CLAUDE.md §10: schema-mirror drift is a bug, not a convention.
P2  every population-bearing column in the database resolves to a live code.
    The column list is DISCOVERED, not transcribed — every column named exactly
    `population` or `population_code`, in every table but the two excluded below.
    New tables are covered the day they land; a hardcoded list would have to be
    remembered, and this file is a case study in what happens when it is not.
P3  no retired code appears in those columns, reported with the DR-2026-07-23
    crosswalk so the message says what to write instead.
P4  no code column holds a comma-joined list. That is the packed-CSV defect
    `items.applicable_groups` was dropped for, and it hides retired codes from a  # [RETIRED-VOCAB-OK]
    whole-string match. Each packed element is graded individually.
P5  no unregistered scope marker. `ALL` is a populations row doing exactly that
    job; anything else claiming it resolves nowhere.

Usage:
    python3 scripts/validate_population.py
    python3 scripts/validate_population.py --verbose

Exit codes: 0 = pass, 1 = errors found (including zero subjects)
"""

import argparse
import os
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from schemas.enums import PopulationCode          # noqa: E402

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO / "data" / "guidebook.db"))

# The crosswalk from DR-2026-07-23. Kept here so an error message can say what to
# write instead of merely that something is wrong: a validator reporting "unknown
# code: UPL" sends the reader off to find the DR; one reporting "UPL is retired
# -> LMB" does not.
RETIRED_CROSSWALK = {
    "VIS":  "BLIND",
    "UPL":  "LMB",
    "DBL":  "DEAFBLIND",
    "NEU":  "BRAIN",
    "PCS":  "BRAIN",
    "OFS":  "COM",
    "CFS":  "COM",
    "MCAS": "COM",
    "POTS": "COM",
    "LCOV": "COM",
    "SENS": "NDV",
    "EXH":  "TALL",
    "IntD": "ID",
    "ABI":  "BRAIN",
}

# Tables excluded from the scan, each for a reason that is about MEANING, not
# convenience. Both were found by running the first draft of this scan and reading
# what it flagged, rather than assumed in advance.
EXCLUDED_TABLES = {
    # The authority itself, not a subject.
    "populations",
    # The reclassification map. Its whole purpose is to hold the OLD codes
    # alongside their canonical replacements, so retired codes there are the
    # table working correctly. Flagging them would be flagging the crosswalk for
    # containing the crosswalk.
    "population_reclass",
}

# Column names that hold a code. Deliberately EXACT, not suffix-matched: the
# first draft matched `*_population` too, which swept in
# `evidence_population_match.study_population` and `.target_population`. Those are
# PROSE BY DESIGN — research-contract rule R13 requires grading the
# population-of-study against the population-served, and the graded values are
# sentences ("Women with rheumatoid arthritis (N=20)"). Sixty-odd of them were
# reported as invalid codes, which was the scan being wrong, not the data.
CODE_COLUMNS = {"population", "population_code"}


def discover_population_columns(conn):
    """Every (table, column) in the DB that should hold a population code."""
    out = []
    for (table,) in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ):
        if table in EXCLUDED_TABLES:
            continue
        for row in conn.execute(f'PRAGMA table_info("{table}")'):
            if row[1].lower() in CODE_COLUMNS:
                out.append((table, row[1]))
    return out


def validate(verbose=False):
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found.", file=sys.stderr)
        return 1

    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    errors, notes = [], []

    enum_codes = {m.value for m in PopulationCode}
    db_codes = {r[0] for r in conn.execute("SELECT population_code FROM populations")}

    # --- P1: enum <-> table parity, both directions -------------------------
    for c in sorted(enum_codes - db_codes):
        errors.append(f"P1: '{c}' is in schemas/enums.py PopulationCode but not in the populations table")
    for c in sorted(db_codes - enum_codes):
        errors.append(f"P1: '{c}' is in the populations table but not in schemas/enums.py PopulationCode")
    if enum_codes == db_codes:
        notes.append(f"P1 PASS: enum and populations table agree on {len(db_codes)} codes")

    # --- P2/P3: every population-bearing column resolves --------------------
    columns = discover_population_columns(conn)
    checked_rows = 0
    for table, col in columns:
        n = conn.execute(
            f'SELECT COUNT(*) FROM "{table}" WHERE "{col}" IS NOT NULL AND "{col}" != ""'
        ).fetchone()[0]
        checked_rows += n
        value_counts = dict(conn.execute(
            f'SELECT "{col}", COUNT(*) FROM "{table}" '
            f'WHERE "{col}" IS NOT NULL AND "{col}" != "" GROUP BY 1'
        ))
        values = list(value_counts)
        if verbose and n:
            print(f"  checking {table}.{col}: {n} row(s), {len(values)} distinct")
        for v in values:
            if v in db_codes:
                continue

            # A code column holding a comma-joined list is the packed-CSV defect
            # that items.applicable_groups was dropped for: one column, several  # [RETIRED-VOCAB-OK]
            # facts, no way to join on it. Report the packing AND grade each
            # element, because the elements are where the retired codes hide —
            # spec_value_probes carries "AUT, PCS, DEM, MH, PAIN, OFS", of which
            # two are retired and would be invisible to a whole-string match.
            parts = [p.strip() for p in v.split(",") if p.strip()]
            if len(parts) > 1:
                errors.append(
                    f"P4: {table}.{col} holds {v!r} — several codes packed into one "
                    f"column. A code column must hold one code; use a junction row "
                    f"per population (the defect items.applicable_groups was dropped for)."  # [RETIRED-VOCAB-OK]
                )
                for part in parts:
                    if part in RETIRED_CROSSWALK:
                        errors.append(
                            f"P3: {table}.{col} packs '{part}', retired by "
                            f"DR-2026-07-23 — write '{RETIRED_CROSSWALK[part]}'"
                        )
                    elif part not in db_codes:
                        errors.append(
                            f"P2: {table}.{col} packs '{part}', not a live population code"
                        )
                continue

            if v in RETIRED_CROSSWALK:
                errors.append(
                    f"P3: {table}.{col} holds '{v}', retired by DR-2026-07-23 "
                    f"— write '{RETIRED_CROSSWALK[v]}'"
                )
            elif v == "MULTI":
                errors.append(
                    f"P5: {table}.{col} holds 'MULTI' ({value_counts[v]} row(s)) — an unregistered "
                    f"scope marker. `ALL` is registered as a row in the populations "
                    f"table with exactly this job; `MULTI` is not, so it resolves "
                    f"nowhere. Either register it the same way, or resolve the rows "
                    f"to the populations they actually cover."
                )
            else:
                errors.append(
                    f"P2: {table}.{col} holds '{v}', which is not a live population code"
                )

    # --- vacuity guard ------------------------------------------------------
    # The reason this file exists in its current form. See the module docstring.
    if not columns:
        errors.append(
            "VACUOUS: no population-bearing column found in the database. This "
            "check examined nothing, so a green result would have meant nothing."
        )
    elif checked_rows == 0:
        errors.append(
            f"VACUOUS: found {len(columns)} population-bearing column(s), all "
            "empty. This check examined no values."
        )

    conn.close()

    if errors:
        print(f"population validation: {len(errors)} error(s)")
        for e in errors:
            print(f"  {e}")
        print(f"EXAMINED: {checked_rows}")
        return 1
    for note in notes:
        print(f"  {note}")
    print(f"population validation: PASS ({len(db_codes)} live codes; "
          f"{checked_rows} value(s) across {len(columns)} column(s) all resolve)")
    print(f"EXAMINED: {checked_rows}")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="Validate population codes against the live taxonomy")
    ap.add_argument("--verbose", action="store_true",
                    help="print each column as it is checked")
    return validate(verbose=ap.parse_args().verbose)


if __name__ == "__main__":
    sys.exit(main())
