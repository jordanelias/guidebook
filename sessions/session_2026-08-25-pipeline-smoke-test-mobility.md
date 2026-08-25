# session_2026-08-25-pipeline-smoke-test-mobility

**Opened and closed 2026-08-25.** Commissioned by the owner: an exhaustive, non-destructive smoke
test of the five-stage pipeline (`research → evidence collection → judgment → synthesis → render`)
ahead of a mobility research batch — corridor widths, door thresholds, sloped surfaces, flooring
materials, handrails — drawn from jurisdiction buckets 1 and 2 and driven from the clue store.

**No evidence was admitted, and this session wrote no migration.** `data/guidebook.db` held
sha256 `30a1066…` at open and at close of the session's own work; every stage exercise ran against a
per-agent scratch copy.

**Amended after rebase, 2026-08-25.** PR #119 merged a migration to `main`, and this branch was
rebased onto it, so the branch now carries main's `6cceacd2…`. The claim that matters is unchanged
and is now stated the precise way: **this branch introduces no change to `data/guidebook.db` of its
own** — `git diff --name-only origin/main HEAD -- data/guidebook.db` returns nothing. The earlier
wording pinned a sha that only held while `main` stood still, which is the same class of defect as
a hand-written count in a derived document.

Working record: `scratchpad/session_2026-08-25-pipeline-smoke-test-mobility/` (7,122 lines across
ten logs). Report: the `Severed Walk` artifact. Attestation:
`attestations/sessions_session_2026-08-25-pipeline-smoke-test-mobility.json`, verdict
DEVIATION-LOGGED.

## Method

Six stage agents (Sonnet 5), one per stage plus substrate, each with its own scratch DB, working to
a protocol fixed in writing before any of them ran (`PROTOCOL.md`) so the traces would be
comparable. Three read-only auditors (Fable 5) then contextualised the traces against doctrine.
Findings written by Opus 5, which also audited the seams between stages — the part no stage agent
owned — and re-derived every load-bearing claim before repeating it.

Two process notes worth carrying forward. **The auditors were given a read-only agent type and so
could not write their own files**; two of three digests were transcribed by hand into
`logs/F1-…md` and `logs/F2-…md`, which is a provenance weakness of my making. And **six agents
shared one worktree** — safe only because five were forbidden to touch tracked files and the sixth
restored what it dirtied file-by-file. It worked; it was not guaranteed to.

## The result in one table

| Stage | Rows | Given perfect upstream data |
|---|---:|---|
| research | 978 | runs |
| evidence collection | 92 | **fails its own blocking gate** — flag-sized wiring |
| judgment | **0** | **fails structurally** — no writer, engine hardcoded to 7 pilot cells |
| synthesis | **0** | **fails structurally** — first `update-bpc` INSERT crashes |
| render | 126 | runs, but citation-less |

The row counts say the pipeline is empty downstream. The right-hand column says why that is two
different problems: evidence collection needs half a dozen CLI flags; judgment and synthesis need
a writer and an engine.

**The sever is one column earlier than it looks.** `source_value_extractions` — the join between
"we found a paper" and "the paper says 1200 mm" — is specified in fourteen places, feeds the
directness calculation, is named in the pipeline contract and three governance documents, backs two
views, and **has never been written by anything**: no script, no CLI subcommand, no committed
migration. The project recorded this honestly on 2026-07-12 in three `convergence_assessment`
rationales ("assessment queued, not assumed") and it has been queued since. Every item in the
mobility batch is a quantity; the one stage that produces a quantity has never run.

## Findings requiring an owner decision (DG-NON)

