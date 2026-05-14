#!/usr/bin/env python3
"""
scripts/generate/room_page.py — Static page generator for room pages.

Queries SQLite and produces a self-contained HTML file for a given
room_id. Per page-templates.md Template 3.

Usage:
    python3 scripts/generate/room_page.py R-BA
"""

import json
import os
import sqlite3
import sys
from pathlib import Path
from html import escape

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = REPO_ROOT / "data" / "guidebook.db"
OUTPUT_DIR = REPO_ROOT / "site" / "rooms"


def query_room(conn, room_id):
    """Fetch all data for a room page."""
    room = conn.execute("SELECT * FROM room WHERE room_id = ?", (room_id,)).fetchone()
    if not room:
        return None
    cols = [d[0] for d in conn.execute("SELECT * FROM room LIMIT 0").description]
    room_dict = dict(zip(cols, room))

    # Item matrix with population applicability
    items = conn.execute(
        "SELECT ri.item_code, ri.design_stage, ri.must_appear_on, ri.notes "
        "FROM room_item ri WHERE ri.room_id = ? ORDER BY ri.item_code",
        (room_id,),
    ).fetchall()

    item_list = []
    for item in items:
        code = item[0]
        # Get population applicability for this item in this room
        pops = conn.execute(
            "SELECT population_code, applicability FROM room_item_population "
            "WHERE room_id = ? AND item_code = ?", (room_id, code),
        ).fetchall()
        pop_map = {p[0]: p[1] for p in pops}

        # Get spec title
        spec = conn.execute(
            "SELECT title FROM specification WHERE item_code = ?", (code,)
        ).fetchone()
        title = spec[0] if spec else code

        item_list.append({
            "item_code": code,
            "title": title,
            "design_stage": item[1],
            "must_appear_on": item[2],
            "populations": pop_map,
        })
    room_dict["items"] = item_list

    # DAR provisions
    dar = conn.execute(
        "SELECT description, construction_stage, drawing_reference FROM room_dar_provision WHERE room_id = ?",
        (room_id,),
    ).fetchall()
    room_dict["dar_provisions"] = [
        {"description": d[0], "stage": d[1], "drawing": d[2]} for d in dar
    ]

    # Conflicts
    conflicts = conn.execute(
        "SELECT description, resolution, conflict_domain FROM room_conflict WHERE room_id = ?",
        (room_id,),
    ).fetchall()
    room_dict["conflicts"] = [
        {"description": c[0], "resolution": c[1], "domain": c[2]} for c in conflicts
    ]

    # All population codes appearing in this room's items
    all_pops = conn.execute(
        "SELECT DISTINCT population_code FROM room_item_population WHERE room_id = ? ORDER BY population_code",
        (room_id,),
    ).fetchall()
    room_dict["all_populations"] = [p[0] for p in all_pops]

    return room_dict


