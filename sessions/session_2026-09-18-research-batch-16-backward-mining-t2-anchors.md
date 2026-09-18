# Research batch 16 — the deferred backward passes, and the first anchoring-tier maximum

**Session:** `session_2026-09-18-research-batch-16-backward-mining-t2-anchors`
**Slug:** `accessible-circulation-geometry` · **Parameter:** 3 (`ramp gradient`, TERM-001) × MOB
**Branch:** `claude/batch-protocol-validation-tlkypw`
**Priors committed before the first query:** `589577b`, `scratchpad/<session>/priors.md`

Derive every figure below from the live repo; the commands are named beside each claim.

---

## 1. What this batch was

R2's depth-1 backward pass over the three anchors batch 15 deferred **by name** in the mining
register, plus R1's mandatory Co-1 pass. The driving gap is **GAP-002**: the determination's
threshold half rests entirely on the T4–T6 regulatory stratum and no anchoring-tier source states
a maximum acceptable gradient.

It is a mining batch rather than a search batch because the search space was already well covered
— 37 logged searches on this slug across batches 08–15 — and because three named, pre-screened
reference lists sat unmined.

## 2. The headline

**Vredenburgh, Hedge, Zackowitz and Weiner 2009** (REF-01002, T1 clinical / high_control),
*Evaluation of Wheelchair Users' Perceived Sidewalk and Ramp Slope: Effort and Accessibility*,
Journal of Architectural and Planning Research 26(2):145–158:

> *"Results suggest that for a transit distance of up to 20 feet, a ramp should not exceed a
> maximum cross slope of 5% or a maximum running slope of 7%."*

That is **the first anchoring-tier stated maximum this parameter has had**, and it is derived from
wheelchair users' own Borg-scale perceived effort rather than from a committee. It is the object
GAP-002 names as missing.

**Three things about it matter more than the number.**

**It was invisible to every DOI-keyed pass.** The paper carries no DOI. It sat inside REF-00977's
reference list — an anchor batch 15 deferred — and was reachable only by resolving a title. Two of
the batch's other best candidates (102, 103) are also DOI-less in their deposits. Six batches of
DOI-keyed searching could not have met any of the three.

**It loosens rather than tightens.** 7 % is above the 5 % specification 8 determines, and the
parameter direction is `lower_is_better`. So the standing determination is **safe but
mis-warranted**: nothing here makes 5 % wrong, it makes the *account of why* 5 % an account of the
wrong evidence. Stating the direction plainly because the intuitive reading of "we found the
missing threshold" is that it confirms.

**It is held at skim grade, and the cell is now UNDETERMINED.** The TRID/TRB record and its
verbatim abstract were retrieved and persisted (HTTP 200, 50,825 bytes); **the article was not.**
Batch 15 declined to claim Co-1 for REF-01001 on an ambiguous abstract and the full text proved
that claim would have been false. Moving a determination onto an abstract in a bibliographic index
is the same shape one column along. **Determination gate 1** (`UNLINKED`, trigger REF-01002, tier
read from the source) binds the cell; **GAP-016** is the read that resolves it. What happened next —
specification 8 retired in place, the engine unable to recompute — is §5a, and it is the most
consequential thing in this batch.

## 3. The other two admissions

**REF-00980 — Sanford, Story & Jones 1997**, *An Analysis of the Effects of Ramp Slope on People
with Mobility Impairments*, Assistive Technology 9(1):22–33. 171 subjects, a 30-foot ramp from 1:8
to 1:20, pulse rate / energy expenditure / rate of travel / distance / rest stops. Its conclusion:
*"changes to the technical requirements for ramp slope and length cannot be recommended at this
time."* Extracted `claim_type=absent`, `figure_role=finding`, with a `confirms` edge — **the
corpus's first `confirms` against a code**, where batch 15 produced its first two `insufficient`.
The dangerous misread is named on the row: the companion finding that few had difficulty even at
1:8 *looks* like a warrant for relaxing to 1:8 and the authors explicitly declined to draw it.

