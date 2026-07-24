#!/usr/bin/env bash
# preflight.sh — run every gate CI applies to a PR/merge, LOCALLY, before you push.
#
# Lesson (2026-07-24): every real defect that session was caught by a gate (a --check, a
# validator, reproducibility, an independent audit) — none by re-reading prose. CI's schema/
# db_integrity/governance jobs are PUSH-ONLY (they don't gate the PR), so a data/schema change
# can pass the PR yet fail on merge. Run this first; narrative confidence is not a gate.
#
# Read-only: runs validators + reproducibility + the --check gates (does NOT regenerate — use
# scripts/regenerate_derived.sh to fix staleness). Honors GUIDEBOOK_DB_PATH. Needs pydantic
# (+ jsonschema for attestation audits); pip install -r requirements.txt first.
#
# Prints [PASS]/[FAIL]/[SKIP] per gate, runs them ALL (does not stop at first failure), and
# exits non-zero if any FAIL. Mirrors ci.yml + audit.yml (minus push-only commit-msg).
#
# NB (L2 baseline lesson): a [FAIL] here may be PRE-EXISTING owner-gated debt on main, not your
# change. Before assuming you broke it, confirm the delta — e.g. run the same gate in a throwaway
# `git worktree add /tmp/base origin/main` and diff. test_db_integrity in particular carries a
# standing set of pre-existing failures unrelated to most changes.
cd "$(dirname "$0")/.."
fail=0
run() {  # run "<label>" <cmd...>
  local label="$1"; shift
  if "$@" >/tmp/preflight_step.log 2>&1; then
    echo "[PASS] $label"
  else
    echo "[FAIL] $label"
    sed 's/^/         /' /tmp/preflight_step.log | tail -8
    fail=1
  fi
}

echo "===== preflight: structure & cross-refs ====="
run "validate_bpc"              python3 scripts/validate_bpc.py --all
run "validate_cross_refs"       python3 scripts/validate_cross_refs.py --repo-root .

echo "===== preflight: schema & data layer ====="
run "validate_schema"           python3 scripts/validate_schema.py --verbose
run "validate_schema --cross"   python3 scripts/validate_schema.py --cross-check
run "validate_evidence_state"   python3 scripts/validate_evidence_state.py
run "verification_consistency"  python3 scripts/validate_verification_consistency.py
run "validate_population"       python3 scripts/validate_population.py
run "validate_temporal"         python3 scripts/validate_temporal.py
run "test_db_integrity"         python3 scripts/tests/test_db_integrity.py

echo "===== preflight: governance ====="
run "decision_capture"          python3 scripts/decision_capture.py
run "doctrine_recheck --cross"  python3 scripts/doctrine_recheck.py --cross-ref
run "source_slug_dupes"         python3 scripts/audit/source_slug_links_duplicates.py

echo "===== preflight: DB reproducibility (audit.yml GAP-290, the real PR gate) ====="
if python3 scripts/migrate_db.py --rebuild /tmp/preflight_rebuilt.db >/tmp/preflight_step.log 2>&1; then
  python3 - <<'PY'
import sqlite3, sys, os
a=sqlite3.connect(os.environ.get("GUIDEBOOK_DB_PATH","data/guidebook.db")); b=sqlite3.connect("/tmp/preflight_rebuilt.db")
inv=[("PRAGMA user_version","user_version"),("SELECT COUNT(*) FROM evidence_sources","evidence_sources"),
     ("SELECT COUNT(*) FROM citation_mining","citation_mining"),("SELECT COUNT(*) FROM source_slug_links","source_slug_links"),
     ("SELECT COUNT(*) FROM gaps","gaps"),("SELECT COUNT(*) FROM connections","connections"),("SELECT COUNT(*) FROM items","items")]
bad=[]
for sql,label in inv:
    c=a.execute(sql).fetchone()[0]; r=b.execute(sql).fetchone()[0]
    if c!=r: bad.append(f"{label}: committed={c} rebuilt={r}")
if bad:
    print("[FAIL] reproducibility (7 core invariants)"); [print("         "+x) for x in bad]; sys.exit(1)
print("[PASS] reproducibility (7 core invariants)")
PY
  [ $? -ne 0 ] && fail=1
else
  echo "[FAIL] reproducibility (rebuild errored)"; tail -6 /tmp/preflight_step.log; fail=1
fi

echo "===== preflight: DB-derived output freshness (--check gates) ====="
run "pipeline_completeness --check"  python3 tools/pipeline_completeness.py --check
run "evidentiary_audit --check"      python3 tools/evidentiary_audit.py --check

echo "==================================================="
if [ "$fail" -eq 0 ]; then
  echo "PREFLIGHT: PASS — safe to push."
else
  echo "PREFLIGHT: FAIL — fix the [FAIL] gates above before pushing."
  echo "  (stale --check? run: scripts/regenerate_derived.sh)"
fi
exit "$fail"
