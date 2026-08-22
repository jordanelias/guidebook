# session_2026-08-20-provenance-walk

**Span.** 2026-08-20 to 2026-08-22. **Branch.** `claude/plan-review-execution-428t6b`, PR #111.
**Form.** Agonist/antagonist per DR-2026-08-19 §7, blind-then-compare, throughout.

**Purpose.** Review the most recent plan adversarially, correct it, execute it — and stop where the
evidence said stop. Then execute the authorised cull in full, and map the pipeline so a sequencer
can be built against something other than memory.

**Not a research session.** No search logged, no source admitted, no synthesis authored.
`search_executions` 9 at open and at close; `evidence_sources` 5; `specifications` 0.
**`sessions/LATEST-RESEARCH` is deliberately NOT moved** — moving it would aim the blocking
citation-mining gate at a session with no subjects, which is the failure CLAUDE.md §2(a) records
four times.

**The canonical DB changed, and saying otherwise would be false.**
`ebab426f…8c692b` at open → `f70c48d7…03c2c` at close. Two data migrations were applied:
`data_20260821185244` (the reasoning-doc digestion, 27 leads into `search_candidates`) and
`data_20260821185514` (the compensating retraction of 12 bad `jurisdictional_values` rows).
`user_version` 60 throughout. Row-level state at close: `search_candidates` 30,
`jurisdictional_values` 109 (all value columns NULL, as the 2026-08-12 ruling requires),
`source_locators` 835, `data_migrations` 333.

---

## 1. What was refused, and why that is the result worth keeping

The plan was built around authoring one demonstration cell, **A-18 × AUT**. It was not written.

The antagonist refuted its core claim — "no numeric value is authorable" — with named,
on-parameter, population-justified publications the batch's nine searches never reached. Not one
query paired a reverberation term with a learning-space term and a neurodivergent population. That
is a query-shape failure (R14) at the **batch-frame** level, which no row in `search_executions`
can express.

**REF-00561** (`10.3390/app11093942`, "Indoor Acoustic Requirements for Autism-Friendly Spaces")
has sat in `source_locators` since the 2026-08-06 corpus recovery. The R9 duplicate gate queries
`evidence_sources` only and is blind to all 835 locator rows, so the batch could not see that the
project **already owned** the most on-topic source for the population it was studying. This is the
second witness for OD-5, after Iglehart 2016 / REF-00578.

Full adjudication: `workplan/2026-08-20-adversarial-adjudication-a18-aut.md`. The antagonist's
formulation of why a hedged blank is worse than a wrong number is preserved there verbatim.

Later, BRK-20 found something worse: **A-18 has zero `item_population_links`** — the only item on
its slug without them. The sole route from A-18 to any population is the axis map, which owner
directive D-1 quarantines as scaffolding. The demonstration cell had no lawful applicability edge
at all. Choosing A-18 selected the one item where the question has no permitted answer.

## 2. The cull — executed in full

`workplan/2026-08-18-cull-execution-plan.md` had authorised this two days earlier and it had never
run. The census found it **half-done in the worse direction**: twelve of thirteen registry entries
were already gone while every script they invoked was still on disk. Deregistering a check and
leaving its code is the same accretion, quieter.

**6,716 LOC, 23 files, 15 registry entries.** Registry 66 → 63; quarantine 16 → 4. No registry
entry now points at a missing file. Preflight went 25 → 27 green (50 on the final diff).

Four things were kept against the plan, each on evidence: `adjudication_integrity.py` (its wrapper
is live), `code_currency_audit.py` and `pre_rehab_banner_audit.py` (quarantined, not named for
deletion), `generate_parts.py` (a call-graph orphan that assembles the actual deliverable). An
initial census flagged four registered checks as orphans; **the caller sweep caught it** — CLAUDE.md
§0.4 doing its job.

## 3. Provenance, mechanically

`.claude/hooks/record-command.py` — a PostToolUse(Bash) hook writing one JSON line per command to
`scratchpad/<session>/commands.jsonl`. Landed and proved firing. It exists because prose cannot
deliver provenance: an agent must choose to load it, and attention degrades as context fills.

