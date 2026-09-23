# Token/waste audit over transcripts/harness_*/  (run from repo root: python3 <this> > audit_tokens.out)
# Unit of cost: one API call (assistant message.id, deduped). call_tokens = input+cache_read+cache_write+output.
# Marginal-cost model: every tool call forces one more API call that re-reads the whole context, so a
# tool call's attributable cost = call_tokens / n_tool_uses_in_that_call. "Carry" of a tool result =
# est_tokens(result) x number of later API calls before the next compaction (it is cache-read each time).
import json, glob, os, re, collections, statistics, subprocess, difflib, sqlite3, sys
from datetime import datetime

S = os.path.dirname(os.path.abspath(__file__))
def ts(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00')) if s else None
def est_tok(nchars): return nchars / 4.0

DBW = re.compile(r'scripts/db\.py\s+(?:--\S+\s+)*(add-|amend-|observe-term|correct-|relate-|derive-|adjudicate-|update-|upsert-|resolve-|reattribute-|retire-|log-mining|close-gap|delete-)')
SHELL_READ = re.compile(r'^(?:cd \S+ (?:&&|;) *)?(cat|head|tail|sed -n|grep|rg|find|ls|wc|awk|nl)\b')

def classify_trigger(s, meta):
    if s.startswith('<task-notification>') and 'queued-remote-notifications' in s[:120]: return 'notification'
    if s.startswith('<task-notification>'): return 'bg-task-done'
    if s.startswith('Stop hook feedback'): return 'stop-hook'
    if s.startswith('This session is being continued'): return 'compaction-resume'
    if s.startswith('Another Claude session sent'): return 'peer-msg'
    if meta: return 'meta'
    return 'human'

def load(path):
    calls = []; byid = {}; results = {}; triggers = []; compacts = []; rec_i = 0
    cur_trig = 'start'
    for line in open(path, errors='replace'):
        try: r = json.loads(line)
        except Exception: continue
        rec_i += 1; t = r.get('type')
        if t == 'system' and r.get('subtype') == 'compact_boundary':
            compacts.append((len(calls), r.get('timestamp'), (r.get('compactMetadata') or {}).get('preTokens')))
        if t == 'user':
            c = (r.get('message') or {}).get('content')
            if isinstance(c, list) and any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in c):
                for x in c:
                    if isinstance(x, dict) and x.get('type') == 'tool_result':
                        cc = x.get('content'); s = cc if isinstance(cc, str) else ''.join(
                            (y.get('text', '') if isinstance(y, dict) else str(y)) for y in (cc or []))
                        results[x.get('tool_use_id')] = (len(s), s, len(calls))
            else:
                s = c if isinstance(c, str) else ' '.join(x.get('text', '') for x in (c or []) if isinstance(x, dict))
                cls = classify_trigger(s.strip(), r.get('isMeta'))
                triggers.append((len(calls), cls, r.get('timestamp'), s[:300]))
                cur_trig = cls
        if t == 'assistant':
            m = r.get('message') or {}; mid = m.get('id') or ('noid%d' % rec_i)
            if mid not in byid:
                u = m.get('usage') or {}
                call = dict(id=mid, i=len(calls), ts=r.get('timestamp'), trig=cur_trig, model=m.get('model'),
                            inp=u.get('input_tokens') or 0, cr=u.get('cache_read_input_tokens') or 0,
                            cw=u.get('cache_creation_input_tokens') or 0, out=u.get('output_tokens') or 0,
                            tools=[], text='')
                call['ctx'] = call['inp'] + call['cr'] + call['cw']; call['tot'] = call['ctx'] + call['out']
                byid[mid] = call; calls.append(call)
            call = byid[mid]
            for c in m.get('content') or []:
                if c.get('type') == 'tool_use': call['tools'].append((c['id'], c['name'], c.get('input') or {}))
                elif c.get('type') == 'text': call['text'] += c['text']
    return dict(calls=calls, results=results, triggers=triggers, compacts=compacts)

def carry_calls(calls, compacts, at):
    nxt = [ci for ci, _, _ in compacts if ci > at]
    end = nxt[0] if nxt else len(calls)
    return max(0, end - at - 1)

def tool_share(call): return call['tot'] / max(1, len(call['tools']))

