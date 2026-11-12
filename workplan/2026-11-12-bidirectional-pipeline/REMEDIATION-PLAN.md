# Remediation plan, in batches by dependency

_Generated 2026-11-12 07:05 UTC from the 63 task files at commit 316aef2 by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py`. Nothing below is typed in: re-run the generator (`python3 -I scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py`) after any task file changes, and trust the generator over this text (CLAUDE.md rule 7a)._

**What this is.** The entry document for a Sonnet executor. `REMEDIATION-WORKPLAN.md` is the index (why, owner decision register, Definition of Done); `tasks/T-<id>-*.md` is the one self-contained file per task; this file says **in what order, in what groups, and where to stop.** Evidence base: `01-handshake-ledger.md` and the audit in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/`.

## 1. How to execute

1. **Merge this workplan first.** Every task file sets `$BASE` to `origin/main` once the workplan is on it, and to the workplan branch before that.
2. **Take one batch at a time, in order.** A batch is the set of tasks whose hard dependencies all lie in earlier batches. Do not start batch *n* until every READY task of batch *n-1* is merged and its after-test is green on `$BASE`.
3. **Inside a batch, work lanes in parallel and tasks in a lane serially.** A lane is a set of tasks that touch the same file (or that a task file says to sequence). Merge a lane's tasks in the order listed; where `REMEDIATION-WORKPLAN.md` gives its own merge order for some of them (Wave 0), that order wins, because it also accounts for the characterisation harness of T-014 which must exist before the changes it compares.
4. **One task, one pull request, one executor, one task file.** Run the task's red test before, the same test after, the gate once (`scripts/preflight.sh --base "$BASE" --explain`), and the adversarial pass once before opening the pull request. Rule 9: open the pull request last, then unsubscribe.
5. **Stop at a status that is not READY.** `OWNER: OD-nn` means the owner's answer (in the form the register gives) must be in `references/project-standards.md` first. `NOT FOR SONNET` means an Opus-class session or the Fable agent does it. Neither is an invitation to improvise.
6. **Tooling merges before the research it unlocks (rule 10).** A research task never shares a pull request with tooling, and its row writes go only through the write path of CLAUDE.md §4.
7. **The first execution of an unpiloted task is its pilot.** List any defect found in its task file in the pull request.

## 2. The batches at a glance

| Batch | Tasks | READY | OWNER-blocked | NOT FOR SONNET | Tooling / research | Lanes |
|---|---|---|---|---|---|---|
| 1 | 26 | 24 | 1 | 1 | 24 / 2 | 15 |
| 2 | 13 | 11 | 0 | 2 | 10 / 3 | 9 |
| 3 | 8 | 5 | 1 | 2 | 3 / 5 | 8 |
| 4 | 5 | 3 | 0 | 2 | 5 / 0 | 5 |
| 5 | 4 | 2 | 0 | 2 | 3 / 1 | 4 |
| 6 | 5 | 1 | 0 | 4 | 3 / 2 | 5 |
| 7 | 2 | 1 | 0 | 1 | 2 / 0 | 2 |

Counts are derived; the commands that check them: `ls workplan/2026-11-12-bidirectional-pipeline/tasks/T-[0-9]*-*.md | wc -l`, and the generator's own output.

**Longest dependency chain (7 tasks):** T-008 (READY) → T-016 (READY) → T-017 (READY) → T-018 (NOT FOR SONNET) → T-019 (READY) → T-037 (NOT FOR SONNET) → T-038 (READY).

## Batch 1

