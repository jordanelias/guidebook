#!/usr/bin/env python3
"""retrieval_log --verify-authors, PRESENCE MODE (I6): every verdict proven on fixtures.

WHY THIS EXISTS, as CLAUDE.md section 8 requires. A session whose payloads are
publication pages and PDFs -- the form Co-1, DPO and standards evidence arrives in --
has no Crossref record to diff against, and `--verify-authors` used to stop at
INDETERMINATE there. So a person-author typed from memory onto such a source passed
every gate: the 2026-08-19 failure (CLAUDE.md 5(c)) with nothing pointed at it.
Presence mode looks for each stored surname and the title in the persisted bytes.
What reaches the guidebook without these cases: an invented co-author on an HTML or
PDF source, cited in the book as a person who wrote the work.

The cases prove: a present author passes and the verdict is never CLEAN; an absent
author or title fails with the source named; a one-word title head is not taken as
evidence; a two-letter surname inside a longer word does not count as present; a PDF is read through its text-extraction child; a source with no
artefact, or only a failed (403) retrieval, is UNEXAMINABLE and not counted; an absent
corporate author is reported, not failed; and the JSON path's exit codes are unchanged.

Runs on a COPY of the canonical database and an empty temporary retrieval log, through
the module's own environment variables (GUIDEBOOK_DB_PATH, GUIDEBOOK_RETRIEVAL_LOG).
Fixture sources are admitted through `db.py add-source` on the copy. Manifest lines are
written by hand because the only writer of a retrieved line is `fetch()`, which needs
the network; each line has the shape `fetch()` writes.
"""
import hashlib
import json
import os
import pathlib
import shutil
import sqlite3
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
TMP = tempfile.mkdtemp(prefix="author-presence-")
DB = os.path.join(TMP, "guidebook.db")
LOG = os.path.join(TMP, "retrieval-log")
shutil.copy(REPO / "data" / "guidebook.db", DB)
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO))
os.environ["GUIDEBOOK_DB_PATH"] = DB          # before dbcore resolves a path
import dbcore  # noqa: E402
from schemas.tier_derivation import VALID_SCOPES_BY_TYPE, derive_tier  # noqa: E402

ENV = dict(os.environ, GUIDEBOOK_DB_PATH=DB, GUIDEBOOK_RETRIEVAL_LOG=LOG)
GREY_TIER = str(derive_tier("grey", next(iter(VALID_SCOPES_BY_TYPE["grey"]))))
results = []


def record(tid, name, passed, details=""):
    results.append(bool(passed))
    print(f"  [{'✓' if passed else '✗'}] {tid}: {name}")
    if details and not passed:
        print(f"      {details}")


def next_ref():
    c = sqlite3.connect(DB)
    try:
        return dbcore.next_ref_id(c)
    finally:
        c.close()


def admit(session, title, authors, *extra):
    """One fixture source through db.py add-source on the copy. Returns its ref_id."""
    ref = next_ref()
    args = [sys.executable, str(REPO / "scripts" / "db.py"), "add-source",
            "--ref-id", ref, "--year", "2020", "--title", title,
            "--tier", GREY_TIER, "--evidence-type", "grey", "--session", session]
    for a in authors:
        args += ["--author", a]
    r = subprocess.run(args + list(extra), env=ENV, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"fixture add-source refused: {r.stderr[-400:]}")
    return ref


