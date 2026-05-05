"""
scripts/migrate/migrate_connections.py — Migrate connections to SQLite.

Spec: architecture/sqlite-data-layer.md §9 Phase 1-B, order 4
Sources: references/connections/_index.md + per-topic connections.md files
Validation: 232+ rows; status counts match; all targets populated

Usage:
    python3 scripts/migrate/migrate_connections.py \
        --index-file connections/idx.md \
        --topic-dir connections/ \
        --session SESSION [--dry-run]
"""

import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


def parse_index(path: str) -> list[dict]:
    """Parse _index.md markdown table. Deduplicates by con_id, merging targets."""
    text = Path(path).read_text()
    by_id = {}  # con_id → dict (merge on duplicate)

    for line in text.splitlines():
        if not line.startswith("| CON-"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 8:
            continue

        con_id = parts[1]
        # Skip header row
        if con_id == "CON-ID":
            continue
        status = parts[2]
        targets_raw = parts[3]
        filed_in = parts[4]
        confidence = parts[5]
        opus_reviewed_raw = parts[6]
        session_applied = parts[7] if parts[7] and parts[7] != "—" else None

        # Parse targets: comma-separated, may include notes in parens
        targets = []
        for t in re.split(r",\s*", targets_raw):
            t = t.strip()
            # Remove parenthetical notes
            t = re.sub(r"\s*\([^)]*\)", "", t).strip()
            if t and t != "—":
                targets.append(t)

        # Parse opus_reviewed
        opus_reviewed = 1 if opus_reviewed_raw.lower() == "true" else 0

        # Normalize confidence
        if confidence == "MEDIUM":
            confidence = "MODERATE"

        if con_id in by_id:
            # Merge: combine targets, prefer opus_reviewed=true
            existing = by_id[con_id]
            existing["targets"] = list(dict.fromkeys(
                existing["targets"] + targets
            ))
            if opus_reviewed:
                existing["opus_reviewed"] = 1
        else:
            by_id[con_id] = {
                "con_id": con_id,
                "status": status,
                "targets": targets,
                "filed_in": filed_in,
                "confidence": confidence,
                "opus_reviewed": opus_reviewed,
                "session_applied": session_applied,
            }

    return list(by_id.values())


def parse_topic_descriptions(topic_dir: str) -> dict[str, str]:
    """Parse per-topic connection files for description text.

    Returns {con_id: description_text}.
    """
    descriptions = {}
    topic_path = Path(topic_dir)

    for fpath in sorted(topic_path.glob("*.md")):
        if fpath.name == "idx.md":
            continue
        text = fpath.read_text()

        # Split by ### CON-NNNN headers
        sections = re.split(r"(?=^### CON-\d{4})", text, flags=re.MULTILINE)

        for section in sections:
            m = re.match(r"^### (CON-\d{4})", section)
            if not m:
                continue
            con_id = m.group(1)

            # Extract the Connection: paragraph
            # Look for **Connection:** line
            conn_match = re.search(
                r"\*\*Connection:\*\*\s*(.*?)(?=\n\*\*(?:Evidence|Action|Disposition|Source|Target)|---|\Z)",
                section,
                re.DOTALL
            )
            if conn_match:
                desc = conn_match.group(1).strip()
                # Clean up markdown formatting
                desc = re.sub(r"\n{3,}", "\n\n", desc)
                descriptions[con_id] = desc
            else:
                # Try to get the first substantive paragraph after metadata
                lines = section.split("\n")
                desc_lines = []
                past_metadata = False
                for line in lines[1:]:  # skip header
                    if line.startswith("**") and ":" in line:
                        past_metadata = True
                        continue
                    if past_metadata and line.strip():
                        desc_lines.append(line.strip())
                    elif past_metadata and not line.strip() and desc_lines:
                        break
                if desc_lines:
                    descriptions[con_id] = " ".join(desc_lines)

    return descriptions


def migrate(index_file: str, topic_dir: str, session: str,
            dry_run: bool = False):
    rows = parse_index(index_file)
    print(f"Parsed {len(rows)} connections from index")

    descriptions = parse_topic_descriptions(topic_dir)
    print(f"Parsed {len(descriptions)} descriptions from topic files")

    # Stats
    status_counts = {}
    confidence_counts = {}
    for r in rows:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1
        confidence_counts[r["confidence"]] = \
            confidence_counts.get(r["confidence"], 0) + 1

    print(f"  Status: {json.dumps(status_counts)}")
    print(f"  Confidence: {json.dumps(confidence_counts)}")

    no_targets = [r for r in rows if not r["targets"]]
    if no_targets:
        print(f"  WARNING: {len(no_targets)} connections with no targets:")
        for r in no_targets[:5]:
            print(f"    {r['con_id']}")

    ts = now_utc()
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys=ON")

    inserted = 0
    target_count = 0
    desc_count = 0
    errors = []

    for r in rows:
        desc = descriptions.get(r["con_id"])
        if desc:
            desc_count += 1

        try:
            if not dry_run:
                conn.execute(
                    "INSERT INTO connections "
                    "(con_id, status, confidence, filed_in, description, "
                    " opus_reviewed, session_applied, "
                    " created_at, created_by_session, "
                    " updated_at, updated_by_session) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    [r["con_id"], r["status"], r["confidence"],
                     r["filed_in"], desc,
                     r["opus_reviewed"], r["session_applied"],
                     ts, session, ts, session]
                )
                for t in r["targets"]:
                    conn.execute(
                        "INSERT OR IGNORE INTO connection_targets "
                        "(con_id, target) VALUES (?,?)",
                        [r["con_id"], t]
                    )
            inserted += 1
            target_count += len(r["targets"])
        except sqlite3.IntegrityError as e:
            errors.append(f"  {r['con_id']}: {e}")

    if not dry_run:
        conn.commit()

    conn.close()

    print(f"\n{'[DRY-RUN] Would insert' if dry_run else 'Inserted'}: "
          f"{inserted}/{len(rows)} connections, "
          f"{target_count} targets, "
          f"{desc_count} descriptions attached")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(e)

    # Validation
    if not dry_run:
        conn2 = sqlite3.connect(str(DB_PATH))
        total = conn2.execute(
            "SELECT COUNT(*) FROM connections"
        ).fetchone()[0]
        pending = conn2.execute(
            "SELECT COUNT(*) FROM connections WHERE status='PENDING'"
        ).fetchone()[0]
        orphans = conn2.execute("""
            SELECT COUNT(*) FROM connections c
            LEFT JOIN connection_targets ct ON c.con_id = ct.con_id
            WHERE ct.con_id IS NULL
        """).fetchone()[0]
        targets_total = conn2.execute(
            "SELECT COUNT(*) FROM connection_targets"
        ).fetchone()[0]
        conn2.close()
        print(f"\nValidation:")
        print(f"  Total connections: {total}")
        print(f"  PENDING: {pending}")
        print(f"  Orphan connections (no targets): {orphans}")
        print(f"  Total targets: {targets_total}")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--index-file", required=True)
    p.add_argument("--topic-dir", required=True)
    p.add_argument("--session", required=True)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    migrate(args.index_file, args.topic_dir, args.session, args.dry_run)
