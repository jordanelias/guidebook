#!/usr/bin/env python3
"""Backfill verification_status for sources that already have RESOLVED DOIs.

The resolve_dois.py pipeline sets verification_status=VERIFIED only when it
*discovers* a DOI. Sources that arrived in the DB with DOIs already set
(doi_resolution_outcome='RESOLVED') but no verification_status were never
run through explicit DOI confirmation.

This script:
  1. Selects all sources: doi_resolution_outcome='RESOLVED' AND
     verification_status IS NULL
  2. For each: calls CrossRef /works/<doi> to confirm the DOI is live
     and optionally compares title similarity (pub_title must be >10 chars)
  3. On success: sets verification_status='VERIFIED', verified_by_tool='crossref-doi-backfill'
     and runs metadata enrichment (fills NULL fields from CrossRef response)
  4. On hard 404/410: sets verification_status='UNVERIFIED-1',
     verification_note='DOI confirmed RESOLVED in prior run but CrossRef
     returned 404 at backfill; may be preprint/grey DOI'
  5. On transient (timeout/5xx/429): skips for retry (no write)

Skips REVERTED DOIs unconditionally (already reviewed by a human).

Env:
  GUIDEBOOK_DB_PATH   path to SQLite (default: /tmp/guidebook.db)
  RATE_LIMIT          seconds between requests (default: 1.0)
  SESSION             session label for audit trail
"""

import os
import re
import sqlite3
import time
import urllib.error
import urllib.parse
import urllib.request
import json

DB_PATH  = os.environ.get("GUIDEBOOK_DB_PATH", "/tmp/guidebook.db")
RATE_LIMIT = float(os.environ.get("RATE_LIMIT", "1.0"))
SESSION    = os.environ.get("SESSION", "verify-resolved-dois-backfill")
USER_AGENT = "guidebook-project/2.0 (mailto:jordan@guidebook.dev)"
TABLE      = "evidence_sources"

STOPWORDS = {
    "a","an","the","of","in","on","at","to","for","and","or","with",
    "by","from","as","is","was","are","were","be","been","has","have",
    "had","do","does","did","that","this","these","those","its","it",
    "their","our","but","not","no",
}

def _title_jaccard(a, b):
    if not a or not b:
        return 0.0
    tok = lambda s: {w for w in re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()
                     if w not in STOPWORDS and len(w) > 2}
    A, B = tok(a), tok(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)

def crossref_doi_lookup(doi):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='/')}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("message"), "ok"
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            return None, "not_found"
        if e.code in (429, 503):
            return None, "transient"
        return None, f"http_{e.code}"
    except Exception:
        return None, "transient"

def enrich_from_crossref(conn, ref_id, item, ts):
    """Fill NULL metadata fields from CrossRef item (never overwrites)."""
    if not item:
        return
    def _date_part(it, idx):
        for key in ("published-print", "published-online", "issued"):
            dp = (it.get(key) or {}).get("date-parts")
            if dp:
                try:
                    v = dp[0][idx]
                    if v is not None:
                        return int(v)
                except (IndexError, TypeError, ValueError):
                    pass
        return None

    cr_year  = _date_part(item, 0)
    cr_month = _date_part(item, 1)
    cr_j     = ((item.get("container-title") or [""])[0]) or None
    cr_vol   = item.get("volume") or None
    cr_iss   = item.get("issue") or None
    cr_pg    = item.get("page") or item.get("article-number") or None
    cr_pub   = item.get("publisher") or None
    cr_issn  = ((item.get("ISSN") or [""])[0]) or None
    cr_lang  = item.get("language") or None
    cr_cites = item.get("is-referenced-by-count")
    try:
        cr_cites = int(cr_cites) if cr_cites is not None else None
    except (ValueError, TypeError):
        cr_cites = None

    row = conn.execute(
        f"SELECT pub_year, pub_month, journal_abbrev, volume, issue, pages, "
        f"publisher, issn, language, citation_count, metadata_quality, "
        f"first_author_last, is_corporate_primary, author_count_is_complete "
        f"FROM {TABLE} WHERE ref_id=?", (ref_id,)
    ).fetchone()
    if not row:
        return

    sets, params = [], []
    def _fill(col, cur, new_val):
        if new_val is None:
            return
        if cur is None or (isinstance(cur, str) and not cur.strip()):
            sets.append(f"{col} = ?")
            params.append(new_val)

    _fill("pub_year",      row[0],  cr_year)
    _fill("pub_month",     row[1],  cr_month)
    _fill("journal_abbrev",row[2],  cr_j)
    _fill("volume",        row[3],  cr_vol)
    _fill("issue",         row[4],  cr_iss)
    _fill("pages",         row[5],  cr_pg)
    _fill("publisher",     row[6],  cr_pub)
    _fill("issn",          row[7],  cr_issn)
    _fill("language",      row[8],  cr_lang)
    _fill("citation_count",row[9],  cr_cites)

    if sets:
        conn.execute(
            f"UPDATE {TABLE} SET {', '.join(sets)}, updated_at=?, updated_by_session=? "
            f"WHERE ref_id=?",
            (*params, ts, SESSION, ref_id)
        )

    # Promote metadata_quality to COMPLETE if key fields now all present
    if row[10] != "COMPLETE":
        r2 = conn.execute(
            f"SELECT first_author_last, pub_year, pub_title, doi, journal_abbrev, volume, pages "
            f"FROM {TABLE} WHERE ref_id=?", (ref_id,)
        ).fetchone()
        if r2 and all(r2):
            conn.execute(
                f"UPDATE {TABLE} SET metadata_quality='COMPLETE', updated_at=?, updated_by_session=? "
                f"WHERE ref_id=?", (ts, SESSION, ref_id)
            )

