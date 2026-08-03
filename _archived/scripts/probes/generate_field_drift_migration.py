#!/usr/bin/env python3
"""Generate FIELD-DRIFT bulk population migration."""
import json
import sqlite3

audit = json.load(open('/tmp/full_audit.json'))
TS = '2026-05-21T00:30:00Z'
SESSION = 'session_2026-05-20-ato-rehab'


def q(v):
    if v is None or v == '':
        return 'NULL'
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


def split_pages(c):
    if 'pages_start' in c:
        return c.get('pages_start'), c.get('pages_end')
    pg = c.get('page')
    if pg and '-' in pg:
        a, b = pg.split('-', 1)
        return a.strip(), b.strip()
    return pg, None


# Open DB read-only for cross-checking stored values
conn = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
conn.row_factory = sqlite3.Row


def get_stored(ref_id):
    return conn.execute('SELECT * FROM evidence_sources WHERE ref_id=?', (ref_id,)).fetchone()


def is_empty(v):
    return v in (None, '', 0)


out = []
P = out.append

P("-- data_20260521003000_field_drift_bulk_population.sql")
P("--")
P("-- Bulk-populates empty fields on 144 FIELD-DRIFT and FIELD-DRIFT-WITH-MISMATCH")
P("-- rows from the full-DB verification audit. Per rule 1B: only writes fields where")
P("-- stored value is NULL/empty; never overwrites existing values.")
P("--")
P("-- Also handles 3 single-case corrections discovered during FDM triage:")
P("--   REF-00090: CLEAR-PMID (PMID resolves to virology paper, not the trauma-informed-design")
P("--              paper the stored note describes; likely duplicate-of-REF-00527)")
P("--   REF-00131: OWNER-QUEUE (DOI resolves to AUT posted-content 2025 work-counselling")
P("--              scoping review; stored is Holohan 2022 design scoping review — different topic)")
P("--   REF-00485: CLEAR-DOI (DOI resolves to Dillman-Hasso 2020; stored is Kaplan 1989")
P("--              'Experience of Nature' book predating DOI registration)")
P("--")
P("-- Source: scripts/audit/full_db_metadata_verification.py output /tmp/full_audit.json")
P("BEGIN TRANSACTION;")
P("")

# ============ Bulk FIELD-DRIFT population ============
fd_rows = [o for o in audit if o['verdict'] in ('FIELD-DRIFT', 'FIELD-DRIFT-WITH-MISMATCH')]
fd_rows = [o for o in fd_rows if o['ref_id'] not in ('REF-00090', 'REF-00131', 'REF-00485')]

P(f"-- Bulk FIELD-DRIFT: {len(fd_rows)} rows")
P("")

writes_count = 0
skipped_count = 0
for o in fd_rows:
    ref = o['ref_id']
    c = o['canonical']
    if not c or not isinstance(c, dict) or 'cr' in c:  # skip IDENTIFIER-DISAGREE (have nested cr/pm)
        skipped_count += 1
        continue
    stored = get_stored(ref)
    if stored is None:
        skipped_count += 1
        continue

    writes = {}
    if is_empty(stored['journal_name']) and c.get('journal'):
        writes['journal_name'] = c['journal']
    if is_empty(stored['volume']) and c.get('volume'):
        writes['volume'] = c['volume']
    if is_empty(stored['issue']) and c.get('issue'):
        writes['issue'] = c['issue']
    ps, pe = split_pages(c)
    if is_empty(stored['pages_start']) and ps:
        writes['pages_start'] = ps
    if is_empty(stored['pages_end']) and pe:
        writes['pages_end'] = pe
    if is_empty(stored['publisher']) and c.get('publisher'):
        writes['publisher'] = c['publisher']
    if is_empty(stored['issn']) and c.get('issn'):
        writes['issn'] = c['issn']
    if is_empty(stored['first_author_first']) and c.get('first_author_first'):
        writes['first_author_first'] = c['first_author_first']
    # Year and title NEVER written here — too risky given the patterns we've seen
    # Author surname-form drift left alone too

    if not writes:
        skipped_count += 1
        continue

    sets_sql = []
    for k, v in writes.items():
        sets_sql.append(f"  {k} = COALESCE({k}, {q(v)})")
    P(f"-- {ref} ({o['verdict']}): {len(writes)} field(s)")
    P(f"UPDATE evidence_sources SET")
    P(',\n'.join(sets_sql) + ',')
    P(f"  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || {q(' | bulk-field-drift-population ' + TS + ': filled empty fields from canonical (' + ', '.join(writes.keys()) + ')')},")
    P(f"  updated_at = '{TS}',")
    P(f"  updated_by_session = '{SESSION}'")
    P(f"WHERE ref_id = '{ref}';")
    P("")
    writes_count += 1

