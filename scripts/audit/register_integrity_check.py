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

from pilot_renderings import REGISTER_MAP, ROLES  # noqa: E402  (single source of truth)

RENDER_RE = re.compile(r"<div class='rendering' ([^>]*)>(.*?)</div>", re.S)
ATTR_RE = re.compile(r"data-([a-z-]+)='([^']*)'")
CLAIM_RE = re.compile(r"<p class='claim-strength'>(.*?)</p>", re.S)
BP_RE = re.compile(r"best[\s-]practice", re.I)
TUPLE_KEYS = ("state", "tier-basis", "conv", "rso", "cfo", "sha", "rule-version")


def parse(doc):
    out = {}
    for attrs_raw, body in RENDER_RE.findall(doc):
        attrs = dict(ATTR_RE.findall(attrs_raw))
        m = CLAIM_RE.search(body)
        claim = html.unescape(m.group(1)).strip() if m else ""
        out.setdefault(attrs.get("cell", "?"), []).append(
            {"attrs": attrs, "claim": claim, "body": html.unescape(body)})
    return out


def check(doc):
    errors = []
    cells = parse(doc)
    if not cells:
        return ["no renderings found in document"]
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
        for r in renders:
            a, role = r["attrs"], r["attrs"].get("role")
            tc = a.get("tuple-class")
            rso = a.get("rso") == "1"
            # I3 — no best-practice language on regulatory-stratum-only cells
            if rso and BP_RE.search(r["claim"] + r["body"]):
                errors.append(f"{cell}/{role}: I3 VIOLATION — best-practice language on a "
                              f"regulatory-stratum-only cell")
            # I4/I5 — claim text equals the map row for this tuple-class × register
            if tc not in REGISTER_MAP:
                errors.append(f"{cell}/{role}: unknown tuple-class {tc!r}")
                continue
            expected = REGISTER_MAP[tc][role].format(basis=a.get("tier-basis", ""))
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
    ap.add_argument("--selftest", action="store_true",
                    help="mutation-test the checker itself, then check the real document")
    args = ap.parse_args()
    doc = open(args.html).read()
    if args.selftest:
        if not selftest(doc):
            sys.exit("SELFTEST FAILED — a tampered invariant went undetected")
    errors = check(doc)
    if errors:
        print(f"\n{len(errors)} INTEGRITY VIOLATIONS:")
        print("\n".join(f"  {e}" for e in errors))
        sys.exit(1)
    n_cells = len(parse(doc))
    print(f"PASS: I1–I5 hold across {n_cells} cells × {len(ROLES)} registers")


if __name__ == "__main__":
    main()
