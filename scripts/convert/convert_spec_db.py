#!/usr/bin/env python3
"""
scripts/convert/convert_spec_db.py — Convert specification-database.json
to validated YAML files under data/specifications/.

Reads the legacy JSON format and normalizes:
- Evidence tier compound strings → EvidenceTierRange objects
- Recommendation strength free-text → RecommendationStrength enum + qualifier
- Item code sentinels → assignment_status enum + nullable item_code
- Parameter sentinels → flagged for manual review

Usage:
    python3 scripts/convert/convert_spec_db.py [--input PATH] [--output-dir PATH] [--dry-run]

Output: one YAML file per specification record in data/specifications/.
"""

import argparse
import json
import os
import re
import sys

# Allow importing schemas from repo root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from schemas.specification import Specification
from schemas.enums import (
    ItemAssignmentStatus,
    RecommendationStrength,
    ValueType,
)


def parse_evidence_tier(raw: str) -> dict:
    """Parse compound evidence tier string into structured form.

    Examples:
        "Tier 4-5" → {"floor": 4, "ceiling": 5, "evidence_types_present": []}
        "Co-1/Tier 3" → {"floor": 1, "ceiling": 3, "evidence_types_present": ["co1"]}
        "Tier 1-3" → {"floor": 1, "ceiling": 3, "evidence_types_present": []}
        "Tier 3" → {"floor": 3, "ceiling": 3, "evidence_types_present": []}
    """
    if not raw or raw.strip() == "":
        return None

    evidence_types = []
    co1 = "Co-1" in raw or "co-1" in raw or "Co1" in raw
    if co1:
        evidence_types.append("co1")

    # Remove Co-1/ prefix for tier parsing
    tier_part = re.sub(r"Co-?1/?", "", raw).strip()

    # Match "Tier N-M" or "Tier N"
    m = re.match(r"Tier\s*(\d)\s*-?\s*(\d)?", tier_part)
    if m:
        floor = int(m.group(1))
        ceiling = int(m.group(2)) if m.group(2) else floor
        # If Co-1 present, floor extends to 1 (co-primary)
        if co1 and floor > 1:
            floor = 1
        return {"floor": floor, "ceiling": ceiling, "evidence_types_present": evidence_types}

    # Fallback: try just a number
    m = re.match(r"(\d)", tier_part)
    if m:
        t = int(m.group(1))
        floor = 1 if co1 else t
        return {"floor": floor, "ceiling": t, "evidence_types_present": evidence_types}

    print(f"  WARNING: unparseable evidence_tier: '{raw}'", file=sys.stderr)
    return None


def parse_recommendation_strength(raw: str) -> tuple:
    """Parse recommendation strength into (enum, qualifier).

    Returns:
        (RecommendationStrength, Optional[str])
    """
    if not raw or "UNSET" in raw:
        return (RecommendationStrength.UNSET, None)

    low = raw.lower()
    qualifier = None

    if "strong at tier 0" in low:
        # Extract parenthetical qualifier if present
        m = re.search(r"\((.+)\)", raw)
        if m:
            qualifier = m.group(1)
        return (RecommendationStrength.STRONG_TIER_0, qualifier)

    if "conditional at tier 1" in low:
        m = re.search(r"\((.+)\)", raw)
        if m:
            qualifier = m.group(1)
        return (RecommendationStrength.CONDITIONAL_TIER_1, qualifier)

    if "conditional" in low:
        return (RecommendationStrength.CONDITIONAL, None)

    # Unmapped → UNSET with raw as qualifier
    return (RecommendationStrength.UNSET, raw)


def normalize_item_code(raw: str) -> tuple:
    """Normalize item code, handling sentinels.

    Returns:
        (item_code: Optional[str], assignment_status: ItemAssignmentStatus)
    """
    if not raw or raw in ("[UNASSIGNED]", "", None):
        return (None, ItemAssignmentStatus.UNASSIGNED)
    if raw == "[CROSS-CUTTING]":
        return (None, ItemAssignmentStatus.CROSS_CUTTING)
    # Validate format
    if re.match(r"^[A-K]-\d{2}$", raw):
        return (raw, ItemAssignmentStatus.ASSIGNED)
    # Non-standard but not sentinel — keep as-is, flag
    print(f"  WARNING: non-standard item_code: '{raw}'", file=sys.stderr)
    return (None, ItemAssignmentStatus.UNASSIGNED)


