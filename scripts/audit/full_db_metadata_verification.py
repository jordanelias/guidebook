#!/usr/bin/env python3
"""
Full-DB metadata verification audit.

For every evidence_sources row with a DOI or PMID (238 rows as of HEAD
36cd080a), re-fetch canonical metadata from Crossref / NCBI EUtils and
compare against stored fields. Surface ALL discrepancies — not just the
classifier-strict ones the rehab probes flagged.

Verdict enum:
  CLEAN                    - identifier(s) resolve, all stored fields match canonical
  FIELD-DRIFT              - identifier resolves, minor field updates needed (e.g.,
                             journal_name NULL but canonical has one)
  WRONG-ATTRIBUTION        - identifier resolves to different paper than stored
                             title/author/year describes
  IDENTIFIER-DISAGREE      - DOI and PMID both present but resolve to different papers
  STATUTORY-DEFERRED       - row is statutory; different verification path
  IDENTIFIER-404           - identifier doesn't resolve at registrar
  IDENTIFIER-TRUNCATED     - DOI is publisher-prefix-only fragment
  API-ERROR                - transient API failure; needs retry

Pure audit — emits JSON report, no DB writes. Corrective action is per-class
follow-up migration(s).
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
CROSSREF_BASE = "https://api.crossref.org/works/"
PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
USER_AGENT = "Guidebook-Audit/1.0 (mailto:[email protected])"
CROSSREF_SLEEP = 0.25  # 4 req/s
PUBMED_SLEEP = 0.34    # 3 req/s


def normalize(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def is_doi_truncated(doi):
    """A 'real' DOI has prefix/suffix-with-article-identifier. Truncated DOIs
    are just publisher prefix or publisher+journal stem."""
    if not doi or "/" not in doi:
        return True
    rhs = doi.split("/", 1)[1]
    return len(rhs) < 8 or not re.search(r"[0-9]", rhs)


def crossref_fetch(doi):
    url = CROSSREF_BASE + urllib.parse.quote(doi, safe="")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())["message"], "ok"
    except urllib.error.HTTPError as e:
        return None, f"http_{e.code}"
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
        return None, f"error:{type(e).__name__}"


def pubmed_fetch(pmid):
    url = f"{PUBMED_BASE}?db=pubmed&id={pmid}&retmode=json"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
            rec = data.get("result", {}).get(str(pmid))
            if not rec or rec.get("error"):
                return None, "not-found"
            return rec, "ok"
    except urllib.error.HTTPError as e:
        return None, f"http_{e.code}"
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
        return None, f"error:{type(e).__name__}"


def cr_title(d):
    t = d.get("title") or []
    return t[0] if t else ""


def cr_author(d):
    a = d.get("author") or []
    return a[0].get("family", "") if a else ""


def cr_year(d):
    parts = d.get("issued", {}).get("date-parts", [[None]])
    return parts[0][0] if parts and parts[0] else None


def cr_journal(d):
    c = d.get("container-title") or []
    return c[0] if c else ""


def pm_title(d):
    return d.get("title", "")


def pm_author(d):
    a = d.get("authors") or []
    name = a[0].get("name", "") if a else ""
    return name.rsplit(" ", 1)[0] if " " in name else name


def pm_year(d):
    pd = d.get("pubdate", "")
    m = re.match(r"^(\d{4})", pd)
    return int(m.group(1)) if m else None


def pm_journal(d):
    return d.get("fulljournalname", "") or d.get("source", "")


def pm_doi(d):
    for aid in d.get("articleids", []):
        if aid.get("idtype") == "doi":
            return aid.get("value", "")
    return ""


def compare_field(label, canonical_val, stored_val):
    """Return None if match (or stored is NULL), or a discrepancy string."""
    if not canonical_val:
        return None  # No canonical to compare against
    if stored_val in (None, "", 0):
        return f"{label}-EMPTY: canonical={str(canonical_val)[:60]!r}"
    c, s = normalize(str(canonical_val)), normalize(str(stored_val))
    if label == "title":
        shared = set(c.split()) & set(s.split())
        if len(shared) >= 4 or (len(shared) >= 3 and len(s.split()) <= 5):
            return None
        return f"title-MISMATCH: canonical={str(canonical_val)[:60]!r} stored={str(stored_val)[:60]!r}"
    if label == "year":
        try:
            return None if abs(int(canonical_val) - int(stored_val)) <= 1 else f"year-MISMATCH: canonical={canonical_val} stored={stored_val}"
        except (ValueError, TypeError):
            return None
    if c == s:
        return None
    return f"{label}-MISMATCH: canonical={str(canonical_val)[:60]!r} stored={str(stored_val)[:60]!r}"


def reconcile_doi_pmid(cr_data, pm_data):
    """When both identifiers present, verify they point to the same paper."""
    if not cr_data or not pm_data:
        return None
    issues = []
    # Title: at least 3 shared tokens
    ct, pt = normalize(cr_title(cr_data)), normalize(pm_title(pm_data))
    if ct and pt:
        if len(set(ct.split()) & set(pt.split())) < 3:
            issues.append(f"DOI-PMID-disagree-title: cr={cr_title(cr_data)[:50]!r} pm={pm_title(pm_data)[:50]!r}")
    # Author surname
    ca, pa = normalize(cr_author(cr_data)), normalize(pm_author(pm_data))
    if ca and pa and ca != pa:
        issues.append(f"DOI-PMID-disagree-author: cr={cr_author(cr_data)!r} pm={pm_author(pm_data)!r}")
    # Year ±1
    cy, py = cr_year(cr_data), pm_year(pm_data)
    if cy and py and abs(cy - py) > 1:
        issues.append(f"DOI-PMID-disagree-year: cr={cy} pm={py}")
    # PMID's recorded DOI vs Crossref's queried DOI
    return issues if issues else None


def is_statutory(row):
    return (row["source_type"] == "standard"
            or row["evidence_type"] in ("code", "national_fw")
            or (row["evidence_type"] == "standard_eb" and row["tier"] in (2, 4)))


def audit_row(row):
    """Return (verdict, discrepancies_list, canonical_data_dict)."""
    if is_statutory(row):
        return "STATUTORY-DEFERRED", [], {}

    has_doi = bool(row["doi"])
    has_pmid = bool(row["pmid"])

    if not has_doi and not has_pmid:
        return "NO-IDENTIFIER", ["no DOI or PMID — cannot API-verify"], {}

    if has_doi and is_doi_truncated(row["doi"]):
        if has_pmid:
            # Try PMID path
            pm_data, status = pubmed_fetch(row["pmid"])
            time.sleep(PUBMED_SLEEP)
            if status != "ok" or not pm_data:
                return "IDENTIFIER-TRUNCATED", [f"DOI truncated ({row['doi']!r}); PMID fetch failed ({status})"], {}
            # Use PMID as the canonical source
            return _compare_to_pubmed(row, pm_data, doi_was_truncated=True)
        return "IDENTIFIER-TRUNCATED", [f"DOI truncated ({row['doi']!r}); no PMID for fallback"], {}

    cr_data, cr_status, pm_data, pm_status = None, None, None, None
    if has_doi:
        cr_data, cr_status = crossref_fetch(row["doi"])
        time.sleep(CROSSREF_SLEEP)
    if has_pmid:
        pm_data, pm_status = pubmed_fetch(row["pmid"])
        time.sleep(PUBMED_SLEEP)

    # Identifier resolution failures
    if has_doi and cr_status != "ok":
        if has_pmid and pm_status == "ok":
            return _compare_to_pubmed(row, pm_data, doi_404=True)
        return "IDENTIFIER-404", [f"DOI {row['doi']!r} → {cr_status}; PMID → {pm_status if has_pmid else 'absent'}"], {}
    if has_pmid and pm_status != "ok" and not (has_doi and cr_status == "ok"):
        return "IDENTIFIER-404", [f"PMID {row['pmid']!r} → {pm_status}"], {}

    # If both resolved, check they agree with each other
    if cr_data and pm_data:
        disagree = reconcile_doi_pmid(cr_data, pm_data)
        if disagree:
            return "IDENTIFIER-DISAGREE", disagree, {"cr": _canonical_from_cr(cr_data), "pm": _canonical_from_pm(pm_data)}

    # Compare canonical (use DOI/Crossref as primary if available) against stored
    canonical = cr_data if cr_data else None
    canonical_pm_only = pm_data if not canonical else None

    if canonical:
        return _compare_to_crossref(row, canonical)
    return _compare_to_pubmed(row, canonical_pm_only)


def _canonical_from_cr(cr_data):
    return {
        "title": cr_title(cr_data),
        "author": cr_author(cr_data),
        "year": cr_year(cr_data),
        "journal": cr_journal(cr_data),
        "doi": cr_data.get("DOI"),
    }


def _canonical_from_pm(pm_data):
    return {
        "title": pm_title(pm_data),
        "author": pm_author(pm_data),
        "year": pm_year(pm_data),
        "journal": pm_journal(pm_data),
        "doi": pm_doi(pm_data),
    }


def _compare_to_crossref(row, cr_data):
    discrepancies = []
    canonical = _canonical_from_cr(cr_data)
    for label, c_val, s_val in [
        ("title", canonical["title"], row["pub_title"]),
        ("author", canonical["author"], row["first_author_last"]),
        ("year", canonical["year"], row["pub_year"]),
        ("journal", canonical["journal"], row["journal_name"]),
    ]:
        d = compare_field(label, c_val, s_val)
        if d:
            discrepancies.append(d)

    if not discrepancies:
        return "CLEAN", [], canonical

    # Categorize: wrong-attribution if title AND (author OR year) MISMATCH (not just EMPTY)
    mismatches = [d for d in discrepancies if "-MISMATCH" in d]
    title_mis = any("title-MISMATCH" in d for d in mismatches)
    author_mis = any("author-MISMATCH" in d for d in mismatches)
    year_mis = any("year-MISMATCH" in d for d in mismatches)
    if title_mis and (author_mis or year_mis):
        return "WRONG-ATTRIBUTION", discrepancies, canonical
    if mismatches:
        return "FIELD-DRIFT-WITH-MISMATCH", discrepancies, canonical
    return "FIELD-DRIFT", discrepancies, canonical


def _compare_to_pubmed(row, pm_data, doi_404=False, doi_was_truncated=False):
    discrepancies = []
    canonical = _canonical_from_pm(pm_data)
    for label, c_val, s_val in [
        ("title", canonical["title"], row["pub_title"]),
        ("author", canonical["author"], row["first_author_last"]),
        ("year", canonical["year"], row["pub_year"]),
        ("journal", canonical["journal"], row["journal_name"]),
    ]:
        d = compare_field(label, c_val, s_val)
        if d:
            discrepancies.append(d)
    if doi_404:
        discrepancies.insert(0, "DOI-DID-NOT-RESOLVE — using PMID as canonical")
    if doi_was_truncated:
        discrepancies.insert(0, f"DOI-TRUNCATED ({row['doi']!r}) — using PMID as canonical")
    if not discrepancies or (doi_404 and len(discrepancies) == 1) or (doi_was_truncated and len(discrepancies) == 1):
        if doi_404:
            return "CLEAN-PMID-ONLY-DOI-404", discrepancies, canonical
        if doi_was_truncated:
            return "CLEAN-PMID-DOI-NEEDS-REPLACEMENT", discrepancies, canonical
        return "CLEAN", [], canonical
    mismatches = [d for d in discrepancies if "-MISMATCH" in d]
    title_mis = any("title-MISMATCH" in d for d in mismatches)
    author_mis = any("author-MISMATCH" in d for d in mismatches)
    year_mis = any("year-MISMATCH" in d for d in mismatches)
    if title_mis and (author_mis or year_mis):
        return "WRONG-ATTRIBUTION", discrepancies, canonical
    if mismatches:
        return "FIELD-DRIFT-WITH-MISMATCH", discrepancies, canonical
    return "FIELD-DRIFT", discrepancies, canonical


def main(limit=0):
    import urllib.parse as _up
    globals()["urllib"].parse = _up  # ensure quote() available

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT * FROM evidence_sources
        WHERE (doi IS NOT NULL AND doi != '') OR (pmid IS NOT NULL AND pmid != '')
        ORDER BY ref_id
    """).fetchall()
    print(f"# Cohort: {len(rows)} rows (any identifier)", file=sys.stderr)
    if limit:
        rows = rows[:limit]

    outcomes = []
    for i, r in enumerate(rows):
        verdict, discrepancies, canonical = audit_row(r)
        outcomes.append({
            "ref_id": r["ref_id"],
            "verdict": verdict,
            "stored": {
                "doi": r["doi"],
                "pmid": r["pmid"],
                "first_author_last": r["first_author_last"],
                "pub_year": r["pub_year"],
                "pub_title": (r["pub_title"] or "")[:120],
                "journal_name": r["journal_name"],
                "metadata_quality": r["metadata_quality"],
                "verification_status": r["verification_status"],
                "metadata_integrity_status": r["metadata_integrity_status"],
            },
            "canonical": canonical,
            "discrepancies": discrepancies,
        })
        if (i + 1) % 25 == 0:
            print(f"  [{i+1}/{len(rows)}] last: {r['ref_id']} -> {verdict}", file=sys.stderr)

    from collections import Counter
    cnt = Counter(o["verdict"] for o in outcomes)
    print("\n# === FINAL SUMMARY ===", file=sys.stderr)
    for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
        print(f"#   {k:40s} {v:>4d}", file=sys.stderr)
    print(f"#   TOTAL                                    {len(outcomes):>4d}", file=sys.stderr)

    print(json.dumps(outcomes, indent=2, default=str))


if __name__ == "__main__":
    import urllib.parse  # for quote()
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    main(limit=limit)
