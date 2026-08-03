#!/usr/bin/env python3
"""Pipeline completeness dashboard generator.

Reads ``data/guidebook.db`` (read-only) and emits a self-contained HTML
dashboard reporting the completeness of each stage of the evidence pipeline
(research -> collection -> judgment -> synthesis -> render), with per-category,
per-item, and per-population breakdowns. The enforcement-coverage panel is read
from ``governance/pipeline-contract.yaml``.

Determinism / loop safety: the report's "as-of" date is derived from the DB's
own ``max(updated_at)``, never wall-clock, and every metric is a pure function
of the DB and the contract file, so identical inputs yield byte-identical
output -- the guarantee the CI drift-check (``--check``) relies on. Read-only on
the DB; writes only the HTML file.

Usage:
  python3 tools/pipeline_completeness.py                  # write the dashboard
  python3 tools/pipeline_completeness.py --check          # exit 1 if stale
  python3 tools/pipeline_completeness.py --format fragment # claude.ai artifact body
  GUIDEBOOK_DB_PATH=... python3 tools/pipeline_completeness.py
"""
from __future__ import annotations

import argparse
import html
import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = REPO_ROOT / "data" / "guidebook.db"
DEFAULT_OUT = REPO_ROOT / "tools" / "pipeline-completeness-dashboard.html"
CONTRACT = REPO_ROOT / "governance" / "pipeline-contract.yaml"

# The canonical pipeline spine (governance/pipeline-contract.yaml).
STAGES = ["research", "collection", "judgment", "synthesis", "render"]


# ---------------------------------------------------------------------------
# Data gathering (read-only; deterministic)
# ---------------------------------------------------------------------------
def connect_ro(db_path: Path) -> sqlite3.Connection:
    return sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)


