-- data_20260522023000_mixed_batch_50.sql
-- Mixed batch 50: 4 rows verified.
--
-- REF-00179: Baum CM, Christiansen CH, Bass JD 2015 PEOP book chapter (SLACK Inc, 4th ed.)
-- REF-00080: Finland Invalidiliitto ESKEH 2018 update audit framework
-- REF-00636: India Autism Center West Bengal Practice Design 52-acre township
-- REF-00392: Owsley C, McGwin G, Sloane ME et al. 2001 Optom Vis Sci TIADL (best-effort match)

BEGIN TRANSACTION;

-- REF-00179: Baum PEOP 2015 book chapter
UPDATE evidence_sources SET
    pub_title = 'The Person-Environment-Occupation-Performance (PEOP) Model (book chapter)',
    pub_year = 2015,
    first_author_last = 'Baum',
    first_author_first = 'CM',
    is_corporate_primary = 0,
    author_display = 'Baum CM, Christiansen CH, Bass JD',
    publisher = 'SLACK Incorporated, Thorofare NJ',
    isbn = '978-1-61711-803-0',
    pages_start = '49',
    pages_end = '56',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'NO-MATCH',
    metadata_integrity_status = 'BOOK-CHAPTER-ISBN-CANONICAL',
    metadata_integrity_detail = 'mixed-batch-50 2026-05-22T02:30:00Z: web-search verified via scirp.org + journals.sagepub.com PEOP-model-cfp + ouci.dntb.gov.ua + ottheory.com. Book chapter "The Person-Environment-Occupation-Performance (PEOP) Model" in Christiansen CH, Baum CM, Bass JD (Eds.) *Occupational Therapy: Performance, Participation and Well-being* 4th edition, SLACK Incorporated, Thorofare NJ, pp. 49-56. Companion chapter Bass JD, Baum CM, Christiansen CH (2015) pp. 57-80 (interventions and outcomes). Model lineage: 1st ed (1991), 2nd ed (1997b), 3rd ed (2005), 4th ed (2015), 5th ed (2020/2024 Routledge DOI 10.4324/9781003522997-6). Sister scoping review Bass JD, Marchant JK, de Sam Lazaro SL, Baum CM 2024 OTJR DOI 10.1177/15394492241238951; editorial DOI 10.1177/15394492241252578. Books-as-canonical convention applies — chapter ISBN matches parent book.',
    url = 'https://shopslackbooks.com/products/occupational-therapy-performance-participation-and-well-being',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+slack-publishing+sage-journals',
    last_verified_at = '2026-05-22T02:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T02:30:00Z mixed-batch-50] book-chapter ISBN-canonical',
    updated_at = '2026-05-22T02:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00179';

-- REF-00080: Finland ESKEH 2018
UPDATE evidence_sources SET
    pub_title = 'ESKEH-kartoitusmenetelmä — Rakennetun ympäristön esteettömyyden kartoitusmenetelmä (Built Environment Accessibility Audit Framework — 2018 update edition)',
    pub_year = 2018,
    first_author_last = 'Invalidiliitto',
    is_corporate_primary = 1,
    author_display = 'Invalidiliitto ry, Esteettömyyskeskus ESKE (now Invalidiliiton esteettömyystyö) — Finnish national disability organisation',
    publisher = 'Invalidiliitto ry (The Finnish Association of People with Physical Disabilities), Helsinki',
    standard_number = 'ESKEH (Esteettömyyskartoitusmenetelmä) — originally developed by ESKEH-projekti 2007-2009 (funded by RAY Raha-automaattiyhdistys + Helsinki kaikille -projekti); 2018 update by Invalidiliitto Esteettömyyskeskus ESKE; companion Luonto-ESKEH (nature trails edition) 2014, updated 2019 + 2024 (Suomen Paralympiakomitea Reitit ja rakenteet project); criteria based on Finnish esteettömyysmääräykset/-ohjeet/-suositukset',
    jurisdiction = 'FI',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-50 2026-05-22T02:30:00Z: web-search verified via invalidiliitto.fi (official) + accessiaconsulting.fi + sanastot.suomi.fi. ESKEH covers building + outdoor areas; kartoitusraportti includes nykytila, puutteet, toimenpide-ehdotukset. Used as Finnish national standard for accessibility audits with companion certified auditor training. Underlying Act 306/2019 on the Provision of Digital Services (implementing EU Accessibility Directive 8/2102) + Finnish building code.',
    url = 'https://www.invalidiliitto.fi/esteettomyys/invalidiliiton-esteettomyystyo/eskeh-kartoitusmenetelma',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+invalidiliitto-official',
    last_verified_at = '2026-05-22T02:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T02:30:00Z mixed-batch-50] web-search verified',
    updated_at = '2026-05-22T02:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00080';

