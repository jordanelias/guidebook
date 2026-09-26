#!/usr/bin/env bash
# Batch 20 — REF-01007 backward mining pass: log the execution, stage what it surfaced,
# write the citation_mining row. Then resolve candidate 124 (R15).
set -euo pipefail
cd /home/user/guidebook/.claude/worktrees/agent-acceda5e0fdea113d
export GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/34e8c762-53ff-5f39-b746-3f5298058fcb/scratchpad/b20.db
S=session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa

OUT=$(python3 scripts/db.py log-search --slug accessible-circulation-geometry --language EN --engine crossref-deposit --depth-method scoping --session "$S" \
 --target-tier 3 --target-evidence-type clinical --target-scope lower_control --mining-direction backward \
 --query-text "BACKWARD MINING PASS over REF-01007 (Pinto, Koptcke, David and Kuper 2021, doi 10.3390/ijerph18062953): the publisher-deposited Crossref reference list (32 entries), persisted as retrieval-log/<session>/265e92157feb3c35.json; screened with python3 scripts/research/mining_screen.py --ref REF-01007 --compare, then every title read by eye because a title screen is blind to audits." \
 --prior-expectation "NONE RECORDED BEFORE THE PASS WAS READ, and this field says so rather than inventing one. The per-query priors file covers the Co-1/T2 leg only; this pass was run on admission without a written prior. The only relevant pre-registered statement is batch 19's own warning, carried into priors.md P1: an accessibility audit tabulates gradients while naming no geometry in its title, so slope-strict on an audit's reference list is expected to be blind." \
 --results-found 32 --results-screened 32 --results-admitted 0 --saturation-signal partial --harm-finding 1 \
 --findings-note "DERIVE THE SCREEN YIELD, DO NOT QUOTE IT: python3 scripts/research/mining_screen.py --ref REF-01007 --compare (slope-strict and slope-strict-plus-motion both 0 on this run; slope-loose fires on the accessibility stem). THE ZERO IS THE KNOWN BLIND SPOT, NOT A THIN LIST: reading the 32 titles and then fetching four abstracts (persisted b7b928f29b468566.json) found the audit literature a title screen cannot see. STAGED: Martins et al. 2016 (Ciencia e Saude Coletiva, doi 10.1590/1413-812320152110.20052016), 90 Family Health Units in Joao Pessoa audited against ABNT NBR 9050 -- its abstract reports 'only 47.8% have a wheelchair ramp, of these 30.0% have maximum slope', the first MEASURED-SLOPE compliance figure this pass has seen, wording ambiguous in translation; Mudrick et al. 2012 (Disability and Health Journal, doi 10.1016/j.dhjo.2012.02.002), 2,389 California primary care facilities on a 55-item on-site instrument -- exterior access 'generally met the access criteria', whether ramp slope is an item is not in the abstract. NOT STAGED, read and set aside: Nischith, Bhargava and Akshaya 2018 (J Family Med Prim Care, 67 PHCs in Dakshina Kannada, AIC checklist) reports ramp PRESENCE (60 of 67) in its abstract, the same shape as REF-01007; Frost et al. 2015 (JRRD, 30 clinics, ADA site assessments) reports restrooms and exam rooms, not ramps. harm_finding=1: every audit read reports inadequacy." \
 --session "$S")
echo "$OUT"
# exec_id from log-search's own JSON (stdout only; stderr NOTEs go to the terminal).
# Until 2026-09-26 this was a second `select max(exec_id)` query -- right on this
# single-writer scratch DB, wrong the moment anything else wrote a search in between.
EXEC=$(printf '%s' "$OUT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["exec_id"])')
echo "backward-pass exec_id=$EXEC"

python3 scripts/db.py add-candidate --exec-id "$EXEC" --found-under-slug accessible-circulation-geometry --suggested-slug accessible-circulation-geometry --disposition PENDING-VERIFICATION \
 --title "Martins et al. (2016) — Internal structure of Family Health Units: access for people with disabilities (Ciencia e Saude Coletiva 21(10))" \
 --locator "doi:10.1590/1413-812320152110.20052016 — deposited reference 13 in REF-01007's Crossref record; SciELO, open access. R9 PRE-CHECKED: not held." \
 --locator-status RESOLVED --tier-guess 3 --harm-finding 1 \
 --why-not-admitted "SCREENED ON ABSTRACT ONLY. The one audit in this cluster whose abstract reports a MEASURED SLOPE figure: 'of the 90 buildings evaluated, only 47.8% have a wheelchair ramp, of these 30.0% have maximum slope', against a checklist built on ABNT NBR 9050. The English is a translation and 'have maximum slope' is ambiguous -- it may mean within the permitted maximum, or at it. Do not extract a compliance rate from that sentence; read the Portuguese body." \
 --notes "Found by the REF-01007 backward pass, where the slope-strict title screen scored this reference 0. Portuguese-language full text likely (SciELO); R5 -- a peer-reviewed Brazilian journal article is academic literature, not grey." \
 --session "$S" 2>&1 | tail -3

python3 scripts/db.py add-candidate --exec-id "$EXEC" --found-under-slug accessible-circulation-geometry --suggested-slug accessible-circulation-geometry --disposition PENDING-VERIFICATION \
 --title "Mudrick, Breslin, Liang and Yee (2012) — Physical accessibility in primary health care settings: results from California on-site reviews (Disability and Health Journal 5(3))" \
 --locator "doi:10.1016/j.dhjo.2012.02.002 — deposited reference 7 in REF-01007's Crossref record. R9 PRE-CHECKED: not held." \
 --locator-status RESOLVED --tier-guess 3 --harm-finding 1 \
 --why-not-admitted "SCREENED ON ABSTRACT ONLY, AND ITS BEARING ON GRADIENT IS UNPROVEN. 2,389 primary care facilities rated by health-plan reviewers on a 55-item instrument (parking, exterior access, building entrance, interior, exam equipment). The abstract says exterior and building access 'generally met the access criteria' and puts the barriers in equipment and bathrooms. Whether ramp slope is one of the 55 items, and at what threshold, is exactly what must be read before this is admitted on parameter 3." \
 --notes "Scale is the reason to stage it: the largest on-site audit in the health-facility literature reachable from this pass. No author affiliation is in any payload this batch holds, so none is recorded; whether any author's role carries a Co-1 warrant is a question for the full text, never for memory or venue (D-0178)." \
 --session "$S" 2>&1 | tail -3

python3 scripts/db.py log-mining --slug accessible-circulation-geometry --ref REF-01007 --direction backward \
 --notes "PASS RAN ON ADMISSION against the publisher's Crossref deposit (32 references). DERIVE THE YIELD: python3 scripts/research/mining_screen.py --ref REF-01007 --compare. The slope screens score 0 and that is the documented audit blind spot, not a thin list: reading the titles and four abstracts surfaced two audits worth staging (candidates staged under exec $EXEC: Martins 2016, NBR 9050 slope compliance in 90 Brazilian units; Mudrick 2012, 2,389 California facilities). FORWARD NOT RUN: REF-01007 is T3 (clinical, lower_control) and R2's mandatory mining scope is confirmed T1-T2 anchors; recorded here in notes rather than as a deferral so the executed backward pass is not overwritten." \
 --session "$S" 2>&1 | tail -4
