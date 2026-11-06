#!/usr/bin/env python3
"""Digest CSA/ASC B651:23 BY HEADERS ONLY: its table of contents, its defined-term names, and the
headings of its informative annexes. No clause text and no value is copied (the standard's legal
notice forbids making an electronic copy; the PDF is kept out of git, see the catalogue).
Input: pdftotext -layout of the owner-supplied PDF (retrieval-log artefact 4fae63595a101516.pdf)."""
import re, json, collections, sys
sys.path.insert(0,'/tmp/claude-0/-home-user-guidebook/85c53b12-0695-5c1e-b998-83da3eff20b4/scratchpad/build')
SCR='/tmp/claude-0/-home-user-guidebook/85c53b12-0695-5c1e-b998-83da3eff20b4/scratchpad'
OUT='/home/user/guidebook/scratchpad/session_2026-11-06-base-vocabulary-review'
L=[l.strip() for l in open(f'{SCR}/b651_clean.txt',encoding='utf-8')]
start=next(i for i,l in enumerate(L) if l=='Contents'); end=next(i for i,l in enumerate(L) if i>start and l.startswith('Technical Committee on')and not l.endswith(' 8'))
toc=[];pend=None
for l in L[start:end]:
    if re.match(r'^(January 2023|CSA/ASC B651:23)',l): continue
    m=re.match(r'^((?:Annex [A-F]|\d{1,2}(?:\.\d{1,2}){0,2}))\s+(.+?)\s+(\d{1,3})$',l)
    if m: 
        title=m.group(2)
        if pend: title=pend+' '+title; pend=None
        toc.append((m.group(1),title,int(m.group(3)))); continue
    m2=re.match(r'^((?:Annex [A-F]|\d{1,2}(?:\.\d{1,2}){0,2}))\s+(.+)$',l)
    if m2 and not re.search(r'\d$',l): pend=m2.group(2)+('' ); toc.append(None) if False else None; pend_code=m2.group(1); continue
    if pend and not re.match(r'^\d',l):
        title=pend+' '+re.sub(r'\s+\d{1,3}$','',l); pg=re.search(r'(\d{1,3})$',l)
        toc.append((pend_code,title,int(pg.group(1)) if pg else 0)); pend=None
# Annex sub-headings from the body (informative annexes carry their own numbered headings)
body=[(i,l) for i,l in enumerate(L)]
annex=[]
for i,l in body:
    m=re.match(r'^([A-F]\.\d{1,2}(?:\.\d{1,2})?)\s+([A-Z][^.]{2,90})$',l)
    if m and i>1200: annex.append((m.group(1),m.group(2),0))
seen=set(); heads=[]
for c,t,p in toc+annex:
    if (c,t) in seen: continue
    seen.add((c,t)); heads.append((c,t,p))
# defined terms (names only), from clause 3.1
d0=next(i for i,l in enumerate(L) if l=='3.1 Definitions' and i>800); d1=next(i for i,l in enumerate(L) if l.startswith('3.2 Abbreviations') and i>d0)
terms=[]
for l in L[d0:d1]:
    m=re.match(r'^([A-Z][A-Za-z()/’\' ,-]{2,70}?) — ',l)
    if m: terms.append(m.group(1).strip())
json.dump({'headings':heads,'terms':terms},open(f'{SCR}/build/b651.json','w'),ensure_ascii=False)
FAM={'0':'introduction','1':'scope','2':'references','3':'definitions','4':'general requirements (technique clauses)','5':'interior circulation','6':'interior facilities','7':'residential accommodation','8':'exterior circulation, spaces and amenities','9':'vehicular access','A':'annex A anthropometrics','B':'annex B slip potential','C':'annex C residential references','D':'annex D trails and beach access','E':'annex E outdoor recreation references','F':'annex F other resources'}
def fam(c): return FAM.get(c.split('.')[0].replace('Annex ',''),'?')
import importlib.util
sp=importlib.util.spec_from_file_location('b','/home/user/guidebook/scratchpad/session_2026-11-06-base-vocabulary-review/tools/build.py')
# reuse the technique rules without executing build.py's main body: copy the TAGS list by exec of that block
src=open('/home/user/guidebook/scratchpad/session_2026-11-06-base-vocabulary-review/tools/build.py').read()
tags_src=src[src.index('TAGS=['):src.index('def tags(text)')]
ns={'re':re}; exec(tags_src,ns); TAGS=ns['TAGS']
def tags(t): return [n for n,rx in TAGS if re.search(rx,t.lower())]
# RHFAC overlap by 5-letter stems of content words
rh=json.load(open(f'{SCR}/build/criteria.json'))
stem=lambda w:w[:5]
rhs={stem(w) for r in rh for w in re.findall(r'[a-z]{5,}',(r['text']+' '+r['section_title']).lower())}
STOP={'general','scope','floor','area','allowances','surfaces','requirements','locations','location','generic','features','design','other'}
def novel(t):
    ws=[w for w in re.findall(r'[a-z]{5,}',t.lower()) if w not in STOP]
    return bool(ws) and not any(stem(w) in rhs for w in ws)
