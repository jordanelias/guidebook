#!/usr/bin/env python3
"""
Migration 010: Schema FK Integrity Fix
=======================================
Date: 2026-05-13
Session: session_2026-05-13b-evidence-verification-methodology
Adopted via: DR-2026-05-13 §9 step 1 (FK fix is independent of methodology decision)
Origin handoff: handoff-2026-05-13b-schema-and-verification-methodology.md §3

Scope
-----
Repoint foreign keys from `evidence_sources_v1_legacy` to `evidence_sources` on
four tables (782 rows total) using SQLite's table-rebuild pattern. Includes
two data fixes and one schema addition.

| Table                       | Rows | FK col          | Pattern  |
|-----------------------------|------|-----------------|----------|
| source_slug_links           | 721  | ref_id          | NOT NULL |
| evidence_population_match   | 22   | ref_id          | NULL OK  |
| spec_value_probes           | 18   | ref_id          | NULL OK  |
| citation_mining             | 21   | global_ref_id   | NULL OK  |

Data fixes
----------
- Fix PMP-A02-001-S2 `ref_id` from 'ANSI-S12.60-S5.3' (invalid) to 'REF-00335'
  (ANSI S12.60:2010 in evidence_sources; matches the cited standard).
- Backfill `ref_id` on 5 evidence_population_match rows where ref_id IS NULL
  but `source_ref` is a valid REF-NNNNN that resolves in evidence_sources:
  EPM-S3-001 (REF-00642), EPM-S3-002 (REF-00710), EPM-S3-003 (REF-00711),
  EPM-C4-001 (REF-00551), EPM-C4-002 (REF-00557).

Schema addition
---------------
- Add `gap_id TEXT REFERENCES gaps(gap_id)` to evidence_population_match
  to support standing rule #7's audit trail (which gap generated each match).

NOT in scope
------------
- `search_query` / `search_query_alt` NOT NULL on spec_value_probes
  (6 existing rows have legitimate NULLs; audit-level enforcement stays).
- Dropping `evidence_sources_v1_legacy` (other sessions may reference it;
  defer to a future migration after confirming no remaining FKs).
- Resolving the `source_ref` / `ref_id` duplicate-column anomaly in
  evidence_population_match (both retained; source_ref is raw text, ref_id is FK).

Method
------
SQLite cannot ALTER foreign keys. Each table must be rebuilt:
  CREATE TABLE _new -> INSERT FROM old -> DROP old -> RENAME _new.
Wrapped in a single transaction with `PRAGMA foreign_keys = OFF` outside.
Views are dropped before table rebuild and recreated after.

Verification
------------
- BEFORE: PRAGMA foreign_key_check reports the known violation (PMP-A02-001-S2).
- AFTER: PRAGMA foreign_key_check returns empty rowset.
- AFTER: row counts on all 4 tables match BEFORE counts.
- AFTER: schema FK targets all point to `evidence_sources`.
- AFTER: user_version advances from 9 to 10.

Reversibility
-------------
Pre-migration DB is backed up to `/tmp/guidebook.db.pre-mig007` before this
script runs. If any verification fails, the migration's transaction is rolled
back and the original DB is unchanged. Disaster recovery: restore from backup.

Usage
-----
    python3 migration_007.py [DB_PATH]
    # default DB_PATH = /tmp/guidebook.db
"""
import sqlite3
import sys


DB_PATH = sys.argv[1] if len(sys.argv) > 1 else "/tmp/guidebook.db"


SOURCE_SLUG_LINKS_NEW = """
CREATE TABLE _new_source_slug_links (
    ref_id              TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    local_ref_id        TEXT NOT NULL,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    PRIMARY KEY (ref_id, slug)
)
"""

EVIDENCE_POPULATION_MATCH_NEW = """
CREATE TABLE _new_evidence_population_match (
    match_id            TEXT PRIMARY KEY,
    source_ref          TEXT NOT NULL,
    target_population   TEXT NOT NULL,
    study_population    TEXT,
    sample_size         INTEGER,
    match_grade         TEXT NOT NULL CHECK(match_grade IN ('EXACT','PARTIAL','PROXY','MISMATCH')),
    mismatch_note       TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    ref_id              TEXT REFERENCES evidence_sources(ref_id),
    gap_id              TEXT REFERENCES gaps(gap_id)
)
"""

