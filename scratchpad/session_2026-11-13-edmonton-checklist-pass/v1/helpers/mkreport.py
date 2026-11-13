import json, sqlite3, re, collections, textwrap
SC='/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad/edm/'
OUT='/home/user/guidebook/scratchpad/session_2026-11-13-edmonton-checklist-pass/DIGEST-REPORT.md'
c=sqlite3.connect('file:'+SC+'guidebook.db?mode=ro',uri=True)
q=lambda s,*a:c.execute(s,a).fetchall()
items=json.load(open(SC+'items.json'))
STEM='session_2026-11-13-edmonton-checklist-pass'
def md(rows,head):
    s='| '+' | '.join(head)+' |\n|'+'|'.join('---' for _ in head)+'|\n'
    for r in rows: s+='| '+' | '.join(str(x).replace('|','\\|').replace('\n',' ') for x in r)+' |\n'
    return s
P=[]
w=P.append
# ---- derived facts
nitems=len(items)
cc=collections.Counter('/'.join(sorted({s[0] for s in v['segs']})) for v in items.values())
nobs=q("select count(*) from observed_terms where ref_id='REF-01037'")[0][0]
oc=dict(q("select a.outcome,count(*) from term_adjudications a join observed_terms o using(observation_id) where o.ref_id='REF-01037' group by 1"))
ext=q("select e.extraction_id,e.parameter_id,t.canonical_en,e.source_section,e.claim_type,coalesce(e.claimed_value,''),coalesce(e.claimed_unit,''),coalesce(e.comparator,''),e.figure_role,e.notes,e.claim_text,e.setting from source_value_extractions e join base_parameters p using(parameter_id) join terms t using(term_id) where e.ref_id='REF-01037' order by 1")
lens={r[0]:r[1] for r in q("select extraction_id,group_concat(identity_code) from extraction_lens_links where retired_at is null group by 1")}
w(f"""# Digest report: the City of Edmonton "Checklist for Accessibility & Universal Design" (REF-01037)

**Verdict.** The PDF was digested through the pipeline's `from-evidence` variant, stages 3 to 6, on a scratch copy of the database; it yielded 16 extractions against 10 parameters and 86 harvested phrases, and **no determination**: every cell the engine could compute is `pending`, because the only in-lens source is grey, tier 3, and cannot anchor a value. Nothing is committed to the canonical database and no migration was written; the batch is held for the owner's data pull request. The adversarial pass is running and its findings are in section 9 once it returns.

*Session `{STEM}`, a research session. Every count below is the output of a command shown beside it, re-run on the scratch database `scratchpad/edm/guidebook.db` (a copy of `data/guidebook.db`, schema 131); re-run rather than trust.*

---

## 1. What the document is

| Field | As read from the document or its payload |
|---|---|
| Title | Checklist for Accessibility & Universal Design (printed on PDF p. 1) |
| Issuer | The City of Edmonton Accessibility Advisory Committee (AAC), which the text says "has created this checklist"; the page carries the Edmonton logo and the AAC logo |
| Date | **None printed.** The PDF's own `CreationDate` is 2022-03-24 (`fitz` metadata); the stored year 2022 is that, and the self-link carries a cache-buster `cb=1631580961` (an earlier fetch of the same URL) |
| Form | 9 PDF pages, 504 x 612 pt, Adobe InDesign 17, a text layer, no form fields (`pdfinfo`, `fitz`) |
| Retrieved | `curl`, HTTP 200, 204,209 bytes, sha256 `1a117aff4c5947a86d8a8061b8cd49d8060c56b03a55583e0ab342d0d5e8d525`, logged by `retrieval_log.fetch` under `retrieval-log/{STEM}/manifest.jsonl` |
| Language | English |
| Self-description | "promote the concepts of Universal Design"; "Alberta Building Code requires the minimum standards for accessibility"; aims to "exceed minimum standards where possible"; the AAC mandate is advice to City Council |

**Structure.** Eleven sections (parking, entrances, signage, stairs/escalators, elevators, ramps, handrails, washrooms, interior elements, alarm systems, furniture), each a table of numbered checklist items with a Y/N N/A column. Derive the item count: `python3 scratchpad/edm/items.py` prints one line per item; the table in section 8 has them all. As measured today there are {nitems} numbered items.

**The document colour-codes each statement.** Its legend (PDF p. 1) names two classes: **Code (required)** in blue and **Best Practice** in magenta. The text layer does not carry the distinction; it is in the colour of each run of text. I classified every run by its text-layer colour (`025087` blue, `9e2064` magenta, via PyMuPDF) and checked it against the page renders. A single item often mixes both: item 1.2 is Code for the path and Best Practice for "minimum width of 1500mm/59\"". Counts by class of item (`python3 scratchpad/edm/items.py`): {dict(cc)}.

**Things in the payload a text-only reading would miss**
- The legend names four access categories (Physical Access, Deaf or Hard of Hearing Access, Blind or Low Vision Access, Cognitive Limitations Access) in **white text** on the white page (PDF p. 1, zero-based index 0): they are in the text layer and invisible in the render, and no item carries a per-category mark. So the document gives no item-level group tag; groups are named only in running words (blind, Deaf or hard of hearing, wheelchairs, cane users, visual processing difficulties).
- The PDF names four documents by hyperlink or in text: the Alberta Building Code, City Policy C602, the City's Access Design Guide, and the Safety Codes Council Barrier-Free Design Guide (August 2019 PDF); the Code figures are the document's own attribution to "AB building code" (item 6.1) and none is retrieved here.
- Text defects as printed: item 6.2 "With the ramp at any point shall not be less than 1500mm/60\"" has no subject noun; item 5.3 prints "at least 910 – 915mm" and calls a 1500x1500 mm square a "turning radius"; item 2.10 prints a corridor width under the entrances heading; handrail rules repeat in 4.7 and 7.1.

---

## 2. How it was run (the pipeline's own order)

The owner supplied this document, so this is `/run-pipeline from-evidence` (skips discovery searching only; every later gate applies). The session was opened with `/session-open` and `/orient`, work was done on a scratch copy of the database with the canonical sha256 (`3c575c89c1a6af4b…`) unchanged, and every writer was the sanctioned `db.py` verb.

| Stage | Done |
|---|---|
| 1 base | Read against the live catalogue: ten active parameters, the identity lens, the 94 terms. The catalogue gave the vocabulary; no phrase was coined (OR-17). |
| 2 research | Skipped by the variant. The admission is logged as `log-search --origin owner-supplied` (R17). |
| 3 evidence | R9 pre-check (no URL or title match in `evidence_sources`), R10 persisted retrieval, admission, the nine page renders, full-text derivation, a catalogue scan at full scope. |
| 4 judgment | 86 phrases observed and adjudicated; 16 extractions with lens links; population match; follow-ups; gaps. |
| 5 synthesis | No cross-parameter dependency is stated by the source; no connection written (a relationship with no direct evidence is a gap, not a row). |
| 6 specification | The engine run for ten cells. |
| 7 render | No renderer exists; nothing to render (all cells pending). |
| 8 adversarial | The `antagonist` agent, read-only, with the 12 lenses. |

### Stage 3 in detail
1. **R9/R10.** No row in `evidence_sources` carries the URL or an Edmonton title. The retrieval was persisted (`1a117aff4c5947a8.pdf`) before use. A Crossref bibliographic query was also run and persisted; it returned five unrelated items (a sweep-style step the owner's framing did not call for, see section 7).
2. **Admission.** `add-source` gave REF-01037: source type `guideline`, evidence type `grey`, scope `intrinsic`, **tier 3 (derived by the writer, marker ○)**, grey flag 1 with the reason "municipal advisory committee checklist … neither a code, a standard nor a study", jurisdiction CA, no DOI (outcome NO-MATCH), verification VERIFIED by direct-render (pages read on the renders), URL accessed 2026-11-13. The classification as grey rests on the document being neither a code nor a study; it is my judgment and an owner question (GAP in section 6).
3. **Slug links** (with the claim that bears on each): `stair-ramp-threshold-biomechanics-accessibility`, `threshold-door-hardware`, `accessible-bathroom-and-grab-bar`, `reach-range-and-accessible-controls`, `luminance-contrast-and-pattern`. The slug `accessible-circulation-geometry` was refused (its labels mix schemes, GAP-013) and was not forced.
4. **Reading.** All nine page renders were read and the derived text (`full_text.py`, nine of nine pages, with page markers) against every active parameter and lens; `record-scan --mode catalogue --text-scope full --method full-read --open-pass-done`, then two `--mode targeted` scans after two terms were promoted mid-run.

### Stage 4 in detail
**Observations (R11 harvest, R16).** Every phrase the source uses for a concept, in its own words with the sentence verbatim and a locator, then adjudicated. Totals today: `select outcome,count(*) from term_adjudications a join observed_terms o using(observation_id) where o.ref_id='REF-01037' group by 1` → {oc}, over {nobs} observations. 23 name an existing term; the rest were **DEFERRED** (a quantity or element the catalogue holds no term for; not minted, because OR-17 leaves minting to the data pull request the owner reads). The list is derived by `select o.surface_form, o.locator from observed_terms o join term_adjudications a using(observation_id) where o.ref_id='REF-01037' and a.outcome='DEFERRED'`.

**Parameters.** R16 requires every term an adjudication names to be a parameter or declined with its reason. 14 existing terms were declined as elements (precedent: TERM-089 `ramp`); two were **promoted** to parameters because the source states a figure for them: TERM-022 `level threshold` (parameter 13, item 2.9) and TERM-092 `intermediate landing` (parameter 14, item 6.5). Nothing new was minted.

**Lens.** Each extraction needs at least one lens code, with a warrant in the figure's own or its source's words. Where the item names no group, the figure is tagged `ALL` ("applies to everyone") on the source's purpose statement "meet the needs of all users"; the door-width and elevator-turning figures are tagged `MOB` on the source's sentence "a wider turning radius and wider doors are required by many wheelchairs and scooters today". These are judgments the owner confirms or corrects (GAP).

**Population.** `add-population-match` for ALL and MOB, grade **PROXY** (no participants, no measurement; R13).
""")
w("""### The 16 extractions

Colour class is the source's own marking, read from the text-layer colour and checked on the render. `root_type` is `committee_assertion`, measurement paradigm `stated_unmeasured` on every row. Comparator is the one the writer's vocabulary allows; where the source writes no comparator ("should be 1100mm") `=` is used and the note says so.

""")
rows=[]
for e in ext:
    eid,pid,term,sec,ct,val,unit,cm,role,notes,claim,setting=e
    col='Code (blue)' if 'Code (required) colour' in notes else ('Best Practice (magenta)' if 'Best Practice colour' in notes else '')
    rows.append((eid,f'{pid} {term}',sec.replace('Item ',''),col,f'{cm} {val} {unit}'.strip() if ct!='absent' else 'absent ('+role+')',lens.get(eid,''),'“'+claim+'”'))
