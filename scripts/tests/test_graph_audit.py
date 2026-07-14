#!/usr/bin/env python3
"""
test_graph_audit.py — battery wrapper for the vectorized structural graph audit.

Runs the graph_audit mutation harness (--selftest, which fires every check on
tampered input) and asserts a plain audit run over the canonical DB exits 0 (no
live ERROR). Matches the repo's standalone-script test convention (no pytest).

Usage:
    python3 scripts/tests/test_graph_audit.py
"""
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUDIT = os.path.join(REPO, "scripts", "audit", "graph_audit.py")


def _run(args):
    return subprocess.run([sys.executable, AUDIT] + args, cwd=REPO,
                          capture_output=True, text=True)


def main():
    ok = True
    r = _run(["--selftest"])
    passed = r.returncode == 0 and "SELFTEST: PASS" in r.stdout
    print(f"[{'PASS' if passed else 'FAIL'}] graph_audit --selftest (mutation harness)")
    if not passed:
        print(r.stdout + r.stderr)
    ok = ok and passed

    r = _run([])
    passed = r.returncode == 0 and "VERDICT: PASS" in r.stdout
    print(f"[{'PASS' if passed else 'FAIL'}] graph_audit clean run exits 0")
    if not passed:
        print(r.stdout + r.stderr)
    ok = ok and passed

    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
