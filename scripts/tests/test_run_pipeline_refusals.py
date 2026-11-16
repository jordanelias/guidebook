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
from fractions import Fraction
import hashlib
import inspect
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


sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "scripts" / "research"))
sys.path.insert(0, str(REPO))
from _fixture_log import fixture_log_root  # noqa: E402


def farm(name):
    """A scratch retrieval-log root of symlinks to the tracked sessions, leaving out a pre-admission folder (T-073): a
    fixture source takes the copy's next id, and a folder filed under that id would hand it saved text it never fetched.
    Fixtures written to it leave the tracked log (and every other root) as it was."""
    path = os.path.join(TMP, name)
    return path if os.path.isdir(path) else fixture_log_root(path, DB)


FARM = farm("retrieval-log")
os.environ["GUIDEBOOK_DB_PATH"] = DB
os.environ["GUIDEBOOK_RETRIEVAL_LOG"] = FARM
from schemas.enums import EvidenceMarker  # noqa: E402
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
SRC = {"year": 2020, "evidence_type": "code", "scope": "intrinsic", "verification_status": "UNVERIFIED",
       "source_type": dbcore.schema_choices("evidence_sources", "source_type")[0]}
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
            "source_section": "section 3", "loc_section": "3", "comparator": "="}
    base.update(over)
    # A figure's lens is a set of links since migration 131 (OR-1c); their warrant travels in the payload
    # (lens_basis, lens_basis_text), and the words must be the figure's own: the first word of its claim text.
    base.setdefault("lens_basis", "named_in_text")
    base.setdefault("lens_basis_text", next(iter(re.findall(r"\w+", str(base.get("claim_text") or ""))), ""))
    return base


def lens_of(text):
    """The warrant keyword arguments of derive_extraction for a claim text: the text's own first word."""
    return {"lens_basis": "named_in_text", "lens_basis_text": re.findall(r"\w+", text)[0]}


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
ENUM = dbcore.declared_jurisdictions()    # the base_jurisdictions codes, on the fixture copy
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
            "jurisdiction": JUR, "dry_run": True, "results_found": 1}
    base.update(over)
    return base


r = refusal(db.log_search, **search(slug="no-such-slug"))
record("B01", "log-search refuses an unknown slug by name (not a FOREIGN KEY traceback)",
       r and "slugs" in r, r)
r = refusal(db.log_search, **search(language="ZZ"))
record("J01", "log-search refuses a language lang_jur_map does not hold", r and "lang_jur_map" in r, r)


