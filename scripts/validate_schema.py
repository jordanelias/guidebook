#!/usr/bin/env python3
"""
scripts/validate_schema.py — Validate entity YAML files against Pydantic schemas.

Walks data/ directories and validates each YAML file against the appropriate
schema model. Used by CI (schema job) and session start (--quick mode).

Usage:
    python3 scripts/validate_schema.py                  # validate all
    python3 scripts/validate_schema.py --quick           # quick health check (sample 5)
    python3 scripts/validate_schema.py --dir data/specifications
    python3 scripts/validate_schema.py data/specifications/spec-0001.yaml

Exit codes:
    0 = all valid
    1 = validation failures found
    2 = configuration error
"""

import argparse
import glob
import os
import random
import sys

import yaml

# Allow importing schemas from repo root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.specification import Specification
from schemas.evidence_source import EvidenceSource
from schemas.bpc_metadata import BPCMetadata
from schemas.connection import Connection
from schemas.slug import Slug
from schemas.gap import Gap


# Registry: maps data/ subdirectory to its Pydantic model
ENTITY_REGISTRY = {
    "specifications": Specification,
    "sources": EvidenceSource,
    "bpc-metadata": BPCMetadata,
    "connections": Connection,
    "slugs": Slug,
    "gaps": Gap,
}



def validate_file(path: str, model_class) -> list:
    """Validate a single YAML file against its model.

    Returns list of error dicts. Empty list = valid.
    """
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [{"file": path, "error": f"YAML parse error: {e}"}]
    except Exception as e:
        return [{"file": path, "error": f"File read error: {e}"}]

    if data is None:
        return [{"file": path, "error": "Empty file"}]

    try:
        model_class.model_validate(data)
    except Exception as e:
        errors.append({"file": path, "error": str(e)})

    return errors


def find_entity_files(base_dir: str = "data") -> list:
    """Find all YAML entity files and their model classes.

    Returns list of (path, model_class) tuples.
    """
    results = []
    if not os.path.isdir(base_dir):
        return results

    for subdir, model_class in ENTITY_REGISTRY.items():
        entity_dir = os.path.join(base_dir, subdir)
        if not os.path.isdir(entity_dir):
            continue
        for path in sorted(glob.glob(os.path.join(entity_dir, "*.yaml"))):
            results.append((path, model_class))
        for path in sorted(glob.glob(os.path.join(entity_dir, "*.yml"))):
            results.append((path, model_class))

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Validate guidebook entity YAML against Pydantic schemas"
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Specific files to validate (if omitted, validates all in data/)",
    )
    parser.add_argument(
        "--dir",
        help="Validate all files in a specific data/ subdirectory",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick mode: validate a random sample of 5 files per entity type",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print each file as it's validated",
    )
    parser.add_argument(
        "--cross-check",
        action="store_true",
        help="Run cross-entity referential integrity checks after validation",
    )
    args = parser.parse_args()

    # Determine files to validate
    if args.files:
        # Specific files — infer model from path
        file_list = []
        for f in args.files:
            matched = False
            for subdir, model_class in ENTITY_REGISTRY.items():
                if subdir in f:
                    file_list.append((f, model_class))
                    matched = True
                    break
            if not matched:
                print(f"WARNING: Cannot determine entity type for {f}", file=sys.stderr)
                # Default to Specification
                file_list.append((f, Specification))
    elif args.dir:
        # Specific directory
        entity_dir = args.dir
        subdir_name = os.path.basename(entity_dir)
        model_class = ENTITY_REGISTRY.get(subdir_name)
        if not model_class:
            print(f"ERROR: Unknown entity type '{subdir_name}'", file=sys.stderr)
            print(f"Known types: {list(ENTITY_REGISTRY.keys())}", file=sys.stderr)
            return 2
        file_list = [
            (p, model_class)
            for p in sorted(glob.glob(os.path.join(entity_dir, "*.yaml")))
        ]
    else:
        file_list = find_entity_files()

    if not file_list:
        print("No entity files found to validate.")
        return 0

    # Quick mode: sample
    if args.quick and len(file_list) > 5:
        file_list = random.sample(file_list, min(5, len(file_list)))
        print(f"Quick mode: validating {len(file_list)} sampled files")

    # Validate
    total = 0
    failed = 0
    all_errors = []

    for path, model_class in file_list:
        total += 1
        if args.verbose:
            print(f"  Validating: {path}")
        errors = validate_file(path, model_class)
        if errors:
            failed += 1
            all_errors.extend(errors)

    # Report
    print(f"\nSchema validation: {total} files checked, "
          f"{total - failed} passed, {failed} failed")

    if all_errors:
        print("\nErrors:")
        for e in all_errors:
            print(f"  {e['file']}: {e['error'][:200]}")
        return 1

    # Cross-entity referential integrity
    if args.cross_check:
        cross_errors = run_cross_checks("data")
        if cross_errors:
            print(f"\nCross-entity integrity: {len(cross_errors)} issues")
            for ce in cross_errors[:20]:
                print(f"  {ce}")
            if len(cross_errors) > 20:
                print(f"  ... and {len(cross_errors) - 20} more")
            return 1
        else:
            print("Cross-entity integrity: all checks passed")

    return 0


