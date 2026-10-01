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
determination blocks the move until it is retired, and that the UPDATE reaches the capture
path.

Section C (GAP-055) holds `close-adversarial-pass`'s artefact parse: a SURVIVED artefact
written as a citation ("<file> page 15", "<file> (and the other 11)") used to make a
good-faith pass unclosable, so its audit stayed red for a pass that had done its work. A
path that escapes the repo must still refuse, and cited paths that do not resolve must stay
visible.

Section E (I1) holds `amend-source --field evidence_type`: without it a source filed at the
wrong rung of the ladder (a Co-1/T6 contradiction, a grey report typed as a trial) keeps
anchoring at the wrong strength, because the only correction was hand SQL. It proves the
tier moves with the type by derivation only, that a move to co1 needs the D-0178 warrant,
that a move off co1 keeps the old warrant in the ledger and NULLs the Co-1-only columns, and
that a source a live determination rests on cannot move.

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
                       *extra)

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
        record("X08", "D04 goes quiet after the verb, and A09 (the pointer resolves) holds "
               "with the tombstone in scope",
               "[✓]" in d04 and "[✓]" in a09 and "NOTHING IN SCOPE" not in a09,
               f"{d04} | {a09}")
        msg = refusal(supersede, XA, XB, WHY, S)
        record("X09", "refuses a source already superseded, naming its target",
               msg and XB in msg, f"got {msg!r}")
        XC = next_ref()
        add_source(XC)
        msg = refusal(supersede, XC, XA, WHY, S)
        record("X10", "refuses a --by that is itself superseded (no chains), naming where "
               "it points", msg and XB in msg and superseded_by(XC) is None, f"got {msg!r}")
        out = supersede(XB, XC, WHY, S, dry_run=True)
        deps = {(d["table"], d["column"]): d["rows"] for d in out["dependents_left_in_place"]}
        record("X10b", "a row already superseded BY the source is reported as a dependent "
               "(the pointer has no FK, so it is added by name), not refused",
               deps.get(("evidence_sources", "superseded_by_ref_id")) == 1
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
            con.execute("UPDATE specifications SET retired_at=NULL WHERE specification_id=?",
                        (SPEC,))
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
                    VALID_SCOPES_BY_TYPE[etype])))]), "--session", S, *extra]
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
                "dpo_research")
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
               and PROV in seg and "dpo_research" in seg,
               f"msg={msg!r} out={out} seg={seg!r}")
        out, msg = attempt(db.amend_source, EC, "evidence_type", "co1",
                           "fixture: the preface names the DPO after all", session=S,
                           co1_provenance=PROV, tier=TIER_MAP[("co1", "intrinsic")])
        row = source_row(EC)
        record("E09", "a move TO co1 with the warrant (and an agreeing --tier) writes the "
               "warrant, the derived scope and tier",
               out and out["changed"] and row["evidence_type"] == "co1"
               and row["co1_provenance"] == PROV
               and row["tier"] == TIER_MAP[("co1", "intrinsic")],
               f"msg={msg!r} out={out}")

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
            con.execute("UPDATE specifications SET retired_at=NULL WHERE specification_id=?",
                        (SPEC,))
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
            con = sqlite3.connect(DB)
            con.execute("UPDATE specifications SET retired_at=?, retired_by_session=?, "
                        "retirement_reason=? WHERE specification_id=?",
                        (R_AT, R_BY, R_WHY, SPEC))
            con.commit()
            con.close()

        ok = run_cli("amend-source", "--ref-id", EA, "--field", "evidence_type",
                     "--replacement", "co1", "--co1-provenance", PROV, "--reason", WHY,
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
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 70)
print(f"EXAMINED: {len(results)} assertion(s)")
print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
if sum(results) < len(results):
    print(f"FAILED: {len(results) - sum(results)}")
print("=" * 70)
sys.exit(0 if results and all(results) else 1)
