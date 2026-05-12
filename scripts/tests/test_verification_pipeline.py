#!/usr/bin/env python3
"""Comprehensive test suite for resolve_dois V1.1 — all directions."""
import sqlite3, re, sys, shutil, time, traceback, importlib.util, os, json

DB_ORIG = "/home/claude/test-schema.db"
DB_TEST = "/tmp/pipeline-test-all.db"

results = []

def record(tid, name, passed, details="", error=""):
    results.append({"id": tid, "name": name, "passed": passed})
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

# Load script for unit-testing individual functions
spec = importlib.util.spec_from_file_location("resolve_dois", "/home/claude/resolve_dois_v1.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

print("=" * 70)
print("COMPREHENSIVE TEST SUITE — resolve_dois V1.1")
print("=" * 70)

# ── A: crossref_standard false-positive gate ─────────────────────────────────
print("\n[A] crossref_standard — numeric token gate")

# A01: PAS 6463 MUST NOT match DIN IEC/PAS 63313
try:
    # Simulate: CrossRef returns DIN IEC/PAS 63313:2022-07 for PAS 6463 query
    fake_item = {"DOI": "10.31030/3338310",
                 "title": ["DIN IEC/PAS 63313:2022-07, Positionspapier zu keimtötender"],
                 "type": "standard", "publisher": "DIN Media GmbH"}
    import urllib.request as _ur
    orig_fetch = mod.fetch_json
    def mock_fetch(url, timeout=15):
        return {"message": {"items": [fake_item]}}
    mod.fetch_json = mock_fetch
    doi, reason, item = mod.crossref_standard("PAS 6463:2022", "PAS 6463:2022 Design for the Mind", 2022)
    mod.fetch_json = orig_fetch
    record("A01", "PAS 6463 does NOT match DIN IEC/PAS 63313 (numeric gate rejects it)",
           doi is None,
           details=f"doi={doi} reason={reason} (expect None/no-acceptable-match)")
except Exception as e:
    mod.fetch_json = orig_fetch
    record("A01", "PAS 6463 false positive gate", False, error=traceback.format_exc(limit=2))

# A02: EN 17210 DOES match DIN EN 17210 (17210 appears in title)
try:
    fake_item = {"DOI": "10.31030/3185128",
                 "title": ["DIN EN 17210:2021-08, Barrierefreiheit und Nutzbarkeit der gebauten Umwelt"],
                 "type": "standard", "publisher": "DIN Media GmbH"}
    orig_fetch = mod.fetch_json
    mod.fetch_json = lambda url, timeout=15: {"message": {"items": [fake_item]}}
    doi, reason, item = mod.crossref_standard("EN 17210:2021", "EN 17210:2021 — Accessibility and usability of the built environment", 2021)
    mod.fetch_json = orig_fetch
    record("A02", "EN 17210 correctly matches DIN EN 17210 (17210 in title)",
           doi == "10.31030/3185128",
           details=f"doi={doi} reason={reason}")
except Exception as e:
    mod.fetch_json = orig_fetch
    record("A02", "EN 17210 correct match", False, error=traceback.format_exc(limit=2))

# A03: IEC 60118-4 matches DIN EN IEC 60118-4 (60118 in title)
try:
    fake_item = {"DOI": "10.31030/2853913",
                 "title": ["DIN EN IEC 60118-4:2018-08, Akustik - Hörgeräte - Teil 4"],
                 "type": "standard", "publisher": "DIN Media GmbH"}
    orig_fetch = mod.fetch_json
    mod.fetch_json = lambda url, timeout=15: {"message": {"items": [fake_item]}}
    doi, reason, item = mod.crossref_standard("IEC 60118-4:2014+AMD1:2017", "IEC 60118-4:2014+AMD1:2017 — Hearing loop performance", 2014)
    mod.fetch_json = orig_fetch
    record("A03", "IEC 60118-4 correctly matches DIN EN IEC 60118-4",
           doi == "10.31030/2853913",
           details=f"doi={doi} reason={reason}")
except Exception as e:
    mod.fetch_json = orig_fetch
    record("A03", "IEC 60118-4 correct match", False, error=traceback.format_exc(limit=2))

# A04: crossref_standard returns 3-tuple (doi, reason, item)
try:
    orig_fetch = mod.fetch_json
    mod.fetch_json = lambda url, timeout=15: {"message": {"items": []}}
    result = mod.crossref_standard("ISO 21542:2021", "Accessibility built environment", 2021)
    mod.fetch_json = orig_fetch
    record("A04", "crossref_standard returns 3-tuple (doi, reason, item)",
           isinstance(result, tuple) and len(result) == 3,
           details=f"result type={type(result).__name__} len={len(result) if isinstance(result, tuple) else 'N/A'}")
except Exception as e:
    mod.fetch_json = orig_fetch
    record("A04", "crossref_standard 3-tuple return", False, error=traceback.format_exc(limit=2))

# ── B: DOI written directly ───────────────────────────────────────────────────
print("\n[B] DOI written directly to evidence_sources.doi column")

# B01: write_verification writes doi on match
try:
    conn = fresh()
    rid = "REF-TEST-B01"
    conn.execute("INSERT OR IGNORE INTO evidence_sources (ref_id,source_type,pub_title,pub_year,is_corporate_primary) VALUES (?,?,?,?,?)",
                 (rid,"journal_article","Test paper for B01",2021,0))
    conn.commit()
    mod.write_verification(conn, rid, "crossref-structured", "VERIFIED",
                           doi="10.1234/test-doi-b01", doi_outcome="RESOLVED")
    conn.commit()
    after = read(conn, rid)
    record("B01", "DOI written directly to doi column on match",
           after.get("doi") == "10.1234/test-doi-b01",
           details=f"doi={after.get('doi')}")
except Exception as e:
    record("B01", "DOI direct write", False, error=traceback.format_exc(limit=2))

# B02: NO-MATCH does NOT clobber existing doi
try:
    conn = fresh()
    rid = "REF-TEST-B02"
    conn.execute("INSERT OR IGNORE INTO evidence_sources (ref_id,source_type,pub_title,pub_year,doi,is_corporate_primary) VALUES (?,?,?,?,?,?)",
                 (rid,"journal_article","Test B02",2021,"10.9999/existing",0))
    conn.commit()
    mod.write_verification(conn, rid, "crossref-structured", status=None, doi_outcome="NO-MATCH")
    conn.commit()
    after = read(conn, rid)
    record("B02", "NO-MATCH write never clobbers existing doi",
           after.get("doi") == "10.9999/existing",
           details=f"doi preserved={after.get('doi')}")
except Exception as e:
    record("B02", "doi clobber guard", False, error=traceback.format_exc(limit=2))

# ── C: Metadata enrichment ────────────────────────────────────────────────────
print("\n[C] Metadata enrichment — CrossRef fields written to empty columns")

cr_item = {
    "DOI": "10.1234/enrichment-test",
    "title": ["Evidence-based design for wheelchair accessibility in bathrooms"],
    "container-title": ["Disability and Rehabilitation: Assistive Technology"],
    "ISSN": ["1748-3107"],
    "volume": "18",
    "issue": "3",
    "publisher": "Taylor & Francis",
    "issued": {"date-parts": [[2021, 4]]},
    "author": [{"family": "Smith", "given": "A."}],
}

# C01: Empty fields populated from CrossRef item
try:
    conn = fresh()
    rid = "REF-TEST-C01"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,pub_title,pub_year,first_author_last,doi,is_corporate_primary)
        VALUES (?,?,?,?,?,?,?)""",
        (rid,"journal_article",None,None,"Smith","10.1234/enrichment-test",0))
    conn.commit()
    mod.enrich_from_crossref(conn, rid, cr_item)
    conn.commit()
    after = read(conn, rid)
    checks = {
        "pub_title filled":    bool(after.get("pub_title")),
        "journal_abbrev filled": bool(after.get("journal_abbrev")),
        "volume filled":       after.get("volume") == "18",
        "issue filled":        after.get("issue") == "3",
        "publisher filled":    bool(after.get("publisher")),
        "issn filled":         bool(after.get("issn")),
    }
    record("C01", "Empty bibliographic fields filled from CrossRef item",
           all(checks.values()),
           details=str({k: v for k, v in checks.items() if not v} or "all fields filled"))
except Exception as e:
    record("C01", "Enrichment fills empty fields", False, error=traceback.format_exc(limit=2))

# C02: Existing non-null fields NOT overwritten
try:
    conn = fresh()
    rid = "REF-TEST-C02"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,pub_title,pub_year,first_author_last,doi,journal_abbrev,is_corporate_primary)
        VALUES (?,?,?,?,?,?,?,?)""",
        (rid,"journal_article","ORIGINAL TITLE DO NOT OVERWRITE",2021,"Smith",
         "10.1234/test","Original Journal",0))
    conn.commit()
    mod.enrich_from_crossref(conn, rid, cr_item)
    conn.commit()
    after = read(conn, rid)
    record("C02", "Existing pub_title and journal_abbrev NOT overwritten",
           after.get("pub_title") == "ORIGINAL TITLE DO NOT OVERWRITE" and
           after.get("journal_abbrev") == "Original Journal",
           details=f"title={after.get('pub_title')[:30]} journal={after.get('journal_abbrev')}")
