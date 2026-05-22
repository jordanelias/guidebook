#!/usr/bin/env python3
"""
DB integrity test — scripts/tests/test_db_integrity.py
=======================================================
Runs against data/guidebook.db (or GUIDEBOOK_DB_PATH). Designed for CI:
exits 0 on clean, 1 on any failure.

Checks performed:
  A — Foreign key referential integrity (all declared relationships)
  B — Enum column constraint validation (verification_status, metadata_quality,
      doi_resolution_outcome, url_resolution_outcome, source_type)
  C — Consistency invariants (VERIFIED audit trail, pre-pipeline backfill,
      COMPLETE criteria, run record completeness)
  D — Duplicate / collision detection (duplicate DOIs excluding known intentional
      triples, duplicate ref_ids across tables)
  E — Schema contract (required columns present, migration log non-empty,
      PRAGMA foreign_keys honoured)
  F — Pipeline run health (no regressions, all started runs completed)
  G — Evidence chain integrity (source_slug_links → evidence_sources → authors)

Run:
  python scripts/tests/test_db_integrity.py
  python scripts/tests/test_db_integrity.py --db path/to/guidebook.db
"""

import sys
import os
import sqlite3
import argparse

DB_PATH = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")

results = []

def record(tid, name, passed, detail=""):
    results.append({"id": tid, "name": name, "passed": passed})
    sym = "✓" if passed else "✗"
    print(f"  [{sym}] {tid}: {name}")
    if not passed and detail:
        print(f"      {detail}")


