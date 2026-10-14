#!/usr/bin/env python3
"""walkability.py: measure walkability in every direction over a database and a stage-map.
usage: walkability.py [DB [STAGE_MAP]] [--json]     (defaults: data/guidebook.db, governance/stage-map.yaml)
Read-only. Stage ids come from governance/pipeline-contract.yaml; table -> stage from the stage-map.
Edges: every FOREIGN KEY (child -> parent; a composite key counts once) and every table a view reads (the tables
named after FROM and JOIN once comments and string literals are stripped, through views that read views).
Per ordered stage pair (a before b in the spine):
  up        tables of b that reach a table of a by following FKs child -> parent (transitively, through any stage)
  down      tables of a that reach a table of b by following FKs parent -> child
  skip      as up, but never passing through a table of a stage between a and b
  recvFK    FKs whose child is in b and parent in a (the later stage holds the pointer back: the normal direction)
  sendFK    FKs whose child is in a and parent in b (the earlier stage holds a pointer forward: re-entrant)
Also: zigzag (shortest undirected path over FKs and view co-reads, never passing through a base, infrastructure
or unmapped table; ties go to fewer view hops, then alphabetical order; for all FKs and for FKs with at least one
non-NULL pointer), lateral components per stage (tables joined through a shared FK parent or child, or by a direct
FK between two tables of the stage), re-entrant FK edges with non-NULL counts, FK population, orphans, id columns
with no FK, and views that span stages. A view's stages are those of the tables it reads: a view that reads only
tables of one stage is one-stage whatever it is for.
"""
import sqlite3, sys, json, re, collections, itertools, yaml, os

repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
args = [a for a in sys.argv[1:] if a != '--json']
db = args[0] if args else os.path.join(repo, 'data/guidebook.db')
smap = args[1] if len(args) > 1 else os.path.join(repo, 'governance/stage-map.yaml')
as_json = '--json' in sys.argv
contract = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(smap))), 'governance/pipeline-contract.yaml')
if not os.path.exists(contract): contract = os.path.join(repo, 'governance/pipeline-contract.yaml')
spine = [s['id'] for s in yaml.safe_load(open(contract))['stages']]
st = yaml.safe_load(open(smap))['tables']
c = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
T = [r[0] for r in c.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
V = dict(c.execute("select name, sql from sqlite_master where type='view'").fetchall())
stage = {t: st.get(t, 'UNMAPPED') for t in T}
idx = {s: i for i, s in enumerate(spine)}

# FK edges: (child, parent, child_col, parent_col)
fk = []
for t in T:
    seen_id = set()
    for f in c.execute(f'pragma foreign_key_list("{t}")'):
        if f[2] in stage and f[0] not in seen_id:      # one edge per constraint, not per column
            seen_id.add(f[0]); fk.append((t, f[2], f[3], f[4]))
# view edges: view -> tables it reads (FROM/JOIN targets; comments and strings stripped; views expanded)
_KW = r'\b(?:WHERE|GROUP|ORDER|UNION|LIMIT|HAVING|JOIN|LEFT|RIGHT|INNER|CROSS|FULL|NATURAL|ON|USING|SELECT|EXCEPT|INTERSECT|WINDOW)\b|[();]'
def view_reads(v, seen=()):
    s = re.sub(r"--[^\n]*|/\*.*?\*/|'(?:[^']|'')*'", ' ', V[v], flags=re.S)
    names = set()
    for m in re.finditer(r'\b(?:FROM|JOIN)\b', s, re.I):
        for part in re.split(_KW, s[m.end():], maxsplit=1, flags=re.I)[0].split(','):
            w = part.strip().split()
            if w and re.fullmatch(r'"?\w+"?', w[0]): names.add(w[0].strip('"'))
    out = {n for n in names if n in stage}
    for n in names & set(V) - set(seen) - {v}: out |= view_reads(n, seen + (v,))
    return out
vedge = {v: sorted(view_reads(v)) for v in V}
def vstages(v): return sorted({stage[t] for t in vedge[v] if stage[t] in idx}, key=idx.get)

# adjacency (table graph)
up_adj = collections.defaultdict(set)     # child -> parents
down_adj = collections.defaultdict(set)   # parent -> children
for ch, pa, *_ in fk:
    up_adj[ch].add(pa); down_adj[pa].add(ch)

def reach(src_tables, adj, allowed=None):
    seen = set(src_tables); q = collections.deque(src_tables)
    while q:
        n = q.popleft()
        for m in adj[n]:
            if m in seen: continue
            if allowed is not None and not allowed(m): continue
            seen.add(m); q.append(m)
    return seen

by_stage = collections.defaultdict(list)
for t in T: by_stage[stage[t]].append(t)

out = {'spine': spine, 'tables': len(T), 'views': len(V), 'fk': len(fk)}

# --- up / down / skip over every ordered pair (a before b)
pairs = {}
for a, b in itertools.combinations(spine, 2):
    A, B = by_stage[a], by_stage[b]
    if not A or not B:
        pairs[f'{a}->{b}'] = dict(up=None, down=None, skip=None, note='empty stage'); continue
    # up: some table of B reaches some table of A via child->parent edges
    up = [t for t in B if reach([t], up_adj) & set(A)]
    # down: some table of A reaches some table of B via parent->child edges
    down = [t for t in A if reach([t], down_adj) & set(B)]
    inter = set(spine[idx[a] + 1: idx[b]])
    skip = None
    if inter:
        allowed = lambda m: stage[m] not in inter
        skip = [t for t in B if reach([t], up_adj, allowed) & set(A)]
    # direct (adjacent FK) count
    direct = [e for e in fk if stage[e[0]] == b and stage[e[1]] == a]
    send = [e for e in fk if stage[e[0]] == a and stage[e[1]] == b]
    pairs[f'{a}->{b}'] = dict(up=len(up), down=len(down), skip=(None if skip is None else len(skip)),
                              direct_fk=len(direct), send_fk=len(send), views=[v for v in vedge if {a, b} <= set(vstages(v))])
out['pairs'] = pairs

# --- lateral: per stage, connected components of same-stage tables via a shared parent/child (any stage)
lat = {}
for s in spine + ['infrastructure', 'UNMAPPED']:
    ts = by_stage.get(s, [])
    if not ts: continue
    par = {t: t for t in ts}
    def find(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    share = collections.defaultdict(list)
    for t in ts:
        for p in up_adj[t]: share[('p', p)].append(t)
        for ch in down_adj[t]: share[('c', ch)].append(t)
        for p in up_adj[t]:
            if p in par: par[find(t)] = find(p)
    for k, v in share.items():
        for x in v[1:]: par[find(x)] = find(v[0])
    comps = collections.defaultdict(list)
    for t in ts: comps[find(t)].append(t)
    lat[s] = dict(tables=len(ts), components=len(comps), isolated=sorted(v[0] for v in comps.values() if len(v) == 1))
out['lateral'] = lat

# --- re-entrant: FK edges and view spans going backwards
re_fk = [(ch, pa, cc) for ch, pa, cc, _ in fk if stage[ch] in idx and stage[pa] in idx and idx[stage[ch]] < idx[stage[pa]]]
out['reentrant_fk'] = [dict(child=ch, parent=pa, col=cc, rows=c.execute(f'select count(*) from "{ch}" where "{cc}" is not null').fetchone()[0]) for ch, pa, cc in re_fk]

# --- population of every FK: rows pointing / childless parents
pop = []
for ch, pa, cc, pc in fk:
    n = c.execute(f'select count(*) from "{ch}"').fetchone()[0]
    nn = c.execute(f'select count(*) from "{ch}" where "{cc}" is not null').fetchone()[0]
    pop.append(dict(child=ch, parent=pa, col=cc, rows=n, nonnull=nn))
out['fk_population'] = pop

# --- orphans: tables with no FK in or out and not read by any view
touched = {t for e in fk for t in e[:2]} | {t for v in vedge.values() for t in v}
out['orphans'] = sorted(t for t in T if t not in touched)
# unFK id columns: a column named like another table's single-col PK but with no FK
pk = collections.defaultdict(set)
for t in T:
    cols = c.execute(f'pragma table_info("{t}")').fetchall()
    p = [r[1] for r in cols if r[5]]
    if len(p) == 1: pk[p[0]].add(t)
fkcols = {(e[0], e[2]) for e in fk}
unfk = []
for t in T:
    for r in c.execute(f'pragma table_info("{t}")'):
        if r[1] in pk and t not in pk[r[1]] and (t, r[1]) not in fkcols:
            n = c.execute(f'select count(*) from "{t}" where "{r[1]}" is not null').fetchone()[0]
            unfk.append(dict(table=t, col=r[1], points_at=sorted(pk[r[1]]), nonnull=n))
out['unfk_ids'] = unfk
# --- views spanning stages
out['view_spans'] = {v: vstages(v) for v in sorted(vedge) if len(vstages(v)) > 1}
out['views_no_stage'] = sorted(v for v in vedge if len(vstages(v)) <= 1)


# --- zigzag walk: shortest undirected path between any table of stage a and any table of stage b, FK edges + view co-reads,
#     never passing THROUGH a base, infrastructure or unmapped table (base is shared vocabulary: it connects everything and
#     walks nothing; the others are not spine stages).
NOWALK = {'base', 'infrastructure', 'UNMAPPED'}
def build(fk_set, views):
    g = collections.defaultdict(set)
    for ch, pa in fk_set: g[ch].add(pa); g[pa].add(ch)
    for v in views:
        ts = [x for x in vedge[v] if x in stage]
        for x in ts:
            for y in ts:
                if x != y: g[x].add(y)
    return g
fkpairs = {(ch, pa) for ch, pa, *_ in fk}
live_fk = {(ch, pa) for ch, pa, cc, _ in fk if c.execute(f'select 1 from "{ch}" where "{cc}" is not null limit 1').fetchone()}
live_v = set()
for v in vedge:
    try:
        if c.execute(f'select 1 from "{v}" limit 1').fetchone(): live_v.add(v)
    except Exception: pass
def shortest(g, fks, src, dst):
    """fewest hops; among equal lengths the fewest view hops, then alphabetical: computed over ALL shortest paths"""
    best = None
    for s0 in sorted(src):
        layer = {s0: (0, (s0,))}; seen = {s0}
        while layer:
            hit = [(v, p) for n, (v, p) in layer.items() if n in dst]
            if hit:
                cand = min((v, p) for v, p in hit)
                if best is None or (len(cand[1]), cand[0], cand[1]) < (len(best[1]), best[0], best[1]): best = cand
                break
            nxt = {}
            for n, (v, p) in layer.items():
                if n != s0 and stage[n] in NOWALK: continue
                for m in sorted(g[n]):
                    if m in seen: continue
                    cand = (v + (not ((n, m) in fks or (m, n) in fks)), p + (m,))
                    if m not in nxt or cand < nxt[m]: nxt[m] = cand
            seen |= set(nxt); layer = nxt
    return None if best is None else list(best[1])
def fmt(path, fks, views):
    """a path with each hop labelled: ' - ' for a foreign key, ' ~view~ ' for two tables a view reads together"""
    s = path[0]
    for x, y in zip(path, path[1:]):
        if (x, y) in fks or (y, x) in fks: s += f' - {y}'
        else: s += f' ~{next(v for v in sorted(views) if x in vedge[v] and y in vedge[v])}~ {y}'
    return s
nonbase = [s for s in spine if s != 'base']
g_all, g_live = build(fkpairs, vedge), build(live_fk, live_v)
zz, zzp = {}, {}
for a, b in itertools.combinations(nonbase, 2):
    A, B = by_stage[a], by_stage[b]
    zz[f'{a}<->{b}'] = shortest(g_all, fkpairs, A, set(B)) if A and B else None
    zzp[f'{a}<->{b}'] = shortest(g_live, live_fk, A, set(B)) if A and B else None
out['zigzag'], out['zigzag_populated'] = zz, zzp

if as_json:
    print(json.dumps(out, indent=1, default=str)); sys.exit()
print(f"tables {out['tables']}  views {out['views']}  fk {out['fk']}")
print('\nSTAGE-PAIR MATRIX (tables in later stage that reach an earlier stage / tables in earlier stage that reach later; skip = reach without crossing the intermediate stages)')
print(f"{'pair':28} {'up':>4} {'down':>5} {'skip':>5} {'recvFK':>7} {'sendFK':>7}  views")
for k, v in pairs.items():
    if v.get('note'): print(f'{k:28} {v["note"]}'); continue
    print(f"{k:28} {v['up']:>4} {v['down']:>5} {str(v['skip']):>5} {v['direct_fk']:>7} {v['send_fk']:>7}  {','.join(v['views'])[:60]}")
print('\nZIGZAG WALK between non-base stages (shortest undirected path over FKs and view co-reads, not passing through base, infrastructure or unmapped tables; - is a foreign key, ~v~ a view that reads both):')
for k, pth in zz.items(): print(f"  {k:30} " + (fmt(pth, fkpairs, vedge) if pth else 'NO PATH'))
print('\nZIGZAG, POPULATED EDGES ONLY (an FK counts if some child row has a non-NULL pointer; a view if it returns a row):')
for k, pth in zzp.items(): print(f"  {k:30} " + (fmt(pth, live_fk, live_v) if pth else 'NO PATH'))
print('\nLATERAL (components of same-stage tables joined through a shared parent or child)')
for s, v in lat.items(): print(f"  {s:15} tables {v['tables']:>2} components {v['components']:>2}  isolated: {', '.join(v['isolated'])[:110]}")
print('\nRE-ENTRANT FK edges (child stage earlier than parent stage):')
for r in out['reentrant_fk']: print(f"  {r['child']}.{r['col']} -> {r['parent']}  non-null rows {r['rows']}")
print('\nORPHANS (no FK in/out, no view reads):', ', '.join(out['orphans']))
print('\nunFK id columns:')
for r in unfk: print(f"  {r['table']}.{r['col']} (-> {', '.join(r['points_at'])}) non-null {r['nonnull']}")
print('\nVIEWS spanning >1 stage:', len(out['view_spans']))
for v, s in out['view_spans'].items(): print(f'  {v}: {" + ".join(s)}')
print('views confined to one stage or none:', ', '.join(out['views_no_stage']))
