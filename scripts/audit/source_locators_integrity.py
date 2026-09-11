#!/usr/bin/env python3
"""source_locators_integrity.py — a locator's title must describe the work its
identifier points at.

WHAT WRONG THING REACHES THE *GUIDEBOOK* IF THIS DOES NOT EXIST (CLAUDE.md §8's bar,
which is about the book and not the apparatus):

  A session screens the stash by TITLE and admits, or rejects, the wrong work. The
  identifiers in `source_locators` are sound; the titles are not. A row whose DOI
  resolves to Rouvier 2022 while its title names a different paper is a lead that
  reads as screened when it has not been, and R9b tells the next session to REUSE
  that ref_id rather than mint a new one -- so the wrong title travels forward into
  an admission, and from there into a citation. That is failure mode (c) reached by
  a different road: not an invented author, but a real author attached to the wrong
  work, and every gate that checks whether a field is POPULATED passes it.

RULED, NOT INVENTED. The adjudication of 2026-09-11 §2.3 ruled a gate by this name
(`scratchpad/pr-134-repository-orientation/ADJUDICATION.md`, Ruling 2.3). It was
ruled and never built; the corruption was measured four times by four sessions
writing the same ad-hoc query. A measurement nobody registered is a measurement the
next session repeats.

THE SIGNATURE IS CONSERVATIVE ON PURPOSE. A title that merely looks odd is not
detectable; a title that CONTAINS A DOI is, and a bibliographic title never does.
Two cases, reported separately because they are different facts:

  MISMATCH  the title embeds a DOI and the row carries a DIFFERENT one. This is the
            keyspace fold: two ref-id ranges were merged as one by
            data_20260823225142, so a title landed beside a stranger's identifier.
  ORPHAN    the title embeds a DOI and the row carries none, so there is nothing to
            compare. Suspect, not provable. Reported, never failed.

WHY THE REPAIR IS NOT IN THIS FILE. `db.py` has no writer that can set
`source_locators.title` -- `update-locator` sets `status` only -- and §4 makes that a
coverage bug to fix rather than a licence to hand-write SQL. The writer this needs is
shaped like `correct-source`: it takes NO value flag and reads the true title from a
persisted retrieval payload, because writing a title from anything other than bytes
is how these rows got wrong in the first place. Until that writer exists this check
reports and does not repair, and the count below is the size of the repair.
"""
import argparse
import os
import re
import sqlite3
import sys
from pathlib import Path

# HONOURS GUIDEBOOK_DB_PATH. The blocking db_path_env_audit caught medical_lens_integrity
# hardcoding this and was right to: a script that ignores the variable silently reads the
# committed database while a test believes it is reading a scratch copy, which makes this
# check's own fault injection unreliable.
DB = Path(os.environ.get("GUIDEBOOK_DB_PATH",
                         Path(__file__).resolve().parents[2] / "data" / "guidebook.db"))

# Deliberately not anchored: a DOI appearing ANYWHERE in a title is the signal.
DOI = re.compile(r'10\.\d{4,9}/[^\s"\'<>,;)\]]+')


def _doi_in(text):
    m = DOI.search(text or "")
    return m.group(0).rstrip(".").lower() if m else None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    # --db EXISTS SO THIS CHECK CAN BE FAULT-INJECTED. A gate nobody has seen go red
    # is a gate nobody has tested.
    ap.add_argument("--db", default=str(DB), help="database to read (default: canonical)")
    ap.add_argument("--max-show", type=int, default=8)
    args = ap.parse_args(argv)

    con = sqlite3.connect(f"file:{args.db}?mode=ro", uri=True)
    rows = list(con.execute(
        "SELECT ref_id, title, doi FROM source_locators WHERE title IS NOT NULL"))

    mismatch, orphan = [], []
    for ref_id, title, doi in rows:
        embedded = _doi_in(title)
        if not embedded:
            continue
        if not doi:
            orphan.append((ref_id, embedded))
        elif embedded != (doi or "").lower():
            mismatch.append((ref_id, doi, embedded))

    print("=" * 70)
    print("source_locators_integrity")
    print("=" * 70)
    for ref_id, doi, embedded in mismatch[:args.max_show]:
        print(f"  [FAIL] {ref_id}: doi={doi} but its TITLE embeds {embedded} — the title "
              f"describes a different work")
    if len(mismatch) > args.max_show:
        print(f"  ... and {len(mismatch) - args.max_show} more")
    for ref_id, embedded in orphan[:args.max_show]:
        print(f"  [NOTE] {ref_id}: title embeds {embedded} and the row carries no doi — "
              f"nothing to compare, suspect not proven")
    if len(orphan) > args.max_show:
        print(f"  ... and {len(orphan) - args.max_show} more")

    if not rows:
        print("  source_locators holds no title-bearing row.")
    print(f"\n  title-bearing rows: {len(rows)}  "
          f"titles embedding a doi: {len(mismatch) + len(orphan)}  "
          f"mismatched: {len(mismatch)}  unprovable: {len(orphan)}")
    if mismatch:
        print("  REPAIR IS BLOCKED ON A WRITER, NOT ON A DECISION: db.py cannot set "
              "source_locators.title.")
        print("  It needs a correct-locator that reads the title from a persisted "
              "retrieval payload and takes no value flag, the way correct-source does.")
    print(f"EXAMINED: {len(rows)}")
    print("VERDICT: " + ("FAIL" if mismatch else "CLEAN"))
    return 1 if mismatch else 0


if __name__ == "__main__":
    raise SystemExit(main())
