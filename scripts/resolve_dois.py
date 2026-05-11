#!/usr/bin/env python3
"""Batch DOI resolution via CrossRef API for evidence_sources table.

Two-phase approach:
  Phase 1: PMID → DOI via NCBI ID Converter (high confidence)
  Phase 2: Author + title → DOI via CrossRef title search (moderate confidence)

Environment variables:
  GUIDEBOOK_DB_PATH  — path to SQLite DB (default: data/guidebook.db)
  MAX_RESOLVE        — max Phase 2 candidates per run (default: 100)
"""

import sqlite3
import json
import urllib.request
import urllib.parse
import time
import sys
import os
import re

DB_PATH = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")
RATE_LIMIT = 0.5  # seconds between requests
MAX_RESOLVE = int(os.environ.get("MAX_RESOLVE", "100"))
USER_AGENT = "guidebook-project/1.0 (mailto:jordan@guidebook.dev)"

TABLE = "evidence_sources"


def ncbi_pmid_to_doi(pmid: str) -> str | None:
    """Convert PMID to DOI via NCBI ID Converter API."""
    url = (
        f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
        f"?ids={pmid}&format=json&tool=guidebook&email=jordan@guidebook.dev"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        records = data.get("records", [])
        if records and records[0].get("doi"):
            return records[0]["doi"]
    except Exception as e:
        print(f"  NCBI lookup error: {e}")
    return None


def crossref_title_search(author: str, title: str, year: str) -> str | None:
    """Query CrossRef for a DOI match by author + title keywords."""
    first_author = author.split(",")[0].split(" et al")[0].split("(")[0].strip()

    # Strip metadata noise from title field
    title_clean = re.sub(r"\[.*?\]", "", title)
    title_clean = re.sub(r"PMID[:\s]?\d+", "", title_clean, flags=re.IGNORECASE)
    title_clean = re.sub(r"PMC\d+", "", title_clean)
    title_clean = re.sub(r"GREY[^.;]*", "", title_clean, flags=re.IGNORECASE)
    title_clean = re.sub(r"DOI[:\s]?10\.\S+", "", title_clean, flags=re.IGNORECASE)
    title_clean = re.sub(r"[^\w\s]", " ", title_clean[:150])
    title_clean = " ".join(title_clean.split()[:14])

    if len(title_clean.split()) < 4:
        return None

    query = f"{first_author} {title_clean}"
    url = (
        f"https://api.crossref.org/works?"
        f"query={urllib.parse.quote(query)}&rows=3"
        f"&select=DOI,title,author,published-print,published-online"
    )

    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"  CrossRef error: {e}")
        return None

    items = data.get("message", {}).get("items", [])
    if not items:
        return None

    orig_words = set(re.sub(r"[^\w\s]", "", title.lower()).split())
    noise = {"grey", "pmid", "pmc", "unverified", "possible", "error",
             "wrong", "match", "tbc", "doi", "required", "the", "and",
             "for", "in", "of", "a", "an", "to", "on", "is", "with"}
    orig_words -= noise

    for item in items[:3]:
        doi = item.get("DOI", "")
        if not doi:
            continue
        cr_titles = item.get("title", [])
        cr_title = cr_titles[0] if cr_titles else ""
        cr_words = set(re.sub(r"[^\w\s]", "", cr_title.lower()).split()) - noise

        if not orig_words or not cr_words:
            continue

        overlap = len(orig_words & cr_words)
        overlap_ratio = overlap / min(len(orig_words), len(cr_words))

        # Year check
        year_match = True
        pub = item.get("published-print") or item.get("published-online")
        if pub and year:
            try:
                cr_year = pub.get("date-parts", [[None]])[0][0]
                if cr_year is not None:
                    year_match = abs(int(cr_year) - int(year)) <= 1
            except (ValueError, TypeError, IndexError):
                pass

        if overlap >= 3 and overlap_ratio >= 0.35 and year_match:
            return doi

    return None


def extract_pmid(title: str, notes: str, pmid_col: str) -> str | None:
    """Extract PMID from pmid column, title, or notes fields."""
    # Prefer the dedicated pmid column
    if pmid_col:
        m = re.search(r"(\d{5,})", str(pmid_col))
        if m:
            return m.group(1)
    combined = f"{title or ''} {notes or ''}"
    m = re.search(r"PMID[:\s]?(\d+)", combined, re.IGNORECASE)
    return m.group(1) if m else None


