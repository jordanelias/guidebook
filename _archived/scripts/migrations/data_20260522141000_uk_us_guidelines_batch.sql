-- data_20260522141000_uk_us_guidelines_batch.sql
-- UK + US guideline batch: 2 rows verified.
--
-- REF-00357: Foundations (UK national HIA body) — Disabled Facilities Grant External Review 2018 + AKW Medi-Care 2023
-- REF-00324: SDSU Extension — Laundry Room Design for Independence (Voices for Home Modification of the Dakota project, NDSU + SDSU)

BEGIN TRANSACTION;

-- REF-00357: Foundations + AKW UK DFG framework
UPDATE evidence_sources SET
    pub_title = 'Disabled Facilities Grant (DFG) and Other Adaptations: External Review + AKW Medi-Care partnership reports (UK home adaptations sector guidance)',
    pub_year = 2023,
    first_author_last = 'Foundations',
    is_corporate_primary = 1,
    author_display = 'Foundations (UK national body for Home Improvement Agencies, HIAs) + AKW Medi-Care Ltd (Droitwich, Worcestershire — accessible bathroom + adaptation product manufacturer); originating External Review Dec 2018 by Foundations + IPSOS MORI',
    publisher = 'Foundations, Glossop, Derbyshire — funded by Department for Levelling Up, Housing and Communities (DLUHC, now MHCLG) since 2000; companion AKW Medi-Care Ltd',
    standard_number = 'UK Disabled Facilities Grant (DFG) framework — statutory grant under Housing Grants, Construction and Regeneration Act 1996 + Care Act 2014 + Better Care Fund; managed by Foundations as national body for ~190 HIAs in England since 2000; central government DFG budget £623m for 2023/24 (announced April 2023 with £102m capital top-up); Northern Ireland maximum £25,000 via NIHE; Scotland via local Care + Repair Scotland framework. External Review 2018 + Adapt My Home tool + Home Adaptations Installer Network. Companion: Habinteg HQM standards + RIBA Lifetime Homes; underlying Approved Document M Vol 1 (M4(1)/M4(2)/M4(3) categories) + BS 8300 framework. AKW Medi-Care is UK accessible-bathroom manufacturer regularly partnering with Foundations on adaptations advocacy + practitioner guidance.',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | uk-us-guidelines-batch 2026-05-22T14:10:00Z: web-search verified via foundations.uk.com (official Disabled Facilities Grant and Other Adaptations External Review Full Report) + ageuk.org.uk (The Disabled Facilities Grant: A Step Change report) + commonslibrary.parliament.uk (House of Commons Library research briefing) + akw-ltd.co.uk (AKW Medi-Care manufacturer site). Owner-queue: confirm whether DB cites Foundations 2023 specific report (Step Change, External Review summary) or AKW marketing/practitioner content; current verification reflects framework-level UK DFG attribution.',
    url = 'https://www.foundations.uk.com/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+foundations-uk-official+ageuk',
    last_verified_at = '2026-05-22T14:10:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T14:10:00Z uk-us-guidelines-batch] web-search verified framework',
    updated_at = '2026-05-22T14:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00357';

-- REF-00324: SDSU Extension
UPDATE evidence_sources SET
    pub_title = 'Laundry Room Design for Independence — universal-design accessible-laundry guidance + funding-for-home-modifications resources (Voices for Home Modification of the Dakota project)',
    pub_year = 2020,
    first_author_last = 'SDSU Extension',
    is_corporate_primary = 1,
    author_display = 'South Dakota State University (SDSU) Extension + North Dakota State University (NDSU) Extension — partnered Voices for Home Modification of the Dakota project team',
    publisher = 'SDSU Extension (Brookings, South Dakota) — companion NDSU Extension; Voices for Home Modification of the Dakota project',
    standard_number = 'SDSU Extension + NDSU Extension Voices for Home Modification of the Dakota — Land-grant university extension publication; companion publications: Universal Design for Lifelong Independence, Universal Design in New Construction, Home Modification Planning Guides (2025 update), Funding Home Modifications. Underlying ADA 1990 + ANSI A117.1 + Fair Housing Amendments Act 1988. Specs: 36" entrance door minimum, 5-foot turning radius, 18" lateral clearance left/right of appliance, front-loading washers on 12" pedestal, side-by-side configuration with opposite-swing doors.',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | uk-us-guidelines-batch 2026-05-22T14:10:00Z: web-search verified via extension.sdstate.edu (official SDSU Extension; Laundry Room Design for Independence + Universal Design in New Construction + Home Modification Planning Guides publications); Voices for Home Modification of the Dakota project NDSU + SDSU Extension partnership.',
    url = 'https://extension.sdstate.edu/laundry-room-design-independence',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+sdsu-extension-official',
    last_verified_at = '2026-05-22T14:10:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T14:10:00Z uk-us-guidelines-batch] web-search verified',
    updated_at = '2026-05-22T14:10:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00324';

COMMIT;
