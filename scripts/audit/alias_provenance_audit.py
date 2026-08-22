#!/usr/bin/env python3
"""
scripts/audit/alias_provenance_audit.py — provenance + verification surface for
the controlled vocabulary (terms / term_aliases).

Why this exists. `term_aliases` drives multilingual retrieval via
the (now deleted) query generator, but nothing recorded *where an alias came
from*. Provenance lived in a freeform `notes` string when it was recorded at
all, so a reader could not distinguish a term lifted from a national standards
glossary from one a model produced. On 2026-07-25, 789 non-English aliases
carried no marker of any kind.

That is a trust problem, not a formatting one: retrieval built on unverified
terminology can silently miss the literature it was meant to find, and nobody
downstream can tell which rows to distrust.

What it enforces. Every alias created on or after CUTOFF_SESSION_DATE must
carry a recognised provenance marker. Earlier rows are grandfathered and
reported as UNKNOWN — the same backfill-on-touch convention the attestation
system uses, so this lands as a forward commitment rather than a demand to
retro-document 881 legacy rows before anything else can move.

The verification markers come from references/native-alias-verification.md, so
there is a defined route out of MODEL-GENERATED rather than a permanent label:

    MODEL-GENERATED  -> VERIFIED-GLOSSARY  (national standards body glossary)
                     -> VERIFIED-NATIVE    (qualified native-speaker review)
                     -> VERIFIED-CROSS     (corroborated across published sources)

It also reports languages that lang_jur_map requires but for which no alias
exists at all — those cannot be searched, whatever the coverage tables say.

Read-only. Exit 1 on an unmarked post-cutoff alias; exit 0 otherwise.
"""
import os
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO / "data" / "guidebook.db"))

# Sessions from this date forward must record provenance. Earlier cohorts
# (session_2026-05-09-terms, -terms-2, session_2026-05-10f-term-alias-expansion)
# predate the convention and are reported, not failed.
CUTOFF_SESSION_DATE = "2026-07-24"

VERIFIED_MARKERS = ("VERIFIED-GLOSSARY", "VERIFIED-NATIVE", "VERIFIED-CROSS")
PROVENANCE_MARKERS = ("model-generated", "curated", "repo shorthand") + VERIFIED_MARKERS


def classify(notes):
    n = notes or ""
    for m in VERIFIED_MARKERS:
        if m in n:
            return m
    if "model-generated" in n:
        return "MODEL-GENERATED"
    if "curated" in n:
        return "CURATED-EN"
    if "repo shorthand" in n:
        return "PROJECT-CODE"
    return "UNKNOWN"


def session_date(session):
    """Extract YYYY-MM-DD from a session slug like session_2026-07-25-foo."""
    parts = (session or "").split("_", 1)
    tail = parts[1] if len(parts) > 1 else ""
    return tail[:10]


def main():
    if not DB_PATH.exists():
        print(f"database not found: {DB_PATH}", file=sys.stderr)
        return 2
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row

    rows = con.execute(
        "SELECT term_id, alias, language, notes, created_by_session FROM term_aliases"
    ).fetchall()

    by_lang = {}
    offenders = []
    for r in rows:
        cls = classify(r["notes"])
        d = by_lang.setdefault(r["language"], {})
        d[cls] = d.get(cls, 0) + 1
        if cls == "UNKNOWN" and session_date(r["created_by_session"]) >= CUTOFF_SESSION_DATE:
            offenders.append(r)

    print("=" * 74)
    print("alias_provenance_audit.py — controlled-vocabulary provenance")
    print("=" * 74)
    print(f"database: {DB_PATH}")
    print(f"aliases:  {len(rows)}")
    print(f"EXAMINED: {len(rows)}\n")

    hdr = f"{'lang':<6}{'total':>7}{'verified':>10}{'model-gen':>11}{'curated':>9}{'code':>6}{'UNKNOWN':>9}"
    print(hdr)
    print("-" * len(hdr))
    tot_unknown = tot_verified = 0
    for lang in sorted(by_lang):
        d = by_lang[lang]
        ver = sum(d.get(m, 0) for m in VERIFIED_MARKERS)
        tot = sum(d.values())
        unk = d.get("UNKNOWN", 0)
        tot_unknown += unk
        tot_verified += ver
        print(f"{lang:<6}{tot:>7}{ver:>10}{d.get('MODEL-GENERATED',0):>11}"
              f"{d.get('CURATED-EN',0):>9}{d.get('PROJECT-CODE',0):>6}{unk:>9}")
    print("-" * len(hdr))
    print(f"{'all':<6}{len(rows):>7}{tot_verified:>10}"
          f"{sum(d.get('MODEL-GENERATED',0) for d in by_lang.values()):>11}"
          f"{sum(d.get('CURATED-EN',0) for d in by_lang.values()):>9}"
          f"{sum(d.get('PROJECT-CODE',0) for d in by_lang.values()):>6}{tot_unknown:>9}")

    # Languages required by lang_jur_map that have no vocabulary at all.
    try:
        missing = [r[0] for r in con.execute(
            "SELECT DISTINCT language FROM lang_jur_map WHERE lower(language) NOT IN "
            "(SELECT DISTINCT lower(language) FROM term_aliases) ORDER BY 1")]
    except sqlite3.OperationalError:
        missing = []
    if missing:
        print(f"\nREQUIRED BUT UNSEARCHABLE — no aliases at all: {', '.join(missing)}")
        print("  lang_jur_map requires these; a per-language query builder cannot emit a")
        print("  query without vocabulary, so their search coverage is structurally zero.")
        print("  Build from published glossaries (references/native-alias-verification.md).")

    if tot_verified == 0:
        print(f"\nNOTE: no alias has reached {'/'.join(VERIFIED_MARKERS)} yet.")
        print("  Non-English retrieval currently rests entirely on unreviewed terminology.")

    if tot_unknown:
        print(f"\n{tot_unknown} grandfathered alias(es) predate the provenance convention "
              f"(before {CUTOFF_SESSION_DATE}).")
        print("  Reported, not failed — record provenance on next touch.")

    if offenders:
        print(f"\nFAIL: {len(offenders)} alias(es) created on/after {CUTOFF_SESSION_DATE} "
              f"carry no provenance marker:")
        for r in offenders[:20]:
            print(f"  {r['term_id']}  {r['language']}  {r['alias']}  "
                  f"({r['created_by_session']})")
        if len(offenders) > 20:
            print(f"  ... and {len(offenders) - 20} more")
        print(f"\n  Record one of: {', '.join(PROVENANCE_MARKERS)} in term_aliases.notes.")
        return 1

    print(f"\nRESULTS: all post-{CUTOFF_SESSION_DATE} aliases carry provenance")
    return 0


if __name__ == "__main__":
    sys.exit(main())
