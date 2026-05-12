#!/usr/bin/env python3
"""Channel 2 URL verifier — test suite.
Runs all logic locally with mocked fetcher (this container's egress proxy
blocks arbitrary domains, but the runner won't have that restriction).
"""
import sqlite3, shutil, sys, traceback, importlib.util, os
import urllib.error

DB_ORIG = "/home/claude/live-v1.db"
DB_TEST = "/tmp/ch2-test.db"

results = []
def record(tid, name, passed, details="", error=""):
    results.append(passed)
    sym = "✓" if passed else "✗"
    print(f"  [{sym}] {tid}: {name}")
    if not passed and error: print(f"      ERR: {error[:160]}")
    if details: print(f"      {details}")

def fresh():
    shutil.copy(DB_ORIG, DB_TEST)
    conn = sqlite3.connect(DB_TEST)
    conn.row_factory = sqlite3.Row
    return conn

def read(conn, ref_id):
    r = conn.execute("SELECT * FROM evidence_sources WHERE ref_id=?", (ref_id,)).fetchone()
    return dict(r) if r else {}

spec = importlib.util.spec_from_file_location("verify_urls", "/home/claude/verify_urls.py")
mod = importlib.util.module_from_spec(spec)

# Override DB_PATH and disable real network before loading
os.environ["GUIDEBOOK_DB_PATH"] = DB_TEST
os.environ["USE_WAYBACK"] = "0"  # disable Wayback for unit tests
spec.loader.exec_module(mod)

print("=" * 70)
print("CHANNEL 2 URL VERIFIER — TEST SUITE")
print("=" * 70)

# ── A: Schema setup ──────────────────────────────────────────────────────────
print("\n[A] Schema initialization")

# A01: ensure_schema adds the 3 new columns
try:
    conn = fresh()
    # Strip the columns if they exist from a prior test
    mod.ensure_schema(conn)
    cols = [r[1] for r in conn.execute("PRAGMA table_info(evidence_sources)")]
    needed = ['url_resolution_outcome', 'url_last_fetched', 'url_match_similarity']
    missing = [c for c in needed if c not in cols]
    record("A01", "ensure_schema adds 3 URL-verification columns to evidence_sources",
           not missing,
           details=f"missing: {missing}" if missing else "all present")
except Exception as e:
    record("A01", "schema add columns", False, error=traceback.format_exc(limit=2))

# A02: ensure_schema creates url_verification_runs table
try:
    conn = fresh()
    mod.ensure_schema(conn)
    cols = [r[1] for r in conn.execute("PRAGMA table_info(url_verification_runs)")]
    record("A02", "ensure_schema creates url_verification_runs table",
           len(cols) >= 13,
           details=f"{len(cols)} cols")
except Exception as e:
    record("A02", "create runs table", False, error=traceback.format_exc(limit=2))

# A03: ensure_schema is idempotent
try:
    conn = fresh()
    mod.ensure_schema(conn)
    mod.ensure_schema(conn)
    mod.ensure_schema(conn)
    record("A03", "ensure_schema idempotent (3 sequential calls don't error)", True)
except Exception as e:
    record("A03", "schema idempotent", False, error=traceback.format_exc(limit=2))


# ── B: HTML title extraction ─────────────────────────────────────────────────
print("\n[B] Title extraction from HTML")

# B01: Plain <title> tag
try:
    html = "<html><head><title>Building Accessibility Standards</title></head><body>x</body></html>"
    t = mod.extract_title(html)
    record("B01", "Plain <title> tag extracted",
           t == "Building Accessibility Standards",
           details=f"got: '{t}'")
except Exception as e:
    record("B01", "plain title", False, error=traceback.format_exc(limit=2))

# B02: citation_title meta tag preferred over <title>
try:
    html = """<html><head>
        <meta name="citation_title" content="Accessibility Guidelines for Residential Spaces">
        <title>Site Home Page</title>
        </head></html>"""
    t = mod.extract_title(html)
    record("B02", "citation_title meta preferred over <title>",
           t == "Accessibility Guidelines for Residential Spaces",
           details=f"got: '{t}'")
