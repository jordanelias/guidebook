import json,sys,re
# sequence of search vs log-search events
def events(path):
    for line in open(path,errors='replace'):
        try: r=json.loads(line)
        except: continue
        if r.get('type')!='assistant': continue
        for c in (r.get('message') or {}).get('content') or []:
            if c.get('type')!='tool_use': continue
            n=c['name']; i=c.get('input') or {}
            ts=r.get('timestamp','')[:19]
            if n=='Bash':
                cmd=i.get('command','')
                if re.search(r'db\.py[^|;&]*\blog-search\b',cmd): yield ts,'LOG',len(re.findall(r'log-search',cmd)), 'prior' in cmd
                elif re.search(r'retrieval_log\.py',cmd) or re.search(r'curl[^|]*(crossref|eutils|ncbi|openalex|semanticscholar|archive\.org|eric\.ed|hathitrust|openlibrary|googleapis)',cmd): yield ts,'SEARCHBASH',1,None
            elif n in('WebSearch',) or n.startswith('mcp__PubMed__search') or n.startswith('mcp__Consensus') or n.startswith('mcp__Scholar'):
                yield ts,'SEARCH:'+n.split('__')[-1],1,None
            elif n=='WebFetch': yield ts,'FETCH',1,None
for p in sys.argv[1:]:
    ev=list(events(p))
    s=''.join({'LOG':'L','FETCH':'f','SEARCHBASH':'b'}.get(e[1],'S') for e in ev)
    firstlog=next((i for i,e in enumerate(ev) if e[1]=='LOG'),None)
    pre=[e for e in ev[:firstlog] if e[1]!='LOG'] if firstlog is not None else ev
    print(p.split('/')[-2], 'events',len(ev),'logs',sum(e[2] for e in ev if e[1]=='LOG'),'searches(S)',sum(1 for e in ev if e[1].startswith('SEARCH:')),'searches_before_first_log',sum(1 for e in pre if e[1].startswith('SEARCH:')),'fetch_before_first_log',sum(1 for e in pre if e[1]=='FETCH'))
    print('   seq:',s[:200])
    if firstlog is not None: print('   first log',ev[firstlog][0],'first search', next((e[0] for e in ev if e[1].startswith('SEARCH:')),None))
