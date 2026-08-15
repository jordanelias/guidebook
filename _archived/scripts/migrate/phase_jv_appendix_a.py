#!/usr/bin/env python3
"""
scripts/migrate/phase_jv_appendix_a.py — Appendix A → jurisdictional_value migration

Phase: B2.3
Purpose: Parse 20 jurisdiction comparison tables from Appendix A into
         structured jurisdictional_value records for the SQLite database.

Input:  parts/v10/appendix-a-jurisdiction-comparison.md
Output: data/jurisdictional_values/ (YAML files per table)
        migration-report-appendix-a.md (verification report)

Usage:
    python3 scripts/migrate/phase_jv_appendix_a.py
    python3 scripts/migrate/phase_jv_appendix_a.py --dry-run
    python3 scripts/migrate/phase_jv_appendix_a.py --report-only
"""

import re
import os
import sys
import json
import yaml
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional, List

# ─── Configuration ───────────────────────────────────────────────────────────

APPENDIX_A_PATH = "parts/v10/appendix-a-jurisdiction-comparison.md"
OUTPUT_DIR = "data/jurisdictional_values"
REPORT_PATH = "data/jurisdictional_values/migration-report-appendix-a.md"

# Item code → spec_id mapping (from specification-database.json)
# Populated codes have existing spec_ids; others use item_code as interim key
ITEM_TO_SPEC = {
    "E-01": "SPEC-0044",
    "G-03": "SPEC-0064",
    "H-01": "SPEC-0032",
    "I-01": "SPEC-0054",
    "I-02": "SPEC-0050",
    # Remaining codes will get spec_ids during C3 (specification page migration)
}

# Jurisdiction code normalization
JURISDICTION_MAP = {
    "US": "US", "UK": "GB", "DE": "DE", "DE (current)": "DE",
    "DE (draft)": "DE",  # draft standard, flag in notes
    "AU": "AU", "NO": "NO", "FR": "FR", "CH": "CH",
    "CA": "CA", "EU": "EU", "ISO": "ISO", "JP": "JP",
    "SG": "SG",
    # Skip "Guidebook" rows — those are the project's own values
}

# ─── Table metadata ──────────────────────────────────────────────────────────

@dataclass
class TableMeta:
    """Metadata for each Appendix A table."""
    section: str           # e.g. "A.1"
    title: str             # e.g. "Ramp Gradients"
    item_code: str         # e.g. "E-03"
    primary_column: str    # which column holds the primary value
    unit: Optional[str] = None
    notes: Optional[str] = None

# Map section headings to their item codes and primary value columns
TABLE_REGISTRY = {
    "A.1": TableMeta("A.1", "Ramp Gradients", "E-03", "Max Gradient", "ratio"),
    "A.2": TableMeta("A.2", "Threshold Heights", "E-06", "Max Threshold", "mm"),
    "A.3": TableMeta("A.3", "Corridor & Circulation Widths", "E-08", "Min Width", "mm"),
    "A.4": TableMeta("A.4", "Lift Car Dimensions", "E-01", "Min Car (W×D)", "mm"),
    "A.5": TableMeta("A.5", "Reach Ranges & Controls", "H-01", "Low Reach", "mm"),
    "A.6": TableMeta("A.6", "Luminance Contrast (LRV)", "C-04", "Min Contrast", "LRV"),
    "A.7": TableMeta("A.7", "Assistive Listening Systems", "A-10", "Trigger", None),
    "A.8": TableMeta("A.8", "Visual Fire Alarm", "B-10", "Flash Rate", "Hz"),
    "A.9": TableMeta("A.9", "Changing Places / Adult Changing Facilities", "E-15", "Mandatory", None),
    "A.10": TableMeta("A.10", "Kitchen Worktop", "I-02", "Height", "mm"),
    "A.11": TableMeta("A.11", "Grab Bar Positioning", "G-03", "Height Centre (horiz)", "mm"),
    "A.12": TableMeta("A.12", "Anti-Scald Temperature Limits", "I-03", "Max Temperature", "°C"),
    "A.13": TableMeta("A.13", "Slip Resistance Test Methods", "E-07", "Threshold", None),
    "A.14": TableMeta("A.14", "Door Opening Force", "I-01", "Interior Doors", "N"),
    "A.15": TableMeta("A.15", "Rest Seating Intervals", "E-10", "External Routes", "m"),
    "A.16": TableMeta("A.16", "Classroom Acoustic Standards", "A-04", "RT (general)", "s"),
    "A.17": TableMeta("A.17", "Signage & Tactile Requirements", "D-08", "Sign Height (centre)", "mm"),
    "A.18": TableMeta("A.18", "Platform Lift Dimensions", "E-12", "Min. Platform (W×D)", "mm"),
    "A.19": TableMeta("A.19", "Accessible Bathroom Minimum Dimensions", "G-04", "Min. Floor Area (approx.)", "m²"),
    "A.20": TableMeta("A.20", "TWSI Detail Patterns", "E-09", "Warning Pattern", None),
}