**Entry:** the workplan is on the integration base. No task is a prerequisite.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-001](tasks/T-001-layer0-marks-and-text.md) | Mark what is superseded, and make the Layer 0 commands run as written | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-002](tasks/T-002-contract-entry-text.md) | Make the contract entries say what the owner's stage order says | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-003](tasks/T-003-owner-queue-answered-marks.md) | One home for "answered" in the owner queue | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-004](tasks/T-004-spec-checks-report-live-rows.md) | Specification checks say how many of the rows they read are live | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-005](tasks/T-005-retired-row-view-fixture.md) | A seeded test that a retired determination is surfaced by no determination view | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-006](tasks/T-006-delete-connection-refusal.md) | `delete-connection` refuses an id that is not a row | 0 (now) | TOOLING | READY | yes | — | piloted |
| [T-007](tasks/T-007-add-source-standing.md) | `add-source` writes a verification standing and a source type, or refuses | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-008](tasks/T-008-claimed-number-check.md) | The claimed number is checked as a number, and a number written in words is filed as a num | 0 (now) | TOOLING | READY | yes | — | piloted |
| [T-009](tasks/T-009-script-aware-guards.md) | Quote and name guards that work outside Latin script | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-010](tasks/T-010-add-parameter-domain-refusal.md) | `add-parameter` refuses a term that is not a design quantity (first step) | 0 (now) | TOOLING | READY | yes | — | piloted |
| [T-011](tasks/T-011-supersession-pointer.md) | Re-determining a cell points the retired row at its successor | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-012](tasks/T-012-follow-up-reasons.md) | Follow-up reasons for a skimmed figure and an absence finding | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-013](tasks/T-013-typed-gaps.md) | A gap says what it is a gap in, and a search says which gap caused it | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-014](tasks/T-014-stress-harness-and-probes.md) | Keep the stress scripts as a characterisation harness and their probes as tests | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-015](tasks/T-015-language-fold.md) | Language codes folded at the writers and in the coverage views | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-023](tasks/T-023-ledger-relayed-statements.md) | Enter the relayed statements of 2026-10-12 in the ledger | 2 | TOOLING | OWNER: OD-28 | no | — | not piloted |
| [T-024](tasks/T-024-jurisdiction-registry.md) | Jurisdictions in a table the writers read | 3 | TOOLING | READY | yes | — | not piloted |
| [T-026](tasks/T-026-alias-attestation.md) | A form says how it is attested, and a search says which forms it used | 3 | TOOLING | READY | yes | — | not piloted |
| [T-027](tasks/T-027-source-identity-edition.md) | The source's own title, edition and currency can be written | 3 | TOOLING | READY | yes | — | not piloted |
| [T-035](tasks/T-035-skills-repair.md) | Skills that describe the database that exists | 4 | TOOLING | READY | yes | — | not piloted |
| [T-042](tasks/T-042-derive-choices-and-counts.md) | Counts in the registry as commands, and one Layer 0 measure corrected | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-048](tasks/T-048-root-registry-writer.md) | A writer for the root registry | 2 | TOOLING | READY | yes | — | not piloted |
| [T-051](tasks/T-051-gap-register-cross-stage.md) | The gap register is marked cross-stage in the stage map | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-052](tasks/T-052-mining-stages-out-of-scope-leads.md) | Mining stages an out-of-scope source as a lead | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-103](tasks/T-103-medical-lens.md) | Fill the medical lens by correspondence | research | RESEARCH | NOT FOR SONNET | no | — | not piloted |
| [T-104](tasks/T-104-verify-governing-sources.md) | Verify the sources a first determination would rest on | research | RESEARCH | READY | yes | — | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 1.1: T-001 → T-002 → T-003 → T-051 — sequenced by a soft dependency or a chain of shared files
- Lane 1.2: T-004 → T-006 → T-007 → T-008 → T-009 → T-010 → T-011 → T-013 → T-042 — sequenced by a soft dependency or a chain of shared files
- Lane 1.3: T-005
- Lane 1.4: T-012
- Lane 1.5: T-014
- Lane 1.6: T-015
- Lane 1.7: T-023
- Lane 1.8: T-024
- Lane 1.9: T-026
- Lane 1.10: T-027
- Lane 1.11: T-035
- Lane 1.12: T-048
- Lane 1.13: T-052
- Lane 1.14: T-103
- Lane 1.15: T-104

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-103; waiting on the owner: T-023 (OD-28).

