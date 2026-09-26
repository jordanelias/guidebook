#!/usr/bin/env bash
# Batch 20 — admit candidate 125 (Templer, FHWA-RD-79-3 Vol. 3) as REF-01008, T3 grey
# (owner ruling 2026-09-18: pre-1990 work is historical grounding, same treatment as REF-01005).
set -euo pipefail
cd /home/user/guidebook/.claude/worktrees/agent-acceda5e0fdea113d
export GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/34e8c762-53ff-5f39-b746-3f5298058fcb/scratchpad/b20.db
S=session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa
PDF=retrieval-log/$S/db21e48738335d82.pdf
TXT=retrieval-log/$S/639e73bd17c02f7f.txt

echo "== extractions: Table 20, three curb-height rows =="
for spec in "3|7.62|1:8|X O O O O|the only curb height at which 1:8 is recommended; ramp 9 (1:8, 2 ft, 3 in) was tested and acceptable to manual wheelchair users in ascent (95 percent rating 1 or 2)" \
            "6|15.2|1:10|X X O O O|NO RAMP OF 1:10 OVER A 6-INCH CURB WAS TESTED (Table 1): the 6-inch ramps were 1:8 (ramp 3, unacceptable), 1:12 (ramps 2 and 4) and 1:16 and 1:20. The 1:10 cell is the authors' interpolation between a tested failure and a tested success" \
            "9|22.9|1:12|X X X O O|NO RAMP OF 1:12 OVER A 9-INCH CURB WAS TESTED (Table 1): the 9-inch ramps were 1:5.3, 1:8, 1:10.67 and 1:13.3, and only 1:13.3 (ramp 5) was acceptable to manual wheelchair users in ascent (84 percent). The 1:12 cell is an interpolation just steeper than the gentlest tested 9-inch ramp"; do
  IFS='|' read -r RISE CM VAL ROW WHY <<< "$spec"
  read -r C1 C2 C3 C4 C5 <<< "$ROW"
  python3 scripts/db.py add-extraction --ref-id REF-01008 --slug accessible-circulation-geometry --parameter-id 3 --identity MOB \
   --claim-type numerical --claimed-value "$VAL" --claimed-unit ratio --comparator "<=" --figure-role claim \
   --claim-text "Table 20 Ramp Gradient Recommendations -- Curb Heights Not Exceeding ${RISE}\" (${CM} cm): Gradients Steeper Than 1:8 ${C1}; 1:8 ${C2}; 1:10 ${C3}; 1:12 ${C4}; 1:16 ${C5} (X Not Recommended, O Recommended). *Whenever possible slopes less than the maximum should be employed." \
   --verbatim-exempt "TABLE CELLS, NOT A SENTENCE. The only text layer that can be checked (the Internet Archive DjVuTXT, 639e73bd17c02f7f.txt, around the line reading Table 20 Ramp Gradient Recommendations) serialises the table COLUMN BY COLUMN and reads every O mark as the digit 0, so no row of Table 20 exists as a contiguous string in any artefact. This claim_text is the row transcribed from the RENDERED page (db21e48738335d82.p0053.png, printed page 34, zero-based index 53), and the column-wise text layer agrees with it cell for cell. The sentence introducing the table verifies verbatim: Based on these findings, Table 20 shows recommendations for maximum acceptable gradients for three different curb heights." \
   --source-section "A Study of Short Ramps -- Recommendations; Table 20, Ramp Gradient Recommendations" \
   --jurisdiction US --setting "curb ramp; curb height not exceeding ${RISE} in (${CM} cm)" \
   --extraction-method full-read --extraction-status verified \
   --root-type measurement_primary --root-ref-id REF-01008 --device-class mixed \
   --root-population-note "Table 20 aggregates the ratings of all eight subject groups (Table 19); it is not a wheelchair-only recommendation." \
   --file-anchor "$PDF" --locator-scheme page --loc-section 34 --loc-note "printed page 34 = zero-based index 53; rendered and read (db21e48738335d82.p0053.png)" \
   --relation none \
   --notes "TABLE 20 AS RENDERED: columns are 'Gradients Steeper Than 1:8', 1:8, 1:10, 1:12, 1:16 under 'Maximum Gradient*'; for curb heights not exceeding ${RISE} in (${CM} cm) the row reads ${ROW} (X = Not Recommended, O = Recommended), so the steepest recommended gradient at this height is ${VAL}. Footnote: '*Whenever possible slopes less than the maximum should be employed.' THE RECOMMENDATION IS RISE-CONDITIONED, and that is the finding: the report's own conclusion is 'steeper ramps are acceptable if they are short'. WHAT WAS AND WAS NOT TESTED AT THIS CELL: ${WHY}. Acceptability criterion (printed p.14): 'a ramp is considered to be acceptable if about 80% of the subjects rated the ramp as 1 or 2' on a four-point difficulty scale. Owner ruling 2026-09-18: pre-1990 work is historical grounding, not a current anchor -- T3 grey, cannot lift parameter 3 off proxy." \
   --session "$S" 2>&1 | { grep -E '"extraction_id"|error|Error|REFUS' || true; }
