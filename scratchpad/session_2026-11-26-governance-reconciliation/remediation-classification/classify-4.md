# Classifier 4: T-130 to T-148 (16 tasks)

Read-only throughout. Repository at `cd34b96` (branch ccr-64231823-gqy3xr; `origin/main` contains every commit cited below). Database `PRAGMA user_version` 167. One scratch copy (`scratchpad/c4.db`) was used for a `--dry-run` only.

Context that bears on several rows: the first published determination is almost certainly **ramp gradient (parameter 3, TERM-001)**. It holds 122 live extractions, eight retired determinations (specifications 1 to 8, the last retired over REF-01002 and GAP-019), and the only open determination gate (gate 1, UNLINKED, trigger REF-01002). No other parameter comes close (`select parameter_id, count(*) from source_value_extractions where retired_at is null group by 1`). "Shortest path" below means the path to a re-determined, rendered ramp-gradient cell.

| id | title | class | element(s) | shortest path? | one-line reason | confidence |
|---|---|---|---|---|---|---|
| T-130 | Consolidation sweep: candidates verb, contract bound, loop | APPARATUS | E3 | n | A loop, a bound in the contract and a candidates verb to find 11 shared forms that one query already lists; none touches parameter 3. DEFER (or RETIRE in favour of T-131 run by hand) | high |
| T-131 | First consolidation pass: every pair judged | NEEDED-LATER | E3, E4 | n | The judging is real work (a homonym "paso libre" is held by door width and corridor width), but none of the 11 pairs involves TERM-001 or TERM-091 | medium |
| T-132 | Drift detectors bind (ratchet to blocking; cron prose) | APPARATUS | E5 | n | Moves an existing advisory check to blocking; no live determination exists. The three false "cron" sentences are a 3-line prose fix, not a task. DEFER the ratchet until a determination is live | high |
| T-133 | Determination record points at map rows; gate tier read through pointer | NEEDED-LATER | E4, E5 | n | Item 1 (the gate's tier read live) can matter for the ramp's own gate; item 2 (junction for `functional_basis`) is rule-5 tidying over a frozen table. An advisory parity check already catches drift | medium |
| T-135 | Domain vocabulary table | APPARATUS | E3 | n | 18 clean domains, no case variants, nothing misfiled; OD-69 is no longer a hold (resolved under delegation, checked). DEFER until a variant appears | high |
| T-136 | Base grounds itself: direction and relation words, no base-to-evidence pointer | NEEDED-LATER | E3 | n | Directions can be set today through the stricter existing route; `term_relations` holds 0 rows; does not backfill parameter 3's unwarranted direction (owner question 7) | medium |
| T-137 | Units and kinds as data; exact bounds | NEEDED-LATER | E2, E5 | n | Length and gradient already hold units; bounds are rendered from exact `value_notations` strings, so the float cells mislead no reader. Needed when a non-ASCII unit spelling or a force/time/colour-temperature parameter is determined | medium |
| T-138 | Lens and figure writers refuse what the rulings forbid | NEEDED-LATER | E1, E3, E5 | n | Each guarded defect can reach the book (an `ALL` group, a false "nothing found", a lens changed under a live cell), but every subject is empty today; item 1 is cheap to pull forward | medium |
| T-139 | Typed amendment register | APPARATUS | E2 | n | Current values are correct; only the history is in prose, and each committed data migration already records every UPDATE. A predecessor register was dropped for having no reader (095). RETIRE | medium |
| T-140 | State-graph binding of atoms to sections | APPARATUS | none | n | An instrument over the plan's own quotes; nothing book-facing reads it, and it is red today regardless (4 failures). RETIRE | high |
| T-141 | Small repairs (items 16 to 63) | APPARATUS | E1, E2 | n | Mostly blank-string CHECKs, refusal classing and cue tuning. The translation guards (45) are already partly in code (reviewer name equal to translator name is refused). DEFER items 47, 61 and 62; RETIRE the rest | medium |
| T-142 | Displayed-name rule (CSA/ISO first, count) | NEEDED-LATER | E3, E6 | n | No attested `instrument` or `other_source` form exists, so the rule has no live subject; a heading is wrong only once attested forms arrive | medium |
| T-143 | Degrees converted by tangent | NEEDED-LATER | E2, E5 | n | The 4 degree figures on parameter 3 are conditions and a finding (tier 1), not governing claims, and every parameter's `quantity_kind` is NULL, so the converter would not fire. The task's own step 0 says stop | high |
| T-145 | Identity, need and ICF triples | ALREADY-DONE-OR-SUPERSEDED | E3 | n | Merged: commit 57fcbf3 (migration 165) and 166; 65 rows in `identity_need_icf`; the verbs exist | high |
| T-147 | ICF hierarchy tooling | ALREADY-DONE-OR-SUPERSEDED | E3 | n | Merged: commit 263baa5 (migration 167), followed by repairs b561ffa and 2b390ef; `import-icf-tree` and `icf-glossary` exist | high |
| T-148 | WHO ICF block tree imported | ALREADY-DONE-OR-SUPERSEDED | E3 | n | Merged: commits 86d714a and 903884b (PR 247). The task's own check (a dry run that adds nothing) prints empty lists apart from `d910–d920`, as expected | high |

## Per-task detail

### T-130: APPARATUS (DEFER, or RETIRE in favour of doing T-131 by hand)
- Evidence: the task's query lists 11 (language, form) pairs held by more than one term (`... group by 1,2 having count(distinct term_id)>1`, 11 rows). `consolidation` is not in the contract (`False`), and `consolidation-candidates` is not a verb (`invalid choice`). The defect named is real today.
- Why apparatus: what it adds is a read verb with four proposer reasons, a re-proposal rule, a `consolidation:` bound held in the contract and a "loop with limited repetitions". The 11 pairs can be judged from the one SELECT above, using the existing `add-term-relation` (kind `distinct` and the rest), plus `merge-term` once T-129 lands. The loop and bound protect against duplicates building up over time, which is a property of the apparatus. Nothing wrong reaches the book if the loop does not exist and someone runs the query when the base grows.
- Delete: the task file, the planned `consolidation:` contract key, the `consolidation-candidates` verb and the T130-01..07 tests. Keep the SELECT as the evidence step of T-131.
- Unlisted dependency: T-129 (`merge-term`) is still open (open-tasks.tsv batch 1).

### T-131: NEEDED-LATER
- Evidence: the 11 pairs are TERM-043/053 and TERM-039/051 (DE seeds); LMB TERM-079/088; MOVE TERM-057/080; OFS TERM-053/054; TALL TERM-061 (headroom clearance, a parameter) and TERM-062; "paso libre" TERM-021 (door width) and TERM-002 (corridor width), both parameters; sensory overload TERM-020/042 in ES, FR and JA; 길찾기 TERM-028/038.
- Wrong thing it prevents: the Spanish form "paso libre" resolving to the wrong one of two parameters (door width or corridor width) when a Spanish figure is filed. That is a wrong figure under a wrong parameter, E3. Filing is a judged act, though, and neither ramp term (TERM-001, TERM-091) is in any pair. It can wait until door-width or corridor-width work begins.
- Its evidence command depends on T-130's verb. Run without that verb, it needs only the SELECT.

### T-132: APPARATUS (DEFER)
- Evidence: `derivation_handshake_integrity` is `advisory`, min_items 1. Live determinations: `select count(*) from specifications where retired_at is null` gives 0. "cron" appears at `derivation_handshake_integrity.py:40`, `assess_cell.py:1837` and `research-contract.yaml:218`. `term_merge_integrity` is not in the registry (it is T-129's, not built).
- No wrong thing reaches the book today: the recompute detector exists and prints. Moving it to blocking changes the gate, not the data. Delete the task file. Ratchet with a one-line registry edit in the batch that writes the first live determination; rule 10 puts that edit in its own tooling PR, so it is a two-line PR. The three cron sentences are false prose (rule 7a, third shape). Fix them inline in any PR that touches those files, with no task needed.

### T-133: NEEDED-LATER (item 1 worth pulling forward; item 2 is apparatus)
- Evidence: the view passes the stored tier through (`'g.trigger_tier' in v_open_determination_gates` gives `True`). Specifications are (8, 8, 0) (all carry `functional_basis`, none live). There is no `specification_map_links`. The one open gate is gate 1, on parameter 3, with trigger REF-01002 stored as tier 1 / clinical. Its live tier is also 1 / clinical, so the copy matches today.
- Item 1: specification 8's retirement note records REF-01002 as "one skim extraction read from a third-party index abstract", with GAP-016 ("read the full text") open. If the full read re-tiers REF-01002, the engine's ladder-inversion guard would decide on the stale copy, which would mean a wrong state or marker on the ramp cell (E5). `derivation_handshake_integrity` item 5, an advisory parity check, already reports exactly this divergence. So the risk is caught, not silent. The fix is a single view recreate, cheap enough to do before the ramp is re-determined.
- Item 2: `functional_basis` is a JSON copy of `identity_icf_map` rows. Under OD-77 (delegated, 2026-11-25) that map is "the mapping meant" and frozen to session additions. Retirements by T-102 are still possible. A stored snapshot of what the engine read is not a wrong thing in the book. This is rule-5 / one-value-per-cell tidying: DEFER.
- Plan defect: T-110 (the first determinations) lists T-133 as a dependency. Only item 1 bears on it.

### T-135: APPARATUS (DEFER)
- Evidence: `check_values(terms.domain)` gives `set()`. The 18 domains in use are clean (no NULL, no case variant: the task's own 12.2 query gave `(0, 94, 0)`). `NON_QUANTITY_DOMAINS` holds 6. The ledger has `OD-69 STATUS: RESOLVED UNDER DELEGATION` / `CHECK: confirmed` (line 8016). Line 8535 calls the generator's block of T-135 on OD-69 "an artefact of how it reads gates", so the open-tasks.tsv status "OWNER: OD-69" is stale.
- The wrong thing it names: a misspelt domain makes a new topic class. That has not happened. Render grouping (T-037) has not landed, and a variant would be visible in the 18-row group-by. The cost is one table, a rebuilt `terms` with seven incoming foreign keys, a new verb and 7 tests. DEFER until a variant actually appears or T-037 needs the grouping. Delete nothing yet.

### T-136: NEEDED-LATER
- Evidence: `base_parameters` holds 10 rows. Two have a direction, (3, lower_is_better) and (12, lower_is_better), both with `direction_ref_id` NULL. Today's `set-parameter-direction` requires an admitted source holding an extraction ("FROM AN ADMITTED SOURCE", db.py:8426). `term_relations` holds 0 rows. `term_aliases` attestation counts are model_seed 1163 and unrecorded 1219.
- Item 1 relaxes a stricter refusal into a quote-plus-locator, as OD-71 requires. A direction can be set correctly today, so no wrong figure follows from not doing it. Items 3 and 4 guard a table with 0 rows. Item 2 removes the saved-file wait on absorbed forms, which matters for displayed names (T-142) and E4 synonyms later.
- Unlisted hold, on the shortest path: parameter 3's direction `lower_is_better` carries no warrant, and its backfill is "open owner question 7 of the 2026-11-06 round-3 adjudication" (`skills/run-pipeline_SKILL.md:115`, `:394`). The direction picks which figure anchors the ramp cell, so this is the one item near T-136 that the first determination needs. T-136 explicitly does not do it. [UNVERIFIED whether a later ledger entry answered question 7; I found only the skill's reference.]

### T-137: NEEDED-LATER
- Evidence: `base_units` has no writer and no warrant cells. Units per kind: gradient 2, length 5, colour_temperature, force, luminous_reflectance and time 0 each. `value_min`/`value_max` are REAL. Specifications 5 to 8 nevertheless carry exact `value_notations` (`"max": "1:20", "exact": true`), which the engine writes from Fractions (assess_cell.py:1647, 2383).
- No wrong figure reaches the book: the float cell is not what a reader sees. A figure in an unregistered spelling is refused (missing), not misconverted. Needed before determining operating force (parameter 6, 11 extractions), colour temperature (parameter 10) or reverberation time (parameter 7), and before any Cyrillic or CJK unit spelling.
- Weak point it closes, worth noting: "a kind is warranted by any quote holding a digit". No parameter has a `quantity_kind` today (`count(quantity_kind)` gives 0), so nothing has been wrongly warranted.

### T-138: NEEDED-LATER
- Evidence: the task file's 2026-11-19 output records no retired figure, no live determination, one open gate, 34 live `ALL` identity links all `carried`, and no merged parameter. I re-ran the gate and live-determination parts and both still hold: gate 1 open, 0 live.
- Each item guards something that can reach the book. Item 1: a figure attached to `ALL` under a non-context basis is the wrong group (E3). Item on withdrawn figures: their scan pair reads "read in full, nothing found", which is a false empty search in the published search log. DR-2026-08-19 section 4 publishes empty searches (E1). Item on lens links: a lens changed under a live cell. Every subject is empty today, so nothing wrong is in the book. Item 1 (one refusal widened to every basis) is cheap and could ride with the first lens-linking batch. The `_REGULATORY_FROM_TIER` literal-`4` cleanup is apparatus.

### T-139: APPARATUS (RETIRE)
- Evidence: the task file reports 14 `append_dated_note(` callers and nine amending verbs. No amendment table exists (095 dropped the previous one for having no reader).
- Current values are correct in their cells. Only the before-value lives in a prose trailer. Each amendment reaches the canonical DB only through a committed, append-only `data_*.sql` migration (CLAUDE.md rule 3), so the question "what did this batch change, and what did the cell say before" already has a typed answer: the migration diff and a replay. The task adds a cross-stage table, a helper, a required `--judge` on nine verbs and their callers. Under section 8 the wrong thing is about the record, not the book. Delete the task file. If the owner's 2026-11-06 schema-shape ruling is read as requiring the prose trailers removed, the smaller act is to stop writing the trailers (the migration holds the history). That is an OWNER question only if someone disputes it.

### T-140: APPARATUS (RETIRE)
- Evidence: `build_graph.py --check` today prints `4 failure(s), 5 warning(s), 112 moved` (EVI-055 and EVI-058 are quotes no longer found in `governance/tier-system.md`). It is registered only as a tooling path (`governance/check-registry.yaml:43-44`).
- The state graph is a check on the plan's own quotations of rulings. No guidebook figure, group, source or marker passes through it. It is already red on main, so it is the "red by construction" check rule 6 warns about. Delete T-140, and consider deleting T-134's and T-120's atom-maintenance obligations with the instrument itself. That last step is outside my assignment; it is a recommendation only.

### T-141: APPARATUS (DEFER 47, 61, 62; RETIRE the rest)
- Evidence: `review_translation` already refuses a reviewer whose name equals the translator's (`db.py:14566`). There is no `translated_by_session` cell, so item 45 adds a session-equality check beside the name check. `translation_number_gaps` (`db.py:14366`) compares numbers only, with no comparator or unit. Translations stand at 197 reviewed and 14 rejected.
- Item 47 (a comparator or unit flipped in a translation) is the only one close to "a wrong figure shown to the owner in English". A required review by a different Opus instance (OD-30) already stands between a translation and the reader, so the mechanical check is a second gate. Item 61 (the engine guessing a successor pointer) and item 62 (NULL language read as English, which could skip a translation request) touch E2/E5 history and translation coverage. Defer them. Items 16, 40, 42, 43, 46, 48 to 53 and 57 are blank-string CHECKs, refusal classing, cue tuning and vocabulary tables, with no book-facing wrong thing. Item 63 is blocked by its own text. Recommend splitting out 47 and 62 if anything is kept.

### T-142: NEEDED-LATER
- Evidence: the task's own command was run 2026-11-19. My re-check of the attestation counts (model_seed 1163, unrecorded 1219, none `instrument` or `other_source`) confirms its first figure is still 0. So `v_term_names` falls back as before, and no concept is renamed by `MIN(form_id)` today.
- A wrong displayed name (a book heading) becomes possible only once attested forms are recorded (T-136 item 2, T-107). It adds a base table of issuing bodies, three columns and a retire verb on `term_aliases`, and a counting rule. It is heavy for a rule with no subject. Revisit when the first attested forms land, and consider whether a judge's `rename-term` alone suffices at this scale.

### T-143: NEEDED-LATER
- Evidence: there are 4 live degree figures (extractions 11, 12, 46, 47), all on parameter 3, from tier-1 sources. Their roles are condition, condition, condition and finding, with claim type range. None is a governing claim. No `degrees` unit or `add-unit` verb exists. `select count(*), count(quantity_kind) from base_parameters` gives `(10, 0)`, so by the task's own item 2a the converter would leave every degree figure standing alone even if built.
- Not on the ramp's shortest path: governing claims decide the ramp value, and none is in degrees. The task's own step 0 stops it until T-137 and T-059 are merged.
- Unlisted dependency: a `quantity_kind` for parameter 3 (gradient) must be set, with its warrant, before this task does anything.

### T-145: ALREADY-DONE-OR-SUPERSEDED
- `git log origin/main` contains 57fcbf3 "the judged identity, need and ICF matrix (T-145, migration 165)" and 3c601e3 (its critic). Migrations 165 and 166 are present. `select count(*) from identity_need_icf` gives 65. The verbs `propose-identity-need-icf`, `review-identity-need-icf` and `lens-crosswalk` are at db.py:2384 and 2412. The task file's own banner reads "ANSWERED 2026-11-20 and BUILT". Ledger line 8535 confirms it merged in PR 244. The open-task list is wrong.

### T-147: ALREADY-DONE-OR-SUPERSEDED
- 263baa5 "ICF hierarchy tooling, migration 167, family helper for the ICF lens, import-icf-tree and icf-glossary", then b561ffa and 2b390ef (the repairs), all on `origin/main`. `user_version` is 167. `base_icf` has 136 rows, 105 with a parent, 68 ranges. `import-icf-tree` and `icf-glossary` are at db.py:2750 and 2758. The task file still carries no "built" banner, which is why the generator missed it.

### T-148: ALREADY-DONE-OR-SUPERSEDED
- 86d714a and 903884b on `origin/main` (merged in PR 247, 4645a61). The task's own re-derivation, `import-icf-tree --payload retrieval-log/session_2026-11-22-icf-umbrella-glossary/38776b09204984dc.zip --dry-run` on a scratch copy, prints empty `inserted`, `parented`, `reparented`, `titled`, `replaced`, `confirmed` and `refused` lists, with `unmatched: ["d910–d920"]`, which the task says is expected (OD-74). Its follow-ons T-149 and T-150 (OD-88, all 3-digit categories) are separate tasks and not assigned to me.

## Not reached / unverified
- I did not read every line of T-136 to T-143 past their sections 3 and 4, nor the T-129 design file.
- I did not check whether "open owner question 7" (the warrant for parameter 3's direction) has since been answered. [UNVERIFIED]
- T-138: I took the item-by-item subject counts from the task file's 2026-11-19 output and re-ran only the open-gate and live-determination parts.

## Summary
Counts by class, derived by `grep -E '^\| T-1' classify-4.md | awk -F'|' '{gsub(/ /,"",$4);print $4}' | sort | uniq -c`: APPARATUS 6, NEEDED-LATER 7, ALREADY-DONE-OR-SUPERSEDED 3, NEEDED-NOW 0, OWNER-HOLD 0.

None of these 16 tasks is on the shortest path to a published ramp-gradient determination. T-145, T-147 and T-148 have merged, and the open-task list is stale on them. T-140, T-139, T-132, T-135, T-130 and most of T-141 are machinery: retire or defer.

The critical few:
1. T-133 item 1 alone, one view change, because the ramp's only open gate rests on REF-01002, which the full-text read (GAP-016) may re-tier.
2. T-138 item 1, the `ALL` refusal.
3. A hold none of these tasks covers: parameter 3's unwarranted `lower_is_better` direction (owner question 7), which decides which ramp figure governs.