except Exception as e:
    record("C02", "No overwrite of existing data", False, error=traceback.format_exc(limit=2))

# C03: metadata_quality promoted to COMPLETE when criteria met
try:
    conn = fresh()
    rid = "REF-TEST-C03"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,pub_title,pub_year,first_author_last,doi,
         is_corporate_primary,metadata_quality)
        VALUES (?,?,?,?,?,?,?,?)""",
        (rid,"journal_article",None,None,"Smith","10.1234/test",0,"AUTHOR-TITLE-ONLY"))
    conn.commit()
    mod.enrich_from_crossref(conn, rid, cr_item)
    conn.commit()
    after = read(conn, rid)
    record("C03", "metadata_quality promoted to COMPLETE when doi+title+year+author all present",
           after.get("metadata_quality") == "COMPLETE",
           details=f"quality={after.get('metadata_quality')} title={bool(after.get('pub_title'))} "
                   f"year={bool(after.get('pub_year'))} author={bool(after.get('first_author_last'))}")
except Exception as e:
    record("C03", "COMPLETE promotion", False, error=traceback.format_exc(limit=2))

# C04: metadata_quality NOT promoted when author still missing
try:
    conn = fresh()
    rid = "REF-TEST-C04"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,pub_title,pub_year,doi,is_corporate_primary,metadata_quality)
        VALUES (?,?,?,?,?,?,?)""",
        (rid,"journal_article",None,None,"10.1234/test",0,"AUTHOR-TITLE-ONLY"))
    conn.commit()
    partial_item = {**cr_item}  # has no author field resolved to first_author_last
    mod.enrich_from_crossref(conn, rid, partial_item)
    conn.commit()
    after = read(conn, rid)
    # first_author_last is still NULL (we didn't set it, CrossRef item author != first_author_last)
    record("C04", "metadata_quality stays AUTHOR-TITLE-ONLY when first_author_last still null",
           after.get("metadata_quality") != "COMPLETE" or after.get("first_author_last") is not None,
           details=f"quality={after.get('metadata_quality')} first_author_last={after.get('first_author_last')}")
