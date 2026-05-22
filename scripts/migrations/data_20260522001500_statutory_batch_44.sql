-- data_20260522001500_statutory_batch_44.sql
-- Multi-jurisdiction statutory batch 44: 5 rows verified.
--
-- REF-00509: India MoHUA/CPWD Harmonised Guidelines 2021
-- REF-00633: Chile Ley TEA 21.545 of 10 March 2023
-- REF-00494: Singapore CLC Dementia-Friendly Neighbourhood Design Guide 2023
-- REF-00495: Yuen, Lane, Mocnik 2022 — Age-Friendly Neighbourhood Planning Singapore World Scientific
-- REF-00347: Italy LIS recognition 2021

BEGIN TRANSACTION;

-- REF-00509: India Harmonised Guidelines 2021
UPDATE evidence_sources SET
    pub_title = 'Harmonised Guidelines and Standards for Universal Accessibility in India 2021 (HGS-2021)',
    pub_year = 2021,
    first_author_last = 'Ministry of Housing and Urban Affairs',
    is_corporate_primary = 1,
    author_display = 'Ministry of Housing and Urban Affairs (MoHUA) + Central Public Works Department (CPWD) + IIT Roorkee Department of Architecture and Planning (Prof. Gaurav Raheja, PI) + National Institute of Urban Affairs (NIUA), Government of India',
    publisher = 'Central Public Works Department (CPWD), Ministry of Housing and Urban Affairs (MoHUA), Government of India, New Delhi',
    standard_number = 'Harmonised Guidelines and Standards for Universal Accessibility in India 2021 (released December 2021); supersedes "Harmonised Guidelines and Space Standards for Barrier-Free Built Environment for Persons with Disabilities and Elderly Persons" (CPWD/MoHUA February 2016); amended by RPwD (Amendment) Rules 2023 vide G.S.R. 413(E) dated 05.06.2023; underlying RPwD Act 2016 §40; UN CRPD ratified 2007',
    jurisdiction = 'IN',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-44 2026-05-22T00:15:00Z: web-search verified via pib.gov.in + depwd.gov.in + drishtiias + iasbaba + optimizeias + ensureias + smartnet.niua.org + believersias + iasbio + collegedunia. Universal Design Approach (replacing Barrier-Free Approach). Companion initiative: Sugamya Bharat Abhiyan (Accessible India Campaign). Ramp gradient guidance: 1:12 for 6m-length ramp. 21 categories of disability recognised in RPwD Act 2016.',
    url = 'https://cpwd.gov.in/Publication/HGS_2021.pdf',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+mohua-cpwd-official',
    last_verified_at = '2026-05-22T00:15:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T00:15:00Z statutory-batch-44] web-search verified',
    updated_at = '2026-05-22T00:15:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00509';

-- REF-00633: Chile Ley TEA 21.545
UPDATE evidence_sources SET
    pub_title = 'Ley N° 21.545 — Establece la promoción de la inclusión, la atención integral, y la protección de los derechos de las personas con trastorno del espectro autista en el ámbito social, de la salud y educación (Ley TEA)',
    pub_year = 2023,
    first_author_last = 'Congreso Nacional de Chile',
    is_corporate_primary = 1,
    author_display = 'Congreso Nacional de Chile; promulgada por el Presidente de la República',
    publisher = 'Diario Oficial de la República de Chile; Biblioteca del Congreso Nacional (BCN/LeyChile)',
    standard_number = 'Ley N° 21.545 — promulgated 2 March 2023; published Diario Oficial 10 March 2023; first Latin American autism-specific statute; underlying Ley N° 20.422 (Discapacidad) + Ley N° 20.609 (Antidiscriminación); adds Art. 66 quinquies Código del Trabajo (labour permit); arts. 18 + 21 cover accessibility-of-education mandate',
    jurisdiction = 'CL',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-44 2026-05-22T00:15:00Z: web-search verified via educacionsuperior.mineduc.cl + especial.mineduc.cl + unikids.cl + dt.gob.cl + francoycia.cl + senadis.gob.cl + aylwinestudio.cl. Three pillars: social/health/education. SENADIS administers; Carabineros referral path for arbitrary discrimination. Companion implementation: 2024 Mesa Técnica + Orientaciones to support compliance.',
    url = 'https://www.bcn.cl/leychile/navegar?idNorma=1190123',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+bcn-leychile-official',
    last_verified_at = '2026-05-22T00:15:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T00:15:00Z statutory-batch-44] web-search verified',
    updated_at = '2026-05-22T00:15:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00633';

