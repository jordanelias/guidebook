#!/usr/bin/env python3
"""Print context around regex hits in a source's held text. usage: ctx.py REF-xxxxx 'regex' [width] [max]"""
import re, sys
sys.path.insert(0, 'scripts/research')
import retrieval_log as rl

ref, pat = sys.argv[1], sys.argv[2]
width = int(sys.argv[3]) if len(sys.argv) > 3 else 220
cap = int(sys.argv[4]) if len(sys.argv) > 4 else 12
rx = re.compile(pat, re.I)
seen = 0
for a in rl.artefacts_for_source(ref):
    p = str(a['path'])
    if not (a['exists'] and p.endswith(('.txt', '.html', '.xml', '.json'))):
        continue
    t = open(p, encoding='utf8', errors='ignore').read()
    t = re.sub(r'<[^>]+>', ' ', t) if p.endswith(('.html', '.xml')) else t
    t = re.sub(r'\s+', ' ', t)
    last = -10**9
    for m in rx.finditer(t):
        if m.start() - last < width:
            continue
        last = m.start()
        print(f'[{p.rsplit("/", 1)[-1]} @{m.start()}] ...{t[max(0, m.start() - width // 2):m.end() + width]}...\n')
        seen += 1
        if seen >= cap:
            sys.exit()
