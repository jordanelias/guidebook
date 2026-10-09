#!/usr/bin/env python3
"""
scripts/audit/observation_verbatim_audit.py — is each observation's quote in its source?

WHY THIS EXISTS (tooling T1, 2026-10-09; catalogue-plan-v2 section 8.2, critique F7).
An observation records that a source USES a phrase, with the sentence it sits in. Every
term and parameter the project mints comes from one. Until migration 102 nothing compared
that sentence with the source: the verbatim check had one call site, add-extraction. The
plan measured the 88 observations then held: 34 quotes in a file saved for their own
source, 37 only in some other source's file, 17 in no saved file at all. `db.py
observe-term` now refuses a new observation whose quote is not in its source's saved text
(or records an exemption); this is the BACKSTOP for the rows written before that, and for
any row arriving by another route (a data migration written by hand).

WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT IT (CLAUDE.md section 8): a vocabulary term
minted from a phrase the source never used, which no later gate can tell from a real one
-- the 2026-08-19 fabrication shape (CLAUDE.md 5(c)) one stage along. Its readers: R16
(every adjudicated observation names a disposed term) and the adversarial pass, which
reads the listed rows.

WHAT IT COUNTS, per observation, from retrieval_log.locate_quote (one matching rule):
  scoped    the quote is in a file saved FOR this ref_id               -- fine
  unscoped  only in another source's file (no structured ref_id)       -- counted
  missing   in no persisted, decodable artefact, or no quote at all    -- counted
  exempt    the row carries a recorded [VERBATIM-EXEMPT: reason]       -- reported
and REPORTS, separately, observations whose phrase is not inside their own quote.

RATCHET, NOT A FLOOR OF ZERO. The pre-102 debt cannot be repaired by this tooling PR (it
would be research rows, CLAUDE.md rule 10), so the two counted classes are compared with
`governance/research-contract-baseline.json` (keys observation-quote-missing and
observation-quote-unscoped). The check fails when either count EXCEEDS its baseline; a
count below it is debt paid, and the baseline is lowered in the PR that pays it. That
file's ratchet is witnessed by git (research_batch_dod.py --check-baseline, the blocking research_contract_baseline_ratchet), so the
numbers can only go down. Re-derive them by running this, never from a figure in prose.

Usage:
    python3 scripts/audit/observation_verbatim_audit.py
Exit 0 within baseline; 1 a count above baseline; 2 cannot run.
"""
import json
import os
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "research"))
import retrieval_log                                                   # noqa: E402

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO / "data" / "guidebook.db"))
BASELINE_PATH = REPO / "governance" / "research-contract-baseline.json"
#: The two baselined classes, keyed as the baseline file names them.
KEYS = {"missing": "observation-quote-missing", "unscoped": "observation-quote-unscoped"}
EXEMPT_MARK = "[VERBATIM-EXEMPT:"


def classify(conn):
    """[(observation_id, ref_id, kind, detail, phrase_inside_quote)] for every row."""
    out = []
    for oid, ref, surface, quote, notes in conn.execute(
            "SELECT observation_id, ref_id, surface_form, context_quote, notes "
            "FROM observed_terms ORDER BY observation_id"):
        inside = bool(quote) and (retrieval_log.normalise_quote(surface)
                                  in retrieval_log.normalise_quote(quote))
        if EXEMPT_MARK in (notes or ""):
            out.append((oid, ref, "exempt", "recorded exemption on the row", inside))
        elif not (quote or "").strip():
            out.append((oid, ref, "missing", "no context_quote", inside))
        else:
            kind, detail = retrieval_log.locate_quote(quote, ref_id=ref)
            out.append((oid, ref, kind, detail, inside))
    return out


def main():
    if not DB_PATH.exists():
        print(f"observation_verbatim_audit: no database at {DB_PATH}", file=sys.stderr)
        return 2
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        rows = classify(conn)
    finally:
        conn.close()
    base = {}
    if BASELINE_PATH.exists():
        base = json.loads(BASELINE_PATH.read_text(encoding="utf-8")).get("counts", {})

    by = {}
    for r in rows:
        by.setdefault(r[2], []).append(r)
    print("observation_verbatim_audit — is each observation's quote in its own source?")
    print(f"EXAMINED: {len(rows)}")
    for kind in ("scoped", "unscoped", "missing", "exempt"):
        print(f"  {kind:<9} {len(by.get(kind, []))}")
    outside = [r for r in rows if not r[4]]
    print(f"  REPORTED, not counted: {len(outside)} observation(s) whose phrase is not "
          f"inside its own quote: {[r[0] for r in outside][:20]}")
    if by.get("exempt"):
        print(f"  REPORTED, not counted: exempt observation(s) "
              f"{[r[0] for r in by['exempt']][:20]} -- the adversarial pass reads each "
              f"reason")

    over = []
    for kind, key in KEYS.items():
        n = len(by.get(kind, []))
        b = base.get(key)
        if b is None:
            over.append(f"{kind}: {n} with no baseline entry {key!r} in {BASELINE_PATH.name}")
        elif n > b:
            over.append(f"{kind}: {n} > baseline {b} ({key})")
            for oid, ref, _k, detail, _i in by[kind][:20]:
                print(f"    observation {oid} ({ref}): {detail[:160]}")
        elif n < b:
            print(f"  {kind}: {n} < baseline {b} -- debt paid down; lower {key} in "
                  f"{BASELINE_PATH.relative_to(REPO)} in this PR")
        else:
            print(f"  {kind}: {n} (baseline {b}) -- INHERITED DEBT, not a regression")
    if over:
        print("FAIL: " + "; ".join(over) + ". A new observation's quote must be in a file "
              "saved for its source (db.py observe-term refuses otherwise), so a rise means "
              "a row arrived by another route or an artefact was lost.")
        return 1
    print("PASS: no class above its baseline")
    return 0


if __name__ == "__main__":
    sys.exit(main())
