# Batch 19 — the pre-1990 chain: Steinfeld's bibliography, Walter, Templer

**Assignment:** batch 18 §9 items 1–4, in that order. GAP-025 established that a deferral runs
because a batch is told to run it, not because a counter goes red; this is that batch.

**Priors:** `scratchpad/<session>/priors.md`, committed **before** the bibliography was transcribed
or any screen run. P6 (Co-1) was appended later and says so in its own text.

**Derive every figure below.** Nothing here is a count to quote.

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
