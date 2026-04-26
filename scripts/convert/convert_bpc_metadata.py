#!/usr/bin/env python3
"""
scripts/convert/convert_bpc_metadata.py — Extract metadata from BPC markdown
files into validated YAML under data/bpc-metadata/.

Processes active per-slug BPC files in references/bpc/{topic}/*.md.
Skips frozen top-level files and _template.md / index.md.

Extraction sources per file:
1. Header line: **Updated:** ... **Evidence tier range:** ... **Opus synthesis:** ...
2. YAML block inside ```yaml ... ``` fences
3. Key sources table: extracts REF-IDs and count

Usage:
    python3 scripts/convert/convert_bpc_metadata.py [--bpc-dir PATH] [--output-dir PATH] [--dry-run]
"""

import argparse
import os
import re
import sys

import yaml as yaml_lib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from schemas.bpc_metadata import BPCMetadata


def extract_header_fields(text: str) -> dict:
    """Extract metadata from the BPC header line.

    Format: **Updated:** 2026-03-26 16:45  **Evidence tier range:** 1–6  **Opus synthesis:** YES
    """
    fields = {}

    m = re.search(r'\*\*Updated:\*\*\s*([^\*]+)', text)
    if m:
        fields["header_updated"] = m.group(1).strip()

    m = re.search(r'\*\*Evidence tier range:\*\*\s*([^\*]+)', text)
    if m:
        fields["evidence_tier_range"] = m.group(1).strip()

    m = re.search(r'\*\*Opus synthesis:\*\*\s*([^\*\n]+)', text)
    if m:
        val = m.group(1).strip()
        fields["header_opus"] = val
        if "YES" in val.upper():
            fields["opus_synthesis"] = True
        elif "NO" in val.upper():
            fields["opus_synthesis"] = False

    return fields


def extract_yaml_block(text: str) -> dict:
    """Extract the first YAML block from the BPC file."""
    m = re.search(r'```yaml\n(.*?)\n```', text, re.DOTALL)
    if m:
        try:
            return yaml_lib.safe_load(m.group(1)) or {}
        except yaml_lib.YAMLError:
            return {}
    return {}


def extract_key_source_ref_ids(text: str) -> list:
    """Extract REF-IDs from the Key sources table.

    Looks for table rows with a REF-ID in the first column.
    Formats seen: "01", "DAB-05", "REF-RAP-18"
    """
    ref_ids = []
    in_key_sources = False

    for line in text.split("\n"):
        if re.match(r"^#{2,3}\s+Key sources", line, re.IGNORECASE):
            in_key_sources = True
            continue

        if in_key_sources:
            # Stop at next section
            if re.match(r"^#{2,3}\s+", line) and "Key sources" not in line:
                break

            # Table row with REF-ID
            if "|" in line and not line.strip().startswith("|---"):
                cells = [c.strip() for c in line.split("|")]
                cells = [c for c in cells if c]
                if cells:
                    ref_id = cells[0]
                    # Skip header row
                    if ref_id.lower() in ("ref-id", "refid", "ref_id", "id"):
                        continue
                    if ref_id and ref_id != "---":
                        ref_ids.append(ref_id)

    return ref_ids


