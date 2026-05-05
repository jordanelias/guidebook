"""
scripts/migrate/migrate_decisions.py — Migrate decision_register.yaml → SQLite decisions table.

Spec: architecture/sqlite-data-layer.md §9 Phase 1-B, order 2
Source: data/decisions/decision_register.yaml
Validation: JSON arrays round-trip

Usage:
    python3 scripts/migrate/migrate_decisions.py --source decision_register.yaml --session SESSION [--dry-run]
"""

import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))

try:
    import yaml
except ImportError:
    print("Installing pyyaml...", file=sys.stderr)
    os.system("pip install pyyaml --break-system-packages -q")
    import yaml


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


def migrate(source: str, session: str, dry_run: bool = False):
    with open(source) as f:
        data = yaml.safe_load(f)

    decisions = data.get("decisions", [])
    print(f"Parsed {len(decisions)} decisions from {source}")

    ts = now_utc()
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys=ON")

    inserted = 0
    errors = []

    for d in decisions:
        # Convert list fields to JSON strings
        supersedes = json.dumps(d.get("supersedes") or [])
        predecessors = json.dumps(d.get("predecessors") or [])
        decision_artifacts = json.dumps(d.get("decision_artifacts") or [])
        alternatives = json.dumps(d.get("alternatives_considered") or [])

        # Handle delegation_rationale (may not exist)
        delegation_rationale = d.get("delegation_rationale")

        try:
            if not dry_run:
                conn.execute(
                    "INSERT INTO decisions "
                    "(decision_id, category, delegation, delegation_rationale, "
                    " summary, outcome, rationale, decision_date, decided_by, "
                    " model_routing, effort_level, status, review_status, "
                    " supersedes, predecessors, decision_artifacts, "
                    " alternatives_considered, notes, "
                    " created_at, created_by_session, "
                    " updated_at, updated_by_session) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    [
                        d["decision_id"], d["category"], d["delegation"],
                        delegation_rationale,
                        d["summary"], d["outcome"], d["rationale"],
                        str(d["decision_date"]), d["decided_by"],
                        d["model_routing"], d["effort_level"],
                        d["status"], d["review_status"],
                        supersedes, predecessors, decision_artifacts,
                        alternatives, d.get("notes"),
                        ts, session, ts, session,
                    ]
                )
            inserted += 1
        except (sqlite3.IntegrityError, KeyError) as e:
            errors.append(f"  {d.get('decision_id', '???')}: {e}")

    if not dry_run:
        conn.commit()

    conn.close()

    print(f"\n{'[DRY-RUN] Would insert' if dry_run else 'Inserted'}: "
          f"{inserted}/{len(decisions)} decisions")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(e)

    # Validation: JSON round-trip check
    if not dry_run:
        conn2 = sqlite3.connect(str(DB_PATH))
        conn2.row_factory = sqlite3.Row
        total = conn2.execute("SELECT COUNT(*) FROM decisions").fetchone()[0]

        # Spot-check: verify JSON arrays deserialize correctly
        sample = conn2.execute(
            "SELECT decision_id, supersedes, predecessors, "
            "decision_artifacts, alternatives_considered "
            "FROM decisions LIMIT 5"
        ).fetchall()

        json_ok = 0
        json_fail = 0
        for row in sample:
            try:
                for col in ["supersedes", "predecessors",
                            "decision_artifacts", "alternatives_considered"]:
                    parsed = json.loads(row[col])
                    assert isinstance(parsed, list), f"{col} not a list"
                json_ok += 1
            except (json.JSONDecodeError, AssertionError) as e:
                json_fail += 1
                print(f"  JSON FAIL {row['decision_id']}: {e}")

        conn2.close()
        print(f"\nValidation:")
        print(f"  Total rows: {total} "
              f"({'✓' if total == len(decisions) else '✗ MISMATCH'})")
        print(f"  JSON round-trip: {json_ok}/{json_ok + json_fail} "
              f"samples pass")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--session", required=True)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    migrate(args.source, args.session, args.dry_run)
