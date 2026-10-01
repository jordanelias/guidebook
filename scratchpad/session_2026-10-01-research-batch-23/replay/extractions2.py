import os, subprocess, sys
sys.path.insert(0,'scripts/research')
import retrieval_log as rl
SCR='/tmp/claude-0/-home-user-guidebook/5b214a57-ade4-5889-9a78-ce2de4360478/scratchpad'
S='session_2026-10-01-research-batch-23'
SLUG='accessible-circulation-geometry'
E=[]
def add(ref, juris, ctype, cv, unit, cmp_, role, text, section, notes, locs, device='not_device_scoped'):
    E.append(dict(ref=ref,juris=juris,ctype=ctype,cv=cv,unit=unit,cmp=cmp_,role=role,text=text,section=section,notes=notes,locs=locs,device=device))
kr_src=" OFFICIAL TEXT: the law.go.kr download (PDF author '법제처 국가법령정보센터', file created 2026-03-31, 22 pp.) under the stamp <개정 2023. 12. 11.>; it reads identically to the NEPLA mirror admitted as REF-01019 for item 12 and the 비고, which is why REF-01019's rows are re-rooted here. The issuing ministry is not named in the Annex text itself."
add('REF-01031','KR','numerical','1:12','rise:run ratio (maximum; the rule writes 12분의 1)','<=','claim',
 '경사로의 기울기는 12분의 1 이하로 하여야 한다.','별표 1 제12호 나목(1) (PDF p. 10)',
 "MANDATORY WORDING: '하여야 한다' (shall). A DISTINCT ELEMENT NOT EXTRACTED: item 1 나목(1) sets the gradient of an 접근로 (approach path) at 18분의 1 or less, relaxable to 12분의 1 where terrain makes that difficult -- an approach path, not a 경사로 (ramp); route-vs-ramp scope is GAP-033's open question."+kr_src,
 dict(scheme='section',section='별표 1 제12호',subsection='나',paragraph='1'))
add('REF-01031','KR','numerical','1:8','rise:run ratio (conditional relaxation ceiling; all three conditions required)','<=','condition',
 '다음의 요건을 모두 충족하는 경우에는 경사로의 기울기를 8분의 1까지 완화할 수 있다. (가) 신축이 아닌 기존시설에 설치되는 경사로일 것 (나) 높이가 1미터 이하인 경사로로서 시설의 구조 등의 이유로 기울기를 12분의 1이하로 설치하기가 어려울 것 (다) 시설관리자 등으로부터 상시보조서비스가 제공될 것',
 '별표 1 제12호 나목(2) (PDF p. 10)',
 "THE ONLY RELAXATION IN THE RULE IS CONDITIONED ON HUMAN ASSISTANCE. All of: (가) an existing, not new, facility; (나) ramp height 1 m or less and 1/12 structurally difficult; (다) continuous assistance service provided by the facility manager (상시보조서비스). No other source in this corpus makes a steeper ramp conditional on a staffing provision. STATUS OF THE VERB IS LEFT OPEN: the Annex's own 비고 (PDF p. 22) says items phrased '…할 수 있다' are 권장사항 (recommendations), and this clause is phrased '완화할 수 있다'; whether the 비고 was written to cover a relaxation permission is not stated in the text, so neither 'permission' nor 'recommendation' is asserted here."+kr_src,
 dict(scheme='section',section='별표 1 제12호',subsection='나',paragraph='2'))
