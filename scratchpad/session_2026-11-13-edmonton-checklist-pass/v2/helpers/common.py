"""Replay of the REF-01037 digest: shared wrapper. Every db.py call runs against the
replay scratch copy with GUIDEBOOK_DB_PATH set inline in the child's environment, and
every call (argv, exit, output tail) is appended to the session's digest-log-v2.jsonl,
so a refusal's sentence is kept (ADJUDICATION Q10)."""
import json, os, subprocess, datetime
SC = '/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad/replay'
DB = SC + '/guidebook.db'
REPO = '/home/user/guidebook'
STEM = 'session_2026-11-13-edmonton-checklist-pass'
SESS = REPO + '/scratchpad/' + STEM
LOG = SESS + '/digest-log-v2.jsonl'
REF = 'REF-01037'
TEXT_SHA = '6e725b0be41f32d13870faf7ec538d19527d83593ecf12d1e7d39ffc48e9fd30'


def pdfp(item):
    """PDF page (one-based) of an item; 'p1' is the cover page."""
    if item == 'p1':
        return 1
    maj, mnr = (int(x) for x in item.split('.'))
    if maj == 1: return 2 if mnr <= 9 else 3
    if maj == 2: return 3
    if maj == 3: return 4
    if maj == 4: return 4 if mnr <= 5 else 5
    if maj == 5: return 5
    if maj in (6, 7): return 6
    if maj == 8: return 7
    if maj in (9, 10): return 8
    return 9


def loc(item):
    return f'PDF p. {pdfp(item)}' + ('' if item == 'p1' else f', item {item}')


def run(*argv, step=None, dry=False):
    a = list(argv) + (['--dry-run'] if dry else [])
    env = dict(os.environ, GUIDEBOOK_DB_PATH=DB)
    r = subprocess.run(['python3', 'scripts/db.py', *a], cwd=REPO, env=env,
                       capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    rec = {'ts': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
           'step': step or a[0], 'argv': a, 'exit': r.returncode, 'out': out[-1500:]}
    if not dry:
        with open(LOG, 'a') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    return r.returncode, out


def jid(out, key):
    try:
        return json.loads(out[out.index('{'):])[key]
    except Exception:
        return None
