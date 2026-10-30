#!/usr/bin/env python3
"""
scripts/generate/spec_page_v3.py — specification page generator, built on the site design system.

Renders one specification page into the site's own design language (assets/guidebook.css; exemplar
specs/e-08.html): two typefaces, the 8-step type scale, numbered coloured sections, a hero value card.
Reuses the data loading, unit tokens and APA formatting of spec_page_v2.py.

Inputs (read-only): data/guidebook.db + data/spec_pages/<ITEM>.json + data/question-headings.yaml
Output: specs/<item>.html (next to the e-08 exemplar, so ../assets/guidebook.css resolves)

Scope: only the major identified jurisdictions (SCOPE below) are shown; other data stays staged.

Usage:  python3 scripts/generate/spec_page_v3.py E-03
"""
import json
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import spec_page_v2 as v2  # noqa: E402
from spec_page_v2 import ContractError, JURISDICTION_NAMES, REPO, TOKEN, apa, apa_authors, load, load_question, rt  # noqa: E402

OUT_DIR = REPO / "specs"

# Major identified jurisdictions (workplan/workplan-jurisdiction-sweep.md: P1 + P2 + P3), in display order.
SCOPE = ["US", "UK", "AU", "CA", "DE", "NO", "SE", "ISO", "EU",
         "FR", "CH", "NL", "DK", "FI", "BE", "IE", "ES", "IT", "PT",
         "JP", "SG", "NZ", "KR", "CN"]

MARK = {  # verification level -> (symbol, plain label)
    "primary": ("●", "primary source read"),
    "official-excerpt": ("●", "official excerpt"),
    "secondary": ("○", "secondary sources"),
    "library-title-only": ("○", "library title only"),
    "project-extraction": ("○", "earlier extraction"),
    "values-not-retrieved": ("○", "values not retrieved"),
}

SECTIONS = [  # id, colour, nav label, tag, heading
    ("answers", "blue", "Answers", "Answers", "What to specify"),
    ("why", "oxblood", "Why it matters", "Why it matters", "Why slope matters"),
    ("jurisdictions", "fern", "Jurisdictions", "Jurisdictions", "What each jurisdiction requires"),
    ("evidence", "plum", "Evidence", "Evidence", "What the research says"),
    ("gaps", "terra", "Gaps", "Gaps", "What is still unknown"),
    ("provenance", "slate", "Provenance", "Provenance", "How this page was built"),
]