**REF-00979 — Chow et al. 2009**, *Kinematic and Electromyographic Analysis of Wheelchair
Propulsion on Ramps of Different Slopes for Young Men With Paraplegia*, Arch Phys Med Rehabil
90(2):271–278. *"Major adjustments in stroking kinematics and significant increases in muscle
activity occurred at slopes between 4 degrees and 10 degrees."* This is the input the proxy
inference has lacked: GAP-002's two curves are monotonic and resolve degenerately to 0°, whereas
this reports a **band with a lower edge**. 4° ≈ 7.0 % — conversion for comparison only, per the
2026-09-17 ruling; the source wrote degrees and degrees is stored.

**The convergence is the finding, and it belongs to synthesis rather than to any row.** Two
independent laboratories, different methods (perceived effort; EMG and kinematics), land within a
rounding of each other at ~7 %. Neither was designed to test the other. It is recorded here and
deliberately not composed into a value while REF-01002 sits at skim grade.

## 4. Both rankings of the three anchors were inverted, and mine were too

| Anchor | Batch 15 ranked | My prior | Screen result |
|---|---|---|---|
| REF-00984 *Wheelchair skills tests* | **highest-value** | test-apparatus numbers, needing a guard | **0 of 38** |
| REF-00977 *Disabled-by-design* | deferred on a 403 | 0–2 relevant | 6 of 117, incl. REF-01002 |
| REF-00985 *Fuzzy-logic MSD risk* | **lowest expected** | **0** | **23 of 46**, both other admissions |

Three wrong predictions, all pre-registered, all recorded. The regularity was derivable in advance
and neither session derived it: **a paper cites the literature of its own independent variable.**
REF-00985 measures propulsion effort, so it cites propulsion-on-slopes work; REF-00984 reviews
measurement *instruments*, so it cites reliability and construct validity. Topical proximity of the
anchor to the slug predicted nothing. **GAP-018** sets this out as a hypothesis to be tested
prospectively over the next three or four passes — two observations are not doctrine, and the
deferral note for REF-00979 already carries its prediction so the next pass is a real test.

**A second correction that generalises:** batch 15 deferred REF-00977 because Taylor & Francis
returned 403 and the repository copy refused. That is *full-text* inaccessibility, and backward
mining never needed the full text — the Crossref-deposited reference list is the object, and it is
free. This applies to every paywalled anchor the corpus will meet.

## 5a. The determination surface is now empty, and that is this batch's largest effect

`test_db_integrity` **K02** (blocking) requires a **live** determination to account for every
extraction of its parameter; its scope is `retired_at IS NULL` and its own comment explains why —
a retired determination is history, a live one that omits new evidence *"attests a subset of the
evidence while reading as the whole of it"*, and `derivation_sha` hashes that subset. This batch
added extractions 44–48. Spec 8 held 1–43. K02 went red.

**Re-determination was attempted on a throwaway copy and the engine crashed.**
`assess_cell` reaches `state=provisional` on the *anchored* branch with `confidence=None`, and its
own pydantic gate then refuses it — *"State 'provisional' requires confidence_flag"* — as an
uncaught traceback at `assess_cell.py:1923`, writing nothing. The **proxy** branch builds a
`ProvisionalConfidenceFlag` (specs 4–8 all carry populated dimensions); the anchored branch does
not, and nothing notices that `provisional` is reachable down both. It was unreachable until now
because no anchoring-tier *claim* had ever existed for a determined parameter. **GAP-019.**

**What it would have written is its own argument against forcing it.** Instrumented:
`value_max 7.0 %`, `tier_basis T1`, `rests_on_proxy_inference 0`, `governing` and `supporting` both
`None`. **A single T1 claim displaces the entire regulatory stratum rather than composing with it.**
So the determination would have moved 5 % → 7 % and shed its proxy marker on one skim extraction
read from a third-party index abstract whose article has not been obtained.

