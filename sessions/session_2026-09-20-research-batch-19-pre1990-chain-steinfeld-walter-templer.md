# Batch 19 — the pre-1990 chain: Steinfeld's bibliography, Walter, Templer

**Assignment:** batch 18 §9 items 1–4, in that order. GAP-025 established that a deferral runs
because a batch is told to run it, not because a counter goes red; this is that batch.

**Priors:** `scratchpad/<session>/priors.md`, committed **before** the bibliography was transcribed
or any screen run. P6 (Co-1) was appended later and says so in its own text.

**Derive every figure below.** Nothing here is a count to quote.

---

---

## 0. RETRACTIONS — read this before anything below it

**An adversarial pass over this batch refuted two of its headline findings and five
smaller ones.** Everything below §0 was written before that pass and is left standing as
the record of what I claimed; the corrections are here, in the database rows they touch,
and in the amendments to GAP-037 and GAP-041. Where §0 and a later section disagree, §0
wins.

### R1. "Templer has no ramp research" is FALSE, and it inverts §3, §4 and §13

§4 concluded that John A. Templer's corpus is *"stairs end to end"*, *"four items across
fifteen years, not one about ramps"*. **Templer, John A., _Provisions for elderly and
handicapped pedestrians_, FHWA-RD-79-1/-2/-3** (Georgia Tech Pedestrian Research
Laboratory, contract DOT-FH-11-8504) is a dedicated ramp study. Volume 3's Part I is
*"Short Ramps, Tactile Surfaces and Wheelchair Dimensions"*, opening with **"A Study of
Short Ramps"**; it carries **32 gradient-rating tables** for manual and electric
wheelchair users, cane users and ambulant disabled people, ascent and descent separately;
and **Table 20, "Ramp Gradient Recommendations"**, over gradients **1:8, 1:10, 1:12 and
1:16**. Full text is free on Internet Archive. Derive it:

    curl -sS 'https://archive.org/advancedsearch.php?q=creator%3ATempler+AND+%28pedestrian+OR+ramp+OR+handicapped%29&fl%5B%5D=identifier&rows=20&output=json'
    curl -sSL https://archive.org/download/provisionsforeld00temp_0/provisionsforeld00temp_0_djvu.txt | grep -ci ramp

**How I got it wrong is worse than the fact.** The Crossref query I described as
"resolving his corpus" was `query.bibliographic=Templer+stair+shape+human+movement` —
**a query containing "stair" returned stair papers.** That is query shape, which is R14,
which the same note invoked against ERIC two sentences earlier while exempting itself.
And I never pointed Internet Archive at Templer, though I used that exact endpoint for
Walter an hour before.

**The priority conclusion is inverted, not merely weakened.** §3 argued the footnote scope
means Templer is not part of the 1:12 chain and his retrieval matters less. Table 20
recommends over **the same four bands as Steinfeld's Table 13**, whose footnote marks the
two Steinfeld did not test. Retrieving Templer is now the **strongest** lead on what
footnote c means. Staged as **candidate 125**, and it should be the next batch's first
admission.

### R2. "The scan is unreadable" is FALSE, and it is the deeper error

§2 and the transcription artefact recorded *"no OCR engine is available in this
environment … so this text layer is the best that exists here"*, then marked authors
illegible, years unresolvable, and one title's slope term absent. **The pages are JBIG2
images and render legibly in about a second.**

`pypdf` reads a **text layer**. When that layer is mush it tells you the layer is mush and
**nothing whatever about the document**. I read the mush as a property of the page, and
then reasoned carefully, at length, and wrongly about the consequences — including
building a floor/ceiling band into `mining_screen.py` to bound a damage the document does
not have. **The band was measuring the distance between a bad text layer and my own
guesses.**

What the pages actually say, re-transcribed and persisted as the superseding artefact
`c9361532746ffec9.json`:

| I recorded | The page says |
|---|---|
| "C[u]rren", filed at position **C** | **Birren, J.E.**, *Psychology of aging*, 1964 |
| "'Ramps' IS NOT legible" | **Corlett et al., _Ramps or stairs_**, Applied Ergonomics 3:4, 195–201, 1972 |
| year "not resolvable to 1957" | **Elmer, C.D. … University of IL, 1957** |
| "AUTHOR LOST TO THE SCAN" | **Jones, J.C.** |
| "Steinfeld, **Eckard**" recorded as the reading | **Steinfeld, Edward** |
| "[?] [Un]iversity" | **New York: Columbia University**, 1974 |
| initial "NOT an F on its face", year damaged | **Walter, F. … 1971** |

