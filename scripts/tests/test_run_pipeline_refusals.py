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
reason is an obstacle the ledger classes (R2-3; a reading no longer clears it, R3-1), a
damaged byline behind a malformed deposit is still a cross (R2-4), `full` is checked
against what the scan can count (R2-5; the deposit inference was removed, R3-3), the
exemption is refused where a body is held, for observe-term too (R2-6), a slug must exist
(R2-7), a reference id is computed (R2-9), a connection type has an arity row (R2-10), a
flag that says "live vocabulary" prints it (R2-11), a comparator word is refused in a NAME
only (R2-12), the verified-scan reader examines every live extraction (R2-15) and the
skill-vocabulary audit can go red (R2-16).

Round 3 (same day) lands the third review's repairs, each with the real shape the reviewers found as
well as a synthetic one: a block and a reading are two facts and the ledger (migration 124) says which
holds (R3-1); a decodable body includes a PDF with a text layer and the exemption needs a persisted page
render (R3-2); `full` over a page-less text lands as the operator's claim, marked `uncounted` (R3-3); the
id of a promotion is derived from the document's identity (R3-4); a repeated author is one author (R3-7);
the ledger's header names every block reason (R3-8); the vocabulary audit takes files and cannot pass on
nothing (R3-9); a flag's vocabulary is read from its column (R3-12); a conflict names the flag it refuses
and never takes the scope marker (R3-14); a `.md` session and a foreign `--stamp` do not reach a row
(R3-15, R3-16); `coverage` reports the slug's status (R3-17).

TEST-DESIGN RULE (R3-10). A fixture selector never raises. When the live corpus no longer offers the state
a case needs (every source VERIFIED, scan debt at zero, every parameter given a direction), the selector
builds it by hand on the scratch copy (marked HAND) or the case prints SKIPPED-NO-FIXTURE with the reason:
counted apart from EXAMINED, never silent. A case that depends on a round-2 or round-3 feature is gated by
a probe (`hasattr`, a `sqlite_master` read, a `--help` read, a result key) and goes red BY NAME when the
feature is absent, so an older tree fails case by case and does not crash. The writer's judgement about
which block reasons restate a typed fact has one home, `db._BLOCK_REASON_COPIES`, and is read, not restated.

Nothing here types a count, an id or a code the database can derive; a state the CLI cannot build is made
by SQL on a second copy and marked HAND. A legitimate change to the data (a first real connection, a scope
fill, a new identity code, a source becoming VERIFIED, a parameter given a direction) moves a derived
number, never a relation asserted. Each case shows the refusal fires AND the legitimate shape still passes.

Runs on a COPY of the canonical database (dbcore refuses the canonical file read-write) against a scratch
retrieval-log root of symlinks to the tracked sessions plus the fixtures written here; each scratch copy
of the database gets its own root, because a source minted on a copy takes an id the main copy will mint
too. What an audit's own `--selftest` asserts (research_batch_dod's BLOCKED fixtures) is not repeated.
"""
import contextlib
import functools
import hashlib
import io
import itertools
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
os.chdir(REPO)
TMP = tempfile.mkdtemp(prefix="run-pipeline-refusals-")
DB = os.path.join(TMP, "guidebook.db")
shutil.copy(REPO / "data" / "guidebook.db", DB)


def farm(name):
    """A scratch retrieval-log root of symlinks to the tracked sessions: fixtures written to it leave the
    tracked log (and every other root) as it was."""
    path = os.path.join(TMP, name)
    if not os.path.isdir(path):
        os.makedirs(path)
        for d in (REPO / "retrieval-log").iterdir():
            if d.is_dir():
                os.symlink(d.resolve(), os.path.join(path, d.name))
    return path


FARM = farm("retrieval-log")
os.environ["GUIDEBOOK_DB_PATH"] = DB
os.environ["GUIDEBOOK_RETRIEVAL_LOG"] = FARM
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "scripts" / "research"))
import db        # noqa: E402
import dbcore    # noqa: E402
import retrieval_log  # noqa: E402
from dbcore import Refusal  # noqa: E402
try:
    import pymupdf  # noqa: E402
except Exception:   # noqa: BLE001
    pymupdf = None

S = "session_test-run-pipeline-refusals"
results, skipped = [], []
_scratches = itertools.count()


def record(tid, name, passed, details=""):
    results.append(bool(passed))
    print(f"  [{'✓' if passed else '✗'}] {tid}: {name}")
    if details and not passed:
        print(f"      {str(details)[:400]}")


def skip(tid, why):
    """A case that cannot run for want of a fixture: printed, counted apart, never silent."""
    skipped.append(tid)
    print(f"  [-] {tid}: SKIPPED-NO-FIXTURE: {why}")
    return False


def feature(tid, name, present, what):
    """Gate a round-2/3 case on a probe: absent, the case is red and names the feature."""
    if not present:
        record(tid, name, False, f"feature absent: {what}")
    return bool(present)


def finish(why=None):
    if why:
        skip("registry", f"{why}: the sections below it need it")
    con.close()
    n = len(results)
    if all(results):
        shutil.rmtree(TMP, ignore_errors=True)      # a dozen database copies; kept when a case failed, to look at
    else:
        print(f"\n(scratch kept: {TMP})")
    print(f"\nEXAMINED: {n} cases")
    print(f"SKIPPED-NO-FIXTURE: {len(skipped)}")
    print(f"FAILED: {results.count(False)}" if not all(results) else f"PASS: all {n} cases")
    sys.exit(0 if all(results) and n else 1)


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


def scalar(sql, *p):
    r = q(sql, *p)
    return r[0][0] if r else None


def sql_of(name):
    return scalar("SELECT sql FROM sqlite_master WHERE name=?", name)


@contextlib.contextmanager
def scratch():
    """A second copy of the test database for a case that needs hand-built state (each such
    statement says HAND), with its own copy of the scratch retrieval log: a source minted on the copy
    takes an id the main copy will mint too, and the two must not hold each other's files. db.py follows
    GUIDEBOOK_DB_PATH and GUIDEBOOK_RETRIEVAL_LOG at call time, so its writers act on the copies."""
    k = next(_scratches)
    path = os.path.join(TMP, f"scratch-{k}.db")
    shutil.copy(DB, path)
    root = os.path.join(TMP, f"scratch-log-{k}")
    os.makedirs(root)
    for e in pathlib.Path(retrieval_log.LOG_ROOT).iterdir():
        if e.is_symlink():
            os.symlink(os.readlink(e), os.path.join(root, e.name))
        elif e.is_dir():
            shutil.copytree(e, os.path.join(root, e.name))
    old_root = retrieval_log.LOG_ROOT
    os.environ["GUIDEBOOK_DB_PATH"], os.environ["GUIDEBOOK_RETRIEVAL_LOG"] = path, root
    retrieval_log.DB_PATH, retrieval_log.LOG_ROOT = pathlib.Path(path), pathlib.Path(root)
    retrieval_log._ARTEFACT_INDEX.clear()
    c = sqlite3.connect(path)
    c.row_factory = sqlite3.Row
    try:
        yield c
    finally:
        c.close()
        os.environ["GUIDEBOOK_DB_PATH"], os.environ["GUIDEBOOK_RETRIEVAL_LOG"] = DB, str(old_root)
        retrieval_log.DB_PATH, retrieval_log.LOG_ROOT = pathlib.Path(DB), old_root
        retrieval_log._ARTEFACT_INDEX.clear()


def hand(sql, *p):
    """HAND: SQL on the current copy, for a state no writer builds."""
    c = sqlite3.connect(os.environ["GUIDEBOOK_DB_PATH"])
    c.execute(sql, p)
    c.commit()
    c.close()


@contextlib.contextmanager
def log_root(path):
    """Point the retrieval log at another root for one block."""
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


def put(ref, artefact, body, session="session_fixture", **extra):
    """Hold `body` for `ref` in the current scratch log root under a manifest line of the shape fetch() writes
    (`extra` adds derived/derivation_kind/content_type). Returns the sha256."""
    d = pathlib.Path(retrieval_log.LOG_ROOT) / session
    d.mkdir(exist_ok=True)
    (d / artefact).write_bytes(body)
    sha = hashlib.sha256(body).hexdigest()
    with open(d / "manifest.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"retrieved_at": "2026-11-06T00:00:00+00:00", "ref_id": ref,
                             "url": f"https://example.invalid/{artefact}", "sha256": sha,
                             "bytes": len(body), "exit": 0, "status": 200, "artefact": artefact,
                             "content_type": None, **extra}) + "\n")
    retrieval_log._ARTEFACT_INDEX.clear()
    return sha


def held_text(ref, text, payload=None):
    """Persist for `ref` a derived text (`-text.txt`, the shape the old suffix test missed) and,
    when `payload` is given, a Crossref-shaped bibliographic payload. Returns the text's sha256."""
    d = pathlib.Path(retrieval_log.LOG_ROOT) / "session_fixture"
    d.mkdir(exist_ok=True)
    if payload is not None:
        put(ref, f"{ref}-payload.json", json.dumps({"message": {"DOI": f"10.0000/{ref}", **payload}}).encode(),
            content_type="application/json")
    txt = d / f"{ref}-text.txt"
    txt.write_text(text)
    retrieval_log.record_file(txt, "session_fixture", f"{ref}-payload.json", purpose="fixture text",
                              ref_id=ref, kind="text-extraction")
    retrieval_log._ARTEFACT_INDEX.clear()
    return hashlib.sha256(txt.read_bytes()).hexdigest()


def scan(ref, sha, scope):
    return {"ref_id": ref, "mode": "catalogue", "text_scope": scope, "file_sha256": sha,
            "method": "full-read"}


AUTH = db.parse_author_flags(["corp|Fixture Body"])
SRC = {"year": 2020, "evidence_type": "code", "scope": "intrinsic", "verification_status": "UNVERIFIED"}
_titles = iter(range(1, 10 ** 6))


def new_source(verified=False, **over):
    """A fixture source through the writer, titled so that no staged lead matches it (R3-4)."""
    authors = over.pop("authors", None) or AUTH
    row = {**SRC, "title": f"Fixture source number {next(_titles)} on handrail finials", **over}
    ref = db.insert_evidence_source(row, S, dry_run=False, authors=authors)
    if verified:
        hand("UPDATE evidence_sources SET verification_status='VERIFIED' WHERE ref_id=?", ref)
    return ref


def ledger(c, ref):
    return c.execute("SELECT parameter_id, status, scan_id, text_scope FROM v_scan_ledger WHERE ref_id=? "
                     "ORDER BY parameter_id", (ref,)).fetchall()


def hand_scan(c, ref, scope):
    """HAND: one catalogue reading of `scope`, as the writer would leave it (no file behind it)."""
    top = c.execute("SELECT MAX(parameter_id) FROM base_parameters").fetchone()[0]
    cur = c.execute("INSERT INTO source_scans (ref_id, mode, catalogue_version, text_scope, file_sha256, "
                    "method, created_at, created_by_session) VALUES (?,?,?,?,?,?,?,?)",
                    (ref, "catalogue", top, scope, "0" * 64, "full-read", "t", S))
    c.commit()
    return cur.lastrowid


LIVE_REFS = {r[0] for r in con.execute("SELECT ref_id FROM evidence_sources")}   # before any fixture is added

# ───────────────────────────── registry rows every section needs ─────────────────────────────
SLUG = scalar("SELECT slug FROM slugs WHERE status='ACTIVE' ORDER BY slug LIMIT 1")
IDENT = scalar("SELECT identity_code FROM base_taxonomy_identity WHERE identity_code<>'ALL' "
               "ORDER BY identity_code LIMIT 1")
P_ACTIVE = [r[0] for r in q("SELECT parameter_id FROM base_parameters WHERE status='active' ORDER BY parameter_id")]
if SLUG is None or IDENT is None or len(P_ACTIVE) < 4:
    finish("no ACTIVE slug, identity code or four active parameters")
QUOTE = VALUE = None
FIXTURE_TEXT = ("[PDF page 1 of 1]\nThe clear width of every primary route is to be 1200 mm at its "
                "narrowest point, measured between the handrails.\n")
FIGURE = r"[A-Za-z][^\n.]{20,100}\b(\d{3,4})\b[^\n.]{0,40}"


def extraction(ref, pid, **over):
    base = {"ref_id": ref, "parameter_id": pid, "identity_code": IDENT,
            "claim_type": "numerical", "claimed_value": VALUE, "claimed_unit": "mm",
            "claim_text": QUOTE, "extraction_method": "full-read", "figure_role": "claim",
            "source_section": "section 3", "loc_section": "3"}
    base.update(over)
    return base


def _live_full():
    """The newest full-scope catalogue reading whose derived text carries a quotable figure, for a
    source that holds an extraction on an active, direction-less parameter; None when none does."""
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
            if h["derived"] and h["exists"]:
                m = re.search(FIGURE, h["path"].read_text(encoding="utf-8", errors="replace"))
                if m:
                    return (s["ref_id"], s["catalogue_version"], pids[0][0], m.group(0).strip(),
                            m.group(1), h["sha256"])
    return None


