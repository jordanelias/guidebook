# Simplification workplan — delete first, repair by stage, build only what remains

**Status:** PROPOSED (rulings in §4 open) · **Date:** 2026-10-12 · **Scope:** Layer 0–2 apparatus. No research content; no doctrine change except where a step says *owner*.
**Reader:** the owner, then whoever executes a step. **Self-retiring:** delete this file when Phase 6 closes; git history is the archive.
**Basis:** the stage graph (`workplan/pipeline-state-graph/`: `STATE-GRAPH.md`, `CONFLICTS.md`, `CAPABILITIES.md`, `build_graph.py`), measured on 2026-10-12. Every figure is a result of the command beside it unless marked *estimate*; re-run before quoting (CLAUDE.md rule 7a). Rulings are named by their words here, not by coined labels, because the ledger already uses D4–D13 for other questions.

---

## 1. The aim, and the measure

The owner's direction: as little code as possible, because every extra line is a place for a conflict, an error or a stale claim. This plan (a) deletes what is dead, with evidence, (b) repairs what is left in the stage graph's order, (c) builds the smallest thing that satisfies a ruling, and (d) makes growth cost something.

**Budget metric.** Physical lines of tracked scripts, tools, schemas, workflows and skills. A step is *done* when its rows fall or stay level and the probes it names pass.

| area | lines | command |
|---|---:|---|
| `scripts/` (py + sh) | 46,510 | `git ls-files 'scripts/*.py' 'scripts/**/*.py' 'scripts/*.sh' \| xargs cat \| wc -l` |
| of which `scripts/audit/` (checks) | 12,575 | `git ls-files 'scripts/audit/*.py' \| xargs cat \| wc -l` |
| of which `db.py` + `dbcore.py` | 10,618 | `cat scripts/db.py scripts/dbcore.py \| wc -l` |
| of which `scripts/tests/` | 6,398 | `git ls-files 'scripts/tests/*.py' \| xargs cat \| wc -l` |
| of which `scripts/generate/` + `generate_parts.py` | 2,438 | `git ls-files 'scripts/generate/*.py' scripts/generate_parts.py \| xargs cat \| wc -l` |
| `tools/*.py` | 5,053 | `git ls-files 'tools/*.py' \| xargs cat \| wc -l` |
| `schemas/*.py` | 5,698 | `git ls-files 'schemas/*.py' \| xargs cat \| wc -l` |
| `governance/check-registry.yaml` | 2,525 | `wc -l governance/check-registry.yaml` |
| active skills | 9,871 | `cat skills/*_SKILL.md \| wc -l` |
| `.github/workflows/` | 714 | `cat .github/workflows/*.yml \| wc -l` |
| migrations (immutable history) | 184 files, 20,061 lines | `git ls-files scripts/migrations \| wc -l` |

In the registry, 84 string fields over 300 characters occupy 1,137 of 2,525 lines; 72 of them (1,044 lines) sit under `note`, `floor_basis`, `reason` and `prior_note`, which CLAUDE.md says belong in commit messages (command: §9, "Registry prose").

**Usage evidence** (each re-derivable):

- **Verbs.** Of 72 `db.py` verbs, 29 appear in ten or more lines of the 50 session command logs (`scratchpad/*/commands.jsonl`), 12 once lines containing grep, echo, cat, sed or rg are excluded; four appear in none (`add-icf-code`, `conflicts`, `migrate`, `update-conflict`); 23 appear in three lines or fewer (50 under the exclusion). The figure turns on what counts as a run, so 4.1 deletes on need, not on this count. Command: §9, "Verb usage". The logs begin when the hook did.
- **Checks.** A full `python3 scripts/run_checks.py --all` (85 registered; 5 entries in `quarantine:`) gave 68 green, 7 examined nothing, 10 advisory red on the latest run, and 65, 10, 10 on an earlier one: the green and examined-nothing counts move because session-scoped gates examine only what the session wrote. The red set did not move: `migration_reproducibility_deep`, `validate_schema_cross_check`, `validate_pydantic_schemas`, `retired_vocabulary`, `research_protocol_audit`, `metadata_integrity_audit`, `validate_reasoning`, `context_map_fresh`, `site_pages_fresh`, `source_locators_integrity`. All reds are advisory, which is how they stay red.
- **Tables.** 47 of 82 tables hold rows. 19 NOT NULL foreign keys point into emptied tables; 16 of those no verb can write (`P-UNWRITABLE`). 14 foreign keys point forward along the spine (`P-FWD-FK`).
- **One parameter has data.** 101 extractions, 1 distinct `parameter_id`, 10 parameters minted.

---

## 2. Prune or rebuild?

The owner asked whether a streamlined rebuild is needed again.

| option | what it is | verdict |
|---|---|---|
| **A. Prune in place** | Phases 1–4: delete the dead, repair the rest, keep the proven writers | **Do.** It is the first half of every option. |
| **B. Re-baseline the migrations** | Replace the 184-file chain with one pruned baseline plus a data snapshot (precedent: migration 057, 2026-08-12) | **Not on present evidence.** `python3 scripts/migrate_db.py --rebuild /tmp/x.db` takes about 1.7 s (1.6 s and 1.8 s on two runs). The 458-row `data_migrations` ledger, the attestations and the session records name migration files, so a re-baseline breaks the provenance chain to save nothing measured. Revisit only if rebuild time or replay fragility becomes a measured cost. |
| **C. Clean-room rewrite of `db.py`, the engine and the checks** | Start again, re-implementing the used verbs | **No.** `db.py`'s value is its refusals (CLAUDE.md §4); they encode the fabricated-author failure of 2026-08-19 and others. Two earlier resets (clean-room 2026-08-06, baseline 2026-08-12) did not stop regrowth, because nothing made growth cost anything; rule R3 below addresses that cause and a rewrite does not. [CONFIDENCE: medium — I could not measure a rewrite's size; the case rests on this argument.] |

