#!/usr/bin/env python3
"""
skills/evidence_auditor_validate.py — Output validator for evidence-auditor hybrid skill.

Validates that evidence-auditor output conforms to the expected schema:
- Every claim has required fields (claim_id, section, claim_text, evidence_stratum)
- Evidence strata are valid enum values
- Markers (●/○) are present when in marker verification mode
- OFS/PAIN expert consensus disclosure checked

This is the proof-of-concept for the CO-0008 hybrid skill pattern:
  1. Claude reads evidence-auditor_SKILL.md for judgment guidance
  2. Claude produces YAML output
  3. Claude calls this validator: python3 skills/evidence_auditor_validate.py --check output.yaml
  4. Validator reports pass/fail with field-level errors
  5. Claude fixes errors before committing

Usage:
    python3 skills/evidence_auditor_validate.py --check output.yaml
    python3 skills/evidence_auditor_validate.py --check output.yaml --marker-mode
"""

import argparse
import os
import sys
from typing import Optional

import yaml

# Allow importing schemas from repo root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydantic import BaseModel, ConfigDict, field_validator


# --- Output schema for evidence-auditor ---

VALID_STRATA = {"STRONG", "MODERATE", "EMERGING", "ABSENT"}
VALID_FLAGS = {
    "CONFIRMED_STRATUM",
    "OVERCLAIMED",
    "UNDERCLAIMED",
    "UNSTATED",
    "UNCERTAIN_REVIEW",
    "MARKER-STRATUM-MISMATCH",
    "UNSUPPORTED-MARKER",
    "EVIDENCE-AVAILABLE",
    "UNDISCLOSED-CONSENSUS",
}
VALID_MARKERS = {"●", "○", None, ""}


class EvidenceAuditClaim(BaseModel):
    """Single claim in an evidence audit output."""

    model_config = ConfigDict(extra="forbid")

    claim_id: str
    section: str
    claim_text: str
    source: Optional[str] = None
    claim_type: Optional[str] = None
    stated_stratum: Optional[str] = None
    proposed_stratum: str
    flag: str
    evidence_marker: Optional[str] = None
    population: Optional[str] = None
    action: Optional[str] = None

    @field_validator("proposed_stratum")
    @classmethod
    def valid_proposed_stratum(cls, v: str) -> str:
        if v not in VALID_STRATA:
            raise ValueError(
                f"Invalid proposed_stratum: '{v}'. Must be one of {VALID_STRATA}"
            )
        return v

    @field_validator("stated_stratum")
    @classmethod
    def valid_stated_stratum(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_STRATA:
            raise ValueError(
                f"Invalid stated_stratum: '{v}'. Must be one of {VALID_STRATA}"
            )
        return v

    @field_validator("flag")
    @classmethod
    def valid_flag(cls, v: str) -> str:
        if v not in VALID_FLAGS:
            raise ValueError(
                f"Invalid flag: '{v}'. Must be one of {VALID_FLAGS}"
            )
        return v

    @field_validator("evidence_marker")
    @classmethod
    def valid_marker(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_MARKERS:
            raise ValueError(
                f"Invalid evidence_marker: '{v}'. Must be ● or ○"
            )
        return v


class EvidenceAuditOutput(BaseModel):
    """Complete output of an evidence-auditor run."""

    model_config = ConfigDict(extra="forbid")

    audit_id: str
    input_section: str
    marker_mode: bool = False
    claims: list[EvidenceAuditClaim]
    summary: dict  # Free-form summary statistics


def validate_audit_output(path: str, marker_mode: bool = False) -> dict:
    """Validate evidence-auditor output file.

    Returns:
        {
            "status": "pass" | "fail",
            "errors": [{"field": str, "message": str, "severity": str}],
            "warnings": [...],
            "stats": {"total_claims": int, "valid": int, "invalid": int}
        }
    """
    errors = []
    warnings = []

    # Load YAML
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return {
            "status": "fail",
            "errors": [{"field": "file", "message": str(e), "severity": "FATAL"}],
            "warnings": [],
            "stats": {"total_claims": 0, "valid": 0, "invalid": 0},
        }

    if data is None:
        return {
            "status": "fail",
            "errors": [{"field": "file", "message": "Empty file", "severity": "FATAL"}],
            "warnings": [],
            "stats": {"total_claims": 0, "valid": 0, "invalid": 0},
        }

    # Validate top-level structure
    try:
        output = EvidenceAuditOutput.model_validate(data)
    except Exception as e:
        return {
            "status": "fail",
            "errors": [{"field": "root", "message": str(e), "severity": "ERROR"}],
            "warnings": [],
            "stats": {"total_claims": 0, "valid": 0, "invalid": 0},
        }

    valid_claims = 0
    invalid_claims = 0

    for i, claim in enumerate(output.claims):
        # Marker mode checks
        if marker_mode and not claim.evidence_marker:
            warnings.append({
                "field": f"claims[{i}].evidence_marker",
                "message": f"Claim {claim.claim_id}: marker_mode is on but no marker",
                "severity": "WARN",
            })

        # OFS/PAIN expert consensus disclosure check
        if claim.population in ("OFS", "PAIN", "OFS/ME", "OFS/POTS", "OFS/MCAS"):
            if claim.proposed_stratum in ("EMERGING", "ABSENT"):
                if claim.flag != "UNDISCLOSED-CONSENSUS" and not claim.action:
                    warnings.append({
                        "field": f"claims[{i}]",
                        "message": (
                            f"Claim {claim.claim_id}: {claim.population} at "
                            f"{claim.proposed_stratum} — check expert consensus disclosure"
                        ),
                        "severity": "WARN",
                    })

        valid_claims += 1

    status = "pass" if not errors else "fail"

    return {
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "total_claims": len(output.claims),
            "valid": valid_claims,
            "invalid": invalid_claims,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate evidence-auditor output against schema"
    )
    parser.add_argument(
        "--check",
        required=True,
        help="Path to evidence-auditor output YAML",
    )
    parser.add_argument(
        "--marker-mode",
        action="store_true",
        help="Enable marker verification mode checks",
    )
    args = parser.parse_args()

    result = validate_audit_output(args.check, args.marker_mode)

    # Report
    print(f"Status: {result['status']}")
    print(f"Claims: {result['stats']['total_claims']} total, "
          f"{result['stats']['valid']} valid, "
          f"{result['stats']['invalid']} invalid")

    if result["errors"]:
        print(f"\nErrors ({len(result['errors'])}):")
        for e in result["errors"]:
            print(f"  [{e['severity']}] {e['field']}: {e['message']}")

    if result["warnings"]:
        print(f"\nWarnings ({len(result['warnings'])}):")
        for w in result["warnings"]:
            print(f"  [{w['severity']}] {w['field']}: {w['message']}")

    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