def _built_full():
    """HAND: the same state on a fixture source -- VERIFIED, one full reading of a page-marked derived
    text, one extraction on a direction-less parameter (a direction is cleared when every one has one)."""
    pid = scalar("SELECT parameter_id FROM base_parameters WHERE status='active' AND "
                 "accessibility_direction IS NULL ORDER BY parameter_id DESC")
    if pid is None:
        pid = P_ACTIVE[-1]
        hand("UPDATE base_parameters SET accessibility_direction=NULL, direction_rationale=NULL, "
             "direction_ref_id=NULL WHERE parameter_id=?", pid)
    ref = new_source(verified=True)
    m = re.search(FIGURE, FIXTURE_TEXT)
    sha = held_text(ref, FIXTURE_TEXT)
    out = db.record_scan(scan(ref, sha, "full"), session=S)
    # (a different locator from the one the cases below write, so theirs is not a byte-identical copy)
    db.insert_extraction(extraction(ref, pid, claim_text=m.group(0).strip(), claimed_value=m.group(1),
                                    source_section="section 0", loc_section="0"), S, dry_run=False, relations=[])
    return ref, out["catalogue_version"], pid, m.group(0).strip(), m.group(1), sha


def _live_abstract():
    """A VERIFIED, DOI-bearing source read only at abstract scope that holds a fetched HTML page."""
    for s in q("SELECT ref_id FROM source_scans WHERE text_scope='abstract' AND ref_id IN "
               "(SELECT ref_id FROM evidence_sources WHERE verification_status='VERIFIED' "
               "AND doi IS NOT NULL)"):
        for h in retrieval_log.artefacts_for_source(s["ref_id"]):
            if h["exists"] and not h["derived"] and str(h["path"]).endswith(".html"):
                return s["ref_id"], h["sha256"]
    return None


def _built_abstract():
    """HAND: a VERIFIED, DOI-bearing fixture source with one abstract reading of a held HTML page and
    one extraction (the shape V05 amends)."""
    ref = new_source(verified=True, doi=f"10.0000/fixture-abstract-{next(_titles)}")
    sha = put(ref, f"{ref}-abstract.html", b"<html><body><p>" + QUOTE.encode() + b"</p></body></html>",
              content_type="text/html")
    db.record_scan(scan(ref, sha, "abstract"), session=S)
    other = next(p for p in P_ACTIVE if p != P_FULL)       # the live source holds none for P_FULL (D02)
    db.insert_extraction(extraction(ref, other), S, dry_run=False, relations=[])
    return ref, sha


_f = _live_full() or _built_full()
FULL_REF, FULL_CV, P_FULL, QUOTE, VALUE, FULL_SHA = _f
ABSTRACT_REF, HTML_SHA = _live_abstract() or _built_abstract()
UNVERIFIED_REF = scalar("SELECT ref_id FROM evidence_sources WHERE verification_status='UNVERIFIED' "
                        "ORDER BY ref_id LIMIT 1") or new_source()
NOSCAN_REF = scalar("SELECT e.ref_id FROM evidence_sources e WHERE verification_status='VERIFIED' "
                    "AND NOT EXISTS (SELECT 1 FROM source_scans s WHERE s.ref_id=e.ref_id) "
                    "AND superseded_by_ref_id IS NULL ORDER BY e.ref_id LIMIT 1") or new_source(verified=True)


print("Section M (R2-1, R2-3, R3-1, R3-8): one view says what is owed; a FULL reading outranks a block, a partial one does not")
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
                         "AND UPPER(se.language)=m.language) LIMIT 1", (SLUG,)).fetchone()
    if out_lang is None:
        skip("W01", "every pair of the map is already searched for the slug")
    else:
        c.execute("UPDATE lang_jur_map SET scope_status='scoped-out' WHERE language=?", (out_lang[0],))
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

VOCAB = sorted(dbcore.check_values(con, "evidence_sources", "processing_blocked_reason"))
SCOPES = sorted(dbcore.check_values(con, "source_scans", "text_scope"))
NONFULL = [s for s in SCOPES if s != "full"]          # 'full' is the writer's own word for the whole document
# The writer's JUDGEMENT, named, read from its one home: the reasons that restate a typed fact (a
# recorded reading; superseded_by_ref_id), which the writers refuse by pointer, mapped to that home.
COPY_HOME = {v: h for v, h in getattr(db, "_BLOCK_REASON_COPIES", {}).items() if v in VOCAB}
COPY_VALUES = sorted(COPY_HOME)
VIEW_SQL = sql_of("v_scan_ledger") or ""
_m = re.search(r"IN\s*\(([^)]*)\)\s*THEN\s*'BLOCKED'", VIEW_SQL)
IN_LIST = set(re.findall(r"'([^']+)'", _m.group(1))) if _m else set()
HEADER = re.split(r"\n\s*WITH\s", VIEW_SQL, maxsplit=1)[0]


def unnamed(vocab, header):
    """The values of `vocab` the header does not name as a bare token (R3-8)."""
    return [v for v in vocab if not re.search(r"(?<![\w-])" + re.escape(v) + r"(?![\w-])", header)]


with scratch() as c:
    # HAND: readings (no writer builds a reading without a held file) on a fresh source, which owes every pair.
    U = new_source()

    def setr(ref, v):
        hand("UPDATE evidence_sources SET processing_blocked_reason=? WHERE ref_id=?", v, ref)

    def drop(sid):
        c.execute("DELETE FROM source_scans WHERE scan_id=?", (sid,))
        c.commit()

    obstacle = set()
    for v in VOCAB:                                   # the empirical obstacle set: BLOCKED with nothing read
        setr(U, v)
        if all(r["status"] == "BLOCKED" for r in ledger(c, U)):
            obstacle.add(v)
    OB = sorted(obstacle)
    bad_full, bad_part, bad_free = [], [], []
    for v in OB:
        setr(U, v)
        sid = hand_scan(c, U, "full")
        bad_full += [(v, r["status"]) for r in ledger(c, U)
                     if (r["status"], r["scan_id"], r["text_scope"]) != ("READ-NOTHING-FOUND", sid, "full")]
        drop(sid)
        for s in NONFULL:
            sid = hand_scan(c, U, s)
            bad_part += [(v, s, r["status"]) for r in ledger(c, U)
                         if (r["status"], r["scan_id"], r["text_scope"]) != ("BLOCKED", sid, s)]
            drop(sid)
    for v in [None, *sorted(set(VOCAB) - obstacle)]:  # no obstacle stands: a partial reading is debt
        setr(U, v)
        for s in NONFULL:
            sid = hand_scan(c, U, s)
            bad_free += [(v, s, r["status"]) for r in ledger(c, U)
                         if (r["status"], r["scan_id"], r["text_scope"]) != ("READ-PARTIAL", sid, s)]
            drop(sid)
    record("W02", "a FULL reading outranks a block: the pair reads READ-NOTHING-FOUND and names that reading "
                  "(migration 124: a full reading proves the obstacle gone)", bool(OB) and not bad_full,
           bad_full[:3] or "no obstacle found")
    record("W03", "a partial, fragment or abstract reading does NOT: the pair reads BLOCKED, with that reading's "
                  "scan and scope beside it (blocked, abstract read: not debt, not hidden)",
           bool(OB and NONFULL) and not bad_part, bad_part[:3] or "no obstacle or scope")
    record("W04", "...and with no obstacle standing (NULL, or a reason the ledger does not class) the same reading "
                  "is READ-PARTIAL, the debt it was", bool(NONFULL) and not bad_free, bad_free[:3])
    # Real shapes: every live source that has a reading, with each obstacle set in turn.
    bad, n = [], 0
    for (r,) in c.execute("SELECT DISTINCT ref_id FROM source_scans").fetchall():
        keep = c.execute("SELECT processing_blocked_reason FROM evidence_sources WHERE ref_id=?", (r,)).fetchone()[0]
        setr(r, None)
        base = ledger(c, r)
        for v in OB:
            setr(r, v)
            n += 1
            for b, g in zip(base, ledger(c, r)):
                want = "BLOCKED" if b["status"] in ("READ-PARTIAL", "NOT-READ") else b["status"]
                if (g["status"], g["scan_id"], g["text_scope"]) != (want, b["scan_id"], b["text_scope"]):
                    bad.append((r, v, g["parameter_id"], b["status"], g["status"]))
        setr(r, keep)
    if n:
        record("W05", "every live read source under each obstacle: partial, abstract and unread pairs read BLOCKED "
                      "with the reading still named; full readings and extractions are unchanged", not bad, bad[:3])
    else:
        skip("W05", "no live source has a reading, or no obstacle was found")
record("W06", "the obstacle set the ledger applies (derived by trying every CHECK value on an unread source) is "
              "the view's own BLOCKED list, a proper subset of the CHECK, and never a reason a writer refuses as "
              "a copy of a typed fact",
       bool(obstacle) and obstacle == IN_LIST and obstacle < set(VOCAB) and not obstacle & set(COPY_VALUES),
       (sorted(obstacle), sorted(IN_LIST), COPY_VALUES))
record("W07", "the view's header names EVERY processing_blocked_reason value as a bare token (R3-8: a tenth CHECK "
              "value goes red here until the migration that adds it classes it)",
       bool(VOCAB) and not unnamed(VOCAB, HEADER), unnamed(VOCAB, HEADER))
record("W08", "...and that coverage test can go red: a value absent from the header is reported, a named one is not",
       unnamed([*VOCAB, "zz-not-a-reason"], HEADER) == ["zz-not-a-reason"], unnamed([*VOCAB, "zz-not-a-reason"], HEADER))
OBSTACLE = min(obstacle) if obstacle else None

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
ab_row = scalar("SELECT extraction_id FROM source_value_extractions WHERE ref_id=? LIMIT 1", ABSTRACT_REF)
if ab_row is None:
    skip("V05", "the abstract-scope source holds no extraction")
else:
    r = refusal(db.amend_extraction, ab_row, "extraction_status", "verified", "probe", session=S,
                dry_run=True)
    record("V05", "amend-extraction refuses verified with no full-scope covering reading",
           r and "full" in r, r)
full_row = scalar("SELECT extraction_id FROM source_value_extractions WHERE ref_id=? AND "
                  "parameter_id<=? AND extraction_status<>'verified' LIMIT 1", FULL_REF, FULL_CV)
if full_row is None:
    skip("V06", "every extraction of the full-scope source is already verified")
else:
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
if pymupdf is None:
    skip("X02", "pymupdf is missing, so a PDF's text layer cannot be examined (and the gate refuses)")
    skip("X03", "as X02")
else:
    # A source whose only artefact is a PDF-shaped file pymupdf cannot open: the shape the exemption is for.
    xref = new_source(verified=True)
    put(xref, f"{xref}-undecodable.pdf", b"%PDF-1.4\n" + bytes(range(256)) * 8, content_type="application/pdf")
    hand_scan(con, xref, NONFULL[0] if NONFULL else "partial")
    res, err = ok(db.insert_extraction, extraction(xref, P_FULL, claim_text="a clause read off paper",
                                                   claimed_value="12"),
                  session=S, dry_run=True, relations=[], verbatim_exempt="scanned PDF, no text layer")
    record("X02", "exemption accepted for a source whose only artefact is undecodable",
           res is not None, err)
    res, err = ok(db.observe_term, {"ref_id": xref, "surface_form": "clause", "locator": "p1",
                                    "context_quote": "a clause read off paper",
                                    "verbatim_exempt": "scanned PDF, no text layer"}, S, dry_run=True)
    record("X03", "observe-term accepts the same exemption for that source (R2-6, the shape beside X04)",
           res is not None, err)

print("Section A4: a locator on every quantified row; no byte-identical duplicate")
r = refusal(db.insert_extraction, extraction(FULL_REF, P_FULL, source_section=None,
                                             loc_section=None),
            session=S, dry_run=True, relations=[])
record("L01", "a numerical row with no locator at all is refused (R3, every tier)",
       r and "UNVERIFIED-QUANT" in r, r)
TIER = scalar("SELECT tier FROM evidence_sources WHERE ref_id=?", FULL_REF)
res, err = ok(db.insert_extraction, extraction(FULL_REF, P_FULL, loc_section=None),
              session=S, dry_run=False, relations=[])
record("L02", f"the same row with --source-section is written (tier {TIER} source; prose "
              f"locator suffices below tier 4)", res is not None, err)
r = refusal(db.insert_extraction, extraction(FULL_REF, P_FULL, loc_section=None),
            session=S, dry_run=True, relations=[])
record("L03", "a byte-identical second row is refused (a copy is not a contest)",
       r and "identical" in r, r)

print("Section A5: a full reading names a derived text")
r = refusal(db.record_scan, scan(ABSTRACT_REF, HTML_SHA, "full"), session=S, dry_run=True)
record("S01", "record-scan refuses --text-scope full over a fetched HTML page",
       r and "full_text.py" in r, r)
