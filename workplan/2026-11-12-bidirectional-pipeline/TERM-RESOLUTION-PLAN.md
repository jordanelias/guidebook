# Term-resolution plan: best / ideal / most accommodating, most common, floor

**Status.** Written 2026-11-14 by an Opus-class unifier from seven adjudications of two sweeps of the live surface (terms: best practice, ideal, most accommodating, most forgiving, acceptable). Not read by the owner. Where this plan and the remediation plan conflict, **this plan wins** (owner instruction 2026-11-14, ledger entry "fold the term-resolution plan into the remediation plan"); where either conflicts with a ledger ruling, **the ledger wins** (CLAUDE.md rule 0).

**Sources, all in `scratchpad/session_2026-11-13-edmonton-checklist-pass/sweep/`:** sweep one (`out-*`, `check-out-*`, `CONFLICTS.md`), the resweep (`rout-*`, `check2-out-*`, `CONFLICTS-2.md`), the seven adjudications and summaries in `adj/`. Counts below were computed by command over `adj/adjudication-*.jsonl`; re-run rather than trust: 500 records; verdict CONFLICT 288, NOT-CONFLICT 156, HELD 56; resolution SUPERSEDE 200, LEAVE 199, AMEND 80, OWNER-Q 10, TOOL 6, DELETE 5; unify U6 144, U1 96, U5 96, U2 82, U3 24, U4 18, U9 17, U7 14, U8 9; the 200 SUPERSEDEs span 85 files.

**What was checked.** All 141 records that are CONFLICT with AMEND or TOOL, OWNER-Q, HELD or DELETE had their file:line confirmed (140 contain the term; `assess_cell.py:1469` has "most-accommodatingly"). 50 passages were read in their own files across all seven areas, including 9 no sweep flagged. No wrong citations; substantive errors in some replacement wording were reconciled (section R). **Not done:** each of the 200 SUPERSEDE records was not re-read (10 were); not every unflagged voice-style line; the `doctrine-deltas.json` reader; no check suite was run; whether `tier-system.md:22` itself carries the ⚠ glyph (grep shows it on lines 22 and 49).

**Owner answers applied** (ledger from "Owner statements 2026-11-13 (eleventh set)" to the end): the harm test; "T4 only half circle"; the definition of determination (the word stands); "stage tools should match the actual name of the stage"; "whatever doesn't matter" (no aliases after a rename; the verb is "states the ideal and grades its evidence"; the stage stays "specification").

## 1. Canonical definitions (one home each; everything else points)

Home chosen on evidence: `governance/evidence-architecture.md:2` calls itself "CANONICAL … the single entry point to the evidence architecture" and already holds the direction-aware selection (§5) and invariant I3; CLAUDE.md §9 sends doctrine to `mission-and-epistemics.md` and markers to `tier-system.md`. The ledger stays the record of the owner's words; the governance file holds the operative text and quotes the ledger heading.

