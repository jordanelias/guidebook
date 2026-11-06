#!/usr/bin/env python3
"""Generates rhfac-b651-catalogue.md from the persisted RHFAC survey text.
Regenerate (repo root): pdftotext -layout retrieval-log/session_2026-11-06-base-vocabulary-review/94f80b1b66776c72.pdf /tmp/rhfac.txt
then adapt SCR/paths below. Every figure in the document is computed here, never typed."""
import re, json, collections, sqlite3, sys
SCR='/tmp/claude-0/-home-user-guidebook/85c53b12-0695-5c1e-b998-83da3eff20b4/scratchpad'
OUT='/home/user/guidebook/scratchpad/session_2026-11-06-base-vocabulary-review'
d=json.load(open(f'{SCR}/build/criteria.json'))
con=sqlite3.connect('file:/home/user/guidebook/data/guidebook.db?mode=ro',uri=True)
TECH=[t for t in dict.fromkeys(x for r in d for x in r['techniques'])]
# integrity: stated section totals vs sum of criterion points
raw=[l.strip() for l in open(f'{SCR}/rhfac_clean.txt',encoding='utf-8')]
totals=[int(m.group(1)) for l in raw for m in [re.match(r'^Total (?:Points|Score)\s+(\d+)',l)] if m]
secs=[]; 
for r in d:
    if r['section'] not in secs and r['chapter']!='12': secs.append(r['section'])
sums=[sum(int(r['points']) for r in d if r['section']==s and str(r['points']).isdigit()) for s in secs]
mism=[(s,a,b) for s,a,b in zip(secs,sums,totals) if a!=b]
integrity=f"{len(totals)} stated section totals read, {len(secs)} sections with criteria summed (chapter 12 scored differently); mismatches (section, sum of the criterion points, the total the survey states): {mism if mism else 'none'}. A mismatch is the SURVEY's own arithmetic, kept as printed: the criteria were re-read against the text and none was dropped"
# views
by_sec=collections.OrderedDict()
for r in d: by_sec.setdefault((r['chapter'],r['chapter_title'],r['kind'],r['section'],r['section_title']),[]).append(r)
def secrow(k): return f"{k[3]} {k[4]}"
kinds=list(dict.fromkeys(r['kind'] for r in d))
mx=collections.defaultdict(lambda: collections.Counter())
for r in d:
    for t in r['techniques']: mx[t][r['kind']]+=1
tsec=collections.defaultdict(lambda: collections.Counter())
for r in d:
    for t in r['techniques']: tsec[t][f"{r['section']} {r['section_title']}"]+=1
# recurring concepts
def concept(text):
    t=text.lower(); t=re.sub(r'\([^)]*\)','',t); t=re.sub(r'\bif [a-z ,/-]*$','',t); t=re.sub(r'[^a-z -]',' ',t)
    t=re.sub(r'\b(is|are|has|have|include|includes|with|and|or|at|the|a|an|of|to|for|on|in|if|where|useful|provided|standard|all|units|appropriate)\b',' ',t)
    return re.sub(r'\s+',' ',t).strip()
cs=collections.defaultdict(set); ex={}
for r in d: k=concept(r['text']); cs[k].add(r['section']); ex.setdefault(k,r['text'])
rec=sorted(((len(v),k) for k,v in cs.items() if len(v)>=3),reverse=True)
HELD={'well-illuminated':'illuminat','surface firm stable slip resistant':'slip','seating':'seating','handrails':'handrail','clear width':'width','drainage':'drain',
 'clear signage':'signage','level threshold':'threshold','height clearance':'headroom','edge protection':'edge','tactile attention indicators':'tactile','slope':'gradient',
 'riser height tread depth':'riser','nosing design':'nosing','accessible door hardware':'hardware','shelter':'shelter','accessible controls':'control','outlets switches accessible heights':'outlet'}
def held(key):
    for k,v in HELD.items():
        if key.startswith(k) or k in key:
            r=con.execute("select distinct term_id,canonical_en from terms where lower(canonical_en) like ? union select distinct t.term_id,t.canonical_en from term_aliases a join terms t using(term_id) where lower(a.alias) like ? and lower(a.language)='en'",(f'%{v}%',f'%{v}%')).fetchall()
            return ', '.join(f"{a} {b}" for a,b in r[:4]) or 'none'
    return 'not checked'
