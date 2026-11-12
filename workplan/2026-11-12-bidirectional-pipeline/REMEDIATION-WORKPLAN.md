# Remediation workplan: a pipeline that runs in every direction, at any stage, across languages and jurisdictions

_Written 2026-11-12 (UTC) by the handshake-and-adversarial leg of the bidirectional-pipeline audit. Planning only: no script, schema, governance file or database row was changed in writing it. Canadian English. Every figure is given as the command that produces it; re-run the command, do not trust a number._

## 0. Verdict

**The owner's objective is not met today, and it can be met.** The objective (`grep -n -F "run in all directions" references/project-standards.md`): the pipeline "can be run in all directions at any stage in such a manner where we can dynamically research, adjudicate, synthesize, specify and render across a multitude of languages and jurisdictions". Three later statements of the same day add that the code be "efficient and centralized and clean", that the pipeline be flexible, glossed by the owner as having no "hard coded behaviours", and that it have no dead ends (`grep -n -E "^## Owner statement 2026-11-12" references/project-standards.md`).

What stands in the way, in order of harm to the book:

1. **A determination is computed without regard to the group it is for.** The engine gathers evidence by parameter alone. Fixed by the chain [T-016](tasks/T-016-wp-t1a-reading.md) → [T-017](tasks/T-017-wp-t2-conditions.md) → [T-018](tasks/T-018-link-table.md) → [T-019](tasks/T-019-lens-gather.md).
2. **Guards that a wrong figure or a misquote should not pass, pass it**: the number check, the quote and name checks outside Latin script, a source admitted with no verification standing. [T-008](tasks/T-008-claimed-number-check.md), [T-009](tasks/T-009-script-aware-guards.md), [T-007](tasks/T-007-add-source-standing.md).
3. **The mobility group the owner split is still one code**, and most figures sit on it. [T-102](tasks/T-102-mobility-split.md) (owner decision OD-14).
4. **Nothing exists at render**, so every stage pair ending there has no path. [T-037](tasks/T-037-render.md), [T-038](tasks/T-038-stage-pair-gate.md) (owner decisions).
5. **The base is English-shaped and its scope is in no table**: jurisdictions in code, scope unrecorded, forms unattested. [T-024](tasks/T-024-jurisdiction-registry.md), [T-025](tasks/T-025-base-writers.md), [T-026](tasks/T-026-alias-attestation.md), [T-101](tasks/T-101-scope-fill.md), [T-028](tasks/T-028-concept-identity.md).
6. **A step backward leaves no typed cause**: a gap does not say what it is a gap in. [T-013](tasks/T-013-typed-gaps.md), [T-012](tasks/T-012-follow-up-reasons.md), [T-022](tasks/T-022-contract-re-entry.md).
7. **A source must be re-read for every later parameter, parameters are flat, and synthesis finds nothing.** [T-031](tasks/T-031-clause-unit-and-open-pass.md), [T-029](tasks/T-029-term-relations.md), [T-032](tasks/T-032-synthesis-relations.md), [T-033](tasks/T-033-synthesis-candidates.md) (owner decisions).

**Start now:** the tasks of Wave 0 need no owner decision, no design and no earlier wave (section 4). **Then stop for the owner** at the points listed in section 6; the questions are in section 8, each with a one-line answer form.

## 1. What this folder holds, and which file governs

| File | What it is |
|---|---|
| `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md` | This index: order, dependencies, stop points, the owner decision register, the Definition of Done. |
| `workplan/2026-11-12-bidirectional-pipeline/tasks/T-<id>-<slug>.md` | One file per task, self-contained. Count them: `ls workplan/2026-11-12-bidirectional-pipeline/tasks/T-[0-9]*-*.md | grep -v -- -design | wc -l`. Ids are not contiguous (the hundreds are research tasks; unused numbers mean nothing). |
| `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md` | The evidence base, requirement by requirement. **Where it differs from `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md`, the corrections file governs.** One example: its headline that a wrong-group determination "passes every gate" is false; the blocking integrity check stops it for unverified governing sources, though for the wrong reason. |
| `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/` | The audit: `hs-handshake-matrix.md` (verdict per requirement), `hs-adversarial-findings.md`, `hs-improvement-programme.md` (each IMP entry, the acceptance tests, the final recommendations in §8 and the code-quality, flexibility and dead-end findings in §9), `hs-stress-audit.md` (three rounds of stress tests), `fa-corrections-for-suite.md`. A task file never requires you to open these. |
| `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/stress/` | The stress scripts and their logs, kept as a characterisation harness (`RETAINED.md` says what is kept and why). |

The seven further suite documents first planned are not written; the owner dropped that plan in favour of this one.

## 2. How to execute

