# Remediation plan, in batches by dependency

_Generated 2026-11-19 07:07 UTC from the 120 task files (62 open, 58 merged) at commit ee64bf80 by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py`. Nothing below is typed in: re-run the generator (`python3 -I scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py`) after any task file changes, and trust the generator over this text (CLAUDE.md rule 7a)._

**What this is.** The entry document for a Sonnet executor. `REMEDIATION-WORKPLAN.md` is the index (why, owner decision register, Definition of Done); `tasks/T-<id>-*.md` is the one self-contained file per task; this file says **in what order, in what groups, and where to stop.** Evidence base: `01-handshake-ledger.md` and the audit in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/`.

## 1. How to execute

1. **Merge this workplan first.** Every task file sets `$BASE` to `origin/main` once the workplan is on it, and to the workplan branch before that.
2. **Take one batch at a time, in order.** A batch is the set of tasks whose hard dependencies all lie in earlier batches. Do not start batch *n* until every READY task of batch *n-1* is merged and its after-test is green on `$BASE`.
3. **Inside a batch, work lanes in parallel and tasks in a lane serially.** A lane is a set of tasks that touch the same file (or that a task file says to sequence). Merge a lane's tasks in the order listed; where `REMEDIATION-WORKPLAN.md` gives its own merge order for some of them (Wave 0), that order wins, because it also accounts for the characterisation harness of T-014 which must exist before the changes it compares.
4. **One task, one pull request, one executor, one task file.** Run the task's red test before, the same test after, the gate once (`scripts/preflight.sh --base "$BASE" --explain`), and the adversarial pass once before opening the pull request. Rule 9: open the pull request last, then unsubscribe.
5. **Stop at a status that is not READY.** `OWNER: OD-nn (...)` means that decision's ledger gate is CLOSED for this task (the reason is in brackets); it opens when the ledger carries the owner's answer, or, for a decision the task names as delegated, a delegated resolution whose check is not required or confirmed. `DESIGN:` means the named design file does not exist yet. `NOT FOR SONNET` means an Opus-class session or the Fable agent does it. None is an invitation to improvise. The status is computed when this file is generated; the task's own gate, run at its start, is what binds.
6. **Tooling merges before the research it unlocks (rule 10).** A research task never shares a pull request with tooling, and its row writes go only through the write path of CLAUDE.md §4.
7. **The first execution of an unpiloted task is its pilot.** List any defect found in its task file in the pull request.

## 2. The batches at a glance

| Batch | Tasks | READY | OWNER-blocked (a gate CLOSED) | DESIGN file missing | NOT FOR SONNET | Tooling / research | Lanes |
|---|---|---|---|---|---|---|---|
| 1 | 34 | 14 | 3 | 2 | 18 | 13 / 21 | 29 |
| 2 | 12 | 6 | 1 | 0 | 6 | 8 / 4 | 7 |
| 3 | 2 | 0 | 0 | 0 | 2 | 0 / 2 | 2 |
| 4 | 2 | 0 | 0 | 0 | 2 | 1 / 1 | 2 |
| 5 | 2 | 0 | 0 | 0 | 2 | 2 / 0 | 1 |
| 6 | 2 | 0 | 0 | 0 | 2 | 2 / 0 | 1 |
| 7 | 3 | 2 | 0 | 0 | 1 | 3 / 0 | 1 |
| 8 | 2 | 0 | 0 | 0 | 2 | 1 / 1 | 2 |
| 9 | 3 | 2 | 0 | 0 | 1 | 3 / 0 | 3 |

Counts are derived; the commands that check them: `ls workplan/2026-11-12-bidirectional-pipeline/tasks/T-[0-9]*-*.md | wc -l`, and the generator's own output.