done

# REMOVED 2026-09-26: two add-extraction calls stood here (ramp 4, 1:12 over a 6 in curb; ramp 6,
# 1:10.67 over a 9 in curb). db.py REFUSED both in the real run -- the first for '--stated named'
# with a label its --quote did not contain, the second on the value-in-claim-text check -- and
# `| grep ... || true` hid the refusals from `set -e`. Neither landed. Their corrected versions,
# claim_text read off the rendered Table 3 cell, are w09_templer_table3.sh (extractions 65, 66).
# Removed so this script replays as it ran; the text is in the version history of this file.

echo "== extraction: steeper is acceptable if short (qualitative finding) =="
python3 scripts/db.py add-extraction --ref-id REF-01008 --slug accessible-circulation-geometry --parameter-id 3 --identity MOB \
 --claim-type qualitative --claimed-value "a steeper gradient is acceptable over a shorter rise and run" --figure-role finding \
 --claim-text "Secondly, it is clear that steeper ramps are acceptable if they are short." \
 --source-section "A Study of Short Ramps -- Conclusions (after Table 19)" \
 --jurisdiction US --setting "curb ramps, rises 3-9 in, runs 2-10 ft" \
 --extraction-method full-read --extraction-status verified \
 --root-type measurement_primary --root-ref-id REF-01008 --device-class mixed \
 --file-anchor "$PDF" --locator-scheme page --loc-section 33 --loc-note "printed page 33 = zero-based index 52, rendered (db21e48738335d82.p0052.png)" \
 --relation none \
 --notes "The conclusion Table 20 is built on, and the fourth independent statement of length-conditioning on parameter 3 in this corpus: REF-01002's 7 percent up to 20 ft, REF-01003's short-distance acceptability, REF-00996's mechanism (the greater the rise, the gentler the ramp, because the effort is sustained longer), and this. It is what a single maximum gradient without a length or rise cannot express, and it is why the 1:12 rows in this corpus do not contradict each other." \
 --session "$S" 2>&1 | { grep -E '"extraction_id"|"relation_ids"|REFUS|error' || true; }

echo "== extraction: Walter 1971 at second hand (root untraced) =="
python3 scripts/db.py add-extraction --ref-id REF-01008 --slug accessible-circulation-geometry --parameter-id 3 --identity MOB \
 --claim-type numerical --claimed-value "1:16" --claimed-unit ratio --comparator "<=" --figure-role claim \
 --claim-text "Gradients that were rated by a high percentage of the subjects to be 'easy' or 'comfortable' were recommended—for self-propelled wheelchairs, a slope of 1:9 for the 10 foot (3.05 m) ramp, and 1:16 for the 20 foot (6.1 m) ramp" \
 --source-section "A Study of Short Ramps -- Previous Studies (Walter, reference 3)" \
 --jurisdiction UK --setting "20 ft (6.1 m) indoor laboratory ramp; self-propelled wheelchairs (Walter 1971, reported at second hand)" \
 --extraction-method full-read --extraction-status verified \
 --root-type untraced --device-class manual_self_propelled \
 --root-population-note "Walter's subjects are not described in this account beyond 'self-propelled' and 'assistant-propelled' wheelchairs." \
 --root-classification-basis "Reported SECOND-HAND by REF-01008. root_ref_id is deliberately NULL: Walter 1971 is search_candidates 109, not an admitted source, so there is no row to point at, and external_root_registry has no writer in db.py. This is NOT a claim that REF-01008 measured 1:16 over 20 ft -- its longest test ramp is 10 ft. Same treatment as extraction 57 (Elmer 1957 via REF-01005)." \
 --file-anchor "$TXT" --locator-scheme page --loc-section 4 --loc-note "printed page 4 = zero-based index 23, rendered (db21e48738335d82.p0023.png)" \
 --relation none \
 --notes "WALTER'S RAMP AT SECOND HAND, FROM A SECOND INDEPENDENT READER. As printed: an adjustable indoor laboratory ramp, 20 ft at 1:8.6 to 1:16 and 10 ft at 1:5.5 to 1:10, rated on a four-point scale (easy, comfortable, difficult, impossible); recommended for SELF-PROPELLED wheelchairs 1:9 over 10 ft and 1:16 over 20 ft; for ASSISTANT-PROPELLED 1:9 over 10 ft and 1:12 over 20 ft. The page prints '10 foot (6.1 m)' in the assistant-propelled clause -- a unit slip in the source (10 ft is 3.05 m), recorded as printed. WHAT IT CORROBORATES: REF-01005 (extraction 54) reports that Walter and Steinfeld both found 1:16 over 20 ft accessible. Templer, writing independently, gives the same 1:16-over-20-ft figure for Walter. That corroborates the REPORT OF Walter by a second reader; it does NOT make Walter a second root, and v_value_independence must still count Walter once, and only when Walter itself is read. GAP-026 and the 2026-09-25 owner ruling: Walter itself is exhausted, so this second-hand account is the best text of Walter this project will hold for now." \
 --session "$S" 2>&1 | { grep -E '"extraction_id"|"relation_ids"|REFUS|error' || true; }
