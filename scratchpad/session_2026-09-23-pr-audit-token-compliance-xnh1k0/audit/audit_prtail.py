# Tokens spent after the session's first create_pull_request, and how many of those calls were housekeeping-only
# (git/preserve/notification/PR polling/send_later). Run from repo root.
import json,glob,re,collections
HOUSE_T={'ReadNotifications','mcp__github__pull_request_read','mcp__github__actions_list','mcp__github__actions_get','mcp__Claude_Code_Remote__send_later','mcp__Claude_Code_Remote__delete_trigger','mcp__github__subscribe_pr_activity','mcp__Claude_Code_Remote__subscribe_pr_activity','ToolSearch'}
HB=re.compile(r'^\s*(cd \S+|git (status|add|commit|push|fetch|log|diff|rev-parse|merge-tree|show)|python3 scripts/preserve_transcripts\.py|ls|echo|date)\b')
TT=collections.Counter()
for d in sorted(glob.glob('transcripts/harness_*')):
    sid=d.split('_')[-1]
    if sid=='37f845b8': continue
    calls=[];seen={}
    for l in open(d+'/main.jsonl',errors='replace'):
        r=json.loads(l)
        if r.get('type')!='assistant': continue
        m=r['message']; mid=m.get('id')
        if mid not in seen:
            u=m.get('usage') or {}; seen[mid]=dict(tot=sum(u.get(k) or 0 for k in ('input_tokens','cache_read_input_tokens','cache_creation_input_tokens','output_tokens')),tools=[]); calls.append(seen[mid])
        for c in m.get('content') or []:
            if c.get('type')=='tool_use': seen[mid]['tools'].append((c['name'],c.get('input') or {}))
    first=next((i for i,c in enumerate(calls) if any(n=='mcp__github__create_pull_request' for n,_ in c['tools'])),None)
    tot=sum(c['tot'] for c in calls)
    if first is None: print(sid,'no PR created in main'); continue
    tail=calls[first:]
    hk=[c for c in tail if c['tools'] and all(n in HOUSE_T or (n=='Bash' and all(HB.match(p) for p in re.split(r'&&|;|\n|\|',i.get('command','')) if p.strip())) for n,i in c['tools'])]
    tt=sum(c['tot'] for c in tail); ht=sum(c['tot'] for c in hk)
    TT['all']+=tot; TT['tail']+=tt; TT['hk']+=ht
    print(f"{sid} first PR at call {first}/{len(calls)}; tokens after it {tt/1e6:.0f}M of {tot/1e6:.0f}M ({tt/tot:.0%}); housekeeping-only calls after it {len(hk)} = {ht/1e6:.0f}M")
print(f"TOTAL after-first-PR {TT['tail']/1e6:.0f}M of {TT['all']/1e6:.0f}M; housekeeping-only {TT['hk']/1e6:.0f}M")
