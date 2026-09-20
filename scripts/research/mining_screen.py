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


def _title(ref, reading="unstructured"):
    """The string a screen matches against.

    `reading` selects WHICH transcription of a damaged entry is scored. For a Crossref
    deposit there is only one and the argument does nothing. For a list extracted from a
    scanned page there are two, and the difference between them is the measurement's
    uncertainty rather than a detail: `unstructured` substitutes no letters, `inferred`
    is the best reading with brackets on what was supplied. Scoring only the second
    would let a generous transcription manufacture a yield, which is the failure this
    whole module exists to prevent, one layer in.
    """
    if reading == "inferred" and ref.get("inferred"):
        return ref["inferred"]
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


def supersedes_of(path):
    """The artefact filename this payload declares it replaces, or None."""
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return doc.get("supersedes_artefact") if isinstance(doc, dict) else None


def provenance_of(path):
    """DEPOSITED or EXTRACTED. Never guessed: it is read off the payload itself.

    A publisher-deposited reference list and a reference list transcribed off a damaged
    scan are not the same evidence and must not print under the same column heading.
    Until 2026-09-20 this module had one heading, `deposited`, and would have applied it
    to an OCR transcription -- restating an extraction as a deposit, which is CLAUDE.md
    rule 7a's third shape (a caller restating a checked fact) arriving in a tool's own
    output.
    """
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return "unknown"
    if isinstance(doc, dict) and doc.get("kind") == "pdf-bibliography":
        # READ vs SCRAPED, and the difference is the whole lesson of batch 19. A list
        # transcribed from RENDERED PAGES is as reliable as the reader; one scraped from a
        # damaged TEXT LAYER is not, and reporting both as "EXTRACTED" would hide exactly
        # the distinction that batch cost.
        return "SCRAPED" if doc.get("ocr_damaged") else "READ"
    return "DEPOSITED"


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


def score(refs, rx, reading="unstructured"):
    return sum(1 for r in refs if rx.search(_title(r, reading)))


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
        cands = []
        for _sess, path in index.get(rid, []):
            r = references_for(path)
            if r:
                cands.append((path, r))
        # A CORRECTED TRANSCRIPTION MUST BE ABLE TO TAKE EFFECT. Selection used to be
        # "the payload with the most references", which silently keeps the FIRST of two
        # equal-length lists -- so a re-transcription that fixes readings without changing
        # the count could never win, and the screen would go on scoring the version its
        # author had already withdrawn. Measured on REF-01005: the corrected 38-entry
        # transcription lost to the damaged 38-entry one.
        #
        # An artefact that names the one it replaces wins. The superseded file is NOT
        # deleted -- migrations are append-only in spirit here too, and the withdrawn
        # reading is part of the record of how the corrected one was reached.
        superseded = {supersedes_of(path) for path, _ in cands} - {None}
        live = [c for c in cands if c[0].name not in superseded] or cands
        best = max(live, key=lambda c: len(c[1]), default=None)
        if best is None:
            skipped.append(rid)
            continue
        path, reflist = best
        prov = provenance_of(path)
        # A band, not a point, wherever the transcription is uncertain. floor == ceiling
        # for a deposited list, and the band renders as a single number, so nothing about
        # the existing output changes for the anchors that had it before.
        cells = {}
        for n in chosen:
            rx = compile_screen(screens[n])
            floor = score(reflist, rx, "unstructured")
            ceil = score(reflist, rx, "inferred") if prov == "SCRAPED" else floor
            cells[n] = (floor, max(floor, ceil))
        rows.append((rid, len(reflist), cells, prov))

    if not rows:
        print("EXAMINED: 0 — no payload carried a reference list. Not a zero yield.")
        return 1

    def render(cell):
        lo, hi = cell
        return str(lo) if lo == hi else f"{lo}-{hi}"

    width = max(max(len(n) for n in chosen), 7)
    head = (f"{'ref':<12}{'refs':>6}  {'provenance':<11}"
            + "".join(f"{n:>{width + 2}}" for n in chosen))
    print(head)
    print("-" * len(head))
    for rid, n, sc, prov in sorted(rows, key=lambda r: -r[2][chosen[0]][0]):
        print(f"{rid:<12}{n:>6}  {prov:<11}"
              + "".join(f"{render(sc[n2]):>{width + 2}}" for n2 in chosen))
    print(f"\nEXAMINED: {len(rows)} anchor(s), "
          f"{sum(n for _, n, _, _ in rows)} reference(s)")
    if any(prov in ("SCRAPED", "READ") for *_, prov in rows):
        print("\nPROVENANCE. DEPOSITED: the publisher's own reference list. "
              "READ: transcribed from\nthe RENDERED PAGE of a scan. SCRAPED: taken off a damaged PDF TEXT LAYER, which\nis the unreliable one -- batch 19 read a mangled text layer as evidence the DOCUMENT\nwas illegible and was wrong about authors, years and a title's slope term. A range is\nfloor-ceiling and appears only for SCRAPED: the floor substitutes no letters, the\nceiling is a best guess at the damage. A zero on a SCRAPED list is weak evidence of\nabsence (CLAUDE.md 5a); on a READ list it is as good as the reader.")
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
