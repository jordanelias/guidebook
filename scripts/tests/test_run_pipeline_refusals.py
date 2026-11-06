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


def extraction(ref, pid, **over):
    base = {"ref_id": ref, "parameter_id": pid, "identity_code": "MOB",
            "claim_type": "numerical", "claimed_value": VALUE, "claimed_unit": "mm",
            "claim_text": QUOTE, "extraction_method": "full-read", "figure_role": "claim",
            "source_section": "section 3", "loc_section": "3"}
    base.update(over)
    return base


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
import hashlib  # noqa: E402
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
mal = q("SELECT ref_id FROM evidence_sources WHERE doi='10.5038/2375-0901.19.2.7'")
if mal:
    r = refusal(db.correct_source, mal[0][0], ["authors"], session=S,
                log_session="session_2026-10-30-ramp-spec-pages-rebuild", dry_run=True)
    record("C01", "correct-source refuses authors from a payload that repeats a name",
           r and "repeat" in r, r)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        retrieval_log.verify_authors("session_2026-10-30-ramp-spec-pages-rebuild")
    out = buf.getvalue()
    record("C02", "--verify-authors reports it as MALFORMED, not as a cross",
           "MALFORMED" in out and f"✗ {mal[0][0]}\n" not in out, out[-600:])
else:
    record("C01", "fixture source for the malformed payload is present", False, "REF missing")
r = refusal(db.correct_source, FULL_REF, ["journal_name", "no_such_field"], session=S,
            log_session="x", dry_run=True)
record("C03", "correct-source names every payload-backed field it can rewrite",
       r and "journal_name" in r and "isbn" in r, r)

# ─────────────────────────── Unit A2: research and synthesis writers ───────────────────────────
print("Section B/A13: log-search names what it searched, in the vocabulary the map holds")
SLUG = q("SELECT slug FROM slugs WHERE status='ACTIVE' ORDER BY slug LIMIT 1")[0][0]
sys.path.insert(0, str(REPO))
from schemas.enums import JurisdictionCode  # noqa: E402
ENUM = {e.value for e in JurisdictionCode}
PAIR = next(r for r in q("SELECT language, jurisdiction FROM lang_jur_map ORDER BY 1, 2")
            if r["jurisdiction"] in ENUM)
LANG, JUR = PAIR["language"], PAIR["jurisdiction"]
OTHER_LANG = next(r[0] for r in q("SELECT DISTINCT language FROM lang_jur_map WHERE language NOT IN "
                                  "(SELECT language FROM lang_jur_map WHERE jurisdiction=?)", JUR))
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
r = refusal(db.log_search, **search(language=OTHER_LANG))
record("J02", f"refuses a (language, jurisdiction) pair the map lacks ({OTHER_LANG}, {JUR})",
       r and "lang_jur_map" in r, r)
r = refusal(db.log_search, **search(slug=None, parameter_id=P_RET))
record("J03", "refuses --parameter naming a retired parameter", r and "active" in r, r)
res, err = ok(db.log_search, **search())
record("J04", "a search in a map pair on an active slug is accepted", res is not None, err)

print("Section A8/B2/B3: connections -- derived id, arity, no duplicate, live targets")


def conn_(**over):
    base = {"status": "PENDING", "confidence": "HIGH", "connection_type": "CROSS-PARAMETER",
            "filed_in": SLUG, "description": "fixture", "source_skill": "connection-discovery",
            "opus_reviewed": 0}
    base.update(over)
    return base