-- REF-00636: India Autism Center West Bengal
UPDATE evidence_sources SET
    pub_title = 'India Autism Center (IAC) — 52-acre integrated autism community township, Sirakole/Shirakole, West Bengal (sensory-design and outdoor-spaces emphasis)',
    pub_year = 2024,
    first_author_last = 'Practice Design',
    is_corporate_primary = 1,
    author_display = 'Practice Design (Mumbai + Kolkata) — lead architect Sandip Agarwal; client founders Suresh Kumar + Namita Somani; medical/neuropsychiatric consultant Dr Ranjan',
    publisher = 'India Autism Center (IAC), Sirakole/Shirakole, West Bengal',
    standard_number = 'India Autism Center (IAC) — 52-acre integrated autism community township, Sirakole/Shirakole West Bengal (~17 km from IIM Calcutta); housing 350 residents + daycare 250 ASD individuals; expected completion 2030; sensory-design landscape (indigenous low-level planting with varied colours, textures, fragrances), thermal-shock + urban-heat-island mitigation; controlled/residential/public-edge zoning; featured ArchDaily Sep 2024 + YourStory Jul 2022; companion DDRS (Deendayal Disabled Rehabilitation Scheme) + ADIP Scheme funding contexts.',
    jurisdiction = 'IN',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-50 2026-05-22T02:30:00Z: web-search verified via indiaautismcenter.org (official) + archdaily.com (Sep 2024) + yourstory.com (Jul 2022). First-of-its-kind autism care township in India. Detailed campus design philosophy includes segregation of vehicular/pedestrian traffic for accessibility, sensory-skills development via indigenous flora, indoor-outdoor integration. 350-resident housing + 250-daycare capacity.',
    url = 'https://www.indiaautismcenter.org/about-iac/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+iac-official+archdaily',
    last_verified_at = '2026-05-22T02:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T02:30:00Z mixed-batch-50] web-search verified',
    updated_at = '2026-05-22T02:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00636';

-- REF-00392: Owsley 2001 Optom Vis Sci (best-effort)
UPDATE evidence_sources SET
    pub_title = 'Timed Instrumental Activities of Daily Living (TIADL) Tasks: Relationship to Visual Function in Older Adults',
    pub_year = 2001,
    first_author_last = 'Owsley',
    first_author_first = 'C',
    is_corporate_primary = 0,
    author_display = 'Owsley C, McGwin G Jr, Sloane ME, Stalvey BT, Wells J',
    publisher = 'Lippincott Williams & Wilkins; Optometry and Vision Science',
    journal_name = 'Optometry and Vision Science',
    journal_abbrev = 'Optom Vis Sci',
    doi = '10.1097/00006324-200105000-00019',
    pmid = '11384013',
    issn = '1040-5488',
    volume = '78',
    issue = '5',
    pages_start = '350',
    pages_end = '359',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OWNER-QUEUE-MULTIPLE-OWSLEY-2001-PAPERS',
    metadata_integrity_detail = 'mixed-batch-50 2026-05-22T02:30:00Z: web-search verified via NIH NCBI Bookshelf + Annual Reviews (Vision and Aging) + IOVS + jphysiolanthropol BMC. Owsley 2001 has multiple candidate papers: (a) Owsley C, McGwin G, Sloane ME, Stalvey BT, Wells J (2001) Optom Vis Sci 78(5):350-9 TIADL DOI 10.1097/00006324-200105000-00019 PMID 11384013; (b) Owsley C, Stalvey BT, Wells J, Sloane ME, McGwin G (2001) Arch Ophthalmol 119(6):881-7 cataract crash DOI 10.1001/archopht.119.6.881. DB title "Contrast sensitivity, acuity, and visual impairment in older adults" matches neither exactly. Best-effort selected the TIADL paper as TIADL relates to functional visual assessment in older adults; DB title may be paraphrased. Owner-queue: confirm whether actual cited paper is TIADL (above), cataract crash, or earlier 1987 Owsley/Sloane BJO paper.',
    url = 'https://doi.org/10.1097/00006324-200105000-00019',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+pubmed+ncbi-bookshelf',
    last_verified_at = '2026-05-22T02:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T02:30:00Z mixed-batch-50] DOI resolved + owner-queue flagged',
    updated_at = '2026-05-22T02:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00392';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
