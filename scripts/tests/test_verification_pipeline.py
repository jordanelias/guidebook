#!/usr/bin/env python3
"""V1.2 test suite — maximized metadata enrichment.
Tests cover: new columns, ORCID, full author lists, Phase 4 DOI-lookup, COMPLETE promotion.
"""
import sqlite3, shutil, sys, traceback, importlib.util, os

DB_ORIG = "/home/claude/live-v1.db"
DB_TEST = "/tmp/v12-test.db"

results = []
def record(tid, name, passed, details="", error=""):
    results.append(passed)
    sym = "✓" if passed else "✗"
    print(f"  [{sym}] {tid}: {name}")
    if not passed and error: print(f"      ERR: {error[:120]}")
    if details: print(f"      {details}")

def fresh():
    shutil.copy(DB_ORIG, DB_TEST)
    conn = sqlite3.connect(DB_TEST)
    conn.row_factory = sqlite3.Row
    return conn

def read(conn, ref_id):
    return dict(conn.execute("SELECT * FROM evidence_sources WHERE ref_id=?", (ref_id,)).fetchone() or {})

spec = importlib.util.spec_from_file_location("resolve_dois", "/home/claude/resolve_dois_v1.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

print("=" * 70)
print("V1.2 MAXIMIZED ENRICHMENT — TEST SUITE")
print("=" * 70)

# ── A: Schema additions ─────────────────────────────────────────────────────
print("\n[A] Schema additions for maximized metadata")
conn = fresh()
required_cols = ['pages','pub_month','language','subtype','citation_count']
es_cols = [r[1] for r in conn.execute("PRAGMA table_info(evidence_sources)")]
missing = [c for c in required_cols if c not in es_cols]
record("A01", "New evidence_sources columns added (pages, pub_month, language, subtype, citation_count)",
       not missing,
       details=f"Missing: {missing}" if missing else f"All 5 present; total cols: {len(es_cols)}")

pr_cols = [r[1] for r in conn.execute("PRAGMA table_info(pipeline_runs)")]
p4_cols = ['phase_4_enriched','phase_4_complete','phase_4_transient','metadata_complete_before','metadata_complete_after']
missing_p4 = [c for c in p4_cols if c not in pr_cols]
record("A02", "pipeline_runs has Phase 4 + metadata_complete tracking columns",
       not missing_p4,
       details=f"Missing: {missing_p4}" if missing_p4 else f"All 5 present; total cols: {len(pr_cols)}")

# ── B: enrich_from_crossref — new fields populated ──────────────────────────
print("\n[B] enrich_from_crossref populates new fields")

cr_full = {
    "DOI": "10.1234/test-full",
    "title": ["Comprehensive test paper title"],
    "container-title": ["Journal of Testing"],
    "ISSN": ["1234-5678"],
    "volume": "42",
    "issue": "7",
    "page": "100-115",
    "publisher": "Test Publisher Ltd",
    "issued": {"date-parts": [[2022, 6]]},
    "language": "en",
    "subtype": "review-article",
    "is-referenced-by-count": 25,
    "author": [
        {"family": "Smith", "given": "Jane", "ORCID": "https://orcid.org/0000-0001-2345-6789"},
        {"family": "Jones", "given": "Bob"},
    ],
}

# B01: pages, pub_month, language, subtype, citation_count populated
try:
    conn = fresh()
    rid = "REF-TEST-B01"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,doi,is_corporate_primary) VALUES (?,?,?,?)""",
        (rid,"journal_article","10.1234/test-full",0))
    conn.commit()
    mod.enrich_from_crossref(conn, rid, cr_full)
    conn.commit()
    a = read(conn, rid)
    checks = {
        "pages='100-115'":     a.get("pages") == "100-115",
        "pub_month=6":         a.get("pub_month") == 6,
        "language='en'":       a.get("language") == "en",
        "subtype set":         a.get("subtype") == "review-article",
        "citation_count=25":   a.get("citation_count") == 25,
        "publisher set":       a.get("publisher") == "Test Publisher Ltd",
        "issn set":            a.get("issn") == "1234-5678",
    }
    record("B01", "All 5 new fields populated correctly from CrossRef",
           all(checks.values()),
           details=str({k: v for k, v in checks.items() if not v} or "all populated"))
except Exception as e:
    record("B01", "New fields populated", False, error=traceback.format_exc(limit=2))

# B02: pub_month falls back to NULL when not in CrossRef response
try:
    conn = fresh()
    rid = "REF-TEST-B02"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,doi,is_corporate_primary) VALUES (?,?,?,?)""",
        (rid,"journal_article","10.x/y",0))
    conn.commit()
    no_month = {"DOI":"10.x/y","title":["T"],"issued":{"date-parts":[[2020]]}}  # year only
    mod.enrich_from_crossref(conn, rid, no_month)
    conn.commit()
    a = read(conn, rid)
    record("B02", "pub_month NULL when CrossRef only has year",
           a.get("pub_year") == 2020 and a.get("pub_month") is None)
