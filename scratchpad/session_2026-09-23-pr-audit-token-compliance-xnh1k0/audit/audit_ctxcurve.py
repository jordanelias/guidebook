# Context growth curve per main transcript: API call index at which ctx first exceeds 250k/500k/700k,
# median per-call ctx growth, and compaction events (trigger, preTokens). Run from repo root.
import os, statistics
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audit_tokens.py'); __file__ = _p
exec(open(_p).read().split('# ---- branch -> merged PRs')[0])
for sid, S_ in sessions.items():
    M = S_['main']; cs = M['calls']; ctx = [c['ctx'] for c in cs]
    first = lambda th: next((i for i, x in enumerate(ctx) if x > th), None)
    d = [b - a for a, b in zip(ctx, ctx[1:]) if 0 <= b - a < 100000]
    print(f"{sid} calls={len(cs)} first>250k@{first(250000)} >500k@{first(500000)} >700k@{first(700000)} median_growth/call={statistics.median(d):.0f} tok compactions={[(ci, pt) for ci, _, pt in M['compacts']]}")
