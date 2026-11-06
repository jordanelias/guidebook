import re, json, sys
SCR='/tmp/claude-0/-home-user-guidebook/85c53b12-0695-5c1e-b998-83da3eff20b4/scratchpad'
def parse(path, nolayout_noise=()):
    L=[l.rstrip() for l in open(path,encoding='utf-8')]
    rows=[];cur=None
    crit=re.compile(r'^\s*(\d{1,2}\.\d{1,2}[A-Z]?\.\d{1,2})\s+(.*?)\s+(\d{1,2}|Oui/Non|Yes/No)\s*$')
    crit0=re.compile(r'^\s*(\d{1,2}\.\d{1,2}[A-Z]?\.\d{1,2})\s+(.*)$')
    for ln in L:
        s=ln.strip()
        if not s or re.match(r'^[—\-–] ',s) or re.match(r'^(Maximum|Points|Total|Note)',s) or 'V4.0' in s or 'v 4.0' in s or re.match(r'^\d{1,3}$',s):
            if s.startswith('Total'): cur=None
            continue
        m=crit.match(s)
        if m:
            cur={'code':m.group(1),'text':m.group(2).strip(),'points':m.group(3)}; rows.append(cur); continue
        m=crit0.match(s)
        if m:
            cur={'code':m.group(1),'text':m.group(2).strip(),'points':None}; rows.append(cur); continue
        if cur is not None and not re.match(r'^\d{1,2}\.\d{1,2}\s',s) and not re.match(r'^\d{1,2}\.\s',s):
            mm=re.match(r'^(.*?)\s+(\d{1,2})$',s)
            if mm and cur['points'] is None: cur['text']+=' '+mm.group(1); cur['points']=mm.group(2)
            else: cur['text']+=' '+s
    return rows
if __name__=='__main__':
    en=parse(f'{SCR}/rhfac_clean.txt'); fr=parse(f'{SCR}/rhfac_fr_clean.txt')
    print(len(en),len(fr))
    ce={r['code'] for r in en}; cf={r['code'] for r in fr}
    print('en-only',sorted(ce-cf)[:30]); print('fr-only',sorted(cf-ce)[:30])
    dup=[c for c in ce if sum(1 for r in en if r['code']==c)>1]; print('dup en',dup[:10])
    print([r for r in fr if r['code'] in ('3.3.3','3.3.6','8.2.9')])
    json.dump({'en':en,'fr':fr},open(f'{SCR}/build/rows.json','w'),ensure_ascii=False)
