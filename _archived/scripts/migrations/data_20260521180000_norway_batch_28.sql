-- data_20260521180000_norway_batch_28.sql
-- Norway statutory batch 28: 2 rows verified.
--
-- REF-00088: Norwegian Nasjonal faglig retningslinje om demens (Helsedirektoratet)
-- REF-00270: Husbanken Lån til livsløpsboliger (lifetime-standard housing loan)

BEGIN TRANSACTION;

-- REF-00088: Norwegian National Clinical Guideline on Dementia
UPDATE evidence_sources SET
    pub_title = 'Nasjonal faglig retningslinje om demens (National Clinical Guideline on Dementia)',
    pub_year = 2024,
    first_author_last = 'Helsedirektoratet',
    is_corporate_primary = 1,
    author_display = 'Helsedirektoratet (Norwegian Directorate of Health), Oslo',
    publisher = 'Helsedirektoratet (Norwegian Directorate of Health), Oslo',
    standard_number = 'Nasjonal faglig retningslinje om demens — first published 16 August 2017; latest revision 23 February 2024',
    jurisdiction = 'NO',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'norway-batch-28 2026-05-21T18:00:00Z: web-search verified via helsedirektoratet.no (official) + Tidsskrift for Den norske legeforening + Issuu + Utviklingssenter + Nordic Welfare Centre + PMC8752020 systematic review. Continuously-updated national clinical guideline. Companion products: Veiviser demens (2022, sub-guide for primary care pathway with Aldring og helse + Nasjonalforeningen for folkehelsen), Demensplan 2025. Recommendations not legally binding but normative for tjenester (services) and used to define forsvarlighetskravet (standard of care).',
    url = 'https://www.helsedirektoratet.no/retningslinjer/demens',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+helsedirektoratet-official',
    last_verified_at = '2026-05-21T18:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T18:00:00Z norway-batch-28] web-search verified',
    updated_at = '2026-05-21T18:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00088';

-- REF-00270: Husbanken Lån til livsløpsboliger
UPDATE evidence_sources SET
    pub_title = 'Lån til livsløpsboliger (Loan for lifetime-standard housing) — Husbanken (Norwegian State Housing Bank) Forskrift om lån fra Husbanken Kapittel 2',
    pub_year = 2024,
    first_author_last = 'Husbanken',
    is_corporate_primary = 1,
    author_display = 'Husbanken (Norwegian State Housing Bank), Drammen — under Norwegian Ministry of Local Government and Regional Development',
    publisher = 'Husbanken (Norwegian State Housing Bank), Drammen',
    standard_number = 'Forskrift om lån fra Husbanken (FOR-2019-11-18-1546) Kap. 2; established under Lov 2009-05-29 nr. 30 om Husbanken §§ 1, 8, 10; amended 1 Dec 2019, 14 Apr 2020, 25 Jun 2024 (in force 1 Jul 2024)',
    jurisdiction = 'NO',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'norway-batch-28 2026-05-21T18:00:00Z: web-search verified via husbanken.no (official) + Lovdata + Store norske leksikon + VestlandsHus + Blink Hus. Loan up to 90% of construction cost for lifetime-standard housing (livsløpsbolig). Requirements exceed TEK17 building code minimum: no thresholds or physical barriers; all essential functions (entry, kitchen, living room, bedroom, bath/toilet) on entrance level; spacious bedroom with snusirkel (1500mm turn circle); storage room ≥3m²; bath with utility room. Husbanken founded 1946. Replaced earlier "livsløpsstandard" terminology.',
    url = 'https://www.husbanken.no/bransje/lan-og-tilskudd/boligkvalitet/livslopsstandard/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+husbanken-official+lovdata',
    last_verified_at = '2026-05-21T18:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T18:00:00Z norway-batch-28] web-search verified',
    updated_at = '2026-05-21T18:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00270';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
