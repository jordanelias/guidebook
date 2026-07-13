#!/usr/bin/env python3
"""
scripts/audit/validate_pydantic_schemas.py — Pydantic <-> SQLite field-parity audit.

Per audits/data-integrity-verification-plan.md §1.3 (F-15: "Pydantic<->SQLite
drift is real AND unguarded"). For each schemas/*.py Pydantic model with a
declared live-table mapping (MODEL_TABLE_MAP below), compares its fields
against the corresponding table's PRAGMA table_info() columns and reports:

  (a) fields declared in the Pydantic model but absent from the DB table
  (b) columns present in the DB table but absent from the Pydantic model
  (c) fields/columns with plausibly incompatible basic types

This is a REPORTING tool, not a gate (Level 2 per the plan; "ship at level 2
first (manual CLI)... promote to level 4 once direction-of-drift policy is
documented" -- that per-model accept/reject policy is a separate, future
decision this script does not make). Exit code is always 0 unless run with
--strict.

MODEL_TABLE_MAP is a curated, versioned mapping (same convention as
claims_docket.py's TRIGGERS / EXTRA_RULE_IDS) -- not every schemas/*.py model
has a live table (many are output/analysis shapes, not DB entities: doctrine,
doctrine_recheck, economics, fdr_specialist, question, throughline, temporal,
specialist, case_study, adversarial_use). Two models are deliberately *not*
mapped despite having plausible name matches, because the underlying concept
is a confirmed-absent phantom table, not a drift case:
  - schemas.room.Room / RoomItemEntry / DARProvision / RoomConflict: no `room`
    table exists in the live schema at all (see working/pilot/PILOT-MANIFEST.md
    "Deliberately not used: schemas/room.py -- no room data model exists").
  - schemas.specification.Specification: no `specification` table exists (see
    decisions/DR-2026-07-12-website-architecture-lock.md Context section --
    confirmed absent, page-templates.md's SQL against it never worked).
Tables with no corresponding model at all are listed separately (informational
only, same "not a failure" framing as schema_reference_drift_audit.py's
unreferenced-tables check) -- some are populated by migrations/jobs only and
were never meant to round-trip through a Pydantic model.

Usage:
    python3 scripts/audit/validate_pydantic_schemas.py [--db PATH] [--strict]
    python3 scripts/audit/validate_pydantic_schemas.py --selftest
"""
import argparse
import importlib
import inspect
import os
import pkgutil
import sqlite3
import sys
from pathlib import Path

import pydantic

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))
DEFAULT_DB = REPO_ROOT / "data" / "guidebook.db"

# model qualified name ("<module>.<ClassName>") -> live table name.
# Only models with a confident, unambiguous live-table match are listed.
MODEL_TABLE_MAP = {
    "bpc_metadata.BPCMetadata": "bpc_metadata",
    "connection.Connection": "connections",
    "conflict.Conflict": "conflicts",
    "decision.Decision": "decisions",
    "evidence_source.EvidenceSource": "evidence_sources",
    "evidence_state.ConvergenceAssessment": "convergence_assessment",
    "evidence_state.EvidenceStateRecord": "evidence_cell_state",
    "gap.Gap": "gaps",
    "item.Item": "items",
    "population.Population": "populations",
    "population_links.CitationPopulationLink": "citation_population_links",
    "population_links.ProbePopulationLink": "probe_population_links",
    "population_links.ExtractionPopulationLink": "extraction_population_links",
    "slug.Slug": "slugs",
    "source_value_extraction.SourceValueExtraction": "source_value_extractions",
}

# Basic type-compatibility groups. A field/column pair is flagged as a
# possible type mismatch only if neither's group contains the other's group
# (conservative -- Optional/list/JSON-as-TEXT wrapping is common and not
# itself a bug).
TEXT_LIKE = {"str", "TEXT", "list", "dict"}
NUM_LIKE = {"int", "REAL", "INTEGER", "float"}


def discover_models():
    """Yield (qualname, model_cls) for every Pydantic BaseModel subclass
    defined directly in schemas/*.py (not imported from elsewhere)."""
    import schemas

    for modinfo in pkgutil.iter_modules(schemas.__path__):
        try:
            mod = importlib.import_module(f"schemas.{modinfo.name}")
        except Exception as e:
            print(f"  [skip] schemas.{modinfo.name}: import error: {e}", file=sys.stderr)
            continue
        for name, obj in vars(mod).items():
            if (
                inspect.isclass(obj)
                and issubclass(obj, pydantic.BaseModel)
                and obj.__module__ == mod.__name__
            ):
                yield f"{modinfo.name}.{name}", obj


def python_type_group(annotation) -> str:
    s = str(annotation)
    if "int" in s and "str" not in s:
        return "int"
    if "float" in s:
        return "float"
    if "list" in s or "List" in s:
        return "list"
    if "dict" in s or "Dict" in s:
        return "dict"
    return "str"


def sqlite_type_group(decl_type: str) -> str:
    t = (decl_type or "").upper()
    if "INT" in t:
        return "INTEGER"
    if "REAL" in t or "FLOA" in t or "DOUB" in t:
        return "REAL"
    return "TEXT"


