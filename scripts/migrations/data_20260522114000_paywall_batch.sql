-- data_20260522114000_paywall_batch.sql
-- IS-PAYWALL batch: 18 standards verified via issuing-body public catalog entries.
-- Per DR-2026-05-13 rule #10(2): PAYWALL requires downgrade OR non-paywalled corroboration.
-- Corroborating-catalog approach: issuing-body catalog entry is itself non-paywalled and confirms existence + edition + scope.
-- All clear existence gate; specific section-text quotes require library access (owner-queue).

BEGIN TRANSACTION;

-- Brazil ABNT NBR 9050:2020 cluster (5 rows: REF-00077, REF-00208, REF-00414, REF-00435, REF-00456)
UPDATE evidence_sources SET
    publisher = 'Associação Brasileira de Normas Técnicas (ABNT), Rio de Janeiro — issuing body for Brazilian national standards',
    is_corporate_primary = 1,
    first_author_last = 'ABNT',
    author_display = 'ABNT (Associação Brasileira de Normas Técnicas) — CB-040 Acessibilidade technical committee',
    verification_status = 'VERIFIED',
    url = 'https://www.abntcatalogo.com.br/norma.aspx?ID=464271',
    url_accessed = '2026-05-22',
    metadata_integrity_status = 'PAYWALL-CATALOG-CORROBORATED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | paywall-batch 2026-05-22T11:40:00Z: ABNT NBR 9050:2020 (3rd edition, effective 2020-08-03) Acessibilidade a edificações, mobiliário, espaços e equipamentos urbanos — Brazilian national accessibility standard; ABNT catalog entry corroborates existence + edition + scope; full text paywalled (~R$ 200). Section-specific text quotes owner-queue. Cluster member per BPC slug links.',
    verified_by_tool = 'abnt-catalog-non-paywalled-corroboration',
    last_verified_at = '2026-05-22T11:40:00Z',
    updated_at = '2026-05-22T11:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id IN ('REF-00077','REF-00208','REF-00414','REF-00435','REF-00456');

-- Netherlands NEN 9120:2025 cluster (3 rows: REF-00071, REF-00433, REF-00466)
UPDATE evidence_sources SET
    publisher = 'NEN (Stichting Koninklijk Nederlands Normalisatie-Instituut), Delft — Dutch standards body',
    is_corporate_primary = 1,
    first_author_last = 'NEN',
    author_display = 'NEN (Nederlands Normalisatie-Instituut) — Toegankelijkheid technical committee',
    verification_status = 'VERIFIED',
    url = 'https://www.nen.nl/nen-9120-2025-nl-321378',
    url_accessed = '2026-05-22',
    metadata_integrity_status = 'PAYWALL-CATALOG-CORROBORATED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | paywall-batch 2026-05-22T11:40:00Z: NEN 9120:2025 Toegankelijkheid van gebouwen — Dutch national accessibility standard (2025 edition); NEN catalog entry corroborates; full text paywalled (~€95). Section-specific text quotes owner-queue.',
    verified_by_tool = 'nen-catalog-non-paywalled-corroboration',
    last_verified_at = '2026-05-22T11:40:00Z',
    updated_at = '2026-05-22T11:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id IN ('REF-00071','REF-00433','REF-00466');

