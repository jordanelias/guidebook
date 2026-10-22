import sqlite3, re, sys
sys.path.insert(0,'scripts')
import db
OUT=sys.argv[1]
VB, IC = db._VALUE_BEARING, db._ITEM_CODE
c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
out=[]; w=out.append
uv=c.execute('pragma user_version').fetchone()[0]
w("# Search slugs and parameters, as the database holds them (2026-10-22)\n")
w(f"Read-only listing. Re-derive, do not quote: every figure is the result of a query against `data/guidebook.db` (user_version {uv}). The screen is the one `db.py mint-term-from-catalogue` applies: `db._VALUE_BEARING` (a digit, a comparator or a min/max word) and `db._ITEM_CODE` (an old `[A-Z]-NN` code). Nothing here has been written to the database.\n")
w("## 1. Parameters (`base_parameters`)\n")
w("| id | term | name | status | direction | extractions | live determinations | fails value screen | item code |")
w("|---|---|---|---|---|---|---|---|---|")
for pid,tid,st,direc in c.execute("select parameter_id,term_id,status,accessibility_direction from base_parameters order by 1"):
    n,df=c.execute("select canonical_en,definition from terms where term_id=?",(tid,)).fetchone()
    x=c.execute("select count(*) from source_value_extractions where parameter_id=?",(pid,)).fetchone()[0]
    s=c.execute("select count(*) from specifications where parameter_id=? and retired_at is null",(pid,)).fetchone()[0]
    m=VB.search(n) or VB.search(df or '')
    w(f"| {pid} | {tid} | {n} | {st} | {direc or '-'} | {x} | {s} | {('YES: '+repr(m.group(0))) if m else 'no'} | {'YES' if IC.search(n) else 'no'} |")
w("\nDeclined as a parameter (`parameter_declinations`):")
for tid,reason in c.execute("select term_id,reason from parameter_declinations"): w(f"- {tid}: {reason}")
w("\n## 2. The vocabulary the parameters come from (`terms`)\n")
w("Only terms marked P are parameters. The rest are elements, concepts, conditions, populations and methods. V = the name or definition fails the value screen.\n")
pids={r[0]:r[1] for r in c.execute("select term_id,parameter_id from base_parameters")}
dec={r[0] for r in c.execute("select term_id from parameter_declinations")}
cur=None; nV=0
for d,t,n,df in c.execute("select domain,term_id,canonical_en,definition from terms order by domain,term_id"):
    if d!=cur: w(f"\n**{d}**"); cur=d
    m=VB.search(n) or VB.search(df or ''); nV+=1 if m else 0
    flags=("P%d"%pids[t] if t in pids else ("declined" if t in dec else ""))+(f" V({m.group(0)!r})" if m else "")
    na=c.execute("select count(*) from term_aliases where term_id=?",(t,)).fetchone()[0]
    w(f"- {t} {n}  [{flags.strip() or '-'}] aliases={na}")
w(f"\nTerms failing the value screen: {nV} of {c.execute('select count(*) from terms').fetchone()[0]}. The 17 terms in domain `functional_axis` are named \"... demand\" and are not quantities.")
w(f"\n## 3. Search slugs (`slugs`, {c.execute('select count(*) from slugs').fetchone()[0]} rows)\n")
w("A slug is a research TOPIC. It is not a parameter and no column links one to the other. Counts: sources linked (`source_slug_links`), searches logged (`search_executions`).\n")
w("Status: "+", ".join(f"{s}={n}" for s,n in c.execute("select status,count(*) from slugs group by 1"))+"\n")
cur=None
for td,slug,st,mi in c.execute("select topic_directory,slug,status,merged_into from slugs order by topic_directory,slug"):
    if td!=cur:
        n=c.execute("select count(*) from slugs where topic_directory=?",(td,)).fetchone()[0]; w(f"\n**{td}** ({n})"); cur=td
    ns=c.execute("select count(*) from source_slug_links where slug=?",(slug,)).fetchone()[0]
    nx=c.execute("select count(*) from search_executions where slug=?",(slug,)).fetchone()[0]
    m=VB.search(slug.replace('-',' ')); fl=[]
    if m: fl.append(f"V({m.group(0)!r})")
    if IC.search(slug): fl.append("ITEM-CODE")
    w(f"- {slug}  [{st}{' -> '+mi if mi else ''}] sources={ns} searches={nx}{'  '+' '.join(fl) if fl else ''}")
bad=[(s,(VB.search(s.replace('-',' ')) or IC.search(s)).group(0)) for (s,) in c.execute("select slug from slugs") if VB.search(s.replace('-',' ')) or IC.search(s)]
w(f"\nSlugs failing the screen: {len(bad)} — "+"; ".join(f"{s} ({g!r})" for s,g in bad)+".")
w(f"Slugs with at least one search: {c.execute('select count(distinct slug) from search_executions').fetchone()[0]}. Slugs with at least one linked source: {c.execute('select count(distinct slug) from source_slug_links').fetchone()[0]}.")
open(OUT,"w").write("\n".join(out)+"\n")
print(len(out),"lines")
