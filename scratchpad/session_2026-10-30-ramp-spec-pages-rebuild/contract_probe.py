#!/usr/bin/env python3
"""Probe the live database against the render contract for parameters 3 and 12 (v2, after the adversarial round).
Read-only. usage: python3 -I scratchpad/<session>/contract_probe.py [--json]

Each line is one contract element or invariant: what it reads, how many rows it examined, and a status that is
COMPUTED from what it found, never fixed in advance:
  POPULATED / POPULATED-WITH-DEFECTS (data present; defects counted), EMPTY (reads nothing), BLOCKED (cannot be
  answered from the database today; the reason is named), VIOLATED (an invariant fails), REVIEW (not machine-checkable).
The contract points here by element id; re-run it rather than quoting a figure from the document (rule 7a).
"""
import json, re, sqlite3, sys
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'scripts/assess')
sys.path.insert(0, 'scripts/research')

PARAMS = (3, 12)
PIN = ','.join(str(p) for p in PARAMS)
# The owner's scope (HANDOFF.md section 3). No table holds it until jurisdiction_buckets (T-6b) exists: an INPUT, not a fact.
SCOPE = 'US UK AU CA DE NO SE ISO EU FR CH NL DK FI BE IE ES IT PT JP SG NZ KR CN'.split()

c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
q = lambda sql, *a: c.execute(sql, a).fetchall()
one = lambda sql, *a: c.execute(sql, a).fetchone()[0]
out = []


def row(eid, reads, status, n, note=''):
    out.append(dict(id=eid, reads=reads, status=status, n=n, note=note))


def st(defects, n):
    return 'EMPTY' if not n else ('POPULATED-WITH-DEFECTS' if defects else 'POPULATED')


X = f"source_value_extractions where parameter_id in ({PIN})"
nrows = one(f"select count(*) from {X}")
refs = [r[0] for r in q(f"select distinct ref_id from {X}")]
ph = ','.join('?' * len(refs))

# E0
n0 = one("select count(*) from terms where term_id in ('TERM-089','TERM-001','TERM-091')")
row('E0', 'terms TERM-089, TERM-001, TERM-091', st(n0 != 3, n0), n0, 'TERM-089 is the page; it is not a parameter (OR-14)')
# E1 / E15 / I4
live = one(f"select count(*) from specifications where parameter_id in ({PIN}) and retired_at is null")
row('E1', 'specifications, live rows, parameters 3 and 12', 'POPULATED' if live else 'BLOCKED', live, 'no live determination: needs workplan T-2 to T-4 and the first engine run S-1')
row('E15', 'specifications.marker', 'POPULATED' if live else 'BLOCKED', live, 'a marker exists only on a live determination')
# E2 coverage, scope, duplicates, superseded
rows = q(f"select parameter_id, jurisdiction, count(*) from {X} and claim_type in ('numerical','range') and figure_role='claim' and jurisdiction is not null group by 1,2")
held = {}
for p, j, n in rows:
    held.setdefault(p, {})[j] = n
for p in PARAMS:
    ins = [j for j in SCOPE if j in held.get(p, {})]
    row(f'E2.p{p}', f'claim rows with a jurisdiction, parameter {p}', st(len(ins) < len(SCOPE), sum(held.get(p, {}).values())), sum(held.get(p, {}).values()),
        f'in scope with a row: {len(ins)} of {len(SCOPE)}; held outside the list: {sorted(set(held.get(p, {})) - set(SCOPE))}; in scope with NO row: {[j for j in SCOPE if j not in held.get(p, {})]}')
