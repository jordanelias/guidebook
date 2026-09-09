#!/usr/bin/env python3
"""Pin CLAUDE.md's SPINE line to governance/pipeline-contract.yaml.

WHAT WRONG THING REACHES THE GUIDEBOOK IF THIS DOES NOT EXIST (CLAUDE.md §1).
The stage list is the frame rule 5 is applied against: you cannot tell a
legitimate stage-specific fact from a copy without knowing which stage a table is
in. CLAUDE.md is auto-loaded into every session, so when its stage list drifts
from the contract, every table-to-stage judgement made that session is made
against the wrong map -- and the wrong answer is a duplicated fact in the
database, not a red check.

This is not hypothetical. The five-stage list of 2026-08-25 was superseded by a
six-stage list on 2026-08-27 and by the seven-stage spine (D-0167) the same day;
for thirteen days CLAUDE.md carried BOTH "Substrate is not a stage" and, forty
lines below, the paragraph recording that the machine enforces `base` as one.
One file, two answers, and no check could see it because the list was prose.

WHY THE CONTRACT IS THE PARENT. governance/pipeline-contract.yaml's `stages:` is
the declared single home of the stage ids (rule 5). CLAUDE.md renders it for a
reader; a rendering that disagrees with its source is the defect.
"""
import os
import re
import sys

import yaml

CLAUDE_MD = "CLAUDE.md"
CONTRACT = "governance/pipeline-contract.yaml"
SPINE_RE = re.compile(r"^\s*SPINE:\s*(.+?)\s*$", re.M)
SEP = " -> "


def main() -> int:
    for path in (CLAUDE_MD, CONTRACT):
        if not os.path.exists(path):
            print(f"FAIL: missing {path}")
            return 1

    text = open(CLAUDE_MD, encoding="utf-8").read()
    found = SPINE_RE.findall(text)
    if len(found) != 1:
        print(f"FAIL: expected exactly one SPINE: line in {CLAUDE_MD}, found {len(found)}")
        print("      The line is the checked rendering of the contract; do not hand-edit or duplicate it.")
        return 1

    declared = [s.strip() for s in found[0].split(SEP)]
    contract = [str(s["id"]) for s in yaml.safe_load(open(CONTRACT, encoding="utf-8"))["stages"]]

    print(f"EXAMINED: {len(contract)} contract stage(s) against 1 SPINE line")
    if declared != contract:
        print("FAIL: CLAUDE.md's SPINE line disagrees with the contract, which is the single home.")
        print(f"  CLAUDE.md : {SEP.join(declared)}")
        print(f"  {CONTRACT}: {SEP.join(contract)}")
        print("  Correct CLAUDE.md, or change the contract first if the spine itself was re-ruled.")
        return 1

    print(f"PASS: SPINE matches {CONTRACT} — {SEP.join(contract)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
