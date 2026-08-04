#!/usr/bin/env python3
"""
scripts/generate/spec_page.py — Static page generator for item (specification)
pages.

Queries the LIVE schema (items, item_population_links, item_bpc_links,
bpc_metadata, evidence_cell_state) for a given item_code and produces a single
self-contained HTML file, following the same pattern as
tools/regenerate_vetting_surface.py.

Per decisions/DR-2026-07-12-website-architecture-lock.md item 4: there is no
canonical `specification` table (confirmed absent from data/guidebook.db;
architecture/page-templates.md's Specification Page template was written
against one that was never migrated). item_code is the real, FK-valid
parameter identity (per decisions/DR-2026-07-12-evidence-cell-state-schema-reconciliation.md
item 1) -- this generator queries `items`, not a `specification` table. This
is a rewrite of the previous version of this script, which queried the
non-existent `specification` table and failed on every invocation.

Usage:
    python3 scripts/generate/spec_page.py A-01
"""

import os
import sqlite3
import sys
from pathlib import Path
from html import escape

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO_ROOT / "data" / "guidebook.db"))
OUTPUT_DIR = REPO_ROOT / "site" / "specs"


def query_item(conn, item_code):
    row = conn.execute(
        "SELECT item_code, category, name, bpc_source_slug, status, "
        "pmp_delta_min, pmp_direction, pmp_last_walk_at, pmp_empirical_ceiling "
        "FROM items WHERE item_code = ?",
        (item_code,),
    ).fetchone()
    if not row:
        return None
    item = dict(zip(
        ["item_code", "category", "name", "bpc_source_slug", "status",
         "pmp_delta_min", "pmp_direction", "pmp_last_walk_at", "pmp_empirical_ceiling"], row,
    ))

    populations = conn.execute(
        "SELECT ipl.population_code, p.display_name, ipl.applicability "
        "FROM item_population_links ipl "
        "JOIN populations p ON p.population_code = ipl.population_code "
        "WHERE ipl.item_code = ? ORDER BY ipl.population_code",
        (item_code,),
    ).fetchall()
    item["populations"] = [
        {"code": r[0], "name": r[1], "applicability": r[2]} for r in populations
    ]

    # Governing BPC slugs: item_bpc_links is the intended many-to-many bridge
    # (migration 013) but is only sparsely populated today; bpc_source_slug is
    # the legacy single-string fallback still carried on most items. Report both.
    links = conn.execute(
        "SELECT slug, link_type, rationale FROM item_bpc_links WHERE item_code = ?",
        (item_code,),
    ).fetchall()
    item["bpc_links"] = [{"slug": r[0], "link_type": r[1], "rationale": r[2]} for r in links]

    cells = conn.execute(
        "SELECT cell_id, population_code, state, tier_basis, code_floor_only, "
        "falsification_condition, regulatory_stratum_only, confidence_synthesis_basis, "
        "has_unverified_sources, all_sources_disqualified "
        "FROM evidence_cell_state WHERE item_code = ? ORDER BY population_code",
        (item_code,),
    ).fetchall()
    item["cells"] = [
        {"cell_id": r[0], "population_code": r[1], "state": r[2], "tier_basis": r[3],
         "code_floor_only": r[4], "falsification_condition": r[5],
         "regulatory_stratum_only": r[6], "confidence_synthesis_basis": r[7],
         "has_unverified_sources": r[8], "all_sources_disqualified": r[9]}
        for r in cells
    ]

    # The governing sources behind each cell. Until migration 044 this edge
    # lived only as a JSON array in evidence_cell_state.governing_refs, which
    # this generator never read -- so every page it produced cited nothing at
    # all while presenting a confident determination. cell_source_links makes
    # it a join.
    for c in item["cells"]:
        rows = conn.execute(
            "SELECT csl.ref_id, e.author_display, e.author_display_note, e.pub_year, "
            "e.pub_title, e.tier, e.verification_status "
            "FROM cell_source_links csl "
            "JOIN evidence_sources e ON e.ref_id = csl.ref_id "
            "WHERE csl.cell_id = ? AND csl.role = 'governing' "
            "ORDER BY e.tier, e.pub_year, csl.ref_id",
            (c["cell_id"],),
        ).fetchall()
        c["sources"] = [
            {"ref_id": r[0], "author_display": r[1], "author_display_note": r[2],
             "pub_year": r[3], "pub_title": r[4], "tier": r[5],
             "verification_status": r[6]}
            for r in rows
        ]

    return item


def source_caveats(cell):
    """§2.8 source-quality flags, rendered plainly rather than silently dropped."""
    flags = []
    if cell["has_unverified_sources"]:
        flags.append("UNVERIFIED-1")
    if cell["all_sources_disqualified"]:
        flags.append("ALL-DISQUALIFIED")
    return ", ".join(flags) if flags else "—"


