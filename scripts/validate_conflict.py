#!/usr/bin/env python3
"""
scripts/validate_conflict.py — Validate conflict entities across the corpus.

Checks:
- Conflict IDs match uppercase hyphenated format ([A-Z][-A-Z0-9]+)
- Population codes in conflict parties are valid
- Resolution status is a known value
- UNRESOLVED conflicts have mode_s_trigger set (the Person-Mode handoff)
- Conflict matrix .md files have consistent structure
- YAML files validate against schemas/conflict.py

Usage:
    python3 scripts/validate_conflict.py                  # full scan
    python3 scripts/validate_conflict.py --yaml-only      # validate YAML files only
    python3 scripts/validate_conflict.py --matrices-only  # validate conflict matrices only

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

CONFLICT_ID_RE = re.compile(r"^[A-Z][-A-Z0-9]+$")

# The ratified status vocabulary — owner ruling 2026-08-14, migration 058.
# Mirrors schemas.conflict.RATIFIED_STATUSES and the SQL CHECK on conflicts.
VALID_RESOLUTION_STATUSES = {
    "ACTIVE",
    "PROPOSED",
    "DEFERRED",
    "RESOLVED-EVIDENCE",
    "RESOLVED-CONSENSUS",
    "UNRESOLVED",
    "CLOSED",
    "RETIRED",
}

VALID_STRATEGY_CODES = {
    "SZ",   # Sensory Zoning
    "PP",   # Parallel Provision
    "TZ",   # Temporal Zoning
    "ID",   # Individual Default
    "HA",   # Harm Asymmetry
    "BB",   # Broadest Benefit
    "SRW",  # Shared Route with support
    "OT-REF",  # OT referral
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


def validate_matrices(matrix_dir: str, result: ValidationResult):
    """Validate conflict matrix .md files."""
    if not os.path.isdir(matrix_dir):
        result.warn("matrices", f"Directory not found: {matrix_dir} (skipping)")
        return

    md_files = sorted(f for f in os.listdir(matrix_dir) if f.endswith(".md"))
    if not md_files:
        result.warn("matrices", "No .md files found in conflict-matrices/")
        return

    from schemas.enums import PopulationCode
    valid_pops = {e.value for e in PopulationCode}

    for fname in md_files:
        filepath = os.path.join(matrix_dir, fname)
        source = f"matrix:{fname}"

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for a title heading
        if not re.search(r"^#\s+", content, re.MULTILINE):
            result.warn(source, "No title heading found")

        # Check for resolution status
        found_statuses = set()
        for status in VALID_RESOLUTION_STATUSES:
            if status in content:
                found_statuses.add(status)
        # Also check for retired spellings. Each maps to a ratified word; the two
        # TIER-2 forms used to be redirected to MODE-S spellings, which the
        # 2026-08-14 ruling then retired in turn, so those messages were pointing
        # readers at a word that is no longer legal anywhere.
        # "OPEN" is deliberately absent: it is retired in favour of ACTIVE, but a
        # bare substring match would fire on the SPATIAL-OPEN domain code and on
        # ordinary prose. A substring check is only safe for distinctive spellings.
        for retired, ratified in (
            ("UNRESOLVABLE-TIER-2", "UNRESOLVED"),
            ("TIER-2-ONLY", "UNRESOLVED"),
            ("UNRESOLVABLE-MODE-S", "UNRESOLVED"),
            ("MODE-S-ONLY", "UNRESOLVED"),
            ("RESOLUTION-PROPOSED", "PROPOSED"),
        ):
            if retired in content:
                result.error(
                    source,
                    f"Retired status {retired} found — rename to {ratified}"
                )

        # Check population codes in table rows
        pop_pattern = re.compile(
            r"\b(MOB|VIS|DEAF|NEU|DEM|NDV|PAIN|DBL|OFS|IntD|ALL|"
            r"MOB/AMB|MOB/UPL|NDV/AUT|NDV/ADHD|NDV/SENS|NDV/MH|"
            r"NEU/PCS|OFS/ME|OFS/POTS|OFS/MCAS)\b"
        )
        pops_found = set(pop_pattern.findall(content))
        invalid_pops = pops_found - valid_pops
        if invalid_pops:
            result.error(source, f"Unknown population codes: {sorted(invalid_pops)}")

    print(f"  Matrices: {len(md_files)} files scanned")


def validate_yaml_files(yaml_dir: str, result: ValidationResult):
    """Validate YAML conflict files against the Conflict schema."""
    if not os.path.isdir(yaml_dir):
        result.warn("yaml", f"YAML directory not found: {yaml_dir} (skipping)")
        return

    try:
        from schemas.conflict import Conflict
    except ImportError as e:
        result.error("yaml", f"Cannot import Conflict schema: {e}")
        return

    import yaml

    yaml_files = sorted(
        f for f in os.listdir(yaml_dir) if f.endswith(".yaml") or f.endswith(".yml")
    )

    if not yaml_files:
        result.warn("yaml", f"No YAML files in {yaml_dir}")
        return

    valid_count = 0
    for fname in yaml_files:
        filepath = os.path.join(yaml_dir, fname)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            Conflict.model_validate(data)
            valid_count += 1

        except Exception as e:
            result.error(fname, str(e))

    print(f"  YAML: {valid_count}/{len(yaml_files)} valid")


def main():
    parser = argparse.ArgumentParser(description="Validate conflict entities")
    parser.add_argument("--yaml-only", action="store_true")
    parser.add_argument("--matrices-only", action="store_true")
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result = ValidationResult()

    if args.yaml_only:
        validate_yaml_files(os.path.join(repo_root, "data", "conflicts"), result)
    elif args.matrices_only:
        validate_matrices(
            os.path.join(repo_root, "references", "conflict-matrices"), result
        )
    else:
        print("Running full conflict validation...\n")
        validate_matrices(
            os.path.join(repo_root, "references", "conflict-matrices"), result
        )
        validate_yaml_files(os.path.join(repo_root, "data", "conflicts"), result)

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
