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


def _extension_for(body):
    """Name the artefact for what it CONTAINS, not for what we hoped to fetch.

    Fixed 2026-08-22 (defect B5-f, commit e326e46). Every artefact was written as
    `<sha16>.json` regardless of content type, so a full-text attempt that returned
    HTML, XML or an empty body landed as an unparseable `.json` — and `check_json`
    (registry `syntax` battery, kinds `[always]`, **BLOCKING**) parses every .json in
    the tree. Six of fifteen artefacts failed it on 2026-08-20. That was repaired IN
    DATA ONLY, by hand-renaming the offending files and hand-editing the manifest, so
    the gate passed while the cause stayed live: the very next non-JSON retrieval
    would have re-reddened CI, and "attempt the publisher full text" is exactly the
    R10 ladder rung that returns HTML.

    Sniff the body rather than trusting the URL: `api.crossref.org` can return an
    HTML error page, and a repository PDF endpoint can return JSON metadata.
    """
    head = body.lstrip()[:512]
    if not head:
        return ".txt"                      # a recorded empty response is evidence too
    if head[0] in "{[":
        try:
            json.loads(body)
            return ".json"
        except Exception:
            pass                           # looks like JSON, is not — do not claim .json
    low = head.lower()
    if low.startswith("<?xml") or low.startswith("<!doctype xml"):
        return ".xml"
    if low.startswith("<!doctype html") or low.startswith("<html") or "<html" in low[:200]:
        return ".html"
    if low.startswith("<"):
        return ".xml"
    return ".txt"


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
    artefact = f"{sha[:16]}{_extension_for(body)}"
    (d / artefact).write_text(body, encoding="utf-8")
    with open(d / "manifest.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps({
            "retrieved_at": stamp or _now(), "url": url, "purpose": purpose,
            "sha256": sha, "bytes": len(body), "exit": r.returncode,
            "artefact": artefact,
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


# Bibliographic fields this verifier can check against a Crossref payload, and the
# payload key each is derived from. Deliberately NOT exhaustive: only fields where
# the payload is unambiguously authoritative.
_BIBLIO_FIELDS = (
    ("volume",         lambda m: m.get("volume")),
    ("issue",          lambda m: m.get("issue")),
    ("article_number", lambda m: m.get("article-number")),
    ("pages",          lambda m: m.get("page")),
    ("pub_year",       lambda m: (((m.get("issued") or {}).get("date-parts") or [[]])[0] or [None])[0]),
)


def _biblio_divergences(msg, row):
    """Return (mismatches, gaps) for one source against its payload.

    The distinction is the whole point, and it is the distinction the 2026-08-19
    batch collapsed:

      MISMATCH  the DB asserts a value the payload contradicts. That is a FALSE
                bibliographic field — the same defect class as a fabricated author,
                one field over. REF-00968 carried `pages = '2645738'` while its
                payload filed 2645738 as `article-number` with `page` null: a true
                value in the wrong column, which reads downstream as a page range.
      GAP       the DB is NULL where the payload has a value. Incompleteness, not
                falsehood — reported, never failed. But a row stamped
                metadata_quality='COMPLETE' with gaps is asserting something untrue
                ABOUT ITSELF, so the count is printed where a reader will see it.

    Added 2026-08-22. Until then this module compared authors only, which is why it
    printed CLEAN over five rows whose volume, issue, pages_*, article_number and
    issn were all NULL while the payloads on disk supplied every one of them. A
    checker that examines one field class and reports on the record as a whole is
    the vacuity CLAUDE.md 2(a) names, at field granularity.
    """
    mismatches, gaps = [], []
    artno = str(msg.get("article-number") or "").strip()
    for col, get in _BIBLIO_FIELDS:
        want = get(msg)
        have = row[col] if col in row.keys() else None
        if want in (None, ""):
            # The payload asserts nothing for this field. Usually nothing to say —
            # EXCEPT the mis-file signature: the DB holds a value here that the
            # payload files under a DIFFERENT key. Caught by equality with
            # article-number, which is provable rather than inferred, so this
            # cannot fire on a row whose editor simply had a better source than
            # Crossref. This is the REF-00968 case and the reason this branch
            # exists: `pages = '2645738'` with `page` null and
            # `article-number = '2645738'` is a true value in a false column, and
            # every gate in the repository passed it.
            if col == "pages" and have not in (None, "") and str(have).strip() == artno and artno:
                mismatches.append((col, have,
                                   f"<null>  — the payload files {artno!r} as article-number, "
                                   f"not as a page range; this is a MIS-FILE, move it"))
            continue
        if have in (None, ""):
            gaps.append((col, want))
        elif str(have).strip() != str(want).strip():
            mismatches.append((col, have, want))
    return mismatches, gaps


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
    cx.row_factory = sqlite3.Row
    rows = cx.execute("SELECT * FROM evidence_sources "
                      "WHERE COALESCE(doi,'') <> '' ORDER BY ref_id").fetchall()
    examined, bad, unlogged = 0, [], []
    biblio_bad, biblio_gap = [], []
    for row in rows:
        ref_id, doi = row["ref_id"], row["doi"]
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
        mm, gp = _biblio_divergences(msg, row)
        if mm:
            biblio_bad.append((ref_id, mm))
        if gp:
            biblio_gap.append((ref_id, gp, row["metadata_quality"]))

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

    if biblio_gap:
        n = sum(len(g) for _, g, _ in biblio_gap)
        print(f"\n  BIBLIOGRAPHIC GAPS — {n} field(s) NULL in the DB that the payload supplies.")
        print("  Incompleteness, not falsehood: reported, not failed.")
        for ref_id, gp, mq in biblio_gap:
            flag = "  <-- while stamped metadata_quality='COMPLETE'" if mq == "COMPLETE" else ""
            print(f"      {ref_id}{flag}")
            for col, want in gp:
                print(f"          {col} is NULL; payload has {want!r}")
    for ref_id, mm in biblio_bad:
        print(f"  ✗ {ref_id} BIBLIOGRAPHIC MISMATCH")
        for col, have, want in mm:
            print(f"          {col}: stored {have!r}, payload {want!r}")

    if bad or biblio_bad:
        if bad:
            print(f"\n  {len(bad)} source(s) disagree with the payload on AUTHORS.")
        if biblio_bad:
            print(f"  {len(biblio_bad)} source(s) assert a bibliographic field the payload contradicts.")
        return 1
    if examined == 0:
        print("\n  INDETERMINATE — nothing verifiable. Not a pass.")
        return 1
    tail = "" if not biblio_gap else " Bibliographic gaps above are reported, not failed."
    print("\n  CLEAN — stored authors and asserted bibliographic fields match the")
    print("  retrieved payloads, byte-for-byte source." + tail)
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


def reconstruct_manifest(session):
    """Build a manifest for payloads that are on disk with no manifest line.

    WHY THIS EXISTS, AND WHY backfill() CANNOT DO IT. backfill() iterates
    `evidence_sources WHERE doi <> ''` and re-fetches. That input is exactly what a
    retraction deletes, so a session whose evidence was retracted can never be
    reconstructed by it -- measured 2026-09-02 on the 2026-09-01 circulation batch:
    58 payload files on disk, evidence_sources at 0 rows, backfill exiting 0 in
    silence having logged nothing. And _logged_payloads() returns {} without a
    manifest, so those files are invisible to --verify-authors: the anti-fabrication
    check cannot see the very artefacts written to defeat fabrication.

    WHAT THIS IS, STATED SO IT CANNOT BE MISREAD. Every line it writes carries
    `"reconstructed": true`. The URL is derived from the DOI INSIDE each payload,
    never from its filename -- a filename is a claim by whoever named it, the
    payload's own message.DOI is the retrieved bytes speaking. `retrieved_at` is the
    file mtime, which is when the file was written and not necessarily when the
    request was made.

    THE PROVENANCE HALF IS WEAKER THAN A CONTEMPORANEOUS LINE AND MUST NOT BE
    TREATED AS EQUAL. sha256 here verifies the file against itself, which proves
    nothing about what a server sent. What this DOES restore is the half that caught
    the 2026-08-19 fabrication: the content check, stored author rows against the
    author array in the payload the session actually held. That check is real
    whether the manifest line was written at fetch time or reconstructed after.
    """
    session = _session_stem(session)
    d = LOG_ROOT / session
    if not d.is_dir():
        print(f"  no retrieval log directory for {session!r}")
        print("  EXAMINED: 0")
        return 1
    man = d / "manifest.jsonl"
    known = set()
    if man.exists():
        for line in man.read_text(encoding="utf-8").splitlines():
            if line.strip():
                known.add(json.loads(line).get("artefact"))
    written = skipped = 0
    lines = []
    for f in sorted(d.iterdir()):
        if not f.is_file() or f.name == "manifest.jsonl" or f.name in known:
            continue
        raw = f.read_text(encoding="utf-8", errors="replace")
        try:
            doc = json.loads(raw)
        except Exception:
            skipped += 1          # not JSON: a PDF, a .doc, an HTML error page
            continue
        msg = doc.get("message") if isinstance(doc, dict) else None
        doi = msg.get("DOI") if isinstance(msg, dict) else None
        if not doi:
            skipped += 1          # JSON, but not a single-work Crossref payload
            continue
        lines.append(json.dumps({
            "retrieved_at": datetime.fromtimestamp(
                f.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "url": f"https://api.crossref.org/works/{doi}",
            "purpose": ("RECONSTRUCTED 2026-09-02 from a payload already on disk. NOT a "
                        "contemporaneous fetch record: the URL is derived from the payload's "
                        "own message.DOI, retrieved_at is the file mtime, and sha256 hashes "
                        "the stored file rather than a server response. Restores the CONTENT "
                        "check only."),
            "sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            "bytes": len(raw), "exit": 0, "artefact": f.name,
            "reconstructed": True,
        }, ensure_ascii=False))
        written += 1
    if lines:
        with open(man, "a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
    print(f"  reconstructed {written} manifest line(s); skipped {skipped} "
          f"non-Crossref file(s) (PDF/doc/HTML/query results carry no single message.DOI)")
    print(f"  EXAMINED: {written + skipped}")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--session", required=True)
    p.add_argument("--verify-authors", action="store_true")
    p.add_argument("--backfill", action="store_true")
    p.add_argument("--reconstruct-manifest", action="store_true",
                   help="rebuild manifest lines for payloads already on disk; "
                        "marks every line reconstructed=true")
    a = p.parse_args()
    if a.reconstruct_manifest:
        sys.exit(reconstruct_manifest(a.session))
    if a.backfill:
        sys.exit(backfill(a.session))
    if a.verify_authors:
        sys.exit(verify_authors(a.session))
    p.error("choose --verify-authors, --backfill or --reconstruct-manifest")


if __name__ == "__main__":
    main()
