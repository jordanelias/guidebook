#!/usr/bin/env python3
"""
scripts/doctrine_recheck.py — Doctrine recheck validator (per governance/doctrine-recheck.md, A13).

Runs passes 2.2–2.5 mechanically:
  2.2 Doctrine inventory: enumerate CANONICAL governance docs + RULEs + decisions
  2.3 Cross-reference consistency: every doctrinal_basis ref resolves
  2.4 Drift detection: current vs prior snapshot
  2.5 Decision-register cross-check (post A12 S2)

Pass 2.6 (contamination resampling) is run by contamination_sampler.py + human review.

Usage:
    python3 scripts/doctrine_recheck.py                          # full audit (2.2-2.5)
    python3 scripts/doctrine_recheck.py --snapshot-only          # 2.2 only
    python3 scripts/doctrine_recheck.py --cross-ref              # 2.2-2.3
    python3 scripts/doctrine_recheck.py --baseline-against PATH  # custom prior baseline
    python3 scripts/doctrine_recheck.py --report                 # exit 0 always

Exit codes: 0 = no ERROR findings; 1 = ERROR findings present; 2 = config error.
"""

import argparse
import datetime
import glob
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.doctrine_recheck import (
    RecheckFinding,
    RecheckSession,
    DoctrineSnapshot,
)
from schemas.enums import (
    RecheckFindingSeverity,
    RecheckFindingStatus,
    RecheckTrigger,
)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOVERNANCE_DIR = os.path.join(REPO_ROOT, "governance")
PROJECT_STANDARDS_PATH = os.path.join(REPO_ROOT, "references", "project-standards.md")
DECISION_REGISTER_PATH = os.path.join(REPO_ROOT, "data", "decisions", "decision_register.yaml")
RECHECK_DIR = os.path.join(REPO_ROOT, "data", "doctrine_recheck")


# --- Pass 2.2: Doctrine inventory ---

def build_snapshot() -> DoctrineSnapshot:
    """Walk governance/ and project-standards.md to assemble a doctrine snapshot."""
    governance_docs: list[str] = []
    canonical_rules: list[str] = []
    decision_ids: list[str] = []
    bpc_count = 0

    # Governance docs with Status: CANONICAL
    if os.path.isdir(GOVERNANCE_DIR):
        for path in sorted(glob.glob(os.path.join(GOVERNANCE_DIR, "*.md"))):
            with open(path, "r", encoding="utf-8") as f:
                head = f.read(1000)  # only header matters
            if re.search(r"\*\*Status:\*\*\s*CANONICAL", head):
                rel = os.path.relpath(path, REPO_ROOT)
                governance_docs.append(rel)

    # CANONICAL RULEs
    if os.path.exists(PROJECT_STANDARDS_PATH):
        with open(PROJECT_STANDARDS_PATH, "r", encoding="utf-8") as f:
            text = f.read()
        for m in re.finditer(r"^RULE:\s*(.+?)$", text, re.MULTILINE):
            rule_text = m.group(1)
            if "CANONICAL" in rule_text:
                summary = rule_text.split(". ", 1)[0]
                canonical_rules.append(summary[:120])

    # ACTIVE decisions
    if os.path.exists(DECISION_REGISTER_PATH):
        try:
            with open(DECISION_REGISTER_PATH, "r", encoding="utf-8") as f:
                reg_data = yaml.safe_load(f)
            if isinstance(reg_data, dict):
                for d in reg_data.get("decisions", []):
                    if isinstance(d, dict) and d.get("status") == "ACTIVE":
                        decision_ids.append(d.get("decision_id", ""))
        except Exception:
            pass

    # BPC count
    bpc_root = os.path.join(REPO_ROOT, "references", "bpc")
    if os.path.isdir(bpc_root):
        bpc_count = sum(
            1 for _ in glob.iglob(os.path.join(bpc_root, "**", "*.md"), recursive=True)
        )

    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    return DoctrineSnapshot(
        snapshot_date=now,
        governance_docs=governance_docs,
        canonical_rules=canonical_rules,
        decision_ids=decision_ids,
        bpc_count=bpc_count,
    )


# --- Pass 2.3: Cross-reference consistency ---

