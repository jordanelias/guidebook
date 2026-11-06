#!/usr/bin/env python3
"""The refusals the run-pipeline skill states and no writer held (2026-11-06).

WHY THIS EXISTS (CLAUDE.md section 8). Two independent operator walk-throughs of
`skills/run-pipeline_SKILL.md` on scratch copies of the database wrote, through the
sanctioned CLI, every row the skill says is refused: a `verified` extraction over an
abstract-scope reading (OR-11a), an extraction on an UNVERIFIED source with no reading
recorded, a fabricated claim text behind a false `--verbatim-exempt`, a numerical row with
no locator, a `full` reading of a publisher landing page, a parameter direction with the
rationale "no admitted source read", a term minted beside its near-duplicate, a NAMES-NEW
adjudication to an existing term, a harm finding with no `insufficient` edge, a connection
at SPECULATIVE confidence with a hand-typed id and a retired target, a search with an
unknown slug, language or merged parameter, a hand-typed ref_id, a conflict between a
population and itself, and Crossref's own affiliation-as-author deposit written as six
corporate co-authors. What reaches the guidebook without these cases: a page that prints
"verified" over a figure nobody read in full, a value attributed to a source that was
never obtained, a direction nobody can trace to a document, and a byline that lists a
university five times.

Round 2 (same day) adds the cases for the second pass over the same walk-throughs: what is
owed has one home (R2-1), a real search is never refused for its pairing (R2-2), a block
reason is an obstacle the ledger classes and a reading clears (R2-3), a damaged byline behind
a malformed deposit is still a cross (R2-4), `full` is checked against what the document is
(R2-5), the exemption is refused where a body is held, for observe-term too (R2-6), a slug
must exist (R2-7), a reference id is computed (R2-9), a connection type has an arity row
(R2-10), a flag that says "live vocabulary" prints it (R2-11), a comparator word is refused
in a NAME only (R2-12), the verified-scan reader examines every live extraction (R2-15) and
the skill-vocabulary audit can go red (R2-16). Nothing here types a count, an id or a code
the database can derive; a state the CLI cannot build is made by SQL on a second copy and
marked HAND.

Each case shows the refusal fires AND the legitimate shape still passes. Runs on a COPY
of the canonical database (dbcore refuses the canonical file read-write) against the
tracked retrieval log; one case swaps in a scratch log root to make a source that holds
only undecodable bytes, the one shape `--verbatim-exempt` is for.
"""
import json
import os
import pathlib
import shutil
import sqlite3
import sys
import tempfile
import io
import contextlib
import hashlib
import subprocess

REPO = pathlib.Path(__file__).resolve().parents[2]
os.chdir(REPO)                                  # retrieval-log/ is cwd-relative
TMP = tempfile.mkdtemp(prefix="run-pipeline-refusals-")
DB = os.path.join(TMP, "guidebook.db")
shutil.copy(REPO / "data" / "guidebook.db", DB)
os.environ["GUIDEBOOK_DB_PATH"] = DB
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "scripts" / "research"))
import db        # noqa: E402
import dbcore    # noqa: E402
import retrieval_log  # noqa: E402
from dbcore import Refusal  # noqa: E402

S = "session_test-run-pipeline-refusals"
results = []


def record(tid, name, passed, details=""):
    results.append(bool(passed))
    print(f"  [{'✓' if passed else '✗'}] {tid}: {name}")
    if details and not passed:
        print(f"      {str(details)[:400]}")


def refusal(fn, *a, **k):
    """The Refusal's text if `fn` refuses, else None; any other exception is a defect."""
    try:
        fn(*a, **k)
    except Refusal as exc:
        return str(exc)
    except Exception as exc:  # noqa: BLE001
        print(f"      DEFECT (not a refusal): {type(exc).__name__}: {exc}")
        return None
    return None


def ok(fn, *a, **k):
    """(result, error-text) -- the legitimate shape must not refuse."""
    try:
        return fn(*a, **k), None
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"


con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
q = lambda sql, *p: con.execute(sql, p).fetchall()  # noqa: E731


@contextlib.contextmanager
def scratch():
    """A second copy of the test database for a case that needs hand-built state (each such
    statement says HAND). db.py follows GUIDEBOOK_DB_PATH at call time, so its writers act on it."""
    path = os.path.join(TMP, f"scratch-{len(results)}.db")
    shutil.copy(DB, path)
    os.environ["GUIDEBOOK_DB_PATH"] = path
    retrieval_log.DB_PATH = pathlib.Path(path)       # read once at import, not per call
    c = sqlite3.connect(path)
    c.row_factory = sqlite3.Row
    try:
        yield c
    finally:
        c.close()
        os.environ["GUIDEBOOK_DB_PATH"] = DB
        retrieval_log.DB_PATH = pathlib.Path(DB)


@contextlib.contextmanager
def log_root(path):
    """Point the retrieval log at a scratch root, so a fixture source holds only its fixtures."""
    old = retrieval_log.LOG_ROOT
    retrieval_log.LOG_ROOT = pathlib.Path(path)
    retrieval_log._ARTEFACT_INDEX.clear()
    try:
        yield
    finally:
        retrieval_log.LOG_ROOT = old
        retrieval_log._ARTEFACT_INDEX.clear()


def far(an_id):
    """An id of `an_id`'s shape (prefix and width) that does not exist yet: its number plus a
    power of ten that leaves the width alone."""
    head, num = an_id.rsplit("-", 1)
    return f"{head}-{int(num) + 10 ** (len(num) - 1):0{len(num)}d}"


def cli(*argv):
    return subprocess.run([sys.executable, str(REPO / "scripts" / "db.py"), *argv],
                          capture_output=True, text=True, env=dict(os.environ))


def held_text(root, ref, text, payload=None):
    """In the scratch retrieval-log `root`, persist for `ref` a derived text with no page markers
    (named `-text.txt`, the shape the old suffix test missed) and, when `payload` is given, a
    Crossref-shaped bibliographic payload. Returns the text's sha256."""
    d = pathlib.Path(root) / "session_fixture"
    d.mkdir(parents=True, exist_ok=True)
    src = d / f"{ref}-payload.json"
    src.write_text(json.dumps({"message": {"DOI": f"10.0000/{ref}", **(payload or {})}}))
    if payload is not None:
        with open(d / "manifest.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"retrieved_at": "2026-11-06T00:00:00+00:00", "url": f"x:{ref}",
                                 "purpose": "fixture", "ref_id": ref, "bytes": src.stat().st_size,
                                 "sha256": hashlib.sha256(src.read_bytes()).hexdigest(), "exit": 0,
                                 "status": 200, "artefact": src.name, "content_type": None}) + "\n")
    txt = d / f"{ref}-text.txt"
    txt.write_text(text)
    with log_root(root):
        retrieval_log.record_file(txt, "session_fixture", src.name, purpose="fixture text",
                                  ref_id=ref, kind="text-extraction")
    return hashlib.sha256(txt.read_bytes()).hexdigest()

# Fixtures read from the copy, never hard-coded ids (CLAUDE.md rule 7a).
def _full_fixture():
    """The newest full-scope catalogue reading whose derived text carries a quotable figure,
    for a source that holds an extraction on an active, direction-less parameter."""
    for s in q("SELECT s.ref_id, s.catalogue_version FROM source_scans s JOIN evidence_sources e "
               "USING (ref_id) WHERE s.text_scope='full' AND s.mode='catalogue' "
               "ORDER BY (e.tier < 4) DESC, s.scan_id DESC"):
        pids = q("SELECT parameter_id FROM base_parameters WHERE status='active' AND "
                 "parameter_id<=? AND accessibility_direction IS NULL AND parameter_id IN "
                 "(SELECT parameter_id FROM source_value_extractions WHERE ref_id=?) LIMIT 1",
                 s["catalogue_version"], s["ref_id"])
        if not pids:
            continue
        for h in retrieval_log.artefacts_for_source(s["ref_id"]):
            if not (h["derived"] and h["exists"]):
                continue
            text = h["path"].read_text(encoding="utf-8", errors="replace")
            m = re.search(r"[A-Za-z][^\n.]{20,100}\b(\d{3,4})\b[^\n.]{0,40}", text)
            if m:
                return s["ref_id"], s["catalogue_version"], pids[0][0], m.group(0).strip(), \
                    m.group(1), h["sha256"]
    raise SystemExit("no full-scope reading with a quotable derived text: fixture absent")


