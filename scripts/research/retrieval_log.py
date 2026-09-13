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
count, HTTP status, and the UTC timestamp. Writes happen BEFORE the caller sees
the data, so a caller cannot log a different payload than the one it acted on.
`fetch` returns None -- but STILL writes the artefact and manifest line -- for a
non-2xx status as well as for a transport failure or an unparseable body: a 404
or a publisher interstitial is retrieved evidence of a failed retrieval, not
absence of evidence, and CLAUDE.md 5(c) is the reason that distinction is kept
rather than dropped along with the rest of the failure.

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
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path


def _norm(s):
    """Fold accents and case before comparing surnames.

    A stored "Rosas-Perez" against an actual "Rosas-Pérez" is the SAME PERSON
    differently encoded; the failure this module detects is a DIFFERENT person.
    A plain .lower() compare called that a mismatch, which meant this verifier
    and the since-retired scripts/audit/author_fidelity_audit.py — two checks of one
    property, shipped in the same commit — returned opposite answers on REF-00965.
    Two verifiers with divergent match rules is a defect, not depth; the second one
    is gone and this is now the only place the rule lives.

    Typographic punctuation folds the same way and for the same reason. A stored
    "D'Cruz" against a logged "D\u2019Cruz" is one person and one apostrophe in two
    encodings; on 2026-09-02 that difference alone printed a FAIL over REF-00975,
    and a fidelity check that cries wolf on a curly quote teaches its reader to
    skip the one line that matters.
    """
    s = unicodedata.normalize("NFKD", (s or "").strip().lower())
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s.translate(_PUNCT_FOLD)


# Typographic variants that carry no bibliographic information.
_PUNCT_FOLD = {ord(c): "'" for c in "\u2018\u2019\u02bc\u00b4`"}
_PUNCT_FOLD.update({ord(c): '"' for c in "\u201c\u201d"})
_PUNCT_FOLD.update({ord(c): "-" for c in "\u2010\u2011\u2012\u2013\u2014\u2212"})


def _norm_title(s):
    """Compare titles on their WORDS, not their typesetting.

    Crossref renders an en-dash where a DB row carries a hyphen, capitalises
    differently, and sometimes carries trailing whitespace. None of that is a
    bibliographic disagreement. A different WORD is.
    """
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return " ".join("".join(ch if ch.isalnum() else " " for ch in s).split())


def _given_conflict(real, stored):
    """True only when two given names cannot be the same person's.

    "J." against "Jonathan" is one person under two house styles; "Naoji" against
    "Toshiyuki" is a DIFFERENT PERSON, and until 2026-09-02 this module compared
    family names alone, so it printed CLEAN over exactly that substitution in
    REF-00976. The test is provable rather than inferred — an abbreviation is a
    prefix, and nothing else is excused.
    """
    a, b = _given_tokens(real), _given_tokens(stored)
    if not a or not b:
        return False              # one side is silent: incompleteness, not falsehood
    if len(a) != len(b):
        return False              # one house style carries a middle name, one does not
    # Every token must be able to be the other's abbreviation. "h" / "h" and
    # "dirkjan" / "dirkjan" pass; "naoji" / "toshiyuki" cannot.
    return not all(x.startswith(y) or y.startswith(x) for x, y in zip(a, b))


