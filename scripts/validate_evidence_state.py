#!/usr/bin/env python3
"""
scripts/validate_evidence_state.py — Validate evidence state records.

Per governance/evidence-methodology.md (A6), §2 (cell states), §3 (convergence),
and §1.4/§1.6/§1.7 (scale + directness); decision D-D. Stage 2.4 wires this to
the real DB tables built in Stage 2.3 (evidence_cell_state +
convergence_assessment) — the canonical source under DB-as-truth — in addition
to the original YAML-file path.

DB validation (default; the cell-state machine):
- pending cells must reference a gap that exists in the `gaps` table
  (DB-as-truth; supersedes the gap_register.md scrape)
- provisional cells must carry the confidence flag (dimensions present/absent +
  synthesis basis)
- not_applicable cells must carry a rationale
- stated/provisional cells must have a convergence assessment
- scale-aware: design_scale ∈ {universal, population, person}
- directness-aware (§1.7): a discounted source cannot also anchor the claim;
  convergent needs ≥2 evidence axes, single_axis ≤1; divergent needs
  rationale + synthesis_approach

YAML validation (when explicit files are given, or for Co-1 source fields):
- EvidenceStateRecord / EvidenceSource Pydantic validation
- A5 Co-1 verification-status rules

Usage:
    python3 scripts/validate_evidence_state.py                  # validate DB cell-state + YAML sources
    python3 scripts/validate_evidence_state.py --db path/to.db  # explicit DB
    python3 scripts/validate_evidence_state.py --sources-only    # Co-1 fields only
    python3 scripts/validate_evidence_state.py data/evidence-states/es-0001.yaml

Exit codes:
    0 = all valid
    1 = validation failures found
    2 = configuration error
"""

import argparse
import glob
import json
import os
import sqlite3
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.evidence_state import EvidenceStateRecord
from schemas.evidence_source import EvidenceSource
from schemas.enums import EvidenceType, VerificationStatus
from schemas.directness import ALL_SCALES


def validate_file(path: str, model_class) -> list:
    """Validate a single YAML file. Returns list of error strings."""
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"]

    if data is None:
        return ["File is empty"]

    try:
        model_class.model_validate(data)
    except Exception as e:
        errors.append(str(e))

    return errors


def validate_source_co1_fields(path: str) -> list:
    """Additional Co-1 field validation beyond Pydantic schema.

    Checks A5 §6.3 verification-status rules for Co-1 sources.
    """
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception:
        return []  # Let the main validator catch parse errors

    if not data:
        return []

    et = data.get("evidence_type", "")
    if et != "co1":
        return []

    # Co-1 source: check verification status
    vs = data.get("verification_status")
    if vs in ("UNVERIFIED-CLOSED", "CLOSED-DELETED"):
        errors.append(
            f"Co-1 source {data.get('ref_id', '?')} has "
            f"verification_status={vs} — cells citing this source "
            f"as sole Co-1 evidence must downgrade to pending (A6 §2.8)"
        )

    # Co-1 source: tier must be 1
    tier = data.get("tier")
    if tier is not None and tier != 1:
        errors.append(
            f"Co-1 source {data.get('ref_id', '?')} has tier={tier} "
            f"but Co-1 must be tier=1 (co-primary per T-03)"
        )

    return errors


def validate_evidence_state_cross_refs(path: str, gap_ids: set) -> list:
    """Check cross-references for evidence state records."""
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception:
        return []

    if not data:
        return []

    state = data.get("state", "")
    gap_id = data.get("gap_register_id")

    if state == "pending" and gap_id:
        if gap_ids and gap_id not in gap_ids:
            errors.append(
                f"gap_register_id '{gap_id}' not found in gap_register.md"
            )

    return errors


def load_gap_ids(repo_root: str) -> set:
    """Extract GAP-NNN IDs from gap_register.md."""
    import re

    gap_path = os.path.join(repo_root, "gap_register.md")
    if not os.path.exists(gap_path):
        return set()

    ids = set()
    with open(gap_path, "r", encoding="utf-8") as f:
        for line in f:
            for m in re.finditer(r"GAP-\d{3,4}", line):
                ids.add(m.group())
    return ids


def load_gap_ids_db(conn) -> set:
    """Valid gap ids from the DB gaps table (DB-as-truth; supersedes gap_register.md)."""
    return {r[0] for r in conn.execute("SELECT gap_id FROM gaps")}


