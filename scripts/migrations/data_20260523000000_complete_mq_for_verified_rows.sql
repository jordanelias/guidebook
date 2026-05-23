-- data_20260523000000_complete_mq_for_verified_rows.sql
-- Bulk-set metadata_quality='COMPLETE' on 10 rows that have verification_status='VERIFIED'
-- and full Crossref-resolved bibliographic metadata (DOI + journal + author + year) but were
-- never assigned metadata_quality during the citation-mining sessions that created them.
-- All 10 DOIs sanity-verified at Crossref 2026-05-23.

BEGIN TRANSACTION;

UPDATE evidence_sources SET
    metadata_quality = 'COMPLETE',
    doi_resolution_outcome = COALESCE(doi_resolution_outcome, 'RESOLVED'),
    metadata_integrity_status = COALESCE(metadata_integrity_status, 'CITATION-MINING-COMPLETE-BACKFILL'),
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | mq-backfill 2026-05-23T00:00:00Z: row was created with verification_status=VERIFIED + DOI + journal + author + year populated during citation-mining session but metadata_quality was never set. Crossref re-verified 2026-05-23. Pure data-completeness backfill.',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-23T00:00:00Z mq-backfill] Crossref re-verified',
    updated_at = '2026-05-23T00:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id IN (
    'REF-00704',  -- Lotan + Gold 2009 J Intellect Dev Disabil Snoezelen meta-analysis
    'REF-00713',  -- Barakat + Bakr + Sayad 2019 Alexandria Eng J autism nature
    'REF-00714',  -- Mostafa 2010 Open House Intl autism housing adaptation
    'REF-00715',  -- Piller + Pfeiffer 2016 OTJR preschool sensory environment
    'REF-00716',  -- McAllister + Maguire 2012 Support for Learning ASD-friendly classroom
    'REF-00717',  -- McAllister + Sloan 2016 Br J Special Educ pupil-designed autism school
    'REF-00718',  -- Deochand + Conway + Fuqua 2015 Support for Learning autism treatment centre
    'REF-00719',  -- Kanakri + Shepley + Varni + Tassinary 2017 Res Dev Disabil ASD noise
    'REF-00720',  -- Nagib + Williams 2018 Health & Place therapeutic landscapes home
    'REF-00721'   -- Tufvesson + Tufvesson 2008/2009 J Housing Built Environ inclusive school
);

COMMIT;