So **specification 8 was retired in place** (owner ruling 2026-09-16) with that reasoning recorded
on the row. It stays readable as history at 5 % / 1:20 with its notations intact. **The cell is
undetermined, and that is the true state**: the corpus holds evidence it cannot yet turn into a
determination.

**And the green run now says less than it did.** `test_db_integrity` reports 74/74 — with **K01,
K02 _and C10_ in its own "PASSED HAVING EXAMINED NOTHING" list, which grew from 19 to 22.** That is
CLAUDE.md §5(a) verbatim, the failure this repository has produced four times. **C10 was missing
from this sentence until a code review caught it**, and it is the one of the three that most
deserved naming: *"no published cell rests on an unverified or disputed source"* examined 1 subject
before this batch and 0 after — so the check that would have objected to a determination resting on
REF-01002, the unverified source this batch admitted, is the check the batch silenced. Measured:
`git show 589577b:data/guidebook.db > /tmp/pre.db && python3 scripts/tests/test_db_integrity.py
--db /tmp/pre.db`. An account of a coverage loss that omits one of the three losses is itself the
§5(a) shape at one remove. Comparing 74/74
today against 74/74 before this batch would be a false equivalence: the denominator of examined
checks fell. **GAP-020** records it. This is also the *second* time in three batches the
determination surface emptied — batch 15's review caught spec 7 retired and never re-determined and
fixed it by determining spec 8; that remedy is unavailable here.

## 5. A write-path defect found by using it, and repaired

`db.py log-mining` could not express **a mining pass that ran and found nothing**, and never
cleared a deferral it discharged. Measured live this session:

- It refused an empty connections list unless `--deferred-reason` was given — but R6 says
  `deferred_reason` means DELIBERATELY NOT SEARCHED, so the only expressible record of
  REF-00984's executed zero-yield pass was a false one.
- `citation_mining.notes` existed with **no writer at all**, which is why every substantive mining
  note in this table before today sits in `deferred_reason`.
- It set `backward=1`, `status='mined'` and a connections list on a row while leaving
  `deferred_reason` intact. Observed on REF-00977, whose row simultaneously read *mined, produced
  REF-01002* and *BACKWARD PASS DEFERRED*. **That is the RAP-F61/F69/F70 shape the citation-miner
  skill already records**: a register saying a finished pass is owed is how a session re-queues
  finished work.

Fixed forward: `--notes` added; `--notes` and `--deferred-reason` made mutually exclusive; a pass
that runs now discharges a standing deferral and **carries its text into `notes`** rather than
destroying it (2026-09-16 retire-in-place). **GAP-017** records what is still owed — no registered
check asserts the invariant, so the state found here can recur silently.

## 5b. Mining coverage, asked mid-batch, and an owner ruling

Asked directly whether every source recorded in a table has been citation-mined. Derived: **no.**
`log_mining` sets `backward=1`/`forward=1` **unconditionally**, deferral included, so every one of
the deferred rows carries a flag asserting its direction was mined — and
`citation_mining_completeness` counts **row presence**, reporting `10/10 T1-2 sources mined, 100.0%`
while backward had actually been executed on **3 of 13** sources on this slug.

**Owner ruling, same day** (`references/project-standards.md`, recorded on contact per rule 0):
*"executed is 'mined'"* and *"deferred is okay so long as it runs eventually"*. This **narrows** the
defect and **refuses** the remedy this session first proposed:

- The execution signal **already exists** — `evidence_sources.citation_mining_status`. Splitting the
  direction columns into attempted/executed would be a second home for one fact, which is rule 5.
- **A deferral is not a defect.** Depth-1 forbids mining an anchor admitted in the same pass, so all
  three of this batch's new deferrals are correct behaviour.
- What survives: `citation_mining_completeness` reads the wrong column and overstates.
- What the ruling newly opens: *"runs eventually"* is an obligation with **no mechanism** — no
  ageing, no backlog count, no check that fails on an undischarged deferral. The register holds
  batch 08's deferrals beside batch 16's and cannot tell them apart by age.