import re  # noqa: E402
FULL_REF, FULL_CV, P_FULL, QUOTE, VALUE, FULL_SHA = _full_fixture()
def _abstract_fixture():
    """A VERIFIED, DOI-bearing source read only at abstract scope that holds a fetched HTML page."""
    for s in q("SELECT ref_id FROM source_scans WHERE text_scope='abstract' AND ref_id IN "
               "(SELECT ref_id FROM evidence_sources WHERE verification_status='VERIFIED' "
               "AND doi IS NOT NULL)"):
        for h in retrieval_log.artefacts_for_source(s["ref_id"]):
            if h["exists"] and not h["derived"] and str(h["path"]).endswith(".html"):
                return s["ref_id"], h["sha256"]
    raise SystemExit("no abstract-scope source with a held HTML page: fixture absent")


ABSTRACT_REF, HTML_SHA = _abstract_fixture()
UNVERIFIED_REF = q("SELECT ref_id FROM evidence_sources WHERE verification_status='UNVERIFIED' "
                   "LIMIT 1")[0][0]
NOSCAN_REF = q("SELECT e.ref_id FROM evidence_sources e WHERE verification_status='VERIFIED' "
               "AND NOT EXISTS (SELECT 1 FROM source_scans s WHERE s.ref_id=e.ref_id) "
               "AND superseded_by_ref_id IS NULL LIMIT 1")[0][0]
SLUG = q("SELECT slug FROM slugs WHERE status='ACTIVE' ORDER BY slug LIMIT 1")[0][0]
IDENT = q("SELECT identity_code FROM base_taxonomy_identity WHERE identity_code<>'ALL' "
          "ORDER BY identity_code LIMIT 1")[0][0]
# Two live sources that hold nothing in the scratch retrieval log below, for the cases that
# need a source whose held text and bibliographic payload the test itself decides.
PAGED_REF, PLAIN_REF = [r[0] for r in q("SELECT ref_id FROM evidence_sources WHERE "
                                        "superseded_by_ref_id IS NULL ORDER BY ref_id DESC LIMIT 2")]
LOG3 = os.path.join(TMP, "retrieval-log3")


def extraction(ref, pid, **over):
    base = {"ref_id": ref, "parameter_id": pid, "identity_code": IDENT,
            "claim_type": "numerical", "claimed_value": VALUE, "claimed_unit": "mm",
            "claim_text": QUOTE, "extraction_method": "full-read", "figure_role": "claim",
            "source_section": "section 3", "loc_section": "3"}
    base.update(over)
    return base


print("Section M (R2-1, R2-3): one view says what is owed; a recorded reading outranks a block")
# NOTHING BELOW NAMES A COUNT, ID OR CODE. The oracle is the base table (the map minus
# `scoped-out`, a NULL being owed), independent of the view it checks. A legitimate scope fill
# changes the derived numbers, not the relations asserted.
UNSEARCHED = ("SELECT COUNT(*) FROM lang_jur_map m WHERE NOT EXISTS (SELECT 1 FROM search_executions "
              "se WHERE se.slug=? AND se.jurisdiction=m.jurisdiction AND UPPER(se.language)=m.language)")
with scratch() as c:
    # HAND: a partial scope fill (a data PR the CLI has no verb for): one language, one that
    # still has an unsearched pair for this slug, is recorded out of scope.
    out_lang = c.execute("SELECT m.language FROM lang_jur_map m WHERE NOT EXISTS (SELECT 1 FROM "
                         "search_executions se WHERE se.slug=? AND se.jurisdiction=m.jurisdiction "
                         "AND UPPER(se.language)=m.language) LIMIT 1", (SLUG,)).fetchone()[0]
    c.execute("UPDATE lang_jur_map SET scope_status='scoped-out' WHERE language=?", (out_lang,))
    c.commit()
    try:
        in_view = c.execute("SELECT COUNT(*) FROM v_coverage_priority WHERE slug=?", (SLUG,)).fetchone()[0]
        scope_n = c.execute("SELECT COUNT(*) FROM v_research_scope").fetchone()[0]
    except sqlite3.OperationalError as exc:       # a database from before migration 123
        in_view = scope_n = str(exc)
    owed = c.execute(UNSEARCHED + " AND COALESCE(m.scope_status,'in-scope')<>'scoped-out'", (SLUG,)).fetchone()[0]
    whole = c.execute(UNSEARCHED, (SLUG,)).fetchone()[0]
    owed_rows = c.execute("SELECT COUNT(*) FROM lang_jur_map WHERE COALESCE(scope_status,'in-scope')"
                          "<>'scoped-out'").fetchone()[0]
record("W01", "v_coverage_priority and v_research_scope follow scope_status (a partial fill does "
              "not empty the requirement, and the scoped-out language is no longer owed)",
       in_view == owed and scope_n == owed_rows and owed < whole, (in_view, owed, whole, scope_n))

LEDGER = "SELECT parameter_id, status FROM v_scan_ledger WHERE ref_id=?"
VOCAB = sorted(dbcore.check_values(con, "evidence_sources", "processing_blocked_reason"))
# JUDGEMENT, named: the reasons migration 091's CHECK comment gives as restatements of a typed
# fact (a recorded reading; superseded_by_ref_id), which the writers refuse by pointer.
# Each maps to the typed home a refusal must name (the column's existence is asserted below).
COPY_HOME = {v: h for v, h in (("no-quantified-claims", "record-scan"),
                               ("superseded", "superseded_by_ref_id")) if v in VOCAB}
COPY_VALUES = sorted(COPY_HOME)
read_ref = q("SELECT ref_id FROM v_scan_ledger WHERE status IN ('READ-PARTIAL','READ-NOTHING-FOUND') "
             "LIMIT 1")[0][0]
unread_ref = q("SELECT e.ref_id FROM evidence_sources e WHERE e.superseded_by_ref_id IS NULL AND NOT "
               "EXISTS (SELECT 1 FROM source_scans s WHERE s.ref_id=e.ref_id) LIMIT 1")[0][0]
moved, obstacle = [], set()
with scratch() as c:
    # HAND: set each admitted reason on a source with a recorded reading (the CLI sets it only
    # through amend-source, which the next cases use), and read the ledger.
    base_read = dict(c.execute(LEDGER, (read_ref,)).fetchall())
    for v in VOCAB:
        c.execute("UPDATE evidence_sources SET processing_blocked_reason=? WHERE ref_id=?", (v, read_ref))
        moved += [(v, k) for k, st in c.execute(LEDGER, (read_ref,)).fetchall()
                  if st != base_read[k] and base_read[k] != "NOT-READ"]
        c.execute("UPDATE evidence_sources SET processing_blocked_reason=? WHERE ref_id=?", (v, unread_ref))
        if any(st == "BLOCKED" for _, st in c.execute(LEDGER, (unread_ref,))):
            obstacle.add(v)
record("W02", "a recorded reading outranks a block: no reason changes the status of a pair a reading "
              "or an extraction already settles", not moved, moved[:3])
record("W03", "the ledger classes SOME reasons, not all, as obstacles, and never one a writer refuses "
              "as a copy of a typed fact", bool(obstacle) and obstacle < set(VOCAB)
       and not obstacle & set(COPY_VALUES), (sorted(obstacle), COPY_VALUES))