**Bearing on tier grading, per owner directive:** a tier is a JUDGEMENT, and a judgement with no
recorded derivation is an assertion. `co1_provenance` NULL on all three Co-1 rows is the same
defect class as a citation written from memory.

The hook created a livelock with the container's stop hook — commit → push → CI → wake → new log
line → dirty tree — which burned two CI runs (`d0e856e`, `b19acad`) before diagnosis. Fixed by
excluding the log from the stop hook's dirty and untracked checks. **That fix is ephemeral**: it
lives in the container's `/root/.claude` and has been reverted by the harness at least twice. It
must be applied to the owner's own `~/.claude/stop-hook-git-check.sh` to persist.

## 4. The pipeline map — `governance/pipeline-map.yaml`

Commissioned so a sequencer knows, for every hop: whether the edge is enforced, who writes it, who
reads it, what guards it, and whether the hop is CODE or HAND. Built from four read-only agonist
surveys, then attacked by **three** adversarial passes. **26 breaks, each carrying a `verdict:`.**

Nineteen of twenty headline claims sustained; BRK-15 was cut back. But **six supporting assertions
were wrong**, and the four-stage linear model was refuted outright — the stages are re-entrant
table buckets, not phases, and this session's own reasoning-doc digestion is a 3→2 edge.

The third pass found an error in the correction itself: the view reader counts came from
`grep -rl <name>`, which counts files containing a string and conflates a query with a `DROP VIEW`
and with a comment. **Zero of the 17 views is queried by any code.** Recorded in place rather than
quietly fixed.

Two breaks found on the semantic guard, both latent-until-first-determination:

- **BRK-25** — `v_best_practice` never filters on `regulatory_stratum_only`. It appears only as a
  label (`strength_band='weak'`). A cell anchored solely in T4–T6, which doctrine says is walled
  off from full-strength anchoring, surfaces as best practice **annotated rather than excluded**.
- **BRK-26** — `assess_cell.py:590-599` DROPs and re-CREATEs that view while writing a
  determination, and ships the DDL inside the emitted replayable SQL. Its comment calls the
  replacement interim "until migration 027 adds a real `regulatory_stratum_only` column" — that
  column exists today. Applying it would drop `strength_band` and swap a column test for a
  `tier_basis` string match, carrying the regression into a committed migration.

## 5. Owner directives recorded this session (D-1 … D-5)

In `workplan/2026-08-20-provenance-walk-execution-plan.md` §2c. **Not yet ratified into a DR.**

- **D-1** Scaffolding is research-support only; no scaffolding link may cross into another stage.
- **D-2 / D-2a** Prose is a supplement, never the body of reasoning. The narrative belongs in
  table columns, on the same surface as the data.
- **D-3** Blocking-and-vacuous is three conditions, not one.
- **D-4** Stage 1 is the substrate — and two of its vocabularies (`jurisdictions`, `languages`)
  do not exist as tables.
- **D-5** `items` is the question, `specifications` the answer — and 21 of 93 item names embed a
  specification value, which is the question answering itself.

## 6. My own errors, recorded rather than absorbed

Five, all corrected in-session, all of the same family — **asserting an absence from a tool that
could not have seen the thing if it existed**:

| error | how it was caught |
|---|---|
| Claimed `assess_cell.py` "dissolves" the capture problem | Running it: returns `state='stated'` with a PROXY-graded source in `governing_refs` |
| Invented jurisdiction codes `AU-NZ`, `DK-NO-SE-FI`, `INT` | Self-caught pre-landing; the antagonist then proved **nothing would have caught it** |
| Wrote 12 rows of claimed values into `jurisdictional_values`, violating the 2026-08-12 REFERENCE-ONLY ruling | Blocking `test_db_integrity` L02 cardinality parity (109 YAML vs 121 table). Fixed forward |
| Hand-edited `governance/context-map.yaml`, a GENERATED file | CLAUDE.md §7. Regenerated; the generator swept 52 dead lines automatically |
| Wrote a **stale** `canonical_db_sha256_at_generation` into the map | The §2(b) failure inside the file meant to be authoritative |

