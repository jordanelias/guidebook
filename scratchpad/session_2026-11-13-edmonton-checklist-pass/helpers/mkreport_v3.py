"""Regenerates DIGEST-REPORT.md (third run) from the final replay3 database and the engine's JSON.
Every table is a query printed beside it; re-run rather than trust."""
import json, sqlite3, re, collections, glob
from common import DB, SESS, STEM, REF, SC

c = sqlite3.connect('file:' + DB + '?mode=ro', uri=True)
q = lambda s, *a: c.execute(s, a).fetchall()
items = json.load(open(SESS + '/items.json'))
parked = [json.loads(l) for l in open(SESS + '/parked-writes.jsonl')]
checks = open(SESS + '/checks-after-engine-v3.txt').read()
gid = json.load(open(SC + '/gap-ids.json'))
SHA = '3c575c89c1a6af4b9d2192e9eb43ed78bfeb366d7b31fe5fe41715c731634cdb'
P = []
w = P.append
DBN = '$SC/guidebook.db'


def md(rows, head):
    s = '| ' + ' | '.join(head) + ' |\n|' + '|'.join('---' for _ in head) + '|\n'
    for r in rows:
        s += '| ' + ' | '.join(str('' if x is None else x).replace('|', '\\|').replace('\n', ' ') for x in r) + ' |\n'
    return s


def cmd(s):
    return f'\n`GUIDEBOOK_DB_PATH={DBN}` · query: `{s}`\n\n'


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def klass(item, text):
    if item not in items:
        return 'page 1 (no class)'
    t = norm(text).strip('() ;.')
    for col, seg in items[item]['segs']:
        if t[:25] in norm(seg) or norm(seg).strip('() ;.')[:25] in t:
            return {'CODE': 'Code (required), blue', 'BEST': 'Best Practice, magenta'}[col]
    return '?'


LATEST = ("with latest as (select a.* from term_adjudications a where a.adjudication_id=(select max(adjudication_id) "
          "from term_adjudications b where b.observation_id=a.observation_id)) ")
Q_OUT = LATEST + ("select coalesce(l.outcome,'UNADJUDICATED'), count(*) from observed_terms o left join latest l "
                  "using(observation_id) where o.ref_id='REF-01037' group by 1")
outc = q(Q_OUT)
Q_EXT = ("select e.extraction_id, e.parameter_id, t.canonical_en, e.source_section, e.figure_role, e.claim_type, "
         "coalesce(e.comparator,''), coalesce(e.claimed_value,''), coalesce(e.claimed_unit,''), e.root_type, "
         "coalesce(e.device_class,''), e.harm_finding, e.claim_text from source_value_extractions e join base_parameters p "
         "using(parameter_id) join terms t using(term_id) where e.ref_id='REF-01037' order by 1")
ext = q(Q_EXT)
FIRST = ext[0][0]
Q_LENS = f"select extraction_id, identity_code, needs_code, icf_code, basis from v_live_lens_links where extraction_id >= {FIRST} order by 1, 2, 3, 4"
lens_rows = q(Q_LENS)
lens = collections.defaultdict(list)
for e, i, n, f, b in lens_rows:
    lens[e].append(i or n or f)
rel = collections.defaultdict(list)
Q_REL = ("select from_extraction_id, relation, to_extraction_id, to_label from extraction_relations r join "
         "source_value_extractions e on e.extraction_id=r.from_extraction_id where e.ref_id='REF-01037'")
for f, r_, t, lab in q(Q_REL):
    rel[f].append(f'{r_} → ' + (str(t) if t else f'"{lab}"'))
Q_SPEC = ("select specification_id, parameter_id, coalesce(identity_code, needs_code, icf_code), state, design_scale, "
          "regulatory_stratum_only, code_floor_only, gap_register_id from specifications "
          "where created_by_session='" + STEM + "' order by 1")
specs = q(Q_SPEC)
Q_GAPS = "select gap_id, category, priority, substr(description,1,150) from gaps where created_by_session='" + STEM + "' order by 1"
gaps = q(Q_GAPS)
Q_R16 = ("select distinct a.term_id, t.canonical_en from term_adjudications a join observed_terms o using(observation_id) join terms t "
         "using(term_id) where o.ref_id='REF-01037' and not exists (select 1 from base_parameters p where p.term_id=a.term_id) and not "
         "exists (select 1 from parameter_declinations d where d.term_id=a.term_id and d.revoked_at is null) order by 1")
