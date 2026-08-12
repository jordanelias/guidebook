-- data_20260518004500_author_a18_rt60_occupied_learning_listening_spaces.sql
--
-- Phase E.1 pilot Pass 2 sub-task 2 setup. Authors the missing parent item
-- for RT60 in occupied learning and listening spaces under standing rule #3
-- (structural change) with owner directive 2026-05-18 "path a" + delegation
-- "do whatever makes sense long-term integrity".
--
-- Resolves GAP-282 (P3 OPEN): "Either (a) Simpson 2025's RT60 spec needs a
-- new A-NN item, or (b) the BPC's RT60 reference should map to a different
-- item." Path (a) chosen.
--
-- Scope clarification: A-10b ("RT60 for Hydrotherapy and Pool Environments")
-- remains unchanged. A-18 covers RT60 for occupied learning, listening, and
-- care-environment spaces (classrooms, dementia common areas, sensory rooms,
-- meeting/assembly spaces). The two items partition by context.
--
-- Population elaborations per Item 5 Option A (closed 2026-05-17):
--   spec_variant_a carries the chosen value
--   spec_variant_b carries the alternate / range / origin note
--
-- Writes:
--   1. INSERT items A-18
--   2. INSERT item_population_elaborations × 4 (DEAF, AUT, DEM, ALL-general)
--   3. INSERT item_bpc_links A-18 ↔ room-acoustic-performance (primary)
--   4. UPDATE GAP-282 → CLOSED-FIXED
--   5. INSERT data_migrations row

-- 1. The parent item
INSERT INTO items (item_code, category, name, status, created_at, created_by_session, updated_at, updated_by_session)
VALUES (
    'A-18', 'A',
    'RT60 in Occupied Learning and Listening Spaces',
    'active',
    '2026-05-18 00:45', 'session_2026-05-17-pilot-pass-2-sub-2',
    '2026-05-18 00:45', 'session_2026-05-17-pilot-pass-2-sub-2'
);

-- 2. Population elaborations (4 rows; one INSERT each for parser safety)
INSERT INTO item_population_elaborations (item_code, population_code, variant_distinction, spec_variant_a, spec_variant_b, evidence_ref_id, notes, created_at, created_by_session)
VALUES ('A-18', 'DEAF', 'deaf-hard-of-hearing-aided',
    'RT60 ≤ 0.3 s (proposed; pending rule #8 PMP walk)',
    'ANSI/ASA S12.60-2010 Part 1 specifies RT60 ≤ 0.3 s for classrooms serving children with hearing impairment',
    'REF-00325',
    'Iglehart 2020 (REF-00325, Tier 1) is the anchor for speech-perception degradation above ~0.3 s in pediatric hearing-aid/CI users. PMP walk queued as Pass 2 sub-task 2.',
    '2026-05-18 00:45', 'session_2026-05-17-pilot-pass-2-sub-2');

INSERT INTO item_population_elaborations (item_code, population_code, variant_distinction, spec_variant_a, spec_variant_b, evidence_ref_id, notes, created_at, created_by_session)
VALUES ('A-18', 'AUT', 'autism-sensory-hypersensitivity',
    'RT60 ≤ 0.4 s aspiration (conjecture rationally informed by literature)',
    'Tier-3 design recommendation 0.4-0.7 s from Bettarello 2021 (n=7 rooms, one facility); chosen ≤ 0.4 s sits at lower bound. No Tier-1 quantified threshold exists per GAP-291.',
    'REF-00561',
    'Per Item 2 sign-off (2026-05-17): NDV/AUT line carries the conjecture-rationally-informed-by-literature label. Rule #7 adversarial-research pass closed GAP-291 with 85-95% confidence in the absence claim. Rule #8 PMP for this population is expected to FAIL strict termination; the recorded PMP outcome is the structured form of the conjecture label.',
    '2026-05-18 00:45', 'session_2026-05-17-pilot-pass-2-sub-2');

INSERT INTO item_population_elaborations (item_code, population_code, variant_distinction, spec_variant_a, spec_variant_b, evidence_ref_id, notes, created_at, created_by_session)
VALUES ('A-18', 'DEM', 'dementia-common-area',
    'RT60 ≤ 0.5 s in occupied common areas',
    'Therapeutic target is acoustic calm; RT60 reduction documented as part of intervention bundles. No isolated dose-response curve in reviewed literature.',
    'REF-00571',
    'Devos 2019 (REF-00571, Tier 3) cited in BPC. Matches existing BPC language.',
    '2026-05-18 00:45', 'session_2026-05-17-pilot-pass-2-sub-2');

INSERT INTO item_population_elaborations (item_code, population_code, variant_distinction, spec_variant_a, spec_variant_b, evidence_ref_id, notes, created_at, created_by_session)
VALUES ('A-18', 'ALL', 'general-typical-hearing',
    'RT60 ≤ 0.6 s in occupied general-use indoor space',
    'Consensus value across ANSI/ASA S12.60-2010 (USA), BB93 (UK), DIN 18041:2016 (DE), UNI 11532-2:2020 (IT), AS/NZS 2107 for volumes <= 283 m^3.',
    NULL,
    'Multi-jurisdiction Tier-6 statutory convergence. Detailed citations land in step-3 jurisdiction table of the reasoning doc and in reasoning_doc_citations rows (Pass 3).',
    '2026-05-18 00:45', 'session_2026-05-17-pilot-pass-2-sub-2');

-- 3. Link A-18 to room-acoustic-performance as primary
INSERT INTO item_bpc_links (item_code, slug, link_type, rationale, created_at, created_by_session)
VALUES (
    'A-18', 'room-acoustic-performance', 'primary',
    'RT60 is the parameter; room-acoustic-performance is the BPC that defines it. First population of item_bpc_links per migration 013 + Phase E.1 pilot.',
    '2026-05-18 00:45', 'session_2026-05-17-pilot-pass-2-sub-2'
);

-- 4. Close GAP-282 (P3 OPEN: missing A-NN for RT60-occupied-school-spaces)
UPDATE gaps
SET status = 'CLOSED-FIXED',
    description = description || ' [CLOSED 2026-05-18: A-18 authored as parent item for RT60 in occupied learning and listening spaces; covers Simpson 2025 SR mapping target as well as DEAF/AUT/DEM/general elaborations per Item 5 Option A. Linked to room-acoustic-performance as primary BPC via item_bpc_links.]',
    updated_at = '2026-05-18 00:45',
    updated_by_session = 'session_2026-05-17-pilot-pass-2-sub-2'
WHERE gap_id = 'GAP-282';

-- 5. Track migration
INSERT INTO data_migrations (migration_id, applied_at, content_sha, applied_by_session, notes)
VALUES (
    'author_a18_rt60_occupied_learning_listening_spaces_2026-05-18',
    '2026-05-18 00:45',
    'insert_item_A18_4_elaborations_1_bpc_link_close_GAP_282',
    'session_2026-05-17-pilot-pass-2-sub-2',
    'Phase E.1 pilot Pass 2 sub-task 2 setup. Authors A-18 RT60-occupied-learning-listening-spaces under standing rule #3 Change Order (owner directive 2026-05-18 path a). 4 population_elaborations (DEAF/AUT/DEM/ALL). First item_bpc_links row populated. Closes GAP-282 in passing. Unblocks PMP walk for DEAF RT60 <= 0.3 s.'
);
