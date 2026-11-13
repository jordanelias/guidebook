# Remediation plan, in batches by dependency

_Generated 2026-11-13 05:03 UTC from the 73 task files at commit fa313c4 by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py`. Nothing below is typed in: re-run the generator (`python3 -I scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py`) after any task file changes, and trust the generator over this text (CLAUDE.md rule 7a)._

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
| 1 | 27 | 26 | 0 | 0 | 1 | 25 / 2 | 10 |
| 2 | 14 | 13 | 0 | 0 | 1 | 11 / 3 | 5 |
| 3 | 9 | 8 | 0 | 0 | 1 | 4 / 5 | 8 |
| 4 | 7 | 5 | 0 | 0 | 2 | 6 / 1 | 5 |
| 5 | 4 | 2 | 0 | 0 | 2 | 3 / 1 | 4 |
| 6 | 7 | 2 | 0 | 1 | 5 | 6 / 1 | 5 |
| 7 | 4 | 1 | 0 | 0 | 3 | 2 / 2 | 4 |
| 8 | 1 | 0 | 0 | 0 | 1 | 0 / 1 | 1 |

Counts are derived; the commands that check them: `ls workplan/2026-11-12-bidirectional-pipeline/tasks/T-[0-9]*-*.md | wc -l`, and the generator's own output.

**Longest dependency chain (8 tasks):** T-008 (READY) → T-016 (READY) → T-017 (READY) → T-018 (READY) → T-019 (READY) → T-055 (READY) → T-102 (NOT FOR SONNET) → T-110 (NOT FOR SONNET).

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
| [T-012](tasks/T-012-follow-up-reasons.md) | Follow-up reasons for a skimmed figure and an absence finding | 0 (now) | TOOLING | READY | yes | — | piloted |
| [T-013](tasks/T-013-typed-gaps.md) | A gap says what it is a gap in, and a search says which gap caused it | 0 (now) | TOOLING | READY | yes | — | piloted |
| [T-014](tasks/T-014-stress-harness-and-probes.md) | Keep the stress scripts as a characterisation harness and their probes as tests | 0 (now) | TOOLING | READY | yes | — | piloted |
| [T-015](tasks/T-015-language-fold.md) | Language codes folded at the writers and in the coverage views | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-023](tasks/T-023-ledger-relayed-statements.md) | Enter the relayed statements of 2026-10-12 in the ledger | 2 | TOOLING | READY | yes | — | not piloted |
| [T-024](tasks/T-024-jurisdiction-registry.md) | Jurisdictions in a table the writers read | 3 | TOOLING | READY | yes | — | piloted |
| [T-026](tasks/T-026-alias-attestation.md) | A form says how it is attested, and a search says which forms it used | 3 | TOOLING | READY | yes | — | piloted |
| [T-027](tasks/T-027-source-identity-edition.md) | The source's own title, edition and currency can be written | 3 | TOOLING | READY | yes | — | not piloted |
| [T-035](tasks/T-035-skills-repair.md) | Skills that describe the database that exists | 4 | TOOLING | READY | yes | — | not piloted |
| [T-042](tasks/T-042-derive-choices-and-counts.md) | Counts in the registry as commands, and one Layer 0 measure corrected | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-048](tasks/T-048-root-registry-writer.md) | A writer for the root registry | 2 | TOOLING | READY | yes | — | not piloted |
| [T-051](tasks/T-051-gap-register-cross-stage.md) | The gap register is marked cross-stage in the stage map | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-052](tasks/T-052-mining-stages-out-of-scope-leads.md) | Mining stages an out-of-scope source as a lead | 0 (now) | TOOLING | READY | yes | — | not piloted |
| [T-054](tasks/T-054-identity-retires-to-need.md) | An identity code can be retired to the access need that carries it | 2 | TOOLING | READY | yes | — | not piloted |
| [T-103](tasks/T-103-medical-lens.md) | Fill the medical lens by correspondence | research | RESEARCH | NOT FOR SONNET | no | — | not piloted |
| [T-104](tasks/T-104-verify-governing-sources.md) | Verify the sources a first determination would rest on | research | RESEARCH | READY | yes | — | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 1.1: T-001 → T-002 → T-003 → T-004 → T-006 → T-007 → T-008 → T-009 → T-010 → T-011 → T-012 → T-013 → T-015 → T-024 → T-026 → T-042 → T-051 → T-054 — sequenced by a soft dependency or a chain of shared files
- Lane 1.2: T-005
- Lane 1.3: T-014
- Lane 1.4: T-023
- Lane 1.5: T-027
- Lane 1.6: T-035
- Lane 1.7: T-048
- Lane 1.8: T-052
- Lane 1.9: T-103
- Lane 1.10: T-104

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-103.

## Batch 2

**Entry:** merged and green on `$BASE`: T-002, T-006, T-008, T-010, T-012, T-013, T-014, T-024, T-026, T-051, T-054.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-016](tasks/T-016-wp-t1a-reading.md) | The prior workplan's T-1a: reading (notation arithmetic to one home; the writer refuses pr | 1 (chain, first) | TOOLING | READY | yes | T-008, T-014 | piloted |
| [T-020](tasks/T-020-quantity-kind.md) | A parameter states what kind of quantity it is | 1 | TOOLING | READY | yes | T-010 | piloted |
| [T-022](tasks/T-022-contract-re-entry.md) | Re-entry conditions in the pipeline contract | 2 | TOOLING | READY | yes | T-002, T-012, T-013 | not piloted |
| [T-025](tasks/T-025-base-writers.md) | Writers for the base tables a ruled task must write | 3 | TOOLING | READY | yes | T-024 | piloted |
| [T-028](tasks/T-028-concept-identity.md) | A concept that is not an English string | 3 | TOOLING | NOT FOR SONNET | no | T-026 | piloted |
| [T-034](tasks/T-034-cell-status-verb.md) | One read-only answer for a cell at every stage | 4 | TOOLING | READY | yes | T-013 | not piloted |
| [T-041](tasks/T-041-one-home-for-helpers.md) | One home for helpers defined twice | 0 (now) | TOOLING | READY | yes | T-014 | not piloted |
| [T-043](tasks/T-043-refusals-name-next-action.md) | Every refusal says what to do next | 0 (now) | TOOLING | READY | yes | T-014 | not piloted |
| [T-049](tasks/T-049-translation-home.md) | A typed home for translations, attached by pointer and callable from any stage | 2 | TOOLING | READY | yes | T-008, T-051 | piloted |
| [T-050](tasks/T-050-retire-admission-edges-and-connections.md) | Admission edges and connections retire in place instead of being deleted | 2 | TOOLING | READY | yes | T-006 | not piloted |
| [T-056](tasks/T-056-all-leaves-identity-lens.md) | ALL leaves the identity lens: universal is stated once, by design_scale | 2 | TOOLING | READY | yes | T-054 | not piloted |
| [T-111](tasks/T-111-as-written-wording-for-stored-rows.md) | Bring the two stored spelled-out figures into line | research | RESEARCH | READY | yes | T-008 | not piloted |
| [T-113](tasks/T-113-file-sub-national-instruments.md) | File the four held sub-national instruments under their own codes | research | RESEARCH | READY | yes | T-024 | not piloted |
| [T-114](tasks/T-114-retire-move-ves-to-needs.md) | Retire MOVE and VES to the access needs that carry them | research | RESEARCH | READY | yes | T-054 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 2.1: T-016 → T-020 → T-022 → T-025 → T-028 → T-041 → T-043 → T-049 → T-050 → T-056 — sequenced by a soft dependency or a chain of shared files
- Lane 2.2: T-034
- Lane 2.3: T-111
- Lane 2.4: T-113
- Lane 2.5: T-114

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-028.

## Batch 3

**Entry:** merged and green on `$BASE`: T-008, T-014, T-016, T-020, T-025, T-026, T-028, T-049, T-054.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-017](tasks/T-017-wp-t2-conditions.md) | The prior workplan's T-2: conditions become branches | 1 (chain) | TOOLING | READY | yes | T-008, T-014, T-016 | piloted |
| [T-029](tasks/T-029-term-relations.md) | Typed pointers between terms | 4 | TOOLING | READY | yes | T-020 | not piloted |
| [T-030](tasks/T-030-units-as-data.md) | Units and their exact conversions as rows | 4 | TOOLING | READY | yes | T-016, T-020 | not piloted |
| [T-057](tasks/T-057-base-coverage-view.md) | The base coverage view: one state per concept and in-scope pair | 3 | TOOLING | READY | after T-028 | T-026, T-028 | not piloted |
| [T-101](tasks/T-101-scope-fill.md) | Record the research scope on every pair | research | RESEARCH | READY | yes | T-025 | not piloted |
| [T-108](tasks/T-108-unit-condition-repair.md) | Move conditions out of the unit cell | research | RESEARCH | READY | yes | T-008, T-016 | not piloted |
| [T-109](tasks/T-109-parameter-kinds-data.md) | Give the live parameters their quantity kind | research | RESEARCH | NOT FOR SONNET | no | T-020 | not piloted |
| [T-112](tasks/T-112-translate-held-text.md) | Translate the held non-English text that synthesis needs | research | RESEARCH | READY | yes | T-049 | not piloted |
| [T-116](tasks/T-116-upl-for-upper-limb.md) | Hold the upper-limb population as UPL, and retire LMB to it | research | RESEARCH | READY | yes | T-025, T-054 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 3.1: T-017
- Lane 3.2: T-029 → T-030 — share `governance/context-map.yaml`
- Lane 3.3: T-057
- Lane 3.4: T-101
- Lane 3.5: T-108
- Lane 3.6: T-109
- Lane 3.7: T-112
- Lane 3.8: T-116

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-109.

## Batch 4

**Entry:** merged and green on `$BASE`: T-015, T-017, T-020, T-024, T-025, T-026, T-028, T-029, T-030, T-050, T-057, T-101, T-116.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-018](tasks/T-018-link-table.md) | The link table for several codes of one model on a figure | 1 (chain) | TOOLING | READY | yes | T-017 | piloted |
| [T-032](tasks/T-032-synthesis-relations.md) | Relations synthesis can record, and what a synthesis row is | 4 | TOOLING | NOT FOR SONNET | no | T-029, T-050 | not piloted |
| [T-033](tasks/T-033-synthesis-candidates.md) | Candidate relations on demand (read-only) | 4 | TOOLING | READY | yes | T-029, T-030 | not piloted |
| [T-036](tasks/T-036-jurisdiction-comparison-view.md) | The jurisdiction comparison as a view | 5 | TOOLING | READY | yes | T-024, T-101 | not piloted |
| [T-047](tasks/T-047-add-by-data-test.md) | A durable test that the base changes by data alone | 3 (end) | TOOLING | READY | yes | T-015, T-020, T-024, T-025, T-029 | not piloted |
| [T-058](tasks/T-058-upl-prose-callers.md) | UPL reinstated for upper limb: the retired crosswalk and the prose that names LMB or UPL | 3 | TOOLING | READY | yes | T-116 | not piloted |
| [T-107](tasks/T-107-attest-forms.md) | Attest forms per language and jurisdiction from instruments | research | RESEARCH | NOT FOR SONNET | no | T-026, T-028, T-057 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 4.1: T-018 → T-032 → T-036 — share `governance/context-map.yaml`
- Lane 4.2: T-033
- Lane 4.3: T-047
- Lane 4.4: T-058
- Lane 4.5: T-107

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-032, T-107.

## Batch 5

**Entry:** merged and green on `$BASE`: T-013, T-016, T-017, T-018, T-032, T-056.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-019](tasks/T-019-lens-gather.md) | The engine gathers by the lens tags on the figure (the prior workplan's T-3) | 1 (chain, last) | TOOLING | READY | yes | T-016, T-017, T-018 | piloted |
| [T-040](tasks/T-040-deletion-candidates-sweep.md) | Caller sweep for the deletion candidates | 5 | TOOLING | READY | after T-032 | T-013, T-032 | not piloted |
| [T-053](tasks/T-053-engine-conflict-between-groups.md) | Conflict between groups in the engine | 4 | TOOLING | NOT FOR SONNET | no | T-032 | not piloted |
| [T-115](tasks/T-115-retag-all-rows.md) | Re-tag the figures filed under ALL by their heading's group, then retire ALL | research | RESEARCH | NOT FOR SONNET | no | T-018, T-056 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 5.1: T-019
- Lane 5.2: T-040
- Lane 5.3: T-053
- Lane 5.4: T-115

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-053, T-115.

## Batch 6

**Entry:** merged and green on `$BASE`: T-016, T-019, T-029, T-032, T-036, T-049.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-021](tasks/T-021-cell-question-gate.md) | A question about a published cell can be recorded and flags the cell | 2 | TOOLING | READY | yes | T-019 | not piloted |
| [T-031](tasks/T-031-clause-unit-and-open-pass.md) | The clause as a unit, the open pass, and catalogue growth | 4 | TOOLING | NOT FOR SONNET | no | T-019 | not piloted |
| [T-037](tasks/T-037-render.md) | Render from the database | 5 | TOOLING | NOT FOR SONNET | no | T-019, T-032, T-036, T-049 | not piloted |
| [T-055](tasks/T-055-mobility-family-tooling.md) | Tooling for the mobility family: the devices it needs, and a parent's determination that g | 4 | TOOLING | READY | yes | T-019 | not piloted |
| [T-059](tasks/T-059-wp-t4-agreement.md) | The prior workplan's T-4: agreement (true exclusion causes, recorded divergence, the fragi | 1 (chain, after T-019) | TOOLING | NOT FOR SONNET | no | T-016, T-019 | not piloted |
| [T-060](tasks/T-060-element-determination.md) | The specifications pass writes an element-level determination (OR-14b) | 5 (after T-029 and T-019) | TOOLING | DESIGN: T-060-design.md; NOT FOR SONNET | no | T-019, T-029 | not piloted |
| [T-106](tasks/T-106-retag-lenses.md) | Tag figures with every relevant model | research | RESEARCH | NOT FOR SONNET | no | T-019 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 6.1: T-021 → T-031 — share `governance/context-map.yaml`
- Lane 6.2: T-037
- Lane 6.3: T-055 → T-059 — share `scripts/assess/assess_cell.py`
- Lane 6.4: T-060
- Lane 6.5: T-106

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-031, T-037, T-059, T-060, T-106; a design file missing: T-060 (T-060-design.md).

## Batch 7

**Entry:** merged and green on `$BASE`: T-008, T-009, T-016, T-018, T-021, T-025, T-031, T-037, T-054, T-055.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-038](tasks/T-038-stage-pair-gate.md) | Register the stage-pair gate | 5 | TOOLING | READY | after T-032, T-037 | T-037 | not piloted |
| [T-039](tasks/T-039-owner-edits.md) | The owner's edits as proposals through the write path | 5 | TOOLING | NOT FOR SONNET | no | T-021, T-037 | not piloted |
| [T-102](tasks/T-102-mobility-split.md) | Decompose the mobility family by device, and carry the rows filed under MOB | research | RESEARCH | NOT FOR SONNET | no | T-018, T-025, T-054, T-055 | not piloted |
| [T-105](tasks/T-105-read-held-sources.md) | Read what is held, in full, against every parameter | research | RESEARCH | NOT FOR SONNET | no | T-008, T-009, T-016, T-031 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 7.1: T-038
- Lane 7.2: T-039
- Lane 7.3: T-102
- Lane 7.4: T-105

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-039, T-102, T-105.

## Batch 8

**Entry:** merged and green on `$BASE`: T-019, T-059, T-102, T-104.

| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |
|---|---|---|---|---|---|---|---|
| [T-110](tasks/T-110-first-determinations.md) | First live determinations | research | RESEARCH | NOT FOR SONNET | no | T-019, T-059, T-102, T-104 | not piloted |

**Lanes** (parallel across, serial within; the shared file is the reason):

- Lane 8.1: T-110

**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base "$BASE" --explain` is green on `$BASE`. **Stops in this batch:** not for Sonnet: T-110.

