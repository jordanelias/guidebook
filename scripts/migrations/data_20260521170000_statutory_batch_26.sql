-- data_20260521170000_statutory_batch_26.sql
-- Multi-jurisdictional statutory batch 26: 3 rows verified.
--
-- REF-00457: Switzerland SIA 500 Hindernisfreies Bauen / SN 521 500
-- REF-00366: Korea 1997 편의증진법 (Act on Convenience Promotion for Persons with Disabilities, etc.)
-- REF-00318: Germany KfW 159 Altersgerecht Umbauen (barrier-reduction loan)

BEGIN TRANSACTION;

-- REF-00457: Swiss SIA 500
UPDATE evidence_sources SET
    pub_title = 'SIA Norm 500:2009 — Hindernisfreie Bauten (replaces SN 521 500:1988) — Swiss national standard for barrier-free building',
    pub_year = 2009,
    first_author_last = 'Schweizerischer Ingenieur- und Architektenverein',
    is_corporate_primary = 1,
    author_display = 'Schweizerischer Ingenieur- und Architektenverein (SIA), Zürich',
    publisher = 'Schweizerischer Ingenieur- und Architektenverein (SIA), Zürich',
    standard_number = 'SIA 500:2009 — Hindernisfreie Bauten (Hochbau); replaces SN 521 500:1988; companion VSS-Norm SN 640 075:2014 covers Verkehrsraum (Tiefbau / public outdoor areas)',
    jurisdiction = 'CH',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-26 2026-05-21T17:00:00Z: web-search verified via Schweizerische Fachstelle für hindernisfreie Architektur + Stadt Zürich + Sarnen + Behindertenkonferenz Kanton Zürich + Pro Infirmis + Procap + SPV. Underlying federal law: Behindertengleichstellungsgesetz (BehiG), in force since 1 January 2004. Article 11 of Canton Zürich Constitution also relevant. SIA 500:2009 binding for public buildings, buildings with ≥6 dwellings or >50 workplaces. National network: Schweizerische Fachstelle für hindernisfreie Architektur + Pro Infirmis + Procap (Netzwerk hindernisfreies Bauen).',
    url = 'https://www.hindernisfreie-architektur.ch/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+sia-official+hindernisfreie-architektur',
    last_verified_at = '2026-05-21T17:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T17:00:00Z statutory-batch-26] web-search verified',
    updated_at = '2026-05-21T17:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00457';

-- REF-00366: Korea 1997 편의증진법
UPDATE evidence_sources SET
    pub_title = '장애인·노인·임산부 등의 편의증진 보장에 관한 법률 / Act on the Guarantee of Promotion of Convenience of Persons with Disabilities, the Elderly, Pregnant Women, Etc.',
    pub_year = 1997,
    first_author_last = 'Government of the Republic of Korea',
    is_corporate_primary = 1,
    author_display = 'Government of the Republic of Korea — Ministry of Health and Welfare',
    publisher = 'Government of the Republic of Korea — Korean Law Information Center',
    standard_number = 'Act No. 5332, 10 April 1997 (entered into force 1 January 1998); amended through Act No. 17091 of 24 March 2020',
    jurisdiction = 'KR',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-26 2026-05-21T17:00:00Z: web-search verified via elaw.klri.re.kr (Korean Law Information Center — official) + Current History (UC Press) + WHO MiNDbank + National Human Rights Commission of Korea. First enacted 10 April 1997 (Act No. 5332); entered into force 1 January 1998 (one year after promulgation). Twenty+ amendments through 2020. Companion: 2005 Act on Promoting Transportation Convenience of Mobility Disadvantaged Persons.',
    url = 'https://elaw.klri.re.kr/eng_service/lawView.do?lang=ENG&hseq=20818',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+klri-official',
    last_verified_at = '2026-05-21T17:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T17:00:00Z statutory-batch-26] web-search verified',
    updated_at = '2026-05-21T17:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00366';

-- REF-00318: Germany KfW 159
UPDATE evidence_sources SET
    pub_title = 'KfW 159 — Altersgerecht Umbauen (Kredit) — Federal loan programme for barrier reduction in residential dwellings',
    pub_year = 2024,
    first_author_last = 'Kreditanstalt für Wiederaufbau',
    is_corporate_primary = 1,
    author_display = 'Kreditanstalt für Wiederaufbau (KfW), Frankfurt am Main — German federal development bank',
    publisher = 'Kreditanstalt für Wiederaufbau (KfW), Frankfurt am Main',
    standard_number = 'KfW Programme 159 — Altersgerecht Umbauen; max €50,000 per residential unit; companion grant programme 455-B (€2,500 single measure / €6,250 Altersgerechtes Haus standard)',
    jurisdiction = 'DE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-26 2026-05-21T17:00:00Z: web-search verified via KfW + Architektenkammer Baden-Württemberg + Finanztip + nullbarriere.de + co2online + baufi24. Reduced-rate loan up to €50,000 per residential unit for barrier reduction (Barrierereduzierung) and burglary protection (Einbruchschutz) measures in existing dwellings. Available regardless of applicant age. Term 4-30 years; 1-5 deferred-amortization years. Companion grant programme 455-B reactivated 9 April 2026 with €50M budget for 2026. Funds: walkways, parking, ramps, doors, sanitary rooms, kitchens, lifts, smart-home/control elements, communication systems.',
    url = 'https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestandsimmobilien/F%C3%B6rderprodukte/Altersgerecht-Umbauen-Kredit-(159)/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+kfw-official',
    last_verified_at = '2026-05-21T17:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T17:00:00Z statutory-batch-26] web-search verified',
    updated_at = '2026-05-21T17:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00318';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
