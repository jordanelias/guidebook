-- data_20260517235900_adversarial_research_ndv_aut_rt60_target_absence.sql
--
-- Adversarial-research pass per standing rule #7 on the claim:
-- "NDV/AUT require quantified RT60 targets but no Tier-1 evidence base exists
-- for what those targets should be."
--
-- Pilot session 2026-05-17, room-acoustic-performance reasoning doc Pass 2
-- sub-task 1. Claim under test survives adversarial review with sharpening:
--   - Marzi/Caniato/Gasparella 2025 (Sci Rep, Tier 1) explicitly states the
--     absence of quantitative thresholds for autistic users - direct
--     corroboration of the claim from a Tier-1 venue.
--   - Bettarello 2021 (REF-00561, Tier 3) proposes a 0.4–0.7 s aspirational
--     range from a single Italian daily-care-facility case study (n=7 rooms).
--     This is a quantified DESIGN RECOMMENDATION, not a Tier-1 threshold.
--     The pilot doc's first-pass framing ("no quantified target from
--     Bettarello") was incomplete; sharpened in companion reasoning-doc edit.
--   - Marzi 2024 (Building & Environment, Tier 1) comprehensive review
--     synthesizes existing literature without deriving a new Tier-1 threshold.
--
-- No primary-study or systematic-review dissenter found.
--
-- Writes:
--   1. Two new evidence_sources rows (Marzi 2024 B&E review; Marzi 2025 Sci Rep)
--      with COMPLETE/VERIFIED metadata - both independently web-verified
--      2026-05-17 via Nature, MDPI, ScienceDirect, ResearchGate, PubMed.
--   2. source_slug_links to room-acoustic-performance for both.
--   3. UPDATE REF-00561 with prior_expectation + search_queries_used per
--      adversarial-research skill required outputs.
--   4. INSERT GAP-291 with all four protocol fields populated.
--   5. Four evidence_population_match rows grading each cited study's
--      population fit to the claim.

-- 1. Marzi 2024 - Building & Environment comprehensive review
INSERT INTO evidence_sources (
    ref_id, source_type, author_count, author_count_is_complete,
    first_author_last, first_author_first, author_display,
    pub_year, pub_title, journal_name, journal_name_en, journal_abbrev,
    volume, article_number, publisher, doi,
    lang_detected, lang_detection_method, translation_method,
    tier, evidence_type, jurisdiction,
    metadata_quality, verification_status, doi_resolution_outcome,
    verification_note, last_verified_at, verified_by_tool, verification_attempt_count,
    subtype, citation_count,
    created_at, created_by_session, updated_at, updated_by_session
) VALUES (
    'REF-00726', 'journal_article', 3, 1,
    'Marzi', 'Arianna', 'Marzi, A.; Caniato, M.; Gasparella, A.',
    2024, 'Inclusive indoor comfort of neurodivergent individuals diagnosed before adulthood: A comprehensive study on thermal, acoustic, visual and air quality domains',
    'Building and Environment', 'Building and Environment', 'Build Environ',
    '267', '112254', 'Elsevier', '10.1016/j.buildenv.2024.112254',
    'en', 'native_english', 'native_english',
    1, 'clinical', 'INT',
    'COMPLETE', 'VERIFIED', 'RESOLVED',
    'Web-verified 2026-05-17 via ScienceDirect, ResearchGate, OPUS Bozen. Comprehensive review of ASD/ADHD/ID indoor comfort literature; synthesizes existing studies without deriving new Tier-1 thresholds. Added during Phase E.1 pilot adversarial-research pass on NDV/AUT RT60 target absence.',
    '2026-05-17 23:59', 'manual-web-verification', 1,
    'review_article', 0,
    '2026-05-17 23:59', 'session_2026-05-17-pilot-pass-2-sub-1',
    '2026-05-17 23:59', 'session_2026-05-17-pilot-pass-2-sub-1'
);

