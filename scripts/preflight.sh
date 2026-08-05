#!/usr/bin/env bash
# preflight.sh — run the gates CI will apply, LOCALLY, before you push.
#
# This is now a thin wrapper over scripts/run_checks.py, which reads
# governance/check-registry.yaml. It used to be a second hand-kept list of checks
# alongside ci.yml, audit.yml and research-contract.yml — and the four lists had  [RETIRED-VOCAB-OK]
# already drifted: preflight ran validate_axes and validate_verification_consistency
# that no workflow ran, ci.yml ran validate_jurisdiction and validate_temporal that
# preflight didn't, and the migration-reproducibility invariant existed as two
# separately-maintained inline heredocs. One registry means preflight and CI
# cannot disagree about what a check is.
#
# BY DEFAULT it gates on WHAT YOU CHANGED — it classifies your diff against
# origin/main into work kinds (data / schema / synthesis / governance / render /
# tooling) and runs the checks those kinds warrant. Pass --all to run everything.
#
# Lesson (2026-07-24): every real defect that session was caught by a gate (a
# --check, a validator, reproducibility, an independent audit) — none by re-reading
# prose. Run this first; narrative confidence is not a gate.
#
# Read-only: it runs validators, it does NOT regenerate. To fix a staleness
# failure, run scripts/regenerate_derived.sh.
#
# Needs pydantic + PyYAML (+ jsonschema for the attestation checks):
#     pip install -r requirements.txt jsonschema
#
# Honours GUIDEBOOK_DB_PATH. Prints [PASS]/[FAIL]/[SKIP] per check, runs them ALL
# rather than stopping at the first failure, and exits non-zero if any BLOCKING
# check fails. Advisory and informational failures are reported but do not fail —
# levels are declared in the registry, not here.
#
# NB (L2 baseline lesson): a [FAIL] here may be PRE-EXISTING owner-gated debt on
# main, not your change. Before assuming you broke it, confirm the delta — e.g.
# run the same check in a throwaway `git worktree add /tmp/base origin/main` and
# diff. test_db_integrity and evidentiary_audit_fresh in particular are red on
# main as of 2026-08-01; see references/tooling-register.md §4.
#
# Usage:
#     scripts/preflight.sh                      # gate what you changed vs origin/main
#     scripts/preflight.sh --all                # every registered check
#     scripts/preflight.sh --base HEAD~3        # diff against something else
#     scripts/preflight.sh --explain            # show why each check ran or didn't
#     scripts/preflight.sh --battery schema     # one battery
#   Any further flags are passed straight through to run_checks.py.

set -uo pipefail
cd "$(dirname "$0")/.."

BASE="origin/main"
ARGS=()
MODE_ALL=0
USER_KINDS=0

while [ $# -gt 0 ]; do
  case "$1" in
    --base)  BASE="$2"; shift 2 ;;
    --all)   MODE_ALL=1; shift ;;
    -h|--help)
      sed -n '2,44p' "$0" | sed 's/^# \{0,1\}//'
      exit 0 ;;
    # An explicit --kinds means the caller has chosen the work kinds themselves,
    # so appending --changed-from would hand run_checks.py two contradictory
    # sources of truth. It refuses that combination (deliberately — silently
    # discarding one of them is how a real diff came to report "0 changed
    # files"), which would have made `preflight.sh --kinds X` permanently exit 2.
    --kinds) USER_KINDS=1; ARGS+=("$1"); shift ;;
    *)       ARGS+=("$1"); shift ;;
  esac
done

if ! python3 -c "import yaml" 2>/dev/null; then
  echo "preflight: PyYAML is required — pip install -r requirements.txt" >&2
  exit 2
fi

# The registry selftest runs first: it verifies every registered script still
# exists on disk, so a rename that skipped its caller sweep surfaces here rather
# than as a check that has silently stopped running.
echo "===== preflight: registry selftest ====="
python3 scripts/run_checks.py --selftest || exit 1
echo

if [ "$MODE_ALL" -eq 1 ]; then
  python3 scripts/run_checks.py --all ${ARGS[@]+"${ARGS[@]}"}
elif [ "$USER_KINDS" -eq 1 ]; then
  python3 scripts/run_checks.py ${ARGS[@]+"${ARGS[@]}"}
else
  if ! git rev-parse --verify --quiet "$BASE" >/dev/null; then
    echo "preflight: base ref '$BASE' not found; fetching..." >&2
    git fetch origin main --quiet 2>/dev/null || true
  fi
  python3 scripts/run_checks.py --changed-from "$BASE" ${ARGS[@]+"${ARGS[@]}"}
fi
status=$?

echo
if [ "$status" -eq 0 ]; then
  echo "PREFLIGHT: PASS — safe to push."
  echo "  (gated on your diff — run 'scripts/preflight.sh --all' for the full battery.)"
else
  echo "PREFLIGHT: FAIL — fix the blocking failures above before pushing."
  echo "  (stale --check? run: scripts/regenerate_derived.sh)"
fi
exit "$status"
