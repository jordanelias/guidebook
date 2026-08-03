#!/usr/bin/env python3
"""Generate multi-source recovery follow-up migration.

4 ATO no-ID rows confirmed canonical via OpenAlex + independent Crossref verification:
  - REF-00728 (Keall 2021): canonical DOI 10.1016/s2468-2667(21)00135-3 (Lancet Public Health, MHIPI)
  - REF-00730 (Harper 2022): canonical DOI 10.1101/2022.03.25.22271716 (bioRxiv preprint)
  - REF-00260 (Szanton 2019): canonical DOI 10.1001/jamainternmed.2018.6026 (JAMA Int Med, CAPABLE)
  - REF-00731 (Szanton 2019 displaced): same canonical DOI as REF-00260 — flag as potential-duplicate.
"""
import json

c = json.load(open('/tmp/multi_source_canonical.json'))
TS = '2026-05-21T03:00:00Z'
SESSION = 'session_2026-05-20-ato-rehab'


def q(v):
    if v is None or v == '':
        return 'NULL'
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


def split_pages(c):
    pg = c.get('page')
    if pg and '-' in pg:
        a, b = pg.split('-', 1)
        return a.strip(), b.strip()
    return pg, None


def authors_display(authors_list):
    parts = []
    for a in authors_list[:8]:
        last, given = a[0], a[1]
        if not last:
            continue
        if given:
            initial = given[0] + '.' if given else ''
            parts.append(f"{last}, {initial}")
        else:
            parts.append(last)
    return '; '.join(parts)


def render_upgrade(ref, canon, displaced_from=None, note=''):
    ps, pe = split_pages(canon)
    ad = authors_display(canon['authors'])
    note_full = f"multi-source-recovery {TS}: OpenAlex + Crossref independent confirmation of canonical DOI {canon['doi']}. " + note
    out = []
    out.append(f"-- {ref}: multi-source confirmed canonical upgrade")
    out.append(f"UPDATE evidence_sources SET")
    out.append(f"  doi = {q(canon['doi'])},")
    out.append(f"  pub_title = COALESCE(NULLIF(pub_title,''), {q(canon['title'])}),")
    out.append(f"  pub_year = COALESCE(pub_year, {q(canon['year'])}),")
    out.append(f"  journal_name = COALESCE(NULLIF(journal_name,''), {q(canon['journal'])}),")
    out.append(f"  first_author_last = COALESCE(NULLIF(first_author_last,''), {q(canon['authors'][0][0] if canon['authors'] else '')}),")
    out.append(f"  first_author_first = COALESCE(NULLIF(first_author_first,''), {q(canon['authors'][0][1] if canon['authors'] else '')}),")
    out.append(f"  author_display = COALESCE(NULLIF(author_display,''), {q(ad)}),")
    out.append(f"  author_count = COALESCE(author_count, {len([a for a in canon['authors'] if a[0]])}),")
    out.append(f"  author_count_is_complete = COALESCE(author_count_is_complete, 1),")
    out.append(f"  volume = COALESCE(NULLIF(volume,''), {q(canon.get('volume'))}),")
    out.append(f"  issue = COALESCE(NULLIF(issue,''), {q(canon.get('issue'))}),")
    out.append(f"  pages_start = COALESCE(NULLIF(pages_start,''), {q(ps)}),")
    out.append(f"  pages_end = COALESCE(NULLIF(pages_end,''), {q(pe)}),")
    out.append(f"  publisher = COALESCE(NULLIF(publisher,''), {q(canon.get('publisher'))}),")
    out.append(f"  issn = COALESCE(NULLIF(issn,''), {q(canon.get('issn'))}),")
    out.append(f"  metadata_quality = 'COMPLETE',")
    out.append(f"  verification_status = 'VERIFIED',")
    out.append(f"  doi_resolution_outcome = 'RESOLVED',")
    out.append(f"  metadata_integrity_status = 'OK',")
    out.append(f"  metadata_integrity_detail = COALESCE(metadata_integrity_detail,'') || {q(' | ' + note_full)},")
    out.append(f"  verification_note = COALESCE(verification_note,'') || {q(' | [PROBE ' + TS + ' multi-source-recovery] CONFIRMED canonical via OpenAlex + Crossref')},")
    out.append(f"  updated_at = '{TS}',")
    out.append(f"  updated_by_session = '{SESSION}',")
    out.append(f"  verification_attempt_count = COALESCE(verification_attempt_count, 0) + 1")
    out.append(f"WHERE ref_id = '{ref}';")
    out.append("")
    return '\n'.join(out)