def run_checks(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    # ── A: Foreign key referential integrity ─────────────────────────────────
    print("\n[A] Foreign key referential integrity")

    record("A01", "source_slug_links → evidence_sources",
        conn.execute("""SELECT COUNT(*) FROM source_slug_links l
            WHERE NOT EXISTS (SELECT 1 FROM evidence_sources e WHERE e.ref_id=l.ref_id)
        """).fetchone()[0] == 0)

    record("A02", "item_population_links → items",
        conn.execute("""SELECT COUNT(*) FROM item_population_links l
            WHERE NOT EXISTS (SELECT 1 FROM items i WHERE i.item_code=l.item_code)
        """).fetchone()[0] == 0)

    record("A03", "item_population_links → populations",
        conn.execute("""SELECT COUNT(*) FROM item_population_links l
            WHERE NOT EXISTS (SELECT 1 FROM populations p WHERE p.population_code=l.population_code)
        """).fetchone()[0] == 0)

    record("A04", "spec_value_probes → items",
        conn.execute("""SELECT COUNT(*) FROM spec_value_probes p
            WHERE NOT EXISTS (SELECT 1 FROM items i WHERE i.item_code=p.item_code)
        """).fetchone()[0] == 0)

    record("A05", "evidence_population_match → evidence_sources",
        conn.execute("""SELECT COUNT(*) FROM evidence_population_match m
            WHERE ref_id IS NOT NULL
            AND NOT EXISTS (SELECT 1 FROM evidence_sources e WHERE e.ref_id=m.ref_id)
        """).fetchone()[0] == 0)

    record("A06", "bpc_metadata → slugs",
        conn.execute("""SELECT COUNT(*) FROM bpc_metadata b
            WHERE NOT EXISTS (SELECT 1 FROM slugs s WHERE s.slug=b.slug)
        """).fetchone()[0] == 0)

    record("A07", "citation_mining global_ref_id → source_slug_links",
        conn.execute("""SELECT COUNT(*) FROM citation_mining c
            WHERE global_ref_id IS NOT NULL
            AND NOT EXISTS (SELECT 1 FROM source_slug_links l WHERE l.ref_id=c.global_ref_id)
        """).fetchone()[0] == 0)

    record("A08", "item_population_elaborations → items",
        conn.execute("""SELECT COUNT(*) FROM item_population_elaborations e
            WHERE NOT EXISTS (SELECT 1 FROM items i WHERE i.item_code=e.item_code)
        """).fetchone()[0] == 0)

    # ── B: Enum validation ────────────────────────────────────────────────────
    print("\n[B] Enum column validation")

    VALID_VSTATUS = ("VERIFIED","UNVERIFIED-1","UNVERIFIED-CLOSED",
                     "PROBABILISTIC","CO1-VERIFIED",
                     # V1 state machine §4 (verification-pipeline-proposal-2026-05-12-v2):
                     "NO-MATCH","NEEDS-HUMAN","SUPERSEDED","REVERTED",
                     # DR-2026-05-19 amendment 2026-05-19 — manual-track explicit-cause states:
                     "IS-PAYWALL","DEFERRED-V2-AUTOMATED")
    bad = conn.execute(f"""SELECT COUNT(*) FROM evidence_sources
        WHERE verification_status IS NOT NULL
        AND verification_status NOT IN ({','.join('?'*len(VALID_VSTATUS))})
    """, VALID_VSTATUS).fetchone()[0]
    record("B01", "verification_status values", bad == 0,
           f"{bad} invalid values" if bad else "")

    VALID_MQ = ("COMPLETE","AUTHOR-TITLE-ONLY","GREY","PMID-ONLY","NULL",
                # DR-2026-05-18 — statutory metadata completeness:
                "COMPLETE-STATUTORY")
    bad = conn.execute(f"""SELECT COUNT(*) FROM evidence_sources
        WHERE metadata_quality IS NOT NULL
        AND metadata_quality NOT IN ({','.join('?'*len(VALID_MQ))})
    """, VALID_MQ).fetchone()[0]
    record("B02", "metadata_quality values", bad == 0,
           f"{bad} invalid values" if bad else "")

    VALID_DOI_OUT = ("RESOLVED","NO-MATCH","REVERTED")
    bad = conn.execute(f"""SELECT COUNT(*) FROM evidence_sources
        WHERE doi_resolution_outcome IS NOT NULL
        AND doi_resolution_outcome NOT IN ({','.join('?'*len(VALID_DOI_OUT))})
    """, VALID_DOI_OUT).fetchone()[0]
    record("B03", "doi_resolution_outcome values", bad == 0,
           f"{bad} invalid values" if bad else "")

    # Two URL-resolution vocabularies coexist:
    #   - granular pipeline outputs from scripts/url_verifier.py
    #     (MATCHED/PARTIAL/NO-MATCH/DEAD-LINK/DEAD-DNS/WAYBACK-*/URL-NO-MATCH)
    #   - simpler DOI-resolver/url-fetch outputs that pre-date the granular
    #     pipeline and align with B03's doi_resolution_outcome vocabulary
    #     (RESOLVED/DEAD/RESOLVED-PARTIAL). RESOLVED is the same value B03 uses.
    # The two vocabularies are NOT equivalent (MATCHED implies title-match
    # check; RESOLVED does not), so they are accepted as parallel valid sets
    # rather than merged.
    VALID_URL_OUT = ("MATCHED","PARTIAL","NO-MATCH","DEAD-LINK","DEAD-DNS",
                     "WAYBACK-MATCH","WAYBACK-PARTIAL","URL-NO-MATCH",
                     "RESOLVED","DEAD","RESOLVED-PARTIAL")
    bad = conn.execute(f"""SELECT COUNT(*) FROM evidence_sources
        WHERE url_resolution_outcome IS NOT NULL
        AND url_resolution_outcome NOT IN ({','.join('?'*len(VALID_URL_OUT))})
    """, VALID_URL_OUT).fetchone()[0]
    record("B04", "url_resolution_outcome values", bad == 0,
           f"{bad} invalid values" if bad else "")

    VALID_ST = ("journal_article","book","book_chapter","conference_paper","thesis",
                "primary_research","case_study","standard","guideline","report",
                "grey","internal","letter","editorial","commentary","other")
    bad = conn.execute(f"""SELECT COUNT(*) FROM evidence_sources
        WHERE source_type IS NOT NULL
        AND source_type NOT IN ({','.join('?'*len(VALID_ST))})
    """, VALID_ST).fetchone()[0]
    record("B05", "source_type values", bad == 0,
           f"{bad} invalid values" if bad else "")

    VALID_GAP_STATUS = ("OPEN","IN-PROGRESS","CLOSED-FIXED","CLOSED-RESOLVED",
                         "CLOSED-DELETED","BLOCKED","P1",
                         "CLOSED-SYSTEMIC","CLOSED-SYNC","CLOSED-FALSE-POSITIVE")
    bad = conn.execute(f"""SELECT COUNT(*) FROM gaps
        WHERE status NOT IN ({','.join('?'*len(VALID_GAP_STATUS))})
    """, VALID_GAP_STATUS).fetchone()[0]
    record("B06", "gaps.status values", bad == 0,
           f"{bad} invalid values" if bad else "")

    # ── C: Consistency invariants ─────────────────────────────────────────────
    print("\n[C] Consistency invariants")

    # Every VERIFIED row must have an audit trail
    mystery = conn.execute("""SELECT COUNT(*) FROM evidence_sources
        WHERE verification_status = 'VERIFIED'
        AND (doi IS NULL OR doi = '')
        AND (url IS NULL OR url = '')
        AND (pmid IS NULL OR pmid = '')
        AND (verified_by_tool IS NULL OR verified_by_tool = '')
    """).fetchone()[0]
    record("C01", "VERIFIED rows all have an audit trail (doi/url/pmid or verified_by_tool)",
           mystery == 0,
           f"{mystery} rows VERIFIED with no audit trail — run backfill migration" if mystery else "")

    # All pre-pipeline DOIs have been backfilled
    orphan_doi = conn.execute("""SELECT COUNT(*) FROM evidence_sources
        WHERE doi IS NOT NULL AND doi != '' AND doi_resolution_outcome IS NULL
    """).fetchone()[0]
    record("C02", "All DOI rows have doi_resolution_outcome set (pre-pipeline backfill applied)",
           orphan_doi == 0,
           f"{orphan_doi} rows — run: UPDATE evidence_sources SET doi_resolution_outcome='RESOLVED' "
           "WHERE doi IS NOT NULL AND doi_resolution_outcome IS NULL" if orphan_doi else "")

    # COMPLETE rows have author
    bad_complete = conn.execute("""SELECT COUNT(*) FROM evidence_sources
        WHERE metadata_quality = 'COMPLETE'
        AND (first_author_last IS NULL OR first_author_last = '')
        AND (is_corporate_primary IS NULL OR is_corporate_primary = 0)
    """).fetchone()[0]
    record("C03", "COMPLETE rows all have author (first_author_last or is_corporate_primary)",
           bad_complete == 0,
           f"{bad_complete} COMPLETE rows lack author" if bad_complete else "")

    # COMPLETE rows have doi UNLESS they were Co-1 manually verified
    # (REF-VERIFIED-* rows are human-verified standards that predate the DOI pipeline)
    bad_complete_doi = conn.execute("""SELECT COUNT(*) FROM evidence_sources
        WHERE metadata_quality = 'COMPLETE'
        AND (doi IS NULL OR doi = '')
        AND (verified_by_tool IS NULL OR verified_by_tool NOT LIKE 'co1%')
        AND (doi_resolution_outcome IS NULL OR doi_resolution_outcome = 'RESOLVED')
    """).fetchone()[0]
    record("C04", "COMPLETE rows: either have doi, or co1-verified, or NO-MATCH on record",
           bad_complete_doi == 0,
           f"{bad_complete_doi} COMPLETE rows lack doi with no acceptable explanation" if bad_complete_doi else "")

    # legacy/v2 row count parity — only when legacy table still exists
    has_legacy = conn.execute("""SELECT COUNT(*) FROM sqlite_master
        WHERE type='table' AND name='evidence_sources_v1_legacy'""").fetchone()[0]
    if has_legacy:
        v1 = conn.execute("SELECT COUNT(*) FROM evidence_sources_v1_legacy").fetchone()[0]
        v2 = conn.execute("SELECT COUNT(*) FROM evidence_sources").fetchone()[0]
        record("C05", f"evidence_sources row count matches v1_legacy ({v2} == {v1})",
               v1 == v2,
               f"v1={v1} v2={v2} — {abs(v2-v1)} row delta (new rows added since cutover are expected)" if v1 != v2 else "")
    else:
        record("C05", "v1_legacy parity (table dropped, check skipped)", True)

    # ── D: Duplicate / collision detection ───────────────────────────────────
    print("\n[D] Duplicate and collision detection")

    # Duplicate DOIs — with known exception documented
    # Documented intentional duplicates — same paper cited in multiple BPCs
    # under different scope descriptions. Linked via bpc_note / superseded_by_ref_id.
    # To add a new exception:
    #   1. Verify in the DB the duplicate is intentional (different bpc_shorthand /
    #      bpc_note describing distinct scope claims on the same source).
    #   2. Add a `data_migrations` row documenting WHY it's intentional.
    #   3. Add the DOI to the tuple below.
    # When `superseded_by_ref_id` linkage is added across all these, the tuple
    # should be reduced and the check rewritten to use that column instead.
    KNOWN_DUP_DOIS = (
        "10.31030/2853913",           # IEC 60118-4 — 3 scope citations (hearing loops)
        "10.31030/1803049",           # DIN 18040-2 — 5 distinct-section citations (residential accessibility): visitability / reach range / bathroom-laundry-kitchen / entry / threshold
        "10.31030/1715500",           # DIN 18040-1 — 3 distinct-section citations (public buildings): induction loops / circulation geometry / door hardware
        "10.1016/S0140-6736(14)61006-0",  # HIPI study — 2 BPC citations (falls + lighting)
        "10.1016/j.buildenv.2021.108352",  # Inclusive design failures — 2 BPCs
        "10.1016/j.dhjo.2022.101281", # Accessible design features — 2 BPCs
        "10.1044/2022_LSHSS-21-00181", # Speech intelligibility SR — 2 BPCs
        "10.1080/10400430903496580",   # Wheeled mobility dimensions — 2 BPCs
        "10.1136/bmjopen-2020-046647", # MHIPI study — 2 BPCs
        "10.1177/13623613221102753",   # Autism built environment — 2 BPCs
        "10.1177/1533317509334959",    # Dementia-friendly architecture — 2 BPCs
        "10.1177/193758671100400207",  # EADDAT validation — 2 BPCs
        "10.1371/journal.pone.0269657", # Wheelchair biomechanics — 2 BPCs
        "10.2196/69442",              # Grab bar / bathroom safety — 2 BPCs
        "10.3389/fpsyt.2021.727353",  # ASPECTSS design index — 4 BPCs (autism)
        "10.4324/9781003564164",      # Inclusive Housing Design Guide — 3 BPCs
        "10.1016/j.mayocp.2021.07.004", # Bateman et al. ME/CFS Essentials — 4 BPCs (cool environment / sensory / PEM management / post-COVID)
        "10.3390/ijerph192114279",     # Owen & Crane 2022 TID scoping review — 2 BPCs (REF-00090 + REF-00527; Crane first name mismatch in queue)
        "10.1177/1937586717730338", # Lee 2018 HERD Beyond ADA — 2 BPCs (REF-00033 + REF-00034)
        "10.3389/frdem.2025.1524425", # van Buuren 2025 Frontiers in Dementia wayfinding — 2 BPCs (REF-00488 + REF-00520)
    )
    dup_rows = conn.execute(f"""
        SELECT doi, COUNT(*) AS n FROM evidence_sources
        WHERE doi IS NOT NULL AND doi != ''
        AND doi_resolution_outcome != 'REVERTED'
        AND doi NOT IN ({','.join('?'*len(KNOWN_DUP_DOIS))})
        GROUP BY doi HAVING COUNT(*) > 1
    """, KNOWN_DUP_DOIS).fetchall()
    record("D01", f"No unexpected duplicate DOIs (known IEC 60118-4 triple excluded)",
           len(dup_rows) == 0,
           f"{len(dup_rows)} unexpected duplicates: {[dict(r) for r in dup_rows]}" if dup_rows else "")

    # Duplicate ref_ids across evidence_sources and legacy (should be same set)
    if has_legacy:
        refs_v2 = {r[0] for r in conn.execute("SELECT ref_id FROM evidence_sources")}
        refs_v1 = {r[0] for r in conn.execute("SELECT ref_id FROM evidence_sources_v1_legacy")}
        only_v2 = refs_v2 - refs_v1
        only_v1 = refs_v1 - refs_v2
        record("D02", "evidence_sources and v1_legacy have matching ref_id sets",
               len(only_v2) == 0 and len(only_v1) == 0,
               f"only in v2: {list(only_v2)[:5]}; only in v1: {list(only_v1)[:5]}" if (only_v2 or only_v1) else "")
    else:
        record("D02", "v1_legacy ref_id parity (table dropped, check skipped)", True)

    # Duplicate slugs in bpc_metadata
    dup_slugs = conn.execute("""SELECT slug, COUNT(*) FROM bpc_metadata
        GROUP BY slug HAVING COUNT(*) > 1""").fetchall()
    record("D03", "No duplicate slugs in bpc_metadata",
           len(dup_slugs) == 0,
           f"duplicates: {[dict(r) for r in dup_slugs]}" if dup_slugs else "")

    # ── E: Schema contract ────────────────────────────────────────────────────
    print("\n[E] Schema contract")

    # Required columns present in evidence_sources
    es_cols = {r[1] for r in conn.execute("PRAGMA table_info(evidence_sources)")}
    required_cols = {
        "ref_id", "doi", "pmid", "pmcid", "url", "pub_title", "pub_year",
        "verification_status", "metadata_quality", "doi_resolution_outcome",
        "url_resolution_outcome", "verified_by_tool", "last_verified_at",
        "verification_attempt_count", "pages", "pub_month", "language",
        "subtype", "citation_count", "url_last_fetched", "url_match_similarity",
    }
    missing_cols = required_cols - es_cols
    record("E01", f"evidence_sources has all required columns ({len(required_cols)} checked)",
           len(missing_cols) == 0,
           f"missing: {missing_cols}" if missing_cols else "")

    # pipeline_runs has Phase 4 columns
    pr_cols = {r[1] for r in conn.execute("PRAGMA table_info(pipeline_runs)")}
    p4_required = {"phase_4_enriched", "phase_4_complete", "phase_4_transient",
                   "metadata_complete_before", "metadata_complete_after"}
    missing_p4 = p4_required - pr_cols
    record("E02", "pipeline_runs has Phase 4 tracking columns",
           len(missing_p4) == 0,
           f"missing: {missing_p4}" if missing_p4 else "")

    # url_verification_runs table exists
    has_uvr = conn.execute("""SELECT COUNT(*) FROM sqlite_master
        WHERE type='table' AND name='url_verification_runs'""").fetchone()[0]
    record("E03", "url_verification_runs table exists",
           has_uvr == 1)

    # data_migrations is non-empty
    n_mig = conn.execute("SELECT COUNT(*) FROM data_migrations").fetchone()[0]
    record("E04", f"data_migrations log non-empty ({n_mig} entries)",
           n_mig > 0)

    # Backfill migrations have been applied
    backfills = {r[0] for r in conn.execute(
        "SELECT migration_id FROM data_migrations WHERE migration_id LIKE '%backfill%'")}
    required_backfills = {
        "doi_resolution_outcome_backfill_2026-05-12",
        "verified_by_tool_backfill_2026-05-12",
    }
    missing_bfills = required_backfills - backfills
    record("E05", "Required backfill migrations recorded",
           len(missing_bfills) == 0,
           f"missing migration records: {missing_bfills}" if missing_bfills else "")

    # SQLite integrity check
    ic = conn.execute("PRAGMA integrity_check").fetchone()[0]
    record("E06", "SQLite PRAGMA integrity_check = ok",
           ic == "ok",
           f"integrity_check: {ic}" if ic != "ok" else "")

    # ── F: Pipeline run health ────────────────────────────────────────────────
    print("\n[F] Pipeline run health")

    # No DOI regressions across runs
    regressions = conn.execute("""SELECT COUNT(*) FROM pipeline_runs
        WHERE doi_after IS NOT NULL AND doi_before IS NOT NULL
        AND doi_after < doi_before""").fetchone()[0]
    record("F01", "No DOI regressions in pipeline_runs",
           regressions == 0,
           f"{regressions} runs show doi_after < doi_before" if regressions else "")

    # All runs have completed_at set
    incomplete = conn.execute("""SELECT COUNT(*) FROM pipeline_runs
        WHERE completed_at IS NULL""").fetchone()[0]
    record("F02", "All pipeline_runs have completed_at set",
           incomplete == 0,
           f"{incomplete} runs missing completed_at (interrupted?)" if incomplete else "")

    # All URL runs have completed_at set
    incomplete_url = conn.execute("""SELECT COUNT(*) FROM url_verification_runs
        WHERE completed_at IS NULL""").fetchone()[0]
    record("F03", "All url_verification_runs have completed_at set",
           incomplete_url == 0,
           f"{incomplete_url} url runs missing completed_at" if incomplete_url else "")

    # No VERIFIED regressions (verified_after should be >= verified_before per run)
    ver_regression = conn.execute("""SELECT COUNT(*) FROM pipeline_runs
        WHERE verified_after IS NOT NULL AND verified_before IS NOT NULL
        AND verified_after < verified_before""").fetchone()[0]
    record("F04", "No VERIFIED count regressions in pipeline_runs",
           ver_regression == 0,
           f"{ver_regression} runs show verified_after < verified_before" if ver_regression else "")

    # ── G: Evidence chain integrity ───────────────────────────────────────────
    print("\n[G] Evidence chain integrity")

    # evidence_source_authors ref_ids all exist in evidence_sources
    orphan_authors = conn.execute("""SELECT COUNT(*) FROM evidence_source_authors a
        WHERE NOT EXISTS (SELECT 1 FROM evidence_sources e WHERE e.ref_id=a.ref_id)
    """).fetchone()[0]
    record("G01", "evidence_source_authors → evidence_sources (no orphan author rows)",
           orphan_authors == 0,
           f"{orphan_authors} orphan author rows" if orphan_authors else "")

    # Every source marked COMPLETE has ≥1 author row in evidence_source_authors
    # OR is_corporate_primary=1 (which doesn't need individual author rows)
    complete_no_author = conn.execute("""
        SELECT COUNT(*) FROM evidence_sources e
        WHERE e.metadata_quality = 'COMPLETE'
        AND e.is_corporate_primary = 0
        AND NOT EXISTS (SELECT 1 FROM evidence_source_authors a WHERE a.ref_id = e.ref_id)
    """).fetchone()[0]
    record("G02", "COMPLETE person-authored sources have ≥1 author row",
           complete_no_author == 0,
           f"{complete_no_author} COMPLETE sources missing author rows" if complete_no_author else "")

    # ORCID format: should be 0000-0000-0000-0000 (no URL prefix)
    bad_orcid = conn.execute("""SELECT COUNT(*) FROM evidence_source_authors
        WHERE orcid IS NOT NULL AND orcid != ''
        AND (orcid LIKE 'http%' OR orcid LIKE 'orcid.org%')
    """).fetchone()[0]
    record("G03", "ORCID values stored as plain identifier (no URL prefix)",
           bad_orcid == 0,
           f"{bad_orcid} ORCIDs with URL prefix — strip 'https://orcid.org/'" if bad_orcid else "")

    # ── Summary ───────────────────────────────────────────────────────────────
    conn.close()
    print("\n" + "=" * 70)
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = [r for r in results if not r["passed"]]
    print(f"RESULTS: {passed}/{total} checks passed")
    if failed:
        print("FAILED:")
        for r in failed:
            print(f"  [{r['id']}] {r['name']}")
    print("=" * 70)
    return 0 if not failed else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=DB_PATH)
    args = parser.parse_args()
    sys.exit(run_checks(args.db))
