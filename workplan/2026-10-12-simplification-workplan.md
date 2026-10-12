# Simplification workplan — delete first, repair by stage, build only what remains

**Status:** PROPOSED · **Date:** 2026-10-12 · **Scope:** Layer 0–2 apparatus. No research content, no doctrine change except where a step is marked *owner*.
**Reader:** the owner, then whoever executes a step. **Self-retiring:** delete this file when Phase 6 closes; git history is the archive.
**Basis:** the stage graph (`workplan/pipeline-state-graph/`: `STATE-GRAPH.md`, `CONFLICTS.md`, `CAPABILITIES.md`, `build_graph.py`), measured on branch tip `acaba88` on 2026-10-12. Every figure below is a result, stamped; the command that regenerates it stands beside it. Re-run before quoting (CLAUDE.md rule 7a).

---

## 1. The aim, and the measure

The owner's direction: as little code as possible, because every extra line is a place for a conflict, an error or a stale claim. This plan therefore (a) deletes what is dead, with evidence, (b) repairs what is left by the stage graph's order, (c) builds the smallest thing that satisfies a ruling, and (d) makes growth cost something.

**Budget metric.** Physical lines of tracked scripts, tools, schemas, workflows and skills. One command per row; the plan's *done* test for any step is that its rows fall or stay level and the named probes pass.

| area | lines | command |
|---|---:|---|
| `scripts/` (py + sh) | 46,510 | `git ls-files 'scripts/*.py' 'scripts/**/*.py' 'scripts/*.sh' \| xargs cat \| wc -l` |
| of which `scripts/audit/` (checks) | 12,575 | `git ls-files 'scripts/audit/*.py' \| xargs cat \| wc -l` |
| of which `db.py` + `dbcore.py` | 10,618 | `cat scripts/db.py scripts/dbcore.py \| wc -l` |
| of which `scripts/tests/` | 6,398 | `git ls-files 'scripts/tests/*.py' \| xargs cat \| wc -l` |
| of which render generators | 2,438 | `git ls-files 'scripts/generate/*.py' scripts/generate_parts.py \| xargs cat \| wc -l` |
| `tools/*.py` (dashboards) | 5,053 | `git ls-files 'tools/*.py' \| xargs cat \| wc -l` |
| `schemas/*.py` | 5,698 | `git ls-files 'schemas/*.py' \| xargs cat \| wc -l` |
| `governance/check-registry.yaml` | 2,525 | `wc -l governance/check-registry.yaml` |
| active skills (`skills/*_SKILL.md`) | 9,871 | `cat skills/*_SKILL.md \| wc -l` |
| `.github/workflows/` | 714 | `cat .github/workflows/*.yml \| wc -l` |
| migrations (immutable history) | 184 files, 20,061 lines | `git ls-files scripts/migrations \| wc -l` |

Roughly three lines in five of the Python are statements; the rest are docstrings and comments (tokenizer count: `scripts/` 61–66%, `db.py` 65%). The registry is mostly prose: 88 KB of its 141 KB sits in string fields over 300 characters, which CLAUDE.md says belong in commit messages.

**Usage evidence** (all re-derivable):

- **Verbs.** Of 72 `db.py` verbs, 35 were run ten or more times across the 49 session command logs; 5 never (`migrate`, `add-icf-code`, `set-icf-title`, `update-conflict`, `conflicts`). Counted from `scratchpad/*/commands.jsonl`, excluding grep/echo/cat lines.
- **Checks.** The last full `run_checks.py --all` (85 registered, 5 quarantined and never selected): 69 green, 7 examined nothing, 9 red. All 9 reds are advisory, which is how they stay red.
- **Tables.** 47 of 82 tables hold rows. 19 NOT NULL foreign keys point into emptied tables (probe `P-UNWRITABLE`). 14 foreign keys point forward along the spine (`P-FWD-FK`).
- **One parameter has data.** 101 extractions, 1 distinct `parameter_id`, 10 parameters minted. Nothing yet exists to synthesize *across* parameters.