**Merged** (a merge commit on HEAD names the task's branch, or the re-derive: `git log --merges --format=%s HEAD | grep -o 'task/t-[0-9a-z-]*'` and `git log --no-merges --format=%s HEAD | grep -E '^T-[0-9]+:|execute workplan T-[0-9]+' | grep -E '\(#[0-9]+\)$'`): [T-001](tasks/T-001-layer0-marks-and-text.md), [T-002](tasks/T-002-contract-entry-text.md), [T-003](tasks/T-003-owner-queue-answered-marks.md), [T-004](tasks/T-004-spec-checks-report-live-rows.md), [T-006](tasks/T-006-delete-connection-refusal.md), [T-007](tasks/T-007-add-source-standing.md), [T-008](tasks/T-008-claimed-number-check.md), [T-009](tasks/T-009-script-aware-guards.md), [T-010](tasks/T-010-add-parameter-domain-refusal.md), [T-011](tasks/T-011-supersession-pointer.md), [T-012](tasks/T-012-follow-up-reasons.md), [T-013](tasks/T-013-typed-gaps.md), [T-014](tasks/T-014-stress-harness-and-probes.md), [T-015](tasks/T-015-language-fold.md), [T-016](tasks/T-016-wp-t1a-reading.md), [T-017](tasks/T-017-wp-t2-conditions.md), [T-018](tasks/T-018-link-table.md), [T-019](tasks/T-019-lens-gather.md), [T-020](tasks/T-020-quantity-kind.md), [T-021](tasks/T-021-cell-question-gate.md), [T-022](tasks/T-022-contract-re-entry.md), [T-023](tasks/T-023-ledger-relayed-statements.md), [T-024](tasks/T-024-jurisdiction-registry.md), [T-025](tasks/T-025-base-writers.md), [T-026](tasks/T-026-alias-attestation.md), [T-028](tasks/T-028-concept-identity.md), [T-029](tasks/T-029-term-relations.md), [T-030](tasks/T-030-units-as-data.md), [T-031](tasks/T-031-clause-unit-and-open-pass.md), [T-034](tasks/T-034-cell-status-verb.md), [T-041](tasks/T-041-one-home-for-helpers.md), [T-042](tasks/T-042-derive-choices-and-counts.md), [T-043](tasks/T-043-refusals-name-next-action.md), [T-048](tasks/T-048-root-registry-writer.md), [T-049](tasks/T-049-translation-home.md), [T-050](tasks/T-050-retire-admission-edges-and-connections.md), [T-051](tasks/T-051-gap-register-cross-stage.md), [T-054](tasks/T-054-identity-retires-to-need.md), [T-055](tasks/T-055-mobility-family-tooling.md), [T-061](tasks/T-061-amend-extraction-reformat.md), [T-063](tasks/T-063-derive-extraction-repair.md), [T-067](tasks/T-067-coverage-per-parameter-via-admission.md), [T-073](tasks/T-073-fixture-ids-free-of-the-retrieval-log.md), [T-074](tasks/T-074-latest-adjudication-names-the-term.md), [T-075](tasks/T-075-gate-reports-its-subject-and-base.md), [T-076](tasks/T-076-stale-empty-claims.md), [T-078](tasks/T-078-figure-retires-in-place.md), [T-079](tasks/T-079-deferred-acts-with-age.md), [T-080](tasks/T-080-zero-result-search-states-its-cause.md), [T-083](tasks/T-083-set-kind-on-existing-parameter.md), [T-088](tasks/T-088-refusal-capture-and-disposition.md), [T-089](tasks/T-089-refusal-register-reader.md), [T-090](tasks/T-090-coverage-reads-at-batch-done.md), [T-093](tasks/T-093-ratio-unit-reformat-branch.md), [T-119](tasks/T-119-ledger-unification-entry.md), [T-121](tasks/T-121-ignore-frozen-bpc.md), [T-126](tasks/T-126-code-value-lens-at-recording.md), [T-134](tasks/T-134-state-graph-quotes-and-returns.md).

**Longest dependency chain (9 tasks):** T-102 (NOT FOR SONNET) → T-128 (OWNER: OD-67 (REFERRED BACK TO THE OWNER); NOT FOR SONNET) → T-127 (NOT FOR SONNET) → T-059 (NOT FOR SONNET) → T-068 (NOT FOR SONNET) → T-117 (NOT FOR SONNET) → T-122 (NOT FOR SONNET) → T-037 (NOT FOR SONNET) → T-038 (READY).

## Batch 1

**Entry:** the workplan is on the integration base. No open task is a prerequisite (a merged one may be: see **Merged** above).

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-005](tasks/T-005-retired-row-view-fixture.md) | A seeded test that a retired determination is surfaced by no determination view | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-027](tasks/T-027-source-identity-edition.md) | The source's own title, edition and currency can be written | 3 | TOOLING | READY | yes | — | not piloted |
| [T-032](tasks/T-032-synthesis-relations.md) | Relations synthesis can record, and what a synthesis row is | 4 | TOOLING | NOT FOR SONNET | no | — | not piloted |
| [T-033](tasks/T-033-synthesis-candidates.md) | Candidate relations on demand (read-only) | 4 | TOOLING | READY | yes | — | not piloted |
| [T-047](tasks/T-047-add-by-data-test.md) | A durable test that the base changes by data alone | 3 (end) | TOOLING | READY | yes | — | not piloted |
| [T-052](tasks/T-052-mining-stages-out-of-scope-leads.md) | Mining stages an out-of-scope source as a lead | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-056](tasks/T-056-all-leaves-identity-lens.md) | ALL leaves the identity lens: universal is stated once, by design_scale | 2 | TOOLING | OWNER: OD-48 (REFERRED BACK TO THE OWNER) | no | — | not piloted |
| [T-057](tasks/T-057-base-coverage-view.md) | The base coverage view: one state per concept and in-scope pair | 3 | TOOLING | READY | yes | — | not piloted |
| [T-060](tasks/T-060-element-determination.md) | The specifications pass writes an element-level determination (OR-14b) | 5 (after T-029 and T-019) | TOOLING | DESIGN: T-060-design.md; NOT FOR SONNET | no | — | not piloted |
| [T-069](tasks/T-069-promote-adjudicated-observations.md) | Promote the adjudicated non-English observations to forms of their terms | research | RESEARCH | NOT FOR SONNET | no | — | not piloted |
| [T-070](tasks/T-070-blind-double-extraction.md) | Blind double extraction: do two readers, and do model and effort, record the same rows? | research | RESEARCH | NOT FOR SONNET | no | — | not piloted |
| [T-071](tasks/T-071-regrade-roots.md) | Give every value-supplying figure its root | research | RESEARCH | NOT FOR SONNET | no | — | not piloted |
| [T-081](tasks/T-081-classify-zero-result-searches.md) | Each stored zero-result search states its cause | research | RESEARCH | NOT FOR SONNET | no | — | not piloted |
| [T-082](tasks/T-082-comparator-on-two-stored-figures.md) | The two stored numerical claims with no comparator get one from their source | research | RESEARCH | NOT FOR SONNET | no | — | not piloted |
| [T-084](tasks/T-084-unregistered-map-codes.md) | The language-and-jurisdiction map names only declared jurisdictions | research | RESEARCH | OWNER: OD-46 (REFERRED BACK TO THE OWNER) | no | — | not piloted |
| [T-086](tasks/T-086-bare-ratio-rows.md) | The stored gradients whose unit says only `ratio` | research | RESEARCH | NOT FOR SONNET | no | — | not piloted |
| [T-087](tasks/T-087-edmonton-checklist-batch.md) | Ship the Edmonton checklist digest as a research batch | research | RESEARCH | NOT FOR SONNET | no | — | not piloted |
| [T-091](tasks/T-091-typed-circumstance-carrier.md) | A figure's circumstance (building use, interior or exterior) in typed cells | 4 | TOOLING | DESIGN: T-091-design.md; NOT FOR SONNET | no | — | not piloted |
| [T-101](tasks/T-101-scope-fill.md) | Record the research scope on every pair | research | RESEARCH | READY | yes | — | not piloted |
| [T-102](tasks/T-102-mobility-split.md) | Decompose the mobility family by device, and carry the rows filed under MOB | research | RESEARCH | NOT FOR SONNET | no | — | piloted |
| [T-104](tasks/T-104-verify-governing-sources.md) | Verify the sources a first determination would rest on | research | RESEARCH | READY | yes | — | not piloted |
| [T-105](tasks/T-105-read-held-sources.md) | Read what is held, in full, against every parameter | research | RESEARCH | NOT FOR SONNET | no | — | not piloted |
| [T-106](tasks/T-106-retag-lenses.md) | Tag figures with every relevant model | research | RESEARCH | NOT FOR SONNET | no | — | not piloted |
| [T-108](tasks/T-108-unit-condition-repair.md) | Move conditions out of the unit cell | research | RESEARCH | READY | yes | — | not piloted |
| [T-109](tasks/T-109-parameter-kinds-data.md) | Give the live parameters their quantity kind | research | RESEARCH | NOT FOR SONNET | no | — | not piloted |
| [T-111](tasks/T-111-as-written-wording-for-stored-rows.md) | Bring the two stored spelled-out figures into line | research | RESEARCH | READY | yes | — | not piloted |
| [T-112](tasks/T-112-translate-held-text.md) | Translate the held non-English text that synthesis needs | research | RESEARCH | READY | yes | — | not piloted |
| [T-113](tasks/T-113-file-sub-national-instruments.md) | File the four held sub-national instruments under their own codes | research | RESEARCH | READY | yes | — | not piloted |
| [T-114](tasks/T-114-retire-move-ves-to-needs.md) | Retire MOVE and VES to the access needs that carry them | research | RESEARCH | READY | yes | — | not piloted |
| [T-116](tasks/T-116-upl-for-upper-limb.md) | Hold the upper-limb population as UPL, and retire LMB to it | research | RESEARCH | READY | yes | — | not piloted |
| [T-120](tasks/T-120-doctrine-amendments-and-deletions.md) | Doctrine says what the owner ruled: one home for best, most common and minimum; dead names | 0 (now, after T-119) | TOOLING | NOT FOR SONNET | no | — | not piloted |
| [T-123](tasks/T-123-parameter-directions-from-sources.md) | Each parameter with figures gets an accessibility direction read from an admitted source,  | research | RESEARCH | NOT FOR SONNET | no | — | not piloted |
| [T-129](tasks/T-129-merge-term.md) | Two terms judged one concept merge by a row, the survivor is derived, and a judgment that  | 4 | TOOLING | NOT FOR SONNET | no | — | not piloted |
| [T-135](tasks/T-135-domain-vocabulary.md) | A concept's domain comes from a vocabulary the schema holds, and the non-quantity domains  | 4 | TOOLING | OWNER: OD-69 (REFERRED BACK TO THE OWNER); NOT FOR SONNET | no | — | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 1.1: T-005
- Lane 1.2: T-027
- Lane 1.3: T-032 → T-056 → T-057 → T-120 → T-129 → T-135 — sequenced by a soft dependency or a chain of shared files
- Lane 1.4: T-033
- Lane 1.5: T-047
- Lane 1.6: T-052
- Lane 1.7: T-060
- Lane 1.8: T-091
- Lane 1.9: T-069
- Lane 1.10: T-070
- Lane 1.11: T-071
- Lane 1.12: T-081
- Lane 1.13: T-082
- Lane 1.14: T-084
- Lane 1.15: T-086
- Lane 1.16: T-087
- Lane 1.17: T-101
- Lane 1.18: T-102
- Lane 1.19: T-104
- Lane 1.20: T-105
- Lane 1.21: T-106
- Lane 1.22: T-108
- Lane 1.23: T-109
- Lane 1.24: T-111
- Lane 1.25: T-112
- Lane 1.26: T-113
- Lane 1.27: T-114
- Lane 1.28: T-116
- Lane 1.29: T-123

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-032, T-060, T-069, T-070, T-071, T-081, T-082, T-086, T-087, T-091, T-102, T-105, T-106, T-109, T-120, T-123, T-129, T-135; a decision gate CLOSED: T-056 (OD-48), T-084 (OD-46), T-135 (OD-69); a design file missing: T-060 (T-060-design.md), T-091 (T-091-design.md).