def _given_tokens(s):
    """A given name as its name-parts, with all typesetting discarded.

    Crossref renders Veeger's initials as "Dirkjan (H. E. J.)" where the DB holds
    "Dirkjan H. E. J.", and "Wiebe H.K." against "Wiebe H. K.". Parentheses and
    the spacing of stops are house style. Comparing the raw strings made both of
    those FAILs on 2026-09-02 — noise filed beside the two real substitutions in
    the same run, which is how a real finding gets scrolled past.
    """
    s = _norm(s)
    return "".join(ch if ch.isalnum() else " " for ch in s).split()

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
    # ACCEPTS BYTES as of 2026-09-02. It previously took str, which forced fetch() to
    # decode the body before sniffing it -- and that decode is what silently corrupted
    # every non-UTF-8 artefact. Binary formats are identified by magic number, which is
    # what they are actually identified by; the text branches decode a small head
    # tolerantly, because a sniffer must never raise on the bytes it is inspecting.
    if isinstance(body, bytes):
        raw = body.lstrip()[:512]
        if raw.startswith(b"%PDF-"):
            return ".pdf"                  # the format Co-1 and DPO evidence arrives in
        if raw[:4] in (b"PK\x03\x04", b"PK\x05\x06"):
            return ".zip"                  # .docx/.xlsx/.epub are zips; do not claim more
        if raw.startswith(b"\xd0\xcf\x11\xe0"):
            return ".doc"                  # OLE2: legacy .doc/.xls
        if raw[:3] == b"\xef\xbb\xbf":
            raw = raw[3:]                  # strip a UTF-8 BOM before the text sniffs
        head = raw.decode("utf-8", errors="replace").lstrip()
    else:
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

    Returns None on ANY failure: curl itself failing (no HTTP response at all), an
    empty body, a body that is not JSON -- OR, as of 2026-09-13, an HTTP status
    outside 2xx. The artefact and the manifest line are written regardless: a
    failed retrieval is still evidence of what was attempted and what came back,
    and CLAUDE.md 5(c) is exactly the case for keeping it (see `status` below).
    """
    # BYTES, NOT TEXT, AND FOLLOW REDIRECTS. Both fixed 2026-09-02 after measurement.
    #
    # This function's docstring promises "the artefact on disk is the bytes the caller
    # actually received". With `text=True` that promise was FALSE for every non-UTF-8
    # body, and false SILENTLY -- no exception, exit code 0. curl decoded the bytes with
    # replacement characters, `body.encode("utf-8")` re-encoded the damaged text, and the
    # manifest recorded a sha256 of the damage. Measured on a real RCOT PDF: stored
    # bdfeba45..., actually received ab78cbbc... . A logger whose hash does not identify
    # what arrived cannot support the fidelity audit it exists for, and PDF is the format
    # Co-1 and disability-led evidence overwhelmingly arrives in.
    #
    # `-L` because a DOI is a 302. Without it the artefact was the redirect stub: one
    # 0-byte figshare line sits in this session's manifest as evidence of exactly that.
    #
    # This is the ROOT CAUSE of D04-032, which was closed on 2026-09-02 by reconstructing
    # a manifest for 58 unlogged payloads. That fix treated the symptom -- it never asked
    # why the payloads were unlogged. This is why.
    #
    # HTTP STATUS, NOT JUST EXIT CODE. Fixed 2026-09-13. `curl` without `--fail` exits 0
    # for ANY completed HTTP transaction, 404 and publisher interstitial included -- the
    # body it hands back is an error page, and until now the manifest recorded that as a
    # successful retrieval indistinguishable from the real thing. `-o <tempfile> -w
    # '%{http_code}'` sends the body straight to disk untouched and returns ONLY the
    # final status code (final, because of `-L`: the code after redirects are followed,
    # which is the code for the bytes actually stored) on stdout -- so the body is never
    # routed through Python at all before being read back as bytes, and the "capture
    # bytes exactly" promise above is unaffected by this change; it is the same promise,
    # applied one file-write earlier. A transport failure that never got an HTTP response
    # (DNS, TLS, timeout before headers) reports "000" from curl, which is not a status
    # and is stored as `status: null` rather than invented as 0 or 200.
    fd, tmp_path = tempfile.mkstemp(prefix="retrieval-log-", suffix=".tmp")
    os.close(fd)
    tmp = Path(tmp_path)
    try:
        r = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", str(timeout),
             "-o", str(tmp), "-w", "%{http_code}", url],
            capture_output=True)
        body = tmp.read_bytes() if tmp.exists() else b""  # bytes, straight off disk
    finally:
        tmp.unlink(missing_ok=True)
    code_raw = r.stdout.decode("ascii", errors="replace").strip()
    # curl's own sentinel for "no HTTP response was ever received" is the literal
    # string "000" (measured: a proxy CONNECT failure prints it, curl exit 56).
    # That is not a status code -- 0 is not in any HTTP spec -- so it is None, the
    # same as a stdout curl could not produce a code for at all.
    status = (int(code_raw) if code_raw.isdigit() and len(code_raw) == 3
               and code_raw != "000" else None)
    d = LOG_ROOT / _session_stem(session)
    d.mkdir(parents=True, exist_ok=True)
    sha = hashlib.sha256(body).hexdigest()  # of what arrived, not of a lossy decode
    artefact = f"{sha[:16]}{_extension_for(body)}"
    (d / artefact).write_bytes(body)
    with open(d / "manifest.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps({
            "retrieved_at": stamp or _now(), "url": url, "purpose": purpose,
            "sha256": sha, "bytes": len(body), "exit": r.returncode,
            "status": status, "artefact": artefact,
        }, ensure_ascii=False) + "\n")
    if r.returncode != 0 or not body.strip():
        return None
    if status is None or not (200 <= status < 300):
        return None                        # HTTP-layer failure: recorded above, not hidden
    try:
        # Decode ONLY to parse, never to store. A binary body simply is not JSON, and
        # `errors="replace"` keeps that a clean None rather than an exception raised
        # after the artefact is already safely on disk.
        return json.loads(body.decode("utf-8", errors="replace"))
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


def _manifest_records(session):
    """Every manifest line for a session, in file order. The record of what was FETCHED.

    Separate from _logged_payloads because the two answer different questions:
    this one says what bytes exist, that one says which of them this module can
    parse. Conflating them is how the drop below stayed invisible.
    """
    session = _session_stem(session)
    man = LOG_ROOT / session / "manifest.jsonl"
    if not man.exists():
        return []
    return [json.loads(line) for line in man.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def _logged_payloads(session):
    """Every payload logged for a session, newest last, keyed by URL.

    JSON ONLY, and that is a real limit rather than an implementation detail: a
    payload whose bytes are not JSON is dropped here and this dict is the input to
    every comparison the module makes. Callers that report on coverage MUST call
    _unparsed_payloads() as well; the CONTRACT of this function is deliberately
    unchanged (scripts/db.py's correct-source path depends on it returning parsed
    Crossref-shaped dicts), so the honesty has to be added beside it, not inside it.
    """
    session = _session_stem(session)
    out = {}
    for rec in _manifest_records(session):
        p = LOG_ROOT / session / rec["artefact"]
        if p.exists():
            try:
                out[rec["url"]] = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                pass
    return out


def _unparsed_payloads(session):
    """The payloads _logged_payloads() drops. Returns [(artefact, url, why), ...].

    ADDED 2026-09-10, because the drop was a bare `except: pass` and therefore
    silent. On the 2026-09-02 batch it discards every .xml and .pdf artefact in the
    log — including the PubMed efetch abstracts behind REF-00971/972/974 and the PMC
    full text behind REF-00973, which are exactly the bytes that carry the study
    DESIGN that `evidence_sources.scope` is derived from. A verifier that cannot see
    the design-bearing bytes and prints CLEAN is CLAUDE.md 5(a) at the input.

    This function does not fix that. It makes it PRINTABLE, so no CLEAN verdict is
    issued over an unstated blind spot. Teaching the module to read PubMed XML was
    weighed and declined on 2026-09-10: measured on the live corpus, every
    DOI-bearing source already indexes through a richer Crossref or Unpaywall
    payload, so an adapter would newly examine nothing today while risking the
    displacement of richer records in _index_by_doi's ranking. It is recorded as
    owed work in workplan/2026-09-10-b5b-scope-owner-escalation.md §7 rather than
    half-built here.
    """
    session = _session_stem(session)
    out = []
    for rec in _manifest_records(session):
        p = LOG_ROOT / session / rec["artefact"]
        if not p.exists():
            out.append((rec["artefact"], rec.get("url", ""), "artefact missing from disk"))
            continue
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            ext = p.suffix or "(no extension)"
            why = f"not JSON ({ext}); this module parses Crossref-shaped JSON only"
            out.append((rec["artefact"], rec.get("url", ""), why))
    return out


def _failed_retrievals(session):
    """Manifest lines whose retrieval did not succeed at the HTTP layer.

    Added 2026-09-13 alongside the `status` field. A record here means the artefact
    and manifest line exist -- evidence that an attempt was made and exactly what
    came back -- but the bytes are NOT a usable retrieval: either curl itself never
    got an HTTP response (`exit` != 0) or it did and the final status (after any
    redirect -L followed) was outside 2xx.

    Older manifest lines, written before this field existed, carry no `status` key
    at all. Those are read here as UNKNOWN, never as failed: a missing field is
    silence, and silence is not evidence of failure any more than it was evidence
    of success (the defect this whole module exists to correct, one field over).

    Deliberately does NOT change what `_logged_payloads()` returns -- that
    function's docstring already establishes the pattern this follows: honesty
    about a payload's status is added BESIDE the parser, never folded inside it,
    so a caller with an older, narrower notion of what that function returns (see
    scripts/db.py's correct_source, which depends on its contract) is not silently
    handed different data.
    """
    session = _session_stem(session)
    out = []
    for rec in _manifest_records(session):
        exit_code = rec.get("exit", 0)
        status = rec.get("status")
        if exit_code != 0:
            out.append((rec.get("artefact", ""), rec.get("url", ""),
                        f"curl exit {exit_code}: no HTTP response reached"))
        elif status is not None and not (200 <= status < 300):
            out.append((rec.get("artefact", ""), rec.get("url", ""), f"HTTP {status}"))
    return out


# Locator columns a source may carry INSTEAD of a DOI, in the order they are tried
# against the manifest. REF-00978 -- the corpus's only Co-1 source, whose warrant
# CLAUDE.md 6 calls "the worst failure available here" -- has no DOI at all: it is a
# PDF URL. Until 2026-09-10 verify_authors() selected `WHERE COALESCE(doi,'') <> ''`,
# so that row was filtered out BEFORE the loop and never reached the `unlogged` list
# either. Output: EXAMINED: 8 of nine sources, verdict CLEAN, and nothing anywhere
# said which one was missing.
_ALT_LOCATORS = ("url", "pmid", "pmcid", "handle", "isbn")


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

# Columns any one of which may legitimately carry the payload's title. A
# non-English source stores its native title in `pub_title` and the English in
# `pub_title_en`, so a payload title matching EITHER is a match. Checked as a set,
# never as a single column, or every Japanese admission reads as a fabrication.
_TITLE_COLS = ("pub_title", "pub_title_en", "original_title", "chapter_title", "book_title")


def _index_by_doi(payloads):
    """Every logged payload that identifies a DOI, whatever service produced it.

    Until 2026-09-02 this read `message.DOI` alone — the shape Crossref returns for
    a single work. Unpaywall files the DOI at top level and its authors under
    `z_authors`; a Crossref SEARCH files works under `message.items`. Three of this
    batch's eight sources were logged only in those shapes, and the verifier
    reported them as "NO LOGGED RETRIEVAL … not verifiable offline" — a shrug
    printed over evidence that was sitting on disk. An indexer that sees one
    vendor's envelope and calls the rest unlogged is CLAUDE.md 2(a) at the input.

    Richer envelopes win: a Crossref work carries volume/issue/page that Unpaywall
    does not, so it must not be displaced by a thinner record of the same DOI.
    """
    ranked = {}
    def offer(doi, msg, rank):
        if not doi:
            return
        doi = str(doi).strip().lower()
        if doi and rank >= ranked.get(doi, (-1, None))[0]:
            ranked[doi] = (rank, msg)

    for _url, m in payloads.items():
        if not isinstance(m, dict):
            continue
        msg = m.get("message")
        if isinstance(msg, dict) and msg.get("DOI"):
            offer(msg["DOI"], msg, 3)                       # Crossref, single work
        elif isinstance(msg, dict) and isinstance(msg.get("items"), list):
            for it in msg["items"]:                         # Crossref, search result
                if isinstance(it, dict) and it.get("DOI"):
                    offer(it["DOI"], it, 2)
        elif m.get("doi") and ("z_authors" in m or "title" in m):
            offer(m["doi"], _from_unpaywall(m), 1)          # Unpaywall
    return {d: msg for d, (_r, msg) in ranked.items()}


def _from_unpaywall(m):
    """Re-shape an Unpaywall record into the Crossref keys this module compares.

    Only the fields Unpaywall states are carried across. It has no volume, issue or
    page, and inventing empties for them here would turn silence into a claim.
    """
    out = {"DOI": m.get("doi"), "title": [m.get("title")] if m.get("title") else [],
           "author": [a for a in (m.get("z_authors") or []) if isinstance(a, dict)]}
    if m.get("year"):
        out["issued"] = {"date-parts": [[int(m["year"])]]}
    return out


def _author_conflict(real, stored):
    """Do the payload's authors and the DB's disagree about WHO they are?

    Family names must line up in order. Given names are then checked for
    substitution — the check this module did not have on 2026-09-02, when
    REF-00976 stored HASEGAWA Toshiyuki over a payload that said HASEGAWA Naoji
    and printed CLEAN, because five surnames matched and nothing looked further.
    """
    if [_norm(f) for f, _ in real] != [_norm(f) for f, _ in stored]:
        return True
    return any(_given_conflict(gr, gs) for (_, gr), (_, gs) in zip(real, stored))


def _disp(family, given):
    return ", ".join(x for x in (family, given) if x) or "?"


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

    want_title = next((t for t in (msg.get("title") or []) if t), None)
    if want_title:
        haves = [row[c] for c in _TITLE_COLS if c in row.keys() and row[c]]
        if not haves:
            gaps.append(("pub_title", want_title))
        elif not any(_norm_title(h) == _norm_title(want_title) for h in haves):
            mismatches.append(("pub_title", haves[0], want_title))
    return mismatches, gaps


def _locator_evidence(row, manifest):
    """For a source with no DOI: which logged artefact, if any, stands behind it.

    Returns (label, locator, [(artefact, url), ...]). A hit proves a retrieval was
    made for that locator; it does NOT prove the authors are right, and this
    function never claims it does. Matching is on the manifest URL containing the
    locator, which is provable from the bytes rather than inferred.
    """
    for col in _ALT_LOCATORS:
        val = row[col] if col in row.keys() else None
        val = (str(val).strip() if val is not None else "")
        if not val:
            continue
        hits = [(r["artefact"], r.get("url", "")) for r in manifest
                if val in (r.get("url") or "")]
        return col, val, hits
    return None, None, []


def verify_authors(session):
    """Diff stored authors against the LOGGED payload. Offline. No network.

    EXAMINES EVERY evidence_sources ROW as of 2026-09-10, not only DOI-bearing ones,
    and prints its denominator. A row this module cannot author-diff is now named in
    an UNEXAMINABLE block with the reason, and its existence is carried into the
    closing verdict, so "CLEAN" can never again read as a statement about the whole
    corpus while a source sits silently outside the query that selected it.
    """
    session = _session_stem(session)
    payloads = _logged_payloads(session)
    if not payloads:
        print(f"  no retrieval log for session {session!r} under {LOG_ROOT}/")
        print("  EXAMINED: 0")
        print("\n  INDETERMINATE — a session with no logged retrievals cannot be")
        print("  verified offline. That is the gap this module exists to close;")
        print("  it is not a pass.")
        return 1
    by_doi = _index_by_doi(payloads)

    manifest = _manifest_records(session)
    unparsed = _unparsed_payloads(session)
    failed = _failed_retrievals(session)

    cx = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    cx.row_factory = sqlite3.Row
    rows = cx.execute("SELECT * FROM evidence_sources ORDER BY ref_id").fetchall()
    n_rows = len(rows)
    n_doi = sum(1 for r in rows if (r["doi"] or "").strip())
    examined, bad, unlogged, unexaminable = 0, [], [], []
    biblio_bad, biblio_gap = [], []
    for row in rows:
        ref_id, doi = row["ref_id"], (row["doi"] or "").strip()
        if not doi:
            # NOT a skip. A source with no DOI is located by whatever locator it
            # does have and reported, with or without a hit.
            col, val, hits = _locator_evidence(row, manifest)
            unexaminable.append((ref_id, col, val, hits))
            continue
        msg = by_doi.get(doi.lower())
        if msg is None:
            unlogged.append((ref_id, doi))
            continue
        examined += 1
        real = [((a.get("family") or a.get("name") or ""), (a.get("given") or ""))
                for a in msg.get("author", [])]
        stored = [tuple(r) for r in cx.execute(
            "SELECT last_name, COALESCE(first_name,'') FROM evidence_source_authors "
            "WHERE ref_id=? ORDER BY position", (ref_id,))]
        if _author_conflict(real, stored):
            bad.append((ref_id, [_disp(*a) for a in real], [_disp(*a) for a in stored]))
        mm, gp = _biblio_divergences(msg, row)
        if mm:
            biblio_bad.append((ref_id, mm))
        if gp:
            biblio_gap.append((ref_id, gp, row["metadata_quality"]))

    print("=" * 74)
    print(f"retrieval_log --verify-authors  session={session}")
    print("=" * 74)
    print(f"  logged payloads: {len(payloads)} parsed of {len(manifest)} manifest line(s)"
          f"   DOI-bearing: {len(by_doi)}")
    print(f"  EXAMINED: {examined} of {n_rows} evidence_sources row(s) "
          f"— {n_doi} carry a DOI, {n_rows - n_doi} do not")
    if unexaminable:
        n = len(unexaminable)
        print(f"\n  UNEXAMINABLE — {n} source{'' if n == 1 else 's'} carr"
              f"{'ies' if n == 1 else 'y'} no DOI, so this module cannot")
        print("  diff its authors against a Crossref-shaped payload. REPORTED, never")
        print("  skipped: the CLEAN verdict below does not speak for it.")
        for ref_id, col, val, hits in unexaminable:
            if col is None:
                print(f"      {ref_id}  no DOI and no alternative locator on the row at all")
                continue
            shown = str(val)[:78] + ("…" if len(str(val)) > 78 else "")
            print(f"      {ref_id}  no DOI; locator {col}={shown}")
            if hits:
                for art, _u in hits:
                    print(f"          logged artefact {art} matches this locator — the retrieval "
                          f"happened; its bytes are not author-diffable here")
            else:
                print("          NO logged artefact matches this locator — not verifiable offline")
    if unparsed:
        tally = {}
        for art, _u, _w in unparsed:
            tally[Path(art).suffix or "(none)"] = tally.get(Path(art).suffix or "(none)", 0) + 1
        print(f"\n  NOT INGESTED — {len(unparsed)} of {len(manifest)} logged payload(s) are bytes")
        print("  this module cannot parse: " + ", ".join(
            f"{n}×{ext}" for ext, n in sorted(tally.items(), key=lambda kv: -kv[1])) + ".")
        print("  They were retrieved and are on disk, and they are outside every comparison")
        print("  above — including the PubMed/PMC XML that carries the study DESIGN from which")
        print("  evidence_sources.scope is derived.")
        for art, url, why in unparsed:
            print(f"      {art}  {why}")
            print(f"          {url[:96]}")
    if failed:
        print(f"\n  FAILED RETRIEVALS — {len(failed)} of {len(manifest)} logged attempt(s) did not")
        print("  reach a usable HTTP response (see `status`/`exit` on the manifest line). The")
        print("  artefact and manifest line exist as evidence of the attempt; nothing here is")
        print("  treated as a payload by any comparison in this module.")
        for art, url, why in failed:
            print(f"      {art}  {why}")
            print(f"          {url[:96]}")
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
    scope = (f"the {examined} of {n_rows} source(s) examined"
             if examined != n_rows else f"all {n_rows} source(s)")
    print(f"\n  CLEAN FOR {scope.upper()} — their stored authors and asserted")
    print("  bibliographic fields match the retrieved payloads, byte-for-byte source." + tail)
    if unexaminable or unlogged or unparsed or failed:
        print("  NOT A WHOLE-CORPUS PASS: see the block(s) above for what this verdict")
        print("  does not cover. A source outside the comparison is not a source that agreed.")
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
            # No `status` key. This line was never produced by fetch() reading curl's
            # -w output -- there is no HTTP status to report, and "200" would be a
            # fabrication of exactly the kind this module exists to catch. `exit: 0`
            # is kept as a literal true fact (the file read cleanly), not a stand-in
            # for a status this path never observed. `_failed_retrievals()` reads a
            # missing `status` as unknown, never as failed, for the same reason.
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