def convert_record(rec: dict, warnings: list) -> dict:
    """Convert one legacy JSON record to schema-conformant dict."""

    # Evidence tier
    evidence_tier = parse_evidence_tier(rec.get("evidence_tier", ""))

    # Recommendation strength
    rec_strength, rec_qualifier = parse_recommendation_strength(
        rec.get("recommendation_strength", "")
    )

    # Item code
    item_code, assignment_status = normalize_item_code(rec.get("item_code"))

    # Value type
    vtype = rec.get("value_type", "fixed")
    if vtype not in ("fixed", "range"):
        # Check if qualitative (all values null)
        if all(rec.get(f) is None for f in ("value_min", "value_max", "value_median")):
            vtype = "qualitative"
        else:
            vtype = "fixed"
            warnings.append(f"{rec.get('spec_id')}: unknown value_type '{rec.get('value_type')}' → fixed")

    # Parameter sentinel check
    param = rec.get("parameter", "")
    if param.lower() in ("unclassified", "unknown", "tbd"):
        warnings.append(
            f"{rec.get('spec_id')}: sentinel parameter '{param}' — needs manual assignment"
        )
        param = f"NEEDS_CLASSIFICATION_{rec.get('spec_id', 'UNKNOWN')}"

    # Conditions
    conditions = []
    raw_conditions = rec.get("conditions") or []
    for c in raw_conditions:
        if isinstance(c, dict):
            conditions.append({
                "condition": c.get("condition", ""),
                "value_min": c.get("value_min"),
                "value_max": c.get("value_max"),
            })

    return {
        "spec_id": rec.get("spec_id", "SPEC-0000"),
        "slug": rec.get("slug", rec.get("bpc_source_slug", "")),
        "bpc_source_slug": rec.get("bpc_source_slug", ""),
        "item_code": item_code,
        "assignment_status": assignment_status,
        "parameter": param,
        "value_type": vtype,
        "value_min": rec.get("value_min"),
        "value_max": rec.get("value_max"),
        "value_median": rec.get("value_median"),
        "unit": rec.get("unit") or None,
        "evidence_tier": evidence_tier,
        "opus_synthesized": bool(rec.get("opus_synthesized", False)),
        "recommendation_strength": rec_strength,
        "recommendation_qualifier": rec_qualifier,
        "populations": rec.get("populations", []),
        "jurisdictions_supporting": rec.get("jurisdictions_supporting", []),
        "jurisdictions_divergent": rec.get("jurisdictions_divergent", []),
        "divergence_note": rec.get("divergence_note") or None,
        "tier_2_note": rec.get("tier_2_note") or None,
        "conditions": conditions,
        "percentile_basis": rec.get("percentile_basis"),
        "notes": rec.get("notes") or None,
        "context_note": rec.get("context_note") or None,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Convert specification-database.json to validated YAML"
    )
    parser.add_argument(
        "--input",
        default="references/specification-database.json",
        help="Path to legacy spec-db JSON",
    )
    parser.add_argument(
        "--output-dir",
        default="data/specifications",
        help="Output directory for YAML files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate without writing files",
    )
    args = parser.parse_args()

    # Load
    with open(args.input, "r", encoding="utf-8") as f:
        raw = json.load(f)

    specs = raw.get("specifications", raw) if isinstance(raw, dict) else raw
    print(f"Loaded {len(specs)} records from {args.input}")

    # Convert and validate
    os.makedirs(args.output_dir, exist_ok=True)
    passed = 0
    failed = 0
    all_warnings = []

    for rec in specs:
        sid = rec.get("spec_id", "UNKNOWN")
        warnings = []
        try:
            converted = convert_record(rec, warnings)
            spec = Specification.model_validate(converted)
            if not args.dry_run:
                out_path = os.path.join(args.output_dir, f"{sid.lower()}.yaml")
                spec.to_yaml(out_path)
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  FAIL {sid}: {e}", file=sys.stderr)

        all_warnings.extend(warnings)

    # Report
    print(f"\nResults: {passed} passed, {failed} failed, {len(all_warnings)} warnings")
    for w in all_warnings:
        print(f"  WARN: {w}")

    if failed > 0:
        print(f"\n{failed} records failed validation", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
