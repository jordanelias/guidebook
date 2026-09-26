#!/usr/bin/env bash
# Batch 20 — REF-01008 Table 3 findings. Claim text is the TABLE CELL as rendered, not the prose
# list of ramp numbers: the prose list satisfies add-extraction's digit check only by coincidence
# (ramp numbers 1 and 12 supply the digits of '1:12'), which would attach a gradient to a sentence
# that never states one.
set -euo pipefail
cd /home/user/guidebook/.claude/worktrees/agent-acceda5e0fdea113d
export GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/34e8c762-53ff-5f39-b746-3f5298058fcb/scratchpad/b20.db
S=session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa
PDF=retrieval-log/$S/db21e48738335d82.pdf
EX="TABLE CELL, NOT A SENTENCE. Table 3 is a grid of cells (ramp number, length, subject mean, percent rating 1 or 2, tester mean in parentheses); the Internet Archive DjVuTXT (639e73bd17c02f7f.txt, from the line reading Table 3 Gradient Ratings by Manual Wheelchair Users: Ascent) carries only fragments of it, out of order. This claim_text is the cell transcribed from the RENDERED page (db21e48738335d82.p0036.png, printed page 17, zero-based index 36), with the gradient and curb height from the column and row headers and the ramp geometry from Table 1 (db21e48738335d82.p0024.png). The acceptability verdict verifies verbatim in the prose on printed page 14: From Table 3, the curb ramps to the right of the heavy line are acceptable for ascent: Ramps #1, 4, 5, 9, 10, 11, 12 and 13 are acceptable Ramps #2, 3, 6, 7, 8 are unacceptable"

python3 scripts/db.py add-extraction --ref-id REF-01008 --slug accessible-circulation-geometry --parameter-id 3 --identity MOB \
 --claim-type numerical --claimed-value "1:12" --claimed-unit ratio --comparator "=" --figure-role finding \
 --claim-text "Table 3 Gradient Ratings by Manual Wheelchair Users: Ascent -- gradient 1:12, curb height 6\" (15.2 cm), ramp 4, 6' lgth 1.83m: subject rating 1.26, 100% of subjects rating a 1 or 2, tester rating (1.84). Ratings: 1 Not at all difficult, 2 A little difficult, 3 Difficult, 4 Very difficult." \
 --verbatim-exempt "$EX" \
 --source-section "A Study of Short Ramps -- Results, 1a Manual Wheelchair Users; Table 3, Gradient Ratings by Manual Wheelchair Users: Ascent" \
 --jurisdiction US --setting "curb ramp 4: 1:12, 6 ft (1.83 m) long, over a 6 in (15.24 cm) curb; ascent" \
 --extraction-method full-read --extraction-status verified \
 --root-type measurement_primary --root-ref-id REF-01008 --device-class manual_self_propelled \
 --root-population-note "Manual (self-propelled) wheelchair users; Table 2 lists 18, at least 16 of them aged 16-35." \
 --file-anchor "$PDF" --locator-scheme page --loc-section 17 --loc-note "Table 3 at printed page 17 = zero-based index 36, rendered; prose verdict at printed page 14 = index 33" \
 --relation tested_at --to-label "ramp 4: 1:12 over a 6 in curb, 6 ft run" --to-kind own_sample --stated inferred \
 --quote "Ramps #1, 4, 5, 9, 10, 11, 12 and 13 are acceptable" \
 --notes "READ OFF THE RENDERED TABLE 3. 'inferred' on the edge because the prose names ramps by NUMBER only; that ramp 4 is 1:12 over 6 in for 6 ft comes from joining Table 1. THE CONTRAST WITH REF-01005 IS THE POINT AND IT IS NOT A CONTRADICTION: REF-01005 found almost half of wheelchair users could not complete a 1:12 RUN over its test length, while here every manual wheelchair user rated 1:12 acceptable over a 6-inch RISE and a 6-foot run. Same gradient, different length -- the rise- and length-conditioning that REF-01002 (20 ft bound), REF-01003 (short distances) and this report's own conclusion ('steeper ramps are acceptable if they are short') all state. A 1:12 value without its rise or run is not the same claim. The tester's ratings run harder than the subjects' own at almost every ramp (1.84 against 1.26 here)." \
 --session "$S" 2>&1 | { grep -E '"extraction_id"|"relation_ids"|REFUS|error' || true; }