OBSTACLE = min(obstacle) if obstacle else VOCAB[0]

print("Section A1/A2: extraction_status and the reading record (OR-11a, R16)")
r = refusal(db.insert_extraction, extraction(ABSTRACT_REF, P_FULL, extraction_status="verified",
                                             claim_text="fabricated sentence stating 1200 mm",
                                             claimed_value="1200"),
            session=S, dry_run=True, relations=[], verbatim_exempt="payload is an image")
record("V01", "add-extraction refuses extraction_status=verified over an abstract-scope reading",
       r and "full" in r, r)
r = refusal(db.insert_extraction, extraction(UNVERIFIED_REF, P_FULL,
                                             claim_text="fabricated", claimed_value="12"),
            session=S, dry_run=True, relations=[], verbatim_exempt="unretrievable")
record("V02", "add-extraction refuses a source that is not VERIFIED", r and "VERIFIED" in r, r)
r = refusal(db.insert_extraction, extraction(NOSCAN_REF, P_FULL, claim_text="fabricated",
                                             claimed_value="12"),
            session=S, dry_run=True, relations=[], verbatim_exempt="no artefact")
record("V03", "add-extraction refuses a source with no reading recorded (record-scan first)",
       r and "record-scan" in r, r)
res, err = ok(db.insert_extraction, extraction(FULL_REF, P_FULL, extraction_status="verified"),
              session=S, dry_run=True, relations=[])
record("V04", "add-extraction accepts verified over a full-scope reading that covers the parameter",
       res is not None, err)
ab_row = q("SELECT extraction_id FROM source_value_extractions WHERE ref_id=? LIMIT 1",
           ABSTRACT_REF)[0][0]
r = refusal(db.amend_extraction, ab_row, "extraction_status", "verified", "probe", session=S,
            dry_run=True)
record("V05", "amend-extraction refuses verified with no full-scope covering reading",
       r and "full" in r, r)
full_row = q("SELECT extraction_id FROM source_value_extractions WHERE ref_id=? AND "
             "parameter_id<=? AND extraction_status<>'verified' LIMIT 1", FULL_REF, FULL_CV)[0][0]
res, err = ok(db.amend_extraction, full_row, "extraction_status", "verified", "probe",
              session=S, dry_run=True)
record("V06", "amend-extraction accepts verified over a full-scope covering reading",
       res is not None, err)

print("Section A3: --verbatim-exempt only where no decodable body is held")
r = refusal(db.insert_extraction, extraction(FULL_REF, P_FULL, claim_text="fabricated clause",
                                             claimed_value="12"),
            session=S, dry_run=True, relations=[], verbatim_exempt="scanned")
record("X01", "exemption refused when a derived text / HTML body is held for the source",
       r and "artefact" in r.lower(), r)
# A source holding only undecodable bytes: a scratch log root with one PDF-shaped file.
LOG2 = pathlib.Path(TMP) / "retrieval-log"
sess2 = LOG2 / "session_scratch"
sess2.mkdir(parents=True)
pdf = sess2 / "aaaa.pdf"
pdf.write_bytes(b"%PDF-1.4\n" + bytes(range(256)) * 8)
sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
(sess2 / "manifest.jsonl").write_text(json.dumps({
    "artefact": "aaaa.pdf", "sha256": sha, "ref_id": NOSCAN_REF, "status": 200,
    "content_type": "application/pdf", "url": "x"}) + "\n")
con.execute("INSERT INTO source_scans (ref_id, mode, catalogue_version, text_scope, file_sha256, "
            "method, created_at, created_by_session) VALUES (?,?,?,?,?,?,?,?)",
            (NOSCAN_REF, "catalogue", FULL_CV, "partial", sha, "full-read", "t", S))
con.commit()
retrieval_log.LOG_ROOT = LOG2
retrieval_log._ARTEFACT_INDEX.clear()
res, err = ok(db.insert_extraction, extraction(NOSCAN_REF, P_FULL, claim_text="a clause read off paper",
                                               claimed_value="12"),
              session=S, dry_run=True, relations=[], verbatim_exempt="scanned PDF, no text layer")
record("X02", "exemption accepted for a source whose only artefact is undecodable",
       res is not None, err)
res, err = ok(db.observe_term, {"ref_id": NOSCAN_REF, "surface_form": "clause", "locator": "p1",
                                "context_quote": "a clause read off paper",
                                "verbatim_exempt": "scanned PDF, no text layer"}, S, dry_run=True)
record("X03", "observe-term accepts the same exemption for that source (R2-6, the shape beside X04)",
       res is not None, err)
retrieval_log.LOG_ROOT = pathlib.Path("retrieval-log")
retrieval_log._ARTEFACT_INDEX.clear()

print("Section A4: a locator on every quantified row; no byte-identical duplicate")
r = refusal(db.insert_extraction, extraction(FULL_REF, P_FULL, source_section=None,
                                             loc_section=None),
            session=S, dry_run=True, relations=[])
record("L01", "a numerical row with no locator at all is refused (R3, every tier)",
       r and "UNVERIFIED-QUANT" in r, r)
TIER = q("SELECT tier FROM evidence_sources WHERE ref_id=?", FULL_REF)[0][0]
res, err = ok(db.insert_extraction, extraction(FULL_REF, P_FULL, loc_section=None),
              session=S, dry_run=False, relations=[])
record("L02", f"the same row with --source-section is written (tier {TIER} source; prose "
              f"locator suffices below tier 4)", res is not None, err)
r = refusal(db.insert_extraction, extraction(FULL_REF, P_FULL, loc_section=None),
            session=S, dry_run=True, relations=[])
record("L03", "a byte-identical second row is refused (a copy is not a contest)",
       r and "identical" in r, r)

print("Section A5: a full reading names a derived text")
r = refusal(db.record_scan, {"ref_id": ABSTRACT_REF, "mode": "catalogue", "text_scope": "full",
                             "file_sha256": HTML_SHA, "method": "full-read"}, session=S,
            dry_run=True)
record("S01", "record-scan refuses --text-scope full over a fetched HTML page",
       r and "full_text.py" in r, r)
res, err = ok(db.record_scan, {"ref_id": FULL_REF, "mode": "catalogue", "text_scope": "full",
                               "file_sha256": FULL_SHA, "method": "full-read"}, session=S,
              dry_run=True)
record("S02", "record-scan accepts full over the derived text", res is not None, err)

print("Section A6: a direction names the admitted source it was read from")
r = refusal(db.set_parameter_direction, parameter_id=P_FULL, direction="higher_is_better",
            rationale="no admitted source read", session=S, dry_run=True)
record("D01", "set-parameter-direction refuses with no --ref-id", r and "ref-id" in r, r)
r = refusal(db.set_parameter_direction, parameter_id=P_FULL, direction="higher_is_better",
            rationale="x", ref_id=ABSTRACT_REF, session=S, dry_run=True)
record("D02", "refuses a source holding no extraction for the parameter",
       r and "extraction" in r, r)
res, err = ok(db.set_parameter_direction, parameter_id=P_FULL, direction="higher_is_better",
              rationale="the report's finding", ref_id=FULL_REF, session=S, dry_run=False)
stored = q("SELECT direction_ref_id FROM base_parameters WHERE parameter_id=?", P_FULL)[0][0]
record("D03", "accepted with a source that holds one; direction_ref_id stored",
       res is not None and stored == FULL_REF, err or stored)

print("Section A7: equivalence before minting; NAMES-NEW only through add-term")
near = q("SELECT t.term_id, t.canonical_en FROM terms t JOIN base_parameters p USING (term_id) "
         "WHERE t.canonical_en LIKE '% %' ORDER BY length(t.canonical_en) DESC LIMIT 1")[0]