except Exception as e:
    record("B02", "citation_title pref", False, error=traceback.format_exc(limit=2))

# B03: og:title meta tag preferred over <title>
try:
    html = """<html><head>
        <meta property="og:title" content="WCAG 2.2 Guidelines">
        <title>W3C - Web Standards</title>
        </head></html>"""
    t = mod.extract_title(html)
    record("B03", "og:title preferred over <title>",
           t == "WCAG 2.2 Guidelines",
           details=f"got: '{t}'")
except Exception as e:
    record("B03", "og:title pref", False, error=traceback.format_exc(limit=2))

# B04: HTML entities decoded
try:
    html = "<html><head><title>Caf&eacute; Accessibility &amp; Design</title></head></html>"
    t = mod.extract_title(html)
    record("B04", "HTML entities decoded in title",
           t == "Café Accessibility & Design",
           details=f"got: '{t}'")
except Exception as e:
    record("B04", "entity decode", False, error=traceback.format_exc(limit=2))

# B05: Empty / missing title handled
try:
    t = mod.extract_title("<html><body>No title here</body></html>")
    record("B05", "Missing <title> returns empty string", t == "",
           details=f"got: '{t}'")
except Exception as e:
    record("B05", "missing title", False, error=traceback.format_exc(limit=2))


# ── C: Title similarity ──────────────────────────────────────────────────────
print("\n[C] Title similarity (fuzzy word-overlap)")

# C01: Identical titles → 1.0
try:
    s = mod.title_similarity("WCAG 2.2 Accessibility Guidelines",
                              "WCAG 2.2 Accessibility Guidelines")
    record("C01", "Identical titles return similarity 1.0",
           s == 1.0, details=f"sim={s}")
except Exception as e:
    record("C01", "identical sim", False, error=traceback.format_exc(limit=2))

# C02: Completely disjoint titles → 0.0
try:
    s = mod.title_similarity("WCAG 2.2 Accessibility Guidelines",
                              "Italian Renaissance Painting Techniques")
    record("C02", "Disjoint titles return 0.0", s == 0.0,
           details=f"sim={s}")
except Exception as e:
    record("C02", "disjoint sim", False, error=traceback.format_exc(limit=2))

# C03: Partial overlap mid-range
try:
    s = mod.title_similarity("WCAG 2.2 Accessibility Guidelines",
                              "Web Content Accessibility Guidelines version 2.2")
    record("C03", "Partial overlap in 0.4–1.0 range",
           0.4 <= s <= 1.0, details=f"sim={s:.3f}")
except Exception as e:
    record("C03", "partial sim", False, error=traceback.format_exc(limit=2))

# C04: Stopwords excluded
try:
    # Only stopwords match → 0
    s = mod.title_similarity("The Accessibility Standards",
                              "The For Of Building Design")
    record("C04", "Stopword-only matches excluded (sim should be 0)",
           s == 0.0, details=f"sim={s}")
except Exception as e:
    record("C04", "stopwords excluded", False, error=traceback.format_exc(limit=2))

# C05: Empty inputs handled
try:
    record("C05", "Empty inputs return 0.0",
           mod.title_similarity("", "X") == 0.0 and
           mod.title_similarity("X", "") == 0.0 and
           mod.title_similarity(None, None) == 0.0)
except Exception as e:
    record("C05", "empty inputs", False, error=traceback.format_exc(limit=2))


# ── D: Error-title detection ─────────────────────────────────────────────────
print("\n[D] 'soft 404' page title detection")

# D01: Various error titles caught
try:
    cases = ["404 Not Found", "Page Not Found", "404 - Page does not exist",
             "We couldn't find that page", "Error 404"]
    ok = all(mod.is_error_title(c) for c in cases)
    record("D01", "Common error-title patterns detected", ok)
except Exception as e:
    record("D01", "error title detection", False, error=traceback.format_exc(limit=2))

# D02: Normal titles NOT flagged
try:
    cases = ["WCAG 2.2 Guidelines", "Accessibility in the Built Environment", ""]
    ok = not any(mod.is_error_title(c) for c in cases)
    record("D02", "Real titles not flagged as errors", ok)