## Batch 2

**Entry:** merged and green on `$BASE`: T-032, T-057, T-084, T-091, T-101, T-102, T-105, T-116, T-120, T-129.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-035](tasks/T-035-skills-repair.md) | Skills that describe the database that exists | 4 | TOOLING | NOT FOR SONNET | no | T-120 | not piloted |
| [T-036](tasks/T-036-jurisdiction-comparison-view.md) | The jurisdiction comparison as a view | 5 | TOOLING | READY | yes | T-101 | not piloted |
| [T-040](tasks/T-040-deletion-candidates-sweep.md) | Caller sweep for the deletion candidates | 5 | TOOLING | READY | after T-032 | T-032 | not piloted |
| [T-053](tasks/T-053-engine-conflict-between-groups.md) | Conflict between groups in the engine | 4 | TOOLING | NOT FOR SONNET | no | T-032 | not piloted |
| [T-058](tasks/T-058-upl-prose-callers.md) | UPL reinstated for upper limb: the retired crosswalk and the prose that names LMB or UPL | 3 | TOOLING | READY | yes | T-116 | not piloted |
| [T-062](tasks/T-062-verified-reading-blocking.md) | A `verified` figure with no full reading is refused at rest, not only at write (the prior  | 5 | TOOLING | READY | after T-105 | T-105 | not piloted |
| [T-072](tasks/T-072-seed-quantities-from-codes.md) | Seed the list of quantities from the phrases the held codes use | research | RESEARCH | NOT FOR SONNET | no | T-101, T-105 | not piloted |
| [T-085](tasks/T-085-map-jurisdiction-foreign-key.md) | The map's jurisdiction column points at the registry | 3 | TOOLING | READY | after T-084 | T-084 | not piloted |
| [T-092](tasks/T-092-retag-circumstances.md) | Re-tag each stored figure's circumstance from its free-text setting | research | RESEARCH | NOT FOR SONNET | no | T-091 | not piloted |
| [T-107](tasks/T-107-attest-forms.md) | Attest forms per language and jurisdiction from instruments | research | RESEARCH | NOT FOR SONNET | no | T-057 | not piloted |
| [T-128](tasks/T-128-population-icf-rows-for-proposals.md) | The population-to-ICF rows the writer's proposals need: reaching, seated and standing post | research | RESEARCH | OWNER: OD-67 (REFERRED BACK TO THE OWNER); NOT FOR SONNET | no | T-102 | not piloted |
| [T-130](tasks/T-130-consolidation-sweep.md) | The consolidation sweep: candidate pairs proposed from the live base, judged, and stopped  | 4 | TOOLING | READY | after T-129 | T-129 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 2.1: T-035 → T-036 → T-053 → T-058 → T-062 → T-130 — sequenced by a soft dependency or a chain of shared files
- Lane 2.2: T-040
- Lane 2.3: T-085
- Lane 2.4: T-072
- Lane 2.5: T-092
- Lane 2.6: T-107
- Lane 2.7: T-128

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-035, T-053, T-072, T-092, T-107, T-128; a decision gate CLOSED: T-128 (OD-67).

## Batch 3

**Entry:** merged and green on `$BASE`: T-069, T-102, T-128, T-130.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-127](tasks/T-127-backfill-code-value-lenses.md) | Give every stored code value its lens by contextual judgment, with its warrant (the one-ti | research | RESEARCH | NOT FOR SONNET | no | T-102, T-128 | not piloted |
| [T-131](tasks/T-131-first-consolidation-pass.md) | The first consolidation pass over the base: every candidate pair judged, merged, related o | research | RESEARCH | NOT FOR SONNET | no | T-069, T-130 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 3.1: T-127
- Lane 3.2: T-131

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-127, T-131.

## Batch 4

**Entry:** merged and green on `$BASE`: T-056, T-120, T-127, T-128.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-059](tasks/T-059-wp-t4-agreement.md) | The prior workplan's T-4: agreement (true exclusion causes, recorded divergence, the fragi | 1 (chain, after T-019) | TOOLING | NOT FOR SONNET | no | T-120, T-127, T-128 | not piloted |
| [T-115](tasks/T-115-retag-all-rows.md) | Re-tag the figures filed under ALL by their heading's group, then retire ALL | research | RESEARCH | NOT FOR SONNET | no | T-056, T-127 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 4.1: T-059
- Lane 4.2: T-115

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-059, T-115.

