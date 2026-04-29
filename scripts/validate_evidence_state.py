#!/usr/bin/env python3
"""
scripts/validate_evidence_state.py — Validate evidence state records.

Per governance/evidence-methodology.md (A6):
- pending cells must reference gap_register.md
- provisional cells must carry confidence flag with named dimensions
- not_applicable cells must carry rationale
- stated cells must cite ≥1 source at Tier 1–3 OR Co-1 OR Co-2
- Verification-status downgrade logic per §2.8
- Convergence assessment completeness for multi-axis cells

Also validates EvidenceSource records for A5 Co-1 field requirements.

Usage:
    python3 scripts/validate_evidence_state.py                  # validate all
    python3 scripts/validate_evidence_state.py --quick           # sample 5
    python3 scripts/validate_evidence_state.py --sources-only    # Co-1 fields only
    python3 scripts/validate_evidence_state.py data/evidence-states/es-0001.yaml

Exit codes:
    0 = all valid
    1 = validation failures found
    2 = configuration error
"""

import argparse
import glob
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.evidence_state import EvidenceStateRecord
from schemas.evidence_source import EvidenceSource
from schemas.enums import EvidenceType, VerificationStatus


def validate_file(path: str, model_class) -> list:
    """Validate a single YAML file. Returns list of error strings."""
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"]

    if data is None:
        return ["File is empty"]

    try:
        model_class.model_validate(data)
    except Exception as e:
        errors.append(str(e))

    return errors


def validate_source_co1_fields(path: str) -> list:
    """Additional Co-1 field validation beyond Pydantic schema.

    Checks A5 §6.3 verification-status rules for Co-1 sources.
    """
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception:
        return []  # Let the main validator catch parse errors

    if not data:
        return []

    et = data.get("evidence_type", "")
    if et != "co1":
        return []

    # Co-1 source: check verification status
    vs = data.get("verification_status")
    if vs in ("UNVERIFIED-CLOSED", "CLOSED-DELETED"):
        errors.append(
            f"Co-1 source {data.get('ref_id', '?')} has "
            f"verification_status={vs} — cells citing this source "
            f"as sole Co-1 evidence must downgrade to pending (A6 §2.8)"
        )

    # Co-1 source: tier must be 1
    tier = data.get("tier")
    if tier is not None and tier != 1:
        errors.append(
            f"Co-1 source {data.get('ref_id', '?')} has tier={tier} "
            f"but Co-1 must be tier=1 (co-primary per T-03)"
        )

    return errors


def validate_evidence_state_cross_refs(path: str, gap_ids: set) -> list:
    """Check cross-references for evidence state records."""
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception:
        return []

    if not data:
        return []

    state = data.get("state", "")
    gap_id = data.get("gap_register_id")

    if state == "pending" and gap_id:
        if gap_ids and gap_id not in gap_ids:
            errors.append(
                f"gap_register_id '{gap_id}' not found in gap_register.md"
            )

    return errors


def load_gap_ids(repo_root: str) -> set:
    """Extract GAP-NNN IDs from gap_register.md."""
    import re

    gap_path = os.path.join(repo_root, "gap_register.md")
    if not os.path.exists(gap_path):
        return set()

    ids = set()
    with open(gap_path, "r", encoding="utf-8") as f:
        for line in f:
            for m in re.finditer(r"GAP-\d{3,4}", line):
                ids.add(m.group())
    return ids


def main():
    parser = argparse.ArgumentParser(
        description="Validate evidence state and source records"
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Specific files to validate",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Sample 5 files from each directory",
    )
    parser.add_argument(
        "--sources-only",
        action="store_true",
        help="Only validate EvidenceSource Co-1 fields",
    )
    parser.add_argument(
        "--states-only",
        action="store_true",
        help="Only validate EvidenceStateRecord files",
    )
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gap_ids = load_gap_ids(repo_root)

    total_errors = 0
    total_files = 0
    total_warnings = 0

    # Determine what to validate
    validate_sources = not args.states_only
    validate_states = not args.sources_only

    if args.files:
        # Validate specific files
        for path in args.files:
            if not os.path.exists(path):
                print(f"  NOT FOUND: {path}", file=sys.stderr)
                total_errors += 1
                continue

            total_files += 1
            # Detect type by directory or content
            if "sources" in path:
                errors = validate_file(path, EvidenceSource)
                errors.extend(validate_source_co1_fields(path))
            else:
                errors = validate_file(path, EvidenceStateRecord)
                errors.extend(
                    validate_evidence_state_cross_refs(path, gap_ids)
                )

            if errors:
                total_errors += len(errors)
                print(f"FAIL {path}:")
                for e in errors:
                    print(f"  {e}")
    else:
        # Scan data directories
        source_dir = os.path.join(repo_root, "data", "sources")
        state_dir = os.path.join(repo_root, "data", "evidence-states")

        if validate_sources and os.path.isdir(source_dir):
            files = sorted(glob.glob(os.path.join(source_dir, "*.yaml")))
            if args.quick:
                import random
                files = random.sample(files, min(5, len(files)))

            for path in files:
                total_files += 1
                errors = validate_file(path, EvidenceSource)
                errors.extend(validate_source_co1_fields(path))
                if errors:
                    total_errors += len(errors)
                    print(f"FAIL {os.path.basename(path)}:")
                    for e in errors:
                        print(f"  {e}")

        if validate_states and os.path.isdir(state_dir):
            files = sorted(glob.glob(os.path.join(state_dir, "*.yaml")))
            if args.quick:
                import random
                files = random.sample(files, min(5, len(files)))

            for path in files:
                total_files += 1
                errors = validate_file(path, EvidenceStateRecord)
                errors.extend(
                    validate_evidence_state_cross_refs(path, gap_ids)
                )
                if errors:
                    total_errors += len(errors)
                    print(f"FAIL {os.path.basename(path)}:")
                    for e in errors:
                        print(f"  {e}")

    # Summary
    if total_files == 0:
        print(
            "No data files found. "
            "data/sources/ and data/evidence-states/ directories do not exist yet.",
            file=sys.stderr,
        )
        return 0  # Not an error — data hasn't been materialized

    status = "PASS" if total_errors == 0 else "FAIL"
    print(
        f"\n{status}: {total_files} files checked, "
        f"{total_errors} errors, {total_warnings} warnings",
        file=sys.stderr,
    )
    return 1 if total_errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