---

## 2. Prune or rebuild?

The owner asked whether a streamlined rebuild is needed again. Three options, with what the measurements say:

| option | what it is | verdict |
|---|---|---|
| **A. Prune in place** | Phases 1–4: delete the dead, repair the rest, keep the proven writers | **Do.** It is the common first half of every option. |
| **B. Re-baseline the migrations** | Replace the 184-file replay chain with one pruned baseline plus a data snapshot (precedent: migration 057, 2026-08-12) | **Do not, on present evidence.** `python3 scripts/migrate_db.py --rebuild /tmp/x.db` takes about 1.6 s. The 458-row `data_migrations` ledger, the attestations and the session records name migration files, so a re-baseline breaks the provenance chain to save nothing measured. Revisit only if rebuild time or replay fragility becomes a measured cost. (Decision D4.) |
| **C. Clean-room rewrite of `db.py`, the engine and the checks** | Start again, re-implementing the 35 used verbs | **Do not.** `db.py`'s value is its refusals (CLAUDE.md §4); they encode the fabricated-author failure of 2026-08-19 and several others. A rewrite re-opens each one. Two earlier resets (clean-room 2026-08-06, baseline 2026-08-12) did not stop regrowth, because nothing made growth cost anything. Rule R3 below addresses that cause; a rewrite does not. [CONFIDENCE: medium — I could not measure a rewrite's size; the case rests on this argument.] |

**Gate G3** (end of Phase 3): if `db.py` still carries verbs run three times or fewer that guard nothing the book depends on, delete them (Phase 4); only if the file is still the dominant cost after that, reconsider C for `db.py` alone.

---

## 3. Rules every step obeys

- **R1 Evidence in the commit.** Each deletion's commit message carries the command and its output (CLAUDE.md §8: unreferenced, vacuous, or superseded). A *sweep* means `git grep` for the name **and** the import form (`import x`, `from x`), the stage-map, the registry, the skills, the views in `sqlite_master` (rule 4). My basename-only sweep of 2026-10-12 would have missed a package import; the repo-sweep agent runs the full form.
- **R2 Order by the graph.** Children before parents along each foreign key; stages in spine order for repairs. Where a table's stage-map placement and its foreign keys disagree (`items`), the foreign keys decide the drop order.
- **R3 Net-negative.** A PR touching `scripts/`, `tools/`, `schemas/`, `.github/` or `skills/` must not raise the row totals above, unless its step names the exception and the code it replaces. Enforced by review and the antagonist, not by new code (CLAUDE.md §8: no apparatus about the apparatus).
- **R4 Done = probes.** Each step names the probes or capability predicates it must turn `PASS` (or delete, with their subject). `python3 workplan/pipeline-state-graph/build_graph.py --check` after each PR; `run_checks.py --changed-from origin/main --explain`; `--selftest` after any rename.
- **R5 Rule 10, rule 9.** Tooling PRs first, all merged; the research PR last. One PR at a time, opened last, `unsubscribe_pr_activity` straight after. No history rewriting.
- **R6 Migrations are append-only.** Every schema deletion is a new compensating migration (a `DROP`), never an edit.
- **R7 Antagonist before each PR.** A read-only Fable 5.1 pass on the diff (`antagonist` agent), findings verified against sources before they are applied. It is a review, not a proof. The ledger bars an antagonist pass on a plan or a pass without a fresh owner commission (LED-068, LED-210); the owner has commissioned the passes on this plan.
- **R8 Run from the repository root.** The transcript hook writes under the working directory; step 0.2 removes the cause.
- **R9 The instrument shrinks as it works.** Resolved conflicts are deleted from `conflicts.yaml` in the step that resolves them, and `build_graph.py` verifies quotes only for atoms still cited (step 0.4). A deleted passage then cannot turn the check red for a resolved reason.

---

## 4. Owner decisions — one sitting

Everything not listed here is executable without the owner. Recommended answers are mine, with the evidence.