## Batch 2

**Entry:** merged and green on `$BASE`: T-002, T-006, T-008, T-010, T-012, T-013, T-014, T-024, T-026.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-016](tasks/T-016-wp-t1a-reading.md) | The prior workplan's T-1a: reading (notation arithmetic to one home; the writer refuses pr | 1 (chain, first) | TOOLING | READY | yes | T-008 | not piloted |
| [T-020](tasks/T-020-quantity-kind.md) | A parameter states what kind of quantity it is | 1 | TOOLING | READY | yes | T-010 | not piloted |
| [T-022](tasks/T-022-contract-re-entry.md) | Re-entry conditions in the pipeline contract | 2 | TOOLING | READY | yes | T-002, T-012, T-013 | not piloted |
| [T-025](tasks/T-025-base-writers.md) | Writers for the base tables a ruled task must write | 3 | TOOLING | READY | yes | T-024 | not piloted |
| [T-028](tasks/T-028-concept-identity.md) | A concept that is not an English string | 3 | TOOLING | NOT FOR SONNET | no | T-026 | not piloted |
| [T-034](tasks/T-034-cell-status-verb.md) | One read-only answer for a cell at every stage | 4 | TOOLING | READY | yes | T-013 | not piloted |
| [T-041](tasks/T-041-one-home-for-helpers.md) | One home for helpers defined twice | 0 (now) | TOOLING | READY | yes | T-014 | not piloted |
| [T-043](tasks/T-043-refusals-name-next-action.md) | Every refusal says what to do next | 0 (now) | TOOLING | READY | yes | T-014 | not piloted |
| [T-049](tasks/T-049-translation-home.md) | A typed home for translations, attached by pointer and callable from any stage | 2 | TOOLING | READY | yes | T-008 | not piloted |
| [T-050](tasks/T-050-retire-admission-edges-and-connections.md) | Admission edges and connections retire in place instead of being deleted | 2 | TOOLING | READY | yes | T-006 | not piloted |
| [T-107](tasks/T-107-attest-forms.md) | Attest forms per language and jurisdiction from instruments | research | RESEARCH | NOT FOR SONNET | no | T-026 | not piloted |
| [T-111](tasks/T-111-as-written-wording-for-stored-rows.md) | Bring the two stored spelled-out figures into line | research | RESEARCH | READY | yes | T-008 | not piloted |
| [T-113](tasks/T-113-file-sub-national-instruments.md) | File the four held sub-national instruments under their own codes | research | RESEARCH | READY | yes | T-024 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 2.1: T-016
- Lane 2.2: T-020
- Lane 2.3: T-022 → T-041 → T-043 → T-049 → T-050 — sequenced by a soft dependency or a chain of shared files
- Lane 2.4: T-025
- Lane 2.5: T-028
- Lane 2.6: T-034
- Lane 2.7: T-107
- Lane 2.8: T-111
- Lane 2.9: T-113

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-028, T-107.

## Batch 3

**Entry:** merged and green on `$BASE`: T-008, T-009, T-016, T-020, T-025, T-049.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-017](tasks/T-017-wp-t2-conditions.md) | The prior workplan's T-2: conditions become branches | 1 (chain) | TOOLING | READY | yes | T-016 | not piloted |
| [T-029](tasks/T-029-term-relations.md) | Typed pointers between terms | 4 | TOOLING | READY | yes | T-020 | not piloted |
| [T-030](tasks/T-030-units-as-data.md) | Units and their exact conversions as rows | 4 | TOOLING | READY | yes | T-016, T-020 | not piloted |
| [T-101](tasks/T-101-scope-fill.md) | Record the research scope on every pair | research | RESEARCH | OWNER: OD-01,OD-04 | no | T-025 | not piloted |
| [T-105](tasks/T-105-read-held-sources.md) | Read what is held, in full, against every parameter | research | RESEARCH | NOT FOR SONNET | no | T-008, T-009, T-016 | not piloted |
| [T-108](tasks/T-108-unit-condition-repair.md) | Move conditions out of the unit cell | research | RESEARCH | READY | yes | T-008, T-016 | not piloted |
| [T-109](tasks/T-109-parameter-kinds-data.md) | Give the live parameters their quantity kind | research | RESEARCH | NOT FOR SONNET | no | T-020 | not piloted |
| [T-112](tasks/T-112-translate-held-text.md) | Translate the held non-English text that synthesis needs | research | RESEARCH | READY | yes | T-049 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 3.1: T-017
- Lane 3.2: T-029
- Lane 3.3: T-030
- Lane 3.4: T-101
- Lane 3.5: T-105
- Lane 3.6: T-108
- Lane 3.7: T-109
- Lane 3.8: T-112

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-105, T-109; waiting on the owner: T-101 (OD-01/OD-04).

