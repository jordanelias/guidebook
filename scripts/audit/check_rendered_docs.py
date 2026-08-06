#!/usr/bin/env python3
"""
check_rendered_docs.py — gate the hand-authored rendered documents (specs/*.html)
against the canonical database and against their own integrity requirements.

WHY THIS EXISTS (session 2026-07-24/25). Three independent adversarial audits of
specs/e-08-brief.html found ~90 defects. Every one of the serious ones was
mechanically checkable and none was caught by re-reading the prose:

  * three Deaf authors misnamed on the sources carrying the Co-1 grade, and the
    Deaf collaborators dropped from the citation entirely;
  * a citation list showing 3 of 7 governing refs plus one non-governing ref,
    silently hiding a Tier-6 statute and a non-ASL ethnography;
  * a print stylesheet that hid every source, tier, caveat and legal disclaimer
    at exactly the moment the document becomes an advocacy or policy instrument;
  * a population marked `applies` in the page and `context_dependent` in the DB,
    producing a visibly wrong count and a duplicated group heading;
  * a full-strength (●) grade rendered over a determination whose own record says
    `pending_assessment` with every governing source down-weighted.

A rendered document is a DERIVED SURFACE. It may summarise the record, but it may
not contradict it, and it may not present the record as stronger than it is.

Usage:
    python3 scripts/audit/check_rendered_docs.py [--doc specs/e-08-brief.html]
    python3 scripts/audit/check_rendered_docs.py --all

Honors GUIDEBOOK_DB_PATH. Stdlib only. Exits 1 on any FAIL.
"""
import argparse
import os
import re
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DB = os.environ.get("GUIDEBOOK_DB_PATH", str(REPO / "data" / "guidebook.db"))

# Classes that carry the evidential apparatus. If a document renders citations at
# all, these must survive print and must not depend on script execution.
EVIDENCE_CLASSES = ["pop", "cite", "colophon", "s-meta", "s-status", "honesty"]

findings = []           # (severity, check, doc, message)
def fail(check, doc, msg):  findings.append(("FAIL", check, doc, msg))
def warn(check, doc, msg):  findings.append(("WARN", check, doc, msg))


def conn():
    return sqlite3.connect(f"file:{DB}?mode=ro", uri=True)


def item_code_for(doc):
    """Accepts a Path or a repo-relative string."""
    stem = Path(doc).stem
    m = re.match(r"([a-k]-\d{2})", stem, re.I)
    return m.group(1).upper() if m else None


# ---------------------------------------------------------------- C1 citations
def check_citation_fidelity(html, doc, c):
    """Every REF-ID rendered must exist; surnames stated beside it must match the
    register; and the set shown for a determination must not misrepresent
    governing_refs (no non-governing ref presented as governing, no silent
    omission of a governing ref)."""
    refs = sorted(set(re.findall(r"REF-\d{5}", html)))
    known = {r[0]: (r[1] or "") for r in c.execute(
        "SELECT ref_id, first_author_last FROM evidence_sources")}
    for r in refs:
        if r not in known:
            fail("C1-citation", doc, f"{r} is cited but not in evidence_sources")
            continue
        surname = known[r]
        if not surname:
            continue
        # Look at the rendered text immediately around the ref for a surname claim.
        for m in re.finditer(re.escape(r), html):
            window = re.sub(r"<[^>]+>", " ", html[max(0, m.start() - 700):m.start()])
            # A surname claim looks like "Word, X." or "Word AB (year)".
            claims = re.findall(r"\b([A-Z][a-z]{2,})[,\s]+(?:[A-Z][a-z]*\s*)?[A-Z]?[-A-Za-z]*\s*\(?\d{4}\)?", window[-400:])
            if claims and surname not in window[-400:]:
                warn("C1-citation", doc,
                     f"{r}: register surname {surname!r} not found near the citation "
                     f"(nearby name-like tokens: {sorted(set(claims))[:3]})")
            break

    # governing_refs fidelity, where the doc is about a known item
    code = item_code_for(doc)
    if code:
        for (gr,) in c.execute(
                "SELECT governing_refs FROM evidence_cell_state "
                "WHERE item_code=? AND governing_refs IS NOT NULL", (code,)):
            gov = set(re.findall(r"REF-\d{5}", gr or ""))
            if not gov:
                continue
            # Scope to the panel(s) that actually render this determination — those
            # holding two or more of its governing refs. Refs cited elsewhere in the
            # document support other claims and are not candidates for this cell's
            # governing set. The first version of this check flagged every unrelated
            # reference on the page, which is the kind of noise that gets a gate
            # ignored.
            panels = html.split('<div class="pop"')[1:]
            det = [pl for pl in panels if len(gov & set(re.findall(r"REF-\d{5}", pl))) >= 2]
            shown = set(re.findall(r"REF-\d{5}", "".join(det))) if det else set(refs)
            missing = gov - shown
            if missing:
                fail("C1-governing", doc,
                     f"{code}: governing refs absent from the document: {sorted(missing)}")
            # A ref shown among governing-looking company but not governing must be
            # marked as supporting somewhere in the doc.
            for extra in sorted(shown - gov):
                ctx = html[max(0, html.find(extra) - 400): html.find(extra) + 400].lower()
                if not any(k in ctx for k in ("supporting", "not a governing", "discounted")):
                    warn("C1-governing", doc,
                         f"{code}: {extra} shown alongside governing refs without being "
                         f"marked supporting / discounted / non-governing")