python3 scripts/db.py add-extraction --ref-id REF-01008 --slug accessible-circulation-geometry --parameter-id 3 --identity MOB \
 --claim-type numerical --claimed-value "1:10.67" --claimed-unit ratio --comparator "=" --figure-role finding \
 --claim-text "Table 3 Gradient Ratings by Manual Wheelchair Users: Ascent -- gradient 1:10.67, curb height 9\" (22.9 cm), ramp 6, 8' lgth 2.44m: subject rating 2.16, 58% of subjects rating a 1 or 2, tester rating (2.42). Only ramps to the right of the heavy line are considered acceptable; ramp 6 lies to its left." \
 --verbatim-exempt "$EX" \
 --source-section "A Study of Short Ramps -- Results, 1a Manual Wheelchair Users; Table 3, Gradient Ratings by Manual Wheelchair Users: Ascent" \
 --jurisdiction US --setting "curb ramp 6: 1:10.67, 8 ft (2.44 m) long, over a 9 in (22.85 cm) curb; ascent" \
 --extraction-method full-read --extraction-status verified \
 --root-type measurement_primary --root-ref-id REF-01008 --device-class manual_self_propelled \
 --root-population-note "Manual (self-propelled) wheelchair users; Table 2 lists 18, at least 16 of them aged 16-35." \
 --file-anchor "$PDF" --locator-scheme page --loc-section 17 --loc-note "Table 3 at printed page 17 = zero-based index 36, rendered; Table 1 at printed page 5 = index 24, rendered" \
 --relation tested_at --to-label "ramp 6: 1:10.67 over a 9 in curb, 8 ft run" --to-kind own_sample --stated inferred \
 --quote "Ramps #2, 3, 6, 7, 8 are unacceptable" \
 --notes "READ OFF THE RENDERED TABLE 3: ramp 6 (1:10.67, 8 ft, 9 in) -- subject mean 2.16, only 58 percent rating it 1 or 2, tester mean 2.42 -- below the report's ~80 percent acceptability line. Also unacceptable in ascent: ramp 3 (1:8, 4 ft, 6 in) 44 percent; ramp 8 (1:8, 6 ft, 9 in) 47 percent; ramp 7 (1:5.3, 4 ft, 9 in) 32 percent with two subjects unable. WHY THIS ROW EXISTS: THE GEOMETRY OF RAMP 6 IS THE GEOMETRY OF REF-01005 TABLE 13's 1:10 ROW. Table 13 (rendered this batch, 5dd866a236fb5978.p0056.png) allows 'If slope = 10.0% (1:10) or less steep' with a maximum run of 8 ft and a maximum rise of 9 in -- and 9 in over 8 ft is 1:10.67, ramp 6 exactly. Its 1:8 row (2 ft run, 3 in rise) is likewise ramp 9 exactly. Both rows carry footnote c, 'Based on research of others (Templer, 1977 and Walters, 1971)'. So the combination Table 13 permits in its 1:10 band is one this report TESTED AND FOUND UNACCEPTABLE to manual wheelchair users in ascent, and this report's own Table 20 does not recommend 1:10 above a 6-inch curb. HELD AS AN OBSERVATION, NOT AN IDENTIFICATION: the two matching geometries are consistent with footnote c's Templer being this project's ramp work (tested August-November 1976; an interim report could carry 1977), but THIS REPORT IS DATED MAY 1980 and the referent is not identified -- candidate 115 stays PENDING. Walter's 10-ft recommendation as this report gives it (printed p.4: 1:9, self-propelled) is steeper than 1:10, so Table 13's 1:10 band sits between its two named warrants rather than being taken from either." \
 --session "$S" 2>&1 | { grep -E '"extraction_id"|"relation_ids"|REFUS|error' || true; }
