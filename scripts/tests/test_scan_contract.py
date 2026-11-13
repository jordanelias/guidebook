#!/usr/bin/env python3
"""Tooling T1: the scan contract and the vocabulary lifecycle, every refusal and every
new check proven to fire, and every legitimate shape proven to pass.

WHY THIS EXISTS, as CLAUDE.md section 8 requires. The owner approved tooling T1 on
2026-10-09 ("D8 approve tooling") so that "we can scrape information across any parameter
if it appears in any source no matter the slug" and "add and expand parameter catalogue as
required" (catalogue-plan-v2, scratchpad/session_2026-10-09-research-batch-24-parameter-
pilot/). What reaches the guidebook without these cases, by section:

  O  an observation that folds a second sense of a phrase into the first, or whose quote
     is not in the source it is attributed to -- vocabulary minted from words the source
     never used (critique F3, F7);
  S  a reading recorded as `full` over four pages of seventy-nine, or against bytes the
     source does not hold, or with a typed catalogue version -- so the catalogue implies
     "no code sets a requirement" where nobody read the code (F13);
  H  a full text that is not the whole document, or is not registered under the source;
  L  a parameter that cannot be retired, merged, renamed or un-declined, so every early
     mistake in a growing catalogue is permanent (F5) -- and, when it can, a merge that
     leaves rows pointing at the folded number;
  M  a name minted from an old item, or without the owner's recorded approval (D3);
  U  a cross-slug figure with no follow-up tag, or a live value resting on one silently (D1);
  E  a skimmed figure setting a published value (D1: "skimmed values are not publishable");
  A  the advisory backstops (observation quotes, scan debt, follow-ups, catalogue origins)
     unable to go red;
  G  an admission never read against the catalogue, or with no search behind it, passing
     the batch gate (R16-scan, R17);
  C  rows these writers produce that the capture path cannot ship.

Runs on a COPY of the canonical database in a temp directory, with GUIDEBOOK_RETRIEVAL_LOG
pointed at a temp log holding fixture artefacts, so nothing touches retrieval-log/ or
data/. Fixtures are made through the writers. States no writer can make (a live
determination, a pre-rule admission) are set by SQL on the copy, each saying why. Every
case is recorded rather than raised, so on code without T1 the run reports each missing
verb as a red case and still exits 1 with its summary.
"""
import importlib
import json
import os
import pathlib
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
TMP = tempfile.mkdtemp(prefix="scan-contract-")
DB = os.path.join(TMP, "guidebook.db")
LOG = os.path.join(TMP, "retrieval-log")
shutil.copy(REPO / "data" / "guidebook.db", DB)
os.makedirs(LOG)
os.environ["GUIDEBOOK_DB_PATH"] = DB              # before db/dbcore resolve a path
os.environ["GUIDEBOOK_RETRIEVAL_LOG"] = LOG       # before retrieval_log reads LOG_ROOT
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "scripts" / "research"))
import db                    # noqa: E402
import dbcore                # noqa: E402
import retrieval_log         # noqa: E402
from dbcore import Refusal   # noqa: E402

S = "session_test-scan-contract"
FIX = "session_fixture-scan-contract"
ENV = dict(os.environ)
results = []


def record(tid, name, passed, details=""):
    results.append(bool(passed))
    print(f"  [{'✓' if passed else '✗'}] {tid}: {name}")
    if details and not passed:
        print(f"      {str(details)[:600]}")


def fn(name):
    """The db.py function, or a stub that raises -- so a missing verb is a red case."""
    f = getattr(db, name, None)
    if f is None:
        def missing(*a, **k):
            raise AttributeError(f"db.{name} does not exist")
        return missing
    return f


def refusal(f, *a, **k):
    """The Refusal's text if `f` refuses, else None (any other exception is a defect)."""
    try:
        f(*a, **k)
    except Refusal as exc:
        return str(exc)
    except Exception as exc:  # noqa: BLE001 -- reported, never counted as a refusal
        print(f"      DEFECT, not a refusal: {exc.__class__.__name__}: {exc}")
    return None


def expect_refusal(tid, name, needles, f, *a, **k):
    """record(): `f(*a, **k)` refuses, and the Refusal's text holds every needle."""
    msg = refusal(f, *a, **k)
    record(tid, name, msg and all(n in msg for n in
                                  ((needles,) if isinstance(needles, str) else needles)),
           msg)


def attempt(f, *a, **k):
    try:
        return f(*a, **k)
    except Exception as exc:  # noqa: BLE001 -- recorded red by the caller
        return {"error": f"{exc.__class__.__name__}: {exc}"}


def _absent_schema(exc):
    """A table or column T1 adds, missing because this is code (and a database) without
    T1. Reported and survived, so every later case still runs and goes red on its own --
    one missing table must not hide forty refusals."""
    return isinstance(exc, sqlite3.OperationalError) and (
        "no such table" in str(exc) or "no such column" in str(exc)
        or "has no column" in str(exc))


def q(sql, *params):
    con = sqlite3.connect(DB)
    try:
        return con.execute(sql, params).fetchall()
    except sqlite3.OperationalError as exc:
        if not _absent_schema(exc):
            raise
        print(f"      schema absent: {exc}")
        return []
    finally:
        con.close()


def x(sql, *params):
    """A fixture write by SQL on the COPY, for a state no writer can make. Each call site
    says why."""
    con = sqlite3.connect(DB)
    try:
        cur = con.execute(sql, params)
        con.commit()
        return cur.lastrowid
    except sqlite3.OperationalError as exc:
        if not _absent_schema(exc):
            raise
        print(f"      schema absent: {exc}")
        return None
    finally:
        con.close()


def xfig(sql, *params):
    """`x` for a raw figure (an INSERT into source_value_extractions) and its lens. The figure is written
    without lens columns, which the table's CHECK holds NULL since migration 131 (OR-1c); one `carried`
    link follows, as a fixture standing for a pre-existing figure. Returns the extraction_id."""
    eid = x(sql, *params)
    if eid is not None:
        x("INSERT INTO extraction_lens_links (extraction_id, identity_code, basis, created_at, "
          "created_by_session, updated_at, updated_by_session) VALUES (?, ?, 'carried', 't', ?, 't', ?)",
          eid, POP, S, S)
    return eid


def run(*argv, script="db.py"):
    return subprocess.run([sys.executable, str(REPO / "scripts" / script), *argv],
                          env=ENV, capture_output=True, text=True)


def run_audit(name, *argv):
    return subprocess.run([sys.executable, str(REPO / "scripts" / "audit" / name), *argv],
                          env=ENV, capture_output=True, text=True)


def make_pdf(pages):
    """A minimal valid PDF, one Helvetica text line per page -- no PDF library needed,
    so the case that reads it runs wherever the checks run."""
    def esc(t):
        return t.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    objs = {1: "<< /Type /Catalog /Pages 2 0 R >>",
            3: "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"}
    kids, nid = [], 4
    for text in pages:
        stream = f"BT /F1 12 Tf 72 720 Td ({esc(text)}) Tj ET"
        objs[nid + 1] = f"<< /Length {len(stream)} >>\nstream\n{stream}\nendstream"
        objs[nid] = (f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents "
                     f"{nid + 1} 0 R /Resources << /Font << /F1 3 0 R >> >> >>")
        kids.append(f"{nid} 0 R")
        nid += 2
    objs[2] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(pages)} >>"
    out, offs = b"%PDF-1.4\n", {}
    for i in sorted(objs):
        offs[i] = len(out)
        out += f"{i} 0 obj\n{objs[i]}\nendobj\n".encode("latin-1")
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for i in sorted(objs):
        out += f"{offs[i]:010d} 00000 n \n".encode()
    out += (f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n"
            f"%%EOF\n").encode()
    return out


def put(name, body, ref_id, derived_from=None):
    """Persist a fixture artefact in the temp log with a manifest line, the shape fetch()
    and record_file() write. Returns its sha256."""
    import hashlib
    d = pathlib.Path(LOG) / FIX
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_bytes(body)
    sha = hashlib.sha256(body).hexdigest()
    if derived_from:
        retrieval_log.record_file(d / name, FIX, derived_from, purpose="fixture text",
                                  ref_id=ref_id, kind="text-extraction")
    else:
        with open(d / "manifest.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"retrieved_at": "2026-10-09T00:00:00+00:00",
                                 "url": f"https://fixture.invalid/{name}",
                                 "purpose": "fixture", "ref_id": ref_id, "sha256": sha,
                                 "bytes": len(body), "exit": 0, "status": 200,
                                 "artefact": name, "content_type": None}) + "\n")
    return sha