## Batch 4

**Entry:** merged and green on `$BASE`: T-015, T-017, T-020, T-024, T-025, T-029, T-030, T-050, T-101.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-018](tasks/T-018-link-table.md) | The link table for several codes of one model on a figure | 1 (chain) | TOOLING | NOT FOR SONNET | no | T-017 | not piloted |
| [T-032](tasks/T-032-synthesis-relations.md) | Relations synthesis can record, and what a synthesis row is | 4 | TOOLING | NOT FOR SONNET | no | T-029, T-050 | not piloted |
| [T-033](tasks/T-033-synthesis-candidates.md) | Candidate relations on demand (read-only) | 4 | TOOLING | READY | yes | T-029, T-030 | not piloted |
| [T-036](tasks/T-036-jurisdiction-comparison-view.md) | The jurisdiction comparison as a view | 5 | TOOLING | READY | after T-101 | T-024, T-101 | not piloted |
| [T-047](tasks/T-047-add-by-data-test.md) | A durable test that the base changes by data alone | 3 (end) | TOOLING | READY | yes | T-015, T-020, T-024, T-025, T-029 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 4.1: T-018
- Lane 4.2: T-032
- Lane 4.3: T-033
- Lane 4.4: T-036
- Lane 4.5: T-047

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-018, T-032.

## Batch 5

**Entry:** merged and green on `$BASE`: T-013, T-016, T-017, T-018, T-025, T-032.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-019](tasks/T-019-lens-gather.md) | The engine gathers by the lens tags on the figure (the prior workplan's T-3) | 1 (chain, last) | TOOLING | READY | after T-018 | T-016, T-017, T-018 | not piloted |
| [T-040](tasks/T-040-deletion-candidates-sweep.md) | Caller sweep for the deletion candidates | 5 | TOOLING | READY | after T-032 | T-013, T-032 | not piloted |
| [T-053](tasks/T-053-engine-conflict-between-groups.md) | Conflict between groups in the engine | 4 | TOOLING | NOT FOR SONNET | no | T-032 | not piloted |
| [T-102](tasks/T-102-mobility-split.md) | Execute the mobility split | research | RESEARCH | NOT FOR SONNET | no | T-018, T-025 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 5.1: T-019
- Lane 5.2: T-040
- Lane 5.3: T-053
- Lane 5.4: T-102

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-053, T-102.

## Batch 6

**Entry:** merged and green on `$BASE`: T-019, T-032, T-036, T-049, T-102, T-104.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-021](tasks/T-021-cell-question-gate.md) | A question about a published cell can be recorded and flags the cell | 2 | TOOLING | READY | after T-018 | T-019 | not piloted |
| [T-031](tasks/T-031-clause-unit-and-open-pass.md) | The clause as a unit, the open pass, and catalogue growth | 4 | TOOLING | NOT FOR SONNET | no | T-019 | not piloted |
| [T-037](tasks/T-037-render.md) | Render from the database | 5 | TOOLING | NOT FOR SONNET | no | T-019, T-032, T-036, T-049 | not piloted |
| [T-106](tasks/T-106-retag-lenses.md) | Tag figures with every relevant model | research | RESEARCH | NOT FOR SONNET | no | T-019 | not piloted |
| [T-110](tasks/T-110-first-determinations.md) | First live determinations | research | RESEARCH | NOT FOR SONNET | no | T-019, T-102, T-104 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 6.1: T-021
- Lane 6.2: T-031
- Lane 6.3: T-037
- Lane 6.4: T-106
- Lane 6.5: T-110

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-031, T-037, T-106, T-110.

