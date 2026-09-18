#!/usr/bin/env bash
# Batch 14 write replay. Run against a scratch DB with GUIDEBOOK_DB_PATH set.
#
# Includes TWO CAPTURE MISSES CARRIED OVER FROM BATCH 13, caught when the author
# asked whether the other relevant concepts were being logged as intended. They
# were not: batch 13 wrote 0 research_code_leads and 0 economics_entries while
# reading material that belonged in both. R12 says code values go to
# research_code_leads and economics to economics_entries, never to prose notes.
set -euo pipefail
: "${GUIDEBOOK_DB_PATH:?point this at the scratch DB}"
SID=session_2026-09-18-research-batch-14-co2-professional-bodies
SLUG=accessible-circulation-geometry
D=scripts/db.py
PRIOR='PRIORS.md (committed 6893397, before any query)'

# ---- 1. searches --------------------------------------------------------------
python3 $D log-search --slug $SLUG --language EN --jurisdiction INT \
 --query-text 'World Federation of Occupational Therapists WFOT position statement built environment accessibility ramp gradient' \
 --engine web --depth-method scoping --target-tier 2 --target-evidence-type co2 --target-scope international \
 --results-found 9 --results-screened 9 --results-admitted 0 --saturation-signal none \
 --prior-expectation "$PRIOR: a federation publishes position statements, not dimensions; a ramp gradient is a building-code fact and sits outside what an international federation asserts. Expect a well-formed zero." \
 --findings-note 'ZERO, AND R14 SAYS WHICH KIND: QUERY-SHAPE FAILURE FIRST, THEN A THIN GENUINE ABSENCE. The open-web query returned building-industry and access-board pages and not one wfot.org result, which is a query-shape result, not evidence about WFOT. Went to the source instead (R10): wfot.org/resources and wfot.org/search?q=ramp both returned 403; the Wayback rung on the query-string URL 404d; the rung on https://www.wfot.org/resources returned 200 (103053 bytes, sha256 b4b2be12...). That index lists WFOT resource categories -- Position Statements, Guidelines, Publications, Standards -- and its indexed text contains ZERO occurrences of ramp, gradient, slope, accessib*, housing or built environment. THAT IS WEAK EVIDENCE AND IS LABELLED AS SUCH: the page is a JavaScript-rendered navigation shell with only ~3800 characters of extractable text, so its silence is a rendering fact as much as a content fact. What can be said honestly: no WFOT gradient was found by open web search or by the retrievable resource index, and WFOT remains the least-searched of the three bodies. NOT saturated.' \
 --session "$SID"

# ---- 2. the admission ---------------------------------------------------------
python3 $D add-source --ref-id REF-00998 \
 --author 'corp|Occupational Therapy Australia' --year 2025 \
 --title 'FAQ: Environmental and Home Modifications' \
 --tier 5 --evidence-type national_fw --scope intrinsic --jurisdiction AU \
 --url 'https://otaus.com.au/resources/faq-environmental-and-home-modifications' \
 --url-accessed 2026-09-18 --doi-resolution-outcome NO-MATCH \
 --pages 'FAQ › How should AS1428.1 be applied?' \
 --lang-detected EN --lang-detection-method 'page is English throughout' \
 --metadata-quality COMPLETE --verification-method direct-render \
 --verification-status VERIFIED --verified-by-tool 'retrieval_log.fetch' \
 --slug $SLUG --local-ref-id 17 --session "$SID"

