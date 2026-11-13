"""Regenerates DIGEST-REPORT.md (second run) from the final replay database. Every table is a query
printed with the query beside it; re-run rather than trust."""
import json, sqlite3, re, collections
from common import DB, SESS, STEM, REF

c = sqlite3.connect('file:' + DB + '?mode=ro', uri=True)
q = lambda s, *a: c.execute(s, a).fetchall()
items = json.load(open(SESS + '/items.json'))
parked = [json.loads(l) for l in open(SESS + '/parked-writes.jsonl')]
checks = open(SESS + '/checks-after-engine-v2.txt').read()
P = []
w = P.append
DBN = '$SC/guidebook.db'  # SC = the replay scratch folder named in the brief


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
    t = norm(text).strip('() ;.')
    for col, seg in items[item]['segs']:
        if t[:25] in norm(seg) or norm(seg).strip('() ;.')[:25] in t:
            return {'CODE': 'Code (required), blue', 'BEST': 'Best Practice, magenta'}[col]
    return 'page 1 text (no class)'


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
lens = {r[0]: r[1] for r in q("select extraction_id, group_concat(coalesce(identity_code, needs_code, icf_code) || ' (' || basis || ')') "
                                "from v_live_lens_links group by 1")}
rel = collections.defaultdict(list)
for f, r_, t, lab in q("select from_extraction_id, relation, to_extraction_id, to_label from extraction_relations r join "
                       "source_value_extractions e on e.extraction_id=r.from_extraction_id where e.ref_id='REF-01037'"):
    rel[f].append(f'{r_} → ' + (str(t) if t else f'"{lab}"'))
Q_SPEC = ("select specification_id, parameter_id, coalesce(identity_code, needs_code), state, design_scale, "
          "regulatory_stratum_only, code_floor_only, gap_register_id, rule_version from specifications "
          "where created_by_session='" + STEM + "' order by 1")
specs = q(Q_SPEC)
Q_INLENS = ("select count(distinct e.ref_id), count(distinct e.extraction_id) from source_value_extractions e join "
            "v_live_lens_links l using(extraction_id) where e.parameter_id=? and <lens column>=?")
inlens = []
for sid, p, code, *_ in specs:
    col = 'identity_code' if code.isupper() and not code.startswith('A-') else 'needs_code'
    n = q(f"select count(distinct e.ref_id), count(distinct e.extraction_id), group_concat(distinct e.ref_id) from "
          f"source_value_extractions e join v_live_lens_links l using(extraction_id) where e.parameter_id=? and l.{col}=?", p, code)[0]
    eng = q("select g.description from gaps g join specifications s on s.gap_register_id=g.gap_id where s.specification_id=?", sid)[0][0]
    m = re.search(r'(\d+) extraction\(s\).*?from (\d+) source', eng)
    inlens.append((sid, p, code, n[0], n[1], n[2], (m.group(1) + ' extraction(s), ' + m.group(2) + ' source(s)') if m else '(no count in text)'))
Q_GAPS = "select gap_id, category, priority, substr(description,1,170) from gaps where created_by_session='" + STEM + "' order by 1"
gaps = q(Q_GAPS)