I also invented an anomaly to explain a misreading: having filed Birren under C, I wrote a
note claiming Brattgard was *"out of strict order in the scan"*. **The list is in strict
alphabetical order.**

**The measurement changes:** `slope-strict` on REF-01005 is **2**, not the 1–2 band
reported — Corlett scores in the floor once the title is read rather than guessed.

### R3. Five smaller corrections

- **GAP-041 asserted TRID "reports 20 results".** The artefact contains **no result count
  at all**; the five "Templer" hits are echoes of my own query string. I typed a number
  the bytes do not support, inside a gap whose subject is people mis-scoring retrievals.
  TRID is also **reachable** — batch 16 fetched a record page — so filing it as a closed
  host was wrong.
- **Footnote c reads "Walters, 1971", not "Walter".** Extraction 56 normalised it and
  blamed OCR, erasing a real inconsistency between the report's footnote and its
  bibliography.
- **ERIC returned `numFound` 33 but the request carried `rows=25`.** Eight records were
  never seen; "33 records, none architectural" overstates what was examined, and
  `results_screened=43` is a hand-typed figure the artefact contradicts.
- **"26 of 27 sources have no logged retrieval"** (§11) conflates two things. The tool
  reports **12** DOI-bearing rows with no logged retrieval; 14 others were skipped for
  carrying no DOI, several of which *do* have logged retrievals.
- **§6's "each step came from widening the sample" is wrong at the last step.** Within
  REF-01005 the sample **narrowed**: 124 → 18 returning for 1:16 → **3** for 1:20. The
  1:20 row rests on three people.

### R4. The author of the 1957 dissertation is contested

Templer's FHWA report cites it as **Dixon, Charles E.**; Steinfeld's bibliography plainly
prints **Elmer, C.D.** Two federal reports of the same period disagree. §6's "an author it
never had" should not be read as settled, and candidate 110 now records both.

### R5. What survives the pass

The **footnote-scope reading itself** (marker on 1:8 and 1:10 only, Table 12 confirming the
tested set) was independently confirmed on the rendered page. The 38-entry count, the
ANSI-to-Webb completeness, the Walter holdings identifiers, the REF-01006 admission and
its Co-1 warrant, the compliance figures, and `research_batch_dod` 19/19 all re-derive
correctly. **No letters were smuggled into the conservative transcription** — the band was
useless here, but it was not dishonest.

### R6. Mechanisms fixed, because each of these was a missing mechanism

- **`scripts/research/page_image.py`** renders a persisted PDF page so a session can *look*
  at a scan. `pymupdf` is declared in the check-registry batteries. **This is the fix for
  R2**; without it the next session meets a damaged scan and reasons about its limits
  instead of reading it.
- **`mining_screen.py`** now labels provenance **READ** vs **SCRAPED** vs **DEPOSITED**, and
  a superseding transcription wins over the one it replaces — previously a corrected
  38-entry list could never beat the damaged 38-entry list written to replace it.
- **`amend-source` gates every amendable field against its column's CHECK**, derived. The
  verb I added earlier this batch to fix a vocabulary typo would have accepted the same
  typo.
- **`correct-source` reaches `journal_name` and `publisher`**, from the payload. REF-01006
  was stamped `COMPLETE` with no journal name, and `author_fidelity` could not see it
  because its comparison never looks at `container-title`. GAP-031 had already named this.
- **`amend-extraction` reaches `root_type`**, gated by the column. Extraction 57 claimed a
  primary measurement with no root, and `v_unregistered_roots` could not see it because it
  filters on `root_id IS NOT NULL`.

---

## 1. What the batch was for, and what it actually found

Item 1 was the assigned work and it produced the batch's substantive finding, which is **not** the
one the assignment anticipated. The assignment expected REF-01005's reference list to be "the index
to the whole pre-1990 layer". It is 38 entries of **ergonomics**, and the two items its own
recommendation table names as warrants do not behave as the register assumed.

## 2. Item 1 — REF-01005 backward, and four predictions

No Crossref deposit exists for this report, so there was no reference list to fetch. The 38 entries
were transcribed from the persisted ED184280 scan (pypdf page indices 167–169) and persisted as a
**derived** artefact. Derive the yield:

    python3 scripts/research/mining_screen.py --ref REF-01005 --compare

