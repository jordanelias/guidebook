#!/usr/bin/env python3
"""Batch 20 -- second fix-forward: the independent antagonist pass's SUSTAINED findings and the
owner's rulings of 2026-09-25 on the four withheld findings. Writes to the SCRATCH db only.

Run from the worktree root, after migration 096 (disposition EXHAUSTED) has been applied to the
canonical DB and the canonical DB copied to scratch. Every write goes through db.py; new gap ids
are read from db.py's own output, never computed here. Every quotation below was checked against
the persisted artefact (normalised grep of 639e73bd17c02f7f.txt, 18ef7d575e63330c.xml) or read off
an attested render (db21e48738335d82.p0036/p0052/p0223/p0224/p0246, 5dd866a236fb5978.p0056)
before this script was run.
"""
import json, os, subprocess, sys

SCRATCH = "/tmp/claude-0/-home-user-guidebook/34e8c762-53ff-5f39-b746-3f5298058fcb/scratchpad/b20c.db"
S = "session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa"
ENV = dict(os.environ, GUIDEBOOK_DB_PATH=SCRATCH)
PDF18 = "retrieval-log/session_2026-09-18-research-batch-18-archive-route-ramp-threshold/5dd866a236fb5978.pdf"
PDF20 = f"retrieval-log/{S}/db21e48738335d82.pdf"
RULING = "Owner ruling 2026-09-25, recorded on contact (CLAUDE.md rule 0):"
DRY = "--dry-run" in sys.argv


def db(*args):
    cmd = ["python3", "scripts/db.py", *args, "--session", S] + (["--dry-run"] if DRY else [])
    r = subprocess.run(cmd, capture_output=True, text=True, env=ENV)
    out = r.stdout.strip()
    if r.returncode != 0:
        print("FAILED:", args[:4], "\n", r.stderr[-2000:], out[-800:])
        sys.exit(1)
    try:
        return json.loads(out[out.index("{"):])
    except ValueError:
        return {"raw": out[-300:]}


def step(label, out):
    print(f"{label}: {json.dumps(out)[:170]}")


SOFT = ("ALSO CORRECTED: the batch-20 status note on this row says rows 63 and 64 keep 'verified' because "
        "their claim_text 'verifies byte-for-byte' against a persisted artefact. It verifies under "
        "retrieval_log's NORMALISED match (letters and digits only), not byte-for-byte: the DjVu text "
        "doubles every space, and at extraction 64 reads 'recommended— for self- propelled'.")

# ---- 1. gaps first, so later notes can name them -----------------------------------------
g_slug = db("add-gap", "--category", "SW", "--priority", "P3", "--skill", "governance",
            "--description",
            "resolve-candidate COULD NOT WRITE suggested_slug, so a REHOME disposition could not say where "
            "the candidate belongs. Found by an independent adversarial pass on batch 20: candidate 117 was "
            "re-described as rehomed to stair-ramp-threshold-biomechanics-accessibility while its typed "
            "suggested_slug still named accessible-circulation-geometry, the slug it was found under -- the "
            "prose and the only joinable column disagreeing. CLAUDE.md section 4: a column the CLI cannot "
            "reach is a coverage bug, not a licence for hand SQL. FIXED IN THE SAME BATCH: resolve-candidate "
            "takes --suggested-slug with --disposition REHOME only, validates it against slugs, and records "
            "the replaced value in the notes tail. Derive whether any REHOME row still points back at its "
            "origin: select candidate_id, found_under_slug, suggested_slug from search_candidates where "
            "disposition='REHOME'.").get("gap_id")
step("gap suggested_slug", g_slug)

g_adm = db("add-gap", "--category", "SW", "--priority", "P2", "--skill", "governance",
           "--description",
           "NO VERB COULD ATTACH AN ADMISSION TO AN EXISTING SEARCH. search_admissions is the one carrier of "
           "which search admitted a source, and its only writer was log-search --admitted-ref-id, which "
           "attaches an admission only to a search logged in the same call. A source admitted in a later "
           "batch from a staged candidate therefore could not point back at the search that surfaced it, "
           "although integrity check S01 states that the surfacing search and the admitting search are the "
           "same event (batch 17's candidates 107/108 on exec 77 are the precedent). research_protocol_audit "
           "then reported REF-01007 and REF-01008 as admitted by no search. Batch 20 first read that as the "
           "audit's case (b) and wrote no edge; an independent adversarial pass sustained it as case (a) plus "
           "a writer gap. FIXED IN THE SAME BATCH: db.py link-admission writes the edge ONLY when a "
           "search_candidates row already records both ends (that candidate's exec_id and resolved_ref_id, "
           "disposition ADMITTED) and refuses otherwise, so it restates a recorded fact and cannot attribute "
           "a source to an arbitrary search. Applied to (91, REF-01007) and (90, REF-01008).").get("gap_id")