words = near["canonical_en"].split()
subset_name = " ".join(words[:-1]) + "s"          # token subset, plural: 'ramp runs' shape
obs = q("SELECT observation_id FROM observed_terms WHERE context_quote IS NOT NULL LIMIT 1")[0][0]
r = refusal(db.insert_term, obs, subset_name, "probe", session=S, dry_run=True)
record("T01", f"add-term refuses {subset_name!r} beside {near['term_id']} {near['canonical_en']!r}",
       r and near["term_id"] in r, r)
res, err = ok(db.insert_term, obs, subset_name, "probe", session=S, dry_run=True,
              distinct_from=[near["term_id"]])
record("T02", "accepted when --distinct-from names the near term", res is not None, err)
r = refusal(db.adjudicate_term, obs, "NAMES-NEW", "probe", session=S, term_id=near["term_id"],
            dry_run=True)
record("T03", "adjudicate-term refuses NAMES-NEW, naming add-term", r and "add-term" in r, r)

print("Section A11: a harm finding carries its insufficient edge")
r = refusal(db.insert_extraction, extraction(FULL_REF, P_FULL, figure_role="finding",
                                             harm_finding=1),
            session=S, dry_run=True, relations=[])
record("H01", "--harm-finding with --relation none is refused", r and "insufficient" in r, r)
res, err = ok(db.insert_extraction, extraction(FULL_REF, P_FULL, figure_role="finding",
                                               harm_finding=1, source_section="s. 4"),
              session=S, dry_run=True,
              relations=[{"relation": "insufficient", "to_label": "the code value",
                          "to_kind": "standard", "stated": "inferred", "quote": QUOTE}])
record("H02", "accepted with an insufficient edge", res is not None, err)

print("Section A18: a payload that repeats an author name is malformed")
# A logged payload that repeats an author name and whose DOI a source holds (derived from the
# tracked log, as the writer derives it, not named).
MAL = None
for d in sorted(x for x in retrieval_log.LOG_ROOT.iterdir() if x.is_dir()):
    for doi, msg in retrieval_log._index_by_doi(retrieval_log._logged_payloads(d.name)).items():
        row = q("SELECT ref_id FROM evidence_sources WHERE lower(doi)=?", doi)
        if row and retrieval_log.repeated_author_name(msg.get("author", [])):
            MAL = (d.name, row[0][0])


def verify_out(session):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        retrieval_log.verify_authors(session)
    return buf.getvalue()


def sections(out, ref):
    """(listed as MALFORMED-PAYLOAD, listed as an AUTHORS cross) for `ref`."""
    mal = out.split("MALFORMED-PAYLOAD", 1)[1] if "MALFORMED-PAYLOAD" in out else ""
    return ref in mal, any(ln.startswith(f"  ✗ {ref}") for ln in out.splitlines())


if MAL:
    r = refusal(db.correct_source, MAL[1], ["authors"], session=S, log_session=MAL[0], dry_run=True)
    record("C01", "correct-source refuses authors from a payload that repeats a name",
           r and "repeat" in r, r)
    out = verify_out(MAL[0])
    record("C02", "--verify-authors reports an intact byline behind it as MALFORMED, not as a cross",
           sections(out, MAL[1]) == (True, False), out[-600:])
    with scratch() as c:
        # HAND: damage the byline (delete its last author); no writer removes one author.
        c.execute("DELETE FROM evidence_source_authors WHERE ref_id=? AND position=(SELECT MAX(position) "
                  "FROM evidence_source_authors WHERE ref_id=?)", (MAL[1], MAL[1]))
        c.commit()
        out = verify_out(MAL[0])
    record("C04", "...and a DAMAGED byline behind the same malformed deposit is both MALFORMED and a "
                  "cross (R2-4: the human authors are still compared)",
           sections(out, MAL[1]) == (True, True), out[-600:])
else:
    record("C01", "fixture: a logged payload that repeats an author name, for a source we hold", False,
           "none in the tracked log")
r = refusal(db.correct_source, FULL_REF, ["journal_name", "no_such_field"], session=S,
            log_session="x", dry_run=True)
record("C03", "correct-source names every payload-backed field it can rewrite",
       r and "journal_name" in r and "isbn" in r, r)

# ─────────────────────────── Unit A2: research and synthesis writers ───────────────────────────
print("Section B/A13: log-search names what it searched, in the vocabulary the map holds")
sys.path.insert(0, str(REPO))
from schemas.enums import JurisdictionCode  # noqa: E402
ENUM = {e.value for e in JurisdictionCode}
# A pair the research scope owes (v_research_scope), and a language the map holds that the scope
# does not pair with that jurisdiction.
PAIR = next(r for r in q("SELECT language, jurisdiction FROM v_research_scope ORDER BY 1, 2")
            if r["jurisdiction"] in ENUM)
LANG, JUR = PAIR["language"], PAIR["jurisdiction"]
OTHER_LANG = next(r[0] for r in q("SELECT DISTINCT language FROM lang_jur_map WHERE language NOT IN "
                                  "(SELECT language FROM v_research_scope WHERE jurisdiction=?)", JUR))
P_ACTIVE = [r[0] for r in q("SELECT parameter_id FROM base_parameters WHERE status='active' "
                            "ORDER BY parameter_id")]
P1, P2, P_LAST = P_ACTIVE[0], P_ACTIVE[1], P_ACTIVE[-1]
db.retire_parameter(P_LAST, "fixture: a retired target", session=S)
P_RET = P_LAST


def search(**over):
    base = {"slug": SLUG, "language": LANG, "query_text": "q", "engine": "web",
            "depth_method": "scoping", "session": S, "prior_expectation": "nothing",
            "jurisdiction": JUR, "dry_run": True}
    base.update(over)
    return base


r = refusal(db.log_search, **search(slug="no-such-slug"))
record("B01", "log-search refuses an unknown slug by name (not a FOREIGN KEY traceback)",
       r and "slugs" in r, r)
r = refusal(db.log_search, **search(language="ZZ"))
record("J01", "log-search refuses a language lang_jur_map does not hold", r and "lang_jur_map" in r, r)
def scope_flag(lang):
    """`in_research_scope` as the operator reads it: the JSON `log-search --dry-run` prints."""
    p = cli("log-search", "--slug", SLUG, "--language", lang, "--jurisdiction", JUR, "--query-text", "q",
            "--engine", "web", "--depth-method", "scoping", "--prior-expectation", "nothing",
            "--session", S, "--dry-run")
    try:
        return json.loads(p.stdout).get("in_research_scope")
    except ValueError:
        return p.stdout + p.stderr


r = refusal(db.log_search, **search(language=OTHER_LANG))
record("J02", f"a real search in a declared jurisdiction is not refused for its pairing "
              f"({OTHER_LANG}, {JUR}); the CLI reports in_research_scope False beside True for "
              f"({LANG}, {JUR})", r is None and scope_flag(OTHER_LANG) is False
       and scope_flag(LANG) is True, (r, scope_flag(OTHER_LANG), scope_flag(LANG)))
r = refusal(db.log_search, **search(slug=None, parameter_id=P_RET))
record("J03", "refuses --parameter naming a retired parameter", r and "active" in r, r)
res, err = ok(db.log_search, **search())
record("J04", "a search in a map pair on an active slug is accepted", res is not None, err)
eid, err = ok(db.log_search, **search(language=LANG.lower(), dry_run=False))
stored = q("SELECT language FROM search_executions WHERE exec_id=?", eid)[0][0] if eid else None
record("J05", "log-search --language in lower case lands upper case (the map holds upper case)",
       stored == LANG, err or stored)

print("Section A8/B2/B3: connections -- derived id, arity, no duplicate, live targets")
NEXT_CON = db._next_con_id(con)                    # read before the first write, never typed


def conn_(**over):
    base = {"status": "PENDING", "confidence": "HIGH", "connection_type": "CROSS-PARAMETER",
            "filed_in": SLUG, "description": "fixture", "source_skill": "connection-discovery",
            "opus_reviewed": 0}
    base.update(over)
    return base


