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
# Table -> stage: JUDGED, with a falsifier
# ---------------------------------------------------------------------------
# Rule 8 says derive it or name who judged it. There is no derivable table->stage
# edge in this repository: `pipeline-contract.yaml` stages carry `anchor`,
# `entry` and `criteria` and no `tables:` key, and the retired `pipeline-map.yaml`
# bucketing that once did is what CLAUDE.md §3 warns is NOT this. So this map is
# JUDGED, against CLAUDE.md §3's stage table, and it is named as such.
#
# THE FALSIFIER IS THE POINT, and it is what rule 8's own proof story lacked.
# `dbcore.WRITABLE_TABLES` went blind eight times because a curated list can
# silently omit a live table. This map cannot: the table list is read from
# `sqlite_master`, every live table not named here lands in an UNASSIGNED bucket
# that the page renders first and loudly, and `--check` fails while one exists.
# A new table is therefore visible on the next regeneration rather than absent.
#
# Judged by: batch-10 preparation session, 2026-09-17, against CLAUDE.md §3.
STAGE_OF = {
    # base -- the vocabularies and registries every other stage points into
    "access_duration": "base", "access_need_axis_map": "base",
    "access_need_icf": "base", "access_needs": "base", "access_stakes": "base",
    "axes": "base", "base_icf": "base", "base_parameters": "base",
    "base_taxonomy_medical": "base", "icf_medical_map": "base",
    "identity_medical_map": "base", "lang_jur_map": "base",
    "life_stage_modifiers": "base", "population_axis_map": "base",
    "population_icf_links": "base", "populations": "base", "rooms": "base",
    "room_items": "base", "situations": "base", "slugs": "base",
    "term_aliases": "base", "terms": "base",
    # research -- what was searched, screened and mined, plus the clue store
    "citation_mining": "research", "gap_mining": "research",
    "research_code_leads": "research", "search_admissions": "research",
    "search_candidates": "research", "search_coverage": "research",
    "search_executions": "research", "search_languages": "research",
    # THE CLUE STORE IS RESEARCH, not evidence. `db.py add-locator` is helped
    # "Write a lead into the clue store", and §3's research row is "what was
    # searched, screened and mined, PLUS THE CLUE STORE". Both tables carry
    # status/tier_claimed/recovered_from and no foreign keys -- pre-admission
    # leads, not admitted sources. (Both read "evidence" until 2026-09-17, and
    # source_locators is the largest object this map places -- derive the count,
    # never quote it: SELECT COUNT(*) FROM source_locators.)
    "source_locators": "research", "reference_stubs": "research",
    # evidence -- what was admitted, its identity, verification and extraction
    "case_studies": "evidence", "case_study_outcomes": "evidence",
    "case_study_populations": "evidence", "case_study_specs": "evidence",
    "case_study_strategies": "evidence", "economics_entries": "evidence",
    "economics_entry_populations": "evidence", "economics_entry_specs": "evidence",
    "evidence_source_authors": "evidence", "evidence_sources": "evidence",
    "external_root_registry": "evidence", "extraction_relations": "evidence",
    "jurisdictional_values": "evidence", "source_slug_links": "evidence",
    "source_value_extractions": "evidence", "url_verification_runs": "evidence",
    # Harvest is an EVIDENCE act on an admitted source, not a research one:
    # observed_terms.ref_id is a FK into evidence_sources, and the owner ruling
    # of 2026-08-27 quoted in CLAUDE.md §6 says "harvest concepts AT EVIDENCE
    # (db.py observe-term, verbatim and unjudged), adjudicate at judgment".
    # (Read "research" until 2026-09-17, contradicting the ruling by name.)
    "observed_terms": "evidence",
    # judgment -- whether an extraction is sound and how it weighs
    "citation_population_links": "judgment",
    "evidence_population_match": "judgment",
    "extraction_population_links": "judgment",
    "probe_population_links": "judgment", "term_adjudications": "judgment",
    # synthesis -- what the judgments say together
    "conflicts": "synthesis", "connections": "synthesis",
    "connection_targets": "synthesis", "convergence_assessment": "synthesis",
    "reasoning_doc_citations": "synthesis", "supersession_check": "synthesis",
    "gaps": "synthesis",   # DISPUTED -- see DISPUTED below
    # specification -- the determination
    "determination_gates": "specification",
    "spec_value_probes": "specification",
    "specification_extraction_links": "specification",
    "specification_source_links": "specification",
    "specifications": "specification",
    # render -- book surfaces and the rollups that feed them
    "item_bpc_links": "render", "item_population_elaborations": "render",
    "item_taxonomy_links": "render", "items": "render",
    "term_item_links": "render",
    # Not a vocabulary and nothing points into it, so it fails the base bucket's
    # own entry test; doctrine puts it at render (governance/grounds.md §R role
    # views, held-tensions.md's door-epistemology disclosure). Read "base" until
    # 2026-09-17.
    "weighting_profile": "render",
}

