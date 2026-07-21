# Coverage-completion loop — methodology proposal (2026-07-21)

**Status: PROPOSED.** Requires owner ratification of the decision gates in §8 before any
execution. This document proposes *how* to correct the search-coverage defect; it does **not**
run a single search, build a table, create a routine, or change any adjudicated figure. Those
wait for a ratified gate.

**Relation to existing plans.** This is not a third competing plan. It supplies the *execution
model* that `workplan/search-coverage-completion-workplan.md` (the "what": event-log substrate +
priority queue + §5 loop) and `workplan/de-grade-remediation-and-coverage-extension-2026-07-21.md`
(the "payload": batch cadence, no-new-process, migrations-only) already describe but never
operationalized. It reconciles the one point on which they conflict (§6) and answers the owner's
question — *"maybe this needs to be a looping routine"* — with a concrete, doctrine-bounded loop.

**Governs:** the cadence and mechanism by which `search_coverage`, `search_languages` (or their
successor event log), `term_aliases`, `gaps`, and `evidence_sources` are worked forward.

---

## 1. The defect (verified against `data/guidebook.db`, 2026-07-21)

| Axis | Measured state | Reading |
|---|---|---|
| Jurisdiction cells | **634 SEARCHED** / 3,140 NOT-RUN / 33 THIN / 1 NO-DATA = 3,808 rows (81 slugs × ~48 juris) | **~83% NOT-RUN** (3,140 / 3,774 searched-or-notrun) |
| Language cells | 508 SEARCHED / 190 PARTIAL / 841 NOT-RUN = 1,539 rows (81 × 19) | ~45% touched |
| Dead languages | **AR/BN/HI/SW = 0 SEARCHED; ID = 1** | 5 of 19 languages effectively unrun |