sessions = {}
HOUSE = re.compile(r'^(?:cd \S+ ?(?:&&|;) *)?(?:git (?:status|add|commit|push|fetch|log|diff|merge|rev-parse|show|pull)|python3 scripts/preserve_transcripts\.py|ls\b|date\b|echo\b|[A-Z_]+=|sleep\b|tail\b|head\b)')
HOUSE_TOOLS = {'ReadNotifications', 'mcp__github__pull_request_read', 'mcp__github__actions_list', 'mcp__github__actions_get',
               'mcp__Claude_Code_Remote__send_later', 'mcp__Claude_Code_Remote__delete_trigger', 'mcp__Claude_Code_Remote__update_trigger',
               'mcp__github__subscribe_pr_activity', 'mcp__github__unsubscribe_pr_activity', 'mcp__Claude_Code_Remote__subscribe_pr_activity',
               'mcp__Claude_Code_Remote__unsubscribe_pr_activity', 'mcp__github__get_job_logs', 'ToolSearch', 'TaskUpdate', 'mcp__github__list_pull_requests'}
def is_house(n, i):
    if n in HOUSE_TOOLS: return True
    if n == 'Bash':
        cmd = i.get('command', '').strip()
        nq = re.sub(r"<<-?\s*'?(\w+)'?.*?\n\1\b", 'HEREDOC', cmd, flags=re.S)
        nq = re.sub(r'"(?:[^"\\]|\\.)*"', '""', nq, flags=re.S); nq = re.sub(r"'[^']*'", "''", nq)
        parts = [p.strip() for p in re.split(r'&&|;|\n|\|\|', nq) if p.strip()]
        return all(HOUSE.match(p) or p.startswith(('cd ', '#')) for p in parts) and not re.search(r'git commit(?!.*(transcript|command log|provenance|preserve|session log))', cmd, re.I | re.S)
    return False
READKEY = [re.compile(r"sed -n ['\"]?(\d+,\d+)p['\"]? ([\w./-]+)"), re.compile(r"(?:^|&& |; )cat ([\w./-]+\.\w+)\s*$"),
           re.compile(r"head -(?:n ?)?(\d+) ([\w./-]+)")]
EXCLUDE = {'37f845b8'}  # the auditing session itself
for d in sorted(glob.glob('transcripts/harness_*')):
    sid = d.split('_')[-1]
    if sid in EXCLUDE: continue
    main = load(d + '/main.jsonl')
    subs = {}
    for p in glob.glob(d + '/subagents/*.jsonl'):
        subs[os.path.basename(p)] = load(p)
    idx = json.load(open(d + '/index.json')) if os.path.exists(d + '/index.json') else []
    branches = collections.Counter()
    for line in open(d + '/main.jsonl', errors='replace'):
        try: b = json.loads(line).get('gitBranch')
        except Exception: continue
        if b: branches[b] += 1
    sessions[sid] = dict(main=main, subs=subs, idx=idx, branches=branches)

# ---- branch -> merged PRs, and per-PR diff stats (excluding transcripts/scratchpad) + DB row deltas
merges = subprocess.run(['git', 'log', 'origin/main', '--merges', '--format=%H %s'], capture_output=True, text=True).stdout.splitlines()
pr_of_branch = collections.defaultdict(list); prinfo = {}
for ln in merges:
    h, s = ln.split(' ', 1)
    m = re.match(r'Merge pull request #(\d+) from \S+?/(\S+)', s)
    if not m: continue
    pr, br = int(m.group(1)), m.group(2)
    pr_of_branch[br].append(pr)
    ns = subprocess.run(['git', 'diff', '--numstat', h + '^1', h], capture_output=True, text=True).stdout.splitlines()
    tot = sub = log = gen = mig = 0
    for x in ns:
        a, b_, f = x.split('\t', 2); a = int(a) if a != '-' else 0; b_ = int(b_) if b_ != '-' else 0
        tot += a + b_
        if f.startswith(('transcripts/', 'scratchpad/')): log += a + b_
        elif f.startswith(('site/', 'parts/', 'audits/', 'tools/')) or 'context-map' in f or f.endswith('.html'): gen += a + b_
        else:
            sub += a + b_
            if f.startswith('scripts/migrations/data_'): mig += a
    prinfo[pr] = dict(branch=br, sha=h, tot=tot, log=log, gen=gen, sub=sub, datamig=mig)

def rowcounts(rev):
    b = subprocess.run(['git', 'show', f'{rev}:data/guidebook.db'], capture_output=True).stdout
    if not b: return {}
    p = S + '/_rc.db'; open(p, 'wb').write(b)
    con = sqlite3.connect(p)
    out = {t: con.execute(f'select count(*) from "{t}"').fetchone()[0] for (t,) in con.execute("select name from sqlite_master where type='table'")}
    con.close(); return out
KEY_TABLES = ['evidence_sources', 'search_log', 'search_candidates', 'citation_mining', 'extractions', 'observed_terms', 'population_matches', 'retrieval_log']
for pr, pi in prinfo.items():
    a, b_ = rowcounts(pi['sha'] + '^1'), rowcounts(pi['sha'])
    pi['rows'] = {t: b_.get(t, 0) - a.get(t, 0) for t in set(a) | set(b_) if t != 'pipeline_runs' and b_.get(t, 0) != a.get(t, 0)}
    pi['netrows'] = sum(v for v in pi['rows'].values() if v > 0)

