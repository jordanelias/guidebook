#!/usr/bin/env python3
"""
scripts/generate/population_page.py — Static page generator for population pages.

Queries the LIVE schema (populations, item_population_links, items,
bpc_metadata, evidence_cell_state) and produces a single self-contained HTML
file for a given population code, following the same pattern as
tools/regenerate_vetting_surface.py: query real tables, inline data as JSON,
no framework, no server, no network dependency.

Per decisions/DR-2026-07-12-website-architecture-lock.md item 4:
architecture/navigation-modes.md's four-door UX concept and page-template
*concept* are the design language; architecture/page-templates.md's literal
SQL (queried against a `population`/`specification`/`room` schema that was
never migrated into the canonical DB) is NOT used -- this generator queries
the tables that actually exist. This is a rewrite of the previous version of
this script, which queried the non-existent `population`, `specification`,
and `conflict` tables and failed on every invocation.

Honesty requirement (workplan/website-v0-path-forward-2026-07-12.md): if
evidence_cell_state has no rows for this population, the page says so plainly
rather than omitting the section or implying a determination exists.

Usage:
    python3 scripts/generate/population_page.py MOB
"""

import os
import sqlite3
import sys
from pathlib import Path
from html import escape

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = REPO_ROOT / "data" / "guidebook.db"
OUTPUT_DIR = REPO_ROOT / "site" / "populations"


def query_population(conn, code):
    """Fetch all data for a population page from the real live schema."""
    row = conn.execute(
        "SELECT population_code, display_name, category, description, "
        "parent_code, is_compound, status FROM populations WHERE population_code = ?",
        (code,),
    ).fetchone()
    if not row:
        return None
    pop = dict(zip(
        ["population_code", "display_name", "category", "description",
         "parent_code", "is_compound", "status"], row,
    ))

    items = conn.execute(
        "SELECT ipl.item_code, i.name, i.category, ipl.applicability, ipl.subtype "
        "FROM item_population_links ipl "
        "JOIN items i ON i.item_code = ipl.item_code "
        "WHERE ipl.population_code = ? ORDER BY i.item_code",
        (code,),
    ).fetchall()
    pop["items"] = [
        {"item_code": r[0], "name": r[1], "category": r[2], "applicability": r[3], "subtype": r[4]}
        for r in items
    ]

    bpcs = conn.execute(
        "SELECT slug, evidence_state, bpc_complete, last_updated "
        "FROM bpc_metadata WHERE population = ? ORDER BY slug",
        (code,),
    ).fetchall()
    pop["bpcs"] = [
        {"slug": r[0], "evidence_state": r[1], "bpc_complete": r[2], "last_updated": r[3]}
        for r in bpcs
    ]

    cells = conn.execute(
        "SELECT item_code, state, tier_basis, code_floor_only "
        "FROM evidence_cell_state WHERE population_code = ? ORDER BY item_code",
        (code,),
    ).fetchall()
    pop["cells"] = [
        {"item_code": r[0], "state": r[1], "tier_basis": r[2], "code_floor_only": r[3]}
        for r in cells
    ]

    return pop


def render_html(pop):
    e = escape
    code = e(pop["population_code"])
    label = e(pop["display_name"])
    category = e(pop["category"] or "")
    description = e(pop["description"] or "")
    status = e(pop["status"] or "")

    item_rows = "".join(
        f'<tr><td><a href="/specs/{e(it["item_code"].lower())}.html">{e(it["item_code"])}</a></td>'
        f'<td>{e(it["name"])}</td><td>{e(it["category"] or "")}</td>'
        f'<td>{e(it["applicability"] or "")}</td></tr>\n'
        for it in pop["items"]
    ) or '<tr><td colspan="4" class="empty">No items linked to this population yet.</td></tr>'

    def bpc_badge(state):
        if state == "RETRACTED-PRE-REHAB":
            return '<span class="badge badge-retracted">RETRACTED — pending reverification</span>'
        if state is None:
            return '<span class="badge badge-unknown">no evidence_state recorded</span>'
        return f'<span class="badge">{e(state)}</span>'

    bpc_rows = "".join(
        f'<tr><td>{e(b["slug"])}</td><td>{bpc_badge(b["evidence_state"])}</td>'
        f'<td>{"yes" if b["bpc_complete"] else "no"}</td></tr>\n'
        for b in pop["bpcs"]
    ) or '<tr><td colspan="3" class="empty">No BPC entries recorded for this population.</td></tr>'

    if pop["cells"]:
        cell_rows = "".join(
            f'<tr><td>{e(c["item_code"])}</td><td>{e(c["state"])}</td>'
            f'<td>{e(c["tier_basis"] or "—")}</td>'
            f'<td>{"yes" if c["code_floor_only"] else "no"}</td></tr>\n'
            for c in pop["cells"]
        )
        bp_section = f"""<table>
            <thead><tr><th>Item</th><th>State</th><th>Tier basis</th><th>Code floor only</th></tr></thead>
            <tbody>{cell_rows}</tbody>
        </table>"""
    else:
        bp_section = ('<p class="honest-banner">Best-practice determination: '
                       '<strong>not yet computed</strong> for any item × this population. '
                       'The evidence_cell_state table exists but is empty pending the Phase E '
                       'evidence re-synthesis and best-practice engine build '
                       '(see workplan/best-practices-assessment-system.md). '
                       'This is not a data-loading bug — see the gap register for tracked status.</p>')

    return f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{code} — {label}</title>
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
.pop-code {{ font-family: var(--font-mono); font-size: 14px; color: var(--accent);
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
.badge {{ font-family: var(--font-ui); font-size: 12px; padding: 2px 8px; border-radius: 3px;
          background: var(--accent-light); color: var(--accent); }}
.badge-retracted {{ background: #fce4ec; color: #c62828; }}
.badge-unknown {{ background: #f5f5f5; color: var(--muted); }}
.honest-banner {{ background: #fff8e1; border: 1px solid #ffe082; border-radius: 4px;
                   padding: 12px 16px; font-family: var(--font-ui); font-size: 14px; }}
</style>
</head>
<body>
<span class="pop-code">{code}</span>
<h1>{label}</h1>
<p class="meta">{category} &middot; status: {status}</p>

<section>
<h2>Description</h2>
<p>{description or '<span class="empty">No description recorded.</span>'}</p>
</section>

<section>
<h2>Applicable items ({len(pop['items'])})</h2>
<table>
<thead><tr><th>Item</th><th>Name</th><th>Category</th><th>Applicability</th></tr></thead>
<tbody>{item_rows}</tbody>
</table>
</section>

<section>
<h2>Best Practice Compendium entries ({len(pop['bpcs'])})</h2>
<table>
<thead><tr><th>Slug</th><th>Evidence state</th><th>BPC complete</th></tr></thead>
<tbody>{bpc_rows}</tbody>
</table>
</section>

<section>
<h2>Best-practice determinations</h2>
{bp_section}
</section>

</body>
</html>"""


def generate(code, output_path=None):
    conn = sqlite3.connect(str(DB_PATH))
    pop = query_population(conn, code)
    conn.close()
    if not pop:
        print(f"ERROR: Population '{code}' not found.", file=sys.stderr)
        sys.exit(1)
    html = render_html(pop)
    if output_path is None:
        output_path = OUTPUT_DIR / f"{code.lower()}.html"
    os.makedirs(Path(output_path).parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated: {output_path} ({len(html)} bytes)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 population_page.py <code>")
        sys.exit(1)
    code = sys.argv[1]
    output_path = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = Path(sys.argv[idx + 1])
    generate(code, output_path)


if __name__ == "__main__":
    main()