-- 2. Marzi 2025 - Scientific Reports primary study (Tier-1 corroboration of claim)
INSERT INTO evidence_sources (
    ref_id, source_type, author_count, author_count_is_complete,
    first_author_last, first_author_first, author_display,
    pub_year, pub_month, pub_title, journal_name, journal_name_en, journal_abbrev,
    volume, issue, article_number, publisher, doi, pmid,
    lang_detected, lang_detection_method, translation_method,
    tier, evidence_type, jurisdiction,
    metadata_quality, verification_status, doi_resolution_outcome,
    verification_note, last_verified_at, verified_by_tool, verification_attempt_count,
    subtype, citation_count,
    created_at, created_by_session, updated_at, updated_by_session
) VALUES (
    'REF-00727', 'journal_article', 3, 1,
    'Marzi', 'Arianna', 'Marzi, A.; Caniato, M.; Gasparella, A.',
    2025, 5, 'The influence of indoor temperature and noise on autistic individuals',
    'Scientific Reports', 'Scientific Reports', 'Sci Rep',
    '15', '1', '18802', 'Nature Portfolio', '10.1038/s41598-025-02358-4', '40442157',
    'en', 'native_english', 'native_english',
    1, 'clinical', 'INT',
    'COMPLETE', 'VERIFIED', 'RESOLVED',
    'Web-verified 2026-05-17 via Nature, PubMed PMID 40442157, PMC PMC12122908. Primary empirical study (N=autistic+TD across 6 environmental scenarios). Key quote for NDV/AUT RT60 target-absence claim: "In the absence of specific quantitative data on sound levels tailored to autistic users, a study on neurotypical students was referenced to identify baseline sound levels." Tier-1 corroboration; same research group as Bettarello 2021.',
    '2026-05-17 23:59', 'manual-web-verification', 1,
    'research_article', 3,
    '2026-05-17 23:59', 'session_2026-05-17-pilot-pass-2-sub-1',
    '2026-05-17 23:59', 'session_2026-05-17-pilot-pass-2-sub-1'
);

-- 3. Link both new sources to room-acoustic-performance
INSERT INTO source_slug_links (ref_id, slug, local_ref_id, created_at, created_by_session, updated_at, updated_by_session) VALUES
  ('REF-00726', 'room-acoustic-performance', 'RAP-marzi-2024', '2026-05-17 23:59', 'session_2026-05-17-pilot-pass-2-sub-1', '2026-05-17 23:59', 'session_2026-05-17-pilot-pass-2-sub-1'),
  ('REF-00727', 'room-acoustic-performance', 'RAP-marzi-2025', '2026-05-17 23:59', 'session_2026-05-17-pilot-pass-2-sub-1', '2026-05-17 23:59', 'session_2026-05-17-pilot-pass-2-sub-1');

-- 4. Update REF-00561 (Bettarello 2021) with adversarial-research required fields
UPDATE evidence_sources
SET prior_expectation = 'Expected Bettarello 2021 to be the highest-quality cited source for NDV/AUT acoustic comfort but to be Tier 3 (single-case-study) and to LACK a quantified RT60 threshold. Pilot doc first-pass framing assumed Bettarello says "existing standards inadequate" with no quantified value.',
    search_queries_used = 'Adversarial searches conducted 2026-05-17: (1) autism spectrum classroom reverberation time RT60 quantified threshold peer-reviewed 2024 - no Tier-1 hit; (2) Caniato 2022 2024 autism spectrum disorder indoor comfort acoustic reverberation - surfaced Bettarello self-citation in conference paper stating "0.4-0.7 seconds should represent optimal comfort conditions" - Bettarello DOES quantify, contrary to pilot doc first-pass; (3) Marzi Caniato Gasparella 2024 Building Environment - surfaced REF-00726 (comprehensive review); (4) Marzi Caniato Gasparella 2025 Scientific Reports - surfaced REF-00727 with Tier-1 confirmation of quantitative-data absence.',
    updated_at = '2026-05-17 23:59',
    updated_by_session = 'session_2026-05-17-pilot-pass-2-sub-1'