r16 = q(Q_R16)
n_obs = sum(x[1] for x in outc)
pk_ext = [p for p in parked if p['kind'] == 'extraction']
pk_pair = [p for p in parked if p['kind'] == 'pairing']
n_absent_written = sum(1 for e in ext if e[5] == 'absent')

w(f"""# Digest report, third run: the City of Edmonton "Checklist for Accessibility & Universal Design" (REF-01037)

**Verdict.** The third run wrote {len(ext)} extractions on {len({e[1] for e in ext})} parameters ({sum(1 for e in ext if e[4]=='claim')} value figures, {sum(1 for e in ext if e[11])} page-1 harm findings, {n_absent_written} absent finding), each with every lens link its words warrant ({len(lens_rows)} links: identity, access need and ICF), {n_obs} observations adjudicated once each, no `exceeds` edge, no `ALL`, no promotion, no declination and no minted term; {len(pk_ext)} figures whose clause names no one and {len(pk_pair)} source pairings no relation kind can state are parked as exact argv. **The batch is NON-COMPLIANT on R16 pending OD-53, deliberately**: {len(r16)} held terms the source's phrases name are adjudicated `NAMES-EXISTING` and are neither parameters nor declined; the {len(specs)} cells the lens links reach are all `pending`; nothing is applied, and the canonical database's sha256 did not move.

*Session `{STEM}`, research, `from-evidence` (owner-supplied PDF). A fresh scratch copy of `data/guidebook.db` (`$SC` = `{SC}`), worked as `REPLAY-V3-BRIEF.md` orders over `REPLAY-BRIEF.md` and `ADJUDICATION.md`. The first run is in `v1/`, the second in `v2/`. Every count below is printed with the query that produced it; re-run rather than trust. Canonical sha256 before and after: `{SHA}`. Decision numbers are the register's (`grep -n -E '^### OD-(4[7-9]|5[0-5])' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`): OD-47 lens for a clause naming no one, OD-48 design_scale, OD-49 building type and elements, OD-50 may a non-code source add a parameter, OD-51 Co-1 standing of the committee, OD-52 "barrier-free path of travel", OD-53 bulk declination, OD-54 hand-written canonical rows.*

---

## 1. Stages

| Stage | Done |
|---|---|
| base | Read only. No term minted, promoted or declined. |
| research | Skipped by the variant. Owner-supplied admission logged (`--origin owner-supplied`; the writer demands a subject, so `--slug stair-ramp-threshold-biomechanics-accessibility`: gap {gid['log-search-subject']}). Its `CO1-NOT-APPLICABLE` waiver says only that this batch runs no search and so owes no Co-1 or Co-2 search; the topic's Co-1, T2 and Co-2 pass was not performed (gap {gid['co1-pass']}). |
| evidence | `add-source`: guideline, grey, intrinsic, tier 3 derived, CA, no DOI, no `publisher_location` (not in the payload), VERIFIED `direct-render` (all nine renders p0000 to p0008 read in this run), five slug links. `pub_year` 2022's basis has no writer (gap {gid['pub-year']}). |
| judgment | {n_obs} observations in one pass, each adjudicated once; the catalogue scan recorded after them; {len(ext)} extractions; {len(lens_rows)} lens links; two `insufficient` edges on the harm findings; population match PROXY for MOB, the only identity linked. |
| synthesis | Nothing written: the source's pairings have no relation kind (parked; gap {gid['relation-kind']}). |
| specification | `assess_cell.py` once per cell the lens links reach, after every write: {len(specs)} cells. |
| render | None; every cell pending. |

## 2. Extractions written
Source class is the source's own colour (its legend, PDF p. 1: blue "Code (required)", magenta "Best Practice"; text layer in `items.json`, checked on the renders in this run). It is an attribution, not a guidebook classification.
{cmd(Q_EXT)}""")
rows = []
for e in ext:
    m = re.search(r'item ([\d.]+)', e[3])
    item = m.group(1) if m else 'p1'
    bound = (f'{e[6]} {e[7]} {e[8]}'.strip() if e[5] in ('numerical', 'range') else (e[5] if e[5] == 'absent' else (e[7][:60] + '…')))
    rows.append((e[0], f'{e[1]} {e[2]}', item, klass(item, e[12]) if item != 'p1' else 'page 1 (no class)',
                 e[4] + (' (harm)' if e[11] else ''), bound, ', '.join(lens[e[0]]), e[9], e[10], '; '.join(rel[e[0]]), '“' + e[12][:70] + '”'))
