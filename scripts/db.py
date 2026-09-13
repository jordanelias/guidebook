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
                          --connections '["CON-0241"]' --session SESSION
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
    python3 scripts/db.py add-source --ref-id REF-00971 --author "Smith|Jane" --author "corp|WHO" --year 2022 --title "..." --tier 1 --session SESSION [--slug SLUG --local-ref-id RAP-07]
        (--ref-id is the GLOBAL REF-NNNNN; --local-ref-id is the per-slug label. Different values.)
        (--authors "Smith J; Jones K" still works and is parsed into author rows; --author is preferred because it keeps the given name)
    python3 scripts/db.py validate
    python3 scripts/db.py --help
"""

import json
import os
import re
import zipfile
import sqlite3
import sys
import argparse
from contextlib import contextmanager
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
            "UPDATE connections SET status=?, session_applied=?, "
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
    with connect(readonly=True) as conn:
        row = conn.execute(
            "SELECT backward, forward, connections_produced "
            "FROM citation_mining WHERE slug=? AND global_ref_id=?",
            [slug, ref_id]
        ).fetchone()
    return dict(row) if row else None


def log_mining(slug: str, ref_id: str, direction: str,
               connections: list[str], session: str,
               dry_run: bool = False, deferred_reason: str = None,
               status: str = None):
    """Record a mining pass. Keyed on the global ref_id.

    The `doi` parameter was REMOVED 2026-08-24. It wrote a copy of a value that
    is reachable through global_ref_id, and 2 of 10 rows had already drifted by
    case. Accepting it while ignoring it would have been worse than either
    keeping or dropping it: a caller would believe a DOI had been recorded.
    """
    if direction not in _VALID_DIRECTIONS:
        raise Refusal(
            f"direction must be 'backward' or 'forward', got '{direction}'"
        )
    deferred_reason = (deferred_reason or "").strip() or None
    if connections and deferred_reason:
        raise Refusal(
            f"{ref_id}: a pass cannot both produce connections and be deferred. "
            f"Say which happened.")
    if not connections and not deferred_reason:
        raise Refusal(
            f"{ref_id}: no connections and no --deferred-reason. A mining pass that "
            f"found nothing and does not say why is indistinguishable from one that "
            f"never ran (R8's rule for searches, applied to mining).")
    # citation_mining_status is asserted AGAINST this table by test_db_integrity C08:
    # 'mined' iff a non-deferred mining row resolves to it. Nothing in this writer ever
    # moved it, so the biconditional could not hold through the sanctioned path -- the
    # CLI was structurally unable to produce a state its own integrity test accepts.
    if status is None:
        status = "deferred" if deferred_reason else "mined"
    dir_col = direction
    ts = now()

    with connect(dry_run) as conn:
        # THE WRITER IS WHERE THE DRIFT CAME FROM. This took a global ref_id and
        # wrote it into local_ref_id while leaving global_ref_id NULL, so the
        # pointer column the readers need was never populated and the label
        # column carried a value that was not a label. Key on the reference id;
        # derive the label from source_slug_links, which owns it.
        row = conn.execute(
            "SELECT backward, forward, connections_produced "
            "FROM citation_mining WHERE slug=? AND global_ref_id=?",
            [slug, ref_id]
        ).fetchone()
        if row:
            prior = json.loads(row["connections_produced"] or "[]")
            merged = json.dumps(list(dict.fromkeys(prior + connections)))
            conn.execute(
                f"UPDATE citation_mining SET {dir_col}=1, "
                "connections_produced=?, updated_at=?, updated_by_session=? "
                "WHERE slug=? AND global_ref_id=?",
                [merged, ts, session, slug, ref_id]
            )
        else:
            conn.execute(
                # local_ref_id is LOOKED UP, never invented: source_slug_links owns
                # the per-slug label. doi is NOT written -- it is reachable through
                # global_ref_id and copying it is what drifted 2 of 10 rows by case.
                "INSERT INTO citation_mining "
                "(slug,local_ref_id,global_ref_id,backward,forward,"
                " connections_produced,created_at,created_by_session,"
                " updated_at,updated_by_session) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                [slug,
                 (conn.execute("SELECT local_ref_id FROM source_slug_links "
                               "WHERE slug=? AND ref_id=?", [slug, ref_id]
                               ).fetchone() or [None])[0],
                 ref_id,
                 1 if direction == "backward" else 0,
                 1 if direction == "forward" else 0,
                 json.dumps(connections), ts, session, ts, session]
            )
        if deferred_reason:
            conn.execute("UPDATE citation_mining SET deferred_reason=?, updated_at=?, "
                         "updated_by_session=? WHERE slug=? AND global_ref_id=?",
                         [deferred_reason, ts, session, slug, ref_id])
        dbcore.check_vocab(conn, "evidence_sources", "citation_mining_status",
                           status, "--status")
        conn.execute("UPDATE evidence_sources SET citation_mining_status=?, "
                     "updated_at=?, updated_by_session=? WHERE ref_id=?",
                     [status, ts, session, ref_id])


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
        "session": session, "executed_at": ts,
        "findings_note": findings_note, "harm_finding": harm_finding,
        # The prior belongs HERE, on the search, and nowhere else. Migration 069
        # moved it off evidence_sources, where it could only be reconstructed after
        # reading the source -- the artefact the field exists to prevent.
        "prior_expectation": prior_expectation,
    }
    cols = ", ".join(row)
    ph = ", ".join(["?"] * len(row))
    with connect(dry_run) as conn:
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
            AND (cm.backward IS NULL OR cm.forward IS NULL
                 OR cm.backward=0 OR cm.forward=0)
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

# The ratified status vocabulary — owner ruling 2026-08-14, migration 058.
# RESOLUTION-PROPOSED became PROPOSED; MODE-S-ONLY became UNRESOLVED.
_VALID_CONFLICT_STATUS = frozenset({
    "ACTIVE", "PROPOSED", "DEFERRED", "RESOLVED-EVIDENCE",
    "RESOLVED-CONSENSUS", "UNRESOLVED", "CLOSED", "RETIRED", "SUPERSEDED",
})
_VALID_ITEM_STATUS   = frozenset({"draft", "active", "merged", "retired"})
_VALID_RUN_STATUS    = frozenset({"IN-PROGRESS", "COMPLETE", "HANDED-OFF"})
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
    if data.get("status") not in _VALID_CONFLICT_STATUS:
        raise Refusal(f"Invalid conflict status: {data.get('status')}")
    if data.get("pop_a") and data.get("pop_b"):
        if data["pop_a"] > data["pop_b"]:
            raise Refusal(
                f"pop_a must be < pop_b lexicographically. "
                f"Got pop_a={data['pop_a']} pop_b={data['pop_b']}. "
                f"Swap them before inserting."
            )
    row = {**data, **audit(session)}
    with connect(dry_run) as conn:
        cols = ", ".join(row)
        ph   = ", ".join(["?"] * len(row))
        conn.execute(f"INSERT INTO conflicts ({cols}) VALUES ({ph})", list(row.values()))
    return data["conflict_id"]


def update_conflict(conflict_id: str, session: str,
                    status: str = None, resolution: str = None,
                    evidence: str = None, gap_id: str = None,
                    dry_run: bool = False):
    if status and status not in _VALID_CONFLICT_STATUS:
        raise Refusal(f"Invalid conflict status: {status}")
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
    if data.get("status") and data["status"] not in _VALID_RUN_STATUS:
        raise Refusal(f"Invalid audit run status: {data.get('status')}")
    row = {**data, **audit(session)}
    with connect(dry_run) as conn:
        cols = ", ".join(row)
        ph   = ", ".join(["?"] * len(row))
        conn.execute(f"INSERT INTO item_audit_runs ({cols}) VALUES ({ph})", list(row.values()))
    return data["run_id"]


def update_audit_run(run_id: str, session: str,
                     status: str = None, steps_complete: list = None,
                     steps_started: list = None, brief_path: str = None,
                     spec_hash: str = None, dry_run: bool = False):
    if status and status not in _VALID_RUN_STATUS:
        raise Refusal(f"Invalid audit run status: {status}")
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
    p_gaps.add_argument("--priority", choices=["P1", "P2", "P3"])
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
    p_logm.add_argument("--connections",
                        help="JSON array of CON-IDs. Omit only when --deferred-reason "
                             "says why the pass produced none.")
    p_logm.add_argument("--deferred-reason", dest="deferred_reason",
                        help="Why this anchor was NOT mined. Required when no "
                             "connections are given, so a pass that found nothing is "
                             "distinguishable from one that never ran.")
    p_logm.add_argument("--status", dest="mining_status",
                        help="citation_mining_status to set on the source. Live "
                             "vocabulary from the column's own CHECK. Derived when "
                             "omitted: 'mined' with connections, 'deferred' without.")
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
                            "one standard per design parameter is refused.")
    p_rcl.add_argument("--clause", help="R3's locator: clause/section/page, once retrieved")
    p_rcl.add_argument("--status", default="REFERENCE-ONLY",
                       help="Live vocabulary, derived from the table; not a list in this file")
    p_rcl.add_argument("--recovered-from")
    p_rcl.add_argument("--notes")
    p_rcl.add_argument("--session", required=True)
    p_rcl.add_argument("--dry-run", action="store_true")

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
    p_am.add_argument("--set-harm-finding", action="store_true",
                      help="Raise harm_finding 0 -> 1. R7 makes harm first-class, so a "
                           "search logged with the flag down that did surface harm has an "
                           "incomplete record. Only rises; lowering is refused.")
    p_am.add_argument("--session", required=True)
    p_am.add_argument("--dry-run", action="store_true")

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
    p_rc.add_argument("--session", required=True)
    p_rc.add_argument("--dry-run", action="store_true")

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
                       help="Only with --field scope, and only when the new scope "
                            "derives a different tier: moves the tier to the one value "
                            "the ratified ladder produces, in the same statement. The "
                            "tier is never set on its own.")
    p_ams.add_argument("--session", required=True)
    p_ams.add_argument("--dry-run", action="store_true")

    p_ul = sub.add_parser("update-locator", help="Move a lead's status in the clue store")
    p_ul.add_argument("--ref-id", required=True)
    p_ul.add_argument("--status", required=True,
                      help="Live vocabulary, read from the column's own CHECK")
    p_ul.add_argument("--session", required=True)
    p_ul.add_argument("--dry-run", action="store_true")

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
    # for the four refusals and for why --status/--merged-into are deliberately absent.
    p_ap = sub.add_parser("add-parameter",
                          help="Promote an adjudicated term into base_parameters "
                               "(THE SUBJECT of a determination)")
    p_ap.add_argument("--term-id", dest="term_id", required=True,
                      help="terms.term_id — must carry a NAMES-NEW/NAMES-EXISTING adjudication")
    p_ap.add_argument("--notes")
    p_ap.add_argument("--session", required=True)
    p_ap.add_argument("--dry-run", action="store_true")

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
    p_md.add_argument("--relationship", choices=["names", "member_of", "identity_first"],
                      help="required with --identity")
    p_md.add_argument("--icf", help="axes.axis_code to cross to")
    p_md.add_argument("--role", choices=["PRIMARY", "SECONDARY", "SITUATIONAL"],
                      help="required with --icf. No ALIAS: a diagnosis is never an alias "
                           "of a functional demand (074)")
    p_md.add_argument("--mapping-confidence", dest="mapping_confidence",
                      choices=["high_predictive", "moderate", "low", "minimal"],
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
    p_ax.add_argument("--icf", help="axes.axis_code")
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
    p_amx.add_argument("--field", required=True, choices=["figure_role", "comparator"],
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
    p_ag.add_argument("--priority", required=True, choices=["P1", "P2", "P3"])
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
                      choices=["HIGH", "MODERATE", "SPECULATIVE"])
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
                      choices=["scoping", "systematic"])
    p_ls.add_argument("--session", required=True)
    p_ls.add_argument("--jurisdiction", help="omit for a search not scoped to one")
    p_ls.add_argument("--target-tier", type=int, choices=range(1, 7))
    p_ls.add_argument("--target-evidence-type",
                      choices=["clinical", "sr_meta", "standard_eb", "national_fw",
                               "code", "co1", "co2", "grey"])
    p_ls.add_argument("--target-scope",
                      choices=["intrinsic", "lower_control", "high_control",
                               "national", "international"])
    p_ls.add_argument("--terms-used",
                      help="JSON array of the aliases actually fired — the column "
                           "is json_valid-checked, and it is 0%% populated today, "
                           "so no logged search can yet show which terms it used")
    p_ls.add_argument("--mining-direction",
                      choices=["none", "backward", "forward", "both"])
    p_ls.add_argument("--results-found", type=int, default=0)
    p_ls.add_argument("--results-screened", type=int, default=0)
    p_ls.add_argument("--results-admitted", type=int, default=0)
    p_ls.add_argument("--admitted-ref-id", action="append", dest="admitted_ref_ids",
                      help="repeatable; also written to the search_admissions junction")
    p_ls.add_argument("--saturation-signal", choices=["none", "partial", "saturated"])
    p_ls.add_argument("--findings-note")
    p_ls.add_argument("--harm-finding", type=int, default=0,
                      help="R7: failure/harm/inadequacy is first-class evidence")
    p_ls.add_argument("--deferred-reason",
                      help="a search DELIBERATELY not run. This is what makes "
                           "'not looked for' different from 'nothing found'.")
    p_ls.add_argument("--backfill", type=int, default=0,
                      help="1 = reconstructed after the fact, not logged as it happened")
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
    p_ubpc.add_argument("--closure-definition-version", choices=["v1", "v2"],
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
                      help="RESOLVED | NO-MATCH | REVERTED — the set is DEFINED by "
                           "ENUM_GUARDS in scripts/emit_data_migration.py, not here")
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
                      choices=["tool", "corroborated-not-retrieved",
                               "co1-attestation", "citing-bibliography",
                               "direct-render"],
                      help="REQUIRED when --verification-status VERIFIED. How the "
                           "standing was established (D-0157).")
    p_as.add_argument("--verified-by-tool",
                      help="REQUIRED when --verification-method tool: which tool "
                           "(crossref, pubmed, semantic-scholar, ...). Invariant I4b.")
    p_as.add_argument("--verification-status",
                      choices=["VERIFIED", "UNVERIFIED"],
                      help="REQUIRED in practice. VERIFIED requires an independent connector/registry hit "
                           "(CrossRef, PubMed, Semantic Scholar, a second citing source). A source found only "
                           "in one citing document's bibliography, with no independent hit, is UNVERIFIED "
                           "with disposition OPEN, "
                           "not VERIFIED — do not upgrade it because the citing document looks authoritative.")
    p_as.add_argument("--slug", help="Link to slug (requires --local-ref-id)")
    p_as.add_argument("--local-ref-id", help="Local ref ID within slug")
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
                         choices=list(_VALID_CONFLICT_STATUS))
    p_aconf.add_argument("--resolution")
    p_aconf.add_argument("--evidence")
    p_aconf.add_argument("--gap-id")
    p_aconf.add_argument("--source-skill", default="cross-population-conflict-mapper")
    p_aconf.add_argument("--session", required=True)
    p_aconf.add_argument("--dry-run", action="store_true")

    # update-conflict
    p_uconf = sub.add_parser("update-conflict", help="Update a conflict record")
    p_uconf.add_argument("--conflict-id", required=True)
    p_uconf.add_argument("--status", choices=list(_VALID_CONFLICT_STATUS))
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
                      choices=list(_VALID_ITEM_STATUS))
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
                       choices=list(_VALID_RUN_STATUS))
    p_aar.add_argument("--dry-run", action="store_true")

    # update-audit-run
    p_uar = sub.add_parser("update-audit-run", help="Update an item_audit_runs record")
    p_uar.add_argument("--run-id", required=True)
    p_uar.add_argument("--session", required=True)
    p_uar.add_argument("--status", choices=list(_VALID_RUN_STATUS))
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
    p_asc.add_argument("--evidence-type", required=True,
                       choices=["clinical","co1","co2","sr_meta","standard_eb","national_fw","code","grey"])
    p_asc.add_argument("--outcome", required=True, choices=[
        "current_best","superseded_by","refined_by","divergent_no_supersession",
        "co1_addition_logged","pending"])
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
    p_asc.add_argument("--check-method", required=True, choices=[
        "pubmed_search","scholar_gateway","cochrane_direct","standards_body_direct",
        "multilingual_research","composite"])
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
    p_agm.add_argument("--outcome", required=True, choices=[
        "closure_evidence_found","partial_evidence_found","null_result",
        "gap_recategorized","deferred"])
    p_agm.add_argument("--discoveries", default="[]",
                       help="JSON array of FK ref_ids INSERTed this attempt")
    p_agm.add_argument("--candidate-dois", default="[]",
                       help="JSON array of DOIs of unverified candidates (PI rule #10 gate)")
    p_agm.add_argument("--check-method", required=True, choices=[
        "pubmed_cluster","scholar_gateway_lived_experience","cochrane_direct",
        "standards_body_direct","multilingual_research","composite"])
    p_agm.add_argument("--notes")
    p_agm.add_argument("--session", required=True)
    p_agm.add_argument("--dry-run", action="store_true")

    # update-gap-addressability
    p_uga = sub.add_parser("update-gap-addressability",
                            help="Set gaps.mining_addressability per DR-2026-05-26")
    p_uga.add_argument("--gap-id", required=True)
    p_uga.add_argument("--addressability", required=True, choices=[
        "ADDRESSABLE","NOT-ADDRESSABLE","TRIAGE-NEEDED"])
    p_uga.add_argument("--session", required=True)
    p_uga.add_argument("--dry-run", action="store_true")

    # unmined-gaps
    p_ung = sub.add_parser("unmined-gaps",
                            help="Query gaps eligible for gap-driven mining")
    p_ung.add_argument("--gap-id", help="Filter to a specific gap_id (returns its state)")
    p_ung.add_argument("--priority", choices=["P1","P2","P3"],
                       help="Filter to priority")
    p_ung.add_argument("--include-not-addressable", action="store_true",
                       help="Include NOT-ADDRESSABLE gaps in results (default: ADDRESSABLE only)")
    p_ung.add_argument("--include-recent", action="store_true",
                       help="Include gaps with attempt_at within last 6 months (default: skip)")

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
        _emit(result if result else {"mined": False})

    elif args.command == "log-mining":
        conns = json.loads(args.connections) if args.connections else []
        log_mining(
            slug=args.slug, ref_id=args.ref,
            direction=args.direction, connections=conns,
            session=args.session,
            dry_run=args.dry_run,
            deferred_reason=args.deferred_reason,
            status=args.mining_status,
        )
        print(json.dumps({"logged": True, "connections": len(conns),
                          "dry_run": args.dry_run}))

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
            dry_run=args.dry_run)
        _emit({"exec_id": exec_id, "slug": args.slug,
               "admitted": len(args.admitted_ref_ids or []),
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
            "notes": args.notes,
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
        }, session=args.session, dry_run=args.dry_run)
        _emit({"lead_id": lid, "dry_run": args.dry_run})

    elif args.command == "correct-source":
        ch = correct_source(args.ref_id, args.fields, session=args.session,
                            log_session=args.log_session, dry_run=args.dry_run)
        _emit({"ref_id": args.ref_id, "corrected": ch, "dry_run": args.dry_run})

    elif args.command == "amend-search":
        _emit(amend_search(args.exec_id, args.append_note, session=args.session,
                           dry_run=args.dry_run,
                           set_harm_finding=args.set_harm_finding))

    elif args.command == "resolve-candidate":
        _emit(resolve_candidate(args.candidate_id, args.disposition, args.redescription,
                                session=args.session, admitted_ref_id=args.admitted_ref_id,
                                dry_run=args.dry_run))

    elif args.command == "amend-source":
        _emit(amend_source(args.ref_id, args.field, args.replacement, args.reason,
                           session=args.session, dry_run=args.dry_run,
                           tier=args.tier))

    elif args.command == "update-locator":
        _emit(update_locator(args.ref_id, args.status, session=args.session,
                             dry_run=args.dry_run))

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

    elif args.command == "add-parameter":
        _emit(insert_parameter(
            term_id=args.term_id,
            notes=args.notes,
            session=args.session,
            dry_run=args.dry_run,
        ))

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
                                relations=_relations))

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
                "--co1-provenance is REQUIRED for --evidence-type co1. D-0178: the Co-1 "
                "warrant must NAME the co-production — which disabled people or "
                "organisation produced this work — because that co-production IS the "
                "warrant. If it genuinely cannot be evidenced from the source, the row is "
                "not Co-1; admit it at its actual tier and say why in --notes.")
        authors = (parse_author_flags(args.author) if args.author
                   else parse_author_display(args.authors))
        ref_id = insert_evidence_source(data, session=args.session,
                                        dry_run=args.dry_run, authors=authors)
        if args.slug and args.local_ref_id:
            insert_source_slug_link(ref_id, args.slug, args.local_ref_id,
                                    session=args.session, dry_run=args.dry_run)
        _emit({"ref_id": ref_id, "linked_slug": args.slug, "dry_run": args.dry_run})


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
            "session":   args.session,
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
                           authors: list[dict] | None = None) -> str:
    """Insert a new evidence source and its author rows. Returns ref_id.

    `authors` is a list of evidence_source_authors rows, from parse_author_flags or
    parse_author_display. It is written in the SAME transaction as the source, so a
    source can never exist without the authors it was filed with.
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
    with connect(dry_run) as conn:
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
            for table, extra in (
                ("evidence_sources", "AND COALESCE(superseded_by_ref_id,'') = ''"),
                ("source_locators", ""),
            ):
                dupe = conn.execute(
                    'SELECT ref_id FROM "%s" WHERE LOWER(TRIM(doi))=? AND ref_id<>? %s'
                    % (table, extra),
                    (doi, data["ref_id"])).fetchone()
                if dupe:
                    raise Refusal(
                        f"DOI {data['doi']!r} is already filed as {dupe[0]} in {table} "
                        f"(R9: cross-file the existing ref_id, never duplicate). Link "
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
_CORRECTABLE = {
    "pub_title":      lambda m: next((t for t in (m.get("title") or []) if t), None),
    "volume":         lambda m: m.get("volume"),
    "issue":          lambda m: m.get("issue"),
    "article_number": lambda m: m.get("article-number"),
    "pages":          lambda m: m.get("page"),
    "pub_year":       lambda m: (((m.get("issued") or {}).get("date-parts") or [[]])[0]
                                 or [None])[0],
}


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
                 set_harm_finding: bool = False):
    """APPEND a correction to a logged search's findings_note. Never rewrite it.

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
        row = conn.execute("SELECT exec_id, findings_note, harm_finding "
                           "FROM search_executions WHERE exec_id=?", [exec_id]).fetchone()
        if row is None:
            raise Refusal(f"exec {exec_id}: no such search execution.")
        stamp = audit(session)
        marker = f" || CORRECTED {stamp['created_at'][:10]}: "
        duplicate = note in (row["findings_note"] or "")
        if duplicate and not set_harm_finding:
            return {"exec_id": exec_id, "appended": False,
                    "reason": "this amendment is already on the row"}
        merged = row["findings_note"] or ""
        if not duplicate:
            merged = merged.rstrip() + marker + note
            conn.execute("UPDATE search_executions SET findings_note=? WHERE exec_id=?",
                         [merged, exec_id])
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
        return {"exec_id": exec_id, "appended": not duplicate, "chars": len(merged),
                "harm_finding_raised": raised}


def resolve_candidate(candidate_id: int, disposition: str, redescription: str,
                      session: str, admitted_ref_id: str = None, dry_run: bool = False):
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
    """
    redescription = (redescription or "").strip()
    if not redescription:
        raise Refusal(
            f"candidate {candidate_id}: R15 requires a re-description FROM THE SOURCE "
            f"to resolve a candidate. Refusing to close a hypothesis without one.")
    with connect(dry_run) as conn:
        row = conn.execute("SELECT candidate_id, disposition, notes, title "
                           "FROM search_candidates WHERE candidate_id=?",
                           [candidate_id]).fetchone()
        if row is None:
            raise Refusal(f"candidate {candidate_id}: no such staged candidate.")
        allowed = dbcore.check_values(conn, "search_candidates", "disposition")
        if allowed and disposition not in allowed:
            raise Refusal(
                f"candidate {candidate_id}: disposition {disposition!r} is not in the "
                f"column's own vocabulary {sorted(allowed)}.")
        if disposition == "ADMITTED" and not admitted_ref_id:
            raise Refusal(
                f"candidate {candidate_id}: ADMITTED without --admitted-ref-id names no "
                f"evidence row. Say which source it became.")
        if admitted_ref_id and not conn.execute(
                "SELECT 1 FROM evidence_sources WHERE ref_id=?", [admitted_ref_id]).fetchone():
            raise Refusal(
                f"candidate {candidate_id}: --admitted-ref-id {admitted_ref_id} is not in "
                f"evidence_sources. File the source first.")
        stamp = audit(session)
        tail = f" || RESOLVED {stamp['created_at'][:10]} (R15, re-described from the source"
        tail += f"; admitted as {admitted_ref_id}" if admitted_ref_id else ""
        tail += f"): {redescription}"
        conn.execute("UPDATE search_candidates SET disposition=?, notes=? "
                     "WHERE candidate_id=?",
                     [disposition, (row["notes"] or "").rstrip() + tail, candidate_id])
        return {"candidate_id": candidate_id, "was": row["disposition"],
                "now": disposition, "admitted_ref_id": admitted_ref_id}


