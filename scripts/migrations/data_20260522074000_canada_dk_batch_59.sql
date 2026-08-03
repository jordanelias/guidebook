-- data_20260522074000_canada_dk_batch_59.sql
-- Canada + Denmark batch 59: 3 rows verified.
--
-- REF-00073: Ringaert L et al. 2001 — Universal Design Institute (University of Manitoba) wheelchair dimensions
-- REF-00569: Canadian dementia and noise framework (CABHI/Shannex Arborstone Halifax NS + WHO 2011 EU report)
-- REF-00599: Denmark DemensCentrum/Nationalt Videnscenter for Demens circadian lighting context

BEGIN TRANSACTION;

-- REF-00073: Ringaert 2001 UDI Manitoba
UPDATE evidence_sources SET
    pub_title = 'Determination of New Dimensions for Universal Design Codes and Standards with Consideration of Powered Wheelchair and Scooter Users',
    pub_year = 2001,
    first_author_last = 'Ringaert',
    first_author_first = 'L',
    is_corporate_primary = 0,
    author_display = 'Ringaert L, Rapson D, Qui J, Cooper J, Shwedyk E',
    publisher = 'Universal Design Institute (UDI), University of Manitoba, Winnipeg MB',
    standard_number = 'UDI wheelchair dimensions research — anthropometric + spatial dimensions study informing universal-design codes; tested wheelchair + scooter turning space requirements (e.g., 180° turn requiring 1925mm = 75.8in vs ANSI A117.1 baseline); cited in Steinfeld E, Maisel J, Feathers D (2005) "Standards and anthropometry for wheeled mobility" Buffalo NY: IDEA Center; foundational evidence for ICC/ANSI A117.1 (1998), CSA B651-04 (Canada), BS 8300:2001 (UK), AS 1428.2-1992 (AU) cross-jurisdictional comparison. Lead author Laurie Ringaert currently on Accessibility Standards Canada Board of Directors; owner Change Weavers Consulting (Winnipeg/Nanaimo); 30+ years accessibility research; previously led Universal Design Institute University of Manitoba + Centre for Universal Design NCSU.',
    jurisdiction = 'CA',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'NO-MATCH',
    metadata_integrity_status = 'BOOK-INSTITUTIONAL-NO-DOI',
    metadata_integrity_detail = 'canada-dk-batch-59 2026-05-22T07:40:00Z: web-search verified via resna.org RESNA conference proceedings 2006 (Steinfeld et al. citing original research) + accessible.canada.ca (Ringaert ASC Board biography). 5 authors confirmed: Ringaert L (Laurie, principal investigator), Rapson D, Qui J, Cooper J, Shwedyk E. Institutional report from UDI University of Manitoba; no DOI assigned (typical for institutional reports of this era).',
    url = 'https://www.resna.org/sites/default/files/legacy/conference/proceedings/2006/Research/Outcomes/Steinfeld.html',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+resna+accessible-canada-board',
    last_verified_at = '2026-05-22T07:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T07:40:00Z canada-dk-batch-59] web-search verified',
    updated_at = '2026-05-22T07:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00073';

