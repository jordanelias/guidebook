#!/usr/bin/env python3
"""
tools/regenerate_vetting_surface.py

Regenerates tools/spec-curation-vetting-surface.html from data/guidebook.db.
Idempotent — same DB content produces byte-identical HTML output.

Reads only; writes only the HTML file. Safe to run locally or in CI.

Per DR-2026-05-28-b (the source_value_extractions layer) and the vetting
surface introduced 2026-05-28. The surface displays, per topic:

  - Per-source extractions (source_value_extractions)
  - Synthesis-verified values (reasoning_doc_citations, rule #10)
  - Selection walks (spec_value_probes, rule #8)
  - Evidence spread (source_slug_links + per-source values aggregated
    from all three value-layers above)

Usage:
  python3 tools/regenerate_vetting_surface.py                    # uses default DB
  python3 tools/regenerate_vetting_surface.py --db path/to.db    # custom DB
  GUIDEBOOK_DB_PATH=... python3 tools/regenerate_vetting_surface.py
"""

import argparse
import json
import os
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = REPO_ROOT / "data" / "guidebook.db"
DEFAULT_OUT = REPO_ROOT / "tools" / "spec-curation-vetting-surface.html"


def fetch_backbone(db_path: Path) -> dict:
    """Build the per-topic data backbone from the DB. Read-only."""
    c = sqlite3.connect(str(db_path))
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys = ON")
    q = lambda s, *a: [dict(r) for r in c.execute(s, a).fetchall()]

    # Link-integrity audit (orphan source references across all value-layers)
    valid_refs = {r["ref_id"] for r in q("SELECT ref_id FROM evidence_sources")}

    def orphans(table, col):
        rows = q(
            f"SELECT DISTINCT {col} AS r FROM {table} "
            f"WHERE {col} IS NOT NULL AND {col}!=''"
        )
        return [x["r"] for x in rows if x["r"] not in valid_refs]

    orphan_count = sum(
        len(orphans(t, col))
        for t, col in [
            ("source_slug_links", "ref_id"),
            ("reasoning_doc_citations", "source_ref_id"),
            ("spec_value_probes", "ref_id"),
            ("source_value_extractions", "ref_id"),
        ]
    )

    # Population membership from the authoritative junction tables (migration 021).
    # Keyed by parent id -> sorted list of canonical codes.
    cpl_by = defaultdict(list)
    for r in q("SELECT citation_id, population_code FROM citation_population_links ORDER BY population_code"):
        cpl_by[r["citation_id"]].append(r["population_code"])
    ppl_by = defaultdict(list)
    for r in q("SELECT probe_id, population_code FROM probe_population_links ORDER BY population_code"):
        ppl_by[r["probe_id"]].append(r["population_code"])
    epl_by = defaultdict(list)
    for r in q("SELECT extraction_id, population_code FROM extraction_population_links ORDER BY population_code"):
        epl_by[r["extraction_id"]].append(r["population_code"])

    # Canonical populations taxonomy (for UI to label codes + flag drift)
    populations_taxonomy = {
        r["population_code"]: {
            "display_name": r["display_name"],
            "category": r["category"],
        }
        for r in q(
            "SELECT population_code, display_name, category FROM populations"
        )
    }

    # Item → slug + populations
    item_slug = {
        r["item_code"]: r["bpc_source_slug"]
        for r in q("SELECT item_code, bpc_source_slug FROM items")
    }
    item_pops = defaultdict(list)
    for r in q(
        "SELECT item_code, population_code, applicability "
        "FROM item_population_links"
    ):
        item_pops[r["item_code"]].append((r["population_code"], r["applicability"]))

    # Pre-index per-source values from all three layers, keyed by (slug, ref_id)
    rdc_by = defaultdict(list)
    for r in q(
        """SELECT citation_id, reasoning_doc_slug AS slug, source_ref_id AS ref_id,
                  parameter, claimed_value, claimed_unit,
                  jurisdiction, population, setting, value_match, source_section
           FROM reasoning_doc_citations"""
    ):
        if r["ref_id"]:
            junc = cpl_by.get(r["citation_id"], [])
            rdc_by[(r["slug"], r["ref_id"])].append(
                {
                    "layer": "synthesis",
                    "parameter": r["parameter"],
                    "value": r["claimed_value"],
                    "unit": r["claimed_unit"],
                    "jurisdiction": r["jurisdiction"],
                    "population": ",".join(junc) if junc else r["population"],
                    "setting": r["setting"],
                    "verdict": r["value_match"],
                    "section": r["source_section"],
                }
            )

    probe_by = defaultdict(list)
    for r in q(
        """SELECT probe_id, slug, ref_id, step_value, step_value_unit, population, setting,
                  item_code, walk_id, phase
           FROM spec_value_probes
           WHERE ref_id IS NOT NULL AND passes_strict=1"""
    ):
        junc = ppl_by.get(r["probe_id"], [])
        probe_by[(r["slug"], r["ref_id"])].append(
            {
                "layer": "walk",
                "parameter": r["item_code"] + " walk",
                "value": r["step_value"],
                "unit": r["step_value_unit"],
                "jurisdiction": None,
                "population": ",".join(junc) if junc else r["population"],
                "setting": r["setting"],
                "verdict": "pass",
                "section": r["walk_id"],
            }
        )

    sve_by = defaultdict(list)
    for r in q(
        """SELECT extraction_id, slug, ref_id, parameter, claimed_value, claimed_unit,
                  jurisdiction, population_code, population_label, setting,
                  extraction_status, source_section
           FROM source_value_extractions"""
    ):
        junc = epl_by.get(r["extraction_id"], [])
        sve_by[(r["slug"], r["ref_id"])].append(
            {
                "layer": "extraction",
                "parameter": r["parameter"],
                "value": r["claimed_value"],
                "unit": r["claimed_unit"],
                "jurisdiction": r["jurisdiction"],
                "population": ",".join(junc) if junc else r["population_code"],
                "population_label": r["population_label"],
                "setting": r["setting"],
                "verdict": r["extraction_status"],
                "section": r["source_section"],
            }
        )

    # All known slugs (union of source-link topics and item BPC slugs)
    slugs = sorted(
        {r["slug"] for r in q("SELECT DISTINCT slug FROM source_slug_links")}
        | {
            r["bpc_source_slug"]
            for r in q("SELECT DISTINCT bpc_source_slug FROM items")
            if r["bpc_source_slug"]
        }
    )

    bb = {}
    for slug in slugs:
        linked = q(
            """SELECT e.ref_id, e.author_display, e.pub_year, e.tier, e.evidence_type,
                      e.jurisdiction, e.doi, e.pmid, e.metadata_quality,
                      e.verification_status, e.doi_resolution_outcome,
                      sl.relevance_note
               FROM source_slug_links sl
               JOIN evidence_sources e ON e.ref_id = sl.ref_id
               WHERE sl.slug = ?
               ORDER BY e.tier, e.pub_year""",
            slug,
        )
        for s in linked:
            key = (slug, s["ref_id"])
            # Per-source values: extractions first, then synthesis, then walks
            s["values_cited"] = (
                sve_by.get(key, []) + rdc_by.get(key, []) + probe_by.get(key, [])
            )
            # Bibliography-validity verdict
            has_id = bool(s.get("doi") or s.get("pmid"))
            mq = s.get("metadata_quality") or ""
            vs = s.get("verification_status") or ""
            mq_ok = mq in ("COMPLETE", "COMPLETE-STATUTORY")
            vs_ok = vs in ("VERIFIED", "UNVERIFIED-1")
            if mq == "AUTHOR-TITLE-ONLY" or not vs_ok:
                v = "weak"
            elif has_id and mq_ok:
                v = "strong"
            else:
                v = "ok"
            s["_v"] = {"verdict": v}

        rdc = q(
            """SELECT citation_id, parameter, jurisdiction, population, setting,
                      claimed_value, claimed_unit,
                      source_ref_id, source_section, value_match, claim_match, notes
               FROM reasoning_doc_citations
               WHERE reasoning_doc_slug = ?""",
            slug,
        )
        for row in rdc:
            j = cpl_by.get(row["citation_id"], [])
            row["population"] = ",".join(j) if j else row["population"]
        probes = q(
            """SELECT probe_id, walk_id, item_code, step_index, phase, step_value,
                      step_value_unit, population, setting, passes_strict, ref_id
               FROM spec_value_probes
               WHERE slug = ?
               ORDER BY walk_id, step_index""",
            slug,
        )
        for row in probes:
            j = ppl_by.get(row["probe_id"], [])
            row["population"] = ",".join(j) if j else row["population"]
        sve = q(
            """SELECT extraction_id, ref_id, parameter, population_code,
                      population_label, setting, jurisdiction, claim_type,
                      claimed_value, claimed_unit, source_section, extraction_method,
                      extraction_status, promoted_to_rdc_id, notes
               FROM source_value_extractions
               WHERE slug = ?""",
            slug,
        )
        for row in sve:
            j = epl_by.get(row["extraction_id"], [])
            row["population_code"] = ",".join(j) if j else row["population_code"]
        items_here = [ic for ic, sg in item_slug.items() if sg == slug]
        bb[slug] = {
            "linked_sources": linked,
            "value_extractions": rdc,
            "selection_walks": probes,
            "source_extractions": sve,
            "items": [
                {"item_code": ic, "populations": item_pops.get(ic, [])}
                for ic in items_here
            ],
        }

    schema_version = c.execute("PRAGMA user_version").fetchone()[0]
    c.close()

    totals = {
        "topics": len(bb),
        "sources": sum(len(d["linked_sources"]) for d in bb.values()),
        "extractions_synthesis": sum(len(d["value_extractions"]) for d in bb.values()),
        "extractions_source": sum(len(d["source_extractions"]) for d in bb.values()),
        "walks": sum(
            len({p["walk_id"] for p in d["selection_walks"]}) for d in bb.values()
        ),
        "schema_version": schema_version,
        "orphan_links": orphan_count,
        "sources_with_values": sum(
            1 for d in bb.values() for s in d["linked_sources"] if s.get("values_cited")
        ),
    }
    return {"backbone": bb, "totals": totals, "populations": populations_taxonomy}


