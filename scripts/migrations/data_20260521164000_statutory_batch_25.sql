-- data_20260521164000_statutory_batch_25.sql
-- Multi-jurisdictional statutory batch 25: 6 rows verified in 3 dup pairs.
--
-- Finland: REF-00424 (parent F1) + REF-00459 (door-specific) -- both cite 241/2017
-- Italy:   REF-00364 (parent DM 236/89) + REF-00460 (door-specific)
-- Portugal: REF-00365 (parent DL 163/2006) + REF-00465 (door-specific)

BEGIN TRANSACTION;

-- ─── FINLAND ───────────────────────────────────────────────────────────────
-- REF-00424: Finland Decree 241/2017 — parent statute (F1)
UPDATE evidence_sources SET
    pub_title = 'Government Decree on Accessibility of Buildings (241/2017) — Asetus rakennuksen esteettömyydestä',
    pub_year = 2017,
    first_author_last = 'Ministry of the Environment of Finland',
    is_corporate_primary = 1,
    author_display = 'Ympäristöministeriö / Ministry of the Environment, Finland',
    publisher = 'Finlex — Finnish Legal Database (Ministry of Justice)',
    standard_number = 'Government Decree 241/2017 — supersedes Ministry of the Environment 2005 F1 decree (which reversed the 16 April 1997 F1 decision); entered into force early 2018',
    jurisdiction = 'FI',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00459',
    metadata_integrity_detail = 'statutory-batch-25 2026-05-21T16:40:00Z: web-search verified via Non-Discrimination Ombudsman (yhdenvertaisuusvaltuutettu.fi) + Aalto University + ACCORD Project EU + Edilex (data/rakentamismaaraykset/f1e.pdf) + AccessibleEU European Commission. Forms part of Finland''s implementation of the UN Convention on the Rights of Persons with Disabilities (ratified by Finland 2016). Decree clarifies accessibility requirements for land use, building sites, and construction. Replaces the 2005 F1 decree and the 16 April 1997 F1 decision. Detailed requirements for dimensions, access routes, sanitary facilities, level differences, assembly/accommodation facilities. Owner: 2-row pair with REF-00459 (door-specific citation of same statute).',
    url = 'https://www.finlex.fi/fi/laki/alkup/2017/20170241',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+ymparisto-finlex',
    last_verified_at = '2026-05-21T16:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T16:40:00Z statutory-batch-25] web-search verified',
    updated_at = '2026-05-21T16:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00424';

-- REF-00459: Finland Decree 241/2017 — door-specific citation
UPDATE evidence_sources SET
    pub_title = 'Government Decree on Accessibility of Buildings (241/2017) — door provisions (Sections 7, 9 — door widths and operating-force limits)',
    pub_year = 2017,
    first_author_last = 'Ministry of the Environment of Finland',
    is_corporate_primary = 1,
    author_display = 'Ympäristöministeriö / Ministry of the Environment, Finland',
    publisher = 'Finlex — Finnish Legal Database (Ministry of Justice)',
    standard_number = 'Government Decree 241/2017, door provisions',
    jurisdiction = 'FI',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00424',
    metadata_integrity_detail = 'statutory-batch-25 2026-05-21T16:40:00Z: web-search verified. Same parent statute as REF-00424 — this row appears to be a citation of the door-specific sections (door clear width, operating-force, threshold-height limits) within Decree 241/2017. Owner: 2-row pair with REF-00424; consider consolidating.',
    url = 'https://www.finlex.fi/fi/laki/alkup/2017/20170241',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+ymparisto-finlex',
    last_verified_at = '2026-05-21T16:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T16:40:00Z statutory-batch-25] web-search verified',
    updated_at = '2026-05-21T16:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00459';

-- ─── ITALY ─────────────────────────────────────────────────────────────────
-- REF-00364: Italy DM 236/89 — parent statute
UPDATE evidence_sources SET
    pub_title = 'Decreto Ministeriale 14 giugno 1989, n. 236 — Prescrizioni tecniche necessarie a garantire l''accessibilità, l''adattabilità e la visitabilità degli edifici privati e di edilizia residenziale pubblica sovvenzionata e agevolata',
    pub_year = 1989,
    first_author_last = 'Ministero dei Lavori Pubblici',
    is_corporate_primary = 1,
    author_display = 'Ministero dei Lavori Pubblici (now Ministero delle Infrastrutture e dei Trasporti — MIT), Repubblica Italiana',
    publisher = 'Gazzetta Ufficiale della Repubblica Italiana',
    standard_number = 'DM 14 giugno 1989, n. 236 (attuazione della Legge 9 gennaio 1989, n. 13); estended to public buildings by DPR 503/96',
    jurisdiction = 'IT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00460',
    metadata_integrity_detail = 'statutory-batch-25 2026-05-21T16:40:00Z: web-search verified via Portale FVG Accessibile + montascaleamico.it + contactsrl.it + konemotus.it + unitel.it. Implementing decree for Legge 13/1989. Defines three quality levels: accessibilità (accessibility — highest), visitabilità (visitability), adattabilità (adaptability). Article 3 requires: ≥5% of subsidized residential units must be fully accessible (min 1 per development); accessibility required in social-function spaces (schools, hospitals, theatres, sports venues); applies to private buildings + subsidized/assisted public residential housing. Owner: 2-row pair with REF-00460.',
    url = 'https://www.gazzettaufficiale.it/eli/id/1989/06/23/089A2772/sg',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+gazzetta-ufficiale',
    last_verified_at = '2026-05-21T16:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T16:40:00Z statutory-batch-25] web-search verified',
    updated_at = '2026-05-21T16:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00364';