w(md(rows,['id','parameter','item','source class','value','lens','claim text (verbatim)']))
w("""**Readings that carry ambiguity** (recorded in each row's notes and in the last gap): item 6.1's `1 in 20` is a threshold above which the source says ramps are used, not a stated maximum; item 5.3's `910 – 915mm` is a range with no stated reason and its `1500x1500mm` is a square, not a radius (only the side is the value); item 6.2's 9 m is "at 9m intervals", the sense of maximum being the reader's; item 2.3's 850 mm is "is 850mm", not "minimum".

**Absent findings** (R7: the source was read for the parameter and states no figure, which is itself a result): extraction 240 for LRV contrast (the source requires contrasting colour in many items and states no luminance or reflectance figure) and 241 for operating force (item 2.4 states a grip requirement and no force). Both carry an `absence-needs-tested-value` follow-up: the figure, if any, is to be sought in the guides the source names.

### Stage 5 and 6
No cross-parameter dependency is stated by the source (the nearest, item 5.3's turning space and door width in one item, shares a sentence, not a stated dependency), so no `connections` row and no relation edge was written.

The engine (`assess_cell.py`) was run for the ten cells the new figures reach. Result, read from the written `specifications` rows and the engine's `--report-json`:
""")
cells=q("select specification_id,parameter_id,identity_code,state,coalesce(marker,''),coalesce(value_min,''),regulatory_stratum_only,code_floor_only,rule_version from specifications where created_by_session=? order by parameter_id",STEM)
w(md(cells,['spec','parameter','lens','state','marker','value','regulatory_stratum_only','code_floor_only','rule_version']))
w("""Every cell is **pending**. The gap the engine writes for 3×ALL: "3 extraction(s) of parameter 3 stated in the lens (identity_code=ALL), from 1 source(s), but none of those sources qualified to anchor — disqualified, or tier not derivable from their own (evidence_type, scope)." REF-01037 reads `grain specific`, `scale_directness DIRECT`, `population_directness PROXY`, `conditioning DOWN-WEIGHTED`: a grey tier-3 source cannot anchor, as the tier system fixes it. Parameter 3 does have a direction (`lower_is_better`); parameters 4, 5, 6, 8, 9, 11, 12, 13 and 14 have none recorded, which the gap names. Nothing here is a finding about what the best-practice values are.

**Stage 7.** No renderer exists (`ls scripts/generate/`), and a pending cell is not in `v_best_practice`; the contract's walk by hand finds only a gap to print.

---

## 3. Checks run, and what each examined
All on the scratch database (`GUIDEBOOK_DB_PATH` inline); a check is quoted with the `EXAMINED:` line it printed.
""")
def grab(f,pat):
    t=open(SC+f).read()
    return t