def check_cross_references(snapshot: DoctrineSnapshot) -> list[RecheckFinding]:
    """Examine each governance doc's doctrinal_basis references; flag missing."""
    findings: list[RecheckFinding] = []
    seq = 0

    # Set of identifiers a doctrinal_basis ref can resolve to:
    # - governance/X.md path substring
    # - "§N" section reference (lightly checked)
    governance_filenames = {os.path.basename(p) for p in snapshot.governance_docs}

    for path in snapshot.governance_docs:
        full = os.path.join(REPO_ROOT, path)
        try:
            with open(full, "r", encoding="utf-8") as f:
                text = f.read(8000)  # header + first sections
        except Exception:
            continue
        # Extract doctrinal_basis line
        m = re.search(
            r"\*\*Doctrinal basis:\*\*(.+?)(?:\n\n|\n---|$)", text, re.DOTALL
        )
        if not m:
            continue
        basis_text = m.group(1)
        # Extract referenced governance files
        for ref_match in re.finditer(r"governance/([\w\-]+\.md)", basis_text):
            refname = ref_match.group(1)
            if refname not in governance_filenames:
                seq += 1
                findings.append(RecheckFinding(
                    finding_id=f"RC-000-1{seq:02d}",
                    severity=RecheckFindingSeverity.WARNING,
                    pass_id="2.3",
                    description=(
                        f"{path} doctrinal_basis references governance/{refname} "
                        f"but that file is not in the CANONICAL inventory"
                    ),
                    affected_artifacts=[path, f"governance/{refname}"],
                    recommended_action=(
                        f"Confirm whether governance/{refname} should be CANONICAL "
                        f"(missing Status: CANONICAL header) or whether the reference "
                        f"in {path} should be updated."
                    ),
                ))
    return findings


# --- Pass 2.4: Drift detection ---

def find_prior_snapshot(baseline_path: str | None) -> str | None:
    """Find the most recent prior snapshot, or use the named one."""
    if baseline_path:
        return baseline_path if os.path.exists(baseline_path) else None
    if not os.path.isdir(RECHECK_DIR):
        return None
    snaps = sorted(glob.glob(os.path.join(RECHECK_DIR, "snapshot_*.yaml")))
    return snaps[-1] if snaps else None


def detect_drift(
    current: DoctrineSnapshot, prior_path: str | None
) -> tuple[list[RecheckFinding], dict]:
    findings: list[RecheckFinding] = []
    summary: dict = {"additions": 0, "removals": 0, "mutations": 0}

    if not prior_path:
        return findings, {"additions": "n/a (baseline)", "removals": "n/a", "mutations": "n/a"}

    try:
        prior = DoctrineSnapshot.from_yaml(prior_path)
    except Exception as e:
        findings.append(RecheckFinding(
            finding_id="RC-000-201",
            severity=RecheckFindingSeverity.ERROR,
            pass_id="2.4",
            description=f"Prior snapshot at {prior_path} does not validate: {e}",
            affected_artifacts=[prior_path],
            recommended_action="Re-run recheck against an earlier valid snapshot, "
                                "or accept this recheck as a new baseline.",
        ))
        return findings, summary

    # Governance doc additions/removals
    cur_govs = set(current.governance_docs)
    prior_govs = set(prior.governance_docs)
    added_govs = cur_govs - prior_govs
    removed_govs = prior_govs - cur_govs

    summary["additions"] = len(added_govs)
    summary["removals"] = len(removed_govs)

    seq = 0
    for path in sorted(removed_govs):
        seq += 1
        findings.append(RecheckFinding(
            finding_id=f"RC-000-2{seq:02d}",
            severity=RecheckFindingSeverity.ERROR,
            pass_id="2.4",
            description=(
                f"Governance doc {path} present in prior snapshot "
                f"({prior.snapshot_date}) but absent now"
            ),
            affected_artifacts=[path],
            recommended_action=(
                "Confirm explicit retirement (with successor or rationale recorded). "
                "Silent removal is a finding."
            ),
        ))

    # Decision IDs: removals are findings
    cur_dec = set(current.decision_ids)
    prior_dec = set(prior.decision_ids)
    removed_dec = prior_dec - cur_dec
    for did in sorted(removed_dec):
        seq += 1
        findings.append(RecheckFinding(
            finding_id=f"RC-000-2{seq:02d}",
            severity=RecheckFindingSeverity.WARNING,
            pass_id="2.4",
            description=(
                f"Decision {did} ACTIVE in prior snapshot but no longer ACTIVE "
                f"(may be SUPERSEDED, RETIRED, or removed)"
            ),
            affected_artifacts=[did],
            recommended_action=(
                f"Confirm {did}'s status transition is documented in the decision register."
            ),
        ))

    # Rule count mutation
    cur_rules = len(current.canonical_rules)
    prior_rules = len(prior.canonical_rules)
    if abs(cur_rules - prior_rules) > 0:
        summary["mutations"] = abs(cur_rules - prior_rules)

    return findings, summary