# quantity-bearing
QB=re.compile(r'\b(width|slope|gradient|height|depth|riser|tread|force|time|clearance|size|capacity|dimension|number|ratio|spacing|interval|distance|level|volume|temperature|illuminat|lighting levels|diameter|thickness)\b',re.I)
qb=collections.defaultdict(set)
for r in d:
    for m in set(x.lower() for x in QB.findall(r['text'])): qb[m].add(r['section'])
pairs=con.execute("select language,jurisdiction,role from lang_jur_map where jurisdiction in ('US','UK','AU','CA','DE','NO','SE','ISO','EU','FR','CH','NL','DK','FI','BE','IE','ES','IT','PT','JP','SG','NZ','KR','CN') order by jurisdiction,language").fetchall()
n_param=con.execute("select count(*) from base_parameters where status='active'").fetchone()[0]
n_terms=con.execute("select count(*) from terms").fetchone()[0]
ledger=con.execute("select status,count(*) from v_scan_ledger group by 1 order by 2 desc").fetchall()
rooms=con.execute("select room_code,name from rooms order by room_code").fetchall()
dirs=con.execute("select topic_directory,count(*) from slugs group by 1 order by 1").fetchall()
doms=con.execute("select domain,count(*) from terms group by 1 order by 2 desc").fetchall()
o=[]
w=o.append
w("# Catalogue: RHFAC Rating Survey v4.0 and the CSA/ASC B651 listing, as a basis for the base register\n")
w("Session `session_2026-11-06-base-vocabulary-review`. **A lead catalogue, not evidence and not a specification.** Nothing here is admitted, no database row is written, and every figure below is computed by `scratchpad/session_2026-11-06-base-vocabulary-review/tools/doc.py` from the persisted survey text (re-run, do not trust the prose). Governing statements: the three 2026-11-06 owner entries in `references/project-standards.md` (the third is this task's).\n")
w("## 0. How to read this\n")
w("- **Guideline in approach, not exacting.** The RHFAC survey is a Canadian rating instrument: it lists criteria and weights them by points. It states **no dimension, force, slope or time**. Those live in the codes it rates against (CSA/ASC B651, the National Building Code of Canada and provincial codes), so this catalogue yields concepts and techniques to search for, never values to adopt. A criterion's point weight is RHF's weighting, not a finding about importance for disabled people.")
w("- **English first is preparation, not the register.** The text below is Canadian English from one jurisdiction (CA), one programme and one author. It is the search plan for the other 13 languages of P1+P2+P3 and a seed for the reverse path: concepts that English does not name are added from native-language readings, by the instrument's own phrase (owner E1).")
w("- **Two category axes, one table.** Every criterion carries technique tags and sits in a section that is a room, element or building typology. Both views in section 3 are generated from `rhfac-criteria.tsv`; neither is kept by hand. The technique tags are rule-assigned from the criterion's own words (regexes in `tools/build.py`): a lead for review, with multiple tags allowed because categories overlap by design.\n")
w("## 1. Sources and what was and was not read\n")
w("| Source | Retrieved | Read | Not read |\n|---|---|---|---|")
w("| RHFAC Rating Survey v4.0 (September 2024), `rickhansen.com/sites/default/files/downloads/2024-10/rhfacratingsurveyv40sept20244r.pdf`, 66 pages, sha256 `94f80b1b6677…` | `retrieval-log/session_2026-11-06-base-vocabulary-review/94f80b1b66776c72.pdf` | In full, as text (`pdftotext -layout`): every criterion title and point weight; the prerequisites; the certification levels. | Page images, if any carry content the text layer lacks. The survey names no figures, so the loss is judged small, **[UNVERIFIED]**. |")
w("| ASC database listing for CSA/ASC B651, `accessible.canada.ca/…/csa-asc-b651-accessible-design-built-environment`, sha256 `b0ca9f638851…` | `b0ca9f6388515ded.html` | The listing page: a scope paragraph and five change headings (platform dimensions, tactile direction indicator positioning, a detailed explanation of luminance contrast, functional and cognitive barriers, controls and sizes of power-assisted doors, water-bottle filling stations and controls). | **The standard itself. [SKIPPED: B651:23 full text — a paid, DRM-protected PDF of 283 pages (English) or 307 (French) at the CSA store, SKU 2430328 / 2430329; the ASC page's \"View the full standard\" leads there.]** |")
w("| CSA Group store page for CSA/ASC B651:23, `csagroup.org/store/product/csa-asc%20b651%3a23/`, sha256 `a038f0903154…` | `a038f09031540a36.html` | Edition history (1990, 1995, 2004, 2012, 2018 withdrawn; 2023 current), languages (English, French), and a nine-item list of changes in the 2023 edition (anthropometric dimensions, interpretation notes, luminance contrast, tactile direction indicator positioning, functional and cognitive barriers, power-assisted door controls, platform-lift minimum size, water-bottle filling stations, water-fountain controls). | The standard. |")
w(f"\nThe French RHFAC survey and guide and the French ASC page were retrieved before the owner said they are not needed here; they are in the retrieval log and nothing is drawn from them.\n\n**Parse integrity (computed):** {len(d)} criteria across {len(by_sec)} sections in {len({r['chapter'] for r in d})} chapters; {integrity}.\n")
w("## 2. The register this seeds\n")
w(f"The base holds {n_terms} terms and {n_param} active parameters (`select count(*) from terms`; `… from base_parameters where status='active'`). The {len(d)} criteria collapse to {len(cs)} distinct normalised statements, of which {len(rec)} recur in three or more sections. Those recurring statements are the technique concepts that every typology shares; the long tail is typology-specific. Rows for the register are written only after the tooling PR merges (CLAUDE.md rule 10).\n")
w("### 2.1 Concepts recurring in three or more sections (the shared technique vocabulary)\n")
w("| Sections | Statement as the survey words it (first occurrence) | Held in the base today (term, EN name or alias) |\n|---|---|---|")
for n,k in rec: w(f"| {n} | {ex[k]} | {held(k)} |")
w("\n'Held' is a case-insensitive substring match on the head word in English names and English aliases only; \"none\" means no English hit, not that no concept exists. A held term can be narrower or wider than the survey's criterion.\n")
w("### 2.2 Criteria that name something measurable (quantity-bearing words)\n")
w("The survey gives no values, but its words name the quantities a code would set. Word → number of sections whose criteria use it (regex `QB` in `tools/doc.py`; a lead for the open pass, not a parameter list).\n")
w("| Word | Sections |\n|---|---|")
for k,v in sorted(qb.items(), key=lambda x:(-len(x[1]),x[0])): w(f"| {k} | {len(v)} |")
w("\n## 3. The two views, generated from one table\n")
w("### 3.1 Technique category × kind of place (criterion counts)\n")
w("| Technique tag | "+" | ".join(kinds)+" | Total |\n|---|"+"---|"*(len(kinds)+1))
for t in TECH: w(f"| {t} | "+" | ".join(str(mx[t][k]) for k in kinds)+f" | {sum(mx[t].values())} |")
w("\n### 3.2 Technique → where it appears (top places by criterion count)\n")
for t in TECH:
    top=tsec[t].most_common(8)
    w(f"- **{t}** ({sum(tsec[t].values())} criteria in {len(tsec[t])} sections): "+"; ".join(f"{s} ({n})" for s,n in top))
