#!/usr/bin/env python3
"""
scripts/audit/author_fidelity_audit.py — are the stored authors the paper's actual authors?

WHY THIS EXISTS
---------------
On 2026-08-19 the first research batch after the restart stored FABRICATED author
lists on all five of its admissions: 12 of 19 evidence_source_authors rows named
people who did not write the cited paper. It was found by an adversarial pass, not
by a gate.

Nothing caught it, and the reason is precise: every existing check asks whether the
author fields are POPULATED, never whether they are TRUE.

  C03  first_author_last is non-empty          -> passed
  G02  a COMPLETE source has >=1 author row     -> passed
  R9   no duplicate DOI                         -> passed
  R10  locator resolved and outcome recorded    -> passed
  test_db_integrity                             -> 72/72
  research_protocol_audit                       -> 0 issues

The rows were simultaneously stamped verification_status='VERIFIED',
verified_by_tool='crossref', metadata_quality='COMPLETE',
author_count_is_complete=1 and verification_disposition='CLOSED'. Those flags
asserted exactly the property that failed, so no downstream check would ever have
revisited them. A presence check cannot detect confabulation; only a COMPARISON
against the authoritative payload can.

The worst instance was doctrinal rather than clerical. A Co-1 source -- lived
experience, co-primary with T1 under CRPD Art 4.3 -- had its autistic community
co-authors deleted and replaced with academics who did not write the paper. The
Co-1 tier was claimed while the evidence of co-production was erased. In a
guidebook centred on disabled people that is not a metadata slip.

WHAT IT DOES
------------
For every evidence_sources row carrying a DOI, fetch the Crossref record and
compare the stored author surnames and count against it, in order.

    python3 scripts/audit/author_fidelity_audit.py
    python3 scripts/audit/author_fidelity_audit.py --session <id>
    python3 scripts/audit/author_fidelity_audit.py --selftest

Read-only. Never writes to the database.
"""

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))
API = "https://api.crossref.org/works/"


def norm(s):
    """Compare surnames without punting on accents or case.

    Rosas-Pérez must equal Rosas-Perez; andsensory must equal AndSensory. This is
    deliberately loose on FORM and strict on IDENTITY -- the failure being caught
    is a different person, not a different encoding.
    """
    s = unicodedata.normalize("NFKD", (s or "").strip().lower())
    return "".join(ch for ch in s if not unicodedata.combining(ch))


def crossref(doi, timeout=40):
    r = subprocess.run(["curl", "-sS", "--max-time", str(timeout), API + doi],
                       capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        return None
    try:
        return json.loads(r.stdout)["message"]
    except Exception:
        return None


def audit(session=None, limit=None, sleep=1.0):
    if not DB_PATH.exists():
        print(f"ERROR: no database at {DB_PATH}")
        print("EXAMINED: 0")
        return 1
    cx = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    q = ("SELECT ref_id, doi, author_count FROM evidence_sources "
         "WHERE COALESCE(doi,'') <> ''")
    args = []
    if session:
        q += " AND created_by_session = ?"
        args.append(session)
    q += " ORDER BY ref_id"
    rows = cx.execute(q, args).fetchall()
    if limit:
        rows = rows[:limit]

    print("=" * 78)
    print("author_fidelity_audit — stored authors vs the authoritative record")
    print("=" * 78)

    examined, mismatched, unreachable = 0, [], []
    for ref_id, doi, stored_count in rows:
        stored = [r[0] for r in cx.execute(
            "SELECT last_name FROM evidence_source_authors WHERE ref_id=? ORDER BY position",
            (ref_id,))]
        m = crossref(doi)
        if m is None:
            unreachable.append((ref_id, doi))
            time.sleep(sleep)
            continue
        real = [(a.get("family") or a.get("name") or "") for a in m.get("author", [])]
        examined += 1
        if [norm(x) for x in real] != [norm(x) for x in stored]:
            mismatched.append((ref_id, doi, real, stored, stored_count))
        time.sleep(sleep)

    print(f"  EXAMINED: {examined}")
    if unreachable:
        print(f"  UNREACHABLE: {len(unreachable)} DOI(s) could not be retrieved "
              f"— NOT counted as passing:")
        for ref_id, doi in unreachable[:5]:
            print(f"      {ref_id}  {doi}")

    if mismatched:
        print("-" * 78)
        for ref_id, doi, real, stored, sc in mismatched:
            print(f"  ✗ {ref_id} ({doi})")
            print(f"      record : {len(real)}  {'; '.join(real)}")
            print(f"      stored : {len(stored)} (author_count={sc})  {'; '.join(stored)}")
            ghosts = [s for s in stored if norm(s) not in {norm(r) for r in real}]
            erased = [r for r in real if norm(r) not in {norm(s) for s in stored}]
            if ghosts:
                print(f"      NOT AN AUTHOR OF THIS PAPER: {'; '.join(ghosts)}")
            if erased:
                print(f"      ERASED FROM THE RECORD:      {'; '.join(erased)}")
        print("-" * 78)
        print(f"\n  {len(mismatched)} source(s) store an author list that is not the "
              f"paper's.\n  A populated field is not a true one. Correct by migration "
              f"from the payload,\n  never by hand -- hand-entry is how these arrived.")
        return 1

    if unreachable and examined == 0:
        print("\n  INDETERMINATE — nothing could be retrieved. This is not a pass.")
        return 1
    print("\n  CLEAN — every stored author list matches the authoritative record.")
    return 0


def selftest():
    """Prove the comparison catches what it is for, without touching the network."""
    cases = [
        ("identical",              ["MacLennan", "Woolley"], ["MacLennan", "Woolley"], True),
        ("accent-insensitive",     ["Rosas-Pérez"],          ["Rosas-Perez"],          True),
        ("case-insensitive",       ["andsensory"],           ["AndSensory"],           True),
        ("substituted co-author",  ["MacLennan", "Woolley"], ["MacLennan", "Roach"],   False),
        ("truncated list (7->3)",  ["A", "B", "C", "D", "E", "F", "G"], ["A", "B", "C"], False),
        ("reordered authors",      ["Wright", "McKay"],      ["McKay", "Wright"],      False),
        ("empty stored",           ["Wright"],               [],                       False),
    ]
    ok = 0
    print("\n--- author_fidelity_audit selftest ---")
    for name, real, stored, want in cases:
        got = [norm(x) for x in real] == [norm(x) for x in stored]
        good = got == want
        ok += good
        print(f"  {'PASS' if good else '**FAIL**'}: {name}")
    print(f"\nRESULTS: {ok}/{len(cases)} selftest cases pass")
    print("SELFTEST: " + ("PASS" if ok == len(cases) else "FAIL"))
    return 0 if ok == len(cases) else 1


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--session", help="Limit to sources created by this session")
    p.add_argument("--limit", type=int, help="Check at most N sources")
    p.add_argument("--sleep", type=float, default=1.0, help="Delay between API calls")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    sys.exit(selftest() if a.selftest else audit(a.session, a.limit, a.sleep))


if __name__ == "__main__":
    main()
