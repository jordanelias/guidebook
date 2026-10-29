#!/usr/bin/env python3
"""
scripts/generate/spec_page_v2.py — specification page generator (pilot).

Renders one specification page as a single self-contained HTML file with:
  * a three-tier value model (for everyone / for a specific group, ICF code or access need / for one person);
  * an accordion per jurisdiction (top line = jurisdiction, standard/clause, value, note; body = everything else),
    listing every jurisdiction in the library's search roster, including those with no entry yet;
  * filters by population, ICF code and access need, driven by the classification tables (migration 026);
  * unit selection (length: metric/imperial/as stated; slope: ratio/percent/degrees/as stated);
  * a bulleted "Why it matters".

Replaces scripts/generate/spec_page.py for pages that have a data file in data/spec_pages/, because that
generator needs `specification` / `jurisdictional_value` tables that the migration-built DB does not have.

Inputs (all read-only):  data/guidebook.db  +  data/spec_pages/<ITEM>.json  +  data/question-headings.yaml
Contract: every ref_id / population / ICF / need code named in the JSON must exist in the DB, or the run aborts.

Usage:
    python3 scripts/generate/spec_page_v2.py E-03
    python3 scripts/generate/spec_page_v2.py E-03 --output /tmp/e03.html
"""

import json
import math
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO / "data" / "guidebook.db"))
OUT_DIR = REPO / "site" / "specs"

JURISDICTION_NAMES = {
    "AR": "Argentina", "AT": "Austria", "AU": "Australia", "BD": "Bangladesh", "BE": "Belgium", "BR": "Brazil",
    "CA": "Canada", "CH": "Switzerland", "CL": "Chile", "CN": "China", "CO": "Colombia", "CR": "Costa Rica",
    "DE": "Germany", "DK": "Denmark", "EC": "Ecuador", "EG": "Egypt", "ES": "Spain", "ET": "Ethiopia",
    "EU": "European Union", "FI": "Finland", "FR": "France", "GH": "Ghana", "GT": "Guatemala", "ID": "Indonesia",
    "IE": "Ireland", "IN": "India", "IT": "Italy", "JP": "Japan", "KE": "Kenya", "KR": "South Korea",
    "MA": "Morocco", "MX": "Mexico", "NG": "Nigeria", "NL": "Netherlands", "NO": "Norway", "NZ": "New Zealand",
    "PE": "Peru", "PH": "Philippines", "PT": "Portugal", "SE": "Sweden", "SG": "Singapore", "TH": "Thailand",
    "TZ": "Tanzania", "UK": "United Kingdom", "US": "United States", "UY": "Uruguay", "ZA": "South Africa",
    "ISO": "International (ISO)",
}

LEVELS = {  # level -> (label, css class)
    "primary": ("Primary source read", "ok"),
    "official-excerpt": ("Official page quoting the rule", "ok"),
    "secondary": ("Secondary sources only", "warn"),
    "library-title-only": ("Library title only", "warn"),
    "project-extraction": ("Earlier extraction, not re-verified", "warn"),
    "values-not-retrieved": ("Standard found, values not retrieved", "gap"),
    "none": ("No entry yet", "none"),
}
STATUS = {  # value status -> (label, css class)
    "provisional": ("Provisional", "warn"),
    "regulatory": ("Legal ceiling", "info"),
    "no-evidence": ("Not set: no evidence yet", "gap"),
    "method": ("Set by assessment", "info"),
}
EVIDENCE_LABEL = {"in-library": "Evidence in the library", "external": "Evidence found outside the library (abstract level)",
                  "regulatory": "Regulatory fact"}

TOKEN = re.compile(r"\{\{(slope|len)=([^|}]+)(?:\|([^}]*))?\}\}")


class ContractError(Exception):
    pass


def trim(x):
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return s


def parse_num(expr):
    expr = expr.strip()
    if "/" in expr:
        a, b = expr.split("/")
        return float(a) / float(b)
    return float(expr)


def default_text(kind, v):
    """Server-side default rendering (ratio / metric); the page JS re-renders from the selected units."""
    if kind == "slope":
        n = 1.0 / v
        r = round(n)
        return "1:" + (str(r) if abs(n - r) < 0.06 else f"{n:.1f}".rstrip("0").rstrip("."))
    return f"{v / 1000:.2f}".rstrip("0").rstrip(".") + " m" if v >= 1000 else f"{round(v)} mm"


def rt(text):
    """Escape text and expand unit tokens into <span class="u"> elements."""
    out, pos = [], 0
    for m in TOKEN.finditer(text):
        out.append(escape(text[pos:m.start()]))
        kind, expr, orig = m.group(1), m.group(2), m.group(3)
        v = parse_num(expr)
        attrs = f'class="u" data-k="{kind}" data-v="{v:.8g}"'
        if orig:
            attrs += f' data-o="{escape(orig, quote=True)}"'
        out.append(f"<span {attrs}>{escape(default_text(kind, v))}</span>")
        pos = m.end()
    out.append(escape(text[pos:]))
    return "".join(out)


def load_question(item):
    p = REPO / "data" / "question-headings.yaml"
    if not p.exists():
        return None
    m = re.search(rf"^{re.escape(item)}:\s*\n\s+title:\s*\"(.*?)\"\s*\n\s+question_heading:\s*\"(.*?)\"", p.read_text(encoding="utf-8"), re.M)
    return m.group(2) if m else None


