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
    python3 scripts/db.py upsert-coverage --slug SLUG --jurisdiction AU --session SESSION
    python3 scripts/db.py upsert-language --slug SLUG --language FR --results-count 4 --session SESSION
    python3 scripts/db.py update-bpc --slug SLUG --citation-mining-complete 1 --session SESSION
    python3 scripts/db.py add-source --ref-id REF-001 --authors "Smith J" --year 2022 --title "..." --tier 1 --session SESSION [--slug SLUG --local-ref-id LR-001]
    python3 scripts/db.py validate
    python3 scripts/db.py --help
"""

import json
import os
import sqlite3
import sys
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))

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


@contextmanager
def connect(dry_run: bool = False):
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        if not dry_run:
            conn.commit()
        else:
            conn.rollback()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


def audit(session: str) -> dict:
    ts = now()
    return {
        "created_at": ts, "created_by_session": session,
        "updated_at": ts, "updated_by_session": session,
    }


def _upd(session: str) -> dict:
    return {"updated_at": now(), "updated_by_session": session}


def _validate_cols(data_keys, whitelist: frozenset, context: str):
    unknown = set(data_keys) - whitelist
    if unknown:
        raise ValueError(
            f"{context}: unknown column(s) {unknown}. "
            f"Permitted: {whitelist}"
        )


def _emit(data):
    """Print JSON to stdout."""
    print(json.dumps(data, indent=2, default=str))


# --- Storage layer (CRUD) ---


def next_con_id() -> str:
    with connect() as conn:
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
    with connect() as conn:
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
    with connect() as conn:
        row = conn.execute(
            "SELECT backward, forward, connections_produced "
            "FROM citation_mining WHERE slug=? AND local_ref_id=?",
            [slug, ref_id]
        ).fetchone()
    return dict(row) if row else None


def log_mining(slug: str, ref_id: str, direction: str,
               connections: list[str], session: str,
               doi: str = None, dry_run: bool = False):
    if direction not in _VALID_DIRECTIONS:
        raise ValueError(
            f"direction must be 'backward' or 'forward', got '{direction}'"
        )
    dir_col = direction
    ts = now()

    with connect(dry_run) as conn:
        row = conn.execute(
            "SELECT backward, forward, connections_produced "
            "FROM citation_mining WHERE slug=? AND local_ref_id=?",
            [slug, ref_id]
        ).fetchone()
        if row:
            prior = json.loads(row["connections_produced"] or "[]")
            merged = json.dumps(list(dict.fromkeys(prior + connections)))
            conn.execute(
                f"UPDATE citation_mining SET {dir_col}=1, "
                "connections_produced=?, updated_at=?, updated_by_session=? "
                "WHERE slug=? AND local_ref_id=?",
                [merged, ts, session, slug, ref_id]
            )
        else:
            conn.execute(
                "INSERT INTO citation_mining "
                "(slug,local_ref_id,doi,backward,forward,"
                " connections_produced,created_at,created_by_session,"
                " updated_at,updated_by_session) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                [slug, ref_id, doi,
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
        "admitted_ref_ids": json.dumps(admitted_ref_ids) if admitted_ref_ids else None,
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
        # BOTH carriers, in one transaction. admitted_ref_ids (JSON, on the row)
        # and search_admissions (the junction) hold the same fact, and checks
        # H03/H04 assert they agree in both directions. Writing one without the
        # other is a guaranteed check failure — and worse, a silent disagreement
        # about which sources a search actually produced, at the seam where the
        # research phase hands off to collection.
        for ref_id in (admitted_ref_ids or []):
            conn.execute(
                "INSERT OR IGNORE INTO search_admissions "
                "(exec_id, ref_id, created_at, created_by_session) "
                "VALUES (?, ?, ?, ?)", [exec_id, ref_id, ts, session])
        return exec_id


def next_term_id() -> str:
    with connect() as conn:
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
    with connect() as conn:
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
        with connect() as conn:
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
    with connect() as conn:
        return [dict(r) for r in conn.execute(q, params).fetchall()]


def get_unmined_sources(slug: str) -> list[dict]:
    with connect() as conn:
        rows = conn.execute("""
            SELECT ssl.local_ref_id,
                   es.doi, es.pub_title,
                   COALESCE(cm.backward, 0) AS backward,
                   COALESCE(cm.forward,  0) AS forward
            FROM source_slug_links ssl
            JOIN evidence_sources es ON ssl.ref_id = es.ref_id
            LEFT JOIN citation_mining cm
                ON cm.slug=ssl.slug AND cm.local_ref_id=ssl.local_ref_id
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
    with connect() as conn:
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
    return {
        "slug": slug,
        "jurisdictions_searched": jur,
        "jurisdictions_required": 24,
        "languages_searched": lang,
        "languages_required": 14,
        "searches_deferred_with_reason": deferred,
        "complete": jur >= 24 and lang >= 14,
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
    with connect() as conn:
        return [dict(r) for r in conn.execute(q, params).fetchall()]


# ── CO-0009 Phase 1 Session 1b additions ──────────────────────────────────

import re as _re

_VALID_CONFLICT_STATUS = frozenset({
    "RESOLVED-EVIDENCE", "RESOLVED-CONSENSUS",
    "RESOLUTION-PROPOSED", "UNRESOLVED", "MODE-S-ONLY",
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
    with connect() as conn:
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
    with connect() as conn:
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
    with connect() as conn:
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
    with connect() as conn:
        return [dict(r) for r in conn.execute(q, params).fetchall()]


# --- CLI ---


def main():
    parser = argparse.ArgumentParser(
        description="Guidebook SQLite data layer CLI"
    )
    sub = parser.add_subparsers(dest="command")

    # init
    p_init = sub.add_parser("init", help="Initialize database")
    p_init.add_argument("--force", action="store_true")

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
    p_logm.add_argument("--doi")
    p_logm.add_argument("--dry-run", action="store_true")

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
    p_as.add_argument("--authors", required=True)
    p_as.add_argument("--year", required=True, type=int)
    p_as.add_argument("--title", required=True)
    p_as.add_argument("--tier", required=True, type=int)
    p_as.add_argument("--doi")
    p_as.add_argument("--pmid")
    p_as.add_argument("--jurisdiction")
    p_as.add_argument("--evidence-type")
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

    # validate
    sub.add_parser("validate", help="Run DB validation checks")

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
    # one column; it was replaced by the `item_population_links` junction and
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

    if args.command == "init":
        import subprocess
        cmd = [sys.executable, str(Path(__file__).parent / "init_db.py")]
        if args.force:
            cmd.append("--force")
        sys.exit(subprocess.call(cmd))

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
            session=args.session, doi=args.doi,
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

    elif args.command == "add-source":
        data = {
            "ref_id": args.ref_id,
            "authors": args.authors,
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
        ref_id = insert_evidence_source(data, session=args.session, dry_run=args.dry_run)
        if args.slug and args.local_ref_id:
            insert_source_slug_link(ref_id, args.slug, args.local_ref_id,
                                    session=args.session, dry_run=args.dry_run)
        _emit({"ref_id": ref_id, "linked_slug": args.slug, "dry_run": args.dry_run})

    elif args.command == "validate":
        import subprocess
        sys.exit(subprocess.call(
            [sys.executable, str(Path(__file__).parent / "validate_db.py")]
        ))

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
                "item_population_links junction.\n"
                "Populations attach to an item as one row per (item_code, "
                "population_code), carrying subtype, applicability and rationale_ref "
                "— none of which a CSV could hold.\n"
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


def insert_evidence_source(data: dict, session: str,
                           dry_run: bool = False) -> str:
    """Insert a new evidence source. Returns ref_id."""
    # Map legacy logical field names to the real evidence_sources columns and drop
    # doi_less_key (no such column in the current schema). Without this the CLI crashed
    # with "table evidence_sources has no column named authors" (audit F-17, 2026-06-22).
    _LEGACY = {"authors": "author_display", "year": "pub_year", "title": "pub_title"}
    data = {_LEGACY.get(k, k): v for k, v in data.items() if k != "doi_less_key"}
    _ES_COLS = frozenset({
        "ref_id", "author_display", "pub_year", "pub_title", "doi",
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
        "verification_note",
    })
    _validate_cols(data.keys(), _ES_COLS, "insert_evidence_source")

    # A verification standing implies its evidence. Fill what the caller left out
    # rather than writing a row the blocking invariants reject.
    vs = data.get("verification_status")
    if vs == "VERIFIED":
        data.setdefault("verification_method", "tool")
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
    return data["ref_id"]


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
    with connect() as conn:
        rows = conn.execute("""
            SELECT ssl.local_ref_id, ssl.slug,
                   es.doi, es.tier, es.pub_title AS title,
                   COALESCE(es.lang_detected, es.language) AS lang,
                   COALESCE(cm.backward, 0) AS backward,
                   COALESCE(cm.forward, 0) AS forward
            FROM source_slug_links ssl
            JOIN evidence_sources es ON ssl.ref_id = es.ref_id
            LEFT JOIN citation_mining cm
                ON cm.slug = ssl.slug AND cm.local_ref_id = ssl.local_ref_id
            WHERE es.tier <= ?
            AND (cm.local_ref_id IS NULL OR cm.backward = 0 OR cm.forward = 0)
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
    with connect() as conn:
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


if __name__ == "__main__":
    main()