# ---- per-session metrics
agg = collections.Counter(); table = []
waste = collections.Counter(); wnotes = collections.defaultdict(list)
per = {}
for sid, S_ in sessions.items():
    M = S_['main']; calls = M['calls']; res = M['results']
    u = collections.Counter()
    for c in calls:
        for k in ('inp', 'cr', 'cw', 'out'): u[k] += c[k]
    su = collections.Counter(); sub_calls = 0
    for L in S_['subs'].values():
        for c in L['calls']:
            sub_calls += 1
            for k in ('inp', 'cr', 'cw', 'out'): su[k] += c[k]
    tot_main = sum(u.values()); tot_sub = sum(su.values())
    ctxs = [c['ctx'] for c in calls]
    drops = sum(1 for a, b in zip(ctxs, ctxs[1:]) if a > 200000 and b < a * 0.5)
    prs = sorted({p for br in S_['branches'] for p in pr_of_branch.get(br.replace('claude/', 'claude/'), []) } |
                 {p for br in S_['branches'] for p in pr_of_branch.get(br, [])})
    subl = sum(prinfo[p]['sub'] for p in prs); rows = sum(prinfo[p]['netrows'] for p in prs)
    t0, t1 = ts(calls[0]['ts']), ts(calls[-1]['ts'])
    d = dict(sid=sid, branch=S_['branches'].most_common(1)[0][0] if S_['branches'] else '', calls=len(calls), sub_calls=sub_calls,
             tot=tot_main + tot_sub, tot_main=tot_main, tot_sub=tot_sub, out=u['out'] + su['out'], cr=u['cr'] + su['cr'],
             cw=u['cw'] + su['cw'], inp=u['inp'] + su['inp'],
             ctxmax=max(ctxs), gt500=sum(x > 500000 for x in ctxs), gt700=sum(x > 700000 for x in ctxs),
             compacts=len(M['compacts']), drops=drops, prs=prs, subl=subl, rows=rows,
             hours=(t1 - t0).total_seconds() / 3600, meanctx=statistics.mean(ctxs))
    d['cr_per_out'] = d['cr'] / max(1, d['out'])
    # weighted, input-token-equivalent (assumed relative prices: cache read 0.1x, cache write 1.25x, output 5x input)
    d['wtd'] = d['inp'] + 0.1 * d['cr'] + 1.25 * d['cw'] + 5 * d['out']
    per[sid] = d

    # ----- episodes by trigger class
    ep = collections.Counter(); epn = collections.Counter()
    for c in calls: ep[c['trig']] += c['tot']; epn[c['trig']] += 1
    d['ep'] = ep; d['epn'] = epn
    # episode segmentation: a new episode at each trigger; housekeeping-only if every tool call is housekeeping
    bounds = sorted({t[0] for t in M['triggers']} | {0, len(calls)})
    trig_at = {}
    for t in M['triggers']: trig_at[t[0]] = t[1]
    hk = collections.Counter(); hkn = collections.Counter(); hkeps = collections.Counter(); alleps = collections.Counter()
    for a, b in zip(bounds, bounds[1:]):
        seg = calls[a:b]
        if not seg: continue
        cls = seg[0]['trig']; alleps[cls] += 1
        if all(is_house(n, i) for c in seg for _, n, i in c['tools']):
            hkeps[cls] += 1; hk[cls] += sum(c['tot'] for c in seg); hkn[cls] += len(seg)
    d['hk'] = hk; d['hkn'] = hkn; d['hkeps'] = hkeps; d['alleps'] = alleps
    # context economics
    base = calls[0]['ctx']
    d['floor'] = sum(min(c['ctx'], base) for c in calls)
    d['over250'] = sum(max(0, c['ctx'] - 250000) for c in calls)
    d['over500'] = sum(max(0, c['ctx'] - 500000) for c in calls)

    # (b) stop-hook episodes: commits made inside them
    sh_commits = sh_preserve = 0
    for c in calls:
        if c['trig'] != 'stop-hook': continue
        for _, n, i in c['tools']:
            if n == 'Bash':
                cmd = i.get('command', '')
                if 'git commit' in cmd: sh_commits += 1
                if 'preserve_transcripts' in cmd: sh_preserve += 1
    d['sh_trig'] = sum(1 for t in M['triggers'] if t[1] == 'stop-hook'); d['sh_commits'] = sh_commits
    pres = [(c, i) for c in calls for _, n, i in c['tools'] if n == 'Bash' and 'preserve_transcripts' in i.get('command', '')]
    d['preserve_calls'] = len(pres); d['preserve_tok'] = sum(tool_share(c) for c, _ in pres)
    commits = [i.get('command', '') for c in calls for _, n, i in c['tools'] if n == 'Bash' and 'git commit' in i.get('command', '')]
    d['commits'] = len(commits)
    d['log_commits'] = sum(1 for x in commits if re.search(r'session command log|transcript|preserve', x, re.I))

    # (a) notifications
    rn = [(c, tid) for c in calls for tid, n, _ in c['tools'] if n == 'ReadNotifications']
    gaps = [(ts(b[0]['ts']) - ts(a[0]['ts'])).total_seconds() / 60 for a, b in zip(rn, rn[1:])]
    origins = collections.Counter(); kinds = collections.Counter(); empty = 0
    for c, tid in rn:
        s = res.get(tid, (0, '', 0))[1]
        if not re.search(r'Exactly \d+ notification', s): empty += 1
        for o in re.findall(r'origin: ([^·\n]+?) ·', s): origins[o.strip()[:40]] += 1
        for k in re.findall(r'kind="([^"]+)"', s): kinds[k] += 1
    # notification episode no-op: no Edit/Write/commit/push/db write in the episode
    noop = 0; eps = 0; cur = None; acted = False; ep_tok = collections.Counter()
    for c in calls + [None]:
        if c is None or (c['trig'] != cur or (cur == 'notification' and any(n == 'ReadNotifications' for _, n, _ in c['tools']))):
            if cur == 'notification':
                eps += 1; noop += (not acted)
            if c is None: break
            cur = c['trig']; acted = False
        for _, n, i in c['tools']:
            cmd = i.get('command', '') if n == 'Bash' else ''
            if n in ('Edit', 'Write') or 'git commit' in cmd or 'git push' in cmd or DBW.search(cmd) or n in ('mcp__github__update_pull_request', 'mcp__github__add_issue_comment'):
                acted = True
    d['rn'] = len(rn); d['rn_gap_med'] = statistics.median(gaps) if gaps else None; d['rn_empty'] = empty
    d['rn_origins'] = origins; d['rn_kinds'] = kinds; d['notif_eps'] = eps; d['notif_noop'] = noop
    d['send_later'] = sum(1 for c in calls for _, n, _ in c['tools'] if n.endswith('send_later'))
    d['pr_read'] = sum(1 for c in calls for _, n, _ in c['tools'] if n in ('mcp__github__pull_request_read', 'mcp__github__actions_list', 'mcp__github__actions_get'))

    # (c) repeated Bash commands
    seen = collections.Counter(); dup_tok = 0; dup_n = 0
    fam = collections.Counter(); famtok = collections.Counter()
    for c in calls:
        for _, n, i in c['tools']:
            if n != 'Bash': continue
            cmd = i.get('command', '')
            norm = re.sub(r'GUIDEBOOK_DB_PATH=\S+', '', cmd); norm = re.sub(r'\s+', ' ', norm).strip()
            seen[norm] += 1
            if seen[norm] > 1: dup_n += 1; dup_tok += tool_share(c)
            f = None
            if 'run_checks.py' in cmd:
                f = 'run_checks --all' if '--all' in cmd else ('run_checks --changed-from' if '--changed-from' in cmd else 'run_checks other')
            elif 'test_db_integrity' in cmd: f = 'test_db_integrity'
            elif 'research_batch_dod' in cmd: f = 'research_batch_dod'
            elif re.search(r'select count\(\*\)|count\(\*\)', cmd, re.I) and 'sqlite3' in cmd: f = 'ad-hoc sqlite census'
            elif 'preflight.sh' in cmd: f = 'preflight.sh'
            elif 'context_map.py' in cmd or 'regenerate_derived' in cmd: f = 'regenerate/context_map'
            if f: fam[f] += 1; famtok[f] += tool_share(c)
    d['dup_n'] = dup_n; d['dup_tok'] = dup_tok; d['fam'] = fam; d['famtok'] = famtok

    # (d) large results + carry
    big = []; carry_all = 0; carry_by = collections.Counter()
    for c in calls:
        for tid, n, i in c['tools']:
            if tid not in res: continue
            ln, s, at = res[tid]
            cc = est_tok(ln) * carry_calls(calls, M['compacts'], c['i'])
            carry_all += cc
            k = n
            if n == 'Bash':
                cmd = i.get('command', '')
                m_ = re.search(r'scripts/[\w/.-]+\.(?:py|sh)', cmd)
                k = 'Bash:' + (m_.group(0) if m_ else ('shell-read' if SHELL_READ.match(cmd.strip()) else 'git' if cmd.strip().startswith(('git', 'cd /home/user/guidebook; git', 'cd /home/user/guidebook && git')) else 'python-inline' if 'python3 -' in cmd or 'python3 <<' in cmd else 'other'))
            carry_by[k] += cc
    d['carry_by'] = carry_by
    for c in calls:
        for tid, n, i in c['tools']:
            if tid not in res: continue
            ln, s, at = res[tid]
            cc = est_tok(ln) * carry_calls(calls, M['compacts'], c['i'])
            if ln > 20000:
                lbl = n
                if n == 'Bash':
                    cmd = i.get('command', '')
                    m_ = re.search(r'(scripts/[\w/.-]+\.(?:py|sh))(\s+--?[\w-]+)?', cmd)
                    lbl = 'Bash:' + (m_.group(0) if m_ else cmd.split()[0] if cmd.split() else '')
                elif n == 'ReadNotifications': lbl = 'ReadNotifications'
                big.append((ln, lbl, cc))
    d['big'] = big; d['carry_all'] = carry_all

    # (e) re-reads of same file range
    rk = collections.Counter(); reread_tok = 0; reread_n = 0; readtool = bashread = 0; fileread = collections.Counter()
    for c in calls:
        for tid, n, i in c['tools']:
            key = None
            if n == 'Read': key = (i.get('file_path'), i.get('offset'), i.get('limit')); readtool += 1
            elif n in ('Grep', 'Glob'): readtool += 1
            elif n == 'Bash':
                cmd = i.get('command', '').strip()
                if SHELL_READ.match(cmd): bashread += 1
                for rx in READKEY:
                    m_ = rx.search(cmd)
                    if m_: key = tuple(m_.groups()); break
                if key: fileread[key[-1]] += 1
            if key:
                rk[key] += 1
                if rk[key] > 1:
                    reread_n += 1; reread_tok += tool_share(c) + (est_tok(res.get(tid, (0,))[0]) * carry_calls(calls, M['compacts'], c['i']))
    d['fileread'] = fileread; d['reread_keys'] = [(k, v) for k, v in rk.most_common(5) if v > 1]
    d['reread_n'] = reread_n; d['reread_tok'] = reread_tok; d['readtool'] = readtool; d['bashread'] = bashread
    d['bash'] = sum(1 for c in calls for _, n, _ in c['tools'] if n == 'Bash')

    # (f) subagents
    ag = []
    for c in calls:
        for tid, n, i in c['tools']:
            if n in ('Agent', 'Task'):
                r_ = res.get(tid, (0, '', 0))
                ag.append(dict(type=i.get('subagent_type') or 'general-purpose', desc=i.get('description', ''), prompt=i.get('prompt', ''),
                               bg=bool(i.get('run_in_background')), rlen=r_[0], rtxt=r_[1][:200], ts=c['ts']))
    def sh(t):
        w = re.findall(r'\w+', t.lower()); return {' '.join(w[k:k + 6]) for k in range(max(0, len(w) - 5))}
    shs = [sh(a['prompt']) for a in ag]
    dup_pairs = []
    for a in range(len(ag)):
        for b in range(a + 1, len(ag)):
            if not shs[a] or not shs[b]: continue
            j = len(shs[a] & shs[b]) / len(shs[a] | shs[b])
            if j > 0.35:
                dup_pairs.append((a, b, round(j, 2), ag[a]['desc'][:40], ag[b]['desc'][:40]))
    # subagent files: final text length, tokens, whether it ended with a report
    sf = []
    for k, L in S_['subs'].items():
        last_text = ''
        for c in L['calls']:
            if c['text'].strip(): last_text = c['text']
        tools_used = collections.Counter(n for c in L['calls'] for _, n, _ in c['tools'])
        sf.append(dict(file=k, tok=sum(c['tot'] for c in L['calls']), calls=len(L['calls']), final=len(last_text),
                       ctxmax=max([c['ctx'] for c in L['calls']] or [0]), model=collections.Counter(c['model'] for c in L['calls']).most_common(1),
                       bash=tools_used['Bash'], read=tools_used['Read'] + tools_used['Grep'] + tools_used['Glob']))
    d['subfiles'] = sf
    d['taskstop'] = sum(1 for c in calls for _, n, _ in c['tools'] if n in ('TaskStop', 'KillShell'))
    d['sendmsg'] = sum(1 for c in calls for _, n, _ in c['tools'] if n == 'SendMessage')
    d['agents'] = ag; d['agent_dups'] = dup_pairs
    d['agent_types'] = collections.Counter(a['type'] for a in ag)
    d['agent_failed'] = sum(1 for a in ag if re.search(r'interrupt|error|killed|API Error|stopped', a['rtxt'], re.I) and a['rlen'] < 2000)
    # subagent tokens per file
    d['sub_tok_files'] = {k: sum(c['tot'] for c in L['calls']) for k, L in S_['subs'].items()}

    # (g) preamble before first productive write
    def first_where(pred):
        for c in calls:
            if any(pred(n, i) for _, n, i in c['tools']): return c
    fe = first_where(lambda n, i: n in ('Edit', 'Write') and 'scratchpad' not in (i.get('file_path') or '') and 'transcripts' not in (i.get('file_path') or ''))
    fd = first_where(lambda n, i: n == 'Bash' and bool(DBW.search(i.get('command', ''))))
    fr = first_where(lambda n, i: n.startswith(('mcp__PubMed', 'mcp__Consensus', 'mcp__Scholar', 'WebSearch', 'WebFetch')) or (n == 'Bash' and 'retrieval_log.py' in i.get('command', '') and 'fetch' in i.get('command', '')))
    for lbl, f in (('edit', fe), ('dbw', fd), ('research', fr)):
        d['first_' + lbl] = (f['i'], sum(c['tot'] for c in calls[:f['i']]), (ts(f['ts']) - ts(calls[0]['ts'])).total_seconds() / 60) if f else None
    first = None
    for c in calls:
        for _, n, i in c['tools']:
            cmd = i.get('command', '') if n == 'Bash' else ''
            if n in ('Edit', 'Write') or DBW.search(cmd) or 'git commit' in cmd:
                first = c; break
        if first: break
    if first:
        d['pre_calls'] = first['i']; d['pre_tok'] = sum(c['tot'] for c in calls[:first['i']])
        d['pre_min'] = (ts(first['ts']) - ts(calls[0]['ts'])).total_seconds() / 60
    else:
        d['pre_calls'] = len(calls); d['pre_tok'] = tot_main; d['pre_min'] = None

    # tool usage incl. subagents
    tc = collections.Counter(); skills = collections.Counter()
    for L in [M] + list(S_['subs'].values()):
        for c in L['calls']:
            for _, n, i in c['tools']:
                tc[n] += 1
                if n == 'Skill': skills[i.get('skill')] += 1
                if n == 'Bash' and re.search(r'curl .*(crossref|ncbi|eutils|openalex|semanticscholar|doi\.org)', i.get('command', '')): tc['Bash:curl-scholarly'] += 1
                if n == 'Bash' and 'retrieval_log.py' in i.get('command', ''): tc['Bash:retrieval_log.py'] += 1
    d['tc'] = tc; d['skills'] = skills