def gather(con: sqlite3.Connection) -> dict:
    cur = con.cursor()

    def scalar(q, *a):
        row = cur.execute(q, a).fetchone()
        return (row[0] if row and row[0] is not None else 0)

    def rows(q, *a):
        return cur.execute(q, a).fetchall()

    F: dict = {}

    # Provenance / determinism -------------------------------------------------
    F["as_of"] = str(scalar(
        "SELECT MAX(d) FROM ("
        " SELECT MAX(updated_at) d FROM items"
        " UNION ALL SELECT MAX(updated_at) FROM evidence_sources"
        " UNION ALL SELECT MAX(updated_at) FROM evidence_cell_state"
        " UNION ALL SELECT MAX(updated_at) FROM bpc_metadata"
        " UNION ALL SELECT MAX(updated_at) FROM gaps)"
    ) or "")[:10]
    F["user_version"] = scalar("PRAGMA user_version")
    F["migrations"] = scalar("SELECT COUNT(*) FROM data_migrations")

    # Totals (denominators) ----------------------------------------------------
    items_total = scalar("SELECT COUNT(*) FROM items")
    items_with_slug = scalar(
        "SELECT COUNT(*) FROM items WHERE bpc_source_slug IS NOT NULL AND bpc_source_slug<>''")
    slugs_total = scalar("SELECT COUNT(*) FROM bpc_metadata")
    sources_total = scalar("SELECT COUNT(*) FROM evidence_sources")
    applicable_pairs = scalar("SELECT COUNT(*) FROM item_population_links")
    F.update(items_total=items_total, items_with_slug=items_with_slug,
             slugs_total=slugs_total, sources_total=sources_total,
             applicable_pairs=applicable_pairs)

    # Stage 1 -- research ------------------------------------------------------
    F["research"] = dict(
        search_complete=scalar("SELECT COALESCE(SUM(search_complete),0) FROM bpc_metadata"),
        pico_complete=scalar("SELECT COALESCE(SUM(pico_complete),0) FROM bpc_metadata"),
        coverage_slugs=scalar(
            "SELECT COUNT(DISTINCT slug) FROM search_coverage WHERE status IN ('SEARCHED','THIN')"),
        coverage_done=scalar(
            "SELECT COUNT(*) FROM search_coverage WHERE status IN ('SEARCHED','THIN')"),
        coverage_total=scalar("SELECT COUNT(*) FROM search_coverage"),
        gaps_closed=scalar("SELECT COUNT(*) FROM gaps WHERE status LIKE 'CLOSED%'"),
        gaps_total=scalar("SELECT COUNT(*) FROM gaps"),
    )

    # Stage 2 -- collection ----------------------------------------------------
    F["collection"] = dict(
        verified=scalar("SELECT COUNT(*) FROM evidence_sources WHERE verification_status LIKE 'VERIFIED%'"),
        meta_complete=scalar(
            "SELECT COUNT(*) FROM evidence_sources WHERE metadata_quality IN ('COMPLETE','COMPLETE-STATUTORY')"),
        author_title_only=scalar(
            "SELECT COUNT(*) FROM evidence_sources WHERE metadata_quality='AUTHOR-TITLE-ONLY'"),
        provenance=scalar(
            "SELECT COUNT(*) FROM evidence_sources WHERE derivation_chain IS NOT NULL AND TRIM(derivation_chain)<>''"),
        citation_mining=scalar("SELECT COALESCE(SUM(citation_mining_complete),0) FROM bpc_metadata"),
    )

    # Stage 3 -- judgment ------------------------------------------------------
    cells_total = scalar("SELECT COUNT(*) FROM evidence_cell_state")
    state_counts = {s: n for s, n in rows(
        "SELECT state, COUNT(*) FROM evidence_cell_state GROUP BY state")}
    F["judgment"] = dict(
        cells=cells_total,
        items_judged=scalar("SELECT COUNT(DISTINCT item_code) FROM evidence_cell_state"),
        stated=state_counts.get("stated", 0),
        provisional=state_counts.get("provisional", 0),
        pending=state_counts.get("pending", 0),
        not_applicable=state_counts.get("not_applicable", 0),
        govrefs_ok=scalar(
            "SELECT COUNT(*) FROM evidence_cell_state WHERE state IN ('stated','provisional') "
            "AND governing_refs IS NOT NULL AND TRIM(governing_refs)<>''"),
        govrefs_denom=scalar(
            "SELECT COUNT(*) FROM evidence_cell_state WHERE state IN ('stated','provisional')"),
        convergence=scalar("SELECT COUNT(*) FROM convergence_assessment"),
        value_extractions=scalar("SELECT COUNT(*) FROM source_value_extractions"),
    )

    # Stage 4 -- synthesis -----------------------------------------------------
    F["synthesis"] = dict(
        reasoning_slugs=scalar("SELECT COUNT(DISTINCT reasoning_doc_slug) FROM reasoning_doc_citations"),
        reasoning_citations=scalar("SELECT COUNT(*) FROM reasoning_doc_citations"),
        partial_slugs=scalar("SELECT COUNT(*) FROM bpc_metadata WHERE evidence_state='PARTIAL'"),
        # Live item-facing synthesis: an item whose linked BPC slug is not retracted/empty.
        live_item_synth=scalar(
            "SELECT COUNT(*) FROM items i JOIN bpc_metadata b ON b.slug=i.bpc_source_slug "
            "WHERE b.evidence_state IS NOT NULL AND b.evidence_state NOT IN "
            "('RETRACTED-PRE-REHAB','PARTIAL')"),
    )
    F["bpc_states"] = rows(
        "SELECT COALESCE(evidence_state,'(unset)') s, COUNT(*) n FROM bpc_metadata "
        "GROUP BY evidence_state ORDER BY n DESC, s")

    # Stage 5 -- render (render-readiness of determinations) -------------------
    F["render"] = dict(
        render_ready=scalar(
            "SELECT COUNT(*) FROM evidence_cell_state WHERE state IN ('stated','provisional') "
            "AND design_scale IS NOT NULL AND TRIM(design_scale)<>''"),
        design_scales=scalar(
            "SELECT COUNT(*) FROM (SELECT DISTINCT design_scale FROM evidence_cell_state "
            "WHERE design_scale IS NOT NULL)"),
    )

    # Breakdown by category ----------------------------------------------------
    cats = []
    for (cat,) in rows("SELECT DISTINCT category FROM items ORDER BY category"):
        cats.append(dict(
            cat=cat,
            items=scalar("SELECT COUNT(*) FROM items WHERE category=?", cat),
            with_slug=scalar(
                "SELECT COUNT(*) FROM items WHERE category=? AND bpc_source_slug IS NOT NULL "
                "AND bpc_source_slug<>''", cat),
            judged=scalar(
                "SELECT COUNT(DISTINCT item_code) FROM evidence_cell_state WHERE item_code IN "
                "(SELECT item_code FROM items WHERE category=?)", cat),
            pop_breadth=scalar(
                "SELECT COUNT(DISTINCT population_code) FROM item_population_links WHERE item_code IN "
                "(SELECT item_code FROM items WHERE category=?)", cat),
            states=[
                f"{s.lower().replace('-pre-rehab','')}×{n}" for s, n in rows(
                    "SELECT b.evidence_state s, COUNT(*) n FROM items i "
                    "JOIN bpc_metadata b ON b.slug=i.bpc_source_slug WHERE i.category=? "
                    "AND b.evidence_state IS NOT NULL GROUP BY b.evidence_state ORDER BY n DESC, s", cat)
            ],
        ))
    F["categories"] = cats

    # Breakdown by population (class) -----------------------------------------
    pops = []
    for code, cat, name in rows(
            "SELECT population_code, COALESCE(category,''), COALESCE(display_name,'') FROM populations"):
        applies = scalar(
            "SELECT COUNT(DISTINCT item_code) FROM item_population_links WHERE population_code=?", code)
        det = scalar("SELECT COUNT(*) FROM evidence_cell_state WHERE population_code=?", code)
        if applies or det:
            pops.append(dict(code=code, cls=cat, name=name, applies=applies, det=det))
    pops.sort(key=lambda p: (-p["applies"], -p["det"], p["code"]))
    F["populations"] = pops

    # Item frontier (items that reached judgment) ------------------------------
    synth_slugs = {s for (s,) in rows("SELECT DISTINCT reasoning_doc_slug FROM reasoning_doc_citations")}
    # slug(s) an item is bound to, via bpc_source_slug or item_bpc_links
    frontier = []
    judged_items = [r[0] for r in rows(
        "SELECT DISTINCT item_code FROM evidence_cell_state ORDER BY item_code")]
    for item in judged_items:
        cells = rows(
            "SELECT population_code, state FROM evidence_cell_state WHERE item_code=? "
            "ORDER BY CASE state WHEN 'stated' THEN 0 WHEN 'provisional' THEN 1 "
            "WHEN 'pending' THEN 2 ELSE 3 END, population_code", item)
        item_slugs = {r[0] for r in rows(
            "SELECT bpc_source_slug FROM items WHERE item_code=? AND bpc_source_slug IS NOT NULL", item)}
        item_slugs |= {r[0] for r in rows(
            "SELECT slug FROM item_bpc_links WHERE item_code=?", item)}
        frontier.append(dict(
            item=item,
            cells=[dict(pop=p, state=s) for p, s in cells],
            synthesized=bool(item_slugs & synth_slugs),
        ))
    # champion first (has a reasoning doc), then by cell count, then code
    frontier.sort(key=lambda f: (0 if f["synthesized"] else 1, -len(f["cells"]), f["item"]))
    F["frontier"] = frontier

    return F