# ------------------------------------------------------------------ verdict
n_obs = sum(x[1] for x in outc)
w(f"""# Digest report, second run: the City of Edmonton "Checklist for Accessibility & Universal Design" (REF-01037)

**Verdict.** The replay wrote only what the rules allow while the owner's questions AQ-1 to AQ-8 are open: {len(ext)} extractions ({sum(1 for e in ext if e[4]=='claim')} value figures on parameters {', '.join(str(p) for p in sorted({e[1] for e in ext if e[4]=='claim'}))} with a lawful lens, {sum(1 for e in ext if e[11])} page-1 harm findings), {n_obs} observations covering every numbered item and every printed figure, and no identity `ALL`, no promotion, no declination and no minted term; the figures whose clause names no one are parked as exact writer argv ({len(parked)} lines, waiting on AQ-1), not written. The {len(specs)} cells the new lens links reach are {', '.join(sorted({s[3] for s in specs}))} (no in-lens source can anchor and parameters 5 and 9 have no direction); nothing is applied to the canonical database, whose sha256 did not move.

*Session `{STEM}`, a research session, `from-evidence` variant (owner-supplied PDF). Replay of the first run on a fresh scratch copy of `data/guidebook.db` (`$SC` = `/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad/replay`), applying `ADJUDICATION.md` as `REPLAY-BRIEF.md` orders it. The first run's report, batch, cell reports and check outputs are in `v1/`. Every count below is printed with the query that produced it, run against `$SC/guidebook.db`; re-run rather than trust. Canonical sha256 before and after: `3c575c89c1a6af4b9d2192e9eb43ed78bfeb366d7b31fe5fe41715c731634cdb`.*

---

## 1. Stages

| Stage | Done in this replay |
|---|---|
| base | Read the live catalogue: `select term_id from base_parameters` and `select term_id from parameter_declinations where revoked_at is null` are the only terms an adjudication names. Nothing promoted, declined or minted. |
| research | Skipped by the variant. The admission is logged `--origin owner-supplied` (search exec 204, `--slug stair-ramp-threshold-biomechanics-accessibility`, the subject the writer demands; GAP-103). |
| evidence | `add-source` gave REF-01037 as in the first run (guideline, grey, intrinsic, tier 3 derived, CA, no DOI, VERIFIED by direct-render); five slug links; no re-fetch (the PDF, nine renders, derived text and manifest are the first run's, in `retrieval-log/{STEM}/`). `pub_year` 2022 has no writer for its basis: GAP-106. |
| judgment | Observations in one pass, then adjudication; the catalogue scan recorded after them (scan 19, `--mode catalogue --text-scope full --open-pass-done`); extractions with lawful lens only; relation edges; page-1 harm findings; population match PROXY for MOB. |
| synthesis | No cross-parameter relation stated by the source beyond the edges below; nothing written. |
| specification | `assess_cell.py` once per cell the new lens links reach, after every write. |
| render | No renderer; all cells pending. |

## 2. Extractions written
Source class is the source's own colour marking (its legend, PDF p. 1: blue "Code (required)", magenta "Best Practice"), read from `items.json`; it is an attribution, not a guidebook classification (best practice is the determination's output). Lens is the live link and its basis.
{cmd(Q_EXT)}""")
rows = []
for e in ext:
    eid, p, pn, sec, role, ct, cmpv, v, u, root, dev, harm, txt = e
    it = sec.split('item ')[-1] if 'item ' in sec else 'p1'
    rows.append((eid, f'{p} {pn}', it, klass(it, txt) if it != 'p1' else 'page 1 (no class)', role + (' (harm)' if harm else ''),
                 (f'{cmpv} {v} {u}'.strip() if ct == 'numerical' else v[:70]), lens.get(eid, ''), root, dev,
                 '; '.join(rel.get(eid, [])), '“' + txt[:90] + '”'))
w(md(rows, ['id', 'parameter', 'item', "source's class", 'role', 'bound / value', 'lens (basis)', 'root', 'device', 'edges', 'claim text (verbatim, start)']))
w("""
- Bounds, not points (ADJUDICATION R8): the Code-marked 850 mm is `>=` (the source's page 1 frames its Code class as "the minimum standards"); the magenta 920 and 910 and the 1500 car figure are `>=` with the warrant in notes; the 9 m landing interval is `<=`, a ceiling on a run. "at least 910 – 915mm" is `>=` 910 with 915 in notes.
- Roots: blue figures are `untraced` with a `root_classification_basis` sentence (OR-19 presumed echo of the Alberta code; precedent extractions 57 and 64); magenta figures are `committee_assertion`. Edge 920 `exceeds` 850 is the source's own pairing.
- Lens: MOB for door width and turning rests on the page-1 sentence "a wider turning radius and wider doors are required by many wheelchairs and scooters today", which names exactly those two quantities; each row's notes mark it [ASSUMPTION] (a stricter D-2 reading is AQ-1). The 9 m interval carries the access need `A-EFFORT` on "resting areas" (it exists: `select need_code, family, absorbs from access_needs where need_code='A-EFFORT'`). No identity `ALL` anywhere (`select count(*) from v_live_lens_links l join source_value_extractions e using(extraction_id) where e.ref_id='REF-01037' and l.identity_code='ALL'` → 0).
- Item 5.3's 1500 car figure: `--value-as-written 1500x1500mm` was refused ("the quote states every claimed number as a numeral", which is right) and `raise-follow-up` has no reason for an ambiguous printed figure; the ambiguity is in the row's notes and in GAP-107.
- The parameter-8 (LRV) absent row was not written (F8). The parameter-6 absent finding is parked (no lens).

## 3. Parked writes (not written; waiting on AQ-1)
`scratchpad/""" + STEM + """/parked-writes.jsonl`, one line per figure, each the exact `db.py add-extraction` argv with the lens left blank and `"waits_on": "AQ-1"`, plus the relation edges it would carry (named by the other parked line's key). Each argv was dry-run with a probe lens and accepted, and without one is refused only by D-0182 ("must be stated in at least one lens"). Count: `wc -l` on that file. GAP-109 points to it.
""")
w(md([(r['key'], r['argv'][r['argv'].index('--parameter-id') + 1], next((r['argv'][i + 1] for i, x in enumerate(r['argv']) if x == '--comparator'), '(absent)' if 'absent' in r['argv'] else '(condition)'),
       next((r['argv'][i + 1] for i, x in enumerate(r['argv']) if x == '--claimed-value'), ''),
       '; '.join(f"{e['relation']} → {e['to_parked']}" for e in r.get('edges', [])), r.get('also_waits_on', ''), '“' + r['argv'][r['argv'].index('--claim-text') + 1][:80] + '”') for r in parked],
      ['key', 'parameter', 'comparator', 'value', 'edges', 'also waits on', 'claim text']))
