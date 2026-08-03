#!/usr/bin/env python3
"""The fully-evidenced walk: can a topic be traced to a best practice?

This file used to be four sections. Three were deleted on 2026-08-03 after an
adversarial review, and the reasons are worth keeping:

  A (islands) and B (edge orphans) duplicated scripts/audit/graph_audit.py,
  which already detects dangling references, orphans and empty tables, and
  which has a --selftest mutation harness this never had. Building a parallel
  sweep also violated CLAUDE.md §9 guardrail 3 ("don't spin up a new
  register/sweep — extend the existing apparatus"). Section B additionally
  carried a hand-maintained SOFT_EDGES list: a private copy of the schema, the
  exact anti-pattern its own docstring warned against.

  D ("missing features") reported `term_relations` and `cross_examinations` as
  absent — two tables the same session was proposing to build. An audit that
  reports its author's roadmap as a defect is not an audit. That is the whole
  reason this file was cut back rather than extended.

What survives is section C, because it measures the product rather than the
apparatus: of every ACTIVE topic, how many can be walked to a best practice,
and where the rest stop. Today that number is 0.

Usage:  python3 scripts/audit/table_connectivity.py
"""
import collections
import os
import sqlite3
import sys

DB_PATH = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")

# Each hop is required, not optional. A walk that survives only because a join
# is LEFT is not evidence of anything.
STAGES = [
    ("1 topic",            None),
    ("2 has sources",      "SELECT 1 FROM source_slug_links l WHERE l.slug=:s LIMIT 1"),
    ("3 sources mined",    "SELECT 1 FROM source_slug_links l JOIN evidence_sources e ON e.ref_id=l.ref_id "
                           "WHERE l.slug=:s AND e.citation_mining_status='mined' LIMIT 1"),
    ("4 values captured",  "SELECT 1 FROM source_slug_links l JOIN evidence_sources e ON e.ref_id=l.ref_id "
                           "WHERE l.slug=:s AND e.data_capture_status='captured' LIMIT 1"),
    ("5 population match", "SELECT 1 FROM source_slug_links l JOIN evidence_population_match m ON m.ref_id=l.ref_id "
                           "WHERE l.slug=:s AND m.target_population IN (SELECT population_code FROM populations) LIMIT 1"),
    ("6 has a spec",       "SELECT 1 FROM items i WHERE i.bpc_source_slug=:s LIMIT 1"),
    ("7 spec has a cell",  "SELECT 1 FROM items i JOIN evidence_cell_state c ON c.item_code=i.item_code "
                           "WHERE i.bpc_source_slug=:s LIMIT 1"),
    ("8 BEST PRACTICE",    "SELECT 1 FROM items i JOIN evidence_cell_state c ON c.item_code=i.item_code "
                           "WHERE i.bpc_source_slug=:s AND c.state IN ('stated','provisional') LIMIT 1"),
]


def main():
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    slugs = [r[0] for r in con.execute("SELECT slug FROM slugs WHERE status='ACTIVE'")]
    if not slugs:
        print("EXAMINED: 0\nVERDICT: FAIL — no ACTIVE slugs to walk")
        return 1

    reached_seq = set(slugs)
    print("Fully-evidenced walk — every hop required\n")
    print(f"  {'stage':22s} {'in sequence':>12} {'independent':>12}")
    for label, sql in STAGES:
        if sql is None:
            ind = set(slugs)
        else:
            ind = {s for s in slugs if con.execute(sql, {"s": s}).fetchone()}
        reached_seq &= ind
        flag = "!!" if not reached_seq else "  "
        print(f"{flag} {label:22s} {len(reached_seq):>7}/{len(slugs):<4} {len(ind):>7}/{len(slugs):<4}")

    print(f"\nEXAMINED: {len(slugs)}")
    print(f"FULLY-EVIDENCED WALKS: {len(reached_seq)} of {len(slugs)} ACTIVE topics")
    if reached_seq:
        print("  " + ", ".join(sorted(reached_seq)[:8]))
    print("\nThe independent column matters: where it is much higher than the "
          "in-sequence column,\nthe two halves of the pipeline are populated but "
          "do not meet on the same topic.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