def main():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: DB not found at {DB_PATH}"); return 1

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    candidates = conn.execute(f"""
        SELECT ref_id, doi, pub_title, metadata_quality, source_type, tier
        FROM {TABLE}
        WHERE doi IS NOT NULL AND doi != ''
          AND doi_resolution_outcome = 'RESOLVED'
          AND (verification_status IS NULL OR verification_status = '')
        ORDER BY tier, ref_id
    """).fetchall()

    print(f"Candidates: {len(candidates)} (RESOLVED DOI, verification_status NULL)")
    ts = time.strftime("%Y-%m-%d %H:%M", time.gmtime())

    verified = not_found = transient = skipped = newly_complete = 0

    for r in candidates:
        ref_id  = r["ref_id"]
        doi     = r["doi"]
        pub_title = r["pub_title"] or ""
        mq      = r["metadata_quality"]

        item, status = crossref_doi_lookup(doi)

        if status == "ok" and item:
            # Optionally check title similarity if we have a substantial title
            cr_title = (item.get("title") or [""])[0] or ""
            if len(pub_title) > 10 and len(cr_title) > 10:
                sim = _title_jaccard(pub_title, cr_title)
                note = f"CrossRef DOI backfill: Jaccard={sim:.2f}"
                if sim < 0.25:
                    # Low similarity — might be wrong DOI; mark UNVERIFIED-1
                    conn.execute(f"""
                        UPDATE {TABLE} SET
                            verification_status = 'UNVERIFIED-1',
                            verified_by_tool = 'crossref-doi-backfill',
                            last_verified_at = ?,
                            verification_attempt_count = COALESCE(verification_attempt_count,0)+1,
                            verification_note = ?,
                            updated_at = ?,
                            updated_by_session = ?
                        WHERE ref_id = ?
                    """, (ts, f"Low title similarity {sim:.2f} — backfill flagged for review", ts, SESSION, ref_id))
                    conn.commit()
                    print(f"  UNVERIFIED-1 (low sim {sim:.2f}): {ref_id} | {doi}")
                    print(f"    DB title:  {pub_title[:60]}")
                    print(f"    CR title:  {cr_title[:60]}")
                    skipped += 1
                    time.sleep(RATE_LIMIT)
                    continue
            else:
                note = "CrossRef DOI backfill: DOI live (title too short for Jaccard check)"

            pre_mq = mq
            conn.execute(f"""
                UPDATE {TABLE} SET
                    verification_status = 'VERIFIED',
                    verified_by_tool = 'crossref-doi-backfill',
                    last_verified_at = ?,
                    verification_attempt_count = COALESCE(verification_attempt_count,0)+1,
                    verification_note = ?,
                    updated_at = ?,
                    updated_by_session = ?
                WHERE ref_id = ?
            """, (ts, note, ts, SESSION, ref_id))
            enrich_from_crossref(conn, ref_id, item, ts)
            conn.commit()

            post_mq = conn.execute(f"SELECT metadata_quality FROM {TABLE} WHERE ref_id=?", (ref_id,)).fetchone()[0]
            if pre_mq != "COMPLETE" and post_mq == "COMPLETE":
                newly_complete += 1
                print(f"  VERIFIED (+COMPLETE): {ref_id} | t{r['tier']} | {doi}")
            else:
                print(f"  VERIFIED: {ref_id} | t{r['tier']} | mq={pre_mq} | {doi}")
            verified += 1

        elif status == "not_found":
            conn.execute(f"""
                UPDATE {TABLE} SET
                    verification_status = 'UNVERIFIED-1',
                    verified_by_tool = 'crossref-doi-backfill',
                    last_verified_at = ?,
                    verification_attempt_count = COALESCE(verification_attempt_count,0)+1,
                    verification_note = 'RESOLVED in prior run but CrossRef returned 404 at backfill (preprint DOI or grey-lit DOI)',
                    updated_at = ?,
                    updated_by_session = ?
                WHERE ref_id = ?
            """, (ts, ts, SESSION, ref_id))
            conn.commit()
            print(f"  UNVERIFIED-1 (404): {ref_id} | {doi}")
            not_found += 1

        else:
            print(f"  SKIP (transient/{status}): {ref_id} | {doi}")
            transient += 1

        time.sleep(RATE_LIMIT)

    print()
    print("=== SUMMARY ===")
    print(f"  VERIFIED:         {verified}  (of which {newly_complete} newly upgraded to COMPLETE)")
    print(f"  UNVERIFIED-1:     {not_found + skipped}  ({not_found} 404, {skipped} low-sim)")
    print(f"  Transient/skip:   {transient}")
    print(f"  Total candidates: {len(candidates)}")

    # Final state
    v_after = conn.execute(f"SELECT COUNT(*) FROM {TABLE} WHERE verification_status='VERIFIED'").fetchone()[0]
    c_after = conn.execute(f"SELECT COUNT(*) FROM {TABLE} WHERE metadata_quality='COMPLETE'").fetchone()[0]
    print()
    print(f"  verification_status VERIFIED now: {v_after}")
    print(f"  metadata_quality COMPLETE now:    {c_after}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
