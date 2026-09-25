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

echo "== extractions: Table 20, three curb-height rows =="
for spec in "3|7.62|1:8|X O O O O|the only curb height at which 1:8 is recommended; ramp 9 (1:8, 2 ft, 3 in) was tested and acceptable to manual wheelchair users in ascent (95 percent rating 1 or 2)" \
            "6|15.2|1:10|X X O O O|NO RAMP OF 1:10 OVER A 6-INCH CURB WAS TESTED (Table 1): the 6-inch ramps were 1:8 (ramp 3, unacceptable), 1:12 (ramps 2 and 4) and 1:16 and 1:20. The 1:10 cell is the authors' interpolation between a tested failure and a tested success" \
            "9|22.9|1:12|X X X O O|NO RAMP OF 1:12 OVER A 9-INCH CURB WAS TESTED (Table 1): the 9-inch ramps were 1:5.3, 1:8, 1:10.67 and 1:13.3, and only 1:13.3 (ramp 5) was acceptable to manual wheelchair users in ascent (84 percent). The 1:12 cell is an interpolation just steeper than the gentlest tested 9-inch ramp"; do
  IFS='|' read -r RISE CM VAL ROW WHY <<< "$spec"
  python3 scripts/db.py add-extraction --ref-id REF-01008 --slug accessible-circulation-geometry --parameter-id 3 --identity MOB \
   --claim-type numerical --claimed-value "$VAL" --claimed-unit ratio --comparator "<=" --figure-role claim \
   --claim-text "Based on these findings, Table 20 shows recommendations for maximum acceptable gradients for three different curb heights." \
   --source-section "A Study of Short Ramps -- Recommendations; Table 20, Ramp Gradient Recommendations" \
   --jurisdiction US --setting "curb ramp; curb height not exceeding ${RISE} in (${CM} cm)" \
   --extraction-method full-read --extraction-status verified \
   --root-type measurement_primary --root-ref-id REF-01008 --device-class mixed \
   --root-population-note "Table 20 aggregates the ratings of all eight subject groups (Table 19); it is not a wheelchair-only recommendation." \
   --file-anchor "$PDF" --locator-scheme page --loc-section 34 --loc-note "printed page 34 = zero-based index 53; rendered and read (db21e48738335d82.p0053.png)" \
   --relation none \
   --notes "TABLE 20 AS RENDERED: columns are 'Gradients Steeper Than 1:8', 1:8, 1:10, 1:12, 1:16 under 'Maximum Gradient*'; for curb heights not exceeding ${RISE} in (${CM} cm) the row reads ${ROW} (X = Not Recommended, O = Recommended), so the steepest recommended gradient at this height is ${VAL}. Footnote: '*Whenever possible slopes less than the maximum should be employed.' THE RECOMMENDATION IS RISE-CONDITIONED, and that is the finding: the report's own conclusion is 'steeper ramps are acceptable if they are short'. WHAT WAS AND WAS NOT TESTED AT THIS CELL: ${WHY}. Acceptability criterion (printed p.14): 'a ramp is considered to be acceptable if about 80% of the subjects rated the ramp as 1 or 2' on a four-point difficulty scale. Owner ruling 2026-09-18: pre-1990 work is historical grounding, not a current anchor -- T3 grey, cannot lift parameter 3 off proxy." \
   --session "$S" 2>&1 | grep -E '"extraction_id"|error|Error|REFUS' || true
done

echo "== extraction: manual wheelchair ascent, 1:12 over 6 in acceptable (finding) =="
python3 scripts/db.py add-extraction --ref-id REF-01008 --slug accessible-circulation-geometry --parameter-id 3 --identity MOB \
 --claim-type numerical --claimed-value "1:12" --claimed-unit ratio --comparator "=" --figure-role finding \
 --claim-text "From Table 3, the curb ramps to the right of the heavy line are acceptable for ascent: Ramps #1, 4, 5, 9, 10, 11, 12 and 13 are acceptable Ramps #2, 3, 6, 7, 8 are unacceptable" \
 --source-section "A Study of Short Ramps -- Results, 1a Manual Wheelchair Users; Table 3, Gradient Ratings by Manual Wheelchair Users: Ascent" \
 --jurisdiction US --setting "curb ramp 4: 1:12, 6 ft (1.83 m) long, over a 6 in (15.24 cm) curb; ascent" \
 --extraction-method full-read --extraction-status verified \
 --root-type measurement_primary --root-ref-id REF-01008 --device-class manual_self_propelled \
 --root-population-note "Manual (self-propelled) wheelchair users; Table 2 lists 18, at least 16 of them aged 16-35." \
 --file-anchor "$PDF" --locator-scheme page --loc-section 17 --loc-note "Table 3 at printed page 17 = zero-based index 36, rendered (db21e48738335d82.p0036.png); text at printed page 14 = index 33" \
 --relation tested_at --to-label "1:12 over a 6 in curb, 6 ft run (ramp 4)" --to-kind own_sample --stated named \
 --quote "Ramps #1, 4, 5, 9, 10, 11, 12 and 13 are acceptable" \
 --notes "READ OFF THE RENDERED TABLE 3: ramp 4 (1:12, 6 ft, 6 in curb) -- subject mean rating 1.26, 100 percent of subjects rating it 1 or 2 ('not at all' or 'a little difficult'), tester mean 1.84. THE CONTRAST WITH REF-01005 IS THE POINT AND IT IS NOT A CONTRADICTION: REF-01005 found almost half of wheelchair users could not complete a 1:12 RUN over its test length, while here every manual wheelchair user rated 1:12 acceptable over a 6-inch RISE and a 6-foot run. Same gradient, different length -- which is the rise- and length-conditioning REF-01002 (20 ft bound), REF-01003 (short distances) and this report's own conclusion ('steeper ramps are acceptable if they are short') all state. A 1:12 value without its rise or run is not the same claim. The tester's ratings run harder than the subjects' own at almost every ramp (1.84 vs 1.26 here)."