## Batch 5

**Entry:** merged and green on `$BASE`: T-035, T-059, T-120.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-068](tasks/T-068-convergent-counts-roots.md) | A convergent cell states its sources, their tiers and its independent roots | 2 | TOOLING | NOT FOR SONNET | no | T-059, T-120 | not piloted |
| [T-125](tasks/T-125-capture-statements-of-greater-difficulty.md) | The judgment stage records a source's statement that disabled people struggle more at a va | 6 (after the term-resolution tooling) | TOOLING | NOT FOR SONNET | no | T-035, T-059 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 5.1: T-068 → T-125 — share `skills/run-pipeline_SKILL.md`

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-068, T-125.

## Batch 6

**Entry:** merged and green on `$BASE`: T-059, T-068, T-102, T-120.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-117](tasks/T-117-marker-table-applied.md) | The marker table applied: a circle by tier, and ⚠ in place of it for a grey, unverified or | 6 (after the term-resolution doctrine) | TOOLING | NOT FOR SONNET | no | T-068, T-102, T-120 | not piloted |
| [T-124](tasks/T-124-four-figures-of-a-cell.md) | The four figures of a cell (minimum, mode, median, maximum), computed once at the specific | 6 (after the term-resolution tooling) | TOOLING | NOT FOR SONNET | no | T-059, T-068 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 6.1: T-117 → T-124 — share `scripts/assess/assess_cell.py`

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-117, T-124.