step("gap admissions", g_adm)

g_rul = db("add-gap", "--category", "SW", "--priority", "P3", "--skill", "governance",
           "--description",
           "TWO OWNER RULINGS OF 2026-09-25 HAD NO WRITER TO APPLY THEM. (1) Re-grading an R13 population "
           "match: add-population-match deliberately allows a SECOND row so that a dissent reads as a "
           "contest, but a ruling is not a dissent, and nothing could move an existing grade. (2) Narrowing a "
           "term's definition: nothing could write `terms` after add-term. Both are coverage bugs under "
           "CLAUDE.md section 4. FIXED IN THE SAME BATCH: amend-population-match (grade checked against the "
           "column's own CHECK; the replaced grade and the reason appended to mismatch_note) and amend-term "
           "(definition or scope_note only -- canonical_en is a vocabulary decision -- with the replaced text "
           "and the reason appended to scope_note, the row's only free-text column).").get("gap_id")
step("gap ruling writers", g_rul)

g_vvi = db("add-gap", "--category", "AUDT", "--priority", "P2", "--skill", "governance",
           "--description",
           "v_value_independence COUNTS ABSENCES AS INDEPENDENT ROOTS. The view counts DISTINCT "
           "COALESCE(root_ref_id, root_id) over rows whose root_type is measurement_primary, "
           "participatory_finding or derived_calculation, and never looks at claim_type. A row with "
           "claim_type 'absent' asserts that its source states NO value, yet it adds a root to the "
           "parameter's independent-root count exactly as a measured value does. Batch 20 made it worse: "
           "REF-01007 (extraction 59, absent-confirmed) is a new root that measures nothing on the "
           "parameter. Raised by an independent adversarial pass (finding #9) and WITHHELD from repair in "
           "batch 20 pending an owner decision on how independence should be counted; the view is NOT "
           "redefined here. Derive the absence-only roots rather than trusting any list: select "
           "coalesce(root_ref_id, root_id) root, count(*) n from source_value_extractions where "
           "parameter_id=3 and root_type in ('measurement_primary','participatory_finding',"
           "'derived_calculation') group by root having sum(claim_type <> 'absent') = 0. Compare "
           "select * from v_value_independence where parameter_id=3.").get("gap_id")
step("gap independence view", g_vvi)

g_r1 = db("add-gap", "--category", "RP", "--priority", "P2", "--skill", "multilingual-research",
          "--description",
          "BATCH 20's R1 (Co-1 / T2) LEG WAS A THIN DISCHARGE OF R1, NOT A FULL ONE. It ran three queries "
          "(exec 92-94): English only, one biomedical full-text index (Europe PMC), no DPO or "
          "disability-organisation channel, no non-English vocabulary, no grey-literature route. "
          "research_batch_dod R1 passes when Co-1-targeted searches exist, which is why the gate was green; "
          "an independent adversarial pass (finding #20) sustained that the leg did not do what R1 exists "
          "for -- 'Co-1 / T2 / Co-2 pass FIRST', co-primary with T1 under CRPD 4.3. FOR A FUTURE BATCH, not "
          "a repair: a Co-1 pass on ramp gradient that reaches DPO and user-led outputs in more than one "
          "language and more than one kind of index. Candidate 126 (Mactaggart 2024, a participatory "
          "audit staged by this leg) is the strongest lead it produced.").get("gap_id")
step("gap R1", g_r1)
if not DRY:
    for g in (g_slug, g_adm, g_rul):
        step(f"close {g}", db("close-gap", "--gap-id", g, "--status", "CLOSED-FIXED"))

# ---- 2. #5 candidate 117's typed slug -------------------------------------------------------
step("117", db("resolve-candidate", "--candidate-id", "117", "--disposition", "REHOME",
               "--suggested-slug", "stair-ramp-threshold-biomechanics-accessibility",
               "--redescription",
               f"TYPED COLUMN BROUGHT INTO LINE WITH THE REHOMING. The re-description above rehomed this row to "
               f"stair-ramp-threshold-biomechanics-accessibility while suggested_slug still named "
               f"accessible-circulation-geometry, where it was found -- prose and column disagreeing, found by "
               f"an independent adversarial pass (finding #5). resolve-candidate could not write "
               f"suggested_slug; the flag was added in batch 20 ({g_slug}) and is used here. The same pass "
               f"confirmed the content call: 'gradient' in this report is always an orientation gradient, "
               f"and there is no ramp recommendation."))

