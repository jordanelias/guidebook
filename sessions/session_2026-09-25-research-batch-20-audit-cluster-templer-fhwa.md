# Batch 20 — the audit cluster, Templer's short-ramp study, footnote c, and the backlog nobody ran

**Session id:** `session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa`
**Branch:** `claude/batch-20-audit-cluster-templer-fhwa` (from origin/main @ cf35d441)
**Cell:** parameter 3 (TERM-001 `ramp gradient`) × MOB — **still undetermined, gate 1 still unresolved.**
**Assignment:** the batch-20 runbook drafted 2026-09-25 by a read-only investigation, executed
against live state. Where live state and the runbook disagreed, live state won; §9 lists every case.

**Priors:** `scratchpad/<session>/priors.md` (commit be427f35, before any query) and
`query-priors.md` (aa3207de; the Q1b addendum 26ae1dc1, written after Q1/Q2 and before Q1b).

**Derive every figure.** Where a number appears for legibility the command that regenerates it is
beside it; re-run it rather than trust the sentence.

---

## 0. What an adversarial pass over this batch found, and what it did not

**First, a self-administered pass; the independent one followed and is §0b.** `/adversarial`
requires launching the `antagonist` agent (read-only, a different model) so that one model does not
check its own work. This batch ran as a subagent with no agent-launching tool, so it could not start
one. **What ran first was a self-administered pass in the antagonist's shape** — every claim
attacked against its artefact, every count recomputed — and that is exactly the failure mode the pair
exists to prevent. It found seven defects in my own writing (below) and repaired six by a
fix-forward migration (`data_20260925050758_…`). The coordinating session then dispatched the
independent antagonist over PR #159; what it found, and what the owner ruled on the four points it
could not settle, is §0b. **The self-pass missed every one of the independent pass's findings**,
which is the argument for the pair made by measurement.

