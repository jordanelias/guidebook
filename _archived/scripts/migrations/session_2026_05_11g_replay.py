#!/usr/bin/env python3
"""
scripts/migrations/session_2026_05_11g_replay.py

Replay-script for session_2026-05-11g-citation-mining. This session's DB writes
were clobbered three times by concurrent pushes from session_2026-05-11e-wayfinding-dementia
(commits d803dbda39, ab30ef3d81, c2bc96be28 vs my recoveries b254fb71a1 and 1dc4ca4d25).
See GAP-290 for the architectural issue.

This script captures all DB work I performed so it can be reapplied idempotently
once the concurrent-write window closes. Reads scripts/migrations/session_2026_05_11g_data.json
(the JSON dump of my local DB state) and applies it to data/guidebook.db.

Idempotent: safe to re-run. Each operation checks state before applying.

Usage:
    python3 scripts/migrations/session_2026_05_11g_replay.py [--db data/guidebook.db] [--dry-run]

To apply:
    1. Verify no concurrent agent is writing to data/guidebook.db
    2. Pull latest main, ensure clean tree
    3. Run this script (without --dry-run)
    4. Commit + push the resulting data/guidebook.db with message referencing this script
    5. Verify the audits pass (scripts/audit/citation_mining_completeness.py, source_slug_links_duplicates.py)
"""
import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime

DEFAULT_DB = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")
DEFAULT_DATA = os.path.join(os.path.dirname(__file__), "session_2026_05_11g_data.json")

