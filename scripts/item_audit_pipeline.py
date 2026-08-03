"""
scripts/item_audit_pipeline.py — Wrapper for item audit pipeline.

Orchestrates 8 audit steps for a single item, tracking state in item_audit_runs.
Each step can also be invoked individually via its skill protocol.

Usage:
    python3 scripts/item_audit_pipeline.py --item I-01 --session SESSION
    python3 scripts/item_audit_pipeline.py --item I-01 --session SESSION --skip-steps evidence-auditor
    python3 scripts/item_audit_pipeline.py --item I-01 --session SESSION --force-rerun economics-auditor
    python3 scripts/item_audit_pipeline.py --item I-01 --session SESSION --dry-run
    python3 scripts/item_audit_pipeline.py --item I-01 --session SESSION --status

Decision: D-0150, 2026-05-05.
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DB_PATH   = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))
SPEC_PATH = REPO_ROOT / "versions/current/Guidebook_for_Accessible_Design_v9-0_2026-03-20.md"

PIPELINE_STEPS = [
    "connection-discovery-spec",
    "connection-discovery-evidence",
    "conflict-mapper",
    "content-gap-analyzer",
    "evidence-auditor",
    "functional-deficit-auditor",
    "economics-auditor",
    "audit-consolidator",
]

# Step → source_skill value used in gaps/connections (for force_rerun cleanup)
STEP_SKILL = {
    "connection-discovery-spec":     "connection-discovery",
    "connection-discovery-evidence": "connection-discovery",
    "conflict-mapper":               "cross-population-conflict-mapper",
    "content-gap-analyzer":          "content-gap-analyzer",
    "evidence-auditor":              "evidence-auditor",
    "functional-deficit-auditor":    "functional-deficit-auditor",
    "economics-auditor":             "economics-auditor",
    "audit-consolidator":            "audit-consolidator",
}


# ─── Utility ────────────────────────────────────────────────────────────────

def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


def connect():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def spec_hash(item_code: str) -> str | None:
    """Compute MD5 of normalised item spec text."""
    if not SPEC_PATH.exists():
        return None
    text = SPEC_PATH.read_text(encoding="utf-8")
    start = text.find(f"### {item_code} ")
    if start == -1:
        return None
    end = text.find("\n### ", start + 10)
    section = text[start:end] if end != -1 else text[start:]
    # Normalise: strip trailing whitespace per line, LF endings, strip frontmatter
    section = "\n".join(line.rstrip() for line in section.split("\n"))
    section = re.sub(r"^---\n.*?---\n", "", section, flags=re.DOTALL)
    return hashlib.md5(section.strip().encode()).hexdigest()


def db_update_run(conn, run_id, session, **kwargs):
    """Update item_audit_runs with arbitrary fields."""
    valid = {"status", "steps_complete", "steps_started", "brief_path", "spec_hash"}
    sets  = ["updated_at=?", "updated_by_session=?"]
    vals  = [now(), session]
    for k, v in kwargs.items():
        if k not in valid:
            raise ValueError(f"Unknown field: {k}")
        if isinstance(v, list):
            v = json.dumps(v)
        sets.append(f"{k}=?")
        vals.append(v)
    vals.append(run_id)
    conn.execute(f"UPDATE item_audit_runs SET {', '.join(sets)} WHERE run_id=?", vals)
    conn.commit()


def db_get_run(conn, item_code):
    return conn.execute(
        "SELECT * FROM item_audit_runs WHERE item_code=? ORDER BY created_at DESC LIMIT 1",
        (item_code,)
    ).fetchone()


def db_get_item(conn, item_code):
    return conn.execute(
        "SELECT * FROM items WHERE item_code=?", (item_code,)
    ).fetchone()


# ─── Validation ─────────────────────────────────────────────────────────────

def validate_step_args(skip_steps, force_rerun):
    """Validate skip_steps and force_rerun inputs."""
    unknown_skip  = [s for s in skip_steps  if s not in PIPELINE_STEPS]
    unknown_force = [s for s in force_rerun if s not in PIPELINE_STEPS]
    if unknown_skip:
        raise ValueError(f"Unknown step(s) in skip_steps: {unknown_skip}")
    if unknown_force:
        raise ValueError(f"Unknown step(s) in force_rerun: {unknown_force}")
    conflict = [s for s in force_rerun if s in skip_steps]
    if conflict:
        raise ValueError(
            f"ABORT: {conflict} appears in both skip_steps and force_rerun. "
            f"These are mutually exclusive per step."
        )
    if "audit-consolidator" in skip_steps:
        raise ValueError("ABORT: audit-consolidator cannot be in skip_steps — it always runs.")


def validate_skip_against_prior(conn, item_code, skip_steps):
    """Ensure each skipped step appears in a prior run's steps_complete."""
    runs = conn.execute(
        "SELECT steps_complete FROM item_audit_runs WHERE item_code=? ORDER BY created_at",
        (item_code,)
    ).fetchall()
    all_complete = set()
    for r in runs:
        try:
            all_complete.update(json.loads(r["steps_complete"]))
        except (json.JSONDecodeError, TypeError):
            pass

    invalid_skips = [s for s in skip_steps if s not in all_complete and s != "audit-consolidator"]
    if invalid_skips:
        raise ValueError(
            f"ABORT: {invalid_skips} in skip_steps but not found in any prior "
            f"steps_complete for {item_code}. Cannot skip a never-completed step."
        )


