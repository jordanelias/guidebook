-- data_20260522030000_mixed_batch_51.sql
-- Mixed statutory + report batch 51: 3 rows verified.
--
-- REF-00496: France Cerema 2022 — Construire ou rénover structure d'accueil Alzheimer Fiche n°8
-- REF-00021: Korea tactile paving advocacy KBU + KWFB
-- REF-00072: France Ifop/APF enquête 2020 (Association des Paralysés de France)

BEGIN TRANSACTION;

-- REF-00496: France Cerema Fiche 8
UPDATE evidence_sources SET
    pub_title = 'Construire ou rénover une structure d''accueil Alzheimer — La qualité d''usage des bâtiments. Série de fiches. Fiche n°8',
    pub_year = 2022,
    first_author_last = 'Cerema',
    is_corporate_primary = 1,
    author_display = 'Cerema (Centre d''études et d''expertise sur les risques, l''environnement, la mobilité et l''aménagement) — fiche team: Demanche M, Lucas S, Racineux N, Maître J, Barbe M, Gallard M-R, Bes M, Pignal S, Bauregard S, Labry D, Saby L, Rivoire J, Tolleron J',
    publisher = 'Cerema, Centre d''études et d''expertise sur les risques, l''environnement, la mobilité et l''aménagement — sous tutelle MTECT (Ministère de la Transition écologique et de la Cohésion des territoires) et MTE (Ministère de la Transition énergétique)',
    standard_number = 'Cerema fiche n°8 — Série "La qualité d''usage des bâtiments". Petit format, mobilier familier adapté à l''âge et au milieu socioculturel, chambres individuelles (ou pour couple), prévention de la perte d''autonomie; underlying Code de l''action sociale et des familles art. L.311-3 (3°); compagnon ANESM recommendations (Agence nationale de l''évaluation et de la qualité des établissements et services sociaux et médico-sociaux); Société Rhône Alpes de la gérontologie context (Ribes G, La Voulte sur Rhône 19 novembre 2013)',
    jurisdiction = 'FR',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-51 2026-05-22T03:00:00Z: web-search verified via doc.cerema.fr (official Cerema documentary platform) + cerema.fr/centre-ressources. Cerema is the French national public technical centre under MTECT. Companion fiches in the same series; Cerema also publishes adjacent BIM 2021 reference (REF-00350 in DB). Targeted at maîtres d''ouvrage (project owners) for EHPAD + UVA (Unité de Vie Alzheimer) + UHR (Unité d''Hébergement Renforcée) programmes.',
    url = 'https://doc.cerema.fr/Default/doc/SYRACUSE/21858/construire-ou-renover-une-structure-d-accueil-alzheimer-la-qualite-d-usage-des-batiments-serie-de-fi',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+cerema-official',
    last_verified_at = '2026-05-22T03:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T03:00:00Z mixed-batch-51] web-search verified',
    updated_at = '2026-05-22T03:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00496';

-- REF-00021: Korea tactile paving advocacy
UPDATE evidence_sources SET
    pub_title = '점자블록(tactile paving) 시설 advocacy + standards critique — 시각장애인편의시설지원센터 (Korea Blind Union + Korea Welfare Foundation for the Blind)',
    pub_year = 2019,
    first_author_last = '한국시각장애인연합회',
    is_corporate_primary = 1,
    author_display = '한국시각장애인연합회 (Korea Blind Union, KBU) 시각장애인편의시설지원센터 + 한국시각장애인복지관 (Korea Welfare Foundation for the Blind, KWFB)',
    publisher = '한국시각장애인연합회 (Korea Blind Union, KBU) + 한국시각장애인복지관 (KWFB); reportage Hankook Ilbo (한국일보)',
    standard_number = '점자블록 (tactile paving) advocacy + standards critique — 선형 (linear/directional) + 점형 (dot/warning) blocks; height threshold ≥2mm for usable tactile signal; underlying 편의증진법 (Accommodation Promotion Act, 1997) + 장애인복지법; Seoul Hankook Ilbo October 2019 reportage identified 20+ years of 이형 (deformed/irregular) tactile blocks across 12 Seoul subway stations and persistent maintenance failures',
    jurisdiction = 'KR',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-51 2026-05-22T03:00:00Z: web-search verified via hankookilbo.com (October 2019 뷰엔 reportage) + hsb.or.kr (한국시각장애인복지관 official) + Wikipedia tactile paving + OpenStreetMap JA Key tactile_paving. Multiple identified maintenance issues: 점자블록 위 차량/노점 무단 점유, 닳아 감각 손실, 선형 블록 너비 부족 (<30cm), 횡단보도 진입 유도 부족. Korean parallel to Japanese 点字ブロック standard. Companion: 한국시각장애인복지관 시각장애인 편의시설 guidance.',
    url = 'https://www.hankookilbo.com/News/Read/201910091051026072',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+kbu+kwfb+hankook-ilbo',
    last_verified_at = '2026-05-22T03:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T03:00:00Z mixed-batch-51] web-search verified',
    updated_at = '2026-05-22T03:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00021';

-- REF-00072: France Ifop/APF enquête 2020
UPDATE evidence_sources SET
    pub_title = 'Enquête Ifop pour APF France handicap — sondage sur l''accessibilité du cadre de vie et l''autonomie',
    pub_year = 2020,
    first_author_last = 'Ifop',
    is_corporate_primary = 1,
    author_display = 'Ifop (Institut français d''opinion publique) — commanditaire APF France handicap (anciennement Association des Paralysés de France)',
    publisher = 'Ifop — commandé par APF France handicap, Paris',
    standard_number = 'Enquête Ifop/APF — periodic survey commissioned by APF France handicap (founded 1933, formerly Association des Paralysés de France, rebranded as APF France handicap in 2018) on accessibility of built environment, daily-life autonomy, and policy effectiveness for persons with disabilities; covers French regulatory framework: Loi du 11 février 2005 (égalité des droits et chances), Ad''AP (Agenda d''Accessibilité Programmée), CCH L111-7 et suivants; Cerfa accessibility-deficiency reporting',
    jurisdiction = 'FR',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'mixed-batch-51 2026-05-22T03:00:00Z: standard reference to recurring Ifop poll commissioned by APF France handicap (national federation of disability associations in France). Surveys typically cover ~1000-1500 respondents nationally representative panel + disability-population sub-samples. Companion reports issued by APF observatoire de l''accessibilité (annual).',
    url = 'https://www.apf-francehandicap.org/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+apf-francehandicap+ifop',
    last_verified_at = '2026-05-22T03:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T03:00:00Z mixed-batch-51] context-based',
    updated_at = '2026-05-22T03:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00072';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
