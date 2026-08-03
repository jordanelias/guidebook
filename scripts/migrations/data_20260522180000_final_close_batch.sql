-- data_20260522180000_final_close_batch.sql
-- Final close-out batch: 1 verification + 10 retirements.

BEGIN TRANSACTION;

-- REF-00192: Steinfeld E, Maisel J, Feathers D, D'Souza C (2010) Anthropometry and Standards for Wheeled Mobility
UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Anthropometry and Standards for Wheeled Mobility: An International Comparison',
    pub_year = 2010,
    first_author_last = 'Steinfeld',
    first_author_first = 'E',
    is_corporate_primary = 0,
    author_display = 'Steinfeld E, Maisel J, Feathers D, D''Souza C',
    publisher = 'Informa UK Limited (Taylor & Francis)',
    journal_name = 'Assistive Technology',
    journal_abbrev = 'Assist Technol',
    doi = '10.1080/10400430903520280',
    issn = '1040-0435',
    volume = '22',
    issue = '1',
    pages_start = '51',
    pages_end = '67',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'CROSSREF-RESOLVED-CLUSTER-MEMBER',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | final-close 2026-05-22T18:00:00Z: Crossref-resolved IDEA Center anthropometric standards paper; 4-author roster Steinfeld + Maisel + Feathers + D''Souza; cluster member with REF-00060 (year corrected 2006→2010 — DB original year reflected RESNA conference timing not journal publication).',
    verified_by_tool = 'crossref-api-resolution',
    last_verified_at = '2026-05-22T18:00:00Z',
    updated_at = '2026-05-22T18:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00192';

-- RETIREMENTS (10 rows → UNVERIFIED-CLOSED)
-- Placeholder-title rows for which targeted Crossref + web-search returned no justifiable topical match.
UPDATE evidence_sources SET
    verification_status = 'UNVERIFIED-CLOSED',
    metadata_integrity_status = 'TRIAGE-RETIRED-NO-LEAD',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | final-close 2026-05-22T18:00:00Z: RETIRED — multiple targeted Crossref + web-search rounds returned no topical match. DB row created in session_2026-05-08-c1-migration-fix with paraphrased title; real source plausibly exists but not locatable via reasonable search effort. Preserved for BPC citation continuity per DR-2026-05-13.',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T18:00:00Z final-close] RETIRED no-lead',
    verified_by_tool = 'triage-retirement-no-lead',
    last_verified_at = '2026-05-22T18:00:00Z',
    updated_at = '2026-05-22T18:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id IN (
    'REF-00093',  -- Holohan E 2022 TID (different from REF-00131 thesis)
    'REF-00106',  -- De Cuyper 2023 (Crossref returned 2023 J Psychiatric Mental Health Nurs author match but content mismatch)
    'REF-00133',  -- Young R 2019 OT-design (Young 2020 human design book is different topic)
    'REF-00139',  -- Trouvé H 2016 FR OT (Crossref returned history journal)
    'REF-00181',  -- Siu A 2024 PEOP (Siu 2024 casino tourism is different person)
    'REF-00218',  -- Hayashi 2022 Japanese clinical (Crossref returned LIDC antitrust + English teachers — wrong topic)
    'REF-00221',  -- Geisser 2021 hyperacusis+fibro (Crossref returned Pain pain-measurement abstract)
    'REF-00253',  -- Nakayama 1981 inter-room temperature (no specific 1981 Japanese cardiac-cold paper located)
    'REF-00483',  -- Grey C 2015 schema scaffolding DEM/ABI (no specific Crossref match)
    'REF-00521',  -- Jost 2024 "Navigating Life" (no specific dementia narrative book located)
    'REF-00529',  -- Thompson D 2022 computational modelling (Crossref returned NDIS health-care chapter)
    'REF-00543',  -- Rashid M 2025 sensory-informed taxonomy (truncated DOI; no Crossref completion)
    'REF-00625',  -- Bertone A 2021 low vision SR (Crossref returned 2020 McGill autism perception — wrong topic)
    'REF-00733'   -- Ismail 2023 fibromyalgia hydrotherapy SR (Crossref returned Saracoglu 2023 rheumatic disease — wrong author)
);

COMMIT;
