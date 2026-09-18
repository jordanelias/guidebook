#!/usr/bin/env bash
# Batch 13 write replay. Every row this batch adds, in order, against a scratch DB.
#
# WHY THIS FILE EXISTS. The first pass of this batch was written interactively and
# tripped two BLOCKING gates after the migration had already been applied:
#   * test_db_integrity C04 -- REF-00997 was metadata_quality=COMPLETE with no doi and
#     no doi_resolution_outcome, so it had no acceptable explanation for the absence.
#   * extraction_relations_integrity -- extraction 35 (the 1:8 small-rise case) was a
#     figure_role='condition' that qualified nothing. It was written with --relation
#     none because condition_on demands a row this project holds, and the condition was
#     read as the prose threshold "rise <190mm". That reading was wrong: what the
#     exception qualifies is its SIBLING CLAIM, the 1:14 general rule, exactly as
#     REF-00990 extraction 23 condition_on 22 already does for the Japanese proviso.
# Neither migration had been committed, so both are fixed at source here rather than
# left as a compensating migration for an error that never reached main.
set -euo pipefail
: "${GUIDEBOOK_DB_PATH:?point this at the scratch DB}"
SID=session_2026-09-18-research-batch-13-co2-occupational-therapy
SLUG=accessible-circulation-geometry
D=scripts/db.py
PRIOR='PRIORS.md (committed 3db5769, before any query)'

EX='ARTEFACT IS PERSISTED BUT NOT UTF-8 DECODABLE. Payload: retrieval-log/session_2026-09-18-research-batch-13-co2-occupational-therapy/1d4ebe3dd57422e2.doc, 159744 bytes, application/msword, HTTP 200 via the R10 Wayback ladder after the live URL returned 403. Legacy OLE compound document encoded CP1252, so the verbatim checker classifies it NOT SEARCHED (not valid UTF-8, no charset declaration) and cannot see text that IS present in the bytes. Re-derivable in one line: open(path,"rb").read().decode("cp1252") then search for the sentence. NOT exempt because the text was unretrievable -- exempt because the checker cannot read a format it was handed. A UTF-8 rendition was deliberately NOT generated to satisfy the gate: an artefact this session wrote itself would make the check circular.'
AS='CONTEXT, RECORDED HERE BECAUSE IT IS NOT AN EDGE. The document opens "Refer to the Australian Standard for Design for Access and Mobility (AS 1428.1) section on walkways, ramps and landings" and says "wherever possible, any ramp complies with AS 1428.1", adding that where space or a client disability-related need prevents compliance "the clinical reasoning for this should be thoroughly documented by the prescriber". That is FRAMING, not a comparator edge: the writer refuses audited_against on a figure_role=claim precisely because auditing against a baseline asserts no absolute value of its own, and this document does state its figure. AS 1428.1 is not a row this project holds, so no derived_from edge can be written either. No derivation is asserted: the document never says these figures are lifted from the standard.'

# ---- 1. the three zero-yield / context searches -----------------------------------
python3 $D log-search --slug $SLUG --language EN --jurisdiction GB \
 --query-text 'Royal College of Occupational Therapists housing adaptations guidance ramp gradient slope wheelchair' \
 --engine web --depth-method scoping --target-tier 2 --target-evidence-type co2 --target-scope national \
 --results-found 10 --results-screened 10 --results-admitted 0 --saturation-signal saturated \
 --prior-expectation "$PRIOR: OT professional guidance is about the assessment, not the dimension; expect no gradient from the UK professional body." \
 --findings-note 'ZERO, AND IT REPRODUCES A RESULT ALREADY IN THE DB. Batch 09 read Adaptations without Delay in full and found no gradient anywhere; this pass surfaced the same ecosystem (RCOT, Housing LIN, The OT Practice) and no RCOT-authored gradient. R14 shape: well-formed query, correct index, GENUINE ABSENCE. Its value is the delegation chain it surfaced -- RCOT delegates ramp design to Foundations, and Foundations (see the GB national_fw search in this batch) delegates to Approved Document M. The chain from the OT professional body to a gradient terminates at the building regulator with no OT-discipline warrant at any link.' \
 --session "$SID"

