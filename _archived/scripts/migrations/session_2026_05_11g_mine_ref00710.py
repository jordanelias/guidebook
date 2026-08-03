#!/usr/bin/env python3
"""
scripts/migrations/session_2026_05_11g_mine_ref00710.py

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

USAGE: GUIDEBOOK_DB_PATH=data/guidebook.db python3 session_2026_05_11g_mine_ref00710.py
"""
"""
Backward citation mining for REF-00710 (Tola 2021).
Candidates (12) hand-classified for ASD+BE relevance from CrossRef ref list.
Verify each via CrossRef DOI lookup; check dedup against existing evidence_sources
via doi_less_key; INSERT new rows; commit source_slug_links.
"""
import json, sqlite3, subprocess, sys, os
from datetime import datetime

# Candidates from CrossRef refs of REF-00710 (10.3390/ijerph18063203)
# Passed relevance filter: ASD + built environment + spatial design
CANDIDATES_710 = [
    # (crossref_ref_id, doi, expected_tier, expected_type, notes)
    ("Bates-2017", "10.1002/9781119053484", 4, "book",
     "Care and Design (Wiley) — Imrie, Kullman et al. care-design framework"),
    ("Barakat-2019", "10.1016/j.aej.2018.10.014", 3, "primary-research",
     "Nature as healer — outdoor BE for autistic children"),
    ("Mostafa-2010-OHI", "10.1108/OHI-01-2010-B0004", 3, "primary-research",
     "Housing Adaptation for Adults with ASD"),
    ("Piller-2016", "10.1177/1539449216665116", 1, "primary-research",
     "Sensory Environment and Participation of Preschool Children with ASD (OTJR — OT clinical)"),
    ("McAllister-2012", "10.1111/j.1467-9604.2012.01525.x", 3, "primary-research",
     "Design considerations for ASD-friendly Key Stage 1 classroom"),
    ("McAllister-2016", "10.1111/1467-8578.12160", 3, "primary-research",
     "Designed by the pupils, for the pupils — ASD school"),
    ("Deochand-2015", "10.1111/1467-9604.12103", 4, "primary-research",
     "Design Considerations Intensive Autism Treatment Centre"),
    ("Kanakri-2017", "10.1016/j.ridd.2017.02.004", 3, "primary-research",
     "Noise and ASD in children — exploratory survey"),
    ("Nagib-2018", "10.1016/j.healthplace.2018.05.001", 3, "primary-research",
     "Therapeutic landscapes at home — families of children with autism"),
    ("Tufvesson-2009", "10.1007/s10901-008-9129-6", 3, "primary-research",
     "Swedish school building process — all-inclusive school for children with concentration difficulty"),
    ("Kinnealey-2012", "10.5014/ajot.2012.004010", 1, "primary-research",
     "AJOT — Classroom modification on attention/engagement of students with autism/dyspraxia"),
    ("Mostafa-2018-ASPECTSS", "10.26687/archnet-ijar.v12i3.1589", 3, "primary-research",
     "ASPECTSS™ POE — learning environments designing for autism"),
]

import os
DB = os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db")
SESSION = "session_2026-05-11g-citation-mining.md"
SOURCE_LOCAL_REF = "SEA-01"  # Tola 2021 in school-environment-autism slug
SOURCE_REF_ID = "REF-00710"

def doi_less_key(first_author_surname, year, title):
    """Match the project's dedup function: lower(surname + year + first3_words)."""
    words = title.lower().split()[:3] if title else []
    key = (first_author_surname or "").lower() + str(year or "") + "".join(words)
    return ''.join(c for c in key if c.isalnum())

def fetch_crossref(doi):
    """Fetch metadata for a single DOI from CrossRef."""
    import urllib.request, urllib.parse
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='/')}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "guidebook-citation-miner/1.0 (mailto:jordan@example.com)"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.load(r)['message']
    except Exception as e:
        return {"_error": str(e)}

