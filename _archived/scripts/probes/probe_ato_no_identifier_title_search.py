#!/usr/bin/env python3
"""
ATO no-identifier title-search probe (cohort: 139 academic ATO rows without DOI/PMID).

Three-tier strategy:
  HIGH-CONF: author + year present  -> aggressive phrase-search, all-three-pass cross-check
  MID-CONF:  year only              -> conservative phrase-search, title+year-only check;
                                       need 5+ shared tokens AND publisher markers
  LOW-CONF:  no year                -> SKIP, owner-queue

Citation parser pre-step (from parse_citation_shorthand.py): extract embedded
journal/volume/pages from note-as-title strings to refine the search query.

Per rule 1B: never overwrite existing fields. On MATCH, write canonical only
to empty fields. Pub_title is kept as-is unless completely empty.
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
USER_AGENT = "Guidebook-TitleSearch/3.0 (mailto:[email protected])"
RATE_LIMIT_SLEEP = 0.25


def normalize(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# Parser patterns (subset of parse_citation_shorthand — only patterns yielding
# search-refinement hints, not standalone writes)
PARSER_PATTERNS = [
    # <title>. <Journal> <vol>(<issue>):<pages_start>-<pages_end>
    (re.compile(r"^(?P<title>.+?)\.\s+(?P<journal>[A-Z][A-Za-z][A-Za-z0-9 .&'\-]+?)\s+(?P<volume>\d+)\((?P<issue>\d+[A-Za-z]?)\)\s*[:;]\s*(?P<ps>e?\d+)\s*[-–]\s*(?P<pe>e?\d+)\s*$"),
     "journal+vol(issue):ps-pe"),
    # <title>. <Journal> <vol>:<pages>
    (re.compile(r"^(?P<title>.+?)\.\s+(?P<journal>[A-Z][A-Za-z][A-Za-z0-9 .&'\-]+?)\s+(?P<volume>\d+)\s*[:;]\s*(?P<ps>e?\d+)(?:\s*[-–]\s*(?P<pe>e?\d+))?\s*$"),
     "journal+vol:ps"),
    # <title>. <Journal name>  (terminal journal abbrev)
    (re.compile(r"^(?P<title>.{15,}?)\.\s+(?P<journal>(?:[A-Z][A-Za-z]+\s+){1,3}[A-Z][A-Za-z]+)\s*$"),
     "title.journal-abbrev"),
]


def parse_title(s):
    """Extract (clean_title, journal_hint, volume_hint) or return (None, None, None)."""
    if not s:
        return None, None, None
    s = s.strip()
    for regex, name in PARSER_PATTERNS:
        m = regex.match(s)
        if m:
            g = m.groupdict()
            return (
                g.get("title", "").strip().rstrip(".").strip() if g.get("title") else None,
                g.get("journal", "").strip() if g.get("journal") else None,
                g.get("volume", "").strip() if g.get("volume") else None,
            )
    return None, None, None


def search_crossref(title, author=None, year=None, container_title=None):
    """Bibliographic phrase search. Returns list of top items or error string."""
    params = {"query.bibliographic": title, "rows": 5}
    if author:
        params["query.author"] = author
    if container_title:
        params["query.container-title"] = container_title
    if year:
        params["filter"] = f"from-pub-date:{year-1},until-pub-date:{year+1}"
    url = f"{CROSSREF}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        return data.get("message", {}).get("items", []) or []
    except Exception as e:
        return f"error:{type(e).__name__}"


def cross_check_high(row, item, parsed_title=None):
    """All-three-must-pass: title, author, year. For HIGH-CONF tier."""
    reasons = []
    titles = item.get("title", []) or []
    cr_title = titles[0] if titles else ""
    search_title = parsed_title or row["pub_title"]
    a, b = normalize(cr_title), normalize(search_title or "")
    shared = set(a.split()) & set(b.split())
    if not (len(shared) >= 4 or (len(shared) >= 3 and len(b.split()) <= 5)):
        st_repr = repr(search_title[:50]) if search_title else "''"
        reasons.append(f"title:cr={cr_title[:50]!r} stored={st_repr} shared={len(shared)}")

    authors = item.get("author", []) or []
    cr_last = authors[0].get("family", "") if authors else ""
    db_last = row["first_author_last"] or ""
    if db_last and normalize(cr_last) != normalize(db_last):
        reasons.append(f"author:cr={cr_last!r} db={db_last!r}")

    parts = item.get("issued", {}).get("date-parts", [[None]])
    cr_year = parts[0][0] if parts and parts[0] else None
    db_year = row["pub_year"]
    if cr_year and db_year and abs(int(cr_year) - int(db_year)) > 1:
        reasons.append(f"year:cr={cr_year} db={db_year}")

    return reasons


def cross_check_mid(row, item, parsed_title=None):
    """Title + year only; need 5+ shared tokens AND publisher markers (container_title)."""
    reasons = []
    titles = item.get("title", []) or []
    cr_title = titles[0] if titles else ""
    search_title = parsed_title or row["pub_title"]
    a, b = normalize(cr_title), normalize(search_title or "")
    shared = set(a.split()) & set(b.split())
    if len(shared) < 5:
        reasons.append(f"title-thin:shared={len(shared)} cr={cr_title[:50]!r}")

    parts = item.get("issued", {}).get("date-parts", [[None]])
    cr_year = parts[0][0] if parts and parts[0] else None
    db_year = row["pub_year"]
    if cr_year and db_year and abs(int(cr_year) - int(db_year)) > 1:
        reasons.append(f"year:cr={cr_year} db={db_year}")

    if not (item.get("container-title") and (item.get("volume") or item.get("ISBN"))):
        reasons.append("low-confidence:no publisher markers")
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


def main(limit=0):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT * FROM evidence_sources
        WHERE (doi IS NULL OR doi='') AND (pmid IS NULL OR pmid='')
          AND metadata_quality='AUTHOR-TITLE-ONLY'
          AND source_type IN ('report','journal_article','book_chapter','book','thesis','internal')
        ORDER BY ref_id
    """).fetchall()
    print(f"# Cohort: {len(rows)} rows", file=sys.stderr)
    if limit:
        rows = rows[:limit]

    outcomes = []
    for i, r in enumerate(rows):
        author = r["first_author_last"]
        year = int(r["pub_year"]) if r["pub_year"] else None
        if not year:
            outcomes.append({"ref_id": r["ref_id"], "verdict": "SKIP-NO-YEAR", "reasons": ["no pub_year"], "fields_to_set": {}})
            print(f"[{i+1}/{len(rows)}] {r['ref_id']}: SKIP no-year", file=sys.stderr)
            continue
        tier = "HIGH" if author else "MID"

        title = r["pub_title"] or ""
        parsed_title, parsed_journal, parsed_volume = parse_title(title)
        search_title = parsed_title or title
        if len(normalize(search_title).split()) < 3:
            outcomes.append({"ref_id": r["ref_id"], "verdict": "SKIP-SHORT-TITLE", "reasons": ["title<3 tokens"], "fields_to_set": {}})
            print(f"[{i+1}/{len(rows)}] {r['ref_id']}: SKIP short-title", file=sys.stderr)
            continue

        items = search_crossref(search_title, author, year, parsed_journal)
        time.sleep(RATE_LIMIT_SLEEP)
        if isinstance(items, str):
            outcomes.append({"ref_id": r["ref_id"], "verdict": "SKIP-API-ERROR", "reasons": [items], "fields_to_set": {}})
            print(f"[{i+1}/{len(rows)}] {r['ref_id']}: {items}", file=sys.stderr)
            continue
        if not items:
            outcomes.append({"ref_id": r["ref_id"], "verdict": "HOLD-NO-RESULTS", "reasons": ["empty Crossref response"], "fields_to_set": {}, "tier": tier})
            print(f"[{i+1}/{len(rows)}] {r['ref_id']}: HOLD no-results", file=sys.stderr)
            continue

        top = items[0]
        if tier == "HIGH":
            reasons = cross_check_high(dict(r), top, parsed_title)
        else:
            reasons = cross_check_mid(dict(r), top, parsed_title)

        if reasons:
            outcomes.append({"ref_id": r["ref_id"], "verdict": f"HOLD-{tier}-MISMATCH", "reasons": reasons, "fields_to_set": {}, "tier": tier})
            print(f"[{i+1}/{len(rows)}] {r['ref_id']}: HOLD {tier} ({len(reasons)} reasons)", file=sys.stderr)
            continue

        fields = extract(top, dict(r))
        outcomes.append({
            "ref_id": r["ref_id"],
            "verdict": f"MATCH-{tier}",
            "reasons": [],
            "crossref_doi": top.get("DOI"),
            "crossref_type": top.get("type"),
            "fields_to_set": fields,
            "tier": tier,
        })
        print(f"[{i+1}/{len(rows)}] {r['ref_id']}: MATCH-{tier} DOI={top.get('DOI')}", file=sys.stderr)

    from collections import Counter
    cnt = Counter(o["verdict"] for o in outcomes)
    print("\n# === SUMMARY ===", file=sys.stderr)
    for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
        print(f"#   {k:30s} {v:>3d}", file=sys.stderr)
    print(json.dumps(outcomes, indent=2, default=str))


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    main(limit=limit)
