-- data_20260520213000_statutory_rehab_batch_3.sql
--
-- AUTHOR-TITLE-ONLY × source_type='standard' × NULL — statutory cohort, batch 3.
-- Cohort: 7 rows (KR/SG/UK/UK/ES/DK/KR). All seven had jurisdiction + standard_number
-- + tier + evidence_type already populated; missing publisher (issuing body) and
-- pub_year (edition year), the two remaining COMPLETE-STATUTORY requirements
-- per DR-2026-05-18.
--
-- Protocol: per-row web research on issuing body + edition year, with cross-check
-- between stored title and standard_number's documented content. Same cross-check
-- discipline as batches 1 and 2 — auto-upgrade only where evidence is coherent.
--
-- Outcomes:
--   3 upgrades to COMPLETE-STATUTORY:
--     REF-00020 (KR 편의증진법 enforcement decree) × UNVERIFIED-1 (non-EN primary text)
--     REF-00403 (UK HTM 08-01 Acoustics) × VERIFIED (open-access PDF, title matches)
--     REF-00464 (ES DB SUA) × VERIFIED (open-access PDF, title matches)
--   1 paywall routing (REF-00469 DK SBi 230) — SBi/AAU commercial; cannot confirm
--     edition year without purchase; verification_status=IS-PAYWALL, metadata_quality
--     stays AUTHOR-TITLE-ONLY until edition year recovered
--   3 integrity holds:
--     REF-00164 (SG EASE 2.0) → MISMATCH-MULTI: programme name, not standards doc
--     REF-00193 (UK HBN 00-03) → MISMATCH-TITLE: DB title 'bariatric guidance'
--                                disagrees with HBN 00-03's actual content
--                                ('Clinical and clinical support spaces', 2013)
--     REF-00511 (KR 편의증진법 — 점자블록) → MISMATCH-MULTI: standard_number is
--                                note-style, not a stable provision identifier
--
-- Methodology finding extending batches 1-2: the note-as-title pattern appears
-- in statutory metadata too. REF-00164's standard_number is a programme name;
-- REF-00193's pub_title is wrong-content for a known statutory number; REF-00511's
-- standard_number is a topic description with no article reference. The pattern
-- is cohort-spanning, not academic-cohort-specific.
--
-- Schema dependency: migration 014 (metadata_integrity_status, metadata_integrity_detail).
-- Tracking: runner inserts data_migrations row per filename stem.

BEGIN TRANSACTION;

-- REF-00020: Korean Convenience Promotion Act, Enforcement Decree Table 1 §3 (tactile blocks)
UPDATE evidence_sources SET
  publisher = '보건복지부 (Ministry of Health and Welfare, Republic of Korea)',
  pub_year = 1997,
  pub_year_note = 'Act first enacted 1997-04-10; Enforcement Decree Table 1 last major amend 2012-05-23 per WHO MiNDbank',
  metadata_quality = 'COMPLETE-STATUTORY',
  verification_status = 'UNVERIFIED-1',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'web-research 2026-05-20T21:30:00Z; corroborated via WHO MiNDbank (extranet.who.int/mindbank/item/4087) and Korean Law Information Center (elaw.klri.re.kr); non-EN primary text → UNVERIFIED-1 per V2-manual routing',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-20 statutory-rehab-batch-3] upgrade ATO->COMPLETE-STATUTORY',
  updated_at = '2026-05-20T21:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00020';

-- REF-00164: Singapore EASE 2.0 — MISMATCH: programme, not standard
UPDATE evidence_sources SET
  metadata_integrity_status = 'MISMATCH-MULTI',
  metadata_integrity_detail = 'classification mismatch: EASE 2.0 is an HDB elderly-modification subsidy programme launched 2024, not a standards document. tier=5 national_framework is questionable. The actual statutory standard for Singapore accessibility is BCA Code on Accessibility in the Built Environment 2025 (REF-00074 in IS-PAYWALL queue). Owner: reclassify or merge with the BCA Code row.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-20 statutory-rehab-batch-3] MISMATCH-MULTI (programme-not-standard)',
  updated_at = '2026-05-20T21:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00164';

-- REF-00193: UK HBN 00-03 — title disagreement
UPDATE evidence_sources SET
  metadata_integrity_status = 'MISMATCH-TITLE',
  metadata_integrity_detail = 'standard_number HBN 00-03 documented (NHS England, 2013) as "Clinical and clinical support spaces" — NOT bariatric guidance. db pub_title "healthcare bariatric guidance" wrong-content for this standard. If bariatric guidance was the intended source, standard_number is wrong; if HBN 00-03 was the intended source, pub_title is wrong. Owner review needed.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-20 statutory-rehab-batch-3] MISMATCH-TITLE',
  updated_at = '2026-05-20T21:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00193';