| Prediction | Result |
|---|---|
| **P1a** ≥ 60 references | **FALSIFIED** — 38 |
| **P1b** slope-strict yield 3–12 | **FALSIFIED** — the band is below it |
| **P1c** slope-loose ≥ 3× slope-strict | **FALSIFIED** — they are almost the same |
| **P1d** Templer and Walter both present as discrete entries | **CONFIRMED**, with a discrepancy worth more than the prediction |

**On P1b I must record a second failure, of my own instrument rather than of the prediction.** I
pre-registered "falsified if the yield is 0 or ≥ 20". The yield missed the predicted band and **did
not trigger my own falsification condition**, because I set that condition far wider than the
prediction it was supposed to test. A threshold that cannot fire when the point prediction fails is
not a test. Reported here rather than behind the looser rule that let me off.

**On P1c the reasoning was wrong in a way worth keeping.** I predicted the bare stem `accessib`
would fire on everything because REF-01005 is an accessibility report. It fires on almost nothing:
the **bibliography** is a human-factors and ergonomics bibliography — Damon, Diffrient, Kroemer,
McCormick, Murrell, Poulton, with *Human Factors* and *Applied Ergonomics* as the recurring venues.
A 1979 federal accessibility report drew its authority from ergonomics, not from a disability
literature. That is a finding about the period, and it means **a screen's behaviour tracks the
literature an anchor cites, not the subject of the anchor itself.**

**The most instructive result is a negative one.** Walter's entry scores **zero under every screen**,
because its title in this bibliography carries no slope term — *"Part 3: Ramp gradients"* is a part
title. The single most slope-relevant item in the list is invisible to a title screen. No later
reader should read a low yield here as a thin literature.

## 3. Table 13's footnote is narrower than the register records — and this runs against GAP-037

GAP-037 clause (4) says Table 13 "rests partly on others" and treats Templer and Walter as the two
remaining nodes of **the 1:12 chain**. Reading the table itself:

- The footnote marker `c` appears on the **1:8 and 1:10** rows. It does **not** appear on 1:12 or 1:16.
- Table 12 shows the study tested exactly **1:12, 1:16 and 1:20**.

So the two bands carrying "based on research of others" are **precisely the two outside the tested
range**, and the 1:12 and 1:16 rows rest on Steinfeld's own data. On that reading Templer and Walter
are not nodes of the 1:12 chain at all, and the priority of retrieving them drops.

**Held as a reading, not as settled.** These are single characters on a damaged scan. A cleaner copy
of page 57 decides it in one look. Recorded as extraction 56 and as an amendment to GAP-037 rather
than as a correction to it.

## 4. Item 3 — Templer 1977 does not resolve, and the surname is settled

Four indexes, and the negative is well-formed rather than empty (R14):

- **ERIC** `author:"Templer"` → 33 records, a healthy set, **none architectural** (Bill Templer,
  education; Donald I. Templer, psychology; Andrew J. Templer, management; Lois; Sally).
  `"Templer" AND "stairs"` → **0**. A sound query shape returning 33 and a topic conjunction
  returning 0 is genuine absence *in ERIC*, which is an education index.
- **OpenAlex** Templer + 1977 → 10, none architectural.
- **Crossref** on the dissertation title REF-01005 actually lists → **John A. Templer's corpus**:
  1974 dissertation *Stair shape and human movement*; 1978 *An analysis of the behavior of stair
  users* (NBS IR 78-1554, doi 10.6028/nbs.ir.78-1554); 1984 *The Forgiving Stair*; 1989 *The Soft Stair*.
- **TRID** served a 200 whose page carries no extractable record — a JS shell. Nothing is
  established about what TRID holds.

**Four items across fifteen years, not one about ramps, and nothing dated 1977.** The bibliography's
own Templer is the 1974 stairs dissertation, so the report cites a year its own reference list does
not carry.

**Which item footnote c meant is still not guessed** — batch 18 §9 said it must not be, and the two
nearest neighbours (1974 and 1978) straddle it. Candidate 115 called it "the ramp-slope research";
that was a guess and it is corrected under R15. Candidate 117 stages the 1978 NBS report as the
nearest *resolvable* neighbour, explicitly without claiming it is the referent.

**The structural finding survives whichever it is:** footnote c warrants Table 13's steepest bands on
two named parties, and one of them has no ramp research to his name.

## 5. Item 2 — Walter: the named route is closed, and the holdings layer is what is new

**Jisc Library Hub Discover is unreachable from here** — HTTP 403 behind a Cloudflare interstitial,
twice. Candidate 109 and GAP-037 both named Jisc as the next route; it is closed, and nothing is
established about what Jisc holds.

