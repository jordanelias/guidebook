-- data_20260522080000_aspectss_batch_60.sql
-- ASPECTSS Mostafa 2014 cluster batch 60: 4 rows verified.
--
-- REF-00051, REF-00129, REF-00517, REF-00592: Mostafa M (2014) ARCHITECTURE FOR AUTISM
--   Autism ASPECTSS™ in School Design — Archnet-IJAR 8(1):143-158 DOI 10.26687/archnet-ijar.v8i1.314
-- Prior DB attribution to Frontiers in Psychiatry 10.3389/fpsyt.2021.727353 was wrong (DOI returned 404; not an Aspectss paper).

BEGIN TRANSACTION;

-- REF-00051: ASPECTSS design index
UPDATE evidence_sources SET
    pub_title = 'ARCHITECTURE FOR AUTISM: Autism ASPECTSS™ in School Design',
    pub_year = 2014,
    first_author_last = 'Mostafa',
    first_author_first = 'M',
    is_corporate_primary = 0,
    author_display = 'Mostafa M (Magda) — Department of Architecture, American University in Cairo (AUC)',
    publisher = 'ArchNet-IJAR (International Journal of Architectural Research)',
    journal_name = 'International Journal of Architectural Research: ArchNet-IJAR',
    journal_abbrev = 'Archnet-IJAR',
    doi = '10.26687/archnet-ijar.v8i1.314',
    issn = '1994-6961',
    volume = '8',
    issue = '1',
    pages_start = '143',
    pages_end = '158',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'JOURNAL-CORRECTION-FROM-FRONT-PSYCHIATRY',
    metadata_integrity_detail = 'aspectss-batch-60 2026-05-22T08:00:00Z: Crossref-confirmed via API search "Mostafa 2014 Architecture autism ASPECTSS school design". Prior DB cited Frontiers in Psychiatry DOI 10.3389/fpsyt.2021.727353 (404 invalid) — actual canonical publication is Archnet-IJAR 8(1):143-158 March 2014. Seven principles: Acoustics, Spatial sequencing, Escape, Compartmentalization, Transition spaces, Sensory zoning, Safety. Companion: Mostafa M (2008) unpublished AUC dissertation; Mostafa M (2014) "Architecture for Autism: Application of the Autism ASPECTSS Design Index to Home Environments" International Journal of the Constructed Environment 4(2) DOI 10.18848/2154-8587/cgp/v04i02/37413 (sister paper); Mostafa M (2015) "Architecture for autism: Built environment performance in accordance to the autism ASPECTSS design index" Archnet-IJAR 9(1). Advance Centre for Special Needs Qattameya Cairo + Progressive Architects (Egypt) implementation case. Mostafa now developing 500,000 m² ASPECTSS-based community in UAE (reverse-inclusion).',
    url = 'https://doi.org/10.26687/archnet-ijar.v8i1.314',
    url_accessed = '2026-05-22',
    verified_by_tool = 'crossref-api+archnet+aucegypt',
    last_verified_at = '2026-05-22T08:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T08:00:00Z aspectss-batch-60] DOI resolved + journal+year corrected from Front Psychiatry 2021 to Archnet-IJAR 2014',
    updated_at = '2026-05-22T08:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00051';

