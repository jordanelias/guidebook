#!/usr/bin/env python3
"""Generate the full-DB metadata corrections migration."""
import json

canonical = json.load(open('/tmp/canonical_corrections.json'))
TS = '2026-05-21T00:00:00Z'
SESSION = 'session_2026-05-20-ato-rehab'


def q(v):
    if v is None or v == '':
        return 'NULL'
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


def authors_display(authors_list):
    parts = []
    for a in authors_list[:8]:
        last, given = a[0], a[1]
        if not last:
            continue
        if given:
            initial = given[0] + '.'
            parts.append(f"{last}, {initial}")
        else:
            parts.append(last)
    return '; '.join(parts)


def split_pages(c):
    """Return (ps, pe) from canonical record."""
    if 'pages_start' in c:
        return c.get('pages_start'), c.get('pages_end')
    pg = c.get('page')
    if pg and '-' in pg:
        a, b = pg.split('-', 1)
        return a.strip(), b.strip()
    return pg, None


out = []
P = out.append

P("-- data_20260521000000_full_db_metadata_corrections.sql")
P("--")
P("-- Comprehensive metadata corrections from full-DB verification audit.")
P("-- Audit re-fetched canonical metadata for all 238 evidence_sources rows with any")
P("-- identifier; 12 rows (5%) showed WRONG-ATTRIBUTION or IDENTIFIER-DISAGREE.")
P("--")
P("-- Action types:")
P("--   FIELD-FIX (3 rows): REF-00028, REF-00262, REF-00284 — same paper; fix fields")
P("--   DISPLACE (5 rows):  REF-00150/00233/00240/00302/00571 — wrong-attribution;")
P("--                       overwrite with canonical, preserve displaced as 731-735")
P("--   CLEAR-DOI (2 rows): REF-00176, REF-00478 — DOI was wrong; book metadata real")
P("--   CLEAR-PMID (1 row): REF-00096 — PMID was wrong; DOI is correct")
P("--   OWNER-QUEUE (1 row): REF-00363 — Gitlin DOI/PMID disagree, owner decides")
P("--")
P("BEGIN TRANSACTION;")
P("")


# ============ FIELD-FIX rows ============
def field_fix(ref, c, note):
    ps, pe = split_pages(c)
    disp = authors_display(c['authors'])
    detail = f"field-fix {TS}: same paper ({c['first_author_last']} {c['year']} {c['journal']}). {note}"
    P(f"-- {ref}: FIELD-FIX")
    P(f"UPDATE evidence_sources SET")
    P(f"  pub_title = {q(c['title'])},")
    P(f"  pub_year = {q(c['year'])},")
    P(f"  journal_name = {q(c['journal'])},")
    P(f"  first_author_last = {q(c['first_author_last'])},")
    P(f"  first_author_first = {q(c['first_author_first'])},")
    P(f"  author_display = {q(disp)},")
    P(f"  author_count = {len([a for a in c['authors'] if a[0]])},")
    P(f"  author_count_is_complete = 1,")
    P(f"  volume = {q(c.get('volume'))},")
    P(f"  issue = {q(c.get('issue'))},")
    P(f"  pages_start = {q(ps)},")
    P(f"  pages_end = {q(pe)},")
    P(f"  publisher = {q(c.get('publisher'))},")
    P(f"  issn = {q(c.get('issn'))},")
    P(f"  metadata_quality = 'COMPLETE',")
    P(f"  metadata_integrity_status = 'OK',")
    P(f"  metadata_integrity_detail = {q(detail)},")
    P(f"  verification_note = COALESCE(verification_note,'') || {q(' | [PROBE ' + TS + ' full-DB-audit] FIELD-FIX from canonical')},")
    P(f"  updated_at = '{TS}', updated_by_session = '{SESSION}',")
    P(f"  verification_attempt_count = COALESCE(verification_attempt_count,0)+1")
    P(f"WHERE ref_id = '{ref}';")
    P("")


field_fix('REF-00028', canonical['REF-00028'],
          "Stored had paraphrased pub_title and wrong year 2023; canonical is Levine 2021.")
field_fix('REF-00262', canonical['REF-00262'],
          "Stored first_author_last was 'Carr K' (form drift); title shortened.")