rows=[(c,t,p,fam(c),';'.join(tags(t)),'RHFAC-does-not-name' if novel(t) else '') for c,t,p in heads if c.split('.')[0] not in ('0','1','2','3')]
with open(f'{OUT}/b651-headings.tsv','w',encoding='utf-8') as f:
    f.write('clause\theading (as the TOC words it)\tpage\tclause family\ttechnique tags (rule-assigned lead)\trhfac_overlap (crude word-stem test)\n')
    for r in rows: f.write('\t'.join(map(str,r))+'\n')
nov=[r for r in rows if r[5]]
fm=collections.Counter(r[3] for r in rows)
o=[]; w=o.append
w(f"**Read by headers only** (owner instruction): the table of contents, the {len(terms)} defined-term names of clause 3.1, clause 1.6 (the shall/should/may convention), the three headings and opening lines of 4.7 (functional and cognitive barriers; environmental intolerances; acoustics), and the headings of Annexes A to F. The standard's body clauses were not read, so **no dimension, force, slope or time is recorded here** and none should be inferred. Full heading list with pages: `b651-headings.tsv` ({len(rows)} headings, generated by `tools/b651.py`).\n")
w("**Document facts (title page and revision block):** CSA/ASC B651:23, National Standard of Canada, 'Accessible design for the built environment', January 2023, REVISED JUNE 2025 (errata to clause 5.2.2, Tables 8 a) to d) and Figures 20 a) to d); earlier errata of July 2023 to clauses 1.4, 5.5.1, 6.8.2, 9.4.1 and A.10); 283 pages; English and French editions exist; developed under Accessibility Standards Canada with a technical committee that includes persons with disabilities; the document says it focuses on national and international best practice 'as opposed to focusing on minimum technical requirements'; clause 1.6 separates requirement, recommendation and option by 'shall', 'should' and 'may', and Annexes A to F are informative.\n")
w("**Legal notice:** the PDF's notice allows loading for review, search, browse and print, and says users may not 'make an electronic copy of this document'. The retrieval log's rule that every source be persisted (R10) conflicts with that for this one file. **The PDF is therefore not committed**: it is excluded locally (`.git/info/exclude`) and only its retrieval line, sha256 and this heading-level digest are kept. Whether the project may hold the PDF in the repository is a licensing question for the owner (DG-NON).\n")
w("### B651 clause families (heading counts, computed)\n")
w("| Clause family | Headings |\n|---|---|")
for k,v in fm.items(): w(f"| {k} | {v} |")
w("\n### B651 headings the RHFAC survey does not name (crude word-stem test; a lead for the register, not a judgement)\n")
w("| Clause | Heading | Family | Technique tags |\n|---|---|---|---|")
for r in nov: w(f"| {r[0]} | {r[1]} | {r[3]} | {r[4]} |")
w("\n### B651 defined terms (names as the standard writes them; Canadian English)\n")
w(', '.join(terms)+'.\n')
w("**The overlap test is crude and over-reports gaps** (it matches word stems, so 'Headroom' is flagged although RHFAC's 'Height clearance' is the same concept in other words). **What the digest shows.** B651 frames the *exterior and public realm* far more fully than RHFAC (pedestrian crossings, intersections, transit stops, urban furniture, landscaping, temporary works, trails and beach access in Annex D), treats several technique topics as clauses of their own where RHFAC scores them as single criteria (luminance contrast with a formula and a light-reflectance definition, tactile walking surface indicators, headroom and protruding objects, door-opening force, power-assisted doors, handrail grip, slip potential in Annex B), and puts the human body into the standard through Annex A (reach ranges, walkway widths for crutch users, the detection space for a long white cane, a service dog, dimensions of wheeled mobility devices, turning areas). Clause 4.7 names functional and cognitive barriers, environmental intolerances and acoustics as 'additional considerations' in recommendation form, which is the same ground as RHFAC chapter 11 and criteria 4.5 and 4.6. Whether other jurisdictions' instruments frame those topics as clauses, as recommendations or not at all is exactly what the native-language readings must find out.\n")
open(f'{OUT}/b651-digest.md','w',encoding='utf-8').write('\n'.join(o))
print(len(heads),'headings;',len(rows),'rows;',len(terms),'terms;',len(nov),'not named by RHFAC')