-- REF-00403: UK HTM 08-01 Acoustics — CLEAN MATCH
UPDATE evidence_sources SET
  publisher = 'NHS England (formerly Department of Health, Estates and Facilities Division)',
  pub_year = 2013,
  pub_year_note = 'Published 2013-03-19; supersedes HTM 08-01 Specialist services 2008 and HTM 2045 Acoustics 1996',
  metadata_quality = 'COMPLETE-STATUTORY',
  verification_status = 'VERIFIED',
  url = 'https://www.england.nhs.uk/wp-content/uploads/2021/05/HTM_08-01.pdf',
  url_accessed = '2026-05-20',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'web-research 2026-05-20T21:30:00Z; corroborated via NHS England (england.nhs.uk/publication/health-sector-buildings-acoustic-design-requirements-htm-08-01/) and NBS Publication Index (thenbs.com); open-access PDF directly retrievable',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-20 statutory-rehab-batch-3] upgrade ATO->COMPLETE-STATUTORY × VERIFIED',
  updated_at = '2026-05-20T21:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00403';

-- REF-00464: ES DB SUA — CLEAN MATCH
UPDATE evidence_sources SET
  publisher = 'Ministerio de Transportes, Movilidad y Agenda Urbana (Spain; formerly Ministerio de Fomento)',
  pub_year = 2010,
  pub_year_note = 'DB SUA established by Real Decreto 314/2006 (CTE); current consolidated edition baselined 2010-06 with comments through 2025',
  metadata_quality = 'COMPLETE-STATUTORY',
  verification_status = 'VERIFIED',
  url = 'https://www.codigotecnico.org/pdf/Documentos/SUA/DBSUA.pdf',
  url_accessed = '2026-05-20',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'web-research 2026-05-20T21:30:00Z; primary text open-access at codigotecnico.org; title "Seguridad de utilización y accesibilidad" matches stored pub_title; corroborated via codigotecnico.org official portal and observatoriodelaaccesibilidad.es',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-20 statutory-rehab-batch-3] upgrade ATO->COMPLETE-STATUTORY × VERIFIED',
  updated_at = '2026-05-20T21:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00464';

-- REF-00469: DK SBi 230 — commercial publication, route to IS-PAYWALL queue
UPDATE evidence_sources SET
  publisher = 'Statens Byggeforskningsinstitut (SBi), Aalborg Universitet (Denmark)',
  verification_status = 'IS-PAYWALL',
  metadata_integrity_status = 'OK',
  metadata_integrity_detail = 'web-research 2026-05-20T21:30:00Z; SBi-anvisning series is published commercially by SBi/AAU (sbi.dk). Edition year not confirmable without purchase. Belongs alongside REF-00575 (SBi 218) in owner IS-PAYWALL queue. metadata_quality stays AUTHOR-TITLE-ONLY until pub_year recovered.',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-20 statutory-rehab-batch-3] IS-PAYWALL (SBi commercial, no edition year without purchase)',
  updated_at = '2026-05-20T21:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00469';

-- REF-00511: Korean Convenience Promotion Act, "점자블록 statutory provisions" — note-style standard_number
UPDATE evidence_sources SET
  metadata_integrity_status = 'MISMATCH-MULTI',
  metadata_integrity_detail = 'standard_number "편의증진법 — 점자블록 statutory provisions" is note-style: 편의증진법 (Act on Convenience Promotion) is correct Act name, but "점자블록 statutory provisions" describes a topic (braille/tactile blocks), not a specific article or provision identifier. Same Act underlies REF-00020. Owner: either merge with REF-00020 (if same specific provision) or set a stable standard_number referencing the actual article (e.g., 시행규칙 별표 article ref).',
  verification_note = COALESCE(verification_note, '') || ' | [PROBE 2026-05-20 statutory-rehab-batch-3] MISMATCH-MULTI (note-style standard_number)',
  updated_at = '2026-05-20T21:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00511';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;

-- Summary: 3 upgrades to COMPLETE-STATUTORY (REF-00020 UNVERIFIED-1; REF-00403, REF-00464 VERIFIED),
-- 1 paywall routing (REF-00469), 3 integrity holds (REF-00164, REF-00193, REF-00511).
-- Eligible pool delta: +3. Owner-review queue delta: +3 MISMATCH + 1 IS-PAYWALL = +4.