row('E2.scope', 'jurisdiction_buckets (workplan T-6b)', 'BLOCKED', 0, 'no table holds the scope; a list passed to the renderer is a curated list (rule 8); the list above is this probe\'s input')
sup = q(f"select ref_id, superseded_by_ref_id from evidence_sources where superseded_by_ref_id is not null and ref_id in ({ph})", *refs)
# same instrument under two ref_ids: same jurisdiction and same standard_number or title stem among claim rows' sources
dups = q(f"""select e1.ref_id, e2.ref_id, e1.jurisdiction from evidence_sources e1 join evidence_sources e2
             on e1.ref_id < e2.ref_id and e1.jurisdiction = e2.jurisdiction and e1.jurisdiction is not null
             and lower(substr(coalesce(e1.pub_title,''),1,40)) = lower(substr(coalesce(e2.pub_title,''),1,40)) and coalesce(e1.pub_title,'') <> ''
             where e1.ref_id in ({ph}) and e2.ref_id in ({ph})""", *refs, *refs)
row('E2.dup', 'superseded_by_ref_id; same jurisdiction and title stem under two ref_ids (a heuristic; confirm by hand)', 'POPULATED-WITH-DEFECTS' if (sup or dups) else 'POPULATED', len(sup) + len(dups),
    f'superseded: {sup}; apparent duplicate admissions: {[(a, b, j) for a, b, j in dups]}')
# E3 detail: every loc column
loccols = [x[1] for x in c.execute('pragma table_info(source_value_extractions)') if x[1].startswith('loc_') and not x[1].endswith('_end')] + ['source_section', 'file_anchor']
nolocator = one(f"select count(*) from {X} and claim_type in ('numerical','range') and " + ' and '.join(f'{k} is null' for k in loccols))
notext = one(f"select count(*) from {X} and (claim_text is null or claim_text='')")
row('E3', 'claim_text, source_section, every loc_* column and file_anchor on numerical and range rows', st(notext or nolocator, nrows), nrows, f'rows with no claim_text: {notext}; numerical or range rows with no locator in any of {len(loccols)} columns: {nolocator}')
# E4 lens
lens = {k: one(f"select count(*) from {X} and {k} is not null") for k in ('identity_code', 'icf_code', 'needs_code', 'medical_code')}
used = sorted(r[0] for r in q(f"select distinct identity_code from {X} and identity_code is not null"))
allid = one('select count(*) from base_taxonomy_identity')
row('E4', 'lens columns on the extractions; vocabularies', st(False, sum(lens.values())), sum(lens.values()), f'rows per lens column {lens}; identity codes with a tagged row {used} of {allid}; the rest have NO READING TAGGED to them, which says how the extractor tagged, not that no evidence exists')
# E5 units, by the owning function
try:
    from assess_cell import notation_family
except Exception:
    notation_family = None
units = q(f"select parameter_id, claimed_unit, count(*) from {X} and claim_type in ('numerical','range') group by 1,2")
if notation_family:
    unplaced = [(p, u, n) for p, u, n in units if p == 3 and notation_family(u) is None]
    note = 'parameter 3 rows notation_family cannot place: %d of %d' % (sum(n for _, _, n in unplaced), sum(n for p, _, n in units if p == 3))
else:
    unplaced, note = [], 'assess_cell not importable; E5 not computed'
lenbad = [(p, u, n) for p, u, n in units if p == 12 and u not in ('m', 'mm')]
row('E5', 'claimed_unit of numerical and range rows; assess_cell.notation_family (gradient family only; no length conversion is built)', st(unplaced or lenbad, sum(n for *_, n in units)), sum(n for *_, n in units),
    note + f'; parameter 12 rows whose unit is not a bare m or mm: {sum(n for _, _, n in lenbad)}')
