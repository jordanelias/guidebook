#!/usr/bin/env bash
# Batch 20 — repairs from the adversarial self-pass over the first data migration.
# Fix-forward (rule 3): the first migration is committed and immutable; these APPEND corrections.
set -euo pipefail
cd /home/user/guidebook/.claude/worktrees/agent-acceda5e0fdea113d
export GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/34e8c762-53ff-5f39-b746-3f5298058fcb/scratchpad/b20b.db
S=session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa

echo "== A1: extraction 59 over-claimed the source's reason =="
python3 scripts/db.py amend-extraction --extraction-id 59 --field extraction_status --value absent-confirmed --session "$S" \
 --reason "CORRECTION, SAME BATCH, BY ADVERSARIAL SELF-PASS. This row's notes say 'THE SOURCE SAYS WHY IT IS ABSENT' and that 'the omission is a design choice made for scale'. THE SOURCE DOES NOT SAY THAT. Its introduction gives a GENERAL reason large audits are rare -- tools that require 'measurement of slopes of ramps and widths of doors' are complex, 'As a consequence, few large-scale accessibility audits have been conducted' -- and it analyses a Ministry of Health census it did not design (PMAQ-AB, secondary data). Nothing in it states why PMAQ-AB's instrument asks about ramp presence and not gradient. What stands: the item is presence-only, so the row is correctly ABSENT on parameter 3, and the authors do connect slope measurement to audit complexity in general. What is withdrawn: the claim that this source explains THIS instrument's omission. The status is unchanged; only the reading is corrected."

echo "== A2: candidate 124's re-description carried the same over-claim =="
python3 scripts/db.py resolve-candidate --candidate-id 124 --disposition ADMITTED --admitted-ref-id REF-01007 --session "$S" \
 --redescription "CORRECTION TO THE RE-DESCRIPTION ABOVE, SAME BATCH. It says 'The authors give the reason in their introduction' and that 'the one national audit in this cluster bought its scale by not measuring gradient'. Over-read: the introduction explains why large audits are rare in general (slope and width measurement make tools complex), and the paper is a secondary analysis of a Ministry of Health census whose instrument its authors did not design; no sentence says why that instrument asks about ramp presence and not gradient. Presence-only and absent on parameter 3 stand; the causal claim is withdrawn. Extraction 59 carries the same correction."

echo "== A3: candidate 117's date reading =="
python3 scripts/db.py resolve-candidate --candidate-id 117 --disposition REHOME --session "$S" \
 --redescription "CORRECTION TO THE RE-DESCRIPTION ABOVE, SAME BATCH. It says 'the report was written two years before it was issued'. The title page prints 'February 1976' and 'Issued November 1978'; it does not say what the earlier date marks (drafting, contract completion, a period covered). Recorded as printed, without the inference. Everything else in the rehoming stands."

echo "== A4: candidate 129's locator said open access =="
python3 scripts/db.py resolve-candidate --candidate-id 129 --disposition PENDING-VERIFICATION --session "$S" \
 --redescription "CORRECTION TO THIS ROW'S LOCATOR, SAME BATCH (the row is otherwise unresolved). The locator says 'SciELO, open access'. Europe PMC's record for this DOI (persisted b7b928f29b468566.json) marks it isOpenAccess 'N', language 'por', and lists a free SciELO PDF (scielo.br/pdf/csc/v21n10/en_1413-8123-csc-21-10-3153.pdf). So: free to read on SciELO, not OA-licensed by Europe PMC's reckoning -- the same distinction candidate 123 turned on. Volume 21, issue 10, pages 3153-3160 are confirmed by that payload."

echo "== A5: exec 95's prior field mis-cited priors.md =="
python3 scripts/db.py amend-search --exec-id 95 --session "$S" \
 --append-note "CORRECTION TO THIS ROW'S prior_expectation, SAME BATCH. It says batch 19's warning about audits and title screens was 'carried into priors.md P1'. It was not: P1a-P1f are about what candidates 123 and 124 contain, and none mentions the title-screen blind spot. The honest reading of the prior field is its first sentence -- no per-pass prior was written -- and nothing more."

echo "== A6: GAP-033's grouping omitted one deferral =="
python3 scripts/db.py amend-gap --gap-id GAP-033 --session "$S" \
 --append-note "CORRECTION TO THE BATCH-20 NOTE ABOVE, SAME BATCH. It groups the deferrals into five questions, and the groups as listed account for all but one: observation 54 ('walking and reaching limitations', REF-01005's title) is a FUNCTIONAL-LIMITATION phrase whose only terms are the functional-axis rows TERM-031 and TERM-041 -- not an activity phrase, which is what group (2) names. It belongs with group (2) under a wider heading: phrases whose only possible targets are the functional-axis terms the owner called a bad coinage on 2026-08-18. Derive the membership rather than trusting either note: select o.observation_id, o.surface_form from observed_terms o join term_adjudications a using (observation_id) where a.outcome='DEFERRED' order by 1."