These are not merely low numbers. Under the ratified product posture
(`DR-2026-07-21-product-posture-thinking-tool-not-authority`), the machinery must *adjudicate the
evidence* to surface a best-supported figure at a stated strength, and *"you can only adjudicate a
'best' across the space you enumerate; unenumerated cells are silent omissions the transparency
posture must surface as 'we have not examined X.'"* An 83%-NOT-RUN grid with five untouched
languages is therefore not a cosmetic gap — it is a large field of **silent omissions** that the
posture obligates us either to work or to convert into explicit, reasoned deferrals. That is what
makes this **adjudication-unblocking work, permitted under the anti-displacement freeze** (posture
consequence #2), on the same footing the de-grade workplan already claims.

## 2. Root-cause diagnosis (why the grid looks like this)

1. **Vocabulary blocker (the cause of the five zeros).** `term_aliases` carries controlled
   vocabulary for **14 languages only** (44–91 aliases each). **AR, BN, HI, ID, SW have zero
   aliases.** `scripts/generate_search_queries.py` derives queries from `term_aliases`; with no
   terms it emits nothing. The five zeros are a *missing prerequisite*, not a skipped task —
   consistent with CO-0005's `[UNVERIFIED-TERMS]` flag on AR/HI/BN/SW. **No loop can search a
   language it has no vocabulary for.** Vocabulary build-out is therefore the loop's Phase 0, not
   an afterthought.
2. **The loop was designed but never built.** `search-coverage-completion-workplan.md` §5 defines a
   repeatable execution loop, but its substrate is absent: **`search_executions` (the planned
   single-source-of-truth event log) does not exist; `lang_jur_map` (the jurisdiction↔language
   bridge that says which cells are *required* vs *not-applicable*) exists but is empty (0 rows);
   `gap_mining` is empty.** The current grids are the hand-maintained placeholders that workplan
   wanted to freeze and replace.
3. **No logged-search memory → coverage can't be trusted or resumed.** Verbatim query text survives
   for only ~47 rows. A grid cell reading "SEARCHED" today cannot prove *what* was searched. Any loop
   that writes coverage by hand inherits this un-auditability; the loop must instead *log each
   executed search* and derive coverage from the log.
4. **Not a starvation problem anymore.** Every ACTIVE slug now has ≥1 linked source (0 zero-source
   slugs; the 14 named in the old plan were closed). The remaining defect is *breadth and honest
   enumeration*, not empty slugs — which is why the payload is search+link+defer, not rescue.

## 3. Why a looping routine is the right execution model — and the one thing it must not do

The user's instinct is correct. The work is a long, homogeneous tail — pop the highest-value
uncovered cell, generate queries, run them, log every one, verify locators, admit or record-empty,
check saturation, repeat — over thousands of cells plus vocabulary builds and adversarial passes.
That is definitionally a loop, and its durable state already lives in the DB, so a routine only
needs to supply the *clock and the scaffolding*, not memory.

**But in this project the loop must be *bounded and supervised*, never fire-and-forget.** The
doctrine puts the highest fabrication risk exactly where an autonomous search loop would run:
multilingual queries *"naturally find translations of the same consensus, not contradictory views,"*
and non-English standards *"may simply mirror ISO/EN/ADA without independent evidence"*
(`DR-2026-05-09`). An unattended loop that admitted sources and updated figures would mass-produce
confirmation-biased evidence and silently move adjudicated figures — the precise failure the whole
governance apparatus exists to prevent. **The routine automates the cadence and the mechanical
scaffolding; every act of *judgment* stays gated** (see §4 guardrails, §5 escalation). Concretely,
the loop MUST NOT, unattended: admit a source that fails re-retrieval; change any adjudicated /
consensus figure; ratify a gap closure; or invent vocabulary by back-translation.

## 4. The loop — states, guardrails, terminal states, and the honest success metric

**Per-cell lifecycle:** `REQUIRED → SEARCHED(scoping) → SATURATED(systematic) | DEFERRED-WITH-REASON`.
A cell is *required* only if `lang_jur_map` marks the (jurisdiction, language) pair in-scope for the
slug; otherwise it is `NOT-APPLICABLE` and never counted against us.

**One iteration (mechanical steps the routine performs):**
1. **Pop** the highest-value required cell from the priority queue (mission-value score:
   population thinness · jurisdiction role · open-gap bonus · branch thinness incl. never-run
   tier-6 · language underservice).
2. **Generate** standard + adversarial queries via `generate_search_queries.py`. If the slug/
   language is unreachable (e.g. a dead-vocab language), **do not fabricate** — emit a
   `DEFERRED-WITH-REASON = "no controlled vocabulary"` and enqueue a vocab-build task instead.
3. **Search** on the matched connector (PubMed / Scholar / bioRxiv / Consensus / web / registry),
   including an explicit adversarial term-combination per `DR-2026-05-09`.
4. **Log every fired query** as one event (verbatim `query_text`, `terms_used`, `engine`,
   targeted tier/type/scope, depth, yield) *before* screening. **No silent searches. Empties are
   kept as findings** — a logged zero-yield search is a first-class, valuable result.
5. **Verify locators** — DOIs/URLs must re-retrieve via a real tool call (`resolve_dois` /
   `verify_urls`) before a source advances. No re-retrieval → not admitted.
6. **Stage, do not commit judgment.** Candidate admissions and any figure that a new source would
   move are written to a **batch diff**, not to the live adjudication. Writes go only through
   `emit_data_migration.py → migrate_db.py` (migrations-only doctrine).
7. **Saturation check** — revise/expand; if no new admits, mark `saturated`; attempt backward/
   forward mining on tier-1/2/3 anchors.
8. **Audit + open PR** — run `tools/evidentiary_audit.py` + `scripts/audit/research_protocol_audit.py`;
   the batch lands as a PR for review, never a direct push to a live figure.

**Terminal / done.** The loop is finite: it ends when every *required* cell is either `SATURATED`
or `DEFERRED-WITH-REASON`. Coverage-to-green is explicitly **not** the target.

**Success metric (doctrine-critical).** Progress is measured as **% of required cells with ≥1
logged search** and **% saturated-or-deferred** — i.e. *equal, honest search effort with
transparent yield*. It is **never** "% of cells reading SEARCHED" or "languages taken off zero."
**No quota parity** (`de-grade` discipline): a legitimately empty AR search is a *win* (a logged,
honest omission-closure), not a failure to be papered over. This is the single guardrail that keeps
a loop from degenerating into grid-filling.

> **Owner directive, 2026-07-21 (the ratifying statement for this metric):** *"It's okay if nothing
> surfaces so long as we know that we tried hard to find something to surface."* A logged,
> adversarially-constructed, zero-yield search that re-retrieves nothing is a completed unit of
> work — the omission is now examined and disclosed, not silent. The loop is done with a cell when
> the *effort* is exhausted and recorded, not when the cell holds a result.

## 5. The routine mechanism (concrete, and its escalation gates)

**Shape:** a scheduled trigger firing a **fresh session per batch** (`create_trigger` with
`create_new_session_on_fire=true`). Each firing is a bounded unit of work — *not* an infinite
in-session spin — so cost, blast radius, and reviewability are capped per iteration:

> "Coverage loop — run one bounded batch (default 12 cells or 1 vocab-build) from the priority
> queue per `workplan/coverage-completion-loop-methodology-2026-07-21.md` §4. Log every search,
> keep empties, migrations-only, adversarial pass per DR-2026-05-09. Open a PR with the batch diff
> and the audit delta. **Do not** admit an unverifiable source, change any adjudicated figure, or
> ratify a gap — stage those and stop for review. If the required-cell queue is drained, report
> done and disable this routine."

**Cadence:** start **manual** (owner fires it, or `/loop` on demand) for the first few batches to
calibrate yield and fabrication surface; only promote to a low-frequency cron (e.g. daily) once the
first PRs show the guardrails hold. A fresh-session-per-fire routine is pausable and disables itself
on drain.

**Escalation gates (the loop stops and asks, rather than deciding):**
- a source would **move an adjudicated / consensus figure** → human + Opus synthesis
  (`DR-2026-06-10` model floor), never the loop;
- a cell needs **new controlled vocabulary** → Phase 0 vocab task with its own verification gate
  (no machine back-translation; authoritative-source or native-speaker verification, per CO-0005);
- **adversarial verification** is required before any multilingual admission (`DR-2026-05-09` /
  `DR-2026-05-13`);
- audit regression (`evidentiary_audit.py` grade drop) → pause and surface.

## 6. Reconciliation with the freeze and the two existing workplans

- **Freeze (posture consequence #2):** permitted, because closing silent omissions is a
  precondition for adjudicating a "best" per §1. To *stay* freeze-safe the loop runs the **existing
  pipeline** (de-grade discipline: "no new process") and proposes the **minimum** new substrate.
- **The one genuine conflict — the substrate — is Decision Gate 1 (§8).** The completion workplan
  argues coverage is untrustworthy until searches are logged in `search_executions`; the de-grade
  workplan says "no new process." Both cannot be fully honored. This proposal's recommendation:
  build the **minimum honest logger** (either the full `search_executions` or a thin
  `search_executions`-shaped append table) *first*, because a loop that hand-writes coverage
  re-creates the un-auditable grid we are trying to escape — but the size of that build is the
  owner's call, not this document's.
- **Payload order** follows de-grade: within-corpus relinks (zero-fabrication) before net-new
  search; P1 identity-contradiction slugs early; empties kept; no forced full-band on
  genuinely-constrained slugs.

## 7. Proposed phasing (each phase = a batch class the routine pops)

- **Phase 0 — Unblock the five dead languages.** Build verified `term_aliases` for AR/BN/HI/ID/SW
  *where `lang_jur_map` says they are required* (e.g. HI/BN for IN/BD, AR for EG/MA, ID for ID).
  Verification-gated, no back-translation. Deliverable: the generator reaches 19/19 languages, or a
  logged reason a language stays deferred. This alone retires the most visible symptom honestly.
- **Phase 1 — Stand up the loop's memory + bridge** (size per Gate 1): the logger table + populate
  `lang_jur_map` so "required vs not-applicable" is defined and the priority queue can compute.
- **Phase 2 — Drive the queue** in bounded batches: OPEN gaps (37) first (each becomes ≥1 logged
  search), then tier-6/never-run branches, then the language/jurisdiction long tail — de-grade
  payload order, adversarial pass every few batches.
- **Phase 3 — Saturation sweep + honest deferral.** Convert every remaining required cell to
  saturated or DEFERRED-WITH-REASON; publish the five-axis coverage from the log. Loop disables
  itself.

## 8. Owner decision gates (cannot be decided by this document)

1. **Substrate size** — full `search_executions` + derived views (completion-workplan), or a thin
   append-only logger first? (Recommendation: thin logger now, evolve later — but owner's call.)
2. **Loop autonomy** — (a) manual-fire only; (b) scheduled cron, fresh session per batch,
   PR-gated + escalations as in §5; or (c) higher autonomy. (Recommendation: start (a), promote to
   (b) after guardrails proven. **Never** unattended admission/ratification.)
3. **Freeze classification** — affirm this as adjudication-unblocking (like de-grade) so it may
   proceed, or hold it behind the value-genealogy adjudication backlog.
4. **Vocabulary verification standard for AR/BN/HI/ID/SW** — authoritative-source sufficient, or
   native-speaker review required before those languages go live?

## 9. What this proposal explicitly does NOT do

No search is run, no table is created, no `term_aliases` row is added, no routine/cron is created,
and no adjudicated figure is touched by this document. It is a PROPOSED methodology entering the
ratification pipeline (PR → owner review), consistent with how `DR-2026-07-21-product-posture` was
itself ratified (PR merge + explicit owner directive). Execution begins only after the §8 gates are
answered.