w(md(rows, ['id', 'parameter', 'item', "source's class", 'role', 'bound / value', 'lens links', 'root', 'device', 'edges', 'claim text (start)']))
w(f"""
Every live lens link of these rows, as the brief asks it printed:{cmd(Q_LENS)}""")
w(md(lens_rows, ['extraction', 'identity', 'access need', 'ICF', 'basis']))
w(f"""
- **Lens rule applied throughout (F4):** the words must name the function or need, not merely the feature. The page-1 sentence "a wider turning radius and wider doors are required by many wheelchairs and scooters today" names wheelchair and scooter users (MOB), the need whose design obligation names "doorway/turning clearance" and which absorbs wheelchair users (A-REACH), and moving around using equipment (ICF d465); each row's notes mark the page-1 warrant [ASSUMPTION] (W1, OD-47). Item 2.4's "tight grasping or twisting of the wrist" names hand functions: ICF d440 "Fine hand use" and d445 "Hand and arm use"; no access-need design obligation names grip or the wrist, so no need link. "Level landings/ resting areas" keeps A-EFFORT on "resting areas", marked [ASSUMPTION] as the judge's reading that the words name the resting function. No ICF code is linked to it: b455 has no registry title to read a warrant against. No identity `ALL`: `select count(*) from v_live_lens_links where extraction_id >= {FIRST} and identity_code='ALL'` → {q(f"select count(*) from v_live_lens_links where extraction_id >= {FIRST} and identity_code='ALL'")[0][0]}.
- **No `exceeds` edge (F1):** `select count(*) from extraction_relations r join source_value_extractions e on e.extraction_id=r.from_extraction_id where e.ref_id='REF-01037' and r.relation='exceeds'` → {q("select count(*) from extraction_relations r join source_value_extractions e on e.extraction_id=r.from_extraction_id where e.ref_id='REF-01037' and r.relation='exceeds'")[0][0]}. The edges written are the two harm findings' `insufficient` edges, whose meaning ("the referent's value is NOT ENOUGH for the population or task") is the source's.
- **Bounds, not points:** blue "is"/"should be" figures are `>=` (the source's page 1 calls the code "the minimum standards"); magenta "preferred"/"recommend" figures are `>=` with the reading in notes; the 9 m interval is `<=`; "at least 910 – 915mm" is `>=` 910 with 915 in notes; item 5.3's "1500x1500mm" is stored as the side, as canonical extraction 211 stores "1.4미터×1.4미터" as 1.4 m (`select ref_id, setting from source_value_extractions where extraction_id=211`).
- **Roots:** blue figures `untraced` with the OR-19 echo sentence (precedent canonical extractions 57 and 64); magenta figures `committee_assertion` with the basis sentence F12 gives.
- **Absent findings:** {n_absent_written} written (item 2.4, parameter 6, with its ICF links); none parked. The parameter-8 (LRV) absent row is not written.

## 3. Parked writes (not written)
`scratchpad/{STEM}/parked-writes.jsonl`. Two kinds, counted separately (`grep -c '"kind": "extraction"'` and `grep -c '"kind": "pairing"'` on the file): **{len(pk_ext)} figure lines** waiting on OD-47, each the exact `db.py add-extraction` argv with the lens blank, and **{len(pk_pair)} pairing lines** waiting on "no relation kind states a recommended figure beside a stated floor", each the `relate-extraction` argv with the relation left as a marked hole. No absent finding is parked. Every figure line was dry-run twice against the scratch copy (nothing written): as parked it is refused only by D-0182 ("an extraction must be stated in at least one lens"); with a probe lens (`--identity MOB` on its own first word) it is accepted. The probe is a dry run and says nothing about which lens is right. The written pairing line (2.3) was dry-run and is refused by argparse for its hole, as intended; the two pairings between parked rows cannot be dry-run until those rows exist. Gap {gid['parked']} points at the file.

""")
pr = []
for p in parked:
    a = p['argv']
    if p['kind'] == 'extraction':
        pr.append((p['key'], 'extraction', a[a.index('--parameter-id') + 1], (a[a.index('--comparator') + 1] if '--comparator' in a else '(condition)') + ' ' + (a[a.index('--claimed-value') + 1] if '--claimed-value' in a else ''),
                   '; '.join(f"{e['relation']} → {e['to_parked']}" for e in p.get('edges', [])), p['waits_on'] + ('; ' + p['also_waits_on'] if p.get('also_waits_on') else ''),
                   '“' + a[a.index('--claim-text') + 1][:70] + '”', p.get('dry_run_as_parked', {}).get('exit'), p.get('dry_run_with_probe_lens', {}).get('exit')))
    else:
        pr.append((p['key'], 'pairing', '', '', f"{p['from']} → {p['to']}", p['waits_on'], '“' + a[a.index('--quote') + 1][:70] + '”',
                   p.get('dry_run_as_parked', {}).get('exit', 'not run'), ''))
