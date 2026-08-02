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
  2. Referential integrity — every non-null `check` resolves to a check the
     REGISTRY ACTUALLY RUNS. Five outcomes:
       VERIFIABLE   active entry in check-registry.yaml            -> ok
       QUARANTINED  registered but never selected                  -> FAIL
       UNREGISTERED file exists, no registry entry runs it          -> FAIL
       BROKEN       path missing entirely                           -> FAIL
       INCOMPLETE   `check: null`, an honest declared gap           -> not a failure
     Until 2026-08-01 this checked only that the FILE EXISTED, so
     `register-invariants` — which cites the quarantined register_integrity_check.py
     — reported VERIFIABLE. The one audit whose stated purpose is that "no stage
     cites a gate that does not exist" could not see a gate that does not run.
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


REGISTRY_PATH = REPO / "governance" / "check-registry.yaml"


def _registry_index():
    """Map every script path the registry knows to (registry_id, status).

    The registry is the only thing that decides whether a check RUNS. A contract
    that cites an enforcer is making a claim about enforcement, so it has to be
    resolved against the registry, not against the filesystem.
    """
    import yaml
    try:
        reg = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    except OSError:
        return {}
    index = {}
    for entry in reg.get("checks", []) or []:
        for token in entry.get("cmd", []):
            if isinstance(token, str) and token.endswith((".py", ".js")):
                index[token] = (entry["id"], "ACTIVE")
    for entry in reg.get("quarantine", []) or []:
        for token in entry.get("cmd", []):
            if isinstance(token, str) and token.endswith((".py", ".js")):
                index.setdefault(token, (entry.get("id", "?"), "QUARANTINED"))
    return index


def classify_check(path, registry=None):
    """Classify a contract criterion's enforcer.

    CORRECTED 2026-08-01. This returned VERIFIABLE whenever the file existed on
    disk. Existing is not running: `register-invariants` cites
    scripts/audit/register_integrity_check.py, which is QUARANTINED in the
    registry (it needs an `html` positional so it cannot run corpus-wide, and it
    still enforces I3's repealed absolute form). The file exists, so the contract
    reported its render-stage invariants as VERIFIABLE — phantom enforcement that
    this audit was structurally unable to see, in the one check whose stated
    purpose is that "no stage cites a gate that does not exist".

    Existence is still checked, because a path that is gone is a different and
    worse fault than one that is merely shelved.
    """
    if path is None:
        return "INCOMPLETE"
    if not (REPO / path).exists():
        return "BROKEN"
    registry = _registry_index() if registry is None else registry
    entry = registry.get(path)
    if entry is None:
        return "UNREGISTERED"
    return "VERIFIABLE" if entry[1] == "ACTIVE" else "QUARANTINED"


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

    registry = _registry_index()
    broken, incomplete, verifiable = [], [], []
    quarantined, unregistered = [], []
    for loc, cid, check in contract.all_checks():
        klass = classify_check(check, registry)
        if klass == "BROKEN":
            broken.append((loc, cid, check))
        elif klass == "INCOMPLETE":
            incomplete.append((loc, cid))
        elif klass == "QUARANTINED":
            quarantined.append((loc, cid, check))
        elif klass == "UNREGISTERED":
            unregistered.append((loc, cid, check))
        else:
            verifiable.append((loc, cid, check))

    print(f"[2] referential integrity: {len(verifiable)} VERIFIABLE criteria, "
          f"{len(incomplete)} INCOMPLETE, {len(quarantined)} QUARANTINED, "
          f"{len(unregistered)} UNREGISTERED, {len(broken)} BROKEN")
    for loc, cid, check in broken:
        print(f"    BROKEN: {loc}/{cid} -> {check} (phantom enforcement — path missing)")
    for loc, cid, check in quarantined:
        print(f"    QUARANTINED: {loc}/{cid} -> {check}")
        print(f"      the file exists but the registry never selects it, so this "
              f"criterion is declared enforced and is not enforced")
    for loc, cid, check in unregistered:
        print(f"    UNREGISTERED: {loc}/{cid} -> {check}")
        print(f"      the file exists but no registry entry runs it")
    if incomplete:
        print("    INCOMPLETE (declared-but-unenforced coverage gaps):")
        for loc, cid in incomplete:
            print(f"      - {loc}/{cid}")

    # Self-verification is a property of an ENFORCER (a path), not of a criterion:
    # count over the UNIQUE verifiable enforcer paths, not the criteria list (several
    # criteria reuse the same enforcer, e.g. validate_evidence_state.py x3).
    enforcers = sorted({check for _, _, check in verifiable})
    with_selftest = [p for p in enforcers if _has_selftest(p)]
    without_selftest = [p for p in enforcers if not _has_selftest(p)]
    print(f"[3] INFO: {len(with_selftest)} of {len(enforcers)} UNIQUE enforcers ship a "
          f"--selftest; {len(without_selftest)} do not (a check's passes count only "
          f"after demonstrated firing — evidence-architecture §10). NOTE: a lower bound "
          f"— an enforcer whose mutation harness lives in scripts/tests/ reads as 'no':")
    for c in without_selftest:
        print(f"      - {c}")

    # per-stage coverage
    print()
    for st in contract.stages:
        klasses = [classify_check(c.check, registry) for c in st.criteria]
        v = klasses.count("VERIFIABLE")
        i = klasses.count("INCOMPLETE")
        b = klasses.count("BROKEN") + klasses.count("QUARANTINED") + klasses.count("UNREGISTERED")
        print(f"    stage {st.id:11s}: {v} verifiable / {i} incomplete / {b} not-enforced")

    print(f"\nEXAMINED: {len(list(contract.all_checks()))} contract criteria")
    print(SEP)
    # QUARANTINED and UNREGISTERED join BROKEN as failures. All three are the same
    # fault in different clothes — the contract asserts a criterion is enforced
    # when nothing enforces it. Counting only BROKEN was what let
    # `register-invariants` read green while pointing at a shelved script.
    ok = not (broken or quarantined or unregistered)
    print(f"VERDICT: {'PASS' if ok else 'FAIL'}   "
          f"(broken={len(broken)}, quarantined={len(quarantined)}, "
          f"unregistered={len(unregistered)}, incomplete={len(incomplete)}, "
          f"verifiable={len(verifiable)})")
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

    # Classification is now resolved against the registry, not the filesystem, so
    # the harness has to distinguish all five outcomes. The old version asserted
    # `classify_check("scripts/migrate_db.py") == "VERIFIABLE"` — encoding the very
    # defect being fixed: migrate_db.py exists but no registry entry runs it, so
    # "the file is there" was being read as "the criterion is enforced".
    fixtures = {
        # id                         path                                         expected
        "missing path":              ("scripts/does/not/exist.py",                "BROKEN"),
        "active registered check":   ("scripts/audit/pmp_audit.py",               "VERIFIABLE"),
        "quarantined check":         ("scripts/audit/register_integrity_check.py", "QUARANTINED"),
        "exists but unregistered":   ("scripts/migrate_db.py",                    "UNREGISTERED"),
        "no enforcer named":         (None,                                       "INCOMPLETE"),
    }
    registry = _registry_index()
    for label, (path, expected) in fixtures.items():
        got = classify_check(path, registry)
        results.append((f"{label} -> {expected}" + ("" if got == expected else f" (got {got})"),
                        got == expected))

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
