#!/usr/bin/env python3
"""
Citation mining pipeline.

Step 1: For every evidence_sources row with verified DOI (metadata_integrity_status='OK'
        AND doi IS NOT NULL), fetch Crossref's full record and extract the reference
        list. Aggregate all references into a single pool indexed by (author, year).
Step 2: For every ATO row with no identifier but with author+year, query the pool
        for candidate references matching (author_surname, year ±1).
Step 3: Cross-check each single-match candidate: author + year agree + title-token
        overlap with stored pub_title >= 3 if stored title has >= 5 meaningful tokens,
        else just author+year+publisher-marker.
Step 4: Emit JSON of matches/holds for downstream migration generator.

Output structure for owner triage on holds:
  - Multi-candidate hits get all candidates surfaced
  - Single-candidate hits below threshold get the candidate + reasons

No DB writes. Pure search/analysis.
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
from collections import defaultdict
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "guidebook.db"
CROSSREF = "https://api.crossref.org/works"
USER_AGENT = "Guidebook-CitationMining/1.0 (mailto:[email protected])"
RATE_LIMIT_SLEEP = 0.25
POOL_CACHE = Path("/tmp/citation_pool.json")


def normalize(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def fetch_references(doi):
    url = f"{CROSSREF}/{urllib.parse.quote(doi, safe='')}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        return data["message"].get("reference", []) or [], "ok"
    except Exception as e:
        return [], f"error:{type(e).__name__}"


def build_pool():
    """Mine references from all verified DOIs. Returns dict[(author_norm, year)] -> [refs]."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    seeds = conn.execute("""
        SELECT ref_id, doi FROM evidence_sources
        WHERE doi IS NOT NULL AND doi != ''
          AND metadata_integrity_status = 'OK'
        ORDER BY ref_id
    """).fetchall()
    print(f"Mining references from {len(seeds)} seed papers", file=sys.stderr)

    pool = defaultdict(list)
    seen_dois = set()
    total_refs = 0
    structured_with_doi = 0

    for i, s in enumerate(seeds):
        refs, status = fetch_references(s["doi"])
        time.sleep(RATE_LIMIT_SLEEP)
        if status != "ok":
            print(f"  [{i+1}/{len(seeds)}] {s['ref_id']}: {status}", file=sys.stderr)
            continue
        for ref in refs:
            total_refs += 1
            author = ref.get("author", "")
            year = ref.get("year", "")
            cited_doi = ref.get("DOI", "")
            # Skip refs with no useful match-keys
            if not (author and year):
                continue
            structured_with_doi += 1 if cited_doi else 0
            try:
                y = int(year)
            except (ValueError, TypeError):
                continue
            key = (normalize(author), y)
            pool[key].append({
                "seed_ref": s["ref_id"],
                "doi": cited_doi,
                "author": author,
                "year": y,
                "article_title": ref.get("article-title", ""),
                "journal_title": ref.get("journal-title", ""),
                "volume": ref.get("volume", ""),
                "first_page": ref.get("first-page", ""),
                "unstructured": ref.get("unstructured", ""),
            })
        if (i + 1) % 10 == 0:
            print(f"  [{i+1}/{len(seeds)}] cumulative refs={total_refs} indexed={sum(len(v) for v in pool.values())}", file=sys.stderr)

    # Dedupe by DOI within each (author, year) bucket
    deduped = defaultdict(list)
    for key, refs in pool.items():
        seen = set()
        for r in refs:
            if r["doi"] and r["doi"] in seen:
                continue
            if r["doi"]:
                seen.add(r["doi"])
            deduped[key].append(r)

    print(f"\nPool: {sum(len(v) for v in deduped.values())} unique refs in {len(deduped)} (author, year) buckets", file=sys.stderr)
    print(f"Total refs scanned: {total_refs}, structured_with_doi: {structured_with_doi}", file=sys.stderr)

    # Serialize for cache (defaultdict + tuple keys -> list-of-tuples)
    pool_serializable = [{"author": k[0], "year": k[1], "refs": v} for k, v in deduped.items()]
    POOL_CACHE.write_text(json.dumps(pool_serializable, indent=2, default=str))
    print(f"Cached pool to {POOL_CACHE}", file=sys.stderr)
    return deduped


def load_pool_from_cache():
    if not POOL_CACHE.exists():
        return None
    data = json.loads(POOL_CACHE.read_text())
    pool = defaultdict(list)
    for entry in data:
        pool[(entry["author"], entry["year"])] = entry["refs"]
    return pool


def match_ato_rows(pool):
    """For each ATO row with author+year+no-ID, search the pool."""
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
    print(f"\nMatching {len(rows)} ATO rows against pool", file=sys.stderr)

    outcomes = []
    for r in rows:
        author_norm = normalize(r["first_author_last"])
        year = int(r["pub_year"])
        # Check (author, year), (author, year-1), (author, year+1)
        candidates = []
        for y in (year, year - 1, year + 1):
            candidates.extend(pool.get((author_norm, y), []))

        if not candidates:
            outcomes.append({"ref_id": r["ref_id"], "verdict": "NO-MATCH-IN-POOL",
                             "stored": {"author": r["first_author_last"], "year": year,
                                        "title": (r["pub_title"] or "")[:80]},
                             "candidates": []})
            continue

        # Title-coherence check
        db_title_norm = normalize(r["pub_title"] or "")
        db_tokens = set(db_title_norm.split())
        stop = {"the", "a", "an", "of", "in", "and", "for", "on", "to", "with", "by", "at", "from"}
        meaningful_db_tokens = db_tokens - stop

        scored = []
        for cand in candidates:
            cand_title_norm = normalize(cand.get("article_title", ""))
            cand_tokens = set(cand_title_norm.split())
            shared = cand_tokens & meaningful_db_tokens
            scored.append((len(shared), cand))
        scored.sort(reverse=True, key=lambda x: x[0])

        top_score = scored[0][0] if scored else 0
        top_cand = scored[0][1] if scored else None

        # Verdict logic:
        # MATCH-STRONG:    top shared >= 4 AND >= 1 above next-best  (clear winner)
        # MATCH-PROBABLE:  top shared >= 3 AND unique (one candidate only)
        # MULTI-AMBIGUOUS: multiple candidates with similar scores
        # HOLD-WEAK:       top shared 1-2; surface for owner
        # NO-TITLE-SIGNAL: db_title <3 meaningful tokens; surface candidates only

        if len(meaningful_db_tokens) < 3:
            outcomes.append({"ref_id": r["ref_id"], "verdict": "NO-TITLE-SIGNAL-OWNER",
                             "stored": {"author": r["first_author_last"], "year": year,
                                        "title": (r["pub_title"] or "")[:80]},
                             "candidates": [c for _, c in scored[:5]]})
            continue

        if len(scored) == 1 and top_score >= 3:
            outcomes.append({"ref_id": r["ref_id"], "verdict": "MATCH-PROBABLE",
                             "stored": {"author": r["first_author_last"], "year": year,
                                        "title": (r["pub_title"] or "")[:80]},
                             "candidates": [top_cand],
                             "match_score": top_score})
            continue

        if top_score >= 4 and (len(scored) == 1 or scored[1][0] < top_score - 1):
            outcomes.append({"ref_id": r["ref_id"], "verdict": "MATCH-STRONG",
                             "stored": {"author": r["first_author_last"], "year": year,
                                        "title": (r["pub_title"] or "")[:80]},
                             "candidates": [top_cand],
                             "match_score": top_score})
            continue

        if top_score >= 3:
            outcomes.append({"ref_id": r["ref_id"], "verdict": "MULTI-AMBIGUOUS",
                             "stored": {"author": r["first_author_last"], "year": year,
                                        "title": (r["pub_title"] or "")[:80]},
                             "candidates": [c for _, c in scored[:3]]})
            continue

        outcomes.append({"ref_id": r["ref_id"], "verdict": "HOLD-WEAK-SIGNAL",
                         "stored": {"author": r["first_author_last"], "year": year,
                                    "title": (r["pub_title"] or "")[:80]},
                         "candidates": [c for _, c in scored[:3]],
                         "top_score": top_score})

    return outcomes


def main():
    rebuild = "--rebuild" in sys.argv
    pool = load_pool_from_cache() if not rebuild else None
    if pool is None:
        pool = build_pool()
    else:
        print(f"Loaded pool from cache: {sum(len(v) for v in pool.values())} refs", file=sys.stderr)

    outcomes = match_ato_rows(pool)
    from collections import Counter
    cnt = Counter(o["verdict"] for o in outcomes)
    print("\n# === MATCHING SUMMARY ===", file=sys.stderr)
    for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
        print(f"#   {k:30s} {v:>3d}", file=sys.stderr)
    print(json.dumps(outcomes, indent=2, default=str))


if __name__ == "__main__":
    main()