w(md([
('research_batch_dod --session '+STEM,'COMPLIANT; R16-adjudicate examined 86 observations; R16 examined 23 terms; R17 and R16-scan examined 1 admission'),
('judgment_handoff_shape','EXAMINED 3 invariants, clean'),
('extraction_relations_integrity','EXAMINED 287, CLEAN'),
('adjudication_integrity','EXAMINED 60, PASS, 0 tier inconsistencies'),
('observation_verbatim_audit','PASS: no class above its baseline (it also reports the existing debt paid down by this batch\'s observations)'),
('test_db_integrity','K01 and K02 each examined the ten engine-written cells (10 examined), PASS; 57 checks'),
('derivation_handshake_integrity','EXAMINED 11, CLEAN'),
('validate_evidence_state','EXAMINED 23'),
('medical_lens_integrity','EXAMINED 0, CLEAN (the medical lens is empty: examined nothing)'),
('schema_reference_audit','EXAMINED 1353 references, PASS'),
('verified_scan_integrity','FAIL on rows that existed before this batch; none concerns REF-01037 (`grep -c REF-01037` on its output prints 0)'),
('search_log_completeness --session','NOTHING-IN-SCOPE: no WebSearch or WebFetch line in this session ledger; the owner-supplied admission is listed unwitnessed'),
],['check','result']))
w(f"""`emit_batch_sql.py --scratch … --canonical data/guidebook.db` captured the batch: additive inserts only, 0 updates, 0 deletes (re-run it: it prints its own counts; the SQL is `scratchpad/edm/batch.sql`). It is **not** applied and **not** committed.

---

## 4. Gaps filed, leads, follow-ups
`select gap_id, category, priority, substr(description,1,140) from gaps where created_by_session='{STEM}'` (the engine also wrote one parameter-scoped gap per pending cell):
""")
gs=q("select gap_id,category,priority,substr(description,1,260) from gaps where created_by_session=? and category!='EG' or (created_by_session=? and category='EG') order by gap_id",STEM,STEM)
w(md(gs,['gap','cat','pri','description']))
w("""**Backward-mining leads** staged with `add-locator` (REFERENCE-ONLY, not retrieved or read): `"""+"`, `".join(r[1] for r in q("select ref_id,title from source_locators where recovered_from like 'REF-01037%' order by 1"))+"""`. The backward pass is recorded (`log-mining`); a forward (cited-by) pass is not run and could not be recorded as deferred (the writer refuses once backward set the one `citation_mining_status` flag, GAP-015/GAP-022 unruled).

---

## 5. Every item of the document and what became of it
Class is the source's own colour marking of the item's text (CODE = Code (required), BEST = Best Practice). Obs = observation ids; Ext = extraction ids.
""")
inv=[]
obs=collections.defaultdict(list)
for oid,loc,outc in q("select o.observation_id,o.locator,a.outcome from observed_terms o join term_adjudications a using(observation_id) where o.ref_id='REF-01037' order by 1"):
    m=re.search(r'item (\d+\.\d+)',loc or ''); obs[m.group(1) if m else 'p1'].append(f"{oid}{'E' if outc=='NAMES-EXISTING' else 'D'}")