r = refusal(db.insert_connection, conn_(con_id=far(NEXT_CON)), [("parameter_id", P1), ("parameter_id", P2)],
            session=S, dry_run=True)
record("N01", "add-connection refuses a hand-typed --con-id that is not the next id", r and "next" in r, r)
r = refusal(db.insert_connection, conn_(confidence="SPECULATIVE"),
            [("parameter_id", P1), ("parameter_id", P2)], session=S, dry_run=True)
record("N02", "SPECULATIVE is refused by the column's own CHECK (migration 122)", r and "CHECK" in r, r)
r = refusal(db.insert_connection, conn_(), [("parameter_id", P1)], session=S, dry_run=True)
record("N03", "CROSS-PARAMETER with one parameter target is refused", r and "two" in r, r)
r = refusal(db.insert_connection, conn_(), [("parameter_id", P1), ("parameter_id", P_RET)],
            session=S, dry_run=True)
record("N04", "a retired parameter is refused as a target", r and "active" in r, r)
res, err = ok(db.insert_connection, conn_(), [("parameter_id", P1), ("parameter_id", P2)],
              session=S, dry_run=False)
record("N05", "a well-formed connection lands with a derived id", res == NEXT_CON, err or res)
r = refusal(db.insert_connection, conn_(description="again"),
            [("parameter_id", P2), ("parameter_id", P1)], session=S, dry_run=True)
record("N06", "the same type and target set again is a duplicate, refused", r and "duplicate" in r, r)
r = refusal(db.update_connection_status, NEXT_CON, "BANANA", session=S, dry_run=True)
record("N07", "update-connection refuses a status outside the CHECK, naming the set",
       r and "CHECK" in r, r)
ABSENT_CON = far(NEXT_CON)
r = refusal(db.update_connection_status, ABSENT_CON, "CONSUMED", session=S, dry_run=True)
record("N08", "update-connection refuses an unknown con_id", r and ABSENT_CON in r, r)
res, err = ok(db.update_connection_status, NEXT_CON, "CONSUMED", session=S, dry_run=True)
record("N09", "a CHECK status on a live connection is accepted", err is None, err)

print("Section B4/B5/D4: conflicts -- keyed on the parameter, an unordered pair")
CODES = [r[0] for r in q("SELECT identity_code FROM base_taxonomy_identity WHERE identity_code<>'ALL' "
                         "ORDER BY identity_code DESC LIMIT 2")]
HI, LO = CODES[0], CODES[1]           # HI sorts after LO
GAP = q("SELECT gap_id FROM gaps WHERE status LIKE 'OPEN%' ORDER BY gap_id LIMIT 1")[0][0]
CONF = db.next_conf_id()


def conf(**over):
    # `domain` is a free-text column; the label is a fixture, not a code from the old matrix.
    base = {"conflict_id": CONF, "domain": "fixture-domain", "pop_a": HI, "pop_b": LO,
            "status": "ACTIVE", "source_skill": "cross-population-conflict-mapper",
            "parameter_id": P1}
    base.update(over)
    return base


r = refusal(db.insert_conflict, conf(pop_a=HI, pop_b=HI), session=S, dry_run=True)
record("K01", "add-conflict refuses a population against itself, in words", r and "itself" in r, r)
r = refusal(db.insert_conflict, conf(parameter_id=None), session=S, dry_run=True)
record("K02", "add-conflict refuses with no --parameter-id (keyed on the parameter)",
       r and "parameter" in r, r)
r = refusal(db.insert_conflict, conf(parameter_id=P_RET), session=S, dry_run=True)
record("K03", "refuses a retired parameter", r and "active" in r, r)
res, err = ok(db.insert_conflict, conf(), session=S, dry_run=False)
stored = q("SELECT pop_a, pop_b, parameter_id FROM conflicts WHERE conflict_id=?", CONF)
record("K04", f"({HI}, {LO}) lands ordered ({LO}, {HI}) with its parameter",
       stored and tuple(stored[0]) == (LO, HI, P1), err or stored)
ABSENT_GAP, ABSENT_CONF = far(q("SELECT gap_id FROM gaps WHERE gap_id GLOB 'GAP-[0-9]*' ORDER BY "
                                  "CAST(SUBSTR(gap_id,5) AS INTEGER) DESC LIMIT 1")[0][0]), far(CONF)
r = refusal(db.update_conflict, CONF, session=S, gap_id=ABSENT_GAP, dry_run=True)
record("K05", "update-conflict refuses an unknown gap by name", r and ABSENT_GAP in r, r)
r = refusal(db.update_conflict, ABSENT_CONF, session=S, status="CLOSED", dry_run=True)
record("K06", "update-conflict refuses an unknown conflict", r and ABSENT_CONF in r, r)
res, err = ok(db.update_conflict, CONF, session=S, gap_id=GAP, dry_run=True)
record("K07", "a live gap is accepted", err is None, err)
rows = db.get_conflicts(parameter_id=P1)
record("K08", "db.py conflicts --parameter-id reads the key back",
       [x["conflict_id"] for x in rows] == [CONF], rows)

print("Section A16: a mining attempt records at least one strategy")
r = refusal(db.add_gap_mining, gap_id=GAP, search_strategy_record='{"strategies":[]}',
            candidates_returned=0, candidates_reviewed=0, outcome="null_result",
            discoveries_logged=[], candidate_dois=[], check_method="composite", notes=None,
            session=S, dry_run=True)
record("M01", "add-gap-mining refuses an empty strategies list", r and "strateg" in r, r)
res, err = ok(db.add_gap_mining, gap_id=GAP,
              search_strategy_record='{"strategies":[{"tool":"pubmed","query":"q","candidates_returned":0}]}',
              candidates_returned=0, candidates_reviewed=0, outcome="null_result",
              discoveries_logged=[], candidate_dois=[], check_method="composite", notes=None,
              session=S, dry_run=True)
record("M02", "a strategy record naming one search is accepted", err is None, err)

print("Section A9: the next reference id is computed, never typed")
NEXT = dbcore.next_ref_id(con)
r = refusal(db.insert_locator, {"ref_id": far(NEXT), "title": "t", "recovered_from": "f",
                                "status": "REFERENCE-ONLY"}, session=S, dry_run=True)
record("I01", "add-locator refuses a ref_id that is not next-id ref", r and NEXT in r, r)
res, err = ok(db.insert_locator, {"ref_id": NEXT, "title": "t", "recovered_from": "f",
                                  "status": "REFERENCE-ONLY"}, session=S, dry_run=False)
record("I02", "add-locator accepts the next id (staged)", err is None, err)
AUTH = db.parse_author_flags(["corp|Fixture Body"])
r = refusal(db.insert_evidence_source, {"ref_id": far(NEXT), "year": 2020, "title": "t",
                                        "evidence_type": "code", "scope": "intrinsic"},
            S, dry_run=True, authors=AUTH)
record("I03", "add-source refuses a hand-typed ref_id above the high-water mark", r and "next-id" in r, r)
res, err = ok(db.insert_evidence_source, {"ref_id": NEXT, "year": 2020, "title": "t",
                                          "evidence_type": "code", "scope": "intrinsic"},
              S, dry_run=True, authors=AUTH)
