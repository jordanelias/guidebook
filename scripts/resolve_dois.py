#!/usr/bin/env python3
"""DOI resolution against evidence_sources v2 schema.

Uses the structured columns produced by the v2 migration to query CrossRef and
NCBI precisely instead of parsing free-form text. Honors `doi_resolution_outcome`
so previously-rejected matches are never retried.

Phase 1 — NCBI PMID → DOI (high confidence; biomedical sources).
Phase 2 — CrossRef structured query on first_author_last + pub_title + pub_year.

Acceptance criteria (Phase 2):
  - Author surname must appear in CrossRef result's first 3 authors (case-insensitive).
  - Title-word Jaccard overlap >= 0.55 after stopword removal.
  - Year matches within +/- 1.
  - Only one plausible candidate (ambiguity = reject).

Skip behavior:
  - doi_resolution_outcome = 'REVERTED'  -> permanently skipped.
  - doi_resolution_outcome = 'NO-MATCH' within SKIP_NO_MATCH_DAYS -> skipped.
  - is_corporate_primary = 1 -> skipped (CrossRef author query unsuited for orgs).
  - pub_year IS NULL or first_author_last IS NULL -> skipped.
  - source_type in ('standard','grey','internal','website','guideline') -> skipped.

Env vars:
  GUIDEBOOK_DB_PATH   path to SQLite (default: data/guidebook.db)
  MAX_RESOLVE         max Phase 2 candidates per run (default: 500)
  SKIP_NO_MATCH_DAYS  days before retrying a NO-MATCH (default: 30)
"""

import json
import os
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DB_PATH = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")
MAX_RESOLVE = int(os.environ.get("MAX_RESOLVE", "500"))
SKIP_NO_MATCH_DAYS = int(os.environ.get("SKIP_NO_MATCH_DAYS", "30"))
RATE_LIMIT = 0.5
USER_AGENT = "guidebook-project/2.0 (mailto:jordan@guidebook.dev)"
TABLE = "evidence_sources"

MIN_TITLE_OVERLAP_RATIO = 0.55
MIN_TITLE_OVERLAP_WORDS = 4
MAX_YEAR_DELTA = 1

ELIGIBLE_TYPES = (
    "journal_article", "book", "book_chapter", "thesis",
    "conference_paper", "report", "case_study", "primary_research",
)

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "in", "on", "at", "to", "for",
    "with", "by", "from", "as", "is", "are", "was", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "this", "that", "these", "those",
    "it", "its", "their", "them", "they", "we", "our", "us",
}