| # | Artefact | What was wrong | Disposition |
|---|---|---|---|
| A1 | extraction 59 notes | Said REF-01007 "says why" its instrument omits gradient. It says why large audits are rare *in general*; it analyses a Ministry census it did not design. | Corrected (amend-extraction reason) |
| A2 | candidate 124 re-description | Same over-read ("the authors give the reason"). | Corrected (appended) |
| A3 | candidate 117 re-description | Read "February 1976 / Issued November 1978" as "written two years before it was issued". The page does not say what the earlier date marks. | Corrected (appended) |
| A4 | candidate 129 locator | Called Martins 2016 "open access". Europe PMC marks it not-OA; SciELO serves it free. | Corrected (appended) |
| A5 | exec 95 `prior_expectation` | Claimed batch 19's title-screen warning was "carried into priors.md P1". P1 never mentions it. | Corrected (amend-search) |
| A6 | GAP-033 batch-20 note | Its five groups of deferrals account for all but one (observation 54). | Corrected (amend-gap) |
| A7 | commit c3cca9b1 message | Says Garg's body was sought by "nine routes". Exec 96 records ten requests, and **only six could have returned the body** (Europe PMC fullTextXML, NCBI efetch, PMC HTML, PMC `/pdf/`, the Europe PMC render, ScienceDirect); **four were metadata lookups** (Crossref, Europe PMC core, Unpaywall, OpenAlex). This row first said "nine requests plus an Unpaywall lookup", the same body-versus-metadata conflation GAP-026's 2026-09-18 correction had already named; corrected after the independent pass (§0b, #17). | Not repairable (no history rewrite); recorded here |

**Also caught before emission, by refusals in `db.py` rather than by me:** the first Templer
extraction script tried to attach `1:12` to the prose sentence "Ramps #1, 4, 5, 9, 10, 11, 12 and 13
are acceptable" — and the digit check *passed it*, because ramp numbers 1 and 12 supply the digits of
`1:12`. The value was being attached to a sentence that never states a gradient. Rewritten to quote
the rendered Table 3 cell, with a verbatim-exempt warrant. **The digit check can be satisfied by
coincidence; that is a weakness in the instrument, noted rather than fixed here.** Separately, the
writer refused `claimed_value 1:8/1:10/1:12` against the Table 20 lead-in sentence (correctly — it
states no value), and refused `--stated named` for a label that was not a substring of its quote.

**A disclosure:** one Unpaywall request (exec 96) carried an email address in its URL — the same one
the project's earlier Unpaywall calls in committed manifests carry
(`grep -c api.unpaywall.org retrieval-log/*/manifest.jsonl`), which is the owner's own. It should not
have been sent without being asked; no further Unpaywall call was made. **The owner has since ruled
(2026-09-25): no personal email goes to Unpaywall or any similar third-party API, effective at
once**; nothing in the second fix-forward made such a call, and the committed instances stay as
they are (no history rewrite).

## 0b. The independent pass, the owner's rulings, and the second fix-forward

The coordinating session dispatched the `antagonist` over PR #159 at da1d95ab. Its full report is in
`transcripts/harness_34e8c762/subagents/2026-09-25T05-15-51_adversarial_a1efd54a.jsonl`. The
coordinator sustained most findings for repair, sent four to the owner, and asked for a gap on one
more (#9). Everything below is in one data migration (`data_20260925061025_…`) plus one schema
migration (096). Every quotation that went into it was re-checked against the persisted bytes or an
attested render first. The render for #20 is new: `db21e48738335d82.p0223`, `.p0224`, `.p0246`.

| # | What the independent pass found | Repair |
|---|---|---|
| 1 | §5's "more permissive than the study its footnote rests on" holds only against REF-01008's own data. Against footnote c's other warrant, Walter as REF-01008 reports him (1:9 over 10 ft), Table 13's 1:10 band is **stricter**. Ramp 9, the other footnote-c geometry, was unacceptable in descent to people with walking difficulties (Conclusions p.33; Table 19 row g), and I reported only ramp 6. | Qualified in extraction 66, GAP-037 (C) and §5. |
| 2 | Extractions 61 and 62 are untested Table 20 cells, typed `measurement_primary`. "Interpolate" was my word; the source says only "Based on these findings". Both cells also sit on the **unacceptable** side of Table 3's own heavy line. | `root_type` changed to `committee_assertion` (the authors' recommendation; `derived_calculation` would claim a computation with edges, and none exists). §4. |
| 3 | "No render of this page existed before." Batch 19's independent subagent **did** render index 56 in its scratchpad and read it. My `ls retrieval-log/…` could only see *persisted* renders. | "No **persisted** render." GAP-037 (A); §5 and §9. |
| 4 | Extraction 60 gave only ramp 9's favourable ascent figure. | Table 19 row g descent result added. MOB includes people who walk with difficulty. |
| 5 | Candidate 117 is REHOME, but its typed `suggested_slug` still named the origin slug. `resolve-candidate` could not write the column. | `--suggested-slug` added (REHOME only, validated against `slugs`). GAP-045, closed fixed. Set to the stairs slug. |
| 6 | §11's "case (b), no edge" was wrong. S01's own design says the surfacing search and the admitting search are one event (batch 17's exec 77 precedent). No verb could attach an admission to an existing search. | New verb `link-admission`. It refuses unless a candidate row already records both ends. GAP-046, closed fixed. Wrote (91, REF-01007) and (90, REF-01008). |
| 7 | "REF-01005 does not cite Templer or Walter for 1:12 or 1:16." Footnote c does not *mark* those rows, but page 163 cites Walter for 1:16 (extraction 54). | GAP-037 (B); §5. |
| 8 | "Four independent sources" state length-conditioning. That was a hand count, and it included REF-01002 (abstract only) and REF-01003 (path slopes). | Withdrawn and replaced with an honest listing plus a derivation query: extractions 63 and 65, GAP-037 (D), §4. |
| 11 | Extraction 56's `claim_text` normalises the page's "Walters" to "Walter". | Second row, **extraction 67**, carries the words verbatim. The Walters→Walter identity is stated in its notes as a hypothesis. |
| 12 | Templer and Steinfeld are not fully independent readers of Walter. | Caveat on extraction 64, GAP-037 (E), §4. |
| 13 | Candidate 126's co-facilitators with recorded disabilities were Deaf, lived with albinism, or had visual impairment. **None is a mobility impairment.** | Re-description on 126; §2. |
| 17 | A7 miscounted. Commit c3cca9b1's message repeats claims since withdrawn. | A7 fixed; the list of message corrections is below. |
| 18 | P2b was mis-scored: Table 20 endorses 1:12 only to a 9-in curb. That is qualified, so the prior **held**. | §10. |
| 19 | §9 said 123 "is not" open access. Unpaywall and OpenAlex both give `is_oa` true, green. | "Free to read (green OA via PMC), not OA-licensed." §9. |
| 20 | REF-01008's Part II field tests went unmentioned. The R1 Co-1 leg was two English queries in one biomedical index. | **Extractions 68** (Sioux City, about 1:12, 11 wheelchair users) and **69** (Baltimore, 1:12, 13 users; the surface, not the slope, caused the difficulty). **GAP-049** (open) records the thin R1 discharge. |
| 21 | "334 images" is Internet Archive's imagecount; the persisted PDF has 332 pages. Extractions 63 and 64 verify only after normalisation, not "byte-for-byte". A tail of the batch's own subagent transcript was left uncommitted. | Fixed everywhere; transcripts committed. |
| 9 | `v_value_independence` counts absence-only roots as independent (REF-01007 added one). **Withheld for the owner.** | **GAP-048** (open) gives a derivation query. The view is not redefined. |

**Owner rulings of 2026-09-25 on the four withheld findings**, relayed by the coordinating session
and recorded on contact (rule 0):

1. **#10: REF-01007 re-graded PROXY → PARTIAL**, matching REF-01006. Whether an audit's participants
   were disabled is a Co-1 question, not a population-directness criterion. Applied with the new verb
   `amend-population-match`, which records the old grade and the ruling on `mismatch_note`; REF-01006
   was not reopened.
   - The PROXY warrant followed the research contract's one-line R13 summary ("no-participants =
     PROXY", `governance/research-contract.yaml`), which DR-2026-08-19's own R13 text does not contain.
   - The ruling supersedes that line as applied to a facility audit. **Whether the contract's wording
     should change is the owner's call, and it was not edited.**
2. **#14: TERM-089 ('ramp') narrowed** to exclude the running slope of paths, walkways and trails.
   Applied with the new verb `amend-term`. The other three term points (TERM-094's universalised
   prior, TERM-093's foreclosed criterion term, TERM-092's dangling reference) are recorded on
   GAP-033 as **still open**, not settled.
3. **#15: a CHECK-permitted `EXHAUSTED` disposition** was added by schema migration 096, a table
   rebuild generated from the live DDL. It was applied to candidates 109 and 110.
   - **Candidate 123 stays PENDING-VERIFICATION, deliberately.** EXHAUSTED means no route exists from
     anywhere. For 123 a route exists: PMC serves it free to read.
   - What stopped this batch was a bot barrier on this environment's automated requests (reCAPTCHA,
     Cloudflare), which may be transient. The owner's ruling drew exactly that distinction.
   - Not queued for anyone; no request drafted.
4. **#16: no personal email to third-party APIs**; see §0.

The rulings are recorded in `references/project-standards.md`. GAP-047 (closed fixed) records the two
writer gaps they exposed.

**Corrections to commit messages that cannot be rewritten:**
- **c3cca9b1:**
  - "says why (slope measurement is what keeps audits small)" was withdrawn by A1.
  - "R13 PROXY" is now PARTIAL, by ruling.
  - "nine routes" should read ten requests, six of them body-capable (A7).
  - "Candidate 117 rehomed to the stair slug" was prose only until #5 typed it.
  - "rendered for the first time … contrary to GAP-037's 2026-09-20 text" should read first
    *persisted* render; GAP-037's 2026-09-20 text was right (#3).
  - Table 20's "1:10 to 6 in, 1:12 to 9 in" are untested recommendations (#2).
  - "ramp 6 was unacceptable" is true, and ramp 9 was unacceptable in descent to another group (#1).
- **da1d95ab:** "the audit's own case (b) … no edge written" was wrong (#6).

**A defect in my own checking, found while repairing:** `retrieval_log.quote_in_artefacts` returns a
`(found, detail)` tuple, and my pre-write quote checks tested the tuple's truth, which is always
true. They were vacuous. Re-run properly (`found, detail = …`), every verbatim `claim_text` in this
batch is found, and only the declared verbatim-exempt transcriptions are not. db.py's own write-time
check was not affected.

## 1. Pointer repair first — and it exposed nothing (commit caa52ad8)

`sessions/LATEST` and `LATEST-RESEARCH` still named batch 18, so the four checks scoped to
`LATEST-RESEARCH` had been gating batch 18 since batch 19 closed. Re-pointed to batch 19 and re-run
before any batch-20 write: `research_batch_dod --session <batch-19>` COMPLIANT;
`citation_mining_completeness --session <batch-19> --tier-max 2` CLEAN with a non-zero subject;
`research_dod_session` and `author_fidelity` PASS. **Prior P0 held** except that several DoD rules are
vacuous for batch 19 (R11 examined 0 aliases, and says so). `governance/context-map.yaml` was
already stale on untouched main — the scheduled bot's `pipeline_runs` write had moved the DB
fingerprint (CLAUDE.md rule 3). One observation, not acted on: `citation_mining_session`'s
registry note says to re-promote it to blocking "the first time a batch admits a slug-linked Tier
1-2 source"; batch 19 did (REF-01006). Doing it here would make the next PR's gate depend on
whether the next batch admits a T1-2 source, which is a decision for whoever owns that ratchet.

## 2. The Co-1 / T2 leg (R1), run first

Three Europe PMC full-text queries (exec 92–94). Europe PMC's full-text index was the instrument
because batch 19's lesson is that an audit's ramp data sits in its body, not its title.

- **Q1 (Co-1)** returned 2, one of them REF-01006 — the known positive came back, so the narrowness
  is real rather than a malformed AND-chain (R14). P7a not confirmed by Q1.
- **Q1b (Co-1)** returned 21. **Its prior mis-described it**: it claimed to relax one term and
  changed three, so Q1→Q1b isolates nothing. Recorded in the execution. It found
  **Mactaggart et al. 2024** (Uganda). Its audit tool was adapted with eight youth researchers with
  disabilities, and the pilot audits were run by pairs of trainee facilitators, each pair one youth
  researcher with a disability and one peer without. The tool measures ramp slope, and the audits
  report two of three ramps too steep.
  - **The recorded disabilities of those facilitators are Deaf, albinism and visual impairment.
    None is a mobility impairment** (§0b, #13).
  - **Staged, not admitted** (candidate 126): the slope criterion is in a supplementary appendix not
    retrieved, and whether the co-production meets D-0178 must be read, not guessed.
- **Q2 (T2)** returned 8 and **no systematic review**: the two reviews are rapid/scoping (T3). Two
  primary audits staged (127 Campillay-Campillay 2022, Chile; 128 Obrusnikova 2026, US parks).

**No Co-1 or T2 source was admitted.** R1 passes on targeted searches, not on a source.

## 3. The audit cluster

**REF-01007 — Pinto et al. 2021 (candidate 124), admitted T3 clinical/lower_control.** Full JATS
text read. A secondary analysis of Brazil's 2012 census of every public primary-care facility.
**Its ramp item is presence-only** ("Does the health facility have access ramp?"), so it is filed on
parameter 3 as `claim_type absent` (extraction 59). The staged tier guess of 2 was wrong: a census is
not a synthesis. R13 was graded PROXY (no participants in any role); **re-graded PARTIAL by owner
ruling, matching REF-01006** (§0b). Backward pass (exec 95): the slope screens
score 0 and that is the known blind spot; reading the titles surfaced **Martins 2016** (candidate
129 — the only abstract in view reporting a *measured slope* compliance figure, against NBR 9050) and
**Mudrick 2012** (130, 2,389 US facilities). `python3 scripts/research/mining_screen.py --ref REF-01007 --compare`.

**Candidate 123 — Garg 2024 — not admitted.** Batch 19 and the runbook both called it open access
and retrievable. **It is free-to-read at PMC but not OA-licensed**: NCBI withholds the XML ("The
publisher of this article does not allow downloading of the full text in XML form"); PMC's HTML and
PDF sit behind a reCAPTCHA interstitial; Europe PMC's render and ScienceDirect return Cloudflare 403;
Unpaywall and OpenAlex name no other host. Every attempt is in the retrieval log (exec 96). The
abstract does not say whether a ramp gradient is among its 126 checklist "pointers". Left PENDING and
assigned to no one — it is readable in an ordinary browser, which is a different situation from the
three items the owner ruled exhausted.

## 4. Templer, FHWA-RD-79-3 Vol. 3 (candidate 125) → REF-01008, T3 grey

Scan PDF (332 pages; Internet Archive's metadata says 334 images) and DjVuTXT persisted from
Internet Archive. **Every table used was rendered and looked at** (page indices 2, 23, 24, 28, 36, 52,
53, 318; and 223, 224, 246 for the Part II field tests added in §0b).

- **Sole author.** The Technical Report Documentation Page names John A. Templer only; the staged
  "et al." is corrected (R15). May 1980; 325 pages; Georgia Tech Pedestrian Research Laboratory.
- **It is a CURB-RAMP study and its recommendation is rise-conditioned.** Table 20: 1:8 up to a
  3-inch curb, 1:10 up to 6 inches, 1:12 up to 9 inches, steeper than 1:8 never; "Whenever possible
  slopes less than the maximum should be employed" (extractions 60–62).
  - **Two of those cells were not tested:** Table 1 has no 1:10 ramp over 6 in and no 1:12 ramp over
    9 in.
  - The report never says how it set those cells. "Interpolate", which this line first said, was my
    inference, not the source's word.
  - Both cells lie on the **unacceptable** side of the report's own Table 3 heavy line for
    manual-wheelchair ascent, so extractions 61 and 62 are now `committee_assertion` (§0b, #2).
  - Ramp 9, the 1:8 cell's tested ramp, was unacceptable in descent to people with walking
    difficulties (Table 19 row g).
- **1:12 over a 6-inch rise and 6-foot run was acceptable to every manual wheelchair user in ascent**
  (extraction 65), and "steeper ramps are acceptable if they are short" (63). **This does not
  contradict REF-01005**, where almost half could not complete 1:12 over a longer run. The parameter
  is length- and rise-conditioned.
  - This line first said "stated by four independent sources". That was a hand count, and it is
    withdrawn (§0b, #8).
  - Measured on ramps by REF-01008 only; stated as a mechanism by REF-00996. REF-01002 and REF-01003
    bear on it only once GAP-016 and GAP-033 are answered.
- **Part II, the field tests** (added in §0b, #20). Wheelchair users met no difficulty with the slope
  at two field-built 1:12 curb ramps (extractions 68 and 69); the lip and the surface caused the
  trouble.
- **Sample:** 120 volunteers in eight groups, tested August–November 1976. **Table 2's 18 manual
  wheelchair users are young** — its summary row puts all 18 in the 16–35 bands; its subdivision
  rows do not add up to it, but at least 16 of 18 are 16–35 either way. That is the objection
  REF-01005 raised against the 1957 Illinois sample. R13 PARTIAL.
- **Instrument:** a four-point difficulty rating by the subject plus an independent tester rating;
  heart rate and oxygen consumption were considered and rejected. Acceptable if ~80 % rate it 1–2.
- **Walter 1971 at second hand** (extraction 64, root `untraced`, as extraction 57 did for Elmer):
  1:9 over 10 ft and 1:16 over 20 ft for self-propelled chairs. A second reader of Walter, which
  corroborates the *report* of Walter and is not a second root. It is not fully independent: each
  report knew of the other's work (§0b, #12).
- **Backward pass:** the reference list is five entries (rendered, transcribed, persisted as a READ
  derivation); none is new. `python3 scripts/research/mining_screen.py --ref REF-01008 --compare`.

## 5. Footnote c — first persisted render, and what it settles

Index 56 of REF-01005's scan, rendered at 200 dpi: superscript c on the **1:8 (2 ft run, 3 in rise)**
and **1:10 (8 ft run, 9 in rise)** rows only; the footnote reads "Based on research of others
(Templer, 1977 and **Walters**, 1971)." **No render of this page had been *persisted* before.** Batch
19's persisted renders are indices 55, 162 and 167–169 (`ls retrieval-log/*/5dd866a236fb5978.p*`).
- This paragraph first went further: it said GAP-037's statement that the reading was "confirmed
  independently on a rendered page image" was wrong about the evidence. **That was my error.**
- Batch 19's independent adversarial subagent had rendered index 56 in its scratchpad and read it.
  An `ls` of persisted renders could not see that (§0b, #3).
- GAP-037's 2026-09-20 statement was true. Extraction 67 now carries the footnote verbatim, beside
  extraction 56.

**The new finding is geometric.** Table 13's two footnote-c rows have *exactly* the run and rise of
Templer's test ramps 9 (1:8, 2 ft, 3 in) and 6 (8 ft, 9 in = 1:10.67). That is consistent with the
cited Templer being the Georgia Tech ramp work.

**What the Templer data say about those rows, qualified after the independent pass** (§0b, #1):
- **Ramp 6 was unacceptable to manual wheelchair users in ascent** (58 % against the ~80 % line;
  extraction 66), and Templer's own Table 20 stops 1:10 at a 6-inch curb.
- So Table 13's 1:10 band is more permissive than *REF-01008's* data, a report dated May 1980, after
  REF-01005. It is **stricter** than footnote c's other warrant, Walter as Templer reports him (1:9
  over 10 ft; extraction 64).
- **Ramp 9, the other footnote-c geometry, was unacceptable in descent to people with walking
  difficulties** (Conclusions p.33; Table 19 row g; extraction 60).
- This section first reported only ramp 6.

**What it settles:** footnote c does not mark the 1:12 or 1:16 rows, so it is not a warrant for 1:12.
REF-01005 does separately cite Walter as corroborating 1:16 over 20 ft on its page 163 (extraction 54);
this line first said it cited neither for 1:16 (§0b, #7). **What it does not:**
which document "Templer, 1977" is. There are now three candidates — the 1974 stairs dissertation, the
FHWA ramp study (dated 1980), and a forthcoming Templer book *Stairs and Ramps* that NBS IR 78-1554
cites six times. Candidate 115 stays PENDING; no edge was written from extraction 56 (R15).

## 6. Candidate 117 — NBS IR 78-1554 — rehomed

Read in full from NIST (text layer sound; low-text pages checked). A stair-accident study for the
CPSC; **no ramp recommendation**; every "gradient" is its *orientation gradient*, a perceptual measure
(a false friend). Rehomed to `stair-ramp-threshold-biomechanics-accessibility`: in prose at first,
and in the typed `suggested_slug` only after the independent pass found the column still named this
slug and `resolve-candidate` gained the flag to fix it (§0b, #5). P3a and P3b held.

## 7. GAP-033 — term adjudication has now run over the whole backlog

Every `observed_terms` row has an adjudication with a rationale specific to its context quote.
**Derive:** `select outcome, count(*) from term_adjudications group by outcome`. Six terms minted
through `add-term`, each warranted by the corpus: `ramp` (the element), `level difference`,
`ramp run length`, `intermediate landing`, `ramp usability` (the outcome side; effort, discomfort and
difficulty scales are adjudicated to it as measures), `accessibility audit`.
`select term_id, canonical_en from terms where created_by_session like '%batch-20%'`.

**The deferrals are vocabulary decisions, not phrase decisions**, and GAP-033 stays open to hold
them. The one that matters most for the determination: **ramp versus route gradient** — TERM-001 is
defined on ramps, four observations measure path and trail slopes, and **extraction 49 already files
REF-01003's path slopes on parameter 3.** Whether parameter 3 covers route running slope is a scoping
decision for whoever re-determines it. P5a (a writer defect would surface) was **not** borne out.

**Owner ruling 2026-09-25 (§0b):**
- TERM-089 `ramp` is narrowed to exclude the running slope of paths, walkways and trails, so it no
  longer pre-decides that question.
- Three further points on the minted terms stay **open** on GAP-033:
  - TERM-094's scope note universalises one testable prior.
  - TERM-093 forecloses a separate criterion term.
  - TERM-092's scope note has a dangling reference.

## 8. The exhausted three — per the owner ruling of 2026-09-25

"If we can't access something from anywhere then we have to give up on it for now." Applied
literally: **no retrieval of REF-01002, Walter 1971 or the 1957 dissertation was attempted.**
Candidates 109 and 110 were re-described as exhausted and not queued for anyone, with the routes on
record. Their typed disposition could not say so until the owner's second ruling added `EXHAUSTED`
(migration 096); both now carry it (§0b). Batch 19's request-based next steps are withdrawn by the
ruling (rule 0). REF-01002's
`verification_note` states the disposition; status UNVERIFIED and disposition OPEN are unchanged
because no writer closes them with this reason. GAP-016 stays OPEN, marked NOT-ADDRESSABLE;
GAP-026 CLOSED-DECIDED; GAP-020 and GAP-024 annotated as an accepted limitation.

**One metadata fetch was made, and it is not a full-text attempt:** the publisher's table of contents
for JAPR 26(2) (born-digital PDF, rendered and attested — the attested render was made during the
adversarial pass, after the notes that describe it were written). It prints **"Jerome M. Welner"**.
The stored author row says "Weiner" and **cannot be corrected**: `correct-source` refuses DOI-less
sources and is the only verb that rewrites an admitted source's authors. GAP-044 records the writer
gap rather than bypassing it.

## 9. Where the runbook was wrong on live state

- Candidates 123 and 124 were described as "both open access, retrievable". 124 was.
  - **123 is free to read but not OA-licensed**, and it was not retrievable from here: Unpaywall and
    OpenAlex both give `is_oa` true, green, via PMC. This line first said "123 is not" open access
    (§0b, #19).
  - The access barriers are real.
- Candidate 124's `tier_guess` 2 was, as the runbook warned, not authoritative: T3.
- "Table 20 over 1:8/1:10/1:12/1:16" is right, but it is **a curb-ramp table conditioned on curb
  height**, which changes what it can say about parameter 3.
- The runbook said to "admit" 123 and 124; only 124 could be read, so only 124 was admitted.
- The runbook said batch 19 "called this 'not settled' without ever actually rendering that page".
  - This line first called that correct and GAP-037's claim of a render the error. **Both halves
    were wrong.**
  - Batch 19's independent subagent rendered and read index 56 in its scratchpad. It was never
    persisted (§0b, #3).
- Candidate 117 → a stairs slug exists (`stair-ramp-threshold-biomechanics-accessibility`), so REHOME
  rather than OUT-OF-SCOPE, as the runbook allowed.

## 10. Priors, scored

| Prior | Result |
|---|---|
| P0 pointer repair exposes nothing | **Held** (with vacuous rules noted) |
| P1a compliance figure (Garg 0.7 / Pinto 0.55) | Pinto **falsified** (presence only); Garg **untestable** |
| P1b no threshold derived from outcomes (0.9) | **Held** for Pinto |
| P1c yardstick = national code | Pinto **not tested** — no gradient yardstick at all |
| P1d no Co-1 warrant (0.8) | **Held** for Pinto |
| P1e neither lands at T1 (0.8) | **Held** (T3) |
| P1f PROXY/PARTIAL (0.85) | **Held** (graded PROXY; PARTIAL by owner ruling 2026-09-25) |
| P2b Table 20 does not endorse 1:12 unqualified (0.6) | **Held**: 1:12 is endorsed only up to a 9-in curb, under a footnote urging gentler slopes. First scored "Falsified", which read a qualification as none (§0b, #18) |
| P2c subjective rating, not physiological (0.55) | **Held**; physiological measures considered and rejected |
| P2d Walter given as a ratio (0.6) | **Held** |
| P2e Table 20 legible only on the render (0.5) | **Half**: the text layer carries it column-wise with O read as 0 |
| P2f older/ambulant subjects included (0.75) | **Held**, but the wheelchair group itself is young |
| P3a/P3b | **Held** |
| P4a markers on 1:8/1:10 only (0.8) | **Held**; P4b "Walters" (0.8) **held** |
| P5a writer defect surfaces (0.5) | **Not borne out** |
| P5b modal outcome NAMES-EXISTING/DEFERRED (0.6) | **Held** |
| P5c ≥1 NAMES-NEW (0.4) | **Held** |
| P6 determination does not move (0.97) | **Held** |
| P7a new Co-1 source reachable (0.4) | **Partly**: found and staged, not admitted |
| P7b T2 review tabulating ramp compliance (0.35) | **Not found** |

## 11. Gates

- `research_batch_dod --session <this>` — COMPLIANT on canonical after both migrations. Several rules
  examine nothing this batch (R3: no T4–T6 admission; R5: nothing non-English; R11: no aliases).
- `research_batch_dod --all` — COMPLIANT.
- `test_db_integrity` on the scratch DB before the term adjudications — all PASS; re-run by the
  diff-scoped gate below.
- `retrieval_log --verify-authors` — CLEAN for REF-01007; REF-01008 has no DOI and is outside it.
- `migrate_db --rebuild` reproduces every row this batch wrote; the only drift is the bot's direct
  writes to REF-01006 and `pipeline_runs` (rule 3), which predate this branch.
- `scripts/regenerate_derived.sh` — `--check`-clean.
- `run_checks --changed-from origin/main --explain`, run once at the end: **RESULT PASS**, no blocking
  failure; `run_checks --selftest` PASS. Re-run rather than trust the counts it printed.
  - Advisory failures that are red for reasons this branch did not cause, checked one by one:
    `migration_reproducibility_deep` (the bot's direct UPDATE to REF-01006), `validate_schema_cross_check`,
    `validate_pydantic_schemas`, `retired_vocabulary` (no hit in any batch-20 file),
    `metadata_integrity_audit`, `validate_reasoning`, `source_locators_integrity`, and
    `site_pages_fresh` (examined 0 — vacuous, not a pass).
  - **One advisory failure this branch DID grow, and my first reading of it was wrong:**
    `research_protocol_audit` CHECKs 7 and 8 named REF-01007 and REF-01008 as having **no admitting
    search**.
    - I called that the audit's case (b) and wrote no edge. **Wrong** (§0b, #6).
    - Case (b) is a code clause or a named standard. S01's own design says the search that surfaced
      a candidate and the search that admitted its source are one event, and batch 17's exec 77 is
      the precedent.
    - This is case (a) plus a writer gap. Logging a *new* search would indeed have broken S01, and
      no verb could attach an admission to an *existing* one.
    - Fixed in the second fix-forward: `link-admission` (GAP-046) wrote (91, REF-01007) and
      (90, REF-01008). S01 now examines this batch's admissions.
  - `citation_mining_session` is NOTHING-IN-SCOPE under the new pointer: this batch admitted no
    slug-linked T1-2 source. Correct, and uninformative.
- **After the second fix-forward** (§0b; run once, on canonical):
  - `migrate_db --rebuild` reproduces every row. A full-row diff of every table differs only in the
    ledger's `applied_at` and `applied_by_session` columns, REF-01006's bot-written author and source rows, and `pipeline_runs`
    (rule 3), as before.
  - `test_db_integrity`: S01 now examines this batch's two admissions as well as batch 17's.
  - `run_checks --changed-from origin/main --explain`: **RESULT PASS**, no blocking failure.
    `--selftest` PASS. `research_batch_dod --session <this>` and `--all` COMPLIANT.
  - `research_protocol_audit` no longer names REF-01007 or REF-01008. It stays red on REF-00987, which
    predates this branch.
  - `test_verification_pipeline` came into scope because `scripts/db.py` changed. Its three failures
    (the ≥50/≥30/≥100 corpus assertions CLAUDE.md rule 7a names) are identical on origin/main's DB.
  - `scripts/regenerate_derived.sh --check`-clean; context map regenerated.

## 12. What the next batch takes

1. ~~The independent antagonist pass~~ — run; §0b. What it left for the owner is on GAP-048
   (independence counting absences) and GAP-033 (three term points). GAP-049 records the thin R1 leg,
   for a Co-1 pass that reaches beyond one English biomedical index.
2. **The ramp-versus-route scope of parameter 3** (GAP-033 group 1; extraction 49). It decides what
   evidence the next determination may rest on.
3. **Candidate 126 (Mactaggart 2024)** — the supplementary appendix's ramp criterion, then a D-0178
   reading of the co-production. The strongest Co-1 lead in view, but its facilitators' recorded
   disabilities include no mobility impairment.
4. **Candidate 129 (Martins 2016)** — read the Portuguese body for its measured-slope compliance rate.
5. **GAP-044** — let `correct-source` take a persisted non-Crossref artefact, then correct REF-01002.

Not owed, per the owner ruling: REF-01002, Walter 1971, the 1957 dissertation.