## Batch 7

**Entry:** merged and green on `$BASE`: T-021, T-037.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-038](tasks/T-038-stage-pair-gate.md) | Register the stage-pair gate | 5 | TOOLING | READY | after T-018, T-032, T-037, T-101 | T-037 | not piloted |
| [T-039](tasks/T-039-owner-edits.md) | The owner's edits as proposals through the write path | 5 | TOOLING | NOT FOR SONNET | no | T-021, T-037 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 7.1: T-038
- Lane 7.2: T-039

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-039.

## Owner decision queue (what each answer releases)

Answer forms and options are in the register in `REMEDIATION-WORKPLAN.md` (grep `^### OD-`). An answer binds only once the ledger quotes it (`references/project-standards.md`).

| Decision | Releases | In batches |
|---|---|---|
| OD-01 | T-101 | 3 |
| OD-04 | T-101 | 3 |
| OD-14 | T-102 | 5 |
| OD-15 | T-103 | 1 |
| OD-19 | T-053 | 5 |
| OD-23 | T-031 | 6 |
| OD-28 | T-023 | 1 |

Decisions in the register that no task file lists as a precondition: OD-02, OD-03, OD-05, OD-06, OD-07, OD-08, OD-09, OD-10, OD-11, OD-12, OD-13, OD-17, OD-18, OD-20, OD-21, OD-22, OD-24, OD-25, OD-26, OD-27, OD-29, OD-30.

## NOT FOR SONNET

| Task | Title | Batch | Owner decisions |
|---|---|---|---|
| [T-018](tasks/T-018-link-table.md) | The link table for several codes of one model on a figure | 4 | — |
| [T-028](tasks/T-028-concept-identity.md) | A concept that is not an English string | 2 | — |
| [T-031](tasks/T-031-clause-unit-and-open-pass.md) | The clause as a unit, the open pass, and catalogue growth | 6 | OD-23 |
| [T-032](tasks/T-032-synthesis-relations.md) | Relations synthesis can record, and what a synthesis row is | 4 | — |
| [T-037](tasks/T-037-render.md) | Render from the database | 6 | — |
| [T-039](tasks/T-039-owner-edits.md) | The owner's edits as proposals through the write path | 7 | — |
| [T-053](tasks/T-053-engine-conflict-between-groups.md) | Conflict between groups in the engine | 5 | OD-19 |
| [T-102](tasks/T-102-mobility-split.md) | Execute the mobility split | 5 | OD-14 |
| [T-103](tasks/T-103-medical-lens.md) | Fill the medical lens by correspondence | 1 | OD-15 |
| [T-105](tasks/T-105-read-held-sources.md) | Read what is held, in full, against every parameter | 3 | — |
| [T-106](tasks/T-106-retag-lenses.md) | Tag figures with every relevant model | 6 | — |
| [T-107](tasks/T-107-attest-forms.md) | Attest forms per language and jurisdiction from instruments | 2 | — |
| [T-109](tasks/T-109-parameter-kinds-data.md) | Give the live parameters their quantity kind | 3 | — |
| [T-110](tasks/T-110-first-determinations.md) | First live determinations | 6 | — |

Each file says who does it. Everything that depends on one of these waits for it (the 'Reachable by Sonnet now' column names the blockers).

## Where the pilots stand

`grep -L "Not piloted" workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md` lists the tasks a pilot has touched. Results, defects found and what changed in the plan are in section 12 of `REMEDIATION-WORKPLAN.md` and in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/`.