-- REF-00460: Italy DM 236/89 — door-specific
UPDATE evidence_sources SET
    pub_title = 'DM 236/89 — porte accessibili (Allegato A, art. 8 — accessible doors: clear width, opening force, threshold heights)',
    pub_year = 1989,
    first_author_last = 'Ministero dei Lavori Pubblici',
    is_corporate_primary = 1,
    author_display = 'Ministero dei Lavori Pubblici (now MIT), Repubblica Italiana',
    publisher = 'Gazzetta Ufficiale della Repubblica Italiana',
    standard_number = 'DM 14 giugno 1989, n. 236 — Allegato A (door specifications)',
    jurisdiction = 'IT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00364',
    metadata_integrity_detail = 'statutory-batch-25 2026-05-21T16:40:00Z: web-search verified. Same parent statute as REF-00364 — door-specific citation of Allegato A and Article 8 within DM 236/89. Owner: 2-row pair with REF-00364.',
    url = 'https://www.gazzettaufficiale.it/eli/id/1989/06/23/089A2772/sg',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+gazzetta-ufficiale',
    last_verified_at = '2026-05-21T16:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T16:40:00Z statutory-batch-25] web-search verified',
    updated_at = '2026-05-21T16:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00460';

-- ─── PORTUGAL ──────────────────────────────────────────────────────────────
-- REF-00365: Portugal DL 163/2006 — parent statute
UPDATE evidence_sources SET
    pub_title = 'Decreto-Lei n.º 163/2006, de 8 de agosto — Regime da acessibilidade aos edifícios e estabelecimentos que recebem público, via pública e edifícios habitacionais',
    pub_year = 2006,
    first_author_last = 'Presidência do Conselho de Ministros',
    is_corporate_primary = 1,
    author_display = 'Governo de Portugal — Presidência do Conselho de Ministros (Republic of Portugal)',
    publisher = 'Diário da República — Imprensa Nacional-Casa da Moeda',
    standard_number = 'Decreto-Lei 163/2006 (revogou DL 123/97 de 22 maio); alterado por DL 136/2014 (9 setembro) e DL 125/2017 (4 outubro); prazo adaptação 10 anos terminou 8 fev 2017',
    jurisdiction = 'PT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00465',
    metadata_integrity_detail = 'statutory-batch-25 2026-05-21T16:40:00Z: web-search verified via dre.tretas.org + Academia.edu + Scribd + APD-Sintra + ac-arquitetos.com + acessibilidade-portugal blog. First Portuguese statute to extend accessibility norms to residential housing (previously only public buildings under DL 123/97). Includes ramps (max gradient, min width, rest landings), stairs (step dimensions, mandatory handrails), and lifts (cabin dimensions, control heights). Municipalities (Câmaras Municipais) authorized to refuse licensing of non-compliant new construction, reconstruction, or alteration. Owner: 2-row pair with REF-00465.',
    url = 'https://diariodarepublica.pt/dr/detalhe/decreto-lei/163-2006-540797',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+dre-portugal',
    last_verified_at = '2026-05-21T16:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T16:40:00Z statutory-batch-25] web-search verified',
    updated_at = '2026-05-21T16:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00365';

-- REF-00465: Portugal DL 163/2006 — door-specific
UPDATE evidence_sources SET
    pub_title = 'Decreto-Lei 163/2006 — portas acessíveis (Anexo — sections on door clear width, opening force, threshold height)',
    pub_year = 2006,
    first_author_last = 'Presidência do Conselho de Ministros',
    is_corporate_primary = 1,
    author_display = 'Governo de Portugal — Presidência do Conselho de Ministros (Republic of Portugal)',
    publisher = 'Diário da República — Imprensa Nacional-Casa da Moeda',
    standard_number = 'DL 163/2006, Anexo — door specifications',
    jurisdiction = 'PT',
    metadata_quality = 'COMPLETE-STATUTORY',
    verification_status = 'VERIFIED',
    metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00365',
    metadata_integrity_detail = 'statutory-batch-25 2026-05-21T16:40:00Z: web-search verified. Same parent statute as REF-00365 — door-specific citation of Anexo (annex) sections within DL 163/2006. Owner: 2-row pair with REF-00365.',
    url = 'https://diariodarepublica.pt/dr/detalhe/decreto-lei/163-2006-540797',
    url_accessed = '2026-05-21',
    verified_by_tool = 'web-search-multi+dre-portugal',
    last_verified_at = '2026-05-21T16:40:00Z',
    verification_note = COALESCE(verification_note,'') || ' | [PROBE 2026-05-21T16:40:00Z statutory-batch-25] web-search verified',
    updated_at = '2026-05-21T16:40:00Z',
    updated_by_session = 'session_2026-05-20-ato-rehab',
    verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1
WHERE ref_id = 'REF-00465';

-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)
COMMIT;