| id | question | evidence | recommended | unblocks |
|---|---|---|---|---|
| **D1** | Render: delete the dashboards and the seven generators now, and later build one minimal renderer? Or keep the static stopgap alive? | Renderers' `specifications` queries fail on the live schema (`P-K`); `regenerate_derived.sh` runs only `tools/*.py` (`P-I`). The only record of "static build now, dynamic later" is a retired migration's comment (atom `ADD-002`, unconfirmed). Owner words: "dynamic rendering", "do not rely on artifacts". | **Delete**, then one renderer reading one view (step 3.R). Please confirm or deny the "static now" claim. | 1.4b, 3.R, C-027/C-028 |
| **D2** | Delete the two scheduled DB-writing workflows and their scripts? | `pipeline_runs`: 5 runs, `total_resolved` 0 in all, DOI and verified counts unchanged in each; phase-4 enrichment recorded 1, 1, 2 sources in the last three. No source has a NULL `verification_status`; `url_verification_runs` is empty. The workflows are why every open PR can inherit a binary DB conflict (rule 3). | **Delete.** First read what phase 4 writes, so nothing relied on is lost (evidence gap, step 1.4). | 1.4, C-029, `P-L` |
| **D3** | Branch state. PR #171 closed unmerged; the branch was recreated with batch-24 research plus the instrument. What happens to batch 24? | `git log --oneline origin/main..HEAD` | Land T1 first (0.1). Re-open the research as its own PR after the tooling PRs merge (Phase 5). Put the instrument and this plan on their own branch from `main`. | 0.5, 5 |
| **D4** | Re-baseline the migrations? | 1.6 s rebuild; provenance chain (§2) | **No.** | — |
| **D5** | Does "retire in place, never hard-delete" (LED-169/170) bar *dropping* wholly retired vocabulary tables (axes, splinter tables, item layer), whose rows stay in the migrations that created them? | Owner R3 (2026-08-18) says `axes` and `item_axis_links` are retired; LED-132 says no `population_*` link table may exist. | **No bar**: the rule is about rows in live tables. Please confirm. | 1.1–1.3 |
| **D6** | The two quarantined gates. | `register_integrity_check` is red by construction (frozen pilot document). `adjudication_integrity` is green and guards tier derivation, which every `stated` cell depends on (`P-TIER-DERIVE`). | Delete the first; **promote** the second to the registry proper. | 1.5, C-028 |
| **D7** | Doctrine ruling sheet — ten yes/no items: (a) mission: delete "teaches professional judgment" (C-001); (b) the two-marker line (C-002); (c) "seven tiers" wording and the tier-number-versus-quality statement (C-006); (d) does the 2026-07-20 directive lift the T3-grey-alone "pending" rule for *state*, or only claim strength (C-004)? (e) record LED-018 as amended by Option A (C-005); (f) Co-1 warrant: D-0178 governs; correct `co1-operational` (C-024/025); (g) jurisdiction §2.3 amendment and its decision record (C-049); (h) append the six session-only rulings to the ledger (C-036); (i) the replacement name for "population", or leave the word where the schema has it (C-018, `P-C`); (j) review D-0184, adopted but never reviewed (C-023). | each item's entry in `CONFLICTS.md` | Per entry; (d), (g) and (i) are the open readings. | 2.1, 2.2 |
| **D8** | Medical lens: the 2026-09-11 words ("ensure that medical gets filled out") govern over D-0184's "owner's alone"? | C-022; `P-MEDICAL` | **Yes**; scope = "all items presented to me". Execute `add-medical` in the research PR. | 5, C1.6 |
| **D9** | Cross-parameter synthesis structure. | Only one parameter has extractions. `extraction_relations` already allows an edge between rows of different parameters (0 live). | **Do not build.** Record a GAP; revisit when a second parameter has data. `C3` stays BLOCKED by design. | C-035, `P-X` |
| **D10** | R4 slug × lens coverage: is it evidenced by logged queries that name the lens term, with no new column or table? | `P-M`; `search_executions.terms_used` | **Yes**; delete `P-M`. | C-033 |
| **D11** | Base vocabulary tables with no `db.py` verb are migration-only (doctrine is owner-gated), so LED-182 ("add the verb") means research writes? | `P-O` | **Yes**; delete `P-O`. | C-034, C2.8 |
| **D12** | `not_applicable`: keep the value, unbuilt, flagged as such? | `P-ENG-STATE` | **Keep and flag**; build nothing now. | C-007 |
| **D13** | Two contract criteria whose subject may be dead. (a) `locator-title-matches-identifier` (Ruling 2.3): the gate is red on 31 clue-store titles and cannot be repaired without a new writer (code), though the clue store holds leads, not admitted evidence (LED-082/083). (b) `nine-step-synthesis` and the BPC validators (`validate_reasoning`, `validate_bpc`): is the BPC reasoning-document layer still a live deliverable? | the full run; 2 of 3 reasoning docs are templates; `reasoning_doc_citations` is empty | (a) retire the criterion and the check; (b) retire both if no BPC document is in progress. | 1.5 |