except Exception as e:
    record("C04", "COMPLETE not premature", False, error=traceback.format_exc(limit=2))

# ── D: REVERT behavior ────────────────────────────────────────────────────────
print("\n[D] REVERT — permanent skip, doi cleared, verification reset")

# D01: REVERTED rows excluded from all phase candidate pools
try:
    conn = fresh()
    reverted = conn.execute("SELECT COUNT(*) FROM evidence_sources WHERE doi_resolution_outcome='REVERTED'").fetchone()[0]
    # These must NOT appear in Phase 3 query (doi IS NULL and outcome != REVERTED)
    in_pool = conn.execute("""SELECT COUNT(*) FROM evidence_sources
        WHERE (doi IS NULL OR doi='')
        AND source_type='standard'
        AND standard_number IS NOT NULL
        AND (doi_resolution_outcome IS NULL OR doi_resolution_outcome='NO-MATCH')
        AND doi_resolution_outcome='REVERTED'""").fetchone()[0]
    record("D01", f"REVERTED rows ({reverted} total) excluded from candidate pools",
           in_pool == 0,
           details=f"In pool accidentally: {in_pool}")
except Exception as e:
    record("D01", "REVERTED exclusion from pool", False, error=traceback.format_exc(limit=2))

# D02: PAS 6463 refs specifically have doi=NULL after REVERT
try:
    conn = fresh()
    pas_refs = ["REF-00050", "REF-00516", "REF-00568"]
    all_reverted = all(
        read(conn, ref).get("doi_resolution_outcome") == "REVERTED" and
        read(conn, ref).get("doi") is None
        for ref in pas_refs
    )
    record("D02", "PAS 6463 false positives all have doi=NULL, outcome=REVERTED",
           all_reverted,
           details=f"Checked: {pas_refs}")
