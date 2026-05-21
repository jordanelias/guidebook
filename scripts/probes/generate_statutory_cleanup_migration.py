#!/usr/bin/env python3
"""Generate statutory-cohort cleanup migration (A: DIN/EN/IEC promotion fixing Drift 3,
B: ASD-tagged academic recategorization, C: wrong-DOI ASPECTSS cleanup)."""

TS = '2026-05-21T01:30:00Z'
SESSION = 'session_2026-05-20-ato-rehab'


def q(v):
    if v is None or v == '':
        return 'NULL'
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


out = []
P = out.append

P("-- data_20260521013000_statutory_cohort_cleanup.sql")
P("--")
P("-- Three-part statutory-cohort cleanup from full-DB verification audit.")
P("--")
P("-- A) DIN/EN/IEC promotion to COMPLETE-STATUTORY (14 rows). Per DR-2026-05-18.")
P("--    Standards are real, documented, stored metadata matches reality (verified")
P("--    via web search of DIN 18040 series, EN 17210:2021, IEC 60118-4:2014+AMD1).")
P("--    Simultaneously fixes Drift 3: the 10 overlapping rows had been promoted to")
P("--    COMPLETE-STATUTORY by migration 20260518050000 in history, but the committed")
P("--    DB never received the promotion (a non-runner write demoted them sideways to")
P("--    plain COMPLETE).")
P("--")
P("-- B) ASD-tagged academic recategorization (8 rows). standard_number='ASD' is a")
P("--    topic tag, not a standards identifier. source_type='standard' incorrectly")
P("--    routes them to the statutory verification track. Fix: source_type='report',")
P("--    clear standard_number, populate metadata_integrity_detail explaining.")
P("--")
P("-- C) Wrong-DOI Mostafa-ASPECTSS cleanup (4 rows). Four rows share DOI")
P("--    10.3389/fpsyt.2021.727353 which returns 404 at Crossref. Mostafa 2021 reference")
P("--    is to the DCU 'Autism Friendly University Design Guide' (issuu) — NOT a")
P("--    Frontiers Psychiatry paper. Wrong-DOI attachment; clear DOIs, flag as")
P("--    potential-multi-citation-duplicates for owner merge decision.")
P("--")
P("BEGIN TRANSACTION;")
P("")

# ============ Part A: DIN/EN/IEC promotion ============
P("-- =============================================================")
P("-- Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY (fixes Drift 3)")
P("-- =============================================================")
P("")

din_rows = [
    ('REF-00018', "DIN 32984:2011-10 — Bodenindikatoren im öffentlichen Raum (tactile ground indicators), confirmed via DIN catalog entries"),
    ('REF-00121', "EN 17210:2021 — European standard 'Accessibility and usability of the built environment', confirmed via BIH (Bundesarbeitsgemeinschaft der Integrationsämter)"),
    ('REF-00144', "DIN 18040-2:2011-09 — Barrierefreies Bauen Teil 2: Wohnungen (dwellings), confirmed via baunormenlexikon.de + nullbarriere.de"),
    ('REF-00200', "IEC 60118-4:2014+AMD1:2017 — Electroacoustics - Hearing aids - Part 4: Induction-loop systems for hearing aid purposes - System performance requirements (well-documented IEC standard)"),
    ('REF-00207', "DIN 18040-2:2011 §5 Bedienungshöhen (operating heights) — section reference within confirmed standard"),
    ('REF-00323', "DIN 18040-2:2011-09 — Barrierefreies Bauen Wohnungen, confirmed"),
    ('REF-00328', "IEC 60118-4:2014+AMD1:2017 — Induction-loop systems performance requirements, confirmed"),
    ('REF-00329', "DIN 18041:2016-03 — Hörsamkeit in Räumen (acoustic quality in rooms), well-known German acoustics standard, confirmed"),
    ('REF-00348', "IEC 60118-4:2014+AMD1:2017 — Hearing aids Part 4, confirmed"),
    ('REF-00351', "DIN 18040-1:2010 §5.2.2 — Induktionsschleife / Zwei-Sinne-Prinzip (two-senses principle) section reference within confirmed standard"),
    ('REF-00412', "DIN 18040-2:2011 + Draft E DIN 18040-2:2023 — confirmed series; draft 2023 in progress"),
    ('REF-00422', "DIN 18040-1:2010 — Barrierefreies Bauen Teil 1: Öffentlich zugängliche Gebäude, confirmed via BIH"),
    ('REF-00431', "DIN 18040-2:2011 Nullschwelle doctrine — section reference within confirmed standard"),
    ('REF-00445', "DIN 18040-1/-2 Türen (doors) — section reference within confirmed standards"),
]