# ------------------------------------------------- C2 epistemic persistence
def check_epistemic_persistence(html, doc):
    """Sources, tiers, caveats and the legal disclaimer must survive print and
    must not be script-contingent. A document whose provenance falls off when
    printed is not a cited document."""
    if "cite-trigger" not in html and "pop-src" not in html:
        return  # no evidential apparatus to protect
    # NOTE: static CSS text cannot resolve the cascade — a later !important rule may
    # legitimately re-show a class an earlier block hides. This check therefore only
    # WARNS, and the authoritative test is the print-emulation assertion in the
    # browser harness (scripts/audit/render_audit.js), which reads computed styles.
    # Learned the hard way: the first version of this check FAILED three classes that
    # the renderer proved visible.
    for block in re.findall(r"@media\s+print\s*\{(.*?)\n\}", html, re.S):
        for cls in EVIDENCE_CLASSES:
            # (?![\w-]) so `.pop` does not match `.pop-close`, which legitimately
            # hides the close button while the panel itself prints.
            sel = rf"\.{re.escape(cls)}(?![\w-])"
            hidden = re.search(rf"{sel}[^{{}}]*\{{[^}}]*display\s*:\s*none", block)
            reshown = re.search(rf"{sel}[^{{}}]*\{{[^}}]*display\s*:\s*(?!none)\w+\s*!important", block)
            if hidden and not reshown:
                warn("C2-print", doc,
                     f"a print block hides .{cls} — verify with the browser harness that a "
                     f"later rule re-shows it; if not, sources/caveats/disclaimer are lost in print")
    # script-contingent evidence
    if re.search(r"\.pop\s*\{[^}]*display\s*:\s*none", html) and "<noscript" not in html:
        warn("C2-nojs", doc,
             "source panels are display:none by default and revealed by script, "
             "with no <noscript> fallback — provenance is unavailable without JS")


# ------------------------------------------------------------ C3 doc↔DB drift
def check_doc_db_drift(html, doc, c):
    """Population applicability hardcoded in the page must match the register."""
    code = item_code_for(doc)
    if not code:
        return
    db = {r[0]: r[1] for r in c.execute(
        "SELECT population_code, applicability FROM item_population_links WHERE item_code=?",
        (code,))}
    if not db:
        return
    # hand-authored entries look like  {k:'LPA', ... t:'applies'|'context'}
    for m in re.finditer(r"\{k:'([A-Z]+)'.*?t:'(applies|context)'", html, re.S):
        pop, t = m.group(1), m.group(2)
        if pop not in db:
            continue
        want = "applies" if db[pop] == "applies" else "context"
        if t != want:
            fail("C3-drift", doc,
                 f"{code}×{pop}: document says {t!r}, register says {db[pop]!r}")
    n_app = sum(1 for v in db.values() if v == "applies")
    n_ctx = len(db) - n_app
    words = {7: "seven", 6: "six", 8: "eight", 5: "five", 9: "nine", 4: "four"}
    txt = re.sub(r"<[^>]+>", " ", html).lower()
    for n, kind in ((n_app, "applies"), (n_ctx, "context")):
        w = words.get(n)
        if w and re.search(rf"\b{w}\b", txt) is None and re.search(rf"\b{n}\b", txt) is None:
            warn("C3-count", doc,
                 f"{code}: register has {n} {kind} populations; that count does not "
                 f"appear in the prose (check any stated tally)")


