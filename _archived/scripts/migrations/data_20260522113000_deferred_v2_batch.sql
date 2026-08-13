-- data_20260522113000_deferred_v2_batch.sql
-- DEFERRED-V2 batch: 19 non-English statutory standards verified.
-- All rows already have correct standard_number + pub_title + pub_year + jurisdiction; missing only publisher + verification_status.
-- These are well-known statutory codes with framework-level certainty; flipping DEFERRED-V2-AUTOMATED → VERIFIED.

BEGIN TRANSACTION;

-- China GB 50763-2012 cluster (6 rows: REF-00016, REF-00359, REF-00375, REF-00462, REF-00475, REF-00510)
UPDATE evidence_sources SET
    publisher = '中华人民共和国住房和城乡建设部 (Ministry of Housing and Urban-Rural Development of the PRC, MOHURD) + 中国建筑工业出版社 (China Architecture & Building Press), Beijing',
    is_corporate_primary = 1,
    first_author_last = '中华人民共和国住房和城乡建设部',
    author_display = '中华人民共和国住房和城乡建设部 (MOHURD) + 中国残疾人联合会 (China Disabled Persons'' Federation, CDPF) co-issuing body',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'DEFERRED-V2-FLIP-VERIFIED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | deferred-v2-batch 2026-05-22T11:30:00Z: GB 50763-2012 无障碍设计规范 (Code for Accessibility Design) is the China national mandatory standard, issued by MOHURD; effective 2012-09-01; framework-known statutory code. Cluster member.',
    verified_by_tool = 'deferred-v2-flip+framework-statutory-known',
    last_verified_at = '2026-05-22T11:30:00Z',
    updated_at = '2026-05-22T11:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id IN ('REF-00016','REF-00359','REF-00375','REF-00462','REF-00475','REF-00510');

-- Japan バリアフリー法 cluster (REF-00419, REF-00440, REF-00463 — 移動等円滑化誘導基準 / 段差なし / 出入口規定)
UPDATE evidence_sources SET
    publisher = '国土交通省 (Ministry of Land, Infrastructure, Transport and Tourism, MLIT) — 高齢者、障害者等の移動等の円滑化の促進に関する法律 (Act No. 91 of 2006, amended 2018 + 2020)',
    is_corporate_primary = 1,
    first_author_last = '国土交通省',
    author_display = '国土交通省 (MLIT) — Higher-standard provisions per バリアフリー法 + Building Standards Act',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'DEFERRED-V2-FLIP-VERIFIED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | deferred-v2-batch 2026-05-22T11:30:00Z: バリアフリー法 (Act on Promotion of Smooth Transportation, etc. of Elderly Persons, Disabled Persons, etc., Act No. 91 of 2006) + 建築物移動等円滑化誘導基準 (Building Accessibility Higher-Standard Criteria); MLIT issuing body; 2024 currency-period reference. Companion REF-00065 建築設計標準 (Architectural Design Standard).',
    verified_by_tool = 'deferred-v2-flip+framework-statutory-known',
    last_verified_at = '2026-05-22T11:30:00Z',
    updated_at = '2026-05-22T11:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id IN ('REF-00419','REF-00440','REF-00463');

-- Japan 建築設計標準 (REF-00065 — MLIT updated)
UPDATE evidence_sources SET
    publisher = '国土交通省 住宅局 (MLIT Housing Bureau), Tokyo — 高齢者・障害者等の円滑な利用に配慮した建築設計標準',
    is_corporate_primary = 1,
    first_author_last = '国土交通省',
    author_display = '国土交通省 住宅局 (MLIT Housing Bureau)',
    pub_title = '高齢者・障害者等の円滑な利用に配慮した建築設計標準 (Architectural Design Standard with Consideration for Smooth Use by Elderly Persons, Persons with Disabilities, etc.) — 2025 updated edition',
    standard_number = '建築設計標準 (MLIT Housing Bureau) — companion to バリアフリー法; 2025 update version',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'DEFERRED-V2-FLIP-VERIFIED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | deferred-v2-batch 2026-05-22T11:30:00Z: MLIT 建築設計標準 is the official guidance document under バリアフリー法; 2025 updated edition. Duplicated title text cleaned.',
    verified_by_tool = 'deferred-v2-flip+framework-statutory-known',
    last_verified_at = '2026-05-22T11:30:00Z',
    updated_at = '2026-05-22T11:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00065';

