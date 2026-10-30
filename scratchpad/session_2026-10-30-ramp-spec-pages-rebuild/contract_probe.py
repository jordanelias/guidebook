#!/usr/bin/env python3
"""Probe the live database against the render contract for parameters 3 and 12.
Read-only. usage: python3 scratchpad/<session>/contract_probe.py [--json]

Every line is one contract element or invariant: what it reads, how many rows it finds, and a
status: POPULATED (data present), EMPTY (reads nothing yet), BLOCKED (cannot be answered from the
database today; the reason is named). The contract document points here by element id; re-run it
rather than quoting a figure from the document (CLAUDE.md rule 7a).
"""
import json, sqlite3, sys
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'scripts/research')

PARAMS = (3, 12)
PIN = ','.join(str(p) for p in PARAMS)
# The owner's scope (2026-10-29/30, HANDOFF section 3). No table holds it until jurisdiction_buckets (T-6b) exists.
SCOPE = ('US UK AU CA DE NO SE ISO EU FR CH NL DK FI BE IE ES IT PT JP SG NZ KR CN').split()

c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
q = lambda sql, *a: c.execute(sql, a).fetchall()
one = lambda sql, *a: c.execute(sql, a).fetchone()[0]
out = []


def row(eid, reads, status, n, note=''):
    out.append(dict(id=eid, reads=reads, status=status, n=n, note=note))


# E0 identity
row('E0', 'terms (TERM-089, TERM-001, TERM-091)', 'POPULATED' if one("select count(*) from terms where term_id in ('TERM-089','TERM-001','TERM-091')") == 3 else 'EMPTY',
    one("select count(*) from terms where term_id in ('TERM-089','TERM-001','TERM-091')"), 'canonical_en and definition; the element page is a term pointer (OR-14), TERM-089 is not a parameter')
# E1 determination
live = one(f"select count(*) from specifications where parameter_id in ({PIN}) and retired_at is null")
row('E1', 'specifications (live rows) for parameters 3 and 12', 'POPULATED' if live else 'BLOCKED', live,
    'no live determination: the engine rows T-2 to T-4 and the first run S-1 are unbuilt; the page may not compute a best-practice value itself')
# E2 master table
rows = q(f"select parameter_id, jurisdiction, count(*) from source_value_extractions where parameter_id in ({PIN}) and claim_type in ('numerical','range') and figure_role='claim' and jurisdiction is not null group by 1,2")
held = {}
for p, j, n in rows:
    held.setdefault(p, {})[j] = n
for p in PARAMS:
    inscope = [j for j in SCOPE if j in held.get(p, {})]
    row(f'E2.p{p}', f'source_value_extractions claim rows with a jurisdiction, parameter {p}', 'POPULATED' if inscope else 'EMPTY', sum(held.get(p, {}).values()),
        f'in-scope jurisdictions with a row: {len(inscope)} of {len(SCOPE)}; held outside the list: {sorted(set(held.get(p, {})) - set(SCOPE))}; in scope with no row: {[j for j in SCOPE if j not in held.get(p, {})]}')
row('E2.scope', 'jurisdiction_buckets (T-6b)', 'BLOCKED', 0, 'no table holds the scope; a list passed to the renderer is a curated list (rule 8); lang_jur_map holds language-jurisdiction pairs, not the buckets')
# E3 detail
row('E3', 'extraction claim_text, loc_*, extraction_status, extraction_method', 'POPULATED',
    one(f"select count(*) from source_value_extractions where parameter_id in ({PIN})"),
    'rows with no claim_text: %d; numerical claim rows with no locator (source_section and every loc_* NULL): %d' % (
        one(f"select count(*) from source_value_extractions where parameter_id in ({PIN}) and (claim_text is null or claim_text='')"),
        one(f"select count(*) from source_value_extractions where parameter_id in ({PIN}) and claim_type='numerical' and source_section is null and loc_section is null and loc_clause is null and loc_paragraph is null")))
# E4 lens
lens = {k: one(f"select count(*) from source_value_extractions where parameter_id in ({PIN}) and {k} is not null") for k in ('identity_code', 'icf_code', 'needs_code', 'medical_code')}
used_id = {r[0] for r in q(f"select distinct identity_code from source_value_extractions where parameter_id in ({PIN}) and identity_code is not null")}
all_id = one("select count(*) from base_taxonomy_identity where status='active'") if 'status' in [x[1] for x in c.execute('pragma table_info(base_taxonomy_identity)')] else one("select count(*) from base_taxonomy_identity")
row('E4', 'lens columns on source_value_extractions; vocabularies base_taxonomy_identity, base_icf, access_needs, base_taxonomy_medical', 'POPULATED', sum(lens.values()),
    f'rows per lens column {lens}; identity codes used {sorted(used_id)} of {all_id} in the vocabulary (the rest are the "no evidence" list, derived, not typed)')
