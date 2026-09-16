#!/usr/bin/env python3
"""validate_icf_groupings.py — ICF-grouping-layer integrity + coverage (E6 of the 2026-07-21 ratification register).

The two-layer functional taxonomy (governance/functional-taxonomy.md) added an `base_icf_groupings` layer that
populations, access-needs, and (eventually) items map onto. Nothing validated that layer's
referential integrity or surfaced its coverage gaps. This does both:

INTEGRITY (ERROR, exit 1) — profile-layer containment:
  - every population_icf_grouping_map.grouping_code resolves to an base_icf_groupings row
  - every population_icf_grouping_map.population_code resolves to a populations row
  - every access_need_icf_grouping_map.grouping_code resolves to an base_icf_groupings row (when present)
  - population_icf_grouping_map.role ∈ {PRIMARY, SECONDARY, ALIAS, SITUATIONAL}

COVERAGE (WARN, non-fatal) — surfaced so the debt is visible, not hidden:
  - groupings with zero population mappings
  - groupings with zero item links (the E3 debt — items not yet linked to base_icf_groupings)
  - a per-grouping coverage summary

Read-only. Exit 0 = no integrity errors (coverage warnings do not fail). GUIDEBOOK_DB_PATH honored.
Standalone stdlib. `--selftest` runs a mutation harness (integrity-protocol Mode 1 rule 3).
"""
import os
import sqlite3
import sys

DB = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")
VALID_ROLES = {"PRIMARY", "SECONDARY", "ALIAS", "SITUATIONAL"}


def _has_table(c, t):
    return bool(
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (t,)).fetchone()
    )


def _check(con):
    """Returns (errors, warnings, summary_lines, n_examined).

    n_examined is the count of rows actually walked for referential integrity —
    every population_icf_grouping_map / item_taxonomy_links / access_need_icf_grouping_map row, not
    the grouping vocabulary size (which would be non-zero even if every mapping
    table were empty and nothing was actually checked).
    """
    c = con.cursor()
    errors, warnings, summary = [], [], []
    n_examined = 0
    grouping_codes = {r[0] for r in c.execute("SELECT grouping_code FROM base_icf_groupings")}
    pop_codes = {r[0] for r in c.execute("SELECT population_code FROM populations")}
    summary.append(f"ICF groupings defined: {len(grouping_codes)}")

    # --- INTEGRITY: population_icf_grouping_map ---
    covered_by_pop = set()
    if _has_table(c, "population_icf_grouping_map"):
        for pop, gc, role in c.execute(
            "SELECT population_code, grouping_code, role FROM population_icf_grouping_map"
        ):
            n_examined += 1
            if gc not in grouping_codes:
                errors.append(f"population_icf_grouping_map: grouping_code {gc!r} (pop {pop}) not in base_icf_groupings")
            else:
                covered_by_pop.add(gc)
            if pop not in pop_codes:
                errors.append(f"population_icf_grouping_map: population_code {pop!r} not in populations")
            if role is not None and role not in VALID_ROLES:
                errors.append(
                    f"population_icf_grouping_map: role {role!r} (pop {pop}, grouping {gc}) not in {sorted(VALID_ROLES)}"
                )

    # THE item_taxonomy_links CHECK WAS REMOVED 2026-09-16, and removing it is the fix
    # rather than renaming it. It validated `item_taxonomy_links.icf_code` against THIS
    # table, which was right while the ICF lens pointed at the grouping layer. Migration
    # 081 re-pointed that column at the ICF CODE registry, so the check had come to
    # compare real ICF codes against grouping codes and would have flagged every
    # legitimate row. It passed only because `item_taxonomy_links` holds zero rows --
    # CLAUDE.md rule 4's "treat a 0-row object as unproven, not clean", inside a blocking
    # gate. What it used to guarantee is now a real FOREIGN KEY
    # (`item_taxonomy_links.icf_code -> base_taxonomy_icf.icf_code`), which the database
    # enforces at write time and `schema_reference_audit` re-proves; a Python re-check of
    # a live FK is a second home for one rule (rule 5).

    # --- INTEGRITY: access_need_icf_grouping_map ---
    if _has_table(c, "access_need_icf_grouping_map"):
        for (gc,) in c.execute("SELECT grouping_code FROM access_need_icf_grouping_map"):
            n_examined += 1
            if gc not in grouping_codes:
                errors.append(f"access_need_icf_grouping_map: grouping_code {gc!r} not in base_icf_groupings")

    # --- COVERAGE (warnings) ---
    no_pop = sorted(grouping_codes - covered_by_pop)
    if no_pop:
        warnings.append(f"{len(no_pop)} groupings with zero population mappings: {no_pop}")
    summary.append(f"groupings with ≥1 population mapping: {len(covered_by_pop)}/{len(grouping_codes)}")
    return errors, warnings, summary, n_examined


def selftest():
    """Mutation harness (integrity-protocol Mode 1 rule 3): prove the checker FIRES."""
    con = sqlite3.connect(":memory:")
    con.executescript(
        "CREATE TABLE base_icf_groupings(grouping_code TEXT);"
        "CREATE TABLE populations(population_code TEXT);"
        "CREATE TABLE population_icf_grouping_map(population_code TEXT, grouping_code TEXT, role TEXT);"
        "INSERT INTO base_icf_groupings VALUES('DM-BAL'),('DM-STA');"
        "INSERT INTO populations VALUES('VES');"
    )
    cases = [
        ("clean: valid pop+grouping+role", "INSERT INTO population_icf_grouping_map VALUES('VES','DM-BAL','PRIMARY')", False),
        ("dangling grouping", "INSERT INTO population_icf_grouping_map VALUES('VES','DM-NOPE','PRIMARY')", True),
        ("dangling population", "INSERT INTO population_icf_grouping_map VALUES('XX','DM-BAL','PRIMARY')", True),
        ("bad role", "INSERT INTO population_icf_grouping_map VALUES('VES','DM-BAL','BOGUS')", True),
    ]
    ok = True
    for why, sql, expect in cases:
        con.execute("DELETE FROM population_icf_grouping_map")
        con.execute(sql)
        errs, _, _, _ = _check(con)
        got = len(errs) > 0
        status = "OK" if got == expect else "**MISSED**"
        if got != expect:
            ok = False
        print(f"  [{status}] {why} -> error={got} (expected {expect})")
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    if "--selftest" in sys.argv:
        return selftest()
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    errors, warnings, summary, n_examined = _check(con)
    for s in summary:
        print(f"  {s}")
    for w in warnings:
        print(f"  WARN: {w}")
    if errors:
        print(f"\nFAIL ICF-grouping-layer integrity ({DB}):")
        for e in errors:
            print(f"  {e}")
        print(f"\nFAIL: {len(errors)} integrity errors, {len(warnings)} coverage warnings")
        print(f"EXAMINED: {n_examined}")
        return 1
    print(f"\nOK ICF-grouping-layer integrity ({DB}): 0 errors, {len(warnings)} coverage warnings (non-fatal)")
    print(f"EXAMINED: {n_examined}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
