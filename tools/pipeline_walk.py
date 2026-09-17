#!/usr/bin/env python3
"""Pipeline walk: what a session actually committed, stage by stage.

THE QUESTION THIS ANSWERS, and it is not the one the other dashboards answer.
`pipeline_completeness.py` reports how much of the pipeline is *done*;
`evidentiary_audit.py` grades what is *there*. Neither shows the thing a reviewer
needs before merging a batch: **which rows did this session write, into which
tables, in spine order** -- so a bad write is visible without reading a data
migration by hand.

Read-only on the DB. Writes only the HTML file.

DETERMINISM. The "as-of" is derived from the DB's own timestamps, never wall
clock, and every query is ordered, so identical inputs give byte-identical
output -- the guarantee `--check` relies on.

Usage:
  python3 tools/pipeline_walk.py                     # write the page
  python3 tools/pipeline_walk.py --check             # exit 1 if stale
  python3 tools/pipeline_walk.py --session <id>      # focus one session
  GUIDEBOOK_DB_PATH=... python3 tools/pipeline_walk.py
"""
from __future__ import annotations

import argparse
import html
import json
import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = REPO_ROOT / "data" / "guidebook.db"
DEFAULT_OUT = REPO_ROOT / "tools" / "pipeline-walk.html"
CONTRACT = REPO_ROOT / "governance" / "pipeline-contract.yaml"

#: Rows of any one table shown per session before truncating. Bounds the page
#: without hiding the fact: the header always prints the true total, so a
#: truncated table is visibly truncated rather than silently short.
ROW_CAP = 50

# ---------------------------------------------------------------------------
# Stages: read, never restated
# ---------------------------------------------------------------------------
# CLAUDE.md §3: `governance/pipeline-contract.yaml`'s `stages:` is THE SINGLE HOME
# of the stage ids, and the spine line is a rendering of it. A second copy in a
# tool is rule 7a's hard-coded list -- it goes stale with nothing going red.
# `tools/pipeline_completeness.py:38` holds exactly such a copy (`STAGES = [...]`
# under a comment naming the contract as its source); this module deliberately
# does not repeat it. If the contract gains or renames a stage, this page follows
# and that one does not.