# ---------------- output
def M_(x): return f'{x/1e6:.1f}M'
print('# PER-SESSION TABLE')
print('sid | hours | calls(main/sub) | tot tokens | main/sub | out | cr/out | wtd(Minput-eq) | ctxmax | >500k | >700k | compact | PRs | substantive lines | net DB rows | tok per PR | tok per 1k lines')
T = collections.Counter()
for sid, d in sorted(per.items(), key=lambda x: -x[1]['tot']):
    npr = len(d['prs'])
    print(f"{sid} | {d['hours']:.1f} | {d['calls']}/{d['sub_calls']} | {M_(d['tot'])} | {M_(d['tot_main'])}/{M_(d['tot_sub'])} | {d['out']/1e3:.0f}k | {d['cr_per_out']:.0f} | {d['wtd']/1e6:.1f} | {d['ctxmax']/1e3:.0f}k | {d['gt500']} | {d['gt700']} | {d['compacts']} | {','.join(map(str,d['prs'])) or '-'} | {d['subl']} | {d['rows']} | {M_(d['tot']/npr) if npr else '-'} | {M_(d['tot']/max(1,d['subl'])*1000) if d['subl'] else '-'}")
    for k in ('tot', 'tot_main', 'tot_sub', 'out', 'cr', 'cw', 'inp', 'calls', 'sub_calls', 'gt500', 'gt700', 'compacts', 'wtd'): T[k] += d[k]
