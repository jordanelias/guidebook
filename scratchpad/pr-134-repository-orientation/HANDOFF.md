# Handoff — PR #134, branch `claude/repository-orientation-9380wp`

Written at session close. Everything below is derived; re-derive anything you intend to rely on
(`CLAUDE.md` rule 7).

## Watching — the subscription was dropped, one check-in remains

**PR #134's webhook subscription was deliberately dropped 2026-09-11 05:42.** Every wake produced
transcript lines, the code-enforced stop hook required them committed, and the push re-triggered CI —
a self-sustaining loop with no information in it. Nine consecutive wakes carried the same fact: a
green check suite on a commit whose only content was the transcript of verifying the previous green
check suite.

Two alternatives were considered and rejected. A `paths-ignore` on `ci.yml` for `transcripts/**` is
defensible on the merits — no battery reads that path — but if the job is a required status check, a
skipped run leaves the PR on *"expected — waiting"*, and branch protection is not readable from here.
`[skip ci]` is unavailable for a different reason: `check_commit_msg.py:57` anchors the subject with
`$` after the timestamp, so nothing can follow it.

**So `trig_015hkQrEqNMvH9g7GEEZ4feH` is now the only watcher**, firing 07:11Z and re-arming at 3h.
Its prompt carries the baseline and the reason the watch matters — the scheduled `source-verification`
workflow commits a `pipeline_runs` row into the DB blob, which inherits a binary conflict on every
open DB-touching PR (rule 3; it did this to PR #128). A redundant second check-in was deleted.
**An absent event is no longer evidence that nothing happened.** Re-subscribe with
`subscribe_pr_activity` if the owner wants webhook delivery back.

## THE NEXT SINGLE ACTION

**Decide what resolves a determination's VALUE, because nothing does.** This is the finding the first
determination produced, and it is more important than the determination.

`specifications.value_min`, `value_max` and `value_unit` are written `NULL` by `assess_cell.py` —
hardcoded `None, None, None` at `scripts/assess/assess_cell.py:1079` — and **read by nothing**: no
view, no generator, no check (`grep -rn value_min scripts/ tools/ --include='*.py'` returns only the
engine). So the project's spine defines specification as *"the determination: therefore 1200 mm,
marked ●"* and the stage has no resolved number anywhere. §8 calls an unread field and an uncalled
script the same defect; this is three unread columns whose only writer sets them to NULL.

**No check was added for it, deliberately.** §8's bar is "state what wrong thing reaches the
*guidebook*" — nothing does, because nothing reads the columns, so a gate on them would be apparatus
about the apparatus. The decision owed is upstream of a gate: either value resolution gets built (and
then a `stated` cell without a value should be refused) or the columns get dropped. Do not add the
gate before that is settled.

~~**Write the first determination.**~~ **DONE**, and faithful to ratified doctrine rather than to
intuition. `parameter_id 1 × MOB`, `stated`, `tier_basis T1`, `design_scale population`, 4 governing
refs, `convergence_assessment` `single_axis` with all four sources down-weighted,
`derivation_sha 75c34f1d82b5`. It is `stated` because `evidence-methodology.md:200` makes that the
state for "evidence at Tier 1 … with direct parameter relevance", and four T1 sources hold
extractions on this parameter. **The state machine never asks whether the cell has a VALUE** — that
is doctrine's shape, not an engine bug, and it is what the finding above is about.

One extraction was added first, from bytes, because without it the cell would have been a
determination about experimental design: extractions 1 and 3 record `1:20, 1:16, 1:12, 1:8` and
`1:8 to 1:20`, which are the **test rigs**, and extraction 2 is `claim_type absent`. Extraction 4 is
REF-00979's only outcome claim against gradient — *"major adjustments in stroking kinematics and
significant increases in muscle activity occurred at slopes between 4 degrees and 10 degrees"*
(ascent only). Worth holding beside REF-00980's own conclusion, which is a **non-recommendation**:
*"changes to the technical requirements for ramp slope and length cannot be recommended at this
time."*

### Two gates changed state because a determination finally exists

- **`validate_evidence_state` and `validate_verification_consistency` are no longer vacuous.** Both
  are blocking and both had examined nothing on every possible input. Blocking-and-vacuous is now 2,
  down from 4 at the start of this session and 6 before it.
- **`register_integrity_check` is QUARANTINED**, and the first determination is what exposed it. It
  compared the live DB against `_archived/working/pilot/pilot-renderings.html`, frozen and keyed on
  `[A-Z]-NN` item codes; 071 re-keyed `specifications` on `parameter_id`, so the two can never agree
  again. Measured both ways: against the DB at `7e9b9c8` (0 specifications rows) its selftest printed
  *"clean pass on untampered document: yes"*; against the next commit, holding one determination, it
  aborts. It passed only while it had nothing to cross-check. The invariant logic is sound and
  mutation-fires on all eight tampering scenarios, so it is quarantined rather than deleted, and
  `render/register-invariants` now says `check: null` with the reason.

~~**Re-run batch 06 steps 1–2 on a fresh scratch copy of canonical, emit the data migration, and commit
it.** Four hours of walk work exists **only** in a container scratch DB that dies with the container.
Nothing was emitted through `emit_batch_sql → emit_data_migration → migrate_db`.~~ **DONE 2026-09-11**,
and not by re-running: the scratch had NOT died — the container survived the context compaction — so
the walk was re-based rather than replayed. `migrate_db.py` was pointed at a copy of it via
`GUIDEBOOK_DB_PATH`, which applied 074 and the D-0188 data migration and brought it level with
canonical v74; `emit_batch_sql.py` then emitted only the walk's own additions. Re-running the searches
would have destroyed a record R8 makes append-only.

**The batch was NOT complete, and the DoD gate is what said so.** `research_batch_dod.py` reported five
unmet rules on the first pass — R1 (no Co-1/Co-2 pass), R2 (two T1 anchors with no `citation_mining`
row), R4 and R13 (REF-00979/980 admitted with no `evidence_population_match` row, which R13 calls
silently asserting that the population studied is the population served), and R11-harvest (neither new
source carried an `observed_terms` row). All five were closed from bytes, not memory: PMID 19236980's
abstract was retrieved for REF-00979's study population, both Crossref reference lists were retrieved
for the backward passes, and the Co-1 leg's prior was written to a file and timestamped before the
query ran. Gate now COMPLIANT on all nineteen rules.

~~One thing to re-check when you do: commit `bd0d08c` says Sanford (REF-00980) was staged-not-admitted,
and the scratch admitted it six minutes later with `scope=high_control` **after** the last manifest
fetch. Confirm that scope came from bytes before emitting it.~~ **CHECKED, and it holds.** PMID
10168021's abstract: *"One hundred seventy-one subjects of all ages and using different types of
mobility aids traversed a 30-foot ramp varying in slope from 1:8 to 1:20. Data were recorded for pulse
rate, energy expenditure, rate of travel…"* — experimental control over participants, which is what
`high_control` means under the ruling that device bench tests with no disabled participant are
`lower_control`. REF-00979 likewise: repeated-measures, ten participants with paraplegia, seven
prescribed slopes.

### The Co-1 leg found the venue, not the evidence

Worth reading before anyone records Co-1 as covered on this slug. The query returned **one** hit, and
it was not admitted: PMID 27664403 evaluates two anti-rollback prototypes with twelve chronic-SCI
participants on a fixed 7.3-m rig. Participants **tested** devices; they did not co-produce the
research, and Co-1's warrant is co-production. It is also off-parameter — the ramp is a constant of
the apparatus, so it reports no gradient. The control query (`ramp AND wheelchair`, no methods clause)
returned **97**, which is what makes the single hit a fact about publication venue rather than query
shape (R14). A real Co-1 pass on ramp gradient has to run outside PubMed. It is logged as exec 45 with
that finding in `findings_note`, and the hit is candidate 77 carrying an R7 harm finding: existing
anti-rollback devices restrict backward motion, *"limiting recovery from an overturning wheelchair,
which is a safety concern"*.

## State of the pipeline, measured

Canonical `data/guidebook.db`, `PRAGMA user_version` **74**:

| Table | Rows |
|---|---|
| `evidence_sources` | 9 |
| `base_parameters` | **0** |
| `source_value_extractions` | **0** |
| `convergence_assessment` | **0** |
| `specifications` | **0** |
| `base_taxonomy_medical` | **0** |

**Batch 06's determination is NOT written.** The PR body's claim that "a data migration is applied; the
specification stage is writable for the first time" describes the **scratch**, not canonical — correct
that sentence.

## Landed (44+ commits over `bd59fd4`; PR #134 open, mergeable, 12/12 green at `b3eaf7b`)

- **Apparatus cull, four agonist/antagonist pairs.** Blocking-and-vacuous 6 → 2. One ratified grain
  rule now has one implementation (336-triple equivalence proof). Three deletions **refused** on live
  callers the brief had missed.
- **`D-0188`** — the owner delegation, in all three homes (`727a000`, migration
  `data_20260911012015…`, DR file, attestation).
- **Migration 074** (`e89b8d2`) — `identity_medical_map`, `icf_medical_map`, the two anchor columns.
- **`db.py add-medical`** (`6bb2f71`) with nine refusals, plus the archive-aware verification fix.
- **WHO ICD-11 MMS 2024-01 release file persisted** (`6360a22`), `sha256 b92212138c67738a…`.
- Ledger entries for every ruling, including the corrections below.

## Five corrections the session made to itself — read these before trusting anything above

1. **The escalation contradicting `D-0170`.** "The medical lens stays deferred" was escalated as an
   open question six hours after the owner had ratified the lens. An empty table was read as "nobody
   decided" rather than "a ruling awaits execution."
2. **`source_locators`' corruption direction.** Reported as "the DOI is wrong"; the **title** is the
   corrupted half. REF-00037 genuinely is the Rouvier review. 31 of 36 differ, not 36.
3. **"ICD-11 cannot be verified from this container."** False. WHO's CDN release files are
   unauthenticated. I generalised from a 401 API and a JavaScript browser to a closed building, which
   is what R10 forbids.
4. **The 29-disease-entity grain.** Wrong shape; MB5 is a block and the owner said "high level".
5. **The archive-aware verification defect** — and this is the one to internalise. `add-medical`'s
   payload check substring-matched raw bytes, and the only artefact it will ever see is a
   **deflate-compressed zip**, in which no code occurs literally. So it refused the very payload that
   proves the anchor, and the ruling "verified against the persisted release file at write time" was
   **unexecutable**. The MB5 verification shown at 02:47 was done by hand in Python, never through the
   writer, while the record claimed otherwise. Fixed and proved: `--icd11 BlockL3-MB5,MB56,MB57` now
   returns `anchor_verified: true`, and `ZZ99` is still refused.

**A sixth was found by the pass that confirmed the fifth**: the "demand-populated" ruling was itself a
rationalisation, re-instating the deferral the owner had overruled. Corrected in the ledger — the lens
is populated by **correspondence from `populations` and `axes`**, ~15–20 rows, then on demand. And its
demand count was measured against the committed table while ignoring the scratch, which already held
**REF-00979 "…for Young Men With Paraplegia"** — MB56 in its own title.

## Owner-gated and unanswered

1. **"We have a PR that touches on sourcing medical codes from international database."** All 30 PRs in
   this repo were checked; none does. Which repository?
2. **WHO reuse terms for block *titles* in a CC BY-SA 4.0 work.** The ledger says item 7 is "answered";
   that is true as to *source* and not as to *titles*. Bare identifiers keep exposure minimal.
3. **B5b's four `scope` rulings** — `workplan/2026-09-10-b5b-scope-owner-escalation.md`.
4. **Whether the correspondence-populated correction is accepted** (ruled under D-0188 clause 3).

## Owed

- ~~Write `scratchpad/pr-134-repository-orientation/ADJUDICATION.md` from
  `transcripts/harness_94859b50/subagents/2026-09-11T00-54-46_other_a382a8ba.jsonl` (search
  `Ruling 1.1`). **Three homes cite it and it was never committed** — including an immutable
  `decisions` row, which cannot be corrected.~~ **DONE 2026-09-11.** Written verbatim from the
  transcript's final message rather than paraphrased, with a header naming the source bytes and a
  command that reproduces the body byte-for-byte. Its header also records which of the report's
  rulings landed and which did not — §1.1's 29-row vocabulary is still unwritten, and §2.3's
  `source_locators_integrity` gate was never built.
- ~~Correct the PR body's "data migration is applied" sentence.~~ **ALREADY DONE**, verified
  2026-09-11 against the live body: it reads *"The only data migration applied here is `D-0188`'s
  decisions row"*, and `git diff --name-status origin/main...HEAD -- scripts/migrations/` confirms
  exactly two additions, `074_medical_lens_crossings.sql` and
  `data_20260911012015_…circulation-geometry.sql`. **NOT done, and deliberately:** the body does not
  mention the `ADJUDICATION.md` repair. `update_pull_request` takes no patch — only a whole new body
  — so adding one line means hand-retyping ~4.4 KB of a reviewer-facing record. That is the
  hand-copied dual home this project already carries three of per decision, and a transcription slip
  in it would be worse than the omission. The commit message carries the full account.
- ~~A contract criterion stating **"the medical lens is offered, not adopted"**. Layer 2 enforces it
  (`add-medical`, 074's CHECK); Layer 1 never states it.~~ **DONE 2026-09-11**, as two criteria
  rather than one, because it is two facts at two stages: `base/base-medical-lens-offered-not-adopted`
  (MD- shape, no value-bearing name, every row crossed) and
  `specification/no-diagnosis-only-determination` (a determination is never keyed on a diagnosis
  alone). `medical_lens_integrity`'s registry `basis:` moved off the borrowed
  `base-population-vocabulary` onto the first; `basis` is singular, so selftest C7 lists the second
  among criteria no check claims — enforced, unclaimed, and recorded in the entry rather than left
  to be rediscovered. Two stale rationales in the same entry were corrected in the pass: the
  demand-populated no_floor (superseded by the correspondence correction, whose own CONDITION names
  "any session citing the demand-populated entry") and the "no WHO credentials" note.
- `sessions/LATEST` / `LATEST-RESEARCH` still name batch 05. They move at CLOSE with a session record,
  and **the D-0188 attestation already names `session_2026-09-10-research-batch-06-circulation-geometry`**
  — so the record must be written under exactly that id.

## Traps a fresh session will otherwise rediscover

- **Migration 074's header still says the content is licensing-blocked.** Migrations are immutable
  (rule 3); the ledger supersedes it. Do not edit it.
- **Two session ids are in play**: `…batch-06-circulation-geometry` (data) and
  `…medical-lens-icd11` (the WHO retrieval log). Gates scope by id, and the wrong one passes green
  having examined nothing.
- **`scratchpad/CURRENT`** = `pr-134-repository-orientation` (correct).
- **The b-anchor join over-reaches.** MB56 → b730 → AX-AMB/REA/WHM → carries BAR, LPA, TALL, who
  attach anthropometrically. No mechanical guard exists and `CLAUDE.md` §8's bar does not justify
  building one; `identity_medical_map.relationship` forcing `identity_first` is the schema's own prune.
  Author rows per identity; never generate them from the join.
- **`adherence_log_audit.py:517`** defaults `base=HEAD~1 head=HEAD`, so the two blocking attestation
  gates examine one commit regardless of `--changed-from`.
- **`term_aliases.language` is lowercase** (`'en'`) while `search_executions.language` is uppercase.
  A case-wrong filter returns nothing and reads as absence.