w(md(pr, ['key', 'kind', 'parameter', 'bound', 'edges / pair', 'waits on', 'source words', 'dry-run exit as parked', 'with probe lens']))
w(f"""
Item 6.2's "With the ramp at any point shall not be less than 1500mm/60”" is decided once (F9): its sentence has no subject noun, so what the 1500 mm measures cannot be settled on this source; it is an observation adjudicated `DEFERRED` with that reason and is neither written nor parked. Figures for quantities with no parameter (threshold rise, landing length, stall size, stair rise and run, handrail height and diameter, control, phone, counter, sign and fountain heights, elevator car sizes, door dwell time) are observations only.

## 4. Observations, by latest adjudication
{cmd(Q_OUT)}""")
w(md(outc, ['outcome', 'observations']))
Q_ALL = LATEST + ("select o.observation_id, o.locator, o.surface_form, l.outcome, coalesce(l.term_id,''), substr(l.rationale,1,110) from observed_terms o "
                  "join latest l using(observation_id) where o.ref_id='REF-01037' order by o.observation_id")
w('\nEvery observation:' + cmd(Q_ALL))
w(md(q(Q_ALL), ['obs', 'locator', 'surface form (as printed)', 'outcome', 'term', 'rationale (start)']))
seen = {re.sub(r'.*item ', '', r[0]) for r in q("select locator from observed_terms where ref_id='REF-01037'")}
miss = [k for k in items if k not in seen]
w(f"\nItem coverage against `items.json`: {len(items)} numbered items, items with no observation: {miss or 'none'} (computed by this script).\n")
w(f"""
**R16 is red, deliberately (F2).** A phrase that names a held term is adjudicated `NAMES-EXISTING` to it; R16 then requires the term to be a parameter or declined, and this batch does neither (OD-53 asks whether a single-source batch may decline). The terms:{cmd(Q_R16)}""")
w(md(r16, ['term', 'name']))

# ---- groups
Q_GRP = LATEST + ("select o.locator, o.surface_form, l.outcome, coalesce(l.term_id,'') from observed_terms o join latest l using(observation_id) "
                  "where o.ref_id='REF-01037' and (o.surface_form like '%blind%' or o.surface_form like '%Deaf%' or o.surface_form like '%low vision%' "
                  "or o.surface_form like '%Low Vision%' or o.surface_form like '%cane%' or o.surface_form like '%mobility%' or o.surface_form like '%read%' "
                  "or o.surface_form like '%Access' or o.surface_form like '%Strollers%') order by o.observation_id")
Q_REACH = ("select coalesce(l.identity_code, l.needs_code, l.icf_code) code, count(distinct e.extraction_id), group_concat(distinct e.parameter_id) "
           "from v_live_lens_links l join source_value_extractions e using(extraction_id) where e.ref_id='REF-01037' group by 1 order by 1")
w(f"""
## 5. Which groups the document reaches, and what reached a row
The groups the document's own words name are observations of their own (F7):{cmd(Q_GRP)}""")
w(md(q(Q_GRP), ['locator', 'group phrase as printed', 'outcome', 'term']))
w(f"What reached a row, by lens code:{cmd(Q_REACH)}")
w(md(q(Q_REACH), ['lens code', 'extractions', 'parameters']))
w("""Stated plainly: **this source's blind, low-vision, Deaf, hard-of-hearing, cognitive and quiet-space content reached no extraction.** It reached rows only as observations adjudicated `DEFERRED` (the group phrases; colour contrast; braille, tactile and audible provisions; signage in symbol form for "those with visual processing difficulties or who are unable to read"; the quiet space) or `NAMES-EXISTING` to element terms the catalogue holds as neither parameter nor declined (hearing loop, captioning, pictogram signage, tactile walking surface indicator). Every extraction is a mobility, reach, effort or hand-function figure. A group phrase cannot be adjudicated to its identity code (an adjudication names only a term, and the catalogue holds no term for these groups), so DEFERRED is the only outcome that fits; the four access category names stand in white text on page 1 and are not visible on the render.

## 6. Cells (the engine, once per cell, after every write)
""" + cmd(Q_SPEC))
w(md(specs, ['spec', 'parameter', 'lens', 'state', 'design_scale', 'regulatory_stratum_only', 'code_floor_only', 'gap (engine-written)']))
Q_IN = ("select e.ref_id, s.tier, s.evidence_type, e.figure_role, e.extraction_method, count(*) from source_value_extractions e join v_live_lens_links l "
        "using(extraction_id) join evidence_sources s using(ref_id) where e.parameter_id=? and l.<lens column>=? group by 1,2,3,4,5")
