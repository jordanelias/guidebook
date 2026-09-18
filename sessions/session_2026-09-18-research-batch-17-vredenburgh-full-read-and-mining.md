# Research batch 17 — the read that did not happen, and two passes that did

**Session:** `session_2026-09-18-research-batch-17-vredenburgh-full-read-and-mining`
**Slug:** `accessible-circulation-geometry` · **Parameter:** 3 (`ramp gradient`, TERM-001) × MOB
**Priors committed before the first query:** `36d7de2`, `scratchpad/<session>/priors.md`
**Assignment:** GAP-025, the batch-17 mining order set when the owner closed GAP-022.

Derive every figure below; the commands sit beside each claim in the search log and the gaps.

---

## 1. The headline is a null, and it is the honest one

**GAP-016 is not closed. REF-01002's full text could not be obtained by any route available
to this environment**, measured across seven and every attempt persisted as an artefact:
academia.edu `403` on two different copies, ResearchGate `403`, JSTOR `200` whose body is a
bot interstitial, SafetyLit `503` then empty, OpenAlex `429` with the environment's budget
exhausted.

**The informative one is Crossref.** A bibliographic title search returns five neighbouring
papers and not this one — which **verifies rather than assumes** the no-DOI fact the whole
problem rests on. JAPR never deposited it. Consensus returned the record and the same
abstract, corroborating existence at index level, not full text.

My prior put retrieval "below even odds" and said a failure "is not licence to promote the
extraction". It isn't. **Extraction 45 stays skim/preliminary, REF-01002 stays `UNVERIFIED`,
determination gate 1 stays open, C10 keeps refusing the re-determination, and parameter 3 ×
MOB stays undetermined.** Nothing about the 7 % figure moved. (**GAP-026**.)

What would actually work is **not a search**: a library or document-delivery route — JSTOR
institutional access, ILL, or a request to the corresponding author, whose consultancy
publishes its own papers. The next batch should plan that as a different kind of work rather
than re-run the same seven routes and record a second null.

## 2. The GAP-018 predictor is FALSIFIED — and the result I first reported as its success was a screen artefact

**This section replaces what it first said.** The first half of this batch reported REF-00979
returning **19 of 30** against a pre-registered floor of ≥ 8, and called it the predictor's
first passed prospective test. That went into a commit message (`857050c`), this record, and a
PR body. **It was wrong, and the second half of the batch is what proved it.**

Two further predictions were pre-registered as the sharper test — two wheelchair biomechanics
papers on the same slug, differing only in independent variable:

| Anchor | Its independent variable | Predicted | Loose screen | **Strict screen** |
|---|---|---|---|---|
| REF-00983 | **is** ramp slope | **≥ 8** | **2/23** ✗ | 1/23 |
| REF-00986 | activity type, not slope | **≤ 4** | **9/45** ✗ | 0/45 |

**Both failed, in opposite directions.** That is the hypothesis being wrong, not noise.
REF-00983's references are the *transit-vehicle* literature — because a reference list follows
the paper's **field and problem framing**, not its independent variable.

**Then I tested the screen, and it is confounded.** The regex carries `propuls` and `accessib`,
so **any** wheelchair-propulsion paper matches whether or not it concerns slope. Under a strict
slope-only screen (`ramp|slope|incline|gradient|grade|cross-slope`):

- REF-00986: **9 → 0** of 45
- **REF-00979: 19 → 2 of 30** — the headline "success" was counting *"cites
  wheelchair-propulsion papers"*, trivially true of a wheelchair-propulsion paper.
- REF-00980: 5 → **4** of 25 — the anchor I predicted *low* survives best, because its hits are
  genuinely ramp-titled. **The strict screen inverts the original ranking.**

**GAP-029** carries the retraction. GAP-018 and GAP-027 are superseded by it and must not be
cited as support. Every mining yield this project has recorded used the loose screen and is an
**overcount of slope relevance** — re-derive before quoting any. The commit message at `857050c`
states the false version and cannot be edited; this record is the correction.

## 2a. Two admissions, and a second anchoring-tier value pointing the other way

**REF-01003 — Longmuir, Freeland, Fitzgerald, Yamada & Axelson 2003** (T3, *Environment and
Behavior* 35(3):376–399). A second perceived-difficulty study; paths meeting the proposed
guidelines rated easy-to-moderate — a `confirms` edge, no value stated. **Graded PROXY for
MOB**, because its 23 participants *walked* at preferred pace: ambulatory, not wheelchair users.
The priors predicted that grade before retrieval, and the authors themselves call for work
examining "different perceptions between ambulatory individuals and wheelchair users".

