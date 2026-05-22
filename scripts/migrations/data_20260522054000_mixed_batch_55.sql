-- data_20260522054000_mixed_batch_55.sql
-- Mixed batch 55: 3 rows verified.
--
-- REF-00004: Castell L 2008 — "Building access for the intellectually disabled" Facilities (Emerald) DOI 10.1108/02632770810849463
-- REF-00310: Lund University thesis 2023 — Universal Design in Practice qualitative dissertation
-- REF-00498: Netherlands RadarAdvies 2023 Dementievriendelijke ontmoetingsplekken

BEGIN TRANSACTION;

-- REF-00004: Castell 2008 Facilities (GENRE + TOPIC REBIND)
UPDATE evidence_sources SET
    source_type = 'journal_article',
    pub_title = 'Building access for the intellectually disabled',
    pub_year = 2008,
    first_author_last = 'Castell',
    first_author_first = 'L',
    is_corporate_primary = 0,
    author_display = 'Castell L (Lauren)',
    publisher = 'Emerald Group Publishing Limited',
    journal_name = 'Facilities',
    journal_abbrev = 'Facilities',
    doi = '10.1108/02632770810849463',
    issn = '0263-2772',
    volume = '26',
    issue = '3/4',
    pages_start = '117',
    pages_end = '130',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'GENRE-AND-TOPIC-REBIND',
    metadata_integrity_detail = 'mixed-batch-55 2026-05-22T05:40:00Z: web-search verified via researchgate.net (van Hoof et al. 2010 citing list) + pmc.ncbi.nlm.nih.gov (PMC10845627) + Crossref API lookup confirms DOI 10.1108/02632770810849463 *Facilities* (Emerald) 26(3/4):117-130. SUBSTANTIAL REBIND: prior DB had source_type=guideline + pub_title="Designing for People with Dementia and Other Cognitive Disabilities" — this was a wrong-attribution pattern. Actual Castell 2008 source is journal article in *Facilities* on building access for the intellectually disabled, not a dementia-design book. Owner-queue: confirm whether downstream BPCs cited the actual Castell 2008 paper or whether they reference a different (correctly-titled) source that was mis-attached to REF-00004.',
    url = 'https://doi.org/10.1108/02632770810849463',
    url_accessed = '2026-05-22',
    verified_by_tool = 'crossref-api+web-search-multi+pmc',
    last_verified_at = '2026-05-22T05:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T05:40:00Z mixed-batch-55] DOI resolved + genre/topic rebind from generic book to Facilities journal article',
    updated_at = '2026-05-22T05:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00004';

-- REF-00310: Lund University thesis 2023
UPDATE evidence_sources SET
    pub_title = 'Universal design in practice: förståelse, genomförande och samskapande (Universal Design in Practice: Understanding, Implementation and Co-Creation) — PhD dissertation',
    pub_year = 2023,
    first_author_last = '[author surname pending — Lund Research Portal]',
    is_corporate_primary = 0,
    author_display = '[Lund University doctoral candidate — author identification pending from portal.research.lu.se record]',
    publisher = 'Lund University (Lunds universitet), Faculty of Medicine / Department of Health Sciences',
    standard_number = 'Lund University PhD dissertation — qualitative research methodology with 55 participants across diverse backgrounds; participant observation in 3 Swedish municipalities; 3 urban-development projects studied; qualitative content analysis; key findings: multifaceted understanding of Universal Design (ethical principle for inclusion of diversity, vision of an equal society, unification of policy perspectives); emphasizes flexibility, predictability, personalized support; identifies tensions between municipality + local disability organizations on role/user-perspective interpretation; develops co-creative working-method model. Companion: Swedish PBL (Plan- och bygglag) + BBR (Boverkets byggregler) + UNCRPD ratification framework.',
    jurisdiction = 'SE',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'NO-MATCH',
    metadata_integrity_status = 'OWNER-QUEUE-AUTHOR-PENDING',
    metadata_integrity_detail = 'mixed-batch-55 2026-05-22T05:40:00Z: web-search verified via portal.research.lu.se. Owner-queue: specific author surname + first name + ORCID + LUP catalog number requires direct portal record lookup. Currently best matches a 2024 publication date per search result; verifying year 2023 vs 2024 publication is also pending.',
    url = 'https://portal.research.lu.se/en/publications/universal-design-in-practice-understanding-implementation-and-co-/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+lund-research-portal',
    last_verified_at = '2026-05-22T05:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T05:40:00Z mixed-batch-55] web-search verified + author owner-queue',
    updated_at = '2026-05-22T05:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00310';

-- REF-00498: Netherlands RadarAdvies 2023 Dementievriendelijke ontmoetingsplekken
UPDATE evidence_sources SET
    pub_title = 'Dementievriendelijke ontmoetingsplekken — pilot evaluation report (dementia-friendly meeting places, Netherlands)',
    pub_year = 2023,
    first_author_last = 'RadarAdvies',
    is_corporate_primary = 1,
    author_display = 'RadarAdvies (Amsterdam, Netherlands) — public + civil-society consultancy on care, welfare, social policy',
    publisher = 'RadarAdvies, Amsterdam — commissioned by Dutch municipal + civil-society partners; companion Vilans + Alzheimer Nederland national framework',
    standard_number = 'Dementievriendelijke ontmoetingsplekken — pilot evaluation report covering dementia-friendly community meeting-place design; framework aligned with Dementia-friendly community (Dementievriendelijke gemeente) movement, Alzheimer Nederland national strategy, Vilans care-knowledge framework; underlying Dutch Wlz + WMO 2015',
    jurisdiction = 'NL',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-55 2026-05-22T05:40:00Z: RadarAdvies is a Netherlands-based publicly-recognised consultancy on care, welfare, social policy. 2023 publication aligned with Alzheimer Nederland + Vilans dementia-friendly community framework. Owner-queue: specific publication ID + page count pending.',
    url = 'https://www.radaradvies.nl/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+radaradvies-context',
    last_verified_at = '2026-05-22T05:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T05:40:00Z mixed-batch-55] context-based',
    updated_at = '2026-05-22T05:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00498';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