# E5 units
try:
    from assess.assess_cell import notation_family
except Exception:
    try:
        sys.path.insert(0, 'scripts/assess')
        from assess_cell import notation_family
    except Exception:
        notation_family = None
units = q(f"select parameter_id, claimed_unit, count(*) from source_value_extractions where parameter_id in ({PIN}) and claim_type in ('numerical','range') group by 1,2")
fam = {3: {'%', 'rise:run ratio', 'ratio', 'degrees'}, 12: {'m', 'mm'}}
bad = [(p, u, n) for p, u, n in units if u not in fam[p]]
row('E5', 'claimed_unit on numerical and range rows (slope family; length family)', 'POPULATED' if not bad else 'POPULATED-WITH-DEFECTS', sum(n for _, _, n in units),
    f'rows whose unit is not a bare family member: {sum(n for _, _, n in bad)} (prose carried in the unit field; the engine cannot parse them, and amend-extraction cannot change a unit until workplan T-1b step 8)')
# E6 why it matters (findings)
fnd = q(f"select parameter_id, count(*), sum(claim_type='qualitative') from source_value_extractions where parameter_id in ({PIN}) and figure_role='finding' group by 1")
row('E6', 'extractions with figure_role finding (claim_text verbatim, ref_id)', 'POPULATED' if fnd else 'EMPTY', sum(f[1] for f in fnd), f'by parameter (parameter, findings, qualitative): {fnd}')
# E7 evidence list
refs = [r[0] for r in q(f"select distinct ref_id from source_value_extractions where parameter_id in ({PIN})")]
ph = ','.join('?' * len(refs))
noauth = one(f"select count(*) from evidence_sources e where e.ref_id in ({ph}) and not exists (select 1 from evidence_source_authors a where a.ref_id=e.ref_id)", *refs)
noyear = one(f"select count(*) from evidence_sources where ref_id in ({ph}) and pub_year is null", *refs)
nojour = one(f"select count(*) from evidence_sources where ref_id in ({ph}) and source_type='journal_article' and journal_name is null", *refs)
jour = one(f"select count(*) from evidence_sources where ref_id in ({ph}) and source_type='journal_article'", *refs)
row('E7', 'evidence_sources + evidence_source_authors (v_evidence_authors for the sort key)', 'POPULATED-WITH-DEFECTS' if (noauth or noyear or nojour) else 'POPULATED', len(refs),
    f'sources with no author row {noauth}; no year {noyear}; journal articles with no journal_name {nojour} of {jour} (add-source has no flag for it, GAP-072); APA needs the container for those')
# E8 gaps
live_pending = one(f"select count(*) from specifications where parameter_id in ({PIN}) and retired_at is null and state='pending'")
cols = [x[1] for x in c.execute('pragma table_info(gaps)')]
row('E8', 'gaps, reached through specifications.gap_register_id', 'BLOCKED' if not live_pending else 'POPULATED', live_pending,
    f'gaps has no parameter key (columns: {cols[:7]}); a gap reaches a parameter only through a live pending specification, and there is none. Gaps that name a ramp in prose: {one("select count(*) from gaps where lower(description) like ? or lower(section) like ?", "%ramp%", "%ramp%")}')
# E9 Co-1 statement
co1 = q(f"select distinct e.ref_id from evidence_sources e join source_value_extractions x using(ref_id) where x.parameter_id in ({PIN}) and e.evidence_type='co1'")
row('E9', 'evidence_sources.evidence_type = co1 joined to extractions on the parameters', 'POPULATED' if co1 else 'EMPTY', len(co1),
    f'Co-1 sources on these parameters: {[r[0] for r in co1]}; the earlier page said none existed, which was true of the old library only')
