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
    python3 scripts/db.py next-id connections|gaps|terms
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
import dbcore                                                      # noqa: E402

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
        raise ValueError(f"status must start with CLOSED, got '{status}'")
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
        raise ValueError(f"Invalid priority: {priority}")
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
               dry_run: bool = False):
    """Record a mining pass. Keyed on the global ref_id.

    The `doi` parameter was REMOVED 2026-08-24. It wrote a copy of a value that
    is reachable through global_ref_id, and 2 of 10 rows had already drifted by
    case. Accepting it while ignoring it would have been worse than either
    keeping or dropping it: a caller would believe a DOI had been recorded.
    """
    if direction not in _VALID_DIRECTIONS:
        raise ValueError(
            f"direction must be 'backward' or 'forward', got '{direction}'"
        )
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


class FrozenGridError(RuntimeError):
    """Raised on any attempt to write a legacy coverage grid. See _FROZEN_MSG."""


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
               harm_finding: int = 0, dry_run: bool = False) -> int:
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
    ids = list(admitted_ref_ids or [])
    if len(set(ids)) != len(ids):
        dupes = sorted({r for r in ids if ids.count(r) > 1})
        raise ValueError(
            f"--admitted-ref-id repeated: {', '.join(dupes)}. One admission edge "
            f"per (search, source); a repeat is a miscount, not two admissions "
            f"(invariant H07).")
    if ids and results_admitted and results_admitted != len(ids):
        raise ValueError(
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
                raise ValueError(
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
        raise ValueError(f"Invalid conflict status: {data.get('status')}")
    if data.get("pop_a") and data.get("pop_b"):
        if data["pop_a"] > data["pop_b"]:
            raise ValueError(
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
        raise ValueError(f"Invalid conflict status: {status}")
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


def insert_item(data: dict, session: str, dry_run: bool = False) -> str:
    if not _ITEM_CODE_RE.match(data.get("item_code", "")):
        raise ValueError(f"item_code must match [A-K]-NN[a-z]?, got: '{data.get('item_code')}'")
    if not _CATEGORY_RE.match(data.get("category", "")):
        raise ValueError(f"category must be single letter A-K, got: '{data.get('category')}'")
    if data.get("status") and data["status"] not in _VALID_ITEM_STATUS:
        raise ValueError(f"Invalid item status: {data.get('status')}")
    row = {**data, **audit(session)}
    with connect(dry_run) as conn:
        cols = ", ".join(row)
        ph   = ", ".join(["?"] * len(row))
        conn.execute(f"INSERT INTO items ({cols}) VALUES ({ph})", list(row.values()))
    return data["item_code"]


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
        raise ValueError(f"Invalid audit run status: {data.get('status')}")
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
        raise ValueError(f"Invalid audit run status: {status}")
    # Validate step names
    for step_list in [steps_complete or [], steps_started or []]:
        unknown = [s for s in step_list if s not in _PIPELINE_STEPS]
        if unknown:
            raise ValueError(f"Unknown pipeline step(s): {unknown}. Valid: {sorted(_PIPELINE_STEPS)}")
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
    p_logm.add_argument("--connections", required=True,
                        help="JSON array of CON-IDs")
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
    p_am.add_argument("--session", required=True)
    p_am.add_argument("--dry-run", action="store_true")

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
                       choices=["connections", "gaps", "terms", "conflicts"])

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
                      choices=["tool", "corroborated-not-retrieved",
                               "co1-attestation", "citing-bibliography"],
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

    # add-item
    p_ai = sub.add_parser("add-item", help="Insert an item record")
    p_ai.add_argument("--item-code", required=True)
    p_ai.add_argument("--category", required=True)
    p_ai.add_argument("--name", required=True)
    # RETIRED. `items.applicable_groups` was a CSV of population codes packed into  # [RETIRED-VOCAB-OK]
    # one column; it was replaced by the item×taxonomy junction (today
    # `item_taxonomy_links`) and
    # dropped from the schema. The flag is kept rather than deleted so the failure
    # says where populations went — insert_item builds its INSERT from the dict
    # keys, so passing this used to produce a bare `no such column` from SQLite.
    p_ai.add_argument("--applicable-groups",
                      help=argparse.SUPPRESS)   # [RETIRED-VOCAB-OK]
    p_ai.add_argument("--bpc-source-slug")
    p_ai.add_argument("--status", default="draft",
                      choices=list(_VALID_ITEM_STATUS))
    p_ai.add_argument("--item-id")
    p_ai.add_argument("--session", required=True)
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
        conns = json.loads(args.connections)
        log_mining(
            slug=args.slug, ref_id=args.ref,
            direction=args.direction, connections=conns,
            session=args.session,
            dry_run=args.dry_run
        )
        print(json.dumps({"logged": True, "dry_run": args.dry_run}))

    elif args.command == "next-id":
        id_funcs = {
            "connections": next_con_id,
            "gaps":        next_gap_id,
            "terms":       next_term_id,
            "conflicts":   next_conf_id,
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
                             "synthesis_attribution_required")):
            _v = getattr(args, _flag, None)
            # `is not None`, not truthiness: synthesis_attribution_required is an int flag
            # and 0 is a real, meaningful value that `if _v` would discard.
            if _v is not None:
                data[_col] = _v
        # THE CO-1 WARRANT REFUSAL (D-0178, ratified 2026-08-31). A Co-1 admission whose
        # warrant is not stated is "unwarranted-pending", and Co-1 is co-primary with T1
        # under CRPD Art 4.3 — this is the tier where the claim rests entirely on disabled
        # people having produced the work. CLAUDE.md §6: "Erasing them while claiming the
        # tier is the worst failure available here." On 2026-09-01 two Co-1 rows were
        # written with co1_provenance NULL because the CLI could not say it; nothing
        # refused them. Now something does.
        if (args.evidence_type or "").lower() == "co1" and not args.co1_provenance:
            raise ValueError(
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
        data = {
            "item_code": args.item_code,
            "category":  args.category,
            "name":      args.name,
            "status":    args.status,
        }
        if args.applicable_groups:                          # [RETIRED-VOCAB-OK]
            raise SystemExit(
                "--applicable-groups is retired: items.applicable_groups was dropped "  # [RETIRED-VOCAB-OK]
                "from the schema when the packed CSV column was replaced by the "
                "item_taxonomy_links junction.\n"
                "Populations attach to an item as one row per (item_code, "
                "identity_code), carrying subtype, applicability and rationale_ref "
                "— none of which a CSV could hold. Since migration 065 that same row "
                "may also carry icf_code, needs_code and medical_code, so one fact "
                "can state several lenses at once.\n"
                "Create the item first, then add the links via a data migration "
                "(scripts/emit_data_migration.py); the canonical DB takes writes only "
                "through migrations (CLAUDE.md §0 rule 4)."
            )
        if args.bpc_source_slug:   data["bpc_source_slug"]   = args.bpc_source_slug
        if args.item_id:           data["item_id"]           = args.item_id
        insert_item(data, session=args.session, dry_run=args.dry_run)
        _emit({"item_code": args.item_code, "dry_run": args.dry_run})

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
                raise ValueError("--discoveries must be a JSON array")
        except (json.JSONDecodeError, ValueError) as e:
            print(json.dumps({"error": f"--discoveries: {e}"}))
            sys.exit(2)
        try:
            cand_dois = json.loads(args.candidate_dois) if args.candidate_dois else []
            if not isinstance(cand_dois, list):
                raise ValueError("--candidate-dois must be a JSON array")
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
            raise ValueError("--author was given an empty value")
        if "|" in part:
            head, tail = part.split("|", 1)
        else:
            head, tail = part, ""
        head, tail = head.strip(), tail.strip()
        if head.lower() in ("corp", "corporate"):
            if not tail:
                raise ValueError(f"--author {raw!r}: corporate author has no name")
            out.append({"position": i, "is_corporate": 1, "corporate_name": tail,
                        "last_name": None, "first_name": None})
        else:
            if not head:
                raise ValueError(f"--author {raw!r}: no surname. Give 'Last|Given'.")
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
        raise ValueError("--authors is empty")
    for i, part in enumerate(parts, start=1):
        m = _DISPLAY_PART.match(part)
        if m:
            rows.append({"position": i, "is_corporate": 0, "corporate_name": None,
                         "last_name": m.group("last").strip(),
                         "first_name": m.group("initials").strip()})
        else:
            bad.append(part)
    if bad:
        raise ValueError(
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
        raise ValueError(
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
    })
    _validate_cols(data.keys(), _ES_COLS, "insert_evidence_source")

    # THE REF_ID MUST BE A GLOBAL REFERENCE ID, and nothing else enforced that.
    # `evidence_sources.ref_id` is a bare TEXT PRIMARY KEY with no CHECK, so
    # `add-source --ref-id RAP-04` inserted silently — and until 2026-08-24 the two
    # skills that document this call told sessions to do exactly that, both writing
    # `--ref-id {local_ref_id}` beside `--local-ref-id {local_ref_id}`.
    #
    # What that costs: a source filed under a per-slug label is invisible to the
    # source_locators high-water mark that ref_ids are minted above, collides with the
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
        raise ValueError(
            f"--ref-id {rid!r} is not a global reference id.{hint} Expected REF-NNNNN "
            f"(or REF-VERIFIED-NNN / Co1-NN). There is no allocator: mint above the "
            f"source_locators high-water mark, or you will collide with a held "
            f"identifier (CLAUDE.md §4). Nothing was written.")

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
            raise ValueError(
                "VERIFIED requires --verification-method (how it was established: "
                "tool / corroborated-not-retrieved / co1-attestation / "
                "citing-bibliography). D-0157: a standing without its method is "
                "not a standing. Filing it as UNVERIFIED with disposition OPEN is "
                "the honest move if you have not established it.")
        if data["verification_method"] == "tool" and not data.get("verified_by_tool"):
            raise ValueError(
                "verification_method='tool' requires --verified-by-tool naming "
                "which tool established it (invariant I4b).")
        data.setdefault("verification_attempt_count", 1)
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
            raise ValueError(
                f"{data['ref_id']} already exists. R9: cross-file the existing "
                f"ref_id rather than duplicating. To amend it, ship a migration.")
        if data.get("doi"):
            dupe = conn.execute(
                "SELECT ref_id FROM evidence_sources WHERE doi = ? "
                "AND COALESCE(superseded_by_ref_id,'') = ''", [data["doi"]]).fetchone()
            if dupe:
                raise ValueError(
                    f"DOI {data['doi']} is already filed as {dupe[0]} (R9: "
                    f"pre-check the DOI, cross-file rather than duplicate). "
                    f"Link that ref_id to your slug instead.")
        cols = ", ".join(row)
        ph = ", ".join(["?"] * len(row))
        conn.execute(
            f"INSERT INTO evidence_sources ({cols}) VALUES ({ph})",
            list(row.values())
        )
        # A source with no authors renders as a blank byline everywhere, and the
        # display column that used to paper over that is gone. Refuse the write.
        if not authors:
            raise ValueError(
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
        raise ValueError(
            f"{ref_id}: no retrieval log for session {log_session!r}. A correction is "
            f"only as good as the bytes behind it; re-retrieve first (R10).")
    msg = retrieval_log._index_by_doi(payloads).get((doi or "").lower())
    if msg is None:
        raise ValueError(
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
        raise ValueError(
            f"{ref_id}: cannot correct {', '.join(unknown)} — this writer rewrites only "
            f"fields retrieval_log --verify-authors can prove: "
            f"{', '.join(sorted(_CORRECTABLE))}, authors.")
    with connect(dry_run) as conn:
        row = conn.execute(
            "SELECT ref_id, doi FROM evidence_sources WHERE ref_id=?", [ref_id]).fetchone()
        if row is None:
            raise ValueError(f"{ref_id}: no such evidence source.")
        if not row["doi"]:
            raise ValueError(
                f"{ref_id}: no DOI, so no payload can be keyed to it. Corrections to a "
                f"DOI-less source have no byte-level authority and are refused here.")
        msg = _payload_for(ref_id, row["doi"], log_session)
        stamp = audit(session)
        changed = []

        for f in [x for x in fields if x != "authors"]:
            want = _CORRECTABLE[f](msg)
            if want in (None, ""):
                raise ValueError(
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
                raise ValueError(
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


def amend_search(exec_id: int, note: str, session: str, dry_run: bool = False):
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
        raise ValueError(f"exec {exec_id}: refusing to append an empty amendment.")
    with connect(dry_run) as conn:
        row = conn.execute("SELECT exec_id, findings_note FROM search_executions "
                           "WHERE exec_id=?", [exec_id]).fetchone()
        if row is None:
            raise ValueError(f"exec {exec_id}: no such search execution.")
        stamp = audit(session)
        marker = f" || CORRECTED {stamp['created_at'][:10]}: "
        if note in (row["findings_note"] or ""):
            return {"exec_id": exec_id, "appended": False,
                    "reason": "this amendment is already on the row"}
        merged = (row["findings_note"] or "").rstrip() + marker + note
        conn.execute("UPDATE search_executions SET findings_note=? WHERE exec_id=?",
                     [merged, exec_id])
        return {"exec_id": exec_id, "appended": True, "chars": len(merged)}


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
        raise ValueError(f"Invalid addressability: {addressability}")
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
            raise ValueError(
                f"exec_id {data['exec_id']!r} is not a live search_executions row. "
                f"A candidate is something a SEARCH surfaced; log the search first "
                f"(db.py log-search), then stage what it found.")
        if not dbcore.exists(conn, "slugs", "slug", data.get("found_under_slug")):
            raise ValueError(
                f"found_under_slug {data.get('found_under_slug')!r} is not in `slugs`.")
        if data.get("suggested_slug") and not dbcore.exists(
                conn, "slugs", "slug", data["suggested_slug"]):
            raise ValueError(f"suggested_slug {data['suggested_slug']!r} is not in `slugs`.")
        dbcore.check_vocab(conn, "search_candidates", "disposition",
                           data.get("disposition"), "insert_search_candidate")
        if data.get("locator_status") is not None:
            dbcore.check_vocab(conn, "search_candidates", "locator_status",
                               data["locator_status"], "insert_search_candidate")
        # R15: a staged description is a HYPOTHESIS. ADMITTED without a resolved
        # locator is the shape that lets a guess harden into a fact.
        if data.get("disposition") == "ADMITTED" and data.get("locator_status") != "RESOLVED":
            raise ValueError(
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
            raise ValueError(
                f"ref_id {data.get('ref_id')!r} is not an admitted source. Grade the "
                f"match AFTER admission -- a match row for a source that does not exist "
                f"is a claim about nothing.")
        if not dbcore.exists(conn, "populations", "population_code", data.get("target_population")):
            raise ValueError(
                f"target_population {data.get('target_population')!r} is not in `populations`.")
        dbcore.check_vocab(conn, "evidence_population_match", "match_grade",
                           data.get("match_grade"), "insert_population_match")
        if data.get("match_grade") == "MISMATCH" and not (data.get("mismatch_note") or "").strip():
            raise ValueError(
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
            row["match_id"] = f"{session[:24]}-{ref}-{data['target_population']}"
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
            raise ValueError(f"item_code {data.get('item_code')!r} is not in `items`.")
        tier = data.get("evidence_tier")
        # RANGE_GUARDS in scripts/emit_data_migration.py owns the 1-6 band and cites
        # schemas/evidence_source.py:85 as its authority. Not restated here (rule 5) --
        # the same band is asserted, and the guard remains the place it is DEFINED.
        if tier is None or not (1 <= int(tier) <= 6):
            raise ValueError(
                f"evidence_tier {tier!r} is outside the ratified 1-6 band "
                f"(RANGE_GUARDS in emit_data_migration.py; governance/tier-system.md).")
        # R3: a quantified value needs a locator or an explicit unverified marker.
        loc_fields = [k for k in _COLS if k.startswith("loc_")] + ["source_section"]
        has_locator = any((data.get(k) or "").strip() for k in loc_fields
                          if isinstance(data.get(k), str))
        if data.get("value_numeric") is not None:
            if not data.get("unit"):
                raise ValueError("--value-numeric requires --unit. A number without a "
                                 "unit is not a value.")
            if not has_locator and "[UNVERIFIED-QUANT]" not in (data.get("notes") or ""):
                raise ValueError(
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
            raise ValueError(f"ref_id {data.get('ref_id')!r} is not an admitted source.")
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
                raise ValueError(
                    f"--ref-id was given, so {restated} are reachable through it and must "
                    f"not be copied onto this row (CLAUDE.md rule 5: point, do not copy). "
                    f"Omit them; a reader follows ref_id to evidence_sources.")
            row_source = data.get("source") or ref
        else:
            if not (data.get("source") or "").strip():
                raise ValueError(
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
            raise ValueError(f"slug {data.get('slug')!r} is not in `slugs`.")
        if dbcore.exists(conn, "case_studies", "case_study_id", data.get("case_study_id")):
            raise ValueError(f"case_study_id {data.get('case_study_id')!r} already exists.")
        # `sources` is prose where a junction to evidence_sources.ref_id is the ruling's
        # exact target ("for rendering a citation, we point towards the evidence table").
        # The table is empty, so refuse the copy shape now rather than migrate later:
        # a REF-NNNNN inside the prose field means a pointer was flattened into text.
        if dbcore.REF_ID_SHAPE.search(data.get("sources") or ""):
            raise ValueError(
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
        raise ValueError("--jurisdiction is required and may not be blank: a lead that "
                         "cannot say which jurisdiction it belongs to is not retrievable, "
                         "which is the only purpose this row has.")
    if not std:
        raise ValueError("--standard-name is required and may not be blank.")
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
            raise ValueError(
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
        raise ValueError(
            f"--ref-id {data.get('ref_id')!r} is not a global reference id. Expected "
            f"REF-NNNNN (or REF-VERIFIED-NNN / Co1-NN). Mint with dbcore.next_ref_id().")
    with dbcore.connect(dry_run) as conn:
        if dbcore.exists(conn, "source_locators", "ref_id", ref):
            raise ValueError(f"{ref} already exists in source_locators. Use update-locator.")
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
                    raise ValueError(
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
    main()

