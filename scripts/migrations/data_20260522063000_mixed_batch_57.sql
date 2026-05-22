-- data_20260522063000_mixed_batch_57.sql
-- Mixed batch 57: 3 rows verified.
--
-- REF-00300: hcma/RHFAC Retrofits + Upgrades Cost Study Jan 2024 — Rick Hansen Foundation
-- REF-00254: UK MS Society + Filingeri + Christogianni 2022 MSARD — DOI 10.1016/j.msard.2022.104075
-- REF-00468: Norway Husbanken/DiBK doors guidance (TEK17 + grunnlån)

BEGIN TRANSACTION;

-- REF-00300: RHFAC Retrofits + Upgrades Cost Study 2024
UPDATE evidence_sources SET
    pub_title = 'RHFAC™ Retrofits and Upgrades Cost Study — cost of retrofitting existing office towers + K-12 schools to Rick Hansen Foundation Accessibility Certification Gold (RHFAC v3.0)',
    pub_year = 2024,
    first_author_last = 'hcma',
    is_corporate_primary = 1,
    author_display = 'hcma architecture + design (Vancouver) — Managing Principal Darryl Condon FRAIC; in collaboration with Rick Hansen Foundation (RHF)',
    publisher = 'hcma architecture + design (Vancouver, BC) + Rick Hansen Foundation, Richmond BC',
    standard_number = 'RHFAC Retrofits and Upgrades Cost Study — published January 2024 (publication date 2024-01-05); 10 RHFAC-rated office towers + 10 RHFAC-rated schools (BC + Ontario, built 1974-2019); RHFAC program version 3.0 methodology. Findings: RHFAC Gold achievable for <0.5% of replacement cost in an office tower; <1.5% in a K-12 school; $1.50/sf offices + $9.00/sf schools (gross floor area); no-cost upgrades (furniture relocation), minimal-cost upgrades (assistive listening systems, braille signage, colour-contrast signage, fixture-height adjustment), higher-cost upgrades (fire alarm systems, accessible kitchens, universal washrooms). Companion: 2020 RHFAC Cost Comparison Feasibility Study; underlying CAN-ASC standards + provincial building codes (NBC 2015 + OBC 2018); Accessible Canada Act (S.C. 2019, c. 10) + Accessibility for Manitobans Act + AODA (Ontario).',
    jurisdiction = 'CA',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-57 2026-05-22T06:30:00Z: web-search verified via hcma.ca (official) + rickhansen.com (PDF) + canadianarchitect.com + raic.org (RAIC webinar May 2024) + reminetwork.com + canada.constructconnect.com (Feb 2024 coverage). PDF at https://www.rickhansen.com/sites/default/files/2024-02/rhfac-retrofits-and-upgrades-cost-study-reporthcma-202401050.pdf',
    url = 'https://hcma.ca/assets/rick-hansen-foundation-accessibility-certification-retrofits-and-upgrades-cost-study/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+hcma-official+rick-hansen-foundation',
    last_verified_at = '2026-05-22T06:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T06:30:00Z mixed-batch-57] web-search verified',
    updated_at = '2026-05-22T06:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00300';

-- REF-00254: UK MS heat sensitivity (Christogianni Filingeri 2022 + MS Society resources)
UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Heat and cold sensitivity in multiple sclerosis: A patient-centred perspective on triggers, symptoms, and thermal resilience practices',
    pub_year = 2022,
    first_author_last = 'Christogianni',
    first_author_first = 'A',
    is_corporate_primary = 0,
    author_display = 'Christogianni A, O''Garro J, Bibb R, Filtness A, Filingeri D',
    publisher = 'Elsevier; Multiple Sclerosis and Related Disorders',
    journal_name = 'Multiple Sclerosis and Related Disorders',
    journal_abbrev = 'Mult Scler Relat Disord',
    doi = '10.1016/j.msard.2022.104075',
    issn = '2211-0348',
    volume = '67',
    article_number = '104075',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'CROSS-REF-MS-SOCIETY',
    metadata_integrity_detail = 'mixed-batch-57 2026-05-22T06:30:00Z: web-search verified via eprints.soton.ac.uk (University of Southampton institutional repository) + mssociety.org.uk (commissioning context). 757 persons with MS surveyed; Christogianni A, O''Garro J, Bibb R, Filtness A, Filingeri D (2022) MSARD 67:104075. Companion: MS Society UK "Too hot, too cold: the science behind temperature and MS" + "Under the microscope: heat sensitivity" + "Handling the heat" research blog series featuring Davide Filingeri (Associate Professor in Thermal Physiology, University of Southampton). DB row source_type was guideline; rebound to journal_article since the canonical underlying source is the Christogianni-Filingeri 2022 study. Companion 2024 Chaseling et al. Eur J Appl Physiol cold-water swilling DOI 10.1007/s00421-025-05766-6 (n=13 heat-sensitive pwMS). Uhthoff''s phenomenon framework.',
    url = 'https://doi.org/10.1016/j.msard.2022.104075',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+ms-society-uk+soton-eprints+crossref',
    last_verified_at = '2026-05-22T06:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T06:30:00Z mixed-batch-57] DOI resolved + source_type rebind',
    updated_at = '2026-05-22T06:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00254';

-- REF-00468: Norway Husbanken/DiBK doors guidance
UPDATE evidence_sources SET
    pub_title = 'Norwegian door + entrance accessibility guidance — Husbanken grunnlån kvalitetskrav + DiBK Veileder til TEK17 + Husbankens veileder til grunnlån kap. 5 (livsløpsbolig + tilgjengelighet)',
    pub_year = 2017,
    first_author_last = 'Husbanken',
    is_corporate_primary = 1,
    author_display = 'Husbanken (Den norske stats husbank, Norwegian State Housing Bank, Drammen) + DiBK (Direktoratet for byggkvalitet, Norwegian Building Authority)',
    publisher = 'Husbanken + DiBK — under Kommunal- og distriktsdepartementet (KDD) (Ministry of Local Government and Regional Development)',
    standard_number = 'Husbanken grunnlån kvalitetskrav for tilgjengelighet (Universal Design + Lifetime Home accessibility quality criteria) — includes door + entrance threshold-free + clear-width criteria; underlying Forskrift om tekniske krav til byggverk (Byggteknisk forskrift, TEK17, FOR-2017-06-19-840) §12-2 + §12-12 + §12-15 (doors, doorways, terskel/threshold ≤ 25mm); DiBK Veileder til TEK17 official commentary; Husbankens veileder til grunnlån kap. 5 (kvalitetskrav). Earlier Husbanken 2002 Universal Design compendium ed. Sigmund Asmervik + Tone Rønnevig (companion REF). Norwegian access: ca. 50% of all houses post-WWII financed by Husbanken (Wikipedia Husbanken).',
    jurisdiction = 'NO',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-57 2026-05-22T06:30:00Z: web-search verified via husbanken.no/english (official) + husbanken.no Veileder til grunnlån + dibk.no (Norwegian Building Authority) + lovdata.no TEK17 forskrift. Owner-queue: specific cited document title/year — Husbanken combines multiple instruments (Bostøtte, Startlån, Grunnlån, Investeringstilskudd) with embedded accessibility requirements. Current verification reflects regulatory-framework attribution.',
    url = 'https://husbanken.no/english/about-the-housing-bank/the-housing-banks-role/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+husbanken-official+dibk-context',
    last_verified_at = '2026-05-22T06:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T06:30:00Z mixed-batch-57] regulatory-framework attribution',
    updated_at = '2026-05-22T06:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00468';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