# Judgement fields on evidence_sources: prose an author must WRITE, which no payload
# can supply and no verifier can prove. Deliberately disjoint from _CORRECTABLE. The
# division is the whole design: a BIBLIOGRAPHIC fact comes from the payload and this
# writer refuses to touch it; a JUDGEMENT is written by a person and can only be
# corrected by a person, with the correction recorded.
_AMENDABLE = (
    "co1_provenance", "co1_source_type", "grey_reason", "verification_note",
    "notes", "bpc_note", "scope",
    # verification_disposition belongs here and not with the bibliographic fields:
    # D-0157 states it as a JUDGEMENT -- "verification is finished or it did not
    # happen" -- which no payload can settle. Added 2026-09-02 to correct rows that
    # insert_source had written OPEN while VERIFIED, before its default was fixed.
    "verification_disposition",
)


def amend_source(ref_id: str, field: str, replacement: str, reason: str,
                 session: str, dry_run: bool = False, tier=None):
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
    if tier is not None and field != "scope":
        raise Refusal(
            f"{ref_id}: --tier is only admissible beside --field scope. The tier is "
            f"DERIVED from (evidence_type, scope) by the ratified ladder; it is never "
            f"set on its own, because a tier with no derivation input is exactly the "
            f"state B5(b) found on all nine sources and could not check.")
    new_tier = old_tier = None
    with connect(dry_run) as conn:
        row = conn.execute(f"SELECT ref_id, {field}, metadata_integrity_detail "
                           f"FROM evidence_sources WHERE ref_id=?", [ref_id]).fetchone()
        if row is None:
            raise Refusal(f"{ref_id}: no such evidence source.")
        was = row[field]
        if (was or "").strip() == replacement:
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
        ledger = (row["metadata_integrity_detail"] or "").rstrip()
        ledger += (f" || {stamp['created_at'][:10]} {field} CORRECTED ({reason}). "
                   f"Replaced text was: {was!r}")
        if new_tier is not None:
            ledger += (f" || {stamp['created_at'][:10]} tier CORRECTED {old_tier} -> "
                       f"{new_tier}, derived from (evidence_type, scope) by the "
                       f"ratified ladder in the same statement as the scope.")
        _sets, _vals = [f"{field}=?"], [replacement]
        if new_tier is not None:
            _sets.append("tier=?"); _vals.append(new_tier)
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
        return out


