#!/usr/bin/env python3
"""R9 pre-check, read-only. Usage: python3 r9check.py <doi> [<doi> ...]"""
import sqlite3, sys
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
c = con.cursor()
for doi in sys.argv[1:]:
    d = doi.strip().lower()
    rows = list(c.execute(
        "SELECT ref_id, doi, title, authors, pub_year, tier_claimed, status "
        "FROM source_locators WHERE lower(doi)=?", (d,)))
    ev = list(c.execute("SELECT ref_id FROM evidence_sources WHERE lower(doi)=?", (d,)))
    print(f"\n### {doi}")
    if not rows and not ev:
        print("  R9: NOT HELD in source_locators or evidence_sources")
    for r in rows:
        print(f"  source_locators HIT ref_id={r[0]} status={r[6]} tier={r[5]} year={r[4]}")
        print(f"     title  : {r[2]}")
        print(f"     authors: {r[3]}")
    if len(rows) > 1:
        print(f"  *** WARNING: DOI HELD UNDER {len(rows)} ref_ids — R9 DUPLICATE-IDENTITY DEFECT ***")
    for r in ev:
        print(f"  evidence_sources HIT ref_id={r[0]}")