record("I04", "add-source accepts the id its own locator staged (promotion)", err is None, err)
LOC = {"title": "t", "recovered_from": "f", "status": "REFERENCE-ONLY"}
SRC = {"year": 2020, "title": "t", "evidence_type": "code", "scope": "intrinsic"}
want = dbcore.next_ref_id(con)
got, err = ok(db.insert_locator, dict(LOC), session=S, dry_run=False)
record("I05", "add-locator with no ref_id lands as dbcore.next_ref_id (R2-9)", got == want, err or (got, want))
want = dbcore.next_ref_id(con)
got, err = ok(db.insert_evidence_source, dict(SRC), S, dry_run=False, authors=AUTH)
record("I06", "add-source with no ref_id lands as the next id", got == want, err or (got, want))
r1 = refusal(db.insert_evidence_source, dict(SRC, ref_id=far(want)), S, dry_run=True, authors=AUTH)
r2 = refusal(db.insert_locator, dict(LOC, ref_id=far(want)), session=S, dry_run=True)
record("I07", "a given id that is not the computed one is still refused, naming the flag to omit",
       r1 and r2 and "omit --ref-id" in r1 and "omit --ref-id" in r2, (r1, r2))

print("Section C8: coverage counts what the vocabulary admits and the scope records")
r = refusal(db.get_coverage_completeness, "no-such-slug")
record("G01", "coverage refuses an unknown slug instead of answering zeros", r and "slugs" in r, r)
cov = db.get_coverage_completeness(SLUG)
n_req = q("SELECT COUNT(*) FROM v_research_scope")[0][0]
n_open = q("SELECT COUNT(*) FROM v_coverage_priority WHERE slug=?", SLUG)[0][0]
unreach = sorted(j for (j,) in q("SELECT DISTINCT jurisdiction FROM v_research_scope") if j not in ENUM)
record("G02", "coverage reads required from v_research_scope and unsearched from v_coverage_priority, "
              "and names the owed jurisdictions the declared vocabulary refuses (never complete while "
              "one stands, R2-1, owner question 5)",
       cov.get("pairs_required") == n_req and len(cov.get("pairs_unsearched", ())) == n_open
       and cov.get("pairs_searched", -1) + n_open == n_req and cov["jurisdictions_unreachable"] == unreach
       and (not unreach or (cov["complete"] is False and "unreachable_note" in cov))
       and "scope_recorded" not in cov, cov)
with scratch() as c:
    # HAND: the partial scope fill, taken to its limit -- every row out of scope but one that is
    # still unsearched for this slug -- then to nothing.
    keep = c.execute("SELECT language, jurisdiction FROM v_coverage_priority WHERE slug=? LIMIT 1",
                     (SLUG,)).fetchone()
    c.execute("UPDATE lang_jur_map SET scope_status='scoped-out' WHERE NOT (language=? AND jurisdiction=?)",
              (keep[0], keep[1]))
    c.commit()
    one = db.get_coverage_completeness(SLUG)
    c.execute("UPDATE lang_jur_map SET scope_status='scoped-out'")
    c.commit()
    none = db.get_coverage_completeness(SLUG)
record("G03", "all but one map row scoped-out leaves required at one, not zero, and not complete",
       one.get("pairs_required") == 1 and one["complete"] is False, one)
record("G04", "an empty requirement is never complete (it examined nothing)",
       none.get("pairs_required") == 0 and none["complete"] is False, none)
_, err = ok(db.log_search, **search(language=OTHER_LANG, dry_run=False))
after = db.get_coverage_completeness(SLUG)
record("G05", "a real search outside the owed scope is logged and counted apart (R2-2), not refused",
       err is None and after.get("searches_outside_scope", -1) == cov.get("searches_outside_scope", -2) + 1,
       err or (cov, after))

print("Section E6: mining verbs speak in ref_ids")
UM_SLUG = q("SELECT l.slug FROM source_slug_links l JOIN evidence_sources e USING (ref_id) WHERE "
            "COALESCE(e.citation_mining_status,'')<>'mined' LIMIT 1")[0][0]
um = db.get_unmined_sources(UM_SLUG)
record("U01", "unmined rows carry the global ref_id", bool(um) and "ref_id" in um[0], um[:1])
r = refusal(db.is_mined, SLUG, "11")
record("U02", "is-mined refuses a --ref that is not a reference id", r and "REF-" in r, r)
r = refusal(db.log_mining, SLUG, "11", "backward", session=S, dry_run=True, notes="x")
record("U03", "log-mining refuses the same", r and "REF-" in r, r)

print("Section C4: an unretrievable source is BLOCKED in the ledger, not NOT-READ")
NEXT2 = dbcore.next_ref_id(con)
res, err = ok(db.insert_evidence_source, {"ref_id": NEXT2, "year": 2020, "title": "blocked",
                                          "evidence_type": "code", "scope": "intrinsic",
                                          "verification_status": "UNVERIFIED",
                                          "processing_blocked_reason": OBSTACLE},
              S, dry_run=False, authors=AUTH)
led = q("SELECT status, COUNT(*) FROM v_scan_ledger WHERE ref_id=? GROUP BY 1", NEXT2)
record("Q01", "add-source writes an obstacle as processing_blocked_reason and the ledger shows BLOCKED",
       err is None and {x[0] for x in led} == {"BLOCKED"}, err or led)

print("Section R2-3: a block reason is an obstacle the ledger classes, two reasons are copies, a reading clears it")
for i, v in enumerate(COPY_VALUES, 1):
    r = refusal(db.insert_evidence_source, dict(SRC, verification_status="UNVERIFIED",
                                                processing_blocked_reason=v), S, dry_run=True, authors=AUTH)
    home = COPY_HOME[v]
    record(f"P0{i}", f"add-source refuses processing_blocked_reason {v!r}, naming its typed home {home!r}",
           r and v in r and home in r and "Nothing was written" in r, r)
with scratch() as c:
    ref = dbcore.next_ref_id(c)
    _, err = ok(db.insert_evidence_source, dict(SRC, ref_id=ref, verification_status="UNVERIFIED"), S,
                dry_run=False, authors=AUTH)
    _, err2 = ok(db.amend_source, ref, "processing_blocked_reason", OBSTACLE, "fixture: could not be read",
                 session=S)
    n_block = c.execute("SELECT COUNT(*) FROM v_scan_ledger WHERE ref_id=? AND status='BLOCKED'",
                        (ref,)).fetchone()[0]
    record("P03", f"amend-source --field processing_blocked_reason sets an obstacle ({OBSTACLE!r}) after "
                  f"admission and the ledger reads BLOCKED", err2 is None and n_block > 0, err or err2)
    r = refusal(db.amend_source, ref, "processing_blocked_reason", COPY_VALUES[0], "x", session=S,
                dry_run=True)
    record("P04", "...and refuses a copy value there too", r and COPY_VALUES[0] in r
           and "Nothing was written" in r, r)
    sha = held_text(LOG3, ref, "Fixture text with no page markers.")
    with log_root(LOG3):
        out, err = ok(db.record_scan, {"ref_id": ref, "mode": "catalogue", "text_scope": "partial",
                                       "file_sha256": sha, "method": "full-read"}, S)
    left = c.execute("SELECT processing_blocked_reason FROM evidence_sources WHERE ref_id=?",
                     (ref,)).fetchone()[0]
    record("P05", "record-scan on that source clears the reason and says block_cleared (a reading of held "
                  "bytes proves the block lifted)", out and out.get("block_cleared") == OBSTACLE
           and left is None, err or (out, left))

print("Section R2-4/5/6: a `full` claim is checked against what the document is; the exemption is refused where a body is held")
# The test decides what each fixture source holds: PAGED_REF a derived text with no page markers and a
# Crossref-shaped payload stating pages; PLAIN_REF the same text and no payload at all.
PAGES = "12-34"
SHA_PAGED = held_text(LOG3, PAGED_REF, "Fixture: a landing record with no page markers.", payload={"page": PAGES})
SHA_PLAIN = held_text(LOG3, PLAIN_REF, "Fixture: the single page of a code section.")


def scan(ref, sha, scope):
    return {"ref_id": ref, "mode": "catalogue", "text_scope": scope, "file_sha256": sha,
            "method": "full-read"}


