#!/usr/bin/env python3
"""
scripts/audit/register_integrity_check.py — mechanical check of the five register
integrity invariants (governance/evidence-architecture.md §6) over rendered output.

I1  Tuple identity: every rendering of a cell, in every register, carries the
    identical determination tuple (state, tier_basis, conv, rso, cfo, sha, rule_version).
I2  Floor–anchor pairing: the policymaker rendering must always pair FLOOR with
    ANCHOR (never the floor alone) whenever a regulatory floor exists.
I3  As amended by DR-2026-07-21 Option A: a regulatory-stratum-only cell renders
    as FLAGGED weak-band (○, code-derived) best practice — never unflagged, never
    above the weak band, never suppressed. The absolute form ("no best-practice
    language, ever") was repealed; this checker enforced it until 2026-08-04.
I4  Claim-strength language is drawn only from REGISTER_MAP (imported from the
    renderer — single source of truth), and
I5  no register exceeds its map row: the claim-strength element must EQUAL the
    map text for the cell's tuple-class (saying less is brevity; saying more is
    inflation; saying different is drift). I4 and I5 are checked as one equality.

Mutation discipline: --selftest tampers each invariant in-memory and asserts the
checker FIRES on every tampered variant and passes the untampered document.
Exit 1 on any violation (or any silent selftest miss).
"""
import argparse
import html
import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO_ROOT)
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts", "generate"))

from pilot_renderings import REGISTER_MAP, ROLES, tuple_class  # noqa: E402  (single source of truth)

DEFAULT_DOC = os.path.join(REPO_ROOT, "working", "pilot", "pilot-renderings.html")

RENDER_RE = re.compile(r"<div class='rendering' ([^>]*)>(.*?)</div>", re.S)
ATTR_RE = re.compile(r"data-([a-z-]+)='([^']*)'")
CLAIM_RE = re.compile(r"<p class='claim-strength'>(.*?)</p>", re.S)
TUPLE_KEYS = ("state", "tier-basis", "conv", "rso", "cfo", "sha", "rule-version",
              "reg-refs", "reg-jur")

# I3 lexicon — best-practice language and its synonyms. Lexicon-based checks are
# necessarily incomplete (a synonym list can be outflanked); this list is the
# mechanical floor, and additions belong here, versioned, not scattered in prose.
BP_LEXICON = re.compile(
    r"best[\s-]practice|recommended standard|gold[\s-]standard|design target|"
    r"evidence[\s-]based (?:standard|target|value)|"
    r"evidence (?:\w+\s+){0,3}supports (?:\w+\s+){0,3}as the (?:target|standard)", re.I)

# I5 inflation lexicon — claim strength no register may express anywhere in a
# rendering (claim element OR emphasis body), regardless of tuple-class.
INFLATION_LEXICON = re.compile(
    r"definitively proven|beyond dispute|no further evidence|conclusively "
    r"(?:established|proven|shown)|settled science|indisputabl|irrefutabl", re.I)

# Weak-band flag (DR-2026-07-21 Option A). An RSO rendering may use
# best-practice language ONLY in an element that also carries one of these.
# Plain registers get their own phrasings — a plain reader is not served by "○".
WEAK_FLAG_LEXICON = re.compile(
    r"○|as currently known|code[\s-]derived|weak[\s-]band|"
    r"rules answer, not a research answer|best answer anyone has right now|"
    r"best answer available right now|current regulatory answer|"
    r"NOT academically adjudicated", re.I)

# Markers above the weak band. tier-system §8 puts any regulatory-stratum
# determination at ○; ● and ◐ on such a cell are band errors under
# DR-2026-07-21 §2.3.
ABOVE_BAND_RE = re.compile(r"\[●|\[◐")

PARA_RE = re.compile(r"<p class='emphasis'>(.*?)</p>", re.S)