exs=collections.defaultdict(list)
for e in ext: exs[e[3].replace('Item ','')].append(str(e[0]))
for k,v in items.items():
    cl='/'.join(sorted({s[0] for s in v['segs']}))
    txt=' '.join(s[1] for s in v['segs'])
    inv.append((k,v['page']+1,cl,txt[:110]+('…' if len(txt)>110 else ''),', '.join(obs.get(k,[])),', '.join(exs.get(k,[]))))
w(md(inv,['item','PDF p.','class','text (start)','Obs (E existing term, D deferred)','Ext']))
w("""Items with neither an observation nor an extraction: derive with the table above (an empty Obs and Ext cell). The qualitative requirements that name no group and no figure were observed, adjudicated DEFERRED and not extracted, because an extraction needs a parameter and a stated value or an absence for it.

---

## 6. Questions this pass leaves for the owner (each also filed as a gap)
1. **Tier and evidence type.** Is a municipal advisory-committee checklist `grey` (tier 3, ○), as classified here, or does the owner place it elsewhere? It restates Alberta building code requirements in blue and adds the committee's recommendations in magenta.
2. **Which identity states a figure when the item names no group.** `ALL` on the purpose statement "meet the needs of all users" was used for ramp slope, corridor width, headroom, landing interval and threshold figures; `MOB` for door width and elevator turning. Confirm or correct.
3. **Minting.** 57 phrases are DEFERRED, many of them quantities the source states (stair rise and run, handrail height and diameter, elevator button height, washroom stall size, counter and phone heights, sign height, accessible stall ratio). Which become parameters is the owner's reading in the data pull request (OR-17).
4. **Is the source's colour contrast the catalogue's LRV contrast?** Left DEFERRED.
5. **Code vs Best Practice has no typed column.** The distinction the document draws per statement sits in notes only (tooling gap).
6. **Sub-national jurisdiction.** Alberta and Edmonton are not in `base_jurisdictions`; the figures are recorded under CA.
7. **The two promoted parameters** (13 level threshold, 14 intermediate landing) and the 14 declinations are standing decisions about shared vocabulary.

---

## 7. What I did wrong or changed my mind about, and what I could not do
- **A discovery-style step.** I first ran a Crossref bibliographic query and treated the admission as a research find. The owner supplied the PDF, so there is no search; the Crossref payload is persisted and harmless, and the admission is logged `owner-supplied`. The writer nevertheless demands a subject for the logged search, and I gave it parameter 3 only to satisfy it (a tooling gap).
- **The artefact went to the wrong directory.** I fetched from `scripts/research/`, so `retrieval-log/` landed under it; I moved it to the repository's `retrieval-log/` before using the page renderer and the full-text derivation.
- **The session was opened late.** The first fetch commands ran before `/session-open`; their command-log lines went to the previous session folder (`session_2026-11-13-t019-lens-gather`) and need moving by `session_id`. `scratchpad/CURRENT` now names this session.
- **An overclaim, corrected.** The first catalogue-scan note said every requirement phrase had been observed; 31 items had none. I completed the open pass (31 more observations, ids from 154) and the claim is now true, but the sentence in scan 19's note predates it.
- **Value wording.** `--value-as-written "1 in 16"` was refused (the quote writes both numbers as numerals); the figure is stored as `1:16` with unit `rise:run ratio`.
- **Absent rows.** `figure_role` for an absent claim must be `finding`; first attempt as `claim` was refused.
- **Not done.** No Co-1, T2 or Co-2 pass (the log-search findings note says `CO1-NOT-APPLICABLE` for this document and that such a pass was outside this run); no retrieval of the four named documents; no forward citation pass; no data migration; the adversarial pass is not yet recorded in the database (`record-adversarial-pass` needs the critic's transcript committed first); the extraction status is left `preliminary` (no second reading has verified a row).

## 8. Ship state
Everything above exists only on the scratch database and under `retrieval-log/{STEM}/` (the PDF, nine renders, derived text and manifest, untracked). To ship: commit the retrieval-log session folder and `scratchpad/{STEM}/` (rule 6), emit and apply the batch through `emit_data_migration` and `migrate_db`, and open the data pull request last (rules 9 and 10), on a branch separate from the tooling work. **Collision to fix first:** `scripts/tests/test_run_pipeline_refusals.py` uses `REF-01037` as its fixture source id; with this batch's derived text registered under that id, its cases X02 and X03 are refused (`--verbatim-exempt` is refused over a decodable text). That is a defect in the fixtures (they should derive a free id, rule 8) and will break permanently once REF-01037 is real.

## 9. Adversarial pass
*Running at the time of writing. The critic is the `antagonist` agent, read-only, assigned accuracy (L1, L2, S2), logic (L3 to L8, S1, S3) and sequence (S4) with the 12 lenses; its findings and my disposition of each will be appended here.*
""")
open(OUT,'w').write(''.join(P))
print(len(''.join(P)))
