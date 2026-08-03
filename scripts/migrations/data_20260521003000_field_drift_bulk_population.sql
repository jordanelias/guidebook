-- data_20260521003000_field_drift_bulk_population.sql
--
-- Bulk-populates empty fields on 144 FIELD-DRIFT and FIELD-DRIFT-WITH-MISMATCH
-- rows from the full-DB verification audit. Per rule 1B: only writes fields where
-- stored value is NULL/empty; never overwrites existing values.
--
-- Also handles 3 single-case corrections discovered during FDM triage:
--   REF-00090: CLEAR-PMID (PMID resolves to virology paper, not the trauma-informed-design
--              paper the stored note describes; likely duplicate-of-REF-00527)
--   REF-00131: OWNER-QUEUE (DOI resolves to AUT posted-content 2025 work-counselling
--              scoping review; stored is Holohan 2022 design scoping review — different topic)
--   REF-00485: CLEAR-DOI (DOI resolves to Dillman-Hasso 2020; stored is Kaplan 1989
--              'Experience of Nature' book predating DOI registration)
--
-- Source: scripts/audit/full_db_metadata_verification.py output /tmp/full_audit.json
BEGIN TRANSACTION;

-- Bulk FIELD-DRIFT: 144 rows

-- REF-00006 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'PLOS ONE'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00006';

-- REF-00007 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'American Journal of Alzheimer''s Disease &amp; Other Dementias®'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00007';

-- REF-00008 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Neuropsychological Rehabilitation'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00008';

-- REF-00010 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Topics in Stroke Rehabilitation'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00010';

-- REF-00011 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Disability and Rehabilitation'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00011';

-- REF-00013 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Neuroscience &amp; Biobehavioral Reviews'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00013';

-- REF-00014 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Neuropsychologia'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00014';

-- REF-00025 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Archives of Physical Medicine and Rehabilitation'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00025';

-- REF-00026 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'HERD: Health Environments Research &amp; Design Journal'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00026';

-- REF-00034 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'HERD: Health Environments Research &amp; Design Journal'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00034';

-- REF-00035 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Disability and Rehabilitation: Assistive Technology'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00035';

-- REF-00036 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Frontiers in Public Health'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00036';

-- REF-00037 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'PLOS ONE'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00037';

-- REF-00038 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Physical &amp; Occupational Therapy In Geriatrics'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00038';

-- REF-00041 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Canadian Journal of Disability Studies'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00041';

-- REF-00048 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Autism'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00048';

-- REF-00059 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Assistive technology : the official journal of RESNA'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00059';

-- REF-00068 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'The Lancet'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00068';

-- REF-00070 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'American Journal of Physical Medicine &amp; Rehabilitation'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00070';

-- REF-00083 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Designing Environments for People with Dementia'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00083';

-- REF-00089 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of Clinical Nursing'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00089';

-- REF-00091 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of Child &amp; Adolescent Trauma'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00091';

-- REF-00095 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'BMJ Open'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00095';

-- REF-00100 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of psychiatric research'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00100';

-- REF-00101 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'BMC Health Services Research'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00101';

-- REF-00103 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'BMC Health Services Research'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00103';

-- REF-00105 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'International journal of mental health nursing'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00105';

-- REF-00107 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Sante mentale au Quebec'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00107';

-- REF-00108 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'International Journal of Mental Health Nursing'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00108';

-- REF-00109 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'HERD: Health Environments Research &amp; Design Journal'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00109';

-- REF-00126 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'The psychology of adult development and aging.'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00126';

-- REF-00134 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Disability and Health Journal'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00134';

-- REF-00136 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Building and Environment'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00136';

-- REF-00151 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'The Lancet'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00151';

-- REF-00171 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Building and Environment'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00171';

-- REF-00172 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Science'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00172';

-- REF-00174 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of Motor Behavior'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00174';

-- REF-00178 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Occupational Therapy In Health Care'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00178';

-- REF-00202 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'HERD: Health Environments Research &amp; Design Journal'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00202';

-- REF-00204 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Studies in Health Technology and Informatics'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00204';

-- REF-00214 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'British Journal of Sports Medicine'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00214';

-- REF-00216 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'BMC Neurology'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00216';

-- REF-00220 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Current Rheumatology Reports'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00220';

-- REF-00222 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Indoor Air'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00222';

-- REF-00227 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'The Journal of Pain'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00227';

-- REF-00228 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Temperature'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00228';

-- REF-00229 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Current Pain and Headache Reports'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00229';

-- REF-00242 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Occupational Therapy International'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00242';

-- REF-00255 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of Building Engineering'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00255';