# Every weak-band map row must carry, per register, a flag AND the
# code-is-not-evidence caveat. The I4/I5 equality cannot supply this: checker
# and renderer share REGISTER_MAP, so a regression IN THE MAP passes equality
# silently — the document would match a map that had stopped telling the truth.
REQUIRED_RSO_MARKERS = {
    "designer":        [("○",), ("not evidence", "is not convergence")],
    "ot":              [("○",), ("not a clinically adjudicated target",)],
    "policymaker":     [("○",), ("not evidence", "not even convergence")],
    "disabled_person": [("rules answer, not a research answer",),
                        ("could change when real evidence arrives",)],
    "carer":           [("not from research", "not from research or lived experience"),
                        ("could change when real evidence arrives",)],
    "advocacy_brief":  [("NO research or lived-experience evidence",),
                        ("advocacy point",)],
}


def lint_register_map(m):
    """Assert the weak-band rows still say what Option A requires them to say.

    Runs unconditionally, document or no document. This is the guard against
    the failure mode that actually happened: the previous RSO row asserted
    convergence for every cell, the renderer emitted it faithfully, and the
    checker's equality test confirmed the document matched the map — while the
    map itself was false for two of the three cells it served.
    """
    errs = []
    for key in ("rso_weak_broad", "rso_weak_single"):
        if key not in m:
            errs.append(f"REGISTER_MAP LINT — weak-band row {key!r} is missing; "
                        f"Option A requires regulatory-stratum cells to render flagged")
            continue
        for role, required in REQUIRED_RSO_MARKERS.items():
            text = m[key].get(role, "")
            for alternatives in required:
                if not any(alt.lower() in text.lower() for alt in alternatives):
                    errs.append(f"REGISTER_MAP LINT — {key}/{role} carries none of "
                                f"{alternatives!r}; Option A requires the weak-band flag and "
                                f"the code-is-not-evidence caveat in every register")
    return errs


def parse(doc):
    out = {}
    for attrs_raw, body in RENDER_RE.findall(doc):
        attrs = dict(ATTR_RE.findall(attrs_raw))
        m = CLAIM_RE.search(body)
        claim = html.unescape(m.group(1)).strip() if m else ""
        out.setdefault(attrs.get("cell", "?"), []).append(
            {"attrs": attrs, "claim": claim, "body": html.unescape(body)})
    return out


def _norm(v):
    """DB value as the document should carry it: NULL is empty, never 'None'."""
    return "" if v is None else str(v)


