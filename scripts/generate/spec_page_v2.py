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
EVIDENCE_LABEL = {"in-library": "Evidence",
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
    d["pop_cat"] = {r[0]: r[1] for r in db.execute("SELECT population_code, category FROM populations")}
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
                                 metadata_quality, verification_status, source_type, first_author_last, first_author_first,
                                 author_count, author_count_is_complete, is_corporate_primary, journal_name, volume, issue,
                                 pages, pages_start, pages_end, article_number, publisher, institution, standard_number,
                                 report_number, edition
                          FROM evidence_sources WHERE ref_id=?""", (ref,)).fetchone()
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


# ---------------------------------------------------------------- APA citations
_VANC = re.compile(r"^(?P<last>[A-Z][\w'’\- ]*?) (?P<ini>[A-Z]{1,3})$")


def _initials(first):
    if not first:
        return ""
    first = first.strip()
    if "." in first:
        return re.sub(r"\.(?=[^\s\-])", ". ", first).strip()
    if first.isupper() and len(first) <= 3:
        return ". ".join(first) + "."
    out = []
    for tok in re.split(r"([ \-])", first):
        if tok in (" ", "-"):
            out.append(tok)
        elif tok:
            out.append(tok[0] + ".")
    return "".join(out)


def _vancouver_authors(display):
    """'Sanford JA, Story M, & Jones M' -> [('Sanford', 'J. A.'), ...] or None when the display is not in that form."""
    if not display or "," not in display:
        return None
    out = []
    for part in re.split(r",\s*(?:&\s*)?|\s+&\s+", display.strip()):
        m = _VANC.match(part.strip())
        if not m:
            return None
        out.append((m.group("last"), ". ".join(m.group("ini")) + "."))
    return out or None


def apa_authors(s):
    """Return (reference-list author string, in-text author string, author list complete?)."""
    if s["is_corporate_primary"] or not s["first_author_last"]:
        name = s["author_display"] or s["publisher"] or "Unknown"
        return name, name, True
    vanc = _vancouver_authors(s["author_display"]) if s["author_count_is_complete"] else None
    if vanc and len(vanc) == (s["author_count"] or len(vanc)):
        parts = [f"{a}, {b}" for a, b in vanc]
        ref = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + ", & " + parts[-1]
        if len(vanc) == 1:
            intext = vanc[0][0]
        elif len(vanc) == 2:
            intext = f"{vanc[0][0]} & {vanc[1][0]}"
        else:
            intext = f"{vanc[0][0]} et al."
        return ref, intext, True
    last, ini = s["first_author_last"], _initials(s["first_author_first"])
    first = f"{last}, {ini}" if ini else last
    if (s["author_count"] or 1) > 1 or not s["author_count_is_complete"]:
        return first + ", et al.", last + " et al.", bool(s["author_count_is_complete"])
    return first, last, True


def _end(t):
    t = (t or "").strip()
    return t if t[-1:] in ".?!" else t + "."


def apa(s):
    """Return (in-text label, full APA reference as HTML, author list complete?)."""
    ref_auth, intext, complete = apa_authors(s)
    year = s["pub_year"] or "n.d."
    title = s["pub_title"] or ""
    link = f'https://doi.org/{s["doi"]}' if s["doi"] else (s["url"] or "")
    link_h = f' <a href="{escape(link)}" target="_blank" rel="noopener">{escape(link)}</a>' if link else ""
    if s["source_type"] == "journal_article" and s["journal_name"]:
        vol = f', <i>{escape(str(s["volume"]))}</i>' if s["volume"] else ""
        iss = f'({escape(str(s["issue"]))})' if s["issue"] else ""
        pg = s["pages"] or (f'{s["pages_start"]}-{s["pages_end"]}' if s["pages_start"] and s["pages_end"] else (s["article_number"] or ""))
        pgh = f", {escape(str(pg))}" if pg else ""
        body = f'{escape(_end(title))} <i>{escape(s["journal_name"])}</i>{vol}{iss}{pgh}.'
    else:
        ident = s["standard_number"] or s["report_number"] or s["edition"]
        ident_h = f" ({escape(ident)})" if ident and ident not in title else ""
        pub = s["publisher"] or s["institution"]
        pub_h = f" {escape(_end(pub))}" if pub and pub != ref_auth else ""
        body = f'<i>{escape(title)}</i>{ident_h}.{pub_h}'
    return f"{intext}, {year}", f'{escape(ref_auth)} ({escape(str(year))}). {body}{link_h}', complete


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

    cited = {}

    def cite_btn(ref):
        if ref not in cited:
            sx = d["src"](ref)
            label, html, complete = apa(sx)
            pages = [{"item": r[0], "name": r[1]} for r in d["db"].execute(
                """SELECT DISTINCT i.item_code, i.name FROM source_slug_links l JOIN items i ON i.bpc_source_slug = l.slug
                   WHERE l.ref_id = ? ORDER BY i.item_code""", (ref,))]
            if code not in {p["item"] for p in pages}:
                pages.insert(0, {"item": code, "name": title})
            cited[ref] = {"label": label, "apa": html, "complete": complete, "tier": sx["tier"], "type": sx["evidence_type"],
                          "status": sx["verification_status"], "quality": sx["metadata_quality"], "pages": pages}
        return f'<button type="button" class="cite" data-ref="{escape(ref)}" aria-haspopup="dialog">({escape(cited[ref]["label"])})</button>'

    def cited_under(ref):
        cite_btn(ref)
        links = []
        for p in cited[ref]["pages"]:
            f = f'{p["item"].lower()}.html'
            if p["item"] == code:
                links.append("<b>this page</b>")
            elif (OUT_DIR / f).exists():
                links.append(f'<a href="{escape(f)}">{escape(p["item"])}</a>')
            else:
                links.append(escape(p["item"]))
        return f'<p class="citedon"><span class="tg-l">Cited on</span> {", ".join(links)}</p>'

    # ---- why it matters
    why = []
    for w in page["why_it_matters"]:
        refs = ""
        if w.get("refs"):
            refs = " " + " ".join(cite_btn(r) for r in w["refs"])
        why.append(f'<li><span class="ev ev-{w["evidence"]}">{escape(EVIDENCE_LABEL[w["evidence"]])}</span>'
                   f'<span class="li-text">{rt(w["text"])}{refs}</span></li>')

    # ---- values
    STATUS_NOTE = {"provisional": "", "regulatory": "", "method": ""}

    def value_row(r, scope):
        """One accordion row: who + the answer on the top line; basis, sources and tags inside."""
        pops, icf, needs = r.get("populations", []), r.get("icf", []), r.get("needs", [])
        tags = ""
        if scope == "group":
            tags = (f'<p class="vtags"><span class="tg-l">Groups</span>{chips(pops, d["pops"], "pop")}'
                    f'<span class="tg-l">ICF</span>{chips(icf, d["icf"], "icf")}'
                    f'<span class="tg-l">Needs</span>{chips(needs, d["needs"], "need", with_code=False)}</p>')
        refs = ""
        if r.get("refs"):
            refs = '<p class="vrefs">Sources: ' + " ".join(cite_btn(x) for x in r["refs"]) + "</p>"
        return (f'<details class="vrow fi" {tagattrs(pops, icf, needs, scope)}>'
                f'<summary><span class="vwho">{escape(r["who"])}</span>'
                f'<span class="vans">{rt(r["statement"])}<small>{escape(STATUS_NOTE.get(r["status"], ""))}</small></span></summary>'
                f'<div class="vbody"><p>{rt(r["basis"])}</p>{refs}{tags}</div></details>')

    # A value with no evidence ("Not set") is not shown at all: absence is the signal.
    v = {k: [r for r in rows if r["status"] != "no-evidence"] for k, rows in page["values"].items()}
    values_html = "".join(
        f'<p class="vgrp">{label}</p>' + "".join(value_row(r, scope) for r in v[scope])
        for scope, label in (("universal", "Everyone"), ("group", "Specific groups"), ("person", "One person"))
        if v[scope])

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
                parts.append(f'<li>{cite_btn(ref)} {escape(s["pub_title"])}</li>')
            kb = f'<div class="blk"><h5>In the Guidebook library</h5><ul>{"".join(parts)}</ul></div>'
        name = JURISDICTION_NAMES.get(j["code"], j["code"])
        return (f'<details class="jur fi" id="j-{j["code"]}" data-scope="universal" data-pop="" data-icf="" data-need="{" ".join(needs)}" data-has="1" data-code="{j["code"]}">'
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

    # ---- master comparison table: one row per jurisdiction, values only
    def mcell(code, text):
        if not text:
            return '<td class="mnone">&mdash;</td>'
        return f'<td><button type="button" class="mval" data-code="{code}" aria-haspopup="dialog">{rt(text)}</button></td>'

    def master_row(code):
        name = JURISDICTION_NAMES.get(code, code)
        j = by_code.get(code)
        if not j:
            return (f'<tr class="mrow empty" data-has="0" data-sort=""><th scope="row">{escape(name)}<small>{escape(code)}</small></th>'
                    f'<td class="mnone" colspan="5">No entry yet</td></tr>')
        lvl_label, lvl_cls = LEVELS[j["level"]]
        m = j.get("master")
        std = f'<td class="mstd">{escape(j["standard"])}<small>{escape(j["edition"])}</small></td>'
        ver = f'<td><span class="pill {lvl_cls}">{escape(lvl_label)}</span></td>'
        if m:
            cells = mcell(code, m.get("preferred")) + mcell(code, m.get("max")) + mcell(code, m.get("landing_limit"))
            key = m.get("sort")
        else:
            cells = (f'<td colspan="3"><button type="button" class="mval" data-code="{code}" aria-haspopup="dialog">{rt(j["headline"])}</button>'
                     f'<small class="mnote">summary only; see entry</small></td>')
            key = None
        return (f'<tr class="mrow" data-has="1" data-sort="{"" if key is None else key}">'
                f'<th scope="row">{escape(name)}<small>{escape(code)}</small></th>{std}{cells}{ver}</tr>')

    master_rows = "".join(master_row(c) for c in have + none)

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
            f'<details class="ev-row fi" {tag}><summary>'
            f'<span class="e-cite">{apa(s)[1]}</span>'
            f'<span class="j-badges"><span class="pill info">{escape(e["role"])}</span><span class="pill tier">tier {s["tier"]}</span></span></summary>'
            f'<div class="j-body"><p>{rt(e["relevance"])}</p><p>{cite_btn(e["ref"])}</p>{cited_under(e["ref"])}'
            f'<div class="tags"><span class="tg-l">Study population tags</span>{escape(sub_txt)} <em>({reviewed})</em></div>'
            f'<div class="tags"><span class="tg-l">ICF</span>{chips(s["icf"], d["icf"], "icf")}'
            f'<span class="tg-l">Needs</span>{chips(s["needs"], d["needs"], "need", with_code=False)}</div>'
            f'<p class="checked">{escape(s["metadata_quality"] or "")} &middot; {escape(s["verification_status"] or "")} &middot; {doi}</p></div></details>')

    # ---- gaps
    gap_html = "".join(
        f'<details class="gap"><summary><span class="ref">{escape(g["gap_id"])}</span><span class="pill {"gap" if g["status"].startswith("OPEN") else "none"}">{escape(g["status"])}</span>'
        f'<span class="e-cite">{escape((g["description"] or "")[:150])}...</span></summary><div class="j-body"><p>{escape(g["description"] or "")}</p></div></details>'
        for g in d["gaps"])

    # ---- filter facets (only codes that occur on the page)
    def facet_buttons(kind, codes, table, label_fn, group_of=None, group_names=None):
        def chip(c):
            return (f'<button type="button" class="fchip" data-f="{kind}" data-c="{escape(c)}" aria-pressed="false">'
                    f'{label_fn(c, table[c])}</button>')
        if not group_of:
            return f'<div class="fchips">{"".join(chip(c) for c in sorted(codes))}</div>'
        groups = {}
        for c in sorted(codes):
            groups.setdefault(group_of(c), []).append(c)
        return "".join(
            f'<div class="fsub"><span class="fgl">{escape((group_names or {}).get(g, g))}</span>'
            f'<div class="fchips">{"".join(chip(c) for c in cs)}</div></div>'
            for g, cs in sorted(groups.items(), key=lambda kv: str(kv[0])))
    ICF_CH = {"b": "Body functions", "d": "Activities and participation", "s": "Body structures", "e": "Environment"}
    pop_btn = facet_buttons("pop", {p for p in facets["pop"] if p != "ALL"}, d["pops"],
                            lambda c, n: f'<b>{escape(c)}</b> {escape(n[:1].upper() + n[1:])}',
                            group_of=lambda c: d["pop_cat"].get(c, "other"),
                            group_names={"mobility": "Mobility", "neurological": "Neurological", "pain_fatigue": "Pain and fatigue",
                                         "sensory": "Sensory", "cognitive": "Cognitive", "developmental": "Developmental",
                                         "mental_health": "Mental health", "other": "Other"})
    icf_btn = facet_buttons("icf", facets["icf"], d["icf"], lambda c, n: f'<b>{escape(c)}</b> {escape(n)}',
                            group_of=lambda c: c[:1], group_names=ICF_CH)
    need_btn = facet_buttons("need", facets["need"], d["needs"], lambda c, n: escape(n))

    # ---- at-a-glance tiles: the few numbers a reader came for, computed from the data, never typed in twice
    def slope_tok(v):
        return "{{slope=%.6f|1:%d}}" % (v, round(1 / v))
    tiles = []
    pos = next((TOKEN.search(r["statement"]) for r in page["values"].get("universal", []) if TOKEN.search(r["statement"])), None)
    if pos:
        tiles.append(("Guidebook working position", pos.group(0), "Provisional; see the answers below"))
    maxima = [(j["code"], j["master"]["sort"]) for j in page["jurisdictions"] if j.get("master") and j["master"].get("sort")]
    if maxima:
        counts = {}
        for _, v in maxima:
            counts.setdefault(round(v, 4), []).append(1)
        mv = max(counts, key=lambda k: len(counts[k]))
        tiles.append(("Most common legal maximum", slope_tok(mv), f"{len(counts[mv])} of {len(maxima)} jurisdictions with a stated maximum"))
        gc, gv = min(maxima, key=lambda x: x[1])
        tiles.append(("Gentlest legal maximum", slope_tok(gv), JURISDICTION_NAMES.get(gc, gc)))
    keyfacts = "".join(f'<div><small>{escape(a)}</small><b>{rt(b)}</b><span>{escape(c)}</span></div>' for a, b, c in tiles)

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out = TEMPLATE
    for k, val in {
        "__TITLE__": escape(title), "__CODE__": escape(code), "__QUESTION__": escape(question),
        "__CITES__": json.dumps(cited, ensure_ascii=False).replace("</", "<\\/"), "__KEYFACTS__": keyfacts,
        "__WHY__": "".join(why), "__VALUES__": values_html, "__JURS__": jur_html, "__MASTER_ROWS__": master_rows,
        "__JUR_HAVE__": str(jur_counts[0]), "__JUR_NONE__": str(jur_counts[1]),
        "__EVIDENCE__": "".join(ev_html), "__EXCLUDED__": escape(page["excluded_evidence_note"]),
        "__GAPS__": gap_html or "<p>No open gaps recorded.</p>",
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
[hidden]{display:none!important}.facets{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0}details.facet{flex:1 1 220px;margin:0;background:var(--card)}details.facet>summary{font-family:var(--fu);font-size:14px;font-weight:600;padding:8px 12px}.fnb{color:var(--hit);font-weight:700}.fbody{padding:4px 12px 10px;font-family:var(--fu)}.fsub{margin:6px 0 2px}.fgl{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin:6px 0 3px}.fchips{display:flex;flex-wrap:wrap;gap:5px}.fcount{font-style:normal;opacity:.65;font-size:11px}.fchip.act{background:var(--hit);color:#fff;border-color:var(--hit)}
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
button.cite{font:inherit;font-size:.92em;background:none;border:0;border-bottom:1px dotted var(--accent);color:var(--accent);padding:0 1px;cursor:pointer}
button.cite:hover,button.cite:focus-visible{background:var(--accent-l);outline:2px solid var(--accent)}
.citedon{font-family:var(--fu);font-size:13px;margin:4px 0}
dialog#cdlg{max-width:min(640px,94vw);width:100%;border:1px solid var(--border);border-radius:10px;background:var(--card);color:var(--ink);padding:16px 18px}
dialog#cdlg::backdrop{background:rgba(0,0,0,.45)}#cdlg .apa{font-size:15px;line-height:1.5;padding-left:2em;text-indent:-2em;margin:0 0 10px}
#cdlg .meta{font-family:var(--fu);font-size:12.5px;color:var(--muted);margin:0 0 8px}#cdlg ul{padding-left:18px;margin:4px 0 0}
#cdlg .dact{display:flex;justify-content:flex-end;margin-top:12px}#cdlg .dact button{font-family:var(--fu);border:1px solid var(--border);border-radius:6px;padding:5px 12px;background:var(--card);color:var(--ink);cursor:pointer}
.kf{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px;margin:14px 0}
.kf>div{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:12px 16px;font-family:var(--fu)}
.kf small{display:block;font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.kf b{display:block;font-size:34px;line-height:1.15;margin:2px 0;color:var(--accent)}.kf span{font-size:12.5px;color:var(--muted)}
.vgrp{font-family:var(--fu);font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin:16px 0 2px}
details.vrow{border:0;border-bottom:1px solid var(--border);border-radius:0;background:none;margin:0}
.vrow>summary{display:grid;grid-template-columns:minmax(150px,1fr) 3fr;gap:4px 16px;padding:10px 4px 10px 22px;font-family:var(--fu);align-items:baseline;position:relative}
.vrow>summary::before{position:absolute;left:4px}.vrow[open]>summary{border-bottom:0}
.vwho{color:var(--muted);font-size:14px}.vans{font-size:21px;font-weight:700}.vans small{font-size:12px;font-weight:400;color:var(--muted);margin-left:6px}
.vbody{padding:0 4px 12px 22px;font-size:14px;max-width:70ch}.vbody p{margin:0 0 8px}.vtags{font-family:var(--fu);font-size:12px;display:flex;flex-wrap:wrap;gap:4px;align-items:center}.vrefs{font-family:var(--fu);font-size:13px}
button.mval{font-weight:700}
.mh{font-family:var(--fu);font-size:16px;margin:14px 0 6px}.mhelp{font-size:13px;color:var(--muted);margin:0 0 8px}
.mwrap{overflow-x:auto;margin-bottom:14px;border:1px solid var(--border);border-radius:8px}
table.master{border-collapse:collapse;width:100%;font-family:var(--fu);font-size:13.5px;min-width:760px}
table.master th,table.master td{padding:7px 10px;border-bottom:1px solid var(--border);text-align:left;vertical-align:top}
table.master thead th{background:var(--accent-l);font-size:12px;text-transform:uppercase;letter-spacing:.03em;position:sticky;top:0}
table.master tbody th{font-weight:700;white-space:nowrap}table.master small{display:block;font-weight:400;color:var(--muted);font-size:11.5px}
table.master tr.empty{opacity:.6}table.master tr.hidden{display:none}.mnone{color:var(--muted)}
.mstd{max-width:230px}.mnote{margin-top:2px}
button.mval{font:inherit;background:none;border:0;border-bottom:1px dotted var(--accent);color:var(--ink);text-align:left;padding:0;cursor:pointer}
button.mval:hover,button.mval:focus-visible{background:var(--accent-l);outline:2px solid var(--accent)}
button.msort{font:inherit;text-transform:inherit;letter-spacing:inherit;background:none;border:0;color:inherit;cursor:pointer;padding:0;font-weight:700}
dialog#jdlg{max-width:min(720px,94vw);width:100%;border:1px solid var(--border);border-radius:10px;background:var(--card);color:var(--ink);padding:16px 18px}
dialog#jdlg::backdrop{background:rgba(0,0,0,.45)}#jdlg h4{margin:0 0 8px;font-family:var(--fu)}#jdlg .jd{max-height:60vh;overflow:auto;font-size:14px}
#jdlg .dact{display:flex;gap:8px;justify-content:flex-end;margin-top:12px}#jdlg .dact button{font-family:var(--fu);border:1px solid var(--border);border-radius:6px;padding:5px 12px;background:var(--card);color:var(--ink);cursor:pointer}
.jur.flash{box-shadow:0 0 0 3px var(--accent)}
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
<div class="kf" aria-label="At a glance">__KEYFACTS__</div>
<div class="status" role="note"><b>Pilot page &mdash; read the status.</b> Values marked <i>provisional</i> are not yet supported by evidence. Each jurisdiction figure is labelled by how it was verified (primary source read, official excerpt, secondary source, or earlier project extraction); read the label before relying on a figure. Population, ICF and access-need codes and their tags are <b>provisional and unreviewed</b>. Curated text is staged in <code>data/spec_pages/__CODE__.json</code> until a specification table exists in the database.</div>

<div class="controls" id="controls" aria-label="Page controls">
<div class="crow"><span class="cl">Units</span>
 <span class="seg" role="group" aria-label="Length units"><button type="button" data-u="len" data-m="met" aria-pressed="true">Metric (mm, m)</button><button type="button" data-u="len" data-m="imp" aria-pressed="false">Imperial (in, ft)</button><button type="button" data-u="len" data-m="stated" aria-pressed="false">As stated in source</button></span>
 <span class="seg" role="group" aria-label="Slope units"><button type="button" data-u="slope" data-m="ratio" aria-pressed="true">Ratio (1:n)</button><button type="button" data-u="slope" data-m="pct" aria-pressed="false">Percent</button><button type="button" data-u="slope" data-m="deg" aria-pressed="false">Degrees</button><button type="button" data-u="slope" data-m="stated" aria-pressed="false">As stated</button></span>
</div>
<div id="facets" class="facets" aria-label="Filter the page">
 <details class="facet"><summary>Who it's for<span class="fnb" id="fn-pop"></span></summary><div class="fbody" id="fg-pop">__POPBTN__</div></details>
 <details class="facet"><summary>ICF code<span class="fnb" id="fn-icf"></span></summary><div class="fbody" id="fg-icf">__ICFBTN__</div></details>
 <details class="facet"><summary>Access need<span class="fnb" id="fn-need"></span></summary><div class="fbody" id="fg-need">__NEEDBTN__</div></details>
</div>
<div class="crow" id="activerow" hidden><span class="cl">Active filters</span><span class="fgroup" id="activelist"></span></div>
<div class="crow"><label><input type="checkbox" id="onlyspec"> Hide general (everyone) items when a filter is on</label>
 <button type="button" class="clear" id="clear">Clear filters</button><span class="count" id="count" role="status" aria-live="polite"></span></div>
</div>

<section id="why"><h2>Why it matters</h2><ul class="why">__WHY__</ul></section>

<section id="values"><h2>The answers</h2>__VALUES__</section>

<section id="jurisdictions"><h2>Jurisdiction comparison</h2>
<p style="font-size:14px;color:var(--muted);margin-bottom:10px">__JUR_HAVE__ jurisdictions with an entry and __JUR_NONE__ with none yet. Each row shows the standard, clause, value and a note; open it for everything else. These are general legal requirements that apply to everyone; with an access-need filter on, the provisions that serve that need are highlighted.</p>
<h3 class="mh">At a glance: ramp gradient by jurisdiction</h3>
<p class="mhelp">One row per jurisdiction. Click a value for the detail. Values follow the unit selector above. Rows are labelled by how well they were verified; sort by the steepest maximum to see which jurisdictions allow the steepest ramps.</p>
<div class="mwrap"><table class="master" id="master"><thead><tr><th scope="col">Jurisdiction</th><th scope="col">Standard</th><th scope="col">Preferred</th><th scope="col"><button type="button" id="msort" class="msort" aria-label="Sort by maximum gradient, steepest first">Maximum (and when) &#8645;</button></th><th scope="col">Limit between landings</th><th scope="col">Verification</th></tr></thead><tbody>__MASTER_ROWS__</tbody></table></div>
<dialog id="jdlg" aria-labelledby="jdlg-t"><div id="jdlg-body"></div><div class="dact"><button type="button" id="jdlg-full">Open full entry below</button><button type="button" id="jdlg-close">Close</button></div></dialog>
<h3 class="mh">Full entries</h3>
<div class="jbar"><button type="button" id="expand">Expand all</button><button type="button" id="collapse">Collapse all</button>
<label><input type="checkbox" id="hidenone"> Hide jurisdictions with no entry yet</label></div>
<div id="jlist">__JURS__</div></section>

<section id="evidence"><h2>Evidence in the library</h2>__EVIDENCE__
<p style="font-size:13px;color:var(--muted);margin-top:8px">__EXCLUDED__</p></section>



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
  var kind=el.classList.contains('vrow')?'vcard':(el.classList.contains('jur')?'jur':'ev');tot[kind]++;
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
 ['pop','icf','need'].forEach(function(f){if(sel[f].length)p.push(f+'='+sel[f].join(','));});if(onlySpec)p.push('spec=1');if(lens)p.push('lens='+lens);
 try{history.replaceState(null,'',p.length?'#'+p.join('&'):location.pathname+location.search);}catch(e){}
 try{localStorage.setItem('gb-units',JSON.stringify(prefs));}catch(e){}}
function readHash(){try{var s=JSON.parse(localStorage.getItem('gb-units')||'null');if(s){prefs.len=s.len||prefs.len;prefs.slope=s.slope||prefs.slope;}}catch(e){}
 var h=location.hash.replace(/^#/,'');if(!h)return;h.split('&').forEach(function(kv){var a=kv.split('='),k=a[0],v=a[1]||'';
  if(k==='len'||k==='slope')prefs[k]=v;else if(k==='pop'||k==='icf'||k==='need')sel[k]=v?v.split(','):[];else if(k==='spec')onlySpec=v==='1';else if(k==='lens')lens=v;});}
document.addEventListener('click',function(ev){var t=ev.target.closest('button');if(!t)return;
 if(t.classList.contains('cite')){openCite(t.getAttribute('data-ref'));}
 else if(t.id==='cdlg-close'){document.getElementById('cdlg').close();}
 else if(t.classList.contains('mval')){openJ(t.getAttribute('data-code'));}
 else if(t.id==='jdlg-close'){document.getElementById('jdlg').close();}
 else if(t.id==='jdlg-full'){var dg=document.getElementById('jdlg'),c2=dg.getAttribute('data-code');dg.close();var de=document.getElementById('j-'+c2);if(de){de.open=true;de.scrollIntoView({behavior:'smooth',block:'start'});de.classList.add('flash');setTimeout(function(){de.classList.remove('flash');},2000);}}
 else if(t.id==='msort'){sortMaster();}
 else if(t.hasAttribute('data-u')){prefs[t.getAttribute('data-u')]=t.getAttribute('data-m');renderUnits();writeHash();}
 else if(t.classList.contains('fchip')){var f=t.getAttribute('data-f'),c=t.getAttribute('data-c'),i=sel[f].indexOf(c);if(i>-1)sel[f].splice(i,1);else sel[f].push(c);applyFilter();renderLens();writeHash();}
 else if(t.id==='clear'){sel={pop:[],icf:[],need:[]};applyFilter();renderLens();writeHash();}
 else if(t.id==='expand'||t.id==='collapse'){var d=document.querySelectorAll('#jlist details:not(.hidden)');for(var i2=0;i2<d.length;i2++)d[i2].open=(t.id==='expand');}
 else if(t.id==='vt'||t.id==='vq'){var q=t.id==='vq';document.body.classList.toggle('q',q);document.getElementById('vt').classList.toggle('on',!q);document.getElementById('vq').classList.toggle('on',q);}});
document.getElementById('onlyspec').addEventListener('change',function(e){onlySpec=e.target.checked;applyFilter();writeHash();});
var CITES=null;function cites(){if(CITES===null){try{CITES=JSON.parse(document.getElementById('cites').textContent);}catch(e){CITES={};}}return CITES;}
function esc(t){return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;');}
function openCite(ref){var c=cites()[ref];if(!c)return;var here=location.pathname.split('/').pop().replace('.html','').toUpperCase();
 var pg=c.pages.map(function(p){return '<li>'+(p.item===here?'<b>'+p.item+'</b> (this page)':'<a href="'+p.item.toLowerCase()+'.html">'+p.item+'</a>')+' &mdash; '+esc(p.name)+'</li>';}).join('');
 document.getElementById('cdlg-body').innerHTML='<h4 id="cdlg-t">Bibliographic citation</h4><p class="apa">'+c.apa+'</p>'
  +'<p class="meta">Tier '+c.tier+' &middot; '+esc(c.type||'')+' &middot; '+esc(c.status||'')+(c.complete?'':' &middot; author list incomplete in the library')+'</p>'
  +'<h5>Cited on these pages</h5><ul>'+pg+'</ul>';
 var dg=document.getElementById('cdlg');if(dg.showModal)dg.showModal();else dg.setAttribute('open','');}
var lens='';var LENSLABEL={pop:"Who it's for",icf:'ICF code',need:'Access need'};
var countsDone=false;
function renderLens(){
 if(!countsDone){countsDone=true;var chips=document.querySelectorAll('.fchip');for(var i=0;i<chips.length;i++){var f=chips[i].getAttribute('data-f'),c=chips[i].getAttribute('data-c'),n=0,its=document.querySelectorAll('.vrow,.ev-row');
  for(var k=0;k<its.length;k++){if(toks(its[k],'data-'+f).indexOf(c)>-1)n++;}
  var tag=document.createElement('i');tag.className='fcount';tag.textContent=' '+n;chips[i].appendChild(tag);}}
 var al=document.getElementById('activelist');al.innerHTML='';var any=false;
 ['pop','icf','need'].forEach(function(f){var badge=document.getElementById('fn-'+f);badge.textContent=sel[f].length?' ('+sel[f].length+')':'';
  sel[f].forEach(function(c){any=true;var bt=document.createElement('button');bt.type='button';bt.className='fchip act';bt.setAttribute('data-f',f);bt.setAttribute('data-c',c);bt.setAttribute('aria-pressed','true');
   bt.setAttribute('aria-label','Remove filter '+LENSLABEL[f]+' '+c);bt.textContent=LENSLABEL[f]+': '+c+' \u00d7';al.appendChild(bt);});});
 document.getElementById('activerow').hidden=!any;
 var ch=document.querySelectorAll('#facets .fchip');for(var j=0;j<ch.length;j++){var f2=ch[j].getAttribute('data-f'),c2=ch[j].getAttribute('data-c');ch[j].setAttribute('aria-pressed',sel[f2].indexOf(c2)>-1);}}
function openJ(code){var src=document.getElementById('j-'+code);if(!src)return;var dg=document.getElementById('jdlg');
 var s=src.querySelector('summary'),body=src.querySelector('.j-body');
 var name=s.querySelector('.j-name').firstChild.textContent,std=s.querySelector('.j-std b').textContent;
 document.getElementById('jdlg-body').innerHTML='<h4 id="jdlg-t">'+name+' &middot; '+std+'</h4><div class="jd">'+body.innerHTML+'</div>';
 dg.setAttribute('data-code',code);renderUnits();if(dg.showModal)dg.showModal();else dg.setAttribute('open','');}
var msortDir=0;
function sortMaster(){var tb=document.querySelector('#master tbody'),rows=[].slice.call(tb.querySelectorAll('tr'));msortDir=msortDir===1?-1:1;
 rows.sort(function(a,b){var x=a.getAttribute('data-sort'),y=b.getAttribute('data-sort');
  if(x===''&&y==='')return a.querySelector('th').textContent.localeCompare(b.querySelector('th').textContent);
  if(x==='')return 1;if(y==='')return -1;return (parseFloat(y)-parseFloat(x))*msortDir;});
 rows.forEach(function(r){tb.appendChild(r);});}
function applyMaster(){var h=document.getElementById('hidenone').checked,r=document.querySelectorAll('#master tr.mrow');for(var i=0;i<r.length;i++){r[i].classList.toggle('hidden',h&&r[i].getAttribute('data-has')==='0');}}
document.getElementById('hidenone').addEventListener('change',function(){applyMaster();});
document.getElementById('jdlg').addEventListener('click',function(e){if(e.target===this)this.close();});
document.getElementById('hidenone').addEventListener('change',applyFilter);
readHash();document.getElementById('onlyspec').checked=onlySpec;renderUnits();applyFilter();renderLens();
})();
</script>
<dialog id="cdlg" aria-labelledby="cdlg-t"><div id="cdlg-body"></div><div class="dact"><button type="button" id="cdlg-close">Close</button></div></dialog>
<script type="application/json" id="cites">__CITES__</script>
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
