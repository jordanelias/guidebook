"""
scripts/migrate/migrate_bpc_metadata.py — Migrate BPC front-matter → SQLite bpc_metadata.

Spec: architecture/sqlite-data-layer.md §9 Phase 1-B, order 6
Sources: references/bpc/{topic_dir}/{slug}.md (YAML front-matter + REF-ID table stats)
Validation: count = active slug count

Usage:
    python3 scripts/migrate/migrate_bpc_metadata.py \
        --session SESSION --pat PAT [--dry-run] [--batch-size 10]
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


def get_active_slugs() -> list[dict]:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT slug, bpc_path, topic_directory FROM slugs WHERE status='ACTIVE'"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def fetch_bpc_batch(paths: list[str], pat: str) -> dict[str, str]:
    import requests
    aliases = {}
    query_parts = []
    for i, path in enumerate(paths):
        alias = f"f{i}"
        aliases[alias] = path
        query_parts.append(
            f'{alias}:object(expression:"main:{path}"){{...on Blob{{text}}}}'
        )
    query = (
        'query{repository(owner:"jordanelias",name:"guidebook"){'
        + " ".join(query_parts) + "}}"
    )
    r = requests.post(
        "https://api.github.com/graphql",
        headers={"Authorization": f"bearer {pat}",
                 "Content-Type": "application/json"},
        json={"query": query},
    )
    data = r.json().get("data", {}).get("repository", {})
    result = {}
    for alias, path in aliases.items():
        node = data.get(alias)
        if node and node.get("text"):
            result[path] = node["text"]
    return result


def extract_metadata(text: str, slug: str) -> dict:
    """Extract metadata from BPC file content."""
    meta = {
        "slug": slug,
        "population": "UNKNOWN",
        "last_updated": None,
        "jurisdictions_searched": 0,
        "co1_pass_count": 0,
        "evidence_state": None,
        "pico_complete": 0,
        "search_complete": 0,
        "bpc_complete": 0,
        "citation_mining_complete": 0,
    }

    # Extract population from title or population line
    pop_match = re.search(
        r"\*\*Population[s]?\s*(?:code[s]?)?\s*[:：]\*\*\s*(.+)",
        text, re.IGNORECASE
    )
    if pop_match:
        meta["population"] = pop_match.group(1).strip()
    else:
        # Try from filename convention or first heading
        for line in text.splitlines()[:10]:
            if line.startswith("# "):
                # Often the heading contains population info
                meta["population"] = "SEE-HEADING"
                break

    # Check for BPC synthesis section
    if "## Best Practice Compilation" in text or "## BPC" in text:
        meta["bpc_complete"] = 1
        meta["evidence_state"] = "BPC-PRESENT"
    elif "## Synthesis" in text:
        meta["bpc_complete"] = 1
        meta["evidence_state"] = "SYNTHESIS-PRESENT"
    else:
        meta["evidence_state"] = "NO-BPC"

    # Count jurisdictions from REF-ID table
    jurisdictions = set()
    for line in text.splitlines():
        if line.startswith("|") and not line.startswith("| REF-ID") \
                and not line.startswith("|---"):
            parts = [p.strip() for p in line.split("|")]
            # Look for jurisdiction-like values (2-letter codes)
            for p in parts:
                if re.match(r"^[A-Z]{2}$", p):
                    jurisdictions.add(p)
    if jurisdictions:
        meta["jurisdictions_searched"] = len(jurisdictions)

    # Check for PICO
    if "## PICO" in text or "**PICO" in text:
        meta["pico_complete"] = 1

    # Check for search coverage
    if "## Search" in text and "jurisdict" in text.lower():
        meta["search_complete"] = 1

    # Check for Co-1 evidence
    co1_count = len(re.findall(r"Co-?1", text))
    meta["co1_pass_count"] = min(co1_count, 99)

    # Last updated from schema line
    updated_match = re.search(
        r"\*\*(?:Last )?[Uu]pdated[:：]\*\*\s*(\d{4}-\d{2}-\d{2})",
        text
    )
    if updated_match:
        meta["last_updated"] = updated_match.group(1)

    return meta


def migrate(session: str, pat: str, dry_run: bool = False,
            batch_size: int = 10):
    slugs = get_active_slugs()
    print(f"Active slugs: {len(slugs)}")

    paths = [s["bpc_path"] for s in slugs]
    slug_map = {s["bpc_path"]: s["slug"] for s in slugs}

    all_meta = []

    for i in range(0, len(paths), batch_size):
        batch = paths[i:i + batch_size]
        print(f"  Fetching batch {i // batch_size + 1} "
              f"({len(batch)} files)...")
        texts = fetch_bpc_batch(batch, pat)

        for path, text in texts.items():
            slug = slug_map[path]
            meta = extract_metadata(text, slug)
            all_meta.append(meta)

    print(f"\nExtracted metadata for {len(all_meta)} BPC files")

    ts = now_utc()
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys=ON")

    inserted = 0
    errors = []

    for m in all_meta:
        try:
            if not dry_run:
                conn.execute(
                    "INSERT INTO bpc_metadata "
                    "(slug, population, last_updated, jurisdictions_searched, "
                    " co1_pass_count, evidence_state, pico_complete, "
                    " search_complete, bpc_complete, citation_mining_complete, "
                    " created_at, created_by_session, "
                    " updated_at, updated_by_session) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    [m["slug"], m["population"], m["last_updated"],
                     m["jurisdictions_searched"], m["co1_pass_count"],
                     m["evidence_state"], m["pico_complete"],
                     m["search_complete"], m["bpc_complete"],
                     m["citation_mining_complete"],
                     ts, session, ts, session]
                )
            inserted += 1
        except sqlite3.IntegrityError as e:
            errors.append(f"  {m['slug']}: {e}")

    if not dry_run:
        conn.commit()
    conn.close()

    print(f"\n{'[DRY-RUN] Would insert' if dry_run else 'Inserted'}: "
          f"{inserted}/{len(all_meta)} bpc_metadata rows")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(e)

    if not dry_run:
        conn2 = sqlite3.connect(str(DB_PATH))
        total = conn2.execute("SELECT COUNT(*) FROM bpc_metadata").fetchone()[0]
        slug_count = conn2.execute(
            "SELECT COUNT(*) FROM slugs WHERE status='ACTIVE'"
        ).fetchone()[0]
        conn2.close()
        print(f"\nValidation:")
        print(f"  bpc_metadata rows: {total}")
        print(f"  Active slugs: {slug_count}")
        print(f"  Match: {'✓' if total == slug_count else '✗ MISMATCH'} "
              f"({total}/{slug_count})")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--session", required=True)
    p.add_argument("--pat", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--batch-size", type=int, default=10)
    args = p.parse_args()
    migrate(args.session, args.pat, args.dry_run, args.batch_size)