# ---- 3. #6 admission edges ------------------------------------------------------------------
for ex, ref, cand in ((91, "REF-01007", 124), (90, "REF-01008", 125)):
    step(f"link {ex}->{ref}", db("link-admission", "--exec-id", str(ex), "--ref-id", ref, "--reason",
         f"Candidate {cand} was surfaced by this search and admitted as {ref} in batch 20 by retrieving its "
         f"locator. No verb could attach an admission to an already-logged search, so the edge was missing "
         f"and research_protocol_audit reported {ref} as admitted by no search. Written with link-admission "
         f"({g_adm}), which refuses unless the candidate row records both ends, as S01 requires."))

# ---- 4. owner ruling: REF-01007 population grade ---------------------------------------------
step("REF-01007 match", db("amend-population-match", "--match-id", "session_2026-09-25-resea-REF-01007-MOB",
     "--match-grade", "PARTIAL", "--reason",
     f"{RULING} re-grade to PARTIAL, matching REF-01006's precedent; whether an audit's participants were "
     f"disabled is a Co-1 question, not a criterion of population-match directness. The PROXY warrant above "
     f"therefore does not stand, and it had two faults of its own that an independent adversarial pass raised "
     f"(finding #10). (1) 'PROXY BY R13's OWN LETTER: no participants' -- R13's letter in DR-2026-08-19 "
     f"names children-for-adults, chamber tests and general-population as PROXY at best, and 'no "
     f"participants' is not in it. The harness research contract's one-line summary of R13 "
     f"(governance/research-contract.yaml) DOES read 'Children/general-population/no-participants = PROXY', "
     f"and that line is what the PROXY grade followed; as applied to a facility audit it is superseded by "
     f"this ruling on contact (rule 0). Whether the contract's wording should change is the owner's call and "
     f"was not edited. (2) 'nobody disabled took part in this measurement in any role' is an unsupported "
     f"negative: the paper does not say whether any of the auditors from 45 universities was disabled. "
     f"What PARTIAL records here is what it records for REF-01006: the population "
     f"served is MOB and the measurement is one step removed -- facilities checked for the PRESENCE of a "
     f"ramp, not people negotiating ramps. REF-01006's PARTIAL is the precedent applied, not reopened. "
     f"Applied with amend-population-match ({g_rul})."))

# ---- 5. owner ruling: TERM-089 narrowed ---------------------------------------------------------
step("TERM-089", db("amend-term", "--term-id", "TERM-089", "--field", "definition", "--replacement",
     "An inclined walking or wheeling surface, built as a discrete element, that bridges a level difference "
     "on a route. Excludes the running slope of paths, walkways and trails.",
     "--reason",
     f"{RULING} narrowed to exclude path and trail slopes, so that this term stops pre-deciding GAP-033's "
     f"open ramp-versus-route question (group 1), which stays open there. The ruling covers TERM-089 only; "
     f"the three further points an independent pass raised on batch 20's minted terms are recorded as open "
     f"on GAP-033, not settled by this. Applied with amend-term ({g_rul})."))

step("GAP-033", db("amend-gap", "--gap-id", "GAP-033", "--append-note",
     "OWNER RULING 2026-09-25, AND WHAT IT DID NOT SETTLE. TERM-089 ('ramp') is narrowed to exclude the "
     "running slope of paths, walkways and trails, so it no longer pre-decides group (1), the "
     "ramp-versus-route question, which stays OPEN here. THREE FURTHER POINTS that an independent adversarial "
     "pass raised on batch 20's minted terms (finding #14) are NOT resolved by that ruling and are open on this "
     "gap: (a) TERM-094 ('accessibility audit') has a scope note that states as a universal -- 'An audit "
     "measures COMPLIANCE with a yardstick, never what the yardstick should be' -- what is one testable prior "
     "(batch 20's P1b) drawn from two sources; (b) TERM-093 ('ramp usability') is defined as 'the outcome a "
     "ramp gradient is judged against' and its scope note adjudicates the measures to it as "
     "operationalisations, which forecloses a separate term for the acceptability CRITERION as distinct from "
     "the measure; (c) TERM-092's scope note says 'It bounds TERM ramp run length from above' -- a dangling "
     "reference with no term id. Each is a vocabulary decision for the owner, not a wording fix, and none was "
     "edited."))

