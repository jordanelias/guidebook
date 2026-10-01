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

Runs on a COPY of the canonical database in a temp directory (dbcore refuses to open the
canonical file read-write). Fixtures are made through db.py's own writers. Two states no
writer can make are set by SQL on the copy, and each says why at the point it is set.
Nothing depends on a hard-coded live id: the slugs, source, population and term used are
read from the copy.
"""
import os
import pathlib
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
import db        # noqa: E402
import dbcore    # noqa: E402
from dbcore import Refusal  # noqa: E402

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


def exec_row(exec_id):
    return q("SELECT results_admitted, findings_note FROM search_executions "
             "WHERE exec_id=?", exec_id)[0]


try:
    (A,), (B,) = q("SELECT slug FROM slugs WHERE status='ACTIVE' ORDER BY slug LIMIT 2")
    merged = q("SELECT slug FROM slugs WHERE status='MERGED' ORDER BY slug LIMIT 1")
    MERGED = merged[0][0] if merged else None
    (REF,), (REF2,) = q("SELECT ref_id FROM evidence_sources ORDER BY ref_id LIMIT 2")
    (POP,) = q("SELECT population_code FROM populations ORDER BY population_code LIMIT 1")[0]
    (TERM, DEF) = q("SELECT term_id, definition FROM terms ORDER BY term_id LIMIT 1")[0]

    def search(label):
        return db.log_search(slug=A, language="EN", query_text=f"fixture: {label}",
                             engine="manual", depth_method="scoping", session=S,
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
    out = db.unlink_admission(E1, REF, "fixture: the edge was wrong", S)
    n, note = exec_row(E1)
    record("U03", "removes the edge, lowers the count by one, keeps the edge in the note, "
           "and names the candidate still pointing here",
           not q("SELECT 1 FROM search_admissions WHERE exec_id=? AND ref_id=?", E1, REF)
           and n == 0 and "ADMISSION UNLINKED" in note and REF in note
           and out["candidates_still_naming_this_search"] == [C1], f"out={out} n={n}")
    record("U04", "the edge can be linked again after an unlink (the fix is reversible)",
           db.link_admission(E1, REF, "relinked", S)["edge_added"] is True)

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
        def fixture_term(name):
            obs = db.observe_term({"ref_id": REF, "surface_form": f"fixture phrase: {name}"},
                                  S)
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
        pid = db.insert_parameter(TP, S)["parameter_id"]
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
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 70)
print(f"EXAMINED: {len(results)} assertion(s)")
print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
if sum(results) < len(results):
    print(f"FAILED: {len(results) - sum(results)}")
print("=" * 70)
sys.exit(0 if results and all(results) else 1)
