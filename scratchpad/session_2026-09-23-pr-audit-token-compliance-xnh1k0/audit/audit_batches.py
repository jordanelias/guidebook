# Research-batch session comparison: tokens per unit of research output, and where each session's tokens went.
import json,re,collections,sys
sys.argv=['x']; 
pr=json.load(open(sys.path[0] and __file__.rsplit('/',1)[0]+'/pr_info.json'))
tok=json.load(open(__file__.rsplit('/',1)[0]+'/audit_tokens.json'))
batches={'e124fa82':'08','2aa77402':'09','cb2e5827':'10?-12','fbab52c8':'13-14','3ff1e851':'15 (+content review)','616bcdf9':'16-17','0e701d1b':'18','ca1ae452':'19','556a3270':'06-07 (+infra)','6a6f63cd':'04-05 (+infra)'}
print('session | batches | tokens | calls | hours | search_executions+ | evidence_sources+ | source_value_extractions+ | search_candidates+ | net rows+ | tok/search | tok/net row')
for sid,b in batches.items():
    t=tok[sid]; rows=collections.Counter()
    for p in t['prs']: rows.update(pr[str(p)]['rows'])
    net=sum(v for v in rows.values() if v>0) - rows.get('data_migrations',0)
    se=rows.get('search_executions',0)
    print(f"{sid} | {b} | {t['tot']/1e6:.0f}M | {t['calls']} | {t['hours']:.1f} | {se} | {rows.get('evidence_sources',0)} | {rows.get('source_value_extractions',0)} | {rows.get('search_candidates',0)} | {net} | {t['tot']/se/1e6:.1f}M | {t['tot']/max(1,net)/1e6:.2f}M" if se else f"{sid} | {b} | {t['tot']/1e6:.0f}M | {t['calls']} | {t['hours']:.1f} | {se} | {rows.get('evidence_sources',0)} | {rows.get('source_value_extractions',0)} | {rows.get('search_candidates',0)} | {net} | - | {t['tot']/max(1,net)/1e6:.2f}M")