python3 $D log-search --slug $SLUG --language EN --jurisdiction US \
 --query-text 'AOTA occupational therapy practice guidelines home modifications ramp slope recommendation' \
 --engine web --depth-method scoping --target-tier 2 --target-evidence-type co2 --target-scope national \
 --results-found 9 --results-screened 9 --results-admitted 0 --saturation-signal partial \
 --prior-expectation "$PRIOR: where an OT CPG does state a gradient, expect it to RESTATE A NATIONAL CODE rather than carry its own warrant." \
 --findings-note 'ZERO ADMITTED; candidate 73 UNCHANGED and still an R14 RETRIEVAL FAILURE (library.aota.org member-gated). PRIOR SUPPORTED BUT NOT FROM THE SOURCE: third parties describe the AOTA guideline as addressing "ramp slope specifications according to ADA vs state codes", and one page asserts 1:12 "according to occupational therapy home modification standards". BOTH ARE THIRD-PARTY CHARACTERISATIONS, NOT THE CPG, and nothing was admitted or re-described from them (R15, CLAUDE.md 5(c)). Ladder rungs still untried: WorldCat, Google Books preview, archived NGC summary (ISBN 9781569003572).' \
 --session "$SID"

python3 $D log-search --slug $SLUG --language EN --jurisdiction GB \
 --query-text 'Foundations "Guidance for Ramp Adaptations" home improvement agencies England ramp gradient 1:15 1:12 PDF' \
 --engine web --depth-method systematic --target-tier 5 --target-evidence-type national_fw --target-scope national \
 --results-found 9 --results-screened 9 --results-admitted 0 --saturation-signal saturated \
 --prior-expectation "$PRIOR target 1: expect rise/length-conditioned gradients, and expect T5 national_fw rather than Co-2 because Foundations is the national body for home improvement agencies, not an OT professional body." \
 --findings-note 'THE SNIPPET WAS WRONG AND THE RETRIEVAL PROVED IT. The search index attributes to this page "ramps up to 10m: 1 in 15; up to 5m: 1 in 12". Retrieved (live URL 403 Cloudflare; R10 ladder to Wayback, 200, 69711 bytes, sha256 b201d3be..., snapshot 2023-12-07): the page contains ZERO instances of 1:15, 1:12, 10m or 5m. It states 1:20 as the walkway/ramp BOUNDARY ("For a walkway to be considered accessible, the gradient (slope) must not be steeper than 1:20. A gradient steeper than 1:20 would be considered a ramp") and 1:40 crossfall, then DELEGATES ramp design to Charnwood Borough Council guidance and Approved Document M. Batch 09 candidate 72 called this page "the apparent source of the 1:15/1:12 length-conditioned figures" -- FALSIFIED, and the candidate is re-described per R15. NOT ADMITTED for parameter 3: its 1:20 is a definitional boundary for walkways, not a ceiling on ramps, and filing it as a ramp maximum is the copy rule 5 forbids. CAVEAT: this holds for the 2023-12-07 snapshot; the live page is blocked and unverified.' \
 --session "$SID"

# ---- 2. the admission ------------------------------------------------------------
# --doi-resolution-outcome NO-MATCH: C04 requires a COMPLETE row without a doi to carry
# an acceptable explanation. A 2013 state-government .doc has no DOI and never had one;
# NO-MATCH is the recorded fact, matching REF-00993/94/96.
python3 $D add-source --ref-id REF-00997 \
 --author 'corp|DCSI Equipment Program' --year 2013 \
 --title 'Equipment Program Clinical Considerations for Prescribers — Home Modifications: Ramps' \
 --tier 5 --evidence-type national_fw --scope intrinsic --jurisdiction AU \
 --url 'https://des.sa.gov.au/__data/assets/word_doc/0011/21044/ramps-clinical-considerations-for-prescribers.doc' \
 --url-accessed 2026-09-18 --pages '3' --doi-resolution-outcome NO-MATCH \
 --lang-detected EN --lang-detection-method 'document body is English throughout' \
 --metadata-quality COMPLETE --verification-method direct-render \
 --verification-status VERIFIED --verified-by-tool 'retrieval_log.fetch' \
 --slug $SLUG --local-ref-id 16 --session "$SID"

python3 $D log-search --slug $SLUG --language EN --jurisdiction AU \
 --query-text 'Australian Home Modification Guidelines occupational therapy evidence-based ramp gradient wheelchair slope recommendation' \
 --engine web --depth-method scoping --target-tier 2 --target-evidence-type co2 --target-scope national \
 --results-found 10 --results-screened 10 --results-admitted 1 --admitted-ref-id REF-00997 --saturation-signal partial \
 --prior-expectation "$PRIOR target 4: bodies never searched (CAOT, OT Australia, WFOT) are where a genuine Co-2 admission could still come from; R5 applies." \
 --findings-note 'ONE ADMISSION, AND IT IS NOT Co-2. SWEP (Victoria) Practitioner Manual: DEAD LINK -- HTTP 200 with a 20-byte body reading "File does not exist."; staged as a candidate. SA Equipment Program "Ramps - Clinical Considerations for Prescribers": live URL 403 Cloudflare, R10 ladder to Wayback 200, 159744 bytes application/msword, sha256 1d4ebe3dd57422e2. States a rise-conditioned pair (1:8 step ramps rise <190mm; 1:14 long ramps rise >190mm) AND an individualisation duty: "Assess the client s/carer s ability to propel the wheelchair over this gradient as some clients may require a less steep gradient." Admitted REF-00997 at T5 national_fw, NOT Co-2: a state government equipment program is not an OT professional body, and the document grounds itself in AS 1428.1 -- the 2026-09-13 ruling puts value-restating material in the regulatory stratum. STILL ZERO Co-2 IN THE CORPUS, now for a third recorded reason.' \
 --session "$SID"