def citation(src):
    """One governing source, rendered as a citation a reader can chase.

    Deliberately does NOT compute an evidence marker (●/◐/○). Per
    governance/tier-system.md §5 a marker qualifies a *claim sentence*, not a
    source; deriving one per source here would manufacture a judgement the
    synthesis layer has not made. Tier and verification status are properties
    of the source itself, so those are what get shown.
    """
    e = escape
    author = src["author_display"] or src["author_display_note"] or "[author not recorded]"
    year = f' ({e(str(src["pub_year"]))})' if src["pub_year"] else ""
    title = e(src["pub_title"] or "[title not recorded]")
    tier = f'T{e(str(src["tier"]))}' if src["tier"] is not None else "tier not set"
    vs = src["verification_status"] or "UNVERIFIED"
    vs_cls = "ok" if vs == "VERIFIED" else "warn"
    return (f'<li><span class="ref">{e(src["ref_id"])}</span> '
            f'{e(author)}{year}. <em>{title}</em> '
            f'<span class="tier-badge">{tier}</span> '
            f'<span class="vs {vs_cls}">{e(vs)}</span></li>')


def render_html(item):
    e = escape
    code = e(item["item_code"])
    name = e(item["name"] or "")
    category = e(item["category"] or "")
    status = e(item["status"] or "")

    pop_rows = "".join(
        f'<tr><td><a href="/populations/{e(p["code"].lower())}.html">{e(p["code"])}</a></td>'
        f'<td>{e(p["name"])}</td><td>{e(p["applicability"] or "")}</td></tr>\n'
        for p in item["populations"]
    ) or '<tr><td colspan="3" class="empty">No populations linked to this item yet.</td></tr>'

    bpc_source = item["bpc_source_slug"]
    bpc_rows = "".join(
        f'<tr><td>{e(b["slug"])}</td><td>{e(b["link_type"] or "")}</td>'
        f'<td>{e(b["rationale"] or "")}</td></tr>\n'
        for b in item["bpc_links"]
    )
    if not bpc_rows and bpc_source:
        bpc_rows = (f'<tr><td>{e(bpc_source)}</td><td>legacy bpc_source_slug</td>'
                    f'<td class="empty">item_bpc_links (the intended many-to-many bridge, '
                    f'migration 013) has no row for this item yet — see '
                    f'decisions/DR-2026-07-12-evidence-cell-state-schema-reconciliation.md.</td></tr>')
    elif not bpc_rows:
        bpc_rows = '<tr><td colspan="3" class="empty">No governing BPC recorded for this item.</td></tr>'

    if item["pmp_last_walk_at"]:
        pmp = (f'<p>Progressive Measurement Probe last walked '
               f'{e(item["pmp_last_walk_at"])}: delta_min={e(str(item["pmp_delta_min"]))}, '
               f'direction={e(str(item["pmp_direction"]))}, '
               f'empirical_ceiling={e(str(item["pmp_empirical_ceiling"]))}.</p>')
    else:
        pmp = '<p class="empty">No Progressive Measurement Probe walk recorded for this item.</p>'

    if item["cells"]:
        cell_rows = "".join(
            f'<tr><td>{e(c["population_code"])}</td><td>{e(c["state"])}</td>'
            f'<td>{e(c["tier_basis"] or "—")}</td>'
            f'<td>{"yes" if c["code_floor_only"] else "no"}</td>'
            f'<td>{"yes" if c["regulatory_stratum_only"] else "no"}</td>'
            f'<td>{e(source_caveats(c))}</td>'
            f'<td>{e(c["confidence_synthesis_basis"] or "—")}</td>'
            f'<td>{e(c["falsification_condition"] or "—")}</td></tr>\n'
            for c in item["cells"]
        )
        src_blocks = []
        for c in item["cells"]:
            pop = e(c["population_code"])
            if c["sources"]:
                items_html = "\n".join(citation(s) for s in c["sources"])
                src_blocks.append(
                    f'<h3>{pop} — {len(c["sources"])} governing '
                    f'source{"s" if len(c["sources"]) != 1 else ""}</h3>\n'
                    f'<ul class="sources">{items_html}</ul>'
                )
            else:
                src_blocks.append(
                    f'<h3>{pop}</h3>\n<p class="honest-banner">This determination '
                    f'records <strong>no governing sources</strong>. A '
                    f'<code>{e(c["state"])}</code> cell with an empty source set '
                    f'cannot be checked by a reader — treat it as unevidenced '
                    f'until the omission is explained.</p>'
                )
        sources_section = "\n".join(src_blocks)

        bp_section = f"""<table>
            <thead><tr><th>Population</th><th>State</th><th>Tier basis</th>
            <th>Code floor only</th><th>Regulatory stratum only</th>
            <th>Source caveats</th><th>Confidence basis</th>
            <th>Falsification condition</th></tr></thead>
            <tbody>{cell_rows}</tbody>
        </table>
        <h2>Governing sources</h2>
        <p>Every source below governs the determination for its population.
        Walk the other direction — every specification a source justifies —
        through <code>cell_source_links</code>.</p>
        {sources_section}"""
    else:
        bp_section = ('<p class="honest-banner">Best-practice determination: '
                       '<strong>not yet computed</strong> for this item, for any population. '
                       'See workplan/best-practices-assessment-system.md.</p>')

    return f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{code} — {name}</title>