with log_root(LOG3):
    page_range = getattr(retrieval_log, "payload_page_range", lambda ref: "no such function")
    got = [page_range(x) for x in (PAGED_REF, PLAIN_REF, far(PAGED_REF))]
    bodies = retrieval_log.decodable_body_artefacts(PAGED_REF)
    record("R01", "payload_page_range returns the deposit's page string, and None where no payload states "
                  "one (a source without a payload, an unknown id)", got == [PAGES, None, None], got)
    record("R02", "a derived text is a decodable body by the manifest's `derived` flag, not by a `-full-text.txt` "
                  "suffix", len(bodies) == 1 and bodies[0].endswith("-text.txt")
           and not bodies[0].endswith("-full-text.txt"), bodies)
    r = refusal(db.record_scan, scan(PAGED_REF, SHA_PAGED, "full"), session=S, dry_run=True)
    record("F01", "record-scan --text-scope full over a page-less text is refused when the source's own "
                  "payload states pages, naming the range", r and PAGES in r and "payload" in r, r)
    res, err = ok(db.record_scan, scan(PAGED_REF, SHA_PAGED, "abstract"), session=S, dry_run=True)
    record("F02", "the same call recorded as abstract lands", res is not None, err)
    res, err = ok(db.record_scan, scan(PLAIN_REF, SHA_PLAIN, "full"), session=S, dry_run=True)
    record("F03", "full over a page-less text lands for a source no deposit describes as paged", res is not None, err)
    r = refusal(db.observe_term, {"ref_id": PAGED_REF, "surface_form": "clause", "locator": "p1",
                                  "context_quote": "a clause typed from memory",
                                  "verbatim_exempt": "page read from an image"}, S, dry_run=True)
    record("X04", "observe-term refuses --verbatim-exempt when a decodable body is held, naming it "
                  "(the refusal add-extraction already applied, R2-6)", r and bodies and bodies[0] in r, r)

# ─────────────────────────── Round 2, A2: connection arity, help text, name words ───────────────────────────
print("Section R2-10/11/12: an arity row per CHECK value, help that prints the vocabulary, comparator words in names")
types = sorted(dbcore.check_values(con, "connections", "connection_type"))
record("A01", "every connection_type in the CHECK has an arity row", all(t in db._CONNECTION_ARITY for t in types),
       [t for t in types if t not in db._CONNECTION_ARITY])
victim = next(t for t in types if db._CONNECTION_ARITY[t][0] == "parameter_id")
targets = [("parameter_id", P1), ("parameter_id", P2)]
saved = dict(db._CONNECTION_ARITY)
try:
    del db._CONNECTION_ARITY[victim]            # simulate a type the CHECK gains and the dict lacks
    r = refusal(db.insert_connection, conn_(connection_type=victim), targets, session=S, dry_run=True)
finally:
    db._CONNECTION_ARITY.update(saved)
record("A02", "a type the CHECK admits and the dict lacks is refused by name", r and victim in r
       and "arity" in r and "Nothing was written" in r, r)
r = refusal(db.insert_connection, conn_(connection_type=victim), targets, session=S, dry_run=True)
record("A03", "the same type with its arity row passes", r is None, r)

FLAGS = [("add-extraction", "source_value_extractions", c) for c in
         ("claim_type", "extraction_method", "extraction_status", "root_type", "measurement_paradigm")]
FLAGS += [("add-candidate", "search_candidates", "disposition"),
          ("resolve-candidate", "search_candidates", "disposition"),
          ("add-code-lead", "research_code_leads", "status"),
          ("add-population-match", "evidence_population_match", "match_grade"),
          ("update-locator", "source_locators", "status"), ("add-locator", "source_locators", "status")]
for i, (verb, table, column) in enumerate(FLAGS, 1):
    vals = sorted(dbcore.check_values(con, table, column))
    shown = re.sub(r"\s+", "", cli(verb, "--help").stdout)       # argparse wraps its choice list
    missing = [v for v in vals if v not in shown]
    record(f"O{i:02d}", f"{verb} --help prints every value of {table}.{column}", vals and not missing, missing)
rels = sorted(dbcore.check_values(con, "extraction_relations", "relation"))
shown = re.sub(r"\s+", "", cli("add-extraction", "--help").stdout)
record("O12", "add-extraction --relation help prints every relation value and the literal 'none'",
       all(v in shown for v in rels) and "literal'none'" in shown, [v for v in rels if v not in shown])
bad = cli("update-locator", "--ref-id", NEXT, "--status", "not-a-status", "--session", S, "--dry-run")
record("O13", "argparse itself refuses a status outside the CHECK and lists the set", bad.returncode != 0
       and "invalid choice" in bad.stderr
       and all(v in bad.stderr for v in dbcore.check_values(con, "source_locators", "status")), bad.stderr[-200:])

obs_ = q("SELECT observation_id FROM observed_terms WHERE context_quote IS NOT NULL LIMIT 1")[0][0]
for i, (name, word) in enumerate([("not steeper than", "than"), ("at least one landing", "at least"),
                                  ("no more landings", "no more"), ("not exceeding landings", "not exceeding"),
                                  ("exceeds landings", "exceeds")], 1):
    r = refusal(db.insert_term, obs_, name, "probe", session=S, dry_run=True)
    record(f"Z0{i}", f"add-term refuses the name {name!r}, naming {word!r}", r and f"'{word}'" in r.lower(), r)
live = [t for (t,) in q("SELECT canonical_en FROM terms")]
two = next(t for t in live if " " in t)
r = refusal(db.insert_term, obs_, two + " fixtureword", "probe", session=S, dry_run=True)
record("Z07", "a plain multi-word name is not refused by the value-bearing rule",
       r is None or "carries a number" not in r, r)
# A description is prose: the comparator words guard NAMES only (a definition says "rather than").
r = refusal(db.insert_medical, "MD-FIXTURE", "Fixture condition", "6A02", S,
            description="Affects more than one limb, no more than mild", dry_run=True)
record("Z08", "a description with 'than' and 'no more' is not refused for its words (it is refused later, for "
              "its missing crossing, which this case does not supply)", r is None or "--description" not in r, r)
r = refusal(db.insert_medical, "MD-FIXTURE", "Fixture condition", "6A02", S,
            description="Grade 3 impairment", dry_run=True)
record("Z09", "...and a description with a number still is", r and "--description" in r, r)
r = refusal(db.insert_medical, "MD-FIXTURE", "not steeper than", "6A02", S, dry_run=True)
record("Z10", "...while the same words in the display name are refused", r and "'than'" in r, r)
record("Z06", "no live term name is caught by the widened name rule (it would strand the vocabulary)",
       not [t for t in live if db._VALUE_BEARING_NAME.search(t)],
       [t for t in live if db._VALUE_BEARING_NAME.search(t)])

# ─────────────────────────── Round 2, C: gates and the engine ───────────────────────────
print("Section C: the engine names a missing direction and a slug it does not hold; the verified-scan "
      "reader examines every live extraction; the skill-vocabulary audit can go red")
ICF = q("SELECT icf_code FROM base_icf LIMIT 1")[0][0]


def assess(db_path, pid, slug, *extra):
    return subprocess.run([sys.executable, str(REPO / "scripts/assess/assess_cell.py"), "--db", db_path,
                           "--emit-sql", os.path.join(TMP, "a.sql"), "--parameter-id", str(pid),
                           "--slug", slug, "--identity", IDENT, "--icf", ICF, "--session", S,
                           "--stamp", "2026-11-06T00:00:00Z", *extra],
                          capture_output=True, text=True, env=dict(os.environ))


P_NODIR = q("SELECT parameter_id FROM base_parameters WHERE status='active' AND "
            "accessibility_direction IS NULL AND parameter_id IN (SELECT parameter_id FROM "
            "source_value_extractions) AND parameter_id<>? ORDER BY 1 LIMIT 1", P_FULL)
