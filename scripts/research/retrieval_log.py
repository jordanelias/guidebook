#!/usr/bin/env python3
"""
scripts/research/retrieval_log.py — persist what was actually retrieved.

WHY
---
On 2026-08-19 the first research batch after the restart wrote FABRICATED author
lists onto all five of its admissions, and stamped them
`verification_status='VERIFIED'`, `verified_by_tool='crossref'`,
`verification_method='tool'`, `metadata_quality='COMPLETE'`.

The retrieval had genuinely happened — the reference counts stored alongside match
Crossref exactly, and those numbers exist nowhere but that payload. The author
array was in the same JSON object and was overwritten from memory.

Nothing could detect it, for one structural reason:

    verification_method='tool' was a SELF-ASSERTION WITH NO ARTEFACT BEHIND IT.

No gate could tell an executed retrieval from a claimed one, because the evidence
of the retrieval was never kept. Finding it took an adversarial pass and five
agents. With the payload on disk it is a one-line diff.

Owner ruling, 2026-08-19: "the repository has more than enough room to store
scratchpad logs if they're ever needed. it is very unlikely we will ever have to
look through them unless we are auditing for fidelity."

That is exactly the value profile of this log — near-zero read frequency, and
irreplaceable in the one case that matters.

USE
---
    from retrieval_log import fetch
    payload = fetch("https://api.crossref.org/works/10.xxxx/yyy", session=S,
                    purpose="crossref metadata for REF-00965")

`fetch` returns the parsed JSON *and* writes the raw bytes under
`retrieval-log/<session>/`, with a manifest line recording url, sha256, byte
count, and the UTC timestamp. Writes happen BEFORE the caller sees the data, so a
caller cannot log a different payload than the one it acted on.

    python3 scripts/research/retrieval_log.py --verify-authors --session <id>

verifies stored authors against the LOGGED payload — offline, no network, and
authoritative as-of-retrieval rather than as-of-audit. That distinction matters:
re-fetching at audit time cannot detect a record that was correct when written and
has since been corrected upstream, nor can it run when the API is unreachable.
"""

import argparse
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path


def _norm(s):
    """Fold accents and case before comparing surnames.

    A stored "Rosas-Perez" against an actual "Rosas-Pérez" is the SAME PERSON
    differently encoded; the failure this module detects is a DIFFERENT person.
    A plain .lower() compare called that a mismatch, which meant this verifier
    and scripts/audit/author_fidelity_audit.py — two checks of one property,
    shipped in the same commit — returned opposite answers on REF-00965. Two
    verifiers with divergent match rules is a defect, not depth.
    """
    s = unicodedata.normalize("NFKD", (s or "").strip().lower())
    return "".join(ch for ch in s if not unicodedata.combining(ch))

LOG_ROOT = Path(os.environ.get("GUIDEBOOK_RETRIEVAL_LOG", "retrieval-log"))
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fetch(url, session, purpose="", timeout=40, stamp=None):
    """Retrieve a URL, PERSIST the raw response, then return the parsed JSON.

    The write happens before the return, deliberately: the artefact on disk is the
    bytes the caller actually received, not a later re-fetch that may differ.
    """
    r = subprocess.run(["curl", "-sS", "--max-time", str(timeout), url],
                       capture_output=True, text=True)
    body = r.stdout
    d = LOG_ROOT / _session_stem(session)
    d.mkdir(parents=True, exist_ok=True)
    sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
    (d / f"{sha[:16]}.json").write_text(body, encoding="utf-8")
    with open(d / "manifest.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps({
            "retrieved_at": stamp or _now(), "url": url, "purpose": purpose,
            "sha256": sha, "bytes": len(body), "exit": r.returncode,
            "artefact": f"{sha[:16]}.json",
        }, ensure_ascii=False) + "\n")
    if r.returncode != 0 or not body.strip():
        return None
    try:
        return json.loads(body)
    except Exception:
        return None


def _session_stem(session):
    """Accept both spellings of a session id.

    The DB stores the BARE STEM; sessions/LATEST and emit_data_migration --session
    take the `.md` form; and run_checks.py expands @SESSION@ from the pointer, so a
    registered check receives the `.md` form. CLAUDE.md §7 lists this as a standing
    trap — "getting it wrong scopes a gate to nothing and it passes green" — and
    this module was registered with the wrong one on its first day. Normalise here
    rather than requiring every caller to remember.
    """
    return session[:-3] if session.endswith(".md") else session