## Batch 7

**Entry:** merged and green on `$BASE`: T-059, T-068, T-117, T-124.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-118](tasks/T-118-stage-tools-carry-specification-name.md) | The specification stage's tools carry the stage's name (deferred) | 6 (deferred: last of the term-resolution work) | TOOLING | READY | after T-059, T-068, T-102, T-117, T-120, T-127, T-128 | T-059, T-068, T-117 | not piloted |
| [T-122](tasks/T-122-contract-carries-the-owner-rulings.md) | The stage contracts carry the owner's rulings of 2026-11-14 as criteria, each pointing at  | 6 (after the term-resolution tooling) | TOOLING | NOT FOR SONNET | no | T-059, T-068, T-117, T-124 | not piloted |
| [T-133](tasks/T-133-determination-record-points.md) | A determination's record points at the map rows it read, and a gate weighs its trigger at  | 6 | TOOLING | READY | after T-059, T-068, T-102, T-120, T-124, T-127, T-128 | T-059, T-068, T-124 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 7.1: T-118 → T-122 → T-133 — share `governance/stage-map.yaml`

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-122.

## Batch 8

**Entry:** merged and green on `$BASE`: T-032, T-036, T-059, T-068, T-102, T-104, T-117, T-122, T-123, T-124, T-127, T-128, T-133.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-037](tasks/T-037-render.md) | Render from the database | 5 | TOOLING | NOT FOR SONNET | no | T-032, T-036, T-122, T-124 | not piloted |
| [T-110](tasks/T-110-first-determinations.md) | First live determinations | research | RESEARCH | NOT FOR SONNET | no | T-059, T-068, T-102, T-104, T-117, T-123, T-127, T-128, T-133 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 8.1: T-037
- Lane 8.2: T-110

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-037, T-110.