w("Per cell, from this run's own counts and the engine's `--report-json` (`" + SC + "/emit/cell-<parameter>-<code>.json`), not from the gap sentence. In-lens rows:" + cmd(Q_IN))
crow = []
for sid, p, code, st, ds, rso, cfo, g in specs:
    col = 'identity_code' if code == 'MOB' else ('needs_code' if code.startswith('A-') else 'icf_code')
    inl = q(f"select e.ref_id, s.tier, s.evidence_type, e.figure_role, e.extraction_method, count(*) from source_value_extractions e join v_live_lens_links l using(extraction_id) join evidence_sources s using(ref_id) where e.parameter_id=? and l.{col}=? group by 1,2,3,4,5", p, code)
    d = json.load(open(f'{SC}/emit/cell-{p}-{code}.json'))[0]
    recs = '; '.join(f"{r['ref_id']} T{r['tier']} {r['evidence_type']} pop={r['population_directness']} cond={r['conditioning']} tier_consistent={r['tier_consistent']}" for r in d['source_records'])
    gtxt = q('select description from gaps where gap_id=?', g)[0][0]
    m = re.search(r'from (\d+) source\(s\)', gtxt)
    crow.append((f'{p} × {code}', len({r[0] for r in inl}), '; '.join(f'{r[0]} T{r[1]} {r[2]} {r[3]}/{r[4]} ×{r[5]}' for r in inl),
                 d['n_sources'], recs or '(none gathered)', d['skimmed_findings'] or '', d['excluded_not_publishable'] or '', d['needs_population_assessment'] or '',
                 (m.group(0) if m else '(no source count)') + ('; "disqualified, or tier not derivable"' if 'tier not derivable' in gtxt else '; "NONE COUNTS"' if 'NONE COUNTS' in gtxt else '')))
w(md(crow, ['cell', 'distinct in-lens sources', 'in-lens rows (ref, tier, type, role/method, n)', 'engine n_sources', 'engine source_records',
            'skimmed_findings', 'excluded_not_publishable', 'needs_population_assessment', 'gap sentence says']))
w(f"""
What each cell actually is:
- **5 × MOB and 9 × MOB.** Five distinct sources hold rows in each lens; two are grey tier 3 (REF-00468 and REF-01037) and three are tier-6 codes. The engine gathers two "sources" (REF-00139 and REF-01037): the codes REF-00987 and REF-01031 hold only skimmed rows (`excluded_not_publishable`), and REF-00468's parameter-5 rows are skimmed findings (`skimmed_findings`) while its parameter-9 row is a skimmed claim. Nothing is disqualified: every source record reads `tier_consistent true`; REF-01037 is `DOWN-WEIGHTED`, REF-00139 `NON-ANCHORING`. No anchor exists, no T3-clinical source exists, and a T4-6 source is present, so the engine's regulatory branch ran and wrote `regulatory_stratum_only = 1`, `code_floor_only = 1` and `design_scale = universal` although a grey tier-3 source is in the lens; the cell is still `pending` because the branch found the regulatory evidence not rich enough and parameters 5 and 9 have no direction.
- **5 × A-REACH, 5 × d465, 9 × A-REACH, 9 × d465.** REF-01037 alone. `population_directness NOT_ASSESSED`: the population match writer takes an identity only (`evidence_population_match.target_population` references `base_taxonomy_identity`), so no match row can reach a need or ICF cell. Pending; no direction.
- **12 × A-EFFORT.** Two sources: REF-01033 (tier 1, clinical) holds a finding the engine lists in `skimmed_findings` and leaves out (it owes a dedicated reading), and REF-01037's 9 m ceiling, `NOT_ASSESSED` for the same reason. Parameter 12 has a direction (`lower_is_better`); the cell is pending because its one value-supplying source is grey tier 3.
- **6 × d440 and 6 × d445.** Only REF-01037's absent finding; `n_sources = 0`. The engine's text here ("NONE COUNTS: none states a value") is true.

**Which gap sentences are untrue.** In the seven cells whose text says "none of those sources qualified to anchor — disqualified, or tier not derivable from their own (evidence_type, scope)", that cause is untrue: no source is disqualified and every one is tier-consistent; the cause is that the only value-supplying sources are a grey tier-3 checklist and (in the MOB cells) one code. In the two MOB cells "from 2 source(s)" understates five in-lens sources (it counts gathered value-supplying sources). The regulatory flags of the MOB cells say the cell rests on codes only while a grey source is in the lens. The gap texts are in the batch as the engine wrote them; the defect is gap {gid['engine-text']} (rule 10: not patched).

## 7. Coverage reads (ADJUDICATION section 3)
""")
PARAMS = [p[0] for p in q("select parameter_id from base_parameters where status='active' order by 1")]
VS = ("select l.{col} code, e.parameter_id, count(distinct e.extraction_id) n from v_live_lens_links l join source_value_extractions e "
      "using(extraction_id) where e.figure_role in ('claim','derived') and l.{col} is not null group by 1,2")