res, err = ok(db.record_scan, scan(FULL_REF, FULL_SHA, "full"), session=S, dry_run=True)
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
stored = scalar("SELECT direction_ref_id FROM base_parameters WHERE parameter_id=?", P_FULL)
record("D03", "accepted with a source that holds one; direction_ref_id stored",
       res is not None and stored == FULL_REF, err or stored)

print("Section A7: equivalence before minting; NAMES-NEW only through add-term")
near = q("SELECT t.term_id, t.canonical_en FROM terms t JOIN base_parameters p USING (term_id) "
         "WHERE t.canonical_en LIKE '% %' ORDER BY length(t.canonical_en) DESC LIMIT 1")
obs = scalar("SELECT observation_id FROM observed_terms WHERE context_quote IS NOT NULL LIMIT 1")
if not near or obs is None:
    for t_ in ("T01", "T02", "T03"):
        skip(t_, "no parameter term of two words, or no observation with a quote")
else:
    near = near[0]
    words = near["canonical_en"].split()
    subset_name = " ".join(words[:-1]) + "s"          # token subset, plural: 'ramp runs' shape
    # add-term now requires the name to lie inside the observed phrase (owner E1, 2026-11-06), so
    # the probe observes the phrase it then tries to mint.
    obs = db.observe_term({"ref_id": scalar("SELECT ref_id FROM observed_terms WHERE observation_id=?", obs),
                           "surface_form": subset_name, "language": "EN", "locator": "fixture",
                           "context_quote": f"a fixture sentence using {subset_name} once",
                           "verbatim_exempt": "fixture text: no retrieval artefact carries it"}, S)["observation_id"]
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

print("Section A18/R3-7: a payload that repeats an author name is malformed; one that files an author twice is one author")
# A logged payload that repeats an author name and whose DOI a source holds (derived from the
# tracked log, as the writer derives it, not named).
MAL = None
for d in sorted(x for x in pathlib.Path(retrieval_log.LOG_ROOT).iterdir() if x.is_dir()):
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
    """(listed as MALFORMED-PAYLOAD, listed as an AUTHORS cross) for `ref`; the cross is its own line."""
    mal = out.split("MALFORMED-PAYLOAD", 1)[1] if "MALFORMED-PAYLOAD" in out else ""
    return ref in mal, any(ln == f"  ✗ {ref}" for ln in out.splitlines())


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
    for t_ in ("C01", "C02", "C04"):
        skip(t_, "no logged payload repeats an author name for a source we hold (C05 to C07 build one)")
r = refusal(db.correct_source, FULL_REF, ["journal_name", "no_such_field"], session=S,
            log_session="x", dry_run=True)
record("C03", "correct-source names every payload-backed field it can rewrite",
       r and "journal_name" in r and "isbn" in r, r)
with scratch() as c:
    # Synthetic: a source with two authors and a deposit that lists the first one twice (an author filed
    # twice, not an affiliation); the control deposit lists the byline once.
    DOI = f"10.0000/fixture-dup-{next(_titles)}"
    byline = [("Fixtureauthor", "Ann"), ("Otherauthor", "Bo")]
    ref = new_source(doi=DOI, authors=db.parse_author_flags([f"{f}|{g}" for f, g in byline]))
    people = [{"family": f, "given": g} for f, g in byline]
    for sess, authors in (("session_fixture_ctl", people), ("session_fixture_dup", [*people, people[0]])):
        put(ref, f"{sess}.json", json.dumps({"message": {"DOI": DOI, "author": authors}}).encode(),
            session=sess, content_type="application/json")
    ctl, dup = verify_out("session_fixture_ctl"), verify_out("session_fixture_dup")
    record("C05", "a deposit listing the byline once is neither MALFORMED nor a cross (the control)",
           sections(ctl, ref) == (False, False), ctl[-400:])
    record("C06", "an author the deposit filed twice is MALFORMED and NOT a cross: the stored byline is "
                  "compared de-duplicated, and the note says an author may be filed twice (R3-7)",
           sections(dup, ref) == (True, False) and "or an author twice" in " ".join(dup.split()), dup[-500:])
    c.execute("DELETE FROM evidence_source_authors WHERE ref_id=? AND position=(SELECT MAX(position) "
              "FROM evidence_source_authors WHERE ref_id=?)", (ref, ref))      # HAND: damage the stored byline
    c.commit()
    record("C07", "...and a stored author missing behind the same deposit is a cross, beside MALFORMED",
           sections(verify_out("session_fixture_dup"), ref) == (True, True))

# ─────────────────────────── Unit A2: research and synthesis writers ───────────────────────────
print("Section B/A13: log-search names what it searched, in the vocabulary the map holds")
sys.path.insert(0, str(REPO))
from schemas.enums import JurisdictionCode  # noqa: E402
ENUM = {e.value for e in JurisdictionCode}
# A pair the research scope owes (v_research_scope), and a language the map holds that the scope
# does not pair with that jurisdiction.
PAIR = next((r for r in q("SELECT language, jurisdiction FROM v_research_scope ORDER BY 1, 2")
             if r["jurisdiction"] in ENUM), None)
LANG, JUR = (PAIR["language"], PAIR["jurisdiction"]) if PAIR else (None, None)
OTHER_LANG = scalar("SELECT DISTINCT language FROM lang_jur_map WHERE language NOT IN "
                    "(SELECT language FROM v_research_scope WHERE jurisdiction=?) ORDER BY 1", JUR) if PAIR else None
P1, P2 = P_ACTIVE[0], P_ACTIVE[1]
P_RET = [p for p in P_ACTIVE if p not in (P1, P2, P_FULL)][-1]
db.retire_parameter(P_RET, "fixture: a retired target", session=S)


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


if PAIR and OTHER_LANG:
    r = refusal(db.log_search, **search(language=OTHER_LANG))
    record("J02", f"a real search in a declared jurisdiction is not refused for its pairing "
                  f"({OTHER_LANG}, {JUR}); the CLI reports in_research_scope False beside True for "
                  f"({LANG}, {JUR})", r is None and scope_flag(OTHER_LANG) is False
           and scope_flag(LANG) is True, (r, scope_flag(OTHER_LANG), scope_flag(LANG)))
else:
    skip("J02", "no pair in a declared jurisdiction, or no language outside the pairing")
r = refusal(db.log_search, **search(slug=None, parameter_id=P_RET))
record("J03", "refuses --parameter naming a retired parameter", r and "active" in r, r)
if PAIR:
    res, err = ok(db.log_search, **search())
    record("J04", "a search in a map pair on an active slug is accepted", res is not None, err)
    eid, err = ok(db.log_search, **search(language=LANG.lower(), dry_run=False))
    stored = scalar("SELECT language FROM search_executions WHERE exec_id=?", eid) if eid else None
    record("J05", "log-search --language in lower case lands upper case (the map holds upper case)",
           stored == LANG, err or stored)
else:
    skip("J04", "no pair in a declared jurisdiction")
    skip("J05", "no pair in a declared jurisdiction")

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

print("Section B4/B5/D4/R3-14: conflicts -- keyed on the parameter, an unordered pair, two real populations")
CODES = [r[0] for r in q("SELECT identity_code FROM base_taxonomy_identity WHERE identity_code<>'ALL' "
                         "ORDER BY identity_code DESC LIMIT 2")]
GAP = scalar("SELECT gap_id FROM gaps WHERE status LIKE 'OPEN%' ORDER BY gap_id LIMIT 1")
last_gap = scalar("SELECT gap_id FROM gaps WHERE gap_id GLOB 'GAP-[0-9]*' ORDER BY "
                  "CAST(SUBSTR(gap_id,5) AS INTEGER) DESC LIMIT 1")
if len(CODES) < 2:
    skip("K01-K12", "fewer than two populations besides the scope marker")
else:
    HI, LO = CODES                       # HI sorts after LO
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
    ABSENT_CONF = far(CONF)
    if last_gap is None:
        skip("K05", "no gap id to derive an absent one from")
    else:
        ABSENT_GAP = far(last_gap)
        r = refusal(db.update_conflict, CONF, session=S, gap_id=ABSENT_GAP, dry_run=True)
        record("K05", "update-conflict refuses an unknown gap by name", r and ABSENT_GAP in r, r)
    r = refusal(db.update_conflict, ABSENT_CONF, session=S, status="CLOSED", dry_run=True)
    record("K06", "update-conflict refuses an unknown conflict", r and ABSENT_CONF in r, r)
    if GAP is None:
        skip("K07", "no open gap")
    else:
        res, err = ok(db.update_conflict, CONF, session=S, gap_id=GAP, dry_run=True)
        record("K07", "a live gap is accepted", err is None, err)
    rows = db.get_conflicts(parameter_id=P1)
    record("K08", "db.py conflicts --parameter-id reads the key back",
           [x["conflict_id"] for x in rows] == [CONF], rows)
    NOPE = "0-not-an-identity"             # sorts before every code, so the writer's pair-sort moves it to pop_a
    r = refusal(db.insert_conflict, conf(conflict_id=db.next_conf_id(), pop_a=LO, pop_b=NOPE),
                session=S, dry_run=True)
    record("K09", "an unknown --pop-b is refused under the flag the operator typed (not the sorted slot), "
                  "naming how to list the codes (R3-14)",
           r and "--pop-b" in r and "--pop-a" not in r and "base_taxonomy_identity" in r, r)
    all_name = scalar("SELECT display_name FROM base_taxonomy_identity WHERE identity_code='ALL'")
    if all_name is None:
        skip("K10", "the identity registry holds no scope-marker row")
    else:
        r = refusal(db.insert_conflict, conf(conflict_id=db.next_conf_id(), pop_a="ALL"), session=S, dry_run=True)
        record("K10", "the scope marker is refused as a population, quoting its own display_name (R3-14)",
               r and "--pop-a" in r and all_name in r and "scope marker" in r, r)
    r = refusal(db.insert_conflict, conf(conflict_id=db.next_conf_id(), domain="   "), session=S, dry_run=True)
    record("K11", "a blank --domain is refused (R3-14)", r and "--domain" in r, r)
    res, err = ok(db.insert_conflict, conf(conflict_id=db.next_conf_id(), parameter_id=P2, pop_a=LO, pop_b=HI),
                  session=S, dry_run=True)
    record("K12", "two real populations in either order still land (the control for K09 to K11)",
           res is not None, err)

print("Section A16: a mining attempt records at least one strategy")
if GAP is None:
    skip("M01", "no open gap")
    skip("M02", "no open gap")
else:
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

print("Section A9/R3-4: the next reference id is computed; a promotion keeps the id of the lead it IS")
NEXT = dbcore.next_ref_id(con)
TL_A, TL_B, TL_C = ("Alpha lead on stair nosings and contrast", "Bravo lead on handrail returns and finials",
                    "Charlie lead on tactile paving at kerb ramps")
LOC = {"recovered_from": "f", "status": "REFERENCE-ONLY"}
SRC2 = {"year": 2020, "evidence_type": "code", "scope": "intrinsic"}
M_A, M_B, M_C = (f"{t} (first pass)" for t in (TL_A, TL_B, TL_C))   # the main copy's own leads; the scratch group below stages TL_*
r = refusal(db.insert_locator, {**LOC, "ref_id": far(NEXT), "title": M_A}, session=S, dry_run=True)
record("I01", "add-locator refuses a ref_id that is not next-id ref", r and NEXT in r, r)
res, err = ok(db.insert_locator, {**LOC, "ref_id": NEXT, "title": M_A}, session=S, dry_run=False)
record("I02", "add-locator accepts the next id (staged)", err is None, err)
r = refusal(db.insert_evidence_source, {**SRC2, "ref_id": far(NEXT), "title": M_A},
            S, dry_run=True, authors=AUTH)
record("I03", "add-source refuses a hand-typed ref_id above the high-water mark", r and "next-id" in r, r)
res, err = ok(db.insert_evidence_source, {**SRC2, "ref_id": NEXT, "title": M_A},
              S, dry_run=True, authors=AUTH)
record("I04", "add-source accepts the id its own locator staged (promotion)", err is None, err)
want = dbcore.next_ref_id(con)
got, err = ok(db.insert_locator, {**LOC, "title": M_B}, session=S, dry_run=False)
record("I05", "add-locator with no ref_id lands as dbcore.next_ref_id (R2-9)", got == want, err or (got, want))
want = dbcore.next_ref_id(con)
got, err = ok(db.insert_evidence_source, {**SRC2, "title": M_C}, S, dry_run=False, authors=AUTH)
record("I06", "add-source with no ref_id, for a document no staged lead describes, lands as the next id",
       got == want, err or (got, want))
r1 = refusal(db.insert_evidence_source, {**SRC2, "title": M_C, "ref_id": far(want)}, S, dry_run=True, authors=AUTH)
r2 = refusal(db.insert_locator, {**LOC, "title": M_C, "ref_id": far(want)}, session=S, dry_run=True)
record("I07", "a given id that is not the computed one is still refused, naming the flag to omit",
       r1 and r2 and "omit --ref-id" in r1 and "omit --ref-id" in r2, (r1, r2))