1. **Population taxonomy.** `populations` has no code for ambulant disabled people or part-time
   wheelchair users. `MOB` is "disabled people with mobility needs; wheelchair users", described as
   "General mobility limitation including walking, balance, or wheeled mobility" — the umbrella
   whose erasure of "the ambulatory and part-time-wheelchair disabled" is named in this ledger's own
   work-from-axes RULE as one of the three self-caught erasures that caused the rule to be written.
   The demand layer (`icf_demands`) still distinguishes ambulant movement, wheeled movement and
   transfer, balance and postural demand, and reach and manipulation; cells key on
   `(item × population)`, so the distinction dies at judgment. Handrails serve ambulant and balance
   users first. Ramp gradient is an *opposed* demand. **The batch should not start before this is
   ruled on**, and the ruling is co-production work, not a schema edit.
2. **`E-08`'s rendered figure.** `site/specs/e-08.html` headlines *"Corridor Clear Width (≥1200 mm
   Minimum on All Primary Routes)"* over an honest "not yet computed" body, while
   `governance/tier-system.md` §3's own worked example for this exact parameter is a 1800 mm
   regulatory floor and a 2440 mm Co-1/T2/T3 anchor. DR-2026-08-19 §1.2's "second vector", on the
   batch's flagship item.
3. **Bucket-2 jurisdictions.** `JurisdictionCode` has no member for Spain, Portugal or Finland, and
   no record notices. The enum is *inert* — one script imports it and never opens the DB — so those
   values land silently rather than being refused. Members and a `check_vocab` call must land in the
   same change, in that order, per the sequencing the instrument already prescribes at :347.
4. **Whether any freeze condition returns.** §2.2 froze apparatus until one source had a "complete
   walk"; that phrase occurs once repo-wide, undefined and unenforced, while `evidence_sources ≥ 1`
   is stated five times including in the signed §2.5(c). The check implemented what was ratified.
   Intra-instrument drift in ratified text is not a session's to fix.

## Findings that are code fixes (evidence, not permission)

Ordered by what the batch hits first. Detail and file:line for each in
`scratchpad/…/logs/OPUS-runbook-drift.md`.

1. **Wire the canonical-write guard.** `dbcore.is_canonical()` exists to refuse writes to the
   committed DB; its only callers are its own selftest at `:438-439`. `connect()` never calls it
   and `db_path()` defaults to canonical. Two skills instruct `GUIDEBOOK_DB_PATH=data/guidebook.db`
   on four write commands. This is the instrument's own §12.4 failure mode 1 with its mitigation
   unwired.
2. **A writer for `source_value_extractions`.** Nothing else matters if the batch cannot record a
   measured value.
3. **Promote the 256 stranded mobility leads.** `sessions/artifacts/2026-05-24-b11-mobility-*.json`
   holds a real OpenAlex backward+forward pass — 272 distinct DOIs, 16 in the clue store, 0
   admitted. Hidden from ripgrep by `.ignore`. Promote DOI, year and first author; **never
   `title_short`, which is truncated**. Land this *after* the dedup fix below.
4. **Unblock the first admission.** `add-source` has no `--scope`; `--verification-status VERIFIED`
   never sets `verification_disposition='CLOSED'` (blocking `test_db_integrity` I1);
   `--evidence-type` enforces no vocabulary though the correct list already exists at `db.py:1223`.