-- REF-00272 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of Real Estate Research'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00272';

-- REF-00278 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of Tourism Futures'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00278';

-- REF-00283 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Innovation in Aging'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00283';

-- REF-00325 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'American Journal of Audiology'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00325';

-- REF-00327 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of Speech and Hearing Research'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00327';

-- REF-00331 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'The Journal of the Acoustical Society of America'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00331';

-- REF-00340 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Disability and Rehabilitation'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00340';

-- REF-00341 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Acta Structilia'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00341';

-- REF-00356 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'The American Journal of Occupational Therapy'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00356';

-- REF-00362 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Disability and Health Journal'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00362';

-- REF-00367 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'JMIR rehabilitation and assistive technologies'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00367';

-- REF-00368 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Canadian Journal of Occupational Therapy'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00368';

-- REF-00371 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of medical Internet research'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00371';

-- REF-00373 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Lancet (London, England)'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00373';

-- REF-00374 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Health &amp; Social Care in the Community'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00374';

-- REF-00379 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'An Occupational Therapist’s Guide to Home Modification Practice'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00379';

-- REF-00389 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of Orthopaedic Research'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00389';

-- REF-00397 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'The Journal of Spinal Cord Medicine'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00397';

-- REF-00400 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'BioMed Research International'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00400';

-- REF-00407 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of aging research'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00407';

-- REF-00426 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'British Journal of Occupational Therapy'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00426';

-- REF-00427 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Hong Kong Journal of Occupational Therapy'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00427';

-- REF-00454 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of aging research'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00454';

-- REF-00479 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Environment and Behavior'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00479';

-- REF-00480 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Cognitive Science'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00480';

-- REF-00481 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Cognitive Processing'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00481';

-- REF-00486 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'American Journal of Alzheimer''s Disease &amp; Other Dementias®'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00486';

-- REF-00487 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'HERD: Health Environments Research &amp; Design Journal'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00487';

-- REF-00488 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Frontiers in Dementia'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00488';

-- REF-00489 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'HERD: Health Environments Research &amp; Design Journal'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00489';

-- REF-00500 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Design for People Living with Dementia'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00500';

-- REF-00503 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Sage Open Aging'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00503';

-- REF-00522 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'HERD: Health Environments Research &amp; Design Journal'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00522';

-- REF-00524 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'HERD: Health Environments Research &amp; Design Journal'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00524';

-- REF-00526 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of Gerontological Nursing'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00526';

-- REF-00530 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Work'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00530';

-- REF-00539 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Epilepsia'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00539';

-- REF-00541 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Autism'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00541';

-- REF-00551 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'PLOS Biology'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00551';

-- REF-00554 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Trends in Neurosciences'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00554';

-- REF-00556 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Lighting Research &amp; Technology'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00556';

-- REF-00557 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Lighting Research &amp; Technology'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00557';

-- REF-00558 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of the American Medical Directors Association'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00558';

-- REF-00570 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Language, Speech, and Hearing Services in Schools'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00570';

-- REF-00576 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Ear &amp; Hearing'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00576';

-- REF-00577 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Ear &amp; Hearing'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00577';

-- REF-00578 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'American Journal of Audiology'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00578';

-- REF-00579 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Language, Speech, and Hearing Services in Schools'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00579';

-- REF-00580 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of the American Academy of Audiology'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00580';

-- REF-00581 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Ear &amp; Hearing'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00581';

-- REF-00582 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'American Journal of Audiology'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00582';

-- REF-00583 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Ear &amp; Hearing'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00583';

-- REF-00584 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Ear &amp; Hearing'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00584';

-- REF-00585 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Noise & health'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00585';

-- REF-00586 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Ear &amp; Hearing'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00586';

-- REF-00587 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of the American Academy of Audiology'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00587';

-- REF-00588 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'American Journal of Audiology'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00588';

-- REF-00589 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Autism'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00589';

-- REF-00590 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Infants &amp; Young Children'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00590';

-- REF-00593 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Canadian Journal of Occupational Therapy'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00593';

-- REF-00601 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Language, Speech, and Hearing Services in Schools'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00601';

-- REF-00614 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Diagnosis'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00614';

-- REF-00619 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of Occupational &amp; Environmental Medicine'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00619';

-- REF-00621 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Preventive Medicine Reports'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00621';

-- REF-00622 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Air Quality, Atmosphere &amp; Health'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00622';

-- REF-00623 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'International Journal of Hygiene and Environmental Health'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00623';

-- REF-00624 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Frontiers in Public Health'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00624';

-- REF-00642 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'International Journal of Inclusive Education'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00642';