for reg, col, codes_q in [('identity', 'identity_code', "select identity_code from base_taxonomy_identity where status='active' order by 1"),
                          ('access need', 'needs_code', 'select need_code from access_needs order by 1')]:
    counts = {(a, b): n for a, b, n in q(VS.format(col=col))}
    rows = [[code] + [counts.get((code, p), 0) for p in PARAMS] for (code,) in q(codes_q)]
    w(f'\n**Lens by parameter, {reg} lens** (live value-supplying figures per code and active parameter, zeros included):' + cmd(codes_q + ' ; cross ' + VS.format(col=col)))
    w(md(rows, [reg] + [f'p{p}' for p in PARAMS]))
icf = q(VS.format(col='icf_code'))
w(f"\n**ICF lens** (value-supplying figures): {icf or 'none'}; codes with none: `select count(*) from base_icf` minus that → {q('select count(*) from base_icf')[0][0] - len({x[0] for x in icf})}. The d440/d445 links sit on an absent finding, not a value. Medical lens rows: `select count(*) from base_taxonomy_medical` → {q('select count(*) from base_taxonomy_medical')[0][0]}.\n")
QF = ("select e.extraction_id, e.ref_id, e.parameter_id from source_value_extractions e join v_live_lens_links l using(extraction_id) "
      "where e.figure_role in ('claim','derived') group by 1 having sum(l.identity_code is null)=0 and "
      "sum(l.identity_code='ALL' or l.identity_code in (select identity_code from base_taxonomy_identity where parent_code is null))=count(*)")
lf = q(QF)
w(f"**Lens by figure**: value-supplying figures whose only live links are identities, every one `ALL` or a parent code: {len(lf)}; of them REF-01037's: {sum(1 for r in lf if r[1]==REF)}.{cmd(QF)}")
QG = LATEST + ("select o.ref_id, coalesce(l.outcome,'UNADJUDICATED'), count(*) from observed_terms o left join latest l using(observation_id) "
               "where coalesce(l.outcome,'UNADJUDICATED') in ('DEFERRED','NOT-OURS','UNADJUDICATED') group by 1,2 order by 3 desc limit 8")
w('**Words without a parameter** (observations whose latest adjudication is DEFERRED, NOT-OURS or absent; top rows):' + cmd(QG))
w(md(q(QG), ['ref', 'outcome', 'observations']))