CELL_P = P_NODIR[0][0] if P_NODIR else P1
# Before E01 writes that cell to the test copy, so the accepted call below is not a duplicate.
with scratch() as c:
    path = os.environ["GUIDEBOOK_DB_PATH"]
    held = lambda: tuple(c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]  # noqa: E731
                         for t in ("specifications", "gaps"))
    before = held()
    r = assess(path, CELL_P, SLUG + "-absent")
    record("E05", "assess_cell refuses a slug that is not in `slugs`, naming the table, and writes no row (R2-7)",
           r.returncode != 0 and "slugs" in r.stdout + r.stderr and held() == before,
           (r.stdout + r.stderr)[-300:])
    r = assess(path, CELL_P, SLUG)
    record("E06", "...and the same call with a slug it holds is accepted", r.returncode == 0,
           (r.stdout + r.stderr)[-300:])
if P_NODIR:
    rj = os.path.join(TMP, "assess.json")
    r = assess(DB, P_NODIR[0][0], SLUG, "--report-json", rj)
    rep = json.load(open(rj))[0] if r.returncode == 0 else {}
    gap = q("SELECT description FROM gaps WHERE gap_id=?", rep.get("gap_register_id") or "")
    record("E01", "a pending cell with no direction records set-parameter-direction in its gap",
           r.returncode == 0 and gap and "set-parameter-direction" in gap[0][0],
           (r.stdout + r.stderr)[-300:] if r.returncode else (gap[0][0][-200:] if gap else "no gap"))
    record("E02", "the summary line prints every lens the cell was given",
           f"param {P_NODIR[0][0]}×{IDENT}/" in r.stdout, r.stdout[:120])
    record("E03", "the report carries direction_ref_id beside the direction",
           "direction_ref_id" in rep, list(rep)[:5])
else:
    record("E01", "fixture: an active direction-less parameter with extractions", False, "none in the copy")
# The verified-scan reader: independent oracle (SQL over the base tables), not the script's own query.
LIVE = ("FROM source_value_extractions x JOIN evidence_sources e USING (ref_id) JOIN base_parameters p "
        "USING (parameter_id) WHERE e.superseded_by_ref_id IS NULL AND p.status='active'")
COVER = ("EXISTS (SELECT 1 FROM source_scans s WHERE s.ref_id=x.ref_id{full} AND ((s.mode='catalogue' AND "
         "s.catalogue_version>=x.parameter_id) OR (s.mode='targeted' AND s.target_parameter_id=x.parameter_id)))")
CLASSES = {"VERIFIED-WITHOUT-FULL-READING": "x.extraction_status='verified' AND NOT " +
           COVER.format(full=" AND s.text_scope='full'"),
           "SOURCE-NOT-VERIFIED": "COALESCE(e.verification_status,'')<>'VERIFIED'",
           "NO-COVERING-READING": "NOT " + COVER.format(full="")}


def integrity(db_path):
    """(exit code, EXAMINED, {class: (row count, {ref_id}))) from the script's own output."""
    r = subprocess.run([sys.executable, str(REPO / "scripts/audit/verified_scan_integrity.py")],
                       capture_output=True, text=True, env=dict(os.environ, GUIDEBOOK_DB_PATH=db_path))
    got, cur = {k: (0, set()) for k in CLASSES}, None
    for ln in r.stdout.splitlines():
        m = re.match(r"  ([A-Z-]+): (\d+) row\(s\)", ln)
        if m:
            cur = got[m.group(1)] = (int(m.group(2)), set())
        elif cur and (m := re.match(r"    (REF-\w+):", ln)):
            cur[1].add(m.group(1))
    ex = re.search(r"EXAMINED: (\d+)", r.stdout)
    return r.returncode, int(ex.group(1)) if ex else None, got


want = {k: q(f"SELECT COUNT(*) {LIVE} AND ({w})")[0][0] for k, w in CLASSES.items()}
rc, ex, got = integrity(DB)
record("E04", "verified_scan_integrity examines every live extraction and reports each of its three "
              "classes with the count the base tables give (R2-15); it fails iff one is non-empty",
       ex == q(f"SELECT COUNT(*) {LIVE}")[0][0] and {k: v[0] for k, v in got.items()} == want
       and rc == (1 if any(want.values()) else 0), (rc, ex, got, want))
# A live source, VERIFIED, every live row of it covered by some reading: in no class today.
clean = q(f"SELECT x.ref_id {LIVE} AND e.verification_status='VERIFIED' AND x.ref_id NOT IN (SELECT x.ref_id "
          f"{LIVE} AND ({CLASSES['NO-COVERING-READING']})) LIMIT 1")[0][0]
rows_of = q(f"SELECT COUNT(*) {LIVE} AND x.ref_id=?", clean)[0][0]
with scratch() as c:
    # HAND: an unverified source, and (separately) one whose readings are gone; no writer builds either
    # over a source that already holds extractions (add-extraction refuses both at write time).
    c.execute("UPDATE evidence_sources SET verification_status='UNVERIFIED' WHERE ref_id=?", (clean,))
    c.commit()
    _, _, got1 = integrity(os.environ["GUIDEBOOK_DB_PATH"])
    c.execute("UPDATE evidence_sources SET verification_status='VERIFIED' WHERE ref_id=?", (clean,))
    c.execute("DELETE FROM source_scans WHERE ref_id=?", (clean,))
    c.commit()
    _, _, got2 = integrity(os.environ["GUIDEBOOK_DB_PATH"])
record("E07", "an extraction whose source is not VERIFIED is listed under SOURCE-NOT-VERIFIED (R2-15)",
       clean in got1["SOURCE-NOT-VERIFIED"][1] and got1["SOURCE-NOT-VERIFIED"][0]
       == want["SOURCE-NOT-VERIFIED"] + rows_of, (clean, got1))
record("E08", "an extraction no reading covers is listed under NO-COVERING-READING (R2-15)",
       clean in got2["NO-COVERING-READING"][1] and got2["NO-COVERING-READING"][0]
       == want["NO-COVERING-READING"] + rows_of, (clean, got2))

# skill_vocabulary_audit (advisory; red on prior-version skills): the five retired names must be
# reported; a derived column, CHECK value and verb, and an unticked prose word, must not be.
fx = pathlib.Path(TMP) / "vocab"
(fx / "red").mkdir(parents=True)
(fx / "green").mkdir()
POISON = ("item_code", "E-08", "axis_code", "population_code", "mode_s_trigger")    # retired by ruling
(fx / "red" / "red.md").write_text("Red fixture. " + ", ".join(f"`{t}`" for t in POISON) + ".\n")
verbs = re.search(r"\{([^}]+)\}", re.sub(r"\s+", "", cli("--help").stdout)).group(1).split(",")
col = [r[1] for r in con.execute("PRAGMA table_info(base_parameters)")][1]
(fx / "green" / "green.md").write_text(f"Green fixture. Read `{col}`, use `{OBSTACLE}`, run "
                                       f"`{next(v for v in verbs if '-' in v)}`; the prose word HIGH-IMPACT "
                                       f"has no ticks.\n")


def vocab(d):
    return subprocess.run([sys.executable, str(REPO / "scripts/audit/skill_vocabulary_audit.py"), "--paths",
                           str(fx / d)], capture_output=True, text=True)


red, green = vocab("red"), vocab("green")
record("E09", "skill_vocabulary_audit reports every retired name a skill backticks (R2-16)",
       red.returncode != 0 and all(t in red.stdout for t in POISON), red.stdout[-300:])
record("E10", "...and reports nothing for a live column, a CHECK value, a verb and a prose word",
       green.returncode == 0 and re.search(r"EXAMINED: [1-9]", green.stdout) is not None, green.stdout[-300:])

con.close()
n = len(results)
print(f"\nEXAMINED: {n} cases")
print(f"FAILED: {results.count(False)}" if not all(results) else f"PASS: all {n} cases")
sys.exit(0 if all(results) else 1)
