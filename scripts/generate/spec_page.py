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
DB_PATH = REPO_ROOT / "data" / "guidebook.db"
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
        "SELECT population_code, state, tier_basis, code_floor_only, falsification_condition "
        "FROM evidence_cell_state WHERE item_code = ? ORDER BY population_code",
        (item_code,),
    ).fetchall()
    item["cells"] = [
        {"population_code": r[0], "state": r[1], "tier_basis": r[2],
         "code_floor_only": r[3], "falsification_condition": r[4]}
        for r in cells
    ]

    return item


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
            f'<td>{e(c["falsification_condition"] or "—")}</td></tr>\n'
            for c in item["cells"]
        )
        bp_section = f"""<table>
            <thead><tr><th>Population</th><th>State</th><th>Tier basis</th>
            <th>Code floor only</th><th>Falsification condition</th></tr></thead>
            <tbody>{cell_rows}</tbody>
        </table>"""
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
