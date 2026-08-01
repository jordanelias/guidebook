#!/usr/bin/env python3
"""
scripts/ci_helpers/check_commit_msg.py — the commit-message format gate.

Expected: {skill-name}: {action} [{YYYY-MM-DD HH:MM}]  (timestamp last).

EXEMPTIONS, and why they were added 2026-08-01
----------------------------------------------
This script previously checked HEAD's subject against the pattern with no
exemptions at all. Every human integration on `main` arrives as a GitHub merge
commit ("Merge pull request #NN from ..."), which cannot match the pattern, so
**every push run of ci.yml on main failed** on this step — verified across the
last six push runs, while all PR runs were green.

Two consequences made that worse than cosmetic:

  * The `Doctrine-SHA token` step runs after this one in the same job. A failing
    step skips the rest, so the blocking doctrine gate was never reached on the
    pushes it exists to police.
  * A permanently-red `main` is how the F1 class of bug survives: once red is
    normal, a newly-red check carries no information.

The exemptions mirror check_doctrine_token.py's E3/E4 exactly, so the two gates
in this job agree about what a checkable commit is:

  E3  bot / automation author  -> exempt
  E4  merge commit (>1 parent) -> exempt

Bot commits are exempt rather than fixed because the scheduled workflows compose
their own subjects ("url-verification: V1 run ... verified +0 (757 total); ...")
and those genuinely do not fit the {action} [timestamp] shape. Making the format
gate honest about them is the narrow fix; rewriting the workflows' message
templates is a separate change with no CI consequence.

Usage:
    python3 scripts/ci_helpers/check_commit_msg.py            # HEAD
    python3 scripts/ci_helpers/check_commit_msg.py --rev <sha>
    python3 scripts/ci_helpers/check_commit_msg.py --selftest

Exit codes: 0 = pass or exempt, 1 = fail, 2 = cannot run.
"""

import argparse
import re
import subprocess
import sys

PATTERN = re.compile(r"^[a-z][a-z0-9_-]+:\s+.+\s+\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\]$")
BOT_RE = re.compile(r"dependabot|github-actions|-bot@")


def git(*args):
    proc = subprocess.run(["git", *args], capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def evaluate(message, author, parent_count):
    """Pure decision function — no git, so the selftest can drive it directly.
    Returns (exit_code, explanation)."""
    if BOT_RE.search(author or ""):
        return 0, f"E3: bot commit ({author}) — format exempt."
    if parent_count > 1:
        return 0, "E4: merge commit — format exempt."
    if PATTERN.match(message or ""):
        return 0, "PASS: commit message format valid."
    return 1, ("FAIL: commit message does not match required format\n"
               f"  Got:      {message!r}\n"
               "  Expected: {skill-name}: {action} [YYYY-MM-DD HH:MM]\n"
               "  Example:  workplan-orchestrator: update gap register [2026-04-18 14:30]")


CASES = [
    # (name, message, author, parents, expected_exit)
    ("valid message passes",
     "governance: add a check [2026-08-01 09:12]", "Jordan <j@x>", 1, 0),
    ("timestamp must be last",
     "governance: add a check [2026-08-01 09:12] [DOCTRINE: abc1234]", "Jordan <j@x>", 1, 1),
    ("doctrine token before the timestamp is fine",
     "bpc: rewrite [DOCTRINE: abc1234] [2026-08-01 09:12]", "Jordan <j@x>", 1, 0),
    ("missing timestamp fails",
     "governance: add a check", "Jordan <j@x>", 1, 1),
    ("uppercase prefix fails",
     "Governance: add a check [2026-08-01 09:12]", "Jordan <j@x>", 1, 1),
    ("merge commit is exempt (E4) — the regression this file existed to miss",
     "Merge pull request #75 from jordanelias/claude/x", "Jordan <j@x>", 2, 0),
    ("a merge-shaped subject with ONE parent is not exempt",
     "Merge pull request #75 from jordanelias/claude/x", "Jordan <j@x>", 1, 1),
    ("bot commit is exempt (E3)",
     "url-verification: V1 run 2026-08-01 08:05 — verified +0 (757 total)",
     "github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>", 1, 0),
    ("a human cannot borrow the bot exemption",
     "url-verification: V1 run 2026-08-01 08:05 — verified +0", "Jordan <j@x>", 1, 1),
]


def selftest():
    ok = True
    for name, msg, author, parents, expected in CASES:
        got, _ = evaluate(msg, author, parents)
        passed = got == expected
        ok &= passed
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}"
              + ("" if passed else f"  (expected {expected}, got {got})"))
    print("=" * 70)
    print("SELFTEST:", "PASS — format gate and both exemptions behave as documented."
          if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="HEAD", help="commit to check (default HEAD)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    rc, message, err = git("log", "-1", "--format=%s", args.rev)
    if rc != 0:
        print(f"check_commit_msg: cannot read {args.rev}: {err}", file=sys.stderr)
        return 2
    _, author, _ = git("log", "-1", "--format=%an <%ae>", args.rev)
    _, parents, _ = git("log", "-1", "--format=%P", args.rev)
    parent_count = len(parents.split()) if parents else 0

    print(f"Checking commit message: {message!r}")
    code, explanation = evaluate(message, author, parent_count)
    print(explanation)
    return code


if __name__ == "__main__":
    sys.exit(main())