# ---- 6. owner ruling: EXHAUSTED disposition --------------------------------------------------
for cid in (109, 110):
    step(f"cand {cid}", db("resolve-candidate", "--candidate-id", str(cid), "--disposition", "EXHAUSTED",
         "--redescription",
         f"DISPOSITION MOVED TO EXHAUSTED. {RULING} a real, CHECK-permitted value for 'exhausted, given up "
         f"for now' was added (schema migration 096) and applies to this row, to which no route exists from "
         f"anywhere. The routes tried and the reasons are in the re-description above; this changes the typed "
         f"column so that no sweep reads PENDING-VERIFICATION as work. Not queued for anyone."))
step("cand 123", db("resolve-candidate", "--candidate-id", "123", "--disposition", "PENDING-VERIFICATION",
     "--redescription",
     "STAYS PENDING-VERIFICATION, DELIBERATELY, NOW THAT EXHAUSTED EXISTS (migration 096, owner ruling "
     "2026-09-25). EXHAUSTED is for an item to which no route exists from anywhere. This one has a route: "
     "PubMed Central serves it free to read (Unpaywall and OpenAlex both give is_oa true, green, via PMC), "
     "and what stopped batch 20 -- a reCAPTCHA interstitial and Cloudflare 403s -- is a barrier to this "
     "environment's automated requests, which may be transient. The owner's ruling drew exactly this "
     "distinction. Not queued for anyone, and no request is drafted."))

# ---- 7. candidate 125 page count, candidate 126 warrant ---------------------------------------
step("cand 125", db("resolve-candidate", "--candidate-id", "125", "--disposition", "ADMITTED",
     "--admitted-ref-id", "REF-01008", "--redescription",
     "CORRECTION, SAME BATCH (independent adversarial pass, finding #21): '334 images' above is Internet "
     "Archive's imagecount metadata. The persisted PDF (db21e48738335d82.pdf) has 332 pages, and every page "
     "index batch 20 cites is a zero-based index into that PDF. ALSO: the untested Table 20 cells are the "
     "report's recommendations, not measurements -- 'interpolate' above is batch 20's inference, not the "
     "source's word (see extractions 61 and 62)."))
step("cand 126", db("resolve-candidate", "--candidate-id", "126", "--disposition", "PENDING-VERIFICATION",
     "--redescription",
     "CORRECTION TO THIS ROW'S WARRANT DESCRIPTION (independent adversarial pass, finding #13). It says the "
     "audits were co-facilitated by youth researchers with disabilities, as though that settled the Co-1 "
     "question for this cell. The persisted text: the eight youth researchers who adapted the tool were "
     "'themselves all Ugandan healthcare users with disabilities'; 'Six of the eight youth researchers were "
     "selected to participate in the pilot as trainee facilitators'; 'Each pair of trainee facilitators "
     "included one youth researcher with a disability and one peer without a disability. One trainee was "
     "Deaf, one lived with albinism, and one had visual impairment.' NO MOBILITY IMPAIRMENT IS RECORDED among "
     "the facilitators. For staging against parameter 3 x MOB that matters: whatever Co-1 warrant the "
     "co-production carries under D-0178, it is not co-production by the population this parameter serves."))

# ---- 8. extraction corrections ----------------------------------------------------------------
QUAL = ("THE 'MORE PERMISSIVE' CLAIM ABOVE, QUALIFIED (independent adversarial pass, finding #1). (a) It holds "
        "only against REF-01008's own data: ramp 6's manual-wheelchair ascent result, and Table 20, which stops "
        "1:10 at a 6-in curb. REF-01008 is dated May 1980, after REF-01005, whose 'Templer, 1977' is "
        "unidentified. Against footnote c's OTHER warrant -- Walter as REF-01008 reports him, 1:9 over 10 ft "
        "self-propelled (extraction 64) -- Table 13's 1:10 band over an 8-ft run is STRICTER, not more "
        "permissive. (b) The test was applied to one footnote-c row only. REF-01008's Conclusions (printed p.33, "
        "index 52, rendered): 'Ramps 6 and 9 were found to be unacceptable to one group, either for ascent or "
        "for descent, respectively'. Table 19 row g marks ramp 9 -- the geometry of Table 13's OTHER footnote-c "
        "row (1:8, 2 ft, 3 in) -- not acceptable in descent to people with walking difficulties. So both "
        "footnote-c geometries correspond to a Templer ramp that one group found unacceptable, and batch 20 "
        "reported only this one. Commit c3cca9b1's message states the unqualified form and cannot be "
        "rewritten; this is its correction.")