**A correction I nearly filed and did not.** I formed the hypothesis that batch 18 had fetched the
Open Library record and failed to read it, and checked before writing anything. **It had read it** —
Felix Walter, DLF, London, 1971, 60 pp is already correctly in candidate 109, with the
corporate-versus-directing-author distinction properly drawn. Nothing is retracted from it. Recording
the near-miss because a false accusation against a previous batch would have been cheap to make and
hard to unpick.

**What is new is the holdings layer:** ISBN-10 0901908053, **LCCN 77502052**, **OCLC 222208**, LC
class NA2545.P5 D5, one edition, source record `marc:marc_loc_2016` — a Library of Congress MARC
record, which is why the 1971 date is authoritative rather than inferred while the bibliography's own
year digits for Walter are OCR-damaged. GAP-026 says what this needs is document delivery, not
another search. **An OCLC number is what converts "find Walter 1971" into "request OCLC 222208".**

## 6. New: Elmer 1957, and the literature correcting itself

REF-01005 reports that **Elmer (1957) found 1:8 acceptable as a maximum** and then discounts it — his
subjects were young, highly trained users at a rehabilitation-education centre, where Walter's sample
and Steinfeld's own included large proportions of older people and many with reduced arm function and
low stamina. Extraction 57, `contested=1`.

That is a **sampling** objection, made in 1979, on exactly the grounds this project would use today.
It also dates candidate 110 from a primary source and gives it an author and a form it never had.

**The trajectory is the finding:** 1:8 (1957, discounted as unrepresentative) → 1:12 (measured and
found wanting, 1979) → 1:16 (Walter and Steinfeld converge) → 1:20 (every wheelchair user completed
40 feet). **Seventy years in one direction, and each step came from widening the sample.**

## 7. Co-1 pass — added because R1 failed, and it found the low-probability branch

`research_batch_dod` R1 failed and named a real omission: the batch had no Co-1 leg. Remediated with
a real pass, not a waiver. P6 was written and committed before any Co-1 query fired, and says in its
own text that it is not pre-registration of the batch.

**REF-01006 admitted** — Raghuram, Verma, Lavalekar, Virk, Bhan and Singh 2026, *Participatory
accessibility audits as a tool for disability-inclusive health systems: Findings from two Indian
states*, doi 10.1016/j.dialog.2026.100342, open access, full text retrieved as JATS XML and persisted.

**Co-production evidenced in the retrieved bytes (D-0178), at three levels:** the research team
"composed primarily of persons with disabilities"; a Community Advisory Board of disability rights
advocates; and **all** field investigators persons with disabilities, audits run with a DPO. Named as
Community Based Participatory Research, closing on *"Nothing about us, Without us"*.

**It states a gradient and the statement must not be over-read.** 1:12 is a yardstick taken from the
Harmonised Guidelines and Standards for Universal Accessibility in India (2021) — **not a figure this
study derived** — so it is not Co-1 evidence that 1:12 is right. What it measures is compliance:
**20 of 35 government hospitals** at 1:12 or gentler; 17 of 24 in Madhya Pradesh, 3 of 11 in Goa. An
R7 failure record. Handrail provision is far worse than gradient and would be the finding if this
project held a handrail parameter.

**P6c was wrong and the shape of it was the problem.** I pre-committed to reporting a silence as a
finding, and a source turned up instead. **A prior that makes a null valuable is a prior that makes
looking harder feel unnecessary**, and I would have accepted the silence too readily. **P6b is
untested rather than confirmed:** every query was date-unbounded or post-2000, so nothing was learned
about whether disabled-authored ramp work exists pre-1990.

## 8. The environment finding — GAP-041

Three batches have each independently discovered that **the discovery-catalogue stratum is closed
here**: HathiTrust (batch 18), Jisc (this batch, twice), TRID (this batch, JS shell). None is a null.
The routes that work are **deposit-based**, not catalogue-based.

**Google Books is not merely exhausted.** Batch 18 read its 429 as a daily quota; queried two days
later the body reads `quota_limit_value "0"` — a zero allocation. It will not reset, and no batch
should spend a query discovering that again.

**One query-shape lesson worth more than the whole ladder.** Batch 18 searched Open Library for
Walter 1971 **by title** and got 0. This batch searched the same index **by publisher** and got 99
DLF records with the target among them. Same index, same coverage, opposite result. For an
institutional report the well-formed query is often the **publisher**: a report's title is unstable
across catalogues, its issuing body is not.

