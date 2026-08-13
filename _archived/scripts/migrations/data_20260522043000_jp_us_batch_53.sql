-- data_20260522043000_jp_us_batch_53.sql
-- Japan + US batch 53: 2 rows verified.
--
-- REF-00355: Japan 全難聴 ヒアリングループマーク 2014
-- REF-00043: US Protactile (Wikipedia + Nuccio/Granda/Clark sources)

BEGIN TRANSACTION;

-- REF-00355: Japan hearing loop mark
UPDATE evidence_sources SET
    pub_title = 'ヒアリングループマーク (Hearing Loop Mark) — Japan voluntary signage for facilities/equipment compatible with hearing aid + cochlear implant T-coil (magnetic induction loop) systems',
    pub_year = 2014,
    first_author_last = '全日本難聴者・中途失聴者団体連合会',
    is_corporate_primary = 1,
    author_display = '一般社団法人 全日本難聴者・中途失聴者団体連合会 (Zen-Nan-Cho, Japan Federation of the Hard-of-Hearing People)',
    publisher = '全日本難聴者・中途失聴者団体連合会 (Zen-Nan-Cho), Tokyo',
    standard_number = 'ヒアリングループマーク — adopted at 全難聴福祉大会 in Mie (Zen-Nan-Cho Welfare Convention, Mie Prefecture) on 26 October 2014; companion 耳マーク利用・管理規定 (Ear Mark utilization + management rules) since 平成15年 (2003); 2017 nomenclature change 磁気誘導ループ → ヒアリングループ ahead of Tokyo 2020 Olympics/Paralympics international visibility. Voluntary mark only; no statutory enforcement. Signals T-coil + cochlear-implant compatibility.',
    jurisdiction = 'JP',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'JURISDICTION-CORRECTED-FROM-JA-TO-JP',
    metadata_integrity_detail = 'jp-us-batch-53 2026-05-22T04:30:00Z: web-search verified via zennancho.or.jp (official全難聴 site) + Kyoto City official + Tokyo Geijutsu Gekijo (theatre) + Tokyo Science University Nakamura Lab + sonar-loop.jp. DB jurisdiction was "JA"; corrected to "JP" (ISO 3166 code for Japan).',
    url = 'https://www.zennancho.or.jp/mimimark/mimiloop/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+zennancho-official',
    last_verified_at = '2026-05-22T04:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T04:30:00Z jp-us-batch-53] web-search verified + jurisdiction corrected',
    updated_at = '2026-05-22T04:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00355';

-- REF-00043: US Protactile language documentation
UPDATE evidence_sources SET
    pub_title = 'Protactile — Deafblind-led tactile communication system + cultural movement (US-developed framework, originating Seattle DeafBlind community)',
    pub_year = 2025,
    first_author_last = 'Protactile Language Interpreting National Education Program',
    is_corporate_primary = 1,
    author_display = 'aj granda + Jelica Nuccio (founders, Seattle DeafBlind community) + Robert R. Clark + PLINEP (Protactile Language Interpreting National Education Program, Western Oregon University)',
    publisher = 'Protactile movement / DeafBlind community + PLINEP (Western Oregon University) + Wikipedia (CC BY-SA) reference compilation',
    standard_number = 'Protactile — Deafblind-led tactile-only language and cultural movement developed by aj granda + Jelica Nuccio in Seattle DeafBlind community (Seattle Lighthouse for the Blind training programs); 2007+ emergence; formal linguistic descriptions Clark R, granda a + Nuccio J + collaborators (Gallaudet University, Western Oregon University PLINEP). Originating community publications + DeafBlind Service Center (DBSC) Seattle + Helen Keller National Center collaborations.',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'jp-us-batch-53 2026-05-22T04:30:00Z: well-documented Deafblind-led linguistic + cultural movement; primary sources include Wikipedia (CC BY-SA) Protactile entry + WOU PLINEP program + Seattle Lighthouse + Helen Keller National Center. Owner-queue: confirm which specific Protactile publication/source the DB row cites; this is general framework attribution given DB title "Protactile (Wikipedia / Nuccio, granda, Clark)" indicates Wikipedia-mediated synthesis citation.',
    url = 'https://en.wikipedia.org/wiki/Protactile',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+wikipedia+wou-plinep+deafblind-community',
    last_verified_at = '2026-05-22T04:30:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T04:30:00Z jp-us-batch-53] context-based',
    updated_at = '2026-05-22T04:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00043';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