except Exception as e:
    record("B02", "pub_month NULL handling", False, error=traceback.format_exc(limit=2))

# B03: article-number used as pages fallback when page absent
try:
    conn = fresh()
    rid = "REF-TEST-B03"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,doi,is_corporate_primary) VALUES (?,?,?,?)""",
        (rid,"journal_article","10.x/article",0))
    conn.commit()
    article = {"DOI":"10.x/article","title":["T"],"article-number":"e12345","issued":{"date-parts":[[2021]]}}
    mod.enrich_from_crossref(conn, rid, article)
    conn.commit()
    record("B03", "article-number used as pages when page field absent",
           read(conn, rid).get("pages") == "e12345")
except Exception as e:
    record("B03", "article-number fallback", False, error=traceback.format_exc(limit=2))

# ── C: Author enrichment with ORCID ─────────────────────────────────────────
print("\n[C] Author enrichment with ORCID")

# C01: Full author list with ORCID written when author_count_is_complete=0
try:
    conn = fresh()
    rid = "REF-TEST-C01"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,doi,first_author_last,author_count_is_complete,is_corporate_primary)
        VALUES (?,?,?,?,?,?)""", (rid,"journal_article","10.x/z","Smith",0,0))
    conn.execute("""INSERT INTO evidence_source_authors
        (ref_id,position,last_name,first_name,is_corporate,created_at,created_by_session)
        VALUES (?,1,?,?,0,?,?)""", (rid,"Smith","Jane","2026-01-01","test"))
    conn.commit()
    mod.enrich_from_crossref(conn, rid, cr_full)
    conn.commit()
    authors = list(conn.execute(
        "SELECT position, last_name, first_name, orcid FROM evidence_source_authors WHERE ref_id=? ORDER BY position",
        (rid,)).fetchall())
    record("C01", "Full author list replaced; ORCID populated when present",
           len(authors) == 2 and
           authors[0]["orcid"] == "0000-0001-2345-6789" and
           authors[1]["orcid"] is None,
           details=f"{len(authors)} authors; first ORCID={authors[0]['orcid'] if authors else None}")
except Exception as e:
    record("C01", "ORCID population", False, error=traceback.format_exc(limit=2))

# C02: Author list NOT replaced when author_count_is_complete=1
try:
    conn = fresh()
    rid = "REF-TEST-C02"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,doi,first_author_last,author_count_is_complete,is_corporate_primary)
        VALUES (?,?,?,?,?,?)""", (rid,"journal_article","10.x/aa","Anderson",1,0))
    conn.execute("""INSERT INTO evidence_source_authors
        (ref_id,position,last_name,first_name,is_corporate,created_at,created_by_session)
        VALUES (?,1,?,?,0,?,?)""", (rid,"Anderson","Alice","2026-01-01","manual"))
    conn.commit()
    mod.enrich_from_crossref(conn, rid, cr_full)
    conn.commit()
    authors = list(conn.execute(
        "SELECT last_name FROM evidence_source_authors WHERE ref_id=?", (rid,)).fetchall())
    record("C02", "Manually-curated complete author list NOT replaced",
           len(authors) == 1 and authors[0]["last_name"] == "Anderson",
           details=f"Authors: {[a['last_name'] for a in authors]}")
except Exception as e:
    record("C02", "Manual list preserved", False, error=traceback.format_exc(limit=2))

# C03: ORCID stripped of orcid.org/ prefix
try:
    conn = fresh()
    rid = "REF-TEST-C03"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,doi,first_author_last,is_corporate_primary)
        VALUES (?,?,?,?,?)""", (rid,"journal_article","10.x/cc","Smith",0))
    conn.commit()
    item = {"DOI":"10.x/cc","title":["T"],"issued":{"date-parts":[[2021]]},
            "author":[{"family":"Smith","given":"J","ORCID":"https://orcid.org/0000-0002-1234-5678"}]}
    mod.enrich_from_crossref(conn, rid, item)
    conn.commit()
    orcid = conn.execute("SELECT orcid FROM evidence_source_authors WHERE ref_id=?", (rid,)).fetchone()[0]
    record("C03", "ORCID URL prefix stripped (stores plain identifier)",
           orcid == "0000-0002-1234-5678",
           details=f"orcid={orcid}")