## 9. Tooling, and why each piece was necessary rather than nice

- **`retrieval_log.derive()`** persists an artefact made from bytes already on disk. Deliberately not
  `fetch()`: that function promises the artefact is what a host served, and an OCR transcription was
  served by nobody. Marked derived, given a `derived:` URI that cannot be re-fetched, `status` null.
- **`mining_screen.py` grew a provenance column.** Its one heading was `deposited` and it would have
  printed that over a transcription — an extraction restated as a deposit, in a tool's own output.
- **A yield over a damaged scan is now a band**, floor to ceiling. Without it the transcriber picks
  the yield, which is the same defect the screen registry exists to prevent, one layer in.
- **`source_type` added to `_AMENDABLE`**, and `add-source --help` corrected. See §10.

## 10. Three defects in my own work, all caught by gates before merge

1. **B05.** I wrote Crossref's `journal-article`; the enforced vocabulary is `journal_article`.
   **`add-source --help` advertised the hyphen the blocking check rejects.** Help text fixed, and
   `source_type` added to `_AMENDABLE` so the next session does not need a compensating migration for
   a typo.
2. **`extraction_relations_integrity`.** Extraction 56 was `figure_role='condition'` and qualified
   nothing — its referents are candidates, not rows, which is why no edge could be written. Re-roled
   to `claim`, which is what it is.
3. **`author_fidelity`.** REF-01006 was stamped `metadata_quality='COMPLETE'` while volume,
   article_number and pages were NULL and its own payload supplied all three. Backfilled from the
   payload with `correct-source`.

**All three were mine, all three were caught, none reached main.** The gates did their job on a
session that was reading carefully and still got three things wrong.

## 10a. The B05 fix was a hand edit, and it was corrected to a mechanism

**Added after §10 was written, on the instruction "fix mechanisms, not hand edit" — which
landed on a real gap in what §10 describes.** Fixing my row and correcting the help string
left the mechanism exactly as it was:  declared **no CHECK**, and the
vocabulary's only home was a seventeen-value tuple in a test file. That is CLAUDE.md rule
8's named anti-pattern, in a file that had already fixed the same pattern one check along
(B06, , 2026-09-18) — the comment recording that fix sits eleven lines below
the tuple.

**The failure was three mechanisms deep, and only the third caught it:**

1.  **accepted** the bad value. Every other vocabulary flag on that
   command validates against the live schema; that guard was silently off here because an
   undeclared vocabulary reads as *no constraint*.
2.  **advertised** the value the blocking check rejects.
3. B05 caught it, from the curated tuple, two steps after argparse could have refused it
   for free.

**Migration 089** puts the vocabulary in the column's own CHECK — the ratified answer, per
CLAUDE.md §4 ("vocabularies come from the schema, not a list in code"). Deliberately **not**
a  enum in : that would move the list, not remove it, and
leave two homes where rule 5 allows one.

Three consumers now derive from that one declaration:

-  takes , so **argparse refuses the typo
  before the command runs** and names the live set.
-  renders the vocabulary instead of restating it, so it cannot drift again.
- **B05 reads ** and the tuple is gone.  75/75.

**The DDL was generated from the live schema, not retyped.**  has 97
columns; hand-transcribing them to add one constraint would have been the same class of
error the migration exists to fix. **The first attempt failed and is worth recording:**
SQLite validates the whole schema during , so the five dependent
views aborted it with *"error in view v_evidence_authors: no such table"*. It rolled back
atomically and left the blob untouched — 's transaction boundary (DR-2026-08-19
F5) doing its job. The migration drops and restores those views verbatim.

 reproduces the result, which is the check that matters for a table
rebuild.

**GAP-042 records what this did not do.** Four sibling vocabularies on the same table —
, , , 
— are still curated tuples over columns that declare nothing, and each is one 
flag away from the identical failure. They were left because each CHECK costs a full rebuild
of a 97-column table and this batch did one to fix the defect it had actually caused, not
four more on spec. The gap notes that all four fit in **one** rebuild.

## 11. Gates

- `research_batch_dod --session` — **COMPLIANT, 19/19.** R1 and R7 failed first and were remediated
  by a real Co-1 pass and real candidate staging, not by waiver.
- `run_checks.py --changed-from origin/main` — **PASS.** Re-derive the counts.
- `run_checks.py --selftest` — **PASS.**
- `retrieval_log --verify-authors` — clean for this batch's one admission. 26 of 27 sources have no
  logged retrieval and are not verifiable offline: a corpus-wide condition this batch neither caused
  nor fixed.