# E6 findings
fnd = q(f"select parameter_id, count(*), sum(claim_type='qualitative') from {X} and figure_role='finding' group by 1")
row('E6', 'findings: claim_text verbatim, ref_id', st(False, sum(f[1] for f in fnd)), sum(f[1] for f in fnd), f'(parameter, findings, qualitative): {fnd}')
# E7 APA, and recorded errors
noauth = one(f"select count(*) from evidence_sources e where e.ref_id in ({ph}) and not exists (select 1 from evidence_source_authors a where a.ref_id=e.ref_id)", *refs)
noyear = one(f"select count(*) from evidence_sources where ref_id in ({ph}) and pub_year is null", *refs)
jour = one(f"select count(*) from evidence_sources where ref_id in ({ph}) and source_type='journal_article'", *refs)
nojour = one(f"select count(*) from evidence_sources where ref_id in ({ph}) and source_type='journal_article' and journal_name is null", *refs)
wrong = q(f"select ref_id from evidence_sources where ref_id in ({ph}) and (upper(coalesce(notes,'')) like '%ARE WRONG%' or upper(coalesce(notes,'')) like '%IS WRONG%' or upper(coalesce(notes,'')) like '%WRONG YEAR%' or upper(coalesce(verification_note,'')) like '%ARE WRONG%')", *refs)
row('E7', 'evidence_sources, evidence_source_authors', st(noauth or noyear or nojour or wrong, len(refs)), len(refs),
    f'no author row {noauth}; no year {noyear}; journal articles lacking journal_name {nojour} of {jour} (the add-source writer gap); sources whose own notes say a stored field is wrong (heuristic on the note text): {[r[0] for r in wrong]}')
# E8 gaps
pend = one(f"select count(*) from specifications where parameter_id in ({PIN}) and retired_at is null and state='pending'")
cols = [x[1] for x in c.execute('pragma table_info(gaps)')]
byprose = [r[0] for r in q("select gap_id from gaps where lower(coalesce(description,'')||' '||coalesce(section,'')) glob '*ramp*' or lower(coalesce(description,'')||' '||coalesce(section,'')) glob '*parameter 12*' or lower(coalesce(description,'')||' '||coalesce(section,'')) glob '*gradient*' or lower(coalesce(description,'')||' '||coalesce(section,'')) glob '*landing*' or lower(coalesce(description,'')||' '||coalesce(section,'')) glob '*term-09*'")]
row('E8', 'gaps via specifications.gap_register_id', 'POPULATED' if pend else 'BLOCKED', pend, f'gaps has no parameter key (columns {cols[:7]}); reachable by prose only: {len(byprose)} gaps match ramp, gradient, landing or parameter 12 in their text')
# E9 co-1 with the tier it would print
co1 = q(f"select e.ref_id, e.tier, e.evidence_type from evidence_sources e where e.ref_id in ({ph}) and e.evidence_type='co1'", *refs)
row('E9', 'evidence_type co1 among the parameters\' sources', st(False, len(co1)), len(co1), f'Co-1 sources {[r[0] for r in co1]}; stored tiers {sorted(set(r[1] for r in co1))}: printing the tier alone would label Co-1 as T1 (contract C11)')
# E10 population match, and self-contradiction
pm = one(f"select count(distinct source_ref) from evidence_population_match where source_ref in ({ph})", *refs)
contra = q(f"select source_ref, match_grade from evidence_population_match where source_ref in ({ph}) and match_grade <> 'PROXY' and upper(coalesce(mismatch_note,'')) glob '*PROXY*'", *refs)
row('E10', 'evidence_population_match', st(False, pm), pm, f'sources with a graded match: {pm} of {len(refs)}; notes that mention PROXY while the grade differs, CANDIDATES TO READ BY HAND, not violations (a note often explains why a grade is not PROXY): {[r[0] for r in contra]}')
# E11 scans behind the verified rows
ver = one(f"select count(*) from {X} and extraction_status='verified'")
fullscan = one("select count(*) from source_scans where text_scope='full' and method='full-read'")
unsupported = one(f"select count(*) from {X} and extraction_status='verified' and not exists (select 1 from source_scans s where s.ref_id=source_value_extractions.ref_id and s.text_scope='full' and s.method='full-read')")
row('E11', 'extraction_status; source_scans (OR-11a: verified needs a full-scope full-read scan)', 'EMPTY' if not fullscan else ('POPULATED-WITH-DEFECTS' if unsupported else 'POPULATED'), fullscan,
    f'verified rows {ver}; verified rows with no full-read scan behind them {unsupported}; full-read scans in the whole table {fullscan} (an empty second input examines nothing)')