def is_standard_or_grey(title: str, notes: str, tier) -> bool:
    """Return True if source is unlikely to have a DOI."""
    combined = f"{title or ''} {notes or ''}"
    try:
        if tier is not None and int(tier) >= 4:
            return True
    except (ValueError, TypeError):
        pass
    if re.search(
        r"\bISO\b|\bDIN\b|\bBS \d|\bEN \d|CAN/|ANSI|ASHRAE|ASTM|IEEE"
        r"|PAS \d|\bNCC\b|\bADA\b|\bNBC\b|NFPA|IBC|OBOA|WELL v|Fitwel"
        r"|LEED|BREEAM|\bguideline\b|\bhandbook\b|\bmanual\b"
        r"|position statement|toolkit|\bframework\b|WHO|UN-Habitat"
        r"|\bRIBA\b|\bCNIB\b|\bRNID\b|\bHabinteg\b",
        combined, re.IGNORECASE
    ):
        return True
    return False


def main():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: DB not found at {DB_PATH}")
        return 1

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()]
    if TABLE not in tables:
        print(f"ERROR: {TABLE} table not found. Tables: {tables}")
        return 1

    ts = time.strftime("%Y-%m-%d %H:%M", time.gmtime())

    # ── Phase 1: PMID → DOI ──
    # Check both the dedicated pmid column and PMID mentions in title/notes
    pmid_rows = conn.execute(f"""
        SELECT ref_id, title, notes, pmid
        FROM {TABLE}
        WHERE (doi IS NULL OR doi = '')
        AND (
            (pmid IS NOT NULL AND pmid != '')
            OR title LIKE '%PMID%'
            OR notes LIKE '%PMID%'
        )
    """).fetchall()

    print(f"Phase 1 — PMID candidates: {len(pmid_rows)}")
    pmid_resolved = 0

    for r in pmid_rows:
        pmid = extract_pmid(r["title"], r["notes"], r["pmid"])
        if not pmid:
            continue
        doi = ncbi_pmid_to_doi(pmid)
        if doi:
            conn.execute(
                f"UPDATE {TABLE} SET doi = ?, "
                "updated_at = ?, updated_by_session = 'resolve-dois-action' "
                "WHERE ref_id = ?",
                (doi, ts, r["ref_id"])
            )
            pmid_resolved += 1
            print(f"  PMID→DOI: {r['ref_id']} (PMID:{pmid}) → {doi}")
        time.sleep(RATE_LIMIT)

    print(f"Phase 1 resolved: {pmid_resolved}\n")

    # ── Phase 2: title search ──
    title_rows = conn.execute(f"""
        SELECT ref_id, authors, year, title, notes, tier
        FROM {TABLE}
        WHERE (doi IS NULL OR doi = '')
        AND authors IS NOT NULL AND authors != ''
        AND authors != '(author TBC)'
        AND title IS NOT NULL AND length(title) > 20
        ORDER BY CAST(year AS INTEGER) DESC
        LIMIT ?
    """, (MAX_RESOLVE * 2,)).fetchall()  # over-fetch, filter below

    candidates = [
        r for r in title_rows
        if not is_standard_or_grey(r["title"], r["notes"], r["tier"])
    ][:MAX_RESOLVE]

    print(f"Phase 2 — Title search candidates: {len(candidates)}")
    title_resolved = 0
    skipped = 0

    for r in candidates:
        doi = crossref_title_search(
            r["authors"], r["title"], str(r["year"] or "")
        )
        if doi:
            conn.execute(
                f"UPDATE {TABLE} SET doi = ?, "
                "updated_at = ?, updated_by_session = 'resolve-dois-action' "
                "WHERE ref_id = ?",
                (doi, ts, r["ref_id"])
            )
            title_resolved += 1
            print(f"  RESOLVED: {r['ref_id']} ({r['authors'][:30]}, {r['year']}) → {doi}")
        else:
            skipped += 1

        time.sleep(RATE_LIMIT)

    conn.commit()

    # ── Summary ──
    total = conn.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]
    with_doi = conn.execute(
        f"SELECT COUNT(*) FROM {TABLE} WHERE doi IS NOT NULL AND doi != ''"
    ).fetchone()[0]
    without_doi = total - with_doi

    print(f"\n{'='*50}")
    print(f"Phase 1 (PMID→DOI):    {pmid_resolved}")
    print(f"Phase 2 (title search): {title_resolved}")
    print(f"Total resolved:         {pmid_resolved + title_resolved}")
    print(f"Skipped (no match):     {skipped}")
    print(f"DOI coverage:           {with_doi}/{total} ({100*with_doi//total}%)")
    print(f"Remaining without DOI:  {without_doi}")
    print(f"{'='*50}")

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
