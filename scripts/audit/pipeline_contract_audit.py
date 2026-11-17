#!/usr/bin/env python3
"""
pipeline_contract_audit.py — validate the governance pipeline contract.

The pipeline contract (governance/pipeline-contract.yaml, header per
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
  3. Re-entry carriers (a stage's `re_entry:` list, OD-18) — every ruled return names a later
     stage it comes back from, and a table, column and (for a state) value that exist in the
     live schema. A carrier that does not exist is a return nothing can record. FAIL.
  4. Enforcer self-verification (INFO) — for each VERIFIABLE check under scripts/,
     note whether it ships a `--selftest` (the evidence-architecture §10 rule that a
     check's passes count only once it is demonstrated firing on injected violations).

Ships its mutation harness (`--selftest`): the canonical contract validates; a
malformed / unknown-field contract is rejected; a phantom check path is classed BROKEN; a
re-entry whose carrier is missing, or whose source stage is not later, is reported.

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
sys.path.insert(0, str(REPO / "scripts"))

import dbcore                                            # noqa: E402
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
    disk. Existing is not running: `register-invariants` cited
    scripts/audit/register_integrity_check.py, which was QUARANTINED in the
    registry (it needed an `html` positional so it could not run corpus-wide, and
    it still enforced I3's repealed absolute form). The file existed, so the
    contract reported its render-stage invariants as VERIFIABLE — phantom
    enforcement that this audit was structurally unable to see, in the one check
    whose stated purpose is that "no stage cites a gate that does not exist".

    That example is now historical: the DR-2026-07-21 Option A rework landed on
    2026-08-04 and `register-invariants` is genuinely VERIFIABLE. The correction
    stands on its own reasoning, not on that instance — which is why the
    selftest fixture was repointed at a check that is still shelved rather than
    quietly dropped.

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


def re_entry_problems(contract, conn):
    """Every `re_entry` that cannot work, as (location, why). Reads the schema, writes nothing.

    A return is ruled back from a LATER stage, and is carried by a column that already exists;
    a value, where the column is a state, is one its own CHECK admits (dbcore.check_values).
    """
    order = [st.id for st in contract.stages]
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    out = []
    seen = set()
    for st in contract.stages:
        for r in st.re_entry or []:
            loc = f"stage:{st.id}/{r.id}"
            if r.id in seen:
                out.append((loc, f"re-entry id {r.id!r} is held twice"))
            seen.add(r.id)
            if r.from_stage not in order or order.index(r.from_stage) <= order.index(st.id):
                out.append((loc, f"from_stage {r.from_stage!r} is not a later stage of the contract"))
            if r.carrier_table not in tables:
                out.append((loc, f"carrier table {r.carrier_table!r} does not exist"))
                continue
            cols = {c[1] for c in conn.execute(f'PRAGMA table_info("{r.carrier_table}")')}
            if r.carrier_column not in cols:
                out.append((loc, f"{r.carrier_table} has no column {r.carrier_column!r}"))
            elif r.carrier_value is not None and r.carrier_value not in dbcore.check_values(
                    conn, r.carrier_table, r.carrier_column):
                out.append((loc, f"{r.carrier_value!r} is not in the CHECK of "
                                 f"{r.carrier_table}.{r.carrier_column}"))
    return out


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

    edges = [(st.id, r) for st in contract.stages for r in st.re_entry or []]
    with dbcore.connect(readonly=True) as conn:
        bad = re_entry_problems(contract, conn)
    print(f"[3] re-entry carriers: {len(edges)} ruled returns, {len(bad)} with no working carrier")
    for loc, why in bad:
        print(f"    BROKEN: {loc} -- {why}")

    # Self-verification is a property of an ENFORCER (a path), not of a criterion:
    # count over the UNIQUE verifiable enforcer paths, not the criteria list (several
    # criteria reuse the same enforcer, e.g. validate_evidence_state.py x3).
    enforcers = sorted({check for _, _, check in verifiable})
    with_selftest = [p for p in enforcers if _has_selftest(p)]
    without_selftest = [p for p in enforcers if not _has_selftest(p)]
    print(f"[4] INFO: {len(with_selftest)} of {len(enforcers)} UNIQUE enforcers ship a "
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

    n_crit = len(list(contract.all_checks()))
    print(f"\nEXAMINED: {n_crit + len(edges)} contract criteria and re-entry edges "
          f"({len(edges)} of them re-entry edges)")
    print(SEP)
    # QUARANTINED and UNREGISTERED join BROKEN as failures. All three are the same
    # fault in different clothes — the contract asserts a criterion is enforced
    # when nothing enforces it. Counting only BROKEN was what let
    # `register-invariants` read green while pointing at a shelved script.
    ok = not (broken or quarantined or unregistered or bad)
    print(f"VERDICT: {'PASS' if ok else 'FAIL'}   "
          f"(broken={len(broken)}, quarantined={len(quarantined)}, "
          f"unregistered={len(unregistered)}, re_entry_broken={len(bad)}, incomplete={len(incomplete)}, "
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
        ok = len(c.stages) >= 3
    except Exception:  # noqa: BLE001
        ok = False
    results.append(("canonical contract validates and declares stages", ok))

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
    # The fixtures name files that exist and a SYNTHETIC registry. A fixture that names a live
    # check is a caller of the registry: this one broke on 2026-08-04 (register_integrity_check
    # de-quarantined), again on 2026-08-20 (validate_conflicts deleted), and again when a
    # deletion step emptied the quarantine. Whether the live registry is read correctly is its
    # own case, below.
    registry = {"scripts/db.py": ("fixture_active", "ACTIVE"),
                "scripts/dbcore.py": ("fixture_shelved", "QUARANTINED")}
    fixtures = {
        # id                         path                                         expected
        "missing path":              ("scripts/does/not/exist.py",                "BROKEN"),
        "active registered check":   ("scripts/db.py",                            "VERIFIABLE"),
        "quarantined check":         ("scripts/dbcore.py",                        "QUARANTINED"),
        "exists but unregistered":   ("scripts/migrate_db.py",                    "UNREGISTERED"),
        "no enforcer named":         (None,                                       "INCOMPLETE"),
    }
    for label, (path, expected) in fixtures.items():
        got = classify_check(path, registry)
        results.append((f"{label} -> {expected}" + ("" if got == expected else f" (got {got})"),
                        got == expected))
    results.append(("the live registry index lists this audit as an ACTIVE check",
                    _registry_index().get("scripts/audit/pipeline_contract_audit.py", (None, None))[1] == "ACTIVE"))

    # T022: the re-entry list. The fixtures are a minimal contract with two stages and an in-memory
    # TASK-FIXTURE schema, so no case names a live table; the last case reads the live contract.
    import sqlite3
    fx = sqlite3.connect(":memory:")
    fx.execute("CREATE TABLE fx_carrier (k TEXT CHECK (k IN ('a','b')), p INTEGER)")   # TASK-FIXTURE

    def with_edge(**kw):
        d = _minimal_contract()
        d["stages"].append({"id": "later", "anchor": "a", "entry": ["e"], "criteria": []})
        edge = {"id": "r1", "from_stage": "later", "when": "w", "carrier_table": "fx_carrier",
                "carrier_column": "p", "references": "x"}
        edge.update(kw)
        d["stages"][0]["re_entry"] = [edge]
        return d

    def problems(**kw):
        return re_entry_problems(PipelineContract.model_validate(with_edge(**kw)), fx)

    try:
        PipelineContract.model_validate(with_edge())
        loads = True
    except ValidationError:
        loads = False
    results.append(("T022-01 a stage with a re_entry list validates", loads))
    try:
        PipelineContract.model_validate(with_edge(surprise="x"))
        rejected3 = False
    except ValidationError:
        rejected3 = True
    results.append(("T022-02 a re_entry with an unknown key is rejected (extra=forbid)", rejected3))
    results.append(("T022-03 a carrier that exists reports no problem", problems() == []))
    results.append(("T022-04 a carrier table that does not exist is reported",
                    len(problems(carrier_table="fx_absent")) == 1))
    results.append(("T022-05 a carrier column that does not exist is reported",
                    len(problems(carrier_column="absent")) == 1))
    results.append(("T022-06 a state value outside the column's own CHECK is reported",
                    len(problems(carrier_column="k", carrier_value="c")) == 1
                    and problems(carrier_column="k", carrier_value="a") == []))
    results.append(("T022-07 a source stage that is not later is reported",
                    len(problems(from_stage="research")) == 1))
    two = with_edge()
    two["stages"][0]["re_entry"].append(dict(two["stages"][0]["re_entry"][0]))
    results.append(("T022-09 an edge id held twice is reported",
                    len(re_entry_problems(PipelineContract.model_validate(two), fx)) == 1))
    back = with_edge()                 # the edge sits on the later stage and names the EARLIER one: not a return
    back["stages"][1]["re_entry"] = [dict(back["stages"][0]["re_entry"][0], from_stage=back["stages"][0]["id"])]
    back["stages"][0]["re_entry"] = []
    results.append(("T022-10 a source stage EARLIER than the stage's own is reported (not only the stage itself)",
                    len(re_entry_problems(PipelineContract.model_validate(back), fx)) == 1))
    with dbcore.connect(readonly=True) as live:
        live_bad = re_entry_problems(PipelineContract.load(CONTRACT_PATH), live)
    results.append(("T022-08 every re-entry carrier of the canonical contract exists in the live schema",
                    live_bad == []))

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
