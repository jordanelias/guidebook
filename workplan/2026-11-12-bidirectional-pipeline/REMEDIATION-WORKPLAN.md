# Remediation workplan: a pipeline that runs in every direction, at any stage, across languages and jurisdictions

_Written 2026-11-12 (UTC) by the handshake-and-adversarial leg of the bidirectional-pipeline audit. Planning only: no script, schema, governance file or database row was changed in writing it. Canadian English. Every figure is given as the command that produces it; re-run the command, do not trust a number._

## 0. Verdict

**Since this was written (2026-11-12, later the same day).** Twenty of the owner decisions were delegated to an Opus-class model, and the owner's twelfth instruction asked that the remaining ones be confirmed and, where appropriate, resolved before the plan is called complete. Which decisions stand, which hold up a task and which are answered is read from the ledger, never from this sentence: run the gate loop of section 13, or regenerate `REMEDIATION-PLAN.md` (its owner decision queue splits them into blocking, standing and open). Section 13 records the delegated pass and the gate; `DECISION-CLOSURE.md` records the twelfth-instruction pass, the decision-by-decision confirmation and a phone-ready prompt for every decision still the owner's.

**The owner's objective is not met today, and it can be met.** The objective (`grep -n -F "run in all directions" references/project-standards.md`): the pipeline "can be run in all directions at any stage in such a manner where we can dynamically research, adjudicate, synthesize, specify and render across a multitude of languages and jurisdictions". Three later statements of the same day add that the code be "efficient and centralized and clean", that the pipeline be flexible, glossed by the owner as having no "hard coded behaviours", and that it have no dead ends (`grep -n -E "^## Owner statement 2026-11-12" references/project-standards.md`).

What stands in the way, in order of harm to the book:

1. **A determination is computed without regard to the group it is for.** The engine gathers evidence by parameter alone. Fixed by the chain [T-016](tasks/T-016-wp-t1a-reading.md) → [T-017](tasks/T-017-wp-t2-conditions.md) → [T-018](tasks/T-018-link-table.md) → [T-019](tasks/T-019-lens-gather.md).
2. **Guards that a wrong figure or a misquote should not pass, pass it**: the number check (a figure written in words is now entered as a numeral, by the owner's ruling of 2026-11-12), the quote and name checks outside Latin script, a source admitted with no verification standing. [T-008](tasks/T-008-claimed-number-check.md), [T-009](tasks/T-009-script-aware-guards.md), [T-007](tasks/T-007-add-source-standing.md).
3. **The mobility group the owner decomposed by device is still one code**, and most figures sit on it. [T-055](tasks/T-055-mobility-family-tooling.md), [T-102](tasks/T-102-mobility-split.md) (OD-14 and OD-31 answered 2026-11-12).
4. **Nothing exists at render**, so every stage pair ending there has no path. [T-037](tasks/T-037-render.md), [T-038](tasks/T-038-stage-pair-gate.md) (its decisions resolved under delegation; OD-04, which held it through T-101 and T-036, answered by the owner on 2026-11-12).
5. **The base is English-shaped and its scope is in no table**: jurisdictions in code, scope unrecorded, forms unattested. [T-024](tasks/T-024-jurisdiction-registry.md), [T-025](tasks/T-025-base-writers.md), [T-026](tasks/T-026-alias-attestation.md), [T-101](tasks/T-101-scope-fill.md), [T-028](tasks/T-028-concept-identity.md).
6. **A step backward leaves no typed cause**: a gap does not say what it is a gap in. [T-013](tasks/T-013-typed-gaps.md), [T-012](tasks/T-012-follow-up-reasons.md), [T-022](tasks/T-022-contract-re-entry.md).
7. **A source must be re-read for every later parameter, parameters are flat, and synthesis finds nothing.** [T-031](tasks/T-031-clause-unit-and-open-pass.md), [T-029](tasks/T-029-term-relations.md), [T-032](tasks/T-032-synthesis-relations.md), [T-033](tasks/T-033-synthesis-candidates.md) (OD-23 answered by the owner: a clause inventory backed by retained text, a flagged re-read where neither reaches; the others' decisions are resolved under delegation).
8. **Text in other languages cannot be compared or discussed together**: nowhere holds a translation. [T-049](tasks/T-049-translation-home.md), [T-112](tasks/T-112-translate-held-text.md) (the owner asked for it on 2026-11-12; the target language, English for display, is resolved under delegation as OD-02).

**Start now:** the tasks of Wave 0 need no owner decision, no design and no earlier wave (section 4). **Then stop for the owner** at the points listed in section 6; the questions are in section 8, each with a one-line answer form.

## 1. What this folder holds, and which file governs

| File | What it is |
|---|---|
| `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md` | This index: order, dependencies, stop points, the owner decision register, the Definition of Done. |
| `workplan/2026-11-12-bidirectional-pipeline/tasks/T-<id>-<slug>.md` | One file per task, self-contained. Count them: `ls workplan/2026-11-12-bidirectional-pipeline/tasks/T-[0-9]*-*.md | grep -v -- -design | wc -l`. Ids are not contiguous (the hundreds are research tasks; unused numbers mean nothing). |
| `workplan/2026-11-12-bidirectional-pipeline/01-handshake-ledger.md` | The evidence base, requirement by requirement. **Where it differs from `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/fa-corrections-for-suite.md`, the corrections file governs.** One example: its headline that a wrong-group determination "passes every gate" is false; the blocking integrity check stops it for unverified governing sources, though for the wrong reason. |
| `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-PLAN.md` | The batches, lanes and owner queue, generated from the task files by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py`; never hand-edited. |
| `workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS.md` | The delegated resolutions of twenty register decisions, with the independent check's verdicts, the corrections applied, and the build plan (its last section). Not the owner's words. |
| `workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS-REVIEW.md` | The independent Opus-class review of OD-01, OD-02, OD-12 and OD-14 (delegation condition (d)). |
| `workplan/2026-11-12-bidirectional-pipeline/FOLD-LOG.md` | What the fold of the resolutions into this plan changed, file by file; the owner questions it raised (now register entries OD-31 to OD-35); what it could not resolve. |
| `workplan/2026-11-12-bidirectional-pipeline/DECISION-CLOSURE.md` | The twelfth-instruction pass: every register decision confirmed as blocking, standing or answered, with the commands; the plan issues found and fixed; a phone-ready prompt for each decision still the owner's, in the order of what it releases. |
| `workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md` | Every item still open in the plan after the fifth set of owner answers, classed (plan edit, new task, owner, execution, standing limit), with a resolution plan, a pilot plan and the owner questions that remain. |
| `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/` | The audit: `hs-handshake-matrix.md` (verdict per requirement), `hs-adversarial-findings.md`, `hs-improvement-programme.md` (each IMP entry, the acceptance tests, the final recommendations in §8 and the code-quality, flexibility and dead-end findings in §9), `hs-stress-audit.md` (three rounds of stress tests), `fa-corrections-for-suite.md`. A task file never requires you to open these. |
| `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/stress/` | The stress scripts and their logs, kept as a characterisation harness (`RETAINED.md` says what is kept and why). |

The seven further suite documents first planned are not written; the owner dropped that plan in favour of this one.

## 2. How to execute

0. **Merge this workplan first.** The task files assume the workplan is on the branch a task starts from. Until its pull request is merged to `main`, the integration base is whichever remote branch carries the newest commit to this folder; every task file sets `$BASE` by one line that names no branch (`origin/main` when `main` contains that commit, otherwise the first remote branch that does), and gates and measures against it. A task started from a `main` that lacks the workplan would diff the whole workplan: the pilots showed it.
1. **One task, one session, one pull request.** Pick the next task by section 4 or 5. Open its file. Read `CLAUDE.md`. Do exactly what the file says, in its order: preconditions, evidence, change, sweep, verification, commit, adversarial pass, pull request last.
2. **One pull request merges at a time** (the prior workplan's rule WR-1: `grep -n "WR-1" workplan/2026-10-23-pipeline-resolution-workplan.md`). Branches may be prepared side by side; each later one takes the merged predecessor with `git merge origin/main` and derives its migration number again. Merging is the owner's act unless the owner has said otherwise; an executor does not merge its own pull request and does not watch it (CLAUDE.md rule 9).
3. **Tooling before research, never together** (CLAUDE.md rule 10). A research task starts only when the tooling it names is on `main`.
4. **A task that is `NOT FOR SONNET`** waits for the Fable implementation agent (design) or an Opus-class session (judgment), as its first line says. The owner authorised the Fable agent to "design, author, curate, orchestrate, delete as required" for code, schema, scripts, checks and skills (`grep -n -F "design, author, curate, orchestrate" references/project-standards.md`); doctrine stays with the owner.
5. **When a task stops**, it reports what it ran, what it saw and what it expected, and changes nothing further. A stop is a result, not a failure. Do not work around it.
5a. **The first execution of an unpiloted task is its pilot.** All but three of the task files have never been executed (section 12 says which, by command). The executor of each ends the pull request body with a heading "Task-file defects" listing what in the file was wrong, missing or ambiguous, even when the change succeeded, so the files that follow can be corrected.
6. **When the ground has moved** (a task's evidence command no longer gives the output the file states), the task stops. Either the defect is already fixed, or an earlier merge changed the facts; the orchestrating session re-reads the task against `main` before anyone resumes it.
7. **Nothing in this plan loosens a refusal the project holds on purpose.** The two refusals CLAUDE.md §4 says must stay absent stay absent.

## 3. All tasks

**The Owner decisions column after the delegated pass:** "delegated" means resolved under delegation and read through the ledger gate of section 13, which a task runs before it starts; it is not the owner's answer, and the owner may reverse it at any time, which closes the gate again.

Generated from the task files; regenerate the same view with `grep -h -E "^\| (Task|Wave|Kind|Executor) " workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md`.

| Task | Title | Wave | Layer | Kind | Executor | Needs merged first | Owner decisions | Piloted |
|---|---|---|---|---|---|---|---|---|
| [T-001](tasks/T-001-layer0-marks-and-text.md) | Mark what is superseded, and make the Layer 0 commands run as written | 0 (now) | 0 | TOOLING | Sonnet | none | none | no |
| [T-002](tasks/T-002-contract-entry-text.md) | Make the contract entries say what the owner's stage order says | 0 (now) | 1 | TOOLING | Sonnet | none | none | no |
| [T-003](tasks/T-003-owner-queue-answered-marks.md) | One home for "answered" in the owner queue | 0 (now) | 0 | TOOLING | Sonnet | none | none | no |
| [T-004](tasks/T-004-spec-checks-report-live-rows.md) | Specification checks say how many of the rows they read are live | 0 (now) | 0 | TOOLING | Sonnet | none | none | no |
| [T-005](tasks/T-005-retired-row-view-fixture.md) | A seeded test that a retired determination is surfaced by no determination view | 0 (now) | 0 | TOOLING | Sonnet | none | none | no |
| [T-006](tasks/T-006-delete-connection-refusal.md) | `delete-connection` refuses an id that is not a row | 0 (now) | 2 | TOOLING | Sonnet | none | none | yes |
| [T-007](tasks/T-007-add-source-standing.md) | `add-source` writes a verification standing and a source type, or refuses | 0 (now) | 2 | TOOLING | Sonnet | none | none | no |
| [T-008](tasks/T-008-claimed-number-check.md) | The claimed number is checked as a number, and a number written in words is filed as a numeral | 0 (now) | 1-2 | TOOLING | Sonnet | none | none | in part |
| [T-009](tasks/T-009-script-aware-guards.md) | Quote and name guards that work outside Latin script | 0 (now) | 2 | TOOLING | Sonnet | none (after T-008 if both are open, to avoid conflicting edits) | none | no |
| [T-010](tasks/T-010-add-parameter-domain-refusal.md) | `add-parameter` refuses a term that is not a design quantity (first step) | 0 (now) | 2 | TOOLING | Sonnet | none | none | yes |
| [T-011](tasks/T-011-supersession-pointer.md) | Re-determining a cell points the retired row at its successor | 0 (now) | 2 | TOOLING | Sonnet | none | none | no |
| [T-012](tasks/T-012-follow-up-reasons.md) | Follow-up reasons for a skimmed figure and an absence finding | 0 (now) | 2 | TOOLING | Sonnet | none | none | no |
| [T-013](tasks/T-013-typed-gaps.md) | A gap says what it is a gap in, and a search says which gap caused it | 0 (now) | 1-2 | TOOLING | Sonnet | none | none | no |
| [T-014](tasks/T-014-stress-harness-and-probes.md) | Keep the stress scripts as a characterisation harness and their probes as tests | 0 (now) | 0 | TOOLING | Sonnet | none | none | no |
| [T-015](tasks/T-015-language-fold.md) | Language codes folded at the writers and in the coverage views | 0 (now) | 2 | TOOLING | Sonnet | none | none | no |
| [T-016](tasks/T-016-wp-t1a-reading.md) | The prior workplan's T-1a: reading (notation arithmetic to one home; the writer refuses prose units) | 1 (chain, first) | 2 | TOOLING | Sonnet | T-008 merged (it changes the same writer, and it built what replaces this task's numeral gloss) | none | no |
| [T-017](tasks/T-017-wp-t2-conditions.md) | The prior workplan's T-2: conditions become branches | 1 (chain) | 2 | TOOLING | Sonnet | T-016 merged | none | no |
| [T-018](tasks/T-018-link-table.md) | The link table for several codes of one model on a figure | 1 (chain) | 1 | TOOLING | Sonnet (executing `T-018-design.md`) | T-017 merged; `T-018-design.md` present (written 2026-11-12) | OD-39 (answered 2026-11-12, fifth set: the link table supersedes the 2026-08-28 clause) | no |
| [T-019](tasks/T-019-lens-gather.md) | The engine gathers by the lens tags on the figure (the prior workplan's T-3) | 1 (chain, last) | 2 | TOOLING | Sonnet | T-016, T-017, T-018 merged | none outstanding (OD-08 resolved under delegation) | no |
| [T-020](tasks/T-020-quantity-kind.md) | A parameter states what kind of quantity it is | 1 | 1-2 | TOOLING | Sonnet | T-010 merged | none outstanding (OD-24 delegated) | no |
| [T-021](tasks/T-021-cell-question-gate.md) | A question about a published cell can be recorded and flags the cell | 2 | 2 | TOOLING | Sonnet | T-019 merged | none outstanding (OD-21 delegated) | no |
| [T-022](tasks/T-022-contract-re-entry.md) | Re-entry conditions in the pipeline contract | 2 | 1 | TOOLING | Sonnet | T-002, T-012, T-013 merged | none outstanding (OD-18, OD-08 delegated) | no |
| [T-023](tasks/T-023-ledger-relayed-statements.md) | Enter the relayed statements of 2026-10-12 in the ledger | 2 | 0 | TOOLING | Sonnet | none | OD-28 (answered 2026-11-12) | no |
| [T-024](tasks/T-024-jurisdiction-registry.md) | Jurisdictions in a table the writers read | 3 | 1 | TOOLING | Sonnet | none | none outstanding (OD-01 delegated; OD-04 answered: item 5) | no |
| [T-025](tasks/T-025-base-writers.md) | Writers for the base tables a ruled task must write | 3 | 2 | TOOLING | Sonnet | T-024 merged | none | no |
| [T-026](tasks/T-026-alias-attestation.md) | A form says how it is attested, and a search says which forms it used | 3 | 1-2 | TOOLING | Sonnet | none; `T-028-design.md` present | none | no |
| [T-027](tasks/T-027-source-identity-edition.md) | The source's own title, edition and currency can be written | 3 | 2 | TOOLING | Sonnet | none | none | no |
| [T-028](tasks/T-028-concept-identity.md) | A concept that is not an English string | 3 | 1 | TOOLING | NOT FOR SONNET | T-026 merged | OD-38 (answered 2026-11-12, fifth set: the first English name recorded is shown until a named judge picks); OD-03 delegated | no |
| [T-029](tasks/T-029-term-relations.md) | Typed pointers between terms | 4 | 1 | TOOLING | Sonnet | T-020 merged | none | no |
| [T-030](tasks/T-030-units-as-data.md) | Units and their exact conversions as rows | 4 | 1-2 | TOOLING | Sonnet | T-016, T-020 merged | none outstanding (OD-22, OD-24 delegated) | no |
| [T-031](tasks/T-031-clause-unit-and-open-pass.md) | The clause as a unit, the open pass, and catalogue growth | 4 | 1-2 | TOOLING | NOT FOR SONNET | T-019 merged | OD-23 (answered 2026-11-12) | no |
| [T-032](tasks/T-032-synthesis-relations.md) | Relations synthesis can record, and what a synthesis row is | 4 | 1 | TOOLING | NOT FOR SONNET | T-029, T-050 merged | none outstanding (OD-19 answered: record now; OD-07, OD-12, OD-25, OD-29 delegated; OD-19 moved to T-053) | no |
| [T-033](tasks/T-033-synthesis-candidates.md) | Candidate relations on demand (read-only) | 4 | 2 | TOOLING | Sonnet | T-029, T-030 merged | none | no |
| [T-034](tasks/T-034-cell-status-verb.md) | One read-only answer for a cell at every stage | 4 | 2 | TOOLING | Sonnet | T-013 merged | none | no |
| [T-035](tasks/T-035-skills-repair.md) | Skills that describe the database that exists | 4 | 2 | TOOLING | Sonnet | none for token corrections | none | no |
| [T-036](tasks/T-036-jurisdiction-comparison-view.md) | The jurisdiction comparison as a view | 5 | 1 | TOOLING | Sonnet | T-024 merged; T-101 merged | none outstanding (OD-01 delegated; OD-04 answered, through T-101) | no |
| [T-037](tasks/T-037-render.md) | Render from the database | 5 | 2 | TOOLING | NOT FOR SONNET | T-019, T-032, T-036, T-049 merged | none outstanding (OD-02, OD-08, OD-12, OD-30, OD-33 delegated) | no |
| [T-038](tasks/T-038-stage-pair-gate.md) | Register the stage-pair gate | 5 | 0 | TOOLING | Sonnet | T-037 merged (a render view mapped to the render stage) | none outstanding (OD-26 delegated: wait) | no |
| [T-039](tasks/T-039-owner-edits.md) | The owner's edits as proposals through the write path | 5 | 2 | TOOLING | NOT FOR SONNET | T-021, T-037 merged | none outstanding (OD-20 delegated) | no |
| [T-040](tasks/T-040-deletion-candidates-sweep.md) | Caller sweep for the deletion candidates | 5 | 2 | TOOLING | Sonnet | T-013, T-032 merged | none | no |
| [T-041](tasks/T-041-one-home-for-helpers.md) | One home for helpers defined twice | 0 (now) | 2 | TOOLING | Sonnet | T-014 merged (the harness is the proof) | none | no |
| [T-042](tasks/T-042-derive-choices-and-counts.md) | Counts in the registry as commands, and one Layer 0 measure corrected | 0 (now) | 0-2 | TOOLING | Sonnet | none | none | no |
| [T-043](tasks/T-043-refusals-name-next-action.md) | Every refusal says what to do next | 0 (now) | 2 | TOOLING | Sonnet | T-014 merged | none | no |
| [T-047](tasks/T-047-add-by-data-test.md) | A durable test that the base changes by data alone | 3 (end) | 0 | TOOLING | Sonnet | T-015, T-020, T-024, T-025, T-029 merged | none | no |
| [T-048](tasks/T-048-root-registry-writer.md) | A writer for the root registry | 2 | 2 | TOOLING | Sonnet | none | none | no |
| [T-049](tasks/T-049-translation-home.md) | A typed home for translations, attached by pointer and callable from any stage | 2 | 1-2 | TOOLING | Sonnet | T-008 merged (the fidelity rule uses its number reader) | none (OD-30 delegated: the review rule) | no |
| [T-050](tasks/T-050-retire-admission-edges-and-connections.md) | Admission edges and connections retire in place instead of being deleted | 2 | 2 | TOOLING | Sonnet | T-006 merged | none outstanding (OD-29 delegated) | no |
| [T-051](tasks/T-051-gap-register-cross-stage.md) | The gap register is marked cross-stage in the stage map | 0 (now) | 1 | TOOLING | Sonnet | none | none outstanding (OD-11 delegated) | no |
| [T-052](tasks/T-052-mining-stages-out-of-scope-leads.md) | Mining stages an out-of-scope source as a lead | 0 (now) | 2 | TOOLING | Sonnet | none | none outstanding (OD-05 delegated; OD-04 and OD-34 answered) | no |
| [T-053](tasks/T-053-engine-conflict-between-groups.md) | Conflict between groups in the engine | 4 | 2 | TOOLING | NOT FOR SONNET | T-032 merged | none outstanding (OD-19 and OD-36 answered 2026-11-12) | no |
| [T-054](tasks/T-054-identity-retires-to-need.md) | An identity code can be retired to the access need that carries it (and, since the OI-13 fold, to another identity code; crossing rows retire in place) | 2 | 1-2 | TOOLING | Sonnet | none | none outstanding (OD-37 answered; OI-13 answered, sixth to ninth sets) | no |
| [T-055](tasks/T-055-mobility-family-tooling.md) | Tooling for the mobility family: the devices it needs, and a parent's determination that gathers its children | 4 | 1-2 | TOOLING | Sonnet | T-019 merged; `T-102-design.md` present | none outstanding (OD-14 answered) | no |
| [T-056](tasks/T-056-all-leaves-identity-lens.md) | ALL leaves the identity lens: universal is stated once, by design_scale | 2 | 1-2 | TOOLING | Sonnet | T-054 merged | none outstanding (OD-31 answered) | no |
| [T-101](tasks/T-101-scope-fill.md) | Record the research scope on every pair | research | 3 | RESEARCH | Sonnet | T-025 merged | OD-04 (answered 2026-11-12; and OD-01 delegated) | no |
| [T-102](tasks/T-102-mobility-split.md) | Decompose the mobility family by device, and carry the rows filed under MOB | research | 3 | RESEARCH | NOT FOR SONNET | T-018, T-025, T-054, T-055 merged; `T-102-design.md` present | none outstanding (OD-14 and OD-31 answered 2026-11-12; the codes confirmed in the fifth set and revised in the sixth to ninth: children `WHEEL`, `LLD`, `WALKAID`; `SCI` retired to `WHEEL`) | no |
| [T-103](tasks/T-103-medical-lens.md) | Fill the medical lens by correspondence | research | 3 | RESEARCH | NOT FOR SONNET | none (`add-medical` exists) | OD-15 (answered 2026-11-12: proceed, no WHO agreement sought) | no |
| [T-104](tasks/T-104-verify-governing-sources.md) | Verify the sources a first determination would rest on | research | 3 | RESEARCH | Sonnet | none | none | no |
| [T-105](tasks/T-105-read-held-sources.md) | Read what is held, in full, against every parameter | research | 3 | RESEARCH | NOT FOR SONNET | T-008, T-009, T-016, T-031 merged (OD-23 chose the inventory) | none outstanding (OD-05 delegated) | no |
| [T-106](tasks/T-106-retag-lenses.md) | Tag figures with every relevant model | research | 3 | RESEARCH | NOT FOR SONNET | T-019 merged | none outstanding (OD-06 delegated; mobility codes wait for OD-14) | no |
| [T-107](tasks/T-107-attest-forms.md) | Attest forms per language and jurisdiction from instruments | research | 3 | RESEARCH | NOT FOR SONNET | T-026, T-028 merged | none | no |
| [T-108](tasks/T-108-unit-condition-repair.md) | Move conditions out of the unit cell | research | 3 | RESEARCH | Sonnet | T-016 merged; T-008 merged | none | no |
| [T-109](tasks/T-109-parameter-kinds-data.md) | Give the live parameters their quantity kind | research | 3 | RESEARCH | NOT FOR SONNET | T-020 merged | none outstanding (OD-24 delegated) | no |
| [T-110](tasks/T-110-first-determinations.md) | First live determinations | research | 3 | RESEARCH | NOT FOR SONNET | T-019, T-102, T-104 merged | none | no |
| [T-111](tasks/T-111-as-written-wording-for-stored-rows.md) | Bring the two stored spelled-out figures into line | research | 3 | RESEARCH | Sonnet | T-008 merged | none | no |
| [T-112](tasks/T-112-translate-held-text.md) | Translate the held non-English text that synthesis needs | research | 3 | RESEARCH | Sonnet (drafting); a review verdict is Opus-class | T-049 merged | none outstanding (OD-02, OD-30 delegated) | no |
| [T-113](tasks/T-113-file-sub-national-instruments.md) | File the four held sub-national instruments under their own codes | research | 3 | RESEARCH | Sonnet | T-024 merged | none outstanding (OD-01 delegated; OD-04 answered) | no |
| [T-114](tasks/T-114-retire-move-ves-to-needs.md) | Retire MOVE and VES to the access needs that carry them | research | 3 | RESEARCH | Sonnet | T-054 merged | none outstanding (OD-37 answered) | no |
| [T-116](tasks/T-116-upl-for-upper-limb.md) | Hold the upper-limb population as UPL, and retire LMB to it | research | 3 | RESEARCH | Sonnet | T-025, T-054 merged | none outstanding (OI-13 answered, eighth and ninth sets; `UPL`'s wording and category are proposals the owner confirms) | no |
| [T-058](tasks/T-058-upl-prose-callers.md) | UPL reinstated for upper limb: the retired crosswalk and the prose that names LMB or UPL | 3 | 0-1 | TOOLING | Sonnet | T-116 merged | none outstanding (OI-13 answered) | no |
| [T-057](tasks/T-057-base-coverage-view.md) | The base coverage view: one state per concept and in-scope pair | 3 | 2 | TOOLING | Sonnet | T-026, T-028 merged | none (the owner's 2026-11-06 acceptance test, AT-23) | no |
| [T-059](tasks/T-059-wp-t4-agreement.md) | The prior workplan's T-4: agreement (true exclusion causes, recorded divergence, the fragility note) | 1 | 2 | TOOLING | NOT FOR SONNET | T-016, T-019 merged | none in the register (OR-4, OR-6, OR-6b, OR-6c answered; OR-5b's edges open and held out of this task) | no |
| [T-060](tasks/T-060-element-determination.md) | The specifications pass writes an element-level determination (OR-14b) | 5 | 2 | TOOLING | NOT FOR SONNET | T-019, T-029 merged; design file first | none (OR-14b answered 2026-11-13) | no |
| [T-115](tasks/T-115-retag-all-rows.md) | Re-tag the figures filed under ALL by their heading's group, then retire ALL | research | 3 | RESEARCH | NOT FOR SONNET | T-018, T-056 merged | none outstanding (OD-31 answered) | no |

## 4. Wave 0: what can start now

**No owner decision, no design, no earlier wave.** The set, by command: `grep -l "^| Wave | 0 (now) |" workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md`. Today that is: [T-001](tasks/T-001-layer0-marks-and-text.md), [T-002](tasks/T-002-contract-entry-text.md), [T-003](tasks/T-003-owner-queue-answered-marks.md), [T-004](tasks/T-004-spec-checks-report-live-rows.md), [T-005](tasks/T-005-retired-row-view-fixture.md), [T-006](tasks/T-006-delete-connection-refusal.md), [T-007](tasks/T-007-add-source-standing.md), [T-008](tasks/T-008-claimed-number-check.md), [T-009](tasks/T-009-script-aware-guards.md), [T-010](tasks/T-010-add-parameter-domain-refusal.md), [T-011](tasks/T-011-supersession-pointer.md), [T-012](tasks/T-012-follow-up-reasons.md), [T-013](tasks/T-013-typed-gaps.md), [T-014](tasks/T-014-stress-harness-and-probes.md), [T-015](tasks/T-015-language-fold.md), [T-041](tasks/T-041-one-home-for-helpers.md), [T-042](tasks/T-042-derive-choices-and-counts.md), [T-043](tasks/T-043-refusals-name-next-action.md), [T-051](tasks/T-051-gap-register-cross-stage.md), [T-052](tasks/T-052-mining-stages-out-of-scope-leads.md) (the last two added by the delegated pass).

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
18. [T-051](tasks/T-051-gap-register-cross-stage.md) (the stage map; run the walkability instrument before and after)
19. [T-052](tasks/T-052-mining-stages-out-of-scope-leads.md) (two skills; no code)
20. [T-043](tasks/T-043-refusals-name-next-action.md) (last: by then the new refusals of T-006, T-007, T-008 and T-010 exist and must also name a next action)

**What may be drafted side by side** (files touched decide it; merge is still one at a time):

| Group | Tasks | They share |
|---|---|---|
| Writers | T-006, T-007, T-008, T-009, T-010, T-041, T-043 | `scripts/db.py`: draft in sequence, or expect a merge each time |
| Engine | T-011, T-013, T-041 | `scripts/assess/assess_cell.py` |
| Schema | T-012, T-013, T-015 | the next migration number (derived at execution time, again after each merge) |
| Layer 0 text | T-001, T-002, T-042, T-003 | `CLAUDE.md`, `governance/pipeline-contract.yaml`, `governance/check-registry.yaml` |
| Independent | T-004, T-005, T-014, T-051, T-052 | nothing with the others |

**Also free of any precondition, placed later only for order:** [T-027](tasks/T-027-source-identity-edition.md) (tooling), [T-035](tasks/T-035-skills-repair.md) (tooling), [T-048](tasks/T-048-root-registry-writer.md) (tooling), [T-104](tasks/T-104-verify-governing-sources.md) (research). Any of them may be pulled forward. ([T-026](tasks/T-026-alias-attestation.md) is READY: T-028's one-page forms-home design, `tasks/T-028-design.md`, exists, so a form has one home.) By command (`REMEDIATION-PLAN.md` agrees; trust the command over this list): `grep -L "Owner decisions that must be answered first" workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md | xargs grep -l "merged to .main. first:\*\* none" | xargs grep -L "NOT FOR SONNET"`.

## 5. Later waves, the dependency graph and the critical path

**Critical path to a first live determination that is for the group it names:**

[T-014](tasks/T-014-stress-harness-and-probes.md) → [T-008](tasks/T-008-claimed-number-check.md) → [T-016](tasks/T-016-wp-t1a-reading.md) → [T-017](tasks/T-017-wp-t2-conditions.md) → [T-018](tasks/T-018-link-table.md) → [T-019](tasks/T-019-lens-gather.md) → { [T-104](tasks/T-104-verify-governing-sources.md), [T-102](tasks/T-102-mobility-split.md), [T-106](tasks/T-106-retag-lenses.md) } → [T-110](tasks/T-110-first-determinations.md).

One link on it is not Sonnet's to start: T-102 is an Opus-class session. Its design (`tasks/T-102-design.md`) and T-018's (`tasks/T-018-design.md`) are written. The owner confirmed T-102's codes and edges on 2026-11-12 (fifth set, "Confirm all as proposed"), which discharges the report T-102 was to make before any row; T-102 waits only for T-018, T-025 and T-055 to merge (OD-14 and OD-31 were answered on 2026-11-12). The children's ICF crossings are not named by that answer and are not written until the owner says so (`OPEN-ITEMS-PLAN.md`).

| Wave | Purpose | Tasks | Order inside the wave |
|---|---|---|---|
| 1 | the lens chain and the parameter kind | [T-016](tasks/T-016-wp-t1a-reading.md), [T-017](tasks/T-017-wp-t2-conditions.md), [T-018](tasks/T-018-link-table.md), [T-019](tasks/T-019-lens-gather.md), [T-059](tasks/T-059-wp-t4-agreement.md), [T-020](tasks/T-020-quantity-kind.md) | Serial: T-016, T-017, T-018, T-019, T-059. T-020 beside them (OD-24 resolved under delegation). |
| 2 | carriers for going back, and for translation | [T-021](tasks/T-021-cell-question-gate.md), [T-022](tasks/T-022-contract-re-entry.md), [T-023](tasks/T-023-ledger-relayed-statements.md), [T-048](tasks/T-048-root-registry-writer.md), [T-049](tasks/T-049-translation-home.md), [T-050](tasks/T-050-retire-admission-edges-and-connections.md) | T-048 any time; T-049 after T-008; T-050 after T-006; T-021 after T-019; T-022 after its three; T-023 any time (OD-28 answered). |
| 3 | a base that is data | [T-024](tasks/T-024-jurisdiction-registry.md), [T-025](tasks/T-025-base-writers.md), [T-026](tasks/T-026-alias-attestation.md), [T-027](tasks/T-027-source-identity-edition.md), [T-028](tasks/T-028-concept-identity.md), [T-047](tasks/T-047-add-by-data-test.md), [T-057](tasks/T-057-base-coverage-view.md) | T-024 then T-025; T-027 any time; T-028's one-page design first, then T-026, then T-028's build; T-047 last. |
| 4 | reading once, abstraction, synthesis | [T-029](tasks/T-029-term-relations.md), [T-030](tasks/T-030-units-as-data.md), [T-031](tasks/T-031-clause-unit-and-open-pass.md), [T-032](tasks/T-032-synthesis-relations.md), [T-033](tasks/T-033-synthesis-candidates.md), [T-034](tasks/T-034-cell-status-verb.md), [T-035](tasks/T-035-skills-repair.md), [T-053](tasks/T-053-engine-conflict-between-groups.md) | T-034 after T-013; T-035 any time; T-029 after T-020; T-030 and T-032 after their dependencies (their decisions are delegated); T-031 after T-019 (OD-23 answered); T-033 after T-029 and T-030. T-053 after T-032 (OD-36 answered). |
| 5 | render and the gate over it | [T-036](tasks/T-036-jurisdiction-comparison-view.md), [T-037](tasks/T-037-render.md), [T-038](tasks/T-038-stage-pair-gate.md), [T-039](tasks/T-039-owner-edits.md), [T-040](tasks/T-040-deletion-candidates-sweep.md), [T-060](tasks/T-060-element-determination.md) | T-036 after T-024 and T-101 (OD-04 answered); T-037 after its four dependencies; T-038 after T-037; T-039; T-040. |
| research | rows, each in its own pull request | [T-101](tasks/T-101-scope-fill.md), [T-102](tasks/T-102-mobility-split.md), [T-103](tasks/T-103-medical-lens.md), [T-104](tasks/T-104-verify-governing-sources.md), [T-105](tasks/T-105-read-held-sources.md), [T-106](tasks/T-106-retag-lenses.md), [T-107](tasks/T-107-attest-forms.md), [T-108](tasks/T-108-unit-condition-repair.md), [T-109](tasks/T-109-parameter-kinds-data.md), [T-110](tasks/T-110-first-determinations.md), [T-111](tasks/T-111-as-written-wording-for-stored-rows.md), [T-112](tasks/T-112-translate-held-text.md), [T-113](tasks/T-113-file-sub-national-instruments.md) | T-104 is ungated; T-111 follows T-008 and T-108 follows T-016; the rest wait for tooling, an answer, or an Opus-class session. T-113 follows T-024. |

**Dependency list** (a task on the left needs every task on the right merged; generated from the task files):

```
T-016 <- T-008
T-017 <- T-016
T-018 <- T-017; the design file `tasks/T-018-design.md` (written 2026-11-12)   [owner: OD-39, answered]
T-019 <- T-016, T-017, T-018   [delegated: OD-08]
T-020 <- T-010   [delegated: OD-24]
T-021 <- T-019   [delegated: OD-21]
T-022 <- T-002, T-012, T-013   [delegated: OD-18, OD-08]
T-023 <- (no task)   [owner: OD-28, answered]
T-024 <- (no task)   [delegated: OD-01; owner: OD-04, answered]; item 4 (amend-extraction takes jurisdiction) is what T-113 needs
T-025 <- T-024
T-026 <- (no task); the forms-home design file `tasks/T-028-design.md` (written first under T-028 item 2)
T-028 <- T-026   [delegated: OD-03; owner: OD-38, answered]
T-029 <- T-020
T-030 <- T-016, T-020   [delegated: OD-22, OD-24]
T-031 <- T-019   [owner: OD-23, answered]
T-032 <- T-029, T-050   [delegated: OD-07, OD-12, OD-25, OD-29; owner: OD-19, answered (record now)]
T-033 <- T-029, T-030
T-034 <- T-013
T-036 <- T-024, T-101   [delegated: OD-01; owner: OD-04, answered, through T-101]
T-037 <- T-019, T-032, T-036, T-049   [delegated: OD-02, OD-08, OD-12, OD-30, OD-33]
T-038 <- T-037   [delegated: OD-26 (wait)]
T-039 <- T-021, T-037   [delegated: OD-20]
T-040 <- T-013, T-032
T-041 <- T-014
T-043 <- T-014
T-047 <- T-015, T-020, T-024, T-025, T-029
T-049 <- T-008   [delegated: OD-30]
T-050 <- T-006   [delegated: OD-29]
T-051 <- (no task)   [delegated: OD-11]
T-052 <- (no task)   [delegated: OD-05; owner: OD-04, OD-34, answered]
T-053 <- T-032   [owner: OD-19 and OD-36, answered]
T-054 <- (no task)   [owner: OD-37, answered]
T-055 <- T-019; the design `tasks/T-102-design.md`   [owner: OD-14, answered]
T-056 <- T-054   [owner: OD-31, answered]
T-101 <- T-025   [owner: OD-04, answered; delegated: OD-01]
T-102 <- T-018, T-025, T-054, T-055; the design `tasks/T-102-design.md`, its codes confirmed by the owner (fifth set); an Opus-class session   [owner: OD-14, OD-31, OD-37, answered]
T-103 <- (no task)   [owner: OD-15, answered]
T-105 <- T-008, T-009, T-016, T-031   [delegated: OD-05; T-031 hard since OD-23 chose the inventory]
T-106 <- T-019   [delegated: OD-06]
T-107 <- T-026, T-028, T-057
T-108 <- T-008, T-016
T-109 <- T-020   [delegated: OD-24]
T-110 <- T-019, T-059, T-102, T-104; the owner's confirmation of the T-102 codes (fifth set, in the ledger); the blocking battery green on the scratch copy; an Opus-class session
T-111 <- T-008
T-112 <- T-049   [delegated: OD-02, OD-30]
T-113 <- T-024   [delegated: OD-01; owner: OD-04, answered]
T-114 <- T-054   [owner: OD-37, answered]
T-115 <- T-018, T-056   [owner: OD-31, answered]
T-116 <- T-025, T-054   [OI-13, answered]
T-058 <- T-116   [OI-13, answered]
T-057 <- T-026, T-028
T-059 <- T-016, T-019
T-060 <- T-019, T-029; the design `tasks/T-060-design.md`   [owner: OR-14b, answered 2026-11-13]
```

## 6. Stop points

| When | Who is waited for | What for | What can continue meanwhile |
|---|---|---|---|
| Before T-018 | DISCHARGED 2026-11-12: the design of the link table is written (`tasks/T-018-design.md`) | nothing further; T-018 is Sonnet's | — |
| Before T-026 | DISCHARGED 2026-11-12: the forms-home design of T-028 is written (`tasks/T-028-design.md`) and names the one table that holds a form (`term_aliases`) | nothing further for T-026; T-028 itself stays NOT FOR SONNET | — |
| Before T-102, and so T-110 | DISCHARGED 2026-11-12 as to the owner: the design is written and the owner confirmed its codes and edges (fifth set), so no report is appended. STILL OUTSTANDING: T-018, T-025 and T-055 merge | nothing from the owner (the children's ICF crossings alone wait for an explicit yes, and block no row) | T-104; T-106 after T-019 (ICF and needs lenses only); T-054, T-114 |
| Before T-110 | the blocking battery, green on the scratch copy, the integrity test included | a first live determination | — |
| At the end of every wave | the owner | the wave's lines of the Definition of Done (section 10), run and reported; `python3 workplan/pipeline-state-graph/walkability.py` run as a command until T-038 registers it | — |
| Whenever a task's delegation gate prints CLOSED | the owner, or the correction that closed it | the decision that gate reads (section 13) | every task whose gates are OPEN |
| At any time | the owner | anything touching mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction scope, licensing or trajectory | — |

## 7. Three tracks across the waves

The measurements behind this section are in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md` §9. **What counts as hard-coded** was sharpened by the owner on 2026-11-12: "we can set a rule for synthesis to translate, which isn't hardcoding necessarily" (`grep -n -F "isn't hardcoding necessarily" references/project-standards.md`). So: a behaviour declared **once** as a rule, in a stated place (a column's CHECK, a table, the pipeline contract, the check registry, one named constant), and read from there, is **not** hard-coding. A literal, a fixed list or a branch on a name that is typed in more than one place, or typed in code where a table, a CHECK, the contract or the registry already holds it, **is**. The word "necessarily" leaves the line open and the reading is the audit's. A dead end is a row, state, path, stage or refusal with no sanctioned way onward, back or out (also the audit's reading). The measures below therefore ask two things of a rule: that it is declared once, and that its values are not typed again elsewhere. They do not flag a rule for existing.

```
for r in NON_QUANTITY_DOMAINS QUANTITY_CLAIM_TYPES NOTATION_FAMILIES RULE_VERSION JurisdictionCode; do printf '%s declared %s time(s)\n' $r "$(git grep -n -E "^\s*(class )?$r\b\s*(=|\()" -- scripts schemas | wc -l)"; done   # each 0 or 1
git grep -n -e "'functional_axis'" -e '"functional_axis"' -- scripts schemas ':(exclude)scripts/tests' ':(exclude)scripts/migrations'   # a rule's values typed as a literal outside its home: none today; after T-010, one line, in dbcore
```

| Track | Owner statement | Finding | Tasks | Proof |
|---|---|---|---|---|
| Efficient | REQ-101 | Measured and sufficient: a verb and a determination take well under a second, a rebuild about two seconds, the diff-scoped gate about two minutes once per pull request. Not measured: a hundred times the present rows. | none proposed | timings in the stress logs (`stress/results2/`, `stress/results3/`) |
| Centralized | REQ-101 | Helpers defined twice; jurisdictions and unit families as lists in code; typed counts in the registry. The command-line value lists are already read from the schema. | [T-041](tasks/T-041-one-home-for-helpers.md), [T-042](tasks/T-042-derive-choices-and-counts.md), [T-024](tasks/T-024-jurisdiction-registry.md), [T-030](tasks/T-030-units-as-data.md) | T-041's command prints `{}`; the stress logs are identical before and after (T-014's `stress_diff.py`) |
| Clean | REQ-101 | Skills naming structures that are gone; a verb that reports success having done nothing; a documented command that does not run; checks whose prose contradicts the data; dead apparatus. | [T-035](tasks/T-035-skills-repair.md), [T-006](tasks/T-006-delete-connection-refusal.md), [T-001](tasks/T-001-layer0-marks-and-text.md), [T-004](tasks/T-004-spec-checks-report-live-rows.md), [T-040](tasks/T-040-deletion-candidates-sweep.md) | `skill_vocabulary_audit` exits 0; each task's after-test |
| Declined | REQ-101 | Splitting `scripts/db.py`: no measured cost saved, every import and ledger reference changed. | none | revisit only on a measured problem |
| No hard-coded behaviour | REQ-102 | Jurisdictions (two homes: an enum and a table that disagree), scope (in no home), lens selection (ignored), units (the engine's own copy), what may be a parameter (no rule). Already data-driven and kept: the check registry, vocabularies read from the column's CHECK, the derived capture set, one home for stage ids. | [T-024](tasks/T-024-jurisdiction-registry.md), [T-025](tasks/T-025-base-writers.md), [T-101](tasks/T-101-scope-fill.md), [T-019](tasks/T-019-lens-gather.md), [T-030](tasks/T-030-units-as-data.md), [T-010](tasks/T-010-add-parameter-domain-refusal.md), [T-020](tasks/T-020-quantity-kind.md), [T-029](tasks/T-029-term-relations.md), [T-047](tasks/T-047-add-by-data-test.md) | the add-by-data test (T-047): a language and jurisdiction pair, a jurisdiction, a term, a parameter and a term pointer are added by sanctioned verbs with no file under `scripts/` or `schemas/` changed |
| Translation, wherever it is needed | REQ-104 (owner, ninth and tenth statements of 2026-11-12) | Nothing holds a translation. A number written in words is entered as a numeral at extraction with the wording kept in its own column (T-008); everything else is translated when a stage needs it, by default at synthesis, and that default is one line in the pipeline contract. One design at both grains: the source's wording is kept in a cell that names it, our rendering in a cell that names it as ours, the writer checks against the verified bytes, and the translator is recorded. | [T-008](tasks/T-008-claimed-number-check.md), [T-049](tasks/T-049-translation-home.md), [T-111](tasks/T-111-as-written-wording-for-stored-rows.md), [T-112](tasks/T-112-translate-held-text.md) | AT-107 (translate from a stage other than synthesis, by data alone; the original unchanged; the pointer resolves), AT-108 (changing the rule's one home changes the behaviour with no code edit), AT-109 (a translation that changes a figure is refused) |
| No dead ends: structural | REQ-103 | Stage pairs ending at render; the root registry and the base tables with no writer; the empty medical lens. | [T-037](tasks/T-037-render.md), [T-038](tasks/T-038-stage-pair-gate.md), [T-048](tasks/T-048-root-registry-writer.md), [T-025](tasks/T-025-base-writers.md), [T-103](tasks/T-103-medical-lens.md) | walkability prints no `NO PATH`; CLAUDE.md §4's derivation prints no `UNWRITABLE` line that is not intended |
| No dead ends: state | REQ-103 | A retired determination with no successor; a `pending` row nothing will fill; a new parameter's owed readings where no text is held. | [T-011](tasks/T-011-supersession-pointer.md), [T-019](tasks/T-019-lens-gather.md), [T-031](tasks/T-031-clause-unit-and-open-pass.md) | each task's after-test |
| No dead ends: operational | REQ-103 | Refusals that name no next action; a silent no-op; a command that does not run as written. | [T-043](tasks/T-043-refusals-name-next-action.md), [T-006](tasks/T-006-delete-connection-refusal.md), [T-001](tasks/T-001-layer0-marks-and-text.md) | every distinct refusal the harness produces names a next action |
| No dead ends: reader and process | REQ-103 | No carrier for a question about a published cell; no rendered claim to trace; skills pointing at deleted structures; an answered prompt shown as open. | [T-021](tasks/T-021-cell-question-gate.md), [T-037](tasks/T-037-render.md), [T-035](tasks/T-035-skills-repair.md), [T-003](tasks/T-003-owner-queue-answered-marks.md) | each task's after-test |

A deliberate refusal is not a dead end and is not loosened: one research batch at a time (the capture refuses a batch drafted from an older base; the owner answered OD-27 on 2026-11-12: serial is fine), and the two absent refusals of CLAUDE.md §4.

## 8. Owner decision register

**Status after the delegated pass and the twelfth-instruction pass (2026-11-12).** Each entry below opens with its status. How many are resolved under delegation, referred back, still the owner's, or block a task is derived, never typed: run the gate loop of section 13 for the state of each, and `python3 -I scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py` for which of the CLOSED ones a task waits on (its last-but-one output line names the blocking and the standing sets; `REMEDIATION-PLAN.md` shows them with the tasks they release). The confirmation of each, with evidence, is `DECISION-CLOSURE.md`. A task no longer checks `grep -n -F "OD-NN:"`, which a delegated, a withdrawn and an owner's line all satisfied alike: it runs the ledger gate of section 13, which is OPEN only for an owner's answer, or for a delegated resolution whose independent check is not required or is recorded as confirmed. A task that needs the owner's words (T-102, T-053) opens only on an owner's answer. The rest of this register is as first written, so "Recommendation (the audit's …)" and "Tasks blocked until answered" describe the state before the pass; the status line says what holds now.

Each entry was written as **OWNER DECISION REQUIRED**; its status line says what holds now, and each recommendation is labelled as one. To answer, the owner says one of the answer forms; the session that hears it appends to `references/project-standards.md`, in the ledger's form, the owner's quoted words, the answer line `OD-NN: …`, and the status line with the value `ANSWERED BY THE OWNER` (a deferral takes `DEFERRED BY THE OWNER`; ledger convention and its addendum: `grep -n -F "Convention" references/project-standards.md | tail -2`). A task opens on the status line read through the gate of section 13, never on the `OD-NN:` line alone. OD-16 was withdrawn (it was answered on the record). Count the entries: `grep -c "^### OD-" workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md`.

**Which answers release the most work:** derived, not listed here: the "Blocking" table of `REMEDIATION-PLAN.md` gives, for each CLOSED decision a task waits on, the tasks it holds and every task waiting on those; `DECISION-CLOSURE.md` orders the owner's prompts by it. These ids belong to this plan; an older series with the same letters appears in `decisions/` and is unrelated.

### OD-01  Jurisdiction in a determination; jurisdictions below the country; climate and culture

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check (condition (d)) recorded as confirmed with corrections applied, `grep -n -F "Correction 2026-11-12 — to the delegated resolution of OD-01" references/project-standards.md`. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-01" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-01. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-024, T-036, T-113 (and T-037 through T-036).
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

### OD-02  The language of a page, and how a translated quotation is shown

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check (condition (d)) recorded as confirmed with corrections applied, `grep -n -F "Correction 2026-11-12 — to the delegated resolution of OD-02" references/project-standards.md`. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-02" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-02. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-037, T-112.
- **Question.** **Narrowed on 2026-11-12.** The owner said "probably at synthesis or whatever we need to actually translate everything" (`grep -n -F "actually translate everything" references/project-standards.md`): quotations may be translated, and that part is no longer asked. Still open: which language or languages a page is written in (and so which language held text is translated into), and how a translated quotation is shown beside its original on a page.
- **Why it is the owner's.** Audience and the reading surface are doctrine. The ninth statement leaves the target language to the owner and does not relax two standing rules: a model's wording is never presented as a source's term, and English is not the pivot that decides which concepts exist.
- **Options and what follows from each.**
  - (i) English pages; every quotation shown in its own language with a marked translation beside it. *Then:* One target language; the translations of T-112 are into English.
  - (ii) Pages in several languages. *Then:* Every fixed sentence of a page needs a translation and an owner for it; translations of held text are needed into each page language; beyond this plan.
  - (iii) English pages; the translation shown, the original one step away. *Then:* Shorter pages; the reader meets our wording first, so the mark that it is a translation carries more weight.
- **Recommendation (the audit's, not a decision).** (i).
- **Answer in one line.** `OD-02: pages in English, originals with marked translations beside them` · `OD-02: pages in <languages>` · `OD-02: pages in English, translation shown, original on request`
- **Tasks blocked until answered.** T-037 (render); T-112 (the language to translate into). Not blocked: T-049, which builds the home for translations and takes the target language as an argument
- **Where the evidence is.** HS-1 C-02, REQ-104

### OD-03  A concept that has no English name

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check not required. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-03" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-03. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-028.
- **Question.** How is a concept held when it was first met in another language and has no settled English name? (Unaffected by the owner's statement of 2026-11-12 on translation: a translation is an aid attached to held text and never mints or names a concept.)
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

- **Status (2026-11-12): ANSWERED BY THE OWNER** — the owner selected "P1+P2+P3 as recorded; UN out; sub-national counts toward its country". Answer line: `OD-04: scope = P1+P2+P3 as recorded; UN: out; sub-national: counts toward its country` (`grep -n -F "OD-04: scope = P1+P2+P3 as recorded; UN:" references/project-standards.md`; status: `grep -F "OD-04 STATUS:" references/project-standards.md | tail -1`). **Releases:** T-101 (scope filled with the exact codes), and through it T-036, T-037, T-038, T-039; T-024 item 5 (coverage rolls a sub-national code up to its country); T-052 and T-113 read it.
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

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check not required. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-05" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-05. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-052, T-105.
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

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check not required. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-06" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-06. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-106.
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

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check not required. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-07" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-07. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-032.
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

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check not required. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-08" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-08. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-019, T-022, T-037.
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

- **Status (2026-11-12): ANSWERED BY THE OWNER** — the owner selected "On demand, judgments warranted; no request table". Answer line: `OD-09: runs may be carried through on demand without the owner present, each judgment warranted; no request table` (`grep -n -F "OD-09: runs may be carried through on de" references/project-standards.md`; status: `grep -F "OD-09 STATUS:" references/project-standards.md | tail -1`). **ANSWERED, builds nothing:** no request table; blocks and releases no task.
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

- **Status (2026-11-12): ANSWERED BY THE OWNER** — the owner selected "Strength: 'provisional' = thin evidence; a re-read is a reading's own status". Answer line: `OD-10: provisional means strength of evidence; a re-read owed is a reading's own status` (`grep -n -F "OD-10: provisional means strength of evi" references/project-standards.md`; status: `grep -F "OD-10 STATUS:" references/project-standards.md | tail -1`). **Releases:** no task was waiting; T-012 adds no `provisional` value; texts that say `provisional` means a re-read are listed in `DECISION-CLOSURE.md` §3 for correction.
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

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check not required. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-11" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-11. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-051.
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

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check (condition (d)) recorded as confirmed with corrections applied, `grep -n -F "Correction 2026-11-12 — to the delegated resolution of OD-12" references/project-standards.md`. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-12" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-12. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-032, T-037, T-003 (the queue mark).
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

- **Status (2026-11-12): ANSWERED BY THE OWNER** — the owner selected "Superseded by the pair rulings". Answer line: `OD-13: the 2026-03-19 "at least nine languages" rule is superseded by the language–jurisdiction pair rulings` (`grep -n -F "OD-13: the 2026-03-19 "at least nine lan" references/project-standards.md`; status: `grep -F "OD-13 STATUS:" references/project-standards.md | tail -1`). **Releases:** T-001 item 6 (the back-pointer and the marker at `governance/jurisdiction-philosophy.md`).
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

- **Status (2026-11-12): ANSWERED BY THE OWNER** (third set) — the owner said: "MOVE and VES are access needs, agreed. Decompose MOB by device to wheelchair user, prosthetic device user, other mobility aids (or something like that). retain MH and NDV and TALL". Answer line: `OD-14: MOB is decomposed by device into wheelchair user, prosthetic device user and other mobility aids; the exact codes and edges are settled by the design of T-102 and reported to the owner` (`grep -n -F "OD-14: MOB is decomposed by device" references/project-standards.md`). **Releases:** T-102's design (Opus-class), then T-055 and T-102; T-110 after T-102. The edges the design reports, not decides: `AMB` of 2026-08-25, scooter users, ambulatory wheelchair users, the prosthetic child's overlap with `LMB`. OD-31 still holds T-102's heading-only rows. **Fifth set (2026-11-12): the exact codes confirmed.** The owner selected "Confirm all as proposed": `OD-14: codes confirmed as proposed in T-102-design.md: …` (`grep -n -F "OD-14: codes confirmed as proposed in T-102-design.md" references/project-standards.md`): `MOB` the parent, renamed "disabled people with mobility needs"; children `WHEEL` (ambulatory and part-time wheelchair users included), `PROSTH` (lower-limb prosthesis), `WALKAID` (walking aids); `AMB` not minted; scooter users on `MOB` with `device_class = scooter`; `LMB` unchanged; no child for a person who uses no aid. This discharges T-102's report to the owner; the children's ICF crossings are not named by the answer line and wait for an explicit yes (they hold no row). **Revised by the owner, sixth to ninth sets (OI-13 of `OPEN-ITEMS-PLAN.md`, 2026-11-12):** the children are `WHEEL`, `LLD` ("people with lower-limb differences", condition-defined, replacing `PROSTH`) and `WALKAID`; `SCI` is basically `WHEEL` and is retired to it (T-102, with T-054's identity successor); `LMB` becomes `UPL`, upper limb, outside mobility (T-116 rows, T-058 prose) (`grep -n -E "Owner (answer|clarification) 2026-11-12 \((sixth|seventh|eighth|ninth) set\)" references/project-standards.md`).
- **Question.** The split of the mobility group into ambulant people and wheelchair users is ratified and unexecuted. How are the figures and grades written under `MOB` since then carried, and how are part-time wheelchair users named in a gap? **Widened by the owner's thirteenth statement of 2026-11-12** (`grep -n -F "Owner statement 2026-11-12 (thirteenth)" references/project-standards.md`): `MOB` divides by aid (prosthesis, wheelchair, other aids), by wheelchair drive (power, manual) and by impairment level (paraplegia, quadriplegia), so the question is also which divisions are identity codes, which stay descriptors of a participant or a device, how deep, and what a row written under `MOB` is carried as. Facts and options: `DECISION-CLOSURE.md` §5.
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

- **Status (2026-11-12): ANSWERED BY THE OWNER** — the owner said: "We do not need licenses as this is a not-for-profit advocacy project." Recorded with a caveat ([UNVERIFIED] that not-for-profit status removes the requirement; no legal reading made) and an [ASSUMPTION] that attribution is kept. Answer line: `OD-15: proceed; no WHO written agreement sought; the owner's ground is that the project is a not-for-profit advocacy project` (`grep -n -F "OD-15: proceed; no WHO written agreement" references/project-standards.md`; status: `grep -F "OD-15 STATUS:" references/project-standards.md | tail -1`). **Releases:** T-103.
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

- **Status (2026-11-12): DEFERRED BY THE OWNER** (fifth set) — the owner selected "Ratify after T-022 merges, once I have read the corrected contract". Answer line: `OD-17: the owner will ratify the corrected contract after T-002 and T-022 have merged, once they have read it` (`grep -n -F "OD-17: the owner will ratify" references/project-standards.md`; status: `grep -F "OD-17 STATUS:" references/project-standards.md | tail -1`). Reserved by the delegation; no delegated resolution exists or may be written. **Blocks now:** no task; D-27b treats it as settled (a deferral of a decision no task's gate reads). **Ask again** after T-022 merges, with the diff of `governance/pipeline-contract.yaml` in front of the owner.
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

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check not required. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-18" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-18. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-022.
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

- **Status (2026-11-12): ANSWERED BY THE OWNER** — the owner selected "Record now; the engine applies an ordering once you approve it". Answer line: `OD-19: record now; the engine applies an ordering once the owner approves it` (`grep -n -F "OD-19: record now; the engine applies an" references/project-standards.md`; status: `grep -F "OD-19 STATUS:" references/project-standards.md | tail -1`). **Releases:** the recording half, built in T-032; the engine half (T-053) now waits on OD-36.
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

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check not required. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-20" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-20. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-039.
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

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check not required. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-21" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-21. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-021.
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

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check not required. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-22" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-22. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-030, T-003 (the queue mark).
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

- **Status (2026-11-12): ANSWERED BY THE OWNER** — the owner said: "Clause inventory backed by retained text; clause NOT shown. However, we can still read a source more than once--we just want to minimize duplicate reads for efficiency and managing effort. We can flag a source to be read again for later parameters." Answer line: `OD-23: clause inventory backed by retained text; held clause text shown: no; a source may be read again, flagged, for a later parameter` (`grep -n -F "OD-23: clause inventory backed by retain" references/project-standards.md`; status: `grep -F "OD-23 STATUS:" references/project-standards.md | tail -1`). **Releases:** T-031 (the inventory, the derived re-read flag and the duplicate-read rule); T-105 now depends on T-031. It qualifies the 2026-11-12 "read once" objective into an efficiency aim.
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

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check not required. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-24" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-24. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-020, T-030, T-047, T-109.
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

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check not required. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-25" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-25. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-032.
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

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check not required. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-26" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-26. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-038.
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

- **Status (2026-11-12): ANSWERED BY THE OWNER** — the owner selected "Serial is fine". Answer line: `OD-27: research batches land serially` (`grep -n -F "OD-27: research batches land serially" references/project-standards.md`; status: `grep -F "OD-27 STATUS:" references/project-standards.md | tail -1`). **ANSWERED, builds nothing:** the capture's refusal stays; T-001 item 4 already says so in the skill.
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

- **Status (2026-11-12): ANSWERED BY THE OWNER** — the owner selected "Enter them verbatim from the transcript". Answer line: `OD-28: enter the eight sentences of 2026-10-12 verbatim from the committed transcript` (`grep -n -F "OD-28: enter the eight sentences of 2026" references/project-standards.md`; status: `grep -F "OD-28 STATUS:" references/project-standards.md | tail -1`). **Releases:** T-023.
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

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check not required. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-29" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-29. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-050, T-032, T-006 (its note).
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

### OD-30  Who may translate, and must a translation be reviewed before it is used

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** — not the owner's words; reversible by the owner; independent check not required. Ledger: `grep -n -F "Delegated resolution 2026-11-12 — OD-30" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS.md`, section OD-30. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-049, T-112, T-037.
- **Question.** A translation is a model's, a tool's or a person's wording standing beside a source's. May any model translate, or only one at or above a given class? Must a translation be reviewed, and by whom, before synthesis relies on it, and before a reader is shown it?
- **Why it is the owner's.** The capability floor for synthesis is an owner rule, and what a reader is shown as a rendering of a source's words is audience and mission. The ninth statement leaves "who or what translates … and at what class" and "whether a translation is reviewed" open.
- **Options and what follows from each.**
  - (a) Any model may translate; synthesis may read an unreviewed translation as an aid; only a reviewed one is shown to a reader. *Then:* Translation is cheap and early; a page never shows an unchecked rendering.
  - (b) Opus-class or above translates; review before a reader sees it. *Then:* Fewer, slower translations; the same floor as synthesis.
  - (c) A person reviews every translation before any use. *Then:* The strongest guarantee; translation becomes the pace of the pipeline.
- **Recommendation (the audit's, not a decision).** (a). The audit's reading: recording a translation is mechanical (the table marks it, keeps the original and names the translator), while relying on one is a judgment, so the gate belongs where it is relied on, not where it is recorded.
- **Answer in one line.** `OD-30: any model, review before a reader sees it` · `OD-30: Opus-class or above, review before a reader sees it` · `OD-30: a person reviews every translation`
- **Tasks blocked until answered.** T-112 (who runs it), T-037 (which translations a page may show). Not blocked: T-049
- **Where the evidence is.** REQ-104; `grep -n -F "who or what translates" references/project-standards.md`

### OD-31  A clause that names no one but sits under a disability heading: the group it serves, or `ALL` (GAP-076)

- **Status (2026-11-12): ANSWERED BY THE OWNER** (fourth set) — the owner selected "Heading's group; ALL leaves the identity lens". Answer line: `OD-31: a provision that names no one carries the group its heading names (under a mobility heading, the parent MOB with no child; under a general disability heading, no identity, only its ICF and access-need lenses); ALL leaves the identity lens, universal being stated once, by design_scale` (`grep -n -F "OD-31: a provision that names no one" references/project-standards.md`). **Releases:** T-102's rows (its design and owner report still come first); T-056 (`ALL` retired, writers refuse it, the engine's OR-1b branch removed) and T-115 (the figures filed under `ALL` re-tagged by their heading).
- **Question.** Confirm or correct the ledger's reading of the 2026-11-06 answer: a provision written as accessible design (from an accessibility code, or a study of disabled people) carries the group or groups it serves even when its sentence names no one, and `ALL` is kept for provisions that are universal good design.
- **Why it is the owner's.** Population taxonomy; only the owner can confirm what the owner's hedged words meant.
- **Options and what follows from each.**
  - (a) Confirm. *Then:* a clause under a mobility heading keeps the parent `MOB` (it names no device, so T-102 places it on no child); existing `ALL` rows from accessibility codes are re-tagged by links in the lens fill (T-106); `governance/population-taxonomy.md` §1.3's example of `ALL` (code minimum widths) is overtaken.
  - (b) `ALL`. *Then:* such clauses reach only `ALL` determinations (OR-1b); the mobility determinations lose most of their code rows.
- **Recommendation (this pass's, not a decision).** (a): it is the reading the owner's words support, and (b) would empty the group determinations of the codes written for them.
- **Answer in one line.** `OD-31: confirmed — a clause under a disability heading carries the group it serves` · `OD-31: ALL`
- **Tasks blocked until answered.** T-102
- **Where the evidence is.** `select description from gaps where gap_id='GAP-076'`; `DECISION-CLOSURE.md`, OD-14 and OD-31.

### OD-32  The owner's review of judged discussion text

- **Status (2026-11-12): ANSWERED BY THE OWNER** — the owner selected "Independent model review suffices; I can still question any cell". Answer line: `OD-32: independent model review suffices; the owner can question any cell` (`grep -n -F "OD-32: independent model review suffices" references/project-standards.md`; status: `grep -F "OD-32 STATUS:" references/project-standards.md | tail -1`). **ANSWERED, builds nothing:** T-032 and T-037 build as written.
- **Question.** The delegated OD-12 keeps model-written discussion (Opus-class synthesis rows, reviewed by a second Opus-class instance) but removes the owner's review that both model-writing options of OW-1b offered. Does the owner want to review it before a reader sees it?
- **Why it is the owner's.** It is the owner's own review load, and an option the owner was shown and did not give up.
- **Options and what follows from each.**
  - (a) An independent Opus-class review suffices. *Then:* as built; the owner may still question any cell (OD-21).
  - (b) The owner reviews each discussion row. *Then:* the review status gains an owner value; pages show discussion only after the owner's review; the owner's queue grows by one item per discussed cell.
  - (c) The owner reviews a sample. *Then:* a sampling rule is written into the render task.
- **Recommendation (this pass's, not a decision).** (a), with (c) if the owner wants a check without the load (2026-09-09: "I can't handle this load manually").
- **Answer in one line.** `OD-32: an independent Opus-class review suffices` · `OD-32: the owner reviews each` · `OD-32: the owner reviews a sample of <n> per build`
- **Tasks blocked until answered.** None; informs T-032 and T-037
- **Where the evidence is.** `grep -n -F "without the owner's review" references/project-standards.md`

### OD-33  Where the render table lives

- **Status (2026-11-12): RESOLVED UNDER DELEGATION** (the twelfth-instruction pass: a build product outside the database; the content of the reviewed OD-12 correction 4) — not the owner's words; reversible by the owner; check not required. Ledger: `grep -n -F "OD-33: the render table" references/project-standards.md`. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-037.
- **Question.** OW-1's recorded [ASSUMPTION] put the render table in the database; the corrected OD-12 makes it a build product outside it. Is that acceptable?
- **Why it was asked.** It departs from a reading recorded beside the owner's words. It is not reserved: that reading is an assumption, not a ruling, and the question is code architecture.
- **Options and what follows from each.**
  - (a) A build product, generated from the database at each build. *Then:* no migration per build; a staleness check on input hashes.
  - (b) In the database. *Then:* a write path for rendered prose must be designed first, and every build adds a migration.
- **Answer in one line.** `OD-33: a build product` · `OD-33: in the database, through <write path>`
- **Tasks blocked until answered.** T-037 (its design), now OPEN
- **Where the evidence is.** `DELEGATED-RESOLUTIONS-REVIEW.md` (where the table lives); `DECISION-CLOSURE.md`

### OD-34  A study whose finding does not depend on its country, under the bucket order

- **Status (2026-11-12): ANSWERED BY THE OWNER** — the owner selected "Instruments only: a T1–T3 study is admitted on its merits". Answer line: `OD-34: the 2026-09-28 bucket order covers codes and standards, not laboratory or clinical studies whose finding does not depend on the country; such a T1–T3 study is admitted on its merits` (`grep -n -F "OD-34: the 2026-09-28 bucket order cover" references/project-standards.md`; status: `grep -F "OD-34 STATUS:" references/project-standards.md | tail -1`). **Releases:** no task was waiting; T-052's paragraph stages out-of-scope instruments only.
- **Question.** Is a laboratory or clinical study done in a jurisdiction outside the buckets "evidence from a jurisdiction" under the standing order of 2026-09-28, or may a T1 to T3 study be admitted on its merits before the buckets are exhausted?
- **Why it is the owner's.** It narrows or confirms a standing owner order on scope.
- **Options and what follows from each.**
  - (a) The order covers studies too. *Then:* such studies wait as leads until the slug's buckets are exhausted.
  - (b) The order covers instruments (codes and standards) only. *Then:* a T1 to T3 study is admitted on its merits; codes stay bucket-bound.
- **Recommendation (this pass's, not a decision).** (b): a study's finding about bodies, devices or perception does not depend on the country that hosted it, and criterion 3 weighs against waiting, since non-bucket research is where several lenses are thinnest; but the order's words ("do not research from countries other than…") read as (a).
- **Answer in one line.** `OD-34: the bucket order covers studies` · `OD-34: the bucket order covers instruments only`
- **Tasks blocked until answered.** None; changes what the T-052 convention later admits
- **Where the evidence is.** `grep -n -F "Standing order: do not research" references/project-standards.md`

### OD-35  The status-and-check convention for the ledger

- **Status (2026-11-12): ANSWERED BY THE OWNER** — the owner selected "Keep it". Answer line: `OD-35: the status-and-check convention for decisions is kept` (`grep -n -F "OD-35: the status-and-check convention f" references/project-standards.md`; status: `grep -F "OD-35 STATUS:" references/project-standards.md | tail -1`). **ANSWERED, builds nothing.**
- **Question.** The fold added a ledger convention (status and check lines, latest wins, one gate) so that a delegated resolution opens a task only when its check is recorded; the twelfth-instruction pass added the value `DEFERRED BY THE OWNER`. Does the owner accept it, or prefer another mark?
- **Why it is the owner's.** It decides how the owner's answers are read by every task.
- **Options and what follows from each.**
  - (a) Accept. *Then:* nothing changes.
  - (b) Another mark. *Then:* every task file's gate block and the generator change together.
- **Recommendation (this pass's, not a decision).** (a).
- **Answer in one line.** `OD-35: ledger gate accepted` · `OD-35: <other mark>`
- **Tasks blocked until answered.** None
- **Where the evidence is.** `grep -n -F "Convention 2026-11-12" references/project-standards.md`

### OD-36  The harm ordering in mechanical form, and where its warrants come from

- **Status (2026-11-12): ANSWERED BY THE OWNER** (fourth set) — the owner selected "Approve that ordering, held once as data; each class warranted by a held source's own finding". Answer line: `OD-36: the harm ordering injury > loss of independent use > pain > effort > discomfort is approved, held once as data, each class warranted by a held source's own finding and never by a model's estimate; a tie goes to a named judge` (`grep -n -F "OD-36: the harm ordering" references/project-standards.md`). **Releases:** T-053 (the `harm_classes` table, a warrant pointer per side, refusal to apply where a class is unwarranted, ties left to a named judge).
- **Question.** Approve, in mechanical form, the ordering of harm classes the engine uses to set a default where groups conflict, and say where each side's class is warranted from.
- **Why it is the owner's.** It weighs one group's harm against another's.
- **Options and what follows from each.**
  - (a) Approve an ordinal ordering held once as data (proposed: injury > loss of independent use > pain > effort > discomfort), each side's class warranted by a held source's own finding (a study's harm outcome, or a Co-1 source's account), never by a model's estimate; a tie is recorded for a named judge. *Then:* T-053 builds it; on the ramp case (`DECISION-CLOSURE.md` §2, OD-19) the gentler gradient is the default with rest landings as the supplementary provision.
  - (b) Approve the ordering but require a person's confirmation on each application. *Then:* the engine proposes, a named judge accepts; slower, fully attributed.
  - (c) Not yet. *Then:* conflicts stay recorded only (T-032); T-053 stays stopped.
- **Recommendation (this pass's, not a decision).** (a), with the class vocabulary changed by data only on the owner's word.
- **Answer in one line.** `OD-36: approve <ordering>; warrants from held sources' findings` · `OD-36: approve <ordering>, each application confirmed by a named judge` · `OD-36: not yet`
- **Tasks blocked until answered.** T-053
- **Where the evidence is.** `grep -n -F "RULE: Harm asymmetry governs" references/project-standards.md`; `DECISION-CLOSURE.md` §2 (OD-19) and §4

### OD-37  The identity-lens rule for the codes the population-umbrellas memo flagged

- **Status (2026-11-12): ANSWERED BY THE OWNER** (third set; created and answered in one reply to `POPULATION-UMBRELLAS-MEMO.md`). The owner said: "MOVE and VES are access needs, agreed. Decompose MOB by device to wheelchair user, prosthetic device user, other mobility aids (or something like that). retain MH and NDV and TALL". Answer line: `OD-37: identity-lens rule for the memo's flagged codes: MOVE and VES are access needs; MH, NDV and TALL are retained; MOB is decomposed by device; the memo's wholesale rule is not adopted; ALL, DEAF, LMB and COM stand unchanged unless the owner says otherwise` (`grep -n -F "OD-37: identity-lens rule" references/project-standards.md`). **Releases:** T-054 (a code retires to the need that carries it) and T-114 (`MOVE` to `A-PRECISION`, `VES` to `A-STABLE`). `MH`, `NDV`, `TALL`: retained, **nothing to build**; the memo's findings on them (`MH` named in clinical words rather than "psychosocial disability"; `NDV` a coalition spanning `AUT`, `ADHD`, `ID`, `MH` though kept as a flat peer; `TALL` an anthropometric range `A-SIZE` covers) are open edges for the owner, not tasks. `ALL`, `DEAF`, `LMB`, `COM` unchanged.
- **Question (as put).** Which of the memo's flagged identity codes stay identities, which become needs, and is its wholesale rule adopted?
- **Why it is the owner's.** Population taxonomy.
- **Answer in one line.** Given; see the status line.
- **Tasks blocked until answered.** T-054, T-114 (now open)
- **Where the evidence is.** `POPULATION-UMBRELLAS-MEMO.md` §6; `grep -n -F "Owner answers 2026-11-12 (third set)" references/project-standards.md`

### OD-38  Which English name is shown for a concept that several English-language instruments name differently

- **Status (2026-11-12): ANSWERED BY THE OWNER** (fifth set; entered and answered together) — the owner selected "First recorded, until a named judge picks; the pick is recorded with its reason". Answer line: `OD-38: the first English name recorded is shown until a named judge picks one with rename-term --from-form; the pick is recorded with its reason` (`grep -n -F "OD-38: the first English name recorded is shown" references/project-standards.md`; status: `grep -F "OD-38 STATUS:" references/project-standards.md | tail -1`). **Releases:** T-028's display rule 2 as designed (`tasks/T-028-design.md` section 7), with `rename-term --from-form` taking a named judge and a reason recorded in typed columns (T-028 item 2).
- **Question (as put).** `T-028-design.md` §7 rule 2 shows the first recorded English instrument form when several English-language instruments name one concept differently: arbitrary but deterministic. Keep it, or show our label, or require a pick?
- **Why it is the owner's.** It decides which source's words the reader meets first; the design marked it as where the owner may disagree.
- **Answer in one line.** Given; see the status line.
- **Tasks blocked until answered.** T-028 (now open)
- **Where the evidence is.** `tasks/T-028-design.md` sections 7 and 15; `grep -n -F "Owner answers 2026-11-12 (fifth set)" references/project-standards.md`

### OD-39  Whether the link-table ruling of 2026-11-06 supersedes the 2026-08-28 clause "Never a `population_*` link table"

- **Status (2026-11-12): ANSWERED BY THE OWNER** (fifth set; entered and answered together) — the owner selected "Yes, the 2026-11-06 ruling supersedes that clause". Answer line: `OD-39: the 2026-11-06 link-table ruling supersedes the 2026-08-28 clause "Never a population_* link table"; T-018 appends the SUPERSEDES/BY pair and builds extraction_lens_links` (`grep -n -F "OD-39: the 2026-11-06 link-table ruling supersedes" references/project-standards.md`; status: `grep -F "OD-39 STATUS:" references/project-standards.md | tail -1`). **Releases:** T-018 as designed. **How the supersession is recorded:** the answer line's "appends the SUPERSEDES/BY pair" is the recorder's wording, not the option the owner selected; a machine pair cannot pass `supersession_backpointer_audit` for a target inside the ledger (tested on a scratch copy 2026-11-12: PASS became FAIL), so T-018 records it in a prose ledger entry on the 2026-09-01 precedent (`tasks/T-018-design.md` section 5, step 6, corrected).
- **Question (as put).** OR-1c (2026-11-06) chose a link table "unless that is more prone to errors"; the 2026-08-28 ACTION says "Never a `population_*` link table". Does the later ruling supersede the earlier clause for a figure's lens codes?
- **Why it is the owner's.** Only the owner retires an owner rule where the later ruling does not name it (CLAUDE.md rule 0).
- **Answer in one line.** Given; see the status line.
- **Tasks blocked until answered.** T-018 (now open)
- **Where the evidence is.** `tasks/T-018-design.md` sections 0 and 5; `grep -n -F "ACTION: Four lens columns, one CHECK, real FKs." references/project-standards.md`

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
| D-09 | the mobility family is decomposed by device as the owner answered OD-14 (third set), and `MOVE` and `VES` are needs (OD-37) | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select identity_code, parent_code, status from base_taxonomy_identity where category='mobility' or parent_code='MOB' or identity_code in ('MOVE','VES') order by 1\").fetchall())"`; and T-102's after-test (3) | `MOB`, `SCI`, `LMB` with no parent; `MOVE`, `VES` active | `WHEEL`, `LLD`, `WALKAID` (the fifth-set codes as revised in the sixth to ninth sets) with `parent_code` `MOB`; `SCI` deprecated with `superseded_by_identity` `WHEEL` (T-102) and `LMB` deprecated with successor `UPL`, `UPL` active with no parent (T-116); `MOB` active as their parent and named "disabled people with mobility needs"; T-102's after-test (3) prints 0; `MOVE` and `VES` deprecated with their needs (T-114) |
| D-10 | the fourth lens is usable | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*) from base_taxonomy_medical\").fetchall())"` | `[(0,)]` | above 0 |
| D-11 | jurisdictions: scope is data | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*), sum(scope_status is not null) from lang_jur_map\").fetchall())"` | the second number is 0 | the two numbers are equal, and every pair is `in-scope` exactly when its jurisdiction is in the OD-04 set (T-101's after-test prints `0 0`) |
| D-12 | languages: one spelling per language | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"SELECT (SELECT COUNT(DISTINCT language) FROM v_coverage_language), (SELECT COUNT(DISTINCT UPPER(language)) FROM search_executions WHERE deferred_reason IS NULL)\").fetchall())"` | the two numbers differ | equal |
| D-13 | flexible: the base changes by data alone | `f=$(grep -l 'AT-104' scripts/tests/*.py); echo "file=$f"; [ -n "$f" ] && python3 $f; echo rc=$?` | `file=` (none) and `rc=1` | a file is named and `rc=0` |
| D-14 | units: one home, and a unit can be added without editing the engine | `git grep -n -E "^\s*NOTATION_FAMILIES\s*=" -- scripts schemas` | one line, in the engine (`scripts/assess/assess_cell.py`) | no line in the engine; and the after-test of `tasks/T-030-units-as-data.md` (parameter 12 has a value in both notations) |
| D-15 | languages and scripts: the guards hold outside Latin script | the evidence command in section 3 of `tasks/T-009-script-aware-guards.md` | `True True`, then empty token sets | `False False`, then non-empty token sets and `True` |
| D-16 | adjudicate: a wrong number does not verify, and a number in words is filed as a numeral | the first command (the probe) in section 3 of `tasks/T-008-claimed-number-check.md`; python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select count(*) from source_value_extractions where value_as_written is not null\").fetchall())" | six lines `ACCEPTED`; the query fails (no column) | six lines `REFUSED`; a count above 0 once T-111 has landed |
| D-17 | read once, as an efficiency aim (OD-23: a clause inventory backed by retained text; a flagged re-read where neither reaches) | `python3 scripts/audit/scan_debt.py 2>&1 \| grep -E 'EXAMINED\|DEBT'` | a `DEBT:` line | every owed pair is either covered, matched by the clause inventory, or shown by T-031's derived re-read flag; no pair owed for want of any route |
| D-18 | synthesize: relations can be found and kept | `python3 scripts/db.py --help \| tr "," "\n" \| grep -c -E "synthesis-candidates\|relation-candidates"` | 0 | 1; and the relation rows of T-032 exist per OD-25 |
| D-19 | specify: a live determination the blocking gates examine | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select sum(retired_at is null) from specifications\").fetchall())"; cp data/guidebook.db "$SCRATCH/i.db" && GUIDEBOOK_DB_PATH="$SCRATCH/i.db" python3 scripts/tests/test_db_integrity.py > /dev/null; echo rc=$?` | no live row (the test passes on history only) | above 0, and `rc=0` |
| D-20 | render: a page exists and each claim traces to a row | the after-tests of `tasks/T-037-render.md` | nothing to open | green |
| D-21 | clean: skills describe what exists | `python3 scripts/audit/skill_vocabulary_audit.py > "$SCRATCH/sv.txt"; echo rc=$?; grep -E "EXAMINED\|FAIL\|PASS" "$SCRATCH/sv.txt" \| tail -2` | `rc=1` and a FAIL line | `rc=0` with `EXAMINED:` above 0 |
| D-22 | centralized: no helper with two homes | the evidence command in section 3 of `tasks/T-041-one-home-for-helpers.md` | several names | `{}` |
| D-23 | no typed counts in the registry | `grep -c -E '[0-9]+ today' governance/check-registry.yaml` | not 0 | 0 |
| D-24 | the database is what its migrations make | `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db" && python3 scripts/audit/migration_reproducibility.py --deep; echo rc=$?` | `rc=0` | `rc=0` |
| D-25 | the gates are sound | `python3 scripts/run_checks.py --selftest; echo rc=$?` | `rc=0` | `rc=0` |
| D-28 | translate from any stage, by data alone | `f=$(grep -l 'AT-107' scripts/tests/*.py); echo "file=$f"; [ -n "$f" ] && python3 $f > "$SCRATCH/at107.txt" 2>&1; echo rc=$?; grep -E 'EXAMINED\|FAILED' "$SCRATCH/at107.txt"` | `file=` (none) and `rc=1` | a file is named, `rc=0`, `EXAMINED:` above 0 (the same file holds AT-108 and AT-109) |
| D-29 | the default stage for translation is a rule in one place | `grep -n -A2 "^translation:" governance/pipeline-contract.yaml; git grep -n -E "default_stage" -- scripts schemas \| wc -l` | no such key | the key with its stage; the count shows the readers, and AT-108 (in the file of D-28) shows that changing the key changes the behaviour |
| D-30 | rules are declared once | the first command of section 7 of this file | `NOTATION_FAMILIES`, `RULE_VERSION`, `JurisdictionCode` once each; the others not yet | every line 0 or 1; `JurisdictionCode` 0, or generated from the table |
| D-26 | every task is accounted for | `for f in workplan/2026-11-12-bidirectional-pipeline/tasks/T-[0-9]*-*.md; do echo "$f"; done` | the list | each is merged (its after-test is green on `main`) or declined in the owner's words in the ledger |
| D-27 | every owner decision a task waits on is settled (owner's twelfth instruction: the plan is not complete while one stands open) | `gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md \| tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md \| tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*\|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }; for n in $(grep -h -o -E 'for n in [^;]*;\|"OD-[0-9]+ STATUS:"' workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md \| grep -o -E 'OD-[0-9]+' \| sort -u); do gate $n; done \| grep CLOSED` | the blocking decisions, one CLOSED line each | no line |
| D-27b | every other register decision is answered, resolved under delegation with its gate OPEN, or deferred by the owner | `for n in $(grep -o -E '^### OD-[0-9]+' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md \| cut -c5-); do gate $n; done \| grep CLOSED \| grep -v -F 'DEFERRED BY THE OWNER'` (after defining `gate` as in D-27) | the standing decisions and the blocking ones | no line |
| D-36 | every register entry carries a status line, and no task names a decision the register lacks | `echo $(grep -c '^- \*\*Status (2026-11-12)' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md) $(grep -c '^### OD-' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md); python3 -I scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py \| grep -o "unregistered .*"` | two equal numbers; `unregistered []` | the same |
| D-31 | retire in place: no verb deletes an admission edge or a connection (T-050) | `grep -c -E "DELETE FROM (search_admissions\|connections\|connection_targets)" scripts/db.py` | not 0 | 0, and T-050's after-test green |
| D-32 | the gap register is cross-stage, and no path was lost (T-051) | `python3 -c "import yaml;print(yaml.safe_load(open('governance/stage-map.yaml'))['tables']['gaps'])"` | `synthesis` | `cross-stage`, and D-01's count no higher than before T-051 |
| D-33 | an out-of-scope mined source is staged, not admitted (T-052) | `grep -c -E 'OUT-OF-SCOPE\|outside the scope in force' skills/citation-miner_SKILL.md skills/gap-driven-mining_SKILL.md` | 0 for each | at least 1 for each |
| D-34 | sub-national instruments are filed under their own codes (T-113) | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select ref_id, jurisdiction from evidence_sources where ref_id in ('REF-00992','REF-00995','REF-01013','REF-01029')\").fetchall())"` | the country codes | each a sub-national code whose parent is the country |
| D-35 | conflict between groups: recorded (OD-19, T-032) and weighed by the approved ordering (OD-36, T-053) | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([r[1] for r in c.execute('pragma table_info(conflicts)')], c.execute(\"select count(*) from sqlite_master where name='harm_classes'\").fetchall())"`; then T-053's after-test | no judge, warrant or class columns; no `harm_classes` | judge and warrant columns (T-032); the five classes in order and T-053's after-tests (a) to (f) green |
| D-37 | `ALL` has left the identity lens; universal is stated only by `design_scale` (OD-31) | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select status from base_taxonomy_identity where identity_code='ALL'\").fetchall(), c.execute(\"select count(*) from source_value_extractions where identity_code='ALL'\").fetchall())"`; `git grep -n -E "['\"]ALL['\"]" -- scripts/assess` | `[('active',)]` and a non-zero count; an engine branch | `[('deprecated',)]`, `[(0,)]`, no engine branch (T-056, T-115) |

A line whose command a task changes (a renamed verb, a moved test) is updated in the same pull request; a prose caller is a caller.

## 11. What this plan does not settle

- **Added by the delegated pass, and what the twelfth-instruction pass did with it** (details in `FOLD-LOG.md` and `DECISION-CLOSURE.md` §3): the batch generator now reads both decision bullets and the ledger gate, so a task is shown READY only when every decision it names is OPEN for it (fixed). The forms home of T-026 and T-028: T-026 now waits for T-028's one-page design, which names the one table (fixed in the task files). T-113's verbs were read: `amend-source` takes `jurisdiction`, `amend-extraction` does not; T-024 now adds it (fixed). Still open: T-113 declares sub-national codes, a vocabulary act the OD-01 correction allows only as provenance; whether that is a scope act is OD-04's to say. [ANSWERED by OD-04, 2026-11-12: a sub-national instrument counts toward its country and owes no coverage alone, so declaring its code is provenance, not scope.]
- Why `scripts/audit/doctrine_recheck.py` exits 1 when run bare while its battery is green (the registered invocation differs; inferred, not shown).
- The causes of three advisory failures standing on `main`: `test_scan_contract`, `validate_schema_cross_check`, `research_dod`. T-040 reads and reports them.
- Whether `add-source` refuses a NULL standing when a URL is given (not probed); T-007 closes it either way.
- Whether the order T-016, T-017, T-019 of the prior workplan is forced by the code or only by that plan; it is kept because it is the ruled plan.
- Which retained artefacts are a source's full text (OD-23's route backs the inventory with retained text, so T-031's derived re-read flag depends on it).
- Behaviour at a hundred times the present row counts.
- Not exercised by any stress round: candidate staging to admission, a citation-mining row, merging or declining a parameter that holds figures, a non-English source end to end.
- `scripts/run_checks.py --all` was never run in one call, by instruction; the ten batteries were run one at a time on a copy.
- All but three of the task files have not been executed by anyone (section 12). The three that were each had defects that only execution showed.
- T-008 as redesigned on the owner's ruling (the `value_as_written` column, its writers, the refusal of a digitless figure) and T-049 (translations) are designs of this pass and unpiloted.
- Whether `derive-extraction` should take the as-written wording (T-008 item 6 leaves it to what the verb does today).
- `sessions/` was searched with `git grep`, not read end to end; an owner ruling that only lives there and matches none of the searches would be missing from this plan.

## 12. Pilot results (2026-11-12), and what has and has not been tested

**What was piloted.** Three Sonnet-class executors each took one Wave 0 task in a scratch clone, following only the task file: T-006, T-008 and T-010. Reports and patches: `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/T-006-report.md`, `T-008-report.md`, `T-010-report.md` and the `.patch` beside each. Nothing was pushed; the canonical database did not move.

**Result.** In all three the change worked: red before, green after. In all three the task file had defects that only execution showed. None of the defects was an executor's error. One was a design fault in the plan: T-008 as first written made a figure that a source writes in words impossible to file.

**What changed in the plan because of it.**

| What the pilots showed | Class | What was done | Where |
|---|---|---|---|
| The base branch: in a clone `origin/main` lacks the workplan, so branching from it, the code-size line and the default gate all measured the whole workplan | mechanical, every file | every file sets `$BASE` by test and uses it; this index says to merge the workplan first | section 2 of every task file; section 2 here |
| The gate was listed before the commit and was run twice (`preflight.sh`, then `run_checks.py` on the same diff) | mechanical, every file | one gate, `preflight.sh --base "$BASE" --explain`, once, before the commit; it reads the working tree, so no commit is needed first | section 6 step 4, section 7 |
| `/session-open` and `git switch -c` do not fit a pilot clone | mechanical, every file | each file says what applies to a real execution and what to a pilot | section 2 |
| The sweep printed up to two hundred lines, most of them plans, generated state-graph files and the ledger, so "stop on a caller this file does not mention" could not be met | mechanical, every file | the sweep has a stated exclusion list with reasons, a definition of caller against mention, the hits as of writing, and the callers already known; the stop condition is "a caller you cannot repair in scope" | section 5, section 9 |
| "Read each check's `EXAMINED:` line" could not be followed: a passing check prints none in the gate's output | mechanical, every file | each file names the checks that read what it touches and gives one loop that runs each as the registry does, before and after, and prints its subject | section 6 steps 1 and 3 |
| The test files are registered as advisory, so a test the change turned red (T-010, case V03 of `test_scan_contract`) would not have stopped the gate | mechanical, every file | the before-and-after comparison of failing cases is the stop, at any level | section 6 step 3, section 9 |
| Ids typed into tests and evidence; case ids that collided with existing ones | mechanical, every file | case ids take the task number as prefix, checked free first; probes are derived by query; the evidence commands of T-010 and T-020 derive their term | section 6; T-010, T-020 |
| A write verb in an evidence command, safe only because of the inline database path | mechanical | a reminder is printed beside every such command | section 3 |
| "Add nothing this file does not name" against "fix what the sweep finds" | mechanical, every file | a caller the sweep finds is in scope and is listed in the pull request | sections 5, 8, 9 |
| A "still works" probe that picked a declined term and failed for the wrong reason | mechanical, every file | a positive probe must be one no other refusal stops | section 6 |
| T-006: the function to copy from, the test file, how to build the positive case, a worked `add-connection`, the check to read | mechanical | written into the file | `tasks/T-006-delete-connection-refusal.md` |
| T-010: two real callers missed (a test fixture that turned red; a stale comment) | mechanical | named as callers in the file | `tasks/T-010-add-parameter-domain-refusal.md` section 5 |
| T-010: the refusal could not say what to do with a quantity filed under the wrong domain, because no verb corrects a domain | judgment | `domain` becomes amendable through `amend-term`, with a guard; the refusal names both next actions. Reason: a refusal with no route is a dead end, and one tuple member closes it | T-010 item 3 |
| T-010: the refused domains are a constant, `dbcore.NON_QUANTITY_DOMAINS` | judgment | kept, as a rule declared once with its warrant in its comment (the owner's tenth statement allows that), tested for staleness, and kept by T-020 beside the quantity kind (corrected 2026-11-13: the folded T-020 keeps it, because the domain is a fact of the term and the kind a fact of the parameter, and without it a lens or legal term becomes promotable). Reason: which domains name a lens or a body of law cannot be computed; it is judged, so it is named and held in one place | T-010 item 1; T-020 item 2 |
| T-008: a figure written in words became unfilable | owner ruling | the owner ruled: enter the numeral and unit; the wording may be kept in its own column. T-008 adds `value_as_written`; the prior workplan's numeral gloss is superseded and removed from T-016 | T-008; T-016; T-111 |
| T-008: two stored rows the new check would refuse | judgment | history stands: the check applies when a row is written. Extraction 30 holds a numeral and gets its wording filled in. Extraction 80 holds words as its value, so it is not amended: a second row carries the numeral. Both in a research task | `tasks/T-111-as-written-wording-for-stored-rows.md` |
| T-008: which claim types state a quantity was typed inline | judgment | one declared rule, `dbcore.QUANTITY_CLAIM_TYPES`, tested against the column's CHECK and read by T-016 too. Reason: the CHECK cannot say which of its values are quantities | T-008 item 5 |
| T-008: number forms (a standard's number read as a ratio, a table cell read as one number, "1 in 12", an ambiguous `1,200`) | judgment | symbol ratios are typed and their operands also count on the quote side; a ratio in words is matched by its operands; an ambiguous token is refused in a claimed value and, in a quote, needs the wording recorded. No language's words are listed in code. Reason: "1:20 where the run exceeds 12 m" must not verify `1:12`, and no rule may depend on a list of languages | T-008 items 1, 2, 4 |
| T-008: the evidence command reimplemented the old logic and could not show the result | mechanical | it now runs the real writer function with the quote lookup stubbed, so the same command shows before and after | T-008 section 3 |
| T-008: `amend-extraction` listed as a reader; `_verbatim_norm` left undecided; prose that restates the old check in immutable files | mechanical | readers corrected; delete; the pointer goes on the gap row through `amend-gap` in T-111, never into a committed migration or a session file | T-008 items 6, 7 and section 5 |

**Which tasks were piloted.** By command: piloted, `grep -L "^\*\*Pilot status.\*\* Not piloted" workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md`; not piloted, the same with `-l`. Today the piloted ones are T-006 and T-010 (each as corrected, with one unpiloted addition in T-010) and T-008 in part (its number comparison; the column and its writers follow the owner's ruling and were written after the pilot). Every other task is unpiloted.

**What that means for the executor.** The mechanical defects were of the generator, so they were fixed in every file at once; the fixes themselves have not been piloted. An unpiloted file's evidence command has been run and prints what the file says, and nothing more is known about it. The riskiest unpiloted files are the ones with a schema migration or a new design: [T-008](tasks/T-008-claimed-number-check.md), [T-049](tasks/T-049-translation-home.md), [T-013](tasks/T-013-typed-gaps.md), [T-012](tasks/T-012-follow-up-reasons.md), [T-015](tasks/T-015-language-fold.md), [T-024](tasks/T-024-jurisdiction-registry.md), [T-026](tasks/T-026-alias-attestation.md). The safest are the ones that change text or add a test: [T-002](tasks/T-002-contract-entry-text.md), [T-003](tasks/T-003-owner-queue-answered-marks.md), [T-004](tasks/T-004-spec-checks-report-live-rows.md), [T-005](tasks/T-005-retired-row-view-fixture.md).

## 13. Delegated resolutions, the independent check, and the fold (2026-11-12)

**What happened.** The owner delegated twenty register decisions to an Opus-class model (`grep -n -F "I guess opus can do it" references/project-standards.md`). The model resolved nineteen and referred OD-10 back (`DELEGATED-RESOLUTIONS.md`). A second, independent Opus-class instance checked the four the delegation names (`DELEGATED-RESOLUTIONS-REVIEW.md`): OD-01, OD-02 and OD-12 confirmed with corrections; OD-14 referred back. The corrections are appended to the ledger and marked in the resolutions file; OD-14 is withdrawn. How many delegated resolutions stand: `grep -c "STATUS: RESOLVED UNDER DELEGATION" references/project-standards.md` counts the lines, and the gate loop below gives the state of each (a later line for the same id supersedes an earlier one).

**The gate every task now uses** (`grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`). The ledger carries, per decision, a status line `OD-NN STATUS:` and, for a delegated resolution, a check line `OD-NN CHECK:`; the last of each wins. A decision is OPEN for a task only when its status is `ANSWERED BY THE OWNER`, or `RESOLVED UNDER DELEGATION` with its check `not required`, `confirmed` or `confirmed with corrections applied`. A task that needs the owner's words opens only on the first. Run for every decision:

```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in $(grep -o -E '^### OD-[0-9]+' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md | cut -c5-); do gate $n; done
```

**What the fold changed.** Every task that read a delegated decision now names it in a "Delegated resolutions this task rests on" bullet with the gate, says what the resolution requires in its section 4, and stops (section 9) if the gate prints CLOSED. Five tasks are new: T-050 (OD-29), T-051 (OD-11), T-052 (OD-05), T-053 (the engine part of T-032, held by the reserved OD-19), T-113 (OD-01, research). The build plan, decision by decision, is the last section of `DELEGATED-RESOLUTIONS.md`; the file-by-file record is `FOLD-LOG.md`. `REMEDIATION-PLAN.md` was regenerated from the task files.

**The twelfth-instruction pass (2026-11-12).** The owner asked that the plan's issues be addressed and the decisions still holding up work be confirmed and, where appropriate, resolved before the plan is called complete (`grep -n -F "Owner instruction 2026-11-12 (twelfth)" references/project-standards.md`). That pass is `DECISION-CLOSURE.md`: it entered the fold's five questions as OD-31 to OD-35, resolved OD-33 under the twelfth instruction, prepared every other open decision as a phone-ready prompt, made the generator read the ledger gate, rewrote D-27 and added D-27b and D-36. **The plan is not complete while D-27 prints a line.**

**The owner's answers (2026-11-12, the last fold pass).** The owner answered twelve decisions (`grep -n -F "Owner answers 2026-11-12" references/project-standards.md`): OD-04, OD-23, OD-15, OD-19, OD-28, OD-10, OD-34, OD-13, OD-32, OD-09, OD-27, OD-35. OD-19's answer created OD-36 (the harm ordering's approval), which holds T-053. Still open after the first two sets: OD-14 and OD-31, OD-36, and OD-17 (asked after T-022). **Third set (2026-11-12):** the owner answered OD-14 (decompose `MOB` by device) and, in the same reply to the population-umbrellas memo, OD-37 (`MOVE`, `VES` are needs; `MH`, `NDV`, `TALL` retained; the memo's wholesale rule not adopted). T-102 was redesigned (design first, reported to the owner) and T-054, T-055 (tooling) and T-114 (research) were added. Still open after the third set: OD-31, OD-36, OD-17. **Fourth set (2026-11-12):** the owner answered OD-31 (a provision that names no one carries its heading's group; `ALL` leaves the identity lens) and OD-36 (the harm ordering approved as data with held-source warrants; ties to a named judge). T-102 and T-053 were rewritten to the answers, and T-056 (tooling) and T-115 (research) were added for `ALL`. **Only OD-17 is open, and it blocks no task (it is asked after T-022 merges): by the owner's twelfth instruction no decision that holds up a task stands open.** D-27 prints nothing; D-27b prints OD-17 alone. The fold of the answers into the task files is recorded in `FOLD-LOG.md` §4 and `DECISION-CLOSURE.md` §3; read the open set from D-27, not from this paragraph.

**Fifth set (2026-11-12).** The owner confirmed T-102's codes and edges as proposed (OD-14: `WHEEL`, `PROSTH`, `WALKAID` under `MOB`; `AMB` not minted), deferred OD-17 to after T-002 and T-022 merge (status `DEFERRED BY THE OWNER`), and answered two new decisions entered with their answers: OD-38 (the first English name recorded is shown until a named judge picks with `rename-term --from-form`, the pick recorded with its reason) and OD-39 (the 2026-11-06 link-table ruling supersedes the 2026-08-28 clause). Folded: T-102's report to the owner is discharged (item 2; after-test (2)); T-110 reads the confirmation; T-028 gates on OD-38 and records the pick's judge and reason in typed columns; T-018 gates on OD-39 and records the supersession in prose, because the audit cannot anchor a machine pair on a target inside the ledger. The children's ICF crossings are not named by the answer line and are left for the owner's explicit yes. What remains open in the plan as a whole, by class, with a resolution plan: `OPEN-ITEMS-PLAN.md`.

**OI-13 (2026-11-12, sixth to ninth sets).** The owner answered "SCI and LMB go under MOB" and then clarified three times: `SCI` is basically `WHEEL`; `LMB` becomes `UPL`, upper limb, and "doesnt concern mobility"; the lower-limb child is `LLD`, "people with lower-limb differences", replacing `PROSTH`. Folded: the family is `MOB` with `WHEEL`, `LLD`, `WALKAID`; T-054 gains the identity successor (one exactly-one CHECK over the successor columns) and in-place retirement of crossing rows, so `SCI` and `LMB` can be retired once their rows are carried; T-102 retires `SCI` to `WHEEL` (design §6a) and mints `LLD`; two new tasks hold `UPL`: T-116 (research: mint `UPL`, place `LMB`'s crossings, retire `LMB`) and T-058 (tooling: the DR-2026-07-23 crosswalk back-pointer, the retired-vocabulary record, prose callers); T-025's amend takes description and category; T-055 counts a figure once at a parent. The fold is `FOLD-LOG.md` §9; the open edges are in `OPEN-ITEMS-PLAN.md`.

**The prior workplan mapped (OI-09, 2026-11-13).** Every id of `workplan/2026-10-23-pipeline-resolution-workplan.md` (`grep -n -E '^\*\*(T-[0-9]|H-0)|^\| D-[0-9]|^\| S-1' <that file>`) against this plan. "Read" means the task file's own text or Traces cell was read; "title only" means it was matched on its title and not read to the line, so the match is a hypothesis. The owner's ruling that bears on each is the `OR-` line in the ledger (`grep -n -E '^OR-[0-9]+b?:' references/project-standards.md`).

| Prior id | What it was | Where it is now | Basis |
|---|---|---|---|
| T-1a | notation arithmetic to one home; the writer refuses unreadable figures | T-016 | read |
| T-1b step 8 | `amend-extraction` widened to unit, value and NULL setting (OR-3: "Yes, reformat in place") | **no task** | ruled yes; unmapped |
| T-1b step 9 | the length family, `RULE_VERSION` bump (OR-10: "Yes, convert and show both") | **no task** | ruled yes; unmapped |
| T-1b step 10 | the `verified` gate: a full-scope scan (OR-11a: "Yes, require a full-scope scan") | **no task** | ruled yes; unmapped |
| T-2 | conditions become branches | T-017 | read |
| T-3 | the lens gather | T-019 (and T-018) | read |
| T-4 steps 1, 2, 4 | exclusion causes, recorded divergence, fragility note | T-059 | authored 2026-11-13 |
| T-4 step 3 | the Co-1 dimensional boundary (OR-5) | **no task**: held on OR-5b's three open edges (ledger, tenth set) | by decision |
| T-5 | render | T-037 (replaced) | as the workplan says |
| T-6a | language case fold | T-015 | read (Traces) |
| T-6b | search terms from the alias table, `jurisdiction_buckets`, `v_coverage_parameter_via_admission` | T-026 covers the terms half (the search-to-form junction); the buckets and the view have **no task** | title only; OR-8 and OR-12 ruled |
| T-7 | element pointer, derived at read | replaced by T-060 (stored, OR-14b) | by decision |
| T-8 | `add-root` writer; `convergent` needs two distinct roots | T-048 builds the writer; the distinct-roots condition is **not in it** | read (T-048 has no "distinct") |
| D-1 | repair unreadable and prose-unit rows | T-108 | read (Traces) |
| D-2 | fill a NULL lens only where a quote names the users | T-106 | read (Traces) |
| D-3 | the scan contract exercised | T-105 | title only; OR-16 and OR-25 ruled |
| D-4 | promote adjudicated non-English observations to aliases | **no task** (T-107 attests forms; T-112 translates text) | title only; OR-17 ruled |
| D-5 | blind double extraction (measurement) | **no task** | OR-15 and OR-18 ruled |
| D-6 | element pointers (data) | after T-060 | by decision |
| D-7 | re-grade NULL and untraced roots | **no task** | OR-19 and OR-20 ruled |
| D-8 | seed quantities from observed phrases | **no task** (T-109 gives the live parameters their kind) | title only; OR-13 ruled |
| S-1 | the engine over every parameter, rendered | T-110 (then T-037) | read |

Unmapped after this pass (the count is the rows above that say **no task**): they are owed tasks or declines in the owner's words, and are filed as OI-52 in `OPEN-ITEMS-PLAN.md`. None is a decline: every one has a ruling that says yes or gives a rule.

**Pilot results, second round (2026-11-13).** The staged pilots of `OPEN-ITEMS-PLAN.md` section 4 were run (R2 first, then P0 to P7) as Sonnet-class dry pilots in scratch clones, Opus-class for T-028 and T-102; reports and patches are in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/` (`PILOT-BRIEF.md` is the brief every executor got). Which task files now read as piloted: `grep -l '^\*\*Pilot status.\*\* \*\*Piloted' workplan/2026-11-12-bidirectional-pipeline/tasks/T-[0-9]*-*.md`. Departures from the plan, and what the pilots showed:

- **T-014 was a dry pilot, not a real execution**, so no pull request would be opened for the owner to merge. Its behaviour-preservation claim is therefore unproven (the stress scripts hard-code the repository root; T-014's fold makes it derived).
- **T-102 was a partial pilot** (the carry and the emit-and-replay on a sample); the final `SCI` retirement was not reached because T-054 is not in the stack.
- **Every pilot found defects in its task file**; none was an executor's error. The most common were (by how many files they touched): the generated `governance/context-map.yaml` going stale after a migration; `research_tooling_separation` reading `origin/main` and not `$BASE`; objects a section 4 requires but does not name while section 8 forbids unnamed objects; sweeps that match names and miss behaviour; "thin pointer" task files (T-016, T-017, T-019) that were not self-contained and whose cited report's protocol contradicted them. Cross-cutting fixes went into every file by script; per-task fixes by one Opus-class fold per file, each recording design choices as "Chosen (pilot 2026-11-13)".
- **Design faults the pilots found, now corrected in the files:** `--value-as-written` as a free pass (T-008); a junction by rowid that cannot be a foreign key (T-026, T-028 design, T-049); a quantity kind that anything could be minted under (T-020); a foreign key "only for codes present" that SQL cannot do (T-024); a done-when whose premise was false in the data (T-017: parameter 12 carries condition edges); the emitter replaying an INSERT before the UPDATE it depends on (T-018, which blocks T-102 and every carry-by-replace task until it merges).
- **Pilot patches are provisional.** The patches were made from the unfolded files; their real executions will differ. A stacked pilot's result is provisional on its predecessors (`OPEN-ITEMS-PLAN.md` section 4).
- **Environment faults met:** the local `main` ref was stale (a clone's `origin/main` is old), so every pilot took the branch tip as its base; the container disk filled once (pilot clones removed afterwards; reports and patches are kept in the repository).

