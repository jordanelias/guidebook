#!/usr/bin/env python3
"""
scripts/convert/convert_jurisdictions.py — Convert standards-registry.md
entries to per-jurisdiction YAML files under data/jurisdictions/.

Groups standards-registry entries by jurisdiction code and produces one
YAML file per jurisdiction with all its standard citations.

Usage:
    python3 scripts/convert/convert_jurisdictions.py [--input PATH] [--output-dir PATH] [--dry-run]
"""

import argparse
import os
import re
import sys
from collections import defaultdict

import yaml

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from schemas.enums import JurisdictionCode

VALID_CODES = {member.value for member in JurisdictionCode}

# Name → code mapping
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


def resolve_code(raw: str) -> str | None:
    """Resolve jurisdiction string to canonical code."""
    if not raw:
        return None
    raw = raw.strip().strip('"').strip("'")
    if raw in VALID_CODES:
        return raw
    if raw.upper() in VALID_CODES:
        return raw.upper()
    if raw.lower() in NAME_TO_CODE:
        return NAME_TO_CODE[raw.lower()]
    return None


def parse_registry(path: str) -> list:
    """Parse standards-registry.md YAML blocks into dicts."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.findall(r"```yaml\s*\n(.*?)```", content, re.DOTALL)
    records = []

    for block in blocks:
        try:
            data = yaml.safe_load(block)
        except yaml.YAMLError:
            continue
        if isinstance(data, dict) and "jurisdiction" in data:
            records.append(data)

    return records


def main():
    parser = argparse.ArgumentParser(
        description="Convert standards-registry to per-jurisdiction YAML"
    )
    parser.add_argument(
        "--input",
        default="references/standards-registry.md",
        help="Path to standards-registry.md",
    )
    parser.add_argument(
        "--output-dir",
        default="data/jurisdictions",
        help="Output directory for YAML files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and validate without writing files",
    )
    args = parser.parse_args()

    records = parse_registry(args.input)
    print(f"Parsed {len(records)} registry entries from {args.input}")

    # Group by jurisdiction
    by_jurisdiction = defaultdict(list)
    unresolved = 0

    for rec in records:
        raw_jur = rec.get("jurisdiction", "")
        code = resolve_code(raw_jur)
        if code is None:
            print(f"  WARNING: unresolvable jurisdiction: '{raw_jur}'",
                  file=sys.stderr)
            unresolved += 1
            continue

        entry = {
            "standard_cited": rec.get("standard_cited", ""),
            "current_version": rec.get("current_version", ""),
            "status": rec.get("status", ""),
            "key_changes": rec.get("key_changes", ""),
            "last_checked": rec.get("last_checked", ""),
            "source_url": rec.get("source_url", ""),
        }
        by_jurisdiction[code].append(entry)

    print(f"Grouped into {len(by_jurisdiction)} jurisdictions "
          f"({unresolved} unresolved)")

    if args.dry_run:
        for code in sorted(by_jurisdiction):
            n = len(by_jurisdiction[code])
            print(f"  {code}: {n} standards")
        return 0

    os.makedirs(args.output_dir, exist_ok=True)

    for code in sorted(by_jurisdiction):
        output = {
            "jurisdiction": code,
            "standards": by_jurisdiction[code],
        }
        out_path = os.path.join(args.output_dir, f"{code.lower()}.yaml")
        with open(out_path, "w", encoding="utf-8") as f:
            yaml.dump(output, f, default_flow_style=False, allow_unicode=True,
                      sort_keys=False)

    print(f"Wrote {len(by_jurisdiction)} files to {args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