allprs = sorted({p for d in per.values() for p in d['prs']})
T_sub = sum(prinfo[p]['sub'] for p in allprs)
print(f"TOTAL | | {T['calls']}/{T['sub_calls']} | {M_(T['tot'])} | {M_(T['tot_main'])}/{M_(T['tot_sub'])} | {T['out']/1e3:.0f}k | {T['cr']/T['out']:.0f} | {T['wtd']/1e6:.1f} | | {T['gt500']} | {T['gt700']} | {T['compacts']} | {len(allprs)} PRs | {T_sub} | | {M_(T['tot']/len(allprs))} |")
print(f"cache_read share of all tokens: {T['cr']/T['tot']:.3f}; output share: {T['out']/T['tot']:.4f}; cache_write {T['cw']/T['tot']:.4f}")
print('calls with ctx >500k share of tokens:', f"{sum(c['tot'] for s in sessions.values() for c in s['main']['calls'] if c['ctx']>500000)/T['tot_main']:.3f} of main tokens")

print('\n# PRs per session (merged into origin/main), diff split: total/log(transcripts+scratchpad)/generated/substantive, net rows added')
for sid, d in per.items():
    for p in d['prs']:
        pi = prinfo[p]
        print(f"{sid} #{p} tot={pi['tot']} log={pi['log']} gen={pi['gen']} sub={pi['sub']} datamig_add={pi['datamig']} rows+={pi['netrows']} {dict(sorted(((k,v) for k,v in pi['rows'].items()), key=lambda x:-abs(x[1]))[:6])}")