with scratch() as c:
    nxt = lambda: dbcore.next_ref_id(c)  # noqa: E731
    la, lb = (db.insert_locator({**LOC, "title": t}, session=S, dry_run=False) for t in (TL_A, TL_B))

    def land(title, **o):
        """(the id the writer gives this source, the refusal text) -- a dry run."""
        try:
            return db.insert_evidence_source({**SRC2, "title": title, **o}, S, dry_run=True, authors=AUTH), None
        except Refusal as exc:
            return None, str(exc)

    got, err = land(TL_A)
    record("I08", "no --ref-id, the title of staged lead A: the source lands on A's id, not the next one (R3-4)",
           got == la != nxt(), (got, la, err))
    got, err = land(TL_A, ref_id=lb)
    record("I09", "lead B's id for lead A's document is refused, naming B's title (one document, one identity)",
           got is None and repr(TL_B) in (err or "") and "Nothing was written" in err, (got, err))
    stale = c.execute("SELECT ref_id, title FROM source_locators WHERE COALESCE(status,'')<>'RETIRED' AND "
                      "ref_id NOT IN (SELECT ref_id FROM evidence_sources) AND ref_id NOT IN (?,?) AND "
                      "COALESCE(title,'')<>'' ORDER BY ref_id LIMIT 1", (la, lb)).fetchone()
    if stale is None:
        skip("I10", "no live staged lead outside the fixtures")
    else:
        got, err = land("An unrelated title about door hardware", ref_id=stale["ref_id"])
        record("I10", f"a live staged id ({stale['ref_id']}) for an unrelated title is refused, naming that lead",
               got is None and repr(stale["title"]) in (err or "") and "Nothing was written" in err, (got, err))
    got, err = land("A title no lead carries, about threshold ramps")
    record("I11", "a title matching no lead lands on the next id", got == nxt(), (got, err))
    got, err = land(TL_A, ref_id=la)
    record("I12", "the matching lead's own id, given, is accepted", got == la, (got, err))
    live_doi = c.execute("SELECT ref_id, doi FROM source_locators WHERE COALESCE(doi,'')<>'' AND "
                         "COALESCE(status,'')<>'RETIRED' AND ref_id NOT IN (SELECT ref_id FROM evidence_sources) "
                         "AND ref_id NOT IN (?,?) ORDER BY ref_id LIMIT 1", (la, lb)).fetchone()
    lc = db.insert_locator({**LOC, "title": TL_C + " (DOI-bearing)", "doi": "10.9999/fixture.charlie"},
                           session=S, dry_run=False)
    for label, lid, doi in (("live", live_doi and live_doi["ref_id"], live_doi and live_doi["doi"]),
                            ("fixture", lc, "10.9999/fixture.charlie")):
        if lid is None:
            skip(f"I13 {label}", "no live staged lead carries a DOI")
            continue
        got, err = land("A differently worded title", doi=doi.upper())
        r_given, err_given = land("A differently worded title", doi=doi.upper(), ref_id=nxt())
        record(f"I13 {label}", f"the lead {lid} is promoted under its own id by its DOI (folded), whatever the "
                               f"title; the next id given for it is refused, naming the lead",
               got == lid and r_given is None and lid in (err_given or ""), (got, lid, err_given))
    la2 = db.insert_locator({**LOC, "title": TL_A.upper() + "!"}, session=S, dry_run=False)
    got, err = land(TL_A)
    record("I14", "two staged leads for one document: refused naming both, no id guessed",
           got is None and la in (err or "") and la2 in err and "Nothing was written" in err, (got, err))
    got, err = land(TL_C + " (DOI-bearing)", doi="10.9999/not-charlie")
    record("I15", "the same title with a different DOI is not the lead (a shared identifier that differs)",
           got == nxt() and got != lc, (got, err))

print("Section C8/R3-17: coverage counts what the vocabulary admits and the scope records, and says what the slug is")
r = refusal(db.get_coverage_completeness, "no-such-slug")
record("G01", "coverage refuses an unknown slug instead of answering zeros", r and "slugs" in r, r)
cov = db.get_coverage_completeness(SLUG)
n_req = scalar("SELECT COUNT(*) FROM v_research_scope")
n_open = scalar("SELECT COUNT(*) FROM v_coverage_priority WHERE slug=?", SLUG)
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
    if keep is None:
        one = none = None
        skip("G03", "every owed pair of the slug is already searched")
        skip("G04", "as G03")
    else:
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
    # R3-17: a MERGED slug owes nothing (its survivor does): live, else HAND-made from the active slug.
    merged = c.execute("SELECT slug, merged_into FROM slugs WHERE status='MERGED' ORDER BY slug LIMIT 1").fetchone()
    if merged is None:
        c.execute("INSERT INTO slugs (slug, topic_directory, sl_path, bpc_path, status, merged_into, created_at, "
                  "created_by_session, updated_at, updated_by_session) SELECT slug || '-fixture-merged', "
                  "topic_directory, sl_path, bpc_path, 'MERGED', slug, created_at, created_by_session, "
                  "updated_at, updated_by_session FROM slugs WHERE slug=?", (SLUG,))
        c.commit()
        merged = c.execute("SELECT slug, merged_into FROM slugs WHERE status='MERGED'").fetchone()
    mc = db.get_coverage_completeness(merged[0])
    record("G06", "coverage on a MERGED slug names its status and survivor, says it owes no searches, and is "
                  "not complete (R3-17: 'pairs_required N, searched 0' was debt no search can pay)",
           mc.get("slug_status") == "MERGED" and mc.get("merged_into") == merged[1]
           and mc.get("owes_searches") is False and mc["complete"] is False, mc)
    record("G07", "...and on an ACTIVE slug it names the status and adds no override",
           cov.get("slug_status") == "ACTIVE" and "owes_searches" not in cov and cov.get("merged_into") is None, cov)
    if PAIR:
        r = refusal(db.log_search, **search(slug=merged[0]))
        record("B02", "log-search refuses a MERGED slug, naming the survivor (R3-14: a folded topic is not filed to)",
               r and merged[1] in r and "MERGED" in r, r)
    else:
        skip("B02", "no pair in a declared jurisdiction")
if PAIR and OTHER_LANG:
    _, err = ok(db.log_search, **search(language=OTHER_LANG, dry_run=False))
    after = db.get_coverage_completeness(SLUG)
    record("G05", "a real search outside the owed scope is logged and counted apart (R2-2), not refused",
           err is None and after.get("searches_outside_scope", -1) == cov.get("searches_outside_scope", -2) + 1,
           err or (cov, after))
else:
    skip("G05", "no pair in a declared jurisdiction, or no language outside the pairing")

print("Section E6: mining verbs speak in ref_ids")
UM_SLUG = scalar("SELECT l.slug FROM source_slug_links l JOIN evidence_sources e USING (ref_id) WHERE "
                 "COALESCE(e.citation_mining_status,'')<>'mined' LIMIT 1")
if UM_SLUG is None:
    for t_ in ("U01", "U02", "U03"):
        skip(t_, "every linked source is mined")
else:
    um = db.get_unmined_sources(UM_SLUG)
    record("U01", "unmined rows carry the global ref_id", bool(um) and "ref_id" in um[0], um[:1])
    r = refusal(db.is_mined, SLUG, "11")
    record("U02", "is-mined refuses a --ref that is not a reference id", r and "REF-" in r, r)
    r = refusal(db.log_mining, SLUG, "11", "backward", session=S, dry_run=True, notes="x")
    record("U03", "log-mining refuses the same", r and "REF-" in r, r)

print("Section C4: an unretrievable source is BLOCKED in the ledger, not NOT-READ")
if OBSTACLE is None:
    skip("Q01", "the ledger classes no reason as an obstacle (W06 is red)")
else:
    ref = new_source(processing_blocked_reason=OBSTACLE)
    with scratch() as c:
        led = {r["status"] for r in ledger(c, ref)}
    record("Q01", "add-source writes an obstacle as processing_blocked_reason and the ledger shows BLOCKED",
           led == {"BLOCKED"}, led)

print("Section R2-3/R3-1: a reason is an obstacle the ledger classes, two are copies, and NO reading clears it")
if not COPY_VALUES:
    feature("P01", "add-source refuses the reasons that copy a typed fact", False, "db._BLOCK_REASON_COPIES")
for i, v in enumerate(COPY_VALUES, 1):
    r = refusal(db.insert_evidence_source, {**SRC2, "title": TL_A + str(i), "verification_status": "UNVERIFIED",
                                            "processing_blocked_reason": v}, S, dry_run=True, authors=AUTH)
    home = COPY_HOME[v]
    record(f"P0{i}", f"add-source refuses processing_blocked_reason {v!r}, naming its typed home {home!r}",
           r and v in r and home in r and "Nothing was written" in r, r)


def block_then_read(c, ref, abs_sha, full_sha, ids, label):
    """An unread source blocked for an obstacle, read at abstract scope, re-described, then read in full."""
    nr = {r["parameter_id"] for r in ledger(c, ref) if r["status"] == "NOT-READ"}
    pairs = lambda: [r for r in ledger(c, ref) if r["parameter_id"] in nr]  # noqa: E731
    col = lambda: c.execute("SELECT processing_blocked_reason FROM evidence_sources WHERE ref_id=?",  # noqa: E731
                            (ref,)).fetchone()[0]
    if not nr:
        return [skip(t, f"{label}: every pair of {ref} is read") for t in ids]
    _, err = ok(db.amend_source, ref, "processing_blocked_reason", OBSTACLE, "fixture: could not be read", session=S)
    n_block = sum(r["status"] == "BLOCKED" for r in pairs())
    record(ids[0], f"{label}: amend-source sets an obstacle ({OBSTACLE!r}) after admission and the ledger reads "
                   f"BLOCKED", err is None and n_block == len(nr), err or n_block)
    out, err = ok(db.record_scan, scan(ref, abs_sha, "abstract"), S)
    rows = {(r["status"], r["scan_id"], r["text_scope"]) for r in pairs()}
    record(ids[1], f"{label}: an abstract reading leaves the column alone (no block_cleared) and the ledger reads "
                   f"BLOCKED with that reading beside it", bool(out) and "block_cleared" not in out
           and col() == OBSTACLE and rows == {("BLOCKED", out["scan_id"], "abstract")}, err or (out, col(), rows))
    others = [v for v in OB if v != OBSTACLE]
    if others:
        before = [tuple(r) for r in pairs()]
        _, err = ok(db.amend_source, ref, "processing_blocked_reason", others[0], "re-described", session=S)
        record(ids[2], f"{label}: amend-source re-describes the reason after a reading (R3-21); the ledger, not the "
                       f"column, says what holds, and it still reads BLOCKED with the reading beside it",
               err is None and col() == others[0] and [tuple(r) for r in pairs()] == before
               and {r["status"] for r in pairs()} == {"BLOCKED"}, err or (col(), before[:1]))
    else:
        skip(ids[2], "the ledger classes only one reason as an obstacle")
    out, err = ok(db.record_scan, scan(ref, full_sha, "full"), S)
    st = {r["status"] for r in pairs()}
    record(ids[3], f"{label}: a FULL reading lands, leaves the column alone, and outranks the block "
                   f"(READ-NOTHING-FOUND)", bool(out) and "block_cleared" not in out and col() is not None
           and st == {"READ-NOTHING-FOUND"}, err or (out, col(), st))


if OBSTACLE is None or not OB:
    skip("P03-P10", "the ledger classes no reason as an obstacle (W06 is red)")
else:
    with scratch() as c:
        ref = new_source()
        sha_abs = put(ref, f"{ref}-abstract.html", b"<html>An abstract about stair nosings.</html>",
                      content_type="text/html")
        sha_full = held_text(ref, "Fixture text with no page markers. Stair nosing contrast.\n")
        block_then_read(c, ref, sha_abs, sha_full, ("P03", "P05", "P06", "P07"), "fixture")
        r = refusal(db.amend_source, ref, "processing_blocked_reason", COPY_VALUES[0] if COPY_VALUES else "x", "x",
                    session=S, dry_run=True)
        record("P04", "...and amend-source refuses a copy value there too",
               COPY_VALUES and r and COPY_VALUES[0] in r and "Nothing was written" in r, r)
    # The real shape: a live source nothing has read, holding a fetched file and a derived text (a full
    # reading the writer accepts is found by a dry run, since a derived text may be short of pages).
    real = None
    for r_, url in q("SELECT e.ref_id, e.url FROM evidence_sources e WHERE e.superseded_by_ref_id IS NULL AND NOT "
                     "EXISTS (SELECT 1 FROM source_scans s WHERE s.ref_id=e.ref_id) ORDER BY e.ref_id"):
        held = [h for h in retrieval_log.artefacts_for_source(r_, url) if h["exists"]]
        fetched = next((h for h in held if not h["derived"]), None)
        derived = next((h for h in held if h["derived"] and not h.get("content_type")), None)
        if fetched and derived and ok(db.record_scan, scan(r_, derived["sha256"], "full"), S, dry_run=True)[1] is None:
            real = (r_, fetched["sha256"], derived["sha256"])
            break
    if real is None:
        for t_ in ("P08", "P09", "P10", "P11"):
            skip(t_, "no live source is unread and holds both a fetched file and a derived text the writer takes as full")
    else:
        with scratch() as c:
            block_then_read(c, real[0], real[1], real[2], ("P08", "P09", "P10", "P11"), f"live {real[0]}")