except Exception as e:
    record("C03", "ORCID prefix strip", False, error=traceback.format_exc(limit=2))

# ── D: crossref_doi_lookup function ─────────────────────────────────────────
print("\n[D] CrossRef DOI lookup (Phase 4 helper)")

# D01: Function returns dict on success, None on 404
try:
    orig_fetch = mod.fetch_json
    mod.fetch_json = lambda url, timeout=15: {"message": {"DOI": "10.x/test", "title": ["T"]}}
    item = mod.crossref_doi_lookup("10.x/test")
    mod.fetch_json = orig_fetch
    record("D01", "crossref_doi_lookup returns item dict on success",
           isinstance(item, dict) and item.get("DOI") == "10.x/test")
except Exception as e:
    mod.fetch_json = orig_fetch
    record("D01", "crossref_doi_lookup success", False, error=traceback.format_exc(limit=2))

# D02: Returns None on transient error (HTTPError)
try:
    import urllib.error
    orig_fetch = mod.fetch_json
    def raise_403(url, timeout=15):
        raise urllib.error.HTTPError(url, 403, "Forbidden", {}, None)
    mod.fetch_json = raise_403
    item = mod.crossref_doi_lookup("10.x/test")
    mod.fetch_json = orig_fetch
    record("D02", "crossref_doi_lookup returns None on transient 403",
           item is None)
except Exception as e:
    mod.fetch_json = orig_fetch
    record("D02", "transient handling", False, error=traceback.format_exc(limit=2))

# ── E: Phase 4 candidate selection ──────────────────────────────────────────
print("\n[E] Phase 4 candidate pool")

# E01: Candidate query selects rows with DOI but incomplete enrichment
try:
    conn = fresh()
    # Force a candidate by clearing some fields
    rid = "REF-TEST-E01"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,doi,source_type,pub_title,journal_abbrev,volume,language,pages,citation_count)
        VALUES (?,?,?,?,NULL,NULL,NULL,NULL,NULL)""",
        (rid,"10.x/e01","journal_article","T"))
    conn.commit()
    n = conn.execute(f"""
        SELECT COUNT(*) FROM evidence_sources
        WHERE ref_id=?
        AND doi IS NOT NULL AND doi != ''
        AND (journal_abbrev IS NULL OR journal_abbrev = ''
             OR volume IS NULL OR language IS NULL OR language = ''
             OR pages IS NULL OR pages = '' OR citation_count IS NULL)
        AND source_type IN ('journal_article','book','book_chapter','conference_paper',
                            'thesis','primary_research','case_study','standard')""",
        (rid,)).fetchone()[0]
    record("E01", "Phase 4 query selects rows with DOI but incomplete metadata",
           n == 1)
except Exception as e:
    record("E01", "Phase 4 candidate query", False, error=traceback.format_exc(limit=2))

# E02: Fully-enriched rows NOT selected as candidates
try:
    conn = fresh()
    rid = "REF-TEST-E02"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,doi,source_type,pub_title,journal_abbrev,volume,language,pages,citation_count)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        (rid,"10.x/e02","journal_article","T","Journal","1","en","100-110",5))
    conn.commit()
    n = conn.execute(f"""
        SELECT COUNT(*) FROM evidence_sources
        WHERE ref_id=?
        AND doi IS NOT NULL AND doi != ''
        AND (journal_abbrev IS NULL OR journal_abbrev = ''
             OR volume IS NULL OR language IS NULL OR language = ''
             OR pages IS NULL OR pages = '' OR citation_count IS NULL)""",
        (rid,)).fetchone()[0]
    record("E02", "Fully-enriched rows excluded from candidate pool",
           n == 0)
except Exception as e:
    record("E02", "fully enriched exclusion", False, error=traceback.format_exc(limit=2))

# ── F: COMPLETE promotion at scale ──────────────────────────────────────────
print("\n[F] COMPLETE promotion correctness")

# F01: metadata_quality promoted from AUTHOR-TITLE-ONLY to COMPLETE
try:
    conn = fresh()
    rid = "REF-TEST-F01"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,doi,first_author_last,is_corporate_primary,metadata_quality,
         author_count_is_complete)
        VALUES (?,?,?,?,?,?,?)""",
        (rid,"journal_article","10.x/f01","Smith",0,"AUTHOR-TITLE-ONLY",1))
    conn.commit()
    mod.enrich_from_crossref(conn, rid, cr_full)
    conn.commit()
    record("F01", "metadata_quality promoted AUTHOR-TITLE-ONLY → COMPLETE after enrichment",
           read(conn, rid).get("metadata_quality") == "COMPLETE")