try:
    # ── fixtures, derived from the copy, never hard-coded ───────────────────────────
    (REF_A, SLUG_A), = q("SELECT e.ref_id, l.slug FROM evidence_sources e JOIN "
                         "source_slug_links l USING (ref_id) WHERE e.superseded_by_ref_id "
                         "IS NULL AND e.tier BETWEEN 1 AND 3 ORDER BY e.ref_id LIMIT 1")
    (REF_B,), (REF_C,) = q("SELECT ref_id FROM evidence_sources WHERE superseded_by_ref_id "
                           "IS NULL AND ref_id <> ? ORDER BY ref_id DESC LIMIT 2", REF_A)
    TOMB = q("SELECT ref_id FROM evidence_sources WHERE superseded_by_ref_id IS NOT NULL "
             "ORDER BY ref_id LIMIT 1")
    TOMB = TOMB[0][0] if TOMB else None
    (POP,), = q("SELECT identity_code FROM base_taxonomy_identity WHERE identity_code <> 'ALL' "
                "ORDER BY identity_code LIMIT 1")
    FREE = [t for (t,) in q(
        "SELECT term_id FROM terms t WHERE NOT EXISTS (SELECT 1 FROM base_parameters p "
        "WHERE p.term_id = t.term_id) AND NOT EXISTS (SELECT 1 FROM parameter_declinations "
        "d WHERE d.term_id = t.term_id) ORDER BY term_id")
        if not db._VALUE_BEARING.search(q("SELECT canonical_en FROM terms WHERE term_id=?",
                                          t)[0][0])]
    PAGES = ["Fixture page one: the clear width of a door leaf is measured here.",
             "Fixture page two: the clear width of a corridor route is measured here.",
             "Fixture page three: the turnwise clearance zone of a wheelchair."]
    PDF_SHA = put("fixture3pages.pdf", make_pdf(PAGES), REF_A)
    PART_SHA = put("fixture3pages-text.txt",
                   ("\n".join(f"[PDF page {i} of 3]\n{t}\n" for i, t in
                              enumerate(PAGES[:2], start=1))).encode(), REF_A,
                   derived_from="fixture3pages.pdf")
    OTHER_SHA = put("fixture-other.html",
                    b"<html><body><p>A shared sentence held only by another source.</p>"
                    b"</body></html>", REF_C)
    HTML_SHA = put("fixture-b.html",
                   b"<html><head><script>var hidden = 1;</script></head><body><p>The "
                   b"landing length of a ramp, read whole.</p></body></html>", REF_B)

    # ── O: observe-term, one sighting, verbatim against the source's own text ─────────
    observe = fn("observe_term")

    def obs(phrase, locator, quote, ref=REF_A, **extra):
        d = {"ref_id": ref, "surface_form": phrase, "language": "EN", "locator": locator,
             "context_quote": quote}
        d.update(extra)
        return d

    n_obs = q("SELECT COUNT(*) FROM observed_terms")[0][0]
    o1 = attempt(observe, obs("clear width", "PDF page 1",
                              "the clear width of a door leaf is measured here"), S)
    o2 = attempt(observe, obs("clear width", "PDF page 2",
                              "the clear width of a corridor route is measured here"), S)
    record("O01", "one phrase at two places is TWO observations (F3: the second sense is "
           "not folded into the first)",
           o1.get("created") is True and o2.get("created") is True
           and o1.get("observation_id") != o2.get("observation_id"), f"{o1} {o2}")
    o3 = attempt(observe, obs("clear width", "PDF page 1",
                              "the clear width of a door leaf is measured here"), S)
    record("O02", "the same sighting again returns the earlier row, created False",
           o3.get("created") is False and o3.get("observation_id") == o1.get("observation_id"),
           f"{o3}")
    expect_refusal("O03", "a new observation with no --locator is refused",
                   "--locator",
                   observe, obs("door leaf", None, "the clear width of a door leaf"), S)
    expect_refusal("O04", "a new observation with no --context-quote is refused",
                   "--context-quote", observe, obs("door leaf", "PDF page 1", None), S)
    expect_refusal("O05", "a phrase not inside its own quote is refused",
                   "does not occur inside", observe, obs("handrail", "PDF page 1",
                                      "the clear width of a door leaf is measured here"), S)
    expect_refusal("O06", "a quote found only in ANOTHER source's file is refused (UNSCOPED is not "
                   "a pass) and names both remedies",
                   ("UNSCOPED", "full_text.py", "--verbatim-exempt"),
                   observe, obs("shared sentence", "p1",
                                      "A shared sentence held only by another source."), S)
    expect_refusal("O07", "a quote in no saved file is refused",
                   "does not occur in any",
                   observe, obs("door leaf", "p9", "the door leaf typed from memory"), S)
    # REF_A holds a derived text (above), so the exemption is refused for it (R2-6, the
    # shared _refuse_exempt_with_body); the route is for a source that holds no decodable
    # body, which REF_B is (an HTML file with no declared text type is not one).
    o8 = attempt(observe, obs("door leaf", "p9", "the door leaf typed from memory", ref=REF_B,
                              verbatim_exempt="fixture: read from a page image"), S)
    note8 = q("SELECT notes FROM observed_terms WHERE observation_id=?",
              o8.get("observation_id", -1))
    record("O08", "the recorded exemption route lands, ledgered on the row's notes",
           o8.get("created") is True and note8
           and "[VERBATIM-EXEMPT: fixture: read from a page image]" in (note8[0][0] or ""),
           f"{o8} {note8}")
    expect_refusal("O09", "an exemption is refused when the quote DOES verify for this source",
                   "Drop the exemption", observe, obs("door leaf", "PDF page 1 again",
                                      "the clear width of a door leaf is measured here",
                                      verbatim_exempt="not needed"), S)
    try:
        x("INSERT INTO observed_terms (ref_id, surface_form, language, locator, "
          "context_quote, created_at, created_by_session) VALUES (?, 'clear width', 'EN', "
          "'PDF page 1', 'dup', 't', ?)", REF_A, S)
        dup_refused = False
    except sqlite3.IntegrityError:
        dup_refused = True
    record("O10", "the schema itself refuses a duplicate SIGHTING (migration 102's unique "
           "key), by SQL that bypasses the writer", dup_refused)
    record("O11", "every refused observation wrote nothing (O03-O07, O09)",
           q("SELECT COUNT(*) FROM observed_terms")[0][0] == n_obs + 3)

    # ── terms and parameters for the later sections, minted through the writers ──────
    P = {}
    for key, tid in zip(("A", "B", "C", "D", "E", "R"), FREE):
        out = attempt(db.insert_parameter, tid, S)
        P[key] = out.get("parameter_id")
    TERM_R = FREE[5]

    # ── S: record-scan and the ledger ────────────────────────────────────────────────
    scan = fn("record_scan")

    def sc(**k):
        d = {"ref_id": REF_A, "mode": "catalogue", "text_scope": "partial",
             "file_sha256": PART_SHA, "method": "full-read"}
        d.update(k)
        return d

    n_scan = q("SELECT COUNT(*) FROM source_scans")[0][0] if q(
        "SELECT 1 FROM sqlite_master WHERE name='source_scans'") else None
    expect_refusal("S01", "a typed catalogue version is refused (it is computed)",
                   "COMPUTED", scan, sc(catalogue_version=3), S)
    msg = refusal(scan, sc(ref_id=TOMB), S) if TOMB else "no tombstone in the copy"
    record("S02", "a superseded source (a tombstone) is refused",
           msg and ("superseded" in msg or "tombstone" in msg), msg)
    expect_refusal("S03", "a file saved for ANOTHER source is refused, listing what this one holds",
                   ("no file saved for", "fixture3pages"), scan, sc(file_sha256=OTHER_SHA), S)
    expect_refusal("S04", "'full' over a PDF is refused and names full_text.py",
                   "full_text.py", scan, sc(text_scope="full", file_sha256=PDF_SHA), S)
    expect_refusal("S05", "'full' over a text carrying 2 of 3 pages is refused (Q5)",
                   "2 of 3", scan, sc(text_scope="full"), S)
    s6 = attempt(scan, sc(), S)
    top = q("SELECT MAX(parameter_id) FROM base_parameters")[0][0]
    record("S06", "a partial reading lands with pages and catalogue version COMPUTED",
           s6.get("pages_read") == 2 and s6.get("pages_total") == 3
           and s6.get("catalogue_version") == top, f"{s6} top={top}")
    expect_refusal("S07", "a targeted reading with no target is refused",
                   "--target-parameter-id", scan, sc(mode="targeted"), S)
    expect_refusal("S08", "a catalogue reading with a target is refused",
                   "targeted", scan, sc(mode="catalogue", target_parameter_id=P["A"]), S)

    def ledger(ref, pid):
        r = q("SELECT status, text_scope FROM v_scan_ledger WHERE ref_id=? AND "
              "parameter_id=?", ref, pid) if q(
            "SELECT 1 FROM sqlite_master WHERE name='v_scan_ledger'") else []
        return r[0] if r else None

    record("S09", "after only a partial reading the ledger says READ-PARTIAL",
           ledger(REF_A, P["A"]) == ("READ-PARTIAL", "partial"), ledger(REF_A, P["A"]))

    # H: the full-text helper derives every page, under the ref_id.
    h1 = run("--ref-id", REF_A, "--session", S, script="research/full_text.py")
    full = [r for r in retrieval_log._manifest_records(S)
            if r.get("ref_id") == REF_A and r.get("artefact", "").endswith("-full-text.txt")]
    try:
        import pymupdf  # noqa: F401
        have_mupdf = True
    except ImportError:
        have_mupdf = False
    if have_mupdf:
        record("H01", "full_text.py derives ALL pages with markers and registers the text "
               "under the source's ref_id",
               h1.returncode == 0 and "pages read:  3 of 3" in h1.stdout and len(full) == 1,
               h1.stdout + h1.stderr)
        FULL_SHA = full[0]["sha256"] if full else None
        h2 = run("--ref-id", REF_A, "--session", S, script="research/full_text.py")
        record("H02", "a second run registers nothing new (ALREADY REGISTERED)",
               h2.returncode == 0 and "ALREADY REGISTERED" in h2.stdout
               and len([r for r in retrieval_log._manifest_records(S)
                        if r.get("artefact", "").endswith("-full-text.txt")]) == 1,
               h2.stdout + h2.stderr)
    else:
        # NOT RUN, and said so: CI's battery may lack the PDF reader. The full text is
        # then written by hand in the helper's format so the S cases below still run.
        print("      H01/H02 NOT RUN: pymupdf is absent here (the research battery declares "
              "it); the full text is written by hand in the helper's marker format")
        FULL_SHA = put("fixture3pages-full-text.txt",
                       ("\n".join(f"[PDF page {i} of 3]\n{t}\n" for i, t in
                                  enumerate(PAGES, start=1))).encode(), REF_A,
                       derived_from="fixture3pages.pdf")
    if TOMB:
        h3 = run("--ref-id", TOMB, "--session", S, script="research/full_text.py")
        record("H03", "full_text.py refuses a tombstone", h3.returncode == 2
               and "superseded" in h3.stderr, h3.stdout + h3.stderr)
    h4 = run("--ref-id", REF_C, "--session", S, "--dry-run", script="research/full_text.py")
    record("H04", "full_text.py derives a web page whole (script text dropped) under "
           "--dry-run, writing nothing",
           h4.returncode == 0 and "not paged" in h4.stdout and "DRY RUN" in h4.stdout,
           h4.stdout + h4.stderr)
    s10 = attempt(scan, sc(text_scope="full", file_sha256=FULL_SHA, open_pass_done=True), S)
    record("S10", "'full' over the whole derived text lands, 3 of 3",
           s10.get("pages_read") == 3 and s10.get("pages_total") == 3, s10)
    record("S11", "after a full catalogue reading with no row, the ledger says "
           "READ-NOTHING-FOUND for every parameter up to the catalogue version",
           ledger(REF_A, P["A"]) == ("READ-NOTHING-FOUND", "full")
           and ledger(REF_A, P["B"]) == ("READ-NOTHING-FOUND", "full"),
           (ledger(REF_A, P["A"]), ledger(REF_A, P["B"])))
    # Q4: a parameter promoted AFTER the reading is NOT-READ for that source.
    late = attempt(db.insert_parameter, FREE[6], S).get("parameter_id")
    record("S12", "a parameter promoted after the reading is NOT-READ for that source "
           "(back-fill debt is visible, Q4)",
           ledger(REF_A, late) == ("NOT-READ", None), ledger(REF_A, late))
    d1 = run_audit("scan_debt.py")
    s13 = attempt(scan, sc(mode="targeted", target_parameter_id=late, text_scope="full",
                           file_sha256=FULL_SHA), S)
    record("S13", "a targeted reading for the new parameter covers it",
           ledger(REF_A, late) == ("READ-NOTHING-FOUND", "full"), (s13, ledger(REF_A, late)))
    record("S14", "scan_debt is red while pairs are NOT-READ, and lists the parameter",
           d1.returncode == 1 and f"parameter {late} " in d1.stdout and "EXAMINED:" in d1.stdout,
           d1.stdout[-600:] + d1.stderr)
    xfig("INSERT INTO source_value_extractions (ref_id, slug, parameter_id, "
         "claim_type, claim_text, extraction_method, created_at, updated_at, figure_role) "
         "VALUES (?, ?, ?, 'absent', 'fixture', 'full-read', 't', 't', 'finding')",
         REF_B, SLUG_A, late)    # an `absent` row, the positive statement of absence
    record("S15", "an 'absent' extraction reads STATED-ABSENT, beating any reading",
           ledger(REF_B, late) == ("STATED-ABSENT", None), ledger(REF_B, late))
    record("S16", "every refused reading wrote nothing (S01-S05, S07, S08)",
           n_scan is not None and q("SELECT COUNT(*) FROM source_scans")[0][0]
           == n_scan + 3, n_scan)

    # ── L: the lifecycle verbs ──────────────────────────────────────────────────────
    retire, merge = fn("retire_parameter"), fn("merge_parameter")
    expect_refusal("L01", "retire-parameter refuses a blank reason",
                   "--reason", retire, P["A"], "  ", S)
    gate_pid = q("SELECT parameter_id FROM determination_gates WHERE resolved_at IS NULL "
                 "LIMIT 1")
    if gate_pid:
        expect_refusal("L02", "retire-parameter refuses a parameter with an OPEN gate, naming the "
                       "resolve verb",
                       "resolve-determination-gate", retire, gate_pid[0][0], "fixture", S)
    # A LIVE determination: assess_cell writes them only on a scratch run with every
    # anchoring gate satisfied, which a fixture cannot honestly supply, so it is set here.
    SPEC = x("INSERT INTO specifications (parameter_id, identity_code, state, created_at, "
             "created_by_session) VALUES (?, ?, 'pending', 't', ?)", P["E"], POP, S)
    expect_refusal("L03", "retire-parameter refuses a parameter with a LIVE determination, naming "
                   "retire-specification",
                   "retire-specification", retire, P["E"], "fixture", S)
    # An extraction with a measured root on P[R], so v_value_independence lists it.
    xfig("INSERT INTO source_value_extractions (ref_id, slug, parameter_id, "
         "claim_type, claimed_value, claim_text, extraction_method, created_at, updated_at, "
         "figure_role, root_type, root_ref_id) VALUES (?, ?, ?, 'numerical', '1', "
         "'fixture 1', 'full-read', 't', 't', 'claim', 'measurement_primary', ?)",
         REF_A, SLUG_A, P["R"], REF_A)   # fixture evidence for the reader sweep (Q9)
    listed_before = bool(q("SELECT 1 FROM v_value_independence WHERE parameter_id=?", P["R"]))
    r4 = attempt(retire, P["R"], "fixture: not a design quantity after all", S)
    row = q("SELECT status, notes FROM base_parameters WHERE parameter_id=?", P["R"])[0]
    record("L04", "retire-parameter retires IN PLACE: status retired, reason appended, "
           "extractions kept", r4.get("status") == "retired" and row[0] == "retired"
           and "RETIRED" in (row[1] or "") and "not a design quantity" in (row[1] or "")
           and r4.get("extractions_kept_as_history") == 1, f"{r4} {row}")
    record("L05", "readers filter the retired parameter: v_scan_ledger and "
           "v_value_independence no longer list it (Q9)",
           listed_before and not q("SELECT 1 FROM v_value_independence WHERE parameter_id=?",
                                   P["R"])
           and not q("SELECT 1 FROM v_scan_ledger WHERE parameter_id=?", P["R"]),
           f"listed_before={listed_before}")
    expect_refusal("L06", "retire-parameter refuses a parameter that is not active",
                   "already retired", retire, P["R"], "again", S)
    expect_refusal("L07", "a retired parameter takes no new extraction (the existing writer's "
                   "refusal, now reachable)",
                   "retired", fn("insert_extraction"),
                         {"ref_id": REF_A, "parameter_id": P["R"],
                          "identity_code": POP, "claim_type": "absent", "figure_role": "finding",
                          "lens_basis": "named_in_text", "lens_basis_text": "fixture",
                          "claim_text": "fixture", "extraction_method": "full-read"}, S,
                         relations=[], verbatim_exempt="fixture")

    # merge: P[C] is folded into P[A] first, then P[A] into P[B] -- the chain flattens.
    expect_refusal("L08", "merge-parameter refuses the same parameter twice",
                   "same parameter", merge, P["A"], P["A"], "x", S)
    expect_refusal("L09", "merge-parameter refuses a parameter that is not active",
                   "not active", merge, P["R"], P["A"], "x", S)
    expect_refusal("L10", "merge-parameter refuses while either side has a live determination",
                   "LIVE determination", merge, P["E"], P["A"], "x", S)
    attempt(merge, P["C"], P["A"], "fixture: one quantity", S)
    XA = xfig("INSERT INTO source_value_extractions (ref_id, slug, parameter_id, "
              "claim_type, claim_text, extraction_method, created_at, "
              "updated_at, figure_role) VALUES (?, ?, ?, 'absent', 'fixture', 'full-read', "
              "'t', 't', 'finding')", REF_A, SLUG_A, P["A"])   # a row to re-point
    TS = attempt(scan, sc(mode="targeted", target_parameter_id=P["A"]), S).get("scan_id")
    # History on P[A]: a RETIRED determination and a RESOLVED gate, neither writable here
    # without the engine and an audit, set by SQL so the merge can be seen to keep them.
    OLD = x("INSERT INTO specifications (parameter_id, identity_code, state, created_at, "
            "created_by_session, retired_at, retired_by_session, retirement_reason) "
            "VALUES (?, ?, 'pending', 't', ?, 't', ?, 'fixture history')",
            P["A"], POP, S, S)
    m = attempt(merge, P["A"], P["B"], "fixture: two names for one quantity", S)
    rowA = q("SELECT status, merged_into FROM base_parameters WHERE parameter_id=?", P["A"])[0]
    record("L11", "merge-parameter marks the folded row merged into the survivor",
           rowA == ("merged", P["B"]), f"{m} {rowA}")
    xrow = q("SELECT parameter_id, notes FROM source_value_extractions WHERE "
             "extraction_id=?", XA)[0]
    srow = q("SELECT target_parameter_id, notes FROM source_scans WHERE scan_id=?", TS)
    record("L12", "every row holding the folded id is RE-POINTED with a dated MERGED note: "
           "extractions and targeted readings",
           xrow[0] == P["B"] and "MERGED" in (xrow[1] or "") and srow
           and srow[0][0] == P["B"] and "MERGED" in (srow[0][1] or ""), f"{xrow} {srow}")
    record("L13", "a chain flattens: the parameter merged into the folded one now points "
           "at the survivor",
           q("SELECT merged_into FROM base_parameters WHERE parameter_id=?", P["C"])[0][0]
           == P["B"])
    record("L14", "history stays: the retired determination keeps the folded id, and the "
           "merge says so", q("SELECT parameter_id FROM specifications WHERE "
                              "specification_id=?", OLD)[0][0] == P["A"]
           and m.get("kept_as_history", {}).get("specifications.parameter_id") == 1, m)
    left = [t for (t,) in q("SELECT name FROM sqlite_master WHERE type='table'")
            for f in q(f'PRAGMA foreign_key_list("{t}")')
            if f[2] == "base_parameters" and t not in ("specifications",
                                                       "determination_gates")
            and q(f'SELECT 1 FROM "{t}" WHERE "{f[3]}" = ?', P["A"])]
    record("L15", "outside the two history tables, NO row holds the folded id (derived "
           "from the live FK graph)", not left, left)

    # rename-term
    rename = fn("rename_term")
    TR = FREE[7]
    adj = fn("adjudicate_term")
    # Page three is in the FULL text registered above (H01, or its by-hand stand-in),
    # so this quote verifies scoped and needs no exemption.
    o_tz = attempt(observe, obs("turnwise clearance zone", "PDF page 3",
                                "the turnwise clearance zone of a wheelchair"), S)
    OTZ = o_tz.get("observation_id")
    expect_refusal("N01", "rename-term refuses a rename with no warrant",
                   "exactly one warrant", rename, TR, "turnwise clearance zone", "fixture", S)
    expect_refusal("N02", "rename-term refuses two warrants at once",
                   "exactly one warrant", rename, TR, "turnwise clearance zone", "fixture", S,
                         from_observation=OTZ, ruling_quote="x")
    expect_refusal("N03", "rename-term refuses a value-bearing name",
                   "value", rename, TR, "turning circle 1500", "fixture", S, from_observation=OTZ)
    expect_refusal("N04", "rename-term refuses an observation no adjudication names this term "
                   "with",
                   "adjudicat",
                   rename, TR, "turnwise clearance zone", "fixture", S, from_observation=OTZ)
    attempt(adj, OTZ, "NAMES-EXISTING", "fixture: the phrase names this concept", S,
            term_id=TR)
    expect_refusal("N05", "rename-term refuses a name the observed phrase does not contain",
                   "not in the observed phrase",
                   rename, TR, "turnwise zone", "fixture", S, from_observation=OTZ)
    other_name = q("SELECT canonical_en FROM terms WHERE term_id=?", FREE[8])[0][0]
    expect_refusal("N06", "rename-term refuses a name another term holds",
                   "already the name of",
                   rename, TR, other_name, "fixture", S, from_observation=OTZ)
    old_name = q("SELECT canonical_en FROM terms WHERE term_id=?", TR)[0][0]
    n7 = attempt(rename, TR, "turnwise clearance zone", "fixture: the sources' own phrase",
                 S, from_observation=OTZ)
    alias = q("SELECT alias_type, language, notes FROM term_aliases WHERE term_id=? AND "
              "alias=?", TR, old_name)
    trow = q("SELECT canonical_en, scope_note FROM terms WHERE term_id=?", TR)[0]
    record("N07", "rename-term renames from the observation; the old name is a DEPRECATED "
           "alias in term_aliases' own letter case, marked 'curated'; scope_note records it",
           trow[0] == "turnwise clearance zone" and alias
           and alias[0][0] == "DEPRECATED" and alias[0][1] == "en"
           and "curated" in alias[0][2] and f"canonical_en was '{old_name}'" in (trow[1] or ""),
           f"{n7} {alias} {trow}")
    ap = subprocess.run([sys.executable, str(REPO / "scripts" / "audit" /
                                             "alias_provenance_audit.py")],
                        env=ENV, capture_output=True, text=True)
    record("N08", "alias_provenance_audit passes on the copy after rename and add-alias",
           ap.returncode == 0, ap.stdout[-400:])
    ledger_text = (REPO / "references" / "project-standards.md").read_text(encoding="utf-8")
    body = dbcore.strip_supersedes_citations(ledger_text)
    QUOTE = next((ln for ln in (dbcore.strip_ledger_line_marker(raw)
                                for raw in ledger_text.splitlines())
                  if 60 <= len(ln) <= 200 and '"' not in ln and "`" not in ln
                  and dbcore.count_ledger_quote(body, ln) == 1), None)
    words = [w.lower() for w in (QUOTE or "").split() if w.isalpha() and len(w) > 4]
    RNAME = next((f"{a} {b}" for a, b in zip(words, words[1:])
                  if f"{a} {b}" in (QUOTE or "").lower()
                  and not db._VALUE_BEARING.search(f"{a} {b}")
                  and not q("SELECT 1 FROM terms WHERE lower(canonical_en)=?", f"{a} {b}")
                  and not q("SELECT 1 FROM term_aliases WHERE lower(alias)=?", f"{a} {b}")),
                 None)
    expect_refusal("N09", "rename-term refuses a ruling quote not found exactly once in the ledger",
                   "exactly once", rename, FREE[9], RNAME or "x", "fixture", S,
                         ruling_quote="fixture: words the owner never said")
    n10 = attempt(rename, FREE[9], RNAME, "fixture: the owner's words", S,
                  ruling_quote=QUOTE)
    record("N10", "rename-term renames from an owner ruling quoted once in the ledger",
           QUOTE and RNAME and n10.get("now") == RNAME, f"{n10} quote={QUOTE!r}")

    # revoke-declination
    revoke = fn("revoke_declination")
    TD = FREE[10]
    attempt(db.decline_parameter, TD, "fixture: an element, not a quantity", S)
    DR = sorted(p.relative_to(REPO).as_posix()
                for p in (REPO / "decisions").glob("DR-*.md"))[0]
    expect_refusal("V01", "revoke-declination refuses a term that is not declined",
                   "not declined", revoke, FREE[11], "fixture", DR, S)
    expect_refusal("V02", "revoke-declination refuses a decision reference that does not resolve",
                   "--decision-ref", revoke, TD, "fixture", "a decision somewhere", S)
    v3 = attempt(revoke, TD, "fixture: it is a quantity after all", DR, S)
    p3 = attempt(db.insert_parameter, TD, S)
    record("V03", "a revoked declination is history: the row stays, revoked, and "
           "add-parameter now promotes the term",
           v3.get("revoked") is True and p3.get("parameter_id")
           and q("SELECT revoked_by_session FROM parameter_declinations WHERE term_id=?",
                 TD)[0][0] == S, f"{v3} {p3}")
    expect_refusal("V04", "revoke-declination refuses a second revocation",
                   "already revoked", revoke, TD, "again", DR, S)
    msg = refusal(db.decline_parameter, FREE[12], "fixture", S)  # control: still declines
    TD2 = FREE[12]
    attempt(revoke, TD2, "fixture", DR, S)
    expect_refusal("V05", "decline-parameter refuses to re-decline a revoked term, saying why (one "
                   "row per term)",
                   "REVOKED", db.decline_parameter, TD2, "fixture: again", S)

    # annotate-parameter
    annotate = fn("annotate_parameter")
    expect_refusal("A01", "annotate-parameter refuses a blank note",
                   "--note", annotate, P["B"], "  ", S)
    expect_refusal("A02", "annotate-parameter refuses the separator",
                   "' || '", annotate, P["B"], "a || b", S)
    before = q("SELECT notes FROM base_parameters WHERE parameter_id=?", P["B"])[0][0] or ""
    attempt(annotate, P["B"], "fixture: the earlier note was wrong", S)
    after = q("SELECT notes FROM base_parameters WHERE parameter_id=?", P["B"])[0][0] or ""
    record("A03", "annotate-parameter appends a dated, attributed line and keeps the rest",
           after.startswith(before.rstrip()) and f"ANNOTATED" in after and S in after,
           after[-300:])

    # add-alias
    add_alias = fn("add_alias")
    TA = FREE[13]
    o_cw = attempt(observe, obs("door leaf", "PDF page 1 / door",
                                "the clear width of a door leaf is measured here"), S)
    OCW = o_cw.get("observation_id")
    expect_refusal("AL01", "add-alias refuses DEPRECATED (rename-term's record)",
                   "DEPRECATED", add_alias, TA, OCW, "DEPRECATED", S)
    expect_refusal("AL02", "add-alias refuses an observation no adjudication names the term with",
                   "adjudicat", add_alias, TA, OCW, "SYNONYM", S)
    attempt(adj, OCW, "NAMES-EXISTING", "fixture", S, term_id=TA)
    legacy = q("SELECT o.observation_id FROM observed_terms o WHERE o.created_by_session "
               "<> ? AND COALESCE(o.notes,'') NOT LIKE '%VERBATIM-EXEMPT%' ORDER BY 1 LIMIT 1",
               S)[0][0]
    attempt(adj, legacy, "NAMES-EXISTING", "fixture", S, term_id=TA)
    expect_refusal("AL03", "add-alias refuses an observation whose quote is not in its own source's "
                   "saved text (the fixture log holds none of the corpus)",
                   "source-attested", add_alias, TA, legacy, "SYNONYM", S)
    a4 = attempt(add_alias, TA, OCW, "SYNONYM", S)
    arow = q("SELECT alias, language, jurisdiction, notes FROM term_aliases WHERE term_id=? "
             "AND alias='door leaf'", TA)
    jur = q("SELECT jurisdiction FROM evidence_sources WHERE ref_id=?", REF_A)[0][0]
    record("AL04", "add-alias writes the source's phrase, language in the table's case, the "
           "source's jurisdiction, and the 'source-attested' marker",
           arow and arow[0][1] == "en" and arow[0][2] == jur
           and arow[0][3].startswith("source-attested"), f"{a4} {arow}")
    expect_refusal("AL05", "add-alias refuses an alias the term already holds",
                   "already holds", add_alias, TA, OCW, "SYNONYM", S)

    expect_refusal("AL06", "add-alias refuses TRANSLATION: a source's own phrase is not a rendering "
                   "of the English one (R11)", "TRANSLATION", add_alias, TA, OCW, "TRANSLATION", S)
    # AL07: an alias held WITHOUT a pointer is promoted in place by attesting it; no second row.
    TB = FREE[15]
    x("INSERT INTO term_aliases (term_id, alias, language, alias_type, notes, created_at, "
      "created_by_session, updated_at, updated_by_session, attestation) VALUES (?, 'corridor "
      "route', 'en', 'SYNONYM', 'model-generated', '2026-01-01 00:00', 'fixture', "
      "'2026-01-01 00:00', 'fixture', 'model_seed')", TB)
    o_h = attempt(observe, obs("corridor route", "PDF page 2 / corridor route",
                               "the clear width of a corridor route is measured here"), S)
    attempt(adj, o_h.get("observation_id"), "NAMES-EXISTING", "fixture", S, term_id=TB)
    n_before = q("SELECT count(*) FROM term_aliases WHERE term_id=?", TB)[0][0]
    a7 = attempt(add_alias, TB, o_h.get("observation_id"), "SYNONYM", S)
    row7 = q("SELECT observation_id, alias_type FROM term_aliases WHERE term_id=? AND "
             "alias='corridor route'", TB)
    record("AL07", "add-alias promotes a held alias in place: the pointer is attached and the "
           "attestation becomes other_source; its type and row count are kept",
           a7.get("promoted") is True and row7 == [(o_h["observation_id"],
           "SYNONYM")] and q("SELECT count(*) FROM term_aliases WHERE term_id=?", TB)[0][0]
           == n_before and q("SELECT attestation FROM term_aliases WHERE term_id=? AND "
                             "alias='corridor route'", TB) == [("other_source",)], f"{a7} {row7}")
    expect_refusal("AL08", "and a second attestation of an attested alias is refused",
                   "attested by observation", add_alias, TB, o_h.get("observation_id"),
                   "SYNONYM", S)
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("alias_audit", REPO / "scripts/audit/alias_provenance_audit.py")
    _am = _iu.module_from_spec(_sp); _sp.loader.exec_module(_am)
    record("AL09", "alias_provenance_audit classifies from the pointer, not the notes text",
           _am.classify("source-attested: forged", None) != "SOURCE-ATTESTED"
           and _am.classify("model-generated", 1) == "SOURCE-ATTESTED")
    # T2: a name is a phrase the source used
    ins = fn("insert_term")
    o_n = attempt(observe, obs("turnwise clearance zone", "PDF page 3 / zone",
                               "the turnwise clearance zone of a wheelchair"), S)
    expect_refusal("T201", "add-term refuses a name that is not inside the observed phrase "
                   "(no model-coined gloss, OR-17)", "not inside the observed phrase", ins,
                   o_n.get("observation_id"), "fixture invented gloss", "fixture", S,
                   dry_run=True)
    t202 = attempt(ins, o_n.get("observation_id"), "turnwise clearance", "fixture: a distinct fixture concept", S,
                   dry_run=True, distinct_from=[TR])
    record("T202", "add-term takes a contiguous part of the observed phrase", bool(t202.get("term_id")),
           t202)
    # N10: a name may come from a phrase in another language (owner E1); rename-term no longer
    # demands an English observation
    o_nl = attempt(observe, obs("turnwise clearance zone", "PDF page 3 / nl",
                                "the turnwise clearance zone of a wheelchair", language="NL"), S)
    attempt(adj, o_nl.get("observation_id"), "NAMES-EXISTING", "fixture", S, term_id=FREE[16])
    n10 = attempt(rename, FREE[16], "turnwise clearance", "fixture: native name", S,
                  from_observation=o_nl.get("observation_id"), dry_run=True)
    record("N10b", "rename-term accepts a non-English observation as the warrant for a native name",
           n10.get("changed") is not False and "error" not in n10, n10)
    # ── M: mint-term-from-catalogue ──────────────────────────────────────────────────
    mint = fn("mint_term_from_catalogue")
    APPROVAL = next((h[3:].strip() for h in ledger_text.splitlines()
                     if h.startswith("## ") and re.search(r"\d{4}-\d{2}-\d{2}", h)
                     and dbcore.ledger_heading_count(h[3:]) == 1), None)
    TIER456 = "references/tier456-verified-sources.json"
    ENTRY = json.loads((REPO / TIER456).read_text(encoding="utf-8"))[1]["ref_id"]

    def mt(**k):
        a = dict(catalogue=TIER456, entry_ref=ENTRY, canonical_en="fixture tactile surface "
                 "name", definition="fixture definition of a tactile surface",
                 approval_ref=APPROVAL or "x", session=S)
        a.update(k)
        return a

    expect_refusal("M01", "mint refuses a value-bearing name",
                   "values", mint, **mt(canonical_en="tactile surface 600"))
    expect_refusal("M02", "mint refuses an old item code",
                   "item code", mint, **mt(canonical_en="E-08 corridor"))
    msg = refusal(mint, **mt(catalogue="_archived/data/corpus-pre-reset-2026-08-06.db",
                             entry_ref="items:E-08"))
    record("M03", "mint refuses the old Part 4 item table of the pre-reset corpus",
           msg and ("not selected" in msg or "item code" in msg), msg)
    expect_refusal("M04", "mint refuses an entry that does not resolve in the catalogue file",
                   "no entry", mint, **mt(entry_ref="Tier9_999"))
    expect_refusal("M05", "mint refuses an approval entry not found exactly once in the ledger",
                   "exactly one",
                   mint, **mt(approval_ref="Fixture entry 2026-01-01 the owner never gave"))
    expect_refusal("M05b", "mint refuses an approval ref that carries no date", "no date",
                   mint, **mt(approval_ref="Fixture entry the owner never gave"))
    expect_refusal("M04b", "mint refuses the registry's bracketed template placeholder",
                   "placeholder", mint, **mt(
                       catalogue="references/standards-registry.md",
                       entry_ref="[Standard identifier and year as cited in guidebook]"))
    real_ledger = dbcore.LEDGER_PATH
    fake = pathlib.Path(TMP) / "ledger.md"
    try:
        dbcore.LEDGER_PATH = fake
        fake.write_text(f"## {APPROVAL}\n\n## {APPROVAL}\n", encoding="utf-8")
        expect_refusal("M05c", "mint refuses an approval heading that occurs twice",
                       "exactly one", mint, **mt())
        fake.write_text(f"{APPROVAL}\n", encoding="utf-8")
        expect_refusal("M05d", "mint counts `## ` headings only, not any line that reads the "
                       "same", "exactly one", mint, **mt())
        fake.write_text(f"## {APPROVAL}\n", encoding="utf-8")
        m05e = attempt(mint, **mt(approval_ref=f"## {APPROVAL}", canonical_en="fixture "
                                  "prefix name"), dry_run=True)
        record("M05e", "mint takes the heading with or without its `## ` prefix",
               bool(m05e.get("term_id")), m05e)
    finally:
        dbcore.LEDGER_PATH = real_ledger
    expect_refusal("M06", "mint refuses a catalogue outside the CHECK (adding one is a ruling)",
                   "CHECK", mint, **mt(catalogue="references/not-a-catalogue.md"))
    mt7 = attempt(mint, **mt())
    orow = q("SELECT catalogue, catalogue_entry_ref, catalogue_approval_ref FROM terms "
             "WHERE term_id=?", mt7.get("term_id", ""))
    record("M07", "mint writes the term with its origin (catalogue, entry, approval)",
           mt7.get("term_id") and orow == [(TIER456, ENTRY, APPROVAL)], f"{mt7} {orow}")
    expect_refusal("M08", "mint refuses a name a term already holds",
                   "already", mint, **mt())
    oldterm = q("SELECT term_id FROM terms ORDER BY term_id DESC LIMIT 1")[0][0]
    corpus = "_archived/data/corpus-pre-reset-2026-08-06.db"
    cterm = sqlite3.connect(f"file:{REPO / corpus}?mode=ro&immutable=1", uri=True).execute(
        "SELECT term_id FROM terms ORDER BY term_id LIMIT 1").fetchone()[0]
    mt9 = attempt(mint, **mt(catalogue=corpus, entry_ref=f"terms:{cterm}",
                             canonical_en="fixture corpus term name"))
    record("M09", "mint resolves a pre-reset corpus TERM (the permitted half of that "
           "catalogue)", mt9.get("term_id") and mt9.get("term_id") > oldterm, mt9)
    # M13-M15: the item subjects, by row number, with the guard unchanged
    ITEMS = REPO / "_archived/data/corpus-pre-reset-2026-08-06.db"
    free_item = {"entry_ref": "items:3", "subject": db._item_subject(ITEMS, 3)}
    record("M13", "an item subject resolves by row number, stripped of its aside and showing no old code",
           bool(free_item["subject"]) and not db._ITEM_CODE.search(free_item["subject"]), free_item)
    m14 = attempt(mint, **mt(catalogue=corpus, entry_ref=free_item["entry_ref"],
                             canonical_en="Acoustic Door"), dry_run=True)
    record("M14", "mint resolves an item subject by row number, its name the subject's own",
           bool(m14.get("term_id")), m14)
    expect_refusal("M15", "mint refuses a name that is not inside the item subject (no rewording)",
                   "not inside the item subject", mint, **mt(
                       catalogue=corpus, entry_ref=free_item["entry_ref"],
                       canonical_en="fixture reworded name"))
    vp = run(script="validate_parameters.py")
    record("M10", "validate_parameters P2 passes with the approval entry in the ledger",
           vp.returncode == 0 and "P2: 2 catalogue-minted" in vp.stdout, vp.stdout[-300:])
    x("UPDATE terms SET catalogue=?, catalogue_entry_ref=?, catalogue_approval_ref="
      "'Fixture entry 2026-01-01 that is in no ledger' WHERE term_id=?", TIER456, ENTRY,
      FREE[14])
    # ^ fault injection: an origin whose approval entry the ledger no longer carries
    vp = run(script="validate_parameters.py")
    record("M11", "validate_parameters P2 FAILS an origin whose approval entry is gone",
           vp.returncode == 1 and "P2 FAIL" in vp.stdout, vp.stdout[-400:])
    x("UPDATE terms SET catalogue=NULL, catalogue_entry_ref=NULL, "
      "catalogue_approval_ref=NULL WHERE term_id=?", FREE[14])  # restore the copy
    # M12: a SET-but-incomplete triple is refused by the table, not admitted as a NULL CHECK.
    # `length(trim(NULL)) > 0` is NULL, which SQLite does not count as a violation, so each
    # set branch must test IS NOT NULL first (migrations 104 and 105).
    con = sqlite3.connect(DB)
    admitted = []
    try:
        for label, sql, args in (
                ("terms", "UPDATE terms SET catalogue=?, catalogue_entry_ref=NULL, "
                 "catalogue_approval_ref='h 2026-01-01' WHERE term_id=?", (TIER456, FREE[14])),
                ("parameter_declinations", "UPDATE parameter_declinations SET revoked_at='t', "
                 "revoked_by_session='s' WHERE term_id=(SELECT term_id FROM "
                 "parameter_declinations WHERE revoked_at IS NULL LIMIT 1)", ()),
                ("extraction_follow_ups", "INSERT INTO extraction_follow_ups (extraction_id, "
                 "reason, warrant, raised_at, raised_by_session, resolved_at, "
                 "resolved_by_session) SELECT MIN(extraction_id), "
                 "'read-outside-admitting-purpose', 'w', 't', 's', 't', 's' FROM "
                 "source_value_extractions", ())):
            try:
                con.execute(sql, args)
                admitted.append(label)
            except sqlite3.IntegrityError:
                pass
            con.rollback()
    finally:
        con.close()
    record("M12", "the all-or-none CHECKs refuse a partial triple (NULL is not a pass)",
           not admitted, admitted)

    # ── E: the engine leaves skimmed figures out of what sets a value ────────────────
    sys.path.insert(0, str(REPO / "scripts" / "assess"))
    ac = importlib.import_module("assess_cell")
    PE = P["D"]
    REF_S = REF_B     # a second source, holding ONLY a skimmed claim

    def claim(ref, value, method, quote=None):
        """A claim row. REF_A holds a derived text (section F), so its claims must quote it
        -- the page marker carries the digits -- and the exemption is kept only for REF_S,
        for which no decodable body is indexed."""
        text = quote or f"fixture: shall not exceed {value} mm"
        out = attempt(db.insert_extraction,
                      {"ref_id": ref, "parameter_id": PE,
                       "identity_code": POP, "claim_type": "numerical",
                       "lens_basis": "named_in_text", "lens_basis_text": text.split()[0],
                       "claimed_value": value, "claimed_unit": "mm", "comparator": "<=",
                       "figure_role": "claim", "extraction_method": method,
                       "claim_text": text,
                       "loc_section": f"fixture {method}"},
                      S, relations=[],
                      verbatim_exempt=None if quote else "fixture: no artefact")
        return out.get("extraction_id")

    attempt(db.link_source_slug, REF_S, SLUG_A, "fixture: the engine case", S)
    # Since 2026-11-06 add-extraction refuses a source that is not VERIFIED and a pair no
    # reading covers (R16, OR-11a). The fixture sources are given both states by SQL: the
    # standing, which the copy may not carry for them, and a catalogue reading at the live
    # catalogue version (record-scan would need a manifest artefact for each).
    con = sqlite3.connect(DB)
    try:
        for ref in (REF_A, REF_S):
            con.execute("UPDATE evidence_sources SET verification_status='VERIFIED' WHERE "
                        "ref_id=? AND COALESCE(verification_status,'')<>'VERIFIED'", (ref,))
            con.execute("INSERT INTO source_scans (ref_id, mode, catalogue_version, text_scope, "
                        "file_sha256, method, created_at, created_by_session) SELECT ?, "
                        "'catalogue', MAX(parameter_id), 'partial', ?, 'full-read', 't', ? "
                        "FROM base_parameters", (ref, "f" * 64, S))
        con.commit()
    finally:
        con.close()
    E_FULL, E_SKIM, E_ONLY_SKIM = (claim(REF_A, "3", "full-read", "[PDF page 2 of 3]"),
                                   claim(REF_A, "2", "skim", "[PDF page 2 of 3]"),
                                   claim(REF_S, "1", "skim"))
    con = sqlite3.connect(DB)
    try:
        refs = [s["ref_id"] for s in ac.gather_sources(con, PE)]
        links = ac.gather_extraction_links(con, PE, [REF_A, REF_S])
        by_id = {l["extraction_id"]: l for l in links}
        vmin, vmax, unit, note, _n = ac.compose_value(con, links, "lower_is_better")
        det = ac.determine(con, PE, {"identity_code": POP, "icf_code": None,
                                     "needs_code": None, "medical_code": None},
                           SLUG_A, "fixture")
        check_vals = dbcore.check_values(con, "source_value_extractions",
                                         "extraction_method")
    finally:
        con.close()
    record("E01", "a source holding ONLY a skimmed claim does not enter the governing set",
           REF_A in refs and REF_S not in refs, refs)
    record("E02", "a skimmed claim is an EXCLUDED link with its reason, even beside a "
           "full-read claim from the same source",
           by_id.get(E_SKIM, {}).get("role") == "excluded"
           and "skim" in (by_id.get(E_SKIM, {}).get("exclusion_reason") or "")
           and by_id.get(E_FULL, {}).get("role") == "governing",
           {k: (v["role"], v["exclusion_reason"]) for k, v in by_id.items()
            if k in (E_FULL, E_SKIM, E_ONLY_SKIM)})
    record("E03", "the value is composed from the full-read claim ONLY (3, not the skimmed "
           "2 or 1, which most-accommodating selection would otherwise pick)",
           vmax == 3.0 and unit == "mm", (vmin, vmax, unit, note))
    record("E04", "the engine's output STATES the exclusion",
           sorted(det.get("excluded_not_publishable") or []) == sorted([E_SKIM, E_ONLY_SKIM]),
           det.get("excluded_not_publishable"))
    record("E05", "the rule still names a value the column's own CHECK declares (a renamed "
           "method cannot silently disarm it)",
           set(getattr(ac, "NOT_PUBLISHABLE_METHODS", ())) <= check_vals
           and getattr(ac, "NOT_PUBLISHABLE_METHODS", None), check_vals)

    # ── U: follow-ups, and the advisory reader ───────────────────────────────────────
    raise_fu, resolve_fu = fn("raise_follow_up"), fn("resolve_follow_up")
    RSN = "read-outside-admitting-purpose"
    expect_refusal("U01", "raise-follow-up refuses an unknown extraction",
                   "no such extraction", raise_fu, 10 ** 9, RSN, "w", S)
    expect_refusal("U02", "raise-follow-up refuses a blank warrant",
                   "--warrant", raise_fu, E_FULL, RSN, "  ", S)
    expect_refusal("U03", "raise-follow-up refuses a reason outside the column's CHECK",
                   "CHECK", raise_fu, E_FULL, "a-new-reason", "w", S)
    u4 = attempt(raise_fu, E_FULL, RSN, "fixture: re-check against the parameter's own "
                 "literature", S)
    record("U04", "raise-follow-up writes an open follow-up", u4.get("follow_up_id"), u4)
    expect_refusal("U05", "a second OPEN follow-up for the same extraction and reason is refused",
                   "already has open", raise_fu, E_FULL, RSN, "again", S)
    fa1 = run_audit("extraction_follow_up_audit.py")
    # A LIVE determination governed by that extraction: set by SQL, as in L03.
    LIVE = x("INSERT INTO specifications (parameter_id, identity_code, state, created_at, "
             "created_by_session) VALUES (?, ?, 'pending', 't', ?)", PE, POP, S)
    x("INSERT INTO specification_extraction_links (specification_id, extraction_id, role, "
      "created_at, created_by_session) VALUES (?, ?, 'governing', 't', ?)", LIVE, E_FULL, S)
    fa2 = run_audit("extraction_follow_up_audit.py")
    record("U06", "the follow-up audit lists the open follow-up and passes with no live "
           "value on it, then FAILS once a live determination is governed by it",
           fa1.returncode == 0 and f"follow-up {u4.get('follow_up_id')}" in fa1.stdout
           and fa2.returncode == 1 and "open follow-up" in fa2.stdout,
           fa1.stdout[-300:] + fa2.stdout[-300:])
    x("INSERT INTO specification_extraction_links (specification_id, extraction_id, role, "
      "created_at, created_by_session) VALUES (?, ?, 'governing', 't', ?)",
      LIVE, E_ONLY_SKIM, S)   # a governing SKIMMED link, which the engine never writes
    fa3 = run_audit("extraction_follow_up_audit.py")
    record("U07", "the follow-up audit FAILS a live determination governed by a skimmed "
           "figure", fa3.returncode == 1 and "SKIMMED" in fa3.stdout, fa3.stdout[-300:])
    x("DELETE FROM specification_extraction_links WHERE specification_id=?", LIVE)
    x("UPDATE specifications SET retired_at='t', retired_by_session=?, "
      "retirement_reason='fixture done' WHERE specification_id IN (?, ?)", S, LIVE, SPEC)
    u8 = attempt(resolve_fu, u4.get("follow_up_id"), "fixture: re-checked, it holds", S)
    msg = refusal(resolve_fu, u4.get("follow_up_id"), "again", S)
    u9 = attempt(raise_fu, E_FULL, RSN, "fixture: a new question", S)
    record("U08", "resolve-follow-up closes it; a second resolution is refused; a new "
           "follow-up may then be opened", u8.get("resolved") is True
           and msg and "was resolved by" in msg and u9.get("follow_up_id"), f"{u8} {msg} {u9}")
    # T-012: an absence finding owes a tested value; a skimmed figure owes no follow-up row
    # (extraction_method = 'skim' already holds that debt, so its reason is not in the CHECK).
    ABS = dbcore.ABSENCE_FOLLOW_UP_REASON
    E_ABS = xfig("INSERT INTO source_value_extractions (ref_id, slug, parameter_id, "
                 "claim_type, claim_text, extraction_method, created_at, "
                 "updated_at, figure_role) VALUES (?, ?, ?, 'absent', 'fixture', "
                 "'full-read', 't', 't', 'finding')", REF_A, SLUG_A, PE)  # a row no writer here makes
    t0 = refusal(raise_fu, E_FULL, ABS, "fixture: not an absence", S)
    t1 = attempt(raise_fu, E_ABS, ABS, "fixture: tested value still to find", S)
    t1_again = refusal(raise_fu, E_ABS, ABS, "again", S)
    # The audit lists it and counts it though the only link to it is `excluded`.
    LIVE2 = x("INSERT INTO specifications (parameter_id, identity_code, state, created_at, "
              "created_by_session) VALUES (?, ?, 'pending', 't', ?)", PE, POP, S)
    x("INSERT INTO specification_extraction_links (specification_id, extraction_id, role, "
      "exclusion_reason, created_at, created_by_session) VALUES (?, ?, 'excluded', "
      "'fixture: a finding supplies no value', 't', ?)", LIVE2, E_ABS, S)
    fa4 = run_audit("extraction_follow_up_audit.py")
    x("DELETE FROM specification_extraction_links WHERE specification_id=?", LIVE2)
    x("UPDATE specifications SET retired_at='t', retired_by_session=?, "
      "retirement_reason='fixture done' WHERE specification_id=?", S, LIVE2)
    t1_res = attempt(resolve_fu, t1.get("follow_up_id"), "fixture: tested value found", S)
    record("T012-01", "raise-follow-up writes an open follow-up for an absence finding "
           "owing a tested value; a second open one is refused; resolve-follow-up closes it",
           t1.get("follow_up_id") and t1_again and "already has open" in t1_again
           and t1_res.get("resolved") is True, f"{t1} {t1_again} {t1_res}")
    record("T012-02", "raise-follow-up refuses the absence reason on a row whose claim_type is "
           "not 'absent', naming the claim_type and the extraction",
           t0 and "'numerical'" in t0 and f"extraction {E_FULL}" in t0, t0)
    record("T012-03", "the follow-up audit LISTS an open absence follow-up whose only link is "
           "`excluded`, with its claim_type and the determination reaching it, counts it in "
           "EXAMINED, and does not fail it",
           fa4.returncode == 0 and f"follow-up {t1.get('follow_up_id')}: extraction {E_ABS}"
           in fa4.stdout and "claim_type=absent" in fa4.stdout
           and f"{LIVE2} as excluded" in fa4.stdout
           and "1 open absence follow-up(s)" in fa4.stdout, fa4.stdout[-700:] + fa4.stderr)
    con = sqlite3.connect(DB)
    try:
        reasons = dbcore.check_values(con, "extraction_follow_ups", "reason")
    finally:
        con.close()
    record("T012-04", "the column's CHECK admits exactly the cross-slug reason and the absence "
           "reason: any other extra value (a skimmed-figure reason among them) turns this red",
           reasons == {"read-outside-admitting-purpose", "absence-needs-tested-value"},
           reasons)
    expect_refusal("T012-05", "raise-follow-up refuses a skimmed-figure reason: that debt "
                   "is extraction_method = 'skim', not a second home in a follow-up row",
                   "CHECK", raise_fu, E_ONLY_SKIM, "skimmed-needs-full-read", "w", S)

    # ── T-026: a form says how it is attested; a search says which forms it fired ─────
    # Every probe is chosen by query; every fixture is labelled TASK-FIXTURE, made by SQL on
    # this copy where the writer under test would otherwise make the state it is meant to
    # distinguish (T026-01/02), and removed again where a later audit reads the table.
    T26S = "session_2026-11-13-t026-task-fixture"        # post-cutoff, so the audit reads it
    HAS_ATT = "attestation" in [r[1] for r in q("PRAGMA table_info(term_aliases)")]
    con = sqlite3.connect(DB)
    try:
        held_tokens = set()
        for (nm,) in con.execute("SELECT canonical_en FROM terms UNION ALL SELECT alias FROM "
                                 "term_aliases"):
            held_tokens |= db._name_tokens(nm)
        FIXW = [w for w in ("taskfixturea", "taskfixtureb", "taskfixturec", "taskfixtured",
                            "taskfixturee", "taskfixturef", "taskfixtureg") if w not in held_tokens]
        LJ_EN = con.execute("SELECT language, jurisdiction FROM lang_jur_map WHERE "
                            "upper(language)='EN' ORDER BY jurisdiction LIMIT 1").fetchone()
        LJ_NO = con.execute(
            "SELECT a.language, b.jurisdiction FROM (SELECT DISTINCT language FROM lang_jur_map) a, "
            "(SELECT DISTINCT jurisdiction FROM lang_jur_map) b WHERE NOT EXISTS (SELECT 1 FROM "
            "lang_jur_map m WHERE m.language=a.language AND m.jurisdiction=b.jurisdiction) "
            "ORDER BY 1, 2 LIMIT 1").fetchone()
        LAB = next(((t, n) for t, n in con.execute("SELECT term_id, canonical_en FROM terms")
                    if len(db._name_tokens(n)) >= 2), None)
        ALANG = db._alias_language(con, "EN")
    finally:
        con.close()
    T26 = FREE[17:21]                                     # four terms nothing else here touched
    if len(FIXW) < 7 or len(T26) < 4 or not (LJ_EN and LJ_NO and LAB):
        print("      SKIPPED-NO-FIXTURE: T026 needs 7 unheld words, 4 free terms, an EN pair, "
              "an unpaired pair and a two-token label")
    else:
        def seed_sql(term, text, att, **loc):
            cols = {"term_id": term, "alias": text, "language": ALANG, "alias_type": "SYNONYM",
                    "notes": "model-generated TASK-FIXTURE", "created_at": "2026-11-13 00:00",
                    "created_by_session": T26S, "updated_at": "2026-11-13 00:00",
                    "updated_by_session": T26S}
            if HAS_ATT:
                cols["attestation"] = att
                cols.update(loc)
            return x(f"INSERT INTO term_aliases ({','.join(cols)}) VALUES "
                     f"({','.join('?' * len(cols))})", *cols.values())

        def near(name):
            c = sqlite3.connect(DB)
            try:
                return {t for t, _ in db._near_terms(c, name)}
            finally:
                c.close()

        # T026-01 (AT-24 a): a model seed made by SQL (never by the new writer, which the old
        # code lacks) is not vocabulary: _near_terms does not return its term.
        seed_a = f"{FIXW[0]} {FIXW[1]}"
        seed_sql(T26[0], seed_a, "model_seed")
        record("T026-01", "_near_terms does not compare a model_seed alias (AT-24 a): a seed is a "
               "search aid, so it neither names a concept nor blocks a new one",
               HAS_ATT and T26[0] not in near(f"{seed_a} {FIXW[2]}"), near(f"{seed_a} {FIXW[2]}"))
        # T026-02: the positive control, and a label still screens.
        att_a = f"{FIXW[3]} {FIXW[4]}"
        seed_sql(T26[1], att_a, "instrument", jurisdiction=LJ_EN[1],
                 source_url="https://example.org/task-fixture", source_clause="1.1")
        record("T026-02", "_near_terms still returns the term of an instrument-attested alias, and "
               "of a label: the screen was narrowed, not switched off",
               HAS_ATT and T26[1] in near(f"{att_a} {FIXW[5]}") and LAB[0] in near(f"{LAB[1]} {FIXW[6]}"),
               (near(f"{att_a} {FIXW[5]}"), near(f"{LAB[1]} {FIXW[6]}")))

        # T026-03 (AT-24 b): a search that fired the seed is found by the flag join; the junction
        # stores the form's KEY, not the rowid.
        rid = q("SELECT rowid FROM term_aliases WHERE term_id=? AND alias=?", T26[0], seed_a)
        LS = ["log-search", "--prior-expectation", "fixture: nothing", "--slug", SLUG_A,
              "--language", "EN", "--query-text", "TASK-FIXTURE fixture query", "--engine", "web",
              "--depth-method", "scoping", "--session", S]
        r3 = run(*LS, *(["--form-id", str(rid[0][0])] if rid else []))
        e3 = json.loads(r3.stdout)["exec_id"] if r3.returncode == 0 and r3.stdout.strip() else None
        flagged = q("SELECT DISTINCT f.exec_id FROM search_execution_forms f JOIN term_aliases a "
                    "USING (term_id, alias, language) WHERE a.attestation NOT IN "
                    "('instrument','other_source')")
        stored = q("SELECT term_id, alias, language FROM search_execution_forms WHERE exec_id=?", e3)
        record("T026-03", "log-search --form-id writes a search_execution_forms row by the form's key, "
               "and the flag join (a seed's attestation) finds the search (AT-24 b)",
               e3 and (e3,) in flagged and stored == [(T26[0], seed_a, ALANG)],
               (r3.stdout[-200:], r3.stderr[-300:], flagged, stored))

        # T026-04: --terms-used is refused naming --form-id; an unknown --form-id is refused;
        # neither writes anything.
        n_ex, n_jn = (q("SELECT COUNT(*) FROM search_executions")[0][0],
                      q("SELECT COUNT(*) FROM search_execution_forms")[0][0])
        r4a = run(*LS, "--terms-used", '["x"]')
        r4b = run(*LS, "--form-id", "999999999")
        record("T026-04", "log-search refuses --terms-used (naming --form-id) and a --form-id that "
               "names no row, and writes nothing for either",
               r4a.returncode == 1 and "--form-id" in r4a.stderr and r4b.returncode == 1
               and "names no term_aliases row" in r4b.stderr
               and (q("SELECT COUNT(*) FROM search_executions")[0][0],
                    q("SELECT COUNT(*) FROM search_execution_forms")[0][0]) == (n_ex, n_jn),
               (r4a.returncode, r4a.stderr[-200:], r4b.returncode, r4b.stderr[-200:]))

        # T026-05: the base route writes the locator and attestation; it promotes a seed in place
        # (one row, type kept); an observation route cannot re-attest an attested row.
        aliasfn = fn("add_alias")
        base_kw = dict(language=LJ_EN[0], jurisdiction=LJ_EN[1], source_url="https://example.org/t26",
                       source_clause="2.3", attestation="instrument")
        b5 = attempt(aliasfn, T26[2], None, "SYNONYM", S, alias="corridor route", **base_kw)
        r5 = q("SELECT attestation, source_url, source_clause, jurisdiction, observation_id FROM "
               "term_aliases WHERE term_id=? AND alias='corridor route'", T26[2])
        seed_sql(T26[3], "door leaf", "model_seed")
        n_t3 = q("SELECT COUNT(*) FROM term_aliases WHERE term_id=?", T26[3])[0][0]
        p5 = attempt(aliasfn, T26[3], None, "SYNONYM", S, alias="door leaf", **base_kw)
        r5p = q("SELECT attestation, alias_type, source_clause FROM term_aliases WHERE term_id=? "
                "AND alias='door leaf'", T26[3])
        o5 = attempt(observe, obs("corridor route", "PDF page 2 / T026",
                                  "the clear width of a corridor route is measured here"), S)
        attempt(adj, o5.get("observation_id"), "NAMES-EXISTING", "fixture", S, term_id=T26[2])
        d5 = refusal(aliasfn, T26[2], o5.get("observation_id"), "SYNONYM", S)
        record("T026-05", "add-alias base route writes the locator and attestation; it promotes a "
               "seed in place (one row, type kept); a held instrument row is refused by the "
               "observation route (no downgrade)",
               r5 == [("instrument", "https://example.org/t26", "2.3", LJ_EN[1], None)]
               and p5.get("promoted") is True
               and r5p == [("instrument", "SYNONYM", "2.3")]
               and q("SELECT COUNT(*) FROM term_aliases WHERE term_id=?", T26[3])[0][0] == n_t3
               and d5 and "already holds" in d5
               and q("SELECT attestation FROM term_aliases WHERE term_id=? AND alias='corridor route'",
                     T26[2]) == [("instrument",)], (b5, r5, p5, r5p, d5))

        # T026-06: the refusals of the base and seed routes; none writes a row.
        n_all = q("SELECT COUNT(*) FROM term_aliases")[0][0]
        c6 = [refusal(aliasfn, T26[2], None, "SYNONYM", S, alias="t26 nolocator", **{**base_kw, "source_clause": None}),
              refusal(aliasfn, T26[2], None, "SYNONYM", S, alias="t26 nourl", **{**base_kw, "source_url": None}),
              refusal(aliasfn, T26[2], None, "SYNONYM", S, alias="t26 badpair",
                      **{**base_kw, "language": LJ_NO[0], "jurisdiction": LJ_NO[1]}),
              refusal(aliasfn, T26[2], None, "SYNONYM", S, alias="t26 seedloc", language=LJ_EN[0],
                      seed="owner_supplied", source_url="https://example.org/t26"),
              refusal(aliasfn, T26[2], None, "SYNONYM", S, alias="t26 seedatt", language=LJ_EN[0],
                      seed="instrument"),
              refusal(aliasfn, T26[2], 1, "SYNONYM", S, alias="t26 twoRoutes", **base_kw)]
        want6 = ["--source-page or --source-clause", "--source-url", "lang_jur_map holds no pair",
                 "--source-url", "an attestation needs a locator", "exactly one route"]
        record("T026-06", "add-alias refuses a base route with no locator or no URL, a pair "
               "lang_jur_map lacks, a seed with a locator, a seed that is an attestation, and "
               "two routes; each in words, none writes a row",
               all(m and w in m for m, w in zip(c6, want6))
               and q("SELECT COUNT(*) FROM term_aliases")[0][0] == n_all, c6)

        # T026-07/08: the audit reads the typed column first, and still fails an unrecorded,
        # unmarked post-cutoff row.
        def owner_total(out):
            for line in out.splitlines():
                if line.startswith("all "):
                    return int(line.split()[5])
        a0 = run_audit("alias_provenance_audit.py")
        seed_sql(T26[3], "t26 owner supplied", "owner_supplied")
        x("UPDATE term_aliases SET notes=NULL WHERE alias='t26 owner supplied'")
        a7 = run_audit("alias_provenance_audit.py")
        record("T026-07", "alias_provenance_audit counts a post-cutoff owner_supplied row with no notes "
               "as OWNER-SUPPLIED and exits 0",
               a7.returncode == 0 and a0.returncode == 0 and owner_total(a7.stdout) is not None
               and owner_total(a7.stdout) == (owner_total(a0.stdout) or 0) + 1,
               (a0.stdout[-300:], a7.stdout[-500:], a7.stderr[-200:]))
        seed_sql(T26[3], "t26 unrecorded", "unrecorded")
        x("UPDATE term_aliases SET notes=NULL WHERE alias='t26 unrecorded'")
        a8 = run_audit("alias_provenance_audit.py")
        x("DELETE FROM term_aliases WHERE alias IN ('t26 unrecorded', 't26 owner supplied')")
        record("T026-08", "an unrecorded post-cutoff row with no marker still fails the audit "
               "(the refusal is not weakened)",
               a8.returncode == 1 and "t26 unrecorded" in a8.stdout, a8.stdout[-400:])

        # T026-09: R11 accepts a typed attestation in place of a note, and still fails an
        # unrecorded row with an empty note, scoped to a fixture session.
        SD = "session_2026-11-13-t026-dod-fixture"
        d9 = attempt(aliasfn, T26[2], None, "SYNONYM", SD, alias="t26 dod base", **base_kw)
        g9a = run("--session", SD, script="audit/research_batch_dod.py")
        x("INSERT INTO term_aliases (term_id, alias, language, alias_type, notes, created_at, "
          "created_by_session, updated_at, updated_by_session) VALUES (?, 't26 dod bare', ?, "
          "'SYNONYM', NULL, 't', ?, 't', ?)", T26[2], ALANG, SD, SD)
        g9b = run("--session", SD, script="audit/research_batch_dod.py")
        record("T026-09", "research_batch_dod R11 passes a base-route row with empty notes and "
               "fails an unrecorded row with empty notes",
               "R11: PASS" in g9a.stdout and "R11:" in g9b.stdout and "R11: PASS" not in g9b.stdout
               and "no typed attestation" in g9b.stdout, (d9, g9a.stdout[-300:], g9b.stdout[-500:]))
        x("DELETE FROM term_aliases WHERE alias='t26 dod bare'")      # the audit below reads the table

        # ── T026 repair pass: the screen, the instrument warrant, the locator, the language, the
        # reader, promotion, the owner seed, the key, the withheld model seed ───────────────────
        T27 = FREE[21:27]
        R_PAIRS = sqlite3.connect(DB)
        try:
            LJ_TWO = R_PAIRS.execute(
                "SELECT language, MIN(jurisdiction), MAX(jurisdiction) FROM lang_jur_map "
                "GROUP BY language HAVING COUNT(*) > 1 ORDER BY language LIMIT 1").fetchone()
            REF_A_ROW = R_PAIRS.execute("SELECT tier, evidence_type, scope, jurisdiction FROM "
                                        "evidence_sources WHERE ref_id=?", (REF_A,)).fetchone()
            FR_PAIR = R_PAIRS.execute("SELECT language FROM lang_jur_map WHERE upper(language) "
                                      "<> 'EN' ORDER BY language LIMIT 1").fetchone()
            from schemas.tier_derivation import TIER_MAP            # the ladder, not a list here
            REG = next(iter(sorted(k for k, tier in TIER_MAP.items() if tier >= 4)), None)
            # a ledger heading whose entry names a word as a whole token, once, owner's words
            led = dbcore.LEDGER_PATH.read_text(encoding="utf-8").splitlines()
            heads = [(i, l[3:].strip()) for i, l in enumerate(led) if l.startswith("## ")]

            def heading_word(delegated):
                for k, (i, h) in enumerate(heads):
                    if not re.search(r"\d{4}-\d{2}-\d{2}", h) or \
                            h.startswith(dbcore.LEDGER_DELEGATED_PREFIX) != delegated:
                        continue
                    if dbcore.ledger_heading_count(h) != 1:
                        continue
                    body = "\n".join(led[i + 1:heads[k + 1][0] if k + 1 < len(heads) else None])
                    for w in re.findall(r"(?<![A-Za-z0-9-])[a-z]{9,14}(?![A-Za-z0-9-])", body):
                        if dbcore.ledger_entry_names(h, w):
                            return h, w
                return None
            OWN, DEL = heading_word(False), heading_word(True)
        finally:
            R_PAIRS.close()
        if len(T27) < 6 or not (LJ_TWO and OWN and DEL and FR_PAIR and REG):
            print("      SKIPPED-NO-FIXTURE: the T026 repair cases need 6 free terms, a language "
                  "with two jurisdictions, a non-EN language, an owner heading and a delegated one")
        else:
            def reg_state(on):
                """REF_A as a regulatory-stratum source (on) or as it was: SQL on the copy."""
                if on:
                    x("UPDATE evidence_sources SET evidence_type=?, scope=?, tier=6 WHERE ref_id=?",
                      REG[0], REG[1], REF_A)
                else:
                    x("UPDATE evidence_sources SET evidence_type=?, scope=?, tier=? WHERE ref_id=?",
                      REF_A_ROW[1], REF_A_ROW[2], REF_A_ROW[0], REF_A)

            def seed_row(term, text, atype="SYNONYM", att="model_seed", lang=None, jur=None):
                x("INSERT INTO term_aliases (term_id, alias, language, alias_type, jurisdiction, "
                  "notes, created_at, created_by_session, updated_at, updated_by_session, "
                  "attestation) VALUES (?, ?, ?, ?, ?, 'model-generated TASK-FIXTURE', "
                  "'2026-11-13 00:00', ?, '2026-11-13 00:00', ?, ?)",
                  term, text, lang or ALANG, atype, jur, T26S, T26S, att)

            # T026-10 (finding 1): the screen is not switched off. An `unrecorded` EN alias still
            # screens a near name; the same row typed model_seed does not.
            cands = q("SELECT term_id, alias FROM term_aliases WHERE upper(language)='EN' AND "
                      "attestation='unrecorded' AND created_by_session <> ? ORDER BY term_id, alias", T26S)
            pick = None
            for t_, a_ in cands:
                if len(db._name_tokens(a_)) < 2:
                    continue
                nm = f"{a_} {FIXW[6]}"
                if t_ in near(nm):
                    x("UPDATE term_aliases SET attestation='model_seed' WHERE term_id=? AND alias=? "
                      "AND upper(language)='EN'", t_, a_)
                    gone = t_ not in near(nm)
                    x("UPDATE term_aliases SET attestation='unrecorded' WHERE term_id=? AND alias=? "
                      "AND upper(language)='EN'", t_, a_)
                    if gone:
                        pick = (t_, a_, nm)
                        break
            record("T026-10", "_near_terms still compares an `unrecorded` EN alias (a live refusal is "
                   "not weakened on an open question) and stops comparing it only when it is typed "
                   "model_seed", bool(pick) and pick[0] in near(pick[2]), pick)

            # T026-11 (finding 2a): `instrument` by the observation route needs a regulatory-stratum
            # source, derived from the tier ladder; other_source needs none, and writes the pointer.
            def make_obs(term, phrase, loc):
                """An observation of `phrase` on REF_A (its quote is in the fixture text), adjudicated to `term`."""
                o = attempt(observe, obs(phrase, loc, "the clear width of a door leaf is measured "
                                         "here" if phrase == "door leaf" else
                                         "the clear width of a corridor route is measured here"), S)
                attempt(adj, o.get("observation_id"), "NAMES-EXISTING", "fixture", S, term_id=term)
                return o.get("observation_id")
            m11 = refusal(aliasfn, T27[0], make_obs(T27[0], "door leaf", "PDF page 1 / T026a"),
                          "SYNONYM", S, attestation="instrument")
            reg_state(True)
            o11 = make_obs(T27[1], "door leaf", "PDF page 1 / T026b")
            w11 = attempt(aliasfn, T27[1], o11, "SYNONYM", S, attestation="instrument")
            reg_state(False)
            o11b = make_obs(T27[2], "door leaf", "PDF page 1 / T026c")
            w11b = attempt(aliasfn, T27[2], o11b, "SYNONYM", S)
            record("T026-11", "add-alias: `instrument` by observation needs a regulatory-stratum source "
                   "(refused naming the tier and evidence_type otherwise); the default writes "
                   "other_source and the observation pointer",
                   m11 and f"tier {REF_A_ROW[0]}" in m11 and f"'{REF_A_ROW[1]}'" in m11
                   and q("SELECT attestation, observation_id FROM term_aliases WHERE term_id=? AND "
                         "alias='door leaf'", T27[1]) == [("instrument", o11)]
                   and q("SELECT attestation, observation_id FROM term_aliases WHERE term_id=? AND "
                         "alias='door leaf'", T27[2]) == [("other_source", o11b)],
                   (m11, w11, w11b))

            # T026-12 (finding 2b): a locator that is not one is refused by the writer AND the DDL.
            c12 = [refusal(aliasfn, T27[3], None, "SYNONYM", S, alias="t26 blankloc", language=LJ_EN[0],
                           jurisdiction=LJ_EN[1], attestation="other_source",
                           source_url="http://", source_page="", source_clause=" "),
                   refusal(aliasfn, T27[3], None, "SYNONYM", S, alias="t26 spaceurl", language=LJ_EN[0],
                           jurisdiction=LJ_EN[1], attestation="other_source",
                           source_url="https://example.org/a b", source_clause="1"),
                   refusal(aliasfn, T27[3], None, "SYNONYM", S, alias="t26 blankpage", language=LJ_EN[0],
                           jurisdiction=LJ_EN[1], attestation="other_source",
                           source_url="https://example.org/a", source_page="  ", source_clause="1")]
            ddl_ok = [False] * 4
            con12 = sqlite3.connect(DB)
            try:
                for k, (url, page, clause, line) in enumerate([
                        ("http://", None, "1", None), ("https://example.org/a b", None, "1", None),
                        ("https://example.org/a", "  ", None, None),
                        ("https://example.org/a", None, "1", "  ")]):
                    try:
                        con12.execute(
                            "INSERT INTO term_aliases (term_id, alias, language, alias_type, created_at, "
                            "created_by_session, updated_at, updated_by_session, attestation, source_url, "
                            "source_page, source_clause, source_line) VALUES (?, ?, ?, 'SYNONYM', 't', ?, "
                            "'t', ?, 'other_source', ?, ?, ?, ?)", (T27[3], f"t26 ddl{k}", ALANG, T26S,
                                                                      T26S, url, page, clause, line))
                    except sqlite3.IntegrityError as exc:
                        ddl_ok[k] = "CHECK" in str(exc)
                con12.rollback()
            finally:
                con12.close()
            record("T026-12", "a blank, hostless or whitespace-bearing locator is refused by the writer "
                   "(three shapes) and by the DDL (URL host, URL whitespace, blank page, non-integer "
                   "line); no row is written",
                   all(c12) and all(ddl_ok) and q("SELECT COUNT(*) FROM term_aliases WHERE alias LIKE "
                                                  "'t26 %' AND term_id=?", T27[3])[0][0] == 0,
                   (c12, ddl_ok))

            # T026-13 (finding 3a): a search fires the forms of its own language; one junction row
            # per distinct form however often --form-id is repeated.
            fr = db._alias_language(sqlite3.connect(DB), FR_PAIR[0])
            seed_row(T27[3], "t26 forme", lang=fr)
            rid_fr = q("SELECT rowid FROM term_aliases WHERE term_id=? AND alias='t26 forme'", T27[3])[0][0]
            rid_en = q("SELECT rowid FROM term_aliases WHERE term_id=? AND alias=?", T26[0], seed_a)[0][0]
            r13a = run(*LS, "--form-id", str(rid_fr))
            r13b = run(*LS, "--form-id", str(rid_en), "--form-id", str(rid_en))
            e13 = json.loads(r13b.stdout)["exec_id"] if r13b.returncode == 0 else None
            record("T026-13", "log-search refuses a form of another language than the search (naming both) "
                   "and writes one junction row for a repeated --form-id",
                   r13a.returncode == 1 and repr(fr) in r13a.stderr and "'EN'" in r13a.stderr
                   and q("SELECT COUNT(*) FROM search_execution_forms WHERE exec_id=?", e13) == [(1,)],
                   (r13a.stderr[-300:], r13b.stdout[-200:], r13b.stderr[-200:]))

            # T026-14 (finding 3b): the audit READS the zero-result searches against the junction:
            # no form recorded, an unattested form, an attested form; it does not fail on them.
            def exec_of(*extra):
                r = run(*LS, *extra)
                return json.loads(r.stdout)["exec_id"] if r.returncode == 0 else None
            e_none = exec_of()
            e_un = exec_of("--form-id", str(rid_en))
            e_att = exec_of("--form-id", str(q("SELECT rowid FROM term_aliases WHERE term_id=? AND alias=?",
                                               T26[1], att_a)[0][0]))
            a14 = run_audit("alias_provenance_audit.py")
            ex = lambda n: re.search(rf"exec {n} \(EN\): (\d+) form\(s\) recorded, (\d+) attested", a14.stdout)
            got = [ex(e_none), ex(e_un), ex(e_att)]
            record("T026-14", "alias_provenance_audit reads each zero-result search: 0 forms / 0 attested, "
                   "1 form / 0 attested (flagged), 1 form / 1 attested; counts them in EXAMINED; exit 0",
                   a14.returncode == 0 and all(got)
                   and [g.groups() for g in got] == [("0", "0"), ("1", "0"), ("1", "1")]
                   and f"exec {e_none} (EN): 0 form(s) recorded, 0 attested  <- no attested form" in a14.stdout
                   and f"exec {e_att} (EN): 1 form(s) recorded, 1 attested\n" in a14.stdout
                   and re.search(r"EXAMINED: (\d+)", a14.stdout)
                   and int(re.search(r"EXAMINED: (\d+)", a14.stdout).group(1)) ==
                   q("SELECT COUNT(*) FROM term_aliases")[0][0] +
                   q("SELECT COUNT(*) FROM search_executions WHERE results_found=0 AND deferred_reason IS NULL")[0][0],
                   (a14.returncode, [g and g.groups() for g in got], a14.stdout[-700:]))

            # T026-15 (findings 4, 6, 11): the seed route writes the seed value (owner_supplied, with a
            # ledger heading naming the alias); model_seed is withheld; the refusals of the approval.
            w_own, w_ref = OWN[1], OWN[0]
            s15 = attempt(aliasfn, T27[4], None, "SYNONYM", S, alias=w_own, language=LJ_EN[0],
                          seed="owner_supplied", approval_ref=w_ref)
            m15 = [refusal(aliasfn, T27[4], None, "SYNONYM", S, alias="t26 model", language=LJ_EN[0],
                           seed="model_seed", approval_ref=w_ref),
                   refusal(aliasfn, T27[4], None, "SYNONYM", S, alias="t26 noref", language=LJ_EN[0],
                           seed="owner_supplied"),
                   refusal(aliasfn, T27[4], None, "SYNONYM", S, alias="t26 notnamed", language=LJ_EN[0],
                           seed="owner_supplied", approval_ref=w_ref),
                   refusal(aliasfn, T27[4], None, "SYNONYM", S, alias=DEL[1], language=LJ_EN[0],
                           seed="owner_supplied", approval_ref=DEL[0])]
            record("T026-15", "add-alias --seed owner_supplied writes attestation owner_supplied and prints "
                   "its ledger heading; model_seed is refused naming OR-17; no heading, a heading that "
                   "does not name the alias, and a Delegated resolution are refused",
                   s15.get("attestation") == "owner_supplied" and s15.get("approval_ref") == w_ref
                   and q("SELECT attestation, notes FROM term_aliases WHERE term_id=? AND alias=?",
                         T27[4], w_own) == [("owner_supplied", None)]
                   and m15[0] and "OR-17" in m15[0] and "owner question" in m15[0]
                   and m15[1] and "--approval-ref" in m15[1] and m15[2] and "does not name" in m15[2]
                   and m15[3] and "delegated" in m15[3], (s15, m15))

            # T026-16 (finding 5, and mutants of finding 4): promotion keeps nothing it must not.
            seed_row(T27[5], "t26 legacy", atype="TRANSLATION")
            seed_row(T27[5], "t26 jur", jur="TASK-FIXTURE-J")
            seed_row(T27[0], "t26 pair", lang=db._alias_language(sqlite3.connect(DB), LJ_TWO[0]), jur=LJ_TWO[1])
            kw2 = dict(language=LJ_TWO[0], source_url="https://example.org/t26", source_clause="2.3",
                       attestation="instrument")
            c16 = [refusal(aliasfn, T27[5], None, "SYNONYM", S, alias="t26 legacy", **base_kw),
                   refusal(aliasfn, T27[0], None, "SYNONYM", S, alias="t26 pair", jurisdiction=LJ_TWO[2], **kw2),
                   ]
            seed_row(T27[5], "corridor route", jur="TASK-FIXTURE-J")
            c16.append(refusal(aliasfn, T27[5], make_obs(T27[5], "corridor route", "PDF page 2 / T026j"),
                               "SYNONYM", S))
            # a source with NO jurisdiction does not promote a row that carries one
            seed_row(T27[5], "door leaf", jur=REF_A_ROW[3] or "US")
            o_nj = make_obs(T27[5], "door leaf", "PDF page 1 / T026n")
            x("UPDATE evidence_sources SET jurisdiction=NULL WHERE ref_id=?", REF_A)
            c16.append(refusal(aliasfn, T27[5], o_nj, "SYNONYM", S))
            x("UPDATE evidence_sources SET jurisdiction=? WHERE ref_id=?", REF_A_ROW[3], REF_A)
            SD2 = "session_2026-11-13-t026-promoter"
            p16 = attempt(aliasfn, T27[0], None, "SYNONYM", SD2, alias="t26 pair", jurisdiction=LJ_TWO[1], **kw2)
            row16 = q("SELECT attestation, jurisdiction, created_by_session, updated_by_session FROM term_aliases "
                      "WHERE term_id=? AND alias='t26 pair'", T27[0])
            g16 = run("--session", SD2, script="audit/research_batch_dod.py")
            record("T026-16", "promotion is refused for a legacy TRANSLATION row and for a held jurisdiction "
                   "that is not the attesting one (both routes, a source with none included); a promotion "
                   "keeps created_by_session, sets updated_by_session, and R11's scope counts it",
                   c16[0] and "legacy type" in c16[0] and c16[1] and "jurisdiction" in c16[1]
                   and c16[2] and "jurisdiction" in c16[2] and c16[3] and "jurisdiction" in c16[3]
                   and p16.get("promoted") is True
                   and row16 == [("instrument", LJ_TWO[1], T26S, SD2)]
                   and "1 alias(es) written by this batch" in g16.stdout,
                   (c16, p16, row16, g16.stdout[-400:]))

            # T026-17 (finding 10): the junction follows a corrected spelling and refuses a vanished form.
            fk = sqlite3.connect(DB)
            fk.execute("PRAGMA foreign_keys=ON")
            try:
                try:
                    fk.execute("UPDATE term_aliases SET alias='t26 respelt' WHERE term_id=? AND alias=?",
                               (T26[0], seed_a))
                    moved = fk.execute("SELECT COUNT(*) FROM search_execution_forms WHERE term_id=? "
                                       "AND alias='t26 respelt'", (T26[0],)).fetchone()[0]
                except sqlite3.IntegrityError:
                    moved = 0                      # the key is frozen by the junction row
                try:
                    fk.execute("DELETE FROM term_aliases WHERE term_id=? AND alias='t26 respelt'", (T26[0],))
                    deleted = True
                except sqlite3.IntegrityError:
                    deleted = False
                fk.rollback()
            finally:
                fk.close()
            record("T026-17", "an UPDATE of a searched form's spelling propagates to search_execution_forms; "
                   "a DELETE of it is refused", moved >= 1 and deleted is False, (moved, deleted))

    # ── A: the observation-quote backstop can go red ─────────────────────────────────
    a1 = run_audit("observation_verbatim_audit.py")
    x("INSERT INTO observed_terms (ref_id, surface_form, language, locator, context_quote, "
      "created_at, created_by_session) VALUES (?, 'invented', 'EN', 'nowhere', "
      "'an invented quote no artefact carries', 't', ?)", REF_A, S)
    # ^ fault injection: a row written past the writer, which is what this backstop is for
    a2 = run_audit("observation_verbatim_audit.py")
    record("A04", "observation_verbatim_audit counts by class and FAILS when a class rises "
           "above its baseline",
           "EXAMINED:" in a1.stdout and a2.returncode == 1 and "missing:" in a2.stdout,
           a1.stdout[-300:] + a2.stdout[-300:])

    # ── G: the batch rules on the copy ───────────────────────────────────────────────
    B23 = q("SELECT created_by_session, COUNT(*) FROM evidence_sources GROUP BY 1 "
            "ORDER BY MAX(created_at) DESC LIMIT 1")[0][0]

    def gate():
        return run("--session", B23, script="audit/research_batch_dod.py")

    g1 = gate()
    adm = q("SELECT ref_id FROM evidence_sources WHERE created_by_session=? AND "
            "superseded_by_ref_id IS NULL ORDER BY ref_id LIMIT 1", B23)[0][0]
    # A post-rule admission: no writer back-dates or post-dates created_at, so the copy is
    # moved forward by SQL to put one admission after R16_SCAN_FROM.
    x("UPDATE evidence_sources SET created_at='2026-10-10 00:01' WHERE ref_id=?", adm)
    g2 = gate()
    record("G01", "R16-scan grandfathers a batch admitted before the reading record "
           "(reported, not failed) and FAILS an admission after it with no catalogue "
           "reading", "R16-scan: PASS" in g1.stdout and "REPORTED" in g1.stdout
           and "R16-scan:" in g2.stdout and f"no catalogue-mode reading: {adm}" in g2.stdout,
           g1.stdout[-200:] + g2.stdout[-400:])
    sha_adm = put("fixture-adm.html", b"<html><body>fixture admission text</body></html>",
                  adm)
    attempt(scan, {"ref_id": adm, "mode": "targeted", "target_parameter_id": P["B"],
                   "text_scope": "full", "file_sha256": sha_adm, "method": "full-read"}, S)
    g3 = gate()
    attempt(scan, {"ref_id": adm, "mode": "catalogue", "text_scope": "full",
                   "file_sha256": sha_adm, "method": "full-read"}, S)
    g4 = gate()
    record("G02", "a TARGETED reading does not discharge R16-scan; a catalogue reading does",
           f"no catalogue-mode reading: {adm}" in g3.stdout
           and "R16-scan: PASS" in g4.stdout, g3.stdout[-300:] + g4.stdout[-300:])
    ex = q("SELECT exec_id FROM search_admissions WHERE ref_id=? LIMIT 1", adm)
    attempt(db.unlink_admission, ex[0][0] if ex else -1, adm, "fixture: test R17", S)
    g5 = gate()
    record("G03", "R17 FAILS an admission left with no search_admissions edge",
           "R17:" in g5.stdout and f"no search_admissions edge: {adm}" in g5.stdout,
           g5.stdout[-300:])

    # ── C: everything written above can be shipped ───────────────────────────────────
    con = sqlite3.connect(DB)
    try:
        cap = set(dbcore.writable_tables(con))
    finally:
        con.close()
    NEW = ("source_scans", "extraction_follow_ups")
    record("C01", "each new table is in the derived capture set (dbcore.writable_tables)",
           set(NEW) <= cap, sorted(set(NEW) - cap))
    # The lifecycle verbs on rows the CANONICAL database already holds, so the capture
    # must render UPDATEs (rows minted in the copy are captured as INSERTs, which proves
    # nothing about updates). The open gate on the canonical parameter is resolved first,
    # through its own writer, because merge refuses over an open gate.
    PCAN = q("SELECT parameter_id FROM base_parameters WHERE created_by_session <> ? "
             "AND status = 'active' ORDER BY parameter_id LIMIT 1", S)[0][0]
    for (gid,) in q("SELECT gate_id FROM determination_gates WHERE parameter_id=? AND "
                    "resolved_at IS NULL", PCAN):
        attempt(db.resolve_determination_gate, gate_id=gid,
                rationale="fixture: resolved to exercise merge capture", session=S)
    DCAN = q("SELECT term_id FROM parameter_declinations WHERE created_by_session <> ? "
             "AND revoked_at IS NULL LIMIT 1", S)
    if DCAN:
        attempt(revoke, DCAN[0][0], "fixture: capture of a revocation", DR, S)
    n_moved = q("SELECT COUNT(*) FROM source_value_extractions WHERE parameter_id=?",
                PCAN)[0][0]
    c_m = attempt(merge, PCAN, P["B"], "fixture: capture of a merge of canonical rows", S)
    record("C01b", "merge-parameter re-points every canonical extraction of the folded "
           "parameter", c_m.get("re_pointed", {}).get(
               "source_value_extractions.parameter_id") == n_moved and n_moved > 0, c_m)
    emit_mod = importlib.import_module("emit_batch_sql")
    out_sql = os.path.join(TMP, "capture.sql")
    try:
        emit_mod.emit(DB, str(REPO / "data" / "guidebook.db"), out_sql,
                      allow_delete=["search_admissions"])
        sql = open(out_sql, encoding="utf-8").read()
    except SystemExit as exc:
        sql = f"emit refused: {exc}"
    want = ['INSERT INTO "source_scans"', APPROVAL.replace("'", "''"),
            'INSERT INTO "extraction_follow_ups"', 'UPDATE "parameter_declinations"',
            'UPDATE "base_parameters"', 'INSERT INTO "term_aliases"',
            'UPDATE "source_value_extractions"', 'UPDATE "terms"']
    record("C02", "emit_batch_sql captures every new write: readings, origins, follow-ups, "
           "revocations, lifecycle UPDATEs, aliases, re-pointed rows, renames",
           all(w in sql for w in want), [w for w in want if w not in sql] or sql[-300:])
    replay = os.path.join(TMP, "replay.db")
    shutil.copy(REPO / "data" / "guidebook.db", replay)
    rc = sqlite3.connect(replay, isolation_level=None)
    try:
        code = "\n".join(l for l in sql.splitlines() if not l.strip().startswith("--"))
        for stmt in [s for s in code.split(";\n") if s.strip()]:
            rc.execute(stmt)
        same = all(sorted(rc.execute(f'SELECT * FROM "{t}"').fetchall(), key=str)
                   == sorted(q(f'SELECT * FROM "{t}"'), key=str)
                   for t in NEW + ("base_parameters", "parameter_declinations",
                                   "term_aliases", "observed_terms", "terms"))
    except Exception as exc:  # noqa: BLE001 -- recorded red
        same = False
        print(f"      replay failed: {exc}")
    finally:
        rc.close()
    record("C03", "replaying the captured SQL onto a copy of canonical reproduces the "
           "scratch for every table T1 writes", same)

    # ── CLI: every verb is wired, refuses in a sentence, and dry-runs ────────────────
    cases = [
        ("record-scan", ["--ref-id", REF_A, "--mode", "catalogue", "--text-scope",
                         "partial", "--file-sha256", PART_SHA, "--method", "full-read",
                         "--catalogue-version", "1"], "COMPUTED"),
        ("observe-term", ["--ref-id", REF_A, "--surface-form", "x", "--context-quote",
                          "x y"], "--locator"),
        ("retire-parameter", ["--parameter-id", str(P["R"]), "--reason", "x"], "already"),
        ("merge-parameter", ["--from", str(P["B"]), "--into", str(P["B"]), "--reason", "x"],
         "same parameter"),
        ("rename-term", ["--term-id", TR, "--canonical-en", "x y", "--reason", "x"],
         "warrant"),
        ("revoke-declination", ["--term-id", TD, "--reason", "x", "--decision-ref", "nope"],
         "--decision-ref"),
        ("annotate-parameter", ["--parameter-id", str(P["B"]), "--note", " "], "--note"),
        ("add-alias", ["--term-id", TA, "--observation-id", str(OCW), "--alias-type",
                       "DEPRECATED"], "DEPRECATED"),
        ("mint-term-from-catalogue", ["--catalogue", TIER456, "--entry-ref", ENTRY,
                                      "--canonical-en", "x 1", "--definition", "d",
                                      "--approval-ref", "q"], "values"),
        ("raise-follow-up", ["--extraction-id", "999999999", "--reason", RSN,
                             "--warrant", "w"], "no such extraction"),
        ("resolve-follow-up", ["--follow-up-id", "999999999", "--resolution", "r"],
         "no such row"),
    ]
    bad = []
    for verb, argv, needle in cases:
        r = run(verb, *argv, "--session", S)
        if not (r.returncode == 1 and r.stderr.startswith("REFUSING:") and needle in r.stderr
                and "Traceback" not in r.stderr):
            bad.append(f"{verb}: rc={r.returncode} {r.stderr[-200:]!r}")
    record("CLI1", f"all {len(cases)} new or changed verbs are wired and refuse in a sentence, "
           f"not a traceback", not bad, bad)
    r = run("annotate-parameter", "--parameter-id", str(P["B"]), "--note", "fixture dry",
            "--session", S, "--dry-run")
    record("CLI2", "a --dry-run writes nothing",
           r.returncode == 0 and "fixture dry" not in (q(
               "SELECT notes FROM base_parameters WHERE parameter_id=?", P["B"])[0][0] or ""),
           r.stdout + r.stderr)
except Exception as exc:  # noqa: BLE001 -- the summary must still print
    record("XX", "the run reached its end without an unexpected exception", False,
           f"{exc.__class__.__name__}: {exc}")
    import traceback
    traceback.print_exc()
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 70)
print(f"EXAMINED: {len(results)} assertion(s)")
print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
if sum(results) < len(results):
    print(f"FAILED: {len(results) - sum(results)}")
print("=" * 70)
sys.exit(0 if results and all(results) else 1)
