#!/usr/bin/env python3
"""
pipeline_contract_audit.py — validate the governance pipeline contract.

The pipeline contract (governance/pipeline-contract.yaml, PROPOSED per
DR-2026-07-13-pipeline-contract) declares, per pipeline stage, the integrity +
completeness criteria a stage's output must meet, and names the ratified enforcer
for each. This audit makes the contract itself trustworthy — its whole value is
that no stage cites a gate that does not exist.

Checks:
  1. Contract well-formed — loads + validates against schemas/pipeline_contract.py.
     FAIL (exit 1) on any schema violation.
  2. Referential integrity — every non-null `check` path exists in the repo.
     A missing path is BROKEN (phantom enforcement) -> FAIL. A null check is
     INCOMPLETE (declared-but-unenforced; an honest coverage gap, not a failure).
  3. Enforcer self-verification (INFO) — for each VERIFIABLE check under scripts/,
     note whether it ships a `--selftest` (the evidence-architecture §10 rule that a
     check's passes count only once it is demonstrated firing on injected violations).

Ships its mutation harness (`--selftest`): the canonical contract validates; a
malformed / unknown-field contract is rejected; a phantom check path is classed BROKEN.

Exit code: 0 = contract valid and no BROKEN check; 1 = otherwise.

Usage:
    python3 scripts/audit/pipeline_contract_audit.py
    python3 scripts/audit/pipeline_contract_audit.py --selftest
"""
import os
import sys
from pathlib import Path

REPO = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, str(REPO))

from schemas.pipeline_contract import PipelineContract   # noqa: E402

CONTRACT_PATH = REPO / "governance" / "pipeline-contract.yaml"
SEP = "=" * 70


def classify_check(path):
    if path is None:
        return "INCOMPLETE"
    return "VERIFIABLE" if (REPO / path).exists() else "BROKEN"


def _has_selftest(path):
    try:
        return "--selftest" in (REPO / path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False


def audit():
    print(SEP)
    print("pipeline_contract_audit.py — governance/pipeline-contract.yaml")
    print(SEP)
    try:
        contract = PipelineContract.load(CONTRACT_PATH)
    except Exception as e:  # noqa: BLE001  (report any load/validation failure as FAIL)
        print(f"[1] FAIL: contract does not validate:\n{e}")
        print(SEP)
        print("VERDICT: FAIL (invalid contract)")
        print(SEP)
        return 1
    print(f"[1] PASS: contract validates (status={contract.status}, "
          f"ratified={contract.ratified}, level={contract.enforcement_level})")

    broken, incomplete, verifiable, no_selftest = [], [], [], []
    for loc, cid, check in contract.all_checks():
        klass = classify_check(check)
        if klass == "BROKEN":
            broken.append((loc, cid, check))
        elif klass == "INCOMPLETE":
            incomplete.append((loc, cid))
        else:
            verifiable.append((loc, cid, check))
            if check.startswith("scripts/") and not _has_selftest(check):
                no_selftest.append(check)

    print(f"[2] referential integrity: {len(verifiable)} VERIFIABLE, "
          f"{len(incomplete)} INCOMPLETE, {len(broken)} BROKEN")
    for loc, cid, check in broken:
        print(f"    BROKEN: {loc}/{cid} -> {check} (phantom enforcement — path missing)")
    if incomplete:
        print("    INCOMPLETE (declared-but-unenforced coverage gaps):")
        for loc, cid in incomplete:
            print(f"      - {loc}/{cid}")

    print(f"[3] INFO: {len(verifiable) - len(set(no_selftest))} of {len(verifiable)} "
          f"enforcers ship a --selftest; {len(set(no_selftest))} do not "
          f"(pass counts only after demonstrated firing — evidence-architecture §10):")
    for c in sorted(set(no_selftest)):
        print(f"      - {c}")

    # per-stage coverage
    print()
    for st in contract.stages:
        v = sum(1 for c in st.criteria if classify_check(c.check) == "VERIFIABLE")
        i = sum(1 for c in st.criteria if classify_check(c.check) == "INCOMPLETE")
        b = sum(1 for c in st.criteria if classify_check(c.check) == "BROKEN")
        print(f"    stage {st.id:11s}: {v} verifiable / {i} incomplete / {b} broken")

    print()
    print(SEP)
    ok = not broken
    print(f"VERDICT: {'PASS' if ok else 'FAIL'}   "
          f"(broken={len(broken)}, incomplete={len(incomplete)}, verifiable={len(verifiable)})")
    print(SEP)
    return 0 if ok else 1


# --------------------------------------------------------------------------- #
# mutation harness
# --------------------------------------------------------------------------- #
def _minimal_contract():
    return {
        "version": 1, "status": "PROPOSED", "ratified": False, "authored_by": "t",
        "dr": "d", "enforcement_level": 2, "spine": "s",
        "stages": [{"id": "research", "anchor": "a", "entry": ["e"],
                    "criteria": [{"id": "c1", "kind": "integrity", "criterion": "x",
                                  "references": "r", "check": None}]}],
        "cross_stage": [{"id": "g1", "criterion": "x", "references": "r", "check": None}],
    }


def selftest():
    from pydantic import ValidationError
    print(SEP)
    print("pipeline_contract_audit.py --selftest (mutation harness)")
    print(SEP)
    results = []

    try:
        c = PipelineContract.load(CONTRACT_PATH)
        ok = c.status == "PROPOSED" and c.ratified is False and len(c.stages) >= 3
    except Exception:  # noqa: BLE001
        ok = False
    results.append(("canonical contract validates and is PROPOSED", ok))

    bad = _minimal_contract()
    del bad["version"]
    try:
        PipelineContract.model_validate(bad)
        rejected = False
    except ValidationError:
        rejected = True
    results.append(("contract missing a required field is rejected", rejected))

    bad2 = _minimal_contract()
    bad2["surprise"] = "x"
    try:
        PipelineContract.model_validate(bad2)
        rejected2 = False
    except ValidationError:
        rejected2 = True
    results.append(("contract with an unknown field is rejected (extra=forbid)", rejected2))

    checks_ok = (classify_check("scripts/does/not/exist.py") == "BROKEN"
                 and classify_check("scripts/migrate_db.py") == "VERIFIABLE"
                 and classify_check(None) == "INCOMPLETE")
    results.append(("phantom check -> BROKEN, real -> VERIFIABLE, null -> INCOMPLETE", checks_ok))

    ok_all = True
    for name, passed in results:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok_all = ok_all and passed
    print(SEP)
    print(f"SELFTEST: {'PASS' if ok_all else 'FAIL'} ({sum(1 for _, p in results if p)}/{len(results)})")
    print(SEP)
    return 0 if ok_all else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    return audit()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