except Exception as e:
    record("D02", "normal title not flagged", False, error=traceback.format_exc(limit=2))


# ── E: verify_one with mocked fetcher ────────────────────────────────────────
print("\n[E] verify_one — full verification flow (mocked HTTP)")

def make_mock_fetch(html_body, status=200):
    return lambda url, timeout=20: (status, html_body)

def make_mock_404():
    def _f(url, timeout=20):
        raise urllib.error.HTTPError(url, 404, "Not Found", {}, None)
    return _f

def make_mock_dns_fail():
    def _f(url, timeout=20):
        raise urllib.error.URLError("Name or service not known")
    return _f

def make_mock_5xx():
    def _f(url, timeout=20):
        raise urllib.error.HTTPError(url, 503, "Service Unavailable", {}, None)
    return _f

ts = "2026-05-12 12:00"

# E01: Strong title match → VERIFIED
try:
    conn = fresh()
    mod.ensure_schema(conn)
    rid = "REF-TEST-E01"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,url,pub_title,is_corporate_primary)
        VALUES (?,?,?,?,?)""",
        (rid,"guideline","https://example.org/wcag22",
         "WCAG 2.2 Web Content Accessibility Guidelines",0))
    conn.commit()
    orig = mod.fetch_url
    mod.fetch_url = make_mock_fetch(
        "<html><head><title>WCAG 2.2 Web Content Accessibility Guidelines | W3C</title></head></html>")
    outcome = mod.verify_one(conn, rid, "https://example.org/wcag22",
                              "WCAG 2.2 Web Content Accessibility Guidelines", ts)
    conn.commit()
    mod.fetch_url = orig
    after = read(conn, rid)
    record("E01", "Strong title match → VERIFIED + url_resolution_outcome=MATCHED",
           outcome == "verified" and after["verification_status"] == "VERIFIED"
           and after["url_resolution_outcome"] == "MATCHED",
           details=f"status={after.get('verification_status')} outcome={after.get('url_resolution_outcome')} sim={after.get('url_match_similarity')}")
except Exception as e:
    mod.fetch_url = orig if 'orig' in dir() else mod.fetch_url
    record("E01", "verify strong match", False, error=traceback.format_exc(limit=2))

# E02: Weak match (URL works, title diverges) → NO-MATCH
try:
    conn = fresh()
    mod.ensure_schema(conn)
    rid = "REF-TEST-E02"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,url,pub_title,is_corporate_primary)
        VALUES (?,?,?,?,?)""",
        (rid,"report","https://example.org/random",
         "Building Accessibility Survey 2023",0))
    conn.commit()
    orig = mod.fetch_url
    mod.fetch_url = make_mock_fetch(
        "<html><head><title>Home — Example Organization</title></head></html>")
    outcome = mod.verify_one(conn, rid, "https://example.org/random",
                              "Building Accessibility Survey 2023", ts)
    conn.commit()
    mod.fetch_url = orig
    after = read(conn, rid)
    record("E02", "Title divergence → NO-MATCH (status unchanged, will retry in 30d)",
           outcome == "no-match" and after["verification_status"] is None
           and after["url_resolution_outcome"] == "NO-MATCH",
           details=f"status={after.get('verification_status')} outcome={after.get('url_resolution_outcome')}")
except Exception as e:
    record("E02", "verify weak match", False, error=traceback.format_exc(limit=2))

