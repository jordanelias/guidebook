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
import sqlite3
import sys

import yaml

# Allow importing schemas from repo root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# (No entity model is imported: ENTITY_REGISTRY is empty as of 2026-09-01.
#  schemas/jurisdictional_value.py still exists and is still covered by
#  validate_pydantic_schemas; only this caller's reference is removed.)


# Registry: maps data/ subdirectory to its Pydantic model.
#
# CORRECTED 2026-08-01. This registry previously named six subdirectories —
# specifications, sources, bpc-metadata, connections, slugs, gaps — and NOT ONE OF
# THEM EXISTS under data/. find_entity_files() therefore returned [], main()
# short-circuited on "No entity files found to validate.", and the check exited 0.
# It is registered BLOCKING. So the entity-schema gate has reported green, for its
# whole life, while examining nothing: the most expensive kind of defect, because
# it is counted as coverage.
#
# data/ actually contains: adversarial_use/, decisions/, doctrine_recheck/,
# jurisdictional_values/. Three of those already have validators —
# audit_adversarial_use.py, decision_capture.py and doctrine_recheck.py — so
# duplicating them here would add a second opinion, not coverage. jurisdictional_values
# is the one corpus with a real DB counterpart and no validator at all, which is
# why it is the one wired up.
# SWEPT 2026-09-01. jurisdictional_values was the sole registered entity and its
# YAML corpus moved to _archived/data/jurisdictional_values/ under the owner ruling
# of that date (base + research only; the table is item-keyed and item codes must
# not exist). Rule 4: a removal is not done until the callers are swept, and this
# registry is a caller. The entry is removed rather than left pointing at a path
# that no longer exists, which is the exact stale-registry condition the block at
# the bottom of main() was written to catch.
#
# The registry is now legitimately EMPTY, which is a different state from "names
# directories that do not exist" and must not be reported as the same fault.
ENTITY_REGISTRY = {}



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
                # Was `file_list.append((f, Specification))` — a fallback to a model
                # that is no longer imported, so this branch would have raised
                # NameError. An unrecognised path is a caller error; say so.
                print(f"ERROR: cannot determine entity type for {f}. "
                      f"Known types: {list(ENTITY_REGISTRY)}", file=sys.stderr)
                return 2
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
        # Exit 2, not 0. Finding nothing to validate is a configuration fault —
        # this script returned 0 here for its whole life while ENTITY_REGISTRY
        # named six directories that do not exist, so a BLOCKING gate reported
        # green having examined nothing. The runner's vacuity guard (min_items in
        # check-registry.yaml) catches this independently; the non-zero exit means
        # a direct invocation says so too.
        if ENTITY_REGISTRY:
            print("EXAMINED: 0 entity file(s)")
            # A registry naming directories that do not exist. THIS is the original
            # defect: this script returned 0 here for its whole life while
            # ENTITY_REGISTRY named six missing paths, so a BLOCKING gate reported
            # green having examined nothing.
            print("No entity files found to validate — ENTITY_REGISTRY names no "
                  "directory that exists under data/. This is a configuration fault, "
                  "not a pass.")
            return 2
        # Legitimately EMPTY registry: no entity type is declared at all, so there is
        # nothing to validate and nothing is concealed. A different state from the
        # fault above and it must not be reported as the same one.
        #
        # FIXED 2026-09-02. This branch used to `return 0` right here, which fired
        # BEFORE the --cross-check dispatch below and made validate_schema_cross_check
        # structurally unreachable: it could never run whatever it would have found.
        # Introduced 2026-09-01 while fixing a different vacuity and caught by the
        # adversarial pass the next day. Fall through instead, so the cross-check still
        # gets its chance; file_list is empty, so the validation loop is a no-op.
        print("ENTITY_REGISTRY declares no entity type, so there is no YAML entity "
              "corpus to validate. This is an empty scope, not a configuration fault. "
              "Register a type here when one exists.")

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

    # Report. The EXAMINED line is emitted ONCE, after the cross-check, so it states
    # what the whole check looked at.
    cross_errors, cross_examined = [], 0
    if args.cross_check:
        cross_errors, cross_examined = run_cross_checks("data")
    print(f"\nEXAMINED: {total + cross_examined} subject(s) "
          f"({total} entity file(s), {cross_examined} cross-check subject(s))")
    print(f"Schema validation: {total} files checked, "
          f"{total - failed} passed, {failed} failed")

    if all_errors:
        print("\nErrors:")
        for e in all_errors:
            print(f"  {e['file']}: {e['error'][:200]}")
        return 1

    # Cross-entity referential integrity (already run above so its count reaches EXAMINED)
    if args.cross_check:
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
    """Reconcile research_code_leads against the archive it was restored from.

    REPOINTED 2026-09-02, and this is the first time the function has had a subject.

    Its 2026-08-01 rewrite reconciled data/jurisdictional_values/ against the
    `jurisdictional_values` table on (item_code, jurisdiction, standard_name). Both
    sides of that pairing are gone: the owner's 2026-09-01 ruling emptied the table by
    deleting the item layer it was keyed to, and the YAML moved to _archived/ on
    2026-09-02. The function was returning "not found — cross-check cannot run", which
    is not a check.

    It was ALSO unreachable between 2026-09-01 and 2026-09-02: an empty-registry
    `return 0` fired ahead of its dispatch, so nothing would have run even had it had a
    subject. That is fixed above.

    WHAT IT CHECKS NOW. Owner ruling D-0185 restored the archived corpus as
    research_code_leads, collapsing 109 item-keyed records onto their 83 distinct
    (jurisdiction, standard_name) leads. That relationship is a real, checkable
    invariant: every lead in the archive must be in the table, and the table must
    invent none. It would catch a lead silently dropped by a later migration, and it
    is the only thing standing between the restore and quiet erosion.

    The archive is the SOURCE here, not a second home: it is frozen content under
    _archived/, and the table is the live record. Comparing them is provenance, not
    the dual-write rule 5 forbids.
    """
    errors = []
    arch = os.path.join("_archived", "data", "jurisdictional_values")
    if not os.path.isdir(arch):
        return [f"{arch} not found — the restore provenance cannot be checked"]

    db_path = os.environ.get("GUIDEBOOK_DB_PATH",
                             os.path.join(base_dir, "guidebook.db"))
    if not os.path.exists(db_path):
        return [f"DB not found at {db_path} — cross-check cannot run"]

    def key(jurisdiction, standard_name):
        return (str(jurisdiction or "").strip(), str(standard_name or "").strip())

    archived = set()
    for path in sorted(glob.glob(os.path.join(arch, "*.yaml"))):
        with open(path, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh) or {}
        for rec in doc.get("records", []) or []:
            archived.add(key(rec.get("jurisdiction"), rec.get("standard_name")))

    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        live = {key(j, n) for j, n in
                con.execute("SELECT jurisdiction, standard_name FROM research_code_leads")}
    finally:
        con.close()

    missing = archived - live
    invented = live - archived
    for j, n in sorted(missing)[:20]:
        errors.append(f"in the archive, absent from research_code_leads: {j} / {n}")
    for j, n in sorted(invented)[:20]:
        errors.append(f"in research_code_leads, absent from the archive: {j} / {n}")

    # Returns the count rather than printing its own EXAMINED line. run_checks.py's
    # vacuity guard uses EXAMINED_RE.search(), which takes the FIRST match, and
    # run_checks' own comment states that "EXAMINED: <n> is a WHOLE-CHECK contract, not
    # a per-subject one". Two EXAMINED lines in one run meant the guard read the entity
    # count (0) and never saw the 83 leads this actually reconciled — reporting the
    # check vacuous while it was doing real work. One line, printed by main().
    print(f"Cross-entity provenance: {len(archived)} archived lead(s), {len(live)} live")
    return errors, len(archived | live)


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
