# The term-resolution plan folded into the remediation plan

_Written 2026-11-14 (UTC) by the integrator, on the owner's instruction of 2026-11-14 to fold the term-resolution plan into the remediation plan "with this newest plan having priority in conflicts" (`grep -n -F "Owner instruction 2026-11-14 (last) — fold the term-resolution plan" references/project-standards.md`). Precedence: [`TERM-RESOLUTION-PLAN.md`](TERM-RESOLUTION-PLAN.md) over the remediation plan; the ledger over both (CLAUDE.md rule 0). Changed: plan documents and task files in this folder, the generated `REMEDIATION-PLAN.md`, and one append to the ledger (the registration of OD-57 to OD-62, in the form of the 2026-11-13 referrals). No script, schema, governance file, skill, database row or git state was changed. No count below is typed: each is the command that computes it (rule 7a)._

```
F=workplan/2026-11-12-bidirectional-pipeline
ls $F/tasks | grep -E '^T-1(1[7-9]|2[01])-'                                   # the task files this fold created
grep -c -F 'Superseded in part by TERM-RESOLUTION-PLAN' $F/tasks/T-*.md | grep -v ':0$'   # task files carrying a supersession note
grep -o -E '^### OD-(5[7-9]|6[0-2])' $F/REMEDIATION-WORKPLAN.md                  # the decisions this fold registered
grep -E '^OD-(5[7-9]|6[0-2]) STATUS:' references/project-standards.md            # their status lines
python3 -I <a copy of scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py whose OUT points outside the tree> | head -2   # missing deps [] ; unregistered []
```

## 1. Where each numbered item of the term plan now lives

### Section 1 (the canonical definitions)

