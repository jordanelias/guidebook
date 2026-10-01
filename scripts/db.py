"""
scripts/db.py — SQLite interface for guidebook data layer.

Environment:
    GUIDEBOOK_DB_PATH   Path to database file (default: data/guidebook.db)

CLI usage:
    python3 scripts/db.py init
    python3 scripts/db.py migrate
    python3 scripts/db.py gaps [--priority P1] [--status OPEN]
    python3 scripts/db.py connections [--status PENDING] [--confidence HIGH] [--summary]
    python3 scripts/db.py is-mined --slug SLUG --ref REF-ID
    python3 scripts/db.py log-mining --slug S --ref R --direction backward
                          --notes "found N items, staged on exec X" --session SESSION
                          [--dry-run]
    python3 scripts/db.py next-id connections|gaps|terms|conflicts|ref
    python3 scripts/db.py coverage --slug SLUG
    python3 scripts/db.py synonyms --item A-16 [--language JA]
    python3 scripts/db.py add-gap --category RES --priority P2 --description "..." --session SESSION
    python3 scripts/db.py close-gap --gap-id GAP-001 --status CLOSED-FIXED --session SESSION
    python3 scripts/db.py add-connection --con-id CON-0001 --confidence HIGH --connection-type CROSS-POPULATION --filed-in sensory-environment --description "..." --source-skill connection-scout --targets '["item:A-02"]' --session SESSION
    python3 scripts/db.py update-connection --con-id CON-0001 --status CONSUMED --session SESSION
    python3 scripts/db.py unmined [--slug SLUG] [--tier-max 3]
    python3 scripts/db.py log-search --slug SLUG --language EN --query-text '...' --engine pubmed \
        --depth-method scoping --session SESSION      (upsert-coverage/-language are frozen; see log_search)
    python3 scripts/db.py update-bpc --slug SLUG --citation-mining-complete 1 --session SESSION
    python3 scripts/db.py add-source --ref-id REF-00971 --author "Smith|Jane" --author "corp|WHO" --year 2022 --title "..." --tier 1 --session SESSION [--slug SLUG [--local-ref-id RAP-07]]
        (--ref-id is the GLOBAL REF-NNNNN; --local-ref-id is the per-slug label. Different values.)
        (--authors "Smith J; Jones K" still works and is parsed into author rows; --author is preferred because it keeps the given name)
    python3 scripts/db.py validate
    python3 scripts/db.py record-adversarial-pass --subject-session S --subject-commit SHA \
        --reviewer-transcript transcripts/.../reviewer.jsonl --author-transcript transcripts/.../author.jsonl \
        --session SESSION      (RC4; then dispose-adversarial-finding and close-adversarial-pass)
    python3 scripts/db.py --help
"""

import json
import os
import re
import subprocess
import zipfile
import sqlite3
import sys
import argparse
from contextlib import contextmanager, nullcontext
from datetime import datetime, timezone
from pathlib import Path

# MOVED TO scripts/dbcore.py 2026-08-25. This module now IMPORTS the connection,
# path, audit-stamp and reference-id mechanics it used to own privately -- it was the
# only correct implementation in the repository and it had zero importers, so 55 other
# files re-implemented it 104 times and inherited none of its lessons.
sys.path.insert(0, str(Path(__file__).resolve().parent))
# The REPO ROOT too, so `schemas.*` resolves. add-source derives the ratified tier from
# schemas/tier_derivation.py rather than re-stating the ladder here — a second copy of a
# ratified rule is the dual home rule 5 forbids, and this CLI's whole value is that it
# refuses from the one authority rather than from a list of its own.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import dbcore                                                      # noqa: E402
# The ONE dbcore name imported bare rather than reached through the module: it is raised,
# not called, and a module path in front of it at 114 sites crowds the line whose whole job
# is to carry a sentence. See dbcore.Refusal for why these are a subclass rather than plain
# ValueError -- in short, so that a defect keeps the traceback a refusal does not need.
from dbcore import Refusal                                         # noqa: E402


def _ladder_evidence_types():
    """The evidence-type vocabulary, from the ratified ladder (CLAUDE.md rule 8).

    `schemas/tier_derivation.TIER_MAP`'s keys are the authority `add-source` already
    validates against. Used for argparse `choices=` where the column being written
    declares no CHECK of its own, so `dbcore.schema_choices()` has nothing to read.

    Returns None rather than raising if schemas is not importable: a parser that cannot
    be built is worse than one without a choices constraint, and the writer refuses the
    same values at run time either way.
    """
    try:
        from schemas.tier_derivation import TIER_MAP                 # noqa: E402
        return sorted({et for et, _ in TIER_MAP})
    except Exception:
        return None

# DB_PATH stays a module attribute because callers and tests read it. It is resolved
# through dbcore so there is one resolution, not two.
DB_PATH = dbcore.db_path()

# Column whitelists — validated before any f-string SQL construction
_COVERAGE_COLS = frozenset({
    "status", "co1_attempted", "tier5_attempted", "tier6_attempted", "notes"
})
_LANGUAGE_COLS = frozenset({"status", "results_count", "notes"})
_BPC_META_COLS = frozenset({
    "population", "last_updated", "jurisdictions_searched", "co1_pass_count",
    "evidence_state", "pico_complete", "search_complete", "bpc_complete",
    "citation_mining_complete",
    # DR-2026-05-24: best-practice supersession protocol (migration 015)
    "supersession_check_complete", "closure_definition_version",
})


# connect(), now(), audit(), _upd() and _validate_cols() MOVED to scripts/dbcore.py.
# They are re-exported here under their original names so that every existing caller
# and every skill that documents them keeps working unchanged (CLAUDE.md rule 4: a
# rename is not done until the callers are swept -- so this is not a rename).
connect = dbcore.connect
now = dbcore.now
audit = dbcore.audit
_upd = dbcore.upd
_validate_cols = dbcore.validate_cols


def _txn(conn, dry_run: bool = False):
    """`conn` itself when the caller already holds a write transaction, else a new one.

    Lets two writers share ONE transaction, so a refusal in the second rolls back the
    first. `add-source --slug` is the case: the source and its slug link are one
    admission. As two connect() blocks, a failure in the second left the first
    committed (GAP-058), and under --dry-run the link's foreign key could not see the
    rolled-back source, so the dry run crashed with a traceback instead of reporting.
    """
    return nullcontext(conn) if conn is not None else connect(dry_run)










def _emit(data):
    """Print JSON to stdout."""
    print(json.dumps(data, indent=2, default=str))


# --- Storage layer (CRUD) ---


def next_ref() -> str:
    """The next global REF-NNNNN. Thin CLI wrapper — `dbcore.next_ref_id(conn)` is the rule
    (CLAUDE.md §4: the high-water mark is the UNION of every table holding a ref_id); this
    does not reimplement it. `add-source`'s refusal on a bad ref_id named that function
    directly, sending an operator to a Python call instead of a command
    (workplan/2026-09-10-road-to-batch-06.md B2)."""
    with connect(readonly=True) as conn:
        return dbcore.next_ref_id(conn)


def next_con_id() -> str:
    with connect(readonly=True) as conn:
        row = conn.execute(
            "SELECT con_id FROM connections ORDER BY con_id DESC LIMIT 1"
        ).fetchone()
    if not row:
        return "CON-0001"
    return f"CON-{int(row['con_id'].split('-')[1]) + 1:04d}"


def insert_connection(data: dict, targets: list[str],
                      session: str, dry_run: bool = False) -> str:
    row = {**data, **audit(session)}
    with connect(dry_run) as conn:
        cols = ", ".join(row)
        ph = ", ".join(["?"] * len(row))
        conn.execute(
            f"INSERT INTO connections ({cols}) VALUES ({ph})",
            list(row.values())
        )
        conn.executemany(
            "INSERT OR IGNORE INTO connection_targets "
            "(con_id, target) VALUES (?,?)",
            [(data["con_id"], t) for t in targets]
        )
    return data["con_id"]


def update_connection_status(con_id: str, status: str,
                             session: str, dry_run: bool = False):
    u = _upd(session)
    with connect(dry_run) as conn:
        conn.execute(
            "UPDATE connections SET status=?, created_by_session=?, "
            "updated_at=?, updated_by_session=? WHERE con_id=?",
            [status, session, u["updated_at"], u["updated_by_session"], con_id]
        )


def next_gap_id() -> str:
    with connect(readonly=True) as conn:
        row = conn.execute(
            "SELECT gap_id FROM gaps "
            "WHERE gap_id GLOB 'GAP-[0-9]*' "
            "ORDER BY CAST(SUBSTR(gap_id,5) AS INTEGER) DESC LIMIT 1"
        ).fetchone()
    if not row:
        return "GAP-001"
    return f"GAP-{int(row['gap_id'].split('-')[1]) + 1:03d}"


def insert_gap(data: dict, session: str, dry_run: bool = False) -> str:
    row = {**data, **audit(session)}
    with connect(dry_run) as conn:
        cols = ", ".join(row)
        ph = ", ".join(["?"] * len(row))
        conn.execute(
            f"INSERT INTO gaps ({cols}) VALUES ({ph})",
            list(row.values())
        )
    return data["gap_id"]


def close_gap(gap_id: str, status: str,
              session: str, dry_run: bool = False):
    if not status.startswith("CLOSED"):
        raise Refusal(f"status must start with CLOSED, got '{status}'")
    u = _upd(session)
    with connect(dry_run) as conn:
        conn.execute(
            "UPDATE gaps SET status=?, updated_at=?, updated_by_session=? "
            "WHERE gap_id=?",
            [status, u["updated_at"], u["updated_by_session"], gap_id]
        )


def update_gap_priority(gap_id: str, priority: str,
                        session: str, dry_run: bool = False):
    if priority not in ("P1", "P2", "P3"):
        raise Refusal(f"Invalid priority: {priority}")
    u = _upd(session)
    with connect(dry_run) as conn:
        conn.execute(
            "UPDATE gaps SET priority=?, updated_at=?, updated_by_session=? "
            "WHERE gap_id=?",
            [priority, u["updated_at"], u["updated_by_session"], gap_id]
        )


_VALID_DIRECTIONS = frozenset({"backward", "forward"})


def is_mined(slug: str, ref_id: str) -> dict | None:
    # Keyed on the REFERENCE ID. Callers pass a global ref_id; this matched it
    # against local_ref_id, the per-slug label, which only worked while the two
    # happened to agree. They stopped agreeing on 2026-08-23.
    # THE DIRECTION FLAGS DO NOT MEAN THE PASS RAN, so this verb could not answer the
    # question its only caller asks. Owner ruling 2026-09-18: "executed is 'mined'" --
    # the execution signal is evidence_sources.citation_mining_status, and log_mining
    # sets backward/forward to 1 on a DEFERRED pass as readily as an executed one.
    # citation-miner SKILL.md step 3 reads this verb and says "If already mined (both
    # B+F) -> skip", so on REF-01002 -- backward=1, status='deferred', the anchor named
    # as the next pass's highest-value target -- the next session would have skipped it.
    # `status` and `deferred_reason` are returned so a caller can read the fact the
    # ruling makes authoritative; they are POINTED AT, not copied (rule 5).
    with connect(readonly=True) as conn:
        # connections_produced is NOT selected -- retired 2026-09-28 (DR-2026-09-26
        # phase 2b), and a helper has no obligation to keep surfacing a column the
        # schema still carries for history alone (rule 3 governs the column, not this
        # function's return shape). Dropped here rather than returned-and-disclaimed.
        row = conn.execute(
            "SELECT cm.backward, cm.forward, "
            "       cm.deferred_reason, cm.notes, "
            "       es.citation_mining_status AS status, "
            "       (es.ref_id IS NOT NULL) AS resolves "
            "FROM citation_mining cm "
            "LEFT JOIN evidence_sources es ON es.ref_id = cm.global_ref_id "
            "WHERE cm.slug=? AND cm.global_ref_id=?",
            [slug, ref_id]
        ).fetchone()
    if not row:
        return None
    out = dict(row)
    out["executed"] = mining_executed(out["status"], row["resolves"])
    return out


def mining_executed(status, resolves_in_evidence_sources) -> bool | None:
    """Did the mining pass RUN? True / False / None, and None is not False.

    ONE derivation of "executed", called by `is_mined` and by `log_mining`'s
    regression guard, because answering it twice in one module from two different
    columns is rule 5 at code level -- and the second answer was wrong both ways.

    `None` MEANS THE QUESTION DOES NOT APPLY, and collapsing it to False is the
    defect this exists to prevent. A `citation_mining` row's `global_ref_id` may name
    a `source_locators` LEAD rather than an admitted source: migration 067 dropped
    that FK deliberately -- "a ref_id is an identity that SPANS two tables" -- so the
    ref resolves nowhere in `evidence_sources` and carries no status at all. Measured
    2026-09-18: 10 of 23 live rows, every one of them fully mined with a real DOI
    list. Reporting those as not-executed tells the next session to re-mine finished
    work, which is verbatim the RAP-F61/F69/F70 failure the citation-miner skill
    already records.
    """
    if not resolves_in_evidence_sources:
        return None
    return status == "mined"


def log_mining(slug: str, ref_id: str, direction: str,
               session: str,
               dry_run: bool = False, deferred_reason: str = None,
               status: str = None, notes: str = None,
               discharge_deferral: bool = False):
    """Record a mining pass. Keyed on the global ref_id.

    The `doi` parameter was REMOVED 2026-08-24. It wrote a copy of a value that
    is reachable through global_ref_id, and 2 of 10 rows had already drifted by
    case. Accepting it while ignoring it would have been worse than either
    keeping or dropping it: a caller would believe a DOI had been recorded.

    `connections` was REMOVED 2026-09-28 for the identical reason, the moment
    `connections_produced` stopped being written (DR-2026-09-26 phase 2b, RC5's
    event home: `search_executions.mined_ref_id` together with
    `search_candidates.exec_id` now records what a mining pass surfaced -- this
    column was a copy of exactly that, rule 5). An earlier version of this
    retirement kept `--connections` as an accepted-but-discarded argument, on the
    theory that it still proved a pass "did something" alongside `deferred_reason`/
    `notes`. An adversarial pass caught that as the exact anti-pattern the `doi`
    paragraph above already names: the CLI validated the JSON, used it to satisfy a
    refusal, and reported `"connections": 3` in a call that recorded zero of them
    anywhere -- a caller had every reason to believe a list had been persisted. A
    pass that ran and found something now says so through `--notes` (describe what
    was found, e.g. "N items, staged as candidates on exec X"), and stages the
    items themselves via `add-candidate --exec-id <the mining search's own exec,
    from log-search --mined-ref-id> --surfaced-in <payload>` -- the same discipline
    every other discovery step already follows. Two ways to prove a call did
    something now, not three: `deferred_reason` (not run) or `notes` (ran).
    """
    if direction not in _VALID_DIRECTIONS:
        raise Refusal(
            f"direction must be 'backward' or 'forward', got '{direction}'"
        )
    deferred_reason = (deferred_reason or "").strip() or None
    notes = (notes or "").strip() or None
    if deferred_reason and discharge_deferral:
        raise Refusal(
            f"{ref_id}: --discharge-deferral asserts the standing deferral belongs to "
            f"the {direction} pass just RUN; --deferred-reason asserts this pass was "
            f"deliberately NOT run. One call, one direction, cannot be both. Run the "
            f"discharging pass and the new deferral as two calls, naming the direction "
            f"each belongs to. (Silently ignored until 2026-09-18, which let the new "
            f"text overwrite the standing deferral with no carry into notes -- against "
            f"this verb's own --help, which promises the old text is never destroyed.)")
    if deferred_reason and notes:
        raise Refusal(
            f"{ref_id}: --deferred-reason says the pass was NOT run; --notes records what "
            f"a pass that RAN found. A row cannot assert both. R6: deferred_reason means "
            f"DELIBERATELY NOT SEARCHED and is never a findings channel.")
    if not deferred_reason and not notes:
        # THIRD STATE, ADDED 2026-09-18, NARROWED TO TWO 2026-09-28 when `connections`
        # was removed (see the docstring). The two-way guard this replaced conflated a
        # pass that was never run with one that ran and found nothing, and offered only
        # --deferred-reason for both -- which R6 forbids, since deferred_reason means
        # DELIBERATELY NOT SEARCHED. Measured on REF-00984: its backward pass ran over
        # 38 deposited references, 0 matched, and there was no way to say so. The column
        # for it already existed (citation_mining.notes) and had no writer at all.
        raise Refusal(
            f"{ref_id}: no --deferred-reason and no --notes. A mining pass that ran and "
            f"does not say what it found (even 'nothing') is indistinguishable from one "
            f"that never ran (R8's rule for searches, applied to mining). Use "
            f"--deferred-reason if the pass was NOT run; use --notes if it ran, whether "
            f"or not it found anything.")
    # citation_mining_status is asserted AGAINST this table by test_db_integrity C08:
    # 'mined' iff a non-deferred mining row resolves to it. Nothing in this writer ever
    # moved it, so the biconditional could not hold through the sanctioned path -- the
    # CLI was structurally unable to produce a state its own integrity test accepts.
    # `status` is DELIBERATELY NOT DERIVED HERE. It is derived at its point of use,
    # beside check_vocab, so that `status is None` still means "the operator named
    # none" everywhere above it. Deriving it here made the state-aware refusal below
    # dead code for the first hour of its life -- the reproduction meant to confirm
    # that guard is what caught it.
    dir_col = direction
    ts = now()

    with connect(dry_run) as conn:
        # THE WRITER IS WHERE THE DRIFT CAME FROM. This took a global ref_id and
        # wrote it into local_ref_id while leaving global_ref_id NULL, so the
        # pointer column the readers need was never populated and the label
        # column carried a value that was not a label. Key on the reference id;
        # derive the label from source_slug_links, which owns it.
        # ONE snapshot of the row, read BEFORE anything is written. It was two SELECTs
        # on the same key in the same transaction until 2026-09-18, the second issued
        # AFTER the UPDATE/INSERT below -- so the state-aware refusal fired with a write
        # already on the transaction, and in the INSERT branch it re-read a row this
        # function had just created, where both columns are NULL by construction.
        row = conn.execute(
            "SELECT backward, forward, notes, deferred_reason "
            "FROM citation_mining WHERE slug=? AND global_ref_id=?",
            [slug, ref_id]
        ).fetchone()
        prior_notes = (row["notes"] if row else None) or None
        prior_def = (row["deferred_reason"] if row else None) or None
        undischarged = None
        if row:
            # connections_produced is NOT touched here — retired 2026-09-28, see the
            # docstring. The row's existing value (if any, from before retirement)
            # is left exactly as it was; this UPDATE never re-reads or rewrites it.
            conn.execute(
                f"UPDATE citation_mining SET {dir_col}=1, "
                "updated_at=?, updated_by_session=? "
                "WHERE slug=? AND global_ref_id=?",
                [ts, session, slug, ref_id]
            )
        else:
            # local_ref_id is LOOKED UP, never invented: source_slug_links owns the
            # per-slug label. THE LOOKUP CAN MISS, and until 2026-09-18 the miss fell
            # through as `[None][0]` into a NOT NULL column, so a valid ref_id against
            # the wrong slug exited with an uncaught
            # `sqlite3.IntegrityError: NOT NULL constraint failed` instead of a
            # sentence. CLAUDE.md section 4: db.py refuses, and that is its whole value.
            label = (conn.execute("SELECT local_ref_id FROM source_slug_links "
                                  "WHERE slug=? AND ref_id=?", [slug, ref_id]
                                  ).fetchone() or [None])[0]
            if label is None:
                raise Refusal(
                    f"{ref_id} is not linked to slug '{slug}', so it has no per-slug "
                    f"label to key a mining row on. Either the slug is wrong, or the "
                    f"source needs `db.py link-source-slug` first. Mining a source "
                    f"under a slug it was never filed to writes a row no reader of "
                    f"that slug can resolve.")
            conn.execute(
                # doi is NOT written -- it is reachable through global_ref_id, and
                # copying it is what drifted 2 of 10 rows by case.
                # connections_produced is NOT written either -- retired 2026-09-28,
                # see the docstring. NULL forward (rule 5): the column survives
                # because committed data migrations INSERT it (rule 3), but no new
                # row sets it, and migration 099 relaxed its NOT NULL so this INSERT
                # can omit it instead of taking the old '[]' default and reading as
                # a real empty result.
                "INSERT INTO citation_mining "
                "(slug,local_ref_id,global_ref_id,backward,forward,"
                " created_at,created_by_session,"
                " updated_at,updated_by_session) "
                "VALUES (?,?,?,?,?,?,?,?,?)",
                [slug, label,
                 ref_id,
                 1 if direction == "backward" else 0,
                 1 if direction == "forward" else 0,
                 ts, session, ts, session]
            )
        # THE ROW'S EXISTING STATE DECIDES, NOT THIS CALL'S ARGUMENTS ALONE. The two
        # guards at the top of this function inspect only argv, so a --notes pass
        # followed by a --deferred-reason pass left BOTH columns populated -- the state
        # those guards call impossible -- and regressed citation_mining_status from
        # 'mined' back to 'deferred', erasing the record that a pass had executed.
        if deferred_reason:
            # KEYED ON citation_mining_status, VIA THE ONE DERIVATION -- not on whether
            # `notes` happens to be non-empty, which is how this guard was first
            # written and which was wrong in BOTH directions. False negative: a
            # `--connections` pass sets status='mined' and writes NO notes, so the
            # guard stayed silent on the skill's own documented happy path and let the
            # status regress -- the exact thing it exists to stop. False positive: it
            # fired on lead anchors whose ref resolves in source_locators rather than
            # evidence_sources, which have no status to regress. And `notes` had no
            # writer at all before 2026-09-18, so it was blind to every legacy row.
            _es = conn.execute("SELECT citation_mining_status FROM evidence_sources "
                               "WHERE ref_id=?", [ref_id]).fetchone()
            if mining_executed(_es["citation_mining_status"] if _es else None,
                               _es is not None) and status is None:
                raise Refusal(
                    f"{ref_id}: citation_mining_status already reads 'mined', so "
                    f"writing a deferral would regress it to 'deferred' and erase the "
                    f"record that a pass executed. That column is ONE flag for BOTH "
                    f"directions (GAP-015/GAP-022, unruled), so this is not guessed: "
                    f"pass --status explicitly to say which reading this source "
                    f"carries.")
            # A REPLACED DEFERRAL IS CARRIED, NOT DESTROYED. This UPDATE overwrote
            # `deferred_reason` outright, so re-deferring a row erased the reason the
            # previous session recorded -- while --help promised "its text is carried
            # into notes, never destroyed" and the else-branch below carried a
            # DISCHARGED one faithfully. Corrected 2026-09-18 after an adversarial pass.
            if prior_def and prior_def != deferred_reason:
                superseded = (f"DEFERRAL SUPERSEDED {ts} by {session} "
                              f"({direction} pass). It read: {prior_def}")
                carried_notes = "\n\n".join(
                    [x for x in (prior_notes, superseded) if x])
                conn.execute("UPDATE citation_mining SET notes=? "
                             "WHERE slug=? AND global_ref_id=?",
                             [carried_notes, slug, ref_id])
            conn.execute("UPDATE citation_mining SET deferred_reason=?, updated_at=?, "
                         "updated_by_session=? WHERE slug=? AND global_ref_id=?",
                         [deferred_reason, ts, session, slug, ref_id])
        else:
            # A PASS THAT RAN MAY DISCHARGE THE DEFERRAL IT WAS OWED -- BUT ONLY WHEN
            # SOMEONE SAYS SO. Added 2026-09-18 and narrowed the same day. The first cut
            # cleared deferred_reason UNCONDITIONALLY, which is wrong because
            # `deferred_reason` is ONE column while `backward`/`forward` are TWO: a
            # backward pass silently discharged REF-00989's FORWARD deferral ("Forward
            # mining means finding who cites this source...") and marked the source
            # mined, erasing owed work that the ruling's "runs eventually" depends on.
            # The direction cannot be recovered from the text, so it is not guessed:
            # --discharge-deferral is the operator asserting that the standing deferral
            # belongs to the direction just run. Without it the deferral STANDS, and the
            # returned dict says so rather than leaving it to be noticed later.
            carried = None
            if prior_def and discharge_deferral:
                carried = (f"DEFERRAL DISCHARGED {ts} by {session} "
                           f"({direction} pass). It read: {prior_def}")
            elif prior_def:
                undischarged = prior_def
            # NOTES ACCUMULATE, THEY DO NOT OVERWRITE. Corrected 2026-09-18: this UPDATE
            # replaced the column outright while `connections_produced` a few lines above
            # was carefully merged, so a second pass destroyed the first pass's record --
            # and any carried discharge text with it. (`connections_produced` itself
            # retired 2026-09-28; the contrast is historical, the lesson about `notes`
            # is not.)
            parts = [x for x in (prior_notes,
                                 f"[{direction} {ts}] {notes}" if notes else None,
                                 carried) if x]
            merged_notes = "\n\n".join(parts) if parts else None
            # ONE static statement, conditionality in the PARAMETERS. It was assembled
            # by `+` with a spliced ", deferred_reason=NULL" fragment, which hides the
            # column from the grep rule 4's caller sweep runs. `carried` is always an
            # element of `parts`, so `merged_notes != prior_notes` already covers it --
            # the old `or carried` could never change the outcome.
            if merged_notes != prior_notes:
                conn.execute(
                    "UPDATE citation_mining SET notes=?, deferred_reason=?, "
                    "updated_at=?, updated_by_session=? "
                    "WHERE slug=? AND global_ref_id=?",
                    [merged_notes, None if carried else prior_def,
                     ts, session, slug, ref_id])
        if status is None:
            # THE ROW'S POST-WRITE STATE DECIDES, NOT THIS CALL'S ARGUMENTS. Keyed on
            # `deferred_reason` alone, a --notes pass over a row whose
            # deferral STANDS wrote 'mined' while deferred_reason was still populated --
            # exactly the state test_db_integrity C08 rejects ('mined' iff a NON-deferred
            # row resolves to it). The sanctioned writer produced a C08-red database on
            # its own documented path; batch 17 escaped only because every pass happened
            # to carry --discharge-deferral. `undischarged` is set above precisely when a
            # deferral survived this call, so it is the state, not a second guess at it.
            status = "deferred" if (deferred_reason or undischarged) else "mined"
        dbcore.check_vocab(conn, "evidence_sources", "citation_mining_status",
                           status, "--status")
        conn.execute("UPDATE evidence_sources SET citation_mining_status=?, "
                     "updated_at=?, updated_by_session=? WHERE ref_id=?",
                     [status, ts, session, ref_id])
    out = {"logged": True, "status_set": status, "dry_run": dry_run}
    if undischarged:
        # The deferral this pass did not discharge stays visible -- see the else branch.
        out["deferral_still_standing"] = undischarged
    return out


class FrozenGridError(Refusal):
    """Raised on any attempt to write a legacy coverage grid. See _FROZEN_MSG.

    A Refusal, not the RuntimeError it was until 2026-09-10, because _FROZEN_MSG is a
    refusal in every sense that matters: it says the table no longer accepts writes, why
    it was frozen, and what replaced it. Its own class survives for anyone catching it
    specifically; only the base moved.

    NO OPERATOR MEETS IT TODAY, and the honest version of this note says so. The CLI never
    calls the two functions that raise it -- `main()`'s `upsert-coverage`/`upsert-language`
    branch prints _FROZEN_MSG itself and exits 2 -- so `upsert_search_coverage()` and
    `upsert_search_languages()` currently have no caller at all, and this class is
    classified correctly rather than usefully. That makes them a deletion candidate under
    CLAUDE.md §8 ("an uncalled script and an unread field are the same defect"), which is
    a separate judgment from this one and is not made here.
    """


# ---------------------------------------------------------------------------
# THE LEGACY COVERAGE GRIDS ARE FROZEN.
#
# `search_coverage` (slug x jurisdiction) and `search_languages` (slug x
# language) are hand-kept STATE matrices. `search_executions` is an event LOG:
# one row per query actually run, with its text, terms, engine, depth, results
# and admissions. State and log are different kinds of statement and both are
# worth having — but only if the state is DERIVED from the log. These were
# written independently, so the grid could assert coverage the log could not
# corroborate, and nothing could contradict it.
#
# It did, in both directions, measured 2026-08-06:
#   * 634 cells say SEARCHED. 15 have an execution logged for that exact
#     (slug, jurisdiction); 172 have any execution on the slug at all.
#   * 31 executions land on cells the grid still calls NOT-RUN — the log
#     records work the grid denies.
# The grid simultaneously over-claims and under-claims. It is not a coverage
# map; it is an artifact of whoever last remembered to update it.
#
# THIS IS NOT A NEW DECISION. `workplan/search-coverage-completion-workplan.md`
# already ruled it: replace the placeholder grids with a single logged event
# table and "derive every coverage matrix as a VIEW over that log"; the legacy
# grids are "frozen read-only as historical artifacts". It also ruled that the
# pre-log history is NOT to be reconstructed — the 617 SEARCHED rows written
# 2026-05-09 record real work whose query terms are unrecoverable, and inventing
# executions for them would be worse than leaving them.
#
# The log was built. The views were built (v_coverage_jurisdiction,
# v_coverage_language, v_coverage_branch). The FREEZE was not — because this
# function was the live write path and `research-log-manager_SKILL.md` still
# told every research session to call it. That is how six cells were marked
# SEARCHED on 2026-07-24, after the log existed, against two logged searches
# with different jurisdiction scoping.
#
# So the grids stop accepting writes here, which is the freeze, and `log_search`
# below gives the successor the write path it never had. A store cannot be
# retired while it is the only one that is easy to write to.
# ---------------------------------------------------------------------------
_FROZEN_MSG = (
    "{table} is FROZEN as a historical artifact and no longer accepts writes.\n"
    "\n"
    "It is a hand-kept grid that drifted from the search log in both directions;\n"
    "workplan/search-coverage-completion-workplan.md replaced it with the\n"
    "search_executions log plus derived views, and this closes the write path\n"
    "that kept it alive.\n"
    "\n"
    "Log the search itself instead — it carries what the grid could not (the\n"
    "query text, the terms, the engine, the depth, what came back):\n"
    "\n"
    "  python3 scripts/db.py log-search --slug SLUG --language EN \\\n"
    "      --jurisdiction AU --query-text '...' --engine pubmed \\\n"
    "      --depth-method scoping --results-found N --results-screened N \\\n"
    "      --session SESSION\n"
    "\n"
    "A search you deliberately did NOT run is also a logged row — pass\n"
    "--deferred-reason and say why. Coverage then reads out of\n"
    "v_coverage_jurisdiction / v_coverage_language, which cannot claim more\n"
    "than was logged."
)


def upsert_search_coverage(slug: str, jurisdiction: str,
                           data: dict, session: str,
                           dry_run: bool = False):
    raise FrozenGridError(_FROZEN_MSG.format(table="search_coverage"))


def upsert_search_language(slug: str, language: str,
                           data: dict, session: str,
                           dry_run: bool = False):
    raise FrozenGridError(_FROZEN_MSG.format(table="search_languages"))


def _link_result_artefacts(conn, exec_id, artefacts, *, mined_ref_id, query_text,
                           session, ts):
    """Validate and insert `search_execution_artefacts` rows for `artefacts`.

    RC1 (DR-2026-09-26 section 2.2b)'s writer side, shared by `log-search
    --result-artefact` and `amend-search --add-result-artefact` so the two writers
    cannot drift. `retrieval_log.check_artefact_link` is the ONE place the refusal
    is evaluated -- `provenance_artefact_audit.py`'s re-derivation from bytes calls
    the same function, per rule 5.
    """
    if not artefacts:
        return
    sys.path.insert(0, str(Path(__file__).resolve().parent / "research"))
    import retrieval_log                                              # noqa: E402
    for artefact in artefacts:
        try:
            if mined_ref_id:
                retrieval_log.check_artefact_link(artefact, mined_ref_id=mined_ref_id)
            else:
                retrieval_log.check_artefact_link(artefact, query_text=query_text)
        except ValueError as e:
            raise Refusal(f"--result-artefact {artefact}: {e}")
        conn.execute(
            "INSERT INTO search_execution_artefacts "
            "(exec_id, artefact, created_by_session, created_at) VALUES (?, ?, ?, ?)",
            [exec_id, artefact, session, ts])


def log_search(slug: str, language: str, query_text: str, engine: str,
               depth_method: str, session: str,
               jurisdiction: str = None, target_tier: int = None,
               target_evidence_type: str = None, target_scope: str = None,
               terms_used: str = None, mining_direction: str = None,
               results_found: int = 0, results_screened: int = 0,
               results_admitted: int = 0, saturation_signal: str = None,
               admitted_ref_ids=None, deferred_reason: str = None,
               backfill: int = 0, findings_note: str = None,
               harm_finding: int = 0, prior_expectation: str = None,
               origin: str = "planned", mined_ref_id: str = None,
               origin_pass_id: int = None, result_artefacts=None,
               dry_run: bool = False) -> int:
    """Append one row to search_executions. Returns its exec_id.

    The successor to upsert-coverage/upsert-language. A row here is a completed
    unit of work whether or not it found anything: R8 says keep the empties, and
    a zero-yield search with a well-formed query is evidence about the world,
    not a failure to record. A search deliberately not run is also a row —
    `deferred_reason` is what makes "not looked for" different from "nothing
    found", which is the distinction the whole pipeline is built on.

    `backfill=1` marks a row reconstructed after the fact rather than logged as
    it happened. It exists so honest reconstruction is possible without being
    indistinguishable from contemporaneous logging; it is currently 0 on every
    row.
    """
    # Refuse what H05/H07 forbid, at write time, with a named cause.
    #
    # The first version accepted all of this and let the blocking gate find it
    # later: duplicate ids (H07), results_admitted disagreeing with the number of
    # admitted ids (H05), and a junction written with INSERT OR IGNORE — the same
    # silent no-op this file denounces at length twenty lines up in
    # insert_evidence_source. One file, one diff, two opposite doctrines. A gate
    # that catches a bad write after it lands is strictly worse than a write path
    # that cannot make it.
    # R8 says log every query WITH the prior written before you run it. A flag that
    # is merely available is not that rule: batch 05 logged 43 searches and CHECK 7
    # reports 9 verified citations with no prior, permanently, because
    # search_executions is append-only (R8) and `amend-search` writes only
    # findings_note and harm_finding -- so those nine can never be cleared by any
    # sanctioned path. The check went red forever, and a check that is red forever
    # is one its reader learns to skip: exactly the cry-wolf failure this session
    # fixed in the fidelity checker and then rebuilt here. Refusing at the writer is
    # the only place the prior can still be honest, because after this call the
    # results exist and anything written is a reconstruction.
    #
    # Deliberately NOT argparse required=True: this refusal also catches programmatic
    # callers, and it can say why. An empty string is refused too -- R8 keeps empties
    # as completed work, and "I expected nothing" is a prior worth typing.
    if not (prior_expectation or "").strip():
        raise Refusal(
            "--prior-expectation is required. Write what you expect this search to "
            "find BEFORE you run it (DR-2026-05-09 24). Written afterwards it is a "
            "rationalisation wearing the field that exists to prevent one, and there "
            "is no sanctioned path to add it later: search_executions is append-only "
            "under R8 and amend-search cannot touch this column. A zero-yield "
            "expectation is a legitimate prior -- say so.")
    # The declared jurisdiction vocabulary (I7). Append-only like the prior: amend-search
    # cannot correct this column either, so a wrong code here costs a compensating
    # migration.
    dbcore.check_jurisdiction(jurisdiction, "log-search --jurisdiction")

    # RC5 (DR-2026-09-26 5.2c). `origin` is the INITIATION axis (why the step ran);
    # `mining_direction` is the METHOD axis (how) -- orthogonal, so neither can stand
    # in for the other, and each refusal below names which one was left incoherent.
    mining_on = (mining_direction or "none") != "none"
    if mining_on and not mined_ref_id:
        raise Refusal(
            f"--mining-direction {mining_direction} with no --mined-ref-id. A "
            f"mining pass with no typed source is the gap RC5 exists to close -- "
            f"name what was mined.")
    if mined_ref_id and not mining_on:
        raise Refusal(
            f"--mined-ref-id {mined_ref_id} with --mining-direction "
            f"{mining_direction or 'none'!r}. A mined source with no mining "
            f"direction is incoherent.")
    if origin != "planned" and (target_tier or target_evidence_type or target_scope):
        raise Refusal(
            f"--origin {origin} with a --target-tier/--target-evidence-type/"
            f"--target-scope flag. A lookup targets no tier -- that is what keeps "
            f"it out of v_coverage_branch's Co-1 count.")
    if origin == "adversarial-pass" and origin_pass_id is None:
        raise Refusal(
            "--origin adversarial-pass with no --origin-pass-id. Name the pass "
            "that ran it, or log this as history with amend-search --set-origin "
            "adversarial-pass, which alone accepts a NULL pass id for a pass that "
            "predates adversarial_passes.")
    if origin_pass_id is not None and origin != "adversarial-pass":
        # Named, not the bare `CHECK constraint failed` the schema's own
        # `origin_pass_id IS NULL OR origin = 'adversarial-pass'` raises at INSERT.
        raise Refusal(
            f"--origin-pass-id {origin_pass_id} with --origin {origin!r}. The CHECK "
            f"permits a pass id only with origin=adversarial-pass.")

    ids = list(admitted_ref_ids or [])
    if len(set(ids)) != len(ids):
        dupes = sorted({r for r in ids if ids.count(r) > 1})
        raise Refusal(
            f"--admitted-ref-id repeated: {', '.join(dupes)}. One admission edge "
            f"per (search, source); a repeat is a miscount, not two admissions "
            f"(invariant H07).")
    if results_admitted and not ids:
        # THE DIRECTION THE CHECK BELOW COULD NOT SEE, closed 2026-09-13.
        # That check is conditioned on `ids`, so it fires only when SOME edges
        # were named. An admission count with NO --admitted-ref-id at all --
        # the emptiest violation of the same invariant -- passed silently and
        # wrote a row claiming admissions it has no junction edges for. Found
        # by tripping it while logging batch 07, then measured against
        # canonical: 8 of the 13 executions claiming admissions carry 0 edges,
        # and one of them (exec 44) is batch 06, which the definition-of-done
        # gate had passed COMPLIANT. This is CLAUDE.md 5(a) inside the refusal
        # that exists to prevent it -- a guard that examined nothing.
        #
        # It matters because the junction is the ONE carrier (see the comment
        # at the INSERT below): admitted_ref_ids is deliberately not written,
        # so with no edge there is no path at all from a source back to the
        # search that admitted it.
        raise Refusal(
            f"--results-admitted {results_admitted} with no --admitted-ref-id. "
            f"The count and the edges are the same fact (invariant H05), and "
            f"search_admissions is the only carrier of it -- admitted_ref_ids "
            f"is deliberately not written. A count with no edge claims an "
            f"admission nothing can trace. Name the ref_id(s) admitted, or "
            f"record 0 and say why in --findings-note.")
    if ids and results_admitted and results_admitted != len(ids):
        raise Refusal(
            f"--results-admitted {results_admitted} disagrees with "
            f"{len(ids)} --admitted-ref-id value(s). The count and the edges are "
            f"the same fact; they may not differ (invariant H05).")
    if ids and not results_admitted:
        results_admitted = len(ids)

    ts = now()
    row = {
        "slug": slug, "jurisdiction": jurisdiction, "language": language,
        "target_tier": target_tier, "target_evidence_type": target_evidence_type,
        "target_scope": target_scope, "query_text": query_text,
        "terms_used": terms_used, "engine": engine, "depth_method": depth_method,
        "mining_direction": mining_direction,
        "results_found": results_found, "results_screened": results_screened,
        "results_admitted": results_admitted,
        "saturation_signal": saturation_signal,
        # admitted_ref_ids intentionally NOT written — search_admissions is the
        # sole home (owner ruling 2026-08-24). Column retained because committed
        # data migrations INSERT it and migrations are append-only.

        "deferred_reason": deferred_reason, "backfill": backfill,
        # The audit columns are DERIVED below, inside the connection, and are
        # deliberately absent here -- see the stamp_for call.
        "findings_note": findings_note, "harm_finding": harm_finding,
        # The prior belongs HERE, on the search, and nowhere else. Migration 069
        # moved it off evidence_sources, where it could only be reconstructed after
        # reading the source -- the artefact the field exists to prevent.
        "prior_expectation": prior_expectation,
        "origin": origin, "mined_ref_id": mined_ref_id,
        "origin_pass_id": origin_pass_id,
    }
    with connect(dry_run) as conn:
        if mined_ref_id and not conn.execute(
                "SELECT 1 FROM evidence_sources WHERE ref_id=?", [mined_ref_id]).fetchone():
            # Named, not a bare FOREIGN KEY constraint failed -- same discipline as
            # the --admitted-ref-id check below.
            raise Refusal(
                f"--mined-ref-id {mined_ref_id} is not in evidence_sources. File "
                f"the source first, then log the pass that mined it.")
        # DERIVED, NEVER HAND-TYPED. This table's audit columns were spelled
        # `session` and `executed_at` here as string literals until migration
        # 085 renamed them to the corpus-wide `created_by_session`/`created_at`.
        # That rename's sweep was empirical -- it ran the check battery against
        # a rebuilt DB -- and it could not see these two, because NO CHECK
        # WRITES A SEARCH EXECUTION. The battery stayed green and `log-search`,
        # the first command of every research batch, raised "table
        # search_executions has no column named session" on its next call.
        # Every writer that reached for stamp_for instead survived the same
        # rename untouched, which is the whole argument for deriving: the
        # schema is the one home of the column's name (rule 8).
        row.update(dbcore.stamp_for(conn, "search_executions", session))
        # Keep the junction rows stamped with the execution row's own instant
        # rather than a second, slightly later `now()`.
        ts = row.get("created_at", ts)
        cols = ", ".join(row)
        ph = ", ".join(["?"] * len(row))
        cur = conn.execute(
            f"INSERT INTO search_executions ({cols}) VALUES ({ph})",
            list(row.values()))
        exec_id = cur.lastrowid
        # ONE carrier: search_admissions. Until 2026-08-24 this dual-wrote the
        # same fact into admitted_ref_ids (JSON on the row) and kept the two
        # honest with parity checks H03/H04. Owner ruling 2026-08-24: "it is
        # better to have a table cell point to another table cell than to
        # rewrite" — a fact written into two tables is drift waiting to happen,
        # and a parity check does not prevent that, it makes it survivable and
        # therefore permanent. Nothing ever READ the JSON: it was write-only
        # data guarded by a test. The junction is the record, and it carries its
        # own created_at.
        for ref_id in ids:
            if not conn.execute("SELECT 1 FROM evidence_sources WHERE ref_id=?",
                                [ref_id]).fetchone():
                # Named, not a bare FOREIGN KEY constraint failed. The whole
                # transaction rolls back, execution row included.
                raise Refusal(
                    f"--admitted-ref-id {ref_id} is not in evidence_sources. "
                    f"File the source first (`db.py add-source`), then log the "
                    f"search that admitted it.")
            conn.execute(
                "INSERT INTO search_admissions "
                "(exec_id, ref_id, created_at, created_by_session) "
                "VALUES (?, ?, ?, ?)", [exec_id, ref_id, ts, session])
        _link_result_artefacts(conn, exec_id, result_artefacts,
                               mined_ref_id=mined_ref_id, query_text=query_text,
                               session=session, ts=ts)
        return exec_id


def next_term_id() -> str:
    with connect(readonly=True) as conn:
        row = conn.execute(
            "SELECT term_id FROM terms ORDER BY term_id DESC LIMIT 1"
        ).fetchone()
    if not row:
        return "TERM-0001"
    return f"TERM-{int(row['term_id'].split('-')[1]) + 1:04d}"


# --- Domain queries ---


def get_open_gaps(priority: str = None) -> list[dict]:
    q = "SELECT * FROM gaps WHERE status LIKE 'OPEN%'"
    params = []
    if priority:
        q += " AND priority=?"
        params.append(priority)
    q += " ORDER BY priority, gap_id"
    with connect(readonly=True) as conn:
        return [dict(r) for r in conn.execute(q, params).fetchall()]


def get_connections(status: str = None, confidence: str = None,
                    summary: bool = False) -> list[dict] | dict:
    if summary:
        q = """
            SELECT confidence, COUNT(*) AS cnt
            FROM connections
            WHERE 1=1
        """
        params = []
        if status:
            q += " AND status=?"
            params.append(status)
        q += " GROUP BY confidence"
        with connect(readonly=True) as conn:
            rows = conn.execute(q, params).fetchall()
        result = {r["confidence"]: r["cnt"] for r in rows}
        result["total"] = sum(result.values())
        return result

    q = """
        SELECT c.*, GROUP_CONCAT(ct.target, ', ') AS targets
        FROM connections c
        LEFT JOIN connection_targets ct USING (con_id)
        WHERE 1=1
    """
    params = []
    if status:
        q += " AND c.status=?"
        params.append(status)
    if confidence:
        q += " AND c.confidence=?"
        params.append(confidence)
    q += " GROUP BY c.con_id ORDER BY c.confidence DESC"
    with connect(readonly=True) as conn:
        return [dict(r) for r in conn.execute(q, params).fetchall()]


def get_unmined_sources(slug: str) -> list[dict]:
    with connect(readonly=True) as conn:
        rows = conn.execute("""
            SELECT ssl.local_ref_id,
                   es.doi, es.pub_title,
                   -- THE RULING'S COLUMN IS THE ANSWER; the flags are reported beside
                   -- it so a reader can see the disagreement rather than inherit it.
                   COALESCE(es.citation_mining_status, '') AS citation_mining_status,
                   cm.deferred_reason,
                   COALESCE(cm.backward, 0) AS backward,
                   COALESCE(cm.forward,  0) AS forward
            FROM source_slug_links ssl
            JOIN evidence_sources es ON ssl.ref_id = es.ref_id
            LEFT JOIN citation_mining cm
                -- POINTER, NOT COPY (owner ruling 2026-08-24). This joined on
                -- local_ref_id, the per-slug LABEL, which is copied into both tables
                -- and had already drifted: source_slug_links held RAP-06/09/10 while
                -- citation_mining held RAP-F61/F69/F70 for the same three sources, so
                -- REF-00561/00969/00970 reported UNMINED after being fully mined. The
                -- reference id was in every row the whole time; join on it.
                ON cm.slug=ssl.slug AND cm.global_ref_id=ssl.ref_id
            WHERE ssl.slug=?
            -- OWNER RULING 2026-09-18: "executed is `mined`". The direction flags do
            -- NOT mean a pass ran -- log_mining raises {direction}=1 on a DEFERRAL too
            -- -- so `backward=0 OR forward=0` answered a different question from the one
            -- this verb is asked. Measured the same day: REF-00989 and REF-00993 carry
            -- backward=1, forward=1 AND a standing FORWARD deferral, so this returned
            -- neither, and a session routed to the backlog through this verb was handed
            -- a quarter less work than it was owed. citation_mining_status is the column
            -- the ruling names; a row with no mining row at all is NULL and sorts in.
            AND COALESCE(es.citation_mining_status, '') <> 'mined'
            ORDER BY ssl.local_ref_id
        """, [slug]).fetchall()
    return [dict(r) for r in rows]


def get_coverage_completeness(slug: str) -> dict:
    """Coverage for a slug, answered from the search LOG.

    This used to count non-NOT-RUN cells in the frozen grids, which is how a slug
    could report 14 jurisdictions searched against 0 logged searches. The grids
    are hand-kept and were never reconciled against the log; the log is the only
    store that can show its work.

    The grid's numbers are still returned, under `legacy_grid`, because they are
    the record of pre-log work that genuinely happened and is genuinely
    unrecoverable in query terms. They are labelled, not deleted — an
    unattributed number is what caused this. Nothing computes `complete` from
    them any more.
    """
    with connect(readonly=True) as conn:
        jur = conn.execute(
            "SELECT COUNT(DISTINCT jurisdiction) AS n FROM search_executions "
            "WHERE slug=? AND jurisdiction IS NOT NULL AND deferred_reason IS NULL",
            [slug]).fetchone()["n"]
        lang = conn.execute(
            "SELECT COUNT(DISTINCT language) AS n FROM search_executions "
            "WHERE slug=? AND deferred_reason IS NULL", [slug]).fetchone()["n"]
        deferred = conn.execute(
            "SELECT COUNT(*) AS n FROM search_executions "
            "WHERE slug=? AND deferred_reason IS NOT NULL", [slug]).fetchone()["n"]
        g_jur = conn.execute(
            "SELECT COUNT(*) AS n FROM search_coverage "
            "WHERE slug=? AND status != 'NOT-RUN'", [slug]).fetchone()["n"]
        g_lang = conn.execute(
            "SELECT COUNT(*) AS n FROM search_languages "
            "WHERE slug=? AND status != 'NOT-RUN'", [slug]).fetchone()["n"]
        # Required scope comes from lang_jur_map, the bridge that declares it —
        # not from a literal. These were hardcoded 24 and 14 while
        # tools/pipeline_completeness.py computed against 48, so "how much
        # coverage is owed" had two answers differing 2x, shipped the same day.
        req_jur = conn.execute(
            "SELECT COUNT(DISTINCT jurisdiction) AS n FROM lang_jur_map").fetchone()["n"]
        req_lang = conn.execute(
            "SELECT COUNT(DISTINCT language) AS n FROM lang_jur_map").fetchone()["n"]
    return {
        "slug": slug,
        "jurisdictions_searched": jur,
        "jurisdictions_required": req_jur,
        "languages_searched": lang,
        "languages_required": req_lang,
        "searches_deferred_with_reason": deferred,
        "complete": jur >= req_jur and lang >= req_lang,
        "legacy_grid": {
            "jurisdictions": g_jur,
            "languages": g_lang,
            "note": "frozen hand-kept grids; pre-log work, query terms "
                    "unrecoverable. Not evidence of a search — see "
                    "workplan/search-coverage-completion-workplan.md",
        },
    }


def get_synonyms(item_code: str, language: str = None) -> list[dict]:
    q = """
        SELECT t.term_id, t.canonical_en, ta.alias, ta.language,
               ta.alias_type, ta.jurisdiction
        FROM term_item_links til
        JOIN terms t ON til.term_id = t.term_id
        JOIN term_aliases ta ON t.term_id = ta.term_id
        WHERE til.item_code=?
    """
    params = [item_code]
    if language:
        q += " AND ta.language=?"
        params.append(language)
    q += " ORDER BY t.canonical_en, ta.language, ta.alias"
    with connect(readonly=True) as conn:
        return [dict(r) for r in conn.execute(q, params).fetchall()]


# ── CO-0009 Phase 1 Session 1b additions ──────────────────────────────────

import re as _re

# _VALID_CONFLICT_STATUS / _VALID_ITEM_STATUS / _VALID_RUN_STATUS RETIRED 2026-09-27
# (RC2, DR-2026-09-26-recurring-defect-shapes-remediation.md section 3.2b): each equalled
# a live column CHECK exactly (conflicts.status, items.status, item_audit_runs.status
# respectively) — derived_not_curated_audit.py Class 3 now fails a curated copy of one of
# these outright. Replaced by dbcore.check_declared / dbcore.schema_choices at every
# call site; the owner ruling and migration each cited are unaffected, only their
# vocabulary's SECOND home is gone.
_ITEM_CODE_RE        = _re.compile(r"^[A-K]-\d{2}[a-z]?$")
_CATEGORY_RE         = _re.compile(r"^[A-K]$")
_PIPELINE_STEPS      = frozenset({
    "connection-discovery-spec", "connection-discovery-evidence",
    "conflict-mapper", "content-gap-analyzer", "evidence-auditor",
    "functional-deficit-auditor", "economics-auditor", "audit-consolidator",
})


def next_conf_id() -> str:
    with connect(readonly=True) as conn:
        row = conn.execute(
            "SELECT conflict_id FROM conflicts "
            "WHERE conflict_id GLOB 'CONF-[0-9]*' "
            "ORDER BY CAST(SUBSTR(conflict_id,6) AS INTEGER) DESC LIMIT 1"
        ).fetchone()
    if not row:
        return "CONF-0001"
    return f"CONF-{int(row['conflict_id'].split('-')[1]) + 1:04d}"


def insert_conflict(data: dict, session: str, dry_run: bool = False) -> str:
    if data.get("pop_a") and data.get("pop_b"):
        if data["pop_a"] > data["pop_b"]:
            raise Refusal(
                f"pop_a must be < pop_b lexicographically. "
                f"Got pop_a={data['pop_a']} pop_b={data['pop_b']}. "
                f"Swap them before inserting."
            )
    row = {**data, **audit(session)}
    with connect(dry_run) as conn:
        # conflicts.status happens to share its vocabulary with decisions.status; this
        # writer INSERTs into conflicts, so that is the CHECK it validates against
        # (rule 8: derive from the column the writer actually writes, not whichever
        # column a value-set match finds first).
        dbcore.check_declared(conn, "conflicts", "status", data.get("status"),
                              "insert_conflict")
        cols = ", ".join(row)
        ph   = ", ".join(["?"] * len(row))
        conn.execute(f"INSERT INTO conflicts ({cols}) VALUES ({ph})", list(row.values()))
    return data["conflict_id"]


def update_conflict(conflict_id: str, session: str,
                    status: str = None, resolution: str = None,
                    evidence: str = None, gap_id: str = None,
                    dry_run: bool = False):
    u    = _upd(session)
    sets = [f"updated_at=?", f"updated_by_session=?"]
    vals = [u["updated_at"], u["updated_by_session"]]
    if status is not None:
        sets.append("status=?");     vals.append(status)
    if resolution is not None:
        sets.append("resolution=?"); vals.append(resolution)
    if evidence is not None:
        sets.append("evidence=?");   vals.append(evidence)
    if gap_id is not None:
        sets.append("gap_id=?");     vals.append(gap_id)
    vals.append(conflict_id)
    with connect(dry_run) as conn:
        if status is not None:
            dbcore.check_declared(conn, "conflicts", "status", status, "update_conflict")
        conn.execute(
            f"UPDATE conflicts SET {', '.join(sets)} WHERE conflict_id=?", vals
        )


def get_conflicts(item_code: str = None, domain: str = None,
                  status: str = None, summary: bool = False) -> list | dict:
    q     = "SELECT * FROM conflicts WHERE 1=1"
    params = []
    if item_code:
        q += " AND item_code=?"; params.append(item_code)
    if domain:
        q += " AND domain=?";    params.append(domain)
    if status:
        q += " AND status=?";    params.append(status)
    q += " ORDER BY conflict_id"
    with connect(readonly=True) as conn:
        rows = [dict(r) for r in conn.execute(q, params).fetchall()]
    if summary:
        from collections import Counter
        return dict(Counter(r["status"] for r in rows))
    return rows


def delete_connection(con_id: str, session: str, dry_run: bool = False):
    """Hard-delete a connection and its targets. Use sparingly — for data corrections only."""
    with connect(dry_run) as conn:
        conn.execute("DELETE FROM connection_targets WHERE con_id=?", [con_id])
        conn.execute("DELETE FROM connections WHERE con_id=?", [con_id])


def get_items(category: str = None, status: str = None) -> list:
    q      = "SELECT * FROM items WHERE 1=1"
    params = []
    if category:
        q += " AND category=?"; params.append(category)
    if status:
        q += " AND status=?";   params.append(status)
    q += " ORDER BY item_code"
    with connect(readonly=True) as conn:
        return [dict(r) for r in conn.execute(q, params).fetchall()]


def insert_audit_run(data: dict, session: str, dry_run: bool = False) -> str:
    row = {**data, **audit(session)}
    with connect(dry_run) as conn:
        if data.get("status") is not None:
            dbcore.check_declared(conn, "item_audit_runs", "status", data["status"],
                                  "insert_audit_run")
        cols = ", ".join(row)
        ph   = ", ".join(["?"] * len(row))
        conn.execute(f"INSERT INTO item_audit_runs ({cols}) VALUES ({ph})", list(row.values()))
    return data["run_id"]


def update_audit_run(run_id: str, session: str,
                     status: str = None, steps_complete: list = None,
                     steps_started: list = None, brief_path: str = None,
                     spec_hash: str = None, dry_run: bool = False):
    # Validate step names
    for step_list in [steps_complete or [], steps_started or []]:
        unknown = [s for s in step_list if s not in _PIPELINE_STEPS]
        if unknown:
            raise Refusal(f"Unknown pipeline step(s): {unknown}. Valid: {sorted(_PIPELINE_STEPS)}")
    u    = _upd(session)
    sets = ["updated_at=?", "updated_by_session=?"]
    vals = [u["updated_at"], u["updated_by_session"]]
    if status is not None:
        sets.append("status=?");          vals.append(status)
    if steps_complete is not None:
        sets.append("steps_complete=?");  vals.append(json.dumps(steps_complete))
    if steps_started is not None:
        sets.append("steps_started=?");   vals.append(json.dumps(steps_started))
    if brief_path is not None:
        sets.append("brief_path=?");      vals.append(brief_path)
    if spec_hash is not None:
        sets.append("spec_hash=?");       vals.append(spec_hash)
    vals.append(run_id)
    with connect(dry_run) as conn:
        if status is not None:
            dbcore.check_declared(conn, "item_audit_runs", "status", status,
                                  "update_audit_run")
        conn.execute(
            f"UPDATE item_audit_runs SET {', '.join(sets)} WHERE run_id=?", vals
        )


def get_audit_runs(item_code: str = None, status: str = None) -> list:
    q      = "SELECT * FROM item_audit_runs WHERE 1=1"
    params = []
    if item_code:
        q += " AND item_code=?"; params.append(item_code)
    if status:
        q += " AND status=?";    params.append(status)
    q += " ORDER BY created_at DESC"
    with connect(readonly=True) as conn:
        return [dict(r) for r in conn.execute(q, params).fetchall()]


# --- CLI ---


def main():
    parser = argparse.ArgumentParser(
        description="Guidebook SQLite data layer CLI"
    )
    sub = parser.add_subparsers(dest="command")

    # init — RETIRED 2026-08-15 with scripts/init_db.py (owner approval of the
    # Tier-1 batch). It applied migration 001 only, so it never produced a
    # working database; `migrate_db.py --rebuild` is the real path and is what
    # CLAUDE.md §4 already tells readers to use instead. (Pointer corrected
    # 2026-08-22, was §10.)

    # migrate
    sub.add_parser("migrate", help="Run pending schema migrations")

    # gaps
    p_gaps = sub.add_parser("gaps", help="Query gaps")
    p_gaps.add_argument("--priority", choices=dbcore.schema_choices("gaps", "priority"))
    p_gaps.add_argument("--status")

    # connections
    p_conn = sub.add_parser("connections", help="Query connections")
    p_conn.add_argument("--status")
    p_conn.add_argument("--confidence")
    p_conn.add_argument("--summary", action="store_true")

    # is-mined
    p_mined = sub.add_parser("is-mined", help="Check mining status")
    p_mined.add_argument("--slug", required=True)
    p_mined.add_argument("--ref", required=True)

    # log-mining
    p_logm = sub.add_parser("log-mining", help="Log citation mining")
    p_logm.add_argument("--slug", required=True)
    p_logm.add_argument("--ref", required=True)
    p_logm.add_argument("--direction", required=True,
                        choices=["backward", "forward"])
    p_logm.add_argument("--deferred-reason", dest="deferred_reason",
                        help="Why this anchor was NOT mined -- DELIBERATELY NOT SEARCHED "
                             "(R6). Never a findings channel: if the pass RAN, use --notes.")
    p_logm.add_argument("--notes",
                        help="What a pass that RAN found, including nothing. Writes "
                             "citation_mining.notes, which existed with no writer until "
                             "2026-09-18. APPENDS -- it never overwrites an earlier "
                             "pass's note. Mutually exclusive with --deferred-reason.")
    p_logm.add_argument("--discharge-deferral", dest="discharge_deferral",
                        action="store_true",
                        help="Assert that the deferral standing on this row belongs to "
                             "the direction just run, and clear it (its text is carried "
                             "into notes, never destroyed). NOT automatic, and that is "
                             "the point: deferred_reason is ONE column while backward "
                             "and forward are TWO, so a backward pass cannot tell "
                             "whether the standing deferral was its own. Without this "
                             "flag the deferral stands and the result says so.")
    p_logm.add_argument("--status", dest="mining_status",
                        help="citation_mining_status to set on the source. Live "
                             "vocabulary from the column's own CHECK. Derived when "
                             "omitted: 'deferred' with --deferred-reason, 'mined' "
                             "otherwise -- so an executed zero-yield pass (--notes) "
                             "derives 'mined', which is the 2026-09-18 ruling that "
                             "executed IS mined. This help said \"'mined' with "
                             "connections, 'deferred' without\" until that day, which "
                             "described neither the code nor the ruling.")
    p_logm.add_argument("--session", required=True)
    p_logm.add_argument("--dry-run", action="store_true")

    # ---- ACT 2 (2026-08-25): the tables the CLI could not write ----
    p_cand = sub.add_parser("add-candidate", help="Stage a screened candidate (search_candidates)")
    p_cand.add_argument("--exec-id", type=int)
    p_cand.add_argument("--found-under-slug", required=True)
    p_cand.add_argument("--suggested-slug")
    p_cand.add_argument("--disposition", required=True,
                        help="Live vocabulary, derived from the table; not a list in this file")
    p_cand.add_argument("--title", required=True)
    p_cand.add_argument("--locator")
    p_cand.add_argument("--locator-status")
    p_cand.add_argument("--tier-guess", type=int)
    p_cand.add_argument("--harm-finding", type=int, default=0, choices=[0, 1])
    p_cand.add_argument("--why-not-admitted")
    p_cand.add_argument("--notes")
    # RC1 (DR-2026-09-26 2.2c/d). The path of the payload the candidate appeared
    # in -- or a tracked file under transcripts/, for a route that was never
    # persisted (exec 100's TRANSCRIPT-ONLY shape).
    p_cand.add_argument("--surfaced-in", required=True,
                        help="retrieval-log/<session>/<file> (must already be a "
                             "search_execution_artefacts row for --exec-id), or a "
                             "tracked transcripts/ file")
    p_cand.add_argument("--surfaced-quote",
                        help="a verbatim string from --surfaced-in, required only "
                             "when locator carries no single DOI")
    p_cand.add_argument("--session", required=True)
    p_cand.add_argument("--dry-run", action="store_true")

    p_epm = sub.add_parser("add-population-match",
                           help="Grade population-of-study vs population-served (R13)")
    p_epm.add_argument("--ref-id", required=True)
    p_epm.add_argument("--target-population", required=True)
    p_epm.add_argument("--study-population")
    p_epm.add_argument("--sample-size", type=int)
    p_epm.add_argument("--match-grade", required=True)
    p_epm.add_argument("--mismatch-note")
    p_epm.add_argument("--gap-id")
    p_epm.add_argument("--session", required=True)
    p_epm.add_argument("--dry-run", action="store_true")

    p_jv = sub.add_parser("add-jurisdictional-value",
                          help="Record a code/regulatory value (T4-T6 stratum)")
    p_jv.add_argument("--jv-id")
    p_jv.add_argument("--item-code", required=True)
    p_jv.add_argument("--jurisdiction", required=True)
    p_jv.add_argument("--standard-name")
    p_jv.add_argument("--value-text")
    p_jv.add_argument("--value-numeric", type=float)
    p_jv.add_argument("--unit")
    p_jv.add_argument("--is-code-minimum", type=int, choices=[0, 1])
    p_jv.add_argument("--evidence-tier", type=int, required=True)
    p_jv.add_argument("--source-section")
    p_jv.add_argument("--loc-section")
    p_jv.add_argument("--loc-clause")
    p_jv.add_argument("--notes")
    p_jv.add_argument("--session", required=True)
    p_jv.add_argument("--dry-run", action="store_true")

    p_econ = sub.add_parser("add-economics-entry", help="Record a Part-13 economics finding")
    p_econ.add_argument("--entry-id", required=True)
    p_econ.add_argument("--pillar", required=True)
    p_econ.add_argument("--entry-type", required=True)
    p_econ.add_argument("--ref-id", help="Preferred. Bibliographic facts are reached through it")
    p_econ.add_argument("--source", help="Only for an entry with NO ref_id")
    p_econ.add_argument("--finding", required=True)
    p_econ.add_argument("--status", required=True)
    p_econ.add_argument("--value-numeric", type=float)
    p_econ.add_argument("--value-unit")
    p_econ.add_argument("--currency")
    p_econ.add_argument("--jurisdiction")
    p_econ.add_argument("--notes")
    p_econ.add_argument("--session", required=True)
    p_econ.add_argument("--dry-run", action="store_true")

    p_cs = sub.add_parser("add-case-study", help="Record a Part-12 case study")
    p_cs.add_argument("--case-study-id", required=True)
    p_cs.add_argument("--slug", required=True)
    p_cs.add_argument("--title", required=True)
    p_cs.add_argument("--building-type", required=True)
    p_cs.add_argument("--location", required=True)
    p_cs.add_argument("--year", type=int)
    p_cs.add_argument("--harm-finding", type=int, default=0, choices=[0, 1])
    p_cs.add_argument("--status", required=True)
    p_cs.add_argument("--sources", help="Material with NO ref_id. A REF-NNNNN here is refused")
    p_cs.add_argument("--notes")
    p_cs.add_argument("--session", required=True)
    p_cs.add_argument("--dry-run", action="store_true")

    p_rcl = sub.add_parser("add-code-lead",
                           help="Record a code/standard lead (research_code_leads)")
    p_rcl.add_argument("--jurisdiction", required=True,
                       help="e.g. GB, DE, ISO. NOT NULL: a lead that cannot say where it "
                            "applies is not retrievable.")
    p_rcl.add_argument("--standard-name", required=True,
                       help="e.g. 'BS 8300-2:2018'. Keyed with --jurisdiction; restating "
                            "one standard per design parameter is refused, and so is a "
                            "name that differs from a held one only in case, spacing or "
                            "punctuation (see --distinct-from).")
    p_rcl.add_argument("--clause", help="R3's locator: clause/section/page, once retrieved")
    p_rcl.add_argument("--status", default="REFERENCE-ONLY",
                       help="Live vocabulary, derived from the table; not a list in this file")
    p_rcl.add_argument("--recovered-from")
    p_rcl.add_argument("--notes")
    p_rcl.add_argument("--distinct-from", type=int, action="append", default=None,
                       dest="distinct_from", metavar="LEAD_ID",
                       help="Repeatable. Admit a name that folds to the same key as this "
                            "held lead because they are genuinely different documents. "
                            "Requires --reason, which is appended to --notes.")
    p_rcl.add_argument("--reason",
                       help="Only with --distinct-from: why the near-identical names are "
                            "two documents.")
    p_rcl.add_argument("--session", required=True)
    p_rcl.add_argument("--dry-run", action="store_true")

    p_ucl = sub.add_parser("update-code-lead",
                           help="Move a code lead's status or clause, APPENDING a dated note "
                                "(R15: re-describe from the source)")
    p_ucl.add_argument("--lead-id", required=True, type=int)
    p_ucl.add_argument("--append-note", required=True, dest="append_note",
                       help="Appended as a dated UPDATED segment carrying any replaced "
                            "status or clause. The existing note is never rewritten.")
    p_ucl.add_argument("--status",
                       help="From the column's own CHECK; any move is allowed and ledgered")
    p_ucl.add_argument("--clause", help="R3's locator, replacing the held one")
    p_ucl.add_argument("--session", required=True)
    p_ucl.add_argument("--dry-run", action="store_true")

    p_cs = sub.add_parser("correct-source",
                          help="Rewrite bibliographic fields FROM THE LOGGED PAYLOAD")
    p_cs.add_argument("--ref-id", required=True)
    p_cs.add_argument("--field", action="append", required=True, dest="fields",
                      help="Repeatable. One of: authors, " +
                           "pub_title, volume, issue, article_number, pages, pub_year. "
                           "There is NO flag for the VALUE — it comes from the payload.")
    p_cs.add_argument("--log-session", required=True,
                      help="retrieval-log session holding the payload to read")
    p_cs.add_argument("--session", required=True)
    p_cs.add_argument("--dry-run", action="store_true")

    p_am = sub.add_parser("amend-search",
                          help="APPEND a dated correction to a logged search's findings_note")
    p_am.add_argument("--exec-id", required=True, type=int)
    p_am.add_argument("--append-note", required=True, dest="append_note",
                      help="Appended after a '|| CORRECTED <date>:' marker. The existing "
                           "note is never rewritten -- R8 makes this log append-only.")
    # ADDED 2026-09-18 (batch 18). R5 fires on a NON-ENGLISH search targeted as 'grey',
    # because treating non-English work as grey is the exact error R5 exists to stop:
    # non-indexation in PubMed/Scopus is an INDEXING fact, not an evidence-quality fact.
    # This batch made that error -- it targeted a Dutch 1981 research paper 'grey' because
    # the item has no DOI -- and then had no way to correct it, because the log is
    # append-only and amend-search could append only PROSE. A MISCLASSIFICATION THE GATE
    # READS IS NOT FIXED BY A SENTENCE THE GATE DOES NOT READ.
    #
    # Scoped to this one column on purpose: target_evidence_type classifies what was
    # SOUGHT, not what happened, so correcting it rewrites no history. The query text,
    # results_found and the findings note stay append-only, which is what R8 protects.
    p_am.add_argument("--set-target-evidence-type",
                      help="Correct a MISCLASSIFIED target_evidence_type. The replaced "
                           "value is appended to findings_note, so the correction is "
                           "itself logged rather than silent.")
    p_am.add_argument("--set-harm-finding", action="store_true",
                      help="Raise harm_finding 0 -> 1. R7 makes harm first-class, so a "
                           "search logged with the flag down that did surface harm has an "
                           "incomplete record. Only rises; lowering is refused.")
    # RC5/RC1 (DR-2026-09-26 5.2d). History, through writers only -- never hand SQL.
    p_am.add_argument("--set-origin",
                      choices=dbcore.schema_choices("search_executions", "origin"),
                      help="Correct a row's origin. --set-origin adversarial-pass "
                           "with no --set-origin-pass-id is accepted here for history "
                           "that predates adversarial_passes; --append-note must say "
                           "why no pass id exists.")
    p_am.add_argument("--clear-target", action="store_true",
                      help="NULL target_tier/target_evidence_type/target_scope together "
                           "(2026-09-27, DR-2026-09-26 5.2d). Required before --set-origin "
                           "can move a row off 'planned' when any of the three is set; "
                           "combine both flags in one call.")
    p_am.add_argument("--set-mined-ref-id",
                      help="NULL -> a value only; refuses a mining_direction of none "
                           "and a value already set.")
    p_am.add_argument("--set-origin-pass-id", type=int,
                      help="NULL -> a value only; requires origin=adversarial-pass "
                           "(pass --set-origin too, or it must already be set).")
    p_am.add_argument("--add-result-artefact", action="append",
                      dest="add_result_artefacts",
                      help="repeatable; same refusal as log-search --result-artefact "
                           "(RC1, DR-2026-09-26 2.2b), for a payload fetched after "
                           "logging or history never linked at the time.")
    p_am.add_argument("--session", required=True)
    p_am.add_argument("--dry-run", action="store_true")

    p_ag2 = sub.add_parser("amend-gap",
                           help="APPEND a dated correction to a gap's description")
    p_ag2.add_argument("--gap-id", required=True)
    p_ag2.add_argument("--append-note", required=True, dest="append_note",
                       help="Appended after a '|| CORRECTED <date>:' marker. close-gap "
                            "moves status only, and gaps has no closure-note column, so "
                            "this is the only way to correct a filed description.")
    p_ag2.add_argument("--session", required=True)
    p_ag2.add_argument("--dry-run", action="store_true")

    p_rca = sub.add_parser("reattribute-candidate",
                           help="Repoint a candidate at the search that surfaced it")
    p_rca.add_argument("--candidate-id", required=True, type=int)
    p_rca.add_argument("--exec-id", required=True, type=int,
                       help="The search that ACTUALLY surfaced it. Must already be "
                            "logged -- backfill it with log-search first if it was not.")
    p_rca.add_argument("--reason", required=True,
                       help="Why the original attribution was wrong. Carried into notes "
                            "with the old exec_id, so the move is itself on the record.")
    p_rca.add_argument("--surfaced-in",
                       help="RC1 (DR-2026-09-26 2.2d), same refusal as add-candidate. "
                            "NULL -> a value only; a value already set needs a new exec.")
    p_rca.add_argument("--surfaced-quote",
                       help="required only when the candidate's locator carries no "
                            "single DOI")
    p_rca.add_argument("--session", required=True)
    p_rca.add_argument("--dry-run", action="store_true")

    p_rap = sub.add_parser(
        "record-adversarial-pass",
        help="Record a completed antagonist pass and its findings block (RC4)")
    p_rap.add_argument("--subject-session", required=True,
                       help="Bare stem or .md form; the writer strips a trailing .md")
    p_rap.add_argument("--subject-commit", required=True,
                       help="The sha the reviewer read")
    p_rap.add_argument("--reviewer-transcript", required=True,
                       help="Tracked path under transcripts/")
    p_rap.add_argument("--author-transcript", required=True,
                       help="Tracked path under transcripts/; must differ from "
                            "--reviewer-transcript")
    p_rap.add_argument("--session", required=True)
    p_rap.add_argument("--dry-run", action="store_true")

    p_daf = sub.add_parser(
        "dispose-adversarial-finding",
        help="Set an adversarial finding's disposition (RC4)")
    p_daf.add_argument("--finding-id", required=True, type=int)
    p_daf.add_argument("--disposition", required=True,
                       choices=dbcore.schema_choices("adversarial_findings", "disposition"))
    p_daf.add_argument("--ref",
                       help="REPAIRED: a scripts/migrations/data_*.sql path. OWNER-RULED: "
                            "references/project-standards.md :: \"<verbatim quote>\", "
                            "occurring exactly once. Ignored for REJECTED/PROVISIONAL-DISPUTED, "
                            "which take --reason instead.")
    p_daf.add_argument("--reason",
                       help="Required for REJECTED and PROVISIONAL-DISPUTED.")
    p_daf.add_argument("--session", required=True)
    p_daf.add_argument("--dry-run", action="store_true")

    p_cap = sub.add_parser(
        "close-adversarial-pass",
        help="Close a pass once every lens is covered and at least one row SURVIVED (RC4)",
        description="Close a pass once every lens is covered and at least one row "
                    "SURVIVED (RC4). Do NOT use it on pass 1: the owner ruling of "
                    "2026-09-27 (second; references/project-standards.md, ACTION (2)) "
                    "holds pass 1 OPEN. Pass 2 was left open by its session "
                    "(sessions/session_2026-09-28-research-batch-21-selection.md); the "
                    "process-gap plan the owner approved on 2026-10-01 says not to close "
                    "it, citing that ruling, which names only pass 1. Nothing refuses "
                    "either; the operator is the gate.")
    p_cap.add_argument("--pass-id", required=True, type=int)
    p_cap.add_argument("--session", required=True)
    p_cap.add_argument("--dry-run", action="store_true")

    p_rc = sub.add_parser("resolve-candidate",
                          help="Close a staged candidate, re-describing it from the source (R15)")
    p_rc.add_argument("--candidate-id", required=True, type=int)
    p_rc.add_argument("--disposition", required=True,
                      help="Live vocabulary, read from the column's own CHECK")
    p_rc.add_argument("--redescription", required=True,
                      help="What the SOURCE says, now that it has been read. Appended "
                           "after a RESOLVED marker; the staged hypothesis is kept.")
    p_rc.add_argument("--admitted-ref-id", dest="admitted_ref_id",
                      help="Required when --disposition ADMITTED")
    p_rc.add_argument("--suggested-slug", dest="suggested_slug",
                      help="REQUIRED with --disposition REHOME, refused otherwise: the slug "
                           "the candidate belongs under. Must be a filable (not MERGED) "
                           "slug other than the one it was found under; the replaced value "
                           "is recorded in the RESOLVED line.")
    p_rc.add_argument("--clear-suggested-slug", dest="clear_suggested_slug",
                      action="store_true",
                      help="Empty a stale suggested_slug (not with REHOME). The cleared "
                           "value is recorded in the RESOLVED line.")
    p_rc.add_argument("--session", required=True)
    p_rc.add_argument("--dry-run", action="store_true")

    p_la = sub.add_parser("link-admission",
                          help="Record that an EXISTING search admitted a source -- only "
                               "when a resolved candidate already records both ends")
    p_la.add_argument("--exec-id", required=True, type=int)
    p_la.add_argument("--ref-id", required=True)
    p_la.add_argument("--reason", required=True,
                      help="Why the edge was not written when the search was logged. "
                           "Appended to the search's findings_note.")
    p_la.add_argument("--session", required=True)
    p_la.add_argument("--dry-run", action="store_true")

    p_ula = sub.add_parser("unlink-admission",
                           help="Remove a WRONG admission edge (the corrective half of "
                                "link-admission); the removed edge is kept in the search's "
                                "findings_note. Capture with emit_batch_sql.py "
                                "--allow-delete search_admissions")
    p_ula.add_argument("--exec-id", required=True, type=int)
    p_ula.add_argument("--ref-id", required=True)
    p_ula.add_argument("--reason", required=True,
                       help="Why the edge is wrong. Appended to the search's findings_note.")
    p_ula.add_argument("--session", required=True)
    p_ula.add_argument("--dry-run", action="store_true")

    p_apm = sub.add_parser("amend-population-match",
                           help="Re-grade an R13 match in place (a ruling, not a dissent -- "
                                "a dissent is a second add-population-match row)")
    p_apm.add_argument("--match-id", required=True)
    p_apm.add_argument("--match-grade", required=True,
                       help="Live vocabulary, read from the column's own CHECK")
    p_apm.add_argument("--reason", required=True,
                       help="Appended to mismatch_note with the grade it replaces")
    p_apm.add_argument("--session", required=True)
    p_apm.add_argument("--dry-run", action="store_true")

    p_amt = sub.add_parser("amend-term",
                           help="Replace a term's definition or scope_note, recording the "
                                "text it replaces (canonical_en is not amendable)")
    p_amt.add_argument("--term-id", required=True)
    p_amt.add_argument("--field", required=True, choices=list(_AMENDABLE_TERM_FIELDS))
    p_amt.add_argument("--replacement", required=True)
    p_amt.add_argument("--reason", required=True)
    p_amt.add_argument("--session", required=True)
    p_amt.add_argument("--dry-run", action="store_true")

    p_ams = sub.add_parser("amend-source",
                           help="Correct a JUDGEMENT field on an evidence row, recording what was replaced")
    p_ams.add_argument("--ref-id", required=True)
    p_ams.add_argument("--field", required=True,
                       help="A judgement field, not a bibliographic one. Bibliographic "
                            "fields belong to correct-source and are refused here.")
    p_ams.add_argument("--replacement", required=True)
    p_ams.add_argument("--reason", required=True,
                       help="Why the previous text was wrong. Recorded in "
                            "metadata_integrity_detail with the replaced text.")
    p_ams.add_argument("--tier", type=int, default=None,
                       help="With --field scope, required when the new scope derives a "
                            "different tier; with --field evidence_type, optional. Either "
                            "way it must equal the one value the ratified ladder "
                            "produces, and moves in the same statement. The tier is "
                            "never set on its own.")
    p_ams.add_argument("--scope", default=None,
                       help="Only with --field evidence_type: the scope the new tier is "
                            "derived from. Required when the new type spans more than one "
                            "tier; derived when it admits exactly one.")
    p_ams.add_argument("--co1-provenance", default=None,
                       help="Only with --field evidence_type --replacement co1, and "
                            "required there: the D-0178 warrant naming the co-production. "
                            "A move OFF co1 keeps the old warrant in the ledger and NULLs "
                            "the column.")
    p_ams.add_argument("--co1-source-type", default=None,
                       help="Only with --field evidence_type --replacement co1, and "
                            "required there: a member of schemas.enums.Co1SourceType. "
                            "grain_for grades a Co-1 source's grain from it.")
    p_ams.add_argument("--session", required=True)
    p_ams.add_argument("--dry-run", action="store_true")

    p_lss = sub.add_parser(
        "link-source-slug",
        help="Cross-file an ADMITTED source to an ADDITIONAL slug (R9)")
    p_lss.add_argument("--ref-id", required=True)
    p_lss.add_argument("--slug", required=True,
                       help="Target slug. Vocabulary is the slugs table's own.")
    p_lss.add_argument("--rationale", required=True,
                       help="WHICH CLAIM of this source bears on THIS slug. The "
                            "link is a judgement and the warrant is stored with it; "
                            "a link with no rationale cannot be told from a mis-file.")
    p_lss.add_argument("--local-ref-id",
                       help="The per-slug label. Optional: DERIVED from the slug's own "
                            "scheme when omitted. Give it where derivation refuses (a "
                            "slug whose labels mix schemes, GAP-013). A label another "
                            "ref_id holds on the slug is refused.")
    p_lss.add_argument("--session", required=True)
    p_lss.add_argument("--dry-run", action="store_true")

    p_sps = sub.add_parser(
        "supersede-source",
        help="Mark an admitted source SUPERSEDED BY another (a mirror, a DOI-less "
             "re-entry). Neither row is deleted; dependents are reported, not moved.")
    p_sps.add_argument("--ref-id", required=True, help="The source that stops counting")
    p_sps.add_argument("--by", required=True, help="The admitted source that replaces it")
    p_sps.add_argument("--reason", required=True,
                       help="Why these are one source. Appended to the superseded row's "
                            "notes as a dated SUPERSEDED line.")
    p_sps.add_argument("--session", required=True)
    p_sps.add_argument("--dry-run", action="store_true")

    p_ul = sub.add_parser("update-locator", help="Move a lead's status in the clue store")
    p_ul.add_argument("--ref-id", required=True)
    p_ul.add_argument("--status", required=True,
                      help="Live vocabulary, read from the column's own CHECK")
    p_ul.add_argument("--reason",
                      help="REQUIRED for SCREENED-OUT: why this lead was worked and "
                           "judged unacceptable. The judgement is what the work bought; "
                           "a lead dismissed with no record of why is indistinguishable "
                           "from one nobody examined.")
    p_ul.add_argument("--session", required=True)
    p_ul.add_argument("--dry-run", action="store_true")

    # retire-specification — the supersede path the owner ruled on 2026-09-16.
    p_rs = sub.add_parser("retire-specification",
                          help="Retire a determination in place so its cell can be determined again")
    p_rs.add_argument("--specification-id", required=True, type=int)
    p_rs.add_argument("--reason",
                      help="REQUIRED to retire: why this determination no longer stands. "
                           "The trigger on the table refuses without it.")
    p_rs.add_argument("--superseded-by", type=int,
                      help="The specification that replaced it. May be supplied on a "
                           "LATER call, once the replacement exists — which is the real "
                           "order of events: retire, re-determine, then link.")
    p_rs.add_argument("--session", required=True)
    p_rs.add_argument("--dry-run", action="store_true")

    p_obs = sub.add_parser("observe-term",
                           help="Record that a source USES a phrase (evidence stage, D-0173)")
    p_obs.add_argument("--ref-id", required=True)
    p_obs.add_argument("--surface-form", required=True,
                       help="The phrase AS THE SOURCE WRITES IT. Not normalised, not "
                            "translated, not mapped to one of our terms.")
    p_obs.add_argument("--language", default="EN",
                       help="The language the phrase APPEARS IN, which need not be the "
                            "source's own language")
    p_obs.add_argument("--locator", help="R3: where in the source it appears")
    p_obs.add_argument("--context-quote",
                       help="Enough surrounding text that judgment can adjudicate "
                            "without re-retrieving the source")
    p_obs.add_argument("--notes")
    p_obs.add_argument("--session", required=True)
    p_obs.add_argument("--dry-run", action="store_true")

    # add-term — the writer NAMES-NEW needs. See insert_term for why the term and its
    # adjudication land together.
    p_at = sub.add_parser("add-term",
                          help="Mint a term for a NEW concept and adjudicate it NAMES-NEW")
    p_at.add_argument("--from-observation", dest="from_observation", type=int, required=True,
                      help="observed_terms.observation_id the term is minted FROM")
    p_at.add_argument("--canonical-en", dest="canonical_en", required=True,
                      help="the parameter's name — never a value, never a comparator")
    p_at.add_argument("--rationale", required=True,
                      help="why this phrase names a concept we did not hold")
    p_at.add_argument("--definition")
    p_at.add_argument("--domain")
    p_at.add_argument("--scope-note", dest="scope_note")
    p_at.add_argument("--session", required=True)
    p_at.add_argument("--dry-run", action="store_true")

    # add-parameter — the writer base_parameters shipped without. See insert_parameter
    # for its refusals and for why --status/--merged-into are deliberately absent.
    p_spd = sub.add_parser(
        "set-parameter-direction",
        help="Record which way is better for a disabled person on this parameter "
             "(the most-accommodating rule, owner directive 2026-07-21)")
    p_spd.add_argument("--parameter-id", type=int, required=True)
    p_spd.add_argument("--direction", required=True,
                       choices=dbcore.schema_choices("base_parameters",
                                                     "accessibility_direction"),
                       help="higher_is_better (widest minimum corridor) / "
                            "lower_is_better (lowest maximum threshold height, gentlest "
                            "maximum ramp slope) / contested (population-contested: no "
                            "single value is anchored, DR-2026-07-21 section 5)")
    p_spd.add_argument("--rationale", required=True,
                       help="WHY, for a disabled person. Required by the schema too.")
    p_spd.add_argument("--session", required=True)
    p_spd.add_argument("--dry-run", action="store_true")

    p_ap = sub.add_parser("add-parameter",
                          help="Promote an adjudicated term into base_parameters "
                               "(THE SUBJECT of a determination)")
    p_ap.add_argument("--term-id", dest="term_id", required=True,
                      help="terms.term_id — must carry a NAMES-NEW/NAMES-EXISTING adjudication")
    p_ap.add_argument("--notes")
    p_ap.add_argument("--session", required=True)
    p_ap.add_argument("--dry-run", action="store_true")

    # decline-parameter — the other answer to "is this term a parameter?" (migration 101).
    # See decline_parameter for its refusals and for why there is no un-decline verb.
    p_dp = sub.add_parser("decline-parameter",
                          help="Record that a term is NOT a design parameter, and why "
                               "(parameter_declinations)")
    p_dp.add_argument("--term-id", dest="term_id", required=True,
                      help="terms.term_id being declined — must exist and must not "
                           "already be a parameter")
    p_dp.add_argument("--reason", required=True,
                      help="WHY this term is not a quantity under determination (an "
                           "element, a lens term, a method). Required: a declination that "
                           "cannot say why cannot be contested.")
    p_dp.add_argument("--session", required=True)
    p_dp.add_argument("--dry-run", action="store_true")

    # add-population-icf-link / raise-determination-gate / resolve-determination-gate —
    # the writers migration 080's two tables shipped without. See the functions for the
    # refusals, and for the two that are DELIBERATELY ABSENT (a second link for the same
    # population under a different mechanism, and a resolved-on-creation gate).
    # add-icf-code / set-icf-title — the writers `base_icf` needs to grow after migration
    # 081 seeded it. See the functions for the refusals, and for why a title may never
    # arrive without a source.
    p_icf = sub.add_parser(
        "add-icf-code",
        help="Mint one ICF code into base_icf — the registry the ICF lens points at")
    p_icf.add_argument("--icf-code", dest="icf_code", required=True,
                       help="b/d/e/s + digits, optionally a range (d450, b1342, "
                            "d310–d329). `component` and `is_range` are DERIVED from it")
    p_icf.add_argument("--title", help="the classification's own wording. Needs a source")
    p_icf.add_argument("--title-source", dest="title_source",
                       help="the document stating the title — weaker than a payload, and "
                            "meant to read as weaker")
    p_icf.add_argument("--title-payload", dest="title_payload",
                       help="path under retrieval-log/ whose BYTES contain --title. ONLY "
                            "this makes the title verified rather than recorded")
    p_icf.add_argument("--notes")
    p_icf.add_argument("--session", required=True)
    p_icf.add_argument("--dry-run", action="store_true")

    p_sit = sub.add_parser(
        "set-icf-title",
        help="Name a seeded ICF code (GAP-ICF-TITLES); refuses to overwrite a title")
    p_sit.add_argument("--icf-code", dest="icf_code", required=True)
    p_sit.add_argument("--title", required=True)
    p_sit.add_argument("--title-source", dest="title_source")
    p_sit.add_argument("--title-payload", dest="title_payload",
                       help="path under retrieval-log/ whose BYTES contain --title")
    p_sit.add_argument("--session", required=True)
    p_sit.add_argument("--dry-run", action="store_true")

    p_pil = sub.add_parser(
        "add-population-icf-link",
        help="Map a population to an ICF activity it has a functional deficit in (H3)")
    p_pil.add_argument("--population", required=True,
                       help="populations.population_code — LIVE code, not a retired one")
    p_pil.add_argument("--icf-code", dest="icf_code", required=True,
                       help="d### or a range d###–d###. Free text by design: there is no "
                            "d-code registry to point at yet (080)")
    p_pil.add_argument("--mechanism", required=True,
                       help="HOW the deficit arises — biomechanical, sensory, autonomic, "
                            "cognitive. The same population may reach one code by two "
                            "mechanisms and both are real rows")
    p_pil.add_argument("--mapping-confidence", dest="mapping_confidence", required=True,
                       choices=dbcore.schema_choices("population_icf_links",
                                                     "mapping_confidence"))
    p_pil.add_argument("--provenance", required=True,
                       help="WHERE this row came from: a ref_id, or the promotion that "
                            "produced it. A mapping with no provenance is skill prose "
                            "in a table")
    p_pil.add_argument("--notes")
    p_pil.add_argument("--session", required=True)
    p_pil.add_argument("--dry-run", action="store_true")

    p_gate = sub.add_parser(
        "raise-determination-gate",
        help="Raise an H4 gate: cap a cell at provisional until it is resolved")
    p_gate.add_argument("--parameter-id", dest="parameter_id", type=int, required=True)
    p_gate.add_argument("--identity",
                        help="populations.population_code. OMIT to gate every lens on "
                             "this parameter — what an audit that does not yet know "
                             "which cells exist should do")
    p_gate.add_argument("--verdict", required=True,
                        choices=dbcore.schema_choices("determination_gates", "verdict"))
    p_gate.add_argument("--trigger-ref-id", dest="trigger_ref_id",
                        help="the source that raised it. Its tier and evidence_type are "
                             "READ from it; passing them too is refused")
    p_gate.add_argument("--trigger-tier", dest="trigger_tier", type=int,
                        help="required ONLY without --trigger-ref-id: an audit-raised "
                             "gate has no source, so the strength is asserted")
    p_gate.add_argument("--trigger-evidence-type", dest="trigger_evidence_type",
                        help="required ONLY without --trigger-ref-id")
    p_gate.add_argument("--detail", required=True, help="WHAT was found")
    p_gate.add_argument("--session", required=True)
    p_gate.add_argument("--dry-run", action="store_true")

    p_rg = sub.add_parser(
        "resolve-determination-gate",
        help="Close an H4 gate by the named path, with the rationale the schema requires")
    p_rg.add_argument("--gate-id", dest="gate_id", type=int, required=True)
    p_rg.add_argument("--rationale", required=True,
                      help="the adjudication. A gate released with no stated reason is a "
                           "cell let through by nobody")
    p_rg.add_argument("--session", required=True)
    p_rg.add_argument("--dry-run", action="store_true")

    # add-medical — the writer base_taxonomy_medical shipped without, and went on
    # shipping without for the two weeks between migration 065 creating the table and
    # 074 giving it something to point with. See insert_medical for the refusals.
    p_md = sub.add_parser("add-medical",
                          help="Mint a medical-lens row and at least one crossing "
                               "(the FOURTH lens, D-0170)")
    p_md.add_argument("--code", required=True, help="MD-<UPPER>, e.g. MD-AUTISM")
    p_md.add_argument("--display-name", dest="display_name", required=True,
                      help="the project's OWN name for the concept — not copied prose")
    p_md.add_argument("--description", help="the project's OWN definition")
    p_md.add_argument("--icd11", required=True,
                      help="comma list of ICD-11 codes this ANCHORS to. A bare code is a "
                           "fact; it is a pointer, not borrowed text (rule 5)")
    p_md.add_argument("--icd11-payload", dest="icd11_payload",
                      help="path under retrieval-log/ whose bytes CONTAIN every --icd11 "
                           "code. ONLY this sets icd11_verified_at; absent means NULL, "
                           "and NULL means not verified")
    p_md.add_argument("--identity", help="populations.population_code to cross to")
    p_md.add_argument("--relationship", choices=dbcore.schema_choices("identity_medical_map", "relationship"),
                      help="required with --identity")
    p_md.add_argument("--icf", help="axes.axis_code to cross to")
    p_md.add_argument("--role", choices=dbcore.schema_choices("icf_medical_map", "role"),
                      help="required with --icf. No ALIAS: a diagnosis is never an alias "
                           "of a functional demand (074)")
    p_md.add_argument("--mapping-confidence", dest="mapping_confidence",
                      choices=dbcore.schema_choices("icf_medical_map", "mapping_confidence"),
                      help="required with --icf; functional-taxonomy §3.2")
    p_md.add_argument("--note")
    p_md.add_argument("--session", required=True)
    p_md.add_argument("--dry-run", action="store_true")

    # add-extraction — the writer source_value_extractions shipped without. See
    # insert_extraction for the refusals, and for the three that are DELIBERATELY
    # ABSENT (uniqueness on (ref_id, parameter_id), a value-directness grade, and
    # --promoted-to-rdc-id).
    p_ax = sub.add_parser("add-extraction",
                          help="Record what one source asserts for one parameter "
                               "(the JUDGMENT item, D-0168)")
    p_ax.add_argument("--ref-id", required=True, help="evidence_sources.ref_id — the source read")
    p_ax.add_argument("--slug", required=True, help="the slug the reading happened under")
    p_ax.add_argument("--parameter-id", dest="parameter_id", type=int, required=True,
                      help="base_parameters.parameter_id — THE SUBJECT (owner 2026-08-26)")
    # The four lenses. At least one is required (D-0182); the CLI names them by lens
    # rather than by column so the operator is choosing a LENS, not filling a field.
    p_ax.add_argument("--identity", help="populations.population_code")
    p_ax.add_argument("--icf", help="base_icf.icf_code — a real ICF b/d code")
    p_ax.add_argument("--needs", help="access_needs.need_code")
    p_ax.add_argument("--medical", help="base_taxonomy_medical.medical_code")
    p_ax.add_argument("--claim-type", dest="claim_type", required=True,
                      help="Live vocabulary, read from the column's own CHECK. "
                           "'absent' records that the source asserts NO value — which is "
                           "evidence, and takes no --claimed-value.")
    p_ax.add_argument("--claimed-value", dest="claimed_value")
    p_ax.add_argument("--claimed-unit", dest="claimed_unit")
    # REQUIRED, and this flag is the ONLY thing holding the verbatim guarantee.
    # Before migration 073 `parameter` was NOT NULL, so every row carried at least
    # the source's own phrase for what it measures. 073 retired that column (its
    # verbatim job belongs to observed_terms.surface_form) and left `claim_text`,
    # `source_section` and all 16 `loc_*` columns NULLABLE — so a happy-path row
    # could carry ZERO verbatim from the source it claims to have read. The schema
    # cannot be tightened without a compensating migration; the writer can, in one
    # line, and this is it. The guarantee is therefore the CLI's, not the schema's:
    # a row written by any other path can still carry none.
    p_ax.add_argument("--verbatim-exempt", dest="verbatim_exempt",
                      help="Reason this --claim-text cannot be verified against a "
                           "persisted artefact (a clause read from a standards PDF that "
                           "was never retrieved as JSON/XML, say). LEDGERED onto the "
                           "row's notes, and REFUSED if the text would have verified.")
    p_ax.add_argument("--claim-text", dest="claim_text", required=True,
                      help="REQUIRED. The source's exact phrasing of the claim, "
                           "verbatim. This is the row's only guaranteed verbatim "
                           "anchor — without it an extraction asserts a value with "
                           "nothing of the source's own words behind it. For "
                           "--claim-type absent, quote the passage that SHOULD have "
                           "carried the value and does not.")
    p_ax.add_argument("--source-section", dest="source_section")
    p_ax.add_argument("--jurisdiction")
    p_ax.add_argument("--setting")
    p_ax.add_argument("--extraction-method", dest="extraction_method", required=True,
                      help="Live vocabulary, read from the column's own CHECK")
    p_ax.add_argument("--extraction-status", dest="extraction_status",
                      help="Live vocabulary, read from the column's own CHECK "
                           "(the column's own DEFAULT applies when omitted)")
    # Value genealogy (DR-2026-07-13 H1) — what v_value_independence counts over.
    p_ax.add_argument("--root-id", dest="root_id")
    p_ax.add_argument("--root-type", dest="root_type",
                      help="Live vocabulary, read from the column's own CHECK")
    p_ax.add_argument("--root-ref-id", dest="root_ref_id",
                      help="evidence_sources.ref_id of the root the value traces to")
    p_ax.add_argument("--echo-of", dest="echo_of")
    p_ax.add_argument("--measurement-paradigm", dest="measurement_paradigm",
                      help="Live vocabulary, read from the column's own CHECK")
    p_ax.add_argument("--device-class", dest="device_class",
                      help="Live vocabulary, read from the column's own CHECK")
    p_ax.add_argument("--root-population-note", dest="root_population_note")
    p_ax.add_argument("--root-classification-basis", dest="root_classification_basis")
    p_ax.add_argument("--contested", type=int, choices=[0, 1])
    p_ax.add_argument("--file-anchor", dest="file_anchor")
    # Pinpoint locator (migration 053). One flag per column, generated rather than
    # typed out twice: the columns ARE the list, and duplicating them here would be a
    # second home for the locator hierarchy.
    p_ax.add_argument("--locator-scheme", dest="locator_scheme",
                      help="which family's naming applies (ISO clause vs ADA section)")
    for _lvl in ("division", "part", "section", "subsection", "paragraph",
                 "clause", "subclause"):
        p_ax.add_argument(f"--loc-{_lvl}", dest=f"loc_{_lvl}")
        p_ax.add_argument(f"--loc-{_lvl}-end", dest=f"loc_{_lvl}_end",
                          help=f"end of a span, e.g. ADA 2010 §604-608")
    p_ax.add_argument("--loc-note", dest="loc_note")
    p_ax.add_argument("--notes")
    # figure_role / comparator (migration 075) and the comparator junction they imply
    # a row into -- extraction_relations. See insert_extraction and _write_relation_edge
    # for the refusals; this parser only names the shape.
    p_ax.add_argument("--figure-role", dest="figure_role", required=True,
                      help="REQUIRED. Live vocabulary, read from "
                           "source_value_extractions.figure_role's own CHECK "
                           "('claim'/'finding'/'condition'/'derived'). A value with "
                           "no role reads as a claim, and a tested slope read as a "
                           "claim is how '1:20, 1:16, 1:12, 1:8' became a range no "
                           "source ever asserted (extraction_id 1).")
    p_ax.add_argument("--comparator",
                      help="Live vocabulary, read from the column's own CHECK "
                           "('='/'<'/'<='/'>'/'>='/'between'/'approx'). Omit when "
                           "the figure carries no stated arithmetic relation.")
    p_ax.add_argument("--relation", action="append", dest="relations", required=True,
                      help="REQUIRED, repeatable -- one per comparator edge, aligned "
                           "by position with --to-extraction/--to-label/--to-kind/"
                           "--stated/--quote/--input-role/--cross-source below. Pass "
                           "the literal 'none' -- alone, exactly once, no other "
                           "relation flag -- to say the source states its figure "
                           "ABSOLUTELY. Silence is not the same claim: five of five "
                           "corridor-width sources in the live corpus state theirs "
                           "against a reference they name or invoke. Otherwise live "
                           "vocabulary, read from extraction_relations.relation's own "
                           "CHECK.")
    p_ax.add_argument("--to-extraction", action="append", dest="to_extractions",
                      default=[], help="Repeatable, aligned by position with "
                           "--relation. A row this project already holds. Pass '-' "
                           "for an edge that uses --to-label instead.")
    p_ax.add_argument("--to-label", action="append", dest="to_labels", default=[],
                      help="Repeatable, aligned by position with --relation. Prose "
                           "naming a referent this project has not captured as a "
                           "row. Pass '-' for an edge that uses --to-extraction "
                           "instead.")
    p_ax.add_argument("--to-kind", action="append", dest="to_kinds", default=[],
                      help="Repeatable, aligned by position with --relation. "
                           "Required alongside --to-label. Live vocabulary from the "
                           "column's own CHECK ('standard'/'own_sample'/"
                           "'prior_source'/'unnamed').")
    p_ax.add_argument("--stated", action="append", dest="stateds", default=[],
                      help="Repeatable, aligned by position with --relation. Live "
                           "vocabulary ('named'/'unnamed'/'inferred').")
    p_ax.add_argument("--quote", action="append", dest="quotes", default=[],
                      help="Repeatable, aligned by position with --relation. The "
                           "source's own words for the comparison -- must occur "
                           "byte-for-byte in a persisted retrieval artefact "
                           "(CLAUDE.md 5(c)); a quote from memory is refused.")
    p_ax.add_argument("--input-role", action="append", dest="input_roles", default=[],
                      help="Repeatable, aligned by position with --relation. "
                           "Required iff the paired --relation is derived_from "
                           "('base'/'delta'/'factor').")
    p_ax.add_argument("--cross-source", action="append", dest="cross_sources",
                      default=[], help="Repeatable, aligned by position with "
                           "--relation. A REASON, required when a condition_on/"
                           "derived_from edge's --to-extraction was extracted from a "
                           "DIFFERENT --ref-id than this row: a condition drawn from "
                           "another document is a synthesis act, made explicit here.")
    p_ax.add_argument("--session", required=True)
    p_ax.add_argument("--dry-run", action="store_true")

    # relate-extraction -- add ONE comparator edge to an EXISTING row (migration 075).
    p_rx = sub.add_parser("relate-extraction",
                          help="Add a comparator edge to an existing extraction row, "
                               "or repoint a label edge onto a newly-extracted row")
    p_rx.add_argument("--from", dest="from_extraction", type=int, required=True,
                      help="source_value_extractions.extraction_id -- the figure "
                           "this edge qualifies")
    p_rx.add_argument("--relation", required=True,
                      help="Live vocabulary, read from extraction_relations."
                           "relation's own CHECK")
    p_rx.add_argument("--to-extraction", dest="to_extraction", type=int,
                      help="A row this project already holds")
    p_rx.add_argument("--to-label", dest="to_label",
                      help="Prose naming a referent this project has not captured "
                           "as a row")
    p_rx.add_argument("--to-kind", dest="to_kind",
                      help="Required alongside --to-label")
    p_rx.add_argument("--stated", help="'named'/'unnamed'/'inferred'. Required "
                      "unless --repoint")
    p_rx.add_argument("--quote", help="The source's own words, verbatim -- must "
                      "occur byte-for-byte in a persisted retrieval artefact. "
                      "Required unless --repoint")
    p_rx.add_argument("--input-role", dest="input_role",
                      help="Required iff --relation is derived_from")
    p_rx.add_argument("--cross-source", dest="cross_source_reason",
                      help="A reason, required when --relation is condition_on/"
                           "derived_from and --to-extraction was extracted from a "
                           "DIFFERENT ref_id than --from")
    p_rx.add_argument("--notes")
    p_rx.add_argument("--repoint", action="store_true",
                      help="Given an existing --from/--relation LABEL edge, NULL "
                           "the label and kind, point it at --to-extraction instead, "
                           "and ledger the old label into notes. How an 'ADAAG' "
                           "label edge becomes a real row pointer once ADA 405 is "
                           "admitted and extracted.")
    p_rx.add_argument("--old-label", dest="old_label",
                      help="Disambiguates --repoint when --from/--relation matches "
                           "more than one label edge")
    p_rx.add_argument("--session", required=True)
    p_rx.add_argument("--dry-run", action="store_true")

    # amend-extraction -- figure_role / comparator ONLY. Everything else is a second
    # row and a contest (D-0168), not an overwrite.
    p_amx = sub.add_parser("amend-extraction",
                           help="Change figure_role or comparator on an existing "
                                "row, with a reason ledgered into notes")
    p_amx.add_argument("--extraction-id", dest="extraction_id", type=int,
                       required=True)
    # DERIVED from _AMENDABLE_SVE_FIELDS, not retyped. This list said
    # ["figure_role", "comparator"] and went stale the moment the constant grew,
    # which is rule 8's "twelve argparse choices= lists that duplicate a column's
    # CHECK" in miniature -- one list fewer.
    p_amx.add_argument("--field", required=True,
                       choices=sorted(_AMENDABLE_SVE_FIELDS),
                       help="ONLY these two. A wrong claimed_value or claim_text is "
                            "a SECOND ROW and a contest (D-0168), not an overwrite.")
    p_amx.add_argument("--value", required=True)
    p_amx.add_argument("--reason", required=True,
                       help="Why. Appended to notes, never overwriting it.")
    p_amx.add_argument("--session", required=True)
    p_amx.add_argument("--dry-run", action="store_true")

    # derive-extraction -- a figure_role='derived' row, computed base+delta, plus
    # the two derived_from edges v_derived_figure_check re-verifies it against.
    p_dx = sub.add_parser("derive-extraction",
                          help="Write a computed (base+delta) extraction and the "
                               "derived_from edges that prove it")
    p_dx.add_argument("--ref-id", required=True)
    p_dx.add_argument("--slug", required=True)
    p_dx.add_argument("--parameter-id", dest="parameter_id", type=int, required=True)
    p_dx.add_argument("--identity")
    p_dx.add_argument("--icf")
    p_dx.add_argument("--needs")
    p_dx.add_argument("--medical")
    p_dx.add_argument("--base", type=int, required=True,
                      help="extraction_id of the base figure")
    p_dx.add_argument("--delta", type=int, required=True,
                      help="extraction_id of the delta figure")
    p_dx.add_argument("--claimed-value", dest="claimed_value",
                      help="Omit to compute base + delta")
    p_dx.add_argument("--claimed-unit", dest="claimed_unit",
                      help="Overrides the base figure's unit -- requires "
                           "--conversion-note")
    p_dx.add_argument("--comparator")
    p_dx.add_argument("--conversion-note", dest="conversion_note",
                      help="Required when --claimed-unit overrides the base/delta "
                           "unit")
    p_dx.add_argument("--claim-text", dest="claim_text", required=True)
    p_dx.add_argument("--session", required=True)
    p_dx.add_argument("--dry-run", action="store_true")

    p_adj = sub.add_parser("adjudicate-term",
                           help="Decide whether an observed phrase names our concept "
                                "(judgment stage, D-0173)")
    p_adj.add_argument("--observation-id", required=True, type=int)
    p_adj.add_argument("--outcome", required=True,
                       help="Live vocabulary, read from the column's own CHECK")
    p_adj.add_argument("--term-id",
                       help="Required for NAMES-EXISTING and NAMES-NEW; refused otherwise")
    p_adj.add_argument("--rationale", required=True,
                       help="Why. An adjudication that cannot be contested is not one.")
    p_adj.add_argument("--session", required=True)
    p_adj.add_argument("--dry-run", action="store_true")

    p_loc = sub.add_parser("add-locator", help="Write a lead into the clue store")
    p_loc.add_argument("--ref-id", required=True)
    for f in ("doi", "pmid", "pmcid", "isbn", "issn", "url", "standard-number",
              "title", "authors", "notes", "used-in-bpcs"):
        p_loc.add_argument("--" + f)
    p_loc.add_argument("--pub-year", type=int)
    # TEXT, not int. The column is `tier_claimed TEXT` and its live values include
    # 'Co-1/3', 'Co-2', 'Tier 1', 'INT', 'CA' and 'DE' -- a tier CLAIM is what a
    # lead asserts about itself, not a validated tier. `type=int` made the writer
    # refuse every Co-1 and Co-2 lead, which is the one class CRPD Art 4.3 makes
    # co-primary with T1, and the class this project most needs its clue store to
    # carry. Found 2026-09-02 parking six retracted identities, three of them Co-1.
    p_loc.add_argument("--tier-claimed")
    p_loc.add_argument("--recovered-from", required=True)
    p_loc.add_argument("--status", required=True)
    p_loc.add_argument("--session", required=True)
    p_loc.add_argument("--dry-run", action="store_true")

    # next-id
    p_nid = sub.add_parser("next-id", help="Get next available ID")
    p_nid.add_argument("entity",
                       choices=["connections", "gaps", "terms", "conflicts", "ref"])

    # coverage
    p_cov = sub.add_parser("coverage", help="Check search coverage")
    p_cov.add_argument("--slug", required=True)

    # synonyms
    p_syn = sub.add_parser("synonyms", help="Get synonyms for item")
    p_syn.add_argument("--item", required=True)
    p_syn.add_argument("--language")

    # add-gap
    p_ag = sub.add_parser("add-gap", help="Insert a new gap record")
    p_ag.add_argument("--category", required=True)
    p_ag.add_argument("--priority", required=True, choices=dbcore.schema_choices("gaps", "priority"))
    p_ag.add_argument("--description", required=True)
    p_ag.add_argument("--session", required=True)
    p_ag.add_argument("--skill")
    p_ag.add_argument("--section")
    p_ag.add_argument("--dry-run", action="store_true")

    # close-gap
    p_cg = sub.add_parser("close-gap", help="Close a gap record")
    p_cg.add_argument("--gap-id", required=True)
    p_cg.add_argument("--status", required=True,
                      help="Must start with CLOSED (e.g. CLOSED-FIXED)")
    p_cg.add_argument("--session", required=True)
    p_cg.add_argument("--dry-run", action="store_true")

    # add-connection
    p_ac = sub.add_parser("add-connection", help="Insert a new connection record")
    p_ac.add_argument("--con-id", required=True)
    p_ac.add_argument("--status", default="PENDING")
    p_ac.add_argument("--confidence", required=True,
                      choices=dbcore.schema_choices("connections", "confidence"))
    p_ac.add_argument("--connection-type", required=True)
    p_ac.add_argument("--filed-in", required=True)
    p_ac.add_argument("--description", required=True)
    p_ac.add_argument("--source-skill", required=True)
    p_ac.add_argument("--targets", required=True,
                      help="JSON array of target strings e.g. [item:E-08]")
    p_ac.add_argument("--session", required=True)
    p_ac.add_argument("--dry-run", action="store_true")

    # update-connection
    p_uc = sub.add_parser("update-connection", help="Update connection status")
    p_uc.add_argument("--con-id", required=True)
    p_uc.add_argument("--status", required=True)
    p_uc.add_argument("--session", required=True)
    p_uc.add_argument("--dry-run", action="store_true")

    # unmined
    p_um = sub.add_parser("unmined", help="List unmined Tier 1-N sources")
    p_um.add_argument("--slug", help="Filter to specific slug")
    p_um.add_argument("--tier-max", type=int, default=3)

    # upsert-coverage
    p_ucov = sub.add_parser("upsert-coverage", help="Update search coverage for slug+jurisdiction")
    p_ucov.add_argument("--slug", required=True)
    p_ucov.add_argument("--jurisdiction", required=True)
    p_ucov.add_argument("--status", default="searched")
    p_ucov.add_argument("--co1-attempted", type=int, default=0)
    p_ucov.add_argument("--session", required=True)
    p_ucov.add_argument("--dry-run", action="store_true")

    # upsert-language
    p_ul = sub.add_parser("upsert-language", help="Update search language for slug")
    p_ul.add_argument("--slug", required=True)
    p_ul.add_argument("--language", required=True)
    p_ul.add_argument("--status", default="searched")
    p_ul.add_argument("--results-count", type=int, default=0)
    p_ul.add_argument("--session", required=True)
    p_ul.add_argument("--dry-run", action="store_true")

    # log-search — the successor to the two frozen grids above.
    p_ls = sub.add_parser(
        "log-search",
        help="Append one row to search_executions (replaces upsert-coverage/-language)")
    p_ls.add_argument("--prior-expectation", dest="prior_expectation",
                      help="What you expect this search to find, written BEFORE you run "
                           "it. DR-2026-05-09: logged in advance to expose confirmation "
                           "bias. This is the only moment it can honestly be recorded -- "
                           "a prior written after reading the results is a "
                           "rationalisation wearing the field that prevents one.")
    p_ls.add_argument("--slug", required=True)
    p_ls.add_argument("--language", required=True, help="ISO 639-1, uppercase (EN, FR)")
    p_ls.add_argument("--query-text", required=True,
                      help="the query VERBATIM (R8: log it before screening)")
    p_ls.add_argument("--engine", required=True, help="pubmed, crossref, web, ...")
    # Every choices= list below is copied from the STRICT table's own CHECK
    # constraints, verified against the DDL. The first draft of this command
    # invented `citation-chase` and `targeted` for --depth-method; the column
    # allows only scoping|systematic, so the very first citation-chase search a
    # session logged would have died on `CHECK constraint failed` — a write path
    # that is unexecutable on the day it replaces the one being closed.
    # A citation chase is `--mining-direction backward|forward|both`, which is
    # the column that already means it; the depth axis is scoping vs systematic.
    p_ls.add_argument("--depth-method", required=True,
                      choices=dbcore.schema_choices("search_executions", "depth_method"))
    p_ls.add_argument("--session", required=True)
    p_ls.add_argument("--jurisdiction", help="omit for a search not scoped to one")
    p_ls.add_argument("--target-tier", type=int,
                      choices=dbcore.schema_range("search_executions", "target_tier"))
    p_ls.add_argument("--target-evidence-type",
                      choices=dbcore.schema_choices("search_executions", "target_evidence_type"))
    p_ls.add_argument("--target-scope",
                      choices=dbcore.schema_choices("search_executions", "target_scope"))
    p_ls.add_argument("--terms-used",
                      help="JSON array of the aliases actually fired — the column "
                           "is json_valid-checked, and it is 0%% populated today, "
                           "so no logged search can yet show which terms it used")
    p_ls.add_argument("--mining-direction",
                      choices=dbcore.schema_choices("search_executions", "mining_direction"))
    p_ls.add_argument("--results-found", type=int, default=0)
    p_ls.add_argument("--results-screened", type=int, default=0)
    p_ls.add_argument("--results-admitted", type=int, default=0)
    p_ls.add_argument("--admitted-ref-id", action="append", dest="admitted_ref_ids",
                      help="repeatable; also written to the search_admissions junction")
    p_ls.add_argument("--saturation-signal", choices=dbcore.schema_choices("search_executions", "saturation_signal"))
    p_ls.add_argument("--findings-note")
    p_ls.add_argument("--harm-finding", type=int, default=0,
                      help="R7: failure/harm/inadequacy is first-class evidence")
    p_ls.add_argument("--deferred-reason",
                      help="a search DELIBERATELY not run. This is what makes "
                           "'not looked for' different from 'nothing found'.")
    p_ls.add_argument("--backfill", type=int, default=0,
                      help="1 = reconstructed after the fact, not logged as it happened")
    # RC5 (DR-2026-09-26 5.2c). `origin` is INITIATION (why the step ran);
    # `--mining-direction` above stays METHOD (how) -- orthogonal.
    p_ls.add_argument("--origin", default="planned",
                      choices=dbcore.schema_choices("search_executions", "origin"))
    p_ls.add_argument("--mined-ref-id",
                      help="the source this pass mined; required with a "
                           "--mining-direction other than none")
    p_ls.add_argument("--origin-pass-id", type=int,
                      help="required with --origin adversarial-pass")
    p_ls.add_argument("--result-artefact", action="append", dest="result_artefacts",
                      help="repeatable; retrieval-log/<session>/<file> path of a "
                           "payload this search returned (RC1, DR-2026-09-26 2.2b). "
                           "Refused unless the chain resolves to a fetched, 2xx "
                           "artefact this search's own query_text or mined_ref_id "
                           "identifies.")
    p_ls.add_argument("--dry-run", action="store_true")

    # update-bpc
    p_ubpc = sub.add_parser("update-bpc", help="Update bpc_metadata for a slug")
    p_ubpc.add_argument("--slug", required=True)
    p_ubpc.add_argument("--session", required=True)
    p_ubpc.add_argument("--citation-mining-complete", type=int, choices=[0, 1])
    p_ubpc.add_argument("--bpc-complete", type=int, choices=[0, 1])
    p_ubpc.add_argument("--search-complete", type=int, choices=[0, 1])
    p_ubpc.add_argument("--pico-complete", type=int, choices=[0, 1])
    p_ubpc.add_argument("--evidence-state")
    # DR-2026-05-24 supersession protocol
    p_ubpc.add_argument("--supersession-check-complete", type=int, choices=[0, 1],
                        help="DR-2026-05-24: set when all cited anchor sources have terminal supersession outcomes")
    p_ubpc.add_argument("--closure-definition-version", choices=dbcore.schema_choices("bpc_metadata", "closure_definition_version"),
                        help="DR-2026-05-24: v2 requires citation_mining_complete=1 AND supersession_check_complete=1")
    p_ubpc.add_argument("--dry-run", action="store_true")

    # add-source
    p_as = sub.add_parser("add-source", help="Insert an evidence source")
    p_as.add_argument("--ref-id", required=True)
    # AUTHORS ARE ROWS, NOT A STRING (migration 063). evidence_sources.author_display is
    # writer-retired; who wrote a source has one home, evidence_source_authors, and
    # v_evidence_authors renders it. Until 2026-08-24 this CLI could write the display
    # copy and could NOT write the rows at all — the documented filing path wrote the
    # derived form and left the source of truth empty. Both flags below write rows.
    p_as.add_argument("--author", action="append", metavar="LAST|GIVEN",
                      help="Repeatable, in byline order. 'Payne|Sarah R.' for a person, "
                           "'corp|World Health Organization' for a corporate author. "
                           "Preferred: it stores the given name, which --authors cannot.")
    p_as.add_argument("--authors", metavar='"Last I; Last I"',
                      help="Display form, parsed into author rows. Kept because every "
                           "skill and runbook writes it. Each part must be a surname "
                           "followed by initials; anything this cannot parse without "
                           "guessing is REFUSED rather than approximated.")
    # ADDED 2026-08-25 (Act 2): the three columns CLAUDE.md §4 named as unreachable,
    # which forced a hand-written companion UPDATE after every single admission.
    p_as.add_argument("--url")
    p_as.add_argument("--url-accessed")
    p_as.add_argument("--pages")
    p_as.add_argument("--doi-resolution-outcome",
                      choices=dbcore.schema_choices("evidence_sources",
                                                    "doi_resolution_outcome"),
                      help="Read from the column's own CHECK (rule 8), live since "
                           "migration 091")
    # ADDED 2026-09-18 (batch 18): the venue fields that make a REPORT citable.
    # A government report with no institution and no report number cannot be rendered
    # into a bibliography -- see the _ES_COLS note for how REF-01005 exposed this.
    # choices AND help both READ FROM THE COLUMN'S OWN CHECK (rule 8), as of migration
    # 089. Until then this was a free-text flag whose help string listed the vocabulary by
    # hand -- and listed it WRONG, advertising Crossref's `journal-article` where the
    # project's value is `journal_article`. A session copied the hyphen straight out of the
    # help, the writer accepted it because the column declared no CHECK, and a blocking
    # check caught it two steps later. Now argparse refuses it before the command runs and
    # `--help` cannot drift from the schema, because neither is written down here.
    p_as.add_argument("--source-type",
                      choices=dbcore.schema_choices("evidence_sources", "source_type"),
                      help="Live vocabulary, read from the column's own CHECK")
    p_as.add_argument("--institution", help="the PERFORMING organisation, as ERIC's INSTITUTION field and a report's own title page use the term; the sponsor goes in --publisher")
    p_as.add_argument("--report-number", help="e.g. HUD-PDR 397; the issuer's own number")
    p_as.add_argument("--series")
    p_as.add_argument("--series-number")
    p_as.add_argument("--publisher")
    p_as.add_argument("--publisher-location")
    p_as.add_argument("--book-title")
    p_as.add_argument("--grey-flag", type=int, choices=(0, 1),
                      help="1 for grey literature. evidence_type='grey' with grey_flag=0 "
                           "is the same fact disagreeing with itself across two columns")
    p_as.add_argument("--grey-reason", help="WHY it is grey: the venue, in a phrase")
    p_as.add_argument("--year", required=True, type=int)
    p_as.add_argument("--title", required=True)
    p_as.add_argument("--tier", required=True, type=int)
    p_as.add_argument("--doi")
    p_as.add_argument("--pmid")
    p_as.add_argument("--jurisdiction")
    p_as.add_argument("--evidence-type")
    # ADDED 2026-09-10. `scope` is the discriminator schemas/tier_derivation.py derives
    # the ratified tier FROM, and this CLI could say --tier and could not say --scope. So
    # every tier in the corpus was ASSERTED rather than derived: all 9 admitted sources
    # carry scope NULL, and adjudication_integrity.py reports 9 of 9 underivable. Only
    # `clinical` and `standard_eb` have a real choice; the other six types admit exactly
    # one scope, so it is filled in rather than demanded.
    p_as.add_argument("--scope",
                      help="clinical: high_control | lower_control. standard_eb: national | "
                           "international. Every other type takes 'intrinsic', which is "
                           "supplied automatically. The tier is CHECKED against it.")
    # ADDED 2026-09-02. All three columns were ALREADY in _ES_COLS, so
    # insert_evidence_source accepted them; only the CLI had no way to say them. The
    # cost was measured 2026-09-01: two Co-1 sources admitted with co1_provenance NULL,
    # which DR-2026-08-31 (D-0178) calls "unwarranted-pending" — on the one tier whose
    # entire warrant under CRPD Art 4.3 IS the co-production.
    p_as.add_argument("--co1-provenance",
                      help="HOW the co-production is evidenced — name the disabled people or "
                           "organisation. D-0178: 'published_corpus' says where it was PUBLISHED, "
                           "not that disabled people CO-PRODUCED it. Required for --evidence-type co1.")
    p_as.add_argument("--co1-source-type")
    # --prior-expectation was HERE and is gone (2026-09-03). I added it on 2026-09-02
    # reasoning that admission "is the only moment it can honestly be recorded". That was
    # wrong by one stage. add-source runs in the LOG action, AFTER the source is searched,
    # screened, retrieved and read; DR-2026-05-09 defines the field as what was expected
    # BEFORE searching. A flag here could only ever be satisfied by reconstruction, which
    # is the exact artefact the field exists to prevent. It now lives on `log-search`,
    # where the fact exists, and migration 069 gives search_executions the column.
    p_as.add_argument("--synthesis-attribution-required", type=int, choices=[0, 1])
    p_as.add_argument("--lang-detected", help="ISO 639-1 code for the source's actual publication language")
    p_as.add_argument("--lang-detection-method",
                      help="How --lang-detected was determined, e.g. 'native_title_verified', "
                           "'journal_family_inference', 'citing_document_language'")
    p_as.add_argument("--metadata-quality",
                      # COMPLETE-STATUTORY was missing and it is 333 of 863 rows
                      # (39% of the corpus) — the whole T4-T6 regulatory stratum.
                      # A session filing a standard or code via the documented
                      # path had to either mislabel it COMPLETE or omit the field.
                      choices=["COMPLETE", "COMPLETE-STATUTORY", "PMID-ONLY",
                               "GREY", "AUTHOR-TITLE-ONLY"],
                      help="REQUIRED in practice, not just schema — see adversarial-research skill. "
                           "COMPLETE if DOI/full metadata confirmed via CrossRef/PubMed/Semantic Scholar; "
                           "AUTHOR-TITLE-ONLY if only single-source (citing-document) attestation.")
    p_as.add_argument("--verification-method",
                      # 'direct-render' was missing here until 2026-09-13 even though
                      # evidence_sources.verification_method's own CHECK admits it
                      # (dbcore.check_values(con, "evidence_sources", "verification_method")
                      # returns all five) -- the schema is the authority (CLAUDE.md §4),
                      # so the CLI's list was the thing out of date, not the column.
                      choices=dbcore.schema_choices("evidence_sources", "verification_method"),
                      help="REQUIRED when --verification-status VERIFIED. How the "
                           "standing was established (D-0157).")
    p_as.add_argument("--verified-by-tool",
                      help="REQUIRED when --verification-method tool: which tool "
                           "(crossref, pubmed, semantic-scholar, ...). Invariant I4b.")
    p_as.add_argument("--verification-status",
                      # Read from the column, not restated. Migration 091 gave
                      # verification_status a CHECK, and derived_not_curated_audit went
                      # red on this literal within the same run -- the audit doing
                      # exactly its job: the moment a vocabulary gains a home in the
                      # schema, a hand-written copy of it becomes the second home rule 5
                      # forbids.
                      choices=dbcore.schema_choices("evidence_sources",
                                                    "verification_status"),
                      help="REQUIRED in practice. VERIFIED requires an independent connector/registry hit "
                           "(CrossRef, PubMed, Semantic Scholar, a second citing source). A source found only "
                           "in one citing document's bibliography, with no independent hit, is UNVERIFIED "
                           "with disposition OPEN, "
                           "not VERIFIED — do not upgrade it because the citing document looks authoritative.")
    p_as.add_argument("--slug", help="Link to slug. The slug and the label are resolved "
                                     "before anything is written; a refusal leaves no row.")
    p_as.add_argument("--local-ref-id",
                      help="Per-slug label (with --slug only). Optional: DERIVED from the "
                           "slug's own scheme when omitted. Give it where derivation "
                           "refuses (a slug whose labels mix schemes, GAP-013).")
    p_as.add_argument("--session", required=True)
    p_as.add_argument("--dry-run", action="store_true")

    # validate — RETIRED 2026-08-15 with scripts/validate_db.py. That script was
    # quarantined in the check registry (it queries doi_less_key, a column no
    # live table has) and superseded by scripts/tests/test_db_integrity.py.

    # ── CO-0009 Phase 1 Session 1b ─────────────────────────────────────────

    # add-conflict
    p_aconf = sub.add_parser("add-conflict", help="Insert a conflict record")
    p_aconf.add_argument("--conflict-id", help="CONF-NNNN (auto-generated if omitted)")
    p_aconf.add_argument("--item-code")
    p_aconf.add_argument("--domain", required=True)
    p_aconf.add_argument("--pop-a", required=True, help="Population A (wrapper must ensure pop_a < pop_b)")
    p_aconf.add_argument("--pop-b", required=True, help="Population B")
    p_aconf.add_argument("--status", required=True,
                         choices=dbcore.schema_choices("conflicts", "status"))
    p_aconf.add_argument("--resolution")
    p_aconf.add_argument("--evidence")
    p_aconf.add_argument("--gap-id")
    p_aconf.add_argument("--source-skill", default="cross-population-conflict-mapper")
    p_aconf.add_argument("--session", required=True)
    p_aconf.add_argument("--dry-run", action="store_true")

    # update-conflict
    p_uconf = sub.add_parser("update-conflict", help="Update a conflict record")
    p_uconf.add_argument("--conflict-id", required=True)
    p_uconf.add_argument("--status", choices=dbcore.schema_choices("conflicts", "status"))
    p_uconf.add_argument("--resolution")
    p_uconf.add_argument("--evidence")
    p_uconf.add_argument("--gap-id")
    p_uconf.add_argument("--session", required=True)
    p_uconf.add_argument("--dry-run", action="store_true")

    # conflicts
    p_confs = sub.add_parser("conflicts", help="Query conflict records")
    p_confs.add_argument("--item")
    p_confs.add_argument("--domain")
    p_confs.add_argument("--status")
    p_confs.add_argument("--summary", action="store_true")

    # delete-connection
    p_dc = sub.add_parser("delete-connection",
                           help="Hard-delete a connection by CON-ID (data corrections only)")
    p_dc.add_argument("--con-id", required=True)
    p_dc.add_argument("--session", required=True)
    p_dc.add_argument("--dry-run", action="store_true")

    # add-item — REFUSES. The item layer was deleted by owner ruling 2026-09-01;
    # the handler explains why and what to do instead. Every argument is optional
    # ON PURPOSE: `required=True` would make a bare `db.py add-item` die in argparse
    # with "the following arguments are required", and the caller would never reach
    # the refusal that tells them the layer is gone. An error that teaches beats an
    # error that is merely correct.
    p_ai = sub.add_parser("add-item",
                          help="REFUSED — the item layer was deleted (owner, 2026-09-01)")
    p_ai.add_argument("--item-code")
    p_ai.add_argument("--category")
    p_ai.add_argument("--name")
    p_ai.add_argument("--bpc-source-slug")
    p_ai.add_argument("--status", default="draft",
                      choices=dbcore.schema_choices("items", "status"))
    p_ai.add_argument("--item-id")
    p_ai.add_argument("--session")
    p_ai.add_argument("--dry-run", action="store_true")

    # items
    p_items = sub.add_parser("items", help="Query items")
    p_items.add_argument("--category")
    p_items.add_argument("--status")

    # add-audit-run
    p_aar = sub.add_parser("add-audit-run", help="Create an item_audit_runs record")
    p_aar.add_argument("--item-code", required=True)
    p_aar.add_argument("--session", required=True)
    p_aar.add_argument("--spec-hash")
    p_aar.add_argument("--status", default="IN-PROGRESS",
                       choices=dbcore.schema_choices("item_audit_runs", "status"))
    p_aar.add_argument("--dry-run", action="store_true")

    # update-audit-run
    p_uar = sub.add_parser("update-audit-run", help="Update an item_audit_runs record")
    p_uar.add_argument("--run-id", required=True)
    p_uar.add_argument("--session", required=True)
    p_uar.add_argument("--status", choices=dbcore.schema_choices("item_audit_runs", "status"))
    p_uar.add_argument("--steps-complete", help="JSON array of completed step names")
    p_uar.add_argument("--steps-started",  help="JSON array of started step names")
    p_uar.add_argument("--brief-path")
    p_uar.add_argument("--spec-hash")
    p_uar.add_argument("--dry-run", action="store_true")

    # audit-runs
    p_ar = sub.add_parser("audit-runs", help="Query item_audit_runs")
    p_ar.add_argument("--item")
    p_ar.add_argument("--status")

    # ── DR-2026-05-24: best-practice supersession protocol (migration 015) ─────
    # add-supersession-check
    p_asc = sub.add_parser("add-supersession-check",
                            help="Record a per-anchor-source supersession outcome (DR-2026-05-24)")
    p_asc.add_argument("--slug", required=True)
    p_asc.add_argument("--local-ref", required=True, help="Local ref id, e.g. RAP-23")
    p_asc.add_argument("--ref", required=True, help="Global ref_id, e.g. REF-00064")
    p_asc.add_argument("--tier", required=True, type=int, choices=[1,2,3,4,5,6])
    # THE LADDER IS THE AUTHORITY HERE, not another table's CHECK. This flag writes
    # `supersession_check.anchor_evidence_type`, which declares NO CHECK -- so the
    # mechanical sweep that derived the other nineteen choices lists had nothing local to
    # read and pointed this one at `search_executions.target_evidence_type`, whose
    # vocabulary happens to be identical. That would have made a foreign column
    # authoritative for one it does not govern: correct today, silently wrong the day
    # either CHECK moves. `TIER_MAP`'s keys ARE the evidence-type vocabulary (the ratified
    # ladder `add-source` already validates against), and verified equal to that column's
    # CHECK when this was written. The real gap -- that `anchor_evidence_type`,
    # `evidence_sources.tier` and `evidence_sources.evidence_type` declare no CHECK at all,
    # so CLAUDE.md rule 8's "vocabularies come from the schema" has nothing to come from --
    # is recorded, not closed here: adding those CHECKs is a schema change against the
    # ladder and wants its own migration.
    p_asc.add_argument("--evidence-type", required=True,
                       choices=_ladder_evidence_types())
    p_asc.add_argument("--outcome", required=True, choices=dbcore.schema_choices("supersession_check", "outcome"))
    p_asc.add_argument("--superseding-refs", default="[]",
                       help="JSON array of FK ref_ids (for already-verified candidates)")
    p_asc.add_argument("--superseding-dois", default="[]",
                       help="JSON array of DOIs (for not-yet-INSERTed candidates per PI rule #10)")
    p_asc.add_argument("--refinement-dimension",
                       help="Required when outcome=refined_by; names the dimension refined")
    p_asc.add_argument("--divergence-notes",
                       help="Required when outcome=divergent_no_supersession; summarizes divergence")
    p_asc.add_argument("--search-strategy", required=True,
                       help="JSON object: {tool, query, date_filter, candidates_returned, candidates_reviewed}")
    p_asc.add_argument("--check-method", required=True, choices=dbcore.schema_choices("supersession_check", "check_method"))
    p_asc.add_argument("--notes")
    p_asc.add_argument("--session", required=True)
    p_asc.add_argument("--dry-run", action="store_true")

    # ── DR-2026-05-26: gap-driven mining protocol (migration 017) ─────
    # add-gap-mining
    p_agm = sub.add_parser("add-gap-mining",
                            help="Record a gap-driven mining attempt (DR-2026-05-26)")
    p_agm.add_argument("--gap-id", required=True, help="Gap ID, e.g. GAP-069")
    p_agm.add_argument("--search-strategy", required=True,
                       help="JSON object: {\"strategies\":[{\"tool\":...,\"query\":...,\"candidates_returned\":N},...]}")
    p_agm.add_argument("--candidates-returned", required=True, type=int)
    p_agm.add_argument("--candidates-reviewed", required=True, type=int)
    p_agm.add_argument("--outcome", required=True, choices=dbcore.schema_choices("gap_mining", "outcome"))
    p_agm.add_argument("--discoveries", default="[]",
                       help="JSON array of FK ref_ids INSERTed this attempt")
    p_agm.add_argument("--candidate-dois", default="[]",
                       help="JSON array of DOIs of unverified candidates (PI rule #10 gate)")
    p_agm.add_argument("--check-method", required=True, choices=dbcore.schema_choices("gap_mining", "check_method"))
    p_agm.add_argument("--notes")
    p_agm.add_argument("--session", required=True)
    p_agm.add_argument("--dry-run", action="store_true")

    # update-gap-addressability
    p_uga = sub.add_parser("update-gap-addressability",
                            help="Set gaps.mining_addressability per DR-2026-05-26")
    p_uga.add_argument("--gap-id", required=True)
    p_uga.add_argument("--addressability", required=True, choices=dbcore.schema_choices("gaps", "mining_addressability"))
    p_uga.add_argument("--session", required=True)
    p_uga.add_argument("--dry-run", action="store_true")

    # unmined-gaps
    p_ung = sub.add_parser("unmined-gaps",
                            help="Query gaps eligible for gap-driven mining")
    p_ung.add_argument("--gap-id", help="Filter to a specific gap_id (returns its state)")
    p_ung.add_argument("--priority", choices=dbcore.schema_choices("gaps", "priority"),
                       help="Filter to priority")
    p_ung.add_argument("--include-not-addressable", action="store_true",
                       help="Include NOT-ADDRESSABLE gaps in results (default: ADDRESSABLE only)")
    p_ung.add_argument("--include-recent", action="store_true",
                       help="Include gaps with created_at within last 6 months (default: skip)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "migrate":
        import subprocess
        sys.exit(subprocess.call(
            [sys.executable, str(Path(__file__).parent / "migrate_db.py")]
        ))

    if args.command == "gaps":
        rows = get_open_gaps(priority=args.priority)
        if args.status:
            rows = [r for r in rows if args.status in r["status"]]
        _emit(rows)

    elif args.command == "connections":
        result = get_connections(
            status=args.status,
            confidence=args.confidence,
            summary=args.summary
        )
        _emit(result)

    elif args.command == "is-mined":
        result = is_mined(args.slug, args.ref)
        # THE OUTPUT SHAPE IS TOTAL, AND IT WAS NOT. `{"mined": False}` was emitted ONLY
        # when no citation_mining row existed; a row whose `executed` is False came back
        # with no `mined` key at all. Both skills branch on `mined: false` to decide
        # whether to invoke a mining pass, so the trigger never fired for exactly the
        # rows the owner ruling of 2026-09-18 says are owed -- REF-01002, REF-01003 and
        # REF-01004 among them. `mined` now always appears and always equals
        # `executed is True`, so a caller reading either key gets the same answer, and
        # `row_exists` distinguishes "no row" from "row says not mined" -- a distinction
        # `executed: null` did NOT carry (null means the ref names a source_locators
        # lead, which is a third thing again).
        if result:
            result = {**result, "mined": result.get("executed") is True,
                      "row_exists": True}
        else:
            result = {"mined": False, "executed": False, "row_exists": False}
        _emit(result)

    elif args.command == "log-mining":
        # PRINT WHAT THE WRITER DID, not a fixed dict. Until 2026-09-18 this reported
        # `logged: true` regardless, so a standing deferral the pass left undischarged
        # was invisible at the call site that created it.
        _emit(log_mining(
            slug=args.slug, ref_id=args.ref,
            direction=args.direction,
            session=args.session,
            dry_run=args.dry_run,
            deferred_reason=args.deferred_reason,
            status=args.mining_status,
            notes=args.notes,
            discharge_deferral=args.discharge_deferral,
        ))

    elif args.command == "next-id":
        id_funcs = {
            "connections": next_con_id,
            "gaps":        next_gap_id,
            "terms":       next_term_id,
            "conflicts":   next_conf_id,
            "ref":         next_ref,
        }
        _emit({"next_id": id_funcs[args.entity]()})

    elif args.command == "coverage":
        _emit(get_coverage_completeness(args.slug))

    elif args.command == "synonyms":
        _emit(get_synonyms(args.item, language=args.language))

    elif args.command == "add-gap":
        gap_id = next_gap_id()
        data = {
            "gap_id": gap_id,
            "category": args.category,
            "priority": args.priority,
            "status": "OPEN",
            "description": args.description,
        }
        if args.skill:
            data["skill"] = args.skill
        if args.section:
            data["section"] = args.section
        insert_gap(data, session=args.session, dry_run=args.dry_run)
        _emit({"gap_id": gap_id, "dry_run": args.dry_run})

    elif args.command == "close-gap":
        close_gap(args.gap_id, args.status,
                  session=args.session, dry_run=args.dry_run)
        _emit({"closed": args.gap_id, "status": args.status})

    elif args.command == "add-connection":
        targets = json.loads(args.targets)
        data = {
            "con_id": args.con_id,
            "status": args.status,
            "confidence": args.confidence,
            "connection_type": args.connection_type,
            "filed_in": args.filed_in,
            "description": args.description,
            "source_skill": args.source_skill,
            "opus_reviewed": 0,
        }
        insert_connection(data, targets,
                          session=args.session, dry_run=args.dry_run)
        _emit({"con_id": args.con_id, "dry_run": args.dry_run})

    elif args.command == "update-connection":
        update_connection_status(args.con_id, args.status,
                                 session=args.session, dry_run=args.dry_run)
        _emit({"updated": args.con_id, "status": args.status})

    elif args.command == "unmined":
        if args.slug:
            rows = get_unmined_sources(args.slug)
        else:
            rows = get_unmined_for_all_slugs(tier_max=args.tier_max)
        _emit(rows)

    elif args.command in ("upsert-coverage", "upsert-language"):
        # Kept as commands rather than deleted, so the skills and sessions that
        # still reach for them get the redirect instead of "invalid choice".
        table = ("search_coverage" if args.command == "upsert-coverage"
                 else "search_languages")
        print(_FROZEN_MSG.format(table=table), file=sys.stderr)
        sys.exit(2)

    elif args.command == "log-search":
        exec_id = log_search(
            slug=args.slug, language=args.language, query_text=args.query_text,
            engine=args.engine, depth_method=args.depth_method,
            session=args.session, jurisdiction=args.jurisdiction,
            target_tier=args.target_tier,
            target_evidence_type=args.target_evidence_type,
            target_scope=args.target_scope, terms_used=args.terms_used,
            mining_direction=args.mining_direction,
            results_found=args.results_found,
            results_screened=args.results_screened,
            results_admitted=args.results_admitted,
            saturation_signal=args.saturation_signal,
            admitted_ref_ids=args.admitted_ref_ids,
            deferred_reason=args.deferred_reason, backfill=args.backfill,
            findings_note=args.findings_note, harm_finding=args.harm_finding,
            prior_expectation=args.prior_expectation,
            origin=args.origin, mined_ref_id=args.mined_ref_id,
            origin_pass_id=args.origin_pass_id,
            result_artefacts=args.result_artefacts,
            dry_run=args.dry_run)
        _emit({"exec_id": exec_id, "slug": args.slug,
               "admitted": len(args.admitted_ref_ids or []),
               "linked_artefacts": len(args.result_artefacts or []),
               "dry_run": args.dry_run})

    elif args.command == "update-bpc":
        data = {}
        if args.citation_mining_complete is not None:
            data["citation_mining_complete"] = args.citation_mining_complete
        if args.bpc_complete is not None:
            data["bpc_complete"] = args.bpc_complete
        if args.search_complete is not None:
            data["search_complete"] = args.search_complete
        if args.pico_complete is not None:
            data["pico_complete"] = args.pico_complete
        if args.evidence_state is not None:
            data["evidence_state"] = args.evidence_state
        # DR-2026-05-24
        if args.supersession_check_complete is not None:
            data["supersession_check_complete"] = args.supersession_check_complete
        if args.closure_definition_version is not None:
            data["closure_definition_version"] = args.closure_definition_version
        if not data:
            print(json.dumps({"error": "No fields to update"}))
            sys.exit(1)
        update_bpc_metadata(args.slug, data,
                            session=args.session, dry_run=args.dry_run)
        _emit({"updated": True, "slug": args.slug, "fields": list(data.keys())})

    elif args.command == "add-candidate":
        cid = insert_search_candidate({
            "exec_id": args.exec_id, "found_under_slug": args.found_under_slug,
            "suggested_slug": args.suggested_slug, "disposition": args.disposition,
            "title": args.title, "locator": args.locator,
            "locator_status": args.locator_status, "tier_guess": args.tier_guess,
            "harm_finding": args.harm_finding, "why_not_admitted": args.why_not_admitted,
            "notes": args.notes, "surfaced_in": args.surfaced_in,
            "surfaced_quote": args.surfaced_quote,
        }, session=args.session, dry_run=args.dry_run)
        _emit({"candidate_id": cid, "dry_run": args.dry_run})

    elif args.command == "add-population-match":
        mid = insert_population_match({
            "ref_id": args.ref_id, "target_population": args.target_population,
            "study_population": args.study_population, "sample_size": args.sample_size,
            "match_grade": args.match_grade, "mismatch_note": args.mismatch_note,
            "gap_id": args.gap_id,
        }, session=args.session, dry_run=args.dry_run)
        _emit({"match_id": mid, "dry_run": args.dry_run})

    elif args.command == "add-jurisdictional-value":
        jv = insert_jurisdictional_value({
            "jv_id": args.jv_id, "item_code": args.item_code,
            "jurisdiction": args.jurisdiction, "standard_name": args.standard_name,
            "value_text": args.value_text, "value_numeric": args.value_numeric,
            "unit": args.unit, "is_code_minimum": args.is_code_minimum,
            "evidence_tier": args.evidence_tier, "source_section": args.source_section,
            "loc_section": args.loc_section, "loc_clause": args.loc_clause,
            "notes": args.notes,
        }, session=args.session, dry_run=args.dry_run)
        _emit({"jv_id": jv, "dry_run": args.dry_run})

    elif args.command == "add-economics-entry":
        eid = insert_economics_entry({
            "entry_id": args.entry_id, "pillar": args.pillar,
            "entry_type": args.entry_type, "ref_id": args.ref_id, "source": args.source,
            "finding": args.finding, "status": args.status,
            "value_numeric": args.value_numeric, "value_unit": args.value_unit,
            "currency": args.currency, "jurisdiction": args.jurisdiction,
            "notes": args.notes,
        }, session=args.session, dry_run=args.dry_run)
        _emit({"entry_id": eid, "dry_run": args.dry_run})

    elif args.command == "add-case-study":
        cs = insert_case_study({
            "case_study_id": args.case_study_id, "slug": args.slug, "title": args.title,
            "building_type": args.building_type, "location": args.location,
            "year": args.year, "harm_finding": args.harm_finding, "status": args.status,
            "sources": args.sources, "notes": args.notes,
        }, session=args.session, dry_run=args.dry_run)
        _emit({"case_study_id": cs, "dry_run": args.dry_run})

    elif args.command == "add-code-lead":
        lid = insert_code_lead({
            "jurisdiction": args.jurisdiction, "standard_name": args.standard_name,
            "clause": args.clause, "status": args.status,
            "recovered_from": args.recovered_from, "notes": args.notes,
        }, session=args.session, dry_run=args.dry_run,
            distinct_from=args.distinct_from, reason=args.reason)
        _emit({"lead_id": lid, "dry_run": args.dry_run})

    elif args.command == "update-code-lead":
        _emit(update_code_lead(args.lead_id, args.append_note, session=args.session,
                               status=args.status, clause=args.clause,
                               dry_run=args.dry_run))

    elif args.command == "correct-source":
        ch = correct_source(args.ref_id, args.fields, session=args.session,
                            log_session=args.log_session, dry_run=args.dry_run)
        _emit({"ref_id": args.ref_id, "corrected": ch, "dry_run": args.dry_run})

    elif args.command == "amend-search":
        _emit(amend_search(args.exec_id, args.append_note, session=args.session,
                           dry_run=args.dry_run,
                           set_harm_finding=args.set_harm_finding,
                           set_target_evidence_type=args.set_target_evidence_type,
                           set_origin=args.set_origin,
                           set_mined_ref_id=args.set_mined_ref_id,
                           set_origin_pass_id=args.set_origin_pass_id,
                           add_result_artefacts=args.add_result_artefacts,
                           clear_target=args.clear_target))

    elif args.command == "amend-gap":
        # _emit, not a bare assignment: until 2026-09-25 both of these assigned the
        # writer's result to `out` and never printed it, so a successful amendment and a
        # no-op ("already on the row") were indistinguishable from the shell.
        _emit(amend_gap(args.gap_id, args.append_note, args.session, args.dry_run))
    elif args.command == "reattribute-candidate":
        _emit(reattribute_candidate(args.candidate_id, args.exec_id, args.reason,
                                    args.session, args.dry_run,
                                    surfaced_in=args.surfaced_in,
                                    surfaced_quote=args.surfaced_quote))
    elif args.command == "record-adversarial-pass":
        _emit(record_adversarial_pass(args.subject_session, args.subject_commit,
                                      args.reviewer_transcript, args.author_transcript,
                                      args.session, args.dry_run))
    elif args.command == "dispose-adversarial-finding":
        _emit(dispose_adversarial_finding(args.finding_id, args.disposition, args.ref,
                                          args.session, reason=args.reason,
                                          dry_run=args.dry_run))
    elif args.command == "close-adversarial-pass":
        result = close_adversarial_pass(args.pass_id, args.session, args.dry_run)
        for fid, toks in sorted(result["unresolved"].items()):
            print(f"REPORTED: finding {fid}: path token(s) that did not resolve to a "
                  f"file under the repo: {toks}", file=sys.stderr)
        for fid, toks in sorted(result["database_only"].items()):
            print(f"REPORTED: finding {fid} was admitted only on {toks}, inside the "
                  f"database's directory; the database is not an artefact of attack.",
                  file=sys.stderr)
        _emit(result)
    elif args.command == "resolve-candidate":
        _emit(resolve_candidate(args.candidate_id, args.disposition, args.redescription,
                                session=args.session, admitted_ref_id=args.admitted_ref_id,
                                dry_run=args.dry_run, suggested_slug=args.suggested_slug,
                                clear_suggested_slug=args.clear_suggested_slug))
    elif args.command == "link-admission":
        _emit(link_admission(args.exec_id, args.ref_id, args.reason,
                             session=args.session, dry_run=args.dry_run))
    elif args.command == "unlink-admission":
        _emit(unlink_admission(args.exec_id, args.ref_id, args.reason,
                               session=args.session, dry_run=args.dry_run))
    elif args.command == "amend-population-match":
        _emit(amend_population_match(args.match_id, args.match_grade, args.reason,
                                     session=args.session, dry_run=args.dry_run))
    elif args.command == "amend-term":
        _emit(amend_term(args.term_id, args.field, args.replacement, args.reason,
                         session=args.session, dry_run=args.dry_run))

    elif args.command == "amend-source":
        _emit(amend_source(args.ref_id, args.field, args.replacement, args.reason,
                           session=args.session, dry_run=args.dry_run,
                           tier=args.tier, scope=args.scope,
                           co1_provenance=args.co1_provenance,
                           co1_source_type=args.co1_source_type))

    elif args.command == "retire-specification":
        _emit(retire_specification(args.specification_id, reason=args.reason,
                                   superseded_by=args.superseded_by,
                                   session=args.session, dry_run=args.dry_run))
    elif args.command == "link-source-slug":
        _emit(link_source_slug(args.ref_id, args.slug, args.rationale,
                               session=args.session, dry_run=args.dry_run,
                               local_ref_id=args.local_ref_id))

    elif args.command == "supersede-source":
        _emit(supersede_source(args.ref_id, args.by, args.reason,
                               session=args.session, dry_run=args.dry_run))

    elif args.command == "update-locator":
        _emit(update_locator(args.ref_id, args.status, session=args.session,
                             reason=args.reason, dry_run=args.dry_run))

    elif args.command == "observe-term":
        _emit(observe_term({
            "ref_id": args.ref_id, "surface_form": args.surface_form,
            "language": args.language, "locator": args.locator,
            "context_quote": args.context_quote, "notes": args.notes,
        }, session=args.session, dry_run=args.dry_run))

    elif args.command == "add-term":
        _emit(insert_term(
            from_observation=args.from_observation,
            canonical_en=args.canonical_en,
            rationale=args.rationale,
            definition=args.definition,
            domain=args.domain,
            scope_note=args.scope_note,
            session=args.session,
            dry_run=args.dry_run,
        ))

    elif args.command == "set-parameter-direction":
        _emit(set_parameter_direction(
            parameter_id=args.parameter_id, direction=args.direction,
            rationale=args.rationale, session=args.session, dry_run=args.dry_run))

    elif args.command == "add-parameter":
        _emit(insert_parameter(
            term_id=args.term_id,
            notes=args.notes,
            session=args.session,
            dry_run=args.dry_run,
        ))

    elif args.command == "decline-parameter":
        _emit(decline_parameter(
            term_id=args.term_id,
            reason=args.reason,
            session=args.session,
            dry_run=args.dry_run,
        ))

    elif args.command == "add-icf-code":
        _emit(insert_icf_code(
            icf_code=args.icf_code, title=args.title, title_source=args.title_source,
            title_payload=args.title_payload, notes=args.notes,
            session=args.session, dry_run=args.dry_run))

    elif args.command == "set-icf-title":
        _emit(set_icf_title(
            icf_code=args.icf_code, title=args.title, title_source=args.title_source,
            title_payload=args.title_payload, session=args.session, dry_run=args.dry_run))

    elif args.command == "add-population-icf-link":
        _emit(insert_population_icf_link(
            population=args.population, icf_code=args.icf_code,
            mechanism=args.mechanism, mapping_confidence=args.mapping_confidence,
            provenance=args.provenance, notes=args.notes,
            session=args.session, dry_run=args.dry_run))

    elif args.command == "raise-determination-gate":
        _emit(raise_determination_gate(
            parameter_id=args.parameter_id, identity=args.identity,
            verdict=args.verdict, trigger_ref_id=args.trigger_ref_id,
            trigger_tier=args.trigger_tier,
            trigger_evidence_type=args.trigger_evidence_type,
            detail=args.detail, session=args.session, dry_run=args.dry_run))

    elif args.command == "resolve-determination-gate":
        _emit(resolve_determination_gate(
            gate_id=args.gate_id, rationale=args.rationale,
            session=args.session, dry_run=args.dry_run))

    elif args.command == "add-medical":
        out = insert_medical(
            code=args.code, display_name=args.display_name, icd11=args.icd11,
            description=args.description, icd11_payload=args.icd11_payload,
            identity=args.identity, relationship=args.relationship,
            icf=args.icf, role=args.role, mapping_confidence=args.mapping_confidence,
            note=args.note, session=args.session, dry_run=args.dry_run)
        print(json.dumps(out, indent=2, ensure_ascii=False))

    elif args.command == "add-extraction":
        # The lens flags are named for the LENS and stored in the COLUMN; the mapping
        # is stated once, here, and mirrors db._LENS_COLUMNS' key order.
        _ax = {"ref_id": args.ref_id, "slug": args.slug,
               "parameter_id": args.parameter_id,
               "identity_code": args.identity, "icf_code": args.icf,
               "needs_code": args.needs, "medical_code": args.medical,
               "claim_type": args.claim_type, "claimed_value": args.claimed_value,
               "claimed_unit": args.claimed_unit, "claim_text": args.claim_text,
               "source_section": args.source_section,
               "jurisdiction": args.jurisdiction, "setting": args.setting,
               "extraction_method": args.extraction_method,
               "extraction_status": args.extraction_status,
               "root_id": args.root_id, "root_type": args.root_type,
               "root_ref_id": args.root_ref_id, "echo_of": args.echo_of,
               "measurement_paradigm": args.measurement_paradigm,
               "device_class": args.device_class,
               "root_population_note": args.root_population_note,
               "root_classification_basis": args.root_classification_basis,
               "contested": args.contested, "file_anchor": args.file_anchor,
               "locator_scheme": args.locator_scheme, "loc_note": args.loc_note,
               "notes": args.notes,
               "figure_role": args.figure_role, "comparator": args.comparator}
        for _lvl in ("division", "part", "section", "subsection", "paragraph",
                     "clause", "subclause"):
            _ax[f"loc_{_lvl}"] = getattr(args, f"loc_{_lvl}")
            _ax[f"loc_{_lvl}_end"] = getattr(args, f"loc_{_lvl}_end")
        _relations = _build_relation_groups(
            args.relations, args.to_extractions, args.to_labels, args.to_kinds,
            args.stateds, args.quotes, args.input_roles, args.cross_sources)
        _emit(insert_extraction(_ax, session=args.session, dry_run=args.dry_run,
                                relations=_relations,
                                verbatim_exempt=args.verbatim_exempt))

    elif args.command == "relate-extraction":
        if args.repoint:
            # REFUSE THE FLAGS --repoint CANNOT HONOUR, rather than dropping them.
            # `repoint_extraction_relation` takes from/relation/to-extraction/old-label
            # and nothing else -- it NULLs the label and kind and ledgers the old label,
            # by definition leaving the edge's own assertion untouched. The subparser is
            # shared with the create path, so seven of its flags were accepted here and
            # silently discarded: an operator typing `--repoint --quote "..."` got no
            # quote and no complaint. CLAUDE.md section 8: "an unread field, an uncalled
            # script and an unregistered check are the same defect."
            _ignored = [n for n, v in (
                ("--to-label", args.to_label), ("--to-kind", args.to_kind),
                ("--stated", args.stated), ("--quote", args.quote),
                ("--input-role", args.input_role), ("--notes", args.notes),
                ("--cross-source", args.cross_source_reason)) if v]
            if _ignored:
                raise Refusal(
                    f"relate-extraction --repoint does not accept "
                    f"{', '.join(_ignored)}. Repointing turns an existing LABEL edge "
                    f"into a ROW pointer; it does not restate what the edge asserts, "
                    f"so those values would be silently dropped. Repoint first, then "
                    f"amend the edge if its assertion is also wrong. Nothing was "
                    f"written.")
            _emit(repoint_extraction_relation(
                args.from_extraction, args.relation, args.to_extraction,
                old_label=args.old_label, session=args.session, dry_run=args.dry_run))
        else:
            _emit(relate_extraction(
                args.from_extraction, args.relation, session=args.session,
                dry_run=args.dry_run, to_extraction=args.to_extraction,
                to_label=args.to_label, to_kind=args.to_kind, stated=args.stated,
                quote=args.quote, input_role=args.input_role, notes=args.notes,
                cross_source_reason=args.cross_source_reason))

    elif args.command == "amend-extraction":
        _emit(amend_extraction(args.extraction_id, args.field, args.value,
                               args.reason, session=args.session,
                               dry_run=args.dry_run))

    elif args.command == "derive-extraction":
        _emit(derive_extraction(
            ref_id=args.ref_id, slug=args.slug, parameter_id=args.parameter_id,
            identity=args.identity, icf=args.icf, needs=args.needs,
            medical=args.medical, base=args.base, delta=args.delta,
            claimed_value=args.claimed_value, claimed_unit=args.claimed_unit,
            comparator=args.comparator, conversion_note=args.conversion_note,
            claim_text=args.claim_text, session=args.session, dry_run=args.dry_run))

    elif args.command == "adjudicate-term":
        _emit(adjudicate_term(args.observation_id, args.outcome, args.rationale,
                              session=args.session, term_id=args.term_id,
                              dry_run=args.dry_run))

    elif args.command == "add-locator":
        rid = insert_locator({
            "ref_id": args.ref_id, "doi": args.doi, "pmid": args.pmid,
            "pmcid": args.pmcid, "isbn": args.isbn, "issn": args.issn, "url": args.url,
            "standard_number": args.standard_number, "title": args.title,
            "authors": args.authors, "pub_year": args.pub_year,
            "tier_claimed": args.tier_claimed, "recovered_from": args.recovered_from,
            "status": args.status, "used_in_bpcs": args.used_in_bpcs, "notes": args.notes,
        }, session=args.session, dry_run=args.dry_run)
        _emit({"ref_id": rid, "dry_run": args.dry_run})

    elif args.command == "add-source":
        if not args.author and not args.authors:
            parser.error("add-source needs --author (repeatable, preferred) or --authors")
        if args.author and args.authors:
            parser.error("give --author or --authors, not both: two spellings of the "
                         "author list is the copy this migration removes")
        data = {
            "ref_id": args.ref_id,
            "year": args.year,
            "title": args.title,
            "tier": args.tier,
        }
        if args.doi:
            data["doi"] = args.doi
        if args.pmid:
            data["pmid"] = args.pmid
        if args.jurisdiction:
            data["jurisdiction"] = args.jurisdiction
        if args.evidence_type:
            data["evidence_type"] = args.evidence_type
        if args.lang_detected:
            data["lang_detected"] = args.lang_detected
        if args.lang_detection_method:
            data["lang_detection_method"] = args.lang_detection_method
        if args.metadata_quality:
            data["metadata_quality"] = args.metadata_quality
        if args.verification_status:
            data["verification_status"] = args.verification_status
        if args.verification_method:
            data["verification_method"] = args.verification_method
        if args.verified_by_tool:
            data["verified_by_tool"] = args.verified_by_tool
        for _flag, _col in (("url", "url"), ("url_accessed", "url_accessed"),
                            ("pages", "pages"),
                            ("doi_resolution_outcome", "doi_resolution_outcome"),
                            # The Co-1 warrant and its companions. Omitting these here on
                            # 2026-09-02 made the flag parse, the refusal pass, and the value
                            # silently never reach the row — a worse failure than no flag at
                            # all, because the CLI would have reported success on a Co-1
                            # admission whose warrant was dropped on the floor.
                            ("co1_provenance", "co1_provenance"),
                            ("co1_source_type", "co1_source_type"),
                            ("synthesis_attribution_required",
                             "synthesis_attribution_required"),
                            # Added 2026-09-02: research_protocol_audit CHECK 7 asks for
                            # this on every verified citation and nothing could write it,
                            # so all nine of batch 05's sources failed it and none could
                            # be fixed honestly -- a prior recorded after reading the
                            # source is not a prior.
                            # Added 2026-09-18 (batch 18): the report/venue set. Same
                            # failure shape as the 2026-09-02 note above -- a flag that
                            # parses and never reaches the row reports success on a write
                            # that did not happen.
                            ("source_type", "source_type"),
                            ("institution", "institution"),
                            ("report_number", "report_number"),
                            ("series", "series"),
                            ("series_number", "series_number"),
                            ("publisher", "publisher"),
                            ("publisher_location", "publisher_location"),
                            ("book_title", "book_title"),
                            ("grey_flag", "grey_flag"),
                            ("grey_reason", "grey_reason"),
                            ):
            _v = getattr(args, _flag, None)
            # `is not None`, not truthiness: synthesis_attribution_required is an int flag
            # and 0 is a real, meaningful value that `if _v` would discard.
            if _v is not None:
                data[_col] = _v
        # THE TIER MUST BE DERIVABLE, NOT MERELY ASSERTED (2026-09-10).
        #
        # schemas/tier_derivation.py calls TIER_MAP "the ratified ladder as a total
        # function" over (evidence_type, scope). This CLI could write --tier and had no
        # --scope, so the ladder had no input and the tier was whatever the operator
        # typed. Every one of the 9 admitted sources carries scope NULL, and
        # adjudication_integrity.py reports 9 of 9 stored tiers as underivable — a field
        # that is POPULATED but not TRUE, which is CLAUDE.md §5(c)'s failure exactly, and
        # tier is what drives weight, which drives the determination.
        #
        # Six of the eight evidence types admit exactly one scope, so demanding a flag
        # nobody could get wrong would be friction without a decision. It is supplied.
        # The two that carry a real judgment — clinical (how controlled) and standard_eb
        # (whose standard) — must be said, and are refused if silent.
        #
        # THIS IS A PARITY CHECK, AND RULE 5 SAYS A PARITY CHECK IS NOT A FIX: it makes a
        # dual home survivable, therefore permanent. Once `scope` is recorded, `tier` IS
        # derive_tier(evidence_type, scope) — a stored copy of a computed fact. The
        # sanctioned end state is to retire it: writer-retire --tier, reader-retire the
        # column, NULL forward (CLAUDE.md §5). That is a sweep across every reader of
        # evidence_sources.tier, including the determination engine, and it is not this
        # change. What this change does is stop the two from diverging any further, so the
        # retirement has a consistent corpus to work from. Do not read the guard as the
        # remedy.
        #
        # LAYER: this is a Layer 1 refusal in a Layer 1 writer, deriving from the Layer 1
        # model. The ladder is IMPORTED from schemas/tier_derivation.py, never restated
        # here — a second copy of a ratified rule is the dual home rule 5 forbids, and a
        # CLI whose refusals come from its own list rather than the one authority is the
        # thing this file exists not to be.
        _etype = (args.evidence_type or "").lower()
        if not _etype:
            # BYPASS CLOSED 2026-09-10. The guard below used to be `if _etype:`, so
            # omitting --evidence-type skipped it entirely and a bare `--tier 1` landed
            # a row with type NULL and scope NULL — underivable by construction, which
            # is the precise thing the guard exists to prevent. Proven on a scratch
            # copy: REF-90001 (tier 1, type NULL, scope NULL) accepted.
            raise Refusal(
                "--evidence-type is REQUIRED. The tier is derived from "
                "(evidence_type, scope) — with no type there is nothing to derive it "
                "from, and --tier alone is an assertion.\n"
                "Types: clinical, co1, co2, sr_meta, grey, standard_eb, national_fw, code.")
        # STORE THE NORMALISED FORM. --evidence-type CLINICAL used to derive from the
        # lowercased value and then store the raw string, so the row satisfied the ladder
        # at write time and was invisible to every reader afterwards —
        # assess_cell.classify() compares against lowercase literals, so a 'CLINICAL'
        # source falls into the `other` bucket and silently stops anchoring anything.
        args.evidence_type = _etype
        data["evidence_type"] = _etype
        if True:
            from schemas.tier_derivation import (  # noqa: E402
                TIER_MAP, VALID_SCOPES_BY_TYPE, derive_tier)
            _valid = VALID_SCOPES_BY_TYPE.get(_etype)
            if _valid is None:
                raise Refusal(
                    f"--evidence-type {_etype!r} is not on the ratified ladder. "
                    f"Known types: {sorted(VALID_SCOPES_BY_TYPE)}")
            _scope = args.scope
            if _scope is None and len(_valid) == 1:
                _scope = next(iter(_valid))          # forced by the type; not a judgment
            if _scope is None:
                raise Refusal(
                    f"--scope is REQUIRED for --evidence-type {_etype!r}: it is the "
                    f"discriminator the ratified tier is derived from, and this type "
                    f"spans more than one tier. Choose {sorted(_valid)}.\n"
                    f"Without it the tier is an assertion, and a tier that cannot be "
                    f"derived cannot be contested.")
            if _scope not in _valid:
                raise Refusal(
                    f"--scope {_scope!r} is not admissible for --evidence-type "
                    f"{_etype!r}; valid: {sorted(_valid)}")
            _derived = derive_tier(_etype, _scope)
            if args.tier != _derived:
                raise Refusal(
                    f"--tier {args.tier} contradicts the ratified ladder: "
                    f"({_etype}, {_scope}) derives tier {_derived}.\n"
                    f"The tier is not a free integer — it is a function of the evidence "
                    f"type and its scope. Either the scope is wrong or the tier is; "
                    f"say which, do not assert past it.")
            data["scope"] = _scope

        # THE CO-1 WARRANT REFUSAL (D-0178, ratified 2026-08-31). A Co-1 admission whose
        # warrant is not stated is "unwarranted-pending", and Co-1 is co-primary with T1
        # under CRPD Art 4.3 — this is the tier where the claim rests entirely on disabled
        # people having produced the work. CLAUDE.md §6: "Erasing them while claiming the
        # tier is the worst failure available here." On 2026-09-01 two Co-1 rows were
        # written with co1_provenance NULL because the CLI could not say it; nothing
        # refused them. Now something does.
        if (args.evidence_type or "").lower() == "co1" and not args.co1_provenance:
            raise Refusal(
                "--co1-provenance is REQUIRED for --evidence-type co1. "
                + CO1_WARRANT_REQUIRED
                + "admit it at its actual tier and say why in --notes.")
        # THE SLUG AND ITS LABEL ARE RESOLVED READ-ONLY BEFORE ANY WRITE, and the
        # source and its link are then written in ONE transaction.
        #
        # History, because each step was a defect. (1) The link INSERT sat inside
        # `if args.slug and args.local_ref_id:` while the _emit announced
        # "linked_slug" unconditionally, so `--slug X` without a label wrote no
        # link and said it had. (2) The guard added for that was written AFTER
        # insert_evidence_source, so its refusal left an ORPHAN admission (REF-09999,
        # 2026-09-17). (3) --local-ref-id then became optional and derived -- and the
        # derivation's own refusal (a slug whose labels mix schemes) still fired only
        # inside insert_source_slug_link, after the source had committed. A comment
        # here claimed "refuse before any write" while that was false: batch 23 left
        # an orphan this way and had to hand-delete it (GAP-058). (4) Under --dry-run
        # the second block's foreign key could not see the rolled-back source, so
        # `add-source --slug ... --dry-run` crashed with a traceback.
        #
        # The pre-check below calls the same guards insert_source_slug_link runs, so
        # there is one rule; the shared transaction means that if anything still
        # refuses after the source INSERT, nothing is committed.
        if args.local_ref_id is not None and not args.slug:
            raise Refusal(
                "--local-ref-id was given without --slug. The label is per-slug and "
                "would not be written. Nothing was written.")
        label = None
        if args.slug:
            with connect(readonly=True) as _c:
                _check_slug_filable(_c, args.slug)
                label = _check_link_label(_c, args.slug, args.local_ref_id,
                                          args.ref_id)
        authors = (parse_author_flags(args.author) if args.author
                   else parse_author_display(args.authors))
        local_ref_id = None
        with connect(args.dry_run) as _w:
            ref_id = insert_evidence_source(data, session=args.session,
                                            dry_run=args.dry_run, authors=authors,
                                            conn=_w)
            if args.slug:
                wrote, local_ref_id = insert_source_slug_link(
                    ref_id, args.slug, label, session=args.session, conn=_w)
                if not wrote:
                    raise Refusal(
                        f"the slug link {ref_id} -> '{args.slug}' affected no row, so "
                        f"neither it nor the source was written. Re-run and read the "
                        f"refusal.")
        _emit({"ref_id": ref_id, "linked_slug": args.slug,
               "local_ref_id": local_ref_id, "dry_run": args.dry_run})


    # ── CO-0009 Phase 1 Session 1b ─────────────────────────────────────────

    elif args.command == "add-conflict":
        conf_id = args.conflict_id if args.conflict_id else next_conf_id()
        data = {
            "conflict_id": conf_id,
            "domain":      args.domain,
            "pop_a":       args.pop_a,
            "pop_b":       args.pop_b,
            "status":      args.status,
            "source_skill": args.source_skill,
        }
        if args.item_code:   data["item_code"]  = args.item_code
        if args.resolution:  data["resolution"] = args.resolution
        if args.evidence:    data["evidence"]   = args.evidence
        if args.gap_id:      data["gap_id"]     = args.gap_id
        insert_conflict(data, session=args.session, dry_run=args.dry_run)
        _emit({"conflict_id": conf_id, "dry_run": args.dry_run})

    elif args.command == "update-conflict":
        update_conflict(
            args.conflict_id, session=args.session,
            status=args.status, resolution=args.resolution,
            evidence=args.evidence, gap_id=args.gap_id,
            dry_run=args.dry_run,
        )
        _emit({"updated": args.conflict_id})

    elif args.command == "conflicts":
        result = get_conflicts(
            item_code=args.item, domain=args.domain,
            status=args.status, summary=args.summary,
        )
        _emit(result)

    elif args.command == "delete-connection":
        delete_connection(args.con_id, session=args.session, dry_run=args.dry_run)
        _emit({"deleted": args.con_id, "dry_run": args.dry_run})

    elif args.command == "add-item":
        raise SystemExit(
            "add-item REFUSES: the item layer was deleted by owner ruling 2026-09-01 "
            "and there is no ruling to restore it.\n"
            "\n"
            "WHY, in the owner's terms: if E-08 already exists then the work is "
            "predisposed to filing into a container that already exists, and that "
            "biases every finding. Measured in DR-2026-08-19 1.1, 42 of the 93 item "
            "names embedded a determination -- `E-08 Corridor Clear Width (>=1200 mm "
            "Minimum on All Primary Routes)` states its answer in its own name, so a "
            "search framed on it is a search for confirmation. That is why the layer "
            "went, and why a writer that can retype an old code verbatim is the "
            "contamination path rather than a convenience.\n"
            "\n"
            "This refusal is deliberately not a deletion. Deleting the subcommand "
            "would send you to hand-written SQL against `items`, which CLAUDE.md 4 "
            "names as the exact temptation to refuse.\n"
            "\n"
            "WHAT TO DO INSTEAD -- and this is RULED, not open. Owner ruling "
            "2026-08-26 (references/project-standards.md, grep -n 'judgment object "
            "is the'): the judgment object is the CANONICAL PARAMETER, and `items` "
            "is the render rollup -- derived FROM specifications, never keying "
            "them. specifications.item_code is dropped alongside population_code in "
            "the same migration. Read that ruling's five-clause ACTION before "
            "touching any of it. Do not reach for `slug x population` either: "
            "`populations` is only the identity lens.\n"
            "\n"
            "(This text called the subject an OPEN OWNER DECISION until 2026-09-09, "
            "while the ruling had stood since 2026-08-26. Declaring open a question "
            "already answered is CLAUDE.md rule 4b wearing its other face.)\n"
            "\n"
            "A subject the pipeline PRODUCES is the point. An item must be an output "
            "of the work, never a container chosen before it."
        )

    elif args.command == "items":
        _emit(get_items(category=args.category, status=args.status))

    elif args.command == "add-audit-run":
        run_id = f"{args.item_code}_{args.session}"
        data   = {
            "run_id":    run_id,
            "item_code": args.item_code,
            # `"session": args.session` stood here until migration 085 DROPPED
            # item_audit_runs.session as a duplicate of created_by_session,
            # which insert_audit_run's own audit() stamp supplies.
            "status":    args.status,
        }
        if args.spec_hash: data["spec_hash"] = args.spec_hash
        insert_audit_run(data, session=args.session, dry_run=args.dry_run)
        _emit({"run_id": run_id, "dry_run": args.dry_run})

    elif args.command == "update-audit-run":
        sc = json.loads(args.steps_complete) if args.steps_complete else None
        ss = json.loads(args.steps_started)  if args.steps_started  else None
        update_audit_run(
            args.run_id, session=args.session,
            status=args.status, steps_complete=sc, steps_started=ss,
            brief_path=args.brief_path, spec_hash=args.spec_hash,
            dry_run=args.dry_run,
        )
        _emit({"updated": args.run_id})

    elif args.command == "audit-runs":
        _emit(get_audit_runs(item_code=args.item, status=args.status))

    elif args.command == "add-supersession-check":
        # DR-2026-05-24 — per-anchor-source supersession outcome
        sup_refs = json.loads(args.superseding_refs) if args.superseding_refs else []
        sup_dois = json.loads(args.superseding_dois) if args.superseding_dois else []
        # Validate strategy is parseable JSON
        try:
            strategy = json.loads(args.search_strategy)
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"--search-strategy is not valid JSON: {e}"}))
            sys.exit(2)
        # Validate outcome-specific required args (mirrors SQL CHECK)
        if args.outcome == "refined_by" and not args.refinement_dimension:
            print(json.dumps({"error": "outcome=refined_by requires --refinement-dimension"}))
            sys.exit(2)
        if args.outcome == "divergent_no_supersession" and not args.divergence_notes:
            print(json.dumps({"error": "outcome=divergent_no_supersession requires --divergence-notes"}))
            sys.exit(2)
        if args.outcome in ("superseded_by", "refined_by", "divergent_no_supersession") and not (sup_refs or sup_dois):
            print(json.dumps({"error": f"outcome={args.outcome} requires --superseding-refs or --superseding-dois"}))
            sys.exit(2)
        if args.outcome == "co1_addition_logged" and args.evidence_type != "co1":
            print(json.dumps({"error": "outcome=co1_addition_logged only valid for evidence_type=co1"}))
            sys.exit(2)
        check_id = add_supersession_check(
            slug=args.slug, local_ref_id=args.local_ref, ref_id=args.ref,
            anchor_tier=args.tier, anchor_evidence_type=args.evidence_type,
            outcome=args.outcome,
            superseding_ref_ids=sup_refs, superseding_dois=sup_dois,
            refinement_dimension=args.refinement_dimension,
            divergence_notes=args.divergence_notes,
            search_strategy_record=json.dumps(strategy),
            candidates_returned=int(strategy.get("candidates_returned", 0)),
            candidates_reviewed=int(strategy.get("candidates_reviewed", 0)),
            check_method=args.check_method,
            notes=args.notes,
            session=args.session, dry_run=args.dry_run,
        )
        _emit({"check_id": check_id, "dry_run": args.dry_run})

    elif args.command == "add-gap-mining":
        # DR-2026-05-26 — per-gap mining attempt (migration 017)
        # Validate JSON fields up-front
        try:
            strategy = json.loads(args.search_strategy)
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"--search-strategy is not valid JSON: {e}"}))
            sys.exit(2)
        try:
            discoveries = json.loads(args.discoveries) if args.discoveries else []
            if not isinstance(discoveries, list):
                raise Refusal("--discoveries must be a JSON array")
        except (json.JSONDecodeError, ValueError) as e:
            print(json.dumps({"error": f"--discoveries: {e}"}))
            sys.exit(2)
        try:
            cand_dois = json.loads(args.candidate_dois) if args.candidate_dois else []
            if not isinstance(cand_dois, list):
                raise Refusal("--candidate-dois must be a JSON array")
        except (json.JSONDecodeError, ValueError) as e:
            print(json.dumps({"error": f"--candidate-dois: {e}"}))
            sys.exit(2)
        # Validate outcome-specific required args (mirrors SQL CHECK)
        if args.outcome == "closure_evidence_found" and not discoveries:
            print(json.dumps({"error": "outcome=closure_evidence_found requires at least one entry in --discoveries"}))
            sys.exit(2)
        if args.outcome == "gap_recategorized" and (not args.notes or len(args.notes) < 20):
            print(json.dumps({"error": "outcome=gap_recategorized requires --notes (>=20 chars)"}))
            sys.exit(2)
        if args.outcome == "deferred" and (not args.notes or len(args.notes) < 10):
            print(json.dumps({"error": "outcome=deferred requires --notes (>=10 chars)"}))
            sys.exit(2)
        gap_mining_id = add_gap_mining(
            gap_id=args.gap_id,
            search_strategy_record=json.dumps(strategy),
            candidates_returned=args.candidates_returned,
            candidates_reviewed=args.candidates_reviewed,
            outcome=args.outcome,
            discoveries_logged=discoveries,
            candidate_dois=cand_dois,
            check_method=args.check_method,
            notes=args.notes,
            session=args.session, dry_run=args.dry_run,
        )
        _emit({"gap_mining_id": gap_mining_id, "dry_run": args.dry_run})

    elif args.command == "update-gap-addressability":
        # DR-2026-05-26 — set gaps.mining_addressability
        update_gap_addressability(
            gap_id=args.gap_id,
            addressability=args.addressability,
            session=args.session,
            dry_run=args.dry_run,
        )
        _emit({"gap_id": args.gap_id, "mining_addressability": args.addressability,
               "dry_run": args.dry_run})

    elif args.command == "unmined-gaps":
        # DR-2026-05-26 — query mining-eligible gaps
        rows = get_unmined_gaps(
            gap_id=args.gap_id,
            priority=args.priority,
            include_not_addressable=args.include_not_addressable,
            include_recent=args.include_recent,
        )
        _emit(rows)



# --- Additional Python functions ---


def update_bpc_metadata(slug: str, data: dict, session: str,
                        dry_run: bool = False):
    """Update bpc_metadata for a slug. data keys validated against _BPC_META_COLS."""
    _validate_cols(data.keys(), _BPC_META_COLS, "update_bpc_metadata")
    u = _upd(session)
    with connect(dry_run) as conn:
        exists = conn.execute(
            "SELECT 1 FROM bpc_metadata WHERE slug=?", [slug]
        ).fetchone()
        if exists:
            sets = ", ".join(f"{k}=?" for k in data)
            conn.execute(
                f"UPDATE bpc_metadata SET {sets}, "
                "updated_at=?, updated_by_session=? WHERE slug=?",
                [*data.values(), u["updated_at"], u["updated_by_session"], slug]
            )
        else:
            row = {"slug": slug, **data, **audit(session)}
            cols = ", ".join(row)
            ph = ", ".join(["?"] * len(row))
            conn.execute(
                f"INSERT INTO bpc_metadata ({cols}) VALUES ({ph})",
                list(row.values())
            )


def parse_author_flags(flags: list[str]) -> list[dict]:
    """Turn repeated --author values into evidence_source_authors rows, in byline order.

    'Payne|Sarah R.'                 -> person, last_name='Payne', first_name='Sarah R.'
    'corp|World Health Organization' -> corporate author
    A surname alone is allowed; a given name alone is not, because position in the
    byline is what a citation renders and a nameless surname cannot be rendered.
    """
    out = []
    for i, raw in enumerate(flags, start=1):
        part = (raw or "").strip()
        if not part:
            raise Refusal("--author was given an empty value")
        if "|" in part:
            head, tail = part.split("|", 1)
        else:
            head, tail = part, ""
        head, tail = head.strip(), tail.strip()
        if head.lower() in ("corp", "corporate"):
            if not tail:
                raise Refusal(f"--author {raw!r}: corporate author has no name")
            out.append({"position": i, "is_corporate": 1, "corporate_name": tail,
                        "last_name": None, "first_name": None})
        else:
            if not head:
                raise Refusal(f"--author {raw!r}: no surname. Give 'Last|Given'.")
            out.append({"position": i, "is_corporate": 0, "corporate_name": None,
                        "last_name": head, "first_name": tail or None})
    return out


# A display part is a surname (which may be hyphenated, accented or multi-word, as in
# 'van der Meer') followed by initials: 'Payne S', 'Rosas-Perez C', 'MARKUSSEN A'.
# The initials group is capped at three letters DELIBERATELY. Uncapped, it swallowed a
# genuine multi-word uppercase surname: 'SENTOP DUMEN' parsed as surname 'SENTOP' with
# initials 'DUMEN', silently inventing a name split. Three initials is already generous,
# and anything past it is refused into --author rather than guessed at.
_DISPLAY_PART = re.compile(
    r"^(?P<last>.+?)\s+(?P<initials>[A-Z](?:[.\-]?[A-Z]){0,2}\.?)$")


def parse_author_display(display: str) -> list[dict]:
    """Parse the "Last I; Last I" display form back into author rows.

    THIS REFUSES RATHER THAN GUESSES, and that is the point. The display form is lossy:
    it holds initials where the row holds a given name, so a part it cannot split into
    surname + initials is not approximated. On 2026-08-19 five sources in this repository
    were stored with invented co-authors and passed six gates (CLAUDE.md §2(c)); a parser
    that filled in a plausible reading would be the same failure with a smaller blast
    radius. Use --author, which needs no parsing, for anything this rejects.

    What is stored: first_name holds exactly the initials supplied and nothing more. It
    is not expanded into a given name, because the display form does not contain one.
    """
    rows, bad = [], []
    parts = [p.strip() for p in (display or "").split(";")]
    parts = [p for p in parts if p]
    if not parts:
        raise Refusal("--authors is empty")
    for i, part in enumerate(parts, start=1):
        m = _DISPLAY_PART.match(part)
        if m:
            rows.append({"position": i, "is_corporate": 0, "corporate_name": None,
                         "last_name": m.group("last").strip(),
                         "first_name": m.group("initials").strip()})
        else:
            bad.append(part)
    if bad:
        raise Refusal(
            "--authors could not be parsed without guessing: "
            + "; ".join(repr(b) for b in bad)
            + ". Each part must be a surname followed by initials ('Payne S'). "
              "For a corporate author or a full given name use the repeatable "
              "--author flag: --author 'corp|World Health Organization', "
              "--author 'Payne|Sarah R.'. Nothing was written.")
    return rows


def insert_evidence_source(data: dict, session: str,
                           dry_run: bool = False,
                           authors: list[dict] | None = None,
                           conn=None) -> str:
    """Insert a new evidence source and its author rows. Returns ref_id.

    `authors` is a list of evidence_source_authors rows, from parse_author_flags or
    parse_author_display. It is written in the SAME transaction as the source, so a
    source can never exist without the authors it was filed with.

    `conn`, when given, is a write transaction the caller owns (see _txn): the rows
    land in it and commit or roll back with whatever else the caller writes there.
    """
    # Map legacy logical field names to the real evidence_sources columns and drop
    # doi_less_key (no such column in the current schema). Without this the CLI crashed
    # with "table evidence_sources has no column named authors" (audit F-17, 2026-06-22).
    _LEGACY = {"year": "pub_year", "title": "pub_title"}
    data = {_LEGACY.get(k, k): v for k, v in data.items() if k != "doi_less_key"}

    # `authors` USED TO MAP TO author_display HERE, and that was the whole defect.
    # This writer could set the derived display string and had no way to write
    # evidence_source_authors at all, so the documented filing path populated the copy
    # and left the source of truth empty. Migration 063 writer-retires the copy; refuse
    # it explicitly rather than let a caller quietly write a column nothing reads.
    _DERIVED_AUTHOR_COPIES = ("author_display", "authors", "first_author_last",
                              "first_author_first", "author_count", "is_corporate_primary")
    _given = [c for c in _DERIVED_AUTHOR_COPIES if c in data]
    if _given:
        raise Refusal(
            f"{_given} is/are writer-retired (migration 063). Authors are rows in "
            "evidence_source_authors, derived for display by v_evidence_authors. Pass "
            "the `authors` argument (parse_author_flags / parse_author_display), or on "
            "the CLI use --author / --authors.")
    _ES_COLS = frozenset({
        # ADDED 2026-08-25 (Act 2). CLAUDE.md §4 named url, pages and
        # doi_resolution_outcome as columns `add-source` could not write, which is why
        # a companion hand-written UPDATE was mandatory after every admission -- and
        # DR-2026-08-19 §12.1 step 7 bolds the consequence: "Without
        # doi_resolution_outcome='RESOLVED', every VERIFIED DOI-bearing source fails
        # R10." The hand half of step 7 is where H03/H04/H05 parity was won or lost.
        "url", "url_accessed", "pages", "doi_resolution_outcome",
        "ref_id", "pub_year", "pub_title", "doi",
        "pmid", "tier", "evidence_type", "jurisdiction", "metadata_quality",
        "verification_status", "co1_provenance", "co1_source_type",
        "synthesis_attribution_required", "notes", "lang_detected",
        "lang_detection_method",
        # D-0157's other three columns. Their absence here was not cosmetic: the
        # CLI could write verification_status='VERIFIED' and nothing else, which
        # is a row with a standing and no evidence of how it was reached. That
        # violates I1 (VERIFIED needs a method) and I2 (VERIFIED needs a recorded
        # attempt) the moment it lands — both blocking checks. The two scheduled
        # jobs were swept for D-0157; this third writer was not, and it is the
        # one the skills tell sessions to use.
        "verification_disposition", "verification_method",
        "verification_closure_reason", "verification_attempt_count",
        "verification_note", "verified_by_tool",
        # ADDED 2026-09-10, and its absence explains the corpus rather than excusing it.
        # `scope` is the discriminator schemas/tier_derivation.py derives the ratified
        # tier FROM. It was not on this list, so the sanctioned writer COULD NOT WRITE IT
        # — which is why all 9 admitted sources carry scope NULL and adjudication_integrity
        # reports 9 of 9 stored tiers underivable. That was never operator oversight: the
        # only path that was allowed to write a source had no column for the one field the
        # tier is a function of. Sixth time the capture path has been blind to a live
        # column, after evidence_source_authors, source_locators, observed_terms /
        # term_adjudications, terms, and base_parameters.
        "scope",
        # ADDED 2026-09-18 (batch 18), and this is the SEVENTH entry in the list of
        # blindnesses the comments above enumerate -- the sixth is recorded two
        # paragraphs up, in the same block, by an author who was reading it.
        #
        # What exposed it: REF-01005 is a US government research report (HUD-PDR 397,
        # ERIC ED184280). Every field that makes a report CITABLE -- the issuing
        # institution, the report number, the series, the publisher -- was unreachable
        # through the only sanctioned writer, so the row landed with nine
        # payload-supplied fields NULL under `metadata_quality='COMPLETE'`. A
        # bibliography compiled from that row cannot name what the document IS.
        #
        # The owner rule of 2026-09-18 22:55 is the one that forced this rather than a
        # companion UPDATE: "WHEN THE CLI CANNOT REACH A COLUMN, ADD THE VERB -- DO NOT
        # CLAIM THE WRITE HAPPENED." CLAUDE.md section 4 had already said a table the CLI
        # cannot reach is a coverage bug and not a licence to bypass; what the rule adds
        # is the third option, which is writing the claim without the write.
        #
        # grey_flag/grey_reason ride along deliberately. `evidence_type='grey'` and
        # `grey_flag=0` was the state this row landed in, and the two say the same thing
        # in different columns -- so the writer that can set one must be able to set the
        # other, or they drift by construction.
        "source_type", "publisher", "publisher_location", "book_title",
        "series", "series_number", "report_number", "institution",
        "grey_flag", "grey_reason",
    })
    _validate_cols(data.keys(), _ES_COLS, "insert_evidence_source")

    # THE REF_ID MUST BE A GLOBAL REFERENCE ID, and nothing else enforced that.
    # `evidence_sources.ref_id` is a bare TEXT PRIMARY KEY with no CHECK, so
    # `add-source --ref-id RAP-04` inserted silently — and until 2026-08-24 the two
    # skills that document this call told sessions to do exactly that, both writing
    # `--ref-id {local_ref_id}` beside `--local-ref-id {local_ref_id}`.
    #
    # What that costs: a source filed under a per-slug label is invisible to the
    # high-water mark ref_ids are minted above, collides with the
    # next slug that mints the same label, and renders a citation keyed to a string
    # that means nothing outside one slug. It is the copy-versus-pointer confusion that
    # already put RAP-F61/F69/F70 in citation_mining against RAP-06/09/10 in
    # source_slug_links and reported three fully-mined sources UNMINED.
    #
    # Shapes accepted: REF-NNNNN (924 live), REF-VERIFIED-NNN (11 live, human-verified
    # standards predating the DOI pipeline), Co1-NN/NNN (schemas/evidence_source.py).
    rid = str(data.get("ref_id", ""))
    if not re.fullmatch(r"REF-\d{5}|REF-VERIFIED-\d{3}|Co1-\d{2,3}", rid):
        hint = ""
        if re.fullmatch(r"[A-Z]{2,6}-[A-Z]?\d{1,4}", rid):
            hint = (f" {rid!r} looks like a per-slug LOCAL label, which belongs in "
                    f"--local-ref-id, not --ref-id. They are different values: the "
                    f"global id is unique across the repository, the label is "
                    f"meaningful only inside one slug.")
        raise Refusal(
            f"--ref-id {rid!r} is not a global reference id.{hint} Expected REF-NNNNN "
            f"(or REF-VERIFIED-NNN / Co1-NN). Get the next one from "
            f"`db.py next-id ref` (added 2026-09-10 — this message named the Python "
            f"function for months while no command existed), which computes the high-water mark as the "
            f"UNION of every table holding a ref_id. Nothing was written.")

    # THE DECLARED JURISDICTION VOCABULARY (I7, 2026-10-01). Before this the column took
    # any string, and the blocking jurisdiction_db_vocabulary audit found it afterwards.
    dbcore.check_jurisdiction(data.get("jurisdiction"), "add-source --jurisdiction")

    # A verification standing implies its evidence — so REFUSE the write when the
    # evidence is absent. Do not fill it in.
    #
    # The first version of this defaulted verification_method='tool' and
    # attempt_count=1 for any VERIFIED row, reasoning that it was avoiding a row
    # the blocking invariants reject. It did the opposite twice over: `tool`
    # carries the contract "verified_by_tool names which", so the row failed I4b
    # anyway — and, worse, the defaults were INVENTED FACTS. No tool ran; no
    # attempt happened. A write path that manufactures an audit trail to satisfy
    # an audit is a doctrine violation in a project whose stated epistemics are
    # "I don't know" over invention, and it would have laundered fabricated
    # provenance into the one column that exists to record how a standing was
    # reached. Refusal is symmetrical with the R9 duplicate errors below.
    vs = data.get("verification_status")
    if vs == "VERIFIED":
        if not data.get("verification_method"):
            raise Refusal(
                "VERIFIED requires --verification-method (how it was established: "
                "tool / corroborated-not-retrieved / co1-attestation / "
                "citing-bibliography). D-0157: a standing without its method is "
                "not a standing. Filing it as UNVERIFIED with disposition OPEN is "
                "the honest move if you have not established it.")
        if data["verification_method"] == "tool" and not data.get("verified_by_tool"):
            raise Refusal(
                "verification_method='tool' requires --verified-by-tool naming "
                "which tool established it (invariant I4b).")
        data.setdefault("verification_attempt_count", 1)
        # D-0157 invariant I1: "verification is finished or it did not happen."
        # insert_source set OPEN unconditionally, so EVERY verified source it wrote
        # failed I1 the moment anything looked. That went unnoticed while
        # evidence_sources held 0 rows and I1 was vacuous; this batch is the first to
        # repopulate it, and all nine rows failed together. A default that no row can
        # satisfy is not a default, it is a trap.
        data.setdefault("verification_disposition", "CLOSED")
    elif vs == "UNVERIFIED":
        data.setdefault("verification_disposition", "OPEN")
        data.setdefault("verification_attempt_count", 1)

    row = {**data, **audit(session)}
    with _txn(conn, dry_run) as conn:
        # NOT `INSERT OR IGNORE`. That silently no-opped on a colliding ref_id
        # and still returned the ref_id as though the write had happened — so a
        # session could file a source, be told it succeeded, and have written
        # nothing. R9 says pre-check the DOI and cross-file an existing ref_id
        # rather than duplicating; a silent no-op is neither.
        existing = conn.execute(
            "SELECT ref_id FROM evidence_sources WHERE ref_id = ?",
            [data["ref_id"]]).fetchone()
        if existing:
            raise Refusal(
                f"{data['ref_id']} already exists. R9: cross-file the existing "
                f"ref_id rather than duplicating. To amend it, ship a migration.")
        if data.get("doi"):
            # THE DUPLICATE-IDENTITY REFUSAL, case-folded and cross-filed against BOTH
            # ref_id homes. Measured 2026-09-13 (REF-00784's DOI): this compared
            # `doi = ?` on the RAW argument, so a case-variant DOI -- `= upper(doi)`
            # matches 0 rows, `lower()=lower()` matches 1 -- passed the check as a new
            # DOI and filed a duplicate, exactly the identity split dbcore.norm_doi's
            # own docstring warns about ("stored as two ... case-folded they match; to
            # `=` they do not"). It also queried evidence_sources alone, so a DOI
            # already staged in the clue store (source_locators, via add-locator) was
            # invisible here -- and a promotion (the SAME ref_id being inserted here
            # after add-locator staged it) must not trip on its own locator row, which
            # is what the `ref_id<>?` exclusion is for. insert_locator (add-locator,
            # below) already gets this right; this copies that shape rather than
            # inventing a second one.
            doi = dbcore.norm_doi(data["doi"])
            # A RETIRED LOCATOR IS A TOMBSTONE, NOT A FILING, and the exemption is the
            # exact analogue of `superseded_by_ref_id` on the row above: neither row is a
            # live claim on the DOI, so neither can be the "existing ref_id" this refusal
            # tells the caller to cross-file to. Migration 076 retains the thirteen refs
            # the 2026-09-13 clear deleted as RETIRED `source_locators` rows precisely so
            # their ids are never reissued; without this clause, cross-filing to one is
            # both the only route this refusal offers AND the one thing 076 forbids, so
            # the re-run that same ruling ordered cannot admit a single cleared source.
            # Found by batch 08 on REF-00973/REF-00974 (`research_batch_dod.py` R9a carried
            # the identical hole and is fixed in the same commit).
            for table, extra in (
                ("evidence_sources", "AND COALESCE(superseded_by_ref_id,'') = ''"),
                ("source_locators", "AND COALESCE(status,'') <> 'RETIRED'"),
            ):
                dupe = conn.execute(
                    'SELECT ref_id FROM "%s" WHERE LOWER(TRIM(doi))=? AND ref_id<>? %s'
                    % (table, extra),
                    (doi, data["ref_id"])).fetchone()
                if dupe:
                    raise Refusal(
                        f"DOI {data['doi']!r} is already filed as {dupe[0]} in {table} "
                        f"({R9_REMEDY}). Link "
                        f"that ref_id to your slug instead. Nothing was written.")
        cols = ", ".join(row)
        ph = ", ".join(["?"] * len(row))
        conn.execute(
            f"INSERT INTO evidence_sources ({cols}) VALUES ({ph})",
            list(row.values())
        )
        # A source with no authors renders as a blank byline everywhere, and the
        # display column that used to paper over that is gone. Refuse the write.
        if not authors:
            raise Refusal(
                f"{data['ref_id']}: no authors given. Every source needs its authors "
                f"as rows (--author / --authors); there is no display column to write "
                f"instead. If the work genuinely has no named author, file the issuing "
                f"body as a corporate author: --author 'corp|<name>'.")
        stamp = audit(session)
        for a in authors:
            conn.execute(
                "INSERT INTO evidence_source_authors "
                "(ref_id, position, last_name, first_name, is_corporate, "
                " corporate_name, role, created_at, created_by_session) "
                "VALUES (?,?,?,?,?,?,'author',?,?)",
                [data["ref_id"], a["position"], a.get("last_name"), a.get("first_name"),
                 a.get("is_corporate", 0), a.get("corporate_name"),
                 stamp["created_at"], stamp["created_by_session"]])
    return data["ref_id"]


# Fields `correct-source` can rewrite. The boundary is not a taste judgement: it is
# EXACTLY what retrieval_log --verify-authors can prove against a payload. A field the
# verifier cannot check is a field this writer must not touch, or the repository gains
# a way to assert a bibliographic value that nothing can ever contradict.
def _correctable():
    """The payload-backed columns, DERIVED from the verifier's own map.

    Not a second list. `_BIBLIO_FIELDS` in retrieval_log is what --verify-authors can
    actually prove against a payload, and this dict's contract is to be exactly that set
    -- so it is that set, plus `pub_title`, which the verifier checks through `_TITLE_COLS`
    instead (a non-English source stores its native title in pub_title and the English in
    pub_title_en, so the verifier compares a SET of columns where this writer targets one).
    That exception is stated here rather than left implicit.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent / "research"))
    import retrieval_log                                              # noqa: E402
    out = {"pub_title": lambda m: next((t for t in (m.get("title") or []) if t), None)}
    out.update(dict(retrieval_log.PAYLOAD_FIELDS))
    return out


_CORRECTABLE = _correctable()


def _payload_for(ref_id, doi, log_session):
    """The logged payload for one DOI, or a refusal explaining what is missing."""
    sys.path.insert(0, str(Path(__file__).resolve().parent / "research"))
    import retrieval_log                                              # noqa: E402
    payloads = retrieval_log._logged_payloads(log_session)
    if not payloads:
        raise Refusal(
            f"{ref_id}: no retrieval log for session {log_session!r}. A correction is "
            f"only as good as the bytes behind it; re-retrieve first (R10).")
    msg = retrieval_log._index_by_doi(payloads).get((doi or "").lower())
    if msg is None:
        raise Refusal(
            f"{ref_id}: nothing logged for DOI {doi!r} in session {log_session!r}. "
            f"This writer cannot be told a value, only shown one — re-retrieve the "
            f"locator so there is a payload to read (R10).")
    return msg


def correct_source(ref_id: str, fields: list, session: str, log_session: str,
                   dry_run: bool = False):
    """Rewrite bibliographic fields from the LOGGED PAYLOAD, never from an argument.

    There is deliberately no way to pass a value. On 2026-09-02 three bibliographic
    fields in this batch were wrong in the same direction — REF-00976 stored a title
    and a co-author's given name that no payload asserted, and REF-00973 stored a
    title bent toward the slug it was admitted for ('... During Manual Wheelchair
    Propulsion on Different Slopes' for a paper actually subtitled 'A Study of Manual
    Wheelchair Propulsion'). Every one of them was typed by a writer who had the
    payload on disk.

    A `--title` flag here would rebuild that hole one level up. So the argument names
    WHICH field to take from the payload, and the payload supplies WHAT. Fabricating a
    bibliographic field through this path requires forging the retrieval log first.
    """
    unknown = [f for f in fields if f not in _CORRECTABLE and f != "authors"]
    if unknown:
        raise Refusal(
            f"{ref_id}: cannot correct {', '.join(unknown)} — this writer rewrites only "
            f"fields retrieval_log --verify-authors can prove: "
            f"{', '.join(sorted(_CORRECTABLE))}, authors.")
    with connect(dry_run) as conn:
        row = conn.execute(
            "SELECT ref_id, doi FROM evidence_sources WHERE ref_id=?", [ref_id]).fetchone()
        if row is None:
            raise Refusal(f"{ref_id}: no such evidence source.")
        if not row["doi"]:
            raise Refusal(
                f"{ref_id}: no DOI, so no payload can be keyed to it. Corrections to a "
                f"DOI-less source have no byte-level authority and are refused here.")
        msg = _payload_for(ref_id, row["doi"], log_session)
        stamp = audit(session)
        changed = []

        for f in [x for x in fields if x != "authors"]:
            want = _CORRECTABLE[f](msg)
            if want in (None, ""):
                raise Refusal(
                    f"{ref_id}: the payload states nothing for {f!r}. A silence is not a "
                    f"correction — leave the column NULL rather than inventing one.")
            have = conn.execute(
                f"SELECT {f} FROM evidence_sources WHERE ref_id=?", [ref_id]).fetchone()[0]
            if str(have or "").strip() == str(want).strip():
                continue
            conn.execute(f"UPDATE evidence_sources SET {f}=?, updated_at=?, "
                         f"updated_by_session=? WHERE ref_id=?",
                         [want, stamp["created_at"], stamp["created_by_session"], ref_id])
            changed.append({"field": f, "was": have, "now": want})

        if "authors" in fields:
            real = [a for a in (msg.get("author") or []) if isinstance(a, dict)]
            if not real:
                raise Refusal(
                    f"{ref_id}: the payload names no authors. Refusing to empty the "
                    f"byline on the strength of a payload that simply does not say.")
            was = [f"{r['last_name']}, {r['first_name'] or ''}".strip(", ") for r in
                   conn.execute("SELECT last_name, first_name FROM evidence_source_authors "
                                "WHERE ref_id=? ORDER BY position", [ref_id])]
            conn.execute("DELETE FROM evidence_source_authors WHERE ref_id=?", [ref_id])
            for i, a in enumerate(real, start=1):
                fam = (a.get("family") or "").strip()
                giv = (a.get("given") or "").strip() or None
                corp = 1 if not fam else 0
                conn.execute(
                    "INSERT INTO evidence_source_authors "
                    "(ref_id, position, last_name, first_name, is_corporate, "
                    " corporate_name, role, created_at, created_by_session) "
                    "VALUES (?,?,?,?,?,?,'author',?,?)",
                    [ref_id, i, fam or None, giv, corp,
                     (a.get("name") or "").strip() or None if corp else None,
                     stamp["created_at"], stamp["created_by_session"]])
            now = [f"{(a.get('family') or a.get('name') or '')}, {a.get('given') or ''}"
                   .strip(", ") for a in real]
            if was != now:
                changed.append({"field": "authors", "was": "; ".join(was),
                                "now": "; ".join(now)})
            conn.execute("UPDATE evidence_sources SET updated_at=?, updated_by_session=? "
                         "WHERE ref_id=?",
                         [stamp["created_at"], stamp["created_by_session"], ref_id])
        return changed


def amend_search(exec_id: int, note: str, session: str, dry_run: bool = False,
                 set_harm_finding: bool = False,
                 set_target_evidence_type: str = None,
                 set_origin: str = None, set_mined_ref_id: str = None,
                 set_origin_pass_id: int = None, add_result_artefacts=None,
                 clear_target: bool = False):
    """APPEND a correction to a logged search's findings_note. Never rewrite it.

    --clear-target (2026-09-27, exec 77 / DR-2026-09-26 5.2d). --set-origin's own
    refusal below requires target_tier/target_evidence_type/target_scope to be NULL
    before an origin can move off 'planned' -- correctly, per OQ-7 (R1: no) -- but
    until now nothing could NULL them: --set-target-evidence-type only ever swaps one
    declared value for another. That left a ratified correction unexecutable through
    the CLI, which CLAUDE.md names as a coverage bug to fix, not a licence to hand-write
    SQL. Clears all three together, because the refusal tests them as a group ("a
    lookup targets no tier") and a partial clear would leave the row in the same
    refused state. Combinable with --set-origin in one call: the refusal below reads
    the EFFECTIVE post-clear values, not the stale pre-call row, so
    `--clear-target --set-origin incidental` in one call is how a lookup is corrected --
    there is no ordering in which two separate calls would both succeed.

    R8 makes search_executions an append-only log: a query is logged verbatim before
    screening and empties are kept, so no writer may edit what a search recorded at
    the time. But a note can be WRONG, and leaving a wrong one standing is worse than
    the rule it protects. On 2026-09-02 exec 34 recorded that the Euan's Guide Access
    Survey is "predominantly information provision, toilets and staff attitude rather
    than circulation geometry" — a characterisation written from a 404 page, and false
    on the actual report, whose most-cited barrier is "could not get around the venue
    (lack of lifts, narrow corridors, too little space or poor layout)" at 56%. That
    sentence was the whole reason the batch's one disability-led source was not
    admitted, and until now nothing in the CLI could correct it.

    So: append, with a dated marker, in the '|| CORRECTED <date>:' form the record
    already uses. The original text is never touched, which is what R8 protects, and
    the next reader sees both what was believed and what was established.
    """
    note = (note or "").strip()
    if not note:
        raise Refusal(f"exec {exec_id}: refusing to append an empty amendment.")
    with connect(dry_run) as conn:
        row = conn.execute("SELECT exec_id, findings_note, harm_finding, "
                           "target_evidence_type, mining_direction, origin, "
                           "mined_ref_id, origin_pass_id, query_text, "
                           "target_tier, target_scope "
                           "FROM search_executions WHERE exec_id=?", [exec_id]).fetchone()
        if row is None:
            raise Refusal(f"exec {exec_id}: no such search execution.")
        stamp = audit(session)
        marker = f" || CORRECTED {stamp['created_at'][:10]}: "
        any_setter = (set_harm_finding or set_target_evidence_type or set_origin
                     or set_mined_ref_id or set_origin_pass_id is not None
                     or add_result_artefacts or clear_target)
        duplicate = note in (row["findings_note"] or "")
        if duplicate and not any_setter:
            return {"exec_id": exec_id, "appended": False,
                    "reason": "this amendment is already on the row"}
        merged = row["findings_note"] or ""
        if not duplicate:
            merged = merged.rstrip() + marker + note
            conn.execute("UPDATE search_executions SET findings_note=? WHERE exec_id=?",
                         [merged, exec_id])

        # Effective target_* values AFTER this call, used by --set-origin's refusal
        # below instead of the stale pre-call `row` -- so --clear-target and
        # --set-origin combine in one call rather than deadlocking across two.
        eff_target_tier = row["target_tier"]
        eff_target_evidence_type = row["target_evidence_type"]
        eff_target_scope = row["target_scope"]
        cleared = None
        if clear_target:
            if set_target_evidence_type:
                raise Refusal(
                    f"exec {exec_id}: --clear-target and --set-target-evidence-type "
                    f"together -- clear removes the value, set retypes it. Pick one.")
            was = (row["target_tier"], row["target_evidence_type"], row["target_scope"])
            if was == (None, None, None):
                raise Refusal(
                    f"exec {exec_id}: target_tier/target_evidence_type/target_scope "
                    f"are already NULL. Nothing to clear.")
            conn.execute(
                "UPDATE search_executions SET target_tier=NULL, "
                "target_evidence_type=NULL, target_scope=NULL WHERE exec_id=?",
                [exec_id])
            trail = (f"{marker}target_tier {was[0]!r} -> NULL, target_evidence_type "
                     f"{was[1]!r} -> NULL, target_scope {was[2]!r} -> NULL (a lookup "
                     f"targets no tier; the replaced values are kept here because the "
                     f"columns no longer hold them)")
            conn.execute("UPDATE search_executions SET findings_note=? WHERE exec_id=?",
                         [(merged or "").rstrip() + trail, exec_id])
            merged = (merged or "").rstrip() + trail
            eff_target_tier = eff_target_evidence_type = eff_target_scope = None
            cleared = {"was_target_tier": was[0], "was_target_evidence_type": was[1],
                      "was_target_scope": was[2]}

        retyped = None
        if set_target_evidence_type:
            # The vocabulary comes from the column's own CHECK, never a list here
            # (CLAUDE.md rule 8). check_declared raises with the live set on a bad value.
            dbcore.check_declared(conn, "search_executions", "target_evidence_type",
                                  set_target_evidence_type, f"exec {exec_id}")
            was = row["target_evidence_type"]
            if was == set_target_evidence_type:
                raise Refusal(
                    f"exec {exec_id}: target_evidence_type is already "
                    f"{set_target_evidence_type!r}. Nothing to correct.")
            conn.execute("UPDATE search_executions SET target_evidence_type=? "
                         "WHERE exec_id=?", [set_target_evidence_type, exec_id])
            trail = (f"{marker}target_evidence_type {was!r} -> "
                     f"{set_target_evidence_type!r} (misclassification corrected; the "
                     f"replaced value is kept here because the column no longer holds it)")
            conn.execute("UPDATE search_executions SET findings_note=? WHERE exec_id=?",
                         [(merged or "").rstrip() + trail, exec_id])
            merged = (merged or "").rstrip() + trail
            retyped = {"was": was, "now": set_target_evidence_type}

        origin_set = None
        if set_origin:
            # RC5 (DR-2026-09-26 5.2d). `--set-origin adversarial-pass` is accepted
            # here with no pass id -- unlike log-search's hard requirement -- because
            # history can predate adversarial_passes entirely (exec 100, batch 19's
            # own pass). --append-note is already required on every call and carries
            # the warrant; nothing here can verify prose for truth (CLAUDE.md 5(b)).
            dbcore.check_declared(conn, "search_executions", "origin", set_origin,
                                  f"exec {exec_id}")
            was = row["origin"]
            if was == set_origin:
                raise Refusal(f"exec {exec_id}: origin is already {set_origin!r}. "
                              f"Nothing to correct.")
            # THE SAME REFUSAL log-search MAKES AT INSERT, applied to history too --
            # without it, `--set-origin incidental` silently pulls a row with a live
            # target_tier/target_evidence_type/target_scope out of v_coverage_branch's
            # Co-1 count after the fact, which is exactly what OQ-7 (R1: no) exists to
            # prevent (2026-09-27 ruling). Reads the EFFECTIVE post-clear values (a
            # same-call --clear-target already nulled them above), not the stale
            # pre-call `row` -- see --clear-target's docstring note.
            if (set_origin != "planned"
                    and (eff_target_tier or eff_target_evidence_type
                         or eff_target_scope)):
                raise Refusal(
                    f"exec {exec_id}: --set-origin {set_origin} on a row carrying "
                    f"target_tier/target_evidence_type/target_scope. A lookup targets "
                    f"no tier; correct those first (--clear-target), or this row is "
                    f"not a lookup.")
            conn.execute("UPDATE search_executions SET origin=? WHERE exec_id=?",
                         [set_origin, exec_id])
            trail = f"{marker}origin {was!r} -> {set_origin!r}"
            conn.execute("UPDATE search_executions SET findings_note=? WHERE exec_id=?",
                         [(merged or "").rstrip() + trail, exec_id])
            merged = (merged or "").rstrip() + trail
            origin_set = {"was": was, "now": set_origin}

        mined_ref_set = None
        if set_mined_ref_id:
            if (row["mining_direction"] or "none") == "none":
                raise Refusal(
                    f"exec {exec_id}: --set-mined-ref-id with mining_direction "
                    f"{row['mining_direction'] or 'none'!r}. A mined source with no "
                    f"mining direction is incoherent.")
            if row["mined_ref_id"] is not None:
                raise Refusal(
                    f"exec {exec_id}: mined_ref_id is already {row['mined_ref_id']!r}. "
                    f"Only NULL -> a value is a correction; a different value already "
                    f"set needs a new exec.")
            if not conn.execute("SELECT 1 FROM evidence_sources WHERE ref_id=?",
                                [set_mined_ref_id]).fetchone():
                raise Refusal(
                    f"exec {exec_id}: --set-mined-ref-id {set_mined_ref_id} is not in "
                    f"evidence_sources.")
            conn.execute("UPDATE search_executions SET mined_ref_id=? WHERE exec_id=?",
                         [set_mined_ref_id, exec_id])
            trail = f"{marker}mined_ref_id set to {set_mined_ref_id!r}"
            conn.execute("UPDATE search_executions SET findings_note=? WHERE exec_id=?",
                         [(merged or "").rstrip() + trail, exec_id])
            merged = (merged or "").rstrip() + trail
            mined_ref_set = set_mined_ref_id

        origin_pass_set = None
        if set_origin_pass_id is not None:
            if row["origin_pass_id"] is not None:
                raise Refusal(
                    f"exec {exec_id}: origin_pass_id is already "
                    f"{row['origin_pass_id']}. Only NULL -> a value is a correction.")
            if not conn.execute("SELECT 1 FROM adversarial_passes WHERE pass_id=?",
                                [set_origin_pass_id]).fetchone():
                raise Refusal(
                    f"exec {exec_id}: --set-origin-pass-id {set_origin_pass_id} is "
                    f"not in adversarial_passes.")
            effective_origin = set_origin or row["origin"]
            if effective_origin != "adversarial-pass":
                raise Refusal(
                    f"exec {exec_id}: --set-origin-pass-id with origin "
                    f"{effective_origin!r}. The CHECK permits a pass id only with "
                    f"origin='adversarial-pass' -- pass --set-origin too.")
            conn.execute("UPDATE search_executions SET origin_pass_id=? WHERE exec_id=?",
                         [set_origin_pass_id, exec_id])
            trail = f"{marker}origin_pass_id set to {set_origin_pass_id}"
            conn.execute("UPDATE search_executions SET findings_note=? WHERE exec_id=?",
                         [(merged or "").rstrip() + trail, exec_id])
            merged = (merged or "").rstrip() + trail
            origin_pass_set = set_origin_pass_id

        if add_result_artefacts:
            # RC1 (DR-2026-09-26 2.2b). History, or a payload fetched after logging.
            # --append-note (required on every call) is the warrant; the link itself
            # is appended to findings_note, matching every other setter's trail.
            effective_mined_ref = (set_mined_ref_id if set_mined_ref_id is not None
                                   else row["mined_ref_id"])
            _link_result_artefacts(conn, exec_id, add_result_artefacts,
                                   mined_ref_id=effective_mined_ref,
                                   query_text=row["query_text"],
                                   session=session, ts=stamp["created_at"])
            trail = f"{marker}result artefact(s) added: {', '.join(add_result_artefacts)}"
            conn.execute("UPDATE search_executions SET findings_note=? WHERE exec_id=?",
                         [(merged or "").rstrip() + trail, exec_id])
            merged = (merged or "").rstrip() + trail

        raised = False
        if set_harm_finding:
            # MONOTONIC, 0 -> 1 ONLY. R7 makes failure, harm and inadequacy first-class
            # evidence rather than a by-product, so a search that turned some up and was
            # logged with the flag down has an INCOMPLETE record, not a historical one --
            # completing it is not rewriting what the search found. Lowering the flag
            # would be, and is refused: that would erase a harm finding.
            if row["harm_finding"]:
                raise Refusal(
                    f"exec {exec_id}: harm_finding is already 1. This flag only rises.")
            conn.execute("UPDATE search_executions SET harm_finding=1 WHERE exec_id=?",
                         [exec_id])
            raised = True

        # GAP-053 (DR-2026-09-26 phase 2b, migration 100). Every path that reaches
        # here has written at least the findings_note append above (the early return
        # a few lines up is the only no-op path), so one trailing stamp covers every
        # setter this call ran, rather than repeating it on each of the individual
        # UPDATEs above.
        conn.execute("UPDATE search_executions SET updated_at=?, updated_by_session=? "
                     "WHERE exec_id=?",
                     [stamp["updated_at"], stamp["updated_by_session"], exec_id])
        return {"exec_id": exec_id, "appended": not duplicate, "chars": len(merged),
                "harm_finding_raised": raised, "target_evidence_type": retyped,
                "origin": origin_set, "mined_ref_id": mined_ref_set,
                "origin_pass_id": origin_pass_set, "cleared_target": cleared,
                "result_artefacts_added": len(add_result_artefacts or [])}


def amend_gap(gap_id: str, note: str, session: str, dry_run: bool = False):
    """APPEND a dated correction to a gap's description. Never rewrite it.

    `close-gap` moves `status` and nothing else, and the `gaps` table has no
    closure-note column -- so a gap whose DESCRIPTION states something since
    falsified had no repair path at all. Measured on batch 17: GAP-027's text still
    opened "GAP-018 PREDICTOR PASSED ITS FIRST PROSPECTIVE TEST" after GAP-029
    retracted that result as a screen artefact, and GAP-026 still asserted a
    "SafetyLit 503" its own persisted artefact does not hold. A register whose
    entries state retracted findings is worse than one that is merely incomplete:
    the reader who consults it is misled by the document built to prevent that.

    Append-only, in the same '|| CORRECTED <date>:' form `amend-search` uses, for the
    same reason -- what was believed at filing time is part of the record.
    """
    note = (note or "").strip()
    if not note:
        raise Refusal(f"{gap_id}: refusing to append an empty amendment.")
    with connect(dry_run) as conn:
        row = conn.execute("SELECT gap_id, description, status FROM gaps "
                           "WHERE gap_id=?", [gap_id]).fetchone()
        if row is None:
            raise Refusal(f"{gap_id}: no such gap.")
        if note in (row["description"] or ""):
            return {"gap_id": gap_id, "appended": False,
                    "reason": "this amendment is already on the row"}
        stamp = audit(session)
        merged = ((row["description"] or "").rstrip()
                  + f" || CORRECTED {stamp['created_at'][:10]}: " + note)
        conn.execute("UPDATE gaps SET description=?, updated_at=?, updated_by_session=? "
                     "WHERE gap_id=?",
                     [merged, stamp["created_at"], session, gap_id])
        return {"gap_id": gap_id, "appended": True, "status": row["status"],
                "chars": len(merged)}


def reattribute_candidate(candidate_id: int, exec_id: int, reason: str, session: str,
                          dry_run: bool = False, surfaced_in: str = None,
                          surfaced_quote: str = None):
    """Repoint a staged candidate at the search that actually surfaced it.

    `search_candidates.exec_id` is the provenance edge from a candidate back to the
    query that found it, and NOTHING could write it after the insert. Batch 17 staged
    two candidates against exec 71 -- a Co-1 web search whose own note reads ZERO
    YIELD -- when an unlogged Consensus search had produced them, then recorded in a
    committed migration that it had "corrected" the attribution. It had not: no verb
    existed, so the claim was structurally impossible through the sanctioned path and
    was made anyway. CLAUDE.md section 4: a table the CLI cannot reach is a coverage
    bug to fix, not a licence to hand-write SQL.

    The old exec_id is carried into `notes`, so the repointing is itself on the record
    and a reader can see where the candidate was first filed.
    """
    reason = (reason or "").strip()
    if not reason:
        raise Refusal(
            f"candidate {candidate_id}: --reason is required. Moving a provenance edge "
            f"without saying why replaces one unexplained attribution with another.")
    with connect(dry_run) as conn:
        row = conn.execute("SELECT candidate_id, exec_id, notes, locator, surfaced_in "
                           "FROM search_candidates "
                           "WHERE candidate_id=?", [candidate_id]).fetchone()
        if row is None:
            raise Refusal(f"candidate {candidate_id}: no such candidate.")
        if conn.execute("SELECT 1 FROM search_executions WHERE exec_id=?",
                        [exec_id]).fetchone() is None:
            raise Refusal(
                f"exec {exec_id}: no such search execution. A candidate cannot be "
                f"attributed to a search that was never logged -- log it first (R8 "
                f"keeps every query, backfills included).")

        # Computed once and reused at every write site below (GAP-053, migration 100):
        # was two separate `audit(session)` calls, one per branch that could write.
        stamp = audit(session)

        surfaced_set = None
        if surfaced_in:
            # RC1 (DR-2026-09-26 2.2d). Only NULL -> a value is a correction; a value
            # already set is a reattribution and needs a new exec, same discipline as
            # amend-search's --set-mined-ref-id.
            if row["surfaced_in"] is not None:
                raise Refusal(
                    f"candidate {candidate_id}: surfaced_in is already "
                    f"{row['surfaced_in']!r}. Changing a value already set is a "
                    f"reattribution and needs a new exec.")
            _check_surfaced_in(conn, exec_id, surfaced_in, surfaced_quote,
                               row["locator"], "reattribute-candidate")
            # No updated_* stamp here: whichever of the two branches below runs next
            # always fires (same-exec-with-surfaced always writes when surfaced_set is
            # set; the true-reattribution branch is unconditional), and stamps once
            # there. Stamping here too would write the identical value twice per call.
            conn.execute(
                "UPDATE search_candidates SET surfaced_in=?, surfaced_quote=? "
                "WHERE candidate_id=?",
                [surfaced_in, surfaced_quote, candidate_id])
            surfaced_set = {"surfaced_in": surfaced_in, "surfaced_quote": surfaced_quote}

        if row["exec_id"] == exec_id:
            if surfaced_set is not None:
                # --reason is required and validated above; on THIS path (exec_id
                # unchanged) nothing below writes it anywhere, so an earlier version
                # of this function validated it and then discarded it -- the judge's
                # warrant (rule 8) went unrecorded. Carried into notes exactly as the
                # true-reattribution branch below does for its own --reason.
                carried = (f"SURFACED-IN SET {stamp['created_at'][:10]} by {session}: "
                          f"{reason}")
                merged = "\n\n".join([x for x in ((row["notes"] or "").strip() or None,
                                                   carried) if x])
                conn.execute(
                    "UPDATE search_candidates SET notes=?, updated_at=?, "
                    "updated_by_session=? WHERE candidate_id=?",
                    [merged, stamp["updated_at"], stamp["updated_by_session"],
                     candidate_id])
            return {"candidate_id": candidate_id, "changed": False,
                    "exec_id": exec_id, "surfaced": surfaced_set}
        carried = (f"REATTRIBUTED {stamp['created_at'][:10]} from exec "
                   f"{row['exec_id']} to exec {exec_id} by {session}: {reason}")
        merged = "\n\n".join([x for x in ((row["notes"] or "").strip() or None,
                                           carried) if x])
        # search_candidates carries created_at/created_by_session and NO updated_*
        # pair, so the reattribution's date and author live in the carried note -- which
        # is why `carried` above stamps both. Do not "tidy" this into an updated_at:
        # the column does not exist, and adding one to record a repair would be a
        # second home for a fact the note already holds.
        #
        # SUPERSEDED IN PART 2026-09-28 BY OWNER RULING (references/project-standards.md;
        # GAP-053) -- appended, not rewritten, because the paragraph above is why this
        # comment stood for as long as it did and a superseded record is evidence of what
        # was true when. The tidiness objection above is still correct on its own terms:
        # `updated_at`/`updated_by_session` would restate what `carried` already narrates
        # for a HUMAN reader. GAP-053's need is a different one -- a MACHINE reader.
        # `adversarial_pass_audit.py` scopes a session's subject rows by matching every
        # column ending `_by_session` on the RULE's named tables (CLAUDE.md rule 8:
        # derived, not curated), and `search_candidates` carrying only
        # `created_by_session` made every UPDATE this function issues invisible to it --
        # EXAMINED: 0 over rows a session had, in fact, touched. Migration 100 adds the
        # pair; this function now stamps it below, alongside the narrative note, not
        # instead of it. Two homes of the same fact for two different readers is not the
        # drift rule 5 forbids -- both are written by this one call, from this one
        # `stamp`, so they cannot disagree.
        # BY: `The fix folds into phase 2b's tooling PR (DR-2026-09-26 §7) when that lands.`
        conn.execute("UPDATE search_candidates SET exec_id=?, notes=?, updated_at=?, "
                     "updated_by_session=? WHERE candidate_id=?",
                     [exec_id, merged, stamp["updated_at"], stamp["updated_by_session"],
                      candidate_id])
        return {"candidate_id": candidate_id, "changed": True,
                "from_exec": row["exec_id"], "exec_id": exec_id,
                "surfaced": surfaced_set}


_MODEL_SUFFIX_RE = re.compile(r"\[[^\]]*\]$")
_FINDINGS_BLOCK_RE = re.compile(
    r"^[ \t]*```[ \t]*json[ \t]+adversarial-findings[ \t]*\n(.*?)\n[ \t]*```", re.S | re.M)
_HANDBACK_TOOL_NAMES = frozenset({"SubagentHandback"})


def _is_tracked(rel_path: str) -> bool:
    """True iff `rel_path` (repo-relative) is a tracked file at HEAD.

    An untracked transcript is not an artefact (CLAUDE.md rule 6): its entire
    contents live in ephemeral container storage until committed, so a session
    could name a file that a later clone will never see.
    """
    result = subprocess.run(
        ["git", "-C", str(dbcore.REPO_ROOT), "ls-files", "--error-unmatch", rel_path],
        capture_output=True)
    return result.returncode == 0


def _resolve_transcript_path(rel_path: str, label: str) -> tuple:
    """(resolved absolute Path, normalised repo-relative str), confirmed under transcripts/.

    Containment is checked on the RESOLVED path via `dbcore.resolve_under`, never on the
    raw string -- see that function's docstring for the two bypasses this closes.
    """
    resolved = dbcore.resolve_under(dbcore.REPO_ROOT / "transcripts", rel_path)
    if resolved is None:
        raise Refusal(f"{label} {rel_path!r} does not resolve under transcripts/.")
    return resolved, os.path.normpath(rel_path).replace(os.sep, "/")


def _read_transcript(path: Path) -> tuple:
    """(sorted distinct assistant-turn models, the reviewer's final report text), in
    ONE pass over the file -- it is a full session log and can be large, and this used
    to be two separate functions each streaming and json.loads-ing every line.

    MODELS: reads ONLY `message.model` on records whose `type` is `assistant` -- not
    every `"model"` substring in the file, which over-counted an attachment record's
    `claude-opus-5-5[1m]` alongside the real assistant turns in batch 20's own
    transcript. One trailing bracketed suffix (a context-window annotation, not a
    different model) is stripped from each result before it is deduplicated.

    FINAL REPORT: THE LAST PLAIN TEXT BLOCK IS THE WRONG THING TO READ. In this harness
    a subagent's final report is delivered through a `SubagentHandback` TOOL CALL, not
    as trailing assistant prose -- a real reviewer transcript inspected during this
    feature's own adversarial review carried its whole findings report inside a
    `SubagentHandback` tool_use's `input.message`, followed by a separate, shorter
    plain-text turn ("I've sent the full adversarial pass ... back to the orchestrating
    session") that a last-text-block reader would return instead. The LAST
    `SubagentHandback` call in the transcript is preferred; only if none exists does
    this fall back to the last plain text block, for a reviewer run without that tool.
    """
    models = set()
    last_text, last_handback = "", None
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("type") != "assistant":
                continue
            msg = rec.get("message")
            if not isinstance(msg, dict):
                continue
            model = msg.get("model")
            if model:
                models.add(_MODEL_SUFFIX_RE.sub("", model))
            content = msg.get("content")
            if isinstance(content, str):
                last_text = content
            elif isinstance(content, list):
                texts = [b.get("text", "") for b in content
                         if isinstance(b, dict) and b.get("type") == "text"]
                if texts:
                    last_text = "\n".join(texts)
                for b in content:
                    if (isinstance(b, dict) and b.get("type") == "tool_use"
                            and b.get("name") in _HANDBACK_TOOL_NAMES):
                        inp = b.get("input") or {}
                        parts = [v for v in inp.values() if isinstance(v, str)]
                        if parts:
                            last_handback = "\n".join(parts)
    return sorted(models), (last_handback if last_handback is not None else last_text)


def _extract_findings_block(text: str):
    """The parsed JSON array inside a ```json adversarial-findings``` fence, or None.

    See .claude/agents/antagonist.md, "Report shape". The record is derived
    from the reviewer's own words -- this function never fabricates a finding
    the block did not carry.
    """
    m = _FINDINGS_BLOCK_RE.search(text or "")
    if not m:
        return None
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, list) else None


def record_adversarial_pass(subject_session: str, subject_commit: str,
                            reviewer_transcript: str, author_transcript: str,
                            session: str, dry_run: bool = False) -> dict:
    """Record a completed antagonist pass and its findings (RC4).

    The requirement already existed three times -- the 2026-08-19 RULE, DR-2026-09-11
    clause 2, and pipeline-contract.yaml's cross_stage/definition-of-done -- and none of
    the three was enforced: nothing recorded a pass in checkable form, so batch 20's own
    antagonist pass ran the SAME model as its author while its record called it
    independent, and nothing caught that until this writer's own derivation could.

    Refuses: a second pass for the same subject_session (RULE ACTION 5: at most one
    adversarial pass per research batch); a self-administered pass (the two transcripts
    resolve to the same file); a transcript outside `transcripts/` or not tracked; a
    transcript with no assistant-turn model; a reviewer transcript whose final report
    carries no findings block; a SUSTAINED finding with no severity, or a non-SUSTAINED
    finding with one (RULE ACTION 2: severity grades a confirmed defect, and only that).
    Writes one findings row per block entry -- it never retypes a finding by hand.
    """
    if subject_session.endswith(".md"):
        subject_session = subject_session[:-3]
    reviewer_path, reviewer_rel = _resolve_transcript_path(reviewer_transcript,
                                                           "reviewer_transcript")
    author_path, author_rel = _resolve_transcript_path(author_transcript,
                                                       "author_transcript")
    if reviewer_path == author_path:
        raise Refusal(
            "reviewer_transcript and author_transcript resolve to the same file. A "
            "self-administered pass is not a pass -- batch 20 section 0 says this "
            "about its own.")
    for label, rel in (("reviewer_transcript", reviewer_rel), ("author_transcript", author_rel)):
        if not _is_tracked(rel):
            raise Refusal(
                f"{label} {rel!r} is not a tracked file. Commit it first (CLAUDE.md "
                f"rule 6) -- an untracked transcript is not an artefact.")
    reviewer_models, reviewer_text = _read_transcript(reviewer_path)
    author_models, _ = _read_transcript(author_path)
    if not reviewer_models:
        raise Refusal(f"{reviewer_rel}: no assistant turn carries a model.")
    if not author_models:
        raise Refusal(f"{author_rel}: no assistant turn carries a model.")
    findings_block = _extract_findings_block(reviewer_text)
    if findings_block is None:
        raise Refusal(
            f"{reviewer_rel}: the reviewer's final report carries no "
            f"```json adversarial-findings``` block. See .claude/agents/antagonist.md, "
            f"'Report shape'.")
    for i, f in enumerate(findings_block):
        if not isinstance(f, dict):
            raise Refusal(f"findings block entry {i}: not an object.")

    with connect(dry_run) as conn:
        existing = conn.execute(
            "SELECT pass_id FROM adversarial_passes WHERE subject_session=?",
            [subject_session]).fetchone()
        if existing:
            raise Refusal(
                f"a pass already exists for {subject_session} (pass_id "
                f"{existing['pass_id']}). RULE ACTION (5): at most one adversarial pass "
                f"per research batch; a pass on a pass is forbidden.")
        # The allowed key set is DERIVED from the table's own columns, minus the ones
        # a writer stamps or a later verb sets (rule 8: a hand-typed mirror of the
        # schema is exactly the shape this DR's RC2 closes for a value vocabulary; this
        # is the same shape for a column-name set).
        writer_stamped = {"finding_id", "pass_id", "disposition", "disposition_ref",
                          "disposed_by_session", "disposed_at",
                          "created_by_session", "created_at"}
        allowed_finding_cols = frozenset(dbcore.columns(conn, "adversarial_findings")) - writer_stamped
        for i, f in enumerate(findings_block):
            dbcore.validate_cols(f.keys(), allowed_finding_cols, "record-adversarial-pass")
            if not (f.get("claim_attacked") or "").strip():
                raise Refusal(f"findings block entry {i}: claim_attacked is required.")
            if not (f.get("method") or "").strip():
                raise Refusal(f"findings block entry {i}: method is required.")
            verdict, severity = f.get("verdict"), f.get("severity")
            if verdict == "SUSTAINED" and not (severity or "").strip():
                raise Refusal(f"findings block entry {i}: verdict=SUSTAINED requires "
                              f"severity (RULE ACTION 2).")
            if verdict != "SUSTAINED" and severity:
                raise Refusal(f"findings block entry {i}: severity is set but verdict is "
                              f"{verdict!r}, not SUSTAINED -- only a confirmed defect is graded.")
            dbcore.check_declared(conn, "adversarial_findings", "lens", f.get("lens"),
                                  f"findings block entry {i}")
            dbcore.check_declared(conn, "adversarial_findings", "verdict", f.get("verdict"),
                                  f"findings block entry {i}")
            if severity:
                dbcore.check_declared(conn, "adversarial_findings", "severity",
                                      severity, f"findings block entry {i}")
        row = {
            "subject_session": subject_session, "subject_commit": subject_commit,
            "reviewer_transcript": reviewer_rel,
            "reviewer_models": json.dumps(reviewer_models),
            "author_transcript": author_rel,
            "author_models": json.dumps(author_models),
        }
        row.update(dbcore.stamp_for(conn, "adversarial_passes", session))
        cols = ", ".join(row)
        cur = conn.execute(
            f"INSERT INTO adversarial_passes ({cols}) VALUES ({', '.join('?' * len(row))})",
            list(row.values()))
        pass_id = cur.lastrowid
        finding_ids = []
        for f in findings_block:
            frow = {
                "pass_id": pass_id, "lens": f.get("lens"),
                "subject_table": f.get("subject_table"), "subject_key": f.get("subject_key"),
                "claim_attacked": f["claim_attacked"], "method": f["method"],
                "artefact": f.get("artefact"), "verdict": f.get("verdict"),
                "severity": f.get("severity"),
            }
            frow.update(dbcore.stamp_for(conn, "adversarial_findings", session))
            fcols = ", ".join(frow)
            fcur = conn.execute(
                f"INSERT INTO adversarial_findings ({fcols}) VALUES ({', '.join('?' * len(frow))})",
                list(frow.values()))
            finding_ids.append(fcur.lastrowid)
    return {"pass_id": pass_id, "finding_ids": finding_ids,
            "reviewer_models": reviewer_models, "author_models": author_models,
            "same_model": bool(set(reviewer_models) & set(author_models))}


def dispose_adversarial_finding(finding_id: int, disposition: str, ref: str, session: str,
                                reason: str = None, dry_run: bool = False) -> dict:
    """Set a finding's disposition (RC4). Disposition resolves a CONFIRMED defect, so it
    applies only to a SUSTAINED finding, and only once -- a second call is refused rather
    than silently overwriting the first judge's record (CLAUDE.md rule 8: name who judged
    it, permanently, not whoever called last).

    REPAIRED requires `ref` to be an existing data migration path under
    scripts/migrations/. OWNER-RULED requires `ref` of the form
    `references/project-standards.md :: "<verbatim quote>"`, the quote occurring
    exactly once in the ledger's SUBSTANTIVE prose under the RC3 normalisation
    (`dbcore.count_ledger_quote`, excluding SUPERSEDES/BY citation lines) -- the same
    anchor the SUPERSEDES/BY grammar uses. REJECTED and PROVISIONAL-DISPUTED require
    --reason.
    """
    with connect(dry_run) as conn:
        row = conn.execute(
            "SELECT finding_id, verdict, disposition FROM adversarial_findings "
            "WHERE finding_id=?", [finding_id]).fetchone()
        if row is None:
            raise Refusal(f"finding {finding_id}: no such finding.")
        if row["verdict"] != "SUSTAINED":
            raise Refusal(
                f"finding {finding_id}: verdict is {row['verdict']!r}, not SUSTAINED. "
                f"Disposition resolves a confirmed defect; nothing to dispose here.")
        if row["disposition"] is not None:
            raise Refusal(
                f"finding {finding_id}: already disposed as {row['disposition']!r}. "
                f"A disposition is not amended by a second call.")
        dbcore.check_declared(conn, "adversarial_findings", "disposition", disposition,
                              f"finding {finding_id}")
        if disposition == "REPAIRED":
            import migrate_db
            valid = bool(
                ref and ref.startswith("scripts/migrations/")
                and migrate_db.DATA_PATTERN.match(Path(ref).name)
                and (dbcore.REPO_ROOT / ref).exists())
            if not valid:
                raise Refusal(
                    f"finding {finding_id}: disposition=REPAIRED requires --ref to be an "
                    f"existing file under scripts/migrations/ matching "
                    f"migrate_db.DATA_PATTERN; got {ref!r}.")
        elif disposition == "OWNER-RULED":
            m = re.match(r'^references/project-standards\.md :: "(.+)"$', ref or "", re.S)
            if not m:
                raise Refusal(
                    f"finding {finding_id}: disposition=OWNER-RULED requires --ref of the "
                    f"form 'references/project-standards.md :: \"<verbatim quote>\"'.")
            quote = m.group(1)
            text = (dbcore.REPO_ROOT / "references" / "project-standards.md").read_text(
                encoding="utf-8")
            n = dbcore.count_ledger_quote(dbcore.strip_supersedes_citations(text), quote)
            if n != 1:
                raise Refusal(
                    f"finding {finding_id}: the quote occurs {n} time(s) in the ledger's "
                    f"substantive prose (RC3 normalisation, excluding SUPERSEDES citation "
                    f"lines); it must occur exactly once.")
        elif disposition in ("REJECTED", "PROVISIONAL-DISPUTED"):
            reason = dbcore.require_reason(reason, f"finding {finding_id}")
            ref = reason
        stamp = audit(session)
        conn.execute(
            "UPDATE adversarial_findings SET disposition=?, disposition_ref=?, "
            "disposed_by_session=?, disposed_at=? WHERE finding_id=?",
            [disposition, ref, session, stamp["created_at"], finding_id])
        return {"finding_id": finding_id, "disposition": disposition, "disposition_ref": ref,
                "disposed_by_session": session, "disposed_at": stamp["created_at"]}


#: Wrapping punctuation stripped from an artefact token before it is resolved: brackets
#: and list separators from prose ("(and the other 11)", "a.json;"), quotes and the
#: backtick an agent puts round a path. A trailing full stop is stripped separately so a
#: leading "../" keeps its dots and still meets the containment check.
_ARTEFACT_TOKEN_WRAP = "()[]{},;:'\"`"


def _artefact_path_tokens(artefact: str) -> list:
    """The path-shaped tokens of a finding's artefact string: each whitespace-separated
    token containing '/', stripped of wrapping punctuation, de-duplicated in order."""
    out = []
    for tok in (artefact or "").split():
        if "/" not in tok:
            continue
        prev = None
        while tok != prev:          # "`a/b.md`." needs both strips, in either order
            prev = tok
            tok = tok.strip(_ARTEFACT_TOKEN_WRAP).rstrip(".")
        if tok and tok not in out:
            out.append(tok)
    return out


def close_adversarial_pass(pass_id: int, session: str, dry_run: bool = False) -> dict:
    """Close a pass (RC4). Refuses unless every lens has a row, at least one row is
    SURVIVED, every NOT-ATTACKED row's method says why, and every SURVIVED row's
    artefact resolves to at least one existing file under the repo.

    THE ARTEFACT IS PARSED, NOT MATCHED WHOLE (GAP-055). The antagonist brief asks for
    the artefact a claim was attacked WITH, and the antagonist writes it as a citation:
    "<file> page 15", "<file>; <file>", "<file> and the other five". The literal
    single-file check refused every one of those, so a good-faith pass could not close
    and nothing could amend a finding afterwards (the 2026-09-27 ruling forbids building
    that verb). The candidates are the whole string, then each path-shaped token
    (_artefact_path_tokens); one that resolves through dbcore.resolve_under to an
    existing file satisfies the finding. Containment is still checked on the RESOLVED
    path, so "../outside/x" is refused however it is wrapped. Path-shaped tokens that do
    not resolve are returned as `unresolved` (the CLI prints them as REPORTED): one real
    file admits the finding, and the others it cites stay visible rather than vanish.

    THE DATABASE IS NOT AN ARTEFACT OF ATTACK. A token that resolves only inside the
    directory holding the canonical database (dbcore.CANONICAL_DB's parent) proves that a
    file exists, not what a claim was attacked with: "data/guidebook.db <a query>" names
    every finding's subject at once. Such a finding still closes -- refusing it would
    re-open the GAP-055 trap for a good-faith citation -- but it is returned as
    `database_only` and the CLI prints it as REPORTED, so the weakness stays visible.

    PASSES THIS VERB MUST NOT BE USED ON. Pass 1 is held OPEN by the owner ruling of
    2026-09-27 (second, "exec 77 executed ...; further tooling on pass 1 stood down",
    references/project-standards.md), ACTION (2): "Do not build `amend-adversarial-finding`
    or otherwise chase pass 1 closed as its own effort; it stays open." Pass 2 was left
    OPEN by its own session (sessions/session_2026-09-28-research-batch-21-selection.md);
    the process-gap remediation plan the owner approved on 2026-10-01 says not to close it
    either, citing the same ruling -- which names only pass 1.
    Nothing here refuses them: a curated list of pass ids beside the passes table is what
    rule 8 forbids. The operator is the gate, and this is where they are told.
    """
    with connect(dry_run) as conn:
        prow = conn.execute(
            "SELECT pass_id, closed_at FROM adversarial_passes WHERE pass_id=?",
            [pass_id]).fetchone()
        if prow is None:
            raise Refusal(f"pass {pass_id}: no such pass.")
        if prow["closed_at"]:
            raise Refusal(f"pass {pass_id}: already closed at {prow['closed_at']}.")
        findings = conn.execute(
            "SELECT finding_id, lens, verdict, method, artefact FROM adversarial_findings "
            "WHERE pass_id=?", [pass_id]).fetchall()
        all_lenses = dbcore.check_values(conn, "adversarial_findings", "lens")
        missing = sorted(all_lenses - {f["lens"] for f in findings})
        if missing:
            raise Refusal(f"pass {pass_id}: no finding for lens(es) {missing}.")
        if not any(f["verdict"] == "SURVIVED" for f in findings):
            raise Refusal(
                f"pass {pass_id}: no SURVIVED row. A zero-finding pass must be able to "
                f"show what it attacked (2026-08-19 RULE), or it is indistinguishable "
                f"from a pass that never ran.")
        def _is_file(tok):
            p = dbcore.resolve_under(dbcore.REPO_ROOT, tok)
            return p is not None and p.is_file()

        db_dir = dbcore.CANONICAL_DB.resolve().parent

        def _in_db_dir(tok):
            p = dbcore.resolve_under(dbcore.REPO_ROOT, tok)
            return p is not None and db_dir in p.resolve().parents

        unresolved, database_only = {}, {}
        for f in findings:
            if (f["verdict"] == "NOT-ATTACKED"
                    and len((f["method"] or "").strip()) < 10):
                raise Refusal(
                    f"finding {f['finding_id']}: verdict=NOT-ATTACKED but method "
                    f"({f['method']!r}) is too short to say why. A placeholder is not "
                    f"a reason.")
            if f["verdict"] == "SURVIVED":
                artefact = (f["artefact"] or "").strip()
                path_tokens = _artefact_path_tokens(artefact)
                tried = ([artefact] if artefact else []) + [
                    t for t in path_tokens if t != artefact]
                if not any(_is_file(t) for t in tried):
                    raise Refusal(
                        f"finding {f['finding_id']}: verdict=SURVIVED names artefact "
                        f"{artefact!r}, and no candidate resolves to an existing file "
                        f"under the repo. Tried: {tried}. Lead the artefact with one "
                        f"repo-relative path to an existing (committed) file; anything "
                        f"after it is a qualifier.")
                missed = [t for t in path_tokens if not _is_file(t)]
                if missed:
                    unresolved[f["finding_id"]] = missed
                admitting = [t for t in tried if _is_file(t)]
                if admitting and all(_in_db_dir(t) for t in admitting):
                    database_only[f["finding_id"]] = admitting
        stamp = audit(session)
        conn.execute("UPDATE adversarial_passes SET closed_at=? WHERE pass_id=?",
                     [stamp["created_at"], pass_id])
        return {"pass_id": pass_id, "closed_at": stamp["created_at"], "findings": len(findings),
                "unresolved": unresolved, "database_only": database_only}


def _check_rehome_destination(conn, subject: str, suggested_slug, found_under_slug):
    """Refuse a REHOME that does not say, validly, where the candidate belongs.

    A REHOME disposition means "this belongs under another slug", and suggested_slug is
    the only joinable statement of WHICH. Batch 20 (2026-09-25) gave resolve-candidate an
    OPTIONAL --suggested-slug checked only for existence, and a review the next day found
    it closed nothing: REHOME rows could still sit at NULL -- undecided -- or point at
    the slug they were found under, which is not a rehome at all (candidate 117 was in
    exactly that state while its prose said "rehomed"); and a MERGED slug passed a bare
    existence check although _check_slug_filable refuses it everywhere else in this file.
    Derive the legacy rows this now refuses rather than trusting any list:

        select candidate_id, found_under_slug, suggested_slug from search_candidates
         where disposition='REHOME'
           and (suggested_slug is null or suggested_slug = found_under_slug);

    Called by BOTH writers that can set a REHOME -- add-candidate at staging and
    resolve-candidate at resolution -- for the reason _check_slug_filable gives: a guard
    on one verb leaves the other able to create the row it refuses.
    """
    if not suggested_slug:
        raise Refusal(
            f"{subject}: a REHOME must name where the candidate belongs -- pass "
            f"--suggested-slug. A REHOME with no destination is the undecided state the "
            f"disposition exists to end.")
    if suggested_slug == found_under_slug:
        raise Refusal(
            f"{subject}: --suggested-slug {suggested_slug!r} is the slug it was found "
            f"under. A REHOME pointing at its own origin is not a rehome; if it belongs "
            f"where it was found, it is not REHOME.")
    _check_slug_filable(conn, suggested_slug)


def resolve_candidate(candidate_id: int, disposition: str, redescription: str,
                      session: str, admitted_ref_id: str = None, dry_run: bool = False,
                      suggested_slug: str = None, clear_suggested_slug: bool = False):
    """Close a staged candidate by RE-DESCRIBING it from the source (R15).

    R15: "A staged candidate description is a HYPOTHESIS. On resolution, re-describe
    it from the source and CORRECT it if you over-claimed. Do not let your own guess
    harden into fact." Until now nothing in the CLI could do that -- search_candidates
    had an insert and no way to close a row -- so a resolved candidate kept whatever
    was guessed about it when it was staged.

    Candidate 73 is why this exists. Staged from a 404 page, it asserted that the
    Euan's Guide Access Survey has "6000+ respondents in 2023" and that its content
    "skews to information provision, toilets and staff attitude rather than
    circulation". The retrieved report says over 4,400 respondents, and its
    second-most-cited barrier of twelve is inability to get around the venue for want
    of lifts, corridor width, space or layout.

    The hypothesis is APPENDED TO, never overwritten. R15 asks that a guess not harden
    into fact, and the way to guarantee that is to leave the guess legible beside what
    the source actually said -- an overwrite would erase the evidence that anyone
    guessed at all.

    suggested_slug (2026-09-25/26). REHOME REQUIRES a valid destination
    (_check_rehome_destination). On any other disposition --suggested-slug is refused --
    a moved slug riding on a resolution about something else would be an unexplained
    second change -- and --clear-suggested-slug is the one way to empty a stale value
    (say, a REHOME later found OUT-OF-SCOPE): the UPDATE below cannot write NULL through
    a COALESCE, and db.py has no general "clear this field" idiom to borrow. Either move
    is recorded in the RESOLVED line, because the column keeps only the current value.
    """
    redescription = (redescription or "").strip()
    if not redescription:
        raise Refusal(
            f"candidate {candidate_id}: R15 requires a re-description FROM THE SOURCE "
            f"to resolve a candidate. Refusing to close a hypothesis without one.")
    subject = f"candidate {candidate_id}"
    if suggested_slug is not None and clear_suggested_slug:
        raise Refusal(f"{subject}: --suggested-slug and --clear-suggested-slug contradict "
                      f"each other. Pass one.")
    with connect(dry_run) as conn:
        row = conn.execute("SELECT candidate_id, disposition, notes, title, suggested_slug, "
                           "found_under_slug FROM search_candidates WHERE candidate_id=?",
                           [candidate_id]).fetchone()
        if row is None:
            raise Refusal(f"{subject}: no such staged candidate.")
        allowed = dbcore.check_values(conn, "search_candidates", "disposition")
        if allowed and disposition not in allowed:
            raise Refusal(
                f"{subject}: disposition {disposition!r} is not in the "
                f"column's own vocabulary {sorted(allowed)}.")
        if disposition == "REHOME":
            if clear_suggested_slug:
                raise Refusal(
                    f"{subject}: --clear-suggested-slug with REHOME would leave a rehome "
                    f"with no destination. Name the destination with --suggested-slug.")
            _check_rehome_destination(conn, subject, suggested_slug, row["found_under_slug"])
        elif suggested_slug is not None:
            raise Refusal(
                f"{subject}: --suggested-slug is only accepted with --disposition REHOME. "
                f"It names where a rehomed candidate belongs; on any other disposition it "
                f"would be an unexplained second change. To empty a stale value, pass "
                f"--clear-suggested-slug.")
        if disposition == "ADMITTED" and not admitted_ref_id:
            raise Refusal(
                f"{subject}: ADMITTED without --admitted-ref-id names no "
                f"evidence row. Say which source it became.")
        if admitted_ref_id and not conn.execute(
                "SELECT 1 FROM evidence_sources WHERE ref_id=?", [admitted_ref_id]).fetchone():
            raise Refusal(
                f"{subject}: --admitted-ref-id {admitted_ref_id} is not in "
                f"evidence_sources. File the source first.")
        new_slug = (None if clear_suggested_slug
                    else suggested_slug if suggested_slug is not None
                    else row["suggested_slug"])
        detail = "R15, re-described from the source"
        detail += f"; admitted as {admitted_ref_id}" if admitted_ref_id else ""
        if new_slug != row["suggested_slug"]:
            detail += f"; suggested_slug {row['suggested_slug']} -> {new_slug}"
        # THE EDGE GOES IN THE COLUMN. --admitted-ref-id was required for ADMITTED and
        # then written ONLY into the `notes` tail, so the candidate-to-source link
        # existed as prose and nothing could join on it. Migration 088 gives the table
        # `resolved_ref_id`; writing it here is what lets integrity check S01 compare a
        # candidate's exec_id against the exec that actually admitted its source. The
        # line still names it too -- that is the human-readable record, not the edge.
        # search_candidates has no updated_* pair, so the dated, attributed line IS the
        # audit record of the resolution (the literal RESOLVED is R15's predicate).
        #
        # SUPERSEDED IN PART 2026-09-28 BY OWNER RULING (references/project-standards.md;
        # GAP-053) -- appended, not rewritten, per the paragraph immediately above. The
        # pair now exists, for a different reader than the one that paragraph addressed:
        # see reattribute_candidate's own SUPERSEDED note for the full reasoning (same
        # fact, same fix, sibling function). Both the note and the pair are written below,
        # from one stamp, so they cannot disagree.
        # BY: `The fix folds into phase 2b's tooling PR (DR-2026-09-26 §7) when that lands.`
        stamp = dbcore.upd(session)
        conn.execute("UPDATE search_candidates SET disposition=?, notes=?, "
                     "resolved_ref_id=COALESCE(?, resolved_ref_id), suggested_slug=?, "
                     "updated_at=?, updated_by_session=? "
                     "WHERE candidate_id=?",
                     [disposition,
                      dbcore.append_dated_note(row["notes"], "RESOLVED", session,
                                               f"{detail}: {redescription}",
                                               stamp["updated_at"]),
                      admitted_ref_id, new_slug,
                      stamp["updated_at"], stamp["updated_by_session"], candidate_id])
        return {"candidate_id": candidate_id, "was": row["disposition"],
                "now": disposition, "admitted_ref_id": admitted_ref_id,
                "suggested_slug": new_slug}


def _results_admitted_after(was, edges: int, linked: bool) -> int:
    """The results_admitted value after an admission edge is added (linked) or removed.

    WHY THIS WRITES A COLUMN THE 2026-09-02 REPAIR CALLED WRITER-RETIRED. That session
    deleted invariant H05 (test_db_integrity) because enforcing count == edges after the
    fact had CAUSED harm: a retraction emptied search_admissions and, to keep H05 green,
    rewrote seven searches' results_admitted to 0 -- erasing admissions those searches
    really made. Its resolution: log-search sets the count from its edges at insert, and
    "nothing updates it thereafter".

    link-admission and unlink-admission are the first writers of an admission edge on an
    EXISTING search, and leaving the count alone produced the opposite defect: exec 90
    read 0 admitted with 1 edge, exec 91 read 1 with 2, and v_coverage_language /
    _jurisdiction / _branch -- which SUM this column -- under-counted what those
    searches yielded. DR-2026-08-19 step 7 prescribes updating the count in the same
    transaction as the edge.

    THE RULE BELOW IS AN OWNER RULING (2026-09-26, recorded in
    references/project-standards.md and on GAP-051), not a session's compromise. It first
    landed as a reconciliation of the two records above; the owner confirmed it as the
    answer, superseding for post-insert writes both step 7's "must agree exactly" and the
    2026-09-02 repair's "nothing updates it thereafter":

      * never lowered to agree with the edges (the harm): a link gives max(was, edges),
        so the seven restored historical counts -- count above edges, by design -- are
        never touched; an unlink gives max(edges, was - 1), one fewer and never below
        the edges that remain;
      * moved only by an edge this writer itself adds or removes, the same event-driven,
        monotonic completion amend-search applies to harm_finding ("completing an
        incomplete record is not rewriting what the search found").

    The one place the rule lives; its cases are L03, L06 and U03 in
    scripts/tests/test_db_amend_writers.py.
    """
    was = was or 0
    return max(was, edges) if linked else max(edges, was - 1)


def link_admission(exec_id: int, ref_id: str, reason: str, session: str,
                   dry_run: bool = False):
    """Record that an EXISTING search admitted a source, when a resolved candidate says so.

    ADDED 2026-09-25 (batch 20), and it closes a coverage gap rather than adding a new
    kind of fact. `search_admissions` is the one carrier of "which search admitted this
    source", and its only writer was `log-search --admitted-ref-id`, which can only
    attach an admission to a search logged IN THE SAME CALL. A source admitted in a
    later batch from a staged candidate therefore had no sanctioned way to point back at
    the search that surfaced it, and research_protocol_audit reported batch 20's two
    such sources (REF-01007, REF-01008) as admitted by no search at all.

    WHAT THE REFUSAL PROVES, AND WHAT IT DOES NOT (corrected 2026-09-26). It writes the
    edge only when a search_candidates row already records BOTH ends -- that candidate's
    exec_id is this exec, its resolved_ref_id is this source, disposition ADMITTED. That
    stops an attribution nobody recorded. It does NOT establish that the recorded one is
    TRUE. The edge copies the candidate's exec_id, so integrity check S01, which compares
    exactly those two columns, cannot fail on an edge written here: a green S01 over it
    is two tables agreeing about one fact, not a verification of the fact. And
    search_candidates.exec_id has been wrong before -- candidates 107, 108 and 114 (see
    reattribute_candidate). The truth of the edge rests on the session that logged the
    candidate against this search. A wrong edge is removed with unlink-admission. This
    is not hypothetical: both edges batch 20 first wrote with this verb copied proxy
    filings (batch 19 had put candidates 124 and 125 on the nearest logged search because
    the steps that surfaced them were never logged). They were moved on 2026-09-26 --
    backfill the real step, reattribute-candidate, unlink-admission, link-admission --
    and GAP-050 records the chain.

    A SECOND ADMITTING SEARCH IS ALLOWED. The first version refused a source that another
    exec already admitted. log-search refuses no such thing -- a source surfaced by two
    searches is ordinary -- and the refusal pointed at reattribute-candidate, which
    would have falsified which search surfaced it. Removed 2026-09-26.

    The reason and any change to results_admitted are appended to the search's
    findings_note (search_admissions has no column for either); see
    _results_admitted_after for why the count moves at all. Re-running it on an edge that
    already exists writes nothing unless the count is behind the edges, in which case it
    raises the count and records why.
    """
    reason = dbcore.require_reason(
        reason, f"exec {exec_id} -> {ref_id}",
        "A provenance edge written after the fact must say why it was not written when "
        "the search was logged.")
    with connect(dry_run) as conn:
        ref = dbcore.fold_ref(ref_id)
        ex = conn.execute("SELECT exec_id, findings_note, results_admitted "
                          "FROM search_executions WHERE exec_id=?", [exec_id]).fetchone()
        if ex is None:
            raise Refusal(f"exec {exec_id}: no such search execution.")
        if not dbcore.exists(conn, "evidence_sources", "ref_id", ref):
            raise Refusal(f"{ref}: not an admitted source.")
        cand = [r[0] for r in conn.execute(
            "SELECT candidate_id FROM search_candidates WHERE exec_id=? "
            "AND resolved_ref_id=? AND disposition='ADMITTED'", [exec_id, ref])]
        if not cand:
            raise Refusal(
                f"exec {exec_id} -> {ref}: REFUSED. No search_candidates row records that "
                f"this search surfaced a candidate which was admitted as this source "
                f"(exec_id = {exec_id}, resolved_ref_id = {ref}, disposition ADMITTED). An "
                f"admission edge written without that is an attribution nobody recorded -- "
                f"the fabrication research_protocol_audit names. If the search that "
                f"admitted it was never logged, log it with log-search --admitted-ref-id.")
        admitting = [r[0] for r in conn.execute(
            "SELECT exec_id FROM search_admissions WHERE ref_id=?", [ref])]
        stamp = dbcore.now()
        added = exec_id not in admitting
        if added:
            edge = {"exec_id": exec_id, "ref_id": ref}
            edge.update(dbcore.stamp_for(conn, "search_admissions", session))
            conn.execute(f"INSERT INTO search_admissions ({','.join(edge)}) "
                         f"VALUES ({','.join('?' * len(edge))})", list(edge.values()))
        edges = conn.execute("SELECT COUNT(*) FROM search_admissions WHERE exec_id=?",
                             [exec_id]).fetchone()[0]
        was = ex["results_admitted"] or 0
        count = _results_admitted_after(was, edges, linked=True)
        if not added and count == was:
            return {"exec_id": exec_id, "ref_id": ref, "changed": False,
                    "reason": "edge already present and results_admitted already level"}
        note = ex["findings_note"]
        if added:
            note = dbcore.append_dated_note(
                note, "ADMISSION LINKED", session,
                f"{ref} (candidate {', '.join(map(str, cand))}): {reason}", stamp)
        if count != was:
            note = dbcore.append_dated_note(
                note, "RESULTS_ADMITTED RAISED", session,
                f"{was} -> {count}, level with this search's admission edges"
                + ("" if added else f". {reason}"), stamp)
        # GAP-053 (migration 100): stamped from the same `stamp` the note above dates
        # itself by, so the two cannot disagree.
        conn.execute("UPDATE search_executions SET results_admitted=?, findings_note=?, "
                     "updated_at=?, updated_by_session=? WHERE exec_id=?",
                     [count, note, stamp, session, exec_id])
        return {"exec_id": exec_id, "ref_id": ref, "changed": True, "edge_added": added,
                "candidates": cand, "results_admitted": {"was": was, "now": count},
                "other_admitting_execs": [e for e in admitting if e != exec_id]}


def unlink_admission(exec_id: int, ref_id: str, reason: str, session: str,
                     dry_run: bool = False):
    """Remove an admission edge that is wrong. The corrective half of link-admission.

    ADDED 2026-09-26. db.py had no DELETE or UPDATE on search_admissions at all, so a
    wrong edge -- however it got there: a mis-typed --admitted-ref-id, or a
    link-admission that faithfully copied a candidate's wrong exec_id -- could not be
    corrected through any sanctioned path. Shaped like reattribute_candidate: the move
    needs a reason, and the removed edge is kept in the search's findings_note, because
    the junction row itself is gone.

    results_admitted drops by the edge removed, never below the edges that remain (the
    rule _results_admitted_after states). It does not touch the candidate
    row: if the candidate's own exec_id is what was wrong, correct it with
    reattribute-candidate as well -- the result names any candidate that still points
    at this search, so the second half is not forgotten.

    CAPTURING IT. This is a DELETE, and the capture path is additive by default: run
    emit_batch_sql.py with --allow-delete search_admissions, which renders the removed
    row as a keyed DELETE (only for a table a writer here deletes from). Found the first
    time the verb was used for real (GAP-050's repair, 2026-09-26): emit refused the
    scratch, correctly, until that opt-in existed.
    """
    reason = dbcore.require_reason(
        reason, f"exec {exec_id} -> {ref_id}",
        "Removing a provenance edge without saying why erases an attribution without "
        "a trace of what replaced it.")
    with connect(dry_run) as conn:
        ref = dbcore.fold_ref(ref_id)
        ex = conn.execute("SELECT exec_id, findings_note, results_admitted "
                          "FROM search_executions WHERE exec_id=?", [exec_id]).fetchone()
        if ex is None:
            raise Refusal(f"exec {exec_id}: no such search execution.")
        if not conn.execute("SELECT 1 FROM search_admissions WHERE exec_id=? AND ref_id=?",
                            [exec_id, ref]).fetchone():
            raise Refusal(f"exec {exec_id} -> {ref}: no such admission edge to remove.")
        conn.execute("DELETE FROM search_admissions WHERE exec_id=? AND ref_id=?",
                     [exec_id, ref])
        edges = conn.execute("SELECT COUNT(*) FROM search_admissions WHERE exec_id=?",
                             [exec_id]).fetchone()[0]
        was = ex["results_admitted"] or 0
        count = _results_admitted_after(was, edges, linked=False)
        detail = f"{ref}: {reason}"
        if count != was:
            detail += f" results_admitted {was} -> {count}."
        # One stamp for both the note's date and updated_at (GAP-053, migration 100),
        # so they cannot disagree -- link_admission's own pattern.
        stamp = dbcore.now()
        conn.execute("UPDATE search_executions SET results_admitted=?, findings_note=?, "
                     "updated_at=?, updated_by_session=? WHERE exec_id=?",
                     [count, dbcore.append_dated_note(ex["findings_note"],
                                                      "ADMISSION UNLINKED", session, detail,
                                                      stamp),
                      stamp, session, exec_id])
        still = [r[0] for r in conn.execute(
            "SELECT candidate_id FROM search_candidates WHERE exec_id=? "
            "AND resolved_ref_id=?", [exec_id, ref])]
        return {"exec_id": exec_id, "ref_id": ref, "changed": True,
                "results_admitted": {"was": was, "now": count},
                "candidates_still_naming_this_search": still}


def amend_population_match(match_id: str, match_grade: str, reason: str, session: str,
                           dry_run: bool = False):
    """Re-grade an R13 population match in place, recording the grade it replaces.

    ADDED 2026-09-25 (batch 20) because an owner ruling re-graded REF-01007 and no verb
    could apply it. add-population-match deliberately permits a SECOND row -- a
    dissenting grade reads as a contest (DR-2026-08-19 section 7) -- and that mechanic
    stays. But a ruling is not a dissent: two rows, PROXY and PARTIAL, would tell a
    reader the question is open when it has been decided. So the grade moves, and the
    replaced grade and the reason are appended to mismatch_note, which is the row's
    warrant text. The table has no updated_* columns, so the stamp lives in that note.
    """
    reason = dbcore.require_reason(reason, match_id, "A re-grade must say why.")
    with connect(dry_run) as conn:
        row = conn.execute("SELECT match_id, match_grade, mismatch_note FROM "
                           "evidence_population_match WHERE match_id=?",
                           [match_id]).fetchone()
        if row is None:
            raise Refusal(f"{match_id}: no such population match.")
        dbcore.check_vocab(conn, "evidence_population_match", "match_grade",
                           match_grade, "--match-grade")
        if row["match_grade"] == match_grade:
            return {"match_id": match_id, "changed": False, "match_grade": match_grade}
        conn.execute("UPDATE evidence_population_match SET match_grade=?, "
                     "mismatch_note=? WHERE match_id=?",
                     [match_grade,
                      dbcore.append_dated_note(row["mismatch_note"], "REGRADED", session,
                                               f"{row['match_grade']} -> {match_grade}. "
                                               f"{reason}"),
                      match_id])
        return {"match_id": match_id, "changed": True, "was": row["match_grade"],
                "now": match_grade}


_AMENDABLE_TERM_FIELDS = ("definition", "scope_note")
_TERM_TRAILER = "AMENDED"


def amend_term(term_id: str, field: str, replacement: str, reason: str, session: str,
               dry_run: bool = False):
    """Replace a term's definition or scope note, recording the text it replaces.

    ADDED 2026-09-25 (batch 20) to apply an owner ruling that narrowed TERM-089's
    definition; nothing could write `terms` after add-term minted a row. canonical_en is
    deliberately NOT amendable: renaming a term is a vocabulary decision with callers
    (term_aliases, adjudications, parameters), not a wording fix. `terms` has no notes
    column, so the replaced text and the reason are appended to scope_note -- the only
    free-text column on the row -- as ' || AMENDED <date> by <session>: ...' lines, and
    the stamp goes in updated_*.

    NO-OP DETECTION IS FOR `definition` ONLY (corrected 2026-09-26). The first version
    compared the stored scope_note with the replacement -- but the stored value carries
    the previous trailers, so an identical second call never matched, and it quoted the
    whole old column (trailers included) inside the new trailer, nesting one audit line
    inside the next. Now a scope_note amendment splits the column into its body and the
    audit lines after it, replaces the body, keeps the lines, and adds one more: a
    repeated identical amendment is a second dated line, which is honest, not a bug.
    """
    if field not in _AMENDABLE_TERM_FIELDS:
        raise Refusal(f"--field {field!r}: only {list(_AMENDABLE_TERM_FIELDS)} are "
                      f"amendable. canonical_en is a vocabulary decision, not a wording fix.")
    replacement = (replacement or "").strip()
    if not replacement:
        raise Refusal(f"{term_id}: --replacement is required and may not be blank.")
    marker = f" || {_TERM_TRAILER} "
    if marker in replacement:
        raise Refusal(f"{term_id}: --replacement contains the audit marker {marker.strip()!r}, "
                      f"which would make the body and its history inseparable.")
    reason = dbcore.require_reason(reason, term_id)
    with connect(dry_run) as conn:
        row = conn.execute("SELECT term_id, definition, scope_note FROM terms "
                           "WHERE term_id=?", [term_id]).fetchone()
        if row is None:
            raise Refusal(f"{term_id}: no such term.")
        # Both gates, derived, on every amendable field -- as amend-source and
        # amend-extraction apply them. No-ops today (neither column declares a CHECK or
        # an FK); the first migration that gives one a vocabulary arms this with nothing
        # to update here.
        dbcore.fk_declared(conn, "terms", field, replacement, f"amend-term --field {field}")
        dbcore.check_declared(conn, "terms", field, replacement,
                              f"amend-term --field {field}")
        stamp = dbcore.upd(session)
        old_note = row["scope_note"] or ""
        if field == "definition":
            if (row["definition"] or "").strip() == replacement:
                return {"term_id": term_id, "field": field, "changed": False}
            definition = replacement
            scope_note = dbcore.append_dated_note(
                old_note, _TERM_TRAILER, session,
                f"definition was: '{row['definition'] or ''}'. {reason}",
                stamp["updated_at"])
        else:
            body = old_note.split(marker, 1)[0]
            definition = row["definition"]
            scope_note = dbcore.append_dated_note(
                replacement + old_note[len(body):], _TERM_TRAILER, session,
                f"scope_note was: '{body.strip()}'. {reason}", stamp["updated_at"])
        conn.execute("UPDATE terms SET definition=?, scope_note=?, updated_at=?, "
                     "updated_by_session=? WHERE term_id=?",
                     [definition, scope_note, stamp["updated_at"],
                      stamp["updated_by_session"], term_id])
        return {"term_id": term_id, "field": field, "changed": True}


# Judgement fields on evidence_sources: prose an author must WRITE, which no payload
# can supply and no verifier can prove. Deliberately disjoint from _CORRECTABLE. The
# division is the whole design: a BIBLIOGRAPHIC fact comes from the payload and this
# writer refuses to touch it; a JUDGEMENT is written by a person and can only be
# corrected by a person, with the correction recorded.
# R9's remedy sentence, in ONE place. It was hand-copied into five refusals and
# a skill; when `link-source-slug` landed, three were updated and the rest went
# stale -- one of them (insert_extraction) telling operators outright that
# "there is no CLI verb that links an already-admitted source to a second slug",
# which the same commit had just made false. Interpolate this; never retype it.
R9_REMEDY = (
    "R9: cross-file the existing ref_id, never duplicate it -- "
    "`db.py link-source-slug --ref-id <held> --slug <slug> --rationale <why>`"
)

# THE CO-1 WARRANT SENTENCE (D-0178), in one place for the same reason as R9_REMEDY.
# add-source refuses a Co-1 admission without --co1-provenance, and amend-source
# refuses a move TO co1 without it; both interpolate this and add their own remedy, so
# the doctrine cannot drift between the two doors into the tier.
CO1_WARRANT_REQUIRED = (
    "D-0178: the Co-1 warrant must NAME the co-production — which disabled people or "
    "organisation produced this work — because that co-production IS the warrant. If it "
    "genuinely cannot be evidenced from the source, the row is not Co-1; "
)


_AMENDABLE = (
    "co1_provenance", "co1_source_type", "grey_reason", "verification_note",
    "notes", "bpc_note", "scope",
    # source_type, added 2026-09-20, and the case is the one B05 made against a row
    # this repository had just written. It is a CLASSIFICATION -- is this a report, a
    # journal article, a standard? -- which no payload settles: Crossref's `type` says
    # what the publisher deposited, not what this project counts the item as, and the
    # 1979 HUD study is a `report` here whatever an index calls it. GAP-038 gave
    # add-source the flag to WRITE it and left nothing able to CORRECT it, so the first
    # wrong value cost a compensating migration for a typo -- rule 3 spending its weight
    # on the wrong thing, which is the same argument verification_status was added on.
    # The value that provoked this: `journal-article`, copied straight from Crossref,
    # where the checked vocabulary is `journal_article`. add-source's own --help
    # advertised the hyphen; that is fixed in the same commit.
    "source_type",
    # verification_disposition belongs here and not with the bibliographic fields:
    # D-0157 states it as a JUDGEMENT -- "verification is finished or it did not
    # happen" -- which no payload can settle. Added 2026-09-02 to correct rows that
    # insert_source had written OPEN while VERIFIED, before its default was fixed.
    "verification_disposition",
    # jurisdiction, added 2026-09-18. It sits between the two classes and lands
    # here because the hard case is a JUDGEMENT no payload settles: a synthesis
    # searched across three databases with no single jurisdiction is INT, and
    # choosing INT over a country code is an adjudication, not a transcription.
    # The single-country case (a US survey of ADA-regulated transit) is closer to
    # bibliographic, but splitting one column across two writers by which value it
    # happens to take would be worse than either home. The vocabulary is gated in
    # amend_source by dbcore.check_jurisdiction, so this widens WHO may correct it,
    # not WHAT to. (Until 2026-10-01 this said the vocabulary "stays gated by
    # validate_jurisdiction". That was false: validate_jurisdiction globs files and
    # never reads a table, and this writer accepted any string.)
    "jurisdiction",
    # verification_status and doi_resolution_outcome, added 2026-09-18, and the case
    # for them is the case I4 and C04 make against a row this repository just wrote.
    # Both are JUDGEMENTS about what a retrieval ESTABLISHED, which is exactly what no
    # payload can settle: the payload says what came back, the operator says whether
    # that amounts to having verified the source. Batch 16 graded REF-01002 VERIFIED on
    # an authoritative third-party bibliographic record while its verification_method
    # read corroborated-not-retrieved -- I4 caught it, and NOTHING COULD CORRECT IT.
    # Its DOI outcome was NULL for a work that has no DOI at all, which C04 caught and
    # nothing could correct either. A field a session can get wrong at admission and
    # cannot fix afterwards forces a compensating migration for a typo, which is rule 3
    # spending its weight on the wrong thing.
    #
    # THE RISK IS NAMED RATHER THAN WAVED OFF: verification_status gates real checks, so
    # making it amendable lets a session flip UNVERIFIED to VERIFIED to clear one. Two
    # things hold against that and neither is this constant. I4 still refuses VERIFIED
    # whose method did not obtain the artefact, which is the dangerous direction; and
    # amend-source ledgers the replaced value with a mandatory reason into
    # metadata_integrity_detail, so the flip is legible rather than silent. This widens
    # WHO may correct these, not WHAT to -- the vocabularies stay gated where they were.
    "verification_status",
    "doi_resolution_outcome",
    # evidence_type, added 2026-10-01 (I1 of the batch-23 process-gap review). The type
    # is a CLASSIFICATION -- is this Co-1 work, a code, a grey report? -- which no
    # payload settles, and that review found a mis-tiered row (a Co-1/T6 contradiction)
    # with no correction after capture except hand SQL against a table the CLI reaches.
    # The tier moves WITH the type, derived by the ratified ladder in the same
    # statement, exactly as the scope path below moves it; _retype_source refuses any
    # move a live determination rests on. This grows a curated tuple rule 8 names as a
    # violator: GAP-013 item (1), deriving the amendable set from the live columns,
    # remains the fix.
    "evidence_type",
)


def _retype_source(conn, ref_id: str, new_type: str, scope, tier, co1_provenance,
                   co1_source_type=None):
    """The columns an `amend-source --field evidence_type` move writes beside the type,
    and the ledger text recording them; None when the row already says this.

    THE VOCABULARY IS THE LADDER. evidence_sources.evidence_type declares no CHECK
    (`dbcore.check_values(conn, 'evidence_sources', 'evidence_type')` is empty), so its
    one home is the keys of schemas.tier_derivation.VALID_SCOPES_BY_TYPE, which
    add-source already gates on. The scope is required unless the new type admits
    exactly one, and the tier is DERIVED from (type, scope): --tier is optional and
    refused when it disagrees, because a tier is never asserted on its own.

    THE CO-1 FIELDS MOVE WITH THE TYPE. A move to co1 needs the D-0178 warrant AND a
    co1_source_type: schemas/evidence_source.py co1_field_consistency requires both, and
    schemas.directness.grain_for grades a Co-1 source's grain FROM co1_source_type (a
    community-consensus type is population-grain; NULL falls back to individual-grain),
    so a retype that left it NULL would silently downgrade the source it re-tiers. The
    column declares no CHECK, so its vocabulary is schemas.enums.Co1SourceType, the
    mirror's one home. A move off co1 copies every co1_* column into the ledger and sets
    it NULL: those columns
    are only valid on a Co-1 row (schemas/evidence_source.py co1_field_consistency),
    and only co1 rows carry them (`select evidence_type, count(co1_provenance),
    count(co1_source_type) from evidence_sources group by 1`). The set is read from the
    live schema by its co1_ prefix, never listed. Left in place, a Co-1 warrant on a
    non-Co-1 row is a live claim about a tier the row no longer holds.

    NEVER MOVE AN ADJUDICATED FIGURE. A live determination resting on the source
    (dbcore.determinations_resting_on) refuses the move: re-tiering its source would
    change a written answer's evidence without re-deciding it.
    """
    from schemas.tier_derivation import VALID_SCOPES_BY_TYPE, derive_tier  # noqa: E402
    valid = VALID_SCOPES_BY_TYPE.get(new_type)
    if valid is None:
        raise Refusal(
            f"{ref_id}: evidence_type {new_type!r} is not on the ratified ladder. Known "
            f"types: {sorted(VALID_SCOPES_BY_TYPE)}. Nothing was written.")
    if scope is None and len(valid) == 1:
        scope = next(iter(valid))                    # forced by the type; not a judgment
    if scope is None:
        raise Refusal(
            f"{ref_id}: --scope is REQUIRED to move evidence_type to {new_type!r}: it is "
            f"the discriminator the tier is derived from, and this type spans more than "
            f"one tier. Choose {sorted(valid)}. Nothing was written.")
    if scope not in valid:
        raise Refusal(
            f"{ref_id}: --scope {scope!r} is not admissible for evidence_type "
            f"{new_type!r}; valid: {sorted(valid)}. Nothing was written.")
    derived = derive_tier(new_type, scope)
    if tier is not None and int(tier) != derived:
        raise Refusal(
            f"{ref_id}: --tier {tier} contradicts the ratified ladder, which derives "
            f"{derived} from ({new_type}, {scope}). The tier is not a free field; drop "
            f"--tier or correct the type or scope. Nothing was written.")
    co1_cols = [c[1] for c in conn.execute("PRAGMA table_info(evidence_sources)")
                if c[1].startswith("co1_")]
    cur = conn.execute(
        "SELECT evidence_type, scope, tier%s FROM evidence_sources WHERE ref_id=?"
        % "".join(f", {c}" for c in co1_cols), [ref_id]).fetchone()
    old_type = cur["evidence_type"]
    if (old_type or "").strip().lower() == new_type:
        if cur["scope"] == scope and cur["tier"] == derived:
            return None
        raise Refusal(
            f"{ref_id}: evidence_type is already {new_type!r} (scope {cur['scope']!r}, "
            f"tier {cur['tier']}). This path moves a TYPE; a scope move on an unchanged "
            f"type is `amend-source --field scope`, which carries the tier with it. "
            f"Nothing was written.")
    provenance = (co1_provenance or "").strip()
    if new_type == "co1" and not provenance:
        raise Refusal(
            f"{ref_id}: --co1-provenance is REQUIRED to move evidence_type to co1. "
            + CO1_WARRANT_REQUIRED
            + "leave it at its actual tier. Nothing was written.")
    if new_type != "co1" and co1_provenance is not None:
        raise Refusal(
            f"{ref_id}: --co1-provenance is only admissible when the new evidence_type is "
            f"co1; {new_type!r} carries no Co-1 warrant. Nothing was written.")
    source_type = (co1_source_type or "").strip()
    if new_type != "co1" and co1_source_type is not None:
        raise Refusal(
            f"{ref_id}: --co1-source-type is only admissible when the new evidence_type "
            f"is co1; {new_type!r} carries no Co-1 source type. Nothing was written.")
    if new_type == "co1":
        from schemas.enums import Co1SourceType  # noqa: E402
        members = sorted(m.value for m in Co1SourceType)
        if not source_type:
            raise Refusal(
                f"{ref_id}: --co1-source-type is REQUIRED to move evidence_type to co1. "
                f"A Co-1 row needs it (co1_field_consistency), and grain_for grades the "
                f"source's grain from it: left NULL, a community-consensus source reads as "
                f"one person's account. Choose from schemas.enums.Co1SourceType: "
                f"{members}. Nothing was written.")
        if source_type not in members:
            raise Refusal(
                f"{ref_id}: --co1-source-type {source_type!r} is not a member of "
                f"schemas.enums.Co1SourceType: {members}. Nothing was written.")
    resting = dbcore.determinations_resting_on(conn, ref_id)
    if resting:
        named = ", ".join(f"specification {sid} (via {junction})"
                          for junction, sid in resting)
        raise Refusal(
            f"{ref_id} carries a live determination: {named}. Moving its evidence_type "
            f"re-tiers the evidence that answer was written on without re-deciding it. "
            f"Retire the specification first (db.py retire-specification), then amend, "
            f"then re-determine. Never move an adjudicated figure. Nothing was written.")
    sets = {"scope": scope, "tier": derived}
    moved_scope = (f"scope {cur['scope']!r} unchanged" if cur["scope"] == scope
                   else f"scope {cur['scope']!r} -> {scope!r}")
    text = (f". {moved_scope}; tier {cur['tier']} -> {derived}, derived from "
            f"(evidence_type, scope) by the ratified ladder in the same statement as the "
            f"type.")
    if new_type == "co1":
        sets["co1_provenance"] = provenance
        sets["co1_source_type"] = source_type
        text += (f" co1_provenance written as the D-0178 warrant; replaced text was: "
                 f"{cur['co1_provenance']!r}. co1_source_type written as "
                 f"{source_type!r}; replaced value was {cur['co1_source_type']!r}.")
    leaving = (old_type or "").strip().lower() == "co1"
    moved = {c: cur[c] for c in co1_cols if leaving and cur[c] is not None}
    if moved:
        sets.update({c: None for c in moved})
        text += (" Leaving co1, so the Co-1-only fields are set NULL and their text is "
                 "kept here: " + "; ".join(f"{c} was {v!r}" for c, v in moved.items())
                 + ".")
    out = {"type_was": old_type, "type_now": new_type, "scope_was": cur["scope"],
           "scope_now": scope, "tier_was": cur["tier"], "tier_now": derived,
           "nulled": sorted(moved)}
    return {"sets": sets, "ledger": text, "out": out}


def amend_source(ref_id: str, field: str, replacement: str, reason: str,
                 session: str, dry_run: bool = False, tier=None, scope=None,
                 co1_provenance=None, co1_source_type=None):
    """Replace a JUDGEMENT field on an evidence row, recording what was replaced.

    Replaces rather than appends, and that is the opposite of what resolve-candidate
    and amend-search do, on purpose. Those fields hold a HYPOTHESIS, and R15 wants the
    guess left legible beside the correction. These fields hold a WARRANT -- the
    sentence a downstream reader takes as the reason a source stands where it does. A
    false citation inside co1_provenance is not a historical record of what someone
    believed; it is a live claim about why a Co-1 source counts as Co-1, and leaving
    it in place with a correction underneath means the next reader can still quote it.

    So the wrong text goes, and it goes into metadata_integrity_detail with the date
    and the reason, where it is preserved without being quotable as the warrant.

    Written 2026-09-02 for REF-00978, whose co1_provenance ended "Provenance verified
    from the retrieved report itself (p.2, p.28), not from a description of it." p.2 of
    that PDF is blank, p.28 is survey question 40, and the charity number the sentence
    carried appears nowhere in the 29 pages -- it came from a web description, which is
    the one thing the sentence denies. A verification assertion that is itself the
    thing that failed is the CLAUDE.md 2(c) shape, and it was in the field carrying a
    CRPD Art 4.3 warrant.
    """
    replacement, reason = (replacement or "").strip(), (reason or "").strip()
    if field in _CORRECTABLE or field == "authors":
        raise Refusal(
            f"{ref_id}: {field!r} is a bibliographic field. It is not amendable by hand "
            f"-- use `db.py correct-source`, which takes it from the logged payload.")
    if field not in _AMENDABLE:
        raise Refusal(
            f"{ref_id}: {field!r} is not an amendable judgement field. "
            f"Amendable: {', '.join(_AMENDABLE)}.")
    if not replacement:
        raise Refusal(f"{ref_id}: refusing to blank {field!r}. Give the corrected text.")
    if not reason:
        raise Refusal(
            f"{ref_id}: --reason is required. An unexplained overwrite of a warrant is "
            f"indistinguishable from the error it replaces.")
    if field == "evidence_type":
        # Stored lower-case, as add-source stores it: assess_cell.classify() compares
        # against lower-case literals, so 'CO1' would stop anchoring anything.
        replacement = replacement.lower()
    elif scope is not None or co1_provenance is not None or co1_source_type is not None:
        raise Refusal(
            f"{ref_id}: --scope, --co1-provenance and --co1-source-type are only "
            f"admissible beside --field evidence_type, where they travel with the type. A "
            f"scope on its own is `--field scope`; a Co-1 row's warrant or source type on "
            f"its own is `--field co1_provenance` / `--field co1_source_type`. Nothing was "
            f"written.")
    if field == "jurisdiction":
        # No CHECK on the column, so check_declared below is a no-op for it; the declared
        # vocabulary is the enum (I7).
        dbcore.check_jurisdiction(replacement,
                                  f"{ref_id}: amend-source --field jurisdiction")
    # ── THE TWO VERIFICATION FIELDS CARRY insert_source's REFUSALS WITH THEM ──
    #
    # Added 2026-09-18, hours after those fields were made amendable, because making
    # them amendable opened a hole this writer had no idea it was opening: it applies
    # NO vocabulary gate and NO invariant, so `--field verification_status` accepted
    # any string at all, and accepted VERIFIED on a row whose verification_method is
    # NULL -- the exact row `insert_source` refuses with "a standing without its
    # method is not a standing" (D-0157).
    #
    # AND THE COMMENT DEFENDING THE WIDENING WAS WRONG ABOUT WHY THAT WAS SAFE. It
    # said "I4 still refuses VERIFIED whose method did not obtain the artefact". I4's
    # subject is `verification_status='VERIFIED' AND verification_method IS NOT NULL`,
    # so a NULL-method row is not examined by I4 AT ALL -- it is invisible to I1, I2
    # and I4 alike, and test_db_integrity reports 74/74 over it. A guard that does not
    # see the row it is cited as guarding is not a guard.
    #
    # A typo was equally unstopped: at the time `verification_status` had no CHECK in
    # the schema and no enum-guard entry (migration 091 has since given it one, and
    # ENUM_GUARDS was deleted 2026-09-21), so 'verrified' stored cleanly -- and removed
    # the row from every I-check's subject set, since all of them filter on the
    # literal 'VERIFIED'. add-source gated the same column with argparse choices; this
    # writer gated nothing. The vocabularies did NOT "stay gated where they were".
    # The doi_resolution_outcome special case was DELETED 2026-09-21 with ENUM_GUARDS.
    # It existed because the column had no CHECK, so the generic path could not gate it and
    # `check_vocab` would have fallen back to the live values and refused REVERTED -- legal,
    # with no row yet carrying it. Migration 091 gave the column a real CHECK, so
    # `dbcore.check_declared` below now refuses a bad value from the schema itself and
    # accepts REVERTED. Verified before deleting: check_declared refuses 'BOGUS' and admits
    # 'REVERTED'. One home, and it is the schema's.
    if tier is not None and field not in ("scope", "evidence_type"):
        raise Refusal(
            f"{ref_id}: --tier is only admissible beside --field scope or --field "
            f"evidence_type. The tier is "
            f"DERIVED from (evidence_type, scope) by the ratified ladder; it is never "
            f"set on its own, because a tier with no derivation input is exactly the "
            f"state B5(b) found on all nine sources and could not check.")
    new_tier = old_tier = retype = None
    with connect(dry_run) as conn:
        row = conn.execute(f"SELECT ref_id, {field}, verification_method, "
                           f"verification_disposition, verification_closure_reason, "
                           f"verification_attempt_count, "
                           f"metadata_integrity_detail "
                           f"FROM evidence_sources WHERE ref_id=?", [ref_id]).fetchone()
        if row is None:
            raise Refusal(f"{ref_id}: no such evidence source.")
        # EVERY AMENDABLE FIELD WHOSE COLUMN DECLARES A CHECK IS GATED BY IT, derived
        # rather than listed (rule 8). Added 2026-09-20, and the case against the older
        # shape is that it was field-by-field: `verification_status` got the gate below
        # because someone thought of it, and every other _AMENDABLE field got nothing.
        # That went wrong within hours in this same batch. `source_type` was added to
        # _AMENDABLE precisely to repair a vocabulary typo ('journal-article' for
        # 'journal_article') -- and the verb added to fix the typo would have accepted
        # the identical typo, leaving a blocking check as the only catch, after the
        # fact, which is the shape of the defect it was added for.
        #
        # check_declared is a no-op for a column with no CHECK, so this neither
        # constrains the free-text warrants (co1_provenance, notes, verification_note)
        # nor duplicates the specific gate below; a migration that gives any amendable
        # column a vocabulary arms this in the same commit, with nothing to update here.
        dbcore.fk_declared(conn, "evidence_sources", field, replacement,
                           f"amend-source --field {field}")
        dbcore.check_declared(conn, "evidence_sources", field, replacement,
                              f"amend-source --field {field}")
        if field == "verification_status":
            # The live vocabulary, read from the column rather than retyped beside it
            # (rule 8). This column carries no CHECK, so check_vocab falls back to the
            # live values -- which for THIS column are exactly {VERIFIED, UNVERIFIED},
            # so the fallback is the whole vocabulary and not a sample of it. That is
            # why it is safe here and not for doi_resolution_outcome above. Without any
            # gate, 'verrified' stored cleanly and silently dropped the row out of every
            # I-check, all of which filter on the literal 'VERIFIED'.
            dbcore.check_vocab(conn, "evidence_sources", "verification_status",
                               replacement, "--field verification_status")
        if field == "verification_status" and replacement == "VERIFIED" \
                and not row["verification_method"]:
            # D-0157, carried over from insert_source so amending cannot be the way
            # round it. It lives HERE, on the row this function already read, rather
            # than in the argv block above: the first cut opened a second connection
            # with `connect(True)` -- which is positional `dry_run=True`, NOT
            # `readonly=True` -- so it asked for the canonical blob READ-WRITE and
            # dbcore's rule-3 guard refused it. The invariant was unreachable on the
            # one database it most needed to hold for, and the operator got a
            # migrations-only lecture instead of the real reason.
            raise Refusal(
                f"{ref_id}: VERIFIED requires verification_method (D-0157: a standing "
                f"without its method is not a standing). `add-source` refuses this row; "
                f"amending must not be the way around it. Set the method first, then "
                f"the standing.")
        if field == "verification_status" and replacement != "VERIFIED" \
                and (row["verification_disposition"] or "") == "CLOSED":
            # THE OTHER DIRECTION, UNGUARDED UNTIL 2026-09-18. The D-0157 refusal above
            # covers UNVERIFIED -> VERIFIED, which the comment on _AMENDABLE calls "the
            # dangerous direction" -- but a DEMOTION off a CLOSED row leaves
            # verification_disposition='CLOSED' standing over a non-VERIFIED status,
            # which I3 ("closure is earned and reasoned") and I3b ("closure rests on at
            # least two recorded attempts") both reject. Reproduced on a scratch copy:
            # amending REF-01004 to UNVERIFIED turned 74/74 into 72/74. The disposition
            # is a separate, amendable field; this refuses rather than silently
            # rewriting it, because which closure reason applies is the operator's to
            # state and not this writer's to invent.
            _why = (row["verification_closure_reason"] or "").strip()
            _n = row["verification_attempt_count"] or 0
            if not _why or _n < 2:
                raise Refusal(
                    f"{ref_id}: demoting verification_status to {replacement!r} would "
                    f"leave verification_disposition='CLOSED' over a non-VERIFIED row "
                    f"with "
                    f"{'no closure reason' if not _why else f'{_n} recorded attempt(s)'}"
                    f", which test_db_integrity I3/I3b reject. Amend "
                    f"verification_disposition, verification_closure_reason and "
                    f"verification_attempt_count to say WHY the closure stands, then "
                    f"demote the standing.")
        was = row[field]
        if field == "evidence_type":
            # The type's own no-op test lives in _retype_source: an unchanged type with a
            # different scope is a refusal there, not a silent no-op here.
            retype = _retype_source(conn, ref_id, replacement, scope, tier, co1_provenance,
                                    co1_source_type)
            if retype is None:
                return {"ref_id": ref_id, "field": field, "changed": False}
        elif (was or "").strip() == replacement:
            return {"ref_id": ref_id, "field": field, "changed": False}
        if field == "scope":
            # BYPASS CLOSED 2026-09-10. `scope` is amendable, and amending it changes
            # the ratified tier — this path performed no derivation, so it could write a
            # contradiction. Proven on a scratch copy: REF-00784 amended to
            # (clinical, lower_control) while tier stayed 1, and clinical+lower_control
            # derives 3. The row then satisfied every gate and asserted a tier the
            # ladder does not produce.
            from schemas.tier_derivation import (  # noqa: E402
                VALID_SCOPES_BY_TYPE, derive_tier)
            cur = conn.execute("SELECT evidence_type, tier FROM evidence_sources "
                               "WHERE ref_id=?", [ref_id]).fetchone()
            _et = (cur["evidence_type"] or "").lower()
            if not _et:
                raise Refusal(
                    f"{ref_id} has no evidence_type, so no scope is derivable for it. "
                    f"Set the type first; a scope without a type states nothing.")
            _valid = VALID_SCOPES_BY_TYPE.get(_et, frozenset())
            if replacement not in _valid:
                raise Refusal(
                    f"{ref_id}: scope {replacement!r} is not admissible for "
                    f"evidence_type {_et!r}; valid: {sorted(_valid)}")
            _derived = derive_tier(_et, replacement)
            if cur["tier"] != _derived:
                # PAIRED CHANGE, added 2026-09-12. Until now this was a flat refusal,
                # and `tier` was reachable by NO sanctioned writer: `_AMENDABLE` omits
                # it and `correct-source` takes bibliographic fields from a payload.
                # So the only way to re-tier a source was hand SQL against a table the
                # CLI can reach, which CLAUDE.md 4 calls a coverage bug to fix rather
                # than a licence to bypass. The wrong thing that reached the guidebook
                # without it (the 8 bar): REF-00784 stood at Tier 1 -- co-primary
                # anchoring strength -- on a design its own abstract calls "Case
                # series" with a "sample of convenience", recorded as wrong by the
                # 2026-07-20 anchor sweep and unfixable for fifty-four days.
                #
                # The refusal is kept and NARROWED rather than removed. A tier still
                # cannot be asserted: it can only be moved to the one value the ladder
                # derives from the new scope, in the same statement as that scope, with
                # a reason. There is no path here that writes a row the ladder cannot
                # produce -- which was the original refusal's whole point.
                #
                # THE SECOND PATH, added 2026-10-01 (I1): `--field evidence_type` moves
                # the tier with the TYPE by the same derivation (_retype_source), with
                # --tier optional there and refused when it disagrees. `tier` itself is
                # still in neither _AMENDABLE nor _CORRECTABLE.
                if tier is None:
                    raise Refusal(
                        f"{ref_id}: amending scope to {replacement!r} would make the "
                        f"stored tier {cur['tier']} contradict the ratified ladder, "
                        f"which derives {_derived} from ({_et}, {replacement}).\n"
                        f"Amending the scope is amending the tier. If the scope is what "
                        f"the bytes say, re-run with --tier {_derived} and the two move "
                        f"together; this path will not write a row the ladder cannot "
                        f"produce.")
                if int(tier) != _derived:
                    raise Refusal(
                        f"{ref_id}: --tier {tier} is not derivable from "
                        f"({_et}, {replacement}); the ladder derives {_derived}. The "
                        f"tier is not a free field -- correct the scope instead.")
                new_tier, old_tier = _derived, cur["tier"]
            elif tier is not None and int(tier) != _derived:
                raise Refusal(
                    f"{ref_id}: --tier {tier} contradicts the ladder, which derives "
                    f"{_derived} from ({_et}, {replacement}).")
        stamp = audit(session)
        # THE LEDGER IS THE RECORD, and it is prose on purpose. Migration 094 added an
        # `amendments` table here and 095 dropped it: nothing read it, seven other amending
        # paths never wrote it, and this writer put `reason` into BOTH the table and the
        # ledger below -- so the warrant had two homes and the unread one was the
        # structured copy. 095's header records what a reader would have to be for the
        # register to be worth re-creating. Until then the warrant lives here, in the
        # column `metadata_integrity_audit.py` actually reads.
        ledger = (row["metadata_integrity_detail"] or "").rstrip()
        segment = (f"{stamp['created_at'][:10]} {field} CORRECTED ({reason}). "
                   f"Replaced text was: {was!r}")
        if retype is not None:
            # ONE segment: the type, its scope and tier, and any Co-1 text it carries out
            # of the columns, so the move cannot be read in halves.
            segment += retype["ledger"]
            retype["out"]["ledger_segment"] = segment
        ledger += " || " + segment
        if new_tier is not None:
            ledger += (f" || {stamp['created_at'][:10]} tier CORRECTED {old_tier} -> "
                       f"{new_tier}, derived from (evidence_type, scope) by the "
                       f"ratified ladder in the same statement as the scope.")
        _sets, _vals = [f"{field}=?"], [replacement]
        if new_tier is not None:
            _sets.append("tier=?"); _vals.append(new_tier)
        for col, value in (retype or {}).get("sets", {}).items():
            _sets.append(f"{col}=?"); _vals.append(value)
        conn.execute(
            f"UPDATE evidence_sources SET {', '.join(_sets)}, "
            f"metadata_integrity_status=?, metadata_integrity_detail=?, "
            f"updated_at=?, updated_by_session=? WHERE ref_id=?",
            _vals + ["CORRECTED", ledger.lstrip(" |"),
                     stamp["created_at"], stamp["created_by_session"], ref_id])
        out = {"ref_id": ref_id, "field": field, "changed": True,
               "was_chars": len(was or ""), "now_chars": len(replacement)}
        if new_tier is not None:
            out["tier_was"], out["tier_now"] = old_tier, new_tier
        if retype is not None:
            out.update(retype["out"])
        return out


def retire_specification(specification_id: int, session: str, reason: str = None,
                         superseded_by: int = None, dry_run: bool = False):
    """Retire a determination IN PLACE so its cell can be determined again.

    Owner ruling 2026-09-16, "retire in place, never hard-delete". Until then a
    determined cell could never be re-determined by any route: `idx_spec_row_identity`
    was UNIQUE over the whole table and `specifications.state` had no lifecycle value,
    so the only ways out were deleting the row or inventing a supersede design — the
    first destroys the record of what was concluded, and the second was an owner
    decision no component was entitled to make. Migration 083 made that index PARTIAL
    over live rows; this is the writer that moves a row out of the live set.

    THE ROW DOES NOT LEAVE. It keeps its state, its tier_basis, its derivation_sha and
    its governing_refs, and it stays linked to the extractions it was computed from.
    What changes is that it is no longer the cell's answer. That is the difference
    between a history the project can audit and a hole where a determination used to be.

    LINKING IS A SECOND CALL BY DESIGN. The replacement does not exist at the moment of
    retirement — the engine refuses to run while a live row stands, so the real order is
    retire, re-determine, then link. Passing --superseded-by on a later call fills the
    pointer on an already-retired row; that is the one amendment this writer allows,
    and only while the pointer is still empty.
    """
    with connect(dry_run) as conn:
        row = conn.execute(
            "SELECT specification_id, parameter_id, state, retired_at, "
            "superseded_by_specification_id FROM specifications WHERE specification_id=?",
            [specification_id]).fetchone()
        if row is None:
            raise Refusal(f"specification {specification_id}: no such determination.")

        if row["retired_at"]:
            # Link-only follow-up on an already-retired row.
            if superseded_by is None:
                raise Refusal(
                    f"specification {specification_id} was already retired at "
                    f"{row['retired_at']}. Retiring it twice records nothing new. If you "
                    f"meant to record what replaced it, pass --superseded-by.")
            if row["superseded_by_specification_id"]:
                raise Refusal(
                    f"specification {specification_id} already points at "
                    f"{row['superseded_by_specification_id']} as its replacement. A "
                    f"determination is superseded once; a second replacement means the "
                    f"FIRST replacement is what needs retiring, not this row.")
            if not dbcore.exists(conn, "specifications", "specification_id", superseded_by):
                raise Refusal(f"--superseded-by {superseded_by}: no such determination.")
            if superseded_by == specification_id:
                raise Refusal("a determination cannot supersede itself.")
            conn.execute("UPDATE specifications SET superseded_by_specification_id=?, "
                         "updated_at=?, updated_by_session=? WHERE specification_id=?",
                         [superseded_by, dbcore.now(), session, specification_id])
            return {"specification_id": specification_id, "superseded_by": superseded_by,
                    "linked": True}

        if not (reason or "").strip():
            raise Refusal(
                f"specification {specification_id}: --reason is required to retire a "
                f"determination. Retiring one without recording why discards the "
                f"judgement it cost, and leaves the next reader unable to tell a "
                f"superseded answer from a mistaken one. (The table's own trigger "
                f"refuses this too, so there is no way round it.)")
        conn.execute(
            "UPDATE specifications SET retired_at=?, retired_by_session=?, "
            "retirement_reason=?, superseded_by_specification_id=COALESCE(?, "
            "superseded_by_specification_id), updated_at=?, updated_by_session=? "
            "WHERE specification_id=?",
            [dbcore.now(), session, reason.strip(), superseded_by, dbcore.now(), session,
             specification_id])
        return {"specification_id": specification_id, "parameter_id": row["parameter_id"],
                "was_state": row["state"], "retired": True,
                "superseded_by": superseded_by,
                "note": "the cell is determinable again; the row stays as history"}


def update_locator(ref_id: str, status: str, session: str, reason: str = None,
                   dry_run: bool = False):
    """Move a lead's status. insert_locator has told callers to "Use update-locator"
    for some time, and there was no such command -- an error message naming a remedy
    that does not exist, which CLAUDE.md 4 treats as an unswept caller.

    The transition this exists for is REFERENCE-ONLY -> PROMOTED, declared in the
    column's own CHECK and, measured 2026-09-02, used by NONE of the 881 rows. When a
    lead is cross-filed onto a real evidence row under R9, the clue store still says
    "reference only, not evidence" about a ref_id that now carries an evidence_sources
    row, a slug link and graded population matches. Only the status moves: the lead's
    identifiers are what make it that lead, and rule 5 keeps the bibliography in
    evidence_sources rather than copying it back down here.
    """
    with connect(dry_run) as conn:
        row = conn.execute("SELECT ref_id, status FROM source_locators WHERE ref_id=?",
                           [ref_id]).fetchone()
        if row is None:
            raise Refusal(f"{ref_id}: not in source_locators.")
        dbcore.check_vocab(conn, "source_locators", "status", status, "--status")
        if status == "PROMOTED" and not dbcore.exists(conn, "evidence_sources",
                                                      "ref_id", ref_id):
            raise Refusal(
                f"{ref_id}: PROMOTED means this lead became evidence, and there is no "
                f"evidence_sources row for it. File the source first.")
        # SCREENED-OUT states WHY (migration 082). The column's CHECK enforces this too,
        # so the refusal cannot be bypassed by another writer -- this one exists to fail
        # with a sentence instead of a constraint violation, which is the difference
        # between an operator who knows what to do next and one reading a stack trace.
        if status == "SCREENED-OUT" and not (reason or "").strip():
            raise Refusal(
                f"{ref_id}: SCREENED-OUT requires --reason. Marking a lead off without "
                f"recording why discards the only thing the work produced, and leaves it "
                f"indistinguishable from a lead nobody examined.")
        if reason and status != "SCREENED-OUT":
            raise Refusal(
                f"{ref_id}: --reason is the screening judgement and belongs only to "
                f"SCREENED-OUT; {status!r} does not take one. Use --notes on add-locator "
                f"for anything else.")
        if row["status"] == status:
            return {"ref_id": ref_id, "status": status, "changed": False}
        # WHO WORKED THIS LEAD. update_locator has taken `session` since it was written
        # and stored it nowhere; `batch_capture_report.py` found source_locators
        # unattributable on its first run for exactly that reason (893 rows, no session
        # column, no FK path to one). Both terminal transitions record it: PROMOTED and
        # SCREENED-OUT are equally "this batch worked this lead".
        terminal = status in ("PROMOTED", "SCREENED-OUT")
        conn.execute(
            "UPDATE source_locators SET status=?, screened_reason=?, "
            "created_by_session=COALESCE(?, created_by_session), "
            "created_at=COALESCE(?, created_at) WHERE ref_id=?",
            [status, (reason or "").strip() or None,
             session if terminal else None,
             dbcore.now() if terminal else None, ref_id])
        return {"ref_id": ref_id, "was": row["status"], "now": status, "changed": True,
                "created_by_session": session if terminal else None,
                "screened_reason": (reason or "").strip() or None}


def observe_term(data: dict, session: str, dry_run: bool = False):
    """Record that a source USES a phrase. Makes no claim that it names our concept.

    D-0173, the owner ruling this implements: "Recording that a source uses a phrase is
    a fact about the document, not a claim that the phrase names one of our categories
    -- the same epistemic act as recording its DOI."

    So this writer accepts NO term_id, and there is no flag for one. Adjudication is a
    different stage with its own writer. A single call that could observe and classify
    at once would let the observation be born half-adjudicated, which is precisely the
    presupposition the ruling exists to prevent.
    """
    surface = (data.get("surface_form") or "").strip()
    if not surface:
        raise Refusal("--surface-form is required: the phrase AS THE SOURCE WRITES IT.")
    if "term_id" in data:
        raise Refusal(
            "observe-term does not accept a term_id. Observing that a source uses a "
            "phrase is a fact about the document; deciding whether it names one of our "
            "concepts is judgment, and belongs to `db.py adjudicate-term` (D-0173).")
    with connect(dry_run) as conn:
        ref = dbcore.fold_ref(data.get("ref_id"))
        if not dbcore.exists(conn, "evidence_sources", "ref_id", ref):
            raise Refusal(
                f"ref_id {data.get('ref_id')!r} is not an admitted source. A term is "
                f"observed IN a source; observe it after the source is filed.")
        _refuse_tombstone(conn, ref, "observe-term")
        row = {"ref_id": ref, "surface_form": surface,
               "language": (data.get("language") or "EN").strip().upper(),
               "locator": data.get("locator"),
               "context_quote": data.get("context_quote"),
               "notes": data.get("notes")}
        row.update(dbcore.stamp_for(conn, "observed_terms", session))
        prior = conn.execute(
            "SELECT observation_id FROM observed_terms "
            "WHERE ref_id=? AND surface_form=? AND language=?",
            (ref, surface, row["language"])).fetchone()
        if prior:
            return {"observation_id": prior[0], "created": False,
                    "reason": "this source was already observed using this phrase"}
        cols = ",".join(row)
        cur = conn.execute(f"INSERT INTO observed_terms ({cols}) "
                           f"VALUES ({','.join('?'*len(row))})", list(row.values()))
        return {"observation_id": cur.lastrowid, "created": True}


def adjudicate_term(observation_id: int, outcome: str, rationale: str, session: str,
                    term_id: str = None, dry_run: bool = False):
    """Decide, WITH THE SOURCE IN HAND, whether an observed phrase names our concept.

    The judgment half of D-0173. Divergent adjudications are DELIBERATELY permitted --
    no uniqueness on observation_id -- so an adversarial pass that disagrees lands a
    second row and the divergence reads as a contest. Same mechanic DR-2026-08-19 §7
    fixes for evidence_population_match, which CLAUDE.md §4 lists among the refusals
    that must stay absent.
    """
    rationale = (rationale or "").strip()
    if not rationale:
        raise Refusal(
            "--rationale is required. An adjudication that does not say why cannot be "
            "contested, and being contestable is the point of splitting judgment from "
            "observation.")
    with connect(dry_run) as conn:
        obs = conn.execute("SELECT observation_id, surface_form FROM observed_terms "
                           "WHERE observation_id=?", [observation_id]).fetchone()
        if obs is None:
            raise Refusal(f"observation {observation_id}: no such observed term.")
        dbcore.check_vocab(conn, "term_adjudications", "outcome", outcome, "--outcome")
        names = outcome in ("NAMES-EXISTING", "NAMES-NEW")
        if names and not term_id:
            raise Refusal(
                f"--outcome {outcome} names a term, so --term-id is required. If the "
                f"phrase is not one of our concepts the outcome is NOT-OURS; if it "
                f"cannot be settled on this source alone it is DEFERRED.")
        if not names and term_id:
            raise Refusal(
                f"--outcome {outcome} declines to name a term, so --term-id must be "
                f"absent. Say NAMES-EXISTING or NAMES-NEW if it does name one.")
        if term_id and not dbcore.exists(conn, "terms", "term_id", term_id):
            raise Refusal(
                f"term_id {term_id!r} is not in `terms`. For a concept new to the "
                f"vocabulary, create the term first, then adjudicate NAMES-NEW to it.")
        row = {"observation_id": observation_id, "outcome": outcome,
               "term_id": term_id, "rationale": rationale}
        row.update(dbcore.stamp_for(conn, "term_adjudications", session))
        prior = conn.execute("SELECT created_by_session FROM term_adjudications "
                             "WHERE observation_id=?", [observation_id]).fetchall()
        if prior:
            print(f"NOTE: observation {observation_id} ({obs['surface_form']!r}) already "
                  f"adjudicated by {[r[0] for r in prior]}. Writing a second row -- "
                  f"divergent judgements read as a contest, not as an error.",
                  file=sys.stderr)
        cols = ",".join(row)
        cur = conn.execute(f"INSERT INTO term_adjudications ({cols}) "
                           f"VALUES ({','.join('?'*len(row))})", list(row.values()))
        return {"adjudication_id": cur.lastrowid, "outcome": outcome,
                "contested": bool(prior)}


# A canonical name may not state its own answer. This is the item-layer lesson as a
# refusal: `E-08 Corridor Clear Width (>=1200 mm Minimum)` biased every finding filed
# into it, because the container announced the determination before the evidence did.
# Measured 2026-09-09: no live terms.canonical_en contains any of these.
_VALUE_BEARING = re.compile(r"[0-9\u2265\u2264<>=]|\b(min|max|minimum|maximum)\b", re.I)


def insert_term(from_observation: int, canonical_en: str, rationale: str, session: str,
                definition: str = None, domain: str = None, scope_note: str = None,
                dry_run: bool = False):
    """Mint a term for a concept new to the vocabulary, AND adjudicate it in one act.

    The missing half of D-0173. `adjudicate-term --outcome NAMES-NEW` refuses unless the
    term already exists -- "create the term first, then adjudicate NAMES-NEW to it" --
    and nothing created one, so NAMES-NEW was an outcome the CLI documented and could
    not reach. A checker whose satisfying writer does not exist is a trap (CLAUDE.md §8).

    Term and adjudication land together because they are one judgement: *this observed
    phrase names a concept we did not hold, and here is the term for it.* Splitting them
    would permit a term with no provenance, which is the contamination the owner objected
    to on 2026-09-09 -- prior-version containers that exist before the work does.
    """
    canonical_en = (canonical_en or "").strip()
    rationale = (rationale or "").strip()
    if not canonical_en:
        raise Refusal("--canonical-en is required: a term is its name.")
    if not rationale:
        raise Refusal(
            "--rationale is required. Minting a term is an adjudication, and an "
            "adjudication that does not say why cannot be contested.")
    if _VALUE_BEARING.search(canonical_en):
        raise Refusal(
            f"--canonical-en {canonical_en!r} REFUSED: it carries a number, a comparator "
            f"or a min/max word, so it states a determination in its own name.\n"
            f"That is the defect the item layer was deleted for -- a container that "
            f"announces its answer predisposes every finding filed into it "
            f"(DR-2026-08-19 §1.1: 42 of 93 item names embedded a determination).\n"
            f"Name the PARAMETER, not the value: 'corridor width', not "
            f"'corridor width >=1200 mm'. The value belongs in the determination.")
    with connect(dry_run) as conn:
        obs = conn.execute("SELECT observation_id, surface_form, ref_id FROM observed_terms "
                           "WHERE observation_id=?", [from_observation]).fetchone()
        if obs is None:
            raise Refusal(
                f"observation {from_observation}: no such observed term. A term is minted "
                f"FROM an observed phrase (db.py observe-term), never from nothing -- that "
                f"is what makes the vocabulary an output of the work rather than a "
                f"presupposition.")
        clash = conn.execute("SELECT term_id, canonical_en FROM terms "
                             "WHERE lower(canonical_en)=lower(?)", [canonical_en]).fetchone()
        if clash:
            raise Refusal(
                f"{canonical_en!r} is already TERM {clash['term_id']} "
                f"({clash['canonical_en']!r}). That makes this NAMES-EXISTING, not "
                f"NAMES-NEW:\n  db.py adjudicate-term --observation-id {from_observation} "
                f"--outcome NAMES-EXISTING --term-id {clash['term_id']} --rationale ...")
        # Computed, never stored -- a counter table would be a second home for a fact
        # the column already states (rule 5). Same discipline as dbcore.next_ref_id.
        top = conn.execute("SELECT max(CAST(substr(term_id,6) AS INTEGER)) FROM terms "
                           "WHERE term_id LIKE 'TERM-___'").fetchone()[0] or 0
        term_id = f"TERM-{top + 1:03d}"
        row = {"term_id": term_id, "canonical_en": canonical_en,
               "definition": definition, "domain": domain, "scope_note": scope_note}
        row.update(dbcore.stamp_for(conn, "terms", session))
        conn.execute(f"INSERT INTO terms ({','.join(row)}) "
                     f"VALUES ({','.join('?'*len(row))})", list(row.values()))
        adj = {"observation_id": from_observation, "outcome": "NAMES-NEW",
               "term_id": term_id, "rationale": rationale}
        adj.update(dbcore.stamp_for(conn, "term_adjudications", session))
        cur = conn.execute(f"INSERT INTO term_adjudications ({','.join(adj)}) "
                           f"VALUES ({','.join('?'*len(adj))})", list(adj.values()))
        return {"term_id": term_id, "canonical_en": canonical_en,
                "adjudication_id": cur.lastrowid, "from_surface_form": obs["surface_form"],
                "from_ref_id": obs["ref_id"], "dry_run": dry_run}


_MD_CODE = re.compile(r"^MD-[A-Z]+(-[A-Z]+)*$")


def insert_medical(code: str, display_name: str, icd11: str, session: str,
                   description: str = None, icd11_payload: str = None,
                   identity: str = None, relationship: str = None,
                   icf: str = None, role: str = None, mapping_confidence: str = None,
                   note: str = None, dry_run: bool = False):
    """Mint a medical-lens row AND at least one crossing, in one act.

    THE FOURTH LENS. D-0170 (2026-08-27) adopted it on the owner's ruling -- "yes we
    include the medical model too. we give our users the choice of what model they want to
    use to browse the site." `base_taxonomy_medical` was created by migration 065 and had
    no writer for the fortnight since, which is why D-0182's own evidence could count "0
    medical" attachment points. Migration 074 gave it the crossings; this gives it a verb.

    ROW AND CROSSING TOGETHER, on the `insert_term` precedent. A medical row with no
    crossing cannot be reached from any other lens, so the lens cannot switch into it --
    D-0170's structural requirement, still binding even though D-0184 moved the render path
    off traversal. Minting the row alone would satisfy a CHECK and defeat the purpose.

    WHAT IT REFUSES, and why each refusal is the point:

      A CODE OUTSIDE `^MD-[A-Z]+(-[A-Z]+)*$`. Letters only, so no medical code can ever
      match the `\b[A-Z]-[0-9]{2}\b` prior-version item-code shape that CLAUDE.md §7
      warns a grep will hand you. A digit in this namespace would collide with the exact
      surface the owner deleted the item layer to get away from.

      A VALUE-BEARING NAME OR DESCRIPTION, via the same `_VALUE_BEARING` that gates
      `add-term` -- IMPORTED, not retyped, because two copies of one regex is rule 5 in
      miniature. A diagnosis names the subject, never the determination.

      NO CROSSING. `--identity` needs `--relationship`; `--icf` needs both `--role` and
      `--mapping-confidence`; and at least one of the two must be present.

      `--identity ALL`. ALL is a scope marker, not a population, and crossing a diagnosis
      to "everyone" asserts the medical model as the frame rather than offering it as a
      lens -- which is what D-0170's rationale exists to refuse.

      A DUPLICATE CODE, with the existing row named, on the `add-term` NAMES-EXISTING
      precedent: a second row for one concept is the dual home rule 5 forbids.

    icd11_verified_at IS SET ONLY FROM BYTES. `--icd11-payload` must name a file under
    `retrieval-log/` whose content contains every code in `--icd11`; otherwise the column
    stays NULL and NULL means "not verified". This is `retrieval_log.py`'s artefact
    discipline (CLAUDE.md §5(c)) applied to a vocabulary instead of a citation -- the 2026-
    08-19 fabrication was bibliographic fields written from memory past six green gates, and
    an anchor asserted from memory is the same act on a different column.

    WHAT IS DELIBERATELY ABSENT: any writer for `display_name` or `description` that copies
    text from a classification. The anchor points; the prose is ours. That is rule 5, and it
    is also why the licensing question on WHO's terms does not reach these two columns --
    see scratchpad/pr-134-repository-orientation/MEDICAL-LENS-LICENSING-STOP.md.
    """
    if not _MD_CODE.match(code or ""):
        raise Refusal(
            f"--code {code!r} REFUSED: medical codes are ^MD-[A-Z]+(-[A-Z]+)*$ -- letters "
            f"only, no digits.\nA digit here would produce a token matching the prior-"
            f"version item-code shape [A-Z]-NN that CLAUDE.md §7 warns every grep still "
            f"meets. That surface is what the owner deleted the item layer to escape; this "
            f"namespace does not rejoin it.")
    for field, val in (("--display-name", display_name), ("--description", description)):
        if val and _VALUE_BEARING.search(val):
            raise Refusal(
                f"{field} {val!r} REFUSED: it carries a number, a comparator or a min/max "
                f"word, so it states a determination in its own name.\nA diagnosis names "
                f"the SUBJECT. The value belongs in the determination, which the engine "
                f"computes (owner 2026-09-09).")
    if not (icd11 or "").strip():
        raise Refusal(
            "--icd11 REFUSED: empty. argparse requires the flag to be PRESENT but an empty "
            "string satisfied it, and a row whose anchor points nowhere is worse than one "
            "with no anchor at all -- it reads as satisfied.\nThe anchor is the entire reason "
            "this row exists (rule 5: point, do not copy). Give at least one ICD-11 code or "
            "BlockId.")
    if identity and not relationship:
        raise Refusal("--identity given without --relationship. Say HOW the diagnosis "
                      "relates: names | member_of | identity_first.")
    if icf and not (role and mapping_confidence):
        raise Refusal("--icf needs both --role and --mapping-confidence. A crossing whose "
                      "strength is unstated reads as high-predictive to the next reader, "
                      "which is the inference D-0184 measured and rejected.")
    if not identity and not icf:
        raise Refusal(
            "REFUSED: no crossing given. A medical row with no crossing cannot be reached "
            "from any other lens, so the lens cannot switch into it (D-0170's structural "
            "requirement).\nPass --identity/--relationship, or --icf/--role/"
            "--mapping-confidence, or both.")
    if identity == "ALL":
        raise Refusal(
            "--identity ALL REFUSED: ALL is a scope marker, not a population. Crossing a "
            "diagnosis to every population asserts the medical model as the project's "
            "FRAME rather than offering it as one lens among four -- the reading D-0170's "
            "rationale exists to refuse.")

    verified_at = None
    if icd11_payload:
        pay = Path(icd11_payload)
        # READ ARCHIVE MEMBERS, NOT JUST RAW BYTES. The first version of this check
        # substring-matched `pay.read_bytes()`, and the only artefact it will ever be
        # pointed at is WHO's release file — a DEFLATE-COMPRESSED ZIP, in which no code
        # occurs literally. Measured: b"MB56" in the raw zip -> False; in the decompressed
        # member -> True. So the check refused the very payload that proves the anchor,
        # and the ruling it enforces ("verified against the persisted release file at write
        # time") was unexecutable. The MB5 verification of 2026-09-11 02:47 was done by
        # hand in Python and never through this writer, while the record claimed otherwise.
        bodies = _payload_bodies(pay, "--icd11-payload",
                                 "icd11_verified_at is set from BYTES or not at all")
        missing = [c.strip() for c in icd11.split(",")
                   if c.strip() and not any(c.strip() in b for b in bodies)]
        if missing:
            raise Refusal(
                f"--icd11-payload does not contain {missing!r}. REFUSED rather than stamped: "
                f"a payload that does not mention the code verifies nothing, and a "
                f"verification standing with no artefact behind it is the 2026-08-19 shape.")
        # A REAL stamp, not a guarded one. The first draft of this line read
        # `_now() if "_now" in globals() else None`, and _now() does not exist in this
        # module -- so --icd11-payload would have validated the bytes and then written
        # NULL anyway, leaving a verified anchor indistinguishable from an unverified
        # one. A writer that silently does nothing is worse than one that refuses.
        verified_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    with connect(dry_run) as conn:
        dup = conn.execute("SELECT medical_code, display_name FROM base_taxonomy_medical "
                           "WHERE medical_code = ?", (code,)).fetchone()
        if dup:
            raise Refusal(
                f"--code {code!r} REFUSED: already exists as {dup[1]!r}. Minting a second "
                f"row for one concept is the dual home rule 5 forbids; add a crossing to "
                f"the standing row instead.")
        # PRE-CHECK THE CROSSING TARGETS. Without this, a typo'd --identity or --icf
        # reached the INSERT and surfaced as `sqlite3.IntegrityError: FOREIGN KEY
        # constraint failed` with a traceback naming a line number -- while a
        # DOCTRINAL error (--identity ALL) got a full sentence. So the writer explained
        # the subtle mistake and stack-traced the obvious one. That is the exact pattern
        # PR #133 ("db.py's refusals become sentences too") existed to remove, and this
        # writer reintroduced it. Found by driving the CLI, not by reading it.
        # The transaction did roll back, so nothing was corrupted -- the defect was the
        # message, which is still the difference between a user fixing a typo and a user
        # filing a bug.
        if identity:
            if not conn.execute("SELECT 1 FROM populations WHERE population_code = ?",
                                (identity,)).fetchone():
                near = [r[0] for r in conn.execute(
                    "SELECT population_code FROM populations ORDER BY population_code")]
                raise Refusal(
                    f"--identity {identity!r} REFUSED: not a population_code. The identity "
                    f"lens is `populations`, and its live vocabulary is: {', '.join(near)}")
        if icf:
            # INVERTED 2026-09-13, and the old message is worth remembering because it
            # stated the ruled-out state as doctrine: it read "specifications.icf_code FKs
            # to `axes`, NOT to raw ICF b/d/e codes … a raw code would be refused by the
            # FK". That was true of the schema and is now exactly backwards. Owner ruling,
            # same day: "'AX-' for ICF should never ever exist anywhere", then "keep the
            # ICF lens, give it real ICF codes". Migration 081 re-pointed all six icf_code
            # columns at `base_icf`, so a raw ICF code is the ONLY thing accepted here and
            # an AX- demand code is what the FK now refuses.
            if not dbcore.exists(conn, "base_icf", "icf_code", icf):
                raise Refusal(
                    f"--icf {icf!r} REFUSED: not in `base_icf`, the ICF registry the lens "
                    f"points at since migration 081.\n"
                    f"If this is a real ICF code the registry does not yet hold, mint it:\n"
                    f"  db.py add-icf-code --icf-code {icf} --session ...\n"
                    f"If it is an AX- demand code, it is not an ICF code and never was "
                    f"(owner ruling 2026-09-13).")
        row = {"medical_code": code, "display_name": display_name,
               "description": description, "icd11_anchors": icd11,
               "icd11_verified_at": verified_at, "notes": note}
        row = {k: v for k, v in row.items() if v is not None}
        row.update(dbcore.stamp_for(conn, "base_taxonomy_medical", session))
        conn.execute(
            f"INSERT INTO base_taxonomy_medical ({','.join(row)}) "
            f"VALUES ({','.join('?' * len(row))})", tuple(row.values()))
        crossings = []
        if identity:
            c = {"identity_code": identity, "medical_code": code,
                 "relationship": relationship, "notes": note}
            c = {k: v for k, v in c.items() if v is not None}
            c.update(dbcore.stamp_for(conn, "identity_medical_map", session))
            conn.execute(f"INSERT INTO identity_medical_map ({','.join(c)}) "
                         f"VALUES ({','.join('?' * len(c))})", tuple(c.values()))
            crossings.append({"lens": "identity", "code": identity,
                              "relationship": relationship})
        if icf:
            c = {"icf_code": icf, "medical_code": code, "role": role,
                 "mapping_confidence": mapping_confidence, "notes": note}
            c = {k: v for k, v in c.items() if v is not None}
            c.update(dbcore.stamp_for(conn, "icf_medical_map", session))
            conn.execute(f"INSERT INTO icf_medical_map ({','.join(c)}) "
                         f"VALUES ({','.join('?' * len(c))})", tuple(c.values()))
            crossings.append({"lens": "icf", "code": icf, "role": role,
                              "mapping_confidence": mapping_confidence})
        return {"medical_code": code, "display_name": display_name,
                "icd11_anchors": icd11,
                "icd11_verified_at": verified_at,
                "anchor_verified": bool(verified_at),
                "crossings": crossings, "dry_run": dry_run}


def insert_parameter(term_id: str, session: str, notes: str = None,
                     dry_run: bool = False):
    """Promote an adjudicated term into `base_parameters` — THE SUBJECT of a determination.

    Migration 071 put the parameter at base and re-keyed `specifications` onto it
    (owner 2026-08-26: "the judgment object is the canonical parameter"). The table
    shipped writable — `dbcore.WRITABLE_TABLES` names it — with nothing that could write
    a row, so no parameter_id could be minted and `specifications` stayed unwritable in
    practice. A capturable table with no writer is the mirror of the trap `insert_term`
    was built to close: there, a checker whose satisfying writer did not exist.

    WHAT IT REFUSES, and why each refusal is the point:

    * A term that does not exist. The FK would say `FOREIGN KEY constraint failed`,
      which names neither the term nor the fix.
    * A DECLINED term (`parameter_declinations`, migration 101). Someone judged it not a
      design parameter and said why; promoting it would leave two answers to one
      question. Reversing a declination is a recorded decision, not a promotion, so the
      refusal names the standing declination and there is no un-decline verb.
    DELIBERATELY NOT REFUSED: a term with no adjudication. The first cut of this writer
    demanded a NAMES-NEW/NAMES-EXISTING row, on the reasoning that a parameter is the
    output of judgment (D-0173). Exercised against a scratch copy, that refusal blocked
    all 88 live terms, because `term_adjudications` holds 0 rows and the vocabulary was
    seeded by dedicated sessions in May and July — before observe/adjudicate existed.
    Two provenances are both legitimate: a term MINTED from an observation carries
    NAMES-NEW by construction, and a term that IS the base vocabulary has no observation
    to point at. Gating on the first would have made this a writer that can never write,
    which is the trap `insert_term` was built to close, wearing a new coat. The result
    reports which provenance a promotion had; that is information for the operator, not
    a gate.
    * A second parameter for the same term. The column is UNIQUE, so the database
      refuses it anyway; this says WHICH parameter already holds the term, because a
      dual home is rule 5's central prohibition and the fix is to use the existing one.
    * A value-bearing name. `add-term` already refuses one, but a term minted before
      that guard existed could still carry it, and promotion to parameter is the last
      gate before the name becomes a determination's subject.

    DELIBERATELY ABSENT, and must stay absent: no --status and no --merged-into. A
    parameter is created active. Merging one into another is a different act on an
    existing row — it needs its own verb, its own rationale, and a sweep of whatever
    points at the loser. Letting creation mint a row already marked `merged` would
    permit a parameter that was never alive, which the table's own CHECK cannot catch
    because the shape is legal.
    """
    term_id = (term_id or "").strip()
    if not term_id:
        raise Refusal("--term-id is required: a parameter is a pointer at a term.")
    with connect(dry_run) as conn:
        term = conn.execute("SELECT term_id, canonical_en FROM terms WHERE term_id=?",
                            [term_id]).fetchone()
        if term is None:
            raise Refusal(
                f"{term_id!r}: no such term. A parameter points at a term, and the term "
                f"comes from an observed phrase:\n"
                f"  db.py observe-term ...   then   db.py add-term --from-observation N "
                f"--canonical-en '...' --rationale '...'")
        declined = conn.execute(
            "SELECT reason, created_at, created_by_session FROM parameter_declinations "
            "WHERE term_id=?", [term_id]).fetchone()
        if declined:
            raise Refusal(
                f"{term_id} ({term['canonical_en']!r}) was DECLINED as a parameter by "
                f"{declined['created_by_session']} at {declined['created_at']}: "
                f"{declined['reason']!r}.\n"
                f"Reversing a declination is a recorded decision "
                f"(governance/decision-protocol.md) and a compensating migration, not a "
                f"promotion. Nothing was written.")
        if _VALUE_BEARING.search(term["canonical_en"]):
            raise Refusal(
                f"{term_id} is named {term['canonical_en']!r}, which carries a number, a "
                f"comparator or a min/max word — it states a determination in its own "
                f"name.\nA parameter is what is under determination, never the answer. "
                f"Correct the term's canonical_en first; promoting it would make the "
                f"answer the subject.")
        adj = conn.execute(
            "SELECT adjudication_id, outcome FROM term_adjudications "
            "WHERE term_id=? AND outcome IN ('NAMES-NEW','NAMES-EXISTING') "
            "ORDER BY adjudication_id LIMIT 1", [term_id]).fetchone()
        clash = conn.execute(
            "SELECT p.parameter_id, p.status FROM base_parameters p WHERE p.term_id=?",
            [term_id]).fetchone()
        if clash:
            raise Refusal(
                f"{term_id} is already parameter {clash['parameter_id']} "
                f"(status {clash['status']}). One parameter per term — a second row is "
                f"the dual home rule 5 forbids.\n"
                f"Key the determination on parameter_id {clash['parameter_id']}.")
        row = {"term_id": term_id, "status": "active", "notes": notes}
        row.update(dbcore.stamp_for(conn, "base_parameters", session))
        cur = conn.execute(f"INSERT INTO base_parameters ({','.join(row)}) "
                           f"VALUES ({','.join('?'*len(row))})", list(row.values()))
        return {"parameter_id": cur.lastrowid, "term_id": term_id,
                "canonical_en": term["canonical_en"], "status": "active",
                "provenance": ("adjudicated" if adj else "base-vocabulary"),
                "adjudicated_by": (adj["adjudication_id"] if adj else None),
                "outcome": (adj["outcome"] if adj else None),
                "dry_run": dry_run}


def decline_parameter(term_id: str, reason: str, session: str, dry_run: bool = False):
    """Record that a term is NOT a design parameter, and why — `parameter_declinations`.

    GAP-061's prerequisite. A term judgment has named had one recordable fate: promotion
    (`add-parameter`). A term naming something other than a quantity under determination
    — a population lens term ('wheelchair user'), an element whose quantities are
    separate terms ('ramp'), a method — had none, so "not yet looked at" and "looked at
    and judged not a parameter" read the same. This records the second answer, with its
    warrant, so the judgement can be found and contested.

    A SEPARATE TABLE, NOT A `base_parameters.status` VALUE (migration 101): a declined
    term never holds a parameter_id that an extraction or a determination could point at.

    WHAT IT REFUSES, and why each refusal is the point:

    * A blank --term-id.
    * A term that does not exist. The FK would say `FOREIGN KEY constraint failed`,
      which names neither the term nor the route a term comes from.
    * A blank reason. A declination that cannot say why cannot be contested; the schema
      CHECK refuses it too, but would say so as an IntegrityError.
    * A term that is already a parameter, whatever its status. Declining it would leave
      that parameter_id standing beside a record saying the term is not a parameter —
      two answers to one question. Retiring a parameter is a different act on the
      parameter's own row.
    * A term already declined. One row per term (the PRIMARY KEY); the refusal names the
      standing reason and session, because the fix is to read that judgement, not to
      restate it.

    DELIBERATELY NOT REFUSED: a term with no adjudication, for the reason
    `insert_parameter` gives — the base vocabulary predates observe/adjudicate, and a gate
    on adjudication would make a writer that cannot write.

    DELIBERATELY ABSENT: an un-decline verb. Reversing a declination is a recorded
    decision and a compensating migration, and nothing reads an un-decline yet (CLAUDE.md
    §8). `insert_parameter` refuses a declined term and names this row.
    """
    term_id = (term_id or "").strip()
    if not term_id:
        raise Refusal("--term-id is required: a declination is a judgement about a term.")
    reason = dbcore.require_reason(
        reason, term_id, why="A declination that cannot say why cannot be contested.")
    with connect(dry_run) as conn:
        term = conn.execute("SELECT term_id, canonical_en FROM terms WHERE term_id=?",
                            [term_id]).fetchone()
        if term is None:
            raise Refusal(
                f"{term_id!r}: no such term. Only a term can be declined, and a term comes "
                f"from an observed phrase:\n"
                f"  db.py observe-term ...   then   db.py add-term --from-observation N "
                f"--canonical-en '...' --rationale '...'")
        param = conn.execute(
            "SELECT parameter_id, status FROM base_parameters WHERE term_id=?",
            [term_id]).fetchone()
        if param:
            raise Refusal(
                f"{term_id} ({term['canonical_en']!r}) is already parameter "
                f"{param['parameter_id']} (status {param['status']}). Declining it would "
                f"leave that parameter_id standing beside a record saying the term is not "
                f"a parameter.\n"
                f"Retiring a parameter is a different act on parameter "
                f"{param['parameter_id']}'s own row, not a declination. Nothing was written.")
        prior = conn.execute(
            "SELECT reason, created_at, created_by_session FROM parameter_declinations "
            "WHERE term_id=?", [term_id]).fetchone()
        if prior:
            raise Refusal(
                f"{term_id} ({term['canonical_en']!r}) is already declined, by "
                f"{prior['created_by_session']} at {prior['created_at']}: "
                f"{prior['reason']!r}.\n"
                f"One declination per term. If that reason is wrong, that is a decision "
                f"(governance/decision-protocol.md), not a second row. Nothing was written.")
        row = {"term_id": term_id, "reason": reason}
        row.update(dbcore.stamp_for(conn, "parameter_declinations", session))
        conn.execute(f"INSERT INTO parameter_declinations ({','.join(row)}) "
                     f"VALUES ({','.join('?'*len(row))})", list(row.values()))
        return {"term_id": term_id, "canonical_en": term["canonical_en"],
                "declined": True, "reason": reason,
                "created_by_session": row.get("created_by_session"),
                "dry_run": dry_run}


def set_parameter_direction(*, parameter_id: int, direction: str, rationale: str,
                           session: str, dry_run: bool = False):
    """Record which way is BETTER FOR A DISABLED PERSON on this parameter.

    THE JUDGMENT THE ENGINE CANNOT MAKE, and the one it has been blocked on since
    2026-07-21. The most-accommodating rule (evidence-architecture.md, owner directive,
    Option A) says a determination anchors on the best-for-the-user value "read per the
    parameter's accessibility direction -- the widest minimum corridor, but the LOWEST
    maximum threshold height and the GENTLEST maximum ramp slope". Which of those a
    parameter is cannot be derived from its name, its unit, or its values: it is a fact
    about what the parameter means for a person, and somebody has to state it.

    So this is CLAUDE.md rule 8's other half in one verb. The vocabulary comes from the
    schema (`dbcore.check_declared`), the answer is a judgment, and the WARRANT is required
    beside it -- a direction with no stated reason is an assertion about disabled people's
    needs with nothing behind it, and the schema refuses that pair too (migration 078).

    `contested` IS AN ANSWER, not a refusal to answer. DR-2026-07-21 section 5: where the
    direction is population-contested -- flush thresholds aid wheeled mobility but remove
    the tactile cues cane users rely on, brighter light aids low vision but harms
    photosensitive users -- most-accommodating selection is INAPPLICABLE and no single value
    is anchored. Recording `contested` is what stops the engine silently picking a winner
    between two populations; leaving the field NULL would let a later session mistake "not
    yet examined" for "nothing to see".

    RE-STATING A DIRECTION IS REFUSED. The direction conditions every determination already
    computed for the parameter, so changing it silently re-points those determinations at a
    rule they were not computed under. Retire the parameter or open a decision; do not
    overwrite.
    """
    if not (rationale or "").strip():
        raise Refusal(
            "--rationale is required: a direction is a claim about what serves disabled "
            "people on this parameter, and one with no stated reason cannot be reviewed, "
            "disputed or superseded. The schema refuses the pair too (migration 078).")
    with dbcore.connect(dry_run) as conn:
        row = conn.execute(
            "SELECT p.parameter_id, t.canonical_en, p.accessibility_direction, "
            "p.direction_rationale FROM base_parameters p JOIN terms t "
            "ON t.term_id = p.term_id WHERE p.parameter_id = ?", [parameter_id]).fetchone()
        if row is None:
            raise Refusal(
                f"parameter_id {parameter_id}: no such parameter. Mint one from a term "
                f"first: db.py add-parameter --term-id TERM-NNN --session ...")
        if row["accessibility_direction"]:
            raise Refusal(
                f"parameter {parameter_id} ({row['canonical_en']!r}) already carries "
                f"direction {row['accessibility_direction']!r}: "
                f"{row['direction_rationale']!r}.\nA direction conditions every "
                f"determination computed for the parameter, so overwriting it silently "
                f"re-points those at a rule they were not computed under. If it is wrong, "
                f"that is a decision (governance/decision-protocol.md), not an amendment.")
        dbcore.check_declared(conn, "base_parameters", "accessibility_direction",
                              direction, "set-parameter-direction")
        stamp = dbcore.stamp_for(conn, "base_parameters", session)
        sets = ["accessibility_direction = ?", "direction_rationale = ?"]
        vals = [direction, rationale.strip()]
        for k, v in stamp.items():
            if k.startswith("updated"):
                sets.append(f"{k} = ?")
                vals.append(v)
        conn.execute("UPDATE base_parameters SET " + ", ".join(sets)
                     + " WHERE parameter_id = ?", vals + [parameter_id])
        return {"parameter_id": parameter_id, "canonical_en": row["canonical_en"],
                "accessibility_direction": direction, "direction_rationale": rationale.strip(),
                "dry_run": dry_run}


# --- H3/H4: the two tables migration 080 created ---------------------------------
# Both shipped with no writer, which is the defect `insert_parameter` and
# `insert_medical` were each written to close on their own table: a capturable table
# with nothing that can write it is unreachable through the sanctioned path, and the
# next session reaches for hand SQL (CLAUDE.md section 4 -- "if you find one it cannot,
# that is a coverage bug to fix, not a licence to bypass").

#: The shape an ICF code takes, kept ONLY to tell a new mint from a typo in
#: `add-icf-code`. It is no longer the membership test anywhere: migration 081 created
#: `base_icf` and re-pointed all six `icf_code` columns at it, so membership is the FK's
#: job now -- which is exactly what the block this replaced promised would happen ("when
#: an ICF registry lands, this becomes an FK and the guard goes").
#:
#: Owner rulings 2026-09-13, both: "'AX-' for ICF should never ever exist anywhere", and
#: then, on the fork that opened, "keep the ICF lens, give it real ICF codes".
_ICF_CODE_RE = re.compile(r"^[bdes]\d{3}[0-9]*(?:\s*[-\u2013\u2014]\s*[bdes]\d{3}[0-9]*)?$")


def insert_population_icf_link(*, population: str, icf_code: str, mechanism: str,
                               mapping_confidence: str, provenance: str,
                               notes: str = None, session: str, dry_run: bool = False):
    """Record that a population has a functional deficit in an ICF activity (H3).

    THE TABLE IS SIMULTANEOUSLY THE FORWARD MAP AND THE SUBSTRATE FOR REVERSE-MAPPING,
    which is doctrine's argument for it: reverse-mapping "is what would have flagged
    DEAF's absence from the corridor item's population links MECHANICALLY rather than
    by eye". A forward map with no writer can only ever hold what one migration put
    there, so the reverse direction would go stale the first time the taxonomy moved.

    WHAT IT REFUSES:

    * A population that is not live. The FK says `FOREIGN KEY constraint failed`, which
      names neither the code nor the fix -- and the codes that fail here are usually
      RETIRED ones (the pre-DR-2026-07-23 set the functional-deficit-auditor taught for
      fourteen months), so the refusal points at the crosswalk rather than at the FK.
    * An `icf_code` that is not in `base_icf`. REWRITTEN 2026-09-13: this was a shape
      guard, because at the time there was no ICF registry to point at and free text is
      where a code from another lens gets pasted by accident. Migration 081 created the
      registry and gave this column its FK, so membership is now a real check rather than
      a plausibility one -- and the refusal names the mint verb, because a bare
      `FOREIGN KEY constraint failed` names neither the code nor the fix.
    * An empty `provenance`. The column is NOT NULL, so the database catches a missing
      one -- but not `''`, and a mapping with no provenance is the skill prose again,
      in a table. That is the exact state migration 080 moved the mapping OUT of.
    * A duplicate (population, code, mechanism). UNIQUE catches it; this says which row
      already holds it, because the fix is to read that row rather than add another.

    DELIBERATELY NOT REFUSED, and it must stay that way: a population that already has
    links, and a (population, icf_code) pair that already exists under a DIFFERENT
    mechanism. SCI reaches its codes "biomechanically + autonomically" and both are
    real; the UNIQUE is on the triple for exactly that reason, and collapsing them
    would lose the distinction the mechanism column exists for.
    """
    population = (population or "").strip()
    icf_code = (icf_code or "").strip()
    mechanism = (mechanism or "").strip()
    provenance = (provenance or "").strip()
    if not provenance:
        raise Refusal(
            "--provenance is required and may not be blank. A mapping with no "
            "provenance is skill prose in a table, which is the state migration 080 "
            "moved this mapping out of. Name the source: a ref_id for a row derived "
            "from a study, or the promotion that produced it.")
    with connect(dry_run) as conn:
        if not dbcore.exists(conn, "base_icf", "icf_code", icf_code):
            raise Refusal(
                f"{icf_code!r} is not in `base_icf`, the ICF registry this column has FK'd "
                f"into since migration 081 -- so the bare FK error would say only "
                f"'FOREIGN KEY constraint failed', which names neither the code nor the "
                f"fix.\n"
                f"If it is a real ICF code the registry does not hold yet, mint it first:\n"
                f"  db.py add-icf-code --icf-code {icf_code} --session ...\n"
                f"If it is an AX- demand code, it is not an ICF code and never was (owner "
                f"ruling 2026-09-13).")
        if not dbcore.exists(conn, "populations", "population_code", population):
            live = sorted(r[0] for r in
                          conn.execute("SELECT population_code FROM populations"))
            raise Refusal(
                f"{population!r} is not a live population code. The taxonomy was "
                f"replaced by DR-2026-07-23; a retired code (UPL, VIS, OFS, ABI, ASD, "
                f"PCS, NEU, DBL, ...) must be crosswalked before it can be written.\n"
                f"Live codes: {', '.join(live)}")
        dbcore.check_declared(conn, "population_icf_links", "mapping_confidence",
                              mapping_confidence, "add-population-icf-link")
        clash = conn.execute(
            "SELECT link_id, provenance FROM population_icf_links "
            "WHERE population_code=? AND icf_code=? AND mechanism=?",
            [population, icf_code, mechanism]).fetchone()
        if clash:
            raise Refusal(
                f"link {clash['link_id']} already maps {population} -> {icf_code} by "
                f"this mechanism (provenance {clash['provenance']!r}). One row per "
                f"(population, code, mechanism) -- a second is the dual home rule 5 "
                f"forbids. A DIFFERENT mechanism is a different row and is allowed.")
        row = {"population_code": population, "icf_code": icf_code,
               "mechanism": mechanism, "mapping_confidence": mapping_confidence,
               "provenance": provenance, "notes": notes}
        row.update(dbcore.stamp_for(conn, "population_icf_links", session))
        cur = conn.execute(f"INSERT INTO population_icf_links ({','.join(row)}) "
                           f"VALUES ({','.join('?'*len(row))})", list(row.values()))
        return {"link_id": cur.lastrowid, "population_code": population,
                "icf_code": icf_code, "mechanism": mechanism,
                "mapping_confidence": mapping_confidence, "dry_run": dry_run}


def insert_icf_code(*, icf_code: str, title: str = None, title_source: str = None,
                    title_payload: str = None, notes: str = None, session: str,
                    dry_run: bool = False):
    """Mint one ICF code into `base_icf` — the registry the ICF lens points at.

    OWNER RULING 2026-09-13: "keep the ICF lens, give it real ICF codes", answering the
    fork opened by the same day's "'AX-' for ICF should never ever exist anywhere".
    Migration 081 built the registry and re-pointed all six `icf_code` columns at it; this
    is how it grows afterwards.

    WHAT IS DERIVED RATHER THAN ASKED FOR (CLAUDE.md rule 8). `component` is the code's
    first letter and `is_range` is whether it spans two codes. Both are computable from
    the code itself, so asking for them would be inviting a row whose component disagrees
    with its own identifier.

    THE TITLE IS THE PART THAT CANNOT BE TYPED FROM MEMORY, and this is CLAUDE.md 5(c)
    before the fact rather than after. On 2026-08-19 five sources were stored with invented
    co-authors and six gates passed them, because each asked whether a field was POPULATED
    and never whether it was TRUE. An ICF title recalled rather than read is the same act
    in a smaller field. So `title` may only arrive with a `title_source`, which the schema
    enforces too — and when that source is a persisted payload, the title is checked
    against its BYTES here, the same way `add-medical --icd11-payload` checks an ICD-11
    anchor. A title with no payload is accepted and records its document, which is weaker
    and is meant to read as weaker.

    A CODE WITH NO TITLE IS FINE and is the honest default: 43 of the 72 seeded codes are
    in that state because nothing in this repository names them (GAP-ICF-TITLES). CLAUDE.md
    section 6 wants codes AND names, so an untitled code is a gap — but a gap is not a lie,
    and `set-icf-title` is how it closes.
    """
    icf_code = (icf_code or "").strip()
    if not _ICF_CODE_RE.match(icf_code):
        raise Refusal(
            f"{icf_code!r} is not shaped like an ICF code. Expected b/d/e/s followed by "
            f"digits, optionally a range (e.g. 'd450', 'b1342', 'd310\u2013d329').\n"
            f"If this is an AX- demand code: it is not an ICF code and never was (owner "
            f"ruling 2026-09-13), and `base_icf`'s own CHECK refuses the shape too.")
    if title and not (title_source or title_payload):
        raise Refusal(
            "--title requires --title-source (or --title-payload). A title with no source "
            "is a title from memory, which is the 2026-08-19 fabrication in a smaller "
            "field. The schema refuses the pair as well.")
    with connect(dry_run) as conn:
        clash = conn.execute("SELECT icf_code, title FROM base_icf WHERE icf_code=?",
                             [icf_code]).fetchone()
        if clash:
            raise Refusal(
                f"{icf_code} is already in base_icf (title {clash['title']!r}). One row per "
                f"code — a second is the dual home rule 5 forbids. To add or correct a "
                f"title, use `db.py set-icf-title`.")
        if title and title_payload:
            bodies = _payload_bodies(title_payload, "--title-payload",
                                     "a title is verified from BYTES or it records a "
                                     "document instead")
            if not any(title in b for b in bodies):
                raise Refusal(
                    f"--title {title!r} does not appear in {title_payload}. The payload is "
                    f"what makes this a verified title rather than a remembered one; if the "
                    f"wording differs, use the payload's wording.")
            title_source = f"payload:{title_payload}"
        row = {"icf_code": icf_code, "component": icf_code[0],
               "is_range": 1 if re.search(r"[-\u2013\u2014]", icf_code) else 0,
               "title": title, "title_source": title_source, "notes": notes}
        row.update(dbcore.stamp_for(conn, "base_icf", session))
        conn.execute(f"INSERT INTO base_icf ({','.join(row)}) "
                     f"VALUES ({','.join('?'*len(row))})", list(row.values()))
        return {"icf_code": icf_code, "component": icf_code[0],
                "is_range": row["is_range"], "title": title,
                "title_source": title_source,
                "title_verified": bool(title and title_payload), "dry_run": dry_run}


def set_icf_title(*, icf_code: str, title: str, title_source: str = None,
                  title_payload: str = None, session: str, dry_run: bool = False):
    """Give a seeded ICF code the name CLAUDE.md section 6 requires it to be used with.

    GAP-ICF-TITLES is the subject: 43 of the 72 codes migration 081 seeded carry no title,
    because nothing in this repository states one and supplying it from memory is the act
    CLAUDE.md 5(c) forbids. This is the named path for closing that — retrieve the titles,
    persist the payload under `retrieval-log/`, and write them from the bytes.

    OVERWRITING A TITLE IS REFUSED. A title is a fact about an external classification, not
    a field to keep tidy; replacing one silently would erase whoever established it and the
    payload they established it from. A correction is a different act and owes its own
    reason.
    """
    icf_code = (icf_code or "").strip()
    title = (title or "").strip()
    if not title:
        raise Refusal("--title is required and may not be blank.")
    if not (title_source or title_payload):
        raise Refusal(
            "--title-source or --title-payload is required. A title with no source is a "
            "title from memory; the schema refuses the pair too.")
    with connect(dry_run) as conn:
        row = conn.execute(
            "SELECT icf_code, title, title_source FROM base_icf WHERE icf_code=?",
            [icf_code]).fetchone()
        if row is None:
            raise Refusal(
                f"{icf_code!r} is not in base_icf. Mint it first:\n"
                f"  db.py add-icf-code --icf-code {icf_code} --session ...")
        if row["title"]:
            raise Refusal(
                f"{icf_code} is already titled {row['title']!r} (source "
                f"{row['title_source']!r}). Overwriting would erase whoever established it "
                f"and the payload they established it from. A correction is a different "
                f"act and owes its own reason.")
        if title_payload:
            bodies = _payload_bodies(title_payload, "--title-payload",
                                     "a title is verified from BYTES or it records a "
                                     "document instead")
            if not any(title in b for b in bodies):
                raise Refusal(
                    f"--title {title!r} does not appear in {title_payload}. If the "
                    f"classification words it differently, use its wording.")
            title_source = f"payload:{title_payload}"
        conn.execute("UPDATE base_icf SET title=?, title_source=? WHERE icf_code=?",
                     [title, title_source, icf_code])
        return {"icf_code": icf_code, "title": title, "title_source": title_source,
                "title_verified": bool(title_payload), "dry_run": dry_run}


def raise_determination_gate(*, parameter_id: int, verdict: str, detail: str,
                             identity: str = None, trigger_ref_id: str = None,
                             trigger_tier: int = None, trigger_evidence_type: str = None,
                             session: str, dry_run: bool = False):
    """Raise an H4 gate: a finding that caps a cell at `provisional` until resolved.

    THE GATE IS A ROW, NOT A FLAG, and that is the first of doctrine's three
    disciplines: "the gate binds ONLY WHERE A CHECK HAS ACTUALLY RUN -- no silent
    pretence of coverage." Zero rows means zero cells gated, which is the correct
    reading of "no check has run" rather than a gap.

    THE STRENGTH OF THE TRIGGER IS DERIVED WHEREVER IT CAN BE (CLAUDE.md rule 8), and
    this is the second discipline: "gate rows carry the tier and type of the triggering
    source, so a grey-tier CONTRADICTS cannot pin a T1-anchored cell indefinitely and
    thereby INVERT THE LADDER." A tier that an operator typed is a tier that can be
    typed wrong, and typing it wrong is precisely how the ladder gets inverted. So:

    * with --trigger-ref-id, tier and evidence_type are READ from that source and
      --trigger-tier / --trigger-evidence-type are REFUSED. The pointer supplies them;
      passing them too would be a second home for a fact the source already states
      (rule 5), and the same refusal `insert_economics_entry` makes for --year/--journal
      on an entry that carries a ref_id.
    * without one, both are REQUIRED. An audit-raised gate (an FDA UNLINKED on a
      structural absence) has no source to read, so the operator is stating the strength
      of their own finding -- explicitly, where a reader can see it was asserted rather
      than derived.

    RESOLUTION IS A SEPARATE VERB, deliberately. `resolve-determination-gate` exists
    because resolution "is a NAMED PATH -- evidence-auditor adjudication recorded on the
    cell together with its rationale -- so no cell sits at `provisional` with no owner of
    resolution". Letting this verb create an already-resolved row would permit a gate
    that never bound anything, which the table's own CHECK cannot catch because the shape
    is legal -- the same reason `add-parameter` takes no --status.
    """
    detail = (detail or "").strip()
    if not detail:
        raise Refusal(
            "--detail is required and may not be blank. A gate that cannot say what it "
            "found is a cell pinned at provisional for no stated reason, which is the "
            "deadlock the resolution discipline exists to prevent.")
    if trigger_ref_id and (trigger_tier is not None or trigger_evidence_type):
        raise Refusal(
            "--trigger-tier / --trigger-evidence-type are refused alongside "
            "--trigger-ref-id. The source states both, and this row POINTS at the "
            "source (rule 5); they are read from it. A typed tier is a tier that can be "
            "typed wrong, and a wrong one inverts the ladder the gate exists to protect.")
    if not trigger_ref_id and (trigger_tier is None or not trigger_evidence_type):
        raise Refusal(
            "a gate with no --trigger-ref-id must state --trigger-tier and "
            "--trigger-evidence-type. Doctrine requires every gate to carry the strength "
            "of what raised it, so a grey-tier finding cannot pin a T1-anchored cell. A "
            "gate that cannot say how strong its trigger was inverts the ladder by "
            "omission.")
    with connect(dry_run) as conn:
        param = conn.execute(
            "SELECT parameter_id, status, merged_into FROM base_parameters "
            "WHERE parameter_id=?", [parameter_id]).fetchone()
        if param is None:
            raise Refusal(
                f"parameter_id {parameter_id}: no such parameter. Mint one from a term:\n"
                f"  db.py add-parameter --term-id TERM-NNN --session ...")
        if param["status"] != "active":
            raise Refusal(
                f"parameter {parameter_id} is {param['status']}"
                + (f" (merged into {param['merged_into']})" if param["merged_into"] else "")
                + ". Gating a parameter that no longer stands on its own pins cells "
                  "nobody will look at.")
        if identity and not dbcore.exists(conn, "populations", "population_code", identity):
            raise Refusal(
                f"{identity!r} is not a live population code. Omit --identity to raise "
                f"the gate against EVERY lens on this parameter, which is what an audit "
                f"that does not yet know which cells exist should do.")
        dbcore.check_declared(conn, "determination_gates", "verdict", verdict,
                              "raise-determination-gate")
        if trigger_ref_id:
            src = conn.execute(
                "SELECT ref_id, tier, evidence_type FROM evidence_sources WHERE ref_id=?",
                [trigger_ref_id]).fetchone()
            if src is None:
                raise Refusal(f"{trigger_ref_id!r}: no such source.")
            if src["tier"] is None or not src["evidence_type"]:
                raise Refusal(
                    f"{trigger_ref_id} carries tier={src['tier']!r} "
                    f"evidence_type={src['evidence_type']!r}. A gate reads its strength "
                    f"from the source, and this source does not state it -- so the gate "
                    f"cannot be raised on it without asserting a strength nobody "
                    f"established. Fix the source, or raise the gate without a ref_id and "
                    f"state the strength as your own finding.")
            trigger_tier, trigger_evidence_type = src["tier"], src["evidence_type"]
        row = {"parameter_id": parameter_id, "identity_code": identity,
               "verdict": verdict, "trigger_ref_id": trigger_ref_id,
               "trigger_tier": trigger_tier,
               "trigger_evidence_type": trigger_evidence_type, "detail": detail,
               "raised_at": dbcore.now(), "raised_by_session": session}
        cur = conn.execute(f"INSERT INTO determination_gates ({','.join(row)}) "
                           f"VALUES ({','.join('?'*len(row))})", list(row.values()))
        return {"gate_id": cur.lastrowid, "parameter_id": parameter_id,
                "identity_code": identity, "verdict": verdict,
                "trigger_tier": trigger_tier,
                "trigger_evidence_type": trigger_evidence_type,
                "trigger_strength_source": ("read from " + trigger_ref_id
                                            if trigger_ref_id else "asserted by operator"),
                "dry_run": dry_run}


def resolve_determination_gate(*, gate_id: int, rationale: str, session: str,
                               dry_run: bool = False):
    """Close an H4 gate by the named path, so the cell it pins has an owner.

    The third discipline, and the one that stops a gate becoming a deadlock: "resolution
    is a NAMED PATH -- evidence-auditor adjudication recorded on the cell together with
    its rationale -- so no cell sits at `provisional` with no owner of resolution." The
    schema already refuses a partial resolution (resolved_at, resolved_by_session and
    resolution_rationale arrive together or not at all); this verb is what makes the
    complete one reachable without hand SQL.

    RE-RESOLVING IS REFUSED. A resolved gate that is resolved again would overwrite the
    rationale of whoever actually adjudicated it, and the history of a cell's release is
    the only evidence that the release was considered. Reopening is a different act and
    owes its own verb and its own reason.
    """
    rationale = (rationale or "").strip()
    if not rationale:
        raise Refusal(
            "--rationale is required and may not be blank. Resolution is a NAMED PATH; a "
            "gate released with no stated reason is a cell let through by nobody.")
    with connect(dry_run) as conn:
        g = conn.execute(
            "SELECT gate_id, parameter_id, verdict, resolved_at, resolved_by_session "
            "FROM determination_gates WHERE gate_id=?", [gate_id]).fetchone()
        if g is None:
            raise Refusal(f"gate_id {gate_id}: no such gate.")
        if g["resolved_at"]:
            raise Refusal(
                f"gate {gate_id} was already resolved at {g['resolved_at']} by "
                f"{g['resolved_by_session']}. Re-resolving would overwrite the rationale "
                f"of whoever adjudicated it, and that record is the only evidence the "
                f"release was considered. Reopening is a different act.")
        conn.execute(
            "UPDATE determination_gates SET resolved_at=?, resolved_by_session=?, "
            "resolution_rationale=? WHERE gate_id=?",
            [dbcore.now(), session, rationale, gate_id])
        return {"gate_id": gate_id, "parameter_id": g["parameter_id"],
                "verdict": g["verdict"], "resolved_by_session": session,
                "dry_run": dry_run}


# The four lenses (owner 2026-08-28; CHECK relaxed to "at least one" by D-0182).
# Each column, the base registry its real FK points into, and that registry's key.
# DERIVED FROM THE SCHEMA, not a vocabulary restated in code: the registries ARE the
# vocabulary (CLAUDE.md §4). Mirrors assess_cell.LENS_COLUMNS deliberately — the
# extraction and the determination it feeds must name the lens the same way, or the
# hand-off needs a translation nobody wrote.
_LENS_COLUMNS = {
    "identity_code": ("populations", "population_code"),
    # RE-POINTED 2026-09-13 by owner ruling ("keep the ICF lens, give it real ICF
    # codes"), executed by migration 081. It read ("axes", "axis_code") until then, so
    # the column called `icf_code` resolved to an AX- functional-demand code -- which
    # the same day's ruling bans outright: "'AX-' for ICF should never ever exist
    # anywhere". The demand layer keeps its rows and its maps; it is simply no longer
    # a lens.
    "icf_code": ("base_icf", "icf_code"),
    "needs_code": ("access_needs", "need_code"),
    "medical_code": ("base_taxonomy_medical", "medical_code"),
}

# Columns on source_value_extractions whose CHECK declares a closed vocabulary. The
# MEMBERS are never listed here — dbcore.check_values() reads each column's own CHECK.
# What this list says is only WHICH columns to ask about. Verified 2026-09-10 against
# the live schema: all six yield a non-empty set, which matters because
# dbcore.check_declared() does `if allowed and value not in allowed` — an unparsed
# CHECK returns the empty set and turns the refusal silently OFF (the defect recorded
# in check_values' own docstring, where 16 of 108 vocabularies were unguarded).
_SVE_VOCAB_COLUMNS = (
    "claim_type", "extraction_method", "extraction_status",
    "root_type", "measurement_paradigm", "device_class",
    # ADDED 2026-09-13 with migration 075's writer. Read the same way as the six
    # above -- from the column's own CHECK, never a list restated in code.
    "figure_role", "comparator",
)

# The two relations that require a ROW referent, never a label -- the table's own
# CHECK (`relation NOT IN ('condition_on','derived_from') OR to_extraction_id IS NOT
# NULL`), mirrored here so the CLI can name the reason instead of letting SQLite say
# "CHECK constraint failed".
_ROW_ONLY_RELATIONS = ("condition_on", "derived_from")


def _fmt_num(x: float) -> str:
    """Render a float back to a plain value string, without a forced decimal tail."""
    return str(int(x)) if x == int(x) else repr(x)


def _payload_bodies(pay, flag: str, why: str):
    """Every readable text body inside a persisted payload, for a bytes-not-memory check.

    FACTORED OUT 2026-09-13 so `set-icf-title` verifies an ICF title exactly the way
    `add-medical --icd11-payload` verifies an ICD-11 anchor. Two copies of a
    bytes-verification would be two places for the archive-member bug below to come back.

    READS ARCHIVE MEMBERS, NOT JUST RAW BYTES, and that is the whole reason this is more
    than `read_bytes()`. The first version of the ICD-11 check substring-matched the raw
    file, and the only artefact it will ever be pointed at is WHO's release file -- a
    DEFLATE-COMPRESSED ZIP in which no code occurs literally. Measured: b"MB56" in the raw
    zip -> False; in the decompressed member -> True. So the check refused the very payload
    that proved the anchor, and the ruling it enforced was unexecutable.
    """
    pay = Path(pay)
    if "retrieval-log" not in pay.parts:
        raise Refusal(f"{flag} {str(pay)!r} REFUSED: must live under retrieval-log/, which "
                      f"is the only store a later audit can diff against.")
    if not pay.exists():
        raise Refusal(f"{flag} {str(pay)!r} REFUSED: file does not exist. {why}.")
    bodies = [pay.read_bytes().decode("utf-8", errors="replace")]
    if zipfile.is_zipfile(pay):
        with zipfile.ZipFile(pay) as zf:
            for member in zf.namelist():
                # Bounded: a release file's members are text tabulations. A member larger
                # than 64 MiB is not what this check is for, and decompressing it blindly
                # is how a zip becomes a denial of service.
                if zf.getinfo(member).file_size <= 64 * 1024 * 1024:
                    bodies.append(zf.read(member).decode("utf-8", errors="replace"))
    return bodies


def _verbatim(text: str, ref_id: str = None):
    """Does `text` occur in a persisted retrieval artefact? (found, detail).

    A THIN WRAPPER, AND THAT IS THE POINT. The implementation lived here and walked the
    manifest itself, which put the byte-matching rule in the write path -- a writer that
    verifies itself verifies nothing, which is the reason `retrieval_log.py` is
    deliberately outside that path in the first place (its own module docstring says so).
    It now lives beside the bytes as `retrieval_log.quote_in_artefacts`, where
    `--verify-authors` already lives, and where the normalisation it needs can be reused.

    THE OLD IMPLEMENTATION WAS A RAW BYTE SUBSTRING and was anti-correlated with
    evidential quality: measured across the ten committed extractions, it rejected two
    genuine quotes -- one because the payload is JATS XML and inline markup splits every
    sentence citing a figure, one because the publisher wrote a space before a full stop
    -- while accepting a bibliographic TITLE lifted from an esummary record. The shared
    function normalises to letters and digits, so a quote must still be a quote but no
    longer has to survive the publisher's typography.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent / "research"))
    import retrieval_log                                          # noqa: E402
    return retrieval_log.quote_in_artefacts(text, ref_id=ref_id)


def _require_verbatim(text: str, ref_id: str, field: str, context: str,
                      exempt_reason: str = None, claimed_value: str = None):
    """Refuse a quoted field that is not in the bytes -- ONE RULE, EVERY QUOTED COLUMN.

    The verifier had exactly one call site before 2026-09-13: `extraction_relations.quote`,
    on comparator edges. Meanwhile `insert_extraction` wrote `claim_text` -- the sentence a
    determination actually rests on -- behind nothing but a not-blank test. So the strongest
    guarantee in the writer was attached to the weakest column, and `add-extraction` would
    accept `--claim-text "the study found corridors of 1200mm"` typed from memory while
    refusing a `--quote` beside it. Demonstrated during the audit: claimed_value 9999 with
    an invented claim_text landed and governed a determination.

    IT ALSO MAKES `derive-extraction` HONEST. That verb reasons from the premise that "the
    base and delta rows' own claim_text values already passed that check when those rows
    were written". They had not -- nothing verified claim_text -- so the verb succeeded only
    when a base row's text HAPPENED to be in a payload. Now the premise is true.

    THE NUMBER MUST BE IN THE QUOTE. A numerical claim whose own digits do not appear in the
    verified sentence is a number attached to a quote rather than read from one, which is
    exactly how `1525` and `9999` reached the table during the audit -- both with quotes
    that verified, because the quote was a TITLE and the title was genuinely in the payload.

    EXEMPTION IS EXPLICIT AND LEDGERED, never silent. A clause read from a standards PDF
    that was never persisted as an artefact is a real case; "I could not be bothered to
    retrieve it" is not, and the two are indistinguishable unless the operator writes the
    reason down. An exemption is refused when the text WOULD have verified, so it cannot
    become the lazy default.
    """
    if exempt_reason:
        found, where = _verbatim(text, ref_id)
        if found:
            raise Refusal(
                f"{context}: --verbatim-exempt was given, but {field} DOES occur in a "
                f"persisted artefact ({where}). Drop the exemption -- it is for text no "
                f"retrieval artefact can carry, not for text that verifies.")
        return f"[VERBATIM-EXEMPT: {exempt_reason}]"

    found, where = _verbatim(text, ref_id)
    if not found:
        raise Refusal(
            f"{context}: {field} does not occur in any persisted retrieval artefact "
            f"({where}). Either the payload behind it was never retrieved and persisted "
            f"(R10 -- retrieve it first, retrieval_log.fetch()), or it was typed from "
            f"memory rather than read off the bytes (CLAUDE.md 5(c)). If no artefact can "
            f"carry this text -- a clause from a standards PDF, say -- pass "
            f"--verbatim-exempt with the reason, which is ledgered on the row. "
            f"Nothing was written.")

    if claimed_value:
        digits = re.findall(r"\d+", str(claimed_value))
        if digits:
            body = _verbatim_norm(text)
            missing = [d for d in digits if d not in body]
            if missing:
                # THE CHECK ABOVE IS MONOLINGUAL, AND SILENTLY SO. It asks whether
                # the Arabic digits of claimed_value occur in the quote. A Japanese
                # statute writes its numerals in kanji -- 勾配は、十二分の一を超えないこと
                # states 1:12 and contains no digit at all -- so EVERY CJK code value
                # was unextractable, and --verbatim-exempt could not rescue it because
                # the exemption is refused when the text verifies, which this text
                # does. The escape hatch was closed against the one case that needed
                # it. R5 says non-English work is academic, not lesser; a guard that
                # only reads Arabic numerals makes it unfilable.
                #
                # This WIDENS what counts as the number appearing in the quote; it
                # does not loosen the standard. The figure must still be present in
                # the source's own sentence -- merely written the way that language
                # writes it. A fabricated number fails here exactly as before.
                missing = [d for d in digits if d not in _cjk_to_arabic(body)]
            if missing:
                raise Refusal(
                    f"{context}: claimed_value {claimed_value!r} contains {missing}, which "
                    f"do not appear in the verified {field}. A number attached to a quote "
                    f"rather than read from one is the 2026-08-19 fabrication shape with a "
                    f"figure in place of an author -- and it is how a title, which verifies "
                    f"because titles really are in the payload, came to carry an invented "
                    f"measurement. Quote the sentence that states the value. Nothing was "
                    f"written.")
    return None


_CJK_DIGITS = {"〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4,
               "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
_CJK_UNITS = {"十": 10, "百": 100, "千": 1000}


def _cjk_num(run):
    """Parse one contiguous CJK numeral (十二, 百二十, 七十五) into an int, or None."""
    total = cur = 0
    for ch in run:
        if ch in _CJK_DIGITS:
            cur = _CJK_DIGITS[ch]
        elif ch in _CJK_UNITS:
            total += (cur or 1) * _CJK_UNITS[ch]
            cur = 0
        else:
            return None
    return total + cur


def _cjk_to_arabic(text):
    """`text` with each run of CJK numerals rewritten as its Arabic value.

    Used ONLY to widen the number-in-the-quote check for CJK sources. 分の is not in
    the character class, so 十二分の一 splits into the runs 十二 and 一 and renders
    "12分の1" -- which is how the figure is read aloud and how every secondary source
    in this corpus writes it.
    """
    return re.sub(r"[〇零一二三四五六七八九十百千]+",
                  lambda m: str(_cjk_num(m.group(0)))
                  if _cjk_num(m.group(0)) is not None else m.group(0),
                  text)


def _verbatim_norm(text):
    """The shared normalisation, for the digit test. One home (retrieval_log)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent / "research"))
    import retrieval_log                                          # noqa: E402
    return retrieval_log.normalise_quote(text)


def _write_relation_edge(conn, *, from_id: int, from_ref_id: str,
                         from_figure_role, from_comparator,
                         relation: str, session: str, context: str,
                         to_extraction: int = None, to_label: str = None,
                         to_kind: str = None, stated: str = None, quote: str = None,
                         input_role: str = None, notes: str = None,
                         cross_source_reason: str = None,
                         verbatim_exempt: str = None) -> int:
    """Validate and INSERT one `extraction_relations` row. The one place every
    refusal in this junction's CHECK constraints is restated as a sentence — shared
    by `add-extraction`, `relate-extraction` and `derive-extraction` so there is one
    copy of this logic, not three (CLAUDE.md rule 5 applies to a validation rule as
    much as to a stored fact).

    `from_figure_role` / `from_comparator` are passed in rather than re-queried:
    `insert_extraction` calls this AFTER inserting the row it qualifies but before
    that row is necessarily visible to a fresh SELECT in every SQLite build, and the
    values are already in hand either way.
    """
    if not relation:
        raise Refusal(f"{context}: --relation is required.")
    dbcore.check_declared(conn, "extraction_relations", "relation", relation, context)

    has_row = to_extraction is not None
    has_label = to_label is not None
    if has_row and has_label:
        raise Refusal(
            f"{context}: pass --to-extraction OR --to-label, never both -- the "
            f"referent is a row this project holds, or a label describing one it "
            f"does not, never both at once.")
    if not has_row and not has_label:
        raise Refusal(
            f"{context}: pass --to-extraction or --to-label -- an edge naming no "
            f"referent describes nothing.")

    if not (quote or "").strip():
        raise Refusal(
            f"{context}: --quote is required. Mirrors the verbatim floor "
            f"--claim-text already puts on the row itself: a comparator asserted "
            f"with nothing of the source's own phrasing behind it is not a "
            f"comparator this project has actually read.")

    if has_row:
        if to_extraction == from_id:
            raise Refusal(
                f"{context}: --to-extraction {to_extraction} is the same row this "
                f"edge is FROM. A figure cannot be its own comparator.")
        target = conn.execute(
            "SELECT ref_id FROM source_value_extractions WHERE extraction_id=?",
            (to_extraction,)).fetchone()
        if target is None:
            raise Refusal(
                f"{context}: --to-extraction {to_extraction}: no such extraction. "
                f"condition_on/derived_from name a figure this project actually "
                f"holds as a row -- extract it first, or use --to-label for a "
                f"referent that is not yet its own row.")
        if relation in _ROW_ONLY_RELATIONS and target["ref_id"] != from_ref_id \
                and not (cross_source_reason or "").strip():
            raise Refusal(
                f"{context}: --to-extraction {to_extraction} was extracted from "
                f"{target['ref_id']}, not {from_ref_id} -- a {relation} edge across "
                f"sources is a SYNTHESIS act (drawing a condition or a derivation "
                f"from a different document than the one asserting the figure), "
                f"not a plain pointer. Pass --cross-source with a reason to make "
                f"that explicit, or point at a same-source row.")
        if to_kind is not None:
            raise Refusal(
                f"{context}: --to-kind is meaningless with --to-extraction -- a row "
                f"referent already carries its own kind in its own data. Omit "
                f"--to-kind, or use --to-label if the referent is not a row.")
    else:
        if relation in _ROW_ONLY_RELATIONS:
            raise Refusal(
                f"{context}: relation={relation!r} requires --to-extraction (a row "
                f"this project actually holds), not --to-label -- you cannot be "
                f"conditioned by, or computed from, a figure that does not exist as "
                f"a row.")
        if not to_kind:
            raise Refusal(
                f"{context}: --to-label requires --to-kind -- what sort of thing "
                f"the label names ('standard'/'own_sample'/'prior_source'/"
                f"'unnamed').")
        dbcore.check_declared(conn, "extraction_relations", "to_kind", to_kind, context)
        if stated == "named" and to_label not in quote:
            raise Refusal(
                f"{context}: --stated named asserts the source NAMES this referent "
                f"by the label given ({to_label!r}), but --quote does not contain "
                f"that label as a substring. Either quote the passage that actually "
                f"names it, or this referent is --stated unnamed/inferred instead.")

    if not stated:
        raise Refusal(f"{context}: --stated is required ('named'/'unnamed'/"
                      f"'inferred').")
    dbcore.check_declared(conn, "extraction_relations", "stated", stated, context)
    if stated == "unnamed" and has_row:
        raise Refusal(
            f"{context}: stated=unnamed cannot carry a row referent -- an unnamed "
            f"referent has, by definition, nothing this project could have resolved "
            f"to a row.")
    if to_kind == "unnamed" and stated != "unnamed":
        raise Refusal(
            f"{context}: to_kind=unnamed requires stated=unnamed -- the two "
            f"describe the same fact from two columns and must not disagree.")

    is_derivation = relation == "derived_from"
    if is_derivation and not input_role:
        raise Refusal(
            f"{context}: relation=derived_from requires --input-role "
            f"('base'/'delta'/'factor').")
    if not is_derivation and input_role:
        raise Refusal(
            f"{context}: --input-role is meaningful only with relation=derived_from "
            f"(this edge is {relation!r}). Omit it.")
    if input_role:
        dbcore.check_declared(conn, "extraction_relations", "input_role",
                              input_role, context)

    if relation in ("insufficient", "audited_against") and from_figure_role == "claim":
        raise Refusal(
            f"{context}: figure_role='claim' cannot carry a {relation!r} edge -- a "
            f"row finding the baseline inadequate, or auditing subjects against it "
            f"rather than measuring independently, asserts no absolute value of its "
            f"own; grade it figure_role='finding'. If the source ALSO states an "
            f"absolute value, that is a SECOND row, not this one relabelled.")

    if relation == "delta_over" and not from_comparator:
        raise Refusal(
            f"{context}: relation=delta_over requires --comparator on the row "
            f"(source_value_extractions.comparator) -- 'more than thirty "
            f"centimetres' is comparator='>' against 30, and storing a bare 30 "
            f"turns a floor into a point. Set --comparator when writing the row.")

    verified, where = _verbatim(quote, from_ref_id)
    if not verified:
        # GAP-007, closed 2026-09-18 (batch 18). `add-extraction` has carried
        # --verbatim-exempt since it was built; this edge writer never received it, so
        # the refusal below TOLD THE READER TO USE A FLAG THAT COULD NOT REACH IT. That
        # is worse than a missing flag: the message is a correct instruction to an
        # impossible action, and the only ways past it were to abandon a true extraction
        # or to weaken the check for everyone.
        #
        # It bites exactly where the evidence is oldest. `quote_in_artefacts` cannot
        # decode a scanned PDF's text layer, so NO quote from a microfiche-era report can
        # ever match byte-for-byte -- and the pre-1990 layer (GAP-028) is entirely that
        # shape. REF-01005 (ED184280, a 1979 microfiche) is the row that exposed it.
        #
        # The exemption does not weaken the check: it is REFUSED unless a reason is given,
        # the reason is stored on the row, and the artefact is still required to exist and
        # to be bound to the ref_id. What it stops requiring is byte-equality against
        # bytes that cannot be decoded at all.
        if not (verbatim_exempt or "").strip():
            raise Refusal(
                f"{context}: --quote does not occur byte-for-byte in any persisted "
                f"retrieval artefact ({where}). Either the payload behind this quote "
                f"was never retrieved and persisted (R10 -- retrieve it first, "
                f"retrieval_log.fetch()), or the quote was typed from memory rather "
                f"than read off the bytes (CLAUDE.md 5(c)). If the artefact exists but "
                f"its bytes cannot be decoded -- a scanned PDF's text layer, say -- pass "
                f"--verbatim-exempt with the reason, which is ledgered on the row. "
                f"Nothing was written.")
        notes = ((notes + " || ") if notes else "") + (
            "VERBATIM-EXEMPT: " + verbatim_exempt.strip())

    dup = conn.execute(
        "SELECT relation_id FROM extraction_relations WHERE from_extraction_id=? "
        "AND relation=? AND COALESCE(to_extraction_id,-1)=? "
        "AND COALESCE(to_label,'')=?",
        (from_id, relation, to_extraction if has_row else -1,
         to_label if has_label else "")).fetchone()
    if dup:
        raise Refusal(
            f"{context}: this exact edge already exists (relation_id {dup[0]}). "
            f"One edge is one fact; writing it twice is a duplicate, not a second "
            f"fact.")

    edge = {"from_extraction_id": from_id, "relation": relation,
            "to_extraction_id": to_extraction, "to_label": to_label,
            "to_kind": to_kind, "stated": stated, "input_role": input_role,
            "quote": quote, "notes": notes}
    edge = {k: v for k, v in edge.items() if v is not None}
    edge.update(dbcore.stamp_for(conn, "extraction_relations", session))
    cur = conn.execute(
        f"INSERT INTO extraction_relations ({','.join(edge)}) "
        f"VALUES ({','.join('?' * len(edge))})", list(edge.values()))
    return cur.lastrowid


def _build_relation_groups(relations, to_extractions, to_labels, to_kinds, stateds,
                           quotes, input_roles, cross_sources):
    """Zip `add-extraction`'s repeatable --relation flag with its per-edge
    companions, aligned by position, into a list of edge dicts for
    `insert_extraction(..., relations=...)`.

    'none' -- alone, exactly once, with no other relation flag -- means the source
    states its figure absolutely and no edge is written at all.

    Each companion flag must be given exactly zero times or exactly as many times as
    --relation; the literal placeholder '-' marks "not set for THIS edge" so a mixed
    batch (one edge pointing at a row, the next at a label) still aligns positionally
    without forcing every edge to carry every flag.
    """
    n = len(relations)
    if n == 1 and relations[0] == "none":
        extra = to_extractions or to_labels or to_kinds or stateds or quotes \
            or input_roles or cross_sources
        if extra:
            raise Refusal(
                "--relation none states that the source's figure is absolute and "
                "takes NO other relation flag (--to-extraction/--to-label/"
                "--to-kind/--stated/--quote/--input-role/--cross-source). Nothing "
                "was written.")
        return []
    if "none" in relations:
        raise Refusal(
            "--relation none may only be given alone, exactly once: it says the "
            "source states its figure absolutely, which cannot also be true of a "
            "row that carries a real comparator edge.")

    def _spread(name, values):
        if not values:
            return [None] * n
        if len(values) != n:
            raise Refusal(
                f"{name} was given {len(values)} time(s) but --relation was given "
                f"{n} time(s) -- the repeatable relation flags must align "
                f"positionally, one entry per edge. Pass '-' for an edge that does "
                f"not use {name}.")
        return [None if v == "-" else v for v in values]

    to_ext = _spread("--to-extraction", to_extractions)
    to_lab = _spread("--to-label", to_labels)
    to_knd = _spread("--to-kind", to_kinds)
    stat = _spread("--stated", stateds)
    quo = _spread("--quote", quotes)
    inp = _spread("--input-role", input_roles)
    crs = _spread("--cross-source", cross_sources)
    out = []
    for i in range(n):
        if to_ext[i] is not None:
            try:
                to_ext[i] = int(to_ext[i])
            except ValueError:
                raise Refusal(f"--to-extraction {to_ext[i]!r} is not an integer.")
        out.append({
            "relation": relations[i], "to_extraction": to_ext[i],
            "to_label": to_lab[i], "to_kind": to_knd[i], "stated": stat[i],
            "quote": quo[i], "input_role": inp[i],
            "cross_source_reason": crs[i],
        })
    return out


def insert_extraction(data: dict, session: str, dry_run: bool = False,
                      relations: list = None, verbatim_exempt: str = None):
    """Record ONE judgment item: what one source asserts for one parameter.

    THE WRITER THIS TABLE SHIPPED WITHOUT. `source_value_extractions` has existed
    since migration 018 and `scripts/db.py` contained ZERO references to it —
    measured 2026-09-10, `grep -c source_value_extractions scripts/db.py` -> 0. With
    no extraction writer there was no parameter->evidence edge at all, so the
    determination engine had nothing to gather evidence by except the slug, and
    `param 1 x MOB -> stated` meant "everything linked to
    accessible-circulation-geometry" — 10 sources, 8 of which the engine's own report
    flagged `tier_inconsistent`. This function is what makes that join exist.

    WHAT IT REFUSES, and why each refusal is the point:

    * An unknown `ref_id`. The FK would say `FOREIGN KEY constraint failed`, which
      names neither the source nor the fix. An extraction is a reading OF a source;
      one that names no admitted source is a claim about nothing.

    * An unknown `slug`. Same class. `slug` is NOT NULL here and is a fact of the
      extraction — the reading happened under that topic — not a copy of
      `source_slug_links` (`evidence_sources` has no slug column to point at).

    * A slug the REF IS NOT ADMITTED TO. The column's FK points at `slugs`, so the
      database accepts any live slug and cannot see that this source was never
      admitted to this topic. `source_slug_links` is that record. Without this
      refusal the vetting surface renders the row under a slug whose own
      `linked_sources` does not contain the ref.

    * A MISSING OR BLANK `claim_text`. Migration 073 retired `parameter`, the last
      NOT NULL column carrying the source's own words; `claim_text`,
      `source_section` and all 16 `loc_*` columns are nullable, so without this the
      happy path writes a row with ZERO verbatim from the source it read. The
      guarantee is the CLI's, not the schema's — say so rather than implying the
      table enforces it.

    * A `parameter_id` that is absent, or whose row is not `status='active'`. A
      determination keyed on a parameter folded into another is a determination about
      a subject that no longer stands on its own, and the FK cannot see the
      difference because the row is still there. `assess_cell.validate_parameter()`
      refuses the same thing at the other end; both ends refuse or neither does.

    * FK-INTO-EMPTY-PARENT, refused EARLY and by name. `base_parameters` holds 0 rows
      today, so a bare INSERT dies with `FOREIGN KEY constraint failed` at INSERT and
      never at migration time — the exact failure CLAUDE.md §4 says "makes a broken
      table look healthy": the schema parses, a rebuild reproduces it exactly, and
      every gate stays green over a table that cannot accept a row. The refusal here
      names `db.py add-parameter` as the remedy. The same treatment is given to each
      lens registry, because `base_taxonomy_medical` is ALSO empty and `--medical`
      would fail the same silent way.

    * A lens code that is not live in its own registry — and a BLANK is not an
      absence. `--identity ""` is normalised to None before anything reads it:
      assess_cell records the live incident where a blank skipped validation (falsy),
      satisfied the at-least-one test at the NEXT lens (truthy), was INSERTed as '',
      and produced a `PRAGMA foreign_key_check` violation against `populations`.

    * NO LENS AT ALL. D-0182: absence in a lens is fine, absence in all four is not.
      A value attached to no lens is a value about nobody.

    * The claim/value contradiction, IN WORDS. The table's own CHECK already refuses
      `claim_type='absent'` with a value and any other claim_type without one; this
      refuses it first so the operator gets a sentence instead of
      "CHECK constraint failed", which names neither column.

    * Any value outside a column's own declared CHECK vocabulary, for all six
      vocabulary columns, read from the schema and never from a list in code.

    DELIBERATELY ABSENT REFUSALS — each must STAY absent, and this is where the next
    reader is told so rather than discovering it by removing one:

    * NO UNIQUENESS ON (ref_id, parameter_id). This is the ruled 1:N fan-out. D-0168
      (owner, 2026-08-27): "one evidence source may provide many rows of judgment (eg
      a code document like Canada's NBC 3.8)" — many clauses, many rows, one source,
      one parameter. It is ALSO the DR-2026-08-19 §7 dissent contest: a divergent
      adversarial grade lands as a SECOND row and divergent readings are meant to be
      readable as a contest, not silently overwritten. A uniqueness refusal here
      would be the CLI quietly overruling doctrine, and
      `scripts/audit/judgment_handoff_shape.py` (BLOCKING) fails if the same
      collapse is attempted in the schema. A duplicate is NOTED on stderr, never
      refused: if it is unintended the author sees it in the same session; if it is
      intended it is the whole point.

    * NO VALUE-DIRECTNESS GRADE. There is no value-directness grading rule in this
      repository (workplan 2026-09-10, stop condition 4: "Any step needing a
      value-directness grading rule. None exists. Do not invent one."). The engine
      records the dimension NOT_ASSESSED under G2 — applies but unassessed, never
      silently EXACT. Accepting a grade here would be inventing the rule at the
      point of capture, where it is least visible.

    * NO `--promoted-to-rdc-id`. Promotion to the synthesis layer is a later act on
      an existing row with its own verdict behind it (rule #10 re-read). Letting
      capture assert it would mint an extraction that claims to have been verified
      before it was read twice.

    ONE SIDE EFFECT ON ANOTHER TABLE, and it is not free: the ref's
    `evidence_sources.data_capture_status` is set to 'captured' in the SAME
    transaction. See the comment at the UPDATE for what breaks without it (blocking
    check C06), what the other three capture-table writers do (nothing), and the
    rule 5 tension it stops rather than cures.

    ADDED 2026-09-13 BY MIGRATION 075's WRITER, and refused the same way as
    everything above: `--figure-role` (REQUIRED -- a value with no role reads as a
    claim), `--comparator`, and `relations` -- a list of edge dicts written into
    `extraction_relations` in this SAME transaction (the `add-term` precedent: a
    term and its adjudication land together, and here a figure and what it is
    stated relative to do too). `--relation` is REQUIRED at the CLI; the literal
    'none' (which arrives here as `relations == []`) says the source states its
    figure absolutely. See `_write_relation_edge` for the edge-level refusals and
    `_build_relation_groups` for how the CLI's repeatable flags become this list.
    """
    _COLS = frozenset({
        "ref_id", "slug", "parameter_id",
        "identity_code", "icf_code", "needs_code", "medical_code",
        "jurisdiction", "setting",
        "claim_type", "claimed_value", "claimed_unit", "claim_text", "source_section",
        "root_id", "root_type", "root_ref_id", "echo_of", "measurement_paradigm",
        "device_class", "root_population_note", "root_classification_basis",
        "contested", "file_anchor",
        "locator_scheme", "loc_division", "loc_part", "loc_section", "loc_subsection",
        "loc_paragraph", "loc_clause", "loc_subclause",
        "loc_division_end", "loc_part_end", "loc_section_end", "loc_subsection_end",
        "loc_paragraph_end", "loc_clause_end", "loc_subclause_end", "loc_note",
        "extraction_method", "extraction_status", "notes",
        "figure_role", "comparator",
    })
    dbcore.validate_cols(data.keys(), _COLS, "insert_extraction")
    dbcore.check_jurisdiction(data.get("jurisdiction"), "add-extraction --jurisdiction")
    row = {k: v for k, v in data.items() if v is not None}

    # A BLANK IS NOT AN ABSENCE — normalise before anything reads these.
    for col in _LENS_COLUMNS:
        if col in row and not str(row[col]).strip():
            del row[col]

    with dbcore.connect(dry_run) as conn:
        ref = dbcore.fold_ref(row.get("ref_id"))
        if not dbcore.exists(conn, "evidence_sources", "ref_id", ref):
            raise Refusal(
                f"ref_id {data.get('ref_id')!r} is not an admitted source. An extraction "
                f"is a reading OF a source; extract AFTER admission.\n"
                f"  db.py add-source ...")
        _refuse_tombstone(conn, ref, "add-extraction")
        row["ref_id"] = ref

        if not dbcore.exists(conn, "slugs", "slug", row.get("slug")):
            raise Refusal(
                f"slug {row.get('slug')!r} is not a live slug. The slug records where the "
                f"reading happened, and it must be one the project holds.")

        # THE REF MUST BE ADMITTED TO THE SLUG, not merely exist beside it. The
        # column's FK points at `slugs`, so the database is satisfied by ANY live
        # slug -- it cannot see that this source was never admitted to this topic.
        # Without this refusal an extraction lands under a slug whose own
        # `linked_sources` does not contain the ref, and
        # tools/regenerate_vetting_surface.py renders it there: the vetting surface
        # would show a value mined under a topic the source was never admitted to,
        # which is the one thing that surface exists to make impossible to miss.
        #
        # THIS IS REF<->SLUG COHERENCE, NOT PARAMETER<->SLUG COHERENCE, and the two
        # are deliberately different. test_db_integrity's retired J01 asserted that
        # an extraction's PARAMETER belonged to its slug; that assumption is wrong
        # (a source admitted under one slug may legitimately be read for a parameter
        # another slug also governs) and its deletion note says so. Ref<->slug is the
        # stronger and simpler invariant: the junction that records admission is
        # `source_slug_links`, it is non-empty, and it is the only record of what the
        # project decided this source was admitted FOR.
        if not conn.execute(
                "SELECT 1 FROM source_slug_links WHERE ref_id=? AND slug=?",
                (ref, row.get("slug"))).fetchone():
            held = [r[0] for r in conn.execute(
                "SELECT slug FROM source_slug_links WHERE ref_id=? ORDER BY slug",
                (ref,))]
            raise Refusal(
                f"{ref} is not admitted to slug {row.get('slug')!r}. An extraction is "
                f"mined under a topic the source was ADMITTED to; `source_slug_links` "
                f"is that record and it does not hold this pair.\n"
                f"  admitted to: {held or '(no slug at all)'}\n"
                f"Extract under one of those, or cross-file the source to this "
                f"slug first and say why: {R9_REMEDY}. Inventing the link from "
                f"here would make this writer the thing that decides what a "
                f"source was admitted for, and it would record no grounds.")

        # --- the subject -----------------------------------------------------
        pid = row.get("parameter_id")
        if pid is None:
            raise Refusal(
                "--parameter-id is required: an extraction whose subject is unknown "
                "cannot reach the determination it exists to support (owner 2026-08-26, "
                "'the judgment object is the canonical parameter').")
        n_params = conn.execute("SELECT COUNT(*) FROM base_parameters").fetchone()[0]
        if n_params == 0:
            raise Refusal(
                "`base_parameters` holds no rows, so NO parameter_id can be valid and a "
                "bare INSERT would fail with `FOREIGN KEY constraint failed` — a refusal "
                "that names neither the cause nor the fix (CLAUDE.md §4).\n"
                "Mint the subject first, from an adjudicated term:\n"
                "  db.py add-parameter --term-id TERM-NNN --session ...")
        prow = conn.execute("SELECT status, merged_into FROM base_parameters "
                            "WHERE parameter_id=?", (pid,)).fetchone()
        if prow is None:
            raise Refusal(
                f"parameter_id {pid}: no such parameter. Mint one from a term:\n"
                f"  db.py add-parameter --term-id TERM-NNN --session ...")
        if prow["status"] != "active":
            target = f" (merged into {prow['merged_into']})" if prow["merged_into"] else ""
            raise Refusal(
                f"parameter_id {pid} is {prow['status']}{target}, not active. Key the "
                f"extraction on the surviving parameter — a value filed under a folded "
                f"parameter is unreachable from the determination that replaced it.")

        # --- the lenses ------------------------------------------------------
        if not any(row.get(c) for c in _LENS_COLUMNS):
            raise Refusal(
                "an extraction must be stated in at least one lens (D-0182): pass one or "
                "more of --identity / --icf / --needs / --medical. A value attached to no "
                "lens is a value about nobody.")
        for col, (table, key) in _LENS_COLUMNS.items():
            code = row.get(col)
            if not code:
                continue
            if not dbcore.exists(conn, table, key, code):
                n = conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
                if n == 0:
                    raise Refusal(
                        f"{col} {code!r}: the registry `{table}` holds no rows, so no code "
                        f"is valid in this lens yet and the INSERT would fail with "
                        f"`FOREIGN KEY constraint failed`. Seed the registry in a "
                        f"migration, or state the value in a lens that has one.")
                raise Refusal(
                    f"{col} {code!r} is not a live {key} in `{table}`. The registry is the "
                    f"vocabulary (CLAUDE.md §4); it is not extended from the CLI.")

        # --- the claim -------------------------------------------------------
        claim_type = row.get("claim_type")
        value = row.get("claimed_value")
        # THE VERBATIM FLOOR. `--claim-text` is required at the parser, so this fires
        # on the PYTHON API path and on `--claim-text ""` — a blank is not a quote,
        # and normalising it to None here would restore exactly the zero-verbatim row
        # the requirement exists to forbid.
        if not str(row.get("claim_text") or "").strip():
            raise Refusal(
                "--claim-text is required and must not be blank. Migration 073 retired "
                "`parameter`, the last NOT NULL column that carried the source's own "
                "words; every remaining verbatim column on this table is nullable, so "
                "without --claim-text this row would assert a value with nothing of the "
                "source's own phrasing behind it. Quote the clause you read.")

        # THE QUOTE MUST BE IN THE BYTES (CLAUDE.md 5(c), added 2026-09-13). Blank was
        # the ONLY thing refused above; the sentence a determination rests on could be
        # composed from memory and nothing looked. Demonstrated during the audit:
        # claimed_value 9999 with an invented claim_text landed and governed a cell.
        # `--verbatim-exempt` is the ledgered escape for text no artefact can carry, and
        # is itself refused when the text would have verified.
        _exempt_note = _require_verbatim(
            str(row["claim_text"]), row.get("ref_id"), "--claim-text",
            "add-extraction", exempt_reason=verbatim_exempt, claimed_value=value)
        if _exempt_note:
            row["notes"] = ((row.get("notes") or "") + " " + _exempt_note).strip()

        # THE STRUCTURED LOCATOR, for the regulatory stratum only (added 2026-09-20).
        # R3 says a quantified value needs a locator, and `source_section` free text
        # already satisfied every gate that asked -- so migration 053's seventeen
        # `loc_*` columns went unused by exactly the documents they were built for.
        # Measured 2026-09-20: of 48 extractions, 41 carried no structured locator, and
        # the 17 from the regulatory stratum carried ZERO between them. Their pinpoints
        # were sitting in prose -- `第十九条第二項第四号ロ`, `Advisory 405.2`,
        # `Artikel 19 §1, 4°` -- where nothing can check that a clause resolves, nothing
        # can range over a span, and no pinpoint citation can be rendered.
        #
        # Scoped by TIER, not by a list of evidence types: CLAUDE.md §6 states T4-T6 as
        # the regulatory stratum, so the band is read from the source rather than
        # re-listed here (rule 8 -- a curated list beside the thing it describes is what
        # drifts). A journal article keeps prose: `source_section` of "Abstract, Results"
        # is the honest locator for a paper and there is no clause to give.
        #
        # The hierarchy columns are read from the live table, never typed out, so a
        # migration that adds a level is covered without editing this refusal.
        if value is not None and claim_type != "absent":
            _tier = conn.execute(
                "SELECT tier FROM evidence_sources WHERE ref_id=?", (ref,)).fetchone()
            if _tier and _tier[0] is not None and int(_tier[0]) >= 4:
                _levels = [c[1] for c in conn.execute(
                    'PRAGMA table_info("source_value_extractions")')
                    if c[1].startswith("loc_") and not c[1].endswith("_end")
                    and c[1] != "loc_note"]
                _esc = "[UNVERIFIED-QUANT]" in (row.get("notes") or "")
                if not _esc and not any(str(row.get(c) or "").strip() for c in _levels):
                    raise Refusal(
                        f"R3: {ref} is tier {int(_tier[0])} -- the regulatory stratum -- and this row "
                        f"states a value with no structured locator. A code, standard or statute "
                        f"numbers its own clauses, so give the pinpoint in the hierarchy rather than "
                        f"in prose: one of {', '.join('--' + c.replace('_', '-') for c in _levels)} "
                        f"(with --locator-scheme naming the family, e.g. ADA section vs ISO clause). "
                        f"`--source-section` is still wanted, and stays sufficient on its own for a "
                        f"journal article, but it cannot be checked, sorted or cited to a pinpoint. "
                        f"If this instrument genuinely carries no clause numbering, say so with "
                        f"[UNVERIFIED-QUANT] in --notes. Nothing written.")

        if claim_type == "absent" and value is not None:
            raise Refusal(
                "claim_type='absent' records that the source asserts NO value for this "
                "parameter, so --claimed-value must be omitted. If the source does state "
                "a value, the claim_type is one of the others.")
        if claim_type is not None and claim_type != "absent" and value is None:
            raise Refusal(
                f"claim_type={claim_type!r} requires --claimed-value. If the source "
                f"asserts nothing for this parameter, that is claim_type='absent' — a "
                f"recorded absence, which is evidence, not a missing field.")

        # --- figure_role (migration 075) -------------------------------------
        figure_role = row.get("figure_role")
        if not figure_role:
            raise Refusal(
                "--figure-role is required. A value with no role reads as a claim, "
                "and a tested slope read as a claim is how '1:20, 1:16, 1:12, 1:8' "
                "became a range no source ever asserted (extraction_id 1, the "
                "worked example migration 075 itself cites).")
        if claim_type == "absent" and figure_role != "finding":
            raise Refusal(
                f"claim_type='absent' with figure_role={figure_role!r} is refused: "
                f"absence IS a finding -- the source was read for this parameter "
                f"and stated nothing, which is itself the result, not a claim, a "
                f"condition or a derivation. Use --figure-role finding.")

        # --- the declared vocabularies, read from the schema ------------------
        for col in _SVE_VOCAB_COLUMNS:
            if row.get(col) is not None:
                dbcore.check_declared(conn, "source_value_extractions", col,
                                      row[col], "insert_extraction")

        # --- the relation edges (migration 075's extraction_relations) --------
        # REQUIRED, and checked here rather than only at the parser so the PYTHON
        # API path refuses too -- the same discipline --claim-text already gets.
        if relations is None:
            raise Refusal(
                "--relation is required: pass the literal 'none' (source states "
                "its figure absolutely) or one or more real relation edges. Five "
                "of five corridor-width sources in the live corpus state theirs "
                "against a reference they name or invoke -- silence is not "
                "'absolute', it is unchecked.")
        if figure_role == "derived" and not any(
                e.get("relation") == "derived_from" and e.get("input_role") == "base"
                for e in relations):
            raise Refusal(
                "figure_role='derived' requires at least one derived_from edge "
                "carrying --input-role base. A derived row with nothing pointing "
                "at what it was computed FROM is a number trusted on faith, which "
                "is exactly what v_derived_figure_check (migration 075) exists to "
                "stop trusting silently.")

        # DELIBERATELY NOT REFUSED — see the docstring. Noted so the fan-out is
        # visible in the session log rather than silent.
        prior = conn.execute(
            "SELECT extraction_id, created_by_session FROM source_value_extractions "
            "WHERE ref_id=? AND parameter_id=?", (ref, pid)).fetchall()
        if prior:
            print(f"NOTE: {ref} already carries {len(prior)} extraction(s) for parameter "
                  f"{pid} ({[r[0] for r in prior]}). Writing another — evidence to "
                  f"judgment is 1:N (D-0168), and a divergent reading is a contest "
                  f"(DR-2026-08-19 §7), not an error.", file=sys.stderr)

        row.update(dbcore.stamp_for(conn, "source_value_extractions", session))
        cur = conn.execute(
            f"INSERT INTO source_value_extractions ({','.join(row)}) "
            f"VALUES ({','.join('?' * len(row))})", list(row.values()))
        extraction_id = cur.lastrowid

        # THE EDGES, IN THIS SAME TRANSACTION -- the `add-term` precedent (a term
        # and its adjudication land together). `relations` is `[]` for the literal
        # 'none' (source states its figure absolutely) and a list of edge dicts
        # otherwise; every refusal for an individual edge lives in
        # _write_relation_edge so there is one copy of that logic, not one per
        # caller (add-extraction / relate-extraction / derive-extraction).
        relation_ids = []
        for edge in relations:
            relation_ids.append(_write_relation_edge(
                conn, verbatim_exempt=verbatim_exempt,
                from_id=extraction_id, from_ref_id=ref,
                from_figure_role=figure_role, from_comparator=row.get("comparator"),
                relation=edge.get("relation"), to_extraction=edge.get("to_extraction"),
                to_label=edge.get("to_label"), to_kind=edge.get("to_kind"),
                stated=edge.get("stated"), quote=edge.get("quote"),
                input_role=edge.get("input_role"), notes=edge.get("notes"),
                cross_source_reason=edge.get("cross_source_reason"),
                session=session, context="add-extraction"))

        # THE STATUS THIS ROW MAKES TRUE — set in the SAME transaction as the INSERT,
        # so the two can never be observed apart. `dbcore.connect()` commits once at
        # the end of the with-block and rolls back on any exception, so either both
        # land or neither does.
        #
        # WHAT BREAKS WITHOUT IT: test_db_integrity C06 asserts
        # `evidence_sources.data_capture_status='captured'` <=> a joinable capture row
        # exists, and `source_value_extractions` is one of its four capture tables.
        # test_db_integrity is BLOCKING. `add-extraction` shipped as the table's first
        # writer, so its first row turned a green blocking gate red -- reproduced
        # 2026-09-10: one extraction, `C06 (9 examined) ... 1 have rows but do not claim
        # it`, 68/69.
        #
        # WHAT THE OTHER THREE CAPTURE-TABLE WRITERS DO: NOTHING, AND MOSTLY THEY DO
        # NOT EXIST. Measured 2026-09-10 -- `spec_value_probes` and
        # `reasoning_doc_citations` have no `db.py` writer at all; `economics_entries`
        # has `insert_economics_entry`, which never touches `data_capture_status`. So
        # this is not a convention being followed, it is the first writer to maintain
        # the biconditional at all. C06 is green over those three only because all
        # three tables hold 0 rows. WHEN ANY OF THEM GAINS A WRITER, IT NEEDS THIS
        # SAME BLOCK, and this comment is where that is recorded.
        #
        # RULE 5 TENSION, STATED RATHER THAN PAPERED OVER. `data_capture_status` is a
        # DERIVED DUPLICATE of "does a capture row exist for this ref" -- a fact whose
        # real home is the four capture tables. C06 is therefore a PARITY CHECK over a
        # dual home, and CLAUDE.md rule 5 is explicit that "a parity check is not a fix
        # -- it makes a dual home survivable, therefore permanent". THIS BLOCK STOPS
        # THE BLEED; IT DOES NOT CURE IT. The cure is rule 5's own sequence:
        #   1. WRITER-RETIRE  -- this block, plus the same in any future capture-table
        #                        writer, is the last thing that should ever set the
        #                        column. No new writer of it.
        #   2. READER-RETIRE  -- the live readers are test_db_integrity C06/C07 and
        #                        `governance/pipeline-operations.md`'s stage-4 row.
        #                        Re-point them at the four EXISTS() predicates, which
        #                        are the fact itself rather than a summary of it, and
        #                        C06 dissolves rather than passing.
        #   3. NULL FORWARD   -- the column is NOT NULL with a CHECK, so retiring it
        #                        needs a compensating migration; that migration is the
        #                        right place, not here, because dropping it while a
        #                        blocking check still reads it is how a gate goes red
        #                        on untouched main.
        # AND NOTE WHAT THIS BLOCK HAD TO DO TO EXIST: a JUDGMENT-stage writer reaching
        # back to UPDATE an EVIDENCE-stage row. The 2026-08-27 hand-off ruling names
        # that act directly -- a back-pointer filled in later "require[s] a write into a
        # completed stage, which is what rule 5 exists to stop", and its answer there was
        # to move the fact to the stage that owns it. That the only way to keep C06
        # honest is a cross-stage write is not an argument for the write; it is the
        # clearest available evidence that the column is in the wrong home. Recorded
        # here rather than resolved, because resolving it is the compensating migration
        # in step 3 above.
        #
        # Grep `data_capture_status` before touching any of this: the whole reader set
        # is four files and it is small on purpose.
        _upd = dbcore.upd(session)
        captured = conn.execute(
            "UPDATE evidence_sources SET data_capture_status='captured', "
            "updated_at=?, updated_by_session=? "
            "WHERE ref_id=? AND data_capture_status<>'captured'",
            (_upd["updated_at"], _upd["updated_by_session"], ref)).rowcount
        return {"extraction_id": extraction_id, "ref_id": ref, "parameter_id": pid,
                "slug": row.get("slug"),
                "lens": {c: row.get(c) for c in _LENS_COLUMNS if row.get(c)},
                "claim_type": claim_type, "claimed_value": value,
                "figure_role": figure_role, "comparator": row.get("comparator"),
                "relation_ids": relation_ids,
                "siblings_for_this_parameter": len(prior),
                # Reported, not silent: a status change on ANOTHER table is exactly
                # the kind of side effect an operator should see in the same output
                # as the write that caused it.
                "data_capture_status_set_captured": bool(captured),
                "dry_run": dry_run}


def relate_extraction(from_extraction: int, relation: str, session: str,
                      dry_run: bool = False, to_extraction: int = None,
                      to_label: str = None, to_kind: str = None, stated: str = None,
                      quote: str = None, input_role: str = None, notes: str = None,
                      cross_source_reason: str = None):
    """Add ONE comparator edge to an EXISTING extraction row (migration 075).

    The companion to `insert_extraction`'s own `relations=` for a figure that was
    written before this table existed, or before its comparator was known -- 8 rows
    were already live when migration 075 landed and every refusal below is the one
    `_write_relation_edge` also runs for an edge written at `add-extraction` time,
    so a row's edge set cannot depend on which verb happened to write it first.
    """
    with dbcore.connect(dry_run) as conn:
        row = conn.execute(
            "SELECT extraction_id, ref_id, figure_role, comparator "
            "FROM source_value_extractions WHERE extraction_id=?",
            (from_extraction,)).fetchone()
        if row is None:
            raise Refusal(
                f"relate-extraction: --from {from_extraction}: no such extraction.")
        rid = _write_relation_edge(
            conn, from_id=from_extraction, from_ref_id=row["ref_id"],
            from_figure_role=row["figure_role"], from_comparator=row["comparator"],
            relation=relation, to_extraction=to_extraction, to_label=to_label,
            to_kind=to_kind, stated=stated, quote=quote, input_role=input_role,
            notes=notes, cross_source_reason=cross_source_reason,
            session=session, context="relate-extraction")
    return {"relation_id": rid, "from_extraction_id": from_extraction,
            "relation": relation, "dry_run": dry_run}


def repoint_extraction_relation(from_extraction: int, relation: str,
                                to_extraction: int, session: str,
                                dry_run: bool = False, old_label: str = None):
    """Turn an existing LABEL edge into a real ROW pointer.

    How an 'ADAAG' `to_label` edge becomes a real `to_extraction_id` pointer once
    ADA §405 is itself admitted and extracted: NULL the label and kind, point the
    edge at the new row, and ledger the old label into `notes` rather than losing
    it -- the append discipline `amend-search`/`amend-source` already use, applied
    to a column instead of a whole row.
    """
    with dbcore.connect(dry_run) as conn:
        if to_extraction == from_extraction:
            raise Refusal(
                f"--repoint: --to-extraction {to_extraction} is the same row this "
                f"edge is FROM. A figure cannot be its own comparator.")
        if not dbcore.exists(conn, "source_value_extractions",
                             "extraction_id", to_extraction):
            raise Refusal(
                f"--repoint: --to-extraction {to_extraction}: no such extraction. "
                f"Admit and extract the standard before repointing onto it.")
        q = ("SELECT relation_id, to_label FROM extraction_relations "
             "WHERE from_extraction_id=? AND relation=? AND to_extraction_id IS NULL")
        params = [from_extraction, relation]
        if old_label:
            q += " AND to_label=?"
            params.append(old_label)
        candidates = conn.execute(q, params).fetchall()
        if not candidates:
            raise Refusal(
                f"--repoint: no LABEL edge found for extraction {from_extraction}, "
                f"relation {relation!r}"
                + (f", label {old_label!r}" if old_label else "") +
                ". Nothing to repoint -- write the edge first with relate-extraction, "
                "or check --from/--relation/--old-label.")
        if len(candidates) > 1:
            raise Refusal(
                f"--repoint: {len(candidates)} label edges match extraction "
                f"{from_extraction}, relation {relation!r} -- "
                f"{[c['to_label'] for c in candidates]}. Disambiguate with "
                f"--old-label.")
        rel_id, old_label_val = candidates[0]["relation_id"], candidates[0]["to_label"]
        dup = conn.execute(
            "SELECT relation_id FROM extraction_relations WHERE from_extraction_id=? "
            "AND relation=? AND to_extraction_id=?",
            (from_extraction, relation, to_extraction)).fetchone()
        if dup:
            raise Refusal(
                f"--repoint: extraction {from_extraction} already carries a "
                f"{relation!r} edge to extraction {to_extraction} (relation_id "
                f"{dup[0]}). Repointing would collide with it -- nothing written.")
        existing_notes = conn.execute(
            "SELECT notes FROM extraction_relations WHERE relation_id=?",
            (rel_id,)).fetchone()["notes"]
        stamp = dbcore.now()
        marker = (f" || {stamp[:10]} repointed: to_label {old_label_val!r} -> "
                  f"to_extraction_id {to_extraction}")
        merged = ((existing_notes or "").rstrip() + marker).strip()
        conn.execute(
            "UPDATE extraction_relations SET to_extraction_id=?, to_label=NULL, "
            "to_kind=NULL, notes=? WHERE relation_id=?",
            (to_extraction, merged, rel_id))
    return {"relation_id": rel_id, "repointed_from_label": old_label_val,
            "to_extraction_id": to_extraction, "dry_run": dry_run}


# Only these two, ever. Every other column on this table is a SECOND ROW and a
# contest (D-0168) when it turns out wrong, not an overwrite -- the same rule
# `add-population-match` states for itself by deliberately permitting a dissenting
# second row. figure_role/comparator are GRADING columns migration 075 added NULL
# onto 8 pre-existing rows ("not yet graded"); filling that in later is not a
# contest over what the source said.
# extraction_method and extraction_status added 2026-09-18. They are PROVENANCE,
# not the claim: they record HOW a row was made and how far it has been checked.
# The refusal below is right that a changed claimed_value or claim_text is a
# second row and a contest (D-0168) -- but a row filed `skim`/`preliminary` off an
# abstract, and later CONFIRMED against the full text with the value unchanged, is
# not a contest and filing a duplicate row asserting the same value would
# manufacture one. R15 requires re-describing a staged item from the source on
# resolution; until now there was no way to record that the re-description
# happened. Verified against REF-01001, whose two rows were filed from a
# Crossref-deposited abstract while MDPI was Akamai-blocked.
# root_type ADDED 2026-09-20. It is the same class as figure_role -- a JUDGEMENT about
# what KIND of thing a figure is, which no payload settles -- and it had no repair path,
# so a wrong grade at write time was permanent. Batch 19 wrote root_type
# 'measurement_primary' with root_ref_id NULL on a value REF-01005 did not measure and
# whose actual source this corpus does not hold. The prose field beside it said so
# honestly; the typed columns said "a primary measurement whose root is nothing", and
# nothing could see the contradiction: v_unregistered_roots, which exists for exactly
# this, filters on root_id IS NOT NULL, so a row that leaves root_id null is not examined
# at all. The vocabulary already carried the right value, 'untraced'. Gated below by the
# column's own CHECK, so this widens WHO may correct it, not WHAT to.
_AMENDABLE_SVE_FIELDS = frozenset({"figure_role", "comparator",
                                   "extraction_method", "extraction_status",
                                   "root_type", "root_ref_id"})


def amend_extraction(extraction_id: int, field: str, value: str, reason: str,
                     session: str, dry_run: bool = False):
    """Change figure_role or comparator on an EXISTING row -- and ONLY those two.

    Every other refusal here mirrors the one `insert_extraction` runs at write
    time, because grading a pre-existing row after the fact must not be able to
    reach a state add-extraction itself refuses to create.
    """
    if field not in _AMENDABLE_SVE_FIELDS:
        raise Refusal(
            f"amend-extraction: --field {field!r} refused. Only "
            f"{sorted(_AMENDABLE_SVE_FIELDS)} may be amended here -- a wrong "
            f"claimed_value or claim_text is a SECOND ROW and a contest (D-0168), "
            f"not an overwrite. Write another `db.py add-extraction` if the "
            f"disagreement is over the value or the claim itself.")
    reason = (reason or "").strip()
    if not reason:
        raise Refusal(
            "amend-extraction: --reason is required. An amendment that cannot say "
            "why cannot be contested.")
    value = (value or "").strip()
    if not value:
        raise Refusal("amend-extraction: --value is required and must not be blank.")
    with dbcore.connect(dry_run) as conn:
        # SELECT * rather than a hand-listed column set. The list here was
        # "extraction_id, ref_id, figure_role, comparator, claim_type, notes" and
        # broke with IndexError the moment _AMENDABLE_SVE_FIELDS grew -- a second
        # place naming the amendable columns, one line below the constant that
        # names them. Two lists, one truth.
        row = conn.execute(
            "SELECT * FROM source_value_extractions WHERE extraction_id=?",
            (extraction_id,)).fetchone()
        if row is None:
            raise Refusal(f"amend-extraction: extraction_id {extraction_id}: no "
                          f"such row.")
        # BOTH GATES, DERIVED, ON EVERY AMENDABLE FIELD. The first version of this gated
        # one column by name -- `if field == "root_ref_id"` -- twenty lines below a
        # generic check_declared in amend_source, which is the field-by-field shape rule 8
        # forbids and which this very commit had just criticised. fk_declared reads
        # PRAGMA foreign_key_list, so it is a no-op where no FK is declared and covers
        # every amendable reference the day one becomes amendable.
        dbcore.fk_declared(conn, "source_value_extractions", field, value,
                           f"amend-extraction --field {field}")
        dbcore.check_declared(conn, "source_value_extractions", field, value,
                              "amend-extraction")

        old = row[field]
        if field == "figure_role":
            if row["claim_type"] == "absent" and value != "finding":
                raise Refusal(
                    f"amend-extraction: extraction {extraction_id} has "
                    f"claim_type='absent' -- absence IS a finding, so figure_role "
                    f"must stay 'finding', not {value!r}.")
            if value == "derived":
                base_edge = conn.execute(
                    "SELECT 1 FROM extraction_relations WHERE from_extraction_id=? "
                    "AND relation='derived_from' AND input_role='base'",
                    (extraction_id,)).fetchone()
                if not base_edge:
                    raise Refusal(
                        f"amend-extraction: figure_role='derived' requires at "
                        f"least one derived_from edge carrying input_role=base. "
                        f"extraction {extraction_id} has none -- add one with "
                        f"relate-extraction first.")
            if value == "claim":
                bad = conn.execute(
                    "SELECT relation FROM extraction_relations "
                    "WHERE from_extraction_id=? AND relation IN "
                    "('insufficient','audited_against') LIMIT 1",
                    (extraction_id,)).fetchone()
                if bad:
                    raise Refusal(
                        f"amend-extraction: extraction {extraction_id} carries a "
                        f"{bad[0]!r} edge -- a row finding the baseline inadequate "
                        f"or audited against it asserts no absolute value, so "
                        f"figure_role cannot be 'claim'. Leave it 'finding'.")

        if old == value:
            # THE REASON IS STILL RECORDED. This path used to return early and DISCARD
            # --reason, although the flag's own help says it is "Appended to notes, never
            # overwriting it". A session that re-examined a row, found the value already
            # right, and wrote down what it had learned got a silent no-op -- the finding
            # vanished. Measured on this batch: a correction recording that a quote had
            # been confirmed against a rendered page image, and that the row's page
            # locator means the one-based PDF page rather than the index an earlier note
            # called it, was written and lost.
            #
            # "I checked, and it was already correct, and here is what I found" is a real
            # result and often a more useful one than a change, because it is the only
            # trace that the checking happened at all.
            stamp = dbcore.now()
            marker = f" || {stamp[:10]} {field} CONFIRMED {value} ({reason})"
            conn.execute(
                "UPDATE source_value_extractions SET notes=?, updated_at=?, "
                "updated_by_session=? WHERE extraction_id=?",
                ((row["notes"] or "").rstrip() + marker, stamp, session, extraction_id))
            return {"extraction_id": extraction_id, "field": field, "changed": False,
                    "reason": "already this value; the reason is recorded on notes",
                    "dry_run": dry_run}

        stamp = dbcore.now()
        old_disp = "NULL" if old is None else old
        marker = f" || {stamp[:10]} {field} SET {old_disp} -> {value} ({reason})"
        merged = (row["notes"] or "").rstrip() + marker
        conn.execute(
            f"UPDATE source_value_extractions SET {field}=?, notes=?, "
            f"updated_at=?, updated_by_session=? WHERE extraction_id=?",
            (value, merged, stamp, session, extraction_id))
    return {"extraction_id": extraction_id, "field": field, "old": old, "new": value,
            "changed": True, "dry_run": dry_run}


def derive_extraction(*, ref_id: str, slug: str, parameter_id: int, base: int,
                      delta: int, claim_text: str, session: str,
                      dry_run: bool = False, identity: str = None, icf: str = None,
                      needs: str = None, medical: str = None,
                      claimed_value: str = None, claimed_unit: str = None,
                      comparator: str = None, conversion_note: str = None):
    """Write a figure_role='derived' row computed as base + delta, plus the two
    derived_from edges `v_derived_figure_check` (migration 075) re-verifies it
    against -- a derived figure is never a number trusted on faith.

    Reads --base/--delta with a READ-ONLY pass first (their claimed_value/unit are
    needed to compute or check this row's own before `insert_extraction` can be
    called at all); the actual WRITE -- the row and both derived_from edges -- is
    the ONE transaction inside that single `insert_extraction` call, the same
    guarantee every other caller of it gets.
    """
    with dbcore.connect(dry_run, readonly=True) as conn:
        base_row = conn.execute(
            "SELECT extraction_id, ref_id, claimed_value, claimed_unit, claim_text "
            "FROM source_value_extractions WHERE extraction_id=?", (base,)).fetchone()
        if base_row is None:
            raise Refusal(
                f"derive-extraction: --base {base}: no such extraction. A derived "
                f"figure is computed from a row this project actually holds, never "
                f"invented -- extract the base figure first with add-extraction.")
        delta_row = conn.execute(
            "SELECT extraction_id, ref_id, claimed_value, claimed_unit, claim_text "
            "FROM source_value_extractions WHERE extraction_id=?", (delta,)).fetchone()
        if delta_row is None:
            raise Refusal(
                f"derive-extraction: --delta {delta}: no such extraction. Extract "
                f"the delta figure first with add-extraction.")
        if base == delta:
            raise Refusal("derive-extraction: --base and --delta must be different "
                          "rows -- a figure cannot be derived from itself twice.")

        base_unit, delta_unit = base_row["claimed_unit"], delta_row["claimed_unit"]
        # ONE RULE, ONE REFUSAL: if the unit that will be STORED differs from what
        # either input actually carries, a --claimed-unit and a --conversion-note are
        # both mandatory. This was two sequential checks with two near-identical
        # messages -- one for "base and delta disagree", one for "your override
        # disagrees with base" -- which are the same rule seen from two sides, and
        # which a later change to the reconciliation policy would have had to find in
        # two places that only inspection kept in sync.
        unit = claimed_unit or base_unit
        if (base_unit != delta_unit or unit != base_unit) and not (
                claimed_unit and (conversion_note or "").strip()):
            raise Refusal(
                f"derive-extraction: the unit this row would store ({unit!r}) is not "
                f"the unit both inputs carry -- base (extraction {base}) is "
                f"{base_unit!r}, delta (extraction {delta}) is {delta_unit!r}. Pass "
                f"--claimed-unit WITH a --conversion-note saying how they reconcile, "
                f"or fix the mismatched row first. Note that a converted row is "
                f"invisible to v_derived_figure_check, which joins on equal units, so "
                f"the conversion note is the only record of the arithmetic.")

        def _num(x):
            try:
                return float(x)
            except (TypeError, ValueError):
                return None
        bn, dn = _num(base_row["claimed_value"]), _num(delta_row["claimed_value"])
        if claimed_value is not None:
            cn = _num(claimed_value)
            if bn is not None and dn is not None and cn is not None \
                    and abs(cn - (bn + dn)) > 1e-9:
                raise Refusal(
                    f"derive-extraction: --claimed-value {claimed_value} does not "
                    f"equal base + delta (base extraction {base} = {base_row['claimed_value']!r}, "
                    f"delta extraction {delta} = {delta_row['claimed_value']!r}, sum "
                    f"= {bn + dn}). A derived figure that disagrees with its own "
                    f"inputs is the defect this verb exists to prevent. Nothing "
                    f"was written.")
        elif bn is not None and dn is not None:
            claimed_value = _fmt_num(bn + dn)
        else:
            raise Refusal(
                f"derive-extraction: --claimed-value is required when base or "
                f"delta does not parse as a plain number (base extraction {base} "
                f"= {base_row['claimed_value']!r}, delta extraction {delta} = "
                f"{delta_row['claimed_value']!r}).")

        data = {"ref_id": ref_id, "slug": slug, "parameter_id": parameter_id,
                "identity_code": identity, "icf_code": icf, "needs_code": needs,
                "medical_code": medical, "claim_type": "numerical",
                "claimed_value": claimed_value, "claimed_unit": unit,
                "claim_text": claim_text, "figure_role": "derived",
                "comparator": comparator, "extraction_method": "auto-mined",
                "root_type": "derived_calculation", "root_ref_id": base_row["ref_id"]}
        # EACH EDGE CARRIES ITS OWN TARGET'S QUOTE, not this row's claim_text.
        # Corrected 2026-09-13 before first use. Every edge quote is checked as a
        # byte-substring of a persisted retrieval artefact, and a derived row's
        # claim_text is by its nature the analyst's computation statement -- not
        # something any source said. Passing it as both edge quotes made this verb
        # STRUCTURALLY UNABLE TO SUCCEED: the only path through it was a refusal,
        # which is worse than a missing verb because it looks implemented.
        #
        # The base and delta rows' own claim_text values already passed that check
        # when those rows were written, so using them is an APPLICATION of the rule
        # rather than a carve-out from it -- and it is also the truer record: the
        # warrant for "this figure derives from that one" is what that one says.
        relations = [
            {"relation": "derived_from", "to_extraction": base, "stated": "named",
             "quote": base_row["claim_text"], "input_role": "base"},
            {"relation": "derived_from", "to_extraction": delta, "stated": "named",
             "quote": delta_row["claim_text"], "input_role": "delta"},
        ]
    return insert_extraction(data, session=session, dry_run=dry_run,
                             relations=relations)


def _next_local_ref_id(conn, slug: str) -> str:
    """The next unused local_ref_id for `slug`, INHERITING that slug's scheme.

    A slug labelled ACG-01..ACG-09 gets ACG-10, not "10". Mixing two schemes in
    one slug breaks citation_mining, which copies this label out of
    source_slug_links and joins it as a string.

    This lives here, on the single writer, because `add-source` needs the same
    answer: its refusal used to tell the operator to run the SELECT by hand and
    pass the result, which is rule 8's anti-pattern -- a field that can only be
    right or wrong, never informative.

    The scheme is INFERRED from the rows rather than declared, because
    source_slug_links has nowhere to declare it. That is a real limit and it is
    why the mixed-scheme case refuses instead of guessing; see GAP-013.
    """
    taken = [r[0] for r in conn.execute(
        "SELECT local_ref_id FROM source_slug_links WHERE slug=?", (slug,))]
    # One pass. The `*` form subsumes a prefix-required `+` form -- a bare "10"
    # matches with an empty group(1) -- so `if m.group(1)` recovers that half
    # without a second pattern that could drift from this one.
    parsed = [m for m in (re.match(r"^([A-Za-z]*[-_]?)(\d+)$", t or "")
                          for t in taken) if m]
    prefixes = {m.group(1) for m in parsed if m.group(1)}
    if len(prefixes) > 1:
        raise Refusal(
            f"slug '{slug}' already mixes local_ref_id label schemes "
            f"({sorted(set(taken))[:6]}); a derived label cannot be trusted to "
            f"match. Pass --local-ref-id with the label you mean (add-source and "
            f"link-source-slug both take it), or reconcile the scheme (GAP-013). "
            f"Nothing was written.")
    nxt = max((int(m.group(2)) for m in parsed), default=0) + 1
    if not prefixes:
        return str(nxt)
    width = max(len(m.group(2)) for m in parsed)
    return f"{prefixes.pop()}{nxt:0{width}d}"


def _check_slug_filable(conn, slug: str) -> str:
    """Refuse a slug nothing should be filed into. Returns its status.

    On the single writer rather than on one caller: `add-source --slug` reaches
    the same INSERT, so a guard on the new verb alone would leave the older path
    able to create exactly the row the new one refuses.
    """
    row = conn.execute("SELECT status, merged_into FROM slugs WHERE slug=?",
                       (slug,)).fetchone()
    if row is None:
        raise Refusal(
            f"slug '{slug}' is not in the slugs registry. The vocabulary is "
            f"the table's own, never a guess.")
    if row[0] == "MERGED":
        raise Refusal(
            f"slug '{slug}' is MERGED into '{row[1]}'. Filing evidence into a "
            f"folded topic hides it from every reader that scopes to the live "
            f"set. File under '{row[1]}' instead.")
    return row[0]


def _check_link_label(conn, slug: str, local_ref_id, ref_id: str) -> str:
    """The label `ref_id` would file under on `slug`: the supplied one, stripped, or
    the derived next one. Refuses a blank supplied label, and a label another ref_id
    already holds on that slug.

    source_slug_links has no UNIQUE(slug, local_ref_id) -- check it with
    `select sql from sqlite_master where name='source_slug_links'` -- so nothing but
    this refusal stops two sources sharing the one label that exists to tell them
    apart inside the slug.
    """
    if local_ref_id is None:
        return _next_local_ref_id(conn, slug)
    label = local_ref_id.strip()
    if not label:
        raise Refusal(
            "--local-ref-id is blank. Omit it to derive the slug's next label, or "
            "give one. Nothing was written.")
    holder = conn.execute(
        "SELECT ref_id FROM source_slug_links WHERE slug=? AND local_ref_id=? "
        "AND ref_id<>?", (slug, label, ref_id)).fetchone()
    if holder:
        raise Refusal(
            f"local_ref_id {label!r} is already held on slug '{slug}' by "
            f"{holder[0]}. A label names one source inside its slug. Choose an "
            f"unused label. Nothing was written.")
    return label


def insert_source_slug_link(ref_id: str, slug: str, local_ref_id: str | None,
                             session: str, dry_run: bool = False,
                             relevance_note: str | None = None, conn=None):
    """Link an evidence source to a slug. THE ONLY INSERT into this table.

    `relevance_note` is the GROUNDS -- which claim of this source bears on this
    slug. D-0174 (ADOPTED) named the defect it exists against: "the adjudication
    is made every time and recorded never." Count it rather than trusting a
    figure here (rule 7a):

        select count(relevance_note), count(*) from source_slug_links;

    `local_ref_id=None` DERIVES the label from the slug's own scheme; a supplied
    label is refused if another ref_id holds it on the slug (_check_link_label).
    Both the guards and the derivation live here, not in a caller, because every
    caller lands the same row.

    `conn`, when given, is a write transaction the caller owns (see _txn).

    Returns (inserted, label). `inserted` is True only when a row was actually
    inserted: the INSERT is OR IGNORE, and a caller that reports success on
    rowcount 0 reports a write it did not perform.
    """
    with _txn(conn, dry_run) as conn:
        _check_slug_filable(conn, slug)
        local_ref_id = _check_link_label(conn, slug, local_ref_id, ref_id)
        cur = conn.execute(
            "INSERT OR IGNORE INTO source_slug_links "
            "(ref_id, slug, local_ref_id, relevance_note, created_at, "
            "created_by_session, updated_at, updated_by_session) "
            "VALUES (?,?,?,?,?,?,?,?)",
            [ref_id, slug, local_ref_id, relevance_note,
             *audit(session).values()]
        )
        return cur.rowcount > 0, local_ref_id


def link_source_slug(ref_id: str, slug: str, rationale: str,
                     session: str, dry_run: bool = False, local_ref_id: str | None = None):
    """Cross-file an ALREADY-ADMITTED source to an ADDITIONAL slug (R9).

    `local_ref_id` is optional and DERIVED when omitted. It exists for the slug whose
    labels already mix schemes, where derivation refuses (GAP-013) and the label could
    otherwise not be said at all; a supplied label another ref_id holds is refused.

    WHY THIS EXISTS. `add-source` refuses a second call for a ref_id with
    R9_REMEDY's instruction -- and until 2026-09-18 no command carried it out,
    so the CLI named an action it could not perform and single-slug filing was
    the only expressible outcome. Derive the shape rather than trusting a
    number here (rule 7a):

        select n, count(*) from (select ref_id, count(distinct slug) n
          from source_slug_links group by ref_id) group by n order by n;

    Owner directive 2026-09-18: "you search by slug, but you have to adjudicate
    by all slugs in a category and stuff for each source" -- the search is
    scoped, the ADMISSION is not.

    A link that exists WITHOUT grounds is backfillable here; one that already
    carries grounds is not overwritten, because that is an amendment and
    amend-source is the shape for those.
    """
    if not (rationale or "").strip():
        raise Refusal(
            "--rationale is required. The link is a JUDGEMENT that this source "
            "speaks to this slug; without the warrant it cannot be told apart "
            "from a mis-file. It is stored in source_slug_links.relevance_note, "
            "the column D-0174 named as recorded never. Name the claim that "
            "bears on this slug.")
    ref_id = dbcore.fold_ref(ref_id)
    with connect(readonly=True) as conn:
        row = conn.execute(
            "SELECT superseded_by_ref_id FROM evidence_sources WHERE ref_id=?",
            (ref_id,)).fetchone()
        if row is None:
            raise Refusal(
                f"{ref_id} is not in evidence_sources. This command cross-files "
                f"an ADMITTED source to a further slug; it does not admit one. "
                f"Use add-source first.")
        if (row[0] or "").strip():
            raise Refusal(
                f"{ref_id} is superseded by {row[0]}. Neither row is a live "
                f"claim, which is the ground add-source's own R9 check uses to "
                f"exclude superseded rows. Cross-file the superseding ref_id.")
        status = _check_slug_filable(conn, slug)
        existing = conn.execute(
            "SELECT local_ref_id, relevance_note FROM source_slug_links "
            "WHERE ref_id=? AND slug=?", (ref_id, slug)).fetchone()
    if existing is not None:
        if (existing[1] or "").strip():
            raise Refusal(
                f"{ref_id} is already linked to '{slug}' AND already carries "
                f"grounds. Refusing to overwrite a recorded judgement.")
        if local_ref_id is not None and local_ref_id.strip() != existing[0]:
            # The backfill below writes grounds only. Accepting a different label here
            # would report a relabel that never happened.
            raise Refusal(
                f"{ref_id} is already linked to '{slug}' under label "
                f"{existing[0]!r}; --local-ref-id {local_ref_id!r} would not be "
                f"written. This verb backfills grounds; it does not relabel. "
                f"Nothing was written.")
        u = _upd(session)
        with connect(dry_run) as conn:
            conn.execute(
                "UPDATE source_slug_links SET relevance_note=?, updated_at=?, "
                "updated_by_session=? WHERE ref_id=? AND slug=?",
                [rationale, u["updated_at"], u["updated_by_session"],
                 ref_id, slug])
        local_ref_id, action = existing[0], "backfilled"
    else:
        wrote, local_ref_id = insert_source_slug_link(
            ref_id, slug, local_ref_id, session, dry_run=dry_run,
            relevance_note=rationale)
        if not wrote:
            raise Refusal(
                f"the INSERT for {ref_id} -> '{slug}' affected no row, so the "
                f"link was NOT written. A concurrent write most likely landed "
                f"it between the check and the insert. Re-run and read the "
                f"refusal.")
        action = "inserted"
    return {"ref_id": ref_id, "slug": slug, "local_ref_id": local_ref_id,
            "slug_status": status, "action": action,
            "relevance_note": rationale, "dry_run": dry_run}


def _refuse_tombstone(conn, ref_id: str, what: str):
    """Refuse to file new work against a SUPERSEDED source (a tombstone).

    supersede-source leaves the superseded row in place, and the determination engine
    gathers nothing from it (assess_cell.gather_sources: `superseded_by_ref_id IS NULL`).
    A writer that still accepted it filed an extraction, an observed term or a population
    grade that the engine then dropped without a word: work filed and lost. The same
    ground link-source-slug already refuses on, applied to the writers whose rows the
    engine would drop: add-extraction (and derive-extraction through it), observe-term,
    add-population-match.

    NOT ROUTED THROUGH HERE, on purpose:
      * log-search --admitted-ref-id, link-admission, resolve-candidate --admitted-ref-id:
        they record which search admitted which id, or what a candidate became -- history
        still true of the tombstone, and test_db_integrity S01 reads those edges.
      * log-mining, log-search --mined-ref-id: citation_mining_completeness does not
        filter superseded rows, so a tombstone may still owe a mining row or a deferral,
        and refusing would make that record unwritable.
      * add-economics-entry, raise-determination-gate: nothing drops them by the
        source's liveness; a row pointing at the tombstone is listed among its dependents
        by supersede-source.
      * amend-source, correct-source, amend-extraction, amend-population-match: they
        correct a row's own record, which stays legitimate after supersession.
    """
    row = conn.execute("SELECT superseded_by_ref_id FROM evidence_sources WHERE ref_id=?",
                       (ref_id,)).fetchone()
    if row is not None and (row[0] or "").strip():
        raise Refusal(
            f"{what}: {ref_id} is superseded by {row[0]}. A superseded source is a "
            f"tombstone: the determination engine gathers nothing from it "
            f"(assess_cell.gather_sources reads superseded_by_ref_id IS NULL), so work "
            f"filed against it is silently dropped. File it against {row[0]}. Nothing "
            f"was written.")


def _source_dependents(conn, ref_id: str) -> list:
    """Every row that points at source `ref_id`, by table and column, with its count.

    DERIVED from `PRAGMA foreign_key_list` over every table in sqlite_master, never a
    list: a table that gains a foreign key into evidence_sources is reported the day it
    exists. A column that points at a source WITHOUT a declared foreign key is not seen
    here; `superseded_by_ref_id` is the one such pointer on evidence_sources itself
    (test_db_integrity A09 stands in for its missing FK), so it is added by name.
    """
    out = []
    for (table,) in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
        for fk in conn.execute('PRAGMA foreign_key_list("%s")' % table):
            # fk[2] is the parent table, fk[3] the child column, fk[4] the parent column
            # (None when the FK names the parent's primary key implicitly).
            if fk[2] != "evidence_sources" or fk[4] not in (None, "ref_id"):
                continue
            n = conn.execute('SELECT COUNT(*) FROM "%s" WHERE "%s" = ?'
                             % (table, fk[3]), (ref_id,)).fetchone()[0]
            if n:
                out.append({"table": table, "column": fk[3], "rows": n})
    n = conn.execute("SELECT COUNT(*) FROM evidence_sources WHERE superseded_by_ref_id=?",
                     (ref_id,)).fetchone()[0]
    if n:
        out.append({"table": "evidence_sources", "column": "superseded_by_ref_id",
                    "rows": n})
    return out


def supersede_source(ref_id: str, by: str, reason: str, session: str,
                     dry_run: bool = False) -> dict:
    """Mark admitted source `ref_id` as SUPERSEDED BY admitted source `by` (GAP-060).

    The merge path for a source admitted twice: a mirror of an official document, or a
    DOI-less re-entry that test_db_integrity D04 reports as an author+year+title
    collision. Until this verb the only ways to merge were a curated exemption list
    (D04's KNOWN_DUP_SOURCE_KEYS, which leaves the mirror live and counted) or hand SQL.

    NEITHER ROW IS DELETED. `ref_id` keeps its id and every row that points at it, and
    gains `superseded_by_ref_id` plus a dated SUPERSEDED line in `notes`. Its dependents
    are REPORTED, not moved. Some readers skip a superseded source: assess_cell's gather
    (`superseded_by_ref_id IS NULL`), D04, link-source-slug, add-source's DOI duplicate
    check, and (since the review fix of 2026-10-01) add-extraction, observe-term and
    add-population-match, which refuse it rather than file work the engine drops. A figure
    extracted from the superseded row stops being gathered, so re-extract it from `by` if
    `by` does not already carry it.

    KNOWN GAP, NOT FIXED HERE: the views that read evidence_sources do not filter on
    supersession, so a tombstone still appears in them -- v_convergence_sources,
    v_determination_provenance, v_evidence_authors, v_item_provenance,
    v_source_admission and v_source_reach_all as of 2026-10-01. Re-derive rather than
    trust the list:
        select name from sqlite_master where type='view' and sql like '%evidence_sources%'
           and sql not like '%superseded_by_ref_id%';
    A view change is a schema change, and it belongs in its own migration.

    Refuses: A == B; either missing; A already superseded; B itself superseded (no
    chains); a blank reason; and a LIVE determination resting on A
    (dbcore.determinations_resting_on) -- moving its source would change a written
    answer silently, so retire the specification first.

    Not refused, REPORTED: rows already superseded BY A. They appear in the dependents
    as evidence_sources.superseded_by_ref_id and, after this call, point at a tombstone.
    No verb re-points them; refusing would leave A's duplicate live with no way out.
    """
    a, b = dbcore.fold_ref(ref_id), dbcore.fold_ref(by)
    if not a or not b:
        raise Refusal("supersede-source needs both --ref-id and --by. Nothing was written.")
    reason = dbcore.require_reason(
        reason, f"supersede {a}",
        why="A supersession that cannot say why cannot be contested.")
    if a == b:
        raise Refusal(f"{a} cannot supersede itself. Nothing was written.")
    with connect(dry_run) as conn:
        rows = {r["ref_id"]: r for r in conn.execute(
            "SELECT ref_id, superseded_by_ref_id, notes FROM evidence_sources "
            "WHERE ref_id IN (?, ?)", (a, b))}
        for rid, flag in ((a, "--ref-id"), (b, "--by")):
            if rid not in rows:
                raise Refusal(
                    f"{flag} {rid} is not in evidence_sources. Supersession is between "
                    f"two ADMITTED sources. Nothing was written.")
        if (rows[a]["superseded_by_ref_id"] or "").strip():
            raise Refusal(
                f"{a} is already superseded by {rows[a]['superseded_by_ref_id']}. A "
                f"supersession is not amended by a second call. Nothing was written.")
        if (rows[b]["superseded_by_ref_id"] or "").strip():
            raise Refusal(
                f"{b} is itself superseded by {rows[b]['superseded_by_ref_id']}. No "
                f"chains: supersede {a} by {rows[b]['superseded_by_ref_id']} instead. "
                f"Nothing was written.")
        resting = dbcore.determinations_resting_on(conn, a)
        if resting:
            named = ", ".join(f"specification {sid} (via {junction})"
                              for junction, sid in resting)
            raise Refusal(
                f"{a} carries a live determination: {named}. Superseding it would "
                f"change the evidence set of a written answer without re-deciding it. "
                f"Retire the specification first (db.py retire-specification), then "
                f"supersede, then re-determine. Nothing was written.")
        dependents = _source_dependents(conn, a)
        stamp = now()
        notes = dbcore.append_dated_note(rows[a]["notes"], "SUPERSEDED", session,
                                         f"by {b}: {reason}", stamp)
        conn.execute(
            "UPDATE evidence_sources SET superseded_by_ref_id=?, notes=?, updated_at=?, "
            "updated_by_session=? WHERE ref_id=?", (b, notes, stamp, session, a))
    return {"ref_id": a, "superseded_by": b, "reason": reason,
            "dependents_left_in_place": dependents, "dry_run": dry_run}


def get_unmined_for_all_slugs(tier_max: int = 3) -> list[dict]:
    """Return all unmined Tier 1–N sources across all slugs.

    Non-English sources (lang_detected/language not in {'en', NULL}) sort first
    within each tier, per the citation-mining non-English priority ordering.
    """
    with connect(readonly=True) as conn:
        rows = conn.execute("""
            SELECT ssl.local_ref_id, ssl.slug,
                   es.doi, es.tier, es.pub_title AS title,
                   COALESCE(es.lang_detected, es.language) AS lang,
                   COALESCE(es.citation_mining_status, '') AS citation_mining_status,
                   cm.deferred_reason,
                   COALESCE(cm.backward, 0) AS backward,
                   COALESCE(cm.forward, 0) AS forward
            FROM source_slug_links ssl
            JOIN evidence_sources es ON ssl.ref_id = es.ref_id
            LEFT JOIN citation_mining cm
                -- POINTER, NOT COPY (owner ruling 2026-08-24). This joined on
                -- local_ref_id, the per-slug LABEL, which is copied into both tables
                -- and had already drifted: source_slug_links held RAP-06/09/10 while
                -- citation_mining held RAP-F61/F69/F70 for the same three sources, so
                -- REF-00561/00969/00970 reported UNMINED after being fully mined. The
                -- reference id was in every row the whole time; join on it.
                ON cm.slug = ssl.slug AND cm.global_ref_id = ssl.ref_id
            WHERE es.tier <= ?
            -- SENTINEL MUST MATCH THE JOIN KEY. PD-0 repointed the join to
            -- global_ref_id and left this testing local_ref_id -- the old key. It
            -- works only while every mining row happens to carry a label, and
            -- log_mining LOOKS UP that label from source_slug_links, writing NULL
            -- when no link exists. A mined source with a NULL label would report
            -- UNMINED: the exact PD-0 false negative, surviving in the WHERE clause
            -- after the JOIN was fixed. Test the key the join actually uses.
            -- Same sweep as get_unmined_sources above: the owner ruling of 2026-09-18
            -- makes citation_mining_status the answer and the direction flags a
            -- different question. Kept in step deliberately -- two verbs answering
            -- "what is unmined" differently is how a backlog goes half-invisible.
            AND COALESCE(es.citation_mining_status, '') <> 'mined'
            ORDER BY es.tier ASC,
                     CASE WHEN COALESCE(es.lang_detected, es.language, 'en') = 'en' THEN 1 ELSE 0 END,
                     ssl.slug, ssl.local_ref_id
        """, [tier_max]).fetchall()
    return [dict(r) for r in rows]


def add_supersession_check(*, slug: str, local_ref_id: str, ref_id: str,
                           anchor_tier: int, anchor_evidence_type: str,
                           outcome: str,
                           superseding_ref_ids: list, superseding_dois: list,
                           refinement_dimension: str | None,
                           divergence_notes: str | None,
                           search_strategy_record: str,
                           candidates_returned: int, candidates_reviewed: int,
                           check_method: str,
                           notes: str | None,
                           session: str, dry_run: bool = False) -> str:
    """Insert a supersession_check row (DR-2026-05-24, migration 015).

    Returns the generated check_id. Uses a deterministic id based on
    (slug, local_ref_id, created_at) so repeat calls in the same session don't collide.
    """
    import hashlib
    from datetime import datetime, timezone
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    seed = f"{slug}|{local_ref_id}|{created_at}|{session}"
    check_id = "SUPCHK-" + hashlib.sha256(seed.encode()).hexdigest()[:12]
    with connect(dry_run) as conn:
        conn.execute("""
            INSERT INTO supersession_check (
                check_id, slug, local_ref_id, ref_id,
                anchor_tier, anchor_evidence_type,
                outcome, superseding_ref_ids, superseding_dois,
                refinement_dimension, divergence_notes,
                search_strategy_record, candidates_returned, candidates_reviewed,
                created_at, created_by_session, check_method, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            check_id, slug, local_ref_id, ref_id,
            anchor_tier, anchor_evidence_type,
            outcome,
            json.dumps(superseding_ref_ids) if superseding_ref_ids else None,
            json.dumps(superseding_dois) if superseding_dois else None,
            refinement_dimension, divergence_notes,
            search_strategy_record, candidates_returned, candidates_reviewed,
            created_at, session, check_method, notes,
        ])
    return check_id


# ── DR-2026-05-26 helpers (migration 017) ─────────────────────────────────

def add_gap_mining(*, gap_id: str,
                   search_strategy_record: str,
                   candidates_returned: int, candidates_reviewed: int,
                   outcome: str,
                   discoveries_logged: list,
                   candidate_dois: list,
                   check_method: str,
                   notes: str | None,
                   session: str, dry_run: bool = False) -> int:
    """Insert a gap_mining row (DR-2026-05-26, migration 017).

    Returns the autoincrement gap_mining_id. Append-only: multiple attempts per
    gap_id are allowed; the most recent row (MAX(created_at)) is the operative
    outcome.
    """
    from datetime import datetime, timezone
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with connect(dry_run) as conn:
        cur = conn.execute("""
            INSERT INTO gap_mining (
                gap_id, created_at, created_by_session,
                search_strategy_record, candidates_returned, candidates_reviewed,
                outcome, discoveries_logged, candidate_dois,
                check_method, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            gap_id, created_at, session,
            search_strategy_record, candidates_returned, candidates_reviewed,
            outcome,
            json.dumps(discoveries_logged) if discoveries_logged else None,
            json.dumps(candidate_dois) if candidate_dois else None,
            check_method, notes,
        ])
        return cur.lastrowid


def update_gap_addressability(*, gap_id: str, addressability: str,
                              session: str, dry_run: bool = False):
    """Set gaps.mining_addressability (DR-2026-05-26, migration 017).

    Per-gap classification of resolution path. Defaults from gaps.skill at
    triage time per DR §Addressability classification.
    """
    if addressability not in ("ADDRESSABLE", "NOT-ADDRESSABLE", "TRIAGE-NEEDED"):
        raise Refusal(f"Invalid addressability: {addressability}")
    u = _upd(session)
    with connect(dry_run) as conn:
        conn.execute(
            "UPDATE gaps SET mining_addressability=?, "
            "updated_at=?, updated_by_session=? "
            "WHERE gap_id=?",
            [addressability, u["updated_at"], u["updated_by_session"], gap_id]
        )


def get_unmined_gaps(*, gap_id: str | None = None,
                     priority: str | None = None,
                     include_not_addressable: bool = False,
                     include_recent: bool = False) -> list[dict]:
    """Query mining-eligible gaps (DR-2026-05-26).

    Returns OPEN gaps with mining_addressability=ADDRESSABLE (or all if
    include_not_addressable) that either have no gap_mining row OR whose most
    recent created_at is older than 6 months (per re-eligibility rules in
    DR §5). include_recent overrides the 6-month filter.

    Each result row includes: gap_id, priority, status, skill, section,
    description (truncated), mining_addressability, latest_attempt_at,
    latest_outcome (NULL if never mined).
    """
    from datetime import datetime, timezone, timedelta
    horizon_iso = (datetime.now(timezone.utc) - timedelta(days=183)).strftime("%Y-%m-%dT%H:%M:%SZ")

    where = ["g.status LIKE 'OPEN%'"]
    params: list = []
    if gap_id:
        where.append("g.gap_id = ?")
        params.append(gap_id)
    if priority:
        where.append("g.priority = ?")
        params.append(priority)
    if not include_not_addressable:
        # ADDRESSABLE or NULL (NULL treated as TRIAGE-NEEDED per DR);
        # exclude NOT-ADDRESSABLE explicitly
        where.append("(g.mining_addressability IN ('ADDRESSABLE', 'TRIAGE-NEEDED') "
                     "OR g.mining_addressability IS NULL)")
    where_sql = " AND ".join(where)

    sql = f"""
        SELECT g.gap_id, g.priority, g.status, g.skill, g.section,
               substr(g.description, 1, 180) AS description_snippet,
               g.mining_addressability,
               latest.created_at AS latest_attempt_at,
               latest.outcome    AS latest_outcome
          FROM gaps g
          LEFT JOIN (
              SELECT gm.gap_id, gm.created_at, gm.outcome
                FROM gap_mining gm
                JOIN (
                    SELECT gap_id, MAX(created_at) AS max_at
                      FROM gap_mining
                     GROUP BY gap_id
                ) m ON m.gap_id = gm.gap_id AND m.max_at = gm.created_at
          ) latest ON latest.gap_id = g.gap_id
         WHERE {where_sql}
    """
    rows = []
    with connect(readonly=True) as conn:
        conn.row_factory = sqlite3.Row
        for r in conn.execute(sql, params):
            d = dict(r)
            if not include_recent and d.get("latest_attempt_at"):
                # Skip if attempted within last 6 months UNLESS outcome was
                # partial_evidence_found or deferred (those re-eligible
                # immediately per DR §5).
                if d["latest_attempt_at"] >= horizon_iso and d["latest_outcome"] in (
                    "null_result", "closure_evidence_found", "gap_recategorized"
                ):
                    continue
            rows.append(d)
    # Sort: P1 first, then by gap_id
    priority_order = {"P1": 1, "P2": 2, "P3": 3}
    rows.sort(key=lambda r: (priority_order.get(r["priority"], 9), r["gap_id"]))
    return rows


# ===========================================================================
# ACT 2 (2026-08-25) — the five tables the CLI could not write, plus the stash.
#
# WHY THESE EXIST AT ALL. CLAUDE.md §4 said, in terms: db.py has no subcommand
# for search_candidates, evidence_population_match, economics_entries,
# case_studies or jurisdictional_values, so "those need hand-written SQL against
# the scratch, and THAT GAP IS WHERE THE FABRICATION OF 2026-08-19 ENTERED."
# The gap was the cause, not the setting. These writers close it.
#
# WHAT THEY ARE FOR IS THE REFUSALS. A writer that merely INSERTs is worse than
# hand SQL, because it looks safe. Each one below pre-checks its foreign keys,
# derives its vocabulary from the live table (never a list in this file -- rule 5),
# and refuses rather than guesses. Every refusal here has a selftest case proving
# it fires AND a case proving the legitimate shape still passes; a refusal with
# only the first is a tool that stalls the next batch.
# ===========================================================================


def _check_surfaced_in(conn, exec_id, surfaced_in, surfaced_quote, locator, label):
    """Enforce DR-2026-09-26 section 2.2(d)'s refusal on `surfaced_in`/`surfaced_quote`.

    A thin wrapper: `retrieval_log.check_surfaced_in` is the ONE evaluation, shared
    with `provenance_artefact_audit.py`'s re-derivation (rule 5). `conn` is unused
    here -- retrieval_log opens its own read-only connection, on purpose, staying
    independent of the write path (dbcore.py's docstring: "a writer that verifies
    itself verifies nothing").
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent / "research"))
    import retrieval_log                                              # noqa: E402
    try:
        return retrieval_log.check_surfaced_in(exec_id, surfaced_in, surfaced_quote, locator)
    except ValueError as e:
        raise Refusal(f"{label}: {e}")


def insert_search_candidate(data: dict, session: str, dry_run: bool = False) -> str:
    """Stage a screened-but-not-admitted candidate (research stage)."""
    _COLS = frozenset({
        "candidate_id", "exec_id", "found_under_slug", "suggested_slug", "disposition",
        "title", "locator", "locator_status", "tier_guess", "harm_finding",
        "why_not_admitted", "notes", "surfaced_in", "surfaced_quote",
    })
    dbcore.validate_cols(data.keys(), _COLS, "insert_search_candidate")
    with dbcore.connect(dry_run) as conn:
        if data.get("exec_id") is not None and not dbcore.exists(
                conn, "search_executions", "exec_id", data["exec_id"]):
            raise Refusal(
                f"exec_id {data['exec_id']!r} is not a live search_executions row. "
                f"A candidate is something a SEARCH surfaced; log the search first "
                f"(db.py log-search), then stage what it found.")
        _check_surfaced_in(conn, data.get("exec_id"), data.get("surfaced_in"),
                           data.get("surfaced_quote"), data.get("locator"),
                           "add-candidate")
        if not dbcore.exists(conn, "slugs", "slug", data.get("found_under_slug")):
            raise Refusal(
                f"found_under_slug {data.get('found_under_slug')!r} is not in `slugs`.")
        dbcore.check_vocab(conn, "search_candidates", "disposition",
                           data.get("disposition"), "insert_search_candidate")
        # The same destination rule resolve-candidate applies (_check_rehome_destination),
        # here too because staging is the other writer that can create a REHOME row --
        # and is how six live REHOME rows came to carry no destination at all.
        if data.get("disposition") == "REHOME":
            _check_rehome_destination(conn, "add-candidate", data.get("suggested_slug"),
                                      data.get("found_under_slug"))
        elif data.get("suggested_slug"):
            _check_slug_filable(conn, data["suggested_slug"])
        if data.get("locator_status") is not None:
            dbcore.check_vocab(conn, "search_candidates", "locator_status",
                               data["locator_status"], "insert_search_candidate")
        # R15: a staged description is a HYPOTHESIS. ADMITTED without a resolved
        # locator is the shape that lets a guess harden into a fact.
        if data.get("disposition") == "ADMITTED" and data.get("locator_status") != "RESOLVED":
            raise Refusal(
                "disposition=ADMITTED requires locator_status=RESOLVED. R15: a staged "
                "candidate description is a hypothesis, and admitting one whose locator "
                "was never resolved is how a guess becomes a fact.")
        row = dict(data)
        # `row["session"] = session` stood here until migration 085 renamed the
        # column to `created_by_session`. The stamp_for call on the next line
        # already supplied the right name from the live schema, so the literal
        # was both redundant and the only thing that broke.
        row.update(dbcore.stamp_for(conn, "search_candidates", session))
        if row.get("candidate_id") is None:
            nxt = conn.execute("SELECT COALESCE(MAX(candidate_id),0)+1 FROM search_candidates").fetchone()[0]
            row["candidate_id"] = nxt
        cols = ",".join(row)
        conn.execute(f"INSERT INTO search_candidates ({cols}) VALUES ({','.join('?'*len(row))})",
                     list(row.values()))
    return str(row["candidate_id"])


def insert_population_match(data: dict, session: str, dry_run: bool = False):
    """Grade population-of-STUDY against population-SERVED (R13)."""
    _COLS = frozenset({
        "match_id", "ref_id", "target_population", "study_population",
        "sample_size", "match_grade", "mismatch_note", "gap_id",
    })
    dbcore.validate_cols(data.keys(), _COLS, "insert_population_match")
    with dbcore.connect(dry_run) as conn:
        ref = dbcore.fold_ref(data.get("ref_id"))
        if not dbcore.exists(conn, "evidence_sources", "ref_id", ref):
            raise Refusal(
                f"ref_id {data.get('ref_id')!r} is not an admitted source. Grade the "
                f"match AFTER admission -- a match row for a source that does not exist "
                f"is a claim about nothing.")
        _refuse_tombstone(conn, ref, "add-population-match")
        if not dbcore.exists(conn, "populations", "population_code", data.get("target_population")):
            raise Refusal(
                f"target_population {data.get('target_population')!r} is not in `populations`.")
        dbcore.check_vocab(conn, "evidence_population_match", "match_grade",
                           data.get("match_grade"), "insert_population_match")
        if data.get("match_grade") == "MISMATCH" and not (data.get("mismatch_note") or "").strip():
            raise Refusal(
                "match_grade=MISMATCH requires --mismatch-note. A mismatch that does not "
                "say WHY cannot stop the source drifting into that population's cells later.")

        # DELIBERATELY NOT REFUSED: a second row for the same (ref_id, target_population).
        # DR-2026-08-19 §7 rules that a DISSENTING grade from an adversarial pass lands as
        # a second row distinguished by created_by_session, and that divergent grades read
        # as a contest. A uniqueness refusal here would silently abolish the adversarial
        # mechanic -- the CLI quietly overruling doctrine. If a duplicate is unintended the
        # author sees it in the same session; if it is intended it is the whole point.
        prior = conn.execute(
            "SELECT created_by_session FROM evidence_population_match "
            "WHERE ref_id=? AND target_population=?", (ref, data["target_population"])
        ).fetchall()
        if prior:
            print(f"NOTE: {ref} x {data['target_population']} already graded by "
                  f"{[r[0] for r in prior]}. Writing a second row -- divergent grades read "
                  f"as a contest (DR-2026-08-19 §7), not as an error.", file=sys.stderr)

        row = dict(data)
        row["ref_id"] = ref
        # source_ref is NOT NULL and holds the same value as ref_id -- a live rule-5 dual
        # home this CLI CANNOT remove (committed data migrations INSERT it, so it can never
        # be dropped). What the CLI can do is guarantee the two never disagree: it is
        # written from ref_id, never accepted as a separate argument.
        row["source_ref"] = ref
        row.update(dbcore.stamp_for(conn, "evidence_population_match", session))
        if row.get("match_id") is None:
            # The dissent above is only WRITABLE if the derived id can differ. Until
            # 2026-09-02 this was exactly f"{session}-{ref}-{pop}", so a dissenting grade
            # raised in the SAME session as the grade it dissents from collided on the
            # primary key -- the id derivation quietly abolishing the mechanic the comment
            # above defends. DR-2026-08-19 §7 says "distinguished by created_by_session",
            # which held while adversarial passes were separate sessions; under the
            # agonist/antagonist format they are routinely the same one. Suffix on
            # collision, so the contest can actually be recorded.
            base = f"{session[:24]}-{ref}-{data['target_population']}"
            row["match_id"] = base
            n = 1
            while conn.execute("SELECT 1 FROM evidence_population_match WHERE match_id=?",
                               (row["match_id"],)).fetchone():
                n += 1
                row["match_id"] = f"{base}-{n}"
        cols = ",".join(row)
        conn.execute(f"INSERT INTO evidence_population_match ({cols}) "
                     f"VALUES ({','.join('?'*len(row))})", list(row.values()))
    return row["match_id"]


def insert_jurisdictional_value(data: dict, session: str, dry_run: bool = False):
    """Record a code/regulatory value for an item in a jurisdiction (T4-T6 stratum)."""
    _COLS = frozenset({
        "jv_id", "item_code", "jurisdiction", "standard_name", "value_text",
        "value_numeric", "unit", "is_code_minimum", "evidence_tier", "source_section",
        "notes", "locator_scheme", "loc_division", "loc_part", "loc_section",
        "loc_subsection", "loc_paragraph", "loc_clause", "loc_subclause", "loc_note",
    })
    dbcore.validate_cols(data.keys(), _COLS, "insert_jurisdictional_value")
    dbcore.check_jurisdiction(data.get("jurisdiction"),
                              "add-jurisdictional-value --jurisdiction")
    with dbcore.connect(dry_run) as conn:
        if not dbcore.exists(conn, "items", "item_code", data.get("item_code")):
            raise Refusal(f"item_code {data.get('item_code')!r} is not in `items`.")
        tier = data.get("evidence_tier")
        # RANGE_GUARDS in scripts/emit_data_migration.py owns the 1-6 band and cites
        # schemas/evidence_source.py:85 as its authority. Not restated here (rule 5) --
        # the same band is asserted, and the guard remains the place it is DEFINED.
        if tier is None or not (1 <= int(tier) <= 6):
            raise Refusal(
                f"evidence_tier {tier!r} is outside the ratified 1-6 band "
                f"(RANGE_GUARDS in emit_data_migration.py; governance/tier-system.md).")
        # R3: a quantified value needs a locator or an explicit unverified marker.
        loc_fields = [k for k in _COLS if k.startswith("loc_")] + ["source_section"]
        has_locator = any((data.get(k) or "").strip() for k in loc_fields
                          if isinstance(data.get(k), str))
        if data.get("value_numeric") is not None:
            if not data.get("unit"):
                raise Refusal("--value-numeric requires --unit. A number without a "
                                 "unit is not a value.")
            if not has_locator and "[UNVERIFIED-QUANT]" not in (data.get("notes") or ""):
                raise Refusal(
                    "R3: a quantified code value needs a locator (clause/section/page) "
                    "or an explicit [UNVERIFIED-QUANT] marker in --notes. Nothing written.")
        row = dict(data)
        row.update(dbcore.stamp_for(conn, "jurisdictional_values", session))
        cols = ",".join(row)
        conn.execute(f"INSERT INTO jurisdictional_values ({cols}) "
                     f"VALUES ({','.join('?'*len(row))})", list(row.values()))
    return data.get("jv_id")


def insert_economics_entry(data: dict, session: str, dry_run: bool = False):
    """Record a Part-13 economics finding."""
    _COLS = frozenset({
        "entry_id", "pillar", "entry_type", "ref_id", "source", "finding", "status",
        "value_numeric", "value_unit", "currency", "year", "journal", "jurisdiction",
        "evidence_tier", "study_design", "sample", "source_section", "notes",
    })
    dbcore.validate_cols(data.keys(), _COLS, "insert_economics_entry")
    # The column's DDL comment invites 'MULTI'; the declared code for work spanning
    # jurisdictions is INT, and the blocking audit fails on MULTI either way.
    dbcore.check_jurisdiction(data.get("jurisdiction"),
                              "add-economics-entry --jurisdiction")
    with dbcore.connect(dry_run) as conn:
        dbcore.check_vocab(conn, "economics_entries", "pillar",
                           data.get("pillar"), "insert_economics_entry")
        dbcore.check_vocab(conn, "economics_entries", "entry_type",
                           data.get("entry_type"), "insert_economics_entry")
        ref = dbcore.fold_ref(data.get("ref_id"))
        if ref and not dbcore.exists(conn, "evidence_sources", "ref_id", ref):
            raise Refusal(f"ref_id {data.get('ref_id')!r} is not an admitted source.")
        # THE DUAL-HOME REFUSAL, and a note on WHICH LAYER ENFORCES IT. The CLI does
        # not expose --year/--journal/--study-design/--sample at all, so through
        # `db.py` the restatement is structurally impossible rather than refused --
        # which is stronger. This guard therefore fires only on the PYTHON API path
        # (importers, capture tooling, future writers). Verified 2026-08-25 by calling
        # insert_economics_entry directly; through argparse it is unreachable, and that
        # is the point, not an oversight. Do not "fix" it by adding the flags.
        #
        # `source` is TEXT NOT NULL and sits beside a nullable
        # `ref_id` -- drift by construction once populated. The table is EMPTY today, so
        # the pointer discipline can be enforced before the first row rather than
        # migrated afterwards: when a ref_id is given, the bibliographic facts are
        # reached through it and must not be restated on this row.
        if ref:
            restated = [k for k in ("year", "journal", "study_design", "sample")
                        if data.get(k) is not None]
            if restated:
                raise Refusal(
                    f"--ref-id was given, so {restated} are reachable through it and must "
                    f"not be copied onto this row (CLAUDE.md rule 5: point, do not copy). "
                    f"Omit them; a reader follows ref_id to evidence_sources.")
            row_source = data.get("source") or ref
        else:
            if not (data.get("source") or "").strip():
                raise Refusal(
                    "an entry with no --ref-id must name its --source. `source` is "
                    "NOT NULL and is the only identity a ref-less entry has.")
            row_source = data["source"]
        row = dict(data)
        row["source"] = row_source
        if ref:
            row["ref_id"] = ref
        row.update(dbcore.stamp_for(conn, "economics_entries", session))
        cols = ",".join(row)
        conn.execute(f"INSERT INTO economics_entries ({cols}) "
                     f"VALUES ({','.join('?'*len(row))})", list(row.values()))
    return data.get("entry_id")


def insert_case_study(data: dict, session: str, dry_run: bool = False):
    """Record a Part-12 case study."""
    _COLS = frozenset({
        "case_study_id", "slug", "title", "building_type", "location", "year",
        "harm_finding", "status", "setting", "population_description", "sources",
        "tier", "notes", "part_section",
    })
    dbcore.validate_cols(data.keys(), _COLS, "insert_case_study")
    with dbcore.connect(dry_run) as conn:
        if not dbcore.exists(conn, "slugs", "slug", data.get("slug")):
            raise Refusal(f"slug {data.get('slug')!r} is not in `slugs`.")
        if dbcore.exists(conn, "case_studies", "case_study_id", data.get("case_study_id")):
            raise Refusal(f"case_study_id {data.get('case_study_id')!r} already exists.")
        # `sources` is prose where a junction to evidence_sources.ref_id is the ruling's
        # exact target ("for rendering a citation, we point towards the evidence table").
        # The table is empty, so refuse the copy shape now rather than migrate later:
        # a REF-NNNNN inside the prose field means a pointer was flattened into text.
        if dbcore.REF_ID_SHAPE.search(data.get("sources") or ""):
            raise Refusal(
                "--sources contains a REF-NNNNN. A reference id in a prose field is a "
                "flattened pointer (CLAUDE.md rule 5). Link the source through "
                "case_study_specs / the evidence tables, and keep --sources for material "
                "that has no ref_id.")
        row = dict(data)
        row.update(dbcore.stamp_for(conn, "case_studies", session))
        cols = ",".join(row)
        conn.execute(f"INSERT INTO case_studies ({cols}) VALUES ({','.join('?'*len(row))})",
                     list(row.values()))
    return data.get("case_study_id")


def _lead_name_key(name) -> str:
    """A standard name with case, spacing and punctuation folded away.

    UNICODE-AWARE ON PURPOSE, as test_db_integrity D04's `_norm_title` is: `\\W` under
    re.UNICODE keeps every letter and digit of every script. The ASCII fold first
    proposed for this (`[^a-z0-9]`) erases Korean and Japanese names to the empty
    string, so every non-Latin standard in a jurisdiction would collide with every
    other -- enforcing dedup on the English corpus and blocking the multilingual one.
    """
    return re.sub(r"\W", "", (name or "").casefold(), flags=re.UNICODE)


def insert_code_lead(data: dict, session: str, dry_run: bool = False,
                     distinct_from=None, reason: str = None) -> int:
    """Write a code/standard lead into the research-stage lead store.

    Deliberately NOT a DOI-bearing writer. research_code_leads has no doi column
    (migration 066): a standard is retrieved by clause reference, and letting the two
    identifier shapes share a row format is what put 24 rows in source_locators
    carrying both a standard_number and a DOI.

    A NEAR-DUPLICATE IS REFUSED TOO (I8). The UNIQUE key is exact, so 'DIN 18040-1'
    and 'din 18040 1' could stand as two leads for one document. A name that folds to
    a held name's key (_lead_name_key) in the same jurisdiction is refused, naming the
    held lead, unless `distinct_from` names every such lead and `reason` says why they
    are different documents; the reason is appended to the new row's notes. The cost
    is named: two genuinely different standards whose names differ only in punctuation
    ('ISO 2154-2' beside 'ISO 21542') fold together, and need --distinct-from.
    """
    _COLS = frozenset({
        "jurisdiction", "standard_name", "clause", "status", "recovered_from", "notes",
    })
    dbcore.validate_cols(data.keys(), _COLS, "insert_code_lead")
    jur = (data.get("jurisdiction") or "").strip()
    std = (data.get("standard_name") or "").strip()
    # Both are NOT NULL in the schema; refusing here means the caller gets a sentence
    # instead of an IntegrityError, and refusing on blank means a whitespace string
    # cannot slip past a NOT NULL that only tests for NULL.
    if not jur:
        raise Refusal("--jurisdiction is required and may not be blank: a lead that "
                         "cannot say which jurisdiction it belongs to is not retrievable, "
                         "which is the only purpose this row has.")
    if not std:
        raise Refusal("--standard-name is required and may not be blank.")
    # The declared vocabulary (I7). This is also what makes the duplicate checks below
    # sound: they compare jurisdiction EXACTLY, so 'es' beside 'ES' would split one
    # jurisdiction's leads in two -- and check_jurisdiction refuses the variant.
    dbcore.check_jurisdiction(jur, "add-code-lead --jurisdiction")
    named = set(distinct_from or ())
    reason = (reason or "").strip()
    if reason and not named:
        raise Refusal("--reason is only read beside --distinct-from; it would be dropped. "
                      "Put a lead's own context in --notes. Nothing was written.")
    if named and not reason:
        raise Refusal("--distinct-from needs --reason: two names that differ only in case "
                      "or punctuation are the same document unless someone says why not. "
                      "Nothing was written.")
    notes = data.get("notes")
    with dbcore.connect(dry_run) as conn:
        dbcore.check_vocab(conn, "research_code_leads", "status", data.get("status"),
                           "insert_code_lead")
        # THE DEDUP REFUSAL. 109 archived rows were 83 leads because the same standard was
        # restated once per item. The UNIQUE constraint makes that impossible; this turns
        # it into a sentence naming the row that already holds it -- and, since
        # 2026-10-01, a remedy a verb performs (GAP-005: it used to say "Update that row
        # instead" when no verb could).
        hit = conn.execute(
            "SELECT lead_id FROM research_code_leads WHERE jurisdiction=? AND standard_name=?",
            (jur, std)).fetchone()
        if hit:
            raise Refusal(
                f"{jur} / {std!r} is already held as lead_id {hit[0]}. A code lead is keyed "
                f"on (jurisdiction, standard_name) — restating it is the duplication the "
                f"item-keyed shape produced. Update that row instead: "
                f"`db.py update-code-lead --lead-id {hit[0]} --append-note <what changed>`.")
        # An empty key (a name of symbols only) names nothing to compare; skipping it
        # keeps two such names from colliding on '' -- the ASCII fold's failure, in
        # miniature.
        key = _lead_name_key(std)
        near = [(lid, name) for lid, name in conn.execute(
                    "SELECT lead_id, standard_name FROM research_code_leads "
                    "WHERE jurisdiction=? ORDER BY lead_id", (jur,))
                if key and _lead_name_key(name) == key]
        stray = sorted(named - {lid for lid, _ in near})
        if stray:
            raise Refusal(
                f"--distinct-from {stray}: not a {jur} lead whose name folds to the same key "
                f"as {std!r}, so there is nothing to be distinct from. Nothing was written.")
        unnamed = [(lid, name) for lid, name in near if lid not in named]
        if unnamed:
            held = "; ".join(f"lead_id {lid} {name!r}" for lid, name in unnamed)
            raise Refusal(
                f"{jur} / {std!r} differs from a held lead only in case, spacing or "
                f"punctuation: {held}. That is the same document restated. Update that "
                f"row instead: `db.py update-code-lead --lead-id {unnamed[0][0]} "
                f"--append-note <what changed>`. If they are genuinely two documents, "
                f"re-run with --distinct-from <lead_id> for each and --reason <why>. "
                f"Nothing was written.")
        now = dbcore.now()
        if near:
            notes = dbcore.append_dated_note(
                notes, "DISTINCT-FROM", session,
                "; ".join(f"lead_id {lid} {name!r}" for lid, name in near)
                + f": {reason}", now)
        cur = conn.execute(
            "INSERT INTO research_code_leads (jurisdiction, standard_name, clause, status, "
            "recovered_from, notes, created_at, created_by_session) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (jur, std, data.get("clause"), data.get("status") or "REFERENCE-ONLY",
             data.get("recovered_from"), notes, now, session))
        return cur.lastrowid


def update_code_lead(lead_id: int, append_note: str, session: str, status: str = None,
                     clause: str = None, dry_run: bool = False) -> dict:
    """Move a code lead's status or clause, APPENDING a dated note. GAP-005, I8.

    R15 could not be discharged against a lead: batch 10 retrieved the law behind lead 85,
    proved part of its note false, and nothing could move the status off REFERENCE-ONLY
    or put the correction where a reader of the lead would see it. This is that path.

    APPEND, NEVER REWRITE. The note is a hypothesis about a document someone had not yet
    read (R15); the correction goes after it in a dated ' || UPDATED ...' segment that
    also carries any replaced status or clause, so the next reader sees what was believed
    and what was established -- amend-search's shape, applied to the lead store.

    NO TRANSITION ORDER. The status vocabulary is the column's own CHECK. A forward-only
    order (REFERENCE-ONLY -> RETRIEVED -> SUPERSEDED) would be an ordering list kept
    beside that CHECK, which rule 8 forbids, and it would make a wrongly-set RETRIEVED
    uncorrectable -- the defect this verb exists to end. Every move is ledgered instead.

    A note alone is allowed (a lead re-described without a status change is still R15);
    an identical note already on the row is a no-op. A --status or --clause equal to the
    held value is refused: it asks to move something that is already there.
    """
    note = (append_note or "").strip()
    if not note:
        raise Refusal(
            f"lead {lead_id}: --append-note is required and may not be blank. R15: a lead "
            f"is updated because the source was read, and the note says what it said. "
            f"Nothing was written.")
    if clause is not None and not clause.strip():
        raise Refusal(
            f"lead {lead_id}: --clause may not be blank. Give the locator the retrieved "
            f"document carries; this verb does not clear one. Nothing was written.")
    with dbcore.connect(dry_run) as conn:
        row = conn.execute(
            "SELECT lead_id, jurisdiction, standard_name, clause, status, notes "
            "FROM research_code_leads WHERE lead_id=?", (lead_id,)).fetchone()
        if row is None:
            raise Refusal(f"lead {lead_id}: no such code lead. Nothing was written.")
        moves, sets = [], {}
        if status is not None:
            dbcore.check_vocab(conn, "research_code_leads", "status", status,
                               f"update-code-lead --lead-id {lead_id}")
            if status == row["status"]:
                raise Refusal(
                    f"lead {lead_id}: status is already {status!r}. Omit --status to "
                    f"append a note alone. Nothing was written.")
            moves.append(f"status {row['status']!r} -> {status!r}")
            sets["status"] = status
        if clause is not None:
            clause = clause.strip()
            if clause == (row["clause"] or ""):
                raise Refusal(
                    f"lead {lead_id}: clause is already {clause!r}. Omit --clause to "
                    f"append a note alone. Nothing was written.")
            moves.append(f"clause {row['clause']!r} -> {clause!r}")
            sets["clause"] = clause
        if not moves and note in (row["notes"] or ""):
            return {"lead_id": lead_id, "changed": False,
                    "reason": "this note is already on the row", "dry_run": dry_run}
        stamp = dbcore.upd(session)
        detail = ("; ".join(moves) + ". " if moves else "") + note
        sets["notes"] = dbcore.append_dated_note(row["notes"], "UPDATED", session, detail,
                                                 stamp["updated_at"])
        sets.update(stamp)
        conn.execute(
            "UPDATE research_code_leads SET %s WHERE lead_id=?"
            % ", ".join(f"{c}=?" for c in sets), [*sets.values(), lead_id])
    return {"lead_id": lead_id, "changed": True, "jurisdiction": row["jurisdiction"],
            "standard_name": row["standard_name"], "moves": moves,
            "status": sets.get("status", row["status"]),
            "clause": sets.get("clause", row["clause"]), "appended": detail,
            "dry_run": dry_run}


def insert_locator(data: dict, session: str, dry_run: bool = False) -> str:
    """Write a lead into the clue store."""
    _COLS = frozenset({
        "ref_id", "doi", "pmid", "pmcid", "isbn", "issn", "url", "standard_number",
        "title", "authors", "pub_year", "tier_claimed", "recovered_from", "status",
        "used_in_bpcs", "notes",
    })
    dbcore.validate_cols(data.keys(), _COLS, "insert_locator")
    ref = dbcore.fold_ref(data.get("ref_id"))
    if not ref or not dbcore.REF_ID_SHAPE.fullmatch(ref):
        raise Refusal(
            f"--ref-id {data.get('ref_id')!r} is not a global reference id. Expected "
            f"REF-NNNNN (or REF-VERIFIED-NNN / Co1-NN). Mint with `db.py next-id ref`.")
    with dbcore.connect(dry_run) as conn:
        if dbcore.exists(conn, "source_locators", "ref_id", ref):
            raise Refusal(f"{ref} already exists in source_locators. Use update-locator.")
        dbcore.check_vocab(conn, "source_locators", "status", data.get("status"),
                           "insert_locator")
        doi = dbcore.norm_doi(data.get("doi"))
        if doi:
            # THE DUPLICATE-IDENTITY REFUSAL. Same DOI under a DIFFERENT ref_id is two
            # identities for one source -- the defect R9a/R9b detect after the fact.
            # Case-folded, because 10.1044/2019_AJA-19-0010 and ..._aja-19-0010 are the
            # same DOI and were once stored as two.
            for table in ("source_locators", "evidence_sources"):
                hit = conn.execute(
                    'SELECT ref_id FROM "%s" WHERE LOWER(TRIM(doi))=? AND ref_id<>?' % table,
                    (doi, ref)).fetchone()
                if hit:
                    raise Refusal(
                        f"DOI {data['doi']!r} is already held as {hit[0]} in {table}. "
                        f"{R9_REMEDY}; never mint a second identity "
                        f"for one source. Nothing was written.")
            data = dict(data, doi=doi)
        row = dict(data)
        row["ref_id"] = ref
        # Schema-aware: source_locators carries NO audit columns. Assuming the
        # convention was universal is what refused all 8 rehearsal writes.
        row.update(dbcore.stamp_for(conn, "source_locators", session))
        cols = ",".join(row)
        conn.execute(f"INSERT INTO source_locators ({cols}) VALUES ({','.join('?'*len(row))})",
                     list(row.values()))
    return ref


if __name__ == "__main__":
    # REFUSALS ARE MESSAGES, NOT STACK TRACES. This CLI's whole value is that it says no
    # (CLAUDE.md §4), and its refusals are careful: they cite the ruling, name the remedy
    # and say what was written, which is nothing. Every one of them reached the terminal
    # as the last line of a traceback until 2026-09-10 -- the message at the bottom of a
    # stack the operator did not ask for and has to read past. Same refusals, same exit 1,
    # no stack. Refusal only: anything else keeps its traceback, because anything else is
    # a defect and its location is the evidence.
    try:
        main()
    except Refusal as exc:
        sys.exit(f"REFUSING: {exc}")