def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    p.add_argument("--db", default=DEFAULT_DB)
    p.add_argument("--data", default=DEFAULT_DATA)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    if not os.path.exists(args.db):
        print(f"ERROR: DB not found at {args.db}", file=sys.stderr)
        return 1
    if not os.path.exists(args.data):
        print(f"ERROR: data file not found at {args.data}", file=sys.stderr)
        return 1

    with open(args.data) as f:
        data = json.load(f)

    print(f"=== Replay session {data['session']} ===")
    print(f"  DB: {args.db}")
    print(f"  Data: {args.data}")
    print(f"  Dry-run: {args.dry_run}")
    print()

    con = sqlite3.connect(args.db)
    con.row_factory = sqlite3.Row

    # Stats
    stats = {
        "evidence_sources_inserted": 0,
        "evidence_sources_already_present": 0,
        "source_slug_links_inserted": 0,
        "source_slug_links_already_present": 0,
        "citation_mining_inserted": 0,
        "citation_mining_already_present": 0,
        "evidence_sources_updates_applied": 0,
        "evidence_sources_updates_already_applied": 0,
        "source_slug_links_renumbered": 0,
        "source_slug_links_renumber_already_applied": 0,
        "orphan_rows_deleted": 0,
        "orphan_rows_already_deleted": 0,
        "orphan_rows_held_back": 0,
        "gaps_inserted": 0,
        "gaps_already_present": 0,
        "gaps_closed": 0,
        "gaps_already_closed": 0,
    }

    # 1) evidence_sources
    print("--- evidence_sources new ---")
    for es in data["evidence_sources_new"]:
        existing = con.execute("SELECT ref_id FROM evidence_sources WHERE ref_id = ?", (es["ref_id"],)).fetchone()
        if existing:
            stats["evidence_sources_already_present"] += 1
            continue
        cols = list(es.keys())
        placeholders = ",".join("?" * len(cols))
        if not args.dry_run:
            con.execute(f"INSERT INTO evidence_sources ({','.join(cols)}) VALUES ({placeholders})", tuple(es[c] for c in cols))
        stats["evidence_sources_inserted"] += 1
        print(f"  +{es['ref_id']} T{es.get('tier','?')} {(es.get('authors') or '')[:40]}")

    # 2) source_slug_links new
    print("\n--- source_slug_links new ---")
    for ssl in data["source_slug_links_new"]:
        existing = con.execute(
            "SELECT ref_id FROM source_slug_links WHERE slug = ? AND local_ref_id = ? AND ref_id = ?",
            (ssl["slug"], ssl["local_ref_id"], ssl["ref_id"])
        ).fetchone()
        if existing:
            stats["source_slug_links_already_present"] += 1
            continue
        cols = list(ssl.keys())
        placeholders = ",".join("?" * len(cols))
        if not args.dry_run:
            con.execute(f"INSERT INTO source_slug_links ({','.join(cols)}) VALUES ({placeholders})", tuple(ssl[c] for c in cols))
        stats["source_slug_links_inserted"] += 1

    # 3) source_slug_links renumbered
    print("\n--- source_slug_links renumbered ---")
    for ssl in data["source_slug_links_renumbered"]:
        # Check if the renumber has already been applied (the row matches our target state)
        existing = con.execute(
            "SELECT local_ref_id FROM source_slug_links WHERE slug = ? AND ref_id = ?",
            (ssl["slug"], ssl["ref_id"])
        ).fetchone()
        if existing and existing[0] == ssl["local_ref_id"]:
            stats["source_slug_links_renumber_already_applied"] += 1
            continue
        if not args.dry_run:
            con.execute(
                "UPDATE source_slug_links SET local_ref_id = ?, updated_at = ?, updated_by_session = ? WHERE slug = ? AND ref_id = ?",
                (ssl["local_ref_id"], ssl["updated_at"], ssl["updated_by_session"], ssl["slug"], ssl["ref_id"])
            )
        stats["source_slug_links_renumbered"] += 1
        print(f"  ~ {ssl['slug']} / {ssl['ref_id']} -> local_ref_id={ssl['local_ref_id']}")

    # 4) citation_mining
    print("\n--- citation_mining new ---")
    for cm in data["citation_mining_new"]:
        existing = con.execute(
            "SELECT global_ref_id FROM citation_mining WHERE global_ref_id = ?",
            (cm["global_ref_id"],)
        ).fetchone()
        if existing:
            stats["citation_mining_already_present"] += 1
            continue
        cols = list(cm.keys())
        placeholders = ",".join("?" * len(cols))
        if not args.dry_run:
            con.execute(f"INSERT INTO citation_mining ({','.join(cols)}) VALUES ({placeholders})", tuple(cm[c] for c in cols))
        stats["citation_mining_inserted"] += 1

    # 5) evidence_sources updates (T3 verifications)
    print("\n--- evidence_sources updates (T3 verifications) ---")
    for u in data["evidence_sources_updates"]:
        existing = con.execute("SELECT verification_status FROM evidence_sources WHERE ref_id = ?", (u["ref_id"],)).fetchone()
        if existing and existing[0] == u["verification_status"]:
            stats["evidence_sources_updates_already_applied"] += 1
            continue
        if not args.dry_run:
            con.execute(
                "UPDATE evidence_sources SET verification_status = ?, notes = COALESCE(?, notes), doi = COALESCE(?, doi), updated_at = ?, updated_by_session = ? WHERE ref_id = ?",
                (u["verification_status"], u.get("notes"), u.get("doi"), u["updated_at"], u["updated_by_session"], u["ref_id"])
            )
        stats["evidence_sources_updates_applied"] += 1
        print(f"  ~ {u['ref_id']} -> verification_status={u['verification_status']}")

    # 6) source_slug_links orphan cleanup (sibling-pattern rule)
    print("\n--- source_slug_links orphan cleanup ---")
    orphans = con.execute("SELECT rowid, ref_id, slug, local_ref_id FROM source_slug_links WHERE ref_id NOT LIKE 'REF-%'").fetchall()
    for o in orphans:
        sibling = con.execute(
            "SELECT ref_id FROM source_slug_links WHERE slug = ? AND local_ref_id = ? AND ref_id LIKE 'REF-%'",
            (o["slug"], o["local_ref_id"])
        ).fetchone()
        if not sibling:
            stats["orphan_rows_held_back"] += 1
            print(f"  HELD: {o['ref_id']} / {o['slug']} — no sibling, manual handling required (see GAP-289)")
            continue
        if not args.dry_run:
            con.execute("DELETE FROM source_slug_links WHERE rowid = ?", (o["rowid"],))
        stats["orphan_rows_deleted"] += 1

    # 7) gaps new
    print("\n--- gaps new ---")
    for g in data["gaps_new"]:
        existing = con.execute("SELECT gap_id FROM gaps WHERE gap_id = ?", (g["gap_id"],)).fetchone()
        if existing:
            stats["gaps_already_present"] += 1
            continue
        cols = list(g.keys())
        placeholders = ",".join("?" * len(cols))
        if not args.dry_run:
            con.execute(f"INSERT INTO gaps ({','.join(cols)}) VALUES ({placeholders})", tuple(g[c] for c in cols))
        stats["gaps_inserted"] += 1
        print(f"  + {g['gap_id']} {g.get('category','?')} {g.get('priority','?')}")

    # 8) gaps closed
    print("\n--- gaps closed ---")
    for c in data["gaps_closed"]:
        existing = con.execute("SELECT status FROM gaps WHERE gap_id = ?", (c["gap_id"],)).fetchone()
        if existing and existing[0] == c["status"]:
            stats["gaps_already_closed"] += 1
            continue
        if not args.dry_run:
            now = datetime.utcnow().isoformat(timespec='seconds')
            con.execute(
                "UPDATE gaps SET status = ?, updated_at = ?, updated_by_session = ? WHERE gap_id = ?",
                (c["status"], now, data["session"], c["gap_id"])
            )
        stats["gaps_closed"] += 1
        print(f"  ~ {c['gap_id']} -> {c['status']}")

    if not args.dry_run:
        con.commit()

    print()
    print("=== Summary ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print()
    print("To verify:")
    print(f"  python3 scripts/audit/citation_mining_completeness.py --session {data['session']} --tier-max 2")
    print(f"  python3 scripts/audit/source_slug_links_duplicates.py")

    return 0

if __name__ == "__main__":
    sys.exit(main())