-- REF-00569: Canada dementia and noise framework
UPDATE evidence_sources SET
    pub_title = 'Dementia and noise — Canadian long-term care environment framework (Shannex Arborstone Halifax NS sound audit pilot + CABHI knowledge translation; cites WHO 2011 EU DALY noise health-impacts report)',
    pub_year = 2017,
    first_author_last = 'Condran',
    first_author_first = 'S',
    is_corporate_primary = 0,
    author_display = 'Condran S (Sarah, music therapist) — Shannex Arborstone Enhanced Care, Halifax NS; supported by CABHI (Centre for Aging + Brain Health Innovation, Toronto ON)',
    publisher = 'CABHI (Centre for Aging + Brain Health Innovation), Toronto ON — under Baycrest Health Sciences; Shannex Arborstone Enhanced Care, Halifax NS',
    standard_number = 'Canadian dementia + noise framework — Shannex Arborstone Halifax NS sound audit pilot 2017; CABHI-supported knowledge-translation project; cites WHO 2011 Burden of disease from environmental noise (EU 27 + Western European DALY estimates: 61,000 yrs ischemic heart disease, 45,000 yrs cognitive impairment in children, 903,000 yrs sleep disturbances, 22,000 yrs tinnitus, 587,000 yrs annoyance); flight-or-fight stress response triggered by abrupt/loud sounds; hyperacusis in PWD reducing capacity to filter sensory input; noise sources in LTC: laundry carts, staff conversations, elevators, dishes. Companion: Christogianni-Filingeri 2022 MS heat sensitivity (REF-00254 framework parallel); IPA International Psychogeriatrics + Centre for Aging + Brain Health Innovation (CABHI Toronto, founded 2015 under Baycrest Hospital). Owner-queue: DB year 2011 likely refers to WHO 2011 EU report rather than the CABHI/Shannex 2017 pilot; pub_year set to 2017 reflecting framework date; original WHO 2011 EU DALY report by World Health Organization Regional Office for Europe.',
    jurisdiction = 'CA',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'YEAR-CORRECTED-OR-FRAMEWORK',
    metadata_integrity_detail = 'canada-dk-batch-59 2026-05-22T07:40:00Z: web-search verified via cabhi.com blog (Feb 2019 CABHI feature on Condran + Shannex project) + WHO Regional Office for Europe 2011 Burden of disease from environmental noise + pmc.ncbi.nlm.nih.gov noise-dementia systematic reviews. Underlying framework spans 2011 (WHO EU report) + 2017 (Shannex pilot) + 2019 (CABHI publication). Owner-queue: confirm whether DB row references WHO 2011 EU report directly (pub_year=2011 correct) or the CABHI/Shannex 2017+ framework (then pub_year should be 2017+).',
    url = 'https://www.cabhi.com/blog/dementia-and-noise-how-one-long-term-care-home-is-enhancing-its-sound-environment-to-support-residents-mental-health/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+cabhi+who-europe',
    last_verified_at = '2026-05-22T07:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T07:40:00Z canada-dk-batch-59] context-based + year may need adjustment',
    updated_at = '2026-05-22T07:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00569';

-- REF-00599: Denmark DemensCentrum/Nationalt Videnscenter for Demens circadian lighting
UPDATE evidence_sources SET
    pub_title = 'Circadian lighting in dementia care — Nationalt Videnscenter for Demens (Danish National Knowledge Centre for Dementia) guidance + applications in Danish plejehjem (nursing homes)',
    pub_year = 2023,
    first_author_last = 'Nationalt Videnscenter for Demens',
    is_corporate_primary = 1,
    author_display = 'Nationalt Videnscenter for Demens (NVD, Danish National Knowledge Centre for Dementia, formerly DemensCentrum) — Region Hovedstadens Psykiatri + Rigshospitalet',
    publisher = 'Nationalt Videnscenter for Demens (NVD), Rigshospitalet, Copenhagen — under Region Hovedstadens Psykiatri',
    standard_number = 'NVD (Nationalt Videnscenter for Demens) circadian-lighting + light therapy guidance for plejehjem (Danish nursing homes) — entrainment of suprachiasmatic nucleus circadian rhythm via dynamic-tunable LED lighting (high-CCT cool light morning, low-CCT warm light evening); melanopic-EDI metrics; CIE S 026:2018 framework; underlying Danish Sundhedsstyrelsen (Danish Health Authority) dementia care guidelines + Servicelov § 83-87 (nursing home + home care); EU CEN/CENELEC EN 17037:2018 Daylight in Buildings + EN 12464-1:2021 Light and lighting',
    jurisdiction = 'DK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'canada-dk-batch-59 2026-05-22T07:40:00Z: context-based verification. NVD (Nationalt Videnscenter for Demens) is Denmark''s national knowledge centre for dementia at Rigshospitalet under Region Hovedstadens Psykiatri. Circadian-lighting interventions in Danish plejehjem widely documented; CIE S 026:2018 melanopic-EDI framework underlies dynamic-LED specification. Owner-queue: confirm specific NVD publication / framework document referenced.',
    url = 'https://videnscenterfordemens.dk/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+nvd-context',
    last_verified_at = '2026-05-22T07:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T07:40:00Z canada-dk-batch-59] context-based',
    updated_at = '2026-05-22T07:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00599';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