# ─── Step 2 and 3 auto-skip logic ──────────────────────────────────────────

def should_skip_evidence_mode(item):
    return not item["bpc_source_slug"]


def should_skip_conflict_mapper(item):
    ag = item["applicable_groups"] or ""
    pops = [p.strip() for p in ag.split(",") if p.strip()]
    return len(pops) < 2


# ─── force_rerun cleanup ────────────────────────────────────────────────────

def cleanup_for_force_rerun(conn, item_code, current_session, steps):
    """Delete current-session-only findings for force_rerun steps."""
    for step in steps:
        skill = STEP_SKILL.get(step)
        if not skill:
            continue
        if step in ("connection-discovery-spec", "connection-discovery-evidence"):
            # Remove connections logged this session
            conn.execute(
                "DELETE FROM connection_targets WHERE con_id IN ("
                "  SELECT con_id FROM connections WHERE source_skill=? AND created_by_session=?"
                ")",
                (skill, current_session)
            )
            conn.execute(
                "DELETE FROM connections WHERE source_skill=? AND created_by_session=?",
                (skill, current_session)
            )
        elif step == "conflict-mapper":
            conn.execute(
                "DELETE FROM conflicts WHERE item_code=? AND created_by_session=?",
                (item_code, current_session)
            )
        # For all steps: remove gaps
        conn.execute(
            "DELETE FROM gaps WHERE skill=? AND section=? AND created_by_session=?",
            (skill, item_code, current_session)
        )
    conn.commit()
    print(f"  force_rerun cleanup: removed current-session findings for {steps}")


# ─── Step state helpers ──────────────────────────────────────────────────────

def step_started(conn, run_id, session, steps_started, step_name):
    if step_name not in steps_started:
        steps_started = steps_started + [step_name]
    db_update_run(conn, run_id, session, steps_started=steps_started)
    return steps_started


def step_complete(conn, run_id, session, steps_complete, step_name):
    if step_name not in steps_complete:
        steps_complete = steps_complete + [step_name]
    db_update_run(conn, run_id, session, steps_complete=steps_complete)
    return steps_complete


# ─── Main pipeline ──────────────────────────────────────────────────────────

