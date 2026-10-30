#!/usr/bin/env python3
"""
scripts/generate/spec_page_v3.py — specification page generator.

Built to audits/spec-page-design-requirements-2026-10-29.md:
  * information first: hero figures, then specification table, jurisdiction comparison table, why it matters,
    evidence (APA, alphabetical, regrouped by the chosen lens), gaps, about;
  * Swiss-style grid: 12 columns, section titles in a left rail, content in the right nine, flush-left,
    one neo-grotesque sans (Helvetica/Arial, no web fonts), five sizes, two weights, black/white/grey, red for
    state only, thin rules, no boxes, tints, tiles or status pills;
  * accessibility (WCAG 2.2 AA minimum): semantic tables with explicit roles and captions, labelled controls,
    aria-pressed/expanded, native details and dialog, live region, skip link, scroll-padding under the sticky nav,
    lang on foreign text, a text equivalent for the drawing, forced-colors and dark-scheme support.

Reuses data loading, unit tokens and APA formatting of spec_page_v2.py.
Inputs (read-only): data/guidebook.db + data/spec_pages/<ITEM>.json + data/question-headings.yaml
Output: specs/<item>.html        Usage: python3 scripts/generate/spec_page_v3.py E-03
Scope: only the major identified jurisdictions (SCOPE) are shown; other data stays staged.
"""
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_page_v2 import (ContractError, JURISDICTION_NAMES, REPO, TOKEN, apa, apa_authors, default_text,  # noqa: E402
                          load, load_question, parse_num as parse_f, rt)

OUT_DIR = REPO / "specs"

# Major identified jurisdictions (workplan/workplan-jurisdiction-sweep.md: P1 + P2 + P3), in display order.
SCOPE = ["US", "UK", "AU", "CA", "DE", "NO", "SE", "ISO", "EU",
         "FR", "CH", "NL", "DK", "FI", "BE", "IE", "ES", "IT", "PT",
         "JP", "SG", "NZ", "KR", "CN"]

READ = {  # verification level -> plain wording (words, never colour or symbols alone)
    "primary": "read from the primary text",
    "official-excerpt": "read from an official excerpt",
    "secondary": "from secondary sources",
    "library-title-only": "library title only",
    "project-extraction": "from an earlier extraction",
    "values-not-retrieved": "values not retrieved",
}

_CJK = re.compile(r"[぀-ヿ㐀-鿿＀-￯]+")


def lw(html, default="zh"):
    """Wrap runs of CJK text in a lang-tagged span (WCAG 3.1.2). Kana implies Japanese; otherwise `default`."""
    def f(m):
        run = m.group(0)
        lang = "ja" if re.search(r"[぀-ヿ]", run) else default
        return f'<span lang="{lang}">{run}</span>'
    return _CJK.sub(f, html)


TYPE_LABEL = {"clinical": "clinical study", "sr_meta": "systematic review", "co1": "lived-experience source",
              "co2": "professional guideline", "standard_eb": "standard", "national_fw": "national framework", "code": "code",
              "grey": "report"}


def tier_label(t):
    d = sorted(set(re.findall(r"T(\d)", t or "")))
    names = {"4": "international standard", "5": "national framework", "6": "legal code"}
    if len(d) == 1:
        return f"{names.get(d[0], 'source')} (tier {d[0]})"
    return "tiers " + " and ".join(d) if d else "tier not recorded"


def clean_title(t):
    """Strip internal curation notes such as '(best-fit Crossref candidate ...)' from a stored title."""
    t = t or ""
    i = t.find("Crossref")
    if i > 0:
        j = t.rfind("(", 0, i)
        t = t[:j] if j > 0 else t
    return t.strip()


def first_sentence(text):
    t = text.strip()
    i = t.find(". ")
    return t if i < 0 else t[:i + 1]


