#!/usr/bin/env python3
"""
AUTHOR-TITLE-ONLY × VERIFIED × has-DOI rehabilitation probe.

Cohort: 59 rows. Verified-as-existing (V2-manual or earlier verification) but
metadata never extracted, leaving them stuck at metadata_quality=AUTHOR-TITLE-ONLY
and thus ineligible for synthesis under rule #10.

For each row: GET Crossref → extract journal/volume/issue/pages/author/publisher
→ cross-check against existing pub_title + first_author_last + pub_year → emit
per-row verdict and SQL UPDATE.

Verdict enum:
- ATO->COMPLETE-CROSSREF-MATCH: Crossref returned full metadata + cross-check
  on author/year/title PASSED. Safe to upgrade to COMPLETE.
- ATO->COMPLETE-CROSSREF-PARTIAL: Crossref returned but some fields missing
  (preprint without journal-of-record, etc). Upgrade to COMPLETE with caveat.
- HOLD-CROSSREF-MISMATCH: existing pub_title or first_author_last disagrees
  with Crossref. Do NOT upgrade; flag for manual review.
- HOLD-CROSSREF-MISS: DOI didn't resolve at Crossref (404). Try DOI.org direct.
- HOLD-CROSSREF-ERROR: transient API error; retry next session.
"""
import json
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "guidebook.db"
USER_AGENT = "Guidebook-Rehab/1.0 (mailto:[email protected])"
CROSSREF_BASE = "https://api.crossref.org/works/"
RATE_LIMIT_SLEEP = 0.25  # 4 req/sec, under the 5/sec limit