#: Where the REPOSITORY CONTRADICTS ITSELF about a table's stage. The map still
#: has to put the table somewhere for the walk to render, and the value used is
#: recorded in STAGE_OF -- but silently taking a side in a live dispute is the
#: thing rule 8 calls curating a fact the machine cannot check. So the side is
#: taken openly, with both readings and their citations, and the page prints it.
DISPUTED = {
    "source_value_extractions": (
        "evidence",
        "CLAUDE.md §3 puts extraction at EVIDENCE (\"what was admitted, its "
        "identity, verification and extraction\"). governance/pipeline-contract.yaml "
        "calls the same rows JUDGMENT under its `- id: judgment` stage -- \"One "
        "evidence source may provide many judgment rows\" -- and assess_cell.py:78 "
        "calls it \"the JUDGMENT item (D-0168)\". Four contract criteria naming it "
        "sit under judgment. Rendered at evidence; the dispute is real and open."),
    "extraction_relations": (
        "evidence",
        "Inherits its parent exactly: both ends are FKs into "
        "source_value_extractions, so it cannot sit in a different stage from it. "
        "Disputed for the same reason and by the same documents."),
    "gaps": (
        "synthesis",
        "SYNTHESIS IS THE ONE STAGE WITH NO SUPPORT, and it is where this map put "
        "it. The contract makes \"an OPEN gap\" the RESEARCH stage's entry; most "
        "live rows were written by research-batch sessions (derive, never quote: "
        "SELECT created_by_session, COUNT(*) FROM gaps GROUP BY 1); "
        "evidence_population_match.gap_id is a FK from judgment INTO gaps; and §3 "
        "defines synthesis as weighing, convergence and cross-slug findings, which "
        "a gap is none of. assess_cell also writes it at specification. The honest "
        "answer is a cross-stage register with no single home."),
}

#: Tables that record the repository's own operation rather than a pipeline
#: stage. Named here so they do not sit in UNASSIGNED forever pretending to be
#: an unclassified stage table -- a permanent false alarm teaches its reader to
#: ignore the alarm (CLAUDE.md rule 6's own argument).
INFRASTRUCTURE = {
    "data_migrations", "decisions", "pipeline_runs",
    # RUN LEDGERS, NOT RENDER SURFACES. §3 defines render as "Book surfaces --
    # site/, parts/, tools/*.html". bpc_metadata holds per-slug completion flags
    # (pico_complete, search_complete, citation_mining_complete) and
    # item_audit_runs holds run_id/status/steps_complete: both record the
    # repository's own operation, which is this set's entry test. Both read
    # "render" until 2026-09-17.
    "bpc_metadata", "item_audit_runs",
}


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


def columns(con, table) -> list[str]:
    return [r[1] for r in con.execute(f'PRAGMA table_info("{table}")')]


def session_col(con, table) -> str | None:
    """Which column attributes a row to a session -- DERIVED per table, not curated.

    Three spellings are live: `created_by_session` (most), `session`
    (search_executions, search_candidates), and both (item_audit_runs). A curated
    list of which table uses which is the exact shape rule 8 forbids, so this asks
    the table.
    """
    cols = set(columns(con, table))
    for c in ("created_by_session", "session"):
        if c in cols:
            return c
    return None


def sessions(con, tables) -> list[dict]:
    """Every session id that wrote anything, with what it touched.

    Ordered by first write then id, so the page is stable across runs.
    """
    seen: dict[str, dict] = {}
    for t in tables:
        sc = session_col(con, t)
        if sc is None:
            continue
        stamp = "created_at" if "created_at" in columns(con, t) else None
        q = (f'SELECT "{sc}" AS s, COUNT(*) AS n'
             + (f', MIN("{stamp}") AS first' if stamp else ', NULL AS first')
             + f' FROM "{t}" WHERE "{sc}" IS NOT NULL GROUP BY "{sc}"')
        for row in con.execute(q):
            e = seen.setdefault(row["s"], {"id": row["s"], "rows": 0,
                                           "tables": [], "first": None})
            e["rows"] += row["n"]
            e["tables"].append(t)
            if row["first"] and (e["first"] is None or row["first"] < e["first"]):
                e["first"] = row["first"]
    out = list(seen.values())
    for e in out:
        e["tables"] = sorted(set(e["tables"]))
    out.sort(key=lambda e: (e["first"] or "", e["id"]))
    return out