field_fix('REF-00284', canonical['REF-00284'],
          "Stored author 'Cudjoe T' form drift; title-case variation. Same paper.")


# ============ CLEAR-PMID: REF-00096 ============
P("-- REF-00096: CLEAR-PMID (DOI correct -> van Oel 2020; PMID 36567605 was wrong-attached)")
P(f"UPDATE evidence_sources SET")
P(f"  pmid = NULL,")
P(f"  metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || {q(' | full-DB-audit ' + TS + ': PMID 36567605 cleared - it resolves to Faerden 2023 different paper. DOI alone is correct identifier.')},")
P(f"  verification_note = COALESCE(verification_note,'') || {q(' | [PROBE ' + TS + ' full-DB-audit] CLEAR-PMID 36567605 (wrong-attached)')},")
P(f"  updated_at = '{TS}', updated_by_session = '{SESSION}',")
P(f"  verification_attempt_count = COALESCE(verification_attempt_count,0)+1")
P(f"WHERE ref_id = 'REF-00096';")
P("")


# ============ CLEAR-DOI: REF-00176, REF-00478 ============
def clear_doi(ref, detail):
    P(f"-- {ref}: CLEAR-DOI")
    P(f"UPDATE evidence_sources SET")
    P(f"  doi = NULL,")
    P(f"  verification_status = NULL,")
    P(f"  doi_resolution_outcome = NULL,")
    P(f"  metadata_integrity_status = 'WRONG-DOI-CLEARED',")
    P(f"  metadata_integrity_detail = {q(detail)},")
    P(f"  verification_note = COALESCE(verification_note,'') || {q(' | [PROBE ' + TS + ' full-DB-audit] CLEAR-DOI (wrong-attribution)')},")
    P(f"  updated_at = '{TS}', updated_by_session = '{SESSION}',")
    P(f"  verification_attempt_count = COALESCE(verification_attempt_count,0)+1")
    P(f"WHERE ref_id = '{ref}';")
    P("")


clear_doi('REF-00176',
          f"full-DB-audit {TS}: DOI 10.1126/science.166.3907.856-a CLEARED - it resolves to Weick 1969 book review of Barker in Science. Stored citation IS Barker 1968 'Ecological Psychology' (Stanford UP) - real book predating DOI registration. verification_status reverted from VERIFIED (prior verification was based on wrong identifier).")
clear_doi('REF-00478',
          f"full-DB-audit {TS}: DOI 10.1177/019263658506948224 CLEARED - resolves to Lynch 1985 book review in NASSP Bulletin, not Passini's book. Stored citation IS Passini 1984 'Wayfinding in Architecture' (Van Nostrand Reinhold) - real book predating DOI registration. verification_status reverted from VERIFIED.")


# ============ OWNER-QUEUE: REF-00363 ============
P("-- REF-00363: OWNER-QUEUE (DOI and PMID both Gitlin 2006 but different papers)")
P(f"UPDATE evidence_sources SET")
P(f"  metadata_integrity_status = 'IDENTIFIER-DISAGREE-OWNER-DECIDE',")
P(f"  metadata_integrity_detail = {q(f'full-DB-audit {TS}: DOI 10.1111/j.1532-5415.2006.00703.x -> Gitlin 2006 Multicomponent Home Intervention (JAGS); PMID 17050754 -> Gitlin 2006 Enhancing quality of life of families who use adult day services (different paper). Owner must decide intent; clear the other identifier.')},")
P(f"  verification_note = COALESCE(verification_note,'') || {q(' | [PROBE ' + TS + ' full-DB-audit] OWNER-DECIDE: DOI/PMID resolve to different Gitlin 2006 papers')},")
P(f"  updated_at = '{TS}', updated_by_session = '{SESSION}',")
P(f"  verification_attempt_count = COALESCE(verification_attempt_count,0)+1")
P(f"WHERE ref_id = 'REF-00363';")
P("")