# The admitting search is logged AFTER the source: db.py refuses --admitted-ref-id
# for a ref that does not yet exist, which is the right order and the right refusal.
python3 $D log-search --slug $SLUG --language EN \
 --query-text 'ramp gradient slope home modification accessibility' \
 --engine web --depth-method systematic --target-tier 2 --target-evidence-type co2 --target-scope national \
 --results-found 10 --results-screened 10 --results-admitted 1 --admitted-ref-id REF-00998 --saturation-signal partial \
 --prior-expectation "$PRIOR: CAOT will defer to the National Building Code of Canada if it addresses gradient at all; Occupational Therapy Australia is the most likely of the three to state something, and for that same reason most likely to point at AS 1428.1 rather than carry its own number." \
 --findings-note 'DOMAIN-SCOPED TO wfot.org, caot.ca AND otaus.com.au -- jurisdiction deliberately OMITTED because the query spanned three. This is the query that worked, and the per-body outcome is the finding. CAOT: "OT PRACTICE DOCUMENT: Home Assessment and Modifications", Spring 2024, retrieved (200, 203046 bytes, sha256 81fc675f...) and READ IN FULL -- 2 pages. The word "ramp" occurs ONCE, in a list of what an OT recommends ("bar grabs, handrails, ramps, raised toilet seats"). gradient, slope, 1:12 and 1:20 occur ZERO times. Its companion HomeModification_FactSheet.pdf (200, 122223 bytes) contains none of them either. A national OT professional body practice document on home modification names the ramp and states no dimension: that is RCOT Adaptations without Delay replicated in Canada, and it is a GENUINE ABSENCE, fully read, not a retrieval failure. OTA: FAQ Environmental and Home Modifications, admitted REF-00998 -- see that row. NOT admitting CAOT: it holds no extraction for parameter 3, and admitting a source to carry a zero is not what evidence_sources is for; batch 12 treated its four Co-1 zeroes the same way.' \
 --session "$SID"


# THE SCOPE LIMITATION, which bears directly on the threshold this cell rests on.
python3 $D add-extraction --ref-id REF-00998 --slug $SLUG --parameter-id 3 \
 --identity MOB --claim-type qualitative \
 --claimed-value 'AS 1428.1 does not apply to private dwellings; it governs Class 2-9 buildings' \
 --claim-text 'AS 1428.1:2021 provides the minimum design requirements for building work to enable access for people with disabilities in Class 2-9 buildings. As such, it does not apply to Class 1 and 2 buildings, which are single dwellings (like houses) and those with multiple units (like apartments), respectively.' \
 --source-section 'How should AS1428.1 be applied?' --jurisdiction AU --setting 'private dwellings (Class 1 and 2)' \
 --extraction-method full-read --extraction-status verified --figure-role finding --relation none \
 --notes 'THIS QUALIFIES THE THRESHOLD REF-00997 APPLIES, AND IT IS WHY THIS PAGE WAS ADMITTED AT ALL. REF-00997 (SA prescriber guidance) recommends 1:14 and 1:8 for ramps at private homes and grounds those figures in AS 1428.1. The Australian professional body states that AS 1428.1 DOES NOT APPLY to Class 1 and 2 buildings -- houses and apartments. So the figure governing home ramps in that document is borrowed from a standard that formally excludes homes. REF-00997 half-acknowledges this in its own words ("As ramps are generally on the outside of a building, even a ramp at a private home is likely to be accessed by members of the public at times"), which is a rationale for borrowing it, not a claim that it applies. Recorded as a finding, not a claim: it states no gradient and supplies no value. It reaches a determination only through the proxy branch (086), and REF-00998 is T5 so it is not an anchoring-tier finding either -- it changes no number. What it changes is what a reader should believe about the number.' \
 --session "$SID"

python3 $D add-population-match --ref-id REF-00998 --target-population MOB \
 --study-population 'No study population — a professional association FAQ explaining the scope of a standard; no participants, no measurement' \
 --match-grade PROXY \
 --mismatch-note 'PROXY on the same ground as every regulatory-stratum row in this cell. Noted because the tier call here was the batch question: Occupational Therapy Australia IS the OT professional body, so Co-2 was live. Refused because Co-2 in governance/tier-system.md means professional-body CLINICAL PRACTICE GUIDELINES, and an FAQ page explaining an Australian Standard is not a CPG -- it carries no clinical warrant, no consensus process and no cited evidence. Admitting it Co-2 would have given this batch the Co-2 source it was convened to find, which is exactly why it was refused.' \
 --session "$SID"

