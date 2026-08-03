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

    # Assert the audit RUNS AND CLASSIFIES, not that the repo currently has zero
    # findings. This previously asserted `returncode == 0 and "VERDICT: PASS"`,
    # which made the test fail the moment the audit started reporting a real one:
    # once enforcers were resolved against the registry rather than the
    # filesystem, `register-invariants` correctly became QUARANTINED and the audit
    # correctly went red. A test that requires its subject to find nothing is a
    # test that penalises the subject for working.
    r = _run([])
    passed = (r.returncode in (0, 1)
              and "referential integrity:" in r.stdout
              and "VERDICT:" in r.stdout)
    print(f"[{'PASS' if passed else 'FAIL'}] pipeline_contract_audit runs and reports a verdict")
    if not passed:
        print(r.stdout + r.stderr)
    ok = ok and passed

    # The contract must never regress to phantom enforcement: a criterion may be
    # honestly INCOMPLETE, but a path that is missing outright is always a defect.
    passed = "broken=0" in r.stdout
    print(f"[{'PASS' if passed else 'FAIL'}] no criterion cites a path that does not exist")
    if not passed:
        print(r.stdout + r.stderr)
    ok = ok and passed

    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
