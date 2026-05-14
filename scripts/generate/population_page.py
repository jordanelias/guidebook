#!/usr/bin/env python3
"""
scripts/generate/population_page.py — Static page generator for population pages.

Queries SQLite and produces a self-contained HTML file for a given
population code. Per page-templates.md Template 2.

Usage:
    python3 scripts/generate/population_page.py MOB
"""

import json
import os
import sqlite3
import sys
from pathlib import Path
from html import escape

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = REPO_ROOT / "data" / "guidebook.db"
OUTPUT_DIR = REPO_ROOT / "site" / "populations"


def query_population(conn, code):
    """Fetch all data for a population page."""
    pop = conn.execute("SELECT * FROM population WHERE code = ?", (code,)).fetchone()
    if not pop:
        return None
    cols = [d[0] for d in conn.execute("SELECT * FROM population LIMIT 0").description]
    pop_dict = dict(zip(cols, pop))

    # Specifications
    specs = conn.execute(
        "SELECT sp.role, s.item_code, s.title, s.parameter, s.evidence_tier "
        "FROM specification_population sp "
        "JOIN specification s ON sp.spec_id = s.spec_id "
        "WHERE sp.population_code = ? ORDER BY sp.role, s.item_code",
        (code,),
    ).fetchall()
    pop_dict["specifications"] = [
        {"role": s[0], "item_code": s[1], "title": s[2], "parameter": s[3], "tier": s[4]}
        for s in specs
    ]

    # Conflicts
    conflicts = conn.execute(
        "SELECT DISTINCT c.conflict_id, c.conflict_label, c.resolution_status "
        "FROM conflict c WHERE c.conflict_id IN ("
        "  SELECT conflict_id FROM conflict WHERE "
        "  population_a LIKE '%' || ? || '%' OR population_b LIKE '%' || ? || '%'"
        ")", (code, code),
    ).fetchall()
    pop_dict["conflicts"] = [
        {"id": c[0], "label": c[1], "status": c[2]} for c in conflicts
    ]

    return pop_dict