## Batch 9

**Entry:** merged and green on `$BASE`: T-037, T-110, T-131.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-038](tasks/T-038-stage-pair-gate.md) | Register the stage-pair gate | 5 | TOOLING | READY | after T-032, T-037, T-059, T-068, T-102, T-117, T-120, T-122, T-124, T-127, T-128 | T-037 | not piloted |
| [T-039](tasks/T-039-owner-edits.md) | The owner's edits as proposals through the write path | 5 | TOOLING | NOT FOR SONNET | no | T-037 | not piloted |
| [T-132](tasks/T-132-drift-detectors-bind.md) | The drift detectors bind once their subject exists (a stale stored determination, a write  | 6 | TOOLING | READY | after T-059, T-068, T-069, T-102, T-110, T-117, T-120, T-123, T-124, T-127, T-128, T-129, T-131 | T-110, T-131 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 9.1: T-038
- Lane 9.2: T-039
- Lane 9.3: T-132

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-039.

## Owner decision queue, read from the ledger (what each answer releases)

Every register decision (`grep -o -E '^### OD-[0-9]+' REMEDIATION-WORKPLAN.md`), its state by the ledger gate (the last `OD-NN STATUS:` and `OD-NN CHECK:` lines of `references/project-standards.md`), the tasks whose section 2 names it, and every task that waits on those through the hard dependencies. A decision named in a task's 'Owner decisions' bullet opens that task only on the owner's answer; one named in its 'Delegated resolutions' bullet opens on a delegated resolution whose check is not required or confirmed. The phone-ready prompts for the CLOSED ones are in `DECISION-CLOSURE.md`.

### Blocking: CLOSED, and a task's gate reads it (4)

| Decision | Gate | Tasks it holds | Waiting on those (hard dependencies) | In batches |
|---|---|---|---|---|
| OD-46 | CLOSED (REFERRED BACK TO THE OWNER) | T-084 | T-085 | 1 |
| OD-48 | CLOSED (REFERRED BACK TO THE OWNER) | T-056 | T-115 | 1 |
| OD-67 | CLOSED (REFERRED BACK TO THE OWNER) | T-128 | T-037, T-038, T-039, T-059, T-068, T-110, T-115, T-117, T-118, T-122, T-124, T-125, T-127, T-132, T-133 | 2 |
| OD-69 | CLOSED (REFERRED BACK TO THE OWNER) | T-135 | — | 1 |

### Standing, blocks no task: CLOSED, and no task's gate reads it (7)

OD-17 (DEFERRED BY THE OWNER), OD-47 (REFERRED BACK TO THE OWNER), OD-51 (REFERRED BACK TO THE OWNER), OD-52 (REFERRED BACK TO THE OWNER), OD-54 (REFERRED BACK TO THE OWNER), OD-62 (REFERRED BACK TO THE OWNER), OD-72 (REFERRED BACK TO THE OWNER)

### Open by the ledger gate (60)

| Decision | Gate | Read by |
|---|---|---|
| OD-01 | OPEN (delegated; confirmed with corrections applied) | T-036, T-101, T-113 |
| OD-02 | OPEN (delegated; confirmed with corrections applied) | T-037, T-112 |
| OD-03 | OPEN (delegated; not required) | no task gate |
| OD-04 | OPEN (owner) | T-052, T-101, T-113 |
| OD-05 | OPEN (delegated; not required) | T-052, T-105 |
| OD-06 | OPEN (delegated; not required) | T-106 |
| OD-07 | OPEN (delegated; not required) | T-032 |
| OD-08 | OPEN (delegated; not required) | T-037 |
| OD-09 | OPEN (owner) | no task gate |
| OD-10 | OPEN (owner) | no task gate |
| OD-11 | OPEN (delegated; not required) | no task gate |
| OD-12 | OPEN (delegated; confirmed with corrections applied) | T-032, T-037 |
| OD-13 | OPEN (owner) | no task gate |
| OD-14 | OPEN (owner) | T-102 |
| OD-15 | OPEN (owner) | no task gate |
| OD-18 | OPEN (delegated; not required) | no task gate |
| OD-19 | OPEN (owner) | T-032, T-053 |
| OD-20 | OPEN (delegated; not required) | T-039 |
| OD-21 | OPEN (delegated; not required) | no task gate |
| OD-22 | OPEN (delegated; not required) | no task gate |
| OD-23 | OPEN (owner) | no task gate |
| OD-24 | OPEN (delegated; not required) | T-109 |
| OD-25 | OPEN (delegated; not required) | T-032 |
| OD-26 | OPEN (delegated; not required) | T-038 |
| OD-27 | OPEN (owner) | no task gate |
| OD-28 | OPEN (owner) | no task gate |
| OD-29 | OPEN (delegated; not required) | T-032 |
| OD-30 | OPEN (delegated; not required) | T-037, T-112 |
| OD-31 | OPEN (owner) | T-056, T-102, T-115 |
| OD-32 | OPEN (owner) | no task gate |
| OD-33 | OPEN (delegated; not required) | T-037 |
| OD-34 | OPEN (owner) | T-052 |
| OD-35 | OPEN (owner) | no task gate |
| OD-36 | OPEN (owner) | T-053 |
| OD-37 | OPEN (owner) | T-102, T-114 |
| OD-38 | OPEN (owner) | no task gate |
| OD-39 | OPEN (owner) | no task gate |
| OD-40 | OPEN (delegated; confirmed with corrections applied) | no task gate |
| OD-41 | OPEN (delegated; confirmed with corrections applied) | T-086 |
| OD-42 | OPEN (delegated; confirmed with corrections applied) | no task gate |
| OD-43 | OPEN (owner) | T-068 |
| OD-44 | OPEN (owner) | T-070 |
| OD-45 | OPEN (delegated; confirmed with corrections applied) | T-081 |
| OD-49 | OPEN (delegated; confirmed with corrections applied) | T-091, T-092 |
| OD-50 | OPEN (delegated; confirmed with corrections applied) | no task gate |
| OD-53 | OPEN (delegated; confirmed with corrections applied) | no task gate |
| OD-55 | OPEN (delegated; confirmed with corrections applied) | no task gate |
| OD-56 | OPEN (owner) | T-060 |
| OD-57 | OPEN (owner) | T-117, T-120 |
| OD-58 | OPEN (owner) | T-059 |
| OD-59 | OPEN (owner) | T-117, T-120 |
| OD-60 | OPEN (owner) | T-035 |
| OD-61 | OPEN (owner) | no task gate |
| OD-63 | OPEN (owner) | T-124 |
| OD-64 | OPEN (owner) | T-117 |
| OD-65 | OPEN (owner) | T-059 |
| OD-66 | OPEN (owner) | no task gate |
| OD-68 | OPEN (owner) | no task gate |
| OD-70 | OPEN (owner) | no task gate |
| OD-71 | OPEN (owner) | no task gate |

## NOT FOR SONNET

| Task | Title | Batch | Decisions (owner's words / delegated) |
|---|---|---|---|
| [T-032](tasks/T-032-synthesis-relations.md) | Relations synthesis can record, and what a synthesis row is | 1 | — / OD-07, OD-12, OD-19, OD-25, OD-29 |
| [T-035](tasks/T-035-skills-repair.md) | Skills that describe the database that exists | 2 | OD-60 / — |
| [T-037](tasks/T-037-render.md) | Render from the database | 8 | — / OD-02, OD-08, OD-12, OD-30, OD-33 |
| [T-039](tasks/T-039-owner-edits.md) | The owner's edits as proposals through the write path | 9 | — / OD-20 |
| [T-053](tasks/T-053-engine-conflict-between-groups.md) | Conflict between groups in the engine | 2 | OD-19, OD-36 / — |
| [T-059](tasks/T-059-wp-t4-agreement.md) | The prior workplan's T-4: agreement (true exclusion causes, recorded divergence, | 4 | OD-58, OD-65 / — |
| [T-060](tasks/T-060-element-determination.md) | The specifications pass writes an element-level determination (OR-14b) | 1 | OD-56 / — |
| [T-068](tasks/T-068-convergent-counts-roots.md) | A convergent cell states its sources, their tiers and its independent roots | 5 | OD-43 / — |
| [T-069](tasks/T-069-promote-adjudicated-observations.md) | Promote the adjudicated non-English observations to forms of their terms | 1 | — / — |
| [T-070](tasks/T-070-blind-double-extraction.md) | Blind double extraction: do two readers, and do model and effort, record the sam | 1 | OD-44 / — |
| [T-071](tasks/T-071-regrade-roots.md) | Give every value-supplying figure its root | 1 | — / — |
| [T-072](tasks/T-072-seed-quantities-from-codes.md) | Seed the list of quantities from the phrases the held codes use | 2 | — / — |
| [T-081](tasks/T-081-classify-zero-result-searches.md) | Each stored zero-result search states its cause | 1 | — / OD-45 |
| [T-082](tasks/T-082-comparator-on-two-stored-figures.md) | The two stored numerical claims with no comparator get one from their source | 1 | — / — |
| [T-086](tasks/T-086-bare-ratio-rows.md) | The stored gradients whose unit says only `ratio` | 1 | — / OD-41 |
| [T-087](tasks/T-087-edmonton-checklist-batch.md) | Ship the Edmonton checklist digest as a research batch | 1 | — / — |
| [T-091](tasks/T-091-typed-circumstance-carrier.md) | A figure's circumstance (building use, interior or exterior) in typed cells | 1 | — / OD-49 |
| [T-092](tasks/T-092-retag-circumstances.md) | Re-tag each stored figure's circumstance from its free-text setting | 2 | — / OD-49 |
| [T-102](tasks/T-102-mobility-split.md) | Decompose the mobility family by device, and carry the rows filed under MOB | 1 | OD-14, OD-31, OD-37 / — |
| [T-105](tasks/T-105-read-held-sources.md) | Read what is held, in full, against every parameter | 1 | — / OD-05 |
| [T-106](tasks/T-106-retag-lenses.md) | Tag figures with every relevant model | 1 | — / OD-06 |
| [T-107](tasks/T-107-attest-forms.md) | Attest forms per language and jurisdiction from instruments | 2 | — / — |
| [T-109](tasks/T-109-parameter-kinds-data.md) | Give the live parameters their quantity kind | 1 | — / OD-24 |
| [T-110](tasks/T-110-first-determinations.md) | First live determinations | 8 | — / — |
| [T-115](tasks/T-115-retag-all-rows.md) | Re-tag the figures filed under ALL by their heading's group, then retire ALL | 4 | OD-31 / — |
| [T-117](tasks/T-117-marker-table-applied.md) | The marker table applied: a circle by tier, and ⚠ in place of it for a grey, unv | 6 | OD-57, OD-59, OD-64 / — |
| [T-120](tasks/T-120-doctrine-amendments-and-deletions.md) | Doctrine says what the owner ruled: one home for best, most common and minimum;  | 1 | OD-57, OD-59 / — |
| [T-122](tasks/T-122-contract-carries-the-owner-rulings.md) | The stage contracts carry the owner's rulings of 2026-11-14 as criteria, each po | 7 | — / — |
| [T-123](tasks/T-123-parameter-directions-from-sources.md) | Each parameter with figures gets an accessibility direction read from an admitte | 1 | — / — |
| [T-124](tasks/T-124-four-figures-of-a-cell.md) | The four figures of a cell (minimum, mode, median, maximum), computed once at th | 6 | OD-63 / — |
| [T-125](tasks/T-125-capture-statements-of-greater-difficulty.md) | The judgment stage records a source's statement that disabled people struggle mo | 5 | — / — |
| [T-127](tasks/T-127-backfill-code-value-lenses.md) | Give every stored code value its lens by contextual judgment, with its warrant ( | 3 | — / — |
| [T-128](tasks/T-128-population-icf-rows-for-proposals.md) | The population-to-ICF rows the writer's proposals need: reaching, seated and sta | 2 | OD-67 / — |
| [T-129](tasks/T-129-merge-term.md) | Two terms judged one concept merge by a row, the survivor is derived, and a judg | 1 | — / — |
| [T-131](tasks/T-131-first-consolidation-pass.md) | The first consolidation pass over the base: every candidate pair judged, merged, | 3 | — / — |
| [T-135](tasks/T-135-domain-vocabulary.md) | A concept's domain comes from a vocabulary the schema holds, and the non-quantit | 1 | OD-69 / — |

Each file says who does it. Everything that depends on one of these waits for it (the 'Reachable by Sonnet now' column names the blockers).

## Where the pilots stand

`grep -L "Not piloted" workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md` lists the tasks a pilot has touched. Results, defects found and what changed in the plan are in section 12 of `REMEDIATION-WORKPLAN.md` and in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/`.