r = refusal(db.insert_connection, conn_(con_id="X1"), [("parameter_id", P1), ("parameter_id", P2)],
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
record("N05", "a well-formed connection lands with a derived id", res == "CON-0001", err or res)
r = refusal(db.insert_connection, conn_(description="again"),
            [("parameter_id", P2), ("parameter_id", P1)], session=S, dry_run=True)
record("N06", "the same type and target set again is a duplicate, refused", r and "duplicate" in r, r)
r = refusal(db.update_connection_status, "CON-0001", "BANANA", session=S, dry_run=True)
record("N07", "update-connection refuses a status outside the CHECK, naming the set",
       r and "CHECK" in r, r)
r = refusal(db.update_connection_status, "CON-9999", "CONSUMED", session=S, dry_run=True)
record("N08", "update-connection refuses an unknown con_id", r and "CON-9999" in r, r)
res, err = ok(db.update_connection_status, "CON-0001", "CONSUMED", session=S, dry_run=True)
record("N09", "a CHECK status on a live connection is accepted", err is None, err)

print("Section B4/B5/D4: conflicts -- keyed on the parameter, an unordered pair")
CODES = [r[0] for r in q("SELECT identity_code FROM base_taxonomy_identity WHERE identity_code<>'ALL' "
                         "ORDER BY identity_code DESC LIMIT 2")]
HI, LO = CODES[0], CODES[1]           # HI sorts after LO
GAP = q("SELECT gap_id FROM gaps WHERE status LIKE 'OPEN%' ORDER BY gap_id LIMIT 1")[0][0]


def conf(**over):
    base = {"conflict_id": "CONF-0001", "domain": "LIGHT-INT", "pop_a": HI, "pop_b": LO,
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
stored = q("SELECT pop_a, pop_b, parameter_id FROM conflicts WHERE conflict_id='CONF-0001'")
record("K04", f"({HI}, {LO}) lands ordered ({LO}, {HI}) with its parameter",
       stored and tuple(stored[0]) == (LO, HI, P1), err or stored)
r = refusal(db.update_conflict, "CONF-0001", session=S, gap_id="GAP-99999", dry_run=True)
record("K05", "update-conflict refuses an unknown gap by name", r and "GAP-99999" in r, r)
r = refusal(db.update_conflict, "CONF-9999", session=S, status="CLOSED", dry_run=True)
record("K06", "update-conflict refuses an unknown conflict", r and "CONF-9999" in r, r)
res, err = ok(db.update_conflict, "CONF-0001", session=S, gap_id=GAP, dry_run=True)
record("K07", "a live gap is accepted", err is None, err)
rows = db.get_conflicts(parameter_id=P1)
record("K08", "db.py conflicts --parameter-id reads the key back",
       [x["conflict_id"] for x in rows] == ["CONF-0001"], rows)

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
r = refusal(db.insert_locator, {"ref_id": "REF-99999", "title": "t", "recovered_from": "f",
                                "status": "REFERENCE-ONLY"}, session=S, dry_run=True)
record("I01", "add-locator refuses a ref_id that is not next-id ref", r and NEXT in r, r)
res, err = ok(db.insert_locator, {"ref_id": NEXT, "title": "t", "recovered_from": "f",
                                  "status": "REFERENCE-ONLY"}, session=S, dry_run=False)
record("I02", "add-locator accepts the next id (staged)", err is None, err)
AUTH = db.parse_author_flags(["corp|Fixture Body"])
r = refusal(db.insert_evidence_source, {"ref_id": "REF-01100", "year": 2020, "title": "t",
                                        "evidence_type": "code", "scope": "intrinsic"},
            S, dry_run=True, authors=AUTH)
record("I03", "add-source refuses a hand-typed ref_id above the high-water mark", r and "next-id" in r, r)
res, err = ok(db.insert_evidence_source, {"ref_id": NEXT, "year": 2020, "title": "t",
                                          "evidence_type": "code", "scope": "intrinsic"},
              S, dry_run=True, authors=AUTH)
record("I04", "add-source accepts the id its own locator staged (promotion)", err is None, err)

print("Section C8: coverage counts what the vocabulary admits and the scope records")
r = refusal(db.get_coverage_completeness, "no-such-slug")
record("G01", "coverage refuses an unknown slug instead of answering zeros", r and "slugs" in r, r)
cov = db.get_coverage_completeness(SLUG)
record("G02", "coverage names the map rows the declared vocabulary refuses, and whether a scope is "
              "recorded", isinstance(cov.get("jurisdictions_unreachable"), list)
       and cov.get("scope_recorded") is False and cov["jurisdictions_required"] <= 48, cov)

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
                                          "processing_blocked_reason": "paywalled"},
              S, dry_run=False, authors=AUTH)
led = q("SELECT status, COUNT(*) FROM v_scan_ledger WHERE ref_id=? GROUP BY 1", NEXT2)
record("Q01", "add-source writes processing_blocked_reason and the ledger shows BLOCKED",
       err is None and led and [tuple(x) for x in led][0][0] == "BLOCKED", err or led)

# ─────────────────────────── Unit C: gates and the engine ───────────────────────────
print("Section C: the engine names a missing direction; the verified-scan check examines rows")
import subprocess  # noqa: E402
P_NODIR = q("SELECT parameter_id FROM base_parameters WHERE status='active' AND "
            "accessibility_direction IS NULL AND parameter_id IN (SELECT parameter_id FROM "
            "source_value_extractions) AND parameter_id<>? ORDER BY 1 LIMIT 1", P_FULL)
if P_NODIR:
    rj = os.path.join(TMP, "assess.json")
    r = subprocess.run([sys.executable, str(REPO / "scripts/assess/assess_cell.py"), "--db", DB,
                        "--emit-sql", os.path.join(TMP, "a.sql"), "--parameter-id", str(P_NODIR[0][0]),
                        "--slug", SLUG, "--identity", "MOB", "--icf",
                        q("SELECT icf_code FROM base_icf LIMIT 1")[0][0], "--session", S,
                        "--stamp", "2026-11-06T00:00:00Z", "--report-json", rj],
                       capture_output=True, text=True)
    rep = json.load(open(rj))[0] if r.returncode == 0 else {}
    gap = q("SELECT description FROM gaps WHERE gap_id=?", rep.get("gap_register_id") or "")
    record("E01", "a pending cell with no direction records set-parameter-direction in its gap",
           r.returncode == 0 and gap and "set-parameter-direction" in gap[0][0],
           (r.stdout + r.stderr)[-300:] if r.returncode else (gap[0][0][-200:] if gap else "no gap"))
    record("E02", "the summary line prints every lens the cell was given",
           f"param {P_NODIR[0][0]}×MOB/" in r.stdout, r.stdout[:120])
    record("E03", "the report carries direction_ref_id beside the direction",
           "direction_ref_id" in rep, list(rep)[:5])
else:
    record("E01", "fixture: an active direction-less parameter with extractions", False, "none in the copy")
r = subprocess.run([sys.executable, str(REPO / "scripts/audit/verified_scan_integrity.py")],
                   capture_output=True, text=True, env=dict(os.environ, GUIDEBOOK_DB_PATH=DB))
n_ver = q("SELECT COUNT(*) FROM source_value_extractions x JOIN evidence_sources e USING (ref_id) "
          "JOIN base_parameters p USING (parameter_id) WHERE x.extraction_status='verified' AND "
          "e.superseded_by_ref_id IS NULL AND p.status='active'")[0][0]
record("E04", "verified_scan_integrity prints EXAMINED equal to the live verified rows and fails on one "
              "with no full-scope reading", f"EXAMINED: {n_ver}" in r.stdout and r.returncode == 1,
       r.stdout[:200])

con.close()
n = len(results)
print(f"\nEXAMINED: {n} cases")
print(f"FAILED: {results.count(False)}" if not all(results) else f"PASS: all {n} cases")
sys.exit(0 if all(results) else 1)
