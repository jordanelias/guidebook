#!/usr/bin/env python3
"""Schema walkability: every table, and how you reach the rest of the schema from it.

WHAT WRONG THING REACHES THE GUIDEBOOK WITHOUT THIS (CLAUDE.md §8's test).

CLAUDE.md rule 5 is "never write the same fact into a second table; point, do not copy",
and §3 says the pointer's physical form is a view joining two stages on a shared id:
"A cross-stage view IS the pointer, and is therefore the most protected object in the
schema. Before deleting any view, ask which stages it spans."

NOTHING IN THIS REPOSITORY COULD ANSWER THAT QUESTION. `governance/stage-map.yaml`
assigns a stage to every table, and its own header records the gap: "STILL OWED: the 20
views. §8 specifies a `pointer:` list naming the stages each view spans." So a session
deciding whether a view is dead apparatus or the one pointer holding two stages together
had to work it out by hand, from the view SQL, every time -- and rule 5's failure mode is
that when the pointer goes, the next reader copies the fact instead. Migration 064 exists
because a sweep missed `v_item_provenance`; a byte-exact diff called it clean because the
view rendered 0 rows. A 0-row view and a deleted pointer look identical from the data.

This derives the answer instead of asking anyone to maintain it: which stages each view
spans comes from the tables its SQL names, crossed with the stage map. It is therefore a
DERIVATION, not a second home -- if stage-map.yaml ever grows the `pointer:` list §8
specifies, this page becomes the check on it rather than a rival to it.

It also answers the ordinary question the schema makes hard: from this table, what can I
actually reach, and what reaches me? 97 columns on `evidence_sources` and 15 incoming
foreign keys are not something a person holds in their head.

EVERYTHING HERE IS DERIVED FROM THE LIVE SCHEMA AND THE TWO GOVERNANCE FILES. No table
list, no edge list and no row count is written down in this module (rule 7a). Stage ids
come from `governance/pipeline-contract.yaml`, table→stage from `governance/stage-map.yaml`
-- both read, neither copied.

    python3 tools/schema_walkability.py           # write tools/schema-walkability.html
    python3 tools/schema_walkability.py --check   # is the committed file current?
"""
import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
# GUIDEBOOK_DB_PATH, not a hardcoded path. db_path_env_audit caught this on the first
# run of this tool and the refusal is worth keeping in view: a script that ignores the
# variable reads the COMMITTED database while a test believes it is reading a scratch
# copy, so the test passes against the wrong bytes and says nothing about the change.
DB = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO_ROOT / "data" / "guidebook.db"))
CONTRACT = REPO_ROOT / "governance" / "pipeline-contract.yaml"
STAGE_MAP = REPO_ROOT / "governance" / "stage-map.yaml"
DEFAULT_OUT = REPO_ROOT / "tools" / "schema-walkability.html"
INFRA = "infrastructure"


def load_stages():
    import yaml
    with open(CONTRACT, encoding="utf-8") as fh:
        return [s["id"] for s in yaml.safe_load(fh)["stages"]]


