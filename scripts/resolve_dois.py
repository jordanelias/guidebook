#!/usr/bin/env python3
"""Batch DOI resolution via CrossRef API for evidence_sources table."""

import sqlite3
import json
import urllib.request
import urllib.parse
import time
import sys
import os
import re

DB_PATH = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")
SESSION = "github-action-doi-resolution"
RATE_LIMIT = 0.5  # seconds between requests
MAX_RESOLVE = int(os.environ.get("MAX_RESOLVE", "100"))

def query_crossref(author: str, title: str, year: str) -> str | None:
    """Query CrossRef for a DOI match."""
    # Build query from first author surname + title keywords
    first_author = author.split(",")[0].split(" et al")[0].strip()
    title_clean = re.sub(r"[^\w\s]", " ", title[:80])
    query = f"{first_author} {title_clean}"
    
    url = (
        f"https://api.crossref.org/works?"
        f"query={urllib.parse.quote(query)}&rows=3"
        f"&select=DOI,title,author,published-print,published-online"
    )
    
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "guidebook-project/1.0 (mailto:jordan@guidebook.dev)"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"  ERROR: {e}")
        return None
    
    items = data.get("message", {}).get("items", [])
    if not items:
        return None
    
    # Try to match by title similarity
    orig_words = set(re.sub(r"[^\w\s]", "", title.lower()).split())
    
    for item in items[:3]:
        doi = item.get("DOI", "")
        cr_titles = item.get("title", [])
        cr_title = cr_titles[0] if cr_titles else ""
        cr_words = set(re.sub(r"[^\w\s]", "", cr_title.lower()).split())
        
        # Calculate overlap
        if not orig_words or not cr_words:
            continue
        overlap = len(orig_words & cr_words)
        overlap_ratio = overlap / min(len(orig_words), len(cr_words))
        
        # Check year match if available
        year_match = True
        pub = item.get("published-print") or item.get("published-online")
        if pub and year:
            cr_year = str(pub.get("date-parts", [[None]])[0][0])
            year_match = cr_year == str(year) or abs(int(cr_year or 0) - int(year or 0)) <= 1
        
        if overlap >= 3 and overlap_ratio >= 0.3 and year_match and doi:
            return doi
    
    return None


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Get candidates
    rows = conn.execute("""
        SELECT ref_id, authors, year, title 
        FROM evidence_sources 
        WHERE metadata_quality = 'AUTHOR-TITLE-ONLY' 
        AND doi IS NULL
        AND authors IS NOT NULL AND title IS NOT NULL
        AND title NOT LIKE '%Unverified%'
        AND (authors LIKE '%, %' OR authors LIKE '%et al%')
        ORDER BY CAST(year AS INTEGER) DESC
        LIMIT ?
    """, (MAX_RESOLVE,)).fetchall()
    
    print(f"Candidates: {len(rows)}")
    
    resolved = 0
    skipped = 0
    errors = 0
    ts = time.strftime("%Y-%m-%d %H:%M", time.gmtime())
    
    for r in rows:
        ref_id = r["ref_id"]
        doi = query_crossref(r["authors"], r["title"], r["year"])
        
        if doi:
            conn.execute(
                """UPDATE evidence_sources 
                SET doi = ?, metadata_quality = 'COMPLETE',
                    updated_at = ?, updated_by_session = ?
                WHERE ref_id = ?""",
                (doi, ts, SESSION, ref_id)
            )
            resolved += 1
            print(f"  RESOLVED: {ref_id} → {doi}")
        else:
            skipped += 1
            if skipped % 10 == 0:
                print(f"  ... {skipped} unresolved so far")
        
        time.sleep(RATE_LIMIT)
    
    conn.commit()
    
    # Summary
    complete = conn.execute(
        "SELECT COUNT(*) FROM evidence_sources WHERE metadata_quality = 'COMPLETE'"
    ).fetchone()[0]
    total = conn.execute("SELECT COUNT(*) FROM evidence_sources").fetchone()[0]
    
    print(f"\n{'='*50}")
    print(f"Resolved: {resolved}")
    print(f"Unresolved: {skipped}")
    print(f"COMPLETE total: {complete}/{total}")
    print(f"{'='*50}")
    
    conn.close()
    return 0 if resolved > 0 or skipped == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
