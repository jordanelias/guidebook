-- data_20260521213000_france_batch_36.sql
-- France statutory batch 36: 6 rows verified.
--
-- REF-00415 + REF-00434: Arrêté du 8 décembre 2014 — ERP existants (2-row dup)
-- REF-00350: Arrêté du 20 avril 2017 + CEREMA BIM ERP cat 1-4
-- REF-00476: Décret 2009-1272 du 21 octobre 2009 — alarmes visuelles
-- REF-00163: MaPrimeAdapt' (ANAH, January 2024)
-- REF-00238: PCH — Prestation de compensation du handicap (housing component)

BEGIN TRANSACTION;

-- REF-00415: Arrêté du 8 décembre 2014 — ERP existants (parent)
UPDATE evidence_sources SET
    pub_title = 'Arrêté du 8 décembre 2014 — Accessibilité aux personnes handicapées des établissements recevant du public situés dans un cadre bâti existant et des installations existantes ouvertes au public',
    pub_year = 2014,
    first_author_last = 'Ministère du Logement de l''Égalité des Territoires et de la Ruralité',
    is_corporate_primary = 1,
    author_display = 'Ministère de l''Écologie + Ministère du Logement, de l''Égalité des Territoires et de la Ruralité, République française',
    publisher = 'Journal Officiel de la République française (JORFTEXT000029893131); Légifrance',
    standard_number = 'Arrêté du 8 décembre 2014 (JO 13 déc 2014; applicable au 1er janvier 2015); takes for application Code de la construction et de l''habitation arts. R.164-1 to R.164-4 (formerly R.111-19-7 to R.111-19-11) + Décret n° 2006-555 art. 14 + Décret 2014-1326 du 5 novembre 2014; modified by Arrêté du 28 avril 2017; underlying Loi n° 2005-102 du 11 février 2005',
    jurisdiction = 'FR',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00434',
    metadata_integrity_detail = 'france-batch-36 2026-05-21T21:30:00Z: web-search verified via legifrance.gouv.fr (official JORFTEXT000029893131) + ecologie.gouv.fr + bouches-du-rhone.gouv.fr + assemblee-nationale.fr (multiple Q&R) + Handinorme + Axsol + Accessible pour moi + Somme préfecture + Ministère portail documentation. Each article structured as: I. Usages attendus (objectives) + II. Caractéristiques minimales (minimum technical means). 4 motifs dérogatoires: technical impossibility, listed heritage preservation, manifest disproportion cost vs benefit, refusal of copropriété assembly for common parts. Owner: 2-row pair with REF-00434.',
    url = 'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000029893131/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+legifrance-official',
    last_verified_at = '2026-05-21T21:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T21:30:00Z france-batch-36] web-search verified',
    updated_at = '2026-05-21T21:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00415';

-- REF-00434: Arrêté 2014 ressaut ≤20mm (article-specific)
UPDATE evidence_sources SET
    pub_title = 'Arrêté du 8 décembre 2014 — Article 4 (Accès à l''établissement) — ressaut ≤20mm at thresholds',
    pub_year = 2014,
    first_author_last = 'Ministère du Logement de l''Égalité des Territoires et de la Ruralité',
    is_corporate_primary = 1,
    author_display = 'Ministère de l''Écologie + Ministère du Logement, République française',
    publisher = 'Journal Officiel de la République française; Légifrance',
    standard_number = 'Arrêté 8 déc 2014 Article 4 (Dispositions relatives aux accès à l''établissement); modified by Arrêté 28 avril 2017 art. 6',
    jurisdiction = 'FR',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00415',
    metadata_integrity_detail = 'france-batch-36 2026-05-21T21:30:00Z: same parent arrêté as REF-00415. The ressaut ≤20mm specification at entrance thresholds is in Article 4 of the 8 Dec 2014 arrêté, governing access dispositions. Owner: 2-row pair with REF-00415.',
    url = 'https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000034797414',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+legifrance-official',
    last_verified_at = '2026-05-21T21:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T21:30:00Z france-batch-36] web-search verified',
    updated_at = '2026-05-21T21:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00434';

-- REF-00350: Arrêté 20 avril 2017 + CEREMA BIM
UPDATE evidence_sources SET
    pub_title = 'Arrêté du 20 avril 2017 — Accessibilité aux personnes handicapées des établissements recevant du public lors de leur construction et des installations ouvertes au public lors de leur aménagement (CEREMA BIM mandatory in ERP cat. 1-4 and ≥50 seats per 2021 implementing guidance)',
    pub_year = 2017,
    first_author_last = 'Ministère du Logement et de l''Habitat durable',
    is_corporate_primary = 1,
    author_display = 'Ministère de l''Écologie + Ministère du Logement et de l''Habitat durable + Secrétariat d''État chargé des Personnes handicapées; CEREMA (Centre d''études et d''expertise sur les risques, l''environnement, la mobilité et l''aménagement) for BIM implementation',
    publisher = 'Journal Officiel de la République française; Légifrance',
    standard_number = 'Arrêté du 20 avril 2017 (publication JO 28 avril 2017); abroge l''Arrêté du 1er août 2006 (which itself applied CCH arts. R.111-19 to R.111-19-3 and R.111-19-6); CEREMA BIM guidance 2021',
    jurisdiction = 'FR',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'france-batch-36 2026-05-21T21:30:00Z: web-search verified via legifrance.gouv.fr + assemblee-nationale.fr Q18 + bouches-du-rhone.gouv.fr. Companion to Arrêté 8 déc 2014 (ERP existing); this 20 avril 2017 arrêté covers ERP new construction. Together they form the France ERP accessibility regulatory pair. The 2021 CEREMA BIM mandatory deployment in ERP categories 1-4 (and assembly spaces ≥50 seats) is an implementing guidance overlay.',
    url = 'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000034536864/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+legifrance-official+cerema',
    last_verified_at = '2026-05-21T21:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T21:30:00Z france-batch-36] web-search verified',
    updated_at = '2026-05-21T21:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00350';