step("ext 59", db("amend-extraction", "--extraction-id", "59", "--field", "extraction_status", "--value",
     "absent-confirmed", "--reason",
     "Commit c3cca9b1's message repeats the claim this row's A1 correction withdrew -- that the paper 'says "
     "why (slope measurement is what keeps audits small)'. A commit message cannot be rewritten, so the "
     "correction above stands for it too (independent adversarial pass, finding #17). And R13 for this "
     "source is now PARTIAL by owner ruling 2026-09-25, not the PROXY the same message states."))
step("ext 66", db("amend-extraction", "--extraction-id", "66", "--field", "extraction_status", "--value",
                  "reviewed", "--reason", QUAL + " " + SOFT))
step("ext 60", db("amend-extraction", "--extraction-id", "60", "--field", "extraction_status", "--value",
     "reviewed", "--reason",
     "THE NOTES ABOVE GIVE ONLY RAMP 9's FAVOURABLE FIGURE (independent adversarial pass, finding #4). "
     "REF-01008's Conclusions (printed p.33, index 52, rendered): 'Ramps 6 and 9 were found to be unacceptable "
     "to one group, either for ascent or for descent, respectively'. Table 19 row g marks ramp 9 (1:8, 2 ft, "
     "3 in) not acceptable in DESCENT to people with walking difficulties, and ramp 11 -- the same geometry "
     "with a half-inch lip -- not acceptable in either direction for that group. MOB includes people who walk "
     "with difficulty. The 95 percent in the notes above is the manual-wheelchair ASCENT figure only; Table 20 "
     "recommends 1:8 up to a 3-in curb over that group's result. " + SOFT))
for eid, cell, line in (("61", "no 1:10 ramp over a 6-in curb",
                         "between 1:10.67 and 1:12 in the 6-in row"),
                        ("62", "no 1:12 ramp over a 9-in curb",
                         "between 1:12 and 1:13.3 in the 9-in row")):
    step(f"ext {eid}", db("amend-extraction", "--extraction-id", eid, "--field", "root_type", "--value",
         "committee_assertion", "--reason",
         f"RETYPED measurement_primary -> committee_assertion (independent adversarial pass, finding #2). The "
         f"notes above say this cell was NOT TESTED ({cell} exists in Table 1), so the typed root claimed a "
         f"measurement the prose denies -- the typed-versus-prose contradiction batch 19 corrected on "
         f"extraction 57. The value is the report's recommendation for a combination it did not test: an "
         f"assertion by its authors, self-rooted in REF-01008. committee_assertion is the live vocabulary's "
         f"value for a source that asserts rather than measures; derived_calculation would claim a computed "
         f"value with derived_from edges, and none exists. It also stops the row counting as an independent "
         f"measured root. 'INTERPOLATION' IN THE NOTES ABOVE IS BATCH 20's WORD, NOT THE SOURCE's: the report "
         f"never says how its untested cells were set, only 'Based on these findings, Table 20 shows "
         f"recommendations for maximum acceptable gradients for three different curb heights.' Read it as an "
         f"inference. AND THE CELL SITS ON THE WRONG SIDE OF THE REPORT's OWN LINE: Table 3's heavy line "
         f"('Only ramps to the right of the heavy line are considered acceptable') runs {line} (render "
         f"db21e48738335d82.p0036.png), so this recommendation lies on the unacceptable side of the report's "
         f"own manual-wheelchair-ascent boundary. " + SOFT))
step("ext 65", db("amend-extraction", "--extraction-id", "65", "--field", "extraction_status", "--value",
     "reviewed", "--reason",
     "QUALIFIED (independent adversarial pass, finding #8): the notes above say REF-01002 (20 ft bound), "
     "REF-01003 (short distances) and this report all state the rise- and length-conditioning. REF-01002 is "
     "held on an abstract only, and whether its 20-ft figure is a tested bound is GAP-016's open question; "
     "REF-01003 measures path slopes, not ramps, and its bearing waits on GAP-033's ramp-versus-route "
     "question. What stands on ramps is this report's own conclusion (extraction 63). " + SOFT))