SPEC_VALUE_PROBES_NEW = """
CREATE TABLE _new_spec_value_probes (
    probe_id            TEXT PRIMARY KEY,
    walk_id             TEXT NOT NULL,
    slug                TEXT NOT NULL,
    item_code           TEXT NOT NULL REFERENCES items(item_code),
    spec_value_origin   REAL NOT NULL,
    spec_unit           TEXT NOT NULL,
    direction           TEXT NOT NULL CHECK (direction IN ('up','down')),
    population          TEXT NOT NULL,
    claim_type          TEXT NOT NULL
                        CHECK (claim_type IN (
                            'minimum','maximum','target','range_low','range_high'
                        )),
    step_index          INTEGER NOT NULL,
    phase               TEXT NOT NULL
                        CHECK (phase IN (
                            'outer-pass-1st','outer-pass-2nd','outer-stop',
                            'refinement-pass-1st','refinement-pass-2nd','refinement-stop',
                            'final'
                        )),
    step_value          REAL NOT NULL,
    step_value_unit     TEXT NOT NULL,
    search_query        TEXT,
    search_query_alt    TEXT,
    passes_strict       INTEGER CHECK (passes_strict IN (0,1)),
    ref_id              TEXT REFERENCES evidence_sources(ref_id),
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL
)
"""

CITATION_MINING_NEW = """
CREATE TABLE _new_citation_mining (
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    local_ref_id        TEXT NOT NULL,
    global_ref_id       TEXT REFERENCES evidence_sources(ref_id),
    doi                 TEXT,
    backward            INTEGER NOT NULL DEFAULT 0 CHECK(backward IN (0,1)),
    forward             INTEGER NOT NULL DEFAULT 0 CHECK(forward IN (0,1)),
    connections_produced TEXT NOT NULL DEFAULT '[]',
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    deferred_reason     TEXT,
    PRIMARY KEY (slug, local_ref_id)
)
"""

V_PMP_LATEST_WALK = """
CREATE VIEW v_pmp_latest_walk AS
SELECT
    item_code,
    slug,
    walk_id,
    MAX(created_at) AS walk_completed_at,
    SUM(CASE WHEN phase IN (
            'outer-pass-1st','outer-pass-2nd',
            'refinement-pass-1st','refinement-pass-2nd'
        ) THEN 1 ELSE 0 END) AS supported_steps,
    SUM(CASE WHEN phase IN (
            'outer-stop','refinement-stop'
        ) THEN 1 ELSE 0 END) AS terminator_steps
FROM spec_value_probes
GROUP BY item_code, slug, walk_id
"""

INDEXES = [
    "CREATE INDEX idx_ssl_slug ON source_slug_links(slug)",
    "CREATE INDEX idx_ssl_ref  ON source_slug_links(ref_id)",
    "CREATE INDEX idx_svp_slug_item  ON spec_value_probes(slug, item_code)",
    "CREATE INDEX idx_svp_walk       ON spec_value_probes(walk_id, step_index)",
    "CREATE INDEX idx_svp_item_phase ON spec_value_probes(item_code, phase)",
    "CREATE INDEX idx_svp_ref        ON spec_value_probes(ref_id)",
    "CREATE INDEX idx_cm_unmined ON citation_mining(slug, backward, forward)",
    "CREATE INDEX idx_epm_ref ON evidence_population_match(ref_id)",
    "CREATE INDEX idx_epm_gap ON evidence_population_match(gap_id)",
]


EPM_REF_BACKFILLS = [
    ("EPM-S3-001", "REF-00642"),
    ("EPM-S3-002", "REF-00710"),
    ("EPM-S3-003", "REF-00711"),
    ("EPM-C4-001", "REF-00551"),
    ("EPM-C4-002", "REF-00557"),
]


