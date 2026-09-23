import json,sys,re,glob
for p in sorted(glob.glob('transcripts/harness_*/main.jsonl')):
    uses={};out=[]
    for line in open(p,errors='replace'):
        try:r=json.loads(line)
        except:continue
        m=r.get('message') or {}
        if r.get('type')=='assistant':
            for c in m.get('content') or []:
                if c.get('type')=='tool_use' and c['name']=='Bash' and 'research_batch_dod' in c['input'].get('command',''):
                    uses[c['id']]=(r.get('timestamp','')[:16],c['input']['command'])
        elif r.get('type')=='user' and isinstance(m.get('content'),list):
            for c in m['content']:
                if isinstance(c,dict) and c.get('type')=='tool_result' and c.get('tool_use_id') in uses:
                    s=json.dumps(c.get('content'))
                    verdict=re.findall(r'(COMPLIANT|NON-COMPLIANT|VERDICT[^\\]{0,60}|FAIL[^\\]{0,50}|exit[= ]\d)',s)
                    ts,cmd=uses[c['tool_use_id']]
                    sess=re.search(r'--session[= ]+("?[^ "|]+"?|\$\S+)',cmd); allf='--all' in cmd
                    out.append((ts,(sess.group(1)[:60] if sess else ('--all' if allf else '?')),verdict[-3:] if verdict else s[-120:]))
    if out:
        print('==',p.split('/')[1],'runs',len(out))
        for o in out[-3:]: print('   ',o)