**REF-01004 — Kim, Lee, Lee, Kwon & Chung 2010** (T1, HFES Proceedings 54(9):698–702). Five
slopes (1:6 … 1:14) × **three rise heights** (15/30/45 cm) — the rise-conditioned design this
corpus has never had. It states **1:8 is recommendable when rise is low and space insufficient**.

**That is a second anchoring-tier stated value, and it points the opposite way from REF-01002's
7 %.** They reconcile through their conditions rather than contradicting: **REF-01002 conditions
on distance, REF-01004 conditions on rise, and REF-00996 gives rise-conditioning as the
mechanism.** Three sources, three methods, one conditioning structure — and REF-01004 is the
first to *measure* the rise half rather than state it. The over-read to guard against is quoting
1:8 as a permissive maximum: the same abstract reports **no significant difference between 1:10
and 1:12**, so the paper is not arguing for steeper ramps generally.

## 2b. Rouvier 2022 was retrieved, verified, and could not be admitted

PLOS ONE, open access, 76 references deposited, full byline confirmed via Crossref.
`add-source` **refused it under R9**: the DOI is filed in `source_locators` as REF-00037, and R9
says cross-file rather than duplicate.

**REF-00037 is corrupt in a way that makes that instruction destructive.** Its `doi` holds the
PLOS ONE identifier while its `title` reads *"Inclusive Housing Design Guide. RIBA/Habinteg/CAE.
DOI:10.4324/9781003564164"*, authors Runnalls & Walker, year 2024 — a different work, with a
different DOI inside the title text. A second row, REF-VERIFIED-003, holds the same DOI with
title, authors and year all NULL.

So **R9 applied to a corrupt stash directs an admission onto a mismatched identifier.** That is
the shape the 2026-09-16 retire-in-place ruling records from batch 08 — thirteen RETIRED
tombstones read as live DOI claims — one row-state along, and unfixed. `update-locator` writes
`status` only, and none of `REFERENCE-ONLY|PROMOTED|SCREENED-OUT|RETIRED` honestly says *this
row's DOI does not belong to its title*. Hand SQL was not used. **GAP-030.**

## 3. The finding I did not go looking for

REF-00980's backward pass returned five relevant references. **Every one is pre-1997 and not
one carries a DOI**: a 1957 *study to determine the specifications of wheelchair ramps*; a
1971 architectural movement study whose **Part 3 is titled *Ramp gradients***; a 1979
accessible-buildings study; a 1981 Dutch paper on accessibility by means of ramps; a 1993
review of technical requirements written as an RFP attachment.

**This is a systematic property, not bad luck**, and it now has three demonstrations: REF-01002
(2009, no DOI, invisible to six batches), batch 16's candidates 102 and 103, and this entire
layer. Every search method this project runs is DOI- or index-keyed, so **the foundation
layer of its central parameter is structurally out of reach.**

Why it matters: REF-01002's abstract asserts design recommendations "are based on limited
empirical research". That is a **checkable claim about a named set**, and this batch has now
named it. If the 1971 *Ramp gradients* study is the measurement behind 1:12, the codes are
anchored; if it is not, they may never have been — and under the 2026-09-13 ruling a finding
that a code is insufficient is first-class evidence. **Either answer is a result.**
(**GAP-028**.)

## 4. R1: a third consecutive Co-1 zero, now a pattern worth stating