def fetch_json(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def ncbi_pmid_to_doi(pmid):
    """Convert PMID to DOI via NCBI ID Converter.

    Returns (doi, status) where status is:
      'resolved'  - DOI found and returned
      'no-doi'    - NCBI responded but record has no DOI
      'transient' - network/auth error; do not mark NO-MATCH
    """
    url = (
        "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
        f"?ids={pmid}&format=json&tool=guidebook&email=jordan@guidebook.dev"
    )
    try:
        data = fetch_json(url, timeout=15)
    except urllib.error.HTTPError as e:
        if e.code == 403 or e.code >= 500:
            print(f"    NCBI transient error {e.code} for PMID {pmid}")
            return None, "transient"
        return None, "no-doi"
    except Exception as e:
        print(f"    NCBI transient error for PMID {pmid}: {e}")
        return None, "transient"

    records = data.get("records", []) or []
    if records and records[0].get("doi"):
        return records[0]["doi"], "resolved"
    return None, "no-doi"


def canonical_doi(doi):
    """Normalize a DOI for equality comparison.

    CrossRef occasionally returns near-duplicates like '10.1037//x' and '10.1037/x'
    that resolve to the same paper but compare as different strings. Collapse double
    slashes and lowercase for the comparison key only — the original string is what
    we store.
    """
    if not doi:
        return ""
    return re.sub(r"/{2,}", "/", doi.strip().lower())


def normalize_title_words(s):
    if not s:
        return set()
    cleaned = re.sub(r"[^\w\s]", " ", s.lower())
    return {w for w in cleaned.split() if len(w) > 2 and w not in STOPWORDS}


def crossref_lookup(author_last, pub_title, pub_year):
    """Query CrossRef structured. Returns (doi, reason)."""
    if not author_last or not pub_title or not pub_year:
        return None, "missing-input"

    title_words_query = " ".join(normalize_title_words(pub_title))[:200]
    if not title_words_query:
        return None, "empty-title-words"

    params = {
        "query.author": author_last,
        "query.title": title_words_query,
        "rows": "5",
        "select": "DOI,title,author,published-print,published-online,issued,type",
    }
    yr_lo = int(pub_year) - MAX_YEAR_DELTA
    yr_hi = int(pub_year) + MAX_YEAR_DELTA
    params["filter"] = f"from-pub-date:{yr_lo},until-pub-date:{yr_hi}-12"

    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    try:
        data = fetch_json(url, timeout=15)
    except Exception as e:
        return None, f"crossref-error"

    items = data.get("message", {}).get("items", []) or []
    if not items:
        return None, "no-results"

    orig_words = normalize_title_words(pub_title)
    if not orig_words:
        return None, "empty-title-words"

    # Short title handling: if the source title has fewer than the minimum overlap
    # words, require 100% overlap with the CrossRef title instead of the floor count.
    # This permits perfect matches like "Dynamic touch" (2 substantive words).
    short_title = len(orig_words) < MIN_TITLE_OVERLAP_WORDS

    candidates = []
    for item in items:
        doi = item.get("DOI", "")
        if not doi:
            continue

        cr_authors = item.get("author", []) or []
        cr_surnames = [
            (a.get("family") or "").lower()
            for a in cr_authors[:3]
            if isinstance(a, dict)
        ]
        if not any(author_last.lower() == s for s in cr_surnames):
            continue

        cr_title = (item.get("title") or [""])[0]
        cr_words = normalize_title_words(cr_title)
        if not cr_words:
            continue
        overlap = orig_words & cr_words
        ratio = len(overlap) / min(len(orig_words), len(cr_words))

        if short_title:
            # Require all source title words present in CrossRef result.
            if overlap != orig_words:
                continue
        else:
            if len(overlap) < MIN_TITLE_OVERLAP_WORDS or ratio < MIN_TITLE_OVERLAP_RATIO:
                continue

        date_obj = (
            item.get("published-print")
            or item.get("published-online")
            or item.get("issued")
        )
        cr_year = None
        if date_obj:
            try:
                cr_year = (date_obj.get("date-parts") or [[None]])[0][0]
            except (AttributeError, IndexError, TypeError):
                pass
        if cr_year is not None:
            try:
                if abs(int(cr_year) - int(pub_year)) > MAX_YEAR_DELTA:
                    continue
            except (ValueError, TypeError):
                pass

        candidates.append({
            "doi": doi, "title": cr_title, "ratio": ratio,
            "overlap": len(overlap), "year": cr_year,
        })

    if not candidates:
        return None, "no-acceptable-match"

    candidates.sort(key=lambda c: (-c["ratio"], -c["overlap"]))
    if len(candidates) >= 2:
        top, runner = candidates[0], candidates[1]
        same_doi = canonical_doi(top["doi"]) == canonical_doi(runner["doi"])
        if not same_doi and (top["ratio"] - runner["ratio"]) < 0.10:
            return None, "ambiguous"

    return candidates[0]["doi"], "matched"


def main():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: DB not found at {DB_PATH}")
        return 1

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cols = [r[1] for r in conn.execute(f"PRAGMA table_info({TABLE})")]
    required = {"first_author_last", "pub_title", "pub_year",
                "doi_resolution_outcome", "source_type", "is_corporate_primary"}
    missing = required - set(cols)
    if missing:
        print(f"ERROR: evidence_sources is not v2. Missing: {missing}")
        return 1

    now_iso = time.strftime("%Y-%m-%d %H:%M", time.gmtime())
    cutoff_date = time.strftime(
        "%Y-%m-%d",
        time.gmtime(time.time() - SKIP_NO_MATCH_DAYS * 86400),
    )

    # Phase 1: PMID -> DOI
    pmid_rows = conn.execute(f"""
        SELECT ref_id, pmid FROM {TABLE}
        WHERE (doi IS NULL OR doi = '')
        AND pmid IS NOT NULL AND pmid != ''
        AND (doi_resolution_outcome IS NULL
             OR (doi_resolution_outcome = 'NO-MATCH' AND updated_at < ?))
    """, (cutoff_date,)).fetchall()

    print(f"Phase 1 (PMID -> DOI via NCBI): {len(pmid_rows)} candidates")
    p1_ok = p1_no = p1_transient = 0

    for r in pmid_rows:
        doi, status = ncbi_pmid_to_doi(r["pmid"])
        if status == "resolved" and doi:
            conn.execute(
                f"UPDATE {TABLE} SET doi=?, doi_resolution_outcome='RESOLVED', "
                "updated_at=?, updated_by_session='resolve-dois-action' "
                "WHERE ref_id=?",
                (doi, now_iso, r["ref_id"])
            )
            p1_ok += 1
            print(f"  PMID->DOI: {r['ref_id']} (PMID:{r['pmid']}) -> {doi}")
        elif status == "no-doi":
            # NCBI confirmed no DOI exists for this PMID — mark NO-MATCH.
            conn.execute(
                f"UPDATE {TABLE} SET doi_resolution_outcome='NO-MATCH', "
                "updated_at=?, updated_by_session='resolve-dois-action' "
                "WHERE ref_id=?",
                (now_iso, r["ref_id"])
            )
            p1_no += 1
        else:
            # Transient error (403, timeout, etc.) — leave row alone so it
            # retries next run instead of being skipped for 30 days.
            p1_transient += 1
        time.sleep(RATE_LIMIT)

    conn.commit()
    print(f"Phase 1 done: {p1_ok} resolved, {p1_no} no-match, {p1_transient} transient (will retry)\n")

    # Phase 2: CrossRef structured query
    placeholders = ",".join(["?"] * len(ELIGIBLE_TYPES))
    cr_rows = conn.execute(f"""
        SELECT ref_id, first_author_last, first_author_first, pub_title, pub_year, source_type
        FROM {TABLE}
        WHERE (doi IS NULL OR doi = '')
        AND source_type IN ({placeholders})
        AND is_corporate_primary = 0
        AND first_author_last IS NOT NULL AND first_author_last != ''
        AND pub_title IS NOT NULL AND length(pub_title) > 15
        AND pub_year IS NOT NULL
        AND (doi_resolution_outcome IS NULL
             OR (doi_resolution_outcome = 'NO-MATCH' AND updated_at < ?))
        ORDER BY pub_year DESC, ref_id
        LIMIT ?
    """, (*ELIGIBLE_TYPES, cutoff_date, MAX_RESOLVE)).fetchall()

    print(f"Phase 2 (CrossRef structured): {len(cr_rows)} candidates")
    p2_ok = p2_no = 0
    reasons = {}

    for r in cr_rows:
        doi, reason = crossref_lookup(
            r["first_author_last"], r["pub_title"], r["pub_year"]
        )
        reasons[reason] = reasons.get(reason, 0) + 1

        if doi:
            conn.execute(
                f"UPDATE {TABLE} SET doi=?, doi_resolution_outcome='RESOLVED', "
                "updated_at=?, updated_by_session='resolve-dois-action' "
                "WHERE ref_id=?",
                (doi, now_iso, r["ref_id"])
            )
            p2_ok += 1
            print(f"  RESOLVED: {r['ref_id']} {r['first_author_last']} "
                  f"({r['pub_year']}) -> {doi}")
        else:
            conn.execute(
                f"UPDATE {TABLE} SET doi_resolution_outcome='NO-MATCH', "
                "updated_at=?, updated_by_session='resolve-dois-action' "
                "WHERE ref_id=?",
                (now_iso, r["ref_id"])
            )
            p2_no += 1
        time.sleep(RATE_LIMIT)

    conn.commit()
    print(f"\nPhase 2 done: {p2_ok} resolved, {p2_no} no-match")
    print("Phase 2 no-match reasons:")
    for reason, c in sorted(reasons.items(), key=lambda x: -x[1]):
        print(f"  {reason}: {c}")

    # Summary
    total = conn.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]
    with_doi = conn.execute(
        f"SELECT COUNT(*) FROM {TABLE} WHERE doi IS NOT NULL AND doi != ''"
    ).fetchone()[0]
    no_match = conn.execute(
        f"SELECT COUNT(*) FROM {TABLE} WHERE doi_resolution_outcome='NO-MATCH'"
    ).fetchone()[0]
    reverted = conn.execute(
        f"SELECT COUNT(*) FROM {TABLE} WHERE doi_resolution_outcome='REVERTED'"
    ).fetchone()[0]

    print(f"\n{'=' * 56}")
    print(f"  Total sources:               {total}")
    print(f"  With DOI:                    {with_doi} ({100*with_doi//total}%)")
    print(f"  NO-MATCH (retry in {SKIP_NO_MATCH_DAYS}d):    {no_match}")
    print(f"  REVERTED (never retry):      {reverted}")
    print(f"  This run resolved:           {p1_ok + p2_ok}")
    print(f"{'=' * 56}")

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
