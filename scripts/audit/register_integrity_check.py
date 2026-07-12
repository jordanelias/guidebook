#!/usr/bin/env python3
"""
scripts/audit/register_integrity_check.py — mechanical check of the five register
integrity invariants (governance/evidence-architecture.md §6) over rendered output.

I1  Tuple identity: every rendering of a cell, in every register, carries the
    identical determination tuple (state, tier_basis, conv, rso, cfo, sha, rule_version).
I2  Floor–anchor pairing: the policymaker rendering must always pair FLOOR with
    ANCHOR (never the floor alone) whenever a regulatory floor exists.
I3  No best-practice language on regulatory-stratum-only cells, in any register.
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

RENDER_RE = re.compile(r"<div class='rendering' ([^>]*)>(.*?)</div>", re.S)
ATTR_RE = re.compile(r"data-([a-z-]+)='([^']*)'")
CLAIM_RE = re.compile(r"<p class='claim-strength'>(.*?)</p>", re.S)
TUPLE_KEYS = ("state", "tier-basis", "conv", "rso", "cfo", "sha", "rule-version")

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


def parse(doc):
    out = {}
    for attrs_raw, body in RENDER_RE.findall(doc):
        attrs = dict(ATTR_RE.findall(attrs_raw))
        m = CLAIM_RE.search(body)
        claim = html.unescape(m.group(1)).strip() if m else ""
        out.setdefault(attrs.get("cell", "?"), []).append(
            {"attrs": attrs, "claim": claim, "body": html.unescape(body)})
    return out


def check(doc, db_path=None):
    errors = []
    cells = parse(doc)
    if not cells:
        return ["no renderings found in document"]
    db_rows = {}
    if db_path:
        import sqlite3
        conn = sqlite3.connect(db_path)
        for ic, pc, st, tb, cfo, sha, rv in conn.execute(
                "SELECT item_code, population_code, state, tier_basis, code_floor_only, "
                "derivation_sha, rule_version FROM evidence_cell_state"):
            db_rows[f"{ic}×{pc}"] = dict(state=st, tier_basis=tb or "no basis",
                                         cfo=str(cfo), sha=sha, rule_version=rv)
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
                errors.append(f"{cell}: rendered but no evidence_cell_state row exists")
            else:
                for r in renders[:1]:
                    a = r["attrs"]
                    for html_key, db_key in (("state", "state"), ("tier-basis", "tier_basis"),
                                             ("cfo", "cfo"), ("sha", "sha"),
                                             ("rule-version", "rule_version")):
                        if a.get(html_key, "") != str(row[db_key]):
                            errors.append(f"{cell}: DB CROSS-CHECK VIOLATION — data-{html_key}="
                                          f"{a.get(html_key)!r} but DB says {row[db_key]!r}")
        for r in renders:
            a, role = r["attrs"], r["attrs"].get("role")
            tc = a.get("tuple-class")
            rso_marker = (a.get("tier-basis", "")).endswith("(regulatory_stratum_only)")
            rso_attr = a.get("rso") == "1"
            # Tuple-misreport defenses (bypass c): rso attribute must agree with the
            # tier-basis marker, and tuple-class must equal the recomputation.
            if rso_attr != rso_marker:
                errors.append(f"{cell}/{role}: TUPLE MISREPORT — data-rso={a.get('rso')!r} "
                              f"contradicts tier-basis marker "
                              f"({'present' if rso_marker else 'absent'})")
            recomputed = tuple_class(a.get("state"), a.get("tier-basis"),
                                     a.get("conv") or None, 1 if rso_marker else 0)
            if tc != recomputed:
                errors.append(f"{cell}/{role}: TUPLE MISREPORT — data-tuple-class={tc!r} "
                              f"but recomputation from (state, conv, rso-marker) gives "
                              f"{recomputed!r}")
            rso = rso_marker or rso_attr  # either signal suffices to bind I3
            # I3 — no best-practice language (incl. synonyms) on RSO cells, anywhere
            m = BP_LEXICON.search(r["claim"] + " " + r["body"])
            if rso and m:
                errors.append(f"{cell}/{role}: I3 VIOLATION — best-practice language "
                              f"({m.group(0)!r}) on a regulatory-stratum-only cell")
            # I5 (body) — inflation lexicon banned in every rendering, every cell
            m = INFLATION_LEXICON.search(r["body"]) or INFLATION_LEXICON.search(r["claim"])
            if m:
                errors.append(f"{cell}/{role}: I5 VIOLATION — claim-strength inflation "
                              f"({m.group(0)!r}) in rendering body")
            # I4/I5 (claim element) — claim text equals the map row exactly
            if recomputed not in REGISTER_MAP:
                errors.append(f"{cell}/{role}: unknown tuple-class {recomputed!r}")
                continue
            expected = REGISTER_MAP[recomputed][role].format(basis=a.get("tier-basis", ""))
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


def selftest(doc):
    """Tamper each invariant; the checker must fire on every tampered variant."""
    base_errors = check(doc)
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
        "data-tuple-class='regulatory_stratum_only'", "data-tuple-class='provisional_t3'")
    if bad_c != doc:
        tampers.append(("tuple misreport: RSO relabelled non-RSO", bad_c))
    ok = True
    for label, bad in tampers:
        fired = len(check(bad)) > 0
        ok &= fired
        print(f"{'FIRED' if fired else '**SILENT — MUTATION MISSED**'}: {label}")
    print(f"clean pass on untampered document: {'yes' if not base_errors else 'NO'}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html", help="rendered pilot HTML")
    ap.add_argument("--db", default=None,
                    help="cross-check rendered tuples against evidence_cell_state in this DB "
                         "(defeats self-reported-attribute bypasses)")
    ap.add_argument("--selftest", action="store_true",
                    help="mutation-test the checker itself, then check the real document")
    args = ap.parse_args()
    doc = open(args.html).read()
    if args.selftest:
        if not selftest(doc):
            sys.exit("SELFTEST FAILED — a tampered invariant went undetected")
    errors = check(doc, db_path=args.db)
    if errors:
        print(f"\n{len(errors)} INTEGRITY VIOLATIONS:")
        print("\n".join(f"  {e}" for e in errors))
        sys.exit(1)
    n_cells = len(parse(doc))
    print(f"PASS: I1–I5 hold across {n_cells} cells × {len(ROLES)} registers"
          + (" (DB cross-check on)" if args.db else ""))


if __name__ == "__main__":
    main()
