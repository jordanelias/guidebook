# How often sessions ran check suites, what they cost, how often a run repeated with no
# intervening change, and which checks never went red. Run from repo root. Reads transcripts only;
# runs no suite.  python3 audit_suites.py > audit_suites.out
import json, glob, os, re, collections, yaml

EXCLUDE = {'37f845b8'}
def load(path):
    calls = []; byid = {}; results = {}; compacts = []; stophooks = []; rec_i = 0
    for line in open(path, errors='replace'):
        try: r = json.loads(line)
        except Exception: continue
        rec_i += 1; t = r.get('type')
        if t == 'system' and r.get('subtype') == 'compact_boundary': compacts.append(len(calls))
        if t == 'system' and r.get('subtype') == 'stop_hook_summary': stophooks.append(r)
        if t == 'attachment' and (r.get('attachment') or {}).get('hookEvent') == 'Stop':
            stophooks.append({'att': len(str((r.get('attachment') or {}).get('content') or '')), 'callidx': len(calls)})
        if t == 'user':
            c = (r.get('message') or {}).get('content')
            if isinstance(c, list):
                for x in c:
                    if isinstance(x, dict) and x.get('type') == 'tool_result':
                        cc = x.get('content'); s = cc if isinstance(cc, str) else ''.join(
                            (y.get('text', '') if isinstance(y, dict) else str(y)) for y in (cc or []))
                        results[x.get('tool_use_id')] = s
        if t == 'assistant':
            m = r.get('message') or {}; mid = m.get('id') or ('noid%d' % rec_i)
            if mid not in byid:
                u = m.get('usage') or {}
                call = dict(i=len(calls), ts=r.get('timestamp'), tools=[],
                            tot=sum((u.get(k) or 0) for k in ('input_tokens', 'cache_read_input_tokens', 'cache_creation_input_tokens', 'output_tokens')))
                byid[mid] = call; calls.append(call)
            for c in m.get('content') or []:
                if c.get('type') == 'tool_use': byid[mid]['tools'].append((c['id'], c['name'], c.get('input') or {}))
    return calls, results, compacts, stophooks

def later(calls, compacts, at):
    nxt = [ci for ci in compacts if ci > at]; end = nxt[0] if nxt else len(calls)
    return max(0, end - at - 1)

SUITE = [
    ('run_checks', re.compile(r'scripts/run_checks\.py([^|;&\n]*)')),
    ('test_db_integrity', re.compile(r'scripts/tests/test_db_integrity\.py([^|;&\n]*)')),
    ('other tests/pytest', re.compile(r'(?:pytest|scripts/tests/(?!test_db_integrity)test_\w+\.py)([^|;&\n]*)')),
    ('research_batch_dod', re.compile(r'scripts/audit/research_batch_dod\.py([^|;&\n]*)')),
    ('preflight.sh', re.compile(r'scripts/preflight\.sh([^|;&\n]*)')),
    ('direct audit script', re.compile(r'scripts/audit/(?!research_batch_dod)(\w+)\.py')),
]
def rc_mode(args):
    for f in ('--selftest', '--list', '--all', '--changed-from', '--battery', '--kinds', '--dry-run'):
        if f in args: return f
    return '(bare/other)'

RO = re.compile(r'^\s*(?:cd \S+|cat|head|tail|sed -n|grep|rg|find|ls|wc|awk|nl|echo|date|printf|sort|uniq|cut|tr|jq|true|test|\[|diff|git (?:status|log|diff|show|rev-parse|branch|add|commit|push|ls-files|blame|stash list|merge-tree)|python3 scripts/(?:run_checks|audit/research_batch_dod|tests/test_\w+)\.py|bash scripts/preflight\.sh|scripts/preflight\.sh|python3 scripts/preserve_transcripts\.py --check|export \w+=|\w+=\S+$)')
def mutating(n, i):
    if n in ('Edit', 'Write', 'NotebookEdit'): return True
    if n != 'Bash': return False
    cmd = i.get('command', '')
    if re.search(r'sed -i|>\s*[\w./]|tee |mv |cp |rm |git (?:merge|pull|checkout|reset|fetch)|migrate_db\.py|emit_|regenerate|build_site|context_map\.py|preserve_transcripts\.py(?! --check)', cmd): return True
    if 'db.py' in cmd and re.search(r'db\.py\s+(?:--\S+\s+)*(add-|amend-|observe-|correct-|relate-|derive-|adjudicate-|update-|upsert-|resolve-|reattribute-|retire-|log-mining|close-gap|delete-)', cmd): return True
    if re.search(r"python3 (?:-|<<|-c)", cmd):
        return bool(re.search(r'\b(insert|update|delete|create|drop|alter)\b|write_text|open\([^)]*[\'"]w', cmd, re.I))
    segs = [s for s in re.split(r'&&|\|\||;|\n|\|', cmd) if s.strip()]
    return not all(RO.match(s) or re.match(r'^\s*(2>&1|>/dev/null)', s) for s in segs)