def load_stage_map():
    import yaml
    with open(STAGE_MAP, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    return doc["tables"], doc.get("disputed", {})


def connect_ro(path):
    return sqlite3.connect(f"file:{path}?mode=ro", uri=True)


def collect(con):
    """Every fact the page renders, read off the live schema."""
    tables = [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    views = [(r[0], r[1] or "") for r in con.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='view' ORDER BY name")]

    rows, cols = {}, {}
    for t in tables:
        rows[t] = con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
        cols[t] = [{"name": c[1], "type": c[2], "notnull": bool(c[3]), "pk": bool(c[5])}
                   for c in con.execute(f'PRAGMA table_info("{t}")')]

    empty = {t for t in tables if rows[t] == 0}

    # Foreign keys: the edges. `from` is this table's column, `table`/`to` the referent.
    edges = []
    for t in tables:
        for f in con.execute(f'PRAGMA foreign_key_list("{t}")'):
            target, from_col, to_col = f[2], f[3], f[4]
            notnull = any(c["name"] == from_col and c["notnull"] for c in cols[t])
            edges.append({"src": t, "dst": target, "col": from_col,
                          "to_col": to_col, "notnull": notnull,
                          # CLAUDE.md §4: a NOT NULL FK into an EMPTIED table makes this
                          # table unwritable, and the refusal comes at INSERT, never at
                          # migration time -- so the schema looks healthy and every gate
                          # stays green over a table that cannot accept a row.
                          "dead": notnull and target in empty})

    # Which tables a view names. COMMENTS ARE STRIPPED FIRST: view_reads is the sole
    # input to spanned(), which decides whether a view is flagged a cross-stage POINTER --
    # the verdict this page exists to supply and the one a session consults before
    # deleting a view. A table named only in a `-- comment` would promote a non-crossing
    # view to POINTER, or pad the read-list a reader trusts. Measured: v_item_provenance's
    # SQL comment mentions evidence_source_authors, and the unstripped scan reported that
    # table as one the view reads. dbcore already has the stripper, so this reuses it
    # rather than writing a second one (rule 5).
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import dbcore
    views = [(v, dbcore._strip_sql_line_comments(sql)) for v, sql in views]

    def named_in(sql, name):
        i, n = 0, len(name)
        while (i := sql.find(name, i)) != -1:
            before = sql[i - 1] if i else " "
            after = sql[i + n] if i + n < len(sql) else " "
            if not (before.isalnum() or before == "_") and \
               not (after.isalnum() or after == "_"):
                return True
            i += n
        return False

    view_reads = {v: sorted(t for t in tables if named_in(sql, t)) for v, sql in views}
    view_rows = {}
    for v, _ in views:
        try:
            view_rows[v] = con.execute(f'SELECT COUNT(*) FROM "{v}"').fetchone()[0]
        except sqlite3.Error:
            view_rows[v] = None
    return tables, views, rows, cols, edges, view_reads, view_rows, empty


def build(con):
    stages = load_stages()
    stage_of, disputed = load_stage_map()
    tables, views, rows, cols, edges, view_reads, view_rows, empty = collect(con)

    def stage(t):
        return stage_of.get(t, "UNASSIGNED")

    # A view CROSSES stages when the tables it reads sit in more than one stage.
    # CLAUDE.md §3's convention: `base` is not a stage for this purpose, so a view
    # reading one stage plus base crosses nothing. Infrastructure is excluded on the
    # same reasoning -- it is not a pipeline position.
    def spanned(names):
        return sorted({stage(t) for t in names} - {"base", INFRA, "UNASSIGNED"})

    view_info = []
    for v, sql in views:
        reads = view_reads[v]
        sp = spanned(reads)
        view_info.append({
            "name": v, "reads": reads, "spans": sp, "crosses": len(sp) > 1,
            "rows": view_rows[v],
            "sql": sql.strip(),
        })

    out_by, in_by = {t: [] for t in tables}, {t: [] for t in tables}
    for e in edges:
        out_by[e["src"]].append(e)
        if e["dst"] in in_by:
            in_by[e["dst"]].append(e)

    tinfo = []
    for t in tables:
        dead = [e for e in out_by[t] if e["dead"]]
        tinfo.append({
            "name": t, "stage": stage(t), "rows": rows[t],
            "cols": cols[t], "ncols": len(cols[t]),
            "out": out_by[t], "in": in_by[t],
            "unwritable": bool(dead),
            "unwritable_via": [f'{e["col"]} -> {e["dst"]}' for e in dead],
            "views": sorted(v["name"] for v in view_info if t in v["reads"]),
            "disputed": disputed.get(t),
            # An ISLAND has no foreign key in either direction. Rule 5 says reach a fact
            # by pointer; a table nothing points at and which points at nothing cannot be
            # reached that way, so either it is genuinely standalone vocabulary or its
            # pointer was never built.
            "island": not out_by[t] and not in_by[t],
        })

    # NO DATE AND NO COMMIT SHA IN THE RENDERED BYTES, and this is a repair rather than a
    # preference. The first version of this file stamped date.today() and the short HEAD
    # sha into the page. --check compares byte-for-byte, so the stamp guaranteed the page
    # could NEVER match: committing it moves HEAD, so the committed file records the
    # previous sha forever, and the date rolls over nightly. Measured on the branch that
    # introduced it -- committed 4c9a38e against HEAD ab695e6, --check STALE, and
    # schema_walkability_fresh red. That is a gate red by construction, which the registry
    # note added alongside it argues against in its own words, and it also broke
    # scripts/regenerate_derived.sh, which runs every --check under `set -euo pipefail`.
    #
    # The page's content is a pure function of the schema and the two governance files, so
    # it is rendered as one. WHEN it was generated is already recorded, exactly once and
    # without anyone maintaining it, by git: `git log -1 -- tools/schema-walkability.html`.
    # Writing it into the page as well is rule 7a's own target -- a fact copied beside the
    # thing that already knows it, which then goes stale on its own.
    return {
        "schema_version": con.execute("PRAGMA user_version").fetchone()[0],
        "spine": stages,
        "stage_order": stages + [INFRA, "UNASSIGNED"],
        "tables": tinfo,
        "views": view_info,
        "counts": {
            "tables": len(tinfo),
            "views": len(view_info),
            "edges": len(edges),
            "empty": len(empty),
            "unwritable": sum(1 for t in tinfo if t["unwritable"]),
            "islands": sum(1 for t in tinfo if t["island"]),
            "crossing_views": sum(1 for v in view_info if v["crosses"]),
        },
    }


PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Schema Walkability</title>
<style>
:root{--bg:#fbfaf8;--panel:#fff;--ink:#1a1a1a;--dim:#6b6b6b;--line:#e2ded7;
 --accent:#7a4b2a;--warn:#9a3412;--ok:#2f6b47;--chip:#f0ece5;--hl:#fff8e6}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
 --bg:#14151a;--panel:#1c1e25;--ink:#e9e6e1;--dim:#9a968f;--line:#2e313a;
 --accent:#d9a066;--warn:#f08a5d;--ok:#6fc08d;--chip:#262932;--hl:#2a2418}}
:root[data-theme="dark"]{--bg:#14151a;--panel:#1c1e25;--ink:#e9e6e1;--dim:#9a968f;
 --line:#2e313a;--accent:#d9a066;--warn:#f08a5d;--ok:#6fc08d;--chip:#262932;--hl:#2a2418}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
 font:15px/1.55 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:1500px;margin:0 auto;padding:24px 16px 80px}
h1{font-size:26px;margin:0 0 4px;letter-spacing:-.01em}
.sub{color:var(--dim);font-size:13.5px;margin-bottom:6px}
code,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px}
.spine{margin:14px 0 18px;padding:10px 12px;background:var(--panel);
 border:1px solid var(--line);border-radius:10px;overflow-x:auto;white-space:nowrap}
.spine b{color:var(--accent)}
.bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:14px}
input[type=search]{flex:1 1 260px;min-width:0;padding:9px 12px;border:1px solid var(--line);
 border-radius:8px;background:var(--panel);color:var(--ink);font-size:14px}
select,button{padding:9px 11px;border:1px solid var(--line);border-radius:8px;
 background:var(--panel);color:var(--ink);font-size:13.5px;cursor:pointer}
button.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.stats{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;
 padding:8px 13px;min-width:92px}
.stat b{display:block;font-size:21px;line-height:1.2}
.stat span{font-size:11.5px;color:var(--dim);text-transform:uppercase;letter-spacing:.05em}
.cols{display:grid;grid-template-columns:minmax(0,340px) minmax(0,1fr);gap:16px}
@media (max-width:900px){.cols{grid-template-columns:1fr}}
.list{background:var(--panel);border:1px solid var(--line);border-radius:10px;
 max-height:72vh;overflow:auto}
.row{padding:8px 12px;border-bottom:1px solid var(--line);cursor:pointer;
 display:flex;gap:8px;align-items:baseline}
.row:last-child{border-bottom:0}
.row:hover{background:var(--hl)}
.row.sel{background:var(--chip);box-shadow:inset 3px 0 0 var(--accent)}
.row .nm{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis}
.row .ct{color:var(--dim);font-size:12px}
.chip{display:inline-block;padding:1px 7px;border-radius:999px;background:var(--chip);
 color:var(--dim);font-size:10.5px;letter-spacing:.04em;text-transform:uppercase}
.chip.w{background:var(--warn);color:#fff}
.chip.k{background:var(--accent);color:#fff}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}
.panel h2{margin:0 0 2px;font-size:20px}
.panel h3{margin:20px 0 7px;font-size:12.5px;text-transform:uppercase;
 letter-spacing:.06em;color:var(--dim)}
.note{border-left:3px solid var(--warn);padding:9px 12px;background:var(--hl);
 border-radius:0 8px 8px 0;margin:12px 0;font-size:13.5px}
.note.ok{border-left-color:var(--ok)}
ul.edges{list-style:none;margin:0;padding:0}
ul.edges li{padding:6px 0;border-bottom:1px dashed var(--line)}
ul.edges li:last-child{border-bottom:0}
a.tl{color:var(--accent);cursor:pointer;text-decoration:none;border-bottom:1px dotted}
a.tl:hover{text-decoration:none;border-bottom-style:solid}
.x{color:var(--warn);font-weight:600}
.muted{color:var(--dim)}
pre{background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:11px;
 overflow:auto;font-size:12px;margin:8px 0 0}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media (max-width:760px){.grid2{grid-template-columns:1fr}}
.empty{padding:28px;text-align:center;color:var(--dim)}
footer{margin-top:28px;color:var(--dim);font-size:12.5px;line-height:1.7}
</style></head><body><div class="wrap">
<h1>Schema Walkability</h1>
<div class="sub">Every table, what it points at, what points at it &mdash; and which views
carry a fact across a stage boundary. Derived from the live schema; nothing here is
maintained by hand.</div>
<div class="spine mono" id="spine"></div>
<div class="stats" id="stats"></div>
<div class="bar">
  <input type="search" id="q" placeholder="Filter tables and views&hellip;" autocomplete="off">
  <select id="stage"></select>
  <button id="fUn">Unwritable</button>
  <button id="fIs">Islands</button>
  <button id="fEm">Empty</button>
  <button id="fVw">Crossing views</button>
</div>
<div class="cols">
  <div class="list" id="list"></div>
  <div class="panel" id="detail"></div>
</div>
<footer id="foot"></footer>
</div>
<script id="data" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('data').textContent);
const T=Object.fromEntries(D.tables.map(t=>[t.name,t]));
const F={un:false,is:false,em:false,vw:false};
let sel=null;
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

document.getElementById('spine').innerHTML='SPINE: <b>'+D.spine.join('</b> &rarr; <b>')+'</b>';
const C=D.counts;
document.getElementById('stats').innerHTML=[
 ['tables',C.tables],['views',C.views],['fk edges',C.edges],['empty',C.empty],
 ['unwritable',C.unwritable],['islands',C.islands],['crossing views',C.crossing_views]
].map(([k,v])=>`<div class="stat"><b>${v}</b><span>${k}</span></div>`).join('');

const sg=document.getElementById('stage');
sg.innerHTML='<option value="">every stage</option>'+
  D.stage_order.map(s=>`<option value="${s}">${s}</option>`).join('');

function items(){
  const q=document.getElementById('q').value.trim().toLowerCase();
  const st=sg.value;
  let ts=D.tables.filter(t=>
     (!q||t.name.toLowerCase().includes(q))&&(!st||t.stage===st)&&
     (!F.un||t.unwritable)&&(!F.is||t.island)&&(!F.em||t.rows===0));
  let vs=D.views.filter(v=>(!q||v.name.toLowerCase().includes(q))&&
     (!F.vw||v.crosses)&&(!st||v.spans.includes(st))&&!F.un&&!F.is&&!F.em);
  if(F.vw) ts=[];
  return {ts,vs};
}
function renderList(){
  const {ts,vs}=items();
  const el=document.getElementById('list');
  if(!ts.length&&!vs.length){el.innerHTML='<div class="empty">Nothing matches.</div>';return}
  el.innerHTML=
   ts.map(t=>`<div class="row ${sel===t.name?'sel':''}" data-k="t:${esc(t.name)}">
     <span class="nm mono">${esc(t.name)}</span>
     ${t.unwritable?'<span class="chip w">unwritable</span>':''}
     ${t.island?'<span class="chip">island</span>':''}
     <span class="ct">${t.rows}</span>
     <span class="chip">${esc(t.stage)}</span></div>`).join('')+
   vs.map(v=>`<div class="row ${sel==='v:'+v.name?'sel':''}" data-k="v:${esc(v.name)}">
     <span class="nm mono">${esc(v.name)}</span>
     ${v.crosses?'<span class="chip k">pointer</span>':''}
     <span class="ct">${v.rows===null?'?':v.rows}</span></div>`).join('');
  el.querySelectorAll('.row').forEach(r=>r.onclick=()=>{show(r.dataset.k);});
}
function link(n){return `<a class="tl mono" onclick="show('t:${esc(n)}')">${esc(n)}</a>`}

function show(key){
  sel=key.startsWith('v:')?key:key.slice(2);
  renderList();
  const el=document.getElementById('detail');
  if(key.startsWith('v:')){
    const v=D.views.find(x=>x.name===key.slice(2));
    el.innerHTML=`<h2 class="mono">${esc(v.name)}</h2>
     <div class="sub">view &middot; renders ${v.rows===null?'?':v.rows} row(s)</div>
     ${v.crosses?`<div class="note"><b>This view is a POINTER.</b> It joins
       <b>${v.spans.join('</b> and <b>')}</b>. CLAUDE.md &sect;3: a cross-stage view is what
       &ldquo;point, do not copy&rdquo; means in SQL, and is the most protected object in
       the schema. Deleting it forces the next reader back to copying the fact.
       ${v.rows===0?'<br><br><b>It currently renders 0 rows</b> &mdash; which is exactly how migration 064&rsquo;s missed caller looked. Rule 4: treat a 0-row object as unproven, not clean.':''}</div>`
      :`<div class="note ok">Spans ${v.spans.length?'<b>'+v.spans.join('</b>, <b>')+'</b> only':'no pipeline stage'}
        &mdash; not a cross-stage pointer. (<code>base</code> and <code>infrastructure</code>
        are excluded by &sect;3&rsquo;s convention.)</div>`}
     <h3>Reads</h3><div>${v.reads.map(link).join(' &middot; ')||'<span class="muted">nothing resolvable</span>'}</div>
     <h3>Definition</h3><pre>${esc(v.sql)}</pre>`;
    return;
  }
  const t=T[key.slice(2)];
  if(!t){el.innerHTML='<div class="empty">Unknown.</div>';return}
  const out=t.out.map(e=>`<li>${e.notnull?'<b>NOT NULL</b> ':''}<code>${esc(e.col)}</code>
     &rarr; ${link(e.dst)}<code>.${esc(e.to_col)}</code>
     ${T[e.dst]&&T[e.dst].stage!==t.stage?`<span class="chip">${esc(t.stage)}&rarr;${esc(T[e.dst].stage)}</span>`:''}
     ${e.dead?'<span class="x"> &mdash; target is EMPTY, so this table cannot accept a row</span>':''}</li>`).join('');
  const inn=t.in.map(e=>`<li>${link(e.src)}<code>.${esc(e.col)}</code> &rarr;
     <code>${esc(e.to_col)}</code>${e.notnull?' <span class="muted">(required there)</span>':''}</li>`).join('');
  el.innerHTML=`<h2 class="mono">${esc(t.name)}</h2>
   <div class="sub">stage <b>${esc(t.stage)}</b> &middot; ${t.rows} row(s) &middot; ${t.ncols} columns</div>
   ${t.unwritable?`<div class="note"><b>UNWRITABLE.</b> ${t.unwritable_via.map(esc).join(', ')}.
     A NOT NULL foreign key into an emptied table refuses at INSERT, never at migration time
     (CLAUDE.md &sect;4) &mdash; so the schema looks healthy, a rebuild reproduces it exactly,
     and every gate stays green over a table that cannot take a row.</div>`:''}
   ${t.island?`<div class="note"><b>ISLAND.</b> No foreign key in either direction. Either it is
     standalone vocabulary, or its pointer was never built &mdash; and rule 5 says a fact is
     reached by pointer, so nothing here can be reached that way.</div>`:''}
   ${t.disputed?`<div class="note">Stage disputed: ${esc(JSON.stringify(t.disputed))}</div>`:''}
   <div class="grid2">
     <div><h3>Points at (${t.out.length})</h3>
       <ul class="edges">${out||'<li class="muted">nothing</li>'}</ul></div>
     <div><h3>Pointed at by (${t.in.length})</h3>
       <ul class="edges">${inn||'<li class="muted">nothing</li>'}</ul></div>
   </div>
   <h3>Read by views (${t.views.length})</h3>
   <div>${t.views.map(v=>`<a class="tl mono" onclick="show('v:${esc(v)}')">${esc(v)}</a>`).join(' &middot; ')||'<span class="muted">none</span>'}</div>
   <h3>Columns</h3>
   <div class="mono" style="font-size:12px">${t.cols.map(c=>
      `${esc(c.name)}<span class="muted">:${esc(c.type||'?')}${c.notnull?' NOT NULL':''}${c.pk?' PK':''}</span>`
    ).join(' &middot; ')}</div>`;
}
['q'].forEach(i=>document.getElementById(i).oninput=renderList);
sg.onchange=renderList;
[['fUn','un'],['fIs','is'],['fEm','em'],['fVw','vw']].forEach(([id,k])=>{
  document.getElementById(id).onclick=e=>{F[k]=!F[k];e.target.classList.toggle('on',F[k]);renderList();};
});
document.getElementById('foot').innerHTML=
 `Rendered from <code>data/guidebook.db</code> at schema version
  <b>${D.schema_version}</b>. This page carries no generation date and no commit sha on
  purpose: it is a pure function of the schema, so <code>--check</code> can compare it
  byte-for-byte. For WHEN it was last regenerated, ask git &mdash;
  <code>git log -1 -- tools/schema-walkability.html</code>. Stage ids from
  <code>governance/pipeline-contract.yaml</code>; table&rarr;stage from
  <code>governance/stage-map.yaml</code>. <b>Do not hand-edit this file</b> &mdash;
  regenerate with <code>scripts/regenerate_derived.sh</code>.<br>
  A view&rsquo;s stage span is DERIVED from the tables its SQL names. <code>stage-map.yaml</code>
  records the per-view <code>pointer:</code> list as still owed; this page computes it rather
  than waiting for it, so it is a derivation and not a second home.`;
renderList();
show('t:'+D.tables[0].name);
</script></body></html>
"""


def render(data):
    return PAGE.replace("__DATA__", json.dumps(data, separators=(",", ":")))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="exit non-zero if the committed file is not a fresh render")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    con = connect_ro(DB)
    try:
        data = build(con)
    finally:
        con.close()
    page = render(data)

    c = data["counts"]
    # EXAMINED, always, per CLAUDE.md §5(a): a check that passes having looked at
    # nothing is the failure mode this repository has produced four separate times.
    summary = (f"EXAMINED: {c['tables']} table(s), {c['views']} view(s), "
               f"{c['edges']} foreign-key edge(s)")

    if args.check:
        if not args.out.exists():
            print(f"MISSING: {args.out} — run: python3 tools/schema_walkability.py")
            print(summary)
            return 1
        if args.out.read_text(encoding="utf-8") != page:
            print(f"STALE: {args.out.name} differs from a fresh render. "
                  f"Run: python3 tools/schema_walkability.py")
            print(summary)
            return 1
        print(f"OK: {args.out.name} is current.")
        print(summary)
        return 0

    args.out.write_text(page, encoding="utf-8")
    print(f"wrote {args.out}  ({len(page)//1024} KB)  schema=v{data['schema_version']}  "
          f"unwritable={c['unwritable']}  islands={c['islands']}  "
          f"crossing-views={c['crossing_views']}")
    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