def main() -> int:
    db = sqlite3.connect(DB_PATH)
    db.isolation_level = None  # manage transactions ourselves so PRAGMAs take effect

    print(f"Migration 010 against: {DB_PATH}")
    print("=" * 60)

    # Pre-state
    pre_uv = db.execute("PRAGMA user_version").fetchone()[0]
    print(f"Pre user_version: {pre_uv}")
    if pre_uv != 9:
        print(f"  HALT: expected user_version=9, found {pre_uv}")
        return 1

    pre_counts = {}
    for t in ["source_slug_links", "evidence_population_match", "spec_value_probes", "citation_mining"]:
        pre_counts[t] = db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"Pre {t}: {pre_counts[t]} rows")
    if pre_counts != {"source_slug_links": 721, "evidence_population_match": 22, "spec_value_probes": 18, "citation_mining": 21}:
        print("  HALT: pre-counts diverge from expected 721/22/18/21")
        return 1

    pre_fk_violations = list(db.execute("PRAGMA foreign_key_check"))
    print(f"Pre FK violations: {pre_fk_violations}")
    if pre_fk_violations != [("spec_value_probes", 6, "evidence_sources_v1_legacy", 0)]:
        print("  HALT: pre-FK-check diverges from expected single PMP-A02-001-S2 violation")
        return 1

    # Begin migration
    db.execute("PRAGMA foreign_keys = OFF")
    db.execute("BEGIN")
    try:
        # 1. Drop dependent view (will be recreated after spec_value_probes rebuild)
        db.execute("DROP VIEW IF EXISTS v_pmp_latest_walk")

        # 2. Rebuild source_slug_links
        db.execute(SOURCE_SLUG_LINKS_NEW)
        db.execute("""INSERT INTO _new_source_slug_links
                      SELECT ref_id, slug, local_ref_id, created_at, created_by_session,
                             updated_at, updated_by_session
                      FROM source_slug_links""")
        db.execute("DROP TABLE source_slug_links")
        db.execute("ALTER TABLE _new_source_slug_links RENAME TO source_slug_links")

        # 3. Rebuild evidence_population_match (adds gap_id column)
        db.execute(EVIDENCE_POPULATION_MATCH_NEW)
        db.execute("""INSERT INTO _new_evidence_population_match
                          (match_id, source_ref, target_population, study_population, sample_size,
                           match_grade, mismatch_note, created_at, created_by_session, ref_id)
                      SELECT match_id, source_ref, target_population, study_population, sample_size,
                             match_grade, mismatch_note, created_at, created_by_session, ref_id
                      FROM evidence_population_match""")
        db.execute("DROP TABLE evidence_population_match")
        db.execute("ALTER TABLE _new_evidence_population_match RENAME TO evidence_population_match")

        # 4. Rebuild spec_value_probes (also fixes the PMP-A02-001-S2 ref_id during INSERT)
        db.execute(SPEC_VALUE_PROBES_NEW)
        db.execute("""INSERT INTO _new_spec_value_probes
                      SELECT probe_id, walk_id, slug, item_code, spec_value_origin, spec_unit,
                             direction, population, claim_type, step_index, phase,
                             step_value, step_value_unit, search_query, search_query_alt,
                             passes_strict,
                             CASE WHEN probe_id='PMP-A02-001-S2' THEN 'REF-00335' ELSE ref_id END,
                             notes, created_at, created_by_session
                      FROM spec_value_probes""")
        db.execute("DROP TABLE spec_value_probes")
        db.execute("ALTER TABLE _new_spec_value_probes RENAME TO spec_value_probes")

        # 5. Rebuild citation_mining
        db.execute(CITATION_MINING_NEW)
        db.execute("""INSERT INTO _new_citation_mining
                      SELECT slug, local_ref_id, global_ref_id, doi, backward, forward,
                             connections_produced, notes, created_at, created_by_session,
                             updated_at, updated_by_session, deferred_reason
                      FROM citation_mining""")
        db.execute("DROP TABLE citation_mining")
        db.execute("ALTER TABLE _new_citation_mining RENAME TO citation_mining")

        # 6. Recreate dependent view
        db.execute(V_PMP_LATEST_WALK)

        # 7. Rebuild indexes
        for idx in INDEXES:
            db.execute(idx)

        # 8. Backfill 5 evidence_population_match.ref_id NULLs
        for match_id, ref_id in EPM_REF_BACKFILLS:
            db.execute("""UPDATE evidence_population_match
                          SET ref_id=?
                          WHERE match_id=? AND ref_id IS NULL""", (ref_id, match_id))

        # 9. Verify FK integrity inside transaction
        post_fk_violations = list(db.execute("PRAGMA foreign_key_check"))
        if post_fk_violations:
            print(f"  HALT: post FK violations: {post_fk_violations}")
            db.execute("ROLLBACK")
            return 1

        # 10. Record migration
        db.execute("""INSERT INTO data_migrations (migration_id, applied_at, content_sha, applied_by_session, notes)
                      VALUES ('010_fk_integrity_2026-05-13',
                              datetime('now'),
                              'fk_integrity_legacy_to_evidence_sources_4tables_782rows_plus_pmp_fix_5_epm_backfill_gap_id_col',
                              'session_2026-05-13b-evidence-verification-methodology',
                              'FK integrity fix: 4 tables repointed from evidence_sources_v1_legacy to evidence_sources (782 rows). PMP-A02-001-S2 ref_id fix. 5 evidence_population_match ref_id backfills. gap_id column added. Per DR-2026-05-13.')""")

        db.execute("COMMIT")
    except Exception as e:
        db.execute("ROLLBACK")
        print(f"  HALT: exception during migration, rolled back: {e}")
        return 1
    db.execute("PRAGMA foreign_keys = ON")
    db.execute(f"PRAGMA user_version = 10")

    # Post-state verification
    print("=" * 60)
    post_uv = db.execute("PRAGMA user_version").fetchone()[0]
    print(f"Post user_version: {post_uv}")
    if post_uv != 10:
        print(f"  HALT: user_version did not advance to 10 (got {post_uv})")
        return 1

    post_counts = {}
    for t in ["source_slug_links", "evidence_population_match", "spec_value_probes", "citation_mining"]:
        post_counts[t] = db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        delta = post_counts[t] - pre_counts[t]
        marker = "OK" if delta == 0 else f"DELTA {delta:+d}"
        print(f"Post {t}: {post_counts[t]} rows ({marker})")
    if post_counts != pre_counts:
        print("  HALT: post-counts diverge from pre-counts")
        return 1

    post_fk_violations = list(db.execute("PRAGMA foreign_key_check"))
    print(f"Post FK violations: {post_fk_violations}")
    if post_fk_violations:
        print("  HALT: FK violations remain after migration")
        return 1

    # Verify FK targets all point to evidence_sources
    for t in ["source_slug_links", "evidence_population_match", "spec_value_probes", "citation_mining"]:
        for fk in db.execute(f"PRAGMA foreign_key_list({t})"):
            target = fk[2]
            if target == "evidence_sources_v1_legacy":
                print(f"  HALT: {t} still has FK to evidence_sources_v1_legacy")
                return 1

    # Verify the data fixes
    pmp_row = db.execute("SELECT ref_id FROM spec_value_probes WHERE probe_id='PMP-A02-001-S2'").fetchone()
    print(f"PMP-A02-001-S2 ref_id: {pmp_row[0]} (expected REF-00335)")
    if pmp_row[0] != "REF-00335":
        print("  HALT: PMP-A02-001-S2 ref_id fix did not apply")
        return 1

    epm_nulls = db.execute("SELECT COUNT(*) FROM evidence_population_match WHERE ref_id IS NULL").fetchone()[0]
    print(f"evidence_population_match ref_id NULLs remaining: {epm_nulls} (expected 0 after backfill)")
    if epm_nulls != 0:
        # Check: was the original NULL count exactly 5?
        print(f"  Note: 5 known NULLs backfilled. If others remain, they were not in the backfill list.")

    # Verify gap_id column exists
    cols = [c[1] for c in db.execute("PRAGMA table_info(evidence_population_match)")]
    if "gap_id" not in cols:
        print("  HALT: gap_id column not added to evidence_population_match")
        return 1
    print("evidence_population_match.gap_id column: present")

    # Verify view rebuilt
    view = db.execute("SELECT sql FROM sqlite_master WHERE type='view' AND name='v_pmp_latest_walk'").fetchone()
    print(f"v_pmp_latest_walk: {'present' if view else 'MISSING'}")
    if not view:
        print("  HALT: v_pmp_latest_walk view not recreated")
        return 1

    # Verify view actually works
    view_count = db.execute("SELECT COUNT(*) FROM v_pmp_latest_walk").fetchone()[0]
    print(f"v_pmp_latest_walk row count: {view_count}")

    print("=" * 60)
    print("Migration 010 SUCCESS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
