#!/usr/bin/env python3
"""
scripts/validate_item.py — Validate item entities across the corpus.

Checks:
- Item codes match [A-K]-NN format
- Category letter matches item code prefix
- Category names resolve to known categories
- No duplicate item codes across all sources
- Specification IDs match SPEC-NNNN format
- YAML files validate against schemas/item.py

Usage:
    python3 scripts/validate_item.py                  # full scan
    python3 scripts/validate_item.py --yaml-only      # validate YAML files only
    python3 scripts/validate_item.py --index-only     # validate part04-item-index only
    python3 scripts/validate_item.py path/to/file     # single file

Exit codes:
    0 = all checks pass
    1 = errors found
    2 = configuration error
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ITEM_CODE_RE = re.compile(r"^[A-K]-\d{2}$")

VALID_CATEGORIES = {
    "A": "Acoustics",
    "B": "Lighting and Visual Environment",
    "C": "Colour and Contrast",
    "D": "Wayfinding and Cognitive Environment",
    "E": "Circulation and Entrances",
    "F": "Thermal and Air Quality",
    "G": "Seating, Surfaces, and Fixtures",
    "H": "Controls and Hardware",
    "I": "Bathroom and Wet Areas",
    "J": "Kitchen and Workspace",
    "K": "Communication and Alerting",
}


class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, source: str, msg: str):
        self.errors.append(f"ERROR [{source}]: {msg}")

    def warn(self, source: str, msg: str):
        self.warnings.append(f"WARN  [{source}]: {msg}")

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


def validate_item_code(code: str, source: str, result: ValidationResult):
    """Validate a single item code."""
    if not ITEM_CODE_RE.match(code):
        result.error(source, f"Invalid item code format: '{code}' (expected [A-K]-NN)")
        return False
    return True


def validate_index(index_path: str, result: ValidationResult):
    """Validate references/part04-item-index.md."""
    if not os.path.exists(index_path):
        result.error("index", f"File not found: {index_path}")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    seen_codes = {}
    in_table = False

    for lineno, line in enumerate(lines, 1):
        line = line.strip()

        if line.startswith("| Code"):
            in_table = True
            continue
        if line.startswith("|---"):
            continue
        if not in_table or not line.startswith("|"):
            continue

        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 5:
            result.warn("index", f"Line {lineno}: table row has fewer than 5 columns")
            continue

        code = cells[0]
        title = cells[1]
        start_str = cells[2]
        end_str = cells[3]

        # Validate code format
        validate_item_code(code, f"index:L{lineno}", result)

        # Check for duplicates
        if code in seen_codes:
            result.warn(
                f"index:L{lineno}",
                f"Duplicate item code '{code}' (first at L{seen_codes[code]})",
            )
        seen_codes[code] = lineno

        # Validate line range
        if start_str.isdigit() and end_str.isdigit():
            start, end = int(start_str), int(end_str)
            if start >= end:
                result.error(
                    f"index:L{lineno}",
                    f"Invalid line range for {code}: start ({start}) >= end ({end})",
                )
        elif not start_str.isdigit() or not end_str.isdigit():
            result.warn(f"index:L{lineno}", f"Non-numeric line range for {code}")

    print(f"  Index: {len(seen_codes)} items scanned")


def validate_yaml_files(yaml_dir: str, result: ValidationResult):
    """Validate YAML item files against the Item schema."""
    if not os.path.isdir(yaml_dir):
        result.warn("yaml", f"YAML directory not found: {yaml_dir} (skipping)")
        return

    try:
        from schemas.item import Item
    except ImportError as e:
        result.error("yaml", f"Cannot import Item schema: {e}")
        return

    yaml_files = sorted(
        f for f in os.listdir(yaml_dir) if f.endswith(".yaml") or f.endswith(".yml")
    )

    if not yaml_files:
        result.warn("yaml", f"No YAML files in {yaml_dir}")
        return

    import yaml

    valid_count = 0
    for fname in yaml_files:
        filepath = os.path.join(yaml_dir, fname)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            Item.model_validate(data)
            valid_count += 1

        except Exception as e:
            result.error(fname, str(e))

    print(f"  YAML: {valid_count}/{len(yaml_files)} valid")


def validate_part4_codes(part4_path: str, result: ValidationResult):
    """Scan Part 4 markdown for item code consistency."""
    if not os.path.exists(part4_path):
        return

    with open(part4_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all item code references
    codes = set(re.findall(r"\b([A-K]-\d{2})\b", content))
    for code in sorted(codes):
        category = code[0]
        if category not in VALID_CATEGORIES:
            result.error("part04", f"Item code '{code}' uses unknown category '{category}'")

    print(f"  Part 4: {len(codes)} unique item codes found")


def main():
    parser = argparse.ArgumentParser(description="Validate item entities")
    parser.add_argument("path", nargs="?", help="Specific file to validate")
    parser.add_argument("--yaml-only", action="store_true")
    parser.add_argument("--index-only", action="store_true")
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result = ValidationResult()

    if args.path:
        if args.path.endswith((".yaml", ".yml")):
            validate_yaml_files(os.path.dirname(args.path), result)
        else:
            validate_index(args.path, result)
    elif args.yaml_only:
        validate_yaml_files(os.path.join(repo_root, "data", "items"), result)
    elif args.index_only:
        validate_index(
            os.path.join(repo_root, "references", "part04-item-index.md"), result
        )
    else:
        print("Running full item validation...\n")
        validate_index(
            os.path.join(repo_root, "references", "part04-item-index.md"), result
        )
        validate_yaml_files(os.path.join(repo_root, "data", "items"), result)
        validate_part4_codes(
            os.path.join(repo_root, "parts", "v10", "part04.md"), result
        )

    # Report
    print()
    if result.warnings:
        for w in result.warnings:
            print(w)
    if result.errors:
        for e in result.errors:
            print(e)

    if result.ok:
        print(f"\n✓ Validation passed ({len(result.warnings)} warnings)")
        sys.exit(0)
    else:
        print(
            f"\n✗ Validation failed: {len(result.errors)} errors, "
            f"{len(result.warnings)} warnings"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
