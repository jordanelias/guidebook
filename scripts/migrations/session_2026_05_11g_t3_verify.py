#!/usr/bin/env python3
"""
scripts/migrations/session_2026_05_11g_t3_verify.py

Captured mining script from session_2026-05-11g-citation-mining.md.
Sister scripts:
  - session_2026_05_11g_data.json       (output: DB state to be reapplied)
  - session_2026_05_11g_replay.py       (idempotent replayer that applies the JSON)
  - session_2026_05_11g_mine_*.py       (this kind: methodology/process scripts)

PURPOSE: Documents HOW the discoveries were made (CrossRef queries, dedup logic,
metadata mapping). Re-running these against a clean DB would re-discover the
same sources and produce the same citation_mining rows.

DEPENDS ON: scripts/db.py (for add-source CLI) and CrossRef REST API
            (no API key required).

USAGE: GUIDEBOOK_DB_PATH=data/guidebook.db python3 session_2026_05_11g_t3_verify.py
"""
import sqlite3, json
from datetime import datetime

import os
DB = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")
SESSION = "session_2026-05-11g-citation-mining.md"

# Verification results from CrossRef bibliographic search
T3_VERIFIED = [
    # (ref_id, local_ref_id, doi, new_authors, year, title_authoritative, confidence, notes)
    ("REF-00700", "SRU-FR-01", "10.1684/med.2022.792", "[unknown — Cairn.info masthead]", "2022",
     "Les espaces Snoezelen : quelle efficacité ?",
     "CONFIRMED",
     "Médecine 2022 journal (John Libbey Eurotext). Title and year match. Authors not in CrossRef metadata."),
    ("REF-00701", "SRU-ZH-01", "10.3389/fpsyt.2025.1623149", "Lyu et al.", "2025",
     "Effectiveness of sensory integration-based intervention in autistic children, focusing on Chinese children: a systematic review",
     "CONFIRMED",
     "Frontiers in Psychiatry 2025 — Lyu et al. systematic review on SI for autistic Chinese children. PMC ID may differ from DB note (DB said PMC12673401) — DOI verified."),
    ("REF-00702", "SRU-KO-01", None, None, None, None,
     "PROBABILISTIC",
     "CrossRef returned Jung (2014) 'A Systematic Review on Effects of School-Based Occupational Therapy' DOI:10.18064/jkasi.2014.12.1.025 as top match. May not be the exact paper the DB note '국내 자폐스펙트럼장애 아동 감각통합 중재방법' refers to. Held without DOI assignment pending owner spot-check."),
    ("REF-00703", "SRU-DA-01", "10.1016/j.ridd.2006.04.001", "McKee, S.A., Harris, G.T., Rice, M.E., Silk, L.", "2007",
     "Effects of a Snoezelen room on the behavior of three autistic clients",
     "CONFIRMED",
     "Research in Developmental Disabilities 28(3):304-316. Title in DB ('disturbing behaviour') was an approximate description, not exact title."),
    ("REF-00704", "SRU-DA-02", "10.1080/13668250903080106", "Lotan, M., Gold, C.", "2009",
     "Meta-analysis of the effectiveness of individual intervention in the controlled multisensory environment (Snoezelen) for individuals with intellectual disabilities",
     "CONFIRMED",
     "J Intellect Dev Disabil 34(3):207-215. Verified."),
]