# ---- 3. extractions: finding (33), claim (34), condition (35) ----------------------
python3 $D add-extraction --ref-id REF-00997 --slug $SLUG --parameter-id 3 \
 --identity MOB --needs A-EFFORT --claim-type qualitative \
 --claimed-value 'the prescriber must assess whether this client can propel over the recommended gradient; some require gentler' \
 --claim-text 'Assess the client’s/carer’s ability to propel the wheelchair over this gradient as some clients may require a less steep gradient.' --verbatim-exempt "$EX" \
 --source-section 'Ramp gradient' --jurisdiction AU --setting 'home environment (domiciliary equipment prescription)' \
 --extraction-method full-read --extraction-status verified --figure-role finding --relation none \
 --notes 'THE SECOND CRITERION-OF-ACCEPTABILITY STATEMENT IN THE CORPUS, AND THE FIRST PLACING THE DUTY ON A NAMED CLINICIAN. REF-00996 (Flemish handbook) states the criterion as a design principle -- physical feasibility for the independently self-propelling wheelchair user is the starting point. This states it as an OPERATIONAL DUTY: the tabulated gradient is a default and the prescriber must test it against this client. It names no number, so it is a finding and reaches a determination only through the proxy branch (086). SECOND LENS DELIBERATE: A-EFFORT ("cost little energy... rest points", absorbing fatigue, pain, cardiac/respiratory) is what an ability-to-propel assessment is about, and every other parameter-3 extraction carries identity_code MOB and nothing else. R4 asks for the combinatorial dimension; this is one honest step, not a backfill of the other 22 rows. VERBATIM NOTE: claim_text carries U+2019 apostrophes as the CP1252 bytes do; an ASCII-stripped reading rendered them as spaces and was discarded as a decode artefact, not a quotation.' \
 --session "$SID"

python3 $D add-extraction --ref-id REF-00997 --slug $SLUG --parameter-id 3 \
 --identity MOB --claim-type numerical --claimed-value '1:14' --claimed-unit 'rise:run ratio' --comparator '<=' \
 --claim-text 'For long ramps with rise >190mm, the recommended gradient is 1:14.' --verbatim-exempt "$EX" \
 --source-section 'Ramp gradient' --jurisdiction AU --setting 'home environment (domiciliary equipment prescription)' \
 --extraction-method full-read --extraction-status verified --figure-role claim --relation none \
 --notes "COMPARATOR IS <=, NOT A POINT, AND THE SOURCE WARRANTS IT. The sentence carries no comparator of its own; read as a POINT it would contribute a floor as well as a ceiling and produce exactly the incoherent interval assess_cell now refuses (the REF-00987 defect). Two sentences in the same document make <= honest: 'some clients may require a less steep gradient' (gentler is expressly in scope) and 'wherever possible, any ramp complies with AS 1428.1' (the figure is a compliance ceiling). $AS" \
 --session "$SID"

python3 $D add-extraction --ref-id REF-00997 --slug $SLUG --parameter-id 3 \
 --identity MOB --claim-type numerical --claimed-value '1:8' --claimed-unit 'rise:run ratio' --comparator '<=' \
 --claim-text 'For step ramps with rise <190mm, the recommended gradient is 1:8.' --verbatim-exempt "$EX" \
 --source-section 'Ramp gradient' --jurisdiction AU --setting 'home environment (domiciliary equipment prescription)' \
 --extraction-method full-read --extraction-status verified --figure-role finding --relation none \
 --notes "FIGURE_ROLE IS finding, FOLLOWING REF-00992 EXTRACTION 26 AND REF-00994 EXTRACTION 29 -- NOT condition. The first pass filed this as a condition by analogy to REF-00990 extraction 23, the Japanese 8-fold proviso, and that analogy was wrong twice over. Substantively: 00990's row is a ただし書 proviso EXCEPTING a stated ceiling, whereas these two sentences are PARALLEL BRANCHES of one rule split at a rise threshold, which is the shape Approved Document M's gradient table and the IPC's two grades already have -- and both of those are filed finding, with no edges. Procedurally: extraction_relations_integrity requires a condition to qualify a row, relate-extraction requires a --quote, and the quote byte-check cannot read this CP1252 artefact, so a condition here was unwritable-with-edge and failed the blocking check. The precedent and the toolchain point the same way, and the precedent is the reason -- see the gap registered by this session for the toolchain half. A small-rise exception is not the parameter general rule, and admitting it as a claim would put a 12.5 percent ceiling into the governing set on a parameter whose current selection is 5 percent. A coincidence worth not over-reading: JP and AU both land on 1:8 for the small-rise case, at different thresholds (160mm vs 190mm), from unrelated instruments. $AS" \
 --session "$SID"