print('\n# EPISODE COST BY TRIGGER (tokens of API calls made in response to each trigger class)')
EP = collections.Counter(); EPN = collections.Counter()
for sid, d in per.items():
    EP.update(d['ep']); EPN.update(d['epn'])
    print(sid, {k: f"{M_(v)}/{d['epn'][k]}c" for k, v in d['ep'].most_common()})
print('TOTAL', {k: f"{M_(v)}/{EPN[k]}calls" for k, v in EP.most_common()})
print('\n# HOUSEKEEPING-ONLY EPISODES (every tool call is git/preserve/notification/PR-poll/send_later; commits log-only)')
HK = collections.Counter(); HKN = collections.Counter(); HKE = collections.Counter(); AE = collections.Counter()
for sid, d in per.items():
    HK.update(d['hk']); HKN.update(d['hkn']); HKE.update(d['hkeps']); AE.update(d['alleps'])
    print(sid, {k: f"{d['hkeps'][k]}/{d['alleps'][k]}eps {M_(v)}" for k, v in d['hk'].most_common()})
print('TOTAL', {k: f"{HKE[k]}/{AE[k]} episodes, {HKN[k]} calls, {M_(v)}" for k, v in HK.most_common()}, 'sum', M_(sum(HK.values())))
print('\n# CONTEXT ECONOMICS: floor = first-call ctx x calls (system prompt+CLAUDE.md+tools); over250/over500 = sum of ctx above threshold')
for sid, d in per.items():
    print(f"{sid} base_ctx={d['floor']/max(1,d['calls'])/1e3:.0f}k floor={M_(d['floor'])} over250k={M_(d['over250'])} over500k={M_(d['over500'])} meanctx={d['meanctx']/1e3:.0f}k compacts={d['compacts']} drops={d['drops']}")
