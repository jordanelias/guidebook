-- data_20260522220000_retire_unverifiable_and_redo_crpd.sql
-- Per owner directive 2026-05-22:
--   (1) Retire rows that cannot be verified.
--   (2) Redo CRPD REF-00159 from scratch as a real primary source.

BEGIN TRANSACTION;

-- (1) RETIREMENT — 18 rows to UNVERIFIED-CLOSED
-- All are c1-migration-fix faithful copies of [GREY — full citation required] markers from
-- BPC reasoning docs. Targeted search of project files (search-logs, registry, BPC docs,
-- migration audit CSV, bibliography draft) found no underlying primary citations. Without
-- owner search-log work to resolve E-codes and TBC placeholders, these cannot be verified.

UPDATE evidence_sources SET
    verification_status = 'UNVERIFIED-CLOSED',
    metadata_integrity_status = 'TRIAGE-RETIRED-OWNER-GAP',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | retire-unverifiable 2026-05-22T22:00:00Z: RETIRED — c1-migration-fix-era row carries [GREY — full citation required] marker from BPC reasoning doc; primary source not located in any project file (search-logs are YAML-only headers, no body source tables; global-reference-registry carries same TBC marker; migration audit CSV carries same TBC marker). Targeted Crossref + web-search did not surface a canonical match. Per owner directive 2026-05-22: rows that cannot be verified are retired. Preserved for BPC citation continuity.',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T22:00:00Z retire-unverifiable] RETIRED owner-gap',
    verified_by_tool = 'triage-retirement-owner-gap',
    last_verified_at = '2026-05-22T22:00:00Z',
    updated_at = '2026-05-22T22:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id IN (
    'REF-00001',  -- (author TBC) IntD home design MDPI 2026
    'REF-00182',  -- (E10 — source TBC) Co-1 housing
    'REF-00183',  -- (E13 — source TBC) ZA middle-class exclusion
    'REF-00184',  -- (E14 — source TBC) ZA Co-1
    'REF-00185',  -- (E17 — source TBC) LAC systematic review
    'REF-00186',  -- (E29 — source TBC) KR 14.6% semi-basement
    'REF-00232',  -- (author TBC) ME/CFS built environment review
    'REF-00243',  -- (author TBC) ME/CFS activity pacing SR
    'REF-00257',  -- (internal) — no title
    'REF-00504',  -- (author TBC) India 2025
    'REF-00513',  -- (scoping review author TBC) TWSI Global South
    'REF-00514',  -- (scoping review author TBC) wayfinding Global South
    'REF-00594',  -- (author TBC) ambient bright light RCT ScienceDirect
    'REF-00595',  -- (author TBC) 24-week cluster RCT MDPI
    'REF-00596',  -- (author TBC) systematic review therapeutic lighting Solarlits
    'REF-00629',  -- UAE quiet design case study
    'REF-00634',  -- (Nigeria Co-1 source) DIY sensory corners
    'REF-00635'   -- (2024 scoping review) sensory room multi-country
);

-- (2) REDO CRPD — REF-00159 resolved as Broderick 2020 + cluster-aware metadata
UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Of rights and obligations: the birth of accessibility',
    pub_year = 2020,
    first_author_last = 'Broderick',
    first_author_first = 'A',
    is_corporate_primary = 0,
    author_display = 'Broderick A (Andrea) — Maastricht University, Faculty of Law',
    publisher = 'Informa UK Limited (Taylor & Francis)',
    journal_name = 'The International Journal of Human Rights',
    journal_abbrev = 'Int J Hum Rights',
    doi = '10.1080/13642987.2019.1634556',
    issn = '1364-2987',
    volume = '24',
    issue = '4',
    pages_start = '393',
    pages_end = '413',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'CRPD-REDO-2026-05-22',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | crpd-redo 2026-05-22T22:00:00Z: Original c1-migration-fix row was "(C01–C12 — full citations in search log) CRPD implementation sources C1–C12 [GREY]" stub representing CRB-05–CRB-12 bundle in references/bpc/frameworks-and-methodology/crpd-implementation-built-environment.md. Per owner directive 2026-05-22 "redo it": replaced stub with canonical primary source — Broderick A 2020 "Of rights and obligations: the birth of accessibility" Int J Hum Rights 24(4):393-413 DOI 10.1080/13642987.2019.1634556 (Maastricht University Faculty of Law). Anchors the legal-theory side of CRPD Article 9 implementation literature. Companion citations now needed in BPC reasoning doc: (a) Jónasdóttir et al. 2020 Scand J Disabil Res 22(1):371-381 DOI 10.16993/sjdr.730 (Iceland implementation case); (b) UN OHCHR SDG-CRPD Resource Package Article 9 Illustrative Indicators (UN agency report); (c) G3ict Toolkit Key Indicators of Accessibility CRPD Article 9 (technical guide reporting on 19 country submissions). Owner-queue: confirm whether to add (a)/(b)/(c) as new REF-IDs or fold into existing source rows.',
    url = 'https://www.tandfonline.com/doi/full/10.1080/13642987.2019.1634556',
    url_accessed = '2026-05-22',
    verified_by_tool = 'crossref-api-resolution+web-search-direct',
    last_verified_at = '2026-05-22T22:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T22:00:00Z crpd-redo] real primary source replaces C01-C12 stub',
    updated_at = '2026-05-22T22:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00159';

COMMIT;
