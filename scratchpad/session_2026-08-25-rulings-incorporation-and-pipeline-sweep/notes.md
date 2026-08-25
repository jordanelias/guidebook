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
