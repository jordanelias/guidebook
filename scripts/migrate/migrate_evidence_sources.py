"""
scripts/migrate/migrate_evidence_sources.py — Migrate BPC REF-ID tables → SQLite.

Spec: architecture/sqlite-data-layer.md §9 Phase 1-B, order 3
Sources: references/bpc/{topic_dir}/{slug}.md (REF-ID tables)
Validation: Collision report before INSERT

This script reads the slugs table for BPC paths, fetches each from GitHub,
parses REF-ID tables, deduplicates, and inserts.

Usage:
    python3 scripts/migrate/migrate_evidence_sources.py \
        --session SESSION --pat PAT [--dry-run] [--batch-size 10]
"""

import base64
import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))
REPO = "jordanelias/guidebook"


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


def get_active_slugs() -> list[dict]:
    """Get active slugs with BPC paths from the database."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT slug, bpc_path FROM slugs WHERE status='ACTIVE'"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def fetch_bpc_batch(paths: list[str], pat: str) -> dict[str, str]:
    """Fetch multiple BPC files via GraphQL batch. Returns {path: text}."""
    import requests

    # Build aliases
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
        headers={
            "Authorization": f"bearer {pat}",
            "Content-Type": "application/json",
        },
        json={"query": query},
    )
    data = r.json().get("data", {}).get("repository", {})

    result = {}
    for alias, path in aliases.items():
        node = data.get(alias)
        if node and node.get("text"):
            result[path] = node["text"]

    return result


def parse_ref_table(text: str, slug: str) -> list[dict]:
    """Parse REF-ID table from a BPC file. Handles variable column layouts."""
    refs = []
    lines = text.splitlines()

    # Find header row and map columns
    col_map = {}
    header_idx = None
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        parts = [p.strip().lower() for p in line.split("|")]
        if "ref-id" in parts:
            header_idx = i
            for j, col in enumerate(parts):
                if "ref-id" in col:
                    col_map["ref_id"] = j
                elif col in ("authors", "author"):
                    col_map["authors"] = j
                elif col == "year":
                    col_map["year"] = j
                elif col == "title":
                    col_map["title"] = j
                elif "doi" in col or "url" in col:
                    col_map["doi"] = j
                elif col in ("tier", "evidence tier"):
                    col_map["tier"] = j
                elif "short" in col or "key" in col:
                    col_map["short_key"] = j
                elif "journal" in col or "publisher" in col:
                    col_map["journal"] = j
                elif "jurisdict" in col:
                    col_map["jurisdiction"] = j
                elif col in ("lang", "language"):
                    col_map["language"] = j
            break

    if not col_map.get("ref_id"):
        return refs  # No REF-ID table found

    # Parse data rows (skip header and separator)
    for line in lines[header_idx + 1:]:
        if not line.startswith("|"):
            break  # End of table
        parts = [p.strip() for p in line.split("|")]

        ref_id_raw = parts[col_map["ref_id"]] if col_map["ref_id"] < len(parts) else ""
        # Skip separator
        if not ref_id_raw or ref_id_raw.startswith("---"):
            continue

        def _get(key):
            idx = col_map.get(key)
            if idx is not None and idx < len(parts):
                v = parts[idx].strip()
                return v if v and v != "—" else ""
            return ""

        authors = _get("authors") or "[Unknown]"
        year = _get("year") or None
        title = _get("title") or "[Unknown]"
        doi_raw = _get("doi")
        tier_raw = _get("tier")
        jurisdiction = _get("jurisdiction")

        # Clean DOI
        doi = None
        if doi_raw:
            m = re.search(r"10\.\d{4,}/[^\s|)]+", doi_raw)
            if m:
                doi = m.group(0)
            elif doi_raw.startswith("DOI:"):
                doi = doi_raw[4:].strip()

        # Parse tier
        tier = None
        m = re.search(r"(?:Tier\s*)?(\d)", tier_raw)
        if m:
            tier = int(m.group(1))

        # Metadata quality
        is_grey = "[GREY" in title or "[GREY" in (doi_raw or "")
        if doi:
            quality = "COMPLETE"
        elif is_grey:
            quality = "GREY"
        else:
            quality = "AUTHOR-TITLE-ONLY"

        # Clean title
        if "[GREY" in title and "title" in title.lower():
            title = f"[Unverified title — {authors} {year}]"

        # Co-1 detection
        co1_provenance = None
        co1_source_type = None
        if ref_id_raw.startswith("Co1-") or "Co-1" in tier_raw:
            co1_provenance = "BPC"
            co1_source_type = "lived-experience"

        # DOI-less dedup key
        doi_less_key = None
        if not doi and authors and year:
            surname = authors.split()[0].lower().rstrip(",.")
            title_words = " ".join(title.split()[:5]).lower()
            doi_less_key = f"{surname}_{year}_{title_words}"

        refs.append({
            "local_ref_id": ref_id_raw,
            "slug": slug,
            "authors": authors,
            "year": year,
            "title": title,
            "doi": doi,
            "doi_less_key": doi_less_key,
            "tier": tier,
            "jurisdiction": jurisdiction or None,
            "metadata_quality": quality,
            "co1_provenance": co1_provenance,
            "co1_source_type": co1_source_type,
        })

    return refs


def migrate(session: str, pat: str, dry_run: bool = False,
            batch_size: int = 10):
    slugs = get_active_slugs()
    print(f"Active slugs: {len(slugs)}")

    # Fetch BPC files in batches
    all_refs = []
    paths = [s["bpc_path"] for s in slugs]
    slug_map = {s["bpc_path"]: s["slug"] for s in slugs}

    for i in range(0, len(paths), batch_size):
        batch = paths[i:i + batch_size]
        print(f"  Fetching batch {i // batch_size + 1} "
              f"({len(batch)} files)...")
        texts = fetch_bpc_batch(batch, pat)

        for path, text in texts.items():
            slug = slug_map[path]
            refs = parse_ref_table(text, slug)
            all_refs.extend(refs)
            if refs:
                print(f"    {slug}: {len(refs)} refs")

    print(f"\nTotal raw refs: {len(all_refs)}")

    # Dedup by DOI and doi_less_key
    global_refs = {}  # dedup_key → ref dict
    collisions = []
    ref_counter = 1

    for r in all_refs:
        if r["doi"]:
            key = f"doi:{r['doi'].lower()}"
        elif r["doi_less_key"]:
            key = f"dlk:{r['doi_less_key']}"
        else:
            key = f"raw:{r['authors']}_{r['year']}_{r['title'][:30]}"

        if key in global_refs:
            existing = global_refs[key]
            # Log collision
            if r["slug"] != existing["_first_slug"]:
                collisions.append({
                    "key": key,
                    "ref_id": existing["ref_id"],
                    "slugs": [existing["_first_slug"], r["slug"]],
                })
            # Add source_slug_link for this occurrence
            existing["_slug_links"].append({
                "slug": r["slug"],
                "local_ref_id": r["local_ref_id"],
            })
        else:
            ref_id = f"REF-{ref_counter:05d}"
            ref_counter += 1
            global_refs[key] = {
                **r,
                "ref_id": ref_id,
                "_first_slug": r["slug"],
                "_slug_links": [{
                    "slug": r["slug"],
                    "local_ref_id": r["local_ref_id"],
                }],
            }

    print(f"Deduplicated: {len(global_refs)} unique sources")
    if collisions:
        print(f"Cross-slug collisions: {len(collisions)}")
        for c in collisions[:10]:
            print(f"  {c['ref_id']}: {c['key'][:60]} → {c['slugs']}")

    # Insert
    ts = now_utc()
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys=ON")

    src_inserted = 0
    link_inserted = 0
    errors = []

    for key, r in global_refs.items():
        try:
            if not dry_run:
                conn.execute(
                    "INSERT INTO evidence_sources "
                    "(ref_id, authors, year, title, doi, doi_less_key, "
                    " tier, jurisdiction, metadata_quality, co1_provenance, "
                    " co1_source_type, "
                    " created_at, created_by_session, "
                    " updated_at, updated_by_session) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    [r["ref_id"], r["authors"], r["year"], r["title"],
                     r["doi"], r["doi_less_key"],
                     r["tier"], r.get("jurisdiction"),
                     r["metadata_quality"],
                     r["co1_provenance"], r["co1_source_type"],
                     ts, session, ts, session]
                )
            src_inserted += 1

            for link in r["_slug_links"]:
                try:
                    if not dry_run:
                        conn.execute(
                            "INSERT INTO source_slug_links "
                            "(ref_id, slug, local_ref_id, "
                            " created_at, created_by_session, "
                            " updated_at, updated_by_session) "
                            "VALUES (?,?,?,?,?,?,?)",
                            [r["ref_id"], link["slug"], link["local_ref_id"],
                             ts, session, ts, session]
                        )
                    link_inserted += 1
                except sqlite3.IntegrityError as e:
                    errors.append(f"  link {r['ref_id']}→{link['slug']}: {e}")
        except sqlite3.IntegrityError as e:
            errors.append(f"  {r['ref_id']}: {e}")

    if not dry_run:
        conn.commit()

    conn.close()

    print(f"\n{'[DRY-RUN] Would insert' if dry_run else 'Inserted'}: "
          f"{src_inserted} sources, {link_inserted} slug links")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors[:20]:
            print(e)

    # Validation
    if not dry_run:
        conn2 = sqlite3.connect(str(DB_PATH))
        src_total = conn2.execute(
            "SELECT COUNT(*) FROM evidence_sources"
        ).fetchone()[0]
        link_total = conn2.execute(
            "SELECT COUNT(*) FROM source_slug_links"
        ).fetchone()[0]
        no_dedup = conn2.execute(
            "SELECT COUNT(*) FROM evidence_sources "
            "WHERE doi IS NULL AND doi_less_key IS NULL"
        ).fetchone()[0]
        conn2.close()
        print(f"\nValidation:")
        print(f"  evidence_sources: {src_total}")
        print(f"  source_slug_links: {link_total}")
        print(f"  Sources without dedup key: {no_dedup}")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--session", required=True)
    p.add_argument("--pat", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--batch-size", type=int, default=10)
    args = p.parse_args()
    migrate(args.session, args.pat, args.dry_run, args.batch_size)