print('TOTAL floor', M_(sum(d['floor'] for d in per.values())), 'over250', M_(sum(d['over250'] for d in per.values())), 'over500', M_(sum(d['over500'] for d in per.values())))

print('\n# (a) NOTIFICATIONS')
for sid, d in per.items():
    print(f"{sid} ReadNotifications={d['rn']} empty={d['rn_empty']} median_gap_min={d['rn_gap_med'] and round(d['rn_gap_med'],1)} episodes={d['notif_eps']} noop_episodes={d['notif_noop']} send_later={d['send_later']} pr/actions reads={d['pr_read']} origins={dict(d['rn_origins'])} kinds={dict(d['rn_kinds'].most_common(5))}")
print('TOTAL RN', sum(d['rn'] for d in per.values()), 'eps', sum(d['notif_eps'] for d in per.values()), 'noop', sum(d['notif_noop'] for d in per.values()),
      'send_later', sum(d['send_later'] for d in per.values()))
O = collections.Counter(); K = collections.Counter()
for d in per.values(): O.update(d['rn_origins']); K.update(d['rn_kinds'])
print('origins', dict(O)); print('kinds', dict(K))

print('\n# (b) STOP-HOOK / TRANSCRIPT CYCLES')
for sid, d in per.items():
    print(f"{sid} stophook_triggers={d['sh_trig']} calls_in_stophook_episodes={d['epn']['stop-hook']} tokens={M_(d['ep']['stop-hook'])} commits_in_those={d['sh_commits']} preserve_calls={d['preserve_calls']} preserve_tok={M_(d['preserve_tok'])} all_commits={d['commits']} log_commits={d['log_commits']}")
print('TOTAL stophook triggers', sum(d['sh_trig'] for d in per.values()), 'calls', EPN['stop-hook'], 'tokens', M_(EP['stop-hook']))

print('\n# (c) REPEATED BASH')
F = collections.Counter(); FT = collections.Counter()
for sid, d in per.items():
    F.update(d['fam']); FT.update(d['famtok'])
    print(f"{sid} exact_dup_bash={d['dup_n']} dup_tok={M_(d['dup_tok'])} fam={dict(d['fam'])}")
print('TOTAL dup', sum(d['dup_n'] for d in per.values()), M_(sum(d['dup_tok'] for d in per.values())))
print('families', {k: f"{v} calls {M_(FT[k])}" for k, v in F.most_common()})

