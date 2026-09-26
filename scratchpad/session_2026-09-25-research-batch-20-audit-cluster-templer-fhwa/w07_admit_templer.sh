#!/usr/bin/env bash
# Batch 20 — admit candidate 125 (Templer, FHWA-RD-79-3 Vol. 3) as REF-01008, T3 grey
# (owner ruling 2026-09-18: pre-1990 work is historical grounding, same treatment as REF-01005).
set -euo pipefail
cd /home/user/guidebook/.claude/worktrees/agent-acceda5e0fdea113d
export GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/34e8c762-53ff-5f39-b746-3f5298058fcb/scratchpad/b20.db
S=session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa
PDF=retrieval-log/$S/db21e48738335d82.pdf
TXT=retrieval-log/$S/639e73bd17c02f7f.txt

echo "== add-source =="
python3 scripts/db.py add-source --ref-id REF-01008 \
 --author "Templer|John A." \
 --year 1980 --title "Provisions for Elderly and Handicapped Pedestrians. Volume 3: The Development and Evaluation of Countermeasures" \
 --tier 3 --evidence-type grey --scope intrinsic --jurisdiction US \
 --source-type report --report-number "FHWA-RD-79-3" \
 --institution "Georgia Institute of Technology, College of Architecture, Pedestrian Research Laboratory" \
 --publisher "Federal Highway Administration, Offices of Research and Development" --publisher-location "Washington, D.C." \
 --grey-flag 1 --grey-reason "US federal contract research report (FHWA contract DOT-FH-11-8504, Georgia Tech Pedestrian Research Laboratory), final report dated May 1980, distributed through NTIS; not peer-reviewed; no DOI (Crossref bibliographic query persisted this batch returns no record for it); digitised by the National Transportation Library on Internet Archive under CC BY-NC-ND 3.0." \
 --url "https://archive.org/details/provisionsforeld00temp_0" --url-accessed "2026-09-25" \
 --doi-resolution-outcome NO-MATCH \
 --lang-detected en --lang-detection-method "read on the rendered Technical Report Documentation Page (zero-based page index 2) and throughout the text" \
 --metadata-quality COMPLETE --verification-method direct-render --verification-status VERIFIED \
 --slug accessible-circulation-geometry --local-ref-id RAMP-HIST-02 \
 --session "$S" 2>&1 | tail -6

echo "== R13 population match =="
python3 scripts/db.py add-population-match --ref-id REF-01008 --target-population MOB \
 --study-population "120 volunteer subjects tested on 12 outdoor laboratory curb ramps and a mountable curb at Georgia Institute of Technology, August-November 1976, recruited through media and disability and elderly organisations; 'All of the subjects were experienced travellers'. Groups: self-propelled (manual) wheelchair users, powered wheelchair users, cane users, crutch users, people with prosthetic lower limbs, people who walk with difficulty but use no aids, elderly people, able-bodied controls (and visually impaired subjects for the detection tests). Table 2 (rendered page index 28) lists 18 manual wheelchair users -- cerebral palsy, spinal cord injury, polio, paraplegia, spina bifida, multiple birth defects -- whose summary row places all 18 in the 16-25 and 26-35 bands (its subdivision rows put one paraplegic man at 36-45 and one woman with residual polio at 56-65, so the table does not add up; at least 16 of 18 are aged 16-35 on either reading) -- and 6 powered wheelchair users." \
 --sample-size 120 --match-grade PARTIAL \
 --mismatch-note "PARTIAL, AND FOR TWO REASONS THAT CUT DIFFERENTLY. (1) THE TASK IS NARROWER THAN THE PARAMETER: every test ramp is a CURB ramp with a rise of 3, 6 or 9 inches and a run of 2-10 feet. What it measures is how steep a SHORT rise can be, not what gradient a building rampway of any length should have; its own conclusion is that 'steeper ramps are acceptable if they are short'. (2) THE MANUAL WHEELCHAIR GROUP IS YOUNG. At least 16 of Table 2's 18 manual wheelchair users are aged 16-35 (its summary row says all 18) -- the same objection REF-01005 raised against the 1957 Illinois sample (young, trained users). Elderly people ARE sampled, but as a separate walking group, not as wheelchair users. The authors say the sample 'is somewhat limited so the results must be considered as indicative, rather than conclusive'. Not PROXY: the subjects are disabled people doing the designed task. NOT Co-1: subjects rated ramps they were asked to use; nothing in the report says disabled people shaped the questions, the instrument or the analysis." \
 --session "$S" 2>&1 | tail -3

# ---- REMOVED 2026-09-26: the extraction attempts that used to follow ---------------------
# This script originally went on to (a) a loop writing Table 20's three curb-height rows and
# (b) four more add-extraction calls (ramp 4, ramp 6, "steeper if short", Walter at second
# hand). In the real run (a) was REFUSED three times by db.py's value-in-claim-text check --
# masked from `set -e` by `| grep ... || true` -- and (b) had no --session at all, so argparse
# rejected the first call and the script stopped there. NOTHING from either landed. The writes
# that did land are w08_templer_extractions.sh (Table 20 rows -> extractions 60-62, then 63,
# 64) and w09_templer_table3.sh (65, 66). Removed so that this script replays as it ran up to
# here; the removed text is in the version history of this file, the archive for code.
