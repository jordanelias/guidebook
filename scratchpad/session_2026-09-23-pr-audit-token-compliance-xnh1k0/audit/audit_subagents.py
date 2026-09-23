# Subagent brief overlap (6-gram Jaccard of first user message) and report delivery. Run from repo root.
import json,glob,re,collections
def sh(t):
    w=re.findall(r'\w+',t.lower()); return {' '.join(w[k:k+6]) for k in range(max(0,len(w)-5))}
T=collections.Counter(); OV=0; OVT=0; ND=0; NDT=0; N=0
for d in sorted(glob.glob('transcripts/harness_*')):
    sid=d.split('_')[-1]
    if sid=='37f845b8': continue
    subs=[]
    for f in sorted(glob.glob(d+'/subagents/*.jsonl')):
        brief=None; tok=0; seen=set(); hb=0; last=''
        for l in open(f,errors='replace'):
            r=json.loads(l)
            if r.get('type')=='user' and brief is None:
                c=r['message']['content']; brief=c if isinstance(c,str) else ' '.join(x.get('text','') for x in c if isinstance(x,dict))
            if r.get('type')=='assistant':
                m=r['message']; 
                if m.get('id') not in seen:
                    seen.add(m.get('id')); u=m.get('usage') or {}; tok+=sum(u.get(k) or 0 for k in ('input_tokens','cache_read_input_tokens','cache_creation_input_tokens','output_tokens'))
                for c in m.get('content') or []:
                    if c.get('type')=='tool_use' and c['name'] in ('SubagentHandback','SendMessage'): hb=max(hb,len(json.dumps(c['input'])))
                    if c.get('type')=='text': last=c['text']
        role=re.sub(r'^[\dT-]+_|_[0-9a-f]+\.jsonl$','',f.split('/')[-1])
        subs.append(dict(f=f.split('/')[-1],brief=brief or '',tok=tok,report=max(hb,len(last)),role=role,sh=sh(brief or '')))
    pairs=[]
    for i in range(len(subs)):
        for j in range(i+1,len(subs)):
            a,b=subs[i]['sh'],subs[j]['sh']
            if a and b:
                jac=len(a&b)/len(a|b)
                if jac>0.25: pairs.append((subs[i]['f'][:19],subs[i]['role'],subs[j]['f'][:19],subs[j]['role'],round(jac,2),subs[j]['tok']))
    nodeliv=[s for s in subs if s['report']<200]
    N+=len(subs); ND+=len(nodeliv); NDT+=sum(s['tok'] for s in nodeliv)
    later=set(p[2] for p in pairs); OV+=len(later); OVT+=sum(s['tok'] for s in subs if s['f'][:19] in later)
    for s in subs: T[s['role']]+=s['tok']
    print(f"{sid} subagents={len(subs)} tokens={sum(s['tok'] for s in subs)/1e6:.1f}M no-report(<200 chars)={len(nodeliv)} overlapping-brief pairs(J>0.25)={len(pairs)}")
    for p in pairs: print('    ',p[:5], f'{p[5]/1e6:.1f}M')
print('TOTAL subagents',N,'no report',ND,f'{NDT/1e6:.1f}M','later-of-overlapping-pair',OV,f'{OVT/1e6:.1f}M')
print('tokens by role', {k:f'{v/1e6:.1f}M' for k,v in T.most_common()})