def load(item):
    page = json.loads((REPO / "data" / "spec_pages" / f"{item}.json").read_text(encoding="utf-8"))
    db = sqlite3.connect(f"file:{DB_PATH.as_posix()}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    row = db.execute("SELECT item_code, name, bpc_source_slug FROM items WHERE item_code=?", (item,)).fetchone()
    if not row:
        raise ContractError(f"item {item} not in DB")
    d = {"page": page, "item": dict(row)}
    d["pops"] = {r[0]: r[1] for r in db.execute("SELECT population_code, display_name FROM populations")}
    d["icf"] = {r[0]: r[1] for r in db.execute("SELECT icf_code, title FROM icf_codes")}
    d["needs"] = {r[0]: r[1] for r in db.execute("SELECT need_code, label FROM access_needs")}
    d["user_version"] = db.execute("PRAGMA user_version").fetchone()[0]
    d["coverage"] = {r[0]: r[1] for r in db.execute(
        "SELECT jurisdiction, status FROM search_coverage WHERE slug=?", (row["bpc_source_slug"],))}
    d["statutory_counts"] = {r[0]: r[1] for r in db.execute(
        "SELECT jurisdiction, COUNT(*) FROM evidence_sources WHERE tier IN (4,5,6) GROUP BY jurisdiction")}
    d["gaps"] = [dict(r) for r in db.execute(
        "SELECT gap_id, priority, status, category, description FROM gaps WHERE section=? ORDER BY gap_id", (item,))]
    d["item_pops"] = [r[0] for r in db.execute("SELECT population_code FROM item_population_links WHERE item_code=?", (item,))]

    def src(ref):
        r = db.execute("""SELECT ref_id, pub_title, author_display, pub_year, tier, evidence_type, doi, url,
                                 metadata_quality, verification_status FROM evidence_sources WHERE ref_id=?""", (ref,)).fetchone()
        if not r:
            raise ContractError(f"ref {ref} named in data/spec_pages/{item}.json is not in evidence_sources")
        s = dict(r)
        s["subject"] = [dict(x) for x in db.execute(
            """SELECT population_code, MAX(confidence) AS confidence, GROUP_CONCAT(DISTINCT method) AS methods
               FROM source_population_tags WHERE ref_id=? AND role='subject' GROUP BY population_code""", (ref,))]
        s["icf"] = [x[0] for x in db.execute("SELECT DISTINCT icf_code FROM source_icf_tags WHERE ref_id=?", (ref,))]
        s["needs"] = [x[0] for x in db.execute("SELECT DISTINCT need_code FROM source_need_tags WHERE ref_id=?", (ref,))]
        s["review"] = {x[0] for x in db.execute("SELECT review_status FROM source_population_tags WHERE ref_id=? AND role='subject'", (ref,))}
        return s

    d["src"] = src
    # contract: all coded references exist
    def need_codes(codes, table, label):
        for c in codes:
            if c not in table:
                raise ContractError(f"{label} code {c!r} in page data is not in the DB")
    v = page["values"]
    for r in v["group"]:
        need_codes(r["populations"], d["pops"], "population")
        need_codes(r["icf"], d["icf"], "ICF")
        need_codes(r["needs"], d["needs"], "access-need")
        for ref in r.get("refs", []):
            src(ref)
    for j in page["jurisdictions"]:
        for p in j["provisions"]:
            need_codes(p[2], d["needs"], "access-need")
        for ref in j.get("kb_refs", []):
            src(ref)
    for w in page["why_it_matters"]:
        for ref in w.get("refs", []):
            src(ref)
    d["db"] = db  # kept open (read-only) for the lifetime of the run; d["src"] closes over it
    return d


def chips(codes, table, cls, with_code=True):
    out = []
    for c in codes:
        label = table.get(c, c)
        label = label[:1].upper() + label[1:] if cls == "pop" else label
        out.append(f'<span class="chip {cls}" title="{escape(c)}">{escape(c)}<span class="chip-l"> {escape(label)}</span></span>' if with_code
                   else f'<span class="chip {cls}">{escape(label)}</span>')
    return "".join(out)


def build(d):
    page, item = d["page"], d["item"]
    code = item["item_code"]
    title = item["name"]
    question = load_question(code) or title
    facets = {"pop": set(), "icf": set(), "need": set()}

    def tagattrs(pops, icf, needs, scope):
        facets["pop"].update(pops)
        facets["icf"].update(icf)
        facets["need"].update(needs)
        return (f'data-scope="{scope}" data-pop="{" ".join(pops)}" data-icf="{" ".join(icf)}" data-need="{" ".join(needs)}"')

    # ---- why it matters
    why = []
    for w in page["why_it_matters"]:
        refs = ""
        if w.get("refs"):
            refs = " " + " ".join(f'<span class="ref">{escape(r)}</span>' for r in w["refs"])
        why.append(f'<li><span class="ev ev-{w["evidence"]}">{escape(EVIDENCE_LABEL[w["evidence"]])}</span>'
                   f'<span class="li-text">{rt(w["text"])}{refs}</span></li>')

    # ---- values
    def value_card(r, scope, tier_label):
        st_label, st_cls = STATUS[r["status"]]
        pops, icf, needs = r.get("populations", []), r.get("icf", []), r.get("needs", [])
        tags = ""
        if scope == "group":
            tags = (f'<div class="tags"><span class="tg-l">Groups</span>{chips(pops, d["pops"], "pop")}'
                    f'<span class="tg-l">ICF</span>{chips(icf, d["icf"], "icf")}'
                    f'<span class="tg-l">Needs</span>{chips(needs, d["needs"], "need", with_code=False)}</div>')
        refs = ""
        if r.get("refs"):
            refs = '<div class="refs">In the library: ' + " ".join(f'<span class="ref">{escape(x)}</span>' for x in r["refs"]) + "</div>"
        return (f'<article class="vcard fi" {tagattrs(pops, icf, needs, scope)}>'
                f'<header><h4>{escape(r["who"])}</h4><span class="pill {st_cls}">{escape(st_label)}</span></header>'
                f'<p class="vstate">{rt(r["statement"])}</p><p class="vbasis">{rt(r["basis"])}</p>{tags}{refs}</article>')

    v = page["values"]
    values_html = (
        '<h3 class="tier">For everyone <small>applies to all people; the universal design scale</small></h3>'
        + "".join(value_card(r, "universal", "everyone") for r in v["universal"])
        + '<h3 class="tier">For a specific group, ICF code or access need <small>filter these with the controls above</small></h3>'
        + "".join(value_card(r, "group", "group") for r in v["group"])
        + '<h3 class="tier">For one person <small>tailored through individual assessment</small></h3>'
        + "".join(value_card(r, "person", "person") for r in v["person"])
    )

    # ---- jurisdictions
    by_code = {j["code"]: j for j in page["jurisdictions"]}
    roster = list(d["coverage"].keys())
    for c in by_code:
        if c not in roster:
            roster.append(c)

    def jur_item(j):
        lvl_label, lvl_cls = LEVELS[j["level"]]
        needs = sorted({n for p in j["provisions"] for n in p[2]})
        rows = []
        for label, text, pneeds in j["provisions"]:
            facets["need"].update(pneeds)
            rows.append(f'<div class="prov" data-need="{" ".join(pneeds)}"><dt>{escape(label)}</dt><dd>{rt(text)}</dd></div>')
        srcs = "".join(f'<li><a href="{escape(s["url"])}" target="_blank" rel="noopener">{escape(s["label"])}</a></li>' for s in j["sources"])
        kb = ""
        if j["kb_refs"]:
            parts = []
            for ref in j["kb_refs"]:
                s = d["src"](ref)
                parts.append(f'<li><span class="ref">{escape(ref)}</span> {escape(s["pub_title"])} ({s["pub_year"]}, tier {s["tier"]})</li>')
            kb = f'<div class="blk"><h5>In the Guidebook library</h5><ul>{"".join(parts)}</ul></div>'
        name = JURISDICTION_NAMES.get(j["code"], j["code"])
        return (f'<details class="jur fi" data-scope="universal" data-pop="" data-icf="" data-need="{" ".join(needs)}" data-has="1" data-code="{j["code"]}">'
                f'<summary><span class="j-name">{escape(name)}<small>{escape(j["code"])}</small></span>'
                f'<span class="j-std"><b>{escape(j["standard"])}</b><small>{escape(j["clause"])} &middot; {escape(j["edition"])}</small></span>'
                f'<span class="j-val">{rt(j["headline"])}</span>'
                f'<span class="j-note">{rt(j["note"])}</span>'
                f'<span class="j-badges"><span class="pill {lvl_cls}">{escape(lvl_label)}</span><span class="pill tier">{escape(j["tier"])}</span></span></summary>'
                f'<div class="j-body"><dl class="provs">{"".join(rows)}</dl>'
                f'<div class="blk"><h5>Compared with the Guidebook position</h5><p>{rt(j["vs_guidebook"])}</p></div>'
                f'<div class="blk"><h5>Regime</h5><p>{escape(j["regime"])}</p></div>'
                f'<div class="blk"><h5>What was read</h5><p>{rt(j["read"])}</p></div>'
                f'<div class="blk"><h5>Open questions</h5><p>{rt(j["open"])}</p></div>'
                f'{kb}'
                + (f'<div class="blk"><h5>Sources</h5><ul>{srcs}</ul></div>' if srcs else "")
                + f'<p class="checked">Checked 2026-10-29 &middot; code currency not machine-verified</p></div></details>')

    def jur_empty(code):
        cov = d["coverage"].get(code)
        n = d["statutory_counts"].get(code, 0)
        msg = ("Searched for this item; no ramp value captured." if cov == "SEARCHED" else "Not yet searched for this item.")
        lib = (f"The library already holds {n} standard/code source(s) for this jurisdiction on other topics." if n
               else "The library holds no standard or code sources for this jurisdiction yet.")
        name = JURISDICTION_NAMES.get(code, code)
        return (f'<details class="jur fi empty" data-scope="universal" data-pop="" data-icf="" data-need="" data-has="0" data-code="{code}">'
                f'<summary><span class="j-name">{escape(name)}<small>{escape(code)}</small></span>'
                f'<span class="j-std"><b>No entry yet</b></span><span class="j-val">&mdash;</span>'
                f'<span class="j-note">{escape(msg)}</span>'
                f'<span class="j-badges"><span class="pill none">No entry yet</span></span></summary>'
                f'<div class="j-body"><p>{escape(msg)} {escape(lib)}</p>'
                f'<p>To add this jurisdiction: identify the national code or standard, read the ramp provisions from the source text, '
                f'and record clause, edition, value, scope and exceptions as above.</p></div></details>')

    have = sorted((c for c in roster if c in by_code), key=lambda c: JURISDICTION_NAMES.get(c, c))
    none = sorted((c for c in roster if c not in by_code), key=lambda c: JURISDICTION_NAMES.get(c, c))
    jur_html = "".join(jur_item(by_code[c]) for c in have) + "".join(jur_empty(c) for c in none)
    jur_counts = (len(have), len(none))

    # ---- evidence in library
    ev_html = []
    for e in page["evidence"]:
        s = d["src"](e["ref"])
        subj = [x["population_code"] for x in s["subject"]]
        scope = "universal" if (not subj or subj == ["ALL"]) else "group"
        pops = [p for p in subj if p != "ALL"]
        tag = tagattrs(pops, s["icf"], s["needs"], scope)
        sub_txt = ", ".join(f'{x["population_code"]} ({x["confidence"]}, {x["methods"]})' for x in s["subject"]) or "none assigned"
        reviewed = "reviewed" if s["review"] == {"REVIEWED"} else "unreviewed"
        doi = f'<a href="https://doi.org/{escape(s["doi"])}" target="_blank" rel="noopener">doi:{escape(s["doi"])}</a>' if s["doi"] else ""
        ev_html.append(
            f'<details class="ev-row fi" {tag}><summary><span class="ref">{escape(s["ref_id"])}</span>'
            f'<span class="e-cite">{escape(s["author_display"] or "")} ({s["pub_year"]}). {escape(s["pub_title"])}</span>'
            f'<span class="j-badges"><span class="pill info">{escape(e["role"])}</span><span class="pill tier">tier {s["tier"]}</span></span></summary>'
            f'<div class="j-body"><p>{rt(e["relevance"])}</p>'
            f'<div class="tags"><span class="tg-l">Study population tags</span>{escape(sub_txt)} <em>({reviewed})</em></div>'
            f'<div class="tags"><span class="tg-l">ICF</span>{chips(s["icf"], d["icf"], "icf")}'
            f'<span class="tg-l">Needs</span>{chips(s["needs"], d["needs"], "need", with_code=False)}</div>'
            f'<p class="checked">{escape(s["metadata_quality"] or "")} &middot; {escape(s["verification_status"] or "")} &middot; {doi}</p></div></details>')
    ext_html = "".join(
        f'<li><b>{escape(x["cite"])}</b> {("<a href=https://doi.org/" + escape(x["doi"]) + " target=_blank rel=noopener>doi:" + escape(x["doi"]) + "</a>") if x["doi"] else "<em>DOI not yet resolved</em>"}'
        f'<br>{escape(x["finding"])}<br><span class="role">{escape(x["role"])}</span></li>' for x in page["external_evidence"])

    # ---- gaps
    gap_html = "".join(
        f'<details class="gap"><summary><span class="ref">{escape(g["gap_id"])}</span><span class="pill {"gap" if g["status"].startswith("OPEN") else "none"}">{escape(g["status"])}</span>'
        f'<span class="e-cite">{escape((g["description"] or "")[:150])}...</span></summary><div class="j-body"><p>{escape(g["description"] or "")}</p></div></details>'
        for g in d["gaps"])

    # ---- filter facets (only codes that occur on the page)
    def facet_buttons(kind, codes, table, label_fn):
        return "".join(f'<button type="button" class="fchip" data-f="{kind}" data-c="{escape(c)}" aria-pressed="false">{label_fn(c, table[c])}</button>'
                       for c in sorted(codes))
    pop_btn = facet_buttons("pop", {p for p in facets["pop"] if p != "ALL"}, d["pops"],
                            lambda c, n: f'<b>{escape(c)}</b> {escape(n[:1].upper() + n[1:])}')
    icf_btn = facet_buttons("icf", facets["icf"], d["icf"], lambda c, n: f'<b>{escape(c)}</b> {escape(n)}')
    need_btn = facet_buttons("need", facets["need"], d["needs"], lambda c, n: escape(n))

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out = TEMPLATE
    for k, val in {
        "__TITLE__": escape(title), "__CODE__": escape(code), "__QUESTION__": escape(question),
        "__WHY__": "".join(why), "__VALUES__": values_html, "__JURS__": jur_html,
        "__JUR_HAVE__": str(jur_counts[0]), "__JUR_NONE__": str(jur_counts[1]),
        "__EVIDENCE__": "".join(ev_html), "__EXCLUDED__": escape(page["excluded_evidence_note"]),
        "__EXTERNAL__": ext_html, "__GAPS__": gap_html or "<p>No open gaps recorded.</p>",
        "__POPBTN__": pop_btn, "__ICFBTN__": icf_btn, "__NEEDBTN__": need_btn,
        "__SLUG__": escape(item["bpc_source_slug"]), "__UV__": str(d["user_version"]), "__STAMP__": stamp,
        "__STAGING__": escape(page["_meta"]["status"]), "__PREPARED__": escape(page["_meta"]["prepared_by"]),
    }.items():
        out = out.replace(k, val)
    return out


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__CODE__ &mdash; __TITLE__</title>
<style>
:root{--ink:#1a1a2e;--paper:#fafaf8;--card:#fff;--accent:#2d5f8a;--accent-l:#e8f0f7;--border:#d4d4d0;--muted:#5f5f5f;
--ok:#1b5e20;--ok-bg:#e8f5e9;--warn:#8a4b00;--warn-bg:#fff3e0;--gap:#a3260b;--gap-bg:#fdecea;--info:#1a4f7a;--info-bg:#e3f0fb;--none:#555;--none-bg:#eee;
--hit:#1565c0;--fb:'Source Serif 4',Georgia,serif;--fu:'DM Sans','Helvetica Neue',sans-serif;--fm:'JetBrains Mono',Consolas,monospace}
@media (prefers-color-scheme:dark){:root{--ink:#ececf1;--paper:#14151a;--card:#1c1e25;--accent:#8ab6e0;--accent-l:#232a35;--border:#363a45;--muted:#a3a6b0;
--ok:#8fd694;--ok-bg:#1e3321;--warn:#f0b36a;--warn-bg:#3a2d17;--gap:#f09a89;--gap-bg:#3a1f1b;--info:#8cc4f0;--info-bg:#1b2d3e;--none:#bbb;--none-bg:#2a2c33;--hit:#6cb0ff}}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--fb);color:var(--ink);background:var(--paper);line-height:1.6;max-width:1040px;margin:0 auto;padding:24px 16px 80px}
h1{font-size:28px;line-height:1.25;margin:6px 0}
h2{font-family:var(--fu);font-size:15px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);margin:0 0 12px}
h3.tier{font-family:var(--fu);font-size:16px;margin:22px 0 10px;color:var(--ink)}h3.tier small{font-weight:400;color:var(--muted);margin-left:8px;font-size:13px}
h4{font-family:var(--fu);font-size:15px}h5{font-family:var(--fu);font-size:12px;text-transform:uppercase;letter-spacing:.4px;color:var(--muted);margin-bottom:2px}
section{margin:0 0 36px;padding-bottom:20px;border-bottom:1px solid var(--border)}
.code{font-family:var(--fm);font-size:14px;color:var(--accent)}
.qline{display:none;font-size:30px;color:var(--accent);font-weight:700;margin:6px 0}
body.q .qline{display:block}body.q h1{display:none}
.toggle{display:inline-flex;gap:4px;background:var(--border);border-radius:6px;padding:3px;margin-bottom:16px}
.toggle button{font-family:var(--fu);font-size:13px;padding:6px 14px;border:0;border-radius:4px;background:transparent;color:var(--muted);cursor:pointer}
.toggle button.on{background:var(--card);color:var(--ink)}
.status{font-family:var(--fu);font-size:13px;border:1px solid var(--border);background:var(--warn-bg);color:var(--ink);border-radius:6px;padding:10px 14px;margin:12px 0}
.status b{color:var(--warn)}
.controls{background:var(--paper);border-bottom:1px solid var(--border);padding:10px 0;margin-bottom:24px;font-family:var(--fu);font-size:13px}
.totop{position:fixed;right:14px;bottom:14px;z-index:6;font-family:var(--fu);font-size:12px;background:var(--accent);color:#fff;padding:7px 12px;border-radius:18px;text-decoration:none;box-shadow:0 2px 6px rgba(0,0,0,.3)}
.crow{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:4px 0}.crow .cl{min-width:104px;color:var(--muted);font-weight:600}
.seg{display:inline-flex;border:1px solid var(--border);border-radius:6px;overflow:hidden}
.seg button{font:inherit;padding:4px 10px;border:0;background:var(--card);color:var(--ink);cursor:pointer;border-right:1px solid var(--border)}
.seg button:last-child{border-right:0}.seg button[aria-pressed=true]{background:var(--accent);color:#fff}
.fchip{font:inherit;font-size:12px;padding:3px 9px;border:1px solid var(--border);border-radius:14px;background:var(--card);color:var(--ink);cursor:pointer}
.fchip[aria-pressed=true]{background:var(--hit);color:#fff;border-color:var(--hit)}.fchip b{font-family:var(--fm);font-weight:500}
.fgroup{display:flex;flex-wrap:wrap;gap:5px;flex:1}
.clear{font:inherit;color:var(--accent);background:none;border:0;cursor:pointer;text-decoration:underline}
.count{color:var(--muted)}
button:focus-visible,summary:focus-visible{outline:3px solid var(--hit);outline-offset:2px}
ul.why{list-style:disc;padding-left:22px}ul.why li{margin:0 0 14px;padding-left:4px}
ul.why li .ev{display:block;font-family:var(--fu);font-size:11px;text-transform:uppercase;letter-spacing:.4px;margin-bottom:2px}
.ev-in-library{color:var(--ok)}.ev-external{color:var(--warn)}.ev-regulatory{color:var(--info)}
.pill{display:inline-block;font-family:var(--fu);font-size:11px;padding:2px 8px;border-radius:10px;white-space:nowrap}
.pill.ok{background:var(--ok-bg);color:var(--ok)}.pill.warn{background:var(--warn-bg);color:var(--warn)}.pill.gap{background:var(--gap-bg);color:var(--gap)}
.pill.info{background:var(--info-bg);color:var(--info)}.pill.none{background:var(--none-bg);color:var(--none)}.pill.tier{background:var(--accent-l);color:var(--accent)}
.vcard{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:12px 14px;margin:0 0 10px}
.vcard header{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}
.vstate{font-size:18px;font-weight:600;margin:6px 0 4px}.vbasis{font-size:14px;color:var(--muted)}
.tags{font-family:var(--fu);font-size:12px;margin-top:8px;display:flex;flex-wrap:wrap;gap:4px;align-items:center}.tg-l{color:var(--muted);margin-right:2px;font-weight:600}
.chip{font-family:var(--fm);font-size:11px;padding:1px 7px;border-radius:4px;background:var(--accent-l);color:var(--accent);border:1px solid var(--border)}
.chip.need{font-family:var(--fu)}.chip-l{font-family:var(--fu);color:var(--muted)}
.refs{font-family:var(--fu);font-size:12px;margin-top:6px;color:var(--muted)}.ref{font-family:var(--fm);font-size:12px;background:var(--accent-l);padding:0 5px;border-radius:3px;color:var(--accent)}
details{background:var(--card);border:1px solid var(--border);border-radius:8px;margin:0 0 8px}
summary{cursor:pointer;list-style:none;padding:10px 14px}summary::-webkit-details-marker{display:none}
summary::before{content:"\25B8";display:inline-block;width:1.1em;color:var(--muted)}details[open]>summary::before{content:"\25BE"}
details[open]>summary{border-bottom:1px solid var(--border)}
.jur>summary{display:grid;grid-template-columns:minmax(120px,1.1fr) minmax(170px,2fr) minmax(110px,1.4fr) minmax(150px,2fr) auto;gap:6px 14px;align-items:start;font-family:var(--fu);font-size:14px}
.jur>summary::before{position:absolute;margin-left:-4px}.jur>summary>*{margin-left:0}.jur>summary .j-name{padding-left:16px}
.j-name{font-weight:700}.j-name small,.j-std small{display:block;font-weight:400;color:var(--muted);font-size:12px}
.j-val{font-size:15px;font-weight:700}.j-note{color:var(--muted);font-size:13px}.j-badges{display:flex;gap:4px;flex-wrap:wrap;justify-content:flex-end}
.jur.empty{opacity:.82}.jur.empty .j-val{color:var(--muted)}
.j-body{padding:12px 14px 14px 30px;font-size:14px}.j-body p{margin:0 0 8px}.blk{margin:10px 0}.blk ul{padding-left:18px}.blk li{margin:2px 0}
dl.provs{display:grid;grid-template-columns:minmax(150px,1fr) 3fr;gap:6px 14px;margin-bottom:10px}
.prov{display:contents}.prov dt{font-weight:600;font-family:var(--fu)}.prov dd{margin:0}
.checked{font-family:var(--fu);font-size:12px;color:var(--muted)}
.ev-row>summary,.gap>summary{display:flex;gap:10px;align-items:center;flex-wrap:wrap;font-family:var(--fu);font-size:14px}.e-cite{flex:1;min-width:200px}
.fi.hit{box-shadow:inset 4px 0 0 var(--hit)}.fi.hidden{display:none}.prov.hit dt,.prov.hit dd{color:var(--hit)}.prov.dim{opacity:.55}
.jbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:10px;font-family:var(--fu);font-size:13px}
.jbar button,.jbar label{font:inherit}.jbar button{background:var(--card);border:1px solid var(--border);border-radius:6px;padding:4px 10px;color:var(--ink);cursor:pointer}
ul.ext{padding-left:20px;font-size:14px}ul.ext li{margin:0 0 10px}.role{font-family:var(--fu);font-size:12px;color:var(--warn)}
.u{white-space:nowrap}
footer{font-family:var(--fu);font-size:12px;color:var(--muted)}
@media(max-width:760px){.jur>summary{grid-template-columns:1fr}.j-badges{justify-content:flex-start}dl.provs{grid-template-columns:1fr}.crow .cl{min-width:100%}}
@media print{.totop{display:none}.jur .j-body{display:block}}
</style>
</head>
<body>
<div class="toggle" role="group" aria-label="View"><button type="button" id="vt" class="on" aria-pressed="true">Technical view</button><button type="button" id="vq" aria-pressed="false">Plain-question view</button></div>
<header>
<span class="code">__CODE__</span>
<h1>__TITLE__</h1>
<p class="qline">__QUESTION__</p>
<p class="count" style="font-family:var(--fu);font-size:13px">Question this specification answers: <i>__QUESTION__</i></p>
</header>
<div class="status" role="note"><b>Pilot page &mdash; read the status.</b> Values marked <i>provisional</i> or <i>not set</i> are not yet supported by evidence in the library. Jurisdiction figures are labelled by how they were verified: only the US text was read from a primary source; others come from secondary sources or earlier project extractions and are shown as such. Population, ICF and access-need codes and their tags are <b>provisional and unreviewed</b>. Curated text is staged in <code>data/spec_pages/__CODE__.json</code> until a specification table exists in the database.</div>

<div class="controls" id="controls" aria-label="Page controls">
<div class="crow"><span class="cl">Units</span>
 <span class="seg" role="group" aria-label="Length units"><button type="button" data-u="len" data-m="met" aria-pressed="true">Metric (mm, m)</button><button type="button" data-u="len" data-m="imp" aria-pressed="false">Imperial (in, ft)</button><button type="button" data-u="len" data-m="stated" aria-pressed="false">As stated in source</button></span>
 <span class="seg" role="group" aria-label="Slope units"><button type="button" data-u="slope" data-m="ratio" aria-pressed="true">Ratio (1:n)</button><button type="button" data-u="slope" data-m="pct" aria-pressed="false">Percent</button><button type="button" data-u="slope" data-m="deg" aria-pressed="false">Degrees</button><button type="button" data-u="slope" data-m="stated" aria-pressed="false">As stated</button></span>
</div>
<div class="crow"><span class="cl">Who it's for</span><span class="fgroup">__POPBTN__</span></div>
<div class="crow"><span class="cl">ICF code</span><span class="fgroup">__ICFBTN__</span></div>
<div class="crow"><span class="cl">Access need</span><span class="fgroup">__NEEDBTN__</span></div>
<div class="crow"><label><input type="checkbox" id="onlyspec"> Hide general (everyone) items when a filter is on</label>
 <button type="button" class="clear" id="clear">Clear filters</button><span class="count" id="count" role="status" aria-live="polite"></span></div>
</div>

<section id="why"><h2>Why it matters</h2><ul class="why">__WHY__</ul></section>

<section id="values"><h2>Values &mdash; who each one is for</h2>__VALUES__</section>

<section id="jurisdictions"><h2>Jurisdiction comparison</h2>
<p style="font-size:14px;color:var(--muted);margin-bottom:10px">__JUR_HAVE__ jurisdictions with an entry and __JUR_NONE__ with none yet. Each row shows the standard, clause, value and a note; open it for everything else. These are general legal requirements that apply to everyone; with an access-need filter on, the provisions that serve that need are highlighted.</p>
<div class="jbar"><button type="button" id="expand">Expand all</button><button type="button" id="collapse">Collapse all</button>
<label><input type="checkbox" id="hidenone"> Hide jurisdictions with no entry yet</label></div>
<div id="jlist">__JURS__</div></section>

<section id="evidence"><h2>Evidence in the library</h2>__EVIDENCE__
<p style="font-size:13px;color:var(--muted);margin-top:8px">__EXCLUDED__</p></section>

<section id="external"><h2>Evidence found but not yet in the library</h2>
<p style="font-size:13px;color:var(--muted);margin-bottom:8px">Read at abstract level only; not ingested or verified beyond a resolved identifier where shown.</p>
<ul class="ext">__EXTERNAL__</ul></section>

<section id="gaps"><h2>Open questions and gaps</h2>__GAPS__</section>

<a class="totop" href="#controls">&uarr; Filters &amp; units</a>
<footer>Item <b>__CODE__</b> &middot; BPC slug <code>__SLUG__</code> &middot; database schema version __UV__ &middot; generated __STAMP__ by scripts/generate/spec_page_v2.py &middot; prepared by __PREPARED__</footer>

<script>
(function(){
var prefs={len:'met',slope:'ratio'},sel={pop:[],icf:[],need:[]},onlySpec=false;
function trim(n){return parseFloat(n).toString();}
function fmtSlope(f,m,o){
 if(m==='stated'&&o)return o;
 if(m==='pct'){var p=f*100;return trim(p.toFixed(p<1?2:1))+' %';}
 if(m==='deg'){return trim((Math.atan(f)*180/Math.PI).toFixed(1))+'°';}
 var n=1/f,r=Math.round(n);return '1:'+(Math.abs(n-r)<0.06?r:trim(n.toFixed(1)));}
function fmtLen(mm,m,o){
 if(m==='stated'&&o)return o;
 if(m==='imp'){var inch=mm/25.4;
  if(inch>=36){var ft=Math.floor(inch/12+1e-9),rem=Math.round((inch-ft*12)*2)/2;if(rem>=12){ft+=1;rem=0;}return ft+' ft'+(rem?' '+trim(rem)+' in':'');}
  return trim(inch.toFixed(1))+' in';}
 if(mm>=1000)return trim((mm/1000).toFixed(2))+' m';return Math.round(mm)+' mm';}
function renderUnits(){var els=document.querySelectorAll('.u');for(var i=0;i<els.length;i++){var e=els[i],k=e.getAttribute('data-k'),v=parseFloat(e.getAttribute('data-v')),o=e.getAttribute('data-o');
 e.textContent=(k==='slope')?fmtSlope(v,prefs.slope,o):fmtLen(v,prefs.len,o);}
 var b=document.querySelectorAll('[data-u]');for(var j=0;j<b.length;j++){b[j].setAttribute('aria-pressed',prefs[b[j].getAttribute('data-u')]===b[j].getAttribute('data-m'));}}
function toks(el,a){var s=el.getAttribute(a)||'';return s?s.split(' '):[];}
function inter(a,b){for(var i=0;i<a.length;i++)if(b.indexOf(a[i])>-1)return true;return false;}
function applyFilter(){
 var active=['pop','icf','need'].filter(function(f){return sel[f].length>0;});
 var items=document.querySelectorAll('.fi'),shown={vcard:0,ev:0,jur:0},tot={vcard:0,ev:0,jur:0};
 var hideNone=document.getElementById('hidenone').checked;
 for(var i=0;i<items.length;i++){var el=items[i],scope=el.getAttribute('data-scope');
  var kind=el.classList.contains('vcard')?'vcard':(el.classList.contains('jur')?'jur':'ev');tot[kind]++;
  var hit=active.length>0&&active.every(function(f){return inter(toks(el,'data-'+f),sel[f]);});
  var show=true;
  if(active.length>0){ if(scope==='group')show=hit; else show=!onlySpec; }
  if(kind==='jur'&&hideNone&&el.getAttribute('data-has')==='0')show=false;
  el.classList.toggle('hidden',!show);el.classList.toggle('hit',active.length>0&&hit&&show);
  if(kind==='jur'&&sel.need.length){var ps=el.querySelectorAll('.prov'),any=false;
   for(var p=0;p<ps.length;p++){var h=inter(toks(ps[p],'data-need'),sel.need);ps[p].classList.toggle('hit',h);ps[p].classList.toggle('dim',!h);any=any||h;}
   el.classList.toggle('hit',any&&show);}
  else if(kind==='jur'){var ps2=el.querySelectorAll('.prov');for(var q=0;q<ps2.length;q++){ps2[q].classList.remove('hit','dim');}}
  if(show)shown[kind]++;}
 document.getElementById('count').textContent=' Showing '+shown.vcard+'/'+tot.vcard+' value cards, '+shown.jur+'/'+tot.jur+' jurisdictions, '+shown.ev+'/'+tot.ev+' evidence items.';
 var chips=document.querySelectorAll('.fchip');for(var c=0;c<chips.length;c++){var f=chips[c].getAttribute('data-f'),code=chips[c].getAttribute('data-c');chips[c].setAttribute('aria-pressed',sel[f].indexOf(code)>-1);}}
function writeHash(){var p=[];if(prefs.len!=='met')p.push('len='+prefs.len);if(prefs.slope!=='ratio')p.push('slope='+prefs.slope);
 ['pop','icf','need'].forEach(function(f){if(sel[f].length)p.push(f+'='+sel[f].join(','));});if(onlySpec)p.push('spec=1');
 try{history.replaceState(null,'',p.length?'#'+p.join('&'):location.pathname+location.search);}catch(e){}
 try{localStorage.setItem('gb-units',JSON.stringify(prefs));}catch(e){}}
function readHash(){try{var s=JSON.parse(localStorage.getItem('gb-units')||'null');if(s){prefs.len=s.len||prefs.len;prefs.slope=s.slope||prefs.slope;}}catch(e){}
 var h=location.hash.replace(/^#/,'');if(!h)return;h.split('&').forEach(function(kv){var a=kv.split('='),k=a[0],v=a[1]||'';
  if(k==='len'||k==='slope')prefs[k]=v;else if(k==='pop'||k==='icf'||k==='need')sel[k]=v?v.split(','):[];else if(k==='spec')onlySpec=v==='1';});}
document.addEventListener('click',function(ev){var t=ev.target.closest('button');if(!t)return;
 if(t.hasAttribute('data-u')){prefs[t.getAttribute('data-u')]=t.getAttribute('data-m');renderUnits();writeHash();}
 else if(t.classList.contains('fchip')){var f=t.getAttribute('data-f'),c=t.getAttribute('data-c'),i=sel[f].indexOf(c);if(i>-1)sel[f].splice(i,1);else sel[f].push(c);applyFilter();writeHash();}
 else if(t.id==='clear'){sel={pop:[],icf:[],need:[]};applyFilter();writeHash();}
 else if(t.id==='expand'||t.id==='collapse'){var d=document.querySelectorAll('#jlist details:not(.hidden)');for(var i2=0;i2<d.length;i2++)d[i2].open=(t.id==='expand');}
 else if(t.id==='vt'||t.id==='vq'){var q=t.id==='vq';document.body.classList.toggle('q',q);document.getElementById('vt').classList.toggle('on',!q);document.getElementById('vq').classList.toggle('on',q);}});
document.getElementById('onlyspec').addEventListener('change',function(e){onlySpec=e.target.checked;applyFilter();writeHash();});
document.getElementById('hidenone').addEventListener('change',applyFilter);
readHash();document.getElementById('onlyspec').checked=onlySpec;renderUnits();applyFilter();
})();
</script>
</body>
</html>
"""


def main():
    if len(sys.argv) < 2:
        print("Usage: spec_page_v2.py <ITEM> [--output PATH]", file=sys.stderr)
        sys.exit(2)
    item = sys.argv[1]
    out = OUT_DIR / f"{item.lower()}.html"
    if "--output" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--output") + 1])
    try:
        d = load(item)
    except ContractError as e:
        print(f"CONTRACT ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    html = build(d)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Generated {out} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