pt_note=" OFFICIAL ORIGINAL: Diário da República, 1.ª série, N.º 152, 8 de Agosto de 2006, DR p. 5678 (PDF p. 9 of 20); the text reads identically to the Ordem dos Arquitectos transcription admitted as REF-01026, whose rows are re-rooted here. CURRENCY NOT ESTABLISHED: the decree has been amended by DL 136/2014 (9 Sept), DL 125/2017 (4 Oct), DL 95/2019 (18 July) and DL 10/2024 (8 Jan) per the PGDL consolidation page retrieved this session (five versions listed); that page's Anexo node did not load, so whether any amendment altered Anexo 2.5 is UNVERIFIED. Portugal has no JurisdictionCode value (jurisdiction_db_vocabulary class, left to the owner and not yet decided). Lead-in of 2.5.1: 'As rampas devem ter a menor inclinação possível'."
add('REF-01032','PT','numerical','6%','% longitudinal gradient (maximum) where the rise is <= 0.6 m and the horizontal projection <= 10 m; interpolated values permitted','<=','claim',
 '1) Ter uma inclinação não superior a 6 %, vencer um desnível não superior a 0,6 m e ter uma projecção horizontal não superior a 10 m;','Anexo, 2.5.1 1)',
 "TIERED BY RISE AND RUN, with explicit permission to use interpolated values ('ou valores interpolados dos indicados')."+pt_note,
 dict(scheme='section',section='Anexo 2.5',subsection='2.5.1',paragraph='1'))
add('REF-01032','PT','numerical','8%','% longitudinal gradient (maximum) where the rise is <= 0.4 m and the horizontal projection <= 5 m; interpolated values permitted','<=','claim',
 '2) Ter uma inclinação não superior a 8 %, vencer um desnível não superior a 0,4 m e ter uma projecção horizontal não superior a 5 m.','Anexo, 2.5.1 2)',
 "SECOND TIER OF THE NEW-BUILD RULE (steeper for shorter, lower ramps)."+pt_note,
 dict(scheme='section',section='Anexo 2.5',subsection='2.5.1',paragraph='2'))
add('REF-01032','PT','numerical','12%','% longitudinal gradient (maximum) in buildings under alteration or conservation only, where the rise is <= 0.1 m and the projection <= 0.83 m; a 10% step allows rise <= 0.2 m and projection <= 2 m','<=','condition',
 'No caso de edifícios sujeitos a obras de alteração ou conservação, se as limitações de espaço impedirem a utilização de rampas com uma inclinação não superior a 8%, as rampas podem ter inclinações superiores se satisfizerem uma das seguintes situações ou valores interpolados dos indicados: 1) Ter uma inclinação não superior a 10%, vencer um desnível não superior a 0,2 m e ter uma projecção horizontal não superior a 2 m; 2) Ter uma inclinação não superior a 12%, vencer um desnível não superior a 0,1 m e ter uma projecção horizontal não superior a 0,83 m.','Anexo, 2.5.2',
 "EXISTING-BUILDING CONCESSION, available only where space prevents 8%."+pt_note,
 dict(scheme='section',section='Anexo 2.5',subsection='2.5.2'))
for i,e in enumerate(E):
    f,w=rl.quote_in_artefacts(e['text'],ref_id=e['ref'])
    print(i,e['ref'],'FOUND' if f else 'MISSING', 'scoped' if f and ('retrieved for '+e['ref']) in w else w[:80],flush=True)
    if not f: continue
    cmd=['python3','scripts/db.py','add-extraction','--ref-id',e['ref'],'--slug',SLUG,'--parameter-id','3','--identity','MOB','--claim-type',e['ctype'],'--claimed-value',e['cv'],'--claimed-unit',e['unit'],'--claim-text',e['text'],'--source-section',e['section'],'--jurisdiction',e['juris'],'--extraction-method','full-read','--extraction-status','preliminary','--root-type','committee_assertion','--root-ref-id',e['ref'],'--measurement-paradigm','stated_unmeasured','--device-class',e['device'],'--figure-role',e['role'],'--comparator',e['cmp'],'--relation','none','--notes',e['notes'],'--session',S,'--locator-scheme',e['locs']['scheme']]
    for k,flag in (('section','--loc-section'),('subsection','--loc-subsection'),('paragraph','--loc-paragraph')):
        if k in e['locs']: cmd+=[flag,e['locs'][k]]
    r=subprocess.run(cmd,env=dict(os.environ,GUIDEBOOK_DB_PATH=SCR+'/batch23.db'),capture_output=True,text=True)
    print('   ->',r.returncode,' | '.join((r.stdout+r.stderr).strip().splitlines()[-3:])[:260],flush=True)
