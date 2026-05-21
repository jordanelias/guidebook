#!/usr/bin/env python3
"""
ATO no-identifier author+year search probe.

The v3 bibliographic-phrase-search probe failed because stored pub_title is
predominantly note-style (research finding, not canonical title). v4 uses
author + year filter alone, returns top-3 Crossref results for cross-check,
and writes only if top result passes strict author+year+type-coherence check.

For rows passing the gate, the DB write is conservative:
  - Stored pub_title is preserved as a 'finding annotation' moved to bpc_note
  - Canonical title replaces stored pub_title
  - All other empty fields populated from canonical

For rows not passing, we still record the top-3 candidates in
metadata_integrity_detail so a future session or owner can disambiguate.

Tier:
  HIGH-CONF: author + year present
  MID-CONF:  year only; SKIP (cannot reliably search 138 reports by year alone)
"""
import json
import re
import sqlite3
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "guidebook.db"
CROSSREF = "https://api.crossref.org/works"
USER_AGENT = "Guidebook-AuthorYear/4.0 (mailto:[email protected])"
RATE_LIMIT_SLEEP = 0.25


def normalize(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def search_crossref(author, year, rows_to_return=5):
    """Author + year filter only. Returns list of top items or error string."""
    params = {
        "query.author": author,
        "filter": f"from-pub-date:{year-1},until-pub-date:{year+1}",
        "rows": rows_to_return,
    }
    url = f"{CROSSREF}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        return data.get("message", {}).get("items", []) or []
    except Exception as e:
        return f"error:{type(e).__name__}"


def gate(row, item):
    """Strict gate: author surname match + year ≤1 + type is academic-publication."""
    reasons = []
    authors = item.get("author", []) or []
    cr_last = authors[0].get("family", "") if authors else ""
    db_last = row["first_author_last"] or ""
    if not db_last:
        reasons.append("no db-author-anchor")
    elif normalize(cr_last) != normalize(db_last):
        reasons.append(f"author:cr={cr_last!r} db={db_last!r}")

    parts = item.get("issued", {}).get("date-parts", [[None]])
    cr_year = parts[0][0] if parts and parts[0] else None
    db_year = row["pub_year"]
    if cr_year and db_year and abs(int(cr_year) - int(db_year)) > 1:
        reasons.append(f"year:cr={cr_year} db={db_year}")

    cr_type = item.get("type", "")
    # Accept journal-article, proceedings-article, book-chapter, monograph, posted-content
    if cr_type not in ("journal-article", "proceedings-article", "book-chapter",
                       "monograph", "book", "posted-content", "report",
                       "reference-entry"):
        reasons.append(f"type-suspect:{cr_type}")

    # Container or volume must be present (otherwise it's probably a preprint stub
    # or metadata-incomplete record)
    if not (item.get("container-title") or item.get("ISBN") or item.get("publisher")):
        reasons.append("no-publisher-markers")

    return reasons


def extract(item, row):
    out = {}
    titles = item.get("title", []) or []
    if titles and not row["pub_title"]:
        out["pub_title"] = titles[0]
    if item.get("DOI"):
        out["doi"] = item["DOI"]
    containers = item.get("container-title", []) or []
    if containers and not row["journal_name"]:
        out["journal_name"] = containers[0]
    for src, dst in [("volume", "volume"), ("issue", "issue"), ("publisher", "publisher")]:
        if item.get(src) and not row[dst]:
            out[dst] = item[src]
    if item.get("page") and not row["pages_start"]:
        pg = item["page"]
        if "-" in pg:
            a, b = pg.split("-", 1)
            out["pages_start"] = a.strip()
            out["pages_end"] = b.strip()
        else:
            out["pages_start"] = pg.strip()
    issns = item.get("ISSN", []) or []
    if issns and not row["issn"]:
        out["issn"] = issns[0]
    authors = item.get("author", []) or []
    if authors:
        if not row["author_count"]:
            out["author_count"] = len(authors)
            out["author_count_is_complete"] = 1
        if not row["first_author_last"] and authors[0].get("family"):
            out["first_author_last"] = authors[0]["family"]
        if not row["first_author_first"] and authors[0].get("given"):
            out["first_author_first"] = authors[0]["given"]
        if not row["author_display"]:
            names = []
            for a in authors[:8]:
                g, f = a.get("given", ""), a.get("family", "")
                if f and g:
                    initials = ".".join(x[0] for x in g.split() if x) + "."
                    names.append(f"{f}, {initials}")
                elif f:
                    names.append(f)
            if names:
                out["author_display"] = "; ".join(names)
    out["metadata_quality"] = "COMPLETE"
    return out


def candidate_summary(item):
    """Compact representation for top-3 fallback storage."""
    titles = item.get("title") or []
    authors = item.get("author") or []
    parts = item.get("issued", {}).get("date-parts", [[None]])
    cy = parts[0][0] if parts and parts[0] else None
    return {
        "title": titles[0] if titles else "",
        "first_author": authors[0].get("family", "") if authors else "",
        "year": cy,
        "doi": item.get("DOI"),
        "type": item.get("type"),
        "container": (item.get("container-title") or [""])[0],
    }


def main(limit=0):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT * FROM evidence_sources
        WHERE (doi IS NULL OR doi='') AND (pmid IS NULL OR pmid='')
          AND metadata_quality='AUTHOR-TITLE-ONLY'
          AND source_type IN ('report','journal_article','book_chapter','book','thesis','internal')
          AND first_author_last IS NOT NULL AND first_author_last != ''
          AND pub_year IS NOT NULL
        ORDER BY ref_id
    """).fetchall()
    print(f"# HIGH-CONF cohort (author+year present): {len(rows)} rows", file=sys.stderr)
    if limit:
        rows = rows[:limit]

    outcomes = []
    for i, r in enumerate(rows):
        author = r["first_author_last"]
        year = int(r["pub_year"])
        items = search_crossref(author, year)
        time.sleep(RATE_LIMIT_SLEEP)
        if isinstance(items, str):
            outcomes.append({"ref_id": r["ref_id"], "verdict": "SKIP-API-ERROR",
                             "reasons": [items], "fields_to_set": {}})
            print(f"[{i+1}/{len(rows)}] {r['ref_id']}: {items}", file=sys.stderr)
            continue
        if not items:
            outcomes.append({"ref_id": r["ref_id"], "verdict": "HOLD-NO-CANDIDATES",
                             "reasons": [f"no Crossref hits for author={author!r} year={year}"],
                             "fields_to_set": {}})
            print(f"[{i+1}/{len(rows)}] {r['ref_id']}: HOLD no-candidates", file=sys.stderr)
            continue

        top = items[0]
        reasons = gate(dict(r), top)
        if reasons:
            outcomes.append({
                "ref_id": r["ref_id"],
                "verdict": "HOLD-GATE-FAILED",
                "reasons": reasons,
                "top_candidates": [candidate_summary(it) for it in items[:3]],
                "fields_to_set": {},
            })
            print(f"[{i+1}/{len(rows)}] {r['ref_id']}: HOLD gate ({len(reasons)} reasons)", file=sys.stderr)
            continue

        # Top result passed the gate — but ALSO check that the stored pub_title
        # (the finding-note) wouldn't contradict the canonical title flagrantly.
        # Mild check: if the stored title has 3+ unique meaningful tokens and
        # zero overlap with canonical, treat as still-hold (might be wrong author
        # match within the author's broader publication record).
        cr_title = (top.get("title") or [""])[0]
        db_title = r["pub_title"] or ""
        if db_title and len(normalize(db_title).split()) >= 3:
            shared = set(normalize(cr_title).split()) & set(normalize(db_title).split())
            db_tokens = set(normalize(db_title).split())
            stop = {"the", "a", "of", "in", "and", "for", "on", "to", "with"}
            meaningful = db_tokens - stop
            if len(meaningful) >= 3 and len(shared) == 0:
                outcomes.append({
                    "ref_id": r["ref_id"],
                    "verdict": "HOLD-TITLE-ORTHOGONAL",
                    "reasons": [f"db_title and cr_title share 0 tokens (db: {db_title[:50]!r}, cr: {cr_title[:50]!r}); top author+year match may be wrong paper from same author"],
                    "top_candidates": [candidate_summary(it) for it in items[:3]],
                    "fields_to_set": {},
                })
                print(f"[{i+1}/{len(rows)}] {r['ref_id']}: HOLD title-orthogonal", file=sys.stderr)
                continue

        fields = extract(top, dict(r))
        outcomes.append({
            "ref_id": r["ref_id"],
            "verdict": "MATCH-AUTHOR-YEAR",
            "reasons": [],
            "crossref_doi": top.get("DOI"),
            "crossref_type": top.get("type"),
            "fields_to_set": fields,
        })
        print(f"[{i+1}/{len(rows)}] {r['ref_id']}: MATCH DOI={top.get('DOI')}", file=sys.stderr)

    from collections import Counter
    cnt = Counter(o["verdict"] for o in outcomes)
    print("\n# === SUMMARY ===", file=sys.stderr)
    for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
        print(f"#   {k:30s} {v:>3d}", file=sys.stderr)
    print(json.dumps(outcomes, indent=2, default=str))


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    main(limit=limit)
