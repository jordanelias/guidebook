-- data_20260521185000_statutory_batch_30.sql
-- Multi-jurisdictional statutory batch 30: 4 rows verified.
--
-- REF-00322: Sweden Boverkets byggregler (BBR) BFS 2011:6
-- REF-00346: Sweden Stockholm en stad för alla
-- REF-00597: Sweden Mynak Riktlinjer för synergonomi (Visual Ergonomics Guidelines)
-- REF-00319: Switzerland IV/AI disability insurance home adaptation co-funding

BEGIN TRANSACTION;

-- REF-00322: Sweden BBR
UPDATE evidence_sources SET
    pub_title = 'Boverkets byggregler (BFS 2011:6) — föreskrifter och allmänna råd, BBR (Swedish Building Regulations) — Tillgänglighet i gemensamma tvättstugor (Accessibility in shared laundries)',
    pub_year = 2024,
    first_author_last = 'Boverket',
    is_corporate_primary = 1,
    author_display = 'Boverket (Swedish National Board of Housing, Building and Planning), Karlskrona',
    publisher = 'Boverket (Swedish National Board of Housing, Building and Planning), Karlskrona',
    standard_number = 'BFS 2011:6 (most recent amendment BFS 2024:14); underlying Plan- och bygglag PBL (2010:900) and Plan- och byggförordning PBF (2011:338); new BFS 2024:12 (specific accessibility regulation) in force 1 Jul 2025 with transition to 30 Jun 2026; consolidated BBR also published',
    jurisdiction = 'SE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-30 2026-05-21T18:50:00Z: web-search verified via boverket.se (official) + Boverket''s Knowledge Base (PBL kunskapsbanken) + rinfo.boverket.se. Original BFS 2011:6; over 30 BFS amendments through BFS 2024:14. Section 3:1 covers accessibility/usability for persons with reduced mobility or orientation. Excludes vacation homes ≤2 dwellings. Stretcher transport must be possible from every dwelling. New 2024 framework includes BFS 2024:12 specifically for tillgänglighet och användbarhet i byggnader (accessibility/usability of buildings).',
    url = 'https://www.boverket.se/sv/PBL-kunskapsbanken/regler-om-byggande/boverkets-byggregler/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+boverket-official',
    last_verified_at = '2026-05-21T18:50:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T18:50:00Z statutory-batch-30] web-search verified',
    updated_at = '2026-05-21T18:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00322';

-- REF-00346: Stockholm en stad för alla
UPDATE evidence_sources SET
    pub_title = 'Stockholm — en stad för alla. Handbok om tillgänglighet för funktionsnedsatta i byggnader, gatu- och parkmiljö',
    pub_year = 2009,
    first_author_last = 'Stockholms stad',
    is_corporate_primary = 1,
    author_display = 'Stockholms stad — Tillståndsenheten / Stadsbyggnadskontoret',
    publisher = 'Stockholms stad, Stadsbyggnadskontoret',
    standard_number = 'Stockholm en stad för alla — handbok; tied to Handikappolitiskt program för Stockholms stad; references FN''s 22 standardregler (standard rule no. 5: tillgänglighet) and Boverkets föreskrifter; companion to lag om enkelt avhjälpta hinder',
    jurisdiction = 'SE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-30 2026-05-21T18:50:00Z: web-search verified via tillstand.stockholm (official) + start.stockholm. Municipal handbook from Stockholms stad. Goal: Stockholm to be world''s most accessible capital by 2010 (per Handikappolitiskt program). Targets all stadens verksamheter (city services). Cites: Boverket''s "Enklare utan hinder" (2005), Boverket''s regulations, PBL. Practical guidance for entréer, ramps, lifts/stairs, K-märkta (heritage-protected) buildings, uteserveringar (outdoor cafés) permissions.',
    url = 'https://tillstand.stockholm/globalassets/foretag-och-organisationer/tillstand-och-regler/tillstand-regler-och-tillsyn/lokal-och-fastigheter/handbocker-och-riktlinjer-vid-byggnation-i-stockholm/stockholm_en-stad-for-alla.pdf',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+stockholms-stad-official',
    last_verified_at = '2026-05-21T18:50:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T18:50:00Z statutory-batch-30] web-search verified',
    updated_at = '2026-05-21T18:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00346';