print('\n# (d) LARGE RESULTS >20KB')
B = collections.Counter(); BC = collections.Counter(); BB = collections.Counter()
for sid, d in per.items():
    for ln, lbl, cc in d['big']:
        B[lbl] += 1; BC[lbl] += cc; BB[lbl] += ln
print('total carry of ALL tool results (est tok = chars/4 x later calls):', M_(sum(d['carry_all'] for d in per.values())))
print('big results n=', sum(B.values()), 'carry', M_(sum(BC.values())))
CB = collections.Counter()
for d in per.values(): CB.update(d['carry_by'])
print('carry by producer (top 15):', {k: M_(v) for k, v in CB.most_common(15)})
for k, v in sorted(B.items(), key=lambda x: -BC[x[0]])[:20]: print(f"  {k}: n={v} chars={BB[k]} carry={M_(BC[k])}")

print('\n# (e) RE-READS')
for sid, d in per.items():
    print(f"{sid} top files read >=4x: {[(f,n) for f,n in d['fileread'].most_common(4) if n>=4]} same-range keys: {d['reread_keys'][:3]}")
    print(f"{sid} reread_n={d['reread_n']} reread_tok={M_(d['reread_tok'])} bash_reads={d['bashread']} of bash={d['bash']} Read/Grep/Glob tools={d['readtool']}")
print('TOTAL reread', sum(d['reread_n'] for d in per.values()), M_(sum(d['reread_tok'] for d in per.values())),
      'bash reads', sum(d['bashread'] for d in per.values()), 'tool reads', sum(d['readtool'] for d in per.values()))

print('\n# (f) SUBAGENTS')
AT = collections.Counter()
for sid, d in per.items():
    AT.update(d['agent_types'])
    print(f"{sid} n={len(d['agents'])} types={dict(d['agent_types'])} bg={sum(a['bg'] for a in d['agents'])} failed/short={d['agent_failed']} sub_tokens={M_(d['tot_sub'])} dup_pairs={d['agent_dups']}")
    print(f"    taskstop={d['taskstop']} sendmessage={d['sendmsg']}")
    for a in d['agents']:
        print(f"    - {a['type']:15} bg={a['bg']} {a['desc'][:60]!r}")
    for f in sorted(d['subfiles'], key=lambda x: x['file']):
        print(f"    * {f['file'][:60]:60} tok={M_(f['tok'])} calls={f['calls']} ctxmax={f['ctxmax']/1e3:.0f}k final_text={f['final']} model={f['model']} bash={f['bash']} read/grep/glob={f['read']}")
print('agent types total', dict(AT))

print('\n# (g) PREAMBLE before first Edit/Write/db.py-write/git commit')
for sid, d in per.items():
    fx = lambda v: f"call {v[0]}, {M_(v[1])}, {v[2]:.0f}min" if v else 'never'
    print(f"{sid} first non-scratch Edit/Write: {fx(d['first_edit'])} | first db.py write: {fx(d['first_dbw'])} | first research retrieval: {fx(d['first_research'])}")
    print(f"{sid} calls={d['pre_calls']} tokens={M_(d['pre_tok'])} minutes={d['pre_min'] and round(d['pre_min'])} share_of_session={d['pre_tok']/d['tot_main']:.2f}")
print('TOTAL preamble tokens', M_(sum(d['pre_tok'] for d in per.values())))

print('\n# TOOLS (main+subagents)')
TC = collections.Counter(); SK = collections.Counter()
for sid, d in per.items():
    TC.update(d['tc']); SK.update(d['skills'])
    r = {k: v for k, v in d['tc'].items() if k.startswith(('mcp__PubMed', 'mcp__Consensus', 'mcp__Scholar', 'mcp__bioRxiv', 'Web', 'Bash:'))}
    print(sid, 'skills', dict(d['skills']), 'research', r)
print('SKILLS', dict(SK)); print('ALL TOOLS', dict(TC.most_common(40)))

json.dump({sid: {k: v for k, v in d.items() if k in ('tot', 'out', 'cr', 'calls', 'ctxmax', 'prs', 'subl', 'rows', 'hours', 'wtd', 'carry_by', 'ep', 'epn', 'hk', 'gt500', 'gt700', 'compacts', 'tot_sub', 'rn', 'sh_trig', 'meanctx', 'over250', 'first_edit', 'first_dbw', 'first_research', 'tc')} for sid, d in per.items()},
          open(S + '/audit_tokens.json', 'w'), indent=1)
json.dump({p: {k: v for k, v in pi.items() if k != 'sha'} for p, pi in prinfo.items()}, open(S + '/pr_info.json', 'w'), indent=1)