| Key | Canonical statement (owner's words) | Home |
|---|---|---|
| U1 best | "best practice IS the same as ideal IS the same as most accommodating": "the one that best responds to an ICF/access need/identity within whatever context", "identified in our research … enough if the research source itself simply asserts the value". Tier sets marker and weight, never eligibility. One exception: "does the research prove that the more accommodating value leads to worse results? if so, research wins. if no, code wins." | New `evidence-architecture.md` §0 "The figures of a cell" |
| U2 most common | "convergence is not evidence of best practice but most common practice"; "convergence just means values coming together", across any tiers | §0 holds the sentence; the definition of convergence stays in `evidence-methodology.md` §3.2 (T-068 rewrites it) |
| U3 floor | "the minimum is a factual data point"; "minimum is code stratum unless there is no code data"; "the minimum in some contexts may be the highest allowable number" | §0 |
| U4 figures, direction | "we just have minimum, mode, median, maximum"; "value direction of parameter matters"; the best is the maximum in accommodation order | §0 |
| U5 show, don't rule | "we gather and show"; "showing data, not determining … acceptable isn't relevant as that's a value judgment"; a determination "means to determine the ideal within the context of all evidence factors and consequently what to choose and how to grade quality of evidence for it": it states the ideal and grades its evidence, never a verdict on a design; "must" and "should" said of a design remain verdicts | `mission-and-epistemics.md` commitment 2 and the posture section |
| U6 code-only | "if the only values are from code then code determines the ideal/best", the most accommodating code value; "the empty circle makes it clear that it's not academically or clinically derived" | §0 (a special case of U1 plus the harm test) |
| U7 markers | ● T1, T2, Co-1, Co-2; ◐ T3, T4 ("T4 only half circle"); ○ T5, T6; ⚠ (U+26A0, no FE0F) takes the circle's place for a grey, unverified or thin basis; thin is "when the evidence doesn't directly concern someone but is conjecture", including the project's own inferences and any value that "mixes"; a vetted clinician's judgment, or a clinician's or academic's derivation, is not thin | `tier-system.md` §5; code home `schemas/tier_derivation.py` `band()`; CLAUDE.md §6 points to it |
| U8 transparency | "presents all values … provides citations … does not claim with own authority" | `mission-and-epistemics.md` (with U5) |
| U9 names | a stage's tools "should match the actual name of the stage"; the stage stays **specification**; its output is a specification; the act is "states the ideal and grades its evidence"; `v_best_practice` keeps its name (Q6) | ledger rule plus `governance/stage-map.yaml` |

## 2. Amend list (R = ready now; W = waits on applying the circle table, Q1)

Every replacement is a pointer ("see evidence-architecture §0") or a short phrase in the owner's words. Where an adjudicator wrote out the full definition (A, E, G did), use a pointer instead (rule 5).

| File | Lines | Change | State |
|---|---|---|---|
| governance/evidence-architecture.md | new §0 | Write U1–U4, U6, U8 | R |
| same | 2, 21, 100, 121, 122*, 175, 177, 204 | "most-accommodating floor selection" becomes "most-accommodating selection; the minimum is its own figure"; best is never convergence; roots shown beside convergence; 121 keeps "best-practice determination" but stops calling the floor the best | R |
| same | 44, 77, 82, 125, 186, 208 | "weak band (○)" for a T4–T6-only basis becomes "the code marker by tier (tier-system §5)" | W |
| governance/evidence-methodology.md | 96, 297, 408, 409* | Point to §0; "the hierarchy adjudicates" becomes "the tier grades the marker" | R |
| same | 144, 289, §2.3 richness | Convergence voice and the code-only state: inside T-068's caller sweep | R (in T-068) |
| governance/mission-and-epistemics.md | 42, 46, 107, 149, 177 | Commitment 2 and Test 3 point to §0; "specifies the evidence-based value" becomes "shows the most accommodating identified value with its citation" | R |
| same | 132 | "Which dimension governs" becomes: the most accommodating value stands unless a source shows it leads to worse results; the divergence stays visible | R |
| same | 44 | Full-strength anchor list | W |
| governance/tier-system.md | 20, 21 | T4 and T5 values are eligible like any other; tier sets weight and marker | R |
| same | 49 (and 22 if it carries the glyph) | The superseded banner's ⚠ becomes the word "Superseded" (⚠ is now a marker) | R |
| same | 100, §5 table | Apply the U7 table | W |
| governance/adversarial-use-framework.md | 23, 29, 31, 85 | Lines 29 and 85 contradict each other inside the file; both point to §0 | R |
| governance/jurisdiction-philosophy.md | 74, 75*, 76 | "A code value does NOT establish best practice" becomes "best only where a cell's values are all code, or under the harm test"; line 75's ranking by jurisdiction count is the mode's significance, not best | R |
| governance/legal-regulatory.md | 29, 89 | Show the four figures; "recommendations" becomes "cited values" | R |
| governance/co1-operational.md | 149 | "the converged best-practice value" becomes "the most common identified value" | R |
| governance/grounds.md, held-tensions.md | 125; 300 | One meaning; point to §0 | R |
| governance/pipeline-contract.yaml | 253, 286 | Band for a T4 basis | W |
| governance/audience-priority.md | 80 | Reclassified to LEAVE: "specifies the evidence-based aspiration" is stating the ideal | n/a |
| CLAUDE.md §6 | marker line | "○ grey, thin or unverified" becomes the U7 table with ⚠ | W |
| CLAUDE.md §6; governance/{adversarial-use-framework, doctrine-recheck, evidence-methodology, jurisdiction-philosophy, migration-survival, pipeline-contract}; skills/{multilingual-research, research-log-manager} | "best_practice_synthesis" | A prose caller of a table not in the schema (`sqlite_master` holds `v_best_practice` and `v_code_floor_only`); becomes `specifications` (`v_best_practice`) | R |
| references/methodology-evidence-hierarchy-mapping.md | 33, 39, 58, 182; 165 | The code stratum is where the minimum comes from; its values are eligible; 165 waits | R; W |
| references/methodology/economics-methodology-core.md | 21–23 | "Best practice based on [N] jurisdictions" becomes the mode; "Tier 0/1/2" become the design-mode names | R |
| workplan/2026-10-30-ramp-spec-pages/RENDER-CONTRACT-parameters-3-and-12.md | 30, 41 | 30: pointer to §0; 41: replace "OR-4" with the harm test; "the guidebook's own choice" now stands (the determination ruling) | R |
| workplan/2026-11-12-bidirectional-pipeline/OWNER-SHEET-PLAIN.md | 72 | Code-only best is now allowed, with its marker; fix before the owner reads OD-48 | R |
| workplan/2026-11-12-bidirectional-pipeline/tasks/T-059-wp-t4-agreement.md | 44 | OR-4 and OR-6c become the harm test for selection; OR-6/6b statuses unchanged | R |
| skills/prose-style-checker_SKILL.md | 6, 53, 61, 100; 27, 31–37 | The four-rung ladder becomes direction order, each value cited, no "acceptable"; "to be + [value]" voice waits on Q4 | R (T-035); Q4 |
| skills/voice-style_SKILL.md | 215, 229, 243; unflagged 209, 210, 212, 218, 236, 237, 239, 251, 256, 328 | Remove "this guidebook recommends", "treats X as mandatory", "Population-Mode default: 33 mm"; 215 must not keep "recommended"; re-read each unflagged line first | R (T-035) |
| skills/research-log-manager_SKILL.md | 6, 52, 133, 177, 179 | Remove the "BPC governs" and item-specification-writer flows (that skill is absent from `skills/`) | R (T-035) |
| skills/supersession-audit_SKILL.md | 19 | Point to the ledger entry superseding DR-2026-05-24 | R (T-035) |
| workplan/pipeline-state-graph/ | atoms: ent 306, 308; evi 20, 23, 35, 273, 328, 373, 407; led1 9, 13, 14, 18; prc 16; conflicts.yaml 2 records (incl. :34); machines.yaml:277 | Take G's edits, with "○" changed to "code marker"; re-quote atoms whose governance source changes (`verify_atoms.py` checks quotes verbatim); add ADD atoms quoting the ledger | R; T4 limb W |
| same, generated | ATOMS.tsv ×11, AMBIGUITIES.tsv ×2, CONFLICTS.md, STATE-GRAPH.md | Never edit by hand; rebuild with `build_graph.py` | R |

\* = flagged by no sweep; read by the unifier or an adjudicator.

**R. How the adjudicators were reconciled.**
1. Seven AMEND/TOOL replacements put a code-only best at "○" or "the empty circle"; after "T4 only half circle" that is wrong for a T4 basis: all become "its code marker by tier".
2. A, E and G disagreed on the mixed cell (a code value more accommodating than every research value): the harm test settles it (code wins unless research shows worse results).
3. A and F read OR-6c as still governing selection; the harm-test entry says it resolves OR-4 and OR-6c for selection; OR-6 and OR-6b keep their status words.
4. F's RENDER-CONTRACT:41 and A's audience-priority:80 rested partly on "authority" verbs; under the determination ruling, choosing which value to showcase is the determination's own act; only design verdicts remain conflicts.
5. G says EVI-184 settles the floor dispute; consistent with C's finding that the engine strings misname the most accommodating code value a "floor claim"; both kept.
6. D and E both ask for the frozen corpora to be superseded file by file; collapsed to one ledger entry per corpus (section 3).

## 3. Supersession entries

**How the audit reads a SUPERSEDES line** (`scripts/audit/supersession_backpointer_audit.py`; grammar in `dbcore.LEDGER_SUPERSEDES_RE`): the line is `SUPERSEDES: <one path> :: "<quote>"`, followed by `BY: references/project-standards.md :: "<quote>"`; the target quote must occur exactly once in the target file; the BY quote must occur exactly once in the ledger's prose; the target's paragraph, or the one after it, must carry a marker naming SUPERSEDED or AMENDED together with the BY quote. So there are no globs, and every machine pair needs a marker line written into its target. The audit is advisory and reads only the ledger and `decisions/*.md`.

**One ledger entry**, "Unification 2026-11-14 — best, most common, minimum; showing and grading", with a BY sentence unique in the ledger (for example "the figures of a cell are read under evidence-architecture §0 from 2026-11-14"):

(a) **Machine pairs, each with a marker appended after the target paragraph** (decisions/ records a live reader still reaches): DR-2026-05-24-best-practice-supersession-protocol.md :12, :14, :85; DR-2026-05-26-gap-driven-mining-protocol.md:126*; DR-2026-07-12-evidence-architecture-unification.md:24; DR-2026-07-12-evidence-cell-state-schema-reconciliation.md:22, :29; DR-2026-07-13-value-genealogy-and-derivation-handshake.md:21; DR-2026-07-20-intra-category-cross-test.md:93; DR-2026-07-21-evidence-architecture-option-a-execution.md:130, :132 (and :15, :24, :75 when the table is applied); DR-2026-07-20-…-weighted-strength-reconciliation.md:43 (W); DR-2026-07-21-product-posture-thinking-tool-not-authority.md:66 ("the practice the evidence best supports"); RATIFICATION-PACKAGE-2026-07-12.md:8, :45. Posture DR:45 is **not** superseded (the determination ruling answers it). Touching `decisions/` requires `attestations/<slug>.json` (rule 2).

(b) **Prose-only supersession** (no globs, no marker): `references/bpc/**` (102 records; already FROZEN or RETRACTED); `references/audits/bpc-audit-pass0-2026-05-10.md`, `…pass2-2026-05-10.md`; `references/connections/**`; `references/fdr/reach-range-and-accessible-controls.md`; `references/systematic-reviews/dd1-ndv-qualitative-dd7-umbrella.md`; `references/methodology/economics-research-methodology-v1.9-archived.md`; workplan: `2026-08-11-remediation-and-pipeline-anatomy.md` (including I3 lines 4886, 4888, 5253, 5625, 6522, W), `2026-08-12-commit-91-adversarial-review.md`, `2026-08-18-research-frame-proposal.md`, `2026-08-20-provenance-walk-execution-plan.md`, `2026-10-30-ramp-spec-pages/{owner-rules/code-baselines-accepted.md, owner-rules/spec-page-requirements.md, reports/spec-page-design-requirements-2026-10-29.md, reports/stress-test-ramp-slopes-2026-10-29__report.md}`, `2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS-2-REVIEW.md`, `best-practices-assessment-system.md`, `methodology-and-pipeline-enforcement-plan-2026-07-23.md`, `next-steps-synthesis-2026-07-14.md`, `phase-e-execution-plan-v1.md`; the three attestations F names (frozen JSON); `governance/mission-PROVISIONAL.md` (superseded, no banner), `governance/pre-stage-a-decisions.md`; `governance/doctrine-deltas.json`: append a new state when commitment 2 is amended, do not supersede it.

(c) **Ledger rules and migration rows, which can only be superseded** (the ledger is append-only, so no marker can sit beside its targets; migrations are immutable): `project-standards.md` lines 14 ("median as default"), 17, 20, 23, 26, 142, 172, 355, 3611, 3944; OR-4 (4689; 4706 ACTION 3); OR-6c, as to selection only; `057_baseline_2026-08-12.sql` decisions D-0004, D-0005 (only the clause "solely from code … in error"), D-0042, D-0076. These four rows stay `ACTIVE` in `decisions` (verified), because no writer exists (TT-6).

(d) **State-graph atoms** are corrected by the instrument's own `status_corrections`, not by the ledger.

Governance passages amended in place need no pair: the old quote is gone, `git log -p` keeps it, and an "Amended 2026-11-14 (ledger: <heading>)" note in the file points to the ledger.

## 4. Tooling tasks (each in its own tooling PR, rule 10)

Next free task number: **T-117** (highest existing T-116, by `ls tasks | grep -oE '^T-[0-9]+' | sort -u | tail -1` and `git grep -ohE '\bT-1[1-9][0-9]\b' -- workplan`).

- **TT-1 → joins T-068.** Rewrite the engine strings in `scripts/assess/assess_cell.py` at 1389 ("FLOOR CLAIM"), 1480, 1488, 1506, 1509 to C's replacements (code-sourced best; agreement is the mode). Line 1469 waits on Q1 (⚠ for the proxy derives from `rests_on_proxy_inference`). Also rewrite one string at `scripts/audit/adjudication_integrity.py:92`, false since migration 117 let code-only rows into `v_best_practice`. Read by: the `basis`, `absent` and `falsification` text stored on specification rows, and render. Without it the book prints "a floor claim, never best practice" on a code-only cell's best. Strings only; depends on PR-2.
- **TT-2 → joins T-059.** Selection becomes the most accommodating identified value across all tiers, replaced only when a source's `source_value_extractions.harm_finding`, or an `extraction_relations` row marking `insufficient`, exists for the same lens and context; only values whose lens matches the cell are compared (OD-47 still open). Read by: the specification value and render. Without it a more accommodating code value is hidden behind a less accommodating research value. Makes the anchoring-only selection branch and the special path for regulatory-only cells deletable as separate cases. Depends on Q2 for which findings count; can be built with "any recorded finding" as the default.
- **TT-3 → new T-117, apply the marker table.** In `band()`: T3 clinical → PARTIAL, T3 grey → PARTIAL, T5 → WEAK. Delete the override for regulatory-only cells at `assess_cell.py:1659–1660` (`band()` already gives T4 PARTIAL, so this one deletion is enough for "T4 only half circle"). A migration relaxes CHECK 116 (`regulatory_stratum_only = 0 OR marker = '○'` becomes `marker <> '●'`) and adds '⚠' to the marker vocabulary. Derive ⚠ from `evidence_type` (grey), `verification_status` (UNVERIFIED), and thin from `evidence_population_match.match_grade` PROXY plus `rests_on_proxy_inference`. The W rows of section 2 ship in the same PR. Without it, T4-only cells show ○ and grey or project-inferred values show a circle that claims a derivation. Replaces the special case for regulatory-only cells. Depends on Q1 and Q3.
- **TT-4 → joins T-035.** The skills rows of section 2. The voice line (prose-style 27) depends on Q4.
- **TT-5 → no tooling task.** The state-graph edits are data in an unregistered instrument and ship with PR-2. Do not register it as a check.
- **TT-6 → file a GAP; do not build.** `scripts/db.py` has no writer for `decisions.status` (only a comment at 1284). The only reader is `skills/doctrine-recheck_SKILL.md:39`, which filters `PROVISIONAL`. Nothing reads the ACTIVE rows, so nothing wrong reaches the book, and the ledger supersession is enough (rule 8).
- **TT-7 → new T-118, bring stage tools under the specification stage's name (owner has not ruled on doing it now).** Objects: the table `determination_gates`; the views `v_open_determination_gates` and `v_determination_provenance`; the functions `dbcore.determinations_resting_on`, `dbcore.live_determinations_linked`, `db.py raise_determination_gate`/`resolve_determination_gate`, `assess_cell.stale_determinations`. Callers: 53 files by `git grep -l -i -E 'determination_gates|v_determination_provenance|determinations_resting_on|v_open_determination_gates' -- ':!scripts/migrations/data_*' ':!scratchpad' ':!transcripts'`; sweep views, skills and the registry (rule 4; run `--selftest`); leave frozen workplan prose; no aliases (default). Derived from `stage-map.yaml`: the only table names carrying another stage's word, or "determination", are `determination_gates` (specification) and `evidence_population_match` (judgment); the map holds no views, so view stages are unjudged. Wrong thing reaching the book without it: none (internal names). **Recommend deferring** until T-068, T-059 and T-117 have landed (same files), then one migration with the caller sweep (rule 8; minimise-code ruling).
- **Checks: add none.** `supersession_backpointer_audit` covers (a). T-068's test guards that convergence does not affect selection. The CHECK 116 change guards markers. A new check here would be apparatus with no book-facing defect.

## 5. Delete list

- `references/connections/application-queue.md`: its only readers are `sessions/` records; nothing in scripts, skills or `.claude` reads it; it queues work for a skill absent from `skills/`, against the dropped item layer.
- `references/website/data/populations.json`: read only by `_archived/scripts/*` and by prose in `architecture/schema-reconciliation.md` and `references/website/schema/unified-data-schema.md`; no script, `.github` or skill reads `references/website`; its values carry no citations. Move to `_archived/` (content, not code) and fix the two prose callers.
- `references/bpc/_template.md`: referenced only by frozen records and one frozen bpc file; no live skill creates BPC files (DR-2026-08-19 §1.4 quarantine). Delete rather than amend.
- The BPC flows in `research-log-manager` that feed item-specification-writer: delete under TT-4.

## 6. Held and owner questions

**Resolved from the rulings (no owner needed):** all 10 OWNER-Q records (harm test: `mission-and-epistemics.md:132`, `project-standards.md:4689` and `:4706`, `T-059:44`, `AMBIGUITIES.tsv:169`, `ATOMS.tsv:1014` and `:1017`, `atoms-evi.jsonl:127` and `:130`; determination ruling: posture DR:45); the T4 question behind the 36 HELD records that cite T4, the circle or the band ("T4 only half circle"; they now wait only on applying the table); the tension "showing data, not determining" against the stage name (the determination ruling); the proxy branch (1469: thin, by "derive thin from the population match and the proxy-inference record"); bpc project inferences (cross-population:27, ms-thermal:24: ⚠ on application); "best practice as currently known" (the marker, not the word, carries provenance; T-037 may drop the qualifier); by default ("whatever"): no aliases, the verb "states the ideal and grades its evidence", the stage stays "specification".

**Still for the owner (Q1 is the only one that blocks code):**
- **Q1.** Apply the circle table now, including lowering T3 clinical from ● to ◐ and replacing ○'s gloss in CLAUDE.md §6? *Recommend yes:* every tier is answered, and §2.2 already holds T3 clinical at `provisional`.
- **Q2.** What proves "worse results"? *Recommend:* a recorded finding from a source that measured the outcome for the same lens and context, at any tier, with that source's marker shown; never a project inference; the tier grades, it does not gate.
- **Q3.** When a cell's sources differ, does the showcased value carry the grade of its own source, or the floor-mean of all sources? *Recommend its own:* "how to grade quality of evidence for it" is about the chosen value; ⚠ applies only when that value's basis is grey, unverified or thin.
- **Q4.** Does the register's "to be + [value]" survive? *Recommend:* keep it for process prose; state values as attributed data.
- **Q5.** Add `references/bpc/` to `.ignore` (owner-gated by DR-2026-08-06)? *Recommend yes:* frozen, quarantined, and it floods every search for "best practice".
- **Q6 (optional; the default stands if unanswered).** Rename "best practice" to "ideal"? *Recommend no rename:* the meaning is fixed, and a rename costs a migration and a caller sweep.
- Render's, not the owner's now: the scope of mode and median (recommend all identified values in the context); OR-6b clusters stay in T-068.

## 7. Sequence

PR-2 and PR-3 can ship now.
1. **PR-1, ledger (governance).** The unification entry plus the (a) machine pairs and their DR markers, and an attestation. Gate: `supersession_backpointer_audit` PASS with EXAMINED up by the number of pairs added; `attestation_presence` and `attestation_schema`; `scripts/preflight.sh`.
2. **PR-2, doctrine (no code).** Section 2's R rows; the CLAUDE.md dead table name; the delete list; atoms re-quoted and rebuilt. Gate: `claude_md_spine`, `schema_reference_audit`, `verify_atoms.py` on each atoms file, `build_graph.py --check`, `run_checks.py --changed-from origin/main`.
3. **PR-3, tooling.** TT-1 and TT-4, then TT-2 after Q2. Gate: `run_checks.py --selftest`, the assess tests, a scratch `migrate_db.py --rebuild`.
4. **PR-4, T-117** (after Q1 and Q3). Migration, `band()`, engine, and the W prose. Gate: rebuild, selftest, `migration_reproducibility_deep`, the UNWRITABLE derivation.
5. **PR-5, research rows.** Re-assess specifications through `db.py`, emit a data migration. Gate: `migration_reproducibility_deep`, the antagonist pass.
6. **PR-6, T-118** (deferred).

Rule 9 for every PR: open it last; call `unsubscribe_pr_activity` immediately after.

## 8. Risks

1. **Harm test and lens.** Code values often carry no lens (OD-47 open); compared against lens-specific research, a generic code value could be showcased as best for a group it never addressed. Compare only values whose lens matches the cell.
2. **"Research wins" taken as the project judging harm.** Only a source's recorded finding may trigger it; a project inference is conjecture (⚠) and cannot.
3. **Applying ◐ to T4** raises some cells' markers: correct under the ruling, but the change must not run before Q1, or the book claims a strength the owner has not released.
4. **Amending governance breaks `verify_atoms.py` quotes.** Re-quote the atoms in the same PR.
5. **Ledger rules can only be superseded in prose**, and the decisions rows stay ACTIVE: a reader of the table or the old ledger lines meets them unmarked. Accepted (rule 8); the GAP records it.
6. **Prose callers are not gated** (rule 4). Re-grep `best_practice_synthesis`, "floor claim", "acceptable" and "Ideal → Best Practice" across `governance/`, `references/`, `architecture/` and `skills/` after PR-2.
7. **Rulings pulling against each other:** OR-6b ("not divergent") against the cluster cue (left with T-068); the minimum stays the T4–T6 stratum while T4 now carries ◐ (compatible, but a reader may conflate them); "gather and show" against the register's subjunctive (Q4).
8. **Hiding a value.** No action here hides one: deletions remove uncited, unread copies, and the harm test keeps both values shown with citations.

## Errata (found while folding the plan into the remediation plan, 2026-11-14; the folded text follows these corrections)

1. **§6 overstates Q1.** It says Q1 is the only question that blocks code; §4 itself makes TT-2 wait on Q2 and TT-3 on Q1 and Q3. Read: Q1 and Q3 gate T-117; Q2 gates the selection change in T-059; Q4 gates only the voice line of T-035; Q5 gates T-121 only.
2. **TT-3's migration is a table rebuild, not an edit.** CHECK 116 was added with `ALTER TABLE specifications ADD COLUMN marker …` (`scripts/migrations/116_specification_marker.sql`, lines 28–30), and SQLite cannot change a column's CHECK in place. Relaxing it and adding ⚠ to the marker vocabulary rebuilds `specifications` (rule 4: its views and callers are swept), under rule 10 in a tooling-only PR.
3. **Line 1469 of `assess_cell.py` belongs to T-117, not TT-1.** It waits on Q1 and TT-1 ships before Q1 is answered.
4. **Conflicts the unifier missed**, resolved in the fold (`TERM-PLAN-FOLD.md` §2): the T068-10 test (it expected "marker ○"), OD-48 option (a) in two files, the dead table name `best_practice_synthesis` in 74 task files, and the convergence wording in the owner sheet.