# HTML template — separate from the data so changes to UI don't reflow data code.
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Guidebook — Spec Curation Vetting Surface</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{--ink:#1a1714;--paper:#f4efe6;--panel:#fbf8f1;--line:#d8cfbe;--muted:#6f6557;
 --strong:#2f6b3d;--ok:#9a7b1f;--weak:#a3392b;--accent:#7a3b12;--hl:#e9dcc3;--syn:#2e4f6e;
 --serif:'Fraunces',Georgia,'Times New Roman',serif;--mono:'JetBrains Mono',ui-monospace,'SF Mono',Menlo,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--mono);font-size:13px;line-height:1.5;
 background-image:radial-gradient(circle at 1px 1px,rgba(0,0,0,.025) 1px,transparent 0);background-size:22px 22px}
header{padding:26px 32px 18px;border-bottom:2px solid var(--ink)}
h1{font-family:var(--serif);font-weight:900;font-size:30px;letter-spacing:-.5px;margin:0 0 4px}
.sub{color:var(--muted);font-size:12px;max-width:78ch}
.regen{font-size:10px;color:var(--muted);margin-top:6px}
.totals{display:flex;gap:26px;margin-top:16px;flex-wrap:wrap}
.tot{border-left:3px solid var(--accent);padding:2px 0 2px 12px}
.tot b{font-family:var(--serif);font-size:24px;font-weight:600;display:block}
.tot span{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:var(--muted)}
.tot.warn b{color:var(--weak)} .tot.new b{color:var(--syn)}
.layout{display:grid;grid-template-columns:340px 1fr;height:calc(100vh - 170px);min-height:500px}
.list{overflow-y:auto;border-right:1px solid var(--line);padding:10px 0}
.ctrl{padding:8px 16px;display:flex;gap:6px;align-items:center;border-bottom:1px dashed var(--line);font-size:11px}
.ctrl select{font-family:var(--mono);font-size:11px;padding:3px;border:1px solid var(--line);background:var(--panel)}
.topic{padding:10px 16px;cursor:pointer;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.topic:hover{background:var(--hl)} .topic.active{background:var(--ink);color:var(--paper)} .topic.active .tname{color:var(--paper)}
.tname{font-size:12px;font-weight:600;font-family:var(--serif)}
.depth{font-size:9px;text-transform:uppercase;letter-spacing:.5px;padding:2px 6px;border-radius:2px;white-space:nowrap}
.d-none{background:#e7ddcb;color:var(--muted)} .d-walk{background:#dde9d4;color:var(--strong)} .d-full{background:var(--strong);color:#fff} .d-src{background:#dbe2ec;color:var(--syn)}
.counts{font-size:10px;color:var(--muted);white-space:nowrap}
.detail{overflow-y:auto;padding:24px 32px}
.detail h2{font-family:var(--serif);font-weight:900;font-size:24px;margin:0 0 2px}
.detail .slug{color:var(--muted);font-size:11px;margin-bottom:18px}
.sec{margin:26px 0}
.sec-h{font-family:var(--serif);font-weight:600;font-size:15px;border-bottom:2px solid var(--ink);padding-bottom:4px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:baseline}
.sec-h em{font-style:normal;font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:1px;font-family:var(--mono)}
table{width:100%;border-collapse:collapse;font-size:11.5px}
th{text-align:left;font-size:9px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);border-bottom:1px solid var(--line);padding:5px 8px 5px 0;font-weight:600}
td{padding:6px 8px 6px 0;border-bottom:1px solid var(--line);vertical-align:top}
.ref{font-weight:600}
.badge{font-size:9px;padding:1px 6px;border-radius:2px;font-weight:600;white-space:nowrap;letter-spacing:.3px}
.b-strong{background:#dcebe0;color:var(--strong)} .b-ok{background:#f0e6c8;color:var(--ok)} .b-weak{background:#f0d9d4;color:var(--weak)}
.b-id{background:#e3e9ef;color:#3a566e} .b-noid{background:#eee5d4;color:var(--muted)}
.m-exact{background:var(--strong);color:#fff} .m-tol{background:#dde9d4;color:var(--strong)} .m-other{background:#f0d9d4;color:var(--weak)}
.s-prel{background:#eee5d4;color:var(--ok)} .s-rev{background:#f0e6c8;color:var(--ok)} .s-ver{background:var(--strong);color:#fff} .s-con{background:#f0d9d4;color:var(--weak)} .s-abs{background:#e7ddcb;color:var(--muted)}
.tier{font-weight:600;font-family:var(--serif)}
.val{font-family:var(--serif);font-size:15px;font-weight:600;color:var(--accent)}
.empty{padding:18px;background:var(--panel);border:1px dashed var(--weak);color:var(--weak);font-size:12px;border-radius:3px}
.empty.info{border-color:var(--syn);color:var(--syn)}
.empty b{font-family:var(--serif)}
.note{font-size:10.5px;color:var(--muted);line-height:1.45;max-width:80ch}
.note.clip{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;cursor:pointer}
.walk{background:var(--panel);border:1px solid var(--line);padding:12px;margin-bottom:12px;border-radius:3px}
.walk-h{display:flex;justify-content:space-between;font-size:11px;margin-bottom:8px}
.step{display:grid;grid-template-columns:30px 130px 1fr 70px 90px;gap:8px;font-size:11px;padding:3px 0;border-top:1px dotted var(--line)}
.step.final{background:var(--hl);font-weight:600}
.legend{padding:14px 32px;border-top:1px solid var(--line);font-size:10px;color:var(--muted);display:flex;gap:18px;flex-wrap:wrap;background:var(--panel)}
.placeholder{display:flex;align-items:center;justify-content:center;height:100%;color:var(--muted);font-family:var(--serif);font-size:18px}
.chain{display:flex;gap:4px;font-size:9px;color:var(--muted);margin-bottom:14px;text-transform:uppercase;letter-spacing:.5px}
.chain span{padding:2px 8px;background:var(--panel);border:1px solid var(--line);border-radius:2px}
.chain span.here{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.chain span.empty-step{opacity:.4;font-style:italic}
.values{display:flex;flex-direction:column;gap:3px;max-width:340px}
.vrow{font-size:10px;line-height:1.3;display:flex;gap:6px;align-items:baseline;flex-wrap:wrap}
.vrow .vval{font-family:var(--serif);font-weight:600;color:var(--accent);font-size:11.5px}
.vrow .vmeta{color:var(--muted);font-size:9.5px}
.vrow .layer-pill{font-size:8px;text-transform:uppercase;letter-spacing:.4px;padding:0 4px;border-radius:2px;font-weight:600}
.layer-synthesis{background:var(--strong);color:#fff}
.layer-walk{background:#dde9d4;color:var(--strong)}
.layer-extraction{background:#dbe2ec;color:var(--syn)}
.no-vals{font-size:10px;color:var(--muted);font-style:italic}
table.spread{table-layout:fixed}
table.spread col.c-ref{width:72px}
table.spread col.c-auth{width:18%}
table.spread col.c-rel{width:18%}
table.spread col.c-tier{width:42px}
table.spread col.c-jur{width:58px}
table.spread col.c-id{width:13%}
table.spread col.c-bib{width:88px}
table.spread col.c-vals{width:auto}
table.spread td,table.spread th{word-wrap:break-word;overflow-wrap:break-word}
table.spread td.c-auth,table.spread td.c-rel{font-size:11px;line-height:1.35}
.tier-row td{background:linear-gradient(to right,var(--ink) 0,var(--ink) 4px,var(--hl) 4px,var(--hl) 100%);
  padding:8px 10px 7px 14px;border-bottom:1px solid var(--ink);border-top:1px solid var(--line)}
.tier-name{font-family:var(--serif);font-weight:700;font-size:13px;color:var(--ink);margin-right:10px}
.tier-disc{font-size:10.5px;color:var(--muted);font-family:var(--serif);font-style:italic}
.no-rel{font-style:italic;color:var(--muted);font-size:10px}
.pop-cell{display:flex;flex-direction:column;gap:2px}
.pop-codes{display:flex;flex-wrap:wrap;gap:3px}
.pop-code{font-family:var(--mono);font-size:10px;font-weight:600;padding:1px 5px;border-radius:2px;
  background:var(--ink);color:var(--paper);letter-spacing:.3px;cursor:help}
.pop-code.all{background:#7a3b12;color:#fff}
.pop-code.drift{background:var(--weak);color:#fff;text-decoration:line-through wavy}
.pop-code.drift::after{content:" ⚠"}
.pop-setting{font-size:10px;color:var(--muted);font-style:italic;line-height:1.3}
.pop-empty{font-size:10px;color:var(--muted);font-style:italic}
.vrow .vpop{display:flex;gap:3px;flex-wrap:wrap;align-items:center}
.vrow .vpop .pop-code{font-size:9px;padding:0 4px}
.vrow .vsetting{font-size:9.5px;color:var(--muted);font-style:italic}
</style></head><body>
<header>
 <h1>Spec Curation Vetting Surface</h1>
 <div class="sub">Per-topic view of the evidence at the Guidebook's disposal, the values extracted from each source, what is selected (overall &amp; per population), and the reasoning. Schema version <b id="sv"></b>. Link integrity verified at build time: <b id="oi"></b> orphan source references. Read-only snapshot of <span class="ref">data/guidebook.db</span>.</div>
 <div class="regen">Auto-regenerated by .github/workflows/regenerate-vetting-surface.yml on every commit that modifies data/guidebook.db.</div>
 <div class="totals">
  <div class="tot"><b id="t-topics"></b><span>topics</span></div>
  <div class="tot"><b id="t-src"></b><span>source-links</span></div>
  <div class="tot new"><b id="t-sext"></b><span>per-source extractions (new layer)</span></div>
  <div class="tot warn"><b id="t-ext"></b><span>synthesis extractions</span></div>
  <div class="tot warn"><b id="t-walk"></b><span>curation walks</span></div>
 </div>
</header>
<div class="ctrl">sort: <select id="sort">
 <option value="src">most sources</option><option value="depth">curation depth</option><option value="name">name A&ndash;Z</option></select>
 <span style="color:var(--muted)">click a topic to inspect its full curation chain</span></div>
<div class="layout">
 <div class="list" id="list"></div>
 <div class="detail" id="detail"><div class="placeholder">Select a topic &rarr;</div></div>
</div>
<div class="legend">
 <span><b>bibliography:</b> <span class="badge b-strong">strong</span> id+complete+verified &middot; <span class="badge b-ok">ok</span> complete/statutory, no DOI &middot; <span class="badge b-weak">weak</span> thin/unverified</span>
 <span><b>extraction status:</b> <span class="badge s-prel">preliminary</span> <span class="badge s-rev">reviewed</span> <span class="badge s-ver">verified</span> <span class="badge s-con">contradicted</span> <span class="badge s-abs">absent-confirmed</span></span>
 <span><b>value-match (synthesis):</b> <span class="badge m-exact">EXACT</span> <span class="badge m-tol">WITHIN-TOL</span></span>
</div>
<script id="vetting-data" type="application/json">__PAYLOAD__</script>
<script>
const DATA=JSON.parse(document.getElementById('vetting-data').textContent);
const BB=DATA.backbone,T=DATA.totals;
const POPS=DATA.populations||{};
function popCell(popStr, setting, settingLabelFallback){
  // popStr: comma-separated codes like 'DEAF' or 'NDV,AUT' or 'ALL' (or null)
  // setting: free-text setting/context (or null)
  let codesHtml='';
  if (popStr) {
    const codes = popStr.split(',').map(x=>x.trim()).filter(Boolean);
    codesHtml = '<div class="pop-codes">' + codes.map(code=>{
      const known = POPS[code];
      if (known) {
        const cls = code==='ALL' ? 'pop-code all' : 'pop-code';
        return '<span class="'+cls+'" title="'+esc(known.display_name)+'">'+esc(code)+'</span>';
      } else {
        return '<span class="pop-code drift" title="not in canonical populations taxonomy">'+esc(code)+'</span>';
      }
    }).join('') + '</div>';
  }
  const settingShow = setting || settingLabelFallback;
  const settingHtml = settingShow ? '<div class="pop-setting">'+esc(settingShow)+'</div>' : '';
  if (!codesHtml && !settingHtml) return '<span class="pop-empty">&mdash;</span>';
  return '<div class="pop-cell">' + codesHtml + settingHtml + '</div>';
}
function popInline(popStr){
  // compact inline rendering for value-pills
  if (!popStr) return '';
  const codes = popStr.split(',').map(x=>x.trim()).filter(Boolean);
  return '<span class="vpop">' + codes.map(code=>{
    const known = POPS[code];
    const cls = !known ? 'pop-code drift' : (code==='ALL' ? 'pop-code all' : 'pop-code');
    const title = known ? known.display_name : 'not in canonical populations taxonomy';
    return '<span class="'+cls+'" title="'+esc(title)+'">'+esc(code)+'</span>';
  }).join('') + '</span>';
}
const $=id=>document.getElementById(id);
$('t-topics').textContent=T.topics;
$('t-src').textContent=T.sources;
$('t-sext').textContent=T.extractions_source;
$('t-ext').textContent=T.extractions_synthesis;
$('t-walk').textContent=T.walks;
$('sv').textContent=T.schema_version;
$('oi').textContent=T.orphan_links;
const list=$('list'),detail=$('detail');
function depth(d){if(d.value_extractions.length)return['full','d-full'];
 if((d.source_extractions||[]).length)return['source','d-src'];
 if(d.selection_walks.length)return['walk','d-walk'];return['none','d-none'];}
function esc(s){return (s==null?'':String(s)).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
function matchClass(m){if(m==='EXACT')return'm-exact';if(m==='WITHIN-TOLERANCE')return'm-tol';return'm-other';}
function statClass(s){return{'preliminary':'s-prel','reviewed':'s-rev','verified':'s-ver','contradicted':'s-con','absent-confirmed':'s-abs'}[s]||'s-prel';}
function idCell(s){const id=s.doi?('doi:'+s.doi):(s.pmid?('PMID:'+s.pmid):null);
 return id?('<span class="badge b-id">'+esc(id)+'</span>'):'<span class="badge b-noid">no id</span>';}
let cur=null;
function renderList(){
 const mode=document.getElementById('sort').value;
 let arr=Object.entries(BB);
 const rank=d=>d.value_extractions.length?3:((d.source_extractions||[]).length?2:(d.selection_walks.length?1:0));
 if(mode==='src')arr.sort((a,b)=>b[1].linked_sources.length-a[1].linked_sources.length);
 else if(mode==='depth')arr.sort((a,b)=>rank(b[1])-rank(a[1])||b[1].linked_sources.length-a[1].linked_sources.length);
 else arr.sort((a,b)=>a[0]<b[0]?-1:1);
 list.innerHTML=arr.map(([slug,d])=>{const[dl,dc]=depth(d);
  return '<div class="topic'+(slug===cur?' active':'')+'" data-s="'+esc(slug)+'">'+
   '<span class="tname">'+esc(slug)+'</span>'+
   '<span class="counts">'+d.linked_sources.length+'src'+
   ((d.source_extractions||[]).length?' &middot; '+d.source_extractions.length+'ext':'')+
   (d.value_extractions.length?' &middot; '+d.value_extractions.length+'syn':'')+
   ' <span class="depth '+dc+'">'+dl+'</span></span></div>';}).join('');
 [...list.querySelectorAll('.topic')].forEach(e=>e.onclick=()=>{cur=e.dataset.s;renderList();renderDetail(cur);});
}
function renderDetail(slug){
 const d=BB[slug];const ls=d.linked_sources,ve=d.value_extractions,sw=d.selection_walks,sx=d.source_extractions||[];
 const steps=[
   {l:'sources',n:ls.length},
   {l:'per-source extractions',n:sx.length},
   {l:'synthesis verifications',n:ve.length},
   {l:'walks',n:new Set(sw.map(p=>p.walk_id)).size}];
 let h='<h2>'+esc(slug)+'</h2><div class="slug">'+ls.length+' linked sources &middot; '+sx.length+' per-source extractions &middot; '+ve.length+' synthesis verifications &middot; '+steps[3].n+' walk(s)</div>';
 h+='<div class="chain">'+steps.map(s=>'<span'+(s.n?' class="here"':' class="empty-step"')+'>'+s.l+': '+s.n+'</span>').join(' &rarr; ')+'</div>';
 h+='<div class="sec"><div class="sec-h">Per-source extractions <em>what each source asserts &middot; per population &middot; pre-synthesis</em></div>';
 if(sx.length){h+='<table><tr><th>source</th><th>parameter</th><th>population &middot; setting</th><th>juris.</th><th>value</th><th>section</th><th>status</th><th>&rarr; rdc</th></tr>';
  sx.forEach(r=>{h+='<tr><td class="ref">'+esc(r.ref_id)+'</td><td>'+esc(r.parameter)+'</td>'+
   '<td>'+popCell(r.population_code, r.setting, r.population_label)+'</td>'+
   '<td>'+esc(r.jurisdiction||'')+'</td>'+
   '<td><span class="val">'+esc(r.claimed_value||'&mdash;')+' '+esc(r.claimed_unit||'')+'</span></td>'+
   '<td><span class="note">'+esc(r.source_section||'')+'</span></td>'+
   '<td><span class="badge '+statClass(r.extraction_status)+'">'+esc(r.extraction_status)+'</span></td>'+
   '<td>'+(r.promoted_to_rdc_id?'<span class="ref">'+esc(r.promoted_to_rdc_id)+'</span>':'<span class="note">&mdash;</span>')+'</td></tr>';});
  h+='</table>';
 }else{h+='<div class="empty info"><b>No per-source extractions yet.</b> '+ls.length+' source-links are present but no values have been pulled from them into the structured layer. Mining this topic creates rows in <span class="ref">source_value_extractions</span> (schema layer added in migration 018).</div>';}
 h+='</div>';
 h+='<div class="sec"><div class="sec-h">Synthesis-verified values <em>re-read &middot; value_match per rule #10</em></div>';
 if(ve.length){h+='<table><tr><th>parameter</th><th>jurisd.</th><th>population &middot; setting</th><th>value</th><th>source &middot; section</th><th>match</th><th>discussion</th></tr>';
  ve.forEach(r=>{h+='<tr><td>'+esc(r.parameter)+'</td><td>'+esc(r.jurisdiction)+'</td>'+
   '<td>'+popCell(r.population, r.setting)+'</td>'+
   '<td><span class="val">'+esc(r.claimed_value)+' '+esc(r.claimed_unit||'')+'</span></td>'+
   '<td><span class="ref">'+esc(r.source_ref_id)+'</span><br><span class="note">'+esc(r.source_section||'')+'</span></td>'+
   '<td>'+(r.value_match?'<span class="badge '+matchClass(r.value_match)+'">'+esc(r.value_match)+'</span>':'')+'</td>'+
   '<td><div class="note clip" onclick="this.classList.toggle(\'clip\')">'+esc(r.notes||'&mdash;')+'</div></td></tr>';});
  h+='</table>';
 }else{h+='<div class="empty"><b>No synthesis-verified values yet.</b> Synthesis rows come from per-source extractions promoted via re-read verification (rule #10 sub-rules 2/3).</div>';}
 h+='</div>';
 if(sw.length){h+='<div class="sec"><div class="sec-h">How the selected value was reached <em>progressive measurement walk</em></div>';
  const walks={};sw.forEach(p=>{(walks[p.walk_id]=walks[p.walk_id]||[]).push(p);});
  Object.entries(walks).forEach(([wid,steps])=>{
   const fin=steps.find(s=>s.phase==='final');
   h+='<div class="walk"><div class="walk-h"><span class="ref">'+esc(wid)+' &middot; item '+esc(steps[0].item_code)+'</span>'+
     (fin?'<span>selected: <span class="val">'+esc(fin.step_value)+' '+esc(fin.step_value_unit||'')+'</span> ('+esc(fin.population)+')</span>':'')+'</div>';
   h+='<div class="step" style="font-weight:600;color:var(--muted);font-size:9px;text-transform:uppercase"><span>#</span><span>phase</span><span>value</span><span>strict</span><span>source</span></div>';
   steps.filter(s=>s.phase!=='final').forEach(s=>{h+='<div class="step'+(s.passes_strict?' final':'')+'"><span>'+s.step_index+'</span><span>'+esc(s.phase)+'</span>'+
     '<span>'+esc(s.step_value)+' '+esc(s.step_value_unit||'')+'</span><span>'+(s.passes_strict?'&#10003; pass':'&mdash;')+'</span>'+
     '<span class="ref">'+esc(s.ref_id||'')+'</span></div>';});
   h+='</div>';});
  h+='</div>';}
 h+='<div class="sec"><div class="sec-h">Evidence spread <em>all sources at disposal &middot; '+ls.length+'</em></div>';
 if(ls.length){
  // Tier-group definition: order T1, Co-1, T2, Co-2, T3, T4, T5, T6 per governance/tier-system.md
  const TIER_GROUPS = [
   {key:'T1', name:'Tier 1', test:s=>s.tier===1 && s.evidence_type!=='co1',
    disc:'Primary research with intervention-level or biomechanical control. Anchors claims that turn on physiological, behavioural, or biomechanical mechanism.'},
   {key:'Co-1', name:'Co-1', test:s=>s.evidence_type==='co1',
    disc:'Disability-led lived-experience publications (DPOs, named-org outputs, CRPD Art. 4.3 consultation). Anchors claims that turn on user preference, dignity, autonomy. Ranks alongside T1 on non-substitutable claim types.'},
   {key:'T2', name:'Tier 2', test:s=>s.tier===2 && s.evidence_type!=='co2',
    disc:'Community-consensus synthesis: systematic reviews / meta-analyses and named-organisation evidence-based standards. Anchors claims that turn on synthesised evidence across multiple primary studies.'},
   {key:'Co-2', name:'Co-2', test:s=>s.evidence_type==='co2',
    disc:'OT / professional-body clinical practice guidelines (CAOT, AOTA, RCOT, COTEC, WFOT, national equivalents). Anchors claims that turn on clinical-professional consensus on rehabilitation or ADL adaptation.'},
   {key:'T3', name:'Tier 3', test:s=>s.tier===3,
    disc:'Lower-control primary research (cross-sectional, observational, qualitative, single-centre) plus grey-literature primary research. Supporting evidence; rarely the sole basis for a claim.'},
   {key:'T4', name:'Tier 4', test:s=>s.tier===4,
    disc:'International standards (ISO, IEC, CEN, BSI PAS, EN 81-70, EN 17210). Code-baseline citations of international harmonisation; supports claims if the standard itself rests on T1/T2 evidence.'},
   {key:'T5', name:'Tier 5', test:s=>s.tier===5 && s.evidence_type!=='co1',
    disc:'National beyond-code frameworks (BS 8300, DIN 18040 draft, Boverket BBR advisories, national CPGs scoped to BE). Best-practice tier at national level; supports claims if framework rests on T1/T2.'},
   {key:'T6', name:'Tier 6', test:s=>s.tier===6,
    disc:'Statutory code &mdash; legally enforceable national / sub-national accessibility codes (ADA, AS 1428.1, Approved Document M, NZ Building Code D1/AS1, GB 50763, etc.). Code-baseline citations only.'},
  ];
  h+='<table class="spread">'+
   '<colgroup><col class="c-ref"><col class="c-auth"><col class="c-rel"><col class="c-tier"><col class="c-jur"><col class="c-id"><col class="c-bib"><col class="c-vals"></colgroup>'+
   '<tr><th>ref</th><th>author (year)</th><th>relevance to this topic</th><th>tier</th><th>juris.</th><th>identifier</th><th>biblio.</th><th>values cited from this source</th></tr>';
  let unBucketed=ls.slice();
  TIER_GROUPS.forEach(g=>{
   const inGroup = ls.filter(g.test);
   if (!inGroup.length) return;
   unBucketed = unBucketed.filter(s=>!g.test(s));
   h+='<tr class="tier-row"><td colspan="8"><span class="tier-name">'+g.name+'</span><span class="tier-disc">'+g.disc+' &nbsp;&middot;&nbsp; '+inGroup.length+' source'+(inGroup.length===1?'':'s')+'</span></td></tr>';
   inGroup.forEach(s=>{const v=s._v.verdict;const vc=s.values_cited||[];
    const valsHtml = vc.length ? '<div class="values">' + vc.map(x=>{
      const lay=x.layer||'extraction';
      const popH = popInline(x.population);
      const setH = x.setting ? '<span class="vsetting">'+esc(x.setting)+'</span>' : '';
      const jurH = x.jurisdiction ? '<span class="vmeta">'+esc(x.jurisdiction)+'</span>' : '';
      return '<div class="vrow"><span class="layer-pill layer-'+lay+'">'+lay+'</span>'+
        '<span class="vval">'+esc(x.value||'&mdash;')+' '+esc(x.unit||'')+'</span>'+
        '<span class="vmeta">'+esc(x.parameter||'')+'</span>'+jurH+popH+setH+'</div>';
    }).join('') + '</div>' : '<span class="no-vals">no values extracted from this source yet</span>';
    const relHtml = s.relevance_note
      ? esc(s.relevance_note)
      : '<span class="no-rel">no relevance note recorded</span>';
    h+='<tr><td class="ref">'+esc(s.ref_id)+'</td>'+
     '<td class="c-auth">'+esc(s.author_display||'&mdash;')+' '+(s.pub_year?'('+esc(s.pub_year)+')':'')+'</td>'+
     '<td class="c-rel">'+relHtml+'</td>'+
     '<td class="tier">T'+esc(s.tier)+'</td><td>'+esc(s.jurisdiction||'&mdash;')+'</td>'+
     '<td>'+idCell(s)+'</td>'+
     '<td><span class="badge b-'+v+'">'+v+'</span></td>'+
     '<td>'+valsHtml+'</td></tr>';});
  });
  // Catch any sources that didn't match any group (shouldn't happen given T1-T6 coverage)
  if (unBucketed.length) {
   h+='<tr class="tier-row"><td colspan="8"><span class="tier-name">Other</span><span class="tier-disc">Sources outside the T1&ndash;T6 / Co-1 / Co-2 ladder. Investigate.</span></td></tr>';
   unBucketed.forEach(s=>{const v=s._v.verdict;
     h+='<tr><td class="ref">'+esc(s.ref_id)+'</td>'+
      '<td class="c-auth">'+esc(s.author_display||'&mdash;')+' '+(s.pub_year?'('+esc(s.pub_year)+')':'')+'</td>'+
      '<td class="c-rel"><span class="no-rel">no relevance note recorded</span></td>'+
      '<td class="tier">T'+esc(s.tier)+'</td><td>'+esc(s.jurisdiction||'&mdash;')+'</td>'+
      '<td>'+idCell(s)+'</td>'+
      '<td><span class="badge b-'+v+'">'+v+'</span></td>'+
      '<td><span class="no-vals">no values extracted from this source yet</span></td></tr>';
   });
  }
  h+='</table>';}else h+='<div class="empty">No sources linked.</div>';
 h+='</div>';
 detail.innerHTML=h;
}
document.getElementById('sort').onchange=renderList;
renderList();
cur=Object.entries(BB).sort((a,b)=>b[1].value_extractions.length-a[1].value_extractions.length)[0][0];
renderList();renderDetail(cur);
</script></body></html>"""


def render(data: dict, out_path: Path) -> int:
    """Write the HTML file. Returns bytes written."""
    payload = json.dumps(data, separators=(",", ":"), sort_keys=True)
    html = HTML_TEMPLATE.replace("__PAYLOAD__", payload)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    return len(html)


def main():
    ap = argparse.ArgumentParser(description="Regenerate the spec-curation vetting surface.")
    ap.add_argument(
        "--db",
        type=Path,
        default=Path(os.environ.get("GUIDEBOOK_DB_PATH", str(DEFAULT_DB))),
        help="Path to data/guidebook.db (default: ./data/guidebook.db)",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help="Output HTML path (default: tools/spec-curation-vetting-surface.html)",
    )
    args = ap.parse_args()

    if not args.db.exists():
        print(f"ERROR: DB not found at {args.db}", file=sys.stderr)
        sys.exit(2)

    data = fetch_backbone(args.db)
    n = render(data, args.out)
    t = data["totals"]
    print(
        f"wrote {args.out}  ({n // 1024} KB)  "
        f"schema=v{t['schema_version']}  topics={t['topics']}  "
        f"sources={t['sources']}  "
        f"extractions={t['extractions_source']}/{t['extractions_synthesis']}  "
        f"orphans={t['orphan_links']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