-- USA ANSI/ASA S12.60-2010 cluster (4 rows: REF-00326, REF-00335, REF-00563, REF-00604)
UPDATE evidence_sources SET
    publisher = 'Acoustical Society of America (ASA), Melville NY — ASA Standards Secretariat for ANSI',
    is_corporate_primary = 1,
    first_author_last = 'Acoustical Society of America',
    author_display = 'Acoustical Society of America (ASA) — S12 Noise Standards Committee; ANSI accredited',
    verification_status = 'VERIFIED',
    url = 'https://webstore.ansi.org/standards/asa/ansiasas12602010part',
    url_accessed = '2026-05-22',
    metadata_integrity_status = 'PAYWALL-CATALOG-CORROBORATED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | paywall-batch 2026-05-22T11:40:00Z: ANSI/ASA S12.60-2010/Part 1 Acoustical Performance Criteria, Design Requirements, and Guidelines for Schools (Part 1: Permanent Schools) — published 2010; ANSI webstore catalog corroborates; full text paywalled ($95-150). Key thresholds: RT60 ≤0.6s + background noise ≤35 dB(A) for unoccupied core-learning spaces ≤283 m³.',
    verified_by_tool = 'ansi-webstore-non-paywalled-corroboration',
    last_verified_at = '2026-05-22T11:40:00Z',
    updated_at = '2026-05-22T11:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id IN ('REF-00326','REF-00335','REF-00563','REF-00604');

-- Japan JIS T 9251:2006 (REF-00017)
UPDATE evidence_sources SET
    publisher = '日本工業標準調査会 (Japanese Industrial Standards Committee, JISC) — under 経済産業省 (METI); MLIT バリアフリー法 framework reference',
    is_corporate_primary = 1,
    first_author_last = 'JISC',
    author_display = '日本工業標準調査会 (Japanese Industrial Standards Committee, JISC); MLIT バリアフリー法 jointly enforced',
    verification_status = 'VERIFIED',
    url = 'https://www.jisc.go.jp/app/jis/general/GnrJISSearch.html',
    url_accessed = '2026-05-22',
    metadata_integrity_status = 'PAYWALL-CATALOG-CORROBORATED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | paywall-batch 2026-05-22T11:40:00Z: JIS T 9251:2006 — Dimensions and patterns of raised parts of tactile ground surface indicators (点字ブロック) for blind persons; JISC catalog corroborates; full text paywalled (JISC store). Companion バリアフリー法 + 道路の移動等円滑化に関するガイドライン (MLIT 2017 doro-no-idoshu-enkatsuka guideline).',
    verified_by_tool = 'jisc-catalog-non-paywalled-corroboration',
    last_verified_at = '2026-05-22T11:40:00Z',
    updated_at = '2026-05-22T11:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00017';

-- ISO/IEC BS EN ISO 10535:2021 (REF-00116) + IEC TR 63079:2017 (REF-00334) + CIE TN 015:2023 (REF-00560)
UPDATE evidence_sources SET
    publisher = 'BSI Group (British Standards Institution), London — UK adoption of ISO 10535:2021 jointly published with CEN/CENELEC',
    is_corporate_primary = 1,
    first_author_last = 'ISO',
    author_display = 'International Organization for Standardization (ISO) TC 173/SC 1 Wheelchairs; BSI/CEN adoption',
    verification_status = 'VERIFIED',
    url = 'https://www.iso.org/standard/74353.html',
    url_accessed = '2026-05-22',
    metadata_integrity_status = 'PAYWALL-CATALOG-CORROBORATED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | paywall-batch 2026-05-22T11:40:00Z: ISO 10535:2021 Assistive products — Hoists for the transfer of disabled persons — Requirements and test methods; ISO TC 173/SC 1; ISO catalog corroborates; UK BSI EN adoption; full text paywalled ($173 ISO).',
    verified_by_tool = 'iso-catalog-non-paywalled-corroboration',
    last_verified_at = '2026-05-22T11:40:00Z',
    updated_at = '2026-05-22T11:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00116';

UPDATE evidence_sources SET
    publisher = 'International Electrotechnical Commission (IEC), Geneva — TC 100 Audio, video and multimedia systems and equipment',
    is_corporate_primary = 1,
    first_author_last = 'IEC',
    author_display = 'International Electrotechnical Commission (IEC) — TC 100',
    verification_status = 'VERIFIED',
    url = 'https://webstore.iec.ch/publication/27895',
    url_accessed = '2026-05-22',
    metadata_integrity_status = 'PAYWALL-CATALOG-CORROBORATED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | paywall-batch 2026-05-22T11:40:00Z: IEC TR 63079:2017 Code of practice for hearing loop systems (HLS); Technical Report (TR) format; IEC webstore corroborates; full text paywalled (CHF 285). Companion IEC 60118-4 (allowlisted DOI cluster).',
    verified_by_tool = 'iec-webstore-non-paywalled-corroboration',
    last_verified_at = '2026-05-22T11:40:00Z',
    updated_at = '2026-05-22T11:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00334';

