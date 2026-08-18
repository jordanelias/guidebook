# 2026-08-18 — How to begin research

**Status:** PROPOSAL, and deliberately small. One slug, end to end, under the admission discipline.
**Marked for Fable 5**, which is returning to improve this: every §6 item is a judgment I could not
settle mechanically, and §5 is the falsification design I am least confident in.

---

## 0. A correction I owe, and it changes the goal

`workplan/2026-08-18-cull-execution-plan.md` §0.3 says the cull "does not re-enter the pre-reset
stash… and that omission is the plan's largest defect." **The adversarial critique said the same
thing. We were both wrong**, and the document that settles it is the reset decision itself:

> `DR-2026-08-06-clean-room-evidence-reset.md` §4.1 — **"Research resuming does not restore these
> rows. It writes new ones under the logged-search discipline (`db.py log-search`), carrying the
> admission edge that 95% of the frozen corpus lacked."**

The reset was not a loss to recover from. It was a decision, taken because **824 of 863 sources had
no recorded admission** and **0 of 306 walks were fully evidenced** — the corpus could not show its
work, so it was demoted to reference. Re-importing it would recreate exactly the condition the reset
existed to end.

**`_archived/data/corpus-pre-reset-2026-08-06.db` is a lead list, not a backup.** Consulting it to
find candidate sources is legitimate; every one still has to be searched for, logged, re-retrieved and
admitted on its own evidence. Correction folded into the cull plan's §0.3 by this document.

## 1. What "begin research" means mechanically

The frame is live and populated. Research does not need to build anything first:

| Live | Count |
|---|---|
| `slugs` — the research units | **106** (80 ACTIVE, 23 STUB, 3 MERGED) |
| `items` × `populations` — the determination grid | 93 × 23 |
| `axes`, `access_needs` + maps | 17, 17, 232 mapping rows |
| `term_aliases` — multilingual search terms | 2,382 |
| `jurisdictional_values` | 109 |

Empty and awaiting the first batch: `search_executions`, `search_admissions`, `search_candidates`,
`evidence_sources`, `source_slug_links`, `specifications`, `gaps`.

**The write path is fixed and non-negotiable:** `scripts/db.py log-search` / `add-source` for research
rows, then `scripts/emit_data_migration.py` → `scripts/migrate_db.py`. Never hand-edit the DB.

**The gate is `python3 scripts/audit/research_batch_dod.py --session <id>`**, which enforces R1–R15 —
the contract injected into every session. It has a `--selftest` that proves its checks fire.

## 2. The first batch: one slug, all the way through

**Slug: `room-acoustic-performance`.**

Chosen for one reason: it is the **only slug with an existing reasoning doc**
(`references/bpc-reasoning/room-acoustic-performance.md`, 300 lines) — the single surviving instance of
the primary deliverable. The walk is known to complete for it.

That matters because the first batch is testing **the pipeline, not the topic.** If a fresh clean-room
pass on a slug that has already been walked once cannot produce an evidenced determination, the defect
is in the machinery and we learn that cheaply. On any other slug, pipeline failure and research
failure look identical.

**Scope: one slug × the populations its axes already map.** Not the whole grid. The deliverable is one
`specifications` row that can be walked backwards to its sources, plus the search log that produced it.

## 3. The sequence

Each step names its rule and its artifact.

| # | Step | Rule | Writes |
|---|---|---|---|
| 1 | Open a session id; run the DoD gate **before** any work to capture the pre-state | — | — |
| 2 | Pull the slug's axes, access needs and populations, and its alias set in every mapped language | R4, R11 | — |
| 3 | **Log every query verbatim before screening any result.** Empties are completed work and are kept | **R8, R14** | `search_executions` |
| 4 | Screen Co-1 / T2 / Co-2 **first**, before T1 | **R1** | `search_candidates` |
| 5 | Pre-check every DOI; cross-file an existing `ref_id` rather than minting a duplicate | R9 | — |
| 6 | Re-retrieve every locator — DOI → Crossref/PubMed → publisher → repository. A publisher block is not a terminal answer | **R10** | — |
| 7 | Admit with `db.py add-source`, carrying `verification_status`, `metadata_quality`, `verification_method`, `--slug` + `--local-ref-id` | R3, R5 | `evidence_sources`, `source_slug_links` |
| 8 | Grade population-of-**study** against population-**served** on every admission | **R13** | `evidence_population_match` |
| 9 | Capture failure / harm / inadequacy findings as first-class, not by-products | R7 | `findings_note` |
| 10 | Route by class: case studies → `case_studies`, economics → `economics_entries`, code values → `jurisdictional_values` | R12 | those tables |
| 11 | Emit the migration and apply it | CLAUDE.md §4 | `data_*.sql` |
| 12 | Run the DoD gate for the session | R1–R15 | — |