step("ext 63", db("amend-extraction", "--extraction-id", "63", "--field", "extraction_status", "--value",
     "verified", "--reason",
     "WITHDRAWN (independent adversarial pass, finding #8): 'the fourth independent statement of "
     "length-conditioning on parameter 3 in this corpus'. The count was typed by hand and took two sources "
     "as support whose bearing open records call unknown. Listed honestly instead of counted: MEASURED on "
     "ramps -- REF-01008 alone, curb ramps with rises of 3-9 in (this row, 65, 66); STATED as a mechanism -- "
     "REF-00996 (T5 framework, no measurement; extraction 32); REF-01002 (7 percent up to 20 ft; extractions "
     "44-45) -- held on an abstract only, and whether 20 ft is a tested bound is GAP-016's open question; "
     "REF-01003 (extraction 49) -- path slopes, not ramps, waiting on GAP-033's ramp-versus-route question. "
     "Derive the parameter-3 rows rather than trusting this list: select extraction_id, ref_id, claim_type, "
     "root_type, substr(setting,1,60) from source_value_extractions where parameter_id=3 order by ref_id. "
     "ALSO: this row's claim_text verifies under retrieval_log's normalised match (letters and digits), not "
     "byte-for-byte -- the DjVu text doubles every space."))
step("ext 64", db("amend-extraction", "--extraction-id", "64", "--field", "extraction_status", "--value",
     "verified", "--reason",
     "Verifies under retrieval_log's normalised match (letters and digits), not byte-for-byte: the DjVu text "
     "reads 'recommended— for self- propelled'. AND A CAVEAT ON 'A SECOND INDEPENDENT READER' (independent "
     "adversarial pass, finding #12): REF-01008 and REF-01005 are not fully independent readers of Walter. "
     "REF-01008 (printed p.4) mentions 'a more extensive study currently underway at Syracuse University' -- "
     "most likely REF-01005's project -- and REF-01005's footnote c cites Templer. Walter stays counted once, "
     "and only as reported, which is the safeguard that matters."))

# ---- 9. #11 the footnote's own words, as a second row beside extraction 56 --------------------
step("ext REF-01005 footnote", db("add-extraction", "--ref-id", "REF-01005", "--slug",
     "accessible-circulation-geometry", "--parameter-id", "3", "--identity", "MOB",
     "--claim-type", "qualitative", "--claimed-value", "warrant scoped to the 1:8 and 1:10 bands only",
     "--figure-role", "claim",
     "--claim-text", "Based on research of others (Templer, 1977 and Walters, 1971).",
     "--verbatim-exempt",
     "RENDER-READ; TEXT LAYER UNDECODABLE. retrieval_log cannot decode the scanned ED184280 PDF "
     "(5dd866a236fb5978.pdf), whose pypdf text at zero-based index 56 reads 'cBased on research of others "
     "(Templer, 1977 and-WaJter$, 1971).'. This claim_text is transcribed letter for letter from the batch-20 "
     "render 5dd866a236fb5978.p0056.png (200 dpi, manifest-attested), and keeps the page's 'Walters'.",
     "--source-section", "Table 13: Maximum Lengths and Slopes for Rampways -- footnote c",
     "--jurisdiction", "US", "--extraction-method", "re-read", "--extraction-status", "reviewed",
     "--root-type", "committee_assertion", "--root-ref-id", "REF-01005",
     "--file-anchor", PDF18, "--locator-scheme", "page", "--loc-section", "57",
     "--loc-note", "one-based PDF page 57 = zero-based index 56 (the convention extraction 56 uses; the "
                   "printed folio is damaged on the scan); rendered in batch 20 as 5dd866a236fb5978.p0056.png",
     "--relation", "none",
     "--notes",
     "WRITTEN AS A SECOND ROW BESIDE EXTRACTION 56, NOT AN EDIT OF IT (D-0168; independent adversarial pass, "
     "finding #11). Extraction 56's claim_text normalises the page's 'Walters' to 'Walter' -- a transcription "
     "that corrects its source and so cannot be audited against it. This row carries the page's own words. "
     "THE WALTER IDENTITY IS A HYPOTHESIS, STATED HERE AND NOT IN THE QUOTE: 'Walters, 1971' is read as Felix "
     "Walter's 1971 Disabled Living Foundation study (candidate 109, now EXHAUSTED) because REF-01005's "
     "bibliography lists Walter, 1971 and its page 163 speaks of 'Walter findings for ramps' (extraction 54); "
     "nothing on this page says so. The only 'Walters' in REF-01008's text is a research assistant in its "
     "credits, not a cited work. SCOPE, from the render: the superscript c sits on the 1:8 row (2 ft run, 3 in "
     "rise) and the 1:10 row (8 ft run, 9 in rise) only."))