def scope_flag(lang):
    """`in_research_scope` as the operator reads it: the JSON `log-search --dry-run` prints."""
    p = cli("log-search", "--results-found", "1", "--slug", SLUG, "--language", lang, "--jurisdiction", JUR, "--query-text", "q",
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
_n_con = [scalar(f"SELECT COUNT(*) FROM {t}") for t in ("connections", "connection_targets")]
_rs = {how: refusal(db.delete_connection, who, session=S, dry_run=dry)
       for how, who, dry in (("absent, dry", ABSENT_CON, True), ("absent, for real", ABSENT_CON, False),
                             ("lower case", NEXT_CON.lower(), False), ("padded", f" {NEXT_CON} ", False))}
record("T006-01", "delete-connection refuses an id that is not a connection, for real and under --dry-run and for a case or "
       "whitespace variant of one that is: it names the verb and the id, says nothing was written, points at `db.py connections`, "
       "and the tables are unchanged",
       all(v and "delete-connection:" in v and "Nothing was written" in v and "db.py connections" in v for v in _rs.values())
       and ABSENT_CON in _rs["absent, dry"] and _n_con == [scalar(f"SELECT COUNT(*) FROM {t}")
                                                          for t in ("connections", "connection_targets")], _rs)
with scratch() as c:                   # the copy holds NEXT_CON, written above; the main copy keeps it for later cases
    _P3 = next((p for p in P_ACTIVE if p not in (P1, P2)), None)
    _other, _e2 = ok(db.insert_connection, conn_(description="T006 second connection"),
                     [("parameter_id", P1), ("parameter_id", _P3)], session=S, dry_run=False) if _P3 else (None, "no third parameter")
    _tot = lambda: [c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in ("connections", "connection_targets")]  # noqa: E731
    _before = _tot()
    res, err = ok(db.delete_connection, NEXT_CON, session=S, dry_run=False)
    left = [c.execute(f"SELECT COUNT(*) FROM {t} WHERE con_id=?", (NEXT_CON,)).fetchone()[0]
            for t in ("connections", "connection_targets")]
    kept = [c.execute(f"SELECT COUNT(*) FROM {t} WHERE con_id=?", (_other,)).fetchone()[0]
            for t in ("connections", "connection_targets")] if _other else None
    record("T006-02", "delete-connection deletes the connection it is given and its targets, and only those: a second connection "
           "and its targets are still there", err is None and _e2 is None and left == [0, 0] and kept == [1, 2]
           and _tot() == [_before[0] - 1, _before[1] - 2], (err, _e2, left, kept, _before, _tot()))
    # A connection whose target rows are gone is still a connection: the lookup is in `connections`, not in its targets.
    if _other:
        hand("DELETE FROM connection_targets WHERE con_id=?", _other)
        _res, _e3 = ok(db.delete_connection, _other, session=S, dry_run=False)
        record("T006-03", "a connection with no target rows is still found, and deleted",
               _e3 is None and scalar("SELECT COUNT(*) FROM connections WHERE con_id=?", _other) == 0, _e3)
    else:
        skip("T006-03", "no second connection could be built on the copy")

print("Section T043: a refusal says what to do next")
_CUE = re.compile(r"db\.py |SELECT |--[a-z]|git ls-files")      # a verb, a query, a flag or a listing command
_NOID = "T043-NO-SUCH-ID"
_a_ref = scalar("SELECT ref_id FROM evidence_sources ORDER BY ref_id LIMIT 1")
_a_exec = scalar("SELECT exec_id FROM search_executions e WHERE NOT EXISTS (SELECT 1 FROM search_admissions a "
                 "WHERE a.exec_id = e.exec_id AND a.ref_id = ?) ORDER BY exec_id LIMIT 1", _a_ref)
_a_term = scalar("SELECT term_id FROM base_parameters WHERE status = 'active' ORDER BY parameter_id LIMIT 1")
_a_fnd = scalar("SELECT finding_id FROM adversarial_findings WHERE verdict = 'SUSTAINED' AND disposition IS NOT NULL "
                "ORDER BY finding_id LIMIT 1")
_t043 = [
    ("update-connection, absent id", refusal(db.update_connection_status, ABSENT_CON, "CONSUMED", session=S, dry_run=True),
     "db.py connections"),
    ("update-connection, status outside the CHECK", refusal(db.update_connection_status, NEXT_CON, "BANANA", session=S,
                                                           dry_run=True), "Pass one of them"),
    ("update-conflict, absent id", refusal(db.update_conflict, _NOID, session=S, status="RESOLVED", dry_run=True),
     "db.py conflicts"),
    ("close-gap, status not CLOSED", refusal(db.close_gap, _NOID, "NOT-CLOSED", session=S, dry_run=True), "SELECT DISTINCT status"),
    ("resolve-follow-up, absent id", refusal(db.resolve_follow_up, 2 ** 31, "x", session=S, dry_run=True), "db.py raise-follow-up"),
    ("amend-population-match, absent id", refusal(db.amend_population_match, _NOID, "x", "reason", session=S, dry_run=True),
     "db.py add-population-match"),
    ("update-locator, absent ref", refusal(db.update_locator, _NOID, "RETIRED", session=S, reason="reason", dry_run=True),
     "db.py add-locator"),
    ("a transcript path outside transcripts/", refusal(db._resolve_transcript_path, "../governance/x", "reviewer_transcript"),
     "git ls-files transcripts/"),
    ("add-connection, a parameter that does not exist", refusal(db.insert_connection, conn_(),
                                                                [("parameter_id", 2 ** 30), ("parameter_id", P1)],
                                                                session=S, dry_run=True), "SELECT parameter_id FROM base_parameters"),
]
if _a_exec and _a_ref:
    _t043.append(("unlink-admission, no such edge", refusal(db.unlink_admission, _a_exec, _a_ref, "reason", session=S, dry_run=True),
                  "SELECT exec_id FROM search_admissions"))
if _a_term:
    _t043.append(("decline-parameter on a term that is a parameter", refusal(db.decline_parameter, _a_term, "reason", session=S,
                                                                             dry_run=True), "db.py retire-parameter"))
if _a_fnd and _a_ref:
    _t043.append(("dispose-adversarial-finding, already disposed", refusal(db.dispose_adversarial_finding, _a_fnd, "REPAIRED",
                                                                           _a_ref, session=S, dry_run=True),
                  "SELECT disposition FROM adversarial_findings"))
_verb_ok = {}
def _verb_exists(msg):
    """Every `db.py <verb>` a message names is a verb the CLI has (its --help exits 0)."""
    for v in re.findall(r"db\.py ([a-z][a-z-]+)", msg or ""):
        if v not in _verb_ok:
            _verb_ok[v] = subprocess.run([sys.executable, str(REPO / "scripts" / "db.py"), v, "--help"],
                                         capture_output=True, text=True).returncode == 0
    return all(_verb_ok[v] for v in re.findall(r"db\.py ([a-z][a-z-]+)", msg or ""))
for _i, (_what, _msg, _tok) in enumerate(_t043, 1):
    record(f"T043-{_i:02d}", f"{_what}: the refusal names the way forward ({_tok!r}), and every `db.py` verb it names exists",
           bool(_msg) and _tok in _msg and bool(_CUE.search(_msg)) and _verb_exists(_msg), _msg)
for _need, _label in ((_a_exec and _a_ref, "unlink-admission"), (_a_term, "decline-parameter"), (_a_fnd and _a_ref, "dispose-adversarial-finding")):
    if not _need:
        skip("T043", f"{_label}: the live database offers no row to build the refusal on")

print("Section T021: a question about a published cell is an open gate with no tier")
_P_Q = next((p for p in P_ACTIVE), None)
_ICF = scalar("SELECT icf_code FROM base_icf ORDER BY icf_code LIMIT 1")
_NEED = scalar("SELECT need_code FROM access_needs ORDER BY need_code LIMIT 1")
if _P_Q is None or _ICF is None:
    skip("T021", "no active parameter or ICF code on the live database to build the question on")
else:
    _text = "a reader asks whether this value suits a person who uses a long cane"
    with scratch() as c:
        _n0 = c.execute("SELECT COUNT(*) FROM determination_gates").fetchone()[0]
        res, err = ok(db.raise_determination_gate, parameter_id=_P_Q, verdict="QUESTION", detail=_text, icf=_ICF,
                      needs=_NEED, session=S, dry_run=False)
        row = c.execute("SELECT verdict, trigger_tier, trigger_evidence_type, trigger_ref_id, icf_code, needs_code, "
                        "detail, raised_by_session FROM determination_gates WHERE gate_id=?",
                        (res["gate_id"] if res else -1,)).fetchone()
        record("T021-06", "a QUESTION is raised with no tier, no evidence type and no source, names the lens codes it was given, "
               "keeps the objection's words and the session, and is listed by v_open_determination_gates",
               err is None and row is not None and tuple(row) == ("QUESTION", None, None, None, _ICF, _NEED, _text, S)
               and c.execute("SELECT COUNT(*) FROM v_open_determination_gates WHERE gate_id=?", (res["gate_id"],)).fetchone()[0] == 1
               and c.execute("SELECT COUNT(*) FROM determination_gates").fetchone()[0] == _n0 + 1, (err, row))
        _rs = {
            "a tier": refusal(db.raise_determination_gate, parameter_id=_P_Q, verdict="QUESTION", detail=_text,
                              trigger_tier=1, session=S, dry_run=True),
            "an evidence type": refusal(db.raise_determination_gate, parameter_id=_P_Q, verdict="QUESTION", detail=_text,
                                        trigger_evidence_type="clinical", session=S, dry_run=True),
            "a source": refusal(db.raise_determination_gate, parameter_id=_P_Q, verdict="QUESTION", detail=_text,
                                trigger_ref_id=_a_ref, session=S, dry_run=True)}
        record("T021-07", "a QUESTION is refused a tier, an evidence type or a source, naming what to do instead",
               all(v and "QUESTION" in v and "--detail" in v for v in _rs.values()), _rs)
        _other = refusal(db.raise_determination_gate, parameter_id=_P_Q, verdict="CONTRADICTS", detail=_text,
                         session=S, dry_run=True)
        record("T021-08", "every other verdict still needs its tier (or a source to read it from)",
               _other and "--trigger-tier" in _other, _other)
        _bad = refusal(db.raise_determination_gate, parameter_id=_P_Q, verdict="QUESTION", detail=_text,
                       icf="ICF-NO-SUCH", session=S, dry_run=True)
        record("T021-09", "a lens code that does not exist is refused, naming the table and the listing query",
               _bad and "--icf" in _bad and "base_icf" in _bad and "SELECT icf_code FROM base_icf" in _bad, _bad)
        res2, err2 = ok(db.resolve_determination_gate, gate_id=res["gate_id"], rationale="answered in the ledger",
                        session=S, dry_run=False)
        record("T021-10", "a question is closed only through resolve-determination-gate with a rationale, and then leaves the open view",
               err2 is None and c.execute("SELECT COUNT(*) FROM v_open_determination_gates WHERE gate_id=?",
                                          (res["gate_id"],)).fetchone()[0] == 0, err2)
        _aud = subprocess.run([sys.executable, str(REPO / "scripts" / "audit" / "derivation_handshake_integrity.py"),
                               "--db", os.environ["GUIDEBOOK_DB_PATH"]], capture_output=True, text=True)
        _gn = c.execute("SELECT COUNT(*), SUM(resolved_at IS NULL) FROM determination_gates").fetchone()
        record("T021-12", "the handshake audit reads a database holding a QUESTION (NULL tier) without failing and counts the gates it read",
               _aud.returncode == 0 and f"gates: {_gn[0]} ({_gn[1]} open)" in _aud.stdout, (_aud.returncode, _aud.stdout[-300:], _aud.stderr[-200:]))
        _hand = None
        try:
            c.execute("INSERT INTO determination_gates (parameter_id, verdict, trigger_tier, trigger_evidence_type, detail, "
                      "raised_at, raised_by_session) VALUES (?, 'QUESTION', 1, 'clinical', 'x', 'now', 'x')", (_P_Q,))
        except sqlite3.IntegrityError as exc:
            _hand = str(exc)
        record("T021-11", "the schema itself refuses a QUESTION that carries a tier", _hand is not None, _hand)

print("Section T025: language-jurisdiction pairs and identity codes are written by verbs, each pointing at an owner entry")
_led = pathlib.Path(dbcore.LEDGER_PATH).read_text(encoding="utf-8").splitlines()
_heads = [l[3:] for l in _led if l.startswith("## ")]
_dated = [h for h in _heads if re.search(r"\d{4}-\d{2}-\d{2}", h) and _heads.count(h) == 1]
_OWNER_H = next((h for h in _dated if h.startswith(dbcore.LEDGER_OWNER_PREFIX)), None)
_OTHER_H = next((h for h in _dated if not h.startswith((dbcore.LEDGER_OWNER_PREFIX, dbcore.LEDGER_DELEGATED_PREFIX))), None)
_DELEG_H = next((h for h in _heads if h.startswith(dbcore.LEDGER_DELEGATED_PREFIX) and _heads.count(h) == 1), None)
_jur = [r[0] for r in q("SELECT jurisdiction_code FROM base_jurisdictions ORDER BY 1")]
_pair = next(((l, j) for (l,) in q("SELECT DISTINCT language FROM lang_jur_map ORDER BY 1") for j in _jur
              if not scalar("SELECT 1 FROM lang_jur_map WHERE language=? AND jurisdiction=?", l, j)), None)
_held = q("SELECT language, jurisdiction FROM lang_jur_map ORDER BY 1, 2 LIMIT 1")[0]
_PAR = scalar("SELECT identity_code FROM base_taxonomy_identity WHERE status='active' ORDER BY identity_code LIMIT 1")
_CAT = scalar("SELECT category FROM base_taxonomy_identity WHERE category IS NOT NULL ORDER BY 1 LIMIT 1")
if not (_OWNER_H and _OTHER_H and _DELEG_H and _pair and _PAR and _CAT):
    skip("T025", "the live ledger or database offers no owner heading, delegated heading, free pair or active code")
else:
    _R = dict(session=S, dry_run=False)
    with scratch() as c:
        res, err = ok(db.add_lang_jur_pair, _pair[0], _pair[1], "PRIMARY", "T025 fixture", _OWNER_H, **_R)
        _r = c.execute("SELECT role, notes, scope_status, created_by_session FROM lang_jur_map WHERE language=? AND "
                       "jurisdiction=?", _pair).fetchone()
        record("T025-01", "add-lang-jur-pair writes one pair with scope_status NULL (owed), the notes and a session stamp, and reports "
               "new_language false for a language the map holds and the approval it read",
               err is None and tuple(_r) == ("PRIMARY", "T025 fixture", None, S) and res["new_language"] is False
               and res["approval_ref"] == _OWNER_H, (err, _r, res))
        _NEWLANG = "ZZTQ"
        res, err = ok(db.add_lang_jur_pair, _NEWLANG, _pair[1], "SECONDARY", None, _OWNER_H, **_R)
        record("T025-02", "a language the map does not hold is admitted only through the verb and reported as new_language true",
               err is None and res["new_language"] is True and c.execute("SELECT COUNT(*) FROM lang_jur_map WHERE language=?", (_NEWLANG,)).fetchone()[0] == 1, err)
        _rs = {
            "lower case": refusal(db.add_lang_jur_pair, "zz", _pair[1], "PRIMARY", None, _OWNER_H, session=S, dry_run=True),
            "jurisdiction not held": refusal(db.add_lang_jur_pair, "ZZTR", "ZZ-NOT-A-CODE", "PRIMARY", None, _OWNER_H, session=S, dry_run=True),
            "role outside the CHECK": refusal(db.add_lang_jur_pair, "ZZTR", _pair[1], "BANANA", None, _OWNER_H, session=S, dry_run=True),
            "pair held": refusal(db.add_lang_jur_pair, _held[0], _held[1], "PRIMARY", None, _OWNER_H, session=S, dry_run=True),
            "no date": refusal(db.add_lang_jur_pair, "ZZTR", _pair[1], "PRIMARY", None, "an undated heading", session=S, dry_run=True),
            "not exactly one": refusal(db.add_lang_jur_pair, "ZZTR", _pair[1], "PRIMARY", None, "2026-01-01 no such entry", session=S, dry_run=True),
            "delegated": refusal(db.add_lang_jur_pair, "ZZTR", _pair[1], "PRIMARY", None, _DELEG_H, session=S, dry_run=True)}
        record("T025-03", "add-lang-jur-pair refuses a lower-case language, a jurisdiction not held, a role outside the CHECK, a held pair, "
               "an approval with no date, one that is not exactly one entry and a delegated resolution, each by name",
               all(_rs.values()) and "upper case" in _rs["lower case"] and "ZZ-NOT-A-CODE" in _rs["jurisdiction not held"]
               and "CHECK" in _rs["role outside the CHECK"] and "already held" in _rs["pair held"] and "carries no date" in _rs["no date"] and "exactly one" in _rs["not exactly one"]
               and "delegated resolution" in _rs["delegated"], _rs)
        _scope = c.execute("SELECT scope_status FROM lang_jur_map WHERE language=? AND jurisdiction=?", _pair).fetchone()[0]
        res, err = ok(db.set_pair_scope, _pair[0], _pair[1], "in-scope", _OWNER_H, **_R)
        _now = c.execute("SELECT scope_status FROM lang_jur_map WHERE language=? AND jurisdiction=?", _pair).fetchone()[0]
        record("T025-04", "set-pair-scope moves one held pair's scope_status and reports the old value",
               err is None and _scope is None and _now == "in-scope" and res["scope_status_was"] is None, (err, _scope, _now))
        _rs = [refusal(db.set_pair_scope, _pair[0], _pair[1], "in-scope", _OWNER_H, session=S, dry_run=True),
               refusal(db.set_pair_scope, "ZZTR", "ZZ", "in-scope", _OWNER_H, session=S, dry_run=True),
               refusal(db.set_pair_scope, _pair[0], _pair[1], "BANANA", _OWNER_H, session=S, dry_run=True)]
        record("T025-05", "set-pair-scope refuses the value the pair already has, a pair not held and a value outside the CHECK",
               all(_rs) and "already" in _rs[0] and "not held" in _rs[1] and "CHECK" in _rs[2], _rs)
        _CODE = "T025ZZ"
        res, err = ok(db.add_identity, _CODE, "T025 fixture group", _CAT, "a fixture", _PAR, _OWNER_H, **_R)
        _i = c.execute("SELECT display_name, category, description, parent_code, status, created_at, updated_at FROM "
                       "base_taxonomy_identity WHERE identity_code=?", (_CODE,)).fetchone()
        record("T025-06", "add-identity writes one active code under a held parent with its name, category, description and stamps",
               err is None and _i["display_name"] == "T025 fixture group" and _i["category"] == _CAT and _i["parent_code"] == _PAR
               and _i["description"] == "a fixture"
               and _i["status"] == "active" and _i["created_at"] and _i["updated_at"], (err, dict(_i) if _i else None))
        _rs = [refusal(db.add_identity, "t025lower", "x", _CAT, "d", None, _OWNER_H, session=S, dry_run=True),
               refusal(db.add_identity, _CODE, "x", _CAT, "d", None, _OWNER_H, session=S, dry_run=True),
               refusal(db.add_identity, "T025Y", "x", "BANANA", "d", None, _OWNER_H, session=S, dry_run=True),
               refusal(db.add_identity, "T025Y", "x", _CAT, "d", "NO-SUCH-PARENT", _OWNER_H, session=S, dry_run=True),
               refusal(db.add_identity, "T025Y", "", _CAT, "d", None, _OWNER_H, session=S, dry_run=True),
               refusal(db.add_identity, "T025Y", "x", _CAT, "d", None, _DELEG_H, session=S, dry_run=True),
               refusal(db.add_identity, "T025 Y", "x", _CAT, "d", None, _OWNER_H, session=S, dry_run=True),
               refusal(db.add_identity, "T025Y", "x", _CAT, " ", None, _OWNER_H, session=S, dry_run=True)]
        record("T025-07", "add-identity refuses a lower-case code, a held code, a category outside the CHECK, a parent not held, a blank name "
               "and a delegated approval",
               all(_rs) and "upper case" in _rs[0] and "already held" in _rs[1] and "CHECK" in _rs[2] and "not held" in _rs[3]
               and "blank" in _rs[4] and "delegated" in _rs[5] and "no space" in _rs[6] and "blank" in _rs[7], _rs)
        c.execute("UPDATE base_taxonomy_identity SET status='deprecated', superseded_by_need=(SELECT need_code FROM access_needs LIMIT 1) "
                  "WHERE identity_code=?", (_CODE,)); c.commit()
        _dep = refusal(db.add_identity, "T025Y", "x", _CAT, "d", _CODE, _OWNER_H, session=S, dry_run=True)
        record("T025-07b", "add-identity refuses a parent that is held but not active", bool(_dep) and "deprecated" in _dep, _dep)
        c.execute("UPDATE base_taxonomy_identity SET status='active', superseded_by_need=NULL WHERE identity_code=?", (_CODE,)); c.commit()
        _no_owner = {"add-lang-jur-pair": refusal(db.add_lang_jur_pair, "ZZTR", _pair[1], "PRIMARY", None, _OTHER_H, session=S, dry_run=True),
                     "set-pair-scope": refusal(db.set_pair_scope, _pair[0], _pair[1], "scoped-out", _OTHER_H, session=S, dry_run=True),
                     "add-identity": refusal(db.add_identity, "T025Y", "x", _CAT, "d", None, _OTHER_H, session=S, dry_run=True),
                     "amend-identity": refusal(db.amend_identity, _CODE, "x", None, None, _OTHER_H, "r", session=S, dry_run=True)}
        _deleg = {"set-pair-scope": refusal(db.set_pair_scope, _pair[0], _pair[1], "scoped-out", _DELEG_H, session=S, dry_run=True),
                  "amend-identity": refusal(db.amend_identity, _CODE, "x", None, None, _DELEG_H, "r", session=S, dry_run=True)}
        record("T025-07c", "each of the four verbs refuses a dated, unique ledger heading that is not the owner's (a session, a referral, a correction) "
               "and set-pair-scope and amend-identity refuse a delegated resolution",
               all(v and "not an entry that records the owner" in v for v in _no_owner.values())
               and all(v and "delegated resolution" in v for v in _deleg.values()), (_no_owner, _deleg))
        res, err = ok(db.amend_identity, _CODE, "T025 renamed", None, None, _OWNER_H, "T025 fixture", **_R)
        _name = c.execute("SELECT display_name FROM base_taxonomy_identity WHERE identity_code=?", (_CODE,)).fetchone()[0]
        res2, err2 = ok(db.amend_identity, _CODE, "T025 renamed", None, None, _OWNER_H, "again", **_R)
        record("T025-08", "amend-identity changes the given field and prints the value it replaces; the same value again changes nothing",
               err is None and res["changed"] and res["replaced"] == {"display_name": "T025 fixture group"} and _name == "T025 renamed"
               and err2 is None and res2["changed"] is False, (err, res, err2, res2))
        _cats = sorted(dbcore.schema_choices("base_taxonomy_identity", "category"))
        _cat2 = next((x for x in _cats if x != _CAT), None)
        res3, err3 = ok(db.amend_identity, _CODE, None, "T025 new description", _cat2, _OWNER_H, "T025 fixture", **_R)
        _i2 = c.execute("SELECT description, category FROM base_taxonomy_identity WHERE identity_code=?", (_CODE,)).fetchone()
        record("T025-08b", "amend-identity changes a description and a category, printing both replaced values",
               err3 is None and tuple(_i2) == ("T025 new description", _cat2)
               and res3["replaced"] == {"description": "a fixture", "category": _CAT}, (err3, res3, tuple(_i2)))
        res4, err4 = ok(db.set_pair_scope, _pair[0], _pair[1], "scoped-out", _OWNER_H, **_R)
        record("T025-05b", "set-pair-scope sets scoped-out from in-scope and reports the old value", err4 is None
               and res4["scope_status_was"] == "in-scope" and res4["scope_status"] == "scoped-out", (err4, res4))
        _rs = [refusal(db.amend_identity, _CODE, None, None, None, _OWNER_H, "r", session=S, dry_run=True),
               refusal(db.amend_identity, _CODE, " ", None, None, _OWNER_H, "r", session=S, dry_run=True),
               refusal(db.amend_identity, "NO-SUCH-CODE", "x", None, None, _OWNER_H, "r", session=S, dry_run=True),
               refusal(db.amend_identity, _CODE, "x", None, None, _OWNER_H, "", session=S, dry_run=True),
               refusal(db.amend_identity, _CODE, None, None, "BANANA", _OWNER_H, "r", session=S, dry_run=True)]
        record("T025-09", "amend-identity refuses no field, a blank value, a code not held and a blank reason",
               all(_rs) and "at least one" in _rs[0] and "blank" in _rs[1] and "not held" in _rs[2] and "--reason" in _rs[3]
               and "CHECK" in _rs[4], _rs)
        # a sub-national code can never satisfy a pair: refused, naming the country (fixture row, HAND on the copy)
        _ctry = scalar("SELECT jurisdiction_code FROM base_jurisdictions WHERE kind='country' ORDER BY 1 LIMIT 1")
        if _ctry:
            c.execute("INSERT INTO base_jurisdictions (jurisdiction_code, kind, parent_code, admission_ref, created_at, created_by_session) "
                      "VALUES (?, 'sub-national', ?, 'TASK-FIXTURE', '2026-11-15', 'syn')", (_ctry + "-TFX", _ctry)); c.commit()
            _sn = refusal(db.add_lang_jur_pair, _pair[0], _ctry + "-TFX", "PRIMARY", None, _OWNER_H, session=S, dry_run=True)
            record("T025-09b", "add-lang-jur-pair refuses a sub-national code, naming the country it counts toward",
                   bool(_sn) and "sub-national" in _sn and repr(_ctry) in _sn, _sn)
        else:
            skip("T025-09b", "no country row to hang a sub-national fixture on")
        _wt = set(dbcore.writable_tables(c))
        record("T025-10", "lang_jur_map and base_taxonomy_identity are in the captured set (a change to either reaches a migration)",
               {"lang_jur_map", "base_taxonomy_identity"} <= _wt, sorted(_wt))

print("Section T027: a source's code currency is written by amend-source, stamped, and its edition by correct-source")
_cv = dbcore.code_currency_vocabulary()
_ref27 = scalar("SELECT ref_id FROM evidence_sources WHERE code_currency_status IS NULL AND tier >= 4 AND superseded_by_ref_id IS NULL ORDER BY ref_id LIMIT 1")
_ref27_t1 = scalar("SELECT ref_id FROM evidence_sources WHERE tier < 4 ORDER BY ref_id LIMIT 1")
_ref27_tomb = scalar("SELECT ref_id FROM evidence_sources WHERE superseded_by_ref_id IS NOT NULL ORDER BY ref_id LIMIT 1")
if not _cv or not _ref27:
    skip("T027", "no readable enum in governance/tier-system.md or no source without a currency status")
else:
    with scratch() as c:
        _before_mis = c.execute("SELECT metadata_integrity_status FROM evidence_sources WHERE ref_id=?", (_ref27,)).fetchone()[0]
        _before = c.execute("SELECT code_currency_status, code_currency_verified_at, code_currency_verified_by_session "
                            "FROM evidence_sources WHERE ref_id=?", (_ref27,)).fetchone()
        res, err = ok(db.amend_source, _ref27, "code_currency_status", _cv[0], "T027 fixture: edition checked", session=S, dry_run=False)
        _row = c.execute("SELECT code_currency_status, code_currency_verified_at, code_currency_verified_by_session, "
                         "metadata_integrity_detail FROM evidence_sources WHERE ref_id=?", (_ref27,)).fetchone()
        record("T027-01", "amend-source sets code_currency_status to a member of the enum governance/tier-system.md ratifies, stamps "
               "code_currency_verified_at and _by_session itself, and ledgers the replaced value with the reason",
               err is None and tuple(_before) == (None, None, None) and _row[0] == _cv[0] and bool(_row[1])
               and _row[2] == dbcore.session_stem(S) and "code_currency_status RECORDED (T027 fixture: edition checked)" in _row[3] and "code_currency_status CORRECTED" not in _row[3], (err, tuple(_row)))
        res, err = ok(db.amend_source, _ref27, "code_currency_status", _cv[0], "again", session=S, dry_run=False)
        record("T027-02", "the same value again changes nothing", err is None and res["changed"] is False, (err, res))
        _rs = {"outside the enum": refusal(db.amend_source, _ref27, "code_currency_status", "CURRENT-ISH", "r", session=S, dry_run=True),
               "stamp typed": refusal(db.amend_source, _ref27, "code_currency_verified_at", "2026-01-01", "r", session=S, dry_run=True),
               "edition by hand": refusal(db.amend_source, _ref27, "edition", "2nd", "r", session=S, dry_run=True)}
        record("T027-03", "a value outside the enum is refused naming the enum; the stamp columns are not amendable; edition is a bibliographic "
               "field and is sent to correct-source",
               all(_rs.values()) and all(v in _rs["outside the enum"] for v in _cv) and "not an amendable" in _rs["stamp typed"]
               and "correct-source" in _rs["edition by hand"], _rs)
        _st = {"tier below 4": refusal(db.amend_source, _ref27_t1, "code_currency_status", _cv[0], "r", session=S, dry_run=True) if _ref27_t1 else "n/a",
               "tombstone": refusal(db.amend_source, _ref27_tomb, "code_currency_status", _cv[0], "r", session=S, dry_run=True) if _ref27_tomb else "n/a"}
        record("T027-06", "code currency is refused for a source below tier 4 and for a tombstone, and writing it does not flip metadata_integrity_status",
               bool(_st["tier below 4"]) and ("T4-T6" in _st["tier below 4"] or _st["tier below 4"] == "n/a")
               and bool(_st["tombstone"]) and ("tombstone" in _st["tombstone"] or _st["tombstone"] == "n/a")
               and _before_mis == c.execute("SELECT metadata_integrity_status FROM evidence_sources WHERE ref_id=?", (_ref27,)).fetchone()[0], (_st,))
        _stamp0 = c.execute("SELECT code_currency_verified_at FROM evidence_sources WHERE ref_id=?", (_ref27,)).fetchone()[0]
        res, err = ok(db.amend_source, _ref27, "code_currency_notes", "checked against the issuing body's page", "T027 note", session=S, dry_run=False)
        _n = c.execute("SELECT code_currency_notes, code_currency_verified_at FROM evidence_sources WHERE ref_id=?", (_ref27,)).fetchone()
        record("T027-04", "code_currency_notes is amendable on its own and does not move the verification stamp",
               err is None and _n[0] == "checked against the issuing body's page" and _n[1] == _stamp0, (err, tuple(_n)))
    record("T027-05", "edition is a field correct-source takes from the logged payload", "edition" in db._CORRECTABLE, sorted(db._CORRECTABLE))
    record("T027-07", "original_title is a field correct-source takes from the logged payload (Crossref original-title), and amend-source sends it there",
           "original_title" in db._CORRECTABLE and "correct-source" in (refusal(db.amend_source, _ref27, "original_title", "x", "r", session=S, dry_run=True) or ""),
           sorted(db._CORRECTABLE))

print("Section T034: cell-status answers where a cell stands, from the tables, and writes nothing")
_tabs = [r[0] for r in q("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
_P_none = scalar("SELECT parameter_id FROM base_parameters WHERE parameter_id NOT IN "
                 "(SELECT parameter_id FROM source_value_extractions) ORDER BY parameter_id LIMIT 1")
_P_fig = scalar("SELECT parameter_id FROM source_value_extractions GROUP BY parameter_id ORDER BY COUNT(*) DESC LIMIT 1")
if _P_none is None or _P_fig is None:
    skip("T034", "the live database has no parameter without figures and one with")
else:
    _cnt = lambda: [scalar(f'SELECT COUNT(*) FROM "{t}"') for t in _tabs]          # noqa: E731
    _n0 = _cnt()
    d_none, e1 = ok(db.cell_status, _P_none)
    d_fig, e2 = ok(db.cell_status, _P_fig)
    record("T034-01", "a parameter with no figures reports nothing held at judgment and evidence and no determination, and its owed pairs are read "
           "from the scope",
           e1 is None and d_none["stages"]["judgment"]["held"] == [] and d_none["stages"]["evidence"]["held"] == []
           and d_none["stages"]["specification"]["held"] == []
           and sorted(d_none["stages"]["research"]["owed"]["scope_unrecorded"] + d_none["stages"]["research"]["owed"]["pairs_in_scope"])
           == sorted(f"{a}/{b}" for a, b in q("SELECT language, jurisdiction FROM lang_jur_map WHERE COALESCE(scope_status, 'in-scope') <> 'scoped-out' "
                                              "AND NOT (language, jurisdiction) IN (SELECT UPPER(language), jurisdiction FROM search_executions "
                                              "WHERE parameter_id = ? AND deferred_reason IS NULL)", _P_none)), e1)
    _judged = [r[0] for r in q("SELECT extraction_id FROM source_value_extractions WHERE parameter_id=? ORDER BY extraction_id", _P_fig)]
    _led = {st: [r[0] for r in q("SELECT ref_id FROM v_scan_ledger WHERE parameter_id=? AND status=? ORDER BY ref_id", _P_fig, st)]
            for st in ("EXTRACTED", "STATED-ABSENT", "READ-NOTHING-FOUND", "NOT-READ", "READ-PARTIAL")}
    _st = d_fig["stages"] if d_fig else {}
    record("T034-02", "a parameter with figures lists every extraction id at judgment, and the scan ledger's statuses at evidence "
           "(held = extracted or stated absent, examined empty = read nothing found, never examined = not read, owed = read in part only)",
           e2 is None and _st["judgment"]["held"] == _judged
           and _st["evidence"]["held"] == sorted(_led["EXTRACTED"] + _led["STATED-ABSENT"])
           and _st["evidence"]["examined_empty"] == _led["READ-NOTHING-FOUND"]
           and _st["evidence"]["never_examined"] == _led["NOT-READ"]
           and _st["evidence"]["owed"]["read_in_part_only"] == _led["READ-PARTIAL"], (e2, len(_judged)))
    _lens = q("SELECT l.identity_code, l.extraction_id FROM v_live_lens_links l JOIN source_value_extractions e ON e.extraction_id = l.extraction_id "
              "WHERE e.parameter_id=? AND l.identity_code IS NOT NULL ORDER BY l.extraction_id", _P_fig)
    if _lens:
        _code = _lens[0][0]
        d_l, e3 = ok(db.cell_status, _P_fig, identity=_code)
        _want = [r[0] for r in q("SELECT e.extraction_id FROM source_value_extractions e WHERE e.parameter_id=? AND EXISTS (SELECT 1 FROM "
                                 "v_live_lens_links l WHERE l.extraction_id=e.extraction_id AND l.identity_code=?) ORDER BY 1", _P_fig, _code)]
        record("T034-03", "a lens narrows the figures to those carrying that code, and no other stage's list is made up",
               e3 is None and d_l["stages"]["judgment"]["held"] == _want and 0 < len(_want) <= len(_judged), (e3, _want[:5]))
    else:
        skip("T034-03", "no figure of the chosen parameter carries an identity code")
    _rs = [refusal(db.cell_status, 2 ** 30), refusal(db.cell_status, _P_fig, identity="NO-SUCH-CODE"),
           refusal(db.cell_status, _P_fig, jurisdiction="ZZ-NOT-A-CODE"), refusal(db.cell_status, _P_fig, language="ZZNOLANG")]
    record("T034-04", "an unknown parameter, lens code, jurisdiction or language is refused, naming the listing query or table",
           all(_rs) and "SELECT parameter_id" in _rs[0] and "base_taxonomy_identity" in _rs[1] and "ZZ-NOT-A-CODE" in _rs[2] and "lang_jur_map" in _rs[3], _rs)
    record("T034-05", "the verb writes nothing: every table holds as many rows after the calls as before", _n0 == _cnt(), (_n0, _cnt()))
    with scratch() as c:
        _pr = c.execute("SELECT language, jurisdiction FROM lang_jur_map WHERE NOT (language, jurisdiction) IN (SELECT UPPER(language), "
                        "jurisdiction FROM search_executions WHERE parameter_id=? AND deferred_reason IS NULL) ORDER BY 1, 2 LIMIT 1", (_P_none,)).fetchone()
        _key = f"{_pr[0]}/{_pr[1]}"
        _seen = {}
        for st in ("scoped-out", "in-scope", None):
            c.execute("UPDATE lang_jur_map SET scope_status=? WHERE language=? AND jurisdiction=?", (st, *_pr))
            c.commit()
            r = db.cell_status(_P_none)["stages"]["research"]
            _seen[st] = (_key in r["never_examined"]["pairs_scoped_out"], _key in r["owed"]["pairs_in_scope"], _key in r["owed"]["scope_unrecorded"])
        record("T034-06", "a pair never searched is reported by its recorded scope: scoped out = never examined, in scope = owed, NULL = scope unrecorded",
               _seen == {"scoped-out": (True, False, False), "in-scope": (False, True, False), None: (False, False, True)}, _seen)

# T-034 repairs after the critic: searches are keyed on a slug, and the lens narrows every stage it can.
if _P_fig is not None:
    _d = db.cell_status(_P_fig)["stages"]["research"]
    _want = sorted(r[0] for r in q("SELECT exec_id FROM search_executions WHERE deferred_reason IS NULL AND (parameter_id = ? OR slug IN "
                                   "(SELECT DISTINCT slug FROM source_value_extractions WHERE parameter_id = ? AND slug IS NOT NULL))", _P_fig, _P_fig))
    record("T034-07", "the research stage lists the searches logged against the parameter or any slug its figures carry (found something + found nothing)",
           sorted(_d["held"] + _d["examined_empty"]) == _want, (len(_want), len(_d["held"]), len(_d["examined_empty"])))
    _lc = q("SELECT l.identity_code FROM v_live_lens_links l JOIN source_value_extractions e ON e.extraction_id = l.extraction_id WHERE e.parameter_id = ? "
            "AND l.identity_code IS NOT NULL GROUP BY 1 ORDER BY COUNT(*) LIMIT 1", _P_fig)
    if _lc:
        _code = _lc[0][0]
        _n = db.cell_status(_P_fig, identity=_code)["stages"]
        _refs = {r[0] for r in q("SELECT DISTINCT e.ref_id FROM source_value_extractions e JOIN v_live_lens_links l ON l.extraction_id = e.extraction_id "
                                 "WHERE e.parameter_id = ? AND l.identity_code = ?", _P_fig, _code)}
        _gate_other = [r[0] for r in q("SELECT gate_id FROM v_open_determination_gates WHERE parameter_id = ? AND identity_code IS NOT NULL AND identity_code <> ?", _P_fig, _code)]
        record("T034-08", "a lens narrows the evidence held to the sources of its figures, drops an open gate that names a different code, and says which lists it did not narrow",
               set(_n["evidence"]["held"]) <= _refs and not (set(_gate_other) & set(_n["specification"]["owed"]["open_gates"]))
               and _n["evidence"].get("not_narrowed") == ["examined_empty", "never_examined", "owed"], (_code, _n["evidence"]["held"][:3], _n["specification"]["owed"]))
    else:
        skip("T034-08", "no figure of the chosen parameter carries an identity code")

if _P_fig is not None:
    with scratch() as c:
        _two = [r[0] for r in c.execute("SELECT identity_code FROM base_taxonomy_identity WHERE identity_code<>'ALL' AND parent_code IS NULL "
                                        "ORDER BY identity_code LIMIT 2")]
        c.execute("UPDATE base_taxonomy_identity SET parent_code=? WHERE identity_code=?", (_two[0], _two[1]))   # HAND, on the copy
        c.execute("INSERT INTO determination_gates (parameter_id, identity_code, verdict, detail, raised_at, raised_by_session) "
                  "VALUES (?,?,'QUESTION','T034 fixture','2026-11-16','TASK-FIXTURE')", (_P_fig, _two[1]))
        c.commit()
        _gid = c.execute("SELECT MAX(gate_id) FROM determination_gates").fetchone()[0]
        _par = db.cell_status(_P_fig, identity=_two[0])["stages"]["specification"]["owed"]["open_gates"]
        _kid = db.cell_status(_P_fig, identity=_two[1])["stages"]["specification"]["owed"]["open_gates"]
        _sib = [r[0] for r in c.execute("SELECT identity_code FROM base_taxonomy_identity WHERE identity_code NOT IN (?,?) AND identity_code<>'ALL' "
                                        "ORDER BY identity_code LIMIT 1", _two)]
        _oth = db.cell_status(_P_fig, identity=_sib[0])["stages"]["specification"]["owed"]["open_gates"] if _sib else None
        record("T034-09", "an open gate on a child identity code is owed on the parent's cell (the engine's rule: the parent gathers the child's figures), on the "
               "child's own, and not on an unrelated code's",
               _gid in _par and _gid in _kid and _oth is not None and _gid not in _oth, (_gid, _par, _kid, _oth))
    with scratch() as c:
        _co = c.execute("SELECT jurisdiction_code FROM base_jurisdictions WHERE kind='country' ORDER BY 1 LIMIT 1").fetchone()[0]
        c.execute("INSERT INTO base_jurisdictions (jurisdiction_code, kind, parent_code) VALUES (?, 'sub-national', ?)", (f"{_co}-ZZ", _co))   # HAND, on the copy
        c.commit()
        _sub, _top = db.cell_status(_P_fig, jurisdiction=f"{_co}-ZZ"), db.cell_status(_P_fig, jurisdiction=_co)
        record("T034-10", "a sub-national jurisdiction is asked about at its country, so it answers as the country does and the report names the country",
               _sub["stages"] == _top["stages"] and _sub["jurisdiction"] == _co, (_sub["jurisdiction"], _co))

print("Section T048: an external root is registered by a verb, and a figure already written can point at it")
_RT = next(iter(sorted(dbcore.schema_choices("external_root_registry", "root_type"))), None)
_EID = scalar("SELECT extraction_id FROM source_value_extractions WHERE root_id IS NULL ORDER BY extraction_id LIMIT 1")
if _RT is None or _EID is None:
    skip("T048", "no root type in the CHECK or no figure without a root on the live database")
else:
    with scratch() as c:
        _n0 = c.execute("SELECT COUNT(*) FROM external_root_registry").fetchone()[0]
        res, err = ok(db.register_root, "T048-ROOT-A", "a fixture root", _RT, "TASK-FIXTURE: a warrant", "n", None, session=S, dry_run=False)
        _row = c.execute("SELECT description, root_type, provenance, root_population_note, created_by_session FROM external_root_registry "
                         "WHERE root_id=?", ("T048-ROOT-A",)).fetchone()
        record("T048-01", "register-root writes one row with its type, its warrant and the session stamp, and the table is then in the captured set",
               err is None and tuple(_row) == ("a fixture root", _RT, "TASK-FIXTURE: a warrant", "n", S)
               and c.execute("SELECT COUNT(*) FROM external_root_registry").fetchone()[0] == _n0 + 1
               and "external_root_registry" in set(dbcore.writable_tables(c)), (err, _row))
        _rs = {"blank description": refusal(db.register_root, "T048-B", " ", _RT, "w", None, None, session=S, dry_run=True),
               "blank warrant": refusal(db.register_root, "T048-B", "d", _RT, "", None, None, session=S, dry_run=True),
               "type outside the CHECK": refusal(db.register_root, "T048-B", "d", "BANANA", "w", None, None, session=S, dry_run=True),
               "space in the id": refusal(db.register_root, "T048 B", "d", _RT, "w", None, None, session=S, dry_run=True),
               "already registered": refusal(db.register_root, "T048-ROOT-A", "d", _RT, "w", None, None, session=S, dry_run=True)}
        record("T048-02", "register-root refuses a blank description, a blank warrant, a type outside the CHECK, a space in the id and a root already registered, "
               "each by name", all(_rs.values()) and "--description" in _rs["blank description"] and "--provenance" in _rs["blank warrant"]
               and "CHECK" in _rs["type outside the CHECK"] and "--root-id" in _rs["space in the id"]
               and "already registered" in _rs["already registered"], _rs)
        res, err = ok(db.amend_extraction, _EID, "root_id", "T048-ROOT-A", "T048 fixture", session=S, dry_run=False)
        _now = c.execute("SELECT root_id FROM source_value_extractions WHERE extraction_id=?", (_EID,)).fetchone()[0]
        _notes = c.execute("SELECT notes FROM source_value_extractions WHERE extraction_id=?", (_EID,)).fetchone()[0] or ""
        _dup = {"case variant": refusal(db.register_root, "t048-root-a", "another", _RT, "w", None, None, session=S, dry_run=True),
                "same description": refusal(db.register_root, "T048-ROOT-Z", " A FIXTURE ROOT ", _RT, "w", None, None, session=S, dry_run=True),
                "an admitted source": refusal(db.register_root, scalar("SELECT ref_id FROM evidence_sources LIMIT 1"), "d", _RT, "w", None, None, session=S, dry_run=True)}
        record("T048-02b", "register-root refuses a case variant of a registered id, a description already registered, and an admitted source's ref_id (a root held here is --root-ref-id)",
               all(_dup.values()) and "another spelling" in _dup["case variant"] and "another spelling" in _dup["same description"] and "--root-ref-id" in _dup["an admitted source"], _dup)
        record("T048-03", "amend-extraction --field root_id points a figure at a registered root and the writer's marker keeps the change in notes",
               err is None and _now == "T048-ROOT-A" and "root_id" in _notes, (err, _now, _notes[-160:]))
        _bad = refusal(db.amend_extraction, _EID, "root_id", "T048-NOT-REGISTERED", "T048 fixture", session=S, dry_run=True)
        record("T048-04", "an id absent from the registry is refused by the foreign-key check, naming the table", bool(_bad) and "external_root_registry" in _bad, _bad)
    _src = pathlib.Path(db.__file__).read_text(encoding="utf-8")
    record("T048-05", "add-extraction's refusal for an unregistered root names the verb that registers one and no longer says no writer exists",
           "db.py register-root" in _src and "has no writer yet" not in _src, None)

print("Section T054: an identity code retires in place to the need or code that carries it, and a crossing row retires in place")
_H54 = [l[3:] for l in pathlib.Path(dbcore.LEDGER_PATH).read_text(encoding="utf-8").splitlines() if l.startswith("## ")]
_H54 = [h for h in _H54 if h.startswith(dbcore.LEDGER_OWNER_PREFIX) and re.search(r"\d{4}-\d{2}-\d{2}", h) and _H54.count(h) == 1]
_OH54 = _H54[0] if _H54 else None
_named54 = lambda code: next((h for h in _H54 if dbcore.ledger_entry_names(h, code)), None)          # noqa: E731
_codes54 = [r[0] for r in q("SELECT identity_code FROM base_taxonomy_identity WHERE status='active' ORDER BY identity_code")]
_NEED54 = scalar("SELECT need_code FROM access_needs ORDER BY need_code LIMIT 1")
_LINK54 = q("SELECT link_id, identity_code FROM identity_icf_map WHERE retired_at IS NULL ORDER BY link_id LIMIT 1")
with scratch() as c:
    _free = [k for k in _codes54 if not db._identity_carriers(c, k) and _named54(k)]
    _carried = [k for k in _codes54 if db._identity_carriers(c, k)]
    if not (_OH54 and _NEED54 and len(_free) >= 2 and _carried and _LINK54):
        skip("T054", "the live ledger or database offers no owner heading, need, two free codes, a carried code and a live crossing row")
    else:
        _a, _b = _free[0], _free[1]
        _HA, _HB = _named54(_a), _named54(_b)
        _R = dict(session=S, dry_run=False)
        _n0 = c.execute("SELECT COUNT(*) FROM base_taxonomy_identity").fetchone()[0]
        res, err = ok(db.retire_identity, _a, _NEED54, None, _HA, "T054 fixture", **_R)
        _r = c.execute("SELECT status, superseded_by_need, superseded_by_identity FROM base_taxonomy_identity WHERE identity_code=?", (_a,)).fetchone()
        record("T054-01", "retire-identity --need deprecates the code in place with that need as its one successor, deletes nothing and reports the approval",
               err is None and tuple(_r) == ("deprecated", _NEED54, None) and c.execute("SELECT COUNT(*) FROM base_taxonomy_identity").fetchone()[0] == _n0
               and res["approval_ref"] == _HA, (err, tuple(_r)))
        if len(_free) > 2:
            res, err = ok(db.retire_identity, _b, None, _free[2], _HB, "T054 fixture", **_R)
            _r2 = c.execute("SELECT status, superseded_by_need, superseded_by_identity FROM base_taxonomy_identity WHERE identity_code=?", (_b,)).fetchone()
            record("T054-02", "retire-identity --to-identity deprecates the code with that identity as its one successor",
                   err is None and tuple(_r2) == ("deprecated", None, _free[2]), (err, tuple(_r2)))
        else:
            skip("T054-02", "fewer than three codes without live carriers")
        _c0 = _carried[0]
        _rs = {"neither": refusal(db.retire_identity, _free[-1], None, None, _OH54, "r", session=S, dry_run=True),
               "both": refusal(db.retire_identity, _free[-1], _NEED54, _free[0], _OH54, "r", session=S, dry_run=True),
               "not held": refusal(db.retire_identity, "NO-SUCH-CODE", _NEED54, None, _OH54, "r", session=S, dry_run=True),
               "already deprecated": refusal(db.retire_identity, _a, _NEED54, None, _HA, "r", session=S, dry_run=True),
               "entry does not name the code": refusal(db.retire_identity, _free[-1], _NEED54, None, _HA if _named54(_free[-1]) != _HA else _OH54, "r", session=S, dry_run=True),
               "need absent": refusal(db.retire_identity, _free[-1], "NO-SUCH-NEED", None, _OH54, "r", session=S, dry_run=True),
               "to itself": refusal(db.retire_identity, _free[-1], None, _free[-1], _OH54, "r", session=S, dry_run=True),
               "to a deprecated code": refusal(db.retire_identity, _free[-1], None, _a, _OH54, "r", session=S, dry_run=True),
               "blank reason": refusal(db.retire_identity, _free[-1], _NEED54, None, _OH54, "", session=S, dry_run=True),
               "not an owner entry": refusal(db.retire_identity, _free[-1], _NEED54, None, "Supersession record 2026-11-15 — x", "r", session=S, dry_run=True),
               "carried": refusal(db.retire_identity, _c0, _NEED54, None, _named54(_c0) or _OH54, "r", session=S, dry_run=True)}
        record("T054-03", "retire-identity refuses neither or both successors, a code not held or already deprecated, a need that does not exist, a retirement "
               "to itself or to a deprecated code, a blank reason, an approval that is not the owner's, and a code a live row still carries (naming the "
               "carriers and the count)",
               all(_rs.values()) and "exactly one" in _rs["neither"] and "exactly one" in _rs["both"] and "not held" in _rs["not held"]
               and "already deprecated" in _rs["already deprecated"] and "access_needs" in _rs["need absent"] and "itself" in _rs["to itself"]
               and "deprecated" in _rs["to a deprecated code"] and "--reason" in _rs["blank reason"] and "owner" in _rs["not an owner entry"]
               and "does not name" in _rs["entry does not name the code"]
               and ("still carried" in _rs["carried"] or not _named54(_c0)) and re.search(r"\w+\.\w+ \(\d+\)", _rs["carried"]), _rs)
        _w = {"add-population-icf-link": refusal(db.insert_population_icf_link, population=_a, icf_code="d450", mechanism="m", mapping_confidence="high_predictive",
                                                provenance="p", session=S, dry_run=True),
              "raise-determination-gate": refusal(db.raise_determination_gate, parameter_id=scalar("SELECT parameter_id FROM base_parameters WHERE status='active' LIMIT 1"),
                                                 verdict="QUESTION", detail="x", identity=_a, session=S, dry_run=True),
              "fk_declared": refusal(dbcore.fk_declared, c, "connection_targets", "identity_code", _a, "add-connection identity_code")}
        record("T054-04", "a writer given the deprecated code refuses it and names the access need that replaced it",
               all(v and "deprecated" in v and _NEED54 in v for v in _w.values()), _w)
        _lid = _LINK54[0][0]
        res, err = ok(db.retire_population_icf_link, _lid, "T054 fixture", **_R)
        _lr = c.execute("SELECT retired_at, retired_by_session, retired_reason FROM identity_icf_map WHERE link_id=?", (_lid,)).fetchone()
        _again = refusal(db.retire_population_icf_link, _lid, "again", session=S, dry_run=True)
        _absent = refusal(db.retire_population_icf_link, 2 ** 30, "r", session=S, dry_run=True)
        _blank = refusal(db.retire_population_icf_link, _lid, " ", session=S, dry_run=True)
        record("T054-05", "retire-population-icf-link retires one crossing row in place with its session and reason; a second retirement, an absent id and a blank reason are refused",
               err is None and all(_lr) and _lr[2] == "T054 fixture" and _again and "already retired" in _again and _absent and "not in identity_icf_map" in _absent
               and _blank and "--reason" in _blank, (err, tuple(_lr), _again, _absent, _blank))
        # T054-09: a retirement is not blocked by records, and says what stays; T054-10: a code that is a deprecated
        # code's successor cannot be retired
        if len(_free) > 4:
            _y, _x = _free[3], _free[4]
            ok(db.retire_identity, _x, None, _y, _named54(_x), "T054 fixture", **_R)
            _blocked = refusal(db.retire_identity, _y, _NEED54, None, _named54(_y), "r", session=S, dry_run=True)
            record("T054-10", "a code another deprecated code names as its successor cannot be retired while that stands",
                   bool(_blocked) and "still carried" in _blocked and "superseded_by_identity" in _blocked, _blocked)
        _bad = []
        _spare = next(k for k in _codes54 if k not in (_a, _b, *_free[2:5]))
        for sql in ("UPDATE base_taxonomy_identity SET status='deprecated' WHERE identity_code=?",
                    "UPDATE base_taxonomy_identity SET superseded_by_need=? WHERE identity_code=?",
                    "UPDATE base_taxonomy_identity SET status='deprecated', superseded_by_need=?, superseded_by_identity=? WHERE identity_code=?"):
            try:
                args = {1: (_spare,), 2: (_NEED54, _spare), 3: (_NEED54, _a, _spare)}[sql.count("?")]
                c.execute(sql, args); _bad.append(sql)
            except sqlite3.IntegrityError:
                pass
        c.rollback()
        record("T054-06", "the schema refuses a deprecated code with no successor, an active code with one, and a deprecated code with two", not _bad, _bad)

with scratch() as c:           # T054-09: a fresh copy, so every free code is still free
    _fc = [k for k in [r[0] for r in c.execute("SELECT identity_code FROM base_taxonomy_identity WHERE status='active' ORDER BY identity_code")]
           if not db._identity_carriers(c, k) and _named54(k)]
    if _fc and _NEED54:
        c.execute("UPDATE evidence_population_match SET target_population=? WHERE rowid=(SELECT MIN(rowid) FROM evidence_population_match)", (_fc[0],)); c.commit()   # HAND: one graded match names it
        res5, err5 = ok(db.retire_identity, _fc[0], _NEED54, None, _named54(_fc[0]), "T054 fixture", session=S, dry_run=False)
        record("T054-09", "a code that only a graded population match still names is retired, and the result lists that record as history (a match is a record, not a carrier)",
               err5 is None and any(r["where"] == "evidence_population_match.target_population" and r["rows"] >= 1 for r in res5["records_kept_as_history"]), (err5, res5))
    else:
        skip("T054-09", "no free code named by an owner entry, or no need")

print("Section T055: device_class takes the mobility values and can be amended on a figure already written")
_EID55 = scalar("SELECT extraction_id FROM source_value_extractions WHERE device_class IS NULL ORDER BY extraction_id LIMIT 1")
_dv = {"lower_limb_prosthesis", "crutches", "cane"}
if _EID55 is None:
    skip("T055", "no figure without a device_class on the live database")
else:
    record("T055-11", "the column's own CHECK admits the three mobility values and keeps every earlier one",
           _dv <= set(dbcore.schema_choices("source_value_extractions", "device_class")) and {"power_chair", "walker_rollator", "mixed", "not_device_scoped"}
           <= set(dbcore.schema_choices("source_value_extractions", "device_class")), sorted(dbcore.schema_choices("source_value_extractions", "device_class")))
    with scratch() as c:
        _out = {}
        for v in sorted(_dv):
            res, err = ok(db.amend_extraction, _EID55, "device_class", v, "T055 fixture", session=S, dry_run=False)
            _out[v] = (err, c.execute("SELECT device_class FROM source_value_extractions WHERE extraction_id=?", (_EID55,)).fetchone()[0])
        _bad = refusal(db.amend_extraction, _EID55, "device_class", "BANANA", "T055 fixture", session=S, dry_run=True)
        record("T055-12", "amend-extraction --field device_class accepts each new value and refuses one outside the CHECK, naming the set",
               all(e is None and now == v for v, (e, now) in _out.items()) and bool(_bad) and "power_chair" in _bad, (_out, _bad))

print("Section T080: a search that found nothing states its cause, or was not run")
_cls80 = sorted(dbcore.schema_choices("search_executions", "absence_class"))
_r0 = refusal(db.log_search, **search(results_found=0))
_r0b = refusal(db.log_search, **search(results_found=0, backfill=1))
record("T080-01", "log-search refuses a zero-result search with no cause, backfill included, naming every value of the column's CHECK and the deferral for a request that returned no result list",
       all(_r0) and all(c in _r0 for c in _cls80) and "--deferred-reason" in _r0 and _r0b and all(c in _r0b for c in _cls80), (_r0, _r0b))
_ok0, _e0 = ok(db.log_search, **search(results_found=0, absence_class=_cls80[0]))
_ok1, _e1 = ok(db.log_search, **search(results_found=0, deferred_reason="TASK-FIXTURE the request returned no result list (403)"))
_ok2, _e2 = ok(db.log_search, **search(results_found=3))
record("T080-02", "a zero-result search carrying a cause, a deferred search, and a search that found something are all accepted (dry run)",
       _e0 is None and _e1 is None and _e2 is None, (_e0, _e1, _e2))
_r3 = refusal(db.log_search, **search(results_found=2, absence_class=_cls80[0]))
record("T080-03", "an absence class on a search that found something is still refused", bool(_r3) and "only a search that found nothing" in _r3, _r3)
_rb = refusal(db.log_search, **search(results_found=0, deferred_reason="  "))
_rn = refusal(db.log_search, **search(results_found=-1))
_rs = refusal(db.log_search, **search(results_found="0"))
_rboth = refusal(db.log_search, **search(results_found=0, absence_class=_cls80[0], deferred_reason="TASK-FIXTURE not run"))
record("T080-04", "a blank deferral, a negative count, a count that is not a whole number, and a class beside a deferral are each refused before a row is written",
       bool(_rb) and "--results-found 0 needs" in _rb and bool(_rn) and "whole number" in _rn and bool(_rs) and "whole number" in _rs
       and bool(_rboth) and "cannot assert both" in _rboth, (_rb, _rn, _rs, _rboth))
_cli80 = cli("log-search", "--slug", SLUG, "--language", LANG, "--jurisdiction", JUR, "--query-text", "q", "--engine", "web",
             "--depth-method", "scoping", "--prior-expectation", "nothing", "--session", S, "--dry-run")
record("T080-05", "through the CLI, a search that states no count (so 0) and no cause is refused with the REFUSING prefix",
       _cli80.returncode != 0 and _cli80.stderr.lstrip().startswith("REFUSING") and "--results-found 0 needs" in _cli80.stderr,
       (_cli80.returncode, _cli80.stderr[:200]))
with scratch() as c:
    _cell = c.execute("SELECT slug, language, jurisdiction FROM v_coverage_priority WHERE jurisdiction IN (SELECT jurisdiction_code FROM base_jurisdictions) AND language IN (SELECT language FROM lang_jur_map) ORDER BY priority_score DESC, slug LIMIT 1").fetchone()
    if _cell is None:
        skip("T080-06", "no owed cell on the live database")
    else:
        _q = lambda: c.execute("SELECT COUNT(*) FROM v_coverage_priority WHERE slug=? AND language=? AND jurisdiction=?", tuple(_cell)).fetchone()[0]
        _n0 = _q()
        _o, _e = ok(db.log_search, **search(slug=_cell[0], language=_cell[1], jurisdiction=_cell[2], results_found=0,
                                            deferred_reason="TASK-FIXTURE the request returned 403", dry_run=False))
        c.commit()
        _n1 = _q()
        _o2, _e2 = ok(db.log_search, **search(slug=_cell[0], language=_cell[1], jurisdiction=_cell[2], results_found=0,
                                              absence_class=_cls80[0], dry_run=False))
        c.commit()
        _n2 = _q()
        record("T080-06", "a deferred search (not run) leaves its cell on the owed list and a search that ran takes it off (migration 137)",
               _e is None and _e2 is None and _n0 == 1 and _n1 == 1 and _n2 == 0, (_e, _e2, _n0, _n1, _n2))

print("Section T073: a fixture retrieval root leaves out a folder filed under an id the database has not minted")
import io as _io
_hw = dbcore.ref_id_high_water(sqlite3.connect(f"file:{DB}?mode=ro", uri=True))
_src = pathlib.Path(TMP) / "t073-source"
for _name, _ref in (("session-below", f"REF-{max(_hw - 1, 1):05d}"), ("session-at", f"REF-{_hw:05d}"), ("session-ahead", f"REF-{_hw + 1:05d}")):
    (_src / _name).mkdir(parents=True, exist_ok=True)
    (_src / _name / "manifest.jsonl").write_text(json.dumps({"ref_id": _ref}) + "\n", encoding="utf-8")
(_src / "session-no-manifest").mkdir(exist_ok=True)
_mx = _src / "session-mixed"                      # one folder, two sources: one admitted (at the mark), one not yet
_mx.mkdir(exist_ok=True)
(_mx / "manifest.jsonl").write_text(json.dumps({"ref_id": f"REF-{_hw:05d}", "artefact": "aaaa.html"}) + "\n"
                                    + json.dumps({"ref_id": f"REF-{_hw + 1:05d}", "artefact": "bbbb.pdf"}) + "\n", encoding="utf-8")
for _f in ("aaaa.html", "bbbb.pdf", "bbbb-full-text.txt"):
    (_mx / _f).write_text("x", encoding="utf-8")
with contextlib.redirect_stdout(_io.StringIO()) as _out:
    _root = pathlib.Path(fixture_log_root(os.path.join(TMP, "t073-root"), DB, source=_src))
_kept = sorted(x.name for x in _root.iterdir())
_mfiles = sorted(x.name for x in (_root / "session-mixed").iterdir())
_mlines = [json.loads(l)["ref_id"] for l in (_root / "session-mixed" / "manifest.jsonl").open() if l.strip()]
record("T073-01", "the fixture root links every folder whose ids the database has minted (below and AT its high-water mark) and one with no manifest, and keeps of a folder holding "
       "an id above the mark only the lines and files of the ids below it, saying so in one line that names the id and the mark",
       _kept == ["session-ahead", "session-at", "session-below", "session-mixed", "session-no-manifest"]
       and _mfiles == ["aaaa.html", "manifest.jsonl"] and _mlines == [f"REF-{_hw:05d}"] and list((_root / "session-ahead").iterdir()) == [_root / "session-ahead" / "manifest.jsonl"]
       and f"REF-{_hw + 1:05d}" in _out.getvalue() and str(_hw) in _out.getvalue(), (_kept, _mfiles, _mlines, _out.getvalue()))
record("T073-02", "the fixture root of this very suite holds no folder above the copy's high-water mark",
       not any(dbcore._MINTABLE.fullmatch((json.loads(l).get("ref_id") or "")) and int(json.loads(l)["ref_id"][4:]) > _hw
               for m in pathlib.Path(FARM).glob("*/manifest.jsonl") for l in m.open() if l.strip()), None)

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
M_A, M_B, M_C = (f"{t} (first pass)" for t in (TL_A, TL_B, TL_C))   # the main copy's own leads; the scratch group below stages TL_*
r = refusal(db.insert_locator, {**LOC, "ref_id": far(NEXT), "title": M_A}, session=S, dry_run=True)
record("I01", "add-locator refuses a ref_id that is not next-id ref", r and NEXT in r, r)
res, err = ok(db.insert_locator, {**LOC, "ref_id": NEXT, "title": M_A}, session=S, dry_run=False)
record("I02", "add-locator accepts the next id (staged)", err is None, err)
r = refusal(db.insert_evidence_source, {**SRC, "ref_id": far(NEXT), "title": M_A},
            S, dry_run=True, authors=AUTH)
record("I03", "add-source refuses a hand-typed ref_id above the high-water mark", r and "next-id" in r, r)
res, err = ok(db.insert_evidence_source, {**SRC, "ref_id": NEXT, "title": M_A},
              S, dry_run=True, authors=AUTH)
record("I04", "add-source accepts the id its own locator staged (promotion)", err is None, err)
want = dbcore.next_ref_id(con)
got, err = ok(db.insert_locator, {**LOC, "title": M_B}, session=S, dry_run=False)
record("I05", "add-locator with no ref_id lands as dbcore.next_ref_id (R2-9)", got == want, err or (got, want))
want = dbcore.next_ref_id(con)
got, err = ok(db.insert_evidence_source, {**SRC, "title": M_C}, S, dry_run=False, authors=AUTH)
record("I06", "add-source with no ref_id, for a document no staged lead describes, lands as the next id",
       got == want, err or (got, want))
r1 = refusal(db.insert_evidence_source, {**SRC, "title": M_C, "ref_id": far(want)}, S, dry_run=True, authors=AUTH)
r2 = refusal(db.insert_locator, {**LOC, "title": M_C, "ref_id": far(want)}, session=S, dry_run=True)
record("I07", "a given id that is not the computed one is still refused, naming the flag to omit",
       r1 and r2 and "omit --ref-id" in r1 and "omit --ref-id" in r2, (r1, r2))
# T-007: a source with no standing, or no type, is refused and the refusal names the live vocabulary
# of the column's own CHECK. UNVERIFIED is a real value and is accepted. Titles match no staged lead.
_T7 = {"title": "Fixture on handrail grip diameters and a T007 probe"}
for _tid, _col, _flag in (("T007-01", "verification_status", "--verification-status"),
                          ("T007-02", "source_type", "--source-type")):
    _row = {k: v for k, v in {**SRC, **_T7}.items() if k != _col}
    _r = refusal(db.insert_evidence_source, _row, S, dry_run=True, authors=AUTH)
    _vocab = dbcore.schema_choices("evidence_sources", _col)
    record(_tid, f"add-source without {_flag} refuses, names it and the column's CHECK vocabulary, joined as the refusal prints it",
           _r and _flag in _r and ", ".join(_vocab) in _r and "Nothing was written" in _r, _r)
_n = scalar("SELECT COUNT(*) FROM evidence_sources")
_r = refusal(db.insert_evidence_source, {**SRC, **_T7, "verification_status": None}, S,
             dry_run=False, authors=AUTH)
record("T007-03", "a standing given as None is refused as absent and writes no row",
       _r and "--verification-status" in _r and scalar("SELECT COUNT(*) FROM evidence_sources") == _n, _r)
_res, _err = ok(db.insert_evidence_source, {**SRC, **_T7}, S, dry_run=True, authors=AUTH)
record("T007-04", "add-source with UNVERIFIED and a source type from the vocabulary is accepted",
       _err is None, _err)
with scratch() as c:
    nxt = lambda: dbcore.next_ref_id(c)  # noqa: E731
    la, lb = (db.insert_locator({**LOC, "title": t}, session=S, dry_run=False) for t in (TL_A, TL_B))

    def land(title, **o):
        """(the id the writer gives this source, the refusal text) -- a dry run."""
        try:
            return db.insert_evidence_source({**SRC, "title": title, **o}, S, dry_run=True, authors=AUTH), None
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
    r = refusal(db.insert_evidence_source, {**SRC, "title": TL_A + str(i), "verification_status": "UNVERIFIED",
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
_MINT = dict(catalogue="references/none.md", entry_ref="x", approval_ref="## 2026-01-01 no such entry", session=S, dry_run=True)
r = refusal(db.mint_term_from_catalogue, canonical_en="Fixture quantity",
            definition="Affects more than one limb, no more than mild", **_MINT)
record("Z08", "a definition with 'than' and 'no more' is not refused for its words (it is refused later, for "
              "its unrecorded approval, which this case does not supply)", r is not None and "--definition" not in r, r)
r = refusal(db.mint_term_from_catalogue, canonical_en="Fixture quantity", definition="Grade 3 impairment", **_MINT)
record("Z09", "...and a definition with a number still is", r and "--definition" in r, r)
r = refusal(db.mint_term_from_catalogue, canonical_en="not steeper than", definition="Fixture definition", **_MINT)
record("Z10", "...while the same words in the canonical name are refused", r and "'than'" in r, r)
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
                           "--slug", slug, "--identity", CELL_IDENT, "--icf", ICF, "--session", session,
                           "--stamp", stamp or STAMP, *extra],
                          capture_output=True, text=True, env=dict(os.environ))


P_NODIR = scalar("SELECT parameter_id FROM base_parameters WHERE status='active' AND "
                 "accessibility_direction IS NULL AND parameter_id IN (SELECT parameter_id FROM "
                 "source_value_extractions) AND parameter_id<>? ORDER BY 1 LIMIT 1", P_FULL)
CELL_P = P_NODIR if P_NODIR is not None else P1
# T-019: a figure reaches a cell only through the live lens links written on it, so the engine cases key their
# cell on an identity taken by query from a live link of the cell's own parameter, and the first such figure is
# given the ICF code the cell also states, through the sanctioned verb on this test's copy (no live figure
# carries two lenses). Its warrant is a word of the figure's own claim text.
CELL_FIG = q("SELECT l.extraction_id, l.identity_code, x.claim_text FROM source_value_extractions x JOIN "
             "v_live_lens_links l USING (extraction_id) WHERE x.parameter_id=? AND l.identity_code IS NOT NULL "
             "ORDER BY 1 LIMIT 1", CELL_P)
CELL_IDENT = CELL_FIG[0][1] if CELL_FIG else None
CELL_WORD = next(iter(re.findall(r"\w+", CELL_FIG[0][2] or "")), "") if CELL_FIG else ""


def link_cell_figure(flag, code):
    """Give the cell's figure one more lens link on the current copy; the refusal, if any, or None."""
    r_ = cli("add-lens-link", "--extraction-id", str(CELL_FIG[0][0]), flag, code, "--basis", "named_in_text",
             "--basis-text", CELL_WORD, "--session", S)
    return None if r_.returncode == 0 else (r_.stderr + r_.stdout)[-300:]


CELL_LINKED = bool(CELL_FIG and CELL_WORD and ICF is not None and link_cell_figure("--icf", ICF) is None)
if not CELL_LINKED:
    for t_ in ("E01-E03", "E05", "E06", "E11", "E12"):
        skip(t_, "the ICF registry is empty, or no figure of the cell's parameter carries an identity link "
                 "to give the cell's ICF code to")
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
               f"param {P_NODIR}×{CELL_IDENT}/" in r.stdout, r.stdout[:120])
        record("E03", "the report carries direction_ref_id beside the direction",
               "direction_ref_id" in rep, list(rep)[:5])
        # T-019: the handshake audit exempts an ENGINE-written pending cell from the missing-path note (it has no
        # answer and claims no path) and keeps the note for a pending row the engine would not have written.
        with scratch() as c:
            path = os.environ["GUIDEBOOK_DB_PATH"]
            sid = c.execute("SELECT MAX(specification_id) FROM specifications WHERE parameter_id=? AND "
                            "retired_at IS NULL", (P_NODIR,)).fetchone()[0]
            audit = lambda: subprocess.run(  # noqa: E731
                [sys.executable, str(REPO / "scripts/audit/derivation_handshake_integrity.py"), "--db", path],
                capture_output=True, text=True, env=dict(os.environ)).stdout
            noted = lambda: f"specification {sid}: no derivation_paths recorded" in audit()  # noqa: E731
            record("F5-a", "an engine-written pending cell (rule_version set, a figure stated in its lens) is "
                           "not noted for its missing path", sid is not None and not noted())
            # HAND: the row as a route that skips the engine would leave it.
            engine_rv = c.execute("SELECT rule_version FROM specifications WHERE specification_id=?", (sid,)).fetchone()[0]
            c.execute("UPDATE specifications SET rule_version=NULL WHERE specification_id=?", (sid,))
            c.commit()
            record("F5-b", "...a pending row with no rule_version is noted", noted())
            other = scalar("SELECT identity_code FROM base_taxonomy_identity WHERE identity_code NOT IN "
                           "(SELECT l.identity_code FROM v_live_lens_links l JOIN source_value_extractions x "
                           "USING (extraction_id) WHERE x.parameter_id=? AND l.identity_code IS NOT NULL) "
                           "ORDER BY 1 LIMIT 1", P_NODIR)
            c.execute("UPDATE specifications SET rule_version=?, identity_code=? WHERE specification_id=?",
                      (engine_rv, other, sid))
            c.commit()
            record("F5-c", "...and so is a pending row in a lens no live-linked figure of its parameter carries "
                           "(the engine would refuse it)", other is not None and noted())
            c.execute("UPDATE specifications SET identity_code=?, state='provisional', marker=? WHERE "
                      "specification_id=?", (CELL_IDENT, EvidenceMarker.WEAK.value, sid))
            c.commit()
            record("F5-d", "...and a hand-written `provisional` row with no derivation_paths is still noted", noted())
    else:
        for t_ in ("E01", "E02", "E03"):
            skip(t_, "no active direction-less parameter holds an extraction")
# ─────────────────────── T-013: a gap says what it is a gap in; a search says which gap caused it ───────────────────────
print("Section T013: add-gap names a cell-less gap's parameter, lens, jurisdiction and language; log-search --gap-id; "
      "an engine-made gap is reached through its cell, never copied (rule 5)")
GAP_SUBJECT = ("parameter_id", "identity_code", "icf_code", "needs_code", "jurisdiction", "language")
gcols = [x[1] for x in con.execute("PRAGMA table_info(gaps)")]
secols = [x[1] for x in con.execute("PRAGMA table_info(search_executions)")]
fk_of = lambda t, col: [tuple(f[2:5]) for f in con.execute(f'PRAGMA foreign_key_list("{t}")') if f[3] == col]  # noqa: E731
record("T013-01", "gaps holds the subject columns and search_executions holds gap_id (the lens and parameter "
                  "columns point where search_executions' own do; gap_id points at gaps)",
       all(c_ in gcols for c_ in GAP_SUBJECT) and "gap_id" in secols
       and all(fk_of("gaps", c_) == fk_of("search_executions", c_) and fk_of("gaps", c_)
               for c_ in ("parameter_id", "identity_code", "icf_code", "needs_code"))
       and fk_of("search_executions", "gap_id") == [("gaps", "gap_id", "gap_id")],
       ([c_ for c_ in GAP_SUBJECT if c_ not in gcols], "gap_id" in secols))

A_PAR = scalar("SELECT parameter_id FROM base_parameters WHERE status='active' ORDER BY 1 LIMIT 1")
A_NEED = scalar("SELECT need_code FROM access_needs ORDER BY 1 LIMIT 1")
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
    skip("T013-02..T013-21", "a registry or the research-scope map is empty")
else:
    flags = ["--parameter", str(A_PAR), "--identity", IDENT, "--icf", ICF, "--needs", A_NEED,
             "--jurisdiction", JUR, "--language", LANG.lower()]
    want = {"parameter_id": A_PAR, "identity_code": IDENT, "icf_code": ICF, "needs_code": A_NEED,
            "jurisdiction": JUR, "language": LANG}
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
        record("T013-03", "add-gap with no subject flag still works and leaves the subject columns NULL",
               g0 is not None and all(row0.get(k_) is None for k_ in GAP_SUBJECT), (r0.stderr[-200:], row0))

        # Each refusal: non-zero exit, the flag or column named, and no row written.
        bad = {"--parameter": ("parameter_id", str(scalar("SELECT MAX(parameter_id) FROM base_parameters") + 1000)),
               "--identity": ("identity_code", IDENT + "-NO-SUCH"), "--icf": ("icf_code", ICF + "-NO-SUCH"),
               "--needs": ("needs_code", A_NEED + "-NO-SUCH"),
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
        ls = lambda gap, *a: cli("log-search", "--results-found", "1", "--parameter", str(A_PAR), "--language", LANG, "--query-text",  # noqa: E731
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
        rn = cli("log-search", "--results-found", "1", "--parameter", str(A_PAR), "--language", LANG, "--query-text", "TASK-FIXTURE probe",
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
    # T-019: a parameter no figure is read for has no cell (the engine refuses and writes nothing: OD-08), so the
    # engine's pending cell is the section-C figure's, given the needs code the cell also states.
    P_ENG = CELL_P if CELL_LINKED else None
    if P_ENG is None:
        skip("T013-10", "no figure of an active parameter can carry the identity, ICF and needs codes of an engine cell")
    else:
        with scratch() as c:
            path = os.environ["GUIDEBOOK_DB_PATH"]
            rj = os.path.join(TMP, "t013-assess.json")
            link_cell_figure("--needs", A_NEED)
            # A lens no earlier case writes (E01-E12 use the default identity and ICF): add a needs code (trap a).
            r = assess(path, P_ENG, SLUG, "--needs", A_NEED, "--report-json", rj)
            rep = json.load(open(rj))[0] if r.returncode == 0 else {}
            cell = c.execute("SELECT parameter_id, identity_code, icf_code, needs_code, gap_register_id "
                             "FROM specifications WHERE gap_register_id=?", (rep.get("gap_register_id") or "",)).fetchone()
            try:
                g = c.execute("SELECT parameter_id, identity_code, icf_code, needs_code, jurisdiction, "
                              "language FROM gaps WHERE gap_id=?", (rep.get("gap_register_id") or "",)).fetchone()
            except sqlite3.OperationalError:
                g = None                                   # no such columns: red below, not a crash
            record("T013-10", "an engine-made gap is reached through its cell (specifications.gap_register_id holds the "
                              "parameter and lenses) and its own subject columns stay NULL: the fact is held once",
                   r.returncode == 0 and rep.get("state") == "pending" and cell is not None and g is not None
                   and tuple(cell)[:4] == (P_ENG, CELL_IDENT, ICF, A_NEED) and all(v_ is None for v_ in tuple(g)),
                   ((r.stdout + r.stderr)[-250:], cell and tuple(cell), g and tuple(g)))
            gid_e = rep.get("gap_register_id") or ""
            try:
                via = c.execute("SELECT parameter_id, identity_code, icf_code, needs_code, subject_home FROM v_gap_subject "
                                "WHERE gap_id=?", (gid_e,)).fetchone()
            except sqlite3.OperationalError as exc:
                via = exc
            record("T013-11", "...and v_gap_subject, the cross-stage view, gives that gap its parameter and lenses from the cell",
                   isinstance(via, sqlite3.Row) and tuple(via) == (P_ENG, CELL_IDENT, ICF, A_NEED, "specifications"), via)

            # (add-gap A) the cell is live: the subject is held there, so a typed gap for it is the second home.
            gap_cli_ = lambda *a: cli("add-gap", "--category", "EG", "--priority", "P3", "--description",  # noqa: E731
                                      "TASK-FIXTURE gap", "--session", S, *a)
            subj_flags = ["--parameter", str(P_ENG), "--identity", CELL_IDENT, "--icf", ICF, "--needs", A_NEED]
            g_before = c.execute("SELECT COUNT(*) FROM gaps").fetchone()[0]
            ra = gap_cli_(*subj_flags)
            spec_id = c.execute("SELECT specification_id FROM specifications WHERE gap_register_id=?", (gid_e,)).fetchone()
            record("T013-13", "add-gap for a subject whose live cell exists is refused, naming the specification and the "
                              "cell's own gap, and writes no row",
                   ra.returncode != 0 and spec_id is not None and f"specification {spec_id[0]}" in ra.stderr + ra.stdout
                   and gid_e in ra.stderr + ra.stdout and c.execute("SELECT COUNT(*) FROM gaps").fetchone()[0] == g_before,
                   (ra.stderr + ra.stdout)[-300:])

            # THE LIVE SHAPE: an OPEN gap whose cell was retired. v_pending (live pending cells only) is empty for it.
            # HAND: retire the cell, as the three live engine gaps' cells are.
            c.execute("UPDATE specifications SET retired_at=?, retired_by_session=?, retirement_reason=? "
                      "WHERE gap_register_id=?", (STAMP, S, "TASK-FIXTURE retired cell", gid_e))
            c.commit()
            in_pending = c.execute("SELECT COUNT(*) FROM v_pending WHERE gap_register_id=?", (gid_e,)).fetchone()[0]
            shown = {g_["gap_id"]: g_ for g_ in ok(db.get_open_gaps)[0] or []}.get(gid_e, {})
            record("T013-14", "an OPEN gap whose cell is retired is not in v_pending, and db.py gaps still gives its parameter "
                              "and lenses (read from the cell through v_gap_subject) and the home it came from",
                   in_pending == 0 and (shown.get("parameter_id"), shown.get("identity_code"), shown.get("icf_code"),
                                        shown.get("needs_code"), shown.get("subject_home")) == (P_ENG, CELL_IDENT, ICF, A_NEED, "specifications")
                   and "description" in shown and "status" in shown,
                   (in_pending, {k_: shown.get(k_) for k_ in ("parameter_id", "identity_code", "subject_home")}))
            # (add-gap A, the legitimate shape) a retired cell holds nothing: the subject may be typed.
            rr = gap_cli_(*subj_flags)
            record("T013-15", "...and once that cell is retired the same subject may be typed on a cell-less gap",
                   rr.returncode == 0, (rr.stderr + rr.stdout)[-300:])
            # A search for the engine gap must agree with the cell's subject (its subject comes from v_gap_subject).
            other_p = scalar("SELECT parameter_id FROM base_parameters WHERE status='active' AND parameter_id<>? "
                             "ORDER BY 1 LIMIT 1", P_ENG)
            base_ls = ["log-search", "--results-found", "1", "--language", LANG, "--query-text", "TASK-FIXTURE probe", "--engine", "manual",
                       "--depth-method", "scoping", "--prior-expectation", "TASK-FIXTURE: none expected", "--session", S]
            r1 = cli(*base_ls, "--parameter", str(other_p), "--gap-id", gid_e)
            r2 = cli(*base_ls, "--parameter", str(P_ENG), "--identity", CELL_IDENT, "--gap-id", gid_e)
            record("T013-16", "log-search --gap-id of an engine gap refuses a search for another parameter (naming both) and "
                              "accepts a search that agrees with the cell",
                   r1.returncode != 0 and str(other_p) in r1.stderr and str(P_ENG) in r1.stderr and gid_e in r1.stderr
                   and r2.returncode == 0, ((r1.stderr)[-250:], r2.stderr[-200:]))

    # A typed (cell-less) gap: a search must agree with it, and the gap must be open; an identical open gap is refused.
    O_PAR = scalar("SELECT parameter_id FROM base_parameters WHERE status='active' AND parameter_id<>? ORDER BY 1 LIMIT 1", A_PAR)
    O_IDENT = scalar("SELECT identity_code FROM base_taxonomy_identity WHERE identity_code<>? ORDER BY 1 LIMIT 1", IDENT)
    O_LANG = scalar("SELECT language FROM lang_jur_map WHERE language<>? ORDER BY 1 LIMIT 1", LANG)
    O_JUR = next((r_[0] for r_ in q("SELECT DISTINCT jurisdiction FROM lang_jur_map WHERE jurisdiction IS NOT NULL "
                                    "AND jurisdiction<>? ORDER BY 1", JUR)
                  if refusal(dbcore.check_jurisdiction, r_[0], "T013") is None), None)    # one the enum declares
    CLOSED = scalar("SELECT gap_id FROM gaps WHERE status LIKE 'CLOSED%' ORDER BY gap_id LIMIT 1")
    CLOSED_STATUS = scalar("SELECT status FROM gaps WHERE gap_id=?", CLOSED)
    if None in (O_PAR, O_IDENT, O_LANG, O_JUR, CLOSED):
        skip("T013-17..T013-20", "no second parameter, identity, language or jurisdiction, or no closed gap, to contradict with")
    else:
        with scratch() as c:
            typed = ["--parameter", str(A_PAR), "--identity", IDENT, "--jurisdiction", JUR, "--language", LANG]
            ga = json.loads(cli("add-gap", "--category", "EG", "--priority", "P3", "--description", "TASK-FIXTURE typed gap",
                                "--session", S, *typed).stdout or "{}").get("gap_id")
            ls_ = lambda gap, **o: cli(*(  # noqa: E731
                ["log-search", "--results-found", "1", "--query-text", "TASK-FIXTURE probe", "--engine", "manual", "--depth-method", "scoping",
                 "--prior-expectation", "TASK-FIXTURE: none expected", "--session", S, "--gap-id", gap]
                + [x for k_, v_ in {"--parameter": str(A_PAR), "--identity": IDENT, "--jurisdiction": JUR,
                                    "--language": LANG, **o}.items() if v_ is not None for x in (k_, v_)]))
            for tid, flag, other, col in (("a", "--parameter", str(O_PAR), "parameter_id"), ("b", "--identity", O_IDENT, "identity_code"),
                                          ("c", "--jurisdiction", O_JUR, "jurisdiction"), ("d", "--language", O_LANG, "language")):
                n0 = n_se(c)
                rx = ls_(ga or "NO-GAP", **{flag: other})
                record(f"T013-17{tid}", f"log-search {flag} {other!r} with --gap-id of a gap typed otherwise is refused naming "
                                        f"{col} and both values, and writes no row",
                       ga is not None and rx.returncode != 0 and col in rx.stderr and ga in rx.stderr and other in rx.stderr
                       and n_se(c) == n0, (rx.stderr + rx.stdout)[-300:])
            n0 = n_se(c)
            rok = ls_(ga or "NO-GAP")
            rnone = ls_(ga or "NO-GAP", **{"--identity": None, "--jurisdiction": None})
            record("T013-18", "...while a search that agrees with the gap, or sets fewer subject flags than it, is accepted",
                   ga is not None and rok.returncode == 0 and rnone.returncode == 0 and n_se(c) == n0 + 2,
                   (rok.stderr + rnone.stderr)[-250:])
            n0 = n_se(c)
            rc_ = ls_(CLOSED, **{"--identity": None, "--jurisdiction": None})
            record("T013-19", "log-search --gap-id of a closed gap is refused naming the id and its status, and writes no row",
                   rc_.returncode != 0 and CLOSED in rc_.stderr and CLOSED_STATUS in rc_.stderr and n_se(c) == n0,
                   (rc_.stderr + rc_.stdout)[-250:])
            # (add-gap B) an identical OPEN typed gap is refused; once it is closed the subject may be filed again.
            g0 = c.execute("SELECT COUNT(*) FROM gaps").fetchone()[0]
            rd = cli("add-gap", "--category", "EG", "--priority", "P3", "--description", "TASK-FIXTURE twin", "--session", S, *typed)
            record("T013-20", "add-gap of a subject an OPEN gap already names exactly is refused, naming that gap, and writes no row",
                   ga is not None and rd.returncode != 0 and ga in rd.stderr + rd.stdout
                   and c.execute("SELECT COUNT(*) FROM gaps").fetchone()[0] == g0, (rd.stderr + rd.stdout)[-300:])
            cg = cli("close-gap", "--gap-id", ga or "NO-GAP", "--status", CLOSED_STATUS, "--session", S)
            re_ = cli("add-gap", "--category", "EG", "--priority", "P3", "--description", "TASK-FIXTURE twin", "--session", S, *typed)
            record("T013-21", "...and once the first is closed the same subject may be filed again",
                   cg.returncode == 0 and re_.returncode == 0, (cg.stderr + re_.stderr)[-250:])

h_ls, h_ag = cli("log-search", "--results-found", "1", "--help").stdout, cli("add-gap", "--help").stdout
record("T013-12", "log-search --help lists --gap-id; add-gap --help lists the subject flags",
       "--gap-id" in h_ls and all(f_ in h_ag for f_ in ("--parameter", "--identity", "--icf", "--needs",
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
        p = cli("log-search", "--results-found", "1", "--slug", SLUG, "--language", LANG, "--jurisdiction", JUR, "--query-text", "stem probe",
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
     "w1200": "The width is 120.0 mm.", "h": "A height of 12,00 m.", "cl": "See clause 1.2 (00) for this.",
     "rooms": "Rooms 1, 200 mm apart.", "lead": "A lip of .5 in.", "lead2": "A width of 12 mm.", "lead3": "A lip of 5 in.",
     "sp20": "A ramp is not steeper than 1 : 20 where the run exceeds 12 m.", "z": "The scale is 5 000:1 200 here.",
     "fn": "The clear width is 1200\u00b9 mm.", "apos": "The width is 1'200 mm.", "apos2": "The width is 1\u2019200 mm.",
     "list": "Widths of 100,200,300 mm are offered.",
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
    for n, name, q_, cv, w in [
            ("50", "1200 with '1,200' under '120.0 mm' (a decimal shift: the wording is not in the quote)", "w1200", "1200", "1,200"),
            ("51", "1.2 with '1,200' under '120.0 mm'", "w1200", "1.2", "1,200"),
            ("52", "1200 with '1,200' under '12,00 m'", "h", "1200", "1,200"),
            ("53", "1200 with '1,200' under 'clause 1.2 (00)'", "cl", "1200", "1,200"),
            ("54", "1.2 with '1,200' under 'rooms 1, 200 mm apart'", "rooms", "1.2", "1,200"),
            ("55", ".12 under '12 mm' (a leading-dot decimal is a decimal)", "lead2", ".12", None),
            ("56", ".5 under '5 in'", "lead3", ".5", None), ("57", "5 under 'a lip of .5 in'", "lead", "5", None),
            ("58", "1:20 under the kanji sentence for 1:12 with the kanji wording of 1:12", "kanji", "1:20", "十二分の一"),
            ("59", "99 under the kanji sentence with the wording 十二", "kanji", "99", "十二"),
            ("60", "1:12 under '1 : 20 where the run exceeds 12 m' (a spaced colon is still a ratio)", "sp20", "1:12", None),
            ("61", "0 under '5 000:1 200' (the padded piece 000 is not a number)", "z", "0", None),
            ("62", "0:1 under '5 000:1 200'", "z", "0:1", None)]:
        r = rv(q_, cv, w)
        record(f"T008-{n}", f"refused: {name}", r is not None and "Nothing was written" in r, r)
    for n, name, q_, cv, w in [
            ("63", "0.5 under 'a lip of .5 in'", "lead", "0.5", None),
            ("64", "1200 under '1200\u00b9 mm' (a footnote mark is not a digit)", "fn", "1200", None),
            ("65", "1200 under \"1'200 mm\" (apostrophe grouping)", "apos", "1200", None),
            ("66", "1200 under '1\u2019200 mm'", "apos2", "1200", None),
            ("67", "200 under '100,200,300 mm' (comma groups are numbers as well)", "list", "200", None),
            ("68", "1:20 under '1 : 20'", "sp20", "1:20", None)]:
        res, err = ok(db._require_verbatim, Q[q_], t8, "--claim-text", "T008", claimed_value=cv, value_as_written=w,
                      claim_type="numerical")
        record(f"T008-{n}", f"accepted: {name}", err is None, err)
    # THE RESIDUAL, shown plainly: a wording with no numeral is not checked for meaning (rule 8: no word list),
    # so one word of the quote (the longest, derived) defeats the guard for each headline refusal above, and so
    # does one letter. A reviewer and the adversarial pass are the check; these cases are accepted ON PURPOSE.
    for n, q_, cv in [("01", "dec", "12"), ("02", "time", "0.6"), ("03", "ratio", "1:1"), ("04", "ratio", "112"),
                      ("05", "space", "120.0"), ("06", "in", "1:8"), ("07", "r20", "1:12"), ("08", "w1200", "1200")]:
        word = max(re.findall(r"[^\W\d_]+", Q[q_]), key=len)
        res, err = ok(db._require_verbatim, Q[q_], t8, "--claim-text", "T008", claimed_value=cv, value_as_written=word,
                      claim_type="numerical")
        record(f"T008-RES-{n}", f"RESIDUAL (accepted on purpose): {cv} under {Q[q_]!r} with the wording {word!r}", err is None, err)
    res, err = ok(db._require_verbatim, Q["dec"], t8, "--claim-text", "T008", claimed_value="12", value_as_written="m",
                  claim_type="numerical")
    record("T008-RES-09", "RESIDUAL (accepted on purpose): 12 under 'no higher than 1.2 m' with the one-letter wording 'm'",
           err is None, err)
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
    record("T008-44", "amend-extraction refuses a wording that is not in the stored quote",
           r is not None and "literal span" in r, r)
    r = refusal(db.amend_extraction, eid, "value_as_written", "Vijf  PROCENT", "probe", session=S, dry_run=True)
    record("T008-49", "...and a wording that is the quote's words in other case or spacing (a literal span only)",
           r is not None and "literal span" in r, r)
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
    record("T008-46", "amend-extraction refuses a wording on a row whose quote states the number as a numeral",
           r is not None and "states every claimed number" in r, r)
    h = cli("add-extraction", "--help")
    record("T008-47", "add-extraction takes --value-as-written", "--value-as-written" in h.stdout, h.stdout[-200:])


print("Section T016: the writer refuses a figure the engine cannot read, a unit that is a sentence, a numerical row with no comparator, and a derived figure that disagrees with its inputs")
# The sentences are test text, one per case, each holding the figure it claims. Every case that expects a
# refusal is one the writer accepted before T-016 (red on the unchanged code); N7, N7b and N10 are controls.
T16 = {"pct": "A ramp gradient of 8.33% is the greatest permitted.", "slash": "The fall is 1/12 over the run.",
       "inv": "A slope of 12:1 is shown on the drawing.", "ok": "Ramps are to be not steeper than 1:12 along the run.",
       "cond": "Where the height difference is at most 0.05 m a ramp is to be not steeper than 1:12.",
       "qual": "The surface is to be slip-resistant when wet.", "base": "The first flight rises 5.5 percent.",
       "delta": "The second flight rises 9.25 percent.", "good": "The combined rise is 14.75 percent.",
       "bad": "The combined rise is 99 percent.",
       "bad2": "The total rise is 99 percent.",
       "bare": "A gradient of 0.0833 is the greatest permitted.", "m77": "The grand rise is 77 percent.",
       "x25": "A third step rises 0.25 percent.", "x50": "A fourth step rises 50 percent.",
       "sum": "The summed rise is 5.75 percent.", "contrast": "Text contrast is to be at least 4.5:1.",
       "d1": "The first segment is 0.1 m long.", "d2": "The second segment is 0.2 m long.",
       "d3": "The whole is 0.3 m long.",
       "ge": "The first landing rises at least 5.5 percent.", "dge": "The second landing rises at least 9.25 percent.",
       "mmd": "The third flight rises 9.25 millimetres.", "nloc": "The fourth flight rises 5.5 percent.",
       "nquo": "The fifth flight rises 5.5 percent.", "ge3": "The third landing rises at least 1 percent.", "two": "The sixth flight rises 2 percent.",
       "rat1": "The first ramp is graded 1:12 along the run.", "rat2": "The second ramp is graded 1:14 along the run.",
       "nu1": "The first run measures 5.5 overall.", "nu2": "The second run measures 9.25 overall.",
       "skim1": "The skimmed rise is 3 percent.", "cond1": "Where the rise is 4 percent the ramp is short.",
       "contra1": "The disputed rise is 6 percent.", "prose1": "The seventh flight rises 2 percent.",
       "relf": "The relating flight rises 7 percent.", "g1": "The g one flight rises 1 percent.",
       "g2": "The g two flight rises 2 percent.", "pa1": "The pa one flight rises 10 percent.",
       "pa2": "The pa two flight rises 4.75 percent."}
RR = "rise:run ratio"
with scratch() as c:
    t16 = new_source(verified=True)
    held_text(t16, "\n".join(T16.values()))
    hand_scan(c, t16, "full")
    pid = P_ACTIVE[0]
    counts = lambda: (c.execute("SELECT COUNT(*) FROM source_value_extractions").fetchone()[0],
                      c.execute("SELECT COUNT(*) FROM extraction_relations").fetchone()[0])

    def w(sentence, value, unit, comparator, claim_type="numerical", **over):
        """A dry-run write of one row through add-extraction's writer: (refusal text or None, error text or None)."""
        row = extraction(t16, pid, claim_text=T16[sentence], claimed_value=value, claimed_unit=unit,
                         comparator=comparator, claim_type=claim_type, **over)
        return (refusal(db.insert_extraction, row, session=S, dry_run=True, relations=[]),
                ok(db.insert_extraction, row, session=S, dry_run=True, relations=[])[1])

    for tid, name, sentence, value, unit, cmp_, want in [
            ("N1", "8.33% is refused and the message says to put % in --claimed-unit", "pct", "8.33%", "%", "<=", "put % in --claimed-unit"),
            ("N2", "1/12 in a gradient unit is refused (it reads as 0.083 %)", "slash", "1/12", RR, "<=", "not 1/12"),
            ("N3", "12:1 is an inverted ratio and is refused", "inv", "12:1", RR, "<=", "inverted"),
            ("N4", "a unit that is a sentence is refused and the message names condition_on", "cond", "1:12",
             RR + " (maximum) where the height difference is <= 0.05 m", "<=", "condition_on"),
            ("N4b", "a unit holding a min/max word alone is refused", "ok", "1:12", RR + " max", "<=", "condition_on"),
            ("N4c", "a unit holding a clause separator alone is refused", "ok", "1:12", RR + "; relaxed", "<=", "condition_on"),
            ("N4f", "a unit holding a comparator symbol alone is refused", "ok", "1:12", "m>=", "<=", "condition_on"),
            ("N4d", "a unit holding a number standing alone is refused and the message sends it to --claimed-value", "ok", "1:12",
             "per 100 m", "<=", "--claimed-value"),
            ("N4e", "a unit holding a parenthesis alone is refused", "ok", "1:12", "ratio (new build)", "<=", "condition_on"),
            ("N5", "a ratio under a unit that is not 'rise:run ratio' is refused", "ok", "1:12", "ratio", "<=", "rise:run ratio"),
            ("N6", "a value-supplying numerical row with no comparator is refused", "ok", "1:12", RR, None, "--comparator")]:
        r, err = w(sentence, value, unit, cmp_)
        record(f"T016-{tid}", name, r is not None and want in r and "Nothing was written" in r, r or err)
    r, err = w("ok", "1:12", RR, "<=")
    record("T016-N7", "control: 1:12 in 'rise:run ratio' with a comparator is accepted", r is None and err is None, r or err)
    r, err = w("qual", "slip-resistant", None, None, claim_type="qualitative")
    record("T016-N7b", "control: a qualitative claim with no unit and no comparator is accepted", r is None and err is None, r or err)
    # dbcore.figure_refusal directly: the cases the verb cannot reach (a range; a value with no digit) and the one the sketch raised on.
    fr = lambda *a: ok(lambda: dbcore.figure_refusal(*a))
    res, err = fr("1:6 to 14:1", RR, "between", "range")
    record("T016-N3b", "a range with an inverted end (1:6 to 14:1) is refused", err is None and res and "inverted" in res, err or res)
    res, err = fr("1:6 to 1:14", RR, "between", "range")
    record("T016-N7c", "a range of two ratios (1:6 to 1:14) is read: None, and no exception", err is None and res is None, err or res)
    # N8 builds its own no-digit value: the stored row that once served as the probe is a defective row a repair removes.
    res, err = fr("twelve", "%", "<=", "numerical")
    record("T016-N8", "a value with no numeral is refused and the message names --value-as-written",
           err is None and res and "--value-as-written" in res, err or res)
    # The fix-naming of each branch (a generic "cannot be placed" text would also refuse these).
    for tid, args, want in [("N8b", ("30,0", "mm", "=", "numerical"), "decimal comma"),
                            ("N8c", ("1 in 12", RR, "<=", "numerical"), "1:12"),
                            ("N8d", ("0-4.8", "%", "between", "range"), "'a to b'")]:
        res, err = fr(*args)
        record(f"T016-{tid}", f"figure_refusal{args[:2]} names its fix ({want})", err is None and res and want in res, err or res)
    # THE ENGINE'S OWN READING decides what a bare figure means (finding: a bare 12 under 'rise:run ratio' is read as 12 %).
    for tid, name, sentence, value, unit, want in [
            ("N12", "a bare 12 under 'rise:run ratio' is refused (read as 12 %)", "ok", "12", RR, "a:b"),
            ("N12b", "a decimal 0.0833 under 'rise:run ratio' is refused", "bare", "0.0833", RR, "a:b"),
            ("N12c", "1/12 with no unit is refused (no scale)", "slash", "1/12", None, "not 1/12")]:
        r, err = w(sentence, value, unit, "<=")
        record(f"T016-{tid}", name, r is not None and want in r, r or err)
    res, err = fr("1/12", "m", "<=", "numerical")
    exact = dbcore.bound_on_scale("1/12", "m", "<=", "numerical")
    record("T016-N12d", "REJECTED part of the finding: 1/12 in metres is accepted, and the engine reads it exactly as stated (1/12 m)",
           err is None and res is None and exact == (None, Fraction(1, 12)), (res, exact))
    # An a:b under another unit: a defined outcome that does not loop, and following its advice works.
    r, err = w("contrast", "4.5:1", "contrast ratio", ">=")
    record("T016-N13", "4.5:1 under 'contrast ratio' is refused with a route that is not 'use rise:run ratio'",
           r is not None and "second term is 1" in r and "only under" in r, r or err)
    r, err = w("contrast", "4.5", "contrast ratio", ">=")
    record("T016-N13b", "...and the single number 4.5 under 'contrast ratio' is accepted", r is None and err is None, r or err)
    ratio_rows = q("SELECT extraction_id, claimed_value FROM source_value_extractions WHERE claimed_unit='ratio' "
                   "AND claim_type IN (SELECT value FROM json_each(?))", json.dumps(list(dbcore.QUANTITY_CLAIM_TYPES)))
    record("T016-N13c", "the stored a:b rows under the unit 'ratio' (not a family member) are refused on re-check, as history; "
           "the family table says why", dbcore.notation_family("ratio") is None and all(
               dbcore.figure_refusal(r_["claimed_value"], "ratio", "<=", "numerical") for r_ in ratio_rows),
           [r_[0] for r_ in ratio_rows])
    # Non-ASCII digits: refused whatever the colon.
    for tid, args in [("N14", ("\uff11\uff12\uff10\uff10", "mm", "=", "numerical")), ("N14b", ("\uff11:\uff11\uff12", RR, "<=", "numerical")),
                      ("N14c", ("\u0661\u0662", "mm", "=", "numerical")), ("N14d", ("\uff11\uff1a\uff11\uff12", RR, "<=", "numerical"))]:
        res, err = fr(*args)
        record(f"T016-{tid}", f"a non-ASCII digit is refused: {args[0]!r}", err is None and res and "ASCII digits" in res, err or res)
    # Units: structural tests, no word list. Ordinary units pass; the stored distinct units that look like a plain unit keep passing.
    plain = ["cd/m2", "m2", "mm2", "m/s2", "kg/m3", "N/mm2", "W/m2K", "min", "m/min", "l/min", "steps/min", "dB (A)", "dB(A)",
             "m^2", "cd m-2", "cd/m\u00b2", "minutes", "max"]
    record("T016-N15", "ordinary units are accepted (no typography or word decides)", not [u for u in plain if dbcore.unit_refusal(u)],
           [u for u in plain if dbcore.unit_refusal(u)])
    live_units = [r_[0] for r_ in q("SELECT DISTINCT claimed_unit FROM source_value_extractions WHERE claimed_unit IS NOT NULL")]
    plain_live = [u for u in live_units if re.fullmatch(r"[A-Za-z%:]+(?: [A-Za-z%:]+)?", u)]
    record("T016-N15b", "every stored unit of one or two plain words is still accepted", plain_live and not [u for u in plain_live if dbcore.unit_refusal(u)],
           [u for u in plain_live if dbcore.unit_refusal(u)])
    record("T016-N15c", "RESIDUAL, shown plainly: a sentence-like unit with no structural mark passes until units are data (T-030)",
           dbcore.unit_refusal("ratio where steep") is None)
    # A derived row has no quote and no locator of its own (OD-40): its words are its inputs' and the warrant is a word of the source's saved text.
    derived = lambda value, **over: extraction(t16, pid, **{"claimed_value": value, "claim_text": None, "claimed_unit": "%", "comparator": "=",
                                                           "figure_role": "derived", "source_section": None, "loc_section": None,
                                                           "lens_basis_text": "combined", **over})
    r = refusal(db.insert_extraction, derived("14.75", comparator=None), session=S, dry_run=True, relations=[])
    record("T016-N6b", "a DERIVED numerical row with no comparator is refused for the comparator", r is not None and "--comparator" in r, r)

    # THE DERIVED ARITHMETIC, one home (db._refuse_derived_mismatch). Base and delta are written for real on the scratch copy.
    def numbered(sentence, value, **over):
        return extraction(t16, pid, claim_text=T16[sentence], claimed_value=value, **{"claimed_unit": "%", "comparator": "=", **over})

    base_id = db.insert_extraction(numbered("base", "5.5"), session=S, dry_run=False, relations=[])["extraction_id"]
    delta_id = db.insert_extraction(numbered("delta", "9.25"), session=S, dry_run=False, relations=[])["extraction_id"]
    edges = [{"relation": "derived_from", "to_extraction": base_id, "stated": "named", "quote": T16["base"], "input_role": "base"},
             {"relation": "derived_from", "to_extraction": delta_id, "stated": "named", "quote": T16["delta"], "input_role": "delta"}]
    before = counts()
    r = refusal(db.insert_extraction, derived("99"), session=S, dry_run=False, relations=edges)
    record("T016-N9", "a derived 99 over 5.5 + 9.25 is refused at write and nothing is written",
           r is not None and "disagrees" in r and counts() == before, (r, counts(), before))
    res, err = ok(db.insert_extraction, derived("14.75"), session=S, dry_run=True, relations=edges)
    record("T016-N10", "control: a derived 14.75 over 5.5 + 9.25 is accepted", err is None, err)

    # derive-extraction (T-063): no comparator, unit, quote or locator is asked for; they are the inputs'.
    r = refusal(db.derive_extraction, ref_id=t16, parameter_id=pid, base=base_id, delta=delta_id, **lens_of(T16["good"]),
                session=S, identity=IDENT, claimed_value="99")
    record("T016-N11", "derive-extraction with a wrong --claimed-value is refused by the shared check, nothing written",
           r is not None and "disagrees with its own base + delta" in r and counts() == before, (r, counts(), before))
    res, err = ok(db.derive_extraction, ref_id=t16, parameter_id=pid, base=base_id, delta=delta_id, **lens_of(T16["good"]),
                  session=S, identity=IDENT)
    xid = (res or {}).get("extraction_id")
    stored = c.execute("SELECT claimed_value, comparator, claimed_unit, figure_role, claim_text, source_section FROM source_value_extractions "
                       "WHERE extraction_id=?", (xid,)).fetchone()
    record("T016-N11a", "derive-extraction with no --claimed-value computes and stores 14.75",
           err is None and stored is not None and stored[0] == "14.75", err or stored)
    edges_of = c.execute("SELECT to_extraction_id, input_role FROM extraction_relations WHERE from_extraction_id=? AND relation='derived_from' "
                         "ORDER BY input_role", (xid,)).fetchall()
    view = c.execute("SELECT stored, recomputed FROM v_derived_figure_check WHERE derived_id=?", (xid,)).fetchall()
    record("T016-N11c", "derive-extraction with no comparator, unit, quote or locator is accepted: comparator and unit are the inputs', two edges, "
           "the view recomputes it (was KNOWN DEFECT 1/3)",
           err is None and stored is not None and tuple(stored)[1:] == ("=", "%", "derived", None, None)
           and [tuple(e) for e in edges_of] == [(base_id, "base"), (delta_id, "delta")]
           and len(view) == 1 and view[0][0] == view[0][1] == 14.75,
           (err, tuple(stored or ()), [tuple(e) for e in edges_of], [tuple(v) for v in view]))

    def landing(sentence, value, **over):
        return db.insert_extraction(numbered(sentence, value, **over), session=S, dry_run=False, relations=[])["extraction_id"]

    def derive(base, delta, **over):
        return dict(ref_id=t16, parameter_id=pid, base=base, delta=delta, **lens_of(T16["good"]), session=S, identity=IDENT, **over)

    ge_id, dge_id = landing("ge", "5.5", comparator=">="), landing("dge", "9.25", comparator=">=")
    before = counts()
    r = refusal(db.derive_extraction, **derive(base_id, dge_id))
    record("T063-01", "a point base plus a delta bounded '>=' is not a bound: refused, nothing written",
           r is not None and "is not a bound" in r and counts() == before, (r, counts(), before))
    res, err = ok(db.derive_extraction, **derive(ge_id, delta_id))
    cmp_ = c.execute("SELECT comparator, claimed_value FROM source_value_extractions WHERE extraction_id=?",
                     ((res or {}).get("extraction_id"),)).fetchone()
    record("T063-02", "a '>=' base plus a point delta keeps the bound: stored comparator '>=', value 14.75",
           err is None and cmp_ is not None and tuple(cmp_) == (">=", "14.75"), err or cmp_)
    res, err = ok(db.derive_extraction, **derive(dge_id, landing("ge3", "1", comparator=">=")))
    cmp_ = c.execute("SELECT comparator, claimed_value FROM source_value_extractions WHERE extraction_id=?",
                     ((res or {}).get("extraction_id"),)).fetchone()
    record("T063-09", "two '>=' figures add and keep the bound: stored comparator '>=', value 10.25",
           err is None and cmp_ is not None and tuple(cmp_) == (">=", "10.25"), err or cmp_)
    mm_id = landing("mmd", "9.25", claimed_unit="mm")
    before = counts()
    r = refusal(db.derive_extraction, **derive(base_id, mm_id))
    record("T063-03", "a base in % and a delta in mm are refused, both units named, nothing written",
           r is not None and "stated in" in r and "'%'" in r and "'mm'" in r and "--conversion-note" not in r and counts() == before,
           (r, counts(), before))
    nloc_id = landing("nloc", "5.5")
    hand("UPDATE source_value_extractions SET source_section=NULL, loc_section=NULL WHERE extraction_id=?", nloc_id)
    before = counts()
    r = refusal(db.derive_extraction, **derive(nloc_id, delta_id))
    record("T063-04", "a base with no locator is refused, and the message names the input",
           r is not None and r.startswith("R3: derived figure's input") and str(nloc_id) in r and counts() == before, (r, counts(), before))
    sig = inspect.signature(db.derive_extraction).parameters
    record("T063-05", "derive-extraction takes no comparator, claimed_unit, conversion_note or claim_text",
           not {"comparator", "claimed_unit", "conversion_note", "claim_text"} & set(sig), sorted(sig))
    r = refusal(db.insert_extraction, {**derived("14.75"), "claim_text": T16["good"]}, session=S, dry_run=True, relations=edges)
    record("T063-06", "a derived row given a claim_text is refused: a figure a source states in words is a claim row",
           r is not None and "claim row" in r and "claim_text" in r, r)
    nquo_id = landing("nquo", "5.5")
    hand("UPDATE source_value_extractions SET claim_text=NULL WHERE extraction_id=?", nquo_id)
    before = counts()
    r = refusal(db.derive_extraction, **derive(nquo_id, delta_id))
    record("T063-07", "an input with no quote is refused, and the message names the input",
           r is not None and str(nquo_id) in r and "no quote" in r and counts() == before, (r, counts(), before))
    tier0 = c.execute("SELECT tier FROM evidence_sources WHERE ref_id=?", (t16,)).fetchone()[0]
    hand("UPDATE evidence_sources SET tier=5 WHERE ref_id=?", t16)
    res, err = ok(db.derive_extraction, **derive(ge_id, landing("two", "2"), dry_run=True))
    hand("UPDATE evidence_sources SET tier=? WHERE ref_id=?", tier0, t16)
    record("T063-10", "a derived figure over a regulatory-stratum source needs no pinpoint of its own: its inputs' locators stand", err is None, err)
    h = cli("derive-extraction", "--help")
    record("T063-08", "derive-extraction --help offers no --comparator, --claimed-unit, --conversion-note or --claim-text, and says --ref-id is only a check",
           not any(f in h.stdout for f in ("--comparator", "--claimed-unit", "--conversion-note", "--claim-text")) and "--ref-id" in h.stdout and "CHECK" in h.stdout,
           h.stdout[-300:])
    # A derived row is written whole: both inputs, or nothing (the critic of T-063: a one-edge derived 999 was accepted).
    before = counts()
    r = refusal(db.insert_extraction, derived("99"), session=S, dry_run=False, relations=edges[:1])
    record("T063-11", "a derived row with ONE input edge is refused at write: base AND delta are both required, nothing written",
           r is not None and "base AND one carrying --input-role delta" in r and counts() == before, (r, counts(), before))
    r = refusal(db.insert_extraction, {**derived("14.75"), "claim_type": "qualitative"}, session=S, dry_run=False, relations=edges)
    record("T063-12", "a derived row that is not a numerical claim is refused", r is not None and "numerical" in r, r)

    # T063-13..: the critic of T-063 (a derived row must never state a figure its inputs do not support).
    r1, r2 = landing("rat1", "1:12", claimed_unit="rise:run ratio"), landing("rat2", "1:14", claimed_unit="rise:run ratio")
    before = counts()
    r = refusal(db.derive_extraction, **derive(r1, r2, claimed_value="1:2"))
    record("T063-13", "two ratios are not summed, and a typed --claimed-value does not make them so: refused, nothing written",
           r is not None and "cannot be summed" in r and counts() == before, (r, counts(), before))
    nu1, nu2 = landing("nu1", "5.5", claimed_unit=None), landing("nu2", "9.25", claimed_unit=None)
    r = refusal(db.derive_extraction, **derive(nu1, nu2, claimed_value="99"))
    record("T063-14", "two figures with no unit are not summed either", r is not None and "cannot be summed" in r, r)
    r = refusal(db.derive_extraction, **derive(r1, r2))
    record("T063-13b", "the same two ratios with no typed value: refused as not summable, not a crash", r is not None and "cannot be summed" in r, r)
    rat_edges = [{"relation": "derived_from", "to_extraction": r1, "stated": "named", "quote": T16["rat1"], "input_role": "base"},
                 {"relation": "derived_from", "to_extraction": r2, "stated": "named", "quote": T16["rat2"], "input_role": "delta"}]
    before = counts()
    r = refusal(db.insert_extraction, {**derived("1:2"), "claimed_unit": "rise:run ratio", "comparator": "="}, session=S,
                dry_run=False, relations=rat_edges)
    record("T063-13c", "through the Python writer too: a derived row whose pair no check can recompute is refused ('nothing can recompute it')",
           r is not None and "nothing can recompute" in r and counts() == before, (r, counts(), before))
    sk = landing("skim1", "3")
    hand("UPDATE source_value_extractions SET extraction_method='skim' WHERE extraction_id=?", sk)
    r = refusal(db.derive_extraction, **derive(sk, delta_id))
    record("T063-15", "an input read by a skim (not publishable) is refused, and the message says so",
           r is not None and "not publishable" in r and str(sk) in r, r)
    cond = landing("cond1", "4", figure_role="condition")
    r = refusal(db.derive_extraction, **derive(cond, delta_id))
    record("T063-16", "a condition row is not an input of a sum", r is not None and "condition" in r and str(cond) in r, r)
    contra = landing("contra1", "6")
    hand("UPDATE source_value_extractions SET extraction_status='contradicted' WHERE extraction_id=?", contra)
    r = refusal(db.derive_extraction, **derive(contra, delta_id))
    record("T063-17", "a contradicted input is refused", r is not None and "contradicted" in r, r)
    r = refusal(db.derive_extraction, **{**derive(base_id, delta_id), "ref_id": "REF-99999"})
    record("T063-18", "a --ref-id that is not the inputs' source is refused (the flag is a check, not a choice)",
           r is not None and "not the inputs' source" in r, r)
    # a regulatory-stratum input with only a PROSE locator is refused, as a claim row of the same shape is (R3)
    prose = landing("prose1", "2")
    hand("UPDATE source_value_extractions SET source_section='clause 4', loc_section=NULL WHERE extraction_id=?", prose)
    tier0 = c.execute("SELECT tier FROM evidence_sources WHERE ref_id=?", (t16,)).fetchone()[0]
    hand("UPDATE evidence_sources SET tier=5 WHERE ref_id=?", t16)
    r = refusal(db.derive_extraction, **derive(ge_id, prose, dry_run=True))
    hand("UPDATE evidence_sources SET tier=? WHERE ref_id=?", tier0, t16)
    record("T063-19", "on a tier-5 source an input with only a prose section is refused: the pinpoint hierarchy is owed",
           r is not None and "pinpoint" in r and str(prose) in r, r)
    # a derived figure is not turned into a claim with no words, nor given another comparator, nor left stale
    d_ok = db.derive_extraction(**derive(landing("g1", "1"), landing("g2", "2")))["extraction_id"]
    r = refusal(db.amend_extraction, d_ok, "figure_role", "claim", "T063 probe", session=S)
    record("T063-20", "a derived row cannot be amended into a claim: it has no words of its own", r is not None and "no words of its own" in r, r)
    r = refusal(db.amend_extraction, d_ok, "comparator", "<=", "T063 probe", session=S)
    record("T063-21", "a derived row's comparator is its inputs': amending it is refused", r is not None and "its inputs'" in r, r)
    inp = c.execute("SELECT to_extraction_id FROM extraction_relations WHERE from_extraction_id=? AND input_role='base'", (d_ok,)).fetchone()[0]
    r = refusal(db.amend_extraction, inp, "comparator", ">=", "T063 probe", session=S)
    record("T063-22", "an input's comparator cannot be amended under a derived row that computed its bound from it",
           r is not None and "input of derived" in r, r)
    # relate-extraction writes the same input rules as derive-extraction (one home: the edge writer)
    rel_from = landing("relf", "7", figure_role="finding")
    r = refusal(db.relate_extraction, rel_from, "derived_from", S, to_extraction=nloc_id, stated="named",
                quote=T16["nloc"], input_role="delta")
    record("T063-23", "relate-extraction refuses a derived_from edge to an input with no locator", r is not None and "no locator" in r, r)
    # two derivations that differ in INPUTS but state the same result are not copies of each other
    a1, a2 = landing("pa1", "10"), landing("pa2", "4.75")
    res, err = ok(db.derive_extraction, **derive(a1, a2, dry_run=False))
    record("T063-24", "a second derivation of 14.75 from DIFFERENT inputs is a second row, not a byte-identical copy", err is None, err)
    r = refusal(db.derive_extraction, **derive(a1, a2))
    record("T063-25", "...and the same inputs again are the copy, refused", r is not None and "exact row" in r, r)

    # --- amend-extraction to `derived` runs the same arithmetic (the `77` row), and an incomplete row is checked when it completes
    base_edge = {"to_extraction": base_id, "stated": "named", "quote": T16["base"], "input_role": "base"}
    delta_edge = {"to_extraction": delta_id, "stated": "named", "quote": T16["delta"], "input_role": "delta"}

    def finding_row(sentence, value):
        return db.insert_extraction(numbered(sentence, value, figure_role="finding"), session=S, dry_run=False,
                                    relations=[])["extraction_id"]

    def edge(row_id, e):
        return refusal(db.relate_extraction, row_id, "derived_from", S, **e)

    f77 = finding_row("m77", "77")
    for e in (base_edge, delta_edge):
        edge(f77, e)
    r = refusal(db.amend_extraction, f77, "figure_role", "derived", "T016 probe", session=S)
    role = c.execute("SELECT figure_role FROM source_value_extractions WHERE extraction_id=?", (f77,)).fetchone()[0]
    record("T016-N16", "amend-extraction to derived refuses a 77 over 5.5 + 9.25 and leaves the role as it was",
           r is not None and "disagrees" in r and role == "finding", (r, role))
    fok = finding_row("good", "14.75")
    for e in (base_edge, delta_edge):
        edge(fok, e)
    res, err = ok(db.amend_extraction, fok, "figure_role", "derived", "T016 probe", session=S)
    record("T016-N16b", "control: amend-extraction to derived accepts a 14.75 over 5.5 + 9.25", err is None, err)
    fnone = finding_row("sum", "5.75")
    r = refusal(db.amend_extraction, fnone, "figure_role", "derived", "T016 probe", session=S)
    record("T016-N16c", "amend-extraction to derived with no edges at all names the missing base edge",
           r is not None and "input_role=base" in r, r)
    # --- every base x delta pair is checked, in either edge order (5.5 + 0.25 = 5.75, but 5.5 + 50 is not)
    d25 = db.insert_extraction(numbered("x25", "0.25"), session=S, dry_run=False, relations=[])["extraction_id"]
    d50 = db.insert_extraction(numbered("x50", "50"), session=S, dry_run=False, relations=[])["extraction_id"]
    e25 = {"to_extraction": d25, "stated": "named", "quote": T16["x25"], "input_role": "delta"}
    e50 = {"to_extraction": d50, "stated": "named", "quote": T16["x50"], "input_role": "delta"}
    three = lambda order: [{"relation": "derived_from", **e} for e in order]
    before = counts()
    for tid, order in [("N17", (base_edge, e25, e50)), ("N17b", (base_edge, e50, e25))]:
        r = refusal(db.insert_extraction, derived("5.75"), session=S, dry_run=False, relations=three(order))
        record(f"T016-{tid}", "a derived 5.75 over 5.5 and two deltas, 0.25 and 50, is refused at write (any edge order)",
               r is not None and "disagrees" in r and counts() == before, (r, counts(), before))
    pair = db.insert_extraction(derived("5.75"), session=S, dry_run=False, relations=three((base_edge, e25)))["extraction_id"]
    before = counts()
    r = edge(pair, e50)
    record("T016-N17c", "...and the third edge, filed afterwards with relate-extraction, is refused", r is not None and "disagrees" in r
           and counts() == before, (r, counts(), before))
    # --- the tolerance is the integrity check's (0.1 + 0.2 stored as 0.3), not exact equality
    ids = [db.insert_extraction(numbered(s_, v_, claimed_unit="m"), session=S, dry_run=False, relations=[])["extraction_id"]
           for s_, v_ in (("d1", "0.1"), ("d2", "0.2"))]
    tol = [{"relation": "derived_from", "to_extraction": ids[0], "stated": "named", "quote": T16["d1"], "input_role": "base"},
           {"relation": "derived_from", "to_extraction": ids[1], "stated": "named", "quote": T16["d2"], "input_role": "delta"}]
    res, err = ok(db.insert_extraction, derived("0.3", claimed_unit="m"), session=S, dry_run=True, relations=tol)
    record("T016-N18", "a derived 0.3 over 0.1 + 0.2 (0.30000000000000004 in binary) is accepted: the tolerance is not exact equality",
           err is None, err)
    # --- a finding amended to a value-supplying role needs the comparator the writer would have required
    nocmp = db.insert_extraction(numbered("qual", "slip", figure_role="finding", claim_type="qualitative", claimed_unit=None,
                                          comparator=None), session=S, dry_run=False, relations=[])["extraction_id"]
    fnum = db.insert_extraction(numbered("ok", "1:12", figure_role="finding", claimed_unit=RR, comparator=None), session=S,
                                dry_run=False, relations=[])["extraction_id"]
    r = refusal(db.amend_extraction, fnum, "figure_role", "claim", "T016 probe", session=S)
    record("T016-N19", "amend-extraction finding -> claim on a numerical row with no comparator is refused for the comparator",
           r is not None and "--comparator" in r, r)
    res, err = ok(db.amend_extraction, nocmp, "figure_role", "claim", "T016 probe", session=S)
    record("T016-N19b", "control: ...a non-numerical row needs none", err is None, err)
    ok(db.amend_extraction, fnum, "comparator", "<=", "T016 probe", session=S)
    res, err = ok(db.amend_extraction, fnum, "figure_role", "claim", "T016 probe", session=S)
    record("T016-N19c", "control: ...and with the comparator set it is accepted", err is None, err)
# ───────────── T-009: quote normalisation and name screens outside Latin script ─────────────
print("Section T009: normalise_quote keeps a mark that is part of a word outside Latin, Greek and Cyrillic, drops a stray "
      "one, and folds every decimal digit; the name screens read any script")
import unicodedata  # noqa: E402
_PROBES = REPO / "scratchpad/session_2026-11-12-pipeline-bidirectional-audit/stress/results3/probes/log.jsonl"
_NUMERIC = ("dec", "indian", "swiss", "german")                 # the probe keys that are numbers, not words
_nq, _L = retrieval_log.normalise_quote, unicodedata.lookup
try:
    _per = json.loads(json.loads(_PROBES.read_text(encoding="utf-8").splitlines()[0])["argv"][-1])
except Exception as _exc:  # noqa: BLE001
    _per = None
    for _t in ("T009-01", "T009-02", "T009-03", "T009-04", "T009-05"):
        skip(_t, f"the retained probe log is unreadable ({type(_exc).__name__})")
if _per is not None:
    _marked = {}
    for _k, _v in _per.items():
        if not _k.startswith(_NUMERIC):
            _marked.setdefault(_k.split("-")[0], []).append((_k, _v))
    _clash = [(a, b) for m in _marked.values() for i, (a, x) in enumerate(m) for b, y in m[i + 1:] if _nq(x) == _nq(y)]
    _lone = [g for g, m in _marked.items() if len(m) < 2]
    record("T009-01", "strings of one script that differ only in a mark (Devanagari, Thai, Hebrew, Arabic, kana) normalise "
           "differently, and every group has a pair to compare", len(_marked) >= 2 and not _lone and not _clash, (_lone, _clash))
    _digits = {k: re.sub(r"\D", "", _nq(v)) for k, v in _per.items() if k.startswith("dec-")}
    _same = {d for k, d in _digits.items() if k != "dec-6.0"}
    record("T009-02", "every decimal digit folds to ASCII: 0.6, 0,6, full-width, Arabic-Indic and Devanagari spellings share one "
           "digit run, 6.0 does not", len(_same) == 1 and _digits["dec-6.0"] not in _same, _digits)
    _nt = retrieval_log.number_tokens
    record("T009-03", "0.6 s and 0,6 s still read as the same number through T-008's reader",
           bool(_nt(_per["dec-0.6"])) and _nt(_per["dec-0.6"]) == _nt(_per["dec-comma"]), (_nt(_per["dec-0.6"]), _nt(_per["dec-comma"])))
    _names = [v for k, v in _per.items() if not k.startswith(_NUMERIC)]
    _empty = [v for v in _names if not db._name_tokens(v)]
    record("T009-04", "a name in any script yields a non-empty token set", bool(_names) and not _empty, _empty)
    _vb = [k for k in ("dec-fullwidth", "dec-arabic-indic", "dec-devanagari") if not db._VALUE_BEARING_NAME.search(_per[k])]
    record("T009-05", "a name carrying a full-width, Arabic-Indic or Devanagari digit is value-bearing", not _vb, _vb)
_KA, _GA = _L("HIRAGANA LETTER KA"), _L("HIRAGANA LETTER GA")
record("T009-06", "an accent on a Latin letter still folds (Pérez meets Perez) and the voicing mark of か が still differs",
       _nq("P\u00e9rez") == _nq("Perez") and _nq(_KA) != _nq(_GA), (_nq(_KA), _nq(_GA)))
# What a mark is attached to decides whether it stays (the adversarial pass on T-009 found each of these on a live artefact or by probe).
_ACUTE = _L("ACUTE ACCENT")                                     # a SPACING accent: NFKC makes it a space and a combining mark
record("T009-07", "a spacing accent used as an apostrophe is nothing (landlord´s meets landlord's), and a lone accent, "
       "a lone vowel sign or an emoji selector leaves no text",
       _nq("landlord" + _ACUTE + "s") == _nq("landlord's") and _nq(_ACUTE) == "" and _nq(" " + _ACUTE + " \n") == ""
       and _nq(_L("HEBREW POINT HIRIQ")) == "" and _nq(_L("HEAVY CHECK MARK") + "\ufe0f") == "",
       [_nq("landlord" + _ACUTE + "s"), _nq(_ACUTE), _nq(_L("HEBREW POINT HIRIQ"))])
_THAI = (_L("THAI CHARACTER NO NEN"), _L("THAI CHARACTER MAI THO"), _L("THAI CHARACTER NIKHAHIT"), _L("THAI CHARACTER SARA AA"))
record("T009-08", "Thai sara am typed as one letter (sara am) and as the extractor writes it (nikhahit, tone, sara aa) are one quote",
       _nq(_THAI[0] + _THAI[1] + _L("THAI CHARACTER SARA AM")) == _nq(_THAI[0] + _THAI[2] + _THAI[1] + _THAI[3]),
       [_nq(_THAI[0] + _THAI[1] + _L("THAI CHARACTER SARA AM")), _nq(_THAI[0] + _THAI[2] + _THAI[1] + _THAI[3])])
_VS = chr(0xE0100)                                              # an ideographic variation selector
record("T009-09", "a variation selector between two ideographs is not part of the word",
       _nq("\u845b" + _VS + "\u98fe\u533a") == _nq("\u845b\u98fe\u533a"), None)
_signs = [_L(n) for n in ("FULLWIDTH LESS-THAN SIGN", "SMALL EQUALS SIGN", "LESS-THAN OVER EQUAL TO", "NOT GREATER-THAN")]
_digit_names = [_L("CIRCLED DIGIT ONE"), _L("SUPERSCRIPT TWO"), _L("VULGAR FRACTION ONE HALF")]
_miss = [c for c in _signs + _digit_names if not db._VALUE_BEARING_NAME.search("width " + c)]
record("T009-10", "a name carrying a non-ASCII comparator, a circled or superscript digit or a fraction is value-bearing; the ASCII "
       "plain name is not", not _miss and not db._VALUE_BEARING_NAME.search("ramp gradient"), _miss)
# _near_terms compares against an alias of ANY language: take a live, non-seed, non-English alias of two or more tokens whose own term
# has no English form that would find it anyway, and offer a name that contains it.
def _en_forms(tid):
    return [r[0] for r in q("SELECT canonical_en FROM terms WHERE term_id=? UNION ALL SELECT alias FROM term_aliases "
                            "WHERE term_id=? AND upper(language)='EN' AND attestation<>'model_seed'", tid, tid)]
_al = [(t, a) for t, a in q("SELECT term_id, alias FROM term_aliases WHERE upper(language)<>'EN' AND attestation<>'model_seed' "
                            "ORDER BY term_id, alias") if len(db._name_tokens(a)) >= 2]
# A near match needs a shared token, so an alias none of whose tokens occurs in any English form of its own term can be found only through the alias.
_al = [(t, a) for t, a in _al if not any(db._name_tokens(a) & db._name_tokens(f) for f in _en_forms(t))]
if not _al:
    skip("T009-11", "no live non-English, non-seed alias of two or more tokens that no English form of its term would also find")
else:
    _t, _a = _al[0]
    record("T009-11", "_near_terms finds a term through an alias in a language other than English",
           any(h[0] == _t for h in db._near_terms(con, _a + " zzprobe")), (_t, _a))

# ───────────── T-010: add-parameter refuses a term filed under a lens, method or legal domain ─────────────
print("Section T010: add-parameter refuses a term whose domain holds lenses, methods or bodies of law, adapts the next action "
      "to the term's declination, and amend-term can correct a term's domain")
_NQ = getattr(dbcore, "NON_QUANTITY_DOMAINS", None)
# The six the T-010 task names are a floor the rule may grow from, not shrink from (a pin of a judged rule, not a second home).
_TASK_SIX = {"functional_axis", "population", "medical", "methodology", "legal", "economics"}
if feature("T010-01", "the rule dbcore.NON_QUANTITY_DOMAINS exists, holds at least the six the task names, and every member is a "
           "domain some term carries (a member no term carries is stale)", _NQ is not None, "dbcore.NON_QUANTITY_DOMAINS"):
    record("T010-01", "the rule holds at least the six the task names, and every member is a domain some term carries",
           _TASK_SIX <= set(_NQ) and all(scalar("SELECT COUNT(*) FROM terms WHERE domain=?", d) for d in _NQ), sorted(_NQ))

    def _terms(domain):
        """Terms of `domain` that are not parameters and carry no digit: a declined one counts (the refusal precedes the
        declination test, and following the refusal's own advice must not starve these cases)."""
        return [t for (t,) in q("SELECT term_id FROM terms WHERE domain=? AND term_id NOT IN (SELECT term_id FROM base_parameters) "
                                "AND canonical_en NOT GLOB '*[0-9]*' ORDER BY term_id", domain)]

    def _undeclined(domain):
        return [t for t in _terms(domain) if not scalar("SELECT COUNT(*) FROM parameter_declinations WHERE term_id=?", t)]

    _live = [r[0] for r in q("SELECT DISTINCT t.domain FROM base_parameters p JOIN terms t USING (term_id) "
                             "WHERE t.domain IS NOT NULL ORDER BY 1")]
    _bad, _skipped = [], []
    for _d in sorted(_NQ):
        _ts = _terms(_d)
        if not _ts:
            _skipped.append(_d)
            continue
        _r = refusal(db.insert_parameter, _ts[0], S, dry_run=True)
        if not (_r and repr(_d) in _r and "decline-parameter" in _r and "amend-term --term-id" in _r
                and "Nothing was written" in _r and str(sorted(_NQ)) in _r and str(_live) in _r
                and scalar("SELECT COUNT(*) FROM base_parameters WHERE term_id=?", _ts[0]) == 0):
            _bad.append((_d, _r))
    for _d in _skipped:
        skip(f"T010-02/{_d}", f"no non-parameter term in the refused domain {_d!r}")
    record("T010-02", "add-parameter refuses a term of EVERY refused domain, naming the domain, both ways out, the refused set and the "
           "live parameters' domains, and writes nothing", not _bad and len(_skipped) < len(_NQ), _bad)

    _legal = _undeclined("legal")
    _fa = _undeclined("functional_axis")
    if not _legal or len(_fa) < 4:
        skip("T010-03", "no free legal term, or fewer than four free functional_axis terms")
    else:
        _vars = []
        for _t, _dirty in ((_legal[0], " Legal"), (_fa[0], "functional-axis"), (_fa[1], "FUNCTIONAL_AXIS ")):
            _was = scalar("SELECT domain FROM terms WHERE term_id=?", _t)
            hand("UPDATE terms SET domain=? WHERE term_id=?", _dirty, _t)
            _vars.append(refusal(db.insert_parameter, _t, S, dry_run=True))
            hand("UPDATE terms SET domain=? WHERE term_id=?", _was, _t)
        record("T010-03", "the rule reads the column as free text: ' Legal', 'functional-axis' and 'FUNCTIONAL_AXIS ' are refused",
               all(_vars), _vars)
    _ok_dom = next((d for d in _live if _undeclined(d)), None)
    if _ok_dom is None:
        skip("T010-04", "no free term in a domain a live parameter has")
    else:
        _res, _err = ok(db.insert_parameter, _undeclined(_ok_dom)[0], S, dry_run=True)
        record("T010-04", f"a free term of a live parameter's domain ({_ok_dom}) is still promoted (dry run)", _err is None, _err)
    record("T010-05", "no live parameter sits in a refused domain",
           not {dbcore.domain_key(d) for d in _live} & set(_NQ), _live)
    # The refusal precedes the declination test, and says the truthful thing for each state of the declination.
    if len(_fa) < 4 or not _legal:
        skip("T010-06", "too few free terms to decline one")
    else:
        db.decline_parameter(_fa[2], "T010 probe: a lens term", S)
        _r = refusal(db.insert_parameter, _fa[2], S, dry_run=True)
        record("T010-06", "a DECLINED term in a refused domain gets the domain refusal, and is told it is already declined "
               "(not told to decline it again)", _r and "standing declination" in _r and "nothing to decline" in _r
               and "--field domain" in _r, _r)
        db.decline_parameter(_legal[0], "T010 probe: a body of law", S)
        hand("UPDATE parameter_declinations SET revoked_at='2026-01-01 00:00', revoked_by_session=?, revocation_reason='T010 probe' "
             "WHERE term_id=?", S, _legal[0])
        _r = refusal(db.insert_parameter, _legal[0], S, dry_run=True)
        record("T010-07", "a term whose declination was REVOKED, in a refused domain, is told decline-parameter cannot repeat it "
               "and that the domain is the way out", _r and "REVOKED" in _r and "--field domain" in _r
               and "decline-parameter --term-id" not in _r, _r)
    _mis = _fa[3] if len(_fa) > 3 else None
    if _mis is None or _ok_dom is None:
        skip("T010-08", "no free functional_axis term or no live parameter domain to move it to")
    else:
        _own = scalar("SELECT domain FROM terms WHERE term_id=?", _mis)
        _held = [r[0] for r in q("SELECT DISTINCT domain FROM terms WHERE domain IS NOT NULL AND term_id<>?", _mis)]
        _none = "zz_" + _ok_dom
        _r = refusal(db.amend_term, _mis, "domain", _none, "T010 probe", S, dry_run=True)
        _same, _e0 = ok(db.amend_term, _mis, "domain", _own, "T010 probe", S, dry_run=True)
        record("T010-08", "amend-term --field domain: a domain no other term carries is refused and every held domain is listed "
               "(quoted, so the echoed replacement cannot satisfy it); the current domain is a no-op, not a refusal",
               _none not in _held and _r and all(repr(d) in _r for d in _held) and "Nothing was written" in _r
               and _e0 is None and _same["changed"] is False, (_r, _same, _e0))
        _res, _err = ok(db.amend_term, _mis, "domain", _ok_dom, "T010 probe: a quantity filed under the wrong domain", S, dry_run=True)
        record("T010-09", "amend-term --field domain to a domain another term carries is accepted (dry run) and writes nothing",
               _err is None and _res["changed"] and scalar("SELECT domain FROM terms WHERE term_id=?", _mis) == _own, _err or _res)
        db.amend_term(_mis, "domain", _ok_dom, "T010 probe: a quantity filed under the wrong domain", S)
        _note = scalar("SELECT scope_note FROM terms WHERE term_id=?", _mis) or ""
        _res, _err = ok(db.insert_parameter, _mis, S, dry_run=True)
        record("T010-10", "after the real amend, the old domain and the reason are recorded in the term's trail, and the term the "
               "refusal turned away is promoted (dry run)",
               _err is None and f"domain was: '{_own}'" in _note and "a quantity filed under the wrong domain" in _note
               and scalar("SELECT domain FROM terms WHERE term_id=?", _mis) == _ok_dom, (_err, _note[-200:]))
    _p = scalar("SELECT p.term_id FROM base_parameters p JOIN terms t USING (term_id) ORDER BY 1")
    if _p is None:
        skip("T010-11", "no live parameter")
    else:
        _rs = {d: refusal(db.amend_term, _p, "domain", d, "T010 probe", S, dry_run=True) for d in sorted(_NQ)
               if scalar("SELECT COUNT(*) FROM terms WHERE domain=? AND term_id<>?", d, _p)}
        record("T010-11", "amend-term refuses to move a term that is already a parameter into ANY refused domain",
               bool(_rs) and all(v and "already a parameter" in v for v in _rs.values()), _rs)


# ───────────── T-015: a language is one of the map's, whatever its letter case ─────────────
print("Section T015: the coverage views fold a language to the map's case; observe-term and add-source refuse a language the "
      "map does not hold and store the map's spelling; an English source sorts as English in any case")
_MAP = [r[0] for r in q("SELECT DISTINCT language FROM lang_jur_map ORDER BY 1")]
record("T015-01", "the coverage views hold one row per slug and language: the distinct languages of v_coverage_language equal the "
       "folded distinct languages of the searches, and no (slug, language) pair is split by case in either view",
       scalar("SELECT COUNT(DISTINCT language) FROM v_coverage_language")
       == scalar("SELECT COUNT(DISTINCT UPPER(language)) FROM search_executions WHERE deferred_reason IS NULL")
       and scalar("SELECT COUNT(*) FROM (SELECT slug, UPPER(language) FROM v_coverage_language GROUP BY 1, 2 HAVING COUNT(*) > 1)") == 0
       and scalar("SELECT COUNT(*) FROM (SELECT slug, parameter_id, jurisdiction, UPPER(language), identity_code, icf_code, needs_code "
                  "FROM v_coverage_lens GROUP BY 1,2,3,4,5,6,7 HAVING COUNT(*) > 1)") == 0
       and scalar("SELECT COUNT(*) FROM v_coverage_language WHERE language <> UPPER(language)") == 0, None)
with scratch() as c:                   # every search stored in lower case: neither view may notice (the live log holds both spellings)
    _snap = lambda: ([tuple(r) for r in c.execute("SELECT slug, language, searches, admitted FROM v_coverage_language ORDER BY 1, 2")],  # noqa: E731
                     [tuple(r) for r in c.execute("SELECT slug, parameter_id, jurisdiction, language, identity_code, icf_code, needs_code, "
                                                  "searches, deferred FROM v_coverage_lens ORDER BY 1, 2, 3, 4, 5, 6, 7")])
    _before = _snap()
    hand("UPDATE search_executions SET language=LOWER(language)")
    _after = _snap()
    hand("UPDATE search_executions SET language=UPPER(language)")
    _upper = _snap()
    record("T015-02", "storing EVERY search as lower case, and then as upper case, changes neither view in any row or figure: both "
           "views read the language, not its spelling", bool(_before[0]) and bool(_before[1]) and _before == _after == _upper,
           (len(_before[0]), len(_after[0]), len(_before[1]), len(_after[1])))
_absent = next("".join(p) for p in itertools.product("ABCDEFGHIJKLMNOPQRSTUVWXYZ", repeat=2) if "".join(p) not in _MAP)
_ref15 = new_source()
_obs15 = {"ref_id": _ref15, "surface_form": "clause", "locator": "p1", "context_quote": "a clause read off paper",
          "verbatim_exempt": "scanned PDF, no text layer"}
r = refusal(db.observe_term, {**_obs15, "language": _absent.lower()}, S, dry_run=True)
record("T015-03", "observe-term refuses a language lang_jur_map does not hold, whatever its case, naming the map",
       r and "lang_jur_map" in r and repr(_absent.lower()) in r and "--language" in r, r)
_held = next((l for l in _MAP if l != "EN"), None)
with scratch() as c:
    if _held is None:
        for _t in ("T015-04", "T015-05", "T015-07"):
            skip(_t, "lang_jur_map holds no language besides EN")
    else:
        _r15 = new_source()
        res, err = ok(db.observe_term, {**_obs15, "ref_id": _r15, "language": _held.lower()}, S, dry_run=False)
        record("T015-04", "observe-term stores a held language in the map's spelling, however it was typed",
               err is None and c.execute("SELECT language FROM observed_terms WHERE ref_id=?", (_r15,)).fetchone()[0] == _held, err)
        _src = {**SRC, "title": "Fixture on handrail finial profiles and a T015 probe"}
        _bad = refusal(db.insert_evidence_source, {**_src, "lang_detected": _absent.lower()}, S, dry_run=True, authors=AUTH)
        _id15, _e15 = ok(db.insert_evidence_source, {**_src, "title": _src["title"] + " two", "lang_detected": _held.lower()}, S,
                         dry_run=False, authors=AUTH)
        record("T015-05", "add-source refuses a --lang-detected the map does not hold, naming that flag and the map, and stores a held "
               "one in the map's spelling", _bad and "lang_jur_map" in _bad and "--lang-detected" in _bad and _e15 is None
               and c.execute("SELECT lang_detected FROM evidence_sources WHERE ref_id=?", (_id15,)).fetchone()[0] == _held, (_bad, _e15))
        # The map's spelling is READ, not assumed upper: with the map holding the language in lower case, both spellings are accepted
        # and the stored value is the map's.
        hand("UPDATE lang_jur_map SET language=LOWER(language) WHERE language=?", _held)
        _id16, _e16 = ok(db.insert_evidence_source, {**_src, "title": _src["title"] + " three", "lang_detected": _held}, S,
                         dry_run=False, authors=AUTH)
        record("T015-07", "the writers store the map's own spelling: with the map holding the language in lower case, an upper-case "
               "--lang-detected is accepted and stored in lower case",
               _e16 is None and c.execute("SELECT lang_detected FROM evidence_sources WHERE ref_id=?", (_id16,)).fetchone()[0] == _held.lower(),
               _e16)
        hand("UPDATE lang_jur_map SET language=UPPER(language) WHERE language=?", _held.lower())
    # An English source is English whatever its spelling: of two unmined sources of one tier, the Japanese one comes first and the
    # English one after it, `EN` or `en`, though the English one sorts earlier by slug and label.
    _un = [r for r in db.get_unmined_for_all_slugs(6)]
    _tier = next((t for t in sorted({r["tier"] for r in _un}) if len([r for r in _un if r["tier"] == t]) >= 2), None)
    if _tier is None:
        skip("T015-06", "no tier with two unmined sources")
    else:
        _two = sorted((r for r in _un if r["tier"] == _tier), key=lambda r: (r["slug"], r["local_ref_id"]))[:2]
        _ids = [c.execute("SELECT ref_id FROM source_slug_links WHERE slug=? AND local_ref_id=?", (r["slug"], r["local_ref_id"])).fetchone()[0]
                for r in _two]
        _res = []
        for _spelling in ("EN", "en"):
            hand("UPDATE evidence_sources SET lang_detected=?, language=NULL WHERE ref_id=?", _spelling, _ids[0])
            hand("UPDATE evidence_sources SET lang_detected='ja', language=NULL WHERE ref_id=?", _ids[1])
            _order = [r["local_ref_id"] for r in db.get_unmined_for_all_slugs(6) if r["tier"] == _tier]
            _res.append(_order.index(_two[1]["local_ref_id"]) < _order.index(_two[0]["local_ref_id"]))
        record("T015-06", "an English source sorts after a non-English one of its tier whether it is stored `EN` or `en`", all(_res), _res)


print("Section T061: amend-extraction reformats in place (OR-3)")
with scratch() as c:
    # T-061 (OR-3): a stored figure is reformatted in place, same numbers and quote, or not at all.
    # The rows are written VALID through the writer, then put into the history shape the writer now
    # refuses by HAND (that shape can no longer be written), then reformatted back through the verb.
    T61 = {"pct":   "The longitudinal gradient is not to exceed 6% where the rise is at most 0.6 m.",
           "ratio": "Every ramp in the survey had a slope of 1:20 over its full length.",
           "comma": "Somente 30,0 % dos predios possuem inclinacao maxima.",
           "range": "The inclination varied between 0 to 4.8 degrees across the trials.",
           "mm":    "The clear width of the passage is to be 1200 mm at least.",
           "qual":  "The surface is to be firm, stable and slip resistant.",
           "words": "A rise of 1:12 is the most that is allowed on a short ramp."}
    ref = new_source(verified=True)
    held_text(ref, "\n".join(T61.values()))
    hand_scan(c, ref, "full")
    P = P_ACTIVE[0]

    def put_row(key, value, unit, cmp_="<=", ctype="numerical", role="claim"):
        return db.insert_extraction(extraction(ref, P, claim_text=T61[key], claimed_value=value,
                                               claimed_unit=unit, comparator=cmp_, claim_type=ctype,
                                               figure_role=role), session=S, dry_run=False,
                                    relations=[])["extraction_id"]

    def row(xid):
        return c.execute("SELECT * FROM source_value_extractions WHERE extraction_id=?", (xid,)).fetchone()

    def amend(x, f, v):
        return db.amend_extraction(x, f, v, "T061 fixture", session=S, dry_run=False)

    A = put_row("pct", "6", "%")
    B = put_row("ratio", "1:20", "rise:run ratio")
    C = put_row("comma", "30.0", "%", "=", role="finding")
    D = put_row("range", "0 to 4.8", "degrees", "between", "range", "condition")
    E = put_row("mm", "1200", "mm", ">=")
    F = put_row("qual", "firm", None, None, "qualitative", "finding")
    G = put_row("words", "1:12", "rise:run ratio")
    # HAND: each row into the shape the writer now refuses (what T-108 finds in the stored history).
    for xid, v, u in ((A, "6%", "% longitudinal gradient (maximum) where the rise is at most 0.6 m"),
                      (B, "1:20", "rise:run ratio (preferred maximum)"), (C, "30,0", "%"), (D, "0-4.8", "degrees"),
                      (E, "1200", "mm (clear, between handrails)"), (G, "one in twelve", "rise:run ratio")):
        hand("UPDATE source_value_extractions SET claimed_value=?, claimed_unit=? WHERE extraction_id=?", v, u, xid)
    stored_A = dict(row(A))

    def refused(tid, name, x, f, v, needle):
        before = row(x)[f]
        r = refusal(amend, x, f, v)
        record(tid, name, r and needle in r and row(x)[f] == before, r)

    # T061-19..22 (the critic of the first commit): a reformat never names another word of the cell, flips a sign,
    # or leaves a row a byte-identical copy of another. A's cell still holds its conditions at this point and
    # contains the free-standing words `rise`, `is` and `m`.
    for tid, bad in (("T061-19", "m"), ("T061-19b", "gradient"), ("T061-19c", "rise"), ("T061-19d", "the")):
        refused(tid, f"a unit that is another word of the cell (`{bad}`) is refused: the unit LEADS the cell", A, "claimed_unit", bad, "does not lead")
    refused("T061-20", "a unit that is another spelling of the leading one (`MM` for `mm (clear ...)`) is refused", E, "claimed_unit", "MM", "does not lead")
    refused("T061-21", "a range hyphen turned into a minus (`0-4.8` -> `0 to -4.8`) is a different figure", D, "claimed_value", "0 to -4.8", "minus signs")
    E2 = put_row("mm", "1200", "mm", ">=")          # written after E was put into its history shape: not a copy yet
    refused("T061-22", "a unit reformat that would leave the row a byte-identical copy of another is refused", E, "claimed_unit", "mm", "byte-identical copy")
    r, err = ok(amend, A, "claimed_value", "6")
    record("T061-01", "a stored `6%` is reformatted to `6` in place (same number)", err is None and row(A)["claimed_value"] == "6", err)
    r, err = ok(amend, A, "claimed_unit", "%")
    record("T061-02", "then the prose unit is cut to the `%` already in its cell, and the figure reads",
           err is None and not dbcore.unit_refusal(row(A)["claimed_unit"])
           and not dbcore.figure_refusal(row(A)["claimed_value"], row(A)["claimed_unit"], row(A)["comparator"], row(A)["claim_type"])
           and row(A)["claim_text"] == stored_A["claim_text"], err)
    refused("T061-03", "a different number (`6` -> `60`) is a second row, not a reformat", A, "claimed_value", "60", "same numbers")
    refused("T061-04", "a moved decimal point (`1:20` -> `1:2.0`) is refused", B, "claimed_value", "1:2.0", "same numbers")
    refused("T061-05", "a unit that is not a word of the cell (`m` for `mm (clear ...)`, a rescale) is refused", E, "claimed_unit", "m",
            "does not lead")
    refused("T061-06", "a unit that leads the cell but under which the figure does not read (`rise:run` for `1:20`) is refused", B, "claimed_unit", "rise:run",
            "still not be readable")
    r, err = ok(amend, B, "claimed_unit", "rise:run ratio")
    record("T061-07", "the cell's own `rise:run ratio` is accepted and the figure reads",
           err is None and row(B)["claimed_unit"] == "rise:run ratio", err)
    r, err = ok(amend, D, "claimed_value", "0 to 4.8")
    record("T061-08", "`0-4.8` is reformatted to `0 to 4.8`", err is None and row(D)["claimed_value"] == "0 to 4.8", err)
    r, err = ok(amend, C, "claimed_value", "30.0")
    record("T061-09", "a decimal comma (`30,0`) is reformatted to a point", err is None and row(C)["claimed_value"] == "30.0", err)
    r, err = ok(amend, A, "setting", "new buildings")
    record("T061-10", "an EMPTY setting is filled in place", err is None and row(A)["setting"] == "new buildings", err)
    refused("T061-11", "a setting already stated is not overwritten (a different applicability is a second row)", A, "setting",
            "existing buildings", "already states setting")
    r, err = ok(amend, A, "setting", "new buildings")
    record("T061-11b", "re-confirming the stored setting is recorded, not refused (`changed` False)",
           err is None and r and r["changed"] is False, err)
    refused("T061-12", "a qualitative claim's value is not reformatted", F, "claimed_value", "rough", "not a quantity")
    refused("T061-14", "a figure held in words (`one in twelve`) is not given a numeral here: that is a second row with --value-as-written",
            G, "claimed_value", "1:12", "same numbers")
    for tid, col in (("T061-16", "claim_text"), ("T061-16b", "ref_id"), ("T061-16c", "identity_code")):
        before = row(A)[col]
        r = refusal(amend, A, col, "x")
        record(tid, f"an excluded column ({col}) is refused, naming the amendable set, and not written",
               r and "SECOND ROW" in r and row(A)[col] == before, r)
    # GAP-013 (rule 8): the amendable set is DERIVED from the live table; the burden of proof is on the named exclusions.
    if feature("T061-13/15/17", "the amendable set of source_value_extractions is derived (GAP-013)",
               hasattr(db, "_amendable_sve_fields") and hasattr(db, "_NOT_AMENDABLE_SVE"),
               "db._amendable_sve_fields and db._NOT_AMENDABLE_SVE"):
        record("T061-13", "claimed_value and claimed_unit are engine columns (the live-determination refusal covers them) and all three "
               "are amendable", {"claimed_value", "claimed_unit"} <= set(dbcore.ENGINE_EXTRACTION_COLUMNS)
               and {"claimed_value", "claimed_unit", "setting"} <= set(db._amendable_sve_fields(c)), None)
        live = set(dbcore.columns(c, "source_value_extractions"))
        amendable, excluded = set(db._amendable_sve_fields(c)), set(db._NOT_AMENDABLE_SVE)
        record("T061-15", "the amendable columns are the live columns minus the named exclusions: the two partition the table, and every "
               "exclusion is a live column with a reason", amendable | excluded == live and not amendable & excluded and bool(amendable)
               and all(isinstance(w, str) and w.strip() for w in db._NOT_AMENDABLE_SVE.values()),
               (sorted(live - amendable - excluded), sorted(excluded - live)))
        hand("ALTER TABLE source_value_extractions ADD COLUMN zz_t061_probe TEXT")
        record("T061-17", "a column added to the table is amendable until someone names why it must not be (the default is derived, not listed)",
               "zz_t061_probe" in db._amendable_sve_fields(c), None)

print("Section T067: v_coverage_parameter_via_admission is one row per active parameter and owed pair, counted through admissions (OR-8)")
# Nothing below names a count, id or code: the pair, the parameter and the source are chosen by query, and the oracle for the grain is
# the base tables. Everything built is built on a scratch copy and is TASK-FIXTURE.
V67 = "v_coverage_parameter_via_admission"
_COLS67 = "parameter_id, language, jurisdiction, role, searches_naming_parameter, searches_reaching_parameter, sources_admitted"


def view67(c):
    return [tuple(r) for r in c.execute(f"SELECT {_COLS67} FROM {V67} ORDER BY parameter_id, language, jurisdiction")]


try:
    _grain = (scalar(f"SELECT COUNT(*) FROM {V67}"),
              scalar(f"SELECT COUNT(*) FROM (SELECT DISTINCT parameter_id, language, jurisdiction FROM {V67})"),
              scalar("SELECT (SELECT COUNT(*) FROM base_parameters WHERE status='active') * (SELECT COUNT(*) FROM v_research_scope)"))
    record("T067-01", "the view holds one row per active parameter and owed pair: its rows equal its distinct keys and equal the "
           "active parameters times the rows of v_research_scope (a pair with nothing is a row of zeros, never a missing row)",
           _grain[0] == _grain[1] == _grain[2] and _grain[0] > 0, _grain)
    _pick = q(f"SELECT v.parameter_id, v.language, v.jurisdiction FROM {V67} v WHERE v.sources_admitted = 0 AND v.searches_reaching_parameter = 0 "
              "AND EXISTS (SELECT 1 FROM source_value_extractions x WHERE x.parameter_id = v.parameter_id "
              "AND x.claim_type <> 'absent' AND COALESCE(x.extraction_method, '') <> 'skim' "
              "AND NOT EXISTS (SELECT 1 FROM evidence_sources e WHERE e.ref_id = x.ref_id AND e.superseded_by_ref_id IS NOT NULL) "
              "AND NOT EXISTS (SELECT 1 FROM search_admissions sa WHERE sa.ref_id = x.ref_id)) ORDER BY 1, 2, 3 LIMIT 1")
    _err67 = None
except sqlite3.OperationalError as exc:
    _grain, _pick, _err67 = None, [], str(exc)
    record("T067-01", "the view holds one row per active parameter and owed pair", False, _err67)

if _err67 is not None:
    for _t in ("T067-02", "T067-03", "T067-04", "T067-05", "T067-07", "T067-08", "T067-09", "T067-10", "T067-11"):
        record(_t, "the view exists", False, _err67)
elif not _pick:
    for _t in ("T067-02", "T067-03", "T067-05", "T067-07", "T067-08", "T067-09", "T067-10", "T067-11"):
        skip(_t, "no (parameter, owed pair) with nothing admitted and an extraction of that parameter in a source no search admitted")
else:
    P67, L67, J67 = _pick[0]
    SLUG67 = SLUG

    def seed(c, jurisdiction=J67, language=L67, deferred=None):
        """TASK-FIXTURE: a search in the pair that admits a source holding an extraction of the parameter (the source chosen by query)."""
        src = c.execute("SELECT x.ref_id FROM source_value_extractions x WHERE x.parameter_id=? AND x.claim_type <> 'absent' "
                        "AND COALESCE(x.extraction_method, '') <> 'skim' AND NOT EXISTS "
                        "(SELECT 1 FROM evidence_sources e WHERE e.ref_id=x.ref_id AND e.superseded_by_ref_id IS NOT NULL) AND NOT EXISTS "
                        "(SELECT 1 FROM search_admissions sa WHERE sa.ref_id=x.ref_id) ORDER BY x.ref_id LIMIT 1", (P67,)).fetchone()[0]
        cur = c.execute("INSERT INTO search_executions (slug, jurisdiction, language, query_text, engine, depth_method, deferred_reason, "
                        "created_by_session, created_at) VALUES (?,?,?,?,?,?,?,?, '2026-01-01T00:00:00Z')",
                        (SLUG67, jurisdiction, language, "TASK-FIXTURE T067", "manual", "scoping", deferred, S))
        c.execute("INSERT INTO search_admissions (exec_id, ref_id, created_at, created_by_session) VALUES (?,?, '2026-01-01T00:00:00Z', ?)",
                  (cur.lastrowid, src, S))
        c.commit()
        return src

    def only_the_pair_moved(c, src, before, after, pair=(L67, J67)):
        """Exactly the rows of the pair for the ACTIVE parameters the admitted source holds moved, each to (naming 0, reaching 1, sources 1)."""
        held = {r[0] for r in c.execute("SELECT x.parameter_id FROM source_value_extractions x JOIN base_parameters p USING (parameter_id) "
                                        "WHERE x.ref_id=? AND p.status='active' AND x.claim_type <> 'absent' AND COALESCE(x.extraction_method, '') <> 'skim'", (src,))}
        moved = [(b, a) for b, a in zip(before, after) if b != a]
        ok_ = (len(before) == len(after) and P67 in held and {a[0] for _, a in moved} == held
               and all(a[1:3] == pair and a[4:] == (0, 1, 1) and b[4:] == (0, 0, 0) for b, a in moved))
        return ok_, moved

    with scratch() as c:
        before = view67(c)
        src = seed(c)
        same, moved = only_the_pair_moved(c, src, before, view67(c))
        record("T067-02", "a non-deferred search in an owed pair that admits a source holding an extraction of the parameter raises that row's "
               "searches_reaching_parameter and sources_admitted to one and leaves searches_naming_parameter alone; the only other rows that "
               "move are the pair's rows for the other active parameters the same source holds, and no row of any other pair moves",
               same, moved[:3])
    with scratch() as c:
        before = view67(c)
        seed(c, deferred="TASK-FIXTURE: deliberately not searched")
        record("T067-03", "the same search with deferred_reason set leaves every row unchanged (a search that did not run reaches nothing)",
               view67(c) == before, None)
    with scratch() as c:
        before = view67(c)
        src = seed(c, language=L67.lower())
        same, moved = only_the_pair_moved(c, src, before, view67(c))
        record("T067-05", "the same search with the language in lower case counts toward the upper-case pair", same, moved[:3])
    with scratch() as c:        # the direct route: a search logged FOR the parameter counts in searches_naming_parameter, and only there
        before = view67(c)
        c.execute("INSERT INTO search_executions (slug, parameter_id, jurisdiction, language, query_text, engine, depth_method, "
                  "created_by_session, created_at) VALUES (NULL,?,?,?,'TASK-FIXTURE T067','manual','scoping',?, '2026-01-01T00:00:00Z')",
                  (P67, J67, L67, S))
        c.commit()
        moved = [(b, a) for b, a in zip(before, view67(c)) if b != a]
        record("T067-07", "a non-deferred search logged for the parameter in the pair raises that one row's searches_naming_parameter to one "
               "and nothing else (it admitted nothing, so it reaches nothing)",
               len(moved) == 1 and moved[0][1][:3] == (P67, L67, J67) and moved[0][1][4:] == (1, 0, 0), moved)
    with scratch() as c:        # two searches admitting ONE source: two searches reached, one source
        seed(c)
        before = view67(c)
        c.execute("INSERT INTO search_executions (slug, jurisdiction, language, query_text, engine, depth_method, created_by_session, "
                  "created_at) VALUES (?,?,?,'TASK-FIXTURE T067 again','manual','scoping',?, '2026-01-01T00:00:00Z')", (SLUG67, J67, L67, S))
        c.execute("INSERT INTO search_admissions (exec_id, ref_id, created_at, created_by_session) SELECT (SELECT MAX(exec_id) FROM "
                  "search_executions), ref_id, '2026-01-01T00:00:00Z', ? FROM search_admissions WHERE exec_id=(SELECT MAX(exec_id) FROM "
                  "search_executions WHERE query_text='TASK-FIXTURE T067')", (S,))
        c.commit()
        row = [r for r in view67(c) if r[:3] == (P67, L67, J67)][0]
        record("T067-08", "a source admitted by two searches of the pair counts two searches reaching the parameter and one source",
               row[5:] == (2, 1), row)
    with scratch() as c:        # an owed pair whose jurisdiction base_jurisdictions does not hold is still reached (a LEFT roll-up, as v_coverage_priority)
        free = c.execute("SELECT v.language, v.jurisdiction FROM v_research_scope v WHERE v.jurisdiction NOT IN "
                         "(SELECT jurisdiction_code FROM base_jurisdictions) ORDER BY 1, 2 LIMIT 1").fetchone()
        if free is None:
            skip("T067-11", "every owed jurisdiction is registered in base_jurisdictions")
        else:
            c.execute("PRAGMA foreign_keys=OFF")        # HAND: a search the writer would refuse (an unregistered jurisdiction), to pin the LEFT roll-up
            before = view67(c)
            src = seed(c, jurisdiction=free[1], language=free[0])
            same, moved = only_the_pair_moved(c, src, before, view67(c), pair=(free[0], free[1]))
            record("T067-11", "a search in an owed pair whose jurisdiction base_jurisdictions does not hold still counts toward that pair "
                   "(the roll-up is a LEFT join, so an unregistered jurisdiction is itself, not nothing)", same, moved[:3])
    with scratch() as c:        # one search admitting two sources that both hold the parameter: one search reached, two sources
        src = seed(c)
        other = c.execute("SELECT x.ref_id FROM source_value_extractions x WHERE x.parameter_id=? AND x.ref_id<>? AND NOT EXISTS "
                          "(SELECT 1 FROM search_admissions sa WHERE sa.ref_id=x.ref_id) ORDER BY x.ref_id LIMIT 1", (P67, src)).fetchone()
        if other is None:
            skip("T067-10", "no second source holding the parameter that no search admitted")
        else:
            c.execute("INSERT INTO search_admissions (exec_id, ref_id, created_at, created_by_session) VALUES "
                      "((SELECT MAX(exec_id) FROM search_executions), ?, '2026-01-01T00:00:00Z', ?)", (other[0], S))
            c.commit()
            row = [r for r in view67(c) if r[:3] == (P67, L67, J67)][0]
            record("T067-10", "one search admitting two sources that both hold the parameter counts one search reaching it and two sources",
                   row[5:] == (1, 2), row)
    with scratch() as c:        # a parameter no longer active is not owed a reading
        c.execute("UPDATE base_parameters SET status='retired' WHERE parameter_id=?", (P67,))   # HAND: a retired parameter
        c.commit()
        record("T067-09", "a parameter that is not active has no row in the view",
               c.execute(f"SELECT COUNT(*) FROM {V67} WHERE parameter_id=?", (P67,)).fetchone()[0] == 0
               and c.execute(f"SELECT COUNT(*) FROM {V67}").fetchone()[0] > 0, None)
    # A sub-national code rolls up to its country (OD-04). Built on a copy: one held `sub-national` code if any, else HAND.
    with scratch() as c:
        sub = c.execute("SELECT jurisdiction_code FROM base_jurisdictions WHERE kind='sub-national' AND parent_code=? ORDER BY 1 LIMIT 1", (J67,)).fetchone()
        if sub is None:
            sub = (J67 + "-ZZT",)       # TASK-FIXTURE: a subdivision of the pair's own jurisdiction
            c.execute("INSERT INTO base_jurisdictions (jurisdiction_code, kind, parent_code, created_at, created_by_session) "
                      "VALUES (?, 'sub-national', ?, '2026-01-01T00:00:00Z', ?)", (sub[0], J67, S))
        before = view67(c)
        src = seed(c, jurisdiction=sub[0])
        same, moved = only_the_pair_moved(c, src, before, view67(c))
        record("T067-04", "the same search logged with a sub-national code whose parent is the pair's jurisdiction counts toward the parent's row",
               same, moved[:3])

with scratch() as c:
    if _err67 is not None:
        record("T067-06", "the view exists", False, _err67)
    else:
        pair = c.execute("SELECT language, jurisdiction FROM v_research_scope ORDER BY 1, 2 LIMIT 1").fetchone()
        c.execute("UPDATE lang_jur_map SET scope_status='scoped-out' WHERE language=? AND jurisdiction=?", tuple(pair))   # HAND: a scope fill
        c.commit()
        gone = c.execute(f"SELECT COUNT(*) FROM {V67} WHERE language=? AND jurisdiction=?", tuple(pair)).fetchone()[0]
        record("T067-06", "a pair recorded scoped-out leaves the view (every row of it, for every parameter)",
               gone == 0 and view67(c) and c.execute(f"SELECT COUNT(*) FROM {V67}").fetchone()[0]
               == c.execute("SELECT (SELECT COUNT(*) FROM base_parameters WHERE status='active') * (SELECT COUNT(*) FROM v_research_scope)").fetchone()[0],
               gone)




# T067-12..19: the critic of T-067 (migration 140). Seeded on scratch copies; chosen by query as above.
if _err67 is None and _pick:
    def row67(c, par=None):
        return [tuple(r) for r in c.execute(
            f"SELECT parameter_id, language, jurisdiction, searches_ran_in_pair, searches_naming_parameter, searches_reaching_parameter, "
            f"sources_admitted, jurisdiction_registered FROM {V67} WHERE language=? AND jurisdiction=? "
            f"AND (? IS NULL OR parameter_id=?) ORDER BY parameter_id", (L67, J67, par, par))]

    with scratch() as c:
        before = view67(c)
        src = seed(c)
        other = c.execute("SELECT ref_id FROM evidence_sources WHERE ref_id<>? ORDER BY ref_id LIMIT 1", (src,)).fetchone()[0]
        c.execute("UPDATE evidence_sources SET superseded_by_ref_id=? WHERE ref_id=?", (other, src)); c.commit()
        record("T067-12", "a SUPERSEDED source is not a source reached: superseding the admitted source returns the view to what it was (LED-171)",
               view67(c) == before, None)
    with scratch() as c:
        src = seed(c)
        c.execute("UPDATE source_value_extractions SET claim_type='absent', claimed_value=NULL WHERE ref_id=? AND parameter_id=?", (src, P67)); c.commit()
        r = row67(c, P67)[0]
        record("T067-13", "an extraction that records the parameter as ABSENT from the source does not make a search reach it",
               r[5] == 0 and r[6] == 0, r)
    with scratch() as c:
        src = seed(c)
        c.execute("UPDATE source_value_extractions SET extraction_method='skim' WHERE ref_id=? AND parameter_id=?", (src, P67)); c.commit()
        r = row67(c, P67)[0]
        record("T067-14", "a skimmed extraction (not publishable) does not make a search reach the parameter", r[5] == 0 and r[6] == 0, r)
    with scratch() as c:
        _vsql = c.execute("SELECT sql FROM sqlite_master WHERE name=?", (V67,)).fetchone()[0]
        record("T067-15", "every method dbcore calls not publishable is named in the view's filter (the literal is pinned to the constant)",
               bool(dbcore.NOT_PUBLISHABLE_METHODS) and all(f"'{m}'" in _vsql for m in dbcore.NOT_PUBLISHABLE_METHODS), (dbcore.NOT_PUBLISHABLE_METHODS,))
    with scratch() as c:
        before = row67(c, P67)[0]
        for deferred in (None, None, "TASK-FIXTURE: not run"):
            c.execute("INSERT INTO search_executions (slug, jurisdiction, language, query_text, engine, depth_method, deferred_reason, "
                      "created_by_session, created_at) VALUES (?,?,?,?,?,?,?,?, '2026-01-01T00:00:00Z')",
                      (SLUG67, J67, L67, "TASK-FIXTURE T067-16", "manual", "scoping", deferred, S))
        c.commit()
        after = row67(c, P67)[0]
        record("T067-16", "searches that RAN in the pair are counted whatever they were for and whatever they admitted (searched, nothing found is not "
               "unsearched), a deferred one is not, and no other count moves",
               after[3] == before[3] + 2 and after[4:7] == before[4:7], (before, after))
    with scratch() as c:
        for k in range(2):
            c.execute("INSERT INTO search_executions (slug, parameter_id, jurisdiction, language, query_text, engine, depth_method, deferred_reason, "
                      "created_by_session, created_at) VALUES (?,?,?,?,?,?,?,?,?, '2026-01-01T00:00:00Z')",
                      (None, P67, J67, L67, f"TASK-FIXTURE T067-17 {k}", "manual", "scoping", None, S))
        c.execute("INSERT INTO search_executions (slug, parameter_id, jurisdiction, language, query_text, engine, depth_method, deferred_reason, "
                  "created_by_session, created_at) VALUES (?,?,?,?,?,?,?,?,?, '2026-01-01T00:00:00Z')",
                  (None, P67, J67, L67, "TASK-FIXTURE T067-17 deferred", "manual", "scoping", "TASK-FIXTURE: not run", S))
        c.commit()
        r = row67(c, P67)[0]
        record("T067-17", "the searches that name the parameter are counted one by one (two that ran count two; a deferred one is not counted)",
               r[4] == 2, r)
    with scratch() as c:
        _into = c.execute("SELECT parameter_id FROM base_parameters WHERE status='active' AND parameter_id<>? ORDER BY 1 LIMIT 1", (P67,)).fetchone()[0]
        c.execute("UPDATE base_parameters SET status='merged', merged_into=? WHERE parameter_id=?", (_into, P67)); c.commit()
        record("T067-18", "a parameter that is not active (here merged) has no row", row67(c, P67) == [], row67(c, P67))
    with scratch() as c:
        bad = [tuple(r) for r in c.execute(f"SELECT parameter_id, language, jurisdiction, jurisdiction_registered FROM {V67} v "
                                           "WHERE jurisdiction_registered <> (EXISTS (SELECT 1 FROM base_jurisdictions j WHERE j.jurisdiction_code = v.jurisdiction))")]
        record("T067-19", "jurisdiction_registered says whether the pair's jurisdiction is a declared code (a structural zero is not an unsearched pair)",
               bad == [], bad[:3])

# T088-BEGIN
# ---------------------------------------------------------------------------------------------------------------------
print("Section T088: a writer's refusal is kept, and every refusal a batch met is disposed")
# T-088. What a writer refused is the only record of what the batch held and could not write; it was printed once and lost.
# The capture is `dbcore.record_refusal` (one home, called by every place a writer says no); the disposition is
# `scripts/audit/refusal_register.py`. Everything here runs on a TEMPORARY tree that holds its own `scratchpad/CURRENT` and
# session folder (`dbcore.REPO_ROOT` is pointed at it for the call and restored), so no case reaches the real session's record.
import ast  # noqa: E402
import collections  # noqa: E402
import runpy  # noqa: E402
from unittest import mock  # noqa: E402

S88 = "session_2026-11-16-t088-fixture"
_TS88 = re.compile(r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\.\d{6}$")
HAS88 = hasattr(dbcore, "record_refusal")
REG88 = None
try:
    import importlib.util as _ilu
    _spec88 = _ilu.spec_from_file_location("refusal_register", REPO / "scripts" / "audit" / "refusal_register.py")
    REG88 = _ilu.module_from_spec(_spec88)
    _spec88.loader.exec_module(REG88)
except Exception as _exc88:   # noqa: BLE001
    REG88, REG88_ERR = None, f"{type(_exc88).__name__}: {_exc88}"
else:
    REG88_ERR = None


@contextlib.contextmanager
def root88(current=S88, folder=S88):
    """A temporary tree with `scratchpad/CURRENT` (omitted when `current` is None) and a session folder (omitted when
    `folder` is None); `dbcore.REPO_ROOT` points at it inside the block."""
    base = pathlib.Path(tempfile.mkdtemp(prefix="t088-", dir=TMP))
    (base / "scratchpad").mkdir()
    if current is not None:
        (base / "scratchpad" / "CURRENT").write_text(current + "\n", encoding="utf-8")
    if folder:
        (base / "scratchpad" / folder).mkdir()
    old, dbcore.REPO_ROOT = dbcore.REPO_ROOT, base
    try:
        yield base
    finally:
        dbcore.REPO_ROOT = old


def file88(base, stem=S88):
    return base / "scratchpad" / stem / "refusals.jsonl"


def lines88(base, stem=S88):
    f = file88(base, stem)
    return [json.loads(x) for x in f.read_bytes().decode("utf-8-sig").splitlines() if x.strip()] if f.exists() else []


def rid88(rec):
    """What names a refusal line: its refusal_id (a line without one is named by its ts)."""
    return rec.get("refusal_id") or rec["ts"]


def refuse88(argv, sentence="a refusal; Nothing was written.", script="scripts/db.py", **kw):
    """What a caller does at a catch point; returns whatever `record_refusal` returns (it must not raise). The keywords
    (the caller's parsed session and db) are passed only where the function takes them."""
    ok = {k: v for k, v in kw.items() if k in inspect.signature(dbcore.record_refusal).parameters}
    return dbcore.record_refusal(script, argv, sentence, **ok)


def run88(script, *argv):
    """Run `script`'s `__main__` in this process: (exit code or message, or the exception it let propagate, stdout, stderr). `dbcore.REPO_ROOT` is whatever the
    caller's `root88` set, so a refusal it keeps lands in the temporary tree."""
    out, err, old, code = io.StringIO(), io.StringIO(), sys.argv, None
    sys.argv = [script, *argv]
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            runpy.run_path(str(REPO / script), run_name="__main__")
    except SystemExit as exc:
        code = exc.code
    except Exception as exc:   # noqa: BLE001 -- a crash: handed back as the exception, which the script let propagate
        code = exc
    finally:
        sys.argv = old
    return code, out.getvalue(), err.getvalue()


def reg88(*argv):
    """(exit code, stdout, stderr) of `refusal_register.main(argv)`."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            rc = REG88.main(list(argv))
        except SystemExit as exc:
            rc = exc.code
    return rc, out.getvalue(), err.getvalue()


_SUCH88 = "99999999"   # a parameter id no database holds: built by the width, not read from data (add-gap refuses it)
_ARGV88 = ["add-gap", "--category", "SW", "--priority", "P1", "--description", "x", "--session", S88, "--parameter", _SUCH88]
_FIELDS88 = {"refusal_id", "ts", "session", "script", "verb", "argv", "sentence", "db"}

if feature("T088-01", "the capture exists", HAS88, "dbcore.record_refusal"):
    with root88() as b:
        refuse88(_ARGV88, "add-gap parameter_id: no such row. Nothing was written.")
        ls = lines88(b)
    record("T088-01", "a refusal whose argv carries the running session appends exactly one line with its eight fields, a uuid refusal_id, and the verb is the subcommand",
           len(ls) == 1 and set(ls[0]) == _FIELDS88 and _TS88.match(ls[0]["ts"]) and re.fullmatch(r"[0-9a-f]{32}", ls[0]["refusal_id"])
           and ls[0]["session"] == S88 and ls[0]["script"] == "scripts/db.py" and ls[0]["verb"] == "add-gap"
           and ls[0]["argv"] == _ARGV88 and ls[0]["sentence"] == "add-gap parameter_id: no such row. Nothing was written."
           and ls[0]["db"] == "<outside-repo>/guidebook.db", ls)
    with root88() as b:
        refuse88(["--db", "/tmp/some-scratch.db", "--session", S88, "--parameter-id", "3"], "the engine said no", "scripts/assess/assess_cell.py")
        refuse88(["--db", f"{b}/data/in-tree.db", "--session", S88], "the engine said no again", "scripts/assess/assess_cell.py")
        ls = lines88(b)
    record("T088-01b", "the engine's refusal names its own script as the verb; `db` is a repository-relative path, else <outside-repo>/<file name>",
           len(ls) == 2 and ls[0]["verb"] == "assess_cell" and ls[0]["db"] == "<outside-repo>/some-scratch.db" and ls[1]["db"] == "data/in-tree.db", ls)

    # T088-02: not the running session -> nothing is written, and nothing is written outside scratchpad/<stem>/.
    cases = {"another session": (S88, S88, ["add-gap", "--session", "session_other"]),
             "no --session": (S88, S88, ["add-gap", "--category", "SW"]),
             "--session with no value": (S88, S88, ["add-gap", "--session"]),
             "CURRENT missing": (None, S88, ["add-gap", "--session", S88]),
             "CURRENT empty": ("", S88, ["add-gap", "--session", S88]),
             "the folder named differently from CURRENT": (S88, S88 + "-other", ["add-gap", "--session", S88]),
             "no session folder": (S88, None, ["add-gap", "--session", S88]),
             "CURRENT naming a path": ("../escape", None, ["add-gap", "--session", "../escape"]),
             "CURRENT a branch slug whose folder exists": ("my-branch-slug", "my-branch-slug", ["add-gap", "--session", "my-branch-slug"]),
             "CURRENT and --session both ..": ("..", "x", ["add-gap", "--session", ".."]),
             "CURRENT and --session both .": (".", "x", ["add-gap", "--session", "."])}
    wrote = []
    for label, (cur, folder, argv) in cases.items():
        with root88(cur, folder) as b:
            (b / "escape").mkdir()      # where a CURRENT of `../escape` would lead
            refuse88(argv)
            got = [str(p.relative_to(b)) for p in b.rglob("refusals.jsonl")]
            if got:
                wrote.append((label, got))
    record("T088-02", "a call under another session, with no --session, with CURRENT missing, empty, a path, a branch slug, `..` or `.`, with the folder named "
           "differently from CURRENT, or with no folder appends nothing, anywhere", not wrote, wrote)

    # T088-03: the spellings argparse accepts for the session are all the running session.
    spell = {"--session=": ["add-gap", f"--session={S88}"], ".md form": ["add-gap", "--session", S88 + ".md"],
             "prefix --ses": ["add-gap", "--ses", S88], "prefix --se": ["add-gap", "--se", S88], "prefix --s": ["add-gap", "--s", S88],
             "last value wins": ["add-gap", "--session", "session_other", "--session", S88]}
    missed = []
    for label, argv in spell.items():
        with root88() as b:
            refuse88(argv)
            if len(lines88(b)) != 1:
                missed.append(label)
    with root88(S88 + ".md") as b:
        refuse88(["add-gap", "--session", S88])
        if len(lines88(b)) != 1:
            missed.append("CURRENT holding the .md pointer form")
    with root88() as b:                 # the caller's parsed namespace decides, whatever the argv spells
        refuse88(["add-gap", "--x", "1"], session=S88 + ".md")
        n_first = len(lines88(b))
        refuse88(["add-gap", "--session", S88], session="session_other")
        n_second = len(lines88(b))
    if (n_first, n_second) != (1, 1):
        missed.append(f"the parsed session wins over the argv (captured {n_first} then {n_second}, want 1 then 1)")
    record("T088-03", "`--session=S`, `--session S.md`, any argparse prefix down to `--s`, the last of two --session flags, a CURRENT holding the .md form, and "
           "the caller's parsed session (which wins over the argv) are all the running session", not missed, missed)

    # T088-04: never raises, whatever goes wrong while keeping it.
    survived, boom = [], {}
    with root88() as b:
        file88(b).mkdir()      # a directory where the file goes: the append fails (a read-only mode would not, as root)
        try:
            refuse88(_ARGV88)
        except Exception as exc:   # noqa: BLE001
            boom["directory"] = f"{type(exc).__name__}: {exc}"
    for exc_t in (UnicodeEncodeError("utf-8", "x", 0, 1, "bad"), TypeError("not serialisable"), PermissionError("read-only"), OSError("disk full"), ValueError("v")):
        with root88() as b:
            with mock.patch.object(dbcore, "append_line", side_effect=exc_t, create=True):
                try:
                    refuse88(_ARGV88)
                except Exception as exc:   # noqa: BLE001
                    boom[type(exc_t).__name__] = f"{type(exc).__name__}: {exc}"
    with root88() as b:
        with mock.patch.object(dbcore.json, "dumps", side_effect=TypeError("circular")):
            try:
                refuse88(_ARGV88)
            except Exception as exc:   # noqa: BLE001
                boom["json.dumps"] = f"{type(exc).__name__}: {exc}"
    record("T088-04", "a failure while keeping the refusal (a directory in the way, UnicodeEncodeError, TypeError, PermissionError, OSError, a serialising error) "
           "leaves the caller untouched: record_refusal returns, never raises", not boom, boom)
    with root88() as b:      # a byte that is not UTF-8 in argv (a surrogate escape) must be kept, not lost to the encoder
        refuse88(["add-gap", "--session", S88, "--description", "caf\udce9 x"], "bad byte: caf\udce9")
        ls = lines88(b)
        listed = reg88("list", "--session", S88) if REG88 else (None, "", "")
    record("T088-04b", "a non-UTF-8 byte in argv or the sentence is written as an escape, and the line reads back",
           len(ls) == 1 and "caf" in ls[0]["argv"][-1] and "caf" in ls[0]["sentence"] and listed[0] in (None, 1) and "EXAMINED: 1" in (listed[1] or "EXAMINED: 1"), ls)

    # T088-05: privacy, both ways. The file is committed to a public repository and its argv is the replay command: what is
    # private must not reach it, and what is not must come back exactly as it went in.
    LEAK88 = {
        "a URL query": (["--url", "https://x/y.pdf?token=SEKRET&sig=SIG1"], "could not fetch 'https://x/y.pdf?token=SEKRET&sig=SIG1'", ("SEKRET", "SIG1")),
        "URL userinfo": (["--url", "https://bob:HUNTER2@host.example/y"], "bad https://bob:HUNTER2@host.example/y", ("HUNTER2", "bob")),
        "an email address": (["--note", "ask jane.doe@example.org"], "write to jane.doe@example.org", ("jane.doe", "example.org")),
        "--password and a sentence quoting it": (["--password", "PW3"], "the password 'PW3' was refused", ("PW3",)),
        "--api_key": (["--api_key", "KEYONE"], "key KEYONE", ("KEYONE",)),
        "--auth with a scheme": (["--auth", "Bearer BEAR1"], "auth 'Bearer BEAR1'", ("BEAR1",)),
        "--header Authorization": (["--header", "Authorization: Bearer BEAR2"], "header 'Authorization: Bearer BEAR2'", ("BEAR2",)),
        "a Bearer value in prose (no Authorization)": (["--note", "sent Bearer ZZTOP9 upstream"], "sent Bearer ZZTOP9 upstream", ("ZZTOP9",)),
        "an Authorization value that is not Bearer": (["--header", "Authorization: Basic QWxhZGRpbjpvcGVu"], "header 'Authorization: Basic QWxhZGRpbjpvcGVu'", ("QWxhZGRpbjpvcGVu",)),
        "--key": (["--key", "KEYTWO"], "KEYTWO", ("KEYTWO",)),
        "--pat": (["--pat", "PATONE"], "PATONE", ("PATONE",)),
        "-p": (["-p", "PTWO"], "PTWO", ("PTWO",)),
        "--token=v": (["--token=TOK9"], "TOK9", ("TOK9",)),
        "--Password": (["--Password", "PWUP"], "PWUP", ("PWUP",)),
        "--secret-key": (["--secret-key", "SK77"], "SK77", ("SK77",)),
        "--cookie": (["--cookie", "COOK1"], "COOK1", ("COOK1",)),
        "a home path": (["--note", "/home/alice/work /Users/bob/y /root/w"], "saw /home/alice/z and /root/w", ("alice", "bob", "/root/")),
        "a Windows path": (["--note", "C:\\Users\\jane\\x"], "saw C:\\Users\\jane\\x", ("jane",)),
        "~user": (["--note", "~jane/x"], "saw ~jane/x", ("jane",)),
        "the harness scratch form": (["--note", "/tmp/claude-0/-home-jane-guidebook/82388ac1-2e44-55eb-8ade-e982067adc5f/scratchpad/x"],
                                     "in /tmp/claude-0/-home-jane-guidebook/82388ac1-2e44-55eb-8ade-e982067adc5f/scratchpad/x", ("jane", "82388ac1")),
    }
    leaked = []
    for label, (extra, sentence, forbidden) in LEAK88.items():
        with root88() as b:
            refuse88(["add-source", "--session", S88, *extra], sentence)
            raw = file88(b).read_text(encoding="utf-8")
        if any(w in raw for w in forbidden) or "<redacted>" not in raw.replace("<scratch>", "<redacted>").replace("<email>", "<redacted>").replace("~", "<redacted>"):
            leaked.append((label, raw[:300]))
    with root88() as b:
        refuse88(["--session", S88, "--db", f"{b}/data/x.db", "--note", f"{b}/data/x.pdf and /home/alice/w"], f"{b}/data/x.pdf is not held; {b}", "scripts/assess/assess_cell.py")
        ln = lines88(b)[0]
        raw = file88(b).read_text(encoding="utf-8")
    if str(b) in raw or "alice" in raw or ln["argv"][-1] != "data/x.pdf and ~/w" or ln["sentence"] != "data/x.pdf is not held; ." or ln["db"] != "data/x.db":
        leaked.append(("the repository root", ln))
    with root88() as b:
        refuse88(["--session", S88, "--db", "/tmp/claude-0/-home-jane-guidebook/82388ac1-2e44-55eb-8ade-e982067adc5f/s.db"], "x", "scripts/assess/assess_cell.py")
        ln = lines88(b)[0]
    if ln["db"] != "<outside-repo>/s.db":
        leaked.append(("the db field", ln["db"]))
    record("T088-05", "no secret value, URL query or userinfo, email, home or harness path, or a secret quoted in the sentence reaches the line (argv, sentence and db alike)",
           not leaked, leaked)

    DAMAGE88 = ["https://city.example.org/home/accessibility/guide.pdf", "/var/root/x", "/root-dir", "https://x/home/y", "/srv/Users/zed/f",
                "a ~ b and ~/c", "50% of? it", "Smith, J.", "REF-00012", "C:/Program Files/x", "mail: not an address"]
    damaged = []
    for text in DAMAGE88:
        with root88() as b:
            refuse88(["add-gap", "--session", S88, "--tokens", "5", "--author", "Smith", "--keywords", "a b", "--note", text], f"saw {text}")
            ln = lines88(b)[0]
        if ln["argv"][3:] != ["--tokens", "5", "--author", "Smith", "--keywords", "a b", "--note", text] or ln["sentence"] != f"saw {text}":
            damaged.append((text, ln["argv"][3:], ln["sentence"]))
    record("T088-05c", "what is not private comes back exactly: ordinary URLs and words (`--tokens 5`, `--author`, `/var/root/x`, `/root-dir`, `https://x/home/y`) are not rewritten",
           not damaged, damaged)

    with root88() as b:      # through db.py's own main: an unrecognised secret flag is a usage error whose sentence quotes the value
        code, out, err = run88("scripts/db.py", "add-gap", "--category", "SW", "--priority", "P1", "--description", "see https://x/y.pdf?token=SEKRET from /home/alice/w",
                               "--session", S88, "--parameter", _SUCH88, "--api_key", "KEYONE")
        raw = file88(b).read_text(encoding="utf-8") if file88(b).exists() else ""
    record("T088-05d", "through db.py's main, a usage error naming an unrecognised --api_key keeps no secret value, URL query or home path in argv or sentence, and still exits 2 with argparse's words",
           code == 2 and "unrecognized arguments" in err and raw.count("\n") == 1 and not any(w in raw for w in ("SEKRET", "alice", "KEYONE"))
           and '"--api_key", "<redacted>"' in raw and "https://x/y.pdf?<redacted>" in raw, (code, err[-160:], raw[:400]))

    # nothing in any writer's own flags is named like a secret, so the redaction never eats a real value
    _flags = set()
    for _f in (REPO / "scripts").rglob("*.py"):
        if _f.relative_to(REPO / "scripts").parts[0] in ("tests", "migrations"):
            continue
        for _n in ast.walk(ast.parse(_f.read_text(encoding="utf-8"))):
            if isinstance(_n, ast.Call) and getattr(_n.func, "attr", "") == "add_argument":
                _flags.update(a.value for a in _n.args if isinstance(a, ast.Constant) and isinstance(a.value, str) and a.value.startswith("-"))
    _named = sorted(f for f in _flags if dbcore._secret_flag(f)) if hasattr(dbcore, "_secret_flag") else ["no dbcore._secret_flag"]
    record("T088-05b", "no flag of any script under scripts/ is named like a token, secret, password, credential, key, auth or pat (the redaction would hide its value from the record)",
           bool(_flags) and not _named, _named)

    # T088-06: two refusals of one retry loop are two lines with two keys; 24 processes at once are 24 intact lines with 24 ids.
    with root88() as b:
        for _ in range(3):
            refuse88(_ARGV88)
        got = lines88(b)
    record("T088-06", "refusals repeated at once (one retry loop) carry distinct ts and distinct refusal_id, so a disposition names one",
           len(got) == 3 and len({x["ts"] for x in got}) == 3 and len({rid88(x) for x in got}) == 3, got)
    with root88() as b:
        code = ("import sys, pathlib; sys.path.insert(0, 'scripts'); import dbcore; dbcore.REPO_ROOT = pathlib.Path(sys.argv[1]); "
                "dbcore.record_refusal('scripts/db.py', ['add-gap', '--session', sys.argv[2]], 'concurrent; ' + 'x' * 6000)")
        procs = [subprocess.Popen([sys.executable, "-c", code, str(b), S88], cwd=REPO) for _ in range(24)]
        for p_ in procs:
            p_.wait()
        got = lines88(b)
    record("T088-06b", "24 processes refusing at once leave 24 intact lines (large ones included) with 24 distinct refusal_id",
           len(got) == 24 and len({rid88(x) for x in got}) == 24, (len(got), len({rid88(x) for x in got})))

    # T088-19: an interrupted write leaves a stump with no newline; the next append starts its own line.
    with root88() as b:
        refuse88(_ARGV88)
        file88(b).write_bytes(file88(b).read_bytes().rstrip(b"\n")[:-9])
        refuse88(_ARGV88, "after the stump")
        after = file88(b).read_bytes().splitlines()
        try:
            kept = [json.loads(x) for x in after[1:]]
        except ValueError:
            kept = []
        stump_then = reg88("list", "--session", S88) if REG88 else (None, "", "")
        disp = reg88("dispose", "--session", S88, "--id", rid88(kept[0]), "--as", "waived", "--reason", "TASK-FIXTURE: a stump precedes it") if (REG88 and kept) else (None, "", "")
        with open(file88(b), "ab") as fh:
            fh.write(b'{"kind": "disposition", "refus')      # a stump after the disposition too
        refuse88(_ARGV88, "after the second stump")
        final = [x for x in file88(b).read_bytes().splitlines() if x.strip()]
        try:
            last_ok = bool(json.loads(final[-1])["sentence"] == "after the second stump")
            third = json.loads(final[-1])
        except ValueError:
            last_ok, third = False, {"ts": "?"}
        with open(file88(b), "ab") as fh:
            fh.write(b'{"kind": "disposition", "refus')      # a stump, then the disposition of that very refusal
        disp3 = reg88("dispose", "--session", S88, "--id", rid88(third), "--as", "waived", "--reason", "TASK-FIXTURE: dispose after a stump") if REG88 else (None, "", "")
        try:
            disp3_ok = disp3[0] == 0 and json.loads(file88(b).read_bytes().splitlines()[-1])["kind"] == "disposition"
        except ValueError:
            disp3_ok = False
    record("T088-19", "a file ending in a partial line (no newline) gets the next refusal and the next disposition on their own lines: both are readable, `dispose` succeeds "
           "and `list` reads it; the stump alone is reported",
           len(after) == 2 and len(kept) == 1 and kept[0]["sentence"] == "after the stump" and disp[0] == 0 and "PROBLEM line 1: unreadable" in stump_then[1]
           and last_ok and disp3_ok, (after, disp, stump_then, disp3))

# T088-07..: the CLI. Every place a writer says no keeps its sentence, and none of them changes its exit or its words.
if feature("T088-07", "the capture exists", HAS88, "dbcore.record_refusal"):
    real = REPO / "scratchpad" / (REPO / "scratchpad" / "CURRENT").read_text(encoding="utf-8").strip() / "refusals.jsonl"
    size_before = real.stat().st_size if real.exists() else None
    r = cli("add-gap", "--category", "SW", "--priority", "P1", "--description", "x", "--session", "session_fixture", "--parameter", _SUCH88)
    r2 = cli("add-gap", "--category", "NEW-CATEGORY", "--priority", "P1", "--description", "x", "--session", "session_fixture")
    size_after = real.stat().st_size if real.exists() else None
    record("T088-07", "db.py refusing, or failing its usage check, under another session exits as before with the same words, and the real session's refusals.jsonl does not change",
           r.returncode == 1 and r.stderr.startswith("REFUSING: add-gap parameter_id: gaps.parameter_id=") and r.stderr.rstrip().endswith("Nothing was written.")
           and r2.returncode == 2 and "invalid choice: 'NEW-CATEGORY'" in r2.stderr and size_before == size_after, (r.returncode, r.stderr[:160], r2.returncode, size_before, size_after))

    # --- T088-08: one run per place a writer says no, on the CODE, with exit and words checked as they were, and the stored
    # sentence equal to what the process said. The 11 JSON sites of db.py are derived from its source (one case per
    # `_json_refusal(` call, bijectively); the engine's 4th place (an IntegrityError that means two checks drifted) and full_text.py's
    # 4th (an artefact that exists with other bytes) need state no fixture builds: only T088-09 holds those.
    eng = ["scripts/assess/assess_cell.py"]
    asc = ["scripts/db.py", "add-supersession-check", "--slug", "s", "--local-ref", "x", "--ref", "REF-00001", "--tier", "1", "--evidence-type", "clinical",
           "--search-strategy", "{}", "--outcome", "current_best", "--check-method", "pubmed_search", "--session", S88]
    _agm_outcomes = dbcore.schema_choices("gap_mining", "outcome")
    _agm_method = dbcore.schema_choices("gap_mining", "check_method")[0]

    def agm(outcome="deferred", **over):
        a = {"--gap-id": "GAP-001", "--search-strategy": "{}", "--candidates-returned": "0", "--candidates-reviewed": "0", "--outcome": outcome,
             "--check-method": _agm_method, "--session": S88, **over}
        return ["scripts/db.py", "add-gap-mining", *[x for kv in a.items() for x in kv]]

    def swap(argv, flag, value):
        i = argv.index(flag)
        return argv[:i + 1] + [value] + argv[i + 2:]

    json_cases = {
        "asc: search-strategy not JSON": swap(asc, "--search-strategy", "{bad"),
        "asc: refined_by with no dimension": swap(asc, "--outcome", "refined_by"),
        "asc: divergent_no_supersession with no notes": swap(asc, "--outcome", "divergent_no_supersession"),
        "asc: superseded_by with no superseding source": swap(asc, "--outcome", "superseded_by"),
        "asc: co1_addition_logged for another evidence type": swap(asc, "--outcome", "co1_addition_logged"),
        "agm: search-strategy not JSON": agm(**{"--search-strategy": "{bad"}),
        "agm: --discoveries not an array": agm(**{"--discoveries": "{}"}),
        "agm: --candidate-dois not an array": agm(**{"--candidate-dois": "{}"}),
        "agm: closure_evidence_found with no discoveries": agm("closure_evidence_found"),
        "agm: gap_recategorized with no notes": agm("gap_recategorized"),
        "agm: deferred with no notes": agm("deferred"),
    }
    sites = {}
    for label, argv in json_cases.items():
        sites[f"db.py JSON error, {label}"] = (argv, "json", "add-supersession-check" if label.startswith("asc") else "add-gap-mining", "scripts/db.py")
    sites["db.py: a Refusal"] = (["scripts/db.py", *_ARGV88], "str", "add-gap", "scripts/db.py")
    sites["db.py: argparse, an unknown vocabulary term"] = (["scripts/db.py", "add-gap", "--category", "NEW-CATEGORY", "--priority", "P1", "--description", "x", "--session", S88],
                                                            "usage", "add-gap", "scripts/db.py")
    sites["db.py: argparse, a missing required flag of a subcommand"] = (["scripts/db.py", "add-gap", "--session", S88], "usage", "add-gap", "scripts/db.py")
    sites["engine: the canonical-DB guard"] = (eng + ["--db", "data/guidebook.db", "--emit-sql", f"{TMP}/x.sql", "--parameter-id", "1", "--slug", "s", "--session", S88,
                                                      "--stamp", "2026-01-01 00:00"], "stderr1", "assess_cell", eng[0])
    sites["engine: a foreign --stamp"] = (eng + ["--db", DB, "--emit-sql", f"{TMP}/x.sql", "--parameter-id", "1", "--slug", "s", "--session", S88, "--stamp", "bad"],
                                          "stderr2", "assess_cell", eng[0])
    sites["engine: a Refusal, with --db and --session abbreviated"] = (eng + ["--d", DB, "--emit-sql", f"{TMP}/x.sql", "--parameter-id", _SUCH88, "--slug", "s", "--se", S88,
                                                                              "--stamp", "2026-01-01 00:00"], "stderr1", "assess_cell", eng[0])
    sites["engine: argparse, a missing required flag"] = (eng + ["--session", S88], "usage", "assess_cell", eng[0])
    sites["full_text.py: not an admitted source, with --session abbreviated"] = (["scripts/research/full_text.py", "--ref-id", "REF-99999", "--s", S88], "stderr2", "full_text",
                                                                                 "scripts/research/full_text.py")
    sites["full_text.py: argparse, a missing required flag"] = (["scripts/research/full_text.py", "--session", S88], "usage", "full_text", "scripts/research/full_text.py")
    _empty88 = os.path.join(TMP, "t088-empty.sql")
    pathlib.Path(_empty88).write_text("", encoding="utf-8")
    _body88 = os.path.join(TMP, "t088-body.sql")
    pathlib.Path(_body88).write_text("UPDATE gaps SET status = status WHERE gap_id = 'TASK-FIXTURE';\n", encoding="utf-8")
    _tier88 = os.path.join(TMP, "t088-tier.sql")
    pathlib.Path(_tier88).write_text("INSERT INTO evidence_sources (ref_id, tier) VALUES ('REF-1', 9);\n", encoding="utf-8")
    _out88 = os.path.join(TMP, "t088-mig")
    em = ["scripts/emit_data_migration.py", "--session", S88 + ".md", "--summary", "TASK-FIXTURE", "--output-dir", _out88]
    sites["emit_data_migration.py: an empty SQL body"] = (em + ["--input", _empty88], "stderr1", "emit_data_migration", "scripts/emit_data_migration.py")
    sites["emit_data_migration.py: a value outside an audit range"] = (em + ["--input", _tier88], "stderr1", "emit_data_migration", "scripts/emit_data_migration.py")
    sites["emit_data_migration.py: argparse, no --summary"] = (["scripts/emit_data_migration.py", "--session", S88 + ".md"], "usage", "emit_data_migration",
                                                               "scripts/emit_data_migration.py")
    bad, said_all, js_sentences = [], {}, []
    for label, (argv, kind, verb, script) in sites.items():
        with root88() as b:
            code, out, err = run88(*argv)
            ls = lines88(b)
        if kind == "json":
            ok, said = code == 2 and out.startswith('{"error"'), (json.loads(out.splitlines()[0])["error"] if out.startswith('{"error"') else None)
        elif kind == "str":
            ok, said = isinstance(code, str) and code.startswith("REFUSING: ") and not err, (code or "")[len("REFUSING: "):]
        elif kind == "usage":
            ok = code == 2 and "usage:" in err and "error:" in err
            said = err.split("error: ", 1)[1].rstrip("\n") if "error: " in err else None
        else:
            ok = code == int(kind[-1]) and err.startswith("REFUSING: ") and out == ""
            said = err[len("REFUSING: "):].rstrip("\n")
        if label.startswith("emit_data_migration.py: an empty") or label.startswith("emit_data_migration.py: a value"):
            ok = code == 1 and "ERROR" in err
            said = " ".join(x.strip() for x in err.splitlines())
        if not ok:
            bad.append((label, "exit/words changed", code, out[:100], err[:160]))
        elif len(ls) != 1 or ls[0]["verb"] != verb or ls[0]["script"] != script or ls[0]["sentence"] != dbcore._scrub(said):
            bad.append((label, "kept line wrong (verb, script, or the sentence is not exactly what was said)", ls, said))
        if kind == "json":
            js_sentences.append(said)
    # the engine's usage-error words and the engine's session abbreviation were parsed by argparse, not by the capture's argv scan
    # only: the same refusal under the session recorded by its prefix is one line (above); here the second duplicate-payload run
    with root88() as b:
        run88(*em, "--input", _body88)
        code, out, err = run88(*em, "--input", _body88)
        ls = lines88(b)
    if not (code == 1 and "byte-identical" in err and len(ls) == 1 and ls[0]["sentence"] == dbcore._scrub(err.rstrip("\n").splitlines()[-1])):
        bad.append(("emit_data_migration.py: the same payload twice", code, err[:120], ls))
    with scratch() as c:      # full_text.py: a superseded source, and an --artefact it does not hold (HAND: the state no writer builds)
        ref = c.execute("SELECT ref_id FROM evidence_sources WHERE superseded_by_ref_id IS NULL ORDER BY ref_id LIMIT 1").fetchone()[0]
        with root88() as b:
            code, out, err = run88("scripts/research/full_text.py", "--ref-id", ref, "--session", S88, "--artefact", "no-such-file.pdf")
            ls = lines88(b)
        if not (code == 2 and err.startswith("REFUSING: --artefact 'no-such-file.pdf'") and len(ls) == 1 and ls[0]["sentence"] == dbcore._scrub(err[len("REFUSING: "):].rstrip("\n"))):
            bad.append(("full_text.py: an --artefact it does not hold", code, err[:160], ls))
        hand("UPDATE evidence_sources SET superseded_by_ref_id = ? WHERE ref_id = ?", far(ref), ref)
        with root88() as b:
            code, out, err = run88("scripts/research/full_text.py", "--ref-id", ref, "--session", S88)
            ls = lines88(b)
        if not (code == 2 and f"REFUSING: {ref} is superseded by" in err and len(ls) == 1 and ls[0]["sentence"] == dbcore._scrub(err[len("REFUSING: "):].rstrip("\n"))):
            bad.append(("full_text.py: a superseded source", code, err[:160], ls))
    # a CRASH (any other exception) is kept too, then raised unchanged: the traceback and the exit code are the evidence
    crashes = {"db.py: a writer verb crashes on its own input": (["scripts/db.py", *swap(asc, "--search-strategy", "{}")[1:], "--superseding-refs", "{bad"], "scripts/db.py", "add-supersession-check"),
               "engine: a database that cannot be opened": (eng + ["--db", f"{TMP}/no-such-dir/x.db", "--emit-sql", f"{TMP}/x.sql", "--parameter-id", "1", "--slug", "s",
                                                                  "--session", S88, "--stamp", "2026-01-01 00:00"], eng[0], "assess_cell"),
               "full_text.py: a database that cannot be opened": (["scripts/research/full_text.py", "--ref-id", "REF-00001", "--session", S88], "scripts/research/full_text.py", "full_text")}
    for label, (argv, script, verb) in crashes.items():
        with root88() as b:
            with mock.patch.dict(os.environ, {"GUIDEBOOK_DB_PATH": f"{TMP}/no-such-dir/x.db"} if label.startswith("full_text") else {}):
                code, out, err = run88(*argv)
            ls = lines88(b)
        if not (isinstance(code, Exception) and len(ls) == 1 and ls[0]["verb"] == verb and ls[0]["script"] == script
                and ls[0]["sentence"] == dbcore._scrub(f"{type(code).__name__}: {code}")):
            bad.append((label, "a crash is kept, then raised unchanged", type(code).__name__, ls))
    # the JSON sites are derived from the source: every `_json_refusal(` call has a case whose sentence matches its text
    _src = ast.parse((REPO / "scripts" / "db.py").read_text(encoding="utf-8"))
    _pat = []
    for _n in ast.walk(_src):
        if isinstance(_n, ast.Call) and getattr(_n.func, "id", "") == "_json_refusal" and _n.args:
            _a = _n.args[0]
            _parts = _a.values if isinstance(_a, ast.JoinedStr) else [_a]
            _pat.append("".join(re.escape(str(p.value)) if isinstance(p, ast.Constant) else ".*" for p in _parts))
    _uncovered = [p for p in _pat if not any(re.fullmatch(p, s or "") for s in js_sentences)]
    if len(_pat) != len(json_cases) or _uncovered:
        bad.append(("the derived JSON sites", len(_pat), len(json_cases), _uncovered))
    record("T088-08", "each place a writer says no that a fixture can reach (db.py's Refusal, its 11 JSON errors derived from the source, its usage errors; the engine's three and its usage error; "
           "full_text.py's three and its usage error; emit_data_migration.py's four) exits as before, in the same words, and keeps exactly one line whose sentence is what the process said",
           not bad, bad)

    # --- T088-09: the capture set is DERIVED from the syntax, not listed: in every writer script (one that adds `--session`, outside tests,
    # migrations and audit) each place that says no -- `sys.exit(<message or non-zero>)`, `raise SystemExit(...)`, a print/write of a REFUSING or
    # ERROR sentence, a printed `{"error": ...}`, a `return <non-zero>`, a plain ArgumentParser -- must be preceded, in its own block or one that
    # encloses it within its function, by a call to something that calls `record_refusal`. What it cannot see: a refusal returned as a value to
    # a caller that exits, a message with another prefix, an exit through `os._exit`, a script with no `--session` (the capture needs the
    # session), a subprocess writer, and whether the recorded sentence is the one printed (T088-08 runs that).
    def _head88(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.JoinedStr) and node.values and isinstance(node.values[0], ast.Constant):
            return str(node.values[0].value)
        return ""

    def _calls88(node):
        return [n for n in ast.walk(node) if isinstance(n, ast.Call)]

    def _cname88(call):
        return call.func.attr if isinstance(call.func, ast.Attribute) else getattr(call.func, "id", "")

    def cands88(tree):
        out = []
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                nm = _cname88(n)
                if nm in ("exit", "SystemExit") and n.args and not isinstance(n.args[0], ast.Call) and not (isinstance(n.args[0], ast.Constant) and n.args[0].value in (0, None)):
                    out.append((n, "exits with a message or a non-zero code"))
                elif nm in ("print", "write") and n.args and _head88(n.args[0]).strip().startswith(("REFUSING", "ERROR")):
                    out.append((n, "prints a REFUSING or ERROR sentence"))
                elif nm == "print" and n.args and any(isinstance(d, ast.Dict) and any(isinstance(k, ast.Constant) and k.value == "error" for k in d.keys) for d in ast.walk(n.args[0])):
                    out.append((n, "prints a JSON error"))
                elif nm == "ArgumentParser":
                    out.append((n, "a plain ArgumentParser: its usage errors are not kept"))
            elif isinstance(n, ast.Raise) and n.exc is None:
                out.append((n, "re-raises a caught exception"))
            elif isinstance(n, ast.Return) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, int) and not isinstance(n.value.value, bool) and n.value.value:
                out.append((n, "returns a non-zero exit code"))
        return out

    def unrouted88(src):
        tree = ast.parse(src)
        par = {c: n for n in ast.walk(tree) for c in ast.iter_child_nodes(n)}
        rec = {"record_refusal"} | {f.name for f in ast.walk(tree) if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))
                                    and any(_cname88(c) == "record_refusal" for c in _calls88(f))}

        def routed(node):
            cur = node
            while cur in par:
                up = par[cur]
                for field in ("body", "orelse", "finalbody", "handlers"):
                    block = getattr(up, field, None)
                    # a STATEMENT of the block, before this one, that is itself the call: a recorder call buried in an earlier `if`, or in
                    # a function defined above, keeps nothing for this place
                    if isinstance(block, list) and cur in block and any(isinstance(s, ast.Expr) and isinstance(s.value, ast.Call) and _cname88(s.value) in rec
                                                                       for s in block[:block.index(cur)]):
                        return True
                if isinstance(up, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    return False
                cur = up
            return False

        def fn(node):
            while node in par:
                node = par[node]
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    return node.name
            return "<module>"
        return [(fn(c), ast.unparse(c), why) for c, why in cands88(tree) if why.startswith("a plain") or not routed(c)]

    def writers88():
        for f in sorted((REPO / "scripts").rglob("*.py")):
            if f.relative_to(REPO / "scripts").parts[0] in ("tests", "migrations", "audit") or f.name == "dbcore.py":
                continue
            src = f.read_text(encoding="utf-8")
            if any(isinstance(c, ast.Call) and _cname88(c) == "add_argument" and c.args and isinstance(c.args[0], ast.Constant) and c.args[0].value == "--session"
                   for c in ast.walk(ast.parse(src))):
                yield str(f.relative_to(REPO)), src

    # places that say no and are not routed, with how many there are, who judged them not a writer's refusal, and the phrase the docs name them by
    # (a count that moves, or a place that is gone, fails: this list cannot go stale)
    EXEMPT88 = {("scripts/db.py", "main", "sys.exit(1)"): (1, "no subcommand given: prints the usage and exits 1", None),
                ("scripts/emit_data_migration.py", "selftest", "return 1"): (1, "the selftest's own verdict", None),
                ("scripts/research/full_text.py", "main", "return 1"): (1, "exit 1 is `NOTHING TO DERIVE`: a state of the reader, not a refusal to write", "NOTHING TO DERIVE"),
                ("scripts/research/full_text.py", "main", "return 2"): (2, "`AMBIGUOUS` (several derivable files: a choice for the operator) and the missing PDF reader (the environment)", "several-derivable-files")}
    # whole scripts whose errors are not routed: infrastructure or reader errors, named in /batch-done and the skill
    NOT_ROUTED88 = {"scripts/migrate_db.py": "applies migrations: its errors are the runner's, and a failed one is rolled back",
                    "scripts/research/page_image.py": "renders a page to an image: a reader",
                    "scripts/research/retrieval_log.py": "the retrieval ledger: errors are returned codes of fetch/verify helpers"}
    found88, seen88 = {}, collections.Counter()
    for rel, src in writers88():
        left = []
        for item in unrouted88(src):
            if (rel, item[0], item[1]) in EXEMPT88:
                seen88[(rel, item[0], item[1])] += 1
            else:
                left.append(item)
        if left:
            found88[rel] = left
    used88 = {k for k, v in EXEMPT88.items() if seen88[k] == v[0]}
    seeded = unrouted88("import sys\ndef main():\n    sys.exit('REFUSING: x')\n") + unrouted88("def f():\n    print(json.dumps({'error': 'x'}))\n    return 1\n") + \
        unrouted88("import argparse\nap = argparse.ArgumentParser()\n") + unrouted88("def main():\n    print('ERROR: x', file=sys.stderr)\n    return 2\n") + \
        unrouted88("try:\n    main()\nexcept Exception as exc:\n    raise\n")
    clean = unrouted88("def _rec(s):\n    dbcore.record_refusal('x', [], s)\n\ndef main():\n    _rec('x')\n    sys.exit('REFUSING: x')\n")
    record("T088-09", "every place a writer script says no is preceded by a call that keeps it (derived from the syntax: sys.exit with a message or code, a REFUSING/ERROR print, "
           "a JSON error print, a non-zero return, a plain ArgumentParser); the scripts left out are exactly the named ones, and the exemptions are all still real",
           set(found88) == set(NOT_ROUTED88) and used88 == set(EXEMPT88) and len(seeded) == 7 and not clean,
           ({k: v[:2] for k, v in found88.items() if k not in NOT_ROUTED88}, set(NOT_ROUTED88) - set(found88), set(EXEMPT88) - used88, seeded, clean))

# T088-10..: the disposition.
if feature("T088-10", "the reader exists", REG88 is not None, f"scripts/audit/refusal_register.py ({REG88_ERR})") and HAS88:
    with root88() as b:
        empty = reg88("list", "--session", S88)
        file88(b).write_text("", encoding="utf-8")
        empty_file = reg88("list", "--session", S88)
        file88(b).write_text("\n  \n", encoding="utf-8")
        blank_file = reg88("list", "--session", S88)
        file88(b).write_text("{this is not json\n", encoding="utf-8")
        only_bad = reg88("list", "--session", S88)
    record("T088-10", "a folder with no refusals.jsonl, an empty one or a blank one is a batch that met none: `list` says so, prints EXAMINED: 0 and exits 0; a file holding "
           "only an unreadable line is not that: it exits 1 and says PROBLEM",
           all(x[0] == 0 and "no refusal captured" in x[1] and "EXAMINED: 0 refusal(s)" in x[1] for x in (empty, empty_file, blank_file))
           and only_bad[0] == 1 and "PROBLEM" in only_bad[1] and "EXAMINED: 0 refusal(s)" in only_bad[1], (empty, empty_file, blank_file, only_bad))

    notrun = {}
    for label, (cur, folder, arg) in {"CURRENT names a folder that does not exist": (S88 + "-typo", S88, None),
                                      "CURRENT holds a branch slug": ("my-branch-slug", "my-branch-slug", None),
                                      "CURRENT is empty": ("", S88, None),
                                      "CURRENT is missing": (None, S88, None),
                                      "--session ..": (S88, S88, ".."),
                                      "--session .": (S88, S88, "."),
                                      "--session a path": (S88, S88, f"../{S88}"),
                                      "--session a typo": (S88, S88, S88 + "x")}.items():
        with root88(cur, folder) as b:
            notrun[label] = reg88("list", *(["--session", arg] if arg else []))
            d = reg88("dispose", "--session", arg or (cur or "x"), "--id", "x", "--as", "retried")
            notrun[label] = (*notrun[label], d[0])
    record("T088-10b", "`list` is NOT RUN (exit 2, no EXAMINED line, nothing read) when the session is not a session_YYYY-MM-DD-... stem with an existing folder "
           "(missing folder, branch slug, empty or missing CURRENT, `..`, `.`, a path, a typo); `dispose` refuses the same",
           all(v[0] == 2 and v[1].startswith("NOT RUN:") and "EXAMINED" not in v[1].replace("NOT EXAMINED", "") and v[3] == 1 for v in notrun.values()), notrun)

    with scratch() as c:
        gap_open = json.loads(cli("add-gap", "--category", "SW", "--priority", "P3", "--description", "TASK-FIXTURE T088 open gap", "--session", S).stdout)["gap_id"]
        gap_shut = json.loads(cli("add-gap", "--category", "SW", "--priority", "P3", "--description", "TASK-FIXTURE T088 closed gap", "--session", S).stdout)["gap_id"]
        hand("UPDATE gaps SET status='CLOSED' WHERE gap_id=?", gap_shut)
        gap_none = far(gap_open)
        absent = c.execute("SELECT COUNT(*) FROM gaps WHERE gap_id=?", (gap_none,)).fetchone()[0] == 0
        with root88() as b:
            for k in range(5):
                refuse88(_ARGV88 + [str(k)], f"refusal number {k}; Nothing was written.")
            ids = [rid88(x) for x in lines88(b)]
            first = reg88("list", "--session", S88)
            size0 = file88(b).stat().st_size
            fails = {}
            for label, (said, argv) in {
                    "an unknown id": ("no refusal of", ["--id", "0" * 32, "--as", "retried"]),
                    "parked without a gap": ("parked needs --gap-id", ["--id", ids[0], "--as", "parked"]),
                    "parked on an absent gap": ("not in the gaps table", ["--id", ids[0], "--as", "parked", "--gap-id", gap_none]),
                    "parked on a closed gap": ("not open", ["--id", ids[0], "--as", "parked", "--gap-id", gap_shut]),
                    "waived without a reason": ("waived needs --reason", ["--id", ids[0], "--as", "waived"]),
                    "waived with a blank reason": ("waived needs --reason", ["--id", ids[0], "--as", "waived", "--reason", "   "]),
                    "waived with a reason that is a dot": ("waived needs --reason", ["--id", ids[0], "--as", "waived", "--reason", "."]),
                    "waived with a nine-character reason": ("waived needs --reason", ["--id", ids[0], "--as", "waived", "--reason", "not a gap"]),
                    "waived with a reason of no letter or digit": ("waived needs --reason", ["--id", ids[0], "--as", "waived", "--reason", "!!!!!!!!!!!!"]),
                    "retried with a gap": ("belongs to parked", ["--id", ids[0], "--as", "retried", "--gap-id", gap_open]),
                    "an unknown disposition": ("invalid choice", ["--id", ids[0], "--as", "ignored"])}.items():
                rc, _, err = reg88("dispose", "--session", S88, *argv)
                fails[label] = (rc != 0 and said in err, file88(b).stat().st_size == size0)
            ok_a = reg88("dispose", "--session", S88, "--id", ids[0], "--as", "retried")
            second = reg88("dispose", "--session", S88, "--id", ids[0], "--as", "waived", "--reason", "again, for good reason")
            mid = reg88("list", "--session", S88)
            ok_b = reg88("dispose", "--session", S88, "--id", ids[1], "--as", "parked", "--gap-id", gap_open)
            ok_c = reg88("dispose", "--session", S88, "--id", ids[2], "--as", "waived", "--reason", "TASK-FIXTURE: not content")
            ok_d = reg88("dispose", "--session", S88, "--id", ids[3], "--as", "retried", "--reason", "the corrected call wrote it")
            one_left = reg88("list", "--session", S88)
            ok_e = reg88("dispose", "--session", S88, "--id", ids[4], "--as", "retried")
            done = reg88("list", "--session", S88)
    record("T088-11", "`list` shows five UNDISPOSED, prints each refusal's id, and exits 1; EXAMINED counts the refusals",
           first[0] == 1 and first[1].count("UNDISPOSED") >= 5 and "UNDISPOSED: 5" in first[1] and "EXAMINED: 5 refusal(s)" in first[1]
           and all(t in first[1] for t in ids), first)
    record("T088-12", "dispose refuses an unknown id, a parked with no gap / an absent gap / a closed gap, a waived with no, a blank, a one-character, a nine-character or a "
           "symbols-only reason, a gap given to retried, and an unknown disposition, each saying which rule it is and leaving the file as it was",
           absent and all(v == (True, True) for v in fails.values()), (absent, fails))
    record("T088-13", "a retried, a parked (real open gap), a waived (with a reason) are written; a second disposition of the same refusal is refused",
           ok_a[0] == 0 and ok_b[0] == 0 and ok_c[0] == 0 and ok_d[0] == 0 and ok_e[0] == 0 and second[0] == 1 and "already disposed" in second[2], (ok_a, ok_b, ok_c, second))
    record("T088-14", "after one disposition `list` still exits 1 and counts the other four; with the fourth still open it names exactly one; with all five it exits 0 "
           "and EXAMINED still counts five (a disposition is not a refusal)",
           mid[0] == 1 and "UNDISPOSED: 4" in mid[1] and "EXAMINED: 5 refusal(s)" in mid[1]
           and one_left[0] == 1 and "UNDISPOSED: 1" in one_left[1]
           and done[0] == 0 and "UNDISPOSED: 0" in done[1] and "EXAMINED: 5 refusal(s)" in done[1] and f"parked {gap_open}" in done[1], (mid, one_left, done))

    # a record that cannot be read is reported, never skipped
    with root88() as b:
        refuse88(_ARGV88)
        rid = rid88(lines88(b)[0])
        with open(file88(b), "a", encoding="utf-8") as fh:
            fh.write("{this is not json\n")
            fh.write(json.dumps({"kind": "disposition", "refusal_id": "1999-01-01 00:00:00.000000", "as": "retried", "ts": "x"}) + "\n")
            fh.write(json.dumps({"kind": "mystery"}) + "\n")
            fh.write(json.dumps({"kind": "disposition", "refusal_id": rid, "as": "shrugged", "ts": "x"}) + "\n")
        bad_ = reg88("list", "--session", S88)
        reg88("dispose", "--session", S88, "--id", rid, "--as", "retried")
        reg88("dispose", "--session", S88, "--id", rid, "--as", "retried")        # refused: already disposed
        twice = reg88("list", "--session", S88)
        with open(file88(b), "a", encoding="utf-8") as fh:                       # a hand-edited second disposition
            fh.write(json.dumps({"kind": "disposition", "refusal_id": rid, "as": "waived", "reason": "a reason of length", "ts": "x"}) + "\n")
        dup = reg88("list", "--session", S88)
    record("T088-15", "`list` reports a line that is not JSON, an unknown kind, an unknown disposition and a disposition no refusal carries, and exits 1 even when every refusal is disposed",
           bad_[0] == 1 and bad_[1].count("PROBLEM") == 4 and "UNDISPOSED: 1" in bad_[1] and twice[0] == 1 and twice[1].count("PROBLEM") == 4 and "UNDISPOSED: 0" in twice[1]
           and dup[0] == 1 and "disposed a second time" in dup[1], (bad_, twice, dup))

    # a refusal id two lines carry cannot name one; a line written before refusal_id existed is still named by its ts
    with root88() as b:
        refuse88(_ARGV88)
        ln = lines88(b)[0]
        with open(file88(b), "a", encoding="utf-8") as fh:
            fh.write(json.dumps(ln) + "\n")                    # a hand-copied line: two refusals, one id
        size = file88(b).stat().st_size
        twin = reg88("dispose", "--session", S88, "--id", rid88(ln), "--as", "retried")
        grew = file88(b).stat().st_size != size
        listed = reg88("list", "--session", S88)
        with open(file88(b), "a", encoding="utf-8") as fh:        # ...and a disposition written for it by hand covers neither
            fh.write(json.dumps({"kind": "disposition", "refusal_id": rid88(ln), "as": "retried", "ts": "x"}) + "\n")
        covered = reg88("list", "--session", S88)
    record("T088-18", "an id that two refusal lines carry cannot name one: dispose refuses and writes nothing, `list` flags it and counts both undisposed, and a hand-written "
           "disposition for it covers neither (no refusal is merged away)",
           twin[0] == 1 and "carried by 2" in twin[2] and not grew and "EXAMINED: 2 refusal(s)" in listed[1] and "UNDISPOSED: 2" in listed[1] and "carried by 2" in listed[1]
           and "UNDISPOSED: 2" in covered[1] and covered[0] == 1, (twin, listed, covered))
    with root88() as b:
        old = {k: v for k, v in {"ts": "2026-11-16 10:00:00.000001", "session": S88, "script": "scripts/db.py", "verb": "add-gap", "argv": [], "sentence": "old line", "db": "data/guidebook.db"}.items()}
        file88(b).write_text(json.dumps(old) + "\n", encoding="utf-8")
        o_list = reg88("list", "--session", S88)
        o_disp = reg88("dispose", "--session", S88, "--id", old["ts"], "--as", "retried")
        o_done = reg88("list", "--session", S88)
    record("T088-18b", "a refusal line written before refusal_id existed is named by its ts, listed and disposed as before",
           o_list[0] == 1 and o_disp[0] == 0 and o_done[0] == 0 and "UNDISPOSED: 0" in o_done[1], (o_list, o_disp, o_done))

    # a foreign line, a byte-order mark and CRLF line ends
    with root88() as b:
        mine = {"refusal_id": "a" * 32, "ts": "2026-11-16 10:00:00.000001", "session": S88, "script": "scripts/db.py", "verb": "add-gap", "argv": [], "sentence": "mine", "db": "x"}
        theirs = {**mine, "refusal_id": "b" * 32, "session": "session_2026-01-01-someone-else", "sentence": "theirs"}
        file88(b).write_bytes(b"\xef\xbb\xbf" + (json.dumps(mine) + "\r\n" + json.dumps(theirs) + "\r\n").encode("utf-8"))
        bom = reg88("list", "--session", S88)
    record("T088-20", "a file that starts with a byte-order mark and uses CRLF is read (its first line is not reported unreadable) and a line whose session is not the folder's is flagged foreign",
           "unreadable" not in bom[1] and "EXAMINED: 2 refusal(s)" in bom[1] and bom[1].count("foreign line") == 1 and "session_2026-01-01-someone-else" in bom[1] and bom[0] == 1, bom)

    # a disposition is checked again when it is read
    with scratch() as c:
        g_ok = json.loads(cli("add-gap", "--category", "SW", "--priority", "P3", "--description", "TASK-FIXTURE T088 recheck", "--session", S).stdout)["gap_id"]
        with root88() as b:
            for k in range(6):
                refuse88(_ARGV88 + [str(k)], f"recheck {k}; Nothing was written.")
            ids = [rid88(x) for x in lines88(b)]
            ok_p = reg88("dispose", "--session", S88, "--id", ids[0], "--as", "parked", "--gap-id", g_ok)
            before = reg88("list", "--session", S88)
            hand("UPDATE gaps SET status='CLOSED-FIXED' WHERE gap_id=?", g_ok)           # the gap is closed after the refusal was parked
            closed = reg88("list", "--session", S88)
            hand("DELETE FROM gaps WHERE gap_id=?", g_ok)
            gone = reg88("list", "--session", S88)
            with open(file88(b), "a", encoding="utf-8") as fh:                           # hand-written dispositions that dispose would have refused
                for rid, how, gap, why in ((ids[1], "parked", None, None), (ids[2], "parked", "GAP-NOPE-1", None), (ids[3], "waived", None, "."),
                                           (ids[4], "retried", "GAP-1", None), (ids[5], "waived", None, None)):
                    fh.write(json.dumps({"kind": "disposition", "refusal_id": rid, "as": how, "gap_id": gap, "reason": why, "ts": "x"}) + "\n")
            hand_ = reg88("list", "--session", S88)
    record("T088-21", "`list` checks every disposition again: a parked gap closed or deleted afterwards, a hand-written parked with no gap or an absent gap, a waived with a dot or no reason "
           "and a retried with a gap each make the refusal UNDISPOSED again, with the reason printed, and exit 1",
           ok_p[0] == 0 and "parked " + g_ok in before[1] and "UNDISPOSED: 5" in before[1]
           and closed[0] == 1 and "no longer holds" in closed[1] and "not open" in closed[1] and "UNDISPOSED: 6" in closed[1]
           and gone[0] == 1 and "not in the gaps table" in gone[1] and "UNDISPOSED: 6" in gone[1]
           and hand_[0] == 1 and hand_[1].count("no longer holds") >= 6 and "UNDISPOSED: 6" in hand_[1], (before, closed, gone, hand_))

    # the database a gap is checked against is the one the refusal names (a repository-relative path), else the one this process opens
    with scratch() as c:
        mine = json.loads(cli("add-gap", "--category", "SW", "--priority", "P3", "--description", "TASK-FIXTURE T088 named db", "--session", S).stdout)["gap_id"]
        with root88() as b:
            refuse88(_ARGV88)
            ln = lines88(b)[0]
            rid = rid88(ln)
            shutil.copy(os.environ["GUIDEBOOK_DB_PATH"], b / "named-elsewhere.db")
            _c = sqlite3.connect(b / "named-elsewhere.db")
            _c.execute("DELETE FROM gaps WHERE gap_id=?", (mine,))
            _c.commit()
            _c.close()
            file88(b).write_text(json.dumps({**ln, "db": "named-elsewhere.db"}) + "\n", encoding="utf-8")
            refused = reg88("dispose", "--session", S88, "--id", rid, "--as", "parked", "--gap-id", mine)
            file88(b).write_text(json.dumps({**ln, "db": "<outside-repo>/gone.db"}) + "\n", encoding="utf-8")
            fallback = reg88("dispose", "--session", S88, "--id", rid, "--as", "parked", "--gap-id", mine)
    record("T088-16", "a gap is looked up in the database the refusal names (absent there: refused), and when that file is outside the repository or gone, in the one this process opens",
           refused[0] == 1 and "not in the gaps table" in refused[2] and fallback[0] == 0, (refused, fallback))

# T088-17: the Layer 0 rule and the Layer 2 protocol say what the code does.
_bd = re.sub(r"\s+", " ", (REPO / ".claude" / "commands" / "batch-done.md").read_text(encoding="utf-8"))
_sk = re.sub(r"\s+", " ", (REPO / "skills" / "run-pipeline_SKILL.md").read_text(encoding="utf-8"))
_line = 'python3 scripts/audit/refusal_register.py list --session "$(cat scratchpad/CURRENT)"'
try:
    _named, _exempt = set(NOT_ROUTED88), EXEMPT88
    _nosession = [rel for rel in ("scripts/research/emit_batch_sql.py",) if rel not in dict(writers88())]
except NameError:
    _named, _nosession = set(), []
_names_ok = bool(_named) and bool(_nosession) and all(pathlib.Path(n).name in _bd and pathlib.Path(n).name in _sk for n in _named | set(_nosession)) \
    and all(v[2] in _bd and v[2] in _sk for v in EXEMPT88.values() if v[2])
record("T088-17", "/batch-done runs `refusal_register.py list` on CURRENT, says it exits 2 / NOT RUN when CURRENT's folder is missing, says an undisposed refusal is a batch not done, "
       "and names the scripts that keep nothing (derived: the ones the T088-09 sweep leaves out, and a script with no --session); the skill's resume section says what to do when a writer refuses",
       _line in _bd and "An undisposed refusal is a batch that is not done" in _bd and "NOT RUN" in _bd and "exits 2" in _bd and "--id K" in _bd
       and "When a writer refuses" in _sk and "refusal_register.py list" in _sk and "NOT RUN" in _sk and "worktree" in _sk and "usage error" in _sk and _names_ok
       and all(w in _sk and w in _bd for w in ("retried", "parked", "waived")), (_line in _bd, "When a writer refuses" in _sk, _names_ok))
# T088-END


finish()
