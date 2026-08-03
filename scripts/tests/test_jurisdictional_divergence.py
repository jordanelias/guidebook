#!/usr/bin/env python3
"""
test_jurisdictional_divergence.py — battery wrapper for the jurisdictional
value-divergence surface. Runs the mutation harness (--selftest) and asserts a
plain run over the canonical DB exits 0 (descriptive tool). Matches the repo's
standalone-script test convention.

Usage:
    python3 scripts/tests/test_jurisdictional_divergence.py
"""
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUDIT = os.path.join(REPO, "scripts", "audit", "jurisdictional_divergence.py")


def _run(args):
    return subprocess.run([sys.executable, AUDIT] + args, cwd=REPO,
                          capture_output=True, text=True)


def main():
    ok = True
    r = _run(["--selftest"])
    passed = r.returncode == 0 and "SELFTEST: PASS" in r.stdout
    print(f"[{'PASS' if passed else 'FAIL'}] jurisdictional_divergence --selftest")
    if not passed:
        print(r.stdout + r.stderr)
    ok = ok and passed

    r = _run([])
    passed = r.returncode == 0 and "SURFACED:" in r.stdout
    print(f"[{'PASS' if passed else 'FAIL'}] jurisdictional_divergence clean run exits 0")
    if not passed:
        print(r.stdout + r.stderr)
    ok = ok and passed

    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