Plus one claim carried from an unverified report and **retracted**: a "277-row `evidence_sources`
divergence RED in `migration_reproducibility_deep`". Running the check gives PASS, 63 tables
identical. BRK-21 is a live code path, not a live divergence.

**Method note, since it generalises.** Claims derived from `PRAGMA`/`sqlite_master` and from SQL
against live data held exactly, every time. Claims about code behaviour derived from grep hit
counts failed every time. Reading finds what *can* happen; running finds what *does* happen on
today's data — the retraction above needed both, and neither alone was sufficient.

---

## 7. HANDOFF — what the next session does

**Read first:** `decisions/DR-2026-08-19-research-restart-operative-instrument.md` (operative),
then `governance/pipeline-map.yaml` (26 breaks with verdicts), then this record.

**State at handoff.** `user_version` 60 · DB sha `f70c48d7…03c2c` · `evidence_sources` 5 ·
`specifications` 0 · `search_executions` 9 · `search_candidates` 30 · registry 63 checks,
4 quarantined · preflight PASS, 50 green, 9 nothing-in-scope, 3 advisory failures (pre-existing,
measured identical on `origin/main`).

**Do not** author a determination as the next act. The frame that would feed it is the one the
antagonist refuted.

Ordered:

1. **BRK-26 first — it is a defect in the write path you are about to use.** A determination run
   today pushes a stale view amendment into a committed migration. Not owner-gated; it is a
   correctness fix to code whose own comment explains why it exists. Do BRK-25 in the same pass
   or record why not.
2. **A search round with the corrected frame.** `("reverberation time" OR RT60 OR Tmf) AND
   (classroom OR school OR "learning space") AND (autistic OR neurodivergent OR SEN)`. Log verbatim
   before screening (R8). Non-trivial yield proves the zero-value finding was query-shape, not
   absence.
3. **Promote REF-00561** through a full R1–R15 admission walk. It is already owned.
4. **Backfill the bibliography from payloads on disk** — `volume`, `issue`, `pages_*`,
   `article_number`, `issn` are NULL on all five rows while the held Crossref payloads supply them,
   and every row is stamped `metadata_quality='COMPLETE'`, which is false as stored. Also
   `REF-00968.pages` holds an article number no payload asserts.
5. **Populate `corporate_name_note` on REF-00966** so the DB explains why "andsensory, Emily" looks
   malformed. **It is correct — she publishes under @21andsensory.** The 2026-08-19 deletion of the
   autistic community co-authors is repaired; without the note the next agent to "tidy" it deletes
   her again. Correct rendering is **Emily (@21andsensory)**.
6. **Close the map's two under-evidenced blocks** — `unclassified_paths:` was carried from an
   earlier survey without re-deriving it against `run_checks.classify()`, and
   `steps_that_are_hand_sql: [4, 5, 8, 10]` verified only Step 4 directly.

**Owner-gated, do not act unilaterally:**

- **Tier re-grade** of REF-00965 and REF-00968 from Co-1 to T3 — no co-production warrant is
  visible in the retrieved record, and `co1_source_type`/`co1_provenance` are NULL on all three.
  If sustained, `tier_basis='Co-1'` rests on **one** source, not three. Needs full texts this
  environment cannot reach. Evidence-tier definitions are DG-NON.
- **Rename `jurisdictional_values` → `jurisdictions`**, create the missing `jurisdictions` and
  `languages` substrate tables, and drop the value columns the REFERENCE-ONLY ruling forbids
  (BRK-02, BRK-22, D-4).
- **D-5 sweep** of the 21 item names that embed a specification value.
- **Lift D-1 … D-5 into a ratified DR.** They are directives recorded in a workplan, which is the
  weakest surface in the repo — `workplan/**` matches no work kind, so a plan-only commit
  classifies to the empty set.
- **OD-5** now has two witnesses and is the demonstrated cause of a repeated, population-level miss.
