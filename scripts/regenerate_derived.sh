#!/usr/bin/env bash
# regenerate_derived.sh — regenerate every DB-derived output the CORRECT way, then verify.
#
# Lesson (2026-07-24): a dashboard was regenerated with `python3 tool.py > out.html`, which
# captured the tool's stdout STATUS LINE instead of its HTML — the tools write their own
# output path (DEFAULT_OUT). The `> redirect` is always wrong here; call the writer, no redirect.
# This script is the single sanctioned regeneration entry point after ANY data/guidebook.db change.
#
# Each generator writes its own file(s); we then run the tools' own `--check` gates (what CI runs)
# to prove the committed tree now matches a fresh regeneration. Exit non-zero if anything is stale.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== Regenerating DB-derived outputs (tool writers, never stdout redirect) =="
python3 tools/pipeline_completeness.py
python3 tools/evidentiary_audit.py
python3 tools/regenerate_vetting_surface.py

echo "== Verifying --check gates (mirror CI regenerate-*.yml) =="
python3 tools/pipeline_completeness.py --check
python3 tools/evidentiary_audit.py --check

echo "All DB-derived outputs regenerated and --check-clean. Review 'git status' and commit."
