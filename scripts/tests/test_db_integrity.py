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
      triples, duplicate ref_ids across tables, and the DOI-less half: sources
      colliding on author+year+title, plus sources with no computable key at all)
  E — Schema contract (required columns present, migration log non-empty,
      PRAGMA foreign_keys honoured)
  F — Pipeline run health (no regressions, all started runs completed)
  G — Evidence chain integrity (source_slug_links → evidence_sources → authors)
  H — JSON-array ↔ junction parity (cell_source_links, search_admissions), held
      in both directions while the JSON columns await their caller sweep
  I — D-0157 verification-standing invariants (status × disposition × method ×
      attempt count)

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

    # A09 stands in for a foreign key that migration 039 deliberately did NOT
    # declare. Every other soft edge in that migration became a real FK; this
    # one would have required rebuilding evidence_sources — 88 columns, 9
    # inbound FKs — to protect 44 values, and hand-transcribing a definition
    # that size is how a rebuild silently changes a type or a CHECK. The
    # constraint is traded for this check; if evidence_sources is ever rebuilt
    # for another reason, declare the FK and delete this.
    record("A09", "evidence_sources.superseded_by_ref_id → evidence_sources",
        conn.execute("""SELECT COUNT(*) FROM evidence_sources s
            WHERE s.superseded_by_ref_id IS NOT NULL
            AND s.superseded_by_ref_id <> ''
            AND NOT EXISTS (SELECT 1 FROM evidence_sources e
                            WHERE e.ref_id = s.superseded_by_ref_id)
        """).fetchone()[0] == 0)

    # The two normalised edge junctions (migrations 044, 050). Their FKs are
    # declared, but a declared FK only binds writes made with
    # PRAGMA foreign_keys=ON — it does not retroactively validate rows already
    # in the file, and section H's parity checks compare each junction against
    # its JSON column, not against the tables the ids point at. A ref present in
    # BOTH stores but absent from evidence_sources would pass every H check.
    for tid, junction, col, parent, pcol in (
        ("A10", "cell_source_links",  "cell_id", "evidence_cell_state", "cell_id"),
        ("A11", "cell_source_links",  "ref_id",  "evidence_sources",    "ref_id"),
        ("A12", "search_admissions",  "exec_id", "search_executions",   "exec_id"),
        ("A13", "search_admissions",  "ref_id",  "evidence_sources",    "ref_id"),
    ):
        n = conn.execute(f"""SELECT COUNT(*) FROM {junction} j
            WHERE NOT EXISTS (SELECT 1 FROM {parent} p WHERE p.{pcol} = j.{col})
        """).fetchone()[0]
        record(tid, f"{junction}.{col} → {parent}", n == 0,
               f"{n} rows pointing at a {parent} row that does not exist" if n else "")

    # ── B: Enum validation ────────────────────────────────────────────────────
    print("\n[B] Enum column validation")

    # D-0157 (ADOPTED 2026-08-04): the standing is BINARY. How it was
    # established lives in verification_method, whether more effort is owed in
    # verification_disposition, and how much was spent in
    # verification_attempt_count. Every value this list used to carry was one of
    # those three facts smuggled into the status string -- and UNVERIFIED-1
    # asserted an attempt count its own column contradicted in 25 of 31 rows.
    VALID_VSTATUS = ("VERIFIED", "UNVERIFIED")
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
                "grey","internal","letter","editorial","commentary","other",
                # D-0157 section 4.6 ratifies `code`: 16 rows, statutory
                # instruments (French arretes, Italian DPCM, Japanese ministerial
                # standards), mirroring EvidenceType.CODE in schemas/enums.py.
                # Used consistently since coinage; the transcription here was
                # simply never updated.
                "code")
    bad = conn.execute(f"""SELECT COUNT(*) FROM evidence_sources
        WHERE source_type IS NOT NULL
        AND source_type NOT IN ({','.join('?'*len(VALID_ST))})
    """, VALID_ST).fetchone()[0]
    record("B05", "source_type values", bad == 0,
           f"{bad} invalid values" if bad else "")

    VALID_GAP_STATUS = ("OPEN","IN-PROGRESS","CLOSED-FIXED","CLOSED-RESOLVED",
                         "CLOSED-DELETED","BLOCKED","P1",
                         "CLOSED-SYSTEMIC","CLOSED-SYNC","CLOSED-FALSE-POSITIVE",
                         # 2026-08-03: written by the owner-approved DR-2026-07-20
                         # migration (data_20260720135718_...sql:18,34), which closes a
                         # gap by *deciding* it rather than fixing or deleting it.
                         "CLOSED-DECIDED")
    bad = conn.execute(f"""SELECT COUNT(*) FROM gaps
        WHERE status NOT IN ({','.join('?'*len(VALID_GAP_STATUS))})
    """, VALID_GAP_STATUS).fetchone()[0]
    record("B06", "gaps.status values", bad == 0,
           f"{bad} invalid values" if bad else "")

    # ── D-0157 standing invariants (I1–I4) ────────────────────────────────────
    # The point of splitting one column into three is that they can now be
    # checked against each other. Each of these was unprovable while the claim
    # and its evidence were the same string.
    # NULL disposition is the hole a newly inserted row falls through, so the
    # test is "not CLOSED", not "is OPEN".
    i1 = conn.execute("""SELECT COUNT(*) FROM evidence_sources
        WHERE verification_status='VERIFIED'
          AND COALESCE(verification_disposition,'') <> 'CLOSED'""").fetchone()[0]
    record("I1", "no source is VERIFIED with effort still owed", i1 == 0,
           f"{i1} rows VERIFIED without a CLOSED disposition — verification is "
           f"finished or it did not happen" if i1 else "")

    i2 = conn.execute("""SELECT COUNT(*) FROM evidence_sources
        WHERE verification_status='VERIFIED'
          AND COALESCE(verification_attempt_count,0)=0""").fetchone()[0]
    record("I2", "a VERIFIED source records at least one attempt", i2 == 0,
           f"{i2} rows VERIFIED with zero attempts — nobody recorded doing the thing "
           f"that verified them; adjudication queue, not a backfill" if i2 else "")

    i3 = conn.execute("""SELECT COUNT(*) FROM evidence_sources
        WHERE verification_disposition='CLOSED'
          AND COALESCE(verification_status,'') <> 'VERIFIED'
          AND COALESCE(verification_closure_reason,'') = ''""").fetchone()[0]
    record("I3", "closure is earned and reasoned", i3 == 0,
           f"{i3} rows CLOSED without a closure reason" if i3 else "")

    i3b = conn.execute("""SELECT COUNT(*) FROM evidence_sources
        WHERE verification_disposition='CLOSED'
          AND COALESCE(verification_status,'') <> 'VERIFIED'
          AND COALESCE(verification_attempt_count,0) < 2""").fetchone()[0]
    record("I3b", "closure rests on at least two recorded attempts", i3b == 0,
           f"{i3b} rows CLOSED with fewer than 2 attempts — 'cannot be verified "
           f"after effort spent' requires the effort to be on record" if i3b else "")

    i4 = conn.execute("""SELECT COUNT(*) FROM evidence_sources
        WHERE verification_status='VERIFIED'
          AND verification_method IS NOT NULL
          AND verification_method NOT IN ('direct-render','co1-attestation','tool')""").fetchone()[0]
    record("I4", "VERIFIED is reachable only by a method that obtains the artefact", i4 == 0,
           f"{i4} rows VERIFIED via a method that never obtained the document" if i4 else "")

    i4b = conn.execute("""SELECT COUNT(*) FROM evidence_sources
        WHERE verification_method='tool'
          AND COALESCE(verified_by_tool,'') = ''""").fetchone()[0]
    record("I4b", "method='tool' names the tool that established it", i4b == 0,
           f"{i4b} rows claim a tool established them without naming it" if i4b else "")

    # The three new columns have CHECK constraints in migration 049, but a
    # pre-049 database or a hand-edited blob would not, and B-checks are where
    # vocabulary is enforced in this suite.
    VALID_DISP = ("OPEN", "CLOSED")
    bad = conn.execute(f"""SELECT COUNT(*) FROM evidence_sources
        WHERE verification_disposition IS NOT NULL
        AND verification_disposition NOT IN ({','.join('?'*len(VALID_DISP))})""",
        VALID_DISP).fetchone()[0]
    record("B07", "verification_disposition values", bad == 0,
           f"{bad} invalid values" if bad else "")

    VALID_METH = ("direct-render","co1-attestation","corroborated-not-retrieved",
                  "citing-bibliography","tool")
    bad = conn.execute(f"""SELECT COUNT(*) FROM evidence_sources
        WHERE verification_method IS NOT NULL
        AND verification_method NOT IN ({','.join('?'*len(VALID_METH))})""",
        VALID_METH).fetchone()[0]
    record("B08", "verification_method values", bad == 0,
           f"{bad} invalid values" if bad else "")

    VALID_CR = ("paywalled","print-only","access-denied-persistent","withdrawn",
                "not-found-after-search","disputed-existence")
    bad = conn.execute(f"""SELECT COUNT(*) FROM evidence_sources
        WHERE verification_closure_reason IS NOT NULL
        AND verification_closure_reason NOT IN ({','.join('?'*len(VALID_CR))})""",
        VALID_CR).fetchone()[0]
    record("B09", "verification_closure_reason values", bad == 0,
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

    # C06 — data_capture_status must agree with the joinable evidence tables in
    # BOTH directions. A status that can drift from the rows it summarises is
    # worse than no status: it looks authoritative while being wrong. When W5.4
    # gives jurisdictional_values a ref_id, add it to this predicate AND to the
    # backfill in data_20260802215744.
    CAPTURED = """(EXISTS (SELECT 1 FROM source_value_extractions x WHERE x.ref_id=s.ref_id)
                OR EXISTS (SELECT 1 FROM spec_value_probes p       WHERE p.ref_id=s.ref_id)
                OR EXISTS (SELECT 1 FROM reasoning_doc_citations r WHERE r.source_ref_id=s.ref_id)
                OR EXISTS (SELECT 1 FROM economics_entries e       WHERE e.ref_id=s.ref_id))"""
    claims_not_held = conn.execute(f"""SELECT COUNT(*) FROM evidence_sources s
        WHERE s.data_capture_status='captured' AND NOT {CAPTURED}""").fetchone()[0]
    held_not_claimed = conn.execute(f"""SELECT COUNT(*) FROM evidence_sources s
        WHERE s.data_capture_status<>'captured' AND {CAPTURED}""").fetchone()[0]
    record("C06", "data_capture_status='captured' ⟺ a joinable capture row exists",
           claims_not_held == 0 and held_not_claimed == 0,
           f"{claims_not_held} claim capture with no row; {held_not_claimed} have rows but do not claim it"
           if (claims_not_held or held_not_claimed) else "")

    # C08 — citation_mining_status must agree with citation_mining in both
    # directions, resolving a row to its source the way the table's own primary
    # key does: global_ref_id when present, otherwise (slug, local_ref_id)
    # through source_slug_links.
    #
    # This check exists because its absence cost something. The original
    # backfill joined on global_ref_id alone — NULL in 146 of 183 rows — and
    # left 80 sources reading 'pending' while holding a non-deferred mining
    # row. C06 was written for data_capture_status and had no counterpart
    # here, so nothing contradicted the wrong value. A status column without a
    # biconditional is an assertion nobody checks.
    MINED_SRC = """SELECT COALESCE(m.global_ref_id, l.ref_id) FROM citation_mining m
                   LEFT JOIN source_slug_links l
                     ON l.slug = m.slug AND l.local_ref_id = m.local_ref_id
                   WHERE COALESCE(m.deferred_reason,'') = ''
                     AND COALESCE(m.global_ref_id, l.ref_id) IS NOT NULL"""
    claims_mined = conn.execute(f"""SELECT COUNT(*) FROM evidence_sources
        WHERE citation_mining_status='mined' AND ref_id NOT IN ({MINED_SRC})""").fetchone()[0]
    mined_not_claimed = conn.execute(f"""SELECT COUNT(*) FROM evidence_sources
        WHERE citation_mining_status<>'mined' AND ref_id IN ({MINED_SRC})""").fetchone()[0]
    record("C08", "citation_mining_status='mined' ⟺ a non-deferred mining row resolves to it",
           claims_mined == 0 and mined_not_claimed == 0,
           f"{claims_mined} claim mined with no row; {mined_not_claimed} have a row but do not claim it"
           if (claims_mined or mined_not_claimed) else "")

    # C10 — a published cell may not rest on a source that has not been
    # established as real and usable.
    #
    # CORRECTED 2026-08-02, same day it was written. The first version tested
    # data_capture_status='pending' and failed 13 of 13 cells. That was wrong,
    # and wrong in an instructive way: capture-pending means "no row in an
    # extraction table", NOT "unread". All 59 sources cited by published cells
    # are VERIFIED or DISPUTED with COMPLETE metadata, and every cell carries a
    # convergence_id and tier_basis — they were plainly read. A cell cannot
    # precede the reading that produced it, so a well-formed cell is itself
    # evidence its sources were read, and the first version could only ever
    # have fired on a fabricated cell.
    #
    # Read-ness is recorded in verification_status, not in capture status. That
    # is what this now tests. DISPUTED counts as a failure: a best practice
    # resting on a source whose standing is contested is exactly the case worth
    # surfacing. (The old note here counted 2 DISPUTED among 59; D-0157
    # retired that status and no governing ref has ever been one.)
    # D-0157: a published cell may rest only on a source whose standing is
    # VERIFIED. The old list admitted VERIFIED-2 -- corroborated but never
    # obtained -- as sound; the remap moved those 71 rows to UNVERIFIED, so this
    # narrowing is the same judgement applied consistently rather than a new one.
    OK_VSTATUS = ("VERIFIED",)
    try:
        ph = ",".join("?" * len(OK_VSTATUS))
        unsound = conn.execute(f"""
            SELECT COUNT(DISTINCT c.cell_id)
            FROM evidence_cell_state c
            JOIN json_each(c.governing_refs) j
            JOIN evidence_sources e ON e.ref_id = j.value
            WHERE c.state IN ('stated','provisional')
              AND COALESCE(e.verification_status,'') NOT IN ({ph})""",
            OK_VSTATUS).fetchone()[0]
        total_cells = conn.execute("""SELECT COUNT(*) FROM evidence_cell_state
            WHERE state IN ('stated','provisional')""").fetchone()[0]
        record("C10", "no published cell rests on an unverified or disputed source",
               unsound == 0,
               f"{unsound} of {total_cells} published cells cite a source that is "
               f"not verified (disputed, unverified, or no status)"
               if unsound else "")
    except sqlite3.OperationalError as exc:
        record("C10", "no published cell rests on an unverified or disputed source",
               False, f"could not evaluate: {exc}")

    # C07 — a value column must hold a value, not a state written as prose.
    # This is not hypothetical: '[author surname pending ...]' strings in
    # first_author_last are non-empty, so C03 accepted them as authors and a
    # missing author passed a blocking gate. Unknown belongs in NULL plus a
    # coded status, never in the value field.
    # Guarding one column was not enough: the identical mask survived one column
    # over, on the same rows, in author_display — which is what the vetting
    # surface actually renders. Since migration 041 every one of these has a
    # paired *_note overflow, so prose in the VALUE column is now unambiguously
    # a defect rather than a place-of-last-resort.
    PLACEHOLDER = ("{c} LIKE '[%' OR {c} LIKE '%pending%' OR {c} LIKE '%TBD%' "
                   "OR {c} LIKE '%TBC%' OR {c} LIKE '%unknown (%'")
    VALUE_COLS = [("evidence_sources", "first_author_last"),
                  ("evidence_sources", "author_display"),
                  ("evidence_sources", "publisher"),
                  ("evidence_source_authors", "corporate_name")]
    placeholder, detail = 0, []
    for tbl, col in VALUE_COLS:
        n = conn.execute(f"SELECT COUNT(*) FROM {tbl} WHERE "
                         + PLACEHOLDER.format(c=col)).fetchone()[0]
        placeholder += n
        if n:
            detail.append(f"{tbl}.{col}={n}")
    record("C07", "value columns hold values, not placeholder states",
           placeholder == 0,
           f"{placeholder} rows hold placeholder prose in a value column "
           f"({', '.join(detail)}) — the prose belongs in the paired _note column"
           if placeholder else "")

    # C09 — the states nobody can contradict. C06 binds only 'captured' and C08
    # only 'mined', which leaves every "we looked and decided" state freely
    # assertable: all 852 pending rows could be flipped to 'none-extractable'
    # and the whole suite would still pass. Those are the states most worth
    # lying about, so they are the ones that most need a witness. Migration
    # 040's own DDL promises a reason accompanies them; this enforces it.
    unreasoned = conn.execute("""SELECT COUNT(*) FROM evidence_sources
        WHERE data_capture_status IN ('deferred','none-extractable')
          AND COALESCE(processing_blocked_reason,'') = ''""").fetchone()[0]
    orphan_reason = conn.execute("""SELECT COUNT(*) FROM evidence_sources
        WHERE COALESCE(processing_blocked_reason,'') <> ''
          AND data_capture_status NOT IN ('deferred','none-extractable')
          AND citation_mining_status <> 'deferred'""").fetchone()[0]
    bad_deferred = conn.execute("""SELECT COUNT(*) FROM evidence_sources s
        WHERE s.citation_mining_status='deferred' AND NOT EXISTS (
            SELECT 1 FROM citation_mining m
            LEFT JOIN source_slug_links l
              ON l.slug=m.slug AND l.local_ref_id=m.local_ref_id
            WHERE COALESCE(m.global_ref_id, l.ref_id) = s.ref_id
              AND COALESCE(m.deferred_reason,'') <> '')""").fetchone()[0]
    record("C09", "a 'we looked and stopped' state carries its witness",
           unreasoned == 0 and orphan_reason == 0 and bad_deferred == 0,
           f"{unreasoned} deferred/none-extractable with no coded reason; "
           f"{orphan_reason} reasons attached to a non-stopped state; "
           f"{bad_deferred} claim mining-deferred with no deferred mining row"
           if (unreasoned or orphan_reason or bad_deferred) else "")

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
        "10.1016/j.buildenv.2021.108352",  # Zallio + Clarkson 2021 IDEA — 3 BPCs (REF-00136 + REF-00137 + REF-00171)
        "10.1016/j.dhjo.2022.101281", # Accessible design features — 2 BPCs
        "10.1044/2022_LSHSS-21-00181", # Speech intelligibility SR — 2 BPCs
        "10.1080/10400430903496580",   # Wheeled mobility dimensions — 2 BPCs
        "10.1080/10400430903520280",   # Steinfeld Maisel Feathers D'Souza 2010 Anthropometry+Standards Wheeled Mobility — 2 BPCs (REF-00060 + REF-00192)
        "10.1136/bmjopen-2020-046647", # MHIPI study — 2 BPCs
        "10.1177/13623613221102753",   # Autism built environment — 2 BPCs
        "10.1177/1533317509334959",    # Dementia-friendly architecture — 2 BPCs
        "10.1177/193758671100400207",  # EADDAT validation — 2 BPCs
        "10.1371/journal.pone.0269657", # Wheelchair biomechanics — 2 BPCs
        "10.2196/69442",              # Levine 2025 JMIR R&AT grab bar/bathroom safety — 3 BPCs (REF-00029+00367+00391)
        "10.3389/fpsyt.2021.727353",  # ASPECTSS design index — 4 BPCs (autism)
        "10.4324/9781003564164",      # Inclusive Housing Design Guide — 3 BPCs
        "10.1016/j.mayocp.2021.07.004", # Bateman et al. ME/CFS Essentials — 4 BPCs (cool environment / sensory / PEM management / post-COVID)
        "10.3390/ijerph192114279",     # Owen & Crane 2022 TID scoping review — 2 BPCs (REF-00090 + REF-00527; Crane first name mismatch in queue)
        "10.1016/j.msard.2022.104075", # Christogianni Filingeri 2022 MS heat sensitivity — 2 BPCs (REF-00254 + REF-VERIFIED-010 pre-existing)
        "10.26687/archnet-ijar.v8i1.314", # Mostafa 2014 Archnet-IJAR ARCHITECTURE FOR AUTISM ASPECTSS — 5 BPCs (REF-00051+00129+00517+00592+00724)
        "10.1155/2017/2865960",        # Putthinoi+Lersilp+Chakpitak 2017 J Aging Res Thai elderly — 2 BPCs (REF-00407+REF-00454)
        "10.3233/wor-210997",          # Manandhar 2022 Work LRV preferences VI — 2 BPCs (REF-00393+REF-00530)
        "10.1177/1937586717730338", # Lee 2018 HERD Beyond ADA — 2 BPCs (REF-00033 + REF-00034)
        "10.3389/frdem.2025.1524425", # van Buuren 2025 Frontiers in Dementia wayfinding — 2 BPCs (REF-00488 + REF-00520)
        "10.1016/j.ergon.2014.07.001",  # Kim 2014 IJIE ramp slope wheelchair — 2 BPCs (REF-00030 + REF-00386)
        "10.1177/13623613231180266",  # Unwin 2024 Autism multi-sensory environments — 2 BPCs (REF-00542 + REF-00609)
        "10.1177/19375867211043546",  # van Buuren 2022 HERD Dementia-Friendly Design — 2 BPCs (REF-00301 + REF-00487)
        "10.2196/60622",              # Harper 2025 IJMR stair high-contrast striping — 2 BPCs (REF-00395 + REF-00534)
        "10.1108/arch-07-2023-0178",   # Ielegems & Vanrie 2024 Archnet-IJAR 18(4) cost UD public buildings — 2 BPCs (REF-00296 + REF-00307)
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

    # D04 — the DOI-less half of D01.
    #
    # R9 ("pre-check the DOI, cross-file the existing ref_id, never duplicate")
    # is only mechanically enforceable for sources that HAVE a DOI, which D01
    # covers. 422 of 863 sources have none — every T4/T5/T6 code, standard and
    # decree, plus grey and non-indexed work — and for those nothing has
    # detected a re-entry since `evidence_sources.doi_less_key` left the schema.
    #
    # That column was a stored author_year_title dedup key, present in
    # 001_initial_schema.sql and dropped by migrate_evidence_sources_v2.py when
    # authors were normalised into evidence_source_authors. Dropping it was
    # right: a denormalised key that can be recomputed from pub fields is a
    # second copy waiting to disagree with the first. What was never done is
    # re-expressing the CHECK on the new basis, so scripts/validate_db.py C5
    # ("without doi or doi_less_key — incomplete dedup data") simply started
    # crashing and was quarantined. The contract was sound; only its column
    # was obsolete. This recomputes the key and applies the contract.
    #
    # Key = normalised(first author) + pub_year + normalised(full title). The
    # full title is load-bearing: truncating it collapses legitimately distinct
    # clause-level rows (BCA Code 2025 whole-code vs Chapter 8; Finnish Decree
    # 241/2017 general vs door provisions) into false positives.
    KNOWN_DUP_SOURCE_KEYS = (
        # (normalised_author, pub_year, normalised_title) pairs that are
        # deliberately two rows. Empty today — every current collision is a
        # genuine re-entry queued for merge. Add here only with the reason.
    )
    import re as _re

    # Normalisation is Unicode-aware by necessity, not by politeness. An
    # ASCII-only fold ([^a-z]) erases 中华人民共和国住房和城乡建设部, 日本工業標準調査会,
    # 한국시각장애인연합회 and every other non-Latin corporate author to the empty
    # string. Both effects are unacceptable: D05 would report those sources as
    # "keyless" for not being Latin, and D04 would SKIP them — enforcing dedup
    # discipline on the English corpus while exempting the multilingual one, in
    # a corpus whose R5/R11 exist to prevent exactly that asymmetry.
    # Split before folding so "国土交通省 住宅局 (MLIT Housing Bureau)" keys on the
    # in-language name rather than the parenthetical gloss (R11: no
    # back-translation).
    def _norm_author(a):
        a = _re.split(r"[,;&(]| et al| and ", (a or "").casefold())[0]
        return _re.sub(r"\W", "", a, flags=_re.UNICODE)

    def _norm_title(t):
        return _re.sub(r"\W", "", (t or "").casefold(), flags=_re.UNICODE)

    # A merged duplicate is retained as a tombstone (forward-only; the row keeps
    # its id and gains superseded_by_ref_id), so without this exclusion a
    # completed merge still collides with its own canonical row and D04 can
    # never go green — the check would forbid the very remediation it demands.
    # Mirrors D01's `doi_resolution_outcome != 'REVERTED'` exclusion above.
    # This narrows the check to "no *live* duplicates", which is what it means;
    # the pointer's own integrity is guarded separately by A09.
    _groups = {}
    for r in conn.execute("""SELECT ref_id, pub_year, author_display, pub_title
                             FROM evidence_sources
                             WHERE (doi IS NULL OR doi = '')
                             AND (superseded_by_ref_id IS NULL
                                  OR superseded_by_ref_id = '')"""):
        key = (_norm_author(r[2]), r[1], _norm_title(r[3]))
        if not key[0] or not key[2] or key in KNOWN_DUP_SOURCE_KEYS:
            continue  # no computable key — C03/G02 own missing-author coverage
        _groups.setdefault(key, []).append(r[0])
    dup_sources = {k: v for k, v in _groups.items() if len(v) > 1}
    record("D04", "No duplicate DOI-less sources (author+year+title collision)",
           len(dup_sources) == 0,
           f"{len(dup_sources)} collisions across "
           f"{sum(len(v) for v in dup_sources.values())} rows: "
           + "; ".join("+".join(v) for v in sorted(dup_sources.values()))
           if dup_sources else "")

    # Sources with no DOI and no computable dedup key are invisible to both
    # D01 and D04 — the actual "incomplete dedup data" condition validate_db C5
    # was written to catch.
    undedupable = sum(
        1 for r in conn.execute("""SELECT author_display, pub_year, pub_title
                                   FROM evidence_sources
                                   WHERE doi IS NULL OR doi = ''""")
        if not _norm_author(r[0]) or r[1] is None or not _norm_title(r[2]))
    record("D05", "Every DOI-less source has a computable dedup key",
           undedupable == 0,
           f"{undedupable} DOI-less sources lack author, year or title — "
           f"invisible to both D01 and D04" if undedupable else "")

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

    # ── H: JSON-array ↔ junction parity ───────────────────────────────────────
    # Two edges on the walk are being migrated out of JSON TEXT columns and into
    # foreign-keyed junction tables (migrations 044 and 050). Until the columns
    # are dropped — a structural removal that needs a caller sweep — both stores
    # exist, and the only thing keeping them from silently diverging is this
    # section. Migration 044's header called for it; it is here now, covering
    # both junctions. Each is checked in BOTH directions: a one-way check would
    # pass while the junction quietly lost rows.
    print("\n[H] JSON-array ↔ junction parity")

    # Both edge columns carry a table-level CHECK (json_valid(...)), so text
    # that is not JSON at all cannot be written — fault-injection confirms the
    # UPDATE is refused, and an unguarded json_each over the live data does not
    # raise. What the CHECK does NOT stop is a valid JSON *scalar*: json_valid
    # ('3') is true. A scalar there would be skipped by json_each and quietly
    # shrink the comparison set instead of failing it. The shape is not
    # hypothetical — `citation_mining.connections_produced` holds a bare integer
    # in 13 of its 25 non-empty rows, a count in a column whose other rows hold
    # a list. So every parity query is scoped to rows that are demonstrably
    # arrays, and the rows that are not are reported by H06 rather than dropped.
    ARRAY_ROWS = ("{t}.{c} IS NOT NULL AND {t}.{c} != '' "
                  "AND json_valid({t}.{c}) AND json_type({t}.{c}) = 'array'")

    EDGE_JSON = (("evidence_cell_state", "governing_refs"),
                 ("search_executions",   "admitted_ref_ids"))

    def _parity(tid_a, tid_b, label, junction, jcols, table, tcol, key):
        jk, rk = jcols
        arrays = ARRAY_ROWS.format(t="t", c=tcol)
        extra = conn.execute(f"""
            SELECT COUNT(*) FROM {junction} j WHERE NOT EXISTS (
              SELECT 1 FROM {table} t, json_each(t.{tcol}) je
              WHERE {arrays} AND t.{key} = j.{jk} AND je.value = j.{rk})
        """).fetchone()[0]
        missing = conn.execute(f"""
            SELECT COUNT(*) FROM {table} t, json_each(t.{tcol}) je
            WHERE {arrays} AND NOT EXISTS (
              SELECT 1 FROM {junction} j WHERE j.{jk} = t.{key} AND j.{rk} = je.value)
        """).fetchone()[0]
        record(tid_a, f"{label}: every junction row is in the JSON", extra == 0,
               f"{extra} rows in {junction} with no matching {tcol} entry" if extra else "")
        record(tid_b, f"{label}: every JSON entry is in the junction", missing == 0,
               f"{missing} {tcol} entries with no {junction} row" if missing else "")

    _parity("H01", "H02", "cell_source_links ↔ governing_refs",
            "cell_source_links", ("cell_id", "ref_id"),
            "evidence_cell_state", "governing_refs", "cell_id")

    _parity("H03", "H04", "search_admissions ↔ admitted_ref_ids",
            "search_admissions", ("exec_id", "ref_id"),
            "search_executions", "admitted_ref_ids", "exec_id")

    # results_admitted is a third store of the same fact. It was consistent with
    # the JSON on all 84 rows when 050 was written; if it drifts, the junction is
    # the one to trust and this says so out loud rather than letting a stale
    # counter be read as yield.
    admit_count_drift = conn.execute("""
        SELECT COUNT(*) FROM search_executions se
        WHERE se.results_admitted != (
          SELECT COUNT(*) FROM search_admissions sa WHERE sa.exec_id = se.exec_id)
    """).fetchone()[0]
    record("H05", "results_admitted equals the admission edge count",
           admit_count_drift == 0,
           f"{admit_count_drift} executions whose results_admitted disagrees with "
           f"search_admissions" if admit_count_drift else "")

    # H06 is what makes H01–H04 non-vacuous: they only compare rows that are
    # JSON arrays, so a column drifting into some other shape would quietly
    # shrink the comparison set rather than fail it. This names that drift.
    nonarray = []
    for table, tcol in EDGE_JSON:
        n = conn.execute(f"""SELECT COUNT(*) FROM {table} t
            WHERE t.{tcol} IS NOT NULL AND t.{tcol} != ''
              AND NOT (json_valid(t.{tcol}) AND json_type(t.{tcol}) = 'array')
        """).fetchone()[0]
        if n:
            nonarray.append(f"{table}.{tcol}: {n}")
    record("H06", "edge JSON columns hold arrays, not scalars or malformed text",
           not nonarray, "; ".join(nonarray))

    # A ref repeated inside one array collapses to a single junction row (the
    # PK dedupes it), and both parity directions still pass — the junction
    # contains it and every entry is found. Only a count comparison sees it.
    dup = []
    for junction, jk, rk, table, tcol, key in (
        ("cell_source_links", "cell_id", "ref_id",
         "evidence_cell_state", "governing_refs", "cell_id"),
        ("search_admissions", "exec_id", "ref_id",
         "search_executions", "admitted_ref_ids", "exec_id"),
    ):
        arrays = ARRAY_ROWS.format(t="t", c=tcol)
        entries = conn.execute(
            f"SELECT COUNT(*) FROM {table} t, json_each(t.{tcol}) je WHERE {arrays}"
        ).fetchone()[0]
        edges = conn.execute(f"SELECT COUNT(*) FROM {junction}").fetchone()[0]
        if entries != edges:
            dup.append(f"{tcol} has {entries} entries but {junction} has {edges} rows")
    record("H07", "no id repeats inside a single JSON edge array", not dup,
           "; ".join(dup))

    # ── J: hop-4 edge coherence (source_value_extractions.item_code) ──────────
    # The column (migration 052) is nullable by design — NULL means the item was
    # not established at extraction. What it must never hold is an item that
    # contradicts the row's own slug or its own probe.
    print("\n[J] Extraction → item edge coherence")

    # An extraction's item should belong to the extraction's slug, by either
    # route the repo models that with: the item_bpc_links junction (hop 7's
    # edge object) or the legacy items.bpc_source_slug scalar it is replacing.
    # Assumption stated out loud: this holds while extractions describe items
    # their own BPC governs. If a legitimate cross-slug extraction ever appears,
    # this check is the thing that should be revisited — not silently widened.
    incoherent = conn.execute("""
        SELECT COUNT(*) FROM source_value_extractions sve
        WHERE sve.item_code IS NOT NULL
          AND NOT EXISTS (SELECT 1 FROM item_bpc_links l
                          WHERE l.item_code = sve.item_code AND l.slug = sve.slug)
          AND NOT EXISTS (SELECT 1 FROM items i
                          WHERE i.item_code = sve.item_code
                            AND i.bpc_source_slug = sve.slug)
    """).fetchone()[0]
    record("J01", "an extraction's item belongs to the extraction's slug",
           incoherent == 0,
           f"{incoherent} extractions whose item_code is not linked to their slug"
           if incoherent else "")

    # Where a row's own basis text names a PMP probe, that probe carries a typed
    # item_code. The two must agree — this is the W1 witness the backfill relied
    # on, turned into a standing check so it cannot drift apart later.
    probe_disagree = conn.execute("""
        SELECT COUNT(*) FROM source_value_extractions sve
        JOIN spec_value_probes p
          ON sve.root_classification_basis LIKE '%' || p.probe_id || '%'
        WHERE sve.item_code IS NOT NULL AND p.item_code != sve.item_code
    """).fetchone()[0]
    record("J02", "an extraction agrees with the PMP probe its basis text names",
           probe_disagree == 0,
           f"{probe_disagree} extractions disagreeing with their named probe"
           if probe_disagree else "")

    # J01 and J02 do NOT hold the judgment the backfill actually made, and an
    # adversarial review proved it by injection: setting extraction 6 to A-10b
    # passes both, because A-10b shares bpc_source_slug='room-acoustic-performance'
    # (so J01's second branch admits it) and row 6 names no probe (so J02 never
    # reaches it). The realistic error was never cross-slug — it was the OTHER
    # RT60 item, same slug. J01 guards the least-likely class.
    #
    # These eight assignments were adjudicated once, per row, in
    # data_20260804175506 under three named witness classes. That adjudication
    # is not mechanizable — but it is pinnable, and pinning it is what stops a
    # later pass from quietly reassigning a row to A-10b. This is a snapshot
    # check by design: if the set legitimately changes, this check changes with
    # it in the same commit, and the diff is the record of the re-adjudication.
    ADJUDICATED_A18 = tuple(range(1, 9))
    moved = conn.execute(f"""
        SELECT COUNT(*) FROM source_value_extractions
        WHERE extraction_id IN ({','.join('?' * len(ADJUDICATED_A18))})
          AND (item_code IS NULL OR item_code != 'A-18')
    """, ADJUDICATED_A18).fetchone()[0]
    record("J03", "the 8 adjudicated RT60 extractions still hold their assigned item",
           moved == 0,
           f"{moved} of the 8 rows adjudicated to A-18 by data_20260804175506 no "
           f"longer carry it — re-adjudicate in a migration, don't drift" if moved else "")

    # ── K: determination attestation (derivation_sha) ─────────────────────────
    # evidence-architecture §10 mechanical check 2: "same evidence + same
    # rule_version ⇒ same state + same derivation_sha". The sha is computed by
    # assess_cell.sha() over item|population|sorted(governing_refs)::rule_version,
    # so it attests WHICH cell identity and WHICH governing set produced the
    # determination. If a row moves after the sha is stamped and nobody
    # restamps, the hash silently attests a state that no longer exists — worse
    # than a NULL, which at least admits it attests nothing.
    #
    # This was found by hand during a render review, which is the wrong way to
    # find it. Both live failures were caused by ordinary maintenance: cell 9007
    # by the NEU→BRAIN population rename, cell 9003 by a governing-set
    # narrowing in the DB-integrity backlog sweep. Neither operation is unusual;
    # what was missing was anything that noticed.
    print("\n[K] Determination attestation")

    import hashlib as _hashlib
    import json as _json
    stale, unattested = [], 0
    for cid, ic, pc, gr, rv, sha_rec in conn.execute(
            "SELECT cell_id, item_code, population_code, governing_refs, rule_version, "
            "derivation_sha FROM evidence_cell_state"):
        if not sha_rec or not rv:
            unattested += 1
            continue
        refs = sorted(_json.loads(gr or "[]"))
        payload = f"{ic}|{pc}|" + "|".join(refs) + "::" + rv
        if _hashlib.sha256(payload.encode()).hexdigest() != sha_rec:
            stale.append(f"{cid} ({ic}×{pc})")
    record("K01", "every recorded derivation_sha verifies against its own row",
           not stale,
           f"{len(stale)} stale: {', '.join(stale)} — the row changed after the "
           f"determination was stamped; restamp or clear, don't leave a hash "
           f"attesting a state that no longer exists" if stale else "")

    # Reported, not enforced. Whether an unattested determination is acceptable
    # is an owner call — these rows were hand-migrated, not produced by an
    # engine run, so there is no derivation to hash. Failing on them would
    # demand a fabricated sha, which is the opposite of what K01 protects.
    if unattested:
        print(f"      note: {unattested} determination(s) carry no sha or no rule_version "
              f"and are unattested — reported, not failed (owner question)")

    # ── L: shadow-store parity (YAML ↔ DB) ────────────────────────────────────
    # Two governance stores are deliberately dual today: the DB table and the
    # YAML file that four scripts still open. Dual-store is only safe while
    # something holds them equal — otherwise the "DB is canonical" rule decays
    # into "whichever one you happened to open". These are the holders.
    print("\n[L] Shadow-store parity")

    import json as _js
    try:
        import yaml as _yaml
    except ImportError:
        record("L01", "decision register: YAML ↔ decisions table", True,
               "SKIPPED — PyYAML not installed")
        _yaml = None

    # Paths resolve from THIS FILE's location, not from cwd and not from the DB
    # path. The first version of this check derived them from `db_path`, and a
    # fault-injection run against a scratch copy in another directory made it
    # silently SKIP — recorded as a pass. A parity check that reports success
    # because it could not find one of the two stores is worse than no check.
    # A missing register is now a failure: it is part of the repo, so its
    # absence is a finding rather than a reason to stand down.
    REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    if _yaml is not None:
        reg = os.path.join(REPO, "data", "decisions", "decision_register.yaml")
        if not os.path.exists(reg):
            record("L01", "decision register: YAML ↔ decisions table", False,
                   f"register not found at {reg} — four scripts open it, including "
                   f"the blocking decision_capture.py")
        else:
            y = {d["decision_id"]: d for d in _yaml.safe_load(open(reg))["decisions"]}
            dbrows = {r[0]: r for r in conn.execute(
                "SELECT decision_id, category, delegation, status, decision_date, "
                "effort_level, supersedes FROM decisions")}
            only_y = sorted(set(y) - set(dbrows))
            only_d = sorted(set(dbrows) - set(y))
            drift = []
            for did in sorted(set(y) & set(dbrows)):
                d, r = y[did], dbrows[did]
                if (d["category"], d["delegation"], d["status"], d["decision_date"],
                        int(d["effort_level"])) != (r[1], r[2], r[3], r[4], r[5]):
                    drift.append(did)
                elif _js.loads(r[6] or "[]") != (d.get("supersedes") or []):
                    drift.append(did)
            detail = []
            if only_y:
                detail.append(f"{len(only_y)} in YAML only ({', '.join(only_y[:5])})")
            if only_d:
                detail.append(f"{len(only_d)} in DB only ({', '.join(only_d[:5])})")
            if drift:
                detail.append(f"{len(drift)} disagree on a field ({', '.join(drift[:5])})")
            record("L01", "decision register: YAML ↔ decisions table",
                   not (only_y or only_d or drift),
                   "; ".join(detail) + " — reconcile in a migration; the DB is canonical "
                   "(CLAUDE.md §2), so a YAML-only entry is an import gap and a "
                   "disagreement is a finding, not something to overwrite"
                   if detail else "")

    # jurisdictional_values has a YAML mirror too, held equal by
    # validate_schema.py --cross-check. Asserted here as well because that
    # check runs in a different battery and a data-only PR may not select it.
    jv_dir = os.path.join(REPO, "data", "jurisdictional_values")
    if _yaml is not None and os.path.isdir(jv_dir):
        n_yaml = 0
        for fn in os.listdir(jv_dir):
            if fn.endswith((".yaml", ".yml")):
                doc = _yaml.safe_load(open(os.path.join(jv_dir, fn))) or {}
                vals = doc.get("records") or []
                n_yaml += len(vals) if isinstance(vals, list) else 0
        n_db = conn.execute("SELECT COUNT(*) FROM jurisdictional_values").fetchone()[0]
        record("L02", "jurisdictional_values: YAML record count matches the table",
               n_yaml == n_db,
               f"{n_yaml} YAML records vs {n_db} table rows" if n_yaml != n_db else "")

    # ── L03: the legacy coverage grids are frozen ─────────────────────────────
    #
    # search_coverage (slug × jurisdiction) and search_languages (slug × language)
    # are hand-kept STATE grids. search_executions is the event LOG that replaced
    # them. State and log are both worth having, but only if the state is DERIVED
    # from the log — these were written independently, so the grid asserted
    # coverage the log could not corroborate and nothing could contradict it.
    #
    # It drifted in BOTH directions (measured 2026-08-06): of 634 cells marked
    # SEARCHED, 15 had an execution logged for that exact (slug, jurisdiction);
    # meanwhile 31 executions landed on cells the grid still called NOT-RUN.
    #
    # workplan/search-coverage-completion-workplan.md already ruled these "frozen
    # read-only as historical artifacts", and ruled that the pre-log rows are NOT
    # to be reconstructed — they record real work whose query terms are gone, and
    # inventing executions for them would be worse than leaving them. The log and
    # the derived views were built; the freeze was not, because db.py's
    # upsert-coverage was the live write path and a skill told every research
    # session to call it. That path is closed; this is what keeps it closed.
    #
    # A DIGEST, not a row count. A count-only freeze passes any UPDATE — the same
    # detection floor that lets the reproducibility gate miss an in-place edit.
    # Checked here rather than in a new script because a fifteenth enforcer file
    # is fifteen more chances to drift; DB invariants live in this file.
    FROZEN_GRIDS = {
        # table: (row count, sha256 of the sorted full contents)
        "search_coverage":  (4960, "f279875883ab6bfa272f7753d0bb55baff743128be3530193812d85a97944e21"),
        "search_languages": (1558, "b2d288a79ea4dd3280e43945615b0501d42fa7ae420845e2402e01b1d4859d3b"),
    }
    import hashlib as _hl
    for _tbl, (_want_n, _want_d) in FROZEN_GRIDS.items():
        try:
            _rows = conn.execute(f"SELECT * FROM {_tbl}").fetchall()
        except sqlite3.OperationalError as _exc:
            # A dropped table must FAIL this check, not abort the suite. The
            # first version let the OperationalError escape, so `DROP TABLE
            # search_coverage` killed all 71 checks with a traceback instead of
            # reporting the one that noticed — and dropping these tables is an
            # active proposal, so the crash was on the roadmap.
            record("L03", f"{_tbl} is frozen (hand-kept grid superseded by "
                          f"search_executions)", False,
                   f"table is unreadable ({_exc}). If it was retired, that is an "
                   f"owner-gated move and this constant retires with it.")
            continue
        # NUL sentinel for NULL. `"" if v is None else str(v)` mapped NULL and
        # the empty string to the same byte, so `UPDATE search_coverage SET
        # notes='' WHERE notes IS NULL` changed 4,950 rows and the digest did not
        # move — a content freeze that a table-wide UPDATE walked through.
        _digest = _hl.sha256(
            "\n".join(sorted("\x1f".join("\x00" if v is None else str(v) for v in r)
                             for r in _rows)).encode()).hexdigest()
        _ok = len(_rows) == _want_n and _digest == _want_d
        record("L03", f"{_tbl} is frozen (hand-kept grid superseded by search_executions)",
               _ok,
               f"{len(_rows)} rows / digest {_digest[:12]} — expected {_want_n} rows / "
               f"{_want_d[:12]}. This grid is history, not state: log the search itself "
               f"with `db.py log-search` and read coverage from v_coverage_jurisdiction / "
               f"v_coverage_language. If the change is deliberate, say so in the PR and "
               f"update the constant." if not _ok else "")

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