def build(d):
    page, item = d["page"], d["item"]
    code, title = item["item_code"], item["name"]
    short = title.split(" (")[0]
    question = load_question(code) or short
    facets = {"pop": set(), "icf": set(), "need": set()}

    def src(ref):
        s_ = dict(d["src"](ref))
        s_["pub_title"] = clean_title(s_["pub_title"])
        return s_

    def slope_tok(x):
        return "{{slope=%.6f|1:%d}}" % (x, round(1 / x))

    def tok_vals(text):
        return [parse_f(m.group(2)) for m in TOKEN.finditer(text or "") if m.group(1) == "slope"]

    # Best practice is the most accommodating value stated by a current standard (or improved on by evidence).
    # It is NOT the most common or most agreed value.
    scoped = [j for j in page["jurisdictions"] if j["code"] in SCOPE and j.get("master")]
    stated = [(x, j["code"], fld) for j in scoped for fld in ("preferred", "max") for x in tok_vals(j["master"].get(fld))]
    best = min((x for x, _, _ in stated), default=None)
    steepest = max((x for x, _, f in stated if f == "max"), default=None)
    maxima = [(j["code"], j["master"]["sort"]) for j in scoped if j["master"].get("sort")]

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
            sx = src(ref)
            label, html, complete = apa(sx)
            pages = [{"item": r[0], "name": r[1], "href": page_href(r[0])} for r in d["db"].execute(
                """SELECT DISTINCT i.item_code, i.name FROM source_slug_links l JOIN items i ON i.bpc_source_slug = l.slug
                   WHERE l.ref_id = ? ORDER BY i.item_code""", (ref,))]
            if code not in {p["item"] for p in pages}:
                pages.insert(0, {"item": code, "name": title, "href": None})
            cited[ref] = {"label": label, "apa": lw(html), "complete": complete, "tier": sx["tier"], "type": sx["evidence_type"],
                          "type_label": TYPE_LABEL.get(sx["evidence_type"], sx["evidence_type"] or ""),
                          "status": sx["verification_status"],
                          "status_label": "metadata verified" if sx["verification_status"] == "VERIFIED" else "metadata not yet verified",
                          "pages": pages}
        return (f'<button type="button" class="lk cite" data-ref="{escape(ref)}" aria-haspopup="dialog">'
                f'({lw(escape(cited[ref]["label"]))})</button>')

    def cited_on(ref):
        cite_btn(ref)
        links = []
        for p in cited[ref]["pages"]:
            if p["item"] == code:
                links.append("this page")
            elif p["href"]:
                links.append(f'<a href="{escape(p["href"])}">{escape(p["item"])}</a>')
            else:
                links.append(escape(p["item"]))
        return f'Cited on: {", ".join(links)}.'

    # ---- 1. values by group: who / value / basis, each with the project's evidence marker (doctrine: unmarked = error)
    def marker_html(r):
        m = r.get("marker")
        if m == "●":
            return ' <span class="mk"><span aria-hidden="true">●</span> evidence-based</span>'
        if m == "○":
            return ' <span class="mk"><span aria-hidden="true">○</span> inferred</span>'
        return ""

    v = {k: [r for r in rows if r["status"] != "no-evidence"] for k, rows in page["values"].items()}
    rows = []
    for scope in ("universal", "group", "person"):
        for r in v[scope]:
            pops, icf, needs = r.get("populations", []), r.get("icf", []), r.get("needs", [])
            basis = r.get("short") or first_sentence(r["basis"])
            refs = (" " + " ".join(cite_btn(x) for x in r.get("refs", [])[:3])) if r.get("refs") else ""
            rows.append(f'<tr role="row" class="fi vrow" {tagattrs(pops, icf, needs, scope)}>'
                        f'<th role="rowheader" scope="row" data-l="Who">{escape(r["who"])}</th>'
                        f'<td role="cell" class="val" data-l="Value">{rt(r["statement"])}</td>'
                        f'<td role="cell" data-l="Basis">{rt(basis)}{refs}{marker_html(r)}</td></tr>')
    legend = ('<p class="muted">● evidence-based: a standard or study states the value. ○ inferred: reasoned from related evidence, '
              'with the gap recorded. Values are provisional.</p>')
    spec_html = ('<p class="muted fcnt" id="fc-spec"></p>' + legend + '<table class="plain spec" role="table"><caption class="vh">Recommended value for each group of people</caption>'
                 '<colgroup><col style="width:19%"><col style="width:24%"><col style="width:57%"></colgroup>'
                 '<thead role="rowgroup"><tr role="row"><th role="columnheader" scope="col">Who it applies to</th>'
                 '<th role="columnheader" scope="col">Value</th><th role="columnheader" scope="col">Basis</th></tr></thead>'
                 f'<tbody role="rowgroup">{"".join(rows)}</tbody></table>')

    # ---- 2. jurisdictions
    by_code = {j["code"]: j for j in page["jurisdictions"] if j["code"] in SCOPE}
    alpha = lambda c: JURISDICTION_NAMES.get(c, c).lower()  # noqa: E731
    have = sorted((c for c in SCOPE if c in by_code), key=alpha)
    none = sorted((c for c in SCOPE if c not in by_code), key=alpha)

    def split_q(text):
        i = text.find(" (")
        return (text, "") if i < 0 else (text[:i], text[i:])

    def clause_text(j):
        return j.get("clause_display") or "clause not recorded"

    def gcell(label, text, cls="val"):
        if not text:
            return f'<td role="cell" class="nil" data-l="{label}"><span class="vh">None stated</span><span aria-hidden="true">&ndash;</span></td>'
        main, qual = split_q(text)
        return (f'<td role="cell" class="{cls}" data-l="{label}"><span class="mv">{rt(main)}</span>'
                + (f'<span class="mq">{rt(qual)}</span>' if qual else "") + "</td>")

    def src_link(j):
        s0 = j["sources"][0] if j["sources"] else None
        if not s0:
            return "no link recorded"
        return (f'<a href="{escape(s0["url"])}" target="_blank" rel="noopener">{escape(s0["label"])}'
                '<span class="vh"> (opens in a new tab)</span></a>')

    master = ""
    if best:
        master += (f'<tbody role="rowgroup" class="mg gb"><tr role="row"><th role="rowheader" scope="row">Best practice</th>'
                   f'<td role="cell" class="val" data-l="Preferred"><span class="mv">{rt(slope_tok(best))}</span></td>'
                   f'<td role="cell" class="val" data-l="Maximum"><span class="mv">{rt(slope_tok(best))}</span></td>'
                   f'<td role="cell" class="nil" data-l="Between landings"><span class="vh">None stated</span><span aria-hidden="true">&ndash;</span></td></tr>'
                   f'<tr role="row" class="std"><td role="cell" colspan="4">Best value found for the people it serves; no study in the library improves on it.</td></tr></tbody>')
    for c in have:
        j = by_code[c]
        m = j.get("master") or {"preferred": None, "max": j["headline"], "landing_limit": None, "sort": None}
        key = "" if m.get("sort") is None else m["sort"]
        dl = "ja" if c == "JP" else "zh"
        cl = "" if clause_text(j) in j["standard"] else f", {escape(clause_text(j))}"
        std = (f'<i>{lw(escape(j["standard"]), dl)}</i>{cl}, {escape(j["edition"])} &middot; {escape(tier_label(j["tier"]))} '
               f'&middot; {READ[j["level"]]} &middot; Source: {src_link(j)}')
        master += (f'<tbody role="rowgroup" class="mg" data-code="{c}" data-sort="{key}"><tr role="row"><th role="rowheader" scope="row">'
                   f'<a href="#j-{c}" class="jlink">{escape(JURISDICTION_NAMES.get(c, c))}</a></th>'
                   f'{gcell("Preferred", m.get("preferred"))}{gcell("Maximum", m.get("max"))}{gcell("Between landings", m.get("landing_limit"), "sv")}</tr>'
                   f'<tr role="row" class="std"><td role="cell" colspan="4">{std}.</td></tr></tbody>')

    PCOLS = [("landing", "Landings"), ("width", "Clear width"), ("handrails", "Handrails"), ("cross", "Cross-slope")]

    def pcell(label, text):
        if not text:
            return f'<td role="cell" class="nil" data-l="{label}">not read</td>'
        main, qual = split_q(text)
        return f'<td role="cell" class="sv" data-l="{label}">{rt(main)}' + (f'<span class="mq">{rt(qual)}</span>' if qual else "") + "</td>"

    prow = ""
    for c in have:
        pm = (by_code[c].get("master") or {}).get("params") or {}
        nm_ = escape(JURISDICTION_NAMES.get(c, c))
        if not any(pm.get(k) for k, _ in PCOLS):
            prow += (f'<tbody role="rowgroup" class="mg" data-code="{c}"><tr role="row"><th role="rowheader" scope="row">{nm_}</th>'
                     f'<td role="cell" class="nil span" colspan="4">Only the gradient has been read.</td></tr></tbody>')
        else:
            prow += (f'<tbody role="rowgroup" class="mg" data-code="{c}"><tr role="row"><th role="rowheader" scope="row">{nm_}</th>'
                     + "".join(pcell(lab, pm.get(k)) for k, lab in PCOLS) + "</tr></tbody>")

    def jur_entry(j):
        needs = sorted({n for p in j["provisions"] for n in p[2]})
        facets["need"].update(needs)
        dl = "ja" if j["code"] == "JP" else "zh"
        prov = "".join(f'<div class="prov" data-need="{" ".join(p[2])}"><dt>{escape(p[0])}</dt><dd>{rt(p[1])}</dd></div>' for p in j["provisions"])
        srcs = "".join(f'<li><a href="{escape(s["url"])}" target="_blank" rel="noopener">{escape(s["label"])} (opens in a new tab)</a></li>' for s in j["sources"])
        lib = "".join(f"<li>{cite_btn(r)}</li>" for r in j["kb_refs"])
        return (f'<details class="jx fi" id="j-{j["code"]}" data-scope="universal" data-pop="" data-icf="" data-need="{" ".join(needs)}">'
                f'<summary><b class="jn">{escape(JURISDICTION_NAMES.get(j["code"], j["code"]))}</b> '
                f'<span class="muted">{lw(escape(j["standard"]), dl)}, {escape(j["edition"])}</span></summary>'
                f'<div class="body"><p class="muted">{escape(j["regime"])}; {escape(clause_text(j))}; {escape(tier_label(j["tier"]))}.</p>'
                f'<dl class="provs">{prov}</dl>'
                f'<p><b>Compared with best practice.</b> {rt(j["vs_guidebook"])}</p>'
                f'<p><b>What was read.</b> {rt(j["read"])}</p>'
                + (f'<p><b>Open.</b> {rt(j["open"])}</p>' if j.get("open") else "")
                + (f'<p><b>In the library.</b></p><ul>{lib}</ul>' if lib else "")
                + (f'<p><b>Links.</b></p><ul>{srcs}</ul>' if srcs else "")
                + "</div></details>")

    pending = (f'<p><b>Not yet covered ({len(none)}):</b> {", ".join(escape(JURISDICTION_NAMES.get(c, c)) for c in none)}.</p>' if none else "")
    jur_html = (
        '<a class="skip skipin" href="#detail-list">Skip the tables to the details by jurisdiction</a>'
        '<p class="ordrow"><button type="button" class="lk msort" id="msort" aria-label="Change table order, currently alphabetical">Order: A–Z</button> '
        '<span class="muted">Select a jurisdiction name to open its full entry.</span></p>'
        '<table class="plain cmp" id="master" role="table"><caption class="vh">Ramp gradient requirement by jurisdiction</caption>'
        '<colgroup><col style="width:19%"><col style="width:18%"><col style="width:24%"><col style="width:39%"></colgroup>'
        '<thead role="rowgroup"><tr role="row"><th role="columnheader" scope="col">Jurisdiction</th>'
        '<th role="columnheader" scope="col">Preferred</th>'
        '<th role="columnheader" scope="col" id="th-max" aria-sort="none">Maximum</th>'
        f'<th role="columnheader" scope="col">Between landings</th></tr></thead>{master}</table>'
        '<h3>Other ramp requirements</h3>'
        '<table class="plain cmp" id="master2" role="table"><caption class="vh">Other ramp requirements by jurisdiction</caption>'
        '<colgroup><col style="width:19%"><col style="width:30%"><col style="width:17%"><col style="width:22%"><col style="width:12%"></colgroup>'
        '<thead role="rowgroup"><tr role="row"><th role="columnheader" scope="col">Jurisdiction</th>'
        + "".join(f'<th role="columnheader" scope="col">{lab}</th>' for _, lab in PCOLS) + f'</tr></thead>{prow}</table>'
        + pending +
        f'<details class="alljx" id="detail-list"><summary>Details by jurisdiction ({len(have)})</summary>' + "".join(jur_entry(by_code[c]) for c in have) + "</details>")

    # ---- 3. why it matters
    why = "".join(f'<li>{rt(w["text"])}{" " + " ".join(cite_btn(r) for r in w.get("refs", []))}</li>' for w in page["why_it_matters"])

    # ---- 4. evidence: reference list, alphabetical by first author's last name
    ev = []
    for e in page["evidence"]:
        s = src(e["ref"])
        last = unicodedata.normalize("NFKD", apa_authors(s)[0].split(",")[0]).encode("ascii", "ignore").decode().lower()
        ev.append((re.sub(r"[^a-z0-9 ]", "", last), s["pub_year"] or 0, e, s))
    ev.sort(key=lambda t: (t[0], t[1]))  # key built below from the last name only
    ev_items = []
    for _, _, e, s in ev:
        subj = [x["population_code"] for x in s["subject"] if x["population_code"] != "ALL"]
        tag = tagattrs(subj, s["icf"], s["needs"], "group" if subj else "universal")
        doi = (f' <a href="https://doi.org/{escape(s["doi"])}" target="_blank" rel="noopener">doi:{escape(s["doi"])} (opens in a new tab)</a>'
               if s["doi"] else "")
        pops_txt = ", ".join(d["pops"].get(x["population_code"], x["population_code"]) for x in s["subject"]
                             if x["population_code"] != "ALL") or "population not recorded"
        pops_txt = pops_txt[:1].upper() + pops_txt[1:]
        type_lab = TYPE_LABEL.get(s["evidence_type"], s["evidence_type"] or "")
        meta = (f'{escape(pops_txt)} &middot; Evidence tier {s["tier"]} ({escape(type_lab)}) &middot; '
                f'{"DOI recorded" if s["doi"] else "no DOI recorded"} &middot; '
                f'{"metadata verified" if s["verification_status"] == "VERIFIED" else "metadata not yet verified"}')
        ev_items.append(f'<li class="fi evr" {tag}><details><summary><span class="apa">{lw(apa(s)[1])}</span>'
                        f'<span class="evmeta">{meta}</span><span class="evmeta">{rt(first_sentence(e["relevance"]))}</span></summary>'
                        f'<div class="body"><p>{rt(e["relevance"])}</p>'
                        f'<p class="muted">{doi.strip()} {cited_on(e["ref"])}</p></div></details></li>')

    # ---- 5. gaps
    gaps = "".join(f'<li><b>{escape(g["gap_id"])}</b> ({escape(g["status"])}). {escape(g["description"] or "")}</li>' for g in d["gaps"])
    gaps_n = len(d["gaps"])
    none_who = [r["who"] for rows_ in page["values"].values() for r in rows_ if r["status"] == "no-evidence"]
    co1_n = d["db"].execute("""SELECT COUNT(*) FROM source_slug_links l JOIN evidence_sources es ON es.ref_id = l.ref_id
                               WHERE l.slug = ? AND es.evidence_type = 'co1'""", (item["bpc_source_slug"],)).fetchone()[0]
    gap_lead = ""
    if none_who:
        gap_lead += f'<p>No evidence yet for: {escape("; ".join(w[:1].lower() + w[1:] for w in none_who))}.</p>'
    gap_lead += ('<p>No lived-experience (Co-1) evidence on this item is recorded in the library.</p>' if co1_n == 0
                 else f'<p>{co1_n} lived-experience (Co-1) source(s) are recorded for this item.</p>')

    # ---- filter options (only codes that occur on the page)
    def opt(kind, c, label):
        return f'<button type="button" class="fchip" data-f="{kind}" data-c="{escape(c)}" aria-pressed="false">{label}</button>'

    def facet(kind, codes, table, group_of=None, group_names=None, show_code=True):
        def lab(c):
            n = table[c]
            n = n[:1].upper() + n[1:] if kind == "pop" else n
            return f"{escape(c)} {escape(n)}" if show_code else escape(n)
        if not group_of:
            return "".join(opt(kind, c, lab(c)) for c in sorted(codes))
        groups = {}
        for c in sorted(codes):
            groups.setdefault(group_of(c), []).append(c)
        return "".join(f'<div class="fgp"><span class="gl" id="g-{kind}-{i}">{escape((group_names or {}).get(g, g))}</span>'
                       f'<span class="fgi" role="group" aria-labelledby="g-{kind}-{i}">' + "".join(opt(kind, c, lab(c)) for c in cs) + "</span></div>"
                       for i, (g, cs) in enumerate(sorted(groups.items(), key=lambda kv: str(kv[0]))))

    pop_f = facet("pop", {p for p in facets["pop"] if p != "ALL"}, d["pops"], lambda c: d["pop_cat"].get(c, "other"),
                  {"mobility": "Mobility", "neurological": "Neurological", "pain_fatigue": "Pain and fatigue", "sensory": "Sensory",
                   "cognitive": "Cognitive", "developmental": "Developmental", "mental_health": "Mental health", "other": "Other"})
    icf_f = facet("icf", facets["icf"], d["icf"], lambda c: c[:1],
                  {"b": "Body functions", "d": "Activities and participation", "s": "Body structures", "e": "Environment"})
    need_f = facet("need", facets["need"], d["needs"], show_code=False)

    # ---- hero figures (computed from the data, never typed twice)
    facts = []
    if best:
        facts.append(("Best practice found", rt(slope_tok(best))))
    gc = gv = None
    if maxima:
        gc, gv = min(maxima, key=lambda t: t[1])
        facts.append((f"Gentlest legal maximum, {JURISDICTION_NAMES.get(gc, gc)}", rt(slope_tok(gv))))
    hero = f'<dl class="hero" style="--n:{len(facts)}">' + "".join(f'<div class="hf"><dt class="hl">{escape(a)}</dt><dd class="hv">{b}</dd></div>' for a, b in facts) + "</dl>"
    pref_by = sorted({c for x, c, f in stated if best and abs(x - best) < 1e-6 and f == "preferred"})
    max_by = sorted({c for x, c, f in stated if best and abs(x - best) < 1e-6 and f == "max"})
    bits = []
    if pref_by:
        bits.append("stated as preferred in " + ", ".join(JURISDICTION_NAMES.get(c, c) for c in pref_by))
    if max_by:
        bits.append("stated as the maximum in " + ", ".join(JURISDICTION_NAMES.get(c, c) for c in max_by))
    basis_txt = page["_meta"].get("best_practice_basis", "Best practice is what benefits the people it is for most.")
    hero_note = (f'<p class="muted herotip">{escape(basis_txt)} Found {"; ".join(bits)}. This rests on standards alone, so it is provisional.</p>') if bits else ""
    plain = ""
    if best:
        n_ = round(1 / best)
        plain = ('<p class="inplain">' + rt("In plain terms: for every {{len=1000|1 m}} a ramp climbs, a " + slope_tok(best)
                 + " slope needs {{len=%d|%d m}} of ramp. A gentler slope takes less effort to push, walk or roll up." % (n_ * 1000, n_)) + "</p>")
    scope_note = f"{len(have)} of {len(SCOPE)} major jurisdictions read; {len(ev_items)} studies in the library."

    # ---- figure: the run needed to climb the same rise at each gradient (real text; only the triangles scale)
    rise_mm = 500
    frows = []
    if best:
        frows.append(("Best practice found", best, True))
    if gv:
        frows.append((f"Gentlest legal maximum, {JURISDICTION_NAMES.get(gc, gc)}", gv, False))
    frows.sort(key=lambda r: r[1])
    fig = ""
    if frows:
        max_run = max(rise_mm / f for _, f, _ in frows)
        items = []
        for lab, f, strong in frows:
            run_mm = rise_mm / f
            pct = run_mm / max_run * 82.0
            sw = "2.5" if strong else "1.25"
            items.append(
                f'<li class="frow{" fstrong" if strong else ""}"><span class="flab">{escape(lab)} '
                f'<span class="fs u" data-k="slope" data-v="{f:.8g}">{default_text("slope", f)}</span></span>'
                f'<span class="ft"><svg class="tri" aria-hidden="true" focusable="false" viewBox="0 0 100 20" preserveAspectRatio="none" style="width:{pct:.1f}%">'
                f'<path d="M0.5 19.5 L0.5 0.5 L99.5 19.5 Z" fill="none" stroke="currentColor" stroke-width="{sw}" vector-effect="non-scaling-stroke" stroke-linejoin="round"/></svg>'
                f'<span class="fv u" data-k="len" data-v="{run_mm:.8g}">{default_text("len", run_mm)}</span></span></li>')
        fig = ('<figure class="fig" aria-labelledby="fig-c"><ul class="figrows">' + "".join(items) + "</ul>"
               f'<figcaption id="fig-c">Horizontal run needed to climb the same <span class="u" data-k="len" data-v="{rise_mm}">{default_text("len", rise_mm)}</span> '
               'rise at each gradient. Triangle length is drawn to a true horizontal scale; the rise is drawn the same height in every row.</figcaption></figure>')

    # ---- assemble
    sections = [("spec", "Values by group", spec_html), ("jurisdictions", "Requirements by jurisdiction", jur_html),
                ("why", "Why it matters", f'<ul class="why">{why}</ul>'),
                ("evidence", "Evidence", f'<p class="muted fcnt" id="fc-ev"></p><div id="evlist"><ol class="refs" id="evol">{"".join(ev_items)}</ol></div>')]
    if gaps:
        sections.append(("gaps", "Gaps", gap_lead + f'<details class="gps"><summary>{gaps_n} gaps recorded for this item</summary><div class="body"><ul>{gaps}</ul></div></details>'))
    prov = (f'<p>{escape(page["_meta"].get("reader_status", page["_meta"]["status"]))}</p>'
            f'<p class="muted">Generated {datetime.now(timezone.utc).strftime("%Y-%m-%d")} from the Guidebook database. '
            f'Evidence base: {escape(item["bpc_source_slug"])}.</p>')
    sections.append(("about", "About this page", prov))
    metas = {"jurisdictions": f"{len(have)} of {len(SCOPE)} read", "evidence": f"{len(ev_items)} sources"}
    nav = '<li><a href="#main" data-snav="main">Overview</a></li>' + "".join(
        f'<li><a href="#{sid}" data-snav="{sid}"><span class="snc-n">{i + 1}</span> {head}</a></li>' for i, (sid, head, _) in enumerate(sections))
    myj = "".join(f'<option value="{c}">{escape(JURISDICTION_NAMES.get(c, c))}</option>' for c in have)
    body = "".join(
        f'<section class="section" id="{sid}" aria-labelledby="h-{sid}"><h2 id="h-{sid}"><span class="n">{i + 1}</span><span class="t">{head}</span>'
        + (f'<span class="sec-meta">{metas[sid]}</span>' if sid in metas else "") + f'</h2><div class="sc">{html}</div></section>'
        for i, (sid, head, html) in enumerate(sections))

    out = TEMPLATE
    for k, val in {
        "__TITLE__": escape(short), "__CODE__": escape(code), "__QUESTION__": escape(question),
        "__HERO__": hero + hero_note + plain, "__FIG__": fig, "__MYJ__": myj, "__NAV__": nav, "__SECTIONS__": body, "__SCOPE__": escape(scope_note),
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
<title>__CODE__ __TITLE__ &mdash; Guidebook specification</title>
<meta name="description" content="Specification __CODE__: __TITLE__. Provisional.">
<style>
:root{--bg:#fff;--ink:#000;--muted:#595959;--rule:#d0d0d0;--hit:#f2f2f2;--red:#c4161c;
 --f:"Helvetica Neue",Helvetica,Arial,"Liberation Sans",sans-serif;
 --s1:56px;--s2:24px;--s3:16px;--s4:16px;--s5:13px;--gap:24px}
@media (prefers-color-scheme:dark){:root{--bg:#000;--ink:#fff;--muted:#b3b3b3;--rule:#3a3a3a;--hit:#161616;--red:#ff6b70}}
*{box-sizing:border-box}[hidden]{display:none!important}
html{scroll-padding-top:64px}
body{margin:0;background:var(--bg);color:var(--ink);font:400 var(--s4)/1.5 var(--f);font-variant-numeric:tabular-nums}
a{color:inherit;text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px;overflow-wrap:anywhere}
a:hover{text-decoration-thickness:2px}
input,select,button{font-family:inherit;font-size:inherit;color:inherit}
.vh{position:absolute!important;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
.wrap{max-width:1120px;margin:0 auto;padding:0 32px}
.skip{position:absolute;left:-9999px;top:8px;background:var(--bg);color:var(--ink);padding:10px 14px;border:2px solid var(--ink);z-index:30}.skip:focus{left:8px}
.top{font-size:var(--s4)}.top .wrap{display:flex;gap:6px 32px;align-items:baseline;flex-wrap:wrap;padding-top:14px;padding-bottom:14px}
.top .brand{font-weight:700;text-decoration:none}.top nav{color:var(--ink)}
.sectnav{position:sticky;top:0;z-index:5;background:var(--bg);border-top:1px solid var(--ink);border-bottom:1px solid var(--rule)}
.sectnav ol{display:flex;flex-wrap:wrap;list-style:none;margin:0 auto;padding:0 20px;max-width:1120px;gap:0}
.sectnav .navd{border:0}.navd>summary{display:none;font-weight:700}.sectnav li{margin:0}.sectnav a{display:block;padding:12px 12px 9px;font-size:var(--s4);color:var(--ink);text-decoration:none;white-space:nowrap;border-bottom:3px solid transparent;min-height:44px}
.sectnav a:hover{color:var(--ink);text-decoration:underline}
.sectnav a[aria-current=true]{color:var(--ink);font-weight:700;border-bottom-color:var(--red)}
.page{padding-top:56px;padding-bottom:120px}
.kicker{margin:0 0 20px;font-size:var(--s5);color:var(--muted)}
h1{margin:0;max-width:24em;font-size:var(--s2);line-height:1.2;font-weight:700}
.q{margin:20px 0 0;max-width:34em;font-size:var(--s2);line-height:1.25}
.hero{display:grid;grid-template-columns:repeat(var(--n,3),minmax(0,1fr));gap:0 var(--gap);margin:36px 0 0;padding-top:12px;border-top:1px solid var(--ink)}
.herotip{margin:12px 0 0;max-width:62ch}.inplain{margin:16px 0 0;max-width:62ch}.mk{white-space:nowrap;color:var(--muted);font-size:var(--s5)}
.hf{display:flex;flex-direction:column-reverse;justify-content:flex-end;gap:6px}.hl{font-size:var(--s5);color:var(--muted)}.hv{margin:0;font-size:var(--s1);font-weight:700;line-height:1.05}
.fig{margin:40px 0 0}.figrows{list-style:none;margin:0;padding:0;border-bottom:1px solid var(--rule)}
.frow{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,9fr);gap:0 var(--gap);align-items:center;padding:10px 0;margin:0;border-top:1px solid var(--rule)}
.flab{font-size:var(--s5);color:var(--muted)}.fs{color:var(--muted)}.fstrong .flab{color:var(--ink);font-weight:700}
.ft{display:grid;grid-template-columns:minmax(0,1fr) 7.5em;gap:12px;align-items:center;min-width:0}.tri{display:block;height:20px;color:var(--ink)}.fv{font-size:var(--s4);white-space:nowrap;text-align:right}.fstrong .fv{font-weight:700}
.fig figcaption{margin-top:12px;font-size:var(--s5);color:var(--muted);max-width:52em}
.bar{margin:36px 0 0;border-top:1px solid var(--ink)}
.brow{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,9fr);gap:0 var(--gap);padding:10px 0;border-bottom:1px solid var(--rule);align-items:center}
.tl{font-size:var(--s5);color:var(--muted)}.cx{display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center}
.sel-l{font-size:var(--s5);color:var(--muted);display:inline-flex;align-items:center;gap:8px}
.sel{font-size:var(--s4);padding:5px 8px;min-height:36px;border:1px solid var(--ink);background:var(--bg);color:var(--ink);border-radius:0}
.seg{display:inline-flex;flex-wrap:wrap;gap:0 20px}
.seg button{font-size:var(--s4);padding:6px 0;min-height:36px;background:none;color:var(--muted);border:0;border-bottom:3px solid transparent;cursor:pointer}
.seg button:hover{color:var(--ink);text-decoration:underline}
.seg button[aria-expanded=true]{color:var(--ink);font-weight:700;border-bottom-color:var(--red)}
.pills{border-bottom:0;padding-top:0}.pills .pg{grid-column:2}.pg{display:flex;flex-wrap:wrap;gap:0 28px}
.fgp{display:flex;flex-direction:column;margin-top:8px}.fgi{display:flex;flex-wrap:wrap;gap:0 18px}
.gl{font-size:var(--s5);color:var(--muted)}
.fchip{font-size:var(--s4);padding:6px 0;min-height:36px;background:none;border:0;border-bottom:3px solid transparent;cursor:pointer;color:var(--ink);text-align:left}
.fchip:hover{text-decoration:underline}.fchip[aria-pressed=true]{font-weight:700;border-bottom-color:var(--red)}
.fcount{font-size:var(--s5);color:var(--muted);margin-left:4px;font-weight:400}
.applied{display:inline-flex;flex-wrap:wrap;gap:0 16px}.clr{font-size:var(--s5)}
.section{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,9fr);gap:0 var(--gap);margin:80px 0 0;padding-top:12px;border-top:3px solid var(--ink)}
h2{grid-column:1;margin:0;font-size:var(--s2);line-height:1.15;font-weight:700}
h2 .n{display:block;font-size:var(--s2);font-weight:400;color:var(--muted);margin-bottom:6px}h2 .t{display:block}
.sec-meta{display:block;margin-top:8px;font-size:var(--s5);font-weight:400;color:var(--muted)}
.sc{grid-column:2;min-width:0}.sc>p{max-width:68ch}
h3{margin:36px 0 8px;font-size:var(--s4);font-weight:700}
p{margin:0 0 12px}.muted,.note{color:var(--muted)}.muted,.std,.note{font-size:var(--s5)}
.lk{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer;text-align:left;text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px}
.lk:hover{text-decoration-thickness:2px}.cite{display:inline-block;padding:2px 0;min-height:24px}.ordrow{margin:0 0 8px;font-size:var(--s5)}.msort{color:var(--ink);font-size:var(--s5);font-weight:400;margin-left:8px;min-height:32px;padding:4px 6px}
.mval{font-size:var(--s3);font-weight:700;line-height:1.3}
a:focus-visible,button:focus-visible,summary:focus-visible,select:focus-visible,input:focus-visible,.pg:focus-visible{outline:3px solid var(--red);outline-offset:2px}
dialog h3:focus{outline:none}.jlink{font-weight:700;display:inline-block;padding:3px 0;min-height:24px}.fcnt{margin:0 0 8px}.fchip:disabled{color:var(--muted);cursor:default;text-decoration:none;opacity:.7}
.pills .pg{max-height:45vh;overflow:auto}.skipin:focus{top:60px}
tbody.mine>tr>*{background:var(--hit)}tbody.mine>tr:first-child>th{box-shadow:inset 4px 0 0 var(--red);padding-left:12px}
table.plain{width:100%;table-layout:fixed;border-collapse:collapse;margin:0 0 12px}table.plain td,table.plain th{overflow-wrap:anywhere}
table.plain th,table.plain td{padding:12px 20px 12px 0;text-align:left;vertical-align:top;border-top:1px solid var(--rule)}
table.plain thead th{font-size:var(--s5);font-weight:400;color:var(--muted);border-top:0;border-bottom:1px solid var(--ink);padding-top:8px;padding-bottom:8px;position:sticky;top:46px;background:var(--bg);z-index:2}
table.plain tbody th{font-weight:400}table.plain .nil{color:var(--muted);font-size:var(--s5)}.sv{font-size:var(--s4);font-weight:400;line-height:1.35}
.val{font-size:var(--s3);font-weight:700;line-height:1.3}
.mv{font-size:var(--s3);font-weight:700;line-height:1.3}.mq{display:block;font-size:var(--s5);font-weight:400;color:var(--muted);line-height:1.4;margin-top:2px}
table.spec td:nth-child(3){font-size:var(--s5);color:var(--muted);line-height:1.5}table.spec td:nth-child(3) .cite{color:inherit}
table.cmp tbody.mg>tr:first-child>*{padding-bottom:2px}
table.cmp tr.std td{padding:0 20px 12px 0;border-top:0;font-size:var(--s5);color:var(--muted)}
table.cmp tbody.gb>tr:first-child>*{border-top:1px solid var(--ink)}table.cmp tbody.gb th{font-weight:700}table.cmp tbody.gb tr.std td{padding-bottom:14px;border-bottom:1px solid var(--ink)}
.fi.hidden{display:none}.fi.hit,.prov.hit{background:var(--hit);box-shadow:inset 4px 0 0 var(--red)}
details{border-top:1px solid var(--rule)}details:last-of-type{border-bottom:1px solid var(--rule)}
details>summary{cursor:pointer;list-style:none;padding:12px 8px 12px 28px;position:relative;min-height:44px}
details>summary::-webkit-details-marker{display:none}details>summary::before{content:"\25B8";position:absolute;left:4px;top:11px;color:var(--ink)}
details[open]>summary::before{content:"\25BE"}details>summary:hover .jn{text-decoration:underline}
.jn{font-weight:700;margin-right:12px}
.body{padding:2px 0 16px;max-width:66ch}.body p{margin:0 0 10px}.body ul{margin:0 0 10px;padding-left:20px}
dl.provs{margin:0 0 12px}.prov{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2.4fr);gap:2px var(--gap);padding:8px 0;border-top:1px solid var(--rule)}
.prov dt{font-weight:700}.prov dd{margin:0}.prov.dim{opacity:.55}
ul,ol{padding-left:20px;margin:0 0 12px}li{margin:0 0 12px}
.why{max-width:34em;list-style:none;padding-left:0}.why li{font-size:var(--s3);line-height:1.4;padding:12px 0;margin:0;border-top:1px solid var(--rule)}.why li:last-child{border-bottom:1px solid var(--rule)}
ol.refs{padding-left:0;list-style:none}ol.refs li{padding:0;margin:0;border-top:1px solid var(--rule)}
ol.refs details{border:0}ol.refs details>summary{padding:12px 8px 12px 28px;min-height:44px}
ol.refs .body{padding-left:28px}.evmeta{display:block;font-size:var(--s5);color:var(--muted);padding-left:2em;margin-top:2px}
ol.refs li.evgrp{font-weight:700;padding:24px 0 8px;border-top:1px solid var(--ink)}
.apa{overflow-wrap:anywhere;display:block;padding-left:2em;text-indent:-2em}.scope{margin:80px 0 0;padding-top:12px;border-top:1px solid var(--ink);font-size:var(--s5);color:var(--muted)}
dialog{max-width:min(680px,94vw);width:100%;border:2px solid var(--ink);border-radius:0;background:var(--bg);color:var(--ink);padding:24px 28px}
dialog::backdrop{background:rgba(0,0,0,.55)}dialog h3{margin:0 0 14px;font-size:var(--s2);line-height:1.15}dialog .jd{max-height:60vh;overflow:auto;font-size:var(--s4)}
dialog .apa-full{padding-left:2em;text-indent:-2em;margin:0 0 12px}
.dact{display:flex;justify-content:flex-end;gap:24px;margin-top:16px;font-size:var(--s5)}
.dact button{padding:8px 0;min-height:44px;background:none;border:0;border-bottom:2px solid var(--ink);cursor:pointer}.dact button:hover{text-decoration:underline}
@media (max-width:900px){
 .section{grid-template-columns:minmax(0,1fr);margin-top:56px}h2{margin-bottom:16px}.sc{grid-column:1}
 h2 .n{display:inline;margin:0 10px 0 0}h2 .t{display:inline}
 .brow{grid-template-columns:minmax(0,1fr);gap:4px}.pills .pg{grid-column:1}.frow{grid-template-columns:minmax(0,1fr);gap:6px}
}
@media (max-height:500px){
 .sectnav{position:static}.page{padding-top:16px}.kicker{margin-bottom:6px}.bar{margin-top:12px;display:flex;flex-wrap:wrap;gap:0 24px}.brow{display:flex;gap:8px 12px;border:0;padding:2px 0}.brow.pills{flex:0 0 100%}.hero{margin-top:12px}table.plain thead th{top:0}
}
@media (pointer:coarse){.cite,.jlink,.clr,.msort{display:inline-block;padding:10px 4px}}
@media (max-width:760px){
 .wrap{padding:0 20px}.page{padding-top:32px}.hv{font-size:36px}.sectnav{position:static}
 .hero{grid-template-columns:1fr;gap:16px;margin-top:32px}
 .frow{grid-template-columns:minmax(0,1fr);gap:6px}
 .section{grid-template-columns:minmax(0,1fr);margin-top:56px}h2{margin-bottom:16px}.sc{grid-column:1}
 h2 .n{display:inline;margin:0 10px 0 0}h2 .t{display:inline}
 .brow{grid-template-columns:minmax(0,1fr);gap:4px}.pills .pg{grid-column:1}.prov{grid-template-columns:minmax(0,1fr)}
 table.cmp thead,table.spec thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
 table.cmp tbody.mg>tr:first-child{display:grid;grid-template-columns:1fr 1fr;gap:0 16px;padding:12px 0 0;border-top:1px solid var(--rule)}
 table.cmp tbody.mg>tr:first-child>*{border:0;padding:0 0 4px}table.cmp tbody.mg>tr:first-child>th{grid-column:1/-1}
 table.cmp td.span{grid-column:1/-1}table.cmp tbody.mg>tr:first-child{grid-template-columns:1fr 1fr}
 table.plain{display:block;table-layout:auto}table.plain tbody{display:block}table.plain colgroup{display:none}
 table.cmp tr.std,table.cmp tr.std td{display:block}
 .navd>summary{display:block}.sectnav ol{display:block;padding:0 12px 8px}.sectnav li a{white-space:normal}
 table.cmp td[data-l]::before,table.spec td[data-l]::before{content:attr(data-l);display:block;font-size:var(--s5);color:var(--muted);font-weight:400}
 table.cmp tr.std td{padding:0 0 12px}
 table.spec tr{display:block;padding:12px 0;border-top:1px solid var(--rule)}table.spec th,table.spec td{display:block;padding:0;border:0}.val{white-space:normal}
 .seg button,.fchip,.sel{min-height:44px}
}
@media (forced-colors:active){.fi.hit,.prov.hit{border-left:4px solid Highlight}.seg button[aria-expanded=true],.fchip[aria-pressed=true],.sectnav a[aria-current=true]{border-bottom:3px solid Highlight}}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important;scroll-behavior:auto!important}}
@media print{.bar,.sectnav,.top,.skip{display:none}details>summary::before{content:""}}
</style>
</head>
<body>
<a href="#main" class="skip">Skip to main content</a>
<header class="top"><div class="wrap"><a href="../index.html" class="brand">Guidebook</a>
 <nav aria-label="Breadcrumb"><a href="../index.html">Browse</a> / <a href="../index.html#exemplar">Specifications</a> / __CODE__</nav></div></header>
