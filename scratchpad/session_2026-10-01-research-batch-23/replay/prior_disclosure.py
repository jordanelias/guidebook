import os, subprocess, sqlite3
SCR='/tmp/claude-0/-home-user-guidebook/5b214a57-ade4-5889-9a78-ce2de4360478/scratchpad'
S='session_2026-10-01-research-batch-23'
pre=set()
for line in open(SCR+'/priors.txt'):
    if ':' in line and line.split(':')[0] in ('KR','SG','PT','EU','FR','ES','NL','SE','AU','CO1-KR'): pre.add(line.split(':',1)[1].strip())
con=sqlite3.connect('file:%s/batch23.db?mode=ro'%SCR,uri=True)
rows=con.execute("select exec_id,prior_expectation from search_executions where created_by_session=? order by exec_id",(S,)).fetchall()
def run(args):
    r=subprocess.run(['python3','scripts/db.py']+args,env=dict(os.environ,GUIDEBOOK_DB_PATH=SCR+'/batch23.db'),capture_output=True,text=True)
    return r.returncode,(r.stdout+r.stderr).strip().splitlines()[-2:]
n=0;skipped=0
for eid,p in rows:
    p=(p or '').strip()
    if p in pre or p.startswith('No pre-registered prior') or p.startswith('BACKFILLED'):
        skipped+=1; continue
    rc,o=run(['amend-search','--exec-id',str(eid),'--append-note',"PRIOR DISCLOSURE (adversarial pass F4): this row's prior_expectation was COMPOSED AT LOGGING TIME, after the search or fetch had been run and its result read; it describes what was then expected given the preceding result and is NOT a pre-registered prior. Only the first-search priors for KR, SG, PT, EU, FR, ES, NL, SE, AU and the Korean Co-1 query were written before any search ran (priors.txt, written 02:36:01 UTC; first WebSearch about 02:36:03 UTC). All search rows of this batch were logged after the fact, in one pass.",'--session',S])
    n+=1
    if rc: print(eid,rc,o)
print('disclosure appended to',n,'execs; left alone',skipped)
for eid,q in con.execute("select exec_id,query_text from search_executions where created_by_session=? and (query_text like '%fub.se%' or query_text like '%madrid.es/Unidades%')",(S,)).fetchall():
    print(eid,q[:50],run(['amend-search','--exec-id',str(eid),'--append-note',"R5 RETARGET DISCLOSURE (adversarial pass F9): the grey -> co1 change above was made AFTER research_batch_dod R5 reported these execs. R5's rationale concerns non-English PEER-REVIEWED work, and neither document is peer-reviewed, so the R5 failure was arguably a false positive and a reasoned waiver was the honest route; the edit was nonetheless gate-driven. The earlier Co-1-channel exec for each document had already recorded it as Co-1-ADJACENT (FUB) or as a Co-1 DPO-sector question (CERMI) before this fetch was logged.",'--session',S]))