**GAP-021** carries the measurement, **GAP-022** the corrected framing under the ruling. Live
status, derived not quoted: `mined 3 · deferred 10 · pending 10` of 23 sources — the ten `pending`
are the T4–T6 regulatory stratum, which has never been mined at all.

## 6. Three refusals that caught real errors

- `add-extraction` refused `claim_type=qualitative` for Sanford and **named the correct grade**:
  a source asserting no value is `absent`, a recorded absence, which is evidence. My grade was
  wrong and the CLI's was right.
- It refused `--stated named` against the label *"the technical requirements … under the ADA
  accessibility guidelines"*, because the conclusion sentence does not contain that phrase — the
  ADA framing is in the study's opening sentence, not the one making the claim. The edge was
  narrowed to what the source actually says.
- It refused `condition_on` against prose: *you cannot be conditioned by a figure that does not
  exist as a row*. The 20-foot transit distance became extraction 44 and the 7 % hangs off it as
  an edge. This project has already been bitten by a determination that dropped its qualifier.

## 7. What this batch did NOT do

**It did not close GAP-002 and it did not move the figure — it removed the figure.** Specification 8
is retired at 5 % / 1:20 and readable as history; nothing in the book now states a ramp gradient.
The threshold source exists, is anchoring-tier, and is unread beyond its abstract.

**It ran no Co-1 pass that yielded anything**, and R1 passed on two well-formed zero-yields (HR via
HUPT's own publications index, which was fetched rather than inferred; SV via DHR). A 1:12 / 8.3 %
figure appeared in a search-engine summary with no retrieved document behind it and is recorded
nowhere — that is the §5(c) shape exactly.

**It mined three anchors and deferred three more**, because depth-1 is a hard constraint and all
three admissions are hop-2 from this batch's own passes. REF-01002 should lead the next pass, and
its obstacle is named: no DOI, so no deposit, so GAP-016 must obtain the article first.

**It left seven deferrals on this slug untouched** — deliberately; those passes genuinely have not
run, and rewriting them would destroy the record of what was owed.

## 8. Gate state

```
python3 scripts/audit/research_batch_dod.py --session session_2026-09-18-research-batch-16-backward-mining-t2-anchors
python3 scripts/audit/citation_mining_completeness.py --session session_2026-09-18-research-batch-16-backward-mining-t2-anchors.md
python3 scripts/run_checks.py --changed-from origin/main --explain
```

## 9. Owed, in priority order

1. **GAP-016 (P1)** — read Vredenburgh et al. in full. Decides whether parameter 3 stops being a
   proxy. Four things the abstract does not answer are named on the gap.
1b. **GAP-019 (P1)** — the engine cannot emit an anchored `provisional` cell, and behind that, a
   single T1 claim displacing the regulatory stratum. Needs a ruling, not a defect fix; **GAP-020**
   (P1) is the empty determination surface that follows from it.
1c. **GAP-022 (P1)** — make `citation_mining_completeness` read status rather than presence, and
   build the missing measure for "runs eventually", landing both together.
2. **REF-01002's backward set** — the thinnest, most directly relevant seam, per its own framing
   that design recommendations rest on *"limited empirical research"*. Blocked with GAP-016.
3. **Candidate 96 (Gagnon 2014)** — JRRD, open access, a slope series. If it reports an inflection
   rather than a monotone rise it corroborates REF-00979's band from a third laboratory.
4. **GAP-018** — test the "cites its own independent variable" predictor prospectively before it
   becomes doctrine.
5. **GAP-017** — nothing gates the mined-and-deferred contradiction; the sweep for other writers
   carrying a `deferred_reason` column has not run.
6. Inherited and untouched: **GAP-008** (`source_locators` writer), **GAP-009** (cross-slug
   backlog for batches 01–14), **GAP-011**, **GAP-012**, **GAP-015**.
