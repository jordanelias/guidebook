# Pipeline content review and walkability check — 2026-09-18

**Scope:** the content the pipeline has actually created, and whether the spine walks.
**Gate on:** Batch 15.
**Method:** every figure below is derived from `data/guidebook.db` read-only at
`PRAGMA user_version = 87`, plus one full `run_checks.py --all`. **Re-derive rather than trust
these numbers** (rule 7a) — the command is given beside each one.

---

## VERDICT

**The walk completes six of seven hand-offs and then stops dead.** Every stage boundary from
`base` through `specification` is crossed by a real foreign key — which is a genuine advance over
the 2026-08-27 measurement recorded in `references/project-standards.md` (*"each stage is joined to
the next through a shared topic label, not through the thing the previous stage produced — which is
why the pipeline does not walk"*). Two of the three junctions that document specified now exist and
carry rows.

**Two boundaries are still broken, and they are the first and last things a reader would touch:**
`judgment → synthesis` has no key at all, and `specification → render` has no output and no writer.
The project can determine. It cannot publish.

Content quality on the live corpus is **good and improving** — the evidence stage is the strongest
layer in the repository, R8 discipline is perfect from batch 08 onward, and batch 13's falsification
of a plausible snippet is exactly what R10 exists to produce. The defects below are concentrated in
the **judgment, synthesis and render** stages, which is to say: in everything downstream of
admission.

---

## 1. The walk, measured

Re-derive with `scratchpad/batch-13-content-review-kpz7u8/walk.py`.

| # | Hand-off | Mechanism | State |
|---|---|---|---|
| 1 | base → research | `search_executions.slug` → `slugs` | **KEYED** |
| 2 | research → evidence | `search_admissions(exec_id, ref_id)` junction | **KEYED** (one source short) |
| 3 | evidence internal | `source_value_extractions.ref_id` | **KEYED** |
| 4 | evidence → judgment | `evidence_population_match.ref_id` | **KEYED** (not all sources graded) |
| 5 | judgment → synthesis | `convergence_assessment` | **NO KEY — 0 FKs** |
| 6 | synthesis → specification | `specifications.convergence_id` | **KEYED** |
| 7 | specification → render | — | **NO OUTPUT, NO WRITER** |

**The ratios are deliberately not written here.** They moved within hours of this
document being published — batch 15 took the walk from 59/59 · 15/16 · 26/26 · 12/16 · 4/7 to
65/65 · 19/20 · 33/33 · 16/20 · 5/8, and a table of literals would now be wrong in five cells.
Run `walk.py` for the live numbers; that is rule 7a applied to this document's own table, which
first shipped with the literals in it.

`PRAGMA foreign_key_check` returns **0 violations**. The keys that exist are sound.

---

## 2. Findings, worst first

### F1 — `specification → render` does not exist. BLOCKING THE BOOK.

`site/` contains exactly one file, `site/assets/guidebook.css`. There are **no pages**, and no
script in `scripts/` renders one (`ls scripts/ | grep -iE 'render|site|build'` is empty).
`regenerate_derived.sh` regenerates four `tools/*.html` dashboards — those are governance surfaces,
not the book.

`site_pages_fresh` reports `FRESH: 0 page(s)` and `EXAMINED: 0`, trips its own vacuity guard, and is
**advisory**. This is failure mode (a) from CLAUDE.md §5 — a gate passing having examined nothing —
except it is failing, and being ignored because it is advisory.

**And the marker is unreachable.** CLAUDE.md §6 mandates ● / ◐ / ○ and says *"unmarked is an
error."* `specifications` has **no marker column** (`PRAGMA table_info(specifications)`), and the
only code that assigns a marker is `scripts/audit/register_integrity_check.py`, which is
**QUARANTINED** and operates on register prose, not on a determination. So the one mandated
reader-facing attribute of a determination has no home, no writer, and no gate.

Parameter 3 has a live determination — 5 % / 1:20, provisional — that no reader can reach.
*(Correction, 2026-09-18: this read "spec 7" when written. Batch 15 retired 7 and determined 8,
which carries the same interval. `walk.py` now derives the live id rather than pinning it.)*

### F2 — `judgment → synthesis` is the one unkeyed hand-off, and it copies.

`convergence_assessment` has **zero foreign keys**. It carries its evidence as JSON text in four
columns (`clinical_sources`, `co1_sources`, `co2_sources`, `discounted_sources`) — **14 ref_ids for
`convergence_id = 7`**, none of them a pointer.

This is one defect wearing two hats. As a *walk* defect it is the single break in the keyed spine.
As a *rule 5* defect it is the same fact written into a second home: those ref_ids already exist as
rows in `evidence_sources`, and the grading that put them in one bucket rather than another already
exists in `evidence_population_match`. The fix is the junction the 2026-08-27 design already
specified — `syn_judgment_links` in the hand-off table — and the JSON columns retire behind it
under the writer-retire → reader-retire → NULL-forward sequence.

### F3 — rule 5 is violated twice inside `specifications`, both exactly measurable.

**(a) `governing_refs` duplicates `specification_source_links`.** For `specification_id = 7` the
JSON array and the set of `role='governing'` link rows are **identical** — same eight ref_ids. One
is a pointer table with real FKs; the other is a copy beside it. All 30 rows in
`specification_source_links` carry `role='governing'`, so the link table is currently *only* the
duplicate.

**(b) `functional_basis` duplicates `population_icf_links`.** The column holds a JSON array of nine
ICF codes with a mechanism string. Those nine codes are **exactly** `population_icf_links` for
`population_code='MOB'`, reachable by pointer through `specifications.identity_code`. The array is
copied into **all seven** specification rows, and the identical mechanism sentence appears 63 times.

Both are the shape rule 5 names: *"a table cell should point to another table cell rather than
rewrite."* Neither is caught by any gate.

### F4 — the supersession chain breaks after spec 3, so retired rows are dead ends.

| spec | retired | `superseded_by_specification_id` |
|---|---|---|
| 1 | YES | 2 |
| 2 | YES | 3 |
| 3 | YES | ~~NULL~~ → 4 |
| 4 | YES | ~~NULL~~ → 5 |
| 5 | YES | ~~NULL~~ → 6 |
| 6 | YES | ~~NULL~~ → 7 |
| 7 | YES | 8 |
| 8 | no | — |

Six rows were retired and **two** carried a forward pointer. A reader landing on retired spec 4 had
no keyed route to the live determination; the successor was named only in `retirement_reason` prose,
which is a prose caller, the class rule 7a says has no gate at all.

**FIXED 2026-09-18** — the chain now runs unbroken 1→2→3→4→5→6→7→8 with spec 8 live. The fix also
caught a worse state the original table could not show: batch 15 retired spec 7 *without*
re-determining, so for several hours the corpus held **zero live determinations** and nothing went
red. `retire_specification`'s own docstring sets the order as *retire, re-determine, then link*;
only the first step had been taken. No gate asserts that a parameter has a live specification, and
that remains true.

The retire-in-place policy itself is sound and well-reasoned; every `retirement_reason` here is
honest and specific about *why* the row was superseded rather than found wrong. The defect is that
the policy was implemented without the pointer that makes it navigable.

### F5 — REF-00987 cannot be traced to a logged search, and it governs every live determination.

`REF-00987` (2010 ADA Standards) is the **only** one of 16 sources with no `search_admissions` row.
It is also in `governing_refs` on specs 4–7. So the single most-cited standard in the corpus is the
one whose admission has no R8 provenance. Every other source traces to an exec id.

### F6 — R13 grading is inconsistent *within* strata, so it is a gap and not a policy.

12 of 16 sources carry an `evidence_population_match` row. The four that do not are REF-00988 (T5),
REF-00990, REF-00991, REF-00992 (T6). But REF-00987 and REF-00995 — **also T6 codes** — are graded
`PROXY`, and REF-00996/997/998 — **also T5** — are graded. The same `evidence_type` is treated both
ways, which rules out "codes are exempt" as the explanation.

### F7 — the judgment stage's second output has never been written.

`observed_terms` holds 29 rows spanning **all 16 sources** — the R11 harvest is complete and done
well, in each source's own words. `term_adjudications` holds **0**. CLAUDE.md §6 is explicit:
harvest at evidence, adjudicate at judgment, and *"zero links after judgment is a defect."*

### F8 — all 16 structured locator columns are empty.

`locator_scheme` and the fifteen `loc_*` columns are populated on **0 of 26** extractions;
`source_section` is populated on **26 of 26**. Every locator in the corpus is free text.

The locators themselves are good — `第十九条第二項第四号ロただし書`, `Section 1, para 1.26(b)-(c),
Table 1` — precise enough for a human to re-retrieve. But nothing can compare, sort, or range-check
them, which is what the hierarchy was built for.

### F9 — `lang_detected` has no CHECK, and carries one value in two cases.

Canonical per `lang_jur_map.language` is **uppercase** (`EN`, `JA`, `NL`, `DE`). `evidence_sources`
holds **9 non-canonical lowercase rows**, 2 canonical, 5 NULL. The two most recent batches used the
canonical form; the earlier ones did not.

Rule 8 says a vocabulary comes from the column's own CHECK. This column **has no CHECK**, which is
why the drift entered unseen — `dbcore.check_values()` cannot hold a column that declares nothing.

### F10 — 73 of 87 staged candidates are unresolved R15 hypotheses.

`disposition='PENDING-VERIFICATION'` on 73 rows. **55 are legacy** (Aug sessions, mostly the
retired acoustic corpus and reasoning-doc digestion); **18 sit on the live ramp-gradient corpus.**
R15 says a staged description is a hypothesis to be re-described from the source on resolution —
18 live ones have hardened without that pass.

### F11 — `convergence_assessment` rows duplicate each other.

Rows 4 and 5 are identical in every substantive column; so are 6 and 7. A new convergence row is
written per specification even when the convergence itself is unchanged, so the table grows with
the determination history rather than with the assessments.

---

## 3. What is working, stated because it narrows where the fix goes

- **R8 prior discipline is perfect on the live corpus.** All 28 executions missing
  `prior_expectation` are batches 01–03 (execs 1–28, August, acoustic slug). **Batches 08–14 are
  0 missing out of 27.** The rule took, and the gap is legacy.
- **Empties are kept.** 40 of 59 executions are zero-yield and retained — R8's hardest instruction
  to follow, followed.
- **Verification is complete.** 16/16 sources `VERIFIED`; not one NULL `verification_status`, which
  is the exact pool the scheduled cron would otherwise claim.
- **Extraction discipline is strong.** 20 of 26 `full-read`, 20 `verified`, and 2
  `absent-confirmed` — the R14 distinction between a well-formed zero-yield and a query-shape
  failure is being recorded rather than assumed.
- **Co-2 is honestly empty.** `co2_sources` is `[]` across all four convergence rows after two
  dedicated Co-2 batches. The session records show both passes ran and admitted nothing. That is a
  null result recorded as one, not a miss.
- **Batch 13's Foundations falsification** is the single best piece of work in the recent record: a
  plausible, specific, numerate search snippet was chased to a Wayback snapshot and found to contain
  none of the figures attributed to it. That is failure mode (c) caught before it landed.
- **Blocking battery is green**; the 9 failures are advisory, and `PRAGMA foreign_key_check` is
  clean.

---

## 4. Recommended sequencing for Batch 15

The research question and the repair queue are separable, and the repairs are cheap.

**Before Batch 15 — mechanical, no owner decision needed (rule 8: deleting and repairing are not
gated):**
1. **F9** — add the CHECK to `lang_detected`, normalise the 9 rows. Smallest fix, closes a whole
   drift class.
2. **F5** — write the missing `search_admissions` row for REF-00987, or record why it cannot exist.
3. **F4** — backfill `superseded_by_specification_id` on specs 3–6.
4. **F6** — grade the four ungraded sources, or record the exemption as a rule so the inconsistency
   becomes a policy.

**Needs a decision, so raise it rather than implement it:**
5. **F2 + F3** — the junction that replaces `convergence_assessment`'s JSON, and the retirement of
   `governing_refs` / `functional_basis` behind their pointer tables. This is the rule-5 sweep, it
   touches `specifications`, and a committed data migration has INSERTed into these columns, so it
   is writer-retire → reader-retire → NULL-forward, not a drop.
6. **F1** — the render stage. This is the largest gap in the project and the only one that stands
   between a determined cell and a reader. It is content and doctrine adjacent (what a book surface
   shows, and how a marker is assigned), so it is **owner sign-off territory** under rule 8.

**The research target itself.** Spec 7 states its own falsification condition: *"Overturned if a
source states a value for this parameter at an anchoring tier."* The cell is a **PROXY** precisely
because all eight governing claims are T4–T6 and no T1/Co-1/T2/Co-2 source states a value —
which is GAP-002 in one sentence. **Batch 15's highest-value target is an anchoring-tier source
that states a ramp gradient value**, because that single admission is what lifts parameter 3 off
proxy inference. The Co-2 route has now been worked twice (batches 13, 14) and returned a real
null; the GB delegation chain batch 13 traced shows why. **T2 synthesis is the untried stratum** —
`select count(*) from search_executions where target_evidence_type='t2'` is the figure to check
before framing.

---

## 5. What this review did not examine

- **The 62 tables holding 0 rows** were counted, not audited. `items`, `case_studies`,
  `connections`, `bpc_metadata` and the rest are empty by design or by deletion, and separating
  those two is a different question from this one.
- **Reader-facing prose** in `references/` was not swept for contradictions against the DB
  (failure mode (b)). `retired_vocabulary` reports 63 occurrences on the live surface and is the
  place to start.
- **The 893 `source_locators` rows** were not re-retrieved. `source_locators_integrity` reports 31
  mismatched and 17 unprovable titles and states the repair is blocked on a missing writer, not on
  a decision.
- **No claim here rests on reading the full text of any source.** This is a review of the
  pipeline's structure and the shape of its content, not a re-verification of its evidence.