# ─── Data structures ─────────────────────────────────────────────────────────

@dataclass
class JurisdictionalValue:
    """A single jurisdictional value record."""
    spec_id: Optional[str]
    item_code: str
    jurisdiction: str
    standard_name: str
    value_text: str
    value_numeric: Optional[float] = None
    unit: Optional[str] = None
    is_code_minimum: int = 1
    evidence_tier: int = 6  # codes are Tier 6 by default
    source_section: str = ""  # e.g. "A.1"
    notes: Optional[str] = None


# ─── Parsing ─────────────────────────────────────────────────────────────────

def parse_markdown_table(lines: List[str]) -> List[dict]:
    """Parse a markdown table into a list of row dicts."""
    rows = []
    headers = None

    for line in lines:
        line = line.strip()
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if not cells:
            continue
        # Skip separator rows
        if all(c.startswith('-') or c == '' for c in cells):
            continue
        if headers is None:
            headers = cells
            continue
        row = {}
        for i, h in enumerate(headers):
            row[h] = cells[i] if i < len(cells) else ''
        rows.append(row)

    return rows


def extract_numeric(text: str) -> Optional[float]:
    """Try to extract a numeric value from a text string."""
    text = text.replace('**', '').replace('≤', '').replace('≥', '').replace('>', '').replace('<', '')
    # Try common patterns
    # "1:12 (8.3%)" → 8.3
    pct = re.search(r'(\d+\.?\d*)%', text)
    if pct:
        return float(pct.group(1))
    # "1200mm" → 1200
    mm = re.search(r'(\d+\.?\d*)\s*mm', text)
    if mm:
        return float(mm.group(1))
    # "43°C" → 43
    deg = re.search(r'(\d+\.?\d*)\s*°C', text)
    if deg:
        return float(deg.group(1))
    # "20N" → 20
    n = re.search(r'(\d+\.?\d*)\s*N\b', text)
    if n:
        return float(n.group(1))
    # "0.6s" → 0.6
    s = re.search(r'(\d+\.?\d*)\s*s\b', text)
    if s:
        return float(s.group(1))
    # "5.0 m²" → 5.0
    sqm = re.search(r'(\d+\.?\d*)\s*m²', text)
    if sqm:
        return float(sqm.group(1))
    # "2 Hz" → 2
    hz = re.search(r'(\d+\.?\d*)\s*Hz', text)
    if hz:
        return float(hz.group(1))
    # Plain number
    plain = re.search(r'^(\d+\.?\d*)$', text.strip())
    if plain:
        return float(plain.group(1))
    # "≤5mm" → 5
    leq = re.search(r'(\d+\.?\d*)', text)
    if leq:
        return float(leq.group(1))

    return None


