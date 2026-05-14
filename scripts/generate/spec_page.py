#!/usr/bin/env python3
"""
scripts/generate/spec_page.py — Static page generator for specification pages.

Queries SQLite database and produces a self-contained HTML file
for a given item_code. Supports both spec mode and question mode
via CSS toggle (no server round-trip).

Per page-templates.md Template 1.

Usage:
    python3 scripts/generate/spec_page.py E-08
    python3 scripts/generate/spec_page.py E-08 --output /tmp/e08.html
"""

import json
import os
import sqlite3
import sys
from pathlib import Path
from html import escape

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = REPO_ROOT / "data" / "guidebook.db"
OUTPUT_DIR = REPO_ROOT / "site" / "specs"


def query_spec(conn, item_code):
    """Fetch all data for a specification page."""
    # Main spec record
    spec = conn.execute(
        "SELECT * FROM specification WHERE item_code = ?", (item_code,)
    ).fetchone()
    if not spec:
        return None

    cols = [d[0] for d in conn.execute("SELECT * FROM specification LIMIT 0").description]
    spec_dict = dict(zip(cols, spec))

    # Measurements
    meas = conn.execute(
        "SELECT * FROM measurement WHERE spec_id = ? ORDER BY CASE design_mode "
        "WHEN 'universal' THEN 1 WHEN 'population_based' THEN 2 WHEN 'person_specific' THEN 3 END, population_code",
        (spec_dict["spec_id"],),
    ).fetchall()
    m_cols = [d[0] for d in conn.execute("SELECT * FROM measurement LIMIT 0").description]
    spec_dict["measurements"] = [dict(zip(m_cols, m)) for m in meas]

    # Populations
    pops = conn.execute(
        "SELECT sp.population_code, sp.role, p.label FROM specification_population sp "
        "JOIN population p ON sp.population_code = p.code "
        "WHERE sp.spec_id = ? ORDER BY sp.role, sp.population_code",
        (spec_dict["spec_id"],),
    ).fetchall()
    spec_dict["populations"] = [{"code": p[0], "role": p[1], "label": p[2]} for p in pops]

    # Jurisdictional values
    jvs = conn.execute(
        "SELECT * FROM jurisdictional_value WHERE spec_id = ? ORDER BY jurisdiction",
        (spec_dict["spec_id"],),
    ).fetchall()
    jv_cols = [d[0] for d in conn.execute("SELECT * FROM jurisdictional_value LIMIT 0").description]
    spec_dict["jurisdictions"] = [dict(zip(jv_cols, jv)) for jv in jvs]

    # Performance criteria
    criteria = conn.execute(
        "SELECT * FROM performance_criterion WHERE spec_id = ?",
        (spec_dict["spec_id"],),
    ).fetchall()
    pc_cols = [d[0] for d in conn.execute("SELECT * FROM performance_criterion LIMIT 0").description]
    spec_dict["criteria"] = [dict(zip(pc_cols, c)) for c in criteria]

    # Evidence sources
    sources = conn.execute(
        "SELECT es.*, ss.role AS source_role FROM evidence_source es "
        "JOIN specification_source ss ON es.ref_id = ss.ref_id "
        "WHERE ss.spec_id = ? ORDER BY ss.role DESC, es.year",
        (spec_dict["spec_id"],),
    ).fetchall()
    es_cols = [d[0] for d in conn.execute(
        "SELECT es.*, ss.role AS source_role FROM evidence_source es "
        "JOIN specification_source ss ON es.ref_id = ss.ref_id LIMIT 0"
    ).description]
    spec_dict["sources"] = [dict(zip(es_cols, s)) for s in sources]

    # Connections
    conns = conn.execute(
        "SELECT * FROM connection_endpoint WHERE spec_id = ?",
        (spec_dict["spec_id"],),
    ).fetchall()
    ce_cols = [d[0] for d in conn.execute("SELECT * FROM connection_endpoint LIMIT 0").description]
    spec_dict["connections"] = [dict(zip(ce_cols, c)) for c in conns]

    return spec_dict