def compatible(py_group: str, sql_group: str) -> bool:
    if py_group in NUM_LIKE and sql_group in NUM_LIKE:
        return True
    if py_group in TEXT_LIKE and sql_group in TEXT_LIKE:
        return True
    return False


def check_pair(model_cls, table: str, conn) -> dict:
    """Return {'pydantic_only': [...], 'db_only': [...], 'type_mismatch': [(f, pytype, dbtype)]}."""
    cols = {r[1]: r[2] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}
    fields = model_cls.model_fields
    pydantic_only = sorted(set(fields) - set(cols))
    db_only = sorted(set(cols) - set(fields))
    type_mismatch = []
    for name in sorted(set(fields) & set(cols)):
        py_group = python_type_group(fields[name].annotation)
        sql_group = sqlite_type_group(cols[name])
        if not compatible(py_group, sql_group):
            type_mismatch.append((name, py_group, sql_group))
    return {"pydantic_only": pydantic_only, "db_only": db_only, "type_mismatch": type_mismatch}


def run(db_path: Path, strict: bool) -> int:
    conn = sqlite3.connect(str(db_path))
    live_tables = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()}

    models = dict(discover_models())
    print(f"Discovered {len(models)} Pydantic models across schemas/*.py; "
          f"{len(MODEL_TABLE_MAP)} mapped to a live table.\n")

    total_drift = 0
    for qualname, table in sorted(MODEL_TABLE_MAP.items()):
        if qualname not in models:
            print(f"[ERROR] {qualname} -> {table}: model not found (mapping stale?)")
            total_drift += 1
            continue
        if table not in live_tables:
            print(f"[ERROR] {qualname} -> {table}: table not found in {db_path.name} (mapping stale?)")
            total_drift += 1
            continue
        result = check_pair(models[qualname], table, conn)
        n = len(result["pydantic_only"]) + len(result["db_only"]) + len(result["type_mismatch"])
        if n == 0:
            print(f"  OK    {qualname:45s} <-> {table}")
            continue
        total_drift += n
        print(f"  DRIFT {qualname:45s} <-> {table}")
        if result["pydantic_only"]:
            print(f"          Pydantic-only (not in DB): {result['pydantic_only']}")
        if result["db_only"]:
            print(f"          DB-only (not in Pydantic): {result['db_only']}")
        for f, py_t, sql_t in result["type_mismatch"]:
            print(f"          Type mismatch: {f} (Pydantic={py_t}, DB={sql_t})")

    mapped_tables = set(MODEL_TABLE_MAP.values())
    unmapped_tables = sorted(live_tables - mapped_tables)
    print(f"\n{len(unmapped_tables)} / {len(live_tables)} live tables have no mapped Pydantic model "
          f"(not a failure -- some are migration/job-populated only):")
    for t in unmapped_tables:
        print(f"    {t}")

    conn.close()
    print(f"\n{'='*60}\nTotal drift findings: {total_drift} "
          f"(informational -- per-table accept/reject policy is separate future work)")
    if strict and total_drift:
        return 1
    return 0


def selftest() -> int:
    """Mutation discipline: build a synthetic model + synthetic table with
    deliberate drift in both directions and a type mismatch, confirm the
    checker fires on all three; confirm it stays quiet on an exact match."""
    import tempfile
    from pydantic import BaseModel

    ok = True

    class DriftModel(BaseModel):
        keep: str
        pydantic_only_field: str

    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    conn = sqlite3.connect(tmp.name)
    conn.execute("CREATE TABLE drift_table (keep TEXT, db_only_col INTEGER)")
    conn.commit()

    result = check_pair(DriftModel, "drift_table", conn)
    fired_pydantic_only = result["pydantic_only"] == ["pydantic_only_field"]
    fired_db_only = result["db_only"] == ["db_only_col"]
    print(f"{'FIRED' if fired_pydantic_only else '**MISSED**'}: Pydantic-only field detected")
    print(f"{'FIRED' if fired_db_only else '**MISSED**'}: DB-only column detected")
    ok &= fired_pydantic_only and fired_db_only

    class TypeMismatchModel(BaseModel):
        should_be_int: str

    conn.execute("CREATE TABLE type_table (should_be_int INTEGER)")
    conn.commit()
    result2 = check_pair(TypeMismatchModel, "type_table", conn)
    fired_type = len(result2["type_mismatch"]) == 1 and result2["type_mismatch"][0][0] == "should_be_int"
    print(f"{'FIRED' if fired_type else '**MISSED**'}: type mismatch detected")
    ok &= fired_type

    class CleanModel(BaseModel):
        a: str
        b: int

    conn.execute("CREATE TABLE clean_table (a TEXT, b INTEGER)")
    conn.commit()
    result3 = check_pair(CleanModel, "clean_table", conn)
    clean_quiet = not result3["pydantic_only"] and not result3["db_only"] and not result3["type_mismatch"]
    print(f"{'PASS' if clean_quiet else '**FAIL**'}: exact-match model/table stays quiet")
    ok &= clean_quiet

    conn.close()
    os.unlink(tmp.name)
    print("SELFTEST:", "ALL FIRED" if ok else "FAILURE")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--strict", action="store_true",
                     help="exit 1 if any drift found (default: always exit 0, informational)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(selftest())
    sys.exit(run(args.db, args.strict))


if __name__ == "__main__":
    main()
