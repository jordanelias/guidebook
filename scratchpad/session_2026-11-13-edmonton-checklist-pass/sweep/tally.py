import json,collections,sys,os
tot=collections.Counter(); sense=collections.Counter(); flag=collections.Counter(); per={}
miss=[]
for i in range(1,8):
    hits=[l.rstrip('\n') for l in open(f'part-{i}.hits')]
    if not os.path.exists(f'out-{i}.jsonl'): miss.append(i); continue
    recs=[json.loads(l) for l in open(f'out-{i}.jsonl')]
    ok=len(hits)==len(recs) and all(h.startswith(f"{r['file']}:{r['line']}:") for h,r in zip(hits,recs))
    per[i]=(len(hits),len(recs),ok,collections.Counter(r['flag'] for r in recs))
    for r in recs: sense[r['sense']]+=1; flag[r['flag']]+=1
print('missing parts',miss)
for i,(h,r,ok,f) in per.items(): print(i,h,r,'aligned' if ok else 'MISALIGNED',dict(f))
print('records',sum(sense.values()),dict(sense.most_common()));print(dict(flag.most_common()))