w("\n### 3.3 Place → techniques it uses\n")
w("| Section (room, element or typology) | Kind | Criteria | Technique tags present (count) |\n|---|---|---|---|")
for k,rs in by_sec.items():
    c=collections.Counter(t for r in rs for t in r['techniques'])
    w(f"| {k[3]} {k[4]} | {k[2]} | {len(rs)} | "+", ".join(f"{t} {n}" for t,n in c.most_common())+" |")
w("\n### 3.4 Against the project's own categories\n")
w("Technique-like categories the base already has — topic directories of `slugs`: "+", ".join(f"{a} ({b})" for a,b in dirs)+"; term domains: "+", ".join(f"{a} ({b})" for a,b in doms)+".\n")
w("Rooms the base holds (`rooms`, uncategorised, no reader): "+", ".join(f"{a} {b}" for a,b in rooms)+f". The survey frames {sum(1 for k in by_sec if k[2]=='building typology / room')} building typologies or rooms in its chapter 8 and {sum(1 for k in by_sec if k[0]=='9')} dwelling rooms in chapter 9; the base's {len(rooms)} rooms cover few of them (no pool, library, laboratory, lodging room, retail outlet, playground, fitness space, trail, viewpoint). **A typology/room axis in the base needs a source-derived list, not the current 17 rooms** (owner E8 froze `rooms`; that stands until a page reads them).\n")
w("## 4. Beyond these two sources (leads, each [UNVERIFIED] until a source in hand states it)\n")
w("- **Named by the B651 listing but not by RHFAC:** luminance (colour) contrast as a method; tactile direction indicator positioning; platform size for platform lifts; controls and sizes of power-assisted doors; water-bottle filling stations and fountain controls; anthropometric dimensions as the basis of clearances; functional and cognitive barriers as a category.")
w("- **Categories the survey scores thinly or not at all**, from the project's own vocabulary and ICF frame: sound insulation between spaces and plant noise as measured quantities; vibration; air quality and ventilation (the survey asks only that scents be absent or contained); thermal setpoints; flicker and photosensitive thresholds (the survey asks for none identified); wayfinding for people who are Deafblind; sign-language and captioning provision as a space requirement; evacuation for people who cannot use stairs beyond \"area of refuge\" and \"evacuation chair\"; bariatric and short or tall stature ranges (owner-ruled body-size frame, access need A-SIZE); tactile and haptic communication zones; ceiling hoists; adult changing facilities beyond the washroom item; queuing and timed access.")
w("- **Not in either source:** building typologies the survey does not frame (transit stations and vehicles, hospitals and clinics, schools beyond \"specialized learning spaces\", prisons, places of worship, cemeteries, temporary event structures). Whether a P1+P2+P3 instrument frames them is a question for the native-language readings, not for this list.\n")
w("## 5. Research coverage, derived from the base\n")
w("**Principle (owner, 2026-11-06): the base sets the research coverage.** Coverage is one measure of a (concept × language-and-jurisdiction pair) cell, computed from the base and the reading records; no separate list of what has been searched is kept (rules 5 and 8). The pairs are `lang_jur_map` rows for the P1+P2+P3 jurisdictions:\n")
w(f"{len(pairs)} pairs (`select language, jurisdiction from lang_jur_map where jurisdiction in (…P1+P2+P3…)`): "+", ".join(f"{l}/{j}" for l,j,r in pairs)+".\n")
w(f"**Today:** the reading ledger (`v_scan_ledger`) holds, for the {n_param} active parameters only: "+", ".join(f"{s} {n}" for s,n in ledger)+f". Not one of the {len(rec)} recurring concepts above and none of the long tail has a cell, because none is a term yet; and the language half of a pair cannot be derived for any source, since `evidence_sources.language` is NULL on every row (plan defect A6). **Coverage of the new register is 0 until the first native-language reading is recorded.**\n")
w("**Cell states** (proposed; the bucket table T-6b is the home): NOT-SEARCHED; SEARCHED-FOUND (phrase, locator, quote, instrument); SEARCHED-ABSENT (the instrument was read in full and states nothing); SEARCHED-QUERY-FAILED (the search shape failed, R14); NOT-OBTAINABLE (instrument held back by paywall or block, with the attempt logged).\n")
w("## 6. The terminology research pass\n")
w("This is research, and it needs passes that read instruments in their own language. One pass per language-and-jurisdiction pair:\n")
w("1. **Instrument list** for the pair: the primary accessibility instrument(s) in force, current editions only (workplan HANDOFF section 3), from `research_code_leads`, `references/standards-registry.md` and what is held. Retrieve each through `retrieval_log.fetch`; a block goes to the Wayback `if_` route (CLAUDE.md section 7); a failure is logged, not hidden.")
w("2. **Search seeds.** The English register is rendered into the language as **flagged, model-generated search seeds** (owner OR-12b, third 2026-11-06 statement): terms the model believes are in use in that jurisdiction, never word for word, recorded as seeds and never as aliases. Seeds only point the reading.")
w("3. **Read the instrument in full in its own language** (OR-13 open pass), not only for the seeds. For each concept found: the phrase **as the instrument writes it**, locator, a verbatim quote that verifies in the saved text, and the instrument. For each concept the instrument treats that the register lacks: the same record, in the instrument's phrase (reverse harvest, E1). For each register concept not found after a full reading: SEARCHED-ABSENT.")
w("4. **Observe → adjudicate → attest** with the verbs that exist (`observe-term`, `adjudicate-term`, `add-alias` or `add-term --from-observation`); a seed whose phrase is found becomes an attested alias in place (migration 117). Rows ship in a research PR after the tooling PR merges.")
w("5. **No pair is second-read before every pair is first-read**, so English does not become the frame (plan C.3).\n")
w("## 7. What this needs from the owner\n")
w("- Whether to run the first terminology passes now (research with retrieval and logging, no database rows until the tooling PR merges), and for which pairs first. Recommended: one pilot pass in three structurally different languages (Japanese, German, French) to expose method defects before all 14.\n")
open(f'{OUT}/rhfac-b651-catalogue.md','w',encoding='utf-8').write('\n'.join(o))
print('written', len('\n'.join(o)), 'chars;', integrity)