except Exception as e:
    record("F01", "COMPLETE promotion", False, error=traceback.format_exc(limit=2))

# F02: Already-COMPLETE rows stay COMPLETE
try:
    conn = fresh()
    rid = "REF-TEST-F02"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,doi,first_author_last,metadata_quality,is_corporate_primary)
        VALUES (?,?,?,?,?,?)""",
        (rid,"journal_article","10.x/f02","Smith","COMPLETE",0))
    conn.commit()
    mod.enrich_from_crossref(conn, rid, cr_full)
    conn.commit()
    record("F02", "Already-COMPLETE rows stay COMPLETE (no downgrade)",
           read(conn, rid).get("metadata_quality") == "COMPLETE")
except Exception as e:
    record("F02", "no downgrade", False, error=traceback.format_exc(limit=2))

# ── G: Live state — Phase 4 enrichment produced real results ────────────────
print("\n[G] Live state — Phase 4 production results")

# G01: Live DB now has populated language column
try:
    conn = fresh()
    n_lang = conn.execute("SELECT COUNT(*) FROM evidence_sources WHERE language IS NOT NULL").fetchone()[0]
    record("G01", "Live DB has language populated on ≥50 sources after Phase 4 production run",
           n_lang >= 50,
           details=f"language populated: {n_lang}")
except Exception as e:
    record("G01", "live language state", False, error=traceback.format_exc(limit=2))

# G02: Live DB has ORCID populated
try:
    conn = fresh()
    n_orcid = conn.execute("SELECT COUNT(*) FROM evidence_source_authors WHERE orcid IS NOT NULL AND orcid != ''").fetchone()[0]
    record("G02", "Live DB has ORCID populated on ≥30 authors (was 0)",
           n_orcid >= 30,
           details=f"ORCID populated: {n_orcid}")
except Exception as e:
    record("G02", "live ORCID state", False, error=traceback.format_exc(limit=2))

# G03: COMPLETE count increased substantially
try:
    conn = fresh()
    n_complete = conn.execute("SELECT COUNT(*) FROM evidence_sources WHERE metadata_quality='COMPLETE'").fetchone()[0]
    record("G03", "COMPLETE metadata count ≥ 100 (was 67 pre-V1.2)",
           n_complete >= 100,
           details=f"COMPLETE: {n_complete}")
except Exception as e:
    record("G03", "live COMPLETE state", False, error=traceback.format_exc(limit=2))

# G04: pipeline_runs has Phase 4 metrics recorded
try:
    conn = fresh()
    row = conn.execute(
        "SELECT * FROM pipeline_runs ORDER BY started_at DESC LIMIT 1"
    ).fetchone()
    if row:
        d = dict(row)
        record("G04", "Most recent pipeline_runs record includes Phase 4 metrics",
               "phase_4_enriched" in d and d.get("phase_4_enriched") is not None,
               details=f"phase_4_enriched={d.get('phase_4_enriched')} newly_complete={d.get('phase_4_complete')}")
    else:
        record("G04", "Phase 4 metrics in pipeline_runs", False, error="no pipeline_runs records")
except Exception as e:
    record("G04", "pipeline_runs Phase 4 record", False, error=traceback.format_exc(limit=2))

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
total = len(results)
passed = sum(results)
print(f"RESULTS: {passed}/{total} tests passed")
if passed < total:
    print(f"FAILED: {total - passed} tests")
print("=" * 70)
sys.exit(0 if passed == total else 1)
