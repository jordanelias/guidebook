-- data_20260522134000_statutory_round4.sql
-- Statutory + grey-round-4 batch.
--
-- REF-VERIFIED-001: Schroeder S, Steinfeld E (1979) "The Estimated Cost of Accessible Buildings"
--                    Syracuse University + US HUD Office of Policy Development and Research
--                    Foundational US accessibility-cost reference; 9 buildings; 0.12-0.5% retrofit / 0.006-0.13% new-build

BEGIN TRANSACTION;

UPDATE evidence_sources SET
    pub_title = 'The Estimated Cost of Accessible Buildings',
    pub_year = 1979,
    first_author_last = 'Schroeder',
    first_author_first = 'S',
    is_corporate_primary = 0,
    author_display = 'Schroeder S, Steinfeld E',
    publisher = 'U.S. Government Printing Office (Washington, DC) — sponsored by U.S. Department of Housing and Urban Development (HUD) Office of Policy Development and Research; conducted at Syracuse University',
    standard_number = 'HUD-PDR-400 series; commissioned alongside Chollet DJ (1979) "A Cost-Benefit Analysis of Accessibility" + Steinfeld E (1979) HUD-PDR-400 Selected Bibliography on Barrier-Free Design; foundational US accessibility-cost research base for ADA 1990, ANSI A117.1 series, Fair Housing Act 1988 amendments. 9 buildings analyzed: high-rise tower, garden apartments, single-family house, college dormitory, convention hall, public branch library, town hall, college classroom, retail shopping center (8 in Syracuse / North Syracuse / Clarkstown / Glen Falls NY + 1 in Detroit MI). Retrofit cost range 0.12-0.5%; original-design cost range 0.006-0.13% (shopping center to college classroom); ~1% commonly cited as conservative upper bound.',
    jurisdiction = 'US',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || ' | statutory-round4 2026-05-22T13:40:00Z: web-search verified via gao.gov HRD-90-44BR (1990 GAO cost-comparison report citing Schroeder+Steinfeld 1979) + independentliving.org (cibrio94 brief survey citing the report) + huduser.gov (HUD official sources) + files.eric.ed.gov ED184282 (Steinfeld 1979 Selected Bibliography companion HUD-PDR-400). Author Steinfeld continued as Director of IDEA Center at SUNY/Buffalo through 2020s; 5-decade body of foundational accessibility-cost + universal-design research.',
    url = 'https://www.huduser.gov/portal/publications/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+gao+huduser+independentliving',
    last_verified_at = '2026-05-22T13:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T13:40:00Z statutory-round4] web-search verified foundational ref',
    updated_at = '2026-05-22T13:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab'
WHERE ref_id = 'REF-VERIFIED-001';

COMMIT;
