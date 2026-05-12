#!/usr/bin/env python3
"""
Channel 2 URL verifier — Source Verification Pipeline V1
========================================================

For sources where the canonical record is a URL (gov't portals, standards
bodies without DOIs, NGO reports, WHO documents), this script:

  1. Fetches the URL
  2. Extracts the page's <title> (prefers citation_title / og:title meta tags)
  3. Fuzzy-matches the page title against the source's pub_title
  4. Writes verification state to evidence_sources

This is the GENERIC verifier. Per-publisher scrapers (DIN beuth.de, CSA store,
JIS database, GB openstd, etc.) plug in later as discoverers — they find
candidate URLs which this verifier then confirms.

Outcomes
--------
  VERIFIED            — URL reachable AND title similarity >= TITLE_MATCH_HIGH
  PROBABILISTIC       — URL reachable AND TITLE_MATCH_LOW <= sim < TITLE_MATCH_HIGH
                         (page exists but title diverges; flag for human review)
  (no status change)  — URL reachable but title doesn't match (likely wrong URL);
                         url_resolution_outcome=URL-NO-MATCH, 30-day retry
  UNVERIFIED-CLOSED   — 404/410 (page permanently gone); url_resolution_outcome=DEAD
                         Wayback fallback attempted before declaring DEAD.
  (no write)          — 403/429/5xx/timeout (transient); retry next run

Wayback Machine fallback
-------------------------
On 404/410, queries https://archive.org/wayback/available to find the most
recent snapshot. If a snapshot exists, verifies against the snapshot's title.
Outcome notes record the snapshot URL so reviewers can inspect.

Schema additions (applied via migration before first run):
  evidence_sources.url_resolution_outcome  TEXT
  evidence_sources.url_last_fetched        TEXT
  evidence_sources.url_match_similarity    REAL

Environment variables:
  GUIDEBOOK_DB_PATH    Path to guidebook.db (default: data/guidebook.db)
  MAX_VERIFY           Maximum sources to attempt per run (default: 500)
  RATE_LIMIT           Seconds between requests (default: 3.0)
  SKIP_NO_MATCH_DAYS   Days before retrying NO-MATCH rows (default: 30)
  USE_WAYBACK          1 to enable Wayback fallback (default: 1)
"""

import os
import re
import sys
import time
import html
import sqlite3
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

# ─── Constants ───────────────────────────────────────────────────────────────

USER_AGENT = "guidebook-project/2.0 URL-Verifier (mailto:jordan@guidebook.dev)"
DB_PATH    = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")
MAX_VERIFY = int(os.environ.get("MAX_VERIFY", "500"))
RATE_LIMIT = float(os.environ.get("RATE_LIMIT", "3.0"))
SKIP_NO_MATCH_DAYS = int(os.environ.get("SKIP_NO_MATCH_DAYS", "30"))
USE_WAYBACK = os.environ.get("USE_WAYBACK", "1") == "1"
SESSION = os.environ.get("GITHUB_RUN_ID", "manual") or "manual"

# Verification thresholds
TITLE_MATCH_HIGH = 0.50  # >= => VERIFIED
TITLE_MATCH_LOW  = 0.20  # >= => PROBABILISTIC

# Fetch limits
TIMEOUT_S       = 20
MAX_PAGE_BYTES  = 500_000  # cap memory per page

STOPWORDS = {
    "the", "and", "for", "with", "from", "this", "that", "are", "was",
    "were", "into", "than", "but", "not", "all", "any", "can", "has",
    "have", "had", "may", "use", "used", "via", "per", "its",
}

TABLE = "evidence_sources"


# ─── HTML title extraction ───────────────────────────────────────────────────

class TitleExtractor(HTMLParser):
    """Extract <title>, citation_title meta, and og:title meta from HTML."""
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = None
        self.meta_title = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title" and not self.title:
            self.in_title = True
            return
        if tag.lower() == "meta":
            d = {k.lower(): v for k, v in attrs if v is not None}
            name = (d.get("name") or "").lower()
            prop = (d.get("property") or "").lower()
            if name in ("citation_title", "dc.title") or prop == "og:title":
                if not self.meta_title and d.get("content"):
                    self.meta_title = d["content"].strip()

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title and not self.title:
            t = data.strip()
            if t:
                self.title = t


def extract_title(body):
    """Get the best title from the HTML body. Prefers meta tags over <title>."""
    p = TitleExtractor()
    try:
        # Cap to first MAX_PAGE_BYTES so very large pages don't blow up memory.
        p.feed(body[:MAX_PAGE_BYTES])
    except Exception:
        pass
    raw = (p.meta_title or p.title or "")
    return html.unescape(raw).strip()


# ─── Fuzzy title matching ────────────────────────────────────────────────────