def gather_enforcement(contract_path: Path) -> dict:
    """Per-stage enforcement coverage from the pipeline contract (check != null).

    Errors are raised, never swallowed: a silent fallback would make the output
    depend on whether PyYAML is importable, which would break the byte-identical
    ``--check`` guarantee. PyYAML is a pinned project dependency (requirements.txt);
    CI installs it before running this generator.
    """
    out = {s: dict(verifiable=0, incomplete=0) for s in STAGES}
    try:
        import yaml  # PyYAML is a pinned dependency (requirements.txt)
    except ImportError as exc:  # pragma: no cover - environment guard
        raise SystemExit(
            "error: PyYAML is required (pip install pyyaml or -r requirements.txt)") from exc
    data = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    for stage in data.get("stages", []):
        sid = stage.get("id")
        if sid not in out:
            continue
        for crit in stage.get("criteria", []):
            key = "verifiable" if crit.get("check") else "incomplete"
            out[sid][key] += 1
    return out


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------
def pct(n: int, d: int) -> int:
    return round(100 * n / d) if d else 0


def band(p: int) -> str:
    if p <= 0:
        return "b0"
    if p < 15:
        return "b1"
    if p < 50:
        return "b2"
    if p < 85:
        return "b3"
    return "b4"


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def gauge(idx: int, name: str, n: int, d: int, denom_label: str, tag: str) -> str:
    p = pct(n, d)
    b = band(p)
    # keep an at-a-glance sliver even at 0-1%
    w = max(p, 2)
    return f"""      <div class="gauge">
        <div class="stage-idx">STAGE {idx}</div><div class="stage-name">{esc(name)}</div>
        <div class="pct {b}-fg">{p}<small>%</small></div>
        <div class="denom">{n} / {d}<br>{esc(denom_label)}</div>
        <div class="bar"><i class="{b}-bg-solid" style="width:{w}%"></i></div>
        <span class="stage-tag {b}-tag">{esc(tag)}</span>
      </div>"""


def metric(lbl: str, val: str, n: int | None = None, d: int | None = None) -> str:
    bar = ""
    if n is not None and d is not None:
        p = pct(n, d)
        bar = (f'\n          <span class="mini-bar"><i class="{band(p)}-bg-solid" '
               f'style="width:{max(p, 2)}%"></i></span>')
    return (f'          <div class="metric-row"><span class="lbl">{lbl}</span>'
            f'<span class="val">{val}</span>{bar}</div>')


def chip(text: str, ok: bool) -> str:
    cls = "ver" if ok else "inc"
    dot = "b4" if ok else "b2"
    return f'<span class="chip {cls}"><span class="g {dot}-bg-solid"></span>{esc(text)}</span>'


def heat(n: int, d: int) -> str:
    p = pct(n, d)
    b = band(p)
    return (f'<span class="heat"><span class="sw {b}-sw">'
            f'<i class="{b}-bg-solid" style="width:{max(p, 3)}%"></i></span>'
            f'<span class="frac">{n}/{d} · {p}%</span></span>')


STATE_BAND = {"stated": "b4", "provisional": "b2", "pending": "b0",
              "not_applicable": "b0"}
STATE_SHORT = {"stated": "stated", "provisional": "prov", "pending": "pending",
               "not_applicable": "n/a"}