def _jlist(val):
    """Parse a JSON-array text column to a list. [] for NULL/empty; a '<...>'
    sentinel element when the column is present but not a JSON array."""
    if val is None or val == "":
        return []
    try:
        v = json.loads(val)
    except (json.JSONDecodeError, TypeError):
        return ["<malformed-json>"]
    return v if isinstance(v, list) else ["<not-a-json-array>"]


def _bad_json(lst) -> bool:
    return any(isinstance(x, str) and x.startswith("<") and x.endswith(">") for x in lst)


def _ref_tiers(conn, ref_ids):
    """Look up evidence_sources.tier for a list of ref_ids. Returns {ref_id: tier}."""
    if not ref_ids:
        return {}
    placeholders = ",".join("?" for _ in ref_ids)
    rows = conn.execute(
        f"SELECT ref_id, tier FROM evidence_sources WHERE ref_id IN ({placeholders})",
        list(ref_ids),
    )
    return {r[0]: r[1] for r in rows}


def validate_cell_states_db(conn, gap_ids: set):
    """Validate evidence_cell_state rows against the §2 state machine, scale-aware.
    Mirrors schemas.evidence_state.EvidenceStateRecord's state-field rules at the
    data layer, plus pending⇒gap-link against the gaps table. Returns (errors, n).

    Also enforces (per decisions/DR-2026-07-12-evidence-cell-state-schema-reconciliation.md
    and decisions/DR-2026-07-12-tier3-stated-threshold.md, both PROPOSED pending owner
    ratification -- this validator implements what ratification would require, it does
    not itself constitute ratification):
    - anti-hallucination: stated/provisional cells must cite governing_refs (non-empty,
      well-formed JSON array) -- a determination cannot exist without the sources that
      establish it.
    - code_floor_only cells (Tier-6-only evidence, best-practices-assessment-system.md
      §3's hard rule) can never be 'stated'.
    - Tier-3-alone (single_axis convergence, all clinical_sources resolve to tier=3)
      cannot be 'stated' -- tier-system.md's "rarely the sole basis" characterization
      of Tier 3.
    """
    errors = []
    cols = ("cell_id,item_code,population_code,state,design_scale,convergence_id,"
            "confidence_dimensions_present,confidence_dimensions_absent,"
            "confidence_synthesis_basis,gap_register_id,not_applicable_rationale,"
            "governing_refs,code_floor_only")
    # G1b (unification DR, ACCEPTED 2026-07-13): the T4-6-only flag is
    # migration-027 schema; select it where present, marker-check `tier_basis`
    # everywhere (pre-027 DBs stay validatable).
    have_rso = any(r[1] == "regulatory_stratum_only"
                   for r in conn.execute("PRAGMA table_info(evidence_cell_state)"))
    cols += ",tier_basis" + (",regulatory_stratum_only" if have_rso else "")
    n = 0
    for row in conn.execute(f"SELECT {cols} FROM evidence_cell_state"):
        (cell_id, item_code, pop, state, design_scale, conv_id,
         cdp, cda, csb, gap_id, na_rat,
         governing_refs, code_floor_only, tier_basis) = row[:14]
        rso = row[14] if have_rso else 0
        n += 1
        tag = f"cell {cell_id} ({item_code}×{pop})"
        # scale-aware: design_scale vocabulary (§1.4/§1.6)
        if design_scale is not None and design_scale not in ALL_SCALES:
            errors.append(f"{tag}: design_scale {design_scale!r} not in {sorted(ALL_SCALES)}")
        # state-dependent required fields
        if state == "pending":
            if not gap_id:
                errors.append(f"{tag}: state 'pending' requires gap_register_id (§2.4)")
            elif gap_ids and gap_id not in gap_ids:
                errors.append(f"{tag}: gap_register_id {gap_id!r} not in gaps table")
        elif state == "provisional":
            if not csb or not _jlist(cdp) or not _jlist(cda):
                errors.append(f"{tag}: state 'provisional' requires confidence flag — "
                              f"dimensions_present, dimensions_absent, synthesis_basis (§2.3)")
            if conv_id is None:
                errors.append(f"{tag}: state 'provisional' requires a convergence assessment")
        elif state == "not_applicable":
            if not na_rat:
                errors.append(f"{tag}: state 'not_applicable' requires not_applicable_rationale (§2.5)")
        elif state == "stated":
            if conv_id is None:
                errors.append(f"{tag}: state 'stated' requires a convergence assessment (≥1 source axis, §2.2)")
            if code_floor_only:
                errors.append(f"{tag}: state 'stated' but code_floor_only=1 — a Tier-6-only "
                               f"cell can never be 'stated' (best-practices-assessment-system.md §3)")
            if rso == 1 or (tier_basis or "").endswith("(regulatory_stratum_only)"):
                errors.append(f"{tag}: state 'stated' but the cell is regulatory-stratum-only "
                               f"(T4-6 basis) — never 'stated' (G1b, unification DR ACCEPTED)")

        # anti-hallucination gate (DR-2026-07-12-evidence-cell-state-schema-reconciliation.md):
        # stated/provisional cells must cite the sources that establish them
        if state in ("stated", "provisional"):
            refs = _jlist(governing_refs)
            if not refs or _bad_json(refs):
                errors.append(f"{tag}: state {state!r} requires non-empty governing_refs "
                               f"(anti-hallucination gate)")

        # Tier-3-alone stated threshold (DR-2026-07-12-tier3-stated-threshold.md)
        if state == "stated" and conv_id is not None:
            conv_row = conn.execute(
                "SELECT status, clinical_sources, co1_sources, co2_sources "
                "FROM convergence_assessment WHERE convergence_id = ?",
                (conv_id,),
            ).fetchone()
            if conv_row:
                status, clinical, co1, co2 = conv_row
                if status == "single_axis":
                    clinical_refs = _jlist(clinical)
                    co1_refs, co2_refs = _jlist(co1), _jlist(co2)
                    if clinical_refs and not co1_refs and not co2_refs and not _bad_json(clinical_refs):
                        tiers = _ref_tiers(conn, clinical_refs)
                        if tiers and all(t == 3 for t in tiers.values()):
                            errors.append(
                                f"{tag}: state 'stated' but single-axis convergence is "
                                f"Tier-3-alone ({sorted(tiers)}) — Tier 3 is 'rarely the "
                                f"sole basis' (tier-system.md); must be 'provisional'"
                            )
    return errors, n


