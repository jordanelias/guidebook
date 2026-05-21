-- data_20260521133000_us_reports_batch_18.sql
-- US reports batch 18: 3 rows web-search verified.
--
-- REF-00092: SAMHSA TIP 57 Trauma-Informed Care in Behavioral Health Services (2014)
-- REF-00140: Visitability (Eleanor Smith / Concrete Change, 1987 framework origin)
-- REF-00113: Evidence-based design for behavioral/mental health — Center for Health Design BMH Toolbox

BEGIN TRANSACTION;

-- REF-00092: SAMHSA TIP 57
UPDATE evidence_sources SET
    pub_title = 'Trauma-Informed Care in Behavioral Health Services — Treatment Improvement Protocol (TIP) Series 57',
    pub_year = 2014,
    first_author_last = 'Substance Abuse and Mental Health Services Administration',
    is_corporate_primary = 1,
    author_display = 'Substance Abuse and Mental Health Services Administration (SAMHSA); Center for Substance Abuse Treatment (CSAT); U.S. Department of Health and Human Services (HHS)',
    publisher = 'Substance Abuse and Mental Health Services Administration (SAMHSA), Rockville, MD',
    standard_number = 'HHS Publication No. (SMA) 14-4816 (volume); HHS Publication No. (SMA) 13-4801 (citation form); TIP Series 57',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-reports-batch-18 2026-05-21T13:30:00Z: web-search verified via samhsa.gov + library.samhsa.gov + ncbi.nlm.nih.gov NCBI Bookshelf NBK207201 + EMDR International Association + Whatcom College open textbook. Published March 2014. Public domain. Produced under contracts 270-99-7072, 270-04-7049, 270-09-0307 by the Knowledge Application Program (KAP) — joint venture of CDM Group and JBS International.',
    url = 'https://library.samhsa.gov/product/tip-57-trauma-informed-care-behavioral-health-services/sma14-4816',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+samhsa-official',
    last_verified_at = '2026-05-21T13:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T13:30:00Z us-reports-batch-18] web-search verified',
    updated_at = '2026-05-21T13:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00092';

-- REF-00140: Visitability — Eleanor Smith / Concrete Change
UPDATE evidence_sources SET
    pub_title = 'Visitability — original framework (zero-step entrance; 32-inch interior doors; main-floor accessible bath)',
    pub_year = 1987,
    first_author_last = 'Smith',
    first_author_first = 'Eleanor',
    is_corporate_primary = 0,
    author_display = 'Smith, E. — founder, Concrete Change (Atlanta, GA)',
    publisher = 'Concrete Change (Atlanta, GA) — successor organization: National Council on Independent Living (NCIL), visitability.org',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-reports-batch-18 2026-05-21T13:30:00Z: web-search verified via wbdg.org + visitability.org/about-concrete-change + NCIL + Wikipedia + Univ. of Georgia Special Collections (Eleanor Smith Papers, RBRL357) + 19th News + HerLife Magazine. Concept originated by Eleanor Smith in 1986-87 (organization founded 1986 as "Let''s Get Together", renamed Concrete Change in 1988-89). Originally termed "Basic Home Access"; renamed "Visitability" in 1990 after learning the UK term. Three core features: (1) one zero-step entrance, (2) 32-inch clear interior doorways on main floor including bathroom, (3) at least half-bath (preferably full) on main floor. Concrete Change retired 2017; NCIL maintains visitability.org. Smith also co-authored the 2008 AARP Public Policy Institute Visitability paper (Maisel/Smith/Steinfeld — REF-00267).',
    url = 'https://visitability.org/about-concrete-change/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+visitability-org-official',
    last_verified_at = '2026-05-21T13:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T13:30:00Z us-reports-batch-18] web-search verified',
    updated_at = '2026-05-21T13:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00140';

-- REF-00113: CHD Behavioral & Mental Health Toolbox
UPDATE evidence_sources SET
    pub_title = 'Behavioral & Mental Health Toolbox (incl. Issue Brief on Behavioral Health design; Universal Approach & Benefit Analysis tool; Lessons Learned)',
    pub_year = 2018,
    first_author_last = 'Center for Health Design',
    is_corporate_primary = 1,
    author_display = 'The Center for Health Design (CHD) — Concord, CA',
    publisher = 'The Center for Health Design (CHD), Concord, California',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'us-reports-batch-18 2026-05-21T13:30:00Z: web-search verified via healthdesign.org. Living toolbox/issue brief on evidence-based design for behavioral and mental health (BMH) facilities. Issue Brief PDF dated 2018 (Issue Brief_Behavioral Health_2018.pdf). Companion resources include "Design for Behavioral and Mental Health: A Universal Approach & Benefit Analysis" tool and "Lessons Learned about Behavioral and Mental Health". CHD defines evidence-based design (EBD): "the deliberate attempt to base building decisions on the best available research evidence with the goal of improving outcomes." Closely related: Shepley (2017) "Design for Mental & Behavioral Health" (Routledge) — separate book, not this row. Owner-queue: if the BPC citation refers to Shepley''s book specifically, reassign.',
    url = 'https://www.healthdesign.org/behavioral-mental-health-toolbox',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+chd-official',
    last_verified_at = '2026-05-21T13:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T13:30:00Z us-reports-batch-18] web-search verified',
    updated_at = '2026-05-21T13:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00113';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