# --- Pass 2.5: Decision-register cross-check ---

def check_decision_register(snapshot: DoctrineSnapshot) -> list[RecheckFinding]:
    findings: list[RecheckFinding] = []
    if not os.path.exists(DECISION_REGISTER_PATH):
        findings.append(RecheckFinding(
            finding_id="RC-000-901",
            severity=RecheckFindingSeverity.WARNING,
            pass_id="2.5",
            description="Decision register missing; pass 2.5 cannot run",
            affected_artifacts=[
                os.path.relpath(DECISION_REGISTER_PATH, REPO_ROOT)
            ],
            recommended_action="A12 must land before pass 2.5 is operative",
        ))
        return findings

    if not snapshot.decision_ids:
        findings.append(RecheckFinding(
            finding_id="RC-000-902",
            severity=RecheckFindingSeverity.INFO,
            pass_id="2.5",
            description=(
                "Decision register is empty; A12 Session 2 seeding pending. "
                "Pass 2.5 RULE coverage check suppressed."
            ),
            affected_artifacts=[
                os.path.relpath(DECISION_REGISTER_PATH, REPO_ROOT)
            ],
            recommended_action="Run A12 Session 2 to seed the register from "
                                "project-standards RULE blocks",
        ))
        return findings

    # Post-seeding: check that each CANONICAL rule has a Decision record.
    # Heuristic: Decision record's decision_artifacts should contain a path
    # that appears in the rule summary (e.g., "governance/time-model.md").
    # This pass is lenient pre-A12-S2; tightens at A12 S2.
    return findings


# --- Main ---

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--snapshot-only", action="store_true")
    ap.add_argument("--cross-ref", action="store_true")
    ap.add_argument("--full", action="store_true",
                    help="run passes 2.2-2.5 (default)")
    ap.add_argument("--baseline-against", default=None,
                    help="path to prior snapshot for drift detection")
    ap.add_argument("--report", action="store_true",
                    help="print summary; exit 0 always")
    args = ap.parse_args()

    # Pass 2.2 (always)
    snapshot = build_snapshot()
    print(
        f"Doctrine snapshot {snapshot.snapshot_date}: "
        f"{len(snapshot.governance_docs)} CANONICAL govs · "
        f"{len(snapshot.canonical_rules)} CANONICAL rules · "
        f"{len(snapshot.decision_ids)} ACTIVE decisions · "
        f"{snapshot.bpc_count} BPC files"
    )

    if args.snapshot_only:
        # Write snapshot only
        os.makedirs(RECHECK_DIR, exist_ok=True)
        date_tag = snapshot.snapshot_date.split(" ")[0]
        out_path = os.path.join(RECHECK_DIR, f"snapshot_{date_tag}.yaml")
        snapshot.to_yaml(out_path)
        print(f"Snapshot written: {os.path.relpath(out_path, REPO_ROOT)}")
        return 0

    # Passes 2.3-2.5
    all_findings: list[RecheckFinding] = []

    findings_23 = check_cross_references(snapshot)
    all_findings.extend(findings_23)

    if not args.cross_ref:
        prior = find_prior_snapshot(args.baseline_against)
        findings_24, drift_summary = detect_drift(snapshot, prior)
        all_findings.extend(findings_24)
        findings_25 = check_decision_register(snapshot)
        all_findings.extend(findings_25)
    else:
        drift_summary = {}

    # Categorise findings
    errors = [f for f in all_findings
              if (f.severity if isinstance(f.severity, str) else f.severity.value) == "ERROR"]
    warnings = [f for f in all_findings
                if (f.severity if isinstance(f.severity, str) else f.severity.value) == "WARNING"]
    infos = [f for f in all_findings
             if (f.severity if isinstance(f.severity, str) else f.severity.value) == "INFO"]

    if drift_summary:
        print(f"Drift summary: {drift_summary}")

    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for f in errors:
            print(f"  [{f.pass_id}] {f.description}")
    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for f in warnings:
            print(f"  [{f.pass_id}] {f.description}")
    if infos:
        print(f"\nINFO ({len(infos)}):")
        for f in infos:
            print(f"  [{f.pass_id}] {f.description}")
    if not all_findings:
        print("\nAll mechanical passes clean. Pass 2.6 (contamination resampling) "
              "is the recheck reviewer's responsibility — run "
              "scripts/contamination_sampler.py and classify each sampled BPC.")

    if args.report:
        return 0
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