<style>
:root {{
    --ink: #1a1a2e; --paper: #fafaf8; --accent: #2d5f8a;
    --accent-light: #e8f0f7; --border: #d4d4d0; --muted: #6b6b6b;
    --font-body: Georgia, 'Times New Roman', serif;
    --font-ui: -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif;
    --font-mono: 'Courier New', Consolas, monospace;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: var(--font-body); color: var(--ink); background: var(--paper);
       line-height: 1.6; max-width: 860px; margin: 0 auto; padding: 24px; }}
.item-code {{ font-family: var(--font-mono); font-size: 14px; color: var(--accent);
              letter-spacing: 1px; text-transform: uppercase; }}
h1 {{ font-size: 26px; font-weight: 600; margin: 8px 0 4px; }}
.meta {{ font-family: var(--font-ui); font-size: 13px; color: var(--muted); margin-bottom: 20px; }}
section {{ margin: 28px 0; padding-bottom: 20px; border-bottom: 1px solid var(--border); }}
section:last-child {{ border-bottom: none; }}
h2 {{ font-family: var(--font-ui); font-size: 15px; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.5px; color: var(--muted); margin-bottom: 10px; }}
h3 {{ font-family: var(--font-ui); font-size: 13px; font-weight: 600; margin: 18px 0 6px;
      color: var(--ink); }}
ul.sources {{ list-style: none; font-size: 14px; }}
ul.sources li {{ padding: 6px 0 6px 12px; border-left: 2px solid var(--border);
                 margin-bottom: 6px; }}
ul.sources .ref {{ font-family: var(--font-mono); font-size: 12px; color: var(--accent); }}
.tier-badge {{ font-family: var(--font-ui); font-size: 11px; padding: 1px 5px;
               background: var(--accent-light); color: var(--accent); border-radius: 2px; }}
.vs {{ font-family: var(--font-ui); font-size: 11px; letter-spacing: 0.3px; }}
.vs.ok {{ color: #2e6b3e; }}
.vs.warn {{ color: #8a4b2d; font-weight: 600; }}
table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
th {{ font-family: var(--font-ui); font-size: 12px; text-transform: uppercase; text-align: left;
      padding: 6px 10px; background: var(--accent-light); color: var(--accent);
      border-bottom: 2px solid var(--border); }}
td {{ padding: 6px 10px; border-bottom: 1px solid var(--border); }}
td a {{ color: var(--accent); text-decoration: none; font-family: var(--font-mono); }}
.empty {{ color: var(--muted); font-style: italic; }}
.honest-banner {{ background: #fff8e1; border: 1px solid #ffe082; border-radius: 4px;
                   padding: 12px 16px; font-family: var(--font-ui); font-size: 14px; }}
</style>
</head>
<body>
<span class="item-code">{code}</span>
<h1>{name}</h1>
<p class="meta">category: {category} &middot; status: {status}</p>

<section>
<h2>Applicable populations ({len(item['populations'])})</h2>
<table>
<thead><tr><th>Code</th><th>Name</th><th>Applicability</th></tr></thead>
<tbody>{pop_rows}</tbody>
</table>
</section>

<section>
<h2>Governing Best Practice Compendium entries</h2>
<table>
<thead><tr><th>Slug</th><th>Link type</th><th>Rationale</th></tr></thead>
<tbody>{bpc_rows}</tbody>
</table>
</section>

<section>
<h2>Progressive Measurement Probe</h2>
{pmp}
</section>

<section>
<h2>Best-practice determinations</h2>
{bp_section}
</section>

</body>
</html>"""


def generate(item_code, output_path=None):
    conn = sqlite3.connect(str(DB_PATH))
    item = query_item(conn, item_code)
    conn.close()
    if not item:
        print(f"ERROR: Item '{item_code}' not found.", file=sys.stderr)
        sys.exit(1)
    html = render_html(item)
    if output_path is None:
        output_path = OUTPUT_DIR / f"{item_code.lower()}.html"
    os.makedirs(Path(output_path).parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated: {output_path} ({len(html)} bytes)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 spec_page.py <item_code>")
        sys.exit(1)
    item_code = sys.argv[1]
    output_path = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = Path(sys.argv[idx + 1])
    generate(item_code, output_path)


if __name__ == "__main__":
    main()
