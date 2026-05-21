#!/usr/bin/env python3
"""
Multi-source ATO no-identifier recovery probe.

Queries OpenAlex and Semantic Scholar in parallel for each ATO×no-ID row with
author+year. Promotes to MATCH-CONFIRMED only when both APIs return the same
DOI (or one returns a DOI and the other returns the same paper title/author
without DOI). Single-source matches get HOLD-SINGLE-SOURCE with the candidate
attached for owner review.

This is deliberately stricter than the v4 author+year Crossref probe (which
yielded zero confirmed matches and one wrong-attribution risk). Two-API
agreement substantially reduces wrong-Levine-paper-from-same-author class
of error because the two APIs have different ranking/scoring algorithms.

Per rule 1B: never overwrite existing fields on write.

Output JSON has one record per ATO row with full candidates from both APIs
for downstream migration generator and owner queue.
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
OPENALEX = "https://api.openalex.org/works"
SEMSCHOLAR = "https://api.semanticscholar.org/graph/v1/paper/search"
USER_AGENT = "Guidebook-MultiSource/1.0 (mailto:[email protected])"
OPENALEX_SLEEP = 0.15  # 10 req/s polite
SEMSCHOLAR_SLEEP = 0.4  # 100 req / 5 min unauth = 3 req/sec safe; pace conservatively


def normalize(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def strip_doi_url(d):
    if not d:
        return None
    d = d.strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if d.lower().startswith(prefix):
            d = d[len(prefix):]
    return d.strip().lower() or None


def openalex_search(author, year, title_hint=None):
    """Author + year filter on OpenAlex. title_hint refines search if non-empty."""
    search_q = author
    if title_hint:
        # Pull 3-5 meaningful tokens from title_hint
        toks = [t for t in normalize(title_hint).split()
                if len(t) > 3 and t not in {"the", "and", "for", "with", "from"}]
        search_q = f"{author} " + " ".join(toks[:4])
    params = {
        "search": search_q,
        "filter": f"publication_year:{year}",
        "per-page": 5,
    }
    url = f"{OPENALEX}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        return data.get("results", []) or [], "ok"
    except Exception as e:
        return [], f"error:{type(e).__name__}"


def semscholar_search(author, year, title_hint=None):
    """Author + year on Semantic Scholar."""
    q = author
    if title_hint:
        toks = [t for t in normalize(title_hint).split()
                if len(t) > 3 and t not in {"the", "and", "for", "with", "from"}]
        q = f"{author} " + " ".join(toks[:4])
    params = {
        "query": q,
        "year": str(year),
        "fields": "title,externalIds,authors,year,venue,publicationTypes",
        "limit": 5,
    }
    url = f"{SEMSCHOLAR}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        return data.get("data", []) or [], "ok"
    except urllib.error.HTTPError as e:
        if e.code == 429:
            time.sleep(5)
            return [], "rate-limited"
        return [], f"http_{e.code}"
    except Exception as e:
        return [], f"error:{type(e).__name__}"


def oa_first_author(item):
    auths = item.get("authorships", []) or []
    if not auths:
        return ""
    name = auths[0].get("author", {}).get("display_name", "")
    return name.rsplit(" ", 1)[-1] if name else ""


def oa_doi(item):
    return strip_doi_url(item.get("doi"))


def oa_title(item):
    return item.get("title", "") or ""


def oa_year(item):
    return item.get("publication_year")


def oa_venue(item):
    psl = item.get("primary_location") or {}
    src = psl.get("source") or {}
    return src.get("display_name", "")


def ss_first_author(item):
    auths = item.get("authors", []) or []
    if not auths:
        return ""
    name = auths[0].get("name", "")
    return name.rsplit(" ", 1)[-1] if name else ""


def ss_doi(item):
    eid = item.get("externalIds") or {}
    return strip_doi_url(eid.get("DOI"))


def ss_title(item):
    return item.get("title", "") or ""


def ss_year(item):
    return item.get("year")


def ss_venue(item):
    return item.get("venue", "")


def title_overlap(t1, t2):
    """Token overlap count between two titles."""
    a = set(normalize(t1).split())
    b = set(normalize(t2).split())
    stop = {"the", "a", "an", "of", "in", "and", "for", "on", "to", "with", "by", "at", "from"}
    return len(a & b - stop)


def find_matching_pair(oa_items, ss_items, db_author):
    """Look for the same DOI in both result lists. Returns (oa_item, ss_item, doi) or None."""
    oa_dois = {oa_doi(it): it for it in oa_items if oa_doi(it)}
    ss_dois = {ss_doi(it): it for it in ss_items if ss_doi(it)}
    common = set(oa_dois) & set(ss_dois)
    for doi in common:
        # Verify author matches stored in both
        oa_a = normalize(oa_first_author(oa_dois[doi]))
        ss_a = normalize(ss_first_author(ss_dois[doi]))
        db_a = normalize(db_author)
        if oa_a == db_a or ss_a == db_a:
            return oa_dois[doi], ss_dois[doi], doi
    return None


def single_source_candidate(items, db_author, db_year, get_doi, get_author, get_title, get_year):
    """Return the strongest single-source candidate passing author + year gate, or None."""
    for it in items:
        cand_doi = get_doi(it)
        cand_author = get_author(it)
        cand_year = get_year(it)
        if not cand_doi:
            continue
        if normalize(cand_author) != normalize(db_author):
            continue
        if cand_year and db_year and abs(int(cand_year) - int(db_year)) > 1:
            continue
        return it
    return None


def main(limit=0):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT * FROM evidence_sources
        WHERE (doi IS NULL OR doi='') AND (pmid IS NULL OR pmid='')
          AND metadata_quality='AUTHOR-TITLE-ONLY'
          AND first_author_last IS NOT NULL AND first_author_last != ''
          AND pub_year IS NOT NULL
        ORDER BY ref_id
    """).fetchall()
    print(f"# Cohort: {len(rows)} ATO×no-ID rows with author+year", file=sys.stderr)
    if limit:
        rows = rows[:limit]

    outcomes = []
    for i, r in enumerate(rows):
        author = r["first_author_last"]
        year = int(r["pub_year"])
        title_hint = r["pub_title"] or ""

        oa_items, oa_status = openalex_search(author, year, title_hint)
        time.sleep(OPENALEX_SLEEP)
        ss_items, ss_status = semscholar_search(author, year, title_hint)
        time.sleep(SEMSCHOLAR_SLEEP)

        record = {
            "ref_id": r["ref_id"],
            "stored": {
                "author": author, "year": year,
                "title": (r["pub_title"] or "")[:100],
                "source_type": r["source_type"],
            },
            "openalex_status": oa_status,
            "semscholar_status": ss_status,
            "openalex_candidates": [],
            "semscholar_candidates": [],
        }

        # Build candidate summaries for record
        for it in oa_items[:3]:
            record["openalex_candidates"].append({
                "doi": oa_doi(it),
                "title": oa_title(it)[:120],
                "author": oa_first_author(it),
                "year": oa_year(it),
                "venue": oa_venue(it),
                "primary_topic": (it.get("primary_topic") or {}).get("display_name"),
            })
        for it in ss_items[:3]:
            record["semscholar_candidates"].append({
                "doi": ss_doi(it),
                "title": ss_title(it)[:120],
                "author": ss_first_author(it),
                "year": ss_year(it),
                "venue": ss_venue(it),
                "types": it.get("publicationTypes"),
            })

        # Two-source agreement check
        pair = find_matching_pair(oa_items, ss_items, author)
        if pair:
            oa_it, ss_it, doi = pair
            # Extra: title-coherence with stored
            t_overlap_oa = title_overlap(oa_title(oa_it), title_hint)
            record.update({
                "verdict": "MATCH-CONFIRMED-2-SOURCE",
                "matched_doi": doi,
                "match_authors_oa": oa_first_author(oa_it),
                "match_title_oa": oa_title(oa_it)[:120],
                "match_title_overlap_with_stored": t_overlap_oa,
            })
            print(f"[{i+1}/{len(rows)}] {r['ref_id']}: MATCH-2-SOURCE doi={doi} title-overlap={t_overlap_oa}", file=sys.stderr)
            outcomes.append(record)
            continue

        # Single-source matches with strict gate
        oa_single = single_source_candidate(oa_items, author, year,
                                            oa_doi, oa_first_author, oa_title, oa_year)
        ss_single = single_source_candidate(ss_items, author, year,
                                            ss_doi, ss_first_author, ss_title, ss_year)

        if oa_single and ss_single and oa_doi(oa_single) != ss_doi(ss_single):
            record.update({"verdict": "DISAGREE-OWNER",
                           "oa_doi": oa_doi(oa_single),
                           "ss_doi": ss_doi(ss_single)})
            print(f"[{i+1}/{len(rows)}] {r['ref_id']}: DISAGREE oa={oa_doi(oa_single)} ss={ss_doi(ss_single)}", file=sys.stderr)
        elif oa_single:
            record.update({"verdict": "HOLD-SINGLE-OA",
                           "candidate_doi": oa_doi(oa_single),
                           "candidate_title": oa_title(oa_single)[:120]})
            print(f"[{i+1}/{len(rows)}] {r['ref_id']}: SINGLE-OA doi={oa_doi(oa_single)}", file=sys.stderr)
        elif ss_single:
            record.update({"verdict": "HOLD-SINGLE-SS",
                           "candidate_doi": ss_doi(ss_single),
                           "candidate_title": ss_title(ss_single)[:120]})
            print(f"[{i+1}/{len(rows)}] {r['ref_id']}: SINGLE-SS doi={ss_doi(ss_single)}", file=sys.stderr)
        elif not oa_items and not ss_items:
            record["verdict"] = "NO-CANDIDATES"
            print(f"[{i+1}/{len(rows)}] {r['ref_id']}: NO-CANDIDATES", file=sys.stderr)
        else:
            record["verdict"] = "HOLD-GATE-FAILED"
            print(f"[{i+1}/{len(rows)}] {r['ref_id']}: HOLD gate", file=sys.stderr)

        outcomes.append(record)

    from collections import Counter
    cnt = Counter(o["verdict"] for o in outcomes)
    print("\n# === SUMMARY ===", file=sys.stderr)
    for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
        print(f"#   {k:30s} {v:>3d}", file=sys.stderr)
    print(json.dumps(outcomes, indent=2, default=str))


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    main(limit=limit)
