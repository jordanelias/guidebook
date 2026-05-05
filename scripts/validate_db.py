"""
scripts/validate_db.py — Validation checks for guidebook.db.

Spec: architecture/sqlite-data-layer.md §10

Exit codes:
    0  all checks pass (including INFO)
    1  error (C1-C4, C8)
    2  warning only (C5)

Usage:
    python3 scripts/validate_db.py
    python3 scripts/validate_db.py --verbose
"""

import json
import os
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))
EXPECTED_SCHEMA_VERSION = 3


def validate(verbose: bool = False):
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")

    errors = []
    warnings = []
    infos = []

    # C1: PRAGMA integrity_check
    ic = conn.execute("PRAGMA integrity_check").fetchone()[0]
    if ic != "ok":
        errors.append(f"C1 FAIL: integrity_check returned '{ic}'")
    else:
        infos.append("C1 PASS: integrity_check ok")

    # C2: PRAGMA foreign_key_check
    fk_violations = conn.execute("PRAGMA foreign_key_check").fetchall()
    if fk_violations:
        errors.append(
            f"C2 FAIL: {len(fk_violations)} foreign key violation(s)"
        )
        if verbose:
            for v in fk_violations[:10]:
                errors.append(f"  table={v[0]} rowid={v[1]} ref={v[2]}")
    else:
        infos.append("C2 PASS: no foreign key violations")

    # C3: PRAGMA user_version
    uv = conn.execute("PRAGMA user_version").fetchone()[0]
    if uv != EXPECTED_SCHEMA_VERSION:
        errors.append(
            f"C3 FAIL: user_version={uv}, expected {EXPECTED_SCHEMA_VERSION}"
        )
    else:
        infos.append(f"C3 PASS: user_version={uv}")

    # C4: connections with 0 targets
    orphan_conns = conn.execute("""
        SELECT c.con_id FROM connections c
        LEFT JOIN connection_targets ct ON c.con_id = ct.con_id
        WHERE ct.con_id IS NULL
    """).fetchall()
    if orphan_conns:
        errors.append(
            f"C4 FAIL: {len(orphan_conns)} connection(s) with 0 targets: "
            + ", ".join(r[0] for r in orphan_conns[:10])
        )
    else:
        infos.append("C4 PASS: all connections have >=1 target")

    # C5: evidence_sources without doi or doi_less_key
    no_dedup = conn.execute("""
        SELECT ref_id FROM evidence_sources
        WHERE doi IS NULL AND doi_less_key IS NULL
    """).fetchall()
    if no_dedup:
        warnings.append(
            f"C5 WARN: {len(no_dedup)} evidence source(s) with no doi or "
            "doi_less_key (incomplete dedup data)"
        )
    else:
        infos.append("C5 PASS: all evidence sources have dedup key")

    # C6: citation_mining mined both directions but no connections
    both_mined_empty = conn.execute("""
        SELECT slug, local_ref_id FROM citation_mining
        WHERE backward=1 AND forward=1 AND connections_produced='[]'
    """).fetchall()
    if both_mined_empty:
        infos.append(
            f"C6 INFO: {len(both_mined_empty)} source(s) fully mined with "
            "no connections produced (valid outcome)"
        )
    else:
        infos.append("C6 INFO: no fully-mined-empty-result rows")

    # C7: unmined sources per slug
    unmined = conn.execute("""
        SELECT ssl.slug, COUNT(*) AS cnt
        FROM source_slug_links ssl
        LEFT JOIN citation_mining cm
            ON cm.slug=ssl.slug AND cm.local_ref_id=ssl.local_ref_id
        WHERE cm.slug IS NULL
        GROUP BY ssl.slug
    """).fetchall()
    if unmined:
        total = sum(r["cnt"] for r in unmined)
        infos.append(
            f"C7 INFO: {total} unmined source(s) across "
            f"{len(unmined)} slug(s)"
        )
        if verbose:
            for r in unmined:
                infos.append(f"  {r['slug']}: {r['cnt']} unmined")
    else:
        infos.append("C7 INFO: all linked sources have mining records")

    # C8: gaps with invalid status/priority
    bad_gaps = conn.execute("""
        SELECT gap_id, priority, status FROM gaps
        WHERE status LIKE 'OPEN%'
        AND priority NOT IN ('P1','P2','P3')
    """).fetchall()
    if bad_gaps:
        errors.append(
            f"C8 FAIL: {len(bad_gaps)} open gap(s) with invalid priority"
        )
    else:
        infos.append("C8 PASS: all open gaps have valid priority")

    # C9: term_item_links referencing non-existent items (Phase 1: INFO only)
    # Items table doesn't exist yet in Phase 1 — skip FK check
    infos.append("C9 SKIP: items table not yet created (Phase 1)")

    conn.close()

    # Report
    for msg in infos:
        print(f"  {msg}")
    for msg in warnings:
        print(f"  {msg}")
    for msg in errors:
        print(f"  {msg}")

    print()
    if errors:
        print(f"RESULT: {len(errors)} error(s), {len(warnings)} warning(s)")
        sys.exit(1)
    elif warnings:
        print(f"RESULT: 0 errors, {len(warnings)} warning(s)")
        sys.exit(2)
    else:
        print("RESULT: all checks passed")
        sys.exit(0)


if __name__ == "__main__":
    verbose = "--verbose" in sys.argv
    validate(verbose=verbose)