def render_html(room):
    """Render room page as HTML."""
    e = escape
    rid = e(room["room_id"])
    label = e(room["room_label"])
    btype = e(room["building_type"]).title()
    density = e(room.get("evidence_density") or "")
    crit = e(room.get("criticality_note") or "")
    all_pops = room["all_populations"]

    # Item matrix header
    pop_headers = "".join(f'<th class="pop-col">{e(p)}</th>' for p in all_pops)

    # Item matrix rows grouped by design stage
    stages = {"SD": [], "DD": [], "CD": [], "RFO": []}
    for item in room["items"]:
        stage = item.get("design_stage") or "—"
        stages.setdefault(stage, []).append(item)

    matrix_rows = ""
    for stage in ["SD", "DD", "CD", "RFO"]:
        items = stages.get(stage, [])
        if not items:
            continue
        matrix_rows += f'<tr class="stage-header"><td colspan="{3 + len(all_pops)}">{e(stage)}</td></tr>\n'
        for item in items:
            pop_cells = ""
            for p in all_pops:
                app = item["populations"].get(p)
                if app == "primary":
                    pop_cells += '<td class="app-primary">●</td>'
                elif app == "secondary":
                    pop_cells += '<td class="app-secondary">◐</td>'
                else:
                    pop_cells += '<td class="app-none">·</td>'
            matrix_rows += (
                f'<tr><td><a href="/specs/{e(item["item_code"])}">{e(item["item_code"])}</a></td>'
                f'<td>{e(item["title"])}</td>'
                f'<td class="drawing-ref">{e(item.get("must_appear_on") or "")}</td>'
                f'{pop_cells}</tr>\n'
            )

    # DAR provisions
    dar_rows = ""
    for d in room["dar_provisions"]:
        dar_rows += f'<tr><td>{e(d["description"])}</td><td>{e(d.get("stage") or "")}</td><td>{e(d.get("drawing") or "")}</td></tr>\n'

    # Conflict register
    conflict_rows = ""
    for c in room["conflicts"]:
        domain_link = f'<a href="/conflicts/{e(c["domain"])}">{e(c["domain"])}</a>' if c.get("domain") else "—"
        conflict_rows += f'<tr><td>{e(c["description"])}</td><td>{e(c.get("resolution") or "")}</td><td>{domain_link}</td></tr>\n'

    html = f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{rid} — {label}</title>
    <style>
        :root {{
            --ink: #1a1a2e; --paper: #fafaf8; --accent: #2d5f8a;
            --accent-light: #e8f0f7; --border: #d4d4d0; --muted: #6b6b6b;
            --font-body: 'Source Serif 4', Georgia, serif;
            --font-ui: 'DM Sans', 'Helvetica Neue', sans-serif;
            --font-mono: 'JetBrains Mono', Consolas, monospace;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: var(--font-body); color: var(--ink); background: var(--paper);
               line-height: 1.65; max-width: 960px; margin: 0 auto; padding: 24px; }}

        .room-header {{ margin-bottom: 32px; }}
        .room-id {{ font-family: var(--font-mono); font-size: 14px; color: var(--accent); letter-spacing: 1px; }}
        h1 {{ font-size: 28px; font-weight: 600; margin: 8px 0; }}
        .room-meta {{ display: flex; gap: 12px; flex-wrap: wrap; }}
        .meta-tag {{ font-family: var(--font-ui); font-size: 13px; padding: 4px 10px;
                    border-radius: 4px; background: var(--accent-light); color: var(--accent); }}

        section {{ margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid var(--border); }}
        section:last-child {{ border-bottom: none; }}
        h2 {{ font-family: var(--font-ui); font-size: 16px; font-weight: 600;
              text-transform: uppercase; letter-spacing: 0.5px; color: var(--muted); margin-bottom: 12px; }}

        .crit-note {{ font-size: 15px; line-height: 1.7; padding: 12px 16px;
                     background: #fff8e1; border-left: 4px solid #ffc107; margin-bottom: 16px; }}

        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        th {{ font-family: var(--font-ui); font-size: 11px; text-transform: uppercase;
              letter-spacing: 0.5px; text-align: left; padding: 6px 10px;
              background: var(--accent-light); color: var(--accent); border-bottom: 2px solid var(--border); }}
        td {{ padding: 6px 10px; border-bottom: 1px solid var(--border); vertical-align: top; }}
        td a {{ color: var(--accent); text-decoration: none; font-family: var(--font-mono); }}

        .stage-header td {{ font-family: var(--font-ui); font-weight: 600; font-size: 12px;
                           background: #f0f0f0; color: var(--muted); text-transform: uppercase;
                           letter-spacing: 1px; padding: 8px 10px; }}

        .pop-col {{ text-align: center; min-width: 48px; }}
        .app-primary {{ text-align: center; color: #2e7d32; font-weight: bold; }}
        .app-secondary {{ text-align: center; color: #1565c0; }}
        .app-none {{ text-align: center; color: #e0e0e0; }}
        .drawing-ref {{ font-family: var(--font-ui); font-size: 12px; color: var(--muted); }}

        .dar-section table {{ background: #e8f5e9; }}
        .dar-section th {{ background: #c8e6c9; color: #2e7d32; }}

        @media (max-width: 640px) {{
            body {{ padding: 16px; }}
            h1 {{ font-size: 22px; }}
            table {{ font-size: 12px; }}
            .pop-col {{ min-width: 36px; }}
        }}
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
</head>
<body>

<header class="room-header">
    <span class="room-id">{rid}</span>
    <h1>{label}</h1>
    <div class="room-meta">
        <span class="meta-tag">{btype}</span>
        <span class="meta-tag">{density}</span>
    </div>
</header>

<section>
    <p class="crit-note">{crit}</p>
</section>

<section>
    <h2>Item Application Matrix</h2>
    <table>
        <thead><tr><th>Code</th><th>Specification</th><th>Drawing</th>{pop_headers}</tr></thead>
        <tbody>{matrix_rows}</tbody>
    </table>
</section>

<section class="dar-section">
    <h2>DAR Provisions</h2>
    <table>
        <thead><tr><th>Provision</th><th>Stage</th><th>Drawing</th></tr></thead>
        <tbody>{dar_rows}</tbody>
    </table>
</section>

<section>
    <h2>Conflict Register</h2>
    <table>
        <thead><tr><th>Conflict</th><th>Resolution</th><th>Domain</th></tr></thead>
        <tbody>{conflict_rows}</tbody>
    </table>
</section>

</body>
</html>"""

    return html


def generate(room_id, output_path=None):
    conn = sqlite3.connect(str(DB_PATH))
    room = query_room(conn, room_id)
    conn.close()
    if not room:
        print(f"ERROR: Room '{room_id}' not found.", file=sys.stderr)
        sys.exit(1)
    html = render_html(room)
    if output_path is None:
        output_path = OUTPUT_DIR / f"{room_id.lower().replace('-', '_')}.html"
    os.makedirs(Path(output_path).parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated: {output_path} ({len(html)} bytes)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 room_page.py <room_id>")
        sys.exit(1)
    room_id = sys.argv[1]
    output_path = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = Path(sys.argv[idx + 1])
    generate(room_id, output_path)


if __name__ == "__main__":
    main()
