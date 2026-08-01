#!/usr/bin/env python3
"""
scripts/ci_helpers/check_doctrine_token.py — the [DOCTRINE: <sha>] commit-token gate.

Any commit touching a SYNTHESIS PATH must carry `[DOCTRINE: <7-hex>]` before the
timestamp, matching the current SHA of governance/mission-and-epistemics.md:

    {skill}: {action} [DOCTRINE: <sha>] [YYYY-MM-DD HH:MM]

WHY THIS IS A SCRIPT
--------------------
It was a ~45-line inline bash block in ci.yml. Inline CI bash cannot be run
locally, cannot be unit-tested, and its exemption logic (doctrine self-
modification, bots, merge commits) was unverifiable except by pushing. This is
the same logic, runnable and selftested.

Exemptions, in order:
  E1  no synthesis path touched                  -> token not required
  E2  the commit modifies the doctrine itself    -> exempt; re-attestation is
      owed within RE_ATTESTATION_WINDOW (5 commits or by next session close),
      enforced separately by the attestation checks
  E3  bot / automation author                    -> exempt
  E4  merge commit (>1 parent)                   -> exempt

Checks:
  C1  a token is present when one is required
  C2  the token matches HEAD:governance/mission-and-epistemics.md

Usage:
    python3 scripts/ci_helpers/check_doctrine_token.py                # HEAD vs HEAD~1
    python3 scripts/ci_helpers/check_doctrine_token.py --target <sha> --before <sha>
    python3 scripts/ci_helpers/check_doctrine_token.py --selftest

Exit codes: 0 = pass or exempt, 1 = fail, 2 = cannot run.
"""

import argparse
import re
import subprocess
import sys

SYNTHESIS_RE = re.compile(
    r"^(references/bpc-reasoning|references/connection-reasoning|decisions|sessions)/"
)
TOKEN_RE = re.compile(r"\[DOCTRINE:\s*([a-f0-9]{7})\]")
DOCTRINE_PATH = "governance/mission-and-epistemics.md"
BOT_RE = re.compile(r"dependabot|github-actions|-bot@")


def git(*args):
    proc = subprocess.run(["git", *args], capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def changed_files(target, before):
    if before:
        rc, out, _ = git("diff", "--name-only", before, target)
        if rc == 0:
            return out.splitlines()
    rc, out, _ = git("show", "--name-only", "--format=", target)
    return out.splitlines() if rc == 0 else []


def evaluate(files, message, author, parent_count, expected):
    """Pure decision function — no git, so the selftest can drive it directly.
    Returns (exit_code, explanation)."""
    if not any(SYNTHESIS_RE.match(f) for f in files):
        return 0, "E1: no synthesis paths touched — doctrine token not required."
    if DOCTRINE_PATH in files:
        return 0, ("E2: doctrine commit — token exempt. Re-attestation required "
                   "within RE_ATTESTATION_WINDOW commits.")
    if BOT_RE.search(author or ""):
        return 0, f"E3: bot commit ({author}) — exempt."
    if parent_count > 1:
        return 0, "E4: merge commit — exempt."

    match = TOKEN_RE.search(message or "")
    if not match:
        return 1, ("C1 FAIL: commit touches synthesis paths; the message must contain "
                   f"[DOCTRINE: <7-char-sha>].\n  Expected token: [DOCTRINE: {expected}]\n"
                   "  PR note: only the head commit message is checked; intermediate "
                   "commits are not walked.")
    token = match.group(1)
    if token != expected:
        return 1, (f"C2 FAIL: doctrine token [{token}] does not match "
                   f"HEAD:{DOCTRINE_PATH} ({expected}).\n"
                   "  The doctrine changed since this commit was authored. "
                   "Re-read it and update the token.")
    return 0, f"C2 PASS: doctrine token {token} matches HEAD."


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", default="HEAD", help="commit to check (default HEAD)")
    ap.add_argument("--before", default="", help="base commit for the diff")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    rc, expected, err = git("rev-parse", f"HEAD:{DOCTRINE_PATH}")
    if rc != 0:
        print(f"ERROR: cannot resolve HEAD:{DOCTRINE_PATH} — {err}")
        return 2
    expected = expected[:7]

    files = changed_files(args.target, args.before)
    _, message, _ = git("log", "-1", "--format=%B", args.target)
    _, author, _ = git("log", "-1", "--format=%ae", args.target)
    _, parents, _ = git("log", "-1", "--format=%P", args.target)

    code, explanation = evaluate(files, message, author, len(parents.split()), expected)
    print(explanation)
    return code


def selftest():
    """Drive `evaluate` through every branch. The exemption logic is the part that
    silently over-permits, so each exemption is asserted individually."""
    print("=" * 70)
    print("check_doctrine_token --selftest")
    print("=" * 70)
    failures = []
    sha = "0f2f525"

    cases = [
        ("E1 non-synthesis change needs no token",
         (["scripts/x.py"], "tooling: x [2026-08-01 10:00]", "a@b.com", 1, sha), 0),
        ("E2 doctrine self-modification is exempt",
         ([f"{DOCTRINE_PATH}", "decisions/DR-x.md"], "gov: amend [2026-08-01 10:00]",
          "a@b.com", 1, sha), 0),
        ("E3 bot commit is exempt",
         (["sessions/s.md"], "bot: x [2026-08-01 10:00]",
          "github-actions[bot]@users.noreply.github.com", 1, sha), 0),
        ("E4 merge commit is exempt",
         (["sessions/s.md"], "Merge pull request #1", "a@b.com", 2, sha), 0),
        ("C1 synthesis change with NO token FAILS",
         (["references/bpc-reasoning/x.md"], "bpc: x [2026-08-01 10:00]",
          "a@b.com", 1, sha), 1),
        ("C2 synthesis change with WRONG token FAILS",
         (["decisions/DR-x.md"], f"gov: x [DOCTRINE: deadbee] [2026-08-01 10:00]",
          "a@b.com", 1, sha), 1),
        ("C2 synthesis change with correct token PASSES",
         (["decisions/DR-x.md"], f"gov: x [DOCTRINE: {sha}] [2026-08-01 10:00]",
          "a@b.com", 1, sha), 0),
        ("connection-reasoning counts as a synthesis path",
         (["references/connection-reasoning/CON-1.md"], "bpc: x [2026-08-01 10:00]",
          "a@b.com", 1, sha), 1),
        ("a path merely CONTAINING 'decisions/' does not count",
         (["data/decisions/decision_register.yaml"], "data: x [2026-08-01 10:00]",
          "a@b.com", 1, sha), 0),
    ]

    for label, args, expected_code in cases:
        code, _ = evaluate(*args)
        if code == expected_code:
            print(f"  [PASS] {label}")
        else:
            print(f"  [FAIL] {label}: expected exit {expected_code}, got {code}")
            failures.append(label)

    print("=" * 70)
    if failures:
        print(f"SELFTEST: FAIL — {len(failures)} case(s): {', '.join(failures)}")
        return 1
    print("SELFTEST: PASS — token gate and all four exemptions behave as documented.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
