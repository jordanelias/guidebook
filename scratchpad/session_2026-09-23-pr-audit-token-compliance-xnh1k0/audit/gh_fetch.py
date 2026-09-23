import json, subprocess, sys
def get(url):
    out = subprocess.run(['curl','-sS','-H','Accept: application/vnd.github+json',url],capture_output=True,text=True).stdout
    return json.loads(out)
def gql(q):
    out = subprocess.run(['curl','-sS','-X','POST','https://api.github.com/graphql','-d',json.dumps({'query':q})],capture_output=True,text=True).stdout
    return json.loads(out)
R='https://api.github.com/repos/jordanelias/guidebook'
res={}
for n in range(116,158):
    pr=get(f'{R}/pulls/{n}')
    sha=pr['head']['sha']
    cr=get(f'{R}/commits/{sha}/check-runs?per_page=100')
    st=get(f'{R}/commits/{sha}/status')
    rv=get(f'{R}/pulls/{n}/reviews?per_page=100')
    ic=get(f'{R}/issues/{n}/comments?per_page=100')
    res[n]=dict(pr={k:pr.get(k) for k in ['number','title','merged','merged_at','merged_by','base','head','body','created_at','commits','review_comments','comments','mergeable_state','merge_commit_sha']},
               checks=[{k:c.get(k) for k in ['name','status','conclusion','started_at','completed_at','app']} for c in cr.get('check_runs',[])],
               status=st.get('state'), statuses=[{k:s.get(k) for k in ['context','state','updated_at']} for s in st.get('statuses',[])],
               reviews=[{k:r.get(k) for k in ['state','submitted_at','body']}|{'user':r['user']['login']} for r in rv] if isinstance(rv,list) else rv,
               comments=[{'user':c['user']['login'],'created_at':c['created_at'],'body':c['body'][:400]} for c in ic] if isinstance(ic,list) else ic)
    q='{repository(owner:"jordanelias",name:"guidebook"){pullRequest(number:%d){reviewThreads(first:100){nodes{isResolved isOutdated comments(first:1){nodes{author{login} body createdAt}}}}}}}'%n
    g=gql(q)
    try: res[n]['threads']=g['data']['repository']['pullRequest']['reviewThreads']['nodes']
    except Exception as e: res[n]['threads']=str(g)[:300]
    for k in ('app',):
        for c in res[n]['checks']: c['app']=(c['app'] or {}).get('slug')
    res[n]['pr']['base']=pr['base']['ref']; res[n]['pr']['head']=pr['head']['ref']+'@'+sha[:8]
    res[n]['pr']['merged_by']=(pr.get('merged_by') or {}).get('login')
    print(n, file=sys.stderr)
json.dump(res,open('gh/prs.json','w'),indent=1)
