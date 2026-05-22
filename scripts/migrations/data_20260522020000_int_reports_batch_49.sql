-- data_20260522020000_int_reports_batch_49.sql
-- INT reports batch 49: 2 rows verified.
--
-- REF-00188: UN-Habitat 2014 — Accessibility of Housing Handbook
-- REF-00311: OECD 2020 — Affordable Housing Database overview

BEGIN TRANSACTION;

-- REF-00188: UN-Habitat Housing Accessibility Handbook
UPDATE evidence_sources SET
    pub_title = 'Accessibility of Housing: A Handbook of Inclusive Affordable Housing Solutions for Persons with Disabilities and Older Persons',
    pub_year = 2014,
    first_author_last = 'UN-Habitat',
    is_corporate_primary = 1,
    author_display = 'United Nations Human Settlements Programme (UN-Habitat) — Housing Unit + Global Network for Sustainable Housing (GNSH)',
    publisher = 'United Nations Human Settlements Programme (UN-Habitat), Nairobi',
    standard_number = 'UN-Habitat Housing Accessibility Handbook (2014 first edition; widely re-disseminated 2015-2016, including Issuu publication January 2016); Global Network for Sustainable Housing (GNSH) publication; cited by OHCHR special procedures on right to adequate housing as 2014; Sustainable Development Goals Target 11.1 (access for all to adequate, safe, affordable housing and basic services + slum upgrading by 2030); UN-Habitat 2014 slum estimate 881 million.',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'YEAR-CORRECTED-2016-TO-2014',
    metadata_integrity_detail = 'int-batch-49 2026-05-22T02:00:00Z: web-search verified via unhabitat.org official catalog + Issuu UN-Habitat channel + OHCHR (cites 2014) + CUDA Australia (Universal Design Australia) + Habitat III Policy Paper 10. Original publication year 2014 confirmed by OHCHR Special Rapporteur resources page. Author corporate (UN-Habitat) — Housing Unit administers GNSH globally. Bridges accessibility gap with slum upgrading + reconstruction + large-scale affordable + social housing programmes.',
    url = 'https://unhabitat.org/sites/default/files/download-manager-files/Accessibility%20of%20Housing%20_%20web.pdf',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+unhabitat-official+ohchr',
    last_verified_at = '2026-05-22T02:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T02:00:00Z int-batch-49] web-search verified + year corrected',
    updated_at = '2026-05-22T02:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00188';

-- REF-00311: OECD Affordable Housing Database overview 2020
UPDATE evidence_sources SET
    pub_title = 'OECD Affordable Housing Database — Overview of Social and Affordable Housing indicators',
    pub_year = 2020,
    first_author_last = 'OECD',
    is_corporate_primary = 1,
    author_display = 'OECD Directorate of Employment, Labour and Social Affairs — Social Policy Division',
    publisher = 'Organisation for Economic Co-operation and Development (OECD), Paris',
    standard_number = 'OECD Affordable Housing Database (AHD) — oe.cd/ahd; underlying data source: OECD Questionnaire on Affordable and Social Housing (QuASH), rounds 2016, 2019, 2021, 2023; covers PH1-PH7 indicators: housing market conditions (HC1-HC2), housing allowances (PH3), social rental (PH4), affordable housing programmes (PH5), rental regulation (PH6), financing improvements + regeneration (PH7). 2020 snapshot referenced in Society at a Glance 2024 (10th biennial edition).',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'int-batch-49 2026-05-22T02:00:00Z: web-search verified via oecd.org (official affordable-housing portal) + webfs.oecd.org file directory + Society at a Glance 2024 reference. ~28 million social-rental dwellings across OECD + EU countries (6-7% of housing stock average). Social housing >15% of housing stock in NL, AT, DK, UK per 2023 QuASH (PH4.2).',
    url = 'https://www.oecd.org/en/data/datasets/oecd-affordable-housing-database.html',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+oecd-official',
    last_verified_at = '2026-05-22T02:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T02:00:00Z int-batch-49] web-search verified',
    updated_at = '2026-05-22T02:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00311';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