for ref, detail in din_rows:
    P(f"-- {ref}: promote to COMPLETE-STATUTORY (was COMPLETE; pre-DR-2026-05-18 legacy)")
    P(f"UPDATE evidence_sources SET")
    P(f"  metadata_quality = 'COMPLETE-STATUTORY',")
    P(f"  metadata_integrity_status = 'OK',")
    P(f"  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || {q(' | statutory-cohort-cleanup ' + TS + ' Part A: ' + detail + '. Promoted to COMPLETE-STATUTORY per DR-2026-05-18.')},")
    P(f"  verification_note = COALESCE(verification_note, '') || {q(' | [PROBE ' + TS + ' statutory-cohort-cleanup] Part A: DIN/EN/IEC promotion to COMPLETE-STATUTORY')},")
    P(f"  updated_at = '{TS}', updated_by_session = '{SESSION}',")
    P(f"  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1")
    P(f"WHERE ref_id = '{ref}';")
    P("")

# ============ Part B: ASD-tagged recategorization ============
P("-- =============================================================")
P("-- Part B: ASD-tagged academic recategorization (8 rows)")
P("-- =============================================================")
P("")

asd_rows = [
    ('REF-00049', 'Caniato 2024 Institute of Acoustics — academic paper, not a standard'),
    ('REF-00547', 'Black 2022 SAGE/Autism — scoping review, not a standard'),
    ('REF-00602', 'Kates 2025 PLOS — binaural study, not a standard'),
    ('REF-00611', 'Leonardi 2025 SAGE/Autism — multisensory environments review, not a standard'),
    ('REF-00612', 'De Domenico 2024 MDPI/JCM — multi-sensory environment study, not a standard'),
    ('REF-00613', 'Kim 2022 SAGE/HERD — multisensory environment evaluation, not a standard'),
    ('REF-00702', 'Korean Academy of Sensory Integration 2022 — systematic review, not a standard'),
    ('REF-00710', 'Tola 2021 MDPI/IJERPH — built environment review, not a standard'),
]

for ref, note in asd_rows:
    P(f"-- {ref}: recategorize source_type standard->report, clear ASD tag")
    P(f"UPDATE evidence_sources SET")
    P(f"  source_type = 'report',")
    P(f"  standard_number = NULL,")
    P(f"  metadata_integrity_status = COALESCE(metadata_integrity_status, 'OK'),")
    P(f"  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || {q(' | statutory-cohort-cleanup ' + TS + ' Part B: ' + note + '. source_type recategorized standard->report; standard_number cleared (ASD is topic tag, not standards identifier).')},")
    P(f"  verification_note = COALESCE(verification_note, '') || {q(' | [PROBE ' + TS + ' statutory-cohort-cleanup] Part B: ASD-tag recategorization')},")
    P(f"  updated_at = '{TS}', updated_by_session = '{SESSION}'")
    P(f"WHERE ref_id = '{ref}';")
    P("")

# ============ Part C: Mostafa-ASPECTSS wrong-DOI cleanup ============
P("-- =============================================================")
P("-- Part C: Mostafa-ASPECTSS wrong-DOI cleanup (4 rows)")
P("-- =============================================================")
P("")

aspectss_refs = ['REF-00051', 'REF-00129', 'REF-00517', 'REF-00592']
for ref in aspectss_refs:
    P(f"-- {ref}: clear wrong DOI (Frontiers Psychiatry 10.3389/fpsyt.2021.727353 → 404)")
    P(f"UPDATE evidence_sources SET")
    P(f"  doi = NULL,")
    P(f"  verification_status = NULL,")
    P(f"  doi_resolution_outcome = NULL,")
    P(f"  metadata_quality = CASE WHEN metadata_quality = 'COMPLETE-STATUTORY' THEN 'AUTHOR-TITLE-ONLY' ELSE metadata_quality END,")
    P(f"  metadata_integrity_status = 'WRONG-DOI-CLEARED-POTENTIAL-DUPLICATE',")
    P(f"  metadata_integrity_detail = {q('statutory-cohort-cleanup ' + TS + ' Part C: DOI 10.3389/fpsyt.2021.727353 CLEARED — returns 404 at Crossref. Mostafa 2021 reference is to DCU \"Autism Friendly University Design Guide\" (issuu.com/magdamostafa/docs/the_autism_friendly_design_guide), NOT a Frontiers Psychiatry paper. All four rows (REF-00051, REF-00129, REF-00517, REF-00592) share this wrong-DOI; they are likely multi-citation references to the same Mostafa source. Owner: decide whether to merge into single row or keep separated by aspect.')},")
    P(f"  verification_note = COALESCE(verification_note, '') || {q(' | [PROBE ' + TS + ' statutory-cohort-cleanup] Part C: CLEAR-DOI wrong-attribution + potential-duplicate flag')},")
    P(f"  updated_at = '{TS}', updated_by_session = '{SESSION}',")
    P(f"  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1")
    P(f"WHERE ref_id = '{ref}';")
    P("")

P("-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)")
P("COMMIT;")

print('\n'.join(out))
