#!/usr/bin/env python3
"""
scripts/validate_jurisdiction.py — Validate jurisdiction codes and standards-registry.

Per governance/jurisdiction-philosophy.md (A8):
- All jurisdiction codes resolve to JurisdictionCode enum
- GB rejected (must be UK)
- Standards-registry entries have required fields and valid status
- BPC jurisdiction coverage tracked

Usage:
    python3 scripts/validate_jurisdiction.py              # full scan
    python3 scripts/validate_jurisdiction.py --registry    # standards-registry only
    python3 scripts/validate_jurisdiction.py --sources     # source jurisdiction fields only

Exit codes: 0 = pass, 1 = errors, 2 = config error
"""

import argparse
import glob
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.enums import JurisdictionCode

VALID_CODES = {member.value for member in JurisdictionCode}
VALID_STATUSES = {"CURRENT", "UPDATED", "SUPERSEDED", "WITHDRAWN"}
REQUIRED_REGISTRY_FIELDS = {
    "jurisdiction", "standard_cited", "current_version",
    "status", "last_checked",
}
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}(\s\d{2}:\d{2})?$")

# Common full-name → code mapping for jurisdiction-tracker output
NAME_TO_CODE = {
    "australia": "AU", "bangladesh": "BD", "brazil": "BR", "canada": "CA",
    "switzerland": "CH", "china": "CN", "germany": "DE", "denmark": "DK",
    "egypt": "EG", "france": "FR", "indonesia": "ID", "ireland": "IE",
    "india": "IN", "japan": "JP", "kenya": "KE", "south korea": "KR",
    "nigeria": "NG", "netherlands": "NL", "norway": "NO",
    "new zealand": "NZ", "sweden": "SE", "singapore": "SG",
    "united kingdom": "UK", "uk": "UK", "united states": "US", "usa": "US",
    "south africa": "ZA", "iso": "ISO", "eu": "EU",
    "european union": "EU",
}


def resolve_jurisdiction(raw) -> str | None:
    """Resolve a jurisdiction string to a canonical code."""
    if not raw or not isinstance(raw, str):
        return None
    raw = raw.strip().strip('"').strip("'")
    if raw in VALID_CODES:
        return raw
    if raw.upper() in VALID_CODES:
        return raw.upper()
    lower = raw.lower()
    if lower in NAME_TO_CODE:
        return NAME_TO_CODE[lower]
    return None


def validate_registry(path: str) -> tuple:
    """Validate standards-registry.md entries. Returns (errors, warnings)."""
    errors = []
    warnings = []

    if not os.path.exists(path):
        return [f"Standards registry not found: {path}"], []

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract YAML blocks
    blocks = re.findall(r"```yaml\s*\n(.*?)```", content, re.DOTALL)

    seen_pairs = set()
    for i, block in enumerate(blocks):
        try:
            data = yaml.safe_load(block)
        except yaml.YAMLError as e:
            errors.append(f"YAML parse error in block {i+1}: {e}")
            continue

        if not isinstance(data, dict):
            continue

        # Skip template/example blocks — identified by jurisdiction being a list
        # or a placeholder string like '[2-letter code or full name]'
        raw_jur = data.get("jurisdiction", "")
        if not isinstance(raw_jur, str) or (isinstance(raw_jur, str) and raw_jur.startswith("[")):
            continue  # template placeholder — not a real registry entry

        # Check required fields
        missing = REQUIRED_REGISTRY_FIELDS - set(data.keys())
        if missing:
            errors.append(
                f"Block {i+1}: missing fields: {missing}"
            )

        # Check jurisdiction
        jur = raw_jur
        if jur == "GB":
            errors.append(
                f"Block {i+1}: 'GB' must be 'UK' per project convention"
            )
        code = resolve_jurisdiction(jur)
        if code is None and jur:
            warnings.append(
                f"Block {i+1}: unrecognised jurisdiction '{jur}' "
                f"(not in canonical 24 — Phase 3 expansion or data error)"
            )

        # Check status
        status = data.get("status", "")
        if isinstance(status, str):
            status = status.strip().strip('"')
        if status and status not in VALID_STATUSES:
            errors.append(
                f"Block {i+1}: invalid status '{status}' "
                f"(must be {VALID_STATUSES})"
            )
        if status == "SUPERSEDED":
            warnings.append(
                f"Block {i+1}: SUPERSEDED — {data.get('standard_cited', '?')} "
                f"in {jur} requires update before publication"
            )

        # Check date format
        lc = data.get("last_checked", "")
        if isinstance(lc, str) and lc and not DATE_PATTERN.match(lc.strip().strip('"')):
            errors.append(
                f"Block {i+1}: last_checked format must be YYYY-MM-DD HH:MM, "
                f"got: '{lc}'"
            )

        # Duplicate detection
        pair_key = (jur, data.get("standard_cited", ""))
        if pair_key in seen_pairs:
            warnings.append(
                f"Block {i+1}: duplicate entry for {jur} / "
                f"{data.get('standard_cited', '?')}"
            )
        seen_pairs.add(pair_key)

    return errors, warnings


def validate_source_jurisdictions(repo_root: str) -> tuple:
    """Check jurisdiction fields on EvidenceSource YAML files."""
    errors = []
    warnings = []
    source_dir = os.path.join(repo_root, "data", "sources")

    if not os.path.isdir(source_dir):
        return [], []

    for path in sorted(glob.glob(os.path.join(source_dir, "*.yaml"))):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception:
            continue

        if not isinstance(data, dict):
            continue

        jur = data.get("jurisdiction")
        if jur is None:
            continue

        if jur == "GB":
            errors.append(
                f"{os.path.basename(path)}: 'GB' must be 'UK'"
            )
        elif resolve_jurisdiction(jur) is None:
            warnings.append(
                f"{os.path.basename(path)}: unrecognized jurisdiction '{jur}'"
            )

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(
        description="Validate jurisdiction codes and standards-registry"
    )
    parser.add_argument("--registry", action="store_true",
                        help="Standards-registry only")
    parser.add_argument("--sources", action="store_true",
                        help="Source jurisdiction fields only")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    total_errors = 0
    total_warnings = 0

    if not args.sources:
        registry_path = os.path.join(
            repo_root, "references", "standards-registry.md"
        )
        e, w = validate_registry(registry_path)
        total_errors += len(e)
        total_warnings += len(w)
        for err in e:
            print(f"ERROR registry: {err}")
        for warn in w:
            print(f"WARN  registry: {warn}")

    if not args.registry:
        e2, w2 = validate_source_jurisdictions(repo_root)
        total_errors += len(e2)
        total_warnings += len(w2)
        for err in e2:
            print(f"ERROR source: {err}")
        for warn in w2:
            print(f"WARN  source: {warn}")

    status = "PASS" if total_errors == 0 else "FAIL"
    print(
        f"\n{status}: {total_errors} errors, {total_warnings} warnings",
        file=sys.stderr,
    )
    return 1 if total_errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