# ============ DISPLACE: 5 cases ============
displacements = [
    ('REF-00150', {
        'first_author_last': 'Szanton', 'first_author_first': 'S.',
        'pub_year': 2019, 'pub_title': '$2,825/participant home modification',
        'source_type': 'report', 'tier': 3, 'evidence_type': 'clinical', 'jurisdiction': 'US',
    }, 'REF-00731', canonical['REF-00150']),
    ('REF-00233', {
        'first_author_last': 'Strassheim', 'first_author_first': None,
        'pub_year': 2018, 'pub_title': 'OI in ME/CFS',
        'source_type': 'report', 'tier': 3, 'evidence_type': 'clinical', 'jurisdiction': 'INT',
    }, 'REF-00732', canonical['REF-00233']),
    ('REF-00240', {
        'first_author_last': 'Ismail', 'first_author_first': None,
        'pub_year': 2023, 'pub_title': 'Fibromyalgia hydrotherapy SR. Tandfonline',
        'source_type': 'report', 'tier': 3, 'evidence_type': 'sr_meta', 'jurisdiction': 'INT',
    }, 'REF-00733', canonical['REF-00240']),
    ('REF-00302', {
        'first_author_last': 'Tibble', 'first_author_first': None,
        'pub_year': 2005, 'pub_title': 'Review of extra costs facing disabled people',
        'source_type': 'report', 'tier': 5, 'evidence_type': 'co1', 'jurisdiction': 'UK',
    }, 'REF-00734', canonical['REF-00302']),
    ('REF-00571', {
        'first_author_last': 'Devos', 'first_author_first': None,
        'pub_year': 2019, 'pub_title': 'Dementia soundscape. PMC6950055',
        'source_type': 'report', 'tier': 3, 'evidence_type': 'clinical', 'jurisdiction': 'INT',
    }, 'REF-00735', canonical['REF-00571']),
]

for old_ref, disp, new_ref, c in displacements:
    P(f"-- DISPLACE: {old_ref} -> {new_ref} (identifier resolves to {c['first_author_last']} {c['year']})")
    P(f"-- Step A: insert displaced metadata")
    disp_first = disp.get('first_author_first') or ''
    disp_display = f"{disp['first_author_last']}, {disp_first}" if disp_first else disp['first_author_last']
    detail_displaced = (
        f"Displaced from {old_ref} by full-DB-audit {TS}. {old_ref} carried identifier(s) "
        f"that resolved to {c['first_author_last']} {c['year']} (different paper). "
        f"Identifier(s) stayed with {old_ref}; this row preserves original {disp['first_author_last']} "
        f"metadata. Slug links not migrated; owner review required."
    )
    P(f"INSERT INTO evidence_sources (")
    P(f"  ref_id, source_type, author_count, author_count_is_complete,")
    P(f"  first_author_last, first_author_first, is_corporate_primary, author_display,")
    P(f"  pub_year, pub_title, lang_detected, lang_detection_method, translation_method,")
    P(f"  tier, evidence_type, jurisdiction,")
    P(f"  metadata_quality, verification_status, verification_attempt_count,")
    P(f"  metadata_integrity_status, metadata_integrity_detail,")
    P(f"  verification_note,")
    P(f"  created_at, created_by_session, updated_at, updated_by_session")
    P(f") VALUES (")
    P(f"  {q(new_ref)}, {q(disp['source_type'])}, 1, 0,")
    P(f"  {q(disp['first_author_last'])}, {q(disp_first)}, 0, {q(disp_display)},")
    P(f"  {q(disp['pub_year'])}, {q(disp['pub_title'])}, 'en', 'langdetect', 'native_english',")
    P(f"  {q(disp['tier'])}, {q(disp['evidence_type'])}, {q(disp['jurisdiction'])},")
    P(f"  'AUTHOR-TITLE-ONLY', NULL, 0,")
    P(f"  {q('DISPLACED-FROM-' + old_ref)},")
    P(f"  {q(detail_displaced)},")
    P(f"  {q(f'[{TS} {SESSION}] Created via full-DB-audit displacement from {old_ref}.')},")
    P(f"  '{TS}', '{SESSION}', '{TS}', '{SESSION}'")
    P(f");")
    P("")

    P(f"-- Step B: move evidence_source_authors {old_ref} -> {new_ref}")
    P(f"UPDATE evidence_source_authors SET ref_id = '{new_ref}',")
    P(f"  created_by_session = COALESCE(created_by_session,'') || ' | moved {TS} from {old_ref} (full-DB-audit displacement)'")
    P(f"WHERE ref_id = '{old_ref}';")
    P("")

    P(f"-- Step C: overwrite {old_ref} with canonical {c['first_author_last']} metadata")
    ps, pe = split_pages(c)
    disp_canon = authors_display(c['authors'])
    detail_canonical = (
        f"wrong-attribution-corrected {TS} by full-DB-audit. Canonical metadata for "
        f"identifier(s); displaced {disp['first_author_last']} metadata preserved at {new_ref}. "
        f"jurisdiction reset to NULL (prior {disp['jurisdiction']} belonged to displaced paper)."
    )
    P(f"UPDATE evidence_sources SET")
    P(f"  first_author_last = {q(c['first_author_last'])},")
    P(f"  first_author_first = {q(c['first_author_first'])},")
    P(f"  author_display = {q(disp_canon)},")
    P(f"  author_count = {len([a for a in c['authors'] if a[0]])},")
    P(f"  author_count_is_complete = 1,")
    P(f"  is_corporate_primary = 0,")
    P(f"  pub_year = {q(c['year'])},")
    P(f"  pub_title = {q(c['title'])},")
    P(f"  journal_name = {q(c['journal'])},")
    P(f"  volume = {q(c.get('volume'))},")
    P(f"  issue = {q(c.get('issue'))},")
    P(f"  pages_start = {q(ps)},")
    P(f"  pages_end = {q(pe)},")
    P(f"  publisher = {q(c.get('publisher'))},")
    P(f"  issn = {q(c.get('issn'))},")
    P(f"  jurisdiction = NULL,")
    P(f"  metadata_quality = 'COMPLETE',")
    P(f"  verification_status = 'VERIFIED',")
    P(f"  doi_resolution_outcome = 'RESOLVED',")
    P(f"  metadata_integrity_status = 'OK',")
    P(f"  metadata_integrity_detail = {q(detail_canonical)},")
    P(f"  verification_note = COALESCE(verification_note,'') || {q(' | [PROBE ' + TS + ' full-DB-audit] WRONG-ATTRIBUTION corrected; displaced -> ' + new_ref)},")
    P(f"  updated_at = '{TS}', updated_by_session = '{SESSION}',")
    P(f"  verification_attempt_count = COALESCE(verification_attempt_count,0)+1")
    P(f"WHERE ref_id = '{old_ref}';")
    P("")

    P(f"-- Step D: insert canonical author rows for {old_ref}")
    for i, (last, given) in enumerate(c['authors'][:8], 1):
        if not last:
            continue
        P(f"INSERT INTO evidence_source_authors (ref_id, position, last_name, first_name, suffix, orcid, is_corporate, corporate_name, corporate_name_en, role, created_at, created_by_session) VALUES ('{old_ref}', {i}, {q(last)}, {q(given)}, NULL, NULL, 0, NULL, NULL, 'author', '{TS}', '{SESSION}');")
    P("")


