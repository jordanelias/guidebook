# Session notes — 2026-08-25, rulings incorporation and pipeline sweep

Created at the FIRST natural break, not at session end, per the owner directive of
2026-08-25 now standing as `CLAUDE.md` §0 rule 7. Two sessions on 2026-08-24 closed
with no record and no scratchpad; their reasoning was recovered from a transcript
only because someone thought to look before it was gone.

## What the owner asked, in order

1. Rebase and read PR #117 in full.
2. Ensure the four owner rulings in the attached screenshots are ratified and
   incorporated into process — *"as they are fundamental."*
3. Always commit scratchpads, regularly enough that compaction cannot take them.
4. Interrogate DR / CLAUDE.md / guardrails for OTHER rulings discarded or missed
   over the past couple of weeks.
5. Fable 5 read-only audit of CLAUDE.md; Opus 5 to rewrite it entirely.
6. Does CLAUDE.md require the stage-by-stage pipeline to be recorded as well as
   pointer discipline?
7. Sweep for ALL pipeline descriptors/frameworks start to finish — owner recalls an
   EIGHT-stage pipeline.
8. Sweep for other cases of multiple owners and conflicts.
9. *"we only need one set of tools that manages how to write to a table, read a
   table, and cross-reference them."*

## Findings so far

### F1 — the four rulings were NOT ratified and NOT incorporated
Measured, not assumed. Greps for the rulings' own terms across
`references/project-standards.md`, `CLAUDE.md` and `governance/*.md` returned NOTHING
for all four. Meanwhile `DR-2026-08-24`'s header still read "§2 WAS CARVED OUT OF THAT
RATIFICATION" — a label that was correct when §2 held my inferences and wrong from the
moment §2 was replaced with the owner's quoted words. For a day the document told every
reader that the owner's own rulings were unratified inference, while PD-0, PD-3 and PD-5
shipped to `main` citing §2.1.

Rule 0 settles it: a live owner statement binds ON CONTACT. There was never a carve-out
to lift in substance, only a stale label to remove.

FIXED in `68c5126`: carve-out lifted; all four entered in the append-only ledger as
RULEs with the owner's words quoted; `CLAUDE.md` rules 5 and 6 added; §6 given the
cross-product frame.

### F2 — pydantic is missing from the container and it reddens the governance battery
`origin/main` at `d6ef7e9`, measured in a clean worktree:
  without pydantic  5 BLOCKING failures, 10 advisory  -> FAIL
  with pydantic     0 blocking,           4 advisory  -> PASS, 50 green
The five are validate_schema, validate_evidence_state, audit_adversarial_use,
decision_capture, doctrine_recheck — the whole governance battery, which
check-registry.yaml already declares `deps: [pydantic]`.

This INVERTS CLAUDE.md's own advice to reproduce a red check before assuming it is
yours: here the reproduction succeeds on untouched main, and the wrong conclusion is
available. Fixed with `.claude/hooks/ensure-deps.sh` + documented. `pip install -r
requirements.txt` must never be run here — it pins PyYAML==6.0.3 and pip refuses to
uninstall the Debian PyYAML 6.0.1, aborting the whole install so pydantic never lands.

Trap sprung while fixing it: inserting a SessionStart hook at index 0 turns the blocking
`research_contract_sync` red, because `research_contract_hook.py` reads
`SessionStart[0]["hooks"][0]["command"]` by hardcoded index. Append instead.

### F3 — the stage pipeline is not recorded, so rule 5 is not applicable
`CLAUDE.md` names the stage sequence exactly once, in passing, inside rule 5. It never
says what the stages are, which tables belong to which, or R7's other half (*"scaffolding
has to be phase specific… as soon as any tools/work cross phases, they become
illegible"*). Pointer discipline is unusable without the map: judging whether a column is
a legitimate stage-specific fact or a copy REQUIRES knowing its table's stage.