**Steps 3 and 6 are where the old corpus died.** 824 of 863 sources had no admission edge — meaning
the search that found them was never logged, so no one could tell an absent result from an unasked
question. Logging before screening is what makes a zero-yield search a *finding* rather than a gap.

## 4. Acceptance — written before the work

The batch is done when all of these hold, and not before:

1. `research_batch_dod.py --session <id>` **exits 0**, and its `EXAMINED` count is **> 0**. A green
   gate that examined nothing is this repo's signature failure and has occurred four times.
2. `search_executions` has ≥ 1 row **per query run**, empties included.
3. Every admitted source has a `source_slug_links` row **and** an `evidence_population_match` row.
   No match row means silently claiming study and served populations are the same.
4. `scripts/migrate_db.py --rebuild /tmp/rebuilt.db` reproduces the committed DB, **shallow and
   `--deep`**.
5. `test_db_integrity` ≥ 72/72 — no regression from today's state.
6. `scripts/audit/table_connectivity.py` moves off **`FULLY-EVIDENCED WALKS: 0 of 80`**. One is the
   target. **This is the number that says research restarted**; every other metric in this repository
   can move without it.

## 5. The falsification design — and my least confident call

The existing reasoning doc is both an asset and a contamination risk. The design:

**Do not read `references/bpc-reasoning/room-acoustic-performance.md` until step 12 is complete.**
Log searches, screen, admit, determine — then open it and compare.

Three outcomes, all informative:

- **Converges** — the pipeline works and the old corpus was right on this slug.
- **Diverges** — a finding about the pre-reset corpus, recorded as one, and evidence the reset was
  justified beyond the admission-edge argument.
- **Clean-room pass finds materially less** — the honest reading is that the old doc rested on sources
  that would not survive R10 re-retrieval. That is the reset's premise, tested.

**Where I am least sure:** whether reading the old doc *after* the fact still contaminates the
*record* — a session that has seen the target may unconsciously write its determination toward it in
revision. A stricter design would have a second session do the comparison. I have not resolved this
and it is the first thing I would want Fable to attack.

## 6. Marked for Fable 5

Items I could not settle mechanically, in the order I most want them attacked:

1. **§5's contamination design.** See above. My mitigation may be insufficient.
2. **The slug choice.** I picked the one with a prior deliverable to isolate pipeline failure from
   research failure. The opposite case — that a slug with a prior answer is the *worst* first pick
   because it anchors — is arguable and I did not steel-man it.
3. **Scope of the first batch.** One slug × its mapped populations. Whether that is too small to prove
   the pipeline, or already too large for one session, I do not know; nobody has run a batch under the
   R1–R15 discipline, so there is no cycle time to reason from.
4. **The Opus synthesis floor.** PI rule #2 / DR-2026-06-10 bind `best_practice_synthesis` to
   Opus-class models. Steps 1–11 are inventory, verification and search — **not** synthesis, so a
   lower-tier model may run them and queue the doc. I believe step 12's determination sits below the
   floor and the *reasoning doc* sits above it. **I am not certain of that boundary** and it decides
   who may run the batch.
5. **Whether the B-before-E gate binds here.** `bpc-rewrite-workplan-2026-05-11.md` forbids rewriting a
   BPC (Phase E) until its linked sources pass Phase B verification. With `evidence_sources` at 0, a
   first batch is unambiguously Phase B — but the reasoning doc in step 12 may be Phase E work, which
   would gate it behind the batch's own completion rather than allow it in the same session.
6. **Which checks to re-declare.** The reset retired two `min_items` vacuity guards
   (`check_rendered_docs`, `source_slug_links_duplicates`) with an instruction to re-declare them the
   day their subjects repopulate. **This batch repopulates `source_slug_links`.** The re-declaration
   belongs in the same PR and I have not specified its floor value.

## 7. What this does not require

No cull phase is a prerequisite. **Research can begin today, against the repository exactly as it
stands.** The cull plan and this plan are independent, and if only one gets done it should be this one.

One ordering note that does bind: the cull plan's Phase 5 archives workplans, and this batch's session
record will cite them. **Run the first batch before Phase 5, or the citations move underneath it.**
