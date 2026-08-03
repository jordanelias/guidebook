-- data_20260521160000_uk_guidelines_batch_24.sql
-- UK guidelines batch 24: 3 rows verified.
--
-- REF-00230: NICE NG206 ME/CFS 2021 — UK National Institute for Health and Care Excellence
-- REF-00408: DSDC University of Stirling dementia design guidance
-- REF-00428: BS 6440:2011 Powered vertical lifting platforms (lifts in dwellings)

BEGIN TRANSACTION;

-- REF-00230: NICE NG206
UPDATE evidence_sources SET
    pub_title = 'Myalgic encephalomyelitis (or encephalopathy)/chronic fatigue syndrome: diagnosis and management — NICE Guideline NG206',
    pub_year = 2021,
    first_author_last = 'National Institute for Health and Care Excellence',
    is_corporate_primary = 1,
    author_display = 'National Institute for Health and Care Excellence (NICE), UK',
    publisher = 'National Institute for Health and Care Excellence (NICE), London',
    standard_number = 'NICE Guideline NG206 (supersedes CG53 from 2007)',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-guidelines-batch-24 2026-05-21T16:00:00Z: web-search verified via nice.org.uk official + APCP UK + Medscape + Lancet correspondence + PubMed. Published 29 October 2021. Last reviewed 24 January 2025. Supersedes CG53 (2007). Key changes from CG53: removed graded exercise therapy (GET) as treatment; downgraded CBT to supportive intervention only; allows diagnosis after 3 months rather than 4-6; post-exertional malaise (PEM) recognised as core symptom. Affects an estimated 250,000+ people in England and Wales (2.4:1 female:male). Recommendations developed based on evidence reviewed before COVID-19 pandemic — explicitly does not apply to post-COVID-19 syndrome.',
    url = 'https://www.nice.org.uk/guidance/ng206',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+nice-official',
    last_verified_at = '2026-05-21T16:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T16:00:00Z uk-guidelines-batch-24] web-search verified',
    updated_at = '2026-05-21T16:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00230';

-- REF-00408: DSDC Stirling dementia design
UPDATE evidence_sources SET
    pub_title = 'Dementia Design Guidance — Dementia Services Development Centre (DSDC), University of Stirling',
    pub_year = 2020,
    first_author_last = 'Dementia Services Development Centre',
    is_corporate_primary = 1,
    author_display = 'Dementia Services Development Centre (DSDC), University of Stirling — Chief Architect Lesley Palmer',
    publisher = 'Dementia Services Development Centre, University of Stirling, Scotland',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-guidelines-batch-24 2026-05-21T16:00:00Z: web-search verified via dementia.stir.ac.uk + stir.ac.uk news + Care Inspectorate + Housing LIN + Kirklees Council + Dementia Environmental Design blog. DSDC established 1989. Pioneered the Dementia Design Audit Tool (DDAT) in 2008, replaced 2022 by the Environments for Ageing and Dementia Design Assessment Tool (EADDAT) — three tiers (Tier 1 entry-level free; Tier 2 wider building types; Tier 3 in development). Stirling Gold accreditation awarded to ~30 buildings globally. The 2020 "Dementia Design Guidance" stored title is most likely the body of DSDC guidance products including the book "Architecture of Dementia: Stirling Gold 2008-2020" published Sep 2020.',
    url = 'https://www.dementia.stir.ac.uk/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+dsdc-stirling-official',
    last_verified_at = '2026-05-21T16:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T16:00:00Z uk-guidelines-batch-24] web-search verified',
    updated_at = '2026-05-21T16:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00408';

-- REF-00428: BS 6440:2011 powered lifting platforms
UPDATE evidence_sources SET
    pub_title = 'BS 6440:2011 — Powered vertical lifting platforms having non-enclosed or partially enclosed liftways intended for use by persons with impaired mobility — Specification',
    pub_year = 2011,
    first_author_last = 'British Standards Institution',
    is_corporate_primary = 1,
    author_display = 'British Standards Institution (BSI), London',
    publisher = 'British Standards Institution (BSI), London',
    standard_number = 'BS 6440:2011 (supersedes BS 6440:1999; confirmed November 2016)',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-guidelines-batch-24 2026-05-21T16:00:00Z: web-search verified via BSI Knowledge + NBS Publication Index + ANSI Webstore + Stannah Lifts glossary + en-standard.eu + Sesame Access technical. Effective date: 31 August 2011. Confirmed November 2016 (likely source of stored "2016" year). Specification for powered lifting platforms for users with impaired mobility; rated speed ≤0.15 m/s; rated load 280-500 kg; stopping accuracy ±10 mm. Companion: BS EN 81-41 (cabin platform lifts) and BS 5900:2012 (powered home lifts in single-occupancy dwellings). Stored year 2016 corrected to 2011 (publication year) — confirmation in 2016 noted in detail.',
    url = 'https://knowledge.bsigroup.com/products/powered-vertical-lifting-platforms-having-non-enclosed-or-partially-enclosed-liftways-intended-for-use-by-persons-with-impaired-mobility-specification',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+bsi-knowledge+nbs',
    last_verified_at = '2026-05-21T16:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T16:00:00Z uk-guidelines-batch-24] web-search verified',
    updated_at = '2026-05-21T16:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00428';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