1. **One task, one session, one pull request.** Pick the next task by section 4 or 5. Open its file. Read `CLAUDE.md`. Do exactly what the file says, in its order: preconditions, evidence, change, sweep, verification, commit, adversarial pass, pull request last.
2. **One pull request merges at a time** (the prior workplan's rule WR-1: `grep -n "WR-1" workplan/2026-10-23-pipeline-resolution-workplan.md`). Branches may be prepared side by side; each later one takes the merged predecessor with `git merge origin/main` and derives its migration number again. Merging is the owner's act unless the owner has said otherwise; an executor does not merge its own pull request and does not watch it (CLAUDE.md rule 9).
3. **Tooling before research, never together** (CLAUDE.md rule 10). A research task starts only when the tooling it names is on `main`.
4. **A task that is `NOT FOR SONNET`** waits for the Fable implementation agent (design) or an Opus-class session (judgment), as its first line says. The owner authorised the Fable agent to "design, author, curate, orchestrate, delete as required" for code, schema, scripts, checks and skills (`grep -n -F "design, author, curate, orchestrate" references/project-standards.md`); doctrine stays with the owner.
5. **When a task stops**, it reports what it ran, what it saw and what it expected, and changes nothing further. A stop is a result, not a failure. Do not work around it.
6. **When the ground has moved** (a task's evidence command no longer gives the output the file states), the task stops. Either the defect is already fixed, or an earlier merge changed the facts; the orchestrating session re-reads the task against `main` before anyone resumes it.
7. **Nothing in this plan loosens a refusal the project holds on purpose.** The two refusals CLAUDE.md §4 says must stay absent stay absent.

## 3. All tasks

Generated from the task files; regenerate the same view with `grep -h -E "^\| (Task|Wave|Kind|Executor) " workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md`.

| Task | Title | Wave | Layer | Kind | Executor | Needs merged first | Owner decisions |
|---|---|---|---|---|---|---|---|
| [T-001](tasks/T-001-layer0-marks-and-text.md) | Mark what is superseded, and make the Layer 0 commands run as written | 0 (now) | 0 | TOOLING | Sonnet | none | none |
| [T-002](tasks/T-002-contract-entry-text.md) | Make the contract entries say what the owner's stage order says | 0 (now) | 1 | TOOLING | Sonnet | none | none |
| [T-003](tasks/T-003-owner-queue-answered-marks.md) | One home for "answered" in the owner queue | 0 (now) | 0 | TOOLING | Sonnet | none | none |
| [T-004](tasks/T-004-spec-checks-report-live-rows.md) | Specification checks say how many of the rows they read are live | 0 (now) | 0 | TOOLING | Sonnet | none | none |
| [T-005](tasks/T-005-retired-row-view-fixture.md) | A seeded test that a retired determination is surfaced by no determination view | 0 (now) | 0 | TOOLING | Sonnet | none | none |
| [T-006](tasks/T-006-delete-connection-refusal.md) | `delete-connection` refuses an id that is not a row | 0 (now) | 2 | TOOLING | Sonnet | none | none |
| [T-007](tasks/T-007-add-source-standing.md) | `add-source` writes a verification standing and a source type, or refuses | 0 (now) | 2 | TOOLING | Sonnet | none | none |
| [T-008](tasks/T-008-claimed-number-check.md) | The claimed number is checked as a number | 0 (now) | 2 | TOOLING | Sonnet | none (coordinate with T-016 if it is open: both touch the extraction writer) | none |
| [T-009](tasks/T-009-script-aware-guards.md) | Quote and name guards that work outside Latin script | 0 (now) | 2 | TOOLING | Sonnet | none (after T-008 if both are open, to avoid conflicting edits) | none |
| [T-010](tasks/T-010-add-parameter-domain-refusal.md) | `add-parameter` refuses a term that is not a design quantity (first step) | 0 (now) | 2 | TOOLING | Sonnet | none | none |
| [T-011](tasks/T-011-supersession-pointer.md) | Re-determining a cell points the retired row at its successor | 0 (now) | 2 | TOOLING | Sonnet | none | none |
| [T-012](tasks/T-012-follow-up-reasons.md) | Follow-up reasons for a skimmed figure and an absence finding | 0 (now) | 2 | TOOLING | Sonnet | none | none |
| [T-013](tasks/T-013-typed-gaps.md) | A gap says what it is a gap in, and a search says which gap caused it | 0 (now) | 1-2 | TOOLING | Sonnet | none | none |
| [T-014](tasks/T-014-stress-harness-and-probes.md) | Keep the stress scripts as a characterisation harness and their probes as tests | 0 (now) | 0 | TOOLING | Sonnet | none | none |
| [T-015](tasks/T-015-language-fold.md) | Language codes folded at the writers and in the coverage views | 0 (now) | 2 | TOOLING | Sonnet | none | none |
| [T-016](tasks/T-016-wp-t1a-reading.md) | The prior workplan's T-1a: reading (notation arithmetic to one home; the writer refuses prose units) | 1 (chain, first) | 2 | TOOLING | Sonnet | T-008 merged (both change the extraction writer) | none |
| [T-017](tasks/T-017-wp-t2-conditions.md) | The prior workplan's T-2: conditions become branches | 1 (chain) | 2 | TOOLING | Sonnet | T-016 merged | none |
| [T-018](tasks/T-018-link-table.md) | The link table for several codes of one model on a figure | 1 (chain) | 1 | TOOLING | NOT FOR SONNET | T-017 merged; `T-018-design.md` present | none |
| [T-019](tasks/T-019-lens-gather.md) | The engine gathers by the lens tags on the figure (the prior workplan's T-3) | 1 (chain, last) | 2 | TOOLING | Sonnet | T-016, T-017, T-018 merged | OD-08 |
| [T-020](tasks/T-020-quantity-kind.md) | A parameter states what kind of quantity it is | 1 | 1-2 | TOOLING | Sonnet | T-010 merged | OD-24 |
| [T-021](tasks/T-021-cell-question-gate.md) | A question about a published cell can be recorded and flags the cell | 2 | 2 | TOOLING | Sonnet | T-019 merged | OD-21 |
| [T-022](tasks/T-022-contract-re-entry.md) | Re-entry conditions in the pipeline contract | 2 | 1 | TOOLING | Sonnet | T-002, T-012, T-013 merged | OD-18 |
| [T-023](tasks/T-023-ledger-relayed-statements.md) | Enter the relayed statements of 2026-10-12 in the ledger | 2 | 0 | TOOLING | Sonnet | none | OD-28 |
| [T-024](tasks/T-024-jurisdiction-registry.md) | Jurisdictions in a table the writers read | 3 | 1 | TOOLING | Sonnet | none | OD-01 |
| [T-025](tasks/T-025-base-writers.md) | Writers for the base tables a ruled task must write | 3 | 2 | TOOLING | Sonnet | T-024 merged | none |
| [T-026](tasks/T-026-alias-attestation.md) | A form says how it is attested, and a search says which forms it used | 3 | 1-2 | TOOLING | Sonnet | none | none |
| [T-027](tasks/T-027-source-identity-edition.md) | The source's own title, edition and currency can be written | 3 | 2 | TOOLING | Sonnet | none | none |
| [T-028](tasks/T-028-concept-identity.md) | A concept that is not an English string | 3 | 1 | TOOLING | NOT FOR SONNET | T-026 merged | OD-03 |
| [T-029](tasks/T-029-term-relations.md) | Typed pointers between terms | 4 | 1 | TOOLING | Sonnet | T-020 merged | none |
| [T-030](tasks/T-030-units-as-data.md) | Units and their exact conversions as rows | 4 | 1-2 | TOOLING | Sonnet | T-016, T-020 merged | OD-22 |
| [T-031](tasks/T-031-clause-unit-and-open-pass.md) | The clause as a unit, the open pass, and catalogue growth | 4 | 1-2 | TOOLING | NOT FOR SONNET | T-019 merged | OD-23 |
| [T-032](tasks/T-032-synthesis-relations.md) | Relations synthesis can record, and what a synthesis row is | 4 | 1 | TOOLING | NOT FOR SONNET | T-029 merged | OD-07, OD-25, OD-19, OD-29 |
| [T-033](tasks/T-033-synthesis-candidates.md) | Candidate relations on demand (read-only) | 4 | 2 | TOOLING | Sonnet | T-029, T-030 merged | none |
| [T-034](tasks/T-034-cell-status-verb.md) | One read-only answer for a cell at every stage | 4 | 2 | TOOLING | Sonnet | T-013 merged | none |
| [T-035](tasks/T-035-skills-repair.md) | Skills that describe the database that exists | 4 | 2 | TOOLING | Sonnet | none for token corrections | none |
| [T-036](tasks/T-036-jurisdiction-comparison-view.md) | The jurisdiction comparison as a view | 5 | 1 | TOOLING | Sonnet | T-024 merged; T-101 merged | OD-01 |
| [T-037](tasks/T-037-render.md) | Render from the database | 5 | 2 | TOOLING | NOT FOR SONNET | T-019, T-036 merged | OD-02, OD-08, OD-12 |
| [T-038](tasks/T-038-stage-pair-gate.md) | Register the stage-pair gate | 5 | 0 | TOOLING | Sonnet | T-037 merged (a render view mapped to the render stage) | OD-26 |
| [T-039](tasks/T-039-owner-edits.md) | The owner's edits as proposals through the write path | 5 | 2 | TOOLING | NOT FOR SONNET | T-037 merged | OD-20 |
| [T-040](tasks/T-040-deletion-candidates-sweep.md) | Caller sweep for the deletion candidates | 5 | 2 | TOOLING | Sonnet | T-013, T-032 merged | none |
| [T-041](tasks/T-041-one-home-for-helpers.md) | One home for helpers defined twice | 0 (now) | 2 | TOOLING | Sonnet | T-014 merged (the harness is the proof) | none |
| [T-042](tasks/T-042-derive-choices-and-counts.md) | Counts in the registry as commands, and one Layer 0 measure corrected | 0 (now) | 0-2 | TOOLING | Sonnet | none | none |
| [T-043](tasks/T-043-refusals-name-next-action.md) | Every refusal says what to do next | 0 (now) | 2 | TOOLING | Sonnet | T-014 merged | none |
| [T-047](tasks/T-047-add-by-data-test.md) | A durable test that the base changes by data alone | 3 (end) | 0 | TOOLING | Sonnet | T-015, T-020, T-024, T-025, T-029 merged | none |
| [T-048](tasks/T-048-root-registry-writer.md) | A writer for the root registry | 2 | 2 | TOOLING | Sonnet | none | none |
| [T-101](tasks/T-101-scope-fill.md) | Record the research scope on every pair | research | 3 | RESEARCH | Sonnet | T-025 merged | OD-04 |
| [T-102](tasks/T-102-mobility-split.md) | Execute the mobility split | research | 3 | RESEARCH | NOT FOR SONNET | T-018, T-025 merged | OD-14 |
| [T-103](tasks/T-103-medical-lens.md) | Fill the medical lens by correspondence | research | 3 | RESEARCH | NOT FOR SONNET | none (`add-medical` exists) | OD-15 |
| [T-104](tasks/T-104-verify-governing-sources.md) | Verify the sources a first determination would rest on | research | 3 | RESEARCH | Sonnet | none | none |
| [T-105](tasks/T-105-read-held-sources.md) | Read what is held, in full, against every parameter | research | 3 | RESEARCH | NOT FOR SONNET | T-008, T-009, T-016 merged; T-031 if OD-23 chose an inventory | none |
| [T-106](tasks/T-106-retag-lenses.md) | Tag figures with every relevant model | research | 3 | RESEARCH | NOT FOR SONNET | T-019 merged | none |
| [T-107](tasks/T-107-attest-forms.md) | Attest forms per language and jurisdiction from instruments | research | 3 | RESEARCH | NOT FOR SONNET | T-026 merged | none |
| [T-108](tasks/T-108-unit-condition-repair.md) | Move conditions out of the unit cell | research | 3 | RESEARCH | Sonnet | T-016 merged | none |
| [T-109](tasks/T-109-parameter-kinds-data.md) | Give the live parameters their quantity kind | research | 3 | RESEARCH | NOT FOR SONNET | T-020 merged | none |
| [T-110](tasks/T-110-first-determinations.md) | First live determinations | research | 3 | RESEARCH | NOT FOR SONNET | T-019, T-102, T-104 merged | none |

## 4. Wave 0: what can start now

**No owner decision, no design, no earlier wave.** The set, by command: `grep -l "^| Wave | 0 (now) |" workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md`. Today that is: [T-001](tasks/T-001-layer0-marks-and-text.md), [T-002](tasks/T-002-contract-entry-text.md), [T-003](tasks/T-003-owner-queue-answered-marks.md), [T-004](tasks/T-004-spec-checks-report-live-rows.md), [T-005](tasks/T-005-retired-row-view-fixture.md), [T-006](tasks/T-006-delete-connection-refusal.md), [T-007](tasks/T-007-add-source-standing.md), [T-008](tasks/T-008-claimed-number-check.md), [T-009](tasks/T-009-script-aware-guards.md), [T-010](tasks/T-010-add-parameter-domain-refusal.md), [T-011](tasks/T-011-supersession-pointer.md), [T-012](tasks/T-012-follow-up-reasons.md), [T-013](tasks/T-013-typed-gaps.md), [T-014](tasks/T-014-stress-harness-and-probes.md), [T-015](tasks/T-015-language-fold.md), [T-041](tasks/T-041-one-home-for-helpers.md), [T-042](tasks/T-042-derive-choices-and-counts.md), [T-043](tasks/T-043-refusals-name-next-action.md).

**Merge order** (one at a time; the reason is in brackets):

1. [T-014](tasks/T-014-stress-harness-and-probes.md) (first: it repairs the stress harness that later tasks use to prove that behaviour is preserved)
2. [T-008](tasks/T-008-claimed-number-check.md) (on the critical path: the chain to the lens fix starts after it, and it closes the gravest guard)
3. [T-041](tasks/T-041-one-home-for-helpers.md) (a reduction; needs the harness)
4. [T-007](tasks/T-007-add-source-standing.md) (a writer refusal)
5. [T-009](tasks/T-009-script-aware-guards.md) (after T-008, same function family)
6. [T-010](tasks/T-010-add-parameter-domain-refusal.md) (a writer refusal)
7. [T-006](tasks/T-006-delete-connection-refusal.md) (a writer refusal)
8. [T-011](tasks/T-011-supersession-pointer.md) (the engine)
9. [T-004](tasks/T-004-spec-checks-report-live-rows.md) (checks; report only)
10. [T-005](tasks/T-005-retired-row-view-fixture.md) (a test)
11. [T-012](tasks/T-012-follow-up-reasons.md) (schema migration)
12. [T-013](tasks/T-013-typed-gaps.md) (schema migration; touches the engine and two writers)
13. [T-015](tasks/T-015-language-fold.md) (schema migration (views))
14. [T-001](tasks/T-001-layer0-marks-and-text.md) (Layer 0 text)
15. [T-002](tasks/T-002-contract-entry-text.md) (the contract; after T-001, same file)
16. [T-042](tasks/T-042-derive-choices-and-counts.md) (the registry and one CLAUDE.md sentence; after T-001, same file)
17. [T-003](tasks/T-003-owner-queue-answered-marks.md) (the owner queue)
18. [T-043](tasks/T-043-refusals-name-next-action.md) (last: by then the new refusals of T-006, T-007, T-008 and T-010 exist and must also name a next action)

**What may be drafted side by side** (files touched decide it; merge is still one at a time):

| Group | Tasks | They share |
|---|---|---|
| Writers | T-006, T-007, T-008, T-009, T-010, T-041, T-043 | `scripts/db.py`: draft in sequence, or expect a merge each time |
| Engine | T-011, T-013, T-041 | `scripts/assess/assess_cell.py` |
| Schema | T-012, T-013, T-015 | the next migration number (derived at execution time, again after each merge) |
| Layer 0 text | T-001, T-002, T-042, T-003 | `CLAUDE.md`, `governance/pipeline-contract.yaml`, `governance/check-registry.yaml` |
| Independent | T-004, T-005, T-014 | nothing with the others |

**Also free of any precondition, placed later only for order:** [T-026](tasks/T-026-alias-attestation.md) (tooling), [T-027](tasks/T-027-source-identity-edition.md) (tooling), [T-035](tasks/T-035-skills-repair.md) (tooling), [T-048](tasks/T-048-root-registry-writer.md) (tooling), [T-104](tasks/T-104-verify-governing-sources.md) (research). Any of them may be pulled forward. By command: `grep -L "Owner decisions that must be answered first" workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md | xargs grep -l "merged to .main. first:\*\* none" | xargs grep -L "NOT FOR SONNET"`.

## 5. Later waves, the dependency graph and the critical path

**Critical path to a first live determination that is for the group it names:**

[T-014](tasks/T-014-stress-harness-and-probes.md) → [T-008](tasks/T-008-claimed-number-check.md) → [T-016](tasks/T-016-wp-t1a-reading.md) → [T-017](tasks/T-017-wp-t2-conditions.md) → [T-018](tasks/T-018-link-table.md) → [T-019](tasks/T-019-lens-gather.md) → { [T-104](tasks/T-104-verify-governing-sources.md), [T-102](tasks/T-102-mobility-split.md), [T-106](tasks/T-106-retag-lenses.md) } → [T-110](tasks/T-110-first-determinations.md).

Two links on it are not Sonnet's to start: T-018 needs a one-page design from the Fable agent, and T-102 needs the owner's answer to OD-14 and an Opus-class session.

| Wave | Purpose | Tasks | Order inside the wave |
|---|---|---|---|
| 1 | the lens chain and the parameter kind | [T-016](tasks/T-016-wp-t1a-reading.md), [T-017](tasks/T-017-wp-t2-conditions.md), [T-018](tasks/T-018-link-table.md), [T-019](tasks/T-019-lens-gather.md), [T-020](tasks/T-020-quantity-kind.md) | Serial: T-016, T-017, T-018, T-019. T-020 beside them once OD-24 is answered. |
| 2 | carriers for going back | [T-021](tasks/T-021-cell-question-gate.md), [T-022](tasks/T-022-contract-re-entry.md), [T-023](tasks/T-023-ledger-relayed-statements.md), [T-048](tasks/T-048-root-registry-writer.md) | T-048 any time; T-021, T-022, T-023 as their answers arrive. |
| 3 | a base that is data | [T-024](tasks/T-024-jurisdiction-registry.md), [T-025](tasks/T-025-base-writers.md), [T-026](tasks/T-026-alias-attestation.md), [T-027](tasks/T-027-source-identity-edition.md), [T-028](tasks/T-028-concept-identity.md), [T-047](tasks/T-047-add-by-data-test.md) | T-024 then T-025; T-026 and T-027 any time; T-028 after OD-03; T-047 last. |
| 4 | reading once, abstraction, synthesis | [T-029](tasks/T-029-term-relations.md), [T-030](tasks/T-030-units-as-data.md), [T-031](tasks/T-031-clause-unit-and-open-pass.md), [T-032](tasks/T-032-synthesis-relations.md), [T-033](tasks/T-033-synthesis-candidates.md), [T-034](tasks/T-034-cell-status-verb.md), [T-035](tasks/T-035-skills-repair.md) | T-034 after T-013; T-035 any time; T-029 after T-020; T-030, T-031, T-032 after their answers; T-033 after T-029 and T-030. |
| 5 | render and the gate over it | [T-036](tasks/T-036-jurisdiction-comparison-view.md), [T-037](tasks/T-037-render.md), [T-038](tasks/T-038-stage-pair-gate.md), [T-039](tasks/T-039-owner-edits.md), [T-040](tasks/T-040-deletion-candidates-sweep.md) | T-036 after T-024 and T-101; T-037 after its three answers; T-038 after T-037; T-039; T-040. |
| research | rows, each in its own pull request | [T-101](tasks/T-101-scope-fill.md), [T-102](tasks/T-102-mobility-split.md), [T-103](tasks/T-103-medical-lens.md), [T-104](tasks/T-104-verify-governing-sources.md), [T-105](tasks/T-105-read-held-sources.md), [T-106](tasks/T-106-retag-lenses.md), [T-107](tasks/T-107-attest-forms.md), [T-108](tasks/T-108-unit-condition-repair.md), [T-109](tasks/T-109-parameter-kinds-data.md), [T-110](tasks/T-110-first-determinations.md) | T-104 and T-108 are ungated; the rest wait for tooling, an answer, or an Opus-class session. |

**Dependency list** (a task on the left needs every task on the right merged; generated from the task files):

```
T-016 <- T-008
T-017 <- T-016
T-018 <- T-017; plus the design file from the Fable agent
T-019 <- T-016, T-017, T-018   [owner: OD-08, for one sub-case only]
T-020 <- T-010   [owner: OD-24]
T-021 <- T-019   [owner: OD-21]
T-022 <- T-002, T-012, T-013   [owner: OD-18]
T-023 <- (no task)   [owner: OD-28]
T-024 <- (no task)   [owner: OD-01, for sub-national rows only]
T-025 <- T-024
T-028 <- T-026   [owner: OD-03]
T-029 <- T-020
T-030 <- T-016, T-020   [owner: OD-22]
T-031 <- T-019   [owner: OD-23]
T-032 <- T-029   [owner: OD-07, OD-25, OD-19, OD-29]
T-033 <- T-029, T-030
T-034 <- T-013
T-036 <- T-024, T-101   [owner: OD-01]
T-037 <- T-019, T-036   [owner: OD-02, OD-08, OD-12]
T-038 <- T-037   [owner: OD-26, only if an interim gate is wanted]
T-039 <- T-037   [owner: OD-20]
T-040 <- T-013, T-032
T-041 <- T-014
T-043 <- T-014
T-047 <- T-015, T-020, T-024, T-025, T-029
T-101 <- T-025   [owner: OD-04]
T-102 <- T-018, T-025; an Opus-class session   [owner: OD-14]
T-103 <- (no task)   [owner: OD-15]
T-105 <- T-008, T-009, T-016, T-031 (T-031 only if OD-23 chooses a clause inventory)
T-106 <- T-019
T-107 <- T-026
T-108 <- T-016
T-109 <- T-020
T-110 <- T-019, T-102, T-104; the blocking battery green on the scratch copy; an Opus-class session
```

## 6. Stop points

| When | Who is waited for | What for | What can continue meanwhile |
|---|---|---|---|
| Before T-018 | the Fable implementation agent | the one-page design of the link table (`tasks/T-018-design.md`) | all of Wave 0; T-016, T-017; T-048, T-026, T-027, T-035 |
| Inside T-019 | the owner (OD-08) | one sub-case only: a relevant lens with no figure | the ruled part of T-019 is built without it |
| Before T-020, and so T-029, T-030, T-047, T-109 | the owner (OD-24) | quantity kinds; parameter granularity | everything not listed |
| Before T-101, and so T-036 | the owner (OD-04) | what the scope answer covers | T-024, T-025 (the writers) |
| Before T-102, and so T-110 | the owner (OD-14), then an Opus-class session | carrying rows written under `MOB` | T-104, T-106 after T-019 |
| Before T-031 | the owner (OD-23) | how a later parameter reaches a source already read | T-105 on sources whose text is held |
| Before T-032 | the owner (OD-07, OD-25, OD-19, OD-29) | what synthesis records | T-029 and T-033, once OD-24 has released T-020 |
| Before T-037, and so T-038, T-039 | the owner (OD-02, OD-08, OD-12; OD-20 for T-039) | render | every earlier wave |
| Before T-110 | the blocking battery, green on the scratch copy, the integrity test included | a first live determination | — |
| At the end of every wave | the owner | the wave's lines of the Definition of Done (section 10), run and reported; `python3 workplan/pipeline-state-graph/walkability.py` run as a command until T-038 registers it | — |
| At any time | the owner | anything touching mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing or trajectory | — |

## 7. Three tracks across the waves

The measurements behind this section are in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §9. The readings of "hard-coded" and "dead end" used there are the audit's and are unratified: a behaviour is hard-coded when changing it means editing code for something that is data, or editing code in more than one place; a dead end is a row, state, path, stage or refusal with no sanctioned way onward, back or out.

| Track | Owner statement | Finding | Tasks | Proof |
|---|---|---|---|---|
| Efficient | REQ-101 | Measured and sufficient: a verb and a determination take well under a second, a rebuild about two seconds, the diff-scoped gate about two minutes once per pull request. Not measured: a hundred times the present rows. | none proposed | timings in the stress logs (`stress/results2/`, `stress/results3/`) |
| Centralized | REQ-101 | Helpers defined twice; jurisdictions and unit families as lists in code; typed counts in the registry. The command-line value lists are already read from the schema. | [T-041](tasks/T-041-one-home-for-helpers.md), [T-042](tasks/T-042-derive-choices-and-counts.md), [T-024](tasks/T-024-jurisdiction-registry.md), [T-030](tasks/T-030-units-as-data.md) | T-041's command prints `{}`; the stress logs are identical before and after (T-014's `stress_diff.py`) |
| Clean | REQ-101 | Skills naming structures that are gone; a verb that reports success having done nothing; a documented command that does not run; checks whose prose contradicts the data; dead apparatus. | [T-035](tasks/T-035-skills-repair.md), [T-006](tasks/T-006-delete-connection-refusal.md), [T-001](tasks/T-001-layer0-marks-and-text.md), [T-004](tasks/T-004-spec-checks-report-live-rows.md), [T-040](tasks/T-040-deletion-candidates-sweep.md) | `skill_vocabulary_audit` exits 0; each task's after-test |
| Declined | REQ-101 | Splitting `scripts/db.py`: no measured cost saved, every import and ledger reference changed. | none | revisit only on a measured problem |
| No hard-coded behaviour | REQ-102 | Jurisdictions, scope, lens selection, units, what may be a parameter. Already data-driven and kept: the check registry, vocabularies read from the column's CHECK, the derived capture set, one home for stage ids. | [T-024](tasks/T-024-jurisdiction-registry.md), [T-025](tasks/T-025-base-writers.md), [T-101](tasks/T-101-scope-fill.md), [T-019](tasks/T-019-lens-gather.md), [T-030](tasks/T-030-units-as-data.md), [T-010](tasks/T-010-add-parameter-domain-refusal.md), [T-020](tasks/T-020-quantity-kind.md), [T-029](tasks/T-029-term-relations.md), [T-047](tasks/T-047-add-by-data-test.md) | the add-by-data test (T-047): a language and jurisdiction pair, a jurisdiction, a term, a parameter and a term pointer are added by sanctioned verbs with no file under `scripts/` or `schemas/` changed |
| No dead ends: structural | REQ-103 | Stage pairs ending at render; the root registry and the base tables with no writer; the empty medical lens. | [T-037](tasks/T-037-render.md), [T-038](tasks/T-038-stage-pair-gate.md), [T-048](tasks/T-048-root-registry-writer.md), [T-025](tasks/T-025-base-writers.md), [T-103](tasks/T-103-medical-lens.md) | walkability prints no `NO PATH`; CLAUDE.md §4's derivation prints no `UNWRITABLE` line that is not intended |
| No dead ends: state | REQ-103 | A retired determination with no successor; a `pending` row nothing will fill; a new parameter's owed readings where no text is held. | [T-011](tasks/T-011-supersession-pointer.md), [T-019](tasks/T-019-lens-gather.md), [T-031](tasks/T-031-clause-unit-and-open-pass.md) | each task's after-test |
| No dead ends: operational | REQ-103 | Refusals that name no next action; a silent no-op; a command that does not run as written. | [T-043](tasks/T-043-refusals-name-next-action.md), [T-006](tasks/T-006-delete-connection-refusal.md), [T-001](tasks/T-001-layer0-marks-and-text.md) | every distinct refusal the harness produces names a next action |
| No dead ends: reader and process | REQ-103 | No carrier for a question about a published cell; no rendered claim to trace; skills pointing at deleted structures; an answered prompt shown as open. | [T-021](tasks/T-021-cell-question-gate.md), [T-037](tasks/T-037-render.md), [T-035](tasks/T-035-skills-repair.md), [T-003](tasks/T-003-owner-queue-answered-marks.md) | each task's after-test |

A deliberate refusal is not a dead end and is not loosened: one research batch at a time (the capture refuses a batch drafted from an older base; OD-27 asks whether the owner wants otherwise), and the two absent refusals of CLAUDE.md §4.

## 8. Owner decision register

Each entry is **OWNER DECISION REQUIRED**. Nothing here is decided; each recommendation is labelled as one. To answer, the owner says one of the answer forms; the session that hears it appends it to `references/project-standards.md` in the ledger's form, quoting the owner, so that the line `OD-NN: …` can be found by `grep -n -F "OD-NN:" references/project-standards.md`. A task checks for exactly that. OD-16 was withdrawn (it was answered on the record). Count the entries: `grep -c "^### OD-" workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`.

**Which answers release the most work:** OD-24 (T-020 and everything behind it), OD-04 (scope), OD-14 (the mobility split, which the first determinations wait on), OD-02 with OD-08 and OD-12 (render), OD-23 (reading once). These ids belong to this plan; an older series with the same letters appears in `decisions/` and is unrelated.

### OD-01  Jurisdiction in a determination; jurisdictions below the country; climate and culture

- **Question.** Is there one determination per parameter and group, with the jurisdictions shown beside it as a spread, or one determination per jurisdiction? Is a province, state or region a jurisdiction of its own? Are climate and cultural context recorded as typed conditions?
- **Why it is the owner's.** Jurisdiction scope and the shape of the book's central claim are doctrine. The ledger holds no ruling on the cell key carrying a jurisdiction.
- **Options and what follows from each.**
  - (a) One determination per parameter and group; jurisdictions shown as a spread. *Then:* The cell key stays as ruled; a comparison view (T-036) is enough.
  - (b) One determination per jurisdiction. *Then:* The key of `specifications` changes; every determination table, view and check is touched; T-036 stops and a new design is needed.
  - (c) (a), plus typed conditions for climate and cultural context. *Then:* As (a), with condition rows added to figures; no key change.
  - (sub) Sub-national: codes with a parent, or country level only. *Then:* With a parent: a provincial code stops being filed under its country (today an Ontario instrument is stored as Canada, a Flemish one as Belgium). Country only: those rows stay as they are and the page must say so.
- **Recommendation (the audit's, not a decision).** (c), with sub-national codes that carry a parent.
- **Answer in one line.** `OD-01: one determination across jurisdictions, spread shown` · `OD-01: a determination per jurisdiction` · `OD-01: one determination, with typed climate and cultural conditions` · and one of: `OD-01: sub-national codes with a parent` / `OD-01: country level only`
- **Tasks blocked until answered.** T-024 (sub-national rows only; the table and country rows proceed without it), T-036, T-037
- **Where the evidence is.** HS-1 C-03, HS-A12; `REF-01013`, `REF-00995`

### OD-02  The language of a page, and whether a source's sentence may be translated

- **Question.** Is a page written in English with each source quoted in its own language, or are pages produced in several languages? May a quotation be shown in translation, and marked how?
- **Why it is the owner's.** Audience and the reading surface are doctrine; a translated quotation is no longer the source's words.
- **Options and what follows from each.**
  - (i) English pages; each source quoted in its own language. *Then:* Render needs one language; quotes need script support only.
  - (ii) Pages in several languages. *Then:* Every fixed sentence needs a translation and an owner for it; out of reach of this plan.
  - (t) A marked translation beside the original, where the owner permits one. *Then:* Needs a place to hold the translation and who made it.
- **Recommendation (the audit's, not a decision).** (i) for this edition; originals always shown; a marked translation only where the owner permits.
- **Answer in one line.** `OD-02: English pages, sources quoted in the original` · `OD-02: English pages, originals with marked translations` · `OD-02: pages in <languages>`
- **Tasks blocked until answered.** T-037
- **Where the evidence is.** HS-1 C-02

### OD-03  A concept that has no English name

- **Question.** How is a concept held when it was first met in another language and has no settled English name?
- **Why it is the owner's.** It changes the base vocabulary's identity rule, which every stage points into; the ledger records the schema decision as open.
- **Options and what follows from each.**
  - (a) A forms table with a pointer to the display form. *Then:* A schema change across every writer that screens or matches a name (T-028).
  - (b) Keep the English name column and add a label kind. *Then:* Smaller change; the concept is still named by an English gloss.
  - (c) Nothing until such a concept is minted. *Then:* No cost now; the first such concept forces the decision under time pressure.
- **Recommendation (the audit's, not a decision).** (a); (c) is defensible today because no such term exists.
- **Answer in one line.** `OD-03: forms table with a display pointer` · `OD-03: keep canonical_en, add a label kind` · `OD-03: nothing until a non-English-origin concept is minted`
- **Tasks blocked until answered.** T-028
- **Where the evidence is.** `grep -n -F "canonical_en" references/project-standards.md | tail -3`

### OD-04  What the scope answer of 2026-10-30 covers

- **Question.** The owner answered "Yes it is P1+P2+P3" and "do not include countries outside of the major identified countries for now" about the specification page. Does that answer also set the research scope and the base's languages? Is the set recorded in the ledger as an assumption the set meant? Is `UN` in? Are script and regional variants separate pairs?
- **Why it is the owner's.** Jurisdiction scope is doctrine. The set written into the ledger is marked there as the assistant's assumption.
- **Options and what follows from each.**
  - (a) One scope for research, base and page: the recorded set. *Then:* `lang_jur_map.scope_status` is filled once (T-101); coverage stops owing research the owner excluded.
  - (b) The answer covers the page only; research scope stays wider. *Then:* Coverage keeps owing the wider set; the page is cut by a second list.
  - (un) `UN` in or out. *Then:* In: UN instruments are a pair of their own. Out: they are cited but owe no coverage.
- **Recommendation (the audit's, not a decision).** Confirm the recorded set as the one scope, and rule on `UN`.
- **Answer in one line.** `OD-04: scope = <codes>; UN: in|out; applies to: research, base and page` · `OD-04: scope = <codes>; UN: in|out; applies to: page only`
- **Tasks blocked until answered.** T-101; through it T-036 and every coverage reading
- **Where the evidence is.** `grep -n -F "P1+P2+P3" references/project-standards.md`

### OD-05  Evidence from outside the scope that citation mining surfaces

- **Question.** When mining a confirmed source turns up evidence from a jurisdiction outside the scope, is it admitted, staged as a lead, or refused?
- **Why it is the owner's.** Jurisdiction scope; and admitting it changes what the book rests on.
- **Options and what follows from each.**
  - (a) Admit. *Then:* Scope becomes porous; coverage owes follow-up in places the owner excluded.
  - (b) Stage as a lead with its origin. *Then:* Nothing is lost; nothing out of scope is determined on.
  - (c) Refuse. *Then:* Primary research from elsewhere is lost.
- **Recommendation (the audit's, not a decision).** (b); admit only T1 to T3 on the owner's word.
- **Answer in one line.** `OD-05: stage as a lead` · `OD-05: admit T1-T3, stage the rest` · `OD-05: refuse`
- **Tasks blocked until answered.** No task in this plan; it governs research sessions that mine citations (T-105)
- **Where the evidence is.** HS-3 OD-05

### OD-06  Which stage assigns the lenses

- **Question.** Does "evidence stage" in the owner's list of 2026-11-06 mean evidence and judgment together, so that judgment assigns the lens codes?
- **Why it is the owner's.** It is a reading of the owner's own words; population taxonomy.
- **Options and what follows from each.**
  - (a) Confirm: judgment assigns. *Then:* T-106 proceeds as written.
  - (b) Evidence assigns at admission. *Then:* Admission writers gain lens arguments; a different task.
- **Recommendation (the audit's, not a decision).** Confirm (a).
- **Answer in one line.** `OD-06: judgment assigns the lenses` · `OD-06: evidence assigns the lenses`
- **Tasks blocked until answered.** Informs T-106; blocks nothing else
- **Where the evidence is.** `grep -n -F "evidence stage" references/project-standards.md | tail -3`

### OD-07  What one synthesis row is

- **Question.** Is synthesis a step inside the engine, or a separable stage whose rows a determination points at?
- **Why it is the owner's.** It fixes what the synthesis stage holds, which is the spine the owner ruled.
- **Options and what follows from each.**
  - (a) Inside the engine; the narrative tables are deleted. *Then:* Less schema; relations found in one run are not kept for the next.
  - (b) Separable, with its own rows that a determination points at. *Then:* Findings outlive a run; one more stage to gate.
- **Recommendation (the audit's, not a decision).** (b) for relations, with convergence left in the engine.
- **Answer in one line.** `OD-07: synthesis stays inside the engine` · `OD-07: separable, with its own rows`
- **Tasks blocked until answered.** T-032
- **Where the evidence is.** HS-1 REQ-100

### OD-08  What an absent cell means

- **Question.** A cell with no determination may be not relevant, not yet researched, or researched and empty. Is any of these stored as a determination row?
- **Why it is the owner's.** It decides what a reader is told about absence, which is the book's honesty about its gaps.
- **Options and what follows from each.**
  - (a) Store none; derive the three from searches, readings and gaps. *Then:* No `pending` rows for lenses nothing will fill; the cell status query (T-034) answers.
  - (b) Keep a `pending` row with its gap for a lens that is relevant and has no figure. *Then:* The row exists to point at; "relevant" must then be judged and recorded by someone.
- **Recommendation (the audit's, not a decision).** (a).
- **Answer in one line.** `OD-08: no row` · `OD-08: keep pending with its gap`
- **Tasks blocked until answered.** T-019 (one sub-case only; the ruled part proceeds), T-037
- **Where the evidence is.** HS-3 IMP-09

### OD-09  What "dynamically" may do unattended

- **Question.** May a run be started and carried through stages without the owner present, and is the request recorded as a row?
- **Why it is the owner's.** Trajectory and the owner's control of the project.
- **Options and what follows from each.**
  - (a) On demand, with judgment made and warranted by the model; no request table. *Then:* The cause rows (gap, follow-up, search) are the record.
  - (b) A request table. *Then:* One more table with one writer and no reader yet.
- **Recommendation (the audit's, not a decision).** (a).
- **Answer in one line.** `OD-09: on demand, no request table` · `OD-09: record each request as a row`
- **Tasks blocked until answered.** No task; it governs how `/run-pipeline` is invoked
- **Where the evidence is.** HS-3 OD-09

### OD-10  `provisional`: strength of evidence, or a re-read owed

- **Question.** Does `provisional` mean the evidence is thin, or that a reading is still owed?
- **Why it is the owner's.** It is the meaning of a cell state a reader sees.
- **Options and what follows from each.**
  - (a) Strength only; an owed re-read is a follow-up row. *Then:* One more reason value later; the state keeps one meaning.
  - (b) Both. *Then:* The state cannot be read without the note.
- **Recommendation (the audit's, not a decision).** (a).
- **Answer in one line.** `OD-10: provisional means strength only` · `OD-10: provisional also means a re-read is owed`
- **Tasks blocked until answered.** No task; if (a), one further reason value is added to T-012's vocabulary in a later task
- **Where the evidence is.** HS-3 OD-10

### OD-11  Which stage owns the gap register

- **Question.** Is the gap register a research table, or a cross-stage register written by whichever stage finds the gap?
- **Why it is the owner's.** Stage assignment follows the owner's spine.
- **Options and what follows from each.**
  - (a) Cross-stage, named so in the stage map. *Then:* Matches what the engine already does.
  - (b) Research only. *Then:* The engine may no longer write gaps.
- **Recommendation (the audit's, not a decision).** (a).
- **Answer in one line.** `OD-11: cross-stage register` · `OD-11: research owns it`
- **Tasks blocked until answered.** No task blocked; T-013 proceeds either way
- **Where the evidence is.** HS-3 OD-11

### OD-12  How render's prose is produced, and whether it is stored

- **Question.** Are page sentences produced from fixed templates over typed rows, or written? Is the rendered table stored or rebuilt? (The owner queue's OW-1b and OW-1c.)
- **Why it is the owner's.** Mission: the book is a thinking tool and not an authority; who writes its sentences is the owner's.
- **Options and what follows from each.**
  - (a) Fixed templates from typed rows; rebuilt, not stored. *Then:* Every sentence traces to a row; no stored copy to drift.
  - (b) Written prose, stored. *Then:* Needs the synthesis floor for every page and a parity check, which the project's rules warn against.
- **Recommendation (the audit's, not a decision).** (a), until a measured cost says otherwise.
- **Answer in one line.** `OD-12: templates, rebuilt` · `OD-12: written prose, stored`
- **Tasks blocked until answered.** T-037
- **Where the evidence is.** `python3 -c "import yaml;d=yaml.safe_load(open('governance/owner-browser.yaml'));print([q['id'] for q in d['decisions'] if q['id'].startswith('OW-1')])"`

### OD-13  The "at least nine languages" rule of March 2026

- **Question.** Is that rule superseded by the later rulings that count language and jurisdiction pairs?
- **Why it is the owner's.** Only the owner retires an owner rule where the later ruling does not name it.
- **Options and what follows from each.**
  - (a) Superseded. *Then:* One appended back-pointer in the ledger.
  - (b) Still in force. *Then:* Coverage must count languages as well as pairs.
- **Recommendation (the audit's, not a decision).** (a).
- **Answer in one line.** `OD-13: superseded by the pair rulings` · `OD-13: still in force`
- **Tasks blocked until answered.** No task blocked; on (a), one line is appended in T-001 or after it
- **Where the evidence is.** HS-3 OD-13

### OD-14  Carrying the rows written under `MOB` since the split was ratified

- **Question.** The split of the mobility group into ambulant people and wheelchair users is ratified and unexecuted. How are the figures and grades written under `MOB` since then carried, and how are part-time wheelchair users named in a gap?
- **Why it is the owner's.** Population taxonomy.
- **Options and what follows from each.**
  - (a) Fan each row out to both codes, flagged as awaiting re-derivation. *Then:* Fast; every row is provisionally wrong for one of the two groups.
  - (b) Judge each row by its participants or by the users its text names. *Then:* Slow and correct; rows that name nobody lose their identity tag.
  - (c) (a) for code provisions, (b) for studies. *Then:* Studies are judged; provisions are flagged.
- **Recommendation (the audit's, not a decision).** (c). A grade of a study's own participants is never fanned out.
- **Answer in one line.** `OD-14: fan out to both` · `OD-14: judge each row` · `OD-14: fan out code provisions, judge studies` · plus the owner's wording for part-time wheelchair users
- **Tasks blocked until answered.** T-102; through it T-110
- **Where the evidence is.** `grep -n -F "AMB" references/project-standards.md | head -5`

### OD-15  Filling the medical lens

- **Question.** Is the medical lens filled by correspondence as the corrected ruling says, and on what terms given the WHO licence?
- **Why it is the owner's.** Population taxonomy and licensing.
- **Options and what follows from each.**
  - (a) Proceed, English anchors only until the licence is read. *Then:* A reader who thinks in diagnoses gains a route.
  - (b) Wait for the licence. *Then:* The lens stays empty and the fourth lens column stays unusable.
- **Recommendation (the audit's, not a decision).** (a).
- **Answer in one line.** `OD-15: proceed, English anchors only` · `OD-15: wait`
- **Tasks blocked until answered.** T-103
- **Where the evidence is.** HS-A03

### OD-17  Ratify the corrected pipeline contract

- **Question.** After the entry texts are corrected (T-002) and the re-entry conditions added (T-022), does the owner ratify the contract as corrected?
- **Why it is the owner's.** Ratification is the owner's act.
- **Options and what follows from each.**
  - (a) Ratify. *Then:* The contract header can say so.
  - (b) Not yet. *Then:* The header keeps its outstanding precondition.
- **Recommendation (the audit's, not a decision).** Ratify after T-022.
- **Answer in one line.** `OD-17: ratified as corrected` · `OD-17: not yet`
- **Tasks blocked until answered.** No task blocked
- **Where the evidence is.** HS-3 OD-17

### OD-18  What "all directions" covers

- **Question.** Are the cold-entry and re-entry conditions for judgment, synthesis, specification and render, as listed in the top-down specification, the conditions the owner means? May an earlier stage's row be updated to record later use?
- **Why it is the owner's.** The conditions are an inference from the owner's objective, not the owner's words.
- **Options and what follows from each.**
  - (a) Confirm as listed; status updates on earlier rows allowed, copying later facts into them forbidden. *Then:* T-022 writes them into the contract.
  - (b) Correct them. *Then:* T-022 writes the corrected ones.
- **Recommendation (the audit's, not a decision).** (a).
- **Answer in one line.** `OD-18: confirm the entry and re-entry conditions of TD §3 as listed` · `OD-18: <corrected conditions>`
- **Tasks blocked until answered.** T-022
- **Where the evidence is.** `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md` §3

### OD-19  Conflict between groups in the engine

- **Question.** Harm asymmetry and broadest benefit are doctrine the engine does not apply. Does the engine apply a rule, or only record the conflict and the rule a person applied?
- **Why it is the owner's.** CRPD posture and the weighing of one group's harm against another's benefit.
- **Options and what follows from each.**
  - (a) Record only. *Then:* No mechanical weighing; each conflict is resolved by a named judge.
  - (b) The engine applies a rule the owner approves in mechanical form. *Then:* Repeatable; the rule must be written exactly.
- **Recommendation (the audit's, not a decision).** (a) now; (b) only after the owner approves the rule's mechanical form.
- **Answer in one line.** `OD-19: record only` · `OD-19: the engine applies <rule>`
- **Tasks blocked until answered.** T-032 (the engine part)
- **Where the evidence is.** HS-3 OD-19

### OD-20  The owner's edits

- **Question.** Are the owner's changes to a value made as proposals applied through the write path?
- **Why it is the owner's.** It is the owner's own tool.
- **Options and what follows from each.**
  - (a) Proposals through the write path. *Then:* Every change is a migration with its warrant.
  - (b) Another route. *Then:* To be designed.
- **Recommendation (the audit's, not a decision).** Confirm (a), which is the ledger's reading.
- **Answer in one line.** `OD-20: proposals through the write path` · `OD-20: <alternative>`
- **Tasks blocked until answered.** T-039
- **Where the evidence is.** HS-3 IMP-39

### OD-21  A question about a published cell

- **Question.** Is a reader's or the owner's objection to a published value recorded in the database, flagging the cell?
- **Why it is the owner's.** Audience, and what the book admits about itself.
- **Options and what follows from each.**
  - (a) Yes, as an open gate that flags the cell. *Then:* A schema widening of one table (T-021).
  - (b) No. *Then:* Objections stay in session files and the value stays up unmarked.
- **Recommendation (the audit's, not a decision).** (a).
- **Answer in one line.** `OD-21: yes, as an open gate` · `OD-21: no`
- **Tasks blocked until answered.** T-021
- **Where the evidence is.** HS-3 IMP-14

### OD-22  Rounding direction for converted lengths, and the other open prompts

- **Question.** When a minimum or a maximum is converted between units, which way is it rounded (the owner queue's OR-10b)? And each other prompt the queue still shows as open.
- **Why it is the owner's.** A rounding rule changes published values.
- **Options and what follows from each.**
  - (a) Round a minimum up and a maximum down. *Then:* The converted value never states less protection than the source.
  - (b) Nearest. *Then:* A converted minimum can fall below the source's.
- **Recommendation (the audit's, not a decision).** (a).
- **Answer in one line.** `OD-22: round a minimum up and a maximum down` · `OD-22: <rule>`
- **Tasks blocked until answered.** T-030
- **Where the evidence is.** `python3 -c "import yaml;d=yaml.safe_load(open('governance/owner-browser.yaml'));print([q['id'] for q in d['decisions'] if 'answered' not in q])"`

### OD-23  How a parameter defined later reaches a source already read

- **Question.** The owner asked that a source be read once. When a new parameter is defined, how does it reach the sources already read: by re-reading, by sweeping retained text, or by matching a stored inventory of clauses? May held clause text be shown?
- **Why it is the owner's.** Licensing (holding and showing a standard's text) and trajectory (cost of every later parameter).
- **Options and what follows from each.**
  - (a) Re-read. *Then:* Simplest; every new parameter owes a reading of every source, and needs the bytes again.
  - (b) Retained text. *Then:* A new parameter is swept over held text; holding retrieved copies is already ruled acceptable.
  - (c) Clause inventory. *Then:* Queryable and lets groups point at clauses; puts clause text in the database the site reads, and showing it is a further act not yet ruled on; misses what the open pass did not record.
- **Recommendation (the audit's, not a decision).** (c) backed by (b), with a recorded re-read where neither is possible.
- **Answer in one line.** `OD-23: re-read` · `OD-23: retained text` · `OD-23: clause inventory` · `OD-23: clause inventory backed by retained text` · plus: `held clause text may be shown: yes|no`
- **Tasks blocked until answered.** T-031; T-105 where an inventory is chosen
- **Where the evidence is.** HS-1 §5.2 (REQ-098)

### OD-24  How coarse a parameter is, and its quantity kinds

- **Question.** Is a parameter one measured quantity of an element with every clause variation a typed condition, a hierarchy, or fine-grained with groups above? What are the kinds of quantity, and must a parameter belong to an element?
- **Why it is the owner's.** It decides what the book can unify and what divergence it can show; the owner raised it directly.
- **Options and what follows from each.**
  - (a) Flat and coarse, variations as conditions, families by term pointers. *Then:* Unifies; divergence is shown as conditions.
  - (b) Hierarchy. *Then:* Parents and children must be kept consistent.
  - (c) Flat and fine, with equivalence groups. *Then:* Many parameters; unification depends on the groups being complete.
- **Recommendation (the audit's, not a decision).** (a), with a written test for a split (two cases are two parameters only when they cannot be placed on one scale or their directions differ).
- **Answer in one line.** `OD-24: kinds = <list>; element required: yes|no` · and one of: `OD-24: flat and coarse` / `OD-24: hierarchy` / `OD-24: flat and fine with groups`
- **Tasks blocked until answered.** T-020, T-109; through T-020 also T-029, T-030, T-047
- **Where the evidence is.** HS-1 §5.3 (REQ-099)

### OD-25  Which relations synthesis records, and who may judge them

- **Question.** The owner named equivalencies, adjacencies, similarities and commonalities. Which relation kinds are recorded, and which class of model may judge one?
- **Why it is the owner's.** It is the vocabulary of the book's discussion; the capability floor is an owner rule.
- **Options and what follows from each.**
  - (a) Five kinds: equivalence, adjacency, similarity or commonality, conflict, convergence; judged at the synthesis floor. *Then:* Found by query (T-033), judged by an Opus-class model or above.
  - (b) Another list. *Then:* T-032 uses it.
- **Recommendation (the audit's, not a decision).** (a).
- **Answer in one line.** `OD-25: relations = <list>; judged by <class>`
- **Tasks blocked until answered.** T-032
- **Where the evidence is.** HS-1 REQ-100

### OD-26  An interim stage-pair gate before render exists

- **Question.** The ruled gate fails on any stage pair with no path, and every pair ending at render has none until render exists. Is an interim gate wanted meanwhile?
- **Why it is the owner's.** It would add a stored baseline of today's paths, a curated list of the kind the project's rules forbid; only the owner can accept that.
- **Options and what follows from each.**
  - (a) Wait; run the instrument as a command at the end of each wave. *Then:* No new apparatus; a lost path is seen at wave end, not at once.
  - (b) An interim check on a stored baseline. *Then:* A lost path is seen at once; one curated list to maintain.
- **Recommendation (the audit's, not a decision).** (a).
- **Answer in one line.** `OD-26: wait` · `OD-26: interim gate`
- **Tasks blocked until answered.** T-038 (only if an interim gate is wanted; otherwise it waits on T-037)
- **Where the evidence is.** HS-3 IMP-07

### OD-27  Are parallel research batches wanted?

- **Question.** Two research batches drafted from the same base cannot both land: the second is refused at capture and must be redone from the new `main`. Is that acceptable, or must batches run in parallel?
- **Why it is the owner's.** Trajectory: it sets how fast research can go and how much tooling is worth building for it.
- **Options and what follows from each.**
  - (a) Serial is acceptable. *Then:* Nothing to build; the refusal stays and the skill says so (T-001).
  - (b) Parallel is required. *Then:* Identifier allocation and capture must be redesigned; not in this plan.
- **Recommendation (the audit's, not a decision).** (a).
- **Answer in one line.** `OD-27: serial is acceptable` · `OD-27: parallel batches are required`
- **Tasks blocked until answered.** No task blocked
- **Where the evidence is.** HS-5 B-76

### OD-28  The wording of the statements relayed on 2026-10-12

- **Question.** Eight owner sentences (O1 to O8) are quoted in a design file as relayed. Does the owner confirm the wording, so that they can be entered in the ledger?
- **Why it is the owner's.** Only the owner can say what the owner said.
- **Options and what follows from each.**
  - (a) Confirmed. *Then:* T-023 appends them.
  - (b) Corrected. *Then:* T-023 appends the corrected sentences.
- **Recommendation (the audit's, not a decision).** Confirm or correct; until then plans may cite them only as relayed.
- **Answer in one line.** `OD-28: confirmed` · `OD-28: <corrected sentences>`
- **Tasks blocked until answered.** T-023
- **Where the evidence is.** `sed -n "11p" workplan/pipeline-state-graph/IDEAL-GRAPH.md`

### OD-29  Does retire-in-place cover link rows?

- **Question.** The owner ruled "retire in place, never hard-delete" for data rows and identifiers. Two verbs still delete: `delete-connection` (a connection and its targets) and `unlink-admission` (the edge between a search and a source it admitted, built later with a sanctioned capture of the delete). Does the ruling cover a connection, and does it cover an edge that carries no identifier of its own?
- **Why it is the owner's.** It is a reading of the owner's own ruling; a deleted row loses the fact that it existed.
- **Options and what follows from each.**
  - (a) Both retire in place. *Then:* A connection gains a retired status (done inside T-032, which reshapes the table); the admission edge gains a retired mark and the delete capture is removed.
  - (b) A connection retires; an edge with no identifier may be deleted by its sanctioned verb. *Then:* T-032 covers the connection; `unlink-admission` stays, and the ledger says why.
  - (c) Both may be deleted. *Then:* The ledger records the exception the ruling asks for, case by case.
- **Recommendation (the audit's, not a decision).** (b).
- **Answer in one line.** `OD-29: both retire in place` · `OD-29: connections retire; an admission edge may be deleted` · `OD-29: both may be deleted`
- **Tasks blocked until answered.** T-032 (how `delete-connection` ends); no other task
- **Where the evidence is.** `grep -n -F "RETIRE IN PLACE, NEVER HARD-DELETE" references/project-standards.md`; HS-1 REQ-018

## 9. Retained stress-test value

Three rounds of stress scripts found defects that no registered check finds. What is kept and why is in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/stress/RETAINED.md` (the owner permitted retention: `grep -n -F "retain" references/project-standards.md | tail -3`).

- **As a harness:** [T-014](tasks/T-014-stress-harness-and-probes.md) repairs the scripts and adds a normalised log diff. Every task that claims to preserve behaviour (T-041, T-043, T-016, T-017) runs the harness before and after and shows the diff.
- **As permanent tests:** each probe becomes a test in the task whose defect it proves, red before the fix: the number check ([T-008](tasks/T-008-claimed-number-check.md)), the script probes ([T-009](tasks/T-009-script-aware-guards.md)), the element and legal-term promotions ([T-010](tasks/T-010-add-parameter-domain-refusal.md), [T-020](tasks/T-020-quantity-kind.md)), the supersession pointer ([T-011](tasks/T-011-supersession-pointer.md)), the silent delete ([T-006](tasks/T-006-delete-connection-refusal.md)), the source with no standing ([T-007](tasks/T-007-add-source-standing.md)), the wrong-lens determination ([T-019](tasks/T-019-lens-gather.md)), the retired row in a view ([T-005](tasks/T-005-retired-row-view-fixture.md)).
- **As research leads, in research pull requests only:** the sources a first determination rests on that are not verified ([T-104](tasks/T-104-verify-governing-sources.md)); the held source whose text is on file and unread ([T-105](tasks/T-105-read-held-sources.md)).

## 10. Definition of Done

The plan is done when every line below gives its "done" result on `main`, run by someone who did not write the change. Lines are commands; none is a number to remember. Run from the repository root. Where a line needs a scratch copy: `export SCRATCH="${TMPDIR:-/tmp}/guidebook-dod" && mkdir -p "$SCRATCH"`.

| # | The objective says | Command | Today | Done |
|---|---|---|---|---|
| D-01 | all directions: no stage pair without a path | `python3 workplan/pipeline-state-graph/walkability.py \| grep -c "NO PATH"` | not 0 | 0 |
| D-02 | …and a lost path is seen | `python3 scripts/run_checks.py --list \| grep -c -i walkab` | 0 | 1 or more, blocking, with `EXAMINED:` above 0 when run |
| D-03 | no dead end: every refusal names a next action | the evidence command in section 3 of `tasks/T-043-refusals-name-next-action.md` | about half of the distinct messages do | both counts equal; no message listed |
| D-04 | no dead end: no table that cannot be written by accident | the derivation block in CLAUDE.md §4 ("UNWRITABLE") | three lines (two for the medical lens, one for connection targets) | no line, or each remaining line named in the ledger as intended |
| D-05 | no dead end: a root can be registered | `grep -c "writer yet, so until one exists" scripts/db.py` | 1 | 0 |
| D-06 | going back leaves a typed cause | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select (select count(*) from pragma_table_info('gaps') where name='parameter_id'), (select count(*) from pragma_table_info('search_executions') where name='gap_id')\").fetchall())"` | `[(0, 0)]` | `[(1, 1)]` |
| D-07 | at any stage: where a cell stands can be asked | `python3 scripts/db.py --help \| tr "," "\n" \| grep -c -i "cell-status"` | 0 | 1 |
| D-08 | a determination is for the group it names | `cp data/guidebook.db "$SCRATCH/d.db" && python3 scripts/assess/assess_cell.py --db "$SCRATCH/d.db" --emit-sql "$SCRATCH/d.sql" --parameter-id 3 --slug accessible-circulation-geometry --identity DEAF --session session_dod-probe --stamp "2026-01-01 00:00" \| head -1` | `param 3×DEAF provisional …`, computed from figures tagged for other groups | no determination row is written for a group no figure of the parameter names; the wrong-lens test of T-019 passes |
| D-09 | the mobility split is executed | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*) from base_taxonomy_identity where identity_code in ('AMB','WHEEL')\").fetchall())"` | `[(0,)]` | `[(2,)]`, and rows under `MOB` carried as OD-14 directs |
| D-10 | the fourth lens is usable | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*) from base_taxonomy_medical\").fetchall())"` | `[(0,)]` | above 0 |
| D-11 | jurisdictions: scope is data | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*), sum(scope_status is not null) from lang_jur_map\").fetchall())"` | the second number is 0 | the two numbers are equal |
| D-12 | languages: one spelling per language | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"SELECT (SELECT COUNT(DISTINCT language) FROM v_coverage_language), (SELECT COUNT(DISTINCT UPPER(language)) FROM search_executions WHERE deferred_reason IS NULL)\").fetchall())"` | the two numbers differ | equal |
| D-13 | flexible: the base changes by data alone | `f=$(grep -l 'AT-104' scripts/tests/*.py); echo "file=$f"; [ -n "$f" ] && python3 $f; echo rc=$?` | `file=` (none) and `rc=1` | a file is named and `rc=0` |
| D-14 | no hard-coded unit list | `grep -c NOTATION_FAMILIES scripts/assess/assess_cell.py` | not 0 | 0 |
| D-15 | languages and scripts: the guards hold outside Latin script | the evidence command in section 3 of `tasks/T-009-script-aware-guards.md` | `True True`, then empty token sets | `False False`, then non-empty token sets and `True` |
| D-16 | adjudicate: a wrong number does not verify | the tests T-008 adds (named in its pull request), run directly | absent | exit 0 |
| D-17 | read once | `python3 scripts/audit/scan_debt.py 2>&1 \| grep -E 'EXAMINED\|DEBT'` | a `DEBT:` line | no `DEBT:` line, or the debt OD-23's answer leaves, named |
| D-18 | synthesize: relations can be found and kept | `python3 scripts/db.py --help \| tr "," "\n" \| grep -c -E "synthesis-candidates\|relation-candidates"` | 0 | 1; and the relation rows of T-032 exist per OD-25 |
| D-19 | specify: a live determination the blocking gates examine | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select sum(retired_at is null) from specifications\").fetchall())"; cp data/guidebook.db "$SCRATCH/i.db" && GUIDEBOOK_DB_PATH="$SCRATCH/i.db" python3 scripts/tests/test_db_integrity.py > /dev/null; echo rc=$?` | no live row (the test passes on history only) | above 0, and `rc=0` |
| D-20 | render: a page exists and each claim traces to a row | the after-tests of `tasks/T-037-render.md` | nothing to open | green |
| D-21 | clean: skills describe what exists | `python3 scripts/audit/skill_vocabulary_audit.py > "$SCRATCH/sv.txt"; echo rc=$?; grep -E "EXAMINED\|FAIL\|PASS" "$SCRATCH/sv.txt" \| tail -2` | `rc=1` and a FAIL line | `rc=0` with `EXAMINED:` above 0 |
| D-22 | centralized: no helper with two homes | the evidence command in section 3 of `tasks/T-041-one-home-for-helpers.md` | several names | `{}` |
| D-23 | no typed counts in the registry | `grep -c -E '[0-9]+ today' governance/check-registry.yaml` | not 0 | 0 |
| D-24 | the database is what its migrations make | `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db" && python3 scripts/audit/migration_reproducibility.py --deep; echo rc=$?` | `rc=0` | `rc=0` |
| D-25 | the gates are sound | `python3 scripts/run_checks.py --selftest; echo rc=$?` | `rc=0` | `rc=0` |
| D-26 | every task is accounted for | `for f in workplan/2026-11-12-bidirectional-pipeline/tasks/T-[0-9]*-*.md; do echo "$f"; done` | the list | each is merged (its after-test is green on `main`) or declined in the owner's words in the ledger |
| D-27 | every owner decision is answered or deferred by the owner | `for n in $(grep -o -E '^### OD-[0-9]+' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md \| cut -c5-); do printf '%s %s\n' $n $(grep -c -F "$n:" references/project-standards.md); done` | every count is 0 | no count is 0 |

A line whose command a task changes (a renamed verb, a moved test) is updated in the same pull request; a prose caller is a caller.

## 11. What this plan does not settle

- Why `scripts/audit/doctrine_recheck.py` exits 1 when run bare while its battery is green (the registered invocation differs; inferred, not shown).
- The causes of three advisory failures standing on `main`: `test_scan_contract`, `validate_schema_cross_check`, `research_dod`. T-040 reads and reports them.
- Whether `add-source` refuses a NULL standing when a URL is given (not probed); T-007 closes it either way.
- Whether the order T-016, T-017, T-019 of the prior workplan is forced by the code or only by that plan; it is kept because it is the ruled plan.
- Which retained artefacts are a source's full text (OD-23 depends on it).
- Behaviour at a hundred times the present row counts.
- Not exercised by any stress round: candidate staging to admission, a citation-mining row, merging or declining a parameter that holds figures, a non-English source end to end.
- `scripts/run_checks.py --all` was never run in one call, by instruction; the ten batteries were run one at a time on a copy.
- `sessions/` was searched with `git grep`, not read end to end; an owner ruling that only lives there and matches none of the searches would be missing from this plan.