def evidence_marker(tier):
    """Return evidence marker symbol."""
    if isinstance(tier, str):
        import re as _re
        m = _re.search(r'(\d+)', str(tier))
        tier = int(m.group(1)) if m else None
    if tier and tier <= 3:
        return "●"  # stated
    elif tier and tier <= 5:
        return "◐"  # provisional
    return "○"  # pending


def render_html(spec):
    """Render specification page as HTML."""
    e = escape
    item = e(spec["item_code"])
    title = e(spec["title"])
    question = e(spec.get("question_heading") or title)
    marker = evidence_marker(spec.get("evidence_tier"))
    tier = spec.get("evidence_tier") or "—"

    # Measurements by mode
    universal_meas = [m for m in spec["measurements"] if m["design_mode"] == "universal"]
    pop_meas = [m for m in spec["measurements"] if m["design_mode"] == "population_based"]
    ps_meas = [m for m in spec["measurements"] if m["design_mode"] == "person_specific"]

    # Build measurement rows
    meas_rows = ""
    if universal_meas:
        m = universal_meas[0]
        meas_rows += f'<tr class="mode-universal"><td>Universal Mode</td><td>—</td><td>{e(m["unit_display"] or "")}</td><td>{e(m["notes"] or "")}</td></tr>\n'
    for m in pop_meas:
        pop_label = e(m["population_code"] or "ALL")
        meas_rows += f'<tr class="mode-population"><td>Mode P</td><td>{pop_label}</td><td>{e(m["unit_display"] or "")}</td><td>{e(m["notes"] or "")}</td></tr>\n'
    if ps_meas:
        m = ps_meas[0]
        meas_rows += f'<tr class="mode-person"><td>Mode S</td><td>—</td><td>{e(m["unit_display"] or "")}</td><td>{e(m["notes"] or "")}</td></tr>\n'

    # Population badges
    pop_badges = ""
    for p in spec["populations"]:
        opacity = "1.0" if p["role"] == "primary" else "0.5"
        role_label = "Primary" if p["role"] == "primary" else "Secondary"
        pop_badges += f'<span class="pop-badge" style="opacity:{opacity}" title="{role_label}">{e(p["code"])}</span>\n'

    # Jurisdiction rows
    jur_rows = ""
    for jv in spec["jurisdictions"]:
        jur_rows += f'<tr><td>{e(jv["jurisdiction"])}</td><td>{e(jv["standard_name"] or "")}</td><td>{e(jv["clause_ref"] or "")}</td><td>{e(jv["value_text"] or "")}</td><td>{e(jv["notes"] or "")}</td></tr>\n'

    # Conflict domains
    conflict_html = ""
    domains = json.loads(spec.get("conflict_domains") or "[]") if spec.get("conflict_domains") else []
    if domains:
        cards = "".join(f'<a href="/conflicts/{e(d)}" class="conflict-card">{e(d)}</a>' for d in domains)
        conflict_html = f'<div class="conflict-domains">{cards}</div>'

    # Evidence sources
    source_rows = ""
    for s in spec["sources"]:
        role_badge = "★" if s["source_role"] == "primary" else ""
        doi_link = f' <a href="https://doi.org/{e(s["doi"])}" target="_blank">DOI</a>' if s.get("doi") else ""
        url_link = f' <a href="{e(s["url"])}" target="_blank">Link</a>' if s.get("url") and not s.get("doi") else ""
        source_rows += f'<tr><td>{role_badge} {e(s["ref_id"])}</td><td>{e(s["authors"] or "")}</td><td>{s.get("year") or ""}</td><td>{e(s["title"])}{doi_link}{url_link}</td><td>{marker}</td></tr>\n'

    # Cross-references
    xref_links = ""
    for c in spec["connections"]:
        target = e(c["target_item_code"] or "")
        desc = e(c["description"] or "")
        xref_links += f'<a href="/specs/{target}" class="xref-link" title="{desc}">{target}</a>\n'

    # Performance criteria
    criteria_rows = ""
    for pc in spec["criteria"]:
        criteria_rows += f'<tr><td>{e(pc["description"])}</td><td>{e(pc["test_method"] or "")}</td><td>{e(pc["pass_threshold"] or "")}</td></tr>\n'

    # DAR section
    dar_html = ""
    if spec.get("dar_relevant"):
        dar_html = f'''<section class="dar-section" id="dar">
            <h2>Design for Adaptable Readiness (DAR)</h2>
            <div class="dar-flag">⚑ DAR Priority</div>
            <p>{e(spec.get("dar_note") or "")}</p>
        </section>'''

    # Structural backing
    struct_html = ""
    if spec.get("structural_backing_required"):
        struct_html = f'''<section class="engineering-section" id="engineering">
            <h2>Engineering Coordination</h2>
            <p class="struct-flag">⚠ Structural backing required</p>
            <p>Retrofit category: <strong>{e(spec.get("retrofit_category") or "—")}</strong></p>
        </section>'''

    html = f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{item} — {title}</title>
    <style>
        :root {{
            --ink: #1a1a2e;
            --paper: #fafaf8;
            --accent: #2d5f8a;
            --accent-light: #e8f0f7;
            --border: #d4d4d0;
            --muted: #6b6b6b;
            --universal: #2e7d32;
            --population: #1565c0;
            --person: #6a1b9a;
            --warn: #e65100;
            --success: #2e7d32;
            --neutral: #9e9e9e;
            --font-body: 'Source Serif 4', 'Georgia', serif;
            --font-ui: 'DM Sans', 'Helvetica Neue', sans-serif;
            --font-mono: 'JetBrains Mono', 'Consolas', monospace;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: var(--font-body);
            color: var(--ink);
            background: var(--paper);
            line-height: 1.65;
            max-width: 860px;
            margin: 0 auto;
            padding: 24px;
        }}

        /* Mode toggle */
        .mode-toggle {{ display: flex; gap: 4px; background: var(--border); border-radius: 6px; padding: 3px; width: fit-content; margin-bottom: 24px; }}
        .mode-toggle button {{ font-family: var(--font-ui); font-size: 13px; padding: 6px 16px; border: none; border-radius: 4px; cursor: pointer; background: transparent; color: var(--muted); transition: all 0.2s; }}
        .mode-toggle button.active {{ background: white; color: var(--ink); box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}

        /* Section ordering */
        .spec-content {{ display: flex; flex-direction: column; }}
        .spec-content > section {{ order: var(--spec-order); }}
        body.mode-question .spec-content > section {{ order: var(--question-order); }}

        /* Header */
        .spec-header {{ margin-bottom: 32px; }}
        .item-code {{ font-family: var(--font-mono); font-size: 14px; color: var(--accent); letter-spacing: 0.5px; text-transform: uppercase; }}
        h1.spec-title {{ font-size: 28px; font-weight: 600; margin: 8px 0; line-height: 1.3; }}
        h1.question-title {{ font-size: 32px; font-weight: 700; margin: 8px 0; line-height: 1.25; color: var(--accent); display: none; }}
        body.mode-question h1.spec-title {{ display: none; }}
        body.mode-question h1.question-title {{ display: block; }}
        .evidence-badge {{ display: inline-flex; align-items: center; gap: 6px; font-family: var(--font-ui); font-size: 13px; color: var(--muted); padding: 4px 10px; background: var(--accent-light); border-radius: 4px; }}

        /* Sections */
        section {{ margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid var(--border); }}
        section:last-child {{ border-bottom: none; }}
        h2 {{ font-family: var(--font-ui); font-size: 16px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: var(--muted); margin-bottom: 12px; }}

        /* Tables */
        table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
        th {{ font-family: var(--font-ui); font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; text-align: left; padding: 8px 12px; background: var(--accent-light); color: var(--accent); border-bottom: 2px solid var(--border); }}
        td {{ padding: 8px 12px; border-bottom: 1px solid var(--border); vertical-align: top; }}
        .mode-universal td:first-child {{ color: var(--universal); font-weight: 600; }}
        .mode-population td:first-child {{ color: var(--population); font-weight: 600; }}
        .mode-person td:first-child {{ color: var(--person); font-weight: 600; }}

        /* Population badges */
        .pop-badges {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .pop-badge {{ font-family: var(--font-mono); font-size: 13px; padding: 4px 12px; border-radius: 4px; background: var(--accent-light); color: var(--accent); border: 1px solid var(--border); }}

        /* Conflict cards */
        .conflict-domains {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .conflict-card {{ font-family: var(--font-ui); font-size: 13px; padding: 6px 14px; border-radius: 4px; background: #fff3e0; color: var(--warn); border: 1px solid #ffe0b2; text-decoration: none; }}
        .conflict-card:hover {{ background: #ffe0b2; }}

        /* DAR + structural flags */
        .dar-flag {{ font-family: var(--font-ui); font-size: 14px; padding: 8px 14px; background: #e8f5e9; border-left: 4px solid var(--success); margin-bottom: 12px; }}
        .struct-flag {{ font-family: var(--font-ui); font-size: 14px; padding: 8px 14px; background: #fff3e0; border-left: 4px solid var(--warn); margin-bottom: 12px; }}

        /* Cross-references */
        .xref-links {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .xref-link {{ font-family: var(--font-mono); font-size: 14px; padding: 4px 12px; border-radius: 4px; background: var(--accent-light); color: var(--accent); text-decoration: none; border: 1px solid var(--border); }}
        .xref-link:hover {{ background: var(--accent); color: white; }}

        /* Schedule block */
        .schedule-block {{ font-family: var(--font-mono); font-size: 13px; background: #f5f5f5; padding: 16px; border-radius: 6px; border: 1px solid var(--border); white-space: pre-wrap; position: relative; }}
        .copy-btn {{ position: absolute; top: 8px; right: 8px; font-family: var(--font-ui); font-size: 11px; padding: 4px 8px; border: 1px solid var(--border); border-radius: 3px; background: white; cursor: pointer; }}

        /* Why prose */
        .why-prose {{ font-size: 16px; line-height: 1.75; color: #333; }}

        /* Metadata footer */
        .meta-footer {{ font-family: var(--font-ui); font-size: 12px; color: var(--muted); display: flex; gap: 16px; flex-wrap: wrap; }}
        .meta-footer span {{ padding: 2px 8px; background: #f0f0f0; border-radius: 3px; }}

        /* Responsive */
        @media (max-width: 640px) {{
            body {{ padding: 16px; }}
            h1.spec-title {{ font-size: 22px; }}
            h1.question-title {{ font-size: 26px; }}
            table {{ font-size: 13px; }}
            th, td {{ padding: 6px 8px; }}
        }}
    </style>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600;700&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
</head>
<body class="mode-spec">

<nav class="mode-toggle">
    <button id="btn-spec" class="active" onclick="setMode('spec')">Spec Mode</button>
    <button id="btn-question" onclick="setMode('question')">Question Mode</button>
</nav>

<header class="spec-header">
    <span class="item-code">{item}</span>
    <h1 class="spec-title">{title}</h1>
    <h1 class="question-title">{question}</h1>
    <span class="evidence-badge">{marker} Evidence Tier {tier}</span>
</header>

<div class="spec-content">

    <section id="why" style="--spec-order: 10; --question-order: 2">
        <h2>Why It Matters</h2>
        <p class="why-prose">{e(spec.get("why_md") or "")}</p>
    </section>

    <section id="values" style="--spec-order: 2; --question-order: 3">
        <h2>Values</h2>
        <table>
            <thead><tr><th>Mode</th><th>Population</th><th>Value</th><th>Notes</th></tr></thead>
            <tbody>{meas_rows}</tbody>
        </table>
    </section>

    <section id="evidence" style="--spec-order: 3; --question-order: 4">
        <h2>Evidence</h2>
        <p>{e(spec.get("evidence_summary") or "")}</p>
        <table>
            <thead><tr><th></th><th>Authors</th><th>Year</th><th>Title</th><th>Tier</th></tr></thead>
            <tbody>{source_rows}</tbody>
        </table>
    </section>

    <section id="populations" style="--spec-order: 4; --question-order: 5">
        <h2>Population Applicability</h2>
        <div class="pop-badges">{pop_badges}</div>
    </section>

    <section id="jurisdictions" style="--spec-order: 5; --question-order: 6">
        <h2>Jurisdiction Comparison</h2>
        <table>
            <thead><tr><th>Jurisdiction</th><th>Standard</th><th>Clause</th><th>Value</th><th>Notes</th></tr></thead>
            <tbody>{jur_rows}</tbody>
        </table>
    </section>

    <section id="conflicts" style="--spec-order: 6; --question-order: 7">
        <h2>Conflict Domains</h2>
        {conflict_html or '<p style="color:var(--muted)">No cross-population conflicts for this specification.</p>'}
    </section>

    {dar_html.replace('section', 'section id="dar" style="--spec-order: 7; --question-order: 8"') if dar_html else ''}

    {struct_html.replace('section', 'section id="engineering" style="--spec-order: 8; --question-order: 9"') if struct_html else ''}

    <section id="schedule" style="--spec-order: 9; --question-order: 10">
        <h2>Schedule Language</h2>
        <div class="schedule-block">
            <button class="copy-btn" onclick="copySchedule()">Copy</button>
{e(spec.get("schedule_md") or "")}
        </div>
    </section>

    <section id="criteria" style="--spec-order: 11; --question-order: 11">
        <h2>Performance Criteria</h2>
        <table>
            <thead><tr><th>Criterion</th><th>Test Method</th><th>Pass Threshold</th></tr></thead>
            <tbody>{criteria_rows}</tbody>
        </table>
    </section>

    <section id="crossrefs" style="--spec-order: 12; --question-order: 12">
        <h2>Cross-References</h2>
        <div class="xref-links">{xref_links}</div>
    </section>

    <section id="meta" style="--spec-order: 13; --question-order: 13">
        <div class="meta-footer">
            <span>Curation: {e(spec.get("curation_status") or "automated")}</span>
            <span>OT basis: {e(spec.get("ot_evidence_basis") or "—")}</span>
            <span>Retrofit: {e(spec.get("retrofit_category") or "—")}</span>
        </div>
    </section>

</div>

<script>
function setMode(mode) {{
    document.body.className = 'mode-' + mode;
    document.getElementById('btn-spec').className = mode === 'spec' ? 'active' : '';
    document.getElementById('btn-question').className = mode === 'question' ? 'active' : '';
    try {{ localStorage.setItem('guidebook-mode', mode); }} catch(e) {{}}
}}
function copySchedule() {{
    const text = document.querySelector('.schedule-block').innerText.replace('Copy\\n', '');
    navigator.clipboard.writeText(text).then(() => {{
        const btn = document.querySelector('.copy-btn');
        btn.textContent = 'Copied!';
        setTimeout(() => btn.textContent = 'Copy', 2000);
    }});
}}
// Restore mode
try {{
    const saved = localStorage.getItem('guidebook-mode');
    if (saved) setMode(saved);
}} catch(e) {{}}
</script>

</body>
</html>"""

    return html


def generate(item_code, output_path=None):
    """Generate a specification page."""
    conn = sqlite3.connect(str(DB_PATH))
    spec = query_spec(conn, item_code)
    conn.close()

    if not spec:
        print(f"ERROR: Specification '{item_code}' not found in database.", file=sys.stderr)
        sys.exit(1)

    html = render_html(spec)

    if output_path is None:
        output_path = OUTPUT_DIR / f"{item_code.lower()}.html"

    os.makedirs(Path(output_path).parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated: {output_path} ({len(html)} bytes)")
    return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 spec_page.py <item_code> [--output <path>]")
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