---

## 5. Sequence

Phases 0 and 1 need no owner decision except D2, D3, D5 where noted. Phase 2 needs the ruling sheet. Within a phase, steps run in the order written.

### Phase 0 — Hold the line

| step | change | net lines | done when |
|---|---|---|---|
| **0.1** | **Land T1** (owner-approved, LED-206): commit the stress-tested refactor in `guidebook-t1`, run the diff-scoped gate, open the PR, owner merges. The one sanctioned addition. First, so every later `db.py` deletion applies to its final text. Before merge: fix the views `P-H` lists on that tree (they name no lifecycle column), since T1 adds `retire-parameter`/`merge-parameter` (LED-171). | + (T1's own) | `P-V`, `P-W`, `P-PARAM-LIFECYCLE`, `P-H` pass on `main`; C1.3, C1.5, C2.5, C2.6 pass |
| **0.2** | `scripts/preserve_transcripts.py`: anchor `OUT` to the repository root (`Path(__file__).resolve().parents[1] / "transcripts"`), not the working directory. | 0 | no `transcripts/` directory ever appears under a subfolder |
| **0.3** | CLAUDE.md (owner merge): add R3; delete statements the stage graph shows false (C-020: "both sweeps are done"; C-027: "regenerate with `regenerate_derived.sh`", until D1 is decided). | − | `grep` of the removed claims returns nothing |
| **0.4** | `build_graph.py`: verify quotes only for atoms cited by a remaining conflict, machine, probe or predicate. | − | resolved entries no longer need their sources to stay verbatim |
| **0.5** | Branch hygiene per D3. | 0 | — |

### Phase 1 — Delete what is provably dead (agent, evidence in each commit)

| step | delete | evidence to put in the commit | net lines |
|---|---|---|---|
| **1.1** | **Item-layer cluster.** Tables `items`, `item_audit_runs`, `item_bpc_links`, `item_taxonomy_links`, `item_population_elaborations`, `term_item_links`, `room_items`, `case_study_specs`, `economics_entry_specs`, `spec_value_probes` (+ `probe_population_links`, view `v_pmp_latest_walk`), `jurisdictional_values`; verbs `add-item`, `items`, `add-audit-run`, `update-audit-run`, `audit-runs`, `add-jurisdictional-value`; scripts `audit_consolidator.py`, `pmp_audit.py`; their registry entries and the `pmp-strict-termination` criterion; the five skills `item-audit-pipeline`, `audit-consolidator`, `functional-deficit-auditor`, `economics-auditor`, `question-author` (edit `connection-discovery`). | all empty; `P-UNWRITABLE` lists them; verbs run ≤3 times in 49 sessions; the skills' item-layer hit counts; owner R1 (item codes bias research) and CLAUDE.md §7 | −2,121 measured (scripts 759, skills 1,362), plus verbs, DDL and registry entries, not yet measured |
| **1.2** | **Splinter and case-study children.** Drop the five `*_population*` link tables (`P-A`, ruled LED-132) and `case_study_outcomes`, `case_study_strategies`; keep `case_studies` (R12 names it). | 0 rows, no writer or an unreachable one; their harm/outcome content is extractions with `figure_role=finding` | − |
| **1.3** | **Axes retired as one act** (owner R3, "do not relitigate"; DRS-024 says not piecemeal): `axes`, `access_need_axis_map`, `population_axis_map`, `situations`, `slugs.serves_axes`, `validate_axes.py`, the blocking `validate_axes` entry. `population_icf_links` already replaces the map. | `P-AXIS`; ruling in `workplan/2026-08-18-handoff-next-session.md` R3 | −158 (`validate_axes.py`) + DDL |
| **1.4** | **Scheduled DB-writing workflows** (D2): `resolve-dois.yml`, `verify-urls.yml`, `resolve_dois.py`, `verify_urls.py`, `test_url_verifier.py`, `test_verification_pipeline.py`, tables `pipeline_runs`, `url_verification_runs`; shrink `migration_reproducibility`'s exempt list; then compare the deep and count-only reproducibility checks and keep one. | `pipeline_runs` result; empty NULL-verification pool; `P-L` | −2,777 + exempt-list code |
| **1.4b** | **Dashboards and generators** (D1): `regenerate-derived.yml`, `regenerate_derived.sh`, `tools/*.py` and `tools/*.html`, the seven render generators, `parts/` and `site/` if frozen output; check `site_pages_fresh` and, if their subject goes, `render_audit_browser`. | `P-I`, `P-K`; `site_pages_fresh` examines 0 | −7,674 lines of code + 5.7 MB of generated HTML |
| **1.5** | **Checks diet.** Rule K: a check stays only if it examined something on the last full run **and** guards something that reaches the book; a check a contract criterion names is deleted together with its criterion, in one PR the owner merges (the contract is ratified governance). *(a) Named by no criterion — delete:* `code_currency_audit` (234), `pre_rehab_banner_audit` (123), `register_integrity_check` (455, D6), `validate_pydantic_schemas` (365: 213 informational findings, an import error, a curated map rule 8 calls a violation), `population_integrity_audit` (191), `reasoning_doc_citations_audit` (171; its table is empty). *(b) Named, subject retired — delete with the criterion:* `validate_axes` (1.3), `pmp_audit` (1.1), `validate_population` (251; delete if the identity-lens table's own CHECK and FKs already enforce it — confirm first). *(c) Named, red, triage:* `validate_schema_cross_check` (compares to the archive), `retired_vocabulary` (86 hits; most disappear with 1.1–1.3), `research_protocol_audit`, `metadata_integrity_audit`, and the two owner items in D13. *Keep:* the three session-scoped gates and `medical_lens_integrity`. `migration_reproducibility_deep` is settled in 1.4. | the full-run list; contract mapping (`STATE-GRAPH.md` §3 and the contract's `check:` fields) | −1,539 measured for (a), plus (b) and the triage |
| **1.6** | **Skills diet.** Delete the 11 skills nothing live references, `skills/deprecated/`, and the symlinks. For the rest: keep iff a live contract, command, agent, script or registry entry names it (a snapshot migration and generated HTML do not count). | the reference sweep | −1,145 − 1,156 measured, plus triage |
| **1.7** | **Registry prose.** Delete `note`, `floor_basis`, `reason`, `prior_note` narratives; the record is `git log -p`. Behaviour-preserving. | CLAUDE.md "correction histories do not live here" | −1,137 measured (lines inside 84 string fields over 300 characters) |
| **1.8** | `workplan/deprecated/`, `workplan/_superseded/` (about 0.8 MB): delete; git is the archive. | the instrument's §B marks them historical or superseded | docs, not code |

### Phase 2 — Rulings to text (owner sheet, then agent edits)

| step | change | done when |
|---|---|---|
| **2.1** | Owner answers D1–D13 in one sitting (D1–D6 gate steps in Phase 1; D7–D13 gate Phases 2–3). | decisions recorded in the ledger (append-only), no agent-authored ruling |
| **2.2** | Apply them by **deleting** stale clauses, not annotating: the methodology's `(parameter × population)` lines, `co1-operational` sub-type and verification lists, hand-written counts, the cell-state transition table (the engine recomputes state), mission lines (owner). Add the one-line `BY:` pointers for every entry of `status_corrections` in `conflicts.yaml` (the repo's own supersession mechanism); append the six session-only rulings to the ledger. | every status correction and C-001/002/006/007/008/010/011/014/015/016/023/024/025/030/036/038/039/040/041/042/043/044/045/047/049/050 leave `conflicts.yaml` |