5. **Close the R9 writer gap (OD-5's unfixed half).** `add-source` dedups DOIs against
   `evidence_sources` only (`db.py:1992-2000`); `add-locator` checks both. The gate side closed
   2026-08-23. A duplicate is caught after it lands rather than refused — the arrangement
   `db.py:362-368` condemns in its own comments.
6. **Unassessed sources must not anchor** via stated-threshold conditions 1 and 3.
   `evidence-methodology.md:127-132` puts "for the target population" in those two and not in 2 or
   4; `NOT_ASSESSED`, `PARTIAL` and `PROXY` all consolidate to `DOWN-WEIGHTED` and `anchoring()`
   admits all three. `needs_population_assessment` is computed and read by nothing. Do **not**
   apply this to conditions 2 and 4 — a blanket ban wrongly demotes T2 reviews and Co-2 CPGs.
7. **Repair the runbook.** §12.1 step 0 calls `table_connectivity.py`, deleted in the 2026-08-20
   cull (`:794`); step 7 instructs the `admitted_ref_ids` dual write the 2026-08-24 ruling
   abolished, citing H03/H04 which were deleted the same day (`:856-864`); step 4 says "No CLI"
   where `add-candidate` now exists (`:830`).
8. **Co-1 provenance.** Four mechanisms, none live: no CLI flag for `co1_provenance`; the Pydantic
   rule never invoked by the write path; `validate_evidence_state.py:76-110` reads
   `data/sources/*.yaml`, **a directory that does not exist**; and item 6 above.
9. **Small and certain.** `insert_jurisdictional_value` vocabulary check ·
   `update-bpc --population` · `room_page.py` `room`→`rooms` **and** `room_item`→`room_items` ·
   `next_gap_id()` format (`GAP-NNN` vs live `GAP-B0n-NNN`) · `index.html:7`'s "91 provisions, 661
   evidence sources" against a live 93 / 10.

## Deferred deliberately

A writer for `reasoning_doc_citations` (needed at synthesis, two stages away); the attestation
gate's local-vs-CI window split; the pipeline contract's stale prose about `register_integrity_check`
at `:126-129`; `doctrine_recheck --cross-ref` never running the drift pass that, run bare, found
three vanished governance documents; the R8 ordering gap. Each fails §1's burden-of-proof test for
batch 1.

## What works, recorded as plainly as what does not

The anti-fabrication machinery does what it was built to do. A real mobility source was admitted end
to end — Sanford, Story & Jones 1997, *Ramp Slope on People with Mobility Impairments* — retrieved
through `retrieval_log.fetch()` with a byte-identical sha256 to an independent curl, and
`--verify-authors` returned CLEAN. Also working: the five-link write path end to end on scratch
(`emit_batch_sql.py` captures UPDATEs and refuses whole-batch on DELETE; `migration_reproducibility
--deep` 66/66); `log-search`'s refusal when counts disagree with the admitted-id list;
`preflight.sh` running the selftest `--changed-from` skips; backward and forward citation mining;
and the attestation gate, which caught this session's own omission, correctly and blocking.

The gates are thickest around the database and thinnest exactly where the reader is: `index.html`,
`parts/v10` and `site/rooms` are unguarded, and two of the three are measurably wrong today.

## Corrections this session made to itself

Recorded because a register of findings without its retractions is a sales document.

- **D-6 withdrawn.** The 20 `GB` rows and their blind enforcer are already recorded at
  `instrument.md:347`, with a disposition I contradicted ("Correct and blocked, not wrong") and the
  sequencing I would have got wrong. I grepped the script, the table and the enum, never the
  instrument.
- **D-5's UN half withdrawn**; `frame-proposal:602` states it better. Its *mechanism* was then
  refuted by F3: the write is not refused, it lands silently.
- **D-12 reframed twice** — I nearly reported a worse bug that a guard already prevents, then
  mis-assigned the surviving finding to the owner when doctrine already settles it.
- **D-9 refined**: the strong wording is the anomaly, not the loser of a tie.
- **D-20**: the handrail slug exists (`fall-risk-flooring-handrail-design`, STUB, covering flooring
  *and* handrails). My own PROTOCOL asserted the premise that six agents then accepted.

**Three times in one session the record held something my search did not reach**, including the
rule governing whether this session should exist. The pattern is not carelessness about any one
file: code was searched exhaustively and prose opportunistically, in a repository whose binding
decisions live in prose.

## Supersession recorded

`references/project-standards.md` now carries the supersession the owner's 2026-08-25 directive
effected over the 2026-08-19 adversarial-review RULE — whose (a)/(b) subject limbs and clause (5)
("a pass on a pass is forbidden") this session is outside in letter. Scoped to this session only;
the RULE is unamended and the pass owed on batch 1's admitted rows stands.

## next_action

None owed. The batch is the next action, after one owner sitting on the four DG-NON items above and
one PR on the code fixes. **A second smoke test would be the loop.**