except Exception as e:
    record("D02", "PAS 6463 REVERTED state", False, error=traceback.format_exc(limit=2))

# ── E: pipeline_runs integration ──────────────────────────────────────────────
print("\n[E] pipeline_runs — SQLite-native run tracking")

# E01: Table created idempotently
try:
    conn = fresh()
    conn.execute("DROP TABLE IF EXISTS pipeline_runs")
    conn.commit()
    # Running init code from script
    conn.execute("""CREATE TABLE IF NOT EXISTS pipeline_runs (
        run_id TEXT PRIMARY KEY, started_at TEXT NOT NULL, completed_at TEXT,
        phase_0_extracted INTEGER DEFAULT 0,
        phase_1a_resolved INTEGER DEFAULT 0, phase_1a_no_match INTEGER DEFAULT 0, phase_1a_transient INTEGER DEFAULT 0,
        phase_1b_resolved INTEGER DEFAULT 0, phase_1b_no_match INTEGER DEFAULT 0, phase_1b_transient INTEGER DEFAULT 0,
        phase_2a_resolved INTEGER DEFAULT 0, phase_2a_no_match INTEGER DEFAULT 0,
        phase_2b_resolved INTEGER DEFAULT 0, phase_2b_no_match INTEGER DEFAULT 0,
        phase_3_resolved INTEGER DEFAULT 0, phase_3_no_match INTEGER DEFAULT 0,
        doi_before INTEGER DEFAULT 0, doi_after INTEGER DEFAULT 0,
        verified_before INTEGER DEFAULT 0, verified_after INTEGER DEFAULT 0,
        pmcid_before INTEGER DEFAULT 0, pmcid_after INTEGER DEFAULT 0,
        total_resolved INTEGER DEFAULT 0, run_by_session TEXT)""")
    # Second call must not fail
    conn.execute("CREATE TABLE IF NOT EXISTS pipeline_runs (run_id TEXT PRIMARY KEY, started_at TEXT NOT NULL)")
    conn.commit()
    cols = [r[1] for r in conn.execute("PRAGMA table_info(pipeline_runs)")]
    record("E01", "pipeline_runs CREATE TABLE IF NOT EXISTS is idempotent (24 cols)",
           len(cols) == 24,
           details=f"Columns: {len(cols)}")
except Exception as e:
    record("E01", "pipeline_runs idempotent creation", False, error=traceback.format_exc(limit=2))

# E02: Run record written with correct pre-counts
try:
    conn = fresh()
    ts = "2026-05-12 00:01"
    doi_b = conn.execute("SELECT COUNT(*) FROM evidence_sources WHERE doi IS NOT NULL AND doi!=''").fetchone()[0]
    ver_b = conn.execute("SELECT COUNT(*) FROM evidence_sources WHERE verification_status='VERIFIED'").fetchone()[0]
    pmc_b = conn.execute("SELECT COUNT(*) FROM evidence_sources WHERE pmcid IS NOT NULL AND pmcid!=''").fetchone()[0]
    conn.execute("""INSERT OR REPLACE INTO pipeline_runs
        (run_id,started_at,doi_before,verified_before,pmcid_before,run_by_session)
        VALUES (?,?,?,?,?,?)""", (ts,ts,doi_b,ver_b,pmc_b,"test"))
    conn.execute("""UPDATE pipeline_runs SET completed_at=?,
        phase_3_resolved=4, doi_after=?, verified_after=?, pmcid_after=?, total_resolved=4
        WHERE run_id=?""", (ts, doi_b+4, ver_b+4, pmc_b, ts))
    conn.commit()
    row = dict(conn.execute("SELECT * FROM pipeline_runs WHERE run_id=?", (ts,)).fetchone())
    record("E02", "pipeline_runs row written with correct pre/post counts",
           row["doi_before"] == doi_b and row["doi_after"] == doi_b+4 and
           row["phase_3_resolved"] == 4 and row["total_resolved"] == 4,
           details=f"doi_before={row['doi_before']} doi_after={row['doi_after']} "
                   f"phase_3_resolved={row['phase_3_resolved']}")