def normalize(s: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace for fuzzy comparison."""
    if not s:
        return ""
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def crossref_fetch(doi: str) -> tuple[dict | None, str]:
    """Return (work_dict, status). status ∈ {'ok','404','error'}."""
    # Crossref allows /works/<DOI>; URL-quote the DOI but slashes inside DOI
    # are allowed for Crossref.
    url = CROSSREF_BASE + doi
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data.get("message"), "ok"
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, "404"
        return None, f"http_{e.code}"
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
        return None, f"error:{type(e).__name__}"


def cross_check(row: dict, cr: dict) -> tuple[bool, list[str]]:
    """Return (match, mismatch_reasons)."""
    reasons = []
    # Title check
    cr_titles = cr.get("title", []) or []
    cr_subtitles = cr.get("subtitle", []) or []
    cr_full_title = (cr_titles[0] if cr_titles else "") + " " + (cr_subtitles[0] if cr_subtitles else "")
    existing_title = (row["pub_title"] or "") + " " + (row.get("pub_subtitle") or "")
    if cr_full_title.strip() and existing_title.strip():
        a, b = normalize(cr_full_title), normalize(existing_title)
        # Allow partial match: at least 4 tokens shared
        shared = set(a.split()) & set(b.split())
        if len(shared) < 3 and len(b.split()) >= 3:
            reasons.append(f"title:cr={cr_full_title[:60]!r} vs db={existing_title[:60]!r}")

    # Author check (first author surname)
    cr_authors = cr.get("author", []) or []
    cr_first_last = cr_authors[0].get("family", "") if cr_authors else ""
    db_last = row.get("first_author_last") or ""
    if cr_first_last and db_last:
        if normalize(cr_first_last) != normalize(db_last):
            reasons.append(f"author:cr={cr_first_last!r} vs db={db_last!r}")

    # Year check
    cr_year_parts = (cr.get("issued", {}).get("date-parts", [[None]])
                     or cr.get("published-print", {}).get("date-parts", [[None]])
                     or cr.get("published-online", {}).get("date-parts", [[None]]))
    cr_year = cr_year_parts[0][0] if cr_year_parts and cr_year_parts[0] else None
    db_year = row.get("pub_year")
    if cr_year and db_year and int(cr_year) != int(db_year):
        # Allow ±1 year (online-ahead-of-print)
        if abs(int(cr_year) - int(db_year)) > 1:
            reasons.append(f"year:cr={cr_year} vs db={db_year}")

    return len(reasons) == 0, reasons


def extract_metadata(cr: dict) -> dict:
    """Pull canonical academic metadata from a Crossref work record."""
    out = {}
    titles = cr.get("title", []) or []
    if titles:
        out["pub_title"] = titles[0]
    subtitles = cr.get("subtitle", []) or []
    if subtitles:
        out["pub_subtitle"] = subtitles[0]
    containers = cr.get("container-title", []) or []
    if containers:
        out["journal_name"] = containers[0]
    short_containers = cr.get("short-container-title", []) or []
    if short_containers and short_containers[0] != (containers[0] if containers else None):
        out["journal_abbrev"] = short_containers[0]
    if cr.get("volume"):
        out["volume"] = cr["volume"]
    if cr.get("issue"):
        out["issue"] = cr["issue"]
    if cr.get("page"):
        pg = cr["page"]
        if "-" in pg:
            a, b = pg.split("-", 1)
            out["pages_start"] = a.strip()
            out["pages_end"] = b.strip()
        else:
            out["pages_start"] = pg.strip()
    if cr.get("article-number"):
        out["article_number"] = cr["article-number"]
    if cr.get("publisher"):
        out["publisher"] = cr["publisher"]
    # ISSN: prefer print, fall back to electronic
    issns = cr.get("ISSN", []) or []
    if issns:
        out["issn"] = issns[0]
    # Authors → first_author_last, first_author_first, author_display, author_count
    authors = cr.get("author", []) or []
    if authors:
        out["author_count"] = len(authors)
        out["author_count_is_complete"] = 1
        first = authors[0]
        if first.get("family"):
            out["first_author_last"] = first["family"]
        if first.get("given"):
            out["first_author_first"] = first["given"]
        # Build display string
        names = []
        for a in authors:
            given = a.get("given", "")
            family = a.get("family", "")
            if family and given:
                # "Family, G."
                initials = ".".join(g[0] for g in given.split() if g) + "."
                names.append(f"{family}, {initials}")
            elif family:
                names.append(family)
            elif a.get("name"):
                names.append(a["name"])
        if names:
            out["author_display"] = "; ".join(names)
    # Year
    for k in ("issued", "published-print", "published-online"):
        dp = cr.get(k, {}).get("date-parts", [[None]])
        if dp and dp[0] and dp[0][0]:
            out["pub_year"] = int(dp[0][0])
            if len(dp[0]) > 1 and dp[0][1]:
                out["pub_month"] = int(dp[0][1])
            break
    # Type (Crossref's type field is informative but distinct from our source_type)
    cr_type = cr.get("type", "")
    if cr_type:
        out["_crossref_type"] = cr_type  # for analysis, not DB
    return out


def main(limit: int = 0, dry_run: bool = True):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT * FROM evidence_sources
        WHERE metadata_quality='AUTHOR-TITLE-ONLY'
          AND verification_status='VERIFIED'
          AND doi IS NOT NULL AND doi != ''
        ORDER BY ref_id
    """).fetchall()
    print(f"# Cohort: {len(rows)} rows", file=sys.stderr)
    if limit:
        rows = rows[:limit]
        print(f"# Limiting to first {limit}", file=sys.stderr)

    outcomes = []
    for i, r in enumerate(rows):
        doi = r["doi"]
        print(f"\n[{i+1}/{len(rows)}] {r['ref_id']} doi={doi}", file=sys.stderr)
        cr, status = crossref_fetch(doi)
        time.sleep(RATE_LIMIT_SLEEP)
        if status != "ok" or cr is None:
            outcomes.append({
                "ref_id": r["ref_id"],
                "verdict": f"HOLD-CROSSREF-{status.upper()}",
                "reasons": [status],
                "fields_to_set": {},
            })
            print(f"  -> HOLD ({status})", file=sys.stderr)
            continue

        match, reasons = cross_check(dict(r), cr)
        extracted = extract_metadata(cr)
        cr_type = extracted.pop("_crossref_type", "")

        # Only write fields not already populated; the existing field wins
        # unless it is NULL/empty.
        fields_to_set = {}
        for k, v in extracted.items():
            existing = r[k] if k in r.keys() else None
            if existing in (None, "", 0) or (k == "pub_year" and existing is None):
                fields_to_set[k] = v

        if not match:
            verdict = "HOLD-CROSSREF-MISMATCH"
            fields_to_set = {}  # do not write mismatched data
        else:
            # Determine COMPLETE vs PARTIAL
            essentials_present = (
                ("journal_name" in fields_to_set or r["journal_name"])
                and ("pages_start" in fields_to_set or "article_number" in fields_to_set
                     or r["pages_start"] or r["article_number"])
                and ("first_author_last" in fields_to_set or r["first_author_last"])
            )
            # Books / book chapters / standards don't always have these academic
            # fields; check Crossref type. For journal-article type, essentials
            # must be present. For other types (book, dataset, posted-content),
            # we accept whatever the record has.
            if cr_type in ("journal-article", "review-article") and not essentials_present:
                verdict = "ATO->COMPLETE-CROSSREF-PARTIAL"
            else:
                verdict = "ATO->COMPLETE-CROSSREF-MATCH"
            fields_to_set["metadata_quality"] = "COMPLETE"

        outcomes.append({
            "ref_id": r["ref_id"],
            "verdict": verdict,
            "reasons": reasons,
            "crossref_type": cr_type,
            "fields_to_set": fields_to_set,
        })
        print(f"  -> {verdict}  ({len(fields_to_set)} fields)", file=sys.stderr)

    # Summary
    from collections import Counter
    cnt = Counter(o["verdict"] for o in outcomes)
    print("\n# === SUMMARY ===", file=sys.stderr)
    for k, v in sorted(cnt.items()):
        print(f"# {k}: {v}", file=sys.stderr)

    # Emit JSON to stdout for downstream migration generation
    print(json.dumps(outcomes, indent=2, default=str))


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    main(limit=limit)