w("""
Figures for quantities with no parameter (the 13 mm threshold, the 1200 mm landing, the 1700 x 1500 mm stall, stair rise and run, handrail height and diameter, control, phone, counter, sign and fountain heights, elevator car sizes, door dwell time) are observations only and are not parked (brief step 5).

## 4. Observations, by latest adjudication
""" + cmd(Q_OUT))
w(md(outc, ['outcome', 'observations']))
Q_LIST = LATEST + ("select o.observation_id, o.locator, o.surface_form, l.outcome, coalesce(l.term_id,''), substr(l.rationale,1,95) "
                   "from observed_terms o join latest l using(observation_id) where o.ref_id='REF-01037' order by o.observation_id")
w('\nEvery observation, with what its DEFERRED rationale waits on (AQ-4 a quantity; AQ-7 an element or feature; OR-17 colour contrast against TERM-011; AQ-6 the two "barrier-free path of travel" phrases):' + cmd(Q_LIST))
w(md(q(Q_LIST), ['obs', 'locator', 'surface form (as printed)', 'outcome', 'term', 'rationale (start)']))
cover = collections.defaultdict(list)
for oid, locs in q("select observation_id, locator from observed_terms where ref_id='REF-01037'"):
    m = re.search(r'item (\S+)', locs)
    cover[m.group(1) if m else 'p1'].append(oid)
missing = [k for k in items if k not in cover]
w(f"\nItem coverage, derived from `items.json` against the observations' locators: {len(items)} numbered items, items with no observation: {missing or 'none'} (computed by this script; re-run it).\n")

# ------------------------------------------------------------------ cells
w('\n## 5. Cells (the engine, once, after every write)\n' + cmd(Q_SPEC))
w(md(specs, ['spec', 'parameter', 'lens', 'state', 'design_scale', 'regulatory_stratum_only', 'code_floor_only', 'gap', 'rule']))
w('\nIn-lens sources counted by query, against the engine\'s own sentence (F11):' + cmd(Q_INLENS.replace('<lens column>', 'l.identity_code | l.needs_code')))
w(md(inlens, ['spec', 'parameter', 'lens', 'distinct in-lens sources (query)', 'in-lens extractions (query)', 'sources', "engine's gap sentence says"]))
w("""
The engine's "from N source(s)" disagrees with the distinct in-lens sources wherever the cell holds other sources' figures: the defect F11 names, filed as GAP-105 and not patched here (rule 10). A MOB cell built on codes reads `design_scale = universal` while `regulatory_stratum_only` also says so: the collision of AQ-2. Parameters 5 and 9 have no direction (`select parameter_id from base_parameters where accessibility_direction is null`); `set-parameter-direction` was deliberately not run (GAP-110: the judging session's call, to be named in the pull request).

## 6. Coverage reads (ADJUDICATION section 3)
""")
PARAMS = q("select parameter_id from base_parameters where status='active' order by 1")
PARAMS = [p[0] for p in PARAMS]
VS = "select l.{col} code, e.parameter_id, count(distinct e.extraction_id) n from v_live_lens_links l join source_value_extractions e using(extraction_id) where e.figure_role in ('claim','derived') and l.{col} is not null group by 1,2"
for reg, col, codes_q in [('identity', 'identity_code', "select identity_code from base_taxonomy_identity where status='active' order by 1"),
                          ('access need', 'needs_code', 'select need_code from access_needs order by 1')]:
    counts = {(a, b): n for a, b, n in q(VS.format(col=col))}
    rows = [[code] + [counts.get((code, p), 0) for p in PARAMS] for (code,) in q(codes_q)]
    w(f'\n**Lens by parameter, {reg} lens** (live value-supplying figures per code and active parameter, zeros included):' + cmd(codes_q + ' ; cross ' + VS.format(col=col)))
    w(md(rows, [reg] + [f'p{p}' for p in PARAMS]))
