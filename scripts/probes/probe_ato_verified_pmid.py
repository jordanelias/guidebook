#!/usr/bin/env python3
"""
AUTHOR-TITLE-ONLY × VERIFIED × has-PMID rehabilitation probe (batch 2).

Cohort: 9 ATO×VERIFIED×has-PMID rows + 2 batch-1 DOI-TRUNCATED rescue-eligible
rows (REF-00027, REF-00527) that have both a PMID and a truncated DOI.
For the rescue rows, success additionally replaces the truncated DOI with the
canonical full DOI from PubMed's articleids list.

Applies batch-1 lessons:
- NFKD normalizer strips combining marks (no diacritic false positives)
- Migration does not self-insert into data_migrations (runner tracks)
- Type-routed: PubMed esummary returns 'pubtype' and 'doctype' fields

Verdict enum mirrors batch 1:
  ATO->COMPLETE-PUBMED-MATCH       — clean upgrade
  ATO->COMPLETE-PUBMED-MATCH-DOI-RESCUE — clean + canonical DOI replaces truncated
  HOLD-PUBMED-MISMATCH             — author/title/year disagreement
  HOLD-PUBMED-ERROR                — API error or no record
"""
import json
import re
import sqlite3
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "guidebook.db"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
USER_AGENT = "Guidebook-Rehab/1.0 (mailto:[email protected])"
RATE_LIMIT_SLEEP = 0.34  # 3 req/sec without an API key