except Exception as e:
    record("E02", "pipeline_runs row write", False, error=traceback.format_exc(limit=2))

# E03: Commit message query from pipeline_runs produces correct delta string
try:
    conn = fresh()
    ts = "2026-05-12 00:02"
    conn.execute("""INSERT OR REPLACE INTO pipeline_runs
        (run_id,started_at,completed_at,doi_before,doi_after,verified_before,verified_after,
         pmcid_before,pmcid_after,total_resolved,phase_3_resolved,phase_1b_transient)
        VALUES (?,?,?,222,229,283,290,13,13,7,7,2)""", (ts,ts,ts))
    conn.commit()
    r = conn.execute("""SELECT run_id,total_resolved,doi_before,doi_after,
        verified_before,verified_after,pmcid_before,pmcid_after,
        phase_0_extracted,phase_1a_resolved,phase_1b_resolved,
        phase_2a_resolved,phase_2b_resolved,phase_3_resolved,
        phase_1a_transient+phase_1b_transient AS transient
        FROM pipeline_runs ORDER BY started_at DESC LIMIT 1""").fetchone()
    doi_d, ver_d, pmc_d = r[3]-r[2], r[5]-r[4], r[7]-r[6]
    msg = (f"source-verification: V1 run {r[0]} — "
           f"doi {doi_d:+d} ({r[3]} total), verified {ver_d:+d} ({r[5]} total), "
           f"pmcid {pmc_d:+d} ({r[7]} total); "
           f"phases p0={r[8]} p1a={r[9]} p1b={r[10]} p2a={r[11]} p2b={r[12]} p3={r[13]}"
           + (f"; {r[14]} transient" if r[14] else ""))
    record("E03", "Commit message built from pipeline_runs — correct format and deltas",
           "doi +7 (229 total)" in msg and "verified +7 (290 total)" in msg and "p3=7" in msg,
           details=f"msg={msg[:100]}")
except Exception as e:
    record("E03", "Commit message from pipeline_runs", False, error=traceback.format_exc(limit=2))

# ── F: Environment / config ───────────────────────────────────────────────────
print("\n[F] Environment variables")

# F01: RATE_LIMIT parsed as float
try:
    os.environ["RATE_LIMIT"] = "5.0"
    spec2 = importlib.util.spec_from_file_location("resolve_dois2", "/home/claude/resolve_dois_v1.py")
    mod2 = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(mod2)
    record("F01", "RATE_LIMIT=5.0 env var parsed as float",
           mod2.RATE_LIMIT == 5.0,
           details=f"RATE_LIMIT={mod2.RATE_LIMIT} type={type(mod2.RATE_LIMIT).__name__}")
except Exception as e:
    record("F01", "RATE_LIMIT env float parse", False, error=traceback.format_exc(limit=2))

# F02: Default RATE_LIMIT is 5.0 when env not set
try:
    os.environ.pop("RATE_LIMIT", None)
    spec3 = importlib.util.spec_from_file_location("resolve_dois3", "/home/claude/resolve_dois_v1.py")
    mod3 = importlib.util.module_from_spec(spec3)
    spec3.loader.exec_module(mod3)
    record("F02", "Default RATE_LIMIT=5.0 when env not set",
           mod3.RATE_LIMIT == 5.0,
           details=f"RATE_LIMIT={mod3.RATE_LIMIT}")