# E12 conditions: outgoing, inbound, prose
out_e = one(f"select count(*) from extraction_relations r join source_value_extractions x on x.extraction_id=r.from_extraction_id where x.parameter_id in ({PIN}) and r.relation='condition_on'")
in_e = one(f"select count(*) from extraction_relations r join source_value_extractions t on t.extraction_id=r.to_extraction_id where t.parameter_id in ({PIN}) and r.relation='condition_on'")
edgeless = q(f"select extraction_id, claimed_unit, claim_text from source_value_extractions x where parameter_id in ({PIN}) and figure_role='claim' and claim_type in ('numerical','range') and not exists (select 1 from extraction_relations r where r.from_extraction_id=x.extraction_id)")
prose = [e for e, u, t in edgeless if re.search(r'where|relax|except|toler|recommend|prefer|only if|provided that|if ', (u or '') + ' ' + (t or ''), re.I)]
row('E12', 'extraction_relations: outgoing condition_on from the rows, inbound condition_on onto them', st(False, out_e), out_e,
    f'outgoing {out_e}, inbound onto these parameters\' rows {in_e}')
row('I2', 'claim rows with no edge that nonetheless state a condition in their unit or sentence (regex heuristic: where|relax|except|toler|recommend|prefer|only if|provided that|if)', 'POPULATED-WITH-DEFECTS' if prose else 'POPULATED', len(edgeless),
    f'edgeless claim rows {len(edgeless)}; of which carry a condition in prose {len(prose)}; the page may therefore say nothing about conditions for an edgeless row (contract section 8, position 2); --relation none writes no row')
# E13
row('E13', 'weighting_profile (door-epistemology disclosure); held-tensions T5', 'BLOCKED', one('select count(*) from weighting_profile'), 'held tension T5: no session may resolve it (held-tensions section 4); no table says what each role sees first; weighting_profile is read by no script')
# E14 provenance
try:
    import retrieval_log as rl
    heldb = sum(1 for r in refs if any(a['exists'] for a in rl.artefacts_for_source(r)))
except Exception:
    heldb = -1
row('E14', 'retrieval_log.artefacts_for_source per source', st(heldb < len(refs), len(refs)), len(refs), f'sources with a persisted artefact {heldb} of {len(refs)}; schema version {one("pragma user_version")}')
# I1: every numerical row has id, source, verbatim text and a locator
bad_i1 = one(f"select count(*) from {X} and claim_type='numerical' and (claim_text is null or claim_text='' or ref_id is null or ref_id not in (select ref_id from evidence_sources) or (" + ' and '.join(f'{k} is null' for k in loccols) + '))')
row('I1', 'numerical rows: extraction_id, a resolving ref_id, claim_text, a locator', 'VIOLATED' if bad_i1 else 'POPULATED', one(f"select count(*) from {X} and claim_type='numerical'"), f'rows failing: {bad_i1}')
row('I3', 'no figure is composed by the renderer', 'REVIEW', 0, 'not machine-checkable here; the engine owns composition (rule 8)')
# X1 old staged data
try:
    old = json.load(open('workplan/2026-10-30-ramp-spec-pages/data/E-03.json'))
    oldj = [j['code'] for j in old['jurisdictions']]
    held_all = {j for p in held for j in held[p]}
    row('X1', 'old staged page data: jurisdictions with a reading', 'POPULATED', len(oldj), f'old list {oldj}; held now for parameter 3 or 12: {[j for j in oldj if j in held_all]}; not held: {[j for j in oldj if j not in held_all]}')
except Exception as e:
    row('X1', 'old staged page data', 'EMPTY', 0, str(e))

if '--json' in sys.argv:
    print(json.dumps(out, indent=1))
else:
    for r in out:
        print(f"{r['id']:8} {r['status']:24} n={r['n']:<5} {r['reads']}")
        if r['note']:
            print(f"{'':8} {r['note']}")
    print('EXAMINED:', sum(r['n'] for r in out), 'rows read across', len(out), 'probes, parameters', PARAMS, '; schema version', one('pragma user_version'))