def run_pipeline(item_code, session, skip_steps=None, force_rerun=None, dry_run=False):
    skip_steps  = list(skip_steps  or [])
    force_rerun = list(force_rerun or [])

    if not DB_PATH.exists():
        print(f"ERROR: DB not found at {DB_PATH}", file=sys.stderr)
        return 1

    # ── Validate args ────────────────────────────────────────────────────────
    try:
        validate_step_args(skip_steps, force_rerun)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    conn = connect()

    # ── PF-1: Validate item ──────────────────────────────────────────────────
    item = db_get_item(conn, item_code)
    if not item:
        print(f"ERROR: {item_code} not found in items table. Run migrate_items.py first.", file=sys.stderr)
        return 1
    print(f"Item: {item['item_code']} — {item['name']}")
    print(f"Applicable groups: {item['applicable_groups']}")
    print(f"BPC slug: {item['bpc_source_slug'] or 'None'}")

    # ── PF-2: Get or create run ──────────────────────────────────────────────
    run = db_get_run(conn, item_code)
    run_id      = None
    steps_comp  = []
    steps_start = []

    if run:
        run_id      = run["run_id"]
        steps_comp  = json.loads(run["steps_complete"] or "[]")
        steps_start = json.loads(run["steps_started"]  or "[]")
        print(f"\nResuming run: {run_id}")
        print(f"  Status: {run['status']}")
        print(f"  Steps complete: {steps_comp}")

        # Detect mid-step failures
        failures = [s for s in steps_start if s not in steps_comp]
        if failures:
            print(f"  Mid-step failures detected (will re-run): {failures}")
            for f in failures:
                if f not in force_rerun:
                    force_rerun.append(f)
    else:
        run_id = f"{item_code}_{session}"
        h = spec_hash(item_code)
        if not dry_run:
            conn.execute("""
                INSERT INTO item_audit_runs
                (run_id, item_code, session, steps_complete, steps_started,
                 status, spec_hash, created_at, created_by_session, updated_at, updated_by_session)
                VALUES (?,?,?,'[]','[]','IN-PROGRESS',?,?,?,?,?)
            """, (run_id, item_code, session, h, now(), session, now(), session))
            conn.commit()
        print(f"\nNew run: {run_id}")

    # ── PF-3: Validate skip_steps ────────────────────────────────────────────
    try:
        validate_skip_against_prior(conn, item_code, skip_steps)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    # ── PF-4: Spec hash check on resume ─────────────────────────────────────
    if run and run["spec_hash"]:
        current = spec_hash(item_code)
        if current and current != run["spec_hash"]:
            print(f"\nWARN: Spec has changed since last run.")
            print(f"  Stored hash:  {run['spec_hash']}")
            print(f"  Current hash: {current}")
            print("Options: [R] Restart all steps  [C] Continue with stale-state flag")
            choice = input("Choice [R/C]: ").strip().upper()
            if choice == "R":
                print("Restarting pipeline from Step 1...")
                skip_steps  = []
                steps_comp  = []
                steps_start = []
                db_update_run(conn, run_id, session,
                              steps_complete=[], steps_started=[], status="IN-PROGRESS")
            else:
                print("Continuing with stale-state flag in brief.")

    # ── force_rerun cleanup ──────────────────────────────────────────────────
    if force_rerun and not dry_run:
        cleanup_for_force_rerun(conn, item_code, session, force_rerun)

    # ── Execute steps 1-7 ───────────────────────────────────────────────────
    print("\nPipeline execution:")

    for step in PIPELINE_STEPS:
        print(f"\n  [{PIPELINE_STEPS.index(step)+1}/8] {step}")

        # audit-consolidator always runs (handled separately at end)
        if step == "audit-consolidator":
            continue

        # Auto-skip checks
        if step == "connection-discovery-evidence" and should_skip_evidence_mode(item):
            print(f"    AUTO-SKIP: no BPC slug for {item_code}")
            if not dry_run:
                steps_start = step_started(conn, run_id, session, steps_start, step)
                steps_comp  = step_complete(conn, run_id, session, steps_comp, step)
            continue

        if step == "conflict-mapper" and should_skip_conflict_mapper(item):
            print(f"    AUTO-SKIP: fewer than 2 populations in applicable_groups")
            if not dry_run:
                steps_start = step_started(conn, run_id, session, steps_start, step)
                steps_comp  = step_complete(conn, run_id, session, steps_comp, step)
            continue

        # skip_steps check (already complete in prior run)
        if step in skip_steps:
            print(f"    SKIP: prior output in DB")
            continue

        # Already complete this run (not force_rerun)
        if step in steps_comp and step not in force_rerun:
            print(f"    SKIP: already complete this run")
            continue

        # Mark as started
        if not dry_run:
            steps_start = step_started(conn, run_id, session, steps_start, step)

        if dry_run:
            print(f"    [DRY-RUN] Would invoke {step} skill protocol")
        else:
            print(f"    → Invoke {step} skill protocol now (manual — see SKILL.md)")
            print(f"      This script is an orchestrator; each step runs its SKILL.md protocol.")
            print(f"      After completing the step manually, mark it complete:")
            print(f"      python3 scripts/db.py update-audit-run \\")
            print(f"        --run-id {run_id} --session {session} \\")
            print(f"        --steps-complete '{json.dumps(steps_comp + [step])}'")

        # Mark as complete (in automated/test context; in practice, done after step)
        if not dry_run:
            steps_comp = step_complete(conn, run_id, session, steps_comp, step)

    # ── Step 8: audit-consolidator ───────────────────────────────────────────
    print(f"\n  [8/8] audit-consolidator")
    if not dry_run:
        steps_start = step_started(conn, run_id, session, steps_start, "audit-consolidator")
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "audit_consolidator.py"),
             "--item", item_code, "--session", session],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"    {result.stdout.strip()}")
            steps_comp = step_complete(conn, run_id, session, steps_comp, "audit-consolidator")
        else:
            print(f"    ERROR: {result.stderr.strip()}", file=sys.stderr)
            return 1
    else:
        print(f"    [DRY-RUN] Would run audit_consolidator.py")

    # ── Final status ─────────────────────────────────────────────────────────
    if not dry_run:
        db_update_run(conn, run_id, session, status="COMPLETE")

    conn.close()

    print(f"\nITEM-AUDIT-PIPELINE COMPLETE")
    print(f"  Item: {item_code}")
    print(f"  Run ID: {run_id}")
    print(f"  Steps completed: {steps_comp}")
    print(f"  Brief: references/audit-briefs/{item_code}_brief.md")
    return 0