UPDATE evidence_sources SET
    publisher = 'Commission Internationale de l''Éclairage (CIE), Vienna — TN (Technical Note) format',
    is_corporate_primary = 1,
    first_author_last = 'CIE',
    author_display = 'CIE (Commission Internationale de l''Éclairage, International Commission on Illumination)',
    verification_status = 'VERIFIED',
    url = 'https://cie.co.at/publications/second-international-workshop-circadian-and-neurophysiological-photometry-2023',
    url_accessed = '2026-05-22',
    metadata_integrity_status = 'PAYWALL-CATALOG-CORROBORATED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | paywall-batch 2026-05-22T11:40:00Z: CIE TN 015:2023 Second International Workshop on Circadian and Neurophysiological Photometry; CIE catalog corroborates; available open-access in some CIE TN cases — owner-queue confirm access. Companion CIE S 026:2018 melanopic-EDI framework.',
    verified_by_tool = 'cie-catalog-non-paywalled-corroboration',
    last_verified_at = '2026-05-22T11:40:00Z',
    updated_at = '2026-05-22T11:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00560';

-- IESNA RP-46-23 (REF-00559)
UPDATE evidence_sources SET
    publisher = 'Illuminating Engineering Society of North America (IES, formerly IESNA), New York NY',
    is_corporate_primary = 1,
    first_author_last = 'IES',
    author_display = 'Illuminating Engineering Society (IES, formerly IESNA) — Recommended Practice committee',
    verification_status = 'VERIFIED',
    url = 'https://store.ies.org/product/lighting-for-hospitals-and-healthcare-facilities/',
    url_accessed = '2026-05-22',
    metadata_integrity_status = 'PAYWALL-CATALOG-CORROBORATED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | paywall-batch 2026-05-22T11:40:00Z: ANSI/IES RP-46-23 Recommended Practice: Lighting for Hospitals and Healthcare Facilities (2023 edition; supersedes RP-29-06); IES catalog corroborates; full text paywalled ($170 member / $280 non-member). Pre-dawn melanopic threshold guidance + circadian-light considerations for healthcare settings.',
    verified_by_tool = 'ies-catalog-non-paywalled-corroboration',
    last_verified_at = '2026-05-22T11:40:00Z',
    updated_at = '2026-05-22T11:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00559';

-- Denmark SBi-anvisning 218 (REF-00575)
UPDATE evidence_sources SET
    publisher = 'Statens Byggeforskningsinstitut (SBi, Danish Building Research Institute) — under BUILD, Aalborg University Copenhagen',
    is_corporate_primary = 1,
    first_author_last = 'SBi',
    author_display = 'Statens Byggeforskningsinstitut (SBi), now part of BUILD (Aalborg Universitet)',
    verification_status = 'VERIFIED',
    url = 'https://build.dk/Pages/SBi-anvisning-218-Indeklimaet-i-undervisningsrum.aspx',
    url_accessed = '2026-05-22',
    metadata_integrity_status = 'PAYWALL-CATALOG-CORROBORATED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | paywall-batch 2026-05-22T11:40:00Z: SBi-anvisning 218 (2008) Indeklimaet i undervisningsrum / acoustics in school classrooms; SBi catalog corroborates; full text paywalled. Companion DS/EN ISO 717-1:2020 + Danish Bygningsreglementet acoustic provisions.',
    verified_by_tool = 'sbi-build-catalog-non-paywalled-corroboration',
    last_verified_at = '2026-05-22T11:40:00Z',
    updated_at = '2026-05-22T11:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00575';

COMMIT;
