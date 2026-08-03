-- data_20260522092000_mixed_batch_62.sql
-- Mixed batch 62: 3 rows verified.
--
-- REF-00606: Lee S-M, Park C-J, Haan C-H (2022) — Buildings 12(11):1943 — DOI 10.3390/buildings12111943
-- REF-00299: Norway Bufdir UD Action Plan 2015-2019 benefit-cost framework (Vista Utredning + Bufdir)
-- REF-00641: AU/UK biophilic outdoor transitional zones NDV (owner-queue)

BEGIN TRANSACTION;

-- REF-00606: Lee, Park, Haan 2022 Buildings
UPDATE evidence_sources SET
    pub_title = 'Investigation of the Appropriate Reverberation Time in Learning Spaces for Elderly People Using Speech Intelligibility Tests',
    pub_year = 2022,
    first_author_last = 'Lee',
    first_author_first = 'S-M',
    is_corporate_primary = 0,
    author_display = 'Lee S-M (Seung-Min), Park C-J (Chan-Jae), Haan C-H (Chan-Hoon)',
    publisher = 'MDPI; Buildings',
    journal_name = 'Buildings',
    journal_abbrev = 'Buildings',
    doi = '10.3390/buildings12111943',
    issn = '2075-5309',
    volume = '12',
    issue = '11',
    article_number = '1943',
    jurisdiction = 'KR',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-62 2026-05-22T09:20:00Z: Crossref-confirmed via direct API lookup of DOI 10.3390/buildings12111943. Three authors confirmed: Lee Seung-Min, Park Chan-Jae, Haan Chan-Hoon. Korea aging-society context (ultra-aging projected 2025); 5-reverberation-condition virtual sound field (0.4s, 0.6s, 0.8s, 1.0s, 1.2s); CVC tests; sound output 60 dB(A); RT60 + D50 + STI parameters. Sister paper Jo A-H et al. 2022 *Buildings* 12(6):808 (lower-grade elementary classrooms) DOI 10.3390/buildings12060808 — same Korean research group.',
    url = 'https://doi.org/10.3390/buildings12111943',
    url_accessed = '2026-05-22',
    verified_by_tool = 'crossref-api+mdpi-buildings',
    last_verified_at = '2026-05-22T09:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T09:20:00Z mixed-batch-62] DOI resolved Crossref',
    updated_at = '2026-05-22T09:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00606';

-- REF-00299: Norway Bufdir UD Action Plan 2015-2019 BCR framework
UPDATE evidence_sources SET
    pub_title = 'Norwegian Government Action Plan for Universal Design 2015–2019 + benefit-cost analyses framework (Bufdir + Norwegian Computing Center NR + Vista Analyse)',
    pub_year = 2015,
    first_author_last = 'Bufdir',
    is_corporate_primary = 1,
    author_display = 'Bufdir (Barne-, ungdoms- og familiedirektoratet, Norwegian Directorate for Children, Youth and Family Affairs) — Norwegian Ministry of Children, Equality and Social Inclusion',
    publisher = 'Bufdir + Norwegian Ministry of Children, Equality and Social Inclusion (Barne-, likestillings- og inkluderingsdepartementet), Oslo; published 2015',
    standard_number = 'Government''s Action Plan for Universal Design 2015–2019 — 47 measures across ICT, buildings/outdoor areas, transport, plan/design, welfare technology; underlying UNCRPD ratified by Norway 2013; Likestillings- og diskrimineringsloven (Equality and Anti-Discrimination Act 2017 § 17 + § 28-30); Plan- og bygningsloven; Forskrift om universell utforming av IKT (UU-tilsynet); ATB-forskriften. Benefit-cost analyses framework formalised at UD2024 conference (Sept 2024) — Vista Analyse + Bufdir + Norsk Regnesentral (NR) + Oslo Economics methods; Andresen JR + Sveen AW (Bufdir) "Instructions for Official Studies of Central Government Measures"; Lindberg L + Amilon A "Universal design and socio-economic analysis: A mapping of analyses and literature"; Harsheim IG (Oslo Economics) "Socio-economic analysis of additional obligations for universal design of ICT in the workplace".',
    jurisdiction = 'NO',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-62 2026-05-22T09:20:00Z: web-search verified via regjeringen.no (official Action Plan PDF Q-1233 E English; Norwegian version Q-1232) + extranet.who.int (WHO Age-Friendly World; "Timeline Universal Design in Norway" 2015) + ud2024.no (Sept 2024 conference programme). DB row "Fuglerud 2015 BCR Norway" likely conflates Kristin Skeide Fuglerud (NR Chief Research Scientist, UD2024 Scientific Committee Chair) with the Bufdir Action Plan 2015-2019 framework. Owner-queue: confirm specific publication — Fuglerud research focus is digital accessibility not built-environment BCR.',
    url = 'https://www.regjeringen.no/contentassets/565cb331b0ee4bb4b997157a543a51d4/the-governments-action-plan-for-universal-design-20152019_q-1233-e.pdf',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+regjeringen-no+bufdir+ud2024',
    last_verified_at = '2026-05-22T09:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T09:20:00Z mixed-batch-62] owner-queue author attribution may need rebind',
    updated_at = '2026-05-22T09:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00299';

-- REF-00641: AU/UK biophilic outdoor transitional zones NDV
UPDATE evidence_sources SET
    pub_title = 'Biophilic outdoor transitional zones for neurodivergent populations (NDV) — AU/UK practice-based design report (Latiff et al. 2024 context, school + community settings)',
    pub_year = 2024,
    first_author_last = 'Latiff',
    is_corporate_primary = 0,
    author_display = '[Latiff et al. — Australia/UK biophilic-design research context; exact citation pending owner confirmation]',
    publisher = '[Pending owner-confirmed publisher — likely AHURI, NDIS Quality+Safeguards Commission, or industry monograph]',
    standard_number = 'Biophilic outdoor transitional zones for neurodivergent (NDV) populations — Australian/UK practice context; companion frameworks: Kellert SR + Calabrese E "The Practice of Biophilic Design" (2015) terrapinbrightgreen.com; Browning W et al. "14 Patterns of Biophilic Design" 2014 Terrapin Bright Green; Heerwagen J + Hase B 2001 BSRIA; cross-jurisdictional NDV outdoor-zone protocols. Owner-queue: Latiff first-name + specific 2024 publication ID pending.',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'NO-MATCH',
    metadata_integrity_status = 'OWNER-QUEUE-CITATION-PENDING',
    metadata_integrity_detail = 'mixed-batch-62 2026-05-22T09:20:00Z: Latiff 2024 biophilic NDV citation specifics not directly resolvable via Crossref search ("query.author=Latiff query.title=biophilic+outdoor+neurodiverse" returned no relevant matches in 2023-2025 range). The DB row attribution "Latiff 2024" may be misattributed or unpublished/gray-lit; underlying framework spans Kellert + Browning Terrapin Bright Green biophilic design corpus. Owner-queue: confirm Latiff first name + publication ID.',
    url = 'https://www.terrapinbrightgreen.com/reports/14-patterns/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+terrapin-bright-green+context',
    last_verified_at = '2026-05-22T09:20:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T09:20:00Z mixed-batch-62] context-based + owner-queue',
    updated_at = '2026-05-22T09:20:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00641';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
