-- data_20260520210000_ato_pmid_rehab_batch_2.sql
--
-- AUTHOR-TITLE-ONLY × VERIFIED × has-PMID rehabilitation, batch 2 of N for
-- the academic cohort. Cohort: 9 rows (7 ATO×VERIFIED×has-PMID + 2 batch-1
-- DOI-TRUNCATED rescue candidates with PMID).
--
-- Verdicts:
--   2 → COMPLETE (1 clean MATCH + 1 DOI-RESCUE replacing truncated DOI
--                  with canonical full DOI from PubMed articleids)
--   4 → MISMATCH-TITLE (journal-name-as-title pattern subset)
--   3 → MISMATCH-MULTI (wrong-PMID misattribution; 2 already MISMATCH-MULTI
--                       from batch 1's Crossref probe — both APIs flag)
--
-- Yield: 22% upgrade rate (vs batch 1's 58%) reveals that the note-as-title
-- pattern is more concentrated in PMID rows than DOI rows in this corpus.
--
-- Schema dependency: migration 014 (metadata_integrity_status, metadata_integrity_detail).
-- Tracking: runner inserts data_migrations row per filename stem.
--
BEGIN TRANSACTION;

-- REF-00027: ATO->COMPLETE-PUBMED-MATCH-DOI-RESCUE
UPDATE evidence_sources SET
  journal_name='Assistive technology : the official journal of RESNA',
  issn='1040-0435',
  author_count_is_complete=1,
  doi='10.1080/10400435.2014.976799',
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='pubmed-resolved 2026-05-20T21:00:00Z; canonical-DOI=10.1080/10400435.2014.976799',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-PMID-rehab] upgrade ATO->COMPLETE (DOI rescue)',
  updated_at='2026-05-20T21:00:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00027';

-- REF-00069: HOLD-PUBMED-MISMATCH → MISMATCH-MULTI (prior: MISMATCH-MULTI)
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-MULTI',
  metadata_integrity_detail='title:cr=''Design features that reduce the use of seclusion and restrai'' vs db=''MHIPI study. Lancet Public Health 6:e631–e640 '' ; author:cr=''Oostermeijer'' vs db=''Keall'' || pubmed-mismatch 2026-05-20T21:00:00Z: title:pm=''Design features that reduce the use of seclusion and restrai'' vs db=''MHIPI study. Lancet Public Health 6:e631–e640'' ; author:pm=''Oostermeijer'' vs db=''Keall''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-PMID-rehab] MISMATCH-MULTI',
  updated_at='2026-05-20T21:00:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00069';

-- REF-00096: HOLD-PUBMED-MISMATCH → MISMATCH-MULTI (prior: MISMATCH-MULTI)
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-MULTI',
  metadata_integrity_detail='author:cr=''van Oel'' vs db=''Faerden'' ; year:cr=2020 vs db=2022 || pubmed-mismatch 2026-05-20T21:00:00Z: title:pm=''Environmental Transformations Enhancing Dignity in an Acute '' vs db=''Single rooms and patient control in inpatient mental health.''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-PMID-rehab] MISMATCH-MULTI',
  updated_at='2026-05-20T21:00:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00096';

-- REF-00100: HOLD-PUBMED-MISMATCH → MISMATCH-TITLE (prior: None)
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-TITLE',
  metadata_integrity_detail='pubmed-mismatch 2026-05-20T21:00:00Z: title:pm=''Hospital design for inpatient psychiatry: A realistic umbrel'' vs db=''J Psychiatric Research''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-PMID-rehab] MISMATCH-TITLE',
  updated_at='2026-05-20T21:00:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00100';

-- REF-00101: HOLD-PUBMED-MISMATCH → MISMATCH-TITLE (prior: MISMATCH-TITLE)
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-TITLE',
  metadata_integrity_detail='title:cr=''Open Doors by Fair Means: a quasi-experimental controlled st'' vs db=''BMC Health Services Research — psychiatric architecture '' || pubmed-mismatch 2026-05-20T21:00:00Z: title:pm=''Open Doors by Fair Means: a quasi-experimental controlled st'' vs db=''BMC Health Services Research — psychiatric architecture''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-PMID-rehab] MISMATCH-TITLE',
  updated_at='2026-05-20T21:00:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00101';

-- REF-00103: HOLD-PUBMED-MISMATCH → MISMATCH-TITLE (prior: MISMATCH-TITLE)
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-TITLE',
  metadata_integrity_detail='title:cr=''A cross-sectional prospective study of seclusion, restraint '' vs db=''BMC Health Services Research — Norwegian acute psychiatry '' || pubmed-mismatch 2026-05-20T21:00:00Z: title:pm=''A cross-sectional prospective study of seclusion, restraint '' vs db=''BMC Health Services Research — Norwegian acute psychiatry''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-PMID-rehab] MISMATCH-TITLE',
  updated_at='2026-05-20T21:00:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00103';

-- REF-00105: HOLD-PUBMED-MISMATCH → MISMATCH-TITLE (prior: None)
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-TITLE',
  metadata_integrity_detail='pubmed-mismatch 2026-05-20T21:00:00Z: title:pm=''Protocols to reduce seclusion in inpatient mental health uni'' vs db=''Int J Mental Health Nurs''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-PMID-rehab] MISMATCH-TITLE',
  updated_at='2026-05-20T21:00:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00105';

-- REF-00527: HOLD-PUBMED-MISMATCH → MISMATCH-MULTI (prior: DOI-TRUNCATED)
UPDATE evidence_sources SET
  metadata_integrity_status='MISMATCH-MULTI',
  metadata_integrity_detail='stored DOI ''10.35248/2165-7556-22'' lacks article identifier suffix || pubmed-mismatch 2026-05-20T21:00:00Z: title:pm=''Trauma-Informed Design of Supported Housing: A Scoping Revie'' vs db=''Stairway Visual Contrast Enhancement to Reduce Fall-Related '' ; author:pm=''Owen'' vs db=''Harper''',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-PMID-rehab] MISMATCH-MULTI',
  updated_at='2026-05-20T21:00:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00527';

-- REF-00538: ATO->COMPLETE-PUBMED-MATCH
UPDATE evidence_sources SET
  journal_name='Seizure',
  journal_abbrev='Seizure',
  volume='50',
  pages_start='209',
  pages_end='218',
  issn='1059-1311',
  doi='10.1016/j.seizure.2017.04.001',
  metadata_quality='COMPLETE',
  metadata_integrity_status='OK',
  metadata_integrity_detail='pubmed-resolved 2026-05-20T21:00:00Z; canonical-DOI=10.1016/j.seizure.2017.04.001',
  verification_note=COALESCE(verification_note,'') || ' | [PROBE 2026-05-20 ATO-PMID-rehab] upgrade ATO->COMPLETE',
  updated_at='2026-05-20T21:00:00Z',
  updated_by_session='session_2026-05-20-ato-rehab',
  verification_attempt_count=COALESCE(verification_attempt_count,0)+1
WHERE ref_id='REF-00538';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;

-- Summary: 2 upgrades, 7 mismatches.
