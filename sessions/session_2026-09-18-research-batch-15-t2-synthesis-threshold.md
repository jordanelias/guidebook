# Batch 15 — the qualitative seam, a missing writer, and a corrupted DOI column

**Session:** `session_2026-09-18-research-batch-15-t2-synthesis-threshold`
**Parameter:** 3 (TERM-001, ramp gradient) · **Slug:** `accessible-circulation-geometry`
**Priors:** `scratchpad/batch-15-t2-synthesis-threshold/PRIORS.md`, committed at `dea4f1c` before the
first query; a second set at `70bae3e` before the two remediating queries.

**Derive every figure below rather than trusting it** — `scratchpad/batch-15-t2-synthesis-threshold/`
holds the session log, and `python3 scripts/audit/research_batch_dod.py --session <id>` re-runs the gate.

---

## 1. The batch corrected the brief that commissioned it, before framing on it

`workplan/2026-09-18-pipeline-content-review-and-walkability.md` §4 — written by me earlier the same
day — recommended T2 as **"the untried stratum"** and, correctly, named the command to check before
framing on it. Run before the priors were written, that check falsified the word:

```
select count(*) from search_executions where target_evidence_type='sr_meta'   ->  3
```

The vocabulary term is `sr_meta`, not `t2`. T2 was **lightly worked, not untried**. What survived the
correction is the whole warrant for the batch: exactly **one** T2 academic query had ever run against
parameter 3 — exec 30, a PubMed AND-chain gated on `[Publication Type]`.

This is the failure shape batch 13 recorded, caught one step earlier: a true scoped claim, a lossy
restatement, and a reader who trusts the restatement. Here the reader was the author.

## 2. Exec 30 measured its own query shape, and it is now demonstrated rather than asserted

| exec | engine | found | admitted |
|---|---|---:|---:|
| 30 (batch 08) | pubmed, `[Publication Type]` gated | **1** | 1 |
| 60 (this batch) | pubmed, same concepts, gate removed | **107** | 0 |

Two orders of magnitude apart on the same subject. R14 asks whether a zero is query-shape failure,
wrong index, or genuine absence; for exec 30 the answer is now measured.

**Exec 61 then failed the same way in the opposite direction** and is recorded as such: a
threshold-framed query returned **3008** hits because PubMed expanded `accessibility` to the MeSH
term *Architectural Accessibility* OR the stem access/accessed/accessible, and `limit` to
limit/limitation/limited. The AND-chain broadened instead of narrowing. Logged unscreened beyond the
first 25 and deliberately not retried in the same shape.

## 3. The owner directives that redirected the batch mid-flight

Four statements, in order, each superseding the framing before it (rule 0):

> *"we are looking not only for values and parameters, but also logics and arguments and qualitative work"*
> *"if a source speaks towards ramps with a high level of relevancy even tho there is no stated value then surely there is qualitative reasoning that is worthwhile"*
> *"wherever is relevant to accessibility can be mined from it"*
> *"you search by slug, but you have to adjudicate by all slugs in a category and stuff for each source"*

PRIORS.md §2 had scoped the batch to **a stated value**. Under that scope the two best sources this
batch admitted would both have been discarded as "states no value". The directive was recorded as a
supersession and acted on, and the query it produced (exec 64) was the richest of the batch.

## 4. What was admitted

| ref | source | tier (derived) | what it supplies |
|---|---|---|---|
| **REF-00977** | Kapsalis et al. 2022, *Disabled-by-design*, 48 studies, MMAT-appraised | **T2** `sr_meta` | The built environment as a **factor of disablement**; boarding ramps and entrance features named among the least accessible elements. An argument, no value. |
| **REF-00999** | Frost et al. 2020, 384 wheelchair users surveyed | T3 | 78% had ≥1 ramp incident in 3 years; 22% of those injured or with wheelchair damage; >60% named steep slope. **"Despite ADA guidelines, steep ramps remain the primary factor."** |
| **REF-01000** | Velho et al. 2016, mixed methods, London buses | T3 | **"proposed 'solutions' to accessibility, such as ramps, often generate problems of their own"** — paired with a measured 2–3× body weight through the shoulders, linked to shoulder injury. |
| **REF-01001** | Lepoglavec et al. 2023, 8 wheelchair users, 6 gravel trails | T3 | **5.50% the tipping point** after which all respondents felt uncertainty; **>9.01% almost impassable**. Derived from instrumented measurement, not restated from a code. |

**Tiers are derived, never asserted.** `add-source` refused `--tier 1` for Frost with
*"(clinical, lower_control) derives tier 3"* — a cross-sectional survey is uncontrolled. Three of the
four admissions are T3 for that reason, which matters for §6.

