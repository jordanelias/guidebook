#!/usr/bin/env python3
"""db.py's amendment writers from batch 20: every refusal proven to fire, and the
legitimate shape proven to pass.

WHY THIS EXISTS, as CLAUDE.md section 8 requires. db.py's Act-2 banner says "every refusal
here has a selftest case proving it fires AND a case proving the legitimate shape still
passes". Batch 20 (2026-09-25) added link-admission, amend-population-match, amend-term and
resolve-candidate --suggested-slug with no case at all, and a review that simply RAN them
found five defects no gate had seen:
  * link-admission refused a second admitting search, which log-search permits;
  * link-admission left results_admitted behind its own edges (exec 90 read 0 with 1 edge);
  * amend-term could never detect an unchanged scope_note, and nested each audit line
    inside the next;
  * --suggested-slug accepted a MERGED slug and a REHOME pointing at its own origin, and
    could not be required, so REHOME rows could still name no destination;
  * dbcore.fold_ref upper-cased the mixed-case Co1-NN namespace, so every writer that
    folds a ref id would have refused a genuine Co1 source.
What reaches the guidebook without these cases: a wrong provenance edge nothing can remove,
a coverage view that under-counts what searches yielded, a candidate "rehomed" nowhere, a
Co1 source that cannot be graded -- each looking fine to every gate.

Section D (migration 101, GAP-061's prerequisite) holds `decline-parameter` and the one
refusal it adds to `add-parameter` to the same standard. What reaches the guidebook
without it: a term judged NOT to be a design parameter minted as one anyway, so
extractions and determinations can key on a concept somebody already ruled out.

Section S (GAP-058) holds `add-source --slug` to "refuse before any write": a refused
admission used to leave its source and author rows committed, an orphan that is either
shipped or deleted by hand. It also holds `link-source-slug --local-ref-id`, the only way to
file into a slug whose labels mix schemes, and the refusal of a label another source holds.

Section X (GAP-060) holds `supersede-source`: without it a source admitted twice (a mirror,
a DOI-less re-entry) is gathered twice by the determination engine, and D04 stays red with
hand SQL as the only remedy. It proves D04 goes quiet on a fixture collision, that a live
determination blocks the move until it is retired, that the UPDATE reaches the capture
path, and that add-extraction, observe-term and add-population-match then refuse the
superseded source, whose rows the engine would drop.

Section C (GAP-055) holds `close-adversarial-pass`'s artefact parse: a SURVIVED artefact
written as a citation ("<file> page 15", "<file> (and the other 11)") used to make a
good-faith pass unclosable, so its audit stayed red for a pass that had done its work. A
path that escapes the repo must still refuse, and cited paths that do not resolve must stay
visible. The verb's --help must name the 2026-09-27 ruling that holds pass 1 open, and a
finding admitted only on the database file is closed but reported, because the database is
not an artefact of attack.

Section E (I1) holds `amend-source --field evidence_type`: without it a source filed at the
wrong rung of the ladder (a Co-1/T6 contradiction, a grey report typed as a trial) keeps
anchoring at the wrong strength, because the only correction was hand SQL. It proves the
tier moves with the type by derivation only, that a move to co1 needs the D-0178 warrant
and a co1_source_type from schemas.enums.Co1SourceType (grain_for grades a Co-1 source's
grain from it), that a move off co1 keeps the old warrant in the ledger and NULLs the
Co-1-only columns, and that a source a live determination rests on cannot move.

Section K (I8, GAP-005) holds `update-code-lead` and add-code-lead's near-duplicate refusal:
without the verb R15 cannot be discharged against a lead, so a lead whose document was
retrieved stays REFERENCE-ONLY and its note keeps asserting what the document was found not
to say. It proves the move is ledgered and append-only (a note that is only a substring of
the held notes is still appended), that the refusal's "update that row instead" names a
command that works, and that the duplicate key folds case and punctuation
without erasing a Korean or Japanese name.

Section J (I7) holds the declared jurisdiction vocabulary at write time: without it every
writer took any string, so an undeclared code (`PT` on batch 23's branch) reached the corpus
and the blocking `jurisdiction_db_vocabulary` audit found it only after it landed. It proves
an undeclared code, the ruled rejected spelling and a case variant are refused by each
writer of a gated table, that a code admitted in the same change is accepted, that every
value live in a gated table still passes (the refusal mirrors the audit and is not stricter),
and that the audit is green on the copy after the writers ran.

Runs on a COPY of the canonical database in a temp directory (dbcore refuses to open the
canonical file read-write). Fixtures are made through db.py's own writers. Two states no
writer can make are set by SQL on the copy, and each says why at the point it is set.
Nothing depends on a hard-coded live id: the slugs, source, population and term used are
read from the copy.
"""
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
TMP = tempfile.mkdtemp(prefix="db-amend-writers-")
DB = os.path.join(TMP, "guidebook.db")
shutil.copy(REPO / "data" / "guidebook.db", DB)
os.environ["GUIDEBOOK_DB_PATH"] = DB          # before db/dbcore resolve a path
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "scripts" / "tests"))
from _fixture_log import fixture_log_root  # noqa: E402
# T-073: read an isolated root, not the working tree's retrieval log (an untracked pre-admission folder would change a verdict)
os.environ["GUIDEBOOK_RETRIEVAL_LOG"] = fixture_log_root(os.path.join(TMP, "retrieval-log"), DB)
import db        # noqa: E402
import dbcore    # noqa: E402
from dbcore import Refusal  # noqa: E402

# T-007: add-source refuses a source with no standing or no type. Both values are read from
# the columns' own CHECKs; UNVERIFIED needs no verification method, so no other refusal fires.
# T-083: the warrant of a quantity kind is a locator held on the parameter's own row (OD-71); this one is a fixture.
KIND_WARRANT = dict(quantity_kind_source_url="https://example.org/task-fixture", quantity_kind_source_page="TASK-FIXTURE",
                    quantity_kind_quote="TASK-FIXTURE: a clear width of at least 900 mm")
SRC_STANDING = ("--verification-status", "UNVERIFIED",
                "--source-type", dbcore.schema_choices("evidence_sources", "source_type")[0])
sys.path.insert(0, str(REPO))
from schemas.enums import EvidenceMarker  # noqa: E402


def unretire(con, spec):
    """Make a retired specification live again. A live stated or provisional row must carry a
    marker (migration 116); the weakest band is legal on any such row. `reretire` undoes it."""
    con.execute("UPDATE specifications SET retired_at=NULL, marker=CASE WHEN state IN "
                "('stated','provisional') THEN ? END WHERE specification_id=?",
                (EvidenceMarker.WEAK.value, spec))

def reretire(spec, at=None, by=None, why=None):
    """Put a specification back as the canonical copy held it: retired, and unmarked (a retired
    row is exempt from the marker CHECK, and `unretire` gave it one)."""
    con = sqlite3.connect(DB)
    if at is None:
        con.execute("UPDATE specifications SET marker=NULL WHERE specification_id=?", (spec,))
    else:
        con.execute("UPDATE specifications SET retired_at=?, retired_by_session=?, "
                    "retirement_reason=?, marker=NULL WHERE specification_id=?", (at, by, why, spec))
    con.commit()
    con.close()


S = "session_test-db-amend-writers"
results = []


def record(tid, name, passed, details=""):
    results.append(bool(passed))
    print(f"  [{'✓' if passed else '✗'}] {tid}: {name}")
    if details and not passed:
        print(f"      {details}")


def refusal(fn, *a, **k):
    """The Refusal's text if `fn` refuses, else None.

    Any OTHER exception is a defect, not a refusal, and must never count as one: it is
    printed and returns None, so the assertion that expected a refusal goes red and the
    run carries on to the cases after it (fault injection showed a crash here hiding
    every later case)."""
    try:
        fn(*a, **k)
    except Refusal as exc:
        return str(exc)
    except Exception as exc:  # noqa: BLE001 -- reported, never swallowed as a pass
        print(f"      DEFECT, not a refusal: {exc.__class__.__name__}: {exc}")
    return None


def q(sql, *params):
    con = sqlite3.connect(DB)
    try:
        return con.execute(sql, params).fetchall()
    finally:
        con.close()


def w(sql, *params):
    """`q`'s write twin: one statement, committed."""
    con = sqlite3.connect(DB)
    try:
        con.execute(sql, params)
        con.commit()
    finally:
        con.close()


def exec_row(exec_id):
    return q("SELECT results_admitted, findings_note FROM search_executions "
             "WHERE exec_id=?", exec_id)[0]


def run_cli(*args):
    """db.py through argparse, on the copy. The verbs' dispatch blocks are only reached
    this way: a case that calls the function directly cannot see an unwired flag or a
    write the dispatch makes before the function is called."""
    return subprocess.run([sys.executable, str(REPO / "scripts" / "db.py"), *args],
                          env=dict(os.environ, GUIDEBOOK_DB_PATH=DB),
                          capture_output=True, text=True)


def counts(*tables):
    return tuple(q(f'SELECT COUNT(*) FROM "{t}"')[0][0] for t in tables)


try:
    (A,), (B,) = q("SELECT slug FROM slugs WHERE status='ACTIVE' ORDER BY slug LIMIT 2")
    merged = q("SELECT slug FROM slugs WHERE status='MERGED' ORDER BY slug LIMIT 1")
    MERGED = merged[0][0] if merged else None
    (REF,), (REF2,) = q("SELECT ref_id FROM evidence_sources ORDER BY ref_id LIMIT 2")
    (POP,) = q("SELECT identity_code FROM base_taxonomy_identity ORDER BY identity_code LIMIT 1")[0]
    (TERM, DEF) = q("SELECT term_id, definition FROM terms ORDER BY term_id LIMIT 1")[0]

    def search(label):
        return db.log_search(slug=A, language="EN", query_text=f"fixture: {label}",
                             engine="manual", depth_method="scoping", session=S, results_found=1,
                             prior_expectation="fixture prior, written before the call")

    def candidate(exec_id, title, disposition="PENDING-VERIFICATION", **extra):
        # RC1 (DR-2026-09-26 2.2d) made --surfaced-in required. These fixtures have no
        # real search history to link a payload to, so they use the TRANSCRIPT-ONLY
        # route against a stable, tracked sentence in transcripts/README.md.
        extra.setdefault("surfaced_in", "transcripts/README.md")
        extra.setdefault("surfaced_quote", "single home for what the agents actually did")
        return int(db.insert_search_candidate(
            dict({"exec_id": exec_id, "found_under_slug": A, "disposition": disposition,
                  "title": title, "harm_finding": 0}, **extra), S))

    E1, E2, E3 = search("one"), search("two"), search("legacy count")
    C1, C2, C3 = candidate(E1, "c1"), candidate(E2, "c2"), candidate(E3, "c3")

    # ── L: link-admission ─────────────────────────────────────────────────────
    msg = refusal(db.link_admission, E1, REF, "r", S)
    record("L01", "refuses when no candidate records (exec, ref, ADMITTED)",
           msg and "REFUSED" in msg, f"got {msg!r}")
    for c in (C1, C2, C3):
        db.resolve_candidate(c, "ADMITTED", "fixture re-description", S, admitted_ref_id=REF)
    record("L02", "refuses a blank reason",
           refusal(db.link_admission, E1, REF, "   ", S) is not None)

    out = db.link_admission(E1, REF, "fixture link", S)
    n, note = exec_row(E1)
    record("L03", "writes the edge and raises results_admitted to match it",
           out["changed"] and out["edge_added"] and n == 1
           and q("SELECT 1 FROM search_admissions WHERE exec_id=? AND ref_id=?", E1, REF)
           and "ADMISSION LINKED" in note and "RESULTS_ADMITTED RAISED" in note
           and "0 -> 1" in note, f"out={out} n={n}")
    out = db.link_admission(E1, REF, "again", S)
    record("L04", "an edge already present and level is a no-op, not a second row",
           out["changed"] is False
           and q("SELECT COUNT(*) FROM search_admissions WHERE exec_id=? AND ref_id=?",
                 E1, REF)[0][0] == 1, f"out={out}")
    out = db.link_admission(E2, REF, "second search surfaced it too", S)
    record("L05", "a SECOND admitting search is allowed, as log-search allows it",
           # E1 among the others -- not equal to [E1]: the source read from the copy may
           # already carry live admissions of its own.
           out["changed"] and E1 in out["other_admitting_execs"]
           and E2 not in out["other_admitting_execs"], f"out={out}")

    # A historical count above the edges -- the state the 2026-09-02 repair restored on
    # seven rows by design. No writer sets a count without edges (log-search refuses it),
    # so the fixture sets it directly on the copy.
    con = sqlite3.connect(DB)
    con.execute("UPDATE search_executions SET results_admitted=3 WHERE exec_id=?", (E3,))
    con.commit()
    con.close()
    db.link_admission(E3, REF, "legacy row", S)
    record("L06", "never LOWERS a historical count to agree with the edges",
           exec_row(E3)[0] == 3, f"results_admitted={exec_row(E3)[0]}")

    msg = refusal(db.link_admission, E1, "co1-99", "r", S)
    record("L07", "a Co1 id keeps its spelling through fold_ref (refused as Co1-99, "
           "not CO1-99)", msg and "Co1-99" in msg and "CO1-99" not in msg, f"got {msg!r}")

    # ── U: unlink-admission ──────────────────────────────────────────────────
    record("U01", "refuses to remove an edge that does not exist",
           refusal(db.unlink_admission, E1, REF2, "r", S) is not None)
    record("U02", "refuses a blank reason",
           refusal(db.unlink_admission, E1, REF, "", S) is not None)
    n_edges = q("SELECT COUNT(*) FROM search_admissions")[0][0]
    seen = q("SELECT COUNT(*) FROM v_source_admission WHERE exec_id=? AND ref_id=?", E1, REF)[0][0]
    out = db.unlink_admission(E1, REF, "fixture: the edge was wrong", S)
    n, note = exec_row(E1)
    edge = q("SELECT retired_at IS NOT NULL, retired_by_session, retirement_reason FROM search_admissions "
             "WHERE exec_id=? AND ref_id=?", E1, REF)
    record("U03", "RETIRES the edge in place (T-050): the row stays, the three retired columns are set, the count drops "
           "by one, the note carries no second copy of the retirement, and the candidate still pointing here is named",
           edge == [(1, S, "fixture: the edge was wrong")]
           and q("SELECT COUNT(*) FROM search_admissions")[0][0] == n_edges
           and n == 0 and "ADMISSION UNLINKED" not in note
           and out["candidates_still_naming_this_search"] == [C1], f"out={out} n={n} edge={edge}")
    record("T050-01", "a retired edge is gone from v_source_admission, the one pointer from a source to the search that "
           "admitted it (the view still showed it before the retirement)",
           seen == 1 and q("SELECT COUNT(*) FROM v_source_admission WHERE exec_id=? AND ref_id=?", E1, REF)[0][0] == 0,
           f"before={seen}")
    msg = refusal(db.link_admission, E1, REF, "relinked", S)
    record("U04", "link-admission on an edge that exists retired REFUSES and names log-search: the retired edge is the "
           "record of a withdrawn claim and is never un-retired in place",
           msg and "log-search" in msg and "Nothing was written" in msg
           and q("SELECT retired_at IS NOT NULL FROM search_admissions WHERE exec_id=? AND ref_id=?", E1, REF) == [(1,)],
           f"got {msg!r}")
    msg = refusal(db.unlink_admission, E1, REF, "a second, different reason", S)
    record("U05", "a second unlink of a retired edge refuses and leaves the first reason as it was",
           msg and "already retired" in msg
           and q("SELECT retirement_reason FROM search_admissions WHERE exec_id=? AND ref_id=?", E1, REF)
           == [("fixture: the edge was wrong",)], f"got {msg!r}")
    db.resolve_candidate(candidate(E1, "c1b"), "ADMITTED", "fixture re-description", S, admitted_ref_id=REF2)
    db.link_admission(E1, REF2, "fixture: a different source", S)
    record("T050-10", "link-admission counts LIVE edges: after one edge of the search was retired a new one gives 1, not 2",
           exec_row(E1)[0] == 1 and q("SELECT COUNT(*) FROM search_admissions WHERE exec_id=? AND retired_at IS NULL", E1)[0][0] == 1,
           f"results_admitted={exec_row(E1)[0]}")
    try:
        w("UPDATE search_admissions SET retired_at='2026-01-01T00:00:00Z' WHERE exec_id=? AND ref_id=?", E2, REF)
        half = None
    except sqlite3.IntegrityError as exc:
        half = str(exc)
    record("T050-02", "the schema holds the three retired columns together: setting one alone is refused by the table's CHECK",
           half is not None and "CHECK" in half, f"got {half!r}")

    # ── P: amend-population-match ────────────────────────────────────────────
    mid = db.insert_population_match({"ref_id": REF, "target_population": POP,
                                      "match_grade": "PROXY", "mismatch_note": "fixture"}, S)
    record("P01", "refuses a grade outside the column's CHECK",
           refusal(db.amend_population_match, mid, "SORT-OF", "r", S) is not None)
    record("P02", "refuses a blank reason",
           refusal(db.amend_population_match, mid, "PARTIAL", " ", S) is not None)
    record("P03", "the same grade is a no-op",
           db.amend_population_match(mid, "PROXY", "r", S)["changed"] is False)
    db.amend_population_match(mid, "PARTIAL", "fixture ruling", S)
    grade, mnote = q("SELECT match_grade, mismatch_note FROM evidence_population_match "
                     "WHERE match_id=?", mid)[0]
    record("P04", "re-grades and keeps the replaced grade in mismatch_note",
           grade == "PARTIAL" and "REGRADED" in mnote and "PROXY -> PARTIAL" in mnote
           and mnote.startswith("fixture"), f"{grade} {mnote!r}")

    # ── T: amend-term ────────────────────────────────────────────────────────
    record("T01", "refuses canonical_en (a vocabulary decision, not a wording fix)",
           refusal(db.amend_term, TERM, "canonical_en", "x", "r", S) is not None)
    record("T02", "refuses a blank reason",
           refusal(db.amend_term, TERM, "definition", "x", "", S) is not None)
    record("T03", "refuses a blank replacement",
           refusal(db.amend_term, TERM, "definition", "  ", "r", S) is not None)
    record("T04", "refuses a replacement carrying the audit marker",
           refusal(db.amend_term, TERM, "scope_note", "a || AMENDED b", "r", S) is not None)
    record("T05", "an unchanged definition is a no-op",
           db.amend_term(TERM, "definition", DEF, "r", S)["changed"] is False)
    db.amend_term(TERM, "definition", "fixture definition", "r1", S)
    (sn1,) = q("SELECT scope_note FROM terms WHERE term_id=?", TERM)[0]
    record("T06", "a definition change appends one AMENDED line to scope_note",
           sn1.count(" || AMENDED ") == 1 and "definition was:" in sn1, repr(sn1))
    db.amend_term(TERM, "scope_note", "fixture scope", "r2", S)
    db.amend_term(TERM, "scope_note", "fixture scope", "r2", S)
    (sn3,) = q("SELECT scope_note FROM terms WHERE term_id=?", TERM)[0]
    lines = sn3.split(" || AMENDED ")
    record("T07", "a repeated scope_note amendment is a second dated line, never a "
           "no-op and never nested",
           lines[0] == "fixture scope" and len(lines) == 4
           and "scope_note was: 'fixture scope'." in lines[-1]
           and sn3.count("scope_note was: '") == 2, repr(sn3))

    # ── R: resolve-candidate --suggested-slug / --clear-suggested-slug ──────────
    C4 = candidate(E1, "c4")
    record("R01", "--suggested-slug is refused on a non-REHOME disposition",
           refusal(db.resolve_candidate, C4, "OUT-OF-SCOPE", "d", S,
                   suggested_slug=B) is not None)
    record("R02", "REHOME without --suggested-slug is refused",
           refusal(db.resolve_candidate, C4, "REHOME", "d", S) is not None)
    record("R03", "a slug not in the registry is refused",
           refusal(db.resolve_candidate, C4, "REHOME", "d", S,
                   suggested_slug="no-such-slug-xyz") is not None)
    if MERGED:
        msg = refusal(db.resolve_candidate, C4, "REHOME", "d", S, suggested_slug=MERGED)
        record("R04", "a MERGED slug is refused", msg and "MERGED" in msg, f"got {msg!r}")
    else:
        record("R04", "a MERGED slug is refused (no MERGED slug in the copy to test with)",
               False, "fixture missing: add a MERGED slug to the copy")
    record("R05", "a REHOME pointing at the slug it was found under is refused",
           refusal(db.resolve_candidate, C4, "REHOME", "d", S, suggested_slug=A) is not None)
    record("R06", "--suggested-slug and --clear-suggested-slug together are refused",
           refusal(db.resolve_candidate, C4, "OUT-OF-SCOPE", "d", S, suggested_slug=B,
                   clear_suggested_slug=True) is not None)
    record("R07", "--clear-suggested-slug with REHOME is refused",
           refusal(db.resolve_candidate, C4, "REHOME", "d", S,
                   clear_suggested_slug=True) is not None)
    db.resolve_candidate(C4, "REHOME", "fixture rehome", S, suggested_slug=B)
    slug, notes = q("SELECT suggested_slug, notes FROM search_candidates "
                    "WHERE candidate_id=?", C4)[0]
    record("R08", "a valid REHOME sets the slug and records the move in the RESOLVED line",
           slug == B and f"suggested_slug None -> {B}" in notes and "RESOLVED" in notes,
           f"{slug} {notes!r}")
    db.resolve_candidate(C4, "OUT-OF-SCOPE", "fixture: not ours after all", S,
                         clear_suggested_slug=True)
    slug, notes = q("SELECT suggested_slug, notes FROM search_candidates "
                    "WHERE candidate_id=?", C4)[0]
    record("R09", "--clear-suggested-slug empties a stale value and records it",
           slug is None and f"suggested_slug {B} -> None" in notes, f"{slug} {notes!r}")
    record("R10", "staging a REHOME with no destination is refused too (add-candidate)",
           refusal(candidate, E1, "c5", "REHOME") is not None)

    # ── D: decline-parameter, and add-parameter's refusal of a declined term ─────
    # Migration 101. Fixture terms are minted through the writers (observe-term ->
    # add-term) on the copy, never a live id; names carry no digit, comparator or min/max
    # word, because add-term refuses a value-bearing name.
    decline = getattr(db, "decline_parameter", None)
    if decline is None:
        # The pre-101 state: no verb and no table. Recorded rather than raised, so the
        # run still prints its summary and exits 1.
        record("D00", "db.decline_parameter exists (migration 101's writer)", False,
               "no such function -- parameter_declinations has no writer")
    else:
        # A sighting since migration 102: a new observation carries a locator and a quote
        # containing the phrase, and a fixture quote no artefact holds takes the recorded
        # exemption route (observe-term --verbatim-exempt), as a real one would.
        def sighting(ref, phrase):
            return {"ref_id": ref, "surface_form": phrase, "language": "EN",
                    "locator": "fixture locator",
                    "context_quote": f"a fixture sentence using {phrase} once",
                    "verbatim_exempt": "fixture text: no retrieval artefact carries it"}

        # The exemption is refused where a decodable body is held (observe-term shares
        # add-extraction's refusal, R2-6), and the first source by id holds one, so the
        # sighting is made on the first source that holds none (derived, never named).
        BODYLESS = next(r for (r,) in q("SELECT ref_id FROM evidence_sources WHERE "
                                        "superseded_by_ref_id IS NULL ORDER BY ref_id")
                        if not db._retrieval_log().decodable_body_artefacts(r))

        def fixture_term(name):
            obs = db.observe_term(sighting(BODYLESS, f"fixture phrase: {name}"), S)
            return db.insert_term(obs["observation_id"], name, "fixture rationale",
                                  S)["term_id"]

        def declinations(term_id):
            return q("SELECT reason, created_by_session FROM parameter_declinations "
                     "WHERE term_id=?", term_id)

        TD = fixture_term("fixture declinable element")
        TP = fixture_term("fixture promotable quantity")
        TX = fixture_term("fixture lens term")
        WHY = "fixture: an element, not a quantity under determination"

        record("D01", "refuses a blank --term-id", refusal(decline, "  ", WHY, S) is not None)
        msg = refusal(decline, "TERM-NONE", WHY, S)
        record("D02", "refuses an unknown term and names the observe-term -> add-term route",
               msg and "observe-term" in msg and "add-term --from-observation" in msg,
               f"got {msg!r}")
        record("D03", "refuses a blank reason, and writes nothing",
               refusal(decline, TD, "   ", S) is not None and not declinations(TD))
        # T-020, T-083: a promotion names a kind (the first row of base_quantity_kinds, derived) and where a source
        # states a value of it, in the row's own cells (OD-71; a fixture locator).
        KIND = q("SELECT kind_id FROM base_quantity_kinds ORDER BY kind_id LIMIT 1")[0][0]
        pid = db.insert_parameter(TP, S, quantity_kind=KIND, **KIND_WARRANT)["parameter_id"]
        msg = refusal(decline, TP, WHY, S)
        record("D04", "refuses a term that is already a parameter, naming the parameter_id",
               msg and f"parameter {pid}" in msg and not declinations(TP), f"got {msg!r}")
        out = decline(TD, WHY, S, dry_run=True)
        record("D05", "--dry-run reports the declination and writes nothing",
               out["dry_run"] is True and out["declined"] and not declinations(TD),
               f"out={out}")
        out = decline(TD, f"  {WHY}  ", S)
        rows = declinations(TD)
        record("D06", "the legitimate shape writes ONE row, reason stripped, stamped with "
               "the session", rows == [(WHY, S)] and out["declined"] and not out["dry_run"],
               f"rows={rows} out={out}")
        msg = refusal(decline, TD, "fixture: a second reason", S)
        record("D07", "refuses a second declination, naming the standing reason and session",
               msg and WHY in msg and S in msg and len(declinations(TD)) == 1,
               f"got {msg!r}")
        # THE CASE THAT FAILS ON THE PRE-101 CODE: add-parameter promoted any existing
        # term, so a term judged not to be a parameter could still be minted one.
        msg = refusal(db.insert_parameter, TD, S)
        record("D08", "add-parameter refuses a DECLINED term, naming the declination, and "
               "mints no parameter",
               msg and "DECLINED" in msg and WHY in msg
               and not q("SELECT 1 FROM base_parameters WHERE term_id=?", TD),
               f"got {msg!r}")
        con = sqlite3.connect(DB)
        try:
            captured = "parameter_declinations" in dbcore.writable_tables(con)
        finally:
            con.close()
        record("D09", "the capture set derives parameter_declinations from the writer's "
               "INSERT literal (rows written can be shipped)", captured)
        # The CLI wiring, through argparse: an unwired or mis-keyed dispatch is invisible
        # to every case above, which call the function directly.
        env = dict(os.environ, GUIDEBOOK_DB_PATH=DB)
        cli = [sys.executable, str(REPO / "scripts" / "db.py"), "decline-parameter",
               "--term-id", TX, "--session", S, "--dry-run", "--reason"]
        ok = subprocess.run(cli + [WHY], env=env, capture_output=True, text=True)
        bad = subprocess.run(cli + [" "], env=env, capture_output=True, text=True)
        record("D10", "the CLI verb is wired: a dry run exits 0 and writes nothing; a blank "
               "--reason exits 1 with a REFUSING sentence, not a traceback",
               ok.returncode == 0 and '"declined": true' in ok.stdout
               and bad.returncode == 1 and bad.stderr.startswith("REFUSING:")
               and "Traceback" not in bad.stderr and not declinations(TX),
               f"ok={ok.returncode} {ok.stderr[-300:]!r} bad={bad.returncode} "
               f"{bad.stderr[-300:]!r}")

    # ── S: add-source refuses before it writes; link-source-slug --local-ref-id ─────
    # GAP-058. The slug whose labels mix schemes is DERIVED by asking the derivation
    # itself which slugs it refuses, never named here; the single-scheme slug likewise.
    from schemas.tier_derivation import VALID_SCOPES_BY_TYPE, derive_tier  # noqa: E402
    con = sqlite3.connect(DB)
    try:
        mixed, plain = None, None
        for (slug,) in con.execute("SELECT slug FROM slugs WHERE status='ACTIVE' "
                                   "ORDER BY slug"):
            try:
                db._next_local_ref_id(con, slug)
                plain = plain or slug
            except Refusal:
                mixed = mixed or slug
    finally:
        con.close()
    SRC_TABLES = ("evidence_sources", "evidence_source_authors", "source_slug_links")
    GREY_SCOPE = next(iter(VALID_SCOPES_BY_TYPE["grey"]))
    GREY_TIER = str(derive_tier("grey", GREY_SCOPE))

    def next_ref():
        c = sqlite3.connect(DB)
        try:
            return dbcore.next_ref_id(c)
        finally:
            c.close()

    def add_source(ref_id, *extra, title=None):
        return run_cli("add-source", "--ref-id", ref_id, "--author", "corp|Fixture Body",
                       "--year", "2020", "--title", title or f"fixture source {ref_id}",
                       "--tier", GREY_TIER, "--evidence-type", "grey", "--session", S,
                       *SRC_STANDING, *extra)

    def readable(ref_id):
        """Give a fixture source the two states add-extraction has demanded since
        2026-11-06 -- VERIFIED standing and a catalogue reading at the live catalogue
        version (R16, OR-11a) -- by SQL on the copy: record-scan would need a manifest
        artefact for each fixture, and the standing is not what these cases test."""
        c = sqlite3.connect(DB)
        try:
            c.execute("UPDATE evidence_sources SET verification_status='VERIFIED', "
                      "verification_method='direct-render' WHERE ref_id=?", (ref_id,))
            c.execute("INSERT INTO source_scans (ref_id, mode, catalogue_version, text_scope, "
                      "file_sha256, method, created_at, created_by_session) SELECT ?, "
                      "'catalogue', MAX(parameter_id), 'partial', ?, 'full-read', 't', ? "
                      "FROM base_parameters", (ref_id, "f" * 64, S))
            c.commit()
        finally:
            c.close()

    def unused_label(slug, stem="FIXTURE-"):
        n = 1
        while q("SELECT 1 FROM source_slug_links WHERE slug=? AND local_ref_id=?",
                slug, f"{stem}{n:02d}"):
            n += 1
        return f"{stem}{n:02d}"

    def link_label(ref_id, slug):
        rows = q("SELECT local_ref_id FROM source_slug_links WHERE ref_id=? AND slug=?",
                 ref_id, slug)
        return rows[0][0] if rows else None

    if not (mixed and plain):
        record("S00", "the copy holds a mixed-scheme slug and a single-scheme slug to "
               "test with", False, f"mixed={mixed} plain={plain}")
    else:
        R1 = next_ref()
        before = counts(*SRC_TABLES)
        # THE CASE THAT FAILS ON THE OLD CODE: the derivation's refusal fired inside the
        # link INSERT, after insert_evidence_source had committed, so both tables grew.
        r = add_source(R1, "--slug", mixed)
        record("S01", "add-source --slug <mixed-scheme slug> with no label refuses and "
               "writes NOTHING (no source, no author rows, no link)",
               r.returncode == 1 and r.stderr.startswith("REFUSING:")
               and counts(*SRC_TABLES) == before
               and not q("SELECT 1 FROM evidence_sources WHERE ref_id=?", R1),
               f"rc={r.returncode} {r.stderr[-300:]!r} {before} -> {counts(*SRC_TABLES)}")
        (held_ref, held,) = q("SELECT ref_id, local_ref_id FROM source_slug_links "
                              "WHERE slug=? ORDER BY local_ref_id LIMIT 1", mixed)[0]
        r = add_source(R1, "--slug", mixed, "--local-ref-id", held)
        record("S02", "a label another ref_id holds on the slug refuses, names the holder, "
               "and writes nothing",
               r.returncode == 1 and held_ref in r.stderr
               and counts(*SRC_TABLES) == before,
               f"rc={r.returncode} {r.stderr[-300:]!r}")
        r = add_source(R1, "--slug", plain, "--dry-run")
        record("S03", "add-source --slug --dry-run reports the derived label and writes "
               "nothing (it crashed on the link's foreign key before)",
               r.returncode == 0 and '"dry_run": true' in r.stdout
               and '"local_ref_id": null' not in r.stdout
               and counts(*SRC_TABLES) == before,
               f"rc={r.returncode} {r.stdout[-200:]!r} {r.stderr[-300:]!r}")
        r = add_source(R1, "--local-ref-id", "9")
        record("S04", "--local-ref-id without --slug refuses rather than dropping the flag",
               r.returncode == 1 and counts(*SRC_TABLES) == before,
               f"rc={r.returncode} {r.stderr[-300:]!r}")
        L1 = unused_label(mixed)
        r = add_source(R1, "--slug", mixed, "--local-ref-id", L1)
        record("S05", "the same call with an explicit, unused label writes the source and "
               "the link under that label",
               r.returncode == 0 and link_label(R1, mixed) == L1
               and counts(*SRC_TABLES)[:2] == (before[0] + 1, before[1] + 1),
               f"rc={r.returncode} {r.stderr[-300:]!r}")

        R2 = next_ref()
        r = add_source(R2)
        L2 = unused_label(mixed)
        r2 = run_cli("link-source-slug", "--ref-id", R2, "--slug", mixed, "--rationale",
                 "fixture grounds", "--local-ref-id", L2, "--session", S)
        record("S06", "link-source-slug --local-ref-id links an admitted, unlinked source "
               "on a slug where derivation refuses",
               r.returncode == 0 and r2.returncode == 0 and link_label(R2, mixed) == L2,
               f"add={r.returncode} {r.stderr[-200:]!r} link={r2.returncode} "
               f"{r2.stderr[-300:]!r}")
        R3 = next_ref()
        add_source(R3)
        msg = refusal(db.link_source_slug, R3, mixed, "fixture grounds", S, local_ref_id=L1)
        record("S07", "link-source-slug refuses a label another ref_id holds, and writes "
               "no link", msg and R1 in msg and link_label(R3, mixed) is None,
               f"got {msg!r}")
        # R1's link came from add-source, so it carries no grounds: the backfill branch.
        msg = refusal(db.link_source_slug, R1, mixed, "fixture grounds", S,
                      local_ref_id=L2 + "X")
        record("S08", "backfilling grounds on an existing link refuses a DIFFERENT label "
               "(it would report a relabel that is never written)",
               msg and L1 in msg and link_label(R1, mixed) == L1, f"got {msg!r}")
        try:
            out = db.link_source_slug(R1, mixed, "fixture grounds", S, local_ref_id=L1)
        except Exception as exc:  # noqa: BLE001 -- recorded red, so the run still reports
            out = {"error": f"{exc.__class__.__name__}: {exc}"}
        record("S09", "the same label backfills the grounds",
               out.get("action") == "backfilled" and q(
                   "SELECT relevance_note FROM source_slug_links WHERE ref_id=? AND slug=?",
                   R1, mixed)[0][0] == "fixture grounds", f"out={out}")

        # S10: --standard-number (the one citation column with no payload route) lands on the row.
        R_CITE = next_ref()
        r = add_source(R_CITE, "--standard-number", "FIX 1:2020")
        record("S10", "add-source writes standard_number",
               r.returncode == 0 and q("SELECT standard_number FROM evidence_sources WHERE ref_id=?",
                                       R_CITE) == [("FIX 1:2020",)],
               f"rc={r.returncode} {r.stderr[-300:]!r}")

        # S11-S14: typed columns (migrations 119, 120). A flag that parses and never reaches its column,
        # or a refusal that does not fire, would report a write that did not happen.
        pid = q("SELECT parameter_id FROM base_parameters WHERE status='active' LIMIT 1")[0][0]
        a_slug = q("SELECT slug FROM slugs LIMIT 1")[0][0]
        # The id is computed since 2026-11-06 (a typed one must equal it), so the fixture reads
        # the id the writer minted; CROSS-PARAMETER now needs two parameters.
        pid2 = q("SELECT parameter_id FROM base_parameters WHERE status='active' AND parameter_id<>? "
                 "LIMIT 1", pid)[0][0]
        r = run_cli("add-connection", "--confidence", "MODERATE",
                    "--connection-type", "CROSS-PARAMETER", "--filed-in", a_slug,
                    "--description", "fixture", "--source-skill", "fixture", "--parameter", str(pid),
                    "--parameter", str(pid2), "--methodology", "fixture method", "--session", S)
        minted = json.loads(r.stdout).get("con_id") if r.returncode == 0 else None
        record("S11", "add-connection writes one typed target row per target, one kind per column",
               r.returncode == 0 and sorted(q(
                   "SELECT parameter_id IS NOT NULL, methodology IS NOT NULL, slug, identity_code, "
                   "extraction_id FROM connection_targets WHERE con_id=?", minted))
               == [(0, 1, None, None, None), (1, 0, None, None, None), (1, 0, None, None, None)],
               f"rc={r.returncode} {r.stderr[-300:]!r}")
        # T-050 (OD-29): delete-connection retires the connection in place, through the CLI's own dispatch.
        n_con, n_tgt = counts("connections", "connection_targets")
        held_before = minted in db.cell_status(pid)["stages"]["synthesis"]["held"]["connections"]
        r_noreason = run_cli("delete-connection", "--con-id", str(minted), "--session", S)
        r = run_cli("delete-connection", "--con-id", str(minted), "--reason", "fixture: filed in error", "--session", S)
        record("T050-03", "delete-connection --reason RETIRES the connection: the verb keeps its name, the connection and its "
               "targets stay as rows, the three retired columns are set, and `db.py connections` no longer lists it; without "
               "--reason argparse refuses and nothing moves",
               r_noreason.returncode != 0 and r.returncode == 0 and counts("connections", "connection_targets") == (n_con, n_tgt)
               and q("SELECT retired_by_session, retirement_reason, retired_at IS NOT NULL FROM connections WHERE con_id=?", minted)
               == [(S, "fixture: filed in error", 1)]
               and minted not in {c["con_id"] for c in json.loads(run_cli("connections").stdout)},
               f"rc={r_noreason.returncode},{r.returncode} {r.stderr[-300:]!r}")
        r2 = run_cli("delete-connection", "--con-id", str(minted), "--reason", "again", "--session", S)
        record("T050-07", "cell-status lists a live connection of the parameter and drops it once retired",
               held_before and minted not in db.cell_status(pid)["stages"]["synthesis"]["held"]["connections"], held_before)
        record("T050-04", "a second delete-connection of a retired connection refuses, names the verb and keeps the first reason",
               r2.returncode == 1 and "already retired" in r2.stderr
               and q("SELECT retirement_reason FROM connections WHERE con_id=?", minted) == [("fixture: filed in error",)],
               f"rc={r2.returncode} {r2.stderr[-300:]!r}")
        # The same relationship, recorded again after it was withdrawn: the retired row does not block it. Its status
        # may not change afterwards. The status asked for is derived: a value the column's own CHECK holds and the row lacks.
        again = run_cli("add-connection", "--confidence", "MODERATE", "--connection-type", "CROSS-PARAMETER",
                        "--filed-in", a_slug, "--description", "fixture", "--source-skill", "fixture",
                        "--parameter", str(pid), "--parameter", str(pid2), "--methodology", "fixture method", "--session", S)
        record("T050-08", "a connection retired in place does not block recording the same relationship again (the duplicate "
               "check reads live connections only)", again.returncode == 0, f"rc={again.returncode} {again.stderr[-300:]!r}")
        other = next(v for v in sorted(dbcore.check_values(sqlite3.connect(DB), "connections", "status"))
                     if v != q("SELECT status FROM connections WHERE con_id=?", minted)[0][0])
        r3 = run_cli("update-connection", "--con-id", str(minted), "--status", other, "--session", S)
        record("T050-09", "update-connection refuses a retired connection, names the way to record it again and changes nothing",
               r3.returncode == 1 and "retired" in r3.stderr and "add-connection" in r3.stderr
               and q("SELECT status FROM connections WHERE con_id=?", minted)[0][0] != other, f"rc={r3.returncode} {r3.stderr[-300:]!r}")
        if again.returncode == 0:           # leave the table as the later cases expect it
            run_cli("delete-connection", "--con-id", json.loads(again.stdout)["con_id"], "--reason", "fixture", "--session", S)
        r = run_cli("add-connection", "--con-id", "CON-9991", "--confidence", "MODERATE",
                    "--connection-type", "CROSS-PARAMETER", "--filed-in", a_slug,
                    "--description", "fixture", "--source-skill", "fixture", "--parameter", "999999",
                    "--session", S)
        r2 = run_cli("add-connection", "--con-id", "CON-9992", "--confidence", "MODERATE",
                     "--connection-type", "CROSS-PARAMETER", "--filed-in", a_slug,
                     "--description", "fixture", "--source-skill", "fixture", "--session", S)
        record("S12", "add-connection refuses a parameter that does not exist and a connection with "
               "no target, and writes nothing",
               r.returncode == 1 and r2.returncode == 1 and not q(
                   "SELECT 1 FROM connections WHERE con_id IN ('CON-9991','CON-9992')"),
               f"rc={r.returncode},{r2.returncode} {r.stderr[-200:]!r}")
        r = run_cli("log-search", "--results-found", "1", "--slug", plain, "--language", "EN", "--query-text", "fixture zero-yield",
                    "--engine", "manual", "--depth-method", "scoping", "--prior-expectation", "none",
                    "--results-found", "0", "--absence-class", "genuine_absence", "--session", S)
        r2 = run_cli("log-search", "--results-found", "1", "--slug", plain, "--language", "EN", "--query-text", "fixture found",
                     "--engine", "manual", "--depth-method", "scoping", "--prior-expectation", "some",
                     "--results-found", "3", "--absence-class", "genuine_absence", "--session", S)
        record("S13", "log-search --absence-class lands on a zero-yield search and is refused on one that "
               "found something",
               r.returncode == 0 and r2.returncode == 1 and q(
                   "SELECT COUNT(*) FROM search_executions WHERE query_text='fixture zero-yield' "
                   "AND absence_class='genuine_absence'")[0][0] == 1,
               f"rc={r.returncode},{r2.returncode} {r.stderr[-200:]!r} {r2.stderr[-200:]!r}")
        # S14: only a `finding` extraction can carry the harm flag (the CHECK and the writer agree).
        con = sqlite3.connect(DB)
        try:
            con.execute("PRAGMA foreign_keys=ON")
            bad = False
            try:
                con.execute("INSERT INTO source_value_extractions (ref_id, slug, parameter_id, "
                            "claim_type, figure_role, harm_finding, created_by_session, created_at, "
                            "extraction_method, extraction_status) SELECT ref_id, slug, parameter_id, "
                            "claim_type, 'claim', 1, 'fixture', 'now', extraction_method, "
                            "extraction_status FROM source_value_extractions LIMIT 1")
            except sqlite3.IntegrityError:
                bad = True
        finally:
            con.close()
        record("S14", "a non-finding extraction cannot carry harm_finding (CHECK)", bad, "no IntegrityError")
        # S15: a conflict names two populations the identity lens holds; an unknown code is refused by name.
        # `ALL` is a registry row but a scope marker, not a population: add-conflict refuses it (R3-14,
        # db.insert_conflict compares the code to 'ALL'), so the two populations exclude that one row.
        two = [c for (c,) in q("SELECT identity_code FROM base_taxonomy_identity WHERE identity_code<>'ALL' "
                               "ORDER BY identity_code LIMIT 2")]
        ok = run_cli("add-conflict", "--parameter-id", str(pid), "--domain", "FIXTURE", "--pop-a", two[0],
                     "--pop-b", two[1], "--status", "PROPOSED", "--session", S)
        bad_ = run_cli("add-conflict", "--parameter-id", str(pid), "--domain", "FIXTURE2", "--pop-a",
                       "NOT-A-CODE", "--pop-b", two[1], "--status", "PROPOSED", "--session", S)
        record("S15", "add-conflict accepts identity-lens codes and refuses one the lens lacks",
               ok.returncode == 0 and bad_.returncode == 1 and not q(
                   "SELECT 1 FROM conflicts WHERE domain='FIXTURE2'"),
               f"rc={ok.returncode},{bad_.returncode} {bad_.stderr[-200:]!r}")

    # ── X: supersede-source ───────────────────────────────────────────────────
    # GAP-060. Two DOI-less fixture sources with one author, year and title are the
    # collision test_db_integrity D04 exists to catch; the verb is what makes it go quiet
    # without a curated exemption.
    supersede = getattr(db, "supersede_source", None)

    def integrity_line(tid):
        """The copy's test_db_integrity line for `tid`, plus the detail line after it."""
        r = subprocess.run([sys.executable, str(REPO / "scripts" / "tests" /
                                                "test_db_integrity.py")],
                           env=dict(os.environ, GUIDEBOOK_DB_PATH=DB),
                           capture_output=True, text=True)
        lines = r.stdout.splitlines()
        for i, line in enumerate(lines):
            if f"] {tid}:" in line:
                return line + " " + (lines[i + 1] if i + 1 < len(lines) else "")
        return ""

    def superseded_by(ref_id):
        return q("SELECT superseded_by_ref_id FROM evidence_sources WHERE ref_id=?",
                 ref_id)[0][0]

    if supersede is None:
        record("X00", "db.supersede_source exists (GAP-060's writer)", False,
               "no such function -- a duplicate source can be merged only by hand SQL")
    else:
        DUP = "fixture decree on ramp gradients"
        XA = next_ref()
        add_source(XA, title=DUP)
        XB = next_ref()
        add_source(XB, title=DUP)
        d04 = integrity_line("D04")
        record("X01", "the fixture pair is a live D04 collision before the verb runs",
               "[✗]" in d04 and XA in d04 and XB in d04, d04)
        WHY = "fixture: the same decree admitted twice"
        msg = refusal(supersede, XA, XA.lower(), WHY, S)
        record("X02", "refuses A == B (case-folded)",
               msg and "cannot supersede itself" in msg, f"got {msg!r}")
        ghost = next_ref()
        msg = refusal(supersede, ghost, XB, WHY, S)
        record("X03", "refuses a --ref-id that is not admitted",
               msg and "--ref-id" in msg and ghost in msg, f"got {msg!r}")
        msg = refusal(supersede, XA, ghost, WHY, S)
        record("X04", "refuses a --by that is not admitted",
               msg and "--by" in msg and ghost in msg, f"got {msg!r}")
        record("X05", "refuses a blank reason, and writes nothing",
               refusal(supersede, XA, XB, "  ", S) is not None and superseded_by(XA) is None)
        out = supersede(XA, XB, WHY, S, dry_run=True)
        record("X06", "--dry-run reports and writes nothing",
               out["dry_run"] is True and superseded_by(XA) is None, f"out={out}")
        out = supersede(XA, XB, f"  {WHY}  ", S)
        notes, upd_by = q("SELECT notes, updated_by_session FROM evidence_sources "
                          "WHERE ref_id=?", XA)[0]
        deps = {(d["table"], d["column"]) for d in out["dependents_left_in_place"]}
        record("X07", "the legitimate shape sets the pointer, appends one dated SUPERSEDED "
               "line carrying the reason, stamps the session, and REPORTS dependents "
               "found through the live foreign keys",
               superseded_by(XA) == XB and notes.count(" || SUPERSEDED ") == 1
               and f"by {XB}: {WHY}" in notes and upd_by == S
               and ("evidence_source_authors", "ref_id") in deps
               and q("SELECT COUNT(*) FROM evidence_source_authors WHERE ref_id=?",
                     XA)[0][0] == 1, f"out={out} notes={notes!r}")
        # THE CASE THAT FAILS ON THE OLD CODE: there was no verb, so the collision could
        # be cleared only by hand SQL or by a curated exemption that left it counted.
        d04, a09 = integrity_line("D04"), integrity_line("A09")
        # The claim is about THIS fixture pair, not the whole database: D04's detail lists
        # every live collision, so the pair must be absent from it. Asserting the line is
        # green would make the test depend on the rest of the corpus holding no collision,
        # which stopped being true once main carried REF-01019 and REF-01031 (a mirror and
        # its official file, awaiting this very verb). `d04` must be non-empty: a missing
        # line is a vacuous pass, not a quiet check.
        record("X08", "D04 no longer names the fixture pair after the verb, and A09 (the "
               "pointer resolves) holds with the tombstone in scope",
               bool(d04) and XA not in d04 and XB not in d04
               and "[✓]" in a09 and "NOTHING IN SCOPE" not in a09,
               f"{d04} | {a09}")
        msg = refusal(supersede, XA, XB, WHY, S)
        record("X09", "refuses a source already superseded, naming its target",
               msg and XB in msg, f"got {msg!r}")

        # THE TOMBSTONE IS NOT LIVE FOR THE WRITERS WHOSE ROWS THE ENGINE WOULD DROP.
        # On the pre-fix code each of these WROTE a row against a superseded source,
        # which gather_sources then skipped (superseded_by_ref_id IS NULL): work filed and
        # silently lost. Each case uses a payload the writer accepts for a live source,
        # so the only thing that changes between accept and refuse is the supersession.
        con = sqlite3.connect(DB)
        try:
            PID = con.execute("SELECT parameter_id FROM base_parameters "
                              "WHERE status='active' ORDER BY 1 LIMIT 1").fetchone()
            GRADE = sorted(dbcore.check_values(con, "evidence_population_match",
                                               "match_grade"))[0]
        finally:
            con.close()
        XD = next_ref()
        add_source(XD, title=f"fixture extraction source {XD}")
        readable(XD)
        X_PAYLOAD = {"ref_id": XD, "parameter_id": PID and PID[0],
                     "identity_code": POP, "claim_type": "absent", "figure_role": "finding",
                     "claim_text": "fixture: the source states nothing for this parameter",
                     "lens_basis": "named_in_text", "lens_basis_text": "states nothing",
                     "extraction_method": "skim"}
        # No artefact carries a fixture's words; the exemption is the writer's own path
        # for that, and it is ledgered on the row.
        X_EXEMPT = "fixture: a test payload, no retrieved artefact exists"
        try:
            db.link_source_slug(XD, plain, "fixture: speaks to this slug", S)
            first = db.insert_extraction(dict(X_PAYLOAD), S, relations=[],
                                         verbatim_exempt=X_EXEMPT)
            supersede(XD, XB, WHY, S)
        except Exception as exc:  # noqa: BLE001 -- recorded red below
            first = {"error": f"{exc.__class__.__name__}: {exc}"}
        n_sve = counts("source_value_extractions")
        msg = refusal(db.insert_extraction, dict(X_PAYLOAD), S, relations=[],
                      verbatim_exempt=X_EXEMPT)
        record("X15", "add-extraction accepts a payload while the source is live, and "
               "refuses the same payload once it is superseded, naming the live source",
               "extraction_id" in first and msg and f"superseded by {XB}" in msg
               and f"File it against {XB}" in msg
               and counts("source_value_extractions") == n_sve,
               f"first={first} msg={msg!r}")
        record("X15a", "add-extraction leaves evidence_sources.data_capture_status alone (its writer is retired)",
               "extraction_id" in first
               and q("SELECT data_capture_status FROM evidence_sources WHERE ref_id=?", XD)[0][0] == "pending",
               f"first={first}")
        n_obs = counts("observed_terms")
        # Migration 102: a new observation needs a locator and a verifiable quote (or the
        # recorded exemption), so the fixture supplies them; the tombstone refusal fires
        # before either is examined.
        obs_x = {"ref_id": XA, "surface_form": "fixture phrase X", "language": "EN",
                 "locator": "fixture locator",
                 "context_quote": "a fixture sentence using fixture phrase X once",
                 "verbatim_exempt": "fixture text: no retrieval artefact carries it"}
        msg = refusal(db.observe_term, obs_x, S)
        record("X16", "observe-term refuses a superseded source and writes nothing",
               msg and f"superseded by {XB}" in msg and counts("observed_terms") == n_obs,
               f"got {msg!r}")
        n_epm = counts("evidence_population_match")
        msg = refusal(db.insert_population_match,
                      {"ref_id": XA, "target_population": POP, "match_grade": GRADE}, S)
        record("X17", "add-population-match refuses a superseded source and writes nothing",
               msg and f"superseded by {XB}" in msg
               and counts("evidence_population_match") == n_epm, f"got {msg!r}")
        try:
            live = db.observe_term(dict(obs_x, ref_id=XB), S)
        except Exception as exc:  # noqa: BLE001 -- recorded red below
            live = {"error": f"{exc.__class__.__name__}: {exc}"}
        record("X18", "the superseding (live) source is still accepted by observe-term",
               live.get("created") is True, f"{live}")
        XC = next_ref()
        add_source(XC)
        msg = refusal(supersede, XC, XA, WHY, S)
        record("X10", "refuses a --by that is itself superseded (no chains), naming where "
               "it points", msg and XB in msg and superseded_by(XC) is None, f"got {msg!r}")
        out = supersede(XB, XC, WHY, S, dry_run=True)
        deps = {(d["table"], d["column"]): d["rows"] for d in out["dependents_left_in_place"]}
        record("X10b", "a row already superseded BY the source is reported as a dependent "
               "(the pointer has no FK, so it is added by name), not refused",
               deps.get(("evidence_sources", "superseded_by_ref_id"))
               == q("SELECT COUNT(*) FROM evidence_sources WHERE superseded_by_ref_id=?",
                    XB)[0][0] >= 1
               and superseded_by(XB) is None, f"out={out}")
        ok = run_cli("supersede-source", "--ref-id", XC, "--by", XB, "--reason", WHY,
                     "--session", S, "--dry-run")
        bad = run_cli("supersede-source", "--ref-id", XC, "--by", XB, "--reason", " ",
                      "--session", S)
        record("X11", "the CLI verb is wired: a dry run exits 0 and writes nothing; a blank "
               "--reason exits 1 with a REFUSING sentence",
               ok.returncode == 0 and '"dry_run": true' in ok.stdout
               and bad.returncode == 1 and bad.stderr.startswith("REFUSING:")
               and superseded_by(XC) is None,
               f"ok={ok.returncode} {ok.stderr[-300:]!r} bad={bad.returncode} "
               f"{bad.stderr[-300:]!r}")

        # A LIVE determination. Every specification in the copy may be retired, and no
        # writer short of the determination engine creates one, so one is UN-retired by
        # SQL on the copy. Chosen by query: a specification whose convergence holds a
        # source its governing links do not, so both junctions are exercised.
        pick = q("SELECT s.specification_id, l.ref_id, c.ref_id "
                 "FROM specifications s "
                 "JOIN specification_source_links l ON l.specification_id = s.specification_id "
                 "JOIN convergence_sources c ON c.convergence_id = s.convergence_id "
                 "WHERE NOT EXISTS (SELECT 1 FROM specification_source_links l2 "
                 "  WHERE l2.specification_id = s.specification_id AND l2.ref_id = c.ref_id) "
                 "ORDER BY 1, 2, 3 LIMIT 1")
        if not pick:
            record("X12", "a specification with both junctions to test with", False,
                   "fixture missing in the copy")
        else:
            SPEC, LREF, CREF = pick[0]
            con = sqlite3.connect(DB)
            unretire(con, SPEC)
            con.commit()
            con.close()
            msg_l = refusal(supersede, LREF, XB, WHY, S)
            msg_c = refusal(supersede, CREF, XB, WHY, S)
            record("X12", "refuses a source a LIVE specification rests on, through either "
                   "junction, naming the specification",
                   msg_l and f"specification {SPEC} (via specification_source_links)" in msg_l
                   and msg_c and f"specification {SPEC} (via convergence_sources)" in msg_c
                   and superseded_by(LREF) is None and superseded_by(CREF) is None,
                   f"l={msg_l!r} c={msg_c!r}")
            db.retire_specification(SPEC, S, reason="fixture: retired to release its sources")
            reretire(SPEC)
            # The named remedy must work: once the specification is retired, the same
            # call goes through. Written for real, so the capture path can be checked on
            # a row the canonical DB already holds -- an UPDATE, not an INSERT.
            try:
                out = supersede(LREF, XB, WHY, S)
            except Exception as exc:  # noqa: BLE001 -- recorded red, so the run reports
                out = {"error": f"{exc.__class__.__name__}: {exc}"}
            record("X13", "after retire-specification the refusal lifts (the remedy it "
                   "names works)", superseded_by(LREF) == XB, f"out={out}")
            import importlib                                       # noqa: E402
            sys.path.insert(0, str(REPO / "scripts" / "research"))
            emit_mod = importlib.import_module("emit_batch_sql")
            sql_out = os.path.join(TMP, "capture.sql")
            try:
                emit_mod.emit(DB, str(REPO / "data" / "guidebook.db"), sql_out)
                captured = open(sql_out, encoding="utf-8").read()
            except SystemExit as exc:
                captured = f"emit refused: {exc}"
            hit = [ln for ln in captured.splitlines()
                   if ln.startswith('UPDATE "evidence_sources"')
                   and f'"superseded_by_ref_id" = \'{XB}\'' in ln
                   and f'"ref_id" = \'{LREF}\'' in ln]
            record("X14", "emit_batch_sql captures the verb's UPDATE of a canonical row "
                   "(the write can be shipped)", len(hit) == 1, captured[-400:])

    # ── C: close-adversarial-pass parses a SURVIVED artefact ──────────────────────
    # GAP-055. Fixture passes are set by SQL on the copy: record-adversarial-pass derives
    # its findings from two real, tracked transcripts, which a fixture cannot supply. The
    # lens set is the column's own CHECK; the tracked file is the module under test, so
    # no live path is hard-coded.
    TRACKED = pathlib.Path(db.__file__).resolve().relative_to(REPO).as_posix()
    con = sqlite3.connect(DB)
    try:
        LENSES = sorted(dbcore.check_values(con, "adversarial_findings", "lens"))
    finally:
        con.close()

    def make_pass(artefact):
        """A pass with every lens covered: one SURVIVED row carrying `artefact`, the
        rest NOT-ATTACKED with a real reason. Returns (pass_id, survived finding_id)."""
        c = sqlite3.connect(DB)
        try:
            pid = c.execute(
                "INSERT INTO adversarial_passes (subject_session, subject_commit, "
                "reviewer_transcript, reviewer_models, author_transcript, author_models, "
                "created_by_session, created_at) VALUES (?,?,?,?,?,?,?,?)",
                (f"session_fixture-close-{artefact[:24]}", "0000000",
                 "transcripts/fixture/reviewer.jsonl", '["fixture-model"]',
                 "transcripts/fixture/author.jsonl", '["fixture-model"]', S,
                 "2026-10-01 00:00")).lastrowid
            fid = None
            for i, lens in enumerate(LENSES):
                survived = i == 0
                cur = c.execute(
                    "INSERT INTO adversarial_findings (pass_id, lens, claim_attacked, "
                    "method, artefact, verdict, created_by_session, created_at) "
                    "VALUES (?,?,?,?,?,?,?,?)",
                    (pid, lens, "fixture claim",
                     "fixture: attacked it and it held" if survived
                     else "fixture: this lens does not apply to the fixture subject",
                     artefact if survived else None,
                     "SURVIVED" if survived else "NOT-ATTACKED", S, "2026-10-01 00:00"))
                fid = fid or cur.lastrowid
            c.commit()
            return pid, fid
        finally:
            c.close()

    def closed_at(pid):
        return q("SELECT closed_at FROM adversarial_passes WHERE pass_id=?", pid)[0][0]

    def close(pid):
        try:
            return db.close_adversarial_pass(pid, S)
        except Exception as exc:  # noqa: BLE001 -- recorded red, so the run still reports
            return {"error": f"{exc.__class__.__name__}: {exc}"}

    # THE CASE THAT FAILS ON THE OLD CODE: the literal check resolved the whole string,
    # so a real file followed by a qualifier was "not an existing file".
    P1, _ = make_pass(f"{TRACKED} (and the other 11)")
    out = close(P1)
    record("C01", "a SURVIVED artefact that leads with a tracked file and adds a "
           "qualifier closes the pass", closed_at(P1) is not None and not out.get("error")
           and out.get("unresolved") == {}, f"out={out}")
    MISSING = "retrieval-log/no-such-session/none.pdf"
    P2, F2 = make_pass(f"{TRACKED} page 15; {MISSING}")
    out = close(P2)
    record("C02", "one resolving file admits the finding, and a cited path that does "
           "not resolve is returned as unresolved",
           closed_at(P2) is not None and out.get("unresolved") == {F2: [MISSING]},
           f"out={out}")
    P3, F3 = make_pass("source_value_extractions rows 70 and 71")
    msg = refusal(db.close_adversarial_pass, P3, S)
    record("C03", "an artefact with no path-shaped token that resolves still refuses, "
           "listing what it tried, and the pass stays open",
           msg and f"finding {F3}" in msg and "Tried:" in msg and closed_at(P3) is None,
           f"got {msg!r}")
    # Containment, proven with a file that EXISTS outside the repo (the test's temp
    # directory), so the refusal cannot be passing merely because the target is absent.
    outside = os.path.join(TMP, "outside.txt")
    open(outside, "w").close()
    rel_out = os.path.relpath(outside, REPO)
    P4, _ = make_pass(f"({rel_out})")
    msg = refusal(db.close_adversarial_pass, P4, S)
    record("C04", "a '../' token that reaches a real file outside the repo refuses "
           "(containment on the resolved path), wrapped or not",
           rel_out.startswith("..") and msg and closed_at(P4) is None, f"got {msg!r}")
    P5, F5 = make_pass(f"`{TRACKED}`. Also {MISSING}")
    r = run_cli("close-adversarial-pass", "--pass-id", str(P5), "--session", S,
                "--dry-run")
    record("C05", "the CLI verb is wired: a dry run exits 0, prints the unresolved token "
           "as REPORTED, and leaves the pass open",
           r.returncode == 0 and f"REPORTED: finding {F5}" in r.stderr
           and MISSING in r.stderr and closed_at(P5) is None,
           f"rc={r.returncode} {r.stderr[-300:]!r}")

    # The owner ruling that holds pass 1 open must be where the operator reads: the verb's
    # own --help (and the function's docstring), since nothing refuses pass 1 by id.
    h = run_cli("close-adversarial-pass", "--help")
    record("C06", "--help names the 2026-09-27 ruling that holds pass 1 OPEN",
           h.returncode == 0 and "2026-09-27" in h.stdout and "pass 1" in h.stdout
           and "OPEN" in h.stdout, h.stdout[-400:])
    # THE DATABASE IS NOT AN ARTEFACT OF ATTACK. Its path is derived from dbcore, never
    # typed. A finding admitted only on it closes (refusing would re-open GAP-055's trap)
    # but is returned and printed as REPORTED; one that also cites a real file is not.
    DBREL = dbcore.CANONICAL_DB.resolve().relative_to(REPO.resolve()).as_posix()
    P6, F6 = make_pass(f"{DBREL} search_executions.query_text for mining rows")
    r = run_cli("close-adversarial-pass", "--pass-id", str(P6), "--session", S,
                "--dry-run")
    out6 = close(P6)
    P7, _ = make_pass(f"{TRACKED}; {DBREL}")
    out7 = close(P7)
    record("C07", "a finding admitted only on the database file closes but is returned as "
           "database_only and printed as REPORTED; one that also cites a real file is not",
           r.returncode == 0 and f"REPORTED: finding {F6} was admitted only on" in r.stderr
           and out6.get("database_only") == {F6: [DBREL]} and closed_at(P6) is not None
           and out7.get("database_only") == {} and closed_at(P7) is not None,
           f"rc={r.returncode} {r.stderr[-300:]!r} out6={out6} out7={out7}")

    # ── E: amend-source --field evidence_type ──────────────────────────────────
    # I1. Fixture sources are admitted through add-source on the copy; every tier the
    # cases expect is derived from the ladder, never typed. The Co-1 fixture carries a
    # co1_source_type so the move off co1 is seen to clear BOTH Co-1-only columns.
    from schemas.tier_derivation import TIER_MAP  # noqa: E402

    def attempt(fn, *a, **k):
        """(result, None) when `fn` returns, (None, text) when it refuses or fails. A
        non-Refusal exception is a defect and is reported as one."""
        try:
            return fn(*a, **k), None
        except Refusal as exc:
            return None, str(exc)
        except Exception as exc:  # noqa: BLE001 -- recorded red, so the run still reports
            return None, f"DEFECT {exc.__class__.__name__}: {exc}"

    def source_row(ref_id):
        return dict(zip(
            ("evidence_type", "scope", "tier", "co1_provenance", "co1_source_type",
             "metadata_integrity_status", "metadata_integrity_detail",
             "updated_by_session"),
            q("SELECT evidence_type, scope, tier, co1_provenance, co1_source_type, "
              "metadata_integrity_status, metadata_integrity_detail, updated_by_session "
              "FROM evidence_sources WHERE ref_id=?", ref_id)[0]))

    def admit(ref_id, etype, scope=None, *extra):
        args = ["add-source", "--ref-id", ref_id, "--author", "corp|Fixture Body",
                "--year", "2021", "--title", f"fixture retype {ref_id}", "--evidence-type",
                etype, "--tier", str(TIER_MAP[(etype, scope or next(iter(
                    VALID_SCOPES_BY_TYPE[etype])))]), "--session", S, *SRC_STANDING, *extra]
        if scope:
            args += ["--scope", scope]
        return run_cli(*args)

    ONE = {t for t, v in VALID_SCOPES_BY_TYPE.items() if len(v) == 1}
    HI = min(sorted(VALID_SCOPES_BY_TYPE["clinical"]), key=lambda s: TIER_MAP[("clinical", s)])
    PROV = "fixture: written by a named disabled people's organisation, per its own preface"
    EA, EC = next_ref(), None
    r_a = admit(EA, "clinical", HI)
    EC = next_ref()
    r_c = admit(EC, "co1", None, "--co1-provenance", PROV, "--co1-source-type",
                "dpo_position_statement")
    if r_a.returncode or r_c.returncode:
        record("E00", "fixture sources admitted for the retype cases", False,
               f"clinical={r_a.returncode} {r_a.stderr[-200:]!r} "
               f"co1={r_c.returncode} {r_c.stderr[-200:]!r}")
    else:
        WHY = "fixture: the bytes describe a grey report, not a trial"
        grey_tier = TIER_MAP[("grey", next(iter(VALID_SCOPES_BY_TYPE["grey"])))]
        hi_tier = TIER_MAP[("clinical", HI)]
        before = source_row(EA)
        # THE CASE THAT FAILS ON THE OLD CODE: evidence_type was not in _AMENDABLE, so a
        # mis-typed row could only be re-typed (and re-tiered) by hand SQL.
        out, msg = attempt(db.amend_source, EA, "evidence_type", "GREY", WHY, session=S)
        row = source_row(EA)
        seg = (row["metadata_integrity_detail"] or "").split(" || ")[-1]
        record("E01", "a type move succeeds, derives the tier from the ladder (here "
               f"{hi_tier} -> {grey_tier}), stores the type lower-case, and ledgers type, "
               "scope and tier in ONE segment with the reason",
               out and out["changed"] and out["tier_now"] == grey_tier
               and row["evidence_type"] == "grey" and row["tier"] == grey_tier
               and row["scope"] in VALID_SCOPES_BY_TYPE["grey"]
               and row["metadata_integrity_status"] == "CORRECTED"
               and row["updated_by_session"] == S
               and f"evidence_type CORRECTED ({WHY}). Replaced text was: 'clinical'" in seg
               and f"scope {HI!r} -> " in seg and f"tier {hi_tier} -> {grey_tier}" in seg
               and before["metadata_integrity_detail"] is None,
               f"msg={msg!r} out={out} seg={seg!r}")

        # getattr, so the pre-change module (no constant) reports red here rather than
        # crashing the run and hiding every later case.
        WARRANT = getattr(db, "CO1_WARRANT_REQUIRED", None)
        out, msg = attempt(db.amend_source, EA, "evidence_type", "co1", WHY, session=S)
        record("E02", "a move TO co1 without --co1-provenance refuses with add-source's "
               "D-0178 sentence, and writes nothing",
               out is None and msg and WARRANT and WARRANT in msg
               and source_row(EA)["evidence_type"] == "grey", f"msg={msg!r}")
        nf = TIER_MAP[("national_fw", next(iter(VALID_SCOPES_BY_TYPE["national_fw"])))]
        out, msg = attempt(db.amend_source, EA, "evidence_type", "national_fw", WHY,
                           session=S, tier=nf + 1)
        record("E03", "a --tier that disagrees with the ladder refuses, naming the derived "
               "tier, and writes nothing",
               out is None and msg and f"derives {nf} from" in msg
               and source_row(EA)["evidence_type"] == "grey", f"msg={msg!r}")
        out, msg = attempt(db.amend_source, EA, "evidence_type", "clinical", WHY, session=S)
        out2, msg2 = attempt(db.amend_source, EA, "evidence_type", "standard_eb", WHY,
                             session=S, scope=next(iter(VALID_SCOPES_BY_TYPE["grey"])))
        record("E04", "a multi-scope type needs --scope, and an inadmissible scope "
               "refuses; neither writes",
               msg and "--scope is REQUIRED" in msg and msg2 and "not admissible" in msg2
               and source_row(EA)["evidence_type"] == "grey", f"{msg!r} | {msg2!r}")
        out, msg = attempt(db.amend_source, EA, "evidence_type", "folklore", WHY, session=S)
        record("E05", "a type off the ladder refuses and names the ladder's types",
               msg and "not on the ratified ladder" in msg and "'co1'" in msg,
               f"msg={msg!r}")
        out, msg = attempt(db.amend_source, EA, "notes", "fixture note", WHY, session=S,
                           scope=HI)
        out2, msg2 = attempt(db.amend_source, EA, "evidence_type", "code", WHY, session=S,
                             co1_provenance=PROV)
        record("E06", "--scope beside another field, and --co1-provenance beside a non-co1 "
               "type, both refuse",
               msg and "only admissible beside --field evidence_type" in msg
               and msg2 and "only admissible when the new evidence_type is co1" in msg2
               and source_row(EA)["evidence_type"] == "grey", f"{msg!r} | {msg2!r}")
        out, msg = attempt(db.amend_source, EA, "evidence_type", "grey", WHY, session=S)
        record("E07", "the type it already holds (scope and tier consistent) is a no-op",
               out and out["changed"] is False, f"out={out} msg={msg!r}")

        # Leaving co1: the warrant goes to the ledger, in the same segment as the tier
        # move, and both Co-1-only columns are NULLed (correction 17).
        out, msg = attempt(db.amend_source, EC, "evidence_type", "grey",
                           "fixture: no co-production is evidenced in the bytes", session=S)
        row = source_row(EC)
        seg = (row["metadata_integrity_detail"] or "").split(" || ")[-1]
        record("E08", "leaving co1 NULLs co1_provenance and co1_source_type and keeps both "
               "texts in the SAME ledger segment as the tier move",
               out and out["nulled"] == ["co1_provenance", "co1_source_type"]
               and row["co1_provenance"] is None and row["co1_source_type"] is None
               and row["evidence_type"] == "grey"
               and f"tier {TIER_MAP[('co1', 'intrinsic')]} -> {grey_tier}" in seg
               and PROV in seg and "dpo_position_statement" in seg,
               f"msg={msg!r} out={out} seg={seg!r}")
        # THE CASE THAT FAILS ON THE PRE-FIX CODE: a move to co1 wrote a Co-1 row with
        # co1_source_type NULL, which co1_field_consistency rejects and grain_for grades
        # individual-grain whatever the source is. The vocabulary is the enum, read here.
        from schemas.enums import Co1SourceType  # noqa: E402
        CO1_TYPES = sorted(m.value for m in Co1SourceType)
        CO1_ST = CO1_TYPES[0]
        WHY_C = "fixture: the preface names the DPO after all"
        out, msg = attempt(db.amend_source, EC, "evidence_type", "co1", WHY_C, session=S,
                           co1_provenance=PROV)
        record("E13", "a move TO co1 with the warrant but no --co1-source-type refuses, "
               "naming the enum's members, and writes nothing",
               out is None and msg and "--co1-source-type is REQUIRED" in msg
               and all(t in msg for t in CO1_TYPES)
               and source_row(EC)["evidence_type"] == "grey", f"msg={msg!r} out={out}")
        _, msg = attempt(db.amend_source, EC, "evidence_type", "co1", WHY_C, session=S,
                         co1_provenance=PROV, co1_source_type="fixture_not_a_member")
        _, msg2 = attempt(db.amend_source, EC, "evidence_type", "code", WHY_C, session=S,
                          co1_source_type=CO1_ST)
        _, msg3 = attempt(db.amend_source, EC, "notes", "fixture note", WHY_C, session=S,
                          co1_source_type=CO1_ST)
        record("E14", "an unknown --co1-source-type refuses naming the members; beside a "
               "non-co1 type, or beside another field, it refuses too",
               msg and "not a member of schemas.enums.Co1SourceType" in msg
               and msg2 and "only admissible when the new evidence_type is co1" in msg2
               and msg3 and "only admissible beside --field evidence_type" in msg3
               and source_row(EC)["evidence_type"] == "grey",
               f"{msg!r} | {msg2!r} | {msg3!r}")
        # The round trip co1 -> grey -> co1 re-supplies the source type, and ends with it.
        out, msg = attempt(db.amend_source, EC, "evidence_type", "co1", WHY_C, session=S,
                           co1_provenance=PROV, co1_source_type=CO1_ST,
                           tier=TIER_MAP[("co1", "intrinsic")])
        row = source_row(EC)
        seg = (row["metadata_integrity_detail"] or "").split(" || ")[-1]
        record("E09", "a move TO co1 with the warrant and a source type (and an agreeing "
               "--tier) writes both, the derived scope and tier, and ledgers the type",
               out and out["changed"] and row["evidence_type"] == "co1"
               and row["co1_provenance"] == PROV and row["co1_source_type"] == CO1_ST
               and f"co1_source_type written as {CO1_ST!r}" in seg
               and row["tier"] == TIER_MAP[("co1", "intrinsic")],
               f"msg={msg!r} out={out} seg={seg!r}")

        # A LIVE determination, through both junctions. Every specification in the copy
        # is retired and no writer short of the determination engine creates one, so one
        # is UN-retired by SQL on the copy and its retirement restored the same way.
        pick = q("SELECT s.specification_id, l.ref_id, c.ref_id, s.retired_at, "
                 "s.retired_by_session, s.retirement_reason "
                 "FROM specifications s "
                 "JOIN specification_source_links l ON l.specification_id = s.specification_id "
                 "JOIN convergence_sources c ON c.convergence_id = s.convergence_id "
                 "WHERE NOT EXISTS (SELECT 1 FROM specification_source_links l2 "
                 "  WHERE l2.specification_id = s.specification_id AND l2.ref_id = c.ref_id) "
                 "ORDER BY 1, 2, 3 LIMIT 1")
        if not pick:
            record("E10", "a specification with both junctions to test with", False,
                   "fixture missing in the copy")
        else:
            SPEC, LREF, CREF, R_AT, R_BY, R_WHY = pick[0]
            con = sqlite3.connect(DB)
            unretire(con, SPEC)
            con.commit()
            con.close()
            types = {r: source_row(r)["evidence_type"] for r in (LREF, CREF)}
            to = {r: next(t for t in sorted(ONE) if t != types[r] and t != "co1")
                  for r in (LREF, CREF)}
            _, msg_l = attempt(db.amend_source, LREF, "evidence_type", to[LREF], WHY,
                               session=S)
            _, msg_c = attempt(db.amend_source, CREF, "evidence_type", to[CREF], WHY,
                               session=S)
            record("E10", "a source a LIVE specification rests on refuses, through either "
                   "junction, naming it and the footer, and writes nothing",
                   msg_l and f"specification {SPEC} (via specification_source_links)" in msg_l
                   and msg_c and f"specification {SPEC} (via convergence_sources)" in msg_c
                   and "Never move an adjudicated figure" in msg_l
                   and {r: source_row(r)["evidence_type"] for r in types} == types,
                   f"l={msg_l!r} c={msg_c!r}")
            reretire(SPEC, R_AT, R_BY, R_WHY)

        ok = run_cli("amend-source", "--ref-id", EA, "--field", "evidence_type",
                     "--replacement", "co1", "--co1-provenance", PROV,
                     "--co1-source-type", CO1_ST, "--reason", WHY,
                     "--session", S, "--dry-run")
        bad = run_cli("amend-source", "--ref-id", EA, "--field", "notes", "--replacement",
                      "x", "--scope", HI, "--reason", WHY, "--session", S)
        record("E11", "the CLI is wired: a dry run exits 0 with the ledger segment and "
               "writes nothing; --scope beside --field notes exits 1 with REFUSING",
               ok.returncode == 0 and '"type_now": "co1"' in ok.stdout
               and '"ledger_segment"' in ok.stdout
               and source_row(EA)["evidence_type"] == "grey"
               and bad.returncode == 1 and bad.stderr.startswith("REFUSING:"),
               f"ok={ok.returncode} {ok.stderr[-300:]!r} bad={bad.returncode} "
               f"{bad.stderr[-300:]!r}")

        # The capture path, on a CANONICAL row (an UPDATE, not a fixture INSERT): a Co-1
        # row taken from the copy moves off co1, and the NULLs must reach the migration.
        canon = q("SELECT ref_id FROM evidence_sources WHERE evidence_type='co1' "
                  "AND co1_provenance IS NOT NULL AND created_by_session <> ? "
                  "ORDER BY ref_id LIMIT 1", S)
        if not canon:
            record("E12", "a canonical Co-1 row to test capture with", False,
                   "fixture missing in the copy")
        else:
            (CREF1,) = canon[0]
            out, msg = attempt(db.amend_source, CREF1, "evidence_type", "grey", WHY,
                               session=S)
            import importlib                                       # noqa: E402
            sys.path.insert(0, str(REPO / "scripts" / "research"))
            emit_mod = importlib.import_module("emit_batch_sql")
            sql_out = os.path.join(TMP, "capture-retype.sql")
            try:
                emit_mod.emit(DB, str(REPO / "data" / "guidebook.db"), sql_out)
                captured = open(sql_out, encoding="utf-8").read()
            except SystemExit as exc:
                captured = f"emit refused: {exc}"
            hit = [ln for ln in captured.splitlines()
                   if ln.startswith('UPDATE "evidence_sources"')
                   and f'"ref_id" = \'{CREF1}\'' in ln
                   and '"evidence_type" = \'grey\'' in ln
                   and '"co1_provenance" = NULL' in ln
                   and '"co1_source_type" = NULL' in ln]
            record("E12", "emit_batch_sql captures the retype of a canonical row, NULLs "
                   "included (the write can be shipped)",
                   out and len(hit) == 1, f"msg={msg!r} {captured[-400:]!r}")

    # ── K: update-code-lead, and add-code-lead's near-duplicate refusal ────────────
    # I8 / GAP-005. Fixture leads are written through insert_code_lead on the copy, in a
    # jurisdiction read from the copy's own leads. The status vocabulary is the column's
    # CHECK; the two non-default values are taken from it, never typed. Each fixture
    # passes the column default as its status, as the CLI does: insert_code_lead's
    # vocabulary gate refuses a None status before its INSERT fallback is reached.
    update = getattr(db, "update_code_lead", None)
    con = sqlite3.connect(DB)
    try:
        STATUSES = sorted(dbcore.check_values(con, "research_code_leads", "status"))
    finally:
        con.close()
    (JUR,) = q("SELECT jurisdiction FROM research_code_leads ORDER BY lead_id LIMIT 1")[0]

    def lead(lead_id):
        return dict(zip(("status", "clause", "notes", "updated_by_session"), q(
            "SELECT status, clause, notes, updated_by_session FROM research_code_leads "
            "WHERE lead_id=?", lead_id)[0]))

    def code_lead(name, notes=None, **kw):
        return db.insert_code_lead({"jurisdiction": JUR, "status": "REFERENCE-ONLY",
                                    "standard_name": name, "notes": notes}, S, **kw)

    NOTE0 = "fixture: restated on a vendor page, primary text not retrieved"
    NAME1 = "Fixture Standard 4711-2 (ramp provisions)"
    K1 = code_lead(NAME1, NOTE0)
    MOVE_TO = OTHER = None
    if update is None:
        # The pre-WP6 state: no verb. Recorded rather than raised, so the run still
        # prints its summary and exits 1; the near-duplicate cases below still run.
        record("K00", "db.update_code_lead exists (GAP-005's writer)", False,
               "no such function -- a lead's status and note cannot be corrected")
    elif "REFERENCE-ONLY" not in STATUSES or len(STATUSES) < 3:
        record("K00", "the status CHECK still holds the default and two moves to test "
               "with", False, f"CHECK declares {STATUSES}")
    else:
        MOVE_TO, OTHER = [s for s in STATUSES if s != "REFERENCE-ONLY"][:2]
        msg = refusal(update, 999999999, "fixture note", S, status=MOVE_TO)
        record("K01", "refuses an unknown lead", msg and "no such code lead" in msg,
               f"got {msg!r}")
        msg = refusal(update, K1, "   ", S, status=MOVE_TO)
        record("K02", "refuses a blank --append-note (R15) and writes nothing",
               msg and "R15" in msg and lead(K1)["status"] == "REFERENCE-ONLY",
               f"got {msg!r}")
        msg = refusal(update, K1, "fixture note", S, status="FOUND-IT")
        record("K03", "refuses a status outside the column's CHECK, naming the CHECK",
               msg and "CHECK" in msg and lead(K1)["status"] == "REFERENCE-ONLY",
               f"got {msg!r}")
        msg = refusal(update, K1, "fixture note", S, status="REFERENCE-ONLY")
        msg2 = refusal(update, K1, "fixture note", S, clause="  ")
        record("K04", "refuses a --status equal to the held one, and a blank --clause",
               msg and "already" in msg and msg2 and "blank" in msg2, f"{msg!r} | {msg2!r}")
        out = update(K1, "fixture: dry run", S, status=MOVE_TO, dry_run=True)
        record("K05", "--dry-run reports the move and writes nothing",
               out["dry_run"] is True and out["changed"]
               and lead(K1)["status"] == "REFERENCE-ONLY" and lead(K1)["notes"] == NOTE0,
               f"out={out}")
        NOTE1 = "fixture: primary text retrieved; the slope figure is in clause 4.2, not 4.3"
        out = update(K1, f"  {NOTE1}  ", S, status=MOVE_TO, clause="§4.2")
        row = lead(K1)
        record("K06", "a lead moves REFERENCE-ONLY -> " + MOVE_TO + " with a clause: the "
               "old note is kept verbatim, ONE dated UPDATED segment carries the replaced "
               "status and clause and the new note, and the row is stamped",
               out["changed"] and row["status"] == MOVE_TO and row["clause"] == "§4.2"
               and row["notes"].startswith(NOTE0 + " || UPDATED ")
               and row["notes"].count(" || UPDATED ") == 1
               and f"status 'REFERENCE-ONLY' -> '{MOVE_TO}'; clause None -> '§4.2'. "
                   f"{NOTE1}" in row["notes"]
               and row["updated_by_session"] == S, f"out={out} row={row}")
        out = update(K1, "fixture: re-read, the clause holds", S)
        out2 = update(K1, "fixture: re-read, the clause holds", S)
        record("K07", "a note alone is appended (R15 without a status move); the same note "
               "again is a no-op, not a second line",
               out["changed"] and out2["changed"] is False
               and lead(K1)["notes"].count("the clause holds") == 1, f"{out} | {out2}")
        out = update(K1, "fixture: moved back, the retrieval was of a summary", S,
                     status="REFERENCE-ONLY")
        record("K08", "no transition order: a wrong status can be moved back, and the move "
               "is ledgered", out["changed"] and lead(K1)["status"] == "REFERENCE-ONLY"
               and f"status '{MOVE_TO}' -> 'REFERENCE-ONLY'" in lead(K1)["notes"],
               f"out={out}")
        # A note that is only a SUBSTRING of the held text is a new note. The pre-fix
        # check was `note in notes`, so this append was reported as already present and
        # nothing was written.
        K3 = code_lead("Fixture Standard 8080 (substring case)",
                       "fixture: the slope figure is in clause 4.2, not 4.3")
        out = update(K3, "clause 4.2", S)
        out2 = update(K3, "clause 4.2", S)
        record("K16", "a note that is a substring of the held notes is appended, not "
               "mistaken for one already there; the identical note again is a no-op",
               out["changed"] and out2["changed"] is False
               and lead(K3)["notes"].count(" || UPDATED ") == 1
               and lead(K3)["notes"].endswith(": clause 4.2"), f"{out} | {out2}")

        # The exact-duplicate refusal names a command, and the command must work.
        msg = refusal(code_lead, NAME1)
        r = run_cli("update-code-lead", "--lead-id", str(K1), "--append-note",
                    "fixture: the remedy the refusal names", "--status", OTHER,
                    "--session", S, "--dry-run")
        bad = run_cli("update-code-lead", "--lead-id", str(K1), "--append-note", " ",
                      "--session", S)
        record("K09", "an exact restatement refuses with `db.py update-code-lead --lead-id "
               "N`, and that command is wired: a dry run exits 0 and writes nothing; a "
               "blank note exits 1 with REFUSING",
               msg and f"update-code-lead --lead-id {K1}" in msg
               and "Update that row instead" in msg
               and r.returncode == 0 and '"changed": true' in r.stdout
               and lead(K1)["status"] == "REFERENCE-ONLY"
               and bad.returncode == 1 and bad.stderr.startswith("REFUSING:"),
               f"msg={msg!r} r={r.returncode} {r.stderr[-300:]!r} bad={bad.returncode} "
               f"{bad.stderr[-200:]!r}")

    # The near-duplicate refusal is insert_code_lead's, so these cases run whether or
    # not the verb exists: on the pre-WP6 code the variant is simply admitted.
    n0 = q("SELECT COUNT(*) FROM research_code_leads")[0][0]
    VARIANT = "FIXTURE standard 4711 2 — Ramp Provisions"
    msg = refusal(code_lead, VARIANT)
    record("K10", "a case/spacing/punctuation variant of a held name refuses, naming "
           "the held lead and the update command, and writes nothing",
           msg and f"lead_id {K1}" in msg and "update-code-lead" in msg
           and q("SELECT COUNT(*) FROM research_code_leads")[0][0] == n0,
           f"got {msg!r}")
    msg = refusal(code_lead, VARIANT, distinct_from=[K1])
    msg2 = refusal(code_lead, "Fixture Standard 9999", distinct_from=[K1], reason="r")
    msg3 = refusal(code_lead, "Fixture Standard 9999", reason="r")
    record("K11", "--distinct-from without --reason, --distinct-from naming a lead "
           "that is not a near match, and --reason alone all refuse",
           msg and "--reason" in msg and msg2 and "nothing to be distinct from" in msg2
           and msg3 and "only read beside --distinct-from" in msg3,
           f"{msg!r} | {msg2!r} | {msg3!r}")
    WHY_D = "fixture: the 2-part edition and the 2 amendment are separate documents"
    try:
        K2 = code_lead(VARIANT, distinct_from=[K1], reason=WHY_D)
    except Exception as exc:  # noqa: BLE001 -- recorded red, so the run still reports
        K2 = None
        print(f"      {exc.__class__.__name__}: {exc}")
    record("K12", "--distinct-from N --reason admits the variant and records the "
           "reason, naming the lead it is distinct from, in its notes",
           K2 and "DISTINCT-FROM" in (lead(K2)["notes"] or "")
           and f"lead_id {K1}" in lead(K2)["notes"] and WHY_D in lead(K2)["notes"],
           f"K2={K2}")

    # Non-Latin names: the fold must keep the letters. Two different Japanese
    # instruments and a Korean one must not collide, and a spacing variant of one of
    # them must. An ASCII fold turns all three into the empty string: without the
    # writer's empty-key guard they collide (K13 red), and with it every non-Latin
    # variant passes unrefused (K14 red). Both were fault-injected.
    CJK_A, CJK_B = "建築基準法施行令", "高齢者、障害者等の移動等の円滑化の促進に関する法律"
    KO = "장애인·노인·임산부 등의 편의증진 보장에 관한 법률"
    got = {}
    for name in (CJK_A, CJK_B, KO):
        try:
            got[name] = code_lead(name)
        except Exception as exc:  # noqa: BLE001 -- recorded red below
            got[name] = f"{exc.__class__.__name__}: {exc}"
    record("K13", "distinct Japanese and Korean names do not collide",
           all(isinstance(v, int) for v in got.values()), f"got={got}")
    msg = refusal(code_lead, "建築基準法 施行令")
    record("K14", "a spacing variant of a Japanese name does collide, naming the lead "
           "(the fold keeps non-Latin letters)",
           msg and isinstance(got.get(CJK_A), int) and f"lead_id {got[CJK_A]}" in msg,
           f"got {msg!r}")

    if update is not None and MOVE_TO:
        # The capture path, on a CANONICAL lead (an UPDATE, not a fixture INSERT).
        canon = q("SELECT lead_id FROM research_code_leads WHERE status='REFERENCE-ONLY' "
                  "AND created_by_session <> ? ORDER BY lead_id LIMIT 1", S)
        if not canon:
            record("K15", "a canonical REFERENCE-ONLY lead to test capture with", False,
                   "fixture missing in the copy")
        else:
            (CL,) = canon[0]
            try:
                update(CL, "fixture: capture check", S, status=MOVE_TO)
            except Exception as exc:  # noqa: BLE001 -- recorded red below
                print(f"      {exc.__class__.__name__}: {exc}")
            import importlib                                       # noqa: E402
            sys.path.insert(0, str(REPO / "scripts" / "research"))
            emit_mod = importlib.import_module("emit_batch_sql")
            sql_out = os.path.join(TMP, "capture-lead.sql")
            try:
                emit_mod.emit(DB, str(REPO / "data" / "guidebook.db"), sql_out)
                captured = open(sql_out, encoding="utf-8").read()
            except SystemExit as exc:
                captured = f"emit refused: {exc}"
            hit = [ln for ln in captured.splitlines()
                   if ln.startswith('UPDATE "research_code_leads"')
                   and f'"lead_id" = {CL}' in ln and f'"status" = \'{MOVE_TO}\'' in ln
                   and '"updated_by_session"' in ln]
            record("K15", "emit_batch_sql captures update-code-lead's UPDATE of a "
                   "canonical lead (the write can be shipped)", len(hit) == 1,
                   captured[-400:])

    # ── J: the declared jurisdiction vocabulary, refused at write time ─────────────
    # I7. Every value used here is either read from base_jurisdictions / the audit or is one no
    # vocabulary could ever declare ('XX'). The gated tables are DERIVED the way the
    # audit derives them, from its own exclusion sets, so the writers' refusal and the
    # blocking check cannot drift apart unseen.
    import importlib.util                                           # noqa: E402
    _spec = importlib.util.spec_from_file_location(
        "_jdv", REPO / "scripts" / "audit" / "jurisdiction_db_vocabulary.py")
    jdv = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(jdv)
    DECLARED = getattr(dbcore, "declared_jurisdictions", set)()     # empty on a tree without the registry
    REJECTED = jdv.rejected_spellings()
    check_jur = getattr(dbcore, "check_jurisdiction", None)
    UNDECLARED = "XX"
    record("J00", "the fixture code is undeclared and a rejected spelling is parsed",
           UNDECLARED not in DECLARED and bool(REJECTED), f"rejected={REJECTED}")
    BAD, GOOD = next(iter(REJECTED.items()))
    # A declared code admitted in the same change, so J03 also shows the enum was widened.
    NEW = next((c for c in ("PT", "FI", "UN", "UG") if c in DECLARED), None)
    J_TABLES = ("evidence_sources", "evidence_source_authors")

    def jur_of(ref_id):
        rows = q("SELECT jurisdiction FROM evidence_sources WHERE ref_id=?", ref_id)
        return rows[0][0] if rows else "<no row>"

    # THE CASE THAT FAILS ON THE OLD CODE: add-source wrote any string, and the blocking
    # audit found it only after it landed.
    RJ = next_ref()
    before = counts(*J_TABLES)
    r = add_source(RJ, "--jurisdiction", UNDECLARED)
    record("J01", "add-source --jurisdiction XX refuses, names base_jurisdictions and the "
           "audit, and writes nothing",
           r.returncode == 1 and r.stderr.startswith("REFUSING:")
           and "base_jurisdictions" in r.stderr and "jurisdiction_db_vocabulary" in r.stderr
           and counts(*J_TABLES) == before and jur_of(RJ) == "<no row>",
           f"rc={r.returncode} {r.stderr[-300:]!r} {before} -> {counts(*J_TABLES)}")
    r = add_source(RJ, "--jurisdiction", BAD)
    record("J02", f"add-source --jurisdiction {BAD} refuses and names {GOOD}",
           r.returncode == 1 and f"write '{GOOD}'" in r.stderr and jur_of(RJ) == "<no row>",
           f"rc={r.returncode} {r.stderr[-300:]!r}")
    r = add_source(RJ, "--jurisdiction", NEW.lower() if NEW else "pt")
    record("J03", "a case variant of a declared code refuses, naming the declared "
           "spelling (stored codes are compared exactly, so it is not folded)",
           r.returncode == 1 and NEW and f"write '{NEW}'" in r.stderr
           and jur_of(RJ) == "<no row>", f"rc={r.returncode} {r.stderr[-300:]!r}")
    r = add_source(RJ, "--jurisdiction", NEW or "PT")
    record("J04", f"add-source --jurisdiction {NEW} (admitted 2026-10-01) is accepted",
           r.returncode == 0 and NEW and jur_of(RJ) == NEW,
           f"rc={r.returncode} {r.stderr[-300:]!r} stored={jur_of(RJ)!r}")

    n_exec = counts("search_executions")
    msg = refusal(db.log_search, A, "en", "fixture query", "fixture-engine", "keyword", S,
                  jurisdiction=UNDECLARED, prior_expectation="fixture: expect nothing")
    record("J05", "log-search refuses an undeclared jurisdiction before it writes",
           msg and "base_jurisdictions" in msg and counts("search_executions") == n_exec,
           f"got {msg!r}")
    ES_LIKE = (sorted(DECLARED) or ["XX"])[0]
    msg = refusal(db.insert_code_lead, {"jurisdiction": ES_LIKE.lower(),
                                        "standard_name": "Fixture lead J06",
                                        "status": "REFERENCE-ONLY"}, S)
    record("J06", f"add-code-lead refuses '{ES_LIKE.lower()}' and names '{ES_LIKE}' -- its "
           "duplicate checks compare jurisdiction exactly, so a variant would split leads",
           msg and f"write '{ES_LIKE}'" in msg
           and not q("SELECT 1 FROM research_code_leads WHERE standard_name=?",
                     "Fixture lead J06"), f"got {msg!r}")
    msg = refusal(db.insert_extraction, {"ref_id": REF, "parameter_id": 1,
                                         "jurisdiction": UNDECLARED}, S)
    record("J07", "add-extraction refuses an undeclared jurisdiction (by the vocabulary, "
           "before any other check)", msg and "base_jurisdictions" in msg, f"got {msg!r}")
    msg = refusal(db.amend_source, RJ, "jurisdiction", UNDECLARED, "fixture: wrong code", S)
    record("J08", "amend-source --field jurisdiction refuses an undeclared code",
           msg and "base_jurisdictions" in msg and jur_of(RJ) == NEW, f"got {msg!r}")
    OTHER_NEW = next((c for c in ("FI", "UG", "UN", "PT") if c in DECLARED and c != NEW),
                     None)
    out, msg = None, None
    try:
        out = db.amend_source(RJ, "jurisdiction", OTHER_NEW, "fixture: re-scoped", session=S)
    except Exception as exc:  # noqa: BLE001 -- recorded red below
        msg = f"{exc.__class__.__name__}: {exc}"
    record("J09", f"amend-source --field jurisdiction accepts a declared code "
           f"({OTHER_NEW})", out and jur_of(RJ) == OTHER_NEW, f"{msg!r} {jur_of(RJ)!r}")
    msg = refusal(db.insert_economics_entry, {"entry_id": "FIXTURE-J10",
                                              "jurisdiction": "MULTI"}, S)
    record("J10", "add-economics-entry refuses MULTI (its DDL comment's value) by the "
           "vocabulary", msg and "base_jurisdictions" in msg, f"got {msg!r}")

    # Mirror, not stricter: every value LIVE in a table the audit gates passes the
    # writers' refusal, so a real batch writing UK, EU, ISO, INT ... is never blocked by
    # it. Read from the canonical database (read-only), on the audit's own table set.
    canon = sqlite3.connect(f"file:{REPO / 'data' / 'guidebook.db'}?mode=ro", uri=True)
    try:
        gated = [t for (t,) in canon.execute(
                     "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
                 if t not in jdv.EXEMPT | jdv.CANDIDATE_TABLES | jdv.REPORT_ONLY
                 and any(c[1] == "jurisdiction"
                         for c in canon.execute(f'PRAGMA table_info("{t}")'))]
        live = {(t, v) for t in gated for (v,) in canon.execute(
            f'SELECT DISTINCT jurisdiction FROM "{t}" WHERE jurisdiction IS NOT NULL')}
    finally:
        canon.close()
    blocked = sorted((t, v) for t, v in live
                     if check_jur is None or refusal(check_jur, v, "J11") is not None)
    record("J11", f"every value live in the {len(gated)} gated table(s) passes the "
           f"writers' refusal ({len(live)} table/value pair(s))",
           check_jur is not None and live and not blocked, f"blocked {blocked}")

    # And the gate the refusal mirrors is green on the copy after every fixture write
    # above. On the old code J01 had written 'XX' and FI/UG/UN were undeclared.
    r = subprocess.run([sys.executable, str(REPO / "scripts" / "audit" /
                                            "jurisdiction_db_vocabulary.py")],
                       env=dict(os.environ, GUIDEBOOK_DB_PATH=DB),
                       capture_output=True, text=True)
    record("J12", "jurisdiction_db_vocabulary passes on the copy after the writers ran",
           r.returncode == 0 and "VERDICT: PASS" in r.stdout, r.stdout[-400:])

    # J13: conflicts.pop_a / pop_b are foreign keys into the identity lens (migration 121; the item_code
    # column this once guarded is gone). A code the lens lacks is refused by name; the control is the same
    # row with two live codes, because a refusal that also refused that would prove nothing.
    # (`ALL` is the scope marker add-conflict refuses as a population, R3-14; the pair excludes that row.)
    live2 = [c for (c,) in q("SELECT identity_code FROM base_taxonomy_identity WHERE identity_code<>'ALL' "
                             "ORDER BY identity_code LIMIT 2")]
    base = {"conflict_id": "CONF-9999", "domain": "fixture", "pop_a": live2[0], "pop_b": live2[1],
            "status": "PROPOSED",
            # The second active parameter: S15 above already filed this pair on the first, and
            # one conflict per (parameter, pair) is the writer's rule (migration 122).
            "parameter_id": q("SELECT parameter_id FROM base_parameters WHERE status='active' "
                              "ORDER BY parameter_id LIMIT 1 OFFSET 1")[0][0]}
    msg = refusal(db.insert_conflict, {**base, "pop_a": "AAA"}, S, dry_run=True)
    ok_id = None
    try:
        ok_id = db.insert_conflict(base, S, dry_run=True)
    except Exception as exc:  # noqa: BLE001 -- the control failing is a defect to see
        print(f"      CONTROL defect: {exc.__class__.__name__}: {exc}")
    record("J13", "insert_conflict refuses a population the identity lens lacks and still writes the same row with live codes",
           msg is not None and "base_taxonomy_identity" in msg and ok_id == "CONF-9999",
           f"refusal={msg!r} control={ok_id!r}")

    # ── M: log-search records the lens a search covered (R18) ───────────────────────────
    # Three optional columns on search_executions, each checked against the registry its own foreign
    # key names. Through argparse (run_cli), not the function: an unwired flag is invisible to a
    # function call, and the dispatch block is where the flags are passed on.
    lens_live = {"--identity": q("SELECT identity_code FROM base_taxonomy_identity ORDER BY 1 LIMIT 1")[0][0],
                 "--icf": q("SELECT icf_code FROM base_icf ORDER BY 1 LIMIT 1")[0][0],
                 "--needs": q("SELECT need_code FROM access_needs ORDER BY 1 LIMIT 1")[0][0]}

    def ls_lens(label, *extra):
        return run_cli("log-search", "--results-found", "1", "--slug", A, "--language", "EN", "--query-text", f"fixture M: {label}",
                       "--engine", "manual", "--depth-method", "scoping", "--session", S,
                       "--prior-expectation", "fixture prior, written before the call", *extra)

    n_before = counts("search_executions")
    refused = {}
    for flag in ("--identity", "--icf", "--needs"):
        r = ls_lens(f"bad {flag}", flag, "NOT-A-CODE")
        refused[flag] = (r.returncode, "has no matching row in" in (r.stdout + r.stderr))
    record("M01", "log-search refuses an unknown lens code on each of the three flags and writes nothing",
           all(rc != 0 and named for rc, named in refused.values()) and counts("search_executions") == n_before,
           f"{refused} rows {n_before} -> {counts('search_executions')}")
    r = ls_lens("live codes", *[x for kv in lens_live.items() for x in kv])
    row = q("SELECT identity_code, icf_code, needs_code FROM search_executions "
            "WHERE query_text=?", "fixture M: live codes")
    record("M02", "live codes land in their columns",
           r.returncode == 0 and row == [(lens_live["--identity"], lens_live["--icf"], lens_live["--needs"])],
           f"rc={r.returncode} {r.stderr[-300:]} {row}")
    import importlib                                               # noqa: E402
    sys.path.insert(0, str(REPO / "scripts" / "research"))
    emit_mod = importlib.import_module("emit_batch_sql")
    sql_out = os.path.join(TMP, "capture-lens.sql")
    try:
        emit_mod.emit(DB, str(REPO / "data" / "guidebook.db"), sql_out)
        captured = open(sql_out, encoding="utf-8").read()
    except SystemExit as exc:
        captured = f"emit refused: {exc}"
    hit = [ln for ln in captured.splitlines() if ln.startswith('INSERT INTO "search_executions"')
           and "fixture M: live codes" in ln
           # the three lens values, in column order; columns added after them (absence_class,
           # migration 119) follow, so this does not pin where the statement ends
           and ("'%s', '%s', '%s', NULL" % (lens_live["--identity"], lens_live["--icf"], lens_live["--needs"])) in ln]
    record("M03", "emit_batch_sql captures the lens columns of a logged search (the write can be shipped)",
           len(hit) == 1, captured[-400:])

    # ── N: a search with no slug (R43) ──────────────────────────────────────────────────
    # `search_executions.slug` is nullable once the search names a parameter or a mined source;
    # the CHECK refuses all three NULL. Through argparse again, for the same reason as M.
    (PARAM,) = q("SELECT parameter_id FROM base_parameters ORDER BY parameter_id LIMIT 1")[0]

    def ls_bare(label, *extra):
        return run_cli("log-search", "--results-found", "1", "--language", "EN", "--query-text", f"fixture N: {label}",
                       "--engine", "manual", "--depth-method", "scoping", "--session", S,
                       "--prior-expectation", "fixture prior, written before the call", *extra)

    n_before = counts("search_executions")
    r = ls_bare("names nothing")
    record("N01", "log-search refuses a search naming no slug, parameter or mined source, and writes nothing",
           r.returncode != 0 and "names what it looked for" in (r.stdout + r.stderr)
           and counts("search_executions") == n_before, f"rc={r.returncode} {(r.stdout + r.stderr)[-200:]}")
    r = ls_bare("unknown parameter", "--parameter", "999999")
    record("N02", "an unknown --parameter is refused naming its registry, and writes nothing",
           r.returncode != 0 and "has no matching row in" in (r.stdout + r.stderr)
           and counts("search_executions") == n_before, f"rc={r.returncode} {(r.stdout + r.stderr)[-200:]}")
    r = ls_bare("parameter only", "--parameter", str(PARAM))
    row = q("SELECT slug, parameter_id FROM search_executions WHERE query_text=?", "fixture N: parameter only")
    record("N03", "a search naming only a parameter is stored with a NULL slug",
           r.returncode == 0 and row == [(None, PARAM)], f"rc={r.returncode} {r.stderr[-200:]} {row}")

    def ls_cand(exec_id, *extra):
        return run_cli("add-candidate", "--exec-id", str(exec_id), "--disposition", "PENDING-VERIFICATION",
                       "--title", "fixture N candidate", "--surfaced-in", "transcripts/README.md",
                       "--surfaced-quote", "single home for what the agents actually did", "--session", S, *extra)

    (ex_bare,) = q("SELECT exec_id FROM search_executions WHERE query_text=?", "fixture N: parameter only")[0]
    (ex_slug,) = q("SELECT exec_id FROM search_executions WHERE query_text=?", "fixture M: live codes")[0]
    c_before = counts("search_candidates")
    r_no = ls_cand(ex_slug)
    r_bad = ls_cand(ex_slug, "--found-under-slug", "NOT-A-SLUG")
    refused_ok = (r_no.returncode != 0 and "found_under_slug is required" in (r_no.stdout + r_no.stderr)
                  and r_bad.returncode != 0 and "is not in `slugs`" in (r_bad.stdout + r_bad.stderr)
                  and counts("search_candidates") == c_before)
    r_slug_on_bare = ls_cand(ex_bare, "--found-under-slug", A)
    refused_ok = (refused_ok and r_slug_on_bare.returncode != 0
                  and "searched no slug" in (r_slug_on_bare.stdout + r_slug_on_bare.stderr)
                  and counts("search_candidates") == c_before)
    r_ok = ls_cand(ex_bare)
    stored = q("SELECT found_under_slug FROM search_candidates WHERE exec_id=? AND title=?",
               ex_bare, "fixture N candidate")
    record("N04", "a candidate needs --found-under-slug unless its search has no slug, and then refuses one; an unknown slug is still refused",
           refused_ok and r_ok.returncode == 0 and stored == [(None,)],
           f"slugged-no-flag rc={r_no.returncode} bad-slug rc={r_bad.returncode} slugless rc={r_ok.returncode} "
           f"{r_ok.stderr[-200:]} {stored}")
    try:
        emit_mod.emit(DB, str(REPO / "data" / "guidebook.db"), sql_out)
        captured = open(sql_out, encoding="utf-8").read()
    except SystemExit as exc:
        captured = f"emit refused: {exc}"
    hit = [ln for ln in captured.splitlines() if ln.startswith('INSERT INTO "search_executions"')
           and "fixture N: parameter only" in ln and "NULL, %d," % PARAM in ln]
    record("N05", "emit_batch_sql captures a slugless search (the write can be shipped)",
           len(hit) == 1, captured[-400:])

    # ── O: the tier is derived from (evidence_type, scope), never asked for (step 3 evidence) ─────
    from schemas.tier_derivation import TIER_MAP as _TM  # noqa: E402

    def add_o(label, *extra):
        ref = next_ref()
        r = run_cli("add-source", "--ref-id", ref, "--author", "corp|Fixture Body", "--year", "2020",
                    "--title", f"fixture O {label}", "--session", S, *SRC_STANDING, *extra)
        return ref, r

    def tier_of(ref):
        rows = q("SELECT tier FROM evidence_sources WHERE ref_id=?", ref)
        return rows[0][0] if rows else None

    n_src = counts("evidence_sources")
    ref_bad, r_bad = add_o("tier contradicts", "--evidence-type", "grey", "--tier", "1")
    record("O01", "add-source refuses a --tier the ladder does not derive, and writes nothing",
           r_bad.returncode != 0 and "contradicts the ratified ladder" in (r_bad.stdout + r_bad.stderr)
           and counts("evidence_sources") == n_src, f"rc={r_bad.returncode} {(r_bad.stdout + r_bad.stderr)[-200:]}")
    ref_g, r_g = add_o("grey derived", "--evidence-type", "grey")
    ref_c, r_c = add_o("clinical derived", "--evidence-type", "clinical", "--scope", "high_control")
    record("O02", "add-source with no --tier stores the tier the ladder derives",
           r_g.returncode == 0 and r_c.returncode == 0
           and (tier_of(ref_g), tier_of(ref_c)) == (_TM[("grey", "intrinsic")], _TM[("clinical", "high_control")]),
           f"{r_g.stderr[-200:]} {r_c.stderr[-200:]} {(tier_of(ref_g), tier_of(ref_c))}")
    r_am = run_cli("amend-source", "--ref-id", ref_c, "--field", "scope", "--replacement", "lower_control",
                   "--reason", "fixture: re-scoped", "--session", S)
    record("O03", "amend-source --field scope moves the tier to the derived value with no --tier",
           r_am.returncode == 0 and tier_of(ref_c) == _TM[("clinical", "lower_control")],
           f"rc={r_am.returncode} {(r_am.stdout + r_am.stderr)[-200:]} tier={tier_of(ref_c)}")
    n_src = counts("evidence_sources")
    _, r_old = add_o("old co1 type", "--evidence-type", "co1", "--co1-provenance", "fixture: named co-production",
                     "--co1-source-type", "peer_reviewed_literature")
    ref_live, r_live = add_o("live co1 type", "--evidence-type", "co1", "--co1-provenance",
                             "fixture: named co-production", "--co1-source-type", "dpo_position_statement")
    record("O04", "add-source constrains --co1-source-type to the enum: a retired value refuses, a live one lands",
           r_old.returncode != 0 and "is not a member of" in (r_old.stdout + r_old.stderr)
           and r_live.returncode == 0 and counts("evidence_sources")[0] == n_src[0] + 1,
           f"old rc={r_old.returncode} {(r_old.stdout + r_old.stderr)[-150:]} live rc={r_live.returncode} {r_live.stderr[-150:]}")
    r_am_old = run_cli("amend-source", "--ref-id", ref_live, "--field", "co1_source_type", "--replacement",
                       "peer_reviewed_literature", "--reason", "fixture: retired value", "--session", S)
    r_am_ok = run_cli("amend-source", "--ref-id", ref_live, "--field", "co1_source_type", "--replacement",
                      "participatory_research", "--reason", "fixture: live value", "--session", S)
    record("O05", "amend-source --field co1_source_type refuses a value outside the enum and accepts one inside it",
           r_am_old.returncode != 0 and "is not a member of" in (r_am_old.stdout + r_am_old.stderr)
           and r_am_ok.returncode == 0
           and q("SELECT co1_source_type FROM evidence_sources WHERE ref_id=?", ref_live) == [("participatory_research",)],
           f"old rc={r_am_old.returncode} {(r_am_old.stdout + r_am_old.stderr)[-150:]} ok rc={r_am_ok.returncode} {r_am_ok.stderr[-150:]}")

    # ── T-007: add-source through argparse refuses a source with no standing or no type ─────────
    def _bare_add(*standing):
        return run_cli("add-source", "--ref-id", next_ref(), "--author", "corp|Fixture Body", "--year", "2020",
                       "--title", "fixture T007 bare add-source", "--tier", GREY_TIER,
                       "--evidence-type", "grey", "--session", S, *standing)
    n_t7 = counts("evidence_sources")[0]
    r_t7a, r_t7b = _bare_add(), _bare_add(SRC_STANDING[0], SRC_STANDING[1])
    record("T007-05", "add-source with no --verification-status, or with no --source-type, exits non-zero, "
           "names the missing flag and writes no row",
           r_t7a.returncode != 0 and "--verification-status" in r_t7a.stderr
           and r_t7b.returncode != 0 and "--source-type" in r_t7b.stderr
           and counts("evidence_sources")[0] == n_t7,
           f"{r_t7a.returncode} {r_t7a.stderr[-150:]} | {r_t7b.returncode} {r_t7b.stderr[-150:]}")
    n_t7c = counts("evidence_sources")[0]
    r_t7c = _bare_add(*SRC_STANDING)
    record("T007-06", "the same call with both flags lands exactly one row (a positive control: no defect of the refusal turns it red)",
           r_t7c.returncode == 0 and counts("evidence_sources")[0] == n_t7c + 1,
           f"{r_t7c.returncode} {r_t7c.stderr[-200:]}")

    # ── V: an extraction asks for no slug, and a root_id must be registered (step 3 judgment) ───────
    ref_p, _ = add_o("extraction, admitted to no slug", "--evidence-type", "grey")
    readable(ref_p)
    X_P = {"ref_id": ref_p, "parameter_id": PARAM, "identity_code": lens_live["--identity"],
           "claim_type": "absent", "figure_role": "finding",
           "claim_text": "fixture: the source states nothing for this parameter", "extraction_method": "skim",
           "lens_basis": "named_in_text", "lens_basis_text": "states nothing"}
    try:
        got = db.insert_extraction(dict(X_P), S, relations=[], verbatim_exempt=X_EXEMPT)
    except Exception as exc:  # noqa: BLE001 -- recorded red below
        got = {"error": f"{exc.__class__.__name__}: {exc}"}
    n_sve = counts("source_value_extractions")
    msg_root = refusal(db.insert_extraction, {**X_P, "root_id": "NO-SUCH-ROOT"}, S, relations=[],
                       verbatim_exempt=X_EXEMPT)
    msg_slug = refusal(db.insert_extraction, {**X_P, "slug": A}, S, relations=[], verbatim_exempt=X_EXEMPT)
    record("V01", "add-extraction accepts a source admitted to no slug, and stores the row with a NULL slug",
           "extraction_id" in got
           and q("SELECT slug FROM source_value_extractions WHERE extraction_id=?", got.get("extraction_id")) == [(None,)],
           f"{got}")
    record("V02", "an unregistered root_id is refused naming the registry, and a payload naming a slug is refused",
           msg_root and "external_root_registry" in msg_root and msg_slug and "slug" in msg_slug
           and counts("source_value_extractions") == n_sve, f"root={msg_root!r} slug={msg_slug!r}")

    # ── T018: several codes of one model on a figure, by a link table (OR-1c) ─────────────────────
    # Every probe is chosen by query on the copy; every fixture row says TASK-FIXTURE. Every read of
    # the new table or view is guarded, so on a database without them a case records [✗] with the
    # reason and the later cases still run.
    def t018_read(sql, *params):
        try:
            return q(sql, *params), ""
        except sqlite3.Error as exc:
            return None, f"{exc.__class__.__name__}: {exc}"

    def t018_live(extraction_id):
        rows, err = t018_read("SELECT identity_code, icf_code, needs_code, basis FROM "
                              "v_live_lens_links WHERE extraction_id=? ORDER BY link_id", extraction_id)
        return rows, err

    T18_D1, T18_D2 = [c for (c,) in q("SELECT icf_code FROM base_icf WHERE icf_code LIKE 'd%' "
                                      "ORDER BY icf_code LIMIT 2")]
    T18_TEXT = "TASK-FIXTURE T018: the source names two functions on one figure"
    T18_FLAGS = ("--claim-type", "absent", "--figure-role", "finding", "--relation", "none",
                 "--extraction-method", "skim", "--verbatim-exempt", "TASK-FIXTURE: no artefact carries it",
                 "--session", S)

    def t018_cmd(ref, label, *lens_and_extra):
        return ("add-extraction", "--ref-id", ref, "--parameter-id", str(PARAM), *lens_and_extra,
                "--claim-text", f"{T18_TEXT} ({label})", *T18_FLAGS)

    def t018_add(label, *lens_and_extra):
        ref, _ = add_o(f"T018 {label}", "--evidence-type", "grey")
        readable(ref)
        r = run_cli(*t018_cmd(ref, label, *lens_and_extra))
        got = q("SELECT extraction_id FROM source_value_extractions WHERE ref_id=?", ref)
        return r, (got[0][0] if got else None)

    # T018-01 (AT-32, first half): one figure, two ICF codes, two links.
    r01, fig01 = t018_add("two icf", "--icf", T18_D1, "--icf", T18_D2, "--lens-basis", "named_in_text",
                          "--lens-basis-text", "TASK-FIXTURE")
    live01, err01 = t018_live(fig01) if fig01 else (None, "no figure was written")
    cols01 = q("SELECT identity_code, icf_code, needs_code FROM source_value_extractions "
               "WHERE extraction_id=?", fig01) if fig01 else None
    record("T018-01", "one figure with two ICF codes is stored once with two live links, and its own lens columns stay NULL",
           r01.returncode == 0 and live01 is not None
           and sorted((x[1], x[3]) for x in live01) == sorted([(T18_D1, "named_in_text"), (T18_D2, "named_in_text")])
           and cols01 == [(None, None, None)],
           f"rc={r01.returncode} {(r01.stdout + r01.stderr)[-250:]!r} links={live01} {err01} cols={cols01}")

    # A figure with exactly one link, for T018-02 and -03.
    r_b, fig_b = t018_add("one identity", "--identity", POP, "--lens-basis", "named_in_text",
                          "--lens-basis-text", "TASK-FIXTURE")
    only, err_b = t018_live(fig_b) if fig_b else (None, "no figure was written")
    only_id = t018_read("SELECT link_id FROM v_live_lens_links WHERE extraction_id=?", fig_b)[0] if fig_b else None
    n_links = t018_read("SELECT COUNT(*) FROM extraction_lens_links")[0]
    r02 = run_cli("retire-lens-link", "--link-id", str(only_id[0][0] if only_id else 0),
                  "--reason", "TASK-FIXTURE: retiring a figure's last link", "--session", S)
    out02 = r02.stdout + r02.stderr
    record("T018-02", "retire-lens-link refuses a figure's last live link, names add-lens-link, and writes nothing",
           r02.returncode != 0 and "add-lens-link" in out02 and only is not None and len(only) == 1
           and t018_read("SELECT COUNT(*) FROM v_live_lens_links WHERE extraction_id=?", fig_b)[0] == [(1,)]
           and t018_read("SELECT COUNT(*) FROM extraction_lens_links")[0] == n_links,
           f"rc={r02.returncode} {out02[-250:]!r} probe={only} {err_b}")

    # T018-03: a warrant that is nowhere in the figure's words is refused, naming where it looked.
    r03 = run_cli("add-lens-link", "--extraction-id", str(fig_b or 0), "--icf", T18_D2,
                  "--basis", "named_in_text", "--basis-text", "zq-not-in-the-figure-xq", "--session", S)
    out03 = r03.stdout + r03.stderr
    record("T018-03", "add-lens-link refuses a --basis-text found in neither the figure's words nor its source's file, and says where it looked",
           r03.returncode != 0 and "claim_text" in out03 and "zq-not-in-the-figure-xq" in out03
           and t018_read("SELECT COUNT(*) FROM extraction_lens_links")[0] == n_links,
           f"rc={r03.returncode} {out03[-300:]!r}")

    # T018-04 / T018-08: a judged link replaces a carried one in one call, and the captured batch replays.
    probe04, err04 = t018_read(
        "SELECT k.link_id, k.extraction_id, k.identity_code, x.claim_text FROM v_live_lens_links k "
        "JOIN source_value_extractions x ON x.extraction_id = k.extraction_id "
        "JOIN base_taxonomy_identity i ON i.identity_code = k.identity_code AND i.status = 'active' "
        "WHERE k.basis = 'carried' AND TRIM(COALESCE(x.claim_text, '')) <> '' ORDER BY k.link_id LIMIT 1")
    base_copy = os.path.join(TMP, "t018-base.db")
    shutil.copy(DB, base_copy)
    if probe04:
        l04, fig04, code04, ct04 = probe04[0]
        word04 = max(re.findall(r"\w+", ct04), key=len)
        r04 = run_cli("add-lens-link", "--extraction-id", str(fig04), "--identity", code04,
                      "--basis", "named_in_text", "--basis-text", word04, "--session", S)
        rows04, e04 = t018_read("SELECT link_id, basis, basis_text FROM v_live_lens_links "
                                "WHERE extraction_id=? AND identity_code=?", fig04, code04)
        old04, e04b = t018_read("SELECT retired_at IS NOT NULL, retirement_reason FROM extraction_lens_links "
                                "WHERE link_id=?", l04)
        new_id = rows04[0][0] if rows04 else None
        ok04 = (r04.returncode == 0 and rows04 is not None and len(rows04) == 1
                and rows04[0][1:] == ("named_in_text", word04) and old04 is not None
                and old04[0][0] == 1 and old04[0][1] == f"superseded by judged link {new_id}")
        detail04 = f"rc={r04.returncode} {(r04.stdout + r04.stderr)[-250:]!r} live={rows04} {e04} old={old04} {e04b}"
    else:
        ok04, detail04 = False, f"no carried identity link to probe (v_live_lens_links: {err04 or 'empty'})"
    record("T018-04", "add-lens-link on a code that has a carried link retires it ('superseded by judged link <id>') and leaves one live link",
           ok04, detail04)

    # T018-08: the capture replays. emit_mod is imported where case M03 reads the lens columns.
    sql08 = os.path.join(TMP, "t018-replay.sql")
    try:
        emit_mod.emit(DB, base_copy, sql08, replay_path=base_copy)
        replay_copy = os.path.join(TMP, "t018-replayed.db")
        shutil.copy(base_copy, replay_copy)
        import migrate_db                                            # noqa: E402
        con08 = sqlite3.connect(replay_copy, isolation_level=None)
        try:
            migrate_db._apply_atomically(con08, migrate_db._split_statements(open(sql08, encoding="utf-8").read()),
                                         label="T018-08 replay")
        finally:
            con08.close()
        want = q("SELECT * FROM extraction_lens_links ORDER BY link_id")
        got = sqlite3.connect(replay_copy).execute("SELECT * FROM extraction_lens_links ORDER BY link_id").fetchall()
        ok08, detail08 = bool(probe04) and want == got and len(want) > 0, f"scratch {len(want)} rows, replay {len(got)} rows"
    except BaseException as exc:  # noqa: BLE001 -- SystemExit from emit, IntegrityError from the replay
        ok08, detail08 = False, f"{exc.__class__.__name__}: {exc}"
    record("T018-08", "the captured batch replays: applying emit_batch_sql's output to the base reproduces extraction_lens_links row for row",
           ok08, detail08)

    # T018-07: the figure's own lens columns are a dead home: a hand-written INSERT naming one is refused.
    con07 = sqlite3.connect(DB)
    try:
        con07.execute("INSERT INTO source_value_extractions (ref_id, parameter_id, identity_code, claim_type, "
                      "extraction_method, created_at, updated_at) VALUES (?, ?, ?, 'absent', 'skim', 't', 't')",
                      (REF, PARAM, POP))
        out07 = None
    except sqlite3.IntegrityError as exc:
        out07 = str(exc)
    finally:
        con07.rollback()
        con07.close()
    record("T018-07", "a hand-written INSERT into source_value_extractions that names a lens column is refused by the table's CHECK",
           out07 is not None and "CHECK constraint failed" in out07, f"got {out07!r}")

    # ── T018, continued: each refusal of the link writers fires, and the legitimate shape still passes ──
    # A figure with one identity link (fig_b) and one with two ICF links (fig01) exist from above.
    def out_of(r):
        return r.stdout + r.stderr

    def n_figures():
        return counts("source_value_extractions")[0]

    def n_links_now():
        rows, _ = t018_read("SELECT COUNT(*) FROM extraction_lens_links")
        return rows[0][0] if rows else -1

    BASIS = ("--lens-basis", "named_in_text", "--lens-basis-text", "TASK-FIXTURE")
    ref09, _ = add_o("T018 refusals", "--evidence-type", "grey")
    readable(ref09)

    # T018-09: a figure with no lens at all is refused (D-0182), whatever else is right with it.
    nf, nl = n_figures(), n_links_now()
    r09 = run_cli(*t018_cmd(ref09, "no lens", *BASIS))
    record("T018-09", "add-extraction with no lens flag is refused in the D-0182 words, and writes no figure and no link",
           r09.returncode != 0 and "at least one lens" in out_of(r09) and n_figures() == nf and n_links_now() == nl,
           f"rc={r09.returncode} {out_of(r09)[-250:]!r}")

    # T018-10: one code twice in a call is refused by name, before any write.
    r10 = run_cli(*t018_cmd(ref09, "twice", "--icf", T18_D1, "--icf", T18_D1, *BASIS))
    record("T018-10", "add-extraction with one code repeated in a call is refused ('more than once') and writes nothing",
           r10.returncode != 0 and "more than once" in out_of(r10) and n_figures() == nf and n_links_now() == nl,
           f"rc={r10.returncode} {out_of(r10)[-250:]!r}")

    # T018-11: a blank warrant, and a code the registry does not hold, are each refused in words.
    r11a = run_cli("add-lens-link", "--extraction-id", str(fig_b), "--icf", T18_D2, "--basis", "named_in_text",
                   "--basis-text", "   ", "--session", S)
    r11b = run_cli("add-lens-link", "--extraction-id", str(fig_b), "--icf", "NOT-A-CODE", "--basis", "named_in_text",
                   "--basis-text", "TASK-FIXTURE", "--session", S)
    record("T018-11", "add-lens-link refuses a blank --basis-text and an unknown code, each in words",
           r11a.returncode != 0 and "blank" in out_of(r11a)
           and r11b.returncode != 0 and "is not a live icf_code" in out_of(r11b)
           and n_links_now() == nl,
           f"{out_of(r11a)[-120:]!r} | {out_of(r11b)[-120:]!r}")

    # T018-11b: a lens registry with no row is named, not left to `FOREIGN KEY constraint failed`. No live registry is
    # empty any more (the medical one, the only one that was, was deleted 2026-11-16), so the refusal is exercised on a
    # one-table in-memory database: the code is generic over every registry `_LENS_COLUMNS` names.
    import db as _db_t18
    _mem = sqlite3.connect(":memory:")
    _tbl, _key = _db_t18._LENS_COLUMNS["icf_code"]
    _mem.execute(f'CREATE TABLE "{_tbl}" ("{_key}" TEXT PRIMARY KEY)')
    try:
        _db_t18._require_lens_code(_mem, "icf_code", "ANY")
        _empty_msg = None
    except _db_t18.Refusal as _e:
        _empty_msg = str(_e)
    record("T018-11b", "a lens code against an EMPTY registry is refused in words ('holds no rows'), not left to the foreign key",
           bool(_empty_msg) and "holds no rows" in _empty_msg and _tbl in _empty_msg, repr(_empty_msg)[:200])

    # T018-12: a retired identity is not newly used, by either writer. The state is set by SQL on the copy and undone.
    (dep,) = q("SELECT identity_code FROM base_taxonomy_identity WHERE status='active' AND identity_code NOT IN ('ALL', ?) "
               "ORDER BY identity_code LIMIT 1", POP)[0]
    w("UPDATE base_taxonomy_identity SET status='deprecated', superseded_by_need=(SELECT need_code FROM access_needs "
      "ORDER BY need_code LIMIT 1) WHERE identity_code=?", dep)          # the table's CHECK now requires a successor (T-054)
    try:
        r12a = run_cli("add-lens-link", "--extraction-id", str(fig_b), "--identity", dep, "--basis", "named_in_text",
                       "--basis-text", "TASK-FIXTURE", "--session", S)
        r12b = run_cli(*t018_cmd(ref09, "deprecated", "--identity", dep, *BASIS))
    finally:
        w("UPDATE base_taxonomy_identity SET status='active', superseded_by_need=NULL WHERE identity_code=?", dep)
    record("T018-12", "add-lens-link and add-extraction refuse a deprecated identity code and write nothing",
           r12a.returncode != 0 and "deprecated" in out_of(r12a) and r12b.returncode != 0 and "deprecated" in out_of(r12b)
           and n_figures() == nf and n_links_now() == nl, f"{out_of(r12a)[-160:]!r} | {out_of(r12b)[-160:]!r}")

    # T018-13: add-lens-link names exactly one code and an existing figure.
    r13a = run_cli("add-lens-link", "--extraction-id", str(fig_b), "--basis", "named_in_text",
                   "--basis-text", "TASK-FIXTURE", "--session", S)
    r13b = run_cli("add-lens-link", "--extraction-id", str(fig_b), "--icf", T18_D2, "--identity", POP, "--basis",
                   "named_in_text", "--basis-text", "TASK-FIXTURE", "--session", S)
    r13c = run_cli("add-lens-link", "--extraction-id", "0", "--icf", T18_D2, "--basis", "named_in_text",
                   "--basis-text", "TASK-FIXTURE", "--session", S)
    record("T018-13", "add-lens-link refuses no code, two codes, and a figure that does not exist",
           r13a.returncode != 0 and "exactly one" in out_of(r13a) and r13b.returncode != 0 and "exactly one" in out_of(r13b)
           and r13c.returncode != 0 and "no such figure" in out_of(r13c) and n_links_now() == nl,
           f"{out_of(r13a)[-100:]!r} | {out_of(r13b)[-100:]!r} | {out_of(r13c)[-100:]!r}")

    # T018-14: the basis vocabulary is the column's CHECK minus `carried`, at the parser and in the writer.
    r14a = run_cli("add-lens-link", "--extraction-id", str(fig_b), "--icf", T18_D2, "--basis", "carried",
                   "--basis-text", "TASK-FIXTURE", "--session", S)
    r14b = refusal(db.add_lens_link, fig_b, S, icf=T18_D2, basis="carried", basis_text="TASK-FIXTURE")
    r14c = refusal(db.add_lens_link, fig_b, S, icf=T18_D2, basis="not-a-basis", basis_text="TASK-FIXTURE")
    record("T018-14", "'carried' is refused as a basis by the parser and by the writer, as is a value outside the CHECK",
           r14a.returncode != 0 and "invalid choice" in out_of(r14a)
           and r14b and "a lens link needs" in r14b and r14c and "a lens link needs" in r14c and n_links_now() == nl,
           f"{out_of(r14a)[-120:]!r} | {r14b!r} | {r14c!r}")

    # T018-15: a second judged link for a code is refused (only a carried one is replaced); then it is the live one.
    r15a = run_cli("add-lens-link", "--extraction-id", str(fig_b), "--icf", T18_D2, "--basis", "named_in_text",
                   "--basis-text", "TASK-FIXTURE", "--session", S)
    n_after_first = n_links_now()
    r15b = run_cli("add-lens-link", "--extraction-id", str(fig_b), "--icf", T18_D2, "--basis", "named_in_text",
                   "--basis-text", "TASK-FIXTURE", "--session", S)
    record("T018-15", "add-lens-link writes a new code's link, and refuses the same code again naming the live link",
           r15a.returncode == 0 and n_after_first == nl + 1 and r15b.returncode != 0
           and "already holds a live" in out_of(r15b) and n_links_now() == n_after_first,
           f"{out_of(r15a)[-160:]!r} | {out_of(r15b)[-200:]!r}")

    # T018-16: retire-lens-link, link by link, on fig01 (two live links).
    l01 = [r[0] for r in q("SELECT link_id FROM v_live_lens_links WHERE extraction_id=? ORDER BY link_id", fig01)] if fig01 else []
    if len(l01) == 2:
        rb = run_cli("retire-lens-link", "--link-id", str(l01[0]), "--reason", "   ", "--session", S)
        r1 = run_cli("retire-lens-link", "--link-id", str(l01[0]), "--reason", "TASK-FIXTURE: retire the first", "--session", S)
        r1b = run_cli("retire-lens-link", "--link-id", str(l01[0]), "--reason", "TASK-FIXTURE: again", "--session", S)
        r2 = run_cli("retire-lens-link", "--link-id", str(l01[1]), "--reason", "TASK-FIXTURE: the last", "--session", S)
        r0 = run_cli("retire-lens-link", "--link-id", "0", "--reason", "TASK-FIXTURE: none", "--session", S)
        live01 = q("SELECT link_id FROM v_live_lens_links WHERE extraction_id=?", fig01)
        total01 = q("SELECT COUNT(*) FROM extraction_lens_links WHERE extraction_id=?", fig01)[0][0]
        ok16 = (rb.returncode != 0 and "blank" in out_of(rb) and r1.returncode == 0
                and r1b.returncode != 0 and "was retired" in out_of(r1b)
                and r2.returncode != 0 and "last live link" in out_of(r2)
                and r0.returncode != 0 and "no such link" in out_of(r0)
                and live01 == [(l01[1],)] and total01 == 2)
        detail16 = f"{[out_of(x)[-90:] for x in (rb, r1, r1b, r2, r0)]} live={live01} total={total01}"
    else:
        ok16, detail16 = False, f"no figure with two live links to retire from: {l01}"
    record("T018-16", "retire-lens-link refuses a blank reason, an already-retired link, no such link and the last LIVE link "
           "(counted over live links, though the figure holds two rows)", ok16, detail16)

    # T018-17: the warrant is looked for where its basis says, on word boundaries.
    ref17, _ = add_o("T018 warrants", "--evidence-type", "grey")
    readable(ref17)
    HEAD = "TASK-FIXTURE Heading Alpha"
    r17 = run_cli(*t018_cmd(ref17, "warrants - dash", "--identity", POP, *BASIS, "--source-section", HEAD))
    fig17 = (q("SELECT extraction_id FROM source_value_extractions WHERE ref_id=?", ref17) or [(None,)])[0][0]
    needs17 = q("SELECT need_code FROM access_needs ORDER BY need_code LIMIT 1")[0][0]

    def link17(code_flag, code, basis, text):
        return run_cli("add-lens-link", "--extraction-id", str(fig17), code_flag, code, "--basis", basis,
                       "--basis-text", text, "--session", S)
    n17 = n_links_now()
    refused17 = {
        "a heading basis, words only in the claim text": link17("--icf", T18_D1, "heading", "two functions"),
        "a named_in_text basis, words only in the heading": link17("--icf", T18_D1, "named_in_text", "Heading Alpha"),
        "a study_participants basis, words only in the claim text": link17("--icf", T18_D1, "study_participants", "two functions"),
        "a one-letter warrant": link17("--icf", T18_D1, "named_in_text", "e"),
        "a warrant with no letter or digit": link17("--icf", T18_D1, "named_in_text", "."),
        "a warrant with no letter or digit that the text does hold": link17("--icf", T18_D1, "named_in_text", "-"),
        "the front of a word": link17("--icf", T18_D1, "named_in_text", "function"),
        "the middle of a word": link17("--icf", T18_D1, "named_in_text", "unction"),
    }
    missed17 = [k for k, v in refused17.items() if v.returncode == 0]
    nothing17 = n_links_now() == n17
    ok_head = link17("--icf", T18_D1, "heading", "Heading Alpha")
    ok_text = link17("--icf", T18_D2, "named_in_text", "two functions")
    record("T018-17", "a warrant is looked for where its basis says and on word boundaries; each wrong place and each fragment is refused, "
           "and the right one lands",
           r17.returncode == 0 and fig17 and not missed17 and nothing17 and ok_head.returncode == 0 and ok_text.returncode == 0,
           f"create={out_of(r17)[-150:]!r} not refused: {missed17} wrote_nothing={nothing17} head={out_of(ok_head)[-150:]!r} "
           f"text={out_of(ok_text)[-150:]!r}")

    # T018-18: study_participants reads the graded study population; the saved-file route is consulted for named_in_text.
    grade = sorted(dbcore.check_values(sqlite3.connect(DB), "evidence_population_match", "match_grade"))[0]
    w("INSERT INTO evidence_population_match (match_id, source_ref, target_population, study_population, match_grade, "
      "created_at, created_by_session, ref_id) VALUES (?, ?, ?, ?, ?, 't', ?, ?)",
      f"TASK-FIXTURE-{ref17}", ref17, POP, "TASK-FIXTURE participants Zeta", grade, S, ref17)
    r18a = link17("--needs", needs17, "study_participants", "participants Zeta")
    r18b = link17("--icf", "NOT-A-CODE", "study_participants", "participants Zeta")
    PHRASE = "TASK-FIXTURE phrase only in a saved file"
    (T18_D3,) = q("SELECT icf_code FROM base_icf WHERE icf_code LIKE 'd%' ORDER BY icf_code LIMIT 1 OFFSET 2")[0]
    rl = db._retrieval_log()
    _real = rl.locate_quote

    def via(kind):
        """add-lens-link in process, with the quote verifier answering `kind` for the phrase (no artefact is saved for a fixture)."""
        rl.locate_quote = lambda quote, ref_id=None, session=None: (kind, "TASK-FIXTURE verdict")
        try:
            try:
                return db.add_lens_link(fig17, S, icf=T18_D3, basis="named_in_text", basis_text=PHRASE, dry_run=True)
            except Refusal as exc:
                return {"refused": str(exc)}
            except Exception as exc:  # noqa: BLE001 -- recorded red below
                return {"error": f"{exc.__class__.__name__}: {exc}"}
        finally:
            rl.locate_quote = _real
    scoped, unscoped, missing = via("scoped"), via("unscoped"), via("missing")
    record("T018-18", "study_participants is found in the graded study_population, and named_in_text accepts a SCOPED hit in the source's saved "
           "file and refuses an unscoped or missing one",
           r18a.returncode == 0 and r18b.returncode != 0
           and scoped.get("link_id") and scoped.get("dry_run") is True
           and "is not, on word boundaries" in unscoped.get("refused", "")
           and "is not, on word boundaries" in missing.get("refused", ""),
           f"{out_of(r18a)[-150:]!r} | {out_of(r18b)[-100:]!r} | {scoped!r} | {unscoped!r} | {missing!r}")

    # T018-19: the lens is not part of a figure's identity: the same reading in another code is add-lens-link, never a second figure.
    ref19, _ = add_o("T018 identical", "--evidence-type", "grey")
    readable(ref19)
    first19 = run_cli(*t018_cmd(ref19, "same reading", "--icf", T18_D1, *BASIS))
    nf19 = n_figures()
    again19 = run_cli(*t018_cmd(ref19, "same reading", "--icf", T18_D2, *BASIS))
    other19 = run_cli(*t018_cmd(ref19, "another reading", "--icf", T18_D1, *BASIS))
    record("T018-19", "the same row in another lens code is refused naming add-lens-link; a different row for the same source is accepted",
           first19.returncode == 0 and again19.returncode != 0 and "add-lens-link" in out_of(again19)
           and n_figures() == nf19 + 1 and other19.returncode == 0,
           f"{out_of(first19)[-100:]!r} | {out_of(again19)[-200:]!r} | {out_of(other19)[-100:]!r} figures {nf19} -> {n_figures()}")

    # T018-20: a lens code that is not text is a Refusal, not a TypeError.
    r20a = refusal(db.insert_extraction, {"ref_id": REF, "parameter_id": PARAM, "identity_code": 5}, S, relations=[])
    r20b = refusal(db.add_lens_link, fig_b, S, icf=["d1"], basis="named_in_text", basis_text="TASK-FIXTURE")
    record("T018-20", "a lens code that is not text is refused in words by both writers",
           r20a and "is text" in r20a and r20b and "as text" in r20b, f"{r20a!r} | {r20b!r}")

    # ── T126: a code value's lens is judged from its context when its row is recorded; the maps propose ────────────
    # Every code is derived from the copy's registries; where one is not live yet (the Reaching code before it is minted) the
    # fixture mints it on the COPY only, with one identity_icf_map row joining the wheelchair-user identity to it, and
    # says so, so the case keeps asserting the path once the live row exists. The clause and the source's scope clause
    # are saved as a real file for the fixture source (and another for a second source) in the fixture retrieval-log root.
    sys.path.insert(0, str(REPO / "scripts" / "assess"))
    import assess_cell as _t126_engine                                 # noqa: E402

    def t126_first(sql, *params):
        rows = q(sql, *params)
        return rows[0][0] if rows else None

    T126_CTX = ("--claim-type", "absent", "--figure-role", "finding", "--relation", "none",
                "--extraction-method", "skim", "--session", S)
    T126_REASON = "typically concerns wheelchair users"
    reach126 = t126_first("SELECT icf_code FROM base_icf WHERE lower(coalesce(title,'')) LIKE '%reaching%' ORDER BY icf_code")
    wheel126 = t126_first(
        "SELECT i.identity_code FROM base_taxonomy_identity i WHERE i.status='active' AND lower(i.display_name||' '||"
        "coalesce(i.description,'')) LIKE '%wheelchair%' ORDER BY (SELECT COUNT(*) FROM base_taxonomy_identity c "
        "WHERE c.parent_code = i.identity_code AND c.status='active'), i.parent_code IS NULL, i.identity_code")
    need126 = t126_first("SELECT need_code FROM access_needs WHERE lower(coalesce(design_obligation,'')) LIKE '%reachable%' "
                         "AND lower(design_obligation) LIKE '%seated%' ORDER BY need_code")
    clear126 = t126_first("SELECT icf_code FROM base_icf WHERE lower(coalesce(title,'')) LIKE '%moving around using equipment%'")
    blind126 = t126_first("SELECT identity_code FROM base_taxonomy_identity WHERE status='active' AND "
                          "lower(display_name) LIKE '%blind%' AND lower(display_name) LIKE '%low%vision%'")
    reach_fixture = reach126 is None
    if reach_fixture:
        reach126 = "d4452"
        w("INSERT INTO base_icf (icf_code, component, title, title_source, created_at, created_by_session) "
          "VALUES (?, 'd', 'Reaching', 'TASK-FIXTURE T126', 't', ?)", reach126, S)
    if wheel126 and not q("SELECT 1 FROM identity_icf_map WHERE identity_code=? AND icf_code=? AND retired_at IS NULL",
                          wheel126, reach126):
        w("INSERT INTO identity_icf_map (identity_code, icf_code, mechanism, mapping_confidence, provenance, created_at, "
          "created_by_session) VALUES (?, ?, 'TASK-FIXTURE seated reach', 'moderate_contextual', 'TASK-FIXTURE T126', "
          "'2026-01-01 00:00', ?)", wheel126, reach126, S)
    print(f"      T126 codes: reach {reach126} ({'fixture row' if reach_fixture else 'live'}), need {need126}, "
          f"identity {wheel126}, clearance {clear126}, override {blind126}")

    T126_CLAUSE = "TASK-FIXTURE T126 Controls shall be mounted at a height of not more than 1200 mm"
    T126_KNEE = "TASK-FIXTURE T126 Knee clearance under the counter shall be not less than 685 mm"
    T126_PROTRUDE = ("TASK-FIXTURE T126 Objects protruding more than 100 mm into the path shall be detectable by "
                     "people who are blind or have low vision")
    T126_SCOPE = "TASK-FIXTURE T126 This section applies to sanitary rooms in assembly occupancies"
    T126_OTHER = "TASK-FIXTURE T126 phrase saved only for another source"
    log_root = pathlib.Path(os.environ["GUIDEBOOK_RETRIEVAL_LOG"]) / "task-fixture-t126"
    log_root.mkdir(parents=True, exist_ok=True)

    def t126_save(ref, name, body):
        (log_root / name).write_text(body, encoding="utf-8")
        with open(log_root / "manifest.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"ref_id": ref, "artefact": name, "content_type": "text/plain",
                                 "url": f"https://example.org/task-fixture/{name}"}) + "\n")

    code126, _ = add_o("T126 code", "--evidence-type", "code")
    readable(code126)
    other126, _ = add_o("T126 other code", "--evidence-type", "code")
    readable(other126)
    grey126, _ = add_o("T126 research", "--evidence-type", "grey")
    readable(grey126)
    t126_save(code126, "t126-code.txt", "\n".join([T126_SCOPE, T126_CLAUSE, T126_KNEE, T126_PROTRUDE]))
    t126_save(other126, "t126-other.txt", T126_OTHER)
    t126_save(grey126, "t126-grey.txt", T126_CLAUSE)

    def t126_add(ref, clause, *lens, section="TASK-FIXTURE T126 Section 3.8"):
        r = run_cli("add-extraction", "--ref-id", ref, "--parameter-id", str(PARAM), *lens, "--claim-text", clause,
                    "--source-section", section, *T126_CTX)
        got = q("SELECT extraction_id FROM source_value_extractions WHERE ref_id=? AND claim_text=? "
                "ORDER BY extraction_id DESC", ref, clause)
        try:
            res = json.loads(r.stdout) if r.returncode == 0 else {}
        except ValueError:
            res = {}
        return r, (got[0][0] if got else None), res

    def t126_links(fig):
        return t018_read("SELECT identity_code, icf_code, needs_code, basis, basis_text, basis_reason FROM "
                         "v_live_lens_links WHERE extraction_id=? ORDER BY link_id", fig)

    CTX = lambda words: ("--lens-basis", "context", "--lens-basis-text", words, "--lens-basis-reason", T126_REASON)  # noqa: E731

    # T126-01: the owner's mounting-height default: three links by context, the proposal shown, the cell gathers it.
    r01_, fig126, res01 = t126_add(code126, T126_CLAUSE, "--icf", reach126, "--needs", need126, "--identity", wheel126,
                                   *CTX("mounted at a height"))
    links01, e01 = t126_links(fig126) if fig126 else (None, "no figure")
    gathered = None
    if fig126:
        _gc = sqlite3.connect(DB)
        try:
            gathered = [g for g in _t126_engine.gather_extraction_links(_gc, PARAM, [], {"identity_code": wheel126})
                        if g["extraction_id"] == fig126]
        except Exception as exc:  # noqa: BLE001 -- recorded red below
            gathered = f"{exc.__class__.__name__}: {exc}"
        finally:
            _gc.close()
    record("T126-01", "a mounting-height code row is recorded with the reach ICF code, the reach need and the wheelchair-user "
           "identity by context, the words and the reason in two cells; the map's proposal is printed and returned, "
           "and the identity cell gathers the figure",
           r01_.returncode == 0 and links01 is not None and len(links01) == 3
           and all(l[3:] == ("context", "mounted at a height", T126_REASON) for l in links01)
           and res01.get("identities_proposed") and wheel126 in res01["identities_proposed"]
           and res01.get("identities_written") == [wheel126]
           and f"{wheel126}: via ICF {reach126}" in r01_.stderr and "moderate_contextual" in r01_.stderr
           and "provenance" in r01_.stderr
           and isinstance(gathered, list) and len(gathered) == 1 and gathered[0]["in_lens"],
           f"rc={r01_.returncode} {out_of(r01_)[-300:]!r} links={links01} {e01} res={res01} gathered={gathered}")

    # T126-02: knee clearance, the second default; the live map proposes the wheelchair-user family for the clearance code.
    r02_, fig02_, res02 = t126_add(code126, T126_KNEE, "--icf", clear126, "--needs", need126, "--identity", wheel126,
                                   *CTX("knee clearance"))
    live_prop02 = [c for (c,) in q("SELECT DISTINCT identity_code FROM identity_icf_map WHERE icf_code=? AND retired_at "
                                   "IS NULL ORDER BY 1", clear126)]
    record("T126-02", "a knee-clearance code row is recorded with the clearance ICF code, the reach need and the wheelchair-user "
           "identity by context; the proposals are the live map's rows for the clearance code",
           r02_.returncode == 0 and fig02_ and live_prop02 and wheel126 in live_prop02
           and set(live_prop02) <= set(res02.get("identities_proposed") or ())
           and res02.get("identities_written") == [wheel126],
           f"rc={r02_.returncode} {out_of(r02_)[-300:]!r} res={res02} live map={live_prop02}")

    # T126-03: the override: a protruding-object clause that names its group is written for that group, by named_in_text,
    # with none of the default's links; the skill names the override. No code chooses the lens.
    skill126 = (REPO / "skills" / "run-pipeline_SKILL.md").read_text(encoding="utf-8")
    r03_, fig03_, res03 = t126_add(code126, T126_PROTRUDE, "--identity", blind126, "--lens-basis", "named_in_text",
                                   "--lens-basis-text", "blind or have low vision")
    links03, _ = t126_links(fig03_) if fig03_ else (None, "")
    record("T126-03", "a protruding-object clause naming people who are blind or have low vision is written for that group by "
           "named_in_text with no default link, and the skill's guidance names the override",
           r03_.returncode == 0 and links03 == [(blind126, None, None, "named_in_text", "blind or have low vision", None)]
           and "protruding" in skill126 and "Overridden where the clause names another group" in skill126,
           f"rc={r03_.returncode} {out_of(r03_)[-250:]!r} links={links03}")

    # T126-04: context below tier 4 is refused, naming the sixteenth set; nothing is written.
    nf4, nl4 = n_figures(), n_links_now()
    r04_, fig04_, _ = t126_add(grey126, T126_CLAUSE, "--icf", reach126, *CTX("mounted at a height"))
    record("T126-04", "basis context on a source below tier 4 is refused naming the sixteenth set, and writes nothing",
           r04_.returncode != 0 and "sixteenth set" in out_of(r04_) and n_figures() == nf4 and n_links_now() == nl4,
           f"rc={r04_.returncode} {out_of(r04_)[-250:]!r}")

    # T126-05: context with a blank or missing reason is refused; a reason beside another basis is refused.
    def ll126(*extra):
        return run_cli("add-lens-link", "--extraction-id", str(fig126 or 0), "--icf", clear126, *extra, "--session", S)
    nl5 = n_links_now()
    refused5 = {
        "context, no reason": ll126("--basis", "context", "--basis-text", "mounted at a height"),
        "context, blank reason": ll126("--basis", "context", "--basis-text", "mounted at a height", "--basis-reason", "  "),
        "context, reason with no letter": ll126("--basis", "context", "--basis-text", "mounted at a height",
                                                "--basis-reason", "1200"),
        "named_in_text with a reason": ll126("--basis", "named_in_text", "--basis-text", "mounted at a height",
                                             "--basis-reason", T126_REASON),
        "heading with a reason": ll126("--basis", "heading", "--basis-text", "Section 3.8", "--basis-reason", T126_REASON),
        "study_participants with a reason": ll126("--basis", "study_participants", "--basis-text", "participants",
                                                  "--basis-reason", T126_REASON),
    }
    missed5 = [k for k, v in refused5.items() if v.returncode == 0]
    record("T126-05", "context with a missing, blank or letterless reason is refused, and a reason beside any other basis is "
           "refused; nothing is written",
           not missed5 and n_links_now() == nl5
           and "--basis-reason" in out_of(refused5["context, no reason"])
           and "belongs to basis `context` only" in out_of(refused5["named_in_text with a reason"]),
           f"not refused: {missed5}; {[out_of(v)[-120:] for v in refused5.values()]}")

    # T126-06: the context's words must be in the clause, its heading or a file saved for ITS source.
    r06a = ll126("--basis", "context", "--basis-text", "zq not anywhere xq", "--basis-reason", T126_REASON)
    r06b = ll126("--basis", "context", "--basis-text", "saved only for another source", "--basis-reason", T126_REASON)
    r06c = ll126("--basis", "context", "--basis-text", "applies to sanitary rooms", "--basis-reason", T126_REASON)
    r06d = run_cli("add-lens-link", "--extraction-id", str(fig126 or 0), "--needs",
                   t126_first("SELECT need_code FROM access_needs WHERE need_code<>? ORDER BY need_code", need126),
                   "--basis", "context", "--basis-text", "Section 3.8", "--basis-reason", T126_REASON, "--session", S)
    record("T126-06", "context words found nowhere, or only in a file saved for another source, are refused naming where it "
           "looked; words in the source's own saved scope clause and in its heading are accepted",
           r06a.returncode != 0 and r06b.returncode != 0 and "source_section" in out_of(r06b)
           and r06c.returncode == 0 and r06d.returncode == 0,
           f"{out_of(r06a)[-120:]!r} | {out_of(r06b)[-160:]!r} | {out_of(r06c)[-160:]!r} | {out_of(r06d)[-160:]!r}")

    # T126-07: a code row with no lens flag at all is refused (D-0182), as before.
    nf7, nl7 = n_figures(), n_links_now()
    r07_, _, _ = t126_add(code126, T126_CLAUSE + " (no lens)", *CTX("mounted at a height"))
    record("T126-07", "a code row with no lens flag is refused in the D-0182 words and writes nothing",
           r07_.returncode != 0 and "at least one lens" in out_of(r07_) and n_figures() == nf7 and n_links_now() == nl7,
           f"rc={r07_.returncode} {out_of(r07_)[-200:]!r}")

    # T126-08: a stored code figure holding only carried links takes a context link, then its carried link is retired
    # (the T-127 sequence). The probe is derived: the first such figure on the copy with a claim text to quote.
    probe8 = q("SELECT x.extraction_id, x.claim_text, MIN(k.link_id) FROM source_value_extractions x JOIN evidence_sources e "
               "ON e.ref_id = x.ref_id JOIN v_live_lens_links k ON k.extraction_id = x.extraction_id WHERE e.tier >= 4 "
               "AND TRIM(COALESCE(x.claim_text,'')) <> '' GROUP BY x.extraction_id HAVING SUM(k.basis <> 'carried') = 0 "
               "AND SUM(COALESCE(k.icf_code = ?, 0)) = 0 ORDER BY x.extraction_id LIMIT 1", clear126)
    if probe8:
        fig8, ct8, carried8 = probe8[0]
        word8 = max(re.findall(r"[^\W\d_]+", ct8), key=len)
        r08a = run_cli("add-lens-link", "--extraction-id", str(fig8), "--icf", clear126, "--basis", "context",
                       "--basis-text", word8, "--basis-reason", T126_REASON, "--session", S)
        r08b = run_cli("retire-lens-link", "--link-id", str(carried8), "--reason",
                       "TASK-FIXTURE T126: replaced by a judged context link", "--session", S)
        ok8 = (r08a.returncode == 0 and r08b.returncode == 0
               and q("SELECT basis, basis_reason FROM v_live_lens_links WHERE extraction_id=? AND icf_code=?", fig8,
                     clear126) == [("context", T126_REASON)]
               and q("SELECT retired_at IS NOT NULL FROM extraction_lens_links WHERE link_id=?", carried8) == [(1,)])
        detail8 = f"{out_of(r08a)[-200:]!r} | {out_of(r08b)[-200:]!r}"
    else:
        ok8, detail8 = False, "no stored code figure holding only carried links to probe"
    record("T126-08", "add-lens-link --basis context on a stored code figure holding only carried links is accepted, and "
           "retire-lens-link then retires the carried link", ok8, detail8)

    # T126-09: the migration itself, against its parent. The parent is built by the project's own replay
    # (migrate_db.build_plan / rebuild_from_migrations) of every step before the migration, in a temp directory; the
    # migration is then applied to a copy, and every row of extraction_lens_links is compared column by column (the
    # parent's columns), basis_reason must be NULL on every row, and the view must carry it after basis_text. The
    # canonical database is checked for the same column shape.
    import contextlib
    import io
    import migrate_db as _mdb9                                         # noqa: E402
    ok9, detail9 = False, ""
    _orig_plan9 = _mdb9.build_plan
    try:
        plan9 = _orig_plan9()
        idx9 = next(i for i, st in enumerate(plan9) if st[0] == "schema"
                    and st[2].name.endswith("_lens_link_context_basis.sql"))
        par9, mig9 = os.path.join(TMP, "t126-parent.db"), os.path.join(TMP, "t126-migrated.db")
        _mdb9.build_plan = lambda: plan9[:idx9]
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            _mdb9.rebuild_from_migrations(par9)
        _mdb9.build_plan = _orig_plan9
        # The replayed parent's rows hold NULL in basis_text and the three retired_* cells (every link is carried and
        # live), so a migration swapping them would pass a plain comparison: give them distinct values first, within the
        # parent's own CHECKs (a stated basis carries words; a retired link carries all three retired_* cells).
        _f9 = sqlite3.connect(par9)
        try:
            _f9.execute("UPDATE extraction_lens_links SET basis='named_in_text', basis_text='TASK-FIXTURE words '||link_id "
                        "WHERE link_id % 2 = 0")
            _f9.execute("UPDATE extraction_lens_links SET retired_at='2026-01-01 00:'||printf('%02d', link_id % 60), "
                        "retired_by_session='TASK-FIXTURE session '||link_id, retirement_reason='TASK-FIXTURE reason '||link_id "
                        "WHERE link_id % 3 = 0")
            _f9.commit()
        finally:
            _f9.close()
        shutil.copy(par9, mig9)
        _c9 = sqlite3.connect(mig9, isolation_level=None)
        _p9 = sqlite3.connect(par9)
        try:
            _, _v9, _path9 = plan9[idx9]
            _mdb9._apply_atomically(_c9, _mdb9._prepare_body(_path9.read_text(encoding="utf-8"))[0],
                                    label=_path9.name, user_version=_v9, fk_blocking=False)
            cols9 = [r[1] for r in _p9.execute("PRAGMA table_info(extraction_lens_links)")]
            sel9 = f"SELECT {', '.join(cols9)} FROM extraction_lens_links ORDER BY link_id"
            want9, got9 = _p9.execute(sel9).fetchall(), _c9.execute(sel9).fetchall()
            nonnull9 = _c9.execute("SELECT COUNT(basis_reason) FROM extraction_lens_links").fetchone()[0]
            seq9 = [x.execute("SELECT seq FROM sqlite_sequence WHERE name='extraction_lens_links'").fetchall()
                    for x in (_p9, _c9)]
            vcols9 = [r[1] for r in _c9.execute("PRAGMA table_info(v_live_lens_links)")]
            live9 = [x.execute("SELECT COUNT(*) FROM extraction_lens_links WHERE retired_at IS NULL").fetchone()[0]
                     for x in (_p9, _c9)] + [_c9.execute("SELECT COUNT(*) FROM v_live_lens_links").fetchone()[0]]
            vwant9 = _p9.execute("SELECT link_id, extraction_id, identity_code, icf_code, needs_code, basis, basis_text, "
                                 "NULL, created_at, created_by_session FROM extraction_lens_links WHERE retired_at IS NULL "
                                 "ORDER BY link_id").fetchall()
            vgot9 = _c9.execute("SELECT * FROM v_live_lens_links ORDER BY link_id").fetchall()
            idx_sql = ("SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='extraction_lens_links' "
                       "ORDER BY name")
            idx9 = [x.execute(idx_sql).fetchall() for x in (_p9, _c9)]
            spread9 = _p9.execute("SELECT COUNT(DISTINCT basis_text), COUNT(retired_at), COUNT(*) - COUNT(retired_at) "
                                  "FROM extraction_lens_links").fetchone()
        finally:
            _c9.close()
            _p9.close()
        canon9 = sqlite3.connect(f"file:{REPO / 'data' / 'guidebook.db'}?mode=ro", uri=True)
        try:
            ccols9 = [r[1] for r in canon9.execute("PRAGMA table_info(v_live_lens_links)")]
        finally:
            canon9.close()
        ok9 = (len(want9) > 0 and want9 == got9 and nonnull9 == 0 and seq9[0] == seq9[1]
               and all(n > 0 for n in spread9) and vwant9 == vgot9 and idx9[0] == idx9[1] and len(idx9[0]) > 0
               and "basis_reason" in vcols9 and vcols9.index("basis_reason") == vcols9.index("basis_text") + 1
               and len(set(live9)) == 1 and ccols9 == vcols9)
        detail9 = (f"view rows equal={vwant9 == vgot9}, indexes equal={idx9[0] == idx9[1]}, spread {spread9}; "
                   f"parent rows {len(want9)}, migrated rows {len(got9)}, equal={want9 == got9}, basis_reason set "
                   f"{nonnull9}, seq {seq9}, view {vcols9}, live {live9}, canonical view {ccols9}")
    except Exception as exc:  # noqa: BLE001 -- recorded red below
        detail9 = f"{exc.__class__.__name__}: {exc}"
    finally:
        _mdb9.build_plan = _orig_plan9
        for _tmp9 in ("t126-parent.db", "t126-migrated.db"):
            try:
                os.remove(os.path.join(TMP, _tmp9))
            except OSError:
                pass
    record("T126-09", "replayed to its parent and migrated, extraction_lens_links keeps every row column for column with "
           "basis_reason NULL and its sequence floor, and v_live_lens_links returns the same live rows with basis_reason "
           "after basis_text (as the canonical view does)", ok9, detail9)

    # T126-10: the skill carries the owner's guidance and no longer asks for a ruling the owner has given.
    record("T126-10", "the skill holds the owner's warrant, the proposals and no sentence keeping the identity off the links",
           skill126.count("typically concerns wheelchair users") >= 1
           and skill126.count("Moving it earlier needs a ruling") == 0
           and skill126.count("identity_icf_map") >= 1
           and "A proposal is never written because it was proposed" in skill126
           and not re.search(r"not written beside|never written beside", skill126), "")

    # T126-11: a silent omission is flagged: an ICF-only code row whose map proposes a group prints the warning, writes
    # no identity, and the audit lists it.
    r11_, fig11, res11 = t126_add(code126, T126_KNEE, "--icf", clear126, *CTX("knee clearance"),
                                  section="TASK-FIXTURE T126 Section 3.9")

    def audit126():
        return subprocess.run([sys.executable, str(REPO / "scripts" / "audit" / "code_value_identity_audit.py")],
                              env=dict(os.environ, GUIDEBOOK_DB_PATH=DB), capture_output=True, text=True)
    a11 = audit126()
    list_i = a11.stdout.split("(ii)")[0]
    record("T126-11", "an ICF-only code row whose map proposes a group is accepted with 'WARNING: maps propose', writes no "
           "identity, and the audit lists it in (i)",
           r11_.returncode == 0 and "WARNING: maps propose" in r11_.stderr and res11.get("identities_written") == []
           and fig11 and f"extraction {fig11}:" in list_i and a11.returncode == 1,
           f"rc={r11_.returncode} {r11_.stderr[-250:]!r} res={res11} audit rc={a11.returncode} {a11.stdout[-400:]!r}")

    # T126-12: the audit is not vacuous: it examines the figures, lists T126-11's, and leaves out T126-01's (it carries an
    # identity) and a figure whose every link is a heading (OD-31).
    r12_, fig12, _ = t126_add(code126, T126_KNEE, "--icf", clear126, "--lens-basis", "heading",
                              "--lens-basis-text", "Heading Gamma", section="TASK-FIXTURE T126 Heading Gamma")
    a12 = audit126()
    m12 = re.search(r"EXAMINED: (\d+)", a12.stdout)
    list_i = a12.stdout.split("(ii)")[0]
    record("T126-12", "the audit prints EXAMINED above 0, lists the omission, and not a figure with an identity link nor one "
           "whose every link is a heading",
           m12 and int(m12.group(1)) > 0 and fig11 and f"extraction {fig11}:" in list_i and fig126
           and f"extraction {fig126}:" not in list_i and r12_.returncode == 0 and fig12
           and f"extraction {fig12}:" not in list_i,
           f"{a12.stdout[-500:]!r} heading fig={fig12} {out_of(r12_)[-150:]!r}")

    # T126-13: a map row created after a figure's newest live link that proposes a group the figure lacks puts it in
    # list (iii), for information: the exit code does not move.
    new13 = t126_first("SELECT identity_code FROM base_taxonomy_identity WHERE status='active' AND identity_code NOT IN "
                       "(SELECT identity_code FROM v_live_lens_links WHERE extraction_id=? AND identity_code IS NOT NULL) "
                       "AND identity_code <> 'ALL' AND identity_code NOT IN (SELECT identity_code FROM identity_icf_map "
                       "WHERE icf_code=?) ORDER BY identity_code", fig126 or 0, reach126)
    before13 = audit126()
    w("INSERT INTO identity_icf_map (identity_code, icf_code, mechanism, mapping_confidence, provenance, created_at, "
      "created_by_session) VALUES (?, ?, 'TASK-FIXTURE later map row', 'low_indicative', 'TASK-FIXTURE T126-13', "
      "'2099-01-01 00:00', ?)", new13, reach126, S)
    after13 = audit126()
    list_iii = after13.stdout.split("(iii)")[-1]
    w("UPDATE identity_icf_map SET retired_at='2099-01-02 00:00', retired_by_session=?, retired_reason='TASK-FIXTURE' "
      "WHERE provenance='TASK-FIXTURE T126-13'", S)
    retired13 = audit126()
    record("T126-13", "a later map row proposing a group a stored figure lacks lists the figure in (iii), and the exit code "
           "does not change; once that map row is retired it proposes nothing and the figure leaves (iii)",
           fig126 and new13 and f"extraction {fig126}: " in list_iii and new13 in list_iii
           and f"extraction {fig126}: " not in before13.stdout.split("(iii)")[-1]
           and before13.returncode == after13.returncode
           and f"extraction {fig126}: " not in retired13.stdout.split("(iii)")[-1],
           f"before rc={before13.returncode} after rc={after13.returncode} {after13.stdout[-300:]!r} "
           f"retired {retired13.stdout[-200:]!r}")

    # ── T126, repair after the adversarial pass: one case for each branch a seeded defect left green ──────────────────
    def t126_parts(text):
        """The audit's lists (i), (ii) and (iii), and its queue line, by their headings."""
        i_, rest = (text.split("(ii)", 1) + [""])[:2]
        ii_, iii_ = (rest.split("(iii)", 1) + [""])[:2]
        q_ = next((ln for ln in text.splitlines() if ln.startswith("queue")), "")
        return i_, ii_, iii_, q_

    _ro14 = sqlite3.connect(DB)
    try:
        # T126-14: a need reaches groups through its b/d access_need_icf rows. Derived: the first need whose b/d row's
        # ICF code has a live map row, and the groups that route gives.
        n14 = t126_first("SELECT a.need_code FROM access_need_icf a JOIN identity_icf_map m ON m.icf_code = a.icf_code "
                         "AND m.retired_at IS NULL WHERE a.icf_type <> 'e' ORDER BY a.need_code")
        want14 = {c for (c,) in q("SELECT DISTINCT m.identity_code FROM access_need_icf a JOIN identity_icf_map m ON "
                                   "m.icf_code = a.icf_code AND m.retired_at IS NULL WHERE a.need_code=? AND "
                                   "a.icf_type <> 'e'", n14)}
        got14 = db.identity_proposals(_ro14, [], [n14]) if n14 else []
    finally:
        _ro14.close()
    record("T126-14", "the proposals for a need alone are the groups its b/d access_need_icf rows reach, each naming the need",
           n14 and want14 and {p["identity_code"] for p in got14} == want14
           and all(n14 in (p["via_needs"] or "") for p in got14), f"need {n14} want {want14} got {got14}")

    # T126-15: an e-code (environmental factor) of a need proposes nothing: fixture map row on the copy, from an e-code
    # of a need to a group no b/d route of that need reaches.
    n15, e15 = (q("SELECT need_code, icf_code FROM access_need_icf WHERE icf_type='e' ORDER BY need_code, icf_code") or
                [(None, None)])[0]
    _ro15 = sqlite3.connect(DB)
    try:
        reach15 = {p["identity_code"] for p in db.identity_proposals(_ro15, [], [n15])}
    finally:
        _ro15.close()
    x15 = t126_first("SELECT identity_code FROM base_taxonomy_identity WHERE status='active' AND identity_code<>'ALL' "
                     "ORDER BY identity_code") if not reach15 else sorted(
        {c for (c,) in q("SELECT identity_code FROM base_taxonomy_identity WHERE status='active' AND identity_code<>'ALL'")}
        - reach15)[0]
    w("INSERT INTO identity_icf_map (identity_code, icf_code, mechanism, mapping_confidence, provenance, created_at, "
      "created_by_session) VALUES (?, ?, 'TASK-FIXTURE e-code', 'low_indicative', 'TASK-FIXTURE T126-15', '2026-01-01 00:00', ?)",
      x15, e15, S)
    _ro15 = sqlite3.connect(DB)
    try:
        got15 = {p["identity_code"] for p in db.identity_proposals(_ro15, [], [n15])}
        direct15 = {p["identity_code"] for p in db.identity_proposals(_ro15, [e15], [])}
    finally:
        _ro15.close()
    record("T126-15", "a map row on a need's e-code proposes nothing for the need, though the same code given as an ICF code does",
           n15 and x15 not in got15 and x15 in direct15, f"need {n15} e {e15} fixture group {x15} via need {got15} direct {direct15}")

    # T126-01's own output: the warning stays silent with an identity live, the parent and the need's text are printed.
    parent01 = reach126[:-1] if q("SELECT 1 FROM base_icf WHERE icf_code=?", reach126[:-1]) else None
    record("T126-16", "a figure written with an identity link prints no WARNING", r01_.returncode == 0
           and "WARNING" not in r01_.stderr, r01_.stderr[-300:])
    record("T126-17", "a proposal through an ICF code with a parent in the registry names the parent beside it",
           parent01 and f"parent {parent01}" in r01_.stderr, f"parent {parent01}: {r01_.stderr[-300:]!r}")
    record("T126-18", "each need's own registry text is printed with the proposals",
           f"need {need126}: design_obligation:" in r01_.stderr and "absorbs:" in r01_.stderr, r01_.stderr[-300:])

    # T126-19: below tier 4 the writer does not warn, and the audit does not list the figure (an ICF-only research figure
    # whose map proposes groups, by named_in_text: the clause holds the words).
    r19_, fig19, _ = t126_add(grey126, T126_CLAUSE, "--icf", clear126, "--lens-basis", "named_in_text",
                              "--lens-basis-text", "Controls")
    i19, _, _, _ = t126_parts(audit126().stdout)
    record("T126-19", "an ICF-only figure of a source below tier 4 whose map proposes groups prints no WARNING and is not in (i)",
           r19_.returncode == 0 and fig19 and "PROPOSALS" in r19_.stderr and "WARNING" not in r19_.stderr
           and f"extraction {fig19}:" not in i19, f"{out_of(r19_)[-250:]!r}")

    # T126-20 / T126-21: add-lens-link reads the figure's live codes for its proposals, warns, and reports both fields.
    r20a, fig20, _ = t126_add(code126, T126_KNEE, "--needs", need126, *CTX("knee clearance"),
                              section="TASK-FIXTURE T126 Section 4.1")
    r20b = run_cli("add-lens-link", "--extraction-id", str(fig20 or 0), "--icf", clear126, "--basis", "context",
                   "--basis-text", "knee clearance", "--basis-reason", T126_REASON, "--session", S)
    r20c = run_cli("add-lens-link", "--extraction-id", str(fig20 or 0), "--identity", wheel126, "--basis", "context",
                   "--basis-text", "knee clearance", "--basis-reason", T126_REASON, "--session", S)
    try:
        res20b, res20c = json.loads(r20b.stdout), json.loads(r20c.stdout)
    except ValueError:
        res20b, res20c = {}, {}
    record("T126-20", "add-lens-link on an identity proposes from the ICF code already live on the figure, and returns the "
           "groups proposed and the identities written",
           r20c.returncode == 0 and set(live_prop02) <= set(res20c.get("identities_proposed") or ())
           and res20c.get("identities_written") == [wheel126] and set(live_prop02) <= set(res20b.get("identities_proposed") or ()),
           f"{out_of(r20b)[-200:]!r} | {out_of(r20c)[-300:]!r}")
    record("T126-21", "add-lens-link that leaves a code figure with ICF or need links, no identity and a proposal prints the "
           "WARNING, and an empty identities_written",
           r20a.returncode == 0 and "WARNING" not in r20a.stderr and r20b.returncode == 0
           and "WARNING: maps propose" in r20b.stderr and res20b.get("identities_written") == [],
           f"{r20a.stderr[-150:]!r} | {r20b.stderr[-250:]!r}")

    # T126-22: derive-extraction carries the reason: two figures a code source states in one unit, then a derived row by
    # context. The inputs' words are in the source's saved file.
    D22_BASE = "TASK-FIXTURE T126 The clear width shall be not less than 900 mm"
    D22_DELTA = "TASK-FIXTURE T126 Where a door swings into the room add 100 mm"
    t126_save(code126, "t126-code-derive.txt", D22_BASE + "\n" + D22_DELTA)

    def num22(text, value, comp, clause):
        r = run_cli("add-extraction", "--ref-id", code126, "--parameter-id", str(PARAM), "--icf", clear126,
                    *CTX("applies to sanitary rooms"), "--claim-text", text, "--claim-type", "numerical",
                    "--claimed-value", value, "--claimed-unit", "mm", "--comparator", comp, "--figure-role", "claim",
                    "--relation", "none", "--extraction-method", "full-read", "--loc-clause", clause, "--session", S)
        got = q("SELECT extraction_id FROM source_value_extractions WHERE ref_id=? AND claim_text=?", code126, text)
        return r, (got[0][0] if got else None)
    rb22, b22 = num22(D22_BASE, "900", ">=", "TASK-FIXTURE 3.8.1")
    rd22, d22 = num22(D22_DELTA, "100", "=", "TASK-FIXTURE 3.8.2")
    r22 = run_cli("derive-extraction", "--base", str(b22 or 0), "--delta", str(d22 or 0), "--parameter-id", str(PARAM),
                  "--icf", clear126, *CTX("applies to sanitary rooms"), "--session", S)
    l22 = q("SELECT k.basis, k.basis_reason FROM v_live_lens_links k JOIN source_value_extractions x ON x.extraction_id = "
            "k.extraction_id WHERE x.figure_role='derived' AND x.ref_id=?", code126)
    record("T126-22", "derive-extraction --lens-basis context --lens-basis-reason writes the derived row's link with its reason",
           rb22.returncode == 0 and rd22.returncode == 0 and r22.returncode == 0 and l22 == [("context", T126_REASON)],
           f"{out_of(rb22)[-150:]!r} | {out_of(rd22)[-150:]!r} | {out_of(r22)[-250:]!r} links {l22}")

    # T126-23: list (ii) names each live identity no live map row proposes, a retired map row included.
    lone23 = [c for (c,) in q("SELECT identity_code FROM base_taxonomy_identity WHERE status='active' AND identity_code <> ? "
                              "AND identity_code NOT IN (SELECT identity_code FROM identity_icf_map WHERE retired_at IS NULL) "
                              "ORDER BY 1", dbcore.SCOPE_MARKER_IDENTITY)]
    if lone23:
        w("INSERT INTO identity_icf_map (identity_code, icf_code, mechanism, mapping_confidence, provenance, created_at, "
          "created_by_session, retired_at, retired_by_session, retired_reason) VALUES (?, ?, 'TASK-FIXTURE retired', "
          "'low_indicative', 'TASK-FIXTURE T126-23', '2026-01-01 00:00', ?, '2026-01-02 00:00', ?, 'TASK-FIXTURE')",
          lone23[0], clear126, S, S)
    _, ii23, _, _ = t126_parts(audit126().stdout)
    record("T126-23", "list (ii) names every live identity no live map row proposes, one with only a retired map row included",
           lone23 and all(re.search(rf"(?<![\w-]){re.escape(c)}(?![\w-])", ii23) for c in lone23),
           f"want {lone23} got {ii23[:200]!r}")

    # T126-24: list (iii) reads the date of the access_need_icf row a proposal comes through: an old map row reached
    # through a need row created after the figure's newest live link lists the figure. Fixtures on the copy.
    n24 = n14
    r24, fig24, _ = t126_add(code126, T126_CLAUSE, "--needs", n24, "--identity", wheel126, *CTX("mounted at a height"),
                             section="TASK-FIXTURE T126 Section 5.1")
    have24 = {c for (c,) in q("SELECT identity_code FROM v_live_lens_links WHERE extraction_id=? AND identity_code IS NOT "
                               "NULL", fig24 or 0)}
    c24 = t126_first("SELECT icf_code FROM base_icf WHERE component='d' AND icf_code NOT IN (SELECT icf_code FROM "
                     "access_need_icf WHERE need_code=?) AND icf_code NOT IN (SELECT icf_code FROM identity_icf_map) "
                     "ORDER BY icf_code", n24)
    g24 = sorted({c for (c,) in q("SELECT identity_code FROM base_taxonomy_identity WHERE status='active' AND "
                                   "identity_code<>'ALL'")} - have24 - {p for p in want14})[0]
    w("INSERT INTO identity_icf_map (identity_code, icf_code, mechanism, mapping_confidence, provenance, created_at, "
      "created_by_session) VALUES (?, ?, 'TASK-FIXTURE old map row', 'low_indicative', 'TASK-FIXTURE T126-24', "
      "'2026-01-01 00:00', ?)", g24, c24, S)
    _, _, iii24a, _ = t126_parts(audit126().stdout)
    w("INSERT INTO access_need_icf (need_code, icf_code, icf_type, confidence, created_at, created_by_session) "
      "VALUES (?, ?, 'd', 'proposed', '2099-01-01T00:00:00Z', ?)", n24, c24, S)
    _, _, iii24b, _ = t126_parts(audit126().stdout)
    record("T126-24", "a need row created after the figure's newest link, reaching an old map row, lists the figure in (iii)",
           r24.returncode == 0 and fig24 and f"extraction {fig24}:" not in iii24a and f"extraction {fig24}: " in iii24b
           and g24 in iii24b, f"{out_of(r24)[-150:]!r} c={c24} g={g24} before {iii24a[-150:]!r} after {iii24b[-200:]!r}")

    # T126-25: list (i) needs a proposal: a code figure whose ICF code no map row reaches, with no identity, is not listed.
    c25 = t126_first("SELECT icf_code FROM base_icf WHERE component='d' AND icf_code NOT IN (SELECT icf_code FROM "
                     "identity_icf_map) ORDER BY icf_code DESC")
    r25, fig25, _ = t126_add(code126, T126_KNEE, "--icf", c25, *CTX("knee clearance"), section="TASK-FIXTURE T126 Section 6.1")
    i25, _, _, _ = t126_parts(audit126().stdout)
    record("T126-25", "a code figure with an ICF link no map row reaches and no identity is not in (i), and prints no WARNING",
           r25.returncode == 0 and fig25 and f"extraction {fig25}:" not in i25 and "WARNING" not in r25.stderr,
           f"{c25} {out_of(r25)[-200:]!r}")

    # T126-26: ALL is refused as an identity under the context basis, by both writers (OD-31); nothing is written.
    nf26, nl26 = n_figures(), n_links_now()
    r26a = run_cli("add-lens-link", "--extraction-id", str(fig126 or 0), "--identity", "ALL", "--basis", "context",
                   "--basis-text", "mounted at a height", "--basis-reason", T126_REASON, "--session", S)
    r26b, _, _ = t126_add(code126, T126_KNEE, "--identity", "ALL", *CTX("knee clearance"), section="TASK-FIXTURE T126 7.1")
    record("T126-26", "--identity ALL with basis context is refused by add-lens-link and add-extraction, naming OD-31",
           r26a.returncode != 0 and "OD-31" in out_of(r26a) and r26b.returncode != 0 and "OD-31" in out_of(r26b)
           and n_figures() == nf26 and n_links_now() == nl26, f"{out_of(r26a)[-200:]!r} | {out_of(r26b)[-200:]!r}")

    # T126-27: ALL is not an identity in the audit: a code figure carrying ICF d-links the maps reach and only ALL as an
    # identity (written by named_in_text, which T-056 governs) is listed in (i).
    t126_save(code126, "t126-code-all.txt", "TASK-FIXTURE T126 for all users the knee space shall be clear")
    r27, fig27, _ = t126_add(code126, "TASK-FIXTURE T126 for all users the knee space shall be clear", "--icf", clear126,
                             *CTX("knee space"), section="TASK-FIXTURE T126 8.1")
    r27b = run_cli("add-lens-link", "--extraction-id", str(fig27 or 0), "--identity", "ALL", "--basis", "named_in_text",
                   "--basis-text", "for all users", "--session", S)
    a27 = audit126()
    i27, _, _, q27 = t126_parts(a27.stdout)
    record("T126-27", "a code figure whose only identity link is ALL is listed in (i)",
           r27.returncode == 0 and r27b.returncode == 0 and fig27 and f"extraction {fig27}:" in i27,
           f"{out_of(r27b)[-150:]!r} {i27[-200:]!r}")

    # T126-28: the queue line counts, by its own query, the tier-4-and-above figures with no judged non-ALL identity link.
    want28 = q("SELECT COUNT(*) FROM (SELECT k.extraction_id FROM v_live_lens_links k JOIN source_value_extractions x ON "
               "x.extraction_id = k.extraction_id JOIN evidence_sources e ON e.ref_id = x.ref_id WHERE e.tier >= ? "
               "GROUP BY k.extraction_id HAVING SUM(COALESCE(k.identity_code <> 'ALL' AND k.basis <> 'carried', 0)) = 0)",
               dbcore.REGULATORY_FROM_TIER)[0][0]
    m28 = re.search(r"queue \(derived, not a failure\): (\d+)", q27)
    record("T126-28", "the audit's queue line equals the count of tier-4-and-above figures with no judged identity link other "
           "than ALL, and is above 0 (the stored carried links)",
           m28 and int(m28.group(1)) == want28 and want28 > 0, f"line {q27!r} want {want28}")

    # ── T126, second repair ──────────────────────────────────────────────────────────────────────────────────────────
    # T126-29: the scope marker is no group to the writer either: adding an ICF code the maps reach to a stored code figure
    # whose only live link is a carried ALL warns (the critic's walk; the figure is derived by query), and so does
    # adding ALL to T126-27's ICF-only figure.
    probe29 = q("SELECT x.extraction_id, x.claim_text FROM source_value_extractions x JOIN evidence_sources e ON e.ref_id = "
                "x.ref_id JOIN v_live_lens_links k ON k.extraction_id = x.extraction_id WHERE e.tier >= ? AND "
                "TRIM(COALESCE(x.claim_text,'')) <> '' GROUP BY x.extraction_id HAVING COUNT(*) = 1 AND "
                "MAX(k.identity_code) = ? AND MAX(k.basis) = 'carried' ORDER BY x.extraction_id LIMIT 1",
                dbcore.REGULATORY_FROM_TIER, dbcore.SCOPE_MARKER_IDENTITY)
    if probe29:
        fig29, ct29 = probe29[0]
        word29 = max(re.findall(r"[^\W\d_]+", ct29), key=len)
        r29 = run_cli("add-lens-link", "--extraction-id", str(fig29), "--icf", clear126, "--basis", "context",
                      "--basis-text", word29, "--basis-reason", T126_REASON, "--session", S)
        ok29, d29 = (r29.returncode == 0 and "WARNING: maps propose" in r29.stderr), out_of(r29)[-250:]
    else:
        ok29, d29 = False, "no stored code figure whose only live link is a carried scope marker"
    record("T126-29", "a code figure carrying only the scope marker, given an ICF code the maps reach, is warned (the scope "
           "marker is no group), as is adding the marker to an ICF-only figure",
           ok29 and "WARNING: maps propose" in r27b.stderr, f"{d29!r} | {r27b.stderr[-200:]!r}")

    # T126-30: tier 4 is the regulatory stratum's first tier: a source the ladder places exactly there (its type and
    # scope read from the ladder) takes a context link, is warned, and is listed by the audit.
    from schemas.tier_derivation import TIER_MAP as _TM30  # noqa: E402
    # The stratum's first tier is read from CLAUDE.md §6's evidence model ("T4–T6 the regulatory stratum"), not from the
    # constant under test.
    _ts30 = re.search(r"\bT(\d)[–-]T6\*\* the regulatory stratum", (REPO / "CLAUDE.md").read_text(encoding="utf-8"))
    ruled30 = int(_ts30.group(1)) if _ts30 else None
    t4 = next(((et, sc) for (et, sc), tier in sorted(_TM30.items()) if tier == ruled30), None)
    ref30, _ = add_o("T126 tier 4", "--evidence-type", t4[0], "--scope", t4[1]) if t4 else (None, None)
    if ref30:
        readable(ref30)
        t126_save(ref30, "t126-tier4.txt", T126_KNEE)
    r30, fig30, _ = t126_add(ref30 or code126, T126_KNEE, "--icf", clear126, *CTX("knee clearance"),
                             section="TASK-FIXTURE T126 tier 4")
    i30, _, _, _ = t126_parts(audit126().stdout)
    record("T126-30", "an ICF-only context link on a tier-4 source is accepted, warned and listed in (i)",
           t4 and dbcore.REGULATORY_FROM_TIER == ruled30 and q("SELECT tier FROM evidence_sources WHERE ref_id=?", ref30) == [(ruled30,)]
           and r30.returncode == 0 and "WARNING: maps propose" in r30.stderr and fig30 and f"extraction {fig30}:" in i30,
           f"{t4} {out_of(r30)[-250:]!r}")

    # T126-31: a map row naming the scope marker proposes nothing: not to the writer, and not in list (iii).
    w("INSERT INTO identity_icf_map (identity_code, icf_code, mechanism, mapping_confidence, provenance, created_at, "
      "created_by_session) VALUES (?, ?, 'TASK-FIXTURE scope marker row', 'low_indicative', 'TASK-FIXTURE T126-31', "
      "'2099-01-01 00:00', ?)", dbcore.SCOPE_MARKER_IDENTITY, clear126, S)
    _ro31 = sqlite3.connect(DB)
    try:
        got31 = {p["identity_code"] for p in db.identity_proposals(_ro31, [clear126], [])}
    finally:
        _ro31.close()
    _, _, iii31, _ = t126_parts(audit126().stdout)
    record("T126-31", "a later map row naming the scope marker proposes it to no writer and lists no figure in (iii)",
           got31 and dbcore.SCOPE_MARKER_IDENTITY not in got31 and fig27 and f"extraction {fig27}:" not in iii31,
           f"{got31} {iii31[-200:]!r}")

    # T126-32: list (ii) leaves out a deprecated identity (state set by SQL on the copy and undone, as T018-12 does).
    dep32 = next((c for c in lone23 if c != dbcore.SCOPE_MARKER_IDENTITY), None)
    if dep32:
        w("UPDATE base_taxonomy_identity SET status='deprecated', superseded_by_need=(SELECT need_code FROM access_needs "
          "ORDER BY need_code LIMIT 1) WHERE identity_code=?", dep32)
        try:
            _, ii32, _, _ = t126_parts(audit126().stdout)
        finally:
            w("UPDATE base_taxonomy_identity SET status='active', superseded_by_need=NULL WHERE identity_code=?", dep32)
    record("T126-32", "list (ii) names no deprecated identity",
           dep32 and not re.search(rf"(?<![\w-]){re.escape(dep32)}(?![\w-])", ii32), f"{dep32} {ii32[:200]!r}")

    # T126-33: the confirm-or-replace walk. A figure whose only link is a context link takes its replacement on another
    # basis in one add-lens-link call, which retires the context link; a context link is not replaced by another context
    # link, and a stated link is not replaced by a context one.
    r33a, fig33, _ = t126_add(code126, T126_KNEE, "--icf", clear126, *CTX("knee clearance"), section="TASK-FIXTURE T126 9.1")
    old33 = q("SELECT link_id FROM v_live_lens_links WHERE extraction_id=?", fig33 or 0)
    r33b = run_cli("add-lens-link", "--extraction-id", str(fig33 or 0), "--icf", clear126, "--basis", "context",
                   "--basis-text", "knee clearance", "--basis-reason", T126_REASON + " again", "--session", S)
    r33c = run_cli("add-lens-link", "--extraction-id", str(fig33 or 0), "--icf", clear126, "--basis", "named_in_text",
                   "--basis-text", "Knee clearance", "--session", S)
    live33 = q("SELECT link_id, basis FROM v_live_lens_links WHERE extraction_id=?", fig33 or 0)
    gone33 = q("SELECT retirement_reason FROM extraction_lens_links WHERE link_id=?", old33[0][0]) if old33 else []
    r33d = run_cli("add-lens-link", "--extraction-id", str(fig33 or 0), "--icf", clear126, "--basis", "context",
                   "--basis-text", "knee clearance", "--basis-reason", T126_REASON, "--session", S)
    try:
        res33c = json.loads(r33c.stdout)
    except ValueError:
        res33c = {}
    record("T126-33", "add-lens-link on another basis replaces a figure's only context link in one call (retired 'superseded "
           "by judged link <id>'); a second context link on the code and a context link over a stated one are refused",
           r33a.returncode == 0 and len(old33) == 1 and r33b.returncode != 0 and "already holds a live context" in out_of(r33b)
           and r33c.returncode == 0 and len(live33) == 1 and live33[0][1] == "named_in_text"
           and gone33 == [(f"superseded by judged link {live33[0][0]}",)]
           and res33c.get("retired_context_link_id") == old33[0][0]
           and r33d.returncode != 0 and "already holds a live named_in_text" in out_of(r33d),
           f"{out_of(r33b)[-150:]!r} | {out_of(r33c)[-200:]!r} | live {live33} gone {gone33} | {out_of(r33d)[-150:]!r}")

    # T126-34: list (iv) names, by their own query, the figures with no ICF or need link that carry no identity but the
    # scope marker (they reach no group cell) and those reached only through carried identity links.
    rows34 = q("SELECT k.extraction_id, SUM(k.icf_code IS NOT NULL OR k.needs_code IS NOT NULL), "
               "SUM(COALESCE(k.identity_code <> ?, 0)), SUM(k.basis <> 'carried') FROM v_live_lens_links k JOIN "
               "source_value_extractions x ON x.extraction_id = k.extraction_id JOIN evidence_sources e ON e.ref_id = "
               "x.ref_id WHERE e.tier >= ? GROUP BY k.extraction_id ORDER BY k.extraction_id",
               dbcore.SCOPE_MARKER_IDENTITY, dbcore.REGULATORY_FROM_TIER)
    marker34 = [r[0] for r in rows34 if not r[1] and not r[2]]
    carried34 = [r[0] for r in rows34 if not r[1] and r[2] and not r[3]]
    line34 = next((ln for ln in audit126().stdout.splitlines() if ln.startswith("(iv)")), "")
    m34 = re.search(r": (\d+) carry no identity but \S+, so reach no group cell: (.*?); (\d+) are reached only through "
                    r"carried \(unjudged\) identity links: (.*)$", line34)
    ids34 = lambda txt: [] if txt.strip() == "none" else [int(x) for x in txt.split(", ")]  # noqa: E731
    record("T126-34", "list (iv) names the figures that reach no group cell and those reached only through carried links, "
           "as their own query finds them",
           m34 and marker34 and ids34(m34.group(2)) == marker34 and int(m34.group(1)) == len(marker34)
           and ids34(m34.group(4)) == carried34 and int(m34.group(3)) == len(carried34),
           f"want {len(marker34)}/{len(carried34)} line {line34[:300]!r}")

    # G. THE MARKER IS A CACHE OVER `confirms` EDGES, so an edge aimed at a row a LIVE PROXY
    # determination is governed by is refused (dbcore.live_determinations_linked), through both
    # writers, and so is regrading a row in a live determination's provenance; neither is refused
    # once that determination is retired, and a determination that is not a proxy one reads no edges.
    gov = q("SELECT l.specification_id, l.extraction_id FROM specification_extraction_links l "
            "JOIN source_value_extractions x ON x.extraction_id = l.extraction_id "
            "JOIN evidence_sources e ON e.ref_id = x.ref_id AND e.superseded_by_ref_id IS NULL "
            "WHERE l.role='governing' ORDER BY 1, 2 LIMIT 1")
    label_edge = q("SELECT from_extraction_id FROM extraction_relations WHERE relation='confirms' "
                   "AND to_label IS NOT NULL ORDER BY relation_id LIMIT 1")
    finding = q("SELECT extraction_id FROM source_value_extractions WHERE figure_role='finding' "
                "ORDER BY 1 LIMIT 1")
    if not (gov and label_edge and finding):
        record("G00", "a governing row, a label confirms edge and a finding to test with", False,
               f"gov={gov} label_edge={label_edge} finding={finding}")
    else:
        (SPEC_G, GOV_X), FROM_L, FROM_F = gov[0], label_edge[0][0], finding[0][0]
        other = q("SELECT extraction_id FROM specification_extraction_links WHERE specification_id=? "
                  "AND role <> 'governing' ORDER BY 1 LIMIT 1", SPEC_G)
        OTHER_X = other[0][0] if other else None
        con = sqlite3.connect(DB)
        unretire(con, SPEC_G)
        con.execute("UPDATE specifications SET rests_on_proxy_inference=1 WHERE specification_id=?",
                    (SPEC_G,))
        con.commit()
        con.close()

        def linked(x, **k):
            c = sqlite3.connect(DB)
            try:
                return dbcore.live_determinations_linked(c, x, **k)
            finally:
                c.close()

        n_rel = counts("extraction_relations")
        edge = dict(to_extraction=GOV_X, stated="named", quote="fixture quote", dry_run=True)
        msg_add = refusal(db.relate_extraction, FROM_F, "confirms", S, **edge)
        msg_rep = refusal(db.repoint_extraction_relation, FROM_L, "confirms", GOV_X, S, dry_run=True)
        record("G01", "relate-extraction refuses a confirms edge to a row a live proxy determination is "
               "governed by, naming it and retire-specification, and writes nothing",
               msg_add and f"{SPEC_G}" in msg_add and "retire-specification" in msg_add
               and counts("extraction_relations") == n_rel, f"{msg_add!r}")
        record("G02", "--repoint refuses the same for a label edge",
               msg_rep and "retire-specification" in msg_rep, f"{msg_rep!r}")
        record("G03", "the guard reads the governing role: a row the determination only EXCLUDED is "
               "not 'governed by' it, though it is linked",
               OTHER_X is not None and linked(OTHER_X, governing_only=True) == []
               and linked(OTHER_X) == [SPEC_G], f"other={OTHER_X} {linked(OTHER_X) if OTHER_X else ''}")
        def flipped(x):
            """A value of extraction_method that is NOT the row's current one (a real change)."""
            cur = q("SELECT extraction_method FROM source_value_extractions WHERE extraction_id=?", x)[0][0]
            return "skim" if cur != "skim" else "full-read"

        def amend(x, value=None):
            return refusal(db.amend_extraction, x, "extraction_method", value or flipped(x),
                           "fixture", S, dry_run=True)

        msg_amend = amend(GOV_X)
        record("G04", "amend-extraction refuses to regrade a row in a live determination's provenance, "
               "naming it",
               msg_amend and f"{SPEC_G}" in msg_amend and "retire-specification" in msg_amend,
               f"{msg_amend!r}")
        # G04b (T-061 critic): the value and the unit of a figure in a live determination are engine columns, so the
        # live-determination refusal covers them as it covers extraction_method. The reformat rule is switched off for
        # this one call so the case reaches the refusal it names; it asserts membership of ENGINE_EXTRACTION_COLUMNS by
        # behaviour, not by set arithmetic.
        _reformat_rule = db._refuse_unless_reformat
        db._refuse_unless_reformat = lambda *a, **k: None
        try:
            msg_val = refusal(db.amend_extraction, GOV_X, "claimed_value", "999", "fixture", S, dry_run=True)
            msg_unit = refusal(db.amend_extraction, GOV_X, "claimed_unit", "zz-unit", "fixture", S, dry_run=True)
        finally:
            db._refuse_unless_reformat = _reformat_rule
        record("G04b", "amend-extraction refuses a changed claimed_value or claimed_unit on a row in a live determination's provenance",
               bool(msg_val) and "live determination" in msg_val and bool(msg_unit) and "live determination" in msg_unit,
               f"{msg_val!r} | {msg_unit!r}")
        msg_excl = amend(OTHER_X) if OTHER_X else None
        record("G05", "...whatever part the row played: a row the determination only EXCLUDED is "
               "refused too, because regrading could promote it",
               msg_excl and "live determination" in msg_excl, f"{msg_excl!r}")
        noop = refusal(db.amend_extraction, GOV_X, "extraction_method",
                       q("SELECT extraction_method FROM source_value_extractions WHERE "
                         "extraction_id=?", GOV_X)[0][0], "fixture: checked", S, dry_run=True)
        record("G06", "recording that a value was checked and is already right is not a regrading",
               noop is None, f"{noop!r}")
        ref_x = q("SELECT ref_id FROM source_value_extractions WHERE extraction_id=?", GOV_X)[0][0]
        w("UPDATE evidence_sources SET superseded_by_ref_id=? WHERE ref_id=?",
          q("SELECT ref_id FROM evidence_sources WHERE ref_id<>? ORDER BY ref_id LIMIT 1",
            ref_x)[0][0], ref_x)
        msg_sup = amend(GOV_X)
        w("UPDATE evidence_sources SET superseded_by_ref_id=NULL WHERE ref_id=?", ref_x)
        record("G07", "a row of a superseded source is never gathered, so regrading it is not refused",
               not msg_sup or "live determination" not in msg_sup, f"{msg_sup!r}")
        msg_excl_edge = refusal(db.relate_extraction, FROM_F, "confirms", S,
                                **dict(edge, to_extraction=OTHER_X)) if OTHER_X else None
        record("G08", "the edge guard reads the governing role at the writer: a confirms edge to a row "
               "the determination only excluded is not refused for governing it",
               OTHER_X is not None and "governs live proxy" not in (msg_excl_edge or ""),
               f"{msg_excl_edge!r}")
        w("UPDATE specifications SET rests_on_proxy_inference=0 WHERE specification_id=?", SPEC_G)
        msg_np = refusal(db.relate_extraction, FROM_F, "confirms", S, **edge)
        record("G09", "...and the proxy scope at the writer: a live determination that is NOT a proxy "
               "one reads no edges, so the edge is not refused", "governs live proxy" not in (msg_np or ""),
               f"{msg_np!r}")
        record("G10", "while regrading is still refused for it (any live determination)",
               "live determination" in (amend(GOV_X) or ""))
        # T-017: a condition_on edge FROM a governing row would move it out of its live headline
        # (assess_cell.compose_value), so it is refused like a regrade -- unless that row is already a
        # branch, when the headline does not move. The edge runs FROM the conditioned claim TO the
        # condition, so the reverse of an existing pair is refused too (each would condition the
        # other). The relaxation shape, an edge from a condition row TO a governing one, changes what
        # a render shows and not the stored answer, so it is not refused. Rows are chosen by query;
        # the quotes are real: GOV_T, a governing row of the live determination, borrows the quote of
        # an edge it already carries (it passes the verbatim floor), and a condition row likewise.
        GOV_T, GOV_QUOTE = next(((x, qt) for x, qt in q(
            "SELECT r.from_extraction_id, r.quote FROM extraction_relations r JOIN "
            "specification_extraction_links l ON l.extraction_id = r.from_extraction_id AND "
            "l.specification_id = ? AND l.role = 'governing' WHERE r.quote IS NOT NULL AND "
            "r.from_extraction_id NOT IN (SELECT from_extraction_id FROM extraction_relations WHERE "
            "relation = 'condition_on') ORDER BY r.relation_id", SPEC_G)), (None, None))
        cond = [c for (c,) in q(
            "SELECT extraction_id FROM source_value_extractions WHERE figure_role='condition' "
            "AND extraction_id <> ? AND extraction_id NOT IN (SELECT from_extraction_id FROM "
            "extraction_relations WHERE relation='condition_on' AND to_extraction_id=?) ORDER BY 1",
            GOV_T, GOV_T)]
        COND_TO, COND_TO2 = (cond + [None, None])[:2]
        COND_FROM, COND_QUOTE = next(((c, qt) for c, qt in q(
            "SELECT r.from_extraction_id, r.quote FROM extraction_relations r JOIN "
            "source_value_extractions x ON x.extraction_id = r.from_extraction_id WHERE "
            "r.relation='condition_on' AND x.figure_role='condition' AND r.quote IS NOT NULL "
            "ORDER BY 1") if linked(c, governing_only=True) == [] and c != GOV_X), (None, None))
        cedge = dict(stated="named", quote=GOV_QUOTE,
                     cross_source_reason="fixture: the target is chosen by query, not by source")
        n_rel = counts("extraction_relations")
        msg_c5 = refusal(db.relate_extraction, GOV_T, "condition_on", S,
                         **dict(cedge, to_extraction=COND_TO)) if COND_TO and GOV_QUOTE else None
        record("T017-B5", "relate-extraction refuses a condition_on edge FROM a governing row of a "
               "live determination that has none yet, naming it and retire-specification, and (a "
               "real run, not a dry one) writes nothing",
               COND_TO is not None and msg_c5 and "governs a live determination" in msg_c5
               and "retire-specification" in msg_c5 and counts("extraction_relations") == n_rel,
               f"from={GOV_T} to={COND_TO} {msg_c5!r}")
        got_c6 = None
        if COND_FROM:
            try:
                got_c6 = db.relate_extraction(COND_FROM, "condition_on", S, dry_run=True,
                                              **dict(cedge, to_extraction=GOV_T, quote=COND_QUOTE))
            except Refusal as exc:
                got_c6 = str(exc)
        record("T017-B6", "...but the same edge from a condition row to that governing row is accepted",
               COND_FROM is not None and isinstance(got_c6, dict), f"from={COND_FROM} {got_c6!r}")
        # A row that already has a condition_on edge is a branch: a second edge moves no headline.
        got_c7 = None
        if COND_TO and COND_TO2 and GOV_QUOTE:
            w("INSERT INTO extraction_relations (from_extraction_id, relation, to_extraction_id, stated, "
              "quote, created_at, created_by_session) VALUES (?, 'condition_on', ?, 'named', ?, 't', ?)",
              GOV_T, COND_TO, GOV_QUOTE, S)
            try:
                got_c7 = db.relate_extraction(GOV_T, "condition_on", S, dry_run=True,
                                              **dict(cedge, to_extraction=COND_TO2))
            except Refusal as exc:
                got_c7 = str(exc)
            w("DELETE FROM extraction_relations WHERE from_extraction_id=? AND to_extraction_id=? "
              "AND relation='condition_on'", GOV_T, COND_TO)
        record("T017-B6b", "...and a governing row that already carries a condition_on edge may take another "
               "(it is already a branch, so the headline does not move)",
               COND_TO2 is not None and isinstance(got_c7, dict), f"to={COND_TO2} {got_c7!r}")
        # The other relations are not this refusal's: `exceeds` from the same governing row.
        got_c8 = None
        if COND_TO and GOV_QUOTE:
            try:
                got_c8 = db.relate_extraction(GOV_T, "exceeds", S, dry_run=True,
                                              **dict(cedge, to_extraction=COND_TO))
            except Refusal as exc:
                got_c8 = str(exc)
        record("T017-B6c", "...and only a condition_on edge is refused: an exceeds edge from a governing row "
               "is accepted", COND_TO is not None and isinstance(got_c8, dict), f"to={COND_TO} {got_c8!r}")
        # The reverse of an existing pair: each claim would be the other's condition, and both would
        # leave any headline. A live pair is chosen whose target carries a quote of its own.
        pair = next(((a, b, qt) for a, b, qt in q(
            "SELECT r.from_extraction_id, r.to_extraction_id, (SELECT r2.quote FROM extraction_relations "
            "r2 WHERE r2.from_extraction_id = r.to_extraction_id AND r2.quote IS NOT NULL LIMIT 1) "
            "FROM extraction_relations r WHERE r.relation='condition_on' AND r.to_extraction_id IS NOT NULL "
            "ORDER BY r.relation_id") if qt and linked(b, governing_only=True) == []), None)
        n_rel = counts("extraction_relations")
        msg_c9 = refusal(db.relate_extraction, pair[1], "condition_on", S,
                         **dict(cedge, to_extraction=pair[0], quote=pair[2])) if pair else None
        record("T017-B6d", "relate-extraction refuses the reverse of an existing condition_on pair, naming "
               "the direction, and (a real run) writes nothing",
               pair is not None and msg_c9 and "condition of the other" in msg_c9
               and "--from is the claim that holds only under the condition" in msg_c9
               and counts("extraction_relations") == n_rel, f"pair={pair and pair[:2]} {msg_c9!r}")
        # Source-level and comparator guards: the other columns the engine reads. The marker and
        # the interval are caches over them, so a change under a live determination is refused.
        ref_gov = q("SELECT ref_id FROM source_value_extractions WHERE extraction_id=?", GOV_X)[0][0]
        only_x = q("SELECT DISTINCT x.ref_id FROM specification_extraction_links l "
                   "JOIN source_value_extractions x ON x.extraction_id = l.extraction_id "
                   "WHERE l.specification_id=? AND x.ref_id NOT IN (SELECT ref_id FROM "
                   "specification_source_links WHERE specification_id=?) AND x.ref_id NOT IN "
                   "(SELECT c.ref_id FROM convergence_sources c JOIN specifications s ON "
                   "s.convergence_id = c.convergence_id WHERE s.specification_id=?) "
                   "ORDER BY 1 LIMIT 1", SPEC_G, SPEC_G, SPEC_G)
        ref_ext = only_x[0][0] if only_x else None

        def source_flip(ref):
            """A jurisdiction the source does not carry: a column the engine reads, and one whose
            amendment meets no other refusal first (the fixture sources are CLOSED, so a
            verification_status demotion would be refused for that instead)."""
            cur = q("SELECT jurisdiction FROM evidence_sources WHERE ref_id=?", ref)[0][0]
            return refusal(db.amend_source, ref, "jurisdiction", "INT" if cur != "INT" else "US",
                           "fixture", S, dry_run=True)

        msg_vs = source_flip(ref_gov)
        record("G13", "amend-source refuses a column the engine reads (jurisdiction) on a "
               "source a live determination rests on, naming it and the remedy",
               msg_vs and f"specification {SPEC_G}" in msg_vs and "retire-specification" in msg_vs,
               f"{msg_vs!r}")
        msg_ext = source_flip(ref_ext) if ref_ext else None
        record("G14", "...also when the source is reached only through the extraction links (a "
               "source that measured or confirmed, never governed): the third junction",
               ref_ext is not None and msg_ext
               and f"specification {SPEC_G} (via specification_extraction_links)" in msg_ext,
               f"ref={ref_ext} {msg_ext!r}")
        msg_notes = refusal(db.amend_source, ref_gov, "notes", "fixture note", "fixture", S,
                            dry_run=True)
        record("G15", "...and does not refuse a column the engine never reads (notes)",
               not msg_notes, f"{msg_notes!r}")
        cur_cmp = q("SELECT comparator FROM source_value_extractions WHERE extraction_id=?",
                    GOV_X)[0][0]
        msg_cmp = refusal(db.amend_extraction, GOV_X, "comparator",
                          ">=" if cur_cmp != ">=" else "<=", "fixture", S, dry_run=True)
        record("G16", "amend-extraction refuses a comparator change under a live determination "
               "(the stored bounds were composed from it)",
               msg_cmp and "live determination" in msg_cmp and "comparator" in msg_cmp,
               f"{msg_cmp!r}")
        cur_st = q("SELECT extraction_status FROM source_value_extractions WHERE extraction_id=?",
                   GOV_X)[0][0]
        msg_st = refusal(db.amend_extraction, GOV_X, "extraction_status",
                         "reviewed" if cur_st != "reviewed" else "verified", "fixture", S,
                         dry_run=True)
        record("G17", "...but not a provenance column the engine never reads (extraction_status)",
               not msg_st, f"{msg_st!r}")
        msg_sup = refusal(db.supersede_source, ref_ext, ref_gov, "fixture", S, dry_run=True) \
            if ref_ext else None
        record("G18", "supersede-source now refuses a source resting on a live determination only "
               "through the extraction links (the gap its docstring used to record)",
               msg_sup and "live determination" in msg_sup, f"{msg_sup!r}")
        db.retire_specification(SPEC_G, S, reason="fixture: the remedy the refusal names")
        record("G11", "once the determination is retired no helper reports it, so neither guard fires",
               linked(GOV_X) == [])
        record("G12", "and the remedy works: amend-extraction no longer refuses on that ground",
               "live determination" not in (amend(GOV_X) or ""))
    # ── T024: jurisdictions are rows of base_jurisdictions, admitted by a verb ──────────────
    # IMP-17. The declared vocabulary used to be an enum in code, so admitting a jurisdiction
    # meant editing a file and the pairs lang_jur_map owes named codes the writers refused.
    # Every probe is chosen by query. A refusal case asserts the message names its ground (and
    # the CLI cases that the stderr starts REFUSING:), so that an absent verb or flag cannot
    # pass as a refusal. On a tree without the registry each case RECORDS a red line instead
    # of crashing (the ids are read from this file, so a new case is covered the day it is added).
    import contextlib                                                      # noqa: E402
    import io                                                              # noqa: E402
    import re as _re24                                                     # noqa: E402
    T024_READY = (hasattr(dbcore, "declared_jurisdictions") and hasattr(db, "add_jurisdiction")
                  and bool(q("SELECT 1 FROM sqlite_master WHERE name='base_jurisdictions'")))
    if not T024_READY:
        for tid in sorted(set(_re24.findall(r'"(T024-\d\d)"', pathlib.Path(__file__).read_text(
                encoding="utf-8")))):
            record(tid, "the registry exists (base_jurisdictions, dbcore.declared_jurisdictions, "
                   "db.add_jurisdiction)", False, "absent in this tree")
    else:
        DECL0 = dbcore.declared_jurisdictions()
        MAP24 = sorted({j for (j,) in q("SELECT DISTINCT jurisdiction FROM lang_jur_map")})
        UNHELD = [j for j in MAP24 if j not in DECL0]
        ADM, OTHER = (UNHELD + [None, None])[:2]
        HELD24 = sorted(DECL0)[0]
        META = next((c for (c,) in q("SELECT jurisdiction_code FROM base_jurisdictions "
                                     "WHERE kind='meta' ORDER BY 1")), None)
        PAIR24 = q("SELECT p.slug, p.language, p.jurisdiction FROM v_coverage_priority p "
                   "JOIN base_jurisdictions b ON b.jurisdiction_code = p.jurisdiction "
                   "WHERE b.kind='country' ORDER BY p.slug, p.jurisdiction, p.language LIMIT 1")
        # A real dated, non-delegated heading found once that does not name ADM: for the CLI cases,
        # which read the real ledger (a subprocess cannot be given the fixture ledger below).
        REAL_H = next((l[3:].strip() for l in reversed(
            (REPO / "references" / "project-standards.md").read_text(encoding="utf-8").splitlines())
            if l.startswith("## ") and _re24.search(r"\d{4}-\d{2}-\d{2}", l)
            and not l[3:].startswith(dbcore.LEDGER_DELEGATED_PREFIX)
            and dbcore.ledger_heading_count(l[3:].strip()) == 1
            and ADM and not dbcore.ledger_entry_names(l[3:].strip(), ADM)), None)
        record("T024-00", "the probes exist: two owed codes the vocabulary refused, a real ledger "
               "heading, a meta code, an owed unsearched pair of a held country",
               bool(ADM and OTHER and REAL_H and META and PAIR24),
               f"adm={ADM} other={OTHER} real={REAL_H!r} meta={META} pair={PAIR24}")
        SLUG24, LANG24, COUNTRY24 = PAIR24[0]
        SUB24, DASHED = COUNTRY24 + "-T024", COUNTRY24 + "-ZZ"
        # THE FIXTURE LEDGER. The verb reads dbcore.LEDGER_PATH; the in-process cases swap it for
        # this file, whose entries stand for the owner's words (TASK-FIXTURE) and for the kinds of
        # entry that must NOT admit a code.
        H_OK = "Owner ruling 2026-11-13 — TASK-FIXTURE T024 admits some codes"
        H_NONAME = "Owner ruling 2026-11-13 — TASK-FIXTURE T024 says nothing of any code"
        H_DELEG = "Delegated resolution 2026-11-13 — TASK-FIXTURE T024 names a code"
        H_DUP = "Owner ruling 2026-11-13 — TASK-FIXTURE T024 heading found twice"
        H_SESS = "Session note 2026-11-13 — TASK-FIXTURE T024 names a code"
        named = " ".join([ADM, OTHER, SUB24, DASHED, META + "-T024", ADM + "-T024", COUNTRY24])
        FIXL = pathlib.Path(TMP) / "ledger-t024.md"
        FIXL.write_text(
            f"## {H_OK}\nThe owner admits {ADM}, {SUB24} and {HELD24}, and the fixture codes "
            f"{DASHED} {META}-T024 {ADM}-T024.\n\n## {H_NONAME}\nNothing about jurisdictions.\n\n"
            f"## {H_DELEG}\n{named}\n\n## {H_DUP}\n{named}\n\n## {H_DUP}\n{named}\n\n## {H_SESS}\n{named}\n",
            encoding="utf-8")
        REAL_LEDGER, dbcore.LEDGER_PATH = dbcore.LEDGER_PATH, FIXL
        n_jur = lambda: q("SELECT COUNT(*) FROM base_jurisdictions")[0][0]      # noqa: E731
        N0 = n_jur()

        def verb(code, kind, parent=None, ref=H_OK, session=S, dry=False):
            return refusal(db.add_jurisdiction, code, kind, parent, ref, session, dry_run=dry)

        def refused(msg, *needles):
            return msg is not None and n_jur() == N0 and all(n in msg for n in needles)

        try:
            record("T024-01", "refuses an --approval-ref with no date",
                   refused(verb(ADM, "country", ref="no date here"), "no date"))
            record("T024-02", "...one that is the heading of no ledger entry",
                   refused(verb(ADM, "country", ref="2000-01-01 an entry not in the ledger"),
                           "0 ledger entries"))
            record("T024-03", "...one found more than once",
                   refused(verb(ADM, "country", ref=H_DUP), "2 ledger entries"))
            record("T024-04", "...one whose entry says nothing of the code",
                   refused(verb(ADM, "country", ref=H_NONAME), "does not name"))
            record("T024-05", "...and one whose entry names ANOTHER code than the one admitted",
                   refused(verb(OTHER, "country", ref=H_OK), "does not name"))
            record("T024-06", "...and a delegated resolution, which is a model's and not the "
                   "owner's words, even when it names the code",
                   refused(verb(ADM, "country", ref=H_DELEG), "delegated"))
            record("T024-06b", "...and an entry that is not the owner's (a session note), even when it names "
                   "the code (_owner_approval)", refused(verb(ADM, "country", ref=H_SESS), "not an entry"))
            record("T024-07", "refuses a code already held",
                   refused(verb(HELD24, "country", ref=H_OK), "already held"))
            record("T024-08", "refuses a GB-prefixed code",
                   refused(verb(BAD, "country"), "GB"))
            shapes = [ADM.lower(), ADM[0] + " " + ADM[1:], "-", "123", ADM + "-", "-" + ADM,
                      ADM + "-A-B", ADM + "_X", COUNTRY24 + "-"]
            bad = [c for c in shapes if not refused(verb(c, "country"), "must be upper-case")]
            record("T024-09", "refuses a code that is not upper-case letters and digits, a letter "
                   "first, with at most one dash followed by a subdivision",
                   not bad, f"accepted {bad}")
            record("T024-10", "refuses a dash in a country or meta code",
                   refused(verb(DASHED, "country"), "dash belongs")
                   and refused(verb(META + "-T024", "meta"), "dash belongs"))
            record("T024-11", "refuses a --kind outside the column's CHECK, naming the kinds",
                   refused(verb(ADM, "region"), "sub-national"))
            record("T024-12", "refuses a parent on a row that is not sub-national",
                   refused(verb(ADM, "country", COUNTRY24), "sub-national"))
            record("T024-13", "refuses a sub-national row with no parent",
                   refused(verb(SUB24, "sub-national"), "--parent"))
            record("T024-14", "refuses a parent that is held but not a country, and one not held",
                   refused(verb(META + "-T024", "sub-national", META), "country")
                   and refused(verb(ADM + "-T024", "sub-national", ADM), "country"))
            record("T024-15", "refuses a sub-national code that does not start '<parent>-'",
                   refused(verb(ADM, "sub-national", COUNTRY24), f"{COUNTRY24}-"))
            record("T024-16", "refuses a blank --session",
                   refused(verb(ADM, "country", session=" "), "--session"))

            # --dry-run writes nothing; the CLI is wired to the same function.
            dry = db.add_jurisdiction(ADM, "country", None, H_OK, S, dry_run=True)
            record("T024-17", "--dry-run reports the row and leaves the table as it was",
                   dry.get("dry_run") is True and n_jur() == N0
                   and not q("SELECT 1 FROM base_jurisdictions WHERE jurisdiction_code=?", ADM),
                   f"{dry} {n_jur()} vs {N0}")
            r = run_cli("add-jurisdiction", "--code", ADM, "--kind", "country", "--session", S)
            record("T024-18", "a missing --approval-ref is argparse's usage error (rc 2): the flag "
                   "is required, so it can never be a REFUSING line",
                   r.returncode == 2 and "--approval-ref" in r.stderr, f"rc={r.returncode} {r.stderr[-200:]!r}")
            r = run_cli("add-jurisdiction", "--code", ADM, "--kind", "country",
                        "--approval-ref", REAL_H, "--session", S)
            record("T024-19", "the CLI reaches the verb: a real dated ledger entry that does not "
                   "name the code is REFUSING, and nothing is written",
                   r.returncode == 1 and r.stderr.startswith("REFUSING:") and "does not name" in r.stderr
                   and n_jur() == N0, f"rc={r.returncode} {r.stderr[-200:]!r}")

            # Admission: no file is edited, and every reader sees the code.
            cov0 = db.get_coverage_completeness(SLUG24)
            before_ok = refusal(dbcore.check_jurisdiction, ADM, "T024") is not None
            out = db.add_jurisdiction(ADM, "country", None, H_OK, S)
            row = q("SELECT kind, parent_code, admission_ref, created_by_session "
                    "FROM base_jurisdictions WHERE jurisdiction_code=?", ADM)
            record("T024-20", "add-jurisdiction admits the probe as a country with the pointer "
                   "stored and the session", row == [("country", None, H_OK, S)], f"{out} {row}")
            ls = run_cli("log-search", "--results-found", "1", "--slug", SLUG24, "--language", LANG24, "--query-text",
                         "fixture T024: a search in an admitted code", "--engine", "manual",
                         "--depth-method", "scoping", "--session", S, "--prior-expectation",
                         "fixture prior, written before the call", "--jurisdiction", ADM)
            cov1 = db.get_coverage_completeness(SLUG24)
            record("T024-21", "...then check_jurisdiction accepts it and log-search --jurisdiction "
                   "logs it",
                   before_ok and refusal(dbcore.check_jurisdiction, ADM, "T024") is None
                   and ls.returncode == 0
                   and q("SELECT COUNT(*) FROM search_executions WHERE jurisdiction=?", ADM)[0][0] >= 1,
                   f"before_refused={before_ok} log-search rc={ls.returncode} {ls.stderr[-200:]!r}")
            record("T024-22", "...and the code leaves jurisdictions_unreachable of coverage",
                   ADM in cov0["jurisdictions_unreachable"]
                   and ADM not in cov1["jurisdictions_unreachable"],
                   f"{cov0['jurisdictions_unreachable']} -> {cov1['jurisdictions_unreachable']}")

            # Roll-up (OD-04): a search under a sub-national code counts toward its country.
            pre = db.get_coverage_completeness(SLUG24)
            db.add_jurisdiction(SUB24, "sub-national", COUNTRY24, H_OK, S)
            ls = run_cli("log-search", "--results-found", "1", "--slug", SLUG24, "--language", LANG24, "--query-text",
                         "fixture T024: a search in a sub-national code", "--engine", "manual",
                         "--depth-method", "scoping", "--session", S, "--prior-expectation",
                         "fixture prior, written before the call", "--jurisdiction", SUB24)
            post = db.get_coverage_completeness(SLUG24)
            pair_open = lambda: q("SELECT 1 FROM v_coverage_priority WHERE slug=? AND language=? "   # noqa: E731
                                  "AND jurisdiction=?", SLUG24, LANG24, COUNTRY24)
            record("T024-23", "a search logged under a sub-national code raises pairs_searched by "
                   "one and removes the pair from v_coverage_priority",
                   ls.returncode == 0 and post["pairs_searched"] == pre["pairs_searched"] + 1
                   and not pair_open()
                   and [LANG24, COUNTRY24] in [list(x) for x in pre["pairs_unsearched"]],
                   f"log rc={ls.returncode} {ls.stderr[-150:]!r} searched "
                   f"{pre['pairs_searched']} -> {post['pairs_searched']} open={pair_open()}")
            record("T024-24", "...it appears under the country in v_coverage_jurisdiction, and "
                   "_in_research_scope is true for the sub-national code",
                   bool(q("SELECT 1 FROM v_coverage_jurisdiction WHERE slug=? AND jurisdiction=?",
                          SLUG24, COUNTRY24))
                   and not q("SELECT 1 FROM v_coverage_jurisdiction WHERE jurisdiction=?", SUB24)
                   and db._in_research_scope(LANG24, SUB24) is True,
                   f"scope={db._in_research_scope(LANG24, SUB24)}")

            # amend-extraction --field jurisdiction (item 4)
            X24 = q("SELECT extraction_id FROM source_value_extractions ORDER BY extraction_id "
                    "LIMIT 1")[0][0]
            NOT_HELD = next((j for j in MAP24 if j not in dbcore.declared_jurisdictions()), None)
            ax = lambda v: run_cli("amend-extraction", "--extraction-id", str(X24), "--field",     # noqa: E731
                                   "jurisdiction", "--value", v, "--reason", "fixture T024",
                                   "--session", S)
            r_ok, r_bad = ax(HELD24), ax(NOT_HELD or "ZZ")
            record("T024-25", "amend-extraction --field jurisdiction accepts a held code",
                   r_ok.returncode == 0 and q("SELECT jurisdiction FROM source_value_extractions "
                                              "WHERE extraction_id=?", X24)[0][0] == HELD24,
                   f"rc={r_ok.returncode} {r_ok.stderr[-200:]!r}")
            record("T024-26", "...and refuses a code not held",
                   r_bad.returncode != 0 and r_bad.stderr.startswith("REFUSING:")
                   and q("SELECT jurisdiction FROM source_value_extractions WHERE extraction_id=?",
                         X24)[0][0] == HELD24, f"rc={r_bad.returncode} {r_bad.stderr[-200:]!r}")

            # The table's own CHECKs hold the shapes for a row written any other way.
            def raw_insert(code, kind, parent=None, ref=None, session=None):
                con = sqlite3.connect(DB)
                try:
                    con.execute("INSERT INTO base_jurisdictions (jurisdiction_code, kind, "
                                "parent_code, admission_ref, created_by_session) "
                                "VALUES (?,?,?,?,?)", (code, kind, parent, ref, session))
                    return None
                except sqlite3.IntegrityError as exc:
                    return str(exc)
                finally:
                    con.rollback()
                    con.close()
            ctrl = raw_insert(COUNTRY24 + "-CTRL", "sub-national", COUNTRY24)
            hurt = {
                "a dash in a country": raw_insert(DASHED + "X", "country"),
                "a sub-national code with no dash": raw_insert(ADM + "S", "sub-national", COUNTRY24),
                "a sub-national code not starting with its parent": raw_insert(
                    ADM + "-Q", "sub-national", COUNTRY24),
                "an empty subdivision": raw_insert(COUNTRY24 + "-", "sub-national", COUNTRY24),
                "a second dash": raw_insert(COUNTRY24 + "-A-B", "sub-national", COUNTRY24),
                "a parent on a country": raw_insert(ADM + "P", "country", COUNTRY24),
                "no parent on a sub-national": raw_insert(COUNTRY24 + "-NP", "sub-national"),
                "lower case": raw_insert(ADM.lower() + "L", "country"),
                "a digit first": raw_insert("1" + ADM, "country"),
                "a space": raw_insert(ADM + " S", "country"),
                "a GB prefix": raw_insert(BAD + "X", "country"),
            }
            missed = [k for k, v in hurt.items() if not (v and "CHECK constraint failed" in v)]
            record("T024-27", "the table's CHECKs refuse each malformed row and accept a well-formed "
                   "sub-national one",
                   ctrl is None and not missed, f"control={ctrl!r} not refused: {missed}")

            # At rest: the blocking audit re-checks every pointer (it reads dbcore.LEDGER_PATH, the
            # fixture here) and flags a row that landed without one.
            def audit(*rows):
                path = os.path.join(TMP, "audit-t024.db")
                shutil.copy(REPO / "data" / "guidebook.db", path)
                con = sqlite3.connect(path)
                for r_ in rows:
                    con.execute("INSERT INTO base_jurisdictions (jurisdiction_code, kind, "
                                "admission_ref, created_by_session) VALUES (?,?,?,?)", r_)
                con.commit()
                con.close()
                saved = os.environ["GUIDEBOOK_DB_PATH"]
                os.environ["GUIDEBOOK_DB_PATH"] = path
                jdv.DEFAULT_DB = pathlib.Path(path)
                buf = io.StringIO()
                try:
                    with contextlib.redirect_stdout(buf):
                        rc = jdv.main()
                finally:
                    os.environ["GUIDEBOOK_DB_PATH"] = saved
                return rc, buf.getvalue()
            rc0, out0 = audit()
            rc1, out1 = audit((ADM, "country", H_OK, S))
            record("T024-28", "the audit passes the seed alone and a row whose pointer is found once "
                   "and whose entry names the code", rc0 == 0 and rc1 == 0, f"{rc0} {rc1} {out1[-300:]}")
            rc2, out2 = audit((ADM, "country", None, S))
            record("T024-29", "...flags a row that landed with a session and no admission_ref",
                   rc2 == 1 and "landed without an approval" in out2, f"{rc2} {out2[-300:]}")
            rc3, out3 = audit((ADM, "country", "2000-01-01 an entry not in the ledger", S))
            record("T024-30", "...flags a pointer no ledger heading answers",
                   rc3 == 1 and "0 ledger entries" in out3, f"{rc3} {out3[-300:]}")
            rc4, out4 = audit((ADM, "country", H_NONAME, S))
            record("T024-31", "...flags an entry that does not name the code",
                   rc4 == 1 and "does not name" in out4, f"{rc4} {out4[-300:]}")
            rc5, out5 = audit((ADM, "country", H_DELEG, S))
            record("T024-32", "...and a pointer to a delegated resolution",
                   rc5 == 1 and "delegated resolution" in out5, f"{rc5} {out5[-300:]}")
        finally:
            dbcore.LEDGER_PATH = REAL_LEDGER

    # ── T079: a deferred reading is recorded, and every deferred act lists with its age from one view ──
    # AT-17. A search, a mining pass, a reading and an adjudication can each be deferred ("deferred is okay so
    # long as it runs eventually"); only the first two carried a date and nothing listed all four. Every
    # fixture is made through the verbs; the states no verb makes are set by SQL and say so (HAND). Each case
    # RECORDS a red line when the registry is absent, so a tree without it cannot pass by skipping.
    import hashlib                                                         # noqa: E402
    import re as _re79                                                     # noqa: E402
    T079_READY = (hasattr(db, "defer_reading")
                  and bool(q("SELECT 1 FROM sqlite_master WHERE name='reading_deferrals'"))
                  and bool(q("SELECT 1 FROM sqlite_master WHERE name='v_deferred_acts'")))
    if not T079_READY:
        for tid in sorted(set(_re79.findall(r'"(T079-\d\d)"', pathlib.Path(__file__).read_text(encoding="utf-8")))):
            record(tid, "the registry exists (reading_deferrals, v_deferred_acts, db.defer_reading)", False,
                   "absent in this tree")
    else:
        rl79 = db._retrieval_log()
        AUTH79 = db.parse_author_flags(["corp|Fixture Body"])
        _n79 = iter(range(1, 10 ** 6))

        def src79(label):
            """A fixture source through the writer, titled so that no staged lead matches it."""
            return db.insert_evidence_source(
                {"year": 2020, "evidence_type": "code", "scope": "intrinsic", "verification_status": "UNVERIFIED",
                 "source_type": dbcore.schema_choices("evidence_sources", "source_type")[0],
                 "title": f"TASK-FIXTURE T079 {label} number {next(_n79)} on handrail finials"},
                S, dry_run=False, authors=AUTH79)

        def scan79(ref, scope="full", mode="catalogue", target=None):
            """A reading through record-scan, over a derived text with one page marker (so `full` is allowed)."""
            d = pathlib.Path(rl79.LOG_ROOT) / "session_fixture_t079"
            d.mkdir(exist_ok=True)
            txt = d / f"{ref}-{mode}-{scope}-text.txt"
            txt.write_text("[PDF page 1 of 1]\nTASK-FIXTURE T079 reading text.\n")
            rl79.record_file(txt, "session_fixture_t079", f"{ref}-payload.json", purpose="fixture text",
                             ref_id=ref, kind="text-extraction")
            rl79._ARTEFACT_INDEX.clear()
            return db.record_scan({"ref_id": ref, "mode": mode, "target_parameter_id": target, "text_scope": scope,
                                   "file_sha256": hashlib.sha256(txt.read_bytes()).hexdigest(),
                                   "method": "full-read", "notes": "TASK-FIXTURE T079"}, session=S)

        def vq(sql, *params):
            """Rows, or None when the SQL cannot run (an absent view must turn a case red, not crash the run)."""
            try:
                return q(sql, *params)
            except sqlite3.OperationalError as exc:
                print(f"      DEFECT: {exc}")
                return None

        def standing(kind, ref=None, pid=None):
            return vq("SELECT kind, ref_id, parameter_id, reason, deferred_at, created_by_session "
                      "FROM v_deferred_acts WHERE kind=? AND ref_id IS ? AND parameter_id IS ?", kind, ref, pid)

        def n_def():
            return q("SELECT COUNT(*) FROM reading_deferrals")[0][0]

        def defer(ref, pid, reason="TASK-FIXTURE T079: owed, not read yet", dry=False):
            return refusal(db.defer_reading, ref, pid, reason, S, dry_run=dry)

        P79 = [r[0] for r in q("SELECT parameter_id FROM base_parameters WHERE status='active' ORDER BY 1")]
        PA, PB, PRET = P79[0], P79[1], P79[-1]
        R1, R2, R3, R4, R5 = (src79(x) for x in ("one", "two", "three", "four", "five"))

        # ── T079-01 (AT-17): the kinds list together, and an age window keeps the old rows and drops the new ──
        # Nothing here depends on how many deferrals the corpus holds: each count is recomputed from the base tables
        # by the rule the view states (created_at, the date first recorded), so a batch that defers or discharges
        # something cannot turn the case red.
        n_read0 = vq("SELECT COUNT(*) FROM v_deferred_acts WHERE kind='reading'")[0][0]
        cli = run_cli("defer-reading", "--ref-id", R1, "--parameter", str(PA),
                      "--reason", "TASK-FIXTURE T079: the full text is owed", "--session", S)
        kinds = dict(vq("SELECT kind, COUNT(*) FROM v_deferred_acts GROUP BY 1") or [])
        aged = dict(vq("SELECT kind, COUNT(*) FROM v_deferred_acts WHERE deferred_at < datetime('now', '-1 days') "
                       "GROUP BY 1") or [])
        AGE = "created_at < datetime('now', '-1 days')"
        want = {"search": (q("SELECT COUNT(*) FROM search_executions WHERE deferred_reason IS NOT NULL")[0][0],
                           q(f"SELECT COUNT(*) FROM search_executions WHERE deferred_reason IS NOT NULL AND {AGE}")[0][0]),
                "mining": (q("SELECT COUNT(*) FROM citation_mining WHERE deferred_reason IS NOT NULL")[0][0],
                           q(f"SELECT COUNT(*) FROM citation_mining WHERE deferred_reason IS NOT NULL AND {AGE}")[0][0])}
        new_aged = vq("SELECT deferred_at < datetime('now', '-1 days') FROM v_deferred_acts "
                      "WHERE kind='reading' AND ref_id=? AND parameter_id=?", R1, PA)
        record("T079-01", "defer-reading lands through argparse; the view lists search, mining and reading, and "
               "an age window keeps the older rows and excludes the new reading",
               cli.returncode == 0 and kinds.get("reading", 0) == n_read0 + 1
               and all(kinds.get(k, 0) == want[k][0] and aged.get(k, 0) == want[k][1] for k in want)
               and new_aged == [(0,)],
               f"rc={cli.returncode} {cli.stderr[:200]!r} kinds={kinds} aged={aged} want={want} new_aged={new_aged}")
        got = standing("reading", R1, PA)
        record("T079-06", "the new reading row carries its reason, session, and ref and parameter as columns",
               bool(got) and got[0][3].startswith("TASK-FIXTURE T079") and got[0][5] == S
               and q("SELECT status FROM v_scan_ledger WHERE ref_id=? AND parameter_id=?", R1, PA)[0][0] == "NOT-READ",
               f"{got} (the pair stays owed in the ledger)")

        # ── T079-02: every refusal fires, names its ground, and writes nothing ──
        n0 = n_def()
        retired_was = q("SELECT status FROM base_parameters WHERE parameter_id=?", PRET)[0][0]
        w("UPDATE base_parameters SET status='retired' WHERE parameter_id=?", PRET)      # HAND: a retired parameter
        R_OLD, R_NEW = src79("tombstone"), src79("successor")
        w("UPDATE evidence_sources SET superseded_by_ref_id=? WHERE ref_id=?", R_NEW, R_OLD)   # HAND: a tombstone
        scan79(R5, "full")                                  # R5 is fully read: nothing is owed on any pair
        scan79(R4, "full", "targeted", PA)                  # R4: only PA is covered by a full reading
        scan79(R3, "partial")                               # R3: a partial reading covers nothing
        con79 = sqlite3.connect(DB)
        unminted = dbcore.next_ref_id(con79)
        con79.close()
        m = {
            "blank": defer(R2, PA, "   "),
            "no such source": defer(unminted, PA),
            "superseded": defer(R_OLD, PA),
            "retired parameter": defer(R2, PRET),
            "no such parameter": defer(R2, PRET + 1000),
            "pair covered": defer(R4, PA),
            "whole source covered": defer(R5, None),
            "pair covered by a catalogue reading": defer(R5, PB),
            "same pair twice": defer(R1, PA),
        }
        w("UPDATE base_parameters SET status=? WHERE parameter_id=?", retired_was, PRET)
        need = {"blank": "reason", "no such source": "not an admitted source", "superseded": "superseded",
                "retired parameter": "retired", "no such parameter": "no such parameter",
                "pair covered": "full reading", "whole source covered": "full reading",
                "pair covered by a catalogue reading": "full reading", "same pair twice": "already"}
        bad = {k: m[k] for k, v in m.items() if not (v and v.startswith("defer-reading:") and need[k] in v)}
        # F9: every refusal names a next action (T-043's cue: a verb, a query or a flag) and says nothing was written
        CUE79 = _re79.compile(r"db\.py |SELECT |--[a-z]|git ls-files")
        mute = {k: v for k, v in m.items() if not (v and CUE79.search(v) and v.rstrip().endswith("Nothing was written."))}
        record("T079-02", "defer-reading refuses a blank reason, an unknown or superseded source, a retired or "
               "unknown parameter, a pair a full reading covers and a second standing deferral, naming each ground, "
               "a next action, and that nothing was written",
               not bad and not mute and n_def() == n0,
               f"unrefused or unnamed: {bad} no next action / no 'Nothing was written.': {mute} rows {n0}->{n_def()}")
        cli2 = run_cli("defer-reading", "--ref-id", R2, "--parameter", str(PA), "--reason", " ", "--session", S)
        record("T079-07", "through argparse a refusal exits non-zero with stderr starting REFUSING:",
               cli2.returncode != 0 and cli2.stderr.startswith("REFUSING:"), f"{cli2.returncode} {cli2.stderr[:120]!r}")
        # what is NOT refused: a partial reading covers nothing, a targeted full reading covers only its target,
        # and a whole-source deferral is allowed while any pair is owed
        ok_partial, ok_other_pair, ok_whole = defer(R3, PA), defer(R4, PB), defer(R4, None)
        record("T079-08", "a partial reading, an uncovered pair of a partly read source and the whole source "
               "(NULL parameter) of a source with owed pairs are all deferrable",
               ok_partial is None and ok_other_pair is None and ok_whole is None and n_def() == n0 + 3,
               f"{ok_partial!r} {ok_other_pair!r} {ok_whole!r} rows {n0}->{n_def()}")
        twice_whole = defer(R4, None)
        record("T079-17", "a second standing whole-source deferral (NULL parameter) is refused like a second pair",
               twice_whole is not None and twice_whole.startswith("defer-reading:") and "already" in twice_whole,
               f"{twice_whole!r}")
        n1 = n_def()
        dry = defer(R2, PA, dry=True)
        record("T079-09", "--dry-run writes nothing", dry is None and n_def() == n1, f"{dry!r}")

        # ── T079-03: the discharge is derived from a reading, never a write ──
        listed_first = bool(standing("reading", R3, PA))
        scan79(R3, "partial")
        still_partial = bool(standing("reading", R3, PA))
        scan79(R3, "full", "targeted", PB)
        still_other = bool(standing("reading", R3, PA))
        scan79(R3, "full", "targeted", PA)
        gone = not standing("reading", R3, PA)
        kept = q("SELECT COUNT(*) FROM reading_deferrals WHERE ref_id=? AND parameter_id=?", R3, PA)[0][0] == 1
        record("T079-03", "a partial reading does not discharge; a full reading of another parameter does not; "
               "a full reading of the pair does, and the deferral row stays as history",
               listed_first and still_partial and still_other and gone and kept,
               f"{listed_first} {still_partial} {still_other} {gone} {kept}")
        before_whole = bool(standing("reading", R4, None))
        scan79(R4, "partial")                               # a partial catalogue reading is not a full one
        partial_only = bool(standing("reading", R4, None))
        scan79(R4, "full", "targeted", PB)                  # a full TARGETED reading is not a full catalogue reading
        targeted_only = bool(standing("reading", R4, None))
        scan79(R4, "full")                                  # R4's whole-source deferral: a full catalogue reading
        whole_gone = not standing("reading", R4, None)
        record("T079-10", "a whole-source deferral is discharged by a full catalogue reading, not by a partial "
               "one or a full targeted one", before_whole and partial_only and targeted_only and whole_gone,
               f"{before_whole} {partial_only} {targeted_only} {whole_gone}")
        # NO DATE CLAUSE (F2/F3/F4): a deferral stands iff its cell is, now, owed. R4 is read in full at the current
        # version, so a deferral dated far in the future and one dated far in the past both leave the view.
        w("INSERT INTO reading_deferrals (ref_id, parameter_id, reason, created_at, created_by_session) "
          "VALUES (?, NULL, 'TASK-FIXTURE T079 dated later than every reading', '2999-01-01 00:00', ?)", R4, S)
        later = standing("reading", R4, None)
        w("INSERT INTO reading_deferrals (ref_id, parameter_id, reason, created_at, created_by_session) "
          "VALUES (?, NULL, 'TASK-FIXTURE T079 dated before every reading', '2000-01-01 00:00', ?)", R4, S)
        earlier = standing("reading", R4, None)
        record("T079-11", "a deferral over a cell a full reading covers does not list, whatever its date (the date "
               "is no discharge rule: a later-dated deferral cannot outlive the reading, an earlier one cannot hide)",
               later == [] and earlier == [], f"{later} {earlier}")
        # a later state change: a superseded source's deferral is its SUCCESSOR's (the replacement is what is owed),
        # with the date the obligation was first recorded; a retired parameter's deferral leaves (nothing is owed)
        w("UPDATE reading_deferrals SET created_at='2001-02-03 04:05' WHERE ref_id=? AND parameter_id=?", R1, PA)   # HAND: an old obligation
        at_r1 = q("SELECT created_at FROM reading_deferrals WHERE ref_id=? AND parameter_id=?", R1, PA)[0][0]
        w("UPDATE evidence_sources SET superseded_by_ref_id=? WHERE ref_id=?", R_NEW, R1)       # HAND: after the deferral
        under_old = standing("reading", R1, PA)
        under_new = standing("reading", R_NEW, PA)
        twice_new = defer(R_NEW, PA)
        w("UPDATE evidence_sources SET superseded_by_ref_id=NULL WHERE ref_id=?", R1)
        w("UPDATE base_parameters SET status='retired' WHERE parameter_id=?", PA)               # HAND: after the deferral
        gone_ret = not standing("reading", R1, PA)
        w("UPDATE base_parameters SET status='active' WHERE parameter_id=?", PA)
        back = bool(standing("reading", R1, PA))
        record("T079-12", "a deferral on a source later superseded is its successor's, with its original date (and "
               "the successor cannot be deferred a second time); one on a parameter later retired no longer lists; "
               "both list again when the state is undone",
               under_old == [] and len(under_new or []) == 1 and under_new[0][4] == at_r1
               and twice_new is not None and "already" in twice_new and gone_ret and back,
               f"old={under_old} new={under_new} at={at_r1} twice={twice_new} {gone_ret} {back}")

        # ── T079-04: a mining deferral is discharged by log-mining, read from the owner's execution signal ──
        mine = q("SELECT cm.slug, COALESCE(cm.global_ref_id, cm.local_ref_id) FROM citation_mining cm "
                 "JOIN evidence_sources e ON e.ref_id = COALESCE(cm.global_ref_id, cm.local_ref_id) "
                 "WHERE cm.deferred_reason IS NOT NULL AND e.citation_mining_status = 'deferred' ORDER BY 2 LIMIT 2")
        (SL1, MR1), (SL2, MR2) = mine[0], mine[1]
        mcount = lambda ref: vq("SELECT COUNT(*) FROM v_deferred_acts WHERE kind='mining' AND ref_id=?", ref)[0][0]  # noqa: E731
        n_mine0 = vq("SELECT COUNT(*) FROM v_deferred_acts WHERE kind='mining'")[0][0]
        dbl = mcount(MR1)
        # a pass that RAN without --discharge-deferral leaves the deferral standing (one column, two directions)
        out_a = db.log_mining(SL1, MR1, "backward", S, notes="TASK-FIXTURE T079: a pass that ran")
        after_a = mcount(MR1)
        db.log_mining(SL2, MR2, "backward", S, notes="TASK-FIXTURE T079: the pass that discharges",
                      discharge_deferral=True)
        after_b = mcount(MR2)
        n_mine1 = vq("SELECT COUNT(*) FROM v_deferred_acts WHERE kind='mining'")[0][0]
        status_b = q("SELECT citation_mining_status FROM evidence_sources WHERE ref_id=?", MR2)[0][0]
        record("T079-04", "a mining deferral lists once; a pass without --discharge-deferral leaves it listed; "
               "log-mining --discharge-deferral takes it out, with the source's status 'mined'",
               dbl == 1 and after_a == 1 and after_b == 0 and n_mine1 == n_mine0 - 1 and status_b == "mined"
               and bool(out_a.get("deferral_still_standing")),
               f"{dbl} {after_a} {after_b} {n_mine0}->{n_mine1} {status_b} {out_a}")
        # F1: the typed fact lives in the ROW. The source's status is one flag for every slug and both directions, so a
        # pass that ran for another reason sets it to 'mined' and must not hide a standing deferral.
        w("UPDATE evidence_sources SET citation_mining_status='mined' WHERE ref_id=?", MR1)     # HAND: the flag alone
        sig = mcount(MR1)
        w("UPDATE evidence_sources SET citation_mining_status='deferred' WHERE ref_id=?", MR1)
        record("T079-13", "the source's citation_mining_status 'mined' does not take a mining deferral out of the view: "
               "only clearing the row's own deferred_reason (--discharge-deferral) does", sig == 1, f"{sig}")
        # the reproduction as the critic gave it: deferred under slug A, also linked to slug B, a pass logged for B
        SLB = q("SELECT slug FROM slugs WHERE slug NOT IN (SELECT slug FROM source_slug_links WHERE ref_id=?) "
                "ORDER BY slug LIMIT 1", MR1)[0][0]
        db.link_source_slug(MR1, SLB, "TASK-FIXTURE T079: a second slug for the same source", S)
        row_a = q("SELECT deferred_reason FROM citation_mining WHERE slug=? AND global_ref_id=?", SL1, MR1)[0][0]
        out_b = db.log_mining(SLB, MR1, "backward", S, notes="TASK-FIXTURE T079: a pass for the other slug")
        status_after = q("SELECT citation_mining_status FROM evidence_sources WHERE ref_id=?", MR1)[0][0]
        record("T079-21", "a mining deferral under slug A still lists after an unrelated pass for slug B sets the "
               "source to 'mined', and the pass's reply says the deferral still stands",
               mcount(MR1) == 1 and row_a and row_a in (out_b.get("deferral_still_standing") or "")
               and SL1 in (out_b.get("deferral_still_standing") or ""),
               f"listed={mcount(MR1)} status={status_after} {out_b}")
        w("UPDATE evidence_sources SET citation_mining_status='deferred' WHERE ref_id=?", MR1)

        # a lead anchor (a ref that resolves in source_locators, not evidence_sources) has no status to read: its own
        # deferred_reason is the signal, so it lists (an inner join to evidence_sources would drop it silently)
        w("INSERT INTO citation_mining (slug, local_ref_id, global_ref_id, deferred_reason, created_at, created_by_session, "
          "updated_at, updated_by_session) VALUES (?, 'LEAD-T079', NULL, 'TASK-FIXTURE T079: a lead anchor', "
          "'2026-01-01 00:00', ?, '2026-01-01 00:00', ?)", A, S, S)
        lead = vq("SELECT kind, ref_id, deferred_at FROM v_deferred_acts WHERE kind='mining' AND ref_id='LEAD-T079'")
        record("T079-16", "a deferred mining row whose ref is no evidence_sources row (a lead anchor) lists, dated from "
               "its row", lead == [("mining", "LEAD-T079", "2026-01-01 00:00")], f"{lead}")

        # ── T079-05: the adjudication arm lists an observation whose LATEST adjudication is DEFERRED ──
        LATEST79 = ("WITH l AS (SELECT a.* FROM term_adjudications a WHERE a.adjudication_id = "
                    "(SELECT MAX(adjudication_id) FROM term_adjudications b WHERE b.observation_id = a.observation_id)) ")
        pick = q(LATEST79 + "SELECT observation_id FROM l WHERE outcome='DEFERRED' ORDER BY 1 LIMIT 1")
        if not pick:                                        # HAND (TASK-FIXTURE): adjudicate one DEFERRED on the copy
            obs0 = q("SELECT observation_id FROM observed_terms ORDER BY 1 LIMIT 1")[0][0]
            db.adjudicate_term(obs0, "DEFERRED", "TASK-FIXTURE T079: held", S)
            pick = [(obs0,)]
        OB = pick[0][0]
        row = vq("SELECT kind, ref_id, reason, deferred_at, created_by_session, subject FROM v_deferred_acts "
                 "WHERE kind='adjudication' AND subject LIKE ?", f"%observation {OB} %")
        lat = q(LATEST79 + "SELECT rationale, created_at, created_by_session FROM l WHERE observation_id=?", OB)[0]
        o_ref, o_form = q("SELECT ref_id, surface_form FROM observed_terms WHERE observation_id=?", OB)[0]
        n_adj = vq("SELECT COUNT(*) FROM v_deferred_acts WHERE kind='adjudication'")[0][0]
        n_adj_expect = q(LATEST79 + "SELECT COUNT(*) FROM l WHERE outcome='DEFERRED'")[0][0]
        TERMX = q("SELECT term_id FROM terms ORDER BY term_id LIMIT 1")[0][0]
        db.adjudicate_term(OB, "NAMES-EXISTING", "TASK-FIXTURE T079: settled", S, term_id=TERMX)
        gone_adj = not vq("SELECT 1 FROM v_deferred_acts WHERE kind='adjudication' AND subject LIKE ?",
                          f"%observation {OB} %")
        # the reverse order: an older settled judgment and a newer DEFERRED one lists
        db.adjudicate_term(OB, "DEFERRED", "TASK-FIXTURE T079: re-opened", S)
        reopened = vq("SELECT reason FROM v_deferred_acts WHERE kind='adjudication' AND subject LIKE ?",
                      f"%observation {OB} %")
        record("T079-05", "an observation whose latest adjudication is DEFERRED lists with its source, surface form, "
               "rationale, date and session; a later adjudication of another outcome takes it out; a newer DEFERRED "
               "over an older outcome lists; 'DEFERRED' is in the column's CHECK",
               len(row or []) == 1 and row[0][1] == o_ref and row[0][2] == lat[0] and row[0][3] == lat[1]
               and row[0][4] == lat[2] and o_form in row[0][5] and n_adj == n_adj_expect and gone_adj
               and bool(reopened) and reopened[0][0] == "TASK-FIXTURE T079: re-opened"
               and "DEFERRED" in dbcore.check_values(sqlite3.connect(DB), "term_adjudications", "outcome"),
               f"{row} {lat} {n_adj}/{n_adj_expect} gone={gone_adj} reopened={reopened}")

        # two judgments in the SAME minute (created_at is minute-resolution): the higher adjudication_id governs
        db.adjudicate_term(OB, "NAMES-EXISTING", "TASK-FIXTURE T079: settled again, same minute", S, term_id=TERMX)
        tie = vq("SELECT 1 FROM v_deferred_acts WHERE kind='adjudication' AND subject LIKE ?", f"%observation {OB} %")
        record("T079-18", "an observation judged DEFERRED and then settled in the same minute does not list (the "
               "higher id governs, not the date)", tie == [], f"{tie}")
        # a search that names no slug (a parameter, or a mined source) is deferred too, and lists
        db.log_search(slug=None, parameter_id=PA, language="EN", query_text="TASK-FIXTURE T079: a slug-less search",
                      engine="manual", depth_method="scoping", session=S, deferred_reason="TASK-FIXTURE T079: held",
                      prior_expectation="fixture prior, written before the call")
        slugless = vq("SELECT kind, parameter_id, reason FROM v_deferred_acts WHERE kind='search' AND parameter_id=?", PA)
        record("T079-19", "a deferred search naming no slug lists, with its parameter",
               slugless == [("search", PA, "TASK-FIXTURE T079: held")], f"{slugless}")

        # merge-parameter finds every table holding a parameter_id from the live schema and REFUSES one with no notes
        # column unless it is argued into _MERGE_KEEPS_HISTORY: reading_deferrals must be, or a deferral blocks a merge
        def merge_try(fa, into):
            try:
                return db.merge_parameter(fa, into, "TASK-FIXTURE T079", S, dry_run=True)
            except Refusal as exc:
                return str(exc)
        pair79 = next(((fa, into) for fa in P79 for into in P79 if fa != into
                       and isinstance(merge_try(fa, into), dict)), None)     # two active parameters with no live work
        merge79 = None
        if pair79:
            R6 = src79("six")
            defer(R6, pair79[0], "TASK-FIXTURE T079: a deferral on the folded parameter")
            merge79 = merge_try(*pair79)
        record("T079-20", "merge-parameter is not blocked by a reading deferral on the folded parameter: the rows are "
               "kept as history (no notes column to move them with)",
               isinstance(merge79, dict) and "reading_deferrals.parameter_id" in merge79["kept_as_history"],
               f"{merge79}")

        # ── F3: the same-minute tie. A full catalogue reading, a parameter minted after it, a whole-source deferral ──
        R10 = src79("ten")
        scan79(R10, "full")
        w("UPDATE source_scans SET catalogue_version=? WHERE ref_id=?", P79[-2], R10)    # HAND: P79[-1] minted after it
        led10 = q("SELECT status FROM v_scan_ledger WHERE ref_id=? AND parameter_id=?", R10, P79[-1])[0][0]
        first10 = defer(R10, None)
        listed10 = bool(standing("reading", R10, None))
        second10 = defer(R10, None)
        record("T079-22", "a whole-source deferral recorded in the minute of a full catalogue reading that predates a "
               "parameter lists (the ledger says that parameter is NOT-READ), and a second is refused",
               led10 == "NOT-READ" and first10 is None and listed10 and second10 is not None and "already" in second10,
               f"ledger={led10} first={first10!r} listed={listed10} second={second10!r}")

        # ── F2: a whole-source deferral, then TARGETED full readings of every active parameter ──
        R9 = src79("nine")
        d9 = defer(R9, None)
        for pid9 in P79:
            scan79(R9, "full", "targeted", pid9)
        listed9 = standing("reading", R9, None)
        again9 = defer(R9, None)
        record("T079-23", "a whole-source deferral followed by targeted full readings of every active parameter leaves "
               "the view, and the verb agrees (it refuses a second: no reading is owed)",
               d9 is None and listed9 == [] and again9 is not None and "full reading" in again9,
               f"{d9!r} listed={listed9} {again9!r}")

        # ── the verb and the view agree on every state of a cell (one definition of owed, read by both) ──
        RA, RB, RC, RD, RE, RF, RG = (src79(f"matrix {x}") for x in "abcdefg")
        scan79(RA, "full")                                          # RA: a full catalogue reading
        scan79(RB, "full", "targeted", PA)                          # RB: a full targeted reading of PA only
        scan79(RC, "partial")                                       # RC: a partial reading
        for pid in P79:
            if pid != PB:
                scan79(RE, "full", "targeted", pid)                 # RE: every parameter but PB
            scan79(RF, "full", "targeted", pid)                     # RF: every parameter, by targeted readings
        w("UPDATE evidence_sources SET processing_blocked_reason='paywalled' WHERE ref_id=?", RG)   # HAND: a block
        cells = [("pair covered by a catalogue reading", RA, PA, False),
                 ("pair covered by a targeted reading", RB, PA, False),
                 ("another pair of a targeted source", RB, PB, True),
                 ("pair read only in part", RC, PA, True),
                 ("pair never read", RD, PA, True),
                 ("whole source, one parameter uncovered", RE, None, True),
                 ("whole source, every parameter covered by a targeted reading", RF, None, False),
                 ("blocked pair", RG, PA, False),
                 ("blocked whole source", RG, None, False)]
        split = {}
        for label, cref, cpid, expect in cells:
            verb_takes = defer(cref, cpid, dry=True) is None
            w("INSERT INTO reading_deferrals (ref_id, parameter_id, reason, created_at, created_by_session) "
              "VALUES (?, ?, 'TASK-FIXTURE T079 matrix', ?, ?)", cref, cpid, dbcore.now(), S)      # HAND: bypass the verb
            view_lists = bool(standing("reading", cref, cpid))
            w("DELETE FROM reading_deferrals WHERE reason='TASK-FIXTURE T079 matrix'")
            if not (verb_takes == view_lists == expect):
                split[label] = {"verb accepts": verb_takes, "view lists": view_lists, "owed": expect}
        record("T079-24", "the verb accepts a deferral exactly when the view lists one for that cell, over a pair covered "
               "by a catalogue or a targeted reading, a pair read in part or not at all, a whole source with one "
               "parameter uncovered or none, and a blocked source", not split, f"{split}")

        # ── F8: a blocked source is not reading debt (the ledger says so) ──
        blk_pair, blk_whole = defer(RG, PA), defer(RG, None)
        record("T079-25", "a source the ledger reads BLOCKED is refused, naming the block and what to do, with nothing written",
               all(v and v.startswith("defer-reading:") and "paywalled" in v and "BLOCKED" in v
                   and CUE79.search(v) and v.rstrip().endswith("Nothing was written.") for v in (blk_pair, blk_whole)),
               f"{blk_pair!r} {blk_whole!r}")

        # ── F6: the age is the date the obligation was first recorded; touching a row resets nothing ──
        cm = q("SELECT slug, local_ref_id, COALESCE(global_ref_id, local_ref_id), created_at FROM citation_mining "
               "WHERE deferred_reason IS NOT NULL ORDER BY 1, 2 LIMIT 1")[0]
        se = q("SELECT exec_id, created_at FROM search_executions WHERE deferred_reason IS NOT NULL ORDER BY 1 LIMIT 1")[0]
        w("UPDATE citation_mining SET updated_at='2999-01-01 00:00' WHERE slug=? AND local_ref_id=?", cm[0], cm[1])
        w("UPDATE search_executions SET updated_at='2999-01-01 00:00' WHERE exec_id=?", se[0])
        at_m = vq("SELECT deferred_at FROM v_deferred_acts WHERE kind='mining' AND subject=?", f"{cm[2]} {cm[0]}")
        at_s = vq("SELECT deferred_at FROM v_deferred_acts WHERE kind='search' AND subject LIKE ?", f"exec {se[0]} %")
        at_s = at_s or vq("SELECT deferred_at FROM v_deferred_acts WHERE kind='search' AND subject = ?", f"exec {se[0]}")
        record("T079-26", "a deferred mining row and a deferred search keep the date first recorded when their "
               "updated_at moves (an age that reset on a touch would hide an old obligation)",
               at_m == [(cm[3],)] and at_s == [(se[1],)], f"mining {at_m} vs {cm[3]}; search {at_s} vs {se[1]}")

        # a mining deferral on a source is not a reading deferral of it (the standing check reads kind='reading' only)
        R7 = src79("seven")
        w("INSERT INTO citation_mining (slug, local_ref_id, global_ref_id, deferred_reason, created_at, "
          "created_by_session, updated_at, updated_by_session) VALUES (?, ?, ?, 'TASK-FIXTURE T079: a mining deferral "
          "on the same source', '2026-01-01 00:00', ?, '2026-01-01 00:00', ?)", A, R7, R7, S, S)      # HAND
        with_mining = defer(R7, None)
        both7 = (vq("SELECT COUNT(*) FROM v_deferred_acts WHERE kind='mining' AND ref_id=?", R7),
                 vq("SELECT COUNT(*) FROM v_deferred_acts WHERE kind='reading' AND ref_id=?", R7))
        record("T079-27", "a standing mining deferral on a source does not refuse its reading deferral (the two are "
               "different promises)", with_mining is None and both7 == ([(1,)], [(1,)]), f"{with_mining!r} {both7}")

        # the CLI's --dry-run reaches the verb (argparse -> dispatch), so a dry run through the real entry point writes nothing
        n_dry = n_def()
        cli_dry = run_cli("defer-reading", "--ref-id", RD, "--parameter", str(PB),
                          "--reason", "TASK-FIXTURE T079: a dry run through the CLI", "--session", S, "--dry-run")
        record("T079-28", "defer-reading --dry-run through the CLI writes nothing",
               cli_dry.returncode == 0 and n_def() == n_dry, f"rc={cli_dry.returncode} {cli_dry.stderr[:200]!r} {n_dry}->{n_def()}")

        # a lower-case reference id folds to the stored one, as every other writer's does
        R8 = src79("eight")
        lower = defer(R8.lower(), PB)
        stored = standing("reading", R8, PB)
        record("T079-29", "a lower-case ref id is folded (dbcore.fold_ref) and the row is stored under the canonical id",
               lower is None and len(stored or []) == 1, f"{lower!r} {stored}")

        # F10: the session, and the shape of a reason
        LIM79 = getattr(db, "_DEFER_REASON_MAX", 1000)
        shape = {
            "blank session": (refusal(db.defer_reading, R2, PB, "TASK-FIXTURE T079: why", "  ", dry_run=True), "session"),
            "invisible reason": (defer(R2, PB, "\u200b\u200b\u200b", dry=True), "letter or digit"),
            "multi-line reason": (defer(R2, PB, "line one\nline two", dry=True), "one line"),
            "over-long reason": (defer(R2, PB, "x" * (LIM79 + 1), dry=True), str(LIM79)),
        }
        at_limit = defer(R2, PB, "x" * LIM79, dry=True)
        cli_ws = run_cli("defer-reading", "--ref-id", R2, "--parameter", str(PB), "--reason", "TASK-FIXTURE T079: why",
                         "--session", " ", "--dry-run")
        bad_shape = {k: v for k, (v, tok) in shape.items()
                     if not (v and v.startswith("defer-reading:") and tok in v and v.rstrip().endswith("Nothing was written."))}
        record("T079-30", "a blank session, an invisible-only reason, a multi-line reason and one over the stated limit are "
               "refused naming their ground; a reason at the limit passes",
               not bad_shape and at_limit is None and cli_ws.returncode != 0 and cli_ws.stderr.startswith("REFUSING:"),
               f"{bad_shape} at_limit={at_limit!r} cli={cli_ws.returncode} {cli_ws.stderr[:160]!r}")

        # ── T079-14: the arms agree with the tables they read (derived, never typed), and no row lists twice ──
        arms = dict(vq("SELECT kind, COUNT(*) FROM v_deferred_acts GROUP BY 1") or [])
        want_search = q("SELECT COUNT(*) FROM search_executions WHERE deferred_reason IS NOT NULL")[0][0]
        want_adj = q(LATEST79 + "SELECT COUNT(*) FROM l WHERE outcome='DEFERRED'")[0][0]
        rows_total = vq("SELECT COUNT(*) FROM v_deferred_acts")[0][0]
        distinct = vq("SELECT COUNT(*) FROM (SELECT DISTINCT kind, subject, deferred_at FROM v_deferred_acts)")[0][0]
        record("T079-14", "the search and adjudication arms count what their tables hold, and no row is listed twice",
               arms.get("search") == want_search and arms.get("adjudication") == want_adj and rows_total == distinct,
               f"{arms} search={want_search} adj={want_adj} total={rows_total} distinct={distinct}")
        record("T079-15", "reading_deferrals is in dbcore.writable_tables (the capture path sees it)",
               "reading_deferrals" in dbcore.writable_tables(sqlite3.connect(DB)), "")

        # ── F4 + F7: merge-parameter folds a parameter in. Its deferral is the survivor's, with its original date, and a
        # full reading it re-points onto the survivor discharges a deferral of the survivor's pair (a REAL merge, last) ──
        if pair79:
            fa, into = pair79
            R12, R13 = src79("twelve"), src79("thirteen")
            defer(R12, fa, "TASK-FIXTURE T079: a deferral on the folded parameter, kept with its age")
            defer(R13, into, "TASK-FIXTURE T079: a deferral on the survivor's pair")
            scan79(R13, "full", "targeted", fa)
            w("UPDATE source_scans SET created_at='2000-01-01 00:00' WHERE ref_id=?", R13)       # HAND: older than the deferral
            w("UPDATE reading_deferrals SET created_at='2001-02-03 04:05' WHERE ref_id=? AND parameter_id=?", R12, fa)   # HAND: an old obligation
            at12 = q("SELECT created_at FROM reading_deferrals WHERE ref_id=? AND parameter_id=?", R12, fa)[0][0]
            listed_before = bool(standing("reading", R13, into))
            merged = db.merge_parameter(fa, into, "TASK-FIXTURE T079", S)
            moved12 = standing("reading", R12, into)
            gone13 = standing("reading", R13, into)
            again12, again13 = defer(R12, into), defer(R13, into)
            on_folded = defer(R12, fa)
            record("T079-31", "after a merge, a deferral on the folded parameter lists as the survivor's with its original "
                   "date (and the survivor cannot be deferred again); a full reading the merge re-points onto the survivor "
                   "discharges a deferral of its pair; the folded parameter cannot be deferred",
                   isinstance(merged, dict) and listed_before and len(moved12 or []) == 1 and moved12[0][4] == at12
                   and gone13 == [] and again12 is not None and "already" in again12
                   and again13 is not None and "full reading" in again13
                   and on_folded is not None and "merged" in on_folded and str(into) in on_folded,
                   f"{merged} before={listed_before} {moved12} at={at12} {gone13} {again12!r} {again13!r} {on_folded!r}")
        else:
            record("T079-31", "a merge case needs two active parameters with no live work", False, "none on the copy")

    # ── T083: set-parameter-kind sets the kind and its warrant on an existing parameter, once ─────────────────
    # What reaches the guidebook without it: T-109 could give the live parameters their kind only by hand SQL, and a
    # parameter with no kind cannot have its units checked against the right family. Probes are derived on the copy.
    print("Section T083: set-parameter-kind (the kind and its warrant on an existing parameter, written once)")
    FREE_P = ("SELECT parameter_id FROM base_parameters p WHERE status='active' AND quantity_kind IS NULL "
              "AND NOT EXISTS (SELECT 1 FROM specifications s WHERE s.parameter_id=p.parameter_id AND s.retired_at IS NULL) "
              "AND NOT EXISTS (SELECT 1 FROM determination_gates g WHERE g.parameter_id=p.parameter_id AND g.resolved_at IS NULL) "
              "ORDER BY parameter_id")
    free_p = [r[0] for r in q(FREE_P)]
    kinds83 = [r[0] for r in q("SELECT kind_id FROM base_quantity_kinds ORDER BY kind_id")]
    W83 = dict(KIND_WARRANT, quantity_kind_ref_id="TASK-FIXTURE")
    if len(free_p) < 3 or not kinds83:
        record("T083-00", "three active parameters with no kind and no live work, and a kind", False, f"{free_p} {kinds83}")
    else:
        p1, p2, p3 = free_p[:3]
        cols = [r[1] for r in q("PRAGMA table_info(base_parameters)")]
        kind_cols = {"quantity_kind", "quantity_kind_source_url", "quantity_kind_source_page", "quantity_kind_source_line",
                     "quantity_kind_source_clause", "quantity_kind_ref_id", "quantity_kind_quote", "updated_at",
                     "updated_by_session"}
        before = dict(zip(cols, q("SELECT * FROM base_parameters WHERE parameter_id=?", p1)[0]))
        cp = run_cli("set-parameter-kind", "--parameter-id", str(p1), "--quantity-kind", kinds83[0],
                     "--quantity-kind-source-url", W83["quantity_kind_source_url"],
                     "--quantity-kind-source-page", W83["quantity_kind_source_page"],
                     "--quantity-kind-ref-id", W83["quantity_kind_ref_id"],
                     "--quantity-kind-quote", W83["quantity_kind_quote"], "--session", S)
        after = dict(zip(cols, q("SELECT * FROM base_parameters WHERE parameter_id=?", p1)[0]))
        record("T083-01", "set-parameter-kind (through argparse) writes the kind, the locator and the ref_id on an existing "
               "parameter, stamps updated_*, and leaves every other column unchanged",
               cp.returncode == 0 and after["quantity_kind"] == kinds83[0]
               and after["quantity_kind_source_url"] == W83["quantity_kind_source_url"]
               and after["quantity_kind_source_page"] == W83["quantity_kind_source_page"]
               and after["quantity_kind_ref_id"] == "TASK-FIXTURE" and after["updated_by_session"] == S
               and after["quantity_kind_quote"] == W83["quantity_kind_quote"]
               and all(after[c] == before[c] for c in cols if c not in kind_cols),
               f"rc={cp.returncode} {cp.stderr[-300:]!r} {after}")
        spk = db.set_parameter_kind
        r_unknown = refusal(spk, p2, "zz_" + kinds83[0], S, **W83)
        r_none = refusal(spk, p2, kinds83[0], S)
        r_nopage = refusal(spk, p2, kinds83[0], S, quantity_kind_source_url=W83["quantity_kind_source_url"])
        r_url = refusal(spk, p2, kinds83[0], S, **dict(W83, quantity_kind_source_url="ftp://example.org/x"))
        r_noq = refusal(spk, p2, kinds83[0], S, **dict(W83, quantity_kind_quote=None))
        r_nodig = refusal(spk, p2, kinds83[0], S, **dict(W83, quantity_kind_quote="TASK-FIXTURE: wide enough"))
        r_zwp = refusal(spk, p2, kinds83[0], S, **dict(W83, quantity_kind_source_page="3\u200b"))
        r_zwc = refusal(spk, p2, kinds83[0], S, **dict(W83, quantity_kind_source_clause="\u200b4.1"))
        record("T083-02", "the shared refusals fire through the new verb: an unknown kind (naming every kind and add-quantity-kind), "
               "no warrant, a URL with no page or clause, a non-http URL, no quote, a quote with no digit, U+200B in the page or "
               "the clause; nothing written",
               r_unknown and all(k in r_unknown for k in kinds83) and "add-quantity-kind" in r_unknown
               and r_none and "--quantity-kind-source-url" in r_none and r_nopage and "--quantity-kind-source-page" in r_nopage
               and r_url and "--quantity-kind-source-url" in r_url and r_noq and "--quantity-kind-quote" in r_noq
               and r_nodig and "holds no digit" in r_nodig and r_zwp and "invisible" in r_zwp and "--quantity-kind-source-page" in r_zwp
               and r_zwc and "invisible" in r_zwc and "--quantity-kind-source-clause" in r_zwc
               and q("SELECT quantity_kind FROM base_parameters WHERE parameter_id=?", p2)[0][0] is None,
               (r_unknown, r_none, r_nopage, r_url, r_noq, r_nodig, r_zwp, r_zwc))
        other = kinds83[-1]
        r_again = refusal(spk, p1, other, S, **W83)
        record("T083-03", "a second call on the same parameter is refused (written once), naming the stored kind and its warrant, "
               "and the stored kind is unchanged",
               r_again and repr(kinds83[0]) in r_again and W83["quantity_kind_source_url"] in r_again and "written once" in r_again
               and q("SELECT quantity_kind FROM base_parameters WHERE parameter_id=?", p1)[0][0] == kinds83[0], r_again)
        db.retire_parameter(p2, "TASK-FIXTURE T083: a retired parameter", S)
        r_ret = refusal(spk, p2, kinds83[0], S, **W83)
        db.merge_parameter(p3, free_p[3] if len(free_p) > 3 else p1, "TASK-FIXTURE T083: a merged parameter", S)
        surv = q("SELECT merged_into FROM base_parameters WHERE parameter_id=?", p3)[0][0]
        r_mer = refusal(spk, p3, kinds83[0], S, **W83)
        gated = q("SELECT g.parameter_id FROM determination_gates g JOIN base_parameters p USING (parameter_id) "
                  "WHERE g.resolved_at IS NULL AND p.status='active' AND p.quantity_kind IS NULL ORDER BY 1 LIMIT 1")
        r_gate = refusal(spk, gated[0][0], kinds83[0], S, **W83) if gated else "SKIPPED-NO-FIXTURE"
        spec = q("SELECT s.specification_id, s.parameter_id FROM specifications s JOIN base_parameters p USING (parameter_id) "
                 "WHERE s.retired_at IS NOT NULL AND p.status='active' AND p.quantity_kind IS NULL ORDER BY 1 LIMIT 1")
        if spec:
            con83 = sqlite3.connect(DB)
            unretire(con83, spec[0][0])          # HAND, on the copy: a TASK-FIXTURE live determination (no writer revives one)
            con83.commit()
            con83.close()
            r_live = refusal(spk, spec[0][1], kinds83[0], S, **W83)
            reretire(spec[0][0])
        else:
            r_live = "SKIPPED-NO-FIXTURE"
        record("T083-04", "a retired parameter is refused; a merged one names its survivor; a live determination and an open gate "
               "on the parameter are refused (SKIPPED-NO-FIXTURE where the copy holds none)",
               r_ret and "retired" in r_ret and r_mer and "merged" in r_mer and f"parameter {surv}" in r_mer
               and r_gate and (("OPEN determination gate" in r_gate and "must be resolved before the parameter is given its kind" in r_gate
                                and "retired or merged" not in r_gate) or r_gate == "SKIPPED-NO-FIXTURE")
               and r_live and ("LIVE determination" in r_live or r_live == "SKIPPED-NO-FIXTURE"),
               (r_ret, r_mer, r_gate, r_live))
        if gated:
            print(f"      open-gate probe: parameter {gated[0][0]}")
        if not spec:
            print("      SKIPPED-NO-FIXTURE: no retired specification on an active parameter with no kind (live-determination probe)")
        free_t = [t for (t,) in q("SELECT term_id FROM terms WHERE term_id NOT IN (SELECT term_id FROM base_parameters) "
                                  "AND term_id NOT IN (SELECT term_id FROM parameter_declinations) ORDER BY term_id")
                  if not db._VALUE_BEARING_NAME.search(q("SELECT canonical_en FROM terms WHERE term_id=?", t)[0][0])
                  and dbcore.domain_key(q("SELECT domain FROM terms WHERE term_id=?", t)[0][0]) not in dbcore.NON_QUANTITY_DOMAINS]
        free_p2 = [r[0] for r in q(FREE_P)]
        if not free_t or not free_p2:
            record("T083-05", "a free term and a free parameter to compare the two callers' messages", False, f"{free_t[:1]} {free_p2[:1]}")
        else:
            def tail(m):
                return m.split("): ", 1)[1] if m and "): " in m else m
            pairs = [(refusal(db.insert_parameter, free_t[0], S, dry_run=True, **kw),
                      refusal(spk, free_p2[0], kw.pop("quantity_kind", None), S, dry_run=True, **kw))
                     for kw in (dict(), dict(quantity_kind="zz_fixture"), dict(quantity_kind=kinds83[0]))]
            record("T083-05", "add-parameter and set-parameter-kind give the same kind and warrant refusals, word for word after "
                   "the term label (one home, _kind_refusal)",
                   all(a and b and tail(a) == tail(b) for a, b in pairs), pairs)
        # ── T083 repair (after the adversarial passes): the surviving branches, the CHECKs of the quantity-kind migrations ──
        free_p3 = [r[0] for r in q(FREE_P)]
        if len(free_p3) < 2:
            record("T083-06", "two more free parameters for the repair cases", False, free_p3)
        else:
            pa, pb = free_p3[:2]
            sha = lambda: __import__("hashlib").sha256(open(DB, "rb").read()).hexdigest()
            h0 = sha()
            dr = db.set_parameter_kind(pa, kinds83[0], S, dry_run=True, **W83)
            record("T083-07", "--dry-run reports the cells and writes nothing (the copy's bytes are unchanged)",
                   dr["dry_run"] is True and dr["quantity_kind"] == kinds83[0] and sha() == h0
                   and q("SELECT quantity_kind FROM base_parameters WHERE parameter_id=?", pa)[0][0] is None, dr)
            r_line = refusal(spk, pa, kinds83[0], S, **dict(W83, quantity_kind_source_line=0))
            r_blank = refusal(spk, pa, kinds83[0], S, **dict(W83, quantity_kind_source_page="\u00a0",
                                                               quantity_kind_source_clause="4.1"))
            r_host = refusal(spk, pa, kinds83[0], S, **dict(W83, quantity_kind_source_url="https:///no-host"))
            record("T083-08", "set-parameter-kind refuses a line of 0, a page holding only a no-break space beside a clause, and a URL "
                   "with no host, each naming its own flag",
                   r_line and "--quantity-kind-source-line" in r_line and r_blank and "--quantity-kind-source-page" in r_blank
                   and r_host and "--quantity-kind-source-url" in r_host, (r_line, r_blank, r_host))
            out = db.set_parameter_kind(pa, kinds83[0], S, **dict(W83, quantity_kind_source_page=None,
                                                                   quantity_kind_source_clause="TASK-FIXTURE 4.1",
                                                                   quantity_kind_source_line=7))
            got = q("SELECT quantity_kind_source_clause, quantity_kind_source_line, quantity_kind_source_page "
                    "FROM base_parameters WHERE parameter_id=?", pa)[0]
            record("T083-06", "a clause and a line are written as given (no page)",
                   got == ("TASK-FIXTURE 4.1", 7, None) and out["quantity_kind_source_line"] == 7, got)
            old = [run_cli(v, *a, "--quantity-kind", kinds83[0], "--quantity-kind-observation-id", "1", "--session", S)
                   for v, a in (("set-parameter-kind", ("--parameter-id", str(pb))), ("add-parameter", ("--term-id", "TERM-NONE")))]
            record("T083-09", "the dropped flag --quantity-kind-observation-id is refused by argparse (rc 2) on both verbs",
                   all(cp.returncode == 2 and "quantity-kind-observation-id" in cp.stderr for cp in old),
                   [(cp.returncode, cp.stderr[-160:]) for cp in old])
            # Direct UPDATEs, each rolled back, on the committed copy AND on a fresh schema replay of the parent with the
            # newest quantity-kind migration applied to it: the second reads the migration file itself, so a CHECK
            # missing from the file turns this red even when the committed database still holds it.
            mig_qk = sorted((REPO / "scripts" / "migrations").glob("[0-9][0-9][0-9]_quantity_kind_*.sql"))[-1]
            good = dict(quantity_kind=kinds83[0], **{k: v for k, v in W83.items()})
            bad = {"kind with no quote": dict(good, quantity_kind_quote=None),
                   "kind with a URL and no page or clause": dict(good, quantity_kind_source_page=None),
                   "a page holding only a no-break space": dict(good, quantity_kind_source_page="\u00a0"),
                   "U+200B in the page": dict(good, quantity_kind_source_page="3\u200b"),
                   "a clause of U+200B alone": dict(good, quantity_kind_source_clause="\u200b"),
                   "a no-break space inside the URL": dict(good, quantity_kind_source_url="https://example.org/a\u00a0b"),
                   "U+FEFF in the URL": dict(good, quantity_kind_source_url="https://example.org/\ufeff"),
                   "a BLOB page": dict(good, quantity_kind_source_page=b"3"),
                   "a line of text": dict(good, quantity_kind_source_line="seven"),
                   "a quote of spaces and U+200B": dict(good, quantity_kind_quote=" \u200b "),
                   "a ref_id with no kind": dict(quantity_kind_ref_id="TASK-FIXTURE"),
                   "a page with no kind": dict(quantity_kind_source_url="https://example.org/a", quantity_kind_source_page="3"),
                   "a page of U+00AD alone": dict(good, quantity_kind_source_page="\u00ad"),
                   "a page of U+180E alone": dict(good, quantity_kind_source_page="\u180e"),
                   "a page of U+2063 alone": dict(good, quantity_kind_source_page="\u2063"),
                   "a quote of U+3164 alone": dict(good, quantity_kind_quote="\u3164"),
                   "a BLOB kind": dict(good, quantity_kind=kinds83[0].encode()),
                   "a BLOB quote": dict(good, quantity_kind_quote=b"9 mm"),
                   "U+200B in the ref_id": dict(good, quantity_kind_ref_id="TASK\u200bFIXTURE")}

            def holes(path, pid):
                con10 = sqlite3.connect(path)
                con10.execute("PRAGMA foreign_keys=OFF")        # the BLOB kind must meet the CHECK, not the foreign key
                out = {}
                try:
                    for name, cells in [("the legitimate shape", good)] + list(bad.items()):
                        try:
                            con10.execute("UPDATE base_parameters SET " + ", ".join(f"{k}=?" for k in cells)
                                          + " WHERE parameter_id=?", list(cells.values()) + [pid])
                            out[name] = True
                        except sqlite3.IntegrityError:
                            out[name] = False
                        con10.rollback()
                finally:
                    con10.close()
                return out

            import contextlib, io
            import migrate_db
            fresh = os.path.join(TMP, "parent-replay.db")
            mine = int(mig_qk.name[:3])
            cr = sqlite3.connect(fresh, isolation_level=None)
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                for step in migrate_db.build_plan():
                    if step[0] == "schema" and step[1] <= mine:
                        stmts, uv = migrate_db._prepare_body(step[2].read_text(encoding="utf-8"))
                        migrate_db._apply_atomically(cr, stmts, label=step[2].name, fk_blocking=False,
                                                     user_version=(uv if "baseline" in step[2].name else step[1]))
            cr.execute("PRAGMA foreign_keys=OFF")
            fresh_pid = cr.execute("INSERT INTO base_parameters (term_id, status, created_at, created_by_session) "
                                   "VALUES ('TASK-FIXTURE', 'active', '2026-01-01 00:00', ?)", (S,)).lastrowid
            fresh_uv = cr.execute("PRAGMA user_version").fetchone()[0]
            cr.close()
            passed10, fresh10 = holes(DB, pb), holes(fresh, fresh_pid)
            record("T083-10", f"the quantity-kind CHECKs, on the committed copy and on a fresh replay of the parent with {mig_qk.name} "
                   "applied: the legitimate shape is accepted and each hole refused (no quote, no page or clause, wholly blank by "
                   "dbcore.blank_chars, an invisible character in the URL, page, clause or ref_id, a BLOB or text in a typed "
                   "cell, a BLOB kind, a ref_id or a locator with no kind)",
                   fresh_uv == mine and all(r.get("the legitimate shape") is True and not any(r[k] for k in bad)
                                            for r in (passed10, fresh10)),
                   {"committed": {k: v for k, v in passed10.items() if v != (k == "the legitimate shape")},
                    "fresh": {k: v for k, v in fresh10.items() if v != (k == "the legitimate shape")}, "uv": fresh_uv})
            # Pin the migration's spellings to the one definition, as T078-40 pins migration 160.
            mtext = mig_qk.read_text()
            sets = lambda frag: {chr(int(n)) for grp in re.findall(r"char\(([0-9,]+)\)", frag) for n in grp.split(",")}
            blank = set(dbcore.blank_chars()) - {"\x00"}
            hidden = set(db._kind_hidden_chars()) - {"\x00"}
            grab = lambda pat, text: (lambda m: m.group(1) if m else "")(re.search(pat, text, re.S))
            url_glob = grab(r"quantity_kind_source_url NOT GLOB '\*\[' \|\| (.*?) \|\| '\]\*'", mtext)
            cell = lambda c: grab(rf"(ADD COLUMN {c} TEXT.*?;)", mtext)
            spell = {}
            for c in ("quantity_kind_source_page", "quantity_kind_source_clause", "quantity_kind_ref_id"):
                body = cell(c)
                spell[c] = (sets(grab(rf"trim\({c}, (.*?)\) <> ''", body)),
                            sets(grab(rf"{c} NOT GLOB '\*\[' \|\| (.*?) \|\| '\]\*'", body)))
            q_trim = sets(grab(r"trim\(quantity_kind_quote, (.*?)\) <> ''", cell("quantity_kind_quote")))
            record("T083-12", f"{mig_qk.name} spells dbcore.blank_chars() (less U+0000) for the URL and every blank test, and "
                   "db._kind_hidden_chars() for what a page, clause or ref_id may not carry anywhere",
                   sets(url_glob) == blank and q_trim == blank
                   and all(t == blank and g == hidden for t, g in spell.values()), (len(blank), len(hidden)))
            # The surviving branches of the second adversarial pass: each case below is red on its own seeded defect.
            free_p4 = [r[0] for r in q(FREE_P)]
            r_zwu = refusal(spk, pb, kinds83[0], S, **dict(W83, quantity_kind_source_url="https://example.org/\u200bx"))
            r_zwr = refusal(spk, pb, kinds83[0], S, **dict(W83, quantity_kind_ref_id="TASK\u200bFIXTURE"))
            record("T083-13", "set-parameter-kind refuses an invisible character in the URL and in the ref_id, naming each flag",
                   r_zwu and "--quantity-kind-source-url" in r_zwu and "invisible" in r_zwu
                   and r_zwr and "--quantity-kind-ref-id" in r_zwr and "invisible" in r_zwr, (r_zwu, r_zwr))
            r_bq = refusal(spk, pb, kinds83[0], S, **dict(W83, quantity_kind_quote="\u3164 \u00a0"))
            record("T083-14", "a quote that is only blank characters is refused as a missing warrant (naming the flags), not as "
                   "a quote with no digit", r_bq and "needs its warrant" in r_bq and "--quantity-kind-quote" in r_bq
                   and "holds no digit" not in r_bq, r_bq)
            if len(free_p4) < 2:
                record("T083-15", "two more free parameters for the argparse cases", False, free_p4)
            else:
                pc, pd = free_p4[:2]
                cp15 = run_cli("set-parameter-kind", "--parameter-id", str(pc), "--quantity-kind", kinds83[0],
                               "--quantity-kind-quote", "\u3000TASK-FIXTURE: at least 900 mm\u00a0",
                               "--quantity-kind-source-url", W83["quantity_kind_source_url"],
                               "--quantity-kind-source-clause", "TASK-FIXTURE 4.2", "--quantity-kind-source-line", "12",
                               "--quantity-kind-ref-id", "  TASK-FIXTURE  ", "--session", S)
                got15 = q("SELECT quantity_kind_source_clause, quantity_kind_source_line, typeof(quantity_kind_source_line), "
                          "quantity_kind_ref_id, quantity_kind_quote FROM base_parameters WHERE parameter_id=?", pc)[0]
                cp15b = run_cli("set-parameter-kind", "--parameter-id", str(pd), "--quantity-kind", kinds83[0],
                                "--quantity-kind-quote", W83["quantity_kind_quote"],
                                "--quantity-kind-source-url", W83["quantity_kind_source_url"],
                                "--quantity-kind-source-page", "TASK-FIXTURE", "--quantity-kind-source-line", "twelve",
                                "--session", S)
                record("T083-15", "through argparse: the clause and the line reach the row (the line as an integer), the ref_id and "
                       "the quote are stored without their surrounding blanks; a line that is not a number is refused by "
                       "argparse (rc 2)",
                       cp15.returncode == 0 and got15 == ("TASK-FIXTURE 4.2", 12, "integer", "TASK-FIXTURE",
                                                         "TASK-FIXTURE: at least 900 mm")
                       and cp15b.returncode == 2 and "quantity-kind-source-line" in cp15b.stderr,
                       (cp15.returncode, cp15.stderr[-200:], got15, cp15b.returncode, cp15b.stderr[-120:]))

    # ── T-078: a figure retires in place (AT-18; owner 2026-09-16, "retire in place then") ──────────────────────────
    # The figure is a fixture this section builds (a fresh source, made readable on the copy, one `absent` finding in
    # one identity code), so its pair in the scan ledger holds no other figure. Every expected value is read from the
    # copy: the ledger status the pair would have with no figure is read inside a transaction that deletes the figure
    # and is rolled back.
    try:
        import assess_cell as _t078_engine                                 # noqa: E402
        con78 = sqlite3.connect(DB)
        try:
            PID78 = con78.execute("SELECT parameter_id FROM base_parameters WHERE status='active' ORDER BY 1 LIMIT 1").fetchone()[0]
        finally:
            con78.close()
        REF78 = next_ref()
        add_source(REF78, title=f"TASK-FIXTURE T078 source {REF78}")
        readable(REF78)
        P78 = {"ref_id": REF78, "parameter_id": PID78, "identity_code": POP, "claim_type": "absent", "figure_role": "finding",
               "claim_text": "TASK-FIXTURE T078: the source states nothing for this parameter",
               "lens_basis": "named_in_text", "lens_basis_text": "states nothing", "extraction_method": "skim"}
        EX78 = "TASK-FIXTURE T078: a test payload, no retrieved artefact exists"
        LENS78 = {"identity_code": POP}

        def t078_state(fig):
            """(count_extractions, the figure's live links, its pair's ledger status, the figure among the graded links)."""
            c = sqlite3.connect(DB)
            try:
                return (_t078_engine.count_extractions(c, PID78, LENS78),
                        c.execute("SELECT COUNT(*) FROM v_live_lens_links WHERE extraction_id=?", (fig,)).fetchone()[0],
                        c.execute("SELECT status FROM v_scan_ledger WHERE ref_id=? AND parameter_id=?", (REF78, PID78)).fetchone()[0],
                        fig in {l["extraction_id"] for l in _t078_engine.gather_extraction_links(c, PID78, [], LENS78)})
            finally:
                c.close()

        try:
            db.link_source_slug(REF78, plain, "TASK-FIXTURE T078: speaks to this slug", S)
            F78 = db.insert_extraction(dict(P78), S, relations=[], verbatim_exempt=EX78)["extraction_id"]
        except Exception as exc:  # noqa: BLE001 -- recorded red below
            F78 = None
            print(f"      T078 fixture failed: {exc.__class__.__name__}: {exc}")
        if F78 is not None:
            c = sqlite3.connect(DB)
            try:
                c.execute("DELETE FROM extraction_lens_links WHERE extraction_id=?", (F78,))
                c.execute("DELETE FROM source_value_extractions WHERE extraction_id=?", (F78,))
                want_status = c.execute("SELECT status FROM v_scan_ledger WHERE ref_id=? AND parameter_id=?",
                                        (REF78, PID78)).fetchone()[0]
                c.rollback()
            finally:
                c.close()
            before78 = t078_state(F78)
            dup_before = refusal(db.insert_extraction, dict(P78), S, relations=[], verbatim_exempt=EX78)
            # T078-03: a LIVE determination linking the figure blocks the retirement. A TASK-FIXTURE determination is
            # written by hand on the copy, in an identity code no live determination of the parameter holds, linking the
            # figure; it is deleted again after the refusal.
            code78 = q("SELECT identity_code FROM base_taxonomy_identity WHERE identity_code NOT IN (SELECT identity_code "
                       "FROM specifications WHERE retired_at IS NULL AND parameter_id=? AND identity_code IS NOT NULL) "
                       "ORDER BY 1 LIMIT 1", PID78)[0][0]
            c = sqlite3.connect(DB)
            try:
                sid78 = c.execute("INSERT INTO specifications (parameter_id, identity_code, state, created_at, "
                                  "created_by_session, updated_at, updated_by_session) VALUES (?, ?, 'pending', 't', ?, 't', ?)",
                                  (PID78, code78, S, S)).lastrowid
                c.execute("INSERT INTO specification_extraction_links (specification_id, extraction_id, role, exclusion_reason, "
                          "created_at, created_by_session) VALUES (?, ?, 'excluded', 'TASK-FIXTURE T078', 't', ?)", (sid78, F78, S))
                c.commit()
            finally:
                c.close()
            try:
                r_live = refusal(db.retire_extraction, F78, "TASK-FIXTURE T078", S)
                still = q("SELECT retired_at FROM source_value_extractions WHERE extraction_id=?", F78)
            finally:
                w("DELETE FROM specification_extraction_links WHERE specification_id=?", sid78)
                w("DELETE FROM specifications WHERE specification_id=?", sid78)
            record("T078-03", "retire-extraction refuses a figure a live determination links, naming the determination and "
                   "retire-specification",
                   r_live and f"live determination(s) {sid78}" in r_live and "retire-specification" in r_live
                   and still == [(None,)], (r_live, still))
            n78 = counts("source_value_extractions", "extraction_lens_links")
            cp78 = run_cli("retire-extraction", "--extraction-id", str(F78), "--reason", "TASK-FIXTURE T078: misread", "--session", S)
            row78 = q("SELECT retired_at IS NOT NULL, retired_by_session, retirement_reason FROM source_value_extractions "
                      "WHERE extraction_id=?", F78)
            record("T078-01", "retire-extraction RETIRES the figure in place: the row and its links stay, the three retired columns "
                   "are set (the verb is reached through argparse, so an absent verb is red)",
                   cp78.returncode == 0 and row78 == [(1, S, "TASK-FIXTURE T078: misread")]
                   and counts("source_value_extractions", "extraction_lens_links") == n78,
                   f"rc={cp78.returncode} err={cp78.stderr[-300:]!r} row={row78}")
            after78 = t078_state(F78)
            record("T078-04", "the readers drop the retired figure: count_extractions falls by one, v_live_lens_links lists no link "
                   "of it, gather_extraction_links grades it no more, and v_scan_ledger gives its pair the status it has with "
                   "no figure",
                   before78[0] - after78[0] == 1 and before78[1] > 0 and after78[1] == 0 and before78[3] and not after78[3]
                   and before78[2] != want_status and after78[2] == want_status,
                   f"before={before78} after={after78} want_status={want_status!r}")
            n78 = counts("source_value_extractions")
            r_blank = refusal(db.retire_extraction, F78, "  ", S)
            r_unknown = refusal(db.retire_extraction, q("SELECT COALESCE(MAX(extraction_id), 0) + 1 FROM source_value_extractions")[0][0],
                                "TASK-FIXTURE T078", S)
            r_again = refusal(db.retire_extraction, F78, "TASK-FIXTURE T078: a second, different reason", S)
            raw = {}
            for name, sql in (("un-retire", "UPDATE source_value_extractions SET retired_at=NULL, retired_by_session=NULL, "
                                            "retirement_reason=NULL WHERE extraction_id=?"),
                              ("one column alone", "UPDATE source_value_extractions SET retired_at='2026-01-01T00:00:00Z' "
                                                   "WHERE extraction_id=(SELECT MIN(extraction_id) FROM source_value_extractions "
                                                   "WHERE retired_at IS NULL AND extraction_id <> ?)"),
                              ("a blank reason", "UPDATE source_value_extractions SET retired_at='2026-01-01T00:00:00Z', "
                                                 "retired_by_session='s', retirement_reason=' ' WHERE extraction_id=(SELECT "
                                                 "MIN(extraction_id) FROM source_value_extractions WHERE retired_at IS NULL "
                                                 "AND extraction_id <> ?)")):
                try:
                    w(sql, F78)
                    raw[name] = None
                except sqlite3.DatabaseError as exc:
                    raw[name] = str(exc)
            record("T078-02", "retire-extraction refuses a blank reason, an unknown id and a figure already retired (the first reason "
                   "stands); the trigger refuses an un-retire by raw UPDATE and the CHECK or migration 159's triggers refuse one column alone and a blank reason",
                   r_blank and "--reason is required" in r_blank and r_unknown and "no such figure" in r_unknown
                   and r_again and "already retired" in r_again
                   and q("SELECT retirement_reason FROM source_value_extractions WHERE extraction_id=?", F78) == [("TASK-FIXTURE T078: misread",)]
                   and raw["un-retire"] and "stays retired" in raw["un-retire"]
                   and raw["one column alone"] and ("CHECK" in raw["one column alone"] or "is retired with" in raw["one column alone"])
                   and raw["a blank reason"] and ("CHECK" in raw["a blank reason"] or "is retired with" in raw["a blank reason"])
                   and counts("source_value_extractions") == n78,
                   (r_blank, r_unknown, r_again, raw))
            other78 = q("SELECT MIN(extraction_id) FROM source_value_extractions WHERE retired_at IS NULL AND extraction_id <> ?", F78)[0][0]
            r_amend = refusal(db.amend_extraction, F78, "extraction_status", "reviewed", "TASK-FIXTURE T078", S)
            r_from = refusal(db.relate_extraction, F78, "condition_on", S, to_extraction=other78)
            r_to = refusal(db.relate_extraction, other78, "condition_on", S, to_extraction=F78)
            record("T078-05", "amend-extraction and relate-extraction (from or to the figure) refuse a retired figure, naming "
                   "retire-extraction",
                   all(m and "retire-extraction" in m and "was retired" in m for m in (r_amend, r_from, r_to)),
                   (r_amend, r_from, r_to))
            try:
                again78 = db.insert_extraction(dict(P78), S, relations=[], verbatim_exempt=EX78)
            except Exception as exc:  # noqa: BLE001 -- recorded red below
                again78 = {"error": f"{exc.__class__.__name__}: {exc}"}
            record("T078-06", "the same reading is written again once its figure is retired (a wrong retirement is answered by a "
                   "new figure); before the retirement add-extraction refused it as a copy",
                   dup_before and "already carries this exact row" in dup_before and "extraction_id" in again78,
                   (dup_before, again78))
        else:
            record("T078-01", "retire-extraction fixture", False, "the fixture figure could not be written")
    except Exception as exc:  # noqa: BLE001 -- a crash (no verb, no column) is red, never a pass
        record("T078", "the T-078 section ran to its end", False, f"{exc.__class__.__name__}: {exc}")
    # ── T-078 repair: every reader that filters a retired figure, each on a seeded figure, and the refusals the
    # adversarial pass found missing. Fixtures are TASK-FIXTURE rows written by SQL on the copy (the readers are under
    # test, not the writers); every id, code and expected value is read from the copy.
    try:
        import assess_cell as _t78r_engine                              # noqa: E402
        WHY = "TASK-FIXTURE T078R"
        PR = q("SELECT parameter_id FROM base_parameters WHERE status='active' ORDER BY 1 LIMIT 1")[0][0]
        OUT_CODE = q("SELECT identity_code FROM base_taxonomy_identity WHERE identity_code <> ? AND identity_code NOT IN "
                     "(SELECT identity_code FROM base_taxonomy_identity WHERE parent_code = ?) ORDER BY 1 LIMIT 1", POP, POP)[0][0]

        def fresh(read=True):
            r = next_ref()
            add_source(r, title=f"{WHY} source {r}")
            if read:
                readable(r)
            return r

        def seed(ref, pid=None, code=None, **kw):
            row = dict(ref_id=ref, parameter_id=pid or PR, claim_type="numerical", claimed_value="1", claimed_unit="mm",
                       claim_text=f"{WHY} 1 mm", figure_role="claim", comparator=">=", extraction_method="full-read",
                       created_at="t", created_by_session=S, updated_at="t", updated_by_session=S)
            row.update(kw)
            c = sqlite3.connect(DB)
            try:
                x = c.execute(f"INSERT INTO source_value_extractions ({','.join(row)}) VALUES ({','.join('?' * len(row))})",
                              list(row.values())).lastrowid
                c.execute("INSERT INTO extraction_lens_links (extraction_id, identity_code, basis, created_at, "
                          "created_by_session, updated_at, updated_by_session) VALUES (?, ?, 'carried', 't', ?, 't', ?)",
                          (x, code or POP, S, S))
                c.commit()
            finally:
                c.close()
            return x

        def edge(frm, rel, to, role=None):
            w("INSERT INTO extraction_relations (from_extraction_id, relation, to_extraction_id, stated, input_role, quote, "
              "created_at, created_by_session) VALUES (?, ?, ?, 'named', ?, ?, 't', ?)", frm, rel, to, role, WHY, S)

        def retire(x):
            return db.retire_extraction(x, WHY, S)

        def ro():
            c = sqlite3.connect(DB)
            c.row_factory = None
            return c

        def sub(*cmd):
            cp = subprocess.run([sys.executable, *cmd], env=dict(os.environ, GUIDEBOOK_DB_PATH=DB), capture_output=True,
                                text=True, cwd=str(REPO))
            return cp.stdout + cp.stderr

        LENS = {"identity_code": POP}
        RA = fresh()

        # R01 gather_confirmers: a finding of one source confirms a claim of another; the claim is retired.
        RC = fresh()
        t1 = seed(RA)
        x1 = seed(RC, figure_role="finding", claim_type="qualitative", claimed_value="agrees", claimed_unit=None, comparator=None)
        edge(x1, "confirms", t1)
        c = ro(); b1 = RC in {r["ref_id"] for r in _t78r_engine.gather_confirmers(c, PR, LENS)}; c.close()
        # Set by SQL on the copy: retire-extraction refuses a figure a live figure's edge names (T078-26), so this
        # state is reached only by a row written before that refusal; the engine's filter is its floor.
        w("UPDATE source_value_extractions SET retired_at=?, retired_by_session=?, retirement_reason=? WHERE extraction_id=?",
          dbcore.now(), S, WHY, t1)
        c = ro(); a1 = RC in {r["ref_id"] for r in _t78r_engine.gather_confirmers(c, PR, LENS)}; c.close()
        record("T078-07", "gather_confirmers drops a confirmer whose confirmed figure is retired", b1 and not a1, (b1, a1))

        # R02 the out-of-lens count, and R03/R04 cell-status's extractions and slugs.
        y2 = seed(RA, code=OUT_CODE)
        c = ro(); b2 = _t78r_engine.determine(c, PR, LENS, None, None)["n_extractions_outside_lens"]; c.close()
        ex = q("SELECT se.exec_id, se.slug FROM search_executions se WHERE se.parameter_id IS NULL AND se.slug IS NOT NULL "
               "AND se.deferred_reason IS NULL AND se.slug NOT IN (SELECT slug FROM source_value_extractions WHERE "
               "parameter_id = ? AND slug IS NOT NULL AND retired_at IS NULL) ORDER BY 1 LIMIT 1", PR)
        z3 = seed(RA, slug=ex[0][1], claimed_value="3") if ex else None

        def research_execs():
            st = db.cell_status(PR)["stages"]
            return set(st["research"]["held"]) | set(st["research"]["examined_empty"]), st["judgment"]["held"]
        bx, bj = research_execs()
        retire(y2)
        if z3:
            retire(z3)
        ax, aj = research_execs()
        c = ro(); a2 = _t78r_engine.determine(c, PR, LENS, None, None)["n_extractions_outside_lens"]; c.close()
        record("T078-08", "the engine's out-of-lens count falls by the retired figure", b2 - a2 == 1, (b2, a2))
        record("T078-09", "cell-status lists a figure under judgment and drops it once retired", y2 in bj and y2 not in aj
               and z3 in bj and z3 not in aj, (y2, z3))
        record("T078-10", "cell-status reaches a search through the slug a live figure carries, and not through a retired one",
               bool(ex) and ex[0][0] in bx and ex[0][0] not in ax, ex)

        # R05 set-parameter-direction: the source's only figure of a parameter with no direction is retired.
        PD = q("SELECT parameter_id FROM base_parameters WHERE status='active' AND accessibility_direction IS NULL "
               "ORDER BY 1 LIMIT 1")[0][0]
        RD = fresh()
        d5 = seed(RD, pid=PD)
        dirv = sorted(dbcore.check_values(ro(), "base_parameters", "accessibility_direction"))[0]
        ok5 = refusal(db.set_parameter_direction, parameter_id=PD, direction=dirv, rationale=WHY, session=S, ref_id=RD,
                      dry_run=True)
        retire(d5)
        r5 = refusal(db.set_parameter_direction, parameter_id=PD, direction=dirv, rationale=WHY, session=S, ref_id=RD,
                     dry_run=True)
        record("T078-11", "set-parameter-direction accepts a source's live figure and refuses once that figure is retired",
               ok5 is None and r5 and "holds no extraction" in r5, (ok5, r5))

        # R06 add-extraction's NOTE names live prior figures only.
        RN = fresh()
        db.link_source_slug(RN, plain, f"{WHY}: speaks to this slug", S)
        n6 = seed(RN, claimed_value="6")
        retire(n6)
        import contextlib, io                                           # noqa: E401,E402
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            got6 = db.insert_extraction({"ref_id": RN, "parameter_id": PR, "identity_code": POP, "claim_type": "absent",
                                         "figure_role": "finding", "claim_text": f"{WHY}: the source states nothing here",
                                         "lens_basis": "named_in_text", "lens_basis_text": "states nothing",
                                         "extraction_method": "skim"}, S, relations=[], verbatim_exempt=WHY)
        record("T078-12", "add-extraction's NOTE does not count a retired prior figure",
               "extraction_id" in got6 and "already carries" not in buf.getvalue(), buf.getvalue()[-300:])

        # R07-R09 the audits, each on a figure it reports, counted before and after the retirement.
        def num(text, pat):
            m = re.search(pat, text)
            return int(m.group(1)) if m else None
        RU = fresh(read=False)
        u7 = seed(RU, claimed_value="7")
        RQ = fresh()
        w("UPDATE evidence_sources SET tier = 6 WHERE ref_id = ?", RQ)
        q8 = seed(RQ, claimed_value="8")
        b7 = num(sub("scripts/audit/verified_scan_integrity.py"), r"EXAMINED: (\d+)")
        b8 = num(sub("scripts/audit/research_batch_dod.py", "--all"), r"R3: (\d+)")
        b9 = num(sub("scripts/audit/adjudication_integrity.py"), r"source_value_extractions: (\d+)")
        retire(u7); retire(q8)
        a7 = num(sub("scripts/audit/verified_scan_integrity.py"), r"EXAMINED: (\d+)")
        a8 = num(sub("scripts/audit/research_batch_dod.py", "--all"), r"R3: (\d+)")
        a9 = num(sub("scripts/audit/adjudication_integrity.py"), r"source_value_extractions: (\d+)")
        record("T078-13", "verified_scan_integrity examines two figures fewer once two figures it reads are retired",
               None not in (b7, a7) and b7 - a7 == 2, (b7, a7))
        record("T078-14", "research_dod R3 counts one uncited regulatory source fewer once its only figure is retired",
               None not in (b8, a8) and b8 - a8 == 1, (b8, a8))
        record("T078-15", "adjudication_integrity counts live figures (two fewer after two retirements)",
               None not in (b9, a9) and b9 - a9 == 2, (b9, a9))

        # R10-R14 the views, on seeded rows.
        RV = fresh()
        v1 = seed(RV, root_type="measurement_primary", root_ref_id=RV, claimed_value="10")
        v2 = seed(RA, root_id=f"{WHY}-ROOT-UNREG", claimed_value="11")
        v3a = seed(RV, root_ref_id=RV, root_id=f"{WHY}-ROOT-A", claimed_value="12")
        v3b = seed(RV, root_ref_id=RV, root_id=f"{WHY}-ROOT-B", claimed_value="13")
        RS = fresh()
        b_ind = q("SELECT COALESCE(SUM(independent_root_count), 0) FROM v_value_independence WHERE parameter_id=?", PR)[0][0]
        b_unr = q("SELECT COUNT(*) FROM v_unregistered_roots WHERE extraction_id=?", v2)[0][0]
        b_con = q("SELECT COUNT(*) FROM v_root_id_conflicts WHERE conflict_key=?", RV)[0][0]
        pre_ledger = q("SELECT status FROM v_scan_ledger WHERE ref_id=? AND parameter_id=?", RS, PR)[0][0]
        s14 = seed(RS, claimed_value="14")
        b_led = q("SELECT status FROM v_scan_ledger WHERE ref_id=? AND parameter_id=?", RS, PR)[0][0]
        cov = q("SELECT sa.exec_id, sa.ref_id, UPPER(se.language), COALESCE(b.parent_code, se.jurisdiction), p.parameter_id "
                "FROM base_parameters p CROSS JOIN search_admissions sa "
                "JOIN search_executions se USING (exec_id) LEFT JOIN base_jurisdictions b ON b.jurisdiction_code = se.jurisdiction "
                "JOIN evidence_sources e ON e.ref_id = sa.ref_id AND e.superseded_by_ref_id IS NULL "
                "WHERE sa.retired_at IS NULL AND se.deferred_reason IS NULL AND EXISTS (SELECT 1 FROM v_research_scope v "
                "WHERE v.language = UPPER(se.language) AND v.jurisdiction = COALESCE(b.parent_code, se.jurisdiction)) "
                "AND p.status = 'active' AND NOT EXISTS (SELECT 1 FROM source_value_extractions x WHERE x.ref_id = sa.ref_id "
                "AND x.parameter_id = p.parameter_id AND x.retired_at IS NULL) ORDER BY 1, 5 LIMIT 1")
        CV = "SELECT sources_admitted FROM v_coverage_parameter_via_admission WHERE parameter_id=? AND language=? AND jurisdiction=?"
        b_cov = q(CV, cov[0][4], cov[0][2], cov[0][3])[0][0] if cov else None
        c15 = seed(cov[0][1], pid=cov[0][4], claimed_value="15") if cov else None
        m_cov = q(CV, cov[0][4], cov[0][2], cov[0][3])[0][0] if cov else None
        for x in (v1, v2, v3a, s14) + ((c15,) if c15 else ()):
            retire(x)
        record("T078-16", "v_value_independence counts one root fewer once its figure is retired",
               b_ind - q("SELECT COALESCE(SUM(independent_root_count), 0) FROM v_value_independence WHERE parameter_id=?", PR)[0][0] == 1,
               b_ind)
        record("T078-17", "v_unregistered_roots drops a retired figure", b_unr == 1
               and q("SELECT COUNT(*) FROM v_unregistered_roots WHERE extraction_id=?", v2)[0][0] == 0, b_unr)
        record("T078-18", "v_root_id_conflicts drops a conflict once one of its two figures is retired", b_con == 1
               and q("SELECT COUNT(*) FROM v_root_id_conflicts WHERE conflict_key=?", RV)[0][0] == 0, b_con)
        record("T078-19", "v_scan_ledger's EXTRACTED arm is earned by a live figure only: the pair returns to its reading status",
               b_led == "EXTRACTED" and q("SELECT status FROM v_scan_ledger WHERE ref_id=? AND parameter_id=?", RS, PR)[0][0]
               == pre_ledger, (pre_ledger, b_led))
        record("T078-20", "v_coverage_parameter_via_admission reaches a parameter through a live figure only",
               bool(cov) and m_cov - b_cov == 1 and q(CV, cov[0][4], cov[0][2], cov[0][3])[0][0] == b_cov, (cov, b_cov, m_cov))

        # R15 K02 and T018-05, read by test_db_integrity on the copy: a live TASK-FIXTURE determination of PR links every
        # live figure of PR; a retired figure of PR is not linked and has no live link in the view.
        code_k = q("SELECT identity_code FROM base_taxonomy_identity WHERE identity_code NOT IN (SELECT identity_code FROM "
                   "specifications WHERE retired_at IS NULL AND parameter_id=? AND identity_code IS NOT NULL) ORDER BY 1 LIMIT 1", PR)[0][0]
        c = sqlite3.connect(DB)
        try:
            sk = c.execute("INSERT INTO specifications (parameter_id, identity_code, state, rule_version, created_at, "
                           "created_by_session, updated_at, updated_by_session) VALUES (?, ?, 'pending', ?, 't', ?, 't', ?)",
                           (PR, code_k, _t78r_engine.RULE_VERSION, S, S)).lastrowid
            c.executemany("INSERT INTO specification_extraction_links (specification_id, extraction_id, role, exclusion_reason, "
                          "created_at, created_by_session) VALUES (?, ?, 'excluded', ?, 't', ?)",
                          [(sk, x, WHY, S) for (x,) in c.execute("SELECT extraction_id FROM source_value_extractions WHERE "
                                                                 "parameter_id=? AND retired_at IS NULL", (PR,)).fetchall()])
            c.commit()
        finally:
            c.close()
        integ = sub("scripts/tests/test_db_integrity.py")
        w("DELETE FROM specification_extraction_links WHERE specification_id=?", sk)
        w("DELETE FROM specifications WHERE specification_id=?", sk)
        record("T078-21", "test_db_integrity K02 accounts for live figures only (a retired figure of the parameter is not "
               "owed a link; the check names no defect of the fixture determination)",
               "K02" in integ and f"spec {sk} " not in integ and f"spec {sk}:" not in integ,
               [l for l in integ.splitlines() if f"spec {sk}" in l][:3])
        record("T078-22", "test_db_integrity T018-05 asks a live lens link of live figures only",
               "[✓] T018-05" in integ, [l for l in integ.splitlines() if "T018-05" in l][:2])

        # R16 the three retirement columns are not amendable.
        live = q("SELECT MIN(extraction_id) FROM source_value_extractions WHERE retired_at IS NULL")[0][0]
        r16 = [refusal(db.amend_extraction, live, f, "2026-11-19 00:00", WHY, S)
               for f in ("retired_at", "retired_by_session", "retirement_reason")]
        record("T078-23", "amend-extraction refuses each retirement column (set only by retire-extraction)",
               all(m and "refused" in m for m in r16) and q("SELECT retired_at FROM source_value_extractions WHERE "
                                                            "extraction_id=?", live) == [(None,)], r16)

        # The refusals the adversarial pass found missing.
        b24 = seed(RA, claimed_value="20", claim_text=f"{WHY} 20 mm", source_section=f"{WHY} 1")
        d24 = seed(RA, claimed_value="5", claim_text=f"{WHY} 5 mm", source_section=f"{WHY} 1")
        retire(d24)
        r24 = refusal(db.derive_extraction, parameter_id=PR, base=b24, delta=d24, session=S, identity=POP,
                      lens_basis="named_in_text", lens_basis_text=WHY)
        r25 = refusal(db.insert_extraction, {"ref_id": RA, "parameter_id": PR, "identity_code": POP, "claim_type": "numerical",
                                             "claimed_value": "21", "claimed_unit": "mm", "comparator": ">=",
                                             "claim_text": f"{WHY} 21 mm", "figure_role": "claim", "source_section": "1",
                                             "lens_basis": "named_in_text", "lens_basis_text": WHY,
                                             "extraction_method": "full-read"}, S,
                      relations=[{"relation": "condition_on", "to_extraction": d24, "stated": "named", "quote": WHY}],
                      verbatim_exempt=WHY)
        record("T078-24", "derive-extraction refuses a retired input, naming retire-extraction (red with the derived-input "
               "refusal alone removed: this fixture's warrant then fails first; T078-24b holds the edge writer's part)",
               r24 and "was retired" in r24 and "retire-extraction" in r24, r24)
        record("T078-25", "add-extraction refuses an edge to a retired figure (the shared edge writer)",
               r25 and "was retired" in r25, r25)
        # Every relation kind the column's CHECK declares can name a row (no CHECK of the table forbids a row for any
        # kind), so each is probed; the kinds are read, never typed.
        lean_kinds = sorted(dbcore.check_values(ro(), "extraction_relations", "relation"))
        lean, last = {}, None
        for kind in lean_kinds:
            to, frm = seed(RA, claimed_value="30"), seed(RA, claimed_value="31")
            edge(frm, kind, to, "base" if kind == "derived_from" else None)
            lean[kind] = refusal(db.retire_extraction, to, WHY, S)
            last = (to, frm)
        record("T078-26", "retire-extraction refuses a figure while any live figure holds a row edge to it, of every relation "
               "kind, naming the edge and the next act",
               len(lean_kinds) > 0 and all(m and "hold edges to" in m and f"edge " in m and "Retire each" in m
                                           for m in lean.values()), (lean_kinds, lean))
        retire(last[1])
        r39 = refusal(db.retire_extraction, last[0], WHY, S)
        record("T078-39", "once the leaning figure is retired, the figure it leaned on can be retired",
               r39 is None and q("SELECT retired_at IS NOT NULL FROM source_value_extractions WHERE extraction_id=?",
                                 last[0]) == [(1,)], r39)
        r27a = refusal(db.add_lens_link, d24, S, identity=OUT_CODE, basis="named_in_text", basis_text=WHY)
        n_live = q("SELECT COUNT(*) FROM extraction_lens_links WHERE extraction_id=? AND retired_at IS NULL", d24)[0][0]
        link_d = q("SELECT link_id FROM extraction_lens_links WHERE extraction_id=? AND retired_at IS NULL", d24)[0][0]
        r27b = refusal(db.retire_lens_link, link_d, WHY, S)
        record("T078-27", "add-lens-link refuses a retired figure, and retire-lens-link still refuses a retired figure's last "
               "live link (counted on the link table, not the view)",
               r27a and "was retired" in r27a and n_live == 1 and r27b and "last live link" in r27b, (r27a, r27b))
        reasons = sorted(dbcore.check_values(ro(), "extraction_follow_ups", "reason"))
        r28 = [refusal(db.raise_follow_up, d24, r, WHY, S) for r in reasons]
        w("INSERT INTO extraction_follow_ups (extraction_id, reason, warrant, raised_at, raised_by_session) VALUES (?, ?, ?, 't', ?)",
          d24, reasons[0], WHY, S)
        import yaml                                                     # noqa: E402
        ob = next(s_["sql"] for s_ in yaml.safe_load((REPO / "governance" / "owner-browser.yaml").read_text())["queue"]
                  if s_["id"] == "open_follow_ups")
        shown = [r[1] for r in q(ob)]
        audit = sub("scripts/audit/extraction_follow_up_audit.py")
        record("T078-28", "raise-follow-up refuses a retired figure; the owner browser's open_follow_ups and "
               "extraction_follow_up_audit do not list a follow-up on one",
               all(m and "was retired" in m for m in r28) and not any(f"extraction {d24}:" in l for l in shown)
               and not re.search(rf"\b{d24}\b.*{WHY}", audit), (r28, audit[-200:]))
        live2 = seed(RA, claimed_value="40")
        blank = [refusal(db.retire_extraction, live2, rs, S) for rs in (" ​", "\t\n", "⁠ ﻿")]
        raws = {}
        for name, sql_, args in (
                ("reason of NBSP and ZWSP", "UPDATE source_value_extractions SET retired_at=?, retired_by_session=?, "
                 "retirement_reason=? WHERE extraction_id=?", (dbcore.now(), S, " ​", live2)),
                ("session of a tab and a newline", "UPDATE source_value_extractions SET retired_at=?, retired_by_session=?, "
                 "retirement_reason=? WHERE extraction_id=?", (dbcore.now(), "\t\n", WHY, live2)),
                ("retired_at not a date", "UPDATE source_value_extractions SET retired_at=?, retired_by_session=?, "
                 "retirement_reason=? WHERE extraction_id=?", ("not a date", S, WHY, live2)),
                ("a retired row's reason rewritten", "UPDATE source_value_extractions SET retirement_reason=? "
                 "WHERE extraction_id=?", ("another reason", d24)),
                ("a retired row's session rewritten", "UPDATE source_value_extractions SET retired_by_session=? "
                 "WHERE extraction_id=?", ("another session", d24)),
                ("the legitimate shape", "UPDATE source_value_extractions SET retired_at=?, retired_by_session=?, "
                 "retirement_reason=? WHERE extraction_id=?", (dbcore.now(), S, WHY, live2))):
            try:
                w(sql_, *args)
                raws[name] = None
            except sqlite3.DatabaseError as exc:
                raws[name] = str(exc)
        record("T078-29", "a blank reason of whitespace and zero-width characters is refused by retire-extraction and by "
               "migration 159's triggers, as are a session of whitespace, a retired_at not stamped YYYY-MM-DD HH:MM and any "
               "rewrite of a retired row; the legitimate shape passes",
               all(m and "--reason is required" in m for m in blank) and raws.pop("the legitimate shape") is None
               and all(raws.values()), (blank, raws))
        mig = (REPO / "scripts" / "migrations" / "159_figure_retirement_holes.sql").read_text()
        ws154 = re.search(r"char\((32,9,[0-9,]+)\)", (REPO / "scripts" / "migrations" / "154_source_clauses_identity.sql").read_text()).group(1)
        zw = ",".join(str(ord(ch)) for ch in dbcore.ZERO_WIDTH)
        stamp_glob = re.search(r"NOT GLOB '([^']+)'", mig).group(1)
        c = ro()
        try:
            glob_ok = c.execute("SELECT ? GLOB ?, 'not a date' GLOB ?", (dbcore.now(), stamp_glob, stamp_glob)).fetchone()
        finally:
            c.close()
        record("T078-30", "migration 159 spells 154's whitespace set and dbcore.ZERO_WIDTH, and its stamp shape matches "
               "dbcore.now()", set(re.findall(r"char\(([0-9,]+)\)", mig)) == {zw, ws154} and glob_ok == (1, 0),
               (glob_ok,))
        # ── Second repair (T-078): every writer that takes a figure id refuses a retired one; the readers of connections
        # and of the translation queue drop it; amend sees live derived figures only; migration 160's shape.
        g1, g2 = seed(RA, claimed_value="50", claim_text=f"{WHY} 50 mm"), seed(RA, claimed_value="51")
        # translations: a request made while the figure was live, then the figure retired
        LANG = q("SELECT language FROM lang_jur_map ORDER BY language LIMIT 1")[0][0]
        STAGE = next(st["id"] for st in yaml.safe_load((REPO / "governance" / "pipeline-contract.yaml").read_text())["stages"]
                     if st["id"] == "judgment")
        TK = sorted(dbcore.check_values(ro(), "translations", "translator_kind"))[0]
        RK = sorted(dbcore.check_values(ro(), "translations", "reviewed_by_kind"))[0]
        t_rec = db.request_translation("source_value_extractions", "claim_text", str(g1), LANG, STAGE, session=S)["translation_id"]
        t_rev = None
        g3 = seed(RA, claimed_value="52", claim_text=f"{WHY} 52 mm")
        t_rev = db.request_translation("source_value_extractions", "claim_text", str(g3), LANG, STAGE, session=S)["translation_id"]
        db.record_translation(f"{WHY} 52", TK, "TASK-FIXTURE translator", translation_id=t_rev, session=S)
        DUE = db._translation_contract(None).translation.default_stage
        due_b = {r["translation_id"] for r in db.translations_due(DUE)} - {None}   # owed cells carry no id
        # a label edge from a live figure, to repoint onto a retired one
        lab = seed(RA, claimed_value="53")
        w("INSERT INTO extraction_relations (from_extraction_id, relation, to_label, to_kind, stated, quote, created_at, "
          "created_by_session) VALUES (?, 'tested_at', 'TASK-FIXTURE label', 'standard', 'named', ?, 't', ?)", lab, WHY, S)
        conf = sorted(dbcore.check_values(ro(), "connections", "confidence"))[0]
        cstat = "PENDING" if "PENDING" in dbcore.check_values(ro(), "connections", "status") else \
            sorted(dbcore.check_values(ro(), "connections", "status"))[0]
        cdata = lambda: {"status": cstat, "confidence": conf, "connection_type": "METHODOLOGY", "filed_in": plain,  # noqa: E731
                         "description": WHY, "source_skill": WHY, "opus_reviewed": 0}
        con_live = db.insert_connection(cdata(), [("methodology", WHY), ("extraction_id", g2)], S)
        listed_b = [c_ for c_ in db.get_connections(status=cstat) if c_["con_id"] == con_live]
        for x in (g1, g2, g3):
            retire(x)
        r31a = refusal(db.repoint_extraction_relation, lab, "tested_at", g1, S)
        r31b = refusal(db.repoint_extraction_relation, g2, "tested_at", lab, S)
        record("T078-31", "relate-extraction --repoint refuses a retired figure at either end",
               all(m and "was retired" in m for m in (r31a, r31b)), (r31a, r31b))
        r32 = refusal(db.insert_connection, cdata(), [("methodology", WHY), ("extraction_id", g1)], S)
        record("T078-32", "add-connection refuses a retired figure as a target", r32 and "was retired" in r32, r32)
        r33 = refusal(db.request_translation, "source_value_extractions", "claim_text", str(g1), LANG, STAGE, session=S)
        r34 = refusal(db.record_translation, f"{WHY} 50", TK, "TASK-FIXTURE translator", translation_id=t_rec, session=S)
        r35 = refusal(db.review_translation, t_rev, "reviewed", RK, "TASK-FIXTURE reviewer", session=S)
        record("T078-33", "request-translation refuses a retired figure", r33 and "was retired" in r33, r33)
        record("T078-34", "record-translation refuses a request whose figure was retired after the request",
               r34 and "was retired" in r34, r34)
        record("T078-35", "review-translation refuses a translation whose figure was retired", r35 and "was retired" in r35, r35)
        listed_a = [c_ for c_ in db.get_connections(status=cstat) if c_["con_id"] == con_live]
        record("T078-36", "db.py connections lists a live connection without its retired figure target",
               listed_b and f"extraction {g2}" in (listed_b[0]["targets"] or "") and listed_a
               and f"extraction {g2}" not in (listed_a[0]["targets"] or ""), (listed_b, listed_a))
        due_a = {r["translation_id"] for r in db.translations_due(DUE)} - {None}
        record("T078-37", "translations --due-at does not owe a request on a retired figure",
               t_rec in due_b and t_rec not in due_a, (t_rec, sorted(due_b)[-3:], sorted(due_a)[-3:]))
        # amend-extraction --field comparator on a base: refused while a LIVE derived figure uses it, accepted once retired
        b38, d38 = seed(RA, claimed_value="60"), seed(RA, claimed_value="61")
        k38 = seed(RA, claimed_value="121", figure_role="derived", claim_text=None)
        edge(k38, "derived_from", b38, "base")
        edge(k38, "derived_from", d38, "delta")
        newcmp = next(v for v in sorted(dbcore.check_values(ro(), "source_value_extractions", "comparator")) if v != ">=")
        r38a = refusal(db.amend_extraction, b38, "comparator", newcmp, WHY, S)
        retire(k38)
        r38b = refusal(db.amend_extraction, b38, "comparator", newcmp, WHY, S)
        record("T078-38", "amend-extraction --field comparator on a base is refused while a live derived figure uses it and "
               "accepted once that derived figure is retired",
               r38a and "is an input of derived" in r38a and f"[{k38}]" in r38a and r38b is None, (r38a, r38b))
        # migration 160: one blank set, pinned; the frozen columns derived; the holes
        mig160 = (REPO / "scripts" / "migrations" / "160_figure_retirement_shape.sql").read_text()
        trig = re.search(r"CREATE TRIGGER trg_sve_retirement_shape_insert.*?END;", mig160, re.S).group(0)
        in_glob = re.search(r"GLOB '\*\[' \|\| (.*?) \|\| '\]\*'", trig).group(1)
        spelled = {chr(int(n)) for grp in re.findall(r"char\(([0-9,]+)\)", in_glob) for n in grp.split(",")}
        in_trim = re.search(r"trim\(NEW\.retirement_reason, (.*?)\) = ''", trig).group(1)
        record("T078-40", "migration 160 spells dbcore.blank_chars() (less U+0000) in both its session and its reason test",
               spelled == set(dbcore.blank_chars()) - {"\x00"} and in_trim == in_glob, len(spelled))
        frozen = re.search(r"trg_sve_retired_row_frozen\s+BEFORE UPDATE OF (.*?) ON source_value_extractions", mig160,
                           re.S).group(1)
        want = [r[1] for r in q("PRAGMA table_info(source_value_extractions)")
                if r[1] not in ("retired_at", "retired_by_session", "retirement_reason", "updated_at", "updated_by_session")]
        record("T078-41", "the frozen-row trigger names every column of the table but the three retirement columns and the "
               "updated_* stamps (a later column fails this case until a migration adds it)",
               [x.strip() for x in frozen.split(",")] == want, (frozen[:80], len(want)))
        live3 = seed(RA, claimed_value="70")
        ret3 = seed(RA, claimed_value="71")
        retire(ret3)
        U3 = ("UPDATE source_value_extractions SET retired_at=?, retired_by_session=?, retirement_reason=? "
              "WHERE extraction_id=?")
        cases = {"retired_at 9999-99-99 99:99": (U3, ("9999-99-99 99:99", S, WHY, live3)),
                 "retired_at 2026-02-30 00:00": (U3, ("2026-02-30 00:00", S, WHY, live3)),
                 "retired_at in the future": (U3, ("2999-01-01 00:00", S, WHY, live3)),
                 "retired_at a BLOB": (U3, (b"2026-11-19 00:00", S, WHY, live3)),
                 "session not-a-session": (U3, (dbcore.now(), "not-a-session", WHY, live3)),
                 "claimed_value of a retired row": ("UPDATE source_value_extractions SET claimed_value='72' "
                                                    "WHERE extraction_id=?", (ret3,)),
                 "parameter_id of a retired row": ("UPDATE source_value_extractions SET parameter_id=parameter_id "
                                                   "WHERE extraction_id=?", (ret3,)),
                 "a retired row re-stamped": ("UPDATE source_value_extractions SET retired_at=? WHERE extraction_id=?",
                                              ("2026-01-01 00:00", ret3))}
        for ch in "᠎­⠀ㅤ‎⁣\x1f":
            cases[f"reason U+{ord(ch):04X}"] = (U3, (dbcore.now(), S, ch, live3))
        got42 = {}
        for name, (sql_, args) in cases.items():
            try:
                w(sql_, *args)
                got42[name] = None
            except sqlite3.DatabaseError as exc:
                got42[name] = str(exc)
        try:
            w("UPDATE source_value_extractions SET created_at=created_at WHERE extraction_id=?", live3)
            ok42 = True
        except sqlite3.DatabaseError:
            ok42 = False
        record("T078-42", "migration 160's triggers refuse an impossible, future or BLOB retired_at, a session that is not a "
               "stem, a reason of any blank character, a re-stamp and any change to a retired row's value columns",
               all(got42.values()) and ok42, {k: v for k, v in got42.items() if not v})
        vb = [refusal(db.retire_extraction, live3, ch, S) for ch in "᠎­⠀ㅤ‎⁣\x1f"]
        vs = refusal(db.retire_extraction, live3, WHY, "not-a-session")
        record("T078-43", "retire-extraction refuses the same blank reasons and a session that is not a stem",
               all(m and "--reason is required" in m for m in vb) and vs and "not a session stem" in vs, (vb, vs))
        cols44 = dict(ref_id=RA, parameter_id=PR, claim_type="numerical", claimed_value="73", claimed_unit="mm",
                      claim_text=WHY, figure_role="claim", comparator=">=", extraction_method="full-read", created_at="t",
                      created_by_session=S, updated_at="t", updated_by_session=S, retired_by_session=S, retirement_reason=WHY)
        born = {}
        for name, at in (("bad", "not a date"), ("good", dbcore.now())):
            c44 = dict(cols44, retired_at=at)
            try:
                w(f"INSERT INTO source_value_extractions ({','.join(c44)}) VALUES ({','.join('?' * len(c44))})", *c44.values())
                born[name] = None
            except sqlite3.DatabaseError as exc:
                born[name] = str(exc)
        record("T078-44", "a born-retired INSERT is refused when malformed and accepted when well formed (emit_batch_sql's "
               "capture of a figure added and retired in one batch)", born["bad"] and born["good"] is None, born)
        # the second filter sites of two views
        u45 = seed(RA, root_type="measurement_primary", claimed_value="74")
        k46a = seed(RA, root_ref_id=RA, root_id=f"{WHY}-SPAN", claimed_value="75")
        k46b = seed(RV, root_ref_id=RV, root_id=f"{WHY}-SPAN", claimed_value="76")
        b45 = q("SELECT COUNT(*) FROM v_unregistered_roots WHERE extraction_id=? AND defect='rootless'", u45)[0][0]
        b46 = q("SELECT COUNT(*) FROM v_root_id_conflicts WHERE conflict_key=?", f"{WHY}-SPAN")[0][0]
        retire(u45); retire(k46a)
        record("T078-45", "v_unregistered_roots' rootless arm drops a retired figure", b45 == 1 and
               q("SELECT COUNT(*) FROM v_unregistered_roots WHERE extraction_id=?", u45)[0][0] == 0, b45)
        record("T078-46", "v_root_id_conflicts' root-spans-sources arm drops a conflict once one figure is retired", b46 == 1
               and q("SELECT COUNT(*) FROM v_root_id_conflicts WHERE conflict_key=?", f"{WHY}-SPAN")[0][0] == 0, b46)
        mem = sqlite3.connect(":memory:")
        mem.execute("CREATE TABLE extraction_relations (relation TEXT CHECK (relation IN ('a','b')), to_extraction_id INT)")
        r47 = refusal(db._row_only_relations, mem)
        mem.close()
        record("T078-47", "_row_only_relations refuses when the CHECK it reads is absent, never returns nothing",
               r47 and "cannot be read" in r47, r47)
        # T078-24b: derive-extraction with a warrant that holds (a study_population), so a retired input reaches the
        # writers' refusals and not the warrant's; the live control derives.
        grade = sorted(dbcore.check_values(ro(), "evidence_population_match", "match_grade"))[0]
        w("INSERT INTO evidence_population_match (match_id, source_ref, target_population, study_population, match_grade, "
          "created_at, created_by_session) VALUES (?, ?, ?, ?, ?, 't', ?)", f"{WHY}-M", RA, POP, f"{WHY} participants", grade, S)
        # The inputs' words are figures the writer already accepted (their quotes stand in a persisted artefact, as
        # add-extraction requires of an edge's quote); read from the copy, three plain numerals in mm.
        src24 = q("SELECT claim_text, claimed_value FROM source_value_extractions WHERE retired_at IS NULL AND "
                  "figure_role='claim' AND claimed_unit='mm' AND claimed_value GLOB '[0-9]*' AND claimed_value NOT GLOB "
                  "'*[^0-9]*' AND extraction_method='full-read' AND claim_text IS NOT NULL ORDER BY extraction_id LIMIT 3")
        b24b, d24b, e24b = (seed(RA, claimed_value=v, claim_text=t_, source_section=f"{WHY} 1") for t_, v in src24)
        kw24 = dict(parameter_id=PR, session=S, identity=POP, lens_basis="study_participants", lens_basis_text=WHY)
        try:
            ok24 = db.derive_extraction(base=b24b, delta=d24b, **kw24)
        except Exception as exc:  # noqa: BLE001 -- recorded red below
            ok24 = {"error": f"{exc.__class__.__name__}: {exc}"}
        retire(e24b)
        r24b = refusal(db.derive_extraction, base=b24b, delta=e24b, **kw24)
        record("T078-24b", "derive-extraction with a holding warrant derives from live inputs and refuses a retired input "
               "(the edge writer refuses it when the derived-input refusal is removed)",
               "extraction_id" in ok24 and r24b and "was retired" in r24b, (ok24, r24b))
    except Exception as exc:  # noqa: BLE001 -- a crash is red, never a pass
        import traceback
        traceback.print_exc()
        record("T078R", "the T-078 repair section ran to its end", False, f"{exc.__class__.__name__}: {exc}")
    # ── T-144: a closed gap says when, in which session, by what kind of thing and by what it was resolved ────────────
    # (migrations 162 and 163). What reaches the guidebook without it: a gap register whose closings cannot be checked, so
    # a gap closed by mistake or for a reason since withdrawn reads as answered. Fixtures are TASK-FIXTURE gaps made with
    # add-gap on the copy; where a CHECK is under test the rows are written by hand SQL on a fresh replay of the schema
    # migrations FROM THEIR FILES (HAND), so a change to 162 or 163 reaches the case. Every probe is derived.
    try:
        mig162 = (REPO / "scripts" / "migrations" / "162_gap_resolution.sql").read_text()
        g162 = re.search(r"resolved_by_session NOT GLOB '\*\[' \|\| (.*?) \|\| '\]\*'", mig162, re.S).group(1)
        t162 = re.search(r"trim\(resolution_ref, (.*?)\) <> ''", mig162, re.S).group(1)
        sp162 = {chr(int(n)) for grp in re.findall(r"char\(([0-9,]+)\)", g162) for n in grp.split(",")}
        record("T144-01", "migration 162 spells dbcore.blank_chars() (less U+0000) in both its session and its pointer test",
               sp162 == set(dbcore.blank_chars()) - {"\x00"} and t162 == g162, len(sp162))
        cat144, pri144 = dbcore.schema_choices("gaps", "category")[0], dbcore.schema_choices("gaps", "priority")[-1]
        live_closed = sorted(v for (v,) in q("SELECT DISTINCT status FROM gaps WHERE status LIKE 'CLOSED%'"))
        closed144 = next(v for v in live_closed if db._CLOSED_STATUS_SHAPE.fullmatch(v))
        kinds144 = dbcore.check_values(sqlite3.connect(DB), "gaps", "resolution_kind")

        def gap144(label):
            r_ = run_cli("add-gap", "--category", cat144, "--priority", pri144, "--description",
                         f"TASK-FIXTURE T-144 {label}", "--session", S)
            return json.loads(r_.stdout)["gap_id"]

        def row144(g):
            return q("SELECT status, resolved_at, resolved_by_session, resolution_ref, updated_at, resolution_kind, "
                     "updated_by_session FROM gaps WHERE gap_id=?", g)[0]

        def close144(g, ref, kind="reason", sess=S, status=None):
            return refusal(db.close_gap, g, status or closed144, ref, sess, resolution_kind=kind)

        WHY144 = "TASK-FIXTURE: closed by the T-144 test"
        ga, gb, gc = gap144("a"), gap144("b"), gap144("c")
        r02 = run_cli("close-gap", "--gap-id", ga, "--status", closed144, "--resolution-kind", "reason", "--session", S)
        record("T144-02", "close-gap with no --resolution-ref is refused naming the flag and what to give, and writes nothing",
               r02.returncode != 0 and "--resolution-ref is required" in r02.stderr and "--resolution-kind" in r02.stderr
               and row144(ga)[0].startswith("OPEN"), r02.stderr[-200:])
        r03 = [close144(ga, ch) for ch in ("\u00ad", "\u3164", " \u200b ", "\u2800")]
        record("T144-03", "close-gap refuses a pointer of blank characters only (dbcore.is_blank), and writes nothing",
               all(m and "--resolution-ref is required" in m for m in r03) and row144(ga)[0].startswith("OPEN"), r03)
        r04a = close144(ga, 'references/project-standards.md :: "TASK-FIXTURE: a quote the ledger does not hold"', "ledger")
        r04b = [close144(ga, x, "ledger") for x in ("references/project-standards.md :: a quote that is nowhere",
                                                     'references/project-standards.md::"nowhere at all zzz"')]
        record("T144-04", "close-gap refuses a ledger pointer whose quote is not found once, and a malformed ledger pointer",
               r04a and "occurs 0 time(s)" in r04a and all(m and "is not a ledger pointer" in m for m in r04b)
               and row144(ga)[0].startswith("OPEN"), (r04a, r04b))
        r05 = close144(ga, WHY144, sess="not-a-session")
        record("T144-05", "close-gap refuses a session that is not a stem", r05 and "not a session stem" in r05, r05)
        absent144 = db.next_gap_id()
        r06 = close144(absent144, WHY144)
        record("T144-06", "close-gap refuses an unknown gap id (it used to UPDATE nothing and report it closed)",
               r06 and "no such gap" in r06 and not q("SELECT 1 FROM gaps WHERE gap_id=?", absent144), r06)
        r07 = run_cli("close-gap", "--gap-id", ga, "--status", closed144, "--resolution-kind", "reason",
                      "--resolution-ref", f"  {WHY144}  ", "--session", S)
        st7, at7, by7, ref7, upd7, kind7, ubs7 = row144(ga)
        out7 = json.loads(r07.stdout or "{}")
        record("T144-07", "close-gap stamps status, resolved_at (dbcore.now()'s shape), the session, the kind and the "
               "stripped pointer in one UPDATE, stamps updated_by_session, and prints what it stored",
               r07.returncode == 0 and st7 == closed144 and by7 == S and ref7 == WHY144 and kind7 == "reason"
               and ubs7 == S and at7 == upd7 and re.fullmatch(r"\d{4}-\d\d-\d\d \d\d:\d\d", at7 or "")
               and out7 == {"closed": ga, "status": st7, "resolved_at": at7, "resolved_by_session": by7,
                            "resolution_kind": kind7, "resolution_ref": ref7, "dry_run": False},
               (r07.stderr[-200:], row144(ga), out7))
        r08 = close144(ga, "TASK-FIXTURE: a second closing")
        record("T144-08", "close-gap refuses a gap already closed, naming its first resolution, which stands, and the next "
               "act (amend-gap, or a new gap)", r08 and "already" in r08 and WHY144 in r08 and "amend-gap" in r08
               and "add-gap" in r08 and row144(ga)[3] == WHY144, r08)
        w("UPDATE gaps SET status=? WHERE gap_id=?", closed144, gb)    # HAND: a closing with no resolution recorded
        r09 = close144(gb, WHY144)
        record("T144-09", "close-gap refuses a gap closed with no resolution recorded, saying so",
               r09 and "no resolution recorded" in r09 and row144(gb)[1] is None, r09)
        lq144 = next((ln[3:63] for ln in (REPO / "references" / "project-standards.md").read_text().splitlines()
                      if ln.startswith("## Owner") and len(ln) > 70 and dbcore.ledger_quote_count(ln[3:63]) == 1), None)
        r10 = close144(gc, f'references/project-standards.md :: "{lq144}"', "ledger")
        record("T144-10", "an owner ruling closes a gap: a ledger pointer whose quote is found once is accepted",
               lq144 and r10 is None and row144(gc)[3] == f'references/project-standards.md :: "{lq144}"'
               and row144(gc)[5] == "ledger", (lq144, r10))
        # migrations 162 and 163, replayed from their files onto a fresh database (HAND: the CHECKs are under test)
        import contextlib, io
        import migrate_db
        r162, r163 = os.path.join(TMP, "t144-162.db"), os.path.join(TMP, "t144-163.db")
        crp = sqlite3.connect(r162, isolation_level=None)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            steps = [st_ for st_ in migrate_db.build_plan() if st_[0] == "schema" and st_[1] <= 163]
            for step in steps:
                if step[1] == 163:
                    crp.close()
                    shutil.copy(r162, r163)
                    crp = sqlite3.connect(r163, isolation_level=None)
                stmts, uv = migrate_db._prepare_body(step[2].read_text(encoding="utf-8"))
                migrate_db._apply_atomically(crp, stmts, label=step[2].name, fk_blocking=False,
                                             user_version=(uv if "baseline" in step[2].name else step[1]))
        crp.close()
        now144 = dbcore.now()

        def check_holes(path, cases, good):
            con_ = sqlite3.connect(path)
            con_.execute("PRAGMA foreign_keys=OFF")
            con_.execute("INSERT INTO gaps (gap_id, category, priority, status, description, created_at, created_by_session, "
                         "updated_at, updated_by_session) VALUES ('TASK-FIXTURE-G', ?, ?, 'OPEN', 'TASK-FIXTURE', ?, ?, ?, ?)",
                         (cat144, pri144, now144, S, now144, S))
            con_.commit()
            out = {}
            for name, cells in [("the legitimate shape", good)] + list(cases.items()):
                try:
                    con_.execute("UPDATE gaps SET " + ", ".join(f"{k}=?" for k in cells) + " WHERE gap_id='TASK-FIXTURE-G'",
                                 list(cells.values()))
                    out[name] = True
                except sqlite3.IntegrityError:
                    out[name] = False
                con_.rollback()
            con_.close()
            return out

        def cl(at=now144, by=S, ref=WHY144, status=closed144, **k):
            return dict(status=status, resolved_at=at, resolved_by_session=by, resolution_ref=ref, **k)

        bad162 = {"an OPEN gap carrying all three": cl(status="OPEN"),
                  "stamp and session, no pointer": cl(ref=None), "the stamp alone": cl(by=None, ref=None),
                  "the session alone": cl(at=None, ref=None), "the pointer alone": cl(at=None, by=None),
                  "session and pointer, no stamp": cl(at=None), "stamp and pointer, no session": cl(by=None),
                  "resolved_at 2026-02-30 00:00": cl(at="2026-02-30 00:00"),
                  "resolved_at 9999-99-99 99:99": cl(at="9999-99-99 99:99"),
                  "resolved_at with seconds": cl(at=now144 + ":00"),
                  "resolved_at before the gap was created": cl(at="1900-01-01 00:00"),
                  "resolved_at a BLOB": cl(at=now144.encode()),
                  "session not-a-session": cl(by="not-a-session"), "session with .md": cl(by=S + ".md"),
                  "session with a space": cl(by="session_a b"), "session_ and no name": cl(by="session_"),
                  "session a BLOB": cl(by=S.encode()), "pointer a BLOB": cl(ref=WHY144.encode())}
        for ch in "\u180e\u00ad\u2800\u3164\u200e\u2063\x1f ":
            bad162[f"pointer U+{ord(ch):04X}"] = cl(ref=ch * 2)
        h162 = check_holes(r162, bad162, cl())
        bad163 = {k: dict(v, resolution_kind="reason") for k, v in bad162.items()}
        bad163.update({"a kind outside the CHECK": cl(resolution_kind="TASK-FIXTURE-KIND"),
                       "the kind alone": dict(resolution_kind="reason"), "all three, no kind": cl(),
                       "resolved_at 24:00": cl(at=now144[:11] + "24:00", resolution_kind="reason"),
                       "resolved_at minute 60": cl(at=now144[:14] + "60", resolution_kind="reason")})
        h163 = check_holes(r163, bad163, cl(resolution_kind="reason"))
        record("T144-11", "on a fresh replay of the migration files, 162's CHECK and then 163's refuse provenance on an "
               "OPEN gap, every partial set, an impossible, early, seconds-bearing, hour-24 or BLOB stamp, a session that "
               "is not a stem or is a BLOB, a blank or BLOB pointer and a kind outside the CHECK; each accepts a well formed "
               "closing", all(h["the legitimate shape"] is True and not any(v for k, v in h.items()
                                                                           if k != "the legitimate shape")
                              for h in (h162, h163)),
               {"162": [k for k, v in h162.items() if v != (k == "the legitimate shape")],
                "163": [k for k, v in h163.items() if v != (k == "the legitimate shape")]})
        a12 = subprocess.run([sys.executable, str(REPO / "scripts" / "audit" / "gap_mining_audit.py")],
                             env=dict(os.environ, GUIDEBOOK_DB_PATH=DB), capture_output=True, text=True).stdout
        l12 = next((ln for ln in a12.splitlines() if "CHECK 8:" in ln), "")
        go12 = gap144("open, for the audit")
        want12 = q("SELECT COUNT(*) FROM gaps WHERE status LIKE 'CLOSED%' AND resolved_at IS NULL")[0][0]
        n12 = re.search(r"CHECK 8: (\d+) ", l12)
        record("T144-12", "gap_mining_audit lists, as informational, a closed gap with no resolution, not one with it nor an "
               "open gap, and its count is the query's and the number of ids it lists",
               re.search(rf"\b{gb}\b", l12) and not re.search(rf"\b{ga}\b", l12) and not re.search(rf"\b{go12}\b", l12)
               and n12 and int(n12.group(1)) == want12 == len(l12.split(":", 2)[-1].split(","))
               and "no resolution recorded" in l12, l12[:200])
        # the capture path: a closing on a scratch copy reaches emit_batch_sql as one UPDATE carrying the four cells
        c0, c1 = os.path.join(TMP, "t144-c0.db"), os.path.join(TMP, "t144-c1.db")
        shutil.copy(REPO / "data" / "guidebook.db", c0)
        shutil.copy(c0, c1)
        g13 = sqlite3.connect(c0).execute("SELECT gap_id FROM gaps WHERE status LIKE 'OPEN%' ORDER BY gap_id").fetchone()[0]
        subprocess.run([sys.executable, str(REPO / "scripts" / "db.py"), "close-gap", "--gap-id", g13, "--status",
                        closed144, "--resolution-kind", "reason", "--resolution-ref", WHY144, "--session", S],
                       env=dict(os.environ, GUIDEBOOK_DB_PATH=c1), capture_output=True, text=True)
        out13 = os.path.join(TMP, "t144.sql")
        e13 = subprocess.run([sys.executable, str(REPO / "scripts" / "research" / "emit_batch_sql.py"), "--scratch", c1,
                              "--out", out13], env=dict(os.environ, GUIDEBOOK_DB_PATH=c0), capture_output=True, text=True)
        sql13 = [ln for ln in (pathlib.Path(out13).read_text() if os.path.exists(out13) else "").splitlines()
                 if ln.startswith("UPDATE")]
        record("T144-13", "emit_batch_sql captures a closing as one UPDATE carrying status and the four resolution cells",
               e13.returncode == 0 and len(sql13) == 1 and all(f'"{c_}"' in sql13[0] for c_ in
                                                                ("status", "resolved_at", "resolved_by_session",
                                                                 "resolution_kind", "resolution_ref")) and g13 in sql13[0],
               (e13.stderr[-200:], sql13))
        # each kind, checked by what it is
        head144 = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        absent_sha = next(x for x in (head144[::-1], head144[1:] + head144[0], "0" * 40)
                          if subprocess.run(["git", "-C", str(REPO), "cat-file", "-e", f"{x}^{{commit}}"],
                                            capture_output=True).returncode != 0)
        gd, ge, gf, gg = gap144("d"), gap144("e"), gap144("f"), gap144("g")
        r14 = [close144(gd, absent_sha, "commit"), close144(gd, "not-a-sha", "commit")]
        r14ok = close144(gd, head144, "commit")
        record("T144-14", "a commit closes a gap only when it exists in this repository and is shaped as a sha",
               r14[0] and "is not a commit in this repository" in r14[0] and r14[1] and "is not a commit sha" in r14[1]
               and r14ok is None and row144(gd)[3] == head144 and row144(gd)[5] == "commit", (r14, r14ok))
        nogit = tempfile.mkdtemp(prefix="t144-nogit-", dir=TMP)
        r15 = subprocess.run([sys.executable, str(REPO / "scripts" / "db.py"), "close-gap", "--gap-id", ge, "--status",
                              closed144, "--resolution-kind", "commit", "--resolution-ref", head144, "--session", S],
                             env=dict(os.environ, GUIDEBOOK_DB_PATH=DB, PATH=nogit), capture_output=True, text=True)
        record("T144-15", "with no git on the PATH a commit cannot be proved: refused, naming the next act, nothing written",
               r15.returncode != 0 and "git is not available" in r15.stderr and "--resolution-kind task" in r15.stderr
               and row144(ge)[0].startswith("OPEN"), r15.stderr[-250:])
        tdir = REPO / "workplan" / "2026-11-12-bidirectional-pipeline" / "tasks"
        held_t = sorted({m_.group(0) for f_ in tdir.glob("T-[0-9][0-9][0-9]-*.md") if (m_ := re.match(r"T-\d{3}", f_.name))})
        absent_t = next(f"T-{n:03d}" for n in range(1, 1000) if f"T-{n:03d}" not in held_t)
        r16 = [close144(ge, absent_t, "task"), close144(ge, "T-1", "task")]
        r16ok = close144(ge, held_t[0], "task")
        record("T144-16", "a closing from a session with no commit names its task: a task id with no file and a malformed "
               "one are refused, one with its file is accepted",
               r16[0] and "has no task file" in r16[0] and r16[1] and "is not a task id" in r16[1] and r16ok is None
               and row144(ge)[3] == held_t[0], (absent_t, r16, r16ok))
        r17 = [close144(gf, gf, "duplicate"), close144(gf, db.next_gap_id(), "duplicate")]
        r17ok = close144(gf, gg, "duplicate")
        record("T144-17", "a duplicate names another gap that exists: itself and an absent gap are refused, another is "
               "accepted", r17[0] and "not its own duplicate" in r17[0] and r17[1] and "is not a gap" in r17[1]
               and r17ok is None and row144(gf)[3] == gg, (r17, r17ok))
        r18 = [close144(gg, x) for x in (head144[:12], held_t[0], gb, "scripts/migrations/data_9999_none.sql",
                                         f'references/project-standards.md :: "{lq144}"')]
        record("T144-18", "a reason is words: a sha, a task id, a gap id, a data migration path or a ledger pointer given as "
               "a reason is refused, naming the kind to use", all(r18) and all("--resolution-kind" in m for m in r18)
               and row144(gg)[0].startswith("OPEN"), r18)
        r19 = [close144(gg, WHY144, status=s_) for s_ in ("CLOSED", "CLOSED-", "CLOSED-fixed", closed144 + "\u200b",
                                                         "CLOSED and then some junk", "CLOSED-\u00c9T\u00c9", "OPEN")]
        record("T144-19", "the status tail is refused when blank, invisible, not capital ASCII letters or not of the shape; "
               "every closing status in use has the shape", all(m and "is not a closing status" in m for m in r19)
               and all(db._CLOSED_STATUS_SHAPE.fullmatch(v) for v in live_closed), (r19, live_closed))
        r20 = close144(gg, WHY144, kind="TASK-FIXTURE-KIND")
        h20 = run_cli("close-gap", "--help").stdout
        record("T144-20", "a kind outside the CHECK is refused naming the kinds, and --help offers exactly the CHECK's kinds",
               r20 and all(k_ in r20 for k_ in kinds144) and kinds144
               and set(dbcore.schema_choices("gaps", "resolution_kind") or ()) == kinds144
               and all(k_ in h20 for k_ in kinds144), (r20, kinds144))
        # two closers interleaved: the second cannot write while the first holds its transaction, and a stale read
        # cannot overwrite a closing (the guarded UPDATE)
        real_connect = db.connect

        class _Px:
            def __init__(self, c, hook):
                self.c, self.hook = c, hook

            def execute(self, sql, *a):
                if sql.startswith("SELECT status, resolved_at"):
                    r_ = self.hook(self.c, a)
                    if r_ is not None:
                        return r_
                return self.c.execute(sql, *a)

            def __getattr__(self, n):
                return getattr(self.c, n)

        def proxied(hook):
            @contextlib.contextmanager
            def _c(*a, **k):
                with real_connect(*a, **k) as c_:
                    yield _Px(c_, hook)
            return _c

        other = {}
        U21 = ("UPDATE gaps SET status=?, resolved_at=?, resolved_by_session=?, resolution_kind='reason', "
               "resolution_ref=? WHERE gap_id=?")

        def interfere(c_, a):
            try:
                o_ = sqlite3.connect(DB, timeout=0)
                o_.execute(U21, (closed144, dbcore.now(), S, "TASK-FIXTURE: the other closer", a[0][0]))
                o_.commit()
                o_.close()
                other["r"] = "written"
            except sqlite3.OperationalError as exc:
                other["r"] = str(exc)

        class _Stale:
            def fetchone(self):
                return {"status": "OPEN", "resolved_at": None, "resolution_kind": None, "resolution_ref": None, "open": 1}

        def stale(c_, a):
            c_.execute(U21, (closed144, dbcore.now(), S, "TASK-FIXTURE: the other closer", a[0][0]))
            return _Stale()

        gh, gi = gap144("h"), gap144("i")
        try:
            db.connect = proxied(interfere)
            r21 = close144(gh, WHY144)
            db.connect = proxied(stale)
            r22 = close144(gi, WHY144)
        finally:
            db.connect = real_connect
        record("T144-21", "a second closer cannot write while the first holds its transaction; the first closing stands",
               r21 is None and "locked" in other.get("r", "") and row144(gh)[3] == WHY144, (r21, other, row144(gh)))
        record("T144-22", "a closing read as open but closed before its UPDATE is refused by the guarded UPDATE, and nothing "
               "is written", r22 and "closed by another writer" in r22 and row144(gi)[0].startswith("OPEN"), (r22, row144(gi)))
        g23 = run_cli("gaps", "--closed").stdout
        o23 = run_cli("gaps").stdout
        rows23 = {r_["gap_id"]: r_ for r_ in json.loads(g23 or "[]")}
        record("T144-23", "db.py gaps --closed lists closed gaps with the four resolution cells and no open gap; db.py gaps "
               "still lists only the open ones", ga in rows23 and rows23[ga]["resolution_ref"] == WHY144
               and rows23[ga]["resolved_by_session"] == S and rows23[ga]["resolution_kind"] == "reason"
               and gb in rows23 and go12 not in rows23 and ga not in {r_["gap_id"] for r_ in json.loads(o23 or "[]")},
               (sorted(rows23)[:5], len(rows23)))
    except Exception as exc:  # noqa: BLE001 -- a crash is red, never a pass
        import traceback
        traceback.print_exc()
        record("T144R", "the T-144 section ran to its end", False, f"{exc.__class__.__name__}: {exc}")
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 70)
print(f"EXAMINED: {len(results)} assertion(s)")
print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
if sum(results) < len(results):
    print(f"FAILED: {len(results) - sum(results)}")
print("=" * 70)
sys.exit(0 if results and all(results) else 1)