print("Section R3-3: `full` over a text with no page markers lands as the operator's claim, and says so")
record("F00", "payload_page_range is removed: a deposit's `page` says the PDF is paginated, not that an HTML text is "
              "not the document (R3-3)", not hasattr(retrieval_log, "payload_page_range"),
       "retrieval_log.payload_page_range is still defined")
fref = new_source()
sha = held_text(fref, "Fixture: a landing record with no page markers.", payload={"page": "12-34"})
res, err = ok(db.record_scan, scan(fref, sha, "full"), S, dry_run=True)
record("F01", "full over a page-less text lands even when the source's own deposit states pages, and the result "
              "says uncounted (the operator's claim, not a count)",
       bool(res) and res.get("uncounted") is True and res.get("pages_read") is None, err or res)
res, err = ok(db.record_scan, scan(fref, sha, "abstract"), S, dry_run=True)
record("F02", "the same call recorded as abstract lands and is not marked uncounted (a count is owed to full only)",
       res is not None and "uncounted" not in res, err or res)
pref = new_source()
n_pages = 3
sha = held_text(pref, "".join(f"[PDF page {i} of {n_pages}]\nPage {i} of the fixture.\n" for i in range(1, n_pages + 1)))
res, err = ok(db.record_scan, scan(pref, sha, "full"), S, dry_run=True)
record("F03", "full over a text with every page marker lands counted: pages_read equals pages_total, no uncounted",
       bool(res) and res.get("pages_read") == res.get("pages_total") == n_pages and "uncounted" not in res, err or res)
held_n, all_n = 4, 79
rref = new_source()
sha = held_text(rref, "".join(f"[PDF page {i} of {all_n}]\nPage {i}.\n" for i in range(1, held_n + 1)))
r = refusal(db.record_scan, scan(rref, sha, "full"), session=S, dry_run=True)
record("F04", "...while full over fewer pages than the document has is still refused (the check the scan CAN make)",
       r and f"{held_n} of {all_n}" in r and "Nothing was written" in r, r)
# Real shapes: derive, from the logged Crossref payloads, a source of each shape and hold a page-less derived
# text for it in a second scratch log (so the live sources are left as they were).
shapes = {"page equal to the article number (an elocator)": None, "no page at all": None, "a page range a-b": None}
for a in retrieval_log._artefact_index():
    if a.derived or a.ref_id not in LIVE_REFS:
        continue
    try:
        m = json.loads(a.path.read_text()).get("message")
    except Exception:       # noqa: BLE001
        continue
    if not (isinstance(m, dict) and m.get("DOI")):
        continue
    pg, art = str(m.get("page") or "").strip(), str(m.get("article-number") or "").strip()
    k = ("page equal to the article number (an elocator)" if pg and pg == art else
         "no page at all" if not pg else "a page range a-b" if re.fullmatch(r"\d+\s*[-–]\s*\d+", pg) else None)
    if k and shapes[k] is None:
        shapes[k] = a.ref_id
for k, r_ in shapes.items():
    if r_ is None:
        skip("F05", f"no live payload with {k}")
        continue
    with log_root(farm("farm-f")):
        sha = held_text(r_, "Fixture text with no page markers, for a live source of this deposit shape.\n")
        res, err = ok(db.record_scan, scan(r_, sha, "full"), S, dry_run=True)
    record("F05", f"live {r_} (deposit with {k}): full over a page-less derived text lands, uncounted",
           bool(res) and res.get("uncounted") is True and res.get("pages_read") is None, err or res)
tref = new_source()
held_text(tref, "Fixture: a derived text named -text.txt.\n")
bodies = retrieval_log.decodable_body_artefacts(tref)
record("R02", "a derived text is a decodable body by the manifest's `derived` flag, not by a `-full-text.txt` suffix",
       len(bodies) == 1 and bodies[0].endswith("-text.txt") and not bodies[0].endswith("-full-text.txt"), bodies)
r = refusal(db.observe_term, {"ref_id": tref, "surface_form": "clause", "locator": "p1",
                              "context_quote": "a clause typed from memory",
                              "verbatim_exempt": "page read from an image"}, S, dry_run=True)
record("X04", "observe-term refuses --verbatim-exempt when a decodable body is held, naming it "
              "(the refusal add-extraction already applied, R2-6)", r and bodies and bodies[0] in r, r)

print("Section R3-2: a decodable body includes a PDF with a text layer; the exemption needs a persisted page render")
live_body = functools.lru_cache(None)(retrieval_log.decodable_body_artefacts)   # a live source's bodies do not change
KIND = getattr(retrieval_log, "PAGE_RENDER_KIND", None)      # absent on an older tree: D04 to D09 then go red by name


def pdf_bytes(text=None):
    doc = pymupdf.open()
    page = doc.new_page()
    if text:
        page.insert_text((72, 72), text)
    out = doc.tobytes()
    doc.close()
    return out


def render(ref, name):
    """Persist a page picture for `ref` as scripts/research/page_image.py does (a manifest line of its kind)."""
    d = pathlib.Path(retrieval_log.LOG_ROOT) / "session_fixture"
    (d / name).write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * 32)
    retrieval_log.record_file(d / name, "session_fixture", f"{ref}.pdf", ref_id=ref, kind=KIND)
    retrieval_log._ARTEFACT_INDEX.clear()


def notes_of(c, ref):
    return c.execute("SELECT notes FROM observed_terms WHERE ref_id=? ORDER BY observation_id DESC LIMIT 1",
                     (ref,)).fetchone()


def observe(ref, **o):
    return {"ref_id": ref, "surface_form": "gradient", "locator": "p1",
            "context_quote": "a gradient typed from memory", "verbatim_exempt": "page read from an image", **o}


if pymupdf is None:
    for t_ in ("D01-D09",):
        skip(t_, "pymupdf is missing: a PDF's text layer cannot be examined (and every gate that needs it refuses)")
else:
    # Real shapes: each live source holding a PDF and no text page or derived text is decodable iff
    # pymupdf finds text on a page of it.
    bad, n, pdf_text = [], 0, []
    for r_, url in q("SELECT ref_id, url FROM evidence_sources"):
        held = [h for h in retrieval_log.artefacts_for_source(r_, url) if h["exists"]]
        pdfs = [h for h in held if not h["derived"] and h["artefact"].lower().endswith(".pdf")]
        texty = [h for h in held if (h.get("content_type") or "").lower().startswith("text/")
                 or (h["derived"] and not h.get("content_type"))]
        if not pdfs or texty:
            continue
        want = False
        for h in pdfs:
            try:
                want = want or any(retrieval_log.normalise_quote(p.get_text()) for p in pymupdf.open(str(h["path"])))
            except Exception:       # noqa: BLE001 -- a PDF pymupdf cannot open holds no text layer
                pass
        n += 1
        if bool(live_body(r_)) != want:
            bad.append((r_, want))
        if want and not any(h["derived"] and h.get("derivation_kind") == KIND for h in held):
            pdf_text.append((r_, pdfs[0]["artefact"]))      # a text-layer PDF, no render in its manifest
    if n:
        record("D01", "every live source holding only PDFs is decodable iff a page of one has a text layer "
                      "(the oracle is pymupdf, not the writer's helper)", not bad, bad[:3])
    else:
        skip("D01", "no live source holds a PDF and no other body")
    blank, texty_pdf = f"REF-FIX-{next(_titles)}", f"REF-FIX-{next(_titles)}"
    put(blank, "blank.pdf", pdf_bytes(), content_type="application/pdf")
    put(texty_pdf, "texty.pdf", pdf_bytes("Ramp gradient is to be gentle on the primary route"),
        content_type="application/pdf")
    record("D02", "a PDF with no text layer is not a body; one with a text layer is (named, once)",
           retrieval_log.decodable_body_artefacts(blank) == []
           and len(retrieval_log.decodable_body_artefacts(texty_pdf)) == 1, "")
    marks, prose, page = (f"REF-FIX-{next(_titles)}" for _ in range(3))
    put(marks, "m-text.txt", b"[PDF page 1 of 2]\n\n[PDF page 2 of 2]\n", derived=True, derived_from="z.pdf",
        derivation_kind="text-extraction")
    put(prose, "t-text.txt", b"[PDF page 1 of 1]\nRamp gradient shall not exceed a stated ratio\n", derived=True,
        derived_from="z.pdf", derivation_kind="text-extraction")
    put(page, "p.html", b"<p>Ramp gradient</p>", content_type="text/html")
    record("D03", "a derived text of page markers alone is not a body; one with prose is; a fetched page is",
           retrieval_log.decodable_body_artefacts(marks) == [] and len(retrieval_log.decodable_body_artefacts(prose)) == 1
           and len(retrieval_log.decodable_body_artefacts(page)) == 1, "")
    mixed = f"REF-FIX-{next(_titles)}"
    put(mixed, "a.png", b"\x89PNG", content_type="image/png", derived=True, derived_from="z.pdf", derivation_kind=KIND)
    put(mixed, "b.json", b"{}", content_type="application/json", derived=True, derived_from="z.pdf",
        derivation_kind="pdf-bibliography")
    put(mixed, "c-text.txt", b"[PDF page 1 of 1]\nramp\n", derived=True, derived_from="z.pdf",
        derivation_kind="text-extraction")
    PRA = getattr(retrieval_log, "page_render_artefacts", None)
    if feature("D04", "page_render_artefacts lists a derived artefact of the page-render kind and nothing else",
               PRA, "retrieval_log.page_render_artefacts"):
        record("D04", "page_render_artefacts lists a derived artefact of the page-render kind and nothing else",
               PRA(mixed) == ["session_fixture/a.png"], PRA(mixed))
    with scratch() as c:
        t_ref, u_ref = new_source(), new_source()
        put(t_ref, f"{t_ref}.pdf", pdf_bytes("Ramp gradient is to be gentle on the primary route"),
            content_type="application/pdf")
        put(u_ref, f"{u_ref}.pdf", pdf_bytes(), content_type="application/pdf")
        put(u_ref, f"{u_ref}.json", b'{"message": {"title": "x"}}', content_type="application/json")
        r = refusal(db.observe_term, observe(t_ref), S, dry_run=True)
        record("D05", "observe-term --verbatim-exempt over a PDF with a text layer and no page render is refused, naming "
                      "the PDF and the verb that persists a render (R3-2: the exemption was admitting fabricated quotes)",
               r and f"{t_ref}.pdf" in r and "page_image.py" in r and "Nothing was written" in r, r)
        res, err = ok(db.observe_term, observe(u_ref), S)
        note = notes_of(c, u_ref)
        record("D06", "a source holding only bytes that carry no text (a blank PDF, a JSON record) is accepted, with "
                      "no render named", err is None and note and "page renders" not in (note[0] or ""), err or note)
        render(t_ref, f"{t_ref}.p0001.png")
        res, err = ok(db.observe_term, observe(t_ref), S)
        note = notes_of(c, t_ref)
        record("D07", "the same text-layer PDF once a page render is persisted is accepted, and the marker names the render",
               err is None and note and f"{t_ref}.p0001.png" in (note[0] or "") and "page renders held" in (note[0] or ""),
               err or note)
        saved = sys.modules.get("pymupdf")
        sys.modules["pymupdf"] = None       # the reader is missing: the helper must say so, not pass
        try:
            m_ref = new_source()
            put(m_ref, f"{m_ref}.pdf", pdf_bytes("Ramp gradient is to be gentle"), content_type="application/pdf")
            r = refusal(db._refuse_exempt_with_body, m_ref, "--context-quote", "ctx")
        finally:
            sys.modules["pymupdf"] = saved
        record("D08", "with pymupdf missing the exemption is refused naming the dependency (a gate that cannot examine "
                      "does not pass)", r and "ensure-deps.sh" in r, r)
    # Live sources through the one home of the rule (the helper observe-term, add-extraction and
    # relate-extraction all call): those with persisted renders are accepted and the tail names them; those
    # holding a decodable body and no render are refused naming it.
    acc, ref_, n_acc, n_ref = [], [], 0, 0
    for (r_,) in q("SELECT ref_id FROM evidence_sources WHERE superseded_by_ref_id IS NULL"):
        renders = PRA(r_) if PRA else []
        if renders:
            n_acc += 1
            tail, err = ok(db._refuse_exempt_with_body, r_, "--context-quote", "ctx")
            if err or not all(x in (tail or "") for x in renders[:3]):
                acc.append((r_, err or tail))
        elif live_body(r_):
            n_ref += 1
            r = refusal(db._refuse_exempt_with_body, r_, "--context-quote", "ctx")
            if not (r and live_body(r_)[0].split("/")[-1].replace(getattr(retrieval_log, "UNEXAMINABLE_PDF", ""), "") in r):
                ref_.append((r_, r))
    if not PRA:
        record("D09", "live sources with persisted page renders: exemption accepted, the marker tail names them",
               False, "feature absent: retrieval_log.page_render_artefacts")
    elif n_acc:
        record("D09", "live sources with persisted page renders: exemption accepted, the marker tail names them",
               not acc, acc[:2])
    else:
        skip("D09", "no live source holds a persisted page render")
    for r_, name in pdf_text:       # the shape R3-2 is about, selected by pymupdf and the manifest, not by the helper
        r = refusal(db._refuse_exempt_with_body, r_, "--context-quote", "ctx")
        if not (r and name in r):
            ref_.append((r_, r))
    if n_ref or pdf_text:
        record("D10", "live sources holding a decodable body (a text, or a PDF with a text layer) and no render: "
                      "exemption refused, naming the body", not ref_, ref_[:2])
    else:
        skip("D10", "no live source holds a decodable body and no render")

