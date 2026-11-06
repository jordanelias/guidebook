"""Fetch one URL through retrieval_log.fetch and print the artefact path. Run from the repo root:
python3 scratchpad/.../ZH-CN/tools/fetch.py URL 'what'"""
import sys, glob, os
sys.path.insert(0, 'scripts/research'); import retrieval_log as r
url, what = sys.argv[1], sys.argv[2]
before = set(glob.glob('retrieval-log/session_2026-11-06-base-vocabulary-review/*'))
try:
    r.fetch(url, session='session_2026-11-06-base-vocabulary-review', purpose='terminology pass ZH-CN: ' + what)
except Exception as e:
    print('EXC', type(e).__name__, str(e)[:300])
after = set(glob.glob('retrieval-log/session_2026-11-06-base-vocabulary-review/*'))
for p in sorted(after - before): print('NEW', p, os.path.getsize(p))