def update_locator(ref_id: str, status: str, session: str, dry_run: bool = False):
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
        if row["status"] == status:
            return {"ref_id": ref_id, "status": status, "changed": False}
        conn.execute("UPDATE source_locators SET status=? WHERE ref_id=?",
                     [status, ref_id])
        return {"ref_id": ref_id, "was": row["status"], "now": status, "changed": True}


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
        if "retrieval-log" not in pay.parts:
            raise Refusal(f"--icd11-payload {icd11_payload!r} REFUSED: must live under "
                          f"retrieval-log/, which is the only store a later audit can diff "
                          f"against.")
        if not pay.exists():
            raise Refusal(f"--icd11-payload {icd11_payload!r} REFUSED: file does not exist. "
                          f"icd11_verified_at is set from BYTES or not at all.")
        # READ ARCHIVE MEMBERS, NOT JUST RAW BYTES. The first version of this check
        # substring-matched `pay.read_bytes()`, and the only artefact it will ever be
        # pointed at is WHO's release file — a DEFLATE-COMPRESSED ZIP, in which no code
        # occurs literally. Measured: b"MB56" in the raw zip -> False; in the decompressed
        # member -> True. So the check refused the very payload that proves the anchor,
        # and the ruling it enforces ("verified against the persisted release file at write
        # time") was unexecutable. The MB5 verification of 2026-09-11 02:47 was done by
        # hand in Python and never through this writer, while the record claimed otherwise.
        raw = pay.read_bytes()
        bodies = [raw.decode("utf-8", errors="replace")]
        if zipfile.is_zipfile(pay):
            with zipfile.ZipFile(pay) as zf:
                for member in zf.namelist():
                    # Bounded: a release file's members are text tabulations. A member
                    # larger than 64 MiB is not what this check is for, and decompressing
                    # it blindly is how a zip becomes a denial of service.
                    info = zf.getinfo(member)
                    if info.file_size <= 64 * 1024 * 1024:
                        bodies.append(zf.read(member).decode("utf-8", errors="replace"))
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
            if not conn.execute("SELECT 1 FROM axes WHERE axis_code = ?", (icf,)).fetchone():
                near = [r[0] for r in conn.execute("SELECT axis_code FROM axes ORDER BY axis_code")]
                raise Refusal(
                    f"--icf {icf!r} REFUSED: not an axis_code. specifications.icf_code FKs to "
                    f"`axes`, NOT to raw ICF b/d/e codes (CLAUDE.md: a raw code would be refused "
                    f"by the FK). Live vocabulary: {', '.join(near)}")
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
                 "relationship": relationship, "note": note}
            c = {k: v for k, v in c.items() if v is not None}
            c.update(dbcore.stamp_for(conn, "identity_medical_map", session))
            conn.execute(f"INSERT INTO identity_medical_map ({','.join(c)}) "
                         f"VALUES ({','.join('?' * len(c))})", tuple(c.values()))
            crossings.append({"lens": "identity", "code": identity,
                              "relationship": relationship})
        if icf:
            c = {"icf_code": icf, "medical_code": code, "role": role,
                 "mapping_confidence": mapping_confidence, "note": note}
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