**Gate G3** (end of Phase 3): if `db.py` still carries verbs run three times or fewer that no remaining table and no ruling needs, delete them (step 4.1). Only if the file is still the dominant cost after that, reconsider C for `db.py` alone.

---

## 3. Rules every step obeys

- **R1 Evidence and callers in the same change.** A deletion's commit carries the command and its output (CLAUDE.md §8). The sweep (§9, "Caller sweep") covers the name and its import forms, `.github/`, `.claude/`, `governance/*.yaml` (the registry, the contract, `schema-reference-exemptions.yaml`, `known_debt.yaml`), `schemas/`, the skills, views and triggers in `sqlite_master`, the blocking readers (`scripts/tests/test_db_integrity.py`, `schema_reference_audit`) and the prose that names the object. Those edits land in the same PR. **The sweep is run after the deletion, not before:** `schema_reference_audit.py` lists every SQL reader of a dropped table, and `run_checks.py --all` lists every check or fixture that now errors. §5a records what the 2026-10-12 rehearsal found; re-derive it at execution, because it goes stale.
- **R2 Order by the graph.** Children before parents along each foreign key; for repairs, stages in spine order. Where a table's stage-map placement and its foreign keys disagree (`items`), the foreign keys decide.
- **R3 Net-negative.** A PR touching `scripts/`, `tools/`, `schemas/`, `.github/` or `skills/` must not raise the row totals above unless its step names the exception and the code it replaces. Enforced by review, not by new code (CLAUDE.md §8).
- **R4 Done = probes.** Each step names the probes or predicates it must turn `PASS`, or delete with their subject. After each PR: `python3 workplan/pipeline-state-graph/build_graph.py --check`, `run_checks.py --changed-from origin/main --explain`, and `--selftest` after any rename.
- **R5 Rule 10 and rule 9.** Tooling PRs first and merged; the research PR last. One PR at a time, opened last, `unsubscribe_pr_activity` straight after. No history rewriting (`git merge origin/main`, not rebase).
- **R6 Migrations are append-only.** A schema deletion is a new compensating migration. A column that a committed data migration INSERTs is never dropped (rule 5): writer-retire, reader-retire, stop.
- **R7 Antagonist before each PR.** A read-only Fable 5.1 pass on the diff, findings verified against sources before they are applied. A review, not a proof. The ledger bars a pass on a plan or on a pass without a fresh owner commission (LED-068, LED-210; the 2026-10-09 amendment is "for that plan only"). The owner commissioned the passes on this plan in session on 2026-10-12 ("antagonist runs to ensure 100% accuracy"); I found no repository record of that, so step 2.1 records it.
- **R8 Run from the repository root.** The transcript hook writes under the working directory; step 0.4 removes the cause.
- **R9 The instrument shrinks as it works.** A step that resolves a conflict deletes its entry from `conflicts.yaml`; step 0.6 makes the quote check apply only to atoms still cited.

---

## 4. Rulings needed — one sitting

Everything not listed here an agent can execute. Recommended answers are mine, with the evidence. A step marked *owner merge* edits a ratified contract or document.

