#!/usr/bin/env python3
"""
scripts/convert/convert_conflicts.py — conflicts.json → conflict YAML

Reads references/website/data/conflicts.json and produces one YAML file
per conflict domain in data/conflicts/.

Usage:
    python3 scripts/convert/convert_conflicts.py
    python3 scripts/convert/convert_conflicts.py --dry-run
"""

import json
import os
import sys
import yaml
from pathlib import Path


def convert(input_path: str, output_dir: str, dry_run: bool = False):
    """Convert conflicts.json to per-conflict YAML files."""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    records = []

    for conflict in data.get('resolved_conflicts', []) + data.get('unresolvable_conflicts', []):
        cid = conflict['conflict_id']

        # Build party structures
        pop_a = conflict.get('population_a', {})
        pop_b = conflict.get('population_b', {})

        record = {
            'conflict_id': cid,
            'conflict_label': conflict.get('conflict_label', ''),
            'domain': conflict.get('domain', ''),
            'population_a': {
                'codes': pop_a.get('codes', []),
                'specification': pop_a.get('specification', ''),
            },
            'population_b': {
                'codes': pop_b.get('codes', []),
                'specification': pop_b.get('specification', ''),
            },
            'resolution': {
                'status': conflict.get('resolution', {}).get('status', 'OPEN'),
                'strategy_codes': conflict.get('resolution', {}).get('strategy_codes', []),
                'strategy_labels': conflict.get('resolution', {}).get('strategy_labels', []),
                'description': conflict.get('resolution', {}).get('description', ''),
                'evidence_quality': conflict.get('resolution', {}).get('evidence_quality'),
            },
            'governing_principle': conflict.get('governing_principle'),
            'specifications_involved': conflict.get('specifications_involved', []),
            'connection_ids': conflict.get('connection_ids', []),
            'unresolvable_residual': conflict.get('unresolvable_residual'),
            'tier_2_trigger': conflict.get('tier_2_trigger'),
            'mitigation': conflict.get('mitigation'),
            'ot_assessment_mandatory': conflict.get('ot_assessment_mandatory', False),
            'citations': [
                {'ref': c.get('ref', ''), 'finding': c.get('finding')}
                for c in conflict.get('citations', [])
            ],
        }

        # Decision tree (if present)
        dt = conflict.get('decision_tree')
        if dt:
            record['decision_tree'] = dt

        records.append(record)

    if dry_run:
        print(f"Would write {len(records)} conflict records to {output_dir}/")
        for r in records:
            status = r['resolution']['status']
            print(f"  {r['conflict_id']}: {r['conflict_label']} [{status}]")
        return

    for record in records:
        filename = record['conflict_id'].lower().replace(' ', '-') + '.yaml'
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(record, f, default_flow_style=False, allow_unicode=True,
                      sort_keys=False, width=120)
        print(f"  Wrote {filepath}")

    print(f"\nTotal: {len(records)} conflict records")


def main():
    dry_run = '--dry-run' in sys.argv
    repo_root = Path(__file__).resolve().parent.parent.parent
    input_path = repo_root / "references/website/data/conflicts.json"
    output_dir = repo_root / "data/conflicts"

    if not input_path.exists():
        print(f"ERROR: Input not found: {input_path}")
        sys.exit(1)

    convert(str(input_path), str(output_dir), dry_run)


if __name__ == "__main__":
    main()