def normalize(s: str) -> str:
    """NFKD-strip combining marks + lowercase + de-punctuate. Patches the
    batch-1 normalizer's diacritic blindness (REF-00398 Larivière case)."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def pubmed_fetch(pmid: str) -> tuple[dict | None, str]:
    """Return (record_dict, status). status ∈ {'ok','not-found','error'}."""
    url = f"{EUTILS}?db=pubmed&id={pmid}&retmode=json"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            rec = data.get("result", {}).get(pmid)
            if not rec or rec.get("error"):
                return None, "not-found"
            return rec, "ok"
    except urllib.error.HTTPError as e:
        return None, f"http_{e.code}"
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
        return None, f"error:{type(e).__name__}"


def cross_check(row: dict, rec: dict) -> tuple[bool, list[str]]:
    reasons = []
    rec_title = rec.get("title", "")
    db_title = row.get("pub_title") or ""
    if rec_title and db_title:
        a, b = normalize(rec_title), normalize(db_title)
        shared = set(a.split()) & set(b.split())
        if len(shared) < 3 and len(b.split()) >= 3:
            reasons.append(f"title:pm={rec_title[:60]!r} vs db={db_title[:60]!r}")

    # First author: PubMed returns "Family I" format (e.g., "Kennedy MJ")
    rec_authors = rec.get("authors", []) or []
    rec_first = rec_authors[0].get("name", "") if rec_authors else ""
    # Extract surname: text before first space-initials block
    rec_last = rec_first.rsplit(" ", 1)[0] if " " in rec_first else rec_first
    db_last = row.get("first_author_last") or ""
    if rec_last and db_last and normalize(rec_last) != normalize(db_last):
        reasons.append(f"author:pm={rec_last!r} vs db={db_last!r}")

    # Year: pubdate format "2015 Summer" or "2024 Aug 15"
    rec_pubdate = rec.get("pubdate", "")
    rec_year_m = re.match(r"^(\d{4})", rec_pubdate)
    rec_year = int(rec_year_m.group(1)) if rec_year_m else None
    db_year = row.get("pub_year")
    if rec_year and db_year and abs(rec_year - int(db_year)) > 1:
        reasons.append(f"year:pm={rec_year} vs db={db_year}")

    return len(reasons) == 0, reasons


def extract_metadata(rec: dict) -> dict:
    out = {}
    if rec.get("title"): out["pub_title"] = rec["title"]
    if rec.get("fulljournalname"): out["journal_name"] = rec["fulljournalname"]
    if rec.get("source"): out["journal_abbrev"] = rec["source"]
    if rec.get("volume"): out["volume"] = rec["volume"]
    if rec.get("issue"): out["issue"] = rec["issue"]
    if rec.get("pages"):
        pg = rec["pages"]
        if "-" in pg:
            a, b = pg.split("-", 1)
            out["pages_start"] = a.strip()
            out["pages_end"] = b.strip()
        else:
            out["pages_start"] = pg.strip()
    if rec.get("issn"): out["issn"] = rec["issn"]
    # Year
    rec_pubdate = rec.get("pubdate", "")
    rec_year_m = re.match(r"^(\d{4})", rec_pubdate)
    if rec_year_m:
        out["pub_year"] = int(rec_year_m.group(1))
    # DOI from articleids
    for aid in rec.get("articleids", []):
        if aid.get("idtype") == "doi":
            out["doi"] = aid["value"]
            break
    # PMC ID if present
    for aid in rec.get("articleids", []):
        if aid.get("idtype") == "pmc":
            out["pmcid"] = aid["value"]
            break
    # Authors → first_author_first only (last already in db); author_display
    authors = rec.get("authors", []) or []
    if authors:
        out["author_count"] = len(authors)
        out["author_count_is_complete"] = 1
        names = []
        for a in authors:
            n = a.get("name", "")
            if n:
                # Split "Family Initials" → "Family, I."
                parts = n.rsplit(" ", 1)
                if len(parts) == 2:
                    family, initials = parts
                    initials_dotted = ".".join(initials) + "." if initials else ""
                    names.append(f"{family}, {initials_dotted}".rstrip("."))
                else:
                    names.append(n)
        if names:
            out["author_display"] = "; ".join(names)
        # first_author_first as initials (PubMed doesn't store given name in plain form)
        first_name_block = authors[0].get("name", "").rsplit(" ", 1)
        if len(first_name_block) == 2:
            out["first_author_first"] = first_name_block[1]
    # Pubtype for downstream
    out["_pubtype"] = rec.get("pubtype", [])
    return out


def main(limit: int = 0):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Two cohorts unioned:
    #   A) ATO×VERIFIED×has-PMID (no DOI OR has DOI but might still be incomplete) — primary
    #   B) batch-1 DOI-TRUNCATED rows that have a PMID (rescue path)
    rows = conn.execute("""
        SELECT * FROM evidence_sources
        WHERE pmid IS NOT NULL AND pmid != ''
          AND (
                (metadata_quality='AUTHOR-TITLE-ONLY' AND verification_status='VERIFIED')
            OR  (metadata_integrity_status='DOI-TRUNCATED')
          )
        ORDER BY ref_id
    """).fetchall()
    print(f"# Cohort: {len(rows)} rows", file=sys.stderr)
    if limit:
        rows = rows[:limit]

    outcomes = []
    for i, r in enumerate(rows):
        pmid = r["pmid"]
        is_rescue = r["metadata_integrity_status"] == "DOI-TRUNCATED"
        tag = " [DOI-rescue]" if is_rescue else ""
        print(f"\n[{i+1}/{len(rows)}] {r['ref_id']} pmid={pmid}{tag}", file=sys.stderr)
        rec, status = pubmed_fetch(pmid)
        time.sleep(RATE_LIMIT_SLEEP)
        if status != "ok" or rec is None:
            outcomes.append({"ref_id": r["ref_id"], "verdict": f"HOLD-PUBMED-{status.upper()}",
                             "reasons": [status], "fields_to_set": {}, "is_rescue": is_rescue})
            print(f"  -> HOLD ({status})", file=sys.stderr)
            continue

        match, reasons = cross_check(dict(r), rec)
        extracted = extract_metadata(rec)
        pubtype = extracted.pop("_pubtype", [])

        if not match:
            verdict = "HOLD-PUBMED-MISMATCH"
            fields_to_set = {}
        else:
            # Build fields_to_set: only write where existing is empty/NULL
            fields_to_set = {}
            for k, v in extracted.items():
                existing = r[k] if k in r.keys() else None
                if existing in (None, "", 0):
                    fields_to_set[k] = v
            # Rescue path: also overwrite the truncated DOI with canonical
            if is_rescue and "doi" in extracted:
                fields_to_set["doi"] = extracted["doi"]
                verdict = "ATO->COMPLETE-PUBMED-MATCH-DOI-RESCUE"
            else:
                verdict = "ATO->COMPLETE-PUBMED-MATCH"
            fields_to_set["metadata_quality"] = "COMPLETE"

        outcomes.append({
            "ref_id": r["ref_id"], "verdict": verdict, "reasons": reasons,
            "pubtype": pubtype, "fields_to_set": fields_to_set, "is_rescue": is_rescue,
        })
        print(f"  -> {verdict}  ({len(fields_to_set)} fields)", file=sys.stderr)

    from collections import Counter
    cnt = Counter(o["verdict"] for o in outcomes)
    print("\n# === SUMMARY ===", file=sys.stderr)
    for k, v in sorted(cnt.items()):
        print(f"# {k}: {v}", file=sys.stderr)

    print(json.dumps(outcomes, indent=2, default=str))


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    main(limit=limit)
