#!/usr/bin/env python3
"""CLAUDE.md's stated pipeline spine must match the machine's.

WHY THIS EXISTS (CLAUDE.md §1 puts the burden of proof on the addition):
`governance/pipeline-map.yaml` modelled the pipeline as FOUR stages and sat in
`governance/` for thirteen days after the owner ruled SEVEN, and no gate cared,
because nothing anywhere compared a document's account of the pipeline to the
machine's. The owner found it by reading, not by a check -- "governance pipeline
map isn't even correct with the number of pipeline stages" -- and then directed
the correct spine be "safeguarded and placed in Claude.md". On the class of work:
"hence Layer 0 for us". This is that Layer 0 instrument: it ensures Layer 1's
declared shape is what Layer 0's own front page teaches.

WHAT IT ASSERTS, and nothing more: the ordered stage ids on CLAUDE.md's canonical
`SPINE:` line are identical to `governance/pipeline-contract.yaml`'s `stages:`.
It does NOT check that either is *right* -- the contract is the single home and
the owner's ruling is what makes it right.

RULE 5, HONESTLY. "A parity check is not a fix -- it makes a dual home
survivable, therefore permanent." True, and this is a dual home. Kept under the
owner's 2026-09-09 directive to place the pipeline in CLAUDE.md: prose cannot
JOIN, and a front page silent on its own frame is worse than a checked rendering
of one. The failure message therefore never says "they disagree, pick one" -- it
always names the contract as the one to trust and CLAUDE.md as the copy to fix.

Usage:
    python3 scripts/audit/claude_md_spine.py
    python3 scripts/audit/claude_md_spine.py --selftest

Exit codes: 0 = agree, 1 = divergence, 2 = cannot run.
"""
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
CLAUDE_MD = ROOT / "CLAUDE.md"
CONTRACT = ROOT / "governance" / "pipeline-contract.yaml"

# The line is indented so Markdown renders it as a code block, and matched
# loosely on the arrow so an em-dash or a Unicode arrow does not silently make
# the line unfindable -- an unfindable line would make this check vacuous, which
# is CLAUDE.md §2(a), the exact failure it must not reproduce.
SPINE_RE = re.compile(r"^\s*SPINE:\s*(.+?)\s*$", re.MULTILINE)
ARROW_RE = re.compile(r"\s*(?:->|→|—>|>)\s*")


def spine_from_claude_md(text: str):
    """Ordered stage ids from CLAUDE.md's canonical SPINE line."""
    hits = SPINE_RE.findall(text)
    if not hits:
        raise LookupError(
            "no `SPINE:` line in CLAUDE.md. It is the subject of this check; "
            "without it the check would pass having examined nothing.")
    if len(hits) > 1:
        raise LookupError(
            f"{len(hits)} `SPINE:` lines in CLAUDE.md. One rendering, or the "
            f"reader cannot tell which is canonical: {hits}")
    return [p for p in ARROW_RE.split(hits[0].strip()) if p]


def spine_from_contract(doc):
    """Ordered stage ids from the declared single home."""
    stages = doc.get("stages")
    if not stages:
        raise LookupError("governance/pipeline-contract.yaml declares no `stages:`")
    return [s["id"] for s in stages]


def audit() -> int:
    try:
        stated = spine_from_claude_md(CLAUDE_MD.read_text())
        declared = spine_from_contract(yaml.safe_load(CONTRACT.read_text()))
    except (LookupError, OSError, yaml.YAMLError) as exc:
        print(f"CANNOT RUN: {exc}")
        return 2

    print("  contract  (single home): " + " -> ".join(declared))
    print("  CLAUDE.md (rendering)  : " + " -> ".join(stated))
    print(f"EXAMINED: {len(declared)} declared stage id(s)")

    if stated == declared:
        print("PASS: CLAUDE.md renders the contract's spine exactly, in order.")
        return 0

    missing = [s for s in declared if s not in stated]
    extra = [s for s in stated if s not in declared]
    print()
    print("FAIL: CLAUDE.md's SPINE line does not match the contract.")
    if missing:
        print(f"  in the contract, absent from CLAUDE.md: {missing}")
    if extra:
        print(f"  on CLAUDE.md's line, not a contract stage: {extra}")
    if not missing and not extra:
        print("  same ids, DIFFERENT ORDER — the spine is an order, not a set.")
    print()
    print("  governance/pipeline-contract.yaml is the single home of the stage")
    print("  ids. Fix CLAUDE.md's line to match it. If the CONTRACT is what is")
    print("  wrong, that is a stage ruling and it is the owner's — change it")
    print("  there first, then re-render here.")
    return 1


def _selftest() -> int:
    """Prove it can fail. A gate that cannot fail is not a gate (§2(a))."""
    real = spine_from_contract(yaml.safe_load(CONTRACT.read_text()))
    fails = []

    def check(name, cond, detail=""):
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f"  {detail}" if not cond else ""))
        if not cond:
            fails.append(name)

    check("the live pair agrees",
          spine_from_claude_md(CLAUDE_MD.read_text()) == real)
    check("a dropped stage is caught",
          spine_from_claude_md("SPINE: " + " -> ".join(real[1:])) != real)
    check("a REORDERED spine is caught — the ids are a sequence, not a set",
          spine_from_claude_md("SPINE: " + " -> ".join(reversed(real))) != real)
    check("an added stage is caught",
          spine_from_claude_md("SPINE: " + " -> ".join(real + ["curation"])) != real)
    check("the four-stage map that caused this check would be caught",
          spine_from_claude_md("SPINE: substrate -> acquisition -> synthesis -> render") != real)
    check("a Unicode arrow parses, so a paste cannot silently blank the subject",
          spine_from_claude_md("SPINE: a → b") == ["a", "b"])

    for bad, why in [("nothing here", "absent"), ("SPINE: a -> b\nSPINE: c -> d", "duplicated")]:
        try:
            spine_from_claude_md(bad)
            check(f"a {why} SPINE line raises rather than passing vacuously", False,
                  "returned instead of raising")
        except LookupError:
            check(f"a {why} SPINE line raises rather than passing vacuously", True)

    print(f"EXAMINED: {8} assertion(s)")
    print("SELFTEST: " + ("PASS" if not fails else "FAIL — " + ", ".join(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(_selftest() if "--selftest" in sys.argv else audit())
