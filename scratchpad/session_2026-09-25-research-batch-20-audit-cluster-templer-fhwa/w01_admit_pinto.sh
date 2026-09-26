#!/usr/bin/env bash
# Batch 20 — admit candidate 124 (Pinto et al. 2021) as REF-01007, into the SCRATCH db.
set -euo pipefail
cd /home/user/guidebook/.claude/worktrees/agent-acceda5e0fdea113d
export GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/34e8c762-53ff-5f39-b746-3f5298058fcb/scratchpad/b20.db
S=session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa

python3 scripts/db.py add-source --ref-id REF-01007 \
 --author "Pinto|Alexandro" --author "Köptcke|Luciana Sepúlveda" --author "David|Renata" --author "Kuper|Hannah" \
 --year 2021 --title "A National Accessibility Audit of Primary Health Care Facilities in Brazil—Are People with Disabilities Being Denied Their Right to Health?" \
 --tier 3 --evidence-type clinical --scope lower_control --jurisdiction BR \
 --doi "10.3390/ijerph18062953" --pmid 33805773 \
 --url "https://europepmc.org/articles/PMC7999795" --url-accessed "2026-09-25" \
 --doi-resolution-outcome RESOLVED --source-type journal_article \
 --lang-detected en --lang-detection-method "language field 'eng' in the persisted Europe PMC core record, and the retrieved JATS full text is English" \
 --metadata-quality COMPLETE --verification-method tool --verified-by-tool crossref --verification-status VERIFIED \
 --slug accessible-circulation-geometry --local-ref-id RAMP-AUDIT-BR \
 --session "$S" 2>&1 | tail -12