| ruling | question | evidence | recommended | gates |
|---|---|---|---|---|
| **Render apparatus** | Delete the dashboards (`tools/`), their freshness checks and the five renderers now, and later build one small renderer? Or keep the static stopgap alive? Also: move `specs/e-08-brief.html` (hand-authored, an `E-08` container, the only subject of `render_audit_browser`) to `_archived/`. | Renderers' `specifications` queries fail on the live schema (`P-K`); `regenerate_derived.sh` runs only `tools/*.py` (`P-I`). The only record of "static build now, dynamic later" is a retired migration's comment (atom `ADD-002`): no primary record. Owner words: "dynamic rendering", "do not rely on artifacts". `tools/pipeline_completeness.py` and `tools/evidentiary_audit.py` also back two **blocking** freshness checks. | **Delete**, then one renderer (step 3.R). Please confirm or deny the "static now" claim. | 1.1, 3.R |
| **Scheduled workflows** | Delete `resolve-dois.yml` and `verify-urls.yml` with their scripts? | `pipeline_runs`: 5 runs, `total_resolved` 0 in all, DOI and verified counts unchanged in each; phase-4 enrichment recorded 1, 1, 2 sources in the last three. No source has a NULL `verification_status`; `url_verification_runs` is empty. They are why a PR can inherit a binary DB conflict (rule 3). | **Delete.** First read what phase 4 writes so nothing relied on is lost (an open evidence gap). | 1.5 |
| **Dropping row-bearing retired tables** | LED-169's condition covers "any migration that would empty a table", and its action (4) leaves a row that must leave to the owner, case by case. May these go: `axes` (17 rows), `access_need_axis_map` (21), `population_axis_map` (53), `pipeline_runs` (5)? None has a status column, so retire-in-place is unavailable. The empty tables fall under §8's "dead tables: delete them", which LED-169 leaves standing. | R3 (2026-08-18) retired `axes`; `population_icf_links` already holds the re-derived map; the rows remain in the migrations that created them. | **Yes, all four.** | 1.4, 1.5 |
| **Quarantined gates** | Four gates are quarantined: `register_integrity_check`, `adjudication_integrity`, `code_currency_audit`, `pre_rehab_banner_audit` (and `validate_db` is retired). | The first is red by construction (frozen pilot document). `adjudication_integrity` is green and guards tier derivation, on which every `stated` cell depends (`P-TIER-DERIVE`). The other two are red or stale. | Delete three; **promote** `adjudication_integrity`. | 1.6 |
| **Pydantic mirrors** | CLAUDE.md §4 requires a mirror for each schema change, §7 calls drift a bug, DR-2026-09-26 §1.3 adds one, and the operative instrument's OD-7 approved "schemas mirror SQLite". The check that verifies them is red and uses a curated map that rule 8 names as a violation. Keep the requirement? | `validate_pydantic_schemas`: 213 informational findings, an import error | **Keep the requirement for now**; decide after Phase 1 shows how much remains. Until then neither `schemas/` nor the check is deleted. | 1.6, 4.2 |
| **Doctrine sheet** | Ten yes/no items: (a) mission: delete "teaches professional judgment" (C-001); (b) the two-marker line (C-002); (c) "seven tiers" wording and the tier-number-versus-quality statement (C-006); (d) does the 2026-07-20 directive lift the T3-grey-alone "pending" rule for *state*, or only claim strength (C-004)? (e) record LED-018 as amended by Option A (C-005); (f) Co-1 warrant: D-0178 governs; correct `co1-operational` (C-024/025); (g) jurisdiction §2.3 amendment and its decision record (C-049); (h) append the six session-only rulings to the ledger (C-036); (i) the replacement name for "population", or leave the word where the schema has it (C-018, `P-C`); (j) review D-0184, adopted but never reviewed (C-023). | each item's entry in `CONFLICTS.md` | Per entry; (d), (g) and (i) are the open readings. | 2.1, 2.2 |
| **Medical lens** | Do the 2026-09-11 words ("ensure that medical gets filled out") govern over D-0184's "owner's alone"? | C-022; `P-MEDICAL` | **Yes**, scope "all items presented to me"; run `add-medical` in the research PR. | 5 |
| **Cross-parameter synthesis** | Build a structure relating two parameters? | Only one parameter has extractions. `extraction_relations` already allows an edge between rows of different parameters (0 live). | **Do not build.** Record a gap; revisit when a second parameter has data. This capability stays blocked by design. | C-035, `P-X` |
| **Slug-by-lens coverage** | Is R4's coverage evidenced by logged queries that name the lens term, with no new column or table? | `P-M`; `search_executions.terms_used` | **Yes**; delete the probe and predicate C1.8. | C-033 |
| **Base-vocabulary writers** | Base vocabulary tables with no `db.py` verb are migration-only (doctrine is owner-gated), so LED-182's "add the verb" governs research writes? | `P-O` | **Yes**; delete the probe and predicate C2.8. | C-034 |
| **`not_applicable` state** | Keep the value, unbuilt, flagged as such? | `P-ENG-STATE`: the engine never assigns it | **Keep and flag**; build nothing now. | C-007 |
| **Dead contract criteria** | (a) `locator-title-matches-identifier` (Ruling 2.3): red on 31 clue-store titles, unrepairable without a new writer, though the clue store holds leads, not admitted evidence (LED-082/083). (b) `nine-step-synthesis` and the BPC validators `validate_reasoning`, `validate_bpc`: is the BPC reasoning-document layer a live deliverable? | the full run; 2 of 3 reasoning docs are templates; `reasoning_doc_citations` is empty | (a) retire criterion and check; (b) retire both if no BPC document is in progress. | 1.6 |

The *re-baseline* question in §2 is not on this sheet; the owner may overrule the recommendation.

---

## 5. Sequence

### Phase 0 — Hold the line

