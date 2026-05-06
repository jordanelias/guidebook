"""
scripts/migrate/migrate_items.py — Populate items table from spec markdown.

Extracts all ### [A-K]-NN[a-z]? headings from the current spec version and
inserts rows into the items table. Inserts via raw SQL — does NOT use
schemas.item.Item Pydantic model (many model fields not extractable from
headings; model updated separately in CO-0009 Phase 1 Session 1b).

Idempotent: uses INSERT OR IGNORE — safe to re-run.

Usage:
    python3 scripts/migrate/migrate_items.py
    python3 scripts/migrate/migrate_items.py --dry-run
    python3 scripts/migrate/migrate_items.py --verbose
"""

import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
DB_PATH   = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))
SPEC_PATH = REPO_ROOT / "versions/current/Guidebook_for_Accessible_Design_v9-0_2026-03-20.md"
SESSION   = "session_migration_migrate_items"

# Known BPC slug mapping (item_code → bpc_source_slug)
# Populated from cross-references in skill output and BPC directory.
# Items not listed here have bpc_source_slug = NULL.
SLUG_MAP = {
    "I-01": "one-hand-operable-hardware",
    "G-03": "grab-bars",
    "H-01": "acoustic-environment-residential",
    "G-05": "height-adjustable-surfaces",
    "E-01": "passenger-lifts",
    "B-06": "lighting-controls-dimming",
    "H-02": "environmental-controls",
    "K-05": "thermal-comfort-thermoregulation",
}

# Category letter → full name (for reference; not stored — derivable)
CATEGORY_NAMES = {
    "A": "Acoustic", "B": "Lighting", "C": "Circulation",
    "D": "Doors", "E": "Vertical Circulation", "F": "Flooring",
    "G": "Furniture and Fixtures", "H": "Environment",
    "I": "Controls and Hardware", "J": "Wayfinding",
    "K": "Specialist Provisions",
}


def extract_items(text: str) -> list[dict]:
    """Extract item metadata from spec markdown."""
    # Split into sections at each item heading
    heading_re = re.compile(r"^### ([A-K]-\d{2}[a-z]?) (.+?)$", re.MULTILINE)
    matches    = list(heading_re.finditer(text))
    items      = []

    for i, m in enumerate(matches):
        code = m.group(1)
        name = m.group(2).strip()
        cat  = code[0]

        # Extract section text up to next heading
        start   = m.start()
        end     = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[start:end]

        # Applicable Groups
        ag_m = re.search(
            r"\*\*Applicable Groups[:\*\s]*\*?\*?\s*(.+)", section
        )
        applicable_groups = None
        if ag_m:
            raw = ag_m.group(1).strip().rstrip("*").strip()
            # Normalise: remove markdown, parentheses and their content, extra spaces
            raw = re.sub(r"[*_`]", "", raw)
            raw = re.sub(r"\([^)]*\)", "", raw)  # remove (parenthetical notes)
            raw = re.sub(r"\s+", " ", raw).strip().rstrip(",")
            applicable_groups = raw if raw else None

        items.append({
            "item_code":         code,
            "category":          cat,
            "name":              name,
            "applicable_groups": applicable_groups,
            "bpc_source_slug":   SLUG_MAP.get(code),
            "status":            "active",
        })

    return items


def run(dry_run: bool = False, verbose: bool = False) -> int:
    if not SPEC_PATH.exists():
        print(f"ERROR: Spec not found at {SPEC_PATH}", file=sys.stderr)
        return 1

    if not DB_PATH.exists():
        print(f"ERROR: DB not found at {DB_PATH}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys=ON")

    # Check migration 004 applied
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()]
    if "items" not in tables:
        print("ERROR: items table not present — run migration 004 first")
        conn.close()
        return 1

    # Check slugs that exist in DB (FK validation)
    valid_slugs = {
        r[0] for r in conn.execute("SELECT slug FROM slugs").fetchall()
    }

    text  = SPEC_PATH.read_text(encoding="utf-8")
    items = extract_items(text)
    ts    = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

    inserted = skipped = slug_skipped = 0

    for item in items:
        # Validate bpc_source_slug against live slugs table
        slug = item["bpc_source_slug"]
        if slug and slug not in valid_slugs:
            if verbose:
                print(f"  WARN {item['item_code']}: slug '{slug}' not in slugs table — setting NULL")
            item["bpc_source_slug"] = None
            slug_skipped += 1

        if verbose:
            print(f"  {item['item_code']}: {item['name'][:50]}")

        if not dry_run:
            try:
                conn.execute("""
                    INSERT OR IGNORE INTO items
                    (item_code, item_id, category, name, applicable_groups,
                     bpc_source_slug, status,
                     created_at, created_by_session, updated_at, updated_by_session)
                    VALUES (?,NULL,?,?,?,?,?,?,?,?,?)
                """, (
                    item["item_code"],
                    item["category"],
                    item["name"],
                    item["applicable_groups"],
                    item["bpc_source_slug"],
                    item["status"],
                    ts, SESSION, ts, SESSION,
                ))
                if conn.execute(
                    "SELECT changes()"
                ).fetchone()[0] > 0:
                    inserted += 1
                else:
                    skipped += 1
            except sqlite3.IntegrityError as e:
                print(f"  ERROR {item['item_code']}: {e}")

    if not dry_run:
        conn.commit()

    conn.close()

    print(f"migrate_items: {len(items)} items extracted from spec")
    if dry_run:
        print(f"  [DRY-RUN] Would insert {len(items)} items")
    else:
        print(f"  Inserted: {inserted}  Already present: {skipped}")
    if slug_skipped:
        print(f"  Slug warnings (set NULL): {slug_skipped}")

    return 0


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv
    sys.exit(run(dry_run=dry_run, verbose=verbose))