def cellpill(pop: str, state: str) -> str:
    b = STATE_BAND.get(state, "b0")
    return (f'<span class="cellpill st-{state}"><span class="g {b}-bg-solid"></span>'
            f'{esc(pop)} · {esc(STATE_SHORT.get(state, state))}</span>')


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
CSS = """
  :root{
    --paper:#f6f7f9; --card:#fff; --ink:#131a1f; --ink-2:#43535e; --ink-3:#6b7a85;
    --line:#dde3e8; --line-2:#eaeef1; --accent:#3a6ea5; --accent-soft:#e7eef6;
    --b0:#9aa7b0; --b1:#c0603a; --b2:#d69a3c; --b3:#7fa04d; --b4:#3c8f6b;
    --b0-bg:#eceff1; --b1-bg:#f7e4dc; --b2-bg:#f8ecd6; --b3-bg:#e9eed9; --b4-bg:#dcefe6;
    --shadow:0 1px 2px rgba(16,24,32,.05),0 8px 24px rgba(16,24,32,.05);
    --mono:ui-monospace,"SF Mono","Cascadia Code","JetBrains Mono",Menlo,Consolas,monospace;
    --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  }
  @media (prefers-color-scheme:dark){:root{
    --paper:#0e1418; --card:#151d23; --ink:#e7edf1; --ink-2:#a9b7c1; --ink-3:#7c8b95;
    --line:#263139; --line-2:#1d262d; --accent:#6ea0d6; --accent-soft:#1a2735;
    --b0:#5d6b74; --b1:#d1734d; --b2:#e0ad57; --b3:#9bbb63; --b4:#4faa84;
    --b0-bg:#1b242b; --b1-bg:#33211a; --b2-bg:#2c2415; --b3-bg:#26301a; --b4-bg:#16302a;
    --shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px rgba(0,0,0,.35);
  }}
  :root[data-theme="light"]{
    --paper:#f6f7f9; --card:#fff; --ink:#131a1f; --ink-2:#43535e; --ink-3:#6b7a85;
    --line:#dde3e8; --line-2:#eaeef1; --accent:#3a6ea5; --accent-soft:#e7eef6;
    --b0:#9aa7b0; --b1:#c0603a; --b2:#d69a3c; --b3:#7fa04d; --b4:#3c8f6b;
    --b0-bg:#eceff1; --b1-bg:#f7e4dc; --b2-bg:#f8ecd6; --b3-bg:#e9eed9; --b4-bg:#dcefe6;
  }
  :root[data-theme="dark"]{
    --paper:#0e1418; --card:#151d23; --ink:#e7edf1; --ink-2:#a9b7c1; --ink-3:#7c8b95;
    --line:#263139; --line-2:#1d262d; --accent:#6ea0d6; --accent-soft:#1a2735;
    --b0:#5d6b74; --b1:#d1734d; --b2:#e0ad57; --b3:#9bbb63; --b4:#4faa84;
    --b0-bg:#1b242b; --b1-bg:#33211a; --b2-bg:#2c2415; --b3-bg:#26301a; --b4-bg:#16302a;
  }
  *{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%}
  body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
    line-height:1.55;-webkit-font-smoothing:antialiased}
  .wrap{max-width:1080px;margin:0 auto;padding:clamp(20px,4vw,56px) clamp(16px,4vw,40px) 80px}
  h1,h2,h3{text-wrap:balance;line-height:1.15;margin:0}
  a{color:var(--accent)}
  .mono,.num{font-family:var(--mono);font-variant-numeric:tabular-nums}
  /* status tokens */
  .b0-fg{color:var(--b0)} .b1-fg{color:var(--b1)} .b2-fg{color:var(--b2)} .b3-fg{color:var(--b3)} .b4-fg{color:var(--b4)}
  .b0-bg-solid{background:var(--b0)} .b1-bg-solid{background:var(--b1)} .b2-bg-solid{background:var(--b2)}
  .b3-bg-solid{background:var(--b3)} .b4-bg-solid{background:var(--b4)}
  .b0-tag{color:var(--b0);background:var(--b0-bg)} .b1-tag{color:var(--b1);background:var(--b1-bg)}
  .b2-tag{color:var(--b2);background:var(--b2-bg)} .b3-tag{color:var(--b3);background:var(--b3-bg)}
  .b4-tag{color:var(--b4);background:var(--b4-bg)}
  .b0-sw{background:var(--b0-bg);border-color:var(--b0)} .b1-sw{background:var(--b1-bg);border-color:var(--b1)}
  .b2-sw{background:var(--b2-bg);border-color:var(--b2)} .b3-sw{background:var(--b3-bg);border-color:var(--b3)}
  .b4-sw{background:var(--b4-bg);border-color:var(--b4)}
  /* header */
  header.top{border-bottom:1px solid var(--line);padding-bottom:24px;margin-bottom:32px}
  .eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;
    color:var(--accent);margin-bottom:14px}
  h1{font-size:clamp(26px,4.4vw,40px);font-weight:680;letter-spacing:-.02em}
  .lede{color:var(--ink-2);font-size:clamp(15px,1.7vw,17px);max-width:64ch;margin-top:12px}
  .meta-row{display:flex;flex-wrap:wrap;gap:8px 20px;margin-top:18px;font-family:var(--mono);
    font-size:12px;color:var(--ink-3)}
  .meta-row b{color:var(--ink-2);font-weight:600}
  section{margin-top:48px}
  .sec-head{display:flex;align-items:baseline;gap:12px;margin-bottom:18px;flex-wrap:wrap}
  .sec-head h2{font-size:clamp(19px,2.4vw,23px);font-weight:640;letter-spacing:-.01em}
  .sec-num{font-family:var(--mono);color:var(--accent);font-size:13px;font-weight:600}
  .sec-sub{color:var(--ink-3);font-size:13.5px}
  /* gauges */
  .gauges{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}
  @media (max-width:860px){.gauges{grid-template-columns:repeat(2,1fr)}}
  @media (max-width:480px){.gauges{grid-template-columns:1fr}}
  .gauge{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 15px 15px;
    box-shadow:var(--shadow);position:relative;overflow:hidden}
  .gauge .stage-idx{font-family:var(--mono);font-size:11px;color:var(--ink-3);letter-spacing:.1em}
  .gauge .stage-name{font-size:14px;font-weight:640;margin-top:2px}
  .gauge .pct{font-family:var(--mono);font-variant-numeric:tabular-nums;font-weight:680;font-size:30px;
    letter-spacing:-.02em;margin-top:12px;line-height:1}
  .gauge .pct small{font-size:15px;font-weight:600;color:var(--ink-3)}
  .gauge .denom{font-family:var(--mono);font-size:11.5px;color:var(--ink-3);margin-top:6px}
  .bar{height:6px;border-radius:4px;background:var(--line-2);margin-top:12px;overflow:hidden}
  .bar>i{display:block;height:100%;border-radius:4px}
  .stage-tag{display:inline-block;margin-top:11px;font-family:var(--mono);font-size:10.5px;letter-spacing:.05em;
    text-transform:uppercase;padding:2px 7px;border-radius:999px;font-weight:600}
  .pattern{margin-top:16px;background:var(--accent-soft);border:1px solid var(--line);
    border-left:3px solid var(--accent);border-radius:10px;padding:14px 16px;font-size:14.5px;color:var(--ink-2)}
  .pattern b{color:var(--ink)}
  .caveat{background:var(--b2-bg);border:1px solid var(--line);border-left:3px solid var(--b2);
    border-radius:10px;padding:15px 17px;font-size:14px;color:var(--ink-2)}
  .caveat h3{font-size:14px;color:var(--ink);margin-bottom:6px;display:flex;align-items:center;gap:8px}
  .caveat h3 .dot{width:8px;height:8px;border-radius:50%;background:var(--b2);display:inline-block;flex:none}
  /* stage detail */
  .stage-detail{background:var(--card);border:1px solid var(--line);border-radius:12px;
    box-shadow:var(--shadow);overflow:hidden}
  .stage-block{display:grid;grid-template-columns:190px 1fr;border-top:1px solid var(--line-2)}
  .stage-block:first-child{border-top:none}
  @media (max-width:720px){.stage-block{grid-template-columns:1fr}}
  .sb-left{padding:18px;border-right:1px solid var(--line-2)}
  @media (max-width:720px){.sb-left{border-right:none;border-bottom:1px solid var(--line-2)}}
  .sb-left .n{font-family:var(--mono);font-size:11px;color:var(--ink-3);letter-spacing:.1em}
  .sb-left .t{font-size:16px;font-weight:660;margin-top:3px}
  .sb-left .entry{font-size:12.5px;color:var(--ink-3);margin-top:8px}
  .sb-right{padding:16px 18px}
  .metric-row{display:grid;grid-template-columns:1fr auto;gap:4px 14px;align-items:center;padding:7px 0;
    border-top:1px dashed var(--line-2)}
  .metric-row:first-child{border-top:none}
  .metric-row .lbl{font-size:13.5px;color:var(--ink-2)}
  .metric-row .val{font-family:var(--mono);font-variant-numeric:tabular-nums;font-size:13.5px;font-weight:600;
    white-space:nowrap}
  .mini-bar{grid-column:1/-1;height:5px;border-radius:3px;background:var(--line-2);overflow:hidden}
  .mini-bar>i{display:block;height:100%;border-radius:3px}
  .gates{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
  .chip{font-family:var(--mono);font-size:11px;padding:3px 9px;border-radius:999px;font-weight:600;
    border:1px solid var(--line);display:inline-flex;align-items:center;gap:6px}
  .chip.ver{color:var(--b4);background:var(--b4-bg);border-color:transparent}
  .chip.inc{color:var(--b2);background:var(--b2-bg);border-color:transparent}
  .chip .g{width:6px;height:6px;border-radius:50%;flex:none}
  .gate-label{font-family:var(--mono);font-size:11px;color:var(--ink-3);margin-top:12px;text-transform:uppercase;
    letter-spacing:.08em}
  /* tables */
  .tbl-scroll{overflow-x:auto;border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);
    background:var(--card)}
  table{border-collapse:collapse;width:100%;font-size:13.5px}
  th,td{padding:10px 14px;text-align:left;border-top:1px solid var(--line-2);white-space:nowrap}
  thead th{background:var(--card);border-top:none;border-bottom:1px solid var(--line);position:sticky;top:0;
    font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--ink-3);font-weight:600}
  tbody tr:hover td{background:color-mix(in srgb,var(--accent) 5%,transparent)}
  td.code,th.code{font-family:var(--mono);font-weight:600}
  td.n,th.n{font-family:var(--mono);font-variant-numeric:tabular-nums;text-align:right}
  .heat{display:inline-flex;align-items:center;gap:8px}
  .heat .sw{width:30px;height:18px;border-radius:5px;flex:none;border:1px solid;overflow:hidden;display:block}
  .heat .sw>i{display:block;height:100%;border-radius:4px}
  .heat .frac{font-family:var(--mono);font-variant-numeric:tabular-nums;font-size:12.5px;color:var(--ink-2)}
  .ratio-cell{min-width:150px}
  .state-badge{font-family:var(--mono);font-size:11px;padding:2px 8px;border-radius:6px;color:var(--b1);
    background:var(--b1-bg);font-weight:600}
  /* frontier */
  .frontier{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
  @media (max-width:680px){.frontier{grid-template-columns:1fr}}
  .item-card{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:14px 15px;
    box-shadow:var(--shadow)}
  .item-card.champ{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent),var(--shadow)}
  .item-card .ih{display:flex;align-items:baseline;justify-content:space-between;gap:10px}
  .item-card .ic{font-family:var(--mono);font-weight:680;font-size:16px}
  .item-card .inm{font-size:12.5px;color:var(--ink-3);text-align:right}
  .champ-tag{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;
    color:var(--accent);background:var(--accent-soft);padding:2px 7px;border-radius:999px;font-weight:700}
  .cells{display:flex;flex-wrap:wrap;gap:6px;margin-top:11px}
  .cellpill{font-family:var(--mono);font-size:11.5px;padding:3px 9px;border-radius:6px;font-weight:600;
    display:inline-flex;gap:6px;align-items:center;border:1px solid var(--line)}
  .st-stated{color:var(--b4);background:var(--b4-bg);border-color:transparent}
  .st-provisional{color:var(--b2);background:var(--b2-bg);border-color:transparent}
  .st-pending,.st-not_applicable{color:var(--ink-3);background:var(--b0-bg);border-color:transparent}
  .cellpill .g{width:6px;height:6px;border-radius:50%;flex:none}
  .synth-note{margin-top:11px;font-size:12.5px;color:var(--ink-3);padding-top:10px;border-top:1px dashed var(--line-2)}
  .synth-note b{color:var(--b4)}
  .equity{background:var(--b1-bg);border:1px solid var(--line);border-left:3px solid var(--b1);border-radius:10px;
    padding:14px 16px;font-size:13.5px;color:var(--ink-2);margin-top:14px}
  .equity b{color:var(--ink)}
  .legend{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;margin-top:16px;font-family:var(--mono);
    font-size:11.5px;color:var(--ink-3)}
  .legend .li{display:inline-flex;align-items:center;gap:6px}
  .legend .sw{width:22px;height:13px;border-radius:4px}
  footer{margin-top:56px;padding-top:20px;border-top:1px solid var(--line);font-size:12.5px;color:var(--ink-3)}
  footer code{font-family:var(--mono);background:var(--line-2);padding:1px 5px;border-radius:4px;color:var(--ink-2)}
  .two-col{display:grid;grid-template-columns:1fr 1fr;gap:14px}
  @media (max-width:720px){.two-col{grid-template-columns:1fr}}
"""


