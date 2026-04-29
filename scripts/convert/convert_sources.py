#!/usr/bin/env python3
"""
scripts/convert/convert_sources.py — Convert source registries to validated YAML.

Handles two input formats:
1. global-reference-registry.json → EvidenceSource YAML (existing)
2. co1-verified-sources.json → EvidenceSource YAML with Co-1 fields (A5/A6)

Normalizes tier + evidence_type per T-03 decision:
- "1" → tier=1, evidence_type=clinical
- "Co-1" → tier=1, evidence_type=co1 (+ A5 Co-1 fields)
- "Co-2" → tier=2, evidence_type=co2 (per T-03; corrected from prior tier=3)
- "3" → tier=3, evidence_type=sr_meta
- "4" → tier=4, evidence_type=standard_eb
- "5" → tier=5, evidence_type=national_fw
- "6" → tier=6, evidence_type=code

A5 Co-1 field handling:
- co1_provenance: "published_corpus" for all pre-launch sources
- co1_source_type: inferred from source metadata or defaulted
- synthesis_attribution_required: default False; flagged True for substantial sources
- verification_status: mapped from source "status" field

Usage:
    python3 scripts/convert/convert_sources.py [--input PATH] [--output-dir PATH] [--dry-run]
    python3 scripts/convert/convert_sources.py --co1 [--input PATH] [--output-dir PATH]
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from schemas.evidence_source import EvidenceSource
from schemas.enums import (
    Co1Provenance,
    Co1SourceType,
    EvidenceType,
    VerificationStatus,
)


# T-03 tier string → (tier_int, evidence_type) mapping
# Co-2 corrected to tier=2 per T-03 (was incorrectly tier=3 pre-A6)
TIER_MAP = {
    "1": (1, EvidenceType.CLINICAL),
    "Co-1": (1, EvidenceType.CO1),
    "co-1": (1, EvidenceType.CO1),
    "Co-2": (2, EvidenceType.CO2),
    "co-2": (2, EvidenceType.CO2),
    "2": (2, EvidenceType.GREY),  # Tier 2 = NGO/DPO → closest is grey/advocacy
    "3": (3, EvidenceType.SR_META),
    "4": (4, EvidenceType.STANDARD_EB),
    "5": (5, EvidenceType.NATIONAL_FW),
    "6": (6, EvidenceType.CODE),
}

# Verification status mapping from co1-verified-sources.json
VERIFICATION_MAP = {
    "VERIFIED": VerificationStatus.VERIFIED,
    "VERIFIED-WITH-CORRECTION": VerificationStatus.VERIFIED_WITH_CORRECTION,
    "UNVERIFIED-1": VerificationStatus.UNVERIFIED_1,
    "UNVERIFIED-CLOSED": VerificationStatus.UNVERIFIED_CLOSED,
    "CLOSED-DELETED": VerificationStatus.CLOSED_DELETED,
}

# Co-1 source type inference from note/context
CO1_TYPE_KEYWORDS = {
    "peer-reviewed": Co1SourceType.PEER_REVIEWED_LITERATURE,
    "journal": Co1SourceType.PEER_REVIEWED_LITERATURE,
    "DPO": Co1SourceType.DPO_RESEARCH,
    "advocacy": Co1SourceType.ADVOCACY_POSITION,
    "visitability": Co1SourceType.ADVOCACY_POSITION,
    "narrative": Co1SourceType.ACADEMIC_NARRATIVE,
    "ethnography": Co1SourceType.ACADEMIC_NARRATIVE,
    "audit tool": Co1SourceType.VALIDATED_TOOL,
    "assessment": Co1SourceType.VALIDATED_TOOL,
    "ESKEH": Co1SourceType.VALIDATED_TOOL,
    "EADDAT": Co1SourceType.VALIDATED_TOOL,
    "ASPECTSS": Co1SourceType.VALIDATED_TOOL,
}


def parse_tier_and_type(raw_tier: str) -> tuple:
    """Parse legacy tier string into (tier_int, EvidenceType) per T-03.

    Handles all observed formats in global-reference-registry and
    co1-verified-sources.
    """
    if not raw_tier or raw_tier.strip() in ("", "—", "–", "-"):
        return (None, EvidenceType.UNKNOWN)

    raw = raw_tier.strip()

    # Direct lookup first
    if raw in TIER_MAP:
        return TIER_MAP[raw]

    # "Tier N" format
    m = re.match(r"^Tier\s+(\d)", raw, re.IGNORECASE)
    if m:
        t = int(m.group(1))
        if 1 <= t <= 6:
            return TIER_MAP.get(str(t), (t, EvidenceType.UNKNOWN))

    # "Co-1/N" format
    m = re.match(r"^Co-?1/(\d)", raw, re.IGNORECASE)
    if m:
        return (1, EvidenceType.CO1)

    # "Co-2" with any suffix
    m = re.match(r"^Co-?2", raw, re.IGNORECASE)
    if m:
        return (2, EvidenceType.CO2)

    # "N/M" slash range — take strongest
    m = re.match(r"^(\d)\s*/\s*(\d)", raw)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        t = min(a, b)
        return TIER_MAP.get(str(t), (t, EvidenceType.UNKNOWN))

    # "N commentary"
    m = re.match(r"^(\d)\s+\w", raw)
    if m:
        t = int(m.group(1))
        if 1 <= t <= 6:
            return TIER_MAP.get(str(t), (t, EvidenceType.UNKNOWN))

    # Bare numeric
    try:
        t = int(raw)
        if 1 <= t <= 6:
            return TIER_MAP.get(str(t), (t, EvidenceType.UNKNOWN))
    except ValueError:
        pass

    # Dash range "1-3"
    if "-" in raw:
        parts = raw.split("-")
        nums = [int(p.strip()) for p in parts if p.strip().isdigit()]
        if nums:
            t = min(nums)
            return TIER_MAP.get(str(t), (t, EvidenceType.UNKNOWN))

    print(f"  WARNING: unparseable tier: '{raw}'", file=sys.stderr)
    return (None, EvidenceType.UNKNOWN)


def infer_co1_source_type(rec: dict) -> Co1SourceType:
    """Infer Co-1 source type from record metadata."""
    # Check note, title, publisher for keyword matches
    searchable = " ".join([
        rec.get("note", ""),
        rec.get("title", ""),
        rec.get("publisher", ""),
        rec.get("journal", ""),
    ]).lower()

    for keyword, source_type in CO1_TYPE_KEYWORDS.items():
        if keyword.lower() in searchable:
            return source_type

    # Check if it has a journal → peer-reviewed
    if rec.get("journal"):
        return Co1SourceType.PEER_REVIEWED_LITERATURE

    # Check if it has a DOI → likely peer-reviewed
    if rec.get("doi"):
        return Co1SourceType.PEER_REVIEWED_LITERATURE

    # Check publisher for org patterns
    pub = (rec.get("publisher") or "").lower()
    if any(w in pub for w in ["university", "press", "academic"]):
        return Co1SourceType.ACADEMIC_NARRATIVE

    # Default to DPO research (most common for org-published Co-1)
    return Co1SourceType.DPO_RESEARCH


def map_verification_status(raw: str) -> VerificationStatus | None:
    """Map raw verification status string to enum."""
    if not raw:
        return None
    raw = raw.strip().upper()
    # Handle minor variations
    for key, val in VERIFICATION_MAP.items():
        if raw == key.upper():
            return val
    # Partial match
    if "VERIFIED" in raw and "UN" not in raw:
        if "CORRECTION" in raw:
            return VerificationStatus.VERIFIED_WITH_CORRECTION
        return VerificationStatus.VERIFIED
    if "CLOSED-DELETED" in raw or "CLOSED_DELETED" in raw:
        return VerificationStatus.CLOSED_DELETED
    if "UNVERIFIED-CLOSED" in raw:
        return VerificationStatus.UNVERIFIED_CLOSED
    if "UNVERIFIED" in raw:
        return VerificationStatus.UNVERIFIED_1
    return None


def convert_registry_record(rec: dict) -> dict:
    """Convert one global-registry JSON record to schema-conformant dict."""
    ref_id = rec.get("ref_id", "")
    tier_int, evidence_type = parse_tier_and_type(rec.get("tier", ""))

    used_in_slugs = rec.get("used_in_slugs", [])
    if isinstance(used_in_slugs, str):
        used_in_slugs = [s.strip() for s in used_in_slugs.split(",") if s.strip()]

    local_ref_ids = rec.get("local_ref_ids", [])
    if isinstance(local_ref_ids, str):
        local_ref_ids = [s.strip() for s in local_ref_ids.split(",") if s.strip()]

    mq = rec.get("metadata_quality", "")
    mq = mq.strip() if mq and mq.strip() else None

    result = {
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
        "verification_status": rec.get("verification_status") or None,
        "notes": rec.get("notes") or None,
    }

    # Add Co-1 fields if evidence_type is co1
    if evidence_type == EvidenceType.CO1:
        result["co1_provenance"] = Co1Provenance.PUBLISHED_CORPUS.value
        result["co1_source_type"] = infer_co1_source_type(rec).value
        result["synthesis_attribution_required"] = False

    return result


def convert_co1_record(rec: dict) -> dict:
    """Convert one co1-verified-sources.json record to schema-conformant dict."""
    ref_id = rec.get("ref_id", "")

    # Map verification status
    vs = map_verification_status(rec.get("status", ""))

    result = {
        "ref_id": ref_id,
        "authors": rec.get("authors", "(unknown)"),
        "year": rec.get("year") or None,
        "title": rec.get("title", "(untitled)"),
        "doi": rec.get("doi") or None,
        "pmid": str(rec["pmid"]) if rec.get("pmid") else None,
        "tier": 1,  # Co-1 is always tier 1
        "evidence_type": EvidenceType.CO1.value,
        "jurisdiction": rec.get("jurisdiction") or None,
        "used_in_slugs": [],
        "local_ref_ids": [],
        "metadata_quality": None,
        "verification_status": vs.value if vs else None,
        "notes": rec.get("note") or rec.get("notes") or None,
        # A5 Co-1 required fields
        "co1_provenance": Co1Provenance.PUBLISHED_CORPUS.value,
        "co1_source_type": infer_co1_source_type(rec).value,
        "synthesis_attribution_required": False,
    }

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Convert source registries to validated YAML"
    )
    parser.add_argument(
        "--input",
        default="references/global-reference-registry.json",
        help="Path to source JSON",
    )
    parser.add_argument(
        "--output-dir",
        default="data/sources",
        help="Output directory for YAML files",
    )
    parser.add_argument(
        "--co1",
        action="store_true",
        help="Process co1-verified-sources.json format",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate without writing files",
    )
    args = parser.parse_args()

    if args.co1 and args.input == "references/global-reference-registry.json":
        args.input = "references/co1-verified-sources.json"

    with open(args.input, "r", encoding="utf-8") as f:
        records = json.load(f)

    if isinstance(records, dict):
        records = records.get("sources", records.get("references", []))

    print(f"Loaded {len(records)} records from {args.input}")

    os.makedirs(args.output_dir, exist_ok=True)
    passed = 0
    failed = 0

    for rec in records:
        rid = rec.get("ref_id", "UNKNOWN")
        try:
            if args.co1:
                converted = convert_co1_record(rec)
            else:
                converted = convert_registry_record(rec)

            source = EvidenceSource.model_validate(converted)
            if not args.dry_run:
                fname = rid.lower().replace("-", "-") + ".yaml"
                out_path = os.path.join(args.output_dir, fname)
                source.to_yaml(out_path)
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  FAIL {rid}: {e}", file=sys.stderr)

    print(f"\nResults: {passed} passed, {failed} failed")

    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