# ============ v1_legacy sync ============
P("-- v1_legacy sync for new displaced rows")
for old_ref, disp, new_ref, _ in displacements:
    disp_first = disp.get('first_author_first') or ''
    authors_v1 = f"{disp['first_author_last']}, {disp_first}" if disp_first else disp['first_author_last']
    slug = (disp['first_author_last'] + '_' + str(disp['pub_year']) + '_' + disp['pub_title'][:30]).lower().replace(' ', '_')
    P(f"INSERT INTO evidence_sources_v1_legacy (")
    P(f"  ref_id, authors, year, title, doi, doi_less_key, pmid,")
    P(f"  tier, evidence_type, jurisdiction, metadata_quality, verification_status,")
    P(f"  notes, created_at, created_by_session, updated_at, updated_by_session")
    P(f") VALUES (")
    P(f"  '{new_ref}', {q(authors_v1)}, '{disp['pub_year']}',")
    P(f"  {q(disp['pub_title'])}, NULL, {q(slug)}, NULL,")
    P(f"  {disp['tier']}, {q(disp['evidence_type'])}, {q(disp['jurisdiction'])}, 'AUTHOR-TITLE-ONLY', NULL,")
    P(f"  {q(f'Displaced from {old_ref} by full-DB-audit 2026-05-21')},")
    P(f"  '{TS}', '{SESSION}', '{TS}', '{SESSION}'")
    P(f");")

P("")
P("-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)")
P("COMMIT;")

print('\n'.join(out))