-- REF-00700 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Médecine'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00700';

-- REF-00701 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Frontiers in Psychiatry'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00701';

-- REF-00703 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Research in Developmental Disabilities'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00703';

-- REF-00704 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of Intellectual &amp; Developmental Disability'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00704';

-- REF-00711 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'European Psychiatry'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00711';

-- REF-00713 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Alexandria Engineering Journal'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00713';

-- REF-00714 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Open House International'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00714';

-- REF-00715 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'OTJR: Occupational Therapy Journal of Research'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00715';

-- REF-00716 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Support for Learning'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00716';

-- REF-00717 (FIELD-DRIFT-WITH-MISMATCH): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'British Journal of Special Education'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00717';

-- REF-00718 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Support for Learning'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00718';

-- REF-00719 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Research in Developmental Disabilities'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00719';

-- REF-00720 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Health &amp; Place'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00720';

-- REF-00721 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of Housing and the Built Environment'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00721';

-- REF-00722 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'The American Journal of Occupational Therapy'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00722';

-- REF-VERIFIED-002 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'The Journal of Rehabilitation Research and Development'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-VERIFIED-002';

-- REF-VERIFIED-003 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'PLOS ONE'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-VERIFIED-003';

-- REF-VERIFIED-004 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Disability and Rehabilitation'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-VERIFIED-004';

-- REF-VERIFIED-009 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of Speech and Hearing Research'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-VERIFIED-009';

-- REF-VERIFIED-010 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Multiple Sclerosis and Related Disorders'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-VERIFIED-010';

-- REF-VERIFIED-011 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Nature Reviews Neurology'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-VERIFIED-011';

-- REF-VERIFIED-012 (FIELD-DRIFT): 1 field(s)
UPDATE evidence_sources SET
  journal_name = COALESCE(journal_name, 'Journal of Applied Physiology'),
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | bulk-field-drift-population 2026-05-21T00:30:00Z: filled empty fields from canonical (journal_name)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-VERIFIED-012';

-- Bulk population: 139 rows updated, 5 skipped (no fields to fill)

-- REF-00090: CLEAR-PMID (wrong PMID 36742289 -> Girsch virology; stored topic note 'TID PMC9658651' references REF-00527's paper)
UPDATE evidence_sources SET
  pmid = NULL,
  metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00527',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | full-DB-audit 2026-05-21T00:30:00Z: PMID 36742289 cleared (resolves to Girsch 2022 virology paper, not trauma-informed-design). Stored title note references PMC9658651 which is Owen-Crane 2022 trauma-informed-design - same paper as REF-00527. Owner: decide whether to merge.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T00:30:00Z full-DB-audit] CLEAR-PMID + flag potential duplicate of REF-00527',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00090';

-- REF-00131: OWNER-QUEUE (DOI -> AUT 2025 posted-content work-counselling scoping review; stored Holohan 2022 design scoping review)
UPDATE evidence_sources SET
  metadata_integrity_status = 'IDENTIFIER-CONTENT-DISAGREE-OWNER-DECIDE',
  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || ' | full-DB-audit 2026-05-21T00:30:00Z: DOI 10.24135/10292/18859 resolves to AUT Library 2025 posted-content scoping-review protocol on trauma-informed work-oriented counselling (no author listed in Crossref); stored is Holohan 2022 trauma-informed design scoping review. Different topic. Owner: confirm DOI/paper intent, may need replacement DOI.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T00:30:00Z full-DB-audit] OWNER-DECIDE: identifier vs stored topic disagree',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00131';

-- REF-00485: CLEAR-DOI (Kaplan & Kaplan 1989 'Experience of Nature' Cambridge UP - book predates DOI registration; attached DOI is wrong)
UPDATE evidence_sources SET
  doi = NULL,
  verification_status = NULL,
  doi_resolution_outcome = NULL,
  metadata_integrity_status = 'WRONG-DOI-CLEARED',
  metadata_integrity_detail = 'full-DB-audit 2026-05-21T00:30:00Z: DOI 10.31234/osf.io/w36rg CLEARED - resolves to Dillman-Hasso 2020 (PsyArXiv posted-content), not Kaplan 1989. Stored is Kaplan & Kaplan 1989 The Experience of Nature (Cambridge University Press) - real book predating DOI registration. verification_status reverted from VERIFIED.',
  verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T00:30:00Z full-DB-audit] CLEAR-DOI (wrong-attribution)',
  updated_at = '2026-05-21T00:30:00Z',
  updated_by_session = 'session_2026-05-20-ato-rehab',
  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00485';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