icf = q(VS.format(col='icf_code'))
w(f"\n**ICF lens**: codes with any live value-supplying figure: {icf or 'none'}; `select count(*) from base_icf` codes with none: {q('select count(*) from base_icf')[0][0] - len({x[0] for x in icf})}. Medical lens rows: `select count(*) from base_taxonomy_medical` → {q('select count(*) from base_taxonomy_medical')[0][0]}.\n")
QF = ("select e.extraction_id, e.ref_id, e.parameter_id, group_concat(coalesce(l.identity_code,'')||'/'||coalesce(l.needs_code,'')||'/'||coalesce(l.icf_code,'')) from source_value_extractions e "
      "join v_live_lens_links l using(extraction_id) where e.figure_role in ('claim','derived') group by 1 having sum(l.identity_code is null)=0 and "
      "sum(l.identity_code='ALL' or l.identity_code in (select identity_code from base_taxonomy_identity where parent_code is null))=count(*)")
lf = q(QF)
w(f"\n**Lens by figure**: value-supplying figures whose only live links are identities and every identity is `ALL` or a parent code: {len(lf)} (by ref: {dict(collections.Counter(r[1] for r in lf))}).{cmd(QF)}")
QG = LATEST + ("select o.ref_id, coalesce(l.outcome,'UNADJUDICATED'), count(*) from observed_terms o left join latest l using(observation_id) "
               "where coalesce(l.outcome,'UNADJUDICATED') in ('DEFERRED','NOT-OURS','UNADJUDICATED') group by 1,2 order by 3 desc")
w('\n**Group words without a parameter** (observations whose latest adjudication is DEFERRED, NOT-OURS or absent, by source):' + cmd(QG))
w(md(q(QG), ['ref', 'outcome', 'observations']))