w('\n## 8. Gaps filed (the engine\'s included)\n' + cmd(Q_GAPS))
w(md(gaps, ['gap', 'cat', 'pri', 'description (start)']))
w(f"""
Gap ids were assigned by the writer on this fresh copy (this run's own keys to ids: `{SC}/gap-ids.json`); they do not mean what earlier runs' ids meant. Leads: `select ref_id, title from source_locators where recovered_from like 'REF-01037%'`. Backward mining recorded; the forward pass was not run (an owner-supplied, from-evidence batch), no probe was made, and its deferral was refused by the writer (gap {gid['mining-forward']}).

## 9. Checks, run once after the engine
Full output: `scratchpad/{STEM}/checks-after-engine-v3.txt`.
""")
lines = [l for l in checks.splitlines() if l.startswith('=====') or 'EXAMINED' in l or l.startswith('exit=') or re.search(r'COMPLIANT|VERDICT|^PASS|^FAIL|RESULT|K0[12]|R1:|✗', l)]
w('```\n' + '\n'.join(x[:260] for x in lines) + '\n```\n')
w(f"""`research_batch_dod` is red on R16 alone, for the {len(r16)} terms of section 4 (its message truncates the list at eight). `R1` passes on the waiver token: its predicate is `findings_note LIKE '%CO1-NOT-APPLICABLE%'` and does not read the reason (`grep -n "CO1-NOT-APPLICABLE%" scripts/audit/research_batch_dod.py`). `extraction_relations_integrity` is CLEAN and would have been CLEAN with the second run's reversed `exceeds` edge: it reads shape, not meaning. `verified_scan_integrity` is red with the same count on untouched canonical (`python3 scripts/audit/verified_scan_integrity.py`), and no line of its output here names REF-01037.

## 10. The second critic's findings F1 to F13 and the withheld W1 to W3
| | Disposition | Shown by |
|---|---|---|
| F1 | Done: no `exceeds` edge anywhere, none in a parked line; no relation kind fits the pairing (`exceeds` = referent more than needed; `delta_over` = an increment; `confirms` = an independent measurement), so {len(pk_pair)} pairings are parked with the relation as a marked hole and gap {gid['relation-kind']} names the missing kind and that `extraction_relations_integrity` checks shape, not meaning. Harm findings keep `insufficient`. | §2, §3 |
| F2 | Done: {len(r16)} terms adjudicated `NAMES-EXISTING` where the phrase names them; R16 is red and kept red (gap {gid['r16']}); no decline. DEFERRED rationales now say why each is held; none cites AQ-7/OD-53 for what it does not ask. The conflict is in section 11. | §4 |
| F3 | Done: observations for item 4.5's hazard sentence, 6.5, 8.5 pipes, 11.2 grey colours, 4.3 isolated steps, 8.6 toilet paper; the R7 gap {gid['harm']} quotes only the source; the search note lists them. | §4; `select findings_note from search_executions where exec_id=204` |
| F4 | Done: one rule (the words must name the function or need). 2.4's absent finding written with ICF d440, d445 (no need definition names grip or wrist); 9 m keeps A-EFFORT, [ASSUMPTION] in its notes. | §2 |
| F5 | Done: A-REACH and d465 beside MOB on every page-1-warranted row, from the registries' own definitions; no link the words do not name. | §2 lens table |
| F6 | Done: population match PROXY for MOB (the only identity linked); a need or ICF cell cannot take one (its target is an identity), so it stays NOT_ASSESSED. Cells explained from counts and JSON; untrue gap sentences named; engine not patched (gap {gid['engine-text']}). | §6 |
| F7 | Done: observations for 4.1's first sentence, 4.7's handrail contrast, 8.6's bullets, 9.6's seats, 7.3's two heights, 3.6's font, 8.5's faucets, 9.4's counter section, page 1's strollers (NOT-OURS) and four access categories (white text), and the six group phrases. Section 5 added. | §4, §5 |
| F8 | Done: the waiver now says only that this batch owes no search; gap {gid['co1-pass']} records the topic pass not performed (EG, P2; `add-gap` has no `--slug`, so the slug is in its text). R1's substring predicate is a gate-design finding (section 11). | `select findings_note from search_executions where exec_id=204` |
| F9 | Done: each parked `notes` states what the page prints; 6.2's 1500 decided once (observation DEFERRED, not parked); parked lines and absent findings counted separately. | §3 |
| F10 | Done: no row cites a disposable database, an earlier run's gap id or "this replay"; precedents cite canonical rows by query; gap ids are the writer's from this run. | the text-column queries of section 12 |
| F11 | Done: no `publisher_location`; renders p0000 to p0008 read in this run and the methods say so; `pub_year` basis in gap {gid['pub-year']} (no writer takes notes), with the stamp said only to be on the URL and to decode to 2021-09-14. | `select publisher_location, lang_detection_method, verification_method from evidence_sources where ref_id='REF-01037'` |
| F12 | Done: magenta root basis as given. | §2 |
| F13 | Done: the forward pass is said only not to have been run and no probe made. | gap {gid['mining-forward']} |
| W1 | Recorded: MOB kept on the page-1 sentence for the 850 mm it calls inadequate; [ASSUMPTION] in the notes; OD-47. | §2 |
| W2 | Recorded: item 1.2's "minimum width" adjudicated DEFERRED waiting on OD-52, not TERM-002. | §4 |
| W3 | Recorded: Co-1 standing not judged (OD-51); the source is grey. | §1 |

## 11. Conflicts between the rules, the adjudication and the writers
1. **R16 against DEFERRED.** R16 reads only adjudications that name a term (`a.term_id IS NOT NULL`, `grep -n 'undisposed = _rows' -A8 scripts/audit/research_batch_dod.py`); no gate, view or skill reads a DEFERRED row (`git grep -n -E "'DEFERRED'" -- scripts governance/check-registry.yaml ':!scripts/migrations'`). So the honest act (NAMES-EXISTING to an element term the catalogue holds undeclined) turns R16 red, and the dishonest one (DEFERRED with a reason that is not one) keeps it green. R16 also reads every adjudication, not the latest (no `max(adjudication_id)` in its join), so a later re-adjudication cannot clear an earlier one. And the plan's own OD-53 entry says T-087's observations naming such a term "are adjudicated DEFERRED, naming the term and this question, instead of NAMES-EXISTING" (`grep -n -F 'are adjudicated `DEFERRED`' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`): this run follows REPLAY-V3-BRIEF F2, which reverses that, so the plan text and this batch disagree.
2. **DEFERRED is the only outcome left for settled content this batch may not mint.** An element or quantity with no held term can be recorded only as NAMES-NEW (which needs a term, so `add-term`) or DEFERRED. With minting withheld, the rationale says DEFERRED records a withheld act, against the schema's "cannot be settled on this source alone". Likewise a group phrase has no term to name: the group is an identity code, and `term_adjudications.term_id` references `terms` only (`select sql from sqlite_master where name='term_adjudications'`).
3. **R1's substring.** `R1` passes on `findings_note LIKE '%CO1-NOT-APPLICABLE%'` whatever the reason says (`grep -n "CO1-NOT-APPLICABLE%" scripts/audit/research_batch_dod.py`); here it passes on a waiver that concedes the pass was not done.
4. **The relation vocabulary.** No kind for "a recommended figure beside a stated floor" (`select sql from sqlite_master where name='extraction_relations'`); `extraction_relations_integrity` checks shape, so a reversed meaning passes CLEAN (gap {gid['relation-kind']}).
5. **The engine's gap text** (gap {gid['engine-text']}): "from N source(s)" counts gathered value-supplying sources; "disqualified, or tier not derivable" is printed for tier-consistent, down-weighted sources; the regulatory branch writes code-only flags with a grey source in the lens (`grep -n 'elif regulatory:' scripts/assess/assess_cell.py`).
6. **Population match against non-identity lenses.** A need or ICF cell's `population_directness` is always `NOT_ASSESSED`: `evidence_population_match.target_population` references `base_taxonomy_identity` (`select sql from sqlite_master where name='evidence_population_match'`).
7. **`add-gap` has no `--slug`** (`python3 scripts/db.py add-gap --help`), though the brief asked for one on the Co-1 pass gap; the slug is in the description.

## 12. What was not done
- No figure whose clause names no one was written (OD-47); no term minted, promoted or declined (OD-50, OD-53); the route phrases wait on OD-52; no direction set for parameters 5 and 9 (gap {gid['direction']}).
- No Co-1, T2 or Co-2 pass (gap {gid['co1-pass']}); no lead retrieved; no forward citation pass.
- `pub_year`'s basis not written (no writer); `data_capture_status` not moved (no `db.py` verb writes it).
- `batch.sql` emitted, not applied; nothing committed; no adversarial pass on this run.
- Text-column self-check (F10): `select count(*) from source_value_extractions where ref_id='REF-01037' and (notes like '%this replay%' or notes like '%first run%' or notes like '%scratch database%')` → {q("select count(*) from source_value_extractions where ref_id='REF-01037' and (notes like '%this replay%' or notes like '%first run%' or notes like '%scratch database%')")[0][0]}; the same over this session's gaps → {q("select count(*) from gaps where created_by_session=? and (description like '%this replay%' or description like '%first run%' or description like '%scratch database%')", STEM)[0][0]}; over this batch's adjudication rationales → {q("select count(*) from term_adjudications where created_by_session=? and (rationale like '%this replay%' or rationale like '%first run%' or rationale like '%AQ-%')", STEM)[0][0]}.
""")
open(SESS + '/DIGEST-REPORT.md', 'w').write(''.join(P))
print('written', len(''.join(P)))
