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
                                          t)[0][0])
        and q("SELECT domain FROM terms WHERE term_id=?", t)[0][0] not in dbcore.NON_QUANTITY_DOMAINS]
    # T-020, T-083: a promotion names a quantity kind (derived) and where a source states a value of it, held on
    # the parameter's own row (OD-71; a fixture locator).
    KIND = q("SELECT kind_id FROM base_quantity_kinds ORDER BY kind_id LIMIT 1")[0][0]

    def promote(term_id):
        return attempt(db.insert_parameter, term_id, S, quantity_kind=KIND,
                       quantity_kind_source_url="https://example.org/task-fixture",
                       quantity_kind_source_page="TASK-FIXTURE")

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
        out = promote(tid)
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
    late = promote(FREE[6]).get("parameter_id")
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

    # rename-term. Every route names its judge (OD-38, T-028): the cases below give a fixture judge,
    # so each still reaches the refusal it is about; T028-07 calls the writer without one.
    _rename = fn("rename_term")

    def rename(*a, **k):
        return _rename(*a, **{"judge": "TASK-FIXTURE judge", **k})
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
    old_scope = q("SELECT scope_note FROM terms WHERE term_id=?", TR)[0][0]
    # OD-71: a pick rests on a form the base holds, so the observed phrase is recorded as TR's form first.
    attempt(fn("add_alias"), TR, OTZ, "SYNONYM", S)
    FTZ = q("SELECT form_id FROM term_aliases WHERE term_id=? AND alias='turnwise clearance zone'", TR)
    n7 = attempt(rename, TR, "turnwise clearance zone", "fixture: the sources' own phrase",
                 S, from_observation=OTZ)
    alias = q("SELECT alias_type, language, notes FROM term_aliases WHERE term_id=? AND "
              "alias=?", TR, old_name)
    trow = q("SELECT canonical_en, scope_note FROM terms WHERE term_id=?", TR)[0]
    pick7 = q("SELECT former_label, form_id, ref_id, ruling_quote, judge, reason FROM "
              "term_label_picks WHERE term_id=?", TR)
    # T-028: the label is not a form, so the former label is not written into term_aliases, and a
    # correction appended to a note is a fact in the wrong cell (2026-11-06): one pick row holds it.
    record("N07", "rename-term renames from the observation; the old label is NOT written as an alias, "
           "scope_note is unchanged, and one term_label_picks row holds the former label, the "
           "form holding the observed phrase, the source as provenance (ref_id), the judge and the reason",
           trow[0] == "turnwise clearance zone" and alias == [] and trow[1] == old_scope and FTZ
           and pick7 == [(old_name, FTZ[0][0], REF_A, None, "TASK-FIXTURE judge",
                          "fixture: the sources' own phrase")],
           f"{n7} {alias} {trow} {pick7}")
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
    p3 = promote(TD)
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
    # T074: an alias or a rename rests on the LATEST adjudication of its observation (adjudications
    # are appended, never edited: a later one that disagrees is the observation's standing judgment).
    if len(FREE) < 30:
        # A silent skip let the defect come back unseen (the critic of T-074 forced it): research drains FREE by
        # design (R16 promotes or declines every adjudicated term), so the case that says the fixture ran FAILS.
        record("T074-00", "T074 has its fixture: three free terms beyond FREE[27] (research drains them; widen the fixture, do not skip)",
               False, f"len(FREE)={len(FREE)}")
    else:
        record("T074-00", "T074 has its fixture: three free terms beyond FREE[27]", True)
        TX, TY, TZ = FREE[27:30]

        def t74_obs(loc):
            """A fresh observation of 'door leaf' on REF_A (its quote verifies against the fixture text)."""
            return attempt(observe, obs("door leaf", f"PDF page 1 / {loc}",
                                        "the clear width of a door leaf is measured here"),
                           S).get("observation_id")
        n74 = lambda: q("SELECT count(*) FROM term_aliases")[0][0]
        o1 = t74_obs("T074a")
        attempt(adj, o1, "NAMES-EXISTING", "fixture: names it", S, term_id=TX)
        attempt(adj, o1, "NOT-OURS", "fixture: on re-reading, not ours", S)
        a0 = n74()
        m1 = refusal(add_alias, TX, o1, "SYNONYM", S)
        record("T074-01", "add-alias: an observation judged NAMES-EXISTING and later NOT-OURS names "
               "no term: refused naming the latest adjudication, and no alias row lands",
               m1 and m1.startswith("add-alias:") and "latest adjudication of observation" in m1
               and n74() == a0, m1)
        # rename-term refuses a name another term answers to BEFORE it reads the adjudication, and AL04
        # has made 'door leaf' an alias: the rename case observes a phrase no term holds.
        PH2 = "clearance zone of a wheelchair"
        o2 = attempt(observe, obs(PH2, "PDF page 3 / T074d", "the turnwise clearance zone of a "
                                  "wheelchair"), S).get("observation_id")
        attempt(adj, o2, "NAMES-EXISTING", "fixture: names it", S, term_id=TX)
        attempt(adj, o2, "NOT-OURS", "fixture: on re-reading, not ours", S)
        name_x = q("SELECT canonical_en FROM terms WHERE term_id=?", TX)
        m2 = refusal(rename, TX, PH2, "fixture", S, from_observation=o2)
        record("T074-02", "rename-term: an observation judged NAMES-EXISTING and later NOT-OURS is "
               "refused with the latest adjudication, and the name does not move",
               m2 and m2.startswith("rename-term:") and "latest adjudication of observation" in m2
               and q("SELECT canonical_en FROM terms WHERE term_id=?", TX) == name_x, m2)
        o3 = t74_obs("T074b")
        attempt(adj, o3, "DEFERRED", "fixture: cannot settle on this source alone", S)
        attempt(adj, o3, "NAMES-EXISTING", "fixture: settled, names it", S, term_id=TY)
        w3 = attempt(add_alias, TY, o3, "SYNONYM", S)
        record("T074-03", "add-alias: DEFERRED and then NAMES-EXISTING (the live shape of observation "
               "88) is accepted: the latest adjudication names the term",
               q("SELECT observation_id FROM term_aliases WHERE term_id=? AND alias='door leaf'",
                 TY) == [(o3,)], w3)
        o4 = t74_obs("T074c")
        attempt(adj, o4, "NAMES-EXISTING", "fixture: names the first", S, term_id=TX)
        attempt(adj, o4, "NAMES-EXISTING", "fixture: re-pointed at the second", S, term_id=TZ)
        m4 = refusal(add_alias, TX, o4, "SYNONYM", S)
        w4 = attempt(add_alias, TZ, o4, "SYNONYM", S)
        record("T074-04", "add-alias: an observation re-pointed from one term to another is refused for "
               "the first term and accepted for the second",
               m4 and m4.startswith("add-alias:") and "latest adjudication of observation" in m4
               and q("SELECT observation_id FROM term_aliases WHERE term_id=? AND alias='door leaf'",
                     TX) == [] and q("SELECT observation_id FROM term_aliases WHERE term_id=? AND "
                                     "alias='door leaf'", TZ) == [(o4,)], (m4, w4))
    # T074-05..09 (the critic of T-074): the same rule on the other paths and orders.
    if len(FREE) >= 30:
        o5 = t74_obs("T074e")
        attempt(adj, o5, "NAMES-EXISTING", "fixture: names it", S, term_id=TX)
        attempt(adj, o5, "DEFERRED", "fixture: later, cannot settle", S)
        m5 = refusal(add_alias, TX, o5, "SYNONYM", S)
        record("T074-05", "add-alias: NAMES-EXISTING and then DEFERRED names nothing now: refused, and the message says the latest is DEFERRED",
               m5 and "is DEFERRED" in m5, m5)
        o6 = t74_obs("T074f")
        attempt(adj, o6, "NAMES-EXISTING", "fixture: names it", S, term_id=TY)
        attempt(adj, o6, "NOT-OURS", "fixture: dissent in ANOTHER session", S + "-dissent")
        m6 = refusal(add_alias, TY, o6, "SYNONYM", S)
        record("T074-06", "the latest adjudication is the highest id whatever the session: a dissent written by another session governs",
               m6 and "latest adjudication of observation" in m6 and "-dissent" in m6, m6)
        o7 = t74_obs("T074g")
        attempt(adj, o7, "NAMES-EXISTING", "fixture: names the first", S, term_id=TX)
        attempt(adj, o7, "NAMES-EXISTING", "fixture: re-pointed", S, term_id=TZ)
        name_x2 = q("SELECT canonical_en FROM terms WHERE term_id=?", TX)
        m7 = refusal(rename, TX, "clearance zone of a wheelchair seat", "fixture", S, from_observation=o7)
        record("T074-07", "rename-term: an observation re-pointed to another term is refused for the first term and names the term it now names",
               m7 and m7.startswith("rename-term:") and TZ in m7 and q("SELECT canonical_en FROM terms WHERE term_id=?", TX) == name_x2, m7)
        # the base route covers a form no observation covers: where one exists and its latest judgment rejects the term, refused
        _l2 = q("SELECT language FROM observed_terms WHERE observation_id=?", o2)[0][0]
        a8 = n74()
        m8 = refusal(add_alias, TX, None, "SYNONYM", S, alias=PH2, language=_l2, jurisdiction="CA",
                     source_url="https://example.org/doc", source_page="p. 1", attestation="other_source")
        record("T074-08", "add-alias BASE route: a form an observation records, whose latest judgment is NOT-OURS, is refused and names the observation",
               m8 and f"observation {o2}" in m8 and "base route is for a form no observation covers" in m8 and n74() == a8, m8)
        # an alias written under a standing judgment is seen when the judgment is overturned afterwards
        o9 = t74_obs("T074i")
        attempt(adj, o9, "NAMES-EXISTING", "fixture: names it", S, term_id=TX)
        attempt(add_alias, TX, o9, "SYNONYM", S)
        attempt(adj, o9, "NOT-OURS", "fixture: overturned later", S)
        import subprocess as _sp9
        _r9 = _sp9.run([sys.executable, str(REPO / "scripts/audit/alias_provenance_audit.py")],
                       env={**os.environ, "GUIDEBOOK_DB_PATH": DB}, capture_output=True, text=True)
        record("T074-09", "alias_provenance_audit flags an alias whose observation was re-judged NOT-OURS afterwards",
               _r9.returncode == 1 and "re-judged" in _r9.stdout and "no longer names" in _r9.stdout, (_r9.returncode, _r9.stdout[-300:]))
        x("DELETE FROM term_aliases WHERE observation_id=?", o9)       # fixture cleanup: later cases read the audit's verdict
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
    # T028-20 (OD-71): with no form of FREE[16] holding the observed phrase, the pick has no base warrant
    # and is refused, naming add-alias; once the phrase is recorded as its form, the rename is accepted.
    m20 = refusal(rename, FREE[16], "turnwise clearance", "fixture: native name", S,
                  from_observation=o_nl.get("observation_id"), dry_run=True)
    record("T028-20", "rename-term --from-observation is refused while the term holds no form of the observed "
           "phrase (a pick rests on a base form, OD-71), naming add-alias",
           m20 and "holds no form" in m20 and "add-alias --observation-id" in m20, m20)
    attempt(fn("add_alias"), FREE[16], o_nl.get("observation_id"), "SYNONYM", S)
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
                       "lens_basis": "named_in_text", "lens_basis_text": re.findall(r"\w+", text)[0],
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
        # The cell's lens: a figure reaches a cell only through the live lens links written on it (T-019).
        lens = {"identity_code": POP, "icf_code": None, "needs_code": None}
        refs = [s["ref_id"] for s in ac.gather_sources(con, PE, lens)]
        links = ac.gather_extraction_links(con, PE, [REF_A, REF_S], lens)
        by_id = {l["extraction_id"]: l for l in links}
        vmin, vmax, unit, note, _n = ac.compose_value(con, links, "lower_is_better")
        det = ac.determine(con, PE, lens, SLUG_A, "fixture")
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

        def near(name, language="EN"):
            c = sqlite3.connect(DB)
            try:
                return {t for t, _ in db._near_terms(c, name, language)}
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
        # stores the form's form_id (T-028: the declared key, which the capture path carries).
        rid = q("SELECT form_id FROM term_aliases WHERE term_id=? AND alias=?", T26[0], seed_a)
        LS = ["log-search", "--results-found", "1", "--prior-expectation", "fixture: nothing", "--slug", SLUG_A,
              "--language", "EN", "--query-text", "TASK-FIXTURE fixture query", "--engine", "web",
              "--depth-method", "scoping", "--session", S]
        r3 = run(*LS, *(["--form-id", str(rid[0][0])] if rid else []))
        e3 = json.loads(r3.stdout)["exec_id"] if r3.returncode == 0 and r3.stdout.strip() else None
        flagged = q("SELECT DISTINCT f.exec_id FROM search_execution_forms f JOIN term_aliases a "
                    "USING (form_id) WHERE a.attestation NOT IN ('instrument','other_source')")
        stored = q("SELECT form_id FROM search_execution_forms WHERE exec_id=?", e3)
        record("T026-03", "log-search --form-id writes a search_execution_forms row by the form's form_id, "
               "and the flag join (a seed's attestation) finds the search (AT-24 b)",
               e3 and rid and (e3,) in flagged and stored == [(rid[0][0],)],
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
        # (one row, type kept); an observation of an attested form is a further occurrence, a new
        # row, and never re-attests the held one (T-028's occurrence grain replaced T-026's refusal).
        aliasfn = fn("add_alias")
        base_kw = dict(language=LJ_EN[0], jurisdiction=LJ_EN[1], source_url="https://example.org/t26",
                       source_clause="2.3", attestation="instrument")
        b5 = attempt(aliasfn, T26[2], None, "SYNONYM", S, alias="corridor route", **base_kw)
        r5 = q("SELECT attestation, source_url, source_clause, jurisdiction, observation_id FROM "
               "term_aliases WHERE term_id=? AND alias='corridor route'", T26[2])
        seed_sql(T26[3], "swing leaf", "model_seed")
        n_t3 = q("SELECT COUNT(*) FROM term_aliases WHERE term_id=?", T26[3])[0][0]
        p5 = attempt(aliasfn, T26[3], None, "SYNONYM", S, alias="swing leaf", **base_kw)
        r5p = q("SELECT attestation, alias_type, source_clause FROM term_aliases WHERE term_id=? "
                "AND alias='swing leaf'", T26[3])
        o5 = attempt(observe, obs("corridor route", "PDF page 2 / T026",
                                  "the clear width of a corridor route is measured here"), S)
        attempt(adj, o5.get("observation_id"), "NAMES-EXISTING", "fixture", S, term_id=T26[2])
        d5 = attempt(aliasfn, T26[2], o5.get("observation_id"), "SYNONYM", S)
        record("T026-05", "add-alias base route writes the locator and attestation; it promotes a "
               "seed in place (one row, type kept); an observation of a held instrument form is a "
               "new occurrence row, and the instrument row is not re-attested (no downgrade)",
               r5 == [("instrument", "https://example.org/t26", "2.3", LJ_EN[1], None)]
               and p5.get("promoted") is True
               and r5p == [("instrument", "SYNONYM", "2.3")]
               and q("SELECT COUNT(*) FROM term_aliases WHERE term_id=?", T26[3])[0][0] == n_t3
               and d5.get("form_id") and not d5.get("promoted")
               and q("SELECT attestation, observation_id FROM term_aliases WHERE term_id=? AND "
                     "alias='corridor route' ORDER BY form_id", T26[2])
               == [("instrument", None), ("other_source", o5.get("observation_id"))], (b5, r5, p5, r5p, d5))

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

            # T026-10, as T-028 leaves it: an `unrecorded` alias is a seed, a search aid and never
            # vocabulary (E4), so it no longer screens a near name; the same row attested by a source
            # (typed other_source with a locator, by SQL on the copy, then put back) does.
            cands = q("SELECT term_id, alias FROM term_aliases WHERE upper(language)='EN' AND "
                      "attestation='unrecorded' AND created_by_session <> ? ORDER BY term_id, alias", T26S)
            pick = None
            for t_, a_ in cands:
                nm = f"{a_} {FIXW[6]}"
                if len(db._name_tokens(a_)) < 2 or t_ in near(nm):
                    continue                     # reached by its label or another form: not this probe
                x("UPDATE term_aliases SET attestation='other_source', source_url='https://example.org/"
                  "task-fixture', source_clause='TASK-FIXTURE' WHERE term_id=? AND alias=? AND "
                  "upper(language)='EN' AND attestation='unrecorded'", t_, a_)
                found = t_ in near(nm)
                x("UPDATE term_aliases SET attestation='unrecorded', source_url=NULL, source_clause=NULL "
                  "WHERE term_id=? AND alias=? AND source_clause='TASK-FIXTURE'", t_, a_)
                if found:
                    pick = (t_, a_, nm)
                    break
            record("T026-10", "_near_terms does not compare an `unrecorded` EN alias (a seed, E4; T-028) "
                   "and does compare the same row once a source attests it",
                   bool(pick) and pick[0] not in near(pick[2]), pick)

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
            rid_fr = q("SELECT form_id FROM term_aliases WHERE term_id=? AND alias='t26 forme'", T27[3])[0][0]
            rid_en = q("SELECT form_id FROM term_aliases WHERE term_id=? AND alias=?", T26[0], seed_a)[0][0]
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
                # the audit reads ZERO-result searches: --results-found 0 with its cause (R14), which the later flags override
                r = run(*LS, "--results-found", "0", "--absence-class", "genuine_absence", *extra)
                return json.loads(r.stdout)["exec_id"] if r.returncode == 0 else None
            e_none = exec_of()
            e_un = exec_of("--form-id", str(rid_en))
            e_att = exec_of("--form-id", str(q("SELECT form_id FROM term_aliases WHERE term_id=? AND alias=?",
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

            # T026-17 (finding 10), as T-028 leaves it: the junction points by form_id, so a corrected
            # spelling is still the form the search fired, and a vanished form is refused.
            fk = sqlite3.connect(DB)
            fk.execute("PRAGMA foreign_keys=ON")
            fid17 = rid_en
            try:
                try:
                    fk.execute("UPDATE term_aliases SET alias='t26 respelt' WHERE form_id=?", (fid17,))
                    moved = fk.execute("SELECT COUNT(*) FROM search_execution_forms f JOIN term_aliases a "
                                       "USING (form_id) WHERE a.form_id=? AND a.alias='t26 respelt'",
                                       (fid17,)).fetchone()[0]
                except sqlite3.IntegrityError:
                    moved = 0
                try:
                    fk.execute("DELETE FROM term_aliases WHERE form_id=?", (fid17,))
                    deleted = True
                except sqlite3.IntegrityError:
                    deleted = False
                fk.rollback()
            finally:
                fk.close()
            record("T026-17", "a corrected spelling of a searched form is still the form the search fired "
                   "(the junction points by form_id); a DELETE of it is refused", moved >= 1 and deleted is False,
                   (moved, deleted))

    # ── T028: a concept that is not an English string (AT-25). The concept is its id; its names are
    # forms, one row per occurrence; canonical_en is our English label; every label set by judgment
    # names its judge in term_label_picks (OD-38); a name is screened only within its own language
    # (OD-68). Probes are derived by query; names are fixture words no live name holds.
    T28S = "session_2026-11-18-t028-task-fixture"
    con = sqlite3.connect(DB)
    try:
        held28 = set()
        for (n_,) in con.execute("SELECT canonical_en FROM terms UNION ALL SELECT alias FROM term_aliases"):
            held28 |= db._name_tokens(n_)
        W = [w for w in ("taskfixturezel", "taskfixturekap", "taskfixturequil", "taskfixtureumb",
                         "taskfixturepas", "taskfixturecle", "taskfixturemor", "taskfixturesed",
                         "taskfixturebri", "taskfixturevan") if w not in held28]
        NONEN = con.execute("SELECT language, jurisdiction FROM lang_jur_map WHERE upper(language) <> 'EN' "
                            "ORDER BY language, jurisdiction LIMIT 1").fetchone()
        TWOJ = con.execute("SELECT language, MIN(jurisdiction), MAX(jurisdiction) FROM lang_jur_map "
                           "GROUP BY language HAVING COUNT(*) > 1 ORDER BY language LIMIT 1").fetchone()
        ENSC = con.execute("SELECT r.jurisdiction FROM v_research_scope r JOIN lang_jur_map m ON "
                           "upper(m.language) = upper(r.language) AND m.jurisdiction = r.jurisdiction "
                           "WHERE upper(r.language) = 'EN' ORDER BY 1 LIMIT 1").fetchone()
        LAB28 = next(((t, n) for t, n in con.execute("SELECT term_id, canonical_en FROM terms ORDER BY term_id")
                      if len(db._name_tokens(n)) >= 2), None)
        USAGE = sorted(dbcore.check_values(con, "term_aliases", "usage_type") or [])
        EN28 = db._alias_language(con, "EN")
    finally:
        con.close()
    if len(W) < 10 or not (NONEN and TWOJ and ENSC and LAB28):
        print("      SKIPPED-NO-FIXTURE: T028 needs 10 unheld words, a non-EN pair, a language with two "
              "jurisdictions, an EN jurisdiction in research scope and a two-token label")
    else:
        LOC = ["--source-url", "https://example.org/task-fixture-t028", "--source-clause", "TASK-FIXTURE 1.1"]
        LOCK = dict(source_url="https://example.org/task-fixture-t028", source_clause="TASK-FIXTURE 1.1")
        JUDGE = "TASK-FIXTURE judge"
        aliasfn28 = fn("add_alias")

        def forms_of(term):
            return q("SELECT form_id, alias, upper(language), jurisdiction, attestation, observation_id "
                     "FROM term_aliases WHERE term_id=? ORDER BY form_id", term)

        def picks_of(term):
            return q("SELECT former_label, form_id, ref_id, ruling_quote, judge, reason "
                     "FROM term_label_picks WHERE term_id=? ORDER BY pick_id", term)

        def names(term):
            r = q("SELECT label_is_attested_form, display_basis, display_name FROM v_term_names "
                  "WHERE term_id=?", term)
            return r[0] if r else None

        # T028-01 (AT-25): a concept whose first and only attested form is not English, with an English
        # label marked as ours and not counted as an attested English form.
        F1, L1 = f"{W[0]} {W[1]}weg", f"{W[2]} {W[3]} label"
        n_terms = q("SELECT COUNT(*) FROM terms")[0][0]
        r1 = run("add-term", "--first-form", F1, "--form-language", NONEN[0], "--form-jurisdiction", NONEN[1],
                 *LOC, "--attestation", "instrument", "--canonical-en", L1, "--judge", JUDGE,
                 "--rationale", "TASK-FIXTURE: a concept first met in another language", "--session", T28S)
        TA28 = json.loads(r1.stdout).get("term_id") if r1.returncode == 0 and r1.stdout.strip() else None
        f1 = forms_of(TA28)
        record("T028-01", "add-term --first-form mints a concept from a non-English instrument form with an "
               "English label: one term, one member row in that language, one pick row (former_label NULL), "
               "label_is_attested_form 0, display_basis origin_instrument_form, no attested EN form",
               TA28 and q("SELECT COUNT(*) FROM terms")[0][0] == n_terms + 1
               and len(f1) == 1 and f1[0][1:5] == (F1, NONEN[0].upper(), NONEN[1], "instrument")
               and picks_of(TA28) == [(None, f1[0][0], None, None, JUDGE,
                                       "TASK-FIXTURE: a concept first met in another language")]
               and names(TA28) == (0, "origin_instrument_form", F1)
               and not [f for f in f1 if f[2] == "EN" and f[4] in dbcore.ATTESTED_FORMS],
               (r1.returncode, r1.stdout[-300:], r1.stderr[-400:], f1, TA28 and names(TA28)))

        # T028-02 (C-04): add-term --from-observation on a non-English observation, with an English label
        # that is not inside the phrase: accepted, the phrase is the first member row, no pick row.
        o28 = attempt(observe, obs("turnwise clearance zone", "PDF page 3 / T028-02",
                                   "the turnwise clearance zone of a wheelchair", language=NONEN[0]), S)
        L2 = f"{W[4]} {W[5]} label"
        t2 = attempt(ins, o28.get("observation_id"), L2, "TASK-FIXTURE: a concept first met in another language",
                     T28S)
        TB28 = t2.get("term_id")
        f2 = forms_of(TB28)
        record("T028-02", "add-term --from-observation takes an English label not inside a non-English phrase; "
               "the phrase is the first member row (other_source, the observation), and no pick row is written",
               TB28 and f2 == [(f2[0][0], "turnwise clearance zone", NONEN[0].upper(), f2[0][3], "other_source",
                                o28.get("observation_id"))] and picks_of(TB28) == []
               and q("SELECT outcome FROM term_adjudications WHERE observation_id=? AND term_id=?",
                     o28.get("observation_id"), TB28) == [("NAMES-NEW",)], (t2, f2))

        # T028-03: one form attested in two jurisdictions for one term is two occurrences, two form_ids.
        F3 = f"{W[6]} {W[7]}"
        a3 = [attempt(aliasfn28, TA28, None, "SYNONYM", T28S, alias=F3, language=TWOJ[0], jurisdiction=j,
                      attestation="other_source", **LOCK) for j in (TWOJ[1], TWOJ[2])]
        r3 = q("SELECT form_id, jurisdiction FROM term_aliases WHERE term_id=? AND alias=? ORDER BY form_id", TA28, F3)
        record("T028-03", "the same form attested in two jurisdictions for one term is two rows with two form_ids",
               len(r3) == 2 and r3[0][0] != r3[1][0] and {r3[0][1], r3[1][1]} == {TWOJ[1], TWOJ[2]}, (a3, r3))

        # T028-04: rename-term --from-form picks an attested English instrument form of an owed English
        # jurisdiction as the label: display_basis english_instrument_label; no alias row; scope_note unchanged.
        F4 = f"{W[8]} {W[0]}"
        w4 = attempt(aliasfn28, TA28, None, "SYNONYM", T28S, alias=F4, language="EN", jurisdiction=ENSC[0],
                     attestation="instrument", **LOCK)
        fid4 = w4.get("form_id")
        n_forms4, scope4 = len(forms_of(TA28)), (q("SELECT scope_note FROM terms WHERE term_id=?", TA28) or [(None,)])[0][0]
        b4 = names(TA28)
        p4 = attempt(_rename, TA28, F4, "TASK-FIXTURE: the instrument's own term", T28S, from_form=fid4, judge=JUDGE)
        record("T028-04", "rename-term --from-form sets the label to an attested English instrument form: "
               "display_basis english_instrument_label, no alias row written, scope_note unchanged, the pick recorded",
               b4 == (0, "english_instrument_form", F4) and names(TA28) == (1, "english_instrument_label", F4)
               and len(forms_of(TA28)) == n_forms4
               and q("SELECT canonical_en, scope_note FROM terms WHERE term_id=?", TA28) == [(F4, scope4)]
               and picks_of(TA28)[-1] == (L1, fid4, None, None, JUDGE, "TASK-FIXTURE: the instrument's own term"),
               (w4, b4, p4, names(TA28), picks_of(TA28)))

        # T028-05 (AT-24 for names): a model_seed row whose text equals a new name does not clash; it is
        # reported in seed_matches.
        S5 = f"{W[9]} {W[1]}"
        x("INSERT INTO term_aliases (term_id, alias, language, alias_type, notes, created_at, created_by_session, "
          "updated_at, updated_by_session, attestation) VALUES (?, ?, ?, 'SYNONYM', 'model-generated TASK-FIXTURE', "
          "'t', ?, 't', ?, 'model_seed')", TB28, S5, EN28, T28S, T28S)
        c5 = sqlite3.connect(DB)
        try:
            h5 = attempt(db._name_holder, c5, S5, "EN")
        finally:
            c5.close()
        record("T028-05", "_name_holder: a model_seed row with the same text is no clash, and is reported "
               "in seed_matches", isinstance(h5, dict) and h5.get("clashes") == []
               and [m["term_id"] for m in h5.get("seed_matches", [])] == [TB28], h5)

        # T028-06: _near_terms on a non-English name does not return English labels (the control: the
        # same name in EN does).
        nm6 = f"{LAB28[1]} {W[9]}"
        c6 = sqlite3.connect(DB)
        try:
            n6 = [attempt(lambda nm, l: {t for t, _ in db._near_terms(c6, nm, l)}, nm6, lang) for lang in (NONEN[0], "EN")]
            n6 += [attempt(lambda nm, l: {t for t, _ in db._near_terms(c6, nm, l)}, f"{F1} {W[9]}", NONEN[0])]
        finally:
            c6.close()
        record("T028-06", "_near_terms on a non-English name compares no English label (the same name in EN does) "
               "and finds a term through an attested form of its own language",
               isinstance(n6[0], set) and LAB28[0] not in n6[0] and LAB28[0] in n6[1]
               and isinstance(n6[2], set) and TA28 in n6[2], (LAB28, n6))

        # T028-07 (OD-38): every rename-term route without --judge is refused; with it, each writes one pick
        # row holding the former label and the route's one pointer, and no AMENDED trailer.
        F7 = f"{W[7]} {W[3]}"
        fid7 = attempt(aliasfn28, TA28, None, "SYNONYM", T28S, alias=F7, language="EN", jurisdiction=ENSC[0],
                       attestation="other_source", **LOCK).get("form_id")
        words7 = [w.lower() for w in (QUOTE or "").split() if w.isalpha() and len(w) > 4]
        RN7 = next((f"{a} {b}" for a, b in zip(words7, words7[1:])
                    if f"{a} {b}" in (QUOTE or "").lower() and f"{a} {b}" != RNAME
                    and not db._VALUE_BEARING.search(f"{a} {b}")
                    and not q("SELECT 1 FROM terms WHERE lower(canonical_en)=?", f"{a} {b}")
                    and not q("SELECT 1 FROM term_aliases WHERE lower(alias)=?", f"{a} {b}")), None)
        f28 = q("SELECT form_id FROM term_aliases WHERE term_id=? AND alias='turnwise clearance zone'", TB28)
        routes7 = [(TA28, F7, dict(from_form=fid7), "form_id", fid7, None),
                   (TB28, "turnwise clearance", dict(from_observation=o28.get("observation_id")),
                    "form_id", f28[0][0] if f28 else -1, REF_A),
                   (TA28, RN7, dict(ruling_quote=QUOTE), "ruling_quote", (QUOTE or "").strip(), None)]
        ok7 = bool(RN7 and fid7)
        for term7, new7, kw7, col7, val7, ref7 in routes7:
            m7 = refusal(_rename, term7, new7, "TASK-FIXTURE: picked", T28S, **kw7)
            old7, scope7 = (q("SELECT canonical_en, scope_note FROM terms WHERE term_id=?", term7) or [(None, None)])[0]
            n7p = len(picks_of(term7))
            w7 = attempt(_rename, term7, new7, "TASK-FIXTURE: picked", T28S, judge=JUDGE, **kw7)
            last = q(f"SELECT former_label, {col7}, judge, (form_id IS NOT NULL) + (ruling_quote IS NOT NULL), "
                     f"ref_id FROM term_label_picks WHERE term_id=? ORDER BY pick_id DESC LIMIT 1", term7)
            ok7 = ok7 and bool(m7 and "--judge" in m7) and len(picks_of(term7)) == n7p + 1 \
                and last == [(old7, val7, JUDGE, 1, ref7)] \
                and q("SELECT canonical_en, scope_note FROM terms WHERE term_id=?", term7) == [(new7, scope7)]
            if not ok7:
                print(f"      T028-07 route {col7}: {m7!r} {w7} {last}")
        record("T028-07", "rename-term refuses each route (form, observation, ruling) without --judge; with it each "
               "writes one term_label_picks row (former label, the one base warrant: the form or the quote, the "
               "judge, the source as provenance on the observation route) and no AMENDED trailer",
               ok7, (RN7, fid7))

        # T028-08: DOMAIN is refused naming --usage-type; a usage outside the column's CHECK is refused; one
        # inside it is written.
        F8 = f"{W[5]} {W[8]}"
        base8 = dict(alias=F8, language="EN", jurisdiction=ENSC[0], attestation="other_source", **LOCK)
        m8a = refusal(aliasfn28, TB28, None, "DOMAIN", T28S, **base8)
        m8b = refusal(aliasfn28, TB28, None, "SYNONYM", T28S, usage_type="taskfixture_usage", **base8)
        U8 = USAGE[0] if USAGE else None          # the column's CHECK; none on a schema without T-028: red below
        w8 = attempt(aliasfn28, TB28, None, "SYNONYM", T28S, usage_type=U8, **base8)
        record("T028-08", "add-alias refuses DOMAIN naming --usage-type, refuses a usage outside the column's "
               "CHECK, and writes one inside it",
               m8a and "--usage-type" in m8a and m8b and "usage_type" in m8b
               and U8 and q("SELECT usage_type FROM term_aliases WHERE term_id=? AND alias=?", TB28, F8) == [(U8,)],
               (m8a, m8b, w8))

        # T028-09 (guard, and OD-68): a name equal to another term's attested form in the SAME language is
        # refused by rename-term and by add-term --first-form unless --distinct-from names the term; the same
        # written word in ANOTHER language is another name (owner, 2026-11-17) and is not refused.
        m9a = refusal(_rename, TB28, F7, "TASK-FIXTURE", T28S, from_observation=o28.get("observation_id"),
                      judge=JUDGE)
        kw9 = dict(first_form=F7, form_language="EN", form_jurisdiction=ENSC[0], attestation="other_source",
                   judge=JUDGE, dry_run=True, **LOCK)
        m9b = refusal(ins, None, F7, "TASK-FIXTURE: a distinct concept", T28S, **kw9)
        w9c = attempt(ins, None, F7, "TASK-FIXTURE: a distinct concept", T28S, distinct_from=[TA28], **kw9)
        w9d = attempt(ins, None, f"{W[6]} {W[2]} label", "TASK-FIXTURE: another language", T28S,
                      **{**kw9, "form_language": NONEN[0], "form_jurisdiction": NONEN[1]})
        record("T028-09", "an attested same-language form of another term refuses rename-term and add-term "
               "--first-form (unless --distinct-from names it); the same word in another language does not",
               m9a and TA28 in m9a and m9b and TA28 in m9b and w9c.get("term_id") and w9d.get("term_id"),
               (m9a, m9b, w9c, w9d))

        # T028-10: an observation whose quote is in no file saved for its source and is not VERBATIM-EXEMPT
        # still mints the term; its member row is unrecorded, with the observation, and the output says so.
        # Fixture by SQL: observe-term refuses such a quote, and the corpus rows that carry one name live terms.
        F10 = f"{W[4]} {W[9]}"
        o10 = x("INSERT INTO observed_terms (ref_id, surface_form, language, locator, context_quote, created_at, "
                "created_by_session) VALUES (?, ?, 'EN', 'TASK-FIXTURE', ?, 't', ?)", REF_A, F10,
                f"a TASK-FIXTURE sentence using {F10} once, in no saved file", T28S)
        t10 = attempt(ins, o10, F10, "TASK-FIXTURE: the quote is not verified", T28S)
        J10 = q("SELECT jurisdiction FROM evidence_sources WHERE ref_id=?", REF_A)[0][0]
        f10 = forms_of(t10.get("term_id"))
        record("T028-10", "add-term --from-observation with an unverified quote mints the term, writes its form "
               "unrecorded with the observation, and says add-alias promotes it",
               t10.get("term_id") and [f[1:] for f in f10] == [(F10, "EN", J10, "unrecorded", o10)]
               and "add-alias" in (t10.get("form_unrecorded") or ""), (t10, f10))
        # T028-10b: once the quote is verified (here: the observation recorded VERBATIM-EXEMPT, by SQL on the
        # copy), add-alias promotes that unrecorded member row in place; no second row.
        x("UPDATE observed_terms SET notes=? WHERE observation_id=?", f"{retrieval_log.EXEMPT_MARK} TASK-FIXTURE]", o10)
        p10 = attempt(aliasfn28, t10.get("term_id"), o10, "SYNONYM", T28S)
        record("T028-10b", "add-alias --observation-id promotes add-term's unrecorded first form in place once "
               "the quote is verified: one row, now other_source",
               p10.get("promoted") is True
               and [f[4:] for f in forms_of(t10.get("term_id"))] == [("other_source", o10)], (p10,))

        # T028-11: add-term's own refusals, each in words, none writing a term.
        n11 = q("SELECT COUNT(*) FROM terms")[0][0]
        NOPAIR = q("SELECT a.language, b.jurisdiction FROM (SELECT DISTINCT language FROM lang_jur_map) a, "
                   "(SELECT DISTINCT jurisdiction FROM lang_jur_map) b WHERE NOT EXISTS (SELECT 1 FROM lang_jur_map "
                   "m WHERE m.language = a.language AND m.jurisdiction = b.jurisdiction) ORDER BY 1, 2 LIMIT 1")
        L11, F11 = f"{W[1]} {W[2]}", f"{W[1]} {W[2]} {W[3]}"
        b11 = dict(first_form=F11, form_language="EN", form_jurisdiction=ENSC[0], attestation="other_source",
                   judge=JUDGE, **LOCK)
        c11 = [(refusal(ins, None, L11, "r", T28S), "exactly one route"),
               (refusal(ins, o28.get("observation_id"), L11, "r", T28S, **b11), "exactly one route"),
               (refusal(ins, o28.get("observation_id"), L11, "r", T28S, judge=JUDGE), "belong to --first-form"),
               (refusal(ins, None, L11, "r", T28S, **{**b11, "judge": None}), "--judge"),
               (refusal(ins, None, f"{W[4]} {W[6]}", "r", T28S, **b11), "not inside the English first form"),
               (refusal(ins, None, L11, "r", T28S, **{**b11, "source_clause": None}), "--source-page or --source-clause"),
               (refusal(ins, None, L11, "r", T28S, **{**b11, "attestation": "model_seed"}), "other_source"),
               (refusal(ins, None, L11, "r", T28S, **{**b11, "form_language": NOPAIR[0][0] if NOPAIR else None,
                                                      "form_jurisdiction": NOPAIR[0][1] if NOPAIR else None}),
                "lang_jur_map holds no pair"),
               (refusal(ins, None, L11, "r", T28S, **{**b11, "usage_type": "taskfixture_usage"}), "usage_type")]
        record("T028-11", "add-term refuses no route, two routes, a base flag on the observation route, a first form "
               "with no judge, an English first form not holding the label, no page or clause, a seed attestation, "
               "an unpaired language and a usage outside the CHECK; each in words, no term written",
               NOPAIR and all(m and w in m for m, w in c11) and q("SELECT COUNT(*) FROM terms")[0][0] == n11,
               [m for m, w in c11 if not (m and w in m)])

        # T028-12: rename-term --from-form refuses a form of another term, an unattested form of this term, and
        # an attested form whose text is not the new label.
        seed12 = q("SELECT form_id, alias FROM term_aliases WHERE term_id=? AND attestation='model_seed'", TB28)
        other12 = q("SELECT form_id, alias FROM term_aliases WHERE term_id=? AND attestation IN "
                    "('instrument','other_source') ORDER BY form_id LIMIT 1", TA28)
        mine12 = q("SELECT form_id, alias FROM term_aliases WHERE term_id=? AND alias=?", TB28, F8)
        c12 = [refusal(_rename, TB28, other12[0][1], "r", T28S, from_form=other12[0][0], judge=JUDGE)
               if other12 else None,
               refusal(_rename, TB28, seed12[0][1], "r", T28S, from_form=seed12[0][0], judge=JUDGE)
               if seed12 else None,
               refusal(_rename, TB28, f"{W[8]} {W[9]}", "r", T28S, from_form=mine12[0][0], judge=JUDGE)
               if mine12 else None]
        record("T028-12", "rename-term --from-form refuses another term's form and an unattested form (not an "
               "attested member form) and a form whose text is not the new label",
               c12[0] and "not an attested member form" in c12[0] and c12[1] and "not an attested member form"
               in c12[1] and c12[2] and "that form's text" in c12[2], c12)

        # T028-13 (OD-68, _name_holder): a name is compared with labels only when it is English, and with
        # attested forms only of its own language: the same word in another language is no clash.
        c13 = sqlite3.connect(DB)
        try:
            h13 = [db._name_holder(c13, n, l)["clashes"] for n, l in
                   ((LAB28[1], NONEN[0]), (LAB28[1], "EN"), (F7, NONEN[0]), (F7, "EN"))]
        finally:
            c13.close()
        record("T028-13", "_name_holder: a label is no clash for a non-English name and is one for the English "
               "name; an attested English form is no clash in another language and is one in English",
               h13[0] == [] and [c["term_id"] for c in h13[1] if c["kind"] == "label"] == [LAB28[0]]
               and h13[2] == [] and [c["term_id"] for c in h13[3]] == [TA28], h13)

        # T028-14 (OD-68, _near_terms through a writer): add-term --first-form with a name near another term's
        # attested English form is accepted in another language and refused in English.
        N14 = f"{F7} {W[9]}"
        k14 = dict(first_form=N14, attestation="other_source", judge=JUDGE, dry_run=True, **LOCK)
        w14 = attempt(ins, None, f"{W[2]} {W[8]} label", "TASK-FIXTURE: another language", T28S,
                      form_language=NONEN[0], form_jurisdiction=NONEN[1], **k14)
        m14 = refusal(ins, None, N14, "TASK-FIXTURE: English", T28S, form_language="EN",
                      form_jurisdiction=ENSC[0], **k14)
        record("T028-14", "add-term --first-form: a name near an attested English form of another term is accepted "
               "in another language (two independent names) and refused in English (a near match)",
               w14.get("term_id") and m14 and "near match" in m14 and TA28 in m14, (w14, m14))

        # T028-15: add-term --first-form refuses a phrase whose observation is judged NOT-OURS, as the base route
        # of add-alias does (one helper for both).
        P15 = "corridor route is measured"
        o15 = attempt(observe, obs(P15, "PDF page 2 / T028-15",
                                   "the clear width of a corridor route is measured here"), S).get("observation_id")
        attempt(adj, o15, "NOT-OURS", "TASK-FIXTURE: not a concept of ours", S)
        n15 = q("SELECT COUNT(*) FROM terms")[0][0]
        m15 = [refusal(ins, None, P15, "TASK-FIXTURE", T28S, first_form=P15, form_language="EN",
                       form_jurisdiction=ENSC[0], attestation="other_source", judge=JUDGE, **LOCK),
               refusal(aliasfn28, TA28, None, "SYNONYM", T28S, alias=P15, language="EN", jurisdiction=ENSC[0],
                       attestation="other_source", **LOCK)]
        record("T028-15", "add-term --first-form and add-alias's base route both refuse a phrase whose observation's "
               "standing judgment names no term, naming the observation; no term is written",
               all(m and f"observation {o15}" in m and "base route is for a form no observation covers" in m
                   for m in m15) and q("SELECT COUNT(*) FROM terms")[0][0] == n15, m15)

        # T028-16: rename-term --from-form refuses a form whose language is not the English label's.
        fid16 = q("SELECT form_id FROM term_aliases WHERE term_id=? AND alias=?", TA28, F1)
        m16 = refusal(_rename, TA28, F1, "TASK-FIXTURE", T28S, from_form=fid16[0][0] if fid16 else -1, judge=JUDGE)
        record("T028-16", "rename-term --from-form refuses a non-English form as the English label, naming the "
               "next action", m16 and "English label" in m16 and "add-alias" in m16, m16)

        # T028-17: rename-term --from-form refuses an attested NARROWER form: a related search string is not a
        # name of the concept (the member rule, read from v_term_names).
        F17 = f"{W[3]} {W[5]}"
        w17 = attempt(aliasfn28, TA28, None, "NARROWER", T28S, alias=F17, language="EN", jurisdiction=ENSC[0],
                      attestation="other_source", **LOCK)
        m17 = refusal(_rename, TA28, F17, "TASK-FIXTURE", T28S, from_form=w17.get("form_id", -1), judge=JUDGE)
        record("T028-17", "rename-term --from-form refuses an attested NARROWER form (not a member form)",
               w17.get("form_id") and m17 and "not an attested member form" in m17, (w17, m17))

        # T028-18: alias_provenance_audit is NOT RUN (exit 2, no EXAMINED line, the cause named) when the
        # zero-result search read cannot run; it never reports an empty subject. Fixture: a copy whose junction
        # lacks form_id (SQL on a second copy).
        DB18 = os.path.join(TMP, "t028-18.db")
        shutil.copy(DB, DB18)
        c18 = sqlite3.connect(DB18)
        c18.execute("ALTER TABLE search_execution_forms RENAME COLUMN form_id TO taskfixture_fid")
        c18.commit()
        c18.close()
        a18 = subprocess.run([sys.executable, str(REPO / "scripts" / "audit" / "alias_provenance_audit.py")],
                             env={**ENV, "GUIDEBOOK_DB_PATH": DB18}, capture_output=True, text=True)
        record("T028-18", "alias_provenance_audit exits 2 NOT RUN, with no EXAMINED line and the cause named, when "
               "the zero-result search read cannot run",
               a18.returncode == 2 and "NOT RUN" in a18.stdout and "EXAMINED" not in a18.stdout
               and "form_id" in a18.stdout, (a18.returncode, a18.stdout[-300:]))

        # T028-19 (E4; task file section 4 item 2): every writer whose name screen ran reports the seeds that
        # hold the name, as information that refuses nothing: add-term on both routes, add-alias, rename-term,
        # mint-term-from-catalogue.
        P19 = "measured here"
        x("INSERT INTO term_aliases (term_id, alias, language, alias_type, notes, created_at, "
          "created_by_session, updated_at, updated_by_session, attestation) VALUES (?, ?, ?, 'SYNONYM', "
          "'model-generated TASK-FIXTURE', 't', ?, 't', ?, 'model_seed')", TB28, P19, EN28, T28S, T28S)
        o19 = attempt(observe, obs(P19, "PDF page 1 / T028-19",
                                   "the clear width of a door leaf is measured here"), S).get("observation_id")
        out19 = {
            "add-term --from-observation": attempt(ins, o19, P19, "TASK-FIXTURE", T28S, dry_run=True),
            "add-term --first-form": attempt(ins, None, S5, "TASK-FIXTURE", T28S, first_form=S5, form_language="EN",
                                             form_jurisdiction=ENSC[0], attestation="other_source", judge=JUDGE,
                                             dry_run=True, **LOCK),
            "mint-term-from-catalogue": attempt(mint, **mt(canonical_en=S5), dry_run=True),
            "add-alias": attempt(aliasfn28, TA28, None, "SYNONYM", T28S, alias=S5, language="EN",
                                 jurisdiction=ENSC[0], attestation="other_source", **LOCK)}
        out19["rename-term"] = attempt(_rename, TA28, S5, "TASK-FIXTURE: seed report", T28S,
                                       from_form=out19["add-alias"].get("form_id", -1), judge=JUDGE)
        bad19 = {k: v for k, v in out19.items() if [m.get("term_id") for m in v.get("seed_matches") or []] != [TB28]}
        record("T028-19", "add-term (both routes), add-alias, rename-term and mint-term-from-catalogue each report "
               "the seed holding the name in seed_matches and write or accept as before", not bad19, bad19)

        # T028-21 (OD-71): base tables are derived from the stage map; a base table holds no foreign key into
        # another stage other than a nullable provenance ref_id. Asserted for the table this task owns,
        # term_label_picks; the other base tables' foreign keys into evidence and judgment are listed, not
        # failed here (term_aliases.observation_id waits on the owner's answer on an absorbed observation's
        # attestation; term_relations, T-029's, is asserted since migration 151; base_parameters' are T-020's and the 2026-10-30 ruling's).
        import yaml as _yaml
        SM = _yaml.safe_load((REPO / "governance" / "stage-map.yaml").read_text(encoding="utf-8"))["tables"]
        c21 = sqlite3.connect(DB)
        try:
            v21 = []
            for t21 in sorted(t for t, st in SM.items() if st == "base"):
                cols = {r[1]: r[3] for r in c21.execute(f'PRAGMA table_info("{t21}")')}
                for f in c21.execute(f'PRAGMA foreign_key_list("{t21}")'):
                    if SM.get(f[2]) != "base" and not (f[3] == "ref_id" and not cols.get(f[3])):
                        v21.append((t21, f[3], f[2], SM.get(f[2])))
        finally:
            c21.close()
        others21 = [v for v in v21 if v[0] not in ("term_label_picks", "term_relations")]
        if others21:
            print(f"      REPORTED (other base tables, not this task's): {others21}")
        record("T028-21", "term_label_picks and term_relations, base tables by the stage map, hold no foreign key into "
               "another stage; each ref_id is a plain provenance cell",
               SM.get("term_label_picks") == "base" and SM.get("term_relations") == "base"
               and not [v for v in v21 if v[0] in ("term_label_picks", "term_relations")]
               and "ref_id" in [r[1] for r in q("PRAGMA table_info(term_relations)")]
               and "ref_id" in [r[1] for r in q("PRAGMA table_info(term_label_picks)")], v21)


    # ── T029: typed pointers from one term to another, grounded in the base's own cells (AT-67; migrations 147,
    # 148, 151; OD-71). Probes are derived by query; every fixture is labelled TASK-FIXTURE and lives on the copy.
    T29S = "session_2026-11-18-t029-task-fixture"
    con = sqlite3.connect(DB)
    try:
        nonparam29 = [t for (t,) in con.execute("SELECT term_id FROM terms WHERE term_id NOT IN "
                                                "(SELECT term_id FROM base_parameters) ORDER BY term_id")]
        PARAM29 = con.execute("SELECT term_id, parameter_id FROM base_parameters WHERE status = 'active' "
                              "ORDER BY parameter_id LIMIT 1").fetchone()
        KINDS29 = sorted(dbcore.check_values(con, "term_relations", "kind") or [])
    except sqlite3.OperationalError as exc:
        if not _absent_schema(exc):
            raise
        nonparam29, PARAM29, KINDS29 = [], None, []
    finally:
        con.close()
    if len(nonparam29) < 3 or not PARAM29:
        print("      SKIPPED-NO-FIXTURE: T029 needs three terms that are not parameters and an active parameter")
        record("T029-00", "the T029 fixtures exist (three non-parameter terms, an active parameter)",
               False, (len(nonparam29), PARAM29))
    else:
        E29, P29, O29 = nonparam29[:3]
        PT29, PID29 = PARAM29
        K_PROV, K_PAR = "element has provision", "element has parameter"
        URL29 = "https://example.org/task-fixture-t029"
        LOC29 = dict(source_url=URL29, source_page="3", source_line=12)      # where a source says so
        LOC29B = dict(source_url=URL29, source_clause="TASK-FIXTURE 4.1")
        addrel = fn("add_term_relation")
        retrel = fn("retire_term_relation")
        elemread = fn("element_parameters")

        def rels(sql="", *a):
            return q("SELECT relation_id, from_term_id, kind, to_term_id, reason, source_url, source_page, "
                     "source_line, source_clause, ref_id, created_by_session, retired_at FROM term_relations "
                     + sql, *a)

        # T029-01 (AT-67, OD-56): a row of kind `element has provision` between two held terms, with where a source
        # says so, is accepted and the reader prints it among the element's provisions (and not among its
        # parameters), with the locator it was grounded in.
        a1 = attempt(addrel, E29, K_PROV, P29, "TASK-FIXTURE: the element should carry the provision", T29S, **LOC29)
        r1 = attempt(elemread, E29)
        pv1 = (r1.get("provisions") or [{}])[0]
        record("T029-01", "an `element has provision` row between two held terms, grounded in a locator, is "
               "accepted and printed by element-parameters among the provisions with its locator and reason",
               a1.get("relation_id") and [p["term_id"] for p in r1.get("provisions", [])] == [P29]
               and r1.get("parameters") == []
               and (pv1.get("source_url"), pv1.get("source_page"), pv1.get("source_line"),
                    pv1.get("source_clause")) == (URL29, "3", 12, None)
               and pv1.get("reason") == "TASK-FIXTURE: the element should carry the provision"
               and pv1.get("created_by_session") == T29S, (a1, r1))

        # T029-02 (AT-67): a kind outside the CHECK is refused, naming the CHECK's own set; nothing is written.
        n02 = len(rels())
        e2 = refusal(addrel, E29, "equivalent", O29, "TASK-FIXTURE", T29S, **LOC29)
        record("T029-02", "a kind outside the column's CHECK (`equivalent`) is refused, naming the CHECK's set, and "
               "nothing is written; the set is the column's own and holds `distinct`",
               e2 and all(k in e2 for k in KINDS29) and "equivalent" not in KINDS29 and "distinct" in KINDS29
               and len(rels()) == n02, (e2, KINDS29))

        # T029-03: `element has parameter` reads the parameter of the term it points at by looking it up.
        a3 = attempt(addrel, E29, K_PAR, PT29, "TASK-FIXTURE: the element's dimension", T29S, **LOC29B)
        r3 = attempt(elemread, E29)
        pr3 = r3.get("parameters", [])
        record("T029-03", "an `element has parameter` row is printed among the parameters with the parameter the "
               "term carries (looked up, not copied) and its clause locator; a provision that carries no "
               "parameter prints none",
               a3.get("relation_id") and len(pr3) == 1 and pr3[0]["term_id"] == PT29
               and pr3[0]["parameter_id"] == PID29 and pr3[0]["source_clause"] == "TASK-FIXTURE 4.1"
               and [p["parameter_id"] for p in r3["provisions"]] == [None], (a3, r3))

        # T029-04 (amendment 1): `distinct` is stored with the lower term id first whichever way the pair is named,
        # rests on its reason alone, and a second live row for the pair is refused naming the held row.
        lo, hi = sorted((P29, O29))
        a4 = attempt(addrel, hi, "distinct", lo, "TASK-FIXTURE: two concepts", T29S)
        e4a = refusal(addrel, lo, "distinct", hi, "TASK-FIXTURE: again", T29S)
        e4b = refusal(addrel, hi, "distinct", lo, "TASK-FIXTURE: again", T29S)
        r4 = rels("WHERE kind = 'distinct'")
        record("T029-04", "a `distinct` row, justified by its reason alone, is stored lower id first whichever way "
               "it is named; a second live row of the pair, either way round, is refused naming the held relation "
               "and retire-term-relation",
               a4.get("relation_id") and (a4.get("from_term_id"), a4.get("to_term_id")) == (lo, hi)
               and [(r[1], r[3]) for r in r4] == [(lo, hi)]
               and all(e and str(a4["relation_id"]) in e and "retire-term-relation" in e for e in (e4a, e4b)),
               (a4, e4a, e4b, r4))

        # T029-05 (rule 5): the converse of a directed row is a second home of one fact, refused by the same
        # index; a different kind between the same pair is not.
        a5 = attempt(addrel, E29, "broader", O29, "TASK-FIXTURE: broader", T29S, **LOC29)
        e5 = refusal(addrel, O29, "broader", E29, "TASK-FIXTURE: converse", T29S, **LOC29)
        a5b = attempt(addrel, O29, "part of", E29, "TASK-FIXTURE: another kind", T29S, **LOC29)
        record("T029-05", "the converse of a live directed row is refused naming the held relation; a different "
               "kind for the same pair is accepted", a5.get("relation_id") and e5 and str(a5["relation_id"]) in e5
               and a5b.get("relation_id"), (a5, e5, a5b))

        # T029-06 (OD-71): the justification is the base's own cells. Each of these is refused, naming what is
        # required, and writes nothing: no locator on a kind but `distinct` (a reason alone does not justify it),
        # a URL with no page or clause, a page with no URL, a URL that is not http(s), a line below 1, a blank
        # page, and a `distinct` row with no reason.
        n06 = len(rels())
        e6 = {"none": refusal(addrel, E29, "adjacent", O29, "TASK-FIXTURE: reason only", T29S),
              "url only": refusal(addrel, E29, "adjacent", O29, "TASK-FIXTURE", T29S, source_url=URL29),
              "page only": refusal(addrel, E29, "adjacent", O29, "TASK-FIXTURE", T29S, source_page="3"),
              "scheme": refusal(addrel, E29, "adjacent", O29, "TASK-FIXTURE", T29S, source_url="ftp://x.org/a",
                                source_page="3"),
              "line": refusal(addrel, E29, "adjacent", O29, "TASK-FIXTURE", T29S, source_line=0, **LOC29B),
              "blank page": refusal(addrel, E29, "adjacent", O29, "TASK-FIXTURE", T29S, source_url=URL29,
                                    source_page="  ", source_clause="c"),
              "distinct no reason": refusal(addrel, E29, "distinct", O29, None, T29S, **LOC29),
              "distinct partial locator": refusal(addrel, E29, "distinct", O29, "TASK-FIXTURE", T29S,
                                                  source_url=URL29)}
        record("T029-06", "no locator, a partial or malformed one, and a `distinct` row with no reason are each "
               "refused, naming what is required, and write nothing",
               all(e6.values()) and "--source-url" in e6["none"] and "--source-page or --source-clause" in e6["none"]
               and "--reason" in e6["distinct no reason"] and len(rels()) == n06, e6)

        # T029-07: a blank reason, an unknown term and one term at both ends are each refused.
        e7 = {"reason": refusal(addrel, E29, "adjacent", O29, "   ", T29S, **LOC29),
              "term": refusal(addrel, E29, "adjacent", "TASK-FIXTURE-NO-SUCH-TERM", "TASK-FIXTURE", T29S, **LOC29),
              "self": refusal(addrel, E29, "adjacent", E29, "TASK-FIXTURE", T29S, **LOC29)}
        record("T029-07", "a blank reason, an unknown term and the same term at both ends are each refused and "
               "write nothing", e7["reason"] and "--reason" in e7["reason"] and e7["term"] and "no such term" in
               e7["term"] and e7["self"] and "both ends" in e7["self"] and "two different terms" in e7["self"]
               and len(rels()) == n06, e7)

        # T029-08 (amendment 2): a relation is retired in place with a reason, never revived, and the reader keeps
        # only live rows; the pair can then be written again.
        id8 = a1["relation_id"]
        z8 = refusal(retrel, id8, "  ", T29S)
        d8 = attempt(retrel, id8, "TASK-FIXTURE: the source was withdrawn", T29S)
        again8 = refusal(retrel, id8, "TASK-FIXTURE: again", T29S)
        nosuch8 = refusal(retrel, 10 ** 9, "TASK-FIXTURE: none", T29S)
        row8 = q("SELECT retired_at, retired_by_session, retirement_reason, reason, kind, source_url FROM "
                 "term_relations WHERE relation_id=?", id8)
        r8 = attempt(elemread, E29)
        w8 = attempt(addrel, E29, K_PROV, P29, "TASK-FIXTURE: written again", T29S, **LOC29)
        record("T029-08", "retire-term-relation retires in place with a reason (the row stays, its other cells "
               "untouched), refuses a blank reason, a retired row and an unknown one; the reader drops it; the "
               "pair can be written again", z8 and d8.get("retired") is True and again8 and "retired at" in again8
               and nosuch8 and "no such relation" in nosuch8 and "select relation_id" in nosuch8
               and row8 and row8[0][0] and row8[0][1] == dbcore.session_stem(T29S)
               and row8[0][2] == "TASK-FIXTURE: the source was withdrawn"
               and row8[0][3] == "TASK-FIXTURE: the element should carry the provision" and row8[0][4] == K_PROV
               and row8[0][5] == URL29
               and r8.get("provisions") == [] and w8.get("relation_id") and w8["relation_id"] != id8,
               (z8, d8, again8, nosuch8, row8, r8, w8))

        # T029-09: the schema holds what the writers hold, so a route past the writers meets the same refusals.
        def raw(sql, *a):
            c = sqlite3.connect(DB)
            try:
                c.execute(sql, a)
                c.commit()
                return None
            except sqlite3.IntegrityError as exc:
                return str(exc)
            finally:
                c.close()
        ins = ("INSERT INTO term_relations (from_term_id, kind, to_term_id, reason, source_url, source_page, "
               "created_at, created_by_session) VALUES (?, ?, ?, ?, ?, ?, 't', 't')")
        lo9, hi9 = sorted((E29, O29))        # a pair with no live `distinct` row, so only the CHECK can refuse
        raw9 = {
            "a": ("no locator on a kind but `distinct`", raw(ins, E29, "adjacent", P29, "TASK-FIXTURE", None, None)),
            "b": ("a `distinct` row stored higher id first", raw(ins, hi9, "distinct", lo9, "TASK-FIXTURE", None,
                                                                 None)),
            "c": ("one term at both ends", raw(ins, E29, "adjacent", E29, "TASK-FIXTURE", URL29, "3")),
            "e": ("a kind outside the CHECK", raw(ins, E29, "equivalent", O29, "TASK-FIXTURE", URL29, "3")),
            "f": ("the converse of a live row of the same kind", raw(ins, O29, "broader", E29, "TASK-FIXTURE",
                                                                    URL29, "3")),
            "g": ("a `distinct` row with no reason", raw(ins, lo9, "distinct", hi9, None, None, None)),
            "h": ("a page with no URL", raw(ins, lo9, "distinct", hi9, "TASK-FIXTURE", None, "3")),
            "i": ("a URL that is not http(s)", raw(ins, E29, "adjacent", P29, "TASK-FIXTURE", "ftp://x.org/a", "3")),
        }
        # T029-09d: the three retirement cells are set together or not at all, and none is blank: every partial
        # combination and every blank one, derived by looping over the three columns, is refused.
        RET = ("retired_at", "retired_by_session", "retirement_reason")
        bad9d = []
        for mask in range(1, 7):          # every proper, non-empty subset of the three cells set
            vals = {c: ("t" if mask >> i & 1 else None) for i, c in enumerate(RET)}
            if not raw("UPDATE term_relations SET " + ", ".join(f"{c}=?" for c in RET) + " WHERE relation_id=?",
                       *vals.values(), w8["relation_id"]):
                bad9d.append(vals)
        vals = {c: "  " for c in RET}       # all three set, all blank
        if not raw("UPDATE term_relations SET " + ", ".join(f"{c}=?" for c in RET) + " WHERE relation_id=?",
                   *vals.values(), w8["relation_id"]):
            bad9d.append(vals)
        for i, c in enumerate(RET):       # all three set, exactly one of them blank
            vals = {k: ("  " if k == c else "t") for k in RET}
            if not raw("UPDATE term_relations SET " + ", ".join(f"{k}=?" for k in RET) + " WHERE relation_id=?",
                       *vals.values(), w8["relation_id"]):
                bad9d.append(vals)
        record("T029-09d", "the schema refuses a retirement with any one or two of its three cells set, any all-"
               "three set with one or all of them blank (a NULL reason passes a length check, so the form is the "
               "siblings' equality)", not bad9d and q("SELECT retired_at FROM term_relations WHERE relation_id=?",
                                                       w8["relation_id"]) == [(None,)], bad9d)
        for key, (what, err) in raw9.items():
            record(f"T029-09{key}", f"the schema refuses {what}, so a route past the writers meets the same refusal",
                   bool(err), err)

        # T029-10: the table is in the derived capture set, so a relation made on a scratch copy reaches the
        # canonical database through emit_batch_sql.
        con = sqlite3.connect(DB)
        try:
            cap29 = set(dbcore.writable_tables(con))
        finally:
            con.close()
        record("T029-10", "term_relations is in the derived capture set (dbcore.writable_tables)",
               "term_relations" in cap29)

        # T029-11: the reader refuses an unknown element, in a sentence; through the CLI it exits 1, not a traceback.
        r11 = run("element-parameters", "--element", "TASK-FIXTURE-NO-SUCH-TERM")
        record("T029-11", "element-parameters refuses an unknown element in a sentence",
               r11.returncode == 1 and r11.stderr.startswith("REFUSING:") and "no such term" in r11.stderr
               and "Traceback" not in r11.stderr, (r11.returncode, r11.stderr[-200:]))

        # T029-12: the CLI is wired for each verb, takes a kind containing spaces and the grounding flags; the
        # vocabulary offered is the CHECK's own.
        r12 = run("add-term-relation", "--from-term", O29, "--kind", "adjacent", "--to-term", P29, "--reason",
                  "TASK-FIXTURE: via the CLI", "--source-url", URL29, "--source-clause", "TASK-FIXTURE 9",
                  "--ref-id", "TASK-FIXTURE-REF", "--session", T29S)
        id12 = json.loads(r12.stdout).get("relation_id") if r12.returncode == 0 and r12.stdout.strip() else None
        r12b = run("retire-term-relation", "--relation-id", str(id12), "--reason", "TASK-FIXTURE: via the CLI",
                   "--session", T29S)
        r12c = run("add-term-relation", "--help")
        record("T029-12", "add-term-relation and retire-term-relation run through the CLI, and --kind offers "
               "exactly the column's own CHECK set", id12 and r12b.returncode == 0
               and all(k in r12c.stdout.replace("\n", " ") for k in KINDS29)
               and q("SELECT retired_at IS NOT NULL FROM term_relations WHERE relation_id=?", id12) == [(1,)],
               (r12.returncode, r12.stderr[-200:], r12b.returncode, r12b.stderr[-200:]))

        # T029-12b: the parser's --kind choices are READ from the column's CHECK, never a typed list (rule 8).
        import ast
        tree12 = ast.parse((REPO / "scripts" / "db.py").read_text(encoding="utf-8"))
        kind_calls = [n for n in ast.walk(tree12) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                      and n.func.attr == "add_argument" and isinstance(n.func.value, ast.Name)
                      and n.func.value.id == "p_atr" and n.args and isinstance(n.args[0], ast.Constant)
                      and n.args[0].value == "--kind"]
        ch12 = [k.value for c in kind_calls for k in c.keywords if k.arg == "choices"]
        record("T029-12b", "add-term-relation's --kind takes its choices from dbcore.schema_choices(\"term_relations\", "
               "\"kind\"), not a typed list", len(ch12) == 1 and isinstance(ch12[0], ast.Call)
               and getattr(ch12[0].func, "attr", None) == "schema_choices"
               and [a.value for a in ch12[0].args if isinstance(a, ast.Constant)] == ["term_relations", "kind"],
               [ast.dump(c) for c in ch12])

        # T029-13 (OD-56, OD-71): a provision is justified by where a source says the element should carry it,
        # never by a reason alone (the old rule, that an adjudication is no warrant, in the base's own terms): the
        # writer refuses it naming the locator, and the schema refuses it; with a locator it is accepted.
        n13 = len(rels())
        e13 = refusal(addrel, O29, K_PROV, P29, "TASK-FIXTURE: a reason alone", T29S)
        r13 = raw(ins, O29, K_PROV, P29, "TASK-FIXTURE: a reason alone", None, None)
        a13 = attempt(addrel, O29, K_PROV, P29, None, T29S, **LOC29B)
        record("T029-13", "an `element has provision` row with a reason and no locator is refused by the writer "
               "(naming --source-url) and by the schema; one with a locator is accepted",
               e13 and "--source-url" in e13 and r13 and a13.get("relation_id") and len(rels()) == n13 + 1,
               (e13, r13, a13))

        # T029-14: the reason is optional off `distinct`, a blank one is refused by the schema.
        a14 = attempt(addrel, O29, "part of", P29, None, T29S, **LOC29)
        r14 = raw(ins, E29, "adjacent", P29, "  ", URL29, "3")
        record("T029-14", "a relation with no reason is accepted and holds NULL there; a blank reason is refused by "
               "the schema", a14.get("relation_id") and q("SELECT reason FROM term_relations WHERE relation_id=?",
                                                          a14["relation_id"]) == [(None,)] and r14, (a14, r14))

        # T029-15 (a merged or retired parameter), on fixture terms and parameters written by SQL on the copy
        # (no writer builds a merged or retired state without a figure to merge); ids are derived from the form of
        # the held ids.
        pre = q("SELECT substr(term_id, 1, instr(term_id, '-')) FROM terms ORDER BY term_id LIMIT 1")[0][0]
        FT = {n: f"{pre}{num}" for n, num in (("keep", 9990), ("fold", 9991), ("gone", 9992), ("nope", 9993),
                                             ("lo", 9998), ("hi", 10001))}
        if q("SELECT COUNT(*) FROM terms WHERE term_id IN (%s)" % ",".join("?" * len(FT)), *FT.values())[0][0]:
            record("T029-15", "the fixture term ids are free", False, FT)
        else:
            for tid in FT.values():
                x("INSERT INTO terms (term_id, canonical_en, created_at, created_by_session, updated_at, "
                  "updated_by_session) VALUES (?, 'TASK-FIXTURE term', 't', ?, 't', ?)", tid, T29S, T29S)
            for n in ("keep", "fold", "gone"):
                x("INSERT INTO base_parameters (term_id, status, created_at, created_by_session) "
                  "VALUES (?, 'active', 't', ?)", FT[n], T29S)
            pid = {n: q("SELECT parameter_id FROM base_parameters WHERE term_id=?", FT[n])[0][0]
                   for n in ("keep", "fold", "gone")}
            x("INSERT INTO parameter_declinations (term_id, reason, created_at, created_by_session) "
              "VALUES (?, 'TASK-FIXTURE', 't', ?)", FT["nope"], T29S)
            w15 = {n: attempt(addrel, E29, K_PAR, FT[n], None, T29S, **LOC29) for n in ("fold", "nope")}
            x("UPDATE base_parameters SET status='merged', merged_into=? WHERE parameter_id=?", pid["keep"],
              pid["fold"])
            x("UPDATE base_parameters SET status='retired' WHERE parameter_id=?", pid["gone"])
            r15 = attempt(elemread, E29)
            by15 = {p["term_id"]: p for p in r15.get("parameters", [])}
            e15m = refusal(addrel, E29, K_PAR, FT["fold"], None, T29S, **LOC29B)
            e15r = refusal(addrel, E29, K_PAR, FT["gone"], None, T29S, **LOC29)
            a15 = attempt(addrel, E29, K_PAR, FT["keep"], None, T29S, **LOC29)
            record("T029-15a", "the reader follows a merged parameter to the one that stands (its id and term, and "
                   "the id it was written against)", by15.get(FT["fold"], {}).get("parameter_id") == pid["keep"]
                   and by15[FT["fold"]]["parameter_term_id"] == FT["keep"]
                   and by15[FT["fold"]]["merged_from_parameter_id"] == pid["fold"], (w15, by15.get(FT["fold"])))
            record("T029-15b", "the reader flags a term with a live declination: no parameter, declined",
                   by15.get(FT["nope"], {}).get("parameter_id", 0) is None and by15[FT["nope"]]["declined"] is True
                   and by15[FT["fold"]]["declined"] is False, by15.get(FT["nope"]))
            record("T029-15c", "a new `element has parameter` row to a term whose parameter is merged names the "
                   "survivor's term; to one whose parameter is retired says so; to an active one is accepted",
                   e15m and FT["keep"] in e15m and e15r and "retired" in e15r and a15.get("relation_id"),
                   (e15m, e15r, a15))

            # T029-16: `distinct` is stored lower first by the number after the hyphen (a text order puts the
            # 10001 id before the 9998 one); the schema holds the same order.
            a16 = attempt(addrel, FT["hi"], "distinct", FT["lo"], "TASK-FIXTURE: two", T29S)
            r16 = raw(ins, FT["hi"], "distinct", FT["gone"], "TASK-FIXTURE: two", None, None)
            record("T029-16", "a `distinct` row between a 4-digit and a 5-digit id is stored with the numerically "
                   "lower id first, whichever way it is named, and the schema refuses the other order",
                   (a16.get("from_term_id"), a16.get("to_term_id")) == (FT["lo"], FT["hi"]) and r16, (a16, r16))

        # T029-17 (OD-71): term_relations is a base table by the stage map and holds no foreign key into another
        # stage (its only foreign keys are into terms); its ref_id is a plain provenance cell: any text is
        # accepted, validated against nothing, printed by the reader and read by no decision.
        import yaml as _yaml
        SM29 = _yaml.safe_load((REPO / "governance" / "stage-map.yaml").read_text(encoding="utf-8"))["tables"]
        fk29 = [(f[2], SM29.get(f[2])) for f in q("PRAGMA foreign_key_list(term_relations)")]
        cols29 = {r[1]: r[2] for r in q("PRAGMA table_info(term_relations)")}
        a17 = attempt(addrel, O29, "adjacent", E29, "TASK-FIXTURE: provenance", T29S, ref_id="TASK-FIXTURE-NOT-A-REF",
                      **LOC29)
        a17b = attempt(addrel, P29, "adjacent", E29, "TASK-FIXTURE: no provenance", T29S, **LOC29)
        record("T029-17", "term_relations, a base table, holds no foreign key into another stage; ref_id is a "
               "plain nullable cell, accepted unvalidated and equally absent",
               SM29.get("term_relations") == "base" and fk29 and all(st == "base" for _, st in fk29)
               and "ref_id" in cols29 and a17.get("relation_id") and a17b.get("relation_id")
               and q("SELECT ref_id FROM term_relations WHERE relation_id IN (?, ?) ORDER BY relation_id",
                     a17["relation_id"], a17b["relation_id"]) == [("TASK-FIXTURE-NOT-A-REF",), (None,)],
               (fk29, a17, a17b))

    # ── T031: the clause inventory, the re-read flag and the clause pointer (OD-23, migration 153). Probes are derived
    # by query; every fixture is labelled TASK-FIXTURE and lives on the copy and in the temp log.
    T31S = "session_2026-11-18-t031-task-fixture"
    norm = retrieval_log.normalise_quote

    def forms31(term_id):
        return {f for (n,) in q("SELECT canonical_en FROM terms WHERE term_id=? UNION SELECT alias FROM term_aliases "
                                "WHERE term_id=? AND alias_type NOT IN ('NARROWER','BROADER')", term_id, term_id)
                for f in [norm(n)] if f}

    FREE31 = [t for t in FREE[30:] if not q("SELECT 1 FROM base_parameters WHERE term_id=?", t)
              and not q("SELECT 1 FROM parameter_declinations WHERE term_id=? AND revoked_at IS NULL", t)]
    T_IN = FREE31[0] if FREE31 else None
    NAME_IN = q("SELECT canonical_en FROM terms WHERE term_id=?", T_IN)[0][0] if T_IN else ""
    CL31 = [{"locator_scheme": "TASK-FIXTURE clause", "loc_clause": "4.1",
             "clause_text": f"Clause 4.1 The {NAME_IN} of every primary route shall be not less than 1500 mm."},
            {"locator_scheme": "TASK-FIXTURE clause", "loc_clause": "4.2",
             "clause_text": "Clause 4.2 A landing is provided at each change of direction."}]
    PAGES31 = [c["clause_text"] for c in CL31] + ["Clause 4.3 TASK-FIXTURE text of the T031 inventory."]
    BODY31 = "\n".join(f"[PDF page {i} of 3]\n{t}\n" for i, t in enumerate(PAGES31, start=1))
    T_OUT = next((t for t in FREE31[1:] if not any(f in norm(BODY31) for f in forms31(t))), None)
    record("T031-00", "the T031 fixtures exist: two free terms, the second named nowhere in the fixture text",
           T_IN and T_OUT, FREE31)
    SHA31 = put("t031-full-text.txt", BODY31.encode(), REF_A, derived_from="fixture3pages.pdf")
    PATH31 = pathlib.Path(LOG) / FIX / "t031-full-text.txt"

    def sc31(**k):
        d = {"ref_id": REF_A, "mode": "catalogue", "text_scope": "full", "file_sha256": SHA31,
             "method": "full-read", "open_pass_done": True, "clauses": [dict(c) for c in CL31]}
        d.update(k)
        return d

    n31 = (q("SELECT COUNT(*) FROM source_scans")[0][0], q("SELECT COUNT(*) FROM source_clauses")[0][0])
    expect_refusal("T031-02", "clauses without --open-pass-done are refused: the open pass writes the inventory",
                   "open pass", scan, sc31(open_pass_done=False), T31S)
    m3 = [refusal(scan, sc31(**k), T31S) for k in ({"text_scope": "partial"}, {"method": "pre-screen"},
                                                     {"mode": "targeted", "target_parameter_id": PE})]
    record("T031-03", "clauses on a reading that is not full, on a pre-screen and on a targeted reading are each "
           "refused (the open pass of a full catalogue full-read writes the inventory)",
           all(m and "--mode catalogue" in m for m in m3), m3)
    expect_refusal("T031-04", "a clause whose text is not in the file read is refused (backed by retained text)",
                   "does not occur in", scan,
                   sc31(clauses=[{"loc_clause": "9.9", "clause_text": "TASK-FIXTURE clause typed from memory"}]), T31S)
    expect_refusal("T031-05", "a clause that names no level of the hierarchy is refused", "names no place", scan,
                   sc31(clauses=[{"locator_scheme": "TASK-FIXTURE", "clause_text": CL31[1]["clause_text"]}]), T31S)
    m6a = refusal(scan, sc31(clauses=[{"loc_clause": "4.2", "clause_text": "  "}]), T31S)
    m6b = refusal(scan, sc31(clauses=[{"loc_clause": "4.2", "clause_text": CL31[1]["clause_text"],
                                       "loc_page": "2"}]), T31S)
    record("T031-06", "a blank clause text and a key that is not a column of source_clauses are each refused",
           m6a and "no clause_text" in m6a and m6b and "not columns a clause takes" in m6b, (m6a, m6b))
    m6c = [refusal(scan, sc31(clauses=c), T31S) for c in ([], "TASK-FIXTURE", ["TASK-FIXTURE"])]
    m6d = refusal(scan, sc31(clauses=[{"loc_clause": "4.2", "clause_text": "?!"}]), T31S)
    record("T031-06c", "an empty list, a list that is not of objects, and a clause text with no letter or digit "
           "(it matches anything) are each refused",
           all(m and "non-empty list of objects" in m for m in m6c) and m6d and "does not occur in" in m6d,
           (m6c, m6d))
    m6d = [refusal(scan, sc31(clauses=[{"loc_clause": v, "clause_text": CL31[1]["clause_text"]}]), T31S)
           for v in (["4.1", "4.2"], 4, None, {"a": "4.2"})]
    record("T031-06d", "a cell given as a list, a number, a null or an object is refused (one string per cell)",
           all(m and "other than text" in m for m in m6d), m6d)
    m6e = refusal(scan, sc31(clauses=[dict(CL31[1]), {**CL31[1], "clause_text": "A landing is provided"}]), T31S)
    record("T031-06e", "two clauses at one place in one reading are refused (one row per clause per reading)",
           m6e and "same place" in m6e, m6e)
    SHA31X = put("t031-undecodable-text.txt", b"Clause 7 \x81\x82\x83 TASK-FIXTURE", REF_A,
                  derived_from="fixture3pages.pdf")
    expect_refusal("T031-06b", "a file that cannot be decoded is refused: no clause can be checked against it",
                   "cannot be decoded", scan,
                   sc31(file_sha256=SHA31X, clauses=[{"loc_clause": "7", "clause_text": "Clause 7"}]), T31S)
    record("T031-07", "every refused inventory wrote nothing: no reading and no clause (T031-02 to 06e)",
           (q("SELECT COUNT(*) FROM source_scans")[0][0], q("SELECT COUNT(*) FROM source_clauses")[0][0]) == n31, n31)
    s31 = attempt(scan, sc31(), T31S)
    rows31 = q("SELECT clause_id, loc_clause, clause_text FROM source_clauses WHERE scan_id=? ORDER BY clause_id",
               s31.get("scan_id", -1))
    record("T031-01", "the open pass of a full reading writes one source_clauses row per clause, keyed by its scan_id",
           s31.get("clause_ids") == [r[0] for r in rows31] and [r[1] for r in rows31] == ["4.1", "4.2"]
           and [r[2] for r in rows31] == [c["clause_text"] for c in CL31], (s31, rows31))
    cl_path = os.path.join(TMP, "t031-clauses.json")
    with open(cl_path, "w", encoding="utf-8") as fh:
        json.dump(CL31, fh)
    r31 = run("record-scan", "--ref-id", REF_A, "--mode", "catalogue", "--text-scope", "full", "--file-sha256",
              SHA31, "--method", "full-read", "--open-pass-done", "--clauses", cl_path, "--session", T31S,
              "--dry-run")
    r31b = run("record-scan", "--ref-id", REF_A, "--mode", "catalogue", "--text-scope", "full", "--file-sha256",
               SHA31, "--method", "full-read", "--clauses", cl_path, "--session", T31S, "--dry-run")
    r31c = run("record-scan", "--ref-id", REF_A, "--mode", "catalogue", "--text-scope", "full", "--file-sha256",
               SHA31, "--method", "full-read", "--open-pass-done", "--clauses", cl_path + ".missing",
               "--session", T31S, "--dry-run")
    record("T031-01c", "record-scan refuses a --clauses path that is not a readable JSON file, in a sentence",
           r31c.returncode == 1 and r31c.stderr.startswith("REFUSING:") and "not a readable JSON" in r31c.stderr,
           r31c.stderr[-300:])
    record("T031-01b", "record-scan --clauses reads the JSON file on the CLI (dry run lands two clause ids) and "
           "refuses in a sentence without --open-pass-done",
           r31.returncode == 0 and len(json.loads(r31.stdout or "{}").get("clause_ids", [])) == 2
           and r31b.returncode == 1 and r31b.stderr.startswith("REFUSING:") and "open pass" in r31b.stderr,
           r31.stdout[-300:] + r31.stderr[-300:] + r31b.stderr[-300:])

    # Item 2: held clause text is not shown (dbcore.NOT_SHOWN, the one home). The render contract lists no view yet
    # (T-037 has not landed), so every view is held to it, and so is the owner-browser page, which embeds the whole
    # database: it must read no hidden column and never read a table by `*`. Each detector is proven on a seed.
    HIDDEN = {c for cs in dbcore.NOT_SHOWN.values() for c in cs}

    def views_showing(views):
        return [n for n, sql in views
                if any(c in (sql or "").lower() for c in HIDDEN)
                or (any(t in (sql or "") for t in dbcore.NOT_SHOWN)
                    and re.search(r"(^|[\s,])(\w+\.)?\*(\s|,|$)", (sql or "").lower()))]

    def page_shows(html):
        return re.findall(r'"select (?:rowid as _rid, )?\*', html) + (
            [] if "!(META.hidden[r.name] || []).includes(c.name)" in html else ["no META.hidden filter"])

    live_views = q("SELECT name, sql FROM sqlite_master WHERE type='view'")
    seeded = views_showing([("v_seed_a", "SELECT clause_id, clause_text FROM source_clauses"),
                            ("v_seed_b", "SELECT s.ref_id, c.* FROM source_scans s JOIN source_clauses c "
                                         "ON c.scan_id = s.scan_id"),
                            ("v_seed_c", "SELECT count(*) FROM source_clauses")])
    PAGE = (REPO / "scripts" / "generate" / "owner_browser.html").read_text(encoding="utf-8")
    page_seeded = page_shows(PAGE.replace('"select " + sel(name) + " from " + q(name) + " where rowid',
                                          '"select * from " + q(name) + " where rowid', 1))
    page_unfiltered = page_shows(PAGE.replace("!(META.hidden[r.name] || []).includes(c.name)", "true", 1))
    sys.path.insert(0, str(REPO / "scripts" / "generate"))
    con = sqlite3.connect(DB)
    try:
        ob_meta = attempt(importlib.import_module("owner_browser_build").meta, con, DB)
    finally:
        con.close()
    record("T031-08", "no view and not the owner-browser page shows clause_text (OD-23: clause NOT shown); the "
           "detectors flag a seeded view naming it, a seeded `c.*` view, a seeded `select *` page and a page with no "
           "hidden-column filter, and pass count(*); the page build carries dbcore.NOT_SHOWN",
           views_showing(live_views) == [] and seeded == ["v_seed_a", "v_seed_b"] and page_shows(PAGE) == []
           and page_seeded and page_unfiltered == ["no META.hidden filter"]
           and ob_meta.get("hidden") == {t: list(cs) for t, cs in dbcore.NOT_SHOWN.items()},
           (views_showing(live_views), seeded, page_shows(PAGE), page_seeded, page_unfiltered, ob_meta.get("hidden")))

    # Items 3 and 4: the route of each owed pair, and the re-read flag.
    P_IN = promote(T_IN).get("parameter_id") if T_IN else None
    P_OUT = promote(T_OUT).get("parameter_id") if T_OUT else None
    sys.path.insert(0, str(REPO / "scripts" / "audit"))
    scan_debt = importlib.import_module("scan_debt")

    def route(pid):
        con = sqlite3.connect(DB)
        try:
            return next((r for r in scan_debt.reread_routes(con, retrieval_log, pid) if r["ref_id"] == REF_A), None)
        finally:
            con.close()

    ri, ro = route(P_IN), route(P_OUT)
    record("T031-09", "a parameter promoted after the reading is matched against the inventory first (the clause "
           "naming it), then the retained text (on disk): neither pair is flagged",
           ri and ri["route"] == "inventory" and ri["clauses"] == [r[0] for r in rows31[:1]]
           and ro and ro["route"] == "retained-text" and ro["file"].endswith("t031-full-text.txt"), (ri, ro))
    d17 = run_audit("scan_debt.py", "--reread", "--limit", "100000")
    record("T031-17", "with the inventory and the retained text reaching every owed pair of a source read in full, "
           "scan_debt.py --reread passes (exit 0)", d17.returncode == 0 and "PASS:" in d17.stdout,
           d17.stdout[-600:] + d17.stderr)
    con = sqlite3.connect(DB)
    try:
        listed = {r["ref_id"] for r in scan_debt.reread_routes(con, retrieval_log)}
        unread_full = {r for (r,) in con.execute(
            "SELECT DISTINCT ref_id FROM v_scan_ledger WHERE status IN ('NOT-READ','READ-PARTIAL') AND ref_id NOT IN "
            "(SELECT ref_id FROM source_scans WHERE text_scope = 'full' AND method = 'full-read')")}
    finally:
        con.close()
    record("T031-18", "a pair of a source never read in full (REF_B, read in part only; a source never read) is plain "
           "debt, never routed for a re-read",
           REF_B in unread_full and len(unread_full) > 1 and not (listed & unread_full), sorted(listed & unread_full)[:5])
    PATH31.rename(PATH31.with_suffix(".gone"))          # the retained text leaves the disk
    try:
        ro2, ri2 = route(P_OUT), route(P_IN)
        d31 = run_audit("scan_debt.py", "--reread", "--limit", "100000")
        cs_out = attempt(db.cell_status, P_OUT)
        cs_in = attempt(db.cell_status, P_IN)
    finally:
        PATH31.with_suffix(".gone").rename(PATH31)
    record("T031-09b", "with no retained text on disk the pair no clause matches is flagged `reread`; the matched "
           "pair is still reached through the inventory",
           ro2 and ro2["route"] == "reread" and ri2 and ri2["route"] == "inventory", (ro2, ri2))
    good31 = PATH31.read_bytes()
    PATH31.write_bytes(good31 + b"TASK-FIXTURE: the file changed")    # on disk, but no longer the bytes read
    try:
        ro3 = route(P_OUT)
    finally:
        PATH31.write_bytes(good31)
    record("T031-09c", "a retained file that no longer hashes to the scan's sha256 is not retained text: flagged",
           ro3 and ro3["route"] == "reread", ro3)
    # The forms matched are those v_term_names reads (its display name, and the attested forms of
    # v_attested_term_forms), word by word: a BROADER form, an unrecorded form and a form inside a word do not reach
    # the pair; an attested SYNONYM does. Alias rows by SQL on the copy, a state for a fixture.
    def alias31(alias, kind, att):
        loc = ("https://example.org/task-fixture-t031", "1") if att in ("instrument", "other_source") else (None, None)
        return x("INSERT INTO term_aliases (term_id, alias, language, alias_type, attestation, source_url, "
                 "source_page, created_at, created_by_session, updated_at, updated_by_session) VALUES "
                 "(?, ?, 'EN', ?, ?, ?, ?, 't', ?, 't', ?)", T_OUT, alias, kind, att, *loc, T31S, T31S)

    tried = {}
    for key, args in (("broader", ("landing", "BROADER", "other_source")),
                      ("unrecorded", ("change of direction", "SYNONYM", "unrecorded")),
                      ("inside", ("rect", "SYNONYM", "other_source")),
                      ("attested", ("change of direction", "SYNONYM", "other_source"))):
        fid = alias31(*args)
        tried[key] = route(P_OUT)
        x("DELETE FROM term_aliases WHERE form_id = ?", fid)
    record("T031-09d", "a BROADER form, an unrecorded form and a form found only inside a word (`rect` in `direction`) "
           "do not reach the pair; an attested SYNONYM does, through the clause that holds it",
           all(tried[k] and tried[k]["route"] == "retained-text" for k in ("broader", "unrecorded", "inside"))
           and tried["attested"] and tried["attested"]["route"] == "inventory"
           and tried["attested"]["clauses"] == [r[0] for r in rows31[1:2]], tried)
    record("T031-10", "scan_debt.py --reread prints the flagged pair under reread, a REREAD line and EXAMINED, "
           "and exits 1",
           d31.returncode == 1 and "EXAMINED:" in d31.stdout and "REREAD:" in d31.stdout
           and f"{REF_A} x parameter {P_OUT} (NOT-READ)" in d31.stdout.split("  reread")[-1],
           d31.stdout[-600:] + d31.stderr)
    record("T031-13", "cell-status lists the flagged source under evidence, owed, reread_flagged, and not for the "
           "parameter the inventory reaches",
           REF_A in cs_out.get("stages", {}).get("evidence", {}).get("owed", {}).get("reread_flagged", [])
           and REF_A not in cs_in.get("stages", {}).get("evidence", {}).get("owed", {}).get("reread_flagged", [REF_A]),
           (cs_out.get("error"), cs_in.get("error")))
    attempt(scan, sc31(mode="targeted", target_parameter_id=P_OUT, open_pass_done=False, clauses=None), T31S)
    record("T031-15", "the flag is cleared by recording the reading: a targeted reading leaves the pair owed nowhere",
           route(P_OUT) is None and ledger(REF_A, P_OUT) == ("READ-NOTHING-FOUND", "full"), ledger(REF_A, P_OUT))
    # A later full reading of a CHANGED file: the clauses of the old file are not read for it.
    SHA31N = put("t031-full-text-2.txt", (BODY31 + "\nTASK-FIXTURE: a later edition").encode(), REF_A,
                 derived_from="fixture3pages.pdf")
    s31n = attempt(scan, sc31(file_sha256=SHA31N, open_pass_done=False, clauses=None), T31S)
    T3 = next((t for t in FREE31 if t not in (T_IN, T_OUT)), None)
    P3 = promote(T3).get("parameter_id") if T3 else None      # promoted after both readings: owed
    con = sqlite3.connect(DB)
    try:                                                       # an attested form that clause 4.2 of the OLD file holds
        f3 = con.execute("INSERT INTO term_aliases (term_id, alias, language, alias_type, attestation, source_url, "
                         "source_page, created_at, created_by_session, updated_at, updated_by_session) VALUES "
                         "(?, 'change of direction', 'EN', 'SYNONYM', 'other_source', "
                         "'https://example.org/task-fixture-t031', '1', 't', ?, 't', ?)", (T3, T31S, T31S)).lastrowid
        con.commit()
        rn = next((r for r in scan_debt.reread_routes(con, retrieval_log, P3) if r["ref_id"] == REF_A), None)
        con.execute("DELETE FROM term_aliases WHERE form_id = ?", (f3,))
        con.commit()
    finally:
        con.close()
    record("T031-19", "after a full reading of a changed file the old file's clauses no longer reach the pair "
           "(the inventory of the current file is read)",
           s31n.get("scan_id") and P3 and rn and rn["route"] == "retained-text"
           and rn["file"].endswith("t031-full-text-2.txt"),
           (s31n, rn))

    # Item 1, the pointer: a figure read from a clause points at it and types no locator. REF_A is put in the
    # regulatory stratum for these cases (tier 4: R3 demands a pinpoint), restored after: a state for a fixture.
    tier31 = q("SELECT tier FROM evidence_sources WHERE ref_id=?", REF_A)[0][0]
    x("UPDATE evidence_sources SET tier=4 WHERE ref_id=?", REF_A)
    PB = PE if q("SELECT 1 FROM base_parameters WHERE parameter_id=? AND status='active'", PE) else P_IN
    SHA31B = put("t031-b-text.txt", b"Section 2 TASK-FIXTURE the landing length of a ramp, read whole.", REF_B,
                 derived_from="fixture-b.html")
    sb = attempt(scan, {"ref_id": REF_B, "mode": "catalogue", "text_scope": "full", "file_sha256": SHA31B,
                        "method": "full-read", "open_pass_done": True,
                        "clauses": [{"loc_section": "2", "clause_text": "the landing length of a ramp"}]}, T31S)

    def fig31(**k):
        d = {"ref_id": REF_A, "parameter_id": PB, "identity_code": POP, "claim_type": "numerical",
             "lens_basis": "named_in_text", "lens_basis_text": "Clause", "claimed_value": "1500",
             "claimed_unit": "mm", "comparator": ">=", "figure_role": "claim", "extraction_method": "full-read",
             "claim_text": CL31[0]["clause_text"], "clause_id": rows31[0][0] if rows31 else -1}
        d.update(k)
        return d

    try:
        expect_refusal("T031-12a", "add-extraction refuses a clause another source's reading recorded",
                       "is a clause of", db.insert_extraction,
                       fig31(clause_id=(sb.get("clause_ids") or [-1])[0]), T31S, relations=[])
        expect_refusal("T031-12b", "add-extraction refuses a locator typed beside --clause-id (rule 5)",
                       ("second", "--loc-section"), db.insert_extraction, fig31(loc_section="4.1"), T31S,
                       relations=[])
        expect_refusal("T031-12c", "add-extraction refuses a clause_id that is no clause", "not a clause",
                       db.insert_extraction, fig31(clause_id=2 ** 30), T31S, relations=[])
        expect_refusal("T031-12d", "add-extraction refuses --source-section beside --clause-id (a prose locator is a "
                       "locator)", ("second", "--source-section"), db.insert_extraction,
                       fig31(source_section="Clause 9.9 somewhere else"), T31S, relations=[])
        expect_refusal("T031-12e", "add-extraction refuses a quote that is not inside the clause pointed at (clause "
                       "4.1's words with clause 4.2's id)", "not inside clause", db.insert_extraction,
                       fig31(clause_id=rows31[1][0] if len(rows31) > 1 else -1), T31S, relations=[])
        f31 = attempt(db.insert_extraction, fig31(), T31S, relations=[])
        row31 = q("SELECT clause_id, locator_scheme, loc_clause, source_section FROM source_value_extractions "
                  "WHERE extraction_id=?", f31.get("extraction_id", -1))
        record("T031-11", "a tier-4 figure with --clause-id and no locator of its own lands (R3 reads the clause's "
               "place) and stores only the pointer",
               bool(rows31) and row31 == [(rows31[0][0], None, None, None)], (f31, row31))
        g31 = run("--session", T31S, script="audit/research_batch_dod.py")
        record("T031-11b", "the batch gate's R3 counts the clause pointer as a pinpoint for that figure",
               "R3: PASS" in g31.stdout, [l for l in g31.stdout.splitlines() if "R3" in l])
        con = sqlite3.connect(DB)
        con.row_factory = sqlite3.Row
        try:
            inp31 = con.execute("SELECT * FROM source_value_extractions WHERE extraction_id=?",
                                (f31.get("extraction_id", -1),)).fetchone()
            m16 = refusal(db._refuse_bad_derived_input, con, "TASK-FIXTURE", inp31) if inp31 else "no row"
        finally:
            con.close()
        record("T031-16", "a derived figure's input that points at a clause has a locator (R3 for derived inputs)",
               inp31 is not None and m16 is None, m16)
        # R3 joins the clause: a figure (written past the writer, by SQL on the copy) pointing at another source's
        # clause or at no clause has no pinpoint, at the batch gate and as a derived input.
        T31R = "session_2026-11-18-t031-task-fixture-r3"
        bad_ids = [x("INSERT INTO source_value_extractions (ref_id, parameter_id, claim_type, claimed_value, claim_text, "
                     "extraction_method, created_at, created_by_session, updated_at, figure_role, clause_id) VALUES "
                     "(?, ?, 'numerical', '1500', 'TASK-FIXTURE', 'full-read', 't', ?, 't', 'claim', ?)",
                     REF_A, PB, T31R, cid) for cid in ((sb.get("clause_ids") or [-1])[0], 987654321)]
        g20 = run("--session", T31R, script="audit/research_batch_dod.py")
        con = sqlite3.connect(DB)
        con.row_factory = sqlite3.Row
        try:
            m20 = [refusal(db._refuse_bad_derived_input, con, "TASK-FIXTURE", con.execute(
                "SELECT * FROM source_value_extractions WHERE extraction_id=?", (i,)).fetchone()) for i in bad_ids]
        finally:
            con.close()
        x("DELETE FROM source_value_extractions WHERE created_by_session = ?", T31R)
        record("T031-20", "R3 (batch gate and derived input) finds no pinpoint in a pointer to another source's clause "
               "or to no clause",
               "R3: PASS" not in g20.stdout and REF_A in "".join(l for l in g20.stdout.splitlines() if "R3" in l)
               and all(m and "R3" in m for m in m20), ([l for l in g20.stdout.splitlines() if "R3" in l], m20))
    finally:
        x("UPDATE evidence_sources SET tier=? WHERE ref_id=?", tier31, REF_A)
    # The schema itself (migration 154): blank locator cells and blank text, an `_end` without its start, and a second
    # row at one place in one reading are refused by SQL that bypasses the writer.
    def schema_refuses(**cells):
        row = {"scan_id": s31.get("scan_id", -1), "loc_clause": "8.1", "clause_text": "TASK-FIXTURE",
               "created_at": "t", "created_by_session": T31S, **cells}
        con = sqlite3.connect(DB)
        try:
            con.execute(f"INSERT INTO source_clauses ({','.join(row)}) VALUES ({','.join('?' * len(row))})",
                        list(row.values()))
            return False
        except sqlite3.IntegrityError:
            return True
        finally:
            con.rollback()
            con.close()

    held = {"blank loc_clause": schema_refuses(loc_clause=""),
            "spaces loc_section": schema_refuses(loc_section="   "),
            "nbsp clause_text": schema_refuses(clause_text="\u00a0"),
            "end without start": schema_refuses(loc_clause=None, loc_section="8", loc_clause_end="8.2"),
            "same place twice": schema_refuses(locator_scheme=CL31[0]["locator_scheme"], loc_clause="4.1"),
            "control lands": not schema_refuses()}
    record("T031-21", "the schema refuses a blank locator cell, a blank text (no-break space), an `_end` without its "
           "start and a second row at one place in one reading; a good row lands", all(held.values()), held)
    con = sqlite3.connect(DB)
    try:
        record("T031-14", "source_clauses is in the derived capture set, and clause_id is not amendable (the locator "
               "is where the quote was read)",
               "source_clauses" in dbcore.writable_tables(con) and "clause_id" in db._NOT_AMENDABLE_SVE
               and "clause_id" not in db._amendable_sve_fields(con))
    finally:
        con.close()

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
        emit_mod.emit(DB, str(REPO / "data" / "guidebook.db"), out_sql)
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
        ("rename-term", ["--term-id", TR, "--canonical-en", "x y", "--reason", "x", "--judge", "x"],
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