# ---- 10. #20 REF-01008's Part II field tests --------------------------------------------------
step("ext CM8", db("add-extraction", "--ref-id", "REF-01008", "--slug", "accessible-circulation-geometry",
     "--parameter-id", "3", "--identity", "MOB", "--claim-type", "qualitative",
     "--claimed-value", "no difficulty with the slope, in either direction", "--figure-role", "finding",
     "--claim-text", "Eleven test subjects used the ramp to enter and leave the street. None appeared to have "
                     "difficulty with the slope of the ramp, in either direction.",
     "--source-section", "Part II, Countermeasure No. 8 (Single Conventional Ramp) -- Evaluation Results; "
                         "Wheelchair Group",
     "--jurisdiction", "US",
     "--setting", "field-built single conventional curb ramp, slope approximately 1 in 12 (8.33 percent), "
                  "with a lip of about 1/4 in at the street; Sioux City, Iowa; wheelchair users in the "
                  "special-group evaluation",
     "--extraction-method", "full-read", "--extraction-status", "verified",
     "--root-type", "measurement_primary", "--root-ref-id", "REF-01008",
     "--measurement-paradigm", "field_observation",
     "--root-population-note", "Eleven wheelchair users; chair types not stated.",
     "--file-anchor", PDF20, "--locator-scheme", "page", "--loc-section", "205",
     "--loc-note", "printed pp.204-205 = zero-based indices 223-224, both rendered (db21e48738335d82.p0223.png, "
                   ".p0224.png); the slope is stated on p.204 and the quoted sentences are on p.205",
     "--relation", "none",
     "--notes",
     "FIELD DATA THE BATCH-20 ADMISSION LEFT OUT (independent adversarial pass, finding #20). REF-01008 is not "
     "only a laboratory study: Part II built countermeasures in real cities and had special groups use them. "
     "At a single conventional curb ramp in Sioux City with 'a slope of approximately 1 in 12 (8.33 percent)', "
     "eleven wheelchair users used it in both directions and 'None appeared to have difficulty with the slope "
     "of the ramp'. WHAT LIMITS IT: the judgment is an observer's ('appeared'); the curb height and run are not "
     "given in this passage; the chair types are not given. WHAT ELSE THE SAME TEST FOUND: a construction lip "
     "of about a quarter inch 'caused difficulty to three of the 11 subjects'; one subject chose not to use the "
     "ramp at all; on 14 of 20 entries into the street the wheelchair users' path took them beyond the limits "
     "of the crosswalk, which the report attributes to the speed gained descending the ramp. Summary finding 2: "
     "'All of the wheelchair users were able to use the ramp'. A short field ramp at about 1:12 is consistent "
     "with the laboratory finding that steeper ramps are acceptable if short (extraction 63); it says nothing "
     "about longer runs. Owner ruling 2026-09-18: pre-1990 work is historical grounding, not a current anchor."))
step("ext CM9", db("add-extraction", "--ref-id", "REF-01008", "--slug", "accessible-circulation-geometry",
     "--parameter-id", "3", "--identity", "MOB", "--claim-type", "qualitative",
     "--claimed-value", "the slopes gave no difficulty; the surface did", "--figure-role", "finding",
     "--claim-text", "The ramp slopes themselves appeared to give no difficulty to the wheelchair users.",
     "--source-section", "Part II, Countermeasure No. 9 (Double Conventional Ramp) -- Evaluation Results; "
                         "Wheelchair Group; Table 124",
     "--jurisdiction", "US",
     "--setting", "field-built double conventional curb ramps 'sloped, at a 1:12 ratio (8.33 percent)', "
                  "exposed pebble-aggregate surface; Baltimore, Maryland, beside a community and recreation "
                  "center for the elderly",
     "--extraction-method", "full-read", "--extraction-status", "verified",
     "--root-type", "measurement_primary", "--root-ref-id", "REF-01008",
     "--measurement-paradigm", "field_observation",
     "--root-population-note", "Thirteen wheelchair users (the columns of Table 124); at least one used a "
                               "motorized chair.",
     "--file-anchor", PDF20, "--locator-scheme", "page", "--loc-section", "227",
     "--loc-note", "printed p.227 = zero-based index 246, rendered (db21e48738335d82.p0246.png); the 1:12 "
                   "slope is stated on printed p.225 (index 244, text layer only)",
     "--relation", "none",
     "--notes",
     "FIELD DATA, SECOND SITE (independent adversarial pass, finding #20). Table 124 gives each of thirteen "
     "wheelchair users' difficulty factor entering and leaving the street by each ramp; the four means are "
     "2.08 to 2.84, on the four-point scale the report defines for its wheelchair evaluations (1 'equivalent "
     "to maneuvering a level surface with no perceptible change in speed', 4 'could negotiate only with the "
     "greatest difficulty, if at all'). The report attributes the difficulty to the SURFACE, not the slope: "
     "'the pebble textured surface did cause substantial problems, because of its roughness and because of "
     "some loose material on the ramp surface'; three narratives describe chairs jamming on it, one user "
     "needing assistance to complete the ascent. Summary finding 15: 'The wheelchair users had no difficulty "
     "in using the ramps except for the surface finish.' WHAT LIMITS IT: observer-judged; curb height and run "
     "not given in this passage; the slope-versus-surface attribution is the authors'. Owner ruling "
     "2026-09-18: pre-1990 work is historical grounding, not a current anchor."))