python3 $D observe-term --ref-id REF-00998 --surface-form 'Class 1 and 2 buildings' --language EN \
 --locator 'How should AS1428.1 be applied?' \
 --context-quote 'it does not apply to Class 1 and 2 buildings, which are single dwellings (like houses) and those with multiple units (like apartments), respectively' \
 --notes 'THE CATEGORY THAT DECIDES WHETHER THE THRESHOLD APPLIES. A building-classification term doing load-bearing work on an accessibility question: whether a ramp gradient standard reaches the place a disabled person actually lives. Recorded verbatim and unjudged (D-0173).' \
 --session "$SID"
python3 $D observe-term --ref-id REF-00998 --surface-form 'Livable Housing Design Standard' --language EN \
 --locator 'What are the Livable Housing Design requirements?' \
 --context-quote 'Livable Housing Guidelines are advisory' \
 --notes 'The advisory instrument that occupies the space AS 1428.1 vacates for private dwellings. Named by the professional body as the thing to consider when the mandatory standard does not apply. Unjudged (D-0173).' \
 --session "$SID"
python3 $D observe-term --ref-id REF-00998 --surface-form 'private dwellings' --language EN \
 --locator 'What guidelines or standards should be considered when renovating or modifying private dwellings?' \
 --context-quote 'While AS1428.1 does not apply to private dwellings, and Livable Housing Guidelines are advisory' \
 --notes 'The setting this whole parameter is about for a home ramp, and the setting both instruments decline to bind. Unjudged (D-0173).' \
 --session "$SID"

# ---- 3. R12 CAPTURE THAT BATCH 13 OWED -----------------------------------------
# CODE LEADS. Batch 13 admitted REF-00997 whose entire warrant is AS 1428.1 and
# filed no lead. Six AS 1428.1 leads exist from the 2026-09-02 restore, but none
# carries the ramp-gradient clause and none was raised by this line of work.
python3 $D add-code-lead --jurisdiction AU --standard-name 'AS 1428.1:2021 — ramp gradients, landings and handrails' \
 --status REFERENCE-ONLY \
 --notes 'RAISED LATE, AND THE LATENESS IS THE POINT. Batch 13 admitted REF-00997, whose 1:14 and 1:8 recommendations are grounded in AS 1428.1, and filed no code lead at all -- R12 says code values go here, not into prose notes. Batch 14 adds it because the author asked whether the other concepts were being captured and the answer was no. WHAT IS STILL UNRETRIEVED: the clause and its value. Neither REF-00997 nor REF-00998 quotes a gradient FROM the standard -- REF-00997 states its own recommendation and REF-00998 says only that "the standard specifies requirements for ramp gradients, landings, and handrails". The standard is paywalled at Standards Australia (REF-00998 links the catalogue page), so this stays REFERENCE-ONLY under the 2026-08-12 ruling. SCOPE CAVEAT recorded with the lead: REF-00998 states AS 1428.1 does not apply to Class 1 and 2 buildings, so retrieving this clause gives a figure for public buildings, not homes.' \
 --session "$SID"
python3 $D add-code-lead --jurisdiction AU --standard-name 'Livable Housing Design Standard (NCC, 2022)' \
 --status REFERENCE-ONLY \
 --notes 'The instrument that covers private dwellings, which AS 1428.1 does not. Named by Occupational Therapy Australia (REF-00998), which also records that the Livable Housing Guidelines are ADVISORY. Surfaced with a direct URL in the FAQ (ncc.abcb.gov.au/sites/default/files/resources/2023/livable-housing-design-20221219.pdf) and NOT retrieved by this batch -- staged honestly rather than described from a link. If it states a gradient for dwellings it is the first instrument in this corpus that governs the setting a home ramp is actually in.' \
 --session "$SID"