# ─────────────────────────── Round 2, A2: connection arity, help text, name words ───────────────────────────
print("Section R2-10/11/12, R3-12: an arity row per CHECK value, help and choices read from the column, comparator words in names")
types = sorted(dbcore.check_values(con, "connections", "connection_type"))
record("A01", "every connection_type in the CHECK has an arity row", all(t in db._CONNECTION_ARITY for t in types),
       [t for t in types if t not in db._CONNECTION_ARITY])
victim = next((t for t in types if db._CONNECTION_ARITY.get(t, ("",))[0] == "parameter_id"), None)
targets = [("parameter_id", P1), ("parameter_id", P2)]
if victim is None:
    skip("A02", "no connection type takes parameter targets")
    skip("A03", "as A02")
else:
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
tok = lambda column: "zz-added-" + column.replace("_", "-")  # noqa: E731
VOCABS = (("extraction_relations", "to_kind", ("add-extraction", "relate-extraction")),
          ("extraction_relations", "stated", ("add-extraction", "relate-extraction")),
          ("extraction_relations", "input_role", ("add-extraction", "relate-extraction")),
          ("gaps", "category", ("add-gap",)))
with scratch() as c:
    # HAND: a value added to each column's CHECK by editing the stored schema text (a scratch copy only). A
    # help text or a choices list that reads the column shows it; one that restates the vocabulary does not.
    c.execute("PRAGMA writable_schema=ON")
    edited = 0
    for table, column, _ in VOCABS:
        sql = c.execute("SELECT sql FROM sqlite_master WHERE name=?", (table,)).fetchone()[0]
        new = re.sub(rf"\b{column} IN \(", f"{column} IN ('{tok(column)}', ", sql, count=1)
        edited += new != sql
        c.execute("UPDATE sqlite_master SET sql=? WHERE name=?", (new, table))
    c.commit()
    c.execute("PRAGMA writable_schema=OFF")
    if edited != len(VOCABS):
        skip("O14", "a CHECK's text has a shape this edit does not match")
        skip("O15", "as O14")
    else:
        helps = {v: re.sub(r"\s+", "", cli(v, "--help").stdout) for v in ("add-extraction", "relate-extraction", "add-gap")}
        miss = [(verb, column) for _, column, verbs in VOCABS for verb in verbs if tok(column) not in helps[verb]]
        record("O14", "a value added to a CHECK reaches the --help of every flag that takes it: add-extraction's "
                      "--to-kind/--stated/--input-role, relate-extraction's, add-gap's --category (R3-12: read "
                      "from the column, not restated)", not miss, miss)
        rel0 = rels[0] if rels else "none"
        ok_run = cli("relate-extraction", "--from", "1", "--relation", rel0, "--to-kind", tok("to_kind"), "--session", S,
                     "--dry-run")
        bad_run = cli("relate-extraction", "--from", "1", "--relation", rel0, "--to-kind", "nonsense", "--session", S,
                      "--dry-run")
        record("O15", "relate-extraction --to-kind takes its choices from the column: a value the CHECK gains passes "
                      "argparse (it is refused later, for want of the extraction); a bogus one exits 2",
               "invalid choice" not in ok_run.stderr and bad_run.returncode == 2 and "invalid choice" in bad_run.stderr,
               (ok_run.stderr[-200:], bad_run.stderr[-100:]))
h = re.sub(r"\s+", " ", cli("adjudicate-term", "--help").stdout)
record("O16", "adjudicate-term --term-id help no longer says NAMES-NEW needs one: the verb refuses it (T03) and the "
              "help names add-term --from-observation (R3-12)",
       "Required for NAMES-EXISTING and NAMES-NEW" not in h and "add-term --from-observation" in h, h[-300:])
pri = sorted(dbcore.check_values(con, "gaps", "priority"))[0]
bad_cat = cli("add-gap", "--category", "ZZ-not-a-category", "--priority", pri, "--description", "x", "--session", S,
              "--dry-run")
cats = sorted(dbcore.check_values(con, "gaps", "category"))
record("O17", "add-gap --category outside the CHECK is refused by argparse, naming the live values (R3-14: it was a raw "
              "IntegrityError)", bad_cat.returncode == 2 and "invalid choice" in bad_cat.stderr
       and all(v in bad_cat.stderr for v in cats) and "IntegrityError" not in bad_cat.stderr, bad_cat.stderr[-250:])

obs_ = scalar("SELECT observation_id FROM observed_terms WHERE context_quote IS NOT NULL LIMIT 1")
live = [t for (t,) in q("SELECT canonical_en FROM terms")]
two = next((t for t in live if " " in t), None)
if obs_ is None or two is None:
    for t_ in ("Z01-Z05", "Z07"):
        skip(t_, "no observation with a quote, or no multi-word term")
else:
    for i, (name, word) in enumerate([("not steeper than", "than"), ("at least one landing", "at least"),
                                      ("no more landings", "no more"), ("not exceeding landings", "not exceeding"),
                                      ("exceeds landings", "exceeds")], 1):
        r = refusal(db.insert_term, obs_, name, "probe", session=S, dry_run=True)
        record(f"Z0{i}", f"add-term refuses the name {name!r}, naming {word!r}", r and f"'{word}'" in r.lower(), r)
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
VB = getattr(db, "_VALUE_BEARING_NAME", None)
if feature("Z06", "no live term name is caught by the widened name rule", VB is not None, "db._VALUE_BEARING_NAME"):
    record("Z06", "no live term name is caught by the widened name rule (it would strand the vocabulary)",
           not [t for t in live if VB.search(t)], [t for t in live if VB.search(t)])

# ─────────────────────────── Round 2, C: gates and the engine ───────────────────────────
print("Section C: the engine names a missing direction and a slug it does not hold, takes a stamp and a session in the "
      "stored shape; the verified-scan reader examines every live extraction; the skill-vocabulary audit can go red")
ICF = scalar("SELECT icf_code FROM base_icf LIMIT 1")
STAMP = dbcore.now()                    # the shape every stored created_at has: 'YYYY-MM-DD HH:MM'


def assess(db_path, pid, slug, *extra, stamp=None, session=S):
    return subprocess.run([sys.executable, str(REPO / "scripts/assess/assess_cell.py"), "--db", db_path,
                           "--emit-sql", os.path.join(TMP, "a.sql"), "--parameter-id", str(pid),
                           "--slug", slug, "--identity", IDENT, "--icf", ICF, "--session", session,
                           "--stamp", stamp or STAMP, *extra],
                          capture_output=True, text=True, env=dict(os.environ))


P_NODIR = scalar("SELECT parameter_id FROM base_parameters WHERE status='active' AND "
                 "accessibility_direction IS NULL AND parameter_id IN (SELECT parameter_id FROM "
                 "source_value_extractions) AND parameter_id<>? ORDER BY 1 LIMIT 1", P_FULL)
CELL_P = P_NODIR if P_NODIR is not None else P1
if ICF is None:
    for t_ in ("E01-E03", "E05", "E06", "E11", "E12"):
        skip(t_, "the ICF registry is empty")
else:
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
    with scratch() as c:
        path = os.environ["GUIDEBOOK_DB_PATH"]
        n_before = c.execute("SELECT COUNT(*) FROM specifications").fetchone()[0]
        legacy = STAMP.replace(" ", "T") + ":00Z"            # the shape the engine took until R3-16
        r = assess(path, CELL_P, SLUG, stamp=legacy)
        record("E11", f"a --stamp in a foreign shape ({legacy!r}) is refused, naming the shape dbcore.now() writes, "
                      f"before any row (R3-16)", r.returncode != 0 and "--stamp" in r.stdout + r.stderr
               and c.execute("SELECT COUNT(*) FROM specifications").fetchone()[0] == n_before,
               (r.stdout + r.stderr)[-300:])
        top = c.execute("SELECT COALESCE(MAX(rowid), 0) FROM specifications").fetchone()[0]
        r = assess(path, CELL_P, SLUG, session=S + ".md")
        rows = c.execute("SELECT DISTINCT created_by_session FROM specifications WHERE rowid > ?", (top,)).fetchall()
        record("E12", "a `.md` session pointer is stored as the bare stem (CLAUDE.md section 7: a wrong form scopes a "
                      "gate to nothing)", r.returncode == 0 and [x[0] for x in rows] == [S], (rows, r.stderr[-200:]))
    if P_NODIR is not None:
        rj = os.path.join(TMP, "assess.json")
        r = assess(DB, P_NODIR, SLUG, "--report-json", rj)
        rep = json.load(open(rj))[0] if r.returncode == 0 else {}
        gap = q("SELECT description FROM gaps WHERE gap_id=?", rep.get("gap_register_id") or "")
        record("E01", "a pending cell with no direction records set-parameter-direction in its gap",
               r.returncode == 0 and gap and "set-parameter-direction" in gap[0][0],
               (r.stdout + r.stderr)[-300:] if r.returncode else (gap[0][0][-200:] if gap else "no gap"))
        record("E02", "the summary line prints every lens the cell was given",
               f"param {P_NODIR}×{IDENT}/" in r.stdout, r.stdout[:120])
        record("E03", "the report carries direction_ref_id beside the direction",
               "direction_ref_id" in rep, list(rep)[:5])
    else:
        for t_ in ("E01", "E02", "E03"):
            skip(t_, "no active direction-less parameter holds an extraction")
# ─────────────────────── T-013: a gap says what it is a gap in; a search says which gap caused it ───────────────────────
print("Section T013: add-gap names a cell-less gap's parameter, lens, jurisdiction and language; log-search --gap-id; "
      "an engine-made gap is reached through its cell, never copied (rule 5)")
GAP_SUBJECT = ("parameter_id", "identity_code", "icf_code", "needs_code", "medical_code", "jurisdiction", "language")
gcols = [x[1] for x in con.execute("PRAGMA table_info(gaps)")]
secols = [x[1] for x in con.execute("PRAGMA table_info(search_executions)")]
fk_of = lambda t, col: [tuple(f[2:5]) for f in con.execute(f'PRAGMA foreign_key_list("{t}")') if f[3] == col]  # noqa: E731
record("T013-01", "gaps holds the seven subject columns and search_executions holds gap_id (the lens and parameter "
                  "columns point where search_executions' own do; gap_id points at gaps)",
       all(c_ in gcols for c_ in GAP_SUBJECT) and "gap_id" in secols
       and all(fk_of("gaps", c_) == fk_of("search_executions", c_) and fk_of("gaps", c_)
               for c_ in ("parameter_id", "identity_code", "icf_code", "needs_code", "medical_code"))
       and fk_of("search_executions", "gap_id") == [("gaps", "gap_id", "gap_id")],
       ([c_ for c_ in GAP_SUBJECT if c_ not in gcols], "gap_id" in secols))

A_PAR = scalar("SELECT parameter_id FROM base_parameters WHERE status='active' ORDER BY 1 LIMIT 1")
A_NEED = scalar("SELECT need_code FROM access_needs ORDER BY 1 LIMIT 1")
A_MED = scalar("SELECT medical_code FROM base_taxonomy_medical ORDER BY 1 LIMIT 1")
gap_cli = lambda *a: cli("add-gap", "--category", "EG", "--priority", "P3", "--description", "TASK-FIXTURE gap",  # noqa: E731
                         "--session", S, *a)
stored_gap = lambda c_, gid: dict(c_.execute("SELECT * FROM gaps WHERE gap_id=?", (gid,)).fetchone() or {})  # noqa: E731
n_gaps = lambda c_: c_.execute("SELECT COUNT(*) FROM gaps").fetchone()[0]  # noqa: E731
n_se = lambda c_: c_.execute("SELECT COUNT(*) FROM search_executions").fetchone()[0]  # noqa: E731