def normalize_title_words(s):
    if not s:
        return set()
    cleaned = re.sub(r"[^\w\s]", " ", s.lower())
    return {w for w in cleaned.split() if len(w) > 2 and w not in STOPWORDS}


def title_similarity(source_title, page_title):
    """Word-overlap similarity ratio between pub_title and page <title>."""
    src = normalize_title_words(source_title)
    pg  = normalize_title_words(page_title)
    if not src or not pg:
        return 0.0
    overlap = src & pg
    if not overlap:
        return 0.0
    return len(overlap) / min(len(src), len(pg))


# ─── HTTP fetch with proper UA + timeout ─────────────────────────────────────

def fetch_url(url, timeout=TIMEOUT_S):
    """GET the URL, return (status_code, body_text).
    Raises HTTPError on 4xx/5xx, URLError on DNS/connection failure.
    """
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5",
        "Accept-Language": "en-US,en;q=0.5",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read(MAX_PAGE_BYTES)
        charset = r.headers.get_content_charset() or "utf-8"
        try:
            body = raw.decode(charset, errors="replace")
        except (LookupError, UnicodeDecodeError):
            body = raw.decode("utf-8", errors="replace")
        return r.status, body


def is_error_title(t):
    """Detect page-title patterns that indicate the page is an error/404."""
    if not t:
        return False
    low = t.lower()
    return any(s in low for s in [
        "404", "not found", "page not found", "page doesn't exist",
        "page does not exist", "page unavailable", "error 404",
        "this page is missing", "we couldn't find",
    ])


# ─── Wayback Machine fallback ────────────────────────────────────────────────

def wayback_snapshot(url):
    """Query archive.org/wayback/available for the most recent snapshot.
    Returns the snapshot URL or None.
    """
    if not USE_WAYBACK:
        return None
    api = f"https://archive.org/wayback/available?url={urllib.parse.quote(url, safe='')}"
    try:
        req = urllib.request.Request(api, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=15) as r:
            import json
            data = json.loads(r.read())
        snap = (data.get("archived_snapshots") or {}).get("closest") or {}
        if snap.get("available") and snap.get("url"):
            return snap["url"]
    except Exception:
        return None
    return None


# ─── Central write function ──────────────────────────────────────────────────

def write_verification(conn, ref_id, *, status=None, outcome=None,
                       similarity=None, page_title_preview=None, note=None,
                       ts=None):
    """Idempotent write of URL-verification state.

    status passed to evidence_sources.verification_status (None = leave unchanged)
    outcome -> url_resolution_outcome ('MATCHED', 'PARTIAL', 'NO-MATCH', 'DEAD',
                                       'NO-MATCH-WAYBACK', 'WAYBACK-MATCH')
    similarity -> url_match_similarity (float 0..1)
    """
    ts = ts or time.strftime("%Y-%m-%d %H:%M", time.gmtime())
    sets = ["verified_by_tool = ?",
            "last_verified_at = ?",
            "verification_attempt_count = COALESCE(verification_attempt_count,0) + 1",
            "url_last_fetched = ?",
            "updated_at = ?",
            "updated_by_session = ?"]
    params = ["url-fetch-v1", ts, ts, ts, SESSION]

    if status is not None:
        sets.insert(0, "verification_status = ?")
        params.insert(0, status)
    if outcome is not None:
        sets.append("url_resolution_outcome = ?")
        params.append(outcome)
    if similarity is not None:
        sets.append("url_match_similarity = ?")
        params.append(float(similarity))
    if note is not None:
        sets.append("verification_note = ?")
        params.append(note)

    params.append(ref_id)
    conn.execute(
        f"UPDATE {TABLE} SET {', '.join(sets)} WHERE ref_id = ?",
        params,
    )


# ─── Per-source verification logic ───────────────────────────────────────────