**REF-00977 cross-files to a retired ref_id rather than minting one.** The 2026-09-13 corpus clear
retired it with the note *"retained so this ref_id is never reissued and so a re-admission of the same
work cross-files to it (R9)"*. That is exactly what happened, which is the retirement policy working.

## 5. Two structural defects found by the write path, not by any check

### 5a. `source_locators.doi` is shuffled relative to the rest of the row — GAP-008

`add-source` refused Rouvier 2022 because its DOI is *"already filed as REF-00037"*, and Kim 2014
because its DOI is *"already filed as REF-00030"*. **Both refusals are false.** On each row the
`doi`+`issn` pair is internally consistent and correct for the NEW source, while `title`/`authors`/
`pub_year` describe a different work:

| row | `doi` / `issn` belong to | `title` says |
|---|---|---|
| REF-00037 | PLoS One, 1932-6203 → Rouvier 2022 | *Inclusive Housing Design Guide*, Runnalls & Walker 2024 — embedding its **own** different DOI in the title string |
| REF-00030 | Int J Industrial Ergonomics, 0169-8141 → Kim 2014 | a speech-intelligibility / classroom-acoustics review, Murgia et al. |

Both carry `recovered_from='corpus-pre-reset-2026-08-06'`. **R9 breaks in both directions**: false
collisions block correct admissions (2 of 5 candidate DOIs this batch), and the same shuffle must
false-clear real duplicates whose DOI landed elsewhere — silently failing the check R9 exists to be.

`source_locators_integrity` has been reporting this at **advisory** level as a title-quality issue. It
is a DOI-reliability defect that breaks a blocking gate, and the framing understated it. Repair is
blocked on a writer exactly as that check says: `db.py` cannot set `source_locators.doi` or `.title`.

**Consequence for this batch:** Rouvier 2022 was read in full and could not be admitted. The batch's
headline candidate — Kim's rise-conditioned 1:8 / 1:10 / 1:12 — is staged, not filed.

### 5b. The corpus was single-slug because no command could cross-file — GAP-009

Measured before this batch: **every source was linked to exactly one slug; not one to two.** That
looked like an editorial pattern. It was a missing writer. `add-source` refuses a second call with
*"R9: cross-file the existing ref_id rather than duplicating"* — and **no command implemented that
instruction.** The CLI named the correct action and could not perform it, so single-slug filing was
the only expressible outcome.

**Fixed forward:** `db.py link-source-slug` derives `local_ref_id` (rule 8 — never ask for what
`MAX+1` knows), demands a `--rationale` naming which claim bears on the target slug, and refuses an
unadmitted ref_id, an unregistered slug, a duplicate link, and an empty rationale. Ten cross-slug
links were written; the four new sources now reach `stair-ramp-threshold-biomechanics-accessibility`,
`threshold-and-level-access`, `accessible-design-failures-poor-performance` and
`mobility-built-environment`.

**The backlog is not fixed.** Every source from batches 01–14 still needs adjudicating against the
full slug registry, and a second backlog follows from the same directive: the zero-admission searches
whose own `findings_note` records material retrieved, read, and dropped as off-parameter — including
exec 2's *"Co-1 yield is real but OFF-PARAMETER"*.

## 6. What the batch did NOT do, stated plainly

**Parameter 3 is still a proxy determination.** Three of four admissions are T3, and T3 is not an
anchoring tier. Specification 7 was retired in place because five new extractions postdate it, but its
interval is unchanged at 5 % / 1:20 — **none of the new sources changes the value; they change the
warrant.**

The batch did produce the corpus's **first two `insufficient` relations** (extractions 37, 41). That
relation has existed in the schema and the 2026-09-13 ruling has made code-insufficiency findings
first-class evidence, and until now **no row had ever expressed one**.

**GAP-010 is what would settle the proxy.** REF-01001 derives its thresholds from measurement and its
abstract states that disabled people *"were included in the implementation of the research through the
Croatian Association of Paraplegics and Tetraplegics (HUPT)"* — a **named organisation**, which is what
`--co1-provenance` demands. If that is co-production it is **Co-1, co-primary with T1 under CRPD Art
4.3**, it states values, and specification 7's own falsification condition is met. It is filed at T3
anyway, because *"included in the implementation"* does not separate co-production from
participation-as-subjects (D-0178), MDPI is Akamai-blocked, and claiming the tier on an ambiguous
sentence is the mirror of the failure CLAUDE.md §6 calls the worst available here.

## 7. The gate failed first, and was remediated rather than waived