-- REF-00597: Swedish Visual Ergonomics Guidelines
UPDATE evidence_sources SET
    pub_title = 'Riktlinjer för synergonomi — belysning och synförhållanden på arbetsplatsen / Guidelines for Visual Ergonomics — Lighting and Vision in the Workplace',
    pub_year = 2019,
    first_author_last = 'Myndigheten för arbetsmiljökunskap',
    is_corporate_primary = 1,
    author_display = 'Myndigheten för arbetsmiljökunskap (Mynak, Swedish Agency for Work Environment Expertise), Gävle',
    publisher = 'Myndigheten för arbetsmiljökunskap (Mynak), Gävle',
    standard_number = 'Riktlinjer för synergonomi (Mynak); references underlying Arbetsmiljöverket regulations AFS 2020:1 Arbetsplatsens utformning (superseded by AFS 2023:12 Utformning av arbetsplatser); underlying standards SS-EN 12464-1:2021 (indoor lighting) and SS-EN 12464-2:2014 (outdoor lighting)',
    jurisdiction = 'SE',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-30 2026-05-21T18:50:00Z: web-search verified via mynak.se (official) + av.se (Arbetsmiljöverket, parallel agency) + Arbetsmiljöverkets Knowledge Compilation 2019:2 (Dagsljuskrav och utblick) + Elcenter guide. NB: Two Swedish agencies in this space: Arbetsmiljöverket (regulator/inspectorate, AFS rules) and Mynak (Agency for Work Environment Expertise, knowledge products). Mynak''s Guidelines for Visual Ergonomics are knowledge product, not statutory; underlying statutory framework is AFS 2020:1 → AFS 2023:12. English translation available. Targets occupational health services and work environment consultants; also useful for architects, lighting consultants, ljusdesigners.',
    url = 'https://mynak.se/publikationer/riktlinjer-for-synergonomi-belysning-och-synforhallanden-pa-arbetsplatsen/',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+mynak-official+av',
    last_verified_at = '2026-05-21T18:50:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T18:50:00Z statutory-batch-30] web-search verified',
    updated_at = '2026-05-21T18:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00597';

-- REF-00319: Swiss IV/AI disability insurance home adaptation
UPDATE evidence_sources SET
    pub_title = 'Invalidenversicherung (IV) / Assurance Invalidité (AI) — Hilfsmittel (Hilfsmittelliste) for home adaptation co-funding',
    pub_year = 2024,
    first_author_last = 'Bundesamt für Sozialversicherungen',
    is_corporate_primary = 1,
    author_display = 'Bundesamt für Sozialversicherungen (BSV) / Office fédéral des assurances sociales (OFAS) — Federal Social Insurance Office, Bern; administered by cantonal IV-Stellen',
    publisher = 'Bundesamt für Sozialversicherungen (BSV), Bern',
    standard_number = 'Bundesgesetz über die Invalidenversicherung (IVG, SR 831.20); IV is 1st pillar of Swiss social insurance system; 2024 employer/employee contribution rate 1.4% of salary',
    jurisdiction = 'CH',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'statutory-batch-30 2026-05-21T18:50:00Z: web-search verified via bsv.admin.ch (official) + ahv-iv.ch (Information Center OASI/DI) + ch.ch (federal portal) + moneyland.ch + iamexpat.ch + The Poor Swiss + Swiss AIDS Federation + Fidulex. Compulsory social insurance for all Swiss residents. Covers: disability pensions (40%+ work capacity reduction; full pension ≥70%), rehabilitation measures (Eingliederungsmassnahmen), Hilfsmittel (assistive devices including home adaptation, wheelchairs, prostheses), Assistenzbeitrag (assistance contribution at 34.30 CHF/hour base / 51.50 CHF/hour skilled help to support living at home rather than institutional care). ~2.6% of Swiss residents on invalidity pension as of 2020.',
    url = 'https://www.bsv.admin.ch/bsv/de/home/sozialversicherungen/iv.html',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+bsv-admin-official+ahv-iv',
    last_verified_at = '2026-05-21T18:50:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T18:50:00Z statutory-batch-30] web-search verified',
    updated_at = '2026-05-21T18:50:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00319';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