Every result was a restatement of ADA 1:12 or UK 1:15/1:20 by a ramp vendor, a compliance
consultancy or a government body. **Not one was a DPO speaking in its own voice** — after HR
(HUPT's own publications index) and SV (DHR) in batch 16.

Three well-formed zeros support a claim worth testing rather than repeating: **DPOs on this
parameter publish advocacy and barrier testimony, not technical thresholds.** That is a claim
about where Co-1 evidence for a *numeric* parameter lives, and it should be tested against a
parameter where lived experience is more directly dispositive before it is generalised.

## 5. Corrections a code review forced, and what they say about the batch

**Sections 5–8 of this record were written for the first half and contradicted the database in
five places until a code review caught them.** They said the batch admitted nothing, staged
seven candidates, left 107/108 unadmitted, and owed a floor that §2 records as already tested.
All false after the continuation. Rewritten here rather than patched line by line.

**Provenance was broken on both admissions, in two ways.**
- Neither had a `search_admissions` edge, and every search row read `results_admitted = 0` —
  so no path existed from either source back to the search that admitted it. `db.py:646` calls
  that edge *"the only carrier of it"*. The gate passed COMPLIANT over it.
- Candidates 107/108 hung off **exec 71 — the Co-1 search whose own note reads ZERO YIELD**.
  The batch's two best sources were attributed to a search reporting it found nothing.

**Root cause: the Consensus search that actually surfaced them was never logged.** It ran during
the REF-01002 retrieval hunt and I did not treat a locator hunt as a screening search. Backfilled
as **exec 77**, marked `backfill=1`, with the prior recorded as *absent* rather than reconstructed
— DR-2026-05-09 forbids writing one after seeing results.

**A check was silently excusing exactly this.** `research_protocol_audit` CHECK 7 split its legacy
exemption on `(r[2] or "") < "2026-09-03"`, and `r[2]` is `''` both for a pre-cutoff row **and for
a row with no admitting search at all**. So every future source with a missing edge was exempted
forever, by the check built to catch it — CLAUDE.md §5(a) inside its own remedy. Fixed to a
three-way split; it now surfaces **REF-00987**, a pre-existing case it had been masking.

**Also corrected:** candidates 107/108 left `PENDING-VERIFICATION` after admission (and §8 then
listed them as owed work, so the next batch would have re-retrieved two sources it holds);
`citation_mining` notes citing exec 77/78 when the executions were 75/76 — and exec 77 now
*exists*, so a stale pointer resolves to an unrelated row rather than to nothing; `volume` and
`issue` NULL on both admissions while sitting in the persisted payloads.

**And one correction I got wrong on the first attempt.** Closing GAP-018/027 as
`CLOSED-SUPERSEDED` — accurate, accepted by the writer and by the column's own CHECK — turned
**B06 red at 73/74**, because B06 enumerates a narrower curated list. Resolved with
`CLOSED-DECIDED` rather than by widening the check: adding a value to a check to accommodate one
I had just invented is the shape of disabling a test to get green. **GAP-032** records that B06
is a curated vocabulary beside a column that declares its own — rule 8, in a test file.

## 6. Gaps opened and closed

**Opened:** GAP-026 (retrieval null), GAP-028 (the pre-1990 no-DOI layer), **GAP-029** (the
predictor falsified), GAP-030 (GAP-008 blocks Rouvier), GAP-031 (three fields with no repair
path), GAP-032 (B06's curated list).
**Closed:** GAP-018 and GAP-027, both `CLOSED-DECIDED`, superseded by GAP-029.

**GAP-031 distinguishes design from damage**, because the review conflated them: `journal_name`
is NULL on all 25 rows with no writer (real gap); `evidence_population_match` has no amend verb,
so a `--sample-size` I simply failed to pass is now unrepairable except by a second row that
would read as a dissenting grade (real gap); **`author_count` NULL on all 25 is correct** —
migration 063 writer-retired it, and authorship lives in `evidence_source_authors`.

## 7. What this batch did not do

**It still moved no determination.** REF-01004 is T1 and states a value, but the cell stays
undetermined because C10 blocks on REF-01002, unread. **Five consecutive batches on one
parameter.**

It reached **9 searches and 2 admissions** — still under §12.2's minimum viable of 10–12 and
3–4, after a first half that ran 4 and 0 and was closed as complete.

It did not re-derive any earlier mining yield under the strict screen, which GAP-029 says is
owed for every figure in the register.

It did not resolve REF-01002's fourth-author discrepancy (TRID *Weiner* vs a summary's *Welner*),
and the stored row carries an unconfirmed name.

**And GAP-026 overstated one of its seven routes.** It records "SafetyLit 503"; the persisted
artefact is `status: null, exit: 35, bytes: 0` — a connect failure, not an HTTP 503 with a body.
One of the seven routes evidencing a P1 null is evidenced by an empty file.

## 8. Owed

1. **GAP-016 / GAP-028 (P1)** — a library or archive route, not another retrieval ladder.
2. **GAP-029 (P1)** — re-derive every recorded mining yield under the strict screen.
3. **GAP-030 (P1)** — a `correct-locator` verb; GAP-008 has now blocked a verified open-access
   admission twice.
4. **GAP-025's remaining six deferrals**; REF-01003/REF-01004 backward, with the **strict**
   screen.