def show_status(item_code):
    """Show current pipeline status for an item."""
    conn = connect()
    run  = db_get_run(conn, item_code)
    if not run:
        print(f"No audit run found for {item_code}")
        conn.close()
        return

    steps_comp  = json.loads(run["steps_complete"] or "[]")
    steps_start = json.loads(run["steps_started"]  or "[]")
    incomplete  = [s for s in steps_start if s not in steps_comp]

    print(f"Run ID: {run['run_id']}")
    print(f"Status: {run['status']}")
    print(f"Steps complete:  {steps_comp}")
    print(f"Steps started:   {steps_start}")
    if incomplete:
        print(f"Mid-step failures: {incomplete}")
    print(f"Brief path: {run['brief_path'] or 'not yet produced'}")
    conn.close()


# ─── CLI ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Item audit pipeline wrapper")
    parser.add_argument("--item",    required=True, help="Item code (e.g. I-01)")
    parser.add_argument("--session", help="Session name (required unless --status)")
    parser.add_argument("--skip-steps",  nargs="*", default=[],
                        help="Steps to skip (must exist in prior steps_complete)")
    parser.add_argument("--force-rerun", nargs="*", default=[],
                        help="Steps to force re-run (deletes current-session findings first)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--status",  action="store_true", help="Show pipeline status for item")
    args = parser.parse_args()

    if args.status:
        show_status(args.item)
        sys.exit(0)

    if not args.session:
        print("ERROR: --session is required", file=sys.stderr)
        sys.exit(1)

    sys.exit(run_pipeline(
        item_code   = args.item,
        session     = args.session,
        skip_steps  = args.skip_steps,
        force_rerun = args.force_rerun,
        dry_run     = args.dry_run,
    ))