# ---------------------------------------------------------------------------
# HTML assembly
# ---------------------------------------------------------------------------
def render_body(F: dict, enf: dict) -> str:
    r, c, j, sy, rd = (F["research"], F["collection"], F["judgment"],
                       F["synthesis"], F["render"])
    slugs, srcs, items, pairs = (F["slugs_total"], F["sources_total"],
                                 F["items_total"], F["applicable_pairs"])

    # gauge tags derived from the band so they self-describe
    def tag_for(p):
        return {"b0": "None", "b1": "Minimal", "b2": "Low", "b3": "Partial", "b4": "High"}[band(p)]

    g = [
        gauge(1, "Research", r["search_complete"], slugs, "search-complete slugs",
              tag_for(pct(r["search_complete"], slugs))),
        gauge(2, "Collection", c["meta_complete"], srcs, "metadata-complete sources",
              tag_for(pct(c["meta_complete"], srcs))),
        gauge(3, "Judgment", j["cells"], pairs, "cells determined",
              tag_for(pct(j["cells"], pairs))),
        gauge(4, "Synthesis", sy["reasoning_slugs"], slugs, "slugs w/ reasoning doc",
              tag_for(pct(sy["reasoning_slugs"], slugs))),
        gauge(5, "Render", rd["render_ready"], pairs, "cells render-ready",
              tag_for(pct(rd["render_ready"], pairs))),
    ]

    # enforcement summary line
    ver_total = sum(e["verifiable"] for e in enf.values())
    inc_total = sum(e["incomplete"] for e in enf.values())
    enf_line = " · ".join(
        f'{s} <span class="mono">{enf[s]["verifiable"]}/{enf[s]["verifiable"]+enf[s]["incomplete"]}</span>'
        for s in STAGES)

    # ---- stage detail blocks ----
    research_block = f"""      <div class="stage-block">
        <div class="sb-left"><div class="n">STAGE 1</div><div class="t">Research</div>
          <div class="entry">Entry: an open gap or a parameter lacking sufficient evidence.</div></div>
        <div class="sb-right">
{metric("Slugs with search complete", f'{r["search_complete"]} / {slugs} · {pct(r["search_complete"], slugs)}%', r["search_complete"], slugs)}
{metric("Slugs touched by search coverage", f'{r["coverage_slugs"]} / {slugs} · {pct(r["coverage_slugs"], slugs)}%', r["coverage_slugs"], slugs)}
{metric("Slug × jurisdiction cells searched", f'{r["coverage_done"]} / {r["coverage_total"]} · {pct(r["coverage_done"], r["coverage_total"])}%', r["coverage_done"], r["coverage_total"])}
{metric("PICO formalized", f'{r["pico_complete"]} / {slugs} · {pct(r["pico_complete"], slugs)}%', r["pico_complete"], slugs)}
{metric("Gaps closed (register)", f'{r["gaps_closed"]} / {r["gaps_total"]} · {pct(r["gaps_closed"], r["gaps_total"])}%', r["gaps_closed"], r["gaps_total"])}
          <div class="gate-label">Integrity gates</div>
          <div class="gates">{chip("adversarial-fields", True)}{chip("pmp-strict-termination", True)}</div>
        </div>
      </div>"""

    collection_block = f"""      <div class="stage-block">
        <div class="sb-left"><div class="n">STAGE 2</div><div class="t">Collection</div>
          <div class="entry">Entry: sources discovered for the topic under research.</div></div>
        <div class="sb-right">
{metric("Sources verified", f'{c["verified"]} / {srcs} · {pct(c["verified"], srcs)}%', c["verified"], srcs)}
{metric("Metadata complete", f'{c["meta_complete"]} / {srcs} · {pct(c["meta_complete"], srcs)}%', c["meta_complete"], srcs)}
{metric("Author-title-only (rule&nbsp;#10 blockers)", f'{c["author_title_only"]} · {pct(c["author_title_only"], srcs)}%', c["author_title_only"], srcs)}
{metric("Discovery provenance recorded", f'{c["provenance"]} / {srcs} · {pct(c["provenance"], srcs)}%', c["provenance"], srcs)}
{metric("Citation-mining complete (slugs)", f'{c["citation_mining"]} / {slugs} · {pct(c["citation_mining"], slugs)}%', c["citation_mining"], slugs)}
          <div class="gate-label">Integrity gates</div>
          <div class="gates">{chip("evidence-verification", True)}{chip("discovery-provenance · unenforced", False)}</div>
        </div>
      </div>"""

    judgment_block = f"""      <div class="stage-block">
        <div class="sb-left"><div class="n">STAGE 3</div><div class="t">Judgment</div>
          <div class="entry">Entry: verified sources linked to an item × population cell.</div></div>
        <div class="sb-right">
{metric("Cells determined (of applicable pairs)", f'{j["cells"]} / {pairs} · {pct(j["cells"], pairs)}%', j["cells"], pairs)}
{metric("Items with any determination", f'{j["items_judged"]} / {items} · {pct(j["items_judged"], items)}%', j["items_judged"], items)}
{metric("State split", f'{j["stated"]} stated · {j["provisional"]} prov · {j["pending"]} pend')}
{metric("Determinations with governing_refs", f'{j["govrefs_ok"]} / {j["govrefs_denom"]} · {pct(j["govrefs_ok"], j["govrefs_denom"])}%', j["govrefs_ok"], j["govrefs_denom"])}
{metric("Convergence assessments · value extractions", f'{j["convergence"]} · {j["value_extractions"]} rows')}
          <div class="gate-label">Integrity gates</div>
          <div class="gates">{chip("governing-refs", True)}{chip("no-reg-stratum-stated", True)}{chip("tier3-alone-threshold", True)}{chip("derivation-handshake · unenforced", False)}{chip("convergence-independence · unenforced", False)}</div>
        </div>
      </div>"""

    synthesis_block = f"""      <div class="stage-block">
        <div class="sb-left"><div class="n">STAGE 4</div><div class="t">Synthesis</div>
          <div class="entry">Entry: a determination with a resolved value, ready for cross-jurisdictional synthesis.</div></div>
        <div class="sb-right">
{metric("Slugs with a reasoning doc + citations", f'{sy["reasoning_slugs"]} / {slugs} · {pct(sy["reasoning_slugs"], slugs)}%', sy["reasoning_slugs"], slugs)}
{metric("Verified reasoning-doc citations", f'{sy["reasoning_citations"]} rows')}
{metric("Live item-facing syntheses", f'{sy["live_item_synth"]} / {F["items_with_slug"]} · {pct(sy["live_item_synth"], F["items_with_slug"])}%', sy["live_item_synth"], F["items_with_slug"])}
{metric("Slugs in PARTIAL (non-item methodology)", f'{sy["partial_slugs"]}')}
          <div class="gate-label">Integrity gates</div>
          <div class="gates">{chip("nine-step-synthesis", True)}{chip("opus-routing · unenforced", False)}</div>
        </div>
      </div>"""

    render_block = f"""      <div class="stage-block">
        <div class="sb-left"><div class="n">STAGE 5</div><div class="t">Render</div>
          <div class="entry">Entry: determinations tagged with design_scale, ready to present.</div></div>
        <div class="sb-right">
{metric("Determinations render-ready (of matrix)", f'{rd["render_ready"]} / {pairs} · {pct(rd["render_ready"], pairs)}%', rd["render_ready"], pairs)}
{metric("Render-ready share of determinations made", f'{rd["render_ready"]} / {j["cells"]} · {pct(rd["render_ready"], j["cells"])}%', rd["render_ready"], j["cells"])}
{metric("Distinct design-scales in use", f'{rd["design_scales"]}')}
          <div class="gate-label">Integrity gates</div>
          <div class="gates">{chip("register-invariants", True)}{chip("matrix-consistency", True)}{chip("render-freshness · unenforced", False)}</div>
        </div>
      </div>"""

    # ---- category table ----
    cat_rows = ""
    for cat in F["categories"]:
        states = ", ".join(cat["states"]) or "—"
        cat_rows += f"""      <tr>
        <td class="code">{esc(cat["cat"])}</td>
        <td class="n">{cat["items"]}</td>
        <td class="n">{cat["with_slug"]}</td>
        <td><span class="state-badge">{esc(states)}</span></td>
        <td>{heat(cat["judged"], cat["items"])}</td>
        <td class="n">{cat["pop_breadth"]}</td>
      </tr>
"""

    # ---- population table ----
    pop_rows = ""
    for p in F["populations"]:
        cls = f'{esc(p["cls"])} · {esc(p["name"])}' if p["cls"] else esc(p["name"])
        pop_rows += f"""      <tr>
        <td class="code">{esc(p["code"])}</td>
        <td>{cls}</td>
        <td class="n">{p["applies"]}</td>
        <td class="n">{p["det"]}</td>
        <td>{heat(p["det"], p["applies"])}</td>
      </tr>
"""

    # ---- item frontier ----
    n_judged = F["judgment"]["items_judged"]
    cards = ""
    for fr in F["frontier"]:
        champ = " champ" if fr["synthesized"] else ""
        head_right = ('<span class="champ-tag">reached synthesis</span>' if fr["synthesized"]
                      else f'<span class="inm">{len(fr["cells"])} cell{"s" if len(fr["cells"]) != 1 else ""}</span>')
        pills = "".join(cellpill(cl["pop"], cl["state"]) for cl in fr["cells"])
        note = ('<div class="synth-note">Reached <b>synthesis</b>: linked to a reasoning doc with verified citations.</div>'
                if fr["synthesized"] else "")
        cards += f"""      <div class="item-card{champ}">
        <div class="ih"><span class="ic">{esc(fr["item"])}</span>{head_right}</div>
        <div class="cells">{pills}</div>{note}
      </div>
"""

    # zero-determination categories
    zero_cats = [c["cat"] for c in F["categories"] if c["judged"] == 0]
    zero_items = sum(c["items"] for c in F["categories"] if c["judged"] == 0)
    zero_line = (f'Categories <span class="mono">{", ".join(zero_cats)}</span> '
                 f'({zero_items} items) have <b>zero</b> determinations of any kind.'
                 if zero_cats else "Every category has at least one determination.")

    legend = (
        '<span class="li"><span class="sw b0-bg-solid"></span>none</span>'
        '<span class="li"><span class="sw b1-bg-solid"></span>&lt;15%</span>'
        '<span class="li"><span class="sw b2-bg-solid"></span>15–50%</span>'
        '<span class="li"><span class="sw b3-bg-solid"></span>50–85%</span>'
        '<span class="li"><span class="sw b4-bg-solid"></span>&gt;85%</span>')

    return f"""<div class="wrap">
  <header class="top">
    <div class="eyebrow">Accessible Built Environments Guidebook · Evidence Pipeline</div>
    <h1>Pipeline stage completeness</h1>
    <p class="lede">How far the corpus has actually moved through each of the five pipeline stages —
      <span class="mono">research → collection → judgment → synthesis → render</span> — measured against each
      stage's own denominator, then broken down by category, item, and population class.</p>
    <div class="meta-row">
      <span><b>Source</b> data/guidebook.db (read-only)</span>
      <span><b>Schema</b> user_version {F["user_version"]}</span>
      <span><b>Data as of</b> {esc(F["as_of"])}</span>
      <span><b>Auto-generated</b> tools/pipeline_completeness.py</span>
    </div>
  </header>

  <section>
    <div class="sec-head"><span class="sec-num">01</span><h2>The five stages at a glance</h2>
      <span class="sec-sub">content throughput — % of each stage's unit that has cleared it</span></div>
    <div class="gauges">
{chr(10).join(g)}
    </div>
    <div class="pattern"><b>The shape is front-loaded, then it collapses.</b> Sourcing (collection) is essentially
      finished — {c["verified"]}/{srcs} sources verified, metadata near-complete — but almost nothing has been
      <i>adjudicated</i> into determinations (judgment, {pct(j["cells"], pairs)}%) and only
      {sy["reasoning_slugs"]} parameter{"s" if sy["reasoning_slugs"] != 1 else ""} has a real synthesis reasoning
      doc (synthesis, {pct(sy["reasoning_slugs"], slugs)}%). Render faithfully mirrors that emptiness: it can only
      present the {rd["render_ready"]} determinations that exist. This is scaffolding with the shelves stocked but
      the book largely unwritten — consistent with the project's pre-launch, mid-rehabilitation state.</div>
  </section>

  <section>
    <div class="caveat">
      <h3><span class="dot"></span>Read the flags with care: the item-facing corpus is retracted, not finished</h3>
      Every one of the {F["items_with_slug"]} items that points at a BPC slug points at one whose
      <span class="mono">evidence_state = RETRACTED-PRE-REHAB</span>. Those slugs still carry a stale
      <span class="mono">bpc_complete = 1</span> flag from the pre-rehabilitation era — so a naïve flag count would
      report the BPC layer as largely "complete," when the honest current state is that
      <b>{sy["live_item_synth"]} item-facing syntheses are live</b>. The {sy["partial_slugs"]}
      <span class="mono">PARTIAL</span> slugs genuinely in progress are cross-cutting methodology/infrastructure
      units, none linked to a design parameter. The gauges above use current-state signals (reasoning docs,
      materialized cells), not the stale completion flags.
    </div>
  </section>

  <section>
    <div class="sec-head"><span class="sec-num">02</span><h2>Stage by stage</h2>
      <span class="sec-sub">throughput sub-metrics + which integrity gates are actually built</span></div>
    <div class="stage-detail">
{research_block}
{collection_block}
{judgment_block}
{synthesis_block}
{render_block}
    </div>
    <div class="pattern" style="background:var(--card);border-left-color:var(--accent)">
      <b>Governance gates are {ver_total}/{ver_total + inc_total} built.</b> The pipeline contract reports
      enforcement coverage per stage: {enf_line}. Every unenforced criterion is a <i>completeness</i>-kind one
      (provenance, convergence roots, Opus-routing, render-freshness) — the integrity gates are wired; the
      coverage gates are not.
    </div>
  </section>

  <section>
    <div class="sec-head"><span class="sec-num">03</span><h2>Breakdown by category</h2>
      <span class="sec-sub">{len(F["categories"])} item categories — {items} items total</span></div>
    <div class="tbl-scroll"><table>
      <thead><tr><th class="code">Cat</th><th class="n">Items</th><th class="n">With slug</th>
        <th>BPC synthesis state</th><th class="ratio-cell">Reached judgment</th><th class="n">Pop breadth</th></tr></thead>
      <tbody>
{cat_rows}      </tbody>
    </table></div>
    <div class="legend">{legend}
      <span class="li" style="margin-left:auto">Judgment coverage = items with ≥1 determination</span></div>
  </section>

  <section>
    <div class="sec-head"><span class="sec-num">04</span><h2>Breakdown by item — the frontier</h2>
      <span class="sec-sub">the {n_judged} of {items} items with a materialized determination; the other {items - n_judged} have none</span></div>
    <div class="frontier">
{cards}    </div>
    <div class="pattern">{zero_line}</div>
  </section>

  <section>
    <div class="sec-head"><span class="sec-num">05</span><h2>Breakdown by class (population)</h2>
      <span class="sec-sub">the disability-population axis — where determinations exist vs. where they're needed</span></div>
    <div class="tbl-scroll"><table>
      <thead><tr><th class="code">Pop</th><th>Class</th><th class="n">Applies to items</th>
        <th class="n">Determinations</th><th class="ratio-cell">Judgment coverage</th></tr></thead>
      <tbody>
{pop_rows}      </tbody>
    </table></div>
    <div class="equity"><b>Coverage tends to invert need.</b> The most broadly-relevant populations are often the
      least served — several axes that apply to dozens of items carry no determination yet. What determinations
      exist cluster on the handful of axes the early pilots happened to touch.</div>
  </section>

  <footer>
    <div class="two-col">
      <div><strong style="color:var(--ink-2)">How these numbers were derived</strong><br>
        Read-only queries against <code>data/guidebook.db</code> (<code>user_version {F["user_version"]}</code>,
        {F["migrations"]} data migrations). Denominators: research/synthesis over {slugs}
        <code>bpc_metadata</code> slugs; collection over {srcs} <code>evidence_sources</code>; judgment/render over
        {pairs} applicable item×population pairs (<code>item_population_links</code>). Determinations from
        <code>evidence_cell_state</code>; synthesis from <code>reasoning_doc_citations</code>; enforcement coverage
        from <code>governance/pipeline-contract.yaml</code>.</div>
      <div><strong style="color:var(--ink-2)">Two things to keep in mind</strong><br>
        (1) "Completeness" here means throughput, not correctness — a <code>stated</code> cell has cleared the gate,
        not been peer-reviewed. (2) <code>bpc_complete</code> and similar flags are <em>pre-rehabilitation</em>
        artifacts and overstate reality; current-state signals are used throughout. Auto-generated by
        <code>tools/pipeline_completeness.py</code>; do not hand-edit — the "as-of" date is the DB's own
        <code>max(updated_at)</code>, so identical data yields byte-identical output.</div>
    </div>
  </footer>
</div>"""