`research_batch_dod` returned **NON-COMPLIANT** on R1 (no Co-1 pass — I had framed the batch on T2,
and R1 says Co-1 comes first, no exceptions) and R2 (four anchors, empty mining register). Priors for
both remediating queries were written and committed at `70bae3e` **before** they ran. The Co-1 pass
(exec 65) is what found REF-01001. Final state: **COMPLIANT**.

## 8. Three refusals worth recording, because each caught a real error

- `add-extraction` refused a claim typed from an MCP response with no persisted payload behind it.
  The fix was to re-retrieve through `retrieval_log.fetch()` so verification leaves an artefact.
- It refused `--stated named` where the quote did not contain the label asserted — the source says
  *"ADA guidelines"*, not *"ADA 2010 Standards for Accessible Design"*.
- It refused a `claimed_value` carrying **60** and **78** drawn from two different sentences:
  *"A number attached to a quote rather than read from one is the 2026-08-19 fabrication shape with a
  figure in place of an author."* That is the guard working on exactly the case it was built for.

## 9. Owed

1. **GAP-010** — read REF-01001's full text; settle Co-1. Decides whether parameter 3 is still a proxy.
2. **GAP-008** — a writer for `source_locators`, then repair. Until then R9 is unreliable in both directions.
3. **GAP-009** — the cross-slug backlog for batches 01–14, and the off-parameter re-read.
4. **Candidate 88 (Kim 2014)** — the rise-conditioned derived value. Blocked by GAP-008; figure rests
   on an aggregator abstract and must not be cited until the publisher text is read.
5. **REF-00977's backward set** — its 48 included studies are the richest unmined seam for this parameter.

---

## 10. What a code review caught afterwards, and what it changed

An adversarial review of this batch returned fifteen findings. Acted on:

- **`link-source-slug` demanded a `--rationale`, echoed it back, and stored none of it.**
  `source_slug_links.relevance_note` is the column that exists for exactly this, and D-0174 (ADOPTED)
  had already measured it populated in 0 of 10 rows, in these words: *"the adjudication is made every
  time and recorded never."* The new writer collected the adjudication and recorded it never — the
  documented defect with an extra step, shipped by the same session that was congratulating itself on
  fixing a neighbouring one. Fixed: the note is stored; a link that exists without one can be
  backfilled; one that already carries a note is not silently overwritten. All twelve of this batch's
  cross-slug warrants were backfilled.
- **The batch left ZERO live determinations corpus-wide.** Spec 7 was retired in place and never
  re-determined, and nothing went red. `retire_specification`'s own docstring sets the order as
  *retire, re-determine, then link*; only step one had been taken. Fixed: spec 8 determined — **same
  interval**, which is the point, the new evidence changed the warrant and not the value — and the
  supersession chain backfilled unbroken 1→8, closing F4 of this PR's own workplan.
- **Three of four admissions carried `jurisdiction` NULL** although determinable, and the per-link
  fan-out multiplied each omission across every slug it reached. Fixed to US / GB / INT. The column
  had no writer at all — neither `amend-source` nor `correct-source` would take it — so it was added
  to the amendable set with the reasoning recorded beside it.
- **The writer accepted MERGED and STUB slugs and superseded ref_ids, and could report a write it did
  not perform** (`INSERT OR IGNORE`, with the duplicate check on a separate connection). Now refused
  or surfaced; `local_ref_id` also inherits the slug's existing label scheme instead of imposing a
  bare integer on a slug labelled `ACG-01…`.
- **`walk.py` was pinned to literal id 7**, omitted `down_weighted_sources` from the five JSON
  ref-id columns, and would crash on a NULL one. It now derives the live specification id — which
  mattered immediately, since this batch retired 7.

Recorded but NOT fixed here, each being wider than this batch:

- **Multi-slug filing breaks `citation_mining_completeness`'s per-slug semantics.** Its join ignores
  slug while `citation_mining` is keyed per (slug, local_ref_id) and `citation_mining_status` is one
  flag per source. Harmless while every source had one slug; not harmless now. It cuts both ways —
  one pass satisfying R2 for five slugs, and the legacy fallback fanning out into false UNMINED rows.
  **This is a direct consequence of the fix in §5b** and the honest reading is that GAP-009's fix
  opened it.
- **Every `retrieval_log.fetch()` call in batches 10–15 omits `ref_id=`,** so each artefact carries
  `ref_id: null` and every verbatim check resolves to the weak UNSCOPED branch — which proves the
  words are in the corpus, not that they came from this source. Batches 08–09 populated it. That is a
  regression in the §5(c) anti-fabrication control, and it qualifies what this session's attestation
  claims about byte-for-byte verification.
- **Ten commands from this session landed in batch 14's `commands.jsonl`** before `scratchpad/CURRENT`
  was moved — the §7 trap, verbatim, in the session that quoted it.