# ECONOMICS. Read in batch 13, left in prose. R12: economics go here.
python3 $D add-economics-entry --entry-id ECON-001 --pillar construction --entry-type research_gap \
 --source 'Foundations (national body for home improvement agencies, England), "Guidance For Ramp Adaptations" — retrieved by session_2026-09-18-research-batch-13-co2-occupational-therapy via the R10 Wayback ladder, snapshot 2023-12-07, sha256 b201d3bea81d54e1e509e7d18d02ddc67227e5fa83c5e5e10f2741ddea6920d3' \
 --jurisdiction GB --status OPEN \
 --finding 'There is little research investigating the cost comparison between rampscaping, traditional ramps and lifts.' \
 --notes 'AN ABSENCE OF EVIDENCE, STATED BY A NATIONAL BODY, AND THEREFORE FIRST-CLASS (R7). Captured LATE: batch 13 read this sentence, used the page for a different purpose -- falsifying a gradient attribution -- and left the economics finding in prose, which R12 forbids. Filed here rather than backdated into batch 13, because the migration carrying that batch is committed and rule 3 is fix-forward. The page continues: "In general, the steeper the land around the home the more complex and expensive rampscaping would be. On flatter sites grading a tonne of topsoil is likely to cost much less than edging kerbs and handrails." That is a directional cost claim with no figure, which is why value_numeric is empty and the entry_type is research_gap rather than cost_premium. NOT ADMITTED AS A SOURCE: the Foundations page is resolved OUT-OF-SCOPE for parameter 3 (candidate 72), so this entry carries --source rather than a ref_id.' \
 --session "$SID"

# ---- 4. candidates -------------------------------------------------------------
python3 $D add-candidate --found-under-slug $SLUG --disposition MISCELLANEOUS \
 --title 'CAOT, "OT PRACTICE DOCUMENT: Home Assessment and Modifications", Spring 2024 — the Canadian national OT professional body practice document. READ IN FULL (2 pages) and it states NO ramp gradient: "ramp" appears once, in a list of recommended modifications, and gradient/slope/1:12/1:20 appear zero times. Recorded so the next session does not re-retrieve it expecting a figure.' \
 --locator 'https://caot.ca/document/8205/Home%20Assessment%20and%20Modifications%20EN.pdf' \
 --locator-status RESOLVED --tier-guess 2 --harm-finding 0 \
 --why-not-admitted 'Holds no extraction for parameter 3. It is the closest document in this corpus to a Co-2 CPG -- a national professional body practice document -- and it is silent on the dimension, which is a finding about the evidence base rather than evidence about a gradient. Batch 12 treated its four Co-1 zeroes the same way: recorded, not admitted.' \
 --session "$SID"

python3 $D add-candidate --found-under-slug $SLUG --disposition PENDING-VERIFICATION \
 --title 'WFOT (World Federation of Occupational Therapists) resource library — the international federation, and the LEAST searched of the three professional bodies this batch targeted. R15 HYPOTHESIS, UNTESTED: a federation publishes position statements on occupational justice and professional scope, not building dimensions, so a gradient is unlikely to exist. That is a prediction, not a result.' \
 --locator 'https://wfot.org/resources' --locator-status UNVERIFIED --tier-guess 2 --harm-finding 0 \
 --why-not-admitted 'RETRIEVAL LIMITATION, NOT ABSENCE. wfot.org returns 403; the Wayback rung on the resources index returned 200 but the page is a JavaScript-rendered shell with ~3800 characters of extractable text, so its silence on ramp/gradient/accessibility is a rendering fact as much as a content fact. Untried rungs: the members area, WFOT position statements as individually-linked PDFs, and the WFOT Bulletin in a journal index.' \
 --session "$SID"
echo "REPLAY COMPLETE"

# ---- 5. retire and re-determine ------------------------------------------------
# CAUGHT ON THE SCRATCH DB BEFORE EMITTING, which is the procedure batch 13's
# attestation said to adopt after it learned the hard way. K02 ("every pilot-3
# determination accounts for every extraction of its parameter") failed the moment
# extraction 36 existed: specification 6 was computed before it and cannot account
# for it. New evidence for the parameter means the cell is re-determined.
python3 $D retire-specification --specification-id 6 \
 --reason 'New evidence arrived for parameter 3. REF-00998 (Occupational Therapy Australia) adds a finding: AS 1428.1 does not apply to private dwellings, which qualifies the standard REF-00997 grounds its home-ramp recommendations in. A determination is computed from the evidence set that existed when it ran; this one predates that row. Retired so the cell can be re-determined, not because its value was found wrong.' \
 --session "$SID"