# ---- 11. GAP-037: #1, #2, #3, #7, #8, #12 -------------------------------------------------------
step("GAP-037", db("amend-gap", "--gap-id", "GAP-037", "--append-note",
     "SECOND BATCH-20 CORRECTION: AN INDEPENDENT ADVERSARIAL PASS SUSTAINED FIVE FAULTS IN THE BATCH-20 NOTE "
     "ABOVE. (A) CLAUSE (2) CORRECTED A TRUE STATEMENT INTO A FALSE ONE. Batch 19's independent adversarial "
     "subagent DID render index 56 -- a full page and two crops, in its scratchpad -- and read them "
     "(transcripts/harness_ca1ae452/subagents/2026-09-20T03-41-13_other_aaddd48c.jsonl, on main). Batch 20 "
     "checked with ls retrieval-log/*/5dd866a236fb5978.p*, which lists only PERSISTED renders and could not "
     "see a scratchpad file. Correct form: no render was PERSISTED before batch 20; the 2026-09-20 statement "
     "that the reading was confirmed on a rendered page image was true. (B) CLAUSE (3) OVERSTATES. Footnote c "
     "does not MARK the 1:12 or 1:16 rows, as the render shows, but REF-01005 separately cites Walter as "
     "corroboration for 1:16 over 20 ft on its page 163 (extraction 54: 'Walter findings for ramps are similar "
     "to ours') -- this gap's own clause (5). Footnote c is not a warrant for 1:12; Walter is a corroborating "
     "node for 1:16. (C) CLAUSE (4)'s 'MORE PERMISSIVE' HOLDS ONLY AGAINST REF-01008's OWN DATA -- ramp 6's "
     "manual-wheelchair ascent result and Table 20, which stops 1:10 at a 6-in curb -- and REF-01008 is dated "
     "May 1980, after REF-01005. Against footnote c's other warrant, Walter as REF-01008 reports him (1:9 over "
     "10 ft; extraction 64), Table 13's 1:10 band over 8 ft is STRICTER. And the test was applied to one "
     "footnote-c row only: REF-01008's Conclusions say 'Ramps 6 and 9 were found to be unacceptable to one "
     "group, either for ascent or for descent, respectively', and Table 19 row g marks ramp 9 -- the geometry "
     "of Table 13's 1:8 row -- not acceptable in descent to people with walking difficulties (extractions 60, "
     "66). (D) CLAUSE (6) RESTS ON AN UNTESTED CELL AND A HAND COUNT. Table 20's 1:12-to-a-9-in-curb "
     "(extraction 62), like its 1:10-to-a-6-in-curb (61), was never tested, and both lie on the unacceptable "
     "side of the report's own Table 3 heavy line for manual-wheelchair ascent; both rows are now root_type "
     "committee_assertion, and 'interpolation' was batch 20's word, not the source's. The length-conditioning "
     "clause (6) leans on was called 'the fourth independent statement' in extraction 63's notes; that count "
     "took REF-01002 (abstract only; GAP-016) and REF-01003 (path slopes; GAP-033) as support. Listed "
     "honestly: MEASURED on ramps by REF-01008 only (curb ramps, rises 3-9 in, extractions 63 and 65-66, and "
     "its Part II field ramps at about 1:12); STATED as a mechanism by REF-00996 (T5, no measurement); "
     "REF-01002 and REF-01003 bear on it only once GAP-016 and GAP-033 are answered. (E) CLAUSE (7)'s 'second, "
     "independent account' of Walter is not fully independent: REF-01008 mentions a study underway at "
     "Syracuse University, most likely REF-01005's, and REF-01005 cites Templer. Walter stays counted once and "
     "only as reported. ALSO: candidate 117's typed suggested_slug now names the stairs slug (it still named "
     "this gap's slug when clause (5) said 'rehomed'), and a second REF-01005 row now carries footnote c "
     "verbatim, 'Walters' included, beside extraction 56. Commit c3cca9b1's message repeats clauses (2) and "
     "(4) unqualified; it cannot be rewritten, and this is its correction."))

print("DONE", "(dry run)" if DRY else "")