| step | change | net | done when |
|---|---|---|---|
| **0.1** | **Branch and session housekeeping.** PR #171 was merged on 2026-10-10 (`merged_at 2026-10-10T02:10:13Z`), so the working branch carries only the instrument and this plan as unmerged content. Done 2026-10-12: `origin/main` merged into the branch (no conflicts); `scratchpad/CURRENT` moved off batch 24's merged session (CLAUDE.md §7). The 666 command-log lines this branch's sessions had written into that merged folder were moved to this session's `commands.jsonl` and the merged folder's log restored (found by the second antagonist pass; uncommitted until the next commit). | 0 | no commit stacks on merged history |
| **0.2** | **Land T1** (owner-approved, LED-206). Its worktree (`/home/user/guidebook-t1`, branch `claude/t1-scan-contract-tooling`, local only) is based on `3077b99`, behind merged `main`, and carries `data/guidebook.db` plus migrations 102–105, so it meets the binary conflict rule 3 describes: merge `origin/main`, take main's blob, run `python3 scripts/migrate_db.py` (the rehearsal in #171's body), resolve the R16 baseline line, regenerate derived outputs. Then commit the stress-tested refactor, run the gate, open the PR, owner merges. **The one sanctioned addition: committed, 23 files of code, +3,426 / −94 lines (`git diff --shortstat 3077b99..HEAD -- scripts schemas tools .github skills ':!scripts/migrations'` in the T1 worktree), plus 364 lines in four migrations; the uncommitted stress-tested refactor is a further 12 files, +386 / −328 (`git diff --shortstat` there)**, its extras beyond items 1–5 still awaiting the owner's accept-or-strike (SES-063). First, so every later `db.py` deletion applies to its final text. | + | `P-V`, `P-W`, `P-PARAM-LIFECYCLE` pass on `main`; C1.3, C1.5, C2.5, C2.6 pass |
| **0.3** | After T1 merges: fix the views `P-H` lists (they name no lifecycle column) in a small tooling PR of their own, since T1 adds `retire-parameter` and `merge-parameter` (LED-171). Not folded into T1: LED-206 item 5 reserves T1's scope to the owner. | ~0 | `P-H` passes |
| **0.4** | `scripts/preserve_transcripts.py`: anchor `OUT` to the repository root (`Path(__file__).resolve().parents[1] / "transcripts"`), not the working directory. | 0 | no `transcripts/` directory appears under a subfolder |
| **0.5** | CLAUDE.md (owner merge): add R3; delete statements the stage graph shows false (C-020 "both sweeps are done"; C-027 "regenerate with `regenerate_derived.sh`"). Each Phase 1 PR also edits the CLAUDE.md lines that name what it deletes (today lines about `resolve-dois.yml`/`pipeline_runs`, `MODEL_TABLE_MAP`, `tools/*.html`, `item_taxonomy_links`, `add-item`; re-find with `git grep` at the time). | − | `git grep` of each deleted name in CLAUDE.md returns nothing |
| **0.6** | Instrument: verify quotes only for atoms a remaining conflict, machine, probe or predicate cites (README step 2's "quotes verified mechanically" then holds for cited atoms only; the README says so); regenerate `context-map.yaml` (`context_map_fresh` is red because the tree changed — it is stale on any tree change). Done in part 2026-10-12: `P-B` and `P-UNWRITABLE` no longer flag lens registries or same-verb pairs. | − | resolved entries stop needing their sources |

### Phase 1 — Delete what is dead

**1.0 Owner rulings that gate Phase 1:** render apparatus, scheduled workflows, dropping row-bearing retired tables, quarantined gates (§4). Steps that edit a ratified contract criterion are *owner merge*. Order below is the dependency order: 1.1 first, because `tools/pipeline_completeness.py:68–200` reads `items`.

| step | delete | evidence to put in the commit | measured lines |
|---|---|---|---:|
| **1.1** | **Render apparatus** (ruling: render). `tools/*.py` (5,053), `regenerate-derived.yml` + `regenerate_derived.sh` (183), the **five renderers** `build_site.py`, `spec_page.py`, `room_page.py`, `pilot_renderings.py`, `generate_parts.py` (1,884); the checks they back: `pipeline_completeness_fresh` and `evidentiary_audit_fresh` (**blocking**), `schema_walkability_fresh`, `pipeline_walk_fresh`, `site_pages_fresh` (advisory); `render_audit_browser` with `render_audit.js`, and `specs/e-08-brief.html` to `_archived/` (ruling); generated `tools/*.html` (5.7 MB), `parts/`, `site/` if frozen. **Keep** `scripts/generate/research_contract_hook.py` (blocking `research_contract_sync`) and `scripts/generate/context_map.py` (`context_map_fresh`): they are not renderers. Same-PR edits: §5a. | `P-I`, `P-K`; `site_pages_fresh` examines 0 | 7,120 |
| **1.2** | **Item-layer cluster, empty tables only.** Tables `items`, `item_audit_runs`, `item_bpc_links`, `item_taxonomy_links`, `item_population_elaborations`, `term_item_links`, `room_items`, `case_study_specs`, `economics_entry_specs`, `spec_value_probes` (+ `probe_population_links`, view `v_pmp_latest_walk`), `jurisdictional_values`. `conflicts` (empty) references `items`: rebuild it without that foreign key (rehearsed; keeps `item_code` as a plain column until the cross-parameter ruling decides the table). Verbs `add-item`, `items`, `add-audit-run`, `update-audit-run`, `audit-runs`, `add-jurisdictional-value`, and `synonyms` (it reads `term_item_links`; appears in 5 log lines, 1 outside grep/echo, so confirm no ruling needs it). Scripts `audit_consolidator.py`, `pmp_audit.py` and the `pmp-strict-termination` criterion (owner merge). Skills `item-audit-pipeline`, `audit-consolidator`, `functional-deficit-auditor`, `economics-auditor`, `question-author`, `progressive-measurement` (its protocol writes `spec_value_probes`); edit `connection-discovery`, `gap-driven-mining`, `evidence-metadata-rehabilitation`, `reasoning-doc-citations`. Same-PR edits: §5a. | all empty; `P-UNWRITABLE`; item-layer hit counts in the skills; owner R1 (item codes bias research) | 484 + 1,587 = 2,071 (+ tables, verbs, DDL: not yet measured) |
| **1.3** | **Splinter and case-study children.** Drop the other four `*_population*` link tables (`case_study_populations`, `citation_population_links`, `economics_entry_populations`, `extraction_population_links`; `probe_population_links` goes in 1.2; `P-A`, ruled LED-132), `case_study_outcomes`, `case_study_strategies`; keep `case_studies` (R12). Same-PR edits: §5a. | 0 rows; their content is extractions with `figure_role=finding` | tables only |
| **1.4** | **Axes retired as one act** (R3, 2026-08-18; DRS-024: not piecemeal; ruling: dropping row-bearing tables). `axes`, `access_need_axis_map`, `population_axis_map`, `situations`, `slugs.serves_axes` (`ALTER TABLE … DROP COLUMN`, SQLite 3.35 or later; rehearsed on 3.45.1), `validate_axes.py` + the `base-demand-vocabulary` criterion (owner merge). `population_icf_links` already replaces the map. Same-PR edits: §5a. | `P-AXIS` | 158 |
| **1.5** | **Scheduled DB-writing workflows** (rulings: scheduled workflows; dropping row-bearing tables). `resolve-dois.yml`, `verify-urls.yml`, `resolve_dois.py`, `verify_urls.py`, `test_url_verifier.py`, `test_verification_pipeline.py`; tables `pipeline_runs`, `url_verification_runs`; shrink `migration_reproducibility`'s exempt list and the `reproducibility-invariant` criterion's text (owner merge); then merge the two reproducibility gates as the operative instrument's OD-9 already approves in principle (deep as the sole, blocking one) if run time allows. | `pipeline_runs` result; empty NULL-verification pool; `P-L` | 2,775 |
| **1.6** | **Checks diet.** Keep a check only if it examined something on the last full run **and** guards something that reaches the book; deleting a check a contract criterion names deletes the criterion too, in one *owner merge* PR. *(a) Named by no criterion that carries a `check:` — delete:* `code_currency_audit` (234), `pre_rehab_banner_audit` (123), `register_integrity_check` (455; the `register-invariants` criterion names it in prose only, `check: null`: edit the prose), `population_integrity_audit` (191), `reasoning_doc_citations_audit` (171). *(b) Named, subject retired:* `validate_axes` (1.4), `pmp_audit` (1.2), `validate_population` (251; rehearsed: its deletion leaves `base-population-vocabulary` broken, so the criterion goes with it, owner merge; delete only if the identity-lens table's own CHECK and FKs already enforce it — confirm first). *(c) Named, red, triage:* `validate_schema_cross_check`, `retired_vocabulary` (86 occurrences at 54 sites; the 12 sites in `tools/*.html` go with 1.1, which took the count to 73 in the rehearsal; the rest are text in `references/`, `workplan/`, `scratchpad/` and `governance/` to fix or exempt, 8 of them in this instrument and plan), `research_protocol_audit`, `metadata_integrity_audit`, and the dead-criteria ruling's two. *Not touched until the Pydantic ruling:* `validate_pydantic_schemas`. *Keep:* the session-scoped gates and `medical_lens_integrity`. Same-PR edits: §5a. | the full-run list; the contract's `check:` fields | 1,174 for (a) |
| **1.7** | **Skills diet.** After 1.2 and 1.5 have landed, delete the skills the "Unreferenced skills" command in §9 prints (no live contract, command, agent, script, hook or registry entry names them; decisions, attestations and `references/skill-registry.md` do not count), and `skills/deprecated/`, with their `.claude/skills` symlinks and their rows in `references/skill-registry.md`. The rehearsal printed 15 skills, 1,834 lines (`structure-auditor` joins the list only once its referrers are deleted). For the rest, keep iff a live reference exists; triage. | the reference sweep | 1,834 + 1,156 = 2,990 |
| **1.8** | **Registry prose.** Delete the `note`, `floor_basis`, `reason`, `prior_note` narratives over 300 characters (72 fields; §9, "Registry prose"); the record is `git log -p`. The 12 `no_floor` narratives (93 lines) stay: `run_checks.py` C8/C9 require them. Behaviour-preserving (rehearsed: `run_checks.py --all` and `--selftest` unchanged). | CLAUDE.md "correction histories do not live here" | 1,044 |

**Measured deletions named above:** 7,423 (1.1: 7,120 + `render_audit.js` 303) + 2,071 + 158 + 2,775 + 1,174 + 2,990 + 1,044 = **17,635 lines**, against T1's +3,426 and a renderer of at most 300. The tables, verbs, DDL and the (b)/(c) triage in 1.2, 1.6 and 1.7 are not yet measured. The old-workplan-directory step was dropped: it is documents, not code, and the operative instrument's OD-6 and OD-8 already approve *moving* them.

### 5a. What the 2026-10-12 rehearsal found

Method: a scratch clone of `afd1879e`; each step's deletions applied cumulatively; a throwaway migration for each table drop (`migrate_db.py` reported 0 data migrations applied each time; `--rebuild` afterwards gave the same table set and row counts); then `run_checks.py --all`, `--selftest` and `schema_reference_audit.py`. Baseline in the clone: 68 green, 7 examined nothing, 10 advisory red. **Only step 1.1's edits were made and run green** (`--all`: no new red; `--selftest`: pass). For the others the table records what the gates flagged; the edits are the plan's work, and their result is not shown.

| step | broke without caller edits | same-PR edits (file@line from `schema_reference_audit`) |
|---|---|---|
| 1.1 | `schema_reference_audit` (blocking; the four `room*` exemptions go stale); `pipeline_completeness_fresh`, `evidentiary_audit_fresh` (blocking; script missing); `schema_walkability_fresh`, `pipeline_walk_fresh`, `site_pages_fresh` | Remove those five registry entries and `render_audit_browser`; remove exemption keys `room`, `room_conflict`, `room_dar_provision`, `room_item_population`; edit the contract's `render-freshness` criterion (owner merge). Text only, no gate: `scripts/preflight.sh:22,103`, `.ignore:115`, `CLAUDE.md:459`, comments in `dbcore.py`, `db.py`, `context_map.py`, `research_contract_hook.py`, `column_vocabulary_audit.py`, `migration_reproducibility.py`. |
| 1.2 | `test_db_integrity` (blocking; crashes at `:101`); `schema_reference_audit` (blocking; 42 references to 8 names); `pipeline_contract_audit` (`pmp-strict-termination` broken); `test_pipeline_contract`; `test_graph_audit` (selftest reads `items`); `test_db_amend_writers` X01 and X08 (collateral of the `test_db_integrity` crash); `population_integrity_audit` | `test_db_integrity.py` `:101–116`, `:136`, `:139`, `:173`, `:176`, `:540`; `db.py` `:1038`, `:1176`, `:1208`, `:1213`, `:9007`; `audit/graph_audit.py` `:358`, `:395–409`; `audit/graph/extract_db.py` `:138`, `:156`, `:175`; `adherence_log_audit.py:353`; `gap_mining_audit.py:142`; `skills/progressive-measurement_SKILL.md:132`; the `pmp-strict-termination` criterion; `pipeline_contract_audit.py` fixtures `:256` and `:265` (name `pmp_audit.py` and `pre_rehab_banner_audit.py`; re-point at surviving checks); `test_db_amend_writers.py` J10 when `insert_jurisdictional_value` goes; the `specification` exemption key (stale once `question-author` goes). |
| 1.3 | `graph_audit` warns that mission-critical `extraction_population_links` is absent and that its known-debt entry is unverifiable; the verdict stays PASS | `scripts/audit/graph/known_debt.yaml:43–48`; `scripts/audit/graph/topology.py:31` (`MISSION_CRITICAL`, a curated list: rule 8) and, for 1.2, `STATE_DIST["items"]`. (`test_db_integrity` has no reference to a 1.3 table.) |
| 1.4 | `validate_axes` errors (script missing); `base-demand-vocabulary` broken | registry entry; the criterion (owner merge); `test_db_integrity.py:118`. |
| 1.5 | `test_url_verifier`, `test_verification_pipeline` error (script missing); `test_db_integrity` | registry entries; `test_db_integrity.py` `:912`, `:956–981`; the exempt list in `migration_reproducibility.py` and the `reproducibility-invariant` criterion's text (owner merge); `dbcore.py` `NOT_CAPTURED["pipeline_runs"]` (a stale key; the selftest checks reasons, not existence). |
| 1.6 | `base-population-vocabulary` broken after `validate_population`; quarantined entries gone | registry entries; the criterion (owner merge); `register_integrity_check.py` imports `pilot_renderings` (both go; no gate). |
| 1.7, 1.8 | nothing | `references/skill-registry.md` rows for deleted skills. |

### Phase 2 — Rulings to text

| step | change | done when |
|---|---|---|
| **2.1** | Owner answers §4 in one sitting, and records the antagonist commission (R7). | decisions recorded in the ledger (append-only); no agent-authored ruling |
| **2.2** | Apply them by **deleting** stale clauses, not annotating: the methodology's `(parameter × population)` lines, `co1-operational`'s sub-type and verification lists, hand-written counts, the cell-state transition table (the engine recomputes state), mission lines (owner). Add the one-line `BY:` pointers for every entry of `status_corrections` in `conflicts.yaml` (the repo's own supersession mechanism); append the six session-only rulings to the ledger. | every status correction and the document-level conflicts leave `conflicts.yaml` |

### Phase 3 — Repair what remains, along the spine

| stage | change | probes → pass |
|---|---|---|
| **base** | Classify tables in the stage-map (C-011); the word *population* per the doctrine sheet. | `P-AXIS`, `P-C` per the sheet |
| **research** | Slug-by-lens coverage: delete `P-M` and predicate C1.8 if the owner agrees. | — |
| **evidence** | **Stop writing and reading `data_capture_status`:** writer-retire in `insert_extraction` and `derive_extraction`; reader-retire `C06` and `C09` in `test_db_integrity.py` (the queries at `:544–546` and `:676–680`; `C07` reads other columns, though the comment at `db.py:7841` names it) and the prose readers (`governance/pipeline-operations.md`, that comment). **The column stays**: 23 of the 139 committed data migrations INSERT it (`grep -l 'INSERT INTO "evidence_sources"' scripts/migrations/data_*.sql | xargs grep -l data_capture_status | wc -l`), it is `NOT NULL DEFAULT 'pending'` with a CHECK, and a drop needs an `AFTER_DATA` marker and a table rebuild (rule 5, `migrate_db.py:282–310`). The saving is code, not schema; "looked, nothing found" is already a `claim_type=absent` extraction. **Tier input:** stop asking the operator for `--tier` in `add-source` and `amend-source`; derive it from `(evidence_type, scope)` with the existing `derive_tier` (rule 8's own example) and promote `adjudication_integrity`. No view, no column drop (tier is INSERTed by 23 data migrations too). Fix `Co1SourceType` against the live values. | `P-STATUS-WRITERS`, `P-F`, `P-TIER-DERIVE`, `P-CO1-TYPE` |
| **judgment** | Stage-map: `source_value_extractions` → judgment (C-012; owner words LED-106 as adopted). Delete the slug-admission refusal in `insert_extraction` once the render ruling deletes the vetting surface it protected (C-032): the scan contract says slugs guide search only. | `P-STAGE-SVE`, `P-V2` |
| **synthesis** | Nothing built (cross-parameter ruling). Classify the forward foreign keys (`reasoning_doc_citations`, `gaps`) in the stage-map (C-046). | `P-FWD-FK` reviewed |
| **specification** | C-004 per the doctrine sheet (d): if the directive reaches state, change the T3-grey branch of `determine` (a few lines); if not, delete the contradicting prose. `determination_gates` carries `identity_code` only: add the lens columns, or point at the determination (rule 5); decide after a `repo-sweep` of its readers. | `P-GT`, `P-ENG-T3` |
| **render** | **3.R** One renderer (target at most 300 lines) over one view that already carries the marker, strength flag and evidence trail, so the register invariants hold by construction and `register_integrity_check` has nothing left to check. A named exception to R3: it replaces 1.1's renderers. | `P-K`, `P-I`, C4.6–C4.8 |

### Phase 4 — Second-order reduction

| step | change |
|---|---|
| **4.1** | `db.py` and `dbcore.py`: delete verbs run three times or fewer **that no remaining table and no ruling or machine needs** (`decline-parameter`, `supersede-source`, `add-population-icf-link`, `resolve-determination-gate`, `add-icf-code`, `set-icf-title` stay on that test). Re-sweep. Gate G3. |
| **4.2** | `schemas/*.py`: only after the Pydantic ruling. If the requirement is retired, keep the modules the engine imports (`directness`, `tier_derivation`, enums in use) and delete the table mirrors, which are a second home for the schema (rule 5). Evidence: the import graph. |
| **4.3** | Optional comment diet in `db.py` (docstring narrative to commit messages). Behaviour-preserving, large, low value; skip unless review time is available. |

### Phase 5 — Research PR

Only research rows remain. PR #171 already put batch 24 on `main`. Owed from its body: a compensating data migration using T1's `annotate-parameter`, because the note on all nine parameters is false for parameter 12 and restates facts the schema derives (rule 3 forbids editing the first migration). Per the medical-lens ruling, the medical-registry rows through `add-medical`. `research_batch_dod.py` on `scratchpad/CURRENT`. Open last; unsubscribe.

### Phase 6 — Retire the scaffolding

When `conflicts.yaml` is empty: delete `atoms/`, `ATOMS.tsv`, `AMBIGUITIES.tsv`, `OPEN-QUESTIONS.tsv`, `graph.json`, and the quote and conflict code in `build_graph.py`. Keep the derived stage graph and the probes that still test a standing ruling no other gate holds. Delete this file.

---

## 6. The stage graph, by stage

Generated from `graph.json`, the stage-map, the contract and the conflict register. Conflict-to-stage is by judgment (the atoms' own stage tags were too noisy); the last row collects conflicts about records, process and documents that belong to no stage.

| stage | tables | rows | empty | no writer | unwritable | forward FKs from here | verbs writing only here | contract-named check scripts | machines | conflicts | steps |
|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 23 | 2995 | 5 | 15 | 1 | 1 | 8 | 10 | M03 | C-011, C-017, C-018, C-022, C-034, C-049, C-050 | 1.2, 1.3, 1.4, 3 base, 5 |
| research | 11 | 1525 | 4 | 3 | 0 | 4 | 12 | 2 | M01, M09 | C-033 | 3 research |
| evidence | 17 | 460 | 10 | 8 | 6 | 4 | 13 | 3 | M02, M03 | C-006, C-009, C-013, C-015, C-024, C-025, C-026, C-048 | 1.5, 3 evidence |
| judgment | 5 | 132 | 3 | 3 | 2 | 3 | 3 | 2 | M03, M04 | C-012, C-014, C-032 | 0.2, 3 judgment |
| synthesis | 8 | 150 | 5 | 3 | 0 | 1 | 10 | 1 | M07 | C-035, C-046 | 3 synthesis |
| specification | 5 | 198 | 1 | 3 | 1 | 1 | 3 | 3 | M05, M06 | C-003, C-004, C-007, C-008, C-021, C-040 | 3 specification |
| render | 6 | 5 | 5 | 6 | 4 | 0 | 0 | 1 | — | C-005, C-027, C-028, C-031 | 1.1, 3.R |
| infrastructure | 7 | 743 | 2 | 3 | 1 | 0 | 6 | 0 | — | — | 1.5, 1.6 |
| layer 0 / cross | — | — | — | — | — | — | — | — | M08, M10 | C-001, C-002, C-010, C-016, C-019, C-020, C-023, C-029, C-030, C-036, C-037, C-038, C-039, C-041, C-042, C-043, C-044, C-045, C-047 | 0.1–0.6, 1.6–1.8, 2.x, 4.x, 6 |

Regenerate: `python3 workplan/pipeline-state-graph/build_graph.py` (tables, writers, flags, forward FKs), then group by `governance/stage-map.yaml` and the `check:` fields of `governance/pipeline-contract.yaml`. A verb is counted only where every table it writes sits in the stage. The `infrastructure` row is not a spine stage. `unwritable` counts tables no verb can write; `forward FKs from here` counts foreign keys whose child sits in this stage and whose parent sits later in the spine.

---

## 7. Where every issue goes

| step or ruling | conflicts | probes not passing | capability predicates |
|---|---|---|---|
| 0.2 | — | P-V, P-W, P-PARAM-LIFECYCLE | C1.3, C1.5, C2.5, C2.6 |
| 0.2, 3 judgment | C-032 | — | — |
| 0.2; ruling: base-vocabulary writers | C-034 | — | — |
| 0.3 | C-031 | P-H | — |
| 1.1, 3.R | — | P-I | C4.7 |
| 1.2 | C-019, C-026 | — | — |
| 1.2, 1.3, 5 | — | P-UNWRITABLE | — |
| 1.3 | C-020 | P-A | — |
| 1.4 | C-017 | P-AXIS | — |
| 1.5 | — | P-L | — |
| 1.7, 2.2 | C-037 | — | — |
| 2.1 | C-039, C-044 | — | — |
| 2.1 (Co-1), 2.2 | C-024 | — | — |
| 2.1 (D-0184), 2.2 | C-023 | — | — |
| 2.1 (LED-018), 2.2 | C-005 | — | — |
| 2.1 (T3-grey), 3 specification | C-004 | — | — |
| 2.1 (jurisdiction), 2.2 | C-049 | — | — |
| 2.1 (ledger), 2.2 | C-036 | — | — |
| 2.1 (markers), 2.2 | C-002 | — | — |
| 2.1 (mission), 2.2 | C-001 | — | — |
| 2.1 (population word) | — | P-C | — |
| 2.1 (population word), 3 base | C-018 | — | — |
| 2.1 (tier wording), 2.2 | C-006 | — | — |
| 2.2 | C-003, C-008, C-010, C-014, C-015, C-016, C-030, C-038, C-040, C-041, C-042, C-043, C-045, C-047, C-050 | P-LEDGER-GREP | — |
| 2.2, 3 evidence | C-025 | — | — |
| 2.2; ruling: not_applicable | C-007 | — | — |
| 3 base | C-011 | — | — |
| 3 evidence | C-009, C-013, C-048 | P-F, P-CO1-TYPE, P-STATUS-WRITERS | — |
| 3 judgment | C-012 | P-V2, P-STAGE-SVE | C1.4 |
| 3 specification | C-021 | P-B, P-GT | — |
| 3 synthesis | C-046 | P-FWD-FK | — |
| 3.R | — | P-K | C4.6 |
| 5 | — | P-MEDICAL | C1.6 |
| ruling: base-vocabulary writers | — | P-O | — |
| ruling: base-vocabulary writers (predicate deleted) | — | — | C2.8 |
| ruling: cross-parameter | — | P-X | — |
| ruling: cross-parameter (deferred) | C-035 | — | — |
| ruling: cross-parameter (stays failing) | — | — | C3.5 |
| ruling: medical lens; 5 | C-022 | — | — |
| ruling: not_applicable | — | P-ENG-STATE | — |
| ruling: not_applicable (stays failing) | — | — | C4.4 |
| ruling: quarantined gates; 1.6 | — | P-TIER-DERIVE | — |
| ruling: quarantined gates; 1.6, 3.R | C-028 | — | — |
| ruling: quarantined gates; 3.R | — | P-QUARANTINE | C4.8 |
| ruling: render; 1.1, 3.R | C-027 | — | — |
| ruling: scheduled workflows; 1.5 | C-029 | — | — |
| ruling: slug-by-lens | — | P-M | — |
| ruling: slug-by-lens (predicate deleted) | — | — | C1.8 |
| ruling: slug-by-lens; 3 research | C-033 | — | — |

**Status corrections** (the `status_corrections` list in `conflicts.yaml`, 13 entries today: LED-029, LED-018, DRS-039, DRS-040, OPI-229, WRK-003, WRK-033, WRK-171, WRK-172, WRK-004, WRK-173, WRK-043, WRK-068) → step 2.2, as one-line `BY:` pointers.

**Red and empty checks** (§1): `migration_reproducibility_deep` → 1.5; `site_pages_fresh` → 1.1; `context_map_fresh` → 0.6; `validate_schema_cross_check`, `retired_vocabulary`, `research_protocol_audit`, `metadata_integrity_audit` → 1.6(c); `validate_pydantic_schemas` → the Pydantic ruling; `validate_reasoning`, `source_locators_integrity` → the dead-criteria ruling. Examined-nothing: `pmp_audit` → 1.2; `population_integrity_audit`, `reasoning_doc_citations_audit` → 1.6(a); the session-scoped gates and `medical_lens_integrity` stay.

**After the plan, by design:** predicates C3.5 and C4.4 still fail (cross-parameter synthesis deferred; `not_applicable` flagged and unbuilt); C1.8 and C2.8 are deleted with their probes if the owner agrees.

**Process issues:** stray transcript copies under a subfolder → 0.4; T1 refactor uncommitted and its worktree behind merged `main` → 0.2; PR #171 merged and `scratchpad/CURRENT` naming its session → 0.1; probes that tested the wrong function or a comment, over-broad probes, and quote checks that would go red for resolved reasons → 0.6, R9, Phase 6; the stop hook flagging append-only logs → no step (`git config stophook.ignorePath` already excludes `transcripts/` and `*commands.jsonl`; CLAUDE.md §7).

---

## 8. What this plan does not do, and what I could not check

- It decides no ruling. Directions in the register are inferences from rule 0; three independent passes have corrected the register and this plan, and none is proof.
- Line counts are file sizes today. Steps marked *not yet measured* or *triage* depend on a sweep or on reading the check or skill; no step is approved until its sweep is attached.
- **Not checked:** what the cron's phase 4 writes; whether `adherence_log_audit` check 5 fires on current attestations; whether `rename_insurance.py` (275 lines, 7 item-layer hits) is item-layer; whether BPC validators have any live subject; the readers of `determination_gates`; the actual size of a renderer; T1's GitHub state (the branch is local only).
- The 50 command logs begin when the hook did; a verb unused in them may have been used earlier. The command lines also hold greps and echoes that name verbs, so the usage counts bound runs from above.
- §5a is a rehearsal of deletions in a scratch clone with no caller edits (except step 1.1's, which were made and run green): it records which gates went red and which readers `schema_reference_audit` listed. It does not show that the edits, once made, leave every gate green for steps 1.2 to 1.7.
- R3 is a process rule, not a gate; it fails the way every unenforced rule here has.

---

## 9. Commands behind the figures

Run from the repository root.

**Verb usage** (a "run" is a log line containing `scripts/db.py <verb>`; the second figure also drops lines containing grep, echo, cat, sed or rg):

```
python3 - <<'PY'
import json, re, subprocess
verbs = sorted(set(re.findall(r"add_parser\(\s*['\"]([\w-]+)['\"]", open('scripts/db.py').read())))
raw, ex = dict.fromkeys(verbs, 0), dict.fromkeys(verbs, 0)
for f in subprocess.run(['git', 'ls-files', 'scratchpad/*/commands.jsonl'], capture_output=True, text=True).stdout.split():
    for line in open(f):
        c = json.loads(line).get('command', '')
        for v in verbs:
            if re.search(r'scripts/db\.py\s+' + re.escape(v) + r'\b', c):
                raw[v] += 1; ex[v] += not re.search(r'\b(grep|echo|cat|sed|rg)\b', c)
print(len(verbs), sum(n >= 10 for n in raw.values()), sum(n >= 10 for n in ex.values()), [v for v in verbs if not raw[v]], sum(n <= 3 for n in raw.values()))
PY
```

**Registry prose** (fields over 300 characters, by key, as `(count, lines)`):

```
python3 - <<'PY'
import yaml
big = {}
def walk(n):
    if isinstance(n, yaml.MappingNode):
        for k, v in n.value:
            if isinstance(v, yaml.ScalarNode) and len(v.value) > 300:
                big.setdefault(k.value, []).append(v.end_mark.line - v.start_mark.line + 1)
            walk(v)
    elif isinstance(n, yaml.SequenceNode):
        for v in n.value: walk(v)
walk(yaml.compose(open('governance/check-registry.yaml')))
print({k: (len(v), sum(v)) for k, v in big.items()})
PY
```

**Unreferenced skills** (no live contract, command, agent, hook, script, workflow or registry entry names the skill):

```
for f in skills/*_SKILL.md; do s=$(basename $f _SKILL.md); grep -rlqw -- "$s" governance/pipeline-contract.yaml governance/research-contract.yaml governance/check-registry.yaml .claude/commands .claude/agents .claude/settings.json .claude/hooks scripts .github CLAUDE.md || echo "$s $(wc -l < $f)"; done
```

**Caller sweep** (after a deletion; the first line finds names, the other two find what now fails):

```
git grep -lw -e NAME -e NAME2 -- . ':(exclude)transcripts' ':(exclude)scratchpad' ':(exclude)sessions' ':(exclude)_archived' ':(exclude)versions' ':(exclude)audits' ':(exclude)attestations' ':(exclude)decisions' ':(exclude)scripts/migrations'
python3 scripts/audit/schema_reference_audit.py
python3 scripts/run_checks.py --all
```