- Derived outputs regenerated and `--check`-clean; context map regenerated.

## 12. The determination did not move, exactly as predicted

**Parameter 3 × MOB stays undetermined. Determination gate 1 stays open. `specifications` gains no
live row.** Prior P4 put this at 0.95 and gave the reason: the blocker is C10 over REF-01002's
UNVERIFIED status, which nothing in this assignment touches, and both retrieval targets are pre-1990
and therefore historical grounding under the owner ruling of 2026-09-18. **Retrieving both in full
would still leave the cell undetermined.** That is the batch's expected outcome, not a shortfall.

## 13. What the next batch takes

1. **The accessibility-audit cluster, and it is the cheapest real evidence in view.** REF-01006's
   references hold at least five audits of real health facilities — Pinto 2021 (Brazil, national,
   doi 10.3390/ijerph18062953), Garg 2024 (doi 10.1016/j.mjafi.2022.10.011), Singh 2024 (New Delhi),
   Sharma 2025 (Gwalior), Mohapatra 2024 (doi 10.12688/f1000research.156920.1). Candidates 123 and
   124 stage the two strongest. **Every one scores zero under `slope-strict`** — an audit tabulates a
   measured gradient while naming no geometry in its title, which is the Walter false negative from
   the opposite direction. They are DOI-bearing and open access, so unlike everything this batch
   chased they are actually retrievable here.
2. **Templer 1978, one retrieval and no more** (candidate 117). NBS is now NIST and its internal
   reports are public. The question is narrow: does it contain any rampway recommendation at all?
3. **Walter 1971 and Elmer 1957 go to document delivery, not to a fourth retrieval ladder** —
   OCLC 222208 / LCCN 77502052; ProQuest or the University of Illinois repository.
4. **Confirm or refute the footnote-c scope** (§3) against a cleaner scan of page 57. It is one look
   and it decides whether Templer belongs in the 1:12 chain at all.
5. **GAP-016 stays open and is not a search.**

**Not attempted, and owed a third batch running:** GAP-033 — term adjudication has never run.
`term_adjudications` is empty while `observed_terms` is not, and this batch added three more to the
unadjudicated pile.

---

## 14. Code-review repairs — fifteen findings, and the worst one was a gate I had just added

A `/code-review` pass over the diff found fifteen defects. Most were mine and recent; the
two that matter most were in the *repairs* made earlier in this same batch, which is the
pattern worth naming: **fixing a mechanism badly is its own failure mode, and it hides
behind the fact that a fix was made.**

### The worst: `schema_walkability_fresh` was red by construction

The new page embedded `date.today()` and the short HEAD sha, and `--check` compares
byte-for-byte. **Committing the page changes HEAD, so the committed file records the
previous sha forever, and the date rolls over nightly.** Measured on this branch:
committed `4c9a38e` against HEAD `ab695e6`, `--check` STALE, the registered check red.

Two things make this worse than an ordinary bug. **The registry note I wrote for that
check argues against exactly this** — *"the repository has learned that a gate red by
construction teaches its reader to ignore it"* — and `scripts/regenerate_derived.sh`, the
sanctioned regeneration entry point, runs every `--check` under `set -euo pipefail`, so
**I had broken the one script CLAUDE.md tells sessions to use.**

Fixed by removing both volatile fields. The page's content is a pure function of the
schema, so it is rendered as one; *when* it was generated is already recorded, by git,
without anyone maintaining it. Two consecutive renders now produce identical bytes, and
`regenerate_derived.sh` exits 0.

### The second: three repairs each left the hole they were made for

- **`journal_name`/`publisher` added to `_CORRECTABLE`** broke the invariant that
  constant's own header states — *"EXACTLY what retrieval_log --verify-authors can prove
  against a payload"* — because I never extended the verifier. `correct-source`'s refusal
  message then named them as fields the verifier can prove, which was false. Fixed by
  extending `_BIBLIO_FIELDS`, so the invariant is true again rather than merely restated.
- **`root_type` made amendable** repaired one bad row and left the blind spot that let it
  through — `v_unregistered_roots` filtering on `root_id IS NOT NULL`, which I had *named
  in the comment* and not closed. **Migration 090** gives the view a `rootless` arm. Its
  first act was to catch a second row of my own: extraction 56 asserted a committee claim
  with no root. Repairing that needed `root_ref_id`, which no writer reached — now added,
  FK-validated.