<nav class="sectnav" aria-label="Sections of this specification"><details class="navd" open><summary>Sections: <span id="navcur">Overview</span></summary><ol>__NAV__</ol></details></nav>

<main id="main" class="wrap page">
 <p class="kicker">__CODE__ &middot; Specification &middot; Provisional</p>
 <h1>__TITLE__</h1>
 <div class="bar" id="tools" role="group" aria-label="Lens, filters and units">
  <div class="brow"><span class="tl" id="fl">Lens</span><span class="cx">
   <span class="seg" role="group" aria-labelledby="fl"><button type="button" data-lens="pop" aria-expanded="false" aria-controls="pillrow">Who it's for</button><button type="button" data-lens="icf" aria-expanded="false" aria-controls="pillrow">ICF code</button><button type="button" data-lens="need" aria-expanded="false" aria-controls="pillrow">Access need</button></span>
   <span class="applied" id="activelist"></span><button type="button" class="lk clr" id="clear" hidden>Clear all filters</button></span></div>
  <div class="brow pills" id="pillrow" hidden><span></span>
   <div class="pg" data-lens="pop" role="group" aria-label="Who it's for options" tabindex="0" hidden>__POPF__</div><div class="pg" data-lens="icf" role="group" aria-label="ICF code options" tabindex="0" hidden>__ICFF__</div><div class="pg" data-lens="need" role="group" aria-label="Access need options" tabindex="0" hidden>__NEEDF__</div></div>
  <div class="brow" id="onlyrow" hidden><span></span><label><input type="checkbox" id="onlyspec"> Show only rows for the selected people or needs</label></div>
  <div class="brow"><span class="tl">Units</span><span class="cx">
   <label class="sel-l">Length <select class="sel" data-u="len"><option value="met">Metric</option><option value="imp">Imperial</option><option value="stated">As stated</option></select></label>
   <label class="sel-l">Slope <select class="sel" data-u="slope"><option value="ratio">Ratio 1:n</option><option value="pct">Percent</option><option value="deg">Degrees</option><option value="stated">As stated</option></select></label></span></div>
  <div class="brow"><span class="tl">Jurisdiction</span><span class="cx"><label class="sel-l"><span class="vh">My jurisdiction</span><select class="sel" id="myj"><option value="">All, A–Z</option>__MYJ__</select></label></span></div>
 </div>
 <p class="vh" id="live" role="status" aria-live="polite"></p>

 __HERO__
 __FIG__

 __SECTIONS__
 <p class="scope">__SCOPE__</p>