P(f"-- Bulk population: {writes_count} rows updated, {skipped_count} skipped (no fields to fill)")
P("")

# ============ REF-00090: CLEAR-PMID + duplicate flag ============
P("-- REF-00090: CLEAR-PMID (wrong PMID 36742289 -> Girsch virology; stored topic note 'TID PMC9658651' references REF-00527's paper)")
P(f"UPDATE evidence_sources SET")
P(f"  pmid = NULL,")
P(f"  metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00527',")
P(f"  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || {q(' | full-DB-audit ' + TS + ': PMID 36742289 cleared (resolves to Girsch 2022 virology paper, not trauma-informed-design). Stored title note references PMC9658651 which is Owen-Crane 2022 trauma-informed-design - same paper as REF-00527. Owner: decide whether to merge.')},")
P(f"  verification_note = COALESCE(verification_note,'') || {q(' | [PROBE ' + TS + ' full-DB-audit] CLEAR-PMID + flag potential duplicate of REF-00527')},")
P(f"  updated_at = '{TS}',")
P(f"  updated_by_session = '{SESSION}',")
P(f"  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1")
P(f"WHERE ref_id = 'REF-00090';")
P("")

# ============ REF-00131: OWNER-QUEUE ============
P("-- REF-00131: OWNER-QUEUE (DOI -> AUT 2025 posted-content work-counselling scoping review; stored Holohan 2022 design scoping review)")
P(f"UPDATE evidence_sources SET")
P(f"  metadata_integrity_status = 'IDENTIFIER-CONTENT-DISAGREE-OWNER-DECIDE',")
P(f"  metadata_integrity_detail = COALESCE(metadata_integrity_detail, '') || {q(' | full-DB-audit ' + TS + ': DOI 10.24135/10292/18859 resolves to AUT Library 2025 posted-content scoping-review protocol on trauma-informed work-oriented counselling (no author listed in Crossref); stored is Holohan 2022 trauma-informed design scoping review. Different topic. Owner: confirm DOI/paper intent, may need replacement DOI.')},")
P(f"  verification_note = COALESCE(verification_note,'') || {q(' | [PROBE ' + TS + ' full-DB-audit] OWNER-DECIDE: identifier vs stored topic disagree')},")
P(f"  updated_at = '{TS}',")
P(f"  updated_by_session = '{SESSION}',")
P(f"  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1")
P(f"WHERE ref_id = 'REF-00131';")
P("")

# ============ REF-00485: CLEAR-DOI (Kaplan book) ============
P("-- REF-00485: CLEAR-DOI (Kaplan & Kaplan 1989 'Experience of Nature' Cambridge UP - book predates DOI registration; attached DOI is wrong)")
P(f"UPDATE evidence_sources SET")
P(f"  doi = NULL,")
P(f"  verification_status = NULL,")
P(f"  doi_resolution_outcome = NULL,")
P(f"  metadata_integrity_status = 'WRONG-DOI-CLEARED',")
P(f"  metadata_integrity_detail = {q('full-DB-audit ' + TS + ': DOI 10.31234/osf.io/w36rg CLEARED - resolves to Dillman-Hasso 2020 (PsyArXiv posted-content), not Kaplan 1989. Stored is Kaplan & Kaplan 1989 The Experience of Nature (Cambridge University Press) - real book predating DOI registration. verification_status reverted from VERIFIED.')},")
P(f"  verification_note = COALESCE(verification_note,'') || {q(' | [PROBE ' + TS + ' full-DB-audit] CLEAR-DOI (wrong-attribution)')},")
P(f"  updated_at = '{TS}',")
P(f"  updated_by_session = '{SESSION}',")
P(f"  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1")
P(f"WHERE ref_id = 'REF-00485';")
P("")

P("-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)")
P("COMMIT;")

print('\n'.join(out))