- **`amend-extraction --reason` was silently discarded** when the value was already
  correct, though the flag's help says it is *"appended to notes, never overwriting"*. My
  own correction recording that a quote had been confirmed against a rendered page was
  written and lost. *"I checked, it was already right, here is what I found"* is a real
  result — often the only trace that checking happened — and it is now recorded.

### Instrument bugs the review caught

- **The SCRAPED band's ceiling could fall below its floor.** It scored only the `inferred`
  reading, and `_title` discards the unstructured text when an inferred one exists — so an
  entry matching the raw text but not the bracketed reconstruction was dropped from the
  upper bound, with `max(floor, ceil)` hiding it in the aggregate. A ceiling that can be
  lower than its floor is not a bound. Now a per-entry union.
- **`provenance_of` guessed from a magic string in the payload body** instead of the
  `derived` flag `derive()` writes onto the manifest — so any derived artefact not
  literally `kind == "pdf-bibliography"` printed as DEPOSITED, "the publisher's own
  reference list". Exactly the mislabelling that function exists to prevent.
- **`derive()` built a colliding URI** with no content hash, and `_logged_payloads` is
  keyed by URL — so a corrected transcription silently evicted the one it replaced, with
  file order deciding which survived. It also accepted an unvalidated `source_artefact`,
  and both live derivations named a PDF that resolves in neither this session's directory
  nor its manifest. Now hashed and validated.
- **Page renders had no manifest line** — unattested files in an evidence log, with no
  sha256 and no record of what they came from. `retrieval_log.record_file()` attests them.
- **`derive()` had no caller and no CLI**, so the sanctioned way to write a derived
  artefact existed only as an ad-hoc script outside the repo — CLAUDE.md §8's "an uncalled
  script is the same defect". Now `--derive` on `retrieval_log`.
- **`named_in` matched table names inside SQL comments**, and that list is the sole input
  to the cross-stage-pointer verdict. `v_item_provenance`'s comment mentions
  `evidence_source_authors`, which the tool duly reported as a table the view reads.
  `dbcore` already had the stripper.

### And one hand-typed count, in the sentence justifying the check

The registry note said *"five of the six pointers render 0 rows"*. **It is four.** A count
going stale inside the note that argues for the check — rule 7a, in the file CLAUDE.md §8
already lists as an outstanding offender. Replaced with the command that computes it. The
check also omitted the `tooling` kind its sibling declares, so a diff touching **only the
generator** — the change most likely to stale the page — selected nothing.

### What the review confirmed

Extraction 57's `claim_text` **is** verbatim: page index 162 was rendered at 150 dpi,
attested, and reads the sentence word for word. Its `VERBATIM-EXEMPT` warrant is now stale
rather than wrong — true of the text layer, no longer a statement about the document. The
page locator remains genuinely ambiguous (zero-based 162, one-based 163, printed 161, one
`page` scheme that declares none of them), recorded in **GAP-043** with the cheapest fix.

**Gates after the repairs:** `research_batch_dod` 19/19, `test_db_integrity` 75/75,
`run_checks --changed-from origin/main` PASS, `--selftest` PASS, `migrate_db --rebuild`
reproduces, `regenerate_derived.sh` exits 0.

---

## 15. `/simplify` — four agents, and the answer to "did we fix it mechanically?" was no

Four review agents (reuse, simplification, efficiency, altitude) over the same diff. The
owner asked whether the fixes were mechanical. **They were not, and three of the four
hand-patches were the same anti-pattern the fix was for.** Those are now closed.

### The hand-patches, and what replaced them

| hand-patch | mechanism that replaced it |
|---|---|
| grew `_AMENDABLE`/`_AMENDABLE_SVE_FIELDS` three times | **not fixed** — see below |
| migration 090 hard-coded 3 of `root_type`'s 5 CHECK values | **091** rewrites the arm in COMPLEMENT form: `NOT IN ('untraced','derived_calculation')`, each exclusion carrying its reason |
| `if field == "root_ref_id"` FK check | **`dbcore.fk_declared()`**, reading `PRAGMA foreign_key_list` — a no-op where no FK is declared, armed on both amend paths |
| 089 did 1 column of 5 | **091** carries the other four in the rebuild 089 had already paid for |

`_AMENDABLE` is the one I did **not** fix, and the reason is stated rather than skipped:
inverting it to a complement-of-`_CORRECTABLE` derivation would widen the write surface
across **97 columns, 79 of them currently unreachable**, and a wrong exclusion makes a bad
value writable that no gate catches. That is a change to make deliberately, not at the end
of a long session. GAP-013 already holds it; the measurement is added there.

