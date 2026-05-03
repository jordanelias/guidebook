#!/usr/bin/env python3
"""
scripts/convert/convert_populations.py — populations.json → population YAML

Reads references/website/data/populations.json and produces one YAML file
per population code in data/populations/.

Usage:
    python3 scripts/convert/convert_populations.py
    python3 scripts/convert/convert_populations.py --dry-run
"""

import json
import os
import sys
import yaml
from pathlib import Path


def convert(input_path: str, output_dir: str, dry_run: bool = False):
    """Convert populations.json to per-population YAML files."""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    records = []

    for pop in data.get('populations', []):
        code = pop['population_id']

        record = {
            'code': code,
            'parent_code': None,  # Top-level populations
            'label': pop.get('label', ''),
            'definition': pop.get('functional_profile', '')[:200] + '...' if pop.get('functional_profile', '') else '',
            'functional_profile': pop.get('functional_profile'),
            'primary_barriers': pop.get('primary_barriers', []),
            'key_parameters': pop.get('key_specifications', []),
            'evidence_confidence': pop.get('evidence_confidence'),
            'conflict_domains': pop.get('conflict_domains', []),
            'co_occurrence_notes': pop.get('co_occurrence_notes'),
            'co1_status': pop.get('co1_status'),
            'co1_gap_note': pop.get('co1_gap_note'),
            'bpc_slugs': pop.get('bpc_slugs', []),
            'specification_count': pop.get('specification_count'),
        }

        # Handle sub-codes
        sub_codes = pop.get('sub_codes', [])
        sub_labels = pop.get('sub_code_labels', {})
        sub_records = []
        for sc in sub_codes:
            sub_record = {
                'code': sc,
                'parent_code': code,
                'label': sub_labels.get(sc, sc),
                'definition': f'Sub-population of {code}',
            }
            sub_records.append(sub_record)

        records.append(record)
        records.extend(sub_records)

    if dry_run:
        print(f"Would write {len(records)} population records to {output_dir}/")
        for r in records:
            prefix = "  " if r.get('parent_code') else ""
            print(f"  {prefix}{r['code']}: {r['label']}")
        return

    for record in records:
        filename = record['code'].lower().replace('/', '-') + '.yaml'
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(record, f, default_flow_style=False, allow_unicode=True,
                      sort_keys=False, width=120)
        print(f"  Wrote {filepath}")

    print(f"\nTotal: {len(records)} population records")


def main():
    dry_run = '--dry-run' in sys.argv
    repo_root = Path(__file__).resolve().parent.parent.parent
    input_path = repo_root / "references/website/data/populations.json"
    output_dir = repo_root / "data/populations"

    if not input_path.exists():
        print(f"ERROR: Input not found: {input_path}")
        sys.exit(1)

    convert(str(input_path), str(output_dir), dry_run)


if __name__ == "__main__":
    main()