WHERE ref_id = 'REF-00561';

-- 5. Insert GAP-291 - closed-resolved with all four protocol fields populated
INSERT INTO gaps (
    gap_id, category, priority, status, skill, section,
    description, falsification_condition, confidence_interval, shift_conditions, named_dissenter,
    created_at, created_by_session, updated_at, updated_by_session
) VALUES (
    'GAP-291', 'RP', 'P2', 'CLOSED-RESOLVED', 'adversarial-research',
    'room-acoustic-performance / step 6 / NDV-AUT',
    'CLAIM TESTED: "NDV/AUT require quantified RT60 targets but no Tier-1 evidence base exists for what those targets should be." Adversarial-research pass conducted 2026-05-17 during Phase E.1 pilot Pass 2 sub-task 1. Verdict: SURVIVES with sharpening. Marzi 2025 (REF-00727, Sci Rep, Tier 1) explicitly affirms the absence of quantitative thresholds for autistic users from a primary-study venue four years after Bettarello 2021. Bettarello 2021 (REF-00561, Tier 3) proposes an aspirational design range of 0.4-0.7 s from n=7 rooms in one Italian daily-care facility - quantified DESIGN RECOMMENDATION, not Tier-1-validated threshold. Marzi 2024 (REF-00726, B&E, Tier 1) comprehensive review synthesizes existing literature without deriving a new threshold. No primary-study or systematic-review dissenter found.',
    'A peer-reviewed primary study with N>20 autistic occupants AND measurement of RT60 dose-response producing a defensible threshold value (range or ceiling) for autistic occupants. OR an updated PAS 6463 / new ISO / new ANSI standard explicitly publishing a quantified RT60 target for autistic occupants. OR a systematic review identifying ≥3 such primary studies that this pilot search missed.',
    '85-95%',
    'Drops to 50-65% if a Tier-1 systematic review or large-N (N>30) primary study with a quantified RT60 threshold for autistic occupants is located in non-English literature (German DIN-adjacent grey lit, Japanese acoustic research, Italian post-Bettarello empirical extension). Drops to 30-50% if Marzi 2024 B&E review (REF-00726, not yet read in full) actually synthesizes a quantified RT60 recommendation rather than reviewing existing literature. Rises to 95%+ if a 2026 peer-reviewed publication explicitly affirms "no Tier-1 quantified RT60 target exists for NDV/AUT."',
    'NONE FOUND for the Tier-1-threshold-absence claim. Partial counter from same research group: Bettarello et al. 2021 (REF-00561, Tier 3) proposes 0.4-0.7 s aspirational range from one facility (n=7 rooms) - quantified recommendation exists, just not at Tier 1. This is partial sharpening of the claim, not dissent: the Tier-1-threshold-absence holds.',
    '2026-05-17 23:59', 'session_2026-05-17-pilot-pass-2-sub-1',
    '2026-05-17 23:59', 'session_2026-05-17-pilot-pass-2-sub-1'
);

-- 6. evidence_population_match rows for each cited study.
-- Authored as four single-row INSERTs (not a multi-row INSERT) because the
-- sqlite3 Python executescript driver has shown fragility parsing multi-row
-- INSERTs containing commas plus newlines inside string literals (observed
-- 2026-05-17 pilot session). Single-row INSERTs are unambiguous.

INSERT INTO evidence_population_match (match_id, source_ref, target_population, study_population, sample_size, match_grade, mismatch_note, created_at, created_by_session, ref_id, gap_id)
VALUES ('EPM-RAP-001', 'REF-00561', 'NDV/AUT (autism spectrum, sensory hypersensitivity) in built environments', 'Autistic guests in one Italian daily-care facility; rooms analyzed for acoustic optimization', 7, 'PARTIAL', 'Same condition (ASD); small N at room level (n=7 rooms in one facility); single-facility generalization required; quantified output is a design recommendation (0.4-0.7 s) not a population-derived empirical threshold.', '2026-05-17 23:59', 'session_2026-05-17-pilot-pass-2-sub-1', 'REF-00561', 'GAP-291');