</main>
<dialog id="cdlg"><div id="cdlg-body"></div><div class="dact"><button type="button" class="lk" id="cdlg-close">Close</button></div></dialog>
<script type="application/json" id="cites">__CITES__</script>
<script>
(function(){
var prefs={len:'met',slope:'ratio'},sel={pop:[],icf:[],need:[]},onlySpec=false,lens='',myj='';
var LBL={pop:"Who it's for",icf:'ICF code',need:'Access need'};
function trim(n){return parseFloat(n).toString();}
function nb(t){return String(t).replace(/ /g,'\u00a0');}
function fmtSlope(f,m,o){
 if(m==='stated'&&o)return nb(o);
 if(m==='pct'){var p=f*100;return nb(trim(p.toFixed(p<1?2:1))+' %');}
 if(m==='deg'){return trim((Math.atan(f)*180/Math.PI).toFixed(1))+'°';}
 var n=1/f,r=Math.round(n);return '1:'+(Math.abs(n-r)<0.06?r:trim(n.toFixed(1)));}
function fmtLen(mm,m,o){
 if(m==='stated'&&o)return nb(o);
 if(m==='imp'){var inch=mm/25.4;
  if(inch>=36){var ft=Math.floor(inch/12+1e-9),rem=Math.round(inch-ft*12);if(rem>=12){ft+=1;rem=0;}return nb(ft+' ft'+(rem?' '+rem+' in':''));}
  return nb(trim(inch.toFixed(1))+' in');}
 if(mm>=1000)return nb(trim((mm/1000).toFixed(2))+' m');return nb(Math.round(mm)+' mm');}
function renderUnits(){var els=document.querySelectorAll('.u');for(var i=0;i<els.length;i++){var e=els[i],k=e.getAttribute('data-k'),v=parseFloat(e.getAttribute('data-v')),o=e.getAttribute('data-o');
 e.textContent=(k==='slope')?fmtSlope(v,prefs.slope,o):fmtLen(v,prefs.len,o);}
 var b=document.querySelectorAll('select[data-u]');for(var j=0;j<b.length;j++){b[j].value=prefs[b[j].getAttribute('data-u')];}}
function toks(el,a){var s=el.getAttribute(a)||'';return s?s.split(' '):[];}
function inter(a,b){for(var i=0;i<a.length;i++)if(b.indexOf(a[i])>-1)return true;return false;}
function say(t){document.getElementById('live').textContent=t;}
function applyFilter(announce){
 var active=['pop','icf','need'].filter(function(f){return sel[f].length>0;});
 var items=document.querySelectorAll('.fi'),shown={v:0,e:0},tot={v:0,e:0};
 for(var i=0;i<items.length;i++){var el=items[i],scope=el.getAttribute('data-scope'),isJ=el.classList.contains('jx'),kind=el.classList.contains('vrow')?'v':'e';
  var hit=active.length>0&&active.every(function(f){return inter(toks(el,'data-'+f),sel[f]);});
  var show=true;
  if(!isJ&&active.length>0){ if(scope==='group')show=hit; else show=!onlySpec; }
  if(!isJ){tot[kind]++;if(show)shown[kind]++;}
  el.classList.toggle('hidden',!show);el.classList.toggle('hit',active.length>0&&hit&&show);
  if(isJ){var ps=el.querySelectorAll('.prov');for(var p=0;p<ps.length;p++){var h=sel.need.length>0&&inter(toks(ps[p],'data-need'),sel.need);ps[p].classList.toggle('hit',h);ps[p].classList.toggle('dim',sel.need.length>0&&!h);}}}
 var fsp=document.getElementById('fc-spec'),fev=document.getElementById('fc-ev');
 if(fsp)fsp.textContent=active.length?'Filtered: showing '+shown.v+' of '+tot.v+' rows.':'';
 if(fev)fev.textContent=active.length?'Filtered: showing '+shown.e+' of '+tot.e+' studies.':'';
 if(announce)say(active.length?'Showing '+shown.v+' of '+tot.v+' specification rows and '+shown.e+' of '+tot.e+' studies.':'Filters cleared. Showing all rows and studies.');
 var al=document.getElementById('activelist');al.innerHTML='';var any=false;
 ['pop','icf','need'].forEach(function(f){sel[f].forEach(function(c){any=true;var bt=document.createElement('button');bt.type='button';bt.className='fchip act';bt.setAttribute('data-f',f);bt.setAttribute('data-c',c);
   var oc=document.querySelector('.pg .fchip[data-f="'+f+'"][data-c="'+c+'"]'),nm2=oc&&oc.firstChild?oc.firstChild.textContent.trim():c;bt.setAttribute('aria-label','Remove filter: '+nm2);bt.textContent=nm2+' ×';al.appendChild(bt);});});
 document.getElementById('clear').hidden=!any;document.getElementById('onlyrow').hidden=!any;
 var chips=document.querySelectorAll('.pg .fchip');for(var c2=0;c2<chips.length;c2++){var f2=chips[c2].getAttribute('data-f'),code=chips[c2].getAttribute('data-c');chips[c2].setAttribute('aria-pressed',sel[f2].indexOf(code)>-1);}
 regroup();}
function addCounts(){var chips=document.querySelectorAll('.pg .fchip'),its=document.querySelectorAll('.vrow,.evr');
 for(var i=0;i<chips.length;i++){var f=chips[i].getAttribute('data-f'),c=chips[i].getAttribute('data-c'),n=0;for(var k=0;k<its.length;k++){if(toks(its[k],'data-'+f).indexOf(c)>-1)n++;}
  var s=document.createElement('span');s.className='fcount';s.textContent=' ('+n+')';chips[i].appendChild(s);if(n===0){chips[i].disabled=true;chips[i].setAttribute('aria-disabled','true');}}}
function writeHash(){var p=[];if(prefs.len!=='met')p.push('len='+prefs.len);if(prefs.slope!=='ratio')p.push('slope='+prefs.slope);
 ['pop','icf','need'].forEach(function(f){if(sel[f].length)p.push(f+'='+sel[f].join(','));});if(onlySpec)p.push('spec=1');if(lens)p.push('lens='+lens);if(myj)p.push('j='+myj);
 try{history.replaceState(null,'',p.length?'#'+p.join('&'):location.pathname+location.search);}catch(e){}
 try{localStorage.setItem('gb-units',JSON.stringify(prefs));}catch(e){}}
function readHash(){try{var s=JSON.parse(localStorage.getItem('gb-units')||'null');if(s){prefs.len=s.len||prefs.len;prefs.slope=s.slope||prefs.slope;}}catch(e){}
 var h=location.hash.replace(/^#/,'');if(!h||h.indexOf('=')<0)return;h.split('&').forEach(function(kv){var a=kv.split('='),k=a[0],v=a[1]||'';
  if(k==='len'||k==='slope')prefs[k]=v;else if(k==='pop'||k==='icf'||k==='need')sel[k]=v?v.split(','):[];else if(k==='spec')onlySpec=v==='1';else if(k==='lens')lens=v;else if(k==='j')myj=v;});}
var CITES=null;function cites(){if(CITES===null){try{CITES=JSON.parse(document.getElementById('cites').textContent);}catch(e){CITES={};}}return CITES;}
function esc(t){return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;');}
function openDlg(id,opener){var dg=document.getElementById(id);dg._opener=opener||null;dg.setAttribute('aria-labelledby',id+'-t');if(dg.showModal)dg.showModal();else dg.setAttribute('open','');
 var h=dg.querySelector('h3');if(h){h.setAttribute('tabindex','-1');h.focus();}}
function closeDlg(id){var dg=document.getElementById(id);dg.close();if(dg._opener&&dg._opener.focus)dg._opener.focus();}
function openCite(ref,opener){var c=cites()[ref];if(!c)return;var here=location.pathname.split('/').pop().replace('.html','').toUpperCase();
 var pg=c.pages.map(function(p){var lab=p.item===here?p.item+' (this page)':(p.href?'<a href="'+p.href+'">'+p.item+'</a>':p.item);return '<li>'+lab+' &mdash; '+esc(p.name)+'</li>';}).join('');
 document.getElementById('cdlg-body').innerHTML='<h3 id="cdlg-t">Citation</h3><p class="apa-full">'+c.apa+'</p>'
  +'<p class="muted">Evidence tier '+c.tier+' ('+esc(c.type_label||'')+'); '+esc(c.status_label||'')+(c.complete?'':'; other authors not recorded')+'.</p>'
  +'<p><b>Cited on these pages</b></p><ul>'+pg+'</ul>';
 openDlg('cdlg',opener);}
var EVROWS=null;
function regroup(){var box=document.getElementById('evol');if(!box)return;if(EVROWS===null)EVROWS=[].slice.call(box.querySelectorAll('.evr'));
 box.innerHTML='';
 if(!lens){EVROWS.forEach(function(r){box.appendChild(r);});return;}
 var chips=document.querySelectorAll('.pg[data-lens="'+lens+'"] .fchip'),order=[],names={};
 [].forEach.call(chips,function(c){var k=c.getAttribute('data-c');order.push(k);names[k]=c.firstChild.textContent;});
 var groups={},rest=[];
 EVROWS.forEach(function(r){var codes=toks(r,'data-'+lens),g=null;for(var i=0;i<order.length;i++){if(codes.indexOf(order[i])>-1){g=order[i];break;}}
  if(g===null)rest.push(r);else(groups[g]=groups[g]||[]).push(r);});
 function head(t){var h=document.createElement('li');h.className='evgrp';h.textContent=t;box.appendChild(h);}
 order.forEach(function(c){if(groups[c]){head(names[c]);groups[c].forEach(function(r){box.appendChild(r);});}});
 if(rest.length){head('Not tagged to this lens');rest.forEach(function(r){box.appendChild(r);});}
 [].forEach.call(box.querySelectorAll('.evgrp'),function(h){var n=h.nextElementSibling,any=false;while(n&&!n.classList.contains('evgrp')){if(!n.classList.contains('hidden'))any=true;n=n.nextElementSibling;}h.hidden=!any;});}
function renderLens(){[].forEach.call(document.querySelectorAll('.pg'),function(g){g.hidden=(g.getAttribute('data-lens')!==lens);});
 document.getElementById('pillrow').hidden=!lens;
 [].forEach.call(document.querySelectorAll('button[data-lens]'),function(b){b.setAttribute('aria-expanded',b.getAttribute('data-lens')===lens);});regroup();}
var ord=0,ORD=['alphabetical','steepest first','gentlest first'],ORDL=['Order: A–Z','Order: steepest first','Order: gentlest first'];
function nmOf(g){return g.querySelector('th').textContent;}
function pinMine(){['master','master2'].forEach(function(id){var t=document.getElementById(id);if(!t)return;
  [].forEach.call(t.querySelectorAll('tbody.mine'),function(b){b.classList.remove('mine');});
  if(!myj)return;var b=t.querySelector('tbody.mg[data-code="'+myj+'"]');if(!b)return;b.classList.add('mine');
  var gb=t.querySelector('tbody.gb');if(gb)gb.parentNode.insertBefore(b,gb.nextSibling);else t.insertBefore(b,t.querySelector('tbody'));});}
function applyOrder(){var t=document.getElementById('master'),gs=[].slice.call(t.querySelectorAll('tbody.mg:not(.gb)'));
 gs.sort(function(a,b){if(ord===0)return nmOf(a).localeCompare(nmOf(b));
  var x=a.getAttribute('data-sort'),y=b.getAttribute('data-sort');
  if(x===''&&y==='')return nmOf(a).localeCompare(nmOf(b));if(x==='')return 1;if(y==='')return -1;
  var d=(ord===1)?(parseFloat(y)-parseFloat(x)):(parseFloat(x)-parseFloat(y));return d||nmOf(a).localeCompare(nmOf(b));});
 gs.forEach(function(g){t.appendChild(g);});
 var t2=document.getElementById('master2');if(t2){var g2=[].slice.call(t2.querySelectorAll('tbody.mg'));g2.sort(function(a,b){return nmOf(a).localeCompare(nmOf(b));});g2.forEach(function(g){t2.appendChild(g);});}
 pinMine();}
function sortMaster(){ord=(ord+1)%3;applyOrder();
 var bt=document.getElementById('msort');bt.textContent=ORDL[ord];bt.setAttribute('aria-label','Change table order, currently '+ORD[ord]);
 document.getElementById('th-max').setAttribute('aria-sort',ord===0?'none':(ord===1?'descending':'ascending'));
 say('Table order: '+ORD[ord]+'.');}
function openJurisdiction(id){var de=document.getElementById(id);if(!de)return;var par=de.closest('details.alljx');if(par)par.open=true;de.open=true;
 de.scrollIntoView({block:'start'});var sm=de.querySelector('summary');if(sm)sm.focus();}
document.addEventListener('click',function(ev){var ja=ev.target.closest('a.jlink');if(ja){ev.preventDefault();openJurisdiction(ja.getAttribute('href').slice(1));return;}
 var t=ev.target.closest('button');if(!t)return;
 if(t.classList.contains('cite')){openCite(t.getAttribute('data-ref'),t);}
 else if(t.id==='cdlg-close'){closeDlg('cdlg');}
 else if(t.id==='msort'){sortMaster();}
 else if(t.hasAttribute('data-lens')){var ln=t.getAttribute('data-lens');lens=(lens===ln)?'':ln;renderLens();writeHash();}
 else if(t.classList.contains('fchip')){var f=t.getAttribute('data-f'),c=t.getAttribute('data-c'),i=sel[f].indexOf(c);if(i>-1)sel[f].splice(i,1);else sel[f].push(c);applyFilter(true);writeHash();}
 else if(t.id==='clear'){sel={pop:[],icf:[],need:[]};applyFilter(true);writeHash();}});
document.addEventListener('change',function(e){var t=e.target;if(t.matches&&t.matches('select[data-u]')){prefs[t.getAttribute('data-u')]=t.value;renderUnits();writeHash();}});
document.getElementById('onlyspec').addEventListener('change',function(e){onlySpec=e.target.checked;applyFilter(true);writeHash();});
['cdlg'].forEach(function(id){var dg=document.getElementById(id);dg.addEventListener('click',function(e){if(e.target===this)closeDlg(id);});
 dg.addEventListener('close',function(){if(dg._opener&&dg._opener.focus&&document.activeElement===document.body)dg._opener.focus();});});
document.getElementById('myj').addEventListener('change',function(e){myj=e.target.value;pinMine();if(!myj)applyOrder();writeHash();say(myj?'Showing '+e.target.options[e.target.selectedIndex].text+' first in the tables.':'Tables back in order.');});
var secs=[].slice.call(document.querySelectorAll('.section')),navl={};[].forEach.call(document.querySelectorAll('[data-snav]'),function(a){navl[a.getAttribute('data-snav')]=a;});
function spy(){var cur='main',lim=window.innerHeight*0.35;secs.forEach(function(s2){if(s2.getBoundingClientRect().top<=lim)cur=s2.id;});
 if(secs.length&&window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-4)cur=secs[secs.length-1].id;
 for(var k in navl){if(k===cur)navl[k].setAttribute('aria-current','true');else navl[k].removeAttribute('aria-current');}
 var nc=document.getElementById('navcur');if(nc&&navl[cur])nc.textContent=navl[cur].textContent.trim();}
if(window.matchMedia&&window.matchMedia('(max-width:760px)').matches){var nd=document.querySelector('.navd');if(nd)nd.open=false;}
var tick=false;window.addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(function(){spy();tick=false;});}},{passive:true});window.addEventListener('resize',spy);
readHash();document.getElementById('onlyspec').checked=onlySpec;document.getElementById('myj').value=myj;addCounts();renderUnits();applyFilter(false);renderLens();applyOrder();spy();
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
