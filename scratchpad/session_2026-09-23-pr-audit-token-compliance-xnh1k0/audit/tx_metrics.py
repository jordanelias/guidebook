import json, glob, os, collections, re, sys
rows=[]
def scan(path):
    u=collections.Counter(); tools=collections.Counter(); skills=collections.Counter(); agents=collections.Counter()
    first=last=None; branch=None; prompt=None; nturns=0; bash_cmds=collections.Counter(); seen=set()
    big_results=0; result_bytes=0; reads=0; ctxmax=0; models=collections.Counter()
    for line in open(path, errors='replace'):
        try: r=json.loads(line)
        except: continue
        ts=r.get('timestamp'); 
        if ts: first=first or ts; last=ts
        if r.get('gitBranch') and not branch: branch=r['gitBranch']
        if r.get('type')=='queue-operation' and r.get('content') and not prompt: prompt=r['content'][:160]
        if r.get('type')=='user' and not prompt:
            c=(r.get('message') or {}).get('content')
            if isinstance(c,str): prompt=c[:160]
        if r.get('type')=='user':
            c=(r.get('message') or {}).get('content')
            if isinstance(c,list):
                for x in c:
                    if isinstance(x,dict) and x.get('type')=='tool_result':
                        s=json.dumps(x.get('content'))
                        result_bytes+=len(s)
                        if len(s)>20000: big_results+=1
        if r.get('type')=='assistant':
            m=r.get('message') or {}
            mid=m.get('id')
            if mid and mid in seen: 
                # usage repeated per content block; count once
                pass
            else:
                seen.add(mid); nturns+=1
                us=m.get('usage') or {}
                for k in ('input_tokens','output_tokens','cache_read_input_tokens','cache_creation_input_tokens'):
                    u[k]+=us.get(k) or 0
                ctx=(us.get('input_tokens') or 0)+(us.get('cache_read_input_tokens') or 0)+(us.get('cache_creation_input_tokens') or 0)
                ctxmax=max(ctxmax,ctx)
                models[m.get('model')]+=1
            for c in m.get('content') or []:
                if c.get('type')=='tool_use':
                    n=c['name']; tools[n]+=1; i=c.get('input') or {}
                    if n=='Skill': skills[i.get('skill')]+=1
                    if n in('Agent','Task'): agents[i.get('subagent_type') or 'general']+=1
                    if n=='Bash':
                        cmd=(i.get('command') or '').strip()
                        m2=re.findall(r'(scripts/[\w/.-]+\.(?:py|sh))',cmd)
                        for s in m2: bash_cmds[s]+=1
                        if re.match(r'^(cat|head|sed -n|grep|rg|find|ls)\b',cmd): bash_cmds['<shell-read:'+cmd.split()[0]+'>']+=1
    return dict(u=u,tools=tools,skills=skills,agents=agents,first=first,last=last,branch=branch,prompt=prompt,turns=nturns,bash=bash_cmds,big=big_results,rbytes=result_bytes,ctxmax=ctxmax,models=models)
out={}
for d in sorted(glob.glob('transcripts/harness_*')):
    main=scan(d+'/main.jsonl')
    subs=[scan(p) for p in glob.glob(d+'/subagents/*.jsonl')]
    idx=json.load(open(d+'/index.json')) if os.path.exists(d+'/index.json') else []
    su=collections.Counter()
    for s in subs: su.update(s['u'])
    out[os.path.basename(d)]=dict(main=main,subs=len(subs),sub_u=su,roles=collections.Counter(i.get('role') for i in idx))
for k,v in out.items():
    m=v['main']; u=m['u']; su=v['sub_u']
    tot=lambda c: c['input_tokens']+c['cache_read_input_tokens']+c['cache_creation_input_tokens']+c['output_tokens']
    print(f"== {k} {m['first'][:16] if m['first'] else ''}→{m['last'][:16] if m['last'] else ''} branch={m['branch']}")
    print(f"  prompt: {m['prompt']!r}")
    print(f"  main turns={m['turns']} ctxmax={m['ctxmax']} out={u['output_tokens']} cread={u['cache_read_input_tokens']/1e6:.1f}M cwrite={u['cache_creation_input_tokens']/1e6:.2f}M  | subs={v['subs']} roles={dict(v['roles'])} sub_cread={su['cache_read_input_tokens']/1e6:.1f}M sub_out={su['output_tokens']}")
    print(f"  models={dict(m['models'])}")
    print(f"  tools={dict(m['tools'].most_common(12))}")
    print(f"  skills={dict(m['skills'])} agents={dict(m['agents'])} bigresults={m['big']} resultMB={m['rbytes']/1e6:.1f}")
    print(f"  scripts={dict(m['bash'].most_common(14))}")