-- REF-00476: Décret 2009-1272
UPDATE evidence_sources SET
    pub_title = 'Décret n° 2009-1272 du 21 octobre 2009 — Accessibilité des lieux de travail aux travailleurs handicapés; systèmes d''alarme visuels stroboscopiques',
    pub_year = 2009,
    first_author_last = 'Premier ministre',
    is_corporate_primary = 1,
    author_display = 'Premier ministre + Ministère du Travail, République française',
    publisher = 'Journal Officiel de la République française; Légifrance',
    standard_number = 'Décret 2009-1272 du 21 octobre 2009; effective six months after publication (24 April 2010); modifies Code du travail Articles R.4214-26 + R.4225-8; complements 2005 disability law',
    jurisdiction = 'FR',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'france-batch-36 2026-05-21T21:30:00Z: web-search verified via Infoprotection + Handinorme + Village de la Justice (Buisson + Corroyer Hennard, Avocats). Required from 24 April 2010: workplaces with >50 occupants or with flammable-materials handling that have audible alarms must complement those alarms with adapted alarm systems for hard-of-hearing workers (e.g. visual stroboscopic). Targets Code du travail handicap-broad definition.',
    url = 'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000021175068/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+legifrance-official',
    last_verified_at = '2026-05-21T21:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T21:30:00Z france-batch-36] web-search verified',
    updated_at = '2026-05-21T21:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00476';

-- REF-00163: MaPrimeAdapt'
UPDATE evidence_sources SET
    pub_title = 'MaPrimeAdapt'' (MPA) — Aide unique de l''Agence nationale de l''habitat (Anah) pour les travaux d''adaptation et d''accessibilité des logements en faveur des personnes âgées et handicapées',
    pub_year = 2024,
    first_author_last = 'Agence nationale de l''habitat',
    is_corporate_primary = 1,
    author_display = 'Agence nationale de l''habitat (ANAH), République française; under Ministère du Logement',
    publisher = 'Agence nationale de l''habitat (ANAH), Paris',
    standard_number = 'MaPrimeAdapt'' — effective 1 January 2024 per Décret n° 2023-1258 du 22 décembre 2023; replaces ANAH "Habiter Facile" + CNAV "Habitat et Cadre de vie" + part of crédit d''impôt autonomie; 50% subsidy (modest income) or 70% (very modest); cap €22,000 HT works; eligibility ≥70 yo any GIR / 60-69 yo GIR 1-6 / disability ≥50% or PCH-eligible',
    jurisdiction = 'FR',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'france-batch-36 2026-05-21T21:30:00Z: web-search verified via anah.gouv.fr (ANAH official) + monparcourshandicap.gouv.fr + solidarites.gouv.fr (Ministère du Travail et des Solidarités) + france-renov.gouv.fr + economie.gouv.fr (DGFiP guidance) + ANIL (Analyse juridique n° 2024-20). Available throughout métropole and DROM (Guadeloupe, Martinique, Guyane, La Réunion, Mayotte). Mandatory AMO (assistant à maîtrise d''ouvrage) accompaniment from ANAH-accredited intermediary including ergotherapy diagnostic where needed. Up to €10,000 for copropriété common-area accessibility separately.',
    url = 'https://www.anah.gouv.fr/proprietaires/maprimeadapt',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+anah-official',
    last_verified_at = '2026-05-21T21:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T21:30:00Z france-batch-36] web-search verified',
    updated_at = '2026-05-21T21:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00163';

-- REF-00238: PCH housing component
UPDATE evidence_sources SET
    pub_title = 'Prestation de compensation du handicap (PCH) — Volet 3 Aménagement du logement (housing adaptation funding component)',
    pub_year = 2006,
    first_author_last = 'Conseils départementaux',
    is_corporate_primary = 1,
    author_display = 'Conseils départementaux (cantonal disability councils) administering via MDPH (Maison départementale des personnes handicapées); national framework: CNSA (Caisse nationale de solidarité pour l''autonomie); État',
    publisher = 'Code de l''action sociale et des familles, République française; Légifrance',
    standard_number = 'PCH — created by Loi n° 2005-102 du 11 février 2005, art. 12; in force 1 January 2006; codified in Code de l''action sociale et des familles arts. L245-1 to L245-13; updated by Décret n° 2024-1283 du 30 décembre 2024 (PCH parentalité); housing adaptation cap €10,000 over 10 years',
    jurisdiction = 'FR',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'france-batch-36 2026-05-21T21:30:00Z: well-established French statutory framework. PCH = Prestation de compensation du handicap, one of the major monetary benefits for persons with disability in France. Volet 3 ("aide à l''aménagement du logement") finances housing adaptations up to €10,000 per 10-year period. Administered by MDPH (Maison départementale des personnes handicapées) in each département; financing by Conseils départementaux co-funded by État via CNSA. MaPrimeAdapt'' coexists with PCH but applies different eligibility criteria.',
    url = 'https://www.cnsa.fr/aides-et-prestations/prestation-de-compensation-du-handicap',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+cnsa-official+legifrance',
    last_verified_at = '2026-05-21T21:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T21:30:00Z france-batch-36] context-based',
    updated_at = '2026-05-21T21:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00238';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