# ---- 4. R13, R11, candidates ------------------------------------------------------
python3 $D add-population-match --ref-id REF-00997 --target-population MOB \
 --study-population 'No study population — a state equipment programme stating prescription guidance for clinicians; no participants, no measurement, no citation' \
 --match-grade PROXY \
 --mismatch-note 'PROXY on the same ground as REF-00987/94/95/96: an institution stating what wheelchair users need, with nobody in the room. Worth naming precisely because this document comes closest in the corpus to speaking for an individual disabled person -- it instructs the prescriber to assess THIS client and permits a gentler gradient for them. That is an individualisation DUTY, not evidence about a population, and it does not raise the grade. The document tells a clinician to go and find out; it does not report having found out.' \
 --session "$SID"

python3 $D observe-term --ref-id REF-00997 --surface-form 'step ramp' --language EN --locator 'Ramp gradient' \
 --context-quote 'For step ramps with rise <190mm, the recommended gradient is 1:8.' \
 --notes 'A DEVICE CLASS USED AS A GRADIENT BAND. The document splits its recommendation on "step ramp" vs "long ramp" at a 190mm rise, so the phrase does real work: it names the object whose permitted gradient is 1:8 rather than 1:14. Whether it names one of our concepts is for judgment (D-0173); recorded verbatim and unjudged.' \
 --session "$SID"
python3 $D observe-term --ref-id REF-00997 --surface-form 'long ramp' --language EN --locator 'Ramp gradient' \
 --context-quote 'For long ramps with rise >190mm, the recommended gradient is 1:14.' \
 --notes 'The complement of "step ramp" in the same sentence pair, and the carrier of this document governing figure. Recorded verbatim and unjudged (D-0173).' \
 --session "$SID"
python3 $D observe-term --ref-id REF-00997 --surface-form 'prescriber' --language EN --locator 'Australian Standards; Ramp gradient' \
 --context-quote 'the clinical reasoning for this should be thoroughly documented by the prescriber' \
 --notes 'THE ACTOR THE WHOLE DOCUMENT ADDRESSES, and the reason this source is interesting to the Co-2 question even though it is not Co-2. "Prescriber" is a clinical role and the document assigns the gradient decision to it -- including authority to depart from AS 1428.1 on documented clinical reasoning. No other source in this corpus names a person who decides. Unjudged (D-0173).' \
 --session "$SID"

python3 $D resolve-candidate --candidate-id 72 --disposition OUT-OF-SCOPE \
 --redescription 'RETRIEVED AND READ. Live URL 403 (Cloudflare); R10 ladder to Wayback succeeded — snapshot 2023-12-07, HTTP 200, 69711 bytes, sha256 b201d3bea81d54e1e509e7d18d02ddc67227e5fa83c5e5e10f2741ddea6920d3. THE STAGED HYPOTHESIS IS FALSIFIED. Candidate 72 called this page "the apparent source of the 1:15/1:12 length-conditioned figures the search index shows". The retrieved document contains ZERO instances of 1:15, 1:12, 10m or 5m. Its headings are Rampscaping, Rampscaping in practice, Additional considerations, Ramp calculations, Regulations and guidance, Level Access Thresholds. What it states is a BOUNDARY, not a ceiling: "For a walkway to be considered accessible, the gradient (slope) must not be steeper than 1:20. A gradient steeper than 1:20 would be considered a ramp and require all associated ramped requirements such as handrails and kerbs", plus crossfall "no steeper than 1:40". For ramp design it DELEGATES — to a Charnwood Borough Council guide and to Approved Document M, already held as REF-00992. OUT-OF-SCOPE for parameter 3: its 1:20 defines when a walkway becomes a ramp, and filing that as a ramp maximum is the copy rule 5 forbids. THE FINDING IS THE DELEGATION CHAIN: RCOT delegates ramp design to Foundations; Foundations delegates it to the building regulator. The chain from the UK OT professional body to a gradient terminates outside the profession. CAVEAT: falsified against the 2023-12-07 snapshot; the live page is blocked and unverified.' \
 --session "$SID"

