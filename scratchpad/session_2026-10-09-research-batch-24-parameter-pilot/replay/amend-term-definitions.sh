#!/usr/bin/env bash
# Replays batch 24's two definition repairs on a scratch copy of the canonical DB.
# Usage: SCRATCH_DB=/path/to/copy bash amend-term-definitions.sh     (add DRY=--dry-run to rehearse)
# The session stem is pinned: a replay must stamp the session that did the work, not whatever scratchpad/CURRENT names then.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
S="session_2026-10-09-research-batch-24-parameter-pilot"
REASON="The definition stated a direction (a floor or a ceiling) for a term promoted to a parameter; a parameter names the quantity under determination and must not state its own answer (the 2026-09-01 ruling that deleted the item layer)."
GUIDEBOOK_DB_PATH="$SCRATCH_DB" python3 scripts/db.py amend-term --term-id TERM-003 --field definition --replacement "Space for wheelchair 360° rotation" --reason "$REASON" --session "$S" ${DRY:-}
GUIDEBOOK_DB_PATH="$SCRATCH_DB" python3 scripts/db.py amend-term --term-id TERM-005 --field definition --replacement "Force required to operate hardware" --reason "$REASON" --session "$S" ${DRY:-}