def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    now = datetime.utcnow().isoformat(timespec='seconds')

    # Get next REF-ID (only consider REF-NNNNN format, not REF-VERIFIED-NNN)
    mx = con.execute("""
        SELECT MAX(CAST(SUBSTR(ref_id,5) AS INTEGER))
        FROM evidence_sources
        WHERE ref_id LIKE 'REF-%' AND ref_id GLOB 'REF-[0-9][0-9][0-9][0-9][0-9]'
    """).fetchone()[0] or 0
    next_num = mx + 1
    print(f"Max numeric REF: {mx}, next: REF-{next_num:05d}")

    inserted = []
    skipped_dup = []
    failed = []

    for cand_id, doi, tier, etype, notes in CANDIDATES_710:
        print(f"\n--- {cand_id} ({doi}) ---")
        meta = fetch_crossref(doi)
        if "_error" in meta:
            print(f"  CrossRef fail: {meta['_error']}")
            failed.append((cand_id, doi, meta['_error']))
            continue

        title = (meta.get('title') or [''])[0] if meta.get('title') else ''
        year = None
        if meta.get('issued', {}).get('date-parts'):
            year = str(meta['issued']['date-parts'][0][0])
        elif meta.get('published-print', {}).get('date-parts'):
            year = str(meta['published-print']['date-parts'][0][0])
        elif meta.get('published-online', {}).get('date-parts'):
            year = str(meta['published-online']['date-parts'][0][0])

        authors_list = meta.get('author', [])
        if authors_list:
            authors_str = ', '.join(
                f"{a.get('family', '')}, {a.get('given', '')[:1]}." if a.get('given') else a.get('family', '')
                for a in authors_list[:5]
            )
            first_surname = authors_list[0].get('family', '')
        else:
            authors_str = '[unknown]'
            first_surname = ''

        # Fallback when CrossRef returns no author (e.g., editor-only book) — use editors
        if not first_surname:
            editors = meta.get('editor', []) or meta.get('chair', [])
            if editors:
                authors_str = ', '.join(f"{e.get('family', '')}, {e.get('given', '')[:1]}." for e in editors[:5]) + " (eds.)"
                first_surname = editors[0].get('family', '')
            elif meta.get('publisher'):
                # Last resort: institutional author
                authors_str = meta.get('publisher')
                first_surname = (meta.get('publisher') or '').split()[0]

        dlk = doi_less_key(first_surname, year, title)
        print(f"  meta: {first_surname} ({year}) — {title[:80]}")
        print(f"  doi_less_key: {dlk}")

        # Dedup
        existing = con.execute(
            "SELECT ref_id, authors, year, title FROM evidence_sources WHERE doi_less_key = ? OR doi = ?",
            (dlk, doi)
        ).fetchone()
        if existing:
            print(f"  DUPLICATE → already {existing['ref_id']}: {existing['authors']} ({existing['year']})")
            skipped_dup.append((cand_id, doi, existing['ref_id']))
            # Still link to slug if not already linked
            link_exists = con.execute(
                "SELECT 1 FROM source_slug_links WHERE ref_id = ? AND slug = 'school-environment-autism'",
                (existing['ref_id'],)
            ).fetchone()
            if not link_exists:
                # Add link with derivation marker
                local_ref = f"SEA-bw-{existing['ref_id'][-3:]}"
                con.execute("""
                    INSERT INTO source_slug_links (ref_id, slug, local_ref_id, created_at, created_by_session, updated_at, updated_by_session)
                    VALUES (?, 'school-environment-autism', ?, ?, ?, ?, ?)
                """, (existing['ref_id'], local_ref, now, SESSION, now, SESSION))
                print(f"  → linked existing {existing['ref_id']} to school-environment-autism as {local_ref}")
            continue

        # New: INSERT
        new_ref = f"REF-{next_num:05d}"
        next_num += 1
        derivation = f"backward_from:{SOURCE_REF_ID}/{SOURCE_LOCAL_REF};via:CrossRef"
        con.execute("""
            INSERT INTO evidence_sources
            (ref_id, authors, year, title, doi, doi_less_key, tier, evidence_type,
             verification_status, notes, created_at, created_by_session, updated_at, updated_by_session,
             derivation_chain)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'VERIFIED', ?, ?, ?, ?, ?, ?)
        """, (new_ref, authors_str, year, title, doi, dlk, tier, etype, notes, now, SESSION, now, SESSION, derivation))

        # Source-slug link
        local_ref = f"SEA-bw-{new_ref[-3:]}"
        con.execute("""
            INSERT INTO source_slug_links (ref_id, slug, local_ref_id, created_at, created_by_session, updated_at, updated_by_session)
            VALUES (?, 'school-environment-autism', ?, ?, ?, ?, ?)
        """, (new_ref, local_ref, now, SESSION, now, SESSION))

        inserted.append((new_ref, cand_id, doi, tier, first_surname, year))
        print(f"  → INSERTED {new_ref} (T{tier}) linked as {local_ref}")

    con.commit()

    # Citation mining row for REF-00710
    discovered_refs = json.dumps([r[0] for r in inserted])
    con.execute("""
        INSERT INTO citation_mining
        (slug, local_ref_id, global_ref_id, doi, backward, forward, connections_produced,
         notes, created_at, created_by_session, updated_at, updated_by_session, deferred_reason)
        VALUES ('school-environment-autism', 'SEA-01', 'REF-00710', '10.3390/ijerph18063203',
                1, 0, ?,
                ?, ?, ?, ?, ?, ?)
    """, (
        discovered_refs,
        f"Backward mined via CrossRef: 52 refs scanned, 12 candidates ASD+BE-relevant. "
        f"Inserted {len(inserted)} new sources, {len(skipped_dup)} dedup'd against existing. "
        f"Forward DEFERRED (see deferred_reason).",
        now, SESSION, now, SESSION,
        "FORWARD-DEFERRED: Scholar Gateway + Consensus connectors returned 'No approval received'. "
        "PubMed topic search returns 1099 topic-adjacent papers — that is the topic-evidence vs "
        "claim-evidence anti-pattern PI v10.6 standing rule #7 fights. Re-run when Scholar Gateway "
        "or actual cited-by API is available."
    ))
    con.commit()

    print(f"\n=== SUMMARY REF-00710 backward ===")
    print(f"  Inserted: {len(inserted)}")
    for r in inserted:
        print(f"    {r[0]}  T{r[3]}  {r[4]} ({r[5]})")
    print(f"  Dedup (already in DB, linked to slug): {len(skipped_dup)}")
    for r in skipped_dup:
        print(f"    {r[0]} → {r[2]}")
    print(f"  Failed: {len(failed)}")
    for r in failed:
        print(f"    {r[0]} ({r[1]}): {r[2]}")

if __name__ == "__main__":
    main()
