# Remediation workplan: a pipeline that runs in every direction, at any stage, across languages and jurisdictions

_Written 2026-11-12 (UTC) by the handshake-and-adversarial leg of the bidirectional-pipeline audit. Planning only: no script, schema, governance file or database row was changed in writing it. Canadian English. Every figure is given as the command that produces it; re-run the command, do not trust a number._

## Precedence (2026-11-14): the term-resolution plan over this plan; the ledger over both

**The owner instructed on 2026-11-14** that the term-resolution plan be folded into this plan, "with this newest plan having priority in conflicts" (ledger: `grep -n -F "Owner instruction 2026-11-14 (last) — fold the term-resolution plan" references/project-standards.md`). So: where this plan, its task files, `OPEN-ITEMS-PLAN.md`, `DECISION-CLOSURE.md` or `OWNER-SHEET-PLAIN.md` disagree with [`TERM-RESOLUTION-PLAN.md`](TERM-RESOLUTION-PLAN.md) (best, ideal and most accommodating as one quantity; most common practice; the minimum; the four figures; showing and grading; the markers and ⚠; stage names), **the term-resolution plan governs**, and the passage changed to match carries a note "Superseded in part by TERM-RESOLUTION-PLAN section n (2026-11-14)". Where either plan disagrees with an owner ruling in the ledger (`references/project-standards.md`), **the ledger governs** (CLAUDE.md rule 0). The fold, item by item, and every conflict it resolved with the text before and after: [`TERM-PLAN-FOLD.md`](TERM-PLAN-FOLD.md). The term plan's tasks are T-117 to T-121 and additions to T-035, T-059 and T-068; its open questions are OD-57 to OD-62.

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
| `workplan/2026-11-12-bidirectional-pipeline/TERM-RESOLUTION-PLAN.md` | The term-resolution plan of 2026-11-14 (best, most common, minimum; markers; showing and grading). **Governs this plan where they conflict** (section "Precedence" above). |
| `workplan/2026-11-12-bidirectional-pipeline/TERM-PLAN-FOLD.md` | Where each numbered item of the term-resolution plan now lives in this plan, and every conflict the fold resolved, before and after. |
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
| [T-030](tasks/T-030-units-as-data.md) | Units and their exact conversions as rows | 4 | 1-2 | TOOLING | Sonnet | T-016, T-020 merged | none; OD-22, OD-24, OD-42 delegated | no |
| [T-031](tasks/T-031-clause-unit-and-open-pass.md) | The clause as a unit, the open pass, and catalogue growth | 4 | 1-2 | TOOLING | NOT FOR SONNET | T-019 merged | OD-23 (answered 2026-11-12) | no |
| [T-032](tasks/T-032-synthesis-relations.md) | Relations synthesis can record, and what a synthesis row is | 4 | 1 | TOOLING | NOT FOR SONNET | T-029, T-050 merged | none outstanding (OD-19 answered: record now; OD-07, OD-12, OD-25, OD-29 delegated; OD-19 moved to T-053) | no |
| [T-033](tasks/T-033-synthesis-candidates.md) | Candidate relations on demand (read-only) | 4 | 2 | TOOLING | Sonnet | T-029, T-030 merged | none | no |
| [T-034](tasks/T-034-cell-status-verb.md) | One read-only answer for a cell at every stage | 4 | 2 | TOOLING | Sonnet | T-013 merged | none | no |
| [T-035](tasks/T-035-skills-repair.md) | Skills that describe the database that exists (and, since the term-resolution fold, the skills rows of TT-4) | 4 | 2 | TOOLING | Sonnet | T-120 merged (term-resolution fold) | OD-60 (the prose register's voice; referred to the owner 2026-11-14) | no |
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
| [T-056](tasks/T-056-all-leaves-identity-lens.md) | ALL leaves the identity lens: universal is stated once, by design_scale | 2 | 1-2 | TOOLING | Sonnet | T-054 merged | OD-48 (what `design_scale` states; items 3 and 3a); OD-31 answered | no |
| [T-101](tasks/T-101-scope-fill.md) | Record the research scope on every pair | research | 3 | RESEARCH | Sonnet | T-025 merged | OD-04 (answered 2026-11-12; and OD-01 delegated) | no |
| [T-102](tasks/T-102-mobility-split.md) | Decompose the mobility family by device, and carry the rows filed under MOB | research | 3 | RESEARCH | NOT FOR SONNET | T-018, T-025, T-054, T-055 merged; `T-102-design.md` present | none outstanding (OD-14 and OD-31 answered 2026-11-12; the codes confirmed in the fifth set and revised in the sixth to ninth: children `WHEEL`, `LLD`, `WALKAID`; `SCI` retired to `WHEEL`) | no |
| [T-103](tasks/T-103-medical-lens.md) | Fill the medical lens by correspondence | research | 3 | RESEARCH | NOT FOR SONNET | none (`add-medical` exists) | OD-15 (answered 2026-11-12: proceed, no WHO agreement sought) | no |
| [T-104](tasks/T-104-verify-governing-sources.md) | Verify the sources a first determination would rest on | research | 3 | RESEARCH | Sonnet | none | none | no |
| [T-105](tasks/T-105-read-held-sources.md) | Read what is held, in full, against every parameter | research | 3 | RESEARCH | NOT FOR SONNET | T-008, T-009, T-016, T-031 merged (OD-23 chose the inventory) | none outstanding (OD-05 delegated) | no |
| [T-106](tasks/T-106-retag-lenses.md) | Tag figures with every relevant model | research | 3 | RESEARCH | NOT FOR SONNET | T-019 merged | none outstanding (OD-06 delegated; mobility codes wait for OD-14) | no |
| [T-107](tasks/T-107-attest-forms.md) | Attest forms per language and jurisdiction from instruments | research | 3 | RESEARCH | NOT FOR SONNET | T-026, T-028 merged | none | no |
| [T-108](tasks/T-108-unit-condition-repair.md) | Move conditions out of the unit cell | research | 3 | RESEARCH | Sonnet | T-016, T-008, T-061 merged | none (the bare-`ratio` rows are T-086's) | no |
| [T-109](tasks/T-109-parameter-kinds-data.md) | Give the live parameters their quantity kind | research | 3 | RESEARCH | NOT FOR SONNET | T-020, T-083 merged | none outstanding (OD-24 delegated) | no |
| [T-110](tasks/T-110-first-determinations.md) | First live determinations | research | 3 | RESEARCH | NOT FOR SONNET | T-019, T-059, T-102, T-104, T-030, T-077 merged | none in the register (OR-5b's three edges open: a stop in the task) | no |
| [T-111](tasks/T-111-as-written-wording-for-stored-rows.md) | Bring the two stored spelled-out figures into line | research | 3 | RESEARCH | Sonnet | T-008 merged | none | no |
| [T-112](tasks/T-112-translate-held-text.md) | Translate the held non-English text that synthesis needs | research | 3 | RESEARCH | Sonnet (drafting); a review verdict is Opus-class | T-049 merged | none outstanding (OD-02, OD-30 delegated) | no |
| [T-113](tasks/T-113-file-sub-national-instruments.md) | File the four held sub-national instruments under their own codes | research | 3 | RESEARCH | Sonnet | T-024 merged | none outstanding (OD-01 delegated; OD-04 answered) | no |
| [T-114](tasks/T-114-retire-move-ves-to-needs.md) | Retire MOVE and VES to the access needs that carry them | research | 3 | RESEARCH | Sonnet | T-054 merged | none outstanding (OD-37 answered) | no |
| [T-116](tasks/T-116-upl-for-upper-limb.md) | Hold the upper-limb population as UPL, and retire LMB to it | research | 3 | RESEARCH | Sonnet | T-025, T-054 merged | none outstanding (OI-13 answered, eighth and ninth sets; `UPL`'s wording and category are proposals the owner confirms) | no |
| [T-058](tasks/T-058-upl-prose-callers.md) | UPL reinstated for upper limb: the retired crosswalk and the prose that names LMB or UPL | 3 | 0-1 | TOOLING | Sonnet | T-116 merged | none outstanding (OI-13 answered) | no |
| [T-057](tasks/T-057-base-coverage-view.md) | The base coverage view: one state per concept and in-scope pair | 3 | 2 | TOOLING | Sonnet | T-026, T-028 merged | none (the owner's 2026-11-06 acceptance test, AT-23) | no |
| [T-059](tasks/T-059-wp-t4-agreement.md) | The prior workplan's T-4: agreement (true exclusion causes, recorded divergence, the fragility note), and selection across all tiers under the harm test (TT-2) | 1 | 2 | TOOLING | NOT FOR SONNET | T-016, T-019, T-120 merged | OD-58 (what proves "worse results"; referred to the owner 2026-11-14); OR-4 and OR-6c read through the harm test for selection; OR-6, OR-6b answered; OR-5b's edges open and held out of this task | no |
| [T-060](tasks/T-060-element-determination.md) | The specifications pass writes an element-level determination (OR-14b) | 5 | 2 | TOOLING | NOT FOR SONNET | T-019, T-029 merged; design file first | none (OR-14b answered 2026-11-13) | no |
| [T-115](tasks/T-115-retag-all-rows.md) | Re-tag the figures filed under ALL by their heading's group, then retire ALL | research | 3 | RESEARCH | NOT FOR SONNET | T-018, T-056 merged | none outstanding (OD-31 answered) | no |
| [T-061](tasks/T-061-amend-extraction-reformat.md) | `amend-extraction` reformats a figure's value, unit or empty setting in place (the prior workplan's T-1b step 8) | 1 | 2 | TOOLING | Sonnet | T-008, T-016 merged | none (OR-3 answered 2026-10-29); its `ratio` branch is T-093's (OD-41 delegated) | no |
| [T-062](tasks/T-062-verified-reading-blocking.md) | A `verified` figure with no full reading is refused at rest, not only at write (the prior workplan's T-1b step 10, finished) | 5 | 0 | TOOLING | Sonnet | T-105 merged; VERIFIED-WITHOUT-FULL-READING empty on the base | none (OR-11a answered) | no |
| [T-063](tasks/T-063-derive-extraction-repair.md) | `derive-extraction` can write a derived figure honestly | 2 | 2 | TOOLING | Sonnet (OD-40 resolved under delegation) | T-016, T-018 merged | none; OD-40 delegated | no |
| [T-067](tasks/T-067-coverage-per-parameter-via-admission.md) | Coverage per parameter and in-scope pair, reached through admissions | 3 | 2 | TOOLING | Sonnet | none (soft: after T-050) | none (OR-8, OD-04 answered) | no |
| [T-068](tasks/T-068-convergent-counts-roots.md) | A convergent cell states its sources, their tiers and its independent roots (and, since the term-resolution fold, the engine strings of TT-1) | 2 | 2 | TOOLING | NOT FOR SONNET | T-059, T-120 merged | OD-43 (answered by the owner 2026-11-14) | no |
| [T-069](tasks/T-069-promote-adjudicated-observations.md) | Promote the adjudicated non-English observations to forms of their terms | research | 3 | RESEARCH | NOT FOR SONNET | T-026, T-028 merged | none in the register (OR-17); OI-55 (6) holds the non-instrument part | no |
| [T-070](tasks/T-070-blind-double-extraction.md) | Blind double extraction: do two readers, and do model and effort, record the same rows? | research | 3 | RESEARCH | NOT FOR SONNET | T-016 merged | OD-44 (answered by the owner 2026-11-14: A); the owner launches the raters | no |
| [T-071](tasks/T-071-regrade-roots.md) | Give every value-supplying figure its root | research | 3 | RESEARCH | NOT FOR SONNET | T-048 merged | none (OR-19, OR-20 answered) | no |
| [T-072](tasks/T-072-seed-quantities-from-codes.md) | Seed the list of quantities from the phrases the held codes use | research | 3 | RESEARCH | NOT FOR SONNET | T-020, T-028, T-101, T-105 merged | none in the register (OR-13, OR-17); a new quantity kind needs an owner-approved entry | no |
| [T-073](tasks/T-073-fixture-ids-free-of-the-retrieval-log.md) | A fixture source never takes an id the retrieval log already holds | 0 (now) | 0 | TOOLING | Sonnet | none | none | no |
| [T-074](tasks/T-074-latest-adjudication-names-the-term.md) | An alias or a rename rests on the latest adjudication of its observation | 0 (now) | 2 | TOOLING | Sonnet | none | none | no |
| [T-075](tasks/T-075-gate-reports-its-subject-and-base.md) | The gate reports what each check examined, against the base it was given, and rebuilds when its inputs change | 0 (now) | 0 | TOOLING | Sonnet | none | none | no |
| [T-076](tasks/T-076-stale-empty-claims.md) | Sentences and suppressions that call a populated table empty | 0 (now) | 0-1 | TOOLING | Sonnet | none | none (records D-0152's supersession) | no |
| [T-077](tasks/T-077-medical-only-determination-refused.md) | A determination keyed on a medical code alone is refused at write | 0 (now) | 1-2 | TOOLING | Sonnet | none | none (contract criterion no-diagnosis-only-determination) | no |
| [T-078](tasks/T-078-figure-retires-in-place.md) | A figure retires in place | 2 | 1-2 | TOOLING | NOT FOR SONNET | none | none in the register ("retire in place then"; OI-55 (7) related, not waited on) | no |
| [T-079](tasks/T-079-deferred-acts-with-age.md) | A deferred reading is recorded, and every deferred act lists with its age from one view | 2 | 1-2 | TOOLING | Sonnet | none | none | no |
| [T-080](tasks/T-080-zero-result-search-states-its-cause.md) | A zero-result search states its cause when it is logged | 2 | 2 | TOOLING | Sonnet | none | none; OD-45 delegated | no |
| [T-081](tasks/T-081-classify-zero-result-searches.md) | Each stored zero-result search states its cause | research | 3 | RESEARCH | NOT FOR SONNET | T-080 merged | none; OD-45 delegated; OI-55 (1) | no |
| [T-082](tasks/T-082-comparator-on-two-stored-figures.md) | The two stored numerical claims with no comparator get one from their source | research | 3 | RESEARCH | NOT FOR SONNET | none | none (OI-55 (1) applies) | no |
| [T-083](tasks/T-083-set-kind-on-existing-parameter.md) | A verb sets the quantity kind and its warrant on an existing parameter | 1 | 2 | TOOLING | Sonnet | T-020 merged | none outstanding (OD-24 delegated) | no |
| [T-084](tasks/T-084-unregistered-map-codes.md) | The language-and-jurisdiction map names only declared jurisdictions | research | 3 | RESEARCH | Sonnet once answered | T-024, T-025 merged | OD-46; OI-55 (1) | no |
| [T-085](tasks/T-085-map-jurisdiction-foreign-key.md) | The map's jurisdiction column points at the registry | 3 | 1 | TOOLING | Sonnet | T-084 merged | OD-46 (inherited through T-084) | no |
| [T-086](tasks/T-086-bare-ratio-rows.md) | The stored gradients whose unit says only `ratio` | research | 3 | RESEARCH | NOT FOR SONNET | T-061, T-093 merged | none; OD-41 delegated (a reformat); OD-55 delegated, not reached while OD-41 stands | no |
| [T-087](tasks/T-087-edmonton-checklist-batch.md) | Ship the Edmonton checklist digest as a research batch | research | 3 | RESEARCH | NOT FOR SONNET | T-073 merged (T-074 first only if the batch writes an alias or a rename from an observation) | none as a gate; parts held: figures parked on OD-47, observations deferred on OD-52 (both referred to the owner); OD-50 and OD-53 delegated (it may promote quantities and decline elements, lens terms and methods; R16 waived only for terms left undisposed); OD-51 referred, not waited on | no |
| [T-088](tasks/T-088-refusal-capture-and-disposition.md) | A writer's refusal is kept, and every refusal a batch met is disposed | 2 | 0-2 | TOOLING | Sonnet | none | none (OD-54 holds no part of it) | no |
| [T-089](tasks/T-089-refusal-register-reader.md) | The refusal register: every captured refusal, its class, and what it cues | 2 | 0 | TOOLING | Sonnet | T-088 merged | none | no |
| [T-090](tasks/T-090-coverage-reads-at-batch-done.md) | Every research batch reports which groups the catalogue can speak about | 2 | 0 | TOOLING | Sonnet | none | none | no |
| [T-091](tasks/T-091-typed-circumstance-carrier.md) | A figure's circumstance (building use, interior or exterior) in typed cells | 4 | 1-2 | TOOLING | NOT FOR SONNET | none; `T-091-design.md` written first | none; OD-49 delegated (scope narrowed by the owner 2026-11-14) | no |
| [T-092](tasks/T-092-retag-circumstances.md) | Re-tag each stored figure's circumstance from its free-text setting | research | 3 | RESEARCH | NOT FOR SONNET | T-091 merged | none; OD-49 delegated (scope narrowed by the owner 2026-11-14) | no |
| [T-093](tasks/T-093-ratio-unit-reformat-branch.md) | `amend-extraction` accepts `ratio` to `rise:run ratio` as a reformat (OD-41, resolved under delegation) | 1 | 2 | TOOLING | Sonnet | T-061 merged | none; OD-41 delegated | no |
| [T-117](tasks/T-117-marker-table-applied.md) | The marker table applied: a circle by tier, and ⚠ in place of it for a grey, unverified or thin basis (term plan TT-3) | 6 | 1-2 | TOOLING | NOT FOR SONNET | T-119, T-120, T-068 merged | OD-57, OD-59 (referred to the owner 2026-11-14) | no |
| [T-118](tasks/T-118-stage-tools-carry-specification-name.md) | The specification stage's tools carry the stage's name (term plan TT-7; deferred) | 6 | 1-2 | TOOLING | Sonnet | T-021, T-059, T-068, T-117 merged | none (defaults: no aliases; the stage stays specification) | no |
| [T-119](tasks/T-119-ledger-unification-entry.md) | The ledger's unification entry, with its supersession pairs (term plan PR-1) | 0 (now) | 0 | TOOLING | NOT FOR SONNET | none | none | no |
| [T-120](tasks/T-120-doctrine-amendments-and-deletions.md) | Doctrine says what the owner ruled; dead names and copies removed; atoms re-quoted (term plan PR-2) | 0 (now, after T-119) | 0-1 | TOOLING | NOT FOR SONNET | T-119 merged | none | no |
| [T-121](tasks/T-121-ignore-frozen-bpc.md) | The frozen best-practices compendium leaves agent search (term plan Q5) | 0 (once answered) | 0 | TOOLING | Sonnet | none | OD-61 (referred to the owner 2026-11-14) | no |

## 4. Wave 0: what can start now

**No owner decision, no design, no earlier wave.** The set, by command: `grep -l "^| Wave | 0 (now) |" workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md`. Today that is: [T-001](tasks/T-001-layer0-marks-and-text.md), [T-002](tasks/T-002-contract-entry-text.md), [T-003](tasks/T-003-owner-queue-answered-marks.md), [T-004](tasks/T-004-spec-checks-report-live-rows.md), [T-005](tasks/T-005-retired-row-view-fixture.md), [T-006](tasks/T-006-delete-connection-refusal.md), [T-007](tasks/T-007-add-source-standing.md), [T-008](tasks/T-008-claimed-number-check.md), [T-009](tasks/T-009-script-aware-guards.md), [T-010](tasks/T-010-add-parameter-domain-refusal.md), [T-011](tasks/T-011-supersession-pointer.md), [T-012](tasks/T-012-follow-up-reasons.md), [T-013](tasks/T-013-typed-gaps.md), [T-014](tasks/T-014-stress-harness-and-probes.md), [T-015](tasks/T-015-language-fold.md), [T-041](tasks/T-041-one-home-for-helpers.md), [T-042](tasks/T-042-derive-choices-and-counts.md), [T-043](tasks/T-043-refusals-name-next-action.md), [T-051](tasks/T-051-gap-register-cross-stage.md), [T-052](tasks/T-052-mining-stages-out-of-scope-leads.md) (the last two added by the delegated pass), [T-075](tasks/T-075-gate-reports-its-subject-and-base.md), [T-076](tasks/T-076-stale-empty-claims.md), [T-077](tasks/T-077-medical-only-determination-refused.md) (the last three added 2026-11-13 from the pilots' findings and not placed in the merge order below: T-075 after T-014, since it changes the gate the harness is run through; T-077 before T-110, an edge the dependency list holds; T-076 any time). [T-073](tasks/T-073-fixture-ids-free-of-the-retrieval-log.md) and [T-074](tasks/T-074-latest-adjudication-names-the-term.md) were added 2026-11-13 from OI-57 (18) and (6), also outside the merge order: T-073 before the research batch that admits an id a pre-admission retrieval-log folder holds (T-087, the Edmonton batch, depends on it); T-074 preferably before T-069, but not as a gate: T-069 selects its candidates by the latest adjudication itself, so the stricter writer changes none of its writes (checked 2026-11-13).

**Added 2026-11-14 by the term-resolution fold:** [T-119](tasks/T-119-ledger-unification-entry.md) (the ledger's unification entry; Opus-class) can start now, and [T-120](tasks/T-120-doctrine-amendments-and-deletions.md) (the doctrine, Opus-class) after it; neither needs an owner answer (TERM-RESOLUTION-PLAN §7: "PR-2 and PR-3 can ship now"). They sit outside the merge order below; T-120 must merge before T-035, T-059 and T-068, which point to the doctrine home it writes. [T-121](tasks/T-121-ignore-frozen-bpc.md) is one line, held on OD-61.

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
| 1 | the lens chain and the parameter kind | [T-016](tasks/T-016-wp-t1a-reading.md), [T-017](tasks/T-017-wp-t2-conditions.md), [T-018](tasks/T-018-link-table.md), [T-019](tasks/T-019-lens-gather.md), [T-059](tasks/T-059-wp-t4-agreement.md), [T-020](tasks/T-020-quantity-kind.md), [T-061](tasks/T-061-amend-extraction-reformat.md), [T-083](tasks/T-083-set-kind-on-existing-parameter.md), [T-093](tasks/T-093-ratio-unit-reformat-branch.md) | Serial: T-016, T-017, T-018, T-019, T-059. T-020 beside them (OD-24 resolved under delegation). T-061 after T-008 and T-016 (and before T-108); T-083 after T-020 (and before T-109); T-093 after T-061, held on OD-41 and built only under its answer (a) (then before T-086). |
| 2 | carriers for going back, and for translation | [T-021](tasks/T-021-cell-question-gate.md), [T-022](tasks/T-022-contract-re-entry.md), [T-023](tasks/T-023-ledger-relayed-statements.md), [T-048](tasks/T-048-root-registry-writer.md), [T-049](tasks/T-049-translation-home.md), [T-050](tasks/T-050-retire-admission-edges-and-connections.md), [T-063](tasks/T-063-derive-extraction-repair.md), [T-068](tasks/T-068-convergent-counts-roots.md), [T-078](tasks/T-078-figure-retires-in-place.md), [T-079](tasks/T-079-deferred-acts-with-age.md), [T-080](tasks/T-080-zero-result-search-states-its-cause.md), [T-088](tasks/T-088-refusal-capture-and-disposition.md), [T-089](tasks/T-089-refusal-register-reader.md), [T-090](tasks/T-090-coverage-reads-at-batch-done.md) | T-048 any time; T-049 after T-008; T-050 after T-006; T-021 after T-019; T-022 after its three; T-023 any time (OD-28 answered). T-063 after T-016 and T-018, held on OD-40; T-068 after T-059, held on OD-43; T-078 and T-079 any time (T-005 soft after T-078); T-080 held on OD-45. T-088 any time, then T-089 (the refusal register, owner statements 1 to 5 of 2026-11-13); T-090 any time (all three edit `/batch-done`: one lane). |
| 3 | a base that is data | [T-024](tasks/T-024-jurisdiction-registry.md), [T-025](tasks/T-025-base-writers.md), [T-026](tasks/T-026-alias-attestation.md), [T-027](tasks/T-027-source-identity-edition.md), [T-028](tasks/T-028-concept-identity.md), [T-047](tasks/T-047-add-by-data-test.md), [T-057](tasks/T-057-base-coverage-view.md), [T-067](tasks/T-067-coverage-per-parameter-via-admission.md), [T-085](tasks/T-085-map-jurisdiction-foreign-key.md) | T-024 then T-025; T-027 any time; T-028's one-page design first, then T-026, then T-028's build; T-047 last. T-067 any time (after T-050 if both are open); T-085 after the research task T-084 (held on OD-46). |
| 4 | reading once, abstraction, synthesis | [T-029](tasks/T-029-term-relations.md), [T-030](tasks/T-030-units-as-data.md), [T-031](tasks/T-031-clause-unit-and-open-pass.md), [T-032](tasks/T-032-synthesis-relations.md), [T-033](tasks/T-033-synthesis-candidates.md), [T-034](tasks/T-034-cell-status-verb.md), [T-035](tasks/T-035-skills-repair.md), [T-053](tasks/T-053-engine-conflict-between-groups.md), [T-091](tasks/T-091-typed-circumstance-carrier.md) | T-034 after T-013; T-035 any time; T-029 after T-020; T-030 and T-032 after their dependencies (their decisions are delegated); T-031 after T-019 (OD-23 answered); T-033 after T-029 and T-030. T-053 after T-032 (OD-36 answered). T-091 held on OD-49, its design written after the answer. |
| 5 | render and the gate over it | [T-036](tasks/T-036-jurisdiction-comparison-view.md), [T-037](tasks/T-037-render.md), [T-038](tasks/T-038-stage-pair-gate.md), [T-039](tasks/T-039-owner-edits.md), [T-040](tasks/T-040-deletion-candidates-sweep.md), [T-060](tasks/T-060-element-determination.md), [T-062](tasks/T-062-verified-reading-blocking.md) | T-036 after T-024 and T-101 (OD-04 answered); T-037 after its four dependencies; T-038 after T-037; T-039; T-040. T-062 after the research task T-105, once its blocking class prints 0 rows on the base. |
| 6 | term resolution (TERM-RESOLUTION-PLAN, 2026-11-14) | [T-119](tasks/T-119-ledger-unification-entry.md), [T-120](tasks/T-120-doctrine-amendments-and-deletions.md), [T-121](tasks/T-121-ignore-frozen-bpc.md), [T-117](tasks/T-117-marker-table-applied.md), [T-118](tasks/T-118-stage-tools-carry-specification-name.md); and the additions to [T-035](tasks/T-035-skills-repair.md) (TT-4), [T-059](tasks/T-059-wp-t4-agreement.md) (TT-2) and [T-068](tasks/T-068-convergent-counts-roots.md) (TT-1) | The term plan's sequence: T-119 (PR-1), then T-120 (PR-2), both now; then T-068's strings and T-035's skills (PR-3), and T-059's selection once OD-58 is answered; then T-117 (PR-4) once OD-57 and OD-59 are answered; the re-assessment of live specifications (PR-5) is T-110's first write, or a research batch after T-117 if T-110 lands first (OI-65); T-118 (PR-6) last, deferred. T-121 any time once OD-61 is answered. "Wave 6" names the work, not its place: T-119 and T-120 can merge before Wave 1. |
| research | rows, each in its own pull request | [T-101](tasks/T-101-scope-fill.md), [T-102](tasks/T-102-mobility-split.md), [T-103](tasks/T-103-medical-lens.md), [T-104](tasks/T-104-verify-governing-sources.md), [T-105](tasks/T-105-read-held-sources.md), [T-106](tasks/T-106-retag-lenses.md), [T-107](tasks/T-107-attest-forms.md), [T-108](tasks/T-108-unit-condition-repair.md), [T-109](tasks/T-109-parameter-kinds-data.md), [T-110](tasks/T-110-first-determinations.md), [T-111](tasks/T-111-as-written-wording-for-stored-rows.md), [T-112](tasks/T-112-translate-held-text.md), [T-113](tasks/T-113-file-sub-national-instruments.md), [T-069](tasks/T-069-promote-adjudicated-observations.md), [T-070](tasks/T-070-blind-double-extraction.md), [T-071](tasks/T-071-regrade-roots.md), [T-072](tasks/T-072-seed-quantities-from-codes.md), [T-081](tasks/T-081-classify-zero-result-searches.md), [T-082](tasks/T-082-comparator-on-two-stored-figures.md), [T-084](tasks/T-084-unregistered-map-codes.md), [T-086](tasks/T-086-bare-ratio-rows.md), [T-087](tasks/T-087-edmonton-checklist-batch.md), [T-092](tasks/T-092-retag-circumstances.md) | T-104 is ungated; T-111 follows T-008 and T-108 follows T-016 and T-061 (its bare-`ratio` rows are T-086's, which follows T-061 and waits on OD-41); the rest wait for tooling, an answer, or an Opus-class session. T-113 follows T-024. T-082 is ungated (Opus-class); T-069 after T-026 and T-028; T-070 after T-016, held on OD-44; T-071 after T-048; T-072 after T-020, T-028, T-101 and T-105; T-081 after T-080 (OD-45); T-084 after T-024 and T-025 (OD-46). T-087 (the Edmonton batch) after T-073, Opus-class, with parts parked on OD-47, deferred on OD-50 and OD-52, and R16 red pending OD-53; T-092 after T-091 (OD-49). |

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
T-030 <- T-016, T-020   [delegated: OD-22, OD-24, OD-42 (confirmed with corrections, 2026-11-13)]
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
T-056 <- T-054   [owner: OD-31, answered; OD-48, open (items 3 and 3a)]
T-101 <- T-025   [owner: OD-04, answered; delegated: OD-01]
T-102 <- T-018, T-025, T-054, T-055; the design `tasks/T-102-design.md`, its codes confirmed by the owner (fifth set); an Opus-class session   [owner: OD-14, OD-31, OD-37, answered]
T-103 <- (no task)   [owner: OD-15, answered]
T-105 <- T-008, T-009, T-016, T-031   [delegated: OD-05; T-031 hard since OD-23 chose the inventory]
T-106 <- T-019   [delegated: OD-06]
T-107 <- T-026, T-028, T-057
T-108 <- T-008, T-016, T-061   [the bare-ratio rows are T-086's]
T-109 <- T-020, T-083   [delegated: OD-24]
T-110 <- T-019, T-059, T-102, T-104, T-030, T-077 (T-030 so length parameters get a value; T-077 so a medical-only determination is not writable once T-103 fills the medical registry); the owner's confirmation of the T-102 codes (fifth set, in the ledger); the blocking battery green on the scratch copy; an Opus-class session
T-111 <- T-008
T-112 <- T-049   [delegated: OD-02, OD-30]
T-113 <- T-024   [delegated: OD-01; owner: OD-04, answered]
T-114 <- T-054   [owner: OD-37, answered]
T-115 <- T-018, T-056   [owner: OD-31, answered]
T-116 <- T-025, T-054   [OI-13, answered]
T-058 <- T-116   [OI-13, answered]
T-057 <- T-026, T-028
T-059 <- T-016, T-019, T-120   [owner: OD-58, open (TT-2, what proves worse results); OR-4 and OR-6c read through the harm test for selection]
T-060 <- T-019, T-029; the design `tasks/T-060-design.md`   [owner: OR-14b, answered 2026-11-13]
T-005 <- (no task)   [soft: after T-078 if both are open]
T-061 <- T-008, T-016   [owner: none (OR-3 answered); its ratio branch is T-093's, on OD-41 delegated]
T-062 <- T-105   [owner: none (OR-11a answered); VERIFIED-WITHOUT-FULL-READING prints 0 rows on the base]
T-063 <- T-016, T-018   [delegated: OD-40 (confirmed with corrections, 2026-11-13)]
T-067 <- (no task)   [soft: after T-050 if both are open; OR-8 and OD-04 answered]
T-068 <- T-059, T-120   [owner: OD-43, answered 2026-11-14 (refined the same day); TT-1 strings point to T-120's doctrine home]
T-069 <- T-026, T-028   [OR-17; OI-55 (6) holds the non-instrument observations]
T-070 <- T-016   [owner: OD-44, open; the owner launches the raters]
T-071 <- T-048   [OR-19, OR-20 answered; T-048 now makes root_id amendable (OI-57 (7), fold 2026-11-13)]
T-072 <- T-020, T-028, T-101, T-105   [OR-13, OR-17; a new quantity kind needs an owner-approved entry]
T-073 <- (no task)   [OI-57 (18); before the batch that admits the id a pre-admission retrieval-log folder holds]
T-074 <- (no task)   [OI-57 (6); preferably before T-069, not a gate: T-069 selects by the latest adjudication itself]
T-075 <- (no task)
T-076 <- (no task)
T-077 <- (no task)
T-078 <- (no task)   [OI-55 (7) related, not waited on]
T-079 <- (no task)
T-080 <- (no task)   [delegated: OD-45 (confirmed with corrections, 2026-11-13)]
T-081 <- T-080   [delegated: OD-45 (confirmed with corrections, 2026-11-13); OI-55 (1)]
T-082 <- (no task)   [OI-55 (1)]
T-083 <- T-020   [delegated: OD-24]
T-084 <- T-024, T-025   [owner: OD-46, open; OI-55 (1)]
T-085 <- T-084   [owner: OD-46, through T-084]
T-086 <- T-061, T-093   [delegated: OD-41 (a reformat; confirmed with corrections, 2026-11-13); OD-55 delegated, reached only if OD-41 is reversed; carved out of T-108]
T-087 <- T-073   [no owner gate; parts held: figures parked on OD-47, observations deferred on OD-52 (the path phrases), both referred to the owner; OD-50 and OD-53 delegated (quantity concepts may be promoted; elements, lens terms and methods declined; R16 waived only for terms left undisposed); T-074 first only if it writes an alias or a rename from an observation]
T-088 <- (no task)   [owner statements 1 to 5 of 2026-11-13; OD-54 holds no part]
T-089 <- T-088
T-090 <- (no task)
T-091 <- (no task); the design `tasks/T-091-design.md`, written first   [delegated: OD-49 (confirmed with corrections, 2026-11-13)]
T-092 <- T-091   [delegated: OD-49 (confirmed with corrections, 2026-11-13)]
T-093 <- T-061   [delegated: OD-41 (a reformat; confirmed with corrections, 2026-11-13)]
T-035 <- T-120   [owner: OD-60, open (the prose register's voice); term plan TT-4]
T-117 <- T-119, T-120, T-068   [owner: OD-57 and OD-59, open (the circle table; the grade of a mixed cell); term plan TT-3 and the W rows]
T-118 <- T-021, T-059, T-068, T-117   [no owner gate; defaults: no aliases, the stage stays specification; OD-62 optional; term plan TT-7, deferred]
T-119 <- (no task)   [term plan PR-1; an attestation; Opus-class]
T-120 <- T-119   [term plan PR-2; Opus-class]
T-121 <- (no task)   [owner: OD-61, open (.ignore)]
```

## 6. Stop points

| When | Who is waited for | What for | What can continue meanwhile |
|---|---|---|---|
| Before T-018 | DISCHARGED 2026-11-12: the design of the link table is written (`tasks/T-018-design.md`) | nothing further; T-018 is Sonnet's | — |
| Before T-026 | DISCHARGED 2026-11-12: the forms-home design of T-028 is written (`tasks/T-028-design.md`) and names the one table that holds a form (`term_aliases`) | nothing further for T-026; T-028 itself stays NOT FOR SONNET | — |
| Before T-102, and so T-110 | DISCHARGED 2026-11-12 as to the owner: the design is written and the owner confirmed its codes and edges (fifth set), so no report is appended. STILL OUTSTANDING: T-018, T-025 and T-055 merge | nothing from the owner (the children's ICF crossings alone wait for an explicit yes, and block no row) | T-104; T-106 after T-019 (ICF and needs lenses only); T-054, T-114 |
| Before T-110 | the blocking battery, green on the scratch copy, the integrity test included | a first live determination | — |
| At the end of every wave | the owner | the wave's lines of the Definition of Done (section 10), run and reported; `python3 workplan/pipeline-state-graph/walkability.py` run as a command until T-038 registers it | — |
| Before T-070, T-084 (so T-085) | the owner: OD-44 and OD-46, referred back on 2026-11-13 by the second delegated pass and its independent check (section 8; the plain questions: `OWNER-SHEET-PLAIN.md`). OD-40 to OD-43 and OD-45 were resolved under delegation on 2026-11-13; they open T-030 (so T-033 and T-110), T-063, T-068, T-080 (so T-081), T-093 and T-086 only through their confirmed check lines (the gate of section 13), and the owner may reverse any of them | each answer, in the owner's words, with its status line in the ledger | every task whose gates are OPEN |
| Before T-056 (so T-115) | the owner: OD-48, referred back on 2026-11-13; with it OD-47, OD-51, OD-52 and OD-54, also referred, which hold no task's gate (OD-47 and OD-52 hold parts of T-087). OD-49, OD-50, OD-53 and OD-55 were resolved under delegation on 2026-11-13 (OD-47 to OD-54 are the Edmonton adjudication's AQ-1 to AQ-8); OD-49 opens T-091 (so T-092) only through its confirmed check line (section 13) | each answer, in the owner's words, with its status line in the ledger (the plain questions: `OWNER-SHEET-PLAIN.md`) | every task whose gates are OPEN; T-088, T-089, T-090 need no answer |
| Before T-059 (so T-068, T-110, T-117, T-118), T-035, T-117 and T-121 | the owner: OD-57 to OD-61, registered and referred on 2026-11-14 from the term-resolution plan's Q1 to Q5 (OD-62, its optional Q6, holds nothing; the default, no rename, stands while it is unanswered). OD-58 holds T-059 (selection under the harm test); OD-60 holds T-035 (the voice line); OD-57 and OD-59 hold T-117 (the circle table and the grade of a mixed cell); OD-61 holds T-121 (`.ignore`). None is to be resolved under delegation (evidence-tier definitions are always DG-NON) | each answer, in the owner's words, with its status line in the ledger (the plain questions: `OWNER-SHEET-PLAIN.md`, questions 8 to 13) | T-119 and T-120 (no answer needed), and every task whose gates are OPEN |
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

**Status after the delegated pass and the twelfth-instruction pass (2026-11-12).** Each entry below opens with its status. How many are resolved under delegation, referred back, still the owner's, or block a task is derived, never typed: run the gate loop of section 13 for the state of each, and a copy of `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py` whose `OUT` points outside the tree (the script writes `REMEDIATION-PLAN.md` despite its docstring: fact 12 of `DELEGATED-RESOLUTIONS-2-REVIEW.md`) for which of the CLOSED ones a task waits on (its last-but-one output line names the blocking and the standing sets; `REMEDIATION-PLAN.md` shows them with the tasks they release). The confirmation of each, with evidence, is `DECISION-CLOSURE.md`. A task no longer checks `grep -n -F "OD-NN:"`, which a delegated, a withdrawn and an owner's line all satisfied alike: it runs the ledger gate of section 13, which is OPEN only for an owner's answer, or for a delegated resolution whose independent check is not required or is recorded as confirmed. A task that needs the owner's words (T-102, T-053) opens only on an owner's answer. The rest of this register is as first written, so "Recommendation (the audit's …)" and "Tasks blocked until answered" describe the state before the pass; the status line says what holds now. **The second delegated pass (2026-11-13).** At the owner's question of 2026-11-13 (`grep -n -F "Owner question 2026-11-13 — may the open decisions OD-40 to OD-55" references/project-standards.md`), OD-40, OD-41, OD-42, OD-43, OD-45, OD-49, OD-50, OD-53 and OD-55 were resolved under the owner's twelfth instruction and confirmed with corrections by an independent check; OD-44, OD-46, OD-47, OD-48, OD-51, OD-52 and OD-54 were referred back and are put to the owner in plain words in `OWNER-SHEET-PLAIN.md`. Each of OD-40 to OD-55 keeps its registration status as an "Earlier status" line.

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

### OD-40  What a derived figure carries as its quote and its locator

- **Status (2026-11-13): RESOLVED UNDER DELEGATION 2026-11-13, check confirmed with corrections applied** — `OD-40 CHECK: confirmed with corrections applied`. Not the owner's words; reversible by the owner; resolved under the owner's twelfth instruction of 2026-11-12, applied at the owner's question of 2026-11-13, and checked under condition (d) by a second, independent Opus-class instance, whose corrections are applied. It opens a task's gate only through that confirmed check line (the gate of section 13); a delegated resolution never opens a gate that needs the owner's words. Ledger: `grep -n -F "Delegated resolution 2026-11-13 — OD-40" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS-2.md`, section OD-40; check: `DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-40. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-063.
- **Earlier status (2026-11-13, at registration): OPEN (not yet asked)** — raised by the authoring of T-063 (its OQ-A); no ledger line exists, so its gate reads CLOSED. **Holds:** T-063.
- **Question.** A derived figure is one the project computes from two figures it already holds (a base plus a delta, for example a clear width plus a door-swing allowance), "never read off a source directly" (`grep -n -F 'never read off the source' scripts/migrations/075_extraction_relations.sql`). Every other figure carries a quote found in the source's saved bytes and a locator (R3). A computed figure has no sentence of its own in any source, so `derive-extraction` is refused every time and no derived figure exists (`python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select count(*) from source_value_extractions where figure_role='derived'\").fetchone())"`). Its two inputs each carry a verified quote and a locator, and each of the two edges that tie the derived figure to them carries its input's quote. What does a derived figure carry as its quote and its locator?
- **Why it is the owner's.** The verbatim floor is the project's defence against fabricated citations (CLAUDE.md §5 (c)); (a) and (b) each exempt one kind of row from part of it, and two records of the project point different ways (the verb's design intent, and the 2026-09-13 quote check, which together made the verb unable to write). No ruling settles it: `git grep -n -i -E "derived (figure|row).{0,60}(quote|claim_text|verbatim)" -- references/project-standards.md decisions` prints nothing.
- **Options and what follows from each.**
  - (a) None of its own: its words and its place are its two inputs', reached through its two `derived_from` edges ("It is better to have a table cell point to another table cell than to rewrite", CLAUDE.md rule 5). *Then:* the writer stores no quote and no locator for a derived row, refuses one whose inputs lack a quote or a locator, and still checks the arithmetic (T-063 section 4 item 3, under (a)).
  - (b) The analyst's arithmetic sentence ("5.5 + 9.25 = 14.75") as its quote, exempt from the saved-bytes check because `figure_role = 'derived'` already says no source wrote it, but checked to state the stored number; the locator reached through its inputs as in (a). *Then:* the verb's design intent of 2026-09-13 (`grep -n -F "the analyst's computation statement" scripts/db.py`); one row kind skips the saved-bytes test (T-063 section 4 item 3, under (b)).
  - (c) No derived rows: the verb is deleted. *Then:* a figure the project computes is stated only in a determination's note or a synthesis; T-063 deletes `derive_extraction`, its parser and dispatch, its state-graph needle and tests T016-N11 to N11e, and keeps the arithmetic check that `add-extraction` and `relate-extraction` still reach.
- **Recommendation (the author's, not a decision).** None given: T-063 writes the change under each answer and leaves the choice to the owner.
- **Answer in one line.** `OD-40: a derived figure has no quote or locator of its own; both are its inputs'` · `OD-40: a derived figure's quote is the analyst's arithmetic, number-checked; its locator is its inputs'` · `OD-40: no derived rows; delete the verb`
- **Tasks blocked until answered.** None now: resolved under delegation (status above); T-063 (now open on its gate). At registration: T-063
- **Where the evidence is.** `tasks/T-063-derive-extraction-repair.md` sections 2 and 3; `grep -n -F 'KNOWN DEFECT, recorded by T' scripts/db.py`

### OD-41  Is changing the unit `ratio` to `rise:run ratio` on the stored rows a reformat or a new reading?

- **Status (2026-11-13): RESOLVED UNDER DELEGATION 2026-11-13, check confirmed with corrections applied** — `OD-41 CHECK: confirmed with corrections applied`. Not the owner's words; reversible by the owner; resolved under the owner's twelfth instruction of 2026-11-12, applied at the owner's question of 2026-11-13, and checked under condition (d) by a second, independent Opus-class instance, whose corrections are applied. It opens a task's gate only through that confirmed check line (the gate of section 13); a delegated resolution never opens a gate that needs the owner's words. Ledger: `grep -n -F "Delegated resolution 2026-11-13 — OD-41" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS-2.md`, section OD-41; check: `DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-41. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-093 and T-086 (the bare-`ratio` rows); T-061's note points at T-093.
- **Earlier status (2026-11-13, at registration): OPEN (not yet asked)** — raised by the authoring of T-061 (its hand-back's OQ-B); no ledger line exists, so its gate reads CLOSED. **Holds:** T-086 (the bare-`ratio` rows, carved out of T-108 on 2026-11-13 so that T-108 no longer waits), and a one-branch follow-up to T-061 that T-061 does not build.
- **Question.** Stored rows hold the bare word `ratio` as their unit and a figure written `1:20` (`python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select group_concat(extraction_id) from source_value_extractions where claimed_unit='ratio'\").fetchone())"`). OR-3 lets a figure's value, unit or empty setting be reformatted in place when the numbers and the quote stay the same; D-0168 makes a different reading a second row. `rise:run ratio` names a horizontal run that the stored cell does not. Is changing the unit from `ratio` to `rise:run ratio` a reformat under OR-3, or a new reading under D-0168?
- **Why it is the owner's.** It is a reading of the owner's own ruling OR-3 (`grep -n -F 'OR-3: "Yes, reformat in place"' references/project-standards.md`) against the narrower rule it carved out of (`grep -n -F 'Reformatting a figure' references/project-standards.md`).
- **Options and what follows from each.**
  - (a) A reformat. *Then:* one branch is added to T-061's `_refuse_unless_reformat` (accept a new unit that is a member of `dbcore.NOTATION_FAMILIES` when the old unit stands, on word boundaries, in the new one and the stored figure reads under it), and T-086 amends those rows in place.
  - (b) A new reading. *Then:* each row gets a second row with the new unit (D-0168), and the engine must not count the pair twice; T-086 writes the second rows (and raises OQ-T086: what becomes of the stored row).
- **Recommendation (the author's, not a decision).** None given: T-061 leaves the branch unbuilt and names the follow-up under (a).
- **Answer in one line.** `OD-41: ratio to rise:run ratio is a reformat` · `OD-41: ratio to rise:run ratio is a new reading (a second row)`
- **Tasks blocked until answered.** None now: resolved under delegation (status above); T-093, then T-086 (open on their gates and their merge order). At registration: T-086 (the bare-`ratio` rows); the follow-up branch to T-061
- **Where the evidence is.** `tasks/T-061-amend-extraction-reformat.md` section 4, "Not built here"

### OD-42  Is a figure converted between metric units rounded, or shown exactly?

- **Status (2026-11-13): RESOLVED UNDER DELEGATION 2026-11-13, check confirmed with corrections applied** — `OD-42 CHECK: confirmed with corrections applied`. Not the owner's words; reversible by the owner; resolved under the owner's twelfth instruction of 2026-11-12, applied at the owner's question of 2026-11-13, and checked under condition (d) by a second, independent Opus-class instance, whose corrections are applied. It opens a task's gate only through that confirmed check line (the gate of section 13); a delegated resolution never opens a gate that needs the owner's words. Ledger: `grep -n -F "Delegated resolution 2026-11-13 — OD-42" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS-2.md`, section OD-42; check: `DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-42. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-030 (its metric-to-metric display), and through it T-033 and T-110.
- **Earlier status (2026-11-13, at registration): OPEN (not yet asked)** — raised by the authoring of the prior-workplan cluster (T-1b step 9, mapped to T-030); no ledger line exists, so its gate reads CLOSED. **Holds:** the matching part of T-030 (T-030's gate reads the whole bullet, so T-030 waits, and with it T-033 and T-110).
- **Question.** OD-22 (delegated) shows a converted figure at the nearest quarter inch or 5 mm that does not fall on the wrong side of the source's bound (`grep -n -F 'nearest quarter inch or 5 mm' workplan/2026-11-12-bidirectional-pipeline/tasks/T-030-units-as-data.md`). A conversion from inches is inexact; one between metric units (cm to mm, m to mm) is exact. Parameter 12's governing claims are stated in cm, m and mm (T-030 section 3's expected output). Is a figure converted between metric units rounded to 5 mm like one converted from inches, or shown exactly?
- **Why it is the owner's.** A rounding rule changes published values (OD-22's own ground), and OD-22's resolution did not distinguish an exact conversion from an inexact one.
- **Options and what follows from each.**
  - (a) Rounded to 5 mm on the safe side, as from inches. *Then:* one display rule for every conversion; an exact metric value off the 5 mm step (a minimum of 122.2 cm, exactly 1222 mm) is shown at the next safe step (1225 mm), a figure the source did not state.
  - (b) Shown exactly. *Then:* the 5 mm rule applies only where the conversion is inexact; T-030's converter distinguishes exact from inexact factors.
- **Recommendation (the author's, not a decision).** None given.
- **Answer in one line.** `OD-42: a metric-to-metric conversion is rounded to 5 mm on the safe side` · `OD-42: a metric-to-metric conversion is shown exactly`
- **Tasks blocked until answered.** None now: resolved under delegation (status above); T-030 (open on its gates), and through it T-033 and T-110. At registration: T-030 (its metric-to-metric display); through it T-033 and T-110
- **Where the evidence is.** `tasks/T-030-units-as-data.md` sections 2 and 3; `grep -n -F "Delegated resolution 2026-11-12 — OD-22" references/project-standards.md`

### OD-43  When may the engine call a cell `convergent`?

- **Status (2026-11-14): ANSWERED BY THE OWNER** — `OD-43: agreement between any two kinds of evidence counts as convergence; convergence defines most common practice, which is not best practice`. The owner's words (answer 1 of the thirteenth set): "yes convergence is possible too, and it helps define most common practice (which isn't same as best practice)". The delegated limit to the clinical and Co-1 axes is superseded on contact; the remaining conditions (same value or range, anchoring claims that can all hold, two or more independent roots) stand as the recorder's [ASSUMPTION]; a convergence output is most common practice and is never labelled or rendered as best practice. Ledger: `grep -n -F "Owner answers 2026-11-14 (thirteenth set)" references/project-standards.md`. **Blocks now:** nothing (T-068 still waits for T-059 to merge). **Read by:** T-068 (its "Owner decisions" bullet); the render note in T-037 and T-032. **Refined the same day (2026-11-14) by the owner's statements** (ledger: `grep -n -F "Owner statement 2026-11-14 — convergence means values coming together" references/project-standards.md`; the answer line stands, no new status line): convergence means values coming together, among any sources and across any tiers, codes alone included; the root count is shown beside every convergence, not required for it (the "two or more independent roots" condition above is withdrawn); significance is read from the converging sources' tiers and bands, never as a score; convergence is most common practice and moves no value or marker; two or more clusters on different values are divergence between sets and a cue to investigate; a 5% working tolerance and ranges as the general case. Folded into T-068; the diagnostics reader is owed (`OPEN-ITEMS-PLAN.md` OI-57 (36)).
- **Earlier status (2026-11-13): RESOLVED UNDER DELEGATION 2026-11-13, check confirmed with corrections applied** — `OD-43 CHECK: confirmed with corrections applied`. Not the owner's words; reversible by the owner; resolved under the owner's twelfth instruction of 2026-11-12, applied at the owner's question of 2026-11-13, and checked under condition (d) by a second, independent Opus-class instance, whose corrections are applied. It opens a task's gate only through that confirmed check line (the gate of section 13); a delegated resolution never opens a gate that needs the owner's words. Ledger: `grep -n -F "Delegated resolution 2026-11-13 — OD-43" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS-2.md`, section OD-43; check: `DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-43. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-068.
- **Earlier status (2026-11-13, at registration): OPEN (not yet asked)** — raised by the authoring of T-068 (its Q-T068); no ledger line exists, so its gate reads CLOSED. **Holds:** T-068.
- **Question.** Today the engine never writes `convergent`: with two or more evidence axes it writes `pending_assessment`, because no rule "exists for grading agreement between extracted values" (`grep -n -F 'exists for grading agreement between extracted values' scripts/assess/assess_cell.py`). The ratified definition is "Tier 1–3 clinical evidence and Co-1 evidence agree on the parameter value or range" (`grep -n -F 'agree on the parameter value or range' governance/evidence-methodology.md`). After T-059 the engine knows whether the anchoring claims can all hold. When may it call a cell `convergent`?
- **Why it is the owner's.** It sets when the book tells a reader that the evidence agrees. OR-6b (`grep -n -F 'OR-6b: "No, the spread is printed in the note"' references/project-standards.md`) settles that differing satisfiable floors are not `divergent` and says nothing of `convergent`; the H1 doctrine settles that roots, not documents, are counted.
- **Options and what follows from each.**
  - (a) Two or more axes, anchoring claims that can all hold, and two or more independent roots among the governing figures. *Then:* the engine writes `convergent` on those cells (the 2026-10-22 report's T-8 step 2), `pending_assessment` otherwise; T-068 as written.
  - (b) As (a), but only when the axes state the same bound. *Then:* differing floors that can all be met stay `pending_assessment`.
  - (c) The engine never writes it; an Opus-class synthesis session grades it, and the validator checks the root condition only. *Then:* T-068's item 3 is dropped and items 1, 2 and 4 stand; the coordinator says so in T-068 before it is executed.
- **Recommendation (the author's, not a decision).** None given.
- **Answer in one line.** `OD-43: convergent on two or more axes, satisfiable anchors and two or more independent roots` · `OD-43: as that, and only when the axes state the same bound` · `OD-43: the engine never writes convergent; synthesis grades it`
- **Tasks blocked until answered.** None now: answered by the owner 2026-11-14 (status above); T-068 (open on its gate; it still waits for T-059 to merge). Earlier: resolved under delegation 2026-11-13. At registration: T-068
- **Where the evidence is.** `tasks/T-068-convergent-counts-roots.md` sections 2 and 3

### OD-44  Which second source for the blind double extraction?

- **Status (2026-11-14): ANSWERED BY THE OWNER** — `OD-44: A`. The owner's words (answer 2 of the thirteenth set, to the sheet's item 2, which asked for an answer to question 1): "apply recommendations", read by the recorder as the sheet's printed recommendation, option (a) (an [ASSUMPTION]). The source is the one T-070 section 3's query prints for the corpus-wide T1 or T2 source with the most findings (REF-01033 on 2026-11-14; re-run it), retrieved first. Ledger: `grep -n -F "Owner answers 2026-11-14 (thirteenth set)" references/project-standards.md`. **Blocks now:** nothing in the register; T-070 still needs the owner to launch the rater sessions.
- **Earlier status (2026-11-13): REFERRED BACK TO THE OWNER** — the second delegated pass (2026-11-13) referred it, and the independent check upheld the referral (`DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-44). Ledger: `grep -n -F "Referral 2026-11-13 — OD-44" references/project-standards.md`. The question in plain words was `OWNER-SHEET-PLAIN.md`, question 1 (removed once answered).
- **Earlier status (2026-11-13, at registration): OPEN (not yet asked)** — raised by the authoring of T-070 (its Q-T070); no ledger line exists, so its gate reads CLOSED. **Holds:** T-070 (which also needs the owner to launch the rater sessions).
- **Question.** OR-15 answered "Yes, use batch 23's material" to a prompt that described it as "one code with a step table and one T1 paper with findings" (`grep -n -F 'one code with a step table and one T1 paper with findings' governance/owner-browser.yaml`). That premise is false: batch 23 admitted no T1 or T2 source (T-070 section 3's command prints its tiers). The second source exists because "a code converges trivially". Which source is the second test?
- **Why it is the owner's.** OR-15 is the owner's answer to a prompt whose premise does not hold; choosing a substitute is reading the owner's intent.
- **Options and what follows from each.**
  - (a) The corpus-wide T1 or T2 source with the most `finding` rows (not batch 23's). *Then:* the T1 test is kept, but that source has no saved text, so it must be retrieved first (R10) before raters can read it.
  - (b) Batch 23's national framework with the most rows. *Then:* the material stays batch 23's and its text is derivable now; the T1 test is lost.
  - (c) The owner names the source. *Then:* T-070 uses it.
- **Recommendation (the author's, not a decision).** None given.
- **Answer in one line.** `OD-44: the corpus-wide T1 or T2 source with the most findings, retrieved first` · `OD-44: batch 23's national framework` · `OD-44: <ref_id>`
- **Tasks blocked until answered.** None now: answered by the owner 2026-11-14 (status above). At registration: T-070
- **Where the evidence is.** `tasks/T-070-blind-double-extraction.md` sections 2 and 3

### OD-45  A logged search whose request never returned results

- **Status (2026-11-13): RESOLVED UNDER DELEGATION 2026-11-13, check confirmed with corrections applied** — `OD-45 CHECK: confirmed with corrections applied`. Not the owner's words; reversible by the owner; resolved under the owner's twelfth instruction of 2026-11-12, applied at the owner's question of 2026-11-13, and checked under condition (d) by a second, independent Opus-class instance, whose corrections are applied. It opens a task's gate only through that confirmed check line (the gate of section 13); a delegated resolution never opens a gate that needs the owner's words. Ledger: `grep -n -F "Delegated resolution 2026-11-13 — OD-45" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS-2.md`, section OD-45; check: `DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-45. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-080 and T-081.
- **Earlier status (2026-11-13, at registration): OPEN (not yet asked)** — raised by the authoring of T-080; no ledger line exists, so its gate reads CLOSED. **Holds:** T-080 and T-081.
- **Question.** A logged search whose request never returned a result list (a publisher 403 or bot challenge, a 429, a connection reset): which is it? R14 asks a zero-yield search to "say query-shape failure vs wrong index vs genuine absence" (`grep -n -A8 'id: R14' governance/research-contract.yaml`), and the column's CHECK holds those three causes (`python3 -I -c "import sqlite3;s=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select sql from sqlite_master where name='search_executions'\").fetchone()[0];i=s.find('absence_class');print(s[i:i+130])"`); the operative instrument says `deferred_reason` "is for searches *not run*, never a findings channel" (`grep -n -F 'is for searches *not run*' decisions/DR-2026-08-19-research-restart-operative-instrument.md`). Several live zero-result searches call themselves a retrieval failure in their notes (T-080 section 3's command prints them).
- **Why it is the owner's.** It decides what the book may say about absence of evidence, and R14 and the operative instrument are the owner's rules.
- **Options and what follows from each.**
  - (a) A zero-result search under one of R14's three causes (the owner says which). *Then:* T-080 builds the writer refusal on the three; T-081 classifies the stored rows under them.
  - (b) A zero-result search under a fourth cause, `retrieval_failure`, added to the column's CHECK. *Then:* T-080 widens the CHECK by migration; T-081 classifies those rows under it.
  - (c) A search not run, recorded with `deferred_reason` and owed a re-run. *Then:* T-080's refusal tells a request that returned no result list to log with `--deferred-reason`; T-081 records those stored rows as deferrals owed a re-run.
- **Recommendation (the author's, not a decision).** None given.
- **Answer in one line.** `OD-45: a zero-result search, cause <query_shape_failure|wrong_index|genuine_absence>` · `OD-45: a zero-result search, cause retrieval_failure` · `OD-45: a search not run, deferred`
- **Tasks blocked until answered.** None now: resolved under delegation (status above); T-080 (open on its gate), then T-081. At registration: T-080, T-081
- **Where the evidence is.** `tasks/T-080-zero-result-search-states-its-cause.md` sections 2 and 3

### OD-46  The `lang_jur_map` codes missing from the jurisdiction registry

- **Status (2026-11-13): REFERRED BACK TO THE OWNER** — the second delegated pass (2026-11-13) referred it, and the independent check upheld the referral (`DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-46); its gate reads CLOSED until the owner answers. Ledger: `grep -n -F "Referral 2026-11-13 — OD-46" references/project-standards.md`. **The question in plain words:** `OWNER-SHEET-PLAIN.md`, question 2.
- **Earlier status (2026-11-13, at registration): OPEN (not yet asked)** — this is OI-55 (4) of `OPEN-ITEMS-PLAN.md`, registered under this number; no ledger line exists, so its gate reads CLOSED. **Holds:** T-084, and through it T-085.
- **Question.** The map of languages researched per jurisdiction names jurisdiction codes the registry has never declared (count them, and the pairs they hold: `python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('select count(distinct l.jurisdiction), count(*) from lang_jur_map l left join base_jurisdictions b on b.jurisdiction_code=l.jurisdiction where b.jurisdiction_code is null').fetchone())"`; T-084 section 3 lists them). Are they admitted to the registry as declared out-of-scope codes, or are their pairs removed?
- **Why it is the owner's.** Jurisdiction scope is doctrine (CLAUDE.md §8), and T-024 records that admitting such a code "is the owner's decision on scope" (`grep -n -F "is the owner's decision on scope" workplan/2026-11-12-bidirectional-pipeline/tasks/T-024-jurisdiction-registry.md`).
- **Options and what follows from each.**
  - (a) Admit them as declared codes, scoped out. *Then:* T-084 adds each with `add-jurisdiction` (kind and pair scope as the answer gives them, the pairs through `set-pair-scope`); T-085 then adds the foreign key.
  - (b) Remove their pairs. *Then:* there is no sanctioned delete, and under "retire in place then" (`grep -n -F 'retire in place then' references/project-standards.md`) a removal is an owner exception case by case, which needs a tooling task first; T-084 and T-085 wait for it.
- **Recommendation (the author's, not a decision).** None given.
- **Answer in one line.** `OD-46: admit them as declared, scoped-out codes` · `OD-46: remove their pairs (an exception to retire in place)`
- **Tasks blocked until answered.** T-084; through it T-085
- **Where the evidence is.** `tasks/T-084-unregistered-map-codes.md` sections 2 and 3; `tasks/T-024-jurisdiction-registry.md` section 9

**OD-47 to OD-54 are the owner questions AQ-1 to AQ-8 of the Edmonton case study's adjudication** (`scratchpad/session_2026-11-13-edmonton-checklist-pass/ADJUDICATION.md` section 5.3), registered 2026-11-13 by its fold in that order (AQ-1 is OD-47, … AQ-8 is OD-54); **OD-55** is OQ-T086 of `tasks/T-086-bare-ratio-rows.md`. The owner's own words that raised them are in the ledger (`grep -n -F 'Owner statements 2026-11-13 (eleventh set)' references/project-standards.md`). None carries a recommendation: the adjudicator gave none, and none of these is the plan's to settle.

### OD-47  What lens does a figure carry when its clause names no person, function or need?

- **Status (2026-11-13): REFERRED BACK TO THE OWNER** — the second delegated pass (2026-11-13) referred it, and the independent check upheld the referral (`DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-47); its gate reads CLOSED until the owner answers. Ledger: `grep -n -F "Referral 2026-11-13 — OD-47" references/project-standards.md`. **The question in plain words:** `OWNER-SHEET-PLAIN.md`, question 3.
- **Earlier status (2026-11-13, at registration): OPEN (not yet asked)** — the adjudication's AQ-1; no ledger line exists, so its gate reads CLOSED. **Holds:** the part of T-087 that writes figures whose clause names no one (they are parked as exact argv lines with one gap, not written); no task's gate. **Bears on:** T-115 step 3 (it cannot retire `ALL` while such a row keeps its `ALL` link) and T-106 (it leaves such figures as they are); both proceed without it, and say so in a bullet of their own.
- **Question.** OD-31 rules that a provision under a general disability heading carries "no identity, only its ICF and access-need lenses" (`grep -n -F 'OD-31: a provision that names no one' references/project-standards.md`), and D-0182 requires at least one lens. The lens writer accepts a link only on words found in the clause, the heading or the study's participants (`grep -n 'def _require_lens_warrant' -A12 scripts/db.py`). A clause such as "Corridors should be 1100mm" names no one and no function. What lens does it carry?
- **Why it is the owner's.** It decides who a figure is said to be for: the population taxonomy and the lens key.
- **Options and what follows from each.**
  - (a) The judge assigns ICF and need codes from the function the *parameter* serves, with the parameter's definition as the warrant. *Then:* every such figure can be written; the crossing is a property of the parameter, so by rule 5 it is held once on the parameter and derived for figures, which is a schema change.
  - (b) The document's own stated audience is the warrant (in the Edmonton checklist: "people with low vision, people who use different mobility devices"). *Then:* every item of a document carries the same groups, including items that do not concern them.
  - (c) The figure is not written until a clause names someone; the phrase stays an observation and a gap is filed. *Then:* checklists and most code clauses contribute observations only.
  - (d) It keeps `ALL` until re-tagged (T-115's present fallback). *Then:* T-115 step 3 stays blocked, as it already says.
- **Recommendation (the adjudicator's, not a decision).** None given.
- **Answer in one line.** `OD-47: function of the parameter` · `OD-47: the document's stated audience` · `OD-47: not written` · `OD-47: keeps ALL until you rule per row`
- **Tasks blocked until answered.** No task's gate; the parked figures of T-087, and T-115 step 3 for such rows
- **Where the evidence is.** `grep -n -F 'OD-31: a provision that names no one' references/project-standards.md`; `tasks/T-115-retag-all-rows.md` section 4 item 2; `grep -n 'def _require_lens_warrant' -A12 scripts/db.py`; ADJUDICATION Q6, R6 and section 4 F4

### OD-48  What does `design_scale = 'universal'` state?

- **Status (2026-11-13): REFERRED BACK TO THE OWNER** — the second delegated pass (2026-11-13) referred it, and the independent check upheld the referral (`DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-48); its gate reads CLOSED until the owner answers. Ledger: `grep -n -F "Referral 2026-11-13 — OD-48" references/project-standards.md`. **The question in plain words:** `OWNER-SHEET-PLAIN.md`, question 4.
- **Earlier status (2026-11-13, at registration): OPEN (not yet asked)** — the adjudication's AQ-2; no ledger line exists, so its gate reads CLOSED. **Holds:** T-056 (its item 3 and the engine change of item 3a; the adjudicator: "should be answered before T-056 executes"), and through it T-115.
- **Question.** The engine writes `universal` when a determination rests on codes alone (`grep -n 'design_scale = SCALE_UNIVERSAL' scripts/assess/assess_cell.py`). OD-31 says `ALL` leaves the identity lens, "universal being stated once, by design_scale". So a wheelchair-keyed cell built on codes reads `universal`, and the fact "rests on codes only" is already in `specifications.regulatory_stratum_only`. Which fact does the column state?
- **Why it is the owner's.** Design Modes are the ledger's first rule, and Universal Mode is defined there as both "Universal Design" and "Code Compliance" (`grep -n -F 'Universal Design / Code Compliance' references/project-standards.md`).
- **Options and what follows from each.**
  - (a) Whom it is for: `universal` when the determination names no identity. *Then:* "rests on codes only" is read from `regulatory_stratum_only`; the engine's G1 line changes; a code-only wheelchair cell reads `population` with its code marker by tier (○ for a T5 or T6 basis; ◐ for a T4-only basis, "T4 only half circle", once T-117 applies the table). *Superseded in part by TERM-RESOLUTION-PLAN section 1, U7 (2026-11-14): the option first said "with the ○ flag".*
  - (b) What it rests on: `universal` means code-only, as now. *Then:* OD-31's "universal" needs another home, and a figure for everyone is told apart only by having no identity.
  - (c) Both, as two columns. *Then:* a schema change; one already exists.
- **Recommendation (the adjudicator's, not a decision).** None given.
- **Answer in one line.** `OD-48: whom it is for` · `OD-48: what it rests on` · `OD-48: two columns`
- **Tasks blocked until answered.** T-056; through it T-115
- **Where the evidence is.** `grep -n 'design_scale = SCALE_UNIVERSAL' scripts/assess/assess_cell.py`; `grep -n -F 'Universal Design / Code Compliance' references/project-standards.md`; `grep -n -F 'OD-31: a provision that names no one' references/project-standards.md`; `tasks/T-056-all-leaves-identity-lens.md` section 4 items 3 and 3a

### OD-49  Building type, the other circumstances of a figure, and where an element lives

- **Status (2026-11-13): RESOLVED UNDER DELEGATION 2026-11-13, check confirmed with corrections applied** — `OD-49 CHECK: confirmed with corrections applied`. Not the owner's words; reversible by the owner; resolved under the owner's twelfth instruction of 2026-11-12, applied at the owner's question of 2026-11-13, and checked under condition (d) by a second, independent Opus-class instance, whose corrections are applied. It opens a task's gate only through that confirmed check line (the gate of section 13); a delegated resolution never opens a gate that needs the owner's words. Ledger: `grep -n -F "Delegated resolution 2026-11-13 — OD-49" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS-2.md`, section OD-49; check: `DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-49. **Blocks now:** nothing while its gate reads OPEN. **Read by:** T-091 (the typed carrier) and T-092 (the re-tag); T-060's design (where the element lives).
- **Scope narrowed (2026-11-14) by the owner's answer 3 of the thirteenth set** ("do not worry about existing/renovating and code as we are only concerned about design itself"; ledger: `grep -n -F "Owner answers 2026-11-14 (thirteenth set)" references/project-standards.md`): the guidebook concerns the design itself, so "new or existing work" leaves the circumstances a figure carries and no code-status circumstance is added; building use and interior or exterior remain; the headline measurement before any re-tag stands, counts only those two, and is shown to the owner. The status line is unchanged (RESOLVED UNDER DELEGATION); the narrowing is the recorder's [ASSUMPTION] of the owner's words.
- **Earlier status (2026-11-13, at registration): OPEN (not yet asked)** — the adjudication's AQ-3; no ledger line exists, so its gate reads CLOSED. **Holds:** T-091 (the typed carrier) and T-092 (the re-tag). **Bears on:** T-060's design (where the element lives), which reads the answer or points at the term.
- **Question.** (a) You ruled three building levels on 2026-08-27 ("Building types (eg residential, commercial), room types…, construction elements…"). None is linked to a figure; building use, new or existing, and interior or exterior sit together in a free-text cell the engine does not read. Is building type a branch within one determination, or part of what a determination is keyed on, and what is its vocabulary? (b) Is the construction-element level a table of its own, or the element terms the catalogue already holds?
- **Why it is the owner's.** Jurisdiction and scope vocabulary; the key of a determination, ruled twice; a prior ruling's ACTION ("Create three tables") that a later answer (OR-14, "a typed term pointer") may have overtaken.
- **Options and what follows from each.**
  - (a1) A typed circumstance on the figure, shown as a branch; a small project vocabulary seeded from your examples and extended by data with a warrant, each instrument's scope phrase adjudicated to it. *Then:* one determination per parameter and lens, with branches; "public" is adjudicated per instrument.
  - (a2) Part of the key. *Then:* one determination per building type; the key ruled on 2026-08-26 and 2026-08-28 changes.
  - (a3) Leave it in `setting`. *Then:* dwelling and public-building figures compose into one headline; T-091 and T-092 are declined.
  - (b1) Elements are terms; `base_building`'s third level is derived from them. *Then:* one home; the 2026-08-27 ACTION is amended for that level.
  - (b2) A separate `base_elements` table. *Then:* each element exists as a term and as a row, and one must point at the other.
- **Recommendation (the adjudicator's, not a decision).** None given.
- **Answer in one line.** `OD-49: (a1|a2|a3); (b1|b2)`
- **Tasks blocked until answered.** None now: resolved under delegation (status above); T-091 (open on its gate; its design file still owed), then T-092. At registration: T-091, T-092
- **Where the evidence is.** `grep -n -F 'base_building' references/project-standards.md | head -2` (the ruling and its ACTION); `grep -n -F 'Three tables with a typed' references/project-standards.md`; `grep -n -F '13. **OR-14.**' references/project-standards.md`; `grep -n -F 'OD-24: flat and coarse' references/project-standards.md`; `python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('select setting from source_value_extractions where parameter_id=9').fetchall())"`; `tasks/T-091-typed-circumstance-carrier.md` section 3

### OD-50  May a source that is not a code add a parameter?

- **Status (2026-11-13): RESOLVED UNDER DELEGATION 2026-11-13, check confirmed with corrections applied** — `OD-50 CHECK: confirmed with corrections applied`. Not the owner's words; reversible by the owner; resolved under the owner's twelfth instruction of 2026-11-12, applied at the owner's question of 2026-11-13, and checked under condition (d) by a second, independent Opus-class instance, whose corrections are applied. It opens a task's gate only through that confirmed check line (the gate of section 13); a delegated resolution never opens a gate that needs the owner's words. Ledger: `grep -n -F "Delegated resolution 2026-11-13 — OD-50" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS-2.md`, section OD-50; check: `DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-50. **Blocks now:** nothing while its gate reads OPEN. **Read by:** no task's gate; T-087 (it may promote a quantity it states) and T-072.
- **Earlier status (2026-11-13, at registration): OPEN (not yet asked)** — the adjudication's AQ-4; no ledger line exists, so its gate reads CLOSED. **Holds:** nothing (T-087 promotes no parameter while it is open). **Bears on:** T-072 (its subject is the held codes, OR-13, so it proceeds whatever the answer) and T-087.
- **Question.** You ruled that the list of quantities is seeded "From the codes held" (OR-13). REF-01037, a grey checklist, states figures for quantities no held parameter takes (handrail height and diameter, stair rise and run, control heights, toilet height, knee space, door dwell time). May such a source promote a parameter, or only mint the term and wait for a code?
- **Why it is the owner's.** It decides what the guidebook's pages can ask about and on whose word.
- **Options and what follows from each.**
  - (a) Any admitted source may, in its data pull request, under OR-17's conditions and T-020's kind. *Then:* the catalogue grows with each reading; names come from whichever source was read first until a judge picks (OD-38).
  - (b) Term only; a parameter needs a held code or standard that states the quantity. *Then:* the terms wait on T-105 and T-072, and T-079's deferred-adjudication arm keeps them visible.
  - (c) Term only, promoted when two independent sources state it. *Then:* a recurrence rule to build and maintain.
- **Recommendation (the adjudicator's, not a decision).** None given.
- **Answer in one line.** `OD-50: any admitted source` · `OD-50: a code or standard must state it` · `OD-50: two independent sources`
- **Tasks blocked until answered.** None now: resolved under delegation (status above); no task blocked; T-087 and T-072 read it. At registration: No task blocked
- **Where the evidence is.** `grep -n -F 'OR-13: "From the codes held"' references/project-standards.md`; `grep -n -F 'seeded by an open-pass scan' references/project-standards.md`; `grep -n -F 'OR-17: "Yes, bulk, with me reading the PR' references/project-standards.md`; `tasks/T-072-seed-quantities-from-codes.md` section 4

### OD-51  Does a municipal accessibility advisory committee's own document carry Co-1 standing?

- **Status (2026-11-13): REFERRED BACK TO THE OWNER** — the second delegated pass (2026-11-13) referred it, and the independent check upheld the referral (`DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-51); its gate reads CLOSED until the owner answers. Ledger: `grep -n -F "Referral 2026-11-13 — OD-51" references/project-standards.md`. **The question in plain words:** `OWNER-SHEET-PLAIN.md`, question 5.
- **Earlier status (2026-11-13, at registration): OPEN (not yet asked)** — the adjudication's AQ-5; no ledger line exists, so its gate reads CLOSED. **Holds:** nothing; REF-01037 stays T3 grey meanwhile (T-087).
- **Question.** The payload does not state the committee's membership. If membership of disabled people can be shown from another retrieved source, is the committee's checklist Co-1, and what proof is required?
- **Why it is the owner's.** A tier, and the meaning of co-production (CLAUDE.md §6). It adjoins the open second edge of OR-5b (how a lived-experience publication with no reporting guideline is shown to be sound; `OPEN-ITEMS-PLAN.md` OI-51).
- **Options and what follows from each.**
  - (a) Never: an appointed advisory body is not a representative organisation. *Then:* such documents stay grey.
  - (b) Yes, when a retrieved source shows disabled members authored it, recorded as co-producers. *Then:* the source is re-graded on that retrieval, with its co-producers recorded as authors.
  - (c) Decided per source by the owner. *Then:* each such source waits for the owner.
- **Recommendation (the adjudicator's, not a decision).** None given.
- **Answer in one line.** `OD-51: never` · `OD-51: yes, on retrieved proof of authorship` · `OD-51: per source`
- **Tasks blocked until answered.** No task blocked
- **Where the evidence is.** `governance/tier-system.md` (the Co-1 row: `grep -n -F '| **Co-1** |' governance/tier-system.md`); `grep -n -F 'OR-5b STATUS' references/project-standards.md`; ADJUDICATION section 4, "The critic's two withheld questions"

### OD-52  "Barrier-free path of travel" as REF-01037 uses it

- **Status (2026-11-13): REFERRED BACK TO THE OWNER** — the second delegated pass (2026-11-13) referred it, and the independent check upheld the referral (`DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-52); its gate reads CLOSED until the owner answers. Ledger: `grep -n -F "Referral 2026-11-13 — OD-52" references/project-standards.md`. **The question in plain words:** `OWNER-SHEET-PLAIN.md`, question 6.
- **Earlier status (2026-11-13, at registration): OPEN (not yet asked)** — the adjudication's AQ-6; no ledger line exists, so its gate reads CLOSED. **Holds:** two observations of T-087 ("Barrier-free unobstructed path of travel" and "Barrier-free path of travel"), adjudicated `DEFERRED` with a rationale naming this question; no task's gate.
- **Question.** You approved the definition "A circulation route through a building that a person using a wheelchair or other mobility device can travel without barriers" (OT-2). REF-01037 uses the phrase for the route from parking to the entrance, outdoors, and attaches to it a provision for "colour contrast and distinctive patterns where there are changes in level". Do these two observations name the term you approved?
- **Why it is the owner's.** The term, its definition and its placement are the owner's words (OT-1, OT-2), and on 2026-10-29 (fifth) the owner separated it from a route "navigated by someone who is blind".
- **Options and what follows from each.**
  - (a) Yes; the scope note records the exterior use. *Then:* the observations are adjudicated to the term once it is minted.
  - (b) Yes for the route; the contrast provision is a separate figure for blind and low-vision people on the same route. *Then:* as (a), and the contrast provision is read again for its own lens.
  - (c) No; it names something wider, to be adjudicated like "accessible route". *Then:* the observations wait with observation 71's question.
- **Recommendation (the adjudicator's, not a decision).** None given.
- **Answer in one line.** `OD-52: names the term` · `OD-52: names the term; the contrast provision is separate` · `OD-52: names something wider`
- **Tasks blocked until answered.** No task's gate; two observations of T-087
- **Where the evidence is.** `grep -n -F 'OT-1: "Barrier-free path of travel.' references/project-standards.md`; `grep -n -F 'navigated by someone who is blind' references/project-standards.md`; `grep -n -F '**OT-2 — the term' references/project-standards.md`; `grep -n 'id: OT-2' -A12 governance/owner-browser.yaml`; the PDF's items 1.2 and 2.1 (`retrieval-log/session_2026-11-13-edmonton-checklist-pass/1a117aff4c5947a8-full-text.txt`)

### OD-53  Bulk declination in a single-source batch

- **Status (2026-11-13): RESOLVED UNDER DELEGATION 2026-11-13, check confirmed with corrections applied** — `OD-53 CHECK: confirmed with corrections applied`. Not the owner's words; reversible by the owner; resolved under the owner's twelfth instruction of 2026-11-12, applied at the owner's question of 2026-11-13, and checked under condition (d) by a second, independent Opus-class instance, whose corrections are applied. It opens a task's gate only through that confirmed check line (the gate of section 13); a delegated resolution never opens a gate that needs the owner's words. Ledger: `grep -n -F "Delegated resolution 2026-11-13 — OD-53" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS-2.md`, section OD-53; check: `DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-53. **Blocks now:** nothing while its gate reads OPEN. **Read by:** no task's gate; T-087 (its declinations) and T-072 item 6 (their review).
- **Scope overtaken in part (2026-11-14) by the owner's answer 4 of the thirteenth set** ("hearing loops and other similar provisions should be included"; ledger: `grep -n -F "Owner answers 2026-11-14 (thirteenth set)" references/project-standards.md`): a provision whose question is whether it is present (a hearing loop, a visual alarm, a tactile walking surface indicator, a TTY, tactile signage) is included in the book, so a research batch does not decline such a term as "not a measurement"; how it is included is OD-56 (answered by the owner later on 2026-11-14 as (b): the term is kept and reached by an element pointer, T-060; a declination of it as a parameter stays lawful only where that pointer is possible). OD-53 otherwise stands; its status line is unchanged (RESOLVED UNDER DELEGATION).
- **Earlier status (2026-11-13, at registration): OPEN (not yet asked)** — the adjudication's AQ-7; no ledger line exists, so its gate reads CLOSED. **Holds:** part of T-087, not its gate: the held terms that the checklist's phrases name. A phrase that truly names a held term is adjudicated `NAMES-EXISTING` to it (the settled reading); the research gate's R16 then requires every term named by an adjudication of a batch's observations to be a parameter or declined (`grep -n -F 'EVERY CONCEPT A SOURCE STATES A FIGURE FOR IS DISPOSED OF' scripts/audit/research_batch_dod.py`), most held terms are neither (`python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('select count(*), sum(not exists(select 1 from base_parameters p where p.term_id=t.term_id) and not exists(select 1 from parameter_declinations d where d.term_id=t.term_id and d.revoked_at is null)) from terms t').fetchone())"`), and the batch does not decline in bulk while this is open. So R16 stays **red** for those terms, the batch is reported NON-COMPLIANT on R16 pending this question, and its data pull request carries an explicit reasoned waiver (the gate's own instruction: `grep -n -F 'explicit reasoned waiver' scripts/audit/research_batch_dod.py`; the waiver text is T-087 section 11; the terms are listed by T-087 section 6's "R16 terms" query). **Corrected 2026-11-13 by the digest's third run:** this entry first said those observations are adjudicated `DEFERRED` instead, so that R16 stays green. That route is dishonest: `DEFERRED` means "cannot be settled on this source alone" (`select sql from sqlite_master where name='term_adjudications'`), those readings are settled, R16 reads only adjudications that name a term, and no gate reads a `DEFERRED` row, so it keeps R16 green by hiding the act (`scratchpad/session_2026-11-13-edmonton-checklist-pass/REPLAY-V3-BRIEF.md` F2; `DIGEST-REPORT.md` sections 4 and 11). `DEFERRED` stays for phrases genuinely unsettled on the source, for quantity concepts waiting on OD-50, and for elements or group phrases with no held term (its rationale saying it records a withheld act).
- **Question.** May a research batch decline held terms as parameters when a source merely mentions them, or is that T-072's (item 6) to do once, across the catalogue?
- **Why it is the owner's.** OR-17's bulk approval names phrases, names and aliases; E12 names functional-axis and method terms; neither names elements (`grep -n -F 'OR-17: "Yes, bulk, with me reading the PR' references/project-standards.md`; `grep -n -E '^\| E12 ' references/project-standards.md`).
- **Options and what follows from each.**
  - (a) Any batch may, with a reason per term. *Then:* the batch declines those terms itself (`decline-parameter`, one call and one reason per term: T-087 section 4 item 6 if answered before it ships, otherwise a later research batch), R16 turns green, and no adjudication changes.
  - (b) Only the catalogue-wide task. *Then:* T-087's data pull request ships with the R16 waiver, and the terms wait for T-072 item 6 to dispose of them; R16 turns green then, and no adjudication changes.
- **Recommendation (the adjudicator's, not a decision).** None given.
- **Answer in one line.** `OD-53: any batch` · `OD-53: the catalogue task only`
- **Tasks blocked until answered.** None now: resolved under delegation (status above); no task blocked; T-087 and T-072 read it. At registration: No task's gate; the disposal of the held terms T-087's `NAMES-EXISTING` adjudications name (R16 red, waived in its pull request)
- **Where the evidence is.** ADJUDICATION section 3 item 7; `tasks/T-087-edmonton-checklist-batch.md` sections 2, 4 items 3 and 6, 6 and 11; `tasks/T-072-seed-quantities-from-codes.md` section 4 item 6

### OD-54  When a writer cannot hold content, may an agent write the canonical row by hand?

- **Status (2026-11-13): REFERRED BACK TO THE OWNER** — the second delegated pass (2026-11-13) referred it, and the independent check upheld the referral (`DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-54); its gate reads CLOSED until the owner answers. Ledger: `grep -n -F "Referral 2026-11-13 — OD-54" references/project-standards.md`. **The question in plain words:** `OWNER-SHEET-PLAIN.md`, question 7.
- **Earlier status (2026-11-13, at registration): OPEN (not yet asked)** — the adjudication's AQ-8; no ledger line exists, so its gate reads CLOSED. **Holds:** nothing in the plan. T-088 and T-089 build the register reading only (the content waits in the register and is replayed through the writer); no task builds a path that writes a canonical row by hand, so there is no part for this decision to hold. Under answer (b) a task would be authored then.
- **Question.** You proposed a register of what the pipeline could not execute, "alongside having an agent fix it by hand with correct context so we aren't losing content". Does "by hand" mean the agent writes the intended row and a proposed amendment into the register, to be replayed through the writer once it is fixed, or writes the row into the database directly?
- **Why it is the owner's.** The second reading sets aside CLAUDE.md rules 3 and 10, which only a live owner statement can do.
- **Options and what follows from each.**
  - (a) Into the register; replay later. *Then:* no content is lost, the batch is not held up, and every canonical row has still passed a writer's refusals.
  - (b) Into the database, flagged, with the register entry beside it. *Then:* the content is usable at once; a hand-written row bypasses the refusals that exist to stop a mis-typed or invented value, and rules 3 and 10 gain a stated exception with its limits to be written.
- **Recommendation (the adjudicator's, not a decision).** None given.
- **Answer in one line.** `OD-54: into the register, replayed through the writer` · `OD-54: into the database, flagged, within these limits: <…>`
- **Tasks blocked until answered.** No task blocked
- **Where the evidence is.** CLAUDE.md rules 3 and 10 and §4; ADJUDICATION Q10; `tasks/T-088-refusal-capture-and-disposition.md` section 4a

### OD-55  After a second reading of a bare-`ratio` gradient, is the stored row retired?

- **Status (2026-11-13): RESOLVED UNDER DELEGATION 2026-11-13, check confirmed with corrections applied** — `OD-55 CHECK: confirmed with corrections applied`. Not the owner's words; reversible by the owner; resolved under the owner's twelfth instruction of 2026-11-12, applied at the owner's question of 2026-11-13, and checked under condition (d) by a second, independent Opus-class instance, whose corrections are applied. It opens a task's gate only through that confirmed check line (the gate of section 13); a delegated resolution never opens a gate that needs the owner's words. Ledger: `grep -n -F "Delegated resolution 2026-11-13 — OD-55" references/project-standards.md`; reasoning: `DELEGATED-RESOLUTIONS-2.md`, section OD-55; check: `DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-55. **Blocks now:** nothing while its gate reads OPEN. **Read by:** nothing while OD-41 stands as a reformat.
- **Earlier status (2026-11-13, at registration): OPEN (not yet asked)** — OQ-T086 of `tasks/T-086-bare-ratio-rows.md`, registered by the fold of 2026-11-13; no ledger line exists, so its gate reads CLOSED. **Holds:** nothing while OD-41 is unanswered or answered (a). Under OD-41 (b) it bears on T-086 section 4 item 2, which writes the second rows and retires nothing until it is answered; not T-086's gate.
- **Question.** Under OD-41 (b), each stored row whose unit is the bare word `ratio` gets a second row reading `rise:run ratio` (D-0168). The stored row stays and the engine still cannot read it, but the cell's value note counts governing claims, and would count both. Is the stored row retired in place (T-078 builds that verb) once its second reading is written, or are both rows left?
- **Why it is the owner's.** OD-41 (b) as registered does not say, and retiring a figure the owner allowed to stand under D-0168 is a reading of the owner's rule.
- **Options and what follows from each.**
  - (a) Retire the stored row in place under T-078, with its successor named. *Then:* T-086 depends on T-078 for that step, and the note counts one claim per pair.
  - (b) Leave both rows. *Then:* the note counts both, and the engine must not count the pair twice (a correction owed to the engine, filed as a gap).
- **Recommendation (the author's, not a decision).** None given.
- **Answer in one line.** `OD-55: retire the stored row in place once its second reading is written` · `OD-55: leave both rows`
- **Tasks blocked until answered.** None now: resolved under delegation (status above); no task blocked (conditional on OD-41). At registration: No task blocked (part of T-086 under OD-41 (b))
- **Where the evidence is.** `tasks/T-086-bare-ratio-rows.md` sections 2 and 4 item 2; `tasks/T-078-figure-retires-in-place.md`

### OD-56  How is a provision whose question is whether it is present included in the book?

- **Status (2026-11-14): ANSWERED BY THE OWNER** (later the same day; the date in brackets is kept bare so that D-36's count reads it) — `OD-56: (b) an element-level determination lists the provisions an element should carry; a provision is not a parameter` (ledger: `grep -n -F "Owner answer 2026-11-14 — OD-56" references/project-standards.md`; gate: `grep -F "OD-56 STATUS:" references/project-standards.md | tail -1`). The owner wrote "b" in reply to the four options below; the reading as option (b) is the recorder's [ASSUMPTION], told to the owner and not corrected. A provision of presence is not a parameter and no value is computed for it; T-060's element determination points at the provision terms the element should carry, at the source statements that say it should, and at its parameters' determinations and crossing relation rows, and holds no value column; T-029 carries the `element has provision` pointer kind. **No delegated resolution is needed** and none is run; options (a), (c) and (d) are not taken. How a source's statement "a hearing loop should be provided" is typed is for T-060's design file and T-029's kinds. **Holds:** T-060 and T-029 carry it (ACTION (1) and (2) of the ledger entry); T-072 item 6 and T-087 do not decline a provision term without its pointer being possible.
- **Earlier status, kept as history (2026-11-14): OPEN (not yet resolved)** — registered 2026-11-14 on the owner's answer 4 of the thirteenth set ("hearing loops and other similar provisions should be included"; ledger: `grep -n -F "Owner answers 2026-11-14 (thirteenth set)" references/project-standards.md`). The owner has ruled inclusion; this decision is the mechanism. No ledger status line exists, so its gate reads CLOSED. **For a delegated Opus-class resolution** under the owner's twelfth instruction of 2026-11-12 ("You have permission to use Opus for judgment if appropriate here"), as applied at the owner's question of 2026-11-13 (`grep -n -F "Owner question 2026-11-13 — may the open decisions OD-40 to OD-55" references/project-standards.md`), with the delegation's conditions (a) to (e), judged against the owner's three criteria in the order ratified by OI-14, and **checked by a second, independent Opus-class instance before any task relies on it**. If the resolver finds that an option sets the population taxonomy, an evidence-tier definition or another always-DG-NON matter, it refers that part back to the owner. **Holds:** no task yet (the option chosen names the task); meanwhile no research batch declines such a term (OD-53's scope note above).
- **Question.** How is a provision whose question is whether it is present (a hearing loop, a visual alarm, a tactile walking surface indicator, a TTY, tactile signage) included in the book, with a determination or a mark of its own?
- **Why it is the owner's, and why it may be delegated.** The owner ruled that such provisions are included (answer 4); how is machinery, which the owner said on 2026-11-13 they cannot judge ("I don't know the machinery or code"). The book today determines only a quantity under determination: the determination is keyed on "the design parameter under determination" (`grep -n -F 'The determination is keyed on the design parameter under determination' references/project-standards.md`), a parameter is one measured quantity with a kind (OD-24: `grep -n -F 'OD-24: flat and coarse' references/project-standards.md`), and the kinds seeded are length, gradient, force, time, luminous reflectance and its contrast, and colour temperature (T-020 section 4 item 1), none of which is presence. The held terms for such provisions: `python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select term_id, canonical_en, domain from terms where domain in ('acoustic','communication','fire_safety','wayfinding') order by 1\").fetchall())"` (a sample of where such terms sit, not the vocabulary: read `domain`'s CHECK for that).
- **Options and what follows from each.**
  - (a) A quantity kind of presence (provided or not provided, or a count of provisions), added by data with a warrant (T-020's `add-quantity-kind`; OD-24 allows a kind to be "extended by data with a warrant"), so such a provision becomes a parameter with its own determination, lens, marker and branches. *Then:* the engine, its anchoring and agreement rules (T-059, T-068), the floor and above-floor derivation, and render's sentences meet a value that has two states and no direction of more or less accommodating on a scale; the resolver says how a direction (`base_parameters.accessibility_direction`), a bound and "best practice is the most accommodating value" read for it, or the option fails criterion 1. A count of provisions (for example one visual alarm per room) is a quantity and already fits the model; presence alone is the hard case. T-010 plans one rule of refused domains (`NON_QUANTITY_DOMAINS`, T-010 section 4 item 1: lenses, methods and bodies of law); the domains the held provision terms sit in are not among them, which the resolver confirms on the merged code.
  - (b) An element-level determination (T-060, OR-14b "written by the pass") that lists the provisions an element or a room should carry. *Then:* the provision gets its mark only inside an element's page; OR-14b's constraint holds that an element row holds pointers and no value of its own (`grep -n -F 'The element is still never a container that figures are filed into' references/project-standards.md`), so a list of provisions is either a pointer to rows that must exist somewhere (back to (a) or (c)) or a value the element would hold (which that constraint forbids); a provision not tied to one element (a TTY at a service counter, a building's alarm system) has no home; T-060 has no design file yet.
  - (c) A separate typed register of provisions, with its own determination and marker (a table of its own: the provision term, the lens set, the sources that call for it, and a mark). *Then:* a new stage output and its writer, refusals, render template and stage-map entry, built in a tooling pull request (rule 10); its marker needs a rule beside ●, ◐ and ○ or a reading of them for a present-or-absent call; the owner's "one value per cell" and rule 5 decide whether it duplicates any parameter; T-029's typed term pointers connect it to elements and parameters.
  - (d) Leave such provisions as terms, rendered in prose only. *Then:* nothing is built; **the owner's answer 4 rejects this** ("should be included", against the offer "discussed but get no value"), so it is listed only to be declined.
- **Recommendation.** None given here; the resolver weighs the options against the three criteria and the standing rulings, and writes a reversal condition.
- **Answer in one line.** `OD-56: a quantity kind of presence` · `OD-56: an element-level list` · `OD-56: a typed register of provisions` · `OD-56: <other>`
- **Tasks blocked until answered.** None now: answered by the owner (status above); the mechanism is built by T-060 and T-029. At registration: None yet; the resolution names the task that builds the mechanism, and a research batch keeps such terms undeclined until then.
- **Where the evidence is.** The ledger's thirteenth set (above); `OWNER-SHEET-PLAIN.md` item 4 as it was put; the OD-53 independent check (`DELEGATED-RESOLUTIONS-2-REVIEW.md`, OD-53); `tasks/T-020-quantity-kind.md` section 4; `tasks/T-060-element-determination.md` sections 3 and 4; `tasks/T-029-term-relations.md`; `tasks/T-010-add-parameter-domain-refusal.md` section 4 item 1.

**OD-57 to OD-62 are the term-resolution plan's Q1 to Q6** (`TERM-RESOLUTION-PLAN.md` section 6), registered 2026-11-14 by its fold in that order (Q1 is OD-57, … Q6 is OD-62) and referred to the owner (ledger: `grep -n -F "## Registration 2026-11-14" references/project-standards.md`). **None is to be resolved under delegation:** Q1, Q2 and Q3 reach the evidence-tier definitions (always DG-NON: `grep -n -F 'Evidence-tier definitions' governance/decision-protocol.md`), Q4 is the owner's voice, Q5 is gated by the owner's cold-storage record, Q6 is optional. Each recommendation is the unifier's, not a decision. **Resolved by default, not registered** (the plan's readings of the owner's "whatever doesn't matter", [ASSUMPTION]): no aliases after a rename; the verb "states the ideal and grades its evidence"; the stage stays "specification".

### OD-57  Apply the circle table now?

- **Status (2026-11-14): REFERRED BACK TO THE OWNER** — registered from the term-resolution plan's Q1; its gate reads CLOSED until the owner answers. **The question in plain words:** `OWNER-SHEET-PLAIN.md`, question 8. **Holds:** T-117 (and T-118 after it).
- **Question.** The owner's entries of 2026-11-14 built a table: ● T1, T2, Co-1, Co-2; ◐ T3, T4 ("T4 only half circle"); ○ T5, T6; ⚠ (U+26A0) in place of the circle for a grey, unverified or thin basis. Each entry holds its application ("keep `band()` as it is until the owner rules"). Apply it now, including lowering T3 clinical from ● to ◐, raising T3 grey from ○ to ◐, lowering T5 from ◐ to ○, and replacing the ○ gloss "grey, thin or unverified" in `CLAUDE.md` §6?
- **Why it is the owner's.** It changes how every evidence tier is marked: an evidence-tier definition (decision protocol §2.4 item 3), held by the owner's own entries.
- **Options and what follows from each.**
  - (a) Apply it now. *Then:* T-117 builds it (`band()`, the regulatory-only override deleted, CHECK 116 relaxed and widened to ⚠, the W prose rows); T4-only cells rise to ◐, T3 clinical cells fall to ◐, T5 cells fall to ○.
  - (b) Apply it except one row (name it). *Then:* T-117 builds the rest.
  - (c) Not yet. *Then:* T-117 waits; the book keeps the present markers.
- **Recommendation (the unifier's, not a decision).** (a): every tier is answered, and `governance/evidence-methodology.md` §2.2 already holds T3 clinical at `provisional`.
- **Answer in one line.** `OD-57: apply` · `OD-57: apply except <row>` · `OD-57: not yet`
- **Tasks blocked until answered.** T-117; through it T-118
- **Where the evidence is.** `sed -n '/^def band(/,/^def floor_mean/p' schemas/tier_derivation.py`; `grep -n -E '^## Owner (proposal|statement|answer|correction) 2026-11-14 \(last\) — .*(circle|triangle|glyph|thin|tier 4|Co-1 and Co-2|grey)' references/project-standards.md`; `tasks/T-117-marker-table-applied.md`

### OD-58  What proves "worse results" under the harm test?

- **Status (2026-11-14): REFERRED BACK TO THE OWNER** — registered from the term-resolution plan's Q2; its gate reads CLOSED until the owner answers. **The question in plain words:** `OWNER-SHEET-PLAIN.md`, question 9. **Holds:** T-059 (item 6, selection across all tiers; the gate holds the task), and through it T-068, T-110, T-117, T-118.
- **Question.** The owner ruled: "does the research prove that the more accommodating value leads to worse results? if so, research wins. if no, code wins", and left the standard of proof open. What counts as proof that the more accommodating value leads to worse results?
- **Why it is the owner's.** It decides whether a tier gates which value is shown (an evidence-tier definition) and the standard of proof the owner's entry holds open.
- **Options and what follows from each.**
  - (a) A recorded finding (`source_value_extractions.harm_finding`, or an `extraction_relations` row marking `insufficient`) from a source that measured or reported the outcome for the same lens and context, at any tier, shown with that source's marker; never a project inference. *Then:* T-059 item 6 builds it as written.
  - (b) As (a), but only from T1, T2, Co-1 or Co-2 sources. *Then:* a code or grey finding of harm is shown but never replaces the value.
  - (c) Any recorded finding, whatever its lens or context. *Then:* a finding about another group can displace a value for this one (the plan's risk 1).
- **Recommendation (the unifier's, not a decision).** (a): the tier grades the finding, it does not gate it, as the owner ruled for values.
- **Answer in one line.** `OD-58: a recorded finding, same lens and context, any tier` · `OD-58: only from T1, T2, Co-1 or Co-2` · `OD-58: <other>`
- **Tasks blocked until answered.** T-059; through it T-068, T-110, T-117, T-118
- **Where the evidence is.** `grep -n -F 'the most accommodating value stands unless research shows' references/project-standards.md`; `tasks/T-059-wp-t4-agreement.md` section 4 item 6; `TERM-RESOLUTION-PLAN.md` section 8 risks 1 and 2

### OD-59  Does a showcased value carry the grade of its own source, or of all governing sources?

- **Status (2026-11-14): REFERRED BACK TO THE OWNER** — registered from the term-resolution plan's Q3; its gate reads CLOSED until the owner answers. **The question in plain words:** `OWNER-SHEET-PLAIN.md`, question 10. **Holds:** T-117.
- **Question.** When a cell's governing sources differ in tier, the engine today marks the cell with the floor of the mean of all their bands (`floor_mean`), and the entry "T4 only half circle" read that as unchanged (an [ASSUMPTION]). Does the showcased value carry the grade of the source that states it, or that floor mean?
- **Why it is the owner's.** It sets what the marker of a determination says about its evidence (an evidence-tier definition applied); the owner's definition of determination includes "how to grade quality of evidence for it".
- **Options and what follows from each.**
  - (a) Its own source's grade; ⚠ only where that value's basis is grey, unverified or thin. *Then:* a T6 best beside T1 research reads ○ (its own); a T1 best beside T6 codes reads ●.
  - (b) The floor mean of every governing source, as now. *Then:* a T1 best beside T6 codes reads below ●.
- **Recommendation (the unifier's, not a decision).** (a): "how to grade quality of evidence for it" is about the chosen value.
- **Answer in one line.** `OD-59: its own` · `OD-59: the floor mean`
- **Tasks blocked until answered.** T-117
- **Where the evidence is.** `grep -n -A14 '^    marker = None' scripts/assess/assess_cell.py`; `grep -n -F 'what "determination" means' references/project-standards.md`; `tasks/T-117-marker-table-applied.md` section 4 item 3

### OD-60  Does the prose register's "to be + [value]" survive?

- **Status (2026-11-14): REFERRED BACK TO THE OWNER** — registered from the term-resolution plan's Q4; its gate reads CLOSED until the owner answers. **The question in plain words:** `OWNER-SHEET-PLAIN.md`, question 11. **Holds:** T-035 (only its voice line, item 5; the gate holds the task).
- **Question.** The prose register writes values in the soft subjunctive ("to be 1200 mm"). The owner ruled "we gather and show" and that the project does not claim authority over a design. Does "to be + [value]" stay?
- **Why it is the owner's.** The register is the book's voice; the tension is recorded in the plan's risk 7.
- **Options and what follows from each.**
  - (a) Keep it for process prose; state values as attributed data ("REF-… gives 1200 mm"). *Then:* T-035 rewrites the value lines only.
  - (b) Keep it everywhere. *Then:* T-035 leaves the voice line.
  - (c) Drop it. *Then:* T-035 rewrites the register.
- **Recommendation (the unifier's, not a decision).** (a).
- **Answer in one line.** `OD-60: process prose only; values as attributed data` · `OD-60: keep` · `OD-60: drop`
- **Tasks blocked until answered.** T-035
- **Where the evidence is.** `grep -n -i 'to be' skills/prose-style-checker_SKILL.md | head`; `grep -n -F 'we gather and show' references/project-standards.md`

### OD-61  Add `references/bpc/` to `.ignore`?

- **Status (2026-11-14): REFERRED BACK TO THE OWNER** — registered from the term-resolution plan's Q5; its gate reads CLOSED until the owner answers. **The question in plain words:** `OWNER-SHEET-PLAIN.md`, question 12. **Holds:** T-121.
- **Question.** The best-practices compendium (`references/bpc/`) is frozen and quarantined, and every search for "best practice" returns it first. Add it to `.ignore` (agent search only; git and the project's tooling still see it)?
- **Why it is the owner's.** `.ignore`'s scope is set by the owner's cold-storage record (`decisions/DR-2026-08-06-cold-storage-search-scope.md`).
- **Options and what follows from each.** (a) Yes. *Then:* T-121 adds one line and CLAUDE.md §7's list. (b) No. *Then:* T-121 is declined.
- **Recommendation (the unifier's, not a decision).** (a).
- **Answer in one line.** `OD-61: yes` · `OD-61: no`
- **Tasks blocked until answered.** T-121
- **Where the evidence is.** `grep -n -E '^references' .ignore`; `git grep -l -i 'best practice' -- references/bpc | wc -l`

### OD-62  Rename "best practice" to "ideal"? (optional)

- **Status (2026-11-14): REFERRED BACK TO THE OWNER** — registered from the term-resolution plan's Q6, which is optional: **if unanswered, the default stands (no rename)**. It holds no task and is listed as standing. **The question in plain words:** `OWNER-SHEET-PLAIN.md`, question 13.
- **Question.** The owner asked on 2026-11-14 whether "ideal" would serve, then ruled the meaning ("best practice IS the same as ideal IS the same as most accommodating"). Should the project write "ideal" in place of "best practice"?
- **Why it is the owner's.** The book's vocabulary; the owner asked it.
- **Options and what follows from each.** (a) No rename. *Then:* nothing is built; `v_best_practice` keeps its name. (b) Rename. *Then:* a migration and a caller sweep, folded into T-118.
- **Recommendation (the unifier's, not a decision).** (a): the meaning is fixed, and a rename costs a migration and a caller sweep.
- **Answer in one line.** `OD-62: no rename` · `OD-62: rename to ideal`
- **Tasks blocked until answered.** None
- **Where the evidence is.** `grep -n -F 'best practice IS the same as ideal' references/project-standards.md`; `tasks/T-118-stage-tools-carry-specification-name.md` section 2

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
| D-27 | every owner decision a task waits on is settled (owner's twelfth instruction: the plan is not complete while one stands open) | `gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md \| tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md \| tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*\|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }; for n in $({ grep -h -o -E 'for n in [^;]*;\|"OD-[0-9]+ STATUS:"' workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md; grep -h -E '^- \*\*Owner decisions' workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md \| grep -v -i -E '^- \*\*Owner decisions[^*]*\*\* *none'; } \| grep -o -E 'OD-[0-9]+' \| sort -u); do gate $n; done \| grep CLOSED` (the second source, added 2026-11-13, reads a decision a task's 'Owner decisions' bullet names without a gate command of its own, as the generator does) | the blocking decisions, one CLOSED line each; the same set as the generator's `blocking` list | no line |
| D-27b | every other register decision is answered, resolved under delegation with its gate OPEN, or deferred by the owner | `for n in $(grep -o -E '^### OD-[0-9]+' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md \| cut -c5-); do gate $n; done \| grep CLOSED \| grep -v -F 'DEFERRED BY THE OWNER'` (after defining `gate` as in D-27) | the standing decisions and the blocking ones | no line |
| D-36 | every register entry carries a status line, and no task names a decision the register lacks | `echo $(grep -c '^- \*\*Status (20[0-9-]*)' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md) $(grep -c '^### OD-' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md); python3 -I scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py \| grep -o "unregistered .*"` | two equal numbers; `unregistered []` | the same |
| D-31 | retire in place: no verb deletes an admission edge or a connection (T-050) | `grep -c -E "DELETE FROM (search_admissions\|connections\|connection_targets)" scripts/db.py` | not 0 | 0, and T-050's after-test green |
| D-32 | the gap register is cross-stage, and no path was lost (T-051) | `python3 -c "import yaml;print(yaml.safe_load(open('governance/stage-map.yaml'))['tables']['gaps'])"` | `synthesis` | `cross-stage`, and D-01's count no higher than before T-051 |
| D-33 | an out-of-scope mined source is staged, not admitted (T-052) | `grep -c -E 'OUT-OF-SCOPE\|outside the scope in force' skills/citation-miner_SKILL.md skills/gap-driven-mining_SKILL.md` | 0 for each | at least 1 for each |
| D-34 | sub-national instruments are filed under their own codes (T-113) | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select ref_id, jurisdiction from evidence_sources where ref_id in ('REF-00992','REF-00995','REF-01013','REF-01029')\").fetchall())"` | the country codes | each a sub-national code whose parent is the country |
| D-35 | conflict between groups: recorded (OD-19, T-032) and weighed by the approved ordering (OD-36, T-053) | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([r[1] for r in c.execute('pragma table_info(conflicts)')], c.execute(\"select count(*) from sqlite_master where name='harm_classes'\").fetchall())"`; then T-053's after-test | no judge, warrant or class columns; no `harm_classes` | judge and warrant columns (T-032); the five classes in order and T-053's after-tests (a) to (f) green |
| D-37 | `ALL` has left the identity lens; universal is stated only by `design_scale` (OD-31) | `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select status from base_taxonomy_identity where identity_code='ALL'\").fetchall(), c.execute(\"select count(*) from source_value_extractions where identity_code='ALL'\").fetchall())"`; `git grep -n -E "['\"]ALL['\"]" -- scripts/assess` | `[('active',)]` and a non-zero count; an engine branch | `[('deprecated',)]`, `[(0,)]`, no engine branch (T-056, T-115) |
| D-38 | disability coverage is visible at every research batch (the owner's 2026-11-13 instruction; T-090) | `grep -c -F 'COVERAGE' .claude/commands/batch-done.md` | 0 | 1 or more, and the three reads run as written; read by the owner at each research pull request and quoted by T-110 before the first live determinations |
| D-39 | no content is lost to a refusal: every writer refusal is kept and disposed (owner statements 1 to 5 of 2026-11-13; T-088, T-089) | `git grep -n 'def record_refusal' -- scripts/dbcore.py; python3 scripts/audit/refusal_register.py classes > "$SCRATCH/rr.txt" 2>&1; echo rc=$?; grep -E 'EXAMINED\|UNDISPOSED' "$SCRATCH/rr.txt" \| tail -3` | no function, no script | the function; `EXAMINED:` over every committed session's refusals, and no `UNDISPOSED` line from a merged batch |
| D-40 | the owner's meaning of best, most common and minimum has one ledger record, and the decision records that say otherwise are marked (T-119; TERM-RESOLUTION-PLAN §3) | `grep -c -F 'Unification 2026-11-14' references/project-standards.md; python3 scripts/audit/supersession_backpointer_audit.py 2>&1 \| grep -E 'EXAMINED\|FAIL' \| tail -2` | `0`; the audit's present `EXAMINED:` | `1`; PASS, with `EXAMINED:` higher by the pairs T-119 and T-117 add |
| D-41 | doctrine has one home for the figures of a cell, and names no table the schema lacks (T-120) | `grep -c -F '## 0.' governance/evidence-architecture.md; git grep -l -F 'best_practice_synthesis' -- CLAUDE.md governance skills \| wc -l` | `0`, then a count above 0 | `1`, then `0`. **Resolved by default, not by a task's choice** (the owner's "whatever doesn't matter", read by the term plan; [ASSUMPTION]): the act is worded "states the ideal and grades its evidence" |
| D-42 | the best is the most accommodating identified value from any tier, replaced only by a recorded finding of worse results for the same lens and context (T-059 item 6; OD-58) | T-059's tests `T059-H1` to `T059-H4` (section 4 item 6 of `tasks/T-059-wp-t4-agreement.md`) | no such tests | green; and D-27 prints no line for OD-58 |
| D-43 | no engine text calls a code-sourced best a "floor claim" or "never best practice" (T-068 item 8) | `git grep -c -E 'This is a floor claim\|not a best-practice claim\|only T1/Co-1/T2/Co-2 evidence can do that\|excluded from best-practice' -- scripts/assess/assess_cell.py scripts/audit/adjudication_integrity.py` | a count per file | no file listed; T068-24 green |
| D-44 | the marker table is applied: ● T1, T2, Co-1, Co-2; ◐ T3, T4; ○ T5, T6; ⚠ in place of the circle for a grey, unverified or thin basis (T-117; OD-57, OD-59) | `python3 -c "import sys;sys.path.insert(0,'schemas');from tier_derivation import band;print(band(4,'x').value, band(3,'clinical').value, band(3,'grey').value, band(5,'x').value)"; python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select sql from sqlite_master where name='specifications'\").fetchone()[0].count('⚠'))"` | `◐ ● ○ ◐`, then `0` | `◐ ◐ ◐ ○`, then above 0; T117-01 to T117-06 green |
| D-45 | skills rank no "acceptable" rung and claim no authority (T-035 item 5) | `git grep -l -E 'Ideal → Best Practice\|this guidebook recommends' -- skills \| wc -l` | above 0 | `0`; the voice line as OD-60 answers |
| D-46 | the specification stage's objects carry the stage's name (T-118, deferred) | `python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select type,name from sqlite_master where name like '%determination%'\").fetchall())"` | a table and two views | `[]`. **Resolved by default** (the owner's "whatever doesn't matter", read by the term plan; [ASSUMPTION]): no alias object under an old name; the stage stays "specification"; `v_best_practice` keeps its name unless OD-62 is answered "rename" |
| D-47 | the frozen compendium is out of agent search (T-121; OD-61) | `grep -c -E '^references/bpc' .ignore` | `0` | `1`, or T-121 declined by the owner's "no" in the ledger |

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
| T-1a | notation arithmetic to one home; the writer refuses unreadable figures | T-016; the `derive-extraction` repair T-016 left as three recorded blockers is T-063 (on OD-40, resolved under delegation 2026-11-13) | read; T-063 authored 2026-11-13 |
| T-1b step 8 | `amend-extraction` widened to unit, value and NULL setting (OR-3: "Yes, reformat in place") | T-061 (the `ratio` to `rise:run ratio` branch is T-093, on OD-41, resolved under delegation 2026-11-13) | authored 2026-11-13 |
| T-1b step 9 | the length family, `RULE_VERSION` bump (OR-10: "Yes, convert and show both") | T-030 (it already holds OR-10 and OD-22; no new file; the corrections it needs are OI-57 (16); its metric-to-metric display is OD-42, resolved under delegation 2026-11-13) | read |
| T-1b step 10 | the `verified` gate: a full-scope scan (OR-11a: "Yes, require a full-scope scan") | T-062 (the writer half has existed since 2026-11-06; T-062 makes the class blocking at rest, after T-105) | authored 2026-11-13 |
| T-2 | conditions become branches | T-017 | read |
| T-3 | the lens gather | T-019 (and T-018) | read |
| T-4 steps 1, 2, 4 | exclusion causes, recorded divergence, fragility note | T-059 | authored 2026-11-13 |
| T-4 step 3 | the Co-1 dimensional boundary (OR-5) | **no task**: held on OR-5b's three open edges (ledger, tenth set) | by decision |
| T-5 | render | T-037 (replaced) | as the workplan says |
| T-6a | language case fold | T-015 | read (Traces) |
| T-6b | search terms from the alias table, `jurisdiction_buckets`, `v_coverage_parameter_via_admission` | T-026 (the terms half, merged); T-025 and T-101 (the bucket is `lang_jur_map.scope_status` read through `v_research_scope`, migrations 122 and 123); T-067 (the one missing view) | read; OR-8 and OR-12 ruled |
| T-7 | element pointer, derived at read | replaced by T-060 (stored, OR-14b) | by decision |
| T-8 | `add-root` writer; `convergent` needs two distinct roots | T-048 (the writer) plus T-068 (the distinct-roots count, on OD-43, resolved under delegation 2026-11-13 and answered by the owner 2026-11-14: agreement between any two kinds of evidence; since the owner's later statements of 2026-11-14 the roots are counted and shown beside every convergence, no longer a condition of it) | read; T-068 authored 2026-11-13 |
| D-1 | repair unreadable and prose-unit rows | T-108; the bare-`ratio` rows T-086 (on OD-41, resolved under delegation 2026-11-13) | read (Traces) |
| D-2 | fill a NULL lens only where a quote names the users | T-106 | read (Traces) |
| D-3 | the scan contract exercised | T-105 | title only; OR-16 and OR-25 ruled |
| D-4 | promote adjudicated non-English observations to aliases | T-069 | authored 2026-11-13; OR-17 ruled |
| D-5 | blind double extraction (measurement) | T-070 (OD-44, referred back to the owner 2026-11-13 because OR-15's premise is false for batch 23, answered by the owner 2026-11-14: A, the corpus-wide T1 or T2 source with the most findings) | authored 2026-11-13; OR-15 and OR-18 ruled |
| D-6 | element pointers (data) | after T-060 | by decision |
| D-7 | re-grade NULL and untraced roots | T-071 | authored 2026-11-13; OR-19 and OR-20 ruled |
| D-8 | seed quantities from observed phrases | T-072 (T-109 gives the live parameters their kind) | authored 2026-11-13; OR-13 ruled |
| S-1 | the engine over every parameter, rendered | T-110 (then T-037) | read |

Unmapped after this pass: count the rows above that say **no task** (`sed -n '/^\*\*The prior workplan mapped/,/^Unmapped after/p' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md | grep -c -F '**no task**'`). Each is owed a task or a decline in the owner's words (OI-52 in `OPEN-ITEMS-PLAN.md`); none is a decline. Mapped 2026-11-13 by the authoring of T-061 to T-063 and T-067 to T-072: the rows that name them.

**Pilot results, second round (2026-11-13).** The staged pilots of `OPEN-ITEMS-PLAN.md` section 4 were run (R2 first, then P0 to P7) as Sonnet-class dry pilots in scratch clones, Opus-class for T-028 and T-102; reports and patches are in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/` (`PILOT-BRIEF.md` is the brief every executor got). Which task files now read as piloted: `grep -l '^\*\*Pilot status.\*\* \*\*Piloted' workplan/2026-11-12-bidirectional-pipeline/tasks/T-[0-9]*-*.md`. Departures from the plan, and what the pilots showed:

- **T-014 was a dry pilot, not a real execution**, so no pull request would be opened for the owner to merge. Its behaviour-preservation claim is therefore unproven (the stress scripts hard-code the repository root; T-014's fold makes it derived).
- **T-102 was a partial pilot** (the carry and the emit-and-replay on a sample); the final `SCI` retirement was not reached because T-054 is not in the stack.
- **Every pilot found defects in its task file**; none was an executor's error. The most common were (by how many files they touched): the generated `governance/context-map.yaml` going stale after a migration; `research_tooling_separation` reading `origin/main` and not `$BASE`; objects a section 4 requires but does not name while section 8 forbids unnamed objects; sweeps that match names and miss behaviour; "thin pointer" task files (T-016, T-017, T-019) that were not self-contained and whose cited report's protocol contradicted them. Cross-cutting fixes went into every file by script; per-task fixes by one Opus-class fold per file, each recording design choices as "Chosen (pilot 2026-11-13)".
- **Design faults the pilots found, now corrected in the files:** `--value-as-written` as a free pass (T-008); a junction by rowid that cannot be a foreign key (T-026, T-028 design, T-049); a quantity kind that anything could be minted under (T-020); a foreign key "only for codes present" that SQL cannot do (T-024); a done-when whose premise was false in the data (T-017: parameter 12 carries condition edges); the emitter replaying an INSERT before the UPDATE it depends on (T-018, which blocks T-102 and every carry-by-replace task until it merges).
- **Pilot patches are provisional.** The patches were made from the unfolded files; their real executions will differ. A stacked pilot's result is provisional on its predecessors (`OPEN-ITEMS-PLAN.md` section 4).
- **Environment faults met:** the local `main` ref was stale (a clone's `origin/main` is old), so every pilot took the branch tip as its base; the container disk filled once (pilot clones removed afterwards; reports and patches are kept in the repository).

**Thirteenth set (2026-11-14).** The owner answered the four items of "Four things to see first" in `OWNER-SHEET-PLAIN.md` (`grep -n -F "Owner answers 2026-11-14 (thirteenth set)" references/project-standards.md`): (1) agreement between any two kinds of evidence counts as convergence, and convergence defines most common practice, which is not best practice (OD-43 answered by the owner; its delegated limit to the clinical and Co-1 axes superseded on contact); (2) OD-44 answered A; (3) the measurement first, and the guidebook concerns design itself, so "new or existing" and code status leave the circumstances OD-49 types (building use and interior or exterior remain); (4) provisions whose question is presence, such as hearing loops, are included, which overtakes OD-53's declination for them and registers OD-56 (how), open for a delegated, independently checked resolution. Folded into T-068, T-070, T-091, T-092, and a render note in T-037 and T-032; `OPEN-ITEMS-PLAN.md` OI-60; `DECISION-CLOSURE.md` §4 prompt 18.

**OD-56 answered (2026-11-14, later).** The owner wrote "b" in reply to OD-56's four options, read as option (b) (`grep -n -F "Owner answer 2026-11-14 — OD-56" references/project-standards.md`; the reading is an [ASSUMPTION], told to the owner and not corrected): an element-level determination lists the provisions an element should carry, by pointer; a provision is not a parameter and no value is computed for it. No delegated resolution is run. Folded into T-060 (provision-term and source-statement pointers, still no value column), T-029 (the `element has provision` kind, with a test), and a note in T-072 item 6 and T-087; `OPEN-ITEMS-PLAN.md` OI-60 resolved; `DECISION-CLOSURE.md` §4 prompt 18 answered.


**The term-resolution fold (2026-11-14).** On the owner's instruction to fold the term-resolution plan into this one with the newer plan prevailing (section "Precedence" at the top), `TERM-RESOLUTION-PLAN.md` was folded: its TT-1 joins T-068 (item 8: the engine strings), TT-2 joins T-059 (item 6: selection across all tiers under the harm test, held on OD-58), TT-4 joins T-035 (item 5: the skills rows, its voice line on OD-60); TT-3 is T-117 (the marker table, on OD-57 and OD-59), TT-7 is T-118 (deferred), PR-1 is T-119 (the ledger's unification entry), PR-2 is T-120 (doctrine, the dead table name, the delete list, the atoms), and Q5's `.ignore` change is T-121 (on OD-61), apart so that T-120 can ship now; TT-5 is no task (data in T-120), TT-6 is a GAP (`OPEN-ITEMS-PLAN.md` OI-61), and PR-5 is T-110's first write or a research batch after T-117 (OI-65). Q1 to Q6 are OD-57 to OD-62, referred to the owner, none resolved under delegation (ledger: `grep -n -F "## Registration 2026-11-14" references/project-standards.md`). Conflicts resolved in this plan's own text, each with a "Superseded in part" note: T-059 (OR-4 and OR-6c read through the harm test for selection), T-068 (the marker it leaves unchanged; OR-4; TT-1), T-035, T-037 (the figures of a cell and the markers at render), T-060 (new objects carry `specification`), T-110 (OR-6c; PR-5), every task file's "Do not author `best_practice_synthesis`" line, OD-48's option (a) here and in `DECISION-CLOSURE.md` (its "○ flag"), and `OWNER-SHEET-PLAIN.md` (question 4's codes-only sentence and the convergence answer). The mapping item by item, and every conflict with the text before and after: `TERM-PLAN-FOLD.md`. Also corrected: OD-56's status line now carries a bare date, so D-36's count reads it (it printed two unequal numbers before).