def validate_convergence_db(conn):
    """Validate convergence_assessment rows against §3.2 + the §1.7 directness
    conditioning. Returns (errors, n)."""
    errors = []
    cols = ("convergence_id,status,clinical_sources,co1_sources,co2_sources,"
            "down_weighted_sources,discounted_sources,rationale,synthesis_approach")
    n = 0
    for (cid, status, clinical, co1, co2, downw, disc, rationale, synth) in \
            conn.execute(f"SELECT {cols} FROM convergence_assessment"):
        n += 1
        tag = f"convergence {cid}"
        clinical, co1, co2 = _jlist(clinical), _jlist(co1), _jlist(co2)
        downw, disc = _jlist(downw), _jlist(disc)
        anchoring = set(clinical) | set(co1) | set(co2)
        axes = sum(1 for lst in (clinical, co1, co2) if lst and not _bad_json(lst))
        # rationale / axis requirements (§3.2)
        if status == "divergent":
            if not rationale:
                errors.append(f"{tag}: status 'divergent' requires rationale")
            if not synth:
                errors.append(f"{tag}: status 'divergent' requires synthesis_approach")
        elif status == "single_axis":
            if not rationale:
                errors.append(f"{tag}: status 'single_axis' requires rationale (name the axis)")
            if axes > 1:
                errors.append(f"{tag}: status 'single_axis' but {axes} evidence axes present")
        elif status == "convergent":
            if axes < 2:
                errors.append(f"{tag}: status 'convergent' requires ≥2 evidence axes, found {axes}")
        # directness consistency (§1.7): a discounted source cannot also anchor the claim
        overlap = set(disc) & anchoring
        if overlap:
            errors.append(f"{tag}: discounted_sources also listed as anchoring: {sorted(overlap)}")
        # malformed JSON columns
        for name, lst in [("clinical_sources", clinical), ("co1_sources", co1),
                          ("co2_sources", co2), ("down_weighted_sources", downw),
                          ("discounted_sources", disc)]:
            if _bad_json(lst):
                errors.append(f"{tag}: {name} is not a valid JSON array")
    return errors, n