REG = yaml.safe_load(open('governance/check-registry.yaml'))
reg_ids = {c['id']: c.get('level', 'blocking') for c in REG['checks']}
quar = {q['id'] for q in REG.get('quarantine', [])}
chk = collections.defaultdict(collections.Counter)          # run_checks id -> status counts
tdi = collections.defaultdict(collections.Counter)          # test_db_integrity id -> pass/fail
dod = collections.defaultdict(collections.Counter)          # DoD rule -> pass/fail
ci_fail = collections.Counter()

inv = collections.Counter(); inv_tok = collections.Counter(); inv_carry = collections.Counter(); inv_chars = collections.Counter()
rep = collections.Counter(); rep_tok = collections.Counter(); per_sess = {}
stop_dod = 0; stop_att_chars = 0
for d in sorted(glob.glob('transcripts/harness_*')):
    sid = d.split('_')[-1]
    if sid in EXCLUDE: continue
    ps = collections.Counter(); pst = collections.Counter()
    for path in [d + '/main.jsonl'] + glob.glob(d + '/subagents/*.jsonl'):
        calls, res, compacts, stophooks = load(path)
        if path.endswith('main.jsonl'):
            stop_dod += sum(1 for s in stophooks if 'hookInfos' in s and any('research_batch_dod' in (h.get('command') or '') for h in s['hookInfos']))
            stop_att_chars += sum(s.get('att', 0) for s in stophooks)
        last = {}  # key -> call index of last run
        mutated_since = {}
        for c in calls:
            share = c['tot'] / max(1, len(c['tools']))
            for tid, n, i in c['tools']:
                if mutating(n, i):
                    for k in mutated_since: mutated_since[k] = True
                if n not in ('Bash',): continue
                cmd = i.get('command', ''); out = res.get(tid, '')
                hits = []
                for fam, rx in SUITE:
                    for m in rx.finditer(cmd):
                        if fam == 'run_checks': key = 'run_checks ' + rc_mode(m.group(1))
                        elif fam == 'research_batch_dod': key = 'research_batch_dod ' + ('--all' if '--all' in m.group(1) else '--selftest' if 'selftest' in m.group(1) else '--session')
                        elif fam == 'direct audit script': key = 'direct audit script'
                        else: key = fam
                        hits.append((key, re.sub(r'\s+', ' ', m.group(0)).strip()))
                if not hits: continue
                for key, exact in hits:
                    inv[key] += 1; ps[key] += 1
                    inv_tok[key] += share / len(hits); pst[key] += share / len(hits)
                    inv_carry[key] += len(out) / 4 * later(calls, compacts, c['i']) / len(hits)
                    inv_chars[key] += len(out) / len(hits)
                    if exact in last and not mutated_since.get(exact, True):
                        rep[key] += 1; rep_tok[key] += share / len(hits) + len(out) / 4 * later(calls, compacts, c['i']) / len(hits)
                    last[exact] = c['i']; mutated_since[exact] = False
                # parse statuses
                for st, cid in re.findall(r'\[(PASS|FAIL|SKIP|ERR |NONE)\] (\w+)', out): chk[cid][st.strip()] += 1
                for lvl, ids in re.findall(r'(NON-BLOCKING|BLOCKING) failures \(\d+\): ([\w, ]+)', out):
                    for cid in ids.split(','): chk[cid.strip()]['FAIL(summary)'] += 1
                for ids in re.findall(r'NOTHING-IN-SCOPE \(\d+\): ([\w, ]+)', out):
                    for cid in ids.split(','): chk[cid.strip()]['NONE(summary)'] += 1
                for sym, tid_ in re.findall(r'\[(✓|✗)\] ([A-M]\d+\w*):', out): tdi[tid_]['pass' if sym == '✓' else 'fail'] += 1
                for tid_ in re.findall(r'^\s+\[([A-M]\d+\w*)\] ', out.split('FAILED:')[1] if 'FAILED:' in out else '', re.M): tdi[tid_]['fail(summary)'] += 1
                for code in re.findall(r'✗ (R\d+\w*):', out): dod[code]['fail'] += 1
                for code in re.findall(r'(R\d+\w*): PASS', out): dod[code]['pass'] += 1
            for tid, n, i in c['tools']:
                out = res.get(tid, '')
                for cid in re.findall(r'::(?:error|warning)::(\w+) failed', out): ci_fail[cid] += 1
                if n == 'ReadNotifications':
                    for cid in re.findall(r'"name":\s*"([\w -]+)"[^}]*"conclusion":\s*"failure"', out): ci_fail['CI job: ' + cid] += 1
    per_sess[sid] = (ps, pst)