def artefact(session, body, url, ref_id=None, status=200, content_type="text/html",
             derived_from=None, kind=None):
    """Write `body` and its manifest line, in the shape fetch()/_append_derived write."""
    d = pathlib.Path(LOG) / session
    d.mkdir(parents=True, exist_ok=True)
    raw = body if isinstance(body, bytes) else body.encode("utf-8")
    sha = hashlib.sha256(raw).hexdigest()
    ext = ".pdf" if raw.startswith(b"%PDF-") else (
        ".json" if raw.lstrip()[:1] in (b"{", b"[") else
        ".txt" if derived_from else ".html")
    name = sha[:16] + ext
    (d / name).write_bytes(raw)
    line = {"retrieved_at": "2099-01-01T00:00:00+00:00", "url": url, "purpose": "fixture",
            "ref_id": ref_id, "sha256": sha, "bytes": len(raw), "exit": 0,
            "status": None if derived_from else status, "artefact": name,
            "content_type": content_type}
    if derived_from:
        line.update({"url": f"derived:{kind}/{sha[:16]}/{derived_from}", "derived": True,
                     "derived_from": derived_from, "derivation_kind": kind})
    with open(d / "manifest.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(line, ensure_ascii=False) + "\n")
    return name


def verify(session):
    return subprocess.run([sys.executable, str(REPO / "scripts" / "research" /
                                               "retrieval_log.py"),
                           "--session", session, "--verify-authors"],
                          env=ENV, capture_output=True, text=True)


def examined(out):
    lines = [ln.strip() for ln in out.splitlines() if ln.strip().startswith("EXAMINED:")]
    return lines[0] if lines else None


try:
    # ── A: every asserted field present ────────────────────────────────────────
    SA = "session_2099-01-01-author-presence-a"
    TITLE = "Ramp gradients and wheelchair users: a field study"
    RA1 = admit(SA, TITLE, ["Okonkwo|Adaeze", "Pérez-Lindqvist|M."],
                "--url", "https://example.org/ramp-study")
    artefact(SA, "<html><h1>Ramp gradients and wheelchair users</h1>"
                 "<p>Adaeze Okonkwo and M. P&eacute;rez-Lindqvist</p></html>",
             "https://example.org/ramp-study")                       # matched by url
    RA2 = admit(SA, "Kerb ramps for blind pedestrians — a survey", ["Tanaka-Holm|J."])
    pdf = artefact(SA, b"%PDF-1.4\n%fixture bytes, not a text layer\n",
                   "https://example.org/kerb.pdf", ref_id=RA2,
                   content_type="application/pdf")
    artefact(SA, "Kerb ramps for blind pedestrians\nJ. Tanaka-\nHolm, 2020",
             None, derived_from=pdf, kind="text-extraction", content_type=None)
    RA3 = admit(SA, "Accessible counters, a guide", ["corp|Fixture Gloss Council"])
    artefact(SA, "<title>Accessible counters, a guide</title>",
             "https://example.org/counters", ref_id=RA3)
    RA4 = admit(SA, "A source this session filed and never retrieved", ["Mbeki|T."])

    r = verify(SA)
    out = r.stdout
    # THE CASE THAT FAILS ON THE OLD CODE: it printed INDETERMINATE and exited 1 for
    # every session whose payloads were not JSON.
    record("P01", "every asserted field present -> exit 0, PRESENT-IN-BYTES 3 of 3, "
           "EXAMINED 3", r.returncode == 0 and examined(out) == "EXAMINED: 3"
           and "PRESENT-IN-BYTES: 3 of 3 source(s); not Crossref-diffed; cannot detect "
           "an omitted author" in out, f"rc={r.returncode} {out[-900:]!r}")
    record("P02", "the verdict never says CLEAN", r.returncode == 0 and "CLEAN" not in out,
           out[-400:])
    record("P03", "a PDF is read through its text-extraction child (a name split by a "
           "line-break hyphen still counts)", r.returncode == 0 and f"✗ {RA2}" not in out,
           out[-600:])
    record("P04", "a filed source with no artefact is UNEXAMINABLE and not counted",
           "UNEXAMINABLE" in out and RA4 in out.split("UNEXAMINABLE", 1)[-1].split(
               "EXAMINED:", 1)[0], out[-600:])
    record("P05", "an absent corporate author is REPORTED, not failed",
           r.returncode == 0 and "Fixture Gloss Council" in out and "REPORTED" in out,
           out[-600:])
    record("P06", "the url match and the HTML entity both work (the row tagged by url "
           "only, with an accented surname written as &eacute;)",
           r.returncode == 0 and f"✗ {RA1}" not in out, out[-600:])

    # ── B: a person who is not in the bytes ────────────────────────────────────
    SB = "session_2099-01-01-author-presence-b"
    RB = admit(SB, "Threshold heights and walking frames", ["Okonkwo|A.", "Fabricatedson|Q."])
    artefact(SB, "<h1>Threshold heights and walking frames</h1><p>A. Okonkwo</p>",
             "https://example.org/thresholds", ref_id=RB)
    r = verify(SB)
    record("P07", "an absent person-author -> exit 1, the source and the surname named",
           r.returncode == 1 and f"✗ {RB}" in r.stdout and "Fabricatedson" in r.stdout
           and "PRESENT-IN-BYTES: 0 of 1" in r.stdout, f"rc={r.returncode} {r.stdout[-600:]!r}")

    # ── C: a short surname only inside a longer word ───────────────────────────
    SC = "session_2099-01-01-author-presence-c"
    RC = admit(SC, "Reliable ramp surfaces", ["Li|W."])
    artefact(SC, "<h1>Reliable ramp surfaces</h1><p>A reliable, slip-resistant finish.</p>",
             "https://example.org/surfaces", ref_id=RC)
    r = verify(SC)
    record("P08", "'Li' inside 'reliable' is NOT present (whole words for a Latin name)",
           r.returncode == 1 and f"✗ {RC}" in r.stdout and "'Li'" in r.stdout,
           f"rc={r.returncode} {r.stdout[-600:]!r}")

    # ── D: the title is not in the bytes ───────────────────────────────────────
    SD = "session_2099-01-01-author-presence-d"
    RD = admit(SD, "An invented title: with a subtitle", ["Okonkwo|A."])
    artefact(SD, "<h1>Something else entirely</h1><p>A. Okonkwo</p>",
             "https://example.org/other", ref_id=RD)
    r = verify(SD)
    record("P09", "an absent title -> exit 1, its first segment named",
           r.returncode == 1 and f"✗ {RD}" in r.stdout and "'An invented title'" in r.stdout,
           f"rc={r.returncode} {r.stdout[-600:]!r}")
    SD2 = "session_2099-01-01-author-presence-d2"
    RD2 = admit(SD2, "FAQ: Ramps that were never published", ["Okonkwo|A."])
    artefact(SD2, "<h1>FAQ</h1><p>A. Okonkwo answers questions about lifts.</p>",
             "https://example.org/faq", ref_id=RD2)
    r = verify(SD2)
    record("P10", "a one-word first segment ('FAQ') is not evidence: the whole title is "
           "asserted, and it is absent", r.returncode == 1 and f"✗ {RD2}" in r.stdout,
           f"rc={r.returncode} {r.stdout[-600:]!r}")

    # ── E: only a failed retrieval ─────────────────────────────────────────────
    SE = "session_2099-01-01-author-presence-e"
    RE_ = admit(SE, "Blocked page", ["Okonkwo|A."])
    artefact(SE, "<html><title>Just a moment...</title></html>",
             "https://example.org/blocked", ref_id=RE_, status=403)
    r = verify(SE)
    record("P11", "a 403 interstitial is not read as the source: UNEXAMINABLE, EXAMINED 0, "
           "exit 1 (INDETERMINATE, not a pass)",
           r.returncode == 1 and examined(r.stdout) == "EXAMINED: 0"
           and "failed retrieval: HTTP 403" in r.stdout and "INDETERMINATE" in r.stdout,
           f"rc={r.returncode} {r.stdout[-600:]!r}")

    # ── J: the JSON path, unchanged ────────────────────────────────────────────
    for sid, tid, family, want_rc in (("f", "P12", "Okonkwo", 0),
                                      ("g", "P13", "Someoneelse", 1)):
        SJ = f"session_2099-01-01-author-presence-{sid}"
        doi = f"10.99999/fixture-author-presence-{sid}"
        title = f"Crossref-shaped fixture {sid}"
        admit(SJ, title, ["Okonkwo|Adaeze"], "--doi", doi)
        artefact(SJ, json.dumps({"message": {
            "DOI": doi, "title": [title], "issued": {"date-parts": [[2020]]},
            "author": [{"family": family, "given": "Adaeze"}]}}),
            f"https://api.crossref.org/works/{doi}", content_type="application/json")
        r = verify(SJ)
        record(tid, f"JSON path unchanged: a payload whose author is {family!r} -> exit "
               f"{want_rc}, and presence mode does not run",
               r.returncode == want_rc and "PRESENCE MODE" not in r.stdout
               and (("CLEAN FOR" in r.stdout) == (want_rc == 0)),
               f"rc={r.returncode} {r.stdout[-500:]!r}")
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 70)
print(f"EXAMINED: {len(results)} assertion(s)")
print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
if sum(results) < len(results):
    print(f"FAILED: {len(results) - sum(results)}")
print("=" * 70)
sys.exit(0 if results and all(results) else 1)
