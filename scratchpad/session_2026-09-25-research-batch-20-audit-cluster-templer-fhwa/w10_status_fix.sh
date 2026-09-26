#!/usr/bin/env bash
set -euo pipefail
cd /home/user/guidebook/.claude/worktrees/agent-acceda5e0fdea113d
export GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/34e8c762-53ff-5f39-b746-3f5298058fcb/scratchpad/b20.db
S=session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa
for id in 60 61 62 65 66; do
python3 scripts/db.py amend-extraction --extraction-id $id --field extraction_status --value reviewed \
 --reason "Written as 'verified' minutes earlier in the same batch; corrected before emission. This row's claim_text is a TRANSCRIPTION of table cells read off a rendered page and carries a VERBATIM-EXEMPT warrant, so nothing byte-checks it. The corpus's other exempt transcriptions (REF-01005, extractions 52-57) are 'reviewed', and 'verified' is kept here for rows whose claim_text verifies byte-for-byte against a persisted artefact (63, 64)." \
 --session "$S" 2>&1 | tail -2
done