def run_cross_checks(base_dir: str = "data") -> list:
    """Run cross-entity referential integrity checks.

    Returns list of error strings. Empty = all pass.
    """
    errors = []

    # Load indices
    slug_names = _load_field_set(base_dir, "slugs", "slug")
    source_ref_ids = _load_field_set(base_dir, "sources", "ref_id")
    con_ids = _load_field_set(base_dir, "connections", "con_id")
    bpc_slugs = _load_field_set(base_dir, "bpc-metadata", "slug")
    topic_dirs = _load_field_set(base_dir, "bpc-metadata", "topic_directory")

    # Check 1: Specification.bpc_source_slug → Slug or BPC metadata
    known_slugs = slug_names | bpc_slugs
    spec_dir = os.path.join(base_dir, "specifications")
    if os.path.isdir(spec_dir):
        for f in glob.glob(os.path.join(spec_dir, "*.yaml")):
            with open(f) as fh:
                d = yaml.safe_load(fh)
            bpc_slug = d.get("bpc_source_slug", "")
            if bpc_slug and bpc_slug not in known_slugs:
                # Population-level slugs (MOB, VIS, etc.) won't match — skip
                if not bpc_slug.isupper() and len(bpc_slug) > 3:
                    errors.append(
                        f"SPEC {d.get('spec_id')}: bpc_source_slug '{bpc_slug}' "
                        f"not found in slugs or bpc-metadata"
                    )

    # Check 2: Connection.filed_in → topic directory
    conn_dir = os.path.join(base_dir, "connections")
    if os.path.isdir(conn_dir) and topic_dirs:
        for f in glob.glob(os.path.join(conn_dir, "*.yaml")):
            with open(f) as fh:
                d = yaml.safe_load(fh)
            filed = d.get("filed_in", "")
            if filed and filed not in topic_dirs and filed not in (
                "cross-cutting", "_frozen", "population-general"
            ):
                errors.append(
                    f"CON {d.get('con_id')}: filed_in '{filed}' "
                    f"not a known topic directory"
                )

    # Check 3: BPCMetadata.slug → Slug registry
    bpc_dir = os.path.join(base_dir, "bpc-metadata")
    if os.path.isdir(bpc_dir) and slug_names:
        for f in glob.glob(os.path.join(bpc_dir, "*.yaml")):
            with open(f) as fh:
                d = yaml.safe_load(fh)
            slug = d.get("slug", "")
            if slug and slug not in slug_names:
                errors.append(
                    f"BPC {slug}: not found in slug registry"
                )

    return errors


def _load_field_set(base_dir: str, subdir: str, field: str) -> set:
    """Load a set of values for a specific field from all YAML in a subdir."""
    result = set()
    entity_dir = os.path.join(base_dir, subdir)
    if not os.path.isdir(entity_dir):
        return result
    for f in glob.glob(os.path.join(entity_dir, "*.yaml")):
        with open(f) as fh:
            d = yaml.safe_load(fh)
        if d and field in d:
            result.add(d[field])
    return result


if __name__ == "__main__":
    sys.exit(main())
