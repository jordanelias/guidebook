#!/usr/bin/env bash
# Replays batch 24's parameter promotions on a scratch copy of the canonical DB.
# Usage: SCRATCH_DB=/path/to/copy bash populate-parameters.sh     (add DRY=--dry-run to rehearse)
# The canonical data/guidebook.db is never opened for writing; only migrate_db.py does that.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"   # paths below are relative to the repository root
# Pinned: a replay must stamp the session that did the work, not whatever scratchpad/CURRENT names when it is run.
S="session_2026-10-09-research-batch-24-parameter-pilot"
# Replay fidelity: this text must stay byte-identical to what the committed migration carries. One clause in it is wrong
# for TERM-091 (it does hold a NAMES-NEW adjudication from batch 20); that is corrected by an appended note, not here.
NOTE="Promoted from the base vocabulary on the owner's direction of 2026-10-09 (populate the parameter table from the existing terms registry). Judged a measurable design quantity by the session; no source adjudication behind it. Direction left unset until an admitted source states which way is better for a disabled person."
for T in TERM-002 TERM-003 TERM-005 TERM-007 TERM-011 TERM-021 TERM-024 TERM-061 TERM-091; do
  GUIDEBOOK_DB_PATH="$SCRATCH_DB" python3 scripts/db.py add-parameter --term-id "$T" --notes "$NOTE" --session "$S" ${DRY:-}
done