def rows_for(con, table, sess) -> tuple[list[str], list[list], int]:
    """The rows `sess` wrote into `table`: (columns, capped rows, true total)."""
    sc = session_col(con, table)
    if sc is None:
        return [], [], 0
    cols = columns(con, table)
    total = con.execute(
        f'SELECT COUNT(*) FROM "{table}" WHERE "{sc}" = ?', (sess,)).fetchone()[0]
    if not total:
        return cols, [], 0
    # A TOTAL ORDER, or the cap is nondeterministic and --check lies.
    # cols[0] is not unique in nine live tables -- term_aliases holds 2382 rows
    # over 88 distinct term_id, so `ORDER BY term_id LIMIT 50` picks 50 rows out
    # of a huge tie set and SQLite may break the tie differently on a different
    # build, after an added index, or after VACUUM. The page would then differ
    # byte-for-byte from the committed copy and `--check` would report a
    # correctly-generated page stale, with nothing telling the reader why.
    # `_rowid_` is the tiebreaker; a WITHOUT ROWID table has none, so fall back
    # to ordering on every column, which is total by construction.
    allcols = ", ".join(f'"{c}"' for c in cols)
    for order in (f'"{cols[0]}", _rowid_', allcols):
        try:
            got = con.execute(
                f'SELECT * FROM "{table}" WHERE "{sc}" = ? ORDER BY {order} '
                f'LIMIT {ROW_CAP}', (sess,)).fetchall()
            return cols, [list(r) for r in got], total
        except sqlite3.OperationalError:
            continue
    raise RuntimeError(f"no total order available for {table}")


def unwritable(con) -> list[str]:
    """CLAUDE.md §4's probe: a NOT NULL FK into an EMPTIED table.

    The refusal is `FOREIGN KEY constraint failed` at INSERT, never at migration
    time, so the schema looks healthy and every gate stays green over a table that
    cannot accept a row. Derived here, never quoted.

    IT OVER-REPORTS, AND THE PAGE SAYS SO RATHER THAN THE COMMENT ALONE. The probe
    asks only whether the parent table is empty RIGHT NOW. Where a single `db.py`
    call inserts the parent and the child in one transaction, the parent is empty
    beforehand and the write still succeeds -- `connection_targets.con_id`,
    `identity_medical_map.medical_code` and `icf_medical_map.medical_code` were all
    flagged by this probe and are all fine, measured 2026-09-17. Only a child whose
    parent NOTHING fills is genuinely dead. Reporting the raw probe as a verdict
    would manufacture findings, so the page prints it as a list to check, not a
    list of defects.
    """
    empty = {t for t in live_tables(con)
             if con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] == 0}
    out = []
    for t in live_tables(con):
        dead = {f[3] for f in con.execute(f'PRAGMA foreign_key_list("{t}")')
                if f[2] in empty}
        for c in con.execute(f'PRAGMA table_info("{t}")'):
            if c[1] in dead and c[3]:
                out.append(f"{t}.{c[1]}")
    return sorted(out)


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
    known = set(STAGE_OF) | INFRASTRUCTURE
    unassigned = sorted(t for t in tables if t not in known)
    # A mapped name that no longer exists is the other half of the same drift --
    # and it is swept across BOTH maps. Sweeping only STAGE_OF left a renamed or
    # dropped INFRASTRUCTURE table sitting in the set forever, which is rule 4's
    # drift applied to half the map.
    phantom = sorted(t for t in (set(STAGE_OF) | INFRASTRUCTURE) if t not in tables)

    # A MISTYPED STAGE VALUE IS THE ONE WAY A TABLE COULD STILL HIDE, and it
    # would defeat this module's central claim. `unassigned` keys on the table
    # NAME, so STAGE_OF['foo'] = 'evidenc' keeps foo out of it -- while the
    # `s in by_stage` filter below drops foo from every stage list, so the table
    # and every row a session wrote into it vanish from the page with --check
    # green. Nothing validated the VALUES against the contract until now.
    bad_stage = sorted(f"{t} -> {v!r}" for t, v in STAGE_OF.items()
                       if v not in set(stages))
    no_session = sorted(t for t in tables if session_col(con, t) is None)

    by_stage: dict[str, list[str]] = {s: [] for s in stages}
    for t in tables:
        s = STAGE_OF.get(t)
        if s in by_stage:
            by_stage[s].append(t)
    for s in by_stage:
        by_stage[s].sort()

    sess = sessions(con, tables)
    writes: dict[str, dict] = {}
    for e in sess:
        per = {}
        for t in e["tables"]:
            cols, rws, total = rows_for(con, t, e["id"])
            if total:
                per[t] = {"cols": cols, "rows": rws, "total": total,
                          "stage": STAGE_OF.get(t, "unassigned")}
        writes[e["id"]] = per

    return {
        "stages": stages, "by_stage": by_stage, "labels": {s: stage_label(s) for s in stages},
        "unassigned": unassigned, "phantom": phantom, "bad_stage": bad_stage,
        "no_session": no_session,
        "sessions": sess, "writes": writes,
        "disputed": {t: {"stage": v[0], "why": v[1]}
                     for t, v in sorted(DISPUTED.items()) if t in tables},
        "unwritable": unwritable(con), "as_of": as_of(con, tables),
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
.pill.off{color:var(--mut)}
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