# -------------------------------------------------------- C4 grade preconditions
def check_grade_preconditions(html, doc, c):
    """A full-strength ● may not be rendered without disclosing a pending
    convergence assessment, wholesale down-weighting, or a T4–T6 governing ref."""
    code = item_code_for(doc)
    if not code or "●" not in html:
        return
    txt = re.sub(r"<[^>]+>", " ", html).lower()
    for cid, in c.execute(
            "SELECT convergence_id FROM evidence_cell_state "
            "WHERE item_code=? AND convergence_id IS NOT NULL", (code,)):
        row = c.execute("SELECT status, down_weighted_sources FROM convergence_assessment "
                        "WHERE convergence_id=?", (cid,)).fetchone()
        if not row:
            continue
        status, dw = row
        if status and status != "assessed" and "pending_assessment" not in txt \
                and "pending" not in txt:
            fail("C4-grade", doc,
                 f"{code}: ● rendered while convergence_assessment is {status!r} and the "
                 f"document does not disclose it")
        if dw and len(re.findall(r"REF-\d{5}", dw)) >= 3 and "down-weight" not in txt:
            fail("C4-grade", doc,
                 f"{code}: ● rendered while all governing sources are recorded as "
                 f"down-weighted, undisclosed")
    for (gr,) in c.execute("SELECT governing_refs FROM evidence_cell_state "
                           "WHERE item_code=? AND governing_refs IS NOT NULL", (code,)):
        for ref in re.findall(r"REF-\d{5}", gr or ""):
            t = c.execute("SELECT tier FROM evidence_sources WHERE ref_id=?", (ref,)).fetchone()
            if t and t[0] and t[0] >= 4:
                if "tier 6" not in txt and "t6" not in txt and "statute" not in txt:
                    fail("C4-grade", doc,
                         f"{code}: governing ref {ref} is Tier {t[0]} (regulatory stratum) "
                         f"under a ● cell, and the document does not surface it")
                break


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", action="append", default=[])
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    docs = [REPO / d for d in args.doc]
    if args.all or not docs:
        docs = sorted((REPO / "specs").glob("*.html"))
    docs = [d for d in docs if d.exists()]
    print(f"EXAMINED: {len(docs)} rendered document(s)")
    if not docs:
        # Exit 1, not 0. This is a BLOCKING check and it used to return 0 here,
        # so deleting or renaming specs/ turned it green — a gate certifying an
        # empty set is indistinguishable from a gate certifying a clean one, and
        # this repo has produced that failure mode six times. `min_items: 1` in
        # the registry enforces the pairing from the other side.
        print("FAIL: no rendered documents found under specs/. This check has "
              "nothing to check, which is not the same as having found nothing "
              "wrong. Either specs/ moved, or the render step did not run.",
              file=sys.stderr)
        return 1

    c = conn()
    for doc in docs:
        html = doc.read_text(encoding="utf-8", errors="replace")
        rel = str(doc.relative_to(REPO))
        check_citation_fidelity(html, rel, c)
        check_epistemic_persistence(html, rel)
        check_doc_db_drift(html, rel, c)
        check_grade_preconditions(html, rel, c)
    c.close()

    fails = [f for f in findings if f[0] == "FAIL"]
    warns = [f for f in findings if f[0] == "WARN"]
    for sev, check, doc, msg in findings:
        print(f"  [{sev}] {check:14} {doc}: {msg}")
    checked = len(docs) * 4
    print(f"\nRESULTS: {checked - len(fails)}/{checked} checks passed "
          f"({len(docs)} document(s), {len(fails)} failure(s), {len(warns)} warning(s))")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
