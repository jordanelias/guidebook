#!/usr/bin/env python3
"""
test_pipeline_contract.py — battery wrapper for the pipeline-contract audit.

Runs the contract audit's mutation harness (--selftest) and asserts a plain run
over governance/pipeline-contract.yaml exits 0 (contract valid, no BROKEN check).
Requires pydantic (pinned in requirements.txt). Matches the repo's standalone-script
test convention.

Usage:
    python3 scripts/tests/test_pipeline_contract.py
"""
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUDIT = os.path.join(REPO, "scripts", "audit", "pipeline_contract_audit.py")


def _run(args):
    return subprocess.run([sys.executable, AUDIT] + args, cwd=REPO,
                          capture_output=True, text=True)


def main():
    ok = True
    r = _run(["--selftest"])
    passed = r.returncode == 0 and "SELFTEST: PASS" in r.stdout
    print(f"[{'PASS' if passed else 'FAIL'}] pipeline_contract_audit --selftest")
    if not passed:
        print(r.stdout + r.stderr)
    ok = ok and passed

    r = _run([])
    passed = r.returncode == 0 and "VERDICT: PASS" in r.stdout
    print(f"[{'PASS' if passed else 'FAIL'}] pipeline_contract_audit clean run exits 0")
    if not passed:
        print(r.stdout + r.stderr)
    ok = ok and passed

    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
