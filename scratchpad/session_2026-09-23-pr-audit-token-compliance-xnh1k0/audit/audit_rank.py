# Exclusive per-call attribution of MAIN-transcript tokens to waste classes (priority order), reusing
# audit_tokens.py's loader and classifiers. Run from repo root: python3 audit_rank.py
import os, re, collections
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audit_tokens.py')
__file__ = _p
exec(open(_p).read().split('# ---------------- output')[0])
SUITE = re.compile(r'run_checks\.py|test_db_integrity|scripts/tests/test_|pytest|research_batch_dod|preflight\.sh|scripts/audit/\w+\.py')
MUT = re.compile(r'sed -i|git (merge|pull|fetch)|migrate_db|emit_|regenerate|build_site|context_map\.py|db\.py\s+(?:--\S+\s+)*(add-|amend-|observe-|correct-|relate-|derive-|adjudicate-|update-|upsert-|resolve-|reattribute-|retire-|log-mining|close-gap|delete-)|cat >|> [\w./]|tee |\bmv |\bcp |\brm ')
cls_tok = collections.Counter(); cls_n = collections.Counter(); main_total = 0
per_sess = {}
for sid, S_ in sessions.items():
    M = S_['main']; calls = M['calls']; main_total += sum(c['tot'] for c in calls)
    label = {}
    bounds = sorted({t[0] for t in M['triggers']} | {0, len(calls)})
    for a, b in zip(bounds, bounds[1:]):
        seg = calls[a:b]
        if seg and seg[0]['trig'] in ('notification', 'stop-hook') and all(is_house(n, i) for c in seg for _, n, i in c['tools']):
            for c in seg: label[c['i']] = ('1 notification wake, housekeeping only' if seg[0]['trig'] == 'notification' else '2 stop-hook cycle, housekeeping only')
    seen = {}; dirty = {}
    for c in calls:
        if c['i'] in label: continue
        share = c['tot'] / max(1, len(c['tools'])); lab = None
        for _, n, i in c['tools']:
            cmd = re.sub(r'GUIDEBOOK_DB_PATH=\S+', '', i.get('command', '')) if n == 'Bash' else ''
            if n in ('Edit', 'Write') or MUT.search(cmd):
                for k in dirty: dirty[k] = True
            if n == 'Bash':
                norm = re.sub(r'\s+', ' ', cmd).strip()
                if norm in seen and not dirty.get(norm, True):
                    lab = '3 suite re-run, no intervening change' if SUITE.search(cmd) else '4 identical Bash re-run, no intervening change'
                    cls_tok[lab] += share; cls_n[lab] += 1; per_sess.setdefault(sid, collections.Counter())[lab] += share
                seen[norm] = 1; dirty[norm] = False
            elif n in ('ReadNotifications', 'mcp__github__pull_request_read', 'mcp__github__actions_list', 'mcp__github__actions_get', 'mcp__Claude_Code_Remote__send_later'):
                lab = '5 PR polling inside otherwise-productive episodes'
                cls_tok[lab] += share; cls_n[lab] += 1; per_sess.setdefault(sid, collections.Counter())[lab] += share
            elif n == 'Bash' and 'preserve_transcripts' in cmd:
                lab = '6 preserve_transcripts outside stop-hook cycles'
                cls_tok[lab] += share; cls_n[lab] += 1; per_sess.setdefault(sid, collections.Counter())[lab] += share
    for c in calls:
        if c['i'] in label:
            cls_tok[label[c['i']]] += c['tot']; cls_n[label[c['i']]] += 1; per_sess.setdefault(sid, collections.Counter())[label[c['i']]] += c['tot']
M_ = lambda x: f'{x/1e6:.0f}M'
print('EXCLUSIVE CALL-LEVEL ATTRIBUTION (main transcripts; subagent tokens excluded)')
for k in sorted(cls_tok): print(f'  {k}: {cls_n[k]} calls/tool-uses, {M_(cls_tok[k])} = {cls_tok[k]/main_total:.1%} of main')
print(f'  SUM {M_(sum(cls_tok.values()))} = {sum(cls_tok.values())/main_total:.1%} of main {M_(main_total)}')
print('\nPER SESSION')
for sid, c in per_sess.items(): print(' ', sid, {k[:1]: M_(v) for k, v in sorted(c.items())}, f'sum {M_(sum(c.values()))}')
# stop-hook triggers before/after the 2026-09-18 16:37Z loop fix
import datetime as dt
fix = dt.datetime(2026, 9, 18, 16, 37, tzinfo=dt.timezone.utc)
pre = post = 0
for sid, S_ in sessions.items():
    for t in S_['main']['triggers']:
        if t[1] == 'stop-hook':
            if ts(t[2]) < fix: pre += 1
            else: post += 1
print(f'\nstop-hook feedback triggers before fix_stop_hook_loop.sh landed (2026-09-18 16:37Z): {pre}; after: {post}')
