-- data_20260521094000_au_reports_batch_11.sql
--
-- AU reports batch 11: 5 rows web-search verified.
-- Per DR-2026-05-18 statutory-metadata-completeness gray-lit / regulatory protocol.
--
-- REF-00075: Winkler et al. (2024) Supporting design and construction sector — Summer Foundation
-- REF-00076: Newton, Carnemolla, Darcy (2023) UTS Inclusive Bathroom Design (and REF-00153 dup-of)
-- REF-00153: dup-of REF-00076
-- REF-00315: NDIS Home Modifications (NDIA Operational Guideline)
-- REF-00501: Dementia Australia "Designing Dementia-Friendly Care Environments"

BEGIN TRANSACTION;

-- REF-00075: Winkler 2024 Summer Foundation
UPDATE evidence_sources SET
    pub_title = 'Supporting the design and construction sector to transition to minimum accessible standards in new homes: A qualitative study',
    pub_year = 2024,
    first_author_last = 'Winkler',
    first_author_first = 'Di',
    is_corporate_primary = 0,
    author_display = 'Winkler, D.; Liddicoat, S.; D''Cruz, K.; Wellecke, C.; Mulherin, P.; Douglas, J.',
    author_count = 6,
    author_count_is_complete = 1,
    publisher = 'Summer Foundation (Melbourne, Australia)',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'au-reports-batch-11 2026-05-21T09:40:00Z: web-search verified via summerfoundation.org.au + apo.org.au/node/326951 + ABC News reporting. Published 15 Apr 2024 by Summer Foundation. Qualitative study of 16 design/construction professionals (6 builders, 5 architects, 2 developers, 3 access consultants) on integrating accessibility standards in 2022 National Construction Code at Livable Housing Australia Design Silver Standard. Supports the Building Better Homes campaign. APO node 326951.',
    url = 'https://www.summerfoundation.org.au/resources/supporting-the-design-and-construction-sector-to-transition-to-minimum-accessible-standards-in-new-homes-a-qualitative-study/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+summer-foundation-official',
    last_verified_at = '2026-05-21T09:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T09:40:00Z au-reports-batch-11] web-search verified',
    updated_at = '2026-05-21T09:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00075';

-- REF-00076: Newton 2023 UTS bathroom
UPDATE evidence_sources SET
    pub_title = 'An Inclusive and Embodied Approach to Accessible Bathroom Design for Powered and Manual Wheelchair Users',
    pub_year = 2023,
    first_author_last = 'Newton',
    is_corporate_primary = 0,
    author_display = 'Newton, D.; Carnemolla, P.; Darcy, S. (UTS Disability Research Network); with Madon F. & Relf M. (industry collaborators); co-designed with Spinal Cord Injuries Australia & Physical Disability Council NSW',
    publisher = 'University of Technology Sydney (UTS) Disability Research Network — in partnership with Spinal Cord Injuries Australia (SCIA) and Physical Disability Council NSW',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00153',
    metadata_integrity_detail = 'au-reports-batch-11 2026-05-21T09:40:00Z: web-search verified via Access Insight Autumn 2024 (ACA reprint) + UTS Disability Research Network references. Used 3D scanning methodology to evaluate public bathroom design against Australian Design for Access and Mobility (AS 1428.1). Preliminary findings: high level of unsatisfactory placement of key access features. Owner: REF-00076 and REF-00153 appear to cite the same research output — consider consolidating.',
    url = 'https://access.asn.au/access-insight-autumn-2024-new-uts-research-lifts-the-lid-on-how-wheelchair-users-access-public-bathrooms-reprint/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+aca-reprint',
    last_verified_at = '2026-05-21T09:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T09:40:00Z au-reports-batch-11] web-search verified; flagged as potential duplicate of REF-00153',
    updated_at = '2026-05-21T09:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00076';

-- REF-00153: dup-of REF-00076
UPDATE evidence_sources SET
    pub_title = 'An Inclusive and Embodied Approach to Accessible Bathroom Design for Powered and Manual Wheelchair Users',
    pub_year = 2023,
    first_author_last = 'Newton',
    is_corporate_primary = 0,
    author_display = 'Newton, D.; Carnemolla, P.; Darcy, S. (UTS Disability Research Network); with Madon F. & Relf M.; co-designed with Spinal Cord Injuries Australia & Physical Disability Council NSW',
    publisher = 'University of Technology Sydney (UTS) Disability Research Network',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00076',
    metadata_integrity_detail = 'au-reports-batch-11 2026-05-21T09:40:00Z: web-search verified. Same research as REF-00076 — both citations appear to point to the Newton/Carnemolla/Darcy 2023 UTS bathroom research project. Owner: consider consolidating REF-00076 + REF-00153.',
    url = 'https://access.asn.au/access-insight-autumn-2024-new-uts-research-lifts-the-lid-on-how-wheelchair-users-access-public-bathrooms-reprint/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+aca-reprint',
    last_verified_at = '2026-05-21T09:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T09:40:00Z au-reports-batch-11] web-search verified; flagged as potential duplicate of REF-00076',
    updated_at = '2026-05-21T09:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00153';

-- REF-00315: NDIS Home Modifications
UPDATE evidence_sources SET
    pub_title = 'NDIS Home Modifications — Operational Guideline (Capital Supports; reasonable and necessary; OT assessment required)',
    pub_year = 2024,
    first_author_last = 'National Disability Insurance Agency',
    is_corporate_primary = 1,
    author_display = 'National Disability Insurance Agency (NDIA), Australian Government',
    publisher = 'National Disability Insurance Agency (NDIA), Australian Government',
    standard_number = 'NDIS AT Code Guide — Assistive Technology, Home Modifications and Consumables Code Guide',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'au-reports-batch-11 2026-05-21T09:40:00Z: web-search verified via NDIS Quarterly Reports + multiple secondary explanatory sources. NDIS Home Modifications fund "reasonable and necessary" structural and non-structural changes to a participant''s home to enable independent and safe living. Requires OT assessment and report. Capital Supports component of NDIS plan. Statutory authority: National Disability Insurance Scheme Act 2013 (Cth) + NDIS rules. Stored row description is a general program-level claim; the canonical document is the NDIS Operational Guideline on Home Modifications.',
    url = 'https://www.ndis.gov.au/participants/using-your-plan/equipment-and-technology/home-modifications',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+ndis-official',
    last_verified_at = '2026-05-21T09:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T09:40:00Z au-reports-batch-11] web-search verified',
    updated_at = '2026-05-21T09:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00315';

-- REF-00501: Dementia Australia Designing Dementia-Friendly Care Environments
UPDATE evidence_sources SET
    pub_title = 'Designing dementia-friendly care environments',
    first_author_last = 'Dementia Australia',
    is_corporate_primary = 1,
    author_display = 'Dementia Australia; built on the evidence-based work of Prof Richard Fleming and Kirsty Bennett (University of Wollongong)',
    publisher = 'Dementia Australia',
    jurisdiction = 'AU',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'au-reports-batch-11 2026-05-21T09:40:00Z: web-search verified via dementia.org.au + Aged Care Quality and Safety Commission (which mirrors the resource). Living resource on dementia-friendly design principles for care homes, hospitals, and day centres. Year unknown — resource is updated over time. Companion to Fleming & Bennett''s Environmental Audit Tool (EAT) and related dementia-design audit instruments.',
    url = 'https://www.dementia.org.au/professionals/designing-dementia-friendly-care-environments',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+dementia-australia-official',
    last_verified_at = '2026-05-21T09:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T09:40:00Z au-reports-batch-11] web-search verified',
    updated_at = '2026-05-21T09:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00501';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