def se_gap(c_, exec_id):
    """The gap_id on an execution row, or 'NO-COLUMN' on a database that has no such column (red, not a crash)."""
    try:
        return c_.execute("SELECT gap_id FROM search_executions WHERE exec_id=?", (exec_id,)).fetchone()[0]
    except sqlite3.OperationalError:
        return "NO-COLUMN"



if None in (A_PAR, IDENT, ICF, A_NEED, LANG, JUR):
    skip("T013-02..T013-11", "a registry or the research-scope map is empty")
else:
    flags = ["--parameter", str(A_PAR), "--identity", IDENT, "--icf", ICF, "--needs", A_NEED,
             "--jurisdiction", JUR, "--language", LANG.lower()]
    want = {"parameter_id": A_PAR, "identity_code": IDENT, "icf_code": ICF, "needs_code": A_NEED,
            "jurisdiction": JUR, "language": LANG}
    if A_MED is not None:
        flags += ["--medical", A_MED]
        want["medical_code"] = A_MED
    else:
        skip("T013-03/medical", "base_taxonomy_medical holds no row, so --medical has no code to store")
    with scratch() as c:
        before = n_gaps(c)
        r = gap_cli(*flags)
        gid = json.loads(r.stdout)["gap_id"] if r.returncode == 0 and r.stdout.strip() else None
        row = stored_gap(c, gid) if gid else {}
        record("T013-02", "add-gap stores each subject flag in its own column (the language folded to the case the map "
                          "holds), for a gap that has no cell",
               r.returncode == 0 and n_gaps(c) == before + 1 and all(row.get(k_) == v_ for k_, v_ in want.items()),
               (r.stderr[-200:], {k_: row.get(k_) for k_ in want}))
        r0 = gap_cli()
        g0 = json.loads(r0.stdout)["gap_id"] if r0.returncode == 0 and r0.stdout.strip() else None
        row0 = stored_gap(c, g0) if g0 else {}
        record("T013-03", "add-gap with no subject flag still works and leaves the seven columns NULL",
               g0 is not None and all(row0.get(k_) is None for k_ in GAP_SUBJECT), (r0.stderr[-200:], row0))

        # Each refusal: non-zero exit, the flag or column named, and no row written.
        bad = {"--parameter": ("parameter_id", str(scalar("SELECT MAX(parameter_id) FROM base_parameters") + 1000)),
               "--identity": ("identity_code", IDENT + "-NO-SUCH"), "--icf": ("icf_code", ICF + "-NO-SUCH"),
               "--needs": ("needs_code", A_NEED + "-NO-SUCH"), "--medical": ("medical_code", "NO-SUCH-MEDICAL"),
               "--jurisdiction": ("jurisdiction", JUR + "-NO-SUCH"), "--language": ("--language", "ZZ")}
        for k_, (name_, val_) in bad.items():
            n0 = n_gaps(c)
            rb = gap_cli(k_, val_)
            record(f"T013-04{k_[2:5]}", f"add-gap {k_} {val_!r} is refused naming {name_}, and no row is written",
                   rb.returncode != 0 and name_ in rb.stderr + rb.stdout and n_gaps(c) == n0
                   and "Traceback" not in rb.stderr and "unrecognized arguments" not in rb.stderr,
                   (rb.returncode, (rb.stderr + rb.stdout)[-250:]))
        rb = gap_cli("--identity", "")
        record("T013-05", "add-gap --identity '' (a blank) is refused, not dropped", rb.returncode != 0 and n_gaps(c) == before + 2,
               (rb.stderr + rb.stdout)[-200:])

        # log-search --gap-id
        ls = lambda gap, *a: cli("log-search", "--parameter", str(A_PAR), "--language", LANG, "--query-text",  # noqa: E731
                                 "TASK-FIXTURE probe", "--engine", "manual", "--depth-method", "scoping",
                                 "--prior-expectation", "TASK-FIXTURE: none expected", "--session", S,
                                 "--gap-id", gap, *a)
        e0 = n_se(c)
        rl = ls(gid or "NO-GAP")
        eid = json.loads(rl.stdout)["exec_id"] if rl.returncode == 0 and rl.stdout.strip() else None
        held_gap = se_gap(c, eid) if eid else None
        record("T013-06", "log-search --gap-id stores a held gap id on the execution row",
               eid is not None and n_se(c) == e0 + 1 and gid is not None and held_gap == gid,
               (rl.stderr[-200:], held_gap))
        unheld = db.next_gap_id()                       # numeric ordering: the next id, which no row holds
        e1 = n_se(c)
        ru = ls(unheld, "--dry-run")
        rw = ls(unheld)
        record("T013-07", "log-search --gap-id of a gap nothing holds is refused naming the id (dry run and real), "
                          "and no row is written", ru.returncode != 0 and rw.returncode != 0
               and unheld in ru.stderr + ru.stdout and unheld in rw.stderr + rw.stdout and n_se(c) == e1
               and "unrecognized arguments" not in ru.stderr + rw.stderr,
               ((ru.stderr + ru.stdout)[-250:], n_se(c) - e1))
        rn = cli("log-search", "--parameter", str(A_PAR), "--language", LANG, "--query-text", "TASK-FIXTURE probe",
                 "--engine", "manual", "--depth-method", "scoping", "--prior-expectation", "TASK-FIXTURE: none expected",
                 "--session", S)
        enull = json.loads(rn.stdout)["exec_id"] if rn.returncode == 0 and rn.stdout.strip() else None
        record("T013-08", "a search for no gap still logs, with gap_id NULL",
               enull is not None and se_gap(c, enull) is None, rn.stderr[-200:])
        try:
            via = c.execute("SELECT g.parameter_id FROM search_executions e JOIN gaps g ON g.gap_id=e.gap_id "
                            "WHERE e.exec_id=?", (eid,)).fetchone() if eid else None
        except sqlite3.OperationalError as exc:
            via = exc
        record("T013-09", "the gap a search points at is read back through the pointer, with the parameter it is in",
               isinstance(via, sqlite3.Row) and via[0] == A_PAR, via)

    # The engine's own gap: reached from its cell, never copied into the new columns (rule 5).
    P_ENG = scalar("SELECT parameter_id FROM base_parameters WHERE status='active' AND parameter_id NOT IN "
                   "(SELECT parameter_id FROM specifications) AND parameter_id NOT IN "
                   "(SELECT parameter_id FROM source_value_extractions) ORDER BY 1 LIMIT 1")
    if P_ENG is None:
        skip("T013-10", "every active parameter has a determination or an extraction, so no probe is certain to be pending")
    else:
        with scratch() as c:
            path = os.environ["GUIDEBOOK_DB_PATH"]
            rj = os.path.join(TMP, "t013-assess.json")
            # A lens no earlier case writes (E01-E12 use the default identity and ICF): add a needs code (trap a).
            r = assess(path, P_ENG, SLUG, "--needs", A_NEED, "--report-json", rj)
            rep = json.load(open(rj))[0] if r.returncode == 0 else {}
            cell = c.execute("SELECT parameter_id, identity_code, icf_code, needs_code, gap_register_id "
                             "FROM specifications WHERE gap_register_id=?", (rep.get("gap_register_id") or "",)).fetchone()
            try:
                g = c.execute("SELECT parameter_id, identity_code, icf_code, needs_code, medical_code, jurisdiction, "
                              "language FROM gaps WHERE gap_id=?", (rep.get("gap_register_id") or "",)).fetchone()
            except sqlite3.OperationalError:
                g = None                                   # no such columns: red below, not a crash
            record("T013-10", "an engine-made gap is reached through its cell (specifications.gap_register_id holds the "
                              "parameter and lenses) and its own subject columns stay NULL: the fact is held once",
                   r.returncode == 0 and rep.get("state") == "pending" and cell is not None and g is not None
                   and tuple(cell)[:4] == (P_ENG, IDENT, ICF, A_NEED) and all(v_ is None for v_ in tuple(g)),
                   ((r.stdout + r.stderr)[-250:], cell and tuple(cell), g and tuple(g)))
            pend = c.execute("SELECT parameter_id FROM v_pending WHERE gap_register_id=?", (rep.get("gap_register_id") or "",)).fetchone()
            record("T013-11", "...and v_pending, the cross-stage view, gives that gap its parameter by the join",
                   pend is not None and pend[0] == P_ENG, pend)

h_ls, h_ag = cli("log-search", "--help").stdout, cli("add-gap", "--help").stdout
record("T013-12", "log-search --help lists --gap-id; add-gap --help lists the seven subject flags",
       "--gap-id" in h_ls and all(f_ in h_ag for f_ in ("--parameter", "--identity", "--icf", "--needs", "--medical",
                                                          "--jurisdiction", "--language")), (h_ls[-100:], h_ag[-100:]))

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
clean = scalar(f"SELECT x.ref_id {LIVE} AND e.verification_status='VERIFIED' AND x.ref_id NOT IN (SELECT x.ref_id "
               f"{LIVE} AND ({CLASSES['NO-COVERING-READING']})) LIMIT 1")
if clean is None:
    skip("E07", "no VERIFIED source has every live extraction covered by a reading")
    skip("E08", "as E07")
else:
    rows_of = scalar(f"SELECT COUNT(*) {LIVE} AND x.ref_id=?", clean)
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
for sub in ("red", "green", "two"):
    (fx / sub).mkdir(parents=True)
POISON = ("item_code", "E-08", "axis_code", "population_code", "mode_s_trigger")    # retired by ruling
(fx / "red" / "red.md").write_text("Red fixture. " + ", ".join(f"`{t}`" for t in POISON) + ".\n")
verbs = re.search(r"\{([^}]+)\}", re.sub(r"\s+", "", cli("--help").stdout)).group(1).split(",")
col = [r[1] for r in con.execute("PRAGMA table_info(base_parameters)")][1]
(fx / "green" / "green.md").write_text(f"Green fixture. Read `{col}`, use `{OBSTACLE or VOCAB[0]}`, run "
                                       f"`{next(v for v in verbs if '-' in v)}`; the prose word HIGH-IMPACT "
                                       f"has no ticks.\n")


def vocab(*paths):
    return subprocess.run([sys.executable, str(REPO / "scripts/audit/skill_vocabulary_audit.py"), "--paths",
                           *map(str, paths)], capture_output=True, text=True)


red, green = vocab(fx / "red"), vocab(fx / "green")
record("E09", "skill_vocabulary_audit reports every retired name a skill backticks (R2-16)",
       red.returncode != 0 and all(t in red.stdout for t in POISON), red.stdout[-300:])
record("E10", "...and reports nothing for a live column, a CHECK value, a verb and a prose word",
       green.returncode == 0 and re.search(r"EXAMINED: [1-9]", green.stdout) is not None, green.stdout[-300:])
one = vocab(fx / "green" / "green.md")
record("E13", "--paths takes a FILE and examines it (it examined 0 files and printed PASS, R3-9)",
       one.returncode == 0 and re.search(r"EXAMINED: [1-9]\d* token\(s\) across 1 file", one.stdout) is not None,
       one.stdout[-300:])
none_ = vocab(fx / "no-such-dir")
record("E14", "...and a path that names nothing exits 2 rather than passing having examined nothing",
       none_.returncode == 2, (none_.returncode, none_.stdout[-200:], none_.stderr[-200:]))
(fx / "two" / "defines.md").write_text("| `item_code` | a key this file defines in its own table |\n")
(fx / "two" / "names.md").write_text("Prose that names `item_code` without defining it.\n")
both = vocab(fx / "two")
record("E15", "a table in one file defining a token does not launder it for another file (the allowance is per file)",
       both.returncode != 0 and any("names.md" in ln and "item_code" in ln for ln in both.stdout.splitlines())
       and not any("defines.md" in ln for ln in both.stdout.splitlines() if ln.startswith("  ")), both.stdout[-400:])
ENV_READ = re.compile(r"""environ(?:\.get)?\s*[\[(]\s*["']([A-Z][A-Z0-9_]{7,})["']""")
envname = next((m.group(1) for f in sorted((REPO / "scripts").rglob("*.py")) for m in [ENV_READ.search(f.read_text(errors="replace"))] if m), None)
if envname is None:
    skip("E16", "no script reads an environment variable")
else:
    (fx / "green" / "env.md").write_text(f"Set `{envname}` before the run.\n")
    env_run = vocab(fx / "green" / "env.md")
    record("E16", f"an environment variable the code reads ({envname}, derived from the read) is a home, not an "
                  f"unresolved token", env_run.returncode == 0 and "EXAMINED: 1" in env_run.stdout, env_run.stdout[-300:])