def validate_db(db_path: str):
    """Validate the cell-state machine in the DB. Returns (errors, n_cells, n_conv)."""
    if not os.path.exists(db_path):
        return [f"DB not found: {db_path}"], 0, 0
    conn = sqlite3.connect(db_path)
    try:
        tabs = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        missing = {"evidence_cell_state", "convergence_assessment"} - tabs
        if missing:
            return [f"tables absent (run migration 024): {sorted(missing)}"], 0, 0
        gap_ids = load_gap_ids_db(conn)
        cell_errors, n_cells = validate_cell_states_db(conn, gap_ids)
        conv_errors, n_conv = validate_convergence_db(conn)
        return cell_errors + conv_errors, n_cells, n_conv
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Validate evidence state and source records"
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Specific files to validate",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Sample 5 files from each directory",
    )
    parser.add_argument(
        "--sources-only",
        action="store_true",
        help="Only validate EvidenceSource Co-1 fields",
    )
    parser.add_argument(
        "--states-only",
        action="store_true",
        help="Only validate EvidenceStateRecord files",
    )
    parser.add_argument(
        "--db",
        default=None,
        help="Path to guidebook.db (default: $GUIDEBOOK_DB_PATH or data/guidebook.db). "
             "The cell-state machine (evidence_cell_state + convergence_assessment) is "
             "validated from the DB — the canonical source — unless explicit files are given.",
    )
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gap_ids = load_gap_ids(repo_root)

    total_errors = 0
    total_files = 0
    total_warnings = 0
    db_validated = False

    # Determine what to validate
    validate_sources = not args.states_only
    validate_states = not args.sources_only

    if args.files:
        # Validate specific files
        for path in args.files:
            if not os.path.exists(path):
                print(f"  NOT FOUND: {path}", file=sys.stderr)
                total_errors += 1
                continue

            total_files += 1
            # Detect type by directory or content
            if "sources" in path:
                errors = validate_file(path, EvidenceSource)
                errors.extend(validate_source_co1_fields(path))
            else:
                errors = validate_file(path, EvidenceStateRecord)
                errors.extend(
                    validate_evidence_state_cross_refs(path, gap_ids)
                )

            if errors:
                total_errors += len(errors)
                print(f"FAIL {path}:")
                for e in errors:
                    print(f"  {e}")
    else:
        # DB cell-state machine is the canonical source (DB-as-truth). Validate it
        # first; the YAML scans below remain for any materialized file artifacts.
        if validate_states:
            db_path = (args.db or os.environ.get("GUIDEBOOK_DB_PATH")
                       or os.path.join(repo_root, "data", "guidebook.db"))
            db_errors, n_cells, n_conv = validate_db(db_path)
            db_validated = not (db_errors and (db_errors[0].startswith("DB not found")
                                               or db_errors[0].startswith("tables absent")))
            total_files += n_cells + n_conv
            if db_errors:
                total_errors += len(db_errors)
                print(f"FAIL evidence_cell_state machine ({os.path.basename(db_path)}):")
                for e in db_errors:
                    print(f"  {e}")
            else:
                print(f"OK cell-state machine: {n_cells} cells, {n_conv} convergence rows "
                      f"validated from {os.path.basename(db_path)}", file=sys.stderr)

        # Scan data directories
        source_dir = os.path.join(repo_root, "data", "sources")
        state_dir = os.path.join(repo_root, "data", "evidence-states")

        if validate_sources and os.path.isdir(source_dir):
            files = sorted(glob.glob(os.path.join(source_dir, "*.yaml")))
            if args.quick:
                import random
                files = random.sample(files, min(5, len(files)))

            for path in files:
                total_files += 1
                errors = validate_file(path, EvidenceSource)
                errors.extend(validate_source_co1_fields(path))
                if errors:
                    total_errors += len(errors)
                    print(f"FAIL {os.path.basename(path)}:")
                    for e in errors:
                        print(f"  {e}")

        if validate_states and os.path.isdir(state_dir):
            files = sorted(glob.glob(os.path.join(state_dir, "*.yaml")))
            if args.quick:
                import random
                files = random.sample(files, min(5, len(files)))

            for path in files:
                total_files += 1
                errors = validate_file(path, EvidenceStateRecord)
                errors.extend(
                    validate_evidence_state_cross_refs(path, gap_ids)
                )
                if errors:
                    total_errors += len(errors)
                    print(f"FAIL {os.path.basename(path)}:")
                    for e in errors:
                        print(f"  {e}")

    # Summary
    if total_files == 0 and not db_validated:
        print(
            "No data files found. "
            "data/sources/ and data/evidence-states/ directories do not exist yet.",
            file=sys.stderr,
        )
        return 0  # Not an error — data hasn't been materialized

    status = "PASS" if total_errors == 0 else "FAIL"
    print(
        f"\n{status}: {total_files} records checked, "
        f"{total_errors} errors, {total_warnings} warnings",
        file=sys.stderr,
    )
    return 1 if total_errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