def check(doc, db_path=None):
    errors = list(lint_register_map(REGISTER_MAP))
    cells = parse(doc)
    if not cells:
        return errors + ["no renderings found in document"]
    db_rows = {}
    if db_path:
        import json as _json
        import sqlite3
        conn = sqlite3.connect(db_path)
        for ic, pc, st, tb, cfo, sha, rv, rso, gr in conn.execute(
                "SELECT item_code, population_code, state, tier_basis, code_floor_only, "
                "derivation_sha, rule_version, regulatory_stratum_only, governing_refs "
                "FROM specifications"):
            refs = _json.loads(gr) if gr else []
            n_jur = 0
            if rso and refs:
                qs = ",".join("?" * len(refs))
                n_jur = conn.execute(
                    f"SELECT COUNT(DISTINCT jurisdiction) FROM evidence_sources "
                    f"WHERE ref_id IN ({qs})", refs).fetchone()[0]
            db_rows[f"{ic}×{pc}"] = dict(state=st, tier_basis=tb or "no basis",
                                         cfo=str(cfo), sha=sha, rule_version=rv,
                                         rso=str(rso or 0),
                                         **{"reg-refs": str(len(refs) if rso else 0),
                                            "reg-jur": str(n_jur)})
        # DB → DOC. The cross-check below only runs doc → DB, so a document
        # that silently OMITS determinations passes it. That is not a
        # hypothetical: this document sat frozen at 7 of 15 cells for weeks
        # because its generator crashed, and the checker's only complaint was an
        # incidental stale population code. Suppression is an integrity failure
        # in its own right under Option A (weak-band cells render flagged, never
        # suppressed) and G8 (pending cells render with disclosure).
        for cell in sorted(set(db_rows) - set(cells)):
            errors.append(
                f"{cell}: COMPLETENESS VIOLATION — specifications row exists but no "
                f"rendering appears in the document; suppression of a determination is an "
                f"integrity failure (Option A: weak-band cells render flagged, never "
                f"suppressed; G8: pending_assessment cells render with disclosure)")
    for cell, renders in cells.items():
        roles_seen = {r["attrs"].get("role") for r in renders}
        missing = set(ROLES) - roles_seen
        if missing:
            errors.append(f"{cell}: missing role renderings: {sorted(missing)}")
        # I1 — identical tuple across renders
        tuples = {tuple(r["attrs"].get(k, "") for k in TUPLE_KEYS) for r in renders}
        if len(tuples) != 1:
            errors.append(f"{cell}: I1 VIOLATION — {len(tuples)} distinct determination "
                          f"tuples across registers: {sorted(tuples)}")
        # DB cross-check — self-reported attributes must match the determination row
        if db_rows:
            row = db_rows.get(cell)
            if row is None:
                errors.append(f"{cell}: rendered but no specifications row exists")
            else:
                for r in renders[:1]:
                    a = r["attrs"]
                    for html_key, db_key in (("state", "state"), ("tier-basis", "tier_basis"),
                                             ("cfo", "cfo"), ("sha", "sha"),
                                             ("rule-version", "rule_version"),
                                             ("rso", "rso"), ("reg-refs", "reg-refs"),
                                             ("reg-jur", "reg-jur")):
                        if a.get(html_key, "") != _norm(row[db_key]):
                            errors.append(f"{cell}: DB CROSS-CHECK VIOLATION — data-{html_key}="
                                          f"{a.get(html_key)!r} but DB says {row[db_key]!r}")
        for r in renders:
            a, role = r["attrs"], r["attrs"].get("role")
            tc = a.get("tuple-class")
            # Repr leak — independent of --db, so it holds even when the checker
            # runs against a fixture. A NULL must render as the empty string;
            # 'None' is a Python repr escaping into published markup.
            for k in ("sha", "rule-version"):
                if a.get(k) == "None":
                    errors.append(f"{cell}/{role}: REPR LEAK — attribute data-{k} publishes "
                                  f"the Python None repr; a NULL must render as empty")
            rso_marker = (a.get("tier-basis", "")).endswith("(regulatory_stratum_only)")
            rso_attr = a.get("rso") == "1"
            # Tuple-misreport defenses (bypass c): rso attribute must agree with the
            # tier-basis marker, and tuple-class must equal the recomputation.
            if rso_attr != rso_marker:
                errors.append(f"{cell}/{role}: TUPLE MISREPORT — data-rso={a.get('rso')!r} "
                              f"contradicts tier-basis marker "
                              f"({'present' if rso_marker else 'absent'})")
            def _int(k):
                try:
                    return int(a.get(k) or 0)
                except ValueError:
                    return 0
            recomputed = tuple_class(a.get("state"), a.get("tier-basis"),
                                     a.get("conv") or None, 1 if rso_marker else 0,
                                     _int("reg-refs"), _int("reg-jur"))
            if tc != recomputed:
                errors.append(f"{cell}/{role}: TUPLE MISREPORT — data-tuple-class={tc!r} "
                              f"but recomputation from (state, conv, rso-marker) gives "
                              f"{recomputed!r}")
            rso = rso_marker or rso_attr  # either signal suffices to bind I3
            # I3 AS AMENDED (DR-2026-07-21 Option A). The absolute form — no
            # best-practice language on an RSO cell, ever — was REPEALED. A
            # code-consensus claim may anchor best practice at the flagged weak
            # band. What is forbidden now is narrower and sharper:
            #   (1) any above-band marker on an RSO rendering, and
            #   (2) best-practice language that is not flagged weak in the same
            #       element.
            if rso:
                m = ABOVE_BAND_RE.search(r["claim"] + " " + r["body"])
                if m:
                    errors.append(f"{cell}/{role}: I3 VIOLATION — above-weak-band marker "
                                  f"({m.group(0)!r}) on a regulatory-stratum-only cell; "
                                  f"Option A permits the weak band (○) only")
                # Per-element: a body paragraph may use best-practice language
                # only if that same paragraph carries the weak flag. Checking
                # per-element rather than per-rendering is what stops a flag in
                # paragraph 1 from licensing an unflagged claim in paragraph 3.
                for el in [r["claim"]] + PARA_RE.findall(r["body"]):
                    bp = BP_LEXICON.search(el)
                    if bp and not WEAK_FLAG_LEXICON.search(el):
                        errors.append(f"{cell}/{role}: I3 VIOLATION — unflagged best-practice "
                                      f"language ({bp.group(0)!r}) on a regulatory-stratum-only "
                                      f"cell; Option A requires the weak-band flag in the same "
                                      f"element, never suppressed and never unflagged")
            # I5 (body) — inflation lexicon banned in every rendering, every cell
            m = INFLATION_LEXICON.search(r["body"]) or INFLATION_LEXICON.search(r["claim"])
            if m:
                errors.append(f"{cell}/{role}: I5 VIOLATION — claim-strength inflation "
                              f"({m.group(0)!r}) in rendering body")
            # I4/I5 (claim element) — claim text equals the map row exactly
            if recomputed not in REGISTER_MAP:
                errors.append(f"{cell}/{role}: unknown tuple-class {recomputed!r}")
                continue
            expected = REGISTER_MAP[recomputed][role].format(
                basis=a.get("tier-basis", ""), n_refs=_int("reg-refs"), n_jur=_int("reg-jur"))
            if r["claim"] != expected:
                errors.append(f"{cell}/{role}: I4/I5 VIOLATION — claim-strength text is not "
                              f"the REGISTER_MAP row.\n  expected: {expected!r}\n  "
                              f"rendered: {r['claim']!r}")
            # I2 — policymaker must pair floor with anchor whenever a floor is shown
            if role == "policymaker":
                has_floor = "FLOOR" in r["body"]
                has_anchor = "ANCHOR" in r["body"]
                if has_floor and not has_anchor:
                    errors.append(f"{cell}/policymaker: I2 VIOLATION — floor rendered "
                                  f"without paired anchor statement")
    return errors