def build(d):
    page, item = d["page"], d["item"]
    code, title = item["item_code"], item["name"]
    short = title.split(" (")[0]
    question = load_question(code) or short
    facets = {"pop": set(), "icf": set(), "need": set()}

    def tagattrs(pops, icf, needs, scope):
        facets["pop"].update(pops)
        facets["icf"].update(icf)
        facets["need"].update(needs)
        return f'data-scope="{scope}" data-pop="{" ".join(pops)}" data-icf="{" ".join(icf)}" data-need="{" ".join(needs)}"'

    # ---- citations
    cited = {}

    def page_href(c):
        f = f"{c.lower()}.html"
        if (OUT_DIR / f).exists():
            return f
        if (REPO / "site" / "specs" / f).exists():
            return f"../site/specs/{f}"
        return None

    def cite_btn(ref):
        if ref not in cited:
            sx = d["src"](ref)
            label, html, complete = apa(sx)
            pages = [{"item": r[0], "name": r[1], "href": page_href(r[0])} for r in d["db"].execute(
                """SELECT DISTINCT i.item_code, i.name FROM source_slug_links l JOIN items i ON i.bpc_source_slug = l.slug
                   WHERE l.ref_id = ? ORDER BY i.item_code""", (ref,))]
            if code not in {p["item"] for p in pages}:
                pages.insert(0, {"item": code, "name": title, "href": None})
            cited[ref] = {"label": label, "apa": html, "complete": complete, "tier": sx["tier"], "type": sx["evidence_type"],
                          "status": sx["verification_status"], "pages": pages}
        return f'<button type="button" class="cite" data-ref="{escape(ref)}" aria-haspopup="dialog">({escape(cited[ref]["label"])})</button>'

    def cited_on(ref):
        cite_btn(ref)
        links = []
        for p in cited[ref]["pages"]:
            if p["item"] == code:
                links.append("<b>this page</b>")
            elif p["href"]:
                links.append(f'<a href="{escape(p["href"])}">{escape(p["item"])}</a>')
            else:
                links.append(escape(p["item"]))
        return f'<p class="meta">Cited on: {", ".join(links)}</p>'

    # ---- 1. answers
    def value_row(r, scope):
        pops, icf, needs = r.get("populations", []), r.get("icf", []), r.get("needs", [])
        tags = ""
        if scope == "group":
            tags = ('<p class="meta">' + " &middot; ".join(
                [escape(d["pops"].get(p, p)) for p in pops] + [escape(d["needs"].get(n, n)) for n in needs]) + "</p>")
        refs = ('<p class="meta">Sources: ' + " ".join(cite_btn(x) for x in r["refs"]) + "</p>") if r.get("refs") else ""
        return (f'<details class="vrow fi" {tagattrs(pops, icf, needs, scope)}>'
                f'<summary><span class="vwho">{escape(r["who"])}</span><span class="vans">{rt(r["statement"])}</span></summary>'
                f'<div class="body"><p>{rt(r["basis"])}</p>{refs}{tags}</div></details>')

    v = {k: [r for r in rows if r["status"] != "no-evidence"] for k, rows in page["values"].items()}
    answers = "".join(
        f'<p class="grp">{label}</p>' + "".join(value_row(r, scope) for r in v[scope])
        for scope, label in (("universal", "Everyone"), ("group", "Specific groups"), ("person", "One person")) if v[scope])

    # ---- 2. why it matters
    why = "".join(f'<li>{rt(w["text"])}{" " + " ".join(cite_btn(r) for r in w.get("refs", []))}</li>'
                  for w in page["why_it_matters"])

    # ---- 3. jurisdictions (major identified countries only)
    by_code = {j["code"]: j for j in page["jurisdictions"] if j["code"] in SCOPE}
    have = [c for c in SCOPE if c in by_code]
    none = [c for c in SCOPE if c not in by_code]

    def cell(code_, label, text):
        if not text:
            return f'<td data-l="{label}" class="nil">&ndash;</td>'
        return f'<td data-l="{label}"><button type="button" class="mval" data-code="{code_}" aria-haspopup="dialog">{rt(text)}</button></td>'

    gb = page.get("guidebook_row")
    master = ""
    if gb:
        master += (f'<tbody class="mg gb"><tr><th scope="row">Guidebook</th>{cell("", "Preferred", gb.get("preferred")).replace(" data-code=\"\"", "")}'
                   f'{cell("", "Maximum", gb.get("max")).replace(" data-code=\"\"", "")}<td data-l="Between landings" class="nil">&ndash;</td></tr>'
                   f'<tr class="std"><td colspan="4"><i>{escape(gb.get("note", "Working position for this item; provisional"))}</i></td></tr></tbody>')
    for c in have:
        j = by_code[c]
        m = j.get("master") or {"preferred": None, "max": j["headline"], "landing_limit": None, "sort": None}
        sym, lab = MARK[j["level"]]
        key = "" if m.get("sort") is None else m["sort"]
        master += (f'<tbody class="mg" data-sort="{key}"><tr><th scope="row">{escape(JURISDICTION_NAMES.get(c, c))}</th>'
                   f'{cell(c, "Preferred", m.get("preferred"))}{cell(c, "Maximum", m.get("max"))}{cell(c, "Between landings", m.get("landing_limit"))}</tr>'
                   f'<tr class="std"><td colspan="4"><i>{escape(j["standard"])}, {escape(j["edition"])}</i> &middot; <span title="{escape(lab)}">{sym} {escape(lab)}</span></td></tr></tbody>')

    def jur_entry(j):
        sym, lab = MARK[j["level"]]
        needs = sorted({n for p in j["provisions"] for n in p[2]})
        facets["need"].update(needs)
        rows = "".join(f'<div class="prov" data-need="{" ".join(p[2])}"><dt>{escape(p[0])}</dt><dd>{rt(p[1])}</dd></div>' for p in j["provisions"])
        srcs = "".join(f'<li><a href="{escape(s["url"])}" target="_blank" rel="noopener">{escape(s["label"])}</a></li>' for s in j["sources"])
        lib = "".join(f"<li>{cite_btn(r)}</li>" for r in j["kb_refs"])
        return (f'<details class="jx fi" id="j-{j["code"]}" data-scope="universal" data-pop="" data-icf="" data-need="{" ".join(needs)}">'
                f'<summary><span class="jn">{escape(JURISDICTION_NAMES.get(j["code"], j["code"]))}</span>'
                f'<span class="jv">{rt(j["headline"])}</span><span class="jm" title="{escape(lab)}">{sym} {escape(lab)}</span></summary>'
                f'<div class="body"><p class="std"><i>{escape(j["standard"])}</i>, {escape(j["clause"])}, {escape(j["edition"])}</p>'
                f'<dl class="provs">{rows}</dl>'
                f'<h4 class="lbl">Compared with the Guidebook position</h4><p>{rt(j["vs_guidebook"])}</p>'
                f'<h4 class="lbl">What was read</h4><p>{rt(j["read"])}</p>'
                + (f'<h4 class="lbl">Open</h4><p>{rt(j["open"])}</p>' if j.get("open") else "")
                + (f'<h4 class="lbl">In the library</h4><ul>{lib}</ul>' if lib else "")
                + (f'<h4 class="lbl">Links</h4><ul>{srcs}</ul>' if srcs else "")
                + "</div></details>")

    entries = "".join(jur_entry(by_code[c]) for c in have)
    pending = ""
    if none:
        pending = (f'<details class="pending"><summary>{len(none)} major jurisdictions not yet read</summary>'
                   f'<p>{", ".join(escape(JURISDICTION_NAMES.get(c, c)) for c in none)}.</p></details>')

    # ---- 4. evidence, alphabetical by first author's last name (organisation name for corporate authors)
    ev = []
    for e in page["evidence"]:
        s = d["src"](e["ref"])
        ev.append((apa_authors(s)[0].lower(), s["pub_year"] or 0, e, s))
    ev.sort(key=lambda t: (t[0], t[1]))
    ev_html = []
    for _, _, e, s in ev:
        subj = [x["population_code"] for x in s["subject"] if x["population_code"] != "ALL"]
        tag = tagattrs(subj, s["icf"], s["needs"], "group" if subj else "universal")
        ev_html.append(
            f'<details class="evr fi" {tag}><summary><span class="apa">{apa(s)[1]}</span></summary>'
            f'<div class="body"><p>{rt(e["relevance"])}</p><p>{cite_btn(e["ref"])}</p>{cited_on(e["ref"])}'
            f'<p class="meta">Tier {s["tier"]} &middot; {escape(s["evidence_type"] or "")} &middot; {escape(s["verification_status"] or "")}'
            + (f' &middot; <a href="https://doi.org/{escape(s["doi"])}" target="_blank" rel="noopener">doi:{escape(s["doi"])}</a>' if s["doi"] else "")
            + "</p></div></details>")

    # ---- 5. gaps
    gaps = "".join(
        f'<details class="gp"><summary><span class="vwho">{escape(g["gap_id"])}</span><span class="vans">{escape((g["description"] or "")[:110])}&hellip;</span></summary>'
        f'<div class="body"><p>{escape(g["description"] or "")}</p><p class="meta">{escape(g["status"])}</p></div></details>'
        for g in d["gaps"])

    # ---- facets (only codes that occur on the page)
    def chip(kind, c, label):
        return f'<button type="button" class="fchip" data-f="{kind}" data-c="{escape(c)}" aria-pressed="false">{label}</button>'

    def facet(kind, codes, table, group_of=None, group_names=None, show_code=True):
        def lab(c):
            n = table[c]
            n = n[:1].upper() + n[1:] if kind == "pop" else n
            return (f"{escape(c)} {escape(n)}" if show_code else escape(n))
        if not group_of:
            return "".join(chip(kind, c, lab(c)) for c in sorted(codes))
        groups = {}
        for c in sorted(codes):
            groups.setdefault(group_of(c), []).append(c)
        return "".join(f'<span class="fgl">{escape((group_names or {}).get(g, g))}</span>' + "".join(chip(kind, c, lab(c)) for c in cs)
                       for g, cs in sorted(groups.items(), key=lambda kv: str(kv[0])))

    pop_f = facet("pop", {p for p in facets["pop"] if p != "ALL"}, d["pops"], lambda c: d["pop_cat"].get(c, "other"),
                  {"mobility": "Mobility", "neurological": "Neurological", "pain_fatigue": "Pain and fatigue", "sensory": "Sensory",
                   "cognitive": "Cognitive", "developmental": "Developmental", "mental_health": "Mental health", "other": "Other"})
    icf_f = facet("icf", facets["icf"], d["icf"], lambda c: c[:1],
                  {"b": "Body functions", "d": "Activities and participation", "s": "Body structures", "e": "Environment"})
    need_f = facet("need", facets["need"], d["needs"], show_code=False)

    # ---- hero
    pos = next((TOKEN.search(r["statement"]) for r in page["values"].get("universal", []) if TOKEN.search(r["statement"])), None)
    hero_val = rt(pos.group(0)) if pos else ""
    tagline = rt(page["_meta"].get("tagline", ""))

    # ---- assemble
    def section(sid, body, count_note=""):
        _, _, _, tag, head = next(x for x in SECTIONS if x[0] == sid)
        n = [x[0] for x in SECTIONS].index(sid) + 1
        meta = f'<span class="sec-meta">{count_note}</span>' if count_note else ""
        return (f'<section class="section" id="{sid}"><h2><span class="n">{n}</span>{head}{meta}</h2>{body}</section>')

    jur_body = (
        '<p class="lead">One row per jurisdiction. Select a value for its detail.</p>'
        '<div class="cmp-wrap"><table class="cmp" id="master"><thead><tr><th scope="col">Jurisdiction</th><th scope="col">Preferred</th>'
        '<th scope="col"><button type="button" id="msort" class="msort" aria-label="Sort by maximum gradient, steepest first">Maximum &#8645;</button></th>'
        f'<th scope="col">Between landings</th></tr></thead>{master}</table></div>'
        f'{pending}<p class="grp">Full entries</p>{entries}')
    secs = [
        section("answers", answers),
        section("why", f'<ul class="why">{why}</ul>'),
        section("jurisdictions", jur_body, f"{len(have)} of {len(SCOPE)} read"),
        section("evidence", f'<div id="evlist">{"".join(ev_html)}</div>', f"{len(ev_html)} sources"),
    ]
    if gaps:
        secs.append(section("gaps", gaps))
    prov = (f'<p>{escape(page["_meta"]["status"])}</p>'
            f'<p class="meta">Database schema v{d["user_version"]} &middot; generated {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")} '
            f'&middot; evidence base <code>{escape(item["bpc_source_slug"])}</code> &middot; prepared by {escape(page["_meta"]["prepared_by"])}</p>'
            '<p class="meta">Population, ICF and access-need codes and tags are provisional and unreviewed. Each jurisdiction figure is marked '
            '&#9679; primary source read or &#9675; not read from a primary source.</p>')
    secs.append(section("provenance", prov))
    present = {s.split('id="')[1].split('"')[0] for s in secs}
    nav = "".join(f'<li><a href="#{s[0]}" data-snav="{s[0]}"><span class="snc-n">{i + 1}</span>{s[2]}</a></li>'
                  for i, s in enumerate(SECTIONS) if s[0] in present)

    out = TEMPLATE
    for k, val in {
        "__TITLE__": escape(short), "__CODE__": escape(code), "__QUESTION__": escape(question), "__TAGLINE__": tagline,
        "__HERO__": hero_val, "__NAV__": nav, "__SECTIONS__": "".join(secs),
        "__POPF__": pop_f, "__ICFF__": icf_f, "__NEEDF__": need_f,
        "__CITES__": json.dumps(cited, ensure_ascii=False).replace("</", "<\\/"),
    }.items():
        out = out.replace(k, val)
    return out


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__CODE__ __TITLE__ &mdash; Guidebook</title>
<meta name="description" content="Specification __CODE__: __TITLE__.">
<style>
:root{--bg:#fff;--ink:#16181d;--ink2:#3b4048;--muted:#5d6570;--rule:#d9dce1;--soft:#f3f4f6;--accent:#1a4fa3;
 --f:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
 --s1:32px;--s2:24px;--s3:18px;--s4:16px;--s5:14px;--r:4px}
