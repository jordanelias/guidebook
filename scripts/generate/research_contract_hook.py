#!/usr/bin/env python3
"""
scripts/generate/research_contract_hook.py — derive the SessionStart hook payload
from governance/research-contract.yaml.

The R1-R15 contract used to exist as two hand-transcribed copies with no
comparator: the hook text in .claude/settings.json and the rule table in
scripts/audit/research_batch_dod.py. They drifted on R1, R2 and R3 — two of those
changed what the contract obliges. This makes the hook a DERIVED artifact, in the
same shape as the repo's other freshness gates (tools/pipeline_completeness.py
--check, tools/evidentiary_audit.py --check): regenerate, compare, fail on drift.

Usage:
    python3 scripts/generate/research_contract_hook.py --check   # gate (registered)
    python3 scripts/generate/research_contract_hook.py --write   # regenerate
    python3 scripts/generate/research_contract_hook.py           # print payload

Exit codes: 0 = in sync (or written), 1 = drift, 2 = cannot run.
"""

import argparse
import json
import os
import sys
import textwrap

import yaml

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTRACT = os.path.join(REPO, "governance", "research-contract.yaml")
SETTINGS = os.path.join(REPO, ".claude", "settings.json")

BANNER = "================ GUIDEBOOK RESEARCH CONTRACT (harness-injected) ================"
RULE = "=" * 79
PREAMBLE = [
    "RESEARCH IS INVALID IF NOT COMPLIANT WITH OUR GOVERNANCE, VERIFICATION TOOLS,",
    "RULES AND ETHOS. Compliance is mechanical, not remembered.",
]


def _wrap(rule_id, text, width=78):
    """`  R1  first line` then continuation lines aligned under the text column."""
    indent = " " * 6
    head = f"  {rule_id:<3} "
    # break_on_hyphens=False: without it "by-product" wraps to "by-" / "product"
    # and "population-served" splits mid-term. This text is injected into every
    # session; a rule that reads as broken reads as unimportant.
    body = textwrap.wrap(" ".join(text.split()), width=width - len(head),
                         break_on_hyphens=False, break_long_words=False)
    if not body:
        return []
    return [head + body[0]] + [indent + line for line in body[1:]]


def payload_lines():
    with open(CONTRACT, encoding="utf-8") as fh:
        contract = yaml.safe_load(fh)

    by_phase = {p["id"]: [] for p in contract["phases"]}
    for rule in contract["rules"]:
        by_phase.setdefault(rule["phase"], []).append((rule["id"], rule["hook"]))
        # A rule may bear on a second phase (R7 does): stated once per phase it
        # governs, so the injected text matches the phase the reader is in.
        if rule.get("also_phase"):
            by_phase.setdefault(rule["also_phase"], []).append(
                (rule["id"], rule["also_hook"]))

    lines = [BANNER] + PREAMBLE
    for phase in contract["phases"]:
        lines.append("")
        lines.append(phase["heading"])
        for rule_id, text in by_phase.get(phase["id"], []):
            lines.extend(_wrap(rule_id, text))
    lines.append("")
    lines.extend(contract.get("footer", []))
    lines.append(RULE)
    return lines


def hook_command(lines):
    """The printf invocation settings.json carries."""
    quoted = " ".join("'" + line.replace("'", "'\\''") + "'" for line in lines)
    return "printf '%s\\n' " + quoted


def current_command():
    with open(SETTINGS, encoding="utf-8") as fh:
        settings = json.load(fh)
    try:
        return settings["hooks"]["SessionStart"][0]["hooks"][0]["command"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"SessionStart hook not found in settings.json: {exc}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="fail if settings.json has drifted from the contract")
    ap.add_argument("--write", action="store_true",
                    help="regenerate the hook in settings.json")
    args = ap.parse_args()

    try:
        lines = payload_lines()
        wanted = hook_command(lines)
    except Exception as exc:  # noqa: BLE001
        print(f"research_contract_hook: cannot build payload: {exc}", file=sys.stderr)
        return 2

    if not (args.check or args.write):
        print("\n".join(lines))
        return 0

    try:
        have = current_command()
    except Exception as exc:  # noqa: BLE001
        print(f"research_contract_hook: {exc}", file=sys.stderr)
        return 2

    print(f"EXAMINED: {len(lines)} contract line(s)")

    # Second copy, second comparator. The hook is generated; the enforcer is not
    # (its rules are implemented, not transcribed), so what can be checked is that
    # the two vocabularies agree: a rule the contract defines must be one the
    # enforcer knows, and vice versa. This is what would have caught R1/R2/R3
    # drifting, since each divergence began as a rule stated in one place only.
    rule_ids = {r["id"] for r in yaml.safe_load(open(CONTRACT, encoding="utf-8"))["rules"]}
    try:
        enforcer_src = open(os.path.join(REPO, "scripts", "audit",
                                         "research_batch_dod.py"), encoding="utf-8").read()
    except OSError as exc:
        print(f"research_contract_hook: cannot read the enforcer: {exc}", file=sys.stderr)
        return 2
    import re as _re
    enforcer_ids = set(_re.findall(r"\bR(?:1[0-5]|[1-9])\b", enforcer_src))
    only_contract = sorted(rule_ids - enforcer_ids, key=lambda r: int(r[1:]))
    only_enforcer = sorted(enforcer_ids - rule_ids, key=lambda r: int(r[1:]))
    if only_contract or only_enforcer:
        print("FAIL: the contract and its enforcer disagree about which rules exist.")
        if only_contract:
            print(f"      defined in the contract, unknown to the enforcer: {only_contract}")
        if only_enforcer:
            print(f"      enforced but not defined in the contract: {only_enforcer}")
        return 1
    print(f"PASS: contract and enforcer agree on {len(rule_ids)} rule ids")

    if have == wanted:
        print("PASS: the SessionStart hook matches governance/research-contract.yaml")
        return 0

    if args.write:
        with open(SETTINGS, encoding="utf-8") as fh:
            settings = json.load(fh)
        settings["hooks"]["SessionStart"][0]["hooks"][0]["command"] = wanted
        with open(SETTINGS, "w", encoding="utf-8") as fh:
            json.dump(settings, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        print("WROTE: .claude/settings.json regenerated from the contract")
        return 0

    print("FAIL: the SessionStart hook has drifted from governance/research-contract.yaml.")
    print("      The contract is canonical. Regenerate with:")
    print("        python3 scripts/generate/research_contract_hook.py --write")
    print()
    print("  --- contract says the hook should inject ---")
    for line in lines:
        print(f"  | {line}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