def load_stages(contract_path: Path) -> list[str]:
    import yaml  # pinned project dependency; see governance/check-registry.yaml batteries
    with open(contract_path, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    return [s["id"] for s in doc["stages"]]


def stage_label(stage_id: str) -> str:
    """Display form is DERIVED from the id, never stored beside it (CLAUDE.md §3)."""
    return stage_id.replace("-", " ")


# ---------------------------------------------------------------------------
# Table -> stage: JUDGED, and it lives in a data file
# ---------------------------------------------------------------------------
# The judgments used to be a dict in this module. `architecture/meta-scripts-spec.md`
# §8 had already specified where they belong -- `governance/stage-map.yaml`, "one
# entry per table and view naming its stage id from pipeline-contract.yaml" --
# and named three consumers (L1.8, L2.6, L3.5) blocked on its absence. Keeping 77
# judgments inside a renderer meant none of them could read it, and whoever built
# L1 would have re-judged all 77: a second home, which is rule 5.
#
# One mapping, one set of values. `infrastructure` was a separate Python set
# beside the dict, which made it a fourth value of the same function implemented
# as a different structure -- nothing checked the two for overlap, and the stage
# validator never saw it. It is now just another value, so one validator covers
# every entry.
STAGE_MAP = REPO_ROOT / "governance" / "stage-map.yaml"
INFRA = "infrastructure"


def load_stage_map(path: Path) -> tuple[dict, dict]:
    import yaml
    with open(path, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    return doc["tables"], doc.get("disputed", {})


STAGE_OF, DISPUTED = load_stage_map(STAGE_MAP)


# ---------------------------------------------------------------------------
# Reading the database
# ---------------------------------------------------------------------------
def connect_ro(db_path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con


def live_tables(con) -> list[str]:
    return [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%' ORDER BY name")]


def columns(con, table, _cache={}) -> list[str]:
    """PRAGMA table_info, memoised for the life of one run.

    The DB is opened read-only and never mutated mid-run, so the schema cannot
    change under the cache. Measured before it existed: 529 PRAGMA calls over 77
    tables, a 6.87x redundancy, because session_col(), sessions(), rows_for() and
    as_of() each re-asked for the same table.
    """
    key = (id(con), table)
    if key not in _cache:
        _cache[key] = [r[1] for r in con.execute(f'PRAGMA table_info("{table}")')]
    return _cache[key]


# ---------------------------------------------------------------------------
# Session attribution: ONE HOME, and it is not this file
# ---------------------------------------------------------------------------
# `scripts/audit/batch_capture_report.py` already answers "what did this batch
# record, in every table" -- built on the owner request of 2026-09-16, one day
# before this module. Its attribution is strictly better than what this file
# first shipped, and re-deriving it here would give two tools that answer the
# same question differently about the same batch. So this imports it.
#
# WHAT THIS FILE GOT WRONG BY NOT LOOKING FIRST. Its session_col() matched two
# hardcoded names, `created_by_session` and `session`. The corpus uses at least
# eight: `worked_by_session` (source_locators, the largest table this map
# places), `applied_by_session`, `run_by_session`, `raised_by_session`,
# `resolved_by_session`, `attempted_by_session`, `checked_by_session`,
# `verified_by_session`. Fifteen of the eighteen tables this page named
# "not attributable to a session" were attributable -- eight directly and seven
# through a foreign key. A curated list of column names went blind exactly the
# way `dbcore.WRITABLE_TABLES` did eight times, inside the tool whose whole
# argument is that curated lists go blind.
sys.path.insert(0, str(REPO_ROOT / "scripts" / "audit"))
import batch_capture_report as _bcr  # noqa: E402


def attribution(con, tables) -> dict:
    """{table: (kind, sql_predicate)} for every live table. Derived, never listed.

    kind is DIRECT (the table carries a session column), FK (it reaches one
    through a foreign key, up to batch_capture_report.MAX_HOPS) or NONE. A NONE
    table is NAMED on the page rather than omitted: an absent row and an
    unattributable row are different facts.
    """
    direct = {t: cols for t in tables if (cols := _bcr._session_cols(con, t))}
    out = {}
    for t in tables:
        kind, pred, _path = _bcr._resolve(con, t, direct)
        out[t] = (kind, pred)
    return out


def sessions(con, tables, attrib, counts) -> list[dict]:
    """Every session id that wrote anything, with what it touched.

    Session ids ORIGINATE in DIRECT tables -- an FK-attributed row inherits its
    id from a parent -- so enumeration reads the direct ones and attribution
    then reaches the rest. Empty tables are skipped outright, which is what
    keeps this bounded as sessions accumulate.
    """
    seen: dict[str, dict] = {}
    for t in tables:
        kind, _pred = attrib[t]
        if kind != "DIRECT" or not counts[t]:
            continue
        cols = columns(con, t)
        sc = _bcr._session_cols(con, t)[0]
        stamp = "created_at" if "created_at" in cols else None
        # ONE GROUPED QUERY PER TABLE, not one per (session, table): this returns
        # every session's count for this table in a single pass, and the counts
        # are carried through to rows_for() rather than re-derived there.
        q = (f'SELECT "{sc}" AS s, COUNT(*) AS n'
             + (f', MIN("{stamp}") AS first' if stamp else ', NULL AS first')
             + f' FROM "{t}" WHERE "{sc}" IS NOT NULL GROUP BY "{sc}"')
        for row in con.execute(q):
            e = seen.setdefault(row["s"], {"id": row["s"], "rows": 0,
                                           "per_table": {}, "first": None})
            e["rows"] += row["n"]
            e["per_table"][t] = row["n"]
            if row["first"] and (e["first"] is None or row["first"] < e["first"]):
                e["first"] = row["first"]
    # FK-reached tables cannot be grouped in one pass, so they are counted per
    # session -- but only for non-empty ones, of which there are currently none.
    fk = [t for t in tables if attrib[t][0] == "FK" and counts[t]]
    for e in seen.values():
        for t in fk:
            n = con.execute(f'SELECT COUNT(*) FROM "{t}" WHERE {attrib[t][1]}',
                            (e["id"],)).fetchone()[0]
            if n:
                e["per_table"][t] = n
                e["rows"] += n
    out = list(seen.values())
    out.sort(key=lambda e: (e["first"] or "", e["id"]))
    return out


def rows_for(con, table, sess, pred, total) -> tuple[list[str], list[list]]:
    """The rows `sess` wrote into `table`. `total` is passed in, never re-counted."""
    cols = columns(con, table)
    if not total:
        return cols, []
    # A TOTAL ORDER, or the cap is nondeterministic and --check lies. cols[0] is
    # not unique in nine live tables -- term_aliases holds 2382 rows over 88
    # distinct term_id -- so `ORDER BY term_id LIMIT 50` picks 50 out of a huge
    # tie set and SQLite may break the tie differently on another build, after an
    # added index, or after VACUUM. `_rowid_` is the tiebreaker; a WITHOUT ROWID
    # table has none, so fall back to ordering on every column.
    allcols = ", ".join(f'"{c}"' for c in cols)
    for order in (f'"{cols[0]}", _rowid_', allcols):
        try:
            got = con.execute(
                f'SELECT * FROM "{table}" WHERE {pred} ORDER BY {order} '
                f'LIMIT {ROW_CAP}', (sess,)).fetchall()
            return cols, [list(r) for r in got]
        except sqlite3.OperationalError:
            continue
    raise RuntimeError(f"no total order available for {table}")


def unwritable(con, tables) -> dict:
    """CLAUDE.md §4's probe, collapsed to ROOTS rather than leaves.

    The raw probe returns 21 columns today. Printed flat that is a list a reader
    learns to skip -- the same argument this repo makes about a check that is red
    by construction. Nearly all of them are one empty table away from being
    writable: `items` alone accounts for most, and base_parameters -> specifications
    -> specification_source_links is a chain, not three independent facts. So the
    empty PARENTS are the finding and the columns are their consequence.

    IT STILL OVER-REPORTS, and the page says so. The probe asks only whether a
    parent is empty right now; where one db.py call inserts parent and child in
    the same transaction the write succeeds anyway -- connection_targets.con_id,
    identity_medical_map.medical_code and icf_medical_map.medical_code are all
    flagged and all fine. Only a child whose parent NOTHING fills is dead.

    A fuller version -- transitive collapse plus the softer class of NULLABLE FKs
    into empty tables, where the row is writable but the lens is not -- is specced
    as L1.7 in `architecture/meta-scripts-spec.md` and belongs with that module,
    not here.
    """
    empty = {t for t in tables
             if con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] == 0}
    roots: dict = {}
    for t in tables:
        dead = {f[3]: f[2] for f in con.execute(f'PRAGMA foreign_key_list("{t}")')
                if f[2] in empty}
        for c in con.execute(f'PRAGMA table_info("{t}")'):
            if c[1] in dead and c[3]:
                roots.setdefault(dead[c[1]], []).append(f"{t}.{c[1]}")
    return {k: sorted(v) for k, v in sorted(roots.items())}


def _norm_stamp(v) -> str:
    """One comparable form for three stored formats.

    The DB holds '2026-07-23T00:00:00Z', '2026-09-16 04:20' and bare '2026-08-19'
    in the same pair of column names. A raw string MAX puts 'T' (0x54) above ' '
    (0x20), so a midnight ISO stamp sorts above a same-day 23:59 space-separated
    one and the page would claim freshness as of 00:00 while rendering rows
    written at 23:59. Non-strings (an epoch int in a created_at) are coerced
    rather than compared against a str, which used to raise TypeError.
    """
    s = str(v or "").strip().replace("T", " ").rstrip("Z").strip()
    return s


def as_of(con, tables) -> str:
    """Derived from the DB's own timestamps, never wall clock (determinism)."""
    best = ""
    for t in tables:
        cols = set(columns(con, t))
        for c in ("updated_at", "created_at"):
            if c in cols:
                v = con.execute(f'SELECT MAX("{c}") FROM "{t}"').fetchone()[0]
                n = _norm_stamp(v)
                if n and n > best:
                    best = n
    return best or "unknown"


def gather(con) -> dict:
    stages = load_stages(CONTRACT)
    tables = live_tables(con)
    known = set(STAGE_OF)
    unassigned = sorted(t for t in tables if t not in known)
    # A mapped name that no longer exists is the other half of the same drift --
    # and it is swept across BOTH maps. Sweeping only STAGE_OF left a renamed or
    # dropped INFRASTRUCTURE table sitting in the set forever, which is rule 4's
    # drift applied to half the map.
    phantom = sorted(t for t in known if t not in tables)

    # A MISTYPED STAGE VALUE IS THE ONE WAY A TABLE COULD STILL HIDE, and it
    # would defeat this module's central claim. `unassigned` keys on the table
    # NAME, so STAGE_OF['foo'] = 'evidenc' keeps foo out of it -- while the
    # `s in by_stage` filter below drops foo from every stage list, so the table
    # and every row a session wrote into it vanish from the page with --check
    # green. Nothing validated the VALUES against the contract until now.
    # ONE VALIDATOR, EVERY VALUE -- including `infrastructure`, which the old
    # separate set escaped entirely. A stage id the contract does not define
    # keeps its table out of `unassigned` while dropping it from every stage
    # list, so the table would vanish from the page with --check green.
    allowed = set(stages) | {INFRA}
    bad_stage = sorted(f"{t} -> {v!r}" for t, v in STAGE_OF.items()
                       if v not in allowed)

    counts = {t: con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in tables}
    attrib = attribution(con, tables)
    no_session = sorted(t for t in tables if attrib[t][0] == "NONE")

    by_stage: dict[str, list[str]] = {s: [] for s in stages}
    for t in tables:
        st = STAGE_OF.get(t)
        if st in by_stage:
            by_stage[st].append(t)
    for st in by_stage:
        by_stage[st].sort()
    in_stage = {t for st in stages for t in by_stage[st]}

    sess = sessions(con, tables, attrib, counts)
    writes: dict[str, dict] = {}
    for e in sess:
        per = {}
        for t, n in sorted(e["per_table"].items()):
            if not n:
                continue
            if t not in in_stage:
                # OFF-STAGE TABLES CARRY ONLY THEIR COUNT. The page reads .total
                # for these and never .rows, so fetching and embedding them put
                # 141,988 bytes -- 26% of the payload -- into the browser to be
                # parsed and never read.
                per[t] = {"total": n, "stage": STAGE_OF.get(t, INFRA)}
                continue
            cols, rws = rows_for(con, t, e["id"], attrib[t][1], n)
            per[t] = {"cols": cols, "rows": rws, "total": n, "stage": STAGE_OF[t]}
        writes[e["id"]] = per

    return {
        "stages": stages, "by_stage": by_stage, "labels": {s: stage_label(s) for s in stages},
        "unassigned": unassigned, "phantom": phantom, "bad_stage": bad_stage,
        "no_session": no_session,
        "sessions": sess, "writes": writes,
        # POINT, DO NOT COPY (rule 5). This read v[0] -- DISPUTED's own copy of
        # the stage -- so editing STAGE_OF without editing DISPUTED rendered a
        # table under one stage while the panel named another, with --check
        # green. Demonstrated, not theorised.
        "disputed": {t: {"stage": STAGE_OF.get(t), "why": v}
                     for t, v in sorted(DISPUTED.items()) if t in tables},
        "unwritable": unwritable(con, tables), "as_of": as_of(con, tables),
        "n_tables": len(tables),
    }


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
def esc(s) -> str:
    return html.escape("" if s is None else str(s), quote=True)


CSS = """
:root{--bg:#fbfbfa;--fg:#1a1a18;--mut:#6b6b64;--line:#e0dfd9;--card:#fff;
--warn:#8a4b00;--warnbg:#fff4e5;--bad:#8a1c1c;--badbg:#fdecec;--ok:#1f5c2e;
--accent:#2d4a7c;--code:#f3f2ee}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){
--bg:#14140f;--fg:#ececdf;--mut:#9a9a8d;--line:#2e2e26;--card:#1c1c16;
--warn:#f0b56b;--warnbg:#30240f;--bad:#f09a9a;--badbg:#301616;--ok:#8fd4a0;
--accent:#9dbaea;--code:#22221b}}
:root[data-theme=dark]{--bg:#14140f;--fg:#ececdf;--mut:#9a9a8d;--line:#2e2e26;
--card:#1c1c16;--warn:#f0b56b;--warnbg:#30240f;--bad:#f09a9a;--badbg:#301616;
--ok:#8fd4a0;--accent:#9dbaea;--code:#22221b}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
font:15px/1.55 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:32px 16px 80px}
h1{font-size:25px;margin:0 0 4px;letter-spacing:-.01em}
h2{font-size:15px;text-transform:uppercase;letter-spacing:.08em;color:var(--mut);
margin:34px 0 10px;font-weight:600}
.sub{color:var(--mut);font-size:13.5px;margin:0 0 22px}
.card{background:var(--card);border:1px solid var(--line);border-radius:9px;
padding:14px 16px;margin:0 0 12px}
.alert{background:var(--badbg);border-color:var(--bad)}
.alert h2{color:var(--bad);margin-top:0}
.note{background:var(--warnbg);border-color:var(--warn)}
.note h2{color:var(--warn);margin-top:0}
code,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px}
code{background:var(--code);padding:1px 5px;border-radius:4px}
select{font:inherit;padding:7px 10px;border-radius:7px;border:1px solid var(--line);
background:var(--card);color:var(--fg);max-width:100%}
.stage{border:1px solid var(--line);border-radius:9px;margin:0 0 12px;
background:var(--card);overflow:hidden}
.stage>summary{cursor:pointer;padding:12px 16px;font-weight:600;
display:flex;gap:10px;align-items:baseline;list-style:none}
.stage>summary::-webkit-details-marker{display:none}
.stage>summary::before{content:"▸";color:var(--mut);font-size:12px}
.stage[open]>summary::before{content:"▾"}
.stage .body{padding:0 16px 14px}
.pos{margin-left:auto;font-weight:400;color:var(--mut);font-size:12.5px}
.pill{display:inline-block;padding:1px 8px;border-radius:99px;font-size:11.5px;
border:1px solid var(--line);color:var(--mut)}
.pill.on{color:var(--ok);border-color:var(--ok)}
table{border-collapse:collapse;width:100%;margin:8px 0 2px;font-size:12.5px}
th,td{border-bottom:1px solid var(--line);padding:5px 8px;text-align:left;
vertical-align:top;max-width:340px;overflow-wrap:anywhere}
th{color:var(--mut);font-weight:600;white-space:nowrap}
.scroll{overflow-x:auto}
.tname{font-weight:600;margin:14px 0 0;display:flex;gap:9px;align-items:baseline}
.tname .mono{font-size:13px}
.empty{color:var(--mut);font-style:italic;font-size:13px}
.legend{color:var(--mut);font-size:12.5px;margin:6px 0 0}
a{color:var(--accent)}
"""

JS = """
const D=window.__WALK__;
// EVERY interpolated value goes through this. The DB carries 134 cell values
// holding `<` or `&` today: `RT60 <= 0.6 s` survives raw only because the HTML
// parser passes `<` before a non-letter, and the first value with `<` before a
// letter opens a tag and swallows the rest of the cell -- a rendered row that
// differs from the database row, on the surface built to stop exactly that.
function E(v){return String(v).replace(/[&<>"']/g,function(c){
 return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function paint(){
 const s=document.getElementById('sess').value;
 const w=D.writes[s]||{};
 const host=document.getElementById('stages');
 host.innerHTML='';
 let any=false;
 D.stages.forEach(st=>{
  const tabs=(D.by_stage[st]||[]).filter(t=>w[t]);
  const all=(D.by_stage[st]||[]);
  const n=tabs.reduce((a,t)=>a+w[t].total,0);
  const d=document.createElement('details');
  d.className='stage'; if(tabs.length) {d.open=true; any=true;}
  const sm=document.createElement('summary');
  sm.innerHTML='<span>'+E(D.labels[st]||st)+'</span>'+
   '<span class="pill '+(tabs.length?'on':'off')+'">'+
   (tabs.length? n+' row'+(n===1?'':'s')+' in '+tabs.length+' table'+(tabs.length===1?'':'s')
              : 'no writes')+'</span>'+
   '<span class="pos">'+all.length+' tables in stage</span>';
  d.appendChild(sm);
  const b=document.createElement('div'); b.className='body';
  if(!tabs.length){
   b.innerHTML='<p class="empty">This session wrote nothing into this stage.</p>';
  } else {
   tabs.forEach(t=>{
    const e=w[t];
    const h=document.createElement('div');
    const shown=e.rows.length, more=e.total-shown;
    h.innerHTML='<div class="tname"><span class="mono">'+E(t)+'</span>'+
      '<span class="pill">'+e.total+' row'+(e.total===1?'':'s')+'</span>'+
      (more>0?'<span class="pill">showing first '+shown+', '+more+' more</span>':'')+
      '</div>';
    const sc=document.createElement('div'); sc.className='scroll';
    const tb=document.createElement('table');
    tb.innerHTML='<thead><tr>'+e.cols.map(c=>'<th>'+E(c)+'</th>').join('')+'</tr></thead>'+
     '<tbody>'+e.rows.map(r=>'<tr>'+r.map(v=>'<td>'+
       (v===null?'<span class="empty">null</span>':E(v))+'</td>').join('')+'</tr>').join('')+
     '</tbody>';
    sc.appendChild(tb); h.appendChild(sc); b.appendChild(h);
   });
  }
  d.appendChild(b); host.appendChild(d);
 });
 document.getElementById('none').style.display=any?'none':'block';
 // ROWS THE WALK CANNOT SHOW ARE COUNTED, NOT DROPPED. The session list sums
 // every table with a session column, but only stage-assigned tables render --
 // so a session whose writes are all infrastructure used to advertise rows and
 // display none, with nothing accounting for the gap.
 const inStage=new Set(); D.stages.forEach(st=>(D.by_stage[st]||[]).forEach(t=>inStage.add(t)));
 const off=Object.keys(w).filter(t=>!inStage.has(t));
 const offN=off.reduce((a,t)=>a+w[t].total,0);
 const el=document.getElementById('offstage');
 el.innerHTML = offN
  ? '<p>This session also wrote <strong>'+offN+'</strong> row'+(offN===1?'':'s')+
    ' into '+off.length+' table'+(off.length===1?'':'s')+' outside the stage map — '+
    off.map(t=>'<code>'+E(t)+'</code>').join(', ')+
    '. Those are run ledgers or unassigned tables, not pipeline stages, so they are '+
    'counted here rather than rendered above.</p>'
  : '';
 el.style.display = offN ? 'block' : 'none';
}
document.getElementById('sess').addEventListener('change',paint);
paint();
"""


def render_html(F: dict, focus: str | None) -> str:
    sess = F["sessions"]
    default = focus if focus and focus in F["writes"] else (sess[-1]["id"] if sess else "")
    # THE LABEL COUNTS WHAT THE PAGE RENDERS. `sessions()` sums every table with
    # a session column, including run ledgers and anything unassigned; the walk
    # renders stage-assigned tables only. Advertising the larger number sent a
    # reviewer to a session promising 157 rows and showed an empty walk.
    in_stage = {t for st in F["stages"] for t in F["by_stage"].get(st, [])}
    opts = []
    for e in reversed(sess):
        w = F["writes"].get(e["id"], {})
        shown = {t: d for t, d in w.items() if t in in_stage}
        n = sum(d["total"] for d in shown.values())
        off = e["rows"] - n
        label = f'{e["id"]} — {n} rows, {len(shown)} tables'
        if off:
            label += f' (+{off} off-stage)'
        opts.append(f'<option value="{esc(e["id"])}"'
                    f'{" selected" if e["id"] == default else ""}>{esc(label)}</option>')
    opts = "".join(opts)

    alerts = ""
    if F.get("bad_stage"):
        alerts += (
            '<div class="card alert"><h2>Stage values naming no contract stage</h2>'
            '<p>A table mapped to a stage id the contract does not define is dropped from '
            'every stage list while still counting as "assigned" — the one way a live table '
            'could still vanish from this page. Fix the value in <code>STAGE_OF</code>.</p>'
            '<p class="mono">' + ", ".join(esc(x) for x in F["bad_stage"]) + '</p></div>')
    if F["unassigned"]:
        alerts += (
            '<div class="card alert"><h2>Unassigned tables</h2>'
            '<p>These live tables are in no stage. The map is judged, not derived, so '
            'this is how it reports its own gaps rather than hiding them — assign them '
            'in <code>STAGE_OF</code> or say why they are infrastructure.</p><p class="mono">'
            + ", ".join(esc(t) for t in F["unassigned"]) + "</p></div>")
    if F["phantom"]:
        alerts += (
            '<div class="card alert"><h2>Mapped names that no longer exist</h2>'
            '<p>The other half of the same drift: <code>STAGE_OF</code> names a table the '
            'schema does not have. A rename is not done until the callers are swept '
            '(rule 4), and this map is a caller.</p><p class="mono">'
            + ", ".join(esc(t) for t in F["phantom"]) + "</p></div>")
    if F["unwritable"]:
        alerts += (
            '<div class="card note"><h2>NOT NULL foreign keys into empty tables</h2>'
            '<p>The refusal is <code>FOREIGN KEY constraint failed</code> at INSERT, never '
            'at migration time, so the schema looks healthy and every gate stays green over '
            'a table that cannot accept a row (CLAUDE.md §4).</p>'
            '<p><strong>This list over-reports and is a list to check, not a list of '
            'defects.</strong> The probe asks only whether the parent is empty right now. '
            'Where one <code>db.py</code> call inserts parent and child in the same '
            'transaction the write succeeds anyway, so a column here is dead only if '
            '<em>nothing</em> fills its parent.</p><p class="mono">'
            + ", ".join(esc(c) for c in F["unwritable"]) + "</p></div>")

    disputed_html = ""
    if F.get("disputed"):
        rows = "".join(
            f'<tr><td class="mono">{esc(t)}</td><td class="mono">{esc(d["stage"])}</td>'
            f'<td>{esc(d["why"])}</td></tr>' for t, d in F["disputed"].items())
        disputed_html = (
            '<div class="card note"><h2>Contested stage assignments</h2>'
            '<p>The repository contradicts itself about where these tables belong. The walk '
            'still has to put each one somewhere, so it does — and says which side it took '
            'and what argues the other way, rather than picking silently. A map that hides a '
            'live dispute is curating a fact nothing can check.</p>'
            '<div class="scroll"><table><thead><tr><th>table</th><th>rendered at</th>'
            f'<th>the dispute</th></tr></thead><tbody>{rows}</tbody></table></div></div>')

    not_attributable = (
        '<div class="card"><h2>Not attributable to a session</h2>'
        f'<p>{len(F["no_session"])} of {F["n_tables"]} tables carry no session column, so '
        'nothing below can show what a session wrote into them. Named rather than '
        'silently omitted: a walk that skipped them would report "no writes" over rows '
        'it never looked at.</p><p class="mono">'
        + ", ".join(esc(t) for t in F["no_session"]) + "</p></div>")

    payload = json.dumps({
        "stages": F["stages"], "by_stage": F["by_stage"], "writes": F["writes"],
        "labels": F["labels"],
    }, sort_keys=True, ensure_ascii=False, default=str)
    # `json.dumps` escapes neither `<` nor `/`, so a DB value holding the literal
    # `</script>` closes this element early: `window.__WALK__` is then undefined,
    # paint() throws before its first line, and the page renders its chrome over
    # an EMPTY walk with no error -- a reviewer reads "wrote nothing" over a
    # session that wrote rows. No live value contains it today, which is the
    # same "one populated column away" state this session criticised elsewhere,
    # so it is closed rather than noted.
    payload = (payload.replace("</", "<\\/")
                      .replace("<!--", "<\\u0021--")
                      .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pipeline Walk</title><style>{CSS}</style></head><body><div class="wrap">
<h1>Pipeline walk</h1>
<p class="sub">What a session committed, in spine order. Stage ids are read from
<code>governance/pipeline-contract.yaml</code>, the single home; the table list is read from
<code>sqlite_master</code>, so a new table cannot hide. Data as of <strong>{esc(F["as_of"])}</strong>
— derived from the database's own timestamps, never the clock. Regenerate with
<code>python3 tools/pipeline_walk.py</code>.</p>
{alerts}{disputed_html}
<h2 id="sesshead">Session</h2>
<div class="card">
<label for="sess">Show the rows written by session</label><br>
<select id="sess" aria-describedby="sesshelp">{opts}</select>
<p class="legend" id="sesshelp">{len(sess)} sessions have written rows. Stages with writes open automatically;
row counts are the true totals, and any table showing fewer is labelled as truncated.</p>
</div>
<div id="none" class="card" style="display:none"><p class="empty">This session wrote no rows
into any stage-assigned table.</p></div>
<noscript><div class="card alert"><h2>JavaScript is off</h2><p>Every stage, row and
count on this page is built at runtime, so with scripting disabled there is nothing
below but chrome. Run <code>python3 tools/pipeline_walk.py --session &lt;id&gt;</code>
and read its output instead of trusting an empty page.</p></div></noscript>
<div id="stages" aria-live="polite" aria-labelledby="sesshead"></div>
<div id="offstage" class="card" style="display:none"></div>
{not_attributable}
<div class="card"><h2>How to read this</h2>
<p>A stage reading <em>no writes</em> means this session wrote nothing there — not that the
stage is empty. Row counts across the whole corpus live in the completeness dashboard; this
page is scoped to one session on purpose, because the question it answers is
<em>what did this batch put in the database</em>.</p></div>
</div>
<script>window.__WALK__={payload};</script>
<script>{JS}</script>
</body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=os.environ.get("GUIDEBOOK_DB_PATH", str(DEFAULT_DB)))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--session", default=None,
                    help="session id to select by default (bare stem, as the DB stores it)")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the committed page is stale or the map has drifted")
    a = ap.parse_args()

    db = Path(a.db)
    if not db.exists():
        print(f"pipeline_walk: no database at {db}", file=sys.stderr)
        return 1

    con = connect_ro(db)
    try:
        F = gather(con)
    finally:
        con.close()
    page = render_html(F, a.session)
    out = Path(a.out)

    if a.session and a.session not in F["writes"]:
        # CLAUDE.md §7: "Wrong form scopes a gate to nothing and it passes green."
        # Silently falling back to the newest session renders a confident page
        # about a DIFFERENT batch. The bare stem is what the DB stores; a pointer
        # file's trailing `.md` is the usual way to get here.
        print(f"pipeline_walk: --session {a.session!r} wrote no rows under that id. "
              f"The DB stores the BARE STEM (no trailing '.md').", file=sys.stderr)
        return 1

    drift = []
    if F["bad_stage"]:
        drift.append(f"{len(F['bad_stage'])} STAGE_OF value(s) name no contract stage: "
                     + ", ".join(F["bad_stage"]))
    if F["unassigned"]:
        drift.append(f"{len(F['unassigned'])} live table(s) unassigned to a stage: "
                     + ", ".join(F["unassigned"]))
    if F["phantom"]:
        drift.append(f"{len(F['phantom'])} mapped name(s) absent from the schema: "
                     + ", ".join(F["phantom"]))

    if a.check:
        current = out.read_text(encoding="utf-8") if out.exists() else None
        stale = current != page
        print(f"EXAMINED: {F['n_tables']} tables, {len(F['sessions'])} sessions")
        for d in drift:
            print(f"  DRIFT: {d}")
        if stale:
            print("pipeline-walk.html is stale — run: python3 tools/pipeline_walk.py",
                  file=sys.stderr)
        if stale or drift:
            return 1
        print("OK: pipeline-walk.html is current and every live table is assigned.")
        return 0

    out.write_text(page, encoding="utf-8")
    print(f"Wrote {out} — {F['n_tables']} tables, {len(F['sessions'])} sessions, "
          f"as-of {F['as_of']}")
    for d in drift:
        print(f"  DRIFT: {d}", file=sys.stderr)
    # THE WRITER RETURNS 0 EVEN ON DRIFT, and the siblings do the same.
    # `scripts/regenerate_derived.sh` runs under `set -euo pipefail`, so a
    # non-zero here killed the script at the generator and its whole
    # verification block -- including the three sibling `--check` gates -- never
    # ran. Drift is the --check exit code's job; reporting it is the writer's.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
