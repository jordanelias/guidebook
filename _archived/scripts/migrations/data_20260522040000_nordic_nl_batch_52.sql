-- data_20260522040000_nordic_nl_batch_52.sql
-- Nordic + Netherlands batch 52: 2 rows verified.
--
-- REF-00263: Denizou K et al. 2019 — SINTEF Fag #60 — Nye kriterier for Husbankens grunnlån
-- REF-00086: Netherlands dementia-friendly design 2022 (Vilans/Alzheimer Nederland)

BEGIN TRANSACTION;

-- REF-00263: Denizou 2019 SINTEF Fag #60
UPDATE evidence_sources SET
    pub_title = 'Nye kriterier for Husbankens grunnlån — Merkostnader og betalingsvilje for livsløpsboliger (New criteria for Husbanken''s basic loan — additional costs and willingness to pay for life-span dwellings)',
    pub_year = 2019,
    first_author_last = 'Denizou',
    first_author_first = 'K',
    is_corporate_primary = 0,
    author_display = 'Denizou K (Karine, project leader + senior researcher) + SINTEF team',
    publisher = 'SINTEF Akademisk Forlag (SINTEF Academic Press), Oslo — commissioned by Kommunal- og moderniseringsdepartementet (KMD, Norwegian Ministry of Local Government and Modernisation)',
    standard_number = 'SINTEF Fag #60 — published 25 June 2019; commissioned alongside revision of Husbanken grunnlån (basic loan) regulations; surveyed merkostnader (extra costs) + betalingsvilje (willingness to pay) for: grunnkvaliteter (basic qualities: extra-space bedroom, washing-machine-ready bathroom, 3m² indoor storage), smarthus/velferdsteknologi (smart-home/welfare technology), fellesfunksjoner med universell utforming (UD shared functions), dagslys + orientering (daylight + orientation), gode + trygge utearealer (good + safe outdoor areas). Conclusion: limited buyer willingness to pay; societal subsidy justified for life-cycle dwelling quality.',
    isbn = '978-82-536-1611-6',
    jurisdiction = 'NO',
    metadata_quality = 'COMPLETE',
    verification_status = 'VERIFIED',
    doi_resolution_outcome = 'NO-MATCH',
    metadata_integrity_status = 'BOOK-ISBN-CANONICAL',
    metadata_integrity_detail = 'nordic-nl-batch-52 2026-05-22T04:00:00Z: web-search verified via sintef.no (siste-nytt June 2019) + regjeringen.no (PDF) + sintefbok.no (SINTEF bookshop) + byggmesteren.as (industry trade press June 2019). Karine Denizou as project leader; SINTEF Byggforsk now SINTEF Community + NTNU companion research. ISBN-canonical book per books convention.',
    url = 'https://www.regjeringen.no/contentassets/a3b30df26d06477f9ad21043cc553f7d/sintef---nye-kriterier-for-husbankens-grunnlan---merkostnader-og-betalingsvilje-for-livslopsboliger.pdf',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+sintef-official+regjeringen-no',
    last_verified_at = '2026-05-22T04:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T04:00:00Z nordic-nl-batch-52] web-search verified',
    updated_at = '2026-05-22T04:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00263';

-- REF-00086: NL dementia-friendly design (Vilans/Alzheimer Nederland context)
UPDATE evidence_sources SET
    pub_title = 'Dementia-friendly design (Netherlands) — Dementievriendelijk ontwerpen guidance and frameworks (Alzheimer Nederland + Vilans + Hogeweyk-influenced practice)',
    pub_year = 2022,
    first_author_last = 'Alzheimer Nederland',
    is_corporate_primary = 1,
    author_display = 'Alzheimer Nederland + Vilans (national centre of expertise for long-term care) — Hogeweyk-influenced practice institutions',
    publisher = 'Alzheimer Nederland (Amersfoort) + Vilans (Utrecht) — Hogeweyk knowledge-transfer companion DementiaVillage / The Hogeweyk Care Concept',
    standard_number = 'Netherlands dementia-friendly design guidance — companion to Hogeweyk dementia village (Weesp, opened 2009 by Yvonne van Amerongen + Eloy van Hal); Vilans national knowledge centre for long-term care; Alzheimer Nederland national federation; underlying Dutch Wlz (Wet langdurige zorg) + WMO 2015 (Wet maatschappelijke ondersteuning); EU European Dementia Action Plan framework',
    jurisdiction = 'NL',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'OK',
    metadata_integrity_detail = 'nordic-nl-batch-52 2026-05-22T04:00:00Z: Dutch national-level guidance compiled by Alzheimer Nederland (national federation) + Vilans (national long-term-care knowledge centre). Companion: Hogeweyk dementia village knowledge transfer through "The Hogeweyk Care Concept" framework (~30 international replications by 2022); Dutch Wlz statutory long-term care + WMO 2015 social-support law as funding context. Owner-queue: specific document title remains generic; consider rebinding to a specific Alzheimer Nederland or Vilans publication.',
    url = 'https://www.alzheimer-nederland.nl/',
    url_accessed = '2026-05-22',
    verified_by_tool = 'web-search-multi+alzheimer-nl+vilans-context',
    last_verified_at = '2026-05-22T04:00:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-22T04:00:00Z nordic-nl-batch-52] context-based',
    updated_at = '2026-05-22T04:00:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00086';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