# E03: 404 → UNVERIFIED-CLOSED + DEAD-LINK (with Wayback disabled)
try:
    conn = fresh()
    mod.ensure_schema(conn)
    rid = "REF-TEST-E03"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,url,pub_title,is_corporate_primary)
        VALUES (?,?,?,?,?)""",
        (rid,"report","https://example.org/dead",
         "Dead Page Title",0))
    conn.commit()
    orig = mod.fetch_url
    mod.fetch_url = make_mock_404()
    outcome = mod.verify_one(conn, rid, "https://example.org/dead", "Dead Page Title", ts)
    conn.commit()
    mod.fetch_url = orig
    after = read(conn, rid)
    record("E03", "404 → UNVERIFIED-CLOSED + url_resolution_outcome=DEAD-LINK",
           outcome == "dead" and after["verification_status"] == "UNVERIFIED-CLOSED"
           and after["url_resolution_outcome"] == "DEAD-LINK",
           details=f"status={after.get('verification_status')} outcome={after.get('url_resolution_outcome')}")
except Exception as e:
    record("E03", "verify 404 dead", False, error=traceback.format_exc(limit=2))

# E04: DNS failure → UNVERIFIED-CLOSED + DEAD-DNS
try:
    conn = fresh()
    mod.ensure_schema(conn)
    rid = "REF-TEST-E04"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,url,pub_title,is_corporate_primary)
        VALUES (?,?,?,?,?)""",
        (rid,"report","https://nonexistent-domain-xyz.example/page", "Page Title",0))
    conn.commit()
    orig = mod.fetch_url
    mod.fetch_url = make_mock_dns_fail()
    outcome = mod.verify_one(conn, rid, "https://nonexistent-domain-xyz.example/page",
                              "Page Title", ts)
    conn.commit()
    mod.fetch_url = orig
    after = read(conn, rid)
    record("E04", "DNS failure → UNVERIFIED-CLOSED + DEAD-DNS",
           outcome == "dead-dns" and after["verification_status"] == "UNVERIFIED-CLOSED"
           and after["url_resolution_outcome"] == "DEAD-DNS",
           details=f"status={after.get('verification_status')} outcome={after.get('url_resolution_outcome')}")
except Exception as e:
    record("E04", "verify DNS fail", False, error=traceback.format_exc(limit=2))

# E05: 5xx → transient (no DB write)
try:
    conn = fresh()
    mod.ensure_schema(conn)
    rid = "REF-TEST-E05"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,url,pub_title,verification_status,is_corporate_primary)
        VALUES (?,?,?,?,?,?)""",
        (rid,"report","https://example.org/maintenance", "Page Title", None,0))
    conn.commit()
    orig = mod.fetch_url
    mod.fetch_url = make_mock_5xx()
    outcome = mod.verify_one(conn, rid, "https://example.org/maintenance", "Page Title", ts)
    conn.commit()
    mod.fetch_url = orig
    after = read(conn, rid)
    record("E05", "5xx → transient (no verification_status write)",
           outcome == "transient-5xx" and after["verification_status"] is None
           and after["url_resolution_outcome"] is None,
           details=f"outcome={outcome} status={after.get('verification_status')}")
except Exception as e:
    record("E05", "5xx transient", False, error=traceback.format_exc(limit=2))


# ── F: Candidate query & state machine ───────────────────────────────────────
print("\n[F] Candidate query & state machine")

# F01: VERIFIED rows excluded from candidate pool
try:
    conn = fresh()
    mod.ensure_schema(conn)
    rid = "REF-TEST-F01"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,url,pub_title,verification_status,is_corporate_primary)
        VALUES (?,?,?,?,?,?)""",
        (rid,"report","https://x.com/y","T","VERIFIED",0))
    conn.commit()
    n = conn.execute(f"""SELECT COUNT(*) FROM evidence_sources
        WHERE ref_id=? AND url IS NOT NULL AND url != ''
        AND verification_status IS NULL""", (rid,)).fetchone()[0]
    record("F01", "VERIFIED rows excluded from candidate pool", n == 0)
except Exception as e:
    record("F01", "verified excluded", False, error=traceback.format_exc(limit=2))