# ------------------------------------------------------------------ gaps, checks
w('\n## 7. Gaps filed by this session (the three engine gaps included)\n' + cmd(Q_GAPS))
w(md(gaps, ['gap', 'cat', 'pri', 'description (start)']))
w("""
Gap ids GAP-103 onward are reissued on the fresh copy and do not mean what the first run's GAP-103 to GAP-120 meant (the first run's GAP-103, a column proposal, is not refiled: ADJUDICATION Q1). Leads (`add-locator`, REFERENCE-ONLY, not retrieved): `select ref_id, title from source_locators where recovered_from like 'REF-01037%'`. Backward mining recorded; the forward deferral was refused (GAP-104).

## 8. Checks, run once after the engine
Full output: `scratchpad/""" + STEM + """/checks-after-engine-v2.txt`.
""")
lines = [l for l in checks.splitlines() if l.startswith('=====') or 'EXAMINED' in l or l.startswith('exit=') or re.search(r'COMPLIANT|VERDICT|^PASS|^FAIL|RESULT|K0[12]', l)]
w('```\n' + '\n'.join(x[:230] for x in lines) + '\n```\n')
w("""`verified_scan_integrity` is red with the same count on untouched canonical (`python3 scripts/audit/verified_scan_integrity.py` on `data/guidebook.db`); no line of its replay output names REF-01037 or an extraction it wrote (`grep -c REF-01037` on its section → 0).

## 9. The critic's findings F1 to F16
| F | Disposition | Shown by |
|---|---|---|
| F1 | done: "Barrier-free unobstructed path of travel" (1.2) and "Barrier-free path of travel" (2.1) DEFERRED on AQ-6 citing OT-1 and OT-2; not TERM-048, not minted | §4 list, surface forms at items 1.2 and 2.1 |
| F2 | parked: 6.2's 1500 and 870 on parameter 4, verbatim, waiting on AQ-1; observation "With the ramp at any point" DEFERRED as unsettled | §3 keys 6.2-1500, 6.2-870 |
| F3 | done: harm findings on parameters 9 and 5 with `insufficient` edges (to the 850 extraction; to the label "Alberta Building Code", kind standard); search exec 204 harm flag raised; GAP-108 names items 1.5, 4.5, 8.2; directions not set (GAP-110) | §2 rows with (harm); `select harm_finding from search_executions where exec_id=204` |
| F4 | done: no `ALL`; MOB only on the page-1 sentence for door and turning; A-EFFORT on "resting areas"; every other figure parked on AQ-1 | §2 lens column; §3 |
| F5 | not repeated: no `add-parameter`, no `decline-parameter` | `select count(*) from base_parameters` equals canonical; `select count(*) from parameter_declinations` equals canonical |
| F6 | done for written rows (850, 9 m: `untraced` with basis); edge 920 exceeds 850 written; parked rows carry the same | §2 root column |
| F7 | done: bounds, not `=`; 1:20 parked as a `condition` with `condition_on` edges from 1:16 and 1:12; 910 `>=`; 1500 car kept on parameter 5 as its side | §2, §3 |
| F8 | not repeated: no parameter-8 absent row | `select count(*) from source_value_extractions where ref_id='REF-01037' and parameter_id=8` → 0 |
| F9 | done: one pass, scan recorded after it; 8.6 stall, 5.3 stretcher and 1828 by 2032 figures in observation quotes | `select observation_id from observed_terms where ref_id='REF-01037' and (context_quote like '%1700mm%' or context_quote like '%2010mm%' or context_quote like '%1828mm%')` |
| F10 | refused by the writers: no verb holds `pub_year_note` (amend-source: "'pub_year_note' is not an amendable judgement field"; correct-source refuses a DOI-less source); basis recorded in GAP-106 | GAP-106 |
| F11 | done in the report (query beside the engine's sentence, §5); tool defect filed, not patched | GAP-105 |
| F12 | done: no "payment machine" route, no TERM-013 for alarm signals, the stall not TERM-009; every non-parameter term DEFERRED | §4 |
| F13 | moot: no targeted scans (nothing promoted) | `select mode from source_scans where ref_id='REF-01037'` |
| F14 | done: "braille" lower case at 3.3; "mobility devices" as printed with the quote's "(scooters/ walkers/wheelchairs)"; 1.2's phrase in full | §4 |
| F15 | done for `device_class` (mixed, on the page-1 words naming wheelchairs and scooters), `locator_scheme`, `file_anchor`; `data_capture_status` stays `pending` (no `db.py` verb writes it: `grep -c data_capture_status scripts/db.py` → 0) | §2 |
| F16 | answered by not minting at all in this run: the brief's DEFERRED-with-question replaces the OR-17 misreading; minting the terms (A2) conflicts with R16 while AQ-4 and AQ-7 are open (see report section 4 of the hand-back) | §4 rationales |

## 10. What the first run got wrong (from the adjudication)
- It wrote the identity `ALL` on the page-1 preamble "meet the needs of all users", against OD-31, and wrote no ICF or access-need link at all: the fatigue reading of the 9 m resting interval and the blind reading of the route were lost.
- It adjudicated both "barrier-free path of travel" phrases to TERM-048, pre-empting OT-1 and OT-2, and recorded one of them cut short.
- It promoted TERM-022 and TERM-092 to parameters (13 and 14) while declining fourteen held terms as elements; TERM-092 belongs to E2 and T-072 item 6, and TERM-022's definition states its own answer.
- It stored `=` on figures its source calls minimum standards, a ramp threshold as a gradient claim, and "at least 910 – 915mm" as a closed `between`.
- It stored Code-marked figures as `committee_assertion` with no root, and wrote no relation edge for the source's own pairings.
- It wrote an LRV `absent` row on a concept it had itself deferred.
- It wrote no harm row for the page-1 inadequacy statement and took neither R7 route for the hazards tied to no parameter.
- It recorded the catalogue scan before the open pass was complete, missed three figures, ran the engine and checks before its last writes, and reported "the only in-lens source is grey" from the engine's sentence, which counts something else.
- It proposed a best-practice column (GAP-103); best practice is the determination's output, and the source's marking is root attribution and edges.

## 11. What was not done
- No figure whose clause names no one was written (AQ-1); no term minted, promoted or declined (AQ-4, AQ-7); the route phrases wait on AQ-6.
- No direction set for parameters 5 and 9; no Co-1, T2 or Co-2 pass (AQ-5 open on the committee's standing); no retrieval of the four leads; no forward citation pass (and its deferral could not be recorded).
- `pub_year_note` not written (no verb); `data_capture_status` not moved (no verb).
- No migration emitted from `batch.sql`, nothing applied, nothing committed; no adversarial pass on this replay.
- First attempt discarded: the observation driver was run twice against the first fresh copy, which wrote every adjudication twice; that copy was discarded, a new copy taken, and admission and observations run once. Its log is kept outside the repository (`$SC/discarded-attempt1.jsonl`).
""")
open(SESS + '/DIGEST-REPORT.md', 'w').write('\n'.join(P))
print('written', SESS + '/DIGEST-REPORT.md')