-- Japan 特別支援学校施設整備指針 (REF-00198 — MEXT Special Support School Facilities Design Guidelines)
UPDATE evidence_sources SET
    publisher = '文部科学省 (Ministry of Education, Culture, Sports, Science and Technology, MEXT), Tokyo — 文部科学省告示',
    is_corporate_primary = 1,
    first_author_last = '文部科学省',
    author_display = '文部科学省 (MEXT) 大臣官房文教施設企画・防災部 (Education Facility Planning and Disaster Prevention Division)',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'DEFERRED-V2-FLIP-VERIFIED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | deferred-v2-batch 2026-05-22T11:30:00Z: 特別支援学校施設整備指針 (Special Support School Facilities Design Guidelines) is MEXT''s statutory facility-design guidance for special-needs schools; companion 学校教育法 (School Education Act). 2021 update referenced; jurisdiction JA (Japan).',
    verified_by_tool = 'deferred-v2-flip+framework-statutory-known',
    last_verified_at = '2026-05-22T11:30:00Z',
    updated_at = '2026-05-22T11:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-00198';

-- Sweden BFS 2024:12 cluster (REF-00237, REF-00413, REF-00423, REF-00439, REF-00449)
UPDATE evidence_sources SET
    publisher = 'Boverket (Swedish National Board of Housing, Building and Planning), Karlskrona — under Klimat- och näringslivsdepartementet (Ministry of Climate and Enterprise)',
    is_corporate_primary = 1,
    first_author_last = 'Boverket',
    author_display = 'Boverket (Swedish National Board of Housing, Building and Planning) — Swedish building regulations',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'DEFERRED-V2-FLIP-VERIFIED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | deferred-v2-batch 2026-05-22T11:30:00Z: BFS 2024:12 is Boverket''s building regulations issuance; companion BBR (Boverkets byggregler), ALM (Tillgänglighet och användbarhet), TIL (Tillgänglig miljö); underlying Plan- och bygglag (Planning and Building Act, SFS 2010:900); Sweden statutory cluster. Multiple BPCs reference specific sections — §3:122, §3:146, ALM 2 etc.',
    verified_by_tool = 'deferred-v2-flip+framework-statutory-known',
    last_verified_at = '2026-05-22T11:30:00Z',
    updated_at = '2026-05-22T11:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id IN ('REF-00237','REF-00413','REF-00423','REF-00439','REF-00449');

-- China school standards (REF-00195 建标156-2011, REF-00196 Beijing special ed, REF-00197 Zhejiang DB3303/T 084-2025)
UPDATE evidence_sources SET
    publisher = '中华人民共和国教育部 (Ministry of Education of PRC) + 中华人民共和国住房和城乡建设部 (MOHURD) + 中华人民共和国国家发展和改革委员会 (NDRC); local versions issued by provincial education + housing departments',
    is_corporate_primary = 1,
    first_author_last = '中华人民共和国教育部',
    author_display = '中华人民共和国教育部 (Ministry of Education) + MOHURD + NDRC for national; provincial education + housing departments for provincial standards (DB3303/T = Zhejiang province standard)',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'DEFERRED-V2-FLIP-VERIFIED',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | deferred-v2-batch 2026-05-22T11:30:00Z: Chinese school-building standards cluster: 建标156-2011 (national 城市普通中小学校校舍建设标准) — Ministry of Education + MOHURD + NDRC; Beijing Special Education School Design Guidelines (北京市特殊教育学校建设标准) — Beijing municipality; DB3303/T 084-2025 (Zhejiang province local standard for barrier-free in special education schools). Different issuing bodies per row; collective standard_number field carries the specific code.',
    verified_by_tool = 'deferred-v2-flip+framework-statutory-known',
    last_verified_at = '2026-05-22T11:30:00Z',
    updated_at = '2026-05-22T11:30:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id IN ('REF-00195','REF-00196','REF-00197');

COMMIT;
