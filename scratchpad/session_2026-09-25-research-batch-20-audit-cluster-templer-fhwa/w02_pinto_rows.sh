#!/usr/bin/env bash
# Batch 20 — REF-01007 (Pinto et al. 2021): payload-backed biblio fields, R13 match,
# the parameter-3 extraction (claim_type absent), term harvest, R15 resolution of candidate 124.
set -euo pipefail
cd /home/user/guidebook/.claude/worktrees/agent-acceda5e0fdea113d
export GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/34e8c762-53ff-5f39-b746-3f5298058fcb/scratchpad/b20.db
S=session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa
A=retrieval-log/$S/2c65a16afca1967b.xml

echo "== correct-source (values come from the logged Crossref payload, not from me) =="
python3 scripts/db.py correct-source --ref-id REF-01007 --field volume --field issue --field pages \
  --field journal_name --field publisher --log-session "$S" --session "$S" 2>&1 | tail -15

echo "== R13 population match =="
python3 scripts/db.py add-population-match --ref-id REF-01007 --target-population MOB \
 --study-population "No people. The unit of study is 38,812 public primary health care facilities (buildings) in Brazil, audited on site in May-October 2012 by researchers from 45 universities hired by the Ministry of Health, using a 22-item yes/no questionnaire (PMAQ-AB first cycle); this paper is a secondary analysis of that census. The items bearing on mobility-impaired users are the entrance sidewalk, floor, access ramp, handrail and wheelchair-accessible door/corridor items." \
 --sample-size 38812 --match-grade PROXY \
 --mismatch-note "PROXY BY R13's OWN LETTER: no participants. Unlike REF-01006, where every field investigator was a disabled person, nobody disabled took part in this measurement in any role -- the auditors were university researchers, and the authors list the absence of 'complementary qualitative data from people with disabilities' among the limitations. What the row can support is how often a FEATURE IS PRESENT, never whether a disabled person could use it. And on parameter 3 specifically it supports less than that: the ramp item is binary presence, so a facility scored as having an 'access ramp' may have one of any gradient." \
 --session "$S" 2>&1 | tail -4

echo "== extraction: parameter 3 x MOB, claim_type absent =="
python3 scripts/db.py add-extraction --ref-id REF-01007 --slug accessible-circulation-geometry --parameter-id 3 --identity MOB \
 --claim-type absent --figure-role finding \
 --claim-text "Does the health facility have access ramp?" \
 --source-section "2.2 Data Collection -- Table 1, Assessment criteria in accessibility audit, External sub-scale" \
 --jurisdiction BR --setting "public primary health care facilities (national census, 2012)" \
 --extraction-method full-read --extraction-status absent-confirmed \
 --root-type measurement_primary --root-ref-id REF-01007 \
 --measurement-paradigm field_observation --device-class not_device_scoped \
 --root-population-note "38,812 facilities observed on site by trained university researchers; no disabled participants." \
 --file-anchor "$A" --locator-scheme section --loc-section "2.2" --loc-note "Table 1, External sub-scale, sixth item" \
 --relation none \
 --notes "ABSENT IS THE FINDING, AND THE SOURCE SAYS WHY IT IS ABSENT. The largest accessibility audit in this corpus -- every public primary care facility in Brazil -- asks whether a ramp EXISTS and never what gradient it has. The authors state the reason in their introduction: 'Many of these tools are complex, requiring measurement of slopes of ramps and widths of doors, and so on. As a consequence, few large-scale accessibility audits have been conducted'. So the omission is a design choice made for scale, and it generalises: an audit can be national OR measure gradient, and this one chose national. RESULT ON THE ITEM (Table 3 and Results text): 'an access ramp (44%)' and 'a handrail at the entrance (8%)', better in the richer South/Southeast and in larger municipalities. WHAT THIS ROW MUST NOT BE READ AS: evidence that 44 percent of Brazilian primary care facilities have a USABLE ramp. A binary presence item cannot distinguish a 1:20 ramp from a 1:6 one, and REF-01005 measured that at 1:12 almost half of wheelchair users could not complete the run. It bears on parameter 3 only as a limit on what presence-counts can say. The authors also record that each feature 'was scored as yes or no, yet there may be variation in accessibility'." \
 --session "$S" 2>&1 | tail -6

echo "== observe-term (verbatim, unjudged) =="
python3 scripts/db.py observe-term --ref-id REF-01007 --surface-form "access ramp" --language en \
 --locator "2.2 Data Collection, Table 1 (External); Results" \
 --context-quote "Does the health facility have access ramp?" \
 --notes "The instrument's own name for the feature, recorded as a binary presence item. Harvested verbatim and UNJUDGED (D-0173)." \
 --session "$S" 2>&1 | tail -2
python3 scripts/db.py observe-term --ref-id REF-01007 --surface-form "accessibility audit" --language en \
 --locator "1. Introduction" \
 --context-quote "Accessibility audits can be used for monitoring purposes to understand whether facilities are adhering to certain standards" \
 --notes "The method's name as this source uses it -- a monitoring instrument against standards. Unjudged." \
 --session "$S" 2>&1 | tail -2
python3 scripts/db.py observe-term --ref-id REF-01007 --surface-form "external accessibility" --language en \
 --locator "Abstract; 2.3 Data Processing and Analysis" \
 --context-quote "three sub-scales: external accessibility (eight items), internal accessibility (eight items), information accessibility (six items)" \
 --notes "The source's sub-scale for the approach, entrance and ramp items. Unjudged." \
 --session "$S" 2>&1 | tail -2