## Owner decision queue, read from the ledger (what each answer releases)

Every register decision (`grep -o -E '^### OD-[0-9]+' REMEDIATION-WORKPLAN.md`), its state by the ledger gate (the last `OD-NN STATUS:` and `OD-NN CHECK:` lines of `references/project-standards.md`), the tasks whose section 2 names it, and every task that waits on those through the hard dependencies. A decision named in a task's 'Owner decisions' bullet opens that task only on the owner's answer; one named in its 'Delegated resolutions' bullet opens on a delegated resolution whose check is not required or confirmed. The phone-ready prompts for the CLOSED ones are in `DECISION-CLOSURE.md`.

### Blocking: CLOSED, and a task's gate reads it (0)

| Decision | Gate | Tasks it holds | Waiting on those (hard dependencies) | In batches |
|---|---|---|---|---|

### Standing, blocks no task: CLOSED, and no task's gate reads it (1)

OD-17 (DEFERRED BY THE OWNER)

### Open by the ledger gate (37)

| Decision | Gate | Read by |
|---|---|---|
| OD-01 | OPEN (delegated; confirmed with corrections applied) | T-024, T-036, T-101, T-113 |
| OD-02 | OPEN (delegated; confirmed with corrections applied) | T-037, T-112 |
| OD-03 | OPEN (delegated; not required) | T-028 |
| OD-04 | OPEN (owner) | T-024, T-052, T-101, T-113 |
| OD-05 | OPEN (delegated; not required) | T-052, T-105 |
| OD-06 | OPEN (delegated; not required) | T-106 |
| OD-07 | OPEN (delegated; not required) | T-032 |
| OD-08 | OPEN (delegated; not required) | T-019, T-022, T-037 |
| OD-09 | OPEN (owner) | no task gate |
| OD-10 | OPEN (owner) | no task gate |
| OD-11 | OPEN (delegated; not required) | T-051 |
| OD-12 | OPEN (delegated; confirmed with corrections applied) | T-032, T-037 |
| OD-13 | OPEN (owner) | no task gate |
| OD-14 | OPEN (owner) | T-055, T-102 |
| OD-15 | OPEN (owner) | T-103 |
| OD-18 | OPEN (delegated; not required) | T-022 |
| OD-19 | OPEN (owner) | T-032, T-053 |
| OD-20 | OPEN (delegated; not required) | T-039 |
| OD-21 | OPEN (delegated; not required) | T-021 |
| OD-22 | OPEN (delegated; not required) | T-030 |
| OD-23 | OPEN (owner) | T-031 |
| OD-24 | OPEN (delegated; not required) | T-020, T-030, T-109 |
| OD-25 | OPEN (delegated; not required) | T-032 |
| OD-26 | OPEN (delegated; not required) | T-038 |
| OD-27 | OPEN (owner) | no task gate |
| OD-28 | OPEN (owner) | T-023 |
| OD-29 | OPEN (delegated; not required) | T-032, T-050 |
| OD-30 | OPEN (delegated; not required) | T-037, T-049, T-112 |
| OD-31 | OPEN (owner) | T-056, T-102, T-115 |
| OD-32 | OPEN (owner) | no task gate |
| OD-33 | OPEN (delegated; not required) | T-037 |
| OD-34 | OPEN (owner) | T-052 |
| OD-35 | OPEN (owner) | no task gate |
| OD-36 | OPEN (owner) | T-053 |
| OD-37 | OPEN (owner) | T-054, T-102, T-114 |
| OD-38 | OPEN (owner) | T-028 |
| OD-39 | OPEN (owner) | T-018 |