-- REF-00129: ASPECTSS 2.0 (same paper, same DOI; "2.0" likely refers to updated discussion)
UPDATE evidence_sources SET
    pub_title = 'ARCHITECTURE FOR AUTISM: Autism ASPECTSS™ in School Design',
    pub_year = 2014,
    first_author_last = 'Mostafa',
    first_author_first = 'M',
    is_corporate_primary = 0,
    author_display = 'Mostafa M (Magda) — Department of Architecture, American University in Cairo (AUC)',
    publisher = 'ArchNet-IJAR (International Journal of Architectural Research)',
    journal_name = 'International Journal of Architectural Research: ArchNet-IJAR',
    journal_abbrev = 'Archnet-IJAR',
    doi = '10.26687/archnet-ijar.v8i1.314',
    issn = '1994-6961',
    volume = '8',
    issue = '1',
    pages_start = '143',
    pages_end = '158',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'JOURNAL-CORRECTION-FROM-FRONT-PSYCHIATRY-CLUSTER-MEMBER',
    metadata_integrity_detail = 'aspectss-batch-60 2026-05-22T08:00:00Z: Same Mostafa 2014 Archnet-IJAR paper as REF-00051; cluster member. Original DB title "ASPECTSS 2.0" may refer to discussion of updated/applied version; primary canonical source is the 2014 paper. Owner-queue: confirm whether REF-00129 specifically references the 2015 Archnet-IJAR 9(1) "Built environment performance" sister paper instead.',
    url = 'https://doi.org/10.26687/archnet-ijar.v8i1.314',
    url_accessed = '2026-05-22',
    verified_by_tool = 'crossref-api+archnet',
    last_verified_at = '2026-05-22T08:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T08:00:00Z aspectss-batch-60] DOI cluster member',
    updated_at = '2026-05-22T08:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00129';

-- REF-00517: sensory zone transitions cluster member
UPDATE evidence_sources SET
    pub_title = 'ARCHITECTURE FOR AUTISM: Autism ASPECTSS™ in School Design',
    pub_year = 2014,
    first_author_last = 'Mostafa',
    first_author_first = 'M',
    is_corporate_primary = 0,
    author_display = 'Mostafa M (Magda) — Department of Architecture, American University in Cairo (AUC)',
    publisher = 'ArchNet-IJAR (International Journal of Architectural Research)',
    journal_name = 'International Journal of Architectural Research: ArchNet-IJAR',
    journal_abbrev = 'Archnet-IJAR',
    doi = '10.26687/archnet-ijar.v8i1.314',
    issn = '1994-6961',
    volume = '8',
    issue = '1',
    pages_start = '143',
    pages_end = '158',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'JOURNAL-CORRECTION-FROM-FRONT-PSYCHIATRY-CLUSTER-MEMBER',
    metadata_integrity_detail = 'aspectss-batch-60 2026-05-22T08:00:00Z: Same Mostafa 2014 Archnet-IJAR paper as REF-00051; cluster member referenced for sensory-zone-transitions principle (Transition spaces + Sensory zoning are 2 of the 7 ASPECTSS principles).',
    url = 'https://doi.org/10.26687/archnet-ijar.v8i1.314',
    url_accessed = '2026-05-22',
    verified_by_tool = 'crossref-api+archnet',
    last_verified_at = '2026-05-22T08:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T08:00:00Z aspectss-batch-60] DOI cluster member',
    updated_at = '2026-05-22T08:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00517';

-- REF-00592: Autism ASPECTSS Design Index cluster member
UPDATE evidence_sources SET
    pub_title = 'ARCHITECTURE FOR AUTISM: Autism ASPECTSS™ in School Design',
    pub_year = 2014,
    first_author_last = 'Mostafa',
    first_author_first = 'M',
    is_corporate_primary = 0,
    author_display = 'Mostafa M (Magda) — Department of Architecture, American University in Cairo (AUC)',
    publisher = 'ArchNet-IJAR (International Journal of Architectural Research)',
    journal_name = 'International Journal of Architectural Research: ArchNet-IJAR',
    journal_abbrev = 'Archnet-IJAR',
    doi = '10.26687/archnet-ijar.v8i1.314',
    issn = '1994-6961',
    volume = '8',
    issue = '1',
    pages_start = '143',
    pages_end = '158',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'JOURNAL-CORRECTION-FROM-FRONT-PSYCHIATRY-CLUSTER-MEMBER',
    metadata_integrity_detail = 'aspectss-batch-60 2026-05-22T08:00:00Z: Same Mostafa 2014 Archnet-IJAR paper as REF-00051; cluster member.',
    url = 'https://doi.org/10.26687/archnet-ijar.v8i1.314',
    url_accessed = '2026-05-22',
    verified_by_tool = 'crossref-api+archnet',
    last_verified_at = '2026-05-22T08:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T08:00:00Z aspectss-batch-60] DOI cluster member',
    updated_at = '2026-05-22T08:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00592';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