### Phase 3 — Repair what remains, along the spine

| stage | change | probes → pass |
|---|---|---|
| **base** | Apply D11 (delete `P-O`); apply D5/C-018 outcome for the word *population* (rename is the owner's; delete nothing further); classify tables in the stage-map (C-011). | `P-AXIS`, `P-C` per D7 |
| **research** | D10: delete `P-M`. `M01` has no from-state guard; leave and document. | — |
| **evidence** | **Retire `data_capture_status`** (a derived duplicate of "does a capture row exist"; `add-extraction`'s own comment calls the column "in the wrong home"; claim_type `absent` already records "looked, nothing found"): writer-retire in `add-extraction`/`derive-extraction`, reader-retire `C06`/`C07`, NULL forward, then drop. **Tier as a stored derivation** (C-013, rule 8): a `tier_rules(evidence_type, scope, tier)` table and one view replace `evidence_sources.tier`, `add-source --tier`, `adjudication_integrity`'s comparison and the B5a gate — *design to be shown to the owner before building*; net-negative or it does not proceed. Fix `Co1SourceType` against the live values. | `P-STATUS-WRITERS`, `P-F`, `P-TIER-DERIVE`, `P-CO1-TYPE` |
| **judgment** | Stage-map: `source_value_extractions` → judgment (C-012; owner words LED-106 as adopted). Delete the slug-admission refusal in `insert_extraction` once D1 deletes the vetting surface it protected (C-032): the scan contract says slugs guide search only. | `P-STAGE-SVE`, `P-V2` |
| **synthesis** | D9: none built. Classify the forward FKs (`reasoning_doc_citations`, `gaps`) in the stage-map (C-046). | `P-FWD-FK` reviewed |
| **specification** | C-004 per D7(d): if the directive reaches state, change the T3-grey branch (a few lines in `determine`); if not, delete the contradicting prose. `determination_gates` carries `identity_code` only: add the lens columns, or point at the determination (rule 5) — decide after a `repo-sweep` of its readers. | `P-GT`, `P-ENG-T3` |
| **render** | **3.R** One renderer (target ≤300 lines) over one view that already carries the marker, strength flag and evidence trail, so the register invariants hold by construction and `register_integrity_check` has nothing to check. Exception to R3, named: it replaces 2,438 lines of generators. | `P-K`, `P-I`, C4.6–C4.8 |

### Phase 4 — Second-order reduction (what is left after the deletions)

| step | change |
|---|---|
| **4.1** | `db.py`/`dbcore.py`: delete verbs run ≤3 times with no remaining table; re-sweep. Gate G3. |
| **4.2** | `schemas/*.py`: keep only modules the engine imports (`directness`, `tier_derivation`, enums in use); the table mirrors are a second home for the schema (rule 5). Evidence: import graph. |
| **4.3** | Optional: comment diet in `db.py` (docstring narrative to commit messages). Behaviour-preserving, large, low value; skip unless review time is available. |

### Phase 5 — Research PR

Batch-24 rows (and, per D8, the medical-registry rows through `add-medical`) as their own PR after every tooling PR has merged (rule 10). `research_batch_dod.py` on `scratchpad/CURRENT`. Open last; unsubscribe.

### Phase 6 — Retire the scaffolding

When `conflicts.yaml` is empty: delete `atoms/`, `ATOMS.tsv`, `AMBIGUITIES.tsv`, `OPEN-QUESTIONS.tsv`, `graph.json`, the quote and conflict code in `build_graph.py`. Keep the derived stage graph and the probes that still test a standing ruling no other gate holds. Delete this file.

---

## 6. The stage graph, by stage

Generated from `graph.json`, the stage-map, the contract and the conflict register. Conflict-to-stage is by judgment (the atoms' own stage tags were too noisy); `layer 0 / cross` collects the conflicts about records, process and documents that belong to no stage.

| stage | tables | rows | empty | no writer | unwritable | forward FKs from here | verbs writing only here | checks the contract names | machines | conflicts | steps |
|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 23 | 2995 | 5 | 15 | 1 | 1 | 8 | 10 | M03 | C-011, C-017, C-018, C-022, C-034, C-049, C-050 | 1.1, 1.2, 1.3, 3 (base), 5 |
| research | 11 | 1525 | 4 | 3 | 0 | 4 | 12 | 2 | M01, M09 | C-033 | 3 (research) |
| evidence | 17 | 460 | 10 | 8 | 6 | 4 | 13 | 4 | M02, M03 | C-006, C-009, C-013, C-015, C-024, C-025, C-026, C-048 | 1.4, 3 (evidence) |
| judgment | 5 | 132 | 3 | 3 | 2 | 3 | 3 | 2 | M03, M04 | C-012, C-014, C-032 | 0.1, 3 (judgment) |
| synthesis | 8 | 150 | 5 | 3 | 0 | 1 | 10 | 1 | M07 | C-035, C-046 | 3 (synthesis) |
| specification | 5 | 198 | 1 | 3 | 1 | 1 | 3 | 3 | M05, M06 | C-003, C-004, C-007, C-008, C-021, C-040 | 3 (specification) |
| render | 6 | 5 | 5 | 6 | 4 | 0 | 0 | 1 | — | C-005, C-027, C-028, C-031 | 1.4b, 3.R |
| infrastructure | 7 | 743 | 2 | 3 | 1 | 0 | 6 | 0 | — | — | 1.4, 1.5 |
| layer 0 / cross | — | — | — | — | — | — | — | — | M10 | C-001, C-002, C-010, C-016, C-019, C-020, C-023, C-029, C-030, C-036, C-037, C-038, C-039, C-041, C-042, C-043, C-044, C-045, C-047 | 0.2–0.5, 1.5–1.8, 2.x, 4.x, 6 |

Regenerate: `python3 workplan/pipeline-state-graph/build_graph.py` (tables, writers, flags, forward FKs), then group by `governance/stage-map.yaml` and `governance/pipeline-contract.yaml` criteria. Verbs are counted only where every table they write sits in the stage; a verb writing across stages is in none of the rows. The `infrastructure` row is not a spine stage.

**Capability predicates still failing after the plan** (by construction, not by omission): C3.5 (D9 — nothing to synthesize yet). All others are targeted above.

---

## 7. Where every issue goes

| step | conflicts | probes not passing | capability predicates |
|---|---|---|---|
| 0.1 | C-031 | P-H, P-V, P-W, P-PARAM-LIFECYCLE | C1.3, C1.5, C2.5, C2.6 |
| 0.1, 3 judgment | C-032 | — | — |
| 0.1, D11 | C-034 | — | — |
| 1.1 | C-019, C-026 | — | — |
| 1.1, 1.2, 5 | — | P-UNWRITABLE | — |
| 1.2 | C-020 | P-A | — |
| 1.2, 3 specification | — | P-B | — |
| 1.3 | C-017 | P-AXIS | — |
| 1.4 | — | P-L | — |
| 1.4b, 3.R | — | P-I | C4.7 |
| 1.6, 2.2 | C-037 | — | — |
| 2.1 | C-039, C-044 | — | — |
| 2.1 (D7a), 2.2 | C-001 | — | — |
| 2.1 (D7c), 2.2 | C-006 | — | — |
| 2.1 (D7d), 3 specification | C-004 | — | — |
| 2.1 (D7e), 2.2 | C-005 | — | — |
| 2.1 (D7f), 2.2 | C-024 | — | — |
| 2.1 (D7g), 2.2 | C-049 | — | — |
| 2.1 (D7h), 2.2 | C-036 | — | — |
| 2.1 (D7i) | — | P-C | — |
| 2.1 (D7i), 3 base | C-018 | — | — |
| 2.1 (D7j), 2.2 | C-023 | — | — |
| 2.2 | C-003, C-008, C-010, C-014, C-015, C-016, C-030, C-038, C-040, C-041, C-042, C-043, C-045, C-047, C-050 | P-LEDGER-GREP | — |
| 2.2 (D12) | C-007 | — | — |
| 2.2 (D7b) | C-002 | — | — |
| 2.2, 3 evidence | C-025 | — | — |
| 3 base | C-011 | — | — |
| 3 evidence | C-009, C-013, C-048 | P-F, P-CO1-TYPE, P-STATUS-WRITERS | — |
| 3 judgment | C-012 | P-V2, P-STAGE-SVE | C1.4 |
| 3 specification | C-021 | P-GT | — |
| 3 synthesis | C-046 | P-FWD-FK | — |
| 3.R | — | P-K | C4.6 |
| 5 | — | P-MEDICAL | C1.6 |
| D1, 1.4b, 3.R | C-027 | — | — |
| D10 | — | P-M | C1.8 |
| D10, 3 research | C-033 | — | — |
| D11 | — | P-O | C2.8 |
| D12 | — | P-ENG-STATE | C4.4 |
| D2, 1.4 | C-029 | — | — |
| D6, 1.5 | — | P-TIER-DERIVE | — |
| D6, 1.5, 3.R | C-028 | — | — |
| D6, 3.R | — | P-QUARANTINE | C4.8 |
| D8, 5 | C-022 | — | — |
| D9 | — | P-X | — |
| D9 (deferred) | C-035 | — | — |
| D9 (stays blocked) | — | — | C3.5 |

**Status corrections (the `status_corrections` list, 13 entries today):** LED-029, LED-018, DRS-039, DRS-040, OPI-229, WRK-003, WRK-033, WRK-171, WRK-172, WRK-004, WRK-173, WRK-043, WRK-068 → step 2.2 (one-line `BY:` pointers).

**Red and empty checks:** the nine red advisories and seven that examined nothing (last full run) → 1.4 (`migration_reproducibility_deep`), 1.1 (`pmp_audit`), 1.4b (`site_pages_fresh`), 1.5 (the rest), D13.

**Process issues:** stray transcript copies under a subfolder → 0.2; T1 refactor uncommitted → 0.1; closed PR #171 and the recreated branch → D3, 0.5; probes that tested the wrong function or a comment, and quote checks that would go red for resolved reasons → 0.4, R9, Phase 6; atoms from the 2026-08-18 workplan files sampled only 30 of 252 → retired with the scaffolding (Phase 6) unless a remaining entry cites them; the stop hook flagging append-only logs → no step (`git config stophook.ignorePath` already excludes `transcripts/` and `*commands.jsonl`; CLAUDE.md §7).

---

## 8. What this plan does not do, and what I could not check

- It does not decide any ruling. Directions in the register are inferences from rule 0; two independent passes corrected them once and neither is proof.
- The deletion line counts are file sizes today. Items marked *estimate* depend on the per-step sweep; items marked *triage* depend on reading the check or skill. No step is approved until its sweep is attached.
- **Not checked:** what the cron's phase 4 writes (step 1.4); whether the BPC layer (`validate_bpc`, `validate_reasoning`) has any live subject; the readers of `determination_gates`; the actual size of a renderer; whether `rename_insurance.py` is item-layer (it shows 7 item-layer hits; the sweep decides).
- The 49 command logs begin when the hook did; a verb unused in them may have been used earlier.
- Rule R3 is a process rule, not a gate; it fails the way every unenforced rule here has.