| Term plan | Where it lives now |
|---|---|
| U1 to U4, U6 (best; most common; the minimum; the four figures and direction; code-only) | written into `governance/evidence-architecture.md` §0 by **T-120** item 1; recorded in the ledger by **T-119** |
| U5, U8 (show, don't rule; transparency) | `governance/mission-and-epistemics.md`, **T-120** item 2; render's wording, **T-037** (note added) |
| U7 (markers, ⚠, thin) | **T-117** (code and CHECK); the W prose, **T-120** item 2a; OD-57 and OD-59 answered (section 4) |
| U9 (names) | **T-118** (deferred); **T-060** (new objects carry `specification`) |

### Section 2 (the amend list)

| Term plan row | Where it lives now |
|---|---|
| `governance/evidence-architecture.md` new §0 | **T-120** item 1 |
| `evidence-architecture.md` floor-selection, convergence and "best-practice determination" lines (R) | **T-120** item 2 |
| `evidence-architecture.md` "weak band (○)" lines (W) | **T-120** item 2a (moved from T-117 item 6, section 4) |
| `governance/evidence-methodology.md` pointer lines and "the hierarchy adjudicates" (R) | **T-120** item 2 |
| `evidence-methodology.md` convergence voice, code-only state, §2.3 richness ("R (in T-068)") | **T-068** caller sweep (section 5, sentence added) |
| `governance/mission-and-epistemics.md` commitment 2, Test 3, "specifies the evidence-based value", "which dimension governs" (R) | **T-120** item 2; the `doctrine-deltas.json` state, **T-120** item 5 and OI-62 |
| `mission-and-epistemics.md` full-strength anchor list (W) | **T-120** item 2a (moved from T-117, section 4) |
| `governance/tier-system.md` T4/T5 eligibility lines; the banner's ⚠ (R) | **T-120** item 2 |
| `tier-system.md` §5 table (W) | **T-120** item 2a (moved from T-117, section 4) |
| `governance/adversarial-use-framework.md`, `jurisdiction-philosophy.md`, `legal-regulatory.md`, `co1-operational.md`, `grounds.md`, `held-tensions.md` (R) | **T-120** item 2 |
| `governance/pipeline-contract.yaml` band lines (W) | **T-120** item 2a (moved from T-117, section 4) |
| `governance/audience-priority.md` (LEAVE) | **T-120** item 2 names it as left |
| CLAUDE.md §6 marker line (W) | **T-120** item 2a (moved from T-117, section 4) |
| `best_practice_synthesis` in CLAUDE.md §6, governance and skills (R) | **T-120** item 3; and in every task file of this plan, by this fold (conflict 12 below) |
| `references/methodology-evidence-hierarchy-mapping.md` (R; one row W) | **T-120** item 2; the W row, **T-120** item 2a (moved from T-117, section 4) |
| `references/methodology/economics-methodology-core.md` (R) | **T-120** item 2 |
| `workplan/2026-10-30-ramp-spec-pages/RENDER-CONTRACT-parameters-3-and-12.md` (R) | **T-120** item 2 (outside this folder, so not edited by the fold) |
| `OWNER-SHEET-PLAIN.md` line 72 | done by this fold (conflict 15) |
| `tasks/T-059-wp-t4-agreement.md` line 44 | done by this fold (conflicts 1 to 5) |
| `skills/prose-style-checker_SKILL.md` (R; the voice on Q4) | **T-035** item 5; the register rewritten from the doctrine on **OD-60**'s answer (section 4) |
| `skills/voice-style_SKILL.md` | **T-035** item 5 |
| `skills/research-log-manager_SKILL.md` | **T-035** item 5 (and **T-120** item 3 for the dead table name only) |
| `skills/supersession-audit_SKILL.md` | **T-035** item 5 |
| `workplan/pipeline-state-graph/` atoms, `conflicts.yaml`, `machines.yaml` (R; T4 limb W) | **T-120** item 6, the T4 limb included (moved from T-117, section 4) |
| the generated state-graph files | **T-120** item 6 (rebuilt, never hand-edited) |
| R.1 (code-only best at "its code marker by tier", not ○) | **T-117**; T-068's T068-10; OD-48 option (a) in `REMEDIATION-WORKPLAN.md` and `DECISION-CLOSURE.md`; `OWNER-SHEET-PLAIN.md` question 4 (conflicts 8, 13 to 15) |
| R.2 (the mixed cell: harm test) | **T-059** item 6 |
| R.3 (OR-6c resolved for selection; OR-6, OR-6b keep their status words) | **T-059** (conflicts 1 to 5); **T-110** (conflict 11); OI-07; the within-rank approach left open, **OI-66** |
| R.4 ("authority" verbs; the determination ruling) | **T-120** item 2 (RENDER-CONTRACT, audience-priority) |
| R.5 (engine strings misname the most accommodating code value) | **T-068** item 8 |
| R.6 (one ledger entry per corpus collapsed to one) | **T-119** item 1 (b) |

### Section 3 (the supersession entries)

| Term plan | Where it lives now |
|---|---|
| The one ledger entry and its BY sentence | **T-119** item 1 |
| (a) machine pairs | **T-119** items 1 and 2, with an attestation (item 3); since the owner's answers, the pairs tied to the circle table too (section 4) |
| (a) pairs tied to the circle table (weighted-strength reconciliation; option-A execution's table lines) | **T-119** item 1 (a) (moved from T-117 item 6, section 4) |
| (a) the posture record's passage the plan keeps | **T-119** item 1 (named as not superseded) |
| (b) prose-only supersession of frozen corpora | **T-119** item 1 (b) |
| (b) `governance/doctrine-deltas.json` (append, not supersede) | **T-120** item 5; **OI-62** |
| (c) ledger rules (OR-4; OR-6c as to selection) and the baseline `decisions` rows | **T-119** item 1 (c); the rows staying `ACTIVE`, **OI-61** |
| (d) state-graph atoms by `status_corrections` | **T-120** item 6 |
| Governance passages amended in place, with an "Amended 2026-11-14" note | **T-120** (its note form) |

### Section 4 (tooling tasks)

| Term plan | Where it lives now |
|---|---|
| TT-1 (engine strings; `adjudication_integrity.py` line) | **T-068** item 8 and test T068-24; dependency on **T-120** added ("depends on PR-2"); the proxy-branch string (its line 1469, which waited on Q1) moved to **T-117** item 4 |
| TT-2 (selection across all tiers under the harm test; lens-matched only) | **T-059** item 6 and tests T059-H1 to H6; on **OD-58**, answered by a statement standard (section 4); dependency on **T-120** added |
| TT-3 (apply the marker table) | **T-117** (the number the plan named; checked free by `ls tasks \| grep -oE '^T-[0-9]+' \| sort -u \| tail -1`, which printed T-116 before the fold); on **OD-57** and **OD-59**, answered (section 4) |
| TT-4 (skills rows) | **T-035** item 5; on **OD-60**, answered (section 4); dependency on **T-120** added |
| TT-5 (state-graph edits: no task) | data in **T-120** item 6; not registered as a check |
| TT-6 (no writer for `decisions.status`: a GAP) | **OI-61** (class E; the gap row is written by the next research batch) |
| TT-7 (stage tools carry the stage's name; deferred) | **T-118**, after T-021, T-059, T-068 and T-117 (T-021 added by the fold: it widens `determination_gates`) |
| "Checks: add none" | no check added by any of T-117 to T-121 |

### Section 5 (the delete list)

| Term plan | Where it lives now |
|---|---|
| `references/connections/application-queue.md` | **T-120** item 4 (delete) |
| `references/website/data/populations.json` and its two prose callers | **T-120** item 4 (move to `_archived/`, fix callers) |
| `references/bpc/_template.md` | **T-120** item 4 (delete) |
| research-log-manager's BPC flows | **T-035** item 5 |

### Section 6 (held and owner questions)

| Term plan | Where it lives now |
|---|---|
| Resolved from the rulings (the OWNER-Q records; the T4 question; "showing data, not determining"; the proxy branch; bpc project inferences; "best practice as currently known") | applied in **T-059**, **T-117**, **T-037** (qualifier may drop), **T-068**; recorded in the ledger registration's "Resolved by default" paragraph |
| Resolved by default (no aliases; the verb "states the ideal and grades its evidence"; the stage stays "specification") | marked in **D-41** and **D-46** of `REMEDIATION-WORKPLAN.md` §10; **T-118** section 2; the ledger registration |
| Q1 | **OD-57**; held **T-117**; plain question 8; prompt 19 *(answered 2026-11-14, fourteenth set: section 4)* |
| Q2 | **OD-58**; held **T-059**; plain question 9; prompt 20 *(answered 2026-11-14, fourteenth set: section 4)* |
| Q3 | **OD-59**; held **T-117**; plain question 10; prompt 21 *(answered 2026-11-14, fourteenth set: section 4)* |
| Q4 | **OD-60**; held **T-035**; plain question 11; prompt 22 *(answered 2026-11-14, fourteenth set: section 4)* |
| Q5 | **OD-61**; held **T-121** (a task of its own so that T-120 is not held); **OI-63**; plain question 12; prompt 23 *(answered yes 2026-11-14 by the owner's correction: section 4)* |
| Q6 (optional) | **OD-62**; holds no task (standing; no rename while unanswered); plain question 13; prompt 24 |
| Render's: the scope of mode and median; OR-6b clusters in T-068 | ~~T-037 (note added)~~ **OD-63** (the owner's, by the ledger; conflict 21; answered 2026-11-14, fifteenth set: section 6) and **T-124** (the figures' specification-stage home); OR-6b clusters stay in **T-068** item 6 (Q-T068b, part (d) of **OD-66**) |

### Section 7 (sequence)

| Term plan | Where it lives now |
|---|---|
| 1. PR-1, ledger | **T-119** (Wave 0, now) |
| 2. PR-2, doctrine | **T-120** (after T-119) |
| 3. PR-3, tooling: TT-1, TT-4, then TT-2 after Q2 | **T-059** item 6 first (after T-120; OD-58 answered; OD-65 answered 2026-11-14, section 6), then **T-068** item 8 (after T-059 and T-120), **T-035** item 5 (after T-120; OD-60 answered). *Corrected 2026-11-14: the plan's order put TT-1 before TT-2, against the T-059 → T-068 edge; conflict 20 below.* |
| 4. PR-4, T-117 after Q1 and Q3 | **T-117** (after T-119, T-120, T-068 and, since the adversarial repair of 2026-11-14, T-102; OD-57, OD-59 answered; OD-64 answered 2026-11-14, section 6); its W prose in **T-120** (section 4) |
| 5. PR-5, research rows (re-assess specifications) | **T-110**'s first write, T-117 now being its dependency (corrected 2026-11-14; **OI-65**) |
| 6. PR-6, T-118 (deferred) | **T-118** (last, by its dependencies) |
| Rule 9 for every PR | in every new task file's section 11 |

Section 8 (risks) is carried where each bites: risk 1 and 2 in T-059 item 6; risk 3 in T-117 section 8; risk 4 in T-120 item 6; risk 5 in OI-61; risk 6 in T-120 item 7; risk 7 in OD-60 and T-068 item 6; risk 8 in T-120 item 4.

## 2. Conflicts resolved (step A), with the text before and after

Each changed passage carries a note "Superseded in part by TERM-RESOLUTION-PLAN section n (2026-11-14)" (or a "Corrected 2026-11-14" note in the owner's sheet). Searched with `git grep -n -i -E 'best[ _-]?practice|most accommodating|\bideal\b|acceptable|code floor|floor claim|OR-4\b|OR-6c|weak band|○|◐|⚠|\bthin\b|higher rank' -- workplan/2026-11-12-bidirectional-pipeline` and then read in context.

| # | File | Before | After |
|---|---|---|---|
| 1 | `tasks/T-059-wp-t4-agreement.md` §2 Owner decisions | "none in the register. The rulings this task rests on are in the ledger: OR-4 …, OR-6 …, OR-6b … and OR-6c" | OD-58 with its gate; "for selection, OR-4 and OR-6c are read through the harm test"; OR-6, OR-6b keep their status words |
| 2 | same, §3 (the term plan's "T-059:44") | "the most accommodating value wins whatever anchoring tier stated it (OR-4) … the T1 figure is stated and the T2 dispute is noted … the higher rank stating the value" | the most accommodating identified value from any tier, replaced only by a recorded finding of worse results for the same lens and context; the old text kept, marked superseded |
| 3 | same, §4 item 3 | "OR-4 = yes: no change to the selection rule beyond the extension the report names" | "OR-4, read through the harm test: the selection rule changes as item 6 says" |
| 4 | same, §4 item 4 | "the higher rank states the value, the lower rank's dispute is noted"; approach kind `higher_rank_states` | the harm test supplies the approach between ranks; kind `harm_test`; within a rank the refusal is kept and reported (OI-66) |
| 5 | same, §6 step 2 | "A divergence across ranks … is stated at the higher rank" | "stated at the most accommodating value unless a recorded finding of worse results replaces it" |
| 6 | `tasks/T-068-convergent-counts-roots.md` §4 item 3 | "nor its marker (●, ◐, ○)" | "(●, ◐, ○, and ⚠ once T-117 lands)" |
| 7 | same, §4 item 6 | "best practice stays the most accommodating value … (OR-4; …)" | "… replaced only under the harm test (the owner's answer of 2026-11-14, which resolved OR-4 for selection …)" |
| 8 | same, test T068-10 | "the marker ○ as before" | "the marker unchanged by this task, as `band()` and the engine give it on the base (○ while the override stands; ◐ for T4-only once T-117 lands); assert equality, never a typed glyph" |
| 9 | `tasks/T-037-render.md` §4 | (silent on the four figures, ⚠, "acceptable" and the qualifier) | note: every value shown and cited; the four figures in accessibility direction; no "acceptable", "required" or "recommended" on the project's authority; the stored marker incl. ⚠; the qualifier may drop; mode and median scope is render's |
| 10 | `tasks/T-060-element-determination.md` §4 | (no naming rule; its evidence command searched for `element_determination` as a candidate name) | new objects carry `specification` (for example `element_specifications`) |
| 11 | `tasks/T-110-first-determinations.md` §2 | "OR-6c (divergence across ranks …; built by T-059)" | "… which for selection is now read through the harm test (T-059 item 6, held on OD-58)"; PR-5 noted (OI-65) |
| 12 | every task file's section 8 (`grep -l -F "CLAUDE.md §6's \`best_practice_synthesis\` names" workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md \| wc -l`) | "Do not author `best_practice_synthesis` or …" | "Do not author a specification row (`specifications`, read through `v_best_practice`; CLAUDE.md §6's `best_practice_synthesis` names a table not in the schema: superseded in part …) or …" |
| 13 | `REMEDIATION-WORKPLAN.md` OD-48 option (a) | "a code-only wheelchair cell reads `population` with the ○ flag" | "… with its code marker by tier (○ for a T5 or T6 basis; ◐ for a T4-only basis once T-117 applies the table)" |
| 14 | `DECISION-CLOSURE.md` prompt 10 (OD-48) option (a) | "with the ○ flag" | "with its code marker by tier (○ for T5 or T6; ◐ for a T4-only basis once T-117 applies the table)" |
| 15 | `OWNER-SHEET-PLAIN.md` question 4 (the term plan's line 72) | "The July rule's purpose was to stop a value resting only on codes from ever being shown as best practice. Under A that protection is kept by the separate codes-only mark, which already exists." and "shown with the weak-evidence mark (○)" | a codes-only best is now allowed, shown with its mark ("the empty circle makes it clear …"); "shown by the code's own mark (○ for national codes; ◐ for international standards once you apply the circle table) and by the codes-only flag" |
| 16 | `OWNER-SHEET-PLAIN.md`, the first of the four things and the OD-43 summary (a conflict with the ledger, which outranks both plans) | "… and rest on at least two independent sources" | the root count shown beside agreement, not required (the owner's convergence statements of 2026-11-14) |
| 17 | `OPEN-ITEMS-PLAN.md` OI-07, OI-08 | "OR-6c answered (tenth set)"; "Bears on T-110's markers" | OR-6c read through the harm test for selection (OI-66 for the within-rank approach); T-110's markers change with T-117 |
| 18 | `REMEDIATION-WORKPLAN.md` §3 rows and §5 dependency lines for T-035, T-059, T-068 | T-035 "none for token corrections / none"; T-059 "T-016, T-019 / none in the register (OR-4 … answered)"; `T-068 <- T-059 [delegated: OD-43 …]` | T-035 "T-120 / OD-60"; T-059 "T-016, T-019, T-120 / OD-58; OR-4 and OR-6c read through the harm test"; `T-068 <- T-059, T-120 [owner: OD-43, answered …]` |
| 19 | `tasks/T-035-skills-repair.md` §2 | "Tasks … first: none for token corrections"; "Owner decisions: none" | "T-120 merged"; OD-60 with its gate |
| 20 | `TERM-RESOLUTION-PLAN.md` §7, and this file's section 1 row for its step 3 (found by the adversarial pass, 2026-11-14) | "PR-2 and PR-3 can ship now"; "PR-3: TT-1 and TT-4, then TT-2" | the real edges, T-119 → T-120 → T-059 → T-068 → T-117 (T-035 after T-120); the term plan carries it as erratum 5. **A conflict resolved:** the term plan governs the remediation plan where they conflict, but its sequence contradicted the task files' own hard dependencies, which are facts about what each change needs; the dependencies win and the term plan is corrected, not the tasks |
| 21 | `TERM-RESOLUTION-PLAN.md` §6, `tasks/T-037-render.md` §4 (the ledger outranks both) | "Render's, not the owner's now: the scope of mode and median" | the scopes of the maximum, the mode and the median are the owner's ("leave the maximum, mode and median scopes to the owner"): OD-63, holding T-124; erratum 6 |
| 22 | `TERM-RESOLUTION-PLAN.md` §8 risk 1; `tasks/T-059-wp-t4-agreement.md` test T059-H4 (the ledger outranks both) | "a generic code value carries no lens … compare only values whose lens matches"; H4 "not selected, shown" | the premise corrected (code figures carry `ALL`); whether such a value may be selected is OD-65, referred; erratum 7. *Answered 2026-11-14 (section 6): every code value carries a lens; H4 withdrawn* |
| 23 | `tasks/T-037-render.md` §4 and T-122 item 6 ("A page shows every identified value with its citation"; `render-every-value-cited`), from TERM-RESOLUTION-PLAN U8 and the owner's transparency entry, against the owner's answer to OD-63 (fifteenth set, 2026-11-14) | the transparency entry: "presents all values/approaches/data for comparative purposes", read by its recorder as "a cell shows every identified value, each with its citation" (`grep -n -F 'presents all values/approaches/data for comparative purposes' references/project-standards.md`) | OD-63: "on the render page itself, we just have the minimum, mode, median and maximum colour coding the jurisdiction code bodies that we surveyed". **Not resolved, recorded:** the later answer is built on the render page (rule 0), every value stays in the determination and cited, and T-122's criterion is renamed `render-figures-cited`; whether a reader can still reach every value from the page (a link to the specification's cited values) is not stated by either entry, and is left to the owner and to T-037's design, not decided here |

**Read and found not in conflict** (the remaining hits of the search): T-032 (convergence is most common practice, never best: agrees with U2); T-035 item 2 (best practice is the determination's output, the most accommodating value in the direction: agrees with U1, U4); T-087 ("do not record a figure as best practice": agrees); T-061, T-091, T-092 (no term in the swept sense; circumstances are the "context" of U1, carried as T-091 plans); T-053 (its "harm ordering" weighs one group's harm against another's in a conflict between groups, a different rule from the harm test of selection: the two must not be conflated, and T-059 item 6 names only the harm test); T-056 item 3a (it states no marker); D-08, D-19 and D-37 of `REMEDIATION-WORKPLAN.md` §10 ("determination" stands under the owner's definition). Also corrected while there, not a term conflict: OD-56's status line now carries a bare date, so D-36's two counts are equal again.

## 3. What could not be folded, or was folded with a consequence

- **OD-58 held T-059, and so the chain to the first live determinations** (answered 2026-11-14: section 4) (T-059 is a dependency of T-068, T-110, T-117 and T-118). The term plan says TT-2 "can be built with 'any recorded finding' as the default"; the instruction to gate TT-2 on Q2, with TT-2 inside T-059, makes the whole of T-059 wait. If the owner wants T-059's other steps to ship first, TT-2 must be split out into a task of its own; the fold did not do that unasked.
- **T-035's token corrections waited on OD-60** for the same reason (the gate holds the whole task); answered 2026-11-14 (section 4).
- **The `.ignore` change (Q5) has no task in the term plan**; it became T-121 so that T-120 (which the plan says ships now) is not held by OD-61.
- **PR-5** is not a task: no specification is live today, so it is T-110's first write or a later research batch (OI-65).
- **The within-rank divergence approach** under the harm test is not settled by the term plan (OI-66).
- **The RENDER-CONTRACT row** lies outside this folder; it is T-120's to edit, not the fold's.

## 4. After the owner's answers to OD-57 to OD-61 (fourteenth set, 2026-11-14)

Applied by the integrator (ledger: `grep -n -F "Owner answers 2026-11-14 (fourteenth set)" references/project-standards.md`, and for OD-61 the owner's correction `grep -n -F "Owner correction 2026-11-14 (fourteenth set, later) — OD-61" references/project-standards.md`). Each gate now reads OPEN (owner); the generator's owner-decision queue confirms it (`python3 -I <the copy of build_batches.py above> | head -2`). One home per row:

| Answer | Where it was applied |
|---|---|
| OD-57 yes; OD-59 yes | **T-117** keeps the code (`band()`, the override, the mixed-cell marker as "its own", ⚠, the migration, the proxy string); the W prose rows and the atoms' T4 limb moved to **T-120** (item 2a, item 6; gated on OD-57 and OD-59, which are open); the table's decision-record pairs moved to **T-119** (item 1 (a)) |
| OD-58, a statement standard | **T-059** item 6 (the standard; tests H1 to H6; the record for a statement is the task's design point, since `harm_finding` and `insufficient` do not fit it); D-42; T-110's note; the "measured outcome" wording replaced in TERM-RESOLUTION-PLAN §4 and §6, DECISION-CLOSURE and OWNER-SHEET-PLAIN |
| OD-60, rewrite from doctrine | **T-035** item 5 (the register rewritten, its contents and sources named; executor now Opus-class); D-45 |
| OD-61 yes (by correction) | **T-121** open; D-47; OI-63 resolved |
| OD-62 | unchanged: referred, optional, default no rename |

## 5. After the adversarial pass on the remediation plan (2026-11-14)

Four read-only auditors attacked the plan at commit b3d914f3 (`scratchpad/session_2026-11-13-edmonton-checklist-pass/sweep/adj/AUDIT-FINDINGS.md`). The repair writer verified each finding by command; what it changed in the term plan's homes: conflicts 20 to 22 above and the term plan's errata 5 to 8; the selection rule consolidated in one home (`tasks/T-059-wp-t4-agreement.md` section 4 item 6, which T-068, T-110, T-117, T-120 and T-124 point to); four questions registered and referred to the owner (OD-63 to OD-66; ledger: `grep -n -F "questions the adversarial pass on the remediation plan found" references/project-standards.md`); four new tasks (T-122 to T-125). The full list is the remediation workplan's section 13, "The adversarial repair".

## 6. After the owner's answers to OD-63 to OD-65 and OD-66 (a)(b) (fifteenth set, 2026-11-14)

Applied by the integrator (ledger: `grep -n -F "Owner answers 2026-11-14 (fifteenth set)" references/project-standards.md`). OD-63, OD-64 and OD-65 read OPEN on the gate; OD-66 still reads `REFERRED BACK TO THE OWNER`, its parts (c) and (d) open, and holds no task. What moved:

| Answer | Where it was applied |
|---|---|
| OD-63, all values; render shows the four as a colour code on the surveyed code bodies | **T-124** item 1 (the maximum, mode and median over every identified value, every stratum; each figure's rows carry their jurisdiction; test T124-08) and item 2 (where render reads them); **T-037** §4 "The figures of a cell" rewritten (the four only, as a colour code on T-036's surveyed code bodies, read from T-124; the non-colour carrier is T-037's to design, WCAG 2.2 SC 1.4.1; tests F1 to F5); **T-122** items 2 and 6 (criterion renamed `render-figures-cited`); **T-120** item 1 (§0 quotes the answer); D-49; TERM-RESOLUTION-PLAN U4; conflict 23 recorded |
| OD-64, triangle for every grey basis | **T-117** item 1 (the T3 grey ◐ row deleted; `band()` not raised for grey) and test T117-03 (⚠, no circle); **T-120** item 2a (the doctrine table); **T-122** item 3; D-44 (its `band(3,'grey')` term dropped); TERM-RESOLUTION-PLAN U7 and TT-3 |
| OD-65, every code value has a lens by contextual judgment | **T-059** §2 and item 6 "Lens" (no "no lens" branch; where the lens is recorded: `extraction_lens_links`, T-018/T-019, `basis`); test T059-H4 withdrawn (D-42, T-122 updated); **OPEN-ITEMS-PLAN** OI-72 (no task assigns a lens by context where neither clause nor heading names a group; the `basis` CHECK has no value for it); TERM-RESOLUTION-PLAN risk 1. OD-47 stays the owner's |
| OD-66 (a)(b), 2%, one tolerance, a band around the converging value, no chaining | **T-068** item 5 (the constant `Fraction(2, 100)` in one home; the band; no chaining; tests T068-15 at 1.9% and 2.1%, T068-16 with a drifting series, T068-17 at 2%); D-48; every 5% in the plan folder marked withdrawn (derive: `git grep -n -E '5 ?%' -- workplan/2026-11-12-bidirectional-pipeline`; what remains is history or a quoted earlier text) |
| OD-66 (c)(d) | unchanged: referred to the owner; T-068 builds the working readings ("the same"; OR-6b's treatment) *(closed later on 2026-11-14 by the owner's sixteenth set: section 7)* |

## 7. After the owner's instruction of the sixteenth set (2026-11-14)

Applied by the integrator (ledger: `grep -n -F "Owner instruction 2026-11-14 (sixteenth set)" references/project-standards.md` and the four statements after it). OD-66 now reads `ANSWERED BY THE OWNER` on the gate and leaves the standing list. What moved:

| Instruction | Where it was applied |
|---|---|
| OD-66 (c)(d): the registered recommendations; the 2% kept | **T-068** pilot status, item 5 (grouped by the same, consistency beside it, built as decided) and item 6 (Q-T068b closed: OR-6b's treatment, the cue written), test T068-19; register OD-66 (status, answer line, no task); gates table of `REMEDIATION-WORKPLAN.md` §6; `DECISION-CLOSURE.md` prompt 28 and its sixteenth-set paragraph; `OWNER-SHEET-PLAIN.md` question 17 (closed, not asked) |
| Placeholder colours with a non-colour carrier; render details not the owner's | **T-037** §4 item (iii) (the one table of placeholders: colour, text label, marker; the final palette a render design choice) and item (iv) (defaults for a body with several values, a body between the figures, a value that is two figures, a cell with no code body); test T037-F2's wording |
| A task assigning lenses to code values by context, in the judgment stage's recording call (the owner: "yes lens in judgment"), at the moment of recording; mounting height and any clearance default to wheelchair users | **T-126** (new, tooling: `context` basis and `basis_reason` by schema migration; `add-extraction` and `add-lens-link`; skill guidance with the worked defaults; tests T126-01 mounting height, T126-02 knee clearance, T126-03 the override) and **T-127** (new, research: the stored code values); hard dependencies of **T-059** and **T-110**, and T-127 of **T-115**; note in **T-106**; register OD-65 and OD-47 notes; D-50; the critical-path paragraph; **OPEN-ITEMS-PLAN** OI-72 resolved (class R) |

**Conflicts found, recorded, not resolved by the integrator.** (24) The stage map places `source_value_extractions` and `extraction_lens_links` under `judgment` (`grep -n -E 'extraction_lens_links|source_value_extractions' governance/stage-map.yaml`), and the code value's row is recorded by `add-extraction` at the judgment stage (`skills/run-pipeline_SKILL.md` §4); the owner's "that should be done in evidence stage" and "at the moment of recording the row" coincide only if the recording step is what the owner calls the evidence stage. T-126 builds the assignment in the recording call and leaves the table's stage unchanged. **Resolved by the owner:** "yes lens in judgment" (ledger, 'Owner answer 2026-11-14 (sixteenth set, last)'): the lens stays in the judgment stage; "evidence stage" was the timing, at recording. (25) OD-31 gives a provision under a general heading "no identity"; the owner's worked defaults give a mounting-height or clearance clause the wheelchair-user identity by context. The later, more specific statements govern those clauses (rule 0); OD-31's rule stays the default where no worked default applies.