@media (prefers-color-scheme:dark){:root{--bg:#14161a;--ink:#eceef2;--ink2:#c7ccd4;--muted:#9aa2ad;--rule:#2e3239;--soft:#1d2026;--accent:#8db8ff}}
*{box-sizing:border-box}[hidden]{display:none!important}
body{margin:0;background:var(--bg);color:var(--ink);font:400 var(--s4)/1.55 var(--f);font-variant-numeric:tabular-nums}
a{color:var(--accent);overflow-wrap:anywhere}code{font:inherit}.apa,.apa-full,.body{overflow-wrap:anywhere}input,select,button{font-family:inherit}
.wrap{max-width:960px;margin:0 auto;padding:0 20px}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:var(--bg);padding:8px;z-index:20}
.top{border-bottom:1px solid var(--rule);font-size:var(--s5)}.top .wrap{display:flex;gap:6px 20px;align-items:baseline;flex-wrap:wrap;padding-top:10px;padding-bottom:10px}
.top .brand{font-weight:700;color:var(--ink);text-decoration:none;font-size:var(--s4)}.top nav{color:var(--muted)}.top nav a{color:var(--muted)}
.sectnav{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--rule)}
.sectnav ol{display:flex;list-style:none;margin:0 auto;padding:0 12px;max-width:960px;overflow-x:auto;gap:2px}
.sectnav a{display:block;padding:11px 10px 9px;font-size:var(--s5);font-weight:600;color:var(--muted);text-decoration:none;white-space:nowrap;border-bottom:3px solid transparent}
.sectnav a:hover{color:var(--ink)}.sectnav a[aria-current=true]{color:var(--ink);border-bottom-color:var(--ink)}.snc-n{font-weight:400;margin-right:6px}
.page{padding-top:28px;padding-bottom:80px}
.kicker{margin:0 0 6px;font-size:var(--s5);color:var(--muted)}
h1{margin:0;font-size:var(--s1);line-height:1.15;font-weight:700}.q{margin:6px 0 0;font-size:var(--s3);color:var(--ink2)}
.tagline{margin:14px 0 0;font-size:var(--s4);color:var(--ink2);max-width:62ch}
.hero{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;margin:20px 0 4px;padding:14px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.hl{font-size:var(--s5);color:var(--muted)}.hv{font-size:var(--s1);font-weight:700;line-height:1}
.section{margin:0}h2{display:flex;align-items:baseline;gap:12px;margin:56px 0 16px;padding-top:12px;border-top:3px solid var(--ink);font-size:var(--s2);line-height:1.2;font-weight:700;scroll-margin-top:56px}
h2 .n{font-weight:400;color:var(--muted)}.sec-meta{margin-left:auto;font-size:var(--s5);font-weight:400;color:var(--muted)}
h3{margin:0 0 12px;font-size:var(--s3)}
p{margin:0 0 10px}
.lead{font-size:var(--s3);color:var(--ink2);margin:0 0 14px}
.meta{font-size:var(--s5);color:var(--muted)}
.grp,.lbl{font-size:var(--s5);font-weight:600;color:var(--muted);margin:26px 0 6px}.lbl{margin:16px 0 4px}
details{border-top:1px solid var(--rule)}details:last-of-type{border-bottom:1px solid var(--rule)}
summary{cursor:pointer;list-style:none;padding:12px 8px 12px 26px;position:relative;min-height:44px}
summary::-webkit-details-marker{display:none}summary::before{content:"\25B8";position:absolute;left:6px;color:var(--muted)}
details[open]>summary::before{content:"\25BE"}summary:hover{background:var(--soft)}
a:focus-visible,button:focus-visible,summary:focus-visible,select:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.body{padding:2px 8px 16px 26px;max-width:70ch}.body p{margin:0 0 10px}.body ul{margin:0 0 10px;padding-left:20px}
.vrow>summary,.gp>summary{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2fr);gap:4px 24px;align-items:baseline}
.vwho{color:var(--ink2)}.vans{font-size:var(--s3);font-weight:700;line-height:1.3}.gp .vans{font-size:var(--s4);font-weight:400}
.why{padding-left:20px;max-width:66ch;margin:0}.why li{margin:0 0 14px;font-size:var(--s3);line-height:1.5}
.cite,.mval,.msort,.clr{font:inherit;color:inherit;background:none;border:0;border-bottom:1px dotted var(--muted);padding:0;cursor:pointer;text-align:left}
.cite{color:var(--accent);border-bottom-color:var(--accent)}.mval{font-weight:700}.msort{font-weight:600;color:var(--muted)}
.cite:hover,.mval:hover,.msort:hover,.clr:hover{background:var(--soft)}
.cmp-wrap{overflow-x:auto;margin:0 0 20px}
table.cmp{border-collapse:collapse;width:100%}
table.cmp thead th{font-size:var(--s5);font-weight:600;color:var(--muted);text-align:left;padding:8px 14px 8px 0;border-bottom:2px solid var(--ink)}
table.cmp tbody tr:first-child>*{padding:12px 14px 2px 0;vertical-align:top;text-align:left}
table.cmp th[scope=row]{font-weight:700;white-space:nowrap}
table.cmp .std td{padding:0 14px 12px 0;font-size:var(--s5);color:var(--muted);border-bottom:1px solid var(--rule)}
table.cmp .nil{color:var(--muted)}
table.cmp .gb th,table.cmp .gb td{background:var(--soft)}
.pending{border:0}.pending p{padding-left:26px;margin:0 0 12px}
.jx>summary{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2fr) auto;gap:4px 24px;align-items:baseline}
.jn{font-weight:700}.jv{font-weight:600}.jm{font-size:var(--s5);color:var(--muted)}
.std{font-size:var(--s5);color:var(--ink2)}
dl.provs{margin:0 0 8px}.prov{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2.2fr);gap:2px 24px;padding:6px 0;border-top:1px solid var(--rule)}
.prov dt{font-weight:600}.prov dd{margin:0}.prov.hit{box-shadow:inset 3px 0 0 var(--accent);padding-left:10px}.prov.dim{opacity:.5}
.evr .apa{display:block}
.fi.hidden{display:none}.fi.hit>summary{box-shadow:inset 3px 0 0 var(--accent)}
.evgrp{font-size:var(--s5);font-weight:600;color:var(--muted);margin:24px 0 6px}
.bar{margin:20px 0 0;padding:4px 0;border-bottom:1px solid var(--rule)}
.brow{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center;padding:4px 0}
.tl{font-size:var(--s5);font-weight:600;color:var(--muted);width:76px;flex:0 0 auto}
.sel-l{font-size:var(--s5);color:var(--ink2);display:inline-flex;align-items:center;gap:6px}
.sel{font-size:var(--s5);padding:4px 8px;min-height:36px;border:1px solid var(--rule);background:var(--bg);color:var(--ink);border-radius:var(--r)}
.seg{display:inline-flex;flex-wrap:wrap}.seg button{font-size:var(--s5);padding:4px 12px;min-height:36px;background:var(--bg);color:var(--ink);border:1px solid var(--rule);margin:0 -1px 0 0;cursor:pointer}
.seg button:first-child{border-radius:var(--r) 0 0 var(--r)}.seg button:last-child{border-radius:0 var(--r) var(--r) 0}
.seg button:hover,.fchip:hover{background:var(--soft)}
.seg button[aria-pressed=true],.fchip[aria-pressed=true],.fchip.act{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.pills{padding:2px 0 8px 88px}.pg{display:flex;flex-wrap:wrap;gap:4px 6px;align-items:center}.pg[hidden]{display:none}
.fgl{font-size:var(--s5);font-weight:600;color:var(--muted);margin:0 2px 0 8px}
.fchip{font-size:var(--s5);padding:2px 10px;min-height:32px;background:var(--bg);color:var(--ink);border:1px solid var(--rule);border-radius:var(--r);cursor:pointer}
.fcount{font-size:var(--s5);opacity:.7;margin-left:6px}
.applied{display:inline-flex;flex-wrap:wrap;gap:4px}.clr{font-size:var(--s5)}
.only{font-size:var(--s5);color:var(--ink2);padding-left:88px}
.dact{display:flex;justify-content:flex-end;gap:8px;margin-top:12px}.dact button{font-size:var(--s5);padding:8px 16px;min-height:40px;background:var(--bg);color:var(--ink);border:1px solid var(--ink);border-radius:var(--r);cursor:pointer}
.dact button:hover{background:var(--soft)}
dialog{max-width:min(680px,94vw);width:100%;border:2px solid var(--ink);border-radius:var(--r);background:var(--bg);color:var(--ink);padding:20px 24px}
dialog::backdrop{background:rgba(0,0,0,.5)}dialog h3{margin:0 0 12px}dialog .jd{max-height:60vh;overflow:auto;font-size:var(--s5)}
dialog .apa-full{padding-left:2em;text-indent:-2em;margin:0 0 12px}
@media (max-width:640px){
 .wrap{padding:0 16px}h1{font-size:var(--s2)}.hv{font-size:var(--s2)}
 .vrow>summary,.gp>summary,.jx>summary,.prov{grid-template-columns:minmax(0,1fr)}
 table.cmp thead{display:none}
 table.cmp tbody tr:first-child{display:grid;grid-template-columns:1fr 1fr;gap:2px 12px;padding:12px 0 0}
 table.cmp tbody tr:first-child>th{grid-column:1/-1;padding:0}
 table.cmp tbody tr:first-child>td{padding:0 0 4px}
 table.cmp tbody tr:first-child>td::before{content:attr(data-l);display:block;font-size:var(--s5);color:var(--muted)}
 table.cmp tr.std td{padding-bottom:12px}
 table.cmp td.nil{display:none}
 .seg button,.fchip,.sel{min-height:44px}.tl{width:auto;min-width:64px}.pills,.only{padding-left:0}
}
@media print{.bar,.sectnav,.top{display:none}details{display:block}summary::before{content:""}}
</style>
</head>
<body class="mode-spec">
<a href="#main" class="skip">Skip to main content</a>
<header class="top"><div class="wrap"><a href="../index.html" class="brand">Guidebook</a>
 <nav aria-label="Breadcrumb"><a href="../index.html">Browse</a> / <a href="../index.html#exemplar">Specifications</a> / __CODE__</nav></div></header>
<nav class="sectnav" aria-label="Sections of this specification"><ol>__NAV__</ol></nav>

<main id="main" class="wrap page">
 <header>
  <p class="kicker">__CODE__ &middot; Specification &middot; Provisional</p>
  <h1>__TITLE__</h1>
  <p class="q">__QUESTION__</p>
  <p class="tagline">__TAGLINE__</p>
  <div class="hero"><span class="hl">Guidebook working position</span><span class="hv">__HERO__</span></div>
 </header>

 <div class="bar" id="tools" aria-label="Units and filters">
  <div class="brow"><span class="tl">Units</span>
   <label class="sel-l">Length <select class="sel" data-u="len" aria-label="Length units"><option value="met">Metric</option><option value="imp">Imperial</option><option value="stated">As stated</option></select></label>
   <label class="sel-l">Slope <select class="sel" data-u="slope" aria-label="Slope units"><option value="ratio">Ratio 1:n</option><option value="pct">Percent</option><option value="deg">Degrees</option><option value="stated">As stated</option></select></label></div>
  <div class="brow"><span class="tl">Filter by</span>
   <span class="seg" role="group" aria-label="Filter lens"><button type="button" data-lens="pop" aria-pressed="false">Who it's for</button><button type="button" data-lens="icf" aria-pressed="false">ICF code</button><button type="button" data-lens="need" aria-pressed="false">Access need</button></span>
   <span class="applied" id="activelist"></span><button type="button" class="clr" id="clear" hidden>Clear</button><span class="meta" id="count" role="status" aria-live="polite"></span></div>
  <div class="brow pills" id="pillrow" hidden>
   <div class="pg" data-lens="pop" hidden>__POPF__</div><div class="pg" data-lens="icf" hidden>__ICFF__</div><div class="pg" data-lens="need" hidden>__NEEDF__</div></div>
  <label class="brow only" id="onlyrow" hidden><input type="checkbox" id="onlyspec"> Hide general (everyone) answers while filtering</label>
 </div>

 __SECTIONS__
</main>

<dialog id="jdlg" aria-labelledby="jdlg-t"><div id="jdlg-body"></div><div class="dact"><button type="button" id="jdlg-full">Open full entry</button><button type="button" id="jdlg-close">Close</button></div></dialog>
<dialog id="cdlg" aria-labelledby="cdlg-t"><div id="cdlg-body"></div><div class="dact"><button type="button" id="cdlg-close">Close</button></div></dialog>
<script type="application/json" id="cites">__CITES__</script>
<script>
(function(){
var prefs={len:'met',slope:'ratio'},sel={pop:[],icf:[],need:[]},onlySpec=false,lens='';
var LBL={pop:"Who it's for",icf:'ICF code',need:'Access need'};
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
 var b=document.querySelectorAll('select[data-u]');for(var j=0;j<b.length;j++){b[j].value=prefs[b[j].getAttribute('data-u')];}}
function toks(el,a){var s=el.getAttribute(a)||'';return s?s.split(' '):[];}
function inter(a,b){for(var i=0;i<a.length;i++)if(b.indexOf(a[i])>-1)return true;return false;}
function applyFilter(){
 var active=['pop','icf','need'].filter(function(f){return sel[f].length>0;});
 var items=document.querySelectorAll('.fi'),shown={v:0,e:0},tot={v:0,e:0};
 for(var i=0;i<items.length;i++){var el=items[i],scope=el.getAttribute('data-scope'),isJ=el.classList.contains('jx'),kind=el.classList.contains('vrow')?'v':'e';
  var hit=active.length>0&&active.every(function(f){return inter(toks(el,'data-'+f),sel[f]);});
  var show=true;
  if(!isJ&&active.length>0){ if(scope==='group')show=hit; else show=!onlySpec; }
  if(!isJ){tot[kind]++;if(show)shown[kind]++;}
  el.classList.toggle('hidden',!show);el.classList.toggle('hit',active.length>0&&hit&&show);
  if(isJ){var ps=el.querySelectorAll('.prov');for(var p=0;p<ps.length;p++){var h=sel.need.length>0&&inter(toks(ps[p],'data-need'),sel.need);ps[p].classList.toggle('hit',h);ps[p].classList.toggle('dim',sel.need.length>0&&!h);}}}
 document.getElementById('count').textContent=active.length?'Showing '+shown.v+' of '+tot.v+' answers and '+shown.e+' of '+tot.e+' studies.':'';
 var al=document.getElementById('activelist');al.innerHTML='';var any=false;
 ['pop','icf','need'].forEach(function(f){sel[f].forEach(function(c){any=true;var bt=document.createElement('button');bt.type='button';bt.className='fchip act';bt.setAttribute('data-f',f);bt.setAttribute('data-c',c);
   bt.setAttribute('aria-label','Remove filter '+LBL[f]+' '+c);bt.textContent=c+' ×';al.appendChild(bt);});});
 regroup();
 document.getElementById('clear').hidden=!any;document.getElementById('onlyrow').hidden=!any;
 var chips=document.querySelectorAll('.pg .fchip');for(var c2=0;c2<chips.length;c2++){var f2=chips[c2].getAttribute('data-f'),code=chips[c2].getAttribute('data-c');chips[c2].setAttribute('aria-pressed',sel[f2].indexOf(code)>-1);}}
function addCounts(){var chips=document.querySelectorAll('.pg .fchip'),its=document.querySelectorAll('.vrow,.evr');
 for(var i=0;i<chips.length;i++){var f=chips[i].getAttribute('data-f'),c=chips[i].getAttribute('data-c'),n=0;for(var k=0;k<its.length;k++){if(toks(its[k],'data-'+f).indexOf(c)>-1)n++;}
  var s=document.createElement('span');s.className='fcount';s.textContent=n;chips[i].appendChild(s);}}
function writeHash(){var p=[];if(prefs.len!=='met')p.push('len='+prefs.len);if(prefs.slope!=='ratio')p.push('slope='+prefs.slope);
 ['pop','icf','need'].forEach(function(f){if(sel[f].length)p.push(f+'='+sel[f].join(','));});if(onlySpec)p.push('spec=1');if(lens)p.push('lens='+lens);
 try{history.replaceState(null,'',p.length?'#'+p.join('&'):location.pathname+location.search);}catch(e){}
 try{localStorage.setItem('gb-units',JSON.stringify(prefs));}catch(e){}}
function readHash(){try{var s=JSON.parse(localStorage.getItem('gb-units')||'null');if(s){prefs.len=s.len||prefs.len;prefs.slope=s.slope||prefs.slope;}}catch(e){}
 var h=location.hash.replace(/^#/,'');if(!h||h.indexOf('=')<0)return;h.split('&').forEach(function(kv){var a=kv.split('='),k=a[0],v=a[1]||'';
  if(k==='len'||k==='slope')prefs[k]=v;else if(k==='pop'||k==='icf'||k==='need')sel[k]=v?v.split(','):[];else if(k==='spec')onlySpec=v==='1';else if(k==='lens')lens=v;});}
var CITES=null;function cites(){if(CITES===null){try{CITES=JSON.parse(document.getElementById('cites').textContent);}catch(e){CITES={};}}return CITES;}
function esc(t){return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;');}
function openCite(ref){var c=cites()[ref];if(!c)return;var here=location.pathname.split('/').pop().replace('.html','').toUpperCase();
 var pg=c.pages.map(function(p){var lab=p.item===here?'<b>'+p.item+'</b> (this page)':(p.href?'<a href="'+p.href+'">'+p.item+'</a>':p.item);return '<li>'+lab+' &mdash; '+esc(p.name)+'</li>';}).join('');
 document.getElementById('cdlg-body').innerHTML='<h3 id="cdlg-t">Citation</h3><p class="apa-full">'+c.apa+'</p>'
  +'<p class="meta">Tier '+c.tier+' &middot; '+esc(c.type||'')+' &middot; '+esc(c.status||'')+(c.complete?'':' &middot; author list incomplete in the library')+'</p>'
  +'<p class="lbl">Cited on these pages</p><ul>'+pg+'</ul>';
 var dg=document.getElementById('cdlg');if(dg.showModal)dg.showModal();else dg.setAttribute('open','');}
function openJ(code){var src=document.getElementById('j-'+code);if(!src)return;var dg=document.getElementById('jdlg');
 document.getElementById('jdlg-body').innerHTML='<h3 id="jdlg-t">'+src.querySelector('.jn').textContent+'</h3><div class="jd">'+src.querySelector('.body').innerHTML+'</div>';
 dg.setAttribute('data-code',code);renderUnits();if(dg.showModal)dg.showModal();else dg.setAttribute('open','');}
var EVROWS=null;
function regroup(){var box=document.getElementById('evlist');if(!box)return;if(EVROWS===null)EVROWS=[].slice.call(box.querySelectorAll('.evr'));
 box.innerHTML='';
 if(!lens){EVROWS.forEach(function(r){box.appendChild(r);});return;}
 var chips=document.querySelectorAll('.pg[data-lens="'+lens+'"] .fchip'),order=[],names={};
 [].forEach.call(chips,function(c){var k=c.getAttribute('data-c');order.push(k);names[k]=c.firstChild.textContent;});
 var groups={},rest=[];
 EVROWS.forEach(function(r){var codes=toks(r,'data-'+lens),g=null;for(var i=0;i<order.length;i++){if(codes.indexOf(order[i])>-1){g=order[i];break;}}
  if(g===null)rest.push(r);else(groups[g]=groups[g]||[]).push(r);});
 order.forEach(function(c){if(groups[c]){var h=document.createElement('p');h.className='evgrp';h.textContent=names[c];box.appendChild(h);groups[c].forEach(function(r){box.appendChild(r);});}});
 if(rest.length){var h2=document.createElement('p');h2.className='evgrp';h2.textContent='Not tagged to this lens';box.appendChild(h2);rest.forEach(function(r){box.appendChild(r);});}}
function renderLens(){[].forEach.call(document.querySelectorAll('.pg'),function(g){g.hidden=(g.getAttribute('data-lens')!==lens);});
 document.getElementById('pillrow').hidden=!lens;
 [].forEach.call(document.querySelectorAll('button[data-lens]'),function(b){b.setAttribute('aria-pressed',b.getAttribute('data-lens')===lens);});regroup();}
var dir=0;
function sortMaster(){var t=document.getElementById('master'),gs=[].slice.call(t.querySelectorAll('tbody.mg:not(.gb)'));dir=dir===1?-1:1;
 gs.sort(function(a,b){var x=a.getAttribute('data-sort'),y=b.getAttribute('data-sort');
  if(x===''&&y==='')return a.querySelector('th').textContent.localeCompare(b.querySelector('th').textContent);
  if(x==='')return 1;if(y==='')return -1;var d=(parseFloat(y)-parseFloat(x))*dir;return d||a.querySelector('th').textContent.localeCompare(b.querySelector('th').textContent);});
 gs.forEach(function(g){t.appendChild(g);});}
document.addEventListener('click',function(ev){var t=ev.target.closest('button');if(!t)return;
 if(t.classList.contains('cite')){openCite(t.getAttribute('data-ref'));}
 else if(t.id==='cdlg-close'){document.getElementById('cdlg').close();}
 else if(t.classList.contains('mval')){openJ(t.getAttribute('data-code'));}
 else if(t.id==='jdlg-close'){document.getElementById('jdlg').close();}
 else if(t.id==='jdlg-full'){var dg=document.getElementById('jdlg'),c2=dg.getAttribute('data-code');dg.close();var de=document.getElementById('j-'+c2);if(de){de.open=true;de.scrollIntoView({block:'start'});}}
 else if(t.id==='msort'){sortMaster();}
 else if(t.hasAttribute('data-lens')){var ln=t.getAttribute('data-lens');lens=(lens===ln)?'':ln;renderLens();writeHash();}

 else if(t.classList.contains('fchip')&&t.id!=='clear'){var f=t.getAttribute('data-f'),c=t.getAttribute('data-c'),i=sel[f].indexOf(c);if(i>-1)sel[f].splice(i,1);else sel[f].push(c);applyFilter();writeHash();}
 else if(t.id==='clear'){sel={pop:[],icf:[],need:[]};applyFilter();writeHash();}});
document.addEventListener('change',function(e){var t=e.target;if(t.matches&&t.matches('select[data-u]')){prefs[t.getAttribute('data-u')]=t.value;renderUnits();writeHash();}});
document.getElementById('onlyspec').addEventListener('change',function(e){onlySpec=e.target.checked;applyFilter();writeHash();});
['jdlg','cdlg'].forEach(function(id){document.getElementById(id).addEventListener('click',function(e){if(e.target===this)this.close();});});
if('IntersectionObserver' in window){var links={};[].forEach.call(document.querySelectorAll('[data-snav]'),function(a){links[a.getAttribute('data-snav')]=a;});
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){for(var k in links)links[k].removeAttribute('aria-current');if(links[e.target.id])links[e.target.id].setAttribute('aria-current','true');}});},{rootMargin:'-30% 0px -60% 0px'});
 [].forEach.call(document.querySelectorAll('.section'),function(s){io.observe(s);});}
readHash();document.getElementById('onlyspec').checked=onlySpec;addCounts();renderUnits();applyFilter();renderLens();
})();
</script>
</body>
</html>
"""


def main():
    if len(sys.argv) < 2:
        print("Usage: spec_page_v3.py <ITEM> [--output PATH]", file=sys.stderr)
        sys.exit(2)
    item = sys.argv[1].upper()
    out = Path(sys.argv[sys.argv.index("--output") + 1]) if "--output" in sys.argv else OUT_DIR / f"{item.lower()}.html"
    try:
        d = load(item)
        html = build(d)
    except ContractError as e:
        print(f"CONTRACT ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8", newline="\n")
    print(f"Generated {out} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
