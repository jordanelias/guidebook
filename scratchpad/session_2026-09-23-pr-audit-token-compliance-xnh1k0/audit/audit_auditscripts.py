# Which scripts/audit/*.py were invoked directly (outside run_checks) most often, main+subagents. Run from repo root.
import json,glob,re,collections
c=collections.Counter()
for f in glob.glob('transcripts/harness_*/main.jsonl')+glob.glob('transcripts/harness_*/subagents/*.jsonl'):
    if '37f845b8' in f: continue
    for l in open(f,errors='replace'):
        if 'scripts/audit/' not in l: continue
        r=json.loads(l)
        if r.get('type')!='assistant': continue
        for x in r['message'].get('content') or []:
            if x.get('type')=='tool_use' and x['name']=='Bash':
                for m in re.findall(r'scripts/audit/(\w+)\.py',x['input'].get('command','')): c[m]+=1
print(sum(c.values())); print(c.most_common(15))
