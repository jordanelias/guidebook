"""Equivalents pass IT-IT: log the prior, then fetch through retrieval_log, then extract text.
Run from the repository ROOT: python3 <this> "<prior>" "<url>" "<what>"
Appends the prior to equivalents-search-log.md BEFORE fetch(); prints artefact path, status, text path."""
import sys, os, re, json, glob, subprocess, hashlib, html
sys.path.insert(0, 'scripts/research')
import retrieval_log as r
D = 'scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/IT-IT'
prior, url, what = sys.argv[1:4]
with open(f'{D}/equivalents-search-log.md', 'a', encoding='utf-8') as f:
    f.write(f'\n### FETCH {url}\n- what: {what}\n- prior (written before fetch): {prior}\n')
S = 'session_2026-11-06-base-vocabulary-review'
r.fetch(url, session=S, purpose=f'equivalents IT-IT: {what}')
man = sorted(glob.glob(f'retrieval-log/{S}/*.jsonl'))
last = None
for m in man:
    for line in open(m, encoding='utf-8'):
        try:
            j = json.loads(line)
        except Exception:
            continue
        if j.get('url') == url:
            last = j
print(json.dumps({k: last.get(k) for k in last} if last else {}, ensure_ascii=False)[:600])