def render_html(pop):
    """Render population page as HTML."""
    e = escape
    code = e(pop["code"])
    label = e(pop["label"])
    profile = e(pop.get("functional_profile") or "")
    co1 = pop.get("co1_status") or "—"
    confidence = pop.get("evidence_confidence") or "—"

    # Specification rows (primary then secondary)
    primary_specs = [s for s in pop["specifications"] if s["role"] == "primary"]
    secondary_specs = [s for s in pop["specifications"] if s["role"] == "secondary"]

    def spec_rows(specs, role_class):
        rows = ""
        for s in specs:
            tier = s["tier"]
            if isinstance(tier, str):
                import re as _re
                m = _re.search(r'(\d+)', str(tier))
                tier = int(m.group(1)) if m else None
            tier_marker = "●" if tier and tier <= 3 else "◐" if tier and tier <= 5 else "○"
            rows += f'<tr class="{role_class}"><td><a href="/specs/{e(s["item_code"])}">{e(s["item_code"])}</a></td><td>{e(s["title"])}</td><td>{tier_marker}</td></tr>\n'
        return rows

    primary_html = spec_rows(primary_specs, "role-primary")
    secondary_html = spec_rows(secondary_specs, "role-secondary")

    # Conflict cards
    conflict_html = ""
    if pop["conflicts"]:
        cards = "".join(
            f'<a href="/conflicts/{e(c["id"])}" class="conflict-card">{e(c["label"] or c["id"])}</a>'
            for c in pop["conflicts"]
        )
        conflict_html = f'<div class="conflict-domains">{cards}</div>'

    # Co-1 badge
    co1_class = "co1-complete" if co1 == "COMPLETE" else "co1-partial" if co1 == "PARTIAL" else "co1-gap"
    co1_gap = e(pop.get("co1_gap_note") or "")

    html = f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{code} — {label}</title>
    <style>
        :root {{
            --ink: #1a1a2e; --paper: #fafaf8; --accent: #2d5f8a;
            --accent-light: #e8f0f7; --border: #d4d4d0; --muted: #6b6b6b;
            --primary-bg: #e8f5e9; --secondary-bg: #f5f5f5;
            --font-body: 'Source Serif 4', Georgia, serif;
            --font-ui: 'DM Sans', 'Helvetica Neue', sans-serif;
            --font-mono: 'JetBrains Mono', Consolas, monospace;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: var(--font-body); color: var(--ink); background: var(--paper);
               line-height: 1.65; max-width: 860px; margin: 0 auto; padding: 24px; }}

        .pop-header {{ margin-bottom: 32px; }}
        .pop-code {{ font-family: var(--font-mono); font-size: 14px; color: var(--accent);
                     letter-spacing: 1px; text-transform: uppercase; }}
        h1 {{ font-size: 28px; font-weight: 600; margin: 8px 0; }}
        .confidence-badge {{ font-family: var(--font-ui); font-size: 13px; padding: 4px 10px;
                            border-radius: 4px; background: var(--accent-light); color: var(--accent); }}

        section {{ margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid var(--border); }}
        section:last-child {{ border-bottom: none; }}
        h2 {{ font-family: var(--font-ui); font-size: 16px; font-weight: 600;
              text-transform: uppercase; letter-spacing: 0.5px; color: var(--muted); margin-bottom: 12px; }}

        .profile-text {{ font-size: 16px; line-height: 1.75; }}

        table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
        th {{ font-family: var(--font-ui); font-size: 12px; text-transform: uppercase;
              letter-spacing: 0.5px; text-align: left; padding: 8px 12px;
              background: var(--accent-light); color: var(--accent); border-bottom: 2px solid var(--border); }}
        td {{ padding: 8px 12px; border-bottom: 1px solid var(--border); }}
        td a {{ color: var(--accent); text-decoration: none; font-family: var(--font-mono); }}
        td a:hover {{ text-decoration: underline; }}

        .role-primary {{ background: var(--primary-bg); }}
        .role-secondary {{ opacity: 0.7; }}

        .conflict-domains {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .conflict-card {{ font-family: var(--font-ui); font-size: 13px; padding: 6px 14px;
                         border-radius: 4px; background: #fff3e0; color: #e65100;
                         border: 1px solid #ffe0b2; text-decoration: none; }}

        .co1-section {{ display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }}
        .co1-badge {{ font-family: var(--font-ui); font-size: 13px; padding: 4px 12px;
                     border-radius: 4px; font-weight: 600; }}
        .co1-complete {{ background: #e8f5e9; color: #2e7d32; }}
        .co1-partial {{ background: #fff3e0; color: #e65100; }}
        .co1-gap {{ background: #fce4ec; color: #c62828; }}

        .section-label {{ font-family: var(--font-ui); font-size: 13px; color: var(--muted);
                         margin-bottom: 8px; }}

        @media (max-width: 640px) {{ body {{ padding: 16px; }} h1 {{ font-size: 22px; }} }}
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
</head>
<body>

<header class="pop-header">
    <span class="pop-code">{code}</span>
    <h1>{label}</h1>
    <span class="confidence-badge">Evidence confidence: {e(confidence)}</span>
</header>

<section>
    <h2>Functional Profile</h2>
    <p class="profile-text">{profile}</p>
</section>

<section>
    <h2>Specification Matrix</h2>
    <p class="section-label">Primary specifications highlighted; secondary specifications dimmed.</p>
    <table>
        <thead><tr><th>Code</th><th>Specification</th><th>Evidence</th></tr></thead>
        <tbody>
            {primary_html}
            {secondary_html}
        </tbody>
    </table>
</section>

<section>
    <h2>Co-1 (Lived Experience) Evidence</h2>
    <div class="co1-section">
        <span class="co1-badge {co1_class}">Co-1: {e(co1)}</span>
        {'<span>' + co1_gap + '</span>' if co1_gap else ''}
    </div>
</section>

<section>
    <h2>Conflict Involvement</h2>
    {conflict_html or '<p style="color:var(--muted)">No cross-population conflicts involving this population in current data.</p>'}
</section>

</body>
</html>"""

    return html


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