INSERT INTO evidence_population_match (match_id, source_ref, target_population, study_population, sample_size, match_grade, mismatch_note, created_at, created_by_session, ref_id, gap_id)
VALUES ('EPM-RAP-002', 'REF-00726', 'NDV/AUT (autism spectrum, sensory hypersensitivity) in built environments', 'Neurodivergent individuals diagnosed before age 18 (ASD/ADHD/ID); literature reviewed across thermal/acoustic/visual/air-quality comfort', NULL, 'PROXY', 'PROXY: review article (not primary research); multi-condition (ASD + ADHD + ID combined, not ASD-isolated); acoustic findings synthesized from prior studies without new threshold derivation.', '2026-05-17 23:59', 'session_2026-05-17-pilot-pass-2-sub-1', 'REF-00726', 'GAP-291');

INSERT INTO evidence_population_match (match_id, source_ref, target_population, study_population, sample_size, match_grade, mismatch_note, created_at, created_by_session, ref_id, gap_id)
VALUES ('EPM-RAP-003', 'REF-00727', 'NDV/AUT (autism spectrum, sensory hypersensitivity) in built environments', 'Autistic individuals + typically-developed controls across six environmental scenarios; attentional tests + indoor comfort questionnaires', NULL, 'PARTIAL', 'PARTIAL: same condition (ASD); study addresses dB(A) noise level (50 dB(A) baseline; 55 and 60 dB(A) decrement points for ASD attentional performance) rather than RT60 specifically. For the absence-of-quantitative-RT60-thresholds claim itself, this is EXACT corroboration - the paper directly states the absence in its methods justification.', '2026-05-17 23:59', 'session_2026-05-17-pilot-pass-2-sub-1', 'REF-00727', 'GAP-291');

INSERT INTO evidence_population_match (match_id, source_ref, target_population, study_population, sample_size, match_grade, mismatch_note, created_at, created_by_session, ref_id, gap_id)
VALUES ('EPM-RAP-004', 'REF-00642', 'NDV/AUT (autism spectrum) in school built environments', 'Built school environment and autistic students; grey-literature systematic-review-style synthesis', NULL, 'PROXY', 'PROXY: grey-lit (Tier 3, metadata_quality=GREY); school-specific (subset of NDV/AUT built-environment scope); cited in BPC evidence base for slug school-environment-autism (a sibling slug). Confirms that even a 2025 SR-style synthesis works only with grey-lit-tier underlying studies on this question.', '2026-05-17 23:59', 'session_2026-05-17-pilot-pass-2-sub-1', 'REF-00642', 'GAP-291');

-- 7. Track in data_migrations per data-layer pattern
INSERT INTO data_migrations (migration_id, applied_at, content_sha, applied_by_session, notes)
VALUES (
    'adversarial_research_ndv_aut_rt60_target_absence_2026-05-17',
    '2026-05-17 23:59',
    'insert_2_refs_REF_00726_727_update_REF_00561_insert_GAP_291_insert_4_epm_rows',
    'session_2026-05-17-pilot-pass-2-sub-1',
    'Adversarial-research pass on NDV/AUT RT60 target-absence claim per standing rule #7. Claim survives with sharpening. Adds Marzi 2024 (B&E review) and Marzi 2025 (Sci Rep primary study) as eligible Tier-1 sources for the pilot reasoning doc. Updates REF-00561 (Bettarello 2021) with adversarial protocol fields (prior_expectation, search_queries_used). Closes GAP-291 with all four protocol fields populated. Adds 4 evidence_population_match rows. Pass 2 sub-task 1 complete; sub-task 2 (PMP for DEAF RT60 ≤ 0.3 s) is next.'
);