def main():
    con = sqlite3.connect(DB)
    now = datetime.utcnow().isoformat(timespec='seconds')

    print("=== Update T3 verification status (REF-00700..00704) ===")
    for ref_id, local, doi, authors, year, title, conf, notes in T3_VERIFIED:
        # Compute updated metadata
        upd_notes = (f"Verified via CrossRef bibliographic search 2026-05-11 ({conf}). " +
                     notes)
        if conf == "CONFIRMED":
            cur = con.execute("""
                UPDATE evidence_sources
                SET verification_status = 'VERIFIED',
                    doi = COALESCE(?, doi),
                    authors = COALESCE(?, authors),
                    title = COALESCE(?, title),
                    year = COALESCE(?, year),
                    notes = COALESCE(notes, '') || ?,
                    updated_at = ?,
                    updated_by_session = ?
                WHERE ref_id = ?
            """, (doi, authors, title, year, '\n[2026-05-11] ' + upd_notes, now, SESSION, ref_id))
        else:  # PROBABILISTIC — don't overwrite metadata, just flag
            cur = con.execute("""
                UPDATE evidence_sources
                SET verification_status = 'PROBABILISTIC',
                    notes = COALESCE(notes, '') || ?,
                    updated_at = ?,
                    updated_by_session = ?
                WHERE ref_id = ?
            """, ('\n[2026-05-11] ' + upd_notes, now, SESSION, ref_id))

        # Add citation_mining row recording the verification + deferred mining
        con.execute("""
            INSERT INTO citation_mining
            (slug, local_ref_id, global_ref_id, doi, backward, forward, connections_produced,
             notes, created_at, created_by_session, updated_at, updated_by_session, deferred_reason)
            VALUES ('sensory-room-user-control', ?, ?, ?, 0, 0, '[]', ?, ?, ?, ?, ?, ?)
        """, (
            local, ref_id, doi,
            f"VERIFICATION-ONLY pass 2026-05-11. Status: {conf}. " +
            f"Mining DEFERRED — these are Tier 3, not mandatory under standards RULE 124 ('mandatory for Tier 1-2'). " +
            f"Backward mining can be revisited in a separate batch pass. " +
            (f"NOT mined because confidence is PROBABILISTIC — owner spot-check required first." if conf == "PROBABILISTIC" else ""),
            now, SESSION, now, SESSION,
            "DEFERRED-T3: Tier 3 mining is not mandatory; queue for batch pass."
        ))
        print(f"  {ref_id} → {conf}  doi={doi or '-'}  rows-updated={cur.rowcount}")

    # Mark bpc_metadata: school-environment-autism has had its 2 mandatory T2 fully mined (backward only — forward deferred)
    # citation_mining_complete = partial (not yet 1)
    # We won't set to 1 because forward is deferred.
    print("\n=== Update bpc_metadata ===")
    print("  school-environment-autism: citation_mining_complete stays 0 (forward deferred)")
    print("  sensory-room-user-control: citation_mining_complete stays 0 (T3 verification only)")
    print("  No bpc_metadata change this session — mining is partial.")

    con.commit()

    # Final tally
    print("\n=== Session DB delta summary ===")
    new_sources = con.execute("""
        SELECT COUNT(*) FROM evidence_sources WHERE created_by_session = ?
    """, (SESSION,)).fetchone()[0]
    new_links = con.execute("""
        SELECT COUNT(*) FROM source_slug_links WHERE created_by_session = ?
    """, (SESSION,)).fetchone()[0]
    new_mining = con.execute("""
        SELECT COUNT(*) FROM citation_mining WHERE created_by_session = ?
    """, (SESSION,)).fetchone()[0]
    updates = con.execute("""
        SELECT COUNT(*) FROM evidence_sources WHERE updated_by_session = ?
    """, (SESSION,)).fetchone()[0]
    print(f"  New evidence_sources rows: {new_sources}")
    print(f"  New source_slug_links rows: {new_links}")
    print(f"  New citation_mining rows: {new_mining}")
    print(f"  Evidence_sources rows updated this session: {updates}")

    print("\n=== Verify integrity ===")
    # Make sure no orphans
    orphans = con.execute("""
        SELECT ssl.ref_id, ssl.slug FROM source_slug_links ssl
        LEFT JOIN evidence_sources es ON ssl.ref_id = es.ref_id
        WHERE ssl.created_by_session = ? AND es.ref_id IS NULL
    """, (SESSION,)).fetchall()
    print(f"  Orphan links: {len(orphans)}")

    # Citation_mining rows should reference valid global_ref_ids
    bad_cm = con.execute("""
        SELECT cm.global_ref_id FROM citation_mining cm
        LEFT JOIN evidence_sources es ON cm.global_ref_id = es.ref_id
        WHERE cm.created_by_session = ? AND es.ref_id IS NULL
    """, (SESSION,)).fetchall()
    print(f"  citation_mining rows with bad global_ref_id: {len(bad_cm)}")

if __name__ == "__main__":
    main()
