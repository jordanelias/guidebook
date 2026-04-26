#!/usr/bin/env python3
"""
scripts/convert/convert_sources.py — Convert global-reference-registry.json
to validated YAML files under data/sources/.

Normalizes tier + evidence_type per T-03 decision:
- "1" → tier=1, evidence_type=clinical
- "Co-1" → tier=1, evidence_type=co1
- "Co-2" → tier=3, evidence_type=co2 (with CPG marker per project-standards)
- "3" → tier=3, evidence_type=sr_meta (default for Tier 3)
- "4" → tier=4, evidence_type=standard_eb
- "5" → tier=5, evidence_type=national_fw
- "6" → tier=6, evidence_type=code

Usage:
    python3 scripts/convert/convert_sources.py [--input PATH] [--output-dir PATH] [--dry-run]
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from schemas.evidence_source import EvidenceSource
from schemas.enums import EvidenceType


# T-03 tier string → (tier_int, evidence_type) mapping
TIER_MAP = {
    "1": (1, EvidenceType.CLINICAL),
    "Co-1": (1, EvidenceType.CO1),
    "co-1": (1, EvidenceType.CO1),
    "Co-2": (3, EvidenceType.CO2),
    "co-2": (3, EvidenceType.CO2),
    "2": (2, EvidenceType.GREY),  # Tier 2 = NGO/DPO → closest is grey/advocacy
    "3": (3, EvidenceType.SR_META),
    "4": (4, EvidenceType.STANDARD_EB),
    "5": (5, EvidenceType.NATIONAL_FW),
    "6": (6, EvidenceType.CODE),
}


def parse_tier_and_type(raw_tier: str) -> tuple:
    """Parse legacy tier string into (tier_int, EvidenceType) per T-03.

    Handles all observed formats in global-reference-registry:
    - "1", "2", ..., "6" (bare digit)
    - "Tier 1", "Tier 5" (word prefix)
    - "Co-1", "Co-2" (evidence types)
    - "Co-1/3", "Co-1/5" (co-1 with tier ceiling)
    - "5/6", "3/4", "2/5" (tier range with slash)
    - "6 commentary" (tier with trailing text)
    - "—" or empty (no tier)

    Returns (Optional[int], EvidenceType).
    """
    import re

    if not raw_tier or raw_tier.strip() in ("", "—", "–", "-"):
        return (None, EvidenceType.UNKNOWN)

    raw = raw_tier.strip()

    # Direct lookup first
    if raw in TIER_MAP:
        return TIER_MAP[raw]

    # "Tier N" format — strip prefix
    m = re.match(r"^Tier\s+(\d)", raw, re.IGNORECASE)
    if m:
        t = int(m.group(1))
        if 1 <= t <= 6:
            return TIER_MAP.get(str(t), (t, EvidenceType.UNKNOWN))

    # "Co-1/N" format — co-1 evidence type with tier ceiling
    m = re.match(r"^Co-?1/(\d)", raw, re.IGNORECASE)
    if m:
        ceiling = int(m.group(1))
        return (1, EvidenceType.CO1)  # floor=1 (co-primary), type=co1

    # "Co-2/N" or "Co-2" with suffix
    m = re.match(r"^Co-?2", raw, re.IGNORECASE)
    if m:
        return (3, EvidenceType.CO2)

    # "N/M" slash range — take strongest (lowest)
    m = re.match(r"^(\d)\s*/\s*(\d)", raw)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        t = min(a, b)
        return TIER_MAP.get(str(t), (t, EvidenceType.UNKNOWN))

    # "N commentary" — digit with trailing text
    m = re.match(r"^(\d)\s+\w", raw)
    if m:
        t = int(m.group(1))
        if 1 <= t <= 6:
            return TIER_MAP.get(str(t), (t, EvidenceType.UNKNOWN))

    # Try bare numeric
    try:
        t = int(raw)
        if 1 <= t <= 6:
            return TIER_MAP.get(str(t), (t, EvidenceType.UNKNOWN))
    except ValueError:
        pass

    # Compound with dash "1-3" → strongest
    if "-" in raw:
        parts = raw.split("-")
        nums = [int(p.strip()) for p in parts if p.strip().isdigit()]
        if nums:
            t = min(nums)
            return TIER_MAP.get(str(t), (t, EvidenceType.UNKNOWN))

    print(f"  WARNING: unparseable tier: '{raw}'", file=sys.stderr)
    return (None, EvidenceType.UNKNOWN)


def convert_record(rec: dict, warnings: list) -> dict:
    """Convert one global-registry JSON record to schema-conformant dict."""

    ref_id = rec.get("ref_id", "")

    # Parse tier + evidence_type per T-03
    tier_int, evidence_type = parse_tier_and_type(rec.get("tier", ""))

    # Normalize used_in_slugs
    used_in_slugs = rec.get("used_in_slugs", [])
    if isinstance(used_in_slugs, str):
        used_in_slugs = [s.strip() for s in used_in_slugs.split(",") if s.strip()]

    # Normalize local_ref_ids
    local_ref_ids = rec.get("local_ref_ids", [])
    if isinstance(local_ref_ids, str):
        local_ref_ids = [s.strip() for s in local_ref_ids.split(",") if s.strip()]

    # Metadata quality
    mq = rec.get("metadata_quality", "")
    if mq and mq.strip():
        mq = mq.strip()
    else:
        mq = None

    return {
        "ref_id": ref_id,
        "authors": rec.get("authors", "(unknown)"),
        "year": rec.get("year") or None,
        "title": rec.get("title", "(untitled)"),
        "doi": rec.get("doi") or None,
        "pmid": str(rec["pmid"]) if rec.get("pmid") else None,
        "tier": tier_int,
        "evidence_type": evidence_type.value,
        "jurisdiction": rec.get("jurisdiction") or None,
        "used_in_slugs": used_in_slugs,
        "local_ref_ids": local_ref_ids,
        "metadata_quality": mq,
        "notes": rec.get("notes") or None,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Convert global-reference-registry.json to validated YAML"
    )
    parser.add_argument(
        "--input",
        default="references/global-reference-registry.json",
        help="Path to global registry JSON",
    )
    parser.add_argument(
        "--output-dir",
        default="data/sources",
        help="Output directory for YAML files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate without writing files",
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        records = json.load(f)

    if isinstance(records, dict):
        records = records.get("sources", records.get("references", []))

    print(f"Loaded {len(records)} records from {args.input}")

    os.makedirs(args.output_dir, exist_ok=True)
    passed = 0
    failed = 0
    all_warnings = []

    for rec in records:
        rid = rec.get("ref_id", "UNKNOWN")
        warnings = []
        try:
            converted = convert_record(rec, warnings)
            source = EvidenceSource.model_validate(converted)
            if not args.dry_run:
                # Use ref_id as filename: ref-00001.yaml
                fname = rid.lower().replace("-", "-") + ".yaml"
                out_path = os.path.join(args.output_dir, fname)
                source.to_yaml(out_path)
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  FAIL {rid}: {e}", file=sys.stderr)

        all_warnings.extend(warnings)

    print(f"\nResults: {passed} passed, {failed} failed, {len(all_warnings)} warnings")
    for w in all_warnings:
        print(f"  WARN: {w}")

    if failed > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