out = []
P = out.append

P("-- data_20260521030000_multi_source_recovery.sql")
P("--")
P("-- Multi-source ATO recovery follow-up. OpenAlex + Semantic Scholar probe surfaced")
P("-- 6 single-source candidates from 55 ATO×no-ID rows. 4 of 6 verified canonical via")
P("-- independent Crossref query (REF-00260 Szanton, REF-00728 Keall, REF-00730 Harper,")
P("-- REF-00731 Szanton-displaced); 2 were wrong-author-year-collision and stay in queue.")
P("--")
P("-- REF-00260 and REF-00731 share canonical DOI (both Szanton 2019 JAMA Internal")
P("-- Medicine CAPABLE RCT) — REF-00731 marked as POTENTIAL-DUPLICATE-OF-REF-00260 for")
P("-- owner merge decision.")
P("--")
P("BEGIN TRANSACTION;")
P("")

# Apply the 3 distinct DOIs
P(render_upgrade('REF-00728', c['REF-00728_REF-00069_keall'],
                 displaced_from='REF-00069',
                 note='REF-00728 carries Keall MHIPI metadata displaced from REF-00069 on 2026-05-20; now identified as the actual Keall 2021 Lancet Public Health MHIPI study.'))

P(render_upgrade('REF-00730', c['REF-00730_REF-00527_harper'],
                 displaced_from='REF-00527',
                 note='REF-00730 carries Harper metadata displaced from REF-00527 on 2026-05-20; now identified as Harper 2022 bioRxiv preprint on stairway visual contrast.'))

P(render_upgrade('REF-00260', c['REF-00260_REF-00731_szanton'],
                 note='Original CAPABLE costing reference; resolves to Szanton 2019 JAMA Internal Medicine CAPABLE RCT main outcomes paper.'))

# REF-00731 same canonical DOI as REF-00260 — flag duplicate
P("-- REF-00731: same canonical DOI as REF-00260 (both Szanton 2019 JAMA Int Med CAPABLE);")
P("-- upgrade to canonical AND flag potential duplicate for owner merge decision")
P(render_upgrade('REF-00731', c['REF-00260_REF-00731_szanton'],
                 displaced_from='REF-00150',
                 note='REF-00731 carries Szanton metadata displaced from REF-00150 on 2026-05-20; now identified as the same Szanton 2019 paper as REF-00260. POTENTIAL DUPLICATE OF REF-00260 — owner: decide whether to merge.'))

# Override REF-00731's integrity status to flag the duplicate
P("-- REF-00731: override metadata_integrity_status to flag duplicate-of-REF-00260")
P("UPDATE evidence_sources SET")
P(f"  metadata_integrity_status = 'POTENTIAL-DUPLICATE-OF-REF-00260',")
P(f"  metadata_integrity_detail = metadata_integrity_detail || {q(' | DUPLICATE FLAG: REF-00731 and REF-00260 both resolve to canonical DOI 10.1001/jamainternmed.2018.6026 (Szanton 2019 JAMA Int Med CAPABLE). Owner: merge or remove.')},")
P(f"  updated_at = '{TS}',")
P(f"  updated_by_session = '{SESSION}'")
P("WHERE ref_id = 'REF-00731';")
P("")

P("-- (data_migrations tracking row inserted by scripts/migrate_db.py runner)")
P("COMMIT;")

print('\n'.join(out))