def selftest(doc, db_path=None):
    """Tamper each invariant; the checker must fire on every tampered variant."""
    base_errors = check(doc, db_path)
    if base_errors:
        print("selftest aborted — base document not clean:")
        print("\n".join(f"  {e}" for e in base_errors[:5]))
        return False
    tampers = []
    # I1: flip one rendering's data-state
    tampers.append(("I1 tuple divergence",
                    doc.replace("data-role='ot' data-register='clinical' data-state='stated'",
                                "data-role='ot' data-register='clinical' data-state='provisional'", 1)))
    # I3: inject best-practice language into an rso rendering
    m = re.search(r"(data-rso='1'[^>]*>.*?<p class='claim-strength'>)", doc, re.S)
    if m:
        tampers.append(("I3 best-practice on regulatory-stratum-only",
                        doc.replace(m.group(1), m.group(1) + "Best practice: ", 1)))
    # I4/I5: inflate a claim beyond its map row
    m = re.search(r"<p class='claim-strength'>([^<]*)</p>", doc)
    tampers.append(("I4/I5 claim inflation",
                    doc.replace(m.group(0),
                                "<p class='claim-strength'>This is definitively proven "
                                "best practice beyond dispute.</p>", 1)))
    # I2: strip the ANCHOR line from one policymaker body
    m = re.search(r"(data-role='policymaker'.*?)<p class='emphasis'>ANCHOR[^<]*</p>", doc, re.S)
    if m:
        tampers.append(("I2 floor without anchor",
                        doc.replace(m.group(0), m.group(1), 1)))
    # Bypass (a): synonym smuggling into an RSO rendering body
    m = re.search(r"(data-rso='1'[^>]*>.*?<p class='emphasis'>)", doc, re.S)
    if m:
        tampers.append(("I3 bypass: 'recommended standard' synonym in RSO body",
                        doc.replace(m.group(1),
                                    m.group(1) + "This is the recommended standard. ", 1)))
    # Bypass (b): inflation smuggled into a non-RSO emphasis body
    m = re.search(r"(data-rso='0'[^>]*>.*?<p class='emphasis'>)", doc, re.S)
    if m:
        tampers.append(("I5 bypass: inflation in non-RSO body",
                        doc.replace(m.group(1),
                                    m.group(1) + "Definitively proven beyond dispute. ", 1)))
    # Bypass (c): tuple misreport — relabel an RSO rendering as non-RSO with a
    # matching fake tuple-class (the tier-basis marker stays and must betray it)
    bad_c = doc.replace("data-rso='1'", "data-rso='0'").replace(
        "data-tuple-class='rso_weak_single'", "data-tuple-class='provisional_t3'").replace(
        "data-tuple-class='rso_weak_broad'", "data-tuple-class='provisional_t3'")
    if bad_c != doc:
        tampers.append(("tuple misreport: RSO relabelled non-RSO", bad_c))

    # ── Option A rework: one tamper per new rule ───────────────────────────
    # Above-band marker on an RSO rendering (amended I3, clause 1).
    m = re.search(r"(data-rso='1'[^>]*>.*?<p class='claim-strength'>)", doc, re.S)
    if m:
        tampers.append(("I3 amended: above-weak-band marker on RSO",
                        doc.replace(m.group(1), m.group(1) + "[●] ", 1)))
    # Repr leak (independent of --db).
    m = re.search(r"data-sha='[0-9a-f]{8}", doc)
    if m:
        tampers.append(("REPR LEAK: data-sha='None'",
                        doc.replace(m.group(0), "data-sha='None", 1)))
    # Breadth misreport: a single-instrument cell claiming broad-band breadth.
    bad_breadth = doc.replace("data-reg-jur='1'", "data-reg-jur='12'", 1)
    if bad_breadth != doc:
        tampers.append(("breadth misreport: reg-jur inflated", bad_breadth))

    ok = True
    for label, bad in tampers:
        fired = len(check(bad, db_path)) > 0
        ok &= fired
        print(f"{'FIRED' if fired else '**SILENT — MUTATION MISSED**'}: {label}")

    # Map lint: tamper the MAP rather than the document — the failure mode that
    # actually happened, where the document faithfully matched a map that had
    # stopped telling the truth.
    import copy
    bad_map = copy.deepcopy(REGISTER_MAP)
    bad_map["rso_weak_single"]["designer"] = \
        bad_map["rso_weak_single"]["designer"].replace("○ weak, code-derived", "")
    fired = len(lint_register_map(bad_map)) > 0
    ok &= fired
    print(f"{'FIRED' if fired else '**SILENT — MUTATION MISSED**'}: "
          f"REGISTER_MAP lint: weak-band flag stripped from a map row")

    # Completeness (DB → doc). Needs a DB; announce the skip rather than
    # passing quietly, or an absent DB would make this look covered.
    if db_path:
        bad_complete = re.sub(r"<section class='cell'.*?</section>", "", doc, count=1, flags=re.S)
        fired = len(check(bad_complete, db_path)) > 0
        ok &= fired
        print(f"{'FIRED' if fired else '**SILENT — MUTATION MISSED**'}: "
              f"COMPLETENESS: a whole cell section deleted")
    else:
        print("SKIP (no --db): COMPLETENESS tamper requires a DB to compare against")

    print(f"clean pass on untampered document: {'yes' if not base_errors else 'NO'}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    # Defaults, so the check registry can invoke this with no arguments. Its
    # quarantine reason was partly "requires an html positional, so it cannot
    # run corpus-wide as-is"; that is now false.
    ap.add_argument("html", nargs="?", default=DEFAULT_DOC,
                    help=f"rendered pilot HTML (default: {DEFAULT_DOC})")
    ap.add_argument("--db", default=os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"),
                    help="cross-check rendered tuples against specifications in this DB "
                         "(defeats self-reported-attribute bypasses). Pass --db '' to disable, "
                         "for fixture use. Honours GUIDEBOOK_DB_PATH.")
    ap.add_argument("--selftest", action="store_true",
                    help="mutation-test the checker itself, then check the real document")
    args = ap.parse_args()
    doc = open(args.html).read()
    if args.selftest:
        if not selftest(doc, args.db or None):
            sys.exit("SELFTEST FAILED — a tampered invariant went undetected")
    errors = check(doc, db_path=args.db or None)
    if errors:
        print(f"\n{len(errors)} INTEGRITY VIOLATIONS:")
        print("\n".join(f"  {e}" for e in errors))
        sys.exit(1)
    n_cells = len(parse(doc))
    print(f"PASS: I1–I5 hold across {n_cells} cells × {len(ROLES)} registers"
          + (" (DB cross-check on)" if args.db else ""))


if __name__ == "__main__":
    main()