M = lambda x: f'{x/1e6:.1f}M'
print('# SUITE INVOCATIONS (main + subagents). tokens = share of issuing API call; carry = output chars/4 x later calls until compaction')
print('suite/mode | runs | issuing-call tokens | output carry tokens | mean output chars | repeats with no intervening mutating call | tokens of those repeats')
for k, v in inv.most_common():
    print(f'{k} | {v} | {M(inv_tok[k])} | {M(inv_carry[k])} | {inv_chars[k]/v:.0f} | {rep[k]} | {M(rep_tok[k])}')
print(f'TOTAL | {sum(inv.values())} | {M(sum(inv_tok.values()))} | {M(sum(inv_carry.values()))} | | {sum(rep.values())} | {M(sum(rep_tok.values()))}')
print(f'stop-hook automatic research_batch_dod --all runs (not model-issued): {stop_dod}; Stop-hook attachment chars injected: {stop_att_chars}')
print('\n# PER SESSION runs')
for sid, (ps, pst) in per_sess.items():
    print(sid, dict(ps.most_common()), 'tokens', M(sum(pst.values())))

print('\n# run_checks: per-check status across every observed output (local runs; CI ::error:: lines separately)')
seen = set(chk)
never_red = []; always_none = []; red = []
for cid, lvl in sorted(reg_ids.items()):
    c = chk.get(cid, collections.Counter())
    fails = c['FAIL'] + c['ERR'] + c['FAIL(summary)'] + ci_fail.get(cid, 0)
    obs = sum(c.values())
    if fails: red.append((cid, lvl, fails, obs))
    elif obs and c['PASS'] == 0 and (c['NONE'] or c['NONE(summary)']): always_none.append((cid, lvl, obs))
    else: never_red.append((cid, lvl, obs, c['PASS'], c['NONE'] + c['NONE(summary)']))
print(f'registered active checks: {len(reg_ids)} (quarantined {len(quar)})')
print(f'WENT RED at least once ({len(red)}):', ', '.join(f'{a}[{b[0]}]x{c}' for a, b, c, _ in sorted(red, key=lambda x: -x[2])))
print(f'ONLY EVER NOTHING-IN-SCOPE, never PASS or FAIL ({len(always_none)}):', ', '.join(f'{a}[{b}] obs={c}' for a, b, c in always_none))
print(f'NEVER RED ({len(never_red)}) — id[level] observations/PASS/NONE:')
for cid, lvl, obs, p, nn in sorted(never_red, key=lambda x: -x[2]): print(f'   {cid:42} {lvl:13} obs={obs:4} pass={p:4} none={nn}')
print('status ids seen in output but not in current registry:', sorted(x for x in seen if x not in reg_ids and x not in quar)[:40])
print('CI failure lines:', dict(ci_fail.most_common(20)))

print('\n# test_db_integrity: per-test outcomes')
ids = sorted(tdi)
nr = [t for t in ids if not (tdi[t]['fail'] + tdi[t]['fail(summary)'])]
print(f'tests observed {len(ids)}; never failed {len(nr)}; failed at least once: ' + ', '.join(f"{t}x{tdi[t]['fail']+tdi[t]['fail(summary)']}" for t in ids if t not in nr))
src_ids = set(re.findall(r'record\(\s*["\']([A-Z]\d+\w*)["\']', open('scripts/tests/test_db_integrity.py').read()))
print(f'tests declared literally in source now: {len(src_ids)}; never observed failing among them: {len([t for t in src_ids if t not in ids or t in nr])}')
print('\n# research_batch_dod rules (explicit invocations only)')
for code in sorted(dod, key=lambda x: (len(x), x)): print(f"  {code}: pass={dod[code]['pass']} fail={dod[code]['fail']}")

print('\n# chronic reds: PASS vs FAIL observations for checks red >=100 times')
for cid in reg_ids:
    c = chk.get(cid, collections.Counter()); f = c['FAIL'] + c['ERR'] + c['FAIL(summary)']
    if f >= 100: print(f"  {cid:32} {reg_ids[cid]:10} pass={c['PASS']} fail={f} none={c['NONE']+c['NONE(summary)']}")
