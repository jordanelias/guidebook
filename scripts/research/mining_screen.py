#!/usr/bin/env python3
"""Derive a citation-mining yield from a persisted payload and a NAMED screen.

CLAUDE.md rule 7a: a number is written as the command that computes it. A mining yield
is a number, and until 2026-09-18 it was produced by a regex typed into a shell and
recorded nowhere -- so two batches compared counts from two different instruments, a
pre-registered floor was scored against a screen it was not calibrated on, and a
retraction was published without re-deriving the anchor that founded the claim.

This is that command. It reads the screen from `governance/mining-screens.yaml` (the
single home of the terms) and the references from the session retrieval log (the bytes
actually received), so a yield is reproducible by anyone, months later, without the
shell history it was first computed in.

    python3 scripts/research/mining_screen.py --ref REF-00979 --screen slope-strict
    python3 scripts/research/mining_screen.py --all --screen slope-strict
    python3 scripts/research/mining_screen.py --all --compare      # every screen, side by side

EXAMINED is always printed: a yield over zero deposited references is not a low yield,
it is an absent reference list, and the two render identically as "0" (CLAUDE.md 5a).
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCREEN_FILE = ROOT / "governance" / "mining-screens.yaml"
LOG_ROOT = ROOT / "retrieval-log"


def load_screens():
    with open(SCREEN_FILE, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    return doc["screens"]


def compile_screen(spec):
    # \b on both ends would refuse a trailing wildcard stem like `accessib`; only the
    # LEADING boundary is asserted, which is what makes `propuls` match `propulsion`
    # and still refuses `repulsion`. This is the same shape the ad-hoc regexes used, so
    # a re-derivation reproduces the historical numbers rather than quietly improving
    # on them.
    return re.compile(r"\b(" + "|".join(spec["terms"]) + r")", re.I)


def _title(ref):
    return (ref.get("article-title") or ref.get("volume-title")
            or ref.get("unstructured") or "")


def payloads_by_ref():
    """Map ref_id -> [(session, artefact_path)] from every session manifest.

    The manifest is the binding between a reference id and the bytes retrieved for it;
    reading it here rather than guessing filenames is what keeps this honest when a
    payload is re-fetched in a later session.
    """
    out = {}
    for manifest in sorted(LOG_ROOT.glob("*/manifest.jsonl")):
        for line in manifest.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            rid = (rec.get("ref_id") or "").strip()
            art = rec.get("artefact") or rec.get("sha256")
            if not rid or not art:
                continue
            path = manifest.parent / art
            if path.suffix != ".json" or not path.exists():
                continue
            out.setdefault(rid, []).append((manifest.parent.name, path))
    return out


def references_for(path):
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    # NOT EVERY PERSISTED JSON IS CROSSREF-SHAPED. A Crossref `works` response nests the
    # record under `message`; an OpenAlex reply, a search result and an error body do
    # not, and `message` in some of them is a plain string. Treat anything that is not a
    # mapping with a reference list as "no reference list", which is a different fact
    # from a zero yield and is reported as such.
    msg = doc.get("message") if isinstance(doc, dict) else None
    if not isinstance(msg, dict):
        msg = doc if isinstance(doc, dict) else {}
    refs = msg.get("reference")
    return refs if isinstance(refs, list) else None


def score(refs, rx):
    return sum(1 for r in refs if rx.search(_title(r)))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref", help="REF-NNNNN to score")
    ap.add_argument("--all", action="store_true",
                    help="every ref that has a JSON payload with a reference list")
    ap.add_argument("--screen", help="a screen name from governance/mining-screens.yaml")
    ap.add_argument("--compare", action="store_true",
                    help="score under EVERY screen, so a claim about one screen "
                         "inverting another's ranking can be checked rather than asserted")
    args = ap.parse_args()

    screens = load_screens()
    if args.screen and args.screen not in screens:
        print(f"no screen named {args.screen!r}. Declared: {sorted(screens)}",
              file=sys.stderr)
        return 2
    chosen = sorted(screens) if args.compare else [args.screen or "slope-strict"]

    index = payloads_by_ref()
    refs = [args.ref] if args.ref else sorted(index)
    if args.ref and args.ref not in index:
        print(f"{args.ref}: no JSON payload in any session manifest under {LOG_ROOT}/. "
              f"A yield cannot be derived from a payload that was never persisted.",
              file=sys.stderr)
        return 2

    rows, skipped = [], []
    for rid in refs:
        best = None
        for _sess, path in index.get(rid, []):
            r = references_for(path)
            if r and (best is None or len(r) > len(best[1])):
                best = (path, r)
        if best is None:
            skipped.append(rid)
            continue
        rows.append((rid, len(best[1]),
                     {n: score(best[1], compile_screen(screens[n])) for n in chosen}))

    if not rows:
        print("EXAMINED: 0 — no payload carried a reference list. Not a zero yield.")
        return 1

    width = max(len(n) for n in chosen)
    head = f"{'ref':<12}{'deposited':>10}" + "".join(f"{n:>{width + 2}}" for n in chosen)
    print(head)
    print("-" * len(head))
    for rid, n, sc in sorted(rows, key=lambda r: -r[2][chosen[0]]):
        print(f"{rid:<12}{n:>10}" + "".join(f"{sc[n2]:>{width + 2}}" for n2 in chosen))
    print(f"\nEXAMINED: {len(rows)} anchor(s), "
          f"{sum(n for _, n, _ in rows)} deposited reference(s)")
    print(f"SCREENS: " + ", ".join(
        f"{n} v{screens[n].get('version', '?')}" for n in chosen))
    if skipped:
        print(f"NO REFERENCE LIST for {len(skipped)}: {', '.join(skipped)} — these are "
              f"outside the comparison, not zero-yield anchors.")
    print("Ranking is by the FIRST screen listed. Re-run rather than quoting a figure "
          "from a document (rule 7a).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