# E10 population match
pm = one(f"select count(distinct source_ref) from evidence_population_match where source_ref in ({ph})", *refs)
row('E10', 'evidence_population_match (study population versus population served)', 'POPULATED', pm, f'sources with a graded match: {pm} of {len(refs)}; sources with none: {len(refs) - pm} (the DoD requires one only for tier 1 to 3)')
# E11 verification state
st = q(f"select extraction_status, count(*) from source_value_extractions where parameter_id in ({PIN}) group by 1")
vn = one(f"select count(*) from source_value_extractions x where x.parameter_id in ({PIN}) and x.extraction_status='verified' and not exists (select 1 from source_scans s where s.ref_id=x.ref_id and s.text_scope='full' and s.method='full-read')")
row('E11', 'extraction_status; source_scans (OR-11a: verified needs a full-scope full-read scan)', 'POPULATED', sum(n for _, n in st), f'by status {st}; verified rows with no full read scan: {vn}')
# E12 branches
rel = q(f"select r.relation, count(*) from extraction_relations r join source_value_extractions x on x.extraction_id=r.from_extraction_id where x.parameter_id in ({PIN}) group by 1")
unrel = one("select count(*) from source_value_extractions x where x.parameter_id=12 and x.figure_role='claim' and not exists (select 1 from extraction_relations r where r.from_extraction_id=x.extraction_id)")
row('E12', 'extraction_relations (condition_on and the rest) from rows of the parameters', 'POPULATED' if rel else 'EMPTY', sum(n for _, n in rel), f'by relation {rel}; parameter 12 claim rows with no relation row: {unrel} (relation none is stored as no row)')
# E13 audience lens
row('E13', 'weighting_profile (audience, use_pattern, tier_weights)', 'BLOCKED', one('select count(*) from weighting_profile'),
    'holds tier weights for synthesis, read by no script; no table says what each audience sees first or which sections open, so an audience lens has no data to render from')
# E14 provenance
try:
    import retrieval_log as rl
    held_bytes = sum(1 for r in refs if any(a['exists'] for a in rl.artefacts_for_source(r)))
except Exception as e:  # pragma: no cover
    held_bytes = -1
row('E14', 'PRAGMA user_version; retrieval-log artefacts per source (retrieval_log.artefacts_for_source)', 'POPULATED', one('pragma user_version'),
    f'schema version shown; sources with a persisted artefact: {held_bytes} of {len(refs)} (sources read from a live page and never persisted show none)')
# E15 marker
row('E15', 'specifications.marker (the evidence marker, filled and CHECK-held)', 'BLOCKED', live, 'a value is shown with its marker or not at all (unmarked is an error); with no live determination no value may be shown as best practice, only as a sourced row')

# Invariants
row('I1', 'every numerical row has an extraction_id, a ref_id, a verbatim claim_text and a locator', 'POPULATED' if True else '', one(f"select count(*) from source_value_extractions where parameter_id in ({PIN}) and claim_type='numerical'"), 'see E3 for the violators')
row('I2', 'claim rows with no relation row: stated absolutely, or unrecorded (the schema cannot tell: --relation none writes no row)', 'REPORTED', unrel + one("select count(*) from source_value_extractions x where parameter_id=3 and figure_role='claim' and claim_type='numerical' and not exists (select 1 from extraction_relations r where r.from_extraction_id=x.extraction_id)"), 'parameter 12 claim rows %d; the rest are parameter 3' % unrel)
row('I3', 'no figure is computed by the renderer', 'REVIEW', 0, 'not machine-checkable here; enforced by review and by the engine owning composition (rule 8)')
row('I4', 'a displayed state is one of stated, provisional, pending, not_applicable', 'BLOCKED', live, 'needs a live determination')

# Coverage of the old staged page data (E-03.json) by the rows now held
try:
    old = json.load(open('workplan/2026-10-30-ramp-spec-pages/data/E-03.json'))
    oldj = [j['code'] for j in old['jurisdictions']]
    held_all = {j for p in held for j in held[p]}
    row('X1', 'old staged page data: jurisdictions with a reading', 'POPULATED', len(oldj),
        f'old list {oldj}; now held for parameter 3 or 12: {[j for j in oldj if j in held_all]}; not held: {[j for j in oldj if j not in held_all]}')
except Exception as e:
    row('X1', 'old staged page data', 'EMPTY', 0, str(e))

if '--json' in sys.argv:
    print(json.dumps(out, indent=1))
else:
    for r in out:
        print(f"{r['id']:8} {r['status']:24} n={r['n']:<5} {r['reads']}")
        if r['note']:
            print(f"{'':8} {r['note']}")
    print('EXAMINED:', len(out), 'element/invariant probes over parameters', PARAMS, '; schema version', one('pragma user_version'))