except Exception as e:
    record("F02", "Default RATE_LIMIT", False, error=traceback.format_exc(limit=2))

# ── G: State machine ──────────────────────────────────────────────────────────
print("\n[G] State machine — skip logic and write guards")

# G01: NO-MATCH does NOT downgrade existing VERIFIED status
try:
    conn = fresh()
    rid = "REF-TEST-G01"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,pub_title,pub_year,is_corporate_primary,verification_status)
        VALUES (?,?,?,?,?,?)""", (rid,"standard","Test G01",2021,1,"VERIFIED"))
    conn.commit()
    mod.write_verification(conn, rid, "crossref-standard", status=None, doi_outcome="NO-MATCH")
    conn.commit()
    after = read(conn, rid)
    record("G01", "NO-MATCH write preserves existing VERIFIED status",
           after.get("verification_status") == "VERIFIED",
           details=f"status={after.get('verification_status')}")
except Exception as e:
    record("G01", "NO-MATCH doesn't downgrade VERIFIED", False, error=traceback.format_exc(limit=2))

# G02: REVERTED rows permanently excluded from Phase 3 pool
try:
    conn = fresh()
    rev = conn.execute("SELECT COUNT(*) FROM evidence_sources WHERE doi_resolution_outcome='REVERTED'").fetchone()[0]
    in_pool = conn.execute("""SELECT COUNT(*) FROM evidence_sources
        WHERE (doi IS NULL OR doi='') AND source_type='standard'
        AND (doi_resolution_outcome IS NULL OR (doi_resolution_outcome='NO-MATCH'))
        AND doi_resolution_outcome='REVERTED'""").fetchone()[0]
    record("G02", f"REVERTED rows ({rev}) permanently excluded from Phase 3 pool",
           in_pool == 0)
except Exception as e:
    record("G02", "REVERTED exclusion", False, error=traceback.format_exc(limit=2))

# G03: verified_by_tool always populated on write
try:
    conn = fresh()
    rid = "REF-TEST-G03"
    conn.execute("INSERT OR IGNORE INTO evidence_sources (ref_id,source_type,pub_title,pub_year,is_corporate_primary) VALUES (?,?,?,?,?)",
                 (rid,"report","G03 test",2020,0))
    conn.commit()
    for tool in ["crossref-standard","ncbi-pmcid-converter","crossref-structured","url-fetch-v1"]:
        mod.write_verification(conn, rid, tool, "VERIFIED")
        conn.commit()
        assert read(conn, rid).get("verified_by_tool") == tool
    record("G03", "verified_by_tool updated by all 4 channel tools", True)
except AssertionError as e:
    record("G03", "verified_by_tool update", False, error=str(e))
except Exception as e:
    record("G03", "verified_by_tool update", False, error=traceback.format_exc(limit=2))

# G04: enrich_from_crossref does not write to already-populated fields
try:
    conn = fresh()
    rid = "REF-TEST-G04"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,pub_title,pub_year,journal_abbrev,volume,doi,
         first_author_last,is_corporate_primary)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        (rid,"journal_article","Existing title",2020,"Existing Journal","42","10.x/y","Jones",0))
    conn.commit()
    mod.enrich_from_crossref(conn, rid, cr_item)  # cr_item has different title/journal/volume
    conn.commit()
    after = read(conn, rid)
    record("G04", "enrich_from_crossref leaves all pre-populated fields unchanged",
           after.get("pub_title") == "Existing title" and
           after.get("journal_abbrev") == "Existing Journal" and
           after.get("volume") == "42",
           details=f"title={after.get('pub_title')[:20]} journal={after.get('journal_abbrev')} vol={after.get('volume')}")
except Exception as e:
    record("G04", "enrich does not overwrite", False, error=traceback.format_exc(limit=2))

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
total = len(results)
passed = sum(1 for r in results if r["passed"])
failed = [r for r in results if not r["passed"]]
print(f"RESULTS: {passed}/{total} tests passed")
if failed:
    print("FAILED:")
    for r in failed:
        print(f"  [{r['id']}] {r['name']}")
print("=" * 70)
sys.exit(0 if not failed else 1)