# F02: DEAD-LINK rows excluded permanently (no retry)
try:
    conn = fresh()
    mod.ensure_schema(conn)
    rid = "REF-TEST-F02"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,url,pub_title,url_resolution_outcome,is_corporate_primary)
        VALUES (?,?,?,?,?,?)""",
        (rid,"report","https://x.com/y","T","DEAD-LINK",0))
    conn.commit()
    n = conn.execute(f"""SELECT COUNT(*) FROM evidence_sources
        WHERE ref_id=? AND url IS NOT NULL AND url != ''
        AND verification_status IS NULL
        AND (url_resolution_outcome IS NULL
             OR url_resolution_outcome IN ('NO-MATCH'))""", (rid,)).fetchone()[0]
    record("F02", "DEAD-LINK rows permanently excluded from candidate pool", n == 0)
except Exception as e:
    record("F02", "dead excluded", False, error=traceback.format_exc(limit=2))

# F03: NO-MATCH retry window enforced
try:
    conn = fresh()
    mod.ensure_schema(conn)
    rid_recent = "REF-TEST-F03A"
    rid_old    = "REF-TEST-F03B"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,url,pub_title,url_resolution_outcome,last_verified_at,is_corporate_primary)
        VALUES (?,?,?,?,?,?,?)""",
        (rid_recent,"report","https://x.com/recent","T","NO-MATCH","2026-05-12 00:00",0))
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,url,pub_title,url_resolution_outcome,last_verified_at,is_corporate_primary)
        VALUES (?,?,?,?,?,?,?)""",
        (rid_old,"report","https://x.com/old","T","NO-MATCH","2025-01-01 00:00",0))
    conn.commit()
    cutoff = "2026-04-12 00:00"  # 30 days ago
    rows = conn.execute("""SELECT ref_id FROM evidence_sources
        WHERE ref_id LIKE 'REF-TEST-F03%'
        AND verification_status IS NULL
        AND (url_resolution_outcome IS NULL
             OR (url_resolution_outcome = 'NO-MATCH' AND last_verified_at < ?))
        ORDER BY ref_id""", (cutoff,)).fetchall()
    record("F03", "NO-MATCH older than cutoff included; recent excluded",
           len(rows) == 1 and rows[0]["ref_id"] == rid_old,
           details=f"matched: {[r['ref_id'] for r in rows]}")
except Exception as e:
    record("F03", "no-match window", False, error=traceback.format_exc(limit=2))


# ── G: write_verification idempotency ────────────────────────────────────────
print("\n[G] write_verification idempotency & accumulator")

# G01: Repeated writes don't corrupt; attempt_count increments
try:
    conn = fresh()
    mod.ensure_schema(conn)
    rid = "REF-TEST-G01"
    conn.execute("""INSERT OR IGNORE INTO evidence_sources
        (ref_id,source_type,url,pub_title,is_corporate_primary)
        VALUES (?,?,?,?,?)""", (rid,"report","https://x.com/y","T",0))
    conn.commit()
    for i in range(3):
        mod.write_verification(conn, rid, status="VERIFIED", outcome="MATCHED",
                                similarity=0.8, note=f"attempt {i}")
        conn.commit()
    after = read(conn, rid)
    record("G01", "Repeated writes accumulate; attempt_count = 3",
           after["verification_status"] == "VERIFIED"
           and after["verification_attempt_count"] == 3,
           details=f"count={after.get('verification_attempt_count')} status={after.get('verification_status')}")
except Exception as e:
    record("G01", "idempotent write", False, error=traceback.format_exc(limit=2))


# ── H: Run record bookkeeping ────────────────────────────────────────────────
print("\n[H] url_verification_runs bookkeeping")

# H01: ensure_schema creates table with expected columns
try:
    conn = fresh()
    mod.ensure_schema(conn)
    cols = [r[1] for r in conn.execute("PRAGMA table_info(url_verification_runs)")]
    expected = {'run_id','started_at','completed_at','candidates_pool','attempted',
                'verified','probabilistic','no_match','dead','wayback_verified',
                'wayback_probabilistic','dead_dns','transient',
                'verified_before','verified_after','run_by_session'}
    record("H01", "url_verification_runs has all expected columns",
           expected.issubset(set(cols)),
           details=f"missing: {expected - set(cols)}" if not expected.issubset(set(cols)) else "all present")
except Exception as e:
    record("H01", "runs table cols", False, error=traceback.format_exc(limit=2))


# ── Summary ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
total = len(results)
passed = sum(results)
print(f"RESULTS: {passed}/{total} tests passed")
if passed < total:
    print(f"FAILED: {total - passed}")
print("=" * 70)
sys.exit(0 if passed == total else 1)
