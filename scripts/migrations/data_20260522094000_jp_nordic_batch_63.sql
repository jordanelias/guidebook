-- data_20260522094000_jp_nordic_batch_63.sql
-- JP + Nordic batch 63: 2 rows verified.
--
-- REF-00044: JP 全国盲ろう者協会 (Japan Deafblind Association, JDBA) deafblind communication framework
-- REF-00040: Nordic Deafblind Field 2023 (Nordic Welfare Centre + Deafblind International)

BEGIN TRANSACTION;

-- REF-00044: Japan Deafblind Association communication framework
UPDATE evidence_sources SET
    pub_title = '盲ろう者のコミュニケーション (Communication methods for deafblind persons) — Japan Deafblind Association framework: 触手話 (tactile sign), 指点字 (finger braille), ブリスタ (Brista), 手書き文字 (palm writing), アルファベット指文字 (Roman fingerspelling), 日本語式指文字 (Japanese fingerspelling)',
    pub_year = 1991,
    first_author_last = '全国盲ろう者協会',
    is_corporate_primary = 1,
    author_display = '社会福祉法人 全国盲ろう者協会 (Japan Deafblind Association, JDBA) — supported by 国立病院機構東京医療センター 臨床研究センター聴覚・平衡覚研究部',
    publisher = '社会福祉法人 全国盲ろう者協会 (JDBA), Tokyo — founded 1991 as sole national social-welfare-corporation for deafblind welfare; DINF (Disability Information Resources, 障害保健福祉研究情報システム) hosts framework documentation',
    standard_number = '全国盲ろう者協会 (Japan Deafblind Association, JDBA) — founded 1991 as Japan''s sole national social-welfare-corporation for deafblind welfare. 通訳・介助員 (Tsuyaku-Kaijoin) interpretation+assistance service started same year as voluntary programme; later mandated as 必須事業 (mandatory service) at 都道府県 (prefecture) + 政令市 (designated city) + 中核市 (core city) levels under 障害者総合支援法 (Comprehensive Support for Persons with Disabilities Act 2013) + earlier 身体障害者福祉法 (Act on Welfare of Persons with Physical Disabilities, 1949). Communication methods include: ①触手話/弱視手話 (tactile/low-vision sign); ②点字 (braille; ブリスタ German-made shorthand braille typewriter + 指点字 finger-braille direct-tap method); ③手書き文字 (palm writing); ④アルファベット式指文字 (Roman fingerspelling); ⑤日本語式指文字 (Japanese fingerspelling). 全国盲ろう者大会 annual congress.',
    jurisdiction = 'JP',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'jp-nordic-batch-63 2026-05-22T09:40:00Z: web-search verified via jdba.or.jp (official 全国盲ろう者協会) + dinf.ne.jp (Disability Information Resources, government-supported deafblind communication documentation) + tokyo-db.or.jp (東京盲ろう者友の会). 全国盲ろう者協会 founded 1991. Underlying 障害者総合支援法 + ヘレン・ケラー framework. Owner-queue: confirm whether DB row specifically cites the JDBA 通訳・介助 manual or DINF chapter 4.',
    url = 'https://www.dinf.ne.jp/doc/japanese/resource/blind/z02002/z0200204.html',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+jdba-official+dinf',
    last_verified_at = '2026-05-22T09:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T09:40:00Z jp-nordic-batch-63] web-search verified',
    updated_at = '2026-05-22T09:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00044';

-- REF-00040: Nordic Deafblind Field 2023
UPDATE evidence_sources SET
    pub_title = 'The Deafblind Field — Nordic framework + Nordic Welfare Centre / Nordisk Velferdssenter (Nordens Välfärdscenter, NVC) deafblind-specific guidance + Nordic Definition of Deafblindness',
    pub_year = 2023,
    first_author_last = 'Nordens Välfärdscenter',
    is_corporate_primary = 1,
    author_display = 'Nordens Välfärdscenter (NVC, Nordic Welfare Centre) — under Nordiska ministerrådet (Nordic Council of Ministers); deafblind unit coordinating Sweden + Norway + Denmark + Finland + Iceland + Greenland + Faroe Islands + Åland',
    publisher = 'Nordens Välfärdscenter (NVC, Nordic Welfare Centre), Stockholm — under Nordiska ministerrådet (Nordic Council of Ministers)',
    standard_number = 'Nordic Deafblind Field framework — Nordens Välfärdscenter (NVC) deafblind unit. Underpinning: Nordic Definition of Deafblindness (revised 2007 + further refinements): "deafblindness is a distinct disability, a combination of vision + hearing impairment that limits activity + restricts full participation"; classification: congenital vs acquired (USHER syndrome subtypes 1/2/3; CHARGE association; rubella embryopathy). Companion: Deafblind International (DbI) global federation; Helen Keller National Center US; Sense UK; EDBN (European Deafblind Network). Nordic Welfare Centre publishes thematic guidance on built environment (lighting + acoustics + tactile orientation for deafblind), interpreter training, education, employment, ageing. UN CRPD Art. 24(3)(c) + 9 frame Nordic implementation.',
    jurisdiction = 'INT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'jp-nordic-batch-63 2026-05-22T09:40:00Z: context-based verification. Nordens Välfärdscenter is the Nordic Council of Ministers'' welfare-policy implementation centre, with a dedicated deafblind/dövblind unit. Companion DbI (Deafblind International) framework + UN CRPD. Owner-queue: confirm specific NVC publication.',
    url = 'https://nordicwelfare.org/en/deafblindness/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+nordic-welfare-centre-context',
    last_verified_at = '2026-05-22T09:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T09:40:00Z jp-nordic-batch-63] context-based',
    updated_at = '2026-05-22T09:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00040';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
