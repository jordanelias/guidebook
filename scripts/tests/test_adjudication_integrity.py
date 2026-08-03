#!/usr/bin/env python3
"""
test_adjudication_integrity.py — battery wrapper for the adjudication-integrity
audit. Runs the mutation harness (--selftest) and asserts a plain run over the
canonical DB exits 0 (tier-consistent). Requires the pure-Python
schemas/tier_derivation.py. Matches the repo's standalone-script test convention.
"""
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUDIT = os.path.join(REPO, "scripts", "audit", "adjudication_integrity.py")


def _run(args):
    return subprocess.run([sys.executable, AUDIT] + args, cwd=REPO,
                          capture_output=True, text=True)


def main():
    ok = True
    r = _run(["--selftest"])
    passed = r.returncode == 0 and "SELFTEST: PASS" in r.stdout
    print(f"[{'PASS' if passed else 'FAIL'}] adjudication_integrity --selftest")
    if not passed:
        print(r.stdout + r.stderr)
    ok = ok and passed

    r = _run([])
    passed = r.returncode == 0 and "VERDICT: PASS" in r.stdout
    print(f"[{'PASS' if passed else 'FAIL'}] adjudication_integrity clean run exits 0")
    if not passed:
        print(r.stdout + r.stderr)
    ok = ok and passed

    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