# The four lenses (owner 2026-08-28; CHECK relaxed to "at least one" by D-0182).
# Each column, the base registry its real FK points into, and that registry's key.
# DERIVED FROM THE SCHEMA, not a vocabulary restated in code: the registries ARE the
# vocabulary (CLAUDE.md §4). Mirrors assess_cell.LENS_COLUMNS deliberately — the
# extraction and the determination it feeds must name the lens the same way, or the
# hand-off needs a translation nobody wrote.
_LENS_COLUMNS = {
    "identity_code": ("populations", "population_code"),
    "icf_code": ("axes", "axis_code"),
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


def _relation_quote_verified(quote: str):
    """Does `quote` occur byte-for-byte in some persisted retrieval artefact?

    THE IMPORTANT REFUSAL (CLAUDE.md 5(c)). On 2026-08-19 all five sources in the
    first research batch carried invented co-author fields that read as populated
    and true to every gate that never opened the payload. `retrieval_log.py` exists
    so a claim can be checked against the bytes actually received instead of trusted
    on an operator's say-so; this is that discipline applied to a comparator quote
    instead of a bibliographic field.

    Reads BYTES off disk directly, via `retrieval_log._manifest_records()` and
    `Path.read_bytes()` -- NEVER `retrieval_log._logged_payloads()`, which parses
    JSON only and silently drops every artefact that is not JSON, XML included. The
    worked example this migration and this writer both cite -- REF-00784's PubMed
    abstract -- is exactly an `.xml` artefact; `_logged_payloads()` would report zero
    payloads for that session and the one quote this docstring can point at would
    fail its own verification.

    Searches EVERY session directory under retrieval-log/, not only the session
    that is writing this row: a quote retrieved in an earlier session (REF-00784's
    was fetched 2026-09-12, a day before this table's writer existed) is still
    genuine evidence. The manifest format carries no structured ref_id field (every
    ref_id it does carry is free text inside `purpose`), so this cannot also prove
    the artefact was fetched FOR the ref_id on this row -- that residual is named in
    the report this writer's own tests were run under, not hidden.

    CLAUDE.md §5(a): a check that passes or fails having examined nothing is a
    defect. Returns (found, detail) -- detail names the artefact on a hit, or says
    how many were actually examined on a miss.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent / "research"))
    import retrieval_log                                          # noqa: E402
    root = retrieval_log.LOG_ROOT
    if not root.exists():
        return False, f"EXAMINED: 0 -- {root}/ does not exist"
    needle = quote.encode("utf-8")
    examined = 0
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        for rec in retrieval_log._manifest_records(d.name):
            art = d / rec.get("artefact", "")
            if not art.exists():
                continue
            examined += 1
            if needle in art.read_bytes():
                return True, f"{d.name}/{rec['artefact']}"
    return False, f"EXAMINED: {examined} persisted artefact(s) under {root}/*/"


def _write_relation_edge(conn, *, from_id: int, from_ref_id: str,
                         from_figure_role, from_comparator,
                         relation: str, session: str, context: str,
                         to_extraction: int = None, to_label: str = None,
                         to_kind: str = None, stated: str = None, quote: str = None,
                         input_role: str = None, notes: str = None,
                         cross_source_reason: str = None) -> int:
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

    verified, where = _relation_quote_verified(quote)
    if not verified:
        raise Refusal(
            f"{context}: --quote does not occur byte-for-byte in any persisted "
            f"retrieval artefact ({where}). Either the payload behind this quote "
            f"was never retrieved and persisted (R10 -- retrieve it first, "
            f"retrieval_log.fetch()), or the quote was typed from memory rather "
            f"than read off the bytes (CLAUDE.md 5(c)). Nothing was written.")

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
                      relations: list = None):
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
                f"Extract under one of those. Admission to a FURTHER slug happens at "
                f"admission time (`db.py add-source --ref-id ... --slug SLUG "
                f"--local-ref-id ...`); there is no CLI verb that links an "
                f"already-admitted source to a second slug today, and inventing the "
                f"link from here would make this writer the thing that decides what a "
                f"source was admitted for.")

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
                conn, from_id=extraction_id, from_ref_id=ref,
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
_AMENDABLE_SVE_FIELDS = frozenset({"figure_role", "comparator"})


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
        row = conn.execute(
            "SELECT extraction_id, ref_id, figure_role, comparator, claim_type, "
            "notes FROM source_value_extractions WHERE extraction_id=?",
            (extraction_id,)).fetchone()
        if row is None:
            raise Refusal(f"amend-extraction: extraction_id {extraction_id}: no "
                          f"such row.")
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
            return {"extraction_id": extraction_id, "field": field, "changed": False,
                    "reason": "already this value", "dry_run": dry_run}

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


def insert_source_slug_link(ref_id: str, slug: str, local_ref_id: str,
                             session: str, dry_run: bool = False):
    """Link an evidence source to a slug with a local ref ID."""
    with connect(dry_run) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO source_slug_links "
            "(ref_id, slug, local_ref_id, created_at, created_by_session, "
            "updated_at, updated_by_session) VALUES (?,?,?,?,?,?,?)",
            [ref_id, slug, local_ref_id,
             *audit(session).values()]
        )


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
            AND (cm.global_ref_id IS NULL OR cm.backward = 0 OR cm.forward = 0)
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
    (slug, local_ref_id, checked_at) so repeat calls in the same session don't collide.
    """
    import hashlib
    from datetime import datetime, timezone
    checked_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    seed = f"{slug}|{local_ref_id}|{checked_at}|{session}"
    check_id = "SUPCHK-" + hashlib.sha256(seed.encode()).hexdigest()[:12]
    with connect(dry_run) as conn:
        conn.execute("""
            INSERT INTO supersession_check (
                check_id, slug, local_ref_id, ref_id,
                anchor_tier, anchor_evidence_type,
                outcome, superseding_ref_ids, superseding_dois,
                refinement_dimension, divergence_notes,
                search_strategy_record, candidates_returned, candidates_reviewed,
                checked_at, checked_by_session, check_method, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            check_id, slug, local_ref_id, ref_id,
            anchor_tier, anchor_evidence_type,
            outcome,
            json.dumps(superseding_ref_ids) if superseding_ref_ids else None,
            json.dumps(superseding_dois) if superseding_dois else None,
            refinement_dimension, divergence_notes,
            search_strategy_record, candidates_returned, candidates_reviewed,
            checked_at, session, check_method, notes,
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
    gap_id are allowed; the most recent row (MAX(attempt_at)) is the operative
    outcome.
    """
    from datetime import datetime, timezone
    attempt_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with connect(dry_run) as conn:
        cur = conn.execute("""
            INSERT INTO gap_mining (
                gap_id, attempt_at, attempted_by_session,
                search_strategy_record, candidates_returned, candidates_reviewed,
                outcome, discoveries_logged, candidate_dois,
                check_method, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            gap_id, attempt_at, session,
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
    recent attempt_at is older than 6 months (per re-eligibility rules in
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
               latest.attempt_at AS latest_attempt_at,
               latest.outcome    AS latest_outcome
          FROM gaps g
          LEFT JOIN (
              SELECT gm.gap_id, gm.attempt_at, gm.outcome
                FROM gap_mining gm
                JOIN (
                    SELECT gap_id, MAX(attempt_at) AS max_at
                      FROM gap_mining
                     GROUP BY gap_id
                ) m ON m.gap_id = gm.gap_id AND m.max_at = gm.attempt_at
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


def insert_search_candidate(data: dict, session: str, dry_run: bool = False) -> str:
    """Stage a screened-but-not-admitted candidate (research stage)."""
    _COLS = frozenset({
        "candidate_id", "exec_id", "found_under_slug", "suggested_slug", "disposition",
        "title", "locator", "locator_status", "tier_guess", "harm_finding",
        "why_not_admitted", "notes",
    })
    dbcore.validate_cols(data.keys(), _COLS, "insert_search_candidate")
    with dbcore.connect(dry_run) as conn:
        if data.get("exec_id") is not None and not dbcore.exists(
                conn, "search_executions", "exec_id", data["exec_id"]):
            raise Refusal(
                f"exec_id {data['exec_id']!r} is not a live search_executions row. "
                f"A candidate is something a SEARCH surfaced; log the search first "
                f"(db.py log-search), then stage what it found.")
        if not dbcore.exists(conn, "slugs", "slug", data.get("found_under_slug")):
            raise Refusal(
                f"found_under_slug {data.get('found_under_slug')!r} is not in `slugs`.")
        if data.get("suggested_slug") and not dbcore.exists(
                conn, "slugs", "slug", data["suggested_slug"]):
            raise Refusal(f"suggested_slug {data['suggested_slug']!r} is not in `slugs`.")
        dbcore.check_vocab(conn, "search_candidates", "disposition",
                           data.get("disposition"), "insert_search_candidate")
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
        row["session"] = session
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


def insert_code_lead(data: dict, session: str, dry_run: bool = False) -> int:
    """Write a code/standard lead into the research-stage lead store.

    Deliberately NOT a DOI-bearing writer. research_code_leads has no doi column
    (migration 066): a standard is retrieved by clause reference, and letting the two
    identifier shapes share a row format is what put 24 rows in source_locators
    carrying both a standard_number and a DOI.
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
    with dbcore.connect(dry_run) as conn:
        dbcore.check_vocab(conn, "research_code_leads", "status", data.get("status"),
                           "insert_code_lead")
        # THE DEDUP REFUSAL. 109 archived rows were 83 leads because the same standard was
        # restated once per item. The UNIQUE constraint makes that impossible; this turns
        # it into a sentence naming the row that already holds it.
        hit = conn.execute(
            "SELECT lead_id FROM research_code_leads WHERE jurisdiction=? AND standard_name=?",
            (jur, std)).fetchone()
        if hit:
            raise Refusal(
                f"{jur} / {std!r} is already held as lead_id {hit[0]}. A code lead is keyed "
                f"on (jurisdiction, standard_name) — restating it is the duplication the "
                f"item-keyed shape produced. Update that row instead.")
        now = dbcore.now()
        cur = conn.execute(
            "INSERT INTO research_code_leads (jurisdiction, standard_name, clause, status, "
            "recovered_from, notes, created_at, created_by_session) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (jur, std, data.get("clause"), data.get("status") or "REFERENCE-ONLY",
             data.get("recovered_from"), data.get("notes"), now, session))
        return cur.lastrowid


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
                        f"R9: cross-file the existing ref_id, never mint a second identity "
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

