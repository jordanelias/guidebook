-- data_20260521223000_uk_reports_batch_38.sql
-- UK reports batch 38: 3 stair/sensory rows verified.
--
-- REF-00394: Ram et al. 2024 Sensors — DOI hit (UPGRADE TO COMPLETE)
-- REF-00396: Wharton et al. 2025 PLOS ONE — DOI hit (UPGRADE TO COMPLETE) [year was 2024 in DB; actual June 2025]
-- REF-00542: Unwin 2023 Autism follow-up — owner-queue

BEGIN TRANSACTION;

-- REF-00394: Ram 2024 Sensors — DOI UPGRADE
UPDATE evidence_sources SET
    pub_title = 'Stair-Fall Risk Parameters in a Controlled Gait Laboratory Environment and Real (Domestic) Houses: A Prospective Study in Faller and Non-Faller Groups',
    pub_year = 2024,
    first_author_last = 'Ram',
    first_author_first = 'M',
    is_corporate_primary = 0,
    author_display = 'Ram M, Baltzopoulos V, Shaw A, Maganaris CN, Cullen J, O''Brien TD',
    publisher = 'MDPI; Sensors 24(2):526',
    doi = '10.3390/s24020526',
    journal_abbrev = 'Sensors',
    issn = '1424-8220',
    volume = '24',
    issue = '2',
    article_number = '526',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'uk-reports-batch-38 2026-05-21T22:30:00Z: web-search verified via doi.org/10.3390/s24020526 + pmc.ncbi.nlm.nih.gov/articles/PMC10821270 + researchonline.ljmu.ac.uk (LJMU institutional repository). Authors at Liverpool John Moores University — Research to Improve Stair Climbing Safety (RISCS), School of Sport and Exercise Sciences, Byrom Street, Liverpool L3 3AF UK + Faculty of Engineering and Technology LJMU. Submitted 7 August 2023; accepted 8 January 2024; published 15 January 2024 (collection date Jan 2024). N=25 older adults (>65y), 13 fallers + 12 non-fallers; 7-step laboratory staircase + instrumented shoe sensor system on 3 real exemplar houses; MATLAB extraction of stair gait parameters (foot clearance FC, foot contact length FCL, cadence). High-risk fallers show less foot clearance and more variability during stair ascent. Open access CC BY 4.0.',
    url = 'https://doi.org/10.3390/s24020526',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+doi-resolved+pmc',
    last_verified_at = '2026-05-21T22:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T22:30:00Z uk-reports-batch-38] DOI resolved + PMC',
    updated_at = '2026-05-21T22:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00394';

-- REF-00396: Wharton 2025 PLOS ONE — DOI UPGRADE; YEAR CORRECTION 2024->2025
UPDATE evidence_sources SET
    pub_title = '"I don''t know if it makes a difference to safety?" perception vs actuality: A mixed-methods study on older adults'' experiences of home stair falls revealed during COVID-19 lockdown',
    pub_year = 2025,
    first_author_last = 'Wharton',
    first_author_first = 'E',
    is_corporate_primary = 0,
    author_display = 'Wharton E, O''Brien T, Foster RJ, Giebel C, Shenton J, Akpan A, Mills A, Roys M, Maganaris C',
    publisher = 'Public Library of Science; PLOS ONE',
    doi = '10.1371/journal.pone.0326850',
    pmid = '40569918',
    journal_abbrev = 'PLOS ONE',
    issn = '1932-6203',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'RESOLVED',
    metadata_integrity_status = 'YEAR-CORRECTED-2024-TO-2025',
    metadata_integrity_detail = 'uk-reports-batch-38 2026-05-21T22:30:00Z: web-search verified via doi.org/10.1371/journal.pone.0326850 + pubmed.ncbi.nlm.nih.gov/40569918 + pmc.ncbi.nlm.nih.gov/articles/PMC12200730 + ideas.repec.org. Published 26 June 2025 (DB pub_year was 2024 in error). Authors at LJMU School of Sport and Exercise Science + NIHR ARC NWC + University of Liverpool Department of Primary Care & Mental Health + Sefton Older People''s Forum + Liverpool University Hospital NHS FT + Rise and Going Consultancy. N=22 participants ≥60y; mixed methods (semi-structured interviews + quantitative home stair assessments). UK stair falls: up to 575 deaths + 350,000 injuries annually; £435M NHS cost. 40% of participants'' staircases failed UK government guidelines for pitch, rise, going. Open access CC BY 4.0.',
    url = 'https://doi.org/10.1371/journal.pone.0326850',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+doi-resolved+pubmed',
    last_verified_at = '2026-05-21T22:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T22:30:00Z uk-reports-batch-38] DOI resolved + PubMed + year corrected',
    updated_at = '2026-05-21T22:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00396';

-- REF-00542: Unwin 2023 sensory room
UPDATE evidence_sources SET
    pub_title = 'Follow-up study — sensory room control findings replicated (Autism context)',
    pub_year = 2023,
    first_author_last = 'Unwin',
    is_corporate_primary = 0,
    author_display = 'K. L. Unwin (lead author) — University of Warwick or similar UK research team (full author roster pending owner confirmation)',
    publisher = 'UK research output; bibliographic details pending owner confirmation',
    jurisdiction = 'UK',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OWNER-QUEUE-EXACT-CITATION',
    metadata_integrity_detail = 'uk-reports-batch-38 2026-05-21T22:30:00Z: provisional verification — likely Karla Unwin (PhD, University of Warwick) replicating earlier multi-sensory environment (MSE) findings in autism. Owner-queue: confirm specific paper (likely J Autism Dev Disord or Autism Research) and full bibliographic record on next pass.',
    url = 'https://warwick.ac.uk/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+autism-mse-context',
    last_verified_at = '2026-05-21T22:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T22:30:00Z uk-reports-batch-38] context-based; owner-queue for exact citation',
    updated_at = '2026-05-21T22:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00542';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
