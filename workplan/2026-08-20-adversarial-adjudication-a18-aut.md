# Adversarial adjudication — A-18 × AUT, and why the determination was not written

**Date:** 2026-08-20. **Session:** `session_2026-08-20-provenance-walk`.
**Form:** DR-2026-08-19 §7 — agonist / antagonist, blind-then-compare, lenses L1–L8, no third judge.
**Adjudicator:** Opus 5. **Outcome: the determination is NOT authored. Phase 1 is halted.**

The agonist retrieved and filed the affirmative case as artefacts. The antagonist re-derived
everything independently, without reading the agonist's output or the retrieval log, and attacked
the proposed cell. Both reports are in the session scratchpad. This document is the adjudication:
what was sustained, what was refused, and what I could not verify either way.

---

## 1. The finding that stops the phase

**The proposed determination's core claim — "no numeric value is authorable for A-18 × AUT" — is
refuted.** Not by doubt; by named, on-parameter, population-justified publications that the batch's
nine searches did not reach.

| Source | Status | What it is |
|---|---|---|
| Greenland, Harvie-Clark, James & Shield 2026, *Applied Acoustics* 242:111055, `10.1016/j.apacoust.2025.111055` | **EXISTENCE VERIFIED** by me via Crossref; **CLAIMS UNVERIFIED** | "Universal acoustic design for schools: An evidence based approach". Same journal and window as REF-00965. Bridget Shield is a principal classroom-acoustics researcher. |
| Bettarello, Caniato, Scavuzzo & Gasparella 2021, *Applied Sciences* 11(9):3942, `10.3390/app11093942` | **HELD IN THIS PROJECT ALREADY** | "Indoor Acoustic Requirements for Autism-Friendly Spaces". Sitting in `source_locators` as **REF-00561**, `recovered_from='corpus-pre-reset-2026-08-06'`, `doi_resolution_outcome='RESOLVED'`. |
| Mealings, Wilson & Buchholz 2025, `10.1080/08856257.2025.2577923` | reported by antagonist, **not independently verified by me** | Scoping review, autistic children × classroom environment. |
| Rosas-Pérez et al. 2023, `10.1121/2.0001741` | in REF-00965's own reference list, **unadmitted** | Same team, same cohort as REF-00965, but set in *schools and universities* — i.e. more on-item for A-18 than REF-00965 itself. |

**The second witness for OD-5.** REF-00561 is the autism-specific acoustic-requirements paper, and
it has been in this repository since the 2026-08-06 corpus recovery. The R9 duplicate gate queries
`evidence_sources` only and is blind to all 835 `source_locators` rows, so the batch could not see
that it already owned the most on-topic source for the population it was studying. This is the
**same failure already logged at exec 5 for Iglehart 2016 / REF-00578**, occurring a second time,
now landing directly on AUT. OD-5 previously had one witness. It has two.

**What I verified and what I did not.** I fetched Crossref for Greenland 2026 and confirmed title,
journal, volume 242, article 111055, 2026, and the four authors. **The paper is closed access with
no abstract in either Crossref or OpenAlex.** The antagonist's specific figures — a mid-frequency
reverberation criterion of 0.5 s, ambient noise ≤ 35 dB(A), and ASD as the second most prevalent
SHCN group — **could not be verified from any payload held.** They are recorded here as
`[UNVERIFIED-QUANT]` leads and must not be written as fact anywhere. That an antagonist asserted
them is not evidence; this project's signature failure is exactly the promotion of a plausible
assertion into a stored fact.

---

## 2. Why the batch could not have found these

Nine searches ran on a slug whose flagship item is *"RT60 in Occupied Learning and Listening
Spaces"*. **Not one query paired a reverberation term with a learning-space term and a
neurodivergent or SEN population.** Exec 1 — the only AUT-targeted query on the slug — reached for
*autistic adults in buildings*, and contains no "classroom", "school", "learning" or "reverberation
time" criterion.

