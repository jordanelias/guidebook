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
    "citation_mining_complete"
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


def upsert_search_coverage(slug: str, jurisdiction: str,
                           data: dict, session: str,
                           dry_run: bool = False):
    _validate_cols(data.keys(), _COVERAGE_COLS, "upsert_search_coverage")
    ts = now()
    with connect(dry_run) as conn:
        exists = conn.execute(
            "SELECT 1 FROM search_coverage WHERE slug=? AND jurisdiction=?",
            [slug, jurisdiction]
        ).fetchone()
        if exists:
            sets = ", ".join(f"{k}=?" for k in data)
            conn.execute(
                f"UPDATE search_coverage SET {sets}, "
                "updated_at=?, updated_by_session=? "
                "WHERE slug=? AND jurisdiction=?",
                [*data.values(), ts, session, slug, jurisdiction]
            )
        else:
            row = {"slug": slug, "jurisdiction": jurisdiction,
                   **data, **audit(session)}
            cols = ", ".join(row)
            ph = ", ".join(["?"] * len(row))
            conn.execute(
                f"INSERT INTO search_coverage ({cols}) VALUES ({ph})",
                list(row.values())
            )


def upsert_search_language(slug: str, language: str,
                           data: dict, session: str,
                           dry_run: bool = False):
    _validate_cols(data.keys(), _LANGUAGE_COLS, "upsert_search_language")
    ts = now()
    with connect(dry_run) as conn:
        exists = conn.execute(
            "SELECT 1 FROM search_languages WHERE slug=? AND language=?",
            [slug, language]
        ).fetchone()
        if exists:
            sets = ", ".join(f"{k}=?" for k in data)
            conn.execute(
                f"UPDATE search_languages SET {sets}, "
                "updated_at=?, updated_by_session=? "
                "WHERE slug=? AND language=?",
                [*data.values(), ts, session, slug, language]
            )
        else:
            row = {"slug": slug, "language": language,
                   **data, **audit(session)}
            cols = ", ".join(row)
            ph = ", ".join(["?"] * len(row))
            conn.execute(
                f"INSERT INTO search_languages ({cols}) VALUES ({ph})",
                list(row.values())
            )


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
                   es.doi, es.title,
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
    with connect() as conn:
        jur = conn.execute(
            "SELECT COUNT(*) AS n FROM search_coverage "
            "WHERE slug=? AND status != 'NOT-RUN'",
            [slug]
        ).fetchone()["n"]
        lang = conn.execute(
            "SELECT COUNT(*) AS n FROM search_languages "
            "WHERE slug=? AND status != 'NOT-RUN'",
            [slug]
        ).fetchone()["n"]
    return {
        "slug": slug,
        "jurisdictions_searched": jur,
        "jurisdictions_required": 24,
        "languages_searched": lang,
        "languages_required": 14,
        "complete": jur >= 24 and lang >= 14,
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

    # update-bpc
    p_ubpc = sub.add_parser("update-bpc", help="Update bpc_metadata for a slug")
    p_ubpc.add_argument("--slug", required=True)
    p_ubpc.add_argument("--session", required=True)
    p_ubpc.add_argument("--citation-mining-complete", type=int, choices=[0, 1])
    p_ubpc.add_argument("--bpc-complete", type=int, choices=[0, 1])
    p_ubpc.add_argument("--search-complete", type=int, choices=[0, 1])
    p_ubpc.add_argument("--pico-complete", type=int, choices=[0, 1])
    p_ubpc.add_argument("--evidence-state")
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
    p_ai.add_argument("--applicable-groups")
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

    elif args.command == "upsert-coverage":
        data = {"status": args.status, "co1_attempted": args.co1_attempted}
        upsert_search_coverage(args.slug, args.jurisdiction,
                               data=data, session=args.session,
                               dry_run=args.dry_run)
        _emit({"updated": True, "slug": args.slug, "jurisdiction": args.jurisdiction})

    elif args.command == "upsert-language":
        data = {"status": args.status, "results_count": args.results_count}
        upsert_search_language(args.slug, args.language,
                               data=data, session=args.session,
                               dry_run=args.dry_run)
        _emit({"updated": True, "slug": args.slug, "language": args.language})

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
            doi_key = "_".join(args.authors.split()[:1] + [str(args.year)] + args.title.split()[:3]).lower()
            data["doi_less_key"] = doi_key
        if args.pmid:
            data["pmid"] = args.pmid
        if args.jurisdiction:
            data["jurisdiction"] = args.jurisdiction
        if args.evidence_type:
            data["evidence_type"] = args.evidence_type
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
        if args.applicable_groups: data["applicable_groups"] = args.applicable_groups
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
    _ES_COLS = frozenset({
        "ref_id", "authors", "year", "title", "doi", "doi_less_key",
        "pmid", "tier", "evidence_type", "jurisdiction", "metadata_quality",
        "verification_status", "co1_provenance", "co1_source_type",
        "synthesis_attribution_required", "notes"
    })
    _validate_cols(data.keys(), _ES_COLS, "insert_evidence_source")
    row = {**data, **audit(session)}
    with connect(dry_run) as conn:
        cols = ", ".join(row)
        ph = ", ".join(["?"] * len(row))
        conn.execute(
            f"INSERT OR IGNORE INTO evidence_sources ({cols}) VALUES ({ph})",
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
    """Return all unmined Tier 1–N sources across all slugs."""
    with connect() as conn:
        rows = conn.execute("""
            SELECT ssl.local_ref_id, ssl.slug,
                   es.doi, es.tier, es.title,
                   COALESCE(cm.backward, 0) AS backward,
                   COALESCE(cm.forward, 0) AS forward
            FROM source_slug_links ssl
            JOIN evidence_sources es ON ssl.ref_id = es.ref_id
            LEFT JOIN citation_mining cm
                ON cm.slug = ssl.slug AND cm.local_ref_id = ssl.local_ref_id
            WHERE es.tier <= ?
            AND (cm.local_ref_id IS NULL OR cm.backward = 0 OR cm.forward = 0)
            ORDER BY es.tier ASC, ssl.slug, ssl.local_ref_id
        """, [tier_max]).fetchall()
    return [dict(r) for r in rows]


if __name__ == "__main__":
    main()
