import json, re, collections
D='/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad/edm/'
rows=json.load(open(D+'spans.json'))
# keep pages 1..8 (checklist), reading order = (page, y)
rows=[r for r in rows if r[0]>=1]
items=collections.OrderedDict(); cur=None; sec=None
NAME={'025087':'CODE','9e2064':'BEST','ffffff':'HDR'}
for pno,y,col,t in rows:
    if col=='ffffff':
        m=re.match(r'^(\d+)\.\s+([A-Z/ ]+)',t.strip())
        if m: sec=(m.group(1),m.group(2).strip())
        continue
    m=re.match(r'^(\d+\.\d+)\s+(.*)$',t.strip())
    if m:
        cur=m.group(1); items[cur]={'sec':sec,'page':pno,'segs':[]}
        t=m.group(2)
    if cur is None: continue
    segs=items[cur]['segs']
    if segs and segs[-1][0]==NAME[col]: segs[-1][1]+=' '+t.strip()
    else: segs.append([NAME[col],t.strip()])
json.dump(items,open(D+'items.json','w'),indent=1,ensure_ascii=False)
for k,v in items.items():
    print(k,'|',' ‖ '.join(f'[{c}] {s}' for c,s in v['segs']))
