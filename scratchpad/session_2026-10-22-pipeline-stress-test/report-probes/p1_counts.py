import sqlite3, sys
db = sys.argv[1] if len(sys.argv) > 1 else '/home/user/guidebook/data/guidebook.db'
con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
q = lambda s, *a: con.execute(s, a).fetchall()
print('user_version', q('PRAGMA user_version'))
for t in ['base_parameters','terms','slugs','evidence_sources','source_value_extractions','specifications','source_scans',
          'search_executions','term_aliases','access_needs','access_need_icf','identity_icf_map','base_taxonomy_identity','base_icf',
          'base_taxonomy_medical','identity_medical_map','icf_medical_map','evidence_population_match','extraction_relations',
          'convergence_assessment','determination_gates','weighting_profile','external_root_registry','connections','conflicts',
          'citation_mining','term_observations','lang_jur_map','parameter_declinations','gaps','adversarial_passes','extraction_follow_ups']:
    try: print(t, q(f'select count(*) from "{t}"')[0][0])
    except Exception as e: print(t, 'ERR', e)
print('spec live', q('select count(*) from specifications where retired_at is null'))
print('extr by param', q('select parameter_id, count(*) from source_value_extractions group by 1'))
print('extr identity', q('select identity_code, icf_code is null, needs_code, count(*) from source_value_extractions group by 1,2,3'))
print('scan ledger', q('select status, count(*) from v_scan_ledger group by 1'))
print('relations', q("select relation, to_extraction_id is not null, count(*) from extraction_relations group by 1,2"))
print('cross-param edges', q("select count(*) from extraction_relations r join source_value_extractions a on a.extraction_id=r.from_extraction_id join source_value_extractions b on b.extraction_id=r.to_extraction_id where a.parameter_id<>b.parameter_id"))
print('conv status', q('select status, count(*) from convergence_assessment group by 1'))
print('direction', q('select parameter_id, term_id, accessibility_direction, status from base_parameters'))
print('lang_jur distinct jur', q('select count(distinct jurisdiction) from lang_jur_map'))
print('lang_jur cols', [r[1] for r in q('PRAGMA table_info(lang_jur_map)')])
print('search lang labels', q('select language, count(*) from search_executions group by 1'))
print('search jur distinct', q('select count(distinct jurisdiction) from search_executions'))
print('search param non-null', q('select count(*) from search_executions where parameter_id is not null'))
print('search slugs', q('select slug, count(*) from search_executions group by 1'))
print('terms_used', q('select count(*) from search_executions where terms_used is not null'))
print('engine top', q('select count(distinct engine), sum(engine="web") from search_executions'))
print('ev lang', q('select count(*), sum(language is null), sum(lang_detected is not null), sum(lang_detection_method is not null) from evidence_sources'))
print('mining status by tier', q('select citation_mining_status, tier, count(*) from evidence_sources group by 1,2'))
print('code currency T4-6', q('select tier, code_currency_status, count(*) from evidence_sources where tier>=4 group by 1,2'))
print('claimed_unit', q('select claimed_unit, count(*) from source_value_extractions group by 1 order by 2 desc'))
print('ext status', q('select extraction_status, extraction_method, count(*) from source_value_extractions group by 1,2'))
print('comparator null by role', q('select figure_role, claim_type, sum(comparator is null), count(*) from source_value_extractions group by 1,2'))
print('root_type', q('select root_type, count(*) from source_value_extractions group by 1'))
print('setting filled', q('select count(*) from source_value_extractions where setting is not null and trim(setting)<>""'))