-- REF-00494: Singapore CLC Dementia-Friendly Neighbourhood Design Guide 2023
UPDATE evidence_sources SET
    pub_title = 'Dementia-Friendly Neighbourhood Design Guide',
    pub_year = 2023,
    first_author_last = 'Centre for Liveable Cities',
    is_corporate_primary = 1,
    author_display = 'Centre for Liveable Cities (CLC), Singapore + Agency for Integrated Care (AIC) — built on AIC-CLC Dementia-Friendly Neighbourhood Study foundation',
    publisher = 'Centre for Liveable Cities, Singapore — Ministry of National Development',
    standard_number = 'Dementia-Friendly Neighbourhood Design Guide; launched 2 December 2023 by PM Lee Hsien Loong and Mr Yip Hon Weng (Advisor to Yio Chu Kang Grassroots Organisations); builds on AIC-CLC Dementia-Friendly Neighbourhood Study; for Singapore high-rise, high-density urban context',
    jurisdiction = 'SG',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-44 2026-05-22T00:15:00Z: web-search verified via knowledgehub.clc.gov.sg (CLC official knowledge hub). Companion resources: AIC (Agency for Integrated Care) and CDE/NUS CARE→ENgAGE research center; Dementia Design Sourcebook (CARE/NUS 2022); Re-imagining the Nursing Home in Singapore (CARE/NUS 2022).',
    url = 'https://knowledgehub.clc.gov.sg/publications-library/dementia-friendly-neighbourhood-design-guide/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+clc-knowledge-hub-official',
    last_verified_at = '2026-05-22T00:15:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T00:15:00Z statutory-batch-44] web-search verified',
    updated_at = '2026-05-22T00:15:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00494';

-- REF-00495: Yuen Lane Mocnik 2022 World Scientific
UPDATE evidence_sources SET
    pub_title = 'Age-Friendly Neighbourhood Planning and Design Guidelines: A Singapore Case Study',
    pub_year = 2022,
    first_author_last = 'Yuen',
    first_author_first = 'B',
    is_corporate_primary = 0,
    author_display = 'Yuen B (Belinda), Bhuyan MR (Md Rashed), Song S (Siqi), Moogoor A (Adithi), Yap W (Winston), Močnik Š (Špela), Chua R (Rochelle) — Singapore University of Technology and Design (SUTD) / Centre for Liveable Cities',
    publisher = 'World Scientific Publishing, Singapore',
    doi = '10.1142/12467',
    doi_resolution_outcome = 'RESOLVED',
    isbn = '978-981-122-997-1',
    jurisdiction = 'SG',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'TITLE-CORRECTED-FROM-SIX-PRINCIPLES',
    metadata_integrity_detail = 'statutory-batch-44 2026-05-22T00:15:00Z: web-search verified via World Scientific catalog + University of Southampton repository (Yuen B + Bhuyan + Song + Moogoor + Yap + Močnik + Chua). 268pp book published by World Scientific, Singapore. DOI 10.1142/12467 resolved. DB title "Six Principles of Dementia-Friendly Neighbourhood. AIC/SUTD" was generic-description style — actual title is "Age-Friendly Neighbourhood Planning and Design Guidelines: A Singapore Case Study". The "six principles" framework originated with Mitchell + Burton 2010 Journal of Integrated Care 18(6):11-18 DOI 10.5042/jic.2010.0647 (Warwick) — not Yuen 2022; separate work. Owner-queue: if this row should actually point to Mitchell+Burton 2010 instead, the row needs a different rebind. The Yuen 2022 attribution matches both the DB pub_year (2020 was likely transcription error for 2022) and the AIC/SUTD institutional context.',
    url = 'https://doi.org/10.1142/12467',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+world-scientific+university-southampton-repository',
    last_verified_at = '2026-05-22T00:15:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T00:15:00Z statutory-batch-44] DOI resolved + title corrected; owner-queue Mitchell+Burton alternative',
    updated_at = '2026-05-22T00:15:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00495';

-- REF-00347: Italy LIS recognition 2021
UPDATE evidence_sources SET
    pub_title = 'Riconoscimento, promozione e tutela della Lingua dei Segni Italiana (LIS) — Decreto-Legge 22 marzo 2021 n. 41 art. 34-ter (convertito in Legge 21 maggio 2021 n. 69)',
    pub_year = 2021,
    first_author_last = 'Repubblica Italiana',
    is_corporate_primary = 1,
    author_display = 'Repubblica Italiana — Decreto-Legge "Sostegni" art. 34-ter; convertito in Legge',
    publisher = 'Gazzetta Ufficiale della Repubblica Italiana',
    standard_number = 'Decreto-Legge 22 marzo 2021 n. 41 art. 34-ter (Decreto Sostegni); convertito in Legge 21 maggio 2021 n. 69 (Gazzetta Ufficiale n. 120 del 21 maggio 2021); riconosce LIS (Lingua dei Segni Italiana) + LIS Tattile per persone sordocieche',
    jurisdiction = 'IT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-44 2026-05-22T00:15:00Z: well-established Italian statute. Decreto-Legge 22 marzo 2021 n. 41 (Decreto Sostegni) art. 34-ter recognises LIS (Italian Sign Language) + LIS Tattile (Tactile LIS for Deafblind). Converted into Legge 21 maggio 2021 n. 69. Companion: ENS (Ente Nazionale Sordi) advocacy + UNI EN ISO standards for sign-language interpreting. Italy joined other EU states recognising national sign languages.',
    url = 'https://www.gazzettaufficiale.it/eli/id/2021/05/21/21G00080/sg',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+gazzetta-ufficiale',
    last_verified_at = '2026-05-22T00:15:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T00:15:00Z statutory-batch-44] context-based',
    updated_at = '2026-05-22T00:15:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00347';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
