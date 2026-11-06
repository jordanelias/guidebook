import sys, re
sys.path.insert(0, sys.argv[1]); import obs_data as d
T=sys.argv[2]
def norm(s): return re.sub(r'[ 　\t]+',' ',s)
cache={}
def check(f,q):
    if f not in cache:
        raw=open(f'{T}/{d.F[f]}',encoding='utf-8').read(); cache[f]=(raw,norm(raw))
    raw,n=cache[f]
    if q in raw: return 'exact'
    if norm(q) in n: return 'ws-normalised'
    j=re.sub(r'\n[ \u3000]*','',raw)
    if q in j: return 'line-joined'
    return 'MISSING'
bad=0
for o in d.OBS:
    r=check(o[2],o[4]); ph = o[1] in o[4]
    if r=='MISSING' or not ph: bad+=1; print('OBS', r, 'phrase_in_quote=',ph, o[:4])
for o in d.RH:
    r=check(o[1],o[3]); ph=o[0] in o[3]
    if r=='MISSING' or not ph: bad+=1; print('RH', r, 'phrase_in_quote=',ph, o[:3])
print('bad',bad,'obs',len(d.OBS),'rh',len(d.RH))