echo "== extraction: manual wheelchair ascent, the 9-inch rise at 1:10.67 unacceptable (finding) =="
python3 scripts/db.py add-extraction --ref-id REF-01008 --slug accessible-circulation-geometry --parameter-id 3 --identity MOB \
 --claim-type numerical --claimed-value "1:10.67" --claimed-unit ratio --comparator "=" --figure-role finding \
 --claim-text "Ramps #2, 3, 6, 7, 8 are unacceptable" \
 --source-section "A Study of Short Ramps -- Results, 1a Manual Wheelchair Users; Table 3, Gradient Ratings by Manual Wheelchair Users: Ascent" \
 --jurisdiction US --setting "curb ramp 6: 1:10.67, 8 ft (2.44 m) long, over a 9 in (22.85 cm) curb; ascent" \
 --extraction-method full-read --extraction-status verified \
 --root-type measurement_primary --root-ref-id REF-01008 --device-class manual_self_propelled \
 --root-population-note "Manual (self-propelled) wheelchair users; Table 2 lists 18, at least 16 of them aged 16-35." \
 --file-anchor "$PDF" --locator-scheme page --loc-section 17 --loc-note "Table 3 at printed page 17 = zero-based index 36, rendered; Table 1 at printed page 5 = index 24, rendered" \
 --relation tested_at --to-label "1:10.67 over a 9 in curb, 8 ft run (ramp 6)" --to-kind own_sample --stated named \
 --quote "Ramps #2, 3, 6, 7, 8 are unacceptable" \
 --notes "READ OFF THE RENDERED TABLE 3: ramp 6 (1:10.67, 8 ft, 9 in) -- subject mean 2.16, only 58 percent rating it 1 or 2, tester mean 2.42 -- below the report's ~80 percent acceptability line. Also unacceptable in ascent: ramp 3 (1:8, 4 ft, 6 in) 44 percent; ramp 8 (1:8, 6 ft, 9 in) 47 percent; ramp 7 (1:5.3, 4 ft, 9 in) 32 percent with two subjects unable. WHY THIS ROW EXISTS: THE GEOMETRY OF RAMP 6 IS THE GEOMETRY OF REF-01005 TABLE 13's 1:10 ROW. Table 13 (rendered this batch, 5dd866a236fb5978.p0056.png) allows 'If slope = 10.0% (1:10) or less steep' with a maximum run of 8 ft and a maximum rise of 9 in -- and 9 in over 8 ft is 1:10.67, ramp 6 exactly. The 1:8 row (2 ft run, 3 in rise) is likewise ramp 9 exactly. Both rows carry footnote c, 'Based on research of others (Templer, 1977 and Walters, 1971)'. So the combination Table 13 permits at its 1:10 band is one this report TESTED AND FOUND UNACCEPTABLE to manual wheelchair users in ascent, and its own Table 20 does not recommend 1:10 above a 6-inch curb. HELD AS AN OBSERVATION, NOT AN IDENTIFICATION: the two matching geometries are consistent with footnote c's Templer being this project's ramp work (tested Aug-Nov 1976, an interim report of which could carry 1977), but THIS REPORT IS DATED MAY 1980 and the referent is not identified -- candidate 115 stays PENDING. Walter's 10-ft recommendation reported on printed p.4 (1:9 self-propelled) is steeper than 1:10, so the band is bracketed by its two named warrants rather than taken from either."

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
 --notes "The conclusion Table 20 is built on, and the fourth independent statement of length-conditioning on parameter 3 in this corpus: REF-01002's 7 percent up to 20 ft, REF-01003's short-distance acceptability, REF-00996's mechanism (the greater the rise, the gentler the ramp, because the effort is sustained longer), and this. It is what a single maximum gradient without a length or rise cannot express, and it is why the 1:12 rows in this corpus do not contradict each other."

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
 --notes "WALTER'S RAMP AT SECOND HAND, FROM A SECOND INDEPENDENT READER. As printed: an adjustable indoor laboratory ramp, 20 ft at 1:8.6 to 1:16 and 10 ft at 1:5.5 to 1:10, rated on a four-point scale (easy, comfortable, difficult, impossible); recommended for SELF-PROPELLED wheelchairs 1:9 over 10 ft and 1:16 over 20 ft; for ASSISTANT-PROPELLED 1:9 over 10 ft and 1:12 over 20 ft. The page prints '10 foot (6.1 m)' in the assistant-propelled clause -- a unit slip in the source (10 ft is 3.05 m), recorded as printed. WHAT IT CORROBORATES: REF-01005 (extraction 54) reports that Walter and Steinfeld both found 1:16 over 20 ft accessible. Templer, writing independently, gives the same 1:16-over-20-ft figure for Walter. That corroborates the REPORT OF Walter by a second reader; it does NOT make Walter a second root, and v_value_independence must still count Walter once, and only when Walter itself is read. GAP-026 and the 2026-09-25 owner ruling: Walter itself is exhausted, so this second-hand account is the best text of Walter this project will hold for now."
