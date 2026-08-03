-- data_20260522010000_asia_batch_46.sql
-- Asia statutory batch 46: 3 rows verified.
--
-- REF-00511: Korea 편의증진법 (Accommodation Promotion Act) — 1997 + amendments
-- REF-00164: Singapore HDB EASE Programme — 2012, EASE 2.0 2024
-- REF-00474: Japan 光警報装置 ガイドライン 2016 — Visual Fire Alarm Installation Guideline

BEGIN TRANSACTION;

-- REF-00511: Korea 편의증진법
UPDATE evidence_sources SET
    pub_title = '장애인·노인·임산부 등의 편의증진보장에 관한 법률 (편의증진법) — Act on Accommodation Promotion of the Disabled, the Elderly and Pregnant Women — including 점자블록 (tactile paving) provisions',
    pub_year = 1997,
    first_author_last = 'Government of the Republic of Korea',
    is_corporate_primary = 1,
    author_display = '대한민국 정부 / Government of the Republic of Korea — administering Ministry of Health and Welfare (보건복지부)',
    publisher = '대한민국 법령정보센터 (Korea Law Information Center) — 국가법령정보센터',
    standard_number = '장애인·노인·임산부 등의 편의증진보장에 관한 법률 (편의증진법) — enacted 1997 (제정); 시행령 (enforcement decree) at 대통령령 — major amendments 2002.12.30 (대령17824), 2004.03.17 (대령18312), 2007.10.15 (대령20323 — issued alongside 장애인복지법 시행령 전부개정령); underlying 장애인복지법 (Welfare Law for PwDs)',
    jurisdiction = 'KR',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'asia-batch-46 2026-05-22T01:00:00Z: web-search verified via DBpia (사회보장법연구 enactment-history paper) + WHO MiNDbank legislative database + W3C WAI policies + yeslaw.com 시행령 portal. 점자블록 (tactile paving for visually impaired wayfinding) statutory provisions within this Act. Companion Korean Web Content Accessibility Guidelines 2.1 (WCAG 2.0 derivative). Related acts: 장애인복지법 (Welfare Law for PwDs), 장애인차별금지 및 권리구제 등에 관한 법률 (Anti-Discrimination 2008), 교통약자의 이동편의증진법 (Mobility Enhancement for Mobility Impaired Act).',
    url = 'https://www.law.go.kr/lsInfoP.do?lsiSeq=장애인·노인·임산부등의편의증진보장에관한법률',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+law-go-kr-official+who-mindbank',
    last_verified_at = '2026-05-22T01:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T01:00:00Z asia-batch-46] web-search verified',
    updated_at = '2026-05-22T01:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00511';

-- REF-00164: Singapore HDB EASE Programme
UPDATE evidence_sources SET
    pub_title = 'Enhancement for Active Seniors (EASE) Programme — HDB subsidised home modifications for ageing-in-place',
    pub_year = 2012,
    first_author_last = 'Housing & Development Board',
    is_corporate_primary = 1,
    author_display = 'Housing & Development Board (HDB), Singapore + Agency for Integrated Care (AIC), Ministry of National Development',
    publisher = 'Housing & Development Board (HDB), Singapore Government',
    standard_number = 'EASE Programme — launched July 2012; EASE 2.0 launched 1 April 2024 (expanded set); extended to ~80,000 private homes from 1 April 2026 (age 80+ first round, announced Feb 2026 by National Development Minister Chee Hong Tat). Government subsidy 87.5%–95% cost share (by flat type, 3-room highest). 11 fittings: grab bars (8/10 first toilet, 6 second), slip-resistant floor treatment, ramps (up to 5), lowered toilet entrance kerb, widened toilet entrance, foldable U-profile grab bars, bidet sprays, HFAD (home fire alarm device). Eligibility: Singaporean HDB owner with household member 65+ (or 60-64 with ≥1 ADL need + Functional Assessment Report). ~340,000 households tapped as of January 2025.',
    jurisdiction = 'SG',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'asia-batch-46 2026-05-22T01:00:00Z: web-search verified via hdb.gov.sg (official) + aic.sg + agewellsg.gov.sg + homeanddecor.com.sg + dollarsandsense.sg + thestar.com.my. Companion programs: Home Improvement Programme (HIP), Silver Upgrading Programme (SUP), Neighbourhood Renewal Programme (NRP), Estate Upgrading Programme; Silver Housing Bonus Scheme. ADLs: washing, dressing, feeding, toileting, mobility, transferring. Application via EASE Direct Application e-Service at HDB InfoWeb or Mobile@HDB app.',
    url = 'https://www.hdb.gov.sg/residential/living-in-an-hdb-flat/for-our-seniors/ease',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+hdb-gov-sg-official',
    last_verified_at = '2026-05-22T01:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T01:00:00Z asia-batch-46] web-search verified',
    updated_at = '2026-05-22T01:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00164';

-- REF-00474: Japan 光警報装置 ガイドライン
UPDATE evidence_sources SET
    pub_title = '光警報装置の設置に係るガイドライン (Visual Fire Alarm Installation Guideline)',
    pub_year = 2016,
    first_author_last = '総務省消防庁',
    is_corporate_primary = 1,
    author_display = '総務省消防庁 (Fire and Disaster Management Agency, Ministry of Internal Affairs and Communications) — companion 日本火災報知機工業会 (Japan Fire Alarm Manufacturers Association, 火報工)',
    publisher = '総務省消防庁 (Fire and Disaster Management Agency, MIC), Government of Japan',
    standard_number = '「光警報装置の設置に係るガイドライン」(2016) — recommended (not mandatory) installation guideline for visual flashing fire-alarm devices for hearing-impaired + elderly safety; underlying 障害を理由とする差別の解消の推進に関する法律 (Act on the Elimination of Discrimination against Persons with Disabilities, 2013/施行 2016); 国連障害者権利条約 (UN CRPD, ratified by Japan 2014); 「ユニバーサルデザインを踏まえた火災報知設備等の導入・普及のあり方に関する報告書」(MIC report) + 「聴覚障がい者対応型住宅用火災警報器普及支援事業」grant program',
    jurisdiction = 'JP',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'asia-batch-46 2026-05-22T01:00:00Z: web-search verified via 日本火災報知機工業会 (kaho.or.jp official) + 2017 booklet. The 「光警報装置概要表」+ 「光警報装置外観試験・機能試験結果表」(火報工様式) standard forms for installation summary and inspection results documentation are companion industry instruments. International parallel: UL 1971 "Signaling Devices for the Hearing Impaired" (US 60-120 flashes/min minimum intensity standard).',
    url = 'https://www.fdma.go.jp/laws/tutatu/items/280811_yobou_1.pdf',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+fdma-mic-official+japan-fire-alarm-mfg-assoc',
    last_verified_at = '2026-05-22T01:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T01:00:00Z asia-batch-46] web-search verified',
    updated_at = '2026-05-22T01:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00474';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