python3 $D add-candidate --found-under-slug $SLUG --disposition PENDING-VERIFICATION \
 --title 'SWEP (Statewide Equipment Program, Victoria), "Practitioner Manual for Home Modifications" — the Victorian counterpart to the South Australian prescriber guidance admitted as REF-00997. HYPOTHESIS PER R15: expect prescriber-facing home-modification guidance stating a ramp gradient grounded in AS 1428.1, i.e. a second state-level instance of the same shape, not a Co-2 source. UNVERIFIED — not read.' \
 --locator 'https://swep.bhs.org.au/files/320/SWEP_Home_Modifications_Prescriber_Manual.pdf' \
 --locator-status DEAD --tier-guess 5 --harm-finding 0 \
 --why-not-admitted 'DEAD LINK, AND THE FAILURE MODE IS WORTH RECORDING: the URL returns HTTP 200 with a 20-byte body reading "File does not exist." A status-code-only check would score this as a successful retrieval. retrieval_log persisted it (sha256 f056e72fad232b2e), so the artefact shows what actually arrived. R14: a RETRIEVAL failure, not evidence of absence.' \
 --session "$SID"

python3 $D add-candidate --found-under-slug $SLUG --disposition PENDING-VERIFICATION \
 --title 'AOTA, "Occupational Therapy Practice Guidelines for Home Modifications" (Siebert, Smallfield, Stark) — LADDER RUNGS FOR CANDIDATE 73, which batch 09 left at member-gated. This is a BOOK, ISBN 9781569003572, so the untried rungs are WorldCat, a Google Books preview, and the archived National Guideline Clearinghouse summary. R15 HYPOTHESIS, UNREAD: third-party descriptions say it addresses "ramp slope specifications according to ADA vs state codes", which if true makes it code-restating and therefore regulatory-stratum under the 2026-09-13 ruling rather than an anchoring Co-2 CPG. THAT IS A HYPOTHESIS ABOUT A DOCUMENT NOBODY IN THIS PROJECT HAS READ.' \
 --locator 'ISBN 9781569003572' --locator-status UNVERIFIED --tier-guess 2 --harm-finding 0 \
 --why-not-admitted 'Still not retrieved. Batch 09 recorded the library.aota.org block and stopped; R10 says a publisher block is not a terminal answer, and three rungs remain untried. Recorded as distinct from candidate 73 because it names the rungs rather than repeating the block.' \
 --session "$SID"

python3 $D add-gap --category SW --priority P2 \
 --description 'relate-extraction HAS NO --verbatim-exempt AND add-extraction DOES, SO A CONDITION READ FROM A NON-UTF-8 PAYLOAD CANNOT BE GIVEN THE EDGE A BLOCKING CHECK DEMANDS. Measured in batch 13 on REF-00997, a legacy OLE .doc encoded CP1252. add-extraction accepted the rows under --verbatim-exempt, which exists precisely for an artefact the checker cannot decode. relate-extraction then refused the condition_on edge because --quote is required and the quote byte-check reports the same artefact NOT SEARCHED. extraction_relations_integrity (BLOCKING) in turn fails any figure_role=condition that qualifies nothing. The three rules are individually right and jointly make one state unreachable: a proviso extracted from a PDF, a .doc or any non-UTF-8 payload can be written but never correctly related. Batch 13 was not blocked by this -- the precedent-correct role for its row turned out to be finding (REF-00992 ext 26, REF-00994 ext 29) rather than condition -- so this is recorded as a latent trap, not a live one. The next genuine proviso in a PDF hits it. Fix shape: give relate-extraction the same --verbatim-exempt add-extraction already has, ledgered on the edge the way it is ledgered on the row.' \
 --session "$SID"

# ---- 5. retire and re-determine ---------------------------------------------------
python3 $D retire-specification --specification-id 5 \
 --reason 'New evidence arrived for parameter 3. REF-00997 adds a governing claim (1:14 <=, rise >190mm), a condition (1:8 <=, rise <190mm) and a finding (the prescriber must assess whether THIS client can propel the recommended gradient). A determination is computed from the evidence set that existed when it ran; this one predates all three rows. Retired so the cell can be re-determined, not because its value was found wrong.' \
 --session "$SID"
echo "REPLAY COMPLETE"