def parse_appendix_a(filepath: str) -> List[JurisdictionalValue]:
    """Parse the entire Appendix A file into JV records."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    records = []
    current_section = None
    current_lines = []

    for line in lines:
        # Detect section headers
        match = re.match(r'^## A\.(\d+)', line)
        if match:
            # Process previous section
            if current_section and current_lines:
                records.extend(process_section(current_section, current_lines))
            section_num = match.group(1)
            current_section = f"A.{section_num}"
            current_lines = []
            continue

        if line.startswith('## Notes'):
            # Process last section before notes
            if current_section and current_lines:
                records.extend(process_section(current_section, current_lines))
            current_section = None
            current_lines = []
            continue

        if current_section:
            current_lines.append(line)

    # Process final section if any
    if current_section and current_lines:
        records.extend(process_section(current_section, current_lines))

    return records


def process_section(section: str, lines: List[str]) -> List[JurisdictionalValue]:
    """Process a single Appendix A section into JV records."""
    meta = TABLE_REGISTRY.get(section)
    if not meta:
        print(f"  WARNING: No metadata for section {section}, skipping")
        return []

    rows = parse_markdown_table(lines)
    records = []

    for row in rows:
        jurisdiction_raw = row.get('Jurisdiction', '').replace('**', '').strip()

        # Skip guidebook rows (those are our own values, not jurisdiction data)
        if jurisdiction_raw.lower() == 'guidebook':
            continue

        # Normalize jurisdiction code
        jurisdiction = JURISDICTION_MAP.get(jurisdiction_raw)
        if not jurisdiction:
            print(f"  WARNING: Unknown jurisdiction '{jurisdiction_raw}' in {section}")
            continue

        # Extract standard name
        standard = row.get('Standard', '').replace('**', '').strip()

        # Get the primary value column
        primary_col = meta.primary_column
        value_text = row.get(primary_col, '').replace('**', '').strip()

        # Build composite value text from all data columns (skip Jurisdiction and Standard)
        all_values = {}
        for col, val in row.items():
            if col not in ('Jurisdiction', 'Standard') and val.strip() and val.strip() != '—':
                all_values[col] = val.replace('**', '').strip()

        # Create composite value text
        if len(all_values) > 1:
            composite = '; '.join(f"{k}: {v}" for k, v in all_values.items())
        else:
            composite = value_text

        # Extract numeric
        value_numeric = extract_numeric(value_text) if value_text else None

        # Handle special jurisdiction notes
        notes = None
        if jurisdiction_raw == "DE (draft)":
            notes = "Draft standard — pending publication"
        if jurisdiction_raw == "DE (current)":
            notes = "Current standard — revision pending"

        spec_id = ITEM_TO_SPEC.get(meta.item_code)

        jv = JurisdictionalValue(
            spec_id=spec_id,
            item_code=meta.item_code,
            jurisdiction=jurisdiction,
            standard_name=standard,
            value_text=composite,
            value_numeric=value_numeric,
            unit=meta.unit,
            is_code_minimum=1,
            evidence_tier=6,
            source_section=section,
            notes=notes,
        )
        records.append(jv)

    return records


# ─── Output ──────────────────────────────────────────────────────────────────

def write_yaml_records(records: List[JurisdictionalValue], output_dir: str):
    """Write JV records as YAML files grouped by section."""
    os.makedirs(output_dir, exist_ok=True)

    # Group by source_section
    by_section = {}
    for r in records:
        section = r.source_section
        if section not in by_section:
            by_section[section] = []
        by_section[section].append(r)

    for section, section_records in sorted(by_section.items()):
        meta = TABLE_REGISTRY.get(section)
        filename = f"{section.lower().replace('.', '-')}_{meta.item_code.lower().replace('-', '')}.yaml"
        filepath = os.path.join(output_dir, filename)

        data = {
            'section': section,
            'title': meta.title,
            'item_code': meta.item_code,
            'spec_id': ITEM_TO_SPEC.get(meta.item_code),
            'records': [asdict(r) for r in section_records],
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True,
                      sort_keys=False, width=120)

        print(f"  Wrote {len(section_records)} records to {filepath}")


def write_report(records: List[JurisdictionalValue], output_path: str):
    """Write migration verification report."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Statistics
    by_section = {}
    by_jurisdiction = {}
    by_item = {}
    with_spec_id = 0
    without_spec_id = 0

    for r in records:
        by_section[r.source_section] = by_section.get(r.source_section, 0) + 1
        by_jurisdiction[r.jurisdiction] = by_jurisdiction.get(r.jurisdiction, 0) + 1
        by_item[r.item_code] = by_item.get(r.item_code, 0) + 1
        if r.spec_id:
            with_spec_id += 1
        else:
            without_spec_id += 1

    report = []
    report.append("# Appendix A Migration Report")
    report.append(f"**Generated:** script run")
    report.append(f"**Total records:** {len(records)}")
    report.append(f"**Tables processed:** {len(by_section)}")
    report.append(f"**Jurisdictions covered:** {len(by_jurisdiction)}")
    report.append(f"**Item codes covered:** {len(by_item)}")
    report.append(f"**With spec_id:** {with_spec_id}")
    report.append(f"**Without spec_id (pending C3):** {without_spec_id}")
    report.append("")
    report.append("## Records per section")
    report.append("")
    report.append("| Section | Title | Item Code | Records | spec_id |")
    report.append("|---|---|---|---|---|")
    for section in sorted(by_section.keys()):
        meta = TABLE_REGISTRY.get(section)
        sid = ITEM_TO_SPEC.get(meta.item_code, "PENDING")
        report.append(f"| {section} | {meta.title} | {meta.item_code} | {by_section[section]} | {sid} |")

    report.append("")
    report.append("## Records per jurisdiction")
    report.append("")
    report.append("| Jurisdiction | Records |")
    report.append("|---|---|")
    for j in sorted(by_jurisdiction.keys()):
        report.append(f"| {j} | {by_jurisdiction[j]} |")

    report.append("")
    report.append("## Verification checklist")
    report.append("")
    report.append(f"- [{'x' if len(records) >= 150 else ' '}] ≥150 records extracted")
    report.append(f"- [{'x' if len(by_section) == 20 else ' '}] All 20 tables processed ({len(by_section)}/20)")
    report.append(f"- [{'x' if len(by_jurisdiction) >= 6 else ' '}] ≥6 jurisdictions represented ({len(by_jurisdiction)})")
    report.append(f"- [ ] Spot-check: 5 random records verified against source")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

    print(f"  Report written to {output_path}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    dry_run = '--dry-run' in sys.argv
    report_only = '--report-only' in sys.argv

    # Find repo root (script is at scripts/migrate/)
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent

    input_path = repo_root / APPENDIX_A_PATH
    output_dir = repo_root / OUTPUT_DIR
    report_path = repo_root / REPORT_PATH

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        sys.exit(1)

    print(f"Parsing {input_path}...")
    records = parse_appendix_a(str(input_path))
    print(f"Extracted {len(records)} jurisdictional_value records from 20 tables.")

    if dry_run:
        print("\n[DRY RUN] Would write:")
        by_section = {}
        for r in records:
            by_section[r.source_section] = by_section.get(r.source_section, 0) + 1
        for s in sorted(by_section.keys()):
            meta = TABLE_REGISTRY[s]
            print(f"  {s} ({meta.item_code}): {by_section[s]} records")
        return

    if not report_only:
        print(f"\nWriting YAML records to {output_dir}/...")
        write_yaml_records(records, str(output_dir))

    print(f"\nWriting report to {report_path}...")
    write_report(records, str(report_path))

    print("\nDone.")


if __name__ == "__main__":
    main()