def verify_one(conn, ref_id, url, pub_title, ts):
    """Verify a single source's URL. Returns outcome string for stats."""
    # ── Step 1: fetch the URL
    try:
        status, body = fetch_url(url)
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            return verify_dead_with_wayback(conn, ref_id, url, pub_title, ts, e.code)
        elif e.code in (403, 429):
            return "transient-blocked"
        elif 500 <= e.code < 600:
            return "transient-5xx"
        else:
            return "transient-other"
    except urllib.error.URLError as e:
        reason = str(e.reason).lower() if hasattr(e, "reason") else ""
        # DNS failure / no such host => effectively dead
        if any(s in reason for s in ["name or service", "nodename", "no address",
                                      "name resolution"]):
            write_verification(conn, ref_id, status="UNVERIFIED-CLOSED",
                               outcome="DEAD-DNS",
                               note=f"DNS resolution failed: {url}", ts=ts)
            return "dead-dns"
        return "transient-network"
    except (TimeoutError, ConnectionError):
        return "transient-timeout"
    except Exception:
        return "transient-other"

    # ── Step 2: extract title from page
    page_title = extract_title(body)
    if is_error_title(page_title):
        # Site returned 200 but title says "404 not found" — soft dead link
        return verify_dead_with_wayback(conn, ref_id, url, pub_title, ts, 0,
                                        soft_error=page_title)

    # ── Step 3: similarity match
    sim = title_similarity(pub_title or "", page_title)

    if sim >= TITLE_MATCH_HIGH:
        write_verification(conn, ref_id, status="VERIFIED",
                           outcome="MATCHED", similarity=sim,
                           note=f"URL live; title match sim={sim:.2f}: {page_title[:80]}",
                           ts=ts)
        return "verified"
    elif sim >= TITLE_MATCH_LOW:
        write_verification(conn, ref_id, status="PROBABILISTIC",
                           outcome="PARTIAL", similarity=sim,
                           note=f"URL live; partial title match sim={sim:.2f}: {page_title[:80]}",
                           ts=ts)
        return "probabilistic"
    else:
        # URL works but title doesn't match — might be wrong URL or site changed.
        # Use the 30-day NO-MATCH window mechanism: don't set verification_status,
        # but record outcome=NO-MATCH so future runs skip until window passes.
        write_verification(conn, ref_id, status=None,
                           outcome="NO-MATCH", similarity=sim,
                           note=f"URL live but title diverges sim={sim:.2f}: {page_title[:80]}",
                           ts=ts)
        return "no-match"


def verify_dead_with_wayback(conn, ref_id, url, pub_title, ts, code, soft_error=None):
    """A URL is dead. Try Wayback before declaring it permanently closed."""
    snap = wayback_snapshot(url)
    if snap:
        try:
            _, body = fetch_url(snap)
            page_title = extract_title(body)
            sim = title_similarity(pub_title or "", page_title)
            if sim >= TITLE_MATCH_HIGH:
                write_verification(conn, ref_id, status="VERIFIED",
                                   outcome="WAYBACK-MATCH", similarity=sim,
                                   note=f"Live URL dead ({code or 'soft'}); "
                                        f"Wayback snapshot matches sim={sim:.2f}: {snap}",
                                   ts=ts)
                return "wayback-verified"
            elif sim >= TITLE_MATCH_LOW:
                write_verification(conn, ref_id, status="PROBABILISTIC",
                                   outcome="WAYBACK-PARTIAL", similarity=sim,
                                   note=f"Live URL dead; Wayback partial sim={sim:.2f}: {snap}",
                                   ts=ts)
                return "wayback-probabilistic"
        except Exception:
            pass

    # No Wayback match found
    note_prefix = f"HTTP {code}" if code else f"Soft error: {soft_error[:50]}"
    write_verification(conn, ref_id, status="UNVERIFIED-CLOSED",
                       outcome="DEAD-LINK",
                       note=f"{note_prefix}; Wayback no snapshot or no match: {url}",
                       ts=ts)
    return "dead"


# ─── Schema setup ────────────────────────────────────────────────────────────