That is a query-shape failure (R14) at the **batch-frame** level rather than at the level of any
individual query, and no row in `search_executions` can express it. The individual searches were,
by the antagonist's reading and mine, unusually honest — two self-retractions, a correctly
diagnosed engine cap, a genuine-absence call I accept. The frame was wrong, not the craft.

---

## 3. Lens verdicts

| Lens | Verdict | Substance |
|---|---|---|
| **L1 Existence** | SUSTAINED | All five DOIs resolve; corroborated across ≥2 APIs each. Nothing invented. |
| **L2 Fidelity** | SUSTAINED, one defect | Stored claims match abstracts verbatim where checkable. **Defect:** REF-00965 has *four* themes; the DB records three, dropping "Positive impact of music and natural environments" — the theme that most closely converges with REF-00968's "Restoration is Not Silence". Dropping it makes the sources look *less* convergent on the point that most damages a level-reduction reading. |
| **L3 Independence** | **NOT SUSTAINED** | Chain of one, both links confirmed from reference lists: REF-00966 ← REF-00965 ← REF-00968, no closing edge. Three teams, three disjoint samples, three methods — so this is *framing* dependence, not sampling dependence, and their agreement cannot count as three votes. |
| **L4 Tier** | **NOT SUSTAINED** | Two over-grades, both inflating. See §4. |
| **L5 Population** | PARTIALLY SUSTAINED | REF-00607 correctly PROXY; REF-00968 correctly PARTIAL (reached blind on the same three grounds as MB1-012's downgrade). **But** `evidence_population_match` grades population only — so REF-00965 (daily life) and REF-00966 (shops, transport, healthcare) enter a *learning-space* item through EXACT rows with nothing recording the setting objection. |
| **L6 Contrary** | **NOT SUSTAINED** | §1. The value exists; the batch never looked where it lives. |
| **L7 Recognition** | PARTIALLY SUSTAINED | Credit is repaired (see §5). Recognition is not: a cell emitting no value and no requirement renders autistic testimony as a blank, on an item named for autistic people's most-cited environmental barrier. |
| **L8 Query-shape** | PARTIALLY SUSTAINED | Per-query practice is good; the batch frame failed (§2). |

---

## 4. Tier over-grading — referred, not corrected

The antagonist grades **REF-00965 and REF-00968 as T3, not Co-1**: both are researcher-led
qualitative studies *about* autistic people, with no co-production, participatory or DPO warrant
visible in the retrieved record. CLAUDE.md §6 is explicit — *"Co-1's warrant is co-production."*
Only **REF-00966** states participatory method and carries autistic community co-authors.

**Corroborating structural evidence, verified by me:** `co1_source_type` and `co1_provenance` are
**NULL on all three** Co-1-tiered rows. The schema has fields expressly for the Co-1 warrant and
not one is populated. The tier is asserted; the warrant is empty. That is §2(c) of CLAUDE.md one
level up — a gate that asks whether the tier *field* is populated, never whether the tier is
*earned*.

If sustained, `tier_basis='Co-1'` rests on **one** source, not three.

**Not corrected here.** Evidence-tier definitions are the DG-NON class and are owner-gated. A
re-grade also needs the full texts of REF-00965 and REF-00968, which this environment cannot
reach. **Referred to the owner** with the recommendation that it be resolved before any cell on
this slug is written.

Separately: **REF-00967 is tiered T1** on an n=27 single-centre observational EEG study whose own
DB note concedes it "contains no RT60, NRC, STC or NC value". T3 is the defensible grade. Also
referred.

---

## 5. "andsensory, Emily" is correct — do not fix it

The third author of REF-00966 is an autistic self-advocate who publishes under her handle
**@21andsensory**. Crossref, OpenAlex, Europe PMC and the publisher all render the byline as
"Emily andsensory". **The stored value is right.** The 2026-08-19 deletion of the autistic
community co-authors is repaired: Catherine Woolley sits at position 2 and Emily at position 3, on
a paper whose entire Co-1 warrant is their co-authorship.

**Two live risks.** `evidence_source_authors.corporate_name_note` is NULL, so nothing in the
database explains why that surname looks malformed — the next agent to "tidy" it will delete her
again, exactly as happened before. And any rendered credit reading "andsensory E" is a
*presentational* erasure of a chosen name; the correct rendering is **Emily (@21andsensory)**.

Both are recorded here because the fix — populating `corporate_name_note` — is a data write this
session deliberately did not make (§7).

---

## 6. Bibliographic defects confirmed by both passes independently

- `volume`, `issue`, `pages_start`, `pages_end`, `article_number`, `issn` are **NULL on all five
  rows**, while the held Crossref payloads supply them. Every row is stamped
  `verification_status='VERIFIED'`, `verified_by_tool='crossref'`, `metadata_quality='COMPLETE'`.
  **`metadata_quality='COMPLETE'` is false as stored.**
- **`REF-00968.pages = '2645738'` is a value no payload asserts.** Three independent sources agree
  the article has no page range; that is the article number written into a pages column. Same
  family as the 2026-08-19 fabrication, one field-class over, in a row marked VERIFIED.
- `REF-00607.pages` and `REF-00967.pages` likewise hold article numbers, with `volume` NULL.
- `REF-00968.pub_title` drops the possessive apostrophe (`students'` → `students`).

These are precisely the fields the widened `verify_authors()` (plan §5.2) would catch, and precisely
why it prints CLEAN today.

---

## 7. What this session deliberately did not do

No rows were written. The canonical DB's sha256 is unchanged at
`ebab426f54ef45efb76db4c3f461a5ebdc6ce7c2966312b667f55c82168c692b`.

Writing the biblio backfill would have been safe and correct in isolation. It was not done because
the same migration would have been the vehicle for the cell, and **the cell should not be
written** — so the honest artifact of this session is the refusal plus its evidence, not a partial
write that implies the walk completed. The backfill is the first act of the next session.

---

## 8. What the next act is

Not a determination. Not apparatus. **A search round with the right frame**, then a re-grade.

1. **Re-run the AUT query with the item's own terms** — `("reverberation time" OR RT60 OR Tmf) AND
   (classroom OR school OR "learning space") AND (autistic OR neurodivergent OR SEN OR "special
   hearing and communication needs")`. Log verbatim before screening (R8). If this returns
   non-trivial on-parameter yield, the zero-value finding was query-shape, not absence.
2. **Promote REF-00561** (`10.3390/app11093942`) from `source_locators` through a full R1–R15
   admission walk. It is already owned.
3. **Retrieve Greenland 2026** and read its actual criterion. Closed access — expect degraded mode
   and record it. Until then its figures stay `[UNVERIFIED-QUANT]`.
4. **Admit Rosas-Pérez 2023** (`10.1121/2.0001741`) — same cohort as REF-00965 but set in schools
   and universities. Note it makes two of the three proposed governing refs one cohort, which is a
   fresh L3 problem, not a solution.
5. **Resolve the tier question** (§4) with the owner.
6. **OD-5 now has two witnesses.** It is no longer the highest-value *pending* decision; it is the
   demonstrated cause of a repeated, population-level miss.

---

## 9. The result worth keeping

The agonist–antagonist mechanic did the job it was designed for, on its first use against real
research output. A cell was about to be written that would have been well-sourced, carefully
hedged, adversarially reviewed, correctly capped at `provisional` — and **wrong**, because it
would have rendered a coverage failure as an epistemic finding. The antagonist's phrasing is worth
preserving verbatim:

> *"a cell that will sit in the guidebook as a well-documented, adversarially-audited, carefully-hedged blank — and the very quality of its documentation is what will make future readers trust the blank. That is a worse outcome than a wrong number, because a wrong number gets corrected and a well-defended absence does not."*

The pipeline was walked far enough to prove it walks. What it carried back was a reason not to
publish yet. That is a successful pass, not a failed one.
