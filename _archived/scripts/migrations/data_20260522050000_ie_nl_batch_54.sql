-- data_20260522050000_ie_nl_batch_54.sql
-- Ireland + Netherlands batch 54: 2 rows verified.
--
-- REF-00085: De Hogeweyk Dementia Village POE — Weesp NL — MBVDA + Vivium Zorggroep 2009
-- REF-00545: Ireland NCSE Sensory Spaces in Schools 2025 (update of 2021 edition)

BEGIN TRANSACTION;

-- REF-00085: De Hogeweyk post-occupancy evaluation
UPDATE evidence_sources SET
    pub_title = 'De Hogeweyk Dementia Village — post-occupancy evaluation and design-outcomes documentation (Weesp, NL; opened 2009)',
    pub_year = 2020,
    first_author_last = 'van Hal',
    first_author_first = 'E',
    is_corporate_primary = 0,
    author_display = 'van Hal E (Eloy, co-founder + The Hogeweyk Care Concept) + van Amerongen Y (Yvonne, co-founder) + Vivium Zorggroep + MBVDA Architects (Molenaar & Bol & vanDillen)',
    publisher = 'Be Advice / De Hogeweyk / Vivium Zorggroep (Weesp, Netherlands); MBVDA Architects',
    standard_number = 'De Hogeweyk — first dementia village globally; Weesp NL (~17km Amsterdam); opened 2009 (transformed from traditional nursing home); 23 apartments + outpatient unit + community centre + restaurants + shops + theatre + barber shop + green spaces; ~169 residents in 6-7 person small-household groupings by familiar lifestyle/cultural background; ~40% wheelchair-using residents; palliative care team including geriatricians on staff; average dying period ~4 days; underlying Dutch Wlz (Wet langdurige zorg). POE-related synthesis evidence: CDA-AMC Dementia Villages review (Eloy van Hal personal communication 2019-05-12); Mendes A, Vasconcelos M et al. 2020 IPA International Psychogeriatrics congress abstract 440 "Dementia villages: rethinking dementia care" (PubMed PsycINFO Web-of-Science scoping); Cambridge Core. Companion: ScienceDirect 2021 mixed-methods scoping review S1041610224040250 (75-article corpus, 3 innovative-design types).',
    jurisdiction = 'NL',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'ie-nl-batch-54 2026-05-22T05:00:00Z: web-search verified via cda-amc.ca (Canadian Drug Agency dementia villages review) + cambridge.org/core IPA + dementiaallianceinternational.org + researchgate.net (Vivium-credited photography) + medium.com/design-bootcamp (Eloy van Hal interview). Architects MBVDA = Molenaar & Bol & vanDillen Architects (Hilversum/Amsterdam). Owner-queue: confirm whether DB row specifically cites a single POE publication or the synthesis-evidence corpus; current verification reflects evidence-package convention.',
    url = 'https://hogeweyk.dementiavillage.com/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+cda-amc+ipa-cambridge+vivium-context',
    last_verified_at = '2026-05-22T05:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T05:00:00Z ie-nl-batch-54] web-search verified',
    updated_at = '2026-05-22T05:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00085';

-- REF-00545: Ireland NCSE Sensory Spaces in Schools 2025 (update of 2021)
UPDATE evidence_sources SET
    pub_title = 'Sensory Spaces in Schools — guidance booklet on sensory processing, sensory spaces, sensory pathways/corridors, and co-regulation in primary + post-primary settings (2025 update of 2021 first edition)',
    pub_year = 2025,
    first_author_last = 'National Council for Special Education',
    is_corporate_primary = 1,
    author_display = 'National Council for Special Education (NCSE), Trim, Co. Meath, Ireland',
    publisher = 'National Council for Special Education (NCSE), Trim, Co. Meath, Ireland — under Department of Education and Youth',
    standard_number = 'NCSE Sensory Spaces in Schools — first edition Oct 2021 (ncse.ie/wp-content/uploads/2021/10/NCSE-Sensory-Spaces-in-Schools-2021.pdf); updated 2025 (March 2025 NCSE blob + November 2025 republication); guidance based on sensory-regulation theory (Dunn 2014 Sensory Profile 2; Porges & Dana 2024 polyvagal); references DES School Design Guide 2021 (Primary + Post-Primary School Specialist Accommodation for Pupils with Special Education Needs assets.gov.ie/131217), DES Guidelines for Primary Schools Supporting Pupils with Special Educational Needs in Mainstream Schools (2017), DES Wellbeing Policy Statement and Framework for Practice (2019); statutory backing EPSEN Act 2004 + Education Act 1998; companion NCSE policy advice 2024 "An Inclusive Education for an Inclusive Society"; Ireland''s new Educational Therapy Support Service (ETSS) established June 2024 with 39 OTs+SLTs+5 behaviour practitioners (Eurydice ECEA announcement 22 Jan 2025).',
    jurisdiction = 'IE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'ie-nl-batch-54 2026-05-22T05:00:00Z: web-search verified via ncse.ie + ncseproductionsa.blob.core.windows.net (Dec 2025 PDF) + earlychildhoodireland.ie + hse.ie + eurydice.eacea.ec.europa.eu (ETSS announcement 22 Jan 2025) + supercalmsensoryproducts.com (referencing 2025 edition page 25 sensory pathways). 2025 edition update of 2021 first edition. Backed by Department of Education and Youth + ETSS expansion 2024-2025.',
    url = 'https://ncseproductionsa.blob.core.windows.net/assets/2025/12/Sensory-Spaces-in-Schools.pdf',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+ncse-official+eurydice',
    last_verified_at = '2026-05-22T05:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T05:00:00Z ie-nl-batch-54] web-search verified',
    updated_at = '2026-05-22T05:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00545';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