def _logged_payloads(session):
    """Every payload logged for a session, newest last, keyed by URL."""
    session = _session_stem(session)
    man = LOG_ROOT / session / "manifest.jsonl"
    if not man.exists():
        return {}
    out = {}
    for line in man.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        p = LOG_ROOT / session / rec["artefact"]
        if p.exists():
            try:
                out[rec["url"]] = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                pass
    return out


def verify_authors(session):
    """Diff stored authors against the LOGGED payload. Offline. No network."""
    session = _session_stem(session)
    payloads = _logged_payloads(session)
    if not payloads:
        print(f"  no retrieval log for session {session!r} under {LOG_ROOT}/")
        print("  EXAMINED: 0")
        print("\n  INDETERMINATE — a session with no logged retrievals cannot be")
        print("  verified offline. That is the gap this module exists to close;")
        print("  it is not a pass.")
        return 1
    by_doi = {}
    for url, m in payloads.items():
        msg = m.get("message") if isinstance(m, dict) else None
        if isinstance(msg, dict) and msg.get("DOI"):
            by_doi[msg["DOI"].lower()] = msg

    cx = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    rows = cx.execute("SELECT ref_id, doi FROM evidence_sources "
                      "WHERE COALESCE(doi,'') <> '' ORDER BY ref_id").fetchall()
    examined, bad, unlogged = 0, [], []
    for ref_id, doi in rows:
        msg = by_doi.get((doi or "").lower())
        if msg is None:
            unlogged.append((ref_id, doi))
            continue
        examined += 1
        real = [(a.get("family") or a.get("name") or "") for a in msg.get("author", [])]
        stored = [r[0] for r in cx.execute(
            "SELECT last_name FROM evidence_source_authors WHERE ref_id=? ORDER BY position",
            (ref_id,))]
        if [_norm(x) for x in real] != [_norm(x) for x in stored]:
            bad.append((ref_id, real, stored))

    print("=" * 74)
    print(f"retrieval_log --verify-authors  session={session}")
    print("=" * 74)
    print(f"  logged payloads: {len(payloads)}   DOI-bearing: {len(by_doi)}")
    print(f"  EXAMINED: {examined}")
    if unlogged:
        print(f"  NO LOGGED RETRIEVAL for {len(unlogged)} source(s) — not verifiable offline:")
        for ref_id, doi in unlogged[:6]:
            print(f"      {ref_id}  {doi}")
    for ref_id, real, stored in bad:
        print(f"  ✗ {ref_id}\n      logged: {'; '.join(real)}\n      stored: {'; '.join(stored)}")
    if bad:
        print(f"\n  {len(bad)} source(s) disagree with the payload the session received.")
        return 1
    if examined == 0:
        print("\n  INDETERMINATE — nothing verifiable. Not a pass.")
        return 1
    print("\n  CLEAN — stored authors match the retrieved payloads, byte-for-byte source.")
    return 0


def backfill(session, sleep=1.0):
    """Log payloads for a session's existing DOI-bearing sources.

    Honest about what this is: a retrieval made NOW, not a recovery of what the
    authoring session received. Marked as such in the manifest so it is never
    mistaken for contemporaneous evidence.
    """
    import time
    cx = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    rows = cx.execute("SELECT ref_id, doi FROM evidence_sources "
                      "WHERE COALESCE(doi,'') <> '' ORDER BY ref_id").fetchall()
    for ref_id, doi in rows:
        fetch(f"https://api.crossref.org/works/{doi}", session,
              purpose=f"BACKFILL (not contemporaneous) crossref metadata for {ref_id}")
        print(f"  logged {ref_id}  {doi}")
        time.sleep(sleep)
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--session", required=True)
    p.add_argument("--verify-authors", action="store_true")
    p.add_argument("--backfill", action="store_true")
    a = p.parse_args()
    if a.backfill:
        sys.exit(backfill(a.session))
    if a.verify_authors:
        sys.exit(verify_authors(a.session))
    p.error("choose --verify-authors or --backfill")


if __name__ == "__main__":
    main()
