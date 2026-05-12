#!/usr/bin/env python3
"""DOI resolution and source verification against evidence_sources v2 schema.

Per verification-pipeline-proposal-2026-05-12-v2.md V1.

Pipeline phases (run in order, each writes to evidence_sources via write_verification):

  Phase 0  PMC extractor — scan pub_title for embedded PMC IDs, write to pmcid column
           (no network; pure regex pass)
  Phase 1a PMID -> DOI via NCBI ID Converter
  Phase 1b PMCID -> DOI via NCBI ID Converter (covers rows populated in Phase 0)
  Phase 2a CrossRef structured query (person-authored academic)
  Phase 2b CrossRef bibliographic query (corporate-authored academic)
  Phase 3  CrossRef type:standard filter (ISO/EN/BSI standards)

Acceptance for Phase 2a/2b (academic):
  - Author surname (or corporate token) in CrossRef result's first 3 authors / publisher
  - Title-word Jaccard overlap >= 0.55 after stopword removal (or 100% for short titles)
  - Year matches within +/- 1
  - Only one plausible candidate (ambiguity = reject)

Acceptance for Phase 3 (standards):
  - Publisher contains 'BSI', 'British Standards', 'ISO', or 'CEN'
  - Title contains keywords from the source's standard number AND pub_title

Skip behavior (applies to all phases):
  - doi_resolution_outcome = 'REVERTED'  -> permanently skipped
  - doi_resolution_outcome = 'NO-MATCH' within SKIP_NO_MATCH_DAYS -> skipped
  - Already has doi -> skipped

Writes (all phases use central write_verification function):
  - verification_status (VERIFIED / NO-MATCH; not set on transient)
  - verified_by_tool (per-phase identifier)
  - last_verified_at (ISO timestamp)
  - verification_attempt_count (increments)
  - doi (only when found, never clobbers existing)
  - pmcid (only when found, never clobbers existing)
  - verification_note (only when supplied)
  - doi_resolution_outcome (RESOLVED / NO-MATCH)
  - updated_at, updated_by_session

Env vars:
  GUIDEBOOK_DB_PATH   path to SQLite (default: data/guidebook.db)
  MAX_RESOLVE         max candidates per CrossRef phase (default: 500)
  SKIP_NO_MATCH_DAYS  days before retrying a NO-MATCH (default: 30)
  RATE_LIMIT          seconds between API calls (default: 5.0 — conservative)
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
RATE_LIMIT = float(os.environ.get("RATE_LIMIT", "5.0"))
USER_AGENT = "guidebook-project/2.0 (mailto:jordan@guidebook.dev)"
TABLE = "evidence_sources"
SESSION = "resolve-dois-action"

MIN_TITLE_OVERLAP_RATIO = 0.55
MIN_TITLE_OVERLAP_WORDS = 4
MAX_YEAR_DELTA = 1

ELIGIBLE_TYPES = (
    "journal_article", "book", "book_chapter", "thesis",
    "conference_paper", "report", "case_study", "primary_research",
)

# Publisher tokens that identify a CrossRef "type:standard" result as an
# ISO/EN/BSI standard we accept as verification.
STANDARD_PUBLISHER_TOKENS = ("BSI", "British Standards", "ISO", "CEN", "DIN")

# Standard-number prefixes that route to Phase 3 (CrossRef type:standard).
# CrossRef indexes these via BSI's DOI prefix 10.3403/.
CROSSREF_STD_PREFIXES = ("ISO ", "IEC ", "EN ", "BS ", "BS EN ", "BS ISO ",
                          "ISO/IEC ", "ISO/TC ", "PAS ")

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "in", "on", "at", "to", "for",
    "with", "by", "from", "as", "is", "are", "was", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "this", "that", "these", "those",
    "it", "its", "their", "them", "they", "we", "our", "us",
}


# ─── HTTP helper ────────────────────────────────────────────────────────────

def fetch_json(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


# ─── Central write function (per proposal v2 §5; tested 22/22) ──────────────

def write_verification(conn, ref_id, tool, status=None, doi=None, pmcid=None,
                       note=None, doi_outcome=None, ts=None):
    """Atomic verification-state write.

    Only fields explicitly supplied are touched. Never clobbers existing doi or
    pmcid with NULL. Always increments verification_attempt_count. Always sets
    verified_by_tool, last_verified_at, updated_at, updated_by_session.
    """
    ts = ts or time.strftime("%Y-%m-%d %H:%M", time.gmtime())

    sets = ["verified_by_tool = ?", "last_verified_at = ?",
            "verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1",
            "updated_at = ?", "updated_by_session = ?"]
    params = [tool, ts, ts, SESSION]

    if status is not None:
        sets.append("verification_status = ?")
        params.append(status)
    if note is not None:
        sets.append("verification_note = ?")
        params.append(note)
    if doi is not None:
        sets.append("doi = ?")
        params.append(doi)
    if pmcid is not None:
        sets.append("pmcid = ?")
        params.append(pmcid)
    if doi_outcome is not None:
        sets.append("doi_resolution_outcome = ?")
        params.append(doi_outcome)

    params.append(ref_id)
    sql = f"UPDATE {TABLE} SET " + ", ".join(sets) + " WHERE ref_id = ?"
    conn.execute(sql, params)


# ─── NCBI helpers ───────────────────────────────────────────────────────────

def ncbi_id_to_doi(any_id):
    """Convert any NCBI ID (PMID or PMC) to DOI via NCBI ID Converter.

    Accepts both '12345' (PMID) and 'PMC12345' (PMCID).
    Returns (doi, status) where status is 'resolved' | 'no-doi' | 'transient'.
    """
    url = (
        "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
        f"?ids={any_id}&format=json&tool=guidebook&email=jordan@guidebook.dev"
    )
    try:
        data = fetch_json(url, timeout=15)
    except urllib.error.HTTPError as e:
        if e.code == 403 or e.code >= 500 or e.code == 429:
            print(f"    NCBI transient error {e.code} for {any_id}")
            return None, "transient"
        return None, "no-doi"
    except Exception as e:
        print(f"    NCBI transient error for {any_id}: {e}")
        return None, "transient"

    records = data.get("records", []) or []
    if records and records[0].get("doi"):
        return records[0]["doi"], "resolved"
    return None, "no-doi"


# ─── Title / DOI helpers ────────────────────────────────────────────────────

def canonical_doi(doi):
    """Normalize a DOI for equality comparison (collapse '//', lowercase)."""
    if not doi:
        return ""
    return re.sub(r"/{2,}", "/", doi.strip().lower())


def normalize_title_words(s):
    if not s:
        return set()
    cleaned = re.sub(r"[^\w\s]", " ", s.lower())
    return {w for w in cleaned.split() if len(w) > 2 and w not in STOPWORDS}


# ─── CrossRef Phase 2a (person-author structured) ───────────────────────────

def crossref_structured(author_last, pub_title, pub_year):
    """CrossRef structured query for person-authored academic items."""
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
    except Exception:
        return None, "crossref-error"

    items = data.get("message", {}).get("items", []) or []
    if not items:
        return None, "no-results"

    return _select_match(items, pub_title, pub_year, author_last=author_last)


# ─── CrossRef Phase 2b (corporate-author bibliographic) ─────────────────────

def crossref_bibliographic(corp_name, pub_title, pub_year):
    """CrossRef bibliographic query for corporate-authored academic items."""
    if not corp_name or not pub_title or not pub_year:
        return None, "missing-input"

    bib_q = f"{corp_name} {' '.join(normalize_title_words(pub_title))}"[:250]
    params = {
        "query.bibliographic": bib_q,
        "rows": "5",
        "select": "DOI,title,author,published-print,published-online,issued,type,publisher",
    }
    yr_lo = int(pub_year) - MAX_YEAR_DELTA
    yr_hi = int(pub_year) + MAX_YEAR_DELTA
    params["filter"] = f"from-pub-date:{yr_lo},until-pub-date:{yr_hi}-12"

    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    try:
        data = fetch_json(url, timeout=15)
    except Exception:
        return None, "crossref-error"

    items = data.get("message", {}).get("items", []) or []
    if not items:
        return None, "no-results"

    return _select_match(items, pub_title, pub_year, corp_name=corp_name)


# ─── CrossRef Phase 3 (standards via type:standard filter) ──────────────────

def crossref_standard(standard_number, pub_title, pub_year):
    """CrossRef type:standard query for ISO/EN/BSI standards.

    Acceptance criteria:
      - Publisher must contain a STANDARD_PUBLISHER_TOKEN
      - Title must overlap with the source's pub_title keywords
      - Standard number tokens (e.g., '23599') should appear in result title
    """
    if not standard_number or not pub_title:
        return None, "missing-input"

    # Extract numeric part of the standard number for matching
    num_match = re.search(r"\d+", standard_number)
    std_num_token = num_match.group(0) if num_match else ""

    # Build query: standard number + title keywords
    title_kw = " ".join(normalize_title_words(pub_title))[:160]
    bib_q = f"{standard_number} {title_kw}"[:250]

    params = {
        "query.bibliographic": bib_q,
        "filter": "type:standard",
        "rows": "5",
        "select": "DOI,title,publisher,issued,type",
    }

    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    try:
        data = fetch_json(url, timeout=15)
    except Exception:
        return None, "crossref-error"

    items = data.get("message", {}).get("items", []) or []
    if not items:
        return None, "no-results"

    candidates = []
    orig_words = normalize_title_words(pub_title)

    for item in items:
        doi = item.get("DOI", "")
        if not doi:
            continue
        if item.get("type") != "standard":
            continue

        publisher = item.get("publisher", "") or ""
        if not any(tok.lower() in publisher.lower() for tok in STANDARD_PUBLISHER_TOKENS):
            continue

        cr_title = (item.get("title") or [""])[0]
        cr_words = normalize_title_words(cr_title)
        if not cr_words:
            continue

        # Title-word overlap with source pub_title
        overlap = orig_words & cr_words
        ratio = len(overlap) / min(len(orig_words), len(cr_words)) if orig_words and cr_words else 0
        if len(overlap) < 2 or ratio < 0.30:
            continue

        # Standard number token (e.g. '23599') should ideally appear in CrossRef title
        # (not strictly required if title overlap is strong, but boosts confidence)
        num_in_title = bool(std_num_token and std_num_token in cr_title)

        candidates.append({
            "doi": doi, "title": cr_title, "publisher": publisher,
            "ratio": ratio, "overlap": len(overlap), "num_match": num_in_title,
        })

    if not candidates:
        return None, "no-acceptable-match"

    # Prefer candidates where the standard number appears in title
    candidates.sort(key=lambda c: (-int(c["num_match"]), -c["ratio"], -c["overlap"]))

    # Ambiguity check
    if len(candidates) >= 2:
        top, runner = candidates[0], candidates[1]
        same = canonical_doi(top["doi"]) == canonical_doi(runner["doi"])
        if (not same and top["num_match"] == runner["num_match"]
                and (top["ratio"] - runner["ratio"]) < 0.15):
            return None, "ambiguous"

    return candidates[0]["doi"], "matched"


# ─── Shared match selector for academic Phase 2a/2b ─────────────────────────

def _select_match(items, pub_title, pub_year, author_last=None, corp_name=None):
    """Apply acceptance criteria and pick at-most-one DOI from candidate items."""
    orig_words = normalize_title_words(pub_title)
    if not orig_words:
        return None, "empty-title-words"

    short_title = len(orig_words) < MIN_TITLE_OVERLAP_WORDS

    candidates = []
    for item in items:
        doi = item.get("DOI", "")
        if not doi:
            continue

        # Person-author check (Phase 2a)
        if author_last:
            cr_authors = item.get("author", []) or []
            cr_surnames = [
                (a.get("family") or "").lower()
                for a in cr_authors[:3]
                if isinstance(a, dict)
            ]
            if not any(author_last.lower() == s for s in cr_surnames):
                continue

        # Corporate-author check (Phase 2b)
        if corp_name:
            cr_authors = item.get("author", []) or []
            publisher = item.get("publisher", "") or ""
            corp_tok = corp_name.lower().split()[0] if corp_name.split() else ""
            org_match = (
                corp_tok and corp_tok in publisher.lower()
            ) or any(
                isinstance(a, dict) and corp_tok in (a.get("name") or "").lower()
                for a in cr_authors[:3]
            )
            if not org_match:
                continue

        # Title overlap
        cr_title = (item.get("title") or [""])[0]
        cr_words = normalize_title_words(cr_title)
        if not cr_words:
            continue
        overlap = orig_words & cr_words
        ratio = len(overlap) / min(len(orig_words), len(cr_words))

        if short_title:
            if overlap != orig_words:
                continue
        else:
            if len(overlap) < MIN_TITLE_OVERLAP_WORDS or ratio < MIN_TITLE_OVERLAP_RATIO:
                continue

        # Year check
        date_obj = (
            item.get("published-print") or item.get("published-online")
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

        candidates.append({"doi": doi, "title": cr_title, "ratio": ratio,
                           "overlap": len(overlap), "year": cr_year})

    if not candidates:
        return None, "no-acceptable-match"

    candidates.sort(key=lambda c: (-c["ratio"], -c["overlap"]))
    if len(candidates) >= 2:
        top, runner = candidates[0], candidates[1]
        same = canonical_doi(top["doi"]) == canonical_doi(runner["doi"])
        if not same and (top["ratio"] - runner["ratio"]) < 0.10:
            return None, "ambiguous"

    return candidates[0]["doi"], "matched"


# ─── Phase 0: PMC ID extractor (no network) ─────────────────────────────────

def phase_0_pmc_extractor(conn, ts):
    """Extract PMC IDs from pub_title field into the pmcid column.

    Pure regex pass — no network calls. Writes pmcid via write_verification with
    no verification_status (since extraction alone isn't verification).
    """
    rows = conn.execute(f"""
        SELECT ref_id, pub_title, pmcid FROM {TABLE}
        WHERE (pmcid IS NULL OR pmcid = '')
        AND pub_title LIKE '%PMC%'
    """).fetchall()

    extracted = 0
    for r in rows:
        m = re.search(r"PMC(\d+)", r["pub_title"] or "")
        if not m:
            continue
        pmcid = f"PMC{m.group(1)}"
        # Direct UPDATE — extraction is not a verification event, just a backfill.
        conn.execute(
            f"UPDATE {TABLE} SET pmcid=?, updated_at=?, updated_by_session=? WHERE ref_id=?",
            (pmcid, ts, SESSION, r["ref_id"])
        )
        print(f"  PMC extract: {r['ref_id']} <- {pmcid}")
        extracted += 1

    conn.commit()
    return extracted


# ─── Main orchestrator ──────────────────────────────────────────────────────

def main():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: DB not found at {DB_PATH}")
        return 1

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Schema sanity check — V1 requires verified_by_tool and friends
    cols = [r[1] for r in conn.execute(f"PRAGMA table_info({TABLE})")]
    required = {"first_author_last", "pub_title", "pub_year",
                "doi_resolution_outcome", "source_type", "is_corporate_primary",
                "pmcid", "verified_by_tool", "last_verified_at",
                "verification_attempt_count"}
    missing = required - set(cols)
    if missing:
        print(f"ERROR: evidence_sources schema is not V1-extended. Missing: {missing}")
        return 1

    now_iso = time.strftime("%Y-%m-%d %H:%M", time.gmtime())
    cutoff = time.strftime("%Y-%m-%d",
                           time.gmtime(time.time() - SKIP_NO_MATCH_DAYS * 86400))

    # Ensure pipeline_runs table exists (idempotent).
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pipeline_runs (
          run_id             TEXT PRIMARY KEY,
          started_at         TEXT NOT NULL,
          completed_at       TEXT,
          phase_0_extracted  INTEGER DEFAULT 0,
          phase_1a_resolved  INTEGER DEFAULT 0,
          phase_1a_no_match  INTEGER DEFAULT 0,
          phase_1a_transient INTEGER DEFAULT 0,
          phase_1b_resolved  INTEGER DEFAULT 0,
          phase_1b_no_match  INTEGER DEFAULT 0,
          phase_1b_transient INTEGER DEFAULT 0,
          phase_2a_resolved  INTEGER DEFAULT 0,
          phase_2a_no_match  INTEGER DEFAULT 0,
          phase_2b_resolved  INTEGER DEFAULT 0,
          phase_2b_no_match  INTEGER DEFAULT 0,
          phase_3_resolved   INTEGER DEFAULT 0,
          phase_3_no_match   INTEGER DEFAULT 0,
          doi_before         INTEGER DEFAULT 0,
          doi_after          INTEGER DEFAULT 0,
          verified_before    INTEGER DEFAULT 0,
          verified_after     INTEGER DEFAULT 0,
          pmcid_before       INTEGER DEFAULT 0,
          pmcid_after        INTEGER DEFAULT 0,
          total_resolved     INTEGER DEFAULT 0,
          run_by_session     TEXT
        )
    """)

    # Snapshot pre-run state.
    def _count(q):
        return conn.execute(q).fetchone()[0]

    doi_before = _count(f"SELECT COUNT(*) FROM {TABLE} WHERE doi IS NOT NULL AND doi != ''")
    verified_before = _count(f"SELECT COUNT(*) FROM {TABLE} WHERE verification_status='VERIFIED'")
    pmcid_before = _count(f"SELECT COUNT(*) FROM {TABLE} WHERE pmcid IS NOT NULL AND pmcid != ''")

    run_id = now_iso
    conn.execute("""
        INSERT OR REPLACE INTO pipeline_runs
          (run_id, started_at, doi_before, verified_before, pmcid_before, run_by_session)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (run_id, now_iso, doi_before, verified_before, pmcid_before, SESSION))
    conn.commit()
    print(f"Run {run_id}: doi_before={doi_before} verified_before={verified_before} "
          f"pmcid_before={pmcid_before} rate_limit={RATE_LIMIT}s\n")

    # ── Phase 0: PMC extractor ──────────────────────────────────────────────
    print("=" * 56)
    print("Phase 0 — PMC ID extractor")
    print("=" * 56)
    extracted = phase_0_pmc_extractor(conn, now_iso)
    print(f"Phase 0 done: {extracted} PMC IDs extracted to pmcid column\n")

    # ── Phase 1a: PMID -> DOI ──────────────────────────────────────────────
    print("=" * 56)
    print("Phase 1a — PMID -> DOI via NCBI")
    print("=" * 56)
    pmid_rows = conn.execute(f"""
        SELECT ref_id, pmid FROM {TABLE}
        WHERE (doi IS NULL OR doi = '')
        AND pmid IS NOT NULL AND pmid != ''
        AND (doi_resolution_outcome IS NULL
             OR (doi_resolution_outcome = 'NO-MATCH' AND updated_at < ?))
    """, (cutoff,)).fetchall()
    print(f"  Candidates: {len(pmid_rows)}")
    p1a_ok = p1a_no = p1a_t = 0
    for r in pmid_rows:
        doi, status = ncbi_id_to_doi(r["pmid"])
        if status == "resolved" and doi:
            write_verification(conn, r["ref_id"], "ncbi-pmid-converter", "VERIFIED",
                               doi=doi, doi_outcome="RESOLVED",
                               note=f"NCBI PMID:{r['pmid']} -> {doi}")
            p1a_ok += 1
            print(f"  PMID->DOI: {r['ref_id']} (PMID:{r['pmid']}) -> {doi}")
        elif status == "no-doi":
            # NO-MATCH only updates doi_resolution_outcome; verification_status
            # may have been independently set by another channel, do not downgrade.
            write_verification(conn, r["ref_id"], "ncbi-pmid-converter",
                               status=None, doi_outcome="NO-MATCH",
                               note=f"NCBI: no DOI for PMID:{r['pmid']}")
            p1a_no += 1
        else:
            p1a_t += 1
        time.sleep(RATE_LIMIT)
    conn.commit()
    print(f"Phase 1a done: {p1a_ok} resolved, {p1a_no} no-match, {p1a_t} transient\n")

    # ── Phase 1b: PMCID -> DOI ─────────────────────────────────────────────
    print("=" * 56)
    print("Phase 1b — PMCID -> DOI via NCBI")
    print("=" * 56)
    pmcid_rows = conn.execute(f"""
        SELECT ref_id, pmcid FROM {TABLE}
        WHERE (doi IS NULL OR doi = '')
        AND pmcid IS NOT NULL AND pmcid != ''
        AND (doi_resolution_outcome IS NULL
             OR (doi_resolution_outcome = 'NO-MATCH' AND updated_at < ?))
    """, (cutoff,)).fetchall()
    print(f"  Candidates: {len(pmcid_rows)}")
    p1b_ok = p1b_no = p1b_t = 0
    for r in pmcid_rows:
        doi, status = ncbi_id_to_doi(r["pmcid"])
        if status == "resolved" and doi:
            write_verification(conn, r["ref_id"], "ncbi-pmcid-converter", "VERIFIED",
                               doi=doi, doi_outcome="RESOLVED",
                               note=f"NCBI {r['pmcid']} -> {doi}")
            p1b_ok += 1
            print(f"  PMCID->DOI: {r['ref_id']} ({r['pmcid']}) -> {doi}")
        elif status == "no-doi":
            write_verification(conn, r["ref_id"], "ncbi-pmcid-converter",
                               status=None, doi_outcome="NO-MATCH",
                               note=f"NCBI: no DOI for {r['pmcid']}")
            p1b_no += 1
        else:
            p1b_t += 1
        time.sleep(RATE_LIMIT)
    conn.commit()
    print(f"Phase 1b done: {p1b_ok} resolved, {p1b_no} no-match, {p1b_t} transient\n")

    # ── Phase 2a: CrossRef structured (person-author academic) ─────────────
    print("=" * 56)
    print("Phase 2a — CrossRef structured (person-author academic)")
    print("=" * 56)
    placeholders = ",".join(["?"] * len(ELIGIBLE_TYPES))
    p2a_rows = conn.execute(f"""
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
    """, (*ELIGIBLE_TYPES, cutoff, MAX_RESOLVE)).fetchall()
    print(f"  Candidates: {len(p2a_rows)}")
    p2a_ok = p2a_no = 0
    p2a_reasons = {}
    for r in p2a_rows:
        doi, reason = crossref_structured(r["first_author_last"], r["pub_title"], r["pub_year"])
        p2a_reasons[reason] = p2a_reasons.get(reason, 0) + 1
        if doi:
            write_verification(conn, r["ref_id"], "crossref-structured", "VERIFIED",
                               doi=doi, doi_outcome="RESOLVED",
                               note=f"CrossRef structured: {r['first_author_last']} ({r['pub_year']})")
            p2a_ok += 1
            print(f"  RESOLVED: {r['ref_id']} {r['first_author_last']} ({r['pub_year']}) -> {doi}")
        else:
            write_verification(conn, r["ref_id"], "crossref-structured",
                               status=None, doi_outcome="NO-MATCH",
                               note=f"CrossRef structured: {reason}")
            p2a_no += 1
        time.sleep(RATE_LIMIT)
    conn.commit()
    print(f"Phase 2a done: {p2a_ok} resolved, {p2a_no} no-match")
    for k, v in sorted(p2a_reasons.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")
    print()

    # ── Phase 2b: CrossRef bibliographic (corporate-author academic) ───────
    print("=" * 56)
    print("Phase 2b — CrossRef bibliographic (corporate-author academic)")
    print("=" * 56)
    p2b_rows = conn.execute(f"""
        SELECT e.ref_id, e.pub_title, e.pub_year, e.source_type,
               (SELECT a.corporate_name FROM evidence_source_authors a
                WHERE a.ref_id = e.ref_id AND a.position = 1) AS corp
        FROM {TABLE} e
        WHERE (e.doi IS NULL OR e.doi = '')
        AND e.source_type IN ('journal_article','book','book_chapter','conference_paper')
        AND e.is_corporate_primary = 1
        AND e.pub_title IS NOT NULL AND length(e.pub_title) > 15
        AND e.pub_year IS NOT NULL
        AND (e.doi_resolution_outcome IS NULL
             OR (e.doi_resolution_outcome = 'NO-MATCH' AND e.updated_at < ?))
        LIMIT ?
    """, (cutoff, MAX_RESOLVE)).fetchall()
    print(f"  Candidates: {len(p2b_rows)}")
    p2b_ok = p2b_no = 0
    p2b_reasons = {}
    for r in p2b_rows:
        if not r["corp"]:
            continue
        doi, reason = crossref_bibliographic(r["corp"], r["pub_title"], r["pub_year"])
        p2b_reasons[reason] = p2b_reasons.get(reason, 0) + 1
        if doi:
            write_verification(conn, r["ref_id"], "crossref-bibliographic", "VERIFIED",
                               doi=doi, doi_outcome="RESOLVED",
                               note=f"CrossRef bib: {r['corp']} ({r['pub_year']})")
            p2b_ok += 1
            print(f"  RESOLVED: {r['ref_id']} {r['corp']} ({r['pub_year']}) -> {doi}")
        else:
            write_verification(conn, r["ref_id"], "crossref-bibliographic",
                               status=None, doi_outcome="NO-MATCH",
                               note=f"CrossRef bib: {reason}")
            p2b_no += 1
        time.sleep(RATE_LIMIT)
    conn.commit()
    print(f"Phase 2b done: {p2b_ok} resolved, {p2b_no} no-match")
    for k, v in sorted(p2b_reasons.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")
    print()

    # ── Phase 3: CrossRef type:standard (ISO/EN/BSI) ───────────────────────
    print("=" * 56)
    print("Phase 3 — CrossRef type:standard (ISO/EN/BSI)")
    print("=" * 56)
    p3_rows = conn.execute(f"""
        SELECT ref_id, standard_number, pub_title, pub_year
        FROM {TABLE}
        WHERE (doi IS NULL OR doi = '')
        AND source_type = 'standard'
        AND standard_number IS NOT NULL AND standard_number != ''
        AND pub_title IS NOT NULL AND length(pub_title) > 10
        AND (doi_resolution_outcome IS NULL
             OR (doi_resolution_outcome = 'NO-MATCH' AND updated_at < ?))
        LIMIT ?
    """, (cutoff, MAX_RESOLVE)).fetchall()

    # Filter to standards routable to CrossRef (ISO/EN/BSI/IEC/PAS prefixes)
    routable = [
        r for r in p3_rows
        if any(r["standard_number"].upper().startswith(p) for p in CROSSREF_STD_PREFIXES)
    ]
    print(f"  Candidates: {len(p3_rows)} total, {len(routable)} routable to CrossRef")
    p3_ok = p3_no = 0
    p3_reasons = {}
    for r in routable:
        doi, reason = crossref_standard(r["standard_number"], r["pub_title"], r["pub_year"])
        p3_reasons[reason] = p3_reasons.get(reason, 0) + 1
        if doi:
            write_verification(conn, r["ref_id"], "crossref-standard", "VERIFIED",
                               doi=doi, doi_outcome="RESOLVED",
                               note=f"CrossRef type:standard: {r['standard_number']}")
            p3_ok += 1
            print(f"  RESOLVED: {r['ref_id']} {r['standard_number']} -> {doi}")
        else:
            write_verification(conn, r["ref_id"], "crossref-standard",
                               status=None, doi_outcome="NO-MATCH",
                               note=f"CrossRef type:standard: {reason}")
            p3_no += 1
        time.sleep(RATE_LIMIT)
    conn.commit()
    print(f"Phase 3 done: {p3_ok} resolved, {p3_no} no-match")
    for k, v in sorted(p3_reasons.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")
    print()

    # ── Summary + pipeline_runs write ─────────────────────────────────────
    total = conn.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]
    doi_after = conn.execute(
        f"SELECT COUNT(*) FROM {TABLE} WHERE doi IS NOT NULL AND doi != ''"
    ).fetchone()[0]
    no_match = conn.execute(
        f"SELECT COUNT(*) FROM {TABLE} WHERE doi_resolution_outcome='NO-MATCH'"
    ).fetchone()[0]
    reverted = conn.execute(
        f"SELECT COUNT(*) FROM {TABLE} WHERE doi_resolution_outcome='REVERTED'"
    ).fetchone()[0]
    verified_after = conn.execute(
        f"SELECT COUNT(*) FROM {TABLE} WHERE verification_status='VERIFIED'"
    ).fetchone()[0]
    pmcid_after = conn.execute(
        f"SELECT COUNT(*) FROM {TABLE} WHERE pmcid IS NOT NULL AND pmcid != ''"
    ).fetchone()[0]
    this_run_ok = p1a_ok + p1b_ok + p2a_ok + p2b_ok + p3_ok
    completed_at = time.strftime("%Y-%m-%d %H:%M", time.gmtime())

    # Commit per-phase results to pipeline_runs.
    conn.execute("""
        UPDATE pipeline_runs SET
          completed_at       = ?,
          phase_0_extracted  = ?,
          phase_1a_resolved  = ?, phase_1a_no_match  = ?, phase_1a_transient = ?,
          phase_1b_resolved  = ?, phase_1b_no_match  = ?, phase_1b_transient = ?,
          phase_2a_resolved  = ?, phase_2a_no_match  = ?,
          phase_2b_resolved  = ?, phase_2b_no_match  = ?,
          phase_3_resolved   = ?, phase_3_no_match   = ?,
          doi_after          = ?,
          verified_after     = ?,
          pmcid_after        = ?,
          total_resolved     = ?
        WHERE run_id = ?
    """, (
        completed_at,
        extracted,
        p1a_ok, p1a_no, p1a_t,
        p1b_ok, p1b_no, p1b_t,
        p2a_ok, p2a_no,
        p2b_ok, p2b_no,
        p3_ok, p3_no,
        doi_after,
        verified_after,
        pmcid_after,
        this_run_ok,
        run_id,
    ))
    conn.commit()

    print("=" * 56)
    print(f"  Total sources:               {total}")
    print(f"  With DOI:                    {doi_after} ({100*doi_after//total}%)  delta={doi_after-doi_before:+d}")
    print(f"  verification_status VERIFIED: {verified_after}  delta={verified_after-verified_before:+d}")
    print(f"  PMC IDs extracted this run:  {extracted}")
    print(f"  NO-MATCH (retry in {SKIP_NO_MATCH_DAYS}d):    {no_match}")
    print(f"  REVERTED (never retry):      {reverted}")
    print(f"  This run resolved:           {this_run_ok}")
    print(f"    Phase 1a (PMID):                {p1a_ok}")
    print(f"    Phase 1b (PMCID):               {p1b_ok}")
    print(f"    Phase 2a (CrossRef structured): {p2a_ok}")
    print(f"    Phase 2b (CrossRef bib):        {p2b_ok}")
    print(f"    Phase 3 (CrossRef standard):    {p3_ok}")
    print(f"  Run record:                  pipeline_runs['{run_id}']")
    print("=" * 56)

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