### The defect on the page I shipped

`schema-walkability.html` stamped **UNWRITABLE on 18 tables** where `pipeline_walk.py`
reports **6 empty parents** — and `pipeline_walk.unwritable()`'s docstring names three of
my eighteen (`connection_targets`, `identity_medical_map`, `icf_medical_map`) as **known
writable**, because one `db.py` call inserts parent and child in the same transaction. I
re-derived a probe that already existed, and got it wrong. The tool now imports the
sibling for stages, the stage map, `live_tables`, `connect_ro`, `stage_label` and the
collapsed probe, reports roots, and carries the over-report caveat on the row itself.

### Measured wins

- **`dbcore.schema_choices` opened a fresh connection per call.** `db.py` builds 23 of
  them at import, so **every invocation paid ~56 ms** before doing anything — 35% of
  `db.py --help`. Memoized per resolved path (so `GUIDEBOOK_DB_PATH` still works):
  **0.185s → 0.129s**, measured. At 60–136 invocations per research session that is
  3.4–7.7 seconds each.
- **The floor/ceiling band is deleted.** Measured: **zero rows print a range** — the only
  SCRAPED payload is the superseded one the selection drops, and the corrected READ
  transcription carries no `inferred` key. The band existed to bound damage the document
  never had; `page_image.py` removed its reason to exist. The three-way provenance label
  stays, with the caption now telling a reader to re-transcribe a SCRAPED list rather than
  trust its yield. Its ceiling also had a real bug (it could fall *below* its floor) — the
  review pass had fixed the bug inside apparatus that should not exist.
- **B01–B05 now read `check_expression`.** Five hand-curated tuples, ~50 lines, retired;
  the per-column prose moved into the migration headers where a vocabulary decision
  belongs.

### Shared homes

- **`_CORRECTABLE` is derived from `retrieval_log.PAYLOAD_FIELDS`** plus `pub_title`, whose
  exception is now stated. Its header declared the invariant *"EXACTLY what
  --verify-authors can prove"*; two hand-maintained tables held together by a comment is
  rule 5 in Python inside the module that enforces rule 5 in the data.
- **One `_append_derived()`** behind `derive()` and `record_file()`. `fetch()` keeps its
  own, deliberately: it carries HTTP facts (`exit`, `status`) no derivation has.
- **`page_image` uses `retrieval_log.LOG_ROOT` and `_session_stem`.** It had computed its
  own absolute path while `retrieval_log` resolves a relative, env-overridable one — from
  `/tmp` the image landed in one tree and its attestation in another. `--session foo.md`
  likewise split them; CLAUDE.md §7 names that trap.
- **`named_in` collapsed** to one tokenisation intersected with the live table list,
  verified equivalent across all 20 views.

### And the audit caught me mid-fix

Migration 091 gave `verification_status` a CHECK, and **`derived_not_curated_audit` went
red in the same run** on `db.py`'s hand-written `choices=["VERIFIED","UNVERIFIED"]` — a
literal that was fine while the column declared nothing and became a second home the
instant it did not. That is the mechanism proving itself, and it is the strongest evidence
in this section that moving vocabularies into the schema was the right altitude.

**Gates:** `research_batch_dod` 19/19, `test_db_integrity` 75/75, `run_checks
--changed-from origin/main` PASS, `--selftest` PASS, `migrate_db --rebuild` reproduces,
`derived_not_curated_audit` CLEAN.

### Skipped, with reasons

- **Deriving amendability** (above) — GAP-013, too large to land safely here.
- **Moving `spanned()` out of the renderer** into a shared home its three named consumers
  (L1.8/L2.6/L3.5) can read. Correct, and `stage-map.yaml`'s "STILL OWED: a `pointer:`
  list" should then close as *unnecessary* rather than be curated. Deferred as its own
  change.
- **Replacing `schema_walkability_fresh` with a check over `sqlite_master`.** The
  objection is sharp — delete a cross-stage view, regenerate, and the freshness check is
  green with the pointer gone — but designing that check is not a cleanup.
- **`ensure-deps.sh` probing five deps in five interpreters** (~0.21 s per session start).
  It is a hook, and the current shape catches the broken-import case its header documents.
- **Emitting FK edges once instead of twice** in the page (18.6 KB, 15% of the payload).
  Real, and not worth a JS index at this size.
