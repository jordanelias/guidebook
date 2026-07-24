#!/usr/bin/env python3
"""validate_axes.py — axis-layer integrity + coverage (E6 of the 2026-07-21 ratification register).

The two-layer functional taxonomy (governance/functional-taxonomy.md) added an `axes` layer that
populations, access-needs, and (eventually) items map onto. Nothing validated that layer's
referential integrity or surfaced its coverage gaps. This does both:

INTEGRITY (ERROR, exit 1) — profile-layer containment:
  - every population_axis_map.axis_code resolves to an axes row
  - every population_axis_map.population_code resolves to a populations row
  - every item_axis_links.axis_code resolves to an axes row (when the table has rows)
  - every access_need_axis_map.axis_code resolves to an axes row (when present)
  - population_axis_map.role ∈ {PRIMARY, SECONDARY, ALIAS, SITUATIONAL}

COVERAGE (WARN, non-fatal) — surfaced so the debt is visible, not hidden:
  - axes with zero population mappings
  - axes with zero item_axis_links (the E3 debt — items not yet linked to axes)
  - a per-axis coverage summary

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
    """Returns (errors, warnings, summary_lines)."""
    c = con.cursor()
    errors, warnings, summary = [], [], []
    axis_codes = {r[0] for r in c.execute("SELECT axis_code FROM axes")}
    pop_codes = {r[0] for r in c.execute("SELECT population_code FROM populations")}
    summary.append(f"axes defined: {len(axis_codes)}")

    # --- INTEGRITY: population_axis_map ---
    covered_by_pop = set()
    if _has_table(c, "population_axis_map"):
        for pop, ax, role in c.execute(
            "SELECT population_code, axis_code, role FROM population_axis_map"
        ):
            if ax not in axis_codes:
                errors.append(f"population_axis_map: axis_code {ax!r} (pop {pop}) not in axes")
            else:
                covered_by_pop.add(ax)
            if pop not in pop_codes:
                errors.append(f"population_axis_map: population_code {pop!r} not in populations")
            if role is not None and role not in VALID_ROLES:
                errors.append(
                    f"population_axis_map: role {role!r} (pop {pop}, axis {ax}) not in {sorted(VALID_ROLES)}"
                )

    # --- INTEGRITY: item_axis_links ---
    covered_by_item = set()
    if _has_table(c, "item_axis_links"):
        for (ax,) in c.execute("SELECT axis_code FROM item_axis_links"):
            if ax not in axis_codes:
                errors.append(f"item_axis_links: axis_code {ax!r} not in axes")
            else:
                covered_by_item.add(ax)

    # --- INTEGRITY: access_need_axis_map ---
    if _has_table(c, "access_need_axis_map"):
        for (ax,) in c.execute("SELECT axis_code FROM access_need_axis_map"):
            if ax not in axis_codes:
                errors.append(f"access_need_axis_map: axis_code {ax!r} not in axes")

    # --- COVERAGE (warnings) ---
    no_pop = sorted(axis_codes - covered_by_pop)
    no_item = sorted(axis_codes - covered_by_item)
    if no_pop:
        warnings.append(f"{len(no_pop)} axes with zero population mappings: {no_pop}")
    if no_item:
        warnings.append(
            f"{len(no_item)} axes with zero item_axis_links (E3 debt — items not linked to axes): {no_item}"
        )
    summary.append(f"axes with ≥1 population mapping: {len(covered_by_pop)}/{len(axis_codes)}")
    summary.append(f"axes with ≥1 item link: {len(covered_by_item)}/{len(axis_codes)}")
    return errors, warnings, summary


def selftest():
    """Mutation harness (integrity-protocol Mode 1 rule 3): prove the checker FIRES."""
    con = sqlite3.connect(":memory:")
    con.executescript(
        "CREATE TABLE axes(axis_code TEXT);"
        "CREATE TABLE populations(population_code TEXT);"
        "CREATE TABLE population_axis_map(population_code TEXT, axis_code TEXT, role TEXT);"
        "INSERT INTO axes VALUES('AX-BAL'),('AX-STA');"
        "INSERT INTO populations VALUES('VES');"
    )
    cases = [
        ("clean: valid pop+axis+role", "INSERT INTO population_axis_map VALUES('VES','AX-BAL','PRIMARY')", False),
        ("dangling axis", "INSERT INTO population_axis_map VALUES('VES','AX-NOPE','PRIMARY')", True),
        ("dangling population", "INSERT INTO population_axis_map VALUES('XX','AX-BAL','PRIMARY')", True),
        ("bad role", "INSERT INTO population_axis_map VALUES('VES','AX-BAL','BOGUS')", True),
    ]
    ok = True
    for why, sql, expect in cases:
        con.execute("DELETE FROM population_axis_map")
        con.execute(sql)
        errs, _, _ = _check(con)
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
    errors, warnings, summary = _check(con)
    for s in summary:
        print(f"  {s}")
    for w in warnings:
        print(f"  WARN: {w}")
    if errors:
        print(f"\nFAIL axis-layer integrity ({DB}):")
        for e in errors:
            print(f"  {e}")
        print(f"\nFAIL: {len(errors)} integrity errors, {len(warnings)} coverage warnings")
        return 1
    print(f"\nOK axis-layer integrity ({DB}): 0 errors, {len(warnings)} coverage warnings (non-fatal)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