def render_html(F: dict, enf: dict, fmt: str = "full") -> str:
    body = render_body(F, enf)
    title = "Pipeline Completeness — Guidebook"
    if fmt == "fragment":
        # claude.ai Artifact body: title tag + style + content, no html/head/body wrapper.
        return f"<title>{title}</title>\n<style>{CSS}</style>\n{body}\n"
    return (f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>
""")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build(db_path: Path, fmt: str) -> str:
    with connect_ro(db_path) as con:
        F = gather(con)
    enf = gather_enforcement(CONTRACT)
    return render_html(F, enf, fmt)


def main() -> int:
    ap = argparse.ArgumentParser(description="Pipeline completeness dashboard generator.")
    ap.add_argument("--db", default=os.environ.get("GUIDEBOOK_DB_PATH", str(DEFAULT_DB)))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--format", choices=["full", "fragment"], default="full",
                    help="'full' standalone document (default) or 'fragment' for a claude.ai Artifact body")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the committed output is stale vs. the DB (writes nothing)")
    args = ap.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"error: DB not found at {db_path}", file=sys.stderr)
        return 2

    html_out = build(db_path, args.format)
    out_path = Path(args.out)

    if args.check:
        current = out_path.read_text(encoding="utf-8") if out_path.exists() else None
        if current == html_out:
            print(f"OK: {out_path.name} is current.")
            return 0
        print(f"STALE: {out_path.name} differs from a fresh regeneration. "
              f"Run: python3 tools/pipeline_completeness.py", file=sys.stderr)
        return 1

    out_path.write_text(html_out, encoding="utf-8")
    # Deterministic summary line (no wall-clock).
    with connect_ro(db_path) as con:
        F = gather(con)
    print(f"Wrote {out_path} — data as-of {F['as_of']} · "
          f"{F['judgment']['cells']}/{F['applicable_pairs']} cells determined · "
          f"{F['synthesis']['reasoning_slugs']}/{F['slugs_total']} slugs synthesized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