def ensure_schema(conn):
    """Idempotently add the URL-verification columns and runs table."""
    es_cols = [r[1] for r in conn.execute(f"PRAGMA table_info({TABLE})")]
    for col, ddl in [
        ("url_resolution_outcome", "TEXT"),
        ("url_last_fetched",       "TEXT"),
        ("url_match_similarity",   "REAL"),
    ]:
        if col not in es_cols:
            conn.execute(f"ALTER TABLE {TABLE} ADD COLUMN {col} {ddl}")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS url_verification_runs (
          run_id              TEXT PRIMARY KEY,
          started_at          TEXT NOT NULL,
          completed_at        TEXT,
          candidates_pool     INTEGER DEFAULT 0,
          attempted           INTEGER DEFAULT 0,
          verified            INTEGER DEFAULT 0,
          probabilistic       INTEGER DEFAULT 0,
          no_match            INTEGER DEFAULT 0,
          dead                INTEGER DEFAULT 0,
          wayback_verified    INTEGER DEFAULT 0,
          wayback_probabilistic INTEGER DEFAULT 0,
          dead_dns            INTEGER DEFAULT 0,
          transient           INTEGER DEFAULT 0,
          verified_before     INTEGER DEFAULT 0,
          verified_after      INTEGER DEFAULT 0,
          run_by_session      TEXT
        )
    """)
    conn.commit()


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    ensure_schema(conn)

    now_iso = time.strftime("%Y-%m-%d %H:%M", time.gmtime())
    cutoff_iso = time.strftime(
        "%Y-%m-%d %H:%M",
        time.gmtime(time.time() - SKIP_NO_MATCH_DAYS * 86400),
    )

    # Snapshot pre-run state
    verified_before = conn.execute(
        f"SELECT COUNT(*) FROM {TABLE} WHERE verification_status='VERIFIED'"
    ).fetchone()[0]
    pool_size = conn.execute(f"""
        SELECT COUNT(*) FROM {TABLE}
        WHERE url IS NOT NULL AND url != ''
        AND verification_status IS NULL
        AND (
          url_resolution_outcome IS NULL
          OR (url_resolution_outcome = 'NO-MATCH' AND last_verified_at < ?)
        )
    """, (cutoff_iso,)).fetchone()[0]

    # Insert run record
    run_id = now_iso
    conn.execute("""
        INSERT OR REPLACE INTO url_verification_runs
          (run_id, started_at, candidates_pool, verified_before, run_by_session)
        VALUES (?, ?, ?, ?, ?)
    """, (run_id, now_iso, pool_size, verified_before, SESSION))
    conn.commit()

    print(f"Run {run_id}: candidates_pool={pool_size}, verified_before={verified_before}, "
          f"rate_limit={RATE_LIMIT}s, wayback={'on' if USE_WAYBACK else 'off'}\n")
    print("=" * 60)
    print("Channel 2 — Generic URL verifier")
    print("=" * 60)

    candidates = conn.execute(f"""
        SELECT ref_id, url, pub_title
        FROM {TABLE}
        WHERE url IS NOT NULL AND url != ''
        AND verification_status IS NULL
        AND (
          url_resolution_outcome IS NULL
          OR (url_resolution_outcome = 'NO-MATCH' AND last_verified_at < ?)
        )
        ORDER BY ref_id
        LIMIT ?
    """, (cutoff_iso, MAX_VERIFY)).fetchall()

    print(f"  Candidates: {len(candidates)}\n")

    counts = {"verified": 0, "probabilistic": 0, "no-match": 0, "dead": 0,
              "wayback-verified": 0, "wayback-probabilistic": 0,
              "dead-dns": 0, "transient-blocked": 0, "transient-5xx": 0,
              "transient-network": 0, "transient-timeout": 0,
              "transient-other": 0}

    for c in candidates:
        outcome = verify_one(conn, c["ref_id"], c["url"], c["pub_title"], now_iso)
        counts[outcome] = counts.get(outcome, 0) + 1
        symbol = {"verified": "✓", "probabilistic": "~", "no-match": "?",
                  "dead": "✗", "wayback-verified": "↩✓",
                  "wayback-probabilistic": "↩~", "dead-dns": "✗"}.get(outcome, "·")
        host = urllib.parse.urlparse(c["url"]).netloc[:30]
        print(f"  [{symbol}] {c['ref_id']} {host:<30}  -> {outcome}")
        conn.commit()
        time.sleep(RATE_LIMIT)

    # ── Summary
    verified_after = conn.execute(
        f"SELECT COUNT(*) FROM {TABLE} WHERE verification_status='VERIFIED'"
    ).fetchone()[0]
    transient_total = (counts["transient-blocked"] + counts["transient-5xx"]
                       + counts["transient-network"] + counts["transient-timeout"]
                       + counts["transient-other"])
    completed_at = time.strftime("%Y-%m-%d %H:%M", time.gmtime())

    conn.execute("""
        UPDATE url_verification_runs SET
          completed_at = ?,
          attempted = ?,
          verified = ?, probabilistic = ?, no_match = ?,
          dead = ?, wayback_verified = ?, wayback_probabilistic = ?,
          dead_dns = ?, transient = ?, verified_after = ?
        WHERE run_id = ?
    """, (
        completed_at,
        len(candidates),
        counts["verified"], counts["probabilistic"], counts["no-match"],
        counts["dead"], counts["wayback-verified"], counts["wayback-probabilistic"],
        counts["dead-dns"], transient_total, verified_after,
        run_id,
    ))
    conn.commit()

    print()
    print("=" * 60)
    print(f"  Candidates pool:               {pool_size}")
    print(f"  Attempted this run:            {len(candidates)}")
    print(f"  VERIFIED (live + title match): {counts['verified']}")
    print(f"  PROBABILISTIC (partial match): {counts['probabilistic']}")
    print(f"  NO-MATCH (title diverges):     {counts['no-match']} (retry in {SKIP_NO_MATCH_DAYS}d)")
    print(f"  DEAD-LINK (404/410):           {counts['dead']}")
    print(f"  WAYBACK rescued (verified):    {counts['wayback-verified']}")
    print(f"  WAYBACK rescued (partial):     {counts['wayback-probabilistic']}")
    print(f"  DEAD-DNS:                      {counts['dead-dns']}")
    print(f"  Transient (will retry):        {transient_total}")
    print(f"  verification_status VERIFIED:  {verified_before} -> {verified_after}  "
          f"delta={verified_after - verified_before:+d}")
    print(f"  Run record:                    url_verification_runs['{run_id}']")
    print("=" * 60)

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