## NOT FOR SONNET

| Task | Title | Batch | Decisions (owner's words / delegated) |
|---|---|---|---|
| [T-028](tasks/T-028-concept-identity.md) | A concept that is not an English string | 2 | OD-38 / OD-03 |
| [T-031](tasks/T-031-clause-unit-and-open-pass.md) | The clause as a unit, the open pass, and catalogue growth | 6 | OD-23 / — |
| [T-032](tasks/T-032-synthesis-relations.md) | Relations synthesis can record, and what a synthesis row is | 4 | — / OD-07, OD-12, OD-19, OD-25, OD-29 |
| [T-037](tasks/T-037-render.md) | Render from the database | 6 | — / OD-02, OD-08, OD-12, OD-30, OD-33 |
| [T-039](tasks/T-039-owner-edits.md) | The owner's edits as proposals through the write path | 7 | — / OD-20 |
| [T-053](tasks/T-053-engine-conflict-between-groups.md) | Conflict between groups in the engine | 5 | OD-19, OD-36 / — |
| [T-059](tasks/T-059-wp-t4-agreement.md) | The prior workplan's T-4: agreement (true exclusion causes, recorded divergence, | 6 | — / — |
| [T-060](tasks/T-060-element-determination.md) | The specifications pass writes an element-level determination (OR-14b) | 6 | — / — |
| [T-102](tasks/T-102-mobility-split.md) | Decompose the mobility family by device, and carry the rows filed under MOB | 7 | OD-14, OD-31, OD-37 / — |
| [T-103](tasks/T-103-medical-lens.md) | Fill the medical lens by correspondence | 1 | OD-15 / — |
| [T-105](tasks/T-105-read-held-sources.md) | Read what is held, in full, against every parameter | 7 | — / OD-05 |
| [T-106](tasks/T-106-retag-lenses.md) | Tag figures with every relevant model | 6 | — / OD-06 |
| [T-107](tasks/T-107-attest-forms.md) | Attest forms per language and jurisdiction from instruments | 4 | — / — |
| [T-109](tasks/T-109-parameter-kinds-data.md) | Give the live parameters their quantity kind | 3 | — / OD-24 |
| [T-110](tasks/T-110-first-determinations.md) | First live determinations | 8 | — / — |
| [T-115](tasks/T-115-retag-all-rows.md) | Re-tag the figures filed under ALL by their heading's group, then retire ALL | 5 | OD-31 / — |

Each file says who does it. Everything that depends on one of these waits for it (the 'Reachable by Sonnet now' column names the blockers).

## Where the pilots stand

`grep -L "Not piloted" workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md` lists the tasks a pilot has touched. Results, defects found and what changed in the plan are in section 12 of `REMEDIATION-WORKPLAN.md` and in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/`.