print("Section R3-1/R3-8 readers: scan_debt prints what a block rests on; R3-15: a .md session is stored bare")
with scratch() as c:
    if OBSTACLE is None:
        skip("SD1", "no obstacle")
    else:
        u = new_source()
        hand("UPDATE evidence_sources SET processing_blocked_reason=? WHERE ref_id=?", OBSTACLE, u)   # HAND
        hand_scan(c, u, "abstract")                                                                    # HAND
        n_abs = c.execute("SELECT COUNT(*) FROM v_scan_ledger WHERE status='BLOCKED' AND text_scope='abstract'").fetchone()[0]
        n_unc = c.execute("SELECT COUNT(*) FROM source_scans WHERE text_scope='full' AND pages_read IS NULL").fetchone()[0]
        out = subprocess.run([sys.executable, str(REPO / "scripts/audit/scan_debt.py")], capture_output=True, text=True,
                             env=dict(os.environ)).stdout
        flat = " ".join(out.split())
        record("SD1", "scan_debt names the scope of the reading a BLOCKED pair rests on (blocked and abstract read is "
                      "not blocked and unread), and counts the full readings nothing counted",
               n_abs > 0 and f"abstract {n_abs}" in flat and re.search(rf"nothing counted[^:]*: {n_unc}\b", flat) is not None,
               flat[:500])
    slug_ref = c.execute("SELECT l.slug, l.ref_id FROM source_slug_links l WHERE l.slug IN (SELECT slug FROM slugs "
                         "WHERE status<>'MERGED') LIMIT 1").fetchone()
    dbcore_stem = dbcore.audit(S + ".md")
    record("ST1", "dbcore.audit() and upd() store the bare stem and leave a bare stem alone (R3-15)",
           dbcore_stem["created_by_session"] == S == dbcore.upd(S + ".md")["updated_by_session"]
           == dbcore.audit(S)["created_by_session"], dbcore_stem)
    if slug_ref is None:
        skip("ST2", "no source is linked to a live slug")
    else:
        p = cli("log-mining", "--slug", slug_ref[0], "--ref", slug_ref[1], "--direction", "backward", "--notes",
                "stem probe", "--session", S + ".md")
        got = c.execute("SELECT updated_by_session FROM citation_mining WHERE global_ref_id=? AND slug=?",
                        (slug_ref[1], slug_ref[0])).fetchall()
        record("ST2", "log-mining --session x.md stores x in citation_mining.updated_by_session", p.returncode == 0
               and bool(got) and all(g[0] == S for g in got), (p.stdout + p.stderr)[-200:] or [tuple(g) for g in got])
    if PAIR and slug_ref:
        p = cli("log-search", "--slug", SLUG, "--language", LANG, "--jurisdiction", JUR, "--query-text", "stem probe",
                "--engine", "web", "--depth-method", "scoping", "--prior-expectation", "nothing",
                "--admitted-ref-id", slug_ref[1], "--session", S + ".md")
        try:
            eid = json.loads(p.stdout).get("exec_id")
        except ValueError:
            eid = None
        top = c.execute("SELECT created_by_session FROM search_executions WHERE exec_id=?", (eid,)).fetchall()
        adm = c.execute("SELECT created_by_session FROM search_admissions WHERE exec_id=?", (eid,)).fetchall()
        record("ST3", "log-search --session x.md stores x on the execution row AND on its admission rows",
               bool(top) and bool(adm) and top[0][0] == S and all(a[0] == S for a in adm), (p.stdout + p.stderr)[-250:])
    else:
        skip("ST3", "no declared pair, or no linked source")

print("Section T-008: a claimed number is compared with the quote as a number; a figure in words is filed as a numeral with its wording")
# The quotes are held as one fixture text on a fixture source, so every case below reaches the real
# verbatim check; the numbers in them are literals because the point is how a figure is WRITTEN.
Q = {"dec": "The ramp is to be no higher than 1.2 m.", "time": "The signal stays for a time of 6.0 s.",
     "ratio": "A ramp is to be not steeper than 1:12.", "space": "The width is 1 200 mm at its narrowest point.",
     "in": "A ramp is to have a gradient of 1 in 12.", "std": "AS 1428.1:2021 requires a gradient of 1 in 12.",
     "r20": "A ramp is not steeper than 1:20 where the run exceeds 12 m.", "kanji": "勾配は、十二分の一を超えないこと。",
     "comma": "The length is 1,2 m between the rails.", "thou": "The clearance is 1,200 mm above the floor.",
     "indian": "The area is 1,50,000 square metres.", "eu": "The fee is 1.234,56 euros.", "table": "Rows: 800 750",
     "tab": "Table 2 Not exceeding 5 m 1:15 333 mm Not exceeding 2 m 1:12 166 mm",
     "nl": "Een hellingbaan krijgt vijf procent bij niveauverschillen van 50 cm of groter.",
     "fi": "Luiskan kaltevuus saa olla enintään viisi prosenttia."}
with scratch() as c:
    t8 = new_source(verified=True)
    held_text(t8, "\n".join(Q.values()))
    hand_scan(c, t8, "full")

    def rv(q, claimed, wording=None, **kw):
        """The Refusal text, or None when `_require_verbatim` accepts. claim_type defaults to numerical."""
        return refusal(db._require_verbatim, Q[q], t8, "--claim-text", "T008", claimed_value=claimed,
                       value_as_written=wording, **({"claim_type": "numerical"} | kw))

    refused = [
        ("01", "12 under 'no higher than 1.2 m' (a shifted decimal point)", "dec", "12", None),
        ("02", "0.6 under '6.0 s'", "time", "0.6", None),
        ("03", "1:1 under a quote that states only 1:12", "ratio", "1:1", None),
        ("04", "112 under 1:12 (a digit run across two numbers)", "ratio", "112", None),
        ("05", "120.0 under '1 200 mm'", "space", "120.0", None),
        ("06", "1:8 under '1 in 12'", "in", "1:8", None),
        ("07", "1:12 under '1:20 where the run exceeds 12 m' (its 1 is only an operand of 1:20)", "r20", "1:12", None),
        ("08", "1.200 as a claimed value (asks for the unambiguous form)", "thou", "1.200", None),
        ("09", "1.2 under '1,200 mm' with no wording (the only match is ambiguous)", "thou", "1.2", None),
        ("10", "5 under the Dutch sentence with no wording", "nl", "5", None),
        ("11", "a wording that is not in the quote", "nl", "5", "vijftien procent"),
        ("48", "1:333 under the table row '1:15 333 mm' (333 is a piece, not a whole number)", "tab", "1:333", None),
        ("12", "a wording given when the quote states the number as a numeral", "space", "1200", "1 200"),
    ]
    for n, name, q_, cv, w in refused:
        r = rv(q_, cv, w)
        record(f"T008-{n}", f"refused: {name}", r is not None and "Nothing was written" in r, r)
    r = rv("ratio", "twelve")
    record("T008-13", "'twelve' as a numerical value is refused and the message names --value-as-written",
           r is not None and "--value-as-written" in r and "--claimed-unit" in r, r)
    r = rv("fi", "viisi prosenttia", None, claim_type="range")
    record("T008-14", "words as a range value are refused the same way (both quantity types)",
           r is not None and "--value-as-written" in r, r)
    r = refusal(db._require_verbatim, Q["ratio"], t8, "--claim-text", "T008", claimed_value="twelve")
    record("T008-15", "a call that gives no claim_type is treated as a quantity (twelve is refused)",
           r is not None and "--value-as-written" in r, r)
    for n, name, q_, cv, w in [("16", "12 with the wording '1.2 m' (a clear numeral that states a different figure)", "dec", "12", "1.2 m"),
                               ("17", "1:12 with the wording '1:20' under the 1:20 sentence", "r20", "1:12", "1:20"),
                               ("18", "9999 with the wording '1,200' (ambiguous, but 9999 is not a reading)", "thou", "9999", "1,200")]:
        r = rv(q_, cv, w)
        record(f"T008-{n}", f"refused (item 4, the wording must not state a different figure): {name}",
               r is not None and "figure of its own" in r, r)

    accepted = [
        ("19", "1:15 under a table row '1:15 333 mm' (the 333 belongs to the next column; stored rows state it so)", "tab", "1:15", None),
        ("20", "1.2 under '1,2 m'", "comma", "1.2", None), ("21", "1200 under '1 200 mm'", "space", "1200", None),
        ("22", "1:12 under the kanji sentence", "kanji", "1:12", None), ("23", "1:12 under '1:12'", "ratio", "1:12", None),
        ("24", "1/12 under '1:12'", "ratio", "1/12", None), ("25", "1:12 under '1 in 12'", "in", "1:12", None),
        ("26", "1:12 under 'AS 1428.1:2021 ... 1 in 12' (a cited standard does not block a ratio in words)", "std", "1:12", None),
        ("27", "6 under '6.0 s'", "time", "6", None), ("28", "150000 under '1,50,000'", "indian", "150000", None),
        ("29", "1234.56 under '1.234,56'", "eu", "1234.56", None), ("30", "800 under '800 750'", "table", "800", None),
        ("31", "750 under '800 750'", "table", "750", None), ("32", "1428.1 under 'AS 1428.1:2021'", "std", "1428.1", None),
        ("33", "12 under '1:12' (known residual: 12 is stated)", "ratio", "12", None),
        ("34", "5 with 'vijf procent' under the Dutch sentence", "nl", "5", "vijf procent"),
        ("35", "5 with 'viisi prosenttia' under the Finnish sentence", "fi", "5", "viisi prosenttia"),
        ("36", "1200 with the wording '1,200' under '1,200 mm'", "thou", "1200", "1,200"),
        ("37", "1.2 with the wording '1,200' under '1,200 mm'", "thou", "1.2", "1,200"),
        ("38", "9999 with the wording 'higher' (known residual: a wording with no numeral is the extractor's judgment)", "dec", "9999", "higher"),
    ]
    for n, name, q_, cv, w in accepted:
        res, err = ok(db._require_verbatim, Q[q_], t8, "--claim-text", "T008", claimed_value=cv, value_as_written=w,
                      claim_type="numerical")
        record(f"T008-{n}", f"accepted: {name}", err is None, err)
    res, err = ok(db._require_verbatim, Q["dec"], t8, "--claim-text", "T008", claimed_value="wide", claim_type="qualitative")
    record("T008-39", "accepted: a qualitative value with no number", err is None, err)
    record("T008-40", "dbcore.QUANTITY_CLAIM_TYPES are all in the claim_type CHECK (a renamed type cannot leave it behind)",
           set(dbcore.QUANTITY_CLAIM_TYPES) <= dbcore.check_values(con, "source_value_extractions", "claim_type")
           and dbcore.QUANTITY_CLAIM_TYPES, dbcore.QUANTITY_CLAIM_TYPES)
    record("T008-41", "db._verbatim_norm is gone (its only caller was the digit-substring test)",
           not hasattr(db, "_verbatim_norm"))
    ax = lambda **o: extraction(t8, P_FULL, claim_text=Q["nl"], claimed_value="5", claimed_unit="%",
                                source_section="section T8", loc_section="T8", **o)
    r = refusal(db.insert_extraction, ax(), session=S, dry_run=True, relations=[])
    record("T008-42", "end to end: add-extraction's writer refuses 5 under the Dutch sentence with no wording",
           r is not None and "--value-as-written" in r, r)
    res, err = ok(db.insert_extraction, ax(value_as_written="vijf procent"), session=S, dry_run=False, relations=[])
    stored = c.execute("SELECT value_as_written FROM source_value_extractions WHERE ref_id=?", (t8,)).fetchall()
    record("T008-43", "...and writes it with the wording, in the new column",
           err is None and [tuple(x) for x in stored] == [("vijf procent",)], err or stored)
    hand("UPDATE source_value_extractions SET value_as_written=NULL WHERE ref_id=?", t8)     # HAND: a row written before the column
    eid = c.execute("SELECT extraction_id FROM source_value_extractions WHERE ref_id=?", (t8,)).fetchone()[0]
    r = refusal(db.amend_extraction, eid, "value_as_written", "vijftien procent", "probe", session=S, dry_run=True)
    record("T008-44", "amend-extraction refuses a wording that is not in the stored quote", r is not None, r)
    res, err = ok(db.amend_extraction, eid, "value_as_written", "vijf procent", "T-008 probe", session=S, dry_run=False)
    got = c.execute("SELECT value_as_written, claimed_value FROM source_value_extractions WHERE extraction_id=?", (eid,)).fetchone()
    record("T008-45", "amend-extraction sets the wording on a stored row and leaves its figure alone",
           err is None and tuple(got) == ("vijf procent", "5"), err or tuple(got))
    ref2 = new_source(verified=True)
    held_text(ref2, Q["space"])
    hand_scan(c, ref2, "full")
    db.insert_extraction(extraction(ref2, P_FULL, claim_text=Q["space"], claimed_value="1200", source_section="section T8",
                                    loc_section="T8"), S, dry_run=False, relations=[])
    eid2 = c.execute("SELECT extraction_id FROM source_value_extractions WHERE ref_id=?", (ref2,)).fetchone()[0]
    r = refusal(db.amend_extraction, eid2, "value_as_written", "1 200", "probe", session=S, dry_run=True)
    record("T008-46", "amend-extraction refuses a wording on a row whose quote states the number as a numeral", r is not None, r)
    h = cli("add-extraction", "--help")
    record("T008-47", "add-extraction takes --value-as-written", "--value-as-written" in h.stdout, h.stdout[-200:])


finish()