At least two models exist and neither is in CLAUDE.md:
  - `governance/pipeline-map.yaml` — FOUR `layers:`, and it explicitly REFUTED the phase
    reading on 2026-08-21 ("the stages are table buckets, not phases… LAYERS a walk
    re-enters"). That finding is about WRITE ORDER.
  - Owner ruling `DR-2026-08-24` §2.2 — FIVE stages, research -> evidence -> synthesis ->
    specifications -> render. That ruling is about WHAT A TABLE MAY HOLD.
  Both can be true. They collide on the WORD, and they assign tables differently.

Counting across the whole repo (grep -r, so ignored paths included) shows far more
models than two: "9-step" ~71 mentions, "8 step" ~26, "4-phase", "4 stage", "5 stage",
"seven phases", "12-step". The owner recalls an eight-stage pipeline. Sweep running.

**Deliberately did NOT write the stage table into CLAUDE.md yet.** Entrenching one of
several competing models before the sweep returns would be inventing an authority — the
failure class of migration 061.

### F4 — CLAUDE.md audit (Fable 5, read-only) returned and verified
Four stale factual claims, all of the §2(b) class (prose statements of derivable facts):
  A1 "Seven rules" over a list of EIGHT entries (0,1,2,3,4b,4,5,6) — third recorded
     miscount, and this time inside the sentence warning against miscounts.
  A2 the OD-5 sentence is stale: R9a/R9b DO read `source_locators` since 2026-08-23.
     Verified at research_batch_dod.py:472,500.
  A3 the `add-source` capability list is stale: authors are writable as ROWS since
     2026-08-24 (`--author 'Last|Given'`).
  A4 "two blocking checks red" — the registry holds THREE blocking freshness/render
     checks.
All four independently re-verified before acceptance. Rewrite pending the pipeline sweep.

### F5 — this session's command log is being filed under ANOTHER session

`.claude/hooks/record-command.py` appends every Bash call to
`scratchpad/<stem>/commands.jsonl`, and takes `<stem>` from `sessions/LATEST` —
correctly, since 2026-08-23, when it was changed to stop reading `.claude/session`
(a second pointer to the same fact; the fix was itself pointer discipline).

But `sessions/LATEST` still reads `session_2026-08-23-research-batch-03-forward-mining`.
So every command this session runs is appended to BATCH 03's log, polluting the record
of a research session that closed two days ago with governance work it never did.

This is rule 7's own gap, and it is worth stating precisely: the rule says *"if no
session directory exists, create it and commit into it"* — I did that, and it was not
enough, because the HOOK does not look at the directory I created. It looks at the
pointer. **Creating the scratchpad is not the same act as claiming it.**

The fix is not a hook change. `sessions/LATEST` is the single home for "which session is
running" and the hook is right to read it; what is missing is that opening a session must
UPDATE that pointer. That requires the session record to exist first (the pointer names a
`.md`), and touching `sessions/` requires an attestation under CLAUDE.md §0 rule 2.

So the owed unit of work is: session record + attestation + pointer update, done together.
Recorded here rather than rushed, because an attestation written to unblock a stop hook is
the ceremony-without-meaning that rule 2 is already on probation for.

NOTE for whoever reads batch-03's log: lines timestamped 2026-08-24T23:32 onward and all
of 2026-08-25 are NOT batch-03's work. They are PR #116/#117 review and this session.

### F6 — suite interrogation, my own structural pass (deep audit delegated, running)

Measured 2026-08-25. Commands in the command log.

SURFACE SIZES
  scripts/         85 files   26,422 lines
  tools/            4 files    3,284 lines
  .claude/hooks/    2 files      183 lines
  skills/          61 files   11,077 lines

DB ACCESS SHAPES — the headline
  raw `sqlite3.connect(` call sites .......... 104
    of those read-only (`mode=ro`) ............ 54
    of those opening read-write ............... 50
  files importing a shared db helper ........... 0     <-- THE FINDING
  surviving `PRAGMA journal_mode` .............. 1 (a COMMENT in db.py saying it is
                                                    deliberately not set — not a defect)

**There is no shared connection helper. 104 call sites each re-implement the open.**
`scripts/db.py` HAS a `connect()` with the right shape (read-only URI, `query_only`,
no persistent pragma) and NOTHING IMPORTS IT. That is the owner's "one set of tools"
question answered concretely: the suite does not exist as a suite; db.py is one member
of the pile rather than its core.

The 50 read-write opens are NOT 50 rule-3 violations — checked individually:
  · `migrate_db.py`                    the sanctioned writer. Correct.
  · `resolve_dois.py`, `verify_urls.py` exempt writers per DR-2026-05-28 / D-4.3-H
                                        (`pipeline_runs`, `evidence_source_authors`;
                                        named in migration_reproducibility EXEMPT_TABLES).
  · `db.py`                             the write CLI. Correct.
  · `readonly_db_open_audit.py`         its hits are TEST FIXTURE STRINGS. The repo already
                                        has an L2 check for this exact shape.
  · `test_db_integrity.py`, `audit_consolidator.py`  read-only work opening read-write.
                                        Untidy, not dangerous.
So the violation count is far lower than the raw grep implies. **A hit count is not a
finding** — this repo's own rule, and applying it here changed the answer.

CALLER ANALYSIS — scripts/ + tools/, 88 files
  invoked by check-registry ......... 58
  invoked by workflow or hook ........ 6
  referenced by other code .......... 21   (loose heuristic; do not over-trust)
  NO REFERENCE ANYWHERE .............. 3

The 3, each referenced in PROSE but invoked by nothing:
  · `scripts/generate_parts.py` (463 lines) — "A.12 guidebook reassembly engine".
    Named in `governance/pipeline-map.yaml`, so it is IN the pipeline model and nothing
    runs it. **L0 — it renders the book.** Under the cull rule (cull upward from L3,
    never downward from L0) this is NOT a cull candidate. It is KEEP-AND-FIX or
    CONSOLIDATE. L0 ugliness is refactored, never deleted.
  · `scripts/audit_consolidator.py` (297 lines) — L1/L2. Real cull candidate.
  · `scripts/tests/test_adjudication_integrity.py` (42 lines) — L2. Real cull candidate.

Healthier than feared: 58 of 88 are registry-invoked. The problem is not a mass of dead
scripts; it is 104 unshared connection idioms and a core module that exists but is
imported by nothing.

### F7 — pipeline-framework sweep: EIGHTEEN models found (F1..F18)

Full inventory in the agent report. Verified independently before acceptance:

**The eight-stage pipeline EXISTS and the owner's memory is right.** It is
`scripts/audit/table_connectivity.py`, DELETED 2026-08-20 in cull commit `80a34d1`.
Recovered verbatim via `git show 80a34d1~1:scripts/audit/table_connectivity.py`:

    STAGES = ["1 topic", "2 has sources", "3 sources mined", "4 values captured",
              "5 population match", "6 has a spec", "7 item has a spec",
              "8 BEST PRACTICE"]
    # "Each hop is required, not optional. A walk that survives only because a
    #  join is LEFT is not evidence of anything."

This was the repo's ONLY end-to-end PRODUCT metric — "of every ACTIVE topic, how many
can be walked to a best practice", reported as `FULLY-EVIDENCED WALKS: 0 of 80`. It was
quarantined, then culled. **And `workplan/2026-08-19-adversarial-critique-research-restart.md:243`
— a LIVE, un-superseded workplan — still defines the research restart's success criterion
as this script's metric moving off 0 of 80.** The acceptance test for the current phase of
work is a script that no longer exists.

A second eight-model exists and is not it: the 8-STEP item-audit pipeline (D-0150,
2026-05-05, `skills/item-audit-pipeline_SKILL.md`), superseded 2026-05-11 while still
PROPOSED, orchestrator deleted in the same cull.

**THE LIVE CONFLICT THAT MATTERS.** Two five-stage models, and the machine runs the wrong one:
  F17 OWNER   research -> evidence -> synthesis -> specifications -> render  (2026-08-24)
  F9  MACHINE research -> collection -> judgment -> synthesis -> render      (2026-07-13)
They disagree on 3 of 5 names. F17's "specifications" HAS NO STAGE IN F9 AT ALL.
Verified `tools/pipeline_completeness.py:37`:
    STAGES = ["research", "collection", "judgment", "synthesis", "render"]
hardcoded, and its freshness gate `pipeline_completeness_fresh` is BLOCKING. So the
blocking check, the dashboard, `pipeline_contract_audit` and `test_pipeline_contract` all
enforce the agent-authored 2026-07-13 model, while the owner's 2026-08-24 model is enforced
by nothing. Rule 0 says the owner outranks it. Nothing anywhere records that F9 was
re-examined against the ruling.

**CORRECTION to the agent report, verified.** It claimed `test_pipeline_contract.py:225`
asserts `c.status == "PROPOSED"`, mechanically pinning the stale status. IT DOES NOT —
`grep -n 'PROPOSED\|ratified\|status' scripts/tests/test_pipeline_contract.py` returns
nothing. So `pipeline-contract.yaml` reading `status: PROPOSED / ratified: false` while
`decisions/RATIFICATION-RECORD-2026-07-21.md:165` records it ACCEPTED is stale text that
NOTHING PINS. It is freely fixable — a cheaper repair than the report implied.

**DEAD BUT STILL REFERENCED** (each is a live document pointing at something deleted or superseded):
  1. `table_connectivity.py` — deleted; still the restart's success criterion (above).
  2. `skills/item-audit-pipeline_SKILL.md` — superseded 2026-05-11, orchestrator deleted,
     but live-looking with active trigger phrases; `item_audit_runs` still in schema.
  3. `skills/workplan-orchestrator_SKILL.md` — still gates tasks against "v4 C-stages" of a
     workplan superseded 2026-05-11.
  4. `governance/project-instructions-v10_14.md` — live in `governance/` (v10.8-10.13 are
     archived) and still says "All work maps to its seven phases A-G", contradicting
     DR-2026-08-19's "one operative instrument, superseding every planning document".
  5. `pipeline-contract.yaml` status field (above).

**HARD LIMIT ON THE SWEEP, recorded not smoothed:** git history is truncated at root commit
`f97dff9` (2026-07-27), so pre-2026-07-27 deletions are unrecoverable. And F10 — the
deployed claude.ai `<audit_trail>` numbered stage list — is OUTSIDE the repo entirely; its
stage count is unknown and its reconciliation was made a ratification precondition in 2026-07
and never confirmed. If the owner's eight-stage memory is neither of the two found, F10 is
the one place nobody here can look.

### F8 — suite/conflicts sweep. Verified claims only.

**TOOLSET — six write channels, one read helper with zero importers.**
  writes: emit_data_migration->migrate_db (sanctioned) · db.py subcommands (~15) ·
          HAND SQL · emit_batch_sql (capture) · resolve_dois.py · verify_urls.py
  reads:  104 raw `sqlite3.connect(` sites across 56 files; `scripts/db.py` HAS a correct
          shared `connect()` and **0 files import it**; 85 lines re-resolve
          GUIDEBOOK_DB_PATH; 47 files define their own REPO_ROOT.
  joins:  no shared helper at all.
  9 files -> 4-5 in a streamlined suite; ~88 live scripts -> ~70.

**THE HIGHEST-VALUE FIX, and it is causal not cosmetic.** Hand-SQL exists BECAUSE db.py
cannot write `search_candidates`, `evidence_population_match`, `economics_entries`,
`case_studies`, `jurisdictional_values`. That channel delivered the 2026-08-19 author
fabrication into committed data — through a capture tool that was itself blind
(`emit_batch_sql` gained `evidence_source_authors` only 2026-08-22, and `source_locators`
2026-08-23 after it SILENTLY DROPPED 8 ROWS, "emitted 32 statements, not 40… with no error
raised", its own docstring). Every new table without a subcommand re-opens it.

**LATENT GATE COLLISION — verified line by line.**
  `migration_reproducibility.py:55-63` CORE_INVARIANTS includes
      ("SELECT COUNT(*) FROM evidence_sources", "evidence_sources count")
  `migration_reproducibility.py:65` EXEMPT_TABLES = ("evidence_source_authors", "pipeline_runs")
  `resolve_dois.py:149,597,650` and `verify_urls.py:260` all `UPDATE evidence_sources`.
`evidence_sources` is a core invariant and is NOT exempt. The normal gate compares COUNTS,
so an UPDATE is invisible; `--deep` compares columns and would report it as content drift.
`pipeline_runs` has a row from the 2026-08-24 job, so this is live, not theoretical. The
remedy is one DR widening or narrowing the exemption — a decision, no new code.
Also unexempted and uninvarianted: `url_verification_runs`, whose writer has never run.

**VERIFIED BROKEN / DEAD:**
  · `scripts/generate/room_page.py:26` — `SELECT * FROM room`. The live table is `rooms`.
    A phantom table: this script cannot have run successfully since the schema existed.
    Uncalled. L0-shaped but broken -> git is the archive.
  · `skills/gap-driven-mining_SKILL.md:255` instructs `db.py update-gap-research-fields`
    — **0 occurrences in db.py's parser.** A skill telling sessions to run a subcommand
    that does not exist.
  · `db.py` docstring line 8 documents `db.py init` — also nonexistent.
  · **18 views live; 11 have zero readers.** Master plan R6 (2026-08-22) ordered
    *"Delete the 11 unread views — explicitly no owner gate"*. NOT EXECUTED. Includes
    `v_item_provenance`, repaired at the cost of migration 064 three days ago and read by
    nothing.

**DUAL HOMES, measured:**
  AGREE (kept so by parity apparatus — and per rule 5 a parity check makes a dual home
  permanent): check inventory (registry->context-map, generated, blocking freshness);
  decisions (66 files / 166 YAML / 166 DB rows, set-diff both directions = 0);
  research contract (5 homes, 2 blocking checks, PASS).
  DISAGREE NOW: `schemas/*.py` vs live SQLite — **245 drift findings**, 14 of 18 mapped
  pairs drift, `EvidenceSource` missing ~80 columns. And the authority relation ITSELF has
  no home: the registry records an OPEN OWNER QUESTION whether schemas mirror SQLite or the
  YAML layer. Cannot be triaged until that is answered.
  NO SYNC AT ALL: tier/weighting (`weighting_profile`, 5 rows, zero readers, encodes the
  audience-emphasis doctrine and no renderer consumes it); axes vs access_needs; rule text.

**LEVEL RATIO re-derived** across scripts+tools+hooks:
  L0 9,358 : L1 12,169 : L2 7,556 : L3 725  =  1 : 1.30 : 0.81 : 0.08
Better than the census's pre-cull 1 : 2.3 : 1. **The residual problem is not the ratio but
that ~1,900 LOC of L1/L2 has no subject or no runner.**

**CULL LIST (L3->L1, L0 never culled):** ~14 items — `test_adjudication_integrity.py` (L2
whose L1 subject is quarantined), `anchor-correctness-sweep.js` (no invoker), the 11 unread
views, the `validate_db` quarantine tombstone, `room_page.py`. `population_page.py` ->
CONSOLIDATE. The L0 write/read tools -> KEEP-AND-FIX into one suite, never deleted.

### F9 — SUITE CONSOLIDATION AUTHORIZED 2026-08-25

Owner: *"fable 5 plan out suite consolidation with shared library and full table CLI
coverage then Opus to execute carefully agonist-antagonist"*.

Form is this repo's own, per `DR-2026-08-19` §7: the agonist case is the RECORDED
EVIDENCE, the antagonist is a fresh attack on it, **blind-then-compare**, and there is
**no third judge** — adding one adds a loop stage. Adjudication: sustained and accepted →
correct in the same pass; disputed → cap and record the dispute; doctrine-level → the
owner.

**PRE-EXECUTION BASELINE CAPTURED** under `baseline/`, before any change, so the
consolidation can be proved to have changed nothing it should not:

  db.sha256          30a106692ab4110fe4e2082018eb256a325b2884d5740d3f62445b52c07dceaf
                     THE CANONICAL DB MUST NOT MOVE. This whole programme is code-only
                     until an act explicitly emits a migration. If this sha changes and
                     no migration was applied, something wrote the DB directly (rule 3).
  rowcounts.txt      user_version + every table's row count + every view name (85 lines).
                     Views listed because rule 4 says a view is a caller and a 0-row
                     object is unproven, not clean.
  checks-all.txt     run_checks --all: PASS, 50 green, 9 nothing-in-scope, 4 advisory.
                     Advisory failures to hold constant: validate_pydantic_schemas,
                     retired_vocabulary, validate_reasoning, test_verification_pipeline.
                     BLOCKING-and-vacuous at baseline (5): validate_evidence_state,
                     validate_verification_consistency, attestation_presence,
                     attestation_schema, check_rendered_docs. If any of these acquires a
                     subject during the work, that is a CHANGE and must be explained.
  selftest.txt       SELFTEST: PASS — registry coherent.
                     Captured because --changed-from does NOT run the selftest and the
                     selftest is where a rename fails (learned the hard way today).
  connect-sites.txt  104 raw sqlite3.connect( sites across scripts/ + tools/.
                     This is the number the consolidation must move. It is the headline
                     metric, but NOT the acceptance test on its own -- driving it to a
                     smaller number by shuffling code would satisfy the metric and miss
                     the point. The acceptance test is Fable's to define (brief item G).

**THE POINT OF THE EXERCISE, kept in front of everything else.** This is not tidying.
Hand-written SQL exists BECAUSE `db.py` cannot write five tables, and that channel is
how the 2026-08-19 author fabrication reached committed data -- 12 of 19 author rows
naming non-authors, past six green gates, through a capture tool that was itself blind.
Full-table CLI coverage closes the channel. Every act should be judged against whether
it moves that, not against file counts.

### F10 — ACT 6 REFUSED ON EVIDENCE. "Delete the 11 unread views" confuses EMPTY with DEAD.

Master-plan R6 has said since 2026-08-22: *"Delete the 11 unread views — explicitly no
owner gate (CLAUDE.md §1: dead tables and views: delete them)."* Fable's plan carried it
forward as Act 6. **The rule-4 sweep it demanded is what refutes it.**

Measured 2026-08-25. Zero code readers and zero data-migration references for all 11 —
that part holds. But *why* each returns nothing is the question nobody asked:

  v_coverage_priority       7208 rows   data EXISTS, nothing reads it
  v_source_admission          10 rows   PD-6's DESIGNATED POINTER TARGET (open item)
  v_source_reach_all          10 rows   empty-subject: specifications, specification_source_links
  v_item_provenance            0 rows   repaired by migration 064 THREE DAYS AGO
  v_code_floor_only            0 rows   empty-subject: specifications
  v_item_extractions           0 rows   empty-subject: source_value_extractions
  v_pmp_latest_walk            0 rows   empty-subject: spec_value_probes
  v_root_id_conflicts          0 rows   empty-subject: source_value_extractions
  v_registry_duplicate_...     0 rows   empty-subject: external_root_registry
  v_unregistered_roots         0 rows   empty-subject: external_root_registry, source_value_extractions
  v_value_independence         0 rows   empty-subject: external_root_registry, source_value_extractions

**EIGHT OF ELEVEN RETURN NOTHING BECAUSE THEIR SUBJECT TABLES ARE EMPTY** — `specifications`,
`source_value_extractions`, `spec_value_probes`, `external_root_registry`,
`specification_source_links`. Every one of those is a DELIVERABLE table awaiting the
pipeline reaching judgment and synthesis. These are not dead views. They are **render
surfaces waiting for data**, and dropping them destroys capability the schema
deliberately built, on the eve of the work that fills them.

**CLAUDE.md rule 4 already says this and it cuts BOTH ways:** *"treat a 0-row object as
unproven, not clean."* Unproven means do not assume it is clean — and equally, **do not
assume it is dead.** R6 read the second half as licence.

**TWO HAVE NAMED FUTURE READERS IN OPEN WORK, so dropping them is affirmatively wrong:**
  · `v_source_admission` — PD-6's plan is literally *"Data migration NULLing 10 rows,
    AFTER REDIRECTING READERS TO `v_source_admission.query_text`."* Dropping it removes
    the referent before the pointer is built — the inverse of "a pointer nothing
    dereferences", and worse.
  · `v_item_provenance` — migration 064 exists BECAUSE 063 missed it. Paying to repair a
    view on 2026-08-24 and deleting it on 2026-08-25 is not a cull, it is churn.

**THE ONE REAL CANDIDATE, and it is still not clear-cut.** `v_coverage_priority`:
7,208 rows computed over live tables, zero readers, no empty-subject excuse. That is a
genuine standing cost. BUT the owner's cross-product ruling of 2026-08-25 — every slug
against every population, access need and ICF code — is exactly the shape a
slug × language × jurisdiction priority surface serves. Dropping it the same day that
ruling landed would be poor timing at best.

**VERDICT: Act 6 NOT EXECUTED. R6's blanket order is refused on evidence and the master
plan should be corrected rather than obeyed.** Nothing is dropped. This is not a deferral
for lack of time — the sweep was run, and it says the premise is wrong.

The cheap part of Act 6 survives and is worth doing separately: per-caller join helpers,
added only in the commit where a caller adopts them.