def extract_slug_from_heading(text: str) -> str:
    """Extract slug from the first ## heading."""
    m = re.search(r'^## ([^\n]+)', text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return ""


def is_frozen(text: str) -> bool:
    """Check if file has FROZEN marker."""
    return "FROZEN" in text[:200]


def process_bpc_file(filepath: str, topic_dir: str) -> dict:
    """Extract all metadata from a single BPC file.

    Returns dict suitable for BPCMetadata validation.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    frozen = is_frozen(text)
    header = extract_header_fields(text)
    yaml_meta = extract_yaml_block(text)
    ref_ids = extract_key_source_ref_ids(text)
    heading_slug = extract_slug_from_heading(text)

    # Merge sources with priority: yaml_meta > header > filename
    slug = yaml_meta.get("slug") or heading_slug or os.path.splitext(os.path.basename(filepath))[0]

    # Population: yaml uses either "population" or "populations"
    pop = yaml_meta.get("population") or yaml_meta.get("populations")
    if isinstance(pop, list):
        pop = ", ".join(str(p) for p in pop)
    elif pop is None:
        pop = "UNKNOWN"
    pop = str(pop)

    # last_updated
    last_updated = yaml_meta.get("last_updated") or header.get("header_updated") or "UNKNOWN"
    # Clean: may have trailing text like "**Status: COMPLETE**"
    last_updated = re.sub(r'\s+\*\*.*', '', str(last_updated)).strip()
    if not re.match(r'^\d{4}-\d{2}-\d{2}', last_updated):
        last_updated = "1970-01-01"  # Placeholder for files without dates

    return {
        "slug": slug,
        "population": pop,
        "last_updated": last_updated,
        "topic_directory": topic_dir,
        "file_path": filepath,
        "opus_synthesis": yaml_meta.get("opus_synthesis") or header.get("opus_synthesis"),
        "opus_session": yaml_meta.get("opus_session"),
        "status": yaml_meta.get("status"),
        "evidence_tier_range": yaml_meta.get("evidence_tier_range") or header.get("evidence_tier_range"),
        "jurisdiction_count": yaml_meta.get("jurisdiction_count"),
        "language_count": yaml_meta.get("language_count"),
        "co0006_migration": yaml_meta.get("co0006_migration"),
        "key_source_ref_ids": ref_ids,
        "key_source_count": len(ref_ids),
        "header_updated": header.get("header_updated"),
        "header_opus": header.get("header_opus"),
        "is_frozen": frozen,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Extract BPC metadata into validated YAML"
    )
    parser.add_argument(
        "--bpc-dir",
        default="references/bpc",
        help="Path to BPC directory",
    )
    parser.add_argument(
        "--output-dir",
        default="data/bpc-metadata",
        help="Output directory for YAML files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate without writing files",
    )
    parser.add_argument(
        "--include-frozen",
        action="store_true",
        help="Also process frozen top-level files",
    )
    args = parser.parse_args()

    bpc_dir = args.bpc_dir
    if not os.path.isdir(bpc_dir):
        print(f"ERROR: BPC directory not found: {bpc_dir}", file=sys.stderr)
        return 2

    os.makedirs(args.output_dir, exist_ok=True)
    passed = 0
    failed = 0
    skipped = 0

    # Process per-slug files in topic subdirectories
    for entry in sorted(os.listdir(bpc_dir)):
        entry_path = os.path.join(bpc_dir, entry)

        if os.path.isdir(entry_path):
            # Topic directory — process all .md files
            for fname in sorted(os.listdir(entry_path)):
                if not fname.endswith(".md"):
                    continue
                filepath = os.path.join(entry_path, fname)
                try:
                    meta = process_bpc_file(filepath, topic_dir=entry)
                    bpc = BPCMetadata.model_validate(meta)
                    if not args.dry_run:
                        out_name = fname.replace(".md", ".yaml")
                        bpc.to_yaml(os.path.join(args.output_dir, out_name))
                    passed += 1
                except Exception as e:
                    failed += 1
                    print(f"  FAIL {filepath}: {e}", file=sys.stderr)

        elif entry.endswith(".md") and entry not in ("_template.md", "index.md"):
            # Top-level file (frozen population BPCs)
            if not args.include_frozen:
                skipped += 1
                continue
            filepath = entry_path
            try:
                meta = process_bpc_file(filepath, topic_dir="_frozen")
                bpc = BPCMetadata.model_validate(meta)
                if not args.dry_run:
                    out_name = entry.replace(".md", ".yaml")
                    bpc.to_yaml(os.path.join(args.output_dir, out_name))
                passed += 1
            except Exception as e:
                failed += 1
                print(f"  FAIL {filepath}: {e}", file=sys.stderr)

    print(f"\nResults: {passed} passed, {failed} failed, {skipped} skipped (frozen)")

    if failed > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
